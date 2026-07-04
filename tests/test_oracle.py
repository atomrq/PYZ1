from __future__ import annotations

import stat
import subprocess
import sys
from pathlib import Path

import pytest

from pyz1.oracle import OraclePlatformError, generate_oracle_fixtures
from pyz1.oracle_models import OracleGenerationRequest

NEWLINE = "\n"


def test_generate_oracle_fixtures_when_fake_wrapper_succeeds(tmp_path: Path) -> None:
    install_dir = tmp_path / "install"
    benchmarks_dir = tmp_path / "benchmarks"
    out_dir = tmp_path / "oracle"
    _write_fake_install(install_dir)
    _write_benchmark(benchmarks_dir / ".benchmark-01.Z1")
    _write_benchmark(benchmarks_dir / ".benchmark-02.Z1")

    request = OracleGenerationRequest(
        benchmarks_dir=benchmarks_dir,
        out_dir=out_dir,
        z1_install_dir=install_dir,
        mode_names=("default", "spplus"),
        allow_non_linux=True,
        platform_name="Darwin",
        timeout_seconds=None,
    )
    manifest = generate_oracle_fixtures(request)

    assert len(manifest.runs) == 4
    manifest_text = (out_dir / "manifest.json").read_text(encoding="utf-8")
    assert '"schema_version": 1' in manifest_text
    first_run = manifest.runs[0]
    assert first_run.exit_code == 0
    assert first_run.summary_rows == 1
    assert first_run.outputs["summary"].endswith("Z1+summary.dat")
    assert first_run.output_sha256["summary"]


def test_generate_oracle_fixtures_when_macos_without_executor_fails(
    tmp_path: Path,
) -> None:
    request = OracleGenerationRequest(
        benchmarks_dir=tmp_path,
        out_dir=tmp_path / "out",
        z1_install_dir=tmp_path / "install",
        mode_names=("default",),
        allow_non_linux=False,
        platform_name="Darwin",
        timeout_seconds=None,
    )

    with pytest.raises(OraclePlatformError, match="oracle requires Linux"):
        _ = generate_oracle_fixtures(request)


def test_generate_oracle_fixtures_when_wrapper_times_out_records_run(
    tmp_path: Path,
) -> None:
    install_dir = tmp_path / "install"
    benchmarks_dir = tmp_path / "benchmarks"
    out_dir = tmp_path / "oracle"
    _write_fake_install(install_dir, delay_seconds=2)
    _write_benchmark(benchmarks_dir / ".benchmark-01.Z1")
    request = OracleGenerationRequest(
        benchmarks_dir=benchmarks_dir,
        out_dir=out_dir,
        z1_install_dir=install_dir,
        mode_names=("default",),
        allow_non_linux=True,
        platform_name="Darwin",
        timeout_seconds=0.1,
    )

    manifest = generate_oracle_fixtures(request)

    assert len(manifest.runs) == 1
    run = manifest.runs[0]
    assert run.exit_code == 124
    assert run.summary_rows == 0
    assert run.output_sha256 == {}


def test_generate_oracle_fixtures_when_summary_is_unparseable_continues(
    tmp_path: Path,
) -> None:
    install_dir = tmp_path / "install"
    benchmarks_dir = tmp_path / "benchmarks"
    out_dir = tmp_path / "oracle"
    _write_fake_install(install_dir, summary_line="1 1 3 bad 2")
    _write_benchmark(benchmarks_dir / ".benchmark-01.Z1")
    request = OracleGenerationRequest(
        benchmarks_dir=benchmarks_dir,
        out_dir=out_dir,
        z1_install_dir=install_dir,
        mode_names=("default",),
        allow_non_linux=True,
        platform_name="Darwin",
        timeout_seconds=None,
    )

    manifest = generate_oracle_fixtures(request)

    assert len(manifest.runs) == 1
    run = manifest.runs[0]
    assert run.exit_code == 0
    assert run.summary_rows == 0
    assert run.output_sha256["summary"]


def test_generate_oracle_fixtures_when_paths_are_relative_runs_wrapper(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    install_dir = Path("install")
    benchmarks_dir = Path("benchmarks")
    out_dir = Path("oracle")
    _write_fake_install(install_dir)
    _write_benchmark(benchmarks_dir / ".benchmark-01.Z1")
    request = OracleGenerationRequest(
        benchmarks_dir=benchmarks_dir,
        out_dir=out_dir,
        z1_install_dir=install_dir,
        mode_names=("default",),
        allow_non_linux=True,
        platform_name="Darwin",
        timeout_seconds=None,
    )

    manifest = generate_oracle_fixtures(request)

    assert len(manifest.runs) == 1
    run = manifest.runs[0]
    assert run.exit_code == 0
    assert run.summary_rows == 1


def test_oracle_cli_module_when_help_requested_prints_usage() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pyz1.oracle_cli", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Usage: python -m pyz1.oracle_cli" in result.stdout
    assert "--benchmarks" in result.stdout
    assert "--z1-install" in result.stdout


def _write_benchmark(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = (
        "1",
        "10 10 10",
        "3",
        "0 0 0",
        "1 0 0",
        "2 0 0",
    )
    _ = path.write_text(NEWLINE.join(lines) + NEWLINE, encoding="utf-8")


def _write_fake_install(
    install_dir: Path,
    *,
    delay_seconds: int = 0,
    summary_line: str = "1 1 3 2 2 0 0 0 2 0 0 0 0 1 0.001",
) -> None:
    install_dir.mkdir(parents=True, exist_ok=True)
    wrapper = install_dir / "Z1+"
    _ = wrapper.write_text(
        _fake_wrapper_text(
            delay_seconds=delay_seconds,
            summary_line=summary_line,
        ),
        encoding="utf-8",
    )
    _ = wrapper.chmod(wrapper.stat().st_mode | stat.S_IXUSR)
    executable = install_dir / "Z1+.ex"
    _ = executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    _ = executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
    rearrange = install_dir / "Z1+rearrange.pl"
    _ = rearrange.write_text("#!/usr/bin/perl\n", encoding="utf-8")


def _fake_wrapper_text(*, delay_seconds: int, summary_line: str) -> str:
    lines = (
        "#!/bin/sh",
        "set -eu",
        f"sleep {delay_seconds}",
        "mode=default",
        'for arg in "$@"; do',
        '  if [ "$arg" = "+" ]; then mode=spplus; fi',
        "done",
        f"printf '{summary_line}\\n' > Z1+summary.dat",
        "printf '1\\n10 10 10\\n' > Z1+SP.dat",
        "printf '2\\n' >> Z1+SP.dat",
        "printf '0 0 0 1.00 0\\n' >> Z1+SP.dat",
        'if [ "$mode" = "spplus" ]; then',
        "  printf '2 0 0 3.00 1 1 1\\n' >> Z1+SP.dat",
        "else",
        "  printf '2 0 0 3.00 1\\n' >> Z1+SP.dat",
        "fi",
        "printf '1.0\\n' > .Z1+cpu+secs",
        "printf 'fake wrapper ok\\n'",
    )
    return NEWLINE.join(lines) + NEWLINE
