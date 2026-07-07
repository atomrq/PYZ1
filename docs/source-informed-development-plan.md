# Source-Informed Development Plan

Last updated: 2026-07-07.

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

## Reducer Generalization Policy

SP/SP+ detail parity remains a goal, but reducer runtime behavior must move
toward a clean-room algorithm that can run on new systems without oracle final
coordinates. Oracle output is allowed as a teacher and regression target; it is
not allowed as production reducer input.

The primary long-term parity target is statistical parity, not exact
per-chain final geometry equality. Chain-level source, pair, node-count,
contour, and coordinate residuals remain important diagnostics for discovering
missing rules, but they are not the final objective by themselves. Prefer
changes that improve summary/statistical outputs such as `Lpp`, `Z`, `Ne`,
mean/root-mean-square contour measures, and report-level parity while
preserving closed topology diagnostics. Do not turn every remaining per-chain
contour or coordinate residual into a benchmark-specific acceptance target.
Exact SP/SP+ detail matching remains useful when it protects a generalized
topology/source/pairing rule, but a new slice should not be judged solely by
whether every individual chain overlays the oracle chain. Acceptance should
separate statistical parity gates from chain-level diagnostic regressions.
The benchmark regression report now carries a separate `statistical status`
column for that purpose: strict `status` continues to protect detailed
per-chain/oracle diagnostics, while `statistical status` tracks report-level
`Lpp`, `Z`, pairing, node-count, and source-sequence closure without treating
every remaining chain contour residual as an acceptance failure.

Do not treat benchmark-specific oracle final geometry as a final reducer
solution. Any `Vector3(...)` coordinate copied from a Z1+ oracle SP/SP+ output
is only a diagnostic scaffold or temporary oracle-regression shim unless and
until it is replaced by a rule derived from the input system itself.

Reducer implementation should depend on information available for any input:

- chain endpoints and current chain geometry;
- box, shear, PBC/folded-unfolded coordinate handling;
- obstacle/contact constraints and candidate contact surfaces;
- pair topology, paired node ordering, and source bead/contour ordering;
- endpoint-fixed, topology-preserving constrained shortening or relaxation
  rules.

When oracle residuals expose a geometry gap, the GREEN target is not "copy the
oracle coordinate". The GREEN target is to identify and implement a
generalizable constrained-relaxation rule, then use oracle fixtures to measure
whether that rule moves parity in the right direction.

If a short-term regression scaffold must retain oracle-position constants, it
must be explicitly labeled `temporary oracle-regression shim` in code-adjacent
evidence and docs, with an owner task to replace it. Do not add new
benchmark-specific final-position constants as normal reducer progress.

Current audit and replacement plan:
`docs/reducer-oracle-geometry-audit.md`.

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
   - Paired-chain coverage and final node count are now locally closed for the
     task-150 benchmark-05 SP+ slice; continue from final geometry, Lpp, and
     summary mismatch diagnostics.
   - For final geometry and contour residuals, prefer generalized
     endpoint-fixed/contact-constrained relaxation over benchmark-specific
     oracle-position constants. Existing oracle-position shims must be audited
     and replaced rather than expanded.
   - Before each reducer change, re-check the public source/script contract and
     label the change as `source_contract` or `oracle_residual_inference`.
   - Benchmark-04 SP+ must remain passed.

4. **Benchmark 07/10/11 oracle/log smoke expansion**
   - Use `Z1plus-code/benchmark-configurations` to add a report surface for
     benchmark 07/10/11 inputs and reference logs.
   - Start with log/metadata smoke and parser/report coverage, not full reducer
     parity.
   - Treat reference-log values as source-backed summary/statistical contracts
     for report surfaces; do not reinterpret them as per-chain geometry
     acceptance gates.
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
- Do not use benchmark-specific oracle final coordinates as a formal reducer
  algorithm. Such coordinates are at most temporary diagnostic/regression shims
  and must have a replacement plan.
- Do not push RED/GREEN-incomplete slices or worktrees with unexplained
  side-effects.

