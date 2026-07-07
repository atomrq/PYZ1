from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from itertools import zip_longest
from math import sqrt
from typing import TYPE_CHECKING, Final

from pyz1.geometry import (
    GeometryBox,
    Segment,
    closest_segment_points,
    minimum_image_delta,
    unfold_chain,
)
from pyz1.models import Chain, Snapshot, Vector3
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
from pyz1.reducer import (
    ReducerSettings,
    blocked_trace_obstacle_contacts,
    convex_selected_winding_obstacle_chain_indices,
    convex_winding_obstacle_candidate_chain_indices,
    convex_winding_obstacle_candidate_sources,
    reduce_snapshot,
    winding_obstacle_candidate_chain_indices,
)
from pyz1.z1_io import read_z1_file
from pyz1.z1_log import (
    Z1ReducerScanDiagnostics,
    read_z1_log_file,
    reducer_scan_diagnostics,
)

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from pyz1.output_models import ShortestPathPair
    from pyz1.reducer import CoreStageNode, CoreTraceNode, ProjectionTrace

SOURCE_BEAD_TOLERANCE: Final = 1.0e-9
SHORTEST_PATH_POSITION_TOLERANCE: Final = 1.0e-3
STATISTICAL_LPP_DELTA_TOLERANCE: Final = 1.0e-2
STATISTICAL_Z_DELTA_TOLERANCE: Final = 1.0e-9
MAX_TRUE_CHAIN_CONTACT_CANDIDATE_DISTANCE: Final = 0.3
CORE_STAGE_NODE_FILENAME: Final = "Z1+NODES-best-match-step1-entry.dat"
MAX_SOURCE_RESIDUAL_REPORT_DETAILS: Final = 12
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
    SELFZ = "selfz"


class RegressionStatus(StrEnum):
    PASSED = "passed"
    MISMATCH = "mismatch"
    KNOWN_INVALID = "known-invalid"


class StatisticalRegressionStatus(StrEnum):
    PASSED = "passed"
    MISMATCH = "mismatch"
    NOT_APPLICABLE = "n/a"


@dataclass(frozen=True, slots=True)
class RegressionSettingsOverride:
    mode: RegressionMode
    settings: ReducerSettings


@dataclass(frozen=True, slots=True)
class RegressionRequest:
    source_dir: Path
    oracle_root: Path
    report_path: Path
    modes: tuple[RegressionMode, ...]
    benchmark_ids: tuple[str, ...]
    max_node_count: int = 1000
    trace_diagnostics_max_node_count: int = 1000
    settings_overrides: tuple[RegressionSettingsOverride, ...] = ()


@dataclass(frozen=True, slots=True)
class PairingComparison:
    mismatched_pair_count: int


@dataclass(frozen=True, slots=True)
class SummaryFieldMismatch:
    field_name: str
    actual: str
    expected: str


@dataclass(frozen=True, slots=True)
class ChainContourResidual:
    chain_index: int
    actual: float | None
    expected: float | None
    delta: float | None


@dataclass(frozen=True, slots=True)
class SourceBeadResidual:
    chain_index: int
    node_index: int
    actual: float
    expected: float
    delta: float
    actual_pair_chain_index: int | None
    expected_pair_chain_index: int | None


@dataclass(frozen=True, slots=True)
class SourceSequenceResidual:
    source_index: int
    actual: float | None
    expected: float | None
    delta: float | None


@dataclass(frozen=True, slots=True)
class OracleObstacleSourceResidual:
    chain_index: int
    actual: float
    expected: float
    delta: float


@dataclass(frozen=True, slots=True)
class OracleObstacleSourceSegmentAmbiguity:
    chain_index: int
    expected_source: float
    nearest_source: float
    nearest_distance: float
    expected_rank: int
    expected_rank_source: float
    expected_rank_distance: float


@dataclass(frozen=True, slots=True)
class TrueChainContactCandidate:
    chain_index: int
    source_bead: float
    other_source_bead: float
    distance: float


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
    pyz1_obstacle_pair_sequence: tuple[int, ...] | None = None
    oracle_obstacle_pair_sequence: tuple[int, ...] | None = None
    max_node_source_bead_delta: float | None = None
    max_source_delta_chain_index: int | None = None
    max_source_delta_node_index: int | None = None
    source_bead_residuals: tuple[SourceBeadResidual, ...] | None = None
    pyz1_winding_candidate_count: int | None = None
    pyz1_winding_missing_oracle_sequence: tuple[int, ...] | None = None
    pyz1_winding_extra_candidate_count: int | None = None
    pyz1_convex_winding_candidate_count: int | None = None
    pyz1_convex_winding_missing_oracle_sequence: tuple[int, ...] | None = None
    pyz1_convex_winding_extra_candidate_count: int | None = None
    pyz1_convex_selected_winding_sequence: tuple[int, ...] | None = None
    pyz1_convex_selected_missing_oracle_sequence: tuple[int, ...] | None = None
    pyz1_convex_selected_extra_count: int | None = None
    pyz1_blocked_trace_obstacle_sequence: tuple[int, ...] | None = None
    pyz1_retained_blocked_trace_obstacle_sequence: tuple[int, ...] | None = None
    max_oracle_obstacle_source_delta: float | None = None
    max_oracle_obstacle_source_delta_chain: int | None = None
    oracle_obstacle_source_residuals: (
        tuple[OracleObstacleSourceResidual, ...] | None
    ) = None
    max_oracle_obstacle_source_segment_rank: int | None = None
    oracle_obstacle_source_segment_ambiguities: (
        tuple[OracleObstacleSourceSegmentAmbiguity, ...] | None
    ) = None
    oracle_default_source_sequence: tuple[float, ...] | None = None
    oracle_mode_source_sequence_matches_default: bool | None = None
    pyz1_source_sequence: tuple[float, ...] | None = None
    pyz1_source_sequence_mismatch_count: int | None = None
    pyz1_source_sequence_max_delta: float | None = None
    pyz1_source_sequence_residuals: tuple[SourceSequenceResidual, ...] | None = None
    pyz1_true_chain_pair_sequence: tuple[int, ...] | None = None
    pyz1_true_chain_contact_candidate_sequence: tuple[int, ...] | None = None
    pyz1_true_chain_contact_candidate_details: (
        tuple[TrueChainContactCandidate, ...] | None
    ) = None
    oracle_source_nearest_true_chain_contact_sequence: tuple[int, ...] | None = None
    oracle_true_chain_pair_sequence: tuple[int, ...] | None = None
    pyz1_true_chain_pair_node_sequence: tuple[int, ...] | None = None
    oracle_true_chain_pair_node_sequence: tuple[int, ...] | None = None
    max_chain_contour_delta: float | None = None
    max_chain_contour_delta_chain: int | None = None
    chain_contour_residuals: tuple[ChainContourResidual, ...] | None = None
    mean_chain_contour_delta: float | None = None
    root_mean_square_chain_contour_delta: float | None = None
    chain_contour_residual_count: int | None = None
    chain_contour_residual_fraction: float | None = None

    @property
    def statistical_status(self) -> StatisticalRegressionStatus:
        match self.status:
            case RegressionStatus.KNOWN_INVALID:
                return StatisticalRegressionStatus.NOT_APPLICABLE
            case RegressionStatus.PASSED | RegressionStatus.MISMATCH:
                pass
        if (
            self.lpp_delta is None
            or self.z_delta is None
            or self.node_count_mismatches is None
        ):
            return StatisticalRegressionStatus.NOT_APPLICABLE
        if (
            self.lpp_delta <= STATISTICAL_LPP_DELTA_TOLERANCE
            and self.z_delta <= STATISTICAL_Z_DELTA_TOLERANCE
            and self.node_count_mismatches == 0
            and _optional_zero(self.pairing_mismatches)
            and _optional_zero(self.pyz1_source_sequence_mismatch_count)
        ):
            return StatisticalRegressionStatus.PASSED
        return StatisticalRegressionStatus.MISMATCH


