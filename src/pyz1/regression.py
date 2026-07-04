from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isclose, sqrt
from typing import TYPE_CHECKING, Final

from pyz1.geometry import (
    GeometryBox,
    Segment,
    closest_segment_points,
    minimum_image_delta,
)
from pyz1.output_io import (
    format_shortest_path_text,
    format_summary_text,
    parse_shortest_path_text,
    read_summary_file,
)
from pyz1.output_models import (
    ShortestPathChain,
    ShortestPathNode,
    ShortestPathSnapshot,
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
    from pyz1.output_models import ShortestPathPair
    from pyz1.reducer import CoreStageNode, CoreTraceNode, ProjectionTrace

LPP_TOLERANCE: Final = 1.0e-6
Z_TOLERANCE: Final = 1.0e-6
SOURCE_BEAD_TOLERANCE: Final = 1.0e-9
CORE_STAGE_NODE_FILENAME: Final = "Z1+NODES-best-match-step1-entry.dat"
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
    max_node_delta_chain_index: int | None
    max_node_delta_node_index: int | None
    max_node_delta_actual_source_bead: float | None
    max_node_delta_expected_source_bead: float | None
    max_node_actual_pair_fraction: float | None
    max_node_actual_pair_distance: float | None
    max_node_expected_pair_fraction: float | None
    max_node_expected_pair_distance: float | None
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
    oracle_core_stage_node_count: int | None
    pyz1_core_stage_node_count_mismatches: int | None
    pyz1_core_stage_max_node_position_delta: float | None
    pyz1_core_stage_source_bead_matches: int | None
    pyz1_core_stage_source_bead_max_delta: float | None
    note: str


@dataclass(frozen=True, slots=True)
class ShortestPathGeometryComparison:
    node_count_mismatches: int
    max_node_position_delta: float
    max_node_delta_chain_index: int | None
    max_node_delta_node_index: int | None
    max_node_delta_actual_source_bead: float | None
    max_node_delta_expected_source_bead: float | None
    max_node_actual_pair_fraction: float | None
    max_node_actual_pair_distance: float | None
    max_node_expected_pair_fraction: float | None
    max_node_expected_pair_distance: float | None


@dataclass(frozen=True, slots=True)
class _NodePairGeometry:
    fraction: float
    distance: float


@dataclass(frozen=True, slots=True)
class CoreStageGeometryComparison:
    node_count_mismatches: int
    max_node_position_delta: float
    source_bead_matches: int
    source_bead_max_node_position_delta: float


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
            max_node_delta_chain_index=None,
            max_node_delta_node_index=None,
            max_node_delta_actual_source_bead=None,
            max_node_delta_expected_source_bead=None,
            max_node_actual_pair_fraction=None,
            max_node_actual_pair_distance=None,
            max_node_expected_pair_fraction=None,
            max_node_expected_pair_distance=None,
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
            oracle_core_stage_node_count=None,
            pyz1_core_stage_node_count_mismatches=None,
            pyz1_core_stage_max_node_position_delta=None,
            pyz1_core_stage_source_bead_matches=None,
            pyz1_core_stage_source_bead_max_delta=None,
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
            max_node_delta_chain_index=None,
            max_node_delta_node_index=None,
            max_node_delta_actual_source_bead=None,
            max_node_delta_expected_source_bead=None,
            max_node_actual_pair_fraction=None,
            max_node_actual_pair_distance=None,
            max_node_expected_pair_fraction=None,
            max_node_expected_pair_distance=None,
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
            oracle_core_stage_node_count=None,
            pyz1_core_stage_node_count_mismatches=None,
            pyz1_core_stage_max_node_position_delta=None,
            pyz1_core_stage_source_bead_matches=None,
            pyz1_core_stage_source_bead_max_delta=None,
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
    oracle_core_stage = _oracle_core_stage(oracle_dir / CORE_STAGE_NODE_FILENAME)
    pyz1_core_stage_comparison = _pyz1_core_stage_comparison(
        result.diagnostics.core_stage_nodes,
        result.shortest_path.box,
        oracle_core_stage,
    )
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
        max_node_delta_chain_index=geometry_comparison.max_node_delta_chain_index,
        max_node_delta_node_index=geometry_comparison.max_node_delta_node_index,
        max_node_delta_actual_source_bead=(
            geometry_comparison.max_node_delta_actual_source_bead
        ),
        max_node_delta_expected_source_bead=(
            geometry_comparison.max_node_delta_expected_source_bead
        ),
        max_node_actual_pair_fraction=geometry_comparison.max_node_actual_pair_fraction,
        max_node_actual_pair_distance=geometry_comparison.max_node_actual_pair_distance,
        max_node_expected_pair_fraction=(
            geometry_comparison.max_node_expected_pair_fraction
        ),
        max_node_expected_pair_distance=(
            geometry_comparison.max_node_expected_pair_distance
        ),
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
        oracle_core_stage_node_count=(
            _snapshot_node_count(oracle_core_stage)
            if oracle_core_stage is not None
            else None
        ),
        pyz1_core_stage_node_count_mismatches=(
            pyz1_core_stage_comparison.node_count_mismatches
            if pyz1_core_stage_comparison is not None
            else None
        ),
        pyz1_core_stage_max_node_position_delta=(
            pyz1_core_stage_comparison.max_node_position_delta
            if pyz1_core_stage_comparison is not None
            else None
        ),
        pyz1_core_stage_source_bead_matches=(
            pyz1_core_stage_comparison.source_bead_matches
            if pyz1_core_stage_comparison is not None
            else None
        ),
        pyz1_core_stage_source_bead_max_delta=(
            pyz1_core_stage_comparison.source_bead_max_node_position_delta
            if pyz1_core_stage_comparison is not None
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


def _oracle_core_stage(path: Path) -> ShortestPathSnapshot | None:
    if not path.exists():
        return None
    return parse_shortest_path_text(path.read_text(encoding="utf-8"))


def _pyz1_core_stage_comparison(
    core_stage_nodes: tuple[tuple[CoreStageNode, ...], ...],
    box: Vector3,
    oracle_core_stage: ShortestPathSnapshot | None,
) -> CoreStageGeometryComparison | None:
    if oracle_core_stage is None:
        return None
    actual_core_stage = _pyz1_core_stage_snapshot(core_stage_nodes, box)
    index_comparison = _shortest_path_snapshot_geometry_comparison(
        actual_core_stage,
        oracle_core_stage,
    )
    source_bead_comparison = _source_bead_matched_geometry_comparison(
        actual_core_stage,
        oracle_core_stage,
    )
    return CoreStageGeometryComparison(
        node_count_mismatches=index_comparison.node_count_mismatches,
        max_node_position_delta=index_comparison.max_node_position_delta,
        source_bead_matches=source_bead_comparison.source_bead_matches,
        source_bead_max_node_position_delta=(
            source_bead_comparison.source_bead_max_node_position_delta
        ),
    )


@dataclass(frozen=True, slots=True)
class _SourceBeadGeometryComparison:
    source_bead_matches: int
    source_bead_max_node_position_delta: float


def _source_bead_matched_geometry_comparison(
    actual: ShortestPathSnapshot,
    expected: ShortestPathSnapshot,
) -> _SourceBeadGeometryComparison:
    matched_count = 0
    max_position_delta = 0.0
    box = GeometryBox(lengths=actual.box)
    shared_chain_count = min(actual.chain_count, expected.chain_count)
    for chain_index in range(shared_chain_count):
        for actual_node in actual.chains[chain_index].nodes:
            expected_node = _find_source_bead_match(
                actual_node,
                expected.chains[chain_index],
            )
            if expected_node is None:
                continue
            matched_count += 1
            delta = _periodic_node_position_delta(
                actual_node.position,
                expected_node.position,
                box,
            )
            max_position_delta = max(max_position_delta, delta)
    return _SourceBeadGeometryComparison(
        source_bead_matches=matched_count,
        source_bead_max_node_position_delta=max_position_delta,
    )


def _find_source_bead_match(
    actual_node: ShortestPathNode,
    expected_chain: ShortestPathChain,
) -> ShortestPathNode | None:
    return next(
        (
            expected_node
            for expected_node in expected_chain.nodes
            if _source_beads_match(
                actual_node.source_bead,
                expected_node.source_bead,
            )
        ),
        None,
    )


def _source_beads_match(actual: float, expected: float) -> bool:
    return abs(actual - expected) <= SOURCE_BEAD_TOLERANCE


def _periodic_node_position_delta(
    actual: Vector3,
    expected: Vector3,
    box: GeometryBox,
) -> float:
    delta = minimum_image_delta(Segment(start=expected, end=actual), box)
    return sqrt(
        delta.x * delta.x
        + delta.y * delta.y
        + delta.z * delta.z,
    )


def _pyz1_core_stage_snapshot(
    core_stage_nodes: tuple[tuple[CoreStageNode, ...], ...],
    box: Vector3,
) -> ShortestPathSnapshot:
    chains = tuple(
        _pyz1_core_stage_chain(chain_nodes)
        for chain_nodes in core_stage_nodes
    )
    return ShortestPathSnapshot(chains=chains, box=box)


def _pyz1_core_stage_chain(
    core_stage_nodes: tuple[CoreStageNode, ...],
) -> ShortestPathChain:
    return ShortestPathChain(
        nodes=tuple(
            ShortestPathNode(
                position=node.position,
                source_bead=node.source_bead,
                is_entanglement=False,
                pair=None,
            )
            for node in core_stage_nodes
        ),
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


def _shortest_path_geometry_comparison(
    actual: ShortestPathSnapshot,
    expected_text: str,
) -> ShortestPathGeometryComparison:
    return _shortest_path_snapshot_geometry_comparison(
        actual,
        parse_shortest_path_text(expected_text),
    )


def _shortest_path_snapshot_geometry_comparison(
    actual: ShortestPathSnapshot,
    expected: ShortestPathSnapshot,
) -> ShortestPathGeometryComparison:
    node_count_mismatches = abs(actual.chain_count - expected.chain_count)
    max_position_delta = 0.0
    max_delta_chain_index: int | None = None
    max_delta_node_index: int | None = None
    max_delta_actual_source_bead: float | None = None
    max_delta_expected_source_bead: float | None = None
    max_actual_pair_geometry: _NodePairGeometry | None = None
    max_expected_pair_geometry: _NodePairGeometry | None = None
    box = GeometryBox(lengths=actual.box)
    shared_chain_count = min(actual.chain_count, expected.chain_count)
    for chain_index in range(shared_chain_count):
        actual_chain = actual.chains[chain_index]
        expected_chain = expected.chains[chain_index]
        node_count_mismatches += abs(
            actual_chain.node_count - expected_chain.node_count,
        )
        shared_node_count = min(actual_chain.node_count, expected_chain.node_count)
        for node_index in range(shared_node_count):
            actual_node = actual_chain.nodes[node_index]
            expected_node = expected_chain.nodes[node_index]
            delta = _periodic_node_position_delta(
                actual_node.position,
                expected_node.position,
                box,
            )
            if max_delta_chain_index is None or delta > max_position_delta:
                max_position_delta = delta
                max_delta_chain_index = chain_index + 1
                max_delta_node_index = node_index + 1
                max_delta_actual_source_bead = actual_node.source_bead
                max_delta_expected_source_bead = expected_node.source_bead
                max_actual_pair_geometry = _node_pair_geometry(actual_node, actual)
                max_expected_pair_geometry = _node_pair_geometry(
                    expected_node,
                    expected,
                )
    return ShortestPathGeometryComparison(
        node_count_mismatches=node_count_mismatches,
        max_node_position_delta=max_position_delta,
        max_node_delta_chain_index=max_delta_chain_index,
        max_node_delta_node_index=max_delta_node_index,
        max_node_delta_actual_source_bead=max_delta_actual_source_bead,
        max_node_delta_expected_source_bead=max_delta_expected_source_bead,
        max_node_actual_pair_fraction=(
            max_actual_pair_geometry.fraction
            if max_actual_pair_geometry is not None
            else None
        ),
        max_node_actual_pair_distance=(
            max_actual_pair_geometry.distance
            if max_actual_pair_geometry is not None
            else None
        ),
        max_node_expected_pair_fraction=(
            max_expected_pair_geometry.fraction
            if max_expected_pair_geometry is not None
            else None
        ),
        max_node_expected_pair_distance=(
            max_expected_pair_geometry.distance
            if max_expected_pair_geometry is not None
            else None
        ),
    )


def _node_pair_geometry(
    node: ShortestPathNode,
    snapshot: ShortestPathSnapshot,
) -> _NodePairGeometry | None:
    if node.pair is None:
        return None
    pair_chain_index = node.pair.chain_index - 1
    if pair_chain_index < 0 or pair_chain_index >= snapshot.chain_count:
        return None
    pair_chain = snapshot.chains[pair_chain_index]
    pair_node_index = node.pair.node_index
    if pair_node_index < 1 or pair_node_index >= pair_chain.node_count:
        return None
    pair_segment = Segment(
        start=pair_chain.nodes[pair_node_index - 1].position,
        end=pair_chain.nodes[pair_node_index].position,
    )
    closest = closest_segment_points(
        Segment(start=node.position, end=node.position),
        pair_segment,
    )
    return _NodePairGeometry(
        fraction=closest.second_fraction,
        distance=closest.distance,
    )


def _snapshot_node_count(snapshot: ShortestPathSnapshot) -> int:
    return sum(chain.node_count for chain in snapshot.chains)


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
            "max node delta chain | max node delta node | "
            "max node delta actual source | "
            "max node delta expected source | "
            "max node actual pair fraction | "
            "max node actual pair distance | "
            "max node expected pair fraction | "
            "max node expected pair distance | "
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
            "oracle core stage nodes | "
            "pyz1 core stage node count mismatches | "
            "pyz1 core stage max node position delta | "
            "pyz1 core stage source bead matches | "
            "pyz1 core stage source bead max delta | "
            "summary mismatch details | note |"
        ),
        (
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | "
            "---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | "
            "---: | ---: | ---: | ---: | "
            "---: | ---: | ---: | ---: | "
            "---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | "
            "---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |"
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
        f"{_format_optional_int(record.max_node_delta_chain_index)} | "
        f"{_format_optional_int(record.max_node_delta_node_index)} | "
        f"{_format_optional_float(record.max_node_delta_actual_source_bead)} | "
        f"{_format_optional_float(record.max_node_delta_expected_source_bead)} | "
        f"{_format_optional_float(record.max_node_actual_pair_fraction)} | "
        f"{_format_optional_float(record.max_node_actual_pair_distance)} | "
        f"{_format_optional_float(record.max_node_expected_pair_fraction)} | "
        f"{_format_optional_float(record.max_node_expected_pair_distance)} | "
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
        f"{_format_optional_int(record.oracle_core_stage_node_count)} | "
        f"{_format_optional_int(record.pyz1_core_stage_node_count_mismatches)} | "
        f"{_format_optional_float(record.pyz1_core_stage_max_node_position_delta)} | "
        f"{_format_optional_int(record.pyz1_core_stage_source_bead_matches)} | "
        f"{_format_optional_float(record.pyz1_core_stage_source_bead_max_delta)} | "
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
