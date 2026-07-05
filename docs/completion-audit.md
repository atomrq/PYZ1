# pyz1 Completion Audit

This audit maps the active clean-room reproduction goal to current repo evidence.
It is a completion gate, not a parity claim.

Last audited: 2026-07-05.

## Current Verdict

The project is not complete yet. The implemented package has broad parser,
writer, oracle, PPA/PPA+, reducer, SP+, CLI, and smoke coverage, but current
evidence still leaves scientific and scalability boundaries open.

## Proven Current Coverage

| Requirement | Current evidence | Verdict |
| --- | --- | --- |
| Z1 parser and typed input model | `tests/test_z1_io.py`, `tests/test_models.py` | Covered |
| Z1+ output parser/writer coverage | `tests/test_output_io.py`, `tests/test_output_values.py`, `tests/test_initconfig_io.py` | Covered |
| Summary and `Ne` estimator implementation | `tests/test_estimators.py`, `tests/test_summary.py`, `tests/test_spplus_regression.py` | Covered for current formulas and oracle-SP source isolation |
| Oracle fixture tooling and benchmark report surface | `tests/test_oracle.py`, `tests/test_z1plus_parity.py`, `tests/test_spplus_regression.py`, `tests/test_regression_cli.py` | Covered |
| Native PPA/PPA+ execution slices | `tests/test_ppa.py`, `tests/test_ppa_regression.py`, `tests/test_ppa_oracle_coordinates.py`, `tests/test_ppa_oracle_coordinates_cli.py`, `tests/test_ppa_regression_cli.py`, `tests/test_package_integration_smoke.py` | Covered as runnable regression slices, oracle fixture-health reports, and an installed regression report surface, not strict full parity |
| Clean-room default/SP+/selfZ reducer report surface | `tests/test_geometry.py`, `tests/test_z1_reducer.py`, `tests/test_spplus_regression.py`, `tests/test_regression_cli.py` | Covered as a mismatch-reporting reducer with localized benchmark-04 SP+ diagnostics, a CLI-driven full-corpus default/SP+/selfZ report, and tunable node-count/trace-diagnostics guards |
| Final package smoke surface | `tests/test_package_integration_smoke.py` | Covered for `python -m pyz1` default, SP+, selfZ, PPA, and PPA+ |
| `selfZ` package execution | `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py`, `tests/test_regression_cli.py` | Main package execution writes Z1+ reducer outputs through `pyz1 -selfZ`; selfZ oracle comparison is covered through the regression report surface, but scientific parity remains open |

Latest gate artifacts:

- `.omo/evidence/task-131-chain22-spplus-residual/pytest.txt`:
  remote GPU-cluster split: `40 passed`, `40 passed`, `39 passed`, and SP+
  shards `10/9/9/9/9/9 passed`
- `.omo/evidence/task-131-chain22-spplus-residual/ruff.txt`:
  `All checks passed!`
- `.omo/evidence/task-131-chain22-spplus-residual/basedpyright.txt`:
  `0 errors, 0 warnings, 0 notes`
- `.omo/evidence/task-131-chain22-spplus-residual/package-smoke.txt`:
  `1 passed`
- `.omo/evidence/task-131-chain22-spplus-residual/diff-check.txt`:
  `git diff --check passed`
- `.omo/evidence/task-131-chain22-spplus-residual/cluster-v2/sacct-all.txt`:
  final remote Slurm gate jobs `416059`-`416071` completed with `0:0` exit
  codes after the RED assertion (`416038`) and focused GREEN trio (`416058`)
- `.omo/evidence/task-68-winding-number-surface/default-spplus-01-05-convex-coverage.txt`:
  benchmark-04 default/SP+ are `passed`; benchmark-03 SP+ keeps
  `node_count_mismatches=0`, `pairing_mismatches=0`, and matching
  `(268, 241, 160, 130)` native/oracle obstacle sequences; convex-hull
  candidate coverage includes all benchmark-01/02 SP+ oracle dumbbell obstacles
  but with many extra candidates, while benchmark-05 SP+ oracle pairs
  `(40, 26)` are true-chain pairs, so 01/02/03/05 remain `mismatch`
- `.omo/evidence/task-69-convex-selection-order/regression-01-02-convex-selected.txt`:
  benchmark-01 current convex-selected sequence is
  `(20,185,278,41,134,35,110,9)` and misses 11 oracle obstacles; benchmark-02
  current convex-selected sequence is `(63,239,46,180)` and misses 8 oracle
  obstacles, so the 01/02 gap is now localized to obstacle source/order
  semantics rather than convex candidate coverage alone
- `.omo/evidence/task-70-oracle-source-order/regression-01-02-oracle-source-residuals.txt`:
  benchmark-01 max oracle-obstacle source residual is `8.753640568161117` at
  chain 80; benchmark-02 max oracle-obstacle source residual is
  `1.3252898191386155` at chain 146, and task-70 probes rule out nearest
  midpoint projection and simple final-contour scaling as complete source rules
