# pyz1 Task-92 Continuation Handoff

## 1. Origin And Live State

- Source thread id: `019f25e7-a7e7-7a01-b0e6-0dd5a2e489dc`
- Date: 2026-07-04
- CWD / repo root: `/Users/jiaxm/Contents/CodexProjects/Z1`
- Branch: `main`
- Latest accepted code slice commit: `4080f5c feat(pyz1-reducer): retain reciprocal true-chain contacts`
- Remote branch `main` on `origin` was at `4080f5c3f56a2d5d6e5c5348645c4f89186335c5` when the slice completed
- `git status --short --branch` immediately after task-92 push:

```text
## main...origin/main
```

This handoff packet is expected to be committed after the accepted code slice.
If `HEAD` is later than `4080f5c` only because this packet was committed, treat
that as a declared difference, not a blocker.

## 2. Instructions And Policy Read

- User-provided global `AGENTS.md` instructions in the source thread:
  Chinese by default, live-state-first, preserve user changes, use
  `/Users/jiaxm/Contents/CodexProjects` as project root, use
  `/Users/jiaxm/.codex/RESOURCES.md` before remote/source mirror work, use
  `micromamba run -n pyz1`, use Tsinghua mirror for pip installs, keep durable
  plans/evidence in repo docs, and use CodeGraph first when `.codegraph/`
  exists.
- Continue-thread skill:
  `/Users/jiaxm/.codex/skills/continue-thread/SKILL.md`
- Git skill:
  `/Users/jiaxm/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/git-master/SKILL.md`
- Python programming skill and Python reference:
  `/Users/jiaxm/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/programming/SKILL.md`
  and
  `/Users/jiaxm/.codex/plugins/cache/sisyphuslabs/omo/4.13.0/skills/programming/references/python/README.md`
- Project docs read for the handoff:
  `README.md`, `docs/completion-audit.md`, `docs/evidence-ledger.md`
- Repo-local `AGENTS.md` and repo-local task tracker markdown were not present
  at handoff time.
- `.codegraph/` exists and `collect_handoff_state.py` reported both index and
  database present.

## 3. Current Objective And Trackers

Active goal objective, exact text:

```text
完成 pyz1 clean-room 复现的全部计划，推进到完整落地：本地测试持续通过，Z1+ 输出 parser/writer、summary/Ne、oracle parity、PPA/PPA+、clean-room Z1 reducer、SP+ regression、文档和最终集成 smoke 均有可追踪 evidence
```

Goal status at handoff: `active`.

Primary tracker/spec files:

- `README.md`
- `docs/evidence-ledger.md`
- `docs/completion-audit.md`
- `docs/pyz1-contract.md`
- local evidence under `.omo/evidence/` (ignored by Git, intentionally not
  pushed)

Last accepted gate: task-92 reciprocal true-chain contact retention, commit
`4080f5c`.

## 4. Completed Work In Task-92

Task-92 added reciprocal true-chain contact retention for paired collapsed true
chains in `src/pyz1/reducer.py`.

Changed source/test/doc files in commit `4080f5c`:

- `src/pyz1/reducer.py`
  - added paired contact position/source fields to `_TrueChainContactCandidate`
  - added reciprocal fields to `_PreservedKinkCandidate`
  - added `_ReciprocalRetentionState`
  - when true-chain contact candidates are selected, queued reciprocal
    candidates for the paired target chains
  - inserted reciprocal true-chain candidates into still-collapsed two-node
    chains and carried reciprocal `ShortestPathPair` overrides
- `tests/test_spplus_regression.py`
  - locked benchmark-05 task-92 node-count mismatch at `49`
- `docs/evidence-ledger.md`
  - updated latest gate paths and task-92 SP+ diagnostics
- `docs/completion-audit.md`
  - updated latest gate paths, task-92 artifact, remaining boundary, and next
    reducer work

Task-92 focused report:

- `.omo/evidence/task-92-true-chain-reciprocal-retention/benchmark-04-05-spplus.md`

Observed report result:

- benchmark-04 SP+: `passed`
- benchmark-05 SP+: still `mismatch`
- benchmark-05 final nodes improved from 127 to 137
- benchmark-05 node-count mismatches improved from 57 to 49
- benchmark-05 `Lpp` delta improved from `0.802656` to `0.461065`
- benchmark-05 `Z` delta improved from `0.86` to `0.66`
- true-chain pair sequence remains matched at `40,26`
- true-chain pair node sequence remains matched at `3,2`

## 5. Incomplete Work And Next Exact Action

The project is not complete. `docs/completion-audit.md` still states this
explicitly.

Next exact implementation action:

