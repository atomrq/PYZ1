from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pyz1.errors import Z1OutputParseError

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class Z1ScanRecord:
    scan: int
    mean_shortest_path_contour: float
    progress: int
    cutoff_radius: float
    visits: int
    crossings: int
    new_nodes: int
    too_long: int
    ghost_nodes: int
    erased_nodes: int
    mean_bond_length: float
    node_count: int
    max_node_id: int
    handled_crosspoints: int
    memory_percent: float
    cpu_seconds: float


@dataclass(frozen=True, slots=True)
class Z1Log:
    scan_records: tuple[Z1ScanRecord, ...]


def read_z1_log_file(path: Path) -> Z1Log:
    return parse_z1_log_text(path.read_text(encoding="utf-8"))


def parse_z1_log_text(text: str) -> Z1Log:
    return Z1Log(
        scan_records=tuple(
            _parse_scan_record(line_number, line)
            for line_number, line in enumerate(text.splitlines(), start=1)
            if _is_scan_record_line(line)
        ),
    )


def _is_scan_record_line(line: str) -> bool:
    tokens = line.split()
    return len(tokens) > 1 and tokens[0] == "Z1+" and tokens[1].isdigit()


def _parse_scan_record(line_number: int, line: str) -> Z1ScanRecord:
    tokens = line.split()
    try:
        return Z1ScanRecord(
            scan=int(tokens[1]),
            mean_shortest_path_contour=float(tokens[2]),
            progress=int(tokens[3]),
            cutoff_radius=float(tokens[4]),
            visits=int(tokens[5]),
            crossings=int(tokens[6]),
            new_nodes=int(tokens[7]),
            too_long=int(tokens[8]),
            ghost_nodes=int(tokens[9]),
            erased_nodes=int(tokens[10]),
            mean_bond_length=float(tokens[11]),
            node_count=int(tokens[12]),
            max_node_id=int(tokens[13]),
            handled_crosspoints=int(tokens[14]),
            memory_percent=float(tokens[15]),
            cpu_seconds=float(tokens[16]),
        )
    except (IndexError, ValueError) as exc:
        raise Z1OutputParseError(
            line_number=line_number,
            reason="invalid Z1+ scan row",
        ) from exc
