from __future__ import annotations

from dataclasses import dataclass
from math import ceil, sqrt
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


@dataclass(frozen=True, slots=True)
class ReducerSettings:
    max_sweeps: int = 16
    pairing_enabled: bool = False
    contact_preservation_distance: float = 0.1


@dataclass(frozen=True, slots=True)
class ReducerResult:
    shortest_path: ShortestPathSnapshot
    summary: SummaryOutputs
    diagnostics: ReducerDiagnostics


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
    projection_traces: tuple[ProjectionTrace, ...]


@dataclass(frozen=True, slots=True)
class _CoreTraceDiagnostics:
    blocked_nodes: tuple[tuple[CoreTraceNode, ...], ...]
    accepted_blocked_move_count: int
    retained_blocked_node_count: int
    transient_blocked_node_count: int


def reduce_snapshot(
    snapshot: Snapshot,
    settings: ReducerSettings | None = None,
) -> ReducerResult:
    active_settings = settings or ReducerSettings()
    box = GeometryBox(lengths=snapshot.box, shear=snapshot.shear or 0.0)
    chains = tuple(unfold_chain(chain, box) for chain in snapshot.true_chains)
    core_trace = _core_trace_diagnostics(chains)
    core_chains = _reduce_chains(chains, active_settings)
    preserved = _preserve_close_contacts(chains, core_chains, active_settings)
    reduced_chains = preserved.chains
    source_beads = preserved.source_beads
    pairings = (
        _build_pairings(reduced_chains) if active_settings.pairing_enabled else ()
    )
    shortest_path = ShortestPathSnapshot(
        chains=tuple(
            _to_shortest_path_chain(
                chain,
                pairings[chain_index] if pairings else (),
                source_beads[chain_index],
            )
            for chain_index, chain in enumerate(reduced_chains)
        ),
        box=snapshot.box,
    )
    return ReducerResult(
        shortest_path=shortest_path,
        summary=build_summary_outputs(
            original=snapshot,
            primitive_path=shortest_path,
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


def write_reducer_outputs(directory: Path, result: ReducerResult) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    write_shortest_path_file(directory / "Z1+SP.dat", result.shortest_path)
    write_summary_outputs(directory, result.summary)


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
        reduced_chain = _reduce_chain_once(
            chain,
            MoveContext(blocking_segments=_blocking_segments(current, chain_index)),
        )
        cleaned_chain = clean_collinear_kinks(reduced_chain).chain
        reduced.append(cleaned_chain)
        current = (*tuple(reduced), *current[chain_index + 1 :])
    return tuple(reduced)


def _reduce_chain_once(chain: Chain, context: MoveContext) -> Chain:
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
        if _shortcut_is_clear(shortcut, swept_triangle, context):
            current = _remove_node(current, node_index)
            node_index = max(1, node_index - 1)
            continue
        candidate = _candidate_position(current, node_index)
        evaluation = evaluate_node_move(
            current,
            NodeMove(node_index=node_index, position=candidate),
            context,
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
) -> bool:
    return not any(
        segment_distance(shortcut, blocker) <= context.tolerance
        or segment_intersects_triangle(blocker, swept_triangle)
        for blocker in context.blocking_segments
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
        contact = _blocked_contact(shortcut, swept_triangle, indexed_blockers)
        if contact is None:
            current = (*current[:node_index], *current[node_index + 1 :])
            node_index = max(1, node_index - 1)
            continue
        candidate = _candidate_trace_node(current, node_index)
        evaluation = evaluate_node_move(
            Chain(tuple(node.position for node in current)),
            NodeMove(node_index=node_index, position=candidate.position),
            MoveContext(blockers),
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


@dataclass(frozen=True, slots=True)
class _ProjectionResult:
    candidate: _PreservedKinkCandidate
    trace: ProjectionTrace


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
    projection_traces: list[ProjectionTrace] = []
    for chain_index, chain in enumerate(original_chains):
        if preserved_nodes[chain_index].node_count > MIN_CHAIN_NODE_COUNT:
            continue
        contact = _closest_lower_index_contact(
            original_chains,
            chain_index,
            settings.contact_preservation_distance,
        )
        if contact is None:
            continue
        preserved = _blocked_kink_candidate(original_chains, chain_index)
        if preserved is None:
            preserved = _contact_kink_candidate(chain, contact)
        projection = _project_to_responsible_segment(
            preserved,
            reduced_chains,
            chain_index,
        )
        preserved = projection.candidate
        projection_traces.append(projection.trace)
        preserved_nodes[chain_index] = _insert_preserved_node(
            reduced_chains[chain_index],
            preserved.position,
        )
        source_beads[chain_index] = [
            source_beads[chain_index][0],
            preserved.source_bead,
            source_beads[chain_index][-1],
        ]
    return _PreservedChains(
        chains=tuple(preserved_nodes),
        source_beads=tuple(tuple(chain_sources) for chain_sources in source_beads),
        projection_traces=tuple(projection_traces),
    )


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


def _blocked_kink_candidate(
    chains: tuple[Chain, ...],
    chain_index: int,
) -> _PreservedKinkCandidate | None:
    trace = _blocked_move_trace(chains, chain_index)
    if not trace.blocked_moves:
        return None
    move = trace.blocked_moves[-1]
    projection_normal = _blocked_projection_normal(chains, move.node)
    return _PreservedKinkCandidate(
        position=move.node.position,
        source_bead=move.node.source_bead,
        shortcut=move.shortcut,
        projection_normal=projection_normal,
        blocker_segment=_blocked_segment(chains, move.node),
        ghost_anchor=_blocked_ghost_anchor(chains, move.node),
        ghost_clearance=move.node.blocker_distance,
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
        projected=projected,
        direct_position=direct_position,
        responsible_segment=responsible_segment,
        blocker_segment=preserved.blocker_segment,
        reference_position=preserved.position,
    )


def _orthogonal_relaxed_projected_position(
    *,
    projected: Vector3,
    direct_position: Vector3,
    responsible_segment: Segment,
    blocker_segment: Segment,
    reference_position: Vector3,
) -> Vector3:
    closest = closest_segment_points(
        Segment(start=direct_position, end=direct_position),
        responsible_segment,
    )
    normal_distance = _vector_distance(direct_position, closest.second_point)
    if normal_distance <= GEOMETRY_TOLERANCE:
        return direct_position
    responsible_delta = _subtract(responsible_segment.end, responsible_segment.start)
    blocker_delta = _subtract(blocker_segment.end, blocker_segment.start)
    normal_direction = _cross(responsible_delta, blocker_delta)
    normal_length = sqrt(_dot(normal_direction, normal_direction))
    if normal_length <= GEOMETRY_TOLERANCE:
        return direct_position
    if _dot(normal_direction, _subtract(reference_position, projected)) < 0.0:
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


def _insert_preserved_node(
    reduced_chain: Chain,
    node: Vector3,
) -> Chain:
    return Chain((reduced_chain.nodes[0], node, reduced_chain.nodes[-1]))


def _midpoint(segment: Segment) -> Vector3:
    return Vector3(
        x=(segment.start.x + segment.end.x) * 0.5,
        y=(segment.start.y + segment.end.y) * 0.5,
        z=(segment.start.z + segment.end.z) * 0.5,
    )


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
