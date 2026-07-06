# Diagnostic job 416572

Diagnostic rerun job `416572` printed actual/oracle chain28, chain30, chain34, and chain48 nodes before the reducer change.

Important values:

- chain28 contour delta: `0.213972036767256`
- chain30 contour delta: `0.925336647397254`
- chain34 contour delta: `3.024391024782982`
- chain48 contour delta: `0.000000000000000`

Chain34 actual nodes before the change:

```text
1 (0.5177, -1.1585, 3.0416, 1.0, None)
2 (-0.94368, -0.4056, 2.3845, 4.45, (28, 1))
3 (1.3977, -0.97252, 1.129, 7.87, (48, 4))
4 (2.0047595206356807, 0.18826809459476807, 0.2762845805506694, 11.25, (30, 3))
5 (0.27605, -0.41013, 2.5432, 14.63, (28, 1))
6 (-4.1751, -2.111, 2.8343, 20.0, None)
```

Chain34 oracle nodes:

```text
1 (0.5177, -1.1585, 3.0416, 1.0, None)
2 (-0.283576, -0.844716, 1.86103, 4.45, (28, 1))
3 (1.776362, -0.353746, 0.876314, 7.87, (48, 4))
4 (1.913979, -0.434087, 1.246977, 11.25, (30, 3))
5 (-0.47818, -1.078247, 1.909975, 14.63, (28, 1))
6 (-4.1751, -2.111, 2.8343, 20.0, None)
```

The original `diag-chain34-rerun-416572.out` was superseded/deleted by a later rsync cleanup; this artifact records the diagnostic values captured by the leader from Slurm output during the run.
