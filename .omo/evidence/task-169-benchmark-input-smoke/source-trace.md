# Task 169 Source Trace

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
  - Public Z1 input files for benchmark 07/10/11.
  - Header contract: chain count, box lengths, chain lengths, then coordinates.
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code/benchmark-configurations/benchmark-{07,10,11}.dump`
  - Public LAMMPS dump inputs for benchmark 07/10/11.
  - Header contract: one frame, atom count, orthogonal `BOX BOUNDS pp pp pp`,
    and `ITEM: ATOMS id mol type x y z`.

## Clean-Room Boundary

This slice adds an input smoke/report surface only. It parses public `.Z1` and
LAMMPS `.dump` benchmark inputs to record chain count, node count, true-chain
count, box lengths, and shear. It does not run or vendor `Z1+.ex`, does not use
the hidden reducer core, and does not claim reducer parity for benchmark
07/10/11.

## RED Target

Focused tests should fail before implementation because
`pyz1.benchmark_inputs` and the CLI/report entry point do not exist yet. GREEN
requires `.Z1` and `.dump` records for benchmark 07/10/11 to parse as
source-backed input smoke records, with matching chain/node/box baselines.

## Evidence

- RED Slurm job `416777` failed for the intended reason:
  `ModuleNotFoundError: No module named 'pyz1.benchmark_inputs'`.
  - Artifact: `red-focused-416777.out`
- Final focused Slurm job `416781` passed the benchmark input tests.
  - Artifact: `focused-final-416781.out`
- Final static Slurm job `416782` passed `ruff check` and
  `basedpyright --pythonpath` for the changed parser/report surface, CLI, and
  focused tests.
  - Artifact: `static-final-416782.out`
- Final package/report smoke Slurm job `416783` passed editable install and
  the `pyz1-benchmark-input-smoke` console script.
  - Artifacts: `package-smoke-final-416783.out`,
    `benchmark-input-smoke-final.md`

The final report records six parseable source-backed benchmark input records:
`.Z1` and `.dump` for benchmark 07, 10, and 11. The `.Z1` and `.dump` records
agree on chain count, node count, true-chain count, and box lengths for each
benchmark.