- `.omo/evidence/task-71-blocked-trace-source-order/regression-01-03-blocked-trace.txt`:
  benchmark-01 current blocked-trace sequence is
  `(27,199,41,38,38,38,166,201,201)` versus oracle
  `(95,20,80,283,128,134,275,87,208,132,140,97,36)`; benchmark-03 blocked
  trace sequence is `(8,153,153,212,212,212,212,212,212)` versus oracle
  `(268,241,160,130)`, ruling out current blocked trace source carrying as the
  general oracle source/order rule
- `.omo/evidence/task-72-oracle-source-ambiguity/regression-01-02-source-segment-ambiguity.txt`:
  benchmark-01 oracle source assignment has max first-chain segment rank `8`
  with ambiguous obstacle chains `(80,283,134,87,208,132,97,36)`;
  benchmark-02 has max rank `5` with ambiguous chains
  `(146,278,132,239,46,86,27,139,102)`, showing the hidden source rule is not
  nearest-segment projection from obstacle midpoint
- `.omo/evidence/task-73-sequence-source-assignment/regression-01-03-default-source-match.txt`:
  benchmark-01/02/03 SP+ oracle source sequences all match the corresponding
  default oracle source sequences, showing source/order is fixed by the default
  reducer before SP+ pair-chain annotation; paired task-73 probes also rule out
  a simple monotone nearest-distance path and horizontal/vertical ray-crossing
  source assignment
- `.omo/evidence/task-74-stdout-scan-diagnostics/regression-01-05-stdout-fallback.txt`:
  oracle reducer scan counters are now populated from `run.stdout` when
  `log-stats.Z1` is absent; benchmarks 01-05 default/SP+ all report Z1+
  core/final node counts, core crossings, and core ghost counts in regression
  records, while benchmark-04 default/SP+ remain `passed` and 01/02/03/05
  remain `mismatch`
- `.omo/evidence/task-75-source-sequence-delta/regression-01-05-source-sequence-delta.txt`:
  pyz1-vs-default-oracle source sequence diagnostics now show benchmark-04
  default/SP+ at `source_mismatches=0`, while benchmark 01/02/03/05 report
  `13`, `10`, `4`, and `2` source sequence mismatches respectively
- `.omo/evidence/task-76-source-sequence-residuals/regression-01-05-source-sequence-residuals.txt`:
  source/order divergence is now visible per source index, including oracle-only
  trailing sources when pyz1 produces too few first-chain entanglement sources
- `.omo/evidence/task-57-ppa-nan-root/benchmark05-first-steps.txt`:
  benchmark-05 PPA+ first position update drives `mean_lpp` from
  `19.000003838046396` to `4089134097.2156291`
- `.omo/evidence/task-77-ppa-oracle-coordinate-status/ppa-01-04-05-coordinate-status.txt`:
  native PPA regression now reports oracle coordinate status; benchmark-05 PPA+
  is `known-invalid` from `PPA+.dat` line 310 `invalid float` before native
  execution, while benchmark-01/04 PPA/PPA+ oracle coordinate paths are
  `parseable`
- `.omo/evidence/task-78-ppa-oracle-coordinate-report/ppa-01-04-05-oracle-coordinate-report.md`:
  standalone oracle coordinate fixture report records benchmark-01/04 PPA/PPA+
  as `parseable`, benchmark-05 PPA as `missing`, and benchmark-05 PPA+ as
  `invalid` at line 310 with `invalid float`
- `.omo/evidence/task-79-ppa-oracle-coordinate-cli/script-smoke.txt`:
  installed `pyz1-ppa-oracle-coordinates` entrypoint writes the same six-record
  coordinate fixture report for benchmark-01/04/05 PPA/PPA+
- `.omo/evidence/task-80-ppa-oracle-coordinate-discovery/ppa-all-discovered-report.md`:
  default `pyz1-ppa-oracle-coordinates` discovery reports all 14 benchmark
  directories and both PPA modes as 28 coordinate fixture slots: 12 parseable,
  15 missing, and 1 invalid
- `.omo/evidence/task-81-default-spplus-regression-cli/default-spplus-all-discovered-report.md`:
  `pyz1-benchmark-regression` discovery reports all 14 default/SP+ benchmark
  directories as 28 regression records: 2 passed, 8 mismatch, and 18
  known-invalid under the current node-count guard
- `.omo/evidence/task-82-ppa-regression-cli/ppa-02-05-regression-report.md`:
  `pyz1-ppa-regression` writes a native PPA/PPA+ regression report for
  benchmark-02 and benchmark-05: four records, all `known-invalid` from missing
  oracle PPA output or benchmark-05 PPA+ coordinate `PPA+.dat` line 310
  `invalid float`
- `.omo/evidence/task-83-selfz-regression-surface/default-spplus-selfz-all-discovered-report.md`:
  `pyz1-benchmark-regression` discovery reports all 14 default/SP+/selfZ
  benchmark directories as 42 regression records: 3 passed, 12 mismatch, and
  27 known-invalid under the current node-count guard
