# Task 184 Source Trace: Benchmark Regression Summary Physical Deltas

Classification: `source_contract`.

Source evidence:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`
  documents `Z1+summary.dat` column 4 as mean squared end-to-end distance,
  column 7 as coil tube diameter `app`, column 8 as coil tube step length
  `bpp`, and column 9 as square root of mean squared contour length
  `sqrt(<Lpp^2>)`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/scripts/Z1+import-lammps.pl`
  emits the summary header
  `timestep chains N Ree Lpp Z app bpp Lpp2 NeCK NeMK NeCC NeMC`.

Implementation:

- `RegressionRecord` now carries `mean_squared_end_to_end_delta`,
  `coil_tube_diameter_delta`, `coil_tube_step_length_delta`, and
  `root_mean_squared_contour_delta`.
- `pyz1-benchmark-regression` markdown output now reports
  `Ree delta`, `app delta`, `bpp delta`, and `Lpp2 delta`.
- This is a report/evidence surface change only. It does not change reducer
  runtime behavior, strict status, statistical status, or mismatch diagnostics.

Remote GPU-cluster evidence:

- RED job `416899`: focused pytest failed for the intended reason:
  `RegressionRecord` did not expose `mean_squared_end_to_end_delta`.
- Superseded focused GREEN job `416900`: passed before the test was refactored
  to satisfy the ruff statement-count rule.
- Superseded static job `416904`: failed with `PLR0915` after the RED assertion
  pushed the focused test over the statement limit.
- Superseded package-smoke job `416905`: generated the final report surface but
  failed only because the script's exact-row grep expectation used guessed
  residual values.
- Final GREEN job `416906`: focused benchmark-05 SP+ contact-relaxation report
  test passed.
- Final static job `416907`: `ruff` and `basedpyright` passed for
  `src/pyz1/regression.py` and `tests/test_spplus_regression.py`.
- Final package smoke job `416908`: installed `pyz1-benchmark-regression`
  passed and wrote
  `.omo/evidence/task-184-regression-summary-physical-deltas/benchmark-05-spplus-summary-physical-deltas-final.md`.

Final benchmark-05 SP+ contact-relaxation report values:

- strict status: `mismatch`
- statistical status: `passed`
- `Ree delta = 7.17485e-05`
- `app delta = 0.00295412`
- `bpp delta = 0.00058405`
- `Lpp2 delta = 0.00945984`
- `Ne classical kink delta = 0.000493562`
- `Ne modified kink delta = 0.000285714`
- `Ne classical coil delta = 0.0122531`
- `Ne modified coil delta = 0.613306`

The physical summary deltas are retained as statistical/report evidence. They
are not treated as exact-summary hard failures.
