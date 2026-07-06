from __future__ import annotations

from pyz1.errors import LammpsParseError
from pyz1.lammps_common import LammpsBox, ParsedLine, parse_float
from pyz1.models import Vector3


def parse_dump_box(
    *,
    lines: tuple[ParsedLine, ...],
    cursor: int,
) -> tuple[LammpsBox, int]:
    header = lines[cursor]
    if header.text.startswith("ITEM: BOX BOUNDS xy"):
        return _parse_sheared_box(lines=lines, cursor=cursor)
    if header.text.startswith("ITEM: BOX BOUNDS"):
        return _parse_orthogonal_box(lines=lines, cursor=cursor)
    raise LammpsParseError(line_number=header.number, reason="unrecognized BOX BOUNDS")


def _parse_sheared_box(
    *,
    lines: tuple[ParsedLine, ...],
    cursor: int,
) -> tuple[LammpsBox, int]:
    x_fields = lines[cursor + 1].text.split()
    y_fields = lines[cursor + 2].text.split()
    z_fields = lines[cursor + 3].text.split()
    xy = parse_float(x_fields[2], line_number=lines[cursor + 1].number, name="xy")
    xlo_bound = _parse_bound(
        lines=lines,
        cursor=cursor + 1,
        fields=x_fields,
        name="xlo",
    )
    xhi_bound = _parse_bound(
        lines=lines,
        cursor=cursor + 1,
        fields=x_fields,
        name="xhi",
        index=1,
    )
    xlo = xlo_bound - min(0.0, xy)
    xhi = xhi_bound - max(0.0, xy)
    return (
        LammpsBox(
            low=Vector3(
                xlo,
                _parse_bound(
                    lines=lines, cursor=cursor + 2, fields=y_fields, name="ylo"
                ),
                _parse_bound(
                    lines=lines, cursor=cursor + 3, fields=z_fields, name="zlo"
                ),
            ),
            high=Vector3(
                xhi,
                _parse_bound(
                    lines=lines,
                    cursor=cursor + 2,
                    fields=y_fields,
                    name="yhi",
                    index=1,
                ),
                _parse_bound(
                    lines=lines,
                    cursor=cursor + 3,
                    fields=z_fields,
                    name="zhi",
                    index=1,
                ),
            ),
            shear=xy,
        ),
        cursor + 4,
    )


def _parse_orthogonal_box(
    *,
    lines: tuple[ParsedLine, ...],
    cursor: int,
) -> tuple[LammpsBox, int]:
    x_fields = lines[cursor + 1].text.split()
    y_fields = lines[cursor + 2].text.split()
    z_fields = lines[cursor + 3].text.split()
    return (
        LammpsBox(
            low=Vector3(
                _parse_bound(
                    lines=lines, cursor=cursor + 1, fields=x_fields, name="xlo"
                ),
                _parse_bound(
                    lines=lines, cursor=cursor + 2, fields=y_fields, name="ylo"
                ),
                _parse_bound(
                    lines=lines, cursor=cursor + 3, fields=z_fields, name="zlo"
                ),
            ),
            high=Vector3(
                _parse_bound(
                    lines=lines,
                    cursor=cursor + 1,
                    fields=x_fields,
                    name="xhi",
                    index=1,
                ),
                _parse_bound(
                    lines=lines,
                    cursor=cursor + 2,
                    fields=y_fields,
                    name="yhi",
                    index=1,
                ),
                _parse_bound(
                    lines=lines,
                    cursor=cursor + 3,
                    fields=z_fields,
                    name="zhi",
                    index=1,
                ),
            ),
            shear=0.0,
        ),
        cursor + 4,
    )


def _parse_bound(
    *,
    lines: tuple[ParsedLine, ...],
    cursor: int,
    fields: list[str],
    name: str,
    index: int = 0,
) -> float:
    return parse_float(fields[index], line_number=lines[cursor].number, name=name)
