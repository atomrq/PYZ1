from dataclasses import dataclass
from pathlib import Path

from typing_extensions import override


class PyZ1Error(Exception):
    pass


@dataclass(frozen=True, slots=True)
class InputFileMissingError(PyZ1Error):
    path: Path

    @override
    def __str__(self) -> str:
        return f"input file does not exist: {self.path}"


@dataclass(frozen=True, slots=True)
class InvalidChainError(ValueError):
    node_count: int

    @override
    def __str__(self) -> str:
        return f"chain must contain at least two nodes, got {self.node_count}"


@dataclass(frozen=True, slots=True)
class InvalidSnapshotError(ValueError):
    reason: str

    @override
    def __str__(self) -> str:
        return self.reason


@dataclass(frozen=True, slots=True)
class Z1ParseError(ValueError):
    line_number: int
    reason: str

    @override
    def __str__(self) -> str:
        return f"line {self.line_number}: {self.reason}"


@dataclass(frozen=True, slots=True)
class Z1OutputParseError(ValueError):
    line_number: int
    reason: str

    @override
    def __str__(self) -> str:
        return f"line {self.line_number}: {self.reason}"
