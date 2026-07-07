# task-176 reference-log physical fields source trace

Classification: `source_contract`.

This slice extends the public Z1+/PPA+ reference-log smoke report with physical
fields that are already parsed from `mkmat/Z1plus-code` reference logs but were
not yet visible in the markdown report. It does not change reducer runtime or
native PPA/PPA+ execution behavior.

Source mirror:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- Git SHA: `c7219cd394b1295272ebfc098f2835c5c871e6ec`

Relevant public reference logs:

- `benchmark-configurations/Z1+reference-results/log-benchmark-07.txt`
- `benchmark-configurations/PPA+reference-results/log-benchmark-07.txt`
- benchmark 10/11 logs under the same directories

Fields used from the public result sections:

- `Ree`
- `app`
- `bpp`
- `< N >`

Implementation intent:

- Keep `ReferenceLogRecord` parsing unchanged.
- Expose already-parsed `Ree`, `app`, `bpp`, and `<N>` fields in the reference
  log smoke report.
- Strengthen source-backed statistical/physical report targets for benchmark
  07/10/11 without treating them as reducer or coordinate parity gates.
