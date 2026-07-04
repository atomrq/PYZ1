from __future__ import annotations

from pathlib import Path
from typing import Annotated, Final

import typer

from pyz1.ppa_regression import (
    PpaRegressionMode,
    PpaRegressionRequest,
    write_ppa_regression_report,
)

DEFAULT_SOURCE_DIR: Final = Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1+")
DEFAULT_ORACLE_ROOT: Final = Path(
    "tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703",
)
DEFAULT_REPORT_PATH: Final = Path("pyz1-ppa-regression.md")
DEFAULT_MODES: Final = (
    PpaRegressionMode.STANDARD,
    PpaRegressionMode.ACCELERATED,
)

app = typer.Typer(
    add_completion=False,
    help="Write a pyz1 native PPA/PPA+ summary regression report.",
)


@app.callback(invoke_without_command=True)
def main(
    source_dir: Annotated[
        Path,
        typer.Option(
            "--source-dir",
            help="Z1+ source directory containing .benchmark-*.Z1 files.",
        ),
    ] = DEFAULT_SOURCE_DIR,
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
    max_node_count: Annotated[
        int,
        typer.Option(
            "--max-node-count",
            help="Skip benchmarks above this source node count.",
        ),
    ] = 1000,
) -> None:
    requested_benchmark_ids = (
        tuple(benchmark_ids)
        if benchmark_ids is not None
        else discover_benchmark_ids(oracle_root)
    )
    records = write_ppa_regression_report(
        PpaRegressionRequest(
            source_dir=source_dir,
            oracle_root=oracle_root,
            report_path=report_path,
            modes=DEFAULT_MODES,
            benchmark_ids=requested_benchmark_ids,
            max_node_count=max_node_count,
        ),
    )
    typer.echo(
        f"[pyz1] wrote {len(records)} native PPA regression records to {report_path}",
    )


def discover_benchmark_ids(oracle_root: Path) -> tuple[str, ...]:
    return tuple(
        path.name.removeprefix("benchmark-")
        for path in sorted(oracle_root.glob("benchmark-*"))
        if path.is_dir()
    )


if __name__ == "__main__":
    app()
