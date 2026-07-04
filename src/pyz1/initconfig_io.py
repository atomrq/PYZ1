from __future__ import annotations

from typing import TYPE_CHECKING, Final

from pyz1.errors import Z1OutputParseError
from pyz1.models import Chain, Snapshot, Vector3

if TYPE_CHECKING:
    from pathlib import Path

HEADER_LINE_COUNT: Final = 2
METADATA_LINE_COUNT: Final = 2
SHEAR_SENTINEL: Final = "-1"
VECTOR_FIELD_COUNT: Final = 3


def read_init_config_file(path: Path) -> Snapshot:
    return parse_init_config_text(path.read_text(encoding="utf-8"))


def parse_init_config_text(text: str) -> Snapshot:
    lines = _meaningful_lines(text)
    if len(lines) < HEADER_LINE_COUNT:
        raise Z1OutputParseError(
            line_number=len(lines) + 1,
            reason="expected initconfig header",
        )
    chain_count = _parse_positive_int(lines[0], line_number=1, name="chain count")
    box = _parse_vector3(lines[1], line_number=2)
    chains: list[Chain] = []
    cursor = HEADER_LINE_COUNT
    for _ in range(chain_count):
        if cursor >= len(lines):
            raise Z1OutputParseError(
                line_number=cursor + 1,
                reason="expected chain size",
            )
        node_count = _parse_positive_int(
            lines[cursor],
            line_number=cursor + 1,
            name="chain size",
        )
        cursor += 1
        nodes = _parse_chain_nodes(
            lines=lines,
            cursor=cursor,
            node_count=node_count,
        )
        chains.append(Chain(nodes=nodes))
        cursor += node_count
    label, shear = _parse_optional_metadata(lines[cursor:], first_line=cursor + 1)
    if label is None and shear is None and cursor != len(lines):
        raise Z1OutputParseError(
            line_number=cursor + 1,
            reason="unexpected trailing initconfig rows",
        )
    return Snapshot(chains=tuple(chains), box=box, label=label, shear=shear)


def write_init_config_file(path: Path, snapshot: Snapshot) -> None:
    _ = path.write_text(format_init_config_text(snapshot), encoding="utf-8")


def format_init_config_text(snapshot: Snapshot) -> str:
    lines: list[str] = [str(snapshot.chain_count), _format_vector3(snapshot.box)]
    for chain in snapshot.chains:
        lines.append(str(chain.node_count))
        lines.extend(_format_vector3(node) for node in chain.nodes)
    if snapshot.shear is not None:
        lines.append(SHEAR_SENTINEL)
        lines.append(format(snapshot.shear, ".17g"))
    return "\n".join(lines) + "\n"


def _parse_chain_nodes(
    *,
    lines: tuple[str, ...],
    cursor: int,
    node_count: int,
) -> tuple[Vector3, ...]:
    coordinate_lines = lines[cursor : cursor + node_count]
    if len(coordinate_lines) != node_count:
        raise Z1OutputParseError(
            line_number=len(lines),
            reason=f"expected {node_count} coordinate rows",
        )
    return tuple(
        _parse_vector3(raw, line_number=cursor + index + 1)
        for index, raw in enumerate(coordinate_lines)
    )


def _meaningful_lines(text: str) -> tuple[str, ...]:
    return tuple(line.strip() for line in text.splitlines() if line.strip())


def _parse_optional_metadata(
    metadata: tuple[str, ...],
    *,
    first_line: int,
) -> tuple[None, float | None]:
    if len(metadata) == 0:
        return None, None
    if len(metadata) != METADATA_LINE_COUNT:
        raise Z1OutputParseError(
            line_number=first_line,
            reason="unexpected trailing initconfig rows",
        )
    if metadata[0] != SHEAR_SENTINEL:
        raise Z1OutputParseError(
            line_number=first_line,
            reason="invalid initconfig metadata sentinel",
        )
    try:
        return None, float(metadata[1])
    except ValueError as exc:
        raise Z1OutputParseError(
            line_number=first_line + 1,
            reason="invalid shear",
        ) from exc


def _parse_positive_int(raw: str, *, line_number: int, name: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise Z1OutputParseError(
            line_number=line_number,
            reason=f"invalid {name}",
        ) from exc
    if value <= 0:
        raise Z1OutputParseError(
            line_number=line_number,
            reason=f"{name} must be positive",
        )
    return value


def _parse_vector3(raw: str, *, line_number: int) -> Vector3:
    fields = raw.split()
    if len(fields) != VECTOR_FIELD_COUNT:
        raise Z1OutputParseError(
            line_number=line_number,
            reason="expected three floats",
        )
    try:
        return Vector3(float(fields[0]), float(fields[1]), float(fields[2]))
    except ValueError as exc:
        raise Z1OutputParseError(
            line_number=line_number,
            reason="invalid float",
        ) from exc


def _format_vector3(vector: Vector3) -> str:
    return " ".join(format(value, ".17g") for value in vector.as_tuple())