## Immediate Next Slice

The source-trace/I/O-contract pass has current evidence for SP+ column
semantics, negative-`xy` triclinic LAMMPS dump bounds, and Z1+ wrapper path
quoting. The next development slice should return to benchmark-05 SP+ reducer
parity while preserving benchmark-04 SP+ passed.

Task-160 closes the benchmark-05 SP+ chain22 contour residual as
`oracle_residual_inference` after task-159 moved the largest remaining
chain-contour residual from chain43 to chain22. Final regression keeps
benchmark-04 SP+ `passed` and keeps benchmark-05 pair mismatches,
node-count mismatches, source residual details, and `Z` delta closed at
`0`/`none`; benchmark-05 remains a true `mismatch` with `Lpp` delta `0.242685`,
six summary mismatches, and the largest remaining chain-contour residual now
on chain37 (`max chain contour delta = 1.0324`).

Task-161 is redirected from another oracle-coordinate contour patch to a
project-level reducer generalization slice. Keep the chain37 contour RED and
diagnostic evidence, but do not close it by hardcoding the three oracle final
positions. The next reducer work should first audit existing oracle-position
shims and prototype a general endpoint-fixed/contact-constrained relaxation
rule that uses only input-system geometry, topology, and constraints. Before
each reducer change, re-check the visible Z1+/Z1plus-code source surface and
classify the rationale as `source_contract`, `oracle_residual_inference`, or
`diagnostic_only`. Keep benchmark-04 SP+ passed and do not weaken existing
mismatch diagnostics.

Task-162 adds the first generalized building block in
`src/pyz1/contact_relaxation.py`: endpoint-fixed contact-constrained node
relaxation driven by local geometry, not oracle final positions. The next
implementation step is to integrate this kind of helper behind a narrow reducer
guard using input-derived contact candidates, then measure benchmark-04/05 SP+
effects before removing or narrowing existing temporary oracle-regression
shims.

Task-163 performs that first integration step behind
`ReducerSettings.contact_relaxation_enabled`, which defaults to `False`.
The guard uses retained source ordering, pair topology, and pair contact
segments from the current input-derived reducer state. It shortens the
benchmark-05 chain37 focused case while preserving the paired source sequence,
but it is not yet the default reducer path and is not a claim that benchmark-05
full SP+ parity is closed. The next reducer slice should measure full
benchmark-04/05 SP+ deltas with the guard enabled, identify which existing
temporary oracle-regression shims become redundant or conflict with the
general relaxation path, and then retire only those shims that are covered by
remote regression evidence.

Task-164 adds that measurement surface through
`RegressionSettingsOverride` and the `pyz1-benchmark-regression`
`--contact-relaxation` option. Remote benchmark-04/05 SP+ evidence with the
guard enabled keeps benchmark-04 `passed`; benchmark-05 remains a true
`mismatch`, but `Lpp delta` improves from `0.242685` to `0.147902`, max
chain-contour delta improves from `1.0324` on chain37 to `0.999611` on
chain17, and pair mismatches, node-count mismatches, source residual details,
and `Z` delta remain closed. The next reducer slice should inspect the
guard-enabled chain17 residual and compare it against the temporary
oracle-position shims before changing default reducer behavior.

Task-165 performs that inspection as a diagnostic-only slice. Evidence in
`.omo/evidence/task-165-chain17-guard-diagnostic/chain17-geometry.md` shows
that benchmark-05 chain17 already has the expected source/pair sequence and
node count, has no chain17 oracle final-position shim in the reducer, and still
has a `0.999611` guard-enabled contour delta because the interior node geometry
does not relax to the oracle contour. The next RED should therefore target a
general endpoint-fixed multi-node contact-relaxation rule for paired retained
nodes. Do not close the chain17 residual with benchmark-specific final
coordinates.

