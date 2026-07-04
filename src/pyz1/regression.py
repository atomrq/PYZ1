from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isclose, sqrt
from typing import TYPE_CHECKING, Final

from pyz1.output_io import (
    format_shortest_path_text,
    format_summary_text,
    parse_shortest_path_text,
    read_summary_file,
)
from pyz1.reducer import ReducerSettings, reduce_snapshot
from pyz1.z1_io import read_z1_file
from pyz1.z1_log import (
    Z1ReducerScanDiagnostics,
    read_z1_log_file,
    reducer_scan_diagnostics,
)

if TYPE_CHECKING:
    from pathlib import Path

    from pyz1.models import Vector3
    from pyz1.output_models import ShortestPathPair, ShortestPathSnapshot
    from pyz1.reducer import CoreTraceNode, ProjectionTrace

LPP_TOLERANCE: Final = 1.0e-6
Z_TOLERANCE: Final = 1.0e-6
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
class SummaryFieldMismatch:
    field_name: str
    actual: str
    expected: str


@dataclass(frozen=True, slots=True)
class RegressionRecord:
    benchmark_id: str
    mode: RegressionMode
    status: RegressionStatus
    lpp_delta: float | None
    z_delta: float | None
    summary_field_mismatches: int | None
    summary_field_mismatch_details: tuple[SummaryFieldMismatch, ...] | None
    pairing_mismatches: int | None
    node_count_mismatches: int | None
    max_node_position_delta: float | None
    pyz1_core_node_count: int | None
    pyz1_final_node_count: int | None
    pyz1_core_trace_node_count: int | None
    pyz1_core_trace_ghost_nodes: int | None
    pyz1_core_accepted_blocked_moves: int | None
    pyz1_core_transient_blocked_nodes: int | None
    pyz1_first_trace_blocker_chain: int | None
    pyz1_first_trace_blocker_node: int | None
    pyz1_first_trace_shortcut_fraction: float | None
    pyz1_first_trace_blocker_fraction: float | None
    pyz1_first_trace_blocker_distance: float | None
    pyz1_projection_trace_count: int | None
    pyz1_first_projection_responsible_chain: int | None
    pyz1_first_projection_responsible_node: int | None
    pyz1_first_projection_responsible_fraction: float | None
    oracle_core_node_count: int | None
    oracle_final_node_count: int | None
    oracle_core_crossings: int | None
    oracle_core_ghost_nodes: int | None
    note: str


