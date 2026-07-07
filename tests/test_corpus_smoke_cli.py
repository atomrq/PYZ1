from __future__ import annotations

import subprocess
import sys
from os import environ
from pathlib import Path

Z1PLUS_CODE_ROOT = Path(
    environ.get(
        "PYZ1_Z1PLUS_CODE_ROOT",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code",
    ),
)
BENCHMARK_ROOT = Z1PLUS_CODE_ROOT / "benchmark-configurations"


def test_corpus_smoke_cli_when_requested_writes_report(tmp_path: Path) -> None:
    report_path = tmp_path / "corpus-stat-smoke.md"

    result = subprocess.run(  # noqa: S603 - command is fixed package smoke.
        [
            sys.executable,
            "-m",
            "pyz1.corpus_smoke_cli",
            "--benchmark-root",
            str(BENCHMARK_ROOT),
            "--report-path",
            str(report_path),
            "--benchmark-id",
            "07",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = report_path.read_text(encoding="utf-8")
    assert "wrote 1 corpus smoke records" in result.stdout
    assert "| benchmark-07 | passed | 129 | 12900 | 100 | 0 | 0 | 0 | 0 |" in text
