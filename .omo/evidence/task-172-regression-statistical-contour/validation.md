# Task 172 Validation

Remote run root:
`/public/home/jxm/pyz1-cleanroom-runs/task-172-regression-statistical-contour`.

## Passing Gates

- Focused GREEN: job `416800`, `COMPLETED`, `ExitCode=0:0`
  - `tests/test_spplus_regression.py::test_write_benchmark_report_when_contact_relaxation_measures_guarded_spplus`
  - Imported current run-root code with `PYTHONPATH=$PWD/src`
- Static: job `416802`, `COMPLETED`, `ExitCode=0:0`
  - `ruff check src/pyz1/regression.py tests/test_spplus_regression.py`
  - `basedpyright src/pyz1/regression.py tests/test_spplus_regression.py`
- Package/CLI smoke: job `416804`, `COMPLETED`, `ExitCode=0:0`
  - Editable install with Tsinghua PyPI mirror
  - Console-script `pyz1-benchmark-regression` generated the benchmark-05 SP+
    contact-relaxation report and the report contains the new mean/RMS contour
    columns

## Superseded Or Invalid Gates

- `416797`: invalid RED setup; missing cluster-visible `PYZ1_SOURCE_Z1`.
- `416798`: correct RED after source path fix; failed for missing
  `mean_chain_contour_delta`.
- `416799`: invalid GREEN setup; Slurm imported an older editable install from
  task170 instead of current run-root code.
- `416803`: package install succeeded, but shell PATH did not include the
  console script; `416804` reran with the script's absolute env path.
