# Task 173 Validation

Remote run root:
`/public/home/jxm/pyz1-cleanroom-runs/task-173-corpus-ne-smoke`.

## Passing Gates

- Focused GREEN: job `416807`, `COMPLETED`, `ExitCode=0:0`
  - `tests/test_corpus_smoke.py::test_write_corpus_smoke_report_when_inputs_and_logs_align_reports_passed`
- Focused/static final: job `416810`, `COMPLETED`, `ExitCode=0:0`
  - focused pytest
  - `ruff check src/pyz1/corpus_smoke.py tests/test_corpus_smoke.py`
  - `basedpyright src/pyz1/corpus_smoke.py tests/test_corpus_smoke.py`
- Package/CLI smoke final: job `416811`, `COMPLETED`, `ExitCode=0:0`
  - editable install with Tsinghua PyPI mirror
  - `pyz1-corpus-stat-smoke` generated `corpus-stat-ne-smoke-final.md`
  - report contains `Z1+ <Z>`, `Z1+ Ne_MC`, and `PPA+ Ne_MC`

## Superseded Or Expected Failures

- `416806`: intended RED; `CorpusSmokeRecord` lacked
  `z1plus_mean_entanglements`.
- `416808`: superseded static failure; `ruff` flagged a long Markdown separator
  line before the separator was generated from the header.
- `416809`: package smoke passed before the final separator cleanup; retained
  as superseded evidence by `416811`.
