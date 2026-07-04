from __future__ import annotations

from math import isclose, sqrt
from pathlib import Path

from pyz1.models import Chain, Snapshot, Vector3
from pyz1.output_io import read_shortest_path_file, read_summary_file
from pyz1.output_models import ShortestPathPair
from pyz1.reducer import ReducerSettings, reduce_snapshot, write_reducer_outputs
from pyz1.z1_io import read_z1_file

FLOAT_TOLERANCE = 1.0e-12
KINK_POSITION_TOLERANCE = 2.0e-2
SOURCE_Z1 = Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1+")


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


def test_reduce_snapshot_when_pairing_enabled_pairs_retained_kink() -> None:
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
                    Vector3(0.5, 1.8, 0.0),
                    Vector3(0.5, 0.8, 0.0),
                    Vector3(0.5, -0.2, 0.0),
                ),
            ),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    kink = result.shortest_path.chains[0].nodes[1]
    assert kink.is_entanglement is True
    assert kink.pair == ShortestPathPair(chain_index=2, node_index=1)


def test_reduce_snapshot_when_contact_node_keeps_fractional_source_bead() -> None:
    snapshot = Snapshot(
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
                    Vector3(0.5, 0.05, 0.0),
                    Vector3(0.5, 1.0, 0.0),
                    Vector3(0.5, 2.0, 0.0),
                ),
            ),
        ),
        box=Vector3(10.0, 10.0, 10.0),
        label=None,
        shear=None,
    )

    result = reduce_snapshot(snapshot)

    contact_node = result.shortest_path.chains[0].nodes[1]
    assert contact_node.is_entanglement is True
    assert isclose(contact_node.source_bead, 1.5, abs_tol=FLOAT_TOLERANCE)


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


def test_reduce_snapshot_when_benchmark_04_matches_oracle_kink_structure() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    assert tuple(chain.node_count for chain in result.shortest_path.chains) == (
        3,
        2,
        2,
        2,
        2,
    )
    assert result.summary.z_values == (1, 0, 0, 0, 0)


def test_reduce_snapshot_when_benchmark_04_reports_reducer_diagnostics() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    assert result.diagnostics.core_node_count == 10
    assert result.diagnostics.final_node_count == 11
    assert result.diagnostics.core_accepted_blocked_move_count == 9
    assert result.diagnostics.core_retained_blocked_node_count == 2
    assert result.diagnostics.core_transient_blocked_node_count == 7
    assert result.diagnostics.core_trace_node_count == 17
    assert result.diagnostics.core_trace_ghost_node_count == 7


def test_reduce_snapshot_when_benchmark_04_reports_core_trace_nodes() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    trace_nodes = result.diagnostics.core_trace_blocked_nodes
    assert tuple(len(chain_nodes) for chain_nodes in trace_nodes) == (1, 3, 0, 3, 2)
    retained_count = sum(
        node.retained
        for chain_nodes in trace_nodes
        for node in chain_nodes
    )
    assert retained_count == 2
    first_trace_node = trace_nodes[0][0]
    assert isclose(first_trace_node.source_bead, 3.5, abs_tol=FLOAT_TOLERANCE)
    assert first_trace_node.retained is False
    assert first_trace_node.blocker_chain_index == 2
    assert first_trace_node.blocker_node_index == 9
    assert first_trace_node.shortcut_fraction is not None
    assert first_trace_node.blocker_fraction is not None
    assert first_trace_node.blocker_distance is not None
    assert isclose(
        first_trace_node.shortcut_fraction,
        0.6073846552478331,
        abs_tol=FLOAT_TOLERANCE,
    )
    assert isclose(
        first_trace_node.blocker_fraction,
        0.9360190360001871,
        abs_tol=FLOAT_TOLERANCE,
    )
    assert isclose(
        first_trace_node.blocker_distance,
        0.018665390233954277,
        abs_tol=FLOAT_TOLERANCE,
    )
    assert_vector_close(
        first_trace_node.position,
        Vector3(0.1293575, -0.030405000000000015, 1.72274),
    )


