from __future__ import annotations

import subprocess
import sys
from os import environ
from pathlib import Path

from pyz1.regression_cli import discover_benchmark_ids

SOURCE_Z1 = Path(
    environ.get(
        "PYZ1_SOURCE_Z1",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1+",
    ),
)
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
    assert "wrote 3 benchmark regression records" in result.stdout
    assert "| benchmark-04 | default | passed |" in text
    assert "| benchmark-04 | spplus | passed |" in text
    assert "| benchmark-04 | selfz | passed |" in text


def test_regression_cli_when_node_guard_requested_reports_known_invalid(
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
            "--max-node-count",
            "1",
            "--trace-diagnostics-max-node-count",
            "1",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = report_path.read_text(encoding="utf-8")
    assert "wrote 3 benchmark regression records" in result.stdout
    assert "| benchmark-04 | default | known-invalid |" in text
    assert "| benchmark-04 | spplus | known-invalid |" in text
    assert "| benchmark-04 | selfz | known-invalid |" in text
    assert "skipped: node_count>1" in text


def test_regression_cli_when_trace_guard_requested_disables_trace_diagnostics(
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
            "--mode",
            "spplus",
            "--trace-diagnostics-max-node-count",
            "1",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = report_path.read_text(encoding="utf-8")
    assert "wrote 1 benchmark regression records" in result.stdout
    assert "| benchmark-04 | spplus | passed |" in text
    assert "| 10 | 11 | 10 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a |" in text


def test_regression_cli_when_contact_relaxation_requested_writes_guarded_report(
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
            "05",
            "--mode",
            "spplus",
            "--contact-relaxation",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    text = report_path.read_text(encoding="utf-8")
    assert "wrote 1 benchmark regression records" in result.stdout
    expected_row = (
        "| benchmark-05 | spplus | mismatch | 0.00409694 | 0 | 0.886959 | 5 |"
    )
    assert expected_row in text
    assert "| 6 | 0 | 0 |" in text
    assert "| 0 | 0 | none |" in text


def test_discover_benchmark_ids_when_root_has_mixed_entries_returns_sorted_ids(
    tmp_path: Path,
) -> None:
    _ = (tmp_path / "benchmark-10").mkdir()
    _ = (tmp_path / "scratch").mkdir()
    _ = (tmp_path / "benchmark-02").mkdir()

    assert discover_benchmark_ids(tmp_path) == ("02", "10")
