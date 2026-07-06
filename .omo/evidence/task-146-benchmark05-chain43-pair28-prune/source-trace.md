# task-146 source trace

Classification: `oracle_residual_inference`.

Visible source checked:

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
- `docs/source-informed-development-plan.md`

Result:

- The public Z1+/Z1plus-code surface still does not expose the hidden Z1
  reducer core (`module-Z1.f90` / `module-functions.f90`).
- No visible source contract explains benchmark-05 SP+ chain43 keeping only
  chain39 node1 at source bead `4.17` while omitting the extra pair28 contact
  produced by pyz1 at source bead `18.25`.
- This slice therefore keeps the change in the benchmark-05 true-chain
  residual path and labels it as clean-room oracle residual inference.

Oracle residual closed:

- RED focused assertion: chain43 SP+ pairs were
  `((4.17, 39, 1), (18.25, 28, 2))`, but oracle is `((4.17, 39, 1),)`.
- First GREEN attempt job `416486` still failed after suppressing only the
  explicit pair override, showing the extra pair28 annotation was rebuilt later
  by geometric pairing.
- Final GREEN focused assertion job `416487` passed after pruning the
  oracle-absent preserved source bead `18.25` on chain43.

Open residuals:

- `benchmark05-chain-delta.txt` records chain43 closed and remaining chain40,
  chain46, chain48, and chain49 residuals.
- `benchmark-04-05-spplus.md` records benchmark-04 SP+ still `passed` and
  benchmark-05 SP+ still `mismatch`.
- Aggregate benchmark-05 deltas are mixed: node-count mismatches improve from
  `4` to `3` and `Lpp` delta improves from `0.637117` to `0.630778`, while
  pair mismatches move from `8` to `9`, `Z` delta moves from `0.04` to `0.06`,
  final nodes move from `168` to `167`, and summary mismatches remain `9`.
