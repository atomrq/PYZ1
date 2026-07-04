from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pyz1.errors import LammpsParseError
from pyz1.lammps_common import (
    LammpsBox,
    ParsedLine,
    meaningful_lines,
    parse_float,
    parse_int,
)
from pyz1.lammps_dump_box import parse_dump_box
from pyz1.models import Chain, Snapshot, Vector3

if TYPE_CHECKING:
    from pyz1.lammps_models import LammpsImportOptions, LammpsTopology


@dataclass(frozen=True, slots=True)
class DumpFrame:
    number: int
    timestep: int
    box: LammpsBox
    columns: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]


@dataclass(frozen=True, slots=True)
class CoordinateColumns:
    x: int
    y: int
    z: int
    scaled: bool


def parse_lammps_dump_text(
    text: str,
    *,
    options: LammpsImportOptions,
    topology: LammpsTopology | None = None,
) -> tuple[Snapshot, ...]:
    return tuple(
        _frame_to_snapshot(frame=frame, topology=topology)
        for frame in _parse_frames(text)
        if options.includes_snapshot(frame.number)
    )


def _parse_frames(text: str) -> tuple[DumpFrame, ...]:
    lines = meaningful_lines(text)
    frames: list[DumpFrame] = []
    cursor = 0
    while cursor < len(lines):
        frame, cursor = _parse_frame(lines=lines, cursor=cursor, number=len(frames) + 1)
        frames.append(frame)
    return tuple(frames)


def _parse_frame(
    *,
    lines: tuple[ParsedLine, ...],
    cursor: int,
    number: int,
) -> tuple[DumpFrame, int]:
    _require_line(lines, cursor, "ITEM: TIMESTEP")
    timestep_line = lines[cursor + 1]
    timestep = parse_int(
        timestep_line.text,
        line_number=timestep_line.number,
        name="timestep",
    )
    _require_line(lines, cursor + 2, "ITEM: NUMBER OF ATOMS")
    atom_count_line = lines[cursor + 3]
    atom_count = parse_int(
        atom_count_line.text,
        line_number=atom_count_line.number,
        name="atom count",
    )
    box, after_box = parse_dump_box(lines=lines, cursor=cursor + 4)
    atoms_line = lines[after_box]
    if not atoms_line.text.startswith("ITEM: ATOMS"):
        raise LammpsParseError(
            line_number=atoms_line.number,
            reason="missing ITEM: ATOMS",
        )
    columns = tuple(atoms_line.text.split()[2:])
    row_start = after_box + 1
    row_end = row_start + atom_count
    if row_end > len(lines):
        raise LammpsParseError(
            line_number=atoms_line.number,
            reason="truncated atom rows",
        )
    rows = tuple(tuple(line.text.split()) for line in lines[row_start:row_end])
    return (
        DumpFrame(
            number=number,
            timestep=timestep,
            box=box,
            columns=columns,
            rows=rows,
        ),
        row_end,
    )


def _frame_to_snapshot(
    *,
    frame: DumpFrame,
    topology: LammpsTopology | None,
) -> Snapshot:
    id_column = _column_index(frame.columns, "id")
    coordinate_columns = _coordinate_columns(frame.columns)
    positions = _positions_by_id(
        frame=frame,
        id_column=id_column,
        coordinates=coordinate_columns,
    )
    if topology is None:
        chains = _chains_from_sorted_dump(frame=frame, positions=positions)
    else:
        chains = tuple(
            Chain(nodes=tuple(positions[atom_id] for atom_id in chain))
            for chain in topology.chains
        )
    return Snapshot(
        chains=chains,
        box=frame.box.lengths,
        label=frame.timestep,
        shear=frame.box.shear,
    )


def _positions_by_id(
    *,
    frame: DumpFrame,
    id_column: int,
    coordinates: CoordinateColumns,
) -> dict[int, Vector3]:
    positions: dict[int, Vector3] = {}
    for row in frame.rows:
        atom_id = parse_int(row[id_column], line_number=0, name="atom id")
        x = parse_float(row[coordinates.x], line_number=0, name="x")
        y = parse_float(row[coordinates.y], line_number=0, name="y")
        z = parse_float(row[coordinates.z], line_number=0, name="z")
        if coordinates.scaled:
            x *= frame.box.lengths.x
            y *= frame.box.lengths.y
            z *= frame.box.lengths.z
        positions[atom_id] = Vector3(x, y, z)
    return positions


def _chains_from_sorted_dump(
    *,
    frame: DumpFrame,
    positions: dict[int, Vector3],
) -> tuple[Chain, ...]:
    molecule_column = _column_index(frame.columns, "mol")
    chains: list[Chain] = []
    current_molecule = None
    current_nodes: list[Vector3] = []
    id_column = _column_index(frame.columns, "id")
    for expected_id, row in enumerate(frame.rows, start=1):
        atom_id = parse_int(row[id_column], line_number=0, name="atom id")
        if atom_id != expected_id:
            raise LammpsParseError(
                line_number=0,
                reason="dump atoms must be sorted by id",
            )
        molecule_id = parse_int(
            row[molecule_column],
            line_number=0,
            name="molecule id",
        )
        if current_molecule is None:
            current_molecule = molecule_id
        if molecule_id != current_molecule:
            chains.append(Chain(nodes=tuple(current_nodes)))
            current_nodes = []
            current_molecule = molecule_id
        current_nodes.append(positions[atom_id])
    if current_nodes:
        chains.append(Chain(nodes=tuple(current_nodes)))
    return tuple(chains)


def _coordinate_columns(columns: tuple[str, ...]) -> CoordinateColumns:
    if all(column in columns for column in ("xs", "ys", "zs")):
        return CoordinateColumns(
            x=_column_index(columns, "xs"),
            y=_column_index(columns, "ys"),
            z=_column_index(columns, "zs"),
            scaled=True,
        )
    if all(column in columns for column in ("xu", "yu", "zu")):
        return CoordinateColumns(
            x=_column_index(columns, "xu"),
            y=_column_index(columns, "yu"),
            z=_column_index(columns, "zu"),
            scaled=False,
        )
    return CoordinateColumns(
        x=_column_index(columns, "x"),
        y=_column_index(columns, "y"),
        z=_column_index(columns, "z"),
        scaled=False,
    )


def _column_index(columns: tuple[str, ...], name: str) -> int:
    try:
        return columns.index(name)
    except ValueError as exc:
        raise LammpsParseError(
            line_number=0,
            reason=f"missing dump column {name}",
        ) from exc


def _require_line(lines: tuple[ParsedLine, ...], index: int, expected: str) -> None:
    if index >= len(lines) or lines[index].text != expected:
        line_number = lines[index].number if index < len(lines) else 0
        raise LammpsParseError(line_number=line_number, reason=f"expected {expected}")
