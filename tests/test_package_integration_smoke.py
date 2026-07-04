from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

NEWLINE = "\n"
SMOKE_INPUT = (
    "2",
    "10 10 10",
    "3 3",
    "0 0 0",
    "0 2 0",
    "1 1 0",
    "0.5 1.8 0",
    "0.5 0.8 0",
    "0.5 -0.2 0",
)


@dataclass(frozen=True, slots=True)
class PackageSmokeCase:
    name: str
    mode_args: tuple[str, ...]
    stdout_fragment: str
    expected_files: tuple[str, ...]


def test_package_entrypoint_when_modes_run_writes_expected_outputs(
    tmp_path: Path,
) -> None:
    for smoke_case in (
        PackageSmokeCase(
            name="default",
            mode_args=(),
            stdout_fragment="completed default",
            expected_files=(
                "Z1+SP.dat",
                "Z1+summary.dat",
                "Ree_values.dat",
                "Lpp_values.dat",
                "N_values.dat",
                "Z_values.dat",
            ),
        ),
        PackageSmokeCase(
            name="spplus",
            mode_args=("-SP+",),
            stdout_fragment="completed spplus",
            expected_files=("Z1+SP.dat", "Z1+summary.dat", "Lpp_values.dat"),
        ),
        PackageSmokeCase(
            name="ppa",
            mode_args=("-PPA",),
            stdout_fragment="completed ppa",
            expected_files=("PPA.dat", "PPA-summary.dat", "Lpp_values.dat"),
        ),
        PackageSmokeCase(
            name="ppaplus",
            mode_args=("-PPA+",),
            stdout_fragment="completed ppaplus",
            expected_files=("PPA+.dat", "PPA+summary.dat", "Lpp_values.dat"),
        ),
    ):
        case_dir = tmp_path / smoke_case.name
        case_dir.mkdir()
        input_path = case_dir / "config.Z1"
        _ = input_path.write_text(NEWLINE.join(SMOKE_INPUT) + NEWLINE, encoding="utf-8")

        result = subprocess.run(  # noqa: S603 - command is fixed package smoke.
            [
                sys.executable,
                "-m",
                "pyz1",
                *smoke_case.mode_args,
                str(input_path),
            ],
            cwd=case_dir,
            check=False,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, result.stdout + result.stderr
        assert smoke_case.stdout_fragment in result.stdout
        for filename in smoke_case.expected_files:
            assert (case_dir / filename).exists()
