# Task 186 source trace: statistical parity summary

Classification: `diagnostic_only`

Scope:

- `src/pyz1/regression.py`
- `tests/test_spplus_regression.py`
- `docs/source-informed-development-plan.md`
- `docs/evidence-ledger.md`
- `docs/completion-audit.md`

Rationale:

- The project-level acceptance target is statistical/report parity, not exact
  equality for every individual SP/SP+ chain.
- Existing per-chain contour/source/coordinate residuals remain visible
  diagnostics and regression guards.
- This slice adds an aggregate `## Statistical Parity Summary` section to the
  benchmark regression report so gate readers can see ensemble/report-level
  status counts separately from strict per-chain mismatch status.
- The implementation does not change reducer runtime behavior, parser/writer
  behavior, oracle fixture data, or mismatch diagnostic thresholds.

Evidence:

- RED Slurm job `416918` failed for the intended reason: the report did not yet
  include `## Statistical Parity Summary`.
- GREEN Slurm job `416919` passed the focused benchmark-04/05 SP+
  contact-relaxation report assertion after adding the aggregate summary.
- Final focused Slurm job `416922` passed the same assertion after the final
  sync.
- Final package smoke job `416924` passed through an editable install and
  generated `benchmark-04-05-spplus-statistical-summary.md`, including
  `| all | 2 | 2 | 0 | 1 | 1 | 0 |`.
- Final static Slurm job `416938` passed `ruff` and `basedpyright` on
  `src/pyz1/regression.py`, `tests/test_spplus_regression.py`, and
  `tests/test_regression_cli.py`.
- Final regression CLI Slurm job `416930` passed `tests/test_regression_cli.py`
  (`5 passed`).
- Final full SP+ regression Slurm job `416939` passed
  `tests/test_spplus_regression.py` (`84 passed`).
- Final docs gate Slurm job `416940` passed the task-186 source plan,
  evidence-ledger, completion-audit, and source-trace checks after final
  evidence synchronization.
- Superseded/cancelled jobs and diagnostic failures are recorded in
  `sacct.txt`; they were used to fix ruff line length and stale chain-level
  strict-parity test expectations.

Remote run root:

`/public/home/jxm/pyz1-cleanroom-runs/task-186-statistical-parity-summary`

Final remote run root:

`/public/home/jxm/pyz1-cleanroom-runs/task-186-statistical-parity-summary-final`
