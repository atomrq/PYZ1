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
| Native PPA/PPA+ execution slices | `tests/test_ppa.py`, `tests/test_ppa_regression.py`, `tests/test_package_integration_smoke.py` | Covered as runnable regression slices, not strict full parity |
| Clean-room default/SP+ reducer | `tests/test_geometry.py`, `tests/test_z1_reducer.py`, `tests/test_spplus_regression.py` | Covered as a mismatch-reporting reducer with localized benchmark-04 SP+ diagnostics |
| Final package smoke surface | `tests/test_package_integration_smoke.py` | Covered for `python -m pyz1` default, SP+, PPA, and PPA+ |
| Explicit unsupported `selfZ` behavior | `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py` | Covered as a not-implemented CLI boundary |

Latest gate artifacts:

- `.omo/evidence/task-69-convex-selection-order/pytest.txt`:
  `122 passed`
- `.omo/evidence/task-69-convex-selection-order/ruff.txt`:
  `All checks passed!`
- `.omo/evidence/task-69-convex-selection-order/basedpyright.txt`:
  `0 errors, 0 warnings, 0 notes`
- `.omo/evidence/task-69-convex-selection-order/package-smoke.txt`:
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
- `.omo/evidence/task-57-ppa-nan-root/benchmark05-first-steps.txt`:
  benchmark-05 PPA+ first position update drives `mean_lpp` from
  `19.000003838046396` to `4089134097.2156291`
- `.omo/evidence/task-53-reducer-index/default-spplus-after-index.txt`:
  benchmarks 01-05 default/SP+ are `mismatch`; benchmarks 06-14 default/SP+
  are `known-invalid` under `node_count>1000`

## Not Proven Yet

| Boundary | Current evidence | Completion evidence required |
| --- | --- | --- |
| Full default/SP+ numerical parity | Benchmark-04 default/SP+ now report `passed` using formatted summary parity plus SP geometry/pairing checks; benchmark-03 SP+ now matches first-chain obstacle sequence and reports zero node/pair mismatches, but task-66 records four source-bead residual details and a remaining max residual of `1.4679581658620817` plus summary/geometry mismatch; benchmark-01/02/05 remain `mismatch`; task-68 shows benchmark-01/02 oracle dumbbell obstacles are covered by a broader convex-hull candidate surface but with many extra candidates, and task-69 shows the current source-gap/y-min convex selection still misses 11 benchmark-01 and 8 benchmark-02 oracle obstacles; benchmark-05 oracle pairs are true-chain interactions outside dumbbell winding handling; the public Z1+ tree lacks `module-Z1.f90`; benchmark-06+ remain guarded | Reported `passed` status or documented scientifically acceptable tolerance for all intended default/SP+ cases |
| Scalable all-14 default/SP+ regression | Benchmark-06 still timed out at 120 seconds even with bounds index and trace diagnostics disabled | All 14 benchmarks run with measured deltas or a deliberate documented tiered-regression contract accepted as final scope |
| Full native PPA/PPA+ runtime parity | PPA+ benchmark-04 `Lpp` delta improved but remains `mismatch`; task-56 quick slice covers 01/04/05 under `max_node_count=1000`; task-57 shows 05 PPA+ is upstream-invalid because near-zero inter-chain WCA contact produces a first-step `mean_lpp` jump from `19.000003838046396` to `4089134097.2156291`, matching native Fortran `********` overflow in summary and coordinate output | Strict parity, accepted tolerance, or documented upstream-invalid fixture handling for every intended PPA/PPA+ benchmark |
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
   benchmark-01/02, task-69 shows the next reducer gap is source/order semantics
   for selecting multiple oracle obstacles from a broader convex-hull candidate
   surface, not one representative per source-gap group. For
   benchmark-05, task-68 shows the next reducer gap is true-chain interaction
   handling, not dumbbell winding selection. Use task-62/task-68 winding
   diagnostics, task-63/64 sequence report fields, and oracle traces; do not
   assume the missing public `module-Z1.f90` can be read locally.
4. Keep the package gate green after each slice:
   `pytest -q`, `ruff check .`, `basedpyright`, and
   `pytest tests/test_package_integration_smoke.py -q`.
