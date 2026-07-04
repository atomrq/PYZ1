from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import TYPE_CHECKING, Final

from pyz1.initconfig_io import write_init_config_file
from pyz1.models import Chain, Snapshot
from pyz1.output_io import write_summary_file
from pyz1.output_values import write_float_values_file, write_int_values_file
from pyz1.ppa_config import (
    PpaConstants,
    PpaMode,
    PpaPhase,
    PpaSettings,
    accelerated_ppa_settings,
    standard_ppa_settings,
)
from pyz1.ppa_neighbors import (
    PpaNeighborInput,
    fold_periodic_vector,
    wca_neighbor_pairs,
)
from pyz1.ppa_summary import build_ppa_summary_outputs
from pyz1.ppa_vector import (
    PpaVector,
    add_vectors,
    dot_vectors,
    scale_vector,
    subtract_vectors,
    vector_from_model,
    vector_to_model,
    zero_vector,
)

if TYPE_CHECKING:
    from pathlib import Path

    from pyz1.summary import SummaryOutputs

ChainRange = tuple[int, int]
PPA_EARLY_STOP_MAX_GROWTH_PHASE: Final[int] = 3
PPA_EARLY_STOP_MIN_STEP: Final[int] = 300
PPA_EARLY_STOP_RATIO_LIMITS: Final[tuple[float, float, float, float, float]] = (
    0.0,
    1.01,
    1.001,
    1.0001,
    1.00005,
)
PPA_EARLY_STOP_PHASE4_DELTA: Final[float] = 0.005
PPA_EARLY_STOP_PHASE5_DELTA: Final[float] = 0.001

__all__ = (
    "PpaMode",
    "PpaPhase",
    "PpaResult",
    "PpaSettings",
    "accelerated_ppa_settings",
    "run_ppa",
    "standard_ppa_settings",
    "write_ppa_outputs",
)


@dataclass(frozen=True, slots=True)
class PpaResult:
    primitive_path: Snapshot
    summary: SummaryOutputs


@dataclass(slots=True)
class _PpaState:
    """Mutable vectors are the integrator state advanced in place."""

    positions: list[PpaVector]
    velocities: list[PpaVector]
    chain_ranges: tuple[ChainRange, ...]
    chain_for_node: tuple[int, ...]
    box: PpaVector
    shear: float


@dataclass(frozen=True, slots=True)
class _PpaRunProgress:
    global_step: int
    last_system_lpp: float


def run_ppa(snapshot: Snapshot, settings: PpaSettings | None = None) -> PpaResult:
    resolved_settings = settings or accelerated_ppa_settings()
    state = _state_from_snapshot(snapshot)
    _unfold_positions(state)
    progress = _PpaRunProgress(global_step=0, last_system_lpp=_system_lpp(state))
    for phase_index, phase in enumerate(resolved_settings.phases, start=1):
        progress = _run_phase(
            state,
            phase,
            phase_index,
            resolved_settings,
            progress,
        )
    primitive_path = _snapshot_from_state(state)
    summary = build_ppa_summary_outputs(
        original=snapshot,
        primitive_path=primitive_path,
        timestep=snapshot.label or 1,
    )
    return PpaResult(primitive_path=primitive_path, summary=summary)


def write_ppa_outputs(directory: Path, result: PpaResult, mode: PpaMode) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    match mode:
        case PpaMode.STANDARD:
            path_name = "PPA.dat"
            summary_name = "PPA-summary.dat"
        case PpaMode.ACCELERATED:
            path_name = "PPA+.dat"
            summary_name = "PPA+summary.dat"
    write_init_config_file(directory / path_name, result.primitive_path)
    write_summary_file(directory / summary_name, (result.summary.record,))
    write_float_values_file(directory / "Ree_values.dat", result.summary.ree_values)
    write_float_values_file(directory / "Lpp_values.dat", result.summary.lpp_values)
    write_int_values_file(directory / "N_values.dat", result.summary.n_values)


def _run_phase(
    state: _PpaState,
    phase: PpaPhase,
    phase_index: int,
    settings: PpaSettings,
    progress: _PpaRunProgress,
) -> _PpaRunProgress:
    forces = _forces(state, settings.constants)
    half_step = 0.5 * phase.timestep
    global_step = progress.global_step
    last_system_lpp = progress.last_system_lpp
    current_system_lpp = last_system_lpp
    nav = round(1.0 / phase.timestep)
    for _ in range(phase.step_count):
        global_step += 1
        state.velocities = _add_scaled_series(state.velocities, forces, half_step)
        state.positions = _add_scaled_series(
            state.positions,
            state.velocities,
            phase.timestep,
        )
        forces = _forces(state, settings.constants)
        state.velocities = _add_scaled_series(state.velocities, forces, half_step)
        _control_temperature(state, phase.temperature)
        if not settings.early_stop or global_step % nav != 1:
            continue
        current_system_lpp = _system_lpp(state)
        if _should_stop_phase(
            phase_index=phase_index,
            global_step=global_step,
            current_system_lpp=current_system_lpp,
            last_system_lpp=last_system_lpp,
        ):
            last_system_lpp = current_system_lpp
            break
        last_system_lpp = current_system_lpp
    return _PpaRunProgress(
        global_step=global_step,
        last_system_lpp=current_system_lpp,
    )


