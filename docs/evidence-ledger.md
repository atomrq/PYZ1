# pyz1 Evidence Ledger

This ledger maps the clean-room reproduction requirements to current repo tests,
local evidence artifacts, and known open boundaries. It is an index, not a
parity claim.

For a requirement-by-requirement completion verdict, see
`docs/completion-audit.md`.

Future development is governed by `docs/source-informed-development-plan.md`.
That plan records the local `Z1plus-code` source mirror, makes source-first
parser/writer/reducer checks mandatory, and defines the updated work order:
source-trace/I/O contract first, benchmark-05 SP+ parity next, then benchmark
07/10/11 and PPA+ log-smoke expansion.

Reducer geometry parity is additionally constrained by
`docs/reducer-oracle-geometry-audit.md`: oracle final coordinates may be used
to diagnose residuals, but benchmark-specific oracle `Vector3(...)` values are
temporary oracle-regression shims, not final clean-room reducer algorithms.
Task-171 records the current project-level correction: the final reducer target
is statistical parity at the ensemble/report level, while per-chain SP/SP+
residuals are diagnostics and regression guards unless they protect a
generalized topology/source/pairing rule.
Task-177 sharpens that boundary: future SP/SP+ reducer slices should pass or
fail on statistical/report parity, source-backed topology contracts, and
regression safety, not on exact equality for every individual chain.

## Current Quality Gates

Latest remote GPU-cluster gate evidence:

- `.omo/evidence/task-177-statistical-acceptance-boundary/validation.md`:
  records the docs/evidence-only acceptance-boundary update that per-chain
  contour and final-geometry residuals are diagnostics unless they protect a
  generalized topology/contact rule
- `.omo/evidence/task-176-reference-log-physical-fields/source-trace.md`:
  classifies the reference-log physical-field report expansion as
  `source_contract` over public `mkmat/Z1plus-code` benchmark 07/10/11 Z1+/PPA+
  reference logs
- `.omo/evidence/task-176-reference-log-physical-fields/red-focused-416833.out`:
  RED failed for the intended reason: `ReferenceLogRecord` already parsed
  `Ree/app/bpp/<N>`, but the markdown report did not expose those fields
- `.omo/evidence/task-176-reference-log-physical-fields/focused-416835.out`:
  focused reference-log smoke test passed after adding `Ree`, `app`, `bpp`,
  and `<N>` columns to the report
- `.omo/evidence/task-176-reference-log-physical-fields/static-416836.out`:
  `ruff` and `basedpyright` passed for `src/pyz1/reference_logs.py` and
  `tests/test_reference_logs.py`
- `.omo/evidence/task-176-reference-log-physical-fields/package-smoke-416837.out`:
  editable install and `pyz1-reference-log-smoke` console-script report
  generation passed
- `.omo/evidence/task-176-reference-log-physical-fields/reference-log-physical-fields-final.md`:
  final report records six parseable benchmark 07/10/11 Z1+/PPA+ reference-log
  records with source-backed `Ree`, `app`, `bpp`, and `<N>` values
- `.omo/evidence/task-176-reference-log-physical-fields/sacct.txt`:
  records RED job `416833` as expected `FAILED` and final jobs `416835`,
  `416836`, `416837`, and docs gate `416839` as `COMPLETED` with
  `ExitCode=0:0`

- `.omo/evidence/task-175-corpus-ppaplus-stat-fields/source-trace.md`:
  classifies the corpus PPA+ statistical-field expansion as `source_contract`
  over public `mkmat/Z1plus-code` benchmark 07/10/11 Z1+/PPA+ reference logs
- `.omo/evidence/task-175-corpus-ppaplus-stat-fields/red-focused-416822.out`:
  RED failed for the intended reason:
  `CorpusSmokeRecord` did not yet expose `z1plus_mean_shortest_path_contour`
- `.omo/evidence/task-175-corpus-ppaplus-stat-fields/focused-final-416828.out`:
  focused corpus smoke test passed after threading Z1+ `<Lpp>` and PPA+
  `<Lpp>/<Z>/Ne_CC` fields into the report
- `.omo/evidence/task-175-corpus-ppaplus-stat-fields/static-final-416829.out`:
  `ruff` and `basedpyright` passed for `src/pyz1/corpus_smoke.py` and
  `tests/test_corpus_smoke.py`
- `.omo/evidence/task-175-corpus-ppaplus-stat-fields/package-smoke-final-416830.out`:
  editable install and `pyz1-corpus-stat-smoke` console-script report
  generation passed
- `.omo/evidence/task-175-corpus-ppaplus-stat-fields/corpus-stat-ppaplus-fields-final.md`:
  final report keeps benchmark 07/10/11 `passed` and records source-backed
  Z1+ `<Lpp>/<Z>/Ne_MC` plus PPA+ `<Lpp>/<Z>/Ne_CC/Ne_MC` values; PPA+ `<Z>`
  remains the public-log sentinel `-1`
- `.omo/evidence/task-175-corpus-ppaplus-stat-fields/sacct.txt`:
  records RED job `416822` as expected `FAILED` and final jobs `416828`,
  `416829`, `416830`, and docs gate `416831` as `COMPLETED` with
  `ExitCode=0:0`

- `.omo/evidence/task-174-statistical-regression-status/source-trace.md`:
  classifies the benchmark regression status split as `diagnostic_only`; it
  implements the project correction that statistical parity is tracked beside,
  not instead of, strict per-chain diagnostics
- `.omo/evidence/task-174-statistical-regression-status/red-focused-416813.out`:
  RED failed for the intended reason: `RegressionRecord` did not yet expose a
  `statistical_status`
- `.omo/evidence/task-174-statistical-regression-status/focused-final-416817.out`:
  final focused benchmark-05 SP+ contact-relaxation report test passed
- `.omo/evidence/task-174-statistical-regression-status/static-final-416818.out`:
  `ruff` and `basedpyright` passed for `src/pyz1/regression.py` and
  `tests/test_spplus_regression.py`
- `.omo/evidence/task-174-statistical-regression-status/package-smoke-final-416819.out`:
  editable install and `pyz1-benchmark-regression --contact-relaxation` report
  generation passed
- `.omo/evidence/task-174-statistical-regression-status/benchmark-05-spplus-statistical-status-final.md`:
  final report keeps benchmark-05 SP+ strict `status` as `mismatch` while
  adding `statistical status` as `passed`; residual diagnostics remain visible
  with `Lpp delta` `0.00409694`, `Z delta` `0`, zero pair/node/source-sequence
  mismatches, mean chain-contour delta `0.171325`, RMS `0.308536`, and max
  chain-contour delta `0.886959`
- `.omo/evidence/task-174-statistical-regression-status/sacct-green.txt`:
  records final jobs `416817`, `416818`, and `416819` as `COMPLETED` with
  `ExitCode=0:0`; earlier superseded static/package attempts are retained for
  traceability
- `.omo/evidence/task-174-statistical-regression-status/docs-gate-416820.out`
  and `.omo/evidence/task-174-statistical-regression-status/sacct.txt`:
  record the final docs/evidence gate as passed; job `416820` completed with
  `ExitCode=0:0`

- `.omo/evidence/task-173-corpus-ne-smoke/source-trace.md`:
  classifies the corpus Ne smoke expansion as `source_contract` over public
  `mkmat/Z1plus-code` benchmark 07/10/11 Z1+/PPA+ reference logs
- `.omo/evidence/task-173-corpus-ne-smoke/red-focused-416806.out`:
  RED failed for the intended reason:
  `CorpusSmokeRecord` did not yet expose `z1plus_mean_entanglements`
- `.omo/evidence/task-173-corpus-ne-smoke/focused-green-416807.out`:
  focused corpus smoke test passed after threading selected reference-log
  summary/Ne fields into the report
- `.omo/evidence/task-173-corpus-ne-smoke/focused-static-416810.out`:
  final focused pytest, `ruff`, and `basedpyright` passed for
  `src/pyz1/corpus_smoke.py` and `tests/test_corpus_smoke.py`
- `.omo/evidence/task-173-corpus-ne-smoke/package-smoke-final-416811.out`:
  editable install and `pyz1-corpus-stat-smoke` console-script report
  generation passed
- `.omo/evidence/task-173-corpus-ne-smoke/corpus-stat-ne-smoke-final.md`:
  final report keeps benchmark 07/10/11 `passed` for input/reference baseline
  checks and adds source-backed `Z1+ <Z>`, `Z1+ Ne_MC`, and `PPA+ Ne_MC`
  tracking fields
- `.omo/evidence/task-173-corpus-ne-smoke/sacct.txt`:
  records final jobs `416807`, `416810`, and `416811` as `COMPLETED` with
  `ExitCode=0:0`; RED and superseded static/package attempts remain recorded

- `.omo/evidence/task-172-regression-statistical-contour/source-trace.md`:
  classifies the benchmark regression contour-statistics report slice as
  `diagnostic_only`; it adds ensemble-level mean/RMS chain-contour deltas while
  preserving max per-chain contour residual diagnostics and mismatch details
- `.omo/evidence/task-172-regression-statistical-contour/red-focused-416798.out`:
  corrected RED failed for the intended reason:
  `RegressionRecord` did not yet expose `mean_chain_contour_delta`
- `.omo/evidence/task-172-regression-statistical-contour/focused-green-416800.out`:
  final focused benchmark-05 SP+ contact-relaxation report test passed
- `.omo/evidence/task-172-regression-statistical-contour/static-416802.out`:
  `ruff` and `basedpyright` passed for the changed regression report and SP+
  regression test files
- `.omo/evidence/task-172-regression-statistical-contour/package-smoke-416804.out`:
  editable install and console-script benchmark regression smoke passed
- `.omo/evidence/task-172-regression-statistical-contour/benchmark-05-spplus-statistical-contour.md`:
  generated benchmark-05 SP+ contact-relaxation report records `Lpp delta`
  `0.00409694`, `Z delta` `0`, zero pair/node/source-sequence mismatches,
  mean chain-contour delta `0.171325`, and RMS chain-contour delta `0.308536`
- `.omo/evidence/task-172-regression-statistical-contour/sacct.txt`:
  records final jobs `416800`, `416802`, and `416804` as `COMPLETED` with
  `ExitCode=0:0`; invalid/superseded setup jobs are retained for traceability

- `.omo/evidence/task-171-statistical-parity-policy/source-trace.md`:
  classifies this documentation/policy slice as `diagnostic_only`; it points to
  `docs/source-informed-development-plan.md`, `docs/pyz1-contract.md`, and the
  task168-170 source-backed smoke surfaces as the current evidence baseline for
  statistical parity development
- `.omo/evidence/task-171-statistical-parity-policy/docs-gate-416794.out` and
  `.omo/evidence/task-171-statistical-parity-policy/sacct.txt`:
  record the remote GPU-cluster docs gate as passed; job `416794` completed
  with `0:0`, later post-doc-sync validation is recorded in
  `.omo/evidence/task-171-statistical-parity-policy/validation.md`, and
  superseded job `416793` failed only because the first gate used an
  over-strict cross-line grep

- `.omo/evidence/task-170-corpus-stat-smoke/source-trace.md`:
  classifies the benchmark 07/10/11 corpus statistical smoke as a
  `source_contract` over public `mkmat/Z1plus-code` benchmark inputs and
  reference logs
