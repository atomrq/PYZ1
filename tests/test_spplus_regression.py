from __future__ import annotations

from pathlib import Path
from shutil import copyfile

from pyz1.output_io import read_shortest_path_file, read_summary_file
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

SOURCE_Z1 = Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1+")
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
            modes=(RegressionMode.DEFAULT, RegressionMode.SPPLUS),
            benchmark_ids=("04",),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert len(records) == 2
    assert "| benchmark-04 | default |" in text
    assert "| benchmark-04 | spplus | passed |" in text
    assert tuple(record.status for record in records) == (
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
    assert benchmark_05.oracle_true_chain_pair_sequence == (40, 26)
    assert benchmark_05.pyz1_convex_winding_missing_oracle_sequence == (40, 26)
    assert "pyz1 convex winding candidates" in text
    assert "oracle true-chain pair sequence" in text


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
