# pyz1-cleanroom-reproduction - Work Plan

## TL;DR (For humans)
**What you'll get:** A native Python `pyz1` package that can read Z1+/LAMMPS-style polymer configurations, reproduce Z1+ summaries and primitive-path outputs, and eventually run default geometrical Z1+, PPA, and PPA+ without depending on the Linux ELF at runtime.

**Why this approach:** The visible source is enough to port parsers, summaries, estimators, and PPA/PPA+, but the default geometrical Z1+ core lives in missing private modules. The plan therefore uses the original Linux executable only as an oracle to generate fixtures, while the Python geometry core is implemented clean-room from the papers and validated against those fixtures.

**What it will NOT do:** It will not decompile the ELF, mutate the original Z1+ source package, claim exact equivalence before regression evidence exists, or add GPU acceleration in the first implementation.

**Effort:** XL
**Risk:** High - the missing `module-Z1.f90` means the hardest component must be reconstructed from papers and oracle behavior rather than translated.
**Decisions to sanity-check:** Development uses a local micromamba env named `pyz1` with Python 3.11+, NumPy, pytest, and pip; no GPU, no numba; `Z1+.ex` is oracle-only; current non-git project root will not be `git init`-ed unless requested.

Your next move: approve execution of this plan, or adjust dependency/runtime scope first. Full execution detail follows below.

---

> TL;DR (machine): XL/high-risk clean-room pyz1 reproduction with fixture-first validation, direct PPA/PPA+ port, and clean-room geometrical Z1+ core.

## Scope
### Must have
- A Python package under `src/pyz1/` with importable modules and a `pyz1` CLI.
- Z1/Z1+ input parser/writer, including trajectory snapshots, optional labels, and sheared-box metadata where documented.
- LAMMPS data/dump import sufficient for bonded linear-chain use cases described by Z1+.
- Output parsers/writers for `Z1+summary.dat`, `Z1+SP.dat`, `Z1+initconfig.dat`, `Ree_values.dat`, `Lpp_values.dat`, `N_values.dat`, `Z_values.dat`, `PPA.dat`, and `PPA+.dat`.
- `Ne` estimator implementation matching the Z1+ paper and README columns.
- Oracle fixture corpus generated from public benchmarks using Linux `Z1+.ex`, including command, environment, SHA256, and output manifests.
- Python PPA and PPA+ implementations ported from visible Fortran modules.
- Clean-room geometrical Z1+ reducer implementing fixed endpoints, no crossing/slipping, monotonic contour reduction, kink cleanup, and `SP+` pairing.
- Tests and evidence artifacts for every stage.
### Must NOT have (guardrails, anti-slop, scope boundaries)
- Do not decompile, disassemble for logic, or translate ELF-derived machine code.
- Do not modify files under `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`.
- Do not keep `Z1+.ex` as a production/runtime dependency of `pyz1`; it is allowed only under fixture/oracle tooling.
- Do not claim exact equivalence for default geometrical Z1+ until public benchmark fixture comparisons pass with documented tolerances.
- Do not implement branched/cyclic polymer support, GUI, GPU acceleration, or private developer/debug modes in the first version.
- Do not add `numba`, CUDA, GPU, or accelerator-specific dependencies.
- Do not initialize or rewrite git history in the current project root without explicit user instruction.

## Verification strategy
> Zero human intervention - all verification is agent-executed.
- Test decision: TDD/fixture-first with `pytest`; every implementation slice starts from oracle or formula tests.
- Local environment: all local development and tests run via `micromamba run -n pyz1 ...`.
- Local micromamba guard: on this macOS host, prefix micromamba commands with `ulimit -n 1000000` in the same shell because `ulimit -n unlimited` triggers libmamba/codesign `Invalid argument`.
- Dependencies: initial env is `python=3.11`, `numpy`, `pytest`, and `pip`; do not install `numba` or GPU packages.
- Evidence: `.omo/evidence/task-<N>-pyz1-cleanroom-reproduction.<ext>` plus fixture manifests under `tests/fixtures/z1plus_oracle/manifest.json`.
- Numeric policy:
  - Parser and writer round-trips: exact structural equality except floating text formatting tolerances.
  - Summary and estimator formulas: strict tolerances around `1e-10` for deterministic arrays.
  - PPA/PPA+: toleranced comparisons because trajectory integration may diverge in last digits; acceptance must record chosen tolerances.
  - Geometrical Z1+: compare invariants first, then `Lpp`, `Z`, kink count, and `SP+` pairing against oracle fixtures.
