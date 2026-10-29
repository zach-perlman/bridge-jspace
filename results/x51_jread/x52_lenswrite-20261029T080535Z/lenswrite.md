# 51.10's writes at the last token: what the model outputs (descriptive; UNVERIFIED)

Dan, 29 Oct ~09:05 (CPU). Main-test locker-first items of each 51.10 run; the write at P3 (the appended last token) at the reader's read peak; 'none' = unedited. Classes of the top token (full vocabulary): original = O's answer, new = S's answer, digit = another digit, entity = the start of the original or new bridge entity's name, number_word, other. Arms: swap = his swap through the lens; jpp1 / jpp2 = the J++ part of the change at gain 1 / 2; whole = the whole-state patch; *_rand / rand* = the random controls.

## qwen3.5-9b (results/x51_jread/qwen35_9b_x51_10; peaks {'lookup': 24, 'recall': 24})

| reader | arm | n | original | new | digit | entity | number_word | other | top non-answer tokens |
|---|---|---|---|---|---|---|---|---|---|
| recall | none | 75 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| recall | swap | 75 | 0.95 | 0.00 | 0.05 | 0.00 | 0.00 | 0.00 | '6' 2, '5' 1, '2' 1 |
| recall | swap_rand | 75 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| recall | jpp1 | 75 | 0.93 | 0.03 | 0.04 | 0.00 | 0.00 | 0.00 | '6' 1, '5' 1, '3' 1 |
| recall | rand1 | 75 | 0.95 | 0.00 | 0.05 | 0.00 | 0.00 | 0.00 | '6' 2, '5' 1, '3' 1 |
| recall | jpp2 | 75 | 0.65 | 0.15 | 0.20 | 0.00 | 0.00 | 0.00 | '3' 4, '6' 3, '5' 2, '4' 2, '7' 2 |
| recall | rand2 | 75 | 0.84 | 0.04 | 0.12 | 0.00 | 0.00 | 0.00 | '6' 5, '4' 2, '5' 1, '3' 1 |
| recall | whole | 75 | 0.03 | 0.95 | 0.03 | 0.00 | 0.00 | 0.00 | '3' 1, '6' 1 |
| lookup | none | 75 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | swap | 75 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | swap_rand | 75 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | jpp1 | 75 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand1 | 75 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | jpp2 | 75 | 0.97 | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand2 | 75 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | whole | 75 | 0.32 | 0.68 | 0.00 | 0.00 | 0.00 | 0.00 |  |

## qwen3.6-27b (results/x51_jread/x51_10_27b; peaks {'lookup': 60, 'recall': 56})

| reader | arm | n | original | new | digit | entity | number_word | other | top non-answer tokens |
|---|---|---|---|---|---|---|---|---|---|
| recall | none | 69 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| recall | swap | 69 | 0.97 | 0.01 | 0.01 | 0.00 | 0.00 | 0.00 | '5' 1 |
| recall | swap_rand | 69 | 0.99 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | '5' 1 |
| recall | jpp1 | 69 | 0.94 | 0.01 | 0.04 | 0.00 | 0.00 | 0.00 | '5' 3 |
| recall | rand1 | 69 | 0.99 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | '5' 1 |
| recall | jpp2 | 69 | 0.91 | 0.03 | 0.06 | 0.00 | 0.00 | 0.00 | '5' 4 |
| recall | rand2 | 69 | 0.93 | 0.03 | 0.04 | 0.00 | 0.00 | 0.00 | '5' 2, '8' 1 |
| recall | whole | 69 | 0.03 | 0.97 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | none | 69 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | swap | 69 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | swap_rand | 69 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | jpp1 | 69 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand1 | 69 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | jpp2 | 69 | 0.99 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand2 | 69 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | whole | 69 | 0.56 | 0.43 | 0.00 | 0.00 | 0.00 | 0.00 |  |

## muse-glimmer-30b (results/x51_jread/muse30_x51_10; peaks {'lookup': 32, 'recall': 40})

| reader | arm | n | original | new | digit | entity | number_word | other | top non-answer tokens |
|---|---|---|---|---|---|---|---|---|---|
| recall | none | 68 | 0.98 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | '6' 1 |
| recall | swap | 68 | 0.94 | 0.01 | 0.04 | 0.00 | 0.00 | 0.00 | '5' 2, '4' 1 |
| recall | swap_rand | 68 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| recall | jpp1 | 68 | 0.90 | 0.03 | 0.07 | 0.00 | 0.00 | 0.00 | '5' 2, '6' 1, '4' 1, '10' 1 |
| recall | rand1 | 68 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| recall | jpp2 | 68 | 0.38 | 0.38 | 0.23 | 0.00 | 0.00 | 0.00 | '6' 6, '4' 3, '9' 2, '5' 2, '3' 2 |
| recall | rand2 | 68 | 0.90 | 0.04 | 0.06 | 0.00 | 0.00 | 0.00 | '5' 2, '6' 1, '3' 1 |
| recall | whole | 68 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | none | 68 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | swap | 68 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | swap_rand | 68 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | jpp1 | 68 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand1 | 68 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | jpp2 | 68 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand2 | 68 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | whole | 68 | 0.06 | 0.88 | 0.06 | 0.00 | 0.00 | 0.00 | '2' 2, '9' 2 |

## nemotron-3.5-lightning (results/x51_jread/nem35l_x52_jread; peaks {'lookup': 32, 'recall': 36})

| reader | arm | n | original | new | digit | entity | number_word | other | top non-answer tokens |
|---|---|---|---|---|---|---|---|---|---|
| recall | none | 59 | 0.98 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| recall | swap | 59 | 0.78 | 0.14 | 0.09 | 0.00 | 0.00 | 0.00 | '2' 1, '7' 1, '8' 1, '4' 1, '6' 1 |
| recall | swap_rand | 59 | 0.95 | 0.03 | 0.02 | 0.00 | 0.00 | 0.00 | '8' 1 |
| recall | jpp1 | 59 | 0.75 | 0.15 | 0.10 | 0.00 | 0.00 | 0.00 | '6' 2, '9' 2, '3' 1, '5' 1 |
| recall | rand1 | 59 | 0.97 | 0.03 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| recall | jpp2 | 59 | 0.15 | 0.56 | 0.29 | 0.00 | 0.00 | 0.00 | '5' 5, '7' 4, '6' 2, '0' 1, '8' 1 |
| recall | rand2 | 59 | 0.61 | 0.19 | 0.20 | 0.00 | 0.00 | 0.00 | '6' 2, '9' 2, '2' 2, '8' 2, '7' 2 |
| recall | whole | 59 | 0.02 | 0.97 | 0.02 | 0.00 | 0.00 | 0.00 | '6' 1 |
| lookup | none | 59 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | swap | 59 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | swap_rand | 59 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | jpp1 | 59 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand1 | 59 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | jpp2 | 59 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | rand2 | 59 | 0.98 | 0.02 | 0.00 | 0.00 | 0.00 | 0.00 |  |
| lookup | whole | 59 | 0.07 | 0.90 | 0.03 | 0.00 | 0.00 | 0.00 | '9' 1, '3' 1 |

