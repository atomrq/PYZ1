from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isclose, isfinite
from typing import TYPE_CHECKING, Final

from pyz1.output_io import format_summary_text, read_summary_file
from pyz1.ppa import (
    PpaSettings,
    accelerated_ppa_settings,
    run_ppa,
    standard_ppa_settings,
)
from pyz1.z1_io import read_z1_file

if TYPE_CHECKING:
    from pathlib import Path

SUMMARY_TOLERANCE: Final = 1.0e-6
SUMMARY_FIELD_NAMES: Final = (
    "timestep",
    "true_chain_count",
    "mean_original_beads",
    "mean_squared_end_to_end",
    "mean_shortest_path_contour",
    "mean_entanglements",
    "coil_tube_diameter",
    "coil_tube_step_length",
    "root_mean_squared_contour",
    "ne_classical_kink",
    "ne_modified_kink",
    "ne_classical_coil",
    "ne_modified_coil",
    "mean_original_bond_length",
    "original_bead_density",
)


class PpaRegressionMode(StrEnum):
    STANDARD = "ppa"
    ACCELERATED = "ppaplus"


class PpaRegressionStatus(StrEnum):
    PASSED = "passed"
    MISMATCH = "mismatch"
    KNOWN_INVALID = "known-invalid"


@dataclass(frozen=True, slots=True)
class PpaRegressionSettingsOverride:
    mode: PpaRegressionMode
    settings: PpaSettings


@dataclass(frozen=True, slots=True)
class PpaRegressionRequest:
    source_dir: Path
    oracle_root: Path
    report_path: Path
    modes: tuple[PpaRegressionMode, ...]
    benchmark_ids: tuple[str, ...]
    max_node_count: int = 500
    settings_overrides: tuple[PpaRegressionSettingsOverride, ...] = ()


@dataclass(frozen=True, slots=True)
class PpaSummaryFieldMismatch:
    field_name: str
    actual: str
    expected: str


@dataclass(frozen=True, slots=True)
class PpaRegressionRecord:
    benchmark_id: str
    mode: PpaRegressionMode
    status: PpaRegressionStatus
    mean_shortest_path_contour_delta: float | None
    ne_classical_coil_delta: float | None
    ne_modified_coil_delta: float | None
    summary_field_mismatches: int | None
    summary_field_mismatch_details: tuple[PpaSummaryFieldMismatch, ...] | None
    node_count: int | None
    note: str


def write_ppa_regression_report(
    request: PpaRegressionRequest,
) -> tuple[PpaRegressionRecord, ...]:
    records = tuple(
        _compare_benchmark_mode(request, benchmark_id, mode)
        for benchmark_id in request.benchmark_ids
        for mode in request.modes
    )
    request.report_path.parent.mkdir(parents=True, exist_ok=True)
    _ = request.report_path.write_text(_format_report(records), encoding="utf-8")
    return records


def _compare_benchmark_mode(
    request: PpaRegressionRequest,
    benchmark_id: str,
    mode: PpaRegressionMode,
) -> PpaRegressionRecord:
    source_path = request.source_dir / f".benchmark-{benchmark_id}.Z1"
    summary_path = (
        request.oracle_root
        / f"benchmark-{benchmark_id}"
        / mode.value
        / _summary_filename(mode)
    )
    if not source_path.exists() or not summary_path.exists():
        return _known_invalid_record(
            benchmark_id=benchmark_id,
            mode=mode,
            note="missing source or oracle PPA summary",
        )

    snapshot = read_z1_file(source_path)
    if snapshot.node_count > request.max_node_count:
        return _known_invalid_record(
            benchmark_id=benchmark_id,
            mode=mode,
            note=f"skipped: node_count>{request.max_node_count}",
            node_count=snapshot.node_count,
        )

    result = run_ppa(snapshot, _settings_for_mode(mode, request.settings_overrides))
    oracle_summary = read_summary_file(summary_path)[0]
    actual_summary = result.summary.record
    lpp_delta = abs(
        actual_summary.mean_shortest_path_contour
        - oracle_summary.mean_shortest_path_contour,
    )
    ne_classical_delta = abs(
        actual_summary.ne_classical_coil - oracle_summary.ne_classical_coil,
    )
    ne_modified_delta = abs(
        actual_summary.ne_modified_coil - oracle_summary.ne_modified_coil,
    )
    details = _summary_field_mismatches(
        format_summary_text((actual_summary,)),
        summary_path.read_text(encoding="utf-8"),
    )
    status = classify_ppa_summary_deltas(
        lpp_delta=lpp_delta,
        ne_classical_delta=ne_classical_delta,
        ne_modified_delta=ne_modified_delta,
    )
    return PpaRegressionRecord(
        benchmark_id=benchmark_id,
        mode=mode,
        status=status,
        mean_shortest_path_contour_delta=lpp_delta,
        ne_classical_coil_delta=ne_classical_delta,
        ne_modified_coil_delta=ne_modified_delta,
        summary_field_mismatches=len(details),
        summary_field_mismatch_details=details,
        node_count=snapshot.node_count,
        note=_note_for_deltas(
            status=status,
            lpp_delta=lpp_delta,
            ne_classical_delta=ne_classical_delta,
            ne_modified_delta=ne_modified_delta,
        ),
    )


