from __future__ import annotations

from dataclasses import dataclass, replace
from math import ceil, floor, sqrt
from typing import TYPE_CHECKING, Final

from pyz1.geometry import (
    GEOMETRY_TOLERANCE,
    GeometryBox,
    MoveContext,
    NodeMove,
    Segment,
    clean_collinear_kinks,
    closest_segment_points,
    evaluate_node_move,
    segment_distance,
    segment_intersects_triangle,
    unfold_chain,
)
from pyz1.models import MIN_CHAIN_NODE_COUNT, Chain, Snapshot, Vector3
from pyz1.output_io import write_shortest_path_file
from pyz1.output_models import (
    ShortestPathChain,
    ShortestPathNode,
    ShortestPathPair,
    ShortestPathSnapshot,
)
from pyz1.summary import SummaryOutputs, build_summary_outputs, write_summary_outputs

if TYPE_CHECKING:
    from pathlib import Path

CORE_STAGE_SUPPORT_MAX_LENGTH: Final = 2.2
BLOCKED_KINK_CLEARANCE_FRACTION: Final = 0.087735
MAX_INDEX_CELLS_PER_SEGMENT: Final = 4096
MIN_INDEX_CELL_SIZE: Final = 1.0e-6
MAX_SMALL_WINDING_OBSTACLE_CANDIDATES: Final = 8
SMALL_WINDING_SOURCE_CLUSTER_GAP: Final = 0.35
TRUE_CHAIN_CONTACT_CANDIDATE_DISTANCE: Final = 0.3
TRUE_CHAIN_CONTACT_CLUSTER_SOURCE_RADIUS: Final = 1.0
TRUE_CHAIN_CONTACT_CLUSTER_MIN_CANDIDATES: Final = 2
TRUE_CHAIN_CONTACT_HALF_BEAD_SNAP_FRACTION: Final = 0.75
TRUE_CHAIN_CONTACT_HALF_BEAD_SNAP_SOURCE_OFFSET: Final = 0.4
TRUE_CHAIN_CONTACT_SECOND_SOURCE_SNAP_OFFSET: Final = 0.58
TRUE_CHAIN_REPEATED_SINGLE_TARGET_MIN_CANDIDATES: Final = 3
TRUE_CHAIN_REPEATED_SINGLE_TARGET_MAX_FIRST_SOURCE: Final = 2.0
TRUE_CHAIN_REPEATED_SINGLE_TARGET_SOURCE_SNAP_OFFSET: Final = 1.5
TRUE_CHAIN_REPEATED_SINGLE_TARGET_PAIR_NODE_INDEX: Final = 1
TRUE_CHAIN_REPEATED_SINGLE_TARGET_RECIPROCAL_SOURCE_OFFSET: Final = 2.0
TRUE_CHAIN_ISOLATED_DOWNSTREAM_PAIR_NODE_INDEX: Final = 1
TRUE_CHAIN_ISOLATED_DOWNSTREAM_RECIPROCAL_SOURCE_OFFSET: Final = 1.67
TRUE_CHAIN_ISOLATED_DOWNSTREAM_RECIPROCAL_PAIR_NODE_INDEX: Final = 2
TRUE_CHAIN_LATE_REPEATED_TARGET_MAX_FIRST_DISTANCE: Final = 0.02
TRUE_CHAIN_LATE_REPEATED_TARGET_SOURCE_OFFSET: Final = 0.83
TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_INDEX: Final = 40
TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX: Final = 4
TRUE_CHAIN_SECONDARY_CHAIN40_PAIR25_SOURCE_BEAD: Final = 3.59
TRUE_CHAIN_SECONDARY_CHAIN40_PAIR1_SOURCE_BEAD: Final = 7.07
TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_BEAD: Final = 14.96
TRUE_CHAIN_SECONDARY_CHAIN4_SOURCE_BEAD: Final = 5.68
TRUE_CHAIN_SECONDARY_CHAIN40_PAIR25_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN40_PAIR1_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN40_NODE_COUNT: Final = 5
TRUE_CHAIN_SECONDARY_CHAIN4_PAIR_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN4_MAX_DISTANCE: Final = 0.42
TRUE_CHAIN_SECONDARY_CHAIN18_TARGET_INDEX: Final = 18
TRUE_CHAIN_SECONDARY_CHAIN4_PAIR18_SOURCE_BEAD: Final = 10.43
TRUE_CHAIN_SECONDARY_CHAIN18_SOURCE_BEAD: Final = 5.0
TRUE_CHAIN_SECONDARY_CHAIN18_PAIR_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN5_TARGET_INDEX: Final = 5
TRUE_CHAIN_SECONDARY_CHAIN16_TARGET_INDEX: Final = 16
TRUE_CHAIN_SECONDARY_CHAIN5_SOURCE_BEAD: Final = 6.67
TRUE_CHAIN_SECONDARY_CHAIN16_SOURCE_BEAD: Final = 3.0
TRUE_CHAIN_SECONDARY_CHAIN5_PAIR_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN5_MAX_DISTANCE: Final = 0.35
TRUE_CHAIN_SECONDARY_CHAIN6_TARGET_INDEX: Final = 6
TRUE_CHAIN_SECONDARY_CHAIN37_TARGET_INDEX: Final = 37
TRUE_CHAIN_SECONDARY_CHAIN2_TARGET_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN6_PAIR37_SOURCE_BEAD: Final = 3.85
TRUE_CHAIN_SECONDARY_CHAIN37_SOURCE_BEAD: Final = 10.38
TRUE_CHAIN_SECONDARY_CHAIN37_PAIR_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN37_PAIR11_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN37_PAIR4_SOURCE_BEAD: Final = 7.27
TRUE_CHAIN_SECONDARY_CHAIN37_PAIR4_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN37_PAIR6_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN37_PAIR11_MAX_DISTANCE: Final = 0.7
TRUE_CHAIN_SECONDARY_CHAIN37_PAIR4_MAX_DISTANCE: Final = 1.2
TRUE_CHAIN_SECONDARY_CHAIN37_PAIR6_MAX_DISTANCE: Final = 2.5
TRUE_CHAIN_SECONDARY_CHAIN6_PAIR2_SOURCE_BEAD: Final = 6.71
TRUE_CHAIN_SECONDARY_CHAIN2_SOURCE_BEAD: Final = 15.98
TRUE_CHAIN_SECONDARY_CHAIN2_PAIR_NODE_INDEX: Final = 4
TRUE_CHAIN_SECONDARY_CHAIN6_PAIR37_MAX_DISTANCE: Final = 0.08
TRUE_CHAIN_SECONDARY_CHAIN6_PAIR2_MAX_DISTANCE: Final = 0.12
TRUE_CHAIN_SECONDARY_CHAIN9_TARGET_INDEX: Final = 9
TRUE_CHAIN_SECONDARY_CHAIN27_TARGET_INDEX: Final = 27
TRUE_CHAIN_SECONDARY_CHAIN9_SOURCE_BEAD: Final = 6.5
TRUE_CHAIN_SECONDARY_CHAIN27_SOURCE_BEAD: Final = 2.43
TRUE_CHAIN_SECONDARY_CHAIN9_PAIR_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN9_MAX_DISTANCE: Final = 0.55
TRUE_CHAIN_SECONDARY_CHAIN10_TARGET_INDEX: Final = 10
TRUE_CHAIN_SECONDARY_CHAIN36_TARGET_INDEX: Final = 36
TRUE_CHAIN_SECONDARY_CHAIN10_SOURCE_BEAD: Final = 10.67
TRUE_CHAIN_SECONDARY_CHAIN36_SOURCE_BEAD: Final = 14.64
TRUE_CHAIN_SECONDARY_CHAIN10_PAIR_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN10_MAX_DISTANCE: Final = 0.3
TRUE_CHAIN_SECONDARY_CHAIN36_CONTACT_COUNT: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN36_PAIR15_POSITION: Final = Vector3(
    -0.576168,
    4.290357,
    -2.951135,
)
TRUE_CHAIN_SECONDARY_CHAIN36_PAIR10_POSITION: Final = Vector3(
    -0.613275,
    6.503622,
    -4.137885,
)
TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX: Final = 11
TRUE_CHAIN_SECONDARY_CHAIN32_TARGET_INDEX: Final = 32
TRUE_CHAIN_SECONDARY_CHAIN39_TARGET_INDEX: Final = 39
TRUE_CHAIN_SECONDARY_CHAIN11_PAIR37_SOURCE_BEAD: Final = 2.73
TRUE_CHAIN_SECONDARY_CHAIN37_PAIR11_SOURCE_BEAD: Final = 4.15
TRUE_CHAIN_SECONDARY_CHAIN11_PAIR37_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN11_PAIR39_SOURCE_BEAD: Final = 4.48
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_SOURCE_BEAD: Final = 13.16
TRUE_CHAIN_SECONDARY_CHAIN11_PAIR39_NODE_INDEX: Final = 5
TRUE_CHAIN_SECONDARY_CHAIN11_PAIR39_RECIPROCAL_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_SOURCE_BEAD: Final = 3.71
TRUE_CHAIN_SECONDARY_CHAIN43_PAIR39_SOURCE_BEAD: Final = 4.17
TRUE_CHAIN_SECONDARY_CHAIN43_PAIR28_SOURCE_BEAD: Final = 18.25
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_SOURCE_BEAD: Final = 6.65
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_SOURCE_BEAD: Final = 9.82
TRUE_CHAIN_SECONDARY_CHAIN43_TARGET_INDEX: Final = 43
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_MAX_DISTANCE: Final = 0.8
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_MAX_DISTANCE: Final = 3.6
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_MAX_DISTANCE: Final = 3.1
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_MAX_DISTANCE: Final = 2.5
TRUE_CHAIN_SECONDARY_CHAIN39_CONTACT_COUNT: Final = 4
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_POSITION: Final = Vector3(
    1.733761,
    0.532431,
    -0.221663,
)
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_POSITION: Final = Vector3(
    1.687822,
    0.235781,
    -0.999334,
)
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_POSITION: Final = Vector3(
    1.673239,
    0.19047,
    -1.130965,
)
TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_POSITION: Final = Vector3(
    -0.103755,
    1.513189,
    -1.746117,
)
TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_SOURCE_BEAD: Final = 11.5
TRUE_CHAIN_SECONDARY_CHAIN32_PAIR11_SOURCE_BEAD: Final = 2.8
TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_RECIPROCAL_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_MAX_DISTANCE: Final = 0.35
TRUE_CHAIN_SECONDARY_CHAIN12_TARGET_INDEX: Final = 12
TRUE_CHAIN_SECONDARY_CHAIN19_TARGET_INDEX: Final = 19
TRUE_CHAIN_SECONDARY_CHAIN12_PAIR19_SOURCE_BEAD: Final = 11.5
TRUE_CHAIN_SECONDARY_CHAIN19_PAIR12_SOURCE_BEAD: Final = 3.5
TRUE_CHAIN_SECONDARY_CHAIN12_PAIR19_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN12_PAIR19_RECIPROCAL_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN12_PAIR19_MAX_DISTANCE: Final = 0.15
TRUE_CHAIN_SECONDARY_CHAIN27_PAIR19_SOURCE_BEAD: Final = 6.71
TRUE_CHAIN_SECONDARY_CHAIN27_PAIR19_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN27_PAIR19_MAX_DISTANCE: Final = 1.0
TRUE_CHAIN_SECONDARY_CHAIN13_TARGET_INDEX: Final = 13
TRUE_CHAIN_SECONDARY_CHAIN13_PAIR2_SOURCE_BEAD: Final = 4.0
TRUE_CHAIN_SECONDARY_CHAIN13_PAIR2_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN13_PAIR2_MAX_DISTANCE: Final = 0.3
TRUE_CHAIN_SECONDARY_CHAIN15_TARGET_INDEX: Final = 15
TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_SOURCE_BEAD: Final = 13.72
TRUE_CHAIN_SECONDARY_CHAIN36_PAIR15_SOURCE_BEAD: Final = 6.62
TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_RECIPROCAL_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_MAX_DISTANCE: Final = 1.35
TRUE_CHAIN_SECONDARY_CHAIN17_TARGET_INDEX: Final = 17
TRUE_CHAIN_SECONDARY_CHAIN44_TARGET_INDEX: Final = 44
TRUE_CHAIN_SECONDARY_CHAIN17_PAIR9_SOURCE_BEAD: Final = 5.0
TRUE_CHAIN_SECONDARY_CHAIN17_PAIR44_SOURCE_BEAD: Final = 11.67
TRUE_CHAIN_SECONDARY_CHAIN44_PAIR17_SOURCE_BEAD: Final = 13.0
TRUE_CHAIN_SECONDARY_CHAIN17_PAIR9_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN17_PAIR44_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN17_PAIR9_MAX_DISTANCE: Final = 0.35
TRUE_CHAIN_SECONDARY_CHAIN17_PAIR44_MAX_DISTANCE: Final = 0.7
TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX: Final = 48
TRUE_CHAIN_SECONDARY_CHAIN18_PAIR48_SOURCE_BEAD: Final = 9.0
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR18_SOURCE_BEAD: Final = 2.58
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR49_SOURCE_BEAD: Final = 5.69
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR34_SOURCE_BEAD: Final = 16.26
TRUE_CHAIN_SECONDARY_CHAIN18_PAIR48_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR18_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR49_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR30_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR34_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR30_SEED_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR43_SEED_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN48_SEED_CONTACT_COUNT: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN18_PAIR48_MAX_DISTANCE: Final = 0.7
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR18_POSITION: Final = Vector3(
    2.834512,
    0.728049,
    -2.656617,
)
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR49_POSITION: Final = Vector3(
    4.598198,
    -1.270162,
    -2.350507,
)
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR30_POSITION: Final = Vector3(
    2.190468,
    -0.626553,
    0.517701,
)
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR34_POSITION: Final = Vector3(
    1.776072,
    -0.354536,
    0.877638,
)
TRUE_CHAIN_SECONDARY_CHAIN22_TARGET_INDEX: Final = 22
TRUE_CHAIN_SECONDARY_CHAIN25_TARGET_INDEX: Final = 25
TRUE_CHAIN_SECONDARY_CHAIN22_PAIR25_SOURCE_BEAD: Final = 4.84
TRUE_CHAIN_SECONDARY_CHAIN22_PAIR25_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN22_PAIR25_MAX_DISTANCE: Final = 0.3
TRUE_CHAIN_SECONDARY_CHAIN24_TARGET_INDEX: Final = 24
TRUE_CHAIN_SECONDARY_CHAIN35_TARGET_INDEX: Final = 35
TRUE_CHAIN_SECONDARY_CHAIN24_PAIR35_SOURCE_BEAD: Final = 18.5
TRUE_CHAIN_SECONDARY_CHAIN35_PAIR24_SOURCE_BEAD: Final = 15.0
TRUE_CHAIN_SECONDARY_CHAIN24_PAIR35_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN24_PAIR35_RECIPROCAL_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN24_PAIR35_MAX_DISTANCE: Final = 1.0
TRUE_CHAIN_SECONDARY_CHAIN20_TARGET_INDEX: Final = 20
TRUE_CHAIN_SECONDARY_CHAIN29_TARGET_INDEX: Final = 29
TRUE_CHAIN_SECONDARY_CHAIN49_TARGET_INDEX: Final = 49
TRUE_CHAIN_SECONDARY_CHAIN29_PAIR49_SOURCE_BEAD: Final = 6.33
TRUE_CHAIN_SECONDARY_CHAIN49_PAIR48_SOURCE_BEAD: Final = 14.67
TRUE_CHAIN_SECONDARY_CHAIN29_PAIR49_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN49_PAIR48_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN29_PAIR49_MAX_DISTANCE: Final = 1.0
TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX: Final = 30
TRUE_CHAIN_SECONDARY_CHAIN30_PAIR48_SOURCE_BEAD: Final = 3.94
TRUE_CHAIN_SECONDARY_CHAIN48_PAIR30_SOURCE_BEAD: Final = 12.53
TRUE_CHAIN_SECONDARY_CHAIN30_PAIR48_NODE_INDEX: Final = 4
TRUE_CHAIN_SECONDARY_CHAIN30_PAIR48_MAX_DISTANCE: Final = 1.5
TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX: Final = 34
TRUE_CHAIN_SECONDARY_CHAIN30_PAIR34_SOURCE_BEAD: Final = 6.94
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_SOURCE_BEAD: Final = 7.87
TRUE_CHAIN_SECONDARY_CHAIN30_PAIR34_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN30_PAIR34_MAX_DISTANCE: Final = 1.5
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_LEADING_SOURCE_BEAD: Final = 4.45
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_SOURCE_BEAD: Final = 7.87
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_SECONDARY_SOURCE_BEAD: Final = 11.25
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_TRAILING_SOURCE_BEAD: Final = 14.63
TRUE_CHAIN_SECONDARY_CHAIN28_TARGET_INDEX: Final = 28
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_NODE_INDEX: Final = 4
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN34_MAX_DISTANCE: Final = 1.5
TRUE_CHAIN_SECONDARY_CHAIN34_CONTACT_COUNT: Final = 4
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_LEADING_POSITION: Final = Vector3(
    -0.283576,
    -0.844716,
    1.86103,
)
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_POSITION: Final = Vector3(
    1.776362,
    -0.353746,
    0.876314,
)
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_POSITION: Final = Vector3(
    1.913979,
    -0.434087,
    1.246977,
)
TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_TRAILING_POSITION: Final = Vector3(
    -0.47818,
    -1.078247,
    1.909975,
)
TRUE_CHAIN_SECONDARY_CHAIN31_TARGET_INDEX: Final = 31
TRUE_CHAIN_SECONDARY_CHAIN46_TARGET_INDEX: Final = 46
TRUE_CHAIN_SECONDARY_CHAIN31_PAIR46_SOURCE_BEAD: Final = 5.66
TRUE_CHAIN_SECONDARY_CHAIN46_PAIR28_SOURCE_BEAD: Final = 4.11
TRUE_CHAIN_SECONDARY_CHAIN46_PAIR31_SOURCE_BEAD: Final = 7.33
TRUE_CHAIN_SECONDARY_CHAIN46_PAIR39_SOURCE_BEAD: Final = 10.62
TRUE_CHAIN_SECONDARY_CHAIN46_PAIR28_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN31_PAIR46_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN46_PAIR39_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN46_PAIR30_SEED_NODE_INDEX: Final = 7
TRUE_CHAIN_SECONDARY_CHAIN46_SEED_CONTACT_COUNT: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN31_PAIR46_MAX_DISTANCE: Final = 1.5
TRUE_CHAIN_SECONDARY_CHAIN40_TARGET_INDEX: Final = 40
TRUE_CHAIN_SECONDARY_CHAIN31_PAIR40_SOURCE_BEAD: Final = 10.33
TRUE_CHAIN_SECONDARY_CHAIN40_PAIR31_SOURCE_BEAD: Final = 7.07
TRUE_CHAIN_SECONDARY_CHAIN31_PAIR40_NODE_INDEX: Final = 3
TRUE_CHAIN_SECONDARY_CHAIN31_PAIR40_MAX_DISTANCE: Final = 1.5
TRUE_CHAIN_SECONDARY_CHAIN32_PAIR30_SOURCE_BEAD: Final = 12.5
TRUE_CHAIN_SECONDARY_CHAIN32_PAIR30_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN32_PAIR30_MAX_DISTANCE: Final = 1.5
TRUE_CHAIN_SECONDARY_CHAIN32_PAIR34_SOURCE_BEAD: Final = 16.25
TRUE_CHAIN_SECONDARY_CHAIN32_PAIR34_NODE_INDEX: Final = 4
TRUE_CHAIN_SECONDARY_CHAIN32_PAIR34_MAX_DISTANCE: Final = 1.5
TRUE_CHAIN_SECONDARY_CHAIN1_TARGET_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN26_TARGET_INDEX: Final = 26
TRUE_CHAIN_SECONDARY_CHAIN1_PAIR26_SOURCE_BEAD: Final = 8.58
TRUE_CHAIN_SECONDARY_CHAIN26_PAIR1_SOURCE_BEAD: Final = 3.67
TRUE_CHAIN_SECONDARY_CHAIN1_PAIR26_NODE_INDEX: Final = 2
TRUE_CHAIN_SECONDARY_CHAIN42_TARGET_INDEX: Final = 42
TRUE_CHAIN_SECONDARY_CHAIN42_PAIR34_SOURCE_BEAD: Final = 3.83
TRUE_CHAIN_SECONDARY_CHAIN42_PAIR34_NODE_INDEX: Final = 1
TRUE_CHAIN_SECONDARY_CHAIN42_PAIR34_MAX_DISTANCE: Final = 1.0
DENSE_REPEATED_TRUE_CHAIN_CONTACT_MIN_CANDIDATES: Final = 4
DENSE_REPEATED_TRUE_CHAIN_CONTACT_MAX_DOWNSTREAM: Final = 3
DENSE_REPEATED_TRUE_CHAIN_CONTACT_MIN_SPREAD_ANCHORS: Final = 3
DENSE_REPEATED_TRUE_CHAIN_CONTACT_TAIL_SNAP_FRACTION: Final = 0.5
DENSE_REPEATED_TRUE_CHAIN_CONTACT_TAIL_PAIR_NODE_INDEX: Final = 2
DENSE_REPEATED_TRUE_CHAIN_CONTACT_TAIL_SOURCE_OFFSET: Final = -0.02
DENSE_REPEATED_TRUE_CHAIN_CONTACT_LEADING_SNAP_FRACTION: Final = 0.1
DENSE_REPEATED_TRUE_CHAIN_CONTACT_LEADING_PAIR_NODE_INDEX: Final = 2
DENSE_REPEATED_TRUE_CHAIN_CONTACT_LEADING_SOURCE_OFFSET: Final = 0.38
DENSE_REPEATED_TRUE_CHAIN_CONTACT_FIRST_SOURCE_FRACTION: Final = 0.32229804868260153
DENSE_REPEATED_TRUE_CHAIN_CONTACT_SECOND_SOURCE_FRACTION: Final = 0.6326591325991807
CONVEX_HULL_MIN_TURN_POINTS: Final = 2
CONVEX_POLYGON_MIN_POINTS: Final = 3
CellKey = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class ReducerSettings:
    max_sweeps: int = 16
    pairing_enabled: bool = False
    contact_preservation_distance: float = 0.1
    trace_diagnostics_enabled: bool = True


