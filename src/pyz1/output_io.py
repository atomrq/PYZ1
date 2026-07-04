from __future__ import annotations

from math import nan
from typing import TYPE_CHECKING, Final

from pyz1 import output_write
from pyz1.errors import Z1OutputParseError
from pyz1.models import Vector3
from pyz1.output_models import (
    ShortestPathChain,
    ShortestPathNode,
    ShortestPathPair,
    ShortestPathSnapshot,
    Z1SummaryRecord,
)

if TYPE_CHECKING:
    from pathlib import Path

SUMMARY_COLUMN_COUNT: Final = 15
SP_HEADER_LINE_COUNT: Final = 2
SP_NODE_COLUMN_COUNT: Final = 5
SPPLUS_NODE_COLUMN_COUNT: Final = 7
VECTOR_FIELD_COUNT: Final = 3
FORTRAN_OVERFLOW_TOKEN: Final = "************"  # noqa: S105 - Fortran overflow.


def read_summary_file(path: Path) -> tuple[Z1SummaryRecord, ...]:
    return parse_summary_text(path.read_text(encoding="utf-8"))


def write_summary_file(path: Path, records: tuple[Z1SummaryRecord, ...]) -> None:
    output_write.write_summary_file(path, records)


def format_summary_text(records: tuple[Z1SummaryRecord, ...]) -> str:
    return output_write.format_summary_text(records)


def parse_summary_text(text: str) -> tuple[Z1SummaryRecord, ...]:
    records: list[Z1SummaryRecord] = []
    for index, raw in enumerate(_meaningful_lines(text), start=1):
        records.append(_parse_summary_record(raw.split(), line_number=index))
    return tuple(records)


def read_shortest_path_file(path: Path) -> ShortestPathSnapshot:
    return parse_shortest_path_text(path.read_text(encoding="utf-8"))


def write_shortest_path_file(path: Path, snapshot: ShortestPathSnapshot) -> None:
    output_write.write_shortest_path_file(path, snapshot)


def format_shortest_path_text(snapshot: ShortestPathSnapshot) -> str:
    return output_write.format_shortest_path_text(snapshot)


def parse_shortest_path_text(text: str) -> ShortestPathSnapshot:
    lines = _meaningful_lines(text)
    if len(lines) < SP_HEADER_LINE_COUNT:
        raise Z1OutputParseError(
            line_number=len(lines) + 1,
            reason="expected SP header",
        )

    chain_count = _parse_positive_int(lines[0], line_number=1, name="chain count")
    box = _parse_vector3(lines[1], line_number=2)
    chains: list[ShortestPathChain] = []
    cursor = SP_HEADER_LINE_COUNT
    for _ in range(chain_count):
        if cursor >= len(lines):
            raise Z1OutputParseError(
                line_number=cursor + 1,
                reason="expected SP chain size",
            )
        node_count = _parse_positive_int(
            lines[cursor],
            line_number=cursor + 1,
            name="SP node count",
        )
        cursor += 1
        nodes: list[ShortestPathNode] = []
        for _ in range(node_count):
            if cursor >= len(lines):
                raise Z1OutputParseError(
                    line_number=cursor + 1,
                    reason="expected SP node row",
                )
            nodes.append(_parse_sp_node(lines[cursor], line_number=cursor + 1))
            cursor += 1
        chains.append(ShortestPathChain(nodes=tuple(nodes)))
    if cursor != len(lines):
        raise Z1OutputParseError(
            line_number=cursor + 1,
            reason="unexpected trailing SP rows",
        )
    return ShortestPathSnapshot(chains=tuple(chains), box=box)


def _meaningful_lines(text: str) -> tuple[str, ...]:
    return tuple(line.strip() for line in text.splitlines() if line.strip())


