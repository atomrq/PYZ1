# pyz1 output writer evidence

Date: 2026-07-03

## Scope

This slice adds writers for the output objects already modeled in `pyz1`:

- `Z1+summary.dat`
- `PPA-summary.dat`
- `PPA+summary.dat`
- `Z1+SP.dat`
- `PPA.dat`
- `PPA+.dat`
- `Z1+initconfig.dat`
- `Ree_values.dat`
- `Lpp_values.dat`
- `N_values.dat`
- `Z_values.dat`

The summary filenames share the same 15-column row structure. The path
filenames share the same shortest-path node structure.

## Implementation

Files:

```text
src/pyz1/initconfig_io.py
src/pyz1/output_write.py
src/pyz1/output_io.py
src/pyz1/output_values.py
tests/test_initconfig_io.py
tests/test_output_io.py
tests/test_output_values.py
```

Public writer API exposed through `pyz1.output_io`:

```text
format_summary_text
write_summary_file
format_shortest_path_text
write_shortest_path_file
```

The writer serializes `nan` summary fields as the Fortran overflow token
`************`, matching the parser behavior added for PPA/PPA+ oracle files.

`Z1+initconfig.dat`, `PPA.dat`, and `PPA+.dat` are handled as coordinate
snapshot outputs: chain count, box lengths, per-chain node count, and one
`x y z` row per node. `Z1+initconfig.dat` may carry the trailing Z1+ shear
metadata `-1` plus a shear value.

`*_values.dat` files are parsed as per-chain value streams. The parser accepts
both one-value-per-line oracle output and whitespace-separated columns.

## Verification

Red evidence:

```text
.omo/evidence/task-5-writer-red-pyz1-cleanroom-reproduction.txt
```

Focused gate:

```text
.omo/evidence/task-5-writer-quality-pyz1-cleanroom-reproduction.txt
tests/test_output_io.py: 9 passed
ruff: All checks passed
basedpyright: 0 errors, 0 warnings, 0 notes
```

Full gate:

```text
.omo/evidence/final-gate-pyz1-output-writer-20260703.txt
.omo/evidence/final-gate-pyz1-values-initconfig-20260703.txt
pytest: 36 passed
ruff: All checks passed
basedpyright: 0 errors, 0 warnings, 0 notes
```

LOC check:

```text
src/pyz1/initconfig_io.py 132
src/pyz1/output_io.py     235
src/pyz1/output_values.py  48
src/pyz1/output_write.py   65
tests/test_initconfig_io.py 74
tests/test_output_io.py   115
tests/test_output_values.py 42
```

## Todo 5 Status

Complete for the output files named by Todo 5. The remaining project work is in
later todos: estimator generation, oracle long-run completion, PPA/PPA+ port,
and clean-room geometrical reduction.