- Remote/oracle policy: before using the cluster, executor must read `/Users/jiaxm/.codex/RESOURCES.md` and `/Users/jiaxm/.codex/resources/cluster-access.md`; do not store secrets in fixtures.

## Execution strategy
### Parallel execution waves
> Target 5-8 todos per wave. Fewer than 3 (except the final) means you under-split.
- Wave 0: package scaffold, fixture/oracle design, and source-contract extraction.
- Wave 1: parsers, output models, summary/estimator layer.
- Wave 2: oracle generation and CLI compatibility shell.
- Wave 3: PPA/PPA+ port from visible Fortran.
- Wave 4: clean-room geometrical Z1+ reducer.
- Wave 5: benchmark convergence, documentation, and final QA.

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 1 | none | 2-16 | none |
| 2 | 1 | 4, 5, 6, 8, 12 | 3 |
| 3 | 1 | 4, 7, 15 | 2 |
| 4 | 2, 3 | 5, 6, 7, 8, 12, 14 | none |
| 5 | 4 | 8, 12, 14 | 6, 7 |
| 6 | 4 | 8, 10, 12 | 5, 7 |
| 7 | 3, 4 | 11, 12, 14 | 5, 6 |
| 8 | 5, 6 | 9, 10, 12 | 11 |
| 9 | 8 | 10, 12 | 11 |
| 10 | 8, 9 | 12, 14 | 11 |
| 11 | 7 | 12, 14 | 8, 9 |
| 12 | 8, 10, 11 | 13, 14 | none |
| 13 | 12 | 14, 15 | none |
| 14 | 12, 13 | 15, 16 | none |
| 15 | 14 | 16 | none |
| 16 | 15 | final verification | none |

## Todos
> Implementation + Test = ONE todo. Never separate.
<!-- APPEND TASK BATCHES BELOW THIS LINE WITH edit/apply_patch - never rewrite the headers above. -->

### 2026-07-03 checkpoint: benchmark-04 parser/statistics parity slice

- Completed local `pyz1` scaffold, core models, Z1 input parser/writer, Z1+ summary/SP parser, SP+ pairing parser, and input-derived statistics for `benchmark-04`.
- Generated real Z1+ oracle outputs on the Linux cluster via the Perl wrapper, not by direct ELF execution.
- Added fixtures under `tests/fixtures/z1plus_oracle/benchmark-04/{basic,spplus}/`.
- Passing evidence: `.omo/evidence/task-16-pyz1-cleanroom-reproduction.txt` records `18 passed`, ruff clean, basedpyright clean, and LOC checks.
- Detailed oracle/parity evidence: `.omo/evidence/pyz1-benchmark-04-oracle-and-parity.md`.
- Not yet completed from the original full plan: full Ne estimator set, all-14 benchmark oracle manifest with every valid run exit 0, PPA/PPA+ port, and clean-room geometrical reducer.

### 2026-07-03 checkpoint: contract and multi-benchmark oracle corpus

- Completed `docs/pyz1-contract.md` and verified the missing-source, PPA, SP+, NeCK, fixed-endpoint, and oracle policy keywords.
- Implemented `pyz1.oracle` generator core plus `pyz1.oracle_cli` CLI and typed manifest models.
- Added timeout handling so long Z1+ runs are classified as `exit_code=124` instead of blocking the corpus forever.
- Generated local slim oracle corpora:
  - `tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703/manifest.json`: 42 runs, 39 exit 0, 3 timed out.
  - `tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703/manifest.json`: 28 runs, 25 exit 0, 3 timed out.