- `.omo/evidence/task-170-corpus-stat-smoke/red-focused-416784.out`:
  RED failed for the intended reason before implementation:
  `ModuleNotFoundError: No module named 'pyz1.corpus_smoke'`
- `.omo/evidence/task-170-corpus-stat-smoke/focused-final-416788.out`:
  final focused corpus smoke tests passed
- `.omo/evidence/task-170-corpus-stat-smoke/static-final-416789.out`:
  final ruff and basedpyright passed for the corpus report surface, CLI, and
  focused tests
- `.omo/evidence/task-170-corpus-stat-smoke/package-smoke-final-416790.out`:
  package smoke passed after editable install and console-script execution
- `.omo/evidence/task-170-corpus-stat-smoke/corpus-stat-smoke-final.md`:
  final report marks benchmark 07, 10, and 11 `passed` with zero chain-count
  and mean-`N` deltas between input statistics and public Z1+/PPA+ reference
  logs

- `.omo/evidence/task-169-benchmark-input-smoke/source-trace.md`:
  classifies the benchmark 07/10/11 `.Z1`/`.dump` input smoke as a
  `source_contract` over public `mkmat/Z1plus-code` benchmark inputs
- `.omo/evidence/task-169-benchmark-input-smoke/red-focused-416777.out`:
  RED failed for the intended reason before implementation:
  `ModuleNotFoundError: No module named 'pyz1.benchmark_inputs'`
- `.omo/evidence/task-169-benchmark-input-smoke/focused-final-416781.out`:
  final focused benchmark input tests passed
- `.omo/evidence/task-169-benchmark-input-smoke/static-final-416782.out`:
  final ruff and basedpyright passed for the benchmark input report surface,
  CLI, and focused tests
- `.omo/evidence/task-169-benchmark-input-smoke/package-smoke-final-416783.out`:
  package smoke passed after editable install and console-script execution
- `.omo/evidence/task-169-benchmark-input-smoke/benchmark-input-smoke-final.md`:
  final report contains six parseable source-backed records for benchmark
  07/10/11 `.Z1` and `.dump` inputs; each benchmark's formats agree on chain
  count, node count, true-chain count, and box lengths

- `.omo/evidence/task-168-reference-log-smoke/source-trace.md`:
  classifies the benchmark 07/10/11 Z1+/PPA+ reference-log smoke as a
  `source_contract` over public `mkmat/Z1plus-code` logs, not a reducer oracle
  coordinate dependency
- `.omo/evidence/task-168-reference-log-smoke/red-focused-416752.out`:
  RED failed for the intended reason before implementation:
  `ModuleNotFoundError: No module named 'pyz1.reference_logs'`
- `.omo/evidence/task-168-reference-log-smoke/focused-final6-416772.out`:
  final focused reference-log tests passed
- `.omo/evidence/task-168-reference-log-smoke/static-final7-416773.out`:
  final ruff and basedpyright passed for the reference-log parser, CLI, and
  focused tests
- `.omo/evidence/task-168-reference-log-smoke/package-smoke-final6-416774.out`:
  package smoke passed after editable install and console-script execution
- `.omo/evidence/task-168-reference-log-smoke/reference-log-smoke-final6.md`:
  final report contains six parseable source-backed records for benchmark
  07/10/11 Z1+ and PPA+, including benchmark-11 Z1+ `Ne_MC` parsed from the
  public log's adjacent text/number format

- `.omo/evidence/task-167-chain3-single-contact-relaxation/source-trace.md`:
  classifies the guarded single-contact relaxation pass as
  `oracle_residual_inference_generalizable`; it records the project correction
  that SP/SP+ parity should be evaluated primarily on statistical/report
  metrics while chain-level residuals remain diagnostics
- `.omo/evidence/task-167-chain3-single-contact-relaxation/red-focused-corrected-416739.out`:
  corrected RED failed for the intended reason: the previous guard-enabled
  path left benchmark-05 chain3 contour unchanged despite closed source/pair
  topology
- `.omo/evidence/task-167-chain3-single-contact-relaxation/focused-suite-final-416747.out`:
  final remote focused suite passed 17 tests, including geometry tests,
  chain17/chain37 relaxation guards, guarded statistical report coverage, and
  CLI guarded report coverage
- `.omo/evidence/task-167-chain3-single-contact-relaxation/static-final-416751.out`:
  final ruff and basedpyright passed for the changed reducer and regression
  test files
- `.omo/evidence/task-167-chain3-single-contact-relaxation/package-smoke-final-416749.out`:
  package integration smoke passed
- `.omo/evidence/task-167-chain3-single-contact-relaxation/benchmark-04-05-spplus-contact-relaxation.md`:
  guard-enabled SP+ report keeps benchmark-04 `passed`; benchmark-05 remains
  `mismatch`, but `Lpp delta` improves to `0.00409694`, max chain-contour
  delta improves to `0.886959` on chain5, summary field residuals are much
  closer, and pair mismatches, node-count mismatches, source residual details,
  and `Z` delta remain closed
- `.omo/evidence/task-167-chain3-single-contact-relaxation/sacct.txt`:
  records final jobs `416747`, `416749`, `416750`, and `416751` as
  `COMPLETED` with exit code `0:0`; superseded jobs document the invalid RED
  setup, corrected RED, an over-broad single-contact attempt that worsened
  diagnostics, and the E501 static failure before the final rerun
- `.omo/evidence/task-166-chain17-multinode-relaxation/source-trace.md`:
  classifies the guarded final contact-relaxation pass as
  `oracle_residual_inference_generalizable`; it uses input-derived retained
  geometry and pair contact segments only, with no oracle final-coordinate
  runtime input
- `.omo/evidence/task-166-chain17-multinode-relaxation/red-focused-416705.out`:
  focused RED failed for the intended reason: benchmark-05 chain17 guard
  contour did not shorten before the final-pass integration
- `.omo/evidence/task-166-chain17-multinode-relaxation/focused-suite-final-416734.out`:
  final remote focused suite passed 17 tests, including chain17/chain37
  contact-relaxation coverage, guarded report coverage, CLI guarded report
  coverage, and geometry tests
- `.omo/evidence/task-166-chain17-multinode-relaxation/static-final-cli-416735.out`:
  final ruff and basedpyright passed for the changed reducer and regression
  test files
- `.omo/evidence/task-166-chain17-multinode-relaxation/package-smoke-final-416736.out`:
  package integration smoke passed
- `.omo/evidence/task-166-chain17-multinode-relaxation/benchmark-04-05-spplus-contact-relaxation.md`:
  guard-enabled SP+ report keeps benchmark-04 `passed`; benchmark-05 remains
  `mismatch`, but `Lpp delta` improves to `0.0646243`, max chain-contour delta
  improves to `0.986713` on chain3, and pair mismatches, node-count
  mismatches, source residual details, and `Z` delta remain closed
- `.omo/evidence/task-166-chain17-multinode-relaxation/sacct.txt`:
  records final jobs `416734`, `416735`, `416736`, and `416737` as
  `COMPLETED` with exit code `0:0`; superseded jobs document the initial RED,
  an invalid setup failure, static lint fixes, and a rejected too-wide 3+
  retained-node relaxation attempt
- `.omo/evidence/task-165-chain17-guard-diagnostic/source-trace.md`:
  classifies the chain17 guard-enabled residual inspection as
  `diagnostic_only` / `oracle_residual_inference_generalizable`; visible source
  and current reducer inspection confirm no chain17 oracle final-position shim
  is present
- `.omo/evidence/task-165-chain17-guard-diagnostic/chain17-geometry.md`:
  compares benchmark-05 SP+ default, guard-enabled, and oracle chain17
  geometry; the guard-enabled path keeps the oracle source/pair sequence and
  node count but still has `0.999611` contour delta, making the next target a
  generalized endpoint-fixed multi-node relaxation rule rather than copied
  oracle coordinates
- `.omo/evidence/task-164-relaxation-report-surface/source-trace.md`:
  classifies the contact-relaxation regression surface as `diagnostic_only`
  with `oracle_residual_inference_generalizable` measurement; default reducer
  behavior is unchanged
- `.omo/evidence/task-164-relaxation-report-surface/red-focused-pytest.txt`:
  focused RED failed because `RegressionSettingsOverride` did not yet exist
- `.omo/evidence/task-164-relaxation-report-surface/red-cli-pytest.txt`:
  CLI RED failed because `pyz1.regression_cli` did not yet expose
  `--contact-relaxation`
- `.omo/evidence/task-164-relaxation-report-surface/focused-tests-416693.out`:
  remote focused API/CLI tests passed for guard-enabled benchmark report
  generation
- `.omo/evidence/task-164-relaxation-report-surface/benchmark-04-05-spplus-contact-relaxation.md`:
  guard-enabled SP+ report keeps benchmark-04 `passed`; benchmark-05 remains
  `mismatch`, but `Lpp delta` improves to `0.147902`, max chain-contour delta
  improves to `0.999611` on chain17, and pair mismatches, node-count
  mismatches, source residual details, and `Z` delta remain closed
- `.omo/evidence/task-164-relaxation-report-surface/static2-416699.out`:
  corrected remote ruff and basedpyright passed for regression API/CLI and
  focused tests; superseded static job `416692` failed because basedpyright was
  not pointed at the remote venv Python for `typer`
- `.omo/evidence/task-164-relaxation-report-surface/package-smoke-416691.out`:
  package integration smoke passed
- `.omo/evidence/task-164-relaxation-report-surface/sacct.txt`:
  records package smoke `416691`, focused tests `416693`, guard report
  `416694`, and corrected static `416699` as `COMPLETED` with exit code `0:0`
- `.omo/evidence/task-163-relaxation-reducer-guard/source-trace.md`:
  classifies the settings-gated reducer contact-relaxation integration as
  `oracle_residual_inference_generalizable`; the slice uses benchmark-05
  chain37 only to expose a residual and does not copy oracle final coordinates
- `.omo/evidence/task-163-relaxation-reducer-guard/red-focused-pytest.txt`:
  focused RED failed because `ReducerSettings` did not yet expose
  `contact_relaxation_enabled`
- `.omo/evidence/task-163-relaxation-reducer-guard/focused-regression-416689.out`:
  remote GPU-cluster focused GREEN passed
  `tests/test_spplus_regression.py::test_reduce_snapshot_when_contact_relaxation_shortens_chain37`
  with `PYZ1_SOURCE_Z1` pointed at the synced benchmark-05 fixture
- `.omo/evidence/task-163-relaxation-reducer-guard/static-416688.out`:
  remote ruff and basedpyright passed for `src/pyz1/reducer.py`,
  `src/pyz1/contact_relaxation.py`, and `tests/test_spplus_regression.py`
- `.omo/evidence/task-163-relaxation-reducer-guard/package-smoke-416690.out`:
  package integration smoke passed after the settings-gated reducer integration
- `.omo/evidence/task-163-relaxation-reducer-guard/sacct.txt`:
  records jobs `416688`, `416689`, and `416690` as `COMPLETED` with exit
  code `0:0`
- `.omo/evidence/task-162-contact-relaxation/source-trace.md`:
  classifies the contact-constrained relaxation helper as
  `oracle_residual_inference_generalizable`, explicitly avoiding oracle final
  coordinates
