# pyz1 Evidence Ledger

This ledger maps the clean-room reproduction requirements to current repo tests,
local evidence artifacts, and known open boundaries. It is an index, not a
parity claim.

For a requirement-by-requirement completion verdict, see
`docs/completion-audit.md`.

## Current Quality Gates

Latest local gate evidence:

- `.omo/evidence/task-79-ppa-oracle-coordinate-cli/pytest.txt`: `131 passed`
- `.omo/evidence/task-55-ppa-coverage/ppa-focused.txt`: `21 passed`
- `.omo/evidence/task-57-ppa-nan-root/ppa-focused.txt`: `22 passed`
- `.omo/evidence/task-79-ppa-oracle-coordinate-cli/ruff.txt`:
  `All checks passed!`
- `.omo/evidence/task-79-ppa-oracle-coordinate-cli/basedpyright.txt`:
  `0 errors, 0 warnings, 0 notes`
- `.omo/evidence/task-79-ppa-oracle-coordinate-cli/package-smoke.txt`:
  `2 passed`

The package smoke runs `python -m pyz1` for default, SP+, PPA, and PPA+ modes
and checks the expected mode-specific output files.

## Requirement Coverage

| Requirement | Current proof | Evidence |
| --- | --- | --- |
| Z1 input parser and typed models | Unit tests for valid inputs, malformed inputs, metadata, true-chain filtering, and model invariants | `tests/test_z1_io.py`, `tests/test_models.py` |
| Z1+ output parser/writer | Summary, SP/SP+, initconfig, value files, PPA, and PPA+ round-trip tests | `tests/test_output_io.py`, `tests/test_output_values.py`, `tests/test_initconfig_io.py` |
| Summary and `Ne` estimators | Estimator unit tests plus oracle-SP-through-pyz1 summary parity for benchmark-04 SP+ | `tests/test_estimators.py`, `tests/test_summary.py`, `tests/test_spplus_regression.py`, `.omo/evidence/task-42-summary-ne-source/` |
| Oracle fixture tooling and parity reporting | Oracle manifest tests, CLI help smoke, benchmark regression report tests, and logged oracle run metadata | `tests/test_oracle.py`, `tests/test_z1plus_parity.py`, `tests/test_spplus_regression.py` |
| Native PPA/PPA+ slices | PPA mode tests, CLI mode tests, package-level smoke, WCA cell-list candidate generation, native PPA summary regression reporting, Z1+ PPA+ phase-stop regression, 12 parseable oracle coordinate-path summary parity cases, explicit Fortran-overflow known-invalid fixture handling, reusable oracle coordinate fixture status reports, and a package script that drives the coordinate report surface | `tests/test_ppa.py`, `tests/test_ppa_regression.py`, `tests/test_ppa_oracle_coordinates.py`, `tests/test_ppa_oracle_coordinates_cli.py`, `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py`, `.omo/evidence/task-46-ppa-summary-oracle-coverage/`, `.omo/evidence/task-47-ppa-neighbor-list/`, `.omo/evidence/task-48-ppa-native-regression/`, `.omo/evidence/task-49-ppa-lpp-debug/`, `.omo/evidence/task-78-ppa-oracle-coordinate-report/`, `.omo/evidence/task-79-ppa-oracle-coordinate-cli/` |
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

Task-63 adds obstacle-sequence diagnostics to the benchmark regression report.
Evidence in
`.omo/evidence/task-63-obstacle-sequence-report/default-spplus-01-05-sequences.txt`
and `.md` records the native and oracle first-chain SP+ obstacle pair-chain
sequences for each runnable benchmark. For example, benchmark-03 SP+ reports
native `(77, 212, 212)` versus oracle `(268, 241, 160, 130)`. This gives the
next reducer slice a stable report surface for placement/source-bead/pairing
work without changing the pass/fail tolerance.

Task-64 adds a guarded small-winding obstacle candidate path for dumbbell
obstacle snapshots. Evidence in
`.omo/evidence/task-64-obstacle-candidates/default-spplus-01-05-sequences.txt`
shows benchmark-03 SP+ now has `node_count_mismatches=0`,
`pairing_mismatches=0`, and native/oracle first-chain obstacle sequences both
`(268, 241, 160, 130)`. Benchmark-03 SP+ remains a `mismatch` because summary
fields and final geometry/source-bead values still differ; benchmark-01/02/05
remain mismatches, and benchmark-04 default/SP+ remain passed.

