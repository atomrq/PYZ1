from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from typing_extensions import override

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class OraclePlatformError(RuntimeError):
    platform_name: str

    @override
    def __str__(self) -> str:
        return (
            "oracle requires Linux or an explicit executor, "
            f"got {self.platform_name}"
        )


@dataclass(frozen=True, slots=True)
class OracleInputError(RuntimeError):
    path: Path
    reason: str

    @override
    def __str__(self) -> str:
        return f"{self.path}: {self.reason}"