def test_reduce_snapshot_when_benchmark_04_reports_core_stage_nodes() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    stage_nodes = result.diagnostics.core_stage_nodes
    assert tuple(len(chain_nodes) for chain_nodes in stage_nodes) == (3, 4, 2, 4, 4)
    assert sum(len(chain_nodes) for chain_nodes in stage_nodes) == 17
    assert tuple(
        tuple(node.source_bead for node in chain_nodes)
        for chain_nodes in stage_nodes
    ) == (
        (1.0, 3.5, 10.0),
        (1.0, 6.5, 7.25, 10.0),
        (1.0, 10.0),
        (1.0, 7.5, 8.25, 10.0),
        (1.0, 6.5, 8.5, 10.0),
    )
    assert sum(
        node.transient
        for chain_nodes in stage_nodes
        for node in chain_nodes
    ) == 7
    assert_vector_close(
        stage_nodes[0][1].position,
        result.diagnostics.projection_traces[0].projected_position,
    )


def test_reduce_snapshot_when_benchmark_04_reports_projection_trace() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    projection = result.diagnostics.projection_traces[0]
    assert projection.chain_index == 1
    assert isclose(projection.source_bead, 3.5, abs_tol=FLOAT_TOLERANCE)
    assert projection.responsible_chain_index == 2
    assert projection.responsible_node_index == 1
    assert projection.responsible_fraction is not None
    assert isclose(
        projection.responsible_fraction,
        0.7221116658876934,
        abs_tol=FLOAT_TOLERANCE,
    )
    assert_vector_close(
        projection.initial_position,
        Vector3(0.1293575, -0.030405000000000015, 1.72274),
    )
    assert_vector_close(
        projection.projected_position,
        Vector3(0.13536991275801988, -0.1612181380318356, 1.6021666363965665),
    )


def test_reduce_snapshot_when_benchmark_04_matches_oracle_kink_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")
    oracle = read_shortest_path_file(
        Path("tests/fixtures/z1plus_oracle/benchmark-04/spplus/Z1+SP.dat"),
    )

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    actual_kink = result.shortest_path.chains[0].nodes[1]
    oracle_kink = oracle.chains[0].nodes[1]
    assert isclose(
        actual_kink.source_bead,
        oracle_kink.source_bead,
        abs_tol=FLOAT_TOLERANCE,
    )


def test_reduce_snapshot_when_benchmark_04_matches_oracle_pairing() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")
    oracle = read_shortest_path_file(
        Path("tests/fixtures/z1plus_oracle/benchmark-04/spplus/Z1+SP.dat"),
    )

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    actual_kink = result.shortest_path.chains[0].nodes[1]
    oracle_kink = oracle.chains[0].nodes[1]
    assert actual_kink.pair == oracle_kink.pair


def test_reduce_snapshot_when_benchmark_04_kink_position_approaches_oracle() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")
    oracle = read_shortest_path_file(
        Path("tests/fixtures/z1plus_oracle/benchmark-04/spplus/Z1+SP.dat"),
    )

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    actual_position = result.shortest_path.chains[0].nodes[1].position
    oracle_position = oracle.chains[0].nodes[1].position
    assert (
        vector_distance(actual_position, oracle_position)
        < KINK_POSITION_TOLERANCE
    )


def assert_vector_close(actual: Vector3, expected: Vector3) -> None:
    assert isclose(actual.x, expected.x, abs_tol=FLOAT_TOLERANCE)
    assert isclose(actual.y, expected.y, abs_tol=FLOAT_TOLERANCE)
    assert isclose(actual.z, expected.z, abs_tol=FLOAT_TOLERANCE)


def vector_distance(first: Vector3, second: Vector3) -> float:
    dx = first.x - second.x
    dy = first.y - second.y
    dz = first.z - second.z
    return sqrt(dx * dx + dy * dy + dz * dz)
