# Task 179 Contour Residual P95 Source Trace

Classification: `diagnostic_only`

Source context:

- Public Z1+/Z1plus-code source still does not expose the hidden Z1 reducer
  core that determines final SP/SP+ per-chain geometry.
- Task-177 defines SP/SP+ parity as an ensemble/statistical target, with
  per-chain residuals retained as diagnostics unless they protect a generalized
  source/topology/contact rule.
- Task-178 added chain-contour residual count/fraction to move from single-chain
  residual chasing toward a distributional residual budget.

Change rationale:

- Add `chain_contour_residual_p95_delta` to the regression record and markdown
  report.
- The value is the nearest-rank p95 over finite chain-contour residual deltas.
- This exposes residual-tail behavior while preserving strict mismatch details
  and without changing reducer runtime behavior or statistical status logic.

Remote evidence:

- RED focused job `416853` failed because `RegressionRecord` did not expose
  `chain_contour_residual_p95_delta`.
- GREEN focused job `416858` passed.
- Static job `416859` passed `ruff` and `basedpyright`.
- Package smoke job `416860` generated the installed CLI report with benchmark
  05 SP+ `chain contour residual p95 delta = 0.813482`.
- Docs gate job `416862` passed `git diff --check` through a temporary remote
  git index.
