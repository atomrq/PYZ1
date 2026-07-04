from __future__ import annotations

from pathlib import Path

from pyz1.ppa import PpaMode, PpaPhase, PpaSettings
from pyz1.ppa_regression import (
    PpaRegressionMode,
    PpaRegressionRequest,
    PpaRegressionSettingsOverride,
    write_ppa_regression_report,
)

SOURCE_Z1 = Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1+")
PPA_ORACLE_ROOT = Path("tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703")


def test_write_ppa_regression_report_when_oracles_exist_lists_native_modes(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "pyz1-ppa-regression.md"

    records = write_ppa_regression_report(
        PpaRegressionRequest(
            source_dir=SOURCE_Z1,
            oracle_root=PPA_ORACLE_ROOT,
            report_path=report_path,
            modes=(PpaRegressionMode.STANDARD, PpaRegressionMode.ACCELERATED),
            benchmark_ids=("04",),
            settings_overrides=(
                PpaRegressionSettingsOverride(
                    mode=PpaRegressionMode.STANDARD,
                    settings=_quick_settings(PpaMode.STANDARD),
                ),
                PpaRegressionSettingsOverride(
                    mode=PpaRegressionMode.ACCELERATED,
                    settings=_quick_settings(PpaMode.ACCELERATED),
                ),
            ),
        ),
    )

    text = report_path.read_text(encoding="utf-8")
    assert len(records) == 2
    assert "| benchmark-04 | ppa |" in text
    assert "| benchmark-04 | ppaplus |" in text
    assert "native PPA summary regression" in text
    assert records[0].status == "mismatch"
    assert records[0].summary_field_mismatches is not None
    assert records[0].summary_field_mismatches > 0
    assert records[0].mean_shortest_path_contour_delta is not None
    assert records[0].mean_shortest_path_contour_delta > 0.0
    assert records[1].status == "mismatch"


def _quick_settings(mode: PpaMode) -> PpaSettings:
    return PpaSettings(
        mode=mode,
        phases=(PpaPhase(timestep=0.001, temperature=0.0, step_count=80, skin=0.7),),
    )
