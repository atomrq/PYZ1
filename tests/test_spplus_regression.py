from __future__ import annotations

from pathlib import Path

from pyz1.regression import (
    RegressionMode,
    RegressionRequest,
    compare_spplus_pairing,
    write_benchmark_regression_report,
)

SOURCE_Z1 = Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1+")
ORACLE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703")


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
    assert records[1].summary_field_mismatches == 3
    assert "root_mean_squared_contour: 4.597 != 4.598" in text
    assert "ne_modified_coil: 654.152 != 641.605" in text


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
