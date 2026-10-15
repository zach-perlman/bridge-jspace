# exp06_sigma_writes / sigma_v1

| task | lens | condition / λ | scale | null | n | flip [95% CI] |
|---|---|---|---|---|---|---|
| matched | jpp | jpart |  |  | 77 | 52% [41, 63] |
| matched | jpp | jpart |  | yes | 77 | 0% [0, 5] |
| matched | jpp | jpart_matched |  |  | 77 | 14% [8, 24] |
| matched | jpp | jpart_matched |  | yes | 77 | 0% [0, 5] |
| matched | jpp | jpart_matched_sigma |  |  | 77 | 12% [6, 21] |
| matched | jpp | jpart_matched_sigma |  | yes | 77 | 4% [1, 11] |
| steer | jpp | λ=1.0 | 0.03 |  | 164 | 63% [55, 70] |
| steer | jpp | λ=0.5 | 0.03 |  | 164 | 13% [9, 19] |
| steer | jpp | λ=0.1 | 0.03 |  | 164 | 4% [2, 9] |
| steer | jpp | λ=0.0 | 0.03 |  | 164 | 3% [1, 7] |
| steer | jpp |  | 0.03 | yes | 164 | 0% [0, 2] |
| steer | jpp | λ=1.0 | 0.05 |  | 164 | 49% [42, 57] |
| steer | jpp | λ=0.5 | 0.05 |  | 164 | 34% [27, 42] |
| steer | jpp | λ=0.1 | 0.05 |  | 164 | 23% [17, 30] |
| steer | jpp | λ=0.0 | 0.05 |  | 164 | 21% [15, 28] |
| steer | jpp |  | 0.05 | yes | 164 | 0% [0, 2] |
| matched | jlens | jpart |  |  | 77 | 35% [25, 46] |
| matched | jlens | jpart |  | yes | 77 | 1% [0, 7] |
| matched | jlens | jpart_matched |  |  | 77 | 10% [5, 19] |
| matched | jlens | jpart_matched |  | yes | 77 | 0% [0, 5] |
| matched | jlens | jpart_matched_sigma |  |  | 77 | 14% [8, 24] |
| matched | jlens | jpart_matched_sigma |  | yes | 77 | 4% [1, 11] |
| steer | jlens | λ=1.0 | 0.03 |  | 164 | 30% [23, 37] |
| steer | jlens | λ=0.5 | 0.03 |  | 164 | 1% [0, 3] |
| steer | jlens | λ=0.1 | 0.03 |  | 164 | 1% [0, 3] |
| steer | jlens | λ=0.0 | 0.03 |  | 164 | 1% [0, 3] |
| steer | jlens |  | 0.03 | yes | 164 | 0% [0, 2] |
| steer | jlens | λ=1.0 | 0.05 |  | 164 | 35% [28, 43] |
| steer | jlens | λ=0.5 | 0.05 |  | 164 | 12% [8, 17] |
| steer | jlens | λ=0.1 | 0.05 |  | 164 | 8% [5, 13] |
| steer | jlens | λ=0.0 | 0.05 |  | 164 | 8% [5, 13] |
| steer | jlens |  | 0.05 | yes | 164 | 0% [0, 2] |

Paired bootstrap differences in flip rate:
- matched jpp: jpart - matched_sigma: +40 pts [+27, +53]
- matched jpp: matched_sigma - matched: -3 pts [-12, +6]
- steer jpp 0.03: lambda 0.5 - lambda 1: -50 pts [-58, -42]
- steer jpp 0.03: lambda 0.1 - lambda 1: -59 pts [-66, -51]
- steer jpp 0.03: lambda 0.0 - lambda 1: -60 pts [-68, -52]
- steer jpp 0.05: lambda 0.5 - lambda 1: -15 pts [-23, -7]
- steer jpp 0.05: lambda 0.1 - lambda 1: -27 pts [-35, -19]
- steer jpp 0.05: lambda 0.0 - lambda 1: -29 pts [-37, -20]
- matched jlens: jpart - matched_sigma: +21 pts [+9, +32]
- matched jlens: matched_sigma - matched: +4 pts [-4, +12]
- steer jlens 0.03: lambda 0.5 - lambda 1: -29 pts [-37, -23]
- steer jlens 0.03: lambda 0.1 - lambda 1: -29 pts [-37, -23]
- steer jlens 0.03: lambda 0.0 - lambda 1: -29 pts [-37, -23]
- steer jlens 0.05: lambda 0.5 - lambda 1: -24 pts [-32, -16]
- steer jlens 0.05: lambda 0.1 - lambda 1: -27 pts [-35, -20]
- steer jlens 0.05: lambda 0.0 - lambda 1: -27 pts [-35, -20]

Reproduction of earlier runs (items whose flip matches):
- matched jpp jpart: 77/77
- matched jpp jpart_matched: 77/77
- steer jpp 0.03 lambda 1: 162/164
- steer jpp 0.05 lambda 1: 162/164
- matched jlens jpart: 77/77
- matched jlens jpart_matched: 77/77
- steer jlens 0.03 lambda 1: 163/164
- steer jlens 0.05 lambda 1: 164/164
