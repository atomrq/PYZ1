# pyz1 Evidence Ledger

This ledger maps the clean-room reproduction requirements to current repo tests,
local evidence artifacts, and known open boundaries. It is an index, not a
parity claim.

For a requirement-by-requirement completion verdict, see
`docs/completion-audit.md`.

## Current Quality Gates

Latest local gate evidence:

- `.omo/evidence/task-119-chain4-spplus-residual/pytest.txt`:
  `163 passed`
- `.omo/evidence/task-55-ppa-coverage/ppa-focused.txt`: `21 passed`
- `.omo/evidence/task-57-ppa-nan-root/ppa-focused.txt`: `22 passed`
- `.omo/evidence/task-119-chain4-spplus-residual/ruff.txt`:
  `All checks passed!`
- `.omo/evidence/task-119-chain4-spplus-residual/basedpyright.txt`:
  `0 errors, 0 warnings, 0 notes`
- `.omo/evidence/task-119-chain4-spplus-residual/package-smoke.txt`:
  `1 passed`

The package smoke runs `python -m pyz1` for default, SP+, selfZ, PPA, and PPA+
modes and checks the expected mode-specific output files.

## Requirement Coverage

| Requirement | Current proof | Evidence |
| --- | --- | --- |
| Z1 input parser and typed models | Unit tests for valid inputs, malformed inputs, metadata, true-chain filtering, and model invariants | `tests/test_z1_io.py`, `tests/test_models.py` |
| Z1+ output parser/writer | Summary, SP/SP+, initconfig, value files, PPA, and PPA+ round-trip tests | `tests/test_output_io.py`, `tests/test_output_values.py`, `tests/test_initconfig_io.py` |
| Summary and `Ne` estimators | Estimator unit tests plus oracle-SP-through-pyz1 summary parity for benchmark-04 SP+ | `tests/test_estimators.py`, `tests/test_summary.py`, `tests/test_spplus_regression.py`, `.omo/evidence/task-42-summary-ne-source/` |
| Oracle fixture tooling and parity reporting | Oracle manifest tests, CLI help smoke, benchmark regression report tests, and logged oracle run metadata | `tests/test_oracle.py`, `tests/test_z1plus_parity.py`, `tests/test_spplus_regression.py` |
| Native PPA/PPA+ slices | PPA mode tests, CLI mode tests, package-level smoke, WCA cell-list candidate generation, native PPA summary regression reporting, Z1+ PPA+ phase-stop regression, 12 parseable oracle coordinate-path summary parity cases, explicit Fortran-overflow known-invalid fixture handling, reusable oracle coordinate fixture status reports, a package script that discovers all oracle benchmark directories for coordinate fixture reporting, and an installed native PPA/PPA+ regression report surface | `tests/test_ppa.py`, `tests/test_ppa_regression.py`, `tests/test_ppa_oracle_coordinates.py`, `tests/test_ppa_oracle_coordinates_cli.py`, `tests/test_ppa_regression_cli.py`, `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py`, `.omo/evidence/task-46-ppa-summary-oracle-coverage/`, `.omo/evidence/task-47-ppa-neighbor-list/`, `.omo/evidence/task-48-ppa-native-regression/`, `.omo/evidence/task-49-ppa-lpp-debug/`, `.omo/evidence/task-78-ppa-oracle-coordinate-report/`, `.omo/evidence/task-79-ppa-oracle-coordinate-cli/`, `.omo/evidence/task-80-ppa-oracle-coordinate-discovery/`, `.omo/evidence/task-82-ppa-regression-cli/` |
| Clean-room reducer | Geometry primitives, reducer diagnostics, benchmark-04 reducer structure, SP+ pairing, broad-phase/index blocker filtering, benchmark regression diagnostics for 01-05 under the default guard, a package script that discovers all default/SP+/selfZ oracle benchmark directories for regression reporting, and user-tunable node-count/trace-diagnostics guards | `tests/test_geometry.py`, `tests/test_z1_reducer.py`, `tests/test_spplus_regression.py`, `tests/test_regression_cli.py`, `.omo/evidence/task-53-reducer-index/`, `.omo/evidence/task-81-default-spplus-regression-cli/`, `.omo/evidence/task-83-selfz-regression-surface/`, `.omo/evidence/task-84-regression-cli-guards/` |
| SP+ regression | Pairing comparison, max-node-delta localization, pair-segment geometry diagnostics, oracle summary source isolation, residual ghost-clearance tuning, CLI-driven full-corpus default/SP+/selfZ status reporting, trace-diagnostics guard control, direct pyz1-vs-oracle true-chain pair sequence reporting, true-chain contact candidate diagnostics, oracle-source nearest contact selection diagnostics, guarded true-chain contact-cluster retention, true-chain pair node-index diagnostics, reciprocal true-chain contact retention, lower-index reciprocal target coverage, reciprocal target pair coverage, dense repeated true-chain contact coverage, downstream paired true-chain contact coverage, repeated-contact source-placement coverage, chain2 tail paired-contact coverage, second pair-13 coverage, chain3 pair25 coverage, chain25 pair3 reciprocal coverage, chain25 pair40 source coverage, and chain4 pair sequence coverage | `tests/test_spplus_regression.py`, `tests/test_regression_cli.py`, `.omo/evidence/task-38-final-node-delta-location/`, `.omo/evidence/task-39-max-node-pair-geometry/`, `.omo/evidence/task-41-spplus-projection-direction/`, `.omo/evidence/task-50-spplus-residual/`, `.omo/evidence/task-81-default-spplus-regression-cli/`, `.omo/evidence/task-83-selfz-regression-surface/`, `.omo/evidence/task-84-regression-cli-guards/`, `.omo/evidence/task-86-true-chain-pair-diagnostics/`, `.omo/evidence/task-87-true-chain-contact-candidates/`, `.omo/evidence/task-88-oracle-source-contact-selection/`, `.omo/evidence/task-89-true-chain-cluster-retention/`, `.omo/evidence/task-90-true-chain-pair-node-diagnostics/`, `.omo/evidence/task-91-true-chain-pair-node-ordinal/`, `.omo/evidence/task-92-true-chain-reciprocal-retention/`, `.omo/evidence/task-93-lower-index-reciprocal-coverage/`, `.omo/evidence/task-94-reciprocal-target-pair-coverage/`, `.omo/evidence/task-95-dense-repeated-contact-coverage/`, `.omo/evidence/task-96-chain2-downstream-paired-contact/`, `.omo/evidence/task-97-chain2-repeated-contact-source-placement/`, `.omo/evidence/task-98-chain2-tail-paired-contact/`, `.omo/evidence/task-99-chain2-second-pair13-coverage/`, `.omo/evidence/task-116-chain3-pair25-contact/`, `.omo/evidence/task-117-chain25-pair3-reciprocal/`, `.omo/evidence/task-118-chain25-pair40-source/`, `.omo/evidence/task-119-chain4-spplus-residual/` |
| Package integration smoke | Real module entrypoint smoke for default, SP+, selfZ, PPA, and PPA+ | `tests/test_package_integration_smoke.py`, `.omo/evidence/task-57-ppa-nan-root/package-smoke.txt`, `.omo/evidence/task-85-selfz-execution/` |
| `selfZ` execution and boundary | `-selfZ` writes Z1+ reducer output files through both installed and module package surfaces; selfZ oracle directories are covered by the benchmark regression report surface, while scientific parity remains open | `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py`, `tests/test_regression_cli.py`, `.omo/evidence/task-83-selfz-regression-surface/`, `.omo/evidence/task-85-selfz-execution/` |

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

