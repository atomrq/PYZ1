from __future__ import annotations

from math import isclose, isnan
from pathlib import Path
from typing import Final

import pytest

from pyz1.output_io import (
    format_shortest_path_text,
    format_summary_text,
    parse_shortest_path_text,
    parse_summary_text,
    read_shortest_path_file,
    read_summary_file,
    write_shortest_path_file,
    write_summary_file,
)

FIXTURE_ROOT = Path("tests/fixtures/z1plus_oracle/benchmark-04")
FLOAT_TOLERANCE = 1.0e-9
OVERFLOW_SUMMARY_PREFIX: Final = "1 50 20.000 9.466 ************ -1.000 0.000"
OVERFLOW_SUMMARY_SUFFIX: Final = (
    "************ ************ -1.000 -1.000 0.000 0.000 1.000 0.125"
)
BAD_SUMMARY_PREFIX: Final = "1 50 20.000 9.466 bad -1.000 0.000"
BAD_SUMMARY_SUFFIX: Final = (
    "0.000 0.000 -1.000 -1.000 0.000 0.000 1.000 0.125"
)


def assert_close(actual: float, expected: float) -> None:
    assert isclose(actual, expected, rel_tol=FLOAT_TOLERANCE, abs_tol=FLOAT_TOLERANCE)


def assert_vector_close(
    actual: tuple[float, float, float],
    expected: tuple[float, float, float],
) -> None:
    assert_close(actual[0], expected[0])
    assert_close(actual[1], expected[1])
    assert_close(actual[2], expected[2])


def test_parse_basic_summary_when_benchmark_04_oracle() -> None:
    summary = read_summary_file(FIXTURE_ROOT / "basic" / "Z1+summary.dat")

    assert len(summary) == 1
    record = summary[0]
    assert record.timestep == 1
    assert record.true_chain_count == 5
    assert_close(record.mean_original_beads, 10.0)
    assert_close(record.mean_squared_end_to_end, 4.566)
    assert_close(record.mean_shortest_path_contour, 4.230)
    assert_close(record.mean_entanglements, 0.2)
    assert_close(record.coil_tube_diameter, 4.929)
    assert_close(record.coil_tube_step_length, 0.470)
    assert_close(record.root_mean_squared_contour, 4.598)
    assert_close(record.ne_classical_kink, 7.627)
    assert_close(record.ne_modified_kink, 50.0)
    assert_close(record.ne_classical_coil, 10.485)
    assert_close(record.ne_modified_coil, 641.605)
    assert_close(record.mean_original_bond_length, 1.0)
    assert_close(record.original_bead_density, 0.05)


def test_parse_sp_when_basic_oracle_has_no_pairing_columns() -> None:
    snapshot = read_shortest_path_file(FIXTURE_ROOT / "basic" / "Z1+SP.dat")

    assert snapshot.chain_count == 5
    assert_vector_close(snapshot.box.as_tuple(), (10.0, 10.0, 10.0))
    assert tuple(chain.node_count for chain in snapshot.chains) == (3, 2, 2, 2, 2)
    kink = snapshot.chains[0].nodes[1]
    assert_vector_close(kink.position.as_tuple(), (0.131523, -0.159638, 1.614837))
    assert_close(kink.source_bead, 3.5)
    assert kink.is_entanglement
    assert kink.pair is None


def test_parse_spplus_when_kink_has_pairing_columns() -> None:
    snapshot = read_shortest_path_file(FIXTURE_ROOT / "spplus" / "Z1+SP.dat")

    kink = snapshot.chains[0].nodes[1]
    assert kink.is_entanglement
    assert kink.pair is not None
    assert kink.pair.chain_index == 2
    assert kink.pair.node_index == 1


def test_malformed_summary_reports_column_count() -> None:
    with pytest.raises(ValueError, match="expected 15 summary columns"):
        _ = parse_summary_text("1 5 10.0\n")


def test_parse_summary_when_fortran_overflow_field_uses_nan() -> None:
    line = f"{OVERFLOW_SUMMARY_PREFIX} {OVERFLOW_SUMMARY_SUFFIX}"
    summary = parse_summary_text(f"{line}\n")

    record = summary[0]
    assert isnan(record.mean_shortest_path_contour)
    assert isnan(record.coil_tube_step_length)
    assert isnan(record.root_mean_squared_contour)
    assert_close(record.original_bead_density, 0.125)


def test_malformed_summary_float_still_fails() -> None:
    line = f"{BAD_SUMMARY_PREFIX} {BAD_SUMMARY_SUFFIX}"

    with pytest.raises(ValueError, match="invalid mean shortest path contour"):
        _ = parse_summary_text(f"{line}\n")


def test_format_summary_text_when_record_contains_fortran_overflow_nan(
    tmp_path: Path,
) -> None:
    summary = parse_summary_text(
        f"{OVERFLOW_SUMMARY_PREFIX} {OVERFLOW_SUMMARY_SUFFIX}\n",
    )
    path = tmp_path / "Z1+summary.dat"

    text = format_summary_text(summary)
    write_summary_file(path, summary)

    assert text.endswith("\n")
    assert "************" in text
    parsed = read_summary_file(path)
    assert len(parsed) == 1
    assert isnan(parsed[0].mean_shortest_path_contour)
    assert_close(parsed[0].original_bead_density, summary[0].original_bead_density)


def test_format_shortest_path_text_when_spplus_pairing_round_trips(
    tmp_path: Path,
) -> None:
    snapshot = read_shortest_path_file(FIXTURE_ROOT / "spplus" / "Z1+SP.dat")
    path = tmp_path / "Z1+SP.dat"

    text = format_shortest_path_text(snapshot)
    write_shortest_path_file(path, snapshot)

    assert text.startswith("5\n10.000000 10.000000 10.000000\n")
    assert " 2 1\n" in text
    assert read_shortest_path_file(path) == snapshot


def test_malformed_spplus_pairing_reports_missing_node() -> None:
    text = Path(FIXTURE_ROOT / "spplus" / "Z1+SP.dat").read_text(encoding="utf-8")
    malformed = text.replace("1       2       1", "1       2", 1)

    with pytest.raises(ValueError, match="expected 5 or 7 SP node columns"):
        _ = parse_shortest_path_text(malformed)