- `.omo/evidence/task-162-contact-relaxation/remote-gate-416682.out`:
  corrected remote gate passed `tests/test_geometry.py`, ruff, and basedpyright
  for `src/pyz1/contact_relaxation.py`, `src/pyz1/geometry.py`, and
  `tests/test_geometry.py`
- `.omo/evidence/task-162-contact-relaxation/package-smoke-416683.out`:
  package integration smoke passed after the new helper landed
- `.omo/evidence/task-160-chain22-contour/source-trace.md`:
  classifies the benchmark-05 SP+ chain22 contour placement slice as
  `oracle_residual_inference` after checking visible Z1+/Z1plus-code source and
  confirming the hidden reducer core remains unavailable
- `.omo/evidence/task-160-chain22-contour/benchmark-04-05-spplus-final.md`:
  final regression job `416674` keeps benchmark-04 SP+ `passed`; benchmark-05
  SP+ remains a true `mismatch`, but pair mismatches, node-count mismatches,
  source residual details, and `Z` delta stay closed while max chain-contour
  delta moves from chain22 to chain37 (`1.0324`)
- `.omo/evidence/task-160-chain22-contour/sacct.txt`:
  records RED job `416664`, diagnostic jobs `416665` and `416667`, focused
  GREEN job `416666`, package smoke job `416670`, corrected static job
  `416673`, corrected final regression job `416674`, and superseded setup
  failures `416668`, `416669`, `416671`, and `416672`
- `.omo/evidence/task-159-chain43-contour/source-trace.md`:
  classifies the benchmark-05 SP+ chain43 contour placement slice as
  `oracle_residual_inference` after checking visible Z1+/Z1plus-code source and
  confirming the hidden reducer core remains unavailable
- `.omo/evidence/task-159-chain43-contour/benchmark-04-05-spplus-final.md`:
  final regression job `416616` keeps benchmark-04 SP+ `passed`; benchmark-05
  SP+ remains a true `mismatch`, but pair mismatches, node-count mismatches,
  source residual details, and `Z` delta stay closed while max chain-contour
  delta moves from chain43 to chain22 (`1.0894`)
- `.omo/evidence/task-159-chain43-contour/sacct.txt`:
  records RED job `416613`, diagnostic jobs `416614` and `416617`, focused
  GREEN job `416615`, final regression job `416616`, static job `416618`, and
  package smoke job `416619`
- `.omo/evidence/task-158-chain9-contour/source-trace.md`:
  classifies the benchmark-05 SP+ chain9 contour placement slice as
  `oracle_residual_inference` after checking visible Z1+/Z1plus-code source and
  confirming the hidden reducer core remains unavailable
- `.omo/evidence/task-158-chain9-contour/benchmark-04-05-spplus-final.md`:
  final regression rerun job `416611` keeps benchmark-04 SP+ `passed`;
  benchmark-05 SP+ remains a true `mismatch`, but pair mismatches, node-count
  mismatches, source residual details, and `Z` delta stay closed while max
  chain-contour delta moves from chain9 to chain43 (`1.25809`)
- `.omo/evidence/task-158-chain9-contour/sacct.txt`:
  records RED job `416605`, diagnostic job `416606`, focused GREEN job
  `416607`, invalid setup regression job `416608`, static job `416609`,
  package smoke job `416610`, final regression rerun job `416611`, and
  post-fix diagnostic job `416612`
- `.omo/evidence/task-157-chain25-contour/source-trace.md`:
  classifies the benchmark-05 SP+ chain25 contour placement slice as
  `oracle_residual_inference` after checking visible Z1+/Z1plus-code source and
  confirming the hidden reducer core remains unavailable
- `.omo/evidence/task-157-chain25-contour/benchmark-04-05-spplus-final.md`:
  final regression job `416602` keeps benchmark-04 SP+ `passed`; benchmark-05
  SP+ remains a true `mismatch`, but pair mismatches, node-count mismatches,
  source residual details, and `Z` delta stay closed while max chain-contour
  delta moves from chain25 to chain9 (`1.26412`)
- `.omo/evidence/task-157-chain25-contour/sacct.txt`:
  records RED job `416599`, diagnostic job `416600`, focused GREEN job
  `416601`, final regression job `416602`, static job `416603`, and package
  smoke job `416604`
- `.omo/evidence/task-156-chain27-contour/source-trace.md`:
  classifies the benchmark-05 SP+ chain27 contour placement slice as
  `oracle_residual_inference` after checking visible Z1+/Z1plus-code source and
  confirming the hidden reducer core remains unavailable
- `.omo/evidence/task-156-chain27-contour/benchmark-04-05-spplus-final.md`:
  final regression retry job `416597` keeps benchmark-04 SP+ `passed`;
  benchmark-05 SP+ remains a true `mismatch`, but pair mismatches, node-count
  mismatches, source residual details, and `Z` delta stay closed while max
  chain-contour delta moves from chain27 to chain25 (`1.72682`)
- `.omo/evidence/task-156-chain27-contour/sacct.txt`:
  records corrected RED job `416590`, corrected diagnostic job `416592`,
  focused GREEN job `416593`, final regression retry job `416597`, static job
  `416595`, and package smoke job `416596`; invalid setup jobs are retained and
  classified in `benchmark05-chain27-contour.md`
- `.omo/evidence/task-155-chain36-contour/source-trace.md`:
  classifies the benchmark-05 SP+ chain36 contour placement slice as
  `oracle_residual_inference` after checking visible Z1+/Z1plus-code source and
  confirming the hidden reducer core remains unavailable
- `.omo/evidence/task-155-chain36-contour/benchmark-04-05-spplus-final.md`:
  final regression job `416586` keeps benchmark-04 SP+ `passed`; benchmark-05
  SP+ remains a true `mismatch`, but pair mismatches, node-count mismatches,
  source residual details, and `Z` delta stay closed while max chain-contour
  delta moves from chain36 to chain27 (`2.24027`)
- `.omo/evidence/task-155-chain36-contour/sacct.txt`:
  records valid RED job `416583`, diagnostic job `416584`, focused GREEN job
  `416585`, final regression job `416586`, static job `416587`, and package
  smoke job `416588`
- `.omo/evidence/task-154-chain34-contour/source-trace.md`:
  classifies the benchmark-05 SP+ chain34 contour placement slice as
  `oracle_residual_inference` after checking visible Z1+/Z1plus-code source and
  confirming the hidden reducer core remains unavailable
- `.omo/evidence/task-154-chain34-contour/benchmark-04-05-spplus-final.md`:
  final regression job `416580` keeps benchmark-04 SP+ `passed`; benchmark-05
  SP+ remains a true `mismatch`, but pair mismatches, node-count mismatches,
  source residual details, and `Z` delta stay closed while max chain-contour
  delta moves from chain34 to chain36 (`2.44735`)
- `.omo/evidence/task-154-chain34-contour/sacct.txt`:
  records valid RED job `416570`, diagnostic jobs `416571` and `416572`,
  superseded missing-source GREEN job `416578`, focused GREEN job `416579`,
  final regression job `416580`, static job `416581`, and package smoke job
  `416582`
- `.omo/evidence/task-153-chain48-contour/source-trace.md`:
  classifies the benchmark-05 SP+ chain48 contour placement slice as
  `oracle_residual_inference` after checking visible Z1+/Z1plus-code source and
  confirming the hidden reducer core remains unavailable
- `.omo/evidence/task-153-chain48-contour/benchmark-04-05-spplus-final.md`:
  final regression job `416558` keeps benchmark-04 SP+ `passed`; benchmark-05
  SP+ remains a true `mismatch`, but pair mismatches, node-count mismatches,
  source residual details, and `Z` delta stay closed while max chain-contour
  delta moves from chain48 to chain34 (`3.02439`)
- `.omo/evidence/task-153-chain48-contour/sacct.txt`:
  records setup-failed RED job `416545`, valid RED job `416546`, diagnostic
  job `416547`, superseded sync-failed GREEN job `416548`, focused GREEN job
  `416549`, final regression job `416558`, superseded static job `416559`,
  package smoke job `416560`, and final static rerun job `416561`
- `.omo/evidence/task-152-chain39-contour/source-trace.md`:
  classifies the benchmark-05 SP+ chain39 contour placement slice as
  `oracle_residual_inference` after checking visible Z1+/Z1plus-code source and
  confirming the hidden reducer core remains unavailable
- `.omo/evidence/task-152-chain39-contour/benchmark-04-05-spplus-final.md`:
  final regression job `416541` keeps benchmark-04 SP+ `passed`; benchmark-05
  SP+ remains a true `mismatch`, but pair mismatches, node-count mismatches,
  source residual details, and `Z` delta stay closed while max chain-contour
  delta moves from chain39 to chain48 (`3.09306`)
- `.omo/evidence/task-152-chain39-contour/sacct.txt`:
  records RED job `416536`, superseded attempt `416537`, diagnostics `416538`
  and `416539`, focused GREEN job `416540`, final regression job `416541`,
  superseded static job `416542`, package smoke job `416543`, and final static
  rerun job `416544`
- `.omo/evidence/task-151-chain-contour-diagnostics/source-trace.md`:
  classifies the chain-contour residual report surface as `diagnostic_only`
  after checking visible Z1+/Z1plus-code source and confirming the hidden
  reducer core remains unavailable
- `.omo/evidence/task-151-chain-contour-diagnostics/benchmark-04-05-spplus-final.md`:
  final regression job `416532` keeps benchmark-04 SP+ `passed` and reports
  benchmark-05 SP+ as a true `mismatch` with closed pair/node/source/`Z` gaps
  and max chain-contour delta `9.45416` on chain39
- `.omo/evidence/task-151-chain-contour-diagnostics/sacct.txt`:
  records RED job `416524`, focused GREEN jobs `416525` and `416530`, static
  rerun job `416529`, package smoke job `416528`, and final regression job
  `416532`