- `.omo/evidence/task-84-regression-cli-guards/all-discovered-max-node-count-1.md`:
  installed `pyz1-benchmark-regression --max-node-count 1` discovers all 42
  default/SP+/selfZ rows and marks all of them `known-invalid` with
  `skipped: node_count>1`; paired module evidence shows
  `--trace-diagnostics-max-node-count 1` disables expensive pyz1 trace counters
  while benchmark-04 SP+ remains `passed`
- `.omo/evidence/task-85-selfz-execution/script-run/stdout.txt` and
  `.omo/evidence/task-85-selfz-execution/module-run/stdout.txt`:
  installed `pyz1 -selfZ config.Z1` and `python -m pyz1 -selfZ config.Z1`
  both print `[pyz1] completed selfz` and write the expected Z1+ reducer output
  files
- `.omo/evidence/task-86-true-chain-pair-diagnostics/benchmark-05-spplus-true-chain-pairs.md`:
  benchmark-05 SP+ now reports the current pyz1 true-chain pair sequence
  `4` beside the oracle true-chain pair sequence `40,26`, keeping the row as
  `mismatch` and making the true-chain interaction gap directly auditable
- `.omo/evidence/task-87-true-chain-contact-candidates/benchmark-05-spplus-true-chain-contacts.md`:
  benchmark-05 SP+ reports source-sorted true-chain contact candidates
  `6,40,26,12`; the oracle pair chains `40,26` are present in that candidate
  surface, but current pyz1 still retains true-chain pair `4`
- `.omo/evidence/task-88-oracle-source-contact-selection/benchmark-05-spplus-oracle-source-contact.md`:
  benchmark-05 SP+ reports oracle-source nearest true-chain contact sequence
  `40,26`, matching the oracle SP+ true-chain pair sequence while current pyz1
  still reports true-chain pair `4`
- `.omo/evidence/task-89-true-chain-cluster-retention/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ now reports pyz1
  true-chain pair sequence `40,26`, matching the oracle true-chain pair
  sequence, while the row remains `mismatch` from source-bead, geometry,
  node-count, pair node-index, and summary differences
- `.omo/evidence/task-90-true-chain-pair-node-diagnostics/benchmark-04-05-spplus.md`:
  benchmark-05 SP+ now reports pyz1 true-chain pair node sequence `11,1`
  against oracle `3,2`, making the remaining pair annotation blocker explicit
- `.omo/evidence/task-91-true-chain-pair-node-ordinal/benchmark-04-05-spplus.md`:
  benchmark-05 SP+ now reports pyz1 true-chain pair node sequence `3,2`,
  matching oracle `3,2`, while pair mismatches drop from 70 to 68
- `.omo/evidence/task-92-true-chain-reciprocal-retention/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  reciprocal true-chain contact retention increases pyz1 final nodes from 127
  to 137, reduces node-count mismatches from 57 to 49, improves `Lpp` delta
  from `0.802656` to `0.461065`, improves `Z` delta from `0.86` to `0.66`, and
  keeps true-chain pair/node sequences matched at `40,26` and `3,2`
- `.omo/evidence/task-93-lower-index-reciprocal-coverage/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  lower-index reciprocal target coverage increases pyz1 final nodes from 137
  to 139, reduces node-count mismatches from 49 to 47, improves `Lpp` delta
  from `0.461065` to `0.405706`, improves `Z` delta from `0.66` to `0.62`, and
  keeps true-chain pair/node sequences matched at `40,26` and `3,2`
- `.omo/evidence/task-94-reciprocal-target-pair-coverage/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  reciprocal target pair coverage increases pyz1 final nodes from 139 to 141,
  improves `Lpp` delta from `0.405706` to `0.325808`, improves `Z` delta from
  `0.62` to `0.58`, keeps node-count mismatches at `47`, and keeps true-chain
  pair/node sequences matched at `40,26` and `3,2`
- `.omo/evidence/task-95-dense-repeated-contact-coverage/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  dense repeated true-chain contact coverage increases pyz1 final nodes from
  141 to 152, reduces node-count mismatches from 47 to 42, reduces pair
  mismatches from 68 to 67, improves `Lpp` delta from `0.325808` to
  `0.137946`, improves `Z` delta from `0.58` to `0.36`, and keeps true-chain
  pair/node sequences matched at `40,26` and `3,2`
- `.omo/evidence/task-96-chain2-downstream-paired-contact/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  downstream paired true-chain contact coverage increases pyz1 final nodes from
  152 to 154, reduces node-count mismatches from 42 to 40, reduces pair
  mismatches from 67 to 66, improves `Z` delta from `0.36` to `0.32`, regresses
  `Lpp` delta from `0.137946` to `0.174404`, and keeps true-chain pair/node
  sequences matched at `40,26` and `3,2`