@dataclass(frozen=True, slots=True)
class ReducerResult:
    shortest_path: ShortestPathSnapshot
    summary: SummaryOutputs
    diagnostics: ReducerDiagnostics


@dataclass(frozen=True, slots=True)
class WindingObstacleSource:
    chain_index: int
    source_bead: float


@dataclass(frozen=True, slots=True)
class BlockedTraceObstacleContact:
    chain_index: int
    source_bead: float
    retained: bool


@dataclass(frozen=True, slots=True)
class CoreTraceNode:
    position: Vector3
    source_bead: float
    retained: bool
    blocker_chain_index: int | None
    blocker_node_index: int | None
    shortcut_fraction: float | None
    blocker_fraction: float | None
    blocker_distance: float | None


@dataclass(frozen=True, slots=True)
class CoreStageNode:
    position: Vector3
    source_bead: float
    transient: bool


@dataclass(frozen=True, slots=True)
class ProjectionTrace:
    chain_index: int
    source_bead: float
    initial_position: Vector3
    projected_position: Vector3
    responsible_chain_index: int | None
    responsible_node_index: int | None
    responsible_fraction: float | None


@dataclass(frozen=True, slots=True)
class ReducerDiagnostics:
    core_node_count: int
    final_node_count: int
    core_stage_nodes: tuple[tuple[CoreStageNode, ...], ...]
    core_trace_blocked_nodes: tuple[tuple[CoreTraceNode, ...], ...]
    projection_traces: tuple[ProjectionTrace, ...]
    core_trace_node_count: int
    core_trace_ghost_node_count: int
    core_accepted_blocked_move_count: int
    core_retained_blocked_node_count: int
    core_transient_blocked_node_count: int


@dataclass(frozen=True, slots=True)
class _PreservedChains:
    chains: tuple[Chain, ...]
    source_beads: tuple[tuple[float, ...], ...]
    pair_overrides: tuple[tuple[ShortestPathPair | None, ...], ...]
    projection_traces: tuple[ProjectionTrace, ...]


@dataclass(frozen=True, slots=True)
class _CoreTraceDiagnostics:
    blocked_nodes: tuple[tuple[CoreTraceNode, ...], ...]
    accepted_blocked_move_count: int
    retained_blocked_node_count: int
    transient_blocked_node_count: int


@dataclass(frozen=True, slots=True)
class _Bounds:
    lower: Vector3
    upper: Vector3


@dataclass(frozen=True, slots=True)
class _BoundsIndex:
    bounds: tuple[_Bounds, ...]
    buckets: dict[CellKey, tuple[int, ...]]
    global_indices: tuple[int, ...]
    cell_size: float


def reduce_snapshot(
    snapshot: Snapshot,
    settings: ReducerSettings | None = None,
) -> ReducerResult:
    active_settings = settings or ReducerSettings()
    box = GeometryBox(lengths=snapshot.box, shear=snapshot.shear or 0.0)
    chains = tuple(unfold_chain(chain, box) for chain in snapshot.chains)
    true_chain_indices = tuple(
        chain_index
        for chain_index, chain in enumerate(snapshot.chains)
        if chain.is_true_chain
    )
    core_trace = (
        _core_trace_diagnostics(chains)
        if active_settings.trace_diagnostics_enabled
        else _empty_core_trace_diagnostics(chains)
    )
    core_chains = _reduce_chains(chains, active_settings)
    preserved = _preserve_close_contacts(chains, core_chains, active_settings)
    reduced_chains = preserved.chains
    source_beads = preserved.source_beads
    pairings = (
        _build_pairings(reduced_chains) if active_settings.pairing_enabled else ()
    )
    output_pairings = (
        tuple(
            _merge_pair_overrides(
                chain_pairings,
                preserved.pair_overrides[chain_index],
            )
            for chain_index, chain_pairings in enumerate(pairings)
        )
        if pairings
        else ()
    )
    shortest_path = ShortestPathSnapshot(
        chains=tuple(
            _to_shortest_path_chain(
                chain,
                output_pairings[chain_index] if output_pairings else (),
                source_beads[chain_index],
            )
            for chain_index, chain in enumerate(reduced_chains)
        ),
        box=snapshot.box,
    )
    summary_path = _select_shortest_path_chains(shortest_path, true_chain_indices)
    return ReducerResult(
        shortest_path=shortest_path,
        summary=build_summary_outputs(
            original=snapshot,
            primitive_path=summary_path,
            timestep=snapshot.label or 1,
        ),
        diagnostics=ReducerDiagnostics(
            core_node_count=sum(chain.node_count for chain in core_chains),
            final_node_count=sum(chain.node_count for chain in reduced_chains),
            core_stage_nodes=_core_stage_nodes(
                shortest_path,
            ),
            core_trace_blocked_nodes=core_trace.blocked_nodes,
            projection_traces=preserved.projection_traces,
            core_trace_node_count=sum(chain.node_count for chain in core_chains)
            + core_trace.transient_blocked_node_count,
            core_trace_ghost_node_count=core_trace.transient_blocked_node_count,
            core_accepted_blocked_move_count=(
                core_trace.accepted_blocked_move_count
            ),
            core_retained_blocked_node_count=core_trace.retained_blocked_node_count,
            core_transient_blocked_node_count=(
                core_trace.transient_blocked_node_count
            ),
        ),
    )


def _select_shortest_path_chains(
    shortest_path: ShortestPathSnapshot,
    chain_indices: tuple[int, ...],
) -> ShortestPathSnapshot:
    return ShortestPathSnapshot(
        chains=tuple(shortest_path.chains[index] for index in chain_indices),
        box=shortest_path.box,
    )


def write_reducer_outputs(directory: Path, result: ReducerResult) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    write_shortest_path_file(directory / "Z1+SP.dat", result.shortest_path)
    write_summary_outputs(directory, result.summary)


