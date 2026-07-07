from __future__ import annotations

from pathlib import Path
from typing import Annotated, Final

import typer

from pyz1.corpus_smoke import (
    CorpusSmokeReportRequest,
    write_corpus_smoke_report,
)

DEFAULT_BENCHMARK_ROOT: Final = (
    Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code")
    / "benchmark-configurations"
)
DEFAULT_REPORT_PATH: Final = Path("pyz1-corpus-stat-smoke.md")
DEFAULT_BENCHMARK_IDS: Final = ("07", "10", "11")

app = typer.Typer(
    add_completion=False,
    help="Write a smoke report for benchmark input/reference statistic alignment.",
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
) -> None:
    requested_benchmark_ids = (
        tuple(benchmark_ids) if benchmark_ids is not None else DEFAULT_BENCHMARK_IDS
    )
    records = write_corpus_smoke_report(
        CorpusSmokeReportRequest(
            benchmark_root=benchmark_root,
            report_path=report_path,
            benchmark_ids=requested_benchmark_ids,
        ),
    )
    typer.echo(f"wrote {len(records)} corpus smoke records to {report_path}")


if __name__ == "__main__":
    app()
