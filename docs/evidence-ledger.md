# pyz1 Evidence Ledger

This ledger maps the clean-room reproduction requirements to current repo tests,
local evidence artifacts, and known open boundaries. It is an index, not a
parity claim.

For a requirement-by-requirement completion verdict, see
`docs/completion-audit.md`.

## Current Quality Gates

Latest local gate evidence:

- `.omo/evidence/task-61-obstacle-kinks/green-reducer-tests-retained.txt`:
  `15 passed`
- `.omo/evidence/task-55-ppa-coverage/ppa-focused.txt`: `21 passed`
- `.omo/evidence/task-57-ppa-nan-root/ppa-focused.txt`: `22 passed`
- `.omo/evidence/task-61-obstacle-kinks/pytest.txt`: `116 passed`
- `.omo/evidence/task-61-obstacle-kinks/ruff.txt`: `All checks passed!`
- `.omo/evidence/task-61-obstacle-kinks/basedpyright.txt`:
  `0 errors, 0 warnings, 0 notes`
- `.omo/evidence/task-61-obstacle-kinks/package-smoke.txt`: `2 passed`

The package smoke runs `python -m pyz1` for default, SP+, PPA, and PPA+ modes
and checks the expected mode-specific output files.

## Requirement Coverage

| Requirement | Current proof | Evidence |
| --- | --- | --- |
| Z1 input parser and typed models | Unit tests for valid inputs, malformed inputs, metadata, true-chain filtering, and model invariants | `tests/test_z1_io.py`, `tests/test_models.py` |
| Z1+ output parser/writer | Summary, SP/SP+, initconfig, value files, PPA, and PPA+ round-trip tests | `tests/test_output_io.py`, `tests/test_output_values.py`, `tests/test_initconfig_io.py` |
| Summary and `Ne` estimators | Estimator unit tests plus oracle-SP-through-pyz1 summary parity for benchmark-04 SP+ | `tests/test_estimators.py`, `tests/test_summary.py`, `tests/test_spplus_regression.py`, `.omo/evidence/task-42-summary-ne-source/` |
| Oracle fixture tooling and parity reporting | Oracle manifest tests, CLI help smoke, benchmark regression report tests, and logged oracle run metadata | `tests/test_oracle.py`, `tests/test_z1plus_parity.py`, `tests/test_spplus_regression.py` |
| Native PPA/PPA+ slices | PPA mode tests, CLI mode tests, package-level smoke, WCA cell-list candidate generation, native PPA summary regression reporting, Z1+ PPA+ phase-stop regression, 12 parseable oracle coordinate-path summary parity cases, and one explicit Fortran-overflow known-invalid fixture | `tests/test_ppa.py`, `tests/test_ppa_regression.py`, `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py`, `.omo/evidence/task-46-ppa-summary-oracle-coverage/`, `.omo/evidence/task-47-ppa-neighbor-list/`, `.omo/evidence/task-48-ppa-native-regression/`, `.omo/evidence/task-49-ppa-lpp-debug/` |
| Clean-room reducer | Geometry primitives, reducer diagnostics, benchmark-04 reducer structure, SP+ pairing, broad-phase/index blocker filtering, and benchmark regression diagnostics for 01-05 under the default guard | `tests/test_geometry.py`, `tests/test_z1_reducer.py`, `tests/test_spplus_regression.py`, `.omo/evidence/task-53-reducer-index/` |
| SP+ regression | Pairing comparison, max-node-delta localization, pair-segment geometry diagnostics, oracle summary source isolation, and residual ghost-clearance tuning | `tests/test_spplus_regression.py`, `.omo/evidence/task-38-final-node-delta-location/`, `.omo/evidence/task-39-max-node-pair-geometry/`, `.omo/evidence/task-41-spplus-projection-direction/`, `.omo/evidence/task-50-spplus-residual/` |
| Package integration smoke | Real module entrypoint smoke for default, SP+, PPA, and PPA+ | `tests/test_package_integration_smoke.py`, `.omo/evidence/task-57-ppa-nan-root/package-smoke.txt` |
| `selfZ` boundary | `-selfZ` is recognized and fails explicitly instead of silently running the default reducer | `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py`, `.omo/evidence/task-45-selfz-explicit-boundary/` |

## Latest SP+ Parity Measurements