- Added PPA/PPA+ summary parser coverage for Fortran overflow fields rendered as `************`; local reparse now reports 48/48 materialized summary files parseable across both corpora.
- Fixed `python -m pyz1.oracle_cli --help` so oracle generation has a real module entry point.
- Fixed oracle generation with relative `--out` paths by resolving benchmark, output, and Z1+ install paths before entering per-run working directories.
- Completed a remote 300-second rerun for the six original timeout cases:
  - `benchmark-09:{default,spplus,selfz}` still timed out.
  - `benchmark-07:ppa` and `benchmark-10:ppa` completed with summary rows.
  - `benchmark-11:ppa` still timed out.
  - Local manifest copies: `.omo/evidence/oracle-long-300s-20260703/`.
- Detailed corpus evidence: `.omo/evidence/pyz1-oracle-corpus-20260703.md`.
- Todo 7 remains open because the final acceptance criterion requires every valid run to finish exit 0, and four benchmark/mode pairs still exceed 300 seconds.

### 2026-07-03 checkpoint: output writer slice

- Added `src/pyz1/output_write.py` for Z1+ summary and shortest-path text writers.
- Re-exported thin writer wrappers from `src/pyz1/output_io.py` without pushing the parser module above the 250 LOC ceiling.
- Writer coverage includes:
  - `Z1+summary.dat`/`PPA-summary.dat`/`PPA+summary.dat` 15-column row formatting by shared summary record structure.
  - Fortran overflow `nan` serialization back to `************`.
  - `Z1+SP.dat`/`PPA.dat`/`PPA+.dat` shortest-path formatting with optional SP+ `other-chain other-node` columns.
- Evidence:
  - red: `.omo/evidence/task-5-writer-red-pyz1-cleanroom-reproduction.txt`
  - focused quality: `.omo/evidence/task-5-writer-quality-pyz1-cleanroom-reproduction.txt`
  - full gate: `.omo/evidence/final-gate-pyz1-output-writer-20260703.txt`

### 2026-07-03 checkpoint: output value/initconfig completion slice

- Added `src/pyz1/output_values.py` for `Ree_values.dat`, `Lpp_values.dat`, `N_values.dat`, and `Z_values.dat` parser/writer APIs.
- Added `src/pyz1/initconfig_io.py` for `Z1+initconfig.dat`, `PPA.dat`, and `PPA+.dat` coordinate snapshot parser/writer APIs.
- Pulled full `benchmark-04/default` Z1+ oracle files from the remote full oracle run into `tests/fixtures/z1plus_oracle/benchmark-04/basic/` for instance parity coverage.
- Added tests proving:
  - `Z1+initconfig.dat` geometry matches source `.benchmark-04.Z1` within floating tolerance and preserves the Z1+ trailing shear metadata.
  - `Ree_values.dat`, `N_values.dat`, and `Z_values.dat` round-trip against oracle values.
  - `PPA.dat` and `PPA+.dat` parse and re-emit as coordinate snapshot outputs.
- Evidence:
  - red: `.omo/evidence/task-5-values-initconfig-red-pyz1-cleanroom-reproduction.txt`
  - focused quality: `.omo/evidence/task-5-values-initconfig-quality-pyz1-cleanroom-reproduction.txt`
  - full gate: `.omo/evidence/final-gate-pyz1-values-initconfig-20260703.txt`
- Todo 5 output parser/writer scope is complete for the named Z1+ output files.

### 2026-07-04 checkpoint: estimator/statistics slice

- Added `PrimitivePathInput` and `PrimitivePathStatistics` in `src/pyz1/estimators.py`.
- Implemented summary-layer primitive statistics: `<Lpp>`, `<Z>`, `app`, `bpp`, `sqrt(<Lpp^2>)`, `NeCK`, `NeMK`, `NeCC`, and `NeMC`.
- Matched `benchmark-04/default` oracle values from `Z1+summary.dat`, `Ree_values.dat`, `Lpp_values.dat`, `N_values.dat`, and `Z_values.dat`.
- Documented undefined zero-kink and modified-coil behavior as Z1+-style `-1.0` sentinels in `docs/pyz1-contract.md`.
- Evidence:
  - red: `.omo/evidence/task-6-estimators-red-pyz1-cleanroom-reproduction.txt`
  - focused: `.omo/evidence/task-6-estimators-focused-pyz1-cleanroom-reproduction.txt`
  - full gate: `.omo/evidence/final-gate-pyz1-estimators-20260704.txt`

