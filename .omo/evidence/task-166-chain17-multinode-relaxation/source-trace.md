# Task 166 Source Trace

Date: 2026-07-07

## Classification

`oracle_residual_inference_generalizable`

## Sources Checked

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
  - Public install-package mirror with `Z1+.ex`, output helpers, folding logic,
    PPA/CPPA modules, and benchmark inputs.
  - The hidden Z1 reducer core remains unavailable:
    `module-Z1.f90` / `module-functions.f90`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  - Local mirror of `https://github.com/mkmat/Z1plus-code`.
  - Pinned source-informed checkout:
    `c7219cd394b1295272ebfc098f2835c5c871e6ec`.
- `.omo/evidence/task-165-chain17-guard-diagnostic/chain17-geometry.md`
  - Identified benchmark-05 chain17 as a two-retained-contact geometry
    residual: source/pair sequence and node count were closed, but guard
    contour did not shorten.
- `src/pyz1/contact_relaxation.py`
  - Existing helper performs endpoint-fixed contact-constrained relaxation
    from input-derived contact segments.
- `src/pyz1/reducer.py`
  - Final chain17 pair/source sequence is assembled after the first guarded
    reciprocal insertion pass, so task166 adds a second guard-only final pass
    over already-retained two-contact chains.

## Clean-Room Boundary

The implementation does not add oracle final coordinates and does not use
oracle output as runtime input. The final pass uses only current retained chain
geometry, source ordering, pair topology, and pair contact segments already
present in the reducer state.

The final pass is deliberately limited to two retained candidates. A wider
unconditional pass over 3+ retained nodes regressed benchmark-05 max
chain-contour diagnostics in job `416729`; that failed evidence is retained in
`sacct.txt` and `focused-suite-final-416729.out`.

## Remote Gate

Remote GPU-cluster run directory:
`/public/home/jxm/pyz1-cleanroom-runs/task-166-chain17-relaxation`

- RED focused job `416705` failed for the intended assertion:
  chain17 guard contour stayed `15.444350512243195`.
- Final focused job `416734` passed 17 focused tests, including chain17,
  chain37, guarded report, CLI guarded report, and geometry tests.
- Final static job `416735` passed ruff and basedpyright for changed reducer
  and regression-test files.
- Final package smoke job `416736` passed.
- Final benchmark report job `416737` kept benchmark-04 SP+ `passed` and
  benchmark-05 SP+ as a true `mismatch`, with pair mismatches, node-count
  mismatches, source residual details, and `Z` delta closed.

Task166 benchmark-05 guard metrics:

- `Lpp delta`: `0.0646243`
- `max chain contour delta`: `0.986713` on chain3
- previous task164 guard metrics were `Lpp delta = 0.147902` and
  `max chain contour delta = 0.999611` on chain17.
