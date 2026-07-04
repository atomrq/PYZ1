# pyz1

`pyz1` is a local Python implementation path for reproducing the public Z1+
workflow. The project starts with parsers, summaries, fixtures, and tests before
the clean-room geometrical reducer is implemented.

Local development uses the `pyz1` micromamba environment:

```bash
ulimit -n 1000000
micromamba run -n pyz1 python -m pytest
```

The original Linux `Z1+.ex` binary is an oracle for fixtures only; it is not a
runtime dependency of the Python package.