### 2026-07-04 checkpoint: summary generation slice

- Added `src/pyz1/summary.py` for converting original snapshots plus primitive-path outputs into Z1+-compatible summary/value records.
- Implemented `build_summary_outputs()` for `Z1+SP.dat` style shortest paths and `build_summary_outputs_from_coordinate_path()` for coordinate primitive paths such as PPA/PPA+ outputs.
- Implemented `write_summary_outputs()` to emit `Z1+summary.dat`, `Ree_values.dat`, `Lpp_values.dat`, `N_values.dat`, and `Z_values.dat` through the existing writer layer.
- Verified `benchmark-04/default` generated summary/value outputs against the Z1+ oracle fixture.
- Verified PPA-style `Z=-1` sentinel behavior does not produce kink estimators.
- Evidence:
  - red: `.omo/evidence/task-8-summary-red-pyz1-cleanroom-reproduction.txt`
  - writer red: `.omo/evidence/task-8-summary-write-red-pyz1-cleanroom-reproduction.txt`
  - focused/full gate: `.omo/evidence/final-gate-pyz1-summary-20260704.txt`

### 2026-07-04 checkpoint: CLI compatibility slice

- Replaced the scaffold-only CLI with a Z1+-compatible argument parser for the public wrapper options.
- Help now lists `-clean`, `-log`, `-stats`, `-selfZ`, `-SP+`, `-PPA`, `-PPA+`, `-from`, `-to`, `-ignore_H`, and ignored-type options.
- Implemented `-clean`/`-c` cleanup for known Z1+ output files.
- Existing analysis modes validate the input path and fail clearly with `mode is not implemented yet`; they do not call `Z1+.ex`.
- Evidence:
  - red: `.omo/evidence/task-9-cli-red-pyz1-cleanroom-reproduction.txt`
  - focused/full gate: `.omo/evidence/final-gate-pyz1-cli-20260704.txt`