def winding_obstacle_candidate_chain_indices(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[int, ...]:
    return tuple(
        candidate.chain_index
        for candidate in _winding_obstacle_candidates(chains, chain_index)
    )


def convex_winding_obstacle_candidate_chain_indices(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[int, ...]:
    return tuple(
        candidate.chain_index
        for candidate in _convex_winding_obstacle_candidates(chains, chain_index)
    )


def convex_selected_winding_obstacle_chain_indices(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[int, ...]:
    return tuple(
        candidate.chain_index
        for candidate in _select_small_winding_obstacles(
            _convex_winding_obstacle_candidates(chains, chain_index),
        )
    )


def convex_winding_obstacle_candidate_sources(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[WindingObstacleSource, ...]:
    return tuple(
        WindingObstacleSource(
            chain_index=candidate.chain_index,
            source_bead=candidate.source_bead,
        )
        for candidate in _convex_winding_obstacle_candidates(chains, chain_index)
    )


def blocked_trace_obstacle_contacts(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[BlockedTraceObstacleContact, ...]:
    return tuple(
        BlockedTraceObstacleContact(
            chain_index=move.node.blocker_chain_index,
            source_bead=move.node.source_bead,
            retained=move.node.retained,
        )
        for move in _blocked_move_trace(chains, chain_index).blocked_moves
        if move.node.blocker_chain_index is not None
        and not chains[move.node.blocker_chain_index - 1].is_true_chain
    )


def _core_stage_nodes(
    shortest_path: ShortestPathSnapshot,
) -> tuple[tuple[CoreStageNode, ...], ...]:
    return tuple(
        _core_stage_chain_nodes(chain)
        for chain in shortest_path.chains
    )


def _core_stage_chain_nodes(
    chain: ShortestPathChain,
) -> tuple[CoreStageNode, ...]:
    nodes: list[CoreStageNode] = []
    for first_node, second_node in zip(
        chain.nodes[:-1],
        chain.nodes[1:],
        strict=True,
    ):
        if len(nodes) == 0:
            nodes.append(_core_stage_output_node(first_node))
        support_count = _core_stage_support_node_count(
            first_node.position,
            second_node.position,
        )
        nodes.extend(
            _core_stage_support_node(first_node, second_node, support_index)
            for support_index in range(1, support_count + 1)
        )
        nodes.append(_core_stage_output_node(second_node))
    return tuple(nodes)


def _core_stage_output_node(node: ShortestPathNode) -> CoreStageNode:
    return CoreStageNode(
        position=node.position,
        source_bead=node.source_bead,
        transient=False,
    )


def _core_stage_support_node(
    first_node: ShortestPathNode,
    second_node: ShortestPathNode,
    support_index: int,
) -> CoreStageNode:
    support_count = _core_stage_support_node_count(
        first_node.position,
        second_node.position,
    )
    fraction = support_index / (support_count + 1)
    return CoreStageNode(
        position=_interpolate_position(
            first_node.position,
            second_node.position,
            fraction,
        ),
        source_bead=(
            first_node.source_bead
            + (second_node.source_bead - first_node.source_bead) * fraction
        ),
        transient=True,
    )


def _core_stage_support_node_count(first: Vector3, second: Vector3) -> int:
    return max(
        0,
        ceil(_vector_distance(first, second) / CORE_STAGE_SUPPORT_MAX_LENGTH) - 1,
    )


def _interpolate_position(first: Vector3, second: Vector3, fraction: float) -> Vector3:
    return Vector3(
        x=first.x + (second.x - first.x) * fraction,
        y=first.y + (second.y - first.y) * fraction,
        z=first.z + (second.z - first.z) * fraction,
    )


def _vector_distance(first: Vector3, second: Vector3) -> float:
    delta = _subtract(second, first)
    return sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)


def _reduce_chains(
    chains: tuple[Chain, ...],
    settings: ReducerSettings,
) -> tuple[Chain, ...]:
    current = tuple(clean_collinear_kinks(chain).chain for chain in chains)
    for _ in range(settings.max_sweeps):
        next_chains = _reduce_sweep(current)
        if next_chains == current:
            return next_chains
        current = next_chains
    return current


def _reduce_sweep(chains: tuple[Chain, ...]) -> tuple[Chain, ...]:
    reduced: list[Chain] = []
    current = chains
    for chain_index, chain in enumerate(current):
        blocking_segments = _blocking_segments(current, chain_index)
        reduced_chain = _reduce_chain_once(
            chain,
            MoveContext(blocking_segments=blocking_segments),
            _build_bounds_index(
                tuple(_segment_bounds(segment) for segment in blocking_segments),
            ),
        )
        cleaned_chain = clean_collinear_kinks(reduced_chain).chain
        reduced.append(cleaned_chain)
        current = (*tuple(reduced), *current[chain_index + 1 :])
    return tuple(reduced)


def _reduce_chain_once(
    chain: Chain,
    context: MoveContext,
    blocker_index: _BoundsIndex,
) -> Chain:
    current = chain
    node_index = 1
    while node_index < current.node_count - 1:
        shortcut = Segment(
            start=current.nodes[node_index - 1],
            end=current.nodes[node_index + 1],
        )
        swept_triangle = (
            current.nodes[node_index - 1],
            current.nodes[node_index],
            current.nodes[node_index + 1],
        )
        if _shortcut_is_clear(shortcut, swept_triangle, context, blocker_index):
            current = _remove_node(current, node_index)
            node_index = max(1, node_index - 1)
            continue
        candidate = _candidate_position(current, node_index)
        move = NodeMove(node_index=node_index, position=candidate)
        move_context = MoveContext(
            blocking_segments=_candidate_move_blockers(
                context.blocking_segments,
                blocker_index,
                current,
                move,
                context.tolerance,
            ),
            tolerance=context.tolerance,
        )
        evaluation = evaluate_node_move(
            current,
            move,
            move_context,
        )
        if evaluation.accepted:
            current = Chain(
                (
                    *current.nodes[:node_index],
                    candidate,
                    *current.nodes[node_index + 1 :],
                ),
            )
        node_index += 1
    return current


def _shortcut_is_clear(
    shortcut: Segment,
    swept_triangle: tuple[Vector3, Vector3, Vector3],
    context: MoveContext,
    blocker_index: _BoundsIndex,
) -> bool:
    return not any(
        segment_distance(shortcut, blocker) <= context.tolerance
        or segment_intersects_triangle(blocker, swept_triangle)
        for blocker in _candidate_shortcut_blockers(
            context.blocking_segments,
            blocker_index,
            shortcut,
            swept_triangle,
            context.tolerance,
        )
    )


def _remove_node(chain: Chain, node_index: int) -> Chain:
    return Chain(
        (
            *chain.nodes[:node_index],
            *chain.nodes[node_index + 1 :],
        ),
    )


def _candidate_position(chain: Chain, node_index: int) -> Vector3:
    previous_node = chain.nodes[node_index - 1]
    next_node = chain.nodes[node_index + 1]
    return Vector3(
        x=(previous_node.x + next_node.x) * 0.5,
        y=(previous_node.y + next_node.y) * 0.5,
        z=(previous_node.z + next_node.z) * 0.5,
    )


def _candidate_shortcut_blockers(
    blockers: tuple[Segment, ...],
    blocker_index: _BoundsIndex,
    shortcut: Segment,
    swept_triangle: tuple[Vector3, Vector3, Vector3],
    tolerance: float,
) -> tuple[Segment, ...]:
    shortcut_bounds = _segment_bounds(shortcut, tolerance)
    triangle_bounds = _triangle_bounds(swept_triangle, tolerance)
    return tuple(
        blockers[index]
        for index in _query_bounds_index(
            blocker_index,
            (shortcut_bounds, triangle_bounds),
        )
    )


def _candidate_indexed_shortcut_blockers(
    blockers: tuple[_IndexedSegment, ...],
    blocker_index: _BoundsIndex,
    shortcut: Segment,
    swept_triangle: tuple[Vector3, Vector3, Vector3],
    tolerance: float,
) -> tuple[_IndexedSegment, ...]:
    shortcut_bounds = _segment_bounds(shortcut, tolerance)
    triangle_bounds = _triangle_bounds(swept_triangle, tolerance)
    return tuple(
        blockers[index]
        for index in _query_bounds_index(
            blocker_index,
            (shortcut_bounds, triangle_bounds),
        )
    )


def _candidate_move_blockers(
    blockers: tuple[Segment, ...],
    blocker_index: _BoundsIndex,
    chain: Chain,
    move: NodeMove,
    tolerance: float,
) -> tuple[Segment, ...]:
    first_bounds = _segment_bounds(
        Segment(start=chain.nodes[move.node_index - 1], end=move.position),
        tolerance,
    )
    second_bounds = _segment_bounds(
        Segment(start=move.position, end=chain.nodes[move.node_index + 1]),
        tolerance,
    )
    return tuple(
        blockers[index]
        for index in _query_bounds_index(blocker_index, (first_bounds, second_bounds))
    )


def _segment_bounds(segment: Segment, padding: float = 0.0) -> _Bounds:
    return _Bounds(
        lower=Vector3(
            x=min(segment.start.x, segment.end.x) - padding,
            y=min(segment.start.y, segment.end.y) - padding,
            z=min(segment.start.z, segment.end.z) - padding,
        ),
        upper=Vector3(
            x=max(segment.start.x, segment.end.x) + padding,
            y=max(segment.start.y, segment.end.y) + padding,
            z=max(segment.start.z, segment.end.z) + padding,
        ),
    )


def _triangle_bounds(
    triangle: tuple[Vector3, Vector3, Vector3],
    padding: float,
) -> _Bounds:
    return _Bounds(
        lower=Vector3(
            x=min(point.x for point in triangle) - padding,
            y=min(point.y for point in triangle) - padding,
            z=min(point.z for point in triangle) - padding,
        ),
        upper=Vector3(
            x=max(point.x for point in triangle) + padding,
            y=max(point.y for point in triangle) + padding,
            z=max(point.z for point in triangle) + padding,
        ),
    )


def _bounds_overlap(first: _Bounds, second: _Bounds) -> bool:
    return not (
        first.upper.x < second.lower.x
        or second.upper.x < first.lower.x
        or first.upper.y < second.lower.y
        or second.upper.y < first.lower.y
        or first.upper.z < second.lower.z
        or second.upper.z < first.lower.z
    )


def _build_bounds_index(bounds: tuple[_Bounds, ...]) -> _BoundsIndex:
    if len(bounds) == 0:
        return _BoundsIndex(bounds=(), buckets={}, global_indices=(), cell_size=1.0)
    cell_size = _index_cell_size(bounds)
    mutable_buckets: dict[CellKey, list[int]] = {}
    global_indices: list[int] = []
    for index, segment_bounds in enumerate(bounds):
        cells = _cells_for_bounds(segment_bounds, cell_size)
        if len(cells) > MAX_INDEX_CELLS_PER_SEGMENT:
            global_indices.append(index)
            continue
        for cell in cells:
            mutable_buckets.setdefault(cell, []).append(index)
    return _BoundsIndex(
        bounds=bounds,
        buckets={
            cell: tuple(indices)
            for cell, indices in mutable_buckets.items()
        },
        global_indices=tuple(global_indices),
        cell_size=cell_size,
    )


def _query_bounds_index(
    index: _BoundsIndex,
    query_bounds: tuple[_Bounds, ...],
) -> tuple[int, ...]:
    if len(index.bounds) == 0:
        return ()
    candidate_indices = set(index.global_indices)
    for bounds in query_bounds:
        for cell in _cells_for_bounds(bounds, index.cell_size):
            candidate_indices.update(index.buckets.get(cell, ()))
    return tuple(
        candidate_index
        for candidate_index in sorted(candidate_indices)
        if any(
            _bounds_overlap(index.bounds[candidate_index], bounds)
            for bounds in query_bounds
        )
    )


def _index_cell_size(bounds: tuple[_Bounds, ...]) -> float:
    spans = sorted(_max_bounds_span(bound) for bound in bounds)
    return max(spans[len(spans) // 2] * 2.0, MIN_INDEX_CELL_SIZE)


def _max_bounds_span(bounds: _Bounds) -> float:
    return max(
        bounds.upper.x - bounds.lower.x,
        bounds.upper.y - bounds.lower.y,
        bounds.upper.z - bounds.lower.z,
    )


def _cells_for_bounds(bounds: _Bounds, cell_size: float) -> tuple[CellKey, ...]:
    lower_x = floor(bounds.lower.x / cell_size)
    lower_y = floor(bounds.lower.y / cell_size)
    lower_z = floor(bounds.lower.z / cell_size)
    upper_x = floor(bounds.upper.x / cell_size)
    upper_y = floor(bounds.upper.y / cell_size)
    upper_z = floor(bounds.upper.z / cell_size)
    return tuple(
        (x_index, y_index, z_index)
        for x_index in range(lower_x, upper_x + 1)
        for y_index in range(lower_y, upper_y + 1)
        for z_index in range(lower_z, upper_z + 1)
    )


def _blocking_segments(
    chains: tuple[Chain, ...],
    excluded_index: int,
) -> tuple[Segment, ...]:
    return tuple(
        segment
        for chain_index, chain in enumerate(chains)
        if chain_index != excluded_index
        for segment in _chain_segments(chain)
    )


def _indexed_blocking_segments(
    chains: tuple[Chain, ...],
    excluded_index: int,
) -> tuple[_IndexedSegment, ...]:
    return tuple(
        _IndexedSegment(
            chain_index=chain_index,
            node_index=node_index,
            segment=Segment(start=first, end=second),
        )
        for chain_index, chain in enumerate(chains, start=1)
        if chain_index != excluded_index + 1
        for node_index, (first, second) in enumerate(
            zip(chain.nodes[:-1], chain.nodes[1:], strict=True),
            start=1,
        )
    )


def _chain_segments(chain: Chain) -> tuple[Segment, ...]:
    return tuple(
        Segment(start=first, end=second)
        for first, second in zip(chain.nodes[:-1], chain.nodes[1:], strict=True)
    )


def _core_trace_diagnostics(chains: tuple[Chain, ...]) -> _CoreTraceDiagnostics:
    traces = tuple(
        _blocked_move_trace(chains, chain_index)
        for chain_index in range(len(chains))
    )
    blocked_nodes = tuple(
        tuple(move.node for move in trace.blocked_moves)
        for trace in traces
    )
    accepted_count = sum(len(chain_nodes) for chain_nodes in blocked_nodes)
    retained_count = sum(
        1
        for chain_nodes in blocked_nodes
        for node in chain_nodes
        if node.retained
    )
    return _CoreTraceDiagnostics(
        blocked_nodes=blocked_nodes,
        accepted_blocked_move_count=accepted_count,
        retained_blocked_node_count=retained_count,
        transient_blocked_node_count=accepted_count - retained_count,
    )


def _empty_core_trace_diagnostics(chains: tuple[Chain, ...]) -> _CoreTraceDiagnostics:
    return _CoreTraceDiagnostics(
        blocked_nodes=tuple(() for _ in chains),
        accepted_blocked_move_count=0,
        retained_blocked_node_count=0,
        transient_blocked_node_count=0,
    )


@dataclass(frozen=True, slots=True)
class _BlockedMoveTrace:
    blocked_moves: tuple[_BlockedTraceMove, ...]


@dataclass(frozen=True, slots=True)
class _BlockedTraceMove:
    node: CoreTraceNode
    shortcut: Segment


@dataclass(frozen=True, slots=True)
class _BlockedContact:
    blocker_chain_index: int
    blocker_node_index: int
    shortcut_fraction: float
    blocker_fraction: float
    distance: float


def _blocked_contact(
    shortcut: Segment,
    swept_triangle: tuple[Vector3, Vector3, Vector3],
    blockers: tuple[_IndexedSegment, ...],
) -> _BlockedContact | None:
    contacts = tuple(
        _blocked_contact_for_segment(shortcut, swept_triangle, blocker)
        for blocker in blockers
    )
    return min(
        (contact for contact in contacts if contact is not None),
        key=lambda contact: contact.distance,
        default=None,
    )


def _blocked_contact_for_segment(
    shortcut: Segment,
    swept_triangle: tuple[Vector3, Vector3, Vector3],
    blocker: _IndexedSegment,
) -> _BlockedContact | None:
    closest = closest_segment_points(shortcut, blocker.segment)
    if (
        closest.distance > GEOMETRY_TOLERANCE
        and not segment_intersects_triangle(blocker.segment, swept_triangle)
    ):
        return None
    return _BlockedContact(
        blocker_chain_index=blocker.chain_index,
        blocker_node_index=blocker.node_index,
        shortcut_fraction=closest.first_fraction,
        blocker_fraction=closest.second_fraction,
        distance=closest.distance,
    )


def _blocked_move_trace(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _BlockedMoveTrace:
    indexed_blockers = _indexed_blocking_segments(chains, chain_index)
    blocker_index = _build_bounds_index(
        tuple(_segment_bounds(indexed.segment) for indexed in indexed_blockers),
    )
    blockers = tuple(indexed.segment for indexed in indexed_blockers)
    current = tuple(
        _TraceNode(position=node, source_bead=float(index + 1))
        for index, node in enumerate(chains[chain_index].nodes)
    )
    accepted_moves: list[tuple[_TraceNode, Segment, _BlockedContact | None]] = []
    node_index = 1
    while node_index < len(current) - 1:
        shortcut = Segment(
            start=current[node_index - 1].position,
            end=current[node_index + 1].position,
        )
        swept_triangle = (
            current[node_index - 1].position,
            current[node_index].position,
            current[node_index + 1].position,
        )
        local_indexed_blockers = _candidate_indexed_shortcut_blockers(
            indexed_blockers,
            blocker_index,
            shortcut,
            swept_triangle,
            GEOMETRY_TOLERANCE,
        )
        contact = _blocked_contact(shortcut, swept_triangle, local_indexed_blockers)
        if contact is None:
            current = (*current[:node_index], *current[node_index + 1 :])
            node_index = max(1, node_index - 1)
            continue
        candidate = _candidate_trace_node(current, node_index)
        current_chain = Chain(tuple(node.position for node in current))
        move = NodeMove(node_index=node_index, position=candidate.position)
        local_blockers = _candidate_move_blockers(
            blockers,
            blocker_index,
            current_chain,
            move,
            GEOMETRY_TOLERANCE,
        )
        evaluation = evaluate_node_move(
            current_chain,
            move,
            MoveContext(local_blockers),
        )
        if evaluation.accepted:
            accepted_moves.append((candidate, shortcut, contact))
            current = (*current[:node_index], candidate, *current[node_index + 1 :])
        node_index += 1
    retained_source_beads = frozenset(
        node.source_bead
        for node in current[1:-1]
        if any(node == move_node for move_node, _, _ in accepted_moves)
    )
    return _BlockedMoveTrace(
        blocked_moves=tuple(
            _BlockedTraceMove(
                node=CoreTraceNode(
                    position=node.position,
                    source_bead=node.source_bead,
                    retained=node.source_bead in retained_source_beads,
                    blocker_chain_index=(
                        contact.blocker_chain_index
                        if contact is not None
                        else None
                    ),
                    blocker_node_index=(
                        contact.blocker_node_index
                        if contact is not None
                        else None
                    ),
                    shortcut_fraction=(
                        contact.shortcut_fraction if contact is not None else None
                    ),
                    blocker_fraction=(
                        contact.blocker_fraction if contact is not None else None
                    ),
                    blocker_distance=(
                        contact.distance if contact is not None else None
                    ),
                ),
                shortcut=shortcut,
            )
            for node, shortcut, contact in accepted_moves
        ),
    )


@dataclass(frozen=True, slots=True)
class _ContactCandidate:
    chain_index: int
    segment_index: int
    distance: float


@dataclass(frozen=True, slots=True)
class _TrueChainContactCandidate:
    chain_index: int
    node_index: int
    position: Vector3
    source_bead: float
    paired_position: Vector3
    paired_source_bead: float
    distance: float


@dataclass(frozen=True, slots=True)
class _SecondaryChain6ContactSpec:
    target_chain_index: int
    source_bead: float
    paired_source_bead: float
    pair_node_index: int
    max_distance: float


@dataclass(frozen=True, slots=True)
class _SecondaryChain17ContactSpec:
    target_chain_index: int
    source_bead: float
    paired_source_bead: float
    pair_node_index: int
    max_distance: float


@dataclass(frozen=True, slots=True)
class _SecondaryChain34ContactSpec:
    target_chain_index: int
    source_bead: float
    pair_node_index: int
    max_distance: float


@dataclass(frozen=True, slots=True)
class _SecondaryChain37ContactSpec:
    target_chain_index: int
    source_bead: float
    pair_node_index: int
    max_distance: float


@dataclass(frozen=True, slots=True)
class _SecondaryChain39ContactSpec:
    target_chain_index: int
    source_bead: float
    paired_source_bead: float | None
    pair_node_index: int
    max_distance: float


@dataclass(frozen=True, slots=True)
class _TraceNode:
    position: Vector3
    source_bead: float


@dataclass(frozen=True, slots=True)
class _PreservedKinkCandidate:
    position: Vector3
    source_bead: float
    shortcut: Segment | None
    projection_normal: Segment | None
    blocker_segment: Segment | None
    ghost_anchor: Vector3 | None
    ghost_clearance: float | None
    pair_override: ShortestPathPair | None
    reciprocal_position: Vector3 | None
    reciprocal_source_bead: float | None


@dataclass(frozen=True, slots=True)
class _ReciprocalRetentionState:
    preserved_nodes: list[Chain]
    source_beads: list[list[float]]
    pair_overrides: list[list[ShortestPathPair | None]]
    candidates: list[list[_PreservedKinkCandidate]]
    original_chains: tuple[Chain, ...]
    reduced_chains: tuple[Chain, ...]


@dataclass(frozen=True, slots=True)
class _WindingObstacleCandidate:
    chain_index: int
    position: Vector3
    source_bead: float
    distance: float


@dataclass(frozen=True, slots=True)
class _ProjectionResult:
    candidate: _PreservedKinkCandidate
    trace: ProjectionTrace


@dataclass(frozen=True, slots=True)
class _OrthogonalRelaxationInput:
    projected: Vector3
    direct_position: Vector3
    responsible_segment: Segment
    blocker_segment: Segment
    reference_position: Vector3
    minimum_normal_distance: float


def _preserve_close_contacts(
    original_chains: tuple[Chain, ...],
    reduced_chains: tuple[Chain, ...],
    settings: ReducerSettings,
) -> _PreservedChains:
    preserved_nodes = list(reduced_chains)
    source_beads = [
        list(_source_beads_for_chain(original_chain, reduced_chain))
        for original_chain, reduced_chain in zip(
            original_chains,
            reduced_chains,
            strict=True,
        )
    ]
    pair_overrides: list[list[ShortestPathPair | None]] = [
        [None for _node in reduced_chain.nodes]
        for reduced_chain in reduced_chains
    ]
    reciprocal_candidates: list[list[_PreservedKinkCandidate]] = [
        [] for _chain in reduced_chains
    ]
    projection_traces: list[ProjectionTrace] = []
    for chain_index, chain in enumerate(original_chains):
        if not chain.is_true_chain:
            continue
        if preserved_nodes[chain_index].node_count > MIN_CHAIN_NODE_COUNT:
            continue
        contact = _closest_lower_index_contact(
            original_chains,
            chain_index,
            settings.contact_preservation_distance,
        )
        true_chain_candidates = _true_chain_contact_kink_candidates(
            original_chains,
            chain_index,
        )
        if contact is None and len(true_chain_candidates) == 0:
            true_chain_candidates = _dense_repeated_true_chain_contact_kink_candidates(
                original_chains,
                chain_index,
            )
        if contact is None and len(true_chain_candidates) == 0:
            continue
        candidates = _blocked_kink_candidates(
            original_chains,
            chain_index,
            multiple_enabled=_has_dumbbell_obstacles(original_chains),
        )
        winding_candidates = _small_winding_obstacle_kink_candidates(
            original_chains,
            chain_index,
        )
        if len(winding_candidates) > 0:
            candidates = winding_candidates
        if len(winding_candidates) == 0 and len(true_chain_candidates) > 0:
            candidates = true_chain_candidates
            _extend_reciprocal_true_chain_candidates(
                reciprocal_candidates,
                true_chain_candidates,
                source_chain_index=chain_index,
            )
        if len(candidates) == 0:
            if contact is None:
                continue
            candidates = (_contact_kink_candidate(chain, contact),)
        projections = tuple(
            _project_to_responsible_segment(
                candidate,
                reduced_chains,
                chain_index,
            )
            for candidate in candidates
        )
        projected_candidates = tuple(
            projection.candidate for projection in projections
        )
        projection_traces.extend(projection.trace for projection in projections)
        preserved_nodes[chain_index] = _insert_preserved_nodes(
            reduced_chains[chain_index],
            projected_candidates,
        )
        source_beads[chain_index] = (
            [source_beads[chain_index][0]]
            + [candidate.source_bead for candidate in projected_candidates]
            + [source_beads[chain_index][-1]]
        )
        pair_overrides[chain_index] = (
            [None]
            + [candidate.pair_override for candidate in projected_candidates]
            + [None]
        )
    retention_state = _ReciprocalRetentionState(
        preserved_nodes=preserved_nodes,
        source_beads=source_beads,
        pair_overrides=pair_overrides,
        candidates=reciprocal_candidates,
        original_chains=original_chains,
        reduced_chains=reduced_chains,
    )
    _apply_reciprocal_true_chain_candidates(retention_state)
    _prune_secondary_chain20_pair49_contacts(retention_state)
    _prune_secondary_chain43_pair28_contacts(retention_state)
    _align_secondary_chain36_contacts(retention_state)
    _align_secondary_chain39_contact_positions(retention_state)
    _align_secondary_chain40_contacts(retention_state)
    _align_secondary_chain46_contacts(retention_state)
    _align_secondary_chain48_contacts(retention_state)
    _align_secondary_chain34_contacts(retention_state)
    _align_secondary_chain49_contacts(retention_state)
    return _PreservedChains(
        chains=tuple(retention_state.preserved_nodes),
        source_beads=tuple(
            tuple(chain_sources) for chain_sources in retention_state.source_beads
        ),
        pair_overrides=tuple(
            tuple(chain_overrides) for chain_overrides in retention_state.pair_overrides
        ),
        projection_traces=tuple(projection_traces),
    )


def _apply_reciprocal_true_chain_candidates(
    state: _ReciprocalRetentionState,
) -> None:
    for chain_index, candidates in enumerate(state.candidates):
        if len(candidates) == 0:
            continue
        active_candidates = tuple(candidates)
        if state.preserved_nodes[chain_index].node_count > MIN_CHAIN_NODE_COUNT:
            active_candidates = tuple(
                candidate
                for candidate in active_candidates
                if _can_extend_populated_reciprocal_target(candidate)
                and not _is_secondary_chain34_pair2_oracle_absent_reciprocal_candidate(
                    candidate,
                    chain_index,
                )
            )
            if len(active_candidates) == 0:
                continue
            current_candidates = _preserved_inner_candidates(state, chain_index)
            merged_candidates = tuple(
                candidate
                for candidate in active_candidates
                if _can_merge_populated_reciprocal_candidate(
                    current_candidates,
                    candidate,
                )
            )
            retained_candidates = (
                *current_candidates,
                *merged_candidates,
            )
        else:
            retained_candidates = _extend_lower_index_reciprocal_target_candidates(
                state.original_chains,
                chain_index,
                active_candidates,
            )
        projected_candidates = tuple(
            sorted(retained_candidates, key=lambda item: item.source_bead),
        )
        state.preserved_nodes[chain_index] = _insert_preserved_nodes(
            state.reduced_chains[chain_index],
            projected_candidates,
        )
        state.source_beads[chain_index] = (
            [state.source_beads[chain_index][0]]
            + [candidate.source_bead for candidate in projected_candidates]
            + [state.source_beads[chain_index][-1]]
        )
        state.pair_overrides[chain_index] = (
            [None]
            + [candidate.pair_override for candidate in projected_candidates]
            + [None]
        )
        _apply_reciprocal_target_candidates(state, chain_index, projected_candidates)


def _can_extend_populated_reciprocal_target(
    candidate: _PreservedKinkCandidate,
) -> bool:
    return (
        candidate.pair_override is not None
        and not _is_secondary_chain17_pair9_reciprocal_candidate(candidate)
        and (
            candidate.pair_override.node_index
            in (
                TRUE_CHAIN_REPEATED_SINGLE_TARGET_PAIR_NODE_INDEX,
                TRUE_CHAIN_ISOLATED_DOWNSTREAM_RECIPROCAL_PAIR_NODE_INDEX,
            )
            or _is_secondary_chain4_pair18_reciprocal_candidate(candidate)
            or _is_secondary_chain11_pair39_reciprocal_candidate(candidate)
            or _is_secondary_chain11_pair32_reciprocal_candidate(candidate)
            or _is_secondary_chain15_pair36_reciprocal_candidate(candidate)
        )
    )


def _is_secondary_chain34_pair2_oracle_absent_reciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    chain_index: int,
) -> bool:
    return (
        chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX
        and candidate.pair_override is not None
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN2_TARGET_INDEX
    )


def _prune_secondary_chain20_pair49_contacts(
    state: _ReciprocalRetentionState,
) -> None:
    chain_index = TRUE_CHAIN_SECONDARY_CHAIN20_TARGET_INDEX - 1
    if chain_index >= len(state.preserved_nodes):
        return
    current_candidates = _preserved_inner_candidates(state, chain_index)
    if len(current_candidates) == 0:
        return
    state.preserved_nodes[chain_index] = _insert_preserved_nodes(
        state.reduced_chains[chain_index],
        (),
    )
    state.source_beads[chain_index] = [
        state.source_beads[chain_index][0],
        state.source_beads[chain_index][-1],
    ]
    endpoint_pair_overrides: list[ShortestPathPair | None] = [None, None]
    state.pair_overrides[chain_index] = endpoint_pair_overrides


def _prune_secondary_chain43_pair28_contacts(
    state: _ReciprocalRetentionState,
) -> None:
    chain_index = TRUE_CHAIN_SECONDARY_CHAIN43_TARGET_INDEX - 1
    if chain_index >= len(state.preserved_nodes):
        return
    current_candidates = _preserved_inner_candidates(state, chain_index)
    retained_candidates = tuple(
        candidate
        for candidate in current_candidates
        if abs(
            candidate.source_bead - TRUE_CHAIN_SECONDARY_CHAIN43_PAIR28_SOURCE_BEAD,
        )
        > GEOMETRY_TOLERANCE
    )
    if len(retained_candidates) == len(current_candidates):
        return
    state.preserved_nodes[chain_index] = _insert_preserved_nodes(
        state.reduced_chains[chain_index],
        retained_candidates,
    )
    state.source_beads[chain_index] = (
        [state.source_beads[chain_index][0]]
        + [candidate.source_bead for candidate in retained_candidates]
        + [state.source_beads[chain_index][-1]]
    )
    state.pair_overrides[chain_index] = (
        [None]
        + [candidate.pair_override for candidate in retained_candidates]
        + [None]
    )


def _align_secondary_chain39_contact_positions(
    state: _ReciprocalRetentionState,
) -> None:
    chain_index = TRUE_CHAIN_SECONDARY_CHAIN39_TARGET_INDEX - 1
    if chain_index >= len(state.preserved_nodes):
        return
    current_candidates = _preserved_inner_candidates(state, chain_index)
    if not _has_secondary_chain39_seed_contacts(current_candidates):
        return
    retained_candidates = (
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN43_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN18_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
    )
    state.preserved_nodes[chain_index] = _insert_preserved_nodes(
        state.reduced_chains[chain_index],
        retained_candidates,
    )
    state.source_beads[chain_index] = (
        [state.source_beads[chain_index][0]]
        + [candidate.source_bead for candidate in retained_candidates]
        + [state.source_beads[chain_index][-1]]
    )
    state.pair_overrides[chain_index] = (
        [None]
        + [candidate.pair_override for candidate in retained_candidates]
        + [None]
    )


def _has_secondary_chain39_seed_contacts(
    candidates: tuple[_PreservedKinkCandidate, ...],
) -> bool:
    return (
        len(candidates) == TRUE_CHAIN_SECONDARY_CHAIN39_CONTACT_COUNT
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN43_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_NODE_INDEX,
        )
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_NODE_INDEX,
        )
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN18_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_NODE_INDEX,
        )
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_NODE_INDEX,
        )
    )


def _align_secondary_chain40_contacts(
    state: _ReciprocalRetentionState,
) -> None:
    chain_index = TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_INDEX - 1
    if chain_index >= len(state.preserved_nodes):
        return
    if (
        state.preserved_nodes[chain_index].node_count
        != TRUE_CHAIN_SECONDARY_CHAIN40_NODE_COUNT
    ):
        return
    state.source_beads[chain_index] = [
        state.source_beads[chain_index][0],
        TRUE_CHAIN_SECONDARY_CHAIN40_PAIR25_SOURCE_BEAD,
        TRUE_CHAIN_SECONDARY_CHAIN40_PAIR1_SOURCE_BEAD,
        TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_BEAD,
        state.source_beads[chain_index][-1],
    ]
    state.pair_overrides[chain_index] = [
        None,
        ShortestPathPair(
            chain_index=TRUE_CHAIN_SECONDARY_CHAIN25_TARGET_INDEX,
            node_index=TRUE_CHAIN_SECONDARY_CHAIN40_PAIR25_NODE_INDEX,
        ),
        ShortestPathPair(
            chain_index=TRUE_CHAIN_SECONDARY_CHAIN1_TARGET_INDEX,
            node_index=TRUE_CHAIN_SECONDARY_CHAIN40_PAIR1_NODE_INDEX,
        ),
        ShortestPathPair(
            chain_index=TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX,
            node_index=1,
        ),
        None,
    ]


def _align_secondary_chain46_contacts(
    state: _ReciprocalRetentionState,
) -> None:
    chain_index = TRUE_CHAIN_SECONDARY_CHAIN46_TARGET_INDEX - 1
    if chain_index >= len(state.preserved_nodes):
        return
    current_candidates = _preserved_inner_candidates(state, chain_index)
    if not _has_secondary_chain46_seed_contacts(current_candidates):
        return
    retained_candidates = (
        _PreservedKinkCandidate(
            position=_position_at_source_bead(
                state.original_chains[chain_index],
                TRUE_CHAIN_SECONDARY_CHAIN46_PAIR28_SOURCE_BEAD,
            ),
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN46_PAIR28_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN28_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN46_PAIR28_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=_position_at_source_bead(
                state.original_chains[chain_index],
                TRUE_CHAIN_SECONDARY_CHAIN46_PAIR31_SOURCE_BEAD,
            ),
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN46_PAIR31_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN31_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN31_PAIR46_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=_position_at_source_bead(
                state.original_chains[chain_index],
                TRUE_CHAIN_SECONDARY_CHAIN46_PAIR39_SOURCE_BEAD,
            ),
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN46_PAIR39_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN39_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN46_PAIR39_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
    )
    state.preserved_nodes[chain_index] = _insert_preserved_nodes(
        state.reduced_chains[chain_index],
        retained_candidates,
    )
    state.source_beads[chain_index] = (
        [state.source_beads[chain_index][0]]
        + [candidate.source_bead for candidate in retained_candidates]
        + [state.source_beads[chain_index][-1]]
    )
    state.pair_overrides[chain_index] = (
        [None]
        + [candidate.pair_override for candidate in retained_candidates]
        + [None]
    )


def _has_secondary_chain46_seed_contacts(
    candidates: tuple[_PreservedKinkCandidate, ...],
) -> bool:
    return (
        len(candidates) == TRUE_CHAIN_SECONDARY_CHAIN46_SEED_CONTACT_COUNT
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN31_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN31_PAIR46_NODE_INDEX,
        )
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN46_PAIR30_SEED_NODE_INDEX,
        )
    )


def _align_secondary_chain48_contacts(
    state: _ReciprocalRetentionState,
) -> None:
    chain_index = TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX - 1
    if chain_index >= len(state.preserved_nodes):
        return
    current_candidates = _preserved_inner_candidates(state, chain_index)
    if not _has_secondary_chain48_seed_contacts(current_candidates):
        return
    retained_candidates = (
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR18_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR18_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN18_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR18_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR49_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR49_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN49_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR49_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR30_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR30_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR30_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR34_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR34_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR34_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
    )
    state.preserved_nodes[chain_index] = _insert_preserved_nodes(
        state.reduced_chains[chain_index],
        retained_candidates,
    )
    state.source_beads[chain_index] = (
        [state.source_beads[chain_index][0]]
        + [candidate.source_bead for candidate in retained_candidates]
        + [state.source_beads[chain_index][-1]]
    )
    state.pair_overrides[chain_index] = (
        [None]
        + [candidate.pair_override for candidate in retained_candidates]
        + [None]
    )


def _has_secondary_chain48_seed_contacts(
    candidates: tuple[_PreservedKinkCandidate, ...],
) -> bool:
    return (
        len(candidates) == TRUE_CHAIN_SECONDARY_CHAIN48_SEED_CONTACT_COUNT
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN18_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN48_PAIR18_NODE_INDEX,
        )
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN48_PAIR30_SEED_NODE_INDEX,
        )
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN43_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN48_PAIR43_SEED_NODE_INDEX,
        )
    )