def _should_stop_phase(
    *,
    phase_index: int,
    global_step: int,
    current_system_lpp: float,
    last_system_lpp: float,
) -> bool:
    should_stop = (
        current_system_lpp >= last_system_lpp
        and phase_index <= PPA_EARLY_STOP_MAX_GROWTH_PHASE
    )
    if (
        should_stop
        or current_system_lpp <= 0.0
        or global_step <= PPA_EARLY_STOP_MIN_STEP
    ):
        return should_stop
    ratio = last_system_lpp / current_system_lpp
    delta = current_system_lpp - last_system_lpp
    match phase_index:
        case 1 | 2 | 3:
            should_stop = ratio <= PPA_EARLY_STOP_RATIO_LIMITS[phase_index]
        case 4:
            should_stop = ratio <= PPA_EARLY_STOP_RATIO_LIMITS[
                phase_index
            ] or delta <= PPA_EARLY_STOP_PHASE4_DELTA
        case 5:
            should_stop = delta <= PPA_EARLY_STOP_PHASE5_DELTA
        case _:
            should_stop = False
    return should_stop


def _forces(state: _PpaState, constants: PpaConstants) -> list[PpaVector]:
    forces = [zero_vector() for _ in state.positions]
    _add_fene_forces(state, constants, forces)
    _add_wca_forces(state, constants, forces)
    for start, end in state.chain_ranges:
        forces[start] = zero_vector()
        forces[end - 1] = zero_vector()
    return forces


def _add_fene_forces(
    state: _PpaState,
    constants: PpaConstants,
    forces: list[PpaVector],
) -> None:
    spring = constants.fene_unit / _mean_bond_length(state) ** 2
    r0_squared = constants.fene_r0 * constants.fene_r0
    for start, end in state.chain_ranges:
        for first in range(start, end - 1):
            second = first + 1
            segment = subtract_vectors(state.positions[second], state.positions[first])
            r_squared = dot_vectors(segment, segment)
            pair_force = scale_vector(segment, spring / (1.0 - r_squared / r0_squared))
            forces[first] = add_vectors(forces[first], pair_force)
            forces[second] = subtract_vectors(forces[second], pair_force)


def _add_wca_forces(
    state: _PpaState,
    constants: PpaConstants,
    forces: list[PpaVector],
) -> None:
    neighbor_input = PpaNeighborInput(
        positions=state.positions,
        chain_for_node=state.chain_for_node,
        box=state.box,
        shear=state.shear,
        cutoff=constants.wca_cutoff,
    )
    for pair in wca_neighbor_pairs(neighbor_input):
        factor = -24.0 * (2.0 - pair.distance_squared**3) / pair.distance_squared**7
        pair_force = scale_vector(pair.separation, factor)
        forces[pair.first] = add_vectors(forces[pair.first], pair_force)
        forces[pair.second] = subtract_vectors(forces[pair.second], pair_force)


def _control_temperature(state: _PpaState, temperature: float) -> None:
    if temperature <= 0.0:
        state.velocities = [zero_vector() for _ in state.velocities]
        return
    mobile_count = len(state.positions) - 2 * len(state.chain_ranges)
    if mobile_count <= 0:
        return
    velocity_squared = sum(
        dot_vectors(velocity, velocity) for velocity in state.velocities
    )
    if velocity_squared <= 0.0:
        return
    scale = sqrt(3.0 * mobile_count * temperature / velocity_squared)
    state.velocities = [
        scale_vector(velocity, min(1.0, scale)) for velocity in state.velocities
    ]


def _state_from_snapshot(snapshot: Snapshot) -> _PpaState:
    positions: list[PpaVector] = []
    chain_ranges: list[ChainRange] = []
    chain_for_node: list[int] = []
    for chain_index, chain in enumerate(snapshot.chains):
        start = len(positions)
        positions.extend(vector_from_model(node) for node in chain.nodes)
        end = len(positions)
        chain_ranges.append((start, end))
        chain_for_node.extend((chain_index,) * chain.node_count)
    return _PpaState(
        positions=positions,
        velocities=[zero_vector() for _ in positions],
        chain_ranges=tuple(chain_ranges),
        chain_for_node=tuple(chain_for_node),
        box=vector_from_model(snapshot.box),
        shear=snapshot.shear or 0.0,
    )


def _snapshot_from_state(state: _PpaState) -> Snapshot:
    chains: list[Chain] = []
    for start, end in state.chain_ranges:
        chains.append(
            Chain(
                tuple(
                    vector_to_model(position)
                    for position in state.positions[start:end]
                ),
            ),
        )
    return Snapshot(
        chains=tuple(chains),
        box=vector_to_model(state.box),
        label=None,
        shear=None,
    )


def _unfold_positions(state: _PpaState) -> None:
    for start, end in state.chain_ranges:
        state.positions[start] = _fold(state.positions[start], state)
        for node in range(start + 1, end):
            segment = _fold(
                subtract_vectors(state.positions[node], state.positions[node - 1]),
                state,
            )
            state.positions[node] = add_vectors(state.positions[node - 1], segment)


def _fold(vector: PpaVector, state: _PpaState) -> PpaVector:
    return fold_periodic_vector(vector, state.box, state.shear)


def _mean_bond_length(state: _PpaState) -> float:
    total = 0.0
    bond_count = 0
    for start, end in state.chain_ranges:
        for first in range(start, end - 1):
            segment = subtract_vectors(
                state.positions[first + 1],
                state.positions[first],
            )
            total += sqrt(dot_vectors(segment, segment))
            bond_count += 1
    return total / bond_count


def _system_lpp(state: _PpaState) -> float:
    total = 0.0
    for start, end in state.chain_ranges:
        for first in range(start, end - 1):
            segment = subtract_vectors(
                state.positions[first + 1],
                state.positions[first],
            )
            total += sqrt(dot_vectors(segment, segment))
    return total


def _add_scaled_series(
    first: list[PpaVector],
    second: list[PpaVector],
    scale: float,
) -> list[PpaVector]:
    return [
        add_vectors(item, scale_vector(delta, scale))
        for item, delta in zip(first, second, strict=True)
    ]
