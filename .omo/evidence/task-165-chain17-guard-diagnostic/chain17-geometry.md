# Task 165 chain17 guard-enabled geometry diagnostic

Date: 2026-07-07

## Classification

`diagnostic_only` / `oracle_residual_inference_generalizable`.

This artifact compares benchmark-05 SP+ chain17 after enabling the default-off contact-relaxation guard. It uses oracle output only as a measurement target and does not feed oracle final coordinates into the reducer.

## Chain-Level Contours

| path | node count | contour | delta vs oracle |
| --- | ---: | ---: | ---: |
| default | 4 | 15.4444 | 0.999611 |
| guard-enabled | 4 | 15.4444 | 0.999611 |
| oracle | 4 | 14.4447 | 0 |

Original unfolded chain17 contour: 19

## Guard-Enabled Node Comparison

| node | source | pair | guard position | oracle position | position delta | guard distance from source interpolation | oracle distance from source interpolation | guard pair distance | guard pair fraction | oracle pair distance | oracle pair fraction |
| ---: | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1 | n/a | (-2.8561,2.3914,3.442) | (-2.8561,2.3914,3.442) | 0 | 0 | 0 | n/a | n/a | n/a | n/a |
| 2 | 5 | 9:1 | (-3.44693,-0.0226148,0.514403) | (-3.65909,0.833158,0.937243) | 0.97783 | 1.14883 | 1.46592 | 0.955738 | 0.459233 | 0.00127467 | 0.324806 |
| 3 | 11.67 | 44:2 | (-5.09112,0.0502048,-2.78002) | (-5.55873,-1.63226,-2.53901) | 1.76279 | 1.18011 | 1.63474 | 1.41599 | 0 | 0.0260073 | 0.0102489 |
| 4 | 20 | n/a | (-8.7654,-5.6585,-6.8617) | (-8.7654,-5.6585,-6.8617) | 0 | 0 | 0 | n/a | n/a | n/a | n/a |

## Segment-Length Contribution

| segment | source span | guard length | oracle length | abs delta |
| ---: | --- | ---: | ---: | ---: |
| 1 | 1->5 | 3.84023 | 3.05724 | 0.782991 |
| 2 | 5->11.67 | 3.68264 | 4.66597 | 0.983322 |
| 3 | 11.67->20 | 7.92148 | 6.72153 | 1.19994 |

## Immediate Interpretation

- chain17 already has the oracle pair/source sequence from earlier task129 work.
- No chain17 oracle final-position shim exists in `src/pyz1/reducer.py`; current chain17 logic selects input-derived contact candidates and pair overrides.
- The dominant guard-enabled contour residual is geometric, not pair/source topology: node count and pair/source sequence match, while interior positions differ from the oracle contour.
- A production reducer change should therefore target a general endpoint-fixed multi-node relaxation rule for paired retained nodes, not benchmark-specific chain17 coordinates.