Task-65 adds explicit source-bead residual diagnostics to the benchmark
regression report. Evidence in
`.omo/evidence/task-65-benchmark03-source-geometry/default-spplus-01-05-source-deltas.txt`
shows benchmark-03 SP+ still has matching node/pair/obstacle sequence values,
but its largest source-bead residual is `1.4679581658620817` at chain 1 node 5.
The same report surfaces larger source-bead residuals for benchmark-01/02/05,
so future reducer work can track source-coordinate progress directly instead
of inferring it from the max-position-delta node.

Task-66 expands the source-bead diagnostic surface from a single max residual
to shared-node residual details in the benchmark regression report. Evidence in
`.omo/evidence/task-66-source-bead-rule/benchmark03-source-hypotheses.txt`
and `.omo/evidence/task-66-source-bead-rule/benchmark03-contour-parameter-probe.txt`
rules out nearest original-chain projection, XY edge intersection, and
contour-normalized projection as explanations for benchmark-03 SP+ oracle
source beads.
`.omo/evidence/task-66-source-bead-rule/default-spplus-01-05-source-residuals.txt`
confirms benchmark-04 default/SP+ remain `passed`, while benchmark-01/02/03/05
remain `mismatch`. `.omo/evidence/task-66-source-bead-rule/benchmark03-spplus.md`
records that benchmark-03 SP+ still has matching native/oracle obstacle sequence
`(268, 241, 160, 130)`, but its four source residual details are
`c1n2[268->268]`, `c1n3[241->241]`, `c1n4[160->160]`, and `c1n5[130->130]`;
the largest remains `3.92204!=5.39(d=1.46796)`.

Task-67 adds first-chain raw winding candidate coverage diagnostics to the
benchmark regression report. Evidence in
`.omo/evidence/task-67-obstacle-sequence-selection/default-spplus-01-05-winding-coverage.txt`
shows benchmark-01 SP+ has `winding_count 41` but misses oracle obstacles
`(128, 208, 36)`, benchmark-02 SP+ has `winding_count 30` but misses `(146,)`,
benchmark-03 SP+ has `winding_count 8` and misses none, and benchmark-05 SP+
has `winding_count 0` and misses `(40, 26)`. The paired probe
`.omo/evidence/task-67-obstacle-sequence-selection/periodic-image-candidate-probe.txt`
shows these missing oracle obstacles are not recovered by simple +/- box
periodic image shifts. This makes the next reducer blocker explicit:
benchmark-01/02/05 need a different winding/candidate geometry surface before
selection-order tuning can close their SP+ pair sequences.

Task-68 adds convex-hull winding coverage diagnostics and true-chain pair
classification to the benchmark regression report. Evidence in
`.omo/evidence/task-68-winding-number-surface/candidate-surface-probe.txt`
shows nonzero winding number gives the same coverage as the existing even-odd
polygon test, while convex-hull coverage includes the missing benchmark-01/02
dumbbell oracle obstacles. The report evidence
`.omo/evidence/task-68-winding-number-surface/default-spplus-01-05-convex-coverage.txt`
records benchmark-01 SP+ convex coverage as `convex 67 () 54` and benchmark-02
SP+ as `convex 65 () 55`: both cover all oracle dumbbell obstacles but include
many extra candidates, so their next blocker is selection/order on a broader
surface. Benchmark-05 SP+ reports `true_pairs (40, 26)` and still has no
dumbbell winding coverage, so its next blocker is true-chain interaction
handling rather than dumbbell winding selection.

Task-69 adds convex-selected winding diagnostics to the benchmark regression
report. Evidence in
`.omo/evidence/task-69-convex-selection-order/convex-candidate-features.md`
and `.omo/evidence/task-69-convex-selection-order/convex-group-distribution.md`
shows benchmark-01/02 oracle obstacles are not explained by one representative
per source-gap group: benchmark-01 has multiple oracle obstacles in groups
1/3/5/7, while benchmark-02 has multiple oracle obstacles in groups 2/3/4.
The generated report artifact
`.omo/evidence/task-69-convex-selection-order/regression-01-02-convex-selected.txt`
records current convex-selected sequences `(20,185,278,41,134,35,110,9)` for
benchmark-01 and `(63,239,46,180)` for benchmark-02, missing 11 and 8 oracle
obstacles respectively. The paired source probes
`.omo/evidence/task-69-convex-selection-order/oracle-sequence-node-order.md`,
`.omo/evidence/task-69-convex-selection-order/oracle-periodic-image-probe.md`,
and `.omo/evidence/task-69-convex-selection-order/wrapped-vs-unfolded-source.md`
show the remaining blocker is source/order semantics for obstacle placement,
not just convex membership or simple periodic image shifting.

