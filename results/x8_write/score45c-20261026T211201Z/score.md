# Batch 45c: second vs third (scored against the rule fixed in advance)

| routes run | n | position: whole / without / random part / only it / only a random part | cut [CI] | halves | random part's cut [CI] | random part halves | keep >= 0.15 | found |
|---|---|---|---|---|---|---|---|---|
| qwen35_9b_x6_routes_pcf12 | 96 | 0.66 / 0.52 / 0.61 / 0.00 / 0.00 | 0.14 [0.07, 0.21] | False | 0.04 [0.00, 0.09] | False | False | False |
| x6_routes_pcf12_27b | 104 | 0.31 / 0.17 / 0.27 / 0.01 / 0.00 | 0.13 [0.07, 0.21] | False | 0.04 [0.01, 0.08] | False | False | False |
| muse30b_x6_routes_pcf12 | 96 | 0.60 / 0.50 / 0.61 / 0.09 / 0.02 | 0.10 [0.05, 0.17] | False | -0.01 [-0.04, 0.02] | False | False | False |

Found on 0 of 3 models (Q45.6: all three / one or two / none). The random part's cut and halves are beside the rule, not in it (Dan 26 Oct ~21:20).

## The writes between the second and third slot (descriptive)

| write run | move | kind | dose | n | target share |
|---|---|---|---|---|---|
| qwen35_9b_x8_write12 | 1 → 2 | random | 1 | 108 | 0.00 |
| qwen35_9b_x8_write12 | 1 → 2 | random | 4 | 108 | 0.00 |
| qwen35_9b_x8_write12 | 1 → 2 | write | 1 | 108 | 0.06 |
| qwen35_9b_x8_write12 | 1 → 2 | write | 2 | 108 | 0.70 |
| qwen35_9b_x8_write12 | 1 → 2 | write | 3 | 108 | 0.69 |
| qwen35_9b_x8_write12 | 1 → 2 | write | 4 | 108 | 0.66 |
| qwen35_9b_x8_write12 | 2 → 1 | random | 1 | 99 | 0.00 |
| qwen35_9b_x8_write12 | 2 → 1 | random | 4 | 99 | 0.00 |
| qwen35_9b_x8_write12 | 2 → 1 | write | 1 | 99 | 0.07 |
| qwen35_9b_x8_write12 | 2 → 1 | write | 2 | 99 | 0.78 |
| qwen35_9b_x8_write12 | 2 → 1 | write | 3 | 99 | 0.91 |
| qwen35_9b_x8_write12 | 2 → 1 | write | 4 | 99 | 0.92 |
| x8_write12_27b | 1 → 2 | random | 1 | 111 | 0.00 |
| x8_write12_27b | 1 → 2 | random | 4 | 111 | 0.00 |
| x8_write12_27b | 1 → 2 | write | 1 | 111 | 0.00 |
| x8_write12_27b | 1 → 2 | write | 2 | 111 | 0.03 |
| x8_write12_27b | 1 → 2 | write | 3 | 111 | 0.22 |
| x8_write12_27b | 1 → 2 | write | 4 | 111 | 0.41 |
| x8_write12_27b | 2 → 1 | random | 1 | 100 | 0.00 |
| x8_write12_27b | 2 → 1 | random | 4 | 100 | 0.01 |
| x8_write12_27b | 2 → 1 | write | 1 | 100 | 0.00 |
| x8_write12_27b | 2 → 1 | write | 2 | 100 | 0.06 |
| x8_write12_27b | 2 → 1 | write | 3 | 100 | 0.55 |
| x8_write12_27b | 2 → 1 | write | 4 | 100 | 0.73 |
| muse30b_x8_write12 | 1 → 2 | random | 1 | 101 | 0.00 |
| muse30b_x8_write12 | 1 → 2 | random | 4 | 101 | 0.04 |
| muse30b_x8_write12 | 1 → 2 | write | 1 | 101 | 0.09 |
| muse30b_x8_write12 | 1 → 2 | write | 2 | 101 | 0.39 |
| muse30b_x8_write12 | 1 → 2 | write | 3 | 101 | 0.52 |
| muse30b_x8_write12 | 1 → 2 | write | 4 | 101 | 0.50 |
| muse30b_x8_write12 | 2 → 1 | random | 1 | 100 | 0.01 |
| muse30b_x8_write12 | 2 → 1 | random | 4 | 100 | 0.14 |
| muse30b_x8_write12 | 2 → 1 | write | 1 | 100 | 0.13 |
| muse30b_x8_write12 | 2 → 1 | write | 2 | 100 | 0.55 |
| muse30b_x8_write12 | 2 → 1 | write | 3 | 100 | 0.80 |
| muse30b_x8_write12 | 2 → 1 | write | 4 | 100 | 0.80 |
