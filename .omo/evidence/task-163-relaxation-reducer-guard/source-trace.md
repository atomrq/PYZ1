# Task 163 source trace: settings-gated reducer contact relaxation

Date: 2026-07-07

## Source state

- Local official supplemental tree:
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- Commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- Public reducer core status: no visible `module-Z1.f90`,
  `module-functions.f90`, or equivalent Z1 reducer core implementation.

## Classification

`oracle_residual_inference_generalizable`.

Task162 introduced a pure geometry helper that relaxes one retained node using
only local endpoint geometry and contact constraints. Task163 tests a
settings-gated reducer integration path. The RED target does not assert oracle
final coordinates. It requires only that enabling the generalized relaxation
shortens benchmark-05 chain37 while preserving the paired source sequence.

## Visible Source Boundary

- Visible Z1+/Z1plus-code source confirms SP/SP+ output and helper semantics.
- The hidden Z1 reducer relaxation rule is still unavailable.
- This slice therefore uses the oracle residual only to select a real benchmark
  with a known contour gap; the implementation must use input-derived contacts,
  endpoints, and pair topology.