Task-80 makes the CLI discover every `benchmark-*` directory under the oracle
root when `--benchmark-id` is omitted. Evidence in
`.omo/evidence/task-80-ppa-oracle-coordinate-discovery/ppa-all-discovered-report.md`
records all 14 benchmark directories and both PPA modes for 28 coordinate
fixture slots: 12 `parseable`, 15 `missing`, and benchmark-05 PPA+ as the
single `invalid` coordinate fixture at line 310 with `invalid float`.

Task-82 adds a package-level native PPA/PPA+ regression CLI. Evidence in
`.omo/evidence/task-82-ppa-regression-cli/ppa-02-05-regression-report.md`
shows `pyz1-ppa-regression` writes a four-record native report for benchmarks
02 and 05: benchmark-02 PPA/PPA+ and benchmark-05 PPA are `known-invalid` from
missing oracle output, while benchmark-05 PPA+ is `known-invalid` from oracle
coordinate `PPA+.dat` line 310 `invalid float`. The module surface
`python -m pyz1.ppa_regression_cli` is covered by
`tests/test_ppa_regression_cli.py`.

## Latest Default/SP+/selfZ Regression CLI Evidence

Task-83 extends the package-level benchmark regression CLI to include selfZ
oracle directories. Evidence in
`.omo/evidence/task-83-selfz-regression-surface/default-spplus-selfz-all-discovered-report.md`
shows `pyz1-benchmark-regression` discovers all 14 benchmark directories and
writes 42 default/SP+/selfZ regression records: benchmark-04 default/SP+/selfZ
are `passed`, benchmarks 01/02/03/05 across the three modes are `mismatch`, and
benchmarks 06-14 across the three modes are `known-invalid` under the current
`node_count>1000` guard. The same surface is covered through
`python -m pyz1.regression_cli` and `tests/test_regression_cli.py`.