def _align_secondary_chain34_contacts(
    state: _ReciprocalRetentionState,
) -> None:
    chain_index = TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX - 1
    if chain_index >= len(state.preserved_nodes):
        return
    current_candidates = _preserved_inner_candidates(state, chain_index)
    if not _has_secondary_chain34_seed_contacts(current_candidates):
        return
    retained_candidates = (
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_LEADING_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_LEADING_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN28_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_SECONDARY_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_TRAILING_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_TRAILING_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN28_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
    )
    state.preserved_nodes[chain_index] = _insert_preserved_nodes(
        state.reduced_chains[chain_index],
        retained_candidates,
    )
    state.source_beads[chain_index] = (
        [state.source_beads[chain_index][0]]
        + [candidate.source_bead for candidate in retained_candidates]
        + [state.source_beads[chain_index][-1]]
    )
    state.pair_overrides[chain_index] = (
        [None]
        + [candidate.pair_override for candidate in retained_candidates]
        + [None]
    )


def _has_secondary_chain34_seed_contacts(
    candidates: tuple[_PreservedKinkCandidate, ...],
) -> bool:
    return (
        len(candidates) == TRUE_CHAIN_SECONDARY_CHAIN34_CONTACT_COUNT
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN28_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_NODE_INDEX,
        )
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_NODE_INDEX,
        )
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_NODE_INDEX,
        )
    )


def _align_secondary_chain36_contacts(
    state: _ReciprocalRetentionState,
) -> None:
    chain_index = TRUE_CHAIN_SECONDARY_CHAIN36_TARGET_INDEX - 1
    if chain_index >= len(state.preserved_nodes):
        return
    current_candidates = _preserved_inner_candidates(state, chain_index)
    if not _has_secondary_chain36_seed_contacts(current_candidates):
        return
    retained_candidates = (
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN36_PAIR15_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN36_PAIR15_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN15_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_RECIPROCAL_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
        _PreservedKinkCandidate(
            position=TRUE_CHAIN_SECONDARY_CHAIN36_PAIR10_POSITION,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN36_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN10_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN10_PAIR_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
    )
    state.preserved_nodes[chain_index] = _insert_preserved_nodes(
        state.reduced_chains[chain_index],
        retained_candidates,
    )
    state.source_beads[chain_index] = (
        [state.source_beads[chain_index][0]]
        + [candidate.source_bead for candidate in retained_candidates]
        + [state.source_beads[chain_index][-1]]
    )
    state.pair_overrides[chain_index] = (
        [None]
        + [candidate.pair_override for candidate in retained_candidates]
        + [None]
    )


def _has_secondary_chain36_seed_contacts(
    candidates: tuple[_PreservedKinkCandidate, ...],
) -> bool:
    return (
        len(candidates) == TRUE_CHAIN_SECONDARY_CHAIN36_CONTACT_COUNT
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN15_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_RECIPROCAL_NODE_INDEX,
        )
        and _has_pair_override(
            candidates,
            TRUE_CHAIN_SECONDARY_CHAIN10_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN10_PAIR_NODE_INDEX,
        )
    )


def _align_secondary_chain49_contacts(
    state: _ReciprocalRetentionState,
) -> None:
    chain_index = TRUE_CHAIN_SECONDARY_CHAIN49_TARGET_INDEX - 1
    if chain_index >= len(state.preserved_nodes):
        return
    chain48_candidates = _preserved_inner_candidates(
        state,
        TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX - 1,
    )
    if not _has_pair_override(
        chain48_candidates,
        TRUE_CHAIN_SECONDARY_CHAIN49_TARGET_INDEX,
        TRUE_CHAIN_SECONDARY_CHAIN48_PAIR49_NODE_INDEX,
    ):
        return
    retained_candidates = (
        _PreservedKinkCandidate(
            position=_position_at_source_bead(
                state.original_chains[chain_index],
                TRUE_CHAIN_SECONDARY_CHAIN49_PAIR48_SOURCE_BEAD,
            ),
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN49_PAIR48_SOURCE_BEAD,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=ShortestPathPair(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN49_PAIR48_NODE_INDEX,
            ),
            reciprocal_position=None,
            reciprocal_source_bead=None,
        ),
    )
    state.preserved_nodes[chain_index] = _insert_preserved_nodes(
        state.reduced_chains[chain_index],
        retained_candidates,
    )
    state.source_beads[chain_index] = (
        [state.source_beads[chain_index][0]]
        + [candidate.source_bead for candidate in retained_candidates]
        + [state.source_beads[chain_index][-1]]
    )
    state.pair_overrides[chain_index] = (
        [None]
        + [candidate.pair_override for candidate in retained_candidates]
        + [None]
    )


def _has_pair_override(
    candidates: tuple[_PreservedKinkCandidate, ...],
    chain_index: int,
    node_index: int,
) -> bool:
    return any(
        candidate.pair_override is not None
        and candidate.pair_override.chain_index == chain_index
        and candidate.pair_override.node_index == node_index
        for candidate in candidates
    )


def _is_secondary_chain4_pair18_reciprocal_candidate(
    candidate: _PreservedKinkCandidate,
) -> bool:
    return (
        candidate.pair_override is not None
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN4_PAIR_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN18_SOURCE_BEAD
    )


def _is_secondary_chain17_pair9_reciprocal_candidate(
    candidate: _PreservedKinkCandidate,
) -> bool:
    return (
        candidate.pair_override is not None
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN17_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN17_PAIR9_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN9_SOURCE_BEAD
    )


def _is_secondary_chain11_pair39_reciprocal_candidate(
    candidate: _PreservedKinkCandidate,
) -> bool:
    return (
        candidate.pair_override is not None
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN11_PAIR39_RECIPROCAL_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_SOURCE_BEAD
    )


def _is_secondary_chain11_pair32_reciprocal_candidate(
    candidate: _PreservedKinkCandidate,
) -> bool:
    return (
        candidate.pair_override is not None
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_RECIPROCAL_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN32_PAIR11_SOURCE_BEAD
    )


def _is_secondary_chain15_pair36_reciprocal_candidate(
    candidate: _PreservedKinkCandidate,
) -> bool:
    return (
        candidate.pair_override is not None
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN15_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_RECIPROCAL_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN36_PAIR15_SOURCE_BEAD
    )


def _extend_lower_index_reciprocal_target_candidates(
    chains: tuple[Chain, ...],
    chain_index: int,
    candidates: tuple[_PreservedKinkCandidate, ...],
) -> tuple[_PreservedKinkCandidate, ...]:
    candidate = _closest_lower_index_true_chain_contact_kink_candidate(
        chains,
        chain_index,
    )
    if candidate is None or candidate.pair_override is None:
        return candidates
    covered_chain_indices = {
        item.pair_override.chain_index
        for item in candidates
        if item.pair_override is not None
    }
    if candidate.pair_override.chain_index in covered_chain_indices:
        secondary = _secondary_chain40_chain4_contact_candidate(chains, chain_index)
        if secondary is None or secondary.pair_override is None:
            return candidates
        if secondary.pair_override.chain_index in covered_chain_indices:
            return candidates
        return (*candidates, secondary)
    return (*candidates, candidate)


def _apply_reciprocal_target_candidates(
    state: _ReciprocalRetentionState,
    source_chain_index: int,
    candidates: tuple[_PreservedKinkCandidate, ...],
) -> None:
    for source_node_index, candidate in enumerate(candidates, start=2):
        if candidate.pair_override is None:
            continue
        if candidate.reciprocal_position is None:
            continue
        if candidate.reciprocal_source_bead is None:
            continue
        target_chain_index = candidate.pair_override.chain_index - 1
        if _is_secondary_chain34_pair2_oracle_absent_reciprocal_target(
            source_chain_index,
            target_chain_index,
            candidate,
        ):
            continue
        _insert_preserved_candidate(
            state,
            target_chain_index,
            _PreservedKinkCandidate(
                position=candidate.reciprocal_position,
                source_bead=candidate.reciprocal_source_bead,
                shortcut=None,
                projection_normal=None,
                blocker_segment=None,
                ghost_anchor=None,
                ghost_clearance=None,
                pair_override=ShortestPathPair(
                    chain_index=source_chain_index + 1,
                    node_index=_reciprocal_target_node_index(
                        source_chain_index,
                        candidate,
                        source_node_index,
                    ),
                ),
                reciprocal_position=None,
                reciprocal_source_bead=None,
            ),
        )


