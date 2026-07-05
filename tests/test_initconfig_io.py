from __future__ import annotations

from math import isclose
from os import environ
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from pyz1.initconfig_io import (
    format_init_config_text,
    parse_init_config_text,
    read_init_config_file,
    write_init_config_file,
)
from pyz1.z1_io import read_z1_file

if TYPE_CHECKING:
    from pyz1.models import Snapshot, Vector3

FIXTURE_ROOT = Path("tests/fixtures/z1plus_oracle/benchmark-04/basic")
PPA_FIXTURE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703")
SOURCE_Z1 = Path(
    environ.get(
        "PYZ1_SOURCE_Z1",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1+",
    ),
)
FLOAT_TOLERANCE = 1.0e-12


def test_init_config_when_benchmark_04_oracle_matches_source_snapshot() -> None:
    init_snapshot = read_init_config_file(FIXTURE_ROOT / "Z1+initconfig.dat")
    source_snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")

    assert_snapshot_geometry_close(init_snapshot, source_snapshot)
    assert init_snapshot.label is None
    assert init_snapshot.shear == 0.0


def test_init_config_when_formatted_round_trips(tmp_path: Path) -> None:
    snapshot = read_init_config_file(FIXTURE_ROOT / "Z1+initconfig.dat")
    path = tmp_path / "Z1+initconfig.dat"

    text = format_init_config_text(snapshot)
    write_init_config_file(path, snapshot)

    assert text.startswith("5\n10")
    assert parse_init_config_text(text) == snapshot
    assert read_init_config_file(path) == snapshot


def test_ppa_coordinate_outputs_when_benchmark_04_oracle_round_trip() -> None:
    ppa_snapshot = read_init_config_file(
        PPA_FIXTURE_ROOT / "benchmark-04" / "ppa" / "PPA.dat",
    )
    ppaplus_snapshot = read_init_config_file(
        PPA_FIXTURE_ROOT / "benchmark-04" / "ppaplus" / "PPA+.dat",
    )

    assert ppa_snapshot.chain_count == 5
    assert ppaplus_snapshot.chain_count == 5
    assert tuple(chain.node_count for chain in ppa_snapshot.chains) == (
        10,
        10,
        10,
        10,
        10,
    )
    assert parse_init_config_text(format_init_config_text(ppa_snapshot)) == ppa_snapshot
    assert parse_init_config_text(format_init_config_text(ppaplus_snapshot)) == (
        ppaplus_snapshot
    )


def test_init_config_when_truncated_reports_line_context() -> None:
    with pytest.raises(ValueError, match="expected chain size"):
        _ = parse_init_config_text("1\n10 10 10\n")


def assert_snapshot_geometry_close(actual: Snapshot, expected: Snapshot) -> None:
    assert actual.chain_count == expected.chain_count
    assert_vector_close(actual.box, expected.box)
    for actual_chain, expected_chain in zip(
        actual.chains,
        expected.chains,
        strict=True,
    ):
        assert actual_chain.node_count == expected_chain.node_count
        for actual_node, expected_node in zip(
            actual_chain.nodes,
            expected_chain.nodes,
            strict=True,
        ):
            assert_vector_close(actual_node, expected_node)


def assert_vector_close(actual: Vector3, expected: Vector3) -> None:
    assert isclose(actual.x, expected.x, abs_tol=FLOAT_TOLERANCE)
    assert isclose(actual.y, expected.y, abs_tol=FLOAT_TOLERANCE)
    assert isclose(actual.z, expected.z, abs_tol=FLOAT_TOLERANCE)
