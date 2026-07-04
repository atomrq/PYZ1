from __future__ import annotations

from pathlib import Path

from pyz1.ppa_oracle_coordinates import (
    PpaOracleCoordinateReportRequest,
    PpaOracleCoordinateStatus,
    write_ppa_oracle_coordinate_report,
)
from pyz1.ppa_regression import PpaRegressionMode

PPA_ORACLE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703")


def test_write_ppa_oracle_coordinate_report_when_corpus_has_mixed_statuses(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "ppa-oracle-coordinates.md"

    records = write_ppa_oracle_coordinate_report(
        PpaOracleCoordinateReportRequest(
            oracle_root=PPA_ORACLE_ROOT,
            report_path=report_path,
            modes=(PpaRegressionMode.STANDARD, PpaRegressionMode.ACCELERATED),
            benchmark_ids=("01", "04", "05"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert len(records) == 6
    assert records[0].status == PpaOracleCoordinateStatus.PARSEABLE
    assert records[0].node_count == 611
    assert records[3].status == PpaOracleCoordinateStatus.PARSEABLE
    assert records[3].node_count == 50
    assert records[4].status == PpaOracleCoordinateStatus.MISSING
    assert records[5].status == PpaOracleCoordinateStatus.INVALID
    assert records[5].error_line == 310
    assert records[5].error_reason == "invalid float"
    assert "| benchmark-05 | ppa | PPA.dat | missing | n/a | n/a | n/a |" in text
    assert (
        "| benchmark-05 | ppaplus | PPA+.dat | "
        "invalid | n/a | 310 | invalid float |"
    ) in text