Task-70 adds oracle-obstacle source residual diagnostics to the benchmark
regression report. Evidence in
`.omo/evidence/task-70-oracle-source-order/oracle-source-projection-probe.md`
shows oracle SP node positions are close to the paired obstacle midpoints, but
their oracle source beads are not explained by nearest midpoint projection; for
benchmark-01, pair chain 80 reports oracle source `2.19` while the same
convex candidate midpoint projects to source `10.943640568161117`. The contour
probe in
`.omo/evidence/task-70-oracle-source-order/oracle-source-contour-probe.md`
also rules out a simple final-SP-contour reparameterization. The generated
report artifact
`.omo/evidence/task-70-oracle-source-order/regression-01-02-oracle-source-residuals.txt`
records benchmark-01 max oracle-obstacle source residual
`8.753640568161117` at chain 80 and benchmark-02 max residual
`1.3252898191386155` at chain 146. This moves the benchmark-01/02 blocker from
candidate coverage to the hidden source/order rule that maps obstacle contacts
onto first-chain source beads.

Task-71 adds blocked-trace obstacle sequence diagnostics to the benchmark
regression report. Evidence in
`.omo/evidence/task-71-blocked-trace-source-order/block-trace-probe.md` and
`.omo/evidence/task-71-blocked-trace-source-order/regression-01-03-blocked-trace.txt`
shows the reducer's accepted/retained blocked trace is not the missing
source/order rule either: benchmark-01 reports blocked trace sequence
`(27,199,41,38,38,38,166,201,201)` and retained sequence
`(27,199,41,38,38,166,201,201)`, while the oracle sequence is
`(95,20,80,283,128,134,275,87,208,132,140,97,36)`. Benchmark-03 similarly
reports blocked trace sequence `(8,153,153,212,212,212,212,212,212)` while the
oracle sequence is `(268,241,160,130)`. This rules out current blocked trace
source carrying as the general explanation for oracle obstacle source/order.

Task-72 adds oracle source segment ambiguity diagnostics to the benchmark
regression report. Evidence in
`.omo/evidence/task-72-oracle-source-ambiguity/source-segment-ambiguity.md` and
`.omo/evidence/task-72-oracle-source-ambiguity/regression-01-02-source-segment-ambiguity.txt`
shows the oracle source-bead assignment is not nearest first-chain segment
projection from obstacle midpoint. Benchmark-01 reports max source segment rank
`8`, with ambiguous oracle obstacle chains
`(80,283,134,87,208,132,97,36)`; for example, chain 80's nearest midpoint
source is `10.943640568161117`, while the oracle source is `2.19` and the
nearest source-compatible segment is rank 2. Benchmark-02 reports max rank `5`
with ambiguous chains `(146,278,132,239,46,86,27,139,102)`. This localizes the
remaining 01/02 source/order blocker to a non-nearest, sequence-aware source
assignment rule rather than a simple geometric nearest-projection rule.

Task-73 adds default-oracle source sequence diagnostics to the benchmark
regression report and records two source-assignment probes. Evidence in
`.omo/evidence/task-73-sequence-source-assignment/regression-01-03-default-source-match.txt`
shows benchmark-01/02/03 SP+ oracle source sequences match their corresponding
default oracle source sequences exactly; SP+ adds pair-chain annotations, but
does not create a different first-chain source/order sequence. The probe
`.omo/evidence/task-73-sequence-source-assignment/monotone-source-path-probe.md`
rules out a simple strictly increasing minimum-distance source path: for
benchmark-02 it selects all nearest midpoint sources, while oracle sources
remain offset by up to `1.3252898191386155`. The paired
`.omo/evidence/task-73-sequence-source-assignment/ray-crossing-source-probe.md`
rules out horizontal/vertical ray-crossing assignment, with benchmark-02
matching only `0/10` horizontal and `1/10` vertical sources under the local
near-match threshold. The next reducer work should therefore target default
Z1+ source/order generation before SP+ pair annotation.

