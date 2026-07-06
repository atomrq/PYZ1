# task-143 source trace

Classification: `source_contract`.

Local source mirrors:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  - Git commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
  - Upstream: `https://github.com/mkmat/Z1plus-code`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
  - Existing Mendeley/install-package mirror and oracle binary source.

Visible contract used in this slice:

- `Z1plus-code/scripts/Z1+import-lammps.pl`, lines 436-441 and 510-515:
  sheared LAMMPS dump import computes the x lower bound as
  `xlobound - min(0.0, xy)` and the x upper bound as
  `xhibound - max(0.0, xy)`.
- The same file labels the sign change as a 2025-10-05 replacement for the old
  `+ min(...)` rule.
- `Z1plus-code/scripts/extract_backbone.pl`, lines 280-284, independently
  applies the same negative-`xy` correction for triclinic extraction.

pyz1 change:

- `src/pyz1/lammps_dump_box.py` now uses the visible Z1plus-code sign rule for
  negative `xy` triclinic dump bounds.
- `tests/test_lammps_dump_import.py` adds a focused assertion for a negative-`xy`
  dump with scaled coordinates. The assertion fails on the old rule with
  `box.x == 12.0` and passes with the source-backed rule at `box.x == 8.0`.

Remote gate:

- Run root:
  `/public/home/jxm/codex_runs/z1-task143-z1plus-code-io-contract-20260706-162453`
- RED: Slurm job `416442`, expected failure.
- GREEN: Slurm jobs `416443` and final-path rerun `416450`, passed.
- Non-SP pytest shards: final Slurm array `416451`, passed.
- Initial static job `416445` was superseded because it scanned generated
  `.omo/evidence` scripts in the synced run root.
- Package smoke: final Slurm job `416453`, passed.
- Scoped static final job `416452`, passed with
  `ruff check src tests` and `basedpyright`.
