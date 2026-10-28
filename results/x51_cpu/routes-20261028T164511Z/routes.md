# Route split of the lookup's J++ dependence (batch 51, CPU item 2)

Descriptive, after the data. Routes scenes, condition C2 (Iris picked B; B's and C's locker sentences swapped, B -> a new digit), the lookup (PP), X0's chat read. An item's route = its lookup answer under the whole change (x6_routes.classify: identity = B's new locker digit, position = C's digit at B's old slot). On the items of each route: extra loss = share still taking that route without a random part of the part's share minus share still taking it without the part (X0's excess with S_whole = 1 on these items). Cluster bootstrap over bridge items (10,000 resamples, seed 0, 95% intervals; the two routes' subsets on the same draws, so identity - position is paired). Sources: the routes run of record (J++ k = 25 at L), the 47.1 run (C2; J++ at k = 25 and 100, atoms 26-100 with 1-25 kept), the 47.8 / 49.4 anatomy (its test half, the layer's own 25 atoms, every sampled layer). UNVERIFIED.

## At the fixed layer

| model | source | layer | part | C2 items | identity-route n | identity extra loss | position-route n | position extra loss | identity - position | routes under the whole change |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | qwen35_9b_x6_routes (gate True) | 12 | J++ k = 25 | 300 | 144 | 0.12 [0.07, 0.19] | 153 | -0.08 [-0.13, -0.04] | 0.21 [0.14, 0.28] | {'identity': 144, 'position': 153, 'original': 3} |
| qwen3.5-9b | qwen35_9b_x6_routes_x47_1 (gate True) | 12 | J++ k = 25 | 300 | 144 | 0.12 [0.07, 0.19] | 153 | -0.08 [-0.13, -0.04] | 0.21 [0.14, 0.28] | {'identity': 144, 'position': 153, 'original': 3} |
| qwen3.5-9b | qwen35_9b_x6_routes_x47_1 (gate True) | 12 | J++ k = 100 | 300 | 144 | 0.17 [0.09, 0.25] | 153 | -0.33 [-0.43, -0.23] | 0.50 [0.39, 0.62] | {'identity': 144, 'position': 153, 'original': 3} |
| qwen3.5-9b | qwen35_9b_x6_routes_x47_1 (gate True) | 12 | atoms 26-100 | 300 | 144 | 0.11 [0.06, 0.16] | 153 | 0.02 [-0.03, 0.08] | 0.09 [0.02, 0.16] | {'identity': 144, 'position': 153, 'original': 3} |
| qwen3.5-9b | qwen35_9b_x47_anatomy (gate True) | 12 | J++ k = 25 (layer's own) | 200 | 98 | -0.03 [-0.07, 0.01] | 102 | -0.01 [-0.06, 0.03] | -0.02 [-0.08, 0.06] | {'identity': 98, 'position': 102} |
| qwen3.6-27b | x6_routes_27b (gate True) | 32 | J++ k = 25 | 300 | 197 | 0.30 [0.25, 0.34] | 101 | -0.06 [-0.14, 0.01] | 0.36 [0.26, 0.46] | {'identity': 197, 'position': 101, 'original': 1, 'other': 1} |
| qwen3.6-27b | x6_routes_x47_1_27b (gate True) | 32 | J++ k = 25 | 300 | 197 | 0.30 [0.25, 0.34] | 101 | -0.06 [-0.14, 0.01] | 0.36 [0.26, 0.46] | {'identity': 197, 'position': 101, 'original': 1, 'other': 1} |
| qwen3.6-27b | x6_routes_x47_1_27b (gate True) | 32 | J++ k = 100 | 300 | 197 | 0.70 [0.64, 0.76] | 101 | -0.01 [-0.14, 0.10] | 0.71 [0.60, 0.84] | {'identity': 197, 'position': 101, 'original': 1, 'other': 1} |
| qwen3.6-27b | x6_routes_x47_1_27b (gate True) | 32 | atoms 26-100 | 300 | 197 | 0.04 [0.02, 0.07] | 101 | -0.02 [-0.07, 0.03] | 0.06 [0.01, 0.12] | {'identity': 197, 'position': 101, 'original': 1, 'other': 1} |
| qwen3.6-27b | x49_4_anatomy_27b (gate True) | 32 | J++ k = 25 (layer's own) | 150 | 100 | 0.12 [0.06, 0.19] | 49 | -0.04 [-0.09, 0.00] | 0.16 [0.10, 0.23] | {'identity': 100, 'position': 49, 'other': 1} |
| muse-glimmer-30b | muse30b_x6_routes (gate True) | 26 | J++ k = 25 | 300 | 131 | 0.00 [-0.03, 0.04] | 163 | -0.03 [-0.08, 0.01] | 0.03 [-0.02, 0.09] | {'position': 163, 'identity': 131, 'original': 6} |
| muse-glimmer-30b | muse30_x6_routes_x47_1 (gate True) | 26 | J++ k = 25 | 300 | 131 | 0.00 [-0.03, 0.04] | 163 | -0.03 [-0.08, 0.01] | 0.03 [-0.02, 0.09] | {'position': 163, 'identity': 131, 'original': 6} |
| muse-glimmer-30b | muse30_x6_routes_x47_1 (gate True) | 26 | J++ k = 100 | 300 | 131 | 0.04 [0.01, 0.07] | 163 | -0.08 [-0.12, -0.04] | 0.12 [0.07, 0.16] | {'position': 163, 'identity': 131, 'original': 6} |
| muse-glimmer-30b | muse30_x6_routes_x47_1 (gate True) | 26 | atoms 26-100 | 300 | 131 | 0.06 [0.02, 0.11] | 163 | 0.03 [0.00, 0.07] | 0.03 [-0.02, 0.08] | {'position': 163, 'identity': 131, 'original': 6} |
| muse-glimmer-30b | muse30_x47_anatomy (gate True) | 26 | J++ k = 25 (layer's own) | 200 | 83 | 0.02 [-0.02, 0.09] | 113 | -0.01 [-0.03, 0.00] | 0.03 [-0.01, 0.11] | {'position': 113, 'identity': 83, 'original': 4} |

## The anatomy by layer (one-layer removal, the layer's own 25 atoms)

| model | source | layer | part | C2 items | identity-route n | identity extra loss | position-route n | position extra loss | identity - position | routes under the whole change |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | qwen35_9b_x47_anatomy | 2 | J++ k = 25 | 200 | 200 | 0.07 [0.05, 0.11] | 0 | - | - | {'identity': 200} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 4 | J++ k = 25 | 200 | 200 | 0.02 [0.00, 0.03] | 0 | - | - | {'identity': 200} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 6 | J++ k = 25 | 200 | 200 | 0.04 [0.01, 0.07] | 0 | - | - | {'identity': 200} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 8 | J++ k = 25 | 200 | 196 | 0.06 [0.02, 0.10] | 4 | -0.25 [-0.50, 0.00] | 0.31 [0.04, 0.56] | {'identity': 196, 'position': 4} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 10 | J++ k = 25 | 200 | 196 | 0.18 [0.14, 0.22] | 4 | 0.00 [0.00, 0.00] | 0.18 [0.14, 0.22] | {'identity': 196, 'position': 4} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 12 | J++ k = 25 | 200 | 98 | -0.03 [-0.07, 0.01] | 102 | -0.01 [-0.06, 0.03] | -0.02 [-0.08, 0.06] | {'identity': 98, 'position': 102} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 14 | J++ k = 25 | 200 | 83 | -0.06 [-0.10, -0.02] | 111 | -0.01 [-0.04, 0.02] | -0.05 [-0.11, 0.00] | {'identity': 83, 'position': 111, 'original': 6} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 16 | J++ k = 25 | 200 | 27 | -0.07 [-0.17, 0.00] | 65 | -0.05 [-0.08, 0.00] | -0.03 [-0.14, 0.07] | {'original': 108, 'position': 65, 'identity': 27} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 18 | J++ k = 25 | 200 | 4 | 0.00 [0.00, 0.00] | 8 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | {'original': 188, 'position': 8, 'identity': 4} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 20 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 22 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 24 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 26 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 28 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| qwen3.5-9b | qwen35_9b_x47_anatomy | 30 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| qwen3.6-27b | x49_4_anatomy_27b | 8 | J++ k = 25 | 150 | 150 | 0.21 [0.13, 0.29] | 0 | - | - | {'identity': 150} |
| qwen3.6-27b | x49_4_anatomy_27b | 16 | J++ k = 25 | 150 | 150 | 0.01 [0.00, 0.02] | 0 | - | - | {'identity': 150} |
| qwen3.6-27b | x49_4_anatomy_27b | 24 | J++ k = 25 | 150 | 150 | 0.04 [0.01, 0.08] | 0 | - | - | {'identity': 150} |
| qwen3.6-27b | x49_4_anatomy_27b | 30 | J++ k = 25 | 150 | 93 | 0.10 [0.01, 0.19] | 57 | -0.02 [-0.06, 0.00] | 0.11 [0.03, 0.19] | {'identity': 93, 'position': 57} |
| qwen3.6-27b | x49_4_anatomy_27b | 32 | J++ k = 25 | 150 | 100 | 0.12 [0.06, 0.19] | 49 | -0.04 [-0.09, 0.00] | 0.16 [0.10, 0.23] | {'identity': 100, 'position': 49, 'other': 1} |
| qwen3.6-27b | x49_4_anatomy_27b | 34 | J++ k = 25 | 150 | 105 | 0.13 [0.05, 0.24] | 43 | -0.07 [-0.15, -0.02] | 0.20 [0.10, 0.34] | {'identity': 105, 'position': 43, 'other': 1, 'original': 1} |
| qwen3.6-27b | x49_4_anatomy_27b | 40 | J++ k = 25 | 150 | 29 | 0.03 [0.00, 0.16] | 19 | 0.05 [0.00, 0.18] | -0.02 [-0.15, 0.12] | {'identity': 29, 'original': 102, 'position': 19} |
| qwen3.6-27b | x49_4_anatomy_27b | 48 | J++ k = 25 | 150 | 0 | - | 0 | - | - | {'original': 150} |
| qwen3.6-27b | x49_4_anatomy_27b | 56 | J++ k = 25 | 150 | 0 | - | 0 | - | - | {'original': 150} |
| muse-glimmer-30b | muse30_x47_anatomy | 2 | J++ k = 25 | 200 | 198 | 0.05 [0.02, 0.07] | 2 | 0.50 [0.00, 1.00] | -0.45 [-0.97, 0.07] | {'identity': 198, 'position': 2} |
| muse-glimmer-30b | muse30_x47_anatomy | 6 | J++ k = 25 | 200 | 199 | 0.05 [0.01, 0.09] | 1 | 0.00 [0.00, 0.00] | 0.05 [0.02, 0.10] | {'identity': 199, 'position': 1} |
| muse-glimmer-30b | muse30_x47_anatomy | 10 | J++ k = 25 | 200 | 197 | 0.12 [0.07, 0.17] | 3 | 0.33 [0.00, 1.00] | -0.22 [-0.91, 0.15] | {'identity': 197, 'position': 3} |
| muse-glimmer-30b | muse30_x47_anatomy | 14 | J++ k = 25 | 200 | 192 | 0.05 [0.01, 0.09] | 8 | 0.00 [0.00, 0.00] | 0.05 [0.01, 0.09] | {'identity': 192, 'position': 8} |
| muse-glimmer-30b | muse30_x47_anatomy | 18 | J++ k = 25 | 200 | 164 | 0.04 [-0.01, 0.09] | 36 | 0.00 [-0.06, 0.11] | 0.04 [-0.06, 0.10] | {'identity': 164, 'position': 36} |
| muse-glimmer-30b | muse30_x47_anatomy | 22 | J++ k = 25 | 200 | 127 | 0.01 [-0.04, 0.05] | 72 | -0.03 [-0.07, 0.00] | 0.04 [-0.04, 0.10] | {'position': 72, 'identity': 127, 'original': 1} |
| muse-glimmer-30b | muse30_x47_anatomy | 26 | J++ k = 25 | 200 | 83 | 0.02 [-0.02, 0.09] | 113 | -0.01 [-0.03, 0.00] | 0.03 [-0.01, 0.11] | {'position': 113, 'identity': 83, 'original': 4} |
| muse-glimmer-30b | muse30_x47_anatomy | 30 | J++ k = 25 | 200 | 23 | -0.04 [-0.10, 0.00] | 34 | 0.03 [0.00, 0.07] | -0.07 [-0.17, 0.00] | {'original': 143, 'position': 34, 'identity': 23} |
| muse-glimmer-30b | muse30_x47_anatomy | 34 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| muse-glimmer-30b | muse30_x47_anatomy | 38 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| muse-glimmer-30b | muse30_x47_anatomy | 42 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| muse-glimmer-30b | muse30_x47_anatomy | 46 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |
| muse-glimmer-30b | muse30_x47_anatomy | 50 | J++ k = 25 | 200 | 0 | - | 0 | - | - | {'original': 200} |

Where the identity-route items' answers go without J++ (routes run of record):

- qwen3.5-9b: identity items -> {'identity': 103, 'position': 35, 'original': 6}; position items -> {'position': 147, 'original': 4, 'identity': 2}
- qwen3.6-27b: identity items -> {'identity': 135, 'original': 26, 'position': 36}; position items -> {'position': 91, 'original': 10}
- muse-glimmer-30b: identity items -> {'identity': 118, 'original': 5, 'position': 8}; position items -> {'position': 161, 'identity': 1, 'original': 1}
