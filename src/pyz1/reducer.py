from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import TYPE_CHECKING

from pyz1.geometry import (
    GeometryBox,
    MoveContext,
    NodeMove,
    Segment,
    clean_collinear_kinks,
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


@dataclass(frozen=True, slots=True)
class ReducerSettings:
    max_sweeps: int = 16
    pairing_enabled: bool = False
    contact_preservation_distance: float = 0.1


@dataclass(frozen=True, slots=True)
class ReducerResult:
    shortest_path: ShortestPathSnapshot
    summary: SummaryOutputs


def reduce_snapshot(
    snapshot: Snapshot,
    settings: ReducerSettings | None = None,
) -> ReducerResult:
    active_settings = settings or ReducerSettings()
    box = GeometryBox(lengths=snapshot.box, shear=snapshot.shear or 0.0)
    chains = tuple(unfold_chain(chain, box) for chain in snapshot.true_chains)
    reduced_chains = _reduce_chains(chains, active_settings)
    reduced_chains = _preserve_close_contacts(chains, reduced_chains, active_settings)
    pairings = (
        _build_pairings(reduced_chains) if active_settings.pairing_enabled else ()
    )
    shortest_path = ShortestPathSnapshot(
        chains=tuple(
            _to_shortest_path_chain(
                chain,
                pairings[chain_index] if pairings else (),
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
    )


def write_reducer_outputs(directory: Path, result: ReducerResult) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    write_shortest_path_file(directory / "Z1+SP.dat", result.shortest_path)
    write_summary_outputs(directory, result.summary)


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


def _chain_segments(chain: Chain) -> tuple[Segment, ...]:
    return tuple(
        Segment(start=first, end=second)
        for first, second in zip(chain.nodes[:-1], chain.nodes[1:], strict=True)
    )


@dataclass(frozen=True, slots=True)
class _ContactCandidate:
    chain_index: int
    segment_index: int
    distance: float


def _preserve_close_contacts(
    original_chains: tuple[Chain, ...],
    reduced_chains: tuple[Chain, ...],
    settings: ReducerSettings,
) -> tuple[Chain, ...]:
    preserved_nodes = list(reduced_chains)
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
        preserved_nodes[chain_index] = _insert_contact_node(
            reduced_chains[chain_index],
            chain,
            contact,
        )
    return tuple(preserved_nodes)


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


def _insert_contact_node(
    reduced_chain: Chain,
    original_chain: Chain,
    contact: _ContactCandidate,
) -> Chain:
    segment = Segment(
        start=original_chain.nodes[contact.segment_index],
        end=original_chain.nodes[contact.segment_index + 1],
    )
    node = _midpoint(segment)
    return Chain((reduced_chain.nodes[0], node, reduced_chain.nodes[-1]))


def _midpoint(segment: Segment) -> Vector3:
    return Vector3(
        x=(segment.start.x + segment.end.x) * 0.5,
        y=(segment.start.y + segment.end.y) * 0.5,
        z=(segment.start.z + segment.end.z) * 0.5,
    )


@dataclass(frozen=True, slots=True)
class _IndexedNode:
    chain_index: int
    node_index: int
    position: Vector3


def _build_pairings(
    chains: tuple[Chain, ...],
) -> tuple[tuple[ShortestPathPair | None, ...], ...]:
    indexed_nodes = tuple(
        _IndexedNode(
            chain_index=chain_index,
            node_index=node_index,
            position=node,
        )
        for chain_index, chain in enumerate(chains, start=1)
        for node_index, node in enumerate(chain.nodes, start=1)
    )
    return tuple(
        tuple(
            _pair_for_node(chain_index, node_index, node, indexed_nodes, chain)
            for node_index, node in enumerate(chain.nodes)
        )
        for chain_index, chain in enumerate(chains, start=1)
    )


def _pair_for_node(
    chain_index: int,
    node_index: int,
    node: Vector3,
    indexed_nodes: tuple[_IndexedNode, ...],
    chain: Chain,
) -> ShortestPathPair | None:
    if node_index == 0 or node_index == chain.node_count - 1:
        return None
    nearest = min(
        (
            indexed_node
            for indexed_node in indexed_nodes
            if indexed_node.chain_index != chain_index
        ),
        key=lambda indexed_node: _distance(node, indexed_node.position),
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
) -> ShortestPathChain:
    return ShortestPathChain(
        nodes=tuple(
            ShortestPathNode(
                position=node,
                source_bead=float(node_index + 1),
                is_entanglement=0 < node_index < chain.node_count - 1,
                pair=pairings[node_index] if pairings else None,
            )
            for node_index, node in enumerate(chain.nodes)
        ),
    )


def _distance(first: Vector3, second: Vector3) -> float:
    dx = first.x - second.x
    dy = first.y - second.y
    dz = first.z - second.z
    return sqrt(dx * dx + dy * dy + dz * dz)
