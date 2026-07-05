from __future__ import annotations

from os import environ
from pathlib import Path
from typing import Final

import pytest

from pyz1.z1_io import parse_z1_text, read_z1_file, write_z1_text

SOURCE_Z1 = Path(
    environ.get(
        "PYZ1_SOURCE_Z1",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1+",
    ),
)
NEWLINE: Final = "\n"


def test_parse_benchmark_04_snapshot() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")

    assert snapshot.chain_count == 5
    assert snapshot.node_count == 50
    assert snapshot.true_chain_count == 5
    assert snapshot.true_chain_lengths == (10, 10, 10, 10, 10)
    assert snapshot.box.as_tuple() == (10.0, 10.0, 10.0)
    assert snapshot.chains[0].nodes[0].as_tuple() == (0.27934, 0.72293, 0.91668)


def test_parse_monodisperse_chain_count_syntax() -> None:
    lines = (
        "2",
        "5 5 5",
        "2*3",
        "0 0 0",
        "1 0 0",
        "2 0 0",
        "0 1 0",
        "1 1 0",
        "2 1 0",
    )
    snapshot = parse_z1_text(
        NEWLINE.join(lines),
    )

    assert snapshot.chain_count == 2
    assert snapshot.true_chain_lengths == (3, 3)


def test_write_round_trip_preserves_benchmark_structure() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")
    reparsed = parse_z1_text(write_z1_text(snapshot))

    assert reparsed == snapshot


def test_truncated_input_reports_line_context() -> None:
    with pytest.raises(ValueError, match="expected 6 coordinate rows"):
        _ = parse_z1_text("2\n5 5 5\n3 3\n0 0 0")
