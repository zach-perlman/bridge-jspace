# Which route the lookup follows: qwen35_9b_x6_routes_sweep_l10

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.5-9b, layer 10. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.97 [0.95, 0.99] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.09 [0.05, 0.12] | 0.91 [0.88, 0.95] | 0.78 [0.71, 0.85] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 1.00 [0.99, 1.00] | 0.96 [0.92, 0.99] |
| C2 | whole | 300 | 0.98 [0.96, 0.99] | 0.02 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.95 [0.91, 0.98] |
| C2 | no_jpp | 300 | 0.49 [0.45, 0.54] | 0.06 [0.04, 0.09] | 0.00 [0.00, 0.00] | 0.44 [0.39, 0.49] | 0.00 [0.00, 0.00] | 0.48 [0.41, 0.56] |
| C2 | no_jpp_rand | 300 | 0.85 [0.80, 0.89] | 0.02 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.13 [0.10, 0.17] | 0.00 [0.00, 0.01] | 0.88 [0.83, 0.93] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 13.36, C2 13.47.
