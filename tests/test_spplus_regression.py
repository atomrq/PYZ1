from __future__ import annotations

from pathlib import Path
from shutil import copyfile

from pyz1.regression import (
    RegressionMode,
    RegressionRequest,
    compare_spplus_pairing,
    write_benchmark_regression_report,
)

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
    assert records[1].summary_field_mismatches == 3
    assert records[1].node_count_mismatches == 0
    assert records[1].max_node_position_delta is not None
    assert 0.013 < records[1].max_node_position_delta < 0.014
    assert records[1].oracle_core_node_count == 17
    assert records[1].oracle_core_ghost_nodes == 6
    assert "root_mean_squared_contour: 4.597 != 4.598" in text
    assert "ne_modified_coil: 654.152 != 641.605" in text
    assert "oracle core ghosts" in text


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
    assert records[0].oracle_core_node_count == 17
    assert records[0].oracle_final_node_count == 11
    assert records[0].oracle_core_ghost_nodes == 6
    assert "pyz1 core nodes" in text
    assert "oracle core ghosts" in text
    assert "| benchmark-04 | spplus | mismatch |" in text
    assert "| 10 | 11 | 17 | 11 | 1 | 6 |" in text


def test_compare_spplus_pairing_when_pairing_differs_reports_mismatch() -> None:
    original = _spplus_snapshot_text().replace(
        "1       2       1",
        "1       2       2",
        1,
    )

    comparison = compare_spplus_pairing(_spplus_snapshot_text(), original)

    assert comparison.mismatched_pair_count == 1


def _spplus_snapshot_text() -> str:
    return (ORACLE_ROOT / "benchmark-04" / "spplus" / "Z1+SP.dat").read_text(
        encoding="utf-8",
    )