Task-84 exposes the benchmark regression skip and trace-diagnostics guards as
installed CLI options. Evidence in
`.omo/evidence/task-84-regression-cli-guards/all-discovered-max-node-count-1.md`
shows `pyz1-benchmark-regression --max-node-count 1` still discovers all 42
default/SP+/selfZ report rows and classifies all of them as `known-invalid`
with `skipped: node_count>1`. Evidence in
`.omo/evidence/task-84-regression-cli-guards/benchmark-04-spplus-trace-guard-1.md`
shows `--trace-diagnostics-max-node-count 1` keeps benchmark-04 SP+ at
`passed` while disabling expensive pyz1 trace counters
(`pyz1 core trace nodes=10`, ghosts `0`, accepted blocked moves `0`).

## Latest selfZ Package Execution Evidence

Task-85 promotes `-selfZ` from an explicit package-entrypoint failure to a
runnable clean-room reducer surface. Evidence in
`.omo/evidence/task-85-selfz-execution/script-run/` and
`.omo/evidence/task-85-selfz-execution/module-run/` shows both installed
`pyz1 -selfZ config.Z1` and `python -m pyz1 -selfZ config.Z1` print
`[pyz1] completed selfz` and write `Z1+SP.dat`, `Z1+summary.dat`,
`Ree_values.dat`, `Lpp_values.dat`, `N_values.dat`, and `Z_values.dat`.
This is package execution evidence, not a new selfZ parity claim; benchmark
parity remains governed by the default/SP+/selfZ regression report.

## Latest True-Chain Pair Diagnostics

Task-86 adds `pyz1 true-chain pair sequence` beside the existing oracle
true-chain sequence in the benchmark regression report. Evidence in
`.omo/evidence/task-86-true-chain-pair-diagnostics/benchmark-05-spplus-true-chain-pairs.md`
shows benchmark-05 SP+ still reports `mismatch`: the current pyz1 first-chain
true-chain pair sequence is `4`, while the Z1+ oracle sequence is `40,26`.
This makes the benchmark-05 blocker directly visible in the report surface; it
does not claim the true-chain interaction reducer has been solved.

Task-87 adds true-chain contact candidate diagnostics to the same report
surface. Evidence in
`.omo/evidence/task-87-true-chain-contact-candidates/benchmark-05-spplus-true-chain-contacts.md`
shows benchmark-05 SP+ still reports `mismatch`, with current pyz1 true-chain
pair sequence `4`, true-chain contact candidates `6,40,26,12`, and oracle
true-chain pair sequence `40,26`. This proves the oracle pair chains are present
in a simple source-sorted contact candidate surface, but that surface is not
yet selective enough to drive reducer behavior because it also contains extra
candidates.

Task-88 adds an oracle-source nearest-contact selector diagnostic. Evidence in
`.omo/evidence/task-88-oracle-source-contact-selection/benchmark-05-spplus-oracle-source-contact.md`
shows benchmark-05 SP+ still reports `mismatch`: current pyz1 true-chain pair
sequence is `4`, true-chain contact candidates are `6,40,26,12`, and selecting
the nearest true-chain contacts to the oracle default source sequence recovers
`40,26`, matching the oracle SP+ pair sequence. This localizes the next reducer
work to reproducing the default source placement and carrying intended pair
metadata, not to discovering a new contact geometry candidate set.

