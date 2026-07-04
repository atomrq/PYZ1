# pyz1 Completion Audit

This audit maps the active clean-room reproduction goal to current repo evidence.
It is a completion gate, not a parity claim.

Last audited: 2026-07-04.

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
| Oracle fixture tooling and benchmark report surface | `tests/test_oracle.py`, `tests/test_z1plus_parity.py`, `tests/test_spplus_regression.py` | Covered |
| Native PPA/PPA+ execution slices | `tests/test_ppa.py`, `tests/test_ppa_regression.py`, `tests/test_ppa_oracle_coordinates.py`, `tests/test_package_integration_smoke.py` | Covered as runnable regression slices and oracle fixture-health reports, not strict full parity |
| Clean-room default/SP+ reducer | `tests/test_geometry.py`, `tests/test_z1_reducer.py`, `tests/test_spplus_regression.py` | Covered as a mismatch-reporting reducer with localized benchmark-04 SP+ diagnostics |
| Final package smoke surface | `tests/test_package_integration_smoke.py` | Covered for `python -m pyz1` default, SP+, PPA, and PPA+ |
| Explicit unsupported `selfZ` behavior | `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py` | Covered as a not-implemented CLI boundary |

Latest gate artifacts:

- `.omo/evidence/task-78-ppa-oracle-coordinate-report/pytest.txt`:
  `130 passed`
- `.omo/evidence/task-78-ppa-oracle-coordinate-report/ruff.txt`:
  `All checks passed!`
- `.omo/evidence/task-78-ppa-oracle-coordinate-report/basedpyright.txt`:
  `0 errors, 0 warnings, 0 notes`
- `.omo/evidence/task-78-ppa-oracle-coordinate-report/package-smoke.txt`:
  `2 passed`
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
- `.omo/evidence/task-53-reducer-index/default-spplus-after-index.txt`:
  benchmarks 01-05 default/SP+ are `mismatch`; benchmarks 06-14 default/SP+
  are `known-invalid` under `node_count>1000`

## Not Proven Yet

| Boundary | Current evidence | Completion evidence required |
| --- | --- | --- |
| Full default/SP+ numerical parity | Benchmark-04 default/SP+ now report `passed` using formatted summary parity plus SP geometry/pairing checks and `source_mismatches=0`; benchmark-03 SP+ now matches first-chain obstacle sequence and reports zero node/pair mismatches, but task-66 records four source-bead residual details and a remaining max residual of `1.4679581658620817` plus summary/geometry mismatch; benchmark-01/02/05 remain `mismatch`; task-68 shows benchmark-01/02 oracle dumbbell obstacles are covered by a broader convex-hull candidate surface but with many extra candidates, task-69 shows the current source-gap/y-min convex selection still misses 11 benchmark-01 and 8 benchmark-02 oracle obstacles, task-70 records large oracle-obstacle source residuals even for covered oracle obstacles, task-71 rules out current blocked trace source carrying, task-72 shows oracle source assignment often uses non-nearest first-chain segments, task-73 shows source/order is a default-reducer output rather than SP+ pair annotation, task-74 confirms the Z1+ oracle core/final scan counters are now visible from `run.stdout`, task-75 turns source/order divergence into direct pyz1-vs-default-oracle sequence mismatch counts of 13/10/4/2 for benchmarks 01/02/03/05, and task-76 records those divergences per source index including oracle-only trailing sources; benchmark-05 oracle pairs are true-chain interactions outside dumbbell winding handling; the public Z1+ tree lacks `module-Z1.f90`; benchmark-06+ remain guarded | Reported `passed` status or documented scientifically acceptable tolerance for all intended default/SP+ cases |
| Scalable all-14 default/SP+ regression | Benchmark-06 still timed out at 120 seconds even with bounds index and trace diagnostics disabled | All 14 benchmarks run with measured deltas or a deliberate documented tiered-regression contract accepted as final scope |
| Full native PPA/PPA+ runtime parity | PPA+ benchmark-04 `Lpp` delta improved but remains `mismatch`; task-56 quick slice covers 01/04/05 under `max_node_count=1000`; task-57 shows 05 PPA+ is upstream-invalid because near-zero inter-chain WCA contact produces a first-step `mean_lpp` jump from `19.000003838046396` to `4089134097.2156291`, matching native Fortran `********` overflow in summary and coordinate output; task-77 moves oracle coordinate validity into the native PPA regression report and marks benchmark-05 PPA+ `known-invalid` from `PPA+.dat` line 310 `invalid float` before native execution; task-78 adds a standalone coordinate fixture report so parseable/missing/invalid oracle paths are auditable without native PPA runtime | Strict parity, accepted tolerance, or documented upstream-invalid fixture handling for every intended PPA/PPA+ benchmark |
| Native `selfZ` implementation | CLI fails explicitly with not-implemented | Implemented `selfZ` reducer behavior and oracle parity evidence, or a final documented non-goal decision |
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
   benchmark-05, task-68 shows the next reducer gap is true-chain interaction
   handling, not dumbbell winding selection. Use task-62/task-68 winding
   diagnostics, task-63/64 sequence report fields, and oracle traces; do not
   assume the missing public `module-Z1.f90` can be read locally.
4. Keep the package gate green after each slice:
   `pytest -q`, `ruff check .`, `basedpyright`, and
   `pytest tests/test_package_integration_smoke.py -q`.
