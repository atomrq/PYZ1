# task-147 source trace

Classification: `oracle_residual_inference`.

Visible source checked:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- `docs/source-informed-development-plan.md`

Result:

- The public Z1+/Z1plus-code surface still does not expose the hidden Z1
  reducer core (`module-Z1.f90` / `module-functions.f90`).
- No visible source contract explains benchmark-05 SP+ chain40 assigning
  pair25 node3 at source bead `3.59`, pair1 node2 at source bead `7.07`, and
  pair4 node1 at source bead `14.96`.
- This slice therefore keeps the change in the benchmark-05 true-chain
  residual post-pass and labels it as clean-room oracle residual inference.

Oracle residual closed:

- Superseded RED job `416491` failed from remote `PYTHONPATH` setup, not from
  the focused assertion.
- Valid RED job `416492` captured the previous chain40 pair sequence
  `((4.235660267645262, 25, 2), (11.6582816078166, 1, 2), (14.96, 4, 1))`
  versus oracle `((3.59, 25, 3), (7.07, 1, 2), (14.96, 4, 1))`.
- GREEN jobs `416493` and final rerun `416497` passed the focused assertion.

Gate notes:

- Regression job `416494` and final rerun `416499` show benchmark-04 SP+
  still `passed` and benchmark-05 SP+ still `mismatch`.
- Initial static job `416495` is superseded: Slurm reported `0:0` because the
  shell command used `;`, but its output contains a `ruff` `PLR2004` failure.
  Final static rerun `416498` used `&&` and passed `ruff` plus `basedpyright`.
- Package smoke job `416496` and final rerun `416500` passed.

Open residuals:

- `benchmark05-chain-delta.txt` records chain40, chain42, and chain43 closed.
  Remaining active benchmark-05 local pair-sequence chains are chain46,
  chain48, and chain49.
- Aggregate benchmark-05 deltas after task147 are: pair mismatches improve from
  `9` to `8`; node-count mismatches remain `3`; `Lpp` delta remains
  `0.630778`; `Z` delta remains `0.06`; final nodes remain `167`; summary
  mismatches remain `9`.