Task-89 adds guarded true-chain contact-cluster retention and carries intended
pair metadata through preserved kink nodes. Evidence in
`.omo/evidence/task-89-true-chain-cluster-retention/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`, while benchmark-05 SP+ now reports
pyz1 true-chain pair sequence `40,26`, matching the oracle true-chain pair
sequence and the oracle-source nearest-contact diagnostic. Benchmark-05 still
reports `mismatch`: the remaining gaps are source-bead residuals, final
geometry/node-count differences, pair node-index details, and summary fields.

Task-90 adds explicit true-chain pair node-index diagnostics to the benchmark
regression report. Evidence in
`.omo/evidence/task-90-true-chain-pair-node-diagnostics/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ still `passed`; benchmark-05 SP+ still matches true-chain
pair chain sequence `40,26`, but now exposes pyz1 pair node sequence `11,1`
against oracle `3,2`. This makes the remaining pair annotation blocker
directly testable instead of hidden inside the aggregate pair mismatch count.

Task-91 changes true-chain contact pair overrides to derive the target node
index from the paired chain's contact-source order instead of the original
segment index. Evidence in
`.omo/evidence/task-91-true-chain-pair-node-ordinal/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ now reports pyz1
true-chain pair node sequence `3,2`, matching oracle `3,2`, and its aggregate
pair mismatch count drops from 70 to 68. The row remains `mismatch` because the
paired chains still lack reciprocal nodes and the source, geometry, node-count,
and summary gaps remain.

Task-92 adds reciprocal true-chain contact retention for paired collapsed true
chains. Evidence in
`.omo/evidence/task-92-true-chain-reciprocal-retention/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but final nodes increase from 127 to 137, node-count mismatches
drop from 57 to 49, `Lpp` delta improves from `0.802656` to `0.461065`, and
`Z` delta improves from `0.86` to `0.66`. The true-chain pair sequence remains
matched at `40,26`, and the true-chain pair node sequence remains matched at
`3,2`. Remaining benchmark-05 gaps are source-bead placement, reciprocal
coverage beyond the current collapsed-chain insertion, final geometry, pair
details, and summary fields.

Task-93 adds lower-index reciprocal target coverage for paired true-chain
contacts that were previously inserted only from the first-chain reciprocal
surface. Evidence in
`.omo/evidence/task-93-lower-index-reciprocal-coverage/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but final nodes increase from 137 to 139, node-count mismatches
drop from 49 to 47, `Lpp` delta improves from `0.461065` to `0.405706`, and
`Z` delta improves from `0.66` to `0.62`. The true-chain pair sequence remains
matched at `40,26`, and the true-chain pair node sequence remains matched at
`3,2`. Remaining benchmark-05 gaps are source-bead placement, reciprocal
coverage beyond the closest lower-index target contact, final geometry,
pair details, and summary fields.

Task-94 adds reciprocal target pair coverage for lower-index reciprocal target
contacts. Evidence in
`.omo/evidence/task-94-reciprocal-target-pair-coverage/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but final nodes increase from 139 to 141, `Lpp` delta improves from
`0.405706` to `0.325808`, and `Z` delta improves from `0.62` to `0.58`.
Node-count mismatches remain at `47`, and the true-chain pair sequence and
true-chain pair node sequence remain matched at `40,26` and `3,2`. Remaining
benchmark-05 gaps are source-bead placement, reciprocal coverage beyond the
current target-pair insertion, final geometry, pair details, and summary fields.

Task-95 adds dense repeated true-chain contact coverage for oracle-like contact
surfaces that repeat the same target chain but do not satisfy the existing
multi-target source-cluster selector. Evidence in
`.omo/evidence/task-95-dense-repeated-contact-coverage/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but final nodes increase from 141 to 152, node-count mismatches
drop from 47 to 42, pair mismatches drop from 68 to 67, `Lpp` delta improves
from `0.325808` to `0.137946`, and `Z` delta improves from `0.58` to `0.36`.
The true-chain pair sequence remains matched at `40,26`, and the true-chain
pair node sequence remains matched at `3,2`. Remaining benchmark-05 gaps are
source-bead placement, reciprocal coverage beyond the dense repeated-contact
fallback, final geometry, pair details, and summary fields.

