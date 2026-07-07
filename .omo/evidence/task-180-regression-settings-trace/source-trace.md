# Task 180 Regression Settings Trace Source Trace

Classification: `diagnostic_only`

Source context:

- `src/pyz1/regression_cli.py` exposes
  `--contact-relaxation/--no-contact-relaxation` and maps it to an SP+
  `RegressionSettingsOverride`.
- `src/pyz1/regression.py` applies that override through `_settings_for_mode`
  before running the reducer.
- Before this slice, benchmark regression rows only reported `mode=spplus`, so
  the default SP+ path and the contact-relaxation override path were not
  distinguishable in the generated markdown report.

Change rationale:

- Add `contact_relaxation_enabled` to `RegressionRecord`.
- Add a `contact relaxation` column to the benchmark regression report.
- This improves evidence traceability for statistical parity work without
  changing reducer behavior, mismatch diagnostics, or statistical status logic.

Remote evidence:

- RED focused job `416863` failed because `RegressionRecord` did not expose
  `contact_relaxation_enabled`.
- GREEN focused job `416864` passed.
- Static job `416865` passed `ruff` and `basedpyright`.
- Package smoke job `416866` generated the installed CLI report with benchmark
  05 SP+ recorded as `spplus | yes | mismatch | passed`.
- Docs gate job `416868` passed `git diff --check` through a temporary remote
  git index.
