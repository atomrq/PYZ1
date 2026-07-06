# Task 154 benchmark-05 chain34 contour

Focused RED job `416570` failed for the intended chain34 contour residual:

- actual chain34 contour: `13.736895697826398`
- oracle chain34 contour: `10.712504673043416`
- delta: `3.0243910247829824`

Diagnostic rerun job `416572` printed actual/oracle chain28, chain30, chain34, and chain48 node positions. The chain34 internal positions differed from oracle while pair sequence/source beads were already closed.

Focused GREEN rerun job `416579` passed:

- `test_reduce_snapshot_when_benchmark05_chain34_matches_oracle_pairs`
- `test_reduce_snapshot_when_benchmark05_chain34_contour_matches_oracle`
- `test_reduce_snapshot_when_benchmark05_chain48_contour_matches_oracle`

Final regression job `416580` keeps benchmark-04 SP+ `passed`. Benchmark-05 SP+ remains a true `mismatch`, with pair mismatches, node-count mismatches, source residual details, and `Z` delta closed; max chain-contour residual moved from chain34 to chain36 (`2.44735`).
