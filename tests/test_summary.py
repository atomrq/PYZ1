from __future__ import annotations

from math import isclose
from os import environ
from pathlib import Path
from typing import TYPE_CHECKING

from pyz1.models import Chain, Snapshot, Vector3
from pyz1.output_io import read_shortest_path_file, read_summary_file
from pyz1.output_values import read_float_values_file, read_int_values_file
from pyz1.summary import (
    build_summary_outputs,
    build_summary_outputs_from_coordinate_path,
    write_summary_outputs,
)
from pyz1.z1_io import read_z1_file

if TYPE_CHECKING:
    from pyz1.output_models import Z1SummaryRecord

SOURCE_Z1 = Path(
    environ.get(
        "PYZ1_SOURCE_Z1",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1+",
    ),
)
FIXTURE_ROOT = Path("tests/fixtures/z1plus_oracle/benchmark-04/basic")
FLOAT_TOLERANCE = 1.0e-3


def assert_close(actual: float, expected: float) -> None:
    assert isclose(actual, expected, rel_tol=FLOAT_TOLERANCE, abs_tol=FLOAT_TOLERANCE)


def assert_float_values_close(
    actual: tuple[float, ...],
    expected: tuple[float, ...],
) -> None:
    assert len(actual) == len(expected)
    for actual_value, expected_value in zip(actual, expected, strict=True):
        assert_close(actual_value, expected_value)


def test_summary_outputs_match_benchmark_04_oracle() -> None:
    original = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")
    shortest_path = read_shortest_path_file(FIXTURE_ROOT / "Z1+SP.dat")
    expected = read_summary_file(FIXTURE_ROOT / "Z1+summary.dat")[0]

    outputs = build_summary_outputs(
        original=original,
        primitive_path=shortest_path,
        timestep=1,
    )

    assert outputs.n_values == read_int_values_file(FIXTURE_ROOT / "N_values.dat")
    assert outputs.z_values == read_int_values_file(FIXTURE_ROOT / "Z_values.dat")
    for actual, expected_ree in zip(
        outputs.ree_values,
        read_float_values_file(FIXTURE_ROOT / "Ree_values.dat"),
        strict=True,
    ):
        assert_close(actual, expected_ree)
    for actual, expected_lpp in zip(
        outputs.lpp_values,
        read_float_values_file(FIXTURE_ROOT / "Lpp_values.dat"),
        strict=True,
    ):
        assert_close(actual, expected_lpp)
    assert_summary_close(outputs.record, expected)


def test_summary_outputs_write_z1plus_files(tmp_path: Path) -> None:
    original = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")
    shortest_path = read_shortest_path_file(FIXTURE_ROOT / "Z1+SP.dat")
    outputs = build_summary_outputs(
        original=original,
        primitive_path=shortest_path,
        timestep=1,
    )

    write_summary_outputs(tmp_path, outputs)

    assert_summary_close(
        read_summary_file(tmp_path / "Z1+summary.dat")[0],
        outputs.record,
    )
    assert_float_values_close(
        read_float_values_file(tmp_path / "Ree_values.dat"),
        outputs.ree_values,
    )
    assert_float_values_close(
        read_float_values_file(tmp_path / "Lpp_values.dat"),
        outputs.lpp_values,
    )
    assert read_int_values_file(tmp_path / "N_values.dat") == outputs.n_values
    assert read_int_values_file(tmp_path / "Z_values.dat") == outputs.z_values


def test_summary_outputs_from_ppa_coordinate_path_use_z_sentinel() -> None:
    original = Snapshot(
        chains=(
            Chain(
                (
                    Vector3(0.0, 0.0, 0.0),
                    Vector3(1.0, 0.0, 0.0),
                    Vector3(2.0, 0.0, 0.0),
                ),
            ),
            Chain(
                (
                    Vector3(0.0, 1.0, 0.0),
                    Vector3(1.0, 1.0, 0.0),
                    Vector3(2.0, 1.0, 0.0),
                ),
            ),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )

    outputs = build_summary_outputs_from_coordinate_path(
        original=original,
        primitive_path=original,
        entanglement_counts=(-1, -1),
        timestep=7,
    )

    assert outputs.record.timestep == 7
    assert outputs.z_values == (-1, -1)
    assert outputs.record.mean_entanglements == -1.0
    assert outputs.record.ne_classical_kink == -1.0
    assert outputs.record.ne_modified_kink == -1.0
    assert outputs.record.ne_classical_coil == 2.0
    assert outputs.record.ne_modified_coil == -1.0


def assert_summary_close(actual: Z1SummaryRecord, expected: Z1SummaryRecord) -> None:
    assert actual.timestep == expected.timestep
    assert actual.true_chain_count == expected.true_chain_count
    assert_close(actual.mean_original_beads, expected.mean_original_beads)
    assert_close(actual.mean_squared_end_to_end, expected.mean_squared_end_to_end)
    assert_close(
        actual.mean_shortest_path_contour,
        expected.mean_shortest_path_contour,
    )
    assert_close(actual.mean_entanglements, expected.mean_entanglements)
    assert_close(actual.coil_tube_diameter, expected.coil_tube_diameter)
    assert_close(actual.coil_tube_step_length, expected.coil_tube_step_length)
    assert_close(actual.root_mean_squared_contour, expected.root_mean_squared_contour)
    assert_close(actual.ne_classical_kink, expected.ne_classical_kink)
    assert_close(actual.ne_modified_kink, expected.ne_modified_kink)
    assert_close(actual.ne_classical_coil, expected.ne_classical_coil)
    assert_close(actual.ne_modified_coil, expected.ne_modified_coil)
    assert_close(actual.mean_original_bond_length, expected.mean_original_bond_length)
    assert_close(actual.original_bead_density, expected.original_bead_density)