- [x] 1. Scaffold `pyz1` package, test harness, and evidence layout
  What to do / Must NOT do: Create `pyproject.toml`, `src/pyz1/`, `tests/`, `tests/fixtures/`, and `.omo/evidence/`. Configure pytest and a CLI entry point. Use the existing local micromamba `pyz1` env for all commands. Do not implement algorithm logic yet. Do not add numba/GPU dependencies.
  Parallelization: Wave 0 | Blocked by: none | Blocks: all todos
  References: `/Users/jiaxm/Contents/CodexProjects/Z1` current root; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/LICENSE.txt`; `.omo/drafts/pyz1-cleanroom-reproduction.md`
  Acceptance criteria: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest --collect-only)` exits 0; `(ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 --help)` or installed console entry help exits 0.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest --collect-only) | tee .omo/evidence/task-1-pyz1-cleanroom-reproduction.txt`; failure: intentionally run `(ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 missing-file.Z1)` and assert nonzero with clear error captured in the same evidence file.
  Commit: N | no git repo at current root

- [x] 2. Define core data models and invariants
  What to do / Must NOT do: Implement immutable-ish models for boxes, chains, snapshots, trajectories, primitive paths, nodes, kink records, and summary rows. Include invariant validators for fixed endpoints, chain lengths, node indexing, periodic metadata, and true-chain vs dumbbell classification. Do not couple models to file parsing.
  Parallelization: Wave 1 | Blocked by: 1 | Blocks: 4, 5, 6, 8, 12
  References: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt` output/input sections; `docs/references/z1plus-paper-reading-notes.md` sections "2023 Kroger/Dietz/Hoy/Luap CPC" and "本地源码对应关系"
  Acceptance criteria: pytest model tests cover valid linear chains, dumbbells, invalid endpoints, invalid box, and invalid chain-node references.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_models.py -q) | tee .omo/evidence/task-2-pyz1-cleanroom-reproduction.txt`; failure: add an invalid chain fixture inside the test and assert the validator raises the package-specific exception.
  Commit: N | no git repo at current root

- [x] 3. Extract and freeze algorithm/source contracts
  What to do / Must NOT do: Create `docs/pyz1-contract.md` summarizing the exact public surface, equations, constants, missing-source boundary, and fixture tolerance policy. This is a project artifact, not an implementation. Do not copy long copyrighted paper passages.
  Parallelization: Wave 1 | Blocked by: 1 | Blocks: 4, 7, 15
  References: `docs/references/z1plus-paper-reading-notes.md`; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+install.pl`; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-main.f90`; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-PPA.f90`; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-CPPA.f90`
  Acceptance criteria: document includes sections for input formats, output formats, estimator formulas, PPA constants, geometry invariants, and "not source-available".
  QA scenarios: happy: `rg -n "not source-available|PPA|SP\\+|NeCK|fixed endpoints" docs/pyz1-contract.md | tee .omo/evidence/task-3-pyz1-cleanroom-reproduction.txt`; failure: `rg -n "module-Z1.f90 is available" docs/pyz1-contract.md` must return nonzero.
  Commit: N | no git repo at current root

- [x] 4. Implement Z1/Z1+ parser and writer
  What to do / Must NOT do: Parse Z1-formatted snapshots/trajectories and Z1+ optional metadata into core models; write them back in canonical form. Support monodisperse `C*N` chain notation and polydisperse lists. Do not handle LAMMPS here.
  Parallelization: Wave 1 | Blocked by: 2, 3 | Blocks: 5, 6, 7, 8, 12, 14
  References: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`; `docs/references/z1plus-paper-reading-notes.md` "2023 Kroger/Dietz/Hoy/Luap CPC"
  Acceptance criteria: public `.benchmark-01.Z1` and `.benchmark-04.Z1` parse; round-trip preserves chain counts, bead counts, box, coordinates within formatting tolerance.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_z1_io.py -q) | tee .omo/evidence/task-4-pyz1-cleanroom-reproduction.txt`; failure: truncated fixture raises a clear parse error with line number.
  Commit: N | no git repo at current root

- [x] 5. Implement Z1+ output parsers/writers
  What to do / Must NOT do: Parse and write `Z1+summary.dat`, `Z1+SP.dat`, `Z1+initconfig.dat`, `Ree_values.dat`, `Lpp_values.dat`, `N_values.dat`, `Z_values.dat`, `PPA.dat`, and `PPA+.dat`. Do not generate physics results yet.
  Parallelization: Wave 1 | Blocked by: 4 | Blocks: 8, 12, 14
  References: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`; `docs/references/z1plus-paper-reading-notes.md` "本地源码对应关系"
  Acceptance criteria: parser handles oracle files generated later and has synthetic fixtures now; writer round-trips synthetic `SP+` rows with `other-chain/other-node`.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_output_io.py -q) | tee .omo/evidence/task-5-pyz1-cleanroom-reproduction.txt`; failure: malformed `SP+` row with missing paired node must fail validation.
  Commit: N | no git repo at current root

- [x] 6. Implement geometry/statistics primitives and Ne estimators
  What to do / Must NOT do: Implement `Ree`, contour length `Lpp`, rms contour `LPP`, density, true-chain filtering, and `NeCK`, `NeMK`, `NeCC`, `NeMC`. Do not implement path reduction here.
  Parallelization: Wave 1 | Blocked by: 4 | Blocks: 8, 10, 12
  References: `docs/references/z1plus-paper-reading-notes.md` sections "2009 Hoy/Foteinopoulou/Kroger PRE" and "2023 Kroger/Dietz/Hoy/Luap CPC"; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`
  Acceptance criteria: formula tests pass for hand-computed small chains and for at least one Z1+summary oracle row once generated.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_estimators.py -q) | tee .omo/evidence/task-6-pyz1-cleanroom-reproduction.txt`; failure: zero-kink/undefined-PPA cases return documented sentinel/exception behavior, not divide-by-zero.
  Commit: N | no git repo at current root

- [ ] 7. Build Linux oracle runner and fixture manifest
  What to do / Must NOT do: Add tooling that runs the original `Z1+.ex` on Linux/cluster for all 14 public benchmarks with default, `+`, `-selfZ`, `-PPA`, and `-PPA+` where valid. Store outputs under `tests/fixtures/z1plus_oracle/` with SHA256, command, hostname class, date, exit code, and stderr/stdout snippets. Do not store secrets or cluster credentials.
  Parallelization: Wave 2 | Blocked by: 3, 4 | Blocks: 11, 12, 14
  References: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+install.pl`; `/Users/jiaxm/.codex/RESOURCES.md`; `/Users/jiaxm/.codex/resources/cluster-access.md`; `docs/references/z1plus-paper-reading-notes.md` "GPU 集群 black-box 基线"
  Acceptance criteria: manifest exists and every valid run has input hash, output hashes, exit code 0, and parsed summary row count.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1.oracle generate --benchmarks /Users/jiaxm/Contents/CodexProjects/source_code/Z1+ --out tests/fixtures/z1plus_oracle) | tee .omo/evidence/task-7-pyz1-cleanroom-reproduction.txt`; failure: running on macOS without Linux executor returns a clear "oracle requires Linux/cluster" error.
  Commit: N | no git repo at current root

- [x] 8. Implement summary generation compatible with Z1+
  What to do / Must NOT do: Given an original snapshot plus a primitive path result, generate summary/value files in Z1+ column order. Do not implement reduction logic.
  Parallelization: Wave 2 | Blocked by: 5, 6 | Blocks: 9, 10, 12
  References: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`; `docs/references/z1plus-paper-reading-notes.md` "2023 Kroger/Dietz/Hoy/Luap CPC"
  Acceptance criteria: synthetic primitive path fixture emits exact expected summary; at least one oracle fixture parses and re-emits within tolerance.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_summary_writer.py -q) | tee .omo/evidence/task-8-pyz1-cleanroom-reproduction.txt`; failure: PPA path with `Z=-1` does not write kink estimators as if kinks existed.
  Commit: N | no git repo at current root

- [x] 9. Implement CLI compatibility layer
  What to do / Must NOT do: Implement `pyz1 [options] configuration-file` with `-h`, `-clean`, `-stats`, `-log`, `-selfZ`, `+/-SP+`, `-PPA`, `-PPA+`, `-from`, `-to`, `-ignore_H`, and `-ignore_type*`. At this stage, commands may route unavailable algorithm modes to explicit "not implemented yet" errors. Do not silently call `Z1+.ex`.
  Parallelization: Wave 2 | Blocked by: 8 | Blocks: 10, 12
  References: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+template.pl`; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`
  Acceptance criteria: help output lists compatible options; parser-only commands can clean/write files in a temp directory; unavailable modes fail clearly.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_cli.py -q) | tee .omo/evidence/task-9-pyz1-cleanroom-reproduction.txt`; failure: invoking `pyz1 -PPA config.Z1` before PPA implementation must exit nonzero with a mode-specific error.
  Commit: N | no git repo at current root

