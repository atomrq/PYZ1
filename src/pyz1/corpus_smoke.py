from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isclose
from typing import TYPE_CHECKING, Final

from pyz1.benchmark_inputs import (
    BenchmarkInputFormat,
    BenchmarkInputStatus,
    read_benchmark_input_record,
)
from pyz1.reference_logs import (
    ReferenceLogMode,
    ReferenceLogStatus,
    read_reference_log_record,
)

if TYPE_CHECKING:
    from pathlib import Path

    from pyz1.benchmark_inputs import BenchmarkInputRecord


FLOAT_TOLERANCE: Final = 1.0e-9
REPORT_HEADER: Final = (
    "| benchmark | status | input chains | input nodes | input <N> | "
    "Z1+ chains delta | PPA+ chains delta | Z1+ <N> delta | "
    "PPA+ <N> delta | Z1+ <Lpp> | Z1+ <Z> | Z1+ Ne_MC | "
    "PPA+ <Lpp> | PPA+ <Z> | PPA+ Ne_CC | PPA+ Ne_MC | note |"
)


class CorpusSmokeStatus(StrEnum):
    PASSED = "passed"
    MISMATCH = "mismatch"
    INCOMPLETE = "incomplete"


@dataclass(frozen=True, slots=True)
class CorpusSmokeReportRequest:
    benchmark_root: Path
    report_path: Path
    benchmark_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CorpusSmokeRecord:
    benchmark_id: str
    status: CorpusSmokeStatus
    input_chain_count: int | None
    input_node_count: int | None
    input_mean_original_beads: float | None
    z1plus_chain_count_delta: int | None
    ppaplus_chain_count_delta: int | None
    z1plus_mean_original_beads_delta: float | None
    ppaplus_mean_original_beads_delta: float | None
    z1plus_mean_shortest_path_contour: float | None
    z1plus_mean_entanglements: float | None
    z1plus_ne_modified_coil: float | None
    ppaplus_mean_shortest_path_contour: float | None
    ppaplus_mean_entanglements: float | None
    ppaplus_ne_classical_coil: float | None
    ppaplus_ne_modified_coil: float | None
    note: str


@dataclass(frozen=True, slots=True)
class _CorpusDeltas:
    z1plus_chain_count: int
    ppaplus_chain_count: int
    z1plus_mean_original_beads: float
    ppaplus_mean_original_beads: float


def write_corpus_smoke_report(
    request: CorpusSmokeReportRequest,
) -> tuple[CorpusSmokeRecord, ...]:
    records = tuple(
        read_corpus_smoke_record(request.benchmark_root, benchmark_id)
        for benchmark_id in request.benchmark_ids
    )
    request.report_path.parent.mkdir(parents=True, exist_ok=True)
    _ = request.report_path.write_text(_format_report(records), encoding="utf-8")
    return records


def read_corpus_smoke_record(
    benchmark_root: Path,
    benchmark_id: str,
) -> CorpusSmokeRecord:
    z1_input = read_benchmark_input_record(
        benchmark_root,
        benchmark_id,
        BenchmarkInputFormat.Z1,
    )
    dump_input = read_benchmark_input_record(
        benchmark_root,
        benchmark_id,
        BenchmarkInputFormat.DUMP,
    )
    z1plus_log = read_reference_log_record(
        benchmark_root,
        benchmark_id,
        ReferenceLogMode.Z1PLUS,
    )
    ppaplus_log = read_reference_log_record(
        benchmark_root,
        benchmark_id,
        ReferenceLogMode.PPAPLUS,
    )
    if (
        z1_input.status != BenchmarkInputStatus.PARSEABLE
        or dump_input.status != BenchmarkInputStatus.PARSEABLE
        or z1plus_log.status != ReferenceLogStatus.PARSEABLE
        or ppaplus_log.status != ReferenceLogStatus.PARSEABLE
    ):
        return _incomplete_record(benchmark_id)

    if (
        z1_input.chain_count is None
        or z1_input.node_count is None
        or z1_input.true_chain_count is None
        or dump_input.chain_count is None
        or dump_input.node_count is None
        or dump_input.true_chain_count is None
        or z1plus_log.chains is None
        or z1plus_log.mean_original_beads is None
        or z1plus_log.mean_entanglements is None
        or z1plus_log.ne_modified_coil is None
        or ppaplus_log.chains is None
        or ppaplus_log.mean_original_beads is None
        or ppaplus_log.ne_modified_coil is None
    ):
        return _incomplete_record(benchmark_id)

    input_mean_original_beads = z1_input.node_count / z1_input.true_chain_count
    deltas = _CorpusDeltas(
        z1plus_chain_count=z1plus_log.chains - z1_input.true_chain_count,
        ppaplus_chain_count=ppaplus_log.chains - z1_input.true_chain_count,
        z1plus_mean_original_beads=(
            z1plus_log.mean_original_beads - input_mean_original_beads
        ),
        ppaplus_mean_original_beads=(
            ppaplus_log.mean_original_beads - input_mean_original_beads
        ),
    )
    status = _alignment_status(
        z1_input=z1_input,
        dump_input=dump_input,
        deltas=deltas,
    )
    return CorpusSmokeRecord(
        benchmark_id=benchmark_id,
        status=status,
        input_chain_count=z1_input.chain_count,
        input_node_count=z1_input.node_count,
        input_mean_original_beads=input_mean_original_beads,
        z1plus_chain_count_delta=deltas.z1plus_chain_count,
        ppaplus_chain_count_delta=deltas.ppaplus_chain_count,
        z1plus_mean_original_beads_delta=deltas.z1plus_mean_original_beads,
        ppaplus_mean_original_beads_delta=deltas.ppaplus_mean_original_beads,
        z1plus_mean_shortest_path_contour=(
            z1plus_log.mean_shortest_path_contour
        ),
        z1plus_mean_entanglements=z1plus_log.mean_entanglements,
        z1plus_ne_modified_coil=z1plus_log.ne_modified_coil,
        ppaplus_mean_shortest_path_contour=(
            ppaplus_log.mean_shortest_path_contour
        ),
        ppaplus_mean_entanglements=ppaplus_log.mean_entanglements,
        ppaplus_ne_classical_coil=ppaplus_log.ne_classical_coil,
        ppaplus_ne_modified_coil=ppaplus_log.ne_modified_coil,
        note=_status_note(status),
    )


