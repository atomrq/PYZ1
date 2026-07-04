from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, unique
from typing import Final

from pyz1.errors import LammpsParseError
from pyz1.models import Vector3

COMMENT_MARKER: Final = "#"
VECTOR_FIELD_COUNT: Final = 3


@unique
class LammpsDataSection(StrEnum):
    MASSES = "Masses"
    ATOMS = "Atoms"
    BONDS = "Bonds"


@dataclass(frozen=True, slots=True)
class ParsedLine:
    number: int
    text: str


@dataclass(frozen=True, slots=True)
class LammpsBox:
    low: Vector3
    high: Vector3
    shear: float | None

    @property
    def lengths(self) -> Vector3:
        return Vector3(
            self.high.x - self.low.x,
            self.high.y - self.low.y,
            self.high.z - self.low.z,
        )


def meaningful_lines(text: str) -> tuple[ParsedLine, ...]:
    lines: list[ParsedLine] = []
    for index, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.split(COMMENT_MARKER, maxsplit=1)[0].strip()
        if stripped:
            lines.append(ParsedLine(number=index, text=" ".join(stripped.split())))
    return tuple(lines)


def parse_int(raw: str, *, line_number: int, name: str) -> int:
    try:
        return int(raw)
    except ValueError as exc:
        raise LammpsParseError(
            line_number=line_number,
            reason=f"invalid {name}",
        ) from exc


def parse_float(raw: str, *, line_number: int, name: str) -> float:
    try:
        return float(raw)
    except ValueError as exc:
        raise LammpsParseError(
            line_number=line_number,
            reason=f"invalid {name}",
        ) from exc


def parse_vector3(fields: tuple[str, ...], *, line_number: int) -> Vector3:
    if len(fields) != VECTOR_FIELD_COUNT:
        raise LammpsParseError(line_number=line_number, reason="expected three floats")
    return Vector3(
        parse_float(fields[0], line_number=line_number, name="x"),
        parse_float(fields[1], line_number=line_number, name="y"),
        parse_float(fields[2], line_number=line_number, name="z"),
    )


def data_section_from_line(line: str) -> LammpsDataSection | None:
    first = line.split(maxsplit=1)[0]
    match first:
        case LammpsDataSection.MASSES.value:
            return LammpsDataSection.MASSES
        case LammpsDataSection.ATOMS.value:
            return LammpsDataSection.ATOMS
        case LammpsDataSection.BONDS.value:
            return LammpsDataSection.BONDS
        case _:
            return None