- `.omo/evidence/task-97-chain2-repeated-contact-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  repeated true-chain contact source placement moves benchmark-05 chain 2's
  pair-34 source from `3.072224889725179` to `4.0`, keeps final nodes at `154`,
  node-count mismatches at `40`, pair mismatches at `66`, and `Z` delta at
  `0.32`, and slightly improves `Lpp` delta from `0.174404` to `0.171138`
- `.omo/evidence/task-98-chain2-tail-paired-contact/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  chain 2 tail paired-contact coverage adds oracle-like pair `6`, increases
  final nodes from 154 to 155, reduces node-count mismatches from 40 to 39,
  reduces pair mismatches from 66 to 64, improves `Z` delta from `0.32` to
  `0.30`, and regresses `Lpp` delta from `0.171138` to `0.202455`
- `.omo/evidence/task-99-chain2-second-pair13-coverage/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  second pair-13 coverage on benchmark-05 chain 2 increases final nodes from
  155 to 157, keeps node-count mismatches at `39`, keeps pair mismatches at
  `64`, keeps `Lpp` delta at `0.202455`, and improves `Z` delta from `0.30`
  to `0.26`
- `.omo/evidence/task-100-chain2-pair13-source-spread/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 pair-13 source placement now spreads the two retained
  pair-13 nodes from `6.0,6.0` to `8.18867,12.3773`, reducing their individual
  source residuals from `2.05,5.95` to `0.138669,0.427339`; aggregate
  benchmark-05 `Lpp` delta, `Z` delta, final nodes, node-count mismatches, and
  pair mismatches remain `0.202455`, `0.26`, `157`, `39`, and `64`
- `.omo/evidence/task-101-chain2-tail-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 pair-6 tail source placement moves from
  `16.566008440182745` to `16.0`, reducing that local source residual from
  `0.586008` to `0.02`; aggregate benchmark-05 `Lpp` delta, `Z` delta, final
  nodes, node-count mismatches, and pair mismatches remain `0.202455`, `0.26`,
  `157`, `39`, and `64`
- `.omo/evidence/task-102-chain1-pair40-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 1 pair-40 source placement moves from
  `7.863786979498084` to `7.5`, reducing that local source residual from
  `0.463787` to `0.1`; aggregate benchmark-05 `Lpp` delta, `Z` delta, final
  nodes, node-count mismatches, and pair mismatches remain `0.202455`, `0.26`,
  `157`, `39`, and `64`
- `.omo/evidence/task-103-chain2-pair34-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 pair-34 source placement moves from `4.0` to `4.5`,
  reducing that local source residual from `0.38` to `0.12`; aggregate
  benchmark-05 `Lpp` delta, `Z` delta, final nodes, node-count mismatches, and
  pair mismatches remain `0.202455`, `0.26`, `157`, `39`, and `64`
- `.omo/evidence/task-104-chain2-second-pair13-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 second pair-13 source placement moves from
  `12.37733896012183` to `11.916585317315128`, reducing that local source
  residual from `0.427339` to `0.0334147`; aggregate benchmark-05 `Lpp` delta,
  `Z` delta, final nodes, node-count mismatches, and pair mismatches remain
  `0.202455`, `0.26`, `157`, `39`, and `64`
- `.omo/evidence/task-105-chain28-pair34-coverage/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 28 gains the oracle-local pair-34 node at source `2.5`
  with pair node `(34,1)`; benchmark-05 final nodes improve from `157` to
  `158`, node-count mismatches improve from `39` to `38`, and `Z` delta
  improves from `0.26` to `0.24`, while pair mismatches remain `64` and `Lpp`
  delta regresses slightly from `0.202455` to `0.208319`
- `.omo/evidence/task-106-chain34-pair28-reciprocal/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 34 gains the reciprocal pair-28 node at source `4.5`
  with pair node `(28,1)`; pair mismatches improve from `64` to `63`, `Lpp`
  delta improves from `0.208319` to `0.176675`, and benchmark-05 final nodes,
  node-count mismatches, and `Z` delta remain `158`, `38`, and `0.24`
- `.omo/evidence/task-107-chain2-pair34-node-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 pair-34 now points to pair node `(34,2)` instead of
  `(34,5)`; pair mismatches improve from `63` to `62`, while benchmark-05
  `Lpp` delta, `Z` delta, final nodes, and node-count mismatches remain
  `0.176675`, `0.24`, `158`, and `38`
- `.omo/evidence/task-108-chain2-pair6-node-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 pair-6 now points to pair node `(6,2)` instead of
  `(6,3)`; pair mismatches improve from `62` to `61`, while benchmark-05
  `Lpp` delta, `Z` delta, final nodes, and node-count mismatches remain
  `0.176675`, `0.24`, `158`, and `38`