- [ ] 10. Implement LAMMPS data/dump importer
  What to do / Must NOT do: Port the public wrapper/import behavior needed to convert bonded linear-chain LAMMPS data/dump files into internal snapshots. Include `-from`, `-to`, `-ignore_H`, and `-ignore_type*`. Do not attempt full LAMMPS topology coverage beyond Z1+ public behavior.
  Parallelization: Wave 2 | Blocked by: 8, 9 | Blocks: 12, 14
  References: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+import-lammps.pl`; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+template.pl`
  Acceptance criteria: importer tests cover a minimal data file, minimal dump trajectory, ignored atom types, and frame slicing.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_lammps_import.py -q) | tee .omo/evidence/task-10-pyz1-cleanroom-reproduction.txt`; failure: data file without bond connectivity fails with actionable error.
  Commit: N | no git repo at current root

- [ ] 11. Port standard PPA and accelerated PPA+
  What to do / Must NOT do: Implement PPA and PPA+ from visible `module-CPPA.f90` and `module-PPA.f90`: FENE/WCA constants, phases, neighbor lists, periodic offsets, velocity update, temperature control, convergence/phase logic, and output generation. Do not use the missing Z1 geometry module.
  Parallelization: Wave 3 | Blocked by: 7 | Blocks: 12, 14
  References: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-PPA.f90`; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-CPPA.f90`; `docs/references/z1plus-paper-reading-notes.md` "PPA/PPA+ 警告"
  Acceptance criteria: PPA and PPA+ produce `PPA.dat`/`PPA+.dat` and summaries for selected benchmarks with documented numeric tolerances against oracle.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_ppa.py -q) | tee .omo/evidence/task-11-pyz1-cleanroom-reproduction.txt`; failure: benchmark with bond length above FENE limit fails with the same class of diagnostic as Z1+.
  Commit: N | no git repo at current root

