from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Final

from pyz1.reference_log_parser import (
    ReferenceLogParseSpec,
    parse_reference_log_text,
)

if TYPE_CHECKING:
    from pathlib import Path


REPORT_HEADER_PREFIX: Final = "| benchmark | mode | status | chains | Lpp | Z |"
REPORT_HEADER_NE: Final = "Ne_CK | Ne_MK |"
REPORT_HEADER_RIGHT: Final = "Ne_CC | Ne_MC | generated files | note |"
REPORT_HEADER: Final = (
    f"{REPORT_HEADER_PREFIX} {REPORT_HEADER_NE} {REPORT_HEADER_RIGHT}"
)


class ReferenceLogMode(StrEnum):
    Z1PLUS = "z1plus"
    PPAPLUS = "ppaplus"


class ReferenceLogStatus(StrEnum):
    PARSEABLE = "parseable"
    MISSING = "missing"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class ReferenceLogReportRequest:
    reference_root: Path
    report_path: Path
    modes: tuple[ReferenceLogMode, ...]
    benchmark_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReferenceLogRecord:
    benchmark_id: str
    mode: ReferenceLogMode
    status: ReferenceLogStatus
    chains: int | None
    mean_shortest_path_contour: float | None
    mean_entanglements: float | None
    ree: float | None
    app: float | None
    bpp: float | None
    mean_original_beads: float | None
    ne_classical_kink: float | None
    ne_modified_kink: float | None
    ne_classical_coil: float | None
    ne_modified_coil: float | None
    generated_files: tuple[str, ...]
    note: str


def write_reference_log_report(
    request: ReferenceLogReportRequest,
) -> tuple[ReferenceLogRecord, ...]:
    records = tuple(
        read_reference_log_record(request.reference_root, benchmark_id, mode)
        for mode in request.modes
        for benchmark_id in request.benchmark_ids
    )
    request.report_path.parent.mkdir(parents=True, exist_ok=True)
    _ = request.report_path.write_text(_format_report(records), encoding="utf-8")
    return records


def read_reference_log_record(
    reference_root: Path,
    benchmark_id: str,
    mode: ReferenceLogMode,
) -> ReferenceLogRecord:
    path = _reference_log_path(reference_root, benchmark_id, mode)
    if not path.exists():
        return _status_record(
            benchmark_id=benchmark_id,
            mode=mode,
            status=ReferenceLogStatus.MISSING,
            note=f"missing reference log: {path}",
        )

    text = path.read_text(encoding="utf-8")
    raw_values = parse_reference_log_text(text, _parse_spec(mode))
    if raw_values is None:
        return _status_record(
            benchmark_id=benchmark_id,
            mode=mode,
            status=ReferenceLogStatus.INVALID,
            note="result block or required fields not parseable",
        )

    try:
        return ReferenceLogRecord(
            benchmark_id=benchmark_id,
            mode=mode,
            status=ReferenceLogStatus.PARSEABLE,
            chains=int(raw_values.chains),
            mean_shortest_path_contour=float(raw_values.mean_shortest_path_contour),
            mean_entanglements=float(raw_values.mean_entanglements),
            ree=float(raw_values.ree),
            app=float(raw_values.app),
            bpp=float(raw_values.bpp),
            mean_original_beads=float(raw_values.mean_original_beads),
            ne_classical_kink=_optional_float(raw_values.ne_classical_kink),
            ne_modified_kink=_optional_float(raw_values.ne_modified_kink),
            ne_classical_coil=float(raw_values.ne_classical_coil),
            ne_modified_coil=float(raw_values.ne_modified_coil),
            generated_files=raw_values.generated_files,
            note="reference log parseable",
        )
    except ValueError:
        return _status_record(
            benchmark_id=benchmark_id,
            mode=mode,
            status=ReferenceLogStatus.INVALID,
            note="numeric field not parseable",
        )


def discover_reference_log_benchmark_ids(reference_root: Path) -> tuple[str, ...]:
    ids = {
        path.name.removeprefix("log-benchmark-").removesuffix(".txt")
        for mode in ReferenceLogMode
        for path in _reference_log_dir(reference_root, mode).glob("log-benchmark-*.txt")
    }
    return tuple(sorted(ids))


def _reference_log_path(
    reference_root: Path,
    benchmark_id: str,
    mode: ReferenceLogMode,
) -> Path:
    filename = f"log-benchmark-{benchmark_id}.txt"
    return _reference_log_dir(reference_root, mode) / filename


def _reference_log_dir(reference_root: Path, mode: ReferenceLogMode) -> Path:
    match mode:
        case ReferenceLogMode.Z1PLUS:
            return reference_root / "Z1+reference-results"
        case ReferenceLogMode.PPAPLUS:
            return reference_root / "PPA+reference-results"


def _parse_spec(mode: ReferenceLogMode) -> ReferenceLogParseSpec:
    return ReferenceLogParseSpec(
        mode_prefix=_source_log_prefix(mode),
        required_field_names=_required_field_names(mode),
    )


def _source_log_prefix(mode: ReferenceLogMode) -> str:
    match mode:
        case ReferenceLogMode.Z1PLUS:
            return "Z1+"
        case ReferenceLogMode.PPAPLUS:
            return "PPA+"


def _required_field_names(mode: ReferenceLogMode) -> tuple[str, ...]:
    common = (
        "chains",
        "mean_shortest_path_contour",
        "mean_entanglements",
        "ree",
        "app",
        "bpp",
        "mean_original_beads",
        "ne_classical_coil",
        "ne_modified_coil",
    )
    match mode:
        case ReferenceLogMode.Z1PLUS:
            return (*common, "ne_classical_kink", "ne_modified_kink")
        case ReferenceLogMode.PPAPLUS:
            return common


def _optional_float(value: str | None) -> float | None:
    if value is None:
        return None
    return float(value)


def _status_record(
    benchmark_id: str,
    mode: ReferenceLogMode,
    status: ReferenceLogStatus,
    note: str,
) -> ReferenceLogRecord:
    return ReferenceLogRecord(
        benchmark_id=benchmark_id,
        mode=mode,
        status=status,
        chains=None,
        mean_shortest_path_contour=None,
        mean_entanglements=None,
        ree=None,
        app=None,
        bpp=None,
        mean_original_beads=None,
        ne_classical_kink=None,
        ne_modified_kink=None,
        ne_classical_coil=None,
        ne_modified_coil=None,
        generated_files=(),
        note=note,
    )


def _format_report(records: tuple[ReferenceLogRecord, ...]) -> str:
    lines = [
        "# pyz1 reference log smoke",
        "",
        REPORT_HEADER,
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(_format_record_row(record) for record in records)
    lines.append("")
    return "\n".join(lines)


def _format_record_row(record: ReferenceLogRecord) -> str:
    return (
        f"| benchmark-{record.benchmark_id} | {record.mode.value} | "
        f"{record.status.value} | {_format_int(record.chains)} | "
        f"{_format_float(record.mean_shortest_path_contour)} | "
        f"{_format_float(record.mean_entanglements)} | "
        f"{_format_float(record.ne_classical_kink)} | "
        f"{_format_float(record.ne_modified_kink)} | "
        f"{_format_float(record.ne_classical_coil)} | "
        f"{_format_float(record.ne_modified_coil)} | "
        f"{', '.join(record.generated_files)} | {record.note} |"
    )


def _format_int(value: int | None) -> str:
    if value is None:
        return ""
    return str(value)


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.5f}".rstrip("0").rstrip(".")