1. Start from benchmark-05 SP+ after task-92.
2. Investigate reciprocal source/position placement and remaining paired-chain
   coverage for the chains that still show node-count/source/geometry gaps.
3. Use the existing report surface in `tests/test_spplus_regression.py` and
   `.omo/evidence/task-92-true-chain-reciprocal-retention/benchmark-04-05-spplus.md`.
4. Add a failing focused assertion before reducer changes.
5. Keep benchmark-04 SP+ passed and improve benchmark-05 without weakening
   existing mismatch diagnostics.

Do not mark the active goal complete until the completion audit boundaries are
actually closed or explicitly accepted as final non-goals by the user.

## 6. RED/GREEN/Review/Runner State

No RED/GREEN step is in progress.

Task-92 verification passed:

```text
ulimit -n 1000000 && micromamba run -n pyz1 pytest -q
137 passed in 107.01s (0:01:47)

ulimit -n 1000000 && micromamba run -n pyz1 ruff check .
All checks passed!

ulimit -n 1000000 && micromamba run -n pyz1 basedpyright
0 errors, 0 warnings, 0 notes

ulimit -n 1000000 && micromamba run -n pyz1 pytest tests/test_package_integration_smoke.py -q
1 passed in 11.63s

git diff --check
exit 0
```

Evidence artifact paths:

- `.omo/evidence/task-92-true-chain-reciprocal-retention/pytest.txt`
- `.omo/evidence/task-92-true-chain-reciprocal-retention/ruff.txt`
- `.omo/evidence/task-92-true-chain-reciprocal-retention/basedpyright.txt`
- `.omo/evidence/task-92-true-chain-reciprocal-retention/package-smoke.txt`
- `.omo/evidence/task-92-true-chain-reciprocal-retention/diff-check.txt`
- `.omo/evidence/task-92-true-chain-reciprocal-retention/benchmark-04-05-spplus.md`

Manual QA gate for this CLI/library slice is the package and regression report
surface above, not a UI.

## 7. Source/Reference Trace

Already used:

- Z1+ public tree under `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+`
  in earlier slices; the visible public tree lacks `module-Z1.f90`.
- Z1+ oracle fixtures under:
  `tests/fixtures/z1plus_oracle/corpus-default-spplus-selfz-20260703`
  and `tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703`
- CodeGraph for `src/pyz1/reducer.py`, especially
  `_preserve_close_contacts`, `_apply_reciprocal_true_chain_candidates`,
  `_true_chain_contact_kink_candidate`, and
  `_extend_reciprocal_true_chain_candidates`.

Still required:

- Continue reading live source/docs before editing.
- Use CodeGraph first for reducer/source questions while `.codegraph/` exists.
- If remote/source mirror/cluster access becomes relevant, read
  `/Users/jiaxm/.codex/RESOURCES.md` first.

## 8. Decisions, Non-Goals, And Forbidden Actions

Current decisions:

- `pyz1` remains a clean-room Python implementation. It does not use
  Linux `Z1+.ex` at runtime.
- Development stays local in micromamba env `pyz1`.
- No GPU, Numba, CuPy, PyTorch, or accelerator-specific dependency.
- `.omo/` and `.debug-journal.md` stay ignored and local.
- The original public Z1+ source is incomplete for the reducer; do not claim a
  Fortran line-by-line port.

Forbidden or unsafe:

- Do not revert unrelated user changes.
- Do not weaken regression tests to make parity look better.
- Do not mark goal complete while `docs/completion-audit.md` still has open
  scientific/scalability boundaries.
- Do not push `.omo/` evidence to Git.
- Do not touch `main` destructively; no reset, force push, or history rewrite.

## 9. Dirty/Untracked Worktree Summary

At task-92 slice completion, before this packet was written:

```text
## main...origin/main
```

After this packet is committed, the worktree should again be clean. `.omo/`
evidence is ignored/local by design.

## 10. Known Risks And Blockers

- Full default/SP+ numerical parity remains open for benchmarks 01/02/03/05.
- Benchmark-05 SP+ still has source-bead, geometry, remaining reciprocal
  coverage, node-count, pair-detail, and summary mismatches.
- Benchmark-06+ default/SP+/selfZ remain guarded under the default
  `node_count>1000` contract.
- Full native PPA/PPA+ runtime parity remains open.
- selfZ scientific parity remains open beyond package execution and regression
  reporting.
- `omo sparkshell` was unavailable earlier because the LazyCodex runtime target
  was missing; raw shell and CodeGraph were used instead. Do not repair
  LazyCodex unless the user asks.

## 11. Claims To Re-Verify In New Thread

Run live checks before implementation:

- `git status --short --branch` is clean.
- `git log -2 --oneline` includes the task-92 commit and this handoff packet
  commit.
