# Task 165 Source Trace

Date: 2026-07-07

## Classification

`diagnostic_only` / `oracle_residual_inference_generalizable`

## Sources Checked

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
  - Public install-package mirror with `Z1+.ex`, output helpers, folding logic,
    PPA/CPPA modules, and benchmark inputs.
  - The hidden Z1 reducer core remains unavailable:
    `module-Z1.f90` / `module-functions.f90`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  - Local mirror of `https://github.com/mkmat/Z1plus-code`.
  - Pinned checkout for this source-informed plan:
    `c7219cd394b1295272ebfc098f2835c5c871e6ec`.
- `src/pyz1/reducer.py`
  - Existing chain17 logic covers source/pair candidate selection and pair
    sequence overrides.
  - No chain17 oracle final-position shim is present.
- `.omo/evidence/task-164-relaxation-report-surface/benchmark-04-05-spplus-contact-relaxation.md`
  - Guard-enabled benchmark-04/05 SP+ report identifies chain17 as the largest
    remaining chain-contour residual.

## Diagnostic Boundary

This slice uses benchmark-05 SP+ oracle output only as a measurement target.
It does not feed oracle final coordinates into reducer runtime behavior and
does not add benchmark-specific `Vector3(...)` constants.

The observed chain17 residual is therefore treated as evidence for a missing
general relaxation rule: endpoint-fixed, topology-preserving, multi-node
contact-constrained shortening using input geometry, source order, pair
topology, and contact candidates.
