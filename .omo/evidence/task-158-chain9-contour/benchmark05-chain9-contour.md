# Task 158 benchmark-05 chain9 contour evidence

Date: 2026-07-06

## RED

Focused RED job `416605` failed for the intended assertion:

- actual chain9 contour: `10.661034261796697`
- oracle chain9 contour: `9.396915022094282`
- delta: `1.2641192397024152`

## Diagnostic geometry

Diagnostic job `416606` captured pre-fix chain9 and chain27 geometry. Chain9
had the correct pair sequence but an oracle-divergent middle-node position:

```text
actual chain9 contour=10.661034261796697 nodes=3
  node=1 source=1 pos=(-3.746500,1.138700,0.534970) pair=None
  node=2 source=6.5 pos=(-5.012500,-0.935600,2.987500) pair=(27, 1)
  node=3 source=20 pos=(-0.721590,-2.599100,8.535700) pair=None
  segments=3.452590,7.208444
oracle chain9 contour=9.396915022094282 nodes=3
  node=1 source=1 pos=(-3.746500,1.138700,0.534970) pair=None
  node=2 source=6.5 pos=(-3.476827,0.201166,1.775736) pair=(27, 1)
  node=3 source=20 pos=(-0.721590,-2.599100,8.535700) pair=None
  segments=1.578352,7.818563
```

Post-fix diagnostic job `416612` shows chain9 and chain27 contours match the
oracle-local geometry:

```text
actual chain9 contour=9.396915022094282 nodes=3
oracle chain9 contour=9.396915022094282 nodes=3
actual chain27 contour=9.040221112557212 nodes=4
oracle chain27 contour=9.040221112557212 nodes=4
```

## GREEN and gate

- Focused GREEN job `416607`: 4 passed in `123.17s`
- Static job `416609`: ruff and basedpyright passed
- Package smoke job `416610`: 1 passed in `10.41s`
- Final regression job `416611` passed
- Invalid setup job `416608` is retained as non-gate evidence: it failed
  because the ad hoc report script imported a nonexistent helper.

Final regression summary:

- benchmark-04 SP+ `passed`
- benchmark-05 SP+ remains `mismatch`
- benchmark-05 pair mismatches `0`
- benchmark-05 node-count mismatches `0`
- benchmark-05 source residual details `none`
- benchmark-05 `Z` delta `0`
- benchmark-05 `Lpp` delta `0.289635`
- benchmark-05 summary mismatches `6`
- benchmark-05 max chain-contour delta now `1.25809` on chain43
