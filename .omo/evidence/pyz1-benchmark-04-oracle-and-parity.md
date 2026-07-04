# pyz1 benchmark-04 oracle and parity evidence

Date: 2026-07-03

## Scope

This evidence covers the first concrete Z1+ parity slice:

- Input: `/Users/jiaxm/Contents/CodexProjects/source_code/Z1+/.benchmark-04.Z1`
- Z1+ modes: default basic `Z1+SP.dat` and `+` / `SP+`
- pyz1 checks:
  - Parse Z1+ `Z1+summary.dat`
  - Parse basic and SP+ `Z1+SP.dat`
  - Compute input-derived summary fields from `.benchmark-04.Z1`
  - Compare those fields against Z1+ oracle values
  - Check basic SP and SP+ structure/pairing against oracle

## Remote oracle generation

Resource docs were read before remote use:

- `/Users/jiaxm/.codex/RESOURCES.md`
- `/Users/jiaxm/.codex/resources/cluster-access.md`

Direct `192.168.62.200:2341` SSH refused, so the documented FRP route was used:

```text
ssh -p 6301 jxm@47.104.203.55
```

Remote environment:

```text
hostname: admin
uname: Linux admin 3.10.0-1160.el7.x86_64 #1 SMP Mon Oct 19 16:18:59 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

Remote work root:

```text
/public/home/jxm/codex_tmp/pyz1_oracle_20260703_152300
```

The Z1+ Perl wrapper requires an installation directory distinct from the
working directory, and it generates `Z1+parameters` before launching `Z1+.ex`.
Directly launching `Z1+.ex` failed with Fortran EOF on empty `Z1+parameters`;
that failure was not used as oracle data.

Successful runs:

```text
default command: ../install/Z1+ .benchmark-04.Z1
default exit code: 0
default Z1+ cpu seconds: 6.5609999E-03
default outputs: Z1+summary.dat 88 bytes, Z1+SP.dat 833 bytes

SP+ command: ../install/Z1+ + .benchmark-04.Z1
SP+ exit code: 0
SP+ Z1+ cpu seconds: 9.6039996E-03
SP+ outputs: Z1+summary.dat 88 bytes, Z1+SP.dat 849 bytes
```

## Local fixture hashes

```text
c4a2bfe6f11a47b4345005e91700c8b2778ae70c97544cc4a99c9d674c522e06  source_code/Z1+/.benchmark-04.Z1
e6f0d3f29ca91f7e147cd94f8507b6108535c70e10d3380deff4dda6c8659020  source_code/Z1+/Z1+.ex
1c985706a0701cdc9357986fa4a91adeeebaa4c3c8a34a716686aa63e4bb3f4b  tests/fixtures/z1plus_oracle/benchmark-04/basic/Z1+summary.dat
e9c78c19fc6e5bf6934ce40426e8aab35611d6c7d39b9f18eb7f576aec570893  tests/fixtures/z1plus_oracle/benchmark-04/basic/Z1+SP.dat
1c985706a0701cdc9357986fa4a91adeeebaa4c3c8a34a716686aa63e4bb3f4b  tests/fixtures/z1plus_oracle/benchmark-04/spplus/Z1+summary.dat
ab72eb77a9f77e8dd35e473813045d2b7a3dffc91d9ecd016ba2b6264de5ad82  tests/fixtures/z1plus_oracle/benchmark-04/spplus/Z1+SP.dat
```

## Passing local evidence

```text
(ulimit -n 1000000; micromamba run -n pyz1 python -m pytest -q)
18 passed in 0.07s

(ulimit -n 1000000; micromamba run -n pyz1 python -m ruff check src tests)
All checks passed!

(ulimit -n 1000000; micromamba run -n pyz1 basedpyright)
0 errors, 0 warnings, 0 notes
```

Captured artifacts:

- `.omo/evidence/task-5-pyz1-cleanroom-reproduction.txt`
- `.omo/evidence/task-5-quality-pyz1-cleanroom-reproduction.txt`
- `.omo/evidence/task-parity-pyz1-cleanroom-reproduction.txt`
- `.omo/evidence/task-16-pyz1-cleanroom-reproduction.txt`

## Parity status

Passed:

- `.benchmark-04.Z1` input parsing
- Z1+ summary parsing for the default and SP+ runs
- Basic `Z1+SP.dat` parsing
- SP+ `Z1+SP.dat` parsing with pairing columns
- Input-derived fields vs oracle summary:
  - true chain count
  - mean original beads
  - RMS end-to-end distance as emitted by Z1+
  - mean original bond length
  - original bead density
- Basic/SP+ structural oracle checks:
  - 5 shortest-path chains
  - chain node counts `(3, 2, 2, 2, 2)`
  - one entanglement node
  - SP+ pair `(chain=2, node=1)`

Not claimed yet:

- Full clean-room geometrical Z1+ path reduction equivalence
- All 14 benchmark fixtures
- PPA/PPA+ numerical parity
- Writers for every Z1+ output file
