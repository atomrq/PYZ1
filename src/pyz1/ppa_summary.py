from __future__ import annotations

from itertools import pairwise
from math import sqrt

from pyz1.errors import InvalidSnapshotError
from pyz1.models import Chain, Snapshot, Vector3
from pyz1.output_models import Z1SummaryRecord
from pyz1.summary import SummaryOutputs


def build_ppa_summary_outputs(
    *,
    original: Snapshot,
    primitive_path: Snapshot,
    timestep: int,
) -> SummaryOutputs:
    if original.chain_count != primitive_path.chain_count:
        raise InvalidSnapshotError(reason="PPA path chain count must match input")
    true_primitive_chains = primitive_path.true_chains
    if len(true_primitive_chains) == 0:
        raise InvalidSnapshotError(reason="PPA path has no true chains")
    chain_count = original.chain_count
    lpp_values = tuple(_chain_contour(chain) for chain in true_primitive_chains)
    ree_values = tuple(_chain_end_to_end(chain) for chain in true_primitive_chains)
    ave_ree2 = sum(value * value for value in ree_values) / chain_count
    ave_lpp = sum(lpp_values) / chain_count
    ave_lpp2 = sum(value * value for value in lpp_values) / chain_count
    ave_n = original.node_count / chain_count
    record = Z1SummaryRecord(
        timestep=timestep,
        true_chain_count=chain_count,
        mean_original_beads=ave_n,
        mean_squared_end_to_end=sqrt(ave_ree2),
        mean_shortest_path_contour=ave_lpp,
        mean_entanglements=-1.0,
        coil_tube_diameter=ave_ree2 / ave_lpp,
        coil_tube_step_length=(
            ave_lpp * chain_count / (original.node_count - chain_count)
        ),
        root_mean_squared_contour=sqrt(ave_lpp2),
        ne_classical_kink=-1.0,
        ne_modified_kink=-1.0,
        ne_classical_coil=(ave_n - 1.0) * ave_ree2 / ave_lpp**2,
        ne_modified_coil=_modified_coil_estimator(
            mean_original_beads=ave_n,
            mean_end_to_end_squared=ave_ree2,
            mean_contour_squared=ave_lpp2,
        ),
        mean_original_bond_length=_initial_mean_bond_length(original),
        original_bead_density=original.node_count / _box_volume(original.box),
    )
    return SummaryOutputs(
        record=record,
        ree_values=ree_values,
        lpp_values=lpp_values,
        n_values=tuple(chain.node_count for chain in original.chains),
        z_values=(-1,) * len(true_primitive_chains),
    )


def _modified_coil_estimator(
    *,
    mean_original_beads: float,
    mean_end_to_end_squared: float,
    mean_contour_squared: float,
) -> float:
    if mean_end_to_end_squared <= 0.0:
        return -1.0
    denominator = mean_contour_squared / mean_end_to_end_squared - 1.0
    if denominator <= 0.0:
        return -1.0
    return (mean_original_beads - 1.0) / denominator


def _initial_mean_bond_length(snapshot: Snapshot) -> float:
    total = sum(
        _unfolded_chain_contour(chain, snapshot) for chain in snapshot.chains
    )
    return total / (snapshot.node_count - snapshot.chain_count)


def _unfolded_chain_contour(chain: Chain, snapshot: Snapshot) -> float:
    unfolded = [_fold(chain.nodes[0], snapshot.box, snapshot.shear or 0.0)]
    for node in chain.nodes[1:]:
        segment = _fold(
            _subtract(node, unfolded[-1]),
            snapshot.box,
            snapshot.shear or 0.0,
        )
        unfolded.append(_add(unfolded[-1], segment))
    return sum(_distance(first, second) for first, second in pairwise(tuple(unfolded)))


def _chain_contour(chain: Chain) -> float:
    return sum(_distance(first, second) for first, second in pairwise(chain.nodes))


def _chain_end_to_end(chain: Chain) -> float:
    return _distance(chain.nodes[0], chain.nodes[-1])


def _fold(vector: Vector3, box: Vector3, shear: float) -> Vector3:
    y_correction = round(vector.y / box.y)
    x = vector.x - shear * y_correction
    return Vector3(
        x=x - round(x / box.x) * box.x,
        y=vector.y - y_correction * box.y,
        z=vector.z - round(vector.z / box.z) * box.z,
    )


def _add(first: Vector3, second: Vector3) -> Vector3:
    return Vector3(first.x + second.x, first.y + second.y, first.z + second.z)


def _subtract(first: Vector3, second: Vector3) -> Vector3:
    return Vector3(first.x - second.x, first.y - second.y, first.z - second.z)


def _distance(first: Vector3, second: Vector3) -> float:
    dx = first.x - second.x
    dy = first.y - second.y
    dz = first.z - second.z
    return sqrt(dx * dx + dy * dy + dz * dz)


def _box_volume(box: Vector3) -> float:
    return box.x * box.y * box.z
