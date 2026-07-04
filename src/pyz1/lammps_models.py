from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pyz1.errors import LammpsParseError

if TYPE_CHECKING:
    from pyz1.models import Vector3


@dataclass(frozen=True, slots=True)
class LammpsImportOptions:
    first_snapshot: int = 1
    last_snapshot: int | None = None
    each_snapshot: int = 1
    ignore_hydrogen: bool = False
    ignored_atom_types: frozenset[int] = frozenset()

    def __post_init__(self) -> None:
        if self.first_snapshot < 1:
            raise LammpsParseError(
                line_number=0,
                reason="first snapshot must be positive",
            )
        if self.last_snapshot is not None and self.last_snapshot < self.first_snapshot:
            raise LammpsParseError(
                line_number=0,
                reason="last snapshot must not precede first snapshot",
            )
        if self.each_snapshot < 1:
            raise LammpsParseError(
                line_number=0,
                reason="snapshot stride must be positive",
            )

    def includes_snapshot(self, snapshot_number: int) -> bool:
        if snapshot_number < self.first_snapshot:
            return False
        if self.last_snapshot is not None and snapshot_number > self.last_snapshot:
            return False
        return (snapshot_number - self.first_snapshot) % self.each_snapshot == 0


@dataclass(frozen=True, slots=True)
class LammpsAtom:
    atom_id: int
    molecule_id: int
    atom_type: int
    position: Vector3
    mass: float


@dataclass(frozen=True, slots=True)
class LammpsTopology:
    chains: tuple[tuple[int, ...], ...]
    box: Vector3
    shear: float | None

    @property
    def active_atom_ids(self) -> frozenset[int]:
        return frozenset(atom_id for chain in self.chains for atom_id in chain)
