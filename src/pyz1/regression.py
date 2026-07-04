from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isclose
from typing import TYPE_CHECKING, Final

from pyz1.output_io import (
    format_shortest_path_text,
    parse_shortest_path_text,
    read_summary_file,
)
from pyz1.reducer import ReducerSettings, reduce_snapshot
from pyz1.z1_io import read_z1_file

if TYPE_CHECKING:
    from pathlib import Path

    from pyz1.output_models import ShortestPathPair, ShortestPathSnapshot

LPP_TOLERANCE: Final = 1.0e-6
Z_TOLERANCE: Final = 1.0e-6


class RegressionMode(StrEnum):
    DEFAULT = "default"
    SPPLUS = "spplus"


class RegressionStatus(StrEnum):
    PASSED = "passed"
    MISMATCH = "mismatch"
    KNOWN_INVALID = "known-invalid"


@dataclass(frozen=True, slots=True)
class RegressionRequest:
    source_dir: Path
    oracle_root: Path
    report_path: Path
    modes: tuple[RegressionMode, ...]
    benchmark_ids: tuple[str, ...]
    max_node_count: int = 500


@dataclass(frozen=True, slots=True)
class PairingComparison:
    mismatched_pair_count: int


@dataclass(frozen=True, slots=True)
class RegressionRecord:
    benchmark_id: str
    mode: RegressionMode
    status: RegressionStatus
    lpp_delta: float | None
    z_delta: float | None
    pairing_mismatches: int | None
    note: str


def compare_spplus_pairing(
    actual_text: str,
    expected_text: str,
) -> PairingComparison:
    actual = parse_shortest_path_text(actual_text)
    expected = parse_shortest_path_text(expected_text)
    actual_pairs = _pair_sequence(actual)
    expected_pairs = _pair_sequence(expected)
    shared_count = min(len(actual_pairs), len(expected_pairs))
    mismatch_count = abs(len(actual_pairs) - len(expected_pairs)) + sum(
        actual_pairs[index] != expected_pairs[index] for index in range(shared_count)
    )
    return PairingComparison(mismatched_pair_count=mismatch_count)


def write_benchmark_regression_report(
    request: RegressionRequest,
) -> tuple[RegressionRecord, ...]:
    records = tuple(
        _compare_benchmark_mode(request, benchmark_id, mode)
        for benchmark_id in request.benchmark_ids
        for mode in request.modes
    )
    request.report_path.parent.mkdir(parents=True, exist_ok=True)
    _ = request.report_path.write_text(_format_report(records), encoding="utf-8")
    return records


def _compare_benchmark_mode(
    request: RegressionRequest,
    benchmark_id: str,
    mode: RegressionMode,
) -> RegressionRecord:
    source_path = request.source_dir / f".benchmark-{benchmark_id}.Z1"
    oracle_dir = request.oracle_root / f"benchmark-{benchmark_id}" / mode.value
    summary_path = oracle_dir / _summary_filename(mode)
    sp_path = oracle_dir / "Z1+SP.dat"
    if not source_path.exists() or not summary_path.exists() or not sp_path.exists():
        return RegressionRecord(
            benchmark_id=benchmark_id,
            mode=mode,
            status=RegressionStatus.KNOWN_INVALID,
            lpp_delta=None,
            z_delta=None,
            pairing_mismatches=None,
            note="missing source or oracle output",
        )
    snapshot = read_z1_file(source_path)
    if snapshot.node_count > request.max_node_count:
        return RegressionRecord(
            benchmark_id=benchmark_id,
            mode=mode,
            status=RegressionStatus.KNOWN_INVALID,
            lpp_delta=None,
            z_delta=None,
            pairing_mismatches=None,
            note=f"skipped: node_count>{request.max_node_count}",
        )
    result = reduce_snapshot(snapshot, _settings_for_mode(mode))
    oracle_summary = read_summary_file(summary_path)[0]
    actual_summary = result.summary.record
    lpp_delta = abs(
        actual_summary.mean_shortest_path_contour
        - oracle_summary.mean_shortest_path_contour,
    )
    z_delta = abs(actual_summary.mean_entanglements - oracle_summary.mean_entanglements)
    pairing_mismatches = _pairing_mismatch_count(mode, result.shortest_path, sp_path)
    status = _status_from_deltas(lpp_delta, z_delta, pairing_mismatches)
    return RegressionRecord(
        benchmark_id=benchmark_id,
        mode=mode,
        status=status,
        lpp_delta=lpp_delta,
        z_delta=z_delta,
        pairing_mismatches=pairing_mismatches,
        note=_note_for_status(status),
    )


def _settings_for_mode(mode: RegressionMode) -> ReducerSettings:
    match mode:
        case RegressionMode.DEFAULT:
            return ReducerSettings()
        case RegressionMode.SPPLUS:
            return ReducerSettings(pairing_enabled=True)


def _summary_filename(mode: RegressionMode) -> str:
    match mode:
        case RegressionMode.DEFAULT:
            return "Z1+summary.dat"
        case RegressionMode.SPPLUS:
            return "Z1+summary.dat"


def _pairing_mismatch_count(
    mode: RegressionMode,
    actual: ShortestPathSnapshot,
    expected_path: Path,
) -> int | None:
    match mode:
        case RegressionMode.DEFAULT:
            return None
        case RegressionMode.SPPLUS:
            comparison = compare_spplus_pairing(
                format_shortest_path_text(actual),
                expected_path.read_text(encoding="utf-8"),
            )
            return comparison.mismatched_pair_count


def _status_from_deltas(
    lpp_delta: float,
    z_delta: float,
    pairing_mismatches: int | None,
) -> RegressionStatus:
    pairing_clean = pairing_mismatches is None or pairing_mismatches == 0
    if (
        isclose(lpp_delta, 0.0, abs_tol=LPP_TOLERANCE)
        and isclose(z_delta, 0.0, abs_tol=Z_TOLERANCE)
        and pairing_clean
    ):
        return RegressionStatus.PASSED
    return RegressionStatus.MISMATCH


def _note_for_status(status: RegressionStatus) -> str:
    match status:
        case RegressionStatus.PASSED:
            return "within current tolerance"
        case RegressionStatus.MISMATCH:
            return "current clean-room reducer differs from oracle"
        case RegressionStatus.KNOWN_INVALID:
            return "oracle unavailable or invalid"


def _pair_sequence(
    snapshot: ShortestPathSnapshot,
) -> tuple[ShortestPathPair | None, ...]:
    return tuple(
        node.pair
        for chain in snapshot.chains
        for node in chain.nodes
        if node.is_entanglement
    )


def _format_report(records: tuple[RegressionRecord, ...]) -> str:
    lines = [
        "# pyz1 Benchmark Regression",
        "",
        "| benchmark | mode | status | Lpp delta | Z delta | pair mismatches | note |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    lines.extend(_format_record(record) for record in records)
    return "\n".join(lines) + "\n"


def _format_record(record: RegressionRecord) -> str:
    return (
        f"| benchmark-{record.benchmark_id} | {record.mode.value} | "
        f"{record.status.value} | {_format_optional_float(record.lpp_delta)} | "
        f"{_format_optional_float(record.z_delta)} | "
        f"{_format_optional_int(record.pairing_mismatches)} | {record.note} |"
    )


def _format_optional_float(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.6g}"


def _format_optional_int(value: int | None) -> str:
    if value is None:
        return "n/a"
    return str(value)
