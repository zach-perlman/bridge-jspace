# Which route the lookup follows: qwen35_122b_x6_routes_sweep_l36_g75

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.5-122b-a10b, layer 36. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.02 [0.00, 0.04] | 0.98 [0.96, 1.00] | 0.56 [0.47, 0.67] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.02 [0.00, 0.04] | 0.98 [0.96, 1.00] | 0.47 [0.37, 0.59] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.02 [0.00, 0.04] | 0.98 [0.96, 1.00] | 0.53 [0.44, 0.64] |
| C2 | whole | 300 | 0.38 [0.33, 0.43] | 0.58 [0.52, 0.63] | 0.00 [0.00, 0.00] | 0.04 [0.02, 0.06] | 0.00 [0.00, 0.00] | 0.47 [0.38, 0.57] |
| C2 | no_jpp | 300 | 0.37 [0.31, 0.42] | 0.58 [0.52, 0.63] | 0.00 [0.00, 0.00] | 0.06 [0.04, 0.08] | 0.00 [0.00, 0.00] | 0.36 [0.27, 0.46] |
| C2 | no_jpp_rand | 300 | 0.35 [0.31, 0.40] | 0.56 [0.50, 0.62] | 0.00 [0.00, 0.00] | 0.08 [0.06, 0.11] | 0.00 [0.00, 0.00] | 0.41 [0.31, 0.52] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 4.17, C2 4.28.