Task-166 adds the first guarded final-pass version of that rule for already
retained two-contact chains. The pass remains behind
`ReducerSettings.contact_relaxation_enabled`; it uses retained geometry,
source order, pair topology, and pair contact segments, and it adds no oracle
final coordinates. Remote focused/static/package/report evidence in
`.omo/evidence/task-166-chain17-multinode-relaxation/` keeps benchmark-04 SP+
`passed`; benchmark-05 remains a true `mismatch`, but guard-enabled `Lpp delta`
improves to `0.0646243` and max chain-contour delta improves to `0.986713` on
chain3 while pair mismatches, node-count mismatches, source residual details,
and `Z` delta remain closed. A wider 3+ retained-node final pass regressed
benchmark-05 diagnostics and must not be reintroduced without a stronger
multi-node solver and RED coverage.

Task-167 shifts the guarded relaxation acceptance from chain micro-parity
toward statistical parity. It extends the final pass to single retained-contact
chains only when the relaxed move remains within the original contact-clearance
scale and an absolute displacement cap; the 3+ retained-node path remains
excluded. Remote evidence in
`.omo/evidence/task-167-chain3-single-contact-relaxation/` keeps benchmark-04
SP+ `passed`; benchmark-05 remains a true `mismatch`, but guard-enabled `Lpp
delta` improves to `0.00409694`, max chain-contour delta improves to
`0.886959`, pair mismatches, node-count mismatches, source residual details,
and `Z` delta remain closed, and summary fields are much closer. Future
reducer work should use per-chain residuals as diagnostics unless a chain-level
assertion protects topology/source/pair invariants or a clearly generalized
relaxation rule.

Task-168 starts the benchmark 07/10/11 and PPA+ reference-log smoke expansion.
Its scope is a source-backed report/parser surface over public
`Z1plus-code/benchmark-configurations/*reference-results/log-benchmark-XX.txt`
files. This is evidence for summary/statistical parity tracking and package
smoke only; it is not a reducer oracle-coordinate dependency and does not make
per-chain final geometry equality an acceptance gate.

Task-169 adds the matching benchmark 07/10/11 input smoke surface. It parses the
public `.Z1` and `.dump` files from `Z1plus-code/benchmark-configurations` and
reports chain count, node count, true-chain count, box lengths, and shear. This
locks the source-backed input baseline for future statistical parity work and
does not claim reducer parity for those large benchmarks.

Task-170 joins the task168 reference-log smoke and task169 input smoke into a
corpus statistical smoke report. It checks that benchmark 07/10/11 `.Z1` and
`.dump` input statistics agree and that public Z1+/PPA+ reference logs have
zero chain-count and mean-`N` deltas relative to those input statistics. This is
a source-backed statistical baseline gate, not full reducer parity.

Task-171 records the project-level acceptance correction: the long-term reducer
goal is ensemble/statistical parity, not exact equality for every individual
chain. Per-chain SP/SP+ residuals remain useful diagnostics and regression
guards for generalized topology, source, pairing, and contact-relaxation rules,
but future reducer slices should not treat chain-by-chain coordinate overlay as
the primary acceptance condition.

Task-172 applies that policy to the benchmark regression report surface. The
report now includes ensemble `mean chain contour delta` and
`rms chain contour delta` columns next to the existing max chain-contour and
per-chain residual-detail diagnostics. This is a diagnostic/report improvement,
not a reducer algorithm change and not a claim that benchmark-05 full parity is
closed.

Task-173 extends the benchmark 07/10/11 corpus statistical smoke with
source-backed `Z1+ <Z>`, `Z1+ Ne_MC`, and `PPA+ Ne_MC` columns parsed from the
public `mkmat/Z1plus-code` reference logs. This strengthens summary/Ne tracking
for future statistical parity work while keeping the report explicitly separate
from full native reducer or PPA+ runtime parity.

Task-175 extends the same corpus statistical smoke with source-backed
`Z1+ <Lpp>`, `PPA+ <Lpp>`, `PPA+ <Z>`, and `PPA+ Ne_CC` fields from the public
benchmark 07/10/11 reference logs. These are reference-log summary targets for
statistical tracking only; they do not introduce PPA+ coordinate-level parity
requirements.
