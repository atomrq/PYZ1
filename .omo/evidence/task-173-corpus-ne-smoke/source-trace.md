# Task 173 Corpus Ne Smoke

Classification: `source_contract`.

This slice extends the corpus statistical smoke report with source-backed
summary/Ne fields already parsed from public `mkmat/Z1plus-code` reference
logs. It does not run the native reducer and does not claim full reducer or
PPA+ parity.

## Source Boundary

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  - Git checkout: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
  - Public files used:
    - `benchmark-configurations/Z1+reference-results/log-benchmark-07.txt`
    - `benchmark-configurations/Z1+reference-results/log-benchmark-10.txt`
    - `benchmark-configurations/Z1+reference-results/log-benchmark-11.txt`
    - `benchmark-configurations/PPA+reference-results/log-benchmark-07.txt`
    - `benchmark-configurations/PPA+reference-results/log-benchmark-10.txt`
    - `benchmark-configurations/PPA+reference-results/log-benchmark-11.txt`

The visible logs contain `<Z>` and `Ne_MC` values in their results blocks. The
existing `pyz1.reference_logs` parser already reads these fields; this task only
threads selected values into the corpus statistical smoke report.

## Change

`pyz1-corpus-stat-smoke` now reports:

- `Z1+ <Z>`
- `Z1+ Ne_MC`
- `PPA+ Ne_MC`

The existing pass/mismatch status remains based on input/reference chain count
and mean-`N` alignment. These new columns are tracking fields for source-backed
statistical parity work, not acceptance of full native reducer or PPA+
scientific parity.

## RED/GREEN

- RED: `red-focused-416806.out`
  - Focused test failed because `CorpusSmokeRecord` did not yet expose
    `z1plus_mean_entanglements`.
- GREEN: `focused-green-416807.out`
  - Focused test passed after the report carried the selected reference-log
    summary/Ne fields.
- Final focused/static: `focused-static-416810.out`
  - Focused test, `ruff`, and `basedpyright` passed.
- Package smoke: `package-smoke-final-416811.out`
  - Editable install and `pyz1-corpus-stat-smoke` console-script report
    generation passed.

## Report Evidence

`corpus-stat-ne-smoke-final.md` records benchmark 07/10/11 as `passed` for the
existing input/reference baseline and adds:

- benchmark-07: `Z1+ <Z> = 16.48062`, `Z1+ Ne_MC = 21.47797`,
  `PPA+ Ne_MC = 16.19463`
- benchmark-10: `Z1+ <Z> = 4.98`, `Z1+ Ne_MC = 67.09988`,
  `PPA+ Ne_MC = 61.53768`
- benchmark-11: `Z1+ <Z> = 0.04789`, `Z1+ Ne_MC = 706953.05586`,
  `PPA+ Ne_MC = 7769.76838`
