# task-174 statistical regression status source trace

Classification: `diagnostic_only`.

This slice implements the project-level parity correction recorded in
`docs/source-informed-development-plan.md`: the long-term clean-room reducer
target is statistical parity at the ensemble/report level, not exact equality
for every individual chain. Chain-level SP/SP+ contour, source, pair, node, and
coordinate residuals remain diagnostics and regression guards.

Relevant repo sources:

- `docs/source-informed-development-plan.md`: reducer generalization and
  statistical parity policy.
- `docs/evidence-ledger.md`: task-171 and task-172 evidence for separating
  statistical/report-level tracking from per-chain diagnostics.
- `src/pyz1/regression.py`: benchmark regression report writer and current
  strict `RegressionStatus` calculation.
- `tests/test_spplus_regression.py`: benchmark-05 SP+ contact-relaxation report
  coverage with closed pairing/node/source-sequence gaps and residual contour
  diagnostics.

Implementation intent:

- Add a report-level statistical status beside the existing strict status.
- Keep strict `status` unchanged, so benchmark-specific per-chain residuals and
  mismatch diagnostics are not weakened.
- Base the statistical status on ensemble/topology fields already computed by
  the report (`Lpp`, `Z`, pairing, node count, and source-sequence closure),
  not on per-chain coordinate equality.
- Do not change reducer runtime behavior.
