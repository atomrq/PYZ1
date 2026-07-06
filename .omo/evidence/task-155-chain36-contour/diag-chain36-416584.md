# Diagnostic job 416584

Diagnostic job `416584` printed actual/oracle chain10, chain15, and chain36 nodes before the reducer change.

Important values:

- chain10 contour delta: `0.764682135934605`
- chain15 contour delta: `0.035399115799458`
- chain36 contour delta: `2.447349428508309`

Chain36 actual nodes before the change:

```text
1 (-2.1544, 0.29857, -2.3599, 1.0, None)
2 (0.12440329427148612, 4.82230316070961, -1.8780315447134166, 6.62, (15, 2))
3 (-0.3698661681704578, 7.53058548110939, -4.567232636150933, 14.64, (10, 2))
4 (-2.057, 7.4316, -1.4907, 20.0, None)
```

Chain36 oracle nodes:

```text
1 (-2.1544, 0.29857, -2.3599, 1.0, None)
2 (-0.576168, 4.290357, -2.951135, 6.62, (15, 2))
3 (-0.613275, 6.503622, -4.137885, 14.64, (10, 2))
4 (-2.057, 7.4316, -1.4907, 20.0, None)
```

The original `diag-chain36-416584.out` was superseded/deleted by a later rsync cleanup; this artifact records the diagnostic values captured by the leader from Slurm output during the run.