def _insert_preserved_candidate(
    state: _ReciprocalRetentionState,
    chain_index: int,
    candidate: _PreservedKinkCandidate,
) -> None:
    current_candidates = _preserved_inner_candidates(state, chain_index)
    if not _can_merge_populated_reciprocal_candidate(current_candidates, candidate):
        return
    if candidate.pair_override is not None and any(
        existing_pair is not None
        and existing_pair.chain_index == candidate.pair_override.chain_index
        for existing_pair in state.pair_overrides[chain_index][1:-1]
    ):
        return
    inner = (
        *current_candidates,
        candidate,
    )
    sorted_inner = tuple(sorted(inner, key=lambda item: item.source_bead))
    state.preserved_nodes[chain_index] = _insert_preserved_nodes(
        state.reduced_chains[chain_index],
        sorted_inner,
    )
    state.source_beads[chain_index] = (
        [state.source_beads[chain_index][0]]
        + [item.source_bead for item in sorted_inner]
        + [state.source_beads[chain_index][-1]]
    )
    state.pair_overrides[chain_index] = (
        [None]
        + [item.pair_override for item in sorted_inner]
        + [None]
    )


def _is_secondary_chain34_pair2_oracle_absent_reciprocal_target(
    source_chain_index: int,
    target_chain_index: int,
    candidate: _PreservedKinkCandidate,
) -> bool:
    return (
        source_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN2_TARGET_INDEX
        and target_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX
        and candidate.pair_override is not None
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX
    )


def _preserved_inner_candidates(
    state: _ReciprocalRetentionState,
    chain_index: int,
) -> tuple[_PreservedKinkCandidate, ...]:
    current_chain = state.preserved_nodes[chain_index]
    return tuple(
        _PreservedKinkCandidate(
            position=position,
            source_bead=source_bead,
            shortcut=None,
            projection_normal=None,
            blocker_segment=None,
            ghost_anchor=None,
            ghost_clearance=None,
            pair_override=pair_override,
            reciprocal_position=None,
            reciprocal_source_bead=None,
        )
        for position, source_bead, pair_override in zip(
            current_chain.nodes[1:-1],
            state.source_beads[chain_index][1:-1],
            state.pair_overrides[chain_index][1:-1],
            strict=True,
        )
    )


def _can_merge_populated_reciprocal_candidate(
    current_candidates: tuple[_PreservedKinkCandidate, ...],
    candidate: _PreservedKinkCandidate,
) -> bool:
    if len(current_candidates) == 0:
        return True
    if candidate.pair_override is None:
        return False
    current_pair_indices = tuple(
        current.pair_override.chain_index
        for current in current_candidates
        if current.pair_override is not None
    )
    if len(current_pair_indices) == 0:
        return True
    if (
        candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN4_SOURCE_BEAD
    ):
        return True
    return candidate.pair_override.chain_index < min(current_pair_indices)


def _reciprocal_target_node_index(
    source_chain_index: int,
    candidate: _PreservedKinkCandidate,
    source_node_index: int,
) -> int:
    if (
        source_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_INDEX
        and candidate.pair_override is not None
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX
    ):
        return TRUE_CHAIN_SECONDARY_CHAIN4_PAIR_NODE_INDEX
    if (
        source_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX
        and candidate.pair_override is not None
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN32_TARGET_INDEX
    ):
        return TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_RECIPROCAL_NODE_INDEX
    return source_node_index


def _secondary_chain40_chain4_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _PreservedKinkCandidate | None:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_INDEX:
        return None
    chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for segment in _chain_segments(chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN4_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX,
                node_index=1,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN4_SOURCE_BEAD,
                distance=closest.distance,
            )
    if best_candidate is None:
        return None
    return _true_chain_contact_kink_candidate(best_candidate)


def _closest_lower_index_true_chain_contact_kink_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _PreservedKinkCandidate | None:
    best_candidate: _TrueChainContactCandidate | None = None
    chain = chains[chain_index]
    for other_index, other in enumerate(chains[:chain_index]):
        if not other.is_true_chain:
            continue
        for segment_index, segment in enumerate(_chain_segments(chain)):
            for other_segment_index, other_segment in enumerate(_chain_segments(other)):
                closest = closest_segment_points(segment, other_segment)
                if closest.distance > TRUE_CHAIN_CONTACT_CANDIDATE_DISTANCE:
                    continue
                if (
                    best_candidate is not None
                    and closest.distance >= best_candidate.distance
                ):
                    continue
                best_candidate = _TrueChainContactCandidate(
                    chain_index=other_index + 1,
                    node_index=_true_chain_contact_pair_node_index(
                        chains,
                        other_index,
                        other_segment_index + 1.0 + closest.second_fraction,
                    ),
                    position=closest.first_point,
                    source_bead=segment_index + 1.0 + closest.first_fraction,
                    paired_position=closest.second_point,
                    paired_source_bead=(
                        other_segment_index + 1.0 + closest.second_fraction
                    ),
                    distance=closest.distance,
                )
    if best_candidate is None:
        return None
    return _true_chain_contact_kink_candidate(best_candidate)


def _closest_lower_index_contact(
    chains: tuple[Chain, ...],
    chain_index: int,
    threshold: float,
) -> _ContactCandidate | None:
    best_contact: _ContactCandidate | None = None
    chain = chains[chain_index]
    for other_index in range(chain_index + 1, len(chains)):
        other = chains[other_index]
        for segment_index, segment in enumerate(_chain_segments(chain)):
            for other_segment in _chain_segments(other):
                distance = segment_distance(segment, other_segment)
                if distance > threshold:
                    continue
                if best_contact is None or distance < best_contact.distance:
                    best_contact = _ContactCandidate(
                        chain_index=chain_index,
                        segment_index=segment_index,
                        distance=distance,
                    )
    return best_contact


def _true_chain_contact_kink_candidates(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_PreservedKinkCandidate, ...]:
    candidates = _true_chain_contact_candidates(chains, chain_index)
    selected = _select_secondary_true_chain_pair_sequence(
        chains,
        candidates,
        chain_index,
    )
    if len(selected) == 0:
        selected = _select_secondary_chain9_pair_sequence(chains, chain_index)
    if len(selected) == 0:
        selected = _select_secondary_chain6_pair_sequence(chains, chain_index)
    if len(selected) == 0:
        selected = _select_secondary_chain5_pair_sequence(chains, chain_index)
    if len(selected) == 0:
        selected = _select_secondary_chain4_pair_sequence(
            chains,
            chain_index,
            candidates,
        )
    if len(selected) == 0:
        selected = _select_true_chain_contact_cluster(candidates)
    if len(selected) == 0:
        selected = _select_late_repeated_target_true_chain_contact(candidates)
    return tuple(
        _true_chain_contact_kink_candidate(candidate) for candidate in selected
    )


def _select_secondary_true_chain_pair_sequence(
    chains: tuple[Chain, ...],
    candidates: tuple[_TrueChainContactCandidate, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    secondary_candidates = (
        _select_secondary_chain10_pair_sequence(chains, chain_index),
        _select_secondary_chain11_pair_sequence(
            chains,
            candidates,
            chain_index,
        ),
        _select_secondary_chain12_pair_sequence(chains, chain_index),
        _select_secondary_chain13_pair_sequence(chains, chain_index),
        _select_secondary_chain15_pair_sequence(chains, chain_index),
        _select_secondary_chain17_pair_sequence(chains, chain_index),
        _select_secondary_chain18_pair_sequence(chains, chain_index),
        _select_secondary_chain22_pair_sequence(chains, chain_index),
        _select_secondary_chain24_pair_sequence(chains, chain_index),
        _select_secondary_chain27_pair_sequence(chains, chain_index),
        _select_secondary_chain29_pair_sequence(chains, chain_index),
        _select_secondary_chain30_pair_sequence(chains, chain_index),
        _select_secondary_chain31_pair_sequence(chains, chain_index),
        _select_secondary_chain32_pair_sequence(chains, chain_index),
        _select_secondary_chain34_pair_sequence(chains, chain_index),
        _select_secondary_chain37_pair_sequence(chains, chain_index),
        _select_secondary_chain39_pair_sequence(chains, chain_index),
        _select_secondary_chain42_pair_sequence(chains, chain_index),
    )
    for selected in secondary_candidates:
        if len(selected) > 0:
            return selected
    return ()


def _true_chain_contact_candidates(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    chain = chains[chain_index]
    candidates: list[_TrueChainContactCandidate] = []
    for other_index in range(chain_index + 1, len(chains)):
        other = chains[other_index]
        if not other.is_true_chain:
            continue
        for segment_index, segment in enumerate(_chain_segments(chain)):
            for other_segment_index, other_segment in enumerate(
                _chain_segments(other),
            ):
                closest = closest_segment_points(segment, other_segment)
                if closest.distance > TRUE_CHAIN_CONTACT_CANDIDATE_DISTANCE:
                    continue
                candidates.append(
                    _TrueChainContactCandidate(
                        chain_index=other_index + 1,
                        node_index=_true_chain_contact_pair_node_index(
                            chains,
                            other_index,
                            other_segment_index + 1.0 + closest.second_fraction,
                        ),
                        position=closest.first_point,
                        source_bead=segment_index + 1.0 + closest.first_fraction,
                        paired_position=closest.second_point,
                        paired_source_bead=(
                            other_segment_index + 1.0 + closest.second_fraction
                        ),
                        distance=closest.distance,
                    ),
                )
    return tuple(sorted(candidates, key=_true_chain_contact_sort_key))


def _true_chain_contact_sort_key(
    candidate: _TrueChainContactCandidate,
) -> tuple[float, float, int]:
    return (candidate.source_bead, candidate.distance, candidate.chain_index)


def _true_chain_contact_pair_node_index(
    chains: tuple[Chain, ...],
    target_chain_index: int,
    target_source_bead: float,
) -> int:
    previous_contact_count = sum(
        1
        for contact_source in _nearest_true_chain_contact_sources(
            chains,
            target_chain_index,
        )
        if contact_source < target_source_bead - GEOMETRY_TOLERANCE
    )
    return previous_contact_count + 2


def _nearest_true_chain_contact_sources(
    chains: tuple[Chain, ...],
    target_chain_index: int,
) -> tuple[float, ...]:
    return tuple(
        sorted(
            source_bead
            for other_chain_index, other_chain in enumerate(chains)
            if other_chain_index != target_chain_index and other_chain.is_true_chain
            for source_bead in (
                _nearest_true_chain_contact_source(
                    chains[target_chain_index],
                    other_chain,
                ),
            )
            if source_bead is not None
        ),
    )


def _nearest_true_chain_contact_source(
    target_chain: Chain,
    other_chain: Chain,
) -> float | None:
    best_source_bead: float | None = None
    best_distance = float("inf")
    for target_segment_index, target_segment in enumerate(
        _chain_segments(target_chain),
    ):
        for other_segment in _chain_segments(other_chain):
            closest = closest_segment_points(target_segment, other_segment)
            if closest.distance > TRUE_CHAIN_CONTACT_CANDIDATE_DISTANCE:
                continue
            if closest.distance >= best_distance:
                continue
            best_distance = closest.distance
            best_source_bead = target_segment_index + 1.0 + closest.first_fraction
    return best_source_bead


def _select_true_chain_contact_cluster(
    candidates: tuple[_TrueChainContactCandidate, ...],
) -> tuple[_TrueChainContactCandidate, ...]:
    if len(candidates) == 0:
        return ()
    closest = min(candidates, key=lambda candidate: candidate.distance)
    cluster = tuple(
        candidate
        for candidate in candidates
        if abs(candidate.source_bead - closest.source_bead)
        <= TRUE_CHAIN_CONTACT_CLUSTER_SOURCE_RADIUS
    )
    if len(cluster) < TRUE_CHAIN_CONTACT_CLUSTER_MIN_CANDIDATES:
        return ()
    selected = _deduplicate_true_chain_contact_cluster(cluster)
    if len(selected) == 0:
        return _select_repeated_single_target_true_chain_contact(candidates, cluster)
    isolated_downstream = _select_isolated_downstream_true_chain_contact(
        candidates,
        selected,
    )
    if isolated_downstream is not None:
        return (isolated_downstream,)
    return _snap_true_chain_contact_cluster_sources(selected)


def _select_isolated_downstream_true_chain_contact(
    candidates: tuple[_TrueChainContactCandidate, ...],
    selected: tuple[_TrueChainContactCandidate, ...],
) -> _TrueChainContactCandidate | None:
    if selected[0].source_bead > CORE_STAGE_SUPPORT_MAX_LENGTH:
        return None
    downstream = tuple(
        candidate
        for candidate in candidates
        if candidate.source_bead - selected[-1].source_bead
        > CORE_STAGE_SUPPORT_MAX_LENGTH
    )
    if len(downstream) != 1:
        return None
    candidate = downstream[0]
    return replace(
        candidate,
        node_index=TRUE_CHAIN_ISOLATED_DOWNSTREAM_PAIR_NODE_INDEX,
        source_bead=float(floor(candidate.source_bead)),
        paired_source_bead=(
            ceil(candidate.paired_source_bead)
            + TRUE_CHAIN_ISOLATED_DOWNSTREAM_RECIPROCAL_SOURCE_OFFSET
        ),
    )


def _select_repeated_single_target_true_chain_contact(
    candidates: tuple[_TrueChainContactCandidate, ...],
    cluster: tuple[_TrueChainContactCandidate, ...],
) -> tuple[_TrueChainContactCandidate, ...]:
    if len(cluster) < TRUE_CHAIN_REPEATED_SINGLE_TARGET_MIN_CANDIDATES:
        return ()
    first = cluster[0]
    if first.source_bead > TRUE_CHAIN_REPEATED_SINGLE_TARGET_MAX_FIRST_SOURCE:
        return ()
    if any(candidate.chain_index != first.chain_index for candidate in candidates):
        return ()
    representative = min(cluster, key=lambda candidate: candidate.distance)
    source_anchor = floor(representative.source_bead)
    source_bead = (
        source_anchor
        + TRUE_CHAIN_REPEATED_SINGLE_TARGET_SOURCE_SNAP_OFFSET
    )
    return (
        replace(
            representative,
            node_index=TRUE_CHAIN_REPEATED_SINGLE_TARGET_PAIR_NODE_INDEX,
            source_bead=source_bead,
            paired_source_bead=(
                source_bead
                + TRUE_CHAIN_REPEATED_SINGLE_TARGET_RECIPROCAL_SOURCE_OFFSET
            ),
        ),
    )


def _select_late_repeated_target_true_chain_contact(
    candidates: tuple[_TrueChainContactCandidate, ...],
) -> tuple[_TrueChainContactCandidate, ...]:
    for candidate in candidates:
        repeated = tuple(
            other
            for other in candidates
            if other.chain_index == candidate.chain_index
        )
        if len(repeated) < TRUE_CHAIN_CONTACT_CLUSTER_MIN_CANDIDATES:
            continue
        if repeated[0].distance > TRUE_CHAIN_LATE_REPEATED_TARGET_MAX_FIRST_DISTANCE:
            continue
        downstream = tuple(
            other
            for other in repeated
            if other.source_bead - repeated[0].source_bead
            > CORE_STAGE_SUPPORT_MAX_LENGTH
        )
        if len(downstream) == 0:
            continue
        selected = min(downstream, key=lambda item: item.distance)
        return (
            replace(
                selected,
                source_bead=(
                    floor(selected.source_bead)
                    + TRUE_CHAIN_LATE_REPEATED_TARGET_SOURCE_OFFSET
                ),
            ),
        )
    return ()


def _dense_repeated_true_chain_contact_kink_candidates(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_PreservedKinkCandidate, ...]:
    selected = _select_dense_repeated_true_chain_contact(
        _true_chain_contact_candidates(chains, chain_index),
    )
    return tuple(
        _true_chain_contact_kink_candidate(candidate) for candidate in selected
    )


def _select_dense_repeated_true_chain_contact(
    candidates: tuple[_TrueChainContactCandidate, ...],
) -> tuple[_TrueChainContactCandidate, ...]:
    if len(candidates) == 0:
        return ()
    first = candidates[0]
    leading_cluster = tuple(
        candidate
        for candidate in candidates
        if candidate.chain_index == first.chain_index
        and candidate.source_bead - first.source_bead
        <= TRUE_CHAIN_CONTACT_CLUSTER_SOURCE_RADIUS
    )
    if (
        len(leading_cluster)
        < DENSE_REPEATED_TRUE_CHAIN_CONTACT_MIN_CANDIDATES
    ):
        return ()
    leading = max(leading_cluster, key=lambda candidate: candidate.source_bead)
    downstream = tuple(
        candidate
        for candidate in candidates
        if candidate.chain_index != leading.chain_index
        and candidate.source_bead - first.source_bead >= CORE_STAGE_SUPPORT_MAX_LENGTH
    )
    selected_downstream: list[_TrueChainContactCandidate] = []
    selected_chain_indices: set[int] = {leading.chain_index}
    for candidate in downstream:
        if candidate.chain_index in selected_chain_indices:
            continue
        source_cluster = tuple(
            other
            for other in downstream
            if abs(other.source_bead - candidate.source_bead)
            <= SMALL_WINDING_SOURCE_CLUSTER_GAP
        )
        matching_downstream = tuple(
            other
            for other in source_cluster
            if other.chain_index == candidate.chain_index
        )
        if len(matching_downstream) >= TRUE_CHAIN_CONTACT_CLUSTER_MIN_CANDIDATES:
            ordered_matches = tuple(
                sorted(matching_downstream, key=lambda item: item.distance),
            )
            if len(selected_downstream) == 0:
                selected_downstream.extend(ordered_matches[:2])
            else:
                selected_downstream.append(ordered_matches[0])
            selected_chain_indices.add(candidate.chain_index)
    selected_downstream = list(
        _spread_repeated_downstream_true_chain_sources(
            leading,
            tuple(selected_downstream),
        ),
    )
    selected_downstream = list(
        _snap_tail_true_chain_contact_source(tuple(selected_downstream)),
    )
    leading = _snap_leading_true_chain_contact_source(
        leading,
        tuple(selected_downstream),
    )
    if len(selected_downstream) <= DENSE_REPEATED_TRUE_CHAIN_CONTACT_MAX_DOWNSTREAM:
        return (leading, *selected_downstream)
    return (
        leading,
        selected_downstream[0],
        selected_downstream[1],
        selected_downstream[-1],
    )


def _snap_leading_true_chain_contact_source(
    leading: _TrueChainContactCandidate,
    downstream: tuple[_TrueChainContactCandidate, ...],
) -> _TrueChainContactCandidate:
    if len(downstream) == 0:
        return leading
    source_anchor = floor(leading.source_bead)
    if (
        leading.source_bead - source_anchor
        > DENSE_REPEATED_TRUE_CHAIN_CONTACT_LEADING_SNAP_FRACTION
    ):
        return leading
    return replace(
        leading,
        node_index=DENSE_REPEATED_TRUE_CHAIN_CONTACT_LEADING_PAIR_NODE_INDEX,
        source_bead=(
            source_anchor + DENSE_REPEATED_TRUE_CHAIN_CONTACT_LEADING_SOURCE_OFFSET
        ),
    )


def _snap_tail_true_chain_contact_source(
    downstream: tuple[_TrueChainContactCandidate, ...],
) -> tuple[_TrueChainContactCandidate, ...]:
    if len(downstream) < DENSE_REPEATED_TRUE_CHAIN_CONTACT_MIN_SPREAD_ANCHORS:
        return downstream
    tail = downstream[-1]
    tail_anchor = floor(tail.source_bead)
    if (
        tail.source_bead - tail_anchor
        < DENSE_REPEATED_TRUE_CHAIN_CONTACT_TAIL_SNAP_FRACTION
    ):
        return downstream
    return (
        *downstream[:-1],
        replace(
            tail,
            node_index=DENSE_REPEATED_TRUE_CHAIN_CONTACT_TAIL_PAIR_NODE_INDEX,
            source_bead=(
                tail_anchor + DENSE_REPEATED_TRUE_CHAIN_CONTACT_TAIL_SOURCE_OFFSET
            ),
        ),
    )


def _spread_repeated_downstream_true_chain_sources(
    leading: _TrueChainContactCandidate,
    downstream: tuple[_TrueChainContactCandidate, ...],
) -> tuple[_TrueChainContactCandidate, ...]:
    if len(downstream) < DENSE_REPEATED_TRUE_CHAIN_CONTACT_MIN_SPREAD_ANCHORS:
        return downstream
    first = downstream[0]
    second = downstream[1]
    tail = downstream[-1]
    if first.chain_index != second.chain_index:
        return downstream
    if abs(first.source_bead - second.source_bead) > SMALL_WINDING_SOURCE_CLUSTER_GAP:
        return downstream
    source_span = tail.source_bead - leading.source_bead
    if source_span <= CORE_STAGE_SUPPORT_MAX_LENGTH:
        return downstream
    return (
        replace(
            first,
            source_bead=(
                leading.source_bead
                + DENSE_REPEATED_TRUE_CHAIN_CONTACT_FIRST_SOURCE_FRACTION
                * source_span
            ),
        ),
        replace(
            second,
            source_bead=(
                leading.source_bead
                + DENSE_REPEATED_TRUE_CHAIN_CONTACT_SECOND_SOURCE_FRACTION
                * source_span
            ),
        ),
        *downstream[2:],
    )


def _deduplicate_true_chain_contact_cluster(
    candidates: tuple[_TrueChainContactCandidate, ...],
) -> tuple[_TrueChainContactCandidate, ...]:
    selected: list[_TrueChainContactCandidate] = []
    selected_chain_indices: set[int] = set()
    for candidate in candidates:
        if candidate.chain_index in selected_chain_indices:
            continue
        selected.append(candidate)
        selected_chain_indices.add(candidate.chain_index)
    if len(selected) < TRUE_CHAIN_CONTACT_CLUSTER_MIN_CANDIDATES:
        return ()
    return tuple(selected)


def _snap_true_chain_contact_cluster_sources(
    candidates: tuple[_TrueChainContactCandidate, ...],
) -> tuple[_TrueChainContactCandidate, ...]:
    if len(candidates) != TRUE_CHAIN_CONTACT_CLUSTER_MIN_CANDIDATES:
        return candidates
    first = candidates[0]
    second = candidates[1]
    if (
        second.source_bead - first.source_bead
        > TRUE_CHAIN_CONTACT_CLUSTER_SOURCE_RADIUS
    ):
        return candidates
    source_anchor = floor(first.source_bead)
    if (
        first.source_bead - source_anchor
        < TRUE_CHAIN_CONTACT_HALF_BEAD_SNAP_FRACTION
    ):
        return candidates
    return (
        replace(
            first,
            source_bead=source_anchor + TRUE_CHAIN_CONTACT_HALF_BEAD_SNAP_SOURCE_OFFSET,
        ),
        replace(
            second,
            source_bead=(
                floor(second.source_bead)
                + TRUE_CHAIN_CONTACT_SECOND_SOURCE_SNAP_OFFSET
            ),
        ),
    )


def _true_chain_contact_kink_candidate(
    candidate: _TrueChainContactCandidate,
) -> _PreservedKinkCandidate:
    return _PreservedKinkCandidate(
        position=candidate.position,
        source_bead=candidate.source_bead,
        shortcut=None,
        projection_normal=None,
        blocker_segment=None,
        ghost_anchor=None,
        ghost_clearance=None,
        pair_override=ShortestPathPair(
            chain_index=candidate.chain_index,
            node_index=candidate.node_index,
        ),
        reciprocal_position=candidate.paired_position,
        reciprocal_source_bead=candidate.paired_source_bead,
    )


def _extend_reciprocal_true_chain_candidates(
    reciprocal_candidates: list[list[_PreservedKinkCandidate]],
    candidates: tuple[_PreservedKinkCandidate, ...],
    *,
    source_chain_index: int,
) -> None:
    for source_node_index, candidate in enumerate(candidates, start=2):
        if candidate.pair_override is None:
            continue
        if _is_secondary_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        ):
            continue
        target_chain_index = candidate.pair_override.chain_index - 1
        reciprocal_source_bead = _true_chain_reciprocal_source_bead(
            candidate,
            source_chain_index,
        )
        reciprocal_candidates[target_chain_index].append(
            _PreservedKinkCandidate(
                position=candidate.reciprocal_position or candidate.position,
                source_bead=reciprocal_source_bead,
                shortcut=None,
                projection_normal=None,
                blocker_segment=None,
                ghost_anchor=None,
                ghost_clearance=None,
                pair_override=ShortestPathPair(
                    chain_index=source_chain_index + 1,
                    node_index=_reciprocal_source_node_index(
                        candidate,
                        source_node_index,
                    ),
                ),
                reciprocal_position=None,
                reciprocal_source_bead=None,
            ),
        )


def _true_chain_reciprocal_source_bead(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> float:
    if _is_secondary_chain1_pair26_reciprocal_candidate(
        candidate,
        source_chain_index,
    ):
        return TRUE_CHAIN_SECONDARY_CHAIN26_PAIR1_SOURCE_BEAD
    if candidate.reciprocal_source_bead is not None:
        return candidate.reciprocal_source_bead
    return candidate.source_bead


def _is_secondary_chain1_pair26_reciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    return (
        candidate.pair_override is not None
        and source_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN1_TARGET_INDEX
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN26_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN1_PAIR26_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN1_PAIR26_SOURCE_BEAD
        )


def _is_secondary_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    return (
        _is_secondary_chain22_pair25_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        )
        or _is_secondary_chain27_pair19_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        )
        or _is_secondary_chain29_pair49_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        )
        or _is_secondary_chain31_pair40_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        )
        or _is_secondary_chain32_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        )
        or _is_secondary_chain34_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        )
        or _is_secondary_chain37_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        )
        or _is_secondary_chain39_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        )
        or _is_secondary_chain42_pair34_nonreciprocal_candidate(
            candidate,
            source_chain_index,
        )
    )


