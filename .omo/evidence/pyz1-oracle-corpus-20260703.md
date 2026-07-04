# pyz1 oracle corpus evidence

Date: 2026-07-03

## Scope

This artifact records the first multi-benchmark Z1+ oracle corpus generated on
the Linux cluster for `pyz1`.

Source benchmark directory:

```text
/Users/jiaxm/Contents/CodexProjects/source_code/Z1+
```

Remote work root:

```text
/public/home/jxm/codex_tmp/pyz1_oracle_full_20260703_164229
```

Remote route:

```text
ssh -p 6301 jxm@47.104.203.55
```

Remote environment observed earlier in this run:

```text
hostname: admin
kernel: Linux 3.10.0-1160.el7.x86_64
Python used for oracle CLI: /public/home/jxm/.local/bin/python3 via venv
```

## Generator

The generator is implemented in:

- `src/pyz1/oracle.py`
- `src/pyz1/oracle_models.py`
- `src/pyz1/oracle_cli.py`

The CLI entry used after the refactor is:

```text
python -m pyz1.oracle_cli --benchmarks <z1plus_dir> --out <out_dir> --z1-install <z1plus_dir> --modes <modes> --timeout-seconds 120
```

It stages the Z1+ wrapper into a distinct install directory, rewrites the
wrapper install path for the staged directory, runs the Perl wrapper, records
stdout/stderr, hashes existing outputs, and writes `manifest.json`.

The timeout behavior is intentional: a timed-out run is recorded with
`exit_code=124`, `summary_rows=0`, stderr text, and no fabricated output hashes.

## Local fixture corpora

Default, SP+, and self-entanglement corpus:

```text
tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703/manifest.json
```

Summary:

```text
runs: 42
exit_counts: {'0': 39, '124': 3}
summary_rows: 38
timeouts:
  - .benchmark-09.Z1:default
  - .benchmark-09.Z1:spplus
  - .benchmark-09.Z1:selfz
```

PPA and PPA+ corpus:

```text
tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703/manifest.json
```

Summary:

```text
runs: 28
exit_counts: {'0': 25, '124': 3}
summary_rows: 9 in the original manifest; 10 on local reparse after the
Fortran overflow-token parser fix
timeouts:
  - .benchmark-07.Z1:ppa
  - .benchmark-10.Z1:ppa
  - .benchmark-11.Z1:ppa
```

The PPA/PPA+ corpus originally had fewer parsed summary rows because
`benchmark-05/ppaplus/PPA+summary.dat` contains Fortran overflow fields rendered
as `************`. The parser now treats those fields as `nan`, so every
materialized summary file in both local corpora parses successfully.

Reparse evidence:

```text
.omo/evidence/task-5-overflow-corpus-parse-pyz1-cleanroom-reproduction.txt
default/SP+/selfZ: summary_files=38 parseable=38 failed=0 parsed_rows=38
PPA/PPA+: summary_files=10 parseable=10 failed=0 parsed_rows=10
```

## Local verification

Focused oracle generator checks:

```text
tests/test_oracle.py
6 passed
```

Quality gate after fixing the CLI module entry and relative output paths:

```text
pytest: 26 passed
ruff: All checks passed
basedpyright: 0 errors, 0 warnings, 0 notes
```

LOC check after the parser and oracle fixes:

```text
src/pyz1/oracle.py        240
src/pyz1/oracle_cli.py     58
src/pyz1/oracle_models.py  67
src/pyz1/output_io.py     226
tests/test_oracle.py      183
tests/test_output_io.py    86
```

Final local gate evidence:

```text
.omo/evidence/final-gate-pyz1-oracle-corpus-20260703.txt
```

Remote 300-second rerun for the six timeout cases was launched after fixing the
relative output-path bug:

```text
remote_root: /public/home/jxm/codex_tmp/pyz1_oracle_full_20260703_164229
log: /public/home/jxm/codex_tmp/pyz1_oracle_full_20260703_164229/oracle_long_300s.log
local status evidence: .omo/evidence/task-7-long-rerun-status-pyz1-cleanroom-reproduction.txt
```

300-second rerun result:

```text
.omo/evidence/oracle-long-300s-20260703/b09-manifest.json
runs 3
exit_counts {'124': 3}
summary_rows 0
timeouts ['.benchmark-09.Z1:default', '.benchmark-09.Z1:spplus', '.benchmark-09.Z1:selfz']

.omo/evidence/oracle-long-300s-20260703/ppa-manifest.json
runs 3
exit_counts {'0': 2, '124': 1}
summary_rows 2
timeouts ['.benchmark-11.Z1:ppa']
```

Interpretation: increasing the per-run timeout from 120 seconds to 300 seconds
recovers `benchmark-07:ppa` and `benchmark-10:ppa`, but not `benchmark-09`
default/SP+/selfZ or `benchmark-11:ppa`.

## Completion status

Completed:

- `docs/pyz1-contract.md`
- oracle manifest models
- oracle generator with staged wrapper execution
- timeout handling
- unparseable-summary tolerance at the manifest boundary
- Fortran overflow-token parsing for PPA/PPA+ summaries
- CLI module entry for `python -m pyz1.oracle_cli`
- relative-path-safe oracle output directory handling
- local fixture corpora for all 14 benchmarks across five modes

Not complete:

- completion of the four still-long benchmark/mode pairs after the 300-second
  rerun:
  `.benchmark-09.Z1:{default,spplus,selfz}` and `.benchmark-11.Z1:ppa`
- final all-modes all-benchmarks exit-0 oracle corpus
