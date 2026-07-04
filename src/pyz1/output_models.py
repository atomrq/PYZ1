from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyz1.models import Vector3


@dataclass(frozen=True, slots=True)
class Z1SummaryRecord:
    timestep: int
    true_chain_count: int
    mean_original_beads: float
    mean_squared_end_to_end: float
    mean_shortest_path_contour: float
    mean_entanglements: float
    coil_tube_diameter: float
    coil_tube_step_length: float
    root_mean_squared_contour: float
    ne_classical_kink: float
    ne_modified_kink: float
    ne_classical_coil: float
    ne_modified_coil: float
    mean_original_bond_length: float
    original_bead_density: float


@dataclass(frozen=True, slots=True)
class ShortestPathPair:
    chain_index: int
    node_index: int


@dataclass(frozen=True, slots=True)
class ShortestPathNode:
    position: Vector3
    source_bead: float
    is_entanglement: bool
    pair: ShortestPathPair | None


@dataclass(frozen=True, slots=True)
class ShortestPathChain:
    nodes: tuple[ShortestPathNode, ...]

    @property
    def node_count(self) -> int:
        return len(self.nodes)


@dataclass(frozen=True, slots=True)
class ShortestPathSnapshot:
    chains: tuple[ShortestPathChain, ...]
    box: Vector3

    @property
    def chain_count(self) -> int:
        return len(self.chains)
