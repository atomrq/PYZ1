# RED job 416570

Focused pytest:

`tests/test_spplus_regression.py::test_reduce_snapshot_when_benchmark05_chain34_contour_matches_oracle`

Result: expected RED failure, Slurm `FAILED`, `ExitCode=1:0`, elapsed `00:00:32`.

Observed assertion:

- `actual_contour = 13.736895697826398`
- `expected_contour = 10.712504673043416`
- `abs(actual_contour - expected_contour) = 3.0243910247829824`
- threshold: `< 0.001`

The original `red-chain34-contour-416570.out` was superseded/deleted by a later rsync cleanup; this artifact records the exact failure captured by the leader from Slurm output during the run.
