# The slot pairs (after the data, descriptive)

(a) cos between the two halves' mu_k - mu_j (probe states split by bridge entity, seed 0); separation = ||mu_k - mu_j|| / the pooled within-class SD of the layout-free states along that direction. (b) The routes test's C2 items grouped by the pointer's move, from the O bridge's locker slot to the S bridge's (Dan's correction, ~16:00: the first version grouped by the two slots S swapped, which is not the pointer's move). UNVERIFIED.

## (a) The address vectors per slot pair

| model | pair | cos (half A, half B) | separation | ‖μk − μj‖ | within SD |
|---|---|---|---|---|---|
| qwen3.5-9b | 0 ↔ 1 | 0.93 | 1.87 | 4.10 | 2.20 |
| qwen3.5-9b | 0 ↔ 2 | 0.93 | 2.06 | 4.82 | 2.34 |
| qwen3.5-9b | 1 ↔ 2 | 0.81 | 1.34 | 2.43 | 1.81 |
| qwen3.6-27b | 0 ↔ 1 | 0.94 | 1.81 | 13.57 | 7.51 |
| qwen3.6-27b | 0 ↔ 2 | 0.96 | 2.03 | 16.79 | 8.28 |
| qwen3.6-27b | 1 ↔ 2 | 0.83 | 1.25 | 8.39 | 6.73 |
| qwen3.5-122b-a10b | 0 ↔ 1 | 0.93 | 1.95 | 0.93 | 0.47 |
| qwen3.5-122b-a10b | 0 ↔ 2 | 0.94 | 2.06 | 1.05 | 0.51 |
| qwen3.5-122b-a10b | 1 ↔ 2 | 0.79 | 1.27 | 0.52 | 0.41 |
| muse-glimmer-30b | 0 ↔ 1 | 0.92 | 1.78 | 41.38 | 23.26 |
| muse-glimmer-30b | 0 ↔ 2 | 0.92 | 2.09 | 50.84 | 24.32 |
| muse-glimmer-30b | 1 ↔ 2 | 0.74 | 1.20 | 24.87 | 20.65 |

## (b) Per pointer move j -> k: the lookup's position share (routes C2) and the mean-difference write

| model | move | n | whole | without the pointer | without its random part | only the pointer part | only a random part | x8 write s = 4: target | without P_cf | only P_cf |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | 0 → 1 | 54 | 0.31 | 0.00 | 0.48 | 0.76 | 0.00 | 0.89 | 0.00 | 0.61 |
| qwen3.5-9b | 0 → 2 | 39 | 0.08 | 0.00 | 0.08 | 0.10 | 0.00 | 0.67 | 0.00 | 0.56 |
| qwen3.5-9b | 1 → 0 | 61 | 0.54 | 0.00 | 0.54 | 0.39 | 0.00 | 0.94 | 0.03 | 0.64 |
| qwen3.5-9b | 1 → 2 | 47 | 0.53 | 0.28 | 0.55 | 0.00 | 0.00 | 0.51 | 0.06 | 0.09 |
| qwen3.5-9b | 2 → 0 | 50 | 0.74 | 0.10 | 0.82 | 0.18 | 0.00 | 0.88 | 0.10 | 0.44 |
| qwen3.5-9b | 2 → 1 | 49 | 0.78 | 0.14 | 0.69 | 0.00 | 0.00 | 0.54 | 0.06 | 0.18 |
| qwen3.6-27b | 0 → 1 | 48 | 0.21 | 0.04 | 0.21 | 0.44 | 0.02 | 0.87 | 0.06 | 0.44 |
| qwen3.6-27b | 0 → 2 | 41 | 0.02 | 0.00 | 0.00 | 0.05 | 0.00 | 0.49 | 0.00 | 0.41 |
| qwen3.6-27b | 1 → 0 | 57 | 0.53 | 0.00 | 0.32 | 0.07 | 0.00 | 0.86 | 0.05 | 0.28 |
| qwen3.6-27b | 1 → 2 | 54 | 0.24 | 0.20 | 0.19 | 0.00 | 0.00 | 0.02 | 0.02 | 0.00 |
| qwen3.6-27b | 2 → 0 | 50 | 0.56 | 0.02 | 0.42 | 0.00 | 0.00 | 0.79 | 0.00 | 0.30 |
| qwen3.6-27b | 2 → 1 | 50 | 0.38 | 0.08 | 0.34 | 0.00 | 0.00 | 0.02 | 0.02 | 0.06 |
| qwen3.5-122b-a10b | 0 → 1 | 53 | 0.06 | 0.00 | 0.11 | 0.34 | 0.00 | 0.78 | 0.00 | 0.43 |
| qwen3.5-122b-a10b | 0 → 2 | 43 | 0.19 | 0.00 | 0.16 | 0.21 | 0.00 | 0.61 | 0.00 | 0.56 |
| qwen3.5-122b-a10b | 1 → 0 | 58 | 0.62 | 0.02 | 0.55 | 0.47 | 0.00 | 0.99 | 0.03 | 0.59 |
| qwen3.5-122b-a10b | 1 → 2 | 45 | 0.40 | 0.20 | 0.40 | 0.00 | 0.00 | 0.45 | 0.07 | 0.07 |
| qwen3.5-122b-a10b | 2 → 0 | 55 | 0.62 | 0.02 | 0.56 | 0.15 | 0.00 | 1.00 | 0.02 | 0.49 |
| qwen3.5-122b-a10b | 2 → 1 | 46 | 0.35 | 0.07 | 0.30 | 0.00 | 0.00 | 0.12 | 0.02 | 0.04 |
| muse-glimmer-30b | 0 → 1 | 52 | 0.69 | 0.31 | 0.71 | 0.69 | 0.00 | 0.62 | 0.21 | 0.73 |
| muse-glimmer-30b | 0 → 2 | 47 | 0.26 | 0.11 | 0.23 | 0.38 | 0.02 | 0.46 | 0.04 | 0.79 |
| muse-glimmer-30b | 1 → 0 | 56 | 0.45 | 0.09 | 0.43 | 0.29 | 0.00 | 0.68 | 0.14 | 0.34 |
| muse-glimmer-30b | 1 → 2 | 45 | 0.49 | 0.38 | 0.53 | 0.04 | 0.00 | 0.33 | 0.18 | 0.27 |
| muse-glimmer-30b | 2 → 0 | 49 | 0.65 | 0.20 | 0.63 | 0.16 | 0.00 | 0.66 | 0.14 | 0.53 |
| muse-glimmer-30b | 2 → 1 | 51 | 0.71 | 0.57 | 0.73 | 0.16 | 0.04 | 0.38 | 0.45 | 0.31 |

Reading (Dan ~16:00): the pointer directions carry first slot vs the rest; the model also separates slots 1 and 2 (the whole change gives position answers there) but mostly outside the 4 pointer directions. Neither branch of the reading fixed before fits (that the mean-difference vector is our artefact, or that the model does not separate 1 and 2): a third outcome.
