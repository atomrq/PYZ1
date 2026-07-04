from __future__ import annotations

from itertools import pairwise
from math import dist, isclose
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from pyz1.errors import Z1OutputParseError
from pyz1.initconfig_io import read_init_config_file
from pyz1.models import Chain, Snapshot, Vector3
from pyz1.output_io import read_summary_file
from pyz1.output_values import read_float_values_file, read_int_values_file
from pyz1.ppa import PpaMode, PpaPhase, PpaSettings, run_ppa, write_ppa_outputs
from pyz1.ppa_neighbors import PpaNeighborInput, neighbor_cells, wca_neighbor_pairs
from pyz1.ppa_summary import build_ppa_summary_outputs
from pyz1.ppa_vector import PpaVector
from pyz1.z1_io import read_z1_file

if TYPE_CHECKING:
    from pyz1.output_models import Z1SummaryRecord

SOURCE_Z1 = Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1+")
PPA_FIXTURE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703")
PPA_SUMMARY_ORACLE_CASES = (
    ("01", "ppa", "PPA.dat", "PPA-summary.dat"),
    ("01", "ppaplus", "PPA+.dat", "PPA+summary.dat"),
    ("04", "ppa", "PPA.dat", "PPA-summary.dat"),
    ("04", "ppaplus", "PPA+.dat", "PPA+summary.dat"),
    ("07", "ppa", "PPA.dat", "PPA-summary.dat"),
    ("07", "ppaplus", "PPA+.dat", "PPA+summary.dat"),
    ("10", "ppa", "PPA.dat", "PPA-summary.dat"),
    ("10", "ppaplus", "PPA+.dat", "PPA+summary.dat"),
    ("11", "ppa", "PPA.dat", "PPA-summary.dat"),
    ("11", "ppaplus", "PPA+.dat", "PPA+summary.dat"),
    ("12", "ppa", "PPA.dat", "PPA-summary.dat"),
    ("12", "ppaplus", "PPA+.dat", "PPA+summary.dat"),
)
PPA_INVALID_COORDINATE_ORACLE_CASES = (
    ("05", "ppaplus", "PPA+.dat", 310, "invalid float"),
)


def test_run_ppa_when_single_chain_is_bent_keeps_endpoints_and_shortens_path() -> None:
    snapshot = Snapshot(
        chains=(
            Chain(
                (
                    Vector3(-1.5, 0.0, 0.0),
                    Vector3(-0.5, 0.8, 0.0),
                    Vector3(0.5, -0.8, 0.0),
                    Vector3(1.5, 0.0, 0.0),
                ),
            ),
        ),
        box=Vector3(20.0, 20.0, 20.0),
        label=None,
        shear=None,
    )

    result = run_ppa(snapshot, _quick_settings(PpaMode.STANDARD))

    chain = result.primitive_path.chains[0]
    assert chain.nodes[0] == snapshot.chains[0].nodes[0]
    assert chain.nodes[-1] == snapshot.chains[0].nodes[-1]
    assert _contour(chain.nodes) < _contour(snapshot.chains[0].nodes)
    assert result.summary.z_values == (-1,)


def test_run_ppa_when_different_chains_overlap_applies_wca_repulsion() -> None:
    snapshot = Snapshot(
        chains=(
            Chain(
                (
                    Vector3(-1.0, 0.0, 0.0),
                    Vector3(0.0, 0.0, 0.0),
                    Vector3(1.0, 0.0, 0.0),
                ),
            ),
            Chain(
                (
                    Vector3(-1.0, 0.2, 0.0),
                    Vector3(0.0, 0.2, 0.0),
                    Vector3(1.0, 0.2, 0.0),
                ),
            ),
        ),
        box=Vector3(20.0, 20.0, 20.0),
        label=None,
        shear=None,
    )

    result = run_ppa(snapshot, _quick_settings(PpaMode.ACCELERATED))

    before = dist(
        snapshot.chains[0].nodes[1].as_tuple(),
        snapshot.chains[1].nodes[1].as_tuple(),
    )
    after = dist(
        result.primitive_path.chains[0].nodes[1].as_tuple(),
        result.primitive_path.chains[1].nodes[1].as_tuple(),
    )
    assert after > before