@dataclass(frozen=True, slots=True)
class ShortestPathGeometryComparison:
    node_count_mismatches: int
    max_node_position_delta: float
    max_node_delta_chain_index: int | None
    max_node_delta_node_index: int | None
    max_node_delta_actual_source_bead: float | None
    max_node_delta_expected_source_bead: float | None
    max_node_source_bead_delta: float
    max_source_delta_chain_index: int | None
    max_source_delta_node_index: int | None
    source_bead_residuals: tuple[SourceBeadResidual, ...]
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


@dataclass(frozen=True, slots=True)
class _WindingCandidateCoverage:
    candidate_count: int
    missing_oracle_sequence: tuple[int, ...]
    extra_candidate_count: int
    convex_candidate_count: int
    convex_missing_oracle_sequence: tuple[int, ...]
    convex_extra_candidate_count: int
    convex_selected_sequence: tuple[int, ...]
    convex_selected_missing_oracle_sequence: tuple[int, ...]
    convex_selected_extra_count: int
    blocked_trace_obstacle_sequence: tuple[int, ...]
    retained_blocked_trace_obstacle_sequence: tuple[int, ...]
    max_oracle_obstacle_source_delta: float
    max_oracle_obstacle_source_delta_chain: int | None
    oracle_obstacle_source_residuals: tuple[OracleObstacleSourceResidual, ...]
    max_oracle_obstacle_source_segment_rank: int
    oracle_obstacle_source_segment_ambiguities: (
        tuple[OracleObstacleSourceSegmentAmbiguity, ...]
    )
    oracle_true_chain_pair_sequence: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class _SourceSegmentCandidate:
    rank: int
    source_bead: float
    distance: float


@dataclass(frozen=True, slots=True)
class _RegressionStatusInput:
    summary_field_mismatches: int
    pairing_mismatches: int | None
    node_count_mismatches: int
    max_node_position_delta: float


@dataclass(frozen=True, slots=True)
class _ChainContourStatistics:
    mean_absolute_delta: float
    root_mean_square_delta: float


