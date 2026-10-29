# The address swap: when the recall changes, what to (descriptive; UNVERIFIED)

Dan, 29 Oct ~09:05 (CPU). x8_write's recall rows (the swap s (mu_k - mu_j) at the bridge word at L; random = a random vector of the same norm). Scenes rebuilt on CPU (x6_routes.scenes, matched by scene id; every row's bridge and original answer checked). Of the changed recalls: swapped_in = the legs of slot k's item (the item the swap points to), third = the third item's legs, digit = another digit, non_answer = anything else. Items with equal legs make classes overlap (swapped_in is checked first).

## qwen3.5-9b (results/x8_write/qwen35_9b_x8_write; 3000 rows checked)

| arm | s | n | changed | of changed: n | swapped_in | third | digit | non_answer |
|---|---|---|---|---|---|---|---|---|
| write | 1 | 600 | 0.04 | 24 | 0.88 | 0.12 | 0.00 | 0.00 |
| write | 2 | 600 | 0.21 | 129 | 0.84 | 0.09 | 0.06 | 0.00 |
| write | 4 | 600 | 0.43 | 256 | 0.80 | 0.15 | 0.05 | 0.00 |
| random | 1 | 600 | 0.01 | 3 | 0.00 | 0.33 | 0.67 | 0.00 |
| random | 4 | 600 | 0.03 | 18 | 0.28 | 0.44 | 0.28 | 0.00 |

## nemotron-3.5-lightning (results/x8_write/nem35l_x52_write; 3000 rows checked)

| arm | s | n | changed | of changed: n | swapped_in | third | digit | non_answer |
|---|---|---|---|---|---|---|---|---|
| write | 1 | 600 | 0.02 | 12 | 0.75 | 0.08 | 0.17 | 0.00 |
| write | 2 | 600 | 0.27 | 164 | 0.85 | 0.07 | 0.08 | 0.00 |
| write | 4 | 600 | 0.40 | 239 | 0.84 | 0.10 | 0.05 | 0.00 |
| random | 1 | 600 | 0.00 | 1 | 0.00 | 1.00 | 0.00 | 0.00 |
| random | 4 | 600 | 0.01 | 8 | 0.38 | 0.12 | 0.50 | 0.00 |

