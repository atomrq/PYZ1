# pyz1 Contract

This document is the implementation contract for the clean-room `pyz1`
reproduction. It freezes what can be translated from public source, what must be
reconstructed from papers and oracle fixtures, and what parity evidence is
required before claiming equivalence.

The current requirement-to-evidence index is maintained in
`docs/evidence-ledger.md`.

## Source Boundary

The public Z1+ package under
`/Users/jiaxm/Contents/CodexProjects/source_code/Z1+` includes the Perl wrapper,
public benchmarks, output-format declarations, shared modules, and the visible
PPA/PPA+ Fortran modules. It does not include the full default geometrical Z1+
implementation source.

The missing-source boundary is explicit:

- `Z1+install.pl` defines a public distribution and a private distribution.
- The private distribution includes `module-functions.f90` and `module-Z1.f90`.
- The visible package contains a prebuilt Linux x86-64 `Z1+.ex`.
- `pyz1` must not decompile or translate logic from the ELF.
- `Z1+.ex` may be used only as an oracle fixture generator on Linux.

## Runtime Scope

`pyz1` is developed locally in the micromamba environment named `pyz1`.
Commands on this macOS host must use `ulimit -n 1000000` in the same shell as
`micromamba run -n pyz1 ...` because the local libmamba/codesign path fails
under an unlimited file descriptor limit.

The first implementation uses Python and NumPy only. It must not add GPU,
CUDA, CuPy, PyTorch, Numba, or accelerator-specific dependencies.

## Z1 Input Contract

The Z1-formatted input boundary is parsed into typed snapshots before any
algorithm code receives it.

Supported in the current contract:

- Line 1: chain count.
- Line 2: three positive box lengths.
- Line 3: per-chain lengths, including monodisperse `C*N` syntax.
- Coordinate rows: three floats per bead/node.
- Optional metadata: sentinel `-1`, non-negative label, shear value.
- True chains are chains with more than two beads. Two-bead dumbbells are
  parsed, retained in native shortest-path output, and used as reducer
  blockers, but they are excluded from true-chain summary statistics.

Parsing must fail with typed errors for malformed headers, missing coordinate
rows, invalid floats, invalid chain lengths, and unexpected trailing metadata.

## Z1+ Output Contract

`Z1+summary.dat` contains one row per snapshot with exactly 15 columns:

1. timestep or snapshot index
2. true chain count
3. mean beads per original chain
4. RMS end-to-end distance as emitted by Z1+
5. mean primitive-path contour length `<Lpp>`
6. mean entanglements per chain
7. coil tube diameter `app`
8. coil tube step length `bpp`
9. RMS primitive-path contour length `sqrt(<Lpp^2>)`
10. classical kink estimator `NeCK`
11. modified kink estimator `NeMK`
12. classical coil estimator `NeCC`
13. modified coil estimator `NeMC`
14. mean original-chain bond length
15. original bead number density

The Z1+ README labels column 4 as "mean squared end-to-end distance", but the
observed Z1+ `benchmark-04` output and stdout value are the square root of the
mean squared end-to-end distance. `pyz1` stores this field as the value emitted
by Z1+ and uses `root_mean_squared_end_to_end` for input-derived comparisons.

`Z1+SP.dat` contains, per snapshot:

- true chain count
- three box lengths
- for each chain, a shortest-path node count
- for each shortest-path node, either `x y z s E` or `x y z s E chain node`

`s` is the corresponding original-chain bead coordinate. `E=1` marks an
entanglement node, and `E=0` marks a chain end or non-entanglement node. The
extra `chain node` pair appears in SP+ mode and identifies the other node
responsible for the entanglement.

Additional output files now have parser/writer coverage:

- `Z1+initconfig.dat`
- `Ree_values.dat`
- `Lpp_values.dat`
- `N_values.dat`
- `Z_values.dat`
- `PPA.dat`
- `PPA+.dat`
- `PPA-summary.dat`
- `PPA+summary.dat`

`PPA-summary.dat` and `PPA+summary.dat` use the same 15-column summary row
structure as `Z1+summary.dat`. `PPA.dat` and `PPA+.dat` use the coordinate
snapshot structure also used by `Z1+initconfig.dat`.

## Estimator Contract

Input-derived statistics that can be computed before primitive-path reduction:

- true chain count
- mean original-chain bead count
- RMS end-to-end distance
- mean original-chain bond length
- original bead number density

Primitive-path-dependent statistics require a primitive-path result:

- `<Lpp>`
- `sqrt(<Lpp^2>)`
- entanglement count `Z`
- `app`
- `bpp`
- `NeCK`
- `NeMK`
- `NeCC`
- `NeMC`

The `Ne` formulas must follow the Hoy-Foteinopoulou-Kroger estimator definitions
recorded in the paper-reading notes. Undefined or zero-kink cases must return a
documented sentinel or typed error, never a division-by-zero artifact.

