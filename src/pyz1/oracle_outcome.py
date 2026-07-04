from __future__ import annotations

from typing import Final

CRASH_EXIT_CODE: Final = 139
CRASH_SIGNATURES: Final = (
    "CRASHED. contact mk",
    "SIGSEGV",
    "segmentation fault",
    "forrtl: severe",
)


def normalize_oracle_exit_code(
    *,
    exit_code: int,
    stdout: str,
    stderr: str,
) -> int:
    if exit_code != 0:
        return exit_code
    combined_output = f"{stdout}\n{stderr}"
    if any(signature in combined_output for signature in CRASH_SIGNATURES):
        return CRASH_EXIT_CODE
    return exit_code
