from __future__ import annotations

from os import environ
from pathlib import Path
from shutil import copyfile

from pyz1.output_io import read_shortest_path_file, read_summary_file
from pyz1.reducer import ReducerSettings, reduce_snapshot
from pyz1.regression import (
    RegressionMode,
    RegressionRecord,
    RegressionRequest,
    RegressionStatus,
    compare_spplus_pairing,
    write_benchmark_regression_report,
)
from pyz1.summary import build_summary_outputs
from pyz1.z1_io import read_z1_file

SOURCE_Z1 = Path(
    environ.get(
        "PYZ1_SOURCE_Z1",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1+",
    ),
)
ORACLE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703")
LOG_STATS = Path("tests/fixtures/z1plus_oracle/benchmark-04/spplus/log-stats.Z1")


def test_write_benchmark_regression_report_when_oracles_exist_lists_modes(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.DEFAULT, RegressionMode.SPPLUS, RegressionMode.SELFZ),
            benchmark_ids=("04",),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert len(records) == 3
    assert "| benchmark-04 | spplus | passed |" in text
    assert "| benchmark-04 | selfz | passed |" in text
    assert tuple(record.status for record in records) == (
        RegressionStatus.PASSED,
        RegressionStatus.PASSED,
        RegressionStatus.PASSED,
    )
    assert "summary field mismatches" in text
    assert "max node position delta" in text
    assert "node count mismatches" in text
    assert records[1].summary_field_mismatches == 0
    assert records[1].node_count_mismatches == 0
    assert records[1].max_node_position_delta is not None
    assert records[1].max_node_position_delta < 0.001
    assert_benchmark_04_max_delta_location(records[1])
    assert_benchmark_04_max_delta_pair_geometry(records[1])
    assert records[1].pyz1_core_accepted_blocked_moves == 9
    assert records[1].pyz1_core_transient_blocked_nodes == 7
    assert records[1].pyz1_core_trace_node_count == 17
    assert records[1].pyz1_core_trace_ghost_nodes == 7
    assert records[1].pyz1_first_trace_blocker_chain == 2
    assert records[1].pyz1_first_trace_blocker_node == 9
    assert records[1].pyz1_first_trace_shortcut_fraction is not None
    assert 0.607 < records[1].pyz1_first_trace_shortcut_fraction < 0.608
    assert records[1].pyz1_first_trace_blocker_fraction is not None
    assert 0.936 < records[1].pyz1_first_trace_blocker_fraction < 0.937
    assert records[1].pyz1_projection_trace_count == 1
    assert records[1].pyz1_first_projection_responsible_chain == 2
    assert records[1].pyz1_first_projection_responsible_node == 1
    assert records[1].pyz1_first_projection_responsible_fraction is not None
    assert 0.732 < records[1].pyz1_first_projection_responsible_fraction < 0.734
    assert records[1].oracle_core_node_count == 17
    assert records[1].oracle_core_ghost_nodes == 6
    assert records[1].oracle_core_stage_node_count == 17
    assert records[1].pyz1_core_stage_node_count_mismatches == 0
    assert records[1].pyz1_core_stage_max_node_position_delta is not None
    assert 0.037 < records[1].pyz1_core_stage_max_node_position_delta < 0.038
    assert records[1].pyz1_core_stage_source_bead_matches == 14
    assert records[1].pyz1_core_stage_source_bead_max_delta is not None
    assert 0.037 < records[1].pyz1_core_stage_source_bead_max_delta < 0.038
    assert "ne_modified_coil:" not in text
    assert "pyz1 core trace nodes" in text
    assert "pyz1 core transient blocked nodes" in text
    assert "pyz1 first trace blocker fraction" in text
    assert "pyz1 projection traces" in text
    assert "pyz1 first projection fraction" in text
    assert "oracle core ghosts" in text
    assert "oracle core stage nodes" in text
    assert "pyz1 core stage max node position delta" in text
    assert "pyz1 core stage source bead max delta" in text


