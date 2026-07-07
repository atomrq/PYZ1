# Task 181 source trace: chain-contour residual median

Classification: `diagnostic_only`.

This slice adds a benchmark regression report field for the nearest-rank median
of finite chain-contour residual deltas. It does not change reducer runtime
behavior, strict `status`, `statistical status`, or any mismatch diagnostic.

Source trace read before implementation:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  at Git commit `c7219cd394b1295272ebfc098f2835c5c871e6ec`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/benchmark-configurations/README.md`
  documents that the public benchmark configurations reproduce Z1+ and PPA+
  reference results through the visible wrapper.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/scripts/Z1+SP-to-data.pl`
  and `scripts/extract-single-chain-entanglements.pl` document that
  `Z1+SP.dat` is the public shortest-path output surface used by downstream
  helper scripts.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/scripts/Z1+import-lammps.pl`
  exposes the public summary/statistical field names
  `timestep chains N Ree Lpp Z app bpp Lpp2 NeCK NeMK NeCC NeMC`.

Rationale:

- The project target is statistical/ensemble SP/SP+ parity, not exact final
  geometry equality for every chain.
- Existing report fields already expose max, mean, RMS, count/fraction, and
  p95 chain-contour residuals.
- The new median field separates the typical residual level from the p95/max
  tail while preserving per-chain residual details for diagnostics.
- Because the public Z1 reducer core remains unavailable, this report-surface
  field is evidence support for future reducer work, not a source-backed
  scientific formula or an oracle-coordinate shim.

Remote gate:

- RED `416869`: focused pytest failed for the intended missing-field reason.
- GREEN `416879`: focused pytest passed.
- Static `416880`: `ruff` and `basedpyright` passed.
- Package smoke `416884`: editable install plus
  `pyz1-benchmark-regression --contact-relaxation` generated the benchmark-05
  SP+ report with `chain contour residual median delta = 0.147581`.
