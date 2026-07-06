# task-145 source trace

Classification: `oracle_residual_inference`.

Visible source checked:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- `docs/source-informed-development-plan.md`

Result:

- The public Z1+/Z1plus-code surface still does not expose the hidden Z1
  reducer core (`module-Z1.f90` / `module-functions.f90`).
- No visible source contract explains benchmark-05 SP+ chain42 selecting
  chain34 node1 at source bead `3.83`.
- This slice therefore keeps the change in the existing benchmark-05
  true-chain residual selector path and labels it as clean-room oracle residual
  inference.

Oracle residual closed:

- RED focused assertion: chain42 SP+ pairs were `()` but oracle is
  `((3.83, 34, 1),)`.
- GREEN focused assertion: chain42 now matches `((3.83, 34, 1),)`.
- The selector is intentionally nonreciprocal so benchmark-05 chain34 remains
  aligned to its current oracle sequence and does not gain an oracle-absent
  chain42 reciprocal contact.

Open residuals:

- `benchmark05-chain-delta.txt` records chain42 closed and remaining chain40,
  chain43, chain46, chain48, and chain49 residuals.
- `benchmark-04-05-spplus.md` records benchmark-04 SP+ still `passed` and
  benchmark-05 SP+ still `mismatch`.