- `.omo/evidence/task-144-z1plus-template-quoting/source-trace.md`:
  records the source-backed Z1+ wrapper path-quoting contract from
  `mkmat/Z1plus-code/replacements/Z1+template.pl` commit
  `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- `.omo/evidence/task-144-z1plus-template-quoting/pytest.txt`:
  focused RED job `416460` failed for the old unquoted staged wrapper command,
  focused GREEN job `416468` passed, static job `416467` passed, and package
  smoke job `416469` passed
- `.omo/evidence/task-144-z1plus-template-quoting/ruff.txt` and
  `.omo/evidence/task-144-z1plus-template-quoting/basedpyright.txt`:
  final static evidence for `ruff check src tests` and `basedpyright`
- `.omo/evidence/task-144-z1plus-template-quoting/package-smoke.txt`:
  package smoke job `416469` passed
- `.omo/evidence/task-143-z1plus-code-io-contract/source-trace.md`:
  records the source-backed negative-`xy` triclinic LAMMPS dump bounds contract
  from `mkmat/Z1plus-code` commit
  `c7219cd394b1295272ebfc098f2835c5c871e6ec`
- `.omo/evidence/task-143-z1plus-code-io-contract/pytest.txt`:
  focused RED job `416442` failed for the old `box.x == 12.0` behavior,
  final-path focused GREEN job `416450` passed, and final non-SP pytest array
  `416451` passed shards `41/40/40`
- `.omo/evidence/task-143-z1plus-code-io-contract/ruff.txt` and
  `.omo/evidence/task-143-z1plus-code-io-contract/basedpyright.txt`:
  scoped static final job `416452` passed; superseded job `416445` documents a
  gate-script issue from scanning generated `.omo/evidence` Python scripts
- `.omo/evidence/task-143-z1plus-code-io-contract/package-smoke.txt`:
  package smoke job `416453` passed
- `.omo/evidence/task-142-chain39-spplus-residual/pytest.txt`:
  latest full reducer/SP+ remote GPU-cluster split: non-SP shards
  `40/40/40 passed` and SP+
  shards `10/10/9/9/9/9/9 passed`
- `.omo/evidence/task-55-ppa-coverage/ppa-focused.txt`: `21 passed`
- `.omo/evidence/task-57-ppa-nan-root/ppa-focused.txt`: `22 passed`
- `.omo/evidence/task-142-chain39-spplus-residual/ruff.txt`:
  `All checks passed!`
- `.omo/evidence/task-142-chain39-spplus-residual/basedpyright.txt`:
  `0 errors, 0 warnings, 0 notes`
- `.omo/evidence/task-142-chain39-spplus-residual/package-smoke.txt`:
  `1 passed`
- `.omo/evidence/task-142-chain39-spplus-residual/full-gate/sacct.txt` and
  `.omo/evidence/task-142-chain39-spplus-residual/full-gate/rerun-sacct.txt`:
  final remote Slurm gate jobs `416379_0`-`416379_2`,
  `416380_1`-`416380_6`, `416394_0`, `416393`, `416382`, and `416383`
  completed with `0:0` exit codes after the valid RED assertion (`416376`),
  focused GREEN (`416378`), and superseded static/SP+ shard0 attempts
  (`416381`, `416380_0`) captured in the same full-gate evidence directory

The package smoke runs `python -m pyz1` for default, SP+, selfZ, PPA, and PPA+
modes and checks the expected mode-specific output files.

## Requirement Coverage

| Requirement | Current proof | Evidence |
| --- | --- | --- |
| Z1 input parser and typed models | Unit tests for valid inputs, malformed inputs, metadata, true-chain filtering, and model invariants | `tests/test_z1_io.py`, `tests/test_models.py` |
| Z1+ output parser/writer | Summary, SP/SP+, initconfig, value files, PPA, and PPA+ round-trip tests plus source-backed LAMMPS dump triclinic bounds import | `tests/test_output_io.py`, `tests/test_output_values.py`, `tests/test_initconfig_io.py`, `tests/test_lammps_import.py`, `.omo/evidence/task-143-z1plus-code-io-contract/` |
| Summary and `Ne` estimators | Estimator unit tests plus oracle-SP-through-pyz1 summary parity for benchmark-04 SP+ | `tests/test_estimators.py`, `tests/test_summary.py`, `tests/test_spplus_regression.py`, `.omo/evidence/task-42-summary-ne-source/` |
| Oracle fixture tooling and parity reporting | Oracle manifest tests, CLI help smoke, benchmark regression report tests, logged oracle run metadata, and source-backed Z1+ wrapper path-quoting staging for install/output paths containing spaces | `tests/test_oracle.py`, `tests/test_oracle_install.py`, `tests/test_z1plus_parity.py`, `tests/test_spplus_regression.py`, `.omo/evidence/task-144-z1plus-template-quoting/` |
| Native PPA/PPA+ slices | PPA mode tests, CLI mode tests, package-level smoke, WCA cell-list candidate generation, native PPA summary regression reporting, Z1+ PPA+ phase-stop regression, 12 parseable oracle coordinate-path summary parity cases, explicit Fortran-overflow known-invalid fixture handling, reusable oracle coordinate fixture status reports, a package script that discovers all oracle benchmark directories for coordinate fixture reporting, and an installed native PPA/PPA+ regression report surface | `tests/test_ppa.py`, `tests/test_ppa_regression.py`, `tests/test_ppa_oracle_coordinates.py`, `tests/test_ppa_oracle_coordinates_cli.py`, `tests/test_ppa_regression_cli.py`, `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py`, `.omo/evidence/task-46-ppa-summary-oracle-coverage/`, `.omo/evidence/task-47-ppa-neighbor-list/`, `.omo/evidence/task-48-ppa-native-regression/`, `.omo/evidence/task-49-ppa-lpp-debug/`, `.omo/evidence/task-78-ppa-oracle-coordinate-report/`, `.omo/evidence/task-79-ppa-oracle-coordinate-cli/`, `.omo/evidence/task-80-ppa-oracle-coordinate-discovery/`, `.omo/evidence/task-82-ppa-regression-cli/` |
| Clean-room reducer | Geometry primitives, reducer diagnostics, benchmark-04 reducer structure, SP+ pairing, broad-phase/index blocker filtering, benchmark regression diagnostics for 01-05 under the default guard, a package script that discovers all default/SP+/selfZ oracle benchmark directories for regression reporting, and user-tunable node-count/trace-diagnostics guards | `tests/test_geometry.py`, `tests/test_z1_reducer.py`, `tests/test_spplus_regression.py`, `tests/test_regression_cli.py`, `.omo/evidence/task-53-reducer-index/`, `.omo/evidence/task-81-default-spplus-regression-cli/`, `.omo/evidence/task-83-selfz-regression-surface/`, `.omo/evidence/task-84-regression-cli-guards/` |
| SP+ regression | Pairing comparison, max-node-delta localization, pair-segment geometry diagnostics, oracle summary source isolation, residual ghost-clearance tuning, CLI-driven full-corpus default/SP+/selfZ status reporting, trace-diagnostics guard control, direct pyz1-vs-oracle true-chain pair sequence reporting, true-chain contact candidate diagnostics, oracle-source nearest contact selection diagnostics, guarded true-chain contact-cluster retention, true-chain pair node-index diagnostics, reciprocal true-chain contact retention, lower-index reciprocal target coverage, reciprocal target pair coverage, dense repeated true-chain contact coverage, downstream paired true-chain contact coverage, repeated-contact source-placement coverage, chain2 tail paired-contact coverage, second pair-13 coverage, chain3 pair25 coverage, chain25 pair3 reciprocal coverage, chain25 pair40 source coverage, chain4 pair sequence coverage, chain5/chain16 reciprocal pair sequence coverage, chain6/chain37/chain2 pair sequence coverage, chain9/chain27 pair sequence and chain9/chain27 contour coverage, chain25 contour coverage, chain10/chain36 reciprocal pair sequence and contour coverage, chain11/chain37/chain39 reciprocal pair sequence coverage, chain11/chain32 reciprocal pair sequence coverage, chain12/chain19 reciprocal pair sequence coverage, chain13 pair sequence coverage, chain15/chain36 reciprocal pair sequence and contour coverage, chain17/chain44 pair sequence coverage without a chain9 extra reciprocal, chain18/chain48 reciprocal pair sequence coverage, chain22/chain25 one-way source placement and chain22 contour coverage without adding a chain25 reciprocal, chain26/chain1 reciprocal source placement, chain27/chain19 one-way source placement, chain24/chain35 reciprocal pair sequence coverage, chain29/chain49 one-way pair coverage without adding a chain49 reciprocal, chain20 extra pair49 pruning, chain30 pair sequence coverage, chain31 pair sequence coverage, chain32 pair sequence coverage, chain34 pair sequence and contour coverage, chain37 pair sequence coverage, chain39 pair sequence and contour coverage, chain40 pair sequence coverage, chain42 one-way pair34 coverage, chain43 oracle-absent pair28 pruning and chain43 contour coverage, chain46 pair sequence coverage, chain48 pair sequence and contour coverage, and chain49 reciprocal pair coverage | `tests/test_spplus_regression.py`, `tests/test_regression_cli.py`, `.omo/evidence/task-38-final-node-delta-location/`, `.omo/evidence/task-39-max-node-pair-geometry/`, `.omo/evidence/task-41-spplus-projection-direction/`, `.omo/evidence/task-50-spplus-residual/`, `.omo/evidence/task-81-default-spplus-regression-cli/`, `.omo/evidence/task-83-selfz-regression-surface/`, `.omo/evidence/task-84-regression-cli-guards/`, `.omo/evidence/task-86-true-chain-pair-diagnostics/`, `.omo/evidence/task-87-true-chain-contact-candidates/`, `.omo/evidence/task-88-oracle-source-contact-selection/`, `.omo/evidence/task-89-true-chain-cluster-retention/`, `.omo/evidence/task-90-true-chain-pair-node-diagnostics/`, `.omo/evidence/task-91-true-chain-pair-node-ordinal/`, `.omo/evidence/task-92-true-chain-reciprocal-retention/`, `.omo/evidence/task-93-lower-index-reciprocal-coverage/`, `.omo/evidence/task-94-reciprocal-target-pair-coverage/`, `.omo/evidence/task-95-dense-repeated-contact-coverage/`, `.omo/evidence/task-96-chain2-downstream-paired-contact/`, `.omo/evidence/task-97-chain2-repeated-contact-source-placement/`, `.omo/evidence/task-98-chain2-tail-paired-contact/`, `.omo/evidence/task-99-chain2-second-pair13-coverage/`, `.omo/evidence/task-116-chain3-pair25-contact/`, `.omo/evidence/task-117-chain25-pair3-reciprocal/`, `.omo/evidence/task-118-chain25-pair40-source/`, `.omo/evidence/task-119-chain4-spplus-residual/`, `.omo/evidence/task-120-chain5-spplus-residual/`, `.omo/evidence/task-121-chain6-spplus-residual/`, `.omo/evidence/task-122-chain9-spplus-residual/`, `.omo/evidence/task-123-chain10-spplus-residual/`, `.omo/evidence/task-124-chain11-spplus-residual/`, `.omo/evidence/task-125-chain11-pair32-spplus-residual/`, `.omo/evidence/task-126-chain12-spplus-residual/`, `.omo/evidence/task-127-chain13-spplus-residual/`, `.omo/evidence/task-128-chain15-spplus-residual/`, `.omo/evidence/task-129-chain17-spplus-residual/`, `.omo/evidence/task-130-chain18-spplus-residual/`, `.omo/evidence/task-131-chain22-spplus-residual/`, `.omo/evidence/task-132-chain26-spplus-residual/`, `.omo/evidence/task-133-chain27-spplus-residual/`, `.omo/evidence/task-134-chain24-spplus-residual/`, `.omo/evidence/task-135-chain20-chain29-spplus-residual/`, `.omo/evidence/task-136-chain20-spplus-residual/`, `.omo/evidence/task-137-chain30-spplus-residual/`, `.omo/evidence/task-138-chain31-spplus-residual/`, `.omo/evidence/task-139-chain32-spplus-residual/`, `.omo/evidence/task-140-chain34-spplus-residual/`, `.omo/evidence/task-141-chain37-spplus-residual/`, `.omo/evidence/task-142-chain39-spplus-residual/`, `.omo/evidence/task-145-benchmark05-chain42-pair34/`, `.omo/evidence/task-146-benchmark05-chain43-pair28-prune/`, `.omo/evidence/task-147-benchmark05-chain40-pairs/`, `.omo/evidence/task-148-benchmark05-chain46-pairs/`, `.omo/evidence/task-149-benchmark05-chain48-pairs/`, `.omo/evidence/task-150-benchmark05-chain49-pair/`, `.omo/evidence/task-152-chain39-contour/`, `.omo/evidence/task-153-chain48-contour/`, `.omo/evidence/task-154-chain34-contour/`, `.omo/evidence/task-155-chain36-contour/`, `.omo/evidence/task-156-chain27-contour/`, `.omo/evidence/task-157-chain25-contour/`, `.omo/evidence/task-158-chain9-contour/`, `.omo/evidence/task-159-chain43-contour/`, `.omo/evidence/task-160-chain22-contour/` |
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

Task-120 aligns the benchmark-05 chain 5 SP+ pair sequence and its chain16
reciprocal. Evidence in
`.omo/evidence/task-120-chain5-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 5 now keeps `(6.67, 16, 1)` and chain 16 keeps the
reciprocal `(3.0, 5, 2)`, clearing chain5 from the front of the source
residual details. Final nodes move from `158` to `157`, projection traces move
from `35` to `34`, node-count mismatches improve from `32` to `31`, `Lpp`
delta changes from `0.219134` to `0.219083`, `Z` delta regresses from `0.24`
to `0.26`, and pair mismatches remain `60`; downstream geometry, pair-detail,
and summary mismatches remain open.

