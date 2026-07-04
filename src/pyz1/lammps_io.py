from __future__ import annotations

from typing import TYPE_CHECKING

from pyz1.errors import LammpsParseError
from pyz1.lammps_data import LammpsDataParse, parse_lammps_data_text
from pyz1.lammps_dump import parse_lammps_dump_text
from pyz1.lammps_models import LammpsImportOptions

if TYPE_CHECKING:
    from pathlib import Path

    from pyz1.models import Snapshot

__all__ = ("LammpsImportOptions", "import_lammps_files", "import_lammps_text")


def import_lammps_text(
    *,
    data_text: str | None = None,
    dump_text: str | None = None,
    options: LammpsImportOptions | None = None,
) -> tuple[Snapshot, ...]:
    active_options = options or LammpsImportOptions()
    data_parse = _parse_optional_data(data_text=data_text, options=active_options)
    if dump_text is not None:
        topology = None if data_parse is None else data_parse.topology
        return parse_lammps_dump_text(
            dump_text,
            options=active_options,
            topology=topology,
        )
    if data_parse is not None:
        return (data_parse.to_snapshot(),)
    raise LammpsParseError(line_number=0, reason="missing dump AND/OR data file")


def import_lammps_files(
    *,
    data_path: Path | None = None,
    dump_path: Path | None = None,
    options: LammpsImportOptions | None = None,
) -> tuple[Snapshot, ...]:
    data_text = None if data_path is None else data_path.read_text(encoding="utf-8")
    dump_text = None if dump_path is None else dump_path.read_text(encoding="utf-8")
    return import_lammps_text(
        data_text=data_text,
        dump_text=dump_text,
        options=options,
    )


def _parse_optional_data(
    *,
    data_text: str | None,
    options: LammpsImportOptions,
) -> LammpsDataParse | None:
    if data_text is None:
        return None
    return parse_lammps_data_text(data_text, options=options)
