from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Final

import typer

from pyz1.errors import InputFileMissingError
from pyz1.ppa import (
    PpaMode,
    accelerated_ppa_settings,
    run_ppa,
    standard_ppa_settings,
    write_ppa_outputs,
)
from pyz1.reducer import reduce_snapshot, write_reducer_outputs
from pyz1.z1_io import read_z1_file

COMPATIBILITY_HELP: Final = """

Z1+ compatible options:

  -h
  -c or -clean
  -l or -log
  -s or -stats
  -0 or -selfZ
  +  or -SP+
  -t or -PPA
  -p or -PPA+
  -from=snapshot-no
  -to=snapshot-no
  -ignore_H
  -ignore_type1=type-no
  -ignore_type2=type-no
"""

CLEAN_FILENAMES: Final = (
    "Z1+SP.dat",
    "log.Z1",
    "Z1+parameters",
    "Z1+summary.dat",
    "Z1+summary.html",
    "Z1+initconfig.dat",
    "Ree_values.dat",
    "Lpp_values.dat",
    "N_values.dat",
    "Z_values.dat",
    "PPA.dat",
    "PPA+.dat",
    "PPA-summary.dat",
    "PPA-summary.html",
    "PPA+summary.dat",
    "PPA+summary.html",
)

MODE_OPTIONS: Final = {
    "+": "spplus",
    "-SP+": "spplus",
    "-t": "ppa",
    "-PPA": "ppa",
    "-p": "ppaplus",
    "-PPA+": "ppaplus",
}

BOOLEAN_OPTIONS: Final = {
    "-c",
    "-clean",
    "-l",
    "-log",
    "-s",
    "-stats",
    "-0",
    "-selfZ",
    "-ignore_H",
}

VALUE_OPTION_PREFIXES: Final = (
    "-from=",
    "-to=",
    "-ignore_type1=",
    "-ignore_type2=",
)

app = typer.Typer(
    add_completion=False,
    help=(
        "pyz1 clean-room Python workflow for Z1+ compatible analyses."
        f"{COMPATIBILITY_HELP}"
    ),
    no_args_is_help=True,
)


@dataclass(frozen=True, slots=True)
class ParsedCli:
    input_file: Path | None
    clean: bool
    mode: str


@app.command(
    context_settings={
        "allow_extra_args": True,
        "help_option_names": ("-h", "--help"),
        "ignore_unknown_options": True,
    },
    help=(
        "pyz1 clean-room Python workflow for Z1+ compatible analyses."
        f"{COMPATIBILITY_HELP}"
    ),
)
def run(
    ctx: typer.Context,
    args: Annotated[list[str] | None, typer.Argument()] = None,
) -> None:
    parsed = _parse_args(tuple(args or ()))
    if parsed.clean:
        _clean_outputs(Path.cwd())
        typer.echo("[pyz1] finished cleaning")
        return
    if parsed.input_file is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=0)
    if not parsed.input_file.exists():
        typer.echo(str(InputFileMissingError(path=parsed.input_file)))
        raise typer.Exit(code=2)

    if parsed.mode == "default":
        _run_default_mode(parsed)
        return
    if parsed.mode in ("ppa", "ppaplus"):
        _run_ppa_mode(parsed)
        return

    typer.echo(f"pyz1 {parsed.mode} mode is not implemented yet.")
    raise typer.Exit(code=3)


def _parse_args(args: tuple[str, ...]) -> ParsedCli:
    clean = False
    mode = "default"
    input_file: Path | None = None
    for arg in args:
        if arg in ("-c", "-clean"):
            clean = True
            continue
        if arg in MODE_OPTIONS:
            mode = MODE_OPTIONS[arg]
            continue
        if arg in BOOLEAN_OPTIONS or arg.startswith(VALUE_OPTION_PREFIXES):
            continue
        if arg.startswith("-"):
            typer.echo(f"unknown option: {arg}")
            raise typer.Exit(code=2)
        if input_file is not None:
            typer.echo(f"unexpected argument: {arg}")
            raise typer.Exit(code=2)
        input_file = Path(arg)
    return ParsedCli(input_file=input_file, clean=clean, mode=mode)


def _clean_outputs(directory: Path) -> None:
    for filename in CLEAN_FILENAMES:
        path = directory / filename
        if path.exists():
            path.unlink()


def _run_default_mode(parsed: ParsedCli) -> None:
    if parsed.input_file is None:
        typer.echo("default mode requires an input file")
        raise typer.Exit(code=2)
    snapshot = read_z1_file(parsed.input_file)
    write_reducer_outputs(Path.cwd(), reduce_snapshot(snapshot))
    typer.echo("[pyz1] completed default")


def _run_ppa_mode(parsed: ParsedCli) -> None:
    if parsed.input_file is None:
        typer.echo("PPA mode requires an input file")
        raise typer.Exit(code=2)
    snapshot = read_z1_file(parsed.input_file)
    match parsed.mode:
        case "ppa":
            mode = PpaMode.STANDARD
            settings = standard_ppa_settings()
        case "ppaplus":
            mode = PpaMode.ACCELERATED
            settings = accelerated_ppa_settings()
        case _:
            typer.echo(f"pyz1 {parsed.mode} mode is not implemented yet.")
            raise typer.Exit(code=3)
    result = run_ppa(snapshot, settings)
    write_ppa_outputs(Path.cwd(), result, mode)
    typer.echo(f"[pyz1] completed {parsed.mode}")
