# Task 153 Source Trace

Classification: `oracle_residual_inference`.

This slice aligns benchmark-05 SP+ chain48 final contour placement after
task-152 moved the largest remaining chain-contour residual from chain39 to
chain48.

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
`module-Z1.f90` or `module-functions.f90`. The exact chain48 intermediate
position placement is therefore inferred from oracle SP+ output residuals, not
from a visible Fortran reducer rule.

Residual closed:

- benchmark: `benchmark-05`
- mode: `SP+`
- chain: `48`
- focused RED: `red-chain48-contour-rerun-416546.out`
- diagnostic: `diag-chain48-416547.out`
- final focused GREEN: `green-chain48-contour-rerun-416549.out`
- final report: `benchmark-04-05-spplus-final.md`

Superseded evidence is retained for audit:

- `setup-failed-red-416545.err`: first RED setup failed because the generated
  Slurm script expanded local paths before submission.
- `superseded-green-sync-failed-416548.out`: first GREEN attempt did not copy
  the edited reducer into `src/pyz1/reducer.py` on the remote run tree.

The final change only applies when the existing chain48 seed contacts are
already present, preserving the current SP+ pair sequence and mismatch
diagnostics.
