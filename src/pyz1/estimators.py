from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import TYPE_CHECKING

from pyz1.errors import InvalidSnapshotError

if TYPE_CHECKING:
    from pyz1.models import Chain, Snapshot, Vector3


@dataclass(frozen=True, slots=True)
class InputStatistics:
    true_chain_count: int
    mean_original_beads: float
    root_mean_squared_end_to_end: float
    mean_original_bond_length: float
    original_bead_density: float


@dataclass(frozen=True, slots=True)
class PrimitivePathInput:
    original_chain_lengths: tuple[int, ...]
    end_to_end_distances: tuple[float, ...]
    shortest_path_contours: tuple[float, ...]
    entanglement_counts: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class PrimitivePathStatistics:
    mean_shortest_path_contour: float
    mean_entanglements: float
    coil_tube_diameter: float
    coil_tube_step_length: float
    root_mean_squared_contour: float
    ne_classical_kink: float
    ne_modified_kink: float
    ne_classical_coil: float
    ne_modified_coil: float


def compute_input_statistics(snapshot: Snapshot) -> InputStatistics:
    true_chains = snapshot.true_chains
    if len(true_chains) == 0:
        raise InvalidSnapshotError(reason="snapshot has no true chains")
    bond_lengths = _bond_lengths(true_chains)
    return InputStatistics(
        true_chain_count=len(true_chains),
        mean_original_beads=_mean(tuple(chain.node_count for chain in true_chains)),
        root_mean_squared_end_to_end=sqrt(
            _mean(tuple(_squared_end_to_end(chain) for chain in true_chains)),
        ),
        mean_original_bond_length=_mean(bond_lengths),
        original_bead_density=snapshot.node_count / _box_volume(snapshot.box),
    )


def compute_primitive_path_statistics(
    data: PrimitivePathInput,
) -> PrimitivePathStatistics:
    _validate_primitive_path_input(data)
    mean_original_beads = _mean(data.original_chain_lengths)
    mean_end_to_end_squared = _mean_squared(data.end_to_end_distances)
    mean_contour = _mean(data.shortest_path_contours)
    mean_contour_squared = _mean_squared(data.shortest_path_contours)
    mean_entanglements = _mean(data.entanglement_counts)
    original_bond_count = sum(length - 1 for length in data.original_chain_lengths)

    return PrimitivePathStatistics(
        mean_shortest_path_contour=mean_contour,
        mean_entanglements=mean_entanglements,
        coil_tube_diameter=mean_end_to_end_squared / mean_contour,
        coil_tube_step_length=sum(data.shortest_path_contours) / original_bond_count,
        root_mean_squared_contour=sqrt(mean_contour_squared),
        ne_classical_kink=_ne_classical_kink(
            mean_original_beads=mean_original_beads,
            mean_entanglements=mean_entanglements,
        ),
        ne_modified_kink=_ne_modified_kink(
            mean_original_beads=mean_original_beads,
            mean_entanglements=mean_entanglements,
        ),
        ne_classical_coil=(
            (mean_original_beads - 1.0) * mean_end_to_end_squared / mean_contour**2
        ),
        ne_modified_coil=_ne_modified_coil(
            mean_original_beads=mean_original_beads,
            mean_end_to_end_squared=mean_end_to_end_squared,
            mean_contour_squared=mean_contour_squared,
        ),
    )


def _validate_primitive_path_input(data: PrimitivePathInput) -> None:
    chain_count = len(data.original_chain_lengths)
    if chain_count == 0:
        raise InvalidSnapshotError(reason="primitive path input has no chains")
    if (
        len(data.end_to_end_distances) != chain_count
        or len(data.shortest_path_contours) != chain_count
        or len(data.entanglement_counts) != chain_count
    ):
        raise InvalidSnapshotError(
            reason="primitive path series must have the same number of chains",
        )
    if any(length <= 1 for length in data.original_chain_lengths):
        raise InvalidSnapshotError(reason="original chain lengths must exceed one bead")
    if any(distance < 0.0 for distance in data.end_to_end_distances):
        raise InvalidSnapshotError(reason="end-to-end distances must be nonnegative")
    if any(contour <= 0.0 for contour in data.shortest_path_contours):
        raise InvalidSnapshotError(reason="contour lengths must be positive")


def _ne_classical_kink(
    *,
    mean_original_beads: float,
    mean_entanglements: float,
) -> float:
    if mean_entanglements <= 0.0:
        return -1.0
    return (
        mean_original_beads
        * (mean_original_beads - 1.0)
        / (mean_entanglements * (mean_original_beads - 1.0) + mean_original_beads)
    )


def _ne_modified_kink(
    *,
    mean_original_beads: float,
    mean_entanglements: float,
) -> float:
    if mean_entanglements <= 0.0:
        return -1.0
    return mean_original_beads / mean_entanglements


def _ne_modified_coil(
    *,
    mean_original_beads: float,
    mean_end_to_end_squared: float,
    mean_contour_squared: float,
) -> float:
    if mean_end_to_end_squared <= 0.0:
        return -1.0
    denominator = mean_contour_squared / mean_end_to_end_squared - 1.0
    if denominator <= 0.0:
        return -1.0
    return (mean_original_beads - 1.0) / denominator


def _bond_lengths(chains: tuple[Chain, ...]) -> tuple[float, ...]:
    return tuple(
        _distance(first, second)
        for chain in chains
        for first, second in zip(chain.nodes[:-1], chain.nodes[1:], strict=True)
    )


def _squared_end_to_end(chain: Chain) -> float:
    return _squared_distance(chain.nodes[0], chain.nodes[-1])


def _box_volume(box: Vector3) -> float:
    return box.x * box.y * box.z


def _mean(values: tuple[float | int, ...]) -> float:
    if len(values) == 0:
        raise InvalidSnapshotError(reason="mean is undefined for an empty sequence")
    return float(sum(values) / len(values))


def _mean_squared(values: tuple[float, ...]) -> float:
    if len(values) == 0:
        raise InvalidSnapshotError(reason="mean is undefined for an empty sequence")
    return float(sum(value * value for value in values) / len(values))


def _distance(first: Vector3, second: Vector3) -> float:
    return sqrt(_squared_distance(first, second))


def _squared_distance(first: Vector3, second: Vector3) -> float:
    dx = first.x - second.x
    dy = first.y - second.y
    dz = first.z - second.z
    return dx * dx + dy * dy + dz * dz
