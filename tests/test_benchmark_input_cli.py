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


def test_benchmark_input_cli_when_requested_writes_report(tmp_path: Path) -> None:
    report_path = tmp_path / "benchmark-input-smoke.md"

    result = subprocess.run(  # noqa: S603 - command is fixed package smoke.
        [
            sys.executable,
            "-m",
            "pyz1.benchmark_input_cli",
            "--benchmark-root",
            str(BENCHMARK_ROOT),
            "--report-path",
            str(report_path),
            "--benchmark-id",
            "07",
            "--input-format",
            "dump",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = report_path.read_text(encoding="utf-8")
    assert "wrote 1 benchmark input smoke records" in result.stdout
    assert "| benchmark-07 | dump | parseable | 129 | 12900 | 129 |" in text