def _optional_zero(value: int | None) -> bool:
    return value is None or value == 0


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
    result = reduce_snapshot(
        snapshot,
        _settings_for_mode(
            mode,
            request.settings_overrides,
            trace_diagnostics_enabled=(
                snapshot.node_count <= request.trace_diagnostics_max_node_count
            ),
        ),
    )
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
    oracle_shortest_path = parse_shortest_path_text(sp_path.read_text(encoding="utf-8"))
    chain_contour_residuals = _chain_contour_residuals(
        result.shortest_path,
        oracle_shortest_path,
    )
    chain_contour_statistics = _chain_contour_statistics(
        result.shortest_path,
        oracle_shortest_path,
    )
    chain_contour_residual_count = len(chain_contour_residuals)
    chain_contour_compared_chain_count = max(
        result.shortest_path.chain_count,
        oracle_shortest_path.chain_count,
    )
    oracle_default_source_sequence = _oracle_default_source_sequence(
        request,
        benchmark_id,
    )
    oracle_mode_source_sequence = _entanglement_source_sequence(oracle_shortest_path)
    pyz1_source_sequence = _entanglement_source_sequence(result.shortest_path)
    geometry_comparison = _shortest_path_snapshot_geometry_comparison(
        result.shortest_path,
        oracle_shortest_path,
    )
    winding_candidate_coverage = _winding_candidate_coverage(
        snapshot,
        oracle_shortest_path,
    )
    oracle_diagnostics = _oracle_reducer_diagnostics(oracle_dir)
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
    true_chain_contact_candidates = _true_chain_contact_candidates(snapshot)
    status = _status_from_output_comparison(
        _RegressionStatusInput(
            summary_field_mismatches=summary_field_mismatches,
            pairing_mismatches=pairing_mismatches,
            node_count_mismatches=geometry_comparison.node_count_mismatches,
            max_node_position_delta=geometry_comparison.max_node_position_delta,
        ),
    )
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
        pyz1_obstacle_pair_sequence=_obstacle_pair_chain_sequence(
            result.shortest_path,
        ),
        oracle_obstacle_pair_sequence=_obstacle_pair_chain_sequence(
            oracle_shortest_path,
        ),
        max_node_source_bead_delta=geometry_comparison.max_node_source_bead_delta,
        max_source_delta_chain_index=(
            geometry_comparison.max_source_delta_chain_index
        ),
        max_source_delta_node_index=geometry_comparison.max_source_delta_node_index,
        source_bead_residuals=geometry_comparison.source_bead_residuals,
        pyz1_winding_candidate_count=winding_candidate_coverage.candidate_count,
        pyz1_winding_missing_oracle_sequence=(
            winding_candidate_coverage.missing_oracle_sequence
        ),
        pyz1_winding_extra_candidate_count=(
            winding_candidate_coverage.extra_candidate_count
        ),
        pyz1_convex_winding_candidate_count=(
            winding_candidate_coverage.convex_candidate_count
        ),
        pyz1_convex_winding_missing_oracle_sequence=(
            winding_candidate_coverage.convex_missing_oracle_sequence
        ),
        pyz1_convex_winding_extra_candidate_count=(
            winding_candidate_coverage.convex_extra_candidate_count
        ),
        pyz1_convex_selected_winding_sequence=(
            winding_candidate_coverage.convex_selected_sequence
        ),
        pyz1_convex_selected_missing_oracle_sequence=(
            winding_candidate_coverage.convex_selected_missing_oracle_sequence
        ),
        pyz1_convex_selected_extra_count=(
            winding_candidate_coverage.convex_selected_extra_count
        ),
        pyz1_blocked_trace_obstacle_sequence=(
            winding_candidate_coverage.blocked_trace_obstacle_sequence
        ),
        pyz1_retained_blocked_trace_obstacle_sequence=(
            winding_candidate_coverage.retained_blocked_trace_obstacle_sequence
        ),
        max_oracle_obstacle_source_delta=(
            winding_candidate_coverage.max_oracle_obstacle_source_delta
        ),
        max_oracle_obstacle_source_delta_chain=(
            winding_candidate_coverage.max_oracle_obstacle_source_delta_chain
        ),
        oracle_obstacle_source_residuals=(
            winding_candidate_coverage.oracle_obstacle_source_residuals
        ),
        max_oracle_obstacle_source_segment_rank=(
            winding_candidate_coverage.max_oracle_obstacle_source_segment_rank
        ),
        oracle_obstacle_source_segment_ambiguities=(
            winding_candidate_coverage.oracle_obstacle_source_segment_ambiguities
        ),
        oracle_default_source_sequence=oracle_default_source_sequence,
        oracle_mode_source_sequence_matches_default=(
            oracle_default_source_sequence == oracle_mode_source_sequence
            if oracle_default_source_sequence is not None
            else None
        ),
        pyz1_source_sequence=pyz1_source_sequence,
        pyz1_source_sequence_mismatch_count=_source_sequence_mismatch_count(
            pyz1_source_sequence,
            oracle_default_source_sequence,
        ),
        pyz1_source_sequence_max_delta=_source_sequence_max_delta(
            pyz1_source_sequence,
            oracle_default_source_sequence,
        ),
        pyz1_source_sequence_residuals=_source_sequence_residuals(
            pyz1_source_sequence,
            oracle_default_source_sequence,
        ),
        pyz1_true_chain_pair_sequence=_true_chain_pair_sequence(
            result.shortest_path,
            snapshot,
        ),
        pyz1_true_chain_contact_candidate_sequence=tuple(
            candidate.chain_index for candidate in true_chain_contact_candidates
        ),
        pyz1_true_chain_contact_candidate_details=true_chain_contact_candidates,
        oracle_source_nearest_true_chain_contact_sequence=(
            _nearest_true_chain_contact_sequence_for_sources(
                true_chain_contact_candidates,
                oracle_default_source_sequence,
            )
        ),
        oracle_true_chain_pair_sequence=(
            winding_candidate_coverage.oracle_true_chain_pair_sequence
        ),
        pyz1_true_chain_pair_node_sequence=_true_chain_pair_node_sequence(
            result.shortest_path,
            snapshot,
        ),
        oracle_true_chain_pair_node_sequence=_true_chain_pair_node_sequence(
            oracle_shortest_path,
            snapshot,
        ),
        max_chain_contour_delta=_max_chain_contour_delta(chain_contour_residuals),
        max_chain_contour_delta_chain=(
            _max_chain_contour_delta_chain(chain_contour_residuals)
        ),
        chain_contour_residuals=chain_contour_residuals,
        mean_chain_contour_delta=chain_contour_statistics.mean_absolute_delta,
        root_mean_square_chain_contour_delta=(
            chain_contour_statistics.root_mean_square_delta
        ),
        chain_contour_residual_count=chain_contour_residual_count,
        chain_contour_residual_fraction=_chain_contour_residual_fraction(
            chain_contour_residual_count,
            chain_contour_compared_chain_count,
        ),
    )


def _first_core_trace_node(
    blocked_nodes: tuple[tuple[CoreTraceNode, ...], ...],
) -> CoreTraceNode | None:
    for chain_nodes in blocked_nodes:
        if len(chain_nodes) > 0:
            return chain_nodes[0]
    return None


def _winding_candidate_coverage(
    snapshot: Snapshot,
    oracle_shortest_path: ShortestPathSnapshot,
) -> _WindingCandidateCoverage:
    box = GeometryBox(lengths=snapshot.box, shear=snapshot.shear or 0.0)
    chains = tuple(unfold_chain(chain, box) for chain in snapshot.chains)
    candidate_sequence = winding_obstacle_candidate_chain_indices(chains, 0)
    convex_candidate_sequence = convex_winding_obstacle_candidate_chain_indices(
        chains,
        0,
    )
    convex_selected_sequence = convex_selected_winding_obstacle_chain_indices(
        chains,
        0,
    )
    blocked_trace_contacts = blocked_trace_obstacle_contacts(chains, 0)
    convex_sources = {
        source.chain_index: source.source_bead
        for source in convex_winding_obstacle_candidate_sources(chains, 0)
    }
    oracle_sequence = _obstacle_pair_chain_sequence(oracle_shortest_path)
    oracle_source_residuals = _oracle_obstacle_source_residuals(
        oracle_shortest_path,
        convex_sources,
    )
    oracle_source_segment_ambiguities = (
        _oracle_obstacle_source_segment_ambiguities(
            chains,
            oracle_shortest_path,
        )
    )
    candidate_set = set(candidate_sequence)
    convex_candidate_set = set(convex_candidate_sequence)
    convex_selected_set = set(convex_selected_sequence)
    oracle_set = set(oracle_sequence)
    return _WindingCandidateCoverage(
        candidate_count=len(candidate_sequence),
        missing_oracle_sequence=tuple(
            chain_index
            for chain_index in oracle_sequence
            if chain_index not in candidate_set
        ),
        extra_candidate_count=sum(
            chain_index not in oracle_set
            for chain_index in candidate_sequence
        ),
        convex_candidate_count=len(convex_candidate_sequence),
        convex_missing_oracle_sequence=tuple(
            chain_index
            for chain_index in oracle_sequence
            if chain_index not in convex_candidate_set
        ),
        convex_extra_candidate_count=sum(
            chain_index not in oracle_set
            for chain_index in convex_candidate_sequence
        ),
        convex_selected_sequence=convex_selected_sequence,
        convex_selected_missing_oracle_sequence=tuple(
            chain_index
            for chain_index in oracle_sequence
            if chain_index not in convex_selected_set
        ),
        convex_selected_extra_count=sum(
            chain_index not in oracle_set
            for chain_index in convex_selected_sequence
        ),
        blocked_trace_obstacle_sequence=tuple(
            contact.chain_index for contact in blocked_trace_contacts
        ),
        retained_blocked_trace_obstacle_sequence=tuple(
            contact.chain_index
            for contact in blocked_trace_contacts
            if contact.retained
        ),
        max_oracle_obstacle_source_delta=_max_oracle_obstacle_source_delta(
            oracle_source_residuals,
        ),
        max_oracle_obstacle_source_delta_chain=(
            _max_oracle_obstacle_source_delta_chain(oracle_source_residuals)
        ),
        oracle_obstacle_source_residuals=oracle_source_residuals,
        max_oracle_obstacle_source_segment_rank=(
            _max_oracle_obstacle_source_segment_rank(
                oracle_source_segment_ambiguities,
            )
        ),
        oracle_obstacle_source_segment_ambiguities=(
            oracle_source_segment_ambiguities
        ),
        oracle_true_chain_pair_sequence=tuple(
            chain_index
            for chain_index in oracle_sequence
            if chains[chain_index - 1].is_true_chain
        ),
    )