def _alignment_status(
    *,
    z1_input: BenchmarkInputRecord,
    dump_input: BenchmarkInputRecord,
    deltas: _CorpusDeltas,
) -> CorpusSmokeStatus:
    if (
        z1_input.chain_count == dump_input.chain_count
        and z1_input.node_count == dump_input.node_count
        and z1_input.true_chain_count == dump_input.true_chain_count
        and deltas.z1plus_chain_count == 0
        and deltas.ppaplus_chain_count == 0
        and isclose(
            deltas.z1plus_mean_original_beads,
            0.0,
            abs_tol=FLOAT_TOLERANCE,
        )
        and isclose(
            deltas.ppaplus_mean_original_beads,
            0.0,
            abs_tol=FLOAT_TOLERANCE,
        )
    ):
        return CorpusSmokeStatus.PASSED
    return CorpusSmokeStatus.MISMATCH


def _status_note(status: CorpusSmokeStatus) -> str:
    match status:
        case CorpusSmokeStatus.PASSED:
            return "input/reference statistics aligned"
        case CorpusSmokeStatus.MISMATCH:
            return "input/reference statistics mismatch"
        case CorpusSmokeStatus.INCOMPLETE:
            return "missing or invalid input/reference record"


def _incomplete_record(benchmark_id: str) -> CorpusSmokeRecord:
    return CorpusSmokeRecord(
        benchmark_id=benchmark_id,
        status=CorpusSmokeStatus.INCOMPLETE,
        input_chain_count=None,
        input_node_count=None,
        input_mean_original_beads=None,
        z1plus_chain_count_delta=None,
        ppaplus_chain_count_delta=None,
        z1plus_mean_original_beads_delta=None,
        ppaplus_mean_original_beads_delta=None,
        z1plus_mean_shortest_path_contour=None,
        z1plus_mean_entanglements=None,
        z1plus_ne_modified_coil=None,
        ppaplus_mean_shortest_path_contour=None,
        ppaplus_mean_entanglements=None,
        ppaplus_ne_classical_coil=None,
        ppaplus_ne_modified_coil=None,
        note=_status_note(CorpusSmokeStatus.INCOMPLETE),
    )


def _format_report(records: tuple[CorpusSmokeRecord, ...]) -> str:
    lines = [
        "# pyz1 corpus statistical smoke",
        "",
        REPORT_HEADER,
        _format_report_separator(),
    ]
    lines.extend(_format_record_row(record) for record in records)
    lines.append("")
    return "\n".join(lines)


def _format_report_separator() -> str:
    column_count = len(REPORT_HEADER.strip().strip("|").split("|"))
    return "| " + " | ".join("---" for _ in range(column_count)) + " |"


def _format_record_row(record: CorpusSmokeRecord) -> str:
    return (
        f"| benchmark-{record.benchmark_id} | {record.status.value} | "
        f"{_format_int(record.input_chain_count)} | "
        f"{_format_int(record.input_node_count)} | "
        f"{_format_float(record.input_mean_original_beads)} | "
        f"{_format_int(record.z1plus_chain_count_delta)} | "
        f"{_format_int(record.ppaplus_chain_count_delta)} | "
        f"{_format_float(record.z1plus_mean_original_beads_delta)} | "
        f"{_format_float(record.ppaplus_mean_original_beads_delta)} | "
        f"{_format_float(record.z1plus_mean_shortest_path_contour)} | "
        f"{_format_float(record.z1plus_mean_entanglements)} | "
        f"{_format_float(record.z1plus_ne_modified_coil)} | "
        f"{_format_float(record.ppaplus_mean_shortest_path_contour)} | "
        f"{_format_float(record.ppaplus_mean_entanglements)} | "
        f"{_format_float(record.ppaplus_ne_classical_coil)} | "
        f"{_format_float(record.ppaplus_ne_modified_coil)} | "
        f"{record.note} |"
    )


def _format_int(value: int | None) -> str:
    if value is None:
        return ""
    return str(value)


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.5f}".rstrip("0").rstrip(".")