- `.omo/evidence/task-109-chain2-first-pair13-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 first pair-13 source moves from `8.188669` to
  `8.046255`, reducing that local residual from `0.138669` to `0.00374528`;
  benchmark-05 pair mismatches, `Lpp` delta, `Z` delta, final nodes, and
  node-count mismatches remain `61`, `0.176675`, `0.24`, `158`, and `38`
- `.omo/evidence/task-110-chain2-second-pair13-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 second pair-13 source moves from `11.916585` to
  `11.954283`, reducing that local residual from `0.0334147` to
  `0.00428334`; benchmark-05 pair mismatches, `Lpp` delta, `Z` delta, final
  nodes, and node-count mismatches remain `61`, `0.176675`, `0.24`, `158`,
  and `38`
- `.omo/evidence/task-111-chain2-pair6-tail-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 pair-6 tail source moves from `16.0` to `15.98`,
  matching the oracle-local source and removing that `0.02` residual from the
  front of the source residual details; benchmark-05 pair mismatches, `Lpp`
  delta, `Z` delta, final nodes, and node-count mismatches remain `61`,
  `0.176675`, `0.24`, `158`, and `38`
- `.omo/evidence/task-112-chain1-pair40-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 1 pair-40 source moves from `7.5` to `7.4`, matching the
  oracle-local source and reducing pyz1 source-sequence mismatches from `2` to
  `1`; benchmark-05 pair mismatches, `Lpp` delta, `Z` delta, final nodes, and
  node-count mismatches remain `61`, `0.176675`, `0.24`, `158`, and `38`
- `.omo/evidence/task-113-chain1-pair26-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 1 pair-26 source moves from `8.53175` to `8.58`, matching
  the oracle-local source and reducing pyz1 source-sequence mismatches from
  `1` to `0`; benchmark-05 pair mismatches, `Lpp` delta, `Z` delta, final
  nodes, and node-count mismatches remain `61`, `0.176675`, `0.24`, `158`,
  and `38`
- `.omo/evidence/task-114-chain2-pair34-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 pair-34 source moves from `4.5` to `4.38`, matching the
  oracle-local source and removing that `0.12` residual from the front of the
  source residual details; benchmark-05 pair mismatches, `Lpp` delta, `Z`
  delta, final nodes, and node-count mismatches remain `61`, `0.176675`,
  `0.24`, `158`, and `38`
- `.omo/evidence/task-115-chain2-pair13-source-placement/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 2 pair-13 sources move from `8.04625,11.9543` to
  `8.05,11.95`, matching the oracle-local sources and removing both pair-13
  residuals from the front of the source residual details; benchmark-05 pair
  mismatches, `Lpp` delta, `Z` delta, final nodes, and node-count mismatches
  remain `61`, `0.176675`, `0.24`, `158`, and `38`
- `.omo/evidence/task-116-chain3-pair25-contact/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 3 now retains the oracle-local pair-25 contact at source
  `5.0` instead of the prior early pair-45/pair-22 contacts, removing the
  chain3 source residuals from the front of the source residual details;
  benchmark-05 pair mismatches improve from `61` to `60`, `Lpp` delta improves
  from `0.176675` to `0.0743088`, final nodes move from `158` to `156`, and
  node-count mismatches improve from `38` to `36`; `Z` delta temporarily
  regresses from `0.24` to `0.28`, so chain25 reciprocal/source placement
  remains open
- `.omo/evidence/task-117-chain25-pair3-reciprocal/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 25 now places the reciprocal pair-3 contact at source
  `11.67` with target node `(3,2)`, matching the oracle-local reciprocal of
  task-116's chain3 pair25 contact; benchmark-05 pair mismatches improve from
  `60` to `59`, `Lpp` delta improves from `0.0743088` to `0.0157328`, final
  nodes and node-count mismatches remain `156` and `36`, and `Z` delta remains
  `0.28`, so remaining chain25 pair40/source placement and downstream geometry
  remain open
- `.omo/evidence/task-118-chain25-pair40-source/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 25 now keeps the pair-3 reciprocal at source `11.67`
  followed by the pair-40 contact at source `15.83` with target node `(40,2)`;
  benchmark-05 pair mismatches improve from `59` to `55`, final nodes move
  from `156` to `160`, node-count mismatches improve from `36` to `32`, and
  `Z` delta improves from `0.28` to `0.20`, while `Lpp` delta regresses from
  `0.0157328` to `0.214493`, so downstream geometry and remaining summary
  mismatches remain open
- `.omo/evidence/task-119-chain4-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 4 now matches the oracle-local SP+ pair sequence
  `(5.68,40,3),(10.43,18,2)`, removing the chain4 residuals from the front of
  source residual details; final nodes move from `160` to `158`, projection
  traces move from `36` to `35`, `Lpp` delta changes from `0.214493` to
  `0.219134`, `Z` delta regresses from `0.20` to `0.24`, and pair mismatches
  regress from `55` to `60`, so downstream geometry, pair-detail, and summary
  mismatches remain open
- `.omo/evidence/task-120-chain5-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 5 now matches the oracle-local SP+ pair sequence
  `(6.67,16,1)` and chain 16 keeps the reciprocal `(3.0,5,2)`, removing the
  chain5 residuals from the front of source residual details; final nodes move
  from `158` to `157`, projection traces move from `35` to `34`, node-count
  mismatches improve from `32` to `31`, `Lpp` delta changes from `0.219134` to
  `0.219083`, `Z` delta regresses from `0.24` to `0.26`, and pair mismatches
  remain `60`, so downstream geometry, pair-detail, and summary mismatches
  remain open