- `.omo/evidence/task-92-true-chain-reciprocal-retention/pytest.txt` exists and
  says `137 passed`.
- `.omo/evidence/task-92-true-chain-reciprocal-retention/benchmark-04-05-spplus.md`
  exists and records benchmark-04 SP+ `passed`, benchmark-05 SP+ `mismatch`,
  node-count mismatches `49`, true-chain pair sequence `40,26`, and true-chain
  pair node sequence `3,2`.
- `docs/completion-audit.md` still says the project is not complete.

If any of these are missing or conflict with live state, stop implementation and
repair the handoff or ask the user.

## 12. Handoff Decision

Checkpoint result: `create_continuation_thread`.

Quality gate result: passed. Task-92 has no RED/GREEN in progress, full local
tests and package smoke passed, docs are synchronized, and the accepted code
slice is committed and pushed.

Continuation reason: the user explicitly asked to complete this slice and then
perform `continue-thread`. This is also a safe boundary after several accepted
non-trivial reducer slices.

Slice count alone is not the reason; the handoff is justified by the explicit
user request plus a completed, verified, pushed task-92 slice.

## 13. Old-Thread Archival Plan

Archival is not performed by the old/source thread.

The new thread owns old-thread archival after first successful verification. It
may archive the source thread only after it creates/restores the active goal,
verifies live state, reads this packet, confirms named artifacts exist, and
finds no blocking mismatch.

Source thread id to archive after successful verification:
`019f25e7-a7e7-7a01-b0e6-0dd5a2e489dc`.

If thread archival tooling is unavailable, the new thread should report that
exact stop reason and leave the source thread unarchived.

## Active Goal Transfer

Goal status to create or restore in the new thread: `active`.

Exact objective:

```text
完成 pyz1 clean-room 复现的全部计划，推进到完整落地：本地测试持续通过，Z1+ 输出 parser/writer、summary/Ne、oracle parity、PPA/PPA+、clean-room Z1 reducer、SP+ regression、文档和最终集成 smoke 均有可追踪 evidence
```

First new-thread instruction:

```text
先调用 goal tool 创建/恢复上面的完整 active goal；不要缩短为 task-92。然后执行本 handoff 的 startup gate，再继续下一 reducer parity slice。
```

## First Live-State Commands

Run these before implementation:

```bash
pwd
git status --short --branch
git log -3 --oneline
sed -n '1,220p' README.md
sed -n '1,240p' docs/handoffs/2026-07-04-pyz1-task92-continuation.md
sed -n '1,220p' docs/completion-audit.md
tail -n 5 .omo/evidence/task-92-true-chain-reciprocal-retention/pytest.txt
cat .omo/evidence/task-92-true-chain-reciprocal-retention/ruff.txt
cat .omo/evidence/task-92-true-chain-reciprocal-retention/basedpyright.txt
cat .omo/evidence/task-92-true-chain-reciprocal-retention/package-smoke.txt
```

## Exact Starter Message For New Thread

```text
接续 pyz1 clean-room 复现目标。请先创建/恢复 active goal，目标原文如下：

完成 pyz1 clean-room 复现的全部计划，推进到完整落地：本地测试持续通过，Z1+ 输出 parser/writer、summary/Ne、oracle parity、PPA/PPA+、clean-room Z1 reducer、SP+ regression、文档和最终集成 smoke 均有可追踪 evidence

然后执行 startup gate：
1. 在 /Users/jiaxm/Contents/CodexProjects/Z1 运行 pwd、git status --short --branch、git log -3 --oneline。
2. 阅读 docs/handoffs/2026-07-04-pyz1-task92-continuation.md、README.md、docs/completion-audit.md、docs/evidence-ledger.md 的相关段落。
3. 确认 task-92 evidence artifact 存在：.omo/evidence/task-92-true-chain-reciprocal-retention/{pytest.txt,ruff.txt,basedpyright.txt,package-smoke.txt,benchmark-04-05-spplus.md}。
4. 报告 startup result，格式使用 continue-thread skill 的 startup report。
5. 若 startup gate 无 blocking mismatch，继续下一 reducer parity slice：从 benchmark-05 SP+ 的 reciprocal source/position placement 与 remaining paired-chain coverage 入手，先写 failing focused assertion，再改 reducer；保持 benchmark-04 SP+ passed，不要弱化现有 mismatch diagnostics。

验证通过后，新线程负责向源线程 019f25e7-a7e7-7a01-b0e6-0dd5a2e489dc 回报 continuation verification，并在可用工具允许时归档源线程；如果线程消息或归档工具不可用，明确报告不可用原因并保持源线程未归档。
```