- [ ] 12. Implement clean-room geometry kernel primitives
  What to do / Must NOT do: Implement segment math, periodic unfolding, minimum image handling, segment-segment distance/crossing predicates, local candidate move evaluation, endpoint locks, and monotonic contour checks. Do not yet optimize or emit final `SP+`.
  Parallelization: Wave 4 | Blocked by: 8, 10, 11 | Blocks: 13, 14
  References: `docs/references/z1plus-paper-reading-notes.md` sections "2005 Kroger CPC", "2009 Karayiannis & Kroger IJMS", and "2023 Kroger/Dietz/Hoy/Luap CPC"
  Acceptance criteria: property tests show moves never move endpoints, never increase contour length, and reject crossing/slipping cases for constructed 2D/3D examples.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_geometry_kernel.py -q) | tee .omo/evidence/task-12-pyz1-cleanroom-reproduction.txt`; failure: constructed crossing move is rejected and logged with the violated invariant.
  Commit: N | no git repo at current root

- [ ] 13. Implement clean-room geometrical Z1+ reducer
  What to do / Must NOT do: Build the iterative reducer around geometry primitives: temporary nodes, neighbor candidate selection, local shrinking moves, convergence detection, physical node cleanup, kink detection, `selfZ` behavior, and basic `Z1+SP.dat` output. Do not implement private debug/developer modes.
  Parallelization: Wave 4 | Blocked by: 12 | Blocks: 14, 15
  References: `docs/references/z1plus-paper-reading-notes.md`; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-main.f90`; oracle fixtures from todo 7
  Acceptance criteria: reducer matches invariants on all 14 benchmarks; for small benchmarks it matches oracle `Lpp` and `Z` within documented initial tolerances.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_z1_reducer.py -q) | tee .omo/evidence/task-13-pyz1-cleanroom-reproduction.txt`; failure: intentionally disable endpoint lock in a test double and assert invariant check fails.
  Commit: N | no git repo at current root

- [ ] 14. Implement `SP+` binary entanglement pairing and benchmark regression loop
  What to do / Must NOT do: Add `other-chain/other-node` pairing for kink nodes, compare `Z1+SP.dat` structure against oracle, and create a benchmark report that lists pass/fail/tolerance per benchmark and mode. Do not hide mismatches by loosening tolerances without recording the reason.
  Parallelization: Wave 4 | Blocked by: 12, 13 | Blocks: 15, 16
  References: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`; `docs/references/z1plus-paper-reading-notes.md` "2009 Karayiannis & Kroger IJMS" and "GPU 集群 black-box 基线"
  Acceptance criteria: report file exists under `.omo/evidence/pyz1-benchmark-regression.md`; every benchmark/mode is classified as pass, known-invalid, or mismatch with measured deltas.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest tests/test_spplus_regression.py -q) | tee .omo/evidence/task-14-pyz1-cleanroom-reproduction.txt`; failure: altered oracle pairing fixture triggers a structural mismatch.
  Commit: N | no git repo at current root

- [ ] 15. Write user/developer documentation and migration guide
  What to do / Must NOT do: Document installation, CLI usage, supported formats, known limitations, oracle fixture generation, tolerance policy, and how pyz1 differs from Z1+. Do not overstate equivalence.
  Parallelization: Wave 5 | Blocked by: 14 | Blocks: 16
  References: `docs/pyz1-contract.md`; `.omo/evidence/pyz1-benchmark-regression.md`; `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`
  Acceptance criteria: docs include quickstart, examples, limitations, and benchmark status table.
  QA scenarios: happy: `rg -n "Quickstart|Limitations|Benchmark|oracle|Z1\\+.ex" README.md docs/pyz1-contract.md | tee .omo/evidence/task-15-pyz1-cleanroom-reproduction.txt`; failure: `rg -n "exact replacement|guaranteed identical" README.md docs/pyz1-contract.md` must return nonzero.
  Commit: N | no git repo at current root

- [ ] 16. Package-level final integration smoke
  What to do / Must NOT do: Run package install/check, full pytest, CLI smoke on benchmark inputs, and produce a final evidence index. Do not declare completion if any benchmark mismatch is unexplained.
  Parallelization: Wave 5 | Blocked by: 15 | Blocks: final verification
  References: all prior evidence artifacts; `pyproject.toml`; test suite
  Acceptance criteria: full test command exits 0 in micromamba env; CLI writes expected files in a temp workdir; evidence index links every task artifact.
  QA scenarios: happy: `(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest -q) | tee .omo/evidence/task-16-pyz1-cleanroom-reproduction.txt` and `(ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 /Users/jiaxm/Contents/CodexProjects/source_code/Z1+/.benchmark-04.Z1 --out .omo/evidence/smoke-pyz1)`; failure: CLI on malformed input returns nonzero and writes no partial summary unless explicitly requested.
  Commit: N | no git repo at current root

## Final verification wave
> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.
- [ ] F1. Plan compliance audit: verify every todo acceptance criterion has an evidence artifact and every Must NOT guardrail still holds.
- [ ] F2. Code quality review: inspect package boundaries, numerical code clarity, no hidden `Z1+.ex` runtime dependency, no binary-derived logic.
- [ ] F3. Real manual QA: create a temp directory, run `pyz1` on `.benchmark-04.Z1` default and available PPA/PPA+ modes, inspect emitted files, and record paths.
- [ ] F4. Scope fidelity: compare final README/contract against user request and this plan; explicitly list unsupported items.

## Commit strategy
- Current project root is not a git repository. Do not run `git init` or create commits unless the user explicitly asks.
- If the user later binds this as a git repo/worktree, use atomic commits by wave:
  - `chore(pyz1): scaffold package and fixtures`
  - `feat(pyz1-io): parse z1 and z1plus outputs`
  - `feat(pyz1-estimators): implement z1 summary metrics`
  - `feat(pyz1-oracle): add z1plus fixture generator`
  - `feat(pyz1-ppa): port ppa and ppa-plus`
  - `feat(pyz1-geometry): add clean-room z1 reducer`
  - `docs(pyz1): document limits and benchmark status`

## Success criteria
- `pyz1` is importable and has a CLI.
- Local environment `pyz1` exists and all local verification commands run through `micromamba run -n pyz1`.
- On this macOS host, local micromamba verification commands use `ulimit -n 1000000` to avoid the known libmamba/codesign failure.
- Public benchmark inputs can be parsed without modifying original Z1+ files.
- Summary/estimator outputs match oracle where primitive-path data is available.
- PPA/PPA+ outputs match oracle within recorded tolerances for selected benchmarks.
- Geometrical Z1+ clean-room reducer passes invariant tests and benchmark regression status is transparently reported.
- No production code path shells out to `Z1+.ex`.
- No `numba`, CUDA, GPU, or accelerator dependency is introduced.
- Documentation states the missing-source boundary and benchmark status plainly.
- All `.omo/evidence/` artifacts required by todos exist.
