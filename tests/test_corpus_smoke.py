from __future__ import annotations

from os import environ
from pathlib import Path

from pyz1.corpus_smoke import (
    CorpusSmokeReportRequest,
    CorpusSmokeStatus,
    write_corpus_smoke_report,
)

Z1PLUS_CODE_ROOT = Path(
    environ.get(
        "PYZ1_Z1PLUS_CODE_ROOT",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code",
    ),
)
BENCHMARK_ROOT = Z1PLUS_CODE_ROOT / "benchmark-configurations"


def test_write_corpus_smoke_report_when_inputs_and_logs_align_reports_passed(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "corpus-stat-smoke.md"

    records = write_corpus_smoke_report(
        CorpusSmokeReportRequest(
            benchmark_root=BENCHMARK_ROOT,
            report_path=report_path,
            benchmark_ids=("07", "10", "11"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert len(records) == 3
    assert tuple(record.status for record in records) == (
        CorpusSmokeStatus.PASSED,
        CorpusSmokeStatus.PASSED,
        CorpusSmokeStatus.PASSED,
    )
    assert records[0].input_chain_count == 129
    assert records[0].input_node_count == 12900
    assert records[0].input_mean_original_beads == 100.0
    assert records[2].input_chain_count == 1044
    assert records[2].input_node_count == 104400
    assert records[2].z1plus_mean_original_beads_delta == 0.0
    assert records[2].ppaplus_mean_original_beads_delta == 0.0
    assert "| benchmark-07 | passed | 129 | 12900 | 100 | 0 | 0 | 0 | 0 |" in text
    assert "| benchmark-11 | passed | 1044 | 104400 | 100 | 0 | 0 | 0 | 0 |" in text