Task-121 aligns the benchmark-05 chain 6 SP+ pair sequence and the chain37
reciprocal for that pair. Evidence in
`.omo/evidence/task-121-chain6-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 6 now keeps `(3.85, 37, 3)` followed by `(6.71, 2, 4)`,
chain 37 keeps reciprocal `(10.38, 6, 2)`, and chain 2 retains the existing
reciprocal `(15.98, 6, 2)`. Chain6 residuals are removed from the front of the
source residual details; final nodes move from `157` to `159`, projection
traces move from `34` to `35`, node-count mismatches improve from `31` to
`29`, pair mismatches improve from `60` to `49`, and `Z` delta improves from
`0.26` to `0.22`; `Lpp` delta regresses from `0.219083` to `0.299573`, so
downstream geometry, pair-detail, and summary mismatches remain open.

Task-122 aligns the benchmark-05 chain 9 SP+ pair sequence and the chain27
reciprocal for that pair. Evidence in
`.omo/evidence/task-122-chain9-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 9 now keeps `(6.5, 27, 1)` and chain 27 keeps reciprocal
`(2.43, 9, 2)`, clearing chain9 from the front of the source residual details.
Final nodes move from `159` to `160` and `Z` delta improves from `0.22` to
`0.20`; pair mismatches regress from `49` to `50`, node-count mismatches
regress from `29` to `30`, and `Lpp` delta regresses from `0.299573` to
`0.435382`, so downstream geometry, pair-detail, and summary mismatches remain
open.

Task-123 aligns the benchmark-05 chain 10 SP+ pair sequence and the chain36
reciprocal for that pair. Evidence in
`.omo/evidence/task-123-chain10-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 10 now keeps `(10.67, 36, 2)` and chain 36 keeps
reciprocal `(14.64, 10, 2)`, clearing chain10 from the front of the source
residual details. Final nodes move from `160` to `161`, pair mismatches improve
from `50` to `49`, node-count mismatches improve from `30` to `29`, and `Z`
delta improves from `0.20` to `0.18`; `Lpp` delta regresses from `0.435382` to
`0.547564`, so downstream geometry, pair-detail, and summary mismatches remain
open.

Task-124 aligns the benchmark-05 chain 11 early SP+ pair sequence and the
chain37/chain39 reciprocals for those pairs. Evidence in
`.omo/evidence/task-124-chain11-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 11 now keeps `(2.73, 37, 1)` and `(4.48, 39, 5)`, chain
37 keeps reciprocal `(4.15, 11, 2)`, and chain 39 keeps reciprocal
`(13.16, 11, 3)`. The first two chain11 residuals are cleared; final nodes
move from `161` to `164`, node-count mismatches improve from `29` to `26`,
and `Z` delta improves from `0.18` to `0.12`. Pair mismatches regress from
`49` to `52`, and `Lpp` delta regresses from `0.547564` to `0.666519`, so
downstream geometry, pair-detail, and summary mismatches remain open.

Task-125 aligns the remaining benchmark-05 chain 11 pair32 contact and its
chain32 reciprocal. Evidence in
`.omo/evidence/task-125-chain11-pair32-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 11 now also keeps `(11.5, 32, 2)`, and chain 32 keeps
reciprocal `(2.8, 11, 3)`. The remaining chain11 source residual is cleared
from the front of the source residual details; final nodes move from `164` to
`166`, node-count mismatches improve from `26` to `24`, pair mismatches improve
from `52` to `51`, and `Z` delta improves from `0.12` to `0.08`. `Lpp` delta
regresses from `0.666519` to `0.710841`, so downstream geometry, pair-detail,
and summary mismatches remain open.

Task-126 aligns the benchmark-05 chain 12 SP+ pair sequence and the chain19
reciprocal for that pair. Evidence in
`.omo/evidence/task-126-chain12-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 12 now keeps only `(11.5, 19, 1)`, and chain 19 keeps
reciprocal `(3.5, 12, 2)`. The chain12 residuals are cleared from the front of
the source residual details; final nodes move from `166` to `165`,
node-count mismatches improve from `24` to `23`, pair mismatches improve from
`51` to `47`, and `Lpp` delta improves from `0.710841` to `0.699096`. `Z`
delta regresses from `0.08` to `0.10`, so downstream geometry, pair-detail,
and summary mismatches remain open.

Task-127 aligns the benchmark-05 chain 13 SP+ pair sequence. Evidence in
`.omo/evidence/task-127-chain13-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 13 now keeps only `(4.0, 2, 3)`. The chain13 residuals
are cleared from the front of the source residual details; final nodes move
from `165` to `164`, node-count mismatches improve from `23` to `22`, and
pair mismatches improve from `47` to `44`. `Lpp` delta remains `0.699096`,
while `Z` delta regresses from `0.10` to `0.12`, so downstream geometry,
pair-detail, and summary mismatches remain open.

Task-128 aligns the benchmark-05 chain 15 SP+ pair sequence and the chain36
reciprocal for that pair. Evidence in
`.omo/evidence/task-128-chain15-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 15 now keeps `(13.72, 36, 1)`, and chain 36 keeps
reciprocal `(6.62, 15, 2)`. The chain15 residuals are cleared from the front
of the source residual details; final nodes move from `164` to `165`,
node-count mismatches improve from `22` to `21`, pair mismatches improve from
`44` to `41`, `Lpp` delta improves from `0.699096` to `0.698125`, and `Z`
delta improves from `0.12` to `0.10`, so downstream geometry, pair-detail,
and summary mismatches remain open.

Task-129 aligns the benchmark-05 chain 17 SP+ pair sequence and the chain44
reciprocal while preserving the existing chain9 oracle-local pair without an
extra chain17 reciprocal. Evidence in
`.omo/evidence/task-129-chain17-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 17 now keeps `(5.0, 9, 1)` and `(11.67, 44, 2)`, chain
44 keeps reciprocal `(13.0, 17, 3)`, and chain 9 remains `((6.5, 27, 1),)`.
Final nodes move from `165` to `166`, node-count mismatches improve from `21`
to `18`, `Lpp` delta improves from `0.698125` to `0.612388`, and `Z` delta
improves from `0.10` to `0.08`; pair mismatches move from `41` to `43`, so
downstream geometry, remaining pair-detail coverage, and summary mismatches
remain open. The final task-129 gate ran on the GPU cluster with split Slurm
jobs; evidence is under
`.omo/evidence/task-129-chain17-spplus-residual/cluster-v6/`.

Task-130 aligns the benchmark-05 chain 18 SP+ pair sequence and the chain48
reciprocal while preserving the existing chain4 reciprocal into chain18.
Evidence in
`.omo/evidence/task-130-chain18-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ still reports
`mismatch`, but chain 18 now keeps `(5.0, 4, 3)` and `(9.0, 48, 2)`, and
chain 48 keeps reciprocal `(2.58, 18, 2)`. Final nodes move from `166` to
`168`, node-count mismatches improve from `18` to `16`, pair mismatches
improve from `43` to `42`, and `Z` delta improves from `0.08` to `0.04`;
`Lpp` delta moves from `0.612388` to `0.631095`, so downstream geometry,
remaining pair-detail coverage, and summary mismatches remain open. The final
task-130 gate ran on the GPU cluster with split Slurm jobs; evidence is under
`.omo/evidence/task-130-chain18-spplus-residual/cluster-v1/`.

Task-131 aligns the benchmark-05 chain 22 one-way SP+ source placement to
chain25 while preserving the existing chain25 pair sequence without adding a
chain22 reciprocal. Evidence in
`.omo/evidence/task-131-chain22-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but chain 22 now keeps `(4.84,25,2)` and the previous
`c22n2[25->25]: 11.5!=4.84` source residual is removed from the residual
prefix. Final nodes stay at `168`, node-count mismatches stay at `16`, pair
mismatches stay at `42`, and `Z` delta stays at `0.04`; `Lpp` delta moves from
`0.631095` to `0.644068`, so downstream geometry, remaining pair-detail
coverage, and summary mismatches remain open. The final task-131 gate ran on
the GPU cluster with split Slurm jobs; evidence is under
`.omo/evidence/task-131-chain22-spplus-residual/cluster-v2/`.

Task-132 aligns the benchmark-05 chain26 reciprocal source placement for the
existing chain1 pair26 contact. Evidence in
`.omo/evidence/task-132-chain26-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but chain26 now keeps `(3.67,1,3)` and the previous
`c26n2[1->1]: 1.27539!=3.67` source residual is removed from the residual
prefix. Final nodes stay at `168`, node-count mismatches stay at `16`, pair
mismatches stay at `42`, `Z` delta stays at `0.04`, and `Lpp` delta stays at
`0.644068`, so downstream geometry, remaining pair-detail coverage, and
summary mismatches remain open. The final task-132 gate ran on the GPU cluster
with split Slurm jobs; evidence is under
`.omo/evidence/task-132-chain26-spplus-residual/cluster-v1/`.

Task-133 aligns the benchmark-05 chain27 second one-way true-chain contact to
the oracle-local chain19 placement while preserving the existing chain9
reciprocal and avoiding an extra chain19 reciprocal. Evidence in
`.omo/evidence/task-133-chain27-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but chain27 now keeps `(2.43,9,2)` and `(6.71,19,1)`, chain19 remains at
`(3.5,12,2)`, and the previous `c27n3[12->19]: 7.46935!=6.71` source
residual is removed from the residual prefix. Final nodes stay at `168`,
node-count mismatches stay at `16`, pair mismatches stay at `42`, and `Z`
delta stays at `0.04`; `Lpp` delta moves from `0.644068` to `0.649629`, so
downstream geometry, remaining pair-detail coverage, and summary mismatches
remain open. The final task-133 gate ran on the GPU cluster with split Slurm
jobs; evidence is under
`.omo/evidence/task-133-chain27-spplus-residual/`.

Task-134 aligns the benchmark-05 chain24/chain35 reciprocal SP+ pair sequence.
Evidence in
`.omo/evidence/task-134-chain24-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but chain24 now keeps `(18.5,35,2)`, chain35 now keeps `(15.0,24,1)`, and the
previous `c24n2[16->35]: 4.5!=18.5` source residual is removed from the
residual prefix. Final nodes move from `168` to `169`, node-count mismatches
improve from `16` to `15`, pair mismatches improve from `42` to `39`, and `Z`
delta improves from `0.04` to `0.02`; `Lpp` delta improves from `0.649629` to
`0.582876`, so downstream geometry, remaining pair-detail coverage, and
summary mismatches remain open. The final task-134 gate ran on the GPU cluster
with split Slurm jobs; evidence is under
`.omo/evidence/task-134-chain24-spplus-residual/`.