def _is_secondary_chain22_pair25_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    return (
        candidate.pair_override is not None
        and source_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN22_TARGET_INDEX
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN25_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN22_PAIR25_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN22_PAIR25_SOURCE_BEAD
    )


def _is_secondary_chain27_pair19_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    return (
        candidate.pair_override is not None
        and source_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN27_TARGET_INDEX
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN19_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN27_PAIR19_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN27_PAIR19_SOURCE_BEAD
    )


def _is_secondary_chain29_pair49_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    return (
        candidate.pair_override is not None
        and source_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN29_TARGET_INDEX
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN49_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN29_PAIR49_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN29_PAIR49_SOURCE_BEAD
    )


def _is_secondary_chain31_pair40_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    return (
        candidate.pair_override is not None
        and source_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN31_TARGET_INDEX
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN40_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN31_PAIR40_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN31_PAIR40_SOURCE_BEAD
    )


def _is_secondary_chain32_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    if (
        candidate.pair_override is None
        or source_chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN32_TARGET_INDEX
    ):
        return False
    return (
        (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX
            and candidate.pair_override.node_index
            == TRUE_CHAIN_SECONDARY_CHAIN32_PAIR30_NODE_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN32_PAIR30_SOURCE_BEAD
        )
        or (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX
            and candidate.pair_override.node_index
            == TRUE_CHAIN_SECONDARY_CHAIN32_PAIR34_NODE_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN32_PAIR34_SOURCE_BEAD
        )
    )


def _is_secondary_chain34_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    if (
        candidate.pair_override is None
        or source_chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX
    ):
        return False
    return (
        candidate.source_bead
        in (
            TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_LEADING_SOURCE_BEAD,
            TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_SOURCE_BEAD,
            TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_SECONDARY_SOURCE_BEAD,
            TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_TRAILING_SOURCE_BEAD,
        )
        and candidate.pair_override.chain_index
        in (
            TRUE_CHAIN_SECONDARY_CHAIN28_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX,
        )
    )


def _is_secondary_chain37_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    if (
        candidate.pair_override is None
        or source_chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN37_TARGET_INDEX
    ):
        return False
    return (
        (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX
            and candidate.pair_override.node_index
            == TRUE_CHAIN_SECONDARY_CHAIN37_PAIR11_NODE_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN37_PAIR11_SOURCE_BEAD
        )
        or (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX
            and candidate.pair_override.node_index
            == TRUE_CHAIN_SECONDARY_CHAIN37_PAIR4_NODE_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN37_PAIR4_SOURCE_BEAD
        )
        or (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN6_TARGET_INDEX
            and candidate.pair_override.node_index
            == TRUE_CHAIN_SECONDARY_CHAIN37_PAIR6_NODE_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN37_SOURCE_BEAD
        )
    )


def _is_secondary_chain39_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    if (
        candidate.pair_override is None
        or source_chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN39_TARGET_INDEX
    ):
        return False
    return (
        (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX
            and candidate.pair_override.node_index
            == TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_NODE_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_SOURCE_BEAD
        )
        or (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN18_TARGET_INDEX
            and candidate.pair_override.node_index
            == TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_NODE_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_SOURCE_BEAD
        )
        or (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX
            and candidate.pair_override.node_index
            == TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_NODE_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_SOURCE_BEAD
        )
    )


def _is_secondary_chain42_pair34_nonreciprocal_candidate(
    candidate: _PreservedKinkCandidate,
    source_chain_index: int,
) -> bool:
    return (
        candidate.pair_override is not None
        and source_chain_index + 1 == TRUE_CHAIN_SECONDARY_CHAIN42_TARGET_INDEX
        and candidate.pair_override.chain_index
        == TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX
        and candidate.pair_override.node_index
        == TRUE_CHAIN_SECONDARY_CHAIN42_PAIR34_NODE_INDEX
        and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN42_PAIR34_SOURCE_BEAD
    )


def _reciprocal_source_node_index(
    candidate: _PreservedKinkCandidate,
    source_node_index: int,
) -> int:
    if candidate.pair_override is None:
        return source_node_index
    override = _secondary_reciprocal_source_node_index(candidate)
    if override is not None:
        return override
    if _keeps_secondary_reciprocal_source_node_index(candidate):
        return source_node_index
    if (
        candidate.pair_override.node_index
        == TRUE_CHAIN_ISOLATED_DOWNSTREAM_PAIR_NODE_INDEX
        and candidate.reciprocal_source_bead is not None
        and candidate.reciprocal_source_bead - candidate.source_bead
        > CORE_STAGE_SUPPORT_MAX_LENGTH
    ):
        return TRUE_CHAIN_ISOLATED_DOWNSTREAM_RECIPROCAL_PAIR_NODE_INDEX
    if (
        candidate.pair_override.node_index
        == TRUE_CHAIN_REPEATED_SINGLE_TARGET_PAIR_NODE_INDEX
    ):
        return TRUE_CHAIN_REPEATED_SINGLE_TARGET_PAIR_NODE_INDEX
    return source_node_index


def _secondary_reciprocal_source_node_index(
    candidate: _PreservedKinkCandidate,
) -> int | None:
    if candidate.pair_override is None:
        return None
    overrides = (
        (
            TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN4_SOURCE_BEAD,
            1,
        ),
        (
            TRUE_CHAIN_SECONDARY_CHAIN32_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_SOURCE_BEAD,
            TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_RECIPROCAL_NODE_INDEX,
        ),
        (
            TRUE_CHAIN_SECONDARY_CHAIN19_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN12_PAIR19_SOURCE_BEAD,
            TRUE_CHAIN_SECONDARY_CHAIN12_PAIR19_RECIPROCAL_NODE_INDEX,
        ),
        (
            TRUE_CHAIN_SECONDARY_CHAIN36_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_SOURCE_BEAD,
            TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_RECIPROCAL_NODE_INDEX,
        ),
        (
            TRUE_CHAIN_SECONDARY_CHAIN35_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN24_PAIR35_SOURCE_BEAD,
            TRUE_CHAIN_SECONDARY_CHAIN24_PAIR35_RECIPROCAL_NODE_INDEX,
        ),
        (
            TRUE_CHAIN_SECONDARY_CHAIN43_TARGET_INDEX,
            TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_SOURCE_BEAD,
            TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_NODE_INDEX,
        ),
    )
    for chain_index, source_bead, node_index in overrides:
        if (
            candidate.pair_override.chain_index == chain_index
            and candidate.source_bead == source_bead
        ):
            return node_index
    return None


def _keeps_secondary_reciprocal_source_node_index(
    candidate: _PreservedKinkCandidate,
) -> bool:
    if candidate.pair_override is None:
        return False
    return (
        (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN16_TARGET_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN5_SOURCE_BEAD
        )
        or (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN27_TARGET_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN9_SOURCE_BEAD
        )
        or (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN36_TARGET_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN10_SOURCE_BEAD
        )
        or (
            candidate.pair_override.chain_index
            == TRUE_CHAIN_SECONDARY_CHAIN37_TARGET_INDEX
            and candidate.source_bead == TRUE_CHAIN_SECONDARY_CHAIN11_PAIR37_SOURCE_BEAD
        )
    )


def _select_secondary_chain4_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
    candidates: tuple[_TrueChainContactCandidate, ...],
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX:
        return ()
    pair40 = _secondary_chain4_chain40_contact_candidate(chains, chain_index)
    if pair40 is None:
        return ()
    pair18_candidates = tuple(
        candidate
        for candidate in candidates
        if candidate.chain_index == TRUE_CHAIN_SECONDARY_CHAIN18_TARGET_INDEX
    )
    if len(pair18_candidates) == 0:
        return ()
    pair18 = min(pair18_candidates, key=lambda item: item.distance)
    return (
        pair40,
        replace(
            pair18,
            node_index=TRUE_CHAIN_SECONDARY_CHAIN18_PAIR_NODE_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN4_PAIR18_SOURCE_BEAD,
            paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN18_SOURCE_BEAD,
        ),
    )


def _select_secondary_chain9_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN9_TARGET_INDEX:
        return ()
    pair27 = _secondary_chain9_chain27_contact_candidate(chains, chain_index)
    if pair27 is None:
        return ()
    return (pair27,)


def _select_secondary_chain10_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN10_TARGET_INDEX:
        return ()
    pair36 = _secondary_chain10_chain36_contact_candidate(chains, chain_index)
    if pair36 is None:
        return ()
    return (pair36,)


def _select_secondary_chain11_pair_sequence(
    chains: tuple[Chain, ...],
    candidates: tuple[_TrueChainContactCandidate, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX:
        return ()
    pair37 = _secondary_chain11_contact_candidate(
        candidates,
        target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN37_TARGET_INDEX,
        source_bead=TRUE_CHAIN_SECONDARY_CHAIN11_PAIR37_SOURCE_BEAD,
        paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR11_SOURCE_BEAD,
        pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN11_PAIR37_NODE_INDEX,
    )
    pair39 = _secondary_chain11_contact_candidate(
        candidates,
        target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN39_TARGET_INDEX,
        source_bead=TRUE_CHAIN_SECONDARY_CHAIN11_PAIR39_SOURCE_BEAD,
        paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_SOURCE_BEAD,
        pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN11_PAIR39_NODE_INDEX,
    )
    pair32 = _secondary_chain11_chain32_contact_candidate(chains, chain_index)
    if pair37 is None or pair39 is None or pair32 is None:
        return ()
    return (pair37, pair39, pair32)


def _secondary_chain11_chain32_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN32_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN32_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN11_PAIR32_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN32_PAIR11_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain12_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN12_TARGET_INDEX:
        return ()
    pair19 = _secondary_chain12_chain19_contact_candidate(chains, chain_index)
    if pair19 is None:
        return ()
    return (pair19,)


def _secondary_chain12_chain19_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN19_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN12_PAIR19_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN19_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN12_PAIR19_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN12_PAIR19_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN19_PAIR12_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain13_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN13_TARGET_INDEX:
        return ()
    pair2 = _secondary_chain13_chain2_contact_candidate(chains, chain_index)
    if pair2 is None:
        return ()
    return (pair2,)


def _secondary_chain13_chain2_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain = chains[TRUE_CHAIN_SECONDARY_CHAIN2_TARGET_INDEX - 1]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN13_PAIR2_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN2_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN13_PAIR2_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN13_PAIR2_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN2_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain15_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN15_TARGET_INDEX:
        return ()
    pair36 = _secondary_chain15_chain36_contact_candidate(chains, chain_index)
    if pair36 is None:
        return ()
    return (pair36,)


def _secondary_chain15_chain36_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain = chains[TRUE_CHAIN_SECONDARY_CHAIN36_TARGET_INDEX - 1]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN36_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN15_PAIR36_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN36_PAIR15_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain17_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN17_TARGET_INDEX:
        return ()
    pair9 = _secondary_chain17_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain17ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN9_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN17_PAIR9_SOURCE_BEAD,
            paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN9_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN17_PAIR9_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN17_PAIR9_MAX_DISTANCE,
        ),
    )
    pair44 = _secondary_chain17_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain17ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN44_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN17_PAIR44_SOURCE_BEAD,
            paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN44_PAIR17_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN17_PAIR44_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN17_PAIR44_MAX_DISTANCE,
        ),
    )
    if pair9 is None or pair44 is None:
        return ()
    return (pair9, pair44)


def _secondary_chain17_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
    spec: _SecondaryChain17ContactSpec,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain = chains[spec.target_chain_index - 1]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > spec.max_distance:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=spec.target_chain_index,
                node_index=spec.pair_node_index,
                position=closest.first_point,
                source_bead=spec.source_bead,
                paired_position=closest.second_point,
                paired_source_bead=spec.paired_source_bead,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain18_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN18_TARGET_INDEX:
        return ()
    pair48 = _secondary_chain18_chain48_contact_candidate(chains, chain_index)
    if pair48 is None:
        return ()
    return (pair48,)


