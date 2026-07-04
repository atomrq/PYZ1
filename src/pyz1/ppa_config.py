from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, unique
from typing import Final

FENE_UNIT: Final[float] = 100.0
FENE_R0: Final[float] = 1.5
WCA_CUTOFF: Final[float] = 1.122462048309373


@unique
class PpaMode(StrEnum):
    STANDARD = "ppa"
    ACCELERATED = "ppaplus"


@dataclass(frozen=True, slots=True)
class PpaPhase:
    timestep: float
    temperature: float
    step_count: int
    skin: float


@dataclass(frozen=True, slots=True)
class PpaConstants:
    fene_unit: float = FENE_UNIT
    fene_r0: float = FENE_R0
    wca_cutoff: float = WCA_CUTOFF


@dataclass(frozen=True, slots=True)
class PpaSettings:
    mode: PpaMode
    phases: tuple[PpaPhase, ...]
    constants: PpaConstants = field(default_factory=PpaConstants)


def standard_ppa_settings() -> PpaSettings:
    return PpaSettings(
        mode=PpaMode.STANDARD,
        phases=(
            PpaPhase(timestep=0.008, temperature=0.001, step_count=125000, skin=1.0),
        ),
    )


def accelerated_ppa_settings() -> PpaSettings:
    return PpaSettings(
        mode=PpaMode.ACCELERATED,
        phases=(
            PpaPhase(timestep=0.008, temperature=0.1, step_count=1250, skin=0.7),
            PpaPhase(timestep=0.008, temperature=0.05, step_count=1250, skin=0.7),
            PpaPhase(timestep=0.01, temperature=0.005, step_count=1000, skin=0.6),
            PpaPhase(timestep=0.01, temperature=0.001, step_count=1000, skin=0.3),
            PpaPhase(timestep=0.01, temperature=0.0001, step_count=1000, skin=0.2),
        ),
    )
