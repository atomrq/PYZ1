from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pyz1.ppa_regression_cli import discover_benchmark_ids

SOURCE_Z1 = Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1+")
PPA_ORACLE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703")


def test_ppa_regression_cli_when_oracle_output_missing_writes_report(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-ppa-regression.md"

    result = subprocess.run(  # noqa: S603 - command is fixed package smoke.
        [
            sys.executable,
            "-m",
            "pyz1.ppa_regression_cli",
            "--source-dir",
            str(SOURCE_Z1),
            "--oracle-root",
            str(PPA_ORACLE_ROOT),
            "--report-path",
            str(report_path),
            "--benchmark-id",
            "02",
            "--max-node-count",
            "1000",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = report_path.read_text(encoding="utf-8")
    assert "wrote 2 native PPA regression records" in result.stdout
    assert "| benchmark-02 | ppa | known-invalid |" in text
    assert "| benchmark-02 | ppaplus | known-invalid |" in text


def test_discover_benchmark_ids_when_ppa_root_has_mixed_entries_returns_sorted_ids(
    tmp_path: Path,
) -> None:
    _ = (tmp_path / "benchmark-10").mkdir()
    _ = (tmp_path / "scratch").mkdir()
    _ = (tmp_path / "benchmark-02").mkdir()

    assert discover_benchmark_ids(tmp_path) == ("02", "10")
