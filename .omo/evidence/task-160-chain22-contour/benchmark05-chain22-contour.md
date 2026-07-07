# Task 160: Benchmark-05 SP+ Chain22 Contour Placement

Classification: `oracle_residual_inference`.

The public `mkmat/Z1plus-code` supplemental repository does not include the
hidden Z1 reducer core (`module-Z1.f90` / `module-functions.f90`). This slice
therefore keeps the existing visible source contract unchanged and uses the
Z1+ oracle SP+ output to close one clean-room reducer residual.

## RED

Remote Slurm job `416664` ran the focused assertion:

```text
tests/test_spplus_regression.py::test_reduce_snapshot_when_benchmark05_chain22_contour_matches_oracle
```

It failed for the intended reason:

```text
actual contour = 13.584342660879411
oracle contour = 12.494943295278627
delta = 1.0893993656007837
```

## Diagnostic

Pre-fix diagnostic job `416665` showed chain25 already matched the oracle
contour and pairing, while chain22 retained the correct `(25, 2)` pair at
source bead `4.84` but placed the retained node at the wrong final position:

```text
actual chain22 node2 = source 4.84 pos=(-5.341205,-2.714345,1.105042) pair=(25, 2)
oracle chain22 node2 = source 4.84 pos=(-3.090765,-2.209248,0.860356) pair=(25, 2)
```

Post-fix diagnostic job `416667` shows chain22 now matches the oracle contour,
node position, and pair annotation:

```text
actual chain22 contour=12.494943295278627
oracle chain22 contour=12.494943295278627
node2 source=4.84 pos=(-3.090765,-2.209248,0.860356) pair=(25, 2)
segments=2.261512,10.233431
```

## GREEN And Gate

- Focused GREEN job `416666`: `4 passed in 123.54s`.
- Post-fix diagnostic job `416667`: completed with `ExitCode=0:0`.
- Final regression job `416674`:
  - benchmark-04 SP+ `passed`
  - benchmark-05 SP+ remains `mismatch`
  - pair mismatches `0`
  - node-count mismatches `0`
  - source residual details `none`
  - `Z` delta `0`
  - `Lpp` delta `0.242685`
  - summary mismatches `6`
  - max chain-contour delta now `1.0324` on chain37
- Static job `416673`: `ruff check src tests` passed and `basedpyright`
  reported `0 errors, 0 warnings, 0 notes`.
- Package smoke job `416670`: `1 passed in 10.49s`.

Invalid/superseded setup jobs are retained in `sacct.txt`: regression jobs
`416668` and `416672` wrote reports but failed in ad hoc summary scripts, and
static jobs `416669` and `416671` used an incorrect basedpyright interpreter
configuration.

## Evidence

- `source-trace.md`
- `red-chain22-contour-416664.out`
- `diag-chain22-contour-416665.out`
- `green-chain22-contour-416666.out`
- `diag-chain22-postfix-416667.out`
- `benchmark-04-05-spplus-final.md`
- `final-regression-rerun2-416674.out`
- `static-rerun2-416673.out`
- `package-smoke-416670.out`
- `sacct.txt`

Next reducer parity slice should start from benchmark-05 SP+ chain37 final
geometry and contour placement while preserving benchmark-04 SP+ passed and the
existing mismatch diagnostics.
