# pyz1

`pyz1` is a local Python implementation path for reproducing the public Z1+
workflow. It is a clean-room Python package for parsing Z1+/LAMMPS-style polymer
inputs, writing Z1+ compatible outputs, computing summary/`Ne` values, running
native PPA/PPA+ slices, and building a native geometrical Z1 reducer without
using the Linux `Z1+.ex` binary at runtime.

## Quickstart

Local development uses the `pyz1` micromamba environment. On this macOS host,
keep the file-descriptor limit finite for micromamba:

```bash
ulimit -n 1000000; micromamba run -n pyz1 python -m pytest -q
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 --help
```

Run the native default reducer on a Z1 input:

```bash
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 config.Z1
```

Run SP+ pairing mode:

```bash
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 -SP+ config.Z1
```

Run native PPA/PPA+ modes:

```bash
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 -PPA config.Z1
ulimit -n 1000000; micromamba run -n pyz1 python -m pyz1 -PPA+ config.Z1
```

Run the package-level integration smoke:

```bash
ulimit -n 1000000; micromamba run -n pyz1 pytest -q tests/test_package_integration_smoke.py
```

That smoke drives the installed package surface through `python -m pyz1` for
default, SP+, PPA, and PPA+ modes and checks the mode-specific output files.

## Outputs

The package has parser/writer coverage for:

- `Z1+summary.dat`
- `Z1+SP.dat` with optional SP+ `other-chain other-node` columns
- `Z1+initconfig.dat`
- `Ree_values.dat`
- `Lpp_values.dat`
- `N_values.dat`
- `Z_values.dat`
- `PPA.dat`
- `PPA+.dat`
- `PPA-summary.dat`
- `PPA+summary.dat`

Default and SP+ CLI modes currently write `Z1+SP.dat`, `Z1+summary.dat`, and
the `Ree/Lpp/N/Z_values.dat` files. PPA/PPA+ modes write their corresponding
coordinate and summary/value outputs.

## Benchmark Status

The original Linux `Z1+.ex` binary is an oracle for fixtures only; it is not a
runtime dependency of the Python package.

Current regression evidence is written to:

```text
.omo/evidence/pyz1-benchmark-regression.md
```

That report classifies each public benchmark/mode as `passed`, `mismatch`, or
`known-invalid`. The current clean-room reducer is not yet numerically
equivalent to Z1+: `benchmark-04` default/SP+ is reported as a mismatch, and
larger benchmark cases are performance-skipped by a transparent `node_count`
guard until the reducer gets neighbor-list style acceleration.

## Limitations

- The missing public `module-Z1.f90` source means the default geometrical Z1
  reducer is clean-room, not a Fortran translation.
- Default/SP+ reducer parity is not complete. Do not treat current outputs as a
  drop-in replacement for Z1+ scientific production runs.
- PPA/PPA+ has native Python execution and oracle-backed summary slices, but
  full benchmark-level runtime parity remains open.
- The first implementation intentionally avoids GPU, CUDA, CuPy, PyTorch,
  Numba, and accelerator-specific dependencies.

See `docs/pyz1-contract.md` for the implementation contract and parity policy.
