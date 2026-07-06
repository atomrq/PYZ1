# Task 154 source trace: benchmark-05 SP+ chain34 contour

Classification: `oracle_residual_inference`.

Visible source checked before reducer changes:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`, commit `c7219cd394b1295272ebfc098f2835c5c871e6ec`.
- Visible helper scripts include `scripts/Z1+SP-to-data.pl` and `scripts/Z1+dat2dump.pl`, confirming the SP+ output/report surface remains script-visible.
- The hidden reducer core files `module-Z1.f90` and `module-functions.f90` remain unavailable in the public supplemental repository, so chain34 final geometry/contour placement cannot be copied from source and is inferred from oracle residuals.

Task boundary:

- Preserve benchmark-04 SP+ passed.
- Preserve existing benchmark-05 pair sequence, node-count, source, and Z diagnostics.
- Close the largest remaining benchmark-05 SP+ chain contour residual localized to chain34 after task153.