def _parse_summary_record(fields: list[str], *, line_number: int) -> Z1SummaryRecord:
    if len(fields) != SUMMARY_COLUMN_COUNT:
        raise Z1OutputParseError(
            line_number=line_number,
            reason=f"expected 15 summary columns, got {len(fields)}",
        )
    return Z1SummaryRecord(
        timestep=_parse_int(fields[0], line_number=line_number, name="timestep"),
        true_chain_count=_parse_int(
            fields[1],
            line_number=line_number,
            name="true chain count",
        ),
        mean_original_beads=_parse_float(
            fields[2],
            line_number=line_number,
            name="mean original beads",
        ),
        mean_squared_end_to_end=_parse_float(
            fields[3],
            line_number=line_number,
            name="mean squared end-to-end distance",
        ),
        mean_shortest_path_contour=_parse_float(
            fields[4],
            line_number=line_number,
            name="mean shortest path contour",
        ),
        mean_entanglements=_parse_float(
            fields[5],
            line_number=line_number,
            name="mean entanglements",
        ),
        coil_tube_diameter=_parse_float(
            fields[6],
            line_number=line_number,
            name="coil tube diameter",
        ),
        coil_tube_step_length=_parse_float(
            fields[7],
            line_number=line_number,
            name="coil tube step length",
        ),
        root_mean_squared_contour=_parse_float(
            fields[8],
            line_number=line_number,
            name="root mean squared contour",
        ),
        ne_classical_kink=_parse_float(
            fields[9],
            line_number=line_number,
            name="classical kink Ne",
        ),
        ne_modified_kink=_parse_float(
            fields[10],
            line_number=line_number,
            name="modified kink Ne",
        ),
        ne_classical_coil=_parse_float(
            fields[11],
            line_number=line_number,
            name="classical coil Ne",
        ),
        ne_modified_coil=_parse_float(
            fields[12],
            line_number=line_number,
            name="modified coil Ne",
        ),
        mean_original_bond_length=_parse_float(
            fields[13],
            line_number=line_number,
            name="mean original bond length",
        ),
        original_bead_density=_parse_float(
            fields[14],
            line_number=line_number,
            name="original bead density",
        ),
    )


def _parse_sp_node(raw: str, *, line_number: int) -> ShortestPathNode:
    fields = raw.split()
    if len(fields) not in (SP_NODE_COLUMN_COUNT, SPPLUS_NODE_COLUMN_COUNT):
        raise Z1OutputParseError(
            line_number=line_number,
            reason=f"expected 5 or 7 SP node columns, got {len(fields)}",
        )
    pair = None
    if len(fields) == SPPLUS_NODE_COLUMN_COUNT:
        pair = ShortestPathPair(
            chain_index=_parse_int(
                fields[5],
                line_number=line_number,
                name="pair chain",
            ),
            node_index=_parse_int(fields[6], line_number=line_number, name="pair node"),
        )
    return ShortestPathNode(
        position=Vector3(
            _parse_float(fields[0], line_number=line_number, name="x"),
            _parse_float(fields[1], line_number=line_number, name="y"),
            _parse_float(fields[2], line_number=line_number, name="z"),
        ),
        source_bead=_parse_float(
            fields[3],
            line_number=line_number,
            name="source bead",
        ),
        is_entanglement=_parse_entanglement(fields[4], line_number=line_number),
        pair=pair,
    )


def _parse_vector3(raw: str, *, line_number: int) -> Vector3:
    fields = raw.split()
    if len(fields) != VECTOR_FIELD_COUNT:
        raise Z1OutputParseError(
            line_number=line_number,
            reason="expected three floats",
        )
    return Vector3(
        _parse_float(fields[0], line_number=line_number, name="x"),
        _parse_float(fields[1], line_number=line_number, name="y"),
        _parse_float(fields[2], line_number=line_number, name="z"),
    )


def _parse_positive_int(raw: str, *, line_number: int, name: str) -> int:
    value = _parse_int(raw, line_number=line_number, name=name)
    if value <= 0:
        raise Z1OutputParseError(
            line_number=line_number,
            reason=f"{name} must be positive",
        )
    return value


def _parse_entanglement(raw: str, *, line_number: int) -> bool:
    value = _parse_int(raw, line_number=line_number, name="entanglement flag")
    if value not in (0, 1):
        raise Z1OutputParseError(
            line_number=line_number,
            reason="entanglement flag must be 0 or 1",
        )
    return value == 1


def _parse_int(raw: str, *, line_number: int, name: str) -> int:
    try:
        return int(raw)
    except ValueError as exc:
        raise Z1OutputParseError(
            line_number=line_number,
            reason=f"invalid {name}",
        ) from exc


def _parse_float(raw: str, *, line_number: int, name: str) -> float:
    if raw == FORTRAN_OVERFLOW_TOKEN:
        return nan
    try:
        return float(raw)
    except ValueError as exc:
        raise Z1OutputParseError(
            line_number=line_number,
            reason=f"invalid {name}",
        ) from exc