def _oracle_obstacle_source_residuals(
    oracle_shortest_path: ShortestPathSnapshot,
    candidate_sources: Mapping[int, float],
) -> tuple[OracleObstacleSourceResidual, ...]:
    if oracle_shortest_path.chain_count == 0:
        return ()
    residuals: list[OracleObstacleSourceResidual] = []
    for node in oracle_shortest_path.chains[0].nodes:
        if node.pair is None:
            continue
        candidate_source = candidate_sources.get(node.pair.chain_index)
        if candidate_source is None:
            continue
        residuals.append(
            OracleObstacleSourceResidual(
                chain_index=node.pair.chain_index,
                actual=candidate_source,
                expected=node.source_bead,
                delta=abs(candidate_source - node.source_bead),
            ),
        )
    return tuple(residuals)


def _max_oracle_obstacle_source_delta(
    residuals: tuple[OracleObstacleSourceResidual, ...],
) -> float:
    if len(residuals) == 0:
        return 0.0
    return max(residual.delta for residual in residuals)


def _max_oracle_obstacle_source_delta_chain(
    residuals: tuple[OracleObstacleSourceResidual, ...],
) -> int | None:
    if len(residuals) == 0:
        return None
    return max(residuals, key=lambda residual: residual.delta).chain_index


def _oracle_obstacle_source_segment_ambiguities(
    chains: tuple[Chain, ...],
    oracle_shortest_path: ShortestPathSnapshot,
) -> tuple[OracleObstacleSourceSegmentAmbiguity, ...]:
    if len(chains) == 0 or oracle_shortest_path.chain_count == 0:
        return ()
    first_chain = chains[0]
    ambiguities: list[OracleObstacleSourceSegmentAmbiguity] = []
    for node in oracle_shortest_path.chains[0].nodes:
        if node.pair is None:
            continue
        obstacle = chains[node.pair.chain_index - 1]
        if obstacle.is_true_chain:
            continue
        midpoint = _midpoint_between(obstacle.nodes[0], obstacle.nodes[1])
        ranked_sources = _rank_source_segments(first_chain, midpoint)
        if len(ranked_sources) == 0:
            continue
        expected_source = min(
            ranked_sources,
            key=lambda candidate: abs(candidate.source_bead - node.source_bead),
        )
        if expected_source.rank == 1:
            continue
        nearest_source = ranked_sources[0]
        ambiguities.append(
            OracleObstacleSourceSegmentAmbiguity(
                chain_index=node.pair.chain_index,
                expected_source=node.source_bead,
                nearest_source=nearest_source.source_bead,
                nearest_distance=nearest_source.distance,
                expected_rank=expected_source.rank,
                expected_rank_source=expected_source.source_bead,
                expected_rank_distance=expected_source.distance,
            ),
        )
    return tuple(ambiguities)


def _rank_source_segments(
    chain: Chain,
    point: Vector3,
) -> tuple[_SourceSegmentCandidate, ...]:
    point_segment = Segment(start=point, end=point)
    unranked: list[tuple[float, float]] = []
    for segment_index, (start, end) in enumerate(
        zip(chain.nodes[:-1], chain.nodes[1:], strict=True),
        start=1,
    ):
        closest = closest_segment_points(
            point_segment,
            Segment(start=start, end=end),
        )
        unranked.append(
            (segment_index + closest.second_fraction, closest.distance),
        )
    return tuple(
        _SourceSegmentCandidate(
            rank=rank,
            source_bead=source_bead,
            distance=distance,
        )
        for rank, (source_bead, distance) in enumerate(
            sorted(unranked, key=lambda item: (item[1], item[0])),
            start=1,
        )
    )


def _midpoint_between(first: Vector3, second: Vector3) -> Vector3:
    return Vector3(
        x=(first.x + second.x) * 0.5,
        y=(first.y + second.y) * 0.5,
        z=(first.z + second.z) * 0.5,
    )


def _max_oracle_obstacle_source_segment_rank(
    ambiguities: tuple[OracleObstacleSourceSegmentAmbiguity, ...],
) -> int:
    if len(ambiguities) == 0:
        return 1
    return max(ambiguity.expected_rank for ambiguity in ambiguities)


def _first_projection_trace(
    traces: tuple[ProjectionTrace, ...],
) -> ProjectionTrace | None:
    if len(traces) == 0:
        return None
    return traces[0]


def _oracle_reducer_diagnostics(oracle_dir: Path) -> Z1ReducerScanDiagnostics | None:
    for filename in ("log-stats.Z1", "run.stdout"):
        path = oracle_dir / filename
        if path.exists():
            return reducer_scan_diagnostics(read_z1_log_file(path))
    return None


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


def _settings_for_mode(
    mode: RegressionMode,
    overrides: tuple[RegressionSettingsOverride, ...],
    *,
    trace_diagnostics_enabled: bool = True,
) -> ReducerSettings:
    for override in overrides:
        if override.mode == mode:
            return replace(
                override.settings,
                trace_diagnostics_enabled=trace_diagnostics_enabled,
            )
    match mode:
        case RegressionMode.DEFAULT | RegressionMode.SELFZ:
            return ReducerSettings(
                trace_diagnostics_enabled=trace_diagnostics_enabled,
            )
        case RegressionMode.SPPLUS:
            return ReducerSettings(
                pairing_enabled=True,
                trace_diagnostics_enabled=trace_diagnostics_enabled,
            )


