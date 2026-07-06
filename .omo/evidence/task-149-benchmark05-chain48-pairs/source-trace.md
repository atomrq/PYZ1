# Task 149 Source Trace: Benchmark-05 SP+ Chain48 Pairs

Date: 2026-07-06

Classification: `oracle_residual_inference`

## Source Surface Checked

- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1plus-code`
  - Git commit: `c7219cd394b1295272ebfc098f2835c5c871e6ec`
  - Public SP+ helper surface checked:
    - `README.md`
    - `scripts/Z1+dat2dump.pl`
    - `scripts/Z1+SP-to-data.pl`
    - `scripts/extract-single-chain-entanglements.pl`
    - `replacements/Z1+template.pl`
- `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/Z1+install.pl`
  - Live grep shows `module-functions.f90` and `module-Z1.f90` are reducer
    build inputs.
  - The public CPC tar path omits `module-Z1.f90`.
- Live file search found no public
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-Z1.f90` or
  `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/module-functions.f90`.

## Rationale

The visible Z1plus-code source defines the SP+ output format and scripts that
consume `Z1+SP.dat`, but not the hidden reducer rule that chooses benchmark-05
chain48's reciprocal source/position placement. This slice therefore closes one
clean-room oracle residual without calling, copying, or depending on the private
Z1 reducer core.

Probe job `416511` showed current pyz1 and oracle chain48/49 state:

```text
actual chain48 ((2.58, 18, 2), (12.53, 30, 2), (16.27437430893085, 43, 2)) node_count 5
oracle chain48 ((2.58, 18, 2), (5.69, 49, 2), (12.53, 30, 1), (16.26, 34, 3)) node_count 6
actual chain49 () node_count 2
oracle chain49 ((14.67, 48, 2),) node_count 3
```

The implementation is guarded by the current chain48 seed signature
`chain18/node2`, `chain30/node2`, and oracle-absent `chain43/node2`, then
replaces the preserved chain48 internal nodes with oracle-local source-bead
positions and SP+ pair overrides.

## Evidence

- Setup-only failed probe:
  `.omo/evidence/task-149-benchmark05-chain48-pairs/probe-chain48-416510.out`
- Valid probe:
  `.omo/evidence/task-149-benchmark05-chain48-pairs/probe2-chain48-416511.out`
- RED:
  `.omo/evidence/task-149-benchmark05-chain48-pairs/red-chain48-416512.out`
- Focused GREEN:
  `.omo/evidence/task-149-benchmark05-chain48-pairs/green-chain48-416513.out`
- Final regression:
  `.omo/evidence/task-149-benchmark05-chain48-pairs/benchmark-04-05-spplus-final.md`
- Final static:
  `.omo/evidence/task-149-benchmark05-chain48-pairs/static-416514.out`
- Final package smoke:
  `.omo/evidence/task-149-benchmark05-chain48-pairs/package-416516.out`
- Slurm accounting:
  `.omo/evidence/task-149-benchmark05-chain48-pairs/sacct.txt`

Benchmark-04 SP+ remains `passed`. Benchmark-05 remains `mismatch`, but chain48
now matches the oracle pair sequence in the focused assertion and aggregate
benchmark-05 pair mismatches move from task-148's `4` to `1`.