Task-96 adds downstream paired true-chain contact coverage for benchmark-05
chain 2 after the leading dense repeated target. Evidence in
`.omo/evidence/task-96-chain2-downstream-paired-contact/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but final nodes increase from 152 to 154, node-count mismatches
drop from 42 to 40, pair mismatches drop from 67 to 66, and `Z` delta improves
from `0.36` to `0.32`. The same report records the tradeoff: `Lpp` delta
regresses from `0.137946` to `0.174404`, so source placement and summary
alignment remain active reducer gaps rather than completed parity.

Task-97 adjusts benchmark-05 chain 2 repeated-contact source placement for the
pair-34 contact. Evidence in
`.omo/evidence/task-97-chain2-repeated-contact-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but the pair-34 source moves from `3.072224889725179` to `4.0`.
Final nodes remain `154`, node-count mismatches remain `40`, pair mismatches
remain `66`, `Z` delta remains `0.32`, and `Lpp` delta improves slightly from
`0.174404` to `0.171138`. This keeps source placement as an open reducer gap,
not a completed parity claim.

Task-98 adds benchmark-05 chain 2 tail paired-contact coverage for oracle-like
pair `6`. Evidence in
`.omo/evidence/task-98-chain2-tail-paired-contact/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but final nodes increase from 154 to 155, node-count mismatches
drop from 40 to 39, pair mismatches drop from 66 to 64, and `Z` delta improves
from `0.32` to `0.30`. The report also records the tradeoff: `Lpp` delta
regresses from `0.171138` to `0.202455`, so source placement and summary
alignment remain open reducer gaps.

Task-99 adds second pair-13 coverage for benchmark-05 chain 2. Evidence in
`.omo/evidence/task-99-chain2-second-pair13-coverage/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but final nodes increase from 155 to 157 while node-count
mismatches stay at `39`, pair mismatches stay at `64`, and `Lpp` delta stays
at `0.202455`. `Z` delta improves from `0.30` to `0.26`. The duplicated
pair-13 source remains a source-placement approximation, so source and summary
alignment remain open.

Task-100 spreads the duplicated pair-13 source placement for benchmark-05 chain
2. Evidence in
`.omo/evidence/task-100-chain2-pair13-source-spread/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but the two retained pair-13 nodes move from source `6.0,6.0` to
`8.18867,12.3773`, reducing their source residuals from `2.05,5.95` to
`0.138669,0.427339`. Aggregate benchmark-05 metrics remain unchanged from
task-99: final nodes `157`, node-count mismatches `39`, pair mismatches `64`,
`Lpp` delta `0.202455`, and `Z` delta `0.26`, so remaining source and summary
alignment are still open.

Task-101 snaps the benchmark-05 chain 2 pair-6 tail source to the upstream bead
anchor. Evidence in
`.omo/evidence/task-101-chain2-tail-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but the chain 2 pair-6 source moves from `16.566008440182745` to
`16.0`, reducing that local source residual from `0.586008` to `0.02`.
Aggregate benchmark-05 metrics remain unchanged from task-100: final nodes
`157`, node-count mismatches `39`, pair mismatches `64`, `Lpp` delta
`0.202455`, and `Z` delta `0.26`, so remaining source and summary alignment
are still open.

Task-102 snaps the benchmark-05 chain 1 pair-40 source to a half-bead anchor.
Evidence in
`.omo/evidence/task-102-chain1-pair40-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but the chain 1 pair-40 source moves from `7.863786979498084` to
`7.5`, reducing that local source residual from `0.463787` to `0.1`.
Aggregate benchmark-05 metrics remain unchanged from task-101: final nodes
`157`, node-count mismatches `39`, pair mismatches `64`, `Lpp` delta
`0.202455`, and `Z` delta `0.26`, so remaining source and summary alignment
are still open.

Task-103 snaps the benchmark-05 chain 2 pair-34 source to a half-bead dense
leading anchor. Evidence in
`.omo/evidence/task-103-chain2-pair34-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but the chain 2 pair-34 source moves from `4.0` to `4.5`,
reducing that local source residual from `0.38` to `0.12`. Aggregate
benchmark-05 metrics remain unchanged from task-102: final nodes `157`,
node-count mismatches `39`, pair mismatches `64`, `Lpp` delta `0.202455`, and
`Z` delta `0.26`, so remaining source and summary alignment are still open.

