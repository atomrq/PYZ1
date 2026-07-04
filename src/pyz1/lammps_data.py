from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Final

from pyz1.errors import LammpsParseError
from pyz1.lammps_common import (
    LammpsBox,
    LammpsDataSection,
    ParsedLine,
    data_section_from_line,
    meaningful_lines,
    parse_float,
    parse_int,
)
from pyz1.lammps_models import LammpsAtom, LammpsImportOptions, LammpsTopology
from pyz1.models import Chain, Snapshot, Vector3

ATOM_COLUMNS_WITH_CHARGE: Final = 7
ATOM_COLUMNS_WITHOUT_CHARGE: Final = 6
ATOM_COLUMNS_WITH_IMAGES: Final = 9
ATOM_COLUMNS_WITH_CHARGE_IMAGES: Final = 10
HYDROGEN_MASS: Final = 1.0
HYDROGEN_TOLERANCE: Final = 0.01
MASS_ROW_MIN_FIELDS: Final = 2
BOND_ROW_MIN_FIELDS: Final = 4
MAX_LINEAR_CONNECTIONS: Final = 2


@dataclass(frozen=True, slots=True)
class LammpsDataParse:
    topology: LammpsTopology
    atoms: dict[int, LammpsAtom]

    def to_snapshot(self) -> Snapshot:
        chains = tuple(
            Chain(nodes=tuple(self.atoms[atom_id].position for atom_id in chain))
            for chain in self.topology.chains
        )
        return Snapshot(
            chains=chains,
            box=self.topology.box,
            label=0,
            shear=self.topology.shear,
        )


def parse_lammps_data_text(
    text: str,
    *,
    options: LammpsImportOptions,
) -> LammpsDataParse:
    lines = meaningful_lines(text)
    masses = _parse_masses(lines)
    box = _parse_box(lines)
    atoms = _parse_atoms(lines, masses=masses, options=options)
    bonds = _parse_bonds(lines)
    chains = _build_linear_chains(atoms=atoms, bonds=bonds)
    return LammpsDataParse(
        topology=LammpsTopology(chains=chains, box=box.lengths, shear=box.shear),
        atoms=atoms,
    )


def _parse_box(lines: tuple[ParsedLine, ...]) -> LammpsBox:
    xlo = xhi = ylo = yhi = zlo = zhi = None
    shear: float | None = None
    for line in lines:
        fields = line.text.split()
        if fields[-2:] == ["xlo", "xhi"]:
            xlo = parse_float(fields[0], line_number=line.number, name="xlo")
            xhi = parse_float(fields[1], line_number=line.number, name="xhi")
        if fields[-2:] == ["ylo", "yhi"]:
            ylo = parse_float(fields[0], line_number=line.number, name="ylo")
            yhi = parse_float(fields[1], line_number=line.number, name="yhi")
        if fields[-2:] == ["zlo", "zhi"]:
            zlo = parse_float(fields[0], line_number=line.number, name="zlo")
            zhi = parse_float(fields[1], line_number=line.number, name="zhi")
        if fields[-3:] == ["xy", "xz", "yz"]:
            shear = parse_float(fields[0], line_number=line.number, name="xy")
    if (
        xlo is None
        or xhi is None
        or ylo is None
        or yhi is None
        or zlo is None
        or zhi is None
    ):
        raise LammpsParseError(line_number=0, reason="missing box bounds")
    return LammpsBox(
        low=Vector3(xlo, ylo, zlo),
        high=Vector3(xhi, yhi, zhi),
        shear=shear,
    )


def _parse_masses(lines: tuple[ParsedLine, ...]) -> dict[int, float]:
    masses: dict[int, float] = {}
    for line in _section_lines(lines, LammpsDataSection.MASSES):
        fields = line.text.split()
        if len(fields) < MASS_ROW_MIN_FIELDS:
            raise LammpsParseError(line_number=line.number, reason="invalid mass row")
        atom_type = parse_int(fields[0], line_number=line.number, name="atom type")
        masses[atom_type] = parse_float(fields[1], line_number=line.number, name="mass")
    if not masses:
        raise LammpsParseError(line_number=0, reason="missing Masses section")
    return masses


def _parse_atoms(
    lines: tuple[ParsedLine, ...],
    *,
    masses: dict[int, float],
    options: LammpsImportOptions,
) -> dict[int, LammpsAtom]:
    atoms: dict[int, LammpsAtom] = {}
    for line in _section_lines(lines, LammpsDataSection.ATOMS):
        fields = line.text.split()
        atom_id, molecule_id, atom_type, position = _parse_atom_fields(
            fields,
            line=line,
        )
        mass = masses.get(atom_type)
        if mass is None:
            raise LammpsParseError(line_number=line.number, reason="unknown atom type")
        if _is_ignored_atom(atom_type=atom_type, mass=mass, options=options):
            continue
        atoms[atom_id] = LammpsAtom(
            atom_id=atom_id,
            molecule_id=molecule_id,
            atom_type=atom_type,
            position=position,
            mass=mass,
        )
    if not atoms:
        raise LammpsParseError(line_number=0, reason="no active atoms after filtering")
    return atoms