def test_write_benchmark_regression_report_when_stats_log_exists_lists_core_diagnostics(
    tmp_path: Path,
) -> None:
    oracle_root = tmp_path / "oracle"
    oracle_dir = oracle_root / "benchmark-04" / "spplus"
    oracle_dir.mkdir(parents=True)
    _ = copyfile(
        ORACLE_ROOT / "benchmark-04" / "spplus" / "Z1+SP.dat",
        oracle_dir / "Z1+SP.dat",
    )
    _ = copyfile(
        ORACLE_ROOT / "benchmark-04" / "spplus" / "Z1+summary.dat",
        oracle_dir / "Z1+summary.dat",
    )
    _ = copyfile(LOG_STATS, oracle_dir / "log-stats.Z1")
    _ = copyfile(
        Path("tests/fixtures/z1plus_oracle/benchmark-04/spplus")
        / "Z1+NODES-best-match-step1-entry.dat",
        oracle_dir / "Z1+NODES-best-match-step1-entry.dat",
    )
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=oracle_root,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("04",),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert len(records) == 1
    assert records[0].pyz1_core_node_count == 10
    assert records[0].pyz1_final_node_count == 11
    assert records[0].pyz1_core_accepted_blocked_moves == 9
    assert records[0].pyz1_core_transient_blocked_nodes == 7
    assert records[0].pyz1_core_trace_node_count == 17
    assert records[0].pyz1_core_trace_ghost_nodes == 7
    assert records[0].pyz1_first_trace_blocker_chain == 2
    assert records[0].pyz1_first_trace_blocker_node == 9
    assert records[0].pyz1_projection_trace_count == 1
    assert records[0].pyz1_first_projection_responsible_chain == 2
    assert records[0].pyz1_first_projection_responsible_node == 1
    assert records[0].oracle_core_node_count == 17
    assert records[0].oracle_final_node_count == 11
    assert_benchmark_04_max_delta_location(records[0])
    assert_benchmark_04_max_delta_pair_geometry(records[0])
    assert records[0].oracle_core_ghost_nodes == 6
    assert records[0].oracle_core_stage_node_count == 17
    assert records[0].pyz1_core_stage_node_count_mismatches == 0
    assert records[0].pyz1_core_stage_max_node_position_delta is not None
    assert 0.037 < records[0].pyz1_core_stage_max_node_position_delta < 0.038
    assert records[0].pyz1_core_stage_source_bead_matches == 14
    assert records[0].pyz1_core_stage_source_bead_max_delta is not None
    assert 0.037 < records[0].pyz1_core_stage_source_bead_max_delta < 0.038
    assert "pyz1 core nodes" in text
    assert "pyz1 first projection fraction" in text
    assert "oracle core ghosts" in text
    assert "oracle core stage nodes" in text
    assert "pyz1 core stage node count mismatches" in text
    assert "pyz1 core stage source bead matches" in text
    assert "| benchmark-04 | spplus | passed |" in text
    assert "max node delta chain" in text
    assert "| 1 | 2 | 3.5 | 3.5 |" in text
    assert "max node actual pair fraction" in text
    assert "| 0.733072 | 0.00163761 | 0.733114 | 0.00179606 |" in text


def test_write_benchmark_regression_report_when_stdout_has_scan_rows_uses_them(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01",),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert records[0].oracle_core_node_count == 617
    assert records[0].oracle_final_node_count == 615
    assert records[0].oracle_core_crossings == 15
    assert records[0].oracle_core_ghost_nodes == 0
    assert "oracle core nodes" in text
    assert "oracle final nodes" in text


def test_write_benchmark_regression_report_when_default_guard_runs_medium_cases(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01", "06"),
        ),
    )

    assert records[0].status == RegressionStatus.MISMATCH
    assert records[0].node_count_mismatches is not None
    assert records[0].node_count_mismatches > 0
    assert records[1].status == RegressionStatus.KNOWN_INVALID
    assert records[1].note == "skipped: node_count>1000"


def test_write_benchmark_regression_report_when_default_guard_runs_1000_node_case(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("05", "06"),
        ),
    )

    assert records[0].status == RegressionStatus.MISMATCH
    assert records[0].node_count_mismatches is not None
    assert records[0].node_count_mismatches > 0
    assert records[1].status == RegressionStatus.KNOWN_INVALID
    assert records[1].note == "skipped: node_count>1000"


