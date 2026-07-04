from __future__ import annotations

from typing import TYPE_CHECKING

from typer.testing import CliRunner

from pyz1.cli import app

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_help_lists_project_name() -> None:
    result = CliRunner().invoke(app, ["--help"], prog_name="pyz1")

    assert result.exit_code == 0
    assert "pyz1" in result.stdout
    assert "-clean" in result.stdout
    assert "-selfZ" in result.stdout
    assert "-SP+" in result.stdout
    assert "-PPA" in result.stdout
    assert "-PPA+" in result.stdout
    assert "-from=snapshot-no" in result.stdout
    assert "-ignore_H" in result.stdout


def test_missing_input_fails_with_clear_message(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.Z1"

    result = CliRunner().invoke(app, [str(missing_path)])

    assert result.exit_code != 0
    assert "input file does not exist" in result.stdout


def test_clean_removes_z1plus_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for filename in (
        "Z1+SP.dat",
        "Z1+summary.dat",
        "Z1+initconfig.dat",
        "Ree_values.dat",
        "Lpp_values.dat",
        "N_values.dat",
        "Z_values.dat",
        "PPA.dat",
        "PPA+summary.dat",
        "log.Z1",
    ):
        _ = (tmp_path / filename).write_text("stale\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["-clean"], prog_name="pyz1")

    assert result.exit_code == 0
    assert "finished cleaning" in result.stdout
    assert not any(tmp_path.iterdir())


def test_default_analysis_mode_writes_z1_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "config.Z1"
    _ = input_path.write_text("1\n10 10 10\n3\n0 0 0\n1 0 0\n2 0 0\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, [str(input_path)], prog_name="pyz1")

    assert result.exit_code == 0
    assert "completed default" in result.stdout
    assert (tmp_path / "Z1+SP.dat").exists()
    assert (tmp_path / "Z1+summary.dat").exists()


def test_spplus_analysis_mode_fails_clearly_until_pairing_exists(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "config.Z1"
    _ = input_path.write_text("1\n10 10 10\n3\n0 0 0\n1 0 0\n2 0 0\n", encoding="utf-8")

    result = CliRunner().invoke(app, ["-SP+", str(input_path)], prog_name="pyz1")

    assert result.exit_code != 0
    assert "spplus mode is not implemented yet" in result.stdout


def test_ppa_mode_writes_ppa_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "config.Z1"
    _ = input_path.write_text(
        "1\n10 10 10\n3\n0 0 0\n0.5 0.2 0\n1 0 0\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["-PPA", str(input_path)], prog_name="pyz1")

    assert result.exit_code == 0
    assert "completed ppa" in result.stdout
    assert (tmp_path / "PPA.dat").exists()
    assert (tmp_path / "PPA-summary.dat").exists()
    assert (tmp_path / "Lpp_values.dat").exists()


def test_ppaplus_mode_writes_ppaplus_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    input_path = tmp_path / "config.Z1"
    _ = input_path.write_text(
        "1\n10 10 10\n3\n0 0 0\n0.5 0.2 0\n1 0 0\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["-PPA+", str(input_path)], prog_name="pyz1")

    assert result.exit_code == 0
    assert "completed ppaplus" in result.stdout
    assert (tmp_path / "PPA+.dat").exists()
    assert (tmp_path / "PPA+summary.dat").exists()
