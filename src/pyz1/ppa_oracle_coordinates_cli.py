from __future__ import annotations

from pathlib import Path
from typing import Annotated, Final

import typer

from pyz1.ppa_oracle_coordinates import (
    PpaOracleCoordinateReportRequest,
    write_ppa_oracle_coordinate_report,
)
from pyz1.ppa_regression import PpaRegressionMode

DEFAULT_ORACLE_ROOT: Final = Path(
    "tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703",
)
DEFAULT_REPORT_PATH: Final = Path("ppa-oracle-coordinate-report.md")
DEFAULT_BENCHMARK_IDS: Final = (
    "01",
    "04",
    "05",
)
DEFAULT_MODES: Final = (
    PpaRegressionMode.STANDARD,
    PpaRegressionMode.ACCELERATED,
)

app = typer.Typer(
    add_completion=False,
    help="Write a parseability report for Z1+ PPA/PPA+ oracle coordinate files.",
)


@app.callback(invoke_without_command=True)
def main(
    oracle_root: Annotated[
        Path,
        typer.Option(
            "--oracle-root",
            help="Z1+ PPA/PPA+ oracle corpus root.",
        ),
    ] = DEFAULT_ORACLE_ROOT,
    report_path: Annotated[
        Path,
        typer.Option(
            "--report-path",
            help="Markdown report output path.",
        ),
    ] = DEFAULT_REPORT_PATH,
    benchmark_ids: Annotated[
        list[str] | None,
        typer.Option(
            "--benchmark-id",
            help="Benchmark id to include, repeatable.",
        ),
    ] = None,
    modes: Annotated[
        list[PpaRegressionMode] | None,
        typer.Option(
            "--mode",
            help="PPA oracle mode to include, repeatable.",
        ),
    ] = None,
) -> None:
    requested_benchmark_ids = (
        tuple(benchmark_ids)
        if benchmark_ids is not None
        else DEFAULT_BENCHMARK_IDS
    )
    requested_modes = tuple(modes) if modes is not None else DEFAULT_MODES
    records = write_ppa_oracle_coordinate_report(
        PpaOracleCoordinateReportRequest(
            oracle_root=oracle_root,
            report_path=report_path,
            modes=requested_modes,
            benchmark_ids=requested_benchmark_ids,
        ),
    )
    typer.echo(
        f"[pyz1] wrote {len(records)} PPA oracle coordinate records to {report_path}",
    )


if __name__ == "__main__":
    app()