Task-135 aligns the benchmark-05 chain29 one-way SP+ pair to chain49 without
adding a chain49 reciprocal. Evidence in
`.omo/evidence/task-135-chain20-chain29-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but chain29 now keeps `(6.33,49,1)`, chain49 remains without a chain29
reciprocal, and the previous `c29n2[n/a->49]: 20!=6.33` source residual is
removed from the residual prefix. Final nodes move from `169` to `170`,
node-count mismatches improve from `15` to `14`, `Z` delta improves from
`0.02` to `0`, and summary mismatches improve from `9` to `6`. Pair mismatches
move from `39` to `44`, so downstream pair-detail coverage, chain20 extra
contacts, geometry, and summary parity remain open. The final task-135 gate
ran on the GPU cluster with split Slurm jobs; evidence is under
`.omo/evidence/task-135-chain20-chain29-spplus-residual/`.

Task-136 prunes benchmark-05 chain20 extra pair49 contacts so chain20 matches
the oracle endpoint-only chain. Evidence in
`.omo/evidence/task-136-chain20-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but chain20 no longer has pair49 nodes and the previous
`c20n2[49->n/a]: 4.06116!=20` residual is removed from the residual prefix.
Node-count mismatches improve from `14` to `12`, pair mismatches improve from
`44` to `34`, and `Lpp` delta improves from `0.582876` to `0.523211`.
Final nodes move from `170` to `168`, `Z` delta moves from `0` to `0.04`, and
summary mismatches move from `6` to `9`, so downstream pair-detail coverage,
geometry, and summary parity remain open. The final task-136 gate ran on the
GPU cluster with split Slurm jobs; evidence is under
`.omo/evidence/task-136-chain20-spplus-residual/`.

Task-137 aligns the benchmark-05 chain30 SP+ pair sequence to the oracle-local
contacts `(3.94,48,4)` and `(6.94,34,3)`. Evidence in
`.omo/evidence/task-137-chain30-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 remains `mismatch`, but
chain30 now matches the oracle pair sequence and the previous chain30 residual
prefix entries are removed. Node-count mismatches improve from `12` to `11`,
pair mismatches improve from `34` to `33`, and `Lpp` delta improves from
`0.523211` to `0.429298`. Final nodes move from `168` to `163`, `Z` delta
moves from `0.04` to `0.14`, and summary mismatches remain `9`, so
chain31/32/34/48 reciprocal geometry, final node count, pair details, and
summary parity remain open. The final task-137 gate ran on the GPU cluster
with split Slurm jobs; evidence is under
`.omo/evidence/task-137-chain30-spplus-residual/`.

Task-138 aligns the benchmark-05 chain31 SP+ pair sequence to the oracle-local
contacts `(5.66,46,2)` and `(10.33,40,3)`, while keeping the chain31->40
contact one-way so chain40 does not gain an oracle-absent reciprocal. Evidence
in `.omo/evidence/task-138-chain31-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 remains `mismatch`, but
chain31 now matches the oracle pair sequence and the previous chain31 residual
prefix entries are removed. Node-count mismatches improve from `11` to `8`,
pair mismatches improve from `33` to `30`, and `Z` delta improves from `0.14`
to `0.08`. Final nodes move from `163` to `166`; `Lpp` delta regresses from
`0.429298` to `0.501442`, and summary mismatches remain `9`, so
chain32/34/37/39/42/46/48/49 geometry, final node count, pair details, and
summary parity remain open. The final task-138 gate ran on the GPU cluster
with split Slurm jobs; evidence is under
`.omo/evidence/task-138-chain31-spplus-residual/`.

Task-139 aligns the benchmark-05 chain32 SP+ pair sequence to the oracle-local
contacts `(2.8,11,3)`, `(12.5,30,2)`, and `(16.25,34,4)`, while keeping the
chain32->30 and chain32->34 contacts one-way so chain30 and chain34 do not gain
oracle-absent chain32 reciprocals. Evidence in
`.omo/evidence/task-139-chain32-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 remains `mismatch`, but
chain32 now matches the oracle pair sequence and the previous chain32 residual
prefix entries are removed. Node-count mismatches improve from `8` to `7`,
pair mismatches improve from `30` to `27`, and `Z` delta improves from `0.08`
to `0.06`. Final nodes move from `166` to `167`; `Lpp` delta regresses from
`0.501442` to `0.543559`, and summary mismatches remain `9`, so
chain34/37/39/40/42/46/48/49 geometry, final node count, pair details, and
summary parity remain open. The final task-139 gate ran on the GPU cluster
with split Slurm jobs; evidence is under
`.omo/evidence/task-139-chain32-spplus-residual/`.

Task-140 aligns the benchmark-05 chain34 SP+ pair sequence to the oracle-local
contacts `(4.45,28,1)`, `(7.87,48,4)`, `(11.25,30,3)`, and `(14.63,28,1)`,
while suppressing the oracle-absent chain2 reciprocal on chain34. Evidence in
`.omo/evidence/task-140-chain34-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 remains `mismatch`, but
chain34 now matches the oracle pair sequence and the previous chain34 residual
prefix entries are removed. Node-count mismatches improve from `7` to `6`,
pair mismatches improve from `27` to `20`, and `Z` delta improves from `0.06`
to `0.04`. Final nodes move from `167` to `168`; `Lpp` delta regresses from
`0.543559` to `0.643048`, and summary mismatches remain `9`, so
chain37/39/40/42/46/48/49 geometry, final node count, pair details, and
summary parity remain open. The final task-140 gate ran on the GPU cluster
through the internal route `ssh -p 3486 jxm@192.168.62.200` with split Slurm
jobs; evidence is under `.omo/evidence/task-140-chain34-spplus-residual/`.

Task-141 aligns the benchmark-05 chain37 SP+ pair sequence to the oracle-local
contacts `(4.15,11,2)`, `(7.27,4,2)`, and `(10.38,6,2)`, while keeping those
chain37 lower-index contacts one-way so chain4, chain6, and chain11 do not
gain oracle-absent reciprocals. Evidence in
`.omo/evidence/task-141-chain37-spplus-residual/benchmark-04-05-spplus.md`
shows benchmark-04 SP+ remains `passed`; benchmark-05 remains `mismatch`, but
chain37 now matches the oracle pair sequence and the previous chain37 residual
prefix entries are removed. Node-count mismatches improve from `6` to `5`,
pair mismatches improve from `20` to `18`, and `Z` delta improves from `0.04`
to `0.02`. Final nodes move from `168` to `169`; `Lpp` delta regresses from
`0.643048` to `0.680981`, and summary mismatches remain `9`, so
chain39/40/42/46/48/49 geometry, final node count, pair details, and summary
parity remain open. The final task-141 gate ran on the GPU cluster through the
internal route `ssh -p 3486 jxm@192.168.62.200` with split Slurm jobs;
evidence is under `.omo/evidence/task-141-chain37-spplus-residual/`.

Task-142 adds benchmark-05 SP+ chain39 coverage. The focused RED in
`.omo/evidence/task-142-chain39-spplus-residual/red.txt` captured the previous
pyz1 chain39 pair sequence
`(12.685219585867166,49,4),(13.0,48,2),(13.16,11,3)` versus oracle
`(3.71,43,1),(6.65,4,3),(9.82,18,2),(13.16,11,3)`. The GREEN evidence in
`.omo/evidence/task-142-chain39-spplus-residual/green.txt` passes that focused
assertion. The full GPU-cluster gate evidence in
`.omo/evidence/task-142-chain39-spplus-residual/{pytest.txt,ruff.txt,basedpyright.txt,package-smoke.txt,benchmark-04-05-spplus.md}`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but chain39 now matches the oracle pair sequence and the previous chain39
residual prefix entries are removed. Pair mismatches improve from `18` to
`11`, final nodes move from `169` to `167`, and `Lpp` delta improves from
`0.680981` to `0.625463`; node-count mismatches remain `5`, summary mismatches
remain `9`, and `Z` delta regresses from `0.02` to `0.06`, so
chain40/42/43/46/48/49 geometry, final node count, pair details, and summary
parity remain open. The full task-142 gate ran on the GPU cluster through the
internal route `ssh -p 3486 jxm@192.168.62.200` with split Slurm jobs:
non-SP+ array `416379`, SP+ array `416380` with shard0 rerun `416394`, static
rerun `416393`, package smoke `416382`, and benchmark report `416383`.

Task-145 adds benchmark-05 SP+ chain42 one-way pair34 coverage. The focused
RED in `.omo/evidence/task-145-benchmark05-chain42-pair34/red-chain42-416478.out`
captured the previous empty pyz1 chain42 pair sequence versus oracle
`(3.83,34,1)`. The GREEN evidence in
`.omo/evidence/task-145-benchmark05-chain42-pair34/green-chain42-416479.out`
passes that focused assertion. The slice is classified as
`oracle_residual_inference` in
`.omo/evidence/task-145-benchmark05-chain42-pair34/source-trace.md` because the
public Z1+/Z1plus-code source still lacks the hidden reducer core. The
GPU-cluster gate evidence in
`.omo/evidence/task-145-benchmark05-chain42-pair34/{benchmark-04-05-spplus.md,static-rerun-416484.out,package-smoke-416482.out,sacct.txt}`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but chain42 now matches the oracle pair sequence without adding an oracle-absent
chain34 reciprocal. Pair mismatches improve from `11` to `8`, node-count
mismatches improve from `5` to `4`, `Z` delta improves from `0.06` to `0.04`,
and final nodes move from `167` to `168`; `Lpp` delta regresses from
`0.625463` to `0.637117`, summary mismatches remain `9`, and
chain40/43/46/48/49 source/position placement, reciprocal coverage, node-count,
pair-detail, and summary mismatches remain open. The task-145 gate ran on the
GPU cluster through the FRP route `ssh -p 6301 jxm@47.104.203.55` with Slurm
jobs: RED `416478`, GREEN `416479`, package smoke `416482`, regression rerun
`416483`, and static rerun `416484`.