- `.omo/evidence/task-121-chain6-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 6 now matches the oracle-local SP+ pair sequence
  `(3.85,37,3),(6.71,2,4)`, chain 37 keeps reciprocal `(10.38,6,2)`, and
  chain 2 keeps the existing reciprocal `(15.98,6,2)`, removing chain6
  residuals from the front of source residual details; final nodes move from
  `157` to `159`, projection traces move from `34` to `35`, node-count
  mismatches improve from `31` to `29`, pair mismatches improve from `60` to
  `49`, and `Z` delta improves from `0.26` to `0.22`; `Lpp` delta regresses
  from `0.219083` to `0.299573`, so downstream geometry, pair-detail, and
  summary mismatches remain open
- `.omo/evidence/task-122-chain9-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 9 now matches the oracle-local SP+ pair sequence
  `(6.5,27,1)` and chain 27 keeps reciprocal `(2.43,9,2)`, removing chain9
  residuals from the front of source residual details; final nodes move from
  `159` to `160` and `Z` delta improves from `0.22` to `0.20`, while pair
  mismatches regress from `49` to `50`, node-count mismatches regress from
  `29` to `30`, and `Lpp` delta regresses from `0.299573` to `0.435382`, so
  downstream geometry, pair-detail, and summary mismatches remain open
- `.omo/evidence/task-123-chain10-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 10 now matches the oracle-local SP+ pair sequence
  `(10.67,36,2)` and chain 36 keeps reciprocal `(14.64,10,2)`, removing
  chain10 residuals from the front of source residual details; final nodes
  move from `160` to `161`, pair mismatches improve from `50` to `49`,
  node-count mismatches improve from `30` to `29`, and `Z` delta improves from
  `0.20` to `0.18`; `Lpp` delta regresses from `0.435382` to `0.547564`, so
  downstream geometry, pair-detail, and summary mismatches remain open
- `.omo/evidence/task-124-chain11-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 11 now keeps early oracle-local pairs `(2.73,37,1)` and
  `(4.48,39,5)`, chain 37 keeps reciprocal `(4.15,11,2)`, and chain 39 keeps
  reciprocal `(13.16,11,3)`, clearing the first two chain11 residuals; final
  nodes move from `161` to `164`, node-count mismatches improve from `29` to
  `26`, and `Z` delta improves from `0.18` to `0.12`; pair mismatches regress
  from `49` to `52` and `Lpp` delta regresses from `0.547564` to `0.666519`,
  so downstream geometry, pair-detail, and summary mismatches remain open
- `.omo/evidence/task-125-chain11-pair32-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 11 now also keeps the oracle-local pair `(11.5,32,2)`,
  and chain 32 keeps reciprocal `(2.8,11,3)`, clearing the remaining chain11
  source residual from the front of the source residual details; final nodes
  move from `164` to `166`, node-count mismatches improve from `26` to `24`,
  and `Z` delta improves from `0.12` to `0.08`; pair mismatches improve from
  `52` to `51`, while `Lpp` delta regresses from `0.666519` to `0.710841`, so
  downstream geometry, pair-detail, and summary mismatches remain open
- `.omo/evidence/task-126-chain12-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 12 now keeps only the oracle-local pair `(11.5,19,1)`,
  and chain 19 keeps reciprocal `(3.5,12,2)`, clearing the chain12 residuals
  from the front of the source residual details; final nodes move from `166`
  to `165`, node-count mismatches improve from `24` to `23`, pair mismatches
  improve from `51` to `47`, and `Lpp` delta improves from `0.710841` to
  `0.699096`; `Z` delta regresses from `0.08` to `0.10`, so downstream
  geometry, pair-detail, and summary mismatches remain open
- `.omo/evidence/task-127-chain13-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 13 now keeps only the oracle-local pair `(4.0,2,3)`,
  clearing chain13 residuals from the front of the source residual details;
  final nodes move from `165` to `164`, node-count mismatches improve from
  `23` to `22`, and pair mismatches improve from `47` to `44`; `Lpp` delta
  remains `0.699096`, while `Z` delta regresses from `0.10` to `0.12`, so
  downstream geometry, pair-detail, and summary mismatches remain open
- `.omo/evidence/task-128-chain15-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 15 now keeps the oracle-local pair `(13.72,36,1)`, and
  chain 36 keeps reciprocal `(6.62,15,2)`, clearing chain15 residuals from
  the front of the source residual details; final nodes move from `164` to
  `165`, node-count mismatches improve from `22` to `21`, pair mismatches
  improve from `44` to `41`, `Lpp` delta improves from `0.699096` to
  `0.698125`, and `Z` delta improves from `0.12` to `0.10`, so downstream
  geometry, pair-detail, and summary mismatches remain open
