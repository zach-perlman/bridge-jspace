# Which route the lookup follows: qwen35_9b_x6_routes_sweep_l8

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.5-9b, layer 8. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.99 [0.98, 1.00] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.28 [0.23, 0.34] | 0.72 [0.66, 0.77] | 0.66 [0.58, 0.75] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.98 [0.97, 1.00] |
| C2 | whole | 300 | 0.97 [0.95, 0.99] | 0.03 [0.01, 0.05] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.95 [0.92, 0.98] |
| C2 | no_jpp | 300 | 0.31 [0.27, 0.36] | 0.06 [0.02, 0.10] | 0.00 [0.00, 0.00] | 0.63 [0.57, 0.69] | 0.00 [0.00, 0.00] | 0.36 [0.29, 0.44] |
| C2 | no_jpp_rand | 300 | 0.85 [0.81, 0.89] | 0.02 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.12 [0.08, 0.16] | 0.00 [0.00, 0.01] | 0.88 [0.83, 0.93] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 11.89, C2 11.86.
