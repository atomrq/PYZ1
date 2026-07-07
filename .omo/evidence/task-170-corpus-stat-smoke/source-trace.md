# Task 170 Source Trace

Date: 2026-07-07

## Classification

`source_contract`

## Sources Checked

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  - Local mirror of `https://github.com/mkmat/Z1plus-code`.
  - Checked commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/benchmark-configurations/README.md`
  - States that benchmark 07/10/11 results can be reproduced from either
    `benchmark-XX.Z1` or `benchmark-XX.dump`.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/benchmark-configurations/benchmark-{07,10,11}.Z1`
  - Public Z1 input files used by task169 input smoke.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/benchmark-configurations/benchmark-{07,10,11}.dump`
  - Public LAMMPS dump inputs used by task169 input smoke.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/benchmark-configurations/Z1+reference-results/log-benchmark-{07,10,11}.txt`
  - Public Z1+ reference logs used by task168 reference-log smoke.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/benchmark-configurations/PPA+reference-results/log-benchmark-{07,10,11}.txt`
  - Public PPA+ reference logs used by task168 reference-log smoke.

## Clean-Room Boundary

This slice adds a corpus consistency report that cross-checks public benchmark
inputs against public reference-log summary fields. It uses existing pyz1
input and reference-log parsers, does not run or vendor `Z1+.ex`, does not use
the hidden reducer core, and does not claim reducer coordinate parity for
benchmark 07/10/11.

## RED Target

Focused tests should fail before implementation because
`pyz1.corpus_smoke` and the CLI/report entry point do not exist yet. GREEN
requires benchmark 07/10/11 to report zero chain-count and mean-`N` deltas
between `.Z1`/`.dump` input statistics and Z1+/PPA+ reference-log statistics.

## Evidence

- RED Slurm job `416784` failed for the intended reason:
  `ModuleNotFoundError: No module named 'pyz1.corpus_smoke'`.
  - Artifact: `red-focused-416784.out`
- Final focused Slurm job `416788` passed the corpus smoke tests.
  - Artifact: `focused-final-416788.out`
- Final static Slurm job `416789` passed `ruff check` and
  `basedpyright --pythonpath` for the changed corpus report surface, CLI, and
  focused tests.
  - Artifact: `static-final-416789.out`
- Final package/report smoke Slurm job `416790` passed editable install and
  the `pyz1-corpus-stat-smoke` console script.
  - Artifacts: `package-smoke-final-416790.out`,
    `corpus-stat-smoke-final.md`

The final report records benchmark 07, 10, and 11 as `passed`: `.Z1`/`.dump`
input statistics agree, and both Z1+ and PPA+ reference logs have zero
chain-count and mean-`N` deltas relative to the input statistics.
