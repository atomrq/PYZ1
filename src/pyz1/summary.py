from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import TYPE_CHECKING

from pyz1.errors import InvalidSnapshotError
from pyz1.estimators import (
    PrimitivePathInput,
    compute_input_statistics,
    compute_primitive_path_statistics,
)
from pyz1.output_io import write_summary_file
from pyz1.output_models import Z1SummaryRecord
from pyz1.output_values import write_float_values_file, write_int_values_file

if TYPE_CHECKING:
    from pathlib import Path

    from pyz1.models import Chain, Snapshot, Vector3
    from pyz1.output_models import ShortestPathChain, ShortestPathSnapshot


@dataclass(frozen=True, slots=True)
class SummaryOutputs:
    record: Z1SummaryRecord
    ree_values: tuple[float, ...]
    lpp_values: tuple[float, ...]
    n_values: tuple[int, ...]
    z_values: tuple[int, ...]


def build_summary_outputs(
    *,
    original: Snapshot,
    primitive_path: ShortestPathSnapshot,
    timestep: int,
) -> SummaryOutputs:
    z_values = tuple(
        sum(node.is_entanglement for node in chain.nodes)
        for chain in primitive_path.chains
    )
    lpp_values = tuple(_shortest_path_contour(chain) for chain in primitive_path.chains)
    return _build_summary_outputs(
        original=original,
        primitive_chain_count=primitive_path.chain_count,
        timestep=timestep,
        lpp_values=lpp_values,
        z_values=z_values,
    )


def build_summary_outputs_from_coordinate_path(
    *,
    original: Snapshot,
    primitive_path: Snapshot,
    entanglement_counts: tuple[int, ...],
    timestep: int,
) -> SummaryOutputs:
    lpp_values = tuple(_chain_contour(chain) for chain in primitive_path.chains)
    return _build_summary_outputs(
        original=original,
        primitive_chain_count=primitive_path.chain_count,
        timestep=timestep,
        lpp_values=lpp_values,
        z_values=entanglement_counts,
    )


def write_summary_outputs(
    directory: Path,
    outputs: SummaryOutputs,
    *,
    summary_filename: str = "Z1+summary.dat",
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    write_summary_file(directory / summary_filename, (outputs.record,))
    write_float_values_file(directory / "Ree_values.dat", outputs.ree_values)
    write_float_values_file(directory / "Lpp_values.dat", outputs.lpp_values)
    write_int_values_file(directory / "N_values.dat", outputs.n_values)
    write_int_values_file(directory / "Z_values.dat", outputs.z_values)


def _build_summary_outputs(
    *,
    original: Snapshot,
    primitive_chain_count: int,
    timestep: int,
    lpp_values: tuple[float, ...],
    z_values: tuple[int, ...],
) -> SummaryOutputs:
    true_chains = original.true_chains
    if len(true_chains) != primitive_chain_count:
        raise InvalidSnapshotError(
            reason="primitive path chain count must match true chain count",
        )
    if len(z_values) != len(true_chains):
        raise InvalidSnapshotError(
            reason="entanglement count series must match true chain count",
        )
    input_stats = compute_input_statistics(original)
    n_values = tuple(chain.node_count for chain in true_chains)
    ree_values = tuple(_chain_end_to_end(chain) for chain in true_chains)
    primitive_stats = compute_primitive_path_statistics(
        PrimitivePathInput(
            original_chain_lengths=n_values,
            end_to_end_distances=ree_values,
            shortest_path_contours=lpp_values,
            entanglement_counts=z_values,
        ),
    )
    record = Z1SummaryRecord(
        timestep=timestep,
        true_chain_count=input_stats.true_chain_count,
        mean_original_beads=input_stats.mean_original_beads,
        mean_squared_end_to_end=input_stats.root_mean_squared_end_to_end,
        mean_shortest_path_contour=primitive_stats.mean_shortest_path_contour,
        mean_entanglements=primitive_stats.mean_entanglements,
        coil_tube_diameter=primitive_stats.coil_tube_diameter,
        coil_tube_step_length=primitive_stats.coil_tube_step_length,
        root_mean_squared_contour=primitive_stats.root_mean_squared_contour,
        ne_classical_kink=primitive_stats.ne_classical_kink,
        ne_modified_kink=primitive_stats.ne_modified_kink,
        ne_classical_coil=primitive_stats.ne_classical_coil,
        ne_modified_coil=primitive_stats.ne_modified_coil,
        mean_original_bond_length=input_stats.mean_original_bond_length,
        original_bead_density=input_stats.original_bead_density,
    )
    return SummaryOutputs(
        record=record,
        ree_values=ree_values,
        lpp_values=lpp_values,
        n_values=n_values,
        z_values=z_values,
    )


def _shortest_path_contour(chain: ShortestPathChain) -> float:
    return sum(
        _distance(first.position, second.position)
        for first, second in zip(chain.nodes[:-1], chain.nodes[1:], strict=True)
    )


def _chain_contour(chain: Chain) -> float:
    return sum(
        _distance(first, second)
        for first, second in zip(chain.nodes[:-1], chain.nodes[1:], strict=True)
    )


def _chain_end_to_end(chain: Chain) -> float:
    return _distance(chain.nodes[0], chain.nodes[-1])


def _distance(first: Vector3, second: Vector3) -> float:
    dx = first.x - second.x
    dy = first.y - second.y
    dz = first.z - second.z
    return sqrt(dx * dx + dy * dy + dz * dz)
