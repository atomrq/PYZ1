# Task 152 Benchmark-05 Chain39 Contour

Focused RED:

- Slurm job: `416536`
- Assertion:
  `test_reduce_snapshot_when_benchmark05_chain39_contour_matches_oracle`
- Failure:
  `abs((13.85717522059603 - 4.403016908143882)) = 9.454158312452147`

Superseded attempt:

- Slurm job: `416537`
- Source-interpolation placement kept the pair test passing but worsened the
  contour residual to `9.500307853188534`.
- Diagnostic job `416538` shows the oracle chain39 positions:
  `(1.733761, 0.532431, -0.221663)`,
  `(1.687822, 0.235781, -0.999334)`,
  `(1.673239, 0.19047, -1.130965)`,
  `(-0.103755, 1.513189, -1.746117)`.

Focused GREEN:

- Slurm job: `416540`
- Tests:
  - `test_reduce_snapshot_when_benchmark05_chain39_contour_matches_oracle`
  - `test_reduce_snapshot_when_benchmark05_chain39_matches_oracle_pairs`
- Result: `2 passed in 61.37s`

Final gate:

- final regression job `416541`: `COMPLETED`, `ExitCode=0:0`
- static rerun job `416544`: `COMPLETED`, `ExitCode=0:0`
- package smoke job `416543`: `COMPLETED`, `ExitCode=0:0`

Final benchmark report:

- benchmark-04 SP+: `passed`
- benchmark-05 SP+: `mismatch`
- benchmark-05 pair mismatches: `0`
- benchmark-05 node count mismatches: `0`
- benchmark-05 source residual details: `none`
- benchmark-05 `Z` delta: `0`
- benchmark-05 `Lpp` delta: `0.565555`
- benchmark-05 summary field mismatches: `6`
- benchmark-05 max chain-contour delta: `3.09306` on chain48

Task152 closes the chain39 contour residual and leaves benchmark-05 open on
downstream geometry, chain48 contour residual, `Lpp`, and summary parity.