def _known_invalid_record(
    *,
    benchmark_id: str,
    mode: PpaRegressionMode,
    note: str,
    node_count: int | None = None,
) -> PpaRegressionRecord:
    return PpaRegressionRecord(
        benchmark_id=benchmark_id,
        mode=mode,
        status=PpaRegressionStatus.KNOWN_INVALID,
        mean_shortest_path_contour_delta=None,
        ne_classical_coil_delta=None,
        ne_modified_coil_delta=None,
        summary_field_mismatches=None,
        summary_field_mismatch_details=None,
        node_count=node_count,
        note=note,
    )


def _settings_for_mode(
    mode: PpaRegressionMode,
    overrides: tuple[PpaRegressionSettingsOverride, ...],
) -> PpaSettings:
    for override in overrides:
        if override.mode == mode:
            return override.settings
    match mode:
        case PpaRegressionMode.STANDARD:
            return standard_ppa_settings()
        case PpaRegressionMode.ACCELERATED:
            return accelerated_ppa_settings()


def _summary_filename(mode: PpaRegressionMode) -> str:
    match mode:
        case PpaRegressionMode.STANDARD:
            return "PPA-summary.dat"
        case PpaRegressionMode.ACCELERATED:
            return "PPA+summary.dat"


def classify_ppa_summary_deltas(
    *,
    lpp_delta: float,
    ne_classical_delta: float,
    ne_modified_delta: float,
) -> PpaRegressionStatus:
    if not _summary_deltas_are_finite(
        lpp_delta=lpp_delta,
        ne_classical_delta=ne_classical_delta,
        ne_modified_delta=ne_modified_delta,
    ):
        return PpaRegressionStatus.KNOWN_INVALID
    if (
        isclose(lpp_delta, 0.0, abs_tol=SUMMARY_TOLERANCE)
        and isclose(ne_classical_delta, 0.0, abs_tol=SUMMARY_TOLERANCE)
        and isclose(ne_modified_delta, 0.0, abs_tol=SUMMARY_TOLERANCE)
    ):
        return PpaRegressionStatus.PASSED
    return PpaRegressionStatus.MISMATCH


def _summary_deltas_are_finite(
    *,
    lpp_delta: float,
    ne_classical_delta: float,
    ne_modified_delta: float,
) -> bool:
    return (
        isfinite(lpp_delta)
        and isfinite(ne_classical_delta)
        and isfinite(ne_modified_delta)
    )


def _note_for_deltas(
    *,
    status: PpaRegressionStatus,
    lpp_delta: float,
    ne_classical_delta: float,
    ne_modified_delta: float,
) -> str:
    if not _summary_deltas_are_finite(
        lpp_delta=lpp_delta,
        ne_classical_delta=ne_classical_delta,
        ne_modified_delta=ne_modified_delta,
    ):
        return "native PPA summary contains non-finite values"
    return _note_for_status(status)


def _note_for_status(status: PpaRegressionStatus) -> str:
    match status:
        case PpaRegressionStatus.PASSED:
            return "within current PPA summary tolerance"
        case PpaRegressionStatus.MISMATCH:
            return "current native PPA output differs from oracle summary"
        case PpaRegressionStatus.KNOWN_INVALID:
            return "oracle unavailable or invalid"


def _summary_field_mismatches(
    actual_text: str,
    expected_text: str,
) -> tuple[PpaSummaryFieldMismatch, ...]:
    actual_fields = actual_text.split()
    expected_fields = expected_text.split()
    shared_count = min(len(actual_fields), len(expected_fields))
    mismatches = tuple(
        PpaSummaryFieldMismatch(
            field_name=_summary_field_name(index),
            actual=actual_fields[index],
            expected=expected_fields[index],
        )
        for index in range(shared_count)
        if actual_fields[index] != expected_fields[index]
    )
    if len(actual_fields) == len(expected_fields):
        return mismatches
    return (
        *mismatches,
        PpaSummaryFieldMismatch(
            field_name="field_count",
            actual=str(len(actual_fields)),
            expected=str(len(expected_fields)),
        ),
    )


def _summary_field_name(index: int) -> str:
    if index < len(SUMMARY_FIELD_NAMES):
        return SUMMARY_FIELD_NAMES[index]
    return f"field_{index + 1}"


def _format_report(records: tuple[PpaRegressionRecord, ...]) -> str:
    lines = [
        "# pyz1 native PPA summary regression",
        "",
        (
            "| benchmark | mode | status | nodes | Lpp delta | "
            "Ne classical coil delta | Ne modified coil delta | "
            "summary field mismatches | summary mismatch details | note |"
        ),
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    lines.extend(_format_record(record) for record in records)
    return "\n".join(lines) + "\n"


def _format_record(record: PpaRegressionRecord) -> str:
    return (
        f"| benchmark-{record.benchmark_id} | {record.mode.value} | "
        f"{record.status.value} | {_format_optional_int(record.node_count)} | "
        f"{_format_optional_float(record.mean_shortest_path_contour_delta)} | "
        f"{_format_optional_float(record.ne_classical_coil_delta)} | "
        f"{_format_optional_float(record.ne_modified_coil_delta)} | "
        f"{_format_optional_int(record.summary_field_mismatches)} | "
        f"{_format_summary_field_details(record.summary_field_mismatch_details)} | "
        f"{record.note} |"
    )


def _format_optional_float(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.6g}"


def _format_optional_int(value: int | None) -> str:
    if value is None:
        return "n/a"
    return str(value)


def _format_summary_field_details(
    details: tuple[PpaSummaryFieldMismatch, ...] | None,
) -> str:
    if details is None:
        return "n/a"
    if len(details) == 0:
        return "none"
    return "; ".join(
        f"{detail.field_name}: {detail.actual} != {detail.expected}"
        for detail in details
    )
