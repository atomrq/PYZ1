# Reducer Oracle Geometry Audit

Date: 2026-07-07

This audit records a project-level correction for the source-informed
clean-room Z1+ reducer work. SP/SP+ parity remains the target, but production
reducer logic must not depend on oracle final coordinates copied from known
benchmarks.

## Classification Rules

- `source_contract`: behavior backed by visible Z1+/Z1plus-code source,
  wrapper scripts, public Fortran modules, README text, or reference logs.
- `oracle_residual_inference_generalizable`: behavior discovered from oracle
  residuals but implementable from input-system data such as chain geometry,
  source ordering, contact candidates, pair topology, and obstacle constraints.
- `temporary oracle-regression shim`: benchmark-specific oracle final geometry
  or constants that reproduce an oracle fixture but cannot run on a new system
  without oracle coordinates.
- `diagnostic_only`: reporting, RED tests, and analysis artifacts that expose a
  residual without changing reducer output.

## Initial Findings

### Source-Backed Or Public-Source-Bounded Areas

- Parser/writer and SP/SP+ I/O surfaces are source-backed through the visible
  Z1+/Z1plus-code scripts:
  `Z1+SP-to-data.pl`, `Z1+dat2dump.pl`, `Z1+dump.pl`, `Z1+export.pl`,
  `Z1+import-lammps.pl`, `extract-single-chain-entanglements.pl`, and
  `replacements/Z1+template.pl`.
- PPA/CPPA work can consult the visible install-package Fortran modules such
  as `module-PPA.f90`, `module-CPPA.f90`, `module-shared.f90`, and
  `module-output-formats.f90`.
- The public source still does not expose the hidden Z1 reducer core
  (`module-Z1.f90` / `module-functions.f90`), so Z1 reducer geometry rules
  remain clean-room.

### Oracle Residual Inference That May Generalize

- Pair topology, source bead ordering, paired node ordering, and reciprocal
  coverage inferred from SP/SP+ oracle outputs can guide clean-room rules if
  the implementation selects contacts from the input geometry and candidate
  surfaces.
- Existing contact-candidate machinery using closest segment points, pair
  overrides, source bead order, and blocker/contact distances is a plausible
  base for a general constrained relaxation step.
- Chain contour residuals should be treated as evidence of missing relaxation
  or endpoint-fixed constrained shortening behavior, not as instructions to
  copy final coordinates.

### Temporary Oracle-Regression Shims Requiring Replacement

The current reducer contains benchmark-specific final-position constants used
by contour alignment helpers. These should be treated as temporary
oracle-regression shims until replaced by generalized rules:

- chain9/27 contour positions:
  `TRUE_CHAIN_SECONDARY_CHAIN9_PAIR27_POSITION`,
  `TRUE_CHAIN_SECONDARY_CHAIN27_PAIR9_POSITION`,
  `TRUE_CHAIN_SECONDARY_CHAIN27_PAIR19_POSITION`
- chain22/25 contour positions:
  `TRUE_CHAIN_SECONDARY_CHAIN22_PAIR25_POSITION`,
  `TRUE_CHAIN_SECONDARY_CHAIN25_PAIR3_POSITION`,
  `TRUE_CHAIN_SECONDARY_CHAIN25_PAIR40_POSITION`
- chain34/36/39/43/48 contour positions:
  `TRUE_CHAIN_SECONDARY_CHAIN34_*_POSITION`,
  `TRUE_CHAIN_SECONDARY_CHAIN36_*_POSITION`,
  `TRUE_CHAIN_SECONDARY_CHAIN39_*_POSITION`,
  `TRUE_CHAIN_SECONDARY_CHAIN43_PAIR39_POSITION`,
  `TRUE_CHAIN_SECONDARY_CHAIN48_*_POSITION`

The corresponding helper functions include:
`_align_secondary_chain9_contacts`, `_align_secondary_chain22_contacts`,
`_align_secondary_chain25_contacts`, `_align_secondary_chain27_contacts`,
`_align_secondary_chain34_contacts`, `_align_secondary_chain36_contacts`,
`_align_secondary_chain39_contact_positions`,
`_align_secondary_chain43_contacts`, and `_align_secondary_chain48_contacts`.

These shims may remain temporarily to preserve current regression surfaces, but
new work must not expand this pattern as the normal route to parity.

## Task161 Redirect

Task161 keeps the benchmark-05 chain37 contour RED assertion and diagnostics as
`diagnostic_only` / `oracle_residual_inference` evidence. The attempted idea of
closing chain37 by copying three oracle final positions is rejected as a formal
solution because it would not generalize to new systems.

The next GREEN target should be a general rule, for example:

1. Build retained contact nodes from source bead order and pair topology.
2. Keep endpoints fixed.
3. Preserve paired-node ordering and contact/obstacle constraints.
4. Relax retained interior nodes by minimizing local contour length subject to
   contact distance and blocker-clearance constraints.
5. Accept a move only when it improves contour without changing pair topology,
   node count, source bead ordering, or benchmark-04 SP+ pass status.

Oracle fixtures should then measure the residual movement, but oracle final
coordinates must not be production inputs.

## Immediate Replacement Plan

1. Add diagnostics that compare current retained positions with:
   source-bead interpolation on the input chain, paired-segment projections,
   contact distances, and local contour contribution.
2. Prototype a small pure geometry relaxation helper against synthetic unit
   tests before wiring it into benchmark-05.
   - Task162 adds `src/pyz1/contact_relaxation.py` with
     `ContactConstrainedNodeRelaxation` and
     `relax_contact_constrained_node`.
3. Apply the helper first behind a narrow guard that uses input topology and
   candidate contacts, not oracle coordinates.
4. Re-run benchmark-04/05 SP+ regression and record whether existing
   oracle-position shims can be removed or narrowed.
5. Gradually replace the listed temporary shims with the generalized
   constrained-relaxation path.
