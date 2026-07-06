from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Final

from pyz1.errors import Z1OutputParseError
from pyz1.oracle_errors import OracleInputError, OraclePlatformError
from pyz1.oracle_install import (
    EXECUTABLE_NAME,
    WRAPPER_NAME,
    stage_oracle_install,
)
from pyz1.oracle_install import (
    PUBLIC_INSTALL_PATH as INSTALL_SOURCE_PATH,
)
from pyz1.oracle_models import (
    OracleGenerationRequest,
    OracleManifest,
    OracleMode,
    OracleRunRecord,
)
from pyz1.oracle_outcome import normalize_oracle_exit_code
from pyz1.output_io import read_summary_file

MANIFEST_NAME: Final = "manifest.json"
PUBLIC_INSTALL_PATH: Final = INSTALL_SOURCE_PATH

__all__: Final = (
    "PUBLIC_INSTALL_PATH",
    "OracleInputError",
    "OraclePlatformError",
    "generate_oracle_fixtures",
)

ORACLE_MODES: Final = (
    OracleMode(
        name="default",
        arguments=(),
        summary_filename="Z1+summary.dat",
        path_filename="Z1+SP.dat",
    ),
    OracleMode(
        name="spplus",
        arguments=("+",),
        summary_filename="Z1+summary.dat",
        path_filename="Z1+SP.dat",
    ),
    OracleMode(
        name="selfz",
        arguments=("-selfZ",),
        summary_filename="Z1+summary.dat",
        path_filename="Z1+SP.dat",
    ),
    OracleMode(
        name="ppa",
        arguments=("-PPA",),
        summary_filename="PPA-summary.dat",
        path_filename="PPA.dat",
    ),
    OracleMode(
        name="ppaplus",
        arguments=("-PPA+",),
        summary_filename="PPA+summary.dat",
        path_filename="PPA+.dat",
    ),
)


@dataclass(frozen=True, slots=True)
class CommandOutcome:
    exit_code: int
    stdout: str
    stderr: str


def generate_oracle_fixtures(request: OracleGenerationRequest) -> OracleManifest:
    if request.platform_name != "Linux" and not request.allow_non_linux:
        raise OraclePlatformError(platform_name=request.platform_name)
    benchmarks_dir = request.benchmarks_dir.resolve()
    out_dir = request.out_dir.resolve()
    z1_install_dir = request.z1_install_dir.resolve()
    benchmarks = _discover_benchmarks(benchmarks_dir)
    modes = _select_modes(request.mode_names)
    staged_install = stage_oracle_install(z1_install_dir, out_dir)
    runs = tuple(
        _run_benchmark_mode(
            benchmark=benchmark,
            mode=mode,
            staged_install=staged_install,
            out_dir=out_dir,
            timeout_seconds=request.timeout_seconds,
        )
        for benchmark in benchmarks
        for mode in modes
    )
    manifest = OracleManifest(
        schema_version=1,
        generator="pyz1.oracle",
        platform_name=request.platform_name,
        runs=runs,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    _ = (out_dir / MANIFEST_NAME).write_text(
        json.dumps(manifest.to_json(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def _discover_benchmarks(benchmarks_dir: Path) -> tuple[Path, ...]:
    if not benchmarks_dir.is_dir():
        raise OracleInputError(
            path=benchmarks_dir,
            reason="benchmark directory missing",
        )
    benchmarks = tuple(sorted(benchmarks_dir.glob(".benchmark-*.Z1")))
    if len(benchmarks) == 0:
        raise OracleInputError(path=benchmarks_dir, reason="no .benchmark-*.Z1 files")
    return benchmarks


def _select_modes(mode_names: tuple[str, ...]) -> tuple[OracleMode, ...]:
    return tuple(_mode_by_name(name) for name in mode_names)


def _mode_by_name(name: str) -> OracleMode:
    for mode in ORACLE_MODES:
        if mode.name == name:
            return mode
    raise OracleInputError(path=Path(name), reason="unknown oracle mode")


def _run_benchmark_mode(
    *,
    benchmark: Path,
    mode: OracleMode,
    staged_install: Path,
    out_dir: Path,
    timeout_seconds: float | None,
) -> OracleRunRecord:
    benchmark_name = benchmark.stem.removeprefix(".")
    run_dir = out_dir / benchmark_name / mode.name
    run_dir.mkdir(parents=True, exist_ok=True)
    local_input = run_dir / benchmark.name
    _ = shutil.copy2(benchmark, local_input)
    stdout_path = run_dir / "run.stdout"
    stderr_path = run_dir / "run.stderr"
    command = (str(staged_install / WRAPPER_NAME), *mode.arguments, benchmark.name)
    result = _run_command(
        command=command,
        cwd=run_dir,
        timeout_seconds=timeout_seconds,
    )
    _ = stdout_path.write_text(result.stdout, encoding="utf-8")
    _ = stderr_path.write_text(result.stderr, encoding="utf-8")
    summary_path = run_dir / mode.summary_filename
    path_path = run_dir / mode.path_filename
    output_paths = {"summary": summary_path, "path": path_path}
    summary_rows = _summary_row_count(summary_path)
    return OracleRunRecord(
        benchmark=benchmark.name,
        mode=mode.name,
        arguments=mode.arguments,
        exit_code=result.exit_code,
        summary_rows=summary_rows,
        input_sha256=_sha256_file(local_input),
        binary_sha256=_sha256_file(staged_install / EXECUTABLE_NAME),
        output_sha256=_hash_existing_outputs(output_paths),
        outputs=_relative_existing_outputs(output_paths, out_dir=out_dir),
        stdout_path=str(stdout_path.relative_to(out_dir)),
        stderr_path=str(stderr_path.relative_to(out_dir)),
        work_dir=str(run_dir.relative_to(out_dir)),
    )


def _run_command(
    *,
    command: tuple[str, ...],
    cwd: Path,
    timeout_seconds: float | None,
) -> CommandOutcome:
    try:
        result = subprocess.run(  # noqa: S603 - command is the staged Z1+ wrapper.
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return CommandOutcome(
            exit_code=124,
            stdout="",
            stderr=f"oracle run timed out after {timeout_seconds} seconds\n",
        )
    return CommandOutcome(
        exit_code=normalize_oracle_exit_code(
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        ),
        stdout=result.stdout,
        stderr=result.stderr,
    )


def _summary_row_count(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return len(read_summary_file(path))
    except Z1OutputParseError:
        return 0


def _hash_existing_outputs(paths: dict[str, Path]) -> dict[str, str]:
    return {
        name: _sha256_file(path)
        for name, path in paths.items()
        if path.exists()
    }


def _relative_existing_outputs(
    paths: dict[str, Path],
    *,
    out_dir: Path,
) -> dict[str, str]:
    return {
        name: str(path.relative_to(out_dir))
        for name, path in paths.items()
        if path.exists()
    }


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
