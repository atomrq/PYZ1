from __future__ import annotations

from math import isclose
from os import environ
from pathlib import Path

from pyz1.estimators import compute_input_statistics
from pyz1.output_io import read_shortest_path_file, read_summary_file
from pyz1.z1_io import read_z1_file

SOURCE_Z1 = Path(
    environ.get(
        "PYZ1_SOURCE_Z1",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1+",
    ),
)
ORACLE_ROOT = Path("tests/fixtures/z1plus_oracle/benchmark-04")
FLOAT_TOLERANCE = 1.0e-3


def assert_close(actual: float, expected: float) -> None:
    assert isclose(actual, expected, rel_tol=FLOAT_TOLERANCE, abs_tol=FLOAT_TOLERANCE)


def test_benchmark_04_input_statistics_match_z1plus_summary_oracle() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")
    stats = compute_input_statistics(snapshot)
    summary = read_summary_file(ORACLE_ROOT / "basic" / "Z1+summary.dat")[0]

    assert stats.true_chain_count == summary.true_chain_count
    assert_close(stats.mean_original_beads, summary.mean_original_beads)
    assert_close(stats.root_mean_squared_end_to_end, summary.mean_squared_end_to_end)
    assert_close(stats.mean_original_bond_length, summary.mean_original_bond_length)
    assert_close(stats.original_bead_density, summary.original_bead_density)


def test_benchmark_04_sp_oracle_structure_matches_summary() -> None:
    summary = read_summary_file(ORACLE_ROOT / "basic" / "Z1+summary.dat")[0]
    shortest_paths = read_shortest_path_file(ORACLE_ROOT / "basic" / "Z1+SP.dat")

    assert shortest_paths.chain_count == summary.true_chain_count
    entanglements = sum(
        node.is_entanglement
        for chain in shortest_paths.chains
        for node in chain.nodes
    )
    assert entanglements == 1
    assert tuple(chain.node_count for chain in shortest_paths.chains) == (3, 2, 2, 2, 2)


def test_benchmark_04_spplus_oracle_retains_pairing() -> None:
    shortest_paths = read_shortest_path_file(ORACLE_ROOT / "spplus" / "Z1+SP.dat")
    pairs = tuple(
        node.pair
        for chain in shortest_paths.chains
        for node in chain.nodes
        if node.pair is not None
    )

    assert len(pairs) == 1
    assert pairs[0].chain_index == 2
    assert pairs[0].node_index == 1
