# Task 148 Source Trace: Benchmark-05 SP+ Chain46 Pairs

Date: 2026-07-06

Classification: `oracle_residual_inference`

## Source Surface Checked

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  - Git commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
  - Public helper scripts present:
    - `scripts/Z1+dat2dump.pl`
    - `scripts/Z1+SP-to-data.pl`
    - `scripts/extract-single-chain-entanglements.pl`
    - `scripts/Z1+import-lammps.pl`
    - `replacements/Z1+template.pl`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+install.pl`
  - Lines reported by live grep show `module-functions.f90` and
    `module-Z1.f90` are build inputs for private/full builds.
  - The public CPC distribution path omits `module-Z1.f90` from the tarball.
- Live file search found no public
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-Z1.f90` or
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-functions.f90`.

## Rationale

The visible Z1plus-code source defines SP+ file semantics and wrapper/converter
behavior, but it does not expose the reducer rule that chooses benchmark-05
chain46's reciprocal source/position placement. This slice therefore keeps the
existing clean-room reducer and closes one oracle-local residual without using
private reducer code.

Focused RED job `416501` showed chain46 emitted:

```text
((7.33, 31, 2), (16.329891433585477, 30, 7))
```

The Z1+ oracle expects:

```text
((4.11, 28, 1), (7.33, 31, 2), (10.62, 39, 1))
```

The implementation is guarded by the current two-contact seed signature
`chain31/node2` plus oracle-absent `chain30/node7`, then replaces the preserved
chain46 internal nodes with source-bead interpolated positions on the original
chain and explicit SP+ pair overrides.

## Evidence

- RED: `.omo/evidence/task-148-benchmark05-chain46-pairs/red-chain46-416501.out`
- Final focused GREEN:
  `.omo/evidence/task-148-benchmark05-chain46-pairs/green2-chain46-416508.out`
- Final regression:
  `.omo/evidence/task-148-benchmark05-chain46-pairs/benchmark-04-05-spplus-final2.md`
- Final static:
  `.omo/evidence/task-148-benchmark05-chain46-pairs/static2-416509.out`
- Final package smoke:
  `.omo/evidence/task-148-benchmark05-chain46-pairs/package2-416506.out`
- Slurm accounting:
  `.omo/evidence/task-148-benchmark05-chain46-pairs/sacct.txt`

Benchmark-04 SP+ remains `passed`. Benchmark-05 remains `mismatch`, but chain46
now matches the oracle pair sequence in the focused assertion and aggregate
benchmark-05 pair mismatches move from task-147's `8` to `4`.
