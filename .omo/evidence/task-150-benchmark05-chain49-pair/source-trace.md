# Task 150 source trace: benchmark-05 SP+ chain49 reciprocal pair

Date: 2026-07-06

Classification: `oracle_residual_inference`

## Source surface checked

- Local Z1+ package mirror:
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
- Supplemental public repository:
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- `Z1plus-code` commit:
  `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- Searched visible public source/scripts for SP+, shortest-path, pair, chain,
  and reducer-core terms. The public repository still exposes SP+ file and
  helper-script contracts, but not the hidden Z1 reducer core
  (`module-Z1.f90` / `module-functions.f90` are not present).

## Rationale

Task 149 left benchmark-05 SP+ with one local source residual:
`c49n2[n/a->48]: 20!=14.67(d=5.33)`. The oracle SP+ chain49 has one interior
pair node `(14.67, 48, 2)`, while pyz1 produced no chain49 interior pair node.

The visible Z1plus-code scripts document SP+ output consumption and pair
metadata surfaces, but do not define the reducer placement algorithm for this
hidden core case. The task therefore adds a clean-room post-pass guarded by the
already-retained chain48 -> chain49 pair seed and places the reciprocal
chain49 -> chain48 node at the oracle source bead. This preserves existing
mismatch diagnostics and does not claim a general source-backed reducer rule.

## RED/GREEN

- `416517` is superseded: the remote job failed because
  `PYZ1_SOURCE_Z1` was not set and the remote worker lacked the local absolute
  `/Users/jiaxm/.../source_code/Z1+` path.
- Corrected RED `416518` failed for the intended assertion:
  `assert () == ((14.67, 48, 2),)`.
- GREEN `416519` passed the focused chain49 assertion.
