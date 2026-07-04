from __future__ import annotations

import platform
from pathlib import Path  # noqa: TC003 - Typer resolves CLI parameter types.
from typing import Annotated

import typer

from pyz1.oracle import (
    MANIFEST_NAME,
    OracleInputError,
    OraclePlatformError,
    generate_oracle_fixtures,
)
from pyz1.oracle_models import OracleGenerationRequest

app = typer.Typer(add_completion=False, help="Generate Z1+ oracle fixtures.")


@app.command()
def generate(  # noqa: PLR0913 - Typer command parameters define the CLI surface.
    benchmarks: Annotated[
        Path,
        typer.Option(help="Directory containing .benchmark-XX.Z1 files."),
    ],
    out: Annotated[Path, typer.Option(help="Fixture output directory.")],
    z1_install: Annotated[
        Path,
        typer.Option(help="Directory containing Z1+, Z1+.ex, and Z1+rearrange.pl."),
    ],
    modes: Annotated[
        str,
        typer.Option(help="Comma-separated modes: default,spplus,selfz,ppa,ppaplus."),
    ] = "default,spplus,selfz,ppa,ppaplus",
    allow_non_linux: Annotated[
        bool,
        typer.Option(help="Allow local non-Linux execution for test fixtures."),
    ] = False,
    timeout_seconds: Annotated[
        float | None,
        typer.Option(help="Per-run timeout in seconds."),
    ] = None,
) -> None:
    mode_names = tuple(mode.strip() for mode in modes.split(",") if mode.strip())
    request = OracleGenerationRequest(
        benchmarks_dir=benchmarks,
        out_dir=out,
        z1_install_dir=z1_install,
        mode_names=mode_names,
        allow_non_linux=allow_non_linux,
        platform_name=platform.system(),
        timeout_seconds=timeout_seconds,
    )
    try:
        manifest = generate_oracle_fixtures(request)
    except OraclePlatformError as exc:
        _ = typer.echo(str(exc))
        raise typer.Exit(code=2) from exc
    except OracleInputError as exc:
        _ = typer.echo(str(exc))
        raise typer.Exit(code=2) from exc
    _ = typer.echo(f"wrote {out / MANIFEST_NAME} with {len(manifest.runs)} runs")


if __name__ == "__main__":
    app()
