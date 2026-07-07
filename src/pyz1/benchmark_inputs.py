from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Final

from pyz1.lammps_io import import_lammps_files
from pyz1.z1_io import read_z1_file

if TYPE_CHECKING:
    from pathlib import Path

    from pyz1.models import Snapshot


REPORT_HEADER: Final = (
    "| benchmark | input | status | chains | nodes | true chains | box | shear | note |"
)


class BenchmarkInputFormat(StrEnum):
    Z1 = "z1"
    DUMP = "dump"


class BenchmarkInputStatus(StrEnum):
    PARSEABLE = "parseable"
    MISSING = "missing"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class BenchmarkInputReportRequest:
    benchmark_root: Path
    report_path: Path
    input_formats: tuple[BenchmarkInputFormat, ...]
    benchmark_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BenchmarkInputRecord:
    benchmark_id: str
    input_format: BenchmarkInputFormat
    status: BenchmarkInputStatus
    chain_count: int | None
    node_count: int | None
    true_chain_count: int | None
    box_lengths: tuple[float, float, float] | None
    shear: float | None
    note: str


def write_benchmark_input_report(
    request: BenchmarkInputReportRequest,
) -> tuple[BenchmarkInputRecord, ...]:
    records = tuple(
        read_benchmark_input_record(request.benchmark_root, benchmark_id, input_format)
        for input_format in request.input_formats
        for benchmark_id in request.benchmark_ids
    )
    request.report_path.parent.mkdir(parents=True, exist_ok=True)
    _ = request.report_path.write_text(_format_report(records), encoding="utf-8")
    return records


def read_benchmark_input_record(
    benchmark_root: Path,
    benchmark_id: str,
    input_format: BenchmarkInputFormat,
) -> BenchmarkInputRecord:
    path = _benchmark_input_path(benchmark_root, benchmark_id, input_format)
    if not path.exists():
        return _status_record(
            benchmark_id=benchmark_id,
            input_format=input_format,
            status=BenchmarkInputStatus.MISSING,
            note=f"missing benchmark input: {path}",
        )

    snapshot = _read_snapshot(path, input_format)
    return _record_from_snapshot(
        benchmark_id=benchmark_id,
        input_format=input_format,
        snapshot=snapshot,
    )


def discover_benchmark_input_ids(benchmark_root: Path) -> tuple[str, ...]:
    ids = {
        path.name.removeprefix("benchmark-").removesuffix(_input_suffix(input_format))
        for input_format in BenchmarkInputFormat
        for path in benchmark_root.glob(f"benchmark-*{_input_suffix(input_format)}")
    }
    return tuple(sorted(ids))


def _benchmark_input_path(
    benchmark_root: Path,
    benchmark_id: str,
    input_format: BenchmarkInputFormat,
) -> Path:
    return benchmark_root / f"benchmark-{benchmark_id}{_input_suffix(input_format)}"


def _input_suffix(input_format: BenchmarkInputFormat) -> str:
    match input_format:
        case BenchmarkInputFormat.Z1:
            return ".Z1"
        case BenchmarkInputFormat.DUMP:
            return ".dump"


def _read_snapshot(path: Path, input_format: BenchmarkInputFormat) -> Snapshot:
    match input_format:
        case BenchmarkInputFormat.Z1:
            return read_z1_file(path)
        case BenchmarkInputFormat.DUMP:
            return import_lammps_files(dump_path=path)[0]


def _record_from_snapshot(
    *,
    benchmark_id: str,
    input_format: BenchmarkInputFormat,
    snapshot: Snapshot,
) -> BenchmarkInputRecord:
    return BenchmarkInputRecord(
        benchmark_id=benchmark_id,
        input_format=input_format,
        status=BenchmarkInputStatus.PARSEABLE,
        chain_count=snapshot.chain_count,
        node_count=snapshot.node_count,
        true_chain_count=snapshot.true_chain_count,
        box_lengths=snapshot.box.as_tuple(),
        shear=snapshot.shear,
        note="benchmark input parseable",
    )


def _status_record(
    *,
    benchmark_id: str,
    input_format: BenchmarkInputFormat,
    status: BenchmarkInputStatus,
    note: str,
) -> BenchmarkInputRecord:
    return BenchmarkInputRecord(
        benchmark_id=benchmark_id,
        input_format=input_format,
        status=status,
        chain_count=None,
        node_count=None,
        true_chain_count=None,
        box_lengths=None,
        shear=None,
        note=note,
    )


def _format_report(records: tuple[BenchmarkInputRecord, ...]) -> str:
    lines = [
        "# pyz1 benchmark input smoke",
        "",
        REPORT_HEADER,
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(_format_record_row(record) for record in records)
    lines.append("")
    return "\n".join(lines)


def _format_record_row(record: BenchmarkInputRecord) -> str:
    return (
        f"| benchmark-{record.benchmark_id} | {record.input_format.value} | "
        f"{record.status.value} | {_format_int(record.chain_count)} | "
        f"{_format_int(record.node_count)} | {_format_int(record.true_chain_count)} | "
        f"{_format_box(record.box_lengths)} | {_format_float(record.shear)} | "
        f"{record.note} |"
    )


def _format_int(value: int | None) -> str:
    if value is None:
        return ""
    return str(value)


def _format_box(value: tuple[float, float, float] | None) -> str:
    if value is None:
        return ""
    return ", ".join(_format_float(item) for item in value)


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.5f}".rstrip("0").rstrip(".")
