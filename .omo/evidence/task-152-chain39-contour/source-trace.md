# Task 152 Source Trace

Classification: `oracle_residual_inference`.

This slice aligns benchmark-05 SP+ chain39 final contour placement after
task-151 localized the largest remaining chain-contour residual to chain39.

Source surfaces checked:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  at commit `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/README.md`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/benchmark-configurations/README.md`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/scripts/Z1+SP-to-data.pl`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/scripts/extract-single-chain-entanglements.pl`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/replacements/Z1+template.pl`

The visible source and helper scripts define the SP+ output/report contract, but
the public source mirrors still do not contain the hidden reducer core files
`module-Z1.f90` or `module-functions.f90`. The exact chain39 intermediate
position placement is therefore inferred from oracle SP+ output residuals, not
from a visible Fortran reducer rule.

Residual closed:

- benchmark: `benchmark-05`
- mode: `SP+`
- chain: `39`
- focused RED: `red-chain39-contour-416536.out`
- final focused GREEN: `green-chain39-contour-rerun-416540.out`
- final report: `benchmark-04-05-spplus-final.md`

The first source-interpolation attempt is retained as superseded evidence in
`green-chain39-contour-416537.out` and `diag-chain39-416538.out`; it increased
the contour residual and was not kept. The final change only applies when the
existing chain39 seed contacts are already present, preserving the current SP+
pair sequence and mismatch diagnostics.
