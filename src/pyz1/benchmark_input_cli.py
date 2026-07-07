from __future__ import annotations

from pathlib import Path
from typing import Annotated, Final

import typer

from pyz1.benchmark_inputs import (
    BenchmarkInputFormat,
    BenchmarkInputReportRequest,
    discover_benchmark_input_ids,
    write_benchmark_input_report,
)

DEFAULT_BENCHMARK_ROOT: Final = (
    Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code")
    / "benchmark-configurations"
)
DEFAULT_REPORT_PATH: Final = Path("pyz1-benchmark-input-smoke.md")
DEFAULT_INPUT_FORMATS: Final = (BenchmarkInputFormat.Z1, BenchmarkInputFormat.DUMP)

app = typer.Typer(
    add_completion=False,
    help="Write a smoke report for public Z1plus-code benchmark inputs.",
)


@app.callback(invoke_without_command=True)
def main(
    benchmark_root: Annotated[
        Path,
        typer.Option(
            "--benchmark-root",
            help="Z1plus-code benchmark-configurations directory.",
        ),
    ] = DEFAULT_BENCHMARK_ROOT,
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
    input_formats: Annotated[
        list[BenchmarkInputFormat] | None,
        typer.Option(
            "--input-format",
            help="Input format to include, repeatable.",
        ),
    ] = None,
) -> None:
    requested_benchmark_ids = (
        tuple(benchmark_ids)
        if benchmark_ids is not None
        else discover_benchmark_input_ids(benchmark_root)
    )
    requested_formats = (
        tuple(input_formats) if input_formats is not None else DEFAULT_INPUT_FORMATS
    )
    records = write_benchmark_input_report(
        BenchmarkInputReportRequest(
            benchmark_root=benchmark_root,
            report_path=report_path,
            input_formats=requested_formats,
            benchmark_ids=requested_benchmark_ids,
        ),
    )
    typer.echo(f"wrote {len(records)} benchmark input smoke records to {report_path}")


if __name__ == "__main__":
    app()