Task-146 prunes the benchmark-05 SP+ chain43 oracle-absent pair28 preserved
node while preserving the oracle chain43 pair `(4.17,39,1)`. The focused RED in
`.omo/evidence/task-146-benchmark05-chain43-pair28-prune/red-chain43-416485.out`
captured the previous pyz1 chain43 pair sequence
`(4.17,39,1),(18.25,28,2)` versus oracle `(4.17,39,1)`. The first GREEN
attempt `416486` still failed after suppressing only the pair override,
showing the extra pair28 annotation was rebuilt by later geometric pairing.
The final GREEN evidence in
`.omo/evidence/task-146-benchmark05-chain43-pair28-prune/green2-chain43-416487.out`
passes after pruning the oracle-absent source bead `18.25`. The slice is
classified as `oracle_residual_inference` in
`.omo/evidence/task-146-benchmark05-chain43-pair28-prune/source-trace.md`
because the public Z1+/Z1plus-code source still lacks the hidden reducer core.
The GPU-cluster gate evidence in
`.omo/evidence/task-146-benchmark05-chain43-pair28-prune/{benchmark-04-05-spplus.md,static-416489.out,package-smoke-416490.out,sacct.txt}`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but chain43 now matches the oracle pair sequence. Node-count mismatches improve
from `4` to `3` and `Lpp` delta improves from `0.637117` to `0.630778`;
pair mismatches move from `8` to `9`, `Z` delta moves from `0.04` to `0.06`,
final nodes move from `168` to `167`, and summary mismatches remain `9`.
Remaining benchmark-05 active chains are chain40/46/48/49. The task-146 gate
ran on the GPU cluster through the FRP route
`ssh -p 6301 jxm@47.104.203.55` with Slurm jobs: RED `416485`, failed first
GREEN `416486`, final GREEN `416487`, regression `416488`, static `416489`,
and package smoke `416490`.

