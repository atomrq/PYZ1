# Task 153 Benchmark-05 Chain48 Contour

Focused RED:

- Slurm job: `416546`
- Assertion:
  `test_reduce_snapshot_when_benchmark05_chain48_contour_matches_oracle`
- Failure:
  `abs((14.476483146132505 - 11.383422262882965)) = 3.0930608832495405`

Diagnostic:

- Slurm job: `416547`
- Actual chain48 contour before the fix: `14.476483146132505`
- Oracle chain48 contour: `11.383422262882965`
- Oracle-local chain48 positions:
  `(2.834512, 0.728049, -2.656617)`,
  `(4.598198, -1.270162, -2.350507)`,
  `(2.190468, -0.626553, 0.517701)`,
  `(1.776072, -0.354536, 0.877638)`.

Focused GREEN:

- Slurm job: `416549`
- Tests:
  - `test_reduce_snapshot_when_benchmark05_chain48_contour_matches_oracle`
  - `test_reduce_snapshot_when_benchmark05_chain48_matches_oracle_pairs`
- Result: `2 passed in 61.50s`

Final gate:

- final regression job `416558`: `COMPLETED`, `ExitCode=0:0`
- static rerun job `416561`: `COMPLETED`, `ExitCode=0:0`
- package smoke job `416560`: `COMPLETED`, `ExitCode=0:0`

Final benchmark report:

- benchmark-04 SP+: `passed`
- benchmark-05 SP+: `mismatch`
- benchmark-05 pair mismatches: `0`
- benchmark-05 node count mismatches: `0`
- benchmark-05 source residual details: `none`
- benchmark-05 `Z` delta: `0`
- benchmark-05 `Lpp` delta: `0.503694`
- benchmark-05 summary field mismatches: `6`
- benchmark-05 max chain-contour delta: `3.02439` on chain34

Task153 closes the chain48 contour residual and leaves benchmark-05 open on
downstream geometry, chain34 contour residual, `Lpp`, and summary parity.