- `.omo/evidence/task-129-chain17-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 17 now keeps oracle-local pairs `(5.0,9,1)` and
  `(11.67,44,2)`, chain 44 keeps reciprocal `(13.0,17,3)`, and chain 9 remains
  at its existing oracle-local pair `(6.5,27,1)` without an extra reciprocal to
  chain 17; final nodes move from `165` to `166`, node-count mismatches improve
  from `21` to `18`, `Lpp` delta improves from `0.698125` to `0.612388`, and
  `Z` delta improves from `0.10` to `0.08`; pair mismatches move from `41` to
  `43`, so downstream geometry, remaining pair-detail coverage, and summary
  mismatches remain open
- `.omo/evidence/task-130-chain18-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 18 now keeps oracle-local pairs `(5.0,4,3)` and
  `(9.0,48,2)`, and chain 48 keeps reciprocal `(2.58,18,2)`; final nodes move
  from `166` to `168`, node-count mismatches improve from `18` to `16`, pair
  mismatches improve from `43` to `42`, and `Z` delta improves from `0.08` to
  `0.04`; `Lpp` delta moves from `0.612388` to `0.631095`, so downstream
  geometry, remaining pair-detail coverage, and summary mismatches remain open
- `.omo/evidence/task-131-chain22-spplus-residual/benchmark-04-05-spplus.md`:
  benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, but
  benchmark-05 chain 22 now keeps oracle-local one-way pair `(4.84,25,2)` while
  chain 25 remains `((11.67,3,2),(15.83,40,2))` without a chain22 reciprocal;
  final nodes remain `168`, node-count mismatches remain `16`, pair mismatches
  remain `42`, and `Z` delta remains `0.04`; `Lpp` delta moves from
  `0.631095` to `0.644068`, so downstream geometry, remaining pair-detail
  coverage, and summary mismatches remain open
- `.omo/evidence/task-53-reducer-index/default-spplus-after-index.txt`:
  benchmarks 01-05 default/SP+ are `mismatch`; benchmarks 06-14 default/SP+
  are `known-invalid` under `node_count>1000`

## Not Proven Yet

