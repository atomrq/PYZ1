from __future__ import annotations

from math import isnan
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from pathlib import Path

    from pyz1.output_models import (
        ShortestPathNode,
        ShortestPathSnapshot,
        Z1SummaryRecord,
    )

FORTRAN_OVERFLOW_TOKEN: Final = "************"  # noqa: S105 - Fortran overflow.


def write_summary_file(path: Path, records: tuple[Z1SummaryRecord, ...]) -> None:
    _ = path.write_text(format_summary_text(records), encoding="utf-8")


def format_summary_text(records: tuple[Z1SummaryRecord, ...]) -> str:
    if len(records) == 0:
        return ""
    return "\n".join(_format_summary_record(record) for record in records) + "\n"


def write_shortest_path_file(path: Path, snapshot: ShortestPathSnapshot) -> None:
    _ = path.write_text(format_shortest_path_text(snapshot), encoding="utf-8")


def format_shortest_path_text(snapshot: ShortestPathSnapshot) -> str:
    lines: list[str] = [
        str(snapshot.chain_count),
        _format_vector(snapshot.box.as_tuple()),
    ]
    for chain in snapshot.chains:
        lines.append(str(chain.node_count))
        lines.extend(_format_shortest_path_node(node) for node in chain.nodes)
    return "\n".join(lines) + "\n"


def _format_summary_record(record: Z1SummaryRecord) -> str:
    fields = (
        str(record.timestep),
        str(record.true_chain_count),
        _format_summary_float(record.mean_original_beads),
        _format_summary_float(record.mean_squared_end_to_end),
        _format_summary_float(record.mean_shortest_path_contour),
        _format_summary_float(record.mean_entanglements),
        _format_summary_float(record.coil_tube_diameter),
        _format_summary_float(record.coil_tube_step_length),
        _format_summary_float(record.root_mean_squared_contour),
        _format_summary_float(record.ne_classical_kink),
        _format_summary_float(record.ne_modified_kink),
        _format_summary_float(record.ne_classical_coil),
        _format_summary_float(record.ne_modified_coil),
        _format_summary_float(record.mean_original_bond_length),
        _format_summary_float(record.original_bead_density),
    )
    return " ".join(fields)


def _format_shortest_path_node(node: ShortestPathNode) -> str:
    fields = [
        f"{node.position.x:.6f}",
        f"{node.position.y:.6f}",
        f"{node.position.z:.6f}",
        f"{node.source_bead:.6f}",
        str(int(node.is_entanglement)),
    ]
    if node.pair is not None:
        fields.append(str(node.pair.chain_index))
        fields.append(str(node.pair.node_index))
    return " ".join(fields)


def _format_vector(values: tuple[float, float, float]) -> str:
    return " ".join(f"{value:.6f}" for value in values)


def _format_summary_float(value: float) -> str:
    if isnan(value):
        return FORTRAN_OVERFLOW_TOKEN
    return f"{value:.3f}"