def test_write_benchmark_regression_report_when_obstacle_sequence_matches_reports_pairs(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("03",),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert records[0].pyz1_obstacle_pair_sequence == (268, 241, 160, 130)
    assert records[0].oracle_obstacle_pair_sequence == (268, 241, 160, 130)
    assert "pyz1 obstacle pair sequence" in text
    assert "268,241,160,130" in text


def test_write_benchmark_regression_report_when_winding_candidates_miss_oracle(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01", "03"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    benchmark_01 = records[0]
    benchmark_03 = records[1]
    assert benchmark_01.pyz1_winding_candidate_count == 41
    assert benchmark_01.pyz1_winding_missing_oracle_sequence == (128, 208, 36)
    assert benchmark_01.pyz1_winding_extra_candidate_count == 31
    assert benchmark_03.pyz1_winding_candidate_count == 8
    assert benchmark_03.pyz1_winding_missing_oracle_sequence == ()
    assert benchmark_03.pyz1_winding_extra_candidate_count == 4
    assert "pyz1 winding candidates" in text
    assert "pyz1 winding missing oracle sequence" in text
    assert "128,208,36" in text


def test_write_benchmark_regression_report_when_convex_candidates_cover_oracle(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01", "02", "05"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    benchmark_01 = records[0]
    benchmark_02 = records[1]
    benchmark_05 = records[2]
    assert benchmark_01.pyz1_convex_winding_candidate_count == 67
    assert benchmark_01.pyz1_convex_winding_missing_oracle_sequence == ()
    assert benchmark_01.pyz1_convex_winding_extra_candidate_count == 54
    assert benchmark_02.pyz1_convex_winding_candidate_count == 65
    assert benchmark_02.pyz1_convex_winding_missing_oracle_sequence == ()
    assert benchmark_05.pyz1_true_chain_pair_sequence == (40, 26)
    assert benchmark_05.pyz1_true_chain_contact_candidate_sequence == (
        6,
        40,
        26,
        12,
    )
    assert benchmark_05.oracle_source_nearest_true_chain_contact_sequence == (
        40,
        26,
    )
    assert benchmark_05.oracle_true_chain_pair_sequence == (40, 26)
    assert benchmark_05.pyz1_true_chain_pair_node_sequence == (3, 2)
    assert benchmark_05.oracle_true_chain_pair_node_sequence == (3, 2)
    assert benchmark_05.node_count_mismatches == 5
    assert benchmark_05.pyz1_convex_winding_missing_oracle_sequence == (40, 26)
    assert "pyz1 convex winding candidates" in text
    assert "pyz1 true-chain contact candidate sequence" in text
    assert "oracle-source nearest true-chain contact sequence" in text
    assert "pyz1 true-chain pair sequence" in text
    assert "pyz1 true-chain pair node sequence" in text
    assert "oracle true-chain pair sequence" in text
    assert "oracle true-chain pair node sequence" in text


def test_reduce_snapshot_when_benchmark05_chain40_keeps_lower_index_contact() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_40_pairs = tuple(
        node.pair.chain_index
        for node in result.shortest_path.chains[39].nodes[1:-1]
        if node.pair is not None
    )
    assert 25 in chain_40_pairs


def test_reduce_snapshot_when_benchmark05_chain25_keeps_reciprocal_contact() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_25_pairs = tuple(
        node.pair.chain_index
        for node in result.shortest_path.chains[24].nodes[1:-1]
        if node.pair is not None
    )
    assert 40 in chain_25_pairs


def test_reduce_snapshot_when_benchmark05_chain2_keeps_repeated_contact() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pairs = tuple(
        node.pair.chain_index
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None
    )
    assert 34 in chain_2_pairs


def test_reduce_snapshot_when_benchmark05_chain2_places_repeated_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pair_34_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 34
    )
    assert chain_2_pair_34_sources[0] > 3.9


def test_reduce_snapshot_when_benchmark05_chain2_keeps_paired_contact() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pairs = tuple(
        node.pair.chain_index
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None
    )
    assert 13 in chain_2_pairs


def test_reduce_snapshot_when_benchmark05_chain2_keeps_second_pair_contact() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pair_13_count = sum(
        1
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 13
    )
    assert chain_2_pair_13_count >= 2


def test_reduce_snapshot_when_benchmark05_chain2_spreads_pair_sources() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pair_13_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 13
    )
    assert (
        chain_2_pair_13_sources[1] - chain_2_pair_13_sources[0]
        > 2.0
    )


def test_reduce_snapshot_when_benchmark05_chain2_places_first_pair13_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pair_13_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 13
    )
    assert 8.049 < chain_2_pair_13_sources[0] < 8.051