`pyz1` uses the following summary-layer estimator formulas for a primitive-path
result with per-chain original bead counts `N_i`, end-to-end distances `Ree_i`,
primitive contours `Lpp_i`, and kink counts `Z_i`:

- `<N> = mean(N_i)`
- `<Z> = mean(Z_i)`
- `<Lpp> = mean(Lpp_i)`
- `LPP = sqrt(mean(Lpp_i^2))`
- `app = mean(Ree_i^2) / <Lpp>`
- `bpp = sum(Lpp_i) / sum(N_i - 1)`
- `NeCK = <N> * (<N> - 1) / (<Z> * (<N> - 1) + <N>)`
- `NeMK = <N> / <Z>`
- `NeCC = (<N> - 1) * mean(Ree_i^2) / <Lpp>^2`
- `NeMC = (<N> - 1) / (mean(Lpp_i^2) / mean(Ree_i^2) - 1)`

For undefined kink estimators (`<Z> <= 0`) and undefined modified coil
estimators (zero end-to-end mean square or nonpositive denominator), `pyz1`
returns the Z1+-style sentinel `-1.0` instead of raising or allowing a
division-by-zero artifact.

## PPA And PPA+ Contract

The visible `module-CPPA.f90` and `module-PPA.f90` are source-available and may
be ported directly to Python with tests against oracle fixtures. The port must
preserve:

- FENE and WCA constants
- phase schedule and timestep parameters
- Fortran integer step-count semantics for phase schedules
- PPA+ phase-stop checks based on global step and total system `Lpp`
- neighbor-list behavior
- periodic offsets
- endpoint behavior
- convergence diagnostics
- `PPA.dat`, `PPA+.dat`, `PPA-summary.dat`, and `PPA+summary.dat` output

PPA/PPA+ parity is numeric and must use documented tolerances. The tolerances
must be justified by measured deltas, not loosened to hide mismatches.
Known upstream-invalid native outputs must be documented as such instead of
masked by non-native force clipping or coordinate clipping. Benchmark-05 PPA+
is one such fixture: the input is finite and FENE-safe, but a near-zero
inter-chain WCA contact creates a first-step force large enough to overflow the
native fixed-width `Lpp` and coordinate output fields.

## Clean-Room Geometry Contract

The default Z1+ reducer is not source-available. Its Python implementation must
be clean-room from the papers, visible I/O contracts, and oracle behavior.

Required invariants:

- fixed chain endpoints
- no chain crossing
- no chain slipping through a kink or endpoint
- monotonic contour-length reduction for accepted local moves
- periodic unfolding/minimum-image behavior consistent with Z1+ fixtures
- deterministic kink cleanup for reported `Z1+SP.dat`
- SP+ pairing for entanglement nodes

Default geometrical Z1+ equivalence cannot be claimed until benchmark fixtures
show measured agreement for `Lpp`, `Z`, shortest-path structure, and SP+ pairing
under recorded tolerances.

## Oracle Fixture Policy

Oracle data must be generated on Linux with the Z1+ Perl wrapper, not by
directly launching the ELF.

The wrapper behavior is part of the oracle contract:

- installation and working directories must differ
- wrapper writes `Z1+parameters`
- wrapper launches `Z1+.ex`
- wrapper postprocesses `Z1+SP.dat` through `Z1+rearrange.pl`
- wrapper removes `Z1+parameters` after a normal run

Each oracle fixture run must record:

- input benchmark filename
- mode name and exact wrapper arguments
- input SHA256
- binary SHA256
- output SHA256 values
- hostname and kernel string
- command exit code
- stdout/stderr paths
- parsed summary row count

The current first oracle slice is `benchmark-04` in default and SP+ modes. Its
evidence is recorded in
`.omo/evidence/pyz1-benchmark-04-oracle-and-parity.md`.

## Benchmark Regression Status

The local benchmark regression report is:

```text
.omo/evidence/pyz1-benchmark-regression.md
```

The report is an evidence artifact, not a parity claim. It must classify each
checked benchmark/mode as `passed`, `mismatch`, or `known-invalid`, and it must
record measured deltas or an explicit skip reason. Current status is:

- `benchmark-04` default and SP+ are classified as `passed` under the current
  report contract: formatted summary fields match, SP+ pairings match, final
  node counts match, and final node geometry is within the documented
  shortest-path tolerance.
- `benchmark-01`, `benchmark-02`, `benchmark-03`, and `benchmark-05` default
  and SP+ are classified as `mismatch`. For benchmark-01/02/03, two-node
  obstacle chains are now retained in native SP output, participate as
  blockers, and contribute retained blocked-move obstacle kinks; the remaining
  gap is exact Z1+ obstacle-kink placement, source-bead selection, and SP+
  pairing. Task-62 evidence shows simple retained-trace and lower/upper hull
  rules do not fully explain the oracle obstacle sequence. Task-63 adds
  native/oracle obstacle pair-chain sequences to the regression report so this
  gap is tracked directly.