@dataclass(frozen=True, slots=True)
class ShortestPathGeometryComparison:
    node_count_mismatches: int
    max_node_position_delta: float


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
            summary_field_mismatches=None,
            summary_field_mismatch_details=None,
            pairing_mismatches=None,
            node_count_mismatches=None,
            max_node_position_delta=None,
            pyz1_core_node_count=None,
            pyz1_final_node_count=None,
            pyz1_core_trace_node_count=None,
            pyz1_core_trace_ghost_nodes=None,
            pyz1_core_accepted_blocked_moves=None,
            pyz1_core_transient_blocked_nodes=None,
            pyz1_first_trace_blocker_chain=None,
            pyz1_first_trace_blocker_node=None,
            pyz1_first_trace_shortcut_fraction=None,
            pyz1_first_trace_blocker_fraction=None,
            pyz1_first_trace_blocker_distance=None,
            pyz1_projection_trace_count=None,
            pyz1_first_projection_responsible_chain=None,
            pyz1_first_projection_responsible_node=None,
            pyz1_first_projection_responsible_fraction=None,
            oracle_core_node_count=None,
            oracle_final_node_count=None,
            oracle_core_crossings=None,
            oracle_core_ghost_nodes=None,
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
            summary_field_mismatches=None,
            summary_field_mismatch_details=None,
            pairing_mismatches=None,
            node_count_mismatches=None,
            max_node_position_delta=None,
            pyz1_core_node_count=None,
            pyz1_final_node_count=None,
            pyz1_core_trace_node_count=None,
            pyz1_core_trace_ghost_nodes=None,
            pyz1_core_accepted_blocked_moves=None,
            pyz1_core_transient_blocked_nodes=None,
            pyz1_first_trace_blocker_chain=None,
            pyz1_first_trace_blocker_node=None,
            pyz1_first_trace_shortcut_fraction=None,
            pyz1_first_trace_blocker_fraction=None,
            pyz1_first_trace_blocker_distance=None,
            pyz1_projection_trace_count=None,
            pyz1_first_projection_responsible_chain=None,
            pyz1_first_projection_responsible_node=None,
            pyz1_first_projection_responsible_fraction=None,
            oracle_core_node_count=None,
            oracle_final_node_count=None,
            oracle_core_crossings=None,
            oracle_core_ghost_nodes=None,
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
    summary_field_mismatch_details = _summary_field_mismatches(
        format_summary_text((actual_summary,)),
        summary_path.read_text(encoding="utf-8"),
    )
    summary_field_mismatches = len(summary_field_mismatch_details)
    pairing_mismatches = _pairing_mismatch_count(mode, result.shortest_path, sp_path)
    geometry_comparison = _shortest_path_geometry_comparison(
        result.shortest_path,
        sp_path.read_text(encoding="utf-8"),
    )
    oracle_diagnostics = _oracle_reducer_diagnostics(oracle_dir / "log-stats.Z1")
    first_trace_node = _first_core_trace_node(
        result.diagnostics.core_trace_blocked_nodes,
    )
    first_projection = _first_projection_trace(result.diagnostics.projection_traces)
    status = _status_from_deltas(lpp_delta, z_delta, pairing_mismatches)
    return RegressionRecord(
        benchmark_id=benchmark_id,
        mode=mode,
        status=status,
        lpp_delta=lpp_delta,
        z_delta=z_delta,
        summary_field_mismatches=summary_field_mismatches,
        summary_field_mismatch_details=summary_field_mismatch_details,
        pairing_mismatches=pairing_mismatches,
        node_count_mismatches=geometry_comparison.node_count_mismatches,
        max_node_position_delta=geometry_comparison.max_node_position_delta,
        pyz1_core_node_count=result.diagnostics.core_node_count,
        pyz1_final_node_count=result.diagnostics.final_node_count,
        pyz1_core_trace_node_count=result.diagnostics.core_trace_node_count,
        pyz1_core_trace_ghost_nodes=result.diagnostics.core_trace_ghost_node_count,
        pyz1_core_accepted_blocked_moves=(
            result.diagnostics.core_accepted_blocked_move_count
        ),
        pyz1_core_transient_blocked_nodes=(
            result.diagnostics.core_transient_blocked_node_count
        ),
        pyz1_first_trace_blocker_chain=(
            first_trace_node.blocker_chain_index
            if first_trace_node is not None
            else None
        ),
        pyz1_first_trace_blocker_node=(
            first_trace_node.blocker_node_index
            if first_trace_node is not None
            else None
        ),
        pyz1_first_trace_shortcut_fraction=(
            first_trace_node.shortcut_fraction
            if first_trace_node is not None
            else None
        ),
        pyz1_first_trace_blocker_fraction=(
            first_trace_node.blocker_fraction
            if first_trace_node is not None
            else None
        ),
        pyz1_first_trace_blocker_distance=(
            first_trace_node.blocker_distance
            if first_trace_node is not None
            else None
        ),
        pyz1_projection_trace_count=len(result.diagnostics.projection_traces),
        pyz1_first_projection_responsible_chain=(
            first_projection.responsible_chain_index
            if first_projection is not None
            else None
        ),
        pyz1_first_projection_responsible_node=(
            first_projection.responsible_node_index
            if first_projection is not None
            else None
        ),
        pyz1_first_projection_responsible_fraction=(
            first_projection.responsible_fraction
            if first_projection is not None
            else None
        ),
        oracle_core_node_count=(
            oracle_diagnostics.core_node_count
            if oracle_diagnostics is not None
            else None
        ),
        oracle_final_node_count=(
            oracle_diagnostics.final_node_count
            if oracle_diagnostics is not None
            else None
        ),
        oracle_core_crossings=(
            oracle_diagnostics.core_crossings
            if oracle_diagnostics is not None
            else None
        ),
        oracle_core_ghost_nodes=(
            oracle_diagnostics.core_ghost_nodes
            if oracle_diagnostics is not None
            else None
        ),
        note=_note_for_status(status),
    )


def _first_core_trace_node(
    blocked_nodes: tuple[tuple[CoreTraceNode, ...], ...],
) -> CoreTraceNode | None:
    for chain_nodes in blocked_nodes:
        if len(chain_nodes) > 0:
            return chain_nodes[0]
    return None


def _first_projection_trace(
    traces: tuple[ProjectionTrace, ...],
) -> ProjectionTrace | None:
    if len(traces) == 0:
        return None
    return traces[0]


def _oracle_reducer_diagnostics(path: Path) -> Z1ReducerScanDiagnostics | None:
    if not path.exists():
        return None
    return reducer_scan_diagnostics(read_z1_log_file(path))


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


def _shortest_path_geometry_comparison(
    actual: ShortestPathSnapshot,
    expected_text: str,
) -> ShortestPathGeometryComparison:
    expected = parse_shortest_path_text(expected_text)
    node_count_mismatches = abs(actual.chain_count - expected.chain_count)
    max_position_delta = 0.0
    shared_chain_count = min(actual.chain_count, expected.chain_count)
    for chain_index in range(shared_chain_count):
        actual_chain = actual.chains[chain_index]
        expected_chain = expected.chains[chain_index]
        node_count_mismatches += abs(
            actual_chain.node_count - expected_chain.node_count,
        )
        shared_node_count = min(actual_chain.node_count, expected_chain.node_count)
        for node_index in range(shared_node_count):
            delta = _node_position_delta(
                actual_chain.nodes[node_index].position,
                expected_chain.nodes[node_index].position,
            )
            max_position_delta = max(max_position_delta, delta)
    return ShortestPathGeometryComparison(
        node_count_mismatches=node_count_mismatches,
        max_node_position_delta=max_position_delta,
    )


