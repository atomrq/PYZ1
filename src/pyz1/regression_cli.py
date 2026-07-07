from __future__ import annotations

from pathlib import Path
from typing import Annotated, Final

import typer

from pyz1.reducer import ReducerSettings
from pyz1.regression import (
    RegressionMode,
    RegressionRequest,
    RegressionSettingsOverride,
    write_benchmark_regression_report,
)

DEFAULT_SOURCE_DIR: Final = Path("/Users/jiaxm/Contents/CodexProjects/source_code/Z1+")
DEFAULT_ORACLE_ROOT: Final = Path(
    "tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703",
)
DEFAULT_REPORT_PATH: Final = Path("pyz1-benchmark-regression.md")
DEFAULT_MODES: Final = (
    RegressionMode.DEFAULT,
    RegressionMode.SPPLUS,
    RegressionMode.SELFZ,
)

app = typer.Typer(
    add_completion=False,
    help="Write a pyz1 default/SP+/selfZ benchmark regression report.",
)


@app.callback(invoke_without_command=True)
def main(  # noqa: PLR0913 - Typer callback parameters define the CLI surface.
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
            help="Z1+ default/SP+/selfZ oracle corpus root.",
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
        list[RegressionMode] | None,
        typer.Option(
            "--mode",
            help="Regression mode to include, repeatable.",
        ),
    ] = None,
    max_node_count: Annotated[
        int,
        typer.Option(
            "--max-node-count",
            help="Skip benchmarks above this source node count.",
        ),
    ] = 1000,
    trace_diagnostics_max_node_count: Annotated[
        int,
        typer.Option(
            "--trace-diagnostics-max-node-count",
            help="Disable expensive trace diagnostics above this source node count.",
        ),
    ] = 1000,
    contact_relaxation: Annotated[
        bool,
        typer.Option(
            "--contact-relaxation/--no-contact-relaxation",
            help="Enable the experimental contact-relaxation reducer guard for SP+.",
        ),
    ] = False,
) -> None:
    requested_benchmark_ids = (
        tuple(benchmark_ids)
        if benchmark_ids is not None
        else discover_benchmark_ids(oracle_root)
    )
    requested_modes = tuple(modes) if modes is not None else DEFAULT_MODES
    records = write_benchmark_regression_report(
        RegressionRequest(
            source_dir=source_dir,
            oracle_root=oracle_root,
            report_path=report_path,
            modes=requested_modes,
            benchmark_ids=requested_benchmark_ids,
            max_node_count=max_node_count,
            trace_diagnostics_max_node_count=trace_diagnostics_max_node_count,
            settings_overrides=_settings_overrides(contact_relaxation),
        ),
    )
    typer.echo(
        f"[pyz1] wrote {len(records)} benchmark regression records to {report_path}",
    )


def discover_benchmark_ids(oracle_root: Path) -> tuple[str, ...]:
    return tuple(
        path.name.removeprefix("benchmark-")
        for path in sorted(oracle_root.glob("benchmark-*"))
        if path.is_dir()
    )


def _settings_overrides(
    contact_relaxation: bool,
) -> tuple[RegressionSettingsOverride, ...]:
    if not contact_relaxation:
        return ()
    return (
        RegressionSettingsOverride(
            mode=RegressionMode.SPPLUS,
            settings=ReducerSettings(
                pairing_enabled=True,
                contact_relaxation_enabled=True,
            ),
        ),
    )


if __name__ == "__main__":
    app()
