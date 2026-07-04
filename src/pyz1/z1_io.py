from __future__ import annotations

from typing import TYPE_CHECKING, Final

from pyz1.errors import Z1ParseError
from pyz1.models import Chain, Snapshot, Vector3

if TYPE_CHECKING:
    from pathlib import Path

HEADER_LINE_COUNT: Final = 3
METADATA_LINE_COUNT: Final = 3
SHEAR_SENTINEL: Final = "-1"
VECTOR_FIELD_COUNT: Final = 3


def read_z1_file(path: Path) -> Snapshot:
    return parse_z1_text(path.read_text(encoding="utf-8"))


def parse_z1_text(text: str) -> Snapshot:
    lines = _meaningful_lines(text)
    if len(lines) < HEADER_LINE_COUNT:
        raise Z1ParseError(line_number=len(lines) + 1, reason="expected 3 header lines")

    chain_count = _parse_positive_int(lines[0], line_number=1, name="chain count")
    box = _parse_vector3(lines[1], line_number=2)
    chain_lengths = _parse_chain_lengths(lines[2], chain_count=chain_count)
    coordinate_start = HEADER_LINE_COUNT
    coordinate_count = sum(chain_lengths)
    coordinate_lines = lines[coordinate_start : coordinate_start + coordinate_count]
    if len(coordinate_lines) != coordinate_count:
        raise Z1ParseError(
            line_number=len(lines),
            reason=f"expected {coordinate_count} coordinate rows",
        )

    coordinates = tuple(
        _parse_vector3(raw, line_number=coordinate_start + index + 1)
        for index, raw in enumerate(coordinate_lines)
    )
    chains = _build_chains(coordinates=coordinates, chain_lengths=chain_lengths)
    metadata = lines[coordinate_start + coordinate_count :]
    label, shear = _parse_optional_metadata(metadata, first_line=coordinate_count + 4)
    return Snapshot(chains=chains, box=box, label=label, shear=shear)


def write_z1_text(snapshot: Snapshot) -> str:
    lines: list[str] = [
        str(snapshot.chain_count),
        _format_vector3(snapshot.box),
        " ".join(str(chain.node_count) for chain in snapshot.chains),
    ]
    for chain in snapshot.chains:
        lines.extend(_format_vector3(node) for node in chain.nodes)
    if snapshot.label is not None or snapshot.shear is not None:
        lines.append(SHEAR_SENTINEL)
        lines.append(str(snapshot.label if snapshot.label is not None else 0))
        shear = snapshot.shear if snapshot.shear is not None else 0.0
        lines.append(_format_float(shear))
    return "\n".join(lines) + "\n"


def _meaningful_lines(text: str) -> tuple[str, ...]:
    return tuple(line.strip() for line in text.splitlines() if line.strip())


def _parse_positive_int(raw: str, *, line_number: int, name: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise Z1ParseError(line_number=line_number, reason=f"invalid {name}") from exc
    if value <= 0:
        raise Z1ParseError(line_number=line_number, reason=f"{name} must be positive")
    return value


def _parse_vector3(raw: str, *, line_number: int) -> Vector3:
    fields = raw.split()
    if len(fields) != VECTOR_FIELD_COUNT:
        raise Z1ParseError(line_number=line_number, reason="expected three floats")
    try:
        return Vector3(float(fields[0]), float(fields[1]), float(fields[2]))
    except ValueError as exc:
        raise Z1ParseError(line_number=line_number, reason="invalid float") from exc


def _parse_chain_lengths(raw: str, *, chain_count: int) -> tuple[int, ...]:
    fields = raw.split()
    if len(fields) == 1 and "*" in fields[0]:
        repeat_raw, length_raw = fields[0].split("*", maxsplit=1)
        repeat = _parse_positive_int(repeat_raw, line_number=3, name="repeat count")
        length = _parse_positive_int(length_raw, line_number=3, name="chain length")
        lengths = (length,) * repeat
    else:
        lengths = tuple(
            _parse_positive_int(field, line_number=3, name="chain length")
            for field in fields
        )
    if len(lengths) != chain_count:
        raise Z1ParseError(
            line_number=3,
            reason=f"expected {chain_count} chain lengths, got {len(lengths)}",
        )
    return lengths


def _build_chains(
    *,
    coordinates: tuple[Vector3, ...],
    chain_lengths: tuple[int, ...],
) -> tuple[Chain, ...]:
    chains: list[Chain] = []
    cursor = 0
    for length in chain_lengths:
        next_cursor = cursor + length
        chains.append(Chain(nodes=coordinates[cursor:next_cursor]))
        cursor = next_cursor
    return tuple(chains)


def _parse_optional_metadata(
    metadata: tuple[str, ...],
    *,
    first_line: int,
) -> tuple[int | None, float | None]:
    if len(metadata) == 0:
        return None, None
    if len(metadata) != METADATA_LINE_COUNT:
        raise Z1ParseError(line_number=first_line, reason="unexpected trailing lines")
    if metadata[0] != SHEAR_SENTINEL:
        raise Z1ParseError(line_number=first_line, reason="invalid metadata sentinel")
    label = _parse_positive_or_zero_int(metadata[1], line_number=first_line + 1)
    try:
        shear = float(metadata[2])
    except ValueError as exc:
        raise Z1ParseError(line_number=first_line + 2, reason="invalid shear") from exc
    return label, shear


def _parse_positive_or_zero_int(raw: str, *, line_number: int) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise Z1ParseError(line_number=line_number, reason="invalid label") from exc
    if value < 0:
        raise Z1ParseError(line_number=line_number, reason="label must be non-negative")
    return value


def _format_vector3(vector: Vector3) -> str:
    return " ".join(_format_float(value) for value in vector.as_tuple())


def _format_float(value: float) -> str:
    return format(value, ".17g")
