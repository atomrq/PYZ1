from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import floor
from typing import TYPE_CHECKING, Final

from pyz1.ppa_vector import PpaVector, dot_vectors, subtract_vectors

if TYPE_CHECKING:
    from collections.abc import Sequence

CellKey = tuple[int, int, int]
CellCounts = tuple[int, int, int]
CellWidths = tuple[float, float, float]
CELL_OFFSETS: Final[tuple[int, ...]] = (-1, 0, 1)


@dataclass(frozen=True, slots=True)
class PpaNeighborInput:
    positions: Sequence[PpaVector]
    chain_for_node: Sequence[int]
    box: PpaVector
    shear: float
    cutoff: float


@dataclass(frozen=True, slots=True)
class PpaNeighborPair:
    first: int
    second: int
    separation: PpaVector
    distance_squared: float


@dataclass(frozen=True, slots=True)
class _CellGrid:
    counts: CellCounts
    widths: CellWidths


def wca_neighbor_pairs(neighbor_input: PpaNeighborInput) -> tuple[PpaNeighborPair, ...]:
    if neighbor_input.cutoff <= 0.0:
        return ()

    grid = _cell_grid(neighbor_input.box, neighbor_input.cutoff)
    cells = _build_cells(neighbor_input, grid)
    cutoff_squared = neighbor_input.cutoff * neighbor_input.cutoff
    seen_pairs: set[tuple[int, int]] = set()
    pairs: list[PpaNeighborPair] = []

    for cell, node_indices in cells.items():
        for neighbor_cell in _neighbor_cells(cell, grid.counts):
            for first in node_indices:
                for second in cells.get(neighbor_cell, ()):
                    if second <= first:
                        continue
                    pair_key = (first, second)
                    if pair_key in seen_pairs:
                        continue
                    seen_pairs.add(pair_key)
                    if (
                        neighbor_input.chain_for_node[first]
                        == neighbor_input.chain_for_node[second]
                    ):
                        continue
                    separation = minimum_image(
                        subtract_vectors(
                            neighbor_input.positions[second],
                            neighbor_input.positions[first],
                        ),
                        neighbor_input.box,
                        neighbor_input.shear,
                    )
                    distance_squared = dot_vectors(separation, separation)
                    if 0.0 < distance_squared <= cutoff_squared:
                        pairs.append(
                            PpaNeighborPair(
                                first=first,
                                second=second,
                                separation=separation,
                                distance_squared=distance_squared,
                            ),
                        )

    return tuple(sorted(pairs, key=lambda pair: (pair.first, pair.second)))


def fold_periodic_vector(vector: PpaVector, box: PpaVector, shear: float) -> PpaVector:
    y_correction = round(vector.y / box.y)
    x = vector.x - shear * y_correction
    return PpaVector(
        x=x - round(x / box.x) * box.x,
        y=vector.y - y_correction * box.y,
        z=vector.z - round(vector.z / box.z) * box.z,
    )


def minimum_image(vector: PpaVector, box: PpaVector, shear: float) -> PpaVector:
    return fold_periodic_vector(vector, box, shear)


def _cell_grid(box: PpaVector, cutoff: float) -> _CellGrid:
    counts = (
        _axis_cell_count(box.x, cutoff),
        _axis_cell_count(box.y, cutoff),
        _axis_cell_count(box.z, cutoff),
    )
    return _CellGrid(
        counts=counts,
        widths=(box.x / counts[0], box.y / counts[1], box.z / counts[2]),
    )


def _axis_cell_count(length: float, cutoff: float) -> int:
    return max(1, floor(length / cutoff))


def _build_cells(
    neighbor_input: PpaNeighborInput,
    grid: _CellGrid,
) -> dict[CellKey, list[int]]:
    cells: dict[CellKey, list[int]] = {}
    for index, position in enumerate(neighbor_input.positions):
        key = _cell_key(position, neighbor_input, grid)
        cells.setdefault(key, []).append(index)
    return cells


def _cell_key(
    position: PpaVector,
    neighbor_input: PpaNeighborInput,
    grid: _CellGrid,
) -> CellKey:
    folded = fold_periodic_vector(position, neighbor_input.box, neighbor_input.shear)
    return (
        _axis_cell_index(
            folded.x,
            neighbor_input.box.x,
            grid.counts[0],
            grid.widths[0],
        ),
        _axis_cell_index(
            folded.y,
            neighbor_input.box.y,
            grid.counts[1],
            grid.widths[1],
        ),
        _axis_cell_index(
            folded.z,
            neighbor_input.box.z,
            grid.counts[2],
            grid.widths[2],
        ),
    )


def _axis_cell_index(
    coordinate: float,
    length: float,
    cell_count: int,
    cell_width: float,
) -> int:
    shifted = coordinate + 0.5 * length
    return min(cell_count - 1, max(0, floor(shifted / cell_width)))


def _neighbor_cells(cell: CellKey, counts: CellCounts) -> tuple[CellKey, ...]:
    cells: list[CellKey] = []
    for x_offset, y_offset, z_offset in product(
        CELL_OFFSETS,
        CELL_OFFSETS,
        CELL_OFFSETS,
    ):
        cells.append(
            (
                (cell[0] + x_offset) % counts[0],
                (cell[1] + y_offset) % counts[1],
                (cell[2] + z_offset) % counts[2],
            ),
        )
    return tuple(cells)
