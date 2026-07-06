from __future__ import annotations

import shutil
from typing import TYPE_CHECKING, Final

from pyz1.oracle_errors import OracleInputError

if TYPE_CHECKING:
    from pathlib import Path

WRAPPER_NAME: Final = "Z1+"
EXECUTABLE_NAME: Final = "Z1+.ex"
REARRANGE_NAME: Final = "Z1+rearrange.pl"
PUBLIC_INSTALL_PATH: Final = "/Users/jiaxm/Contents/CodexProjects/source_code/Z1+"

WRAPPER_SOURCE_PATCHES: Final[tuple[tuple[str, str], ...]] = (
    (
        "$perl $installation_directory/Z1+import-lammps.pl -data=$configfile",
        '$perl "$installation_directory/Z1+import-lammps.pl" -data="$configfile"',
    ),
    (
        "$perl $installation_directory/Z1+import-lammps.pl -dump=$configfile",
        '$perl "$installation_directory/Z1+import-lammps.pl" -dump="$configfile"',
    ),
    (
        "$perl $installation_directory/Z1+import-lammps.pl -xml=$configfile",
        '$perl "$installation_directory/Z1+import-lammps.pl" -xml="$configfile"',
    ),
    (
        "cp $working_directory/$configfile config.Z1",
        'cp "$working_directory/$configfile" config.Z1',
    ),
    (
        "`$code`",
        '`"$code"`',
    ),
    (
        "$perl $installation_directory/Z1+rearrange.pl $SMDP",
        '$perl "$installation_directory/Z1+rearrange.pl" $SMDP',
    ),
)


def stage_oracle_install(source_dir: Path, out_dir: Path) -> Path:
    _require_file(source_dir / WRAPPER_NAME)
    _require_file(source_dir / EXECUTABLE_NAME)
    _require_file(source_dir / REARRANGE_NAME)
    staged_install = out_dir / "_z1plus_install"
    staged_install.mkdir(parents=True, exist_ok=True)
    for filename in (WRAPPER_NAME, EXECUTABLE_NAME, REARRANGE_NAME):
        _ = shutil.copy2(source_dir / filename, staged_install / filename)
    wrapper = staged_install / WRAPPER_NAME
    _ = wrapper.write_text(
        _patch_wrapper_text(
            wrapper.read_text(encoding="utf-8"),
            staged_install=staged_install,
        ),
        encoding="utf-8",
    )
    return staged_install


def _patch_wrapper_text(text: str, *, staged_install: Path) -> str:
    patched = text.replace(PUBLIC_INSTALL_PATH, str(staged_install))
    for old, new in WRAPPER_SOURCE_PATCHES:
        patched = patched.replace(old, new)
    return patched


def _require_file(path: Path) -> None:
    if not path.is_file():
        raise OracleInputError(path=path, reason="required file missing")
