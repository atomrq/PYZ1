# Task 156 benchmark-05 chain27 contour evidence

## RED

Corrected RED job `416590` failed for the intended focused assertion:

- actual chain27 contour: `11.280489835577272`
- oracle chain27 contour: `9.040221112557212`
- delta: `2.24026872302006`

Setup job `416589` is invalid RED evidence because the Slurm script lacked
`PYTHONPATH` and failed during import collection with `ModuleNotFoundError:
No module named 'pyz1'`.

## Diagnostic

Corrected diagnostic job `416592` completed with exit code `0:0`. Setup job
`416591` is invalid diagnostic evidence because the temporary diagnostic script
used `zip(..., strict=True)` on a shifted sequence.

Key diagnostic rows captured from job `416592`:

- chain9 actual contour `10.661034261796697`; oracle contour
  `9.396915022094284`; delta `1.264119239702413`
- chain19 actual contour `12.895460832680660`; oracle contour
  `12.354529960133098`; delta `0.540930872547563`
- chain27 actual contour `11.280489835577271`; oracle contour
  `9.040221112557212`; delta `2.240268723020058`

Chain27 actual nodes before GREEN:

```text
node=1 source=1    pos=(-2.756300,0.018939,0.541860) pair=None
node=2 source=2.43 pos=(-5.456385,-0.630829,2.925476) pair=(9, 2)
node=3 source=6.71 pos=(-4.672226,0.314894,2.717466) pair=(19, 1)
node=4 source=20   pos=(-5.942100,-0.755290,8.872000) pair=None
segments=3.659820,1.246020,6.374650
```

Chain27 oracle nodes:

```text
node=1 source=1    pos=(-2.756300,0.018939,0.541860) pair=None
node=2 source=2.43 pos=(-3.466043,0.192181,1.801850) pair=(9, 2)
node=3 source=6.71 pos=(-4.161573,0.164689,3.088986) pair=(19, 1)
node=4 source=20   pos=(-5.942100,-0.755290,8.872000) pair=None
segments=1.456476,1.463297,6.120448
```

## GREEN and final gate

- Focused GREEN job `416593`: 4 passed in `122.97s`
  - chain9 pair sequence
  - chain27 contour
  - chain10 pair
  - chain36 contour
- Static job `416595`: `ruff check src tests` passed; `basedpyright` reported
  `0 errors, 0 warnings, 0 notes`
- Package smoke job `416596`: 1 passed in `10.77s`
- Final regression retry job `416597`: completed with exit code `0:0`
  - benchmark-04 SP+ `passed`
  - benchmark-05 SP+ remains `mismatch`
  - benchmark-05 pair mismatches `0`
  - benchmark-05 node-count mismatches `0`
  - benchmark-05 source residual details `none`
  - benchmark-05 `Z` delta `0`
  - benchmark-05 `Lpp` delta `0.349454`
  - benchmark-05 max chain-contour delta `1.7268235104124283` on chain25

Regression setup job `416594` is invalid gate evidence because the temporary
reporting script used `pair_mismatches` instead of `pairing_mismatches` after
successfully writing the markdown report. Retry job `416597` is the accepted
regression gate.