def _summary_filename(mode: RegressionMode) -> str:
    match mode:
        case RegressionMode.DEFAULT | RegressionMode.SELFZ:
            return "Z1+summary.dat"
        case RegressionMode.SPPLUS:
            return "Z1+summary.dat"


def _pairing_mismatch_count(
    mode: RegressionMode,
    actual: ShortestPathSnapshot,
    expected_path: Path,
) -> int | None:
    match mode:
        case RegressionMode.DEFAULT | RegressionMode.SELFZ:
            return None
        case RegressionMode.SPPLUS:
            comparison = compare_spplus_pairing(
                format_shortest_path_text(actual),
                expected_path.read_text(encoding="utf-8"),
            )
            return comparison.mismatched_pair_count


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
    max_source_bead_delta = 0.0
    max_source_delta_chain_index: int | None = None
    max_source_delta_node_index: int | None = None
    source_bead_residuals: list[SourceBeadResidual] = []
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
            source_bead_delta = abs(
                actual_node.source_bead - expected_node.source_bead,
            )
            if source_bead_delta > SOURCE_BEAD_TOLERANCE:
                source_bead_residuals.append(
                    SourceBeadResidual(
                        chain_index=chain_index + 1,
                        node_index=node_index + 1,
                        actual=actual_node.source_bead,
                        expected=expected_node.source_bead,
                        delta=source_bead_delta,
                        actual_pair_chain_index=(
                            actual_node.pair.chain_index
                            if actual_node.pair is not None
                            else None
                        ),
                        expected_pair_chain_index=(
                            expected_node.pair.chain_index
                            if expected_node.pair is not None
                            else None
                        ),
                    ),
                )
            if (
                max_source_delta_chain_index is None
                or source_bead_delta > max_source_bead_delta
            ):
                max_source_bead_delta = source_bead_delta
                max_source_delta_chain_index = chain_index + 1
                max_source_delta_node_index = node_index + 1
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
        max_node_source_bead_delta=max_source_bead_delta,
        max_source_delta_chain_index=max_source_delta_chain_index,
        max_source_delta_node_index=max_source_delta_node_index,
        source_bead_residuals=tuple(source_bead_residuals),
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


