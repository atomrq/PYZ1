# Task 172 Regression Statistical Contour Metrics

Classification: `diagnostic_only`.

This slice implements the task171 statistical-parity policy in the default/SP+
benchmark regression report. It adds ensemble-level chain-contour statistics to
the existing report surface while preserving per-chain contour residual details
and existing mismatch diagnostics.

## Source Boundary

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
  - Public Z1+ source/oracle mirror used for benchmark `.benchmark-05.Z1`
    input.
  - The hidden default reducer core is still unavailable and was not used.
- `tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703`
  - Existing oracle fixture corpus used for benchmark-05 SP+ report comparison.
- `docs/source-informed-development-plan.md`
  - Requires statistical/ensemble parity to be separated from per-chain
    diagnostic regressions.

## Change

`src/pyz1/regression.py` now reports:

- `mean chain contour delta`
- `rms chain contour delta`

These are computed over chain-contour deltas shared by the native and oracle
shortest-path snapshots. They do not change pass/mismatch classification. The
existing `max chain contour delta`, chain id, and residual-detail columns remain
in the report, so per-chain diagnostics are still available.

## RED/GREEN

- Correct RED: `red-focused-416798.out`
  - Focused benchmark-05 SP+ contact-relaxation report test failed with
    `AttributeError: 'RegressionRecord' object has no attribute
    'mean_chain_contour_delta'`.
- Invalid setup RED: `red-focused-416797.out`
  - Failed because the first remote run did not set `PYZ1_SOURCE_Z1` to a
    cluster-visible source mirror.
- Superseded GREEN: `focused-green-416799.out`
  - Failed because the Slurm environment imported an older editable install
    from task170 instead of the current run root.
- Final GREEN: `focused-green-416800.out`
  - `1 passed in 31.01s` with `PYTHONPATH=$PWD/src`.

## Final Validation

- `static-416802.out`: `ruff` and `basedpyright` passed for
  `src/pyz1/regression.py` and `tests/test_spplus_regression.py`.
- `package-smoke-416804.out`: editable install passed, console-script
  regression report generated benchmark-05 SP+ with contact relaxation, and
  the report contains the new mean/RMS contour columns.
- `benchmark-05-spplus-statistical-contour.md`: generated report records
  `Lpp delta = 0.00409694`, `Z delta = 0`, `pair mismatches = 0`,
  `node count mismatches = 0`, `mean chain contour delta = 0.171325`, and
  `rms chain contour delta = 0.308536`.
- `sacct.txt`: final jobs `416800`, `416802`, and `416804` completed with
  `ExitCode=0:0`.