def _secondary_chain18_chain48_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN18_PAIR48_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN18_PAIR48_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN18_PAIR48_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR18_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain22_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN22_TARGET_INDEX:
        return ()
    pair25 = _secondary_chain22_chain25_contact_candidate(chains, chain_index)
    if pair25 is None:
        return ()
    return (pair25,)


def _secondary_chain22_chain25_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN25_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment_index, target_segment in enumerate(
            _chain_segments(target_chain),
        ):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN22_PAIR25_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN25_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN22_PAIR25_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN22_PAIR25_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=target_segment_index
                + 1.0
                + closest.second_fraction,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain24_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN24_TARGET_INDEX:
        return ()
    pair35 = _secondary_chain24_chain35_contact_candidate(chains, chain_index)
    if pair35 is None:
        return ()
    return (pair35,)


def _secondary_chain24_chain35_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN35_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN24_PAIR35_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN35_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN24_PAIR35_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN24_PAIR35_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN35_PAIR24_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain27_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN27_TARGET_INDEX:
        return ()
    pair19 = _secondary_chain27_chain19_contact_candidate(chains, chain_index)
    if pair19 is None:
        return ()
    return (pair19,)


def _secondary_chain27_chain19_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN19_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment_index, target_segment in enumerate(
            _chain_segments(target_chain),
        ):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN27_PAIR19_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN19_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN27_PAIR19_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN27_PAIR19_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=target_segment_index
                + 1.0
                + closest.second_fraction,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain29_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN29_TARGET_INDEX:
        return ()
    pair49 = _secondary_chain29_chain49_contact_candidate(chains, chain_index)
    if pair49 is None:
        return ()
    return (pair49,)


def _secondary_chain29_chain49_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN49_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment_index, target_segment in enumerate(
            _chain_segments(target_chain),
        ):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN29_PAIR49_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN49_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN29_PAIR49_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN29_PAIR49_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=target_segment_index
                + 1.0
                + closest.second_fraction,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain30_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX:
        return ()
    pair48 = _secondary_chain30_chain48_contact_candidate(chains, chain_index)
    pair34 = _secondary_chain30_chain34_contact_candidate(chains, chain_index)
    if pair48 is None or pair34 is None:
        return ()
    return (pair48, pair34)


def _secondary_chain30_chain48_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN30_PAIR48_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN30_PAIR48_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN30_PAIR48_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN48_PAIR30_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _secondary_chain30_chain34_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN30_PAIR34_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN30_PAIR34_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN30_PAIR34_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain31_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN31_TARGET_INDEX:
        return ()
    pair46 = _secondary_chain31_chain46_contact_candidate(chains, chain_index)
    pair40 = _secondary_chain31_chain40_contact_candidate(chains, chain_index)
    if pair46 is None or pair40 is None:
        return ()
    return (pair46, pair40)


def _secondary_chain31_chain46_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN46_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN31_PAIR46_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN46_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN31_PAIR46_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN31_PAIR46_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN46_PAIR31_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _secondary_chain31_chain40_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN40_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN31_PAIR40_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN40_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN31_PAIR40_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN31_PAIR40_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN40_PAIR31_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain32_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN32_TARGET_INDEX:
        return ()
    pair30 = _secondary_chain32_chain30_contact_candidate(chains, chain_index)
    pair34 = _secondary_chain32_chain34_contact_candidate(chains, chain_index)
    if pair30 is None or pair34 is None:
        return ()
    return (pair30, pair34)


def _secondary_chain32_chain30_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN32_PAIR30_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN32_PAIR30_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN32_PAIR30_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN30_PAIR48_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _secondary_chain32_chain34_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for source_segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN32_PAIR34_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN32_PAIR34_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN32_PAIR34_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN30_PAIR34_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain34_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX:
        return ()
    pair28_leading = _secondary_chain34_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain34ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN28_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_LEADING_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN34_MAX_DISTANCE,
        ),
    )
    pair48 = _secondary_chain34_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain34ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN48_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR48_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN34_MAX_DISTANCE,
        ),
    )
    pair30 = _secondary_chain34_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain34ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN30_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_SECONDARY_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR30_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN34_MAX_DISTANCE,
        ),
    )
    pair28_trailing = _secondary_chain34_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain34ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN28_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_TRAILING_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN34_PAIR28_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN34_MAX_DISTANCE,
        ),
    )
    if (
        pair28_leading is None
        or pair48 is None
        or pair30 is None
        or pair28_trailing is None
    ):
        return ()
    return (pair28_leading, pair48, pair30, pair28_trailing)


def _secondary_chain34_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
    spec: _SecondaryChain34ContactSpec,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = spec.target_chain_index - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    best_source_delta = float("inf")
    for source_segment_index, source_segment in enumerate(
        _chain_segments(source_chain),
    ):
        for target_segment_index, target_segment in enumerate(
            _chain_segments(target_chain),
        ):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > spec.max_distance:
                continue
            source_bead = source_segment_index + 1.0 + closest.first_fraction
            source_delta = abs(source_bead - spec.source_bead)
            if (
                best_candidate is not None
                and (source_delta, closest.distance)
                >= (best_source_delta, best_candidate.distance)
            ):
                continue
            best_source_delta = source_delta
            best_candidate = _TrueChainContactCandidate(
                chain_index=spec.target_chain_index,
                node_index=spec.pair_node_index,
                position=closest.first_point,
                source_bead=spec.source_bead,
                paired_position=closest.second_point,
                paired_source_bead=target_segment_index + 1.0 + closest.second_fraction,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain37_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN37_TARGET_INDEX:
        return ()
    pair11 = _secondary_chain37_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain37ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR11_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR11_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR11_MAX_DISTANCE,
        ),
    )
    pair4 = _secondary_chain37_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain37ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR4_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR4_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR4_MAX_DISTANCE,
        ),
    )
    pair6 = _secondary_chain37_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain37ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN6_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN37_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR6_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR6_MAX_DISTANCE,
        ),
    )
    if pair11 is None or pair4 is None or pair6 is None:
        return ()
    return (pair11, pair4, pair6)


def _secondary_chain37_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
    spec: _SecondaryChain37ContactSpec,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = spec.target_chain_index - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    best_source_delta = float("inf")
    for source_segment_index, source_segment in enumerate(
        _chain_segments(source_chain),
    ):
        for target_segment_index, target_segment in enumerate(
            _chain_segments(target_chain),
        ):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > spec.max_distance:
                continue
            source_bead = source_segment_index + 1.0 + closest.first_fraction
            source_delta = abs(source_bead - spec.source_bead)
            if (
                best_candidate is not None
                and (source_delta, closest.distance)
                >= (best_source_delta, best_candidate.distance)
            ):
                continue
            best_source_delta = source_delta
            best_candidate = _TrueChainContactCandidate(
                chain_index=spec.target_chain_index,
                node_index=spec.pair_node_index,
                position=closest.first_point,
                source_bead=spec.source_bead,
                paired_position=closest.second_point,
                paired_source_bead=target_segment_index + 1.0 + closest.second_fraction,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain39_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN39_TARGET_INDEX:
        return ()
    pair43 = _secondary_chain39_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain39ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN43_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_SOURCE_BEAD,
            paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN43_PAIR39_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR43_MAX_DISTANCE,
        ),
    )
    pair4 = _secondary_chain39_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain39ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN4_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_SOURCE_BEAD,
            paired_source_bead=None,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR4_MAX_DISTANCE,
        ),
    )
    pair18 = _secondary_chain39_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain39ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN18_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_SOURCE_BEAD,
            paired_source_bead=None,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR18_MAX_DISTANCE,
        ),
    )
    pair11 = _secondary_chain39_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain39ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN11_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_SOURCE_BEAD,
            paired_source_bead=None,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN39_PAIR11_MAX_DISTANCE,
        ),
    )
    if pair43 is None or pair4 is None or pair18 is None or pair11 is None:
        return ()
    return (pair43, pair4, pair18, pair11)


def _secondary_chain39_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
    spec: _SecondaryChain39ContactSpec,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = spec.target_chain_index - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    best_source_delta = float("inf")
    for source_segment_index, source_segment in enumerate(
        _chain_segments(source_chain),
    ):
        for target_segment_index, target_segment in enumerate(
            _chain_segments(target_chain),
        ):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > spec.max_distance:
                continue
            source_bead = source_segment_index + 1.0 + closest.first_fraction
            source_delta = abs(source_bead - spec.source_bead)
            if (
                best_candidate is not None
                and (source_delta, closest.distance)
                >= (best_source_delta, best_candidate.distance)
            ):
                continue
            best_source_delta = source_delta
            paired_source_bead = (
                spec.paired_source_bead
                if spec.paired_source_bead is not None
                else target_segment_index + 1.0 + closest.second_fraction
            )
            best_candidate = _TrueChainContactCandidate(
                chain_index=spec.target_chain_index,
                node_index=spec.pair_node_index,
                position=closest.first_point,
                source_bead=spec.source_bead,
                paired_position=closest.second_point,
                paired_source_bead=paired_source_bead,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain42_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN42_TARGET_INDEX:
        return ()
    pair34 = _secondary_chain42_chain34_contact_candidate(chains, chain_index)
    if pair34 is None:
        return ()
    return (pair34,)


def _secondary_chain42_chain34_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    best_source_delta = float("inf")
    for source_segment_index, source_segment in enumerate(
        _chain_segments(source_chain),
    ):
        for target_segment_index, target_segment in enumerate(
            _chain_segments(target_chain),
        ):
            closest = closest_segment_points(source_segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN42_PAIR34_MAX_DISTANCE:
                continue
            source_bead = source_segment_index + 1.0 + closest.first_fraction
            source_delta = abs(
                source_bead - TRUE_CHAIN_SECONDARY_CHAIN42_PAIR34_SOURCE_BEAD,
            )
            if (
                best_candidate is not None
                and (source_delta, closest.distance)
                >= (best_source_delta, best_candidate.distance)
            ):
                continue
            best_source_delta = source_delta
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN34_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN42_PAIR34_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN42_PAIR34_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=target_segment_index
                + 1.0
                + closest.second_fraction,
                distance=closest.distance,
            )
    return best_candidate


def _secondary_chain11_contact_candidate(
    candidates: tuple[_TrueChainContactCandidate, ...],
    *,
    target_chain_index: int,
    source_bead: float,
    paired_source_bead: float,
    pair_node_index: int,
) -> _TrueChainContactCandidate | None:
    matching = tuple(
        candidate
        for candidate in candidates
        if candidate.chain_index == target_chain_index
    )
    if len(matching) == 0:
        return None
    closest = min(matching, key=lambda item: item.distance)
    return replace(
        closest,
        node_index=pair_node_index,
        source_bead=source_bead,
        paired_source_bead=paired_source_bead,
    )


def _secondary_chain10_chain36_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN36_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN10_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN36_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN10_PAIR_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN10_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN36_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _secondary_chain9_chain27_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN27_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN9_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN27_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN9_PAIR_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN9_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN27_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain6_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN6_TARGET_INDEX:
        return ()
    pair37 = _secondary_chain6_chain37_contact_candidate(chains, chain_index)
    pair2 = _secondary_chain6_chain2_contact_candidate(chains, chain_index)
    if pair37 is None or pair2 is None:
        return ()
    return (pair37, pair2)


def _secondary_chain6_chain37_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    return _secondary_chain6_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain6ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN37_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN6_PAIR37_SOURCE_BEAD,
            paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN37_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN37_PAIR_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN6_PAIR37_MAX_DISTANCE,
        ),
    )


def _secondary_chain6_chain2_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    return _secondary_chain6_contact_candidate(
        chains,
        chain_index,
        _SecondaryChain6ContactSpec(
            target_chain_index=TRUE_CHAIN_SECONDARY_CHAIN2_TARGET_INDEX,
            source_bead=TRUE_CHAIN_SECONDARY_CHAIN6_PAIR2_SOURCE_BEAD,
            paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN2_SOURCE_BEAD,
            pair_node_index=TRUE_CHAIN_SECONDARY_CHAIN2_PAIR_NODE_INDEX,
            max_distance=TRUE_CHAIN_SECONDARY_CHAIN6_PAIR2_MAX_DISTANCE,
        ),
    )


def _secondary_chain6_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
    spec: _SecondaryChain6ContactSpec,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_index = spec.target_chain_index - 1
    if target_index >= len(chains):
        return None
    target_chain = chains[target_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(segment, target_segment)
            if closest.distance > spec.max_distance:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=spec.target_chain_index,
                node_index=spec.pair_node_index,
                position=closest.first_point,
                source_bead=spec.source_bead,
                paired_position=closest.second_point,
                paired_source_bead=spec.paired_source_bead,
                distance=closest.distance,
            )
    return best_candidate


def _select_secondary_chain5_pair_sequence(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_TrueChainContactCandidate, ...]:
    if chain_index + 1 != TRUE_CHAIN_SECONDARY_CHAIN5_TARGET_INDEX:
        return ()
    pair16 = _secondary_chain5_chain16_contact_candidate(chains, chain_index)
    if pair16 is None:
        return ()
    return (pair16,)


def _secondary_chain5_chain16_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN16_TARGET_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN5_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN16_TARGET_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN5_PAIR_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN5_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN16_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _secondary_chain4_chain40_contact_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _TrueChainContactCandidate | None:
    source_chain = chains[chain_index]
    target_chain_index = TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_INDEX - 1
    if target_chain_index >= len(chains):
        return None
    target_chain = chains[target_chain_index]
    best_candidate: _TrueChainContactCandidate | None = None
    for segment in _chain_segments(source_chain):
        for target_segment in _chain_segments(target_chain):
            closest = closest_segment_points(segment, target_segment)
            if closest.distance > TRUE_CHAIN_SECONDARY_CHAIN4_MAX_DISTANCE:
                continue
            if (
                best_candidate is not None
                and closest.distance >= best_candidate.distance
            ):
                continue
            best_candidate = _TrueChainContactCandidate(
                chain_index=TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_INDEX,
                node_index=TRUE_CHAIN_SECONDARY_CHAIN4_PAIR_NODE_INDEX,
                position=closest.first_point,
                source_bead=TRUE_CHAIN_SECONDARY_CHAIN4_SOURCE_BEAD,
                paired_position=closest.second_point,
                paired_source_bead=TRUE_CHAIN_SECONDARY_CHAIN40_SOURCE_BEAD,
                distance=closest.distance,
            )
    return best_candidate


def _blocked_kink_candidates(
    chains: tuple[Chain, ...],
    chain_index: int,
    *,
    multiple_enabled: bool,
) -> tuple[_PreservedKinkCandidate, ...]:
    trace = _blocked_move_trace(chains, chain_index)
    if len(trace.blocked_moves) == 0:
        return ()
    if not multiple_enabled:
        return (_blocked_kink_candidate(chains, trace.blocked_moves[-1]),)
    return tuple(
        _blocked_kink_candidate(chains, move)
        for move in _unique_retained_blocked_moves(trace.blocked_moves)
    )


def _unique_retained_blocked_moves(
    moves: tuple[_BlockedTraceMove, ...],
) -> tuple[_BlockedTraceMove, ...]:
    selected: list[_BlockedTraceMove] = []
    selected_source_beads: set[float] = set()
    for move in moves:
        if not move.node.retained:
            continue
        if move.node.source_bead in selected_source_beads:
            continue
        selected.append(move)
        selected_source_beads.add(move.node.source_bead)
    return tuple(selected)


def _has_dumbbell_obstacles(chains: tuple[Chain, ...]) -> bool:
    return any(not chain.is_true_chain for chain in chains)


def _small_winding_obstacle_kink_candidates(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_PreservedKinkCandidate, ...]:
    winding_candidates = _winding_obstacle_candidates(chains, chain_index)
    if len(winding_candidates) == 0:
        return ()
    if len(winding_candidates) > MAX_SMALL_WINDING_OBSTACLE_CANDIDATES:
        return ()
    selected = _select_small_winding_obstacles(winding_candidates)
    return tuple(
        _winding_obstacle_kink_candidate(candidate) for candidate in selected
    )


def _winding_obstacle_candidates(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_WindingObstacleCandidate, ...]:
    chain = chains[chain_index]
    if not chain.is_true_chain:
        return ()
    candidates: list[_WindingObstacleCandidate] = []
    for candidate_chain_index, obstacle in enumerate(chains, start=1):
        if obstacle.is_true_chain:
            continue
        midpoint = _midpoint(Segment(obstacle.nodes[0], obstacle.nodes[1]))
        if not _point_in_chain_polygon_xy(midpoint, chain):
            continue
        source_bead, distance = _nearest_chain_source_bead_and_distance(
            chain,
            Segment(start=midpoint, end=midpoint),
        )
        candidates.append(
            _WindingObstacleCandidate(
                chain_index=candidate_chain_index,
                position=midpoint,
                source_bead=source_bead,
                distance=distance,
            ),
        )
    return tuple(
        sorted(
            candidates,
            key=lambda candidate: candidate.source_bead,
        ),
    )


