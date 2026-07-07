# Task 164 source trace: contact relaxation report surface

Date: 2026-07-07

## Source state

- Local official supplemental tree:
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- Commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- Public reducer core status: no visible `module-Z1.f90`,
  `module-functions.f90`, or equivalent Z1 reducer core implementation.

## Classification

`diagnostic_only` with `oracle_residual_inference_generalizable` measurement.

Task163 added a default-off reducer guard,
`ReducerSettings.contact_relaxation_enabled`, that uses input-derived contact
geometry and pair topology. Task164 does not change default reducer behavior.
It adds a regression/report surface so the guard can be measured through the
same benchmark report machinery used for SP/SP+ parity.

## Visible Source Boundary

- Visible Z1+/Z1plus-code source confirms public SP/SP+ output/report
  semantics, but the hidden Z1 relaxation core is still unavailable.
- The new report path therefore uses oracle fixtures only to measure residuals
  and does not use oracle final coordinates as reducer input.
