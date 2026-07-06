# Task 159: Benchmark-05 SP+ Chain43 Contour Placement

Classification: `oracle_residual_inference`.

The public `mkmat/Z1plus-code` supplemental repository does not include the
hidden Z1 reducer core (`module-Z1.f90` / `module-functions.f90`). This slice
therefore keeps the existing visible source contract unchanged and uses the
Z1+ oracle SP+ output to close one clean-room reducer residual.

## RED

Remote Slurm job `416613` ran the focused assertion:

```text
tests/test_spplus_regression.py::test_reduce_snapshot_when_benchmark05_chain43_contour_matches_oracle
```

It failed for the intended reason:

```text
actual contour = 11.931670979654012
oracle contour = 10.673584460117015
delta = 1.258086519536997
```

## Diagnostic

Pre-fix diagnostic job `416614` showed chain39 was already identical to the
oracle contour and pairing, while chain43 retained the correct `(39, 1)` pair
at source bead `4.17` but placed the retained node at the wrong final
position:

```text
actual chain43 node2 = source 4.17 pos=(3.142000,0.092507,-0.284930) pair=(39, 1)
oracle chain43 node2 = source 4.17 pos=(1.730048,0.536360,-0.222815) pair=(39, 1)
```

Post-fix diagnostic job `416617` shows chain43 now matches the oracle contour,
node position, and pair annotation:

```text
actual chain43 contour=10.673584460117015
oracle chain43 contour=10.673584460117015
node2 source=4.17 pos=(1.730048,0.536360,-0.222815) pair=(39, 1)
segments=2.027877,8.645708
```

## GREEN And Gate

- Focused GREEN job `416615`: `4 passed in 124.16s`.
- Final regression job `416616`:
  - benchmark-04 SP+ `passed`
  - benchmark-05 SP+ remains `mismatch`
  - pair mismatches `0`
  - node-count mismatches `0`
  - source residual details `none`
  - `Z` delta `0`
  - `Lpp` delta `0.264473`
  - summary mismatches `6`
  - max chain-contour delta now `1.0894` on chain22
- Static job `416618`: `ruff check src tests` passed and `basedpyright`
  reported `0 errors, 0 warnings, 0 notes`.
- Package smoke job `416619`: `1 passed in 10.45s`.

## Evidence

- `source-trace.md`
- `red-chain43-contour-416613.out`
- `diag-chain43-contour-416614.out`
- `green-chain43-contour-416615.out`
- `benchmark-04-05-spplus-final.md`
- `diag-chain43-postfix-416617.out`
- `static-416618.out`
- `package-smoke-416619.out`
- `sacct.txt`

Next reducer parity slice should start from benchmark-05 SP+ chain22 final
geometry and contour placement while preserving benchmark-04 SP+ passed and the
existing mismatch diagnostics.