def test_reduce_snapshot_when_benchmark05_chain2_places_second_pair13_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pair_13_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 13
    )
    assert 11.949 < chain_2_pair_13_sources[1] < 11.951


def test_reduce_snapshot_when_benchmark05_chain2_keeps_tail_contact() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pairs = tuple(
        node.pair.chain_index
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None
    )
    assert 6 in chain_2_pairs


def test_reduce_snapshot_when_benchmark05_chain2_places_tail_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pair_6_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 6
    )
    assert chain_2_pair_6_sources[0] < 15.99


def test_reduce_snapshot_when_benchmark05_chain2_places_pair6_node() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pair_6_nodes = tuple(
        node.pair.node_index
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 6
    )
    assert chain_2_pair_6_nodes[0] == 2


def test_reduce_snapshot_when_benchmark05_chain2_places_pair34_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pair_34_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 34
    )
    assert 4.37 < chain_2_pair_34_sources[0] < 4.39


def test_reduce_snapshot_when_benchmark05_chain2_places_pair34_node() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_2_pair_34_nodes = tuple(
        node.pair.node_index
        for node in result.shortest_path.chains[1].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 34
    )
    assert chain_2_pair_34_nodes[0] == 2


def test_reduce_snapshot_when_benchmark05_chain3_uses_pair25_contact() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_3_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[2].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_3_pairs == ((5.0, 25, 1),)


def test_reduce_snapshot_when_benchmark05_chain25_uses_pair3_reciprocal() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_25_pair_3 = tuple(
        (
            node.source_bead,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[24].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 3
    )
    assert chain_25_pair_3 == ((11.67, 2),)


def test_reduce_snapshot_when_benchmark05_chain25_places_pair40_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_25_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[24].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_25_pairs == ((11.67, 3, 2), (15.83, 40, 2))


def test_reduce_snapshot_when_benchmark05_chain22_places_pair25_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_22_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[21].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_22_pairs == ((4.84, 25, 2),)


def test_reduce_snapshot_when_benchmark05_chain4_matches_oracle_pair_sequence() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_4_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[3].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_4_pairs == ((5.68, 40, 3), (10.43, 18, 2))


def test_reduce_snapshot_when_benchmark05_chain5_matches_oracle_pair_sequence() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_5_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[4].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_5_pairs == ((6.67, 16, 1),)
    chain_16_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[15].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_16_pairs == ((3.0, 5, 2),)


def test_reduce_snapshot_when_benchmark05_chain6_matches_oracle_pair_sequence() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_6_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[5].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_6_pairs == ((3.85, 37, 3), (6.71, 2, 4))
    chain_37_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[36].nodes[1:-1]
        if node.pair is not None
    )
    assert (10.38, 6, 2) in chain_37_pairs


def test_reduce_snapshot_when_benchmark05_chain9_matches_oracle_pair_sequence() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_9_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[8].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_9_pairs == ((6.5, 27, 1),)
    chain_27_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[26].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_27_pairs == ((2.43, 9, 2), (6.71, 19, 1))


def test_reduce_snapshot_when_benchmark05_chain10_matches_oracle_pair() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_10_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[9].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_10_pairs == ((10.67, 36, 2),)
    chain_36_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[35].nodes[1:-1]
        if node.pair is not None
    )
    assert (14.64, 10, 2) in chain_36_pairs


