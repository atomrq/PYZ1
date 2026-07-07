# Task 182 source trace: regression Ne coil deltas

Classification: `source_contract`.

This slice adds structured `Ne_CC` and `Ne_MC` delta fields to the
default/SP+/selfZ benchmark regression report. It does not change reducer
runtime behavior, strict `status`, `statistical status`, or mismatch
diagnostics.

Source trace read before implementation:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+README.txt`
  documents `Z1+summary.dat` column 12 as the classical coil Ne estimator
  `Ne_CC` and column 13 as the modified coil Ne estimator `Ne_MC`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  at Git commit `c7219cd394b1295272ebfc098f2835c5c871e6ec`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/scripts/Z1+import-lammps.pl`
  emits the source-backed summary/statistical header
  `timestep chains N Ree Lpp Z app bpp Lpp2 NeCK NeMK NeCC NeMC`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/scripts/Z1+SP-to-data.pl`
  documents `Z1+SP.dat` as the public shortest-path surface used with the
  source-backed summary outputs.

Rationale:

- The project target is statistical/ensemble SP/SP+ parity, and `Ne` is one of
  the explicit long-term parity surfaces.
- PPA regression already exposes `Lpp`, `Ne classical coil`, and
  `Ne modified coil` deltas as structured fields. Default/SP+/selfZ regression
  previously only exposed `Lpp delta`, `Z delta`, and textual summary mismatch
  details.
- Adding structured `Ne_CC`/`Ne_MC` deltas makes summary/Ne residuals
  searchable and trendable without weakening strict mismatch details.

Remote gate:

- RED `416886`: focused pytest failed for the intended missing-field reason.
- GREEN `416887`: focused pytest passed.
- Static `416888`: `ruff` and `basedpyright` passed.
- Package smoke `416890`: editable install plus
  `pyz1-benchmark-regression --contact-relaxation` generated the benchmark-05
  SP+ report with `Ne classical coil delta = 0.0122531` and
  `Ne modified coil delta = 0.613306`.
