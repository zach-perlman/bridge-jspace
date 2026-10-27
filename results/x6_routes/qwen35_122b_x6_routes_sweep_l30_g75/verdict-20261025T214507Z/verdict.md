# Which route the lookup follows: qwen35_122b_x6_routes_sweep_l30_g75

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.5-122b-a10b, layer 30. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.93 [0.89, 0.97] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.17 [0.11, 0.22] | 0.83 [0.78, 0.89] | 0.63 [0.53, 0.75] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.87 [0.81, 0.94] |
| C2 | whole | 300 | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.91 [0.87, 0.95] |
| C2 | no_jpp | 300 | 0.59 [0.53, 0.65] | 0.02 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.39 [0.33, 0.45] | 0.00 [0.00, 0.00] | 0.46 [0.37, 0.57] |
| C2 | no_jpp_rand | 300 | 0.94 [0.91, 0.98] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.06 [0.02, 0.09] | 0.00 [0.00, 0.00] | 0.79 [0.71, 0.87] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 2.76, C2 2.74.
