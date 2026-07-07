# Task 171 Statistical Parity Policy

Classification: `diagnostic_only`.

This slice records the project-level correction that the long-term `pyz1`
clean-room reducer target is statistical parity against Z1+, not exact equality
for every individual chain's SP/SP+ final geometry.

## Source And Evidence Baseline

- `docs/source-informed-development-plan.md` already states that the primary
  long-term parity target is statistical parity and that chain-level source,
  pair, node-count, contour, and coordinate residuals are diagnostics.
- `docs/reducer-oracle-geometry-audit.md` keeps benchmark-specific oracle final
  coordinates out of the formal clean-room reducer algorithm.
- `.omo/evidence/task-168-reference-log-smoke/` records source-backed public
  Z1+/PPA+ benchmark 07/10/11 reference-log parsing.
- `.omo/evidence/task-169-benchmark-input-smoke/` records source-backed public
  benchmark 07/10/11 `.Z1`/`.dump` input parsing.
- `.omo/evidence/task-170-corpus-stat-smoke/` records the first combined
  source-backed corpus statistical smoke gate.

## Policy

Future SP/SP+ reducer development should optimize for ensemble/report metrics
such as `Lpp`, `Z`, `Ne`, contour distributions, chain-count consistency, and
reference-log statistical agreement.

Per-chain shortest-path node counts, source positions, contour residuals, final
coordinates, and SP+ pairs remain important diagnostics. They should block a
slice when they expose a broken generalized topology, source-ordering,
pairing, contact, or relaxation rule, or when a change weakens existing
mismatch diagnostics. They should not become the final acceptance condition
that every individual chain must exactly overlay the Z1+ oracle.

Oracle output can still teach missing rules and measure residuals. It must not
be used as runtime input, and benchmark-specific oracle final geometry must not
be hardcoded as the formal reducer solution.

## Updated Docs

- `docs/pyz1-contract.md`: clean-room geometry contract now separates
  statistical acceptance from per-chain diagnostics.
- `docs/completion-audit.md`: current audit now includes task168-170 corpus
  statistical smoke evidence and the task171 parity-policy correction.
- `docs/evidence-ledger.md`: current gate index now points to this
  diagnostic-only policy artifact.
- `docs/source-informed-development-plan.md`: immediate next-slice guidance now
  records task171 as a durable project constraint.
