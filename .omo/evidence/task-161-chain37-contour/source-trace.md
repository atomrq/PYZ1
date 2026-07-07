# Task 161 source trace: benchmark-05 chain37 contour

Date: 2026-07-07

## Z1+ source state

- Local official supplemental tree:
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- Commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- Tree status: `main...origin/main`, clean

## Visible source checked

- `README.md` documents the public Z1+ installation package boundary, LAMMPS
  import helpers, Z1-formatted trajectories, and `Z1+SP.dat` converter use.
- `scripts/Z1+SP-to-data.pl`, `scripts/Z1+dat2dump.pl`,
  `scripts/Z1+dump.pl`, `scripts/Z1+export.pl`,
  `scripts/Z1+import-lammps.pl`, and
  `scripts/extract-single-chain-entanglements.pl` are the visible helper and
  I/O surfaces for SP/SP+ output, trajectory conversion, export, and LAMMPS
  import behavior.
- `replacements/Z1+template.pl` records the public wrapper outputs including
  `Z1+SP.dat`.
- The supplemental tree contains no `module-Z1.f90`, `module-functions.f90`,
  or other public Fortran reducer core files.

## Slice classification

The benchmark-05 chain37 final contour placement is
`oracle_residual_inference`. The public source confirms the SP+ output surface
and helper semantics, but not the hidden reducer placement algorithm. This
slice uses visible oracle output and current mismatch diagnostics to target the
largest remaining benchmark-05 SP+ chain-contour residual after task160.

## Current RED target

- Existing pair coverage already asserts benchmark-05 chain37 SP+ pairs:
  `(4.15,11,2)`, `(7.27,4,2)`, and `(10.38,6,2)`.
- New focused assertion requires benchmark-05 chain37 contour to match
  `tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703/benchmark-05/spplus/Z1+SP.dat`
  within `0.001`.
