from __future__ import annotations

from itertools import pairwise
from math import dist, isclose
from typing import TYPE_CHECKING

from pyz1.initconfig_io import read_init_config_file
from pyz1.models import Chain, Snapshot, Vector3
from pyz1.output_io import read_summary_file
from pyz1.output_values import read_float_values_file, read_int_values_file
from pyz1.ppa import PpaMode, PpaPhase, PpaSettings, run_ppa, write_ppa_outputs

if TYPE_CHECKING:
    from pathlib import Path


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