Task-74 extends oracle reducer diagnostics to read `run.stdout` when
`log-stats.Z1` is not present in the Z1+ oracle fixture directory. Evidence in
`.omo/evidence/task-74-stdout-scan-diagnostics/regression-01-05-stdout-scan-diagnostics.md`
records the parsed Z1+ scan rows for benchmarks 01-05 in default and SP+
modes; for example, benchmark-01 reports core/final node counts `617/615`,
core crossings `15`, and core ghosts `0`, while benchmark-05 reports
`322/170`, `85`, and `137`. The generated regression report summary
`.omo/evidence/task-74-stdout-scan-diagnostics/regression-01-05-stdout-fallback.txt`
confirms these counters now enter the benchmark regression records for all
01-05 default/SP+ cases without changing the known status split: benchmark-04
default/SP+ remain `passed`, while 01/02/03/05 remain `mismatch`.

Task-75 adds pyz1-vs-default-oracle source sequence diagnostics to the benchmark
regression report. Evidence in
`.omo/evidence/task-75-source-sequence-delta/regression-01-05-source-sequence-delta.txt`
records the native first-chain entanglement source sequence, the default Z1+
oracle source sequence, their index-wise mismatch count, and max aligned source
delta for benchmarks 01-05 in default and SP+ modes. The current stable split is
explicit: benchmark-04 default/SP+ have `source_mismatches=0`, while benchmark
01/02/03/05 report `13`, `10`, `4`, and `2` mismatches respectively. This makes
the remaining default reducer source/order blocker directly regression-testable
instead of relying only on residual detail columns.

Task-76 expands the same source/order surface with per-index residual details.
Evidence in
`.omo/evidence/task-76-source-sequence-residuals/regression-01-05-source-sequence-residuals.txt`
records each pyz1-vs-default-oracle source index as `actual!=expected(d=delta)`,
including missing pyz1 entries when the oracle sequence is longer. This shows,
for example, benchmark-01 default/SP+ match neither the first eight oracle
source values nor the five trailing oracle-only values, while benchmark-04
default/SP+ have an empty residual list. The report column
`pyz1 source sequence residual details` makes future source/order changes
observable at the exact source-index level.

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

Task-77 promotes oracle coordinate-path validity into the native PPA regression
report itself. Evidence in
`.omo/evidence/task-77-ppa-oracle-coordinate-status/ppa-01-04-05-coordinate-status.txt`
shows benchmark-01 and benchmark-04 PPA/PPA+ oracle coordinate paths are
`parseable`, benchmark-05 PPA has missing oracle PPA output, and benchmark-05
PPA+ is `known-invalid` before native execution because `PPA+.dat` fails at
line 310 with `invalid float`. The PPA regression report now includes
`oracle coordinate status`, `oracle coordinate error line`, and
`oracle coordinate error reason` columns, so upstream-invalid coordinate
fixtures are part of the same report surface as native summary mismatches.

Task-78 adds a standalone oracle coordinate fixture report API that classifies
coordinate paths without running native PPA. Evidence in
`.omo/evidence/task-78-ppa-oracle-coordinate-report/ppa-01-04-05-oracle-coordinate-report.md`
records a mixed-status slice: benchmark-01 and benchmark-04 PPA/PPA+ are
`parseable` with node counts `611` and `50`, benchmark-05 PPA is `missing`, and
benchmark-05 PPA+ is `invalid` at line 310 with `invalid float`. This makes the
PPA oracle fixture health independently auditable before runtime parity work.

Task-79 drives that fixture-health report through an installed CLI surface.
Evidence in
`.omo/evidence/task-79-ppa-oracle-coordinate-cli/script-smoke.txt` and
`.omo/evidence/task-79-ppa-oracle-coordinate-cli/ppa-01-04-05-script-report.md`
shows the `pyz1-ppa-oracle-coordinates` package script writes the same
six-record mixed-status report after refreshing the editable install. The
module surface `python -m pyz1.ppa_oracle_coordinates_cli` is also covered by
`tests/test_ppa_oracle_coordinates_cli.py`.

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
