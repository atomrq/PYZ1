from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pyz1.regression_cli import discover_benchmark_ids

SOURCE_Z1 = Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1+")
ORACLE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703")


def test_regression_cli_when_benchmark_requested_writes_report(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-benchmark-regression.md"

    result = subprocess.run(  # noqa: S603 - command is fixed package smoke.
        [
            sys.executable,
            "-m",
            "pyz1.regression_cli",
            "--source-dir",
            str(SOURCE_Z1),
            "--oracle-root",
            str(ORACLE_ROOT),
            "--report-path",
            str(report_path),
            "--benchmark-id",
            "04",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = report_path.read_text(encoding="utf-8")
    assert "wrote 2 benchmark regression records" in result.stdout
    assert "| benchmark-04 | default | passed |" in text
    assert "| benchmark-04 | spplus | passed |" in text


def test_discover_benchmark_ids_when_root_has_mixed_entries_returns_sorted_ids(
    tmp_path: Path,
) -> None:
    _ = (tmp_path / "benchmark-10").mkdir()
    _ = (tmp_path / "scratch").mkdir()
    _ = (tmp_path / "benchmark-02").mkdir()

    assert discover_benchmark_ids(tmp_path) == ("02", "10")