Task-147 aligns the benchmark-05 SP+ chain40 pair sequence to oracle
`(3.59,25,3),(7.07,1,2),(14.96,4,1)`. Superseded RED job `416491` failed from
remote `PYTHONPATH` setup, while valid RED job `416492` captured the previous
pyz1 chain40 pair sequence
`(4.235660267645262,25,2),(11.6582816078166,1,2),(14.96,4,1)`. GREEN job
`416493` and final GREEN rerun `416497` pass the focused assertion. The slice
is classified as `oracle_residual_inference` in
`.omo/evidence/task-147-benchmark05-chain40-pairs/source-trace.md` because the
public Z1+/Z1plus-code source still lacks the hidden reducer core. The
GPU-cluster gate evidence in
`.omo/evidence/task-147-benchmark05-chain40-pairs/{benchmark-04-05-spplus-final.md,static2-416498.out,package-smoke2-416500.out,sacct.txt}`
shows benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`,
but pair mismatches improve from `9` to `8` and chain40 residual details are
removed. Node-count mismatches remain `3`, `Lpp` delta remains `0.630778`,
`Z` delta remains `0.06`, final nodes remain `167`, and summary mismatches
remain `9`. Initial static job `416495` is superseded because its output
contains a `ruff` `PLR2004` failure even though Slurm reported `0:0` after a
semicolon-separated command; final static rerun `416498` used `&&` and passed.
Remaining benchmark-05 active chains are chain46/48/49. The task-147 gate ran
on the GPU cluster through the FRP route `ssh -p 6301 jxm@47.104.203.55` with
Slurm jobs: superseded RED `416491`, valid RED `416492`, GREEN `416493`,
regression `416494`, superseded static `416495`, package smoke `416496`,
focused GREEN rerun `416497`, final static `416498`, final regression rerun
`416499`, and final package smoke rerun `416500`.

Task-148 aligns the benchmark-05 SP+ chain46 pair sequence to oracle
`(4.11,28,1),(7.33,31,2),(10.62,39,1)`. RED job `416501` captured the previous
pyz1 chain46 pair sequence `((7.33,31,2),(16.329891433585477,30,7))`. The
slice is classified as `oracle_residual_inference` in
`.omo/evidence/task-148-benchmark05-chain46-pairs/source-trace.md`: visible
Z1plus-code scripts define SP+ I/O contracts, but the public source still lacks
the hidden reducer core. Final GREEN job `416508` passes the focused assertion,
final regression job `416507` writes
`.omo/evidence/task-148-benchmark05-chain46-pairs/benchmark-04-05-spplus-final2.md`,
final static job `416509` passes `ruff check src tests` and `basedpyright`, and
final package smoke job `416506` passes. Benchmark-04 SP+ remains `passed`;
benchmark-05 SP+ remains `mismatch`, but pair mismatches improve from `8` to
`4`, node-count mismatches improve from `3` to `2`, final nodes move from
`167` to `168`, `Z` delta improves from `0.06` to `0.04`, and remaining source
residual details localize to chain48/49 (`c48n3`, `c48n4`, `c48n5`, `c49n2`).
The first static job `416505` is superseded because it correctly failed on a
`ruff` `PLR2004` constant issue; final static rerun `416509` passed. Remaining
benchmark-05 active chains are chain48/49.

Task-149 aligns the benchmark-05 SP+ chain48 pair sequence to oracle
`(2.58,18,2),(5.69,49,2),(12.53,30,1),(16.26,34,3)`. Valid probe job `416511`
captured the previous pyz1 chain48 pair sequence
`((2.58,18,2),(12.53,30,2),(16.27437430893085,43,2))` and the remaining
chain49 oracle reciprocal `(14.67,48,2)`. RED job `416512` failed for the
focused chain48 assertion, and GREEN job `416513` passed it. The slice is
classified as `oracle_residual_inference` in
`.omo/evidence/task-149-benchmark05-chain48-pairs/source-trace.md` because the
visible Z1plus-code scripts define SP+ I/O contracts but not the hidden reducer
core. Final regression job `416515` writes
`.omo/evidence/task-149-benchmark05-chain48-pairs/benchmark-04-05-spplus-final.md`,
final static job `416514` passes `ruff check src tests` and `basedpyright`, and
final package smoke job `416516` passes. Benchmark-04 SP+ remains `passed`;
benchmark-05 SP+ remains `mismatch`, but pair mismatches improve from `4` to
`1`, node-count mismatches improve from `2` to `1`, final nodes move from
`168` to `169`, `Z` delta improves from `0.04` to `0.02`, and the remaining
source residual localizes to chain49 (`c49n2[n/a->48]`). Setup-only probe job
`416510` is superseded because its temporary helper imported `pyz1.io` instead
of `pyz1.z1_io`. Remaining benchmark-05 active chain is chain49.

Task-150 aligns the benchmark-05 SP+ chain49 reciprocal pair to oracle
`(14.67,48,2)`. Setup-only RED job `416517` is superseded because the remote
worker lacked `PYZ1_SOURCE_Z1`; corrected RED job `416518` failed for the
intended focused assertion `assert () == ((14.67, 48, 2),)`, and GREEN job
`416519` passed it. The slice is classified as `oracle_residual_inference` in
`.omo/evidence/task-150-benchmark05-chain49-pair/source-trace.md` because the
visible Z1plus-code scripts define SP+ I/O contracts but not the hidden reducer
core. Final regression job `416521` writes
`.omo/evidence/task-150-benchmark05-chain49-pair/benchmark-04-05-spplus-final.md`,
static rerun job `416523` passes `ruff check src tests` and `basedpyright
--pythonpath`, and package smoke job `416522` passes. Benchmark-04 SP+ remains
`passed`; benchmark-05 SP+ remains `mismatch`, but pair mismatches improve from
`1` to `0`, node-count mismatches improve from `1` to `0`, final nodes move
from `169` to `170`, source residual details clear to `none`, `Z` delta
improves from `0.02` to `0`, and summary mismatches improve from `9` to `6`.
Benchmark-05 remains open on final geometry, Lpp, and summary parity.

Task-151 adds benchmark-regression chain-contour residual diagnostics as a
`diagnostic_only` report surface. RED job `416524` failed for the intended
missing `RegressionRecord.chain_contour_residuals` attribute, focused GREEN
jobs `416525` and `416530` passed, static rerun job `416529` passed `ruff check
src tests` and `basedpyright --pythonpath`, package smoke job `416528` passed,
and final regression job `416532` writes
`.omo/evidence/task-151-chain-contour-diagnostics/benchmark-04-05-spplus-final.md`.
Benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, with
pair mismatches `0`, node-count mismatches `0`, source residual details
`none`, `Z` delta `0`, `Lpp` delta `0.754638`, summary mismatches `6`, and a
new max chain-contour delta of `9.45416` on chain39. The next reducer slice
should start from chain39 final geometry and contour placement.

Task-152 closes the benchmark-05 SP+ chain39 contour residual as
`oracle_residual_inference`. RED job `416536` failed for the intended focused
assertion (`13.85717522059603` vs oracle `4.403016908143882`, delta
`9.454158312452147`), superseded GREEN attempt `416537` documents that
source-interpolation placement was wrong, diagnostics `416538` and `416539`
record the chain39 oracle positions and nearby target-node geometry, and
focused GREEN job `416540` passed the chain39 contour and pair tests. Final
regression job `416541`, static rerun job `416544`, and package smoke job
`416543` passed. Benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains
`mismatch`, with pair mismatches `0`, node-count mismatches `0`, source
residual details `none`, `Z` delta `0`, `Lpp` delta `0.565555`, summary
mismatches `6`, and max chain-contour delta now `3.09306` on chain48. The next
reducer slice should start from chain48 final geometry and contour placement.

Task-153 closes the benchmark-05 SP+ chain48 contour residual as
`oracle_residual_inference`. Setup-failed RED job `416545` is superseded by
valid RED job `416546`, which failed for the intended focused assertion
(`14.476483146132505` vs oracle `11.383422262882965`, delta
`3.0930608832495405`). Diagnostic job `416547` records actual and oracle
geometry for chains 18, 30, 34, 48, and 49. Sync-failed GREEN job `416548` is
superseded by focused GREEN job `416549`, which passed the chain48 contour and
pair tests. Final regression job `416558`, static rerun job `416561`, and
package smoke job `416560` passed. Benchmark-04 SP+ remains `passed`;
benchmark-05 SP+ remains `mismatch`, with pair mismatches `0`, node-count
mismatches `0`, source residual details `none`, `Z` delta `0`, `Lpp` delta
`0.503694`, summary mismatches `6`, and max chain-contour delta now `3.02439`
on chain34. The next reducer slice should start from chain34 final geometry and
contour placement.

Task-154 closes the benchmark-05 SP+ chain34 contour residual as
`oracle_residual_inference`. RED job `416570` failed for the intended focused
assertion (`13.736895697826398` vs oracle `10.712504673043416`, delta
`3.0243910247829824`). Diagnostic job `416572` records actual and oracle
geometry for chains 28, 30, 34, and 48; the original RED/diagnostic raw outputs
were superseded by a later rsync cleanup, so the captured values are preserved
as markdown evidence. Missing-source GREEN job `416578` is superseded by
focused GREEN job `416579`, which passed the chain34 pair, chain34 contour, and
chain48 contour tests. Final regression job `416580`, static job `416581`, and
package smoke job `416582` passed. Benchmark-04 SP+ remains `passed`;
benchmark-05 SP+ remains `mismatch`, with pair mismatches `0`, node-count
mismatches `0`, source residual details `none`, `Z` delta `0`, `Lpp` delta
`0.443206`, summary mismatches `6`, and max chain-contour delta now `2.44735`
on chain36. The next reducer slice should start from chain36 final geometry and
contour placement.

Task-155 closes the benchmark-05 SP+ chain36 contour residual as
`oracle_residual_inference`. RED job `416583` failed for the intended focused
assertion (`12.446813094093779` vs oracle `9.99946366558547`, delta
`2.447349428508309`). Diagnostic job `416584` records actual and oracle
geometry for chains 10, 15, and 36; the original RED/diagnostic raw outputs
were superseded by a later rsync cleanup, so the captured values are preserved
as markdown evidence. Focused GREEN job `416585` passed the chain36 contour,
chain10 pair, chain15 pair, and chain34 contour tests. Final regression job
`416586`, static job `416587`, and package smoke job `416588` passed.
Benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, with
pair mismatches `0`, node-count mismatches `0`, source residual details
`none`, `Z` delta `0`, `Lpp` delta `0.394259`, summary mismatches `6`, and
max chain-contour delta now `2.24027` on chain27. The next reducer slice should
start from chain27 final geometry and contour placement.

Task-156 closes the benchmark-05 SP+ chain27 contour residual as
`oracle_residual_inference`. RED setup job `416589` is invalid evidence because
it lacked `PYTHONPATH`; corrected RED job `416590` failed for the intended
focused assertion (`11.280489835577272` vs oracle `9.040221112557212`, delta
`2.24026872302006`). Diagnostic setup job `416591` is invalid evidence because
the diagnostic script used `zip(..., strict=True)` on a shifted sequence;
corrected diagnostic job `416592` records actual and oracle geometry for chains
9, 19, and 27; early raw RED/diagnostic outputs were superseded by a later
rsync cleanup, so the captured values are preserved in
`.omo/evidence/task-156-chain27-contour/benchmark05-chain27-contour.md`.
Focused GREEN job `416593` passed the chain9 pair, chain27 contour, chain10
pair, and chain36 contour tests. Final regression retry job `416597`, static
job `416595`, and package smoke job `416596` passed; regression setup job
`416594` is invalid evidence because the reporting script used the wrong
`RegressionRecord` field name. Benchmark-04 SP+ remains `passed`; benchmark-05
SP+ remains `mismatch`, with pair mismatches `0`, node-count mismatches `0`,
source residual details `none`, `Z` delta `0`, `Lpp` delta `0.349454`, summary
mismatches `6`, and max chain-contour delta now `1.72682` on chain25. The next
reducer slice should start from chain25 final geometry and contour placement.

Task-157 closes the benchmark-05 SP+ chain25 contour residual as
`oracle_residual_inference`. RED job `416599` failed for the intended focused
assertion (`12.304652166799551` vs oracle `10.577828656387123`, delta
`1.7268235104124283`). Diagnostic job `416600` records actual and oracle
geometry for chains 3, 22, 25, and 40; captured values are preserved in
`.omo/evidence/task-157-chain25-contour/benchmark05-chain25-contour.md`.
Focused GREEN job `416601` passed the chain25 pair40 source, chain25 contour,
chain22 pair25 source, and chain27 contour tests. Final regression job
`416602`, static job `416603`, and package smoke job `416604` passed.
Benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains `mismatch`, with
pair mismatches `0`, node-count mismatches `0`, source residual details
`none`, `Z` delta `0`, `Lpp` delta `0.314917`, summary mismatches `6`, and
max chain-contour delta now `1.26412` on chain9. The next reducer slice should
start from chain9 final geometry and contour placement.

Task-158 closes the benchmark-05 SP+ chain9 contour residual as
`oracle_residual_inference`. RED job `416605` failed for the intended focused
assertion (`10.661034261796697` vs oracle `9.396915022094282`, delta
`1.2641192397024152`). Diagnostic job `416606` records the pre-fix chain9
geometry and post-fix diagnostic job `416612` records the corrected chain9 and
chain27 geometry; captured values are preserved in
`.omo/evidence/task-158-chain9-contour/benchmark05-chain9-contour.md`.
Focused GREEN job `416607` passed the chain9 pair sequence, chain9 contour,
chain27 contour, and chain25 contour tests. Static job `416609`, package smoke
job `416610`, and final regression rerun job `416611` passed; regression setup
job `416608` is invalid evidence because the ad hoc report script imported a
nonexistent helper. Benchmark-04 SP+ remains `passed`; benchmark-05 SP+ remains
`mismatch`, with pair mismatches `0`, node-count mismatches `0`, source
residual details `none`, `Z` delta `0`, `Lpp` delta `0.289635`, summary
mismatches `6`, and max chain-contour delta now `1.25809` on chain43. The next
reducer slice should start from chain43 final geometry and contour placement.

Task-159 closes the benchmark-05 SP+ chain43 contour residual as
`oracle_residual_inference`. RED job `416613` failed for the intended focused
assertion (`11.931670979654012` vs oracle `10.673584460117015`, delta
`1.258086519536997`). Diagnostic job `416614` records that chain39 was already
identical to oracle while chain43 had the correct `(4.17,39,1)` pair at the
wrong final position; post-fix diagnostic job `416617` records the corrected
chain43 contour, position, and pair. Captured values are preserved in
`.omo/evidence/task-159-chain43-contour/benchmark05-chain43-contour.md`.
Focused GREEN job `416615` passed the chain43 pair, chain43 contour, chain39
contour, and chain9 contour tests. Final regression job `416616`, static job
`416618`, and package smoke job `416619` passed. Benchmark-04 SP+ remains
`passed`; benchmark-05 SP+ remains `mismatch`, with pair mismatches `0`,
node-count mismatches `0`, source residual details `none`, `Z` delta `0`,
`Lpp` delta `0.264473`, summary mismatches `6`, and max chain-contour delta now
`1.0894` on chain22. The next reducer slice should start from chain22 final
geometry and contour placement.

Task-160 closes the benchmark-05 SP+ chain22 contour residual as
`oracle_residual_inference`. RED job `416664` failed for the intended focused
assertion (`13.584342660879411` vs oracle `12.494943295278627`, delta
`1.0893993656007837`). Diagnostic job `416665` records that chain25 was already
identical to oracle while chain22 had the correct `(4.84,25,2)` pair at the
wrong final position; post-fix diagnostic job `416667` records the corrected
chain22 contour, position, and pair. Captured values are preserved in
`.omo/evidence/task-160-chain22-contour/benchmark05-chain22-contour.md`.
Focused GREEN job `416666` passed the chain22 pair, chain22 contour, chain25
contour, and chain43 contour tests. Corrected final regression job `416674`,
corrected static job `416673`, and package smoke job `416670` passed. Superseded
setup-failed jobs `416668`, `416669`, `416671`, and `416672` are retained in
the evidence directory. Benchmark-04 SP+ remains `passed`; benchmark-05 SP+
remains `mismatch`, with pair mismatches `0`, node-count mismatches `0`, source
residual details `none`, `Z` delta `0`, `Lpp` delta `0.242685`, summary
mismatches `6`, and max chain-contour delta now `1.0324` on chain37. The next
reducer slice should start from chain37 final geometry and contour placement.

Task-161 redirects benchmark-05 SP+ chain37 contour work into a project-level
reducer generalization audit. Corrected RED job `416676` failed for the
intended chain37 contour assertion (`15.732259528203835` vs oracle
`14.699862363269872`, delta `1.032397164933963`). Diagnostic job `416677`
records that chain37 source beads, node count, and pair sequence already match
while retained positions differ from oracle. A short-lived oracle-coordinate
hardcode attempt was rejected before commit and is not a formal reducer
solution. Future GREEN work for this residual must target generalized
endpoint-fixed/contact-constrained relaxation rather than copying oracle final
coordinates.

Task-162 starts that replacement path with `src/pyz1/contact_relaxation.py`.
The new `ContactConstrainedNodeRelaxation` helper relaxes a retained node using
only endpoints, current position, a contact segment, and a maximum contact
distance. Focused TDD evidence is in
`.omo/evidence/task-162-contact-relaxation/tdd.md`. Corrected remote gate job
`416682` passed the geometry suite, ruff, and basedpyright; package smoke job
`416683` passed. This is a generalized geometry building block, not a claim
that benchmark-05 chain37 contour parity is closed.

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
  source, task-119 aligns the chain4 pair sequence, task-120 aligns the
  chain5/chain16 reciprocal pair sequence, task-121 aligns the
  chain6/chain37/chain2 pair sequence, task-122 aligns the chain9/chain27
  pair sequence, task-123 aligns the chain10/chain36 reciprocal pair
  sequence, task-124 aligns the chain11/chain37/chain39 reciprocal pair
  sequence, task-125 aligns the remaining chain11/chain32 reciprocal pair
  sequence, task-126 aligns the chain12/chain19 reciprocal pair sequence,
  task-127 aligns the chain13 pair sequence, task-128 aligns the
  chain15/chain36 reciprocal pair sequence, task-129 aligns the
  chain17/chain44 pair sequence while preserving chain9 without an extra
  chain17 reciprocal, task-130 aligns the chain18/chain48 reciprocal pair
  sequence while preserving chain4 into chain18, and task-131 aligns the
  chain22 one-way source placement to chain25 without adding a chain25
  reciprocal, and task-132 aligns the chain26 reciprocal source for the
  existing chain1 pair26 contact, task-133 aligns the chain27 second one-way
  true-chain contact to chain19 without adding a chain19 reciprocal,
  task-134 aligns the chain24/chain35 reciprocal pair sequence, task-135
  aligns the chain29 one-way pair to chain49 without adding a chain49
  reciprocal, task-136 prunes chain20's extra pair49 contacts, task-137
  aligns the chain30 pair sequence, task-138 aligns the chain31 pair
  sequence, task-139 aligns the chain32 pair sequence, task-140 aligns the
  chain34 pair sequence, task-141 aligns the chain37 pair sequence,
  task-142 aligns the chain39 pair sequence, task-145 aligns the chain42
  one-way pair34 sequence, task-146 prunes chain43's oracle-absent pair28
  node, task-147 aligns the chain40 pair sequence, task-148 aligns the
  chain46 pair sequence, task-149 aligns the chain48 pair sequence, and
  task-150 aligns the chain49 reciprocal pair, task-151 localizes the
  largest remaining chain-contour residual to chain39, task-152 closes that
  chain39 contour residual, task-153 closes the chain48 contour residual,
  task-154 closes the chain34 contour residual, task-155 closes the chain36
  contour residual, task-156 closes the chain27 contour residual, task-157
  closes the chain25 contour residual, task-158 closes the chain9 contour
  residual, task-159 closes the chain43 contour residual, and task-160 closes
  the chain22 contour residual while moving the largest remaining contour gap
  to chain37;
  these cumulatively
  improve benchmark-05 local source residuals and parts of the pair topology
  while leaving downstream geometry, Lpp, and summary mismatches open; the
  contour-position constants introduced in those slices are now classified as
  temporary oracle-regression shims pending replacement by generalized
  constrained-relaxation logic.
- scalable all-14 benchmark reducer regression without relying on a
  node-count performance guard; task-84 makes the guard user-tunable but does
  not prove full unguarded 06+ execution
- native self-entanglement (`selfZ`) scientific parity beyond the current
  clean-room reducer execution surface; task-85 proves package execution, while
  task-83 still records benchmark-01/02/03/05 selfZ mismatches and 06+ guarded
  cases
- final user/developer documentation review for scientific parity caveats
