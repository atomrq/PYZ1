from __future__ import annotations

from os import environ
from pathlib import Path

from pyz1.reference_logs import (
    ReferenceLogMode,
    ReferenceLogReportRequest,
    ReferenceLogStatus,
    write_reference_log_report,
)

Z1PLUS_CODE_ROOT = Path(
    environ.get(
        "PYZ1_Z1PLUS_CODE_ROOT",
        "/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code",
    ),
)
REFERENCE_ROOT = Z1PLUS_CODE_ROOT / "benchmark-configurations"


def test_write_reference_log_report_when_z1plus_code_logs_exist_lists_smoke_records(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "reference-log-smoke.md"

    records = write_reference_log_report(
        ReferenceLogReportRequest(
            reference_root=REFERENCE_ROOT,
            report_path=report_path,
            modes=(ReferenceLogMode.Z1PLUS, ReferenceLogMode.PPAPLUS),
            benchmark_ids=("07", "10", "11"),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert len(records) == 6
    assert records[0].status == ReferenceLogStatus.PARSEABLE
    assert records[0].chains == 129
    assert records[0].mean_shortest_path_contour == 57.13698
    assert records[0].mean_entanglements == 16.48062
    assert records[0].generated_files == (
        "N_values.dat",
        "Ree_values.dat",
        "Lpp_values.dat",
        "Z_values.dat",
        "Z1+SP.dat",
        "Z1+summary.dat",
        "Z1+summary.html",
        "Z1+initconfig.dat",
    )
    assert records[3].mode == ReferenceLogMode.PPAPLUS
    assert records[3].chains == 129
    assert records[3].mean_shortest_path_contour == 64.43319
    assert records[3].mean_entanglements == -1.0
    assert records[3].ne_classical_kink is None
    assert records[3].ne_classical_coil == 14.02370
    assert "| benchmark-11 | ppaplus | parseable | 1044 | 92.52998 |" in text
    assert "| benchmark-07 | z1plus | parseable | 129 | 57.13698 |" in text