- SP+ structural comparison counts mismatched `other-chain other-node` pairs.
- `benchmark-06` and larger benchmark/mode entries are classified as
  `known-invalid` under the current `node_count>1000` performance guard until
  the reducer has a scalable neighbor-candidate implementation.

## Current Completion Boundary

For the current requirement-by-requirement completion verdict, see
`docs/completion-audit.md`.

Complete now:

- package scaffold and CLI entry
- Z1 input parser/writer
- core immutable data models
- Z1+ summary parser/writer
- Z1+ basic SP parser/writer
- Z1+ SP+ pairing parser/writer
- Z1+ initconfig, value-file, PPA, and PPA+ output parsers/writers
- input-derived statistics and summary/`Ne` estimators
- Linux oracle fixture tooling and parsed oracle corpora
- LAMMPS data/dump importer for bonded linear-chain use cases
- native PPA/PPA+ execution slices and PPA-specific summary semantics
- native clean-room geometry primitives
- native default reducer initial slice
- native SP+ pairing output for retained kink nodes
- native SP+ residual ghost-clearance rule reduces benchmark-04 final kink
  max-position delta to `0.0004385586199525317`; benchmark-04 default/SP+
  are now classified as `passed`; the remaining nonzero `Lpp` delta is retained
  as a diagnostic against the rounded three-decimal summary field rather than a
  pass/fail criterion
- native default/SP+ reducer retains two-node dumbbells in `Z1+SP.dat` and uses
  them as blockers while summary statistics still count only true chains;
  retained blocked-move trace nodes are now written as multiple obstacle kinks
  for dumbbell-obstacle snapshots; benchmark-01/02/03 node-count mismatches
  drop to 5/3/1 after this contract alignment, but the true-chain obstacle kink
  sequence still mismatches Z1+
- public Z1+ source reading is incomplete for the core default reducer:
  `Z1+install.pl` lists `module-Z1.f90` only in the private distribution, and
  the visible public tree supplies the Linux x86-64 ELF oracle `Z1+.ex` instead
- benchmark regression report generation and transparent mismatch/skip status
- benchmark regression rows include SP+ native/oracle first-chain obstacle pair
  sequences, giving the obstacle-placement work a stable diagnostic surface
- default/SP+ benchmark regression runs public benchmarks 01-05 under the
  default `node_count>1000` performance guard and records measured deltas for
  each runnable mismatch
- reducer blocker checks use a bounds index before exact geometry predicates,
  and large custom regression runs can skip expensive trace diagnostics while
  preserving reducer/summary/SP comparison
- package-level final integration smoke through `python -m pyz1` for default,
  SP+, PPA, and PPA+ modes
- explicit CLI failure for `-selfZ` / `-0` so the unsupported self-entanglement
  path cannot be confused with default reducer output
- PPA/PPA+ summary parity for all currently parseable oracle coordinate-path
  fixtures, with Fortran-overflow coordinates tracked as known-invalid
- native PPA/PPA+ WCA force path uses deterministic periodic cell-list candidate
  generation instead of scanning every cross-chain pair
- native PPA/PPA+ summary regression report surface that runs `run_ppa` and
  compares generated summaries against Z1+ PPA/PPA+ oracle summaries
- native PPA+ default accelerated settings mirror the visible Z1+
  integer-truncated phase step counts and phase-stop checks; benchmark-04 PPA+
  `Lpp delta` is reduced from `50.620053857564926` to
  `0.7762019820511341`, with `Ne` deltas remaining near `1e-12`

Not complete yet:

- full PPA/PPA+ benchmark-level runtime parity from native integration output;
  the WCA path now has a local candidate list and benchmark-04 PPA+ completes
  with default accelerated settings and Z1+ phase stops, but strict summary
  parity is still a `mismatch`. Benchmark-05 PPA+ is tracked separately as an
  upstream-invalid native overflow fixture, not a parser/writer mismatch.
- default geometrical Z1+ numerical parity for `Lpp`, `Z`, shortest-path
  structure, and SP+ pairings; benchmark-04 default/SP+ now pass the local
  report contract, benchmark-01/02/03 now preserve two-node obstacle chains in
  SP output and write retained blocked-move obstacle kinks but still miss exact
  Z1+ obstacle-kink placement/source beads/pairings. The public Z1+ source tree
  does not include `module-Z1.f90`, so further clean-room reducer work must be
  driven by papers, oracle output, and documented diagnostics rather than direct
  translation of the missing reducer source. Benchmark-05 still mismatches, and
  benchmark-06+ are still guarded for scalability.
- scalable all-14 benchmark reducer regression without the current
  `node_count>1000` performance guard.
- self-entanglement (`selfZ`) behavior in the native reducer beyond the current
  explicit not-implemented boundary.
- final user/developer documentation review for scientific parity caveats.
