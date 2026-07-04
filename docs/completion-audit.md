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

- `.omo/evidence/task-60-benchmark01-reducer/pytest.txt`: `115 passed`
- `.omo/evidence/task-60-benchmark01-reducer/ruff.txt`: `All checks passed!`
- `.omo/evidence/task-60-benchmark01-reducer/basedpyright.txt`:
  `0 errors, 0 warnings, 0 notes`
- `.omo/evidence/task-60-benchmark01-reducer/package-smoke.txt`: `2 passed`
- `.omo/evidence/task-60-benchmark01-reducer/default-spplus-01-05-after-dumbbells.txt`:
  benchmark-04 default/SP+ are `passed`; benchmarks 01/02/03/05 default/SP+
  remain `mismatch`; benchmark-01/02/03 now retain the 300 two-node obstacle
  chains in native SP output, reducing node-count mismatches to 12/9/3
- `.omo/evidence/task-57-ppa-nan-root/benchmark05-first-steps.txt`:
  benchmark-05 PPA+ first position update drives `mean_lpp` from
  `19.000003838046396` to `4089134097.2156291`
- `.omo/evidence/task-53-reducer-index/default-spplus-after-index.txt`:
  benchmarks 01-05 default/SP+ are `mismatch`; benchmarks 06-14 default/SP+
  are `known-invalid` under `node_count>1000`

## Not Proven Yet

| Boundary | Current evidence | Completion evidence required |
| --- | --- | --- |
| Full default/SP+ numerical parity | Benchmark-04 default/SP+ now report `passed` using formatted summary parity plus SP geometry/pairing checks; benchmarks 01/02/03/05 default/SP+ remain `mismatch`; benchmark-01/02/03 now preserve two-node obstacles in SP output but still miss the true-chain multi-obstacle kink sequences; benchmark-06+ remain guarded | Reported `passed` status or documented scientifically acceptable tolerance for all intended default/SP+ cases |
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
   on benchmarks 01/02/03/05. For benchmark-01/02/03, the next reducer gap is
   true-chain multi-obstacle kink preservation after the two-node obstacle
   output contract was aligned with Z1+.
4. Keep the package gate green after each slice:
   `pytest -q`, `ruff check .`, `basedpyright`, and
   `pytest tests/test_package_integration_smoke.py -q`.
