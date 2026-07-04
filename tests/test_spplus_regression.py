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
    assert "| benchmark-04 | spplus |" in text
    assert "summary field mismatches" in text
    assert "max node position delta" in text
    assert "node count mismatches" in text
    assert records[1].summary_field_mismatches == 1
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
    assert "ne_modified_coil: 641.051 != 641.605" in text
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
    assert "| benchmark-04 | spplus | mismatch |" in text
    assert "max node delta chain" in text
    assert "| 1 | 2 | 3.5 | 3.5 |" in text
    assert "max node actual pair fraction" in text
    assert "| 0.733072 | 0.00186654 | 0.733114 | 0.00179606 |" in text


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
    assert 0.0018 < record.max_node_actual_pair_distance < 0.0019
    assert record.max_node_expected_pair_fraction is not None
    assert 0.733 < record.max_node_expected_pair_fraction < 0.734
    assert record.max_node_expected_pair_distance is not None
    assert 0.0017 < record.max_node_expected_pair_distance < 0.0019
    assert record.max_node_position_delta is not None
    assert record.max_node_position_delta < 0.0005