def test_reduce_snapshot_when_benchmark05_chain11_keeps_early_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_11_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[10].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_11_pairs[:2] == ((2.73, 37, 1), (4.48, 39, 5))
    chain_37_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[36].nodes[1:-1]
        if node.pair is not None
    )
    assert (4.15, 11, 2) in chain_37_pairs
    chain_39_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[38].nodes[1:-1]
        if node.pair is not None
    )
    assert (13.16, 11, 3) in chain_39_pairs


def test_reduce_snapshot_when_benchmark05_chain11_matches_oracle_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_11_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[10].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_11_pairs == (
        (2.73, 37, 1),
        (4.48, 39, 5),
        (11.5, 32, 2),
    )
    chain_32_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[31].nodes[1:-1]
        if node.pair is not None
    )
    assert (2.8, 11, 3) in chain_32_pairs


def test_reduce_snapshot_when_benchmark05_chain12_matches_oracle_pair() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_12_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[11].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_12_pairs == ((11.5, 19, 1),)
    chain_19_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[18].nodes[1:-1]
        if node.pair is not None
    )
    assert (3.5, 12, 2) in chain_19_pairs


def test_reduce_snapshot_when_benchmark05_chain13_matches_oracle_pair() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_13_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[12].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_13_pairs == ((4.0, 2, 3),)


def test_reduce_snapshot_when_benchmark05_chain15_matches_oracle_pair() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_15_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[14].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_15_pairs == ((13.72, 36, 1),)
    chain_36_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[35].nodes[1:-1]
        if node.pair is not None
    )
    assert (6.62, 15, 2) in chain_36_pairs


def test_reduce_snapshot_when_benchmark05_chain17_matches_oracle_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_17_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[16].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_17_pairs == ((5.0, 9, 1), (11.67, 44, 2))
    chain_44_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[43].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_44_pairs == ((13.0, 17, 3),)


def test_reduce_snapshot_when_benchmark05_chain18_matches_oracle_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_18_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[17].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_18_pairs == ((5.0, 4, 3), (9.0, 48, 2))
    chain_48_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[47].nodes[1:-1]
        if node.pair is not None
    )
    assert (2.58, 18, 2) in chain_48_pairs


def test_reduce_snapshot_when_benchmark05_chain1_places_pair40_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_1_pair_40_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[0].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 40
    )
    assert chain_1_pair_40_sources[0] < 7.45


def test_reduce_snapshot_when_benchmark05_chain1_places_pair26_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_1_pair_26_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[0].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 26
    )
    assert 8.57 < chain_1_pair_26_sources[0] < 8.59


def test_reduce_snapshot_when_benchmark05_chain26_places_pair1_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_26_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[25].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_26_pairs == ((3.67, 1, 3),)


def test_reduce_snapshot_when_benchmark05_chain24_matches_oracle_pair() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_24_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[23].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_24_pairs == ((18.5, 35, 2),)
    chain_35_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[34].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_35_pairs == ((15.0, 24, 1),)