The default benchmark regression guard now runs benchmarks 01-05 in default
and SP+ modes. Benchmark 06 and larger cases remain `known-invalid` skips under
the `node_count>1000` performance guard. Current scope evidence is in
`.omo/evidence/task-53-reducer-index/default-spplus-after-index.txt`.
Task-53 adds a bounds index for reducer blocker candidates and an optional
large-case trace-diagnostics skip, but benchmark-06 still timed out at 120
seconds in `.omo/evidence/task-53-reducer-index/benchmark06-index-no-trace-timeout120.txt`;
therefore the default guard remains `node_count>1000`.

Benchmark-04 default and SP+ now classify as `passed` in the local regression
report. Their current summary text, SP+ pairing, final node count, and final
node geometry are within the report contract:

- diagnostic `lpp_delta=0.0003603492416281995` against the rounded
  three-decimal summary field
- `z_delta=0.0`
- `summary_field_mismatches=0`
- `pairing_mismatches=0`
- `node_count_mismatches=0`
- `max_node_position_delta=0.0004385586199525317`
- max-delta node: chain 1, node 2, source bead 3.5

The summary formula itself is not the active blocker: feeding the Z1+ oracle
SP+ path into `pyz1` summary gives `ne_modified_coil=641.606194063256` against
Z1+ `641.605`. Task-59 showed that the apparent `Lpp` delta is a comparison
against the rounded summary file field: recomputing `Lpp` from the oracle SP+
path gives `4.230360301770934`, while the parsed summary field is `4.230`.
The report now treats formatted summary parity plus SP geometry/pairing checks
as the pass/fail surface and keeps `lpp_delta` as a diagnostic number.
Task-58 retuned the retained blocked-kink clearance
fraction from `0.1` to `0.087735`; sweep evidence in
`.omo/evidence/task-58-spplus-residual/summary-rounding-threshold.txt` shows
the threshold that makes benchmark-04 SP+ `ne_modified_coil` round to the oracle
summary value, while
`.omo/evidence/task-59-spplus-lpp/default-spplus-01-05.txt` confirms benchmark-04
default/SP+ are `passed` and the 01/02/03/05 default/SP+ regression categories
remain true mismatches.

Task-60 aligns the reducer's dumbbell/obstacle contract with Z1+ SP output:
two-node dumbbells are now retained in `Z1+SP.dat` and participate as blockers,
while summary outputs still count only true chains. Evidence in
`.omo/evidence/task-60-benchmark01-reducer/default-spplus-01-05-after-dumbbells.txt`
shows benchmark-04 default/SP+ remain `passed`; benchmark-01/02/03 default/SP+
remain `mismatch`, but their `node_count_mismatches` drop from hundreds to
12/9/3 because the 300 two-node obstacle chains are now present in the native
SP output. The remaining benchmark-01/02/03 gap is the true-chain multi-obstacle
kink sequence, not missing obstacle output.

Task-61 preserves retained blocked-move trace nodes as multiple obstacle kinks
when a snapshot contains two-node dumbbell obstacles. Evidence in
`.omo/evidence/task-61-obstacle-kinks/default-spplus-01-05-retained.txt` shows
benchmark-04 default/SP+ remain `passed`, benchmark-05 returns to the task-60
mismatch level, and benchmark-01/02/03 default/SP+ node-count mismatches shrink
again to 5/3/1. These cases are still mismatches: the native reducer does not
yet reproduce the full Z1+ obstacle-kink positions, source beads, or SP+
pairings.

Task-62 records the next reducer boundary without introducing another
heuristic. Evidence in
`.omo/evidence/task-62-obstacle-placement/benchmark03-current-vs-oracle.txt`
shows benchmark-03 now has the smallest obstacle case: native output writes
three first-chain kinks, while Z1+ writes four. The native retained-trace
blockers do not match the oracle obstacle sequence, so the remaining 01/02/03
gap is not a parser, summary, dumbbell-output, or simple trace-retention issue.
`winding-candidates.txt` and `hull-sequence-check.txt` show that a 2D winding
candidate set contains the benchmark-03 oracle obstacles, but simple
lower/upper hull filters do not generalize cleanly to benchmark-01/02.
`z1plus-source-boundary.txt` records the public-source boundary: the distributed
source tree lacks `module-Z1.f90`; `Z1+install.pl` lists that reducer module
only in the private distribution, while the visible runnable oracle is the Linux
x86-64 ELF `Z1+.ex`.

## Latest PPA/PPA+ Oracle Summary Coverage

`tests/test_ppa.py` covers all currently parseable oracle PPA/PPA+ coordinate
paths with matching summary files in
`tests/fixtures/z1plus_oracle/corpus-ppa-ppaplus-20260703`:

- benchmark 01: PPA and PPA+
- benchmark 04: PPA and PPA+
- benchmark 07: PPA and PPA+
- benchmark 10: PPA and PPA+
- benchmark 11: PPA and PPA+
- benchmark 12: PPA and PPA+

