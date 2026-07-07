# Task 167 Source Trace

Date: 2026-07-07

## Classification

`oracle_residual_inference_generalizable`

## Acceptance Direction

Task167 was redirected from per-chain micro-parity to statistical parity. The
benchmark-05 chain3 residual remains useful RED/diagnostic evidence because it
exposed a missing single-contact relaxation path, but the accepted GREEN is the
report-level statistical movement: lower `Lpp`/summary residuals while keeping
pair mismatches, node-count mismatches, source residual details, and `Z` delta
closed. Exact per-chain final geometry equality is not the target.

## Sources Checked

- `/Users/jiaxm/.codex/RESOURCES.md`
  - Confirms the local source mirror and GPU cluster route conventions.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
  - Public install-package mirror with `Z1+.ex`, output helpers, folding logic,
    PPA/CPPA modules, and benchmark inputs.
  - The hidden Z1 reducer core remains unavailable:
    `module-Z1.f90` / `module-functions.f90`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  - Local mirror of `https://github.com/mkmat/Z1plus-code`.
  - Checked commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`.
  - Public scripts and README define parser/writer and LAMMPS conversion
    contracts, but do not expose the hidden Z1 reducer relaxation core.
- `.omo/evidence/task-166-chain17-multinode-relaxation/benchmark-04-05-spplus-contact-relaxation.md`
  - Identifies benchmark-05 chain3 as the current guard-enabled largest
    contour residual after task166.
- `src/pyz1/contact_relaxation.py`
  - Existing helper performs endpoint-fixed contact-constrained local node
    relaxation from input-derived contact segments.
- `src/pyz1/reducer.py`
  - Task166 final pass only revisits already-retained two-contact chains.
    Benchmark-05 chain3 has one retained pair contact, matching oracle source,
    pair, and node count, so it is not currently eligible for the final pass.

## Clean-Room Boundary

The implementation targets a generalized single retained-contact final
relaxation path. It uses only current retained geometry, source ordering, pair
topology, and pair contact segments from the input-derived reducer state. It
does not copy oracle final coordinates and does not use oracle output as
runtime input.

The previous task166 evidence rejected an unconditional 3+ retained-node pass.
Task167 must not reintroduce that broad 3+ path without a stronger solver and
separate RED coverage.

The first broad single-contact attempt was also rejected: job `416741`
improved chain3 but worsened benchmark-05 report diagnostics (`Lpp delta`
regressed to `0.12753`, max chain-contour delta regressed to `1.50772` on
chain36). The final implementation accepts a single-contact move only when the
move remains within the original contact-clearance scale and an absolute
displacement cap.

## Remote Gate

Remote GPU-cluster run directory:
`/public/home/jxm/pyz1-cleanroom-runs/task-167-chain3-single-contact`

- Invalid RED setup job `416738` failed because `PYTHONPATH=src` was missing
  and the remote job imported an older installed `pyz1`.
- Corrected RED job `416739` failed for the intended chain3 diagnostic
  assertion: guard-enabled relaxation left contour unchanged.
- Superseded broad attempt jobs `416740` and `416741` showed chain3 could be
  shortened, but report diagnostics worsened and that approach was rejected.
- Final focused job `416747` passed 17 tests.
- Final static job `416751` passed ruff and basedpyright after superseded
  static job `416748` caught E501 line-length failures.
- Final package smoke job `416749` passed.
- Final benchmark report job `416750` kept benchmark-04 SP+ `passed` and
  benchmark-05 SP+ as a true `mismatch`, with `Lpp delta = 0.00409694`,
  `Z delta = 0`, max chain-contour delta `0.886959` on chain5, pair
  mismatches `0`, node-count mismatches `0`, and source residual details
  `none`.