def _node_position_delta(
    actual: Vector3,
    expected: Vector3,
) -> float:
    return sqrt(
        (actual.x - expected.x) ** 2
        + (actual.y - expected.y) ** 2
        + (actual.z - expected.z) ** 2,
    )


def _summary_field_mismatches(
    actual_text: str,
    expected_text: str,
) -> tuple[SummaryFieldMismatch, ...]:
    actual_fields = actual_text.split()
    expected_fields = expected_text.split()
    shared_count = min(len(actual_fields), len(expected_fields))
    mismatches = tuple(
        SummaryFieldMismatch(
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
        SummaryFieldMismatch(
            field_name="field_count",
            actual=str(len(actual_fields)),
            expected=str(len(expected_fields)),
        ),
    )


def _summary_field_name(index: int) -> str:
    if index < len(SUMMARY_FIELD_NAMES):
        return SUMMARY_FIELD_NAMES[index]
    return f"field_{index + 1}"


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
        (
            "| benchmark | mode | status | Lpp delta | Z delta | "
            "summary field mismatches | pair mismatches | "
            "node count mismatches | max node position delta | "
            "pyz1 core nodes | pyz1 final nodes | "
            "pyz1 core trace nodes | pyz1 core trace ghosts | "
            "pyz1 core accepted blocked moves | "
            "pyz1 core transient blocked nodes | "
            "pyz1 first trace blocker chain | "
            "pyz1 first trace blocker node | "
            "pyz1 first trace shortcut fraction | "
            "pyz1 first trace blocker fraction | "
            "pyz1 first trace blocker distance | "
            "pyz1 projection traces | pyz1 first projection chain | "
            "pyz1 first projection node | pyz1 first projection fraction | "
            "oracle core nodes | oracle final nodes | "
            "oracle core crossings | oracle core ghosts | "
            "summary mismatch details | note |"
        ),
        (
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | "
            "---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | "
            "---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | "
            "---: | ---: | --- | --- |"
        ),
    ]
    lines.extend(_format_record(record) for record in records)
    return "\n".join(lines) + "\n"


def _format_record(record: RegressionRecord) -> str:
    return (
        f"| benchmark-{record.benchmark_id} | {record.mode.value} | "
        f"{record.status.value} | {_format_optional_float(record.lpp_delta)} | "
        f"{_format_optional_float(record.z_delta)} | "
        f"{_format_optional_int(record.summary_field_mismatches)} | "
        f"{_format_optional_int(record.pairing_mismatches)} | "
        f"{_format_optional_int(record.node_count_mismatches)} | "
        f"{_format_optional_float(record.max_node_position_delta)} | "
        f"{_format_optional_int(record.pyz1_core_node_count)} | "
        f"{_format_optional_int(record.pyz1_final_node_count)} | "
        f"{_format_optional_int(record.pyz1_core_trace_node_count)} | "
        f"{_format_optional_int(record.pyz1_core_trace_ghost_nodes)} | "
        f"{_format_optional_int(record.pyz1_core_accepted_blocked_moves)} | "
        f"{_format_optional_int(record.pyz1_core_transient_blocked_nodes)} | "
        f"{_format_optional_int(record.pyz1_first_trace_blocker_chain)} | "
        f"{_format_optional_int(record.pyz1_first_trace_blocker_node)} | "
        f"{_format_first_trace_shortcut_fraction(record)} | "
        f"{_format_first_trace_blocker_fraction(record)} | "
        f"{_format_first_trace_blocker_distance(record)} | "
        f"{_format_optional_int(record.pyz1_projection_trace_count)} | "
        f"{_format_optional_int(record.pyz1_first_projection_responsible_chain)} | "
        f"{_format_optional_int(record.pyz1_first_projection_responsible_node)} | "
        f"{_format_first_projection_fraction(record)} | "
        f"{_format_optional_int(record.oracle_core_node_count)} | "
        f"{_format_optional_int(record.oracle_final_node_count)} | "
        f"{_format_optional_int(record.oracle_core_crossings)} | "
        f"{_format_optional_int(record.oracle_core_ghost_nodes)} | "
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


def _format_first_projection_fraction(record: RegressionRecord) -> str:
    return _format_optional_float(
        record.pyz1_first_projection_responsible_fraction,
    )


def _format_first_trace_shortcut_fraction(record: RegressionRecord) -> str:
    return _format_optional_float(record.pyz1_first_trace_shortcut_fraction)


def _format_first_trace_blocker_fraction(record: RegressionRecord) -> str:
    return _format_optional_float(record.pyz1_first_trace_blocker_fraction)


def _format_first_trace_blocker_distance(record: RegressionRecord) -> str:
    return _format_optional_float(record.pyz1_first_trace_blocker_distance)


def _format_summary_field_details(
    details: tuple[SummaryFieldMismatch, ...] | None,
) -> str:
    if details is None:
        return "n/a"
    if len(details) == 0:
        return "none"
    return "; ".join(
        f"{detail.field_name}: {detail.actual} != {detail.expected}"
        for detail in details
    )
