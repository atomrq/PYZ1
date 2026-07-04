from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PPA_ORACLE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703")


def test_ppa_oracle_coordinate_cli_when_mixed_corpus_writes_report(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "ppa-oracle-coordinate-report.md"

    result = subprocess.run(  # noqa: S603 - command is fixed package smoke.
        [
            sys.executable,
            "-m",
            "pyz1.ppa_oracle_coordinates_cli",
            "--oracle-root",
            str(PPA_ORACLE_ROOT),
            "--report-path",
            str(report_path),
            "--benchmark-id",
            "01",
            "--benchmark-id",
            "04",
            "--benchmark-id",
            "05",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = report_path.read_text(encoding="utf-8")
    assert "wrote 6 PPA oracle coordinate records" in result.stdout
    assert "| benchmark-01 | ppa | PPA.dat | parseable | 611 |" in text
    assert "| benchmark-05 | ppa | PPA.dat | missing | n/a |" in text
    assert "| benchmark-05 | ppaplus | PPA+.dat | invalid | n/a | 310 |" in text
