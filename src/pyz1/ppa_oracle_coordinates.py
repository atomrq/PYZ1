from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pyz1.errors import Z1OutputParseError
from pyz1.initconfig_io import read_init_config_file
from pyz1.ppa_regression import PpaOracleCoordinateStatus, PpaRegressionMode

if TYPE_CHECKING:
    from pathlib import Path

__all__ = (
    "PpaOracleCoordinateRecord",
    "PpaOracleCoordinateReportRequest",
    "PpaOracleCoordinateStatus",
    "write_ppa_oracle_coordinate_report",
)


@dataclass(frozen=True, slots=True)
class PpaOracleCoordinateReportRequest:
    oracle_root: Path
    report_path: Path
    modes: tuple[PpaRegressionMode, ...]
    benchmark_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PpaOracleCoordinateRecord:
    benchmark_id: str
    mode: PpaRegressionMode
    coordinate_filename: str
    status: PpaOracleCoordinateStatus
    node_count: int | None
    error_line: int | None
    error_reason: str | None
    note: str


def write_ppa_oracle_coordinate_report(
    request: PpaOracleCoordinateReportRequest,
) -> tuple[PpaOracleCoordinateRecord, ...]:
    records = tuple(
        _coordinate_record(request.oracle_root, benchmark_id, mode)
        for benchmark_id in request.benchmark_ids
        for mode in request.modes
    )
    request.report_path.parent.mkdir(parents=True, exist_ok=True)
    _ = request.report_path.write_text(_format_report(records), encoding="utf-8")
    return records


def _coordinate_record(
    oracle_root: Path,
    benchmark_id: str,
    mode: PpaRegressionMode,
) -> PpaOracleCoordinateRecord:
    coordinate_filename = _coordinate_filename(mode)
    coordinate_path = (
        oracle_root
        / f"benchmark-{benchmark_id}"
        / mode.value
        / coordinate_filename
    )
    if not coordinate_path.exists():
        return PpaOracleCoordinateRecord(
            benchmark_id=benchmark_id,
            mode=mode,
            coordinate_filename=coordinate_filename,
            status=PpaOracleCoordinateStatus.MISSING,
            node_count=None,
            error_line=None,
            error_reason=None,
            note="missing oracle PPA coordinate path",
        )
    try:
        snapshot = read_init_config_file(coordinate_path)
    except Z1OutputParseError as exc:
        return PpaOracleCoordinateRecord(
            benchmark_id=benchmark_id,
            mode=mode,
            coordinate_filename=coordinate_filename,
            status=PpaOracleCoordinateStatus.INVALID,
            node_count=None,
            error_line=exc.line_number,
            error_reason=exc.reason,
            note="oracle PPA coordinate path is not parseable",
        )
    return PpaOracleCoordinateRecord(
        benchmark_id=benchmark_id,
        mode=mode,
        coordinate_filename=coordinate_filename,
        status=PpaOracleCoordinateStatus.PARSEABLE,
        node_count=snapshot.node_count,
        error_line=None,
        error_reason=None,
        note="oracle PPA coordinate path is parseable",
    )


def _coordinate_filename(mode: PpaRegressionMode) -> str:
    match mode:
        case PpaRegressionMode.STANDARD:
            return "PPA.dat"
        case PpaRegressionMode.ACCELERATED:
            return "PPA+.dat"


def _format_report(records: tuple[PpaOracleCoordinateRecord, ...]) -> str:
    lines = [
        "# Z1+ PPA oracle coordinate fixture report",
        "",
        (
            "| benchmark | mode | coordinate file | status | nodes | "
            "error line | error reason | note |"
        ),
        "| --- | --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    lines.extend(_format_record(record) for record in records)
    return "\n".join(lines) + "\n"


def _format_record(record: PpaOracleCoordinateRecord) -> str:
    return (
        f"| benchmark-{record.benchmark_id} | {record.mode.value} | "
        f"{record.coordinate_filename} | {record.status.value} | "
        f"{_format_optional_int(record.node_count)} | "
        f"{_format_optional_int(record.error_line)} | "
        f"{_format_optional_text(record.error_reason)} | {record.note} |"
    )


def _format_optional_int(value: int | None) -> str:
    if value is None:
        return "n/a"
    return str(value)


def _format_optional_text(value: str | None) -> str:
    if value is None:
        return "n/a"
    return value
