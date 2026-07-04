from __future__ import annotations

from typing import TYPE_CHECKING

from pyz1.errors import Z1OutputParseError

if TYPE_CHECKING:
    from pathlib import Path


def read_float_values_file(path: Path) -> tuple[float, ...]:
    return parse_float_values_text(path.read_text(encoding="utf-8"))


def parse_float_values_text(text: str) -> tuple[float, ...]:
    values: list[float] = []
    for line_number, raw in _tokens_with_line_numbers(text):
        try:
            values.append(float(raw))
        except ValueError as exc:
            raise Z1OutputParseError(
                line_number=line_number,
                reason="invalid float value",
            ) from exc
    return tuple(values)


def write_float_values_file(path: Path, values: tuple[float, ...]) -> None:
    _ = path.write_text(format_float_values_text(values), encoding="utf-8")


def format_float_values_text(values: tuple[float, ...]) -> str:
    if len(values) == 0:
        return ""
    return "\n".join(format(value, ".15g") for value in values) + "\n"


def read_int_values_file(path: Path) -> tuple[int, ...]:
    return parse_int_values_text(path.read_text(encoding="utf-8"))


def parse_int_values_text(text: str) -> tuple[int, ...]:
    values: list[int] = []
    for line_number, raw in _tokens_with_line_numbers(text):
        try:
            values.append(int(raw))
        except ValueError as exc:
            raise Z1OutputParseError(
                line_number=line_number,
                reason="invalid integer value",
            ) from exc
    return tuple(values)


def write_int_values_file(path: Path, values: tuple[int, ...]) -> None:
    _ = path.write_text(format_int_values_text(values), encoding="utf-8")


def format_int_values_text(values: tuple[int, ...]) -> str:
    if len(values) == 0:
        return ""
    return "\n".join(str(value) for value in values) + "\n"


def _tokens_with_line_numbers(text: str) -> tuple[tuple[int, str], ...]:
    pairs: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        pairs.extend((line_number, token) for token in line.split())
    return tuple(pairs)
