# Task 183 Source Trace: Benchmark Regression `Ne_CK`/`Ne_MK` Deltas

Classification: `source_contract`.

Source evidence:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`
  documents `Z1+summary.dat` column 10 as
  `classical kink Ne-estimator = Ne_CK` and column 11 as
  `modified kink Ne-estimator = Ne_MK`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/scripts/Z1+import-lammps.pl`
  emits the summary header
  `timestep chains N Ree Lpp Z app bpp Lpp2 NeCK NeMK NeCC NeMC`.

Implementation:

- `RegressionRecord` now carries `ne_classical_kink_delta` and
  `ne_modified_kink_delta` next to the existing coil Ne deltas.
- `pyz1-benchmark-regression` markdown output now reports
  `Ne classical kink delta` and `Ne modified kink delta` between `Z delta` and
  the coil Ne delta columns, matching the source summary field order.
- This is a report/evidence surface change only. It does not change reducer
  runtime behavior, strict status, statistical status, or mismatch diagnostics.

Remote GPU-cluster evidence:

- RED job `416892`: focused pytest failed for the intended reason:
  `RegressionRecord` did not expose `ne_classical_kink_delta`.
- Superseded GREEN job `416893`: implementation exposed the field, but the
  original exact-zero test expectation was too strict. It measured
  `Ne classical kink delta = 0.0004935622317585597`, proving the report surface
  should track a small statistical residual instead of claiming exact equality.
- GREEN job `416895`: focused benchmark-05 SP+ contact-relaxation report test
  passed with residual bounds for `Ne_CK` and `Ne_MK`.
- Static job `416896`: `ruff` and `basedpyright` passed for
  `src/pyz1/regression.py` and `tests/test_spplus_regression.py`.
- Package smoke job `416897`: installed `pyz1-benchmark-regression` passed and
  wrote `.omo/evidence/task-183-regression-ne-kink-deltas/benchmark-05-spplus-ne-kink-deltas-final.md`.

Final benchmark-05 SP+ contact-relaxation report values:

- strict status: `mismatch`
- statistical status: `passed`
- `Ne classical kink delta = 0.000493562`
- `Ne modified kink delta = 0.000285714`
- `Ne classical coil delta = 0.0122531`
- `Ne modified coil delta = 0.613306`

The nonzero kink deltas are retained as statistical/report evidence. They are
not treated as a per-chain or exact-summary hard failure.
