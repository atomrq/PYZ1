# task-175 corpus PPA+ statistical fields source trace

Classification: `source_contract`.

This slice extends the benchmark 07/10/11 corpus statistical smoke report with
additional source-backed reference-log fields. It does not change reducer or
PPA/PPA+ runtime behavior and does not claim PPA+ coordinate parity.

Source mirror:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- Git SHA: `c7219cd394b1295272ebfc098f2835c5c871e6ec`

Relevant public reference logs:

- `benchmark-configurations/Z1+reference-results/log-benchmark-07.txt`
- `benchmark-configurations/Z1+reference-results/log-benchmark-10.txt`
- `benchmark-configurations/Z1+reference-results/log-benchmark-11.txt`
- `benchmark-configurations/PPA+reference-results/log-benchmark-07.txt`
- `benchmark-configurations/PPA+reference-results/log-benchmark-10.txt`
- `benchmark-configurations/PPA+reference-results/log-benchmark-11.txt`

Fields used from the public logs:

- Z1+ `< Lpp >`
- Z1+ `< Z >`
- Z1+ `Ne_MC`
- PPA+ `< Lpp >`
- PPA+ `< Z >`
- PPA+ `Ne_CC`
- PPA+ `Ne_MC`

Implementation intent:

- Keep the corpus smoke status anchored to input/reference structural alignment.
- Expose additional PPA+ summary/statistical values so future statistical
  parity checks have visible source-backed reference targets.
- Keep this report surface separate from native PPA+ coordinate parity.
