# Task 151 Source Trace

Classification: `diagnostic_only`.

This slice adds benchmark-regression report diagnostics for per-chain shortest
path contour residuals. It does not change reducer output, parser semantics, or
package runtime dependencies.

Source references checked before the diagnostic update:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  at commit `c7219cd394b1295272ebfc098f2835c5c871e6ec`.
- `README.md` documents that Z1+ writes `Z1+SP.dat`, `Z1+PPA.dat`, and
  `Z1+initconfiguration.dat`, and that SP chain extraction exposes shortest
  path coordinates.
- `scripts/Z1+import-lammps.pl` defines the Z1+ summary header as
  `timestep chains N Ree Lpp Z app bpp Lpp2 NeCK NeMK NeCC NeMC`.
- `scripts/Z1+SP-to-data.pl` and
  `scripts/extract-single-chain-entanglements.pl` define the visible SP+
  output/report surface, but not the hidden reducer decision rule.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+` contains visible
  modules such as `module-output-formats.f90`, `module-PPA.f90`, and
  `module-CPPA.f90`, but not the private `module-Z1.f90` or
  `module-functions.f90` reducer core.

Rationale:

Task 150 closed benchmark-05 SP+ pair mismatches, node-count mismatches,
source residuals, and `Z` delta, while final geometry, `Lpp`, and summary
fields remained mismatched. Because the public reducer core is unavailable,
this slice adds a report-only residual surface that localizes contour-length
differences without changing scientific output or weakening existing mismatch
diagnostics.