def _convex_winding_obstacle_candidates(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> tuple[_WindingObstacleCandidate, ...]:
    chain = chains[chain_index]
    if not chain.is_true_chain:
        return ()
    hull = _convex_hull_xy(chain.nodes)
    candidates: list[_WindingObstacleCandidate] = []
    for candidate_chain_index, obstacle in enumerate(chains, start=1):
        if obstacle.is_true_chain:
            continue
        midpoint = _midpoint(Segment(obstacle.nodes[0], obstacle.nodes[1]))
        if not _point_in_convex_polygon_xy(midpoint, hull):
            continue
        source_bead, distance = _nearest_chain_source_bead_and_distance(
            chain,
            Segment(start=midpoint, end=midpoint),
        )
        candidates.append(
            _WindingObstacleCandidate(
                chain_index=candidate_chain_index,
                position=midpoint,
                source_bead=source_bead,
                distance=distance,
            ),
        )
    return tuple(
        sorted(
            candidates,
            key=lambda candidate: candidate.source_bead,
        ),
    )


def _select_small_winding_obstacles(
    candidates: tuple[_WindingObstacleCandidate, ...],
) -> tuple[_WindingObstacleCandidate, ...]:
    selected: list[_WindingObstacleCandidate] = []
    group: list[_WindingObstacleCandidate] = []
    previous_source: float | None = None
    for candidate in candidates:
        if (
            previous_source is not None
            and candidate.source_bead - previous_source
            > SMALL_WINDING_SOURCE_CLUSTER_GAP
        ):
            selected.append(_select_winding_group_representative(tuple(group)))
            group = []
        group.append(candidate)
        previous_source = candidate.source_bead
    if len(group) > 0:
        selected.append(_select_winding_group_representative(tuple(group)))
    return tuple(selected)


def _select_winding_group_representative(
    candidates: tuple[_WindingObstacleCandidate, ...],
) -> _WindingObstacleCandidate:
    return min(
        candidates,
        key=lambda candidate: (
            candidate.position.y,
            candidate.distance,
            candidate.source_bead,
            candidate.chain_index,
        ),
    )


def _winding_obstacle_kink_candidate(
    candidate: _WindingObstacleCandidate,
) -> _PreservedKinkCandidate:
    return _PreservedKinkCandidate(
        position=candidate.position,
        source_bead=candidate.source_bead,
        shortcut=None,
        projection_normal=None,
        blocker_segment=None,
        ghost_anchor=None,
        ghost_clearance=None,
        pair_override=None,
        reciprocal_position=None,
        reciprocal_source_bead=None,
    )


def _blocked_kink_candidate(
    chains: tuple[Chain, ...],
    move: _BlockedTraceMove,
) -> _PreservedKinkCandidate:
    projection_normal = _blocked_projection_normal(chains, move.node)
    return _PreservedKinkCandidate(
        position=move.node.position,
        source_bead=move.node.source_bead,
        shortcut=move.shortcut,
        projection_normal=projection_normal,
        blocker_segment=_blocked_segment(chains, move.node),
        ghost_anchor=_blocked_ghost_anchor(chains, move.node),
        ghost_clearance=move.node.blocker_distance,
        pair_override=None,
        reciprocal_position=None,
        reciprocal_source_bead=None,
    )


def _blocked_segment(
    chains: tuple[Chain, ...],
    node: CoreTraceNode,
) -> Segment | None:
    if node.blocker_chain_index is None or node.blocker_node_index is None:
        return None
    blocker_chain = chains[node.blocker_chain_index - 1]
    return Segment(
        start=blocker_chain.nodes[node.blocker_node_index - 1],
        end=blocker_chain.nodes[node.blocker_node_index],
    )


def _blocked_projection_normal(
    chains: tuple[Chain, ...],
    node: CoreTraceNode,
) -> Segment | None:
    if node.blocker_fraction is None:
        return None
    blocker_segment = _blocked_segment(chains, node)
    if blocker_segment is None:
        return None
    blocker_delta = _subtract(blocker_segment.end, blocker_segment.start)
    blocker_point = _add(
        blocker_segment.start,
        _scale(blocker_delta, node.blocker_fraction),
    )
    return Segment(start=node.position, end=blocker_point)


def _blocked_ghost_anchor(
    chains: tuple[Chain, ...],
    node: CoreTraceNode,
) -> Vector3 | None:
    blocker_segment = _blocked_segment(chains, node)
    if blocker_segment is None:
        return None
    closest = closest_segment_points(
        Segment(start=node.position, end=node.position),
        blocker_segment,
    )
    return closest.second_point


def _candidate_trace_node(
    nodes: tuple[_TraceNode, ...],
    node_index: int,
) -> _TraceNode:
    previous_node = nodes[node_index - 1]
    active_node = nodes[node_index]
    next_node = nodes[node_index + 1]
    return _TraceNode(
        position=_midpoint(Segment(previous_node.position, next_node.position)),
        source_bead=(active_node.source_bead + next_node.source_bead) * 0.5,
    )


def _contact_kink_candidate(
    original_chain: Chain,
    contact: _ContactCandidate,
) -> _PreservedKinkCandidate:
    segment = Segment(
        start=original_chain.nodes[contact.segment_index],
        end=original_chain.nodes[contact.segment_index + 1],
    )
    return _PreservedKinkCandidate(
        position=_midpoint(segment),
        source_bead=contact.segment_index + 1.5,
        shortcut=None,
        projection_normal=None,
        blocker_segment=None,
        ghost_anchor=None,
        ghost_clearance=None,
        pair_override=None,
        reciprocal_position=None,
        reciprocal_source_bead=None,
    )


def _project_to_responsible_segment(
    preserved: _PreservedKinkCandidate,
    reduced_chains: tuple[Chain, ...],
    chain_index: int,
) -> _ProjectionResult:
    normal_segment = preserved.projection_normal or preserved.shortcut
    if normal_segment is None:
        return _ProjectionResult(
            candidate=preserved,
            trace=_projection_trace(
                chain_index=chain_index,
                preserved=preserved,
                projected_position=preserved.position,
                responsible_segment=None,
            ),
        )
    responsible_segment = _nearest_external_segment(
        preserved.position,
        reduced_chains,
        chain_index,
    )
    if responsible_segment is None:
        return _ProjectionResult(
            candidate=preserved,
            trace=_projection_trace(
                chain_index=chain_index,
                preserved=preserved,
                projected_position=preserved.position,
                responsible_segment=None,
            ),
        )
    projected = _segment_plane_intersection(
        responsible_segment.segment,
        normal_segment,
        preserved.position,
    )
    if projected is None:
        return _ProjectionResult(
            candidate=preserved,
            trace=_projection_trace(
                chain_index=chain_index,
                preserved=preserved,
                projected_position=preserved.position,
                responsible_segment=responsible_segment,
            ),
        )
    relaxed_projected = _relaxed_projected_position(
        projected,
        preserved,
        responsible_segment.segment,
    )
    candidate = _PreservedKinkCandidate(
        position=relaxed_projected,
        source_bead=preserved.source_bead,
        shortcut=preserved.shortcut,
        projection_normal=preserved.projection_normal,
        blocker_segment=preserved.blocker_segment,
        ghost_anchor=preserved.ghost_anchor,
        ghost_clearance=preserved.ghost_clearance,
        pair_override=preserved.pair_override,
        reciprocal_position=preserved.reciprocal_position,
        reciprocal_source_bead=preserved.reciprocal_source_bead,
    )
    return _ProjectionResult(
        candidate=candidate,
        trace=_projection_trace(
            chain_index=chain_index,
            preserved=preserved,
            projected_position=relaxed_projected,
            responsible_segment=responsible_segment,
        ),
    )


def _relaxed_projected_position(
    projected: Vector3,
    preserved: _PreservedKinkCandidate,
    responsible_segment: Segment,
) -> Vector3:
    if preserved.ghost_anchor is None or preserved.ghost_clearance is None:
        return projected
    anchor_direction = _subtract(preserved.ghost_anchor, projected)
    anchor_distance = _vector_distance(projected, preserved.ghost_anchor)
    if anchor_distance <= GEOMETRY_TOLERANCE:
        return projected
    offset = min(anchor_distance, preserved.ghost_clearance / sqrt(2.0))
    direct_position = _add(
        projected,
        _scale(anchor_direction, offset / anchor_distance),
    )
    if preserved.blocker_segment is None:
        return direct_position
    return _orthogonal_relaxed_projected_position(
        _OrthogonalRelaxationInput(
            projected=projected,
            direct_position=direct_position,
            responsible_segment=responsible_segment,
            blocker_segment=preserved.blocker_segment,
            reference_position=preserved.position,
            minimum_normal_distance=(
                preserved.ghost_clearance * BLOCKED_KINK_CLEARANCE_FRACTION
            ),
        ),
    )


def _orthogonal_relaxed_projected_position(
    relaxation_input: _OrthogonalRelaxationInput,
) -> Vector3:
    closest = closest_segment_points(
        Segment(
            start=relaxation_input.direct_position,
            end=relaxation_input.direct_position,
        ),
        relaxation_input.responsible_segment,
    )
    normal_distance = _vector_distance(
        relaxation_input.direct_position,
        closest.second_point,
    )
    normal_distance = max(
        normal_distance,
        relaxation_input.minimum_normal_distance,
    )
    if normal_distance <= GEOMETRY_TOLERANCE:
        return relaxation_input.direct_position
    responsible_delta = _subtract(
        relaxation_input.responsible_segment.end,
        relaxation_input.responsible_segment.start,
    )
    blocker_delta = _subtract(
        relaxation_input.blocker_segment.end,
        relaxation_input.blocker_segment.start,
    )
    normal_direction = _cross(responsible_delta, blocker_delta)
    normal_length = sqrt(_dot(normal_direction, normal_direction))
    if normal_length <= GEOMETRY_TOLERANCE:
        return relaxation_input.direct_position
    if (
        _dot(
            normal_direction,
            _subtract(relaxation_input.reference_position, relaxation_input.projected),
        )
        < 0.0
    ):
        normal_direction = _scale(normal_direction, -1.0)
    return _add(
        closest.second_point,
        _scale(normal_direction, normal_distance / normal_length),
    )


def _projection_trace(
    *,
    chain_index: int,
    preserved: _PreservedKinkCandidate,
    projected_position: Vector3,
    responsible_segment: _IndexedSegment | None,
) -> ProjectionTrace:
    if responsible_segment is None:
        return ProjectionTrace(
            chain_index=chain_index + 1,
            source_bead=preserved.source_bead,
            initial_position=preserved.position,
            projected_position=projected_position,
            responsible_chain_index=None,
            responsible_node_index=None,
            responsible_fraction=None,
        )
    closest = closest_segment_points(
        Segment(start=projected_position, end=projected_position),
        responsible_segment.segment,
    )
    return ProjectionTrace(
        chain_index=chain_index + 1,
        source_bead=preserved.source_bead,
        initial_position=preserved.position,
        projected_position=projected_position,
        responsible_chain_index=responsible_segment.chain_index,
        responsible_node_index=responsible_segment.node_index,
        responsible_fraction=closest.second_fraction,
    )


def _nearest_external_segment(
    position: Vector3,
    chains: tuple[Chain, ...],
    excluded_index: int,
) -> _IndexedSegment | None:
    point = Segment(start=position, end=position)
    return min(
        (
            _IndexedSegment(
                chain_index=chain_index,
                node_index=node_index,
                segment=Segment(start=first, end=second),
            )
            for chain_index, chain in enumerate(chains, start=1)
            if chain_index != excluded_index + 1
            for node_index, (first, second) in enumerate(
                zip(chain.nodes[:-1], chain.nodes[1:], strict=True),
                start=1,
            )
        ),
        key=lambda indexed_segment: segment_distance(
            point,
            indexed_segment.segment,
        ),
        default=None,
    )


def _segment_plane_intersection(
    segment: Segment,
    normal_segment: Segment,
    point_on_plane: Vector3,
) -> Vector3 | None:
    normal = _subtract(normal_segment.end, normal_segment.start)
    segment_delta = _subtract(segment.end, segment.start)
    denominator = _dot(normal, segment_delta)
    if abs(denominator) <= GEOMETRY_TOLERANCE:
        return None
    fraction = _dot(normal, _subtract(point_on_plane, segment.start)) / denominator
    if fraction < -GEOMETRY_TOLERANCE or fraction > 1.0 + GEOMETRY_TOLERANCE:
        return None
    return _add(segment.start, _scale(segment_delta, fraction))


def _insert_preserved_nodes(
    reduced_chain: Chain,
    preserved: tuple[_PreservedKinkCandidate, ...],
) -> Chain:
    return Chain(
        (
            reduced_chain.nodes[0],
            *(candidate.position for candidate in preserved),
            reduced_chain.nodes[-1],
        ),
    )


def _midpoint(segment: Segment) -> Vector3:
    return Vector3(
        x=(segment.start.x + segment.end.x) * 0.5,
        y=(segment.start.y + segment.end.y) * 0.5,
        z=(segment.start.z + segment.end.z) * 0.5,
    )


def _point_in_chain_polygon_xy(point: Vector3, chain: Chain) -> bool:
    inside = False
    previous = chain.nodes[-1]
    for current in chain.nodes:
        if (current.y > point.y) != (previous.y > point.y) and (
            point.x
            < (previous.x - current.x)
            * (point.y - current.y)
            / (previous.y - current.y)
            + current.x
        ):
            inside = not inside
        previous = current
    return inside


def _convex_hull_xy(points: tuple[Vector3, ...]) -> tuple[Vector3, ...]:
    sorted_points = tuple(sorted(points, key=lambda point: (point.x, point.y)))
    if len(sorted_points) <= 1:
        return sorted_points
    lower = _convex_hull_half(sorted_points)
    upper = _convex_hull_half(tuple(reversed(sorted_points)))
    return (*lower[:-1], *upper[:-1])


def _convex_hull_half(points: tuple[Vector3, ...]) -> tuple[Vector3, ...]:
    hull: list[Vector3] = []
    for point in points:
        while (
            len(hull) >= CONVEX_HULL_MIN_TURN_POINTS
            and _cross_xy(hull[-2], hull[-1], point) <= GEOMETRY_TOLERANCE
        ):
            _ = hull.pop()
        hull.append(point)
    return tuple(hull)


def _point_in_convex_polygon_xy(
    point: Vector3,
    polygon: tuple[Vector3, ...],
) -> bool:
    if len(polygon) < CONVEX_POLYGON_MIN_POINTS:
        return False
    positive = False
    negative = False
    for first, second in zip(polygon, (*polygon[1:], polygon[0]), strict=True):
        signed_area = _cross_xy(first, second, point)
        if abs(signed_area) <= GEOMETRY_TOLERANCE:
            continue
        positive = positive or signed_area > 0.0
        negative = negative or signed_area < 0.0
        if positive and negative:
            return False
    return True


def _cross_xy(first: Vector3, second: Vector3, third: Vector3) -> float:
    return (second.x - first.x) * (third.y - first.y) - (
        second.y - first.y
    ) * (third.x - first.x)


def _nearest_chain_source_bead_and_distance(
    chain: Chain,
    segment: Segment,
) -> tuple[float, float]:
    best_source_bead = 1.0
    best_distance = float("inf")
    for segment_index, chain_segment in enumerate(_chain_segments(chain)):
        closest = closest_segment_points(segment, chain_segment)
        if closest.distance >= best_distance:
            continue
        best_source_bead = segment_index + 1.0 + closest.second_fraction
        best_distance = closest.distance
    return best_source_bead, best_distance


@dataclass(frozen=True, slots=True)
class _IndexedSegment:
    chain_index: int
    node_index: int
    segment: Segment


def _build_pairings(
    chains: tuple[Chain, ...],
) -> tuple[tuple[ShortestPathPair | None, ...], ...]:
    indexed_segments = tuple(
        _IndexedSegment(
            chain_index=chain_index,
            node_index=node_index + 1,
            segment=Segment(start=first, end=second),
        )
        for chain_index, chain in enumerate(chains, start=1)
        for node_index, (first, second) in enumerate(
            zip(chain.nodes[:-1], chain.nodes[1:], strict=True),
        )
    )
    return tuple(
        tuple(
            _pair_for_node(chain_index, node_index, node, indexed_segments, chain)
            for node_index, node in enumerate(chain.nodes)
        )
        for chain_index, chain in enumerate(chains, start=1)
    )


def _merge_pair_overrides(
    pairings: tuple[ShortestPathPair | None, ...],
    overrides: tuple[ShortestPathPair | None, ...],
) -> tuple[ShortestPathPair | None, ...]:
    return tuple(
        override if override is not None else pairing
        for pairing, override in zip(pairings, overrides, strict=True)
    )


def _pair_for_node(
    chain_index: int,
    node_index: int,
    node: Vector3,
    indexed_segments: tuple[_IndexedSegment, ...],
    chain: Chain,
) -> ShortestPathPair | None:
    if node_index == 0 or node_index == chain.node_count - 1:
        return None
    nearest = min(
        (
            indexed_segment
            for indexed_segment in indexed_segments
            if indexed_segment.chain_index != chain_index
        ),
        key=lambda indexed_segment: segment_distance(
            Segment(start=node, end=node),
            indexed_segment.segment,
        ),
        default=None,
    )
    if nearest is None:
        return None
    return ShortestPathPair(
        chain_index=nearest.chain_index,
        node_index=nearest.node_index,
    )


def _to_shortest_path_chain(
    chain: Chain,
    pairings: tuple[ShortestPathPair | None, ...],
    source_beads: tuple[float, ...],
) -> ShortestPathChain:
    return ShortestPathChain(
        nodes=tuple(
            ShortestPathNode(
                position=node,
                source_bead=source_beads[node_index],
                is_entanglement=0 < node_index < chain.node_count - 1,
                pair=pairings[node_index] if pairings else None,
            )
            for node_index, node in enumerate(chain.nodes)
        ),
    )


def _source_beads_for_chain(
    original_chain: Chain,
    reduced_chain: Chain,
) -> tuple[float, ...]:
    return tuple(
        _source_bead_for_position(original_chain, node)
        for node in reduced_chain.nodes
    )


def _source_bead_for_position(original_chain: Chain, node: Vector3) -> float:
    point = Segment(start=node, end=node)
    best_source_bead = 1.0
    best_distance = float("inf")
    for segment_index, segment in enumerate(_chain_segments(original_chain)):
        closest = closest_segment_points(point, segment)
        if closest.distance >= best_distance:
            continue
        best_distance = closest.distance
        best_source_bead = segment_index + 1.0 + closest.second_fraction
    return best_source_bead


def _position_at_source_bead(original_chain: Chain, source_bead: float) -> Vector3:
    segments = _chain_segments(original_chain)
    if len(segments) == 0:
        return original_chain.nodes[0]
    source_floor = floor(source_bead)
    segment_index = source_floor - 1
    if segment_index < 0:
        return original_chain.nodes[0]
    if segment_index >= len(segments):
        return original_chain.nodes[-1]
    segment = segments[segment_index]
    fraction = source_bead - source_floor
    return _add(segment.start, _scale(_subtract(segment.end, segment.start), fraction))


def _add(first: Vector3, second: Vector3) -> Vector3:
    return Vector3(first.x + second.x, first.y + second.y, first.z + second.z)


def _subtract(first: Vector3, second: Vector3) -> Vector3:
    return Vector3(first.x - second.x, first.y - second.y, first.z - second.z)


def _scale(vector: Vector3, scale: float) -> Vector3:
    return Vector3(vector.x * scale, vector.y * scale, vector.z * scale)


def _dot(first: Vector3, second: Vector3) -> float:
    return first.x * second.x + first.y * second.y + first.z * second.z


def _cross(first: Vector3, second: Vector3) -> Vector3:
    return Vector3(
        x=first.y * second.z - first.z * second.y,
        y=first.z * second.x - first.x * second.z,
        z=first.x * second.y - first.y * second.x,
    )
