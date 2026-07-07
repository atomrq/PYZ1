from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Final

NUMBER_PATTERN: Final = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[Ee][-+]?\d+)?")
RESULT_SECTION_SUFFIX: Final = "results for true chains"
POSTPROCESSING_MARKER: Final = "postprocessing"
GENERATED_FILES_MARKER: Final = "generated files"
FIELD_PREFIXES: Final = {
    "chains": "chains",
    "mean_shortest_path_contour": "< Lpp >",
    "mean_entanglements": "< Z >",
    "ree": "Ree",
    "app": "app",
    "bpp": "bpp",
    "mean_original_beads": "< N >",
    "ne_classical_kink": "Ne_CK:",
    "ne_modified_kink": "Ne_MK:",
    "ne_classical_coil": "Ne_CC:",
    "ne_modified_coil": "Ne_MC:",
}


@dataclass(frozen=True, slots=True)
class ReferenceLogParseSpec:
    mode_prefix: str
    required_field_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RawReferenceLogValues:
    chains: str
    mean_shortest_path_contour: str
    mean_entanglements: str
    ree: str
    app: str
    bpp: str
    mean_original_beads: str
    ne_classical_kink: str | None
    ne_modified_kink: str | None
    ne_classical_coil: str
    ne_modified_coil: str
    generated_files: tuple[str, ...]


def parse_reference_log_text(
    text: str,
    spec: ReferenceLogParseSpec,
) -> RawReferenceLogValues | None:
    lines = tuple(text.splitlines())
    result_section = _result_section_lines(lines, spec.mode_prefix)
    if result_section is None:
        return None

    values = {
        field_name: _extract_field_value(result_section, prefix)
        for field_name, prefix in FIELD_PREFIXES.items()
    }
    if any(values[field_name] is None for field_name in spec.required_field_names):
        return None

    generated_files = _extract_generated_files(lines)
    chains = values["chains"]
    mean_shortest_path_contour = values["mean_shortest_path_contour"]
    mean_entanglements = values["mean_entanglements"]
    ree = values["ree"]
    app = values["app"]
    bpp = values["bpp"]
    mean_original_beads = values["mean_original_beads"]
    ne_classical_coil = values["ne_classical_coil"]
    ne_modified_coil = values["ne_modified_coil"]
    if (
        chains is None
        or mean_shortest_path_contour is None
        or mean_entanglements is None
        or ree is None
        or app is None
        or bpp is None
        or mean_original_beads is None
        or ne_classical_coil is None
        or ne_modified_coil is None
    ):
        return None

    return RawReferenceLogValues(
        chains=chains,
        mean_shortest_path_contour=mean_shortest_path_contour,
        mean_entanglements=mean_entanglements,
        ree=ree,
        app=app,
        bpp=bpp,
        mean_original_beads=mean_original_beads,
        ne_classical_kink=values["ne_classical_kink"],
        ne_modified_kink=values["ne_modified_kink"],
        ne_classical_coil=ne_classical_coil,
        ne_modified_coil=ne_modified_coil,
        generated_files=generated_files,
    )


def _result_section_lines(
    lines: tuple[str, ...],
    mode_prefix: str,
) -> tuple[str, ...] | None:
    start_index = _find_result_section_start(lines, mode_prefix)
    if start_index is None:
        return None

    section: list[str] = []
    for line in lines[start_index + 1 :]:
        if POSTPROCESSING_MARKER in line:
            break
        section.append(line.strip())
    return tuple(section)


def _find_result_section_start(
    lines: tuple[str, ...],
    mode_prefix: str,
) -> int | None:
    for index, line in enumerate(lines):
        if mode_prefix in line and RESULT_SECTION_SUFFIX in line:
            return index
    return None


def _extract_field_value(lines: tuple[str, ...], prefix: str) -> str | None:
    for line in lines:
        if prefix not in line:
            continue
        tail = line[line.index(prefix) + len(prefix) :]
        match = NUMBER_PATTERN.search(tail)
        if match is not None:
            return match.group()
    return None


def _extract_generated_files(lines: tuple[str, ...]) -> tuple[str, ...]:
    marker_index = _find_generated_files_marker(lines)
    if marker_index is None:
        return ()

    files: list[str] = []
    for line in lines[marker_index + 1 :]:
        stripped = line.strip()
        if not stripped:
            continue
        if ")" not in stripped:
            break
        files.append(stripped.split(")", maxsplit=1)[1].strip())
    return tuple(files)


def _find_generated_files_marker(lines: tuple[str, ...]) -> int | None:
    for index, line in enumerate(lines):
        if GENERATED_FILES_MARKER in line:
            return index
    return None