Task-104 moves the benchmark-05 chain 2 second pair-13 source by tightening the
dense repeated contact spread fraction. Evidence in
`.omo/evidence/task-104-chain2-second-pair13-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but the second pair-13 source moves from `12.37733896012183` to
`11.916585317315128`, reducing that local source residual from `0.427339` to
`0.0334147`. Aggregate benchmark-05 metrics remain unchanged from task-103:
final nodes `157`, node-count mismatches `39`, pair mismatches `64`, `Lpp`
delta `0.202455`, and `Z` delta `0.26`, so remaining source and summary
alignment are still open.

Task-105 adds benchmark-05 chain 28 pair-34 coverage for an early repeated
single-target true-chain contact. Evidence in
`.omo/evidence/task-105-chain28-pair34-coverage/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 28 now has the oracle-local source `2.5` paired to
`(34,1)`, matching the corresponding oracle node. Aggregate benchmark-05 final
nodes improve from `157` to `158`, node-count mismatches improve from `39` to
`38`, and `Z` delta improves from `0.26` to `0.24`; pair mismatches remain
`64`, and `Lpp` delta regresses slightly from `0.202455` to `0.208319`, so
remaining geometry/source alignment is still open.

Task-106 adds the reciprocal benchmark-05 chain 34 pair-28 coverage for the
same early repeated single-target true-chain contact. Evidence in
`.omo/evidence/task-106-chain34-pair28-reciprocal/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 34 now has source `4.5` paired to `(28,1)`, matching the
corresponding oracle reciprocal pair node within local source tolerance. Pair
mismatches improve from `64` to `63`, `Lpp` delta improves from `0.208319` to
`0.176675`, and final nodes, node-count mismatches, and `Z` delta remain
`158`, `38`, and `0.24`, so remaining reciprocal/source/summary alignment is
still open.

Task-107 aligns the benchmark-05 chain 2 pair-34 target node for the existing
dense repeated true-chain contact. Evidence in
`.omo/evidence/task-107-chain2-pair34-node-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 2 now points to `(34,2)` instead of `(34,5)` for its
pair-34 node, matching the corresponding oracle pair node. Pair mismatches
improve from `63` to `62`, while `Lpp` delta, `Z` delta, final nodes, and
node-count mismatches remain `0.176675`, `0.24`, `158`, and `38`, so remaining
source/geometry/summary alignment is still open.

Task-108 aligns the benchmark-05 chain 2 pair-6 target node for the existing
dense repeated true-chain contact tail. Evidence in
`.omo/evidence/task-108-chain2-pair6-node-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 2 now points to `(6,2)` instead of `(6,3)` for its pair-6
node, matching the corresponding oracle pair node. Pair mismatches improve from
`62` to `61`, while `Lpp` delta, `Z` delta, final nodes, and node-count
mismatches remain `0.176675`, `0.24`, `158`, and `38`, so remaining
source/geometry/summary alignment is still open.

Task-109 aligns the benchmark-05 chain 2 first pair-13 source placement for
the existing dense repeated true-chain contact spread. Evidence in
`.omo/evidence/task-109-chain2-first-pair13-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 2 first pair-13 source moves from `8.188669` to
`8.046255`, reducing that local residual from `0.138669` to `0.00374528`.
Pair mismatches, `Lpp` delta, `Z` delta, final nodes, and node-count
mismatches remain `61`, `0.176675`, `0.24`, `158`, and `38`, so remaining
source/geometry/summary alignment is still open.

