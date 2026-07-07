# Task 162 source trace: contact-constrained relaxation helper

Date: 2026-07-07

## Source state

- Local official supplemental tree:
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- Commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- Public reducer core status: no visible `module-Z1.f90`,
  `module-functions.f90`, or equivalent Z1 reducer core implementation.

## Classification

`oracle_residual_inference_generalizable`.

Task161 showed benchmark-05 chain37 contour residuals are geometry residuals,
but the project-level policy rejects oracle final-coordinate hardcoding as a
formal reducer solution. This slice starts a general replacement path: a pure
geometry helper that relaxes one retained node using only endpoint geometry,
the current node, a contact segment, and a maximum contact distance.

## Visible Source Boundary

- Visible Z1+/Z1plus-code source confirms SP/SP+ output and helper semantics.
- Visible source does not define the hidden Z1 reducer relaxation rule.
- The helper therefore uses only clean-room geometry primitives already present
  in `pyz1.geometry`: `Segment`, `closest_segment_points`, `segment_distance`,
  and `chain_contour`.
- Implementation is isolated in `src/pyz1/contact_relaxation.py` rather than
  adding more logic to the already large geometry/reducer modules.

## Acceptance Scope

This is not a benchmark-05 GREEN claim. It is a small generalized geometry
building block for later endpoint-fixed/contact-constrained reducer work.