def _parse_atom_fields(
    fields: list[str],
    *,
    line: ParsedLine,
) -> tuple[int, int, int, Vector3]:
    match len(fields):
        case 6 | 9:
            atom_id_raw, molecule_id_raw, atom_type_raw = fields[:3]
            position_fields = tuple(fields[3:6])
        case 7 | 10:
            atom_id_raw, molecule_id_raw, atom_type_raw = fields[:3]
            position_fields = tuple(fields[4:7])
        case _:
            raise LammpsParseError(
                line_number=line.number,
                reason="unrecognized Atoms row",
            )
    return (
        parse_int(atom_id_raw, line_number=line.number, name="atom id"),
        parse_int(molecule_id_raw, line_number=line.number, name="molecule id"),
        parse_int(atom_type_raw, line_number=line.number, name="atom type"),
        Vector3(
            parse_float(position_fields[0], line_number=line.number, name="x"),
            parse_float(position_fields[1], line_number=line.number, name="y"),
            parse_float(position_fields[2], line_number=line.number, name="z"),
        ),
    )


def _parse_bonds(lines: tuple[ParsedLine, ...]) -> tuple[tuple[int, int], ...]:
    bonds: list[tuple[int, int]] = []
    for line in _section_lines(lines, LammpsDataSection.BONDS):
        fields = line.text.split()
        if len(fields) < BOND_ROW_MIN_FIELDS:
            raise LammpsParseError(line_number=line.number, reason="invalid bond row")
        bonds.append(
            (
                parse_int(fields[2], line_number=line.number, name="bond atom 1"),
                parse_int(fields[3], line_number=line.number, name="bond atom 2"),
            ),
        )
    if not bonds:
        raise LammpsParseError(line_number=0, reason="missing bond connectivity")
    return tuple(bonds)


def _section_lines(
    lines: tuple[ParsedLine, ...],
    section: LammpsDataSection,
) -> tuple[ParsedLine, ...]:
    selected: list[ParsedLine] = []
    active = False
    for line in lines:
        current = data_section_from_line(line.text)
        if current is not None:
            active = current == section
            continue
        if active:
            selected.append(line)
    return tuple(selected)


def _is_ignored_atom(
    *,
    atom_type: int,
    mass: float,
    options: LammpsImportOptions,
) -> bool:
    if atom_type in options.ignored_atom_types:
        return True
    return options.ignore_hydrogen and abs(mass - HYDROGEN_MASS) < HYDROGEN_TOLERANCE


def _build_linear_chains(
    *,
    atoms: dict[int, LammpsAtom],
    bonds: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, ...], ...]:
    adjacency: defaultdict[int, list[int]] = defaultdict(list)
    active_ids = frozenset(atoms)
    for first, second in bonds:
        if first in active_ids and second in active_ids:
            adjacency[first].append(second)
            adjacency[second].append(first)
    if not adjacency:
        raise LammpsParseError(line_number=0, reason="missing bond connectivity")
    for atom_id, neighbors in adjacency.items():
        if len(neighbors) > MAX_LINEAR_CONNECTIONS:
            raise LammpsParseError(
                line_number=0,
                reason=f"branched structure at atom {atom_id}",
            )
    terminals = tuple(
        atom_id for atom_id, neighbors in adjacency.items() if len(neighbors) == 1
    )
    if len(terminals) == 0 or len(terminals) % 2 != 0:
        raise LammpsParseError(line_number=0, reason="invalid linear-chain terminals")
    return _walk_chains(terminals=terminals, adjacency=adjacency)


def _walk_chains(
    *,
    terminals: tuple[int, ...],
    adjacency: defaultdict[int, list[int]],
) -> tuple[tuple[int, ...], ...]:
    visited: set[int] = set()
    chains: list[tuple[int, ...]] = []
    for terminal in sorted(terminals):
        if terminal in visited:
            continue
        chain = _walk_one_chain(start=terminal, adjacency=adjacency)
        visited.update(chain)
        chains.append(chain)
    return tuple(chains)


def _walk_one_chain(
    *,
    start: int,
    adjacency: defaultdict[int, list[int]],
) -> tuple[int, ...]:
    chain = [start]
    previous: int | None = None
    current = start
    while True:
        candidates = [atom_id for atom_id in adjacency[current] if atom_id != previous]
        if not candidates:
            return tuple(chain)
        if len(candidates) > 1:
            raise LammpsParseError(line_number=0, reason="ambiguous chain traversal")
        previous = current
        current = candidates[0]
        chain.append(current)