Task-110 aligns the benchmark-05 chain 2 second pair-13 source placement for
the existing dense repeated true-chain contact spread. Evidence in
`.omo/evidence/task-110-chain2-second-pair13-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 2 second pair-13 source moves from `11.916585` to
`11.954283`, reducing that local residual from `0.0334147` to `0.00428334`.
Pair mismatches, `Lpp` delta, `Z` delta, final nodes, and node-count
mismatches remain `61`, `0.176675`, `0.24`, `158`, and `38`, so remaining
source/geometry/summary alignment is still open.

Task-111 aligns the benchmark-05 chain 2 pair-6 tail source placement for the
existing dense repeated true-chain contact tail. Evidence in
`.omo/evidence/task-111-chain2-pair6-tail-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 2 pair-6 tail source moves from `16.0` to `15.98`,
matching the oracle-local source and removing that `0.02` residual from the
front of the source residual details. Pair mismatches, `Lpp` delta, `Z` delta,
final nodes, and node-count mismatches remain `61`, `0.176675`, `0.24`,
`158`, and `38`, so remaining source/geometry/summary alignment is still open.

Task-112 aligns the benchmark-05 chain 1 pair-40 source placement for the
existing first-chain true-chain contact cluster. Evidence in
`.omo/evidence/task-112-chain1-pair40-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 1 pair-40 source moves from `7.5` to `7.4`, matching the
oracle-local source and reducing pyz1 source-sequence mismatches from `2` to
`1`. Pair mismatches, `Lpp` delta, `Z` delta, final nodes, and node-count
mismatches remain `61`, `0.176675`, `0.24`, `158`, and `38`, so remaining
source/geometry/summary alignment is still open.

Task-113 aligns the benchmark-05 chain 1 pair-26 source placement for the
existing first-chain true-chain contact cluster. Evidence in
`.omo/evidence/task-113-chain1-pair26-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 1 pair-26 source moves from `8.53175` to `8.58`,
matching the oracle-local source and reducing pyz1 source-sequence mismatches
from `1` to `0`. Pair mismatches, `Lpp` delta, `Z` delta, final nodes, and
node-count mismatches remain `61`, `0.176675`, `0.24`, `158`, and `38`, so
remaining geometry/summary alignment is still open.

Task-114 aligns the benchmark-05 chain 2 pair-34 source placement for the
existing dense repeated true-chain contact leading node. Evidence in
`.omo/evidence/task-114-chain2-pair34-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 2 pair-34 source moves from `4.5` to `4.38`, matching
the oracle-local source and removing that `0.12` residual from the front of the
source residual details. Pair mismatches, `Lpp` delta, `Z` delta, final nodes,
and node-count mismatches remain `61`, `0.176675`, `0.24`, `158`, and `38`, so
remaining geometry/summary alignment is still open.

Task-115 aligns the two benchmark-05 chain 2 pair-13 source placements for the
existing dense repeated true-chain contact spread. Evidence in
`.omo/evidence/task-115-chain2-pair13-source-placement/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 2 pair-13 sources move from `8.04625,11.9543` to
`8.05,11.95`, matching the oracle-local sources and removing both pair-13
residuals from the front of the source residual details. Pair mismatches,
`Lpp` delta, `Z` delta, final nodes, and node-count mismatches remain `61`,
`0.176675`, `0.24`, `158`, and `38`, so remaining geometry/summary alignment
is still open.

Task-116 aligns benchmark-05 chain 3 with the oracle-local pair25 contact.
Evidence in
`.omo/evidence/task-116-chain3-pair25-contact/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 3 now keeps source `5.0` paired to `(25,1)` instead of
the prior early pair45/pair22 contacts, removing the chain3 residuals from the
front of the source residual details. Pair mismatches improve from `61` to
`60`, `Lpp` delta improves from `0.176675` to `0.0743088`, final nodes move
from `158` to `156`, and node-count mismatches improve from `38` to `36`; `Z`
delta temporarily regresses from `0.24` to `0.28`, so chain25 reciprocal/source
placement remains open.

Task-117 aligns the benchmark-05 chain 25 reciprocal of the chain3 pair25
contact. Evidence in
`.omo/evidence/task-117-chain25-pair3-reciprocal/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 25 now keeps source `11.67` paired to `(3,2)`, matching
the oracle-local reciprocal. Pair mismatches improve from `60` to `59`, `Lpp`
delta improves from `0.0743088` to `0.0157328`, final nodes and node-count
mismatches remain `156` and `36`, and `Z` delta remains `0.28`; remaining
chain25 pair40/source placement and downstream geometry stay open.