def _status_from_output_comparison(
    status_input: _RegressionStatusInput,
) -> RegressionStatus:
    pairing_clean = (
        status_input.pairing_mismatches is None
        or status_input.pairing_mismatches == 0
    )
    if (
        status_input.summary_field_mismatches == 0
        and pairing_clean
        and status_input.node_count_mismatches == 0
        and status_input.max_node_position_delta <= SHORTEST_PATH_POSITION_TOLERANCE
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


def _obstacle_pair_chain_sequence(snapshot: ShortestPathSnapshot) -> tuple[int, ...]:
    if snapshot.chain_count == 0:
        return ()
    return tuple(
        node.pair.chain_index
        for node in snapshot.chains[0].nodes
        if node.is_entanglement and node.pair is not None
    )


def _true_chain_pair_sequence(
    shortest_path: ShortestPathSnapshot,
    source_snapshot: Snapshot,
) -> tuple[int, ...]:
    if shortest_path.chain_count == 0:
        return ()
    return tuple(
        node.pair.chain_index
        for node in shortest_path.chains[0].nodes
        if node.is_entanglement
        and node.pair is not None
        and _has_true_chain_pair(source_snapshot, node.pair.chain_index)
    )


def _true_chain_pair_node_sequence(
    shortest_path: ShortestPathSnapshot,
    source_snapshot: Snapshot,
) -> tuple[int, ...]:
    if shortest_path.chain_count == 0:
        return ()
    return tuple(
        node.pair.node_index
        for node in shortest_path.chains[0].nodes
        if node.is_entanglement
        and node.pair is not None
        and _has_true_chain_pair(source_snapshot, node.pair.chain_index)
    )


def _has_true_chain_pair(snapshot: Snapshot, chain_index: int) -> bool:
    zero_based_index = chain_index - 1
    return (
        0 <= zero_based_index < snapshot.chain_count
        and snapshot.chains[zero_based_index].is_true_chain
    )


def _true_chain_contact_candidates(
    snapshot: Snapshot,
) -> tuple[TrueChainContactCandidate, ...]:
    if snapshot.chain_count <= 1:
        return ()
    box = GeometryBox(lengths=snapshot.box, shear=snapshot.shear or 0.0)
    chains = tuple(unfold_chain(chain, box) for chain in snapshot.chains)
    first_chain = chains[0]
    if not first_chain.is_true_chain:
        return ()
    candidates = tuple(
        candidate
        for chain_index, chain in enumerate(chains[1:], start=2)
        if chain.is_true_chain
        for candidate in (_nearest_true_chain_contact(first_chain, chain, chain_index),)
        if candidate is not None
        and candidate.distance <= MAX_TRUE_CHAIN_CONTACT_CANDIDATE_DISTANCE
    )
    return tuple(
        sorted(
            candidates,
            key=lambda candidate: (
                candidate.source_bead,
                candidate.distance,
                candidate.chain_index,
            ),
        ),
    )


def _nearest_true_chain_contact(
    first_chain: Chain,
    other_chain: Chain,
    other_chain_index: int,
) -> TrueChainContactCandidate | None:
    best_candidate: TrueChainContactCandidate | None = None
    for first_segment_index, first_segment in enumerate(
        _chain_segments(first_chain),
        start=1,
    ):
        for other_segment_index, other_segment in enumerate(
            _chain_segments(other_chain),
            start=1,
        ):
            closest = closest_segment_points(first_segment, other_segment)
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = TrueChainContactCandidate(
                chain_index=other_chain_index,
                source_bead=first_segment_index + closest.first_fraction,
                other_source_bead=other_segment_index + closest.second_fraction,
                distance=closest.distance,
            )
    return best_candidate


def _chain_segments(chain: Chain) -> tuple[Segment, ...]:
    return tuple(
        Segment(start=first_node, end=second_node)
        for first_node, second_node in zip(
            chain.nodes[:-1],
            chain.nodes[1:],
            strict=True,
        )
    )


def _nearest_true_chain_contact_sequence_for_sources(
    candidates: tuple[TrueChainContactCandidate, ...],
    source_sequence: tuple[float, ...] | None,
) -> tuple[int, ...] | None:
    if source_sequence is None:
        return None
    if len(candidates) == 0:
        return ()
    return tuple(
        min(
            candidates,
            key=lambda candidate: (
                abs(candidate.source_bead - source_bead),
                candidate.distance,
                candidate.chain_index,
            ),
        ).chain_index
        for source_bead in source_sequence
    )


def _oracle_default_source_sequence(
    request: RegressionRequest,
    benchmark_id: str,
) -> tuple[float, ...] | None:
    default_sp_path = (
        request.oracle_root
        / f"benchmark-{benchmark_id}"
        / RegressionMode.DEFAULT.value
        / "Z1+SP.dat"
    )
    if not default_sp_path.exists():
        return None
    default_shortest_path = parse_shortest_path_text(
        default_sp_path.read_text(encoding="utf-8"),
    )
    return _entanglement_source_sequence(default_shortest_path)


def _entanglement_source_sequence(
    snapshot: ShortestPathSnapshot,
) -> tuple[float, ...]:
    if snapshot.chain_count == 0:
        return ()
    return tuple(
        node.source_bead
        for node in snapshot.chains[0].nodes
        if node.is_entanglement
    )


def _source_sequence_mismatch_count(
    actual: tuple[float, ...],
    expected: tuple[float, ...] | None,
) -> int | None:
    if expected is None:
        return None
    shared_count = min(len(actual), len(expected))
    return abs(len(actual) - len(expected)) + sum(
        abs(actual[index] - expected[index]) > SOURCE_BEAD_TOLERANCE
        for index in range(shared_count)
    )


def _source_sequence_max_delta(
    actual: tuple[float, ...],
    expected: tuple[float, ...] | None,
) -> float | None:
    if expected is None:
        return None
    shared_count = min(len(actual), len(expected))
    if shared_count == 0:
        return 0.0
    return max(abs(actual[index] - expected[index]) for index in range(shared_count))


def _source_sequence_residuals(
    actual: tuple[float, ...],
    expected: tuple[float, ...] | None,
) -> tuple[SourceSequenceResidual, ...] | None:
    if expected is None:
        return None
    return tuple(
        SourceSequenceResidual(
            source_index=index,
            actual=actual_source,
            expected=expected_source,
            delta=(
                abs(actual_source - expected_source)
                if actual_source is not None and expected_source is not None
                else None
            ),
        )
        for index, (actual_source, expected_source) in enumerate(
            zip_longest(actual, expected),
        )
        if actual_source is None
        or expected_source is None
        or abs(actual_source - expected_source) > SOURCE_BEAD_TOLERANCE
    )


def _chain_contour_residuals(
    actual: ShortestPathSnapshot,
    expected: ShortestPathSnapshot,
) -> tuple[ChainContourResidual, ...]:
    actual_contours = _shortest_path_chain_contours(actual)
    expected_contours = _shortest_path_chain_contours(expected)
    return tuple(
        ChainContourResidual(
            chain_index=index,
            actual=actual_contour,
            expected=expected_contour,
            delta=(
                abs(actual_contour - expected_contour)
                if actual_contour is not None and expected_contour is not None
                else None
            ),
        )
        for index, (actual_contour, expected_contour) in enumerate(
            zip_longest(actual_contours, expected_contours),
            start=1,
        )
        if actual_contour is None
        or expected_contour is None
        or abs(actual_contour - expected_contour) > SHORTEST_PATH_POSITION_TOLERANCE
    )


def _chain_contour_statistics(
    actual: ShortestPathSnapshot,
    expected: ShortestPathSnapshot,
) -> _ChainContourStatistics:
    deltas = _chain_contour_deltas(actual, expected)
    if len(deltas) == 0:
        return _ChainContourStatistics(
            mean_absolute_delta=0.0,
            root_mean_square_delta=0.0,
        )
    return _ChainContourStatistics(
        mean_absolute_delta=sum(deltas) / len(deltas),
        root_mean_square_delta=sqrt(
            sum(delta * delta for delta in deltas) / len(deltas),
        ),
    )


def _chain_contour_residual_fraction(
    residual_count: int,
    compared_chain_count: int,
) -> float:
    if compared_chain_count == 0:
        return 0.0
    return residual_count / compared_chain_count


def _chain_contour_deltas(
    actual: ShortestPathSnapshot,
    expected: ShortestPathSnapshot,
) -> tuple[float, ...]:
    actual_contours = _shortest_path_chain_contours(actual)
    expected_contours = _shortest_path_chain_contours(expected)
    return tuple(
        abs(actual_contour - expected_contour)
        for actual_contour, expected_contour in zip_longest(
            actual_contours,
            expected_contours,
        )
        if actual_contour is not None and expected_contour is not None
    )


def _shortest_path_chain_contours(
    snapshot: ShortestPathSnapshot,
) -> tuple[float, ...]:
    return tuple(_shortest_path_chain_contour(chain) for chain in snapshot.chains)


def _shortest_path_chain_contour(chain: ShortestPathChain) -> float:
    return sum(
        _node_distance(first, second)
        for first, second in zip(chain.nodes[:-1], chain.nodes[1:], strict=True)
    )


def _node_distance(first: ShortestPathNode, second: ShortestPathNode) -> float:
    dx = first.position.x - second.position.x
    dy = first.position.y - second.position.y
    dz = first.position.z - second.position.z
    return sqrt(dx * dx + dy * dy + dz * dz)


def _max_chain_contour_delta(
    residuals: tuple[ChainContourResidual, ...],
) -> float:
    finite_deltas = tuple(
        residual.delta for residual in residuals if residual.delta is not None
    )
    if len(finite_deltas) == 0:
        return 0.0
    return max(finite_deltas)


def _max_chain_contour_delta_chain(
    residuals: tuple[ChainContourResidual, ...],
) -> int | None:
    finite_residuals = tuple(
        residual for residual in residuals if residual.delta is not None
    )
    if len(finite_residuals) == 0:
        return None
    return max(finite_residuals, key=_chain_contour_residual_delta).chain_index


def _chain_contour_residual_delta(residual: ChainContourResidual) -> float:
    if residual.delta is None:
        return -1.0
    return residual.delta


def _format_report(records: tuple[RegressionRecord, ...]) -> str:
    header = (
        "| benchmark | mode | status | statistical status | Lpp delta | Z delta | "
        "max chain contour delta | max chain contour delta chain | "
        "mean chain contour delta | rms chain contour delta | "
        "chain contour residual count | chain contour residual fraction | "
        "chain contour residual details | "
        "summary field mismatches | pair mismatches | "
        "node count mismatches | max node position delta | "
        "max node delta chain | max node delta node | "
        "max node delta actual source | "
        "max node delta expected source | "
        "max node source bead delta | "
        "max source delta chain | "
        "max source delta node | "
        "source bead residual details | "
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
        "pyz1 obstacle pair sequence | "
        "oracle obstacle pair sequence | "
        "pyz1 winding candidates | "
        "pyz1 winding missing oracle sequence | "
        "pyz1 winding extra candidates | "
        "pyz1 convex winding candidates | "
        "pyz1 convex winding missing oracle sequence | "
        "pyz1 convex winding extra candidates | "
        "pyz1 convex selected winding sequence | "
        "pyz1 convex selected missing oracle sequence | "
        "pyz1 convex selected extra candidates | "
        "pyz1 blocked trace obstacle sequence | "
        "pyz1 retained blocked trace obstacle sequence | "
        "max oracle obstacle source delta | "
        "max oracle obstacle source delta chain | "
        "oracle obstacle source residual details | "
        "max oracle source segment rank | "
        "oracle source segment ambiguity details | "
        "oracle default source sequence | "
        "oracle source sequence matches default | "
        "pyz1 source sequence | "
        "pyz1 source sequence mismatches | "
        "pyz1 source sequence max delta | "
        "pyz1 source sequence residual details | "
        "pyz1 true-chain pair sequence | "
        "pyz1 true-chain contact candidate sequence | "
        "pyz1 true-chain contact candidate details | "
        "oracle-source nearest true-chain contact sequence | "
        "oracle true-chain pair sequence | "
        "pyz1 true-chain pair node sequence | "
        "oracle true-chain pair node sequence | "
        "summary mismatch details | note |"
    )
    lines = [
        "# pyz1 Benchmark Regression",
        "",
        header,
        _format_report_separator(header),
    ]
    lines.extend(_format_record(record) for record in records)
    return "\n".join(lines) + "\n"


def _format_report_separator(header: str) -> str:
    column_count = len(header.strip().strip("|").split("|"))
    return "| " + " | ".join("---" for _ in range(column_count)) + " |"


def _format_record(record: RegressionRecord) -> str:
    return (
        f"| benchmark-{record.benchmark_id} | {record.mode.value} | "
        f"{record.status.value} | {record.statistical_status.value} | "
        f"{_format_optional_float(record.lpp_delta)} | "
        f"{_format_optional_float(record.z_delta)} | "
        f"{_format_optional_float(record.max_chain_contour_delta)} | "
        f"{_format_optional_int(record.max_chain_contour_delta_chain)} | "
        f"{_format_optional_float(record.mean_chain_contour_delta)} | "
        f"{_format_optional_float(record.root_mean_square_chain_contour_delta)} | "
        f"{_format_optional_int(record.chain_contour_residual_count)} | "
        f"{_format_optional_float(record.chain_contour_residual_fraction)} | "
        f"{_format_chain_contour_residuals(record.chain_contour_residuals)} | "
        f"{_format_optional_int(record.summary_field_mismatches)} | "
        f"{_format_optional_int(record.pairing_mismatches)} | "
        f"{_format_optional_int(record.node_count_mismatches)} | "
        f"{_format_optional_float(record.max_node_position_delta)} | "
        f"{_format_optional_int(record.max_node_delta_chain_index)} | "
        f"{_format_optional_int(record.max_node_delta_node_index)} | "
        f"{_format_optional_float(record.max_node_delta_actual_source_bead)} | "
        f"{_format_optional_float(record.max_node_delta_expected_source_bead)} | "
        f"{_format_optional_float(record.max_node_source_bead_delta)} | "
        f"{_format_optional_int(record.max_source_delta_chain_index)} | "
        f"{_format_optional_int(record.max_source_delta_node_index)} | "
        f"{_format_source_bead_residuals(record.source_bead_residuals)} | "
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
        f"{_format_int_sequence(record.pyz1_obstacle_pair_sequence)} | "
        f"{_format_int_sequence(record.oracle_obstacle_pair_sequence)} | "
        f"{_format_optional_int(record.pyz1_winding_candidate_count)} | "
        f"{_format_int_sequence(record.pyz1_winding_missing_oracle_sequence)} | "
        f"{_format_optional_int(record.pyz1_winding_extra_candidate_count)} | "
        f"{_format_optional_int(record.pyz1_convex_winding_candidate_count)} | "
        f"{_format_int_sequence(record.pyz1_convex_winding_missing_oracle_sequence)} | "
        f"{_format_optional_int(record.pyz1_convex_winding_extra_candidate_count)} | "
        f"{_format_int_sequence(record.pyz1_convex_selected_winding_sequence)} | "
        f"{_format_convex_selected_missing_sequence(record)} | "
        f"{_format_optional_int(record.pyz1_convex_selected_extra_count)} | "
        f"{_format_int_sequence(record.pyz1_blocked_trace_obstacle_sequence)} | "
        f"{_format_retained_blocked_trace_sequence(record)} | "
        f"{_format_optional_float(record.max_oracle_obstacle_source_delta)} | "
        f"{_format_optional_int(record.max_oracle_obstacle_source_delta_chain)} | "
        f"{_format_oracle_obstacle_source_residuals(record)} | "
        f"{_format_optional_int(record.max_oracle_obstacle_source_segment_rank)} | "
        f"{_format_oracle_source_segment_ambiguities(record)} | "
        f"{_format_float_sequence(record.oracle_default_source_sequence)} | "
        f"{_format_oracle_source_sequence_default_match(record)} | "
        f"{_format_float_sequence(record.pyz1_source_sequence)} | "
        f"{_format_optional_int(record.pyz1_source_sequence_mismatch_count)} | "
        f"{_format_optional_float(record.pyz1_source_sequence_max_delta)} | "
        f"{_format_source_sequence_residuals(record.pyz1_source_sequence_residuals)} | "
        f"{_format_int_sequence(record.pyz1_true_chain_pair_sequence)} | "
        f"{_format_int_sequence(record.pyz1_true_chain_contact_candidate_sequence)} | "
        f"{_format_true_chain_contact_candidates(record)} | "
        f"{_format_oracle_source_nearest_contact_sequence(record)} | "
        f"{_format_int_sequence(record.oracle_true_chain_pair_sequence)} | "
        f"{_format_int_sequence(record.pyz1_true_chain_pair_node_sequence)} | "
        f"{_format_int_sequence(record.oracle_true_chain_pair_node_sequence)} | "
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


def _format_int_sequence(values: tuple[int, ...] | None) -> str:
    if values is None:
        return "n/a"
    if len(values) == 0:
        return "none"
    return ",".join(str(value) for value in values)


def _format_float_sequence(values: tuple[float, ...] | None) -> str:
    if values is None:
        return "n/a"
    if len(values) == 0:
        return "none"
    return ",".join(_format_optional_float(value) for value in values)


def _format_optional_bool(value: bool | None) -> str:
    if value is None:
        return "n/a"
    if value:
        return "yes"
    return "no"


def _format_oracle_source_sequence_default_match(
    record: RegressionRecord,
) -> str:
    return _format_optional_bool(record.oracle_mode_source_sequence_matches_default)


def _format_source_sequence_residuals(
    residuals: tuple[SourceSequenceResidual, ...] | None,
) -> str:
    if residuals is None:
        return "n/a"
    if len(residuals) == 0:
        return "none"
    visible = residuals[:MAX_SOURCE_RESIDUAL_REPORT_DETAILS]
    formatted = "; ".join(_format_source_sequence_residual(item) for item in visible)
    omitted_count = len(residuals) - len(visible)
    if omitted_count == 0:
        return formatted
    return f"{formatted}; ... {omitted_count} more"


def _format_source_sequence_residual(residual: SourceSequenceResidual) -> str:
    return (
        f"{residual.source_index}: "
        f"{_format_optional_float(residual.actual)}"
        f"!={_format_optional_float(residual.expected)}"
        f"(d={_format_optional_float(residual.delta)})"
    )


def _format_chain_contour_residuals(
    residuals: tuple[ChainContourResidual, ...] | None,
) -> str:
    if residuals is None:
        return "n/a"
    if len(residuals) == 0:
        return "none"
    visible = residuals[:MAX_SOURCE_RESIDUAL_REPORT_DETAILS]
    formatted = "; ".join(_format_chain_contour_residual(item) for item in visible)
    omitted_count = len(residuals) - len(visible)
    if omitted_count == 0:
        return formatted
    return f"{formatted}; ... {omitted_count} more"


def _format_chain_contour_residual(residual: ChainContourResidual) -> str:
    return (
        f"c{residual.chain_index}: "
        f"{_format_optional_float(residual.actual)}"
        f"!={_format_optional_float(residual.expected)}"
        f"(d={_format_optional_float(residual.delta)})"
    )


def _format_true_chain_contact_candidates(record: RegressionRecord) -> str:
    candidates = record.pyz1_true_chain_contact_candidate_details
    if candidates is None:
        return "n/a"
    if len(candidates) == 0:
        return "none"
    visible = candidates[:MAX_SOURCE_RESIDUAL_REPORT_DETAILS]
    formatted = "; ".join(
        _format_true_chain_contact_candidate(candidate) for candidate in visible
    )
    omitted_count = len(candidates) - len(visible)
    if omitted_count == 0:
        return formatted
    return f"{formatted}; ... {omitted_count} more"


def _format_true_chain_contact_candidate(
    candidate: TrueChainContactCandidate,
) -> str:
    return (
        f"{candidate.chain_index}: "
        f"s={_format_optional_float(candidate.source_bead)} "
        f"other={_format_optional_float(candidate.other_source_bead)} "
        f"d={_format_optional_float(candidate.distance)}"
    )


def _format_oracle_source_nearest_contact_sequence(record: RegressionRecord) -> str:
    return _format_int_sequence(
        record.oracle_source_nearest_true_chain_contact_sequence,
    )


def _format_convex_selected_missing_sequence(record: RegressionRecord) -> str:
    return _format_int_sequence(record.pyz1_convex_selected_missing_oracle_sequence)


def _format_retained_blocked_trace_sequence(record: RegressionRecord) -> str:
    return _format_int_sequence(record.pyz1_retained_blocked_trace_obstacle_sequence)


def _format_oracle_obstacle_source_residuals(record: RegressionRecord) -> str:
    residuals = record.oracle_obstacle_source_residuals
    if residuals is None:
        return "n/a"
    if len(residuals) == 0:
        return "none"
    visible = residuals[:MAX_SOURCE_RESIDUAL_REPORT_DETAILS]
    formatted = "; ".join(
        _format_oracle_obstacle_source_residual(residual)
        for residual in visible
    )
    omitted_count = len(residuals) - len(visible)
    if omitted_count == 0:
        return formatted
    return f"{formatted}; ... {omitted_count} more"


def _format_oracle_obstacle_source_residual(
    residual: OracleObstacleSourceResidual,
) -> str:
    return (
        f"{residual.chain_index}: "
        f"{_format_optional_float(residual.actual)}"
        f"!={_format_optional_float(residual.expected)}"
        f"(d={_format_optional_float(residual.delta)})"
    )


def _format_oracle_source_segment_ambiguities(record: RegressionRecord) -> str:
    ambiguities = record.oracle_obstacle_source_segment_ambiguities
    if ambiguities is None:
        return "n/a"
    if len(ambiguities) == 0:
        return "none"
    visible = ambiguities[:MAX_SOURCE_RESIDUAL_REPORT_DETAILS]
    formatted = "; ".join(
        _format_oracle_source_segment_ambiguity(ambiguity)
        for ambiguity in visible
    )
    omitted_count = len(ambiguities) - len(visible)
    if omitted_count == 0:
        return formatted
    return f"{formatted}; ... {omitted_count} more"


def _format_oracle_source_segment_ambiguity(
    ambiguity: OracleObstacleSourceSegmentAmbiguity,
) -> str:
    return (
        f"{ambiguity.chain_index}: "
        f"r{ambiguity.expected_rank} "
        f"{_format_optional_float(ambiguity.expected_rank_source)}"
        f"!={_format_optional_float(ambiguity.expected_source)} "
        f"nearest={_format_optional_float(ambiguity.nearest_source)}"
        f"(d={_format_optional_float(ambiguity.nearest_distance)}) "
        f"chosen_d={_format_optional_float(ambiguity.expected_rank_distance)}"
    )


def _format_source_bead_residuals(
    residuals: tuple[SourceBeadResidual, ...] | None,
) -> str:
    if residuals is None:
        return "n/a"
    if len(residuals) == 0:
        return "none"
    visible = residuals[:MAX_SOURCE_RESIDUAL_REPORT_DETAILS]
    formatted = "; ".join(_format_source_bead_residual(item) for item in visible)
    omitted_count = len(residuals) - len(visible)
    if omitted_count == 0:
        return formatted
    return f"{formatted}; ... {omitted_count} more"


def _format_source_bead_residual(residual: SourceBeadResidual) -> str:
    return (
        f"c{residual.chain_index}n{residual.node_index}"
        f"[{_format_optional_int(residual.actual_pair_chain_index)}"
        f"->{_format_optional_int(residual.expected_pair_chain_index)}]: "
        f"{_format_optional_float(residual.actual)}"
        f"!={_format_optional_float(residual.expected)}"
        f"(d={_format_optional_float(residual.delta)})"
    )


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
