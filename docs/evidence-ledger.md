# pyz1 Evidence Ledger

This ledger maps the clean-room reproduction requirements to current repo tests,
local evidence artifacts, and known open boundaries. It is an index, not a
parity claim.

## Current Quality Gates

Latest local gate evidence:

- `.omo/evidence/task-47-ppa-neighbor-list/ppa-focused.txt`: `18 passed`
- `.omo/evidence/task-47-ppa-neighbor-list/pytest.txt`: `109 passed`
- `.omo/evidence/task-47-ppa-neighbor-list/ruff.txt`: `All checks passed!`
- `.omo/evidence/task-47-ppa-neighbor-list/basedpyright.txt`: `0 errors, 0 warnings, 0 notes`

The package smoke runs `python -m pyz1` for default, SP+, PPA, and PPA+ modes
and checks the expected mode-specific output files.

## Requirement Coverage

| Requirement | Current proof | Evidence |
| --- | --- | --- |
| Z1 input parser and typed models | Unit tests for valid inputs, malformed inputs, metadata, true-chain filtering, and model invariants | `tests/test_z1_io.py`, `tests/test_models.py` |
| Z1+ output parser/writer | Summary, SP/SP+, initconfig, value files, PPA, and PPA+ round-trip tests | `tests/test_output_io.py`, `tests/test_output_values.py`, `tests/test_initconfig_io.py` |
| Summary and `Ne` estimators | Estimator unit tests plus oracle-SP-through-pyz1 summary parity for benchmark-04 SP+ | `tests/test_estimators.py`, `tests/test_summary.py`, `tests/test_spplus_regression.py`, `.omo/evidence/task-42-summary-ne-source/` |
| Oracle fixture tooling and parity reporting | Oracle manifest tests, CLI help smoke, benchmark regression report tests, and logged oracle run metadata | `tests/test_oracle.py`, `tests/test_z1plus_parity.py`, `tests/test_spplus_regression.py` |
| Native PPA/PPA+ slices | PPA mode tests, CLI mode tests, package-level smoke, WCA cell-list candidate generation, 12 parseable oracle coordinate-path summary parity cases, and one explicit Fortran-overflow known-invalid fixture | `tests/test_ppa.py`, `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py`, `.omo/evidence/task-46-ppa-summary-oracle-coverage/`, `.omo/evidence/task-47-ppa-neighbor-list/` |
| Clean-room reducer | Geometry primitives, reducer diagnostics, benchmark-04 reducer structure, SP+ pairing, and benchmark regression diagnostics | `tests/test_geometry.py`, `tests/test_z1_reducer.py`, `tests/test_spplus_regression.py` |
| SP+ regression | Pairing comparison, max-node-delta localization, pair-segment geometry diagnostics, and oracle summary source isolation | `tests/test_spplus_regression.py`, `.omo/evidence/task-38-final-node-delta-location/`, `.omo/evidence/task-39-max-node-pair-geometry/`, `.omo/evidence/task-41-spplus-projection-direction/` |
| Package integration smoke | Real module entrypoint smoke for default, SP+, PPA, and PPA+ | `tests/test_package_integration_smoke.py`, `.omo/evidence/task-44-evidence-ledger/` |
| `selfZ` boundary | `-selfZ` is recognized and fails explicitly instead of silently running the default reducer | `tests/test_cli_scaffold.py`, `tests/test_package_integration_smoke.py`, `.omo/evidence/task-45-selfz-explicit-boundary/` |

## Latest SP+ Parity Measurements

Benchmark-04 SP+ regression remains classified as `mismatch`, but the current
measured deltas are localized:

- `lpp_delta=0.0002905926055403185`
- `z_delta=0.0`
- `pairing_mismatches=0`
- `node_count_mismatches=0`
- `max_node_position_delta=0.0008949492811423296`
- max-delta node: chain 1, node 2, source bead 3.5
- summary mismatches: `ne_classical_coil: 10.486 != 10.485`; `ne_modified_coil: 643.254 != 641.605`

The summary formula itself is not the active blocker: feeding the Z1+ oracle
SP+ path into `pyz1` summary gives `ne_modified_coil=641.606194063256` against
Z1+ `641.605`. The remaining summary mismatch comes from reducer geometry/Lpp,
not the estimator formula.

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
cross-boundary near pair, exact cutoff filtering, and same-chain exclusion.

Current candidate-count evidence from
`.omo/evidence/task-47-ppa-neighbor-list/candidate-counts.txt`:

- benchmark 01: `nodes=611`, `all_cross_chain_pairs=186000`,
  `wca_candidate_pairs=18452`
- benchmark 05: `nodes=1000`, `all_cross_chain_pairs=490000`,
  `wca_candidate_pairs=1002`

## Open Boundaries

The following are intentionally not claimed complete:

- full PPA/PPA+ benchmark-level runtime parity from native integration output
- default geometrical Z1+ numerical parity across all benchmarks
- scalable all-14 benchmark reducer regression without the current node-count
  performance guard
- native self-entanglement (`selfZ`) behavior beyond the current explicit
  not-implemented CLI boundary
- final user/developer documentation review for scientific parity caveats