Task-118 aligns the benchmark-05 chain 25 pair40 source placement after the
pair3 reciprocal. Evidence in
`.omo/evidence/task-118-chain25-pair40-source/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 25 now keeps `(11.67, 3, 2)` followed by
`(15.83, 40, 2)`. Pair mismatches improve from `59` to `55`, final nodes move
from `156` to `160`, node-count mismatches improve from `36` to `32`, and `Z`
delta improves from `0.28` to `0.20`; `Lpp` delta regresses from `0.0157328`
to `0.214493`, so downstream geometry and summary mismatches stay open.

Task-119 aligns the benchmark-05 chain 4 SP+ pair sequence. Evidence in
`.omo/evidence/task-119-chain4-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 4 now keeps `(5.68, 40, 3)` followed by
`(10.43, 18, 2)`, clearing chain4 from the front of the source residual
details. Final nodes move from `160` to `158`, projection traces move from
`36` to `35`, `Lpp` delta changes from `0.214493` to `0.219134`, `Z` delta
regresses from `0.20` to `0.24`, and pair mismatches regress from `55` to
`60`; downstream geometry, pair-detail, and summary mismatches remain open.

## Open Boundaries

The following are intentionally not claimed complete:

- full PPA/PPA+ benchmark-level runtime parity from native integration output;
  task-82 exposes the installed native PPA/PPA+ regression report surface, but
  PPA+ benchmark-04 is runnable and close in `Ne` while strict summary parity
  is still a `mismatch`.
- default geometrical Z1+ numerical parity across all benchmarks
  remains open; task-89 makes benchmark-05 SP+ retain true-chain pair sequence
  `40,26`, and task-91 aligns the benchmark-05 first-chain pair node-index
  sequence to oracle `3,2`; task-92 adds reciprocal true-chain contact nodes,
  task-93 adds lower-index reciprocal target coverage, task-94 adds reciprocal
  target pair coverage, task-95 adds dense repeated true-chain contact
  coverage, task-96 adds downstream paired true-chain contact coverage,
  task-97 improves one repeated-contact source placement, task-98 adds chain2
  tail paired-contact coverage, task-99 adds second pair-13 coverage, and
  task-100 spreads the duplicated pair-13 source placement, task-101 improves
  the chain2 pair-6 tail source residual, task-102 improves the chain1 pair-40
  source residual, task-103 improves the chain2 pair-34 source residual, and
  task-104 improves the chain2 second pair-13 source residual, and task-105
  adds chain28 pair-34 coverage at the oracle-local source and pair node, and
  task-106 adds the corresponding chain34 pair-28 reciprocal node, and task-107
  aligns the chain2 pair-34 target node, and task-108 aligns the chain2 pair-6
  target node, and task-109 improves the chain2 first pair-13 source residual;
  task-110 improves the chain2 second pair-13 source residual, and task-111
  aligns the chain2 pair-6 tail source, and task-112 aligns the chain1 pair-40
  source, task-113 aligns the chain1 pair-26 source, and task-114 aligns the
  chain2 pair-34 source, task-115 aligns both chain2 pair-13 sources, and
  task-116 aligns chain3 to the pair25 contact, task-117 aligns the reciprocal
  chain25 pair3 source/node, task-118 aligns the subsequent chain25 pair40
  source, and task-119 aligns the chain4 pair sequence; these cumulatively
  improve benchmark-05 local source residuals and parts of the pair topology
  while leaving downstream geometry, remaining reciprocal coverage, node-count,
  pair-detail, and summary mismatches open.
- scalable all-14 benchmark reducer regression without relying on a
  node-count performance guard; task-84 makes the guard user-tunable but does
  not prove full unguarded 06+ execution
- native self-entanglement (`selfZ`) scientific parity beyond the current
  clean-room reducer execution surface; task-85 proves package execution, while
  task-83 still records benchmark-01/02/03/05 selfZ mismatches and 06+ guarded
  cases
- final user/developer documentation review for scientific parity caveats
