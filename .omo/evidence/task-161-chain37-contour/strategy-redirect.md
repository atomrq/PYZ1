# Task 161 Strategy Redirect

Date: 2026-07-07

## Project-Level Correction

Task161 was redirected before commit. The rejected direction was to close the
benchmark-05 chain37 contour residual by copying the three oracle final
positions into reducer constants. That would only reproduce a known oracle
fixture and would not generalize to new systems.

The current project rule is:

- SP/SP+ detail parity remains a target.
- Oracle output can identify missing rules and measure residuals.
- Production reducer logic must not require oracle final coordinates.
- Benchmark-specific oracle `Vector3(...)` values are at most temporary
  oracle-regression shims and technical debt.
- Future GREEN work should implement generalized endpoint-fixed,
  topology-preserving, contact/obstacle-constrained relaxation or shortening.

## Evidence State

- `416675`: invalid RED setup failure; missing `PYZ1_SOURCE_Z1` on the remote
  run root.
- `416676`: valid RED; chain37 contour assertion failed for the intended
  residual:
  - actual `15.732259528203835`
  - oracle `14.699862363269872`
  - delta `1.032397164933963`
- `416677`: diagnostic; chain37 node count, source beads, and pair sequence
  match oracle, but retained final positions differ.
- `416678` and `416679`: superseded hardcode-attempt jobs submitted before the
  project-level correction arrived. Their outputs are not acceptance evidence
  for a formal reducer fix.

## Current Task161 Status

Task161 is not GREEN. The retained RED assertion is useful, but closing it by
oracle final-position hardcoding is rejected. The next valid implementation
step is to design and test a generalized constrained relaxation helper using
input geometry, source ordering, pair topology, and contact/obstacle
constraints.
