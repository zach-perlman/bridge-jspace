# Which route the lookup follows: nem35l_x52_routes_x47_1

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model nemotron-3.5-lightning, layer 14. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C2 | whole | 300 | 0.43 [0.37, 0.49] | 0.56 [0.50, 0.62] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.78 [0.73, 0.82] |
| C2 | no_jpp | 300 | 0.37 [0.32, 0.42] | 0.57 [0.51, 0.63] | 0.00 [0.00, 0.00] | 0.06 [0.03, 0.10] | 0.00 [0.00, 0.00] | 0.58 [0.49, 0.66] |
| C2 | no_jpp_rand | 300 | 0.41 [0.35, 0.47] | 0.47 [0.41, 0.53] | 0.00 [0.00, 0.00] | 0.12 [0.09, 0.16] | 0.00 [0.00, 0.00] | 0.75 [0.68, 0.80] |
| C2 | no_alf | 300 | 0.31 [0.26, 0.35] | 0.10 [0.07, 0.14] | 0.00 [0.00, 0.00] | 0.59 [0.53, 0.65] | 0.00 [0.00, 0.00] | 0.64 [0.57, 0.70] |
| C2 | no_alf_rand | 300 | 0.41 [0.35, 0.48] | 0.57 [0.50, 0.64] | 0.00 [0.00, 0.00] | 0.02 [0.01, 0.03] | 0.00 [0.00, 0.00] | 0.75 [0.68, 0.80] |
| C2 | no_jpp100 | 300 | 0.24 [0.20, 0.29] | 0.43 [0.38, 0.49] | 0.00 [0.00, 0.00] | 0.33 [0.27, 0.38] | 0.00 [0.00, 0.00] | 0.31 [0.23, 0.39] |
| C2 | no_jpp100_rand | 300 | 0.16 [0.11, 0.21] | 0.15 [0.11, 0.20] | 0.00 [0.00, 0.00] | 0.69 [0.64, 0.74] | 0.00 [0.00, 0.00] | 0.36 [0.27, 0.44] |
| C2 | no_jpp26_100 | 300 | 0.37 [0.31, 0.43] | 0.54 [0.48, 0.60] | 0.00 [0.00, 0.00] | 0.09 [0.06, 0.13] | 0.00 [0.00, 0.00] | 0.71 [0.63, 0.77] |
| C2 | no_jpp26_100_rand | 300 | 0.42 [0.35, 0.48] | 0.51 [0.44, 0.58] | 0.00 [0.00, 0.00] | 0.07 [0.04, 0.11] | 0.00 [0.00, 0.00] | 0.75 [0.69, 0.81] |
| C2 | no_ratoms75 | 300 | 0.42 [0.36, 0.47] | 0.57 [0.52, 0.63] | 0.00 [0.00, 0.00] | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.75 [0.68, 0.81] |
| C2 | no_ratoms75_rand | 300 | 0.42 [0.35, 0.48] | 0.51 [0.44, 0.58] | 0.00 [0.00, 0.00] | 0.07 [0.04, 0.11] | 0.00 [0.00, 0.00] | 0.75 [0.69, 0.81] |
| C2 | no_ratoms75own | 300 | 0.44 [0.38, 0.51] | 0.55 [0.49, 0.62] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.77 [0.72, 0.82] |
| C2 | no_ratoms75own_rand | 300 | 0.43 [0.38, 0.49] | 0.56 [0.51, 0.62] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.77 [0.72, 0.82] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C2 15.18.

## 45k: why does the lookup lose with more J++ atoms? (jobs/c3/batch45.yaml, fixed in advance)

Lookup route shares per arm (no_jpp: J++ at k = 25; each part against a random part of its own share; C0 has no position or identity answer: its switch counts as other):

| condition | arm | n | identity | position | value | original | other |
|---|---|---|---|---|---|---|---|
| C2 | whole | 300 | 0.43 [0.37, 0.49] | 0.56 [0.50, 0.62] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] |
| C2 | no_jpp | 300 | 0.37 [0.32, 0.42] | 0.57 [0.51, 0.63] | 0.00 [0.00, 0.00] | 0.06 [0.03, 0.10] | 0.00 [0.00, 0.00] |
| C2 | no_jpp_rand | 300 | 0.41 [0.35, 0.47] | 0.47 [0.41, 0.53] | 0.00 [0.00, 0.00] | 0.12 [0.09, 0.16] | 0.00 [0.00, 0.00] |
| C2 | no_jpp100 | 300 | 0.24 [0.20, 0.29] | 0.43 [0.38, 0.49] | 0.00 [0.00, 0.00] | 0.33 [0.27, 0.38] | 0.00 [0.00, 0.00] |
| C2 | no_jpp100_rand | 300 | 0.16 [0.11, 0.21] | 0.15 [0.11, 0.20] | 0.00 [0.00, 0.00] | 0.69 [0.64, 0.74] | 0.00 [0.00, 0.00] |

C2, from k = 25 to k = 100, the fall beyond the random part's ([share(no_jpp) - share(no_jpp100)] - [share(no_jpp_rand) - share(no_jpp100_rand)], paired): identity -0.12 [-0.17, -0.07], position -0.18 [-0.25, -0.12].

Mean cos^2 between the span of the k picked atoms and the pointer directions U (||P U||_F^2 / rank U) and the identity direction mu_alt - mu_org (items with both class means):

| condition | k | U: mean | U: median | n | identity: mean | identity: median | n of items |
|---|---|---|---|---|---|---|---|
| C2 | 25 | 0.016 | 0.016 | 300 | 0.286 | 0.286 | 300 of 300 |
| C2 | 100 | 0.060 | 0.060 | 300 | 0.456 | 0.461 | 300 of 300 |

Precondition (Dan ~22:05, on the 27B): C0 lookup extra loss at k = 100 = nan (>= 0.2: no).

Clauses on this model: identity falls >= 0.2 beyond random and position < 0.1 no; neither falls by 0.1 (the 9B's clause) yes; position falls >= 0.2 beyond random and the k = 100 span's mean cos^2 with U over C2 (0.060) >= 0.5: no. The labels and Q45.9 need the 9B and the main-test runs: jppk-summary.
