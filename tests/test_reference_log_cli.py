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
REFERENCE_ROOT = Z1PLUS_CODE_ROOT / "benchmark-configurations"


def test_reference_log_cli_when_requested_writes_report(tmp_path: Path) -> None:
    report_path = tmp_path / "reference-log-smoke.md"

    result = subprocess.run(  # noqa: S603 - command is fixed package smoke.
        [
            sys.executable,
            "-m",
            "pyz1.reference_log_cli",
            "--reference-root",
            str(REFERENCE_ROOT),
            "--report-path",
            str(report_path),
            "--benchmark-id",
            "07",
            "--mode",
            "ppaplus",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = report_path.read_text(encoding="utf-8")
    assert "wrote 1 reference log smoke records" in result.stdout
    assert "| benchmark-07 | ppaplus | parseable | 129 | 64.43319 |" in text
