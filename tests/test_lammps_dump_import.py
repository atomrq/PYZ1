from __future__ import annotations

from pyz1.lammps_io import import_lammps_text

NEWLINE = "\n"


def test_import_dump_when_negative_xy_triclinic_bounds_uses_z1plus_sign_rule() -> None:
    dump_text = NEWLINE.join(
        (
            "ITEM: TIMESTEP",
            "1",
            "ITEM: NUMBER OF ATOMS",
            "3",
            "ITEM: BOX BOUNDS xy xz yz pp pp pp",
            "-2 8 -2",
            "0 10 0",
            "0 10 0",
            "ITEM: ATOMS id mol type xs ys zs",
            "1 1 1 0.0 0.0 0.0",
            "2 1 1 0.5 0.0 0.0",
            "3 1 1 1.0 0.0 0.0",
        ),
    )

    snapshots = import_lammps_text(dump_text=dump_text)

    assert snapshots[0].shear == -2.0
    assert snapshots[0].box.as_tuple() == (8.0, 10.0, 10.0)
    assert snapshots[0].chains[0].nodes[1].as_tuple() == (4.0, 0.0, 0.0)
