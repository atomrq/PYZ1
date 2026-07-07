# Task 185 Source Trace: Benchmark Regression Summary Input Deltas

Classification: `source_contract`.

Source evidence:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`
  documents `Z1+summary.dat` column 14 as mean bond length of the original
  chain and column 15 as bead number density of the original configuration.
- The same README documents the preceding structured summary fields now already
  exposed by the benchmark regression report: `Lpp`, `Z`, `Ree`, `app`, `bpp`,
  `Lpp2`, `Ne_CK`, `Ne_MK`, `Ne_CC`, and `Ne_MC`.

Implementation:

- `RegressionRecord` now carries `mean_original_bond_length_delta` and
  `original_bead_density_delta`.
- `pyz1-benchmark-regression` markdown output now reports `b0 delta` and
  `density delta`.
- This is a report/evidence surface change only. It does not change reducer
  runtime behavior, strict status, statistical status, or mismatch diagnostics.

Remote GPU-cluster evidence:

- RED job `416910`: focused pytest failed for the intended reason:
  `RegressionRecord` did not expose `mean_original_bond_length_delta`.
- Superseded GREEN job `416911`: focused pytest passed before the test was
  refactored to satisfy the ruff statement-count rule.
- Superseded static job `416912`: failed with `PLR0915` after the RED assertion
  pushed the focused test over the statement limit.
- Superseded package-smoke job `416913`: generated the report surface but
  failed because the script expected exact-zero `b0 delta`; the actual
  source-backed residual is `2.02002e-07`.
- Final GREEN job `416914`: focused benchmark-05 SP+ contact-relaxation report
  test passed.
- Final static job `416915`: `ruff` and `basedpyright` passed for
  `src/pyz1/regression.py` and `tests/test_spplus_regression.py`.
- Final package smoke job `416916`: installed `pyz1-benchmark-regression`
  passed and wrote
  `.omo/evidence/task-185-regression-summary-input-deltas/benchmark-05-spplus-summary-input-deltas-final.md`.

Final benchmark-05 SP+ contact-relaxation report values:

- strict status: `mismatch`
- statistical status: `passed`
- `b0 delta = 2.02002e-07`
- `density delta = 0`
- `Ree delta = 7.17485e-05`
- `app delta = 0.00295412`
- `bpp delta = 0.00058405`
- `Lpp2 delta = 0.00945984`

The input summary deltas are retained as statistical/report evidence. They are
not treated as exact-summary hard failures.
