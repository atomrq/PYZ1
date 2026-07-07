# Task 178 Statistical Residual Budget Source Trace

Classification: `diagnostic_only`

Source context:

- Public Z1+/Z1plus-code source does not expose the hidden Z1 reducer core used
  to produce final SP/SP+ per-chain geometry.
- The project acceptance boundary now treats SP/SP+ parity as
  statistical/ensemble parity, while per-chain contour residuals remain
  diagnostics unless they protect a generalized source/topology/contact rule.
- Existing `pyz1` benchmark regression reports already carried max, mean, RMS,
  and detailed per-chain contour residual diagnostics.

Change rationale:

- Add distributional residual-budget fields to the regression report:
  `chain_contour_residual_count` and `chain_contour_residual_fraction`.
- These fields summarize how broad the contour residual surface is without
  turning any one chain's final geometry into a pass/fail target.
- Reducer runtime behavior, strict mismatch diagnostics, and statistical status
  logic are unchanged.

Remote evidence:

- RED focused job `416842` failed because `RegressionRecord` did not expose
  `chain_contour_residual_count`.
- GREEN focused job `416843` passed.
- Static job `416844` passed `ruff` and `basedpyright`.
- Package smoke job `416849` generated the installed CLI report with benchmark
  05 SP+ `chain contour residual count = 32` and
  `chain contour residual fraction = 0.64`.
- Docs gate job `416852` passed `git diff --check` through a temporary remote
  git index.
