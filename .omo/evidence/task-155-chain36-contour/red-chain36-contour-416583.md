# RED job 416583

Focused pytest:

`tests/test_spplus_regression.py::test_reduce_snapshot_when_benchmark05_chain36_contour_matches_oracle`

Result: expected RED failure, Slurm `FAILED`, `ExitCode=1:0`, elapsed `00:00:32`.

Observed assertion:

- `actual_contour = 12.446813094093779`
- `expected_contour = 9.99946366558547`
- `abs(actual_contour - expected_contour) = 2.447349428508309`
- threshold: `< 0.001`

The original `red-chain36-contour-416583.out` was superseded/deleted by a later rsync cleanup; this artifact records the exact failure captured by the leader from Slurm output during the run.
