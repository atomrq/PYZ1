# Task 177 Statistical Acceptance Boundary

Classification: `diagnostic_only`

User correction:

- SP/SP+ parity is a statistical/ensemble target, not exact equality for every
  individual chain.
- Per-chain contour and final-geometry residuals remain diagnostics for
  discovering missing generalized reducer rules.
- A chain-level assertion should be a GREEN acceptance criterion only when it
  protects a source-backed or input-derived topology/contact rule.

Repository changes:

- `docs/source-informed-development-plan.md` now frames benchmark-05 SP+
  continuation as statistical reducer parity.
- The immediate next slice now asks future reducer work to convert remaining
  largest-chain residual framing into a statistical residual budget or
  distributional metric before changing the reducer.

Verification:

- `git diff --check -- docs/source-informed-development-plan.md`

Notes:

- No reducer runtime behavior changed in this slice.
- No local long tests were run because this is a docs/evidence policy update.