def test_run_ppa_when_dumbbells_exist_preserves_them_in_coordinate_output() -> None:
    snapshot = Snapshot(
        chains=(
            Chain(
                (
                    Vector3(0.0, 0.0, 0.0),
                    Vector3(0.5, 0.2, 0.0),
                    Vector3(1.0, 0.0, 0.0),
                ),
            ),
            Chain((Vector3(3.0, 0.0, 0.0), Vector3(4.0, 0.0, 0.0))),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )

    result = run_ppa(snapshot, _quick_settings(PpaMode.STANDARD))

    assert result.primitive_path.chain_count == 2
    assert result.primitive_path.chains[1] == snapshot.chains[1]


def test_wca_neighbor_pairs_when_boundary_pair_is_near_filters_candidates() -> None:
    neighbors = wca_neighbor_pairs(
        PpaNeighborInput(
            positions=(
                PpaVector(0.2, 0.0, 0.0),
                PpaVector(9.9, 0.0, 0.0),
                PpaVector(5.0, 5.0, 5.0),
                PpaVector(5.8, 5.0, 5.0),
                PpaVector(2.0, 0.0, 0.0),
                PpaVector(2.1, 0.0, 0.0),
            ),
            chain_for_node=(0, 1, 2, 3, 4, 4),
            box=PpaVector(10.0, 10.0, 10.0),
            shear=0.0,
            cutoff=0.5,
        ),
    )

    assert tuple((pair.first, pair.second) for pair in neighbors) == ((0, 1),)
    assert isclose(neighbors[0].distance_squared, 0.09, abs_tol=1.0e-12)


def test_wca_neighbor_cells_when_grid_axis_collapses_are_unique() -> None:
    cells = neighbor_cells((0, 0, 0), (1, 2, 1))

    assert len(cells) == len(set(cells))
    assert cells == ((0, 1, 0), (0, 0, 0))


@pytest.mark.parametrize(
    ("benchmark", "mode", "path_name", "summary_name"),
    PPA_SUMMARY_ORACLE_CASES,
)
def test_ppa_summary_when_oracle_coordinate_path_matches_oracle_summary(
    benchmark: str,
    mode: str,
    path_name: str,
    summary_name: str,
) -> None:
    original = read_z1_file(SOURCE_Z1 / f".benchmark-{benchmark}.Z1")
    fixture_dir = PPA_FIXTURE_ROOT / f"benchmark-{benchmark}" / mode
    primitive_path = read_init_config_file(fixture_dir / path_name)
    expected = read_summary_file(fixture_dir / summary_name)[0]

    outputs = build_ppa_summary_outputs(
        original=original,
        primitive_path=primitive_path,
        timestep=1,
    )

    if benchmark == "01":
        assert outputs.n_values[:2] == (11, 2)
        assert len(outputs.lpp_values) == 1
    _assert_ppa_summary_close(outputs.record, expected)


@pytest.mark.parametrize(
    ("benchmark", "mode", "path_name", "line_number", "reason"),
    PPA_INVALID_COORDINATE_ORACLE_CASES,
)
def test_ppa_oracle_coordinate_path_when_fortran_overflows_is_known_invalid(
    benchmark: str,
    mode: str,
    path_name: str,
    line_number: int,
    reason: str,
) -> None:
    fixture_dir = PPA_FIXTURE_ROOT / f"benchmark-{benchmark}" / mode

    with pytest.raises(Z1OutputParseError) as exc_info:
        _ = read_init_config_file(fixture_dir / path_name)
    assert exc_info.value.line_number == line_number
    assert exc_info.value.reason == reason


def test_write_ppa_outputs_when_standard_mode_writes_path_and_summary(
    tmp_path: Path,
) -> None:
    snapshot = Snapshot(
        chains=(
            Chain(
                (
                    Vector3(0.0, 0.0, 0.0),
                    Vector3(0.5, 0.2, 0.0),
                    Vector3(1.0, 0.0, 0.0),
                ),
            ),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )
    result = run_ppa(snapshot, _quick_settings(PpaMode.STANDARD))

    write_ppa_outputs(tmp_path, result, PpaMode.STANDARD)

    written_path = read_init_config_file(tmp_path / "PPA.dat")
    assert written_path.chain_count == 1
    written_summary = read_summary_file(tmp_path / "PPA-summary.dat")[0]
    assert written_summary.timestep == result.summary.record.timestep
    assert isclose(
        written_summary.mean_shortest_path_contour,
        result.summary.record.mean_shortest_path_contour,
        abs_tol=1.0e-3,
    )
    _assert_float_values_close(
        read_float_values_file(tmp_path / "Ree_values.dat"),
        result.summary.ree_values,
    )
    _assert_float_values_close(
        read_float_values_file(tmp_path / "Lpp_values.dat"),
        result.summary.lpp_values,
    )
    assert read_int_values_file(tmp_path / "N_values.dat") == result.summary.n_values


def _quick_settings(mode: PpaMode) -> PpaSettings:
    return PpaSettings(
        mode=mode,
        phases=(PpaPhase(timestep=0.001, temperature=0.0, step_count=80, skin=0.7),),
    )


def _contour(nodes: tuple[Vector3, ...]) -> float:
    return sum(
        dist(first.as_tuple(), second.as_tuple())
        for first, second in pairwise(nodes)
    )


def _assert_float_values_close(
    actual: tuple[float, ...],
    expected: tuple[float, ...],
) -> None:
    assert len(actual) == len(expected)
    for actual_value, expected_value in zip(actual, expected, strict=True):
        assert isclose(actual_value, expected_value, abs_tol=1.0e-12)


def _assert_ppa_summary_close(
    actual: Z1SummaryRecord,
    expected: Z1SummaryRecord,
) -> None:
    assert isclose(
        actual.mean_shortest_path_contour,
        expected.mean_shortest_path_contour,
        abs_tol=1.0e-3,
    )
    assert isclose(
        actual.mean_squared_end_to_end,
        expected.mean_squared_end_to_end,
        abs_tol=1.0e-3,
    )
    assert isclose(
        actual.coil_tube_step_length,
        expected.coil_tube_step_length,
        abs_tol=1.0e-3,
    )
    assert isclose(
        actual.root_mean_squared_contour,
        expected.root_mean_squared_contour,
        abs_tol=1.0e-3,
    )
    assert isclose(
        actual.ne_classical_coil,
        expected.ne_classical_coil,
        abs_tol=1.0e-3,
    )
    assert isclose(
        actual.ne_modified_coil,
        expected.ne_modified_coil,
        abs_tol=1.0e-3,
    )
    assert isclose(
        actual.mean_original_bond_length,
        expected.mean_original_bond_length,
        abs_tol=1.0e-3,
    )
    assert isclose(
        actual.original_bead_density,
        expected.original_bead_density,
        abs_tol=1.0e-3,
    )
