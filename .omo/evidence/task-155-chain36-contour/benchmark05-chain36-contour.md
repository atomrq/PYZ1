# Task 155 benchmark-05 chain36 contour

Focused RED job `416583` failed for the intended chain36 contour residual:

- actual chain36 contour: `12.446813094093779`
- oracle chain36 contour: `9.99946366558547`
- delta: `2.447349428508309`

Diagnostic job `416584` printed actual/oracle chain10, chain15, and chain36 node positions. Chain36 pair/source metadata was already closed, but the two internal node positions differed from oracle.

Focused GREEN job `416585` passed:

- `test_reduce_snapshot_when_benchmark05_chain36_contour_matches_oracle`
- `test_reduce_snapshot_when_benchmark05_chain10_matches_oracle_pair`
- `test_reduce_snapshot_when_benchmark05_chain15_matches_oracle_pair`
- `test_reduce_snapshot_when_benchmark05_chain34_contour_matches_oracle`

Final regression job `416586` keeps benchmark-04 SP+ `passed`. Benchmark-05 SP+ remains a true `mismatch`, with pair mismatches, node-count mismatches, source residual details, and `Z` delta closed; max chain-contour residual moved from chain36 to chain27 (`2.24027`).
