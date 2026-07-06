# Task 157 source trace: benchmark-05 chain25 contour

Date: 2026-07-06

## Z1+ source state

- Local official supplemental tree:
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- Commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- Tree status: `main...origin/main`, clean

## Visible source checked

- `README.md` documents LAMMPS data/dump import, sheared/triclinic handling,
  Z1-formatted trajectory generation, `Z1+SP.dat`/`Z1+PPA.dat` converter use,
  and shortest-path export helpers.
- `scripts/Z1+SP-to-data.pl` parses `Z1+SP.dat` rows as
  `x y z SPpos entangled entmol entbead`, matching the current pyz1 SP+
  7-column reader/writer contract.
- `scripts/Z1+dat2dump.pl` converts `Z1+SP.dat`, `Z1+PPA.dat`, and
  `Z1+initconfiguration.dat` into LAMMPS dump format.

## Slice classification

The public supplemental tree does not include the hidden Z1 reducer core
(`module-Z1.f90` / final shortest-path reducer implementation). The current
benchmark-05 chain25 contour slice therefore remains
`oracle_residual_inference`: target placement is inferred from visible Z1+ SP+
oracle output and current mismatch diagnostics, while preserving benchmark-04
SP+ parity and existing mismatch diagnostics.

## Current RED target

- Existing pair coverage already asserts benchmark-05 chain25 SP+ pairs:
  `(11.67,3,2)` and `(15.83,40,2)`.
- New focused assertion requires benchmark-05 chain25 contour to match
  `tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703/benchmark-05/spplus/Z1+SP.dat`
  within `0.001`.
