# D4 (2): when does the lens's identity stop being the embedding? (Q-depth, Dan: - Part D1: (a) · 60%; (b) · 55%; (c) · 45%
- Part D2: 60%
- Part D3: 40%;
- Part D4: one code · 60%; re-encoded · 30%; in between · 10%). UNVERIFIED.

Per layer the median over test scenes of the W_E-25 part of Delta inside the J++-25 atoms' span and of the J++ part inside the W_E atoms'; overlap = the larger; the first sweep layer below 0.2 against l_J.

| model | layer | n | W_E inside J++ | J++ inside W_E | overlap | share J++ | share W_E |
|---|---|---|---|---|---|---|---|
| qwen3.5-9b | 2 | 200 | 0.055 | 0.057 | 0.057 | 0.260 | 0.198 |
| qwen3.5-9b | 4 | 200 | 0.052 | 0.052 | 0.052 | 0.248 | 0.133 |
| qwen3.5-9b | 6 | 200 | 0.068 | 0.067 | 0.068 | 0.380 | 0.124 |
| qwen3.5-9b | 8 | 200 | 0.048 | 0.049 | 0.049 | 0.266 | 0.112 |
| qwen3.5-9b | 10 | 200 | 0.042 | 0.043 | 0.043 | 0.243 | 0.110 |
| qwen3.5-9b | 12 | 200 | 0.029 | 0.030 | 0.030 | 0.183 | 0.106 |
| qwen3.5-9b | 14 | 200 | 0.026 | 0.027 | 0.027 | 0.161 | 0.105 |
| qwen3.5-9b | 16 | 200 | 0.026 | 0.027 | 0.027 | 0.160 | 0.103 |
| qwen3.5-9b | 18 | 200 | 0.045 | 0.045 | 0.045 | 0.268 | 0.112 |
| qwen3.5-9b | 20 | 200 | 0.040 | 0.041 | 0.041 | 0.245 | 0.111 |
| qwen3.5-9b | 22 | 200 | 0.039 | 0.038 | 0.039 | 0.239 | 0.111 |
| qwen3.5-9b | 24 | 200 | 0.044 | 0.043 | 0.044 | 0.291 | 0.110 |
| qwen3.5-9b | 26 | 200 | 0.049 | 0.047 | 0.049 | 0.318 | 0.110 |
| qwen3.5-9b | 28 | 200 | 0.019 | 0.019 | 0.019 | 0.135 | 0.108 |
| qwen3.5-9b | 30 | 200 | 0.022 | 0.021 | 0.022 | 0.145 | 0.106 |
| muse-glimmer-30b | 2 | 200 | 0.054 | 0.075 | 0.075 | 0.140 | 0.755 |
| muse-glimmer-30b | 6 | 200 | 0.063 | 0.075 | 0.075 | 0.193 | 0.389 |
| muse-glimmer-30b | 10 | 200 | 0.068 | 0.071 | 0.071 | 0.208 | 0.165 |
| muse-glimmer-30b | 14 | 200 | 0.057 | 0.059 | 0.059 | 0.213 | 0.102 |
| muse-glimmer-30b | 18 | 200 | 0.033 | 0.037 | 0.037 | 0.155 | 0.078 |
| muse-glimmer-30b | 22 | 200 | 0.022 | 0.027 | 0.027 | 0.114 | 0.069 |
| muse-glimmer-30b | 26 | 200 | 0.026 | 0.031 | 0.031 | 0.122 | 0.069 |
| muse-glimmer-30b | 30 | 200 | 0.013 | 0.013 | 0.013 | 0.081 | 0.076 |
| muse-glimmer-30b | 34 | 200 | 0.013 | 0.013 | 0.013 | 0.076 | 0.100 |
| muse-glimmer-30b | 38 | 200 | 0.013 | 0.013 | 0.013 | 0.089 | 0.099 |
| muse-glimmer-30b | 42 | 200 | 0.012 | 0.012 | 0.012 | 0.107 | 0.092 |
| muse-glimmer-30b | 46 | 200 | 0.018 | 0.017 | 0.018 | 0.134 | 0.085 |
| muse-glimmer-30b | 50 | 200 | 0.013 | 0.013 | 0.013 | 0.105 | 0.078 |

- qwen3.5-9b: the overlap falls below 0.2 at L2; l_J = L12 (-10 layers)
- muse-glimmer-30b: the overlap falls below 0.2 at L2; l_J = L2 (+0 layers)
