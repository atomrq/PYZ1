# Source-Informed Development Plan

Last updated: 2026-07-06.

This plan guides future `pyz1` clean-room development. It updates the active
direction after reading the public `mkmat/Z1plus-code` repository. It does not
replace the clean-room goal: `pyz1` must not depend on the Linux `Z1+.ex`
binary at package runtime, and the hidden Z1 reducer core remains unavailable.

## Source Trace

Use these local source mirrors before changing parser, writer, reducer, oracle,
or benchmark behavior:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
  - Mendeley/install-package source and oracle binary mirror.
  - Public files include the wrapper, output helpers, PPA/CPPA modules, shared
    parameters, folding logic, benchmarks, and `Z1+.ex`.
  - Public files do not include the private reducer core
    `module-Z1.f90` / `module-functions.f90`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  - GitHub mirror of `https://github.com/mkmat/Z1plus-code`.
  - Current pinned checkout for planning evidence:
    `c7219cd394b1295272ebfc098f2835c5c871e6ec`.
  - Contains official supplemental Perl scripts, benchmark 07/10/11 `.Z1` and
    `.dump` inputs, and Z1+/PPA+ reference logs.

When a future slice uses one of these files, record the exact path and, for the
Git checkout, the commit hash in that slice's evidence artifact or docs update.

## Development Policy

Every future reducer, parser, writer, oracle, PPA/PPA+, or benchmark slice must
classify its rationale before implementation:

- `source_contract`: behavior directly supported by visible Z1+/Z1plus-code
  source, scripts, README text, or reference logs.
- `oracle_residual_inference`: clean-room behavior inferred from oracle output
  residuals because the public reducer core is unavailable.
- `diagnostic_only`: report-surface or evidence improvement that does not
  change scientific output.

Prefer `source_contract` fixes over residual fitting. `oracle_residual_inference`
is allowed for SP/SP+ reducer parity, but the test/evidence must name the
residual being closed and must not weaken existing mismatch diagnostics.

## Updated Work Order

1. **Source trace and I/O contract slice**
   - Add focused evidence that `Z1plus-code` is available locally and identify
     the official scripts that define output/input semantics.
   - Lock SP+ `Z1+SP.dat` interpretation to the official helper scripts:
     `x y z source E paired_chain paired_node`.
   - Check whether existing parser/writer tests need source-backed assertions
     for `.dat`, `.dump`, and SP+ pair annotation semantics.

2. **Parser/writer and converter alignment**
   - Compare current `pyz1` behavior against:
     - `scripts/Z1+dat2dump.pl`
     - `scripts/Z1+SP-to-data.pl`
     - `scripts/extract-single-chain-entanglements.pl`
     - `scripts/Z1+import-lammps.pl`
     - `replacements/Z1+template.pl`
   - Prioritize sheared/triclinic box handling, folded/unfolded coordinate
     semantics, LAMMPS id to Z1 id/mol/bead mapping, SP+ 7-column parsing, and
     path/quoting behavior.
   - Add failing focused assertions before changing `pyz1`.

3. **Benchmark-05 SP+ reducer parity continues**
   - Continue the current benchmark-05 SP+ direction, because SP/SP+ details
     should match Z1+ oracle as closely as possible for the same system.
   - Start from remaining chain49 source/position placement,
     paired-chain coverage, reciprocal placement, and final node-count gaps.
   - Before each reducer change, re-check the public source/script contract and
     label the change as `source_contract` or `oracle_residual_inference`.
   - Benchmark-04 SP+ must remain passed.

4. **Benchmark 07/10/11 oracle/log smoke expansion**
   - Use `Z1plus-code/benchmark-configurations` to add a report surface for
     benchmark 07/10/11 inputs and reference logs.
   - Start with log/metadata smoke and parser/report coverage, not full reducer
     parity.
   - Keep large-case performance guards explicit until the reducer has the
     needed acceleration.

5. **PPA/PPA+ validation refinement**
   - Keep PPA/PPA+ coordinate-level strict parity out of scope unless a future
     source-backed deterministic contract justifies it.
   - Use the GitHub reference logs to strengthen PPA+ smoke, summary/report, and
     known-invalid classification.
   - Preserve the existing conclusion that PPA/PPA+ depends on classical
     parameters and is only meaningful for compatible Kremer-Grest-style systems
     with maximum bond length constraints.

6. **Final integration gate**
   - Continue to require evidence for parser/writer, summary/Ne, oracle parity,
     PPA/PPA+, clean-room reducer, SP+ regression, docs, and package smoke.
   - Evidence must be traceable by path and should include source trace,
     focused RED/GREEN, full gate, benchmark report, static checks, package
     smoke, and docs updates.

## Per-Slice Gate

For every non-trivial future slice:

1. Inspect live repo state with `git status --short --branch`.
2. Read the relevant visible Z1+/Z1plus-code source files before designing the
   change.
3. Write a focused failing assertion or diagnostic artifact first.
4. Implement the smallest change that closes that assertion.
5. Run the appropriate gate through the current accepted execution route. For
   long or broad tests, prefer the GPU-cluster Slurm workflow and record job
   IDs, exit codes, and artifact paths.
6. Confirm benchmark-04 SP+ remains passed whenever reducer behavior changes.
7. Confirm mismatch diagnostics are not weakened or removed.
8. Update evidence/docs with:
   - source paths and Git SHA when applicable;
   - RED and GREEN artifacts;
   - benchmark deltas;
   - open residuals.
9. Commit and push only after the slice gate is closed, the worktree side
   effects are understood, and docs/evidence are synchronized.

## Must Not Do

- Do not treat `mkmat/Z1plus-code` as the hidden Fortran reducer core.
- Do not copy or depend on private/unavailable Z1 reducer code.
- Do not use `Z1+.ex` as a package runtime dependency.
- Do not chase PPA/PPA+ coordinate equality without a source-backed deterministic
  contract.
- Do not weaken existing mismatch diagnostics to make a benchmark pass.
- Do not add benchmark-specific reducer constants without naming whether the
  rationale is source-backed or oracle-residual clean-room inference.
- Do not push RED/GREEN-incomplete slices or worktrees with unexplained
  side-effects.

## Immediate Next Slice

The source-trace/I/O-contract pass has current evidence for SP+ column
semantics, negative-`xy` triclinic LAMMPS dump bounds, and Z1+ wrapper path
quoting. The next development slice should return to benchmark-05 SP+ reducer
parity while preserving benchmark-04 SP+ passed.

Start with the remaining benchmark-05 reciprocal source/position placement and
paired-chain coverage gaps after task-149 aligned the chain48 local pair
sequence. Remaining active chain is chain49. Before each reducer change,
re-check the visible
Z1+/Z1plus-code source surface and classify the rationale as `source_contract`
or `oracle_residual_inference`. Keep benchmark-04 SP+ passed and do not weaken
existing mismatch diagnostics.
