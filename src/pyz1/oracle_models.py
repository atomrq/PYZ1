from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from pathlib import Path

JsonScalar: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]


@dataclass(frozen=True, slots=True)
class OracleMode:
    name: str
    arguments: tuple[str, ...]
    summary_filename: str
    path_filename: str


@dataclass(frozen=True, slots=True)
class OracleGenerationRequest:
    benchmarks_dir: Path
    out_dir: Path
    z1_install_dir: Path
    mode_names: tuple[str, ...]
    allow_non_linux: bool
    platform_name: str
    timeout_seconds: float | None


@dataclass(frozen=True, slots=True)
class OracleRunRecord:
    benchmark: str
    mode: str
    arguments: tuple[str, ...]
    exit_code: int
    summary_rows: int
    input_sha256: str
    binary_sha256: str
    output_sha256: dict[str, str]
    outputs: dict[str, str]
    stdout_path: str
    stderr_path: str
    work_dir: str

    def to_json(self) -> JsonObject:
        output_sha256: JsonObject = dict(self.output_sha256)
        outputs: JsonObject = dict(self.outputs)
        return {
            "benchmark": self.benchmark,
            "mode": self.mode,
            "arguments": list(self.arguments),
            "exit_code": self.exit_code,
            "summary_rows": self.summary_rows,
            "input_sha256": self.input_sha256,
            "binary_sha256": self.binary_sha256,
            "output_sha256": output_sha256,
            "outputs": outputs,
            "stdout_path": self.stdout_path,
            "stderr_path": self.stderr_path,
            "work_dir": self.work_dir,
        }


@dataclass(frozen=True, slots=True)
class OracleManifest:
    schema_version: int
    generator: str
    platform_name: str
    runs: tuple[OracleRunRecord, ...]

    def to_json(self) -> JsonObject:
        return {
            "schema_version": self.schema_version,
            "generator": self.generator,
            "platform_name": self.platform_name,
            "runs": [run.to_json() for run in self.runs],
        }
