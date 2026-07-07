from __future__ import annotations

from pathlib import Path
from typing import Annotated, Final

import typer

from pyz1.reference_logs import (
    ReferenceLogMode,
    ReferenceLogReportRequest,
    discover_reference_log_benchmark_ids,
    write_reference_log_report,
)

DEFAULT_REFERENCE_ROOT: Final = (
    Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code")
    / "benchmark-configurations"
)
DEFAULT_REPORT_PATH: Final = Path("pyz1-reference-log-smoke.md")
DEFAULT_MODES: Final = (ReferenceLogMode.Z1PLUS, ReferenceLogMode.PPAPLUS)

app = typer.Typer(
    add_completion=False,
    help="Write a smoke report for public Z1+/PPA+ reference logs.",
)


@app.callback(invoke_without_command=True)
def main(
    reference_root: Annotated[
        Path,
        typer.Option(
            "--reference-root",
            help="Z1plus-code benchmark-configurations directory.",
        ),
    ] = DEFAULT_REFERENCE_ROOT,
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
        list[ReferenceLogMode] | None,
        typer.Option(
            "--mode",
            help="Reference mode to include, repeatable.",
        ),
    ] = None,
) -> None:
    requested_benchmark_ids = (
        tuple(benchmark_ids)
        if benchmark_ids is not None
        else discover_reference_log_benchmark_ids(reference_root)
    )
    requested_modes = tuple(modes) if modes is not None else DEFAULT_MODES
    records = write_reference_log_report(
        ReferenceLogReportRequest(
            reference_root=reference_root,
            report_path=report_path,
            modes=requested_modes,
            benchmark_ids=requested_benchmark_ids,
        ),
    )
    typer.echo(f"wrote {len(records)} reference log smoke records to {report_path}")


if __name__ == "__main__":
    app()
