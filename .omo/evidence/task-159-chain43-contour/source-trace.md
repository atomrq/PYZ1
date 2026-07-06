# Task 159 source trace: benchmark-05 chain43 contour

Date: 2026-07-06

## Z1+ source state

- Local official supplemental tree:
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- Commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- Tree status: `main...origin/main`, clean

## Visible source checked

- `README.md` documents the public Z1+ installation package boundary, LAMMPS
  import helpers, Z1-formatted trajectories, and `Z1+SP.dat` converter use.
- `scripts/Z1+SP-to-data.pl`, `scripts/Z1+dat2dump.pl`, and
  `scripts/extract-single-chain-entanglements.pl` define public
  `Z1+SP.dat`/shortest-path helper semantics.
- `replacements/Z1+template.pl` records the public wrapper outputs including
  `Z1+SP.dat`.
- The supplemental tree contains no `module-Z1.f90`, `module-functions.f90`,
  or other public Fortran reducer core files.

## Slice classification

The benchmark-05 chain43 final contour placement is therefore
`oracle_residual_inference`. The public source confirms the SP+ output surface
and helper semantics, but not the hidden reducer placement algorithm. This slice
uses visible oracle output and current mismatch diagnostics to close the chain43
contour residual without weakening benchmark-04 SP+ parity or existing mismatch
diagnostics.

## Current RED target

- Existing pair coverage already asserts benchmark-05 chain43 SP+ pair:
  `(4.17,39,1)`.
- New focused assertion requires benchmark-05 chain43 contour to match
  `tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703/benchmark-05/spplus/Z1+SP.dat`
  within `0.001`.
