# Which route the lookup follows: x6_routes_sweep_l28_27b

Fixed in advance (Dan, 25 Oct ~01:50; spec jobs/c3/x6_routes.yaml; predictions: batch 32). Model qwen3.6-27b, layer 28. Cluster bootstrap over the bridge item (10000 resamples). UNVERIFIED.

| condition | arm | n | identity | position | value | original | other | recall follows S |
|---|---|---|---|---|---|---|---|---|
| C0 | whole | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] |
| C0 | no_jpp | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.98 [0.97, 0.99] |
| C0 | no_jpp_rand | 300 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.99 [0.98, 1.00] |
| C2 | whole | 300 | 0.64 [0.59, 0.70] | 0.34 [0.29, 0.40] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.01] | 0.01 [0.00, 0.02] | 0.83 [0.79, 0.87] |
| C2 | no_jpp | 300 | 0.48 [0.43, 0.53] | 0.45 [0.40, 0.51] | 0.00 [0.00, 0.01] | 0.06 [0.04, 0.09] | 0.00 [0.00, 0.01] | 0.64 [0.60, 0.68] |
| C2 | no_jpp_rand | 300 | 0.63 [0.57, 0.68] | 0.32 [0.27, 0.38] | 0.00 [0.00, 0.00] | 0.05 [0.03, 0.07] | 0.00 [0.00, 0.00] | 0.79 [0.74, 0.83] |

Rule (fixed in advance): a route is used iff its share >= 0.2 with lower CI >= 0.1. C1: identity = original (both a). Median norm of the change per condition: C0 37.09, C2 37.44.
