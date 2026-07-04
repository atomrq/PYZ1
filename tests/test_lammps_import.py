from __future__ import annotations

import pytest

from pyz1.lammps_io import LammpsImportOptions, import_lammps_text

NEWLINE = "\n"


def test_import_data_builds_linear_chain_from_bonds() -> None:
    data_text = NEWLINE.join(
        (
            "LAMMPS data",
            "",
            "3 atoms",
            "2 bonds",
            "1 atom types",
            "1 bond types",
            "",
            "0 10 xlo xhi",
            "0 20 ylo yhi",
            "0 30 zlo zhi",
            "",
            "Masses",
            "",
            "1 12.0",
            "",
            "Atoms",
            "",
            "1 1 1 0.0 0.0 0.0",
            "2 1 1 1.0 0.0 0.0",
            "3 1 1 2.0 0.0 0.0",
            "",
            "Bonds",
            "",
            "1 1 1 2",
            "2 1 2 3",
        ),
    )

    snapshots = import_lammps_text(data_text=data_text)

    assert len(snapshots) == 1
    assert snapshots[0].box.as_tuple() == (10.0, 20.0, 30.0)
    assert snapshots[0].true_chain_lengths == (3,)
    assert snapshots[0].chains[0].nodes[2].as_tuple() == (2.0, 0.0, 0.0)


def test_import_data_ignores_hydrogen_branch_when_requested() -> None:
    data_text = NEWLINE.join(
        (
            "LAMMPS data",
            "",
            "4 atoms",
            "3 bonds",
            "2 atom types",
            "1 bond types",
            "",
            "0 10 xlo xhi",
            "0 10 ylo yhi",
            "0 10 zlo zhi",
            "",
            "Masses",
            "",
            "1 12.0",
            "2 1.0",
            "",
            "Atoms",
            "",
            "1 1 1 0.0 0.0 0.0",
            "2 1 1 1.0 0.0 0.0",
            "3 1 1 2.0 0.0 0.0",
            "4 1 2 1.0 1.0 0.0",
            "",
            "Bonds",
            "",
            "1 1 1 2",
            "2 1 2 3",
            "3 1 2 4",
        ),
    )

    snapshots = import_lammps_text(
        data_text=data_text,
        options=LammpsImportOptions(ignore_hydrogen=True),
    )

    assert snapshots[0].true_chain_lengths == (3,)
    assert tuple(node.as_tuple() for node in snapshots[0].chains[0].nodes) == (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (2.0, 0.0, 0.0),
    )


def test_import_data_ignores_configured_atom_types() -> None:
    data_text = NEWLINE.join(
        (
            "LAMMPS data",
            "",
            "4 atoms",
            "3 bonds",
            "2 atom types",
            "1 bond types",
            "",
            "0 10 xlo xhi",
            "0 10 ylo yhi",
            "0 10 zlo zhi",
            "",
            "Masses",
            "",
            "1 12.0",
            "2 16.0",
            "",
            "Atoms",
            "",
            "1 1 1 0.0 0.0 0.0",
            "2 1 1 1.0 0.0 0.0",
            "3 1 1 2.0 0.0 0.0",
            "4 1 2 1.0 1.0 0.0",
            "",
            "Bonds",
            "",
            "1 1 1 2",
            "2 1 2 3",
            "3 1 2 4",
        ),
    )

    snapshots = import_lammps_text(
        data_text=data_text,
        options=LammpsImportOptions(ignored_atom_types=frozenset((2,))),
    )

    assert snapshots[0].true_chain_lengths == (3,)


def test_import_dump_uses_data_bond_topology_when_available() -> None:
    data_text = NEWLINE.join(
        (
            "LAMMPS data",
            "",
            "3 atoms",
            "2 bonds",
            "1 atom types",
            "1 bond types",
            "",
            "0 10 xlo xhi",
            "0 10 ylo yhi",
            "0 10 zlo zhi",
            "",
            "Masses",
            "",
            "1 12.0",
            "",
            "Atoms",
            "",
            "10 1 1 0.0 0.0 0.0",
            "20 1 1 1.0 0.0 0.0",
            "30 1 1 2.0 0.0 0.0",
            "",
            "Bonds",
            "",
            "1 1 10 20",
            "2 1 20 30",
        ),
    )
    dump_text = NEWLINE.join(
        (
            "ITEM: TIMESTEP",
            "5",
            "ITEM: NUMBER OF ATOMS",
            "3",
            "ITEM: BOX BOUNDS",
            "0 10",
            "0 10",
            "0 10",
            "ITEM: ATOMS id mol type x y z",
            "10 9 1 0.0 1.0 0.0",
            "20 9 1 1.0 1.0 0.0",
            "30 9 1 2.0 1.0 0.0",
        ),
    )

    snapshots = import_lammps_text(data_text=data_text, dump_text=dump_text)

    assert snapshots[0].true_chain_lengths == (3,)
    assert snapshots[0].chains[0].nodes[0].as_tuple() == (0.0, 1.0, 0.0)
    assert snapshots[0].chains[0].nodes[2].as_tuple() == (2.0, 1.0, 0.0)


def test_import_dump_slices_frames_and_scales_fractional_coordinates() -> None:
    dump_text = NEWLINE.join(
        (
            "ITEM: TIMESTEP",
            "100",
            "ITEM: NUMBER OF ATOMS",
            "3",
            "ITEM: BOX BOUNDS",
            "0 10",
            "0 20",
            "0 30",
            "ITEM: ATOMS id mol type xs ys zs",
            "1 1 1 0.0 0.0 0.0",
            "2 1 1 0.1 0.0 0.0",
            "3 1 1 0.2 0.0 0.0",
            "ITEM: TIMESTEP",
            "200",
            "ITEM: NUMBER OF ATOMS",
            "3",
            "ITEM: BOX BOUNDS",
            "0 10",
            "0 20",
            "0 30",
            "ITEM: ATOMS id mol type xs ys zs",
            "1 1 1 0.0 0.1 0.0",
            "2 1 1 0.1 0.1 0.0",
            "3 1 1 0.2 0.1 0.0",
        ),
    )

    snapshots = import_lammps_text(
        dump_text=dump_text,
        options=LammpsImportOptions(first_snapshot=2, last_snapshot=2),
    )

    assert len(snapshots) == 1
    assert snapshots[0].label == 200
    assert snapshots[0].chains[0].nodes[1].as_tuple() == (1.0, 2.0, 0.0)


def test_import_data_without_bonds_fails_actionably() -> None:
    data_text = NEWLINE.join(
        (
            "LAMMPS data",
            "",
            "2 atoms",
            "0 bonds",
            "1 atom types",
            "",
            "0 10 xlo xhi",
            "0 10 ylo yhi",
            "0 10 zlo zhi",
            "",
            "Masses",
            "",
            "1 12.0",
            "",
            "Atoms",
            "",
            "1 1 1 0.0 0.0 0.0",
            "2 1 1 1.0 0.0 0.0",
        ),
    )

    with pytest.raises(ValueError, match="bond connectivity"):
        _ = import_lammps_text(data_text=data_text)
