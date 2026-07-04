from __future__ import annotations

from math import isclose
from typing import TYPE_CHECKING

from pyz1.models import Chain, Snapshot, Vector3
from pyz1.output_io import read_shortest_path_file, read_summary_file
from pyz1.reducer import reduce_snapshot, write_reducer_outputs

if TYPE_CHECKING:
    from pathlib import Path

FLOAT_TOLERANCE = 1.0e-12


def test_reduce_snapshot_when_single_bent_chain_has_no_blockers_straightens() -> None:
    snapshot = Snapshot(
        chains=(
            Chain(
                (
                    Vector3(0.0, 0.0, 0.0),
                    Vector3(0.5, 1.0, 0.0),
                    Vector3(1.0, 0.0, 0.0),
                ),
            ),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )

    result = reduce_snapshot(snapshot)

    shortest_path = result.shortest_path.chains[0]
    assert shortest_path.node_count == 2
    assert_vector_close(shortest_path.nodes[0].position, Vector3(0.0, 0.0, 0.0))
    assert_vector_close(shortest_path.nodes[1].position, Vector3(1.0, 0.0, 0.0))
    assert result.summary.z_values == (0,)
    assert isclose(
        result.summary.record.mean_shortest_path_contour,
        1.0,
        abs_tol=FLOAT_TOLERANCE,
    )


def test_reduce_snapshot_when_candidate_would_cross_other_chain_keeps_kink() -> None:
    snapshot = Snapshot(
        chains=(
            Chain(
                (
                    Vector3(0.0, 0.0, 0.0),
                    Vector3(0.0, 2.0, 0.0),
                    Vector3(1.0, 1.0, 0.0),
                ),
            ),
            Chain(
                (
                    Vector3(0.5, -0.2, 0.0),
                    Vector3(0.5, 0.8, 0.0),
                    Vector3(0.5, 1.8, 0.0),
                ),
            ),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )

    result = reduce_snapshot(snapshot)

    first_path = result.shortest_path.chains[0]
    assert first_path.node_count == 3
    assert_vector_close(first_path.nodes[1].position, Vector3(0.0, 2.0, 0.0))
    assert first_path.nodes[1].is_entanglement is True
    assert result.summary.z_values[0] == 1


def test_reduce_snapshot_when_dumbbell_is_present_excludes_it_from_sp() -> None:
    snapshot = Snapshot(
        chains=(
            Chain(
                (
                    Vector3(0.0, 0.0, 0.0),
                    Vector3(0.5, 1.0, 0.0),
                    Vector3(1.0, 0.0, 0.0),
                ),
            ),
            Chain((Vector3(2.0, 0.0, 0.0), Vector3(3.0, 0.0, 0.0))),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )

    result = reduce_snapshot(snapshot)

    assert result.shortest_path.chain_count == 1
    assert result.summary.record.true_chain_count == 1
    assert result.summary.n_values == (3,)


def test_write_reducer_outputs_when_result_is_available_writes_z1_files(
    tmp_path: Path,
) -> None:
    snapshot = Snapshot(
        chains=(
            Chain(
                (
                    Vector3(0.0, 0.0, 0.0),
                    Vector3(0.5, 1.0, 0.0),
                    Vector3(1.0, 0.0, 0.0),
                ),
            ),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )
    result = reduce_snapshot(snapshot)

    write_reducer_outputs(tmp_path, result)

    assert read_shortest_path_file(tmp_path / "Z1+SP.dat") == result.shortest_path
    written_summary = read_summary_file(tmp_path / "Z1+summary.dat")[0]
    assert written_summary.timestep == result.summary.record.timestep
    assert isclose(
        written_summary.mean_shortest_path_contour,
        result.summary.record.mean_shortest_path_contour,
        abs_tol=1.0e-3,
    )


def assert_vector_close(actual: Vector3, expected: Vector3) -> None:
    assert isclose(actual.x, expected.x, abs_tol=FLOAT_TOLERANCE)
    assert isclose(actual.y, expected.y, abs_tol=FLOAT_TOLERANCE)
    assert isclose(actual.z, expected.z, abs_tol=FLOAT_TOLERANCE)
