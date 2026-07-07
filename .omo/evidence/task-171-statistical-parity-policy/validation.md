# Task 171 Validation

Remote run root:
`/public/home/jxm/pyz1-cleanroom-runs/task-171-statistical-parity-policy`.

## Passing Gates

- Job: `416794`
- Command surface: Slurm docs gate on the GPU cluster
- Result: `COMPLETED`, `ExitCode=0:0`
- Stdout: `docs-gate-passed`
- Job: `416795`
- Command surface: post-doc-sync Slurm docs gate on the GPU cluster
- Result: `COMPLETED`, `ExitCode=0:0`
- Stdout: `docs-gate-final-passed`

The gates checked that:

- `.omo/evidence/task-171-statistical-parity-policy/source-trace.md` exists;
- `.omo/evidence/task-171-statistical-parity-policy/validation.md` exists;
- `docs/pyz1-contract.md` records `statistical parity`;
- `docs/source-informed-development-plan.md` records that exact equality for
  every individual chain is not the target;
- `docs/completion-audit.md` references `task-170-corpus-stat-smoke`;
- `docs/evidence-ledger.md` references the task171 docs-gate evidence;
- the task171 source trace is classified as `diagnostic_only`.

## Superseded Gate

- Job: `416793`
- Result: `FAILED`, `ExitCode=1:0`
- Reason: the first docs gate used an exact grep for a phrase that crossed a
  Markdown line break. No source or policy defect was found; job `416794`
  replaced this check with line-local terms.
