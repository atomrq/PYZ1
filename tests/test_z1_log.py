from __future__ import annotations

from pathlib import Path

import pytest

from pyz1.z1_log import (
    parse_z1_log_text,
    read_z1_log_file,
    reducer_scan_diagnostics,
)

LOG_FIXTURE = Path("tests/fixtures/z1plus_oracle/benchmark-04/spplus/log-stats.Z1")


def test_parse_z1_log_text_when_stats_log_has_scan_table() -> None:
    log = read_z1_log_file(LOG_FIXTURE)

    assert len(log.scan_records) == 7
    assert log.scan_records[0].scan == 0
    assert log.scan_records[0].mean_shortest_path_contour == 9.0
    assert log.scan_records[2].crossings == 1
    assert log.scan_records[2].new_nodes == 1
    assert log.scan_records[5].node_count == 17
    assert log.scan_records[-1].node_count == 11
    assert log.scan_records[-1].mean_shortest_path_contour == 4.230


def test_parse_z1_log_text_when_scan_row_is_malformed_reports_line() -> None:
    with pytest.raises(ValueError, match="line 2"):
        _ = parse_z1_log_text("header\nZ1+ 1 broken\n")


def test_parse_z1_log_text_when_non_scan_z1_line_is_short_ignores_it() -> None:
    log = parse_z1_log_text("Z1+\nZ1+ (legend) nodes\n")

    assert log.scan_records == ()


def test_reducer_scan_diagnostics_when_postprocess_scan_exists() -> None:
    log = read_z1_log_file(LOG_FIXTURE)

    diagnostics = reducer_scan_diagnostics(log)

    assert diagnostics is not None
    assert diagnostics.core_node_count == 17
    assert diagnostics.final_node_count == 11
    assert diagnostics.core_mean_shortest_path_contour == 4.231
    assert diagnostics.final_mean_shortest_path_contour == 4.230
