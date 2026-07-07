from __future__ import annotations

from os import environ
from pathlib import Path

from pyz1.benchmark_inputs import (
    BenchmarkInputFormat,
    BenchmarkInputReportRequest,
    BenchmarkInputStatus,
    write_benchmark_input_report,
)

Z1PLUS_CODE_ROOT = Path(
    environ.get(
        "PYZ1_Z1PLUS_CODE_ROOT",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code",
    ),
)
BENCHMARK_ROOT = Z1PLUS_CODE_ROOT / "benchmark-configurations"


def test_write_benchmark_input_report_when_z1_and_dump_exist_lists_smoke_records(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "benchmark-input-smoke.md"

    records = write_benchmark_input_report(
        BenchmarkInputReportRequest(
            benchmark_root=BENCHMARK_ROOT,
            report_path=report_path,
            input_formats=(BenchmarkInputFormat.Z1, BenchmarkInputFormat.DUMP),
            benchmark_ids=("07", "10", "11"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert len(records) == 6
    assert records[0].status == BenchmarkInputStatus.PARSEABLE
    assert records[0].input_format == BenchmarkInputFormat.Z1
    assert records[0].chain_count == 129
    assert records[0].node_count == 12900
    assert records[0].box_lengths == (24.0182, 24.0182, 24.0182)
    assert records[3].input_format == BenchmarkInputFormat.DUMP
    assert records[3].chain_count == 129
    assert records[3].node_count == 12900
    assert records[3].box_lengths == (24.0182, 24.0182, 24.0182)
    assert "| benchmark-11 | dump | parseable | 1044 | 104400 | 1044 |" in text
    assert "| benchmark-10 | z1 | parseable | 100 | 20000 | 100 |" in text
