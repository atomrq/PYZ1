from __future__ import annotations

from math import isclose
from pathlib import Path

import pytest

from pyz1.errors import InvalidSnapshotError
from pyz1.estimators import (
    PrimitivePathInput,
    compute_primitive_path_statistics,
)
from pyz1.output_io import read_summary_file
from pyz1.output_values import read_float_values_file, read_int_values_file

FIXTURE_ROOT = Path("tests/fixtures/z1plus_oracle/benchmark-04/basic")
FLOAT_TOLERANCE = 1.0e-3


def assert_close(actual: float, expected: float) -> None:
    assert isclose(actual, expected, rel_tol=FLOAT_TOLERANCE, abs_tol=FLOAT_TOLERANCE)


def test_primitive_path_statistics_match_benchmark_04_summary_oracle() -> None:
    summary = read_summary_file(FIXTURE_ROOT / "Z1+summary.dat")[0]
    data = PrimitivePathInput(
        original_chain_lengths=read_int_values_file(FIXTURE_ROOT / "N_values.dat"),
        end_to_end_distances=read_float_values_file(FIXTURE_ROOT / "Ree_values.dat"),
        shortest_path_contours=read_float_values_file(FIXTURE_ROOT / "Lpp_values.dat"),
        entanglement_counts=read_int_values_file(FIXTURE_ROOT / "Z_values.dat"),
    )

    stats = compute_primitive_path_statistics(data)

    assert_close(stats.mean_shortest_path_contour, summary.mean_shortest_path_contour)
    assert_close(stats.mean_entanglements, summary.mean_entanglements)
    assert_close(stats.coil_tube_diameter, summary.coil_tube_diameter)
    assert_close(stats.coil_tube_step_length, summary.coil_tube_step_length)
    assert_close(stats.root_mean_squared_contour, summary.root_mean_squared_contour)
    assert_close(stats.ne_classical_kink, summary.ne_classical_kink)
    assert_close(stats.ne_modified_kink, summary.ne_modified_kink)
    assert_close(stats.ne_classical_coil, summary.ne_classical_coil)
    assert_close(stats.ne_modified_coil, summary.ne_modified_coil)


def test_primitive_path_statistics_when_zero_kinks_uses_sentinel() -> None:
    data = PrimitivePathInput(
        original_chain_lengths=(3, 3),
        end_to_end_distances=(2.0, 2.0),
        shortest_path_contours=(2.0, 2.0),
        entanglement_counts=(0, 0),
    )

    stats = compute_primitive_path_statistics(data)

    assert stats.mean_entanglements == 0.0
    assert stats.ne_classical_kink == -1.0
    assert stats.ne_modified_kink == -1.0
    assert stats.ne_classical_coil == 2.0
    assert stats.ne_modified_coil == -1.0


def test_primitive_path_statistics_rejects_mismatched_series() -> None:
    data = PrimitivePathInput(
        original_chain_lengths=(3, 3),
        end_to_end_distances=(2.0,),
        shortest_path_contours=(2.0, 2.0),
        entanglement_counts=(0, 0),
    )

    with pytest.raises(InvalidSnapshotError, match="same number of chains"):
        _ = compute_primitive_path_statistics(data)
