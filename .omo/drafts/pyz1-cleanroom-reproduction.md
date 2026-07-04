---
slug: pyz1-cleanroom-reproduction
status: plan-generated
intent: clear
pending-action: await user approval to execute .omo/plans/pyz1-cleanroom-reproduction.md
approach: Build pyz1 as a native Python clean-room reproduction of Z1+ with Z1+.ex used only as an oracle/fixture generator, not as the final runtime dependency.
---

# Draft: pyz1-cleanroom-reproduction

## Components (topology ledger)
<!-- Lock the SHAPE before depth. One row per top-level component that can succeed or fail independently. -->
<!-- id | outcome (one line) | status: active|deferred | evidence path -->
1. C1 | Package/test scaffold for pyz1 with reproducible fixtures and evidence paths | active | .omo/plans/pyz1-cleanroom-reproduction.md
2. C2 | Z1/Z1+/LAMMPS parsing and output parsing | active | /Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt
3. C3 | Summary statistics and Ne estimators | active | /Users/jiaxm/Contents/CodexProjects/Z1/docs/references/z1plus-paper-reading-notes.md
4. C4 | Oracle runner/fixture generation using Linux Z1+.ex | active | /Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+install.pl
5. C5 | PPA/PPA+ Python port from visible Fortran | active | /Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-PPA.f90 and module-CPPA.f90
6. C6 | Clean-room geometrical Z1+ reducer and SP+ pairing | active | papers + black-box fixtures, because module-Z1.f90 is absent
7. C7 | CLI, documentation, packaging, and final validation | active | plan success criteria

## Open assumptions (announced defaults)
<!-- Record any default you adopt instead of asking, so the user can veto it at the gate. -->
<!-- assumption | adopted default | rationale | reversible? -->
1. Runtime dependency policy | Local micromamba env named `pyz1`; use Python 3.11+, numpy, pytest, pip; no GPU, no numba, no scipy in the first implementation | User explicitly requested local micromamba development and no GPU/numba | reversible
2. Runtime independence | pyz1 final command must not require Z1+.ex; Z1+.ex is oracle-only under tests/fixtures/tools | User asked to reproduce pyz1, not wrap ELF | reversible only by scope change
3. Geometry target | Implement clean-room Z1+ behavior from papers and fixtures, not binary decompilation | module-Z1.f90 is not present; binary reverse engineering would be fragile and legally/ethically worse | not a normal implementation choice
4. Repository state | Do not git-init current /Users/jiaxm/Contents/CodexProjects/Z1 unless user explicitly asks | Current directory is not a git repo; plan artifacts still persist under .omo | reversible
5. Test strategy | TDD/fixture-first inside the `pyz1` micromamba env: create oracle fixtures and failing tests before each implementation slice | Scientific code needs regression fixtures before algorithm tuning | reversible

## Findings (cited - path:lines)
1. Current package is public distribution plus prebuilt Linux ELF, not full private source: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+install.pl` defines PUBLIC_DISTRIBUTION without `module-Z1.f90`/`module-functions.f90`, while PRIVATE_DISTRIBUTION includes them.
2. `module-main.f90` imports `use Z1`, `use PPA`, and `use CPPA`; default execution calls `apply_Z1plus`, PPA calls `apply_PPA`, standard PPA calls `apply_CPPA`.
3. Visible source supports direct PPA/PPA+ port: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-PPA.f90` and `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-CPPA.f90` expose phases, FENE/WCA constants, neighbor-list logic, integration loop, and summary output.
4. Z1+ README defines accepted input classes and outputs: `Z1+summary.dat`, `Z1+SP.dat`, `Z1+initconfig.dat`, `Ree_values.dat`, `Lpp_values.dat`, `N_values.dat`, `Z_values.dat`, `PPA.dat`, `PPA+.dat`.
5. Paper notes establish the algorithm contract: fixed chain ends, no bond crossing/slipping, monotonic path-length reduction, local geometric operations, physical node/kink cleanup, and S/M estimator boundaries.
6. Prior cluster smoke evidence shows the Linux ELF can run and produce oracle output; plan must regenerate fixtures rather than rely on chat-only output.
7. CodeGraph exists but did not return relevant Fortran/document results for this workspace; plan uses focused source reads as fallback.

## Decisions (with rationale)
1. Build a Python package under `src/pyz1/` plus `tests/`, not scripts-only. Rationale: clean-room algorithm needs stable module boundaries and tests.
2. Put all generated oracle artifacts under `tests/fixtures/z1plus_oracle/` or `.omo/evidence/`, with SHA256 manifest. Rationale: exact binary behavior must be reproducible.
3. Implement output-compatible CLI `pyz1` with options matching the useful public surface: default, `+`/`-SP+`, `-selfZ`, `-PPA`, `-PPA+`, `-from`, `-to`, `-ignore_H`, `-ignore_type*`. Rationale: supports direct user migration.
4. Keep PPA/PPA+ as a visible-source port and geometry Z1+ as clean-room. Rationale: source evidence differs across components.
5. Use toleranced numeric comparison for PPA/PPA+ and stricter structural comparison for parser/summary/default geometry where deterministic fixtures allow it.
6. Develop locally on macOS arm64 in the `pyz1` micromamba environment. Linux `Z1+.ex` remains remote/oracle-only because it cannot execute on macOS.
7. On this macOS shell, run micromamba commands inside a shell with `ulimit -n 1000000`; the default `unlimited` fd limit triggers libmamba/codesign `Invalid argument`.

## Scope IN
1. Python package scaffold with tests and CLI.
2. Z1/Z1+ input parser and writer.
3. LAMMPS data/dump import path sufficient to match public wrapper behavior for bonded linear chains.
4. Z1+ output parsers and summary writer.
5. Ne estimator implementation.
6. Oracle fixture generation on Linux cluster or Linux host.
7. PPA/PPA+ port from visible Fortran.
8. Clean-room geometrical Z1+ reducer with kink cleanup and SP+ pairing.
9. Benchmark regression across the 14 public `.benchmark-XX.Z1` files.

## Scope OUT (Must NOT have)
1. No binary decompilation or reverse-engineered ELF-derived source.
2. No claim of exact Z1+ equivalence until benchmark fixtures pass with documented tolerances.
3. No GPU acceleration in initial pyz1.
4. No support for branched/cyclic polymers beyond the public Z1+ linear-chain surface.
5. No hidden dependency on Linux `Z1+.ex` at runtime.
6. No mutation/deletion of original `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+` files.
7. No GPU, no numba, and no CUDA-specific dependency.

## Open questions
None blocking for plan generation. Defaults above can be vetoed before execution.

## Approval gate
status: plan-generated
<!-- When exploration is exhausted and unknowns are answered, set status: awaiting-approval. -->
<!-- That durable record is the loop guard: on a later turn read it and resume at the gate instead of re-running exploration. -->
pending user decision: approve execution of .omo/plans/pyz1-cleanroom-reproduction.md, or request changes to dependency/runtime scope.
