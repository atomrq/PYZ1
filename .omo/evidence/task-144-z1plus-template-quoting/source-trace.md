# Task 144 Source Trace: Z1plus-code Template Path Quoting

Classification: `source_contract`.

Local source mirrors:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`

`mkmat/Z1plus-code` checkout:

- `c7219cd394b1295272ebfc098f2835c5c871e6ec`

Source-backed contract:

- `replacements/Z1+template.pl` lines 3-4 records the 2024-07-11 update:
  the wrapper allows blanks in directory and file names.
- `replacements/Z1+template.pl` lines 107-108 quote
  `$installation_directory/Z1+import-lammps.pl` and `-data="$configfile"`.
- `replacements/Z1+template.pl` lines 113 and 118 quote the `-dump` and `-xml`
  converter paths and config filenames.
- `replacements/Z1+template.pl` line 123 quotes the fallback
  `cp "$working_directory/$configfile" config.Z1` path.
- `replacements/Z1+template.pl` line 257 quotes `"$code"` for logged runs.
- `replacements/Z1+template.pl` line 273 quotes
  `$installation_directory/Z1+rearrange.pl`.

Observed local source mismatch:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+` lines 106-123 and
  272 still use the older unquoted forms.

pyz1 implementation:

- `src/pyz1/oracle_install.py` stages the oracle wrapper and applies the
  official quoting replacements while preserving the package rule that
  `Z1+.ex` is oracle tooling only, not a package runtime dependency.
- `src/pyz1/oracle.py` keeps the public oracle API and delegates staging to the
  source-backed install helper.

Remote evidence:

- Run root:
  `/public/home/jxm/codex_runs/z1-task144-z1plus-template-quoting-20260706`
- RED Slurm job `416460`: old staged wrapper plus the new focused assertion
  failed for the missing quoted `Z1+import-lammps.pl` command.
- GREEN Slurm job `416468`: focused assertion passed on the patched wrapper
  staging path.
- Static Slurm job `416467`: `ruff check src tests` and `basedpyright` passed.
- Package smoke Slurm job `416469`: `tests/test_package_integration_smoke.py`
  passed.

Open scope:

- This slice is an oracle tooling/source-contract hardening change. It does not
  change reducer behavior and therefore has no benchmark-05 SP+ delta.
