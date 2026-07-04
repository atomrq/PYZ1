from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from pyz1.errors import InvalidChainError, InvalidSnapshotError

MIN_CHAIN_NODE_COUNT: Final = 2


@dataclass(frozen=True, slots=True)
class Vector3:
    x: float
    y: float
    z: float

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass(frozen=True, slots=True)
class Chain:
    nodes: tuple[Vector3, ...]

    def __post_init__(self) -> None:
        if len(self.nodes) < MIN_CHAIN_NODE_COUNT:
            raise InvalidChainError(node_count=len(self.nodes))

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def is_true_chain(self) -> bool:
        return self.node_count > MIN_CHAIN_NODE_COUNT


@dataclass(frozen=True, slots=True)
class Snapshot:
    chains: tuple[Chain, ...]
    box: Vector3
    label: int | None
    shear: float | None

    def __post_init__(self) -> None:
        if len(self.chains) == 0:
            raise InvalidSnapshotError(
                reason="snapshot must contain at least one chain",
            )
        if self.box.x <= 0.0 or self.box.y <= 0.0 or self.box.z <= 0.0:
            raise InvalidSnapshotError(reason="box lengths must be positive")

    @property
    def chain_count(self) -> int:
        return len(self.chains)

    @property
    def node_count(self) -> int:
        return sum(chain.node_count for chain in self.chains)

    @property
    def true_chains(self) -> tuple[Chain, ...]:
        return tuple(chain for chain in self.chains if chain.is_true_chain)

    @property
    def true_chain_count(self) -> int:
        return len(self.true_chains)

    @property
    def true_chain_lengths(self) -> tuple[int, ...]:
        return tuple(chain.node_count for chain in self.true_chains)
