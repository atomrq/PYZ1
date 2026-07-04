from __future__ import annotations

from pathlib import Path

import pytest

from pyz1.output_values import (
    format_float_values_text,
    format_int_values_text,
    parse_float_values_text,
    parse_int_values_text,
    read_float_values_file,
    read_int_values_file,
    write_float_values_file,
    write_int_values_file,
)

FIXTURE_ROOT = Path("tests/fixtures/z1plus_oracle/benchmark-04/basic")


def test_float_values_when_benchmark_04_oracle_round_trips(tmp_path: Path) -> None:
    values = read_float_values_file(FIXTURE_ROOT / "Ree_values.dat")
    path = tmp_path / "Ree_values.dat"

    text = format_float_values_text(values)
    write_float_values_file(path, values)

    assert values == (
        5.23526479529928,
        1.20101993263601,
        6.27755232901328,
        5.02852934652867,
        3.27159015998337,
    )
    assert text.endswith("\n")
    assert read_float_values_file(path) == values


def test_int_values_when_benchmark_04_oracle_round_trips(tmp_path: Path) -> None:
    values = read_int_values_file(FIXTURE_ROOT / "Z_values.dat")
    path = tmp_path / "Z_values.dat"

    text = format_int_values_text(values)
    write_int_values_file(path, values)

    assert values == (1, 0, 0, 0, 0)
    assert text.endswith("\n")
    assert read_int_values_file(path) == values


def test_value_parser_accepts_whitespace_columns() -> None:
    assert parse_float_values_text("1.5 2.5\n3.5\n") == (1.5, 2.5, 3.5)
    assert parse_int_values_text("1 2\n3\n") == (1, 2, 3)


def test_malformed_value_reports_line_context() -> None:
    with pytest.raises(ValueError, match="invalid float value"):
        _ = parse_float_values_text("1.0\nbad\n")

