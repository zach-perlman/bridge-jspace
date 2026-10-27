# The slot pairs: address stability and the real pointer part (after the data, descriptive)

(a) cos between the two halves' mu_k - mu_j (probe states split by bridge entity, seed 0); separation = ||mu_k - mu_j|| / the pooled within-class SD of the layout-free states along that direction (all states). (b) Routes C2, keep-only arm: the lookup's position share with only the real change's pointer part added, by the two slots S swapped; the whole change and the random part of the pointer's size beside it. x8: the mean-difference write's target share at s = 4, both directions of the pair pooled. UNVERIFIED.

| model | pair | cos (half A, half B) | separation | ‖μk − μj‖ | within SD | x8 write s = 4 target | n | keep-only pointer: position | whole: position | keep-only random: position | n |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | 0 ↔ 1 | 0.93 | 1.87 | 4.10 | 2.20 | 0.92 | 201 | 0.09 | 0.76 | 0.00 | 99 |
| qwen3.5-9b | 0 ↔ 2 | 0.93 | 2.06 | 4.82 | 2.34 | 0.78 | 192 | 0.22 | 0.54 | 0.00 | 108 |
| qwen3.5-9b | 1 ↔ 2 | 0.81 | 1.34 | 2.43 | 1.81 | 0.52 | 207 | 0.48 | 0.22 | 0.00 | 93 |
| qwen3.6-27b | 0 ↔ 1 | 0.94 | 1.81 | 13.57 | 7.51 | 0.86 | 200 | 0.00 | 0.46 | 0.00 | 100 |
| qwen3.6-27b | 0 ↔ 2 | 0.96 | 2.03 | 16.79 | 8.28 | 0.65 | 189 | 0.04 | 0.39 | 0.00 | 111 |
| qwen3.6-27b | 1 ↔ 2 | 0.83 | 1.25 | 8.39 | 6.73 | 0.02 | 211 | 0.26 | 0.13 | 0.01 | 89 |
| qwen3.5-122b-a10b | 0 ↔ 1 | 0.93 | 1.95 | 0.93 | 0.47 | 0.89 | 199 | 0.08 | 0.50 | 0.00 | 101 |
| qwen3.5-122b-a10b | 0 ↔ 2 | 0.94 | 2.06 | 1.05 | 0.51 | 0.81 | 197 | 0.26 | 0.52 | 0.00 | 103 |
| qwen3.5-122b-a10b | 1 ↔ 2 | 0.79 | 1.27 | 0.52 | 0.41 | 0.28 | 204 | 0.28 | 0.11 | 0.00 | 96 |
| muse-glimmer-30b | 0 ↔ 1 | 0.92 | 1.78 | 41.38 | 23.26 | – | 0 | 0.16 | 0.68 | 0.02 | 100 |
| muse-glimmer-30b | 0 ↔ 2 | 0.92 | 2.09 | 50.84 | 24.32 | – | 0 | 0.18 | 0.47 | 0.00 | 101 |
| muse-glimmer-30b | 1 ↔ 2 | 0.74 | 1.20 | 24.87 | 20.65 | – | 0 | 0.55 | 0.48 | 0.01 | 99 |

Reading (Dan, fixed before this table): if the real pointer part moves the lookup between slots 1 and 2 but the mean-difference vector does not, or its direction is unstable across halves -> our estimate's artefact; if neither moves it and the direction is stable -> the model's code separates the first slot from the rest more than the second from the third.