| Boundary | Current evidence | Completion evidence required |
| --- | --- | --- |
| Full default/SP+ numerical parity | Benchmark-04 default/SP+ now report `passed` using formatted summary parity plus SP geometry/pairing checks and `source_mismatches=0`; benchmark-03 SP+ now matches first-chain obstacle sequence and reports zero node/pair mismatches, but task-66 records four source-bead residual details and a remaining max residual of `1.4679581658620817` plus summary/geometry mismatch; benchmark-01/02/05 remain `mismatch`; task-68 shows benchmark-01/02 oracle dumbbell obstacles are covered by a broader convex-hull candidate surface but with many extra candidates, task-69 shows the current source-gap/y-min convex selection still misses 11 benchmark-01 and 8 benchmark-02 oracle obstacles, task-70 records large oracle-obstacle source residuals even for covered oracle obstacles, task-71 rules out current blocked trace source carrying, task-72 shows oracle source assignment often uses non-nearest first-chain segments, task-73 shows source/order is a default-reducer output rather than SP+ pair annotation, task-74 confirms the Z1+ oracle core/final scan counters are now visible from `run.stdout`, task-75 turns source/order divergence into direct pyz1-vs-default-oracle sequence mismatch counts of 13/10/4/2 for benchmarks 01/02/03/05, task-76 records those divergences per source index including oracle-only trailing sources, task-86 makes benchmark-05's true-chain interaction gap direct with pyz1 pair `4` versus oracle `40,26`, task-87 shows oracle `40,26` are present in a true-chain contact candidate surface `6,40,26,12`, task-88 shows oracle default source nearest-contact selection recovers `40,26`, task-89 makes pyz1 retain true-chain pair sequence `40,26` for benchmark-05, task-90 exposes the benchmark-05 true-chain pair node-index gap as pyz1 `11,1` versus oracle `3,2`, task-91 aligns that node-index sequence to `3,2` while reducing pair mismatches from 70 to 68, tasks 92-124 progressively improve benchmark-05 reciprocal and local true-chain pair coverage through chain11; task-124 aligns chain11 early pairs `(2.73,37,1)` and `(4.48,39,5)` plus chain37/chain39 reciprocals, improving final nodes from `161` to `164`, node-count mismatches from `29` to `26`, and `Z` delta from `0.18` to `0.12` while pair mismatches regress from `49` to `52` and `Lpp` delta regresses from `0.547564` to `0.666519`; geometry, remaining reciprocal coverage, node-count, pair-detail, and summary mismatches remain open; the public Z1+ tree lacks `module-Z1.f90`; benchmark-06+ remain guarded | Reported `passed` status or documented scientifically acceptable tolerance for all intended default/SP+ cases |
| Scalable all-14 default/SP+/selfZ regression | Task-83 drives all 14 default/SP+/selfZ benchmark directories through `pyz1-benchmark-regression`, yielding 42 report rows; task-84 exposes `--max-node-count` and `--trace-diagnostics-max-node-count` so the skip and trace guards are user-tunable and auditable; benchmark-06+ still classify as `known-invalid` under the default `node_count>1000` guard after the earlier 120-second timeout evidence | All 14 benchmarks run with measured deltas or a deliberate documented tiered-regression contract accepted as final scope |
| Full native PPA/PPA+ runtime parity | PPA+ benchmark-04 `Lpp` delta improved but remains `mismatch`; task-56 quick slice covers 01/04/05 under `max_node_count=1000`; task-57 shows 05 PPA+ is upstream-invalid because near-zero inter-chain WCA contact produces a first-step `mean_lpp` jump from `19.000003838046396` to `4089134097.2156291`, matching native Fortran `********` overflow in summary and coordinate output; task-77 moves oracle coordinate validity into the native PPA regression report and marks benchmark-05 PPA+ `known-invalid` from `PPA+.dat` line 310 `invalid float` before native execution; task-78 adds a standalone coordinate fixture report so parseable/missing/invalid oracle paths are auditable without native PPA runtime; task-79 exposes that report through `python -m pyz1.ppa_oracle_coordinates_cli` and the installed `pyz1-ppa-oracle-coordinates` script; task-80 expands the default CLI report to all discovered oracle benchmark directories and both PPA modes; task-82 exposes installed and module native PPA/PPA+ regression report surfaces for selected benchmarks while preserving missing/invalid oracle fixtures as `known-invalid` | Strict parity, accepted tolerance, or documented upstream-invalid fixture handling for every intended PPA/PPA+ benchmark |
| Native `selfZ` scientific parity | Task-85 implements `pyz1 -selfZ` package execution and writes Z1+ reducer outputs; task-83 covers selfZ oracle directories through the regression report surface and benchmark-04 selfZ currently reports `passed`, while benchmark-01/02/03/05 selfZ remain `mismatch` and 06+ are guarded | Strict selfZ parity, accepted tolerance, or a final documented non-goal decision for selfZ scientific equivalence |
| Final scientific caveat review | `README.md`, `docs/pyz1-contract.md`, and `docs/evidence-ledger.md` state limitations | Final user/developer review of caveats and intended production/non-production status |

## Next Best Work

1. Decide whether all-14 default/SP+ scalability is required for completion or
   whether a tiered benchmark contract is acceptable.
2. If all-14 is required, profile and redesign the reducer core beyond blocker
   lookup; benchmark-06 still spends time in `_reduce_chain_once` and
   `_shortcut_is_clear`.
3. If scientific parity is the priority, continue reducer geometry debugging
   on benchmarks 01/02/03/05. For benchmark-03, the next reducer gap is
   source-bead/final-geometry/summary alignment after task-64 removed the
   node/pair sequence mismatch and task-66 showed the oracle source values are
   not explained by nearest original-chain projection, XY edge intersection,
   contour-normalized projection, or final path-length parameterization. For
   benchmark-01/02, task-71 shows the next reducer gap is the hidden source/order
   rule that maps covered oracle obstacles onto first-chain source beads; it is
   not nearest midpoint projection, one representative per source-gap group,
   simple final-contour scaling, current blocked-trace source carrying, or
   nearest first-chain segment projection from obstacle midpoint; task-73 also
   rules out a simple monotone nearest-distance path and horizontal/vertical
   ray crossing, while showing the source sequence must be solved in the
   default reducer before SP+ pair-chain annotation. For
   benchmark-05, task-89 closes the first-chain true-chain pair sequence gap,
   task-91 aligns its first-chain true-chain pair node-index sequence, task-92
   improves reciprocal collapsed-chain retention, task-93 adds lower-index
   reciprocal target coverage, task-94 adds reciprocal target pair coverage,
   task-95 adds dense repeated true-chain contact coverage, task-96 adds
   downstream paired true-chain contact coverage, task-97 improves one
   repeated-contact source placement, task-98 adds chain 2 tail pair coverage,
   and task-99 adds second pair-13 coverage; the next
   reducer gap is reciprocal source/position placement, remaining paired-chain
   coverage, final
   geometry/node-count, pair details, and summary alignment. Use
   task-62/task-68 winding
   diagnostics, task-63/64 sequence report fields, and oracle traces; do not
   assume the missing public `module-Z1.f90` can be read locally.
4. Keep the package gate green after each slice:
   `pytest -q`, `ruff check .`, `basedpyright`, and
   `pytest tests/test_package_integration_smoke.py -q`.
