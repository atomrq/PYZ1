# Task 157 benchmark-05 chain25 contour evidence

## RED

RED job `416599` failed for the intended focused assertion:

- actual chain25 contour: `12.304652166799551`
- oracle chain25 contour: `10.577828656387123`
- delta: `1.7268235104124283`

## Diagnostic

Diagnostic job `416600` completed with exit code `0:0`.

Key diagnostic rows:

- chain3 actual contour `10.860486087341101`; oracle contour
  `9.873772787516396`; delta `0.986713299824705`
- chain22 actual contour `13.584342660879411`; oracle contour
  `12.494943295278627`; delta `1.089399365600784`
- chain25 actual contour `12.304652166799551`; oracle contour
  `10.577828656387123`; delta `1.726823510412428`
- chain40 actual contour `11.780043943064413`; oracle contour
  `11.192862609428554`; delta `0.587181333635860`

Chain25 actual nodes before GREEN:

```text
node=1 source=1     pos=(-2.222200,-3.331100,-3.410400) pair=None
node=2 source=11.67 pos=(-5.582813,-2.348862,1.425370) pair=(3, 2)
node=3 source=15.83 pos=(-2.221865,-2.475626,0.175185) pair=(40, 2)
node=4 source=20    pos=(-2.125800,-3.182500,2.827200) pair=None
segments=5.970191,3.588176,2.746285
```

Chain25 oracle nodes:

```text
node=1 source=1     pos=(-2.222200,-3.331100,-3.410400) pair=None
node=2 source=11.67 pos=(-4.769255,-1.987048,1.422242) pair=(3, 2)
node=3 source=15.83 pos=(-2.356595,-2.305635,0.617153) pair=(40, 2)
node=4 source=20    pos=(-2.125800,-3.182500,2.827200) pair=None
segments=5.625691,2.563317,2.388821
```

## GREEN and final gate

- Focused GREEN job `416601`: 4 passed in `123.35s`
  - chain25 pair40 source
  - chain25 contour
  - chain22 pair25 source
  - chain27 contour
- Static job `416603`: `ruff check src tests` passed; `basedpyright` reported
  `0 errors, 0 warnings, 0 notes`
- Package smoke job `416604`: 1 passed in `10.53s`
- Final regression job `416602`: completed with exit code `0:0`
  - benchmark-04 SP+ `passed`
  - benchmark-05 SP+ remains `mismatch`
  - benchmark-05 pair mismatches `0`
  - benchmark-05 node-count mismatches `0`
  - benchmark-05 source residual details `none`
  - benchmark-05 `Z` delta `0`
  - benchmark-05 `Lpp` delta `0.314917`
  - benchmark-05 max chain-contour delta `1.2641192397024152` on chain9