def test_reduce_snapshot_when_benchmark05_chain29_matches_oracle_pair() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_29_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[28].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_29_pairs == ((6.33, 49, 1),)
    chain_49_pairs = tuple(
        (
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[48].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_49_pairs == ()


def test_reduce_snapshot_when_benchmark05_chain20_drops_extra_pair49() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_20_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[19].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_20_pairs == ()


def test_reduce_snapshot_when_benchmark05_chain30_matches_oracle_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_30_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[29].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_30_pairs == ((3.94, 48, 4), (6.94, 34, 3))


def test_reduce_snapshot_when_benchmark05_chain31_matches_oracle_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_31_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[30].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_31_pairs == ((5.66, 46, 2), (10.33, 40, 3))


def test_reduce_snapshot_when_benchmark05_chain32_matches_oracle_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_32_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[31].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_32_pairs == ((2.8, 11, 3), (12.5, 30, 2), (16.25, 34, 4))


def test_reduce_snapshot_when_benchmark05_chain34_matches_oracle_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_34_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[33].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_34_pairs == (
        (4.45, 28, 1),
        (7.87, 48, 4),
        (11.25, 30, 3),
        (14.63, 28, 1),
    )


def test_reduce_snapshot_when_benchmark05_chain37_matches_oracle_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_37_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[36].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_37_pairs == (
        (4.15, 11, 2),
        (7.27, 4, 2),
        (10.38, 6, 2),
    )


def test_reduce_snapshot_when_benchmark05_chain39_matches_oracle_pairs() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_39_pairs = tuple(
        (
            node.source_bead,
            node.pair.chain_index,
            node.pair.node_index,
        )
        for node in result.shortest_path.chains[38].nodes[1:-1]
        if node.pair is not None
    )
    assert chain_39_pairs == (
        (3.71, 43, 1),
        (6.65, 4, 3),
        (9.82, 18, 2),
        (13.16, 11, 3),
    )


def test_reduce_snapshot_when_benchmark05_chain28_keeps_pair34_contact() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_28_pairs = tuple(
        node.pair.chain_index
        for node in result.shortest_path.chains[27].nodes[1:-1]
        if node.pair is not None
    )
    assert 34 in chain_28_pairs


def test_reduce_snapshot_when_benchmark05_chain28_places_pair34_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_28_pair_34_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[27].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 34
    )
    assert chain_28_pair_34_sources[0] > 2.4


def test_reduce_snapshot_when_benchmark05_chain28_places_pair34_node() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_28_pair_34_nodes = tuple(
        node.pair.node_index
        for node in result.shortest_path.chains[27].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 34
    )
    assert chain_28_pair_34_nodes[0] == 1


def test_reduce_snapshot_when_benchmark05_chain34_keeps_pair28_contact() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_34_pairs = tuple(
        node.pair.chain_index
        for node in result.shortest_path.chains[33].nodes[1:-1]
        if node.pair is not None
    )
    assert 28 in chain_34_pairs


def test_reduce_snapshot_when_benchmark05_chain34_places_pair28_source() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_34_pair_28_sources = tuple(
        node.source_bead
        for node in result.shortest_path.chains[33].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 28
    )
    assert chain_34_pair_28_sources[0] < 4.6


def test_reduce_snapshot_when_benchmark05_chain34_places_pair28_node() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-05.Z1")

    result = reduce_snapshot(snapshot, ReducerSettings(pairing_enabled=True))

    chain_34_pair_28_nodes = tuple(
        node.pair.node_index
        for node in result.shortest_path.chains[33].nodes[1:-1]
        if node.pair is not None and node.pair.chain_index == 28
    )
    assert chain_34_pair_28_nodes[0] == 1


def test_write_benchmark_regression_report_when_convex_selection_misses_oracle(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01", "02"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    benchmark_01 = records[0]
    benchmark_02 = records[1]
    assert benchmark_01.pyz1_convex_selected_winding_sequence == (
        20,
        185,
        278,
        41,
        134,
        35,
        110,
        9,
    )
    assert benchmark_01.pyz1_convex_selected_missing_oracle_sequence == (
        95,
        80,
        283,
        128,
        275,
        87,
        208,
        132,
        140,
        97,
        36,
    )
    assert benchmark_01.pyz1_convex_selected_extra_count == 6
    assert benchmark_02.pyz1_convex_selected_winding_sequence == (63, 239, 46, 180)
    assert benchmark_02.pyz1_convex_selected_missing_oracle_sequence == (
        146,
        278,
        132,
        86,
        27,
        139,
        102,
        217,
    )
    assert benchmark_02.pyz1_convex_selected_extra_count == 2
    assert "pyz1 convex selected winding sequence" in text
    assert "pyz1 convex selected missing oracle sequence" in text


def test_write_benchmark_regression_report_when_oracle_obstacle_sources_differ(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01", "02"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    benchmark_01 = records[0]
    benchmark_02 = records[1]
    assert benchmark_01.max_oracle_obstacle_source_delta is not None
    assert 8.753 < benchmark_01.max_oracle_obstacle_source_delta < 8.754
    assert benchmark_01.max_oracle_obstacle_source_delta_chain == 80
    assert benchmark_01.oracle_obstacle_source_residuals is not None
    assert tuple(
        residual.chain_index
        for residual in benchmark_01.oracle_obstacle_source_residuals[:3]
    ) == (95, 20, 80)
    assert benchmark_02.max_oracle_obstacle_source_delta is not None
    assert 1.325 < benchmark_02.max_oracle_obstacle_source_delta < 1.326
    assert benchmark_02.max_oracle_obstacle_source_delta_chain == 146
    assert "max oracle obstacle source delta" in text
    assert "oracle obstacle source residual details" in text
    assert "80: 10.9436!=2.19(d=8.75364)" in text


def test_write_benchmark_regression_report_when_blocked_trace_sequence_differs(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01", "03"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    benchmark_01 = records[0]
    benchmark_03 = records[1]
    assert benchmark_01.pyz1_blocked_trace_obstacle_sequence == (
        27,
        199,
        41,
        38,
        38,
        38,
        166,
        201,
        201,
    )
    assert benchmark_01.pyz1_retained_blocked_trace_obstacle_sequence == (
        27,
        199,
        41,
        38,
        38,
        166,
        201,
        201,
    )
    assert benchmark_03.pyz1_blocked_trace_obstacle_sequence == (
        8,
        153,
        153,
        212,
        212,
        212,
        212,
        212,
        212,
    )
    assert benchmark_03.oracle_obstacle_pair_sequence == (268, 241, 160, 130)
    assert "pyz1 blocked trace obstacle sequence" in text
    assert "pyz1 retained blocked trace obstacle sequence" in text


def test_write_benchmark_regression_report_when_oracle_source_uses_nonnearest_segment(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01",),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert records[0].max_oracle_obstacle_source_segment_rank == 8
    assert records[0].oracle_obstacle_source_segment_ambiguities is not None
    ambiguity_by_chain = {
        ambiguity.chain_index: ambiguity
        for ambiguity in records[0].oracle_obstacle_source_segment_ambiguities
    }
    assert ambiguity_by_chain[80].expected_rank == 2
    assert 10.94 < ambiguity_by_chain[80].nearest_source < 10.95
    assert ambiguity_by_chain[132].expected_rank == 8
    assert ambiguity_by_chain[36].expected_rank == 4
    assert 1.35 < ambiguity_by_chain[36].nearest_source < 1.36
    assert "max oracle source segment rank" in text
    assert "oracle source segment ambiguity details" in text
    assert "80: r2" in text
    assert "132: r8" in text
    assert "36: r4" in text


def test_write_benchmark_regression_report_when_spplus_sources_match_default(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01", "02"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert records[0].oracle_mode_source_sequence_matches_default is True
    assert records[0].oracle_default_source_sequence == (
        1.4,
        1.79,
        2.19,
        3.06,
        3.5,
        4.56,
        5.24,
        5.99,
        6.74,
        7.47,
        8.27,
        9.16,
        10.08,
    )
    assert records[1].oracle_mode_source_sequence_matches_default is True
    assert records[1].oracle_default_source_sequence == (
        1.95,
        2.85,
        3.62,
        4.32,
        5.06,
        5.85,
        7.48,
        8.32,
        9.2,
        10.1,
    )
    assert "oracle default source sequence" in text
    assert "oracle source sequence matches default" in text


def test_write_benchmark_regression_report_when_pyz1_sources_differ_from_default(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("01", "02"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert records[0].pyz1_source_sequence == (
        2.5,
        3.5,
        4.5,
        6.25,
        7.5,
        8.5,
        9.5,
        10.5,
    )
    assert records[0].pyz1_source_sequence_mismatch_count == 13
    assert records[0].pyz1_source_sequence_max_delta == 4.51
    assert records[0].pyz1_source_sequence_residuals is not None
    assert tuple(
        (
            residual.source_index,
            residual.actual,
            residual.expected,
            residual.delta,
        )
        for residual in records[0].pyz1_source_sequence_residuals[:3]
    ) == (
        (0, 2.5, 1.4, 1.1),
        (1, 3.5, 1.79, 1.71),
        (2, 4.5, 2.19, 2.31),
    )
    assert records[0].pyz1_source_sequence_residuals[-1].source_index == 12
    assert records[0].pyz1_source_sequence_residuals[-1].actual is None
    assert records[0].pyz1_source_sequence_residuals[-1].expected == 10.08
    assert records[1].pyz1_source_sequence == (
        2.5,
        3.5,
        4.5,
        5.5,
        8.125,
        9.5,
        10.5,
    )
    assert records[1].pyz1_source_sequence_mismatch_count == 10
    assert records[1].pyz1_source_sequence_max_delta is not None
    assert 3.65 < records[1].pyz1_source_sequence_max_delta < 3.651
    assert "pyz1 source sequence" in text
    assert "pyz1 source sequence mismatches" in text
    assert "pyz1 source sequence max delta" in text
    assert "pyz1 source sequence residual details" in text
    assert "0: 2.5!=1.4(d=1.1)" in text
    assert "8: n/a!=6.74(d=n/a)" in text


def test_write_benchmark_regression_report_when_source_beads_differ_reports_max_delta(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=ORACLE_ROOT,
            report_path=report_path,
            modes=(RegressionMode.SPPLUS,),
            benchmark_ids=("03",),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert records[0].max_node_source_bead_delta is not None
    assert 1.467 < records[0].max_node_source_bead_delta < 1.468
    assert records[0].max_source_delta_chain_index == 1
    assert records[0].max_source_delta_node_index == 5
    assert records[0].source_bead_residuals is not None
    assert tuple(
        (
            residual.chain_index,
            residual.node_index,
            residual.actual_pair_chain_index,
            residual.expected_pair_chain_index,
        )
        for residual in records[0].source_bead_residuals
    ) == (
        (1, 2, 268, 268),
        (1, 3, 241, 241),
        (1, 4, 160, 160),
        (1, 5, 130, 130),
    )
    assert "max node source bead delta" in text
    assert "max source delta chain" in text
    assert "source bead residual details" in text
    assert "c1n5[130->130]: 3.92204!=5.39(d=1.46796)" in text


def test_compare_spplus_pairing_when_pairing_differs_reports_mismatch() -> None:
    original = _spplus_snapshot_text().replace(
        "1       2       1",
        "1       2       2",
        1,
    )

    comparison = compare_spplus_pairing(_spplus_snapshot_text(), original)

    assert comparison.mismatched_pair_count == 1


def test_build_summary_outputs_when_oracle_spplus_path_matches_ne_coil() -> None:
    snapshot = read_z1_file(SOURCE_Z1 / ".benchmark-04.Z1")
    oracle_path = read_shortest_path_file(
        ORACLE_ROOT / "benchmark-04" / "spplus" / "Z1+SP.dat",
    )
    oracle_summary = read_summary_file(
        ORACLE_ROOT / "benchmark-04" / "spplus" / "Z1+summary.dat",
    )[0]

    outputs = build_summary_outputs(
        original=snapshot,
        primitive_path=oracle_path,
        timestep=snapshot.label or 1,
    )

    assert (
        abs(outputs.record.ne_classical_coil - oracle_summary.ne_classical_coil)
        < 0.001
    )
    assert (
        abs(outputs.record.ne_modified_coil - oracle_summary.ne_modified_coil)
        < 0.002
    )


def _spplus_snapshot_text() -> str:
    return (ORACLE_ROOT / "benchmark-04" / "spplus" / "Z1+SP.dat").read_text(
        encoding="utf-8",
    )


def assert_benchmark_04_max_delta_location(record: RegressionRecord) -> None:
    assert record.max_node_delta_chain_index == 1
    assert record.max_node_delta_node_index == 2
    assert record.max_node_delta_actual_source_bead == 3.5
    assert record.max_node_delta_expected_source_bead == 3.5


def assert_benchmark_04_max_delta_pair_geometry(record: RegressionRecord) -> None:
    assert record.max_node_actual_pair_fraction is not None
    assert 0.732 < record.max_node_actual_pair_fraction < 0.734
    assert record.max_node_actual_pair_distance is not None
    assert 0.0016 < record.max_node_actual_pair_distance < 0.0017
    assert record.max_node_expected_pair_fraction is not None
    assert 0.733 < record.max_node_expected_pair_fraction < 0.734
    assert record.max_node_expected_pair_distance is not None
    assert 0.0017 < record.max_node_expected_pair_distance < 0.0019
    assert record.max_node_position_delta is not None
    assert record.max_node_position_delta < 0.0005