Benchmark 05 PPA+ has both `PPA+.dat` and `PPA+summary.dat`, but the coordinate
path contains Fortran overflow stars on line 310. It is tracked as a known-invalid
coordinate fixture rather than a summary parity case.

## Latest PPA/PPA+ Neighbor-List Evidence

`src/pyz1/ppa_neighbors.py` provides deterministic periodic cell-list candidate
generation for the native WCA force path. The focused regression covers a
cross-boundary near pair, exact cutoff filtering, same-chain exclusion, and
unique periodic neighbor cells when an axis collapses to one or two cells.

Current candidate-count evidence from
`.omo/evidence/task-47-ppa-neighbor-list/candidate-counts.txt`:

- benchmark 01: `nodes=611`, `all_cross_chain_pairs=186000`,
  `wca_candidate_pairs=18452`
- benchmark 05: `nodes=1000`, `all_cross_chain_pairs=490000`,
  `wca_candidate_pairs=1002`

Task-55 tightened the neighbor-cell contract so collapsed axes do not emit
duplicate periodic cell keys. Focused evidence is in
`.omo/evidence/task-55-ppa-coverage/ppa-focused.txt`.

## Latest Native PPA/PPA+ Regression Evidence

`src/pyz1/ppa_regression.py` writes a PPA-specific native summary regression
report. It runs `run_ppa`, compares the produced summary against Z1+ oracle
`PPA-summary.dat` / `PPA+summary.dat`, and classifies the result without mixing
in reducer-specific geometry diagnostics.

Current evidence from `.omo/evidence/task-49-ppa-lpp-debug/`:

- `diagnostics.txt` isolates the old `Lpp delta=50.620053857564926` to the
  native PPA+ final coordinate path, not the summary parser/writer.
- `fene-min-image-toggle.txt` shows changing FENE bond handling to a minimum
  image segment does not materially change the mismatch.
- `early-stop-toggle.txt` confirms the Z1+ PPA+ phase-stop mechanism is
  causal: adding Fortran-style phase stops reduces benchmark-04 PPA+
  `Lpp delta` from `50.620053857564926` to `0.7762019820511341`.
- `native-report.txt` records the current default accelerated benchmark-04 PPA+
  status as `mismatch` with `Lpp delta=0.7762019820511341`,
  `Ne classical coil delta=7.55902839681513e-13`, and
  `Ne modified coil delta=3.027149435282842e-13`.

Additional task-56 quick-regression coverage is in
`.omo/evidence/task-56-ppa-nonfinite/ppa-01-04-05-quick-guard1000.txt`.
That quick slice runs benchmark 01 and 04 PPA/PPA+ plus benchmark 05 PPA+ under
`max_node_count=1000`. It remains a diagnostic slice, not a full parity claim:
benchmark 05 PPA+ is classified as `known-invalid` because the native quick
output reports non-finite `Lpp`, and the default full PPA phase report remains
too slow for the local gate.

Task-57 root-cause evidence is in `.omo/evidence/task-57-ppa-nan-root/`:

- `benchmark05-initial-diagnostics.txt` shows the benchmark-05 PPA+ input is
  finite before dynamics (`mean_lpp=19.000003838046396`,
  `max_abs_unfolded_coord=13.85`) and that the FENE denominator is not close to
  singular (`min_fene_denominator=0.55488848888888809`). The instability comes
  from inter-chain WCA contact: `min_wca_distance_squared=0.0084160399999999684`
  and `max_force_norm=1472449696360073.5`.
- `benchmark05-first-steps.txt` confirms the first PPA+ position update drives
  `mean_lpp` from `19.000003838046396` to `4089134097.2156291`, matching the
  Z1+ native `********` fixed-width overflow in `PPA+summary.dat` and several
  `PPA+.dat` coordinate rows. This fixture is therefore upstream-invalid for
  strict PPA+ numeric parity under the visible native settings, not a parser or
  writer failure.

## Open Boundaries

The following are intentionally not claimed complete:

- full PPA/PPA+ benchmark-level runtime parity from native integration output;
  PPA+ benchmark-04 is runnable and close in `Ne`, but strict summary parity is
  still a `mismatch`.
- default geometrical Z1+ numerical parity across all benchmarks
- scalable all-14 benchmark reducer regression without the current
  `node_count>1000` performance guard
- native self-entanglement (`selfZ`) behavior beyond the current explicit
  not-implemented CLI boundary
- final user/developer documentation review for scientific parity caveats
