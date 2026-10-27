# What the models answer when the answer's sentence is hidden

Question: finding 1's paradox (Qwen3-32B: hiding the answer's sentence from the last tokens leaves 3% right, hiding it from every token after it 10%). Dan's hypothesis: under the second block the model guesses while excluding the digits it can still see in the list.

Runs: each model's first scene set late-read run (the grid's late-read-v2 rows "draw 1"), memory → prompt items: five sentences "The <thing>'s locker is <digit>.", the asked thing's digit is the answer, so four other digits stay visible in the list. Commit b42b21a (uncommitted changes in the tree), script scripts/late_read_guess.py; no seeds (deterministic re-analysis of the runs' rows).

Each answer (the model's top next token after "Answer: ", whitespace stripped) is one of: right = the hidden sentence's digit; visible = another sentence's digit; outside = a digit in no sentence (0 counted apart: the data draws digits 1 to 9 only); not a digit. Blocked rows: items right unedited (the grid's items); the unedited row: all items. Rates: Wilson 95%.

"Right among outside" = right / (right + outside): how often the answer is the hidden digit when it is not a visible one. Its chance under exclusion (guessing uniformly among the digits not visible) is 1 / (digits not in the visible list, the hidden one included): every item here lists 4 visible digits, so 1/6 with 0 to 9 and 1/5 with 1 to 9 (the "1-9" column leaves the zeros out). A blind guess that does not exclude gives the same conditional chance; exclusion shows in the visible share, against a blind guess's 4/10 (0-9) or 4/9 (1-9).

Gate: the right share per blocked arm rounds to the grid's numbers (results/cross_model/20261023T121807Z/grid.csv): passed for every run. Every row's "right" class equals the run's own correct flag: yes.

| model | hidden | layers | n | right | visible | outside (of which 0) | not a digit | right among outside, 0-9 (n) | chance | right among outside, 1-9 (n) | chance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | nothing hidden (all items) | - | 300 | 300 (100% [99, 100]) | 0 (0% [0, 1]) | 0 (0) | 0 | 100% [99, 100] (300) | 17% | 100% [99, 100] (300) | 20% |
| Qwen3.6-27B | hidden from the last tokens | every attention layer | 300 | 26 (9% [6, 12]) | 263 (88% [83, 91]) | 11 (0) | 0 | 70% [54, 83] (37) | 17% | 70% [54, 83] (37) | 20% |
| Qwen3.6-27B | hidden from every token after it | all layers | 300 | 2 (1% [0, 2]) | 295 (98% [96, 99]) | 3 (0) | 0 | 40% [12, 77] (5) | 17% | 40% [12, 77] (5) | 20% |
| Qwen3.6-27B | hidden from the last tokens, all layers (not in the grid) | all layers | 300 | 26 (9% [6, 12]) | 265 (88% [84, 91]) | 9 (0) | 0 | 74% [58, 86] (35) | 17% | 74% [58, 86] (35) | 20% |
| Qwen3.5-9B | nothing hidden (all items) | - | 300 | 300 (100% [99, 100]) | 0 (0% [0, 1]) | 0 (0) | 0 | 100% [99, 100] (300) | 17% | 100% [99, 100] (300) | 20% |
| Qwen3.5-9B | hidden from the last tokens | every attention layer | 300 | 8 (3% [1, 5]) | 289 (96% [94, 98]) | 3 (0) | 0 | 73% [43, 90] (11) | 17% | 73% [43, 90] (11) | 20% |
| Qwen3.5-9B | hidden from every token after it | all layers | 300 | 8 (3% [1, 5]) | 255 (85% [81, 89]) | 37 (0) | 0 | 18% [9, 31] (45) | 17% | 18% [9, 31] (45) | 20% |
| Qwen3.5-9B | hidden from the last tokens, all layers (not in the grid) | all layers | 300 | 7 (2% [1, 5]) | 291 (97% [94, 98]) | 2 (0) | 0 | 78% [45, 94] (9) | 17% | 78% [45, 94] (9) | 20% |
| Olmo-Hybrid-7B | nothing hidden (all items) | - | 100 | 100 (100% [96, 100]) | 0 (0% [0, 4]) | 0 (0) | 0 | 100% [96, 100] (100) | 17% | 100% [96, 100] (100) | 20% |
| Olmo-Hybrid-7B | hidden from the last tokens | every attention layer | 100 | 8 (8% [4, 15]) | 73 (73% [64, 81]) | 19 (0) | 0 | 30% [16, 48] (27) | 17% | 30% [16, 48] (27) | 20% |
| Olmo-Hybrid-7B | hidden from every token after it | all layers | 100 | 5 (5% [2, 11]) | 40 (40% [31, 50]) | 55 (0) | 0 | 8% [4, 18] (60) | 17% | 8% [4, 18] (60) | 20% |
| Olmo-Hybrid-7B | hidden from the last tokens, all layers (not in the grid) | all layers | 100 | 7 (7% [3, 14]) | 71 (71% [61, 79]) | 22 (0) | 0 | 24% [12, 42] (29) | 17% | 24% [12, 42] (29) | 20% |
| Qwen3-32B | nothing hidden (all items) | - | 300 | 300 (100% [99, 100]) | 0 (0% [0, 1]) | 0 (0) | 0 | 100% [99, 100] (300) | 17% | 100% [99, 100] (300) | 20% |
| Qwen3-32B | hidden from the last tokens | all layers | 300 | 10 (3% [2, 6]) | 278 (93% [89, 95]) | 12 (0) | 0 | 45% [27, 65] (22) | 17% | 45% [27, 65] (22) | 20% |
| Qwen3-32B | hidden from every token after it | all layers | 300 | 29 (10% [7, 14]) | 157 (52% [47, 58]) | 112 (0) | 2 | 21% [15, 28] (141) | 17% | 21% [15, 28] (141) | 20% |
| OLMo-3-7B-I | nothing hidden (all items) | - | 100 | 100 (100% [96, 100]) | 0 (0% [0, 4]) | 0 (0) | 0 | 100% [96, 100] (100) | 17% | 100% [96, 100] (100) | 20% |
| OLMo-3-7B-I | hidden from the last tokens | all layers | 100 | 0 (0% [0, 4]) | 96 (96% [90, 98]) | 1 (0) | 3 | 0% [0, 79] (1) | 17% | 0% [0, 79] (1) | 20% |
| OLMo-3-7B-I | hidden from every token after it | all layers | 100 | 4 (4% [2, 10]) | 39 (39% [30, 49]) | 30 (21) | 27 | 12% [5, 27] (34) | 17% | 31% [13, 58] (13) | 20% |
| Gemma 4 31B-it | nothing hidden (all items) | - | 300 | 300 (100% [99, 100]) | 0 (0% [0, 1]) | 0 (0) | 0 | 100% [99, 100] (300) | 17% | 100% [99, 100] (300) | 20% |
| Gemma 4 31B-it | hidden from the last tokens | all layers | 300 | 68 (23% [18, 28]) | 225 (75% [70, 80]) | 7 (0) | 0 | 91% [82, 95] (75) | 17% | 91% [82, 95] (75) | 20% |
| Gemma 4 31B-it | hidden from every token after it | all layers | 300 | 5 (2% [1, 4]) | 155 (52% [46, 57]) | 140 (101) | 0 | 3% [1, 8] (145) | 17% | 11% [5, 24] (44) | 20% |

Visible answers by their sentence's place relative to the hidden sentence (-1 = the sentence just before it), and the answers that are not a digit:

| model | hidden | visible answers by place | not a digit |
|---|---|---|---|
| Qwen3.6-27B | nothing hidden (all items) | - | - |
| Qwen3.6-27B | hidden from the last tokens | -4: 28, -3: 24, -2: 71, -1: 88, +1: 26, +2: 11, +3: 9, +4: 6 | - |
| Qwen3.6-27B | hidden from every token after it | -4: 23, -3: 39, -2: 56, -1: 68, +1: 41, +2: 28, +3: 26, +4: 14 | - |
| Qwen3.6-27B | hidden from the last tokens, all layers (not in the grid) | -4: 28, -3: 25, -2: 75, -1: 83, +1: 24, +2: 15, +3: 9, +4: 6 | - |
| Qwen3.5-9B | nothing hidden (all items) | - | - |
| Qwen3.5-9B | hidden from the last tokens | -4: 2, -3: 27, -2: 64, -1: 84, +1: 45, +2: 32, +3: 17, +4: 18 | - |
| Qwen3.5-9B | hidden from every token after it | -4: 21, -3: 29, -2: 37, -1: 46, +1: 55, +2: 30, +3: 22, +4: 15 | - |
| Qwen3.5-9B | hidden from the last tokens, all layers (not in the grid) | -4: 4, -3: 27, -2: 62, -1: 87, +1: 45, +2: 29, +3: 16, +4: 21 | - |
| Olmo-Hybrid-7B | nothing hidden (all items) | - | - |
| Olmo-Hybrid-7B | hidden from the last tokens | -4: 12, -3: 12, -2: 21, -1: 16, +1: 4, +2: 3, +3: 3, +4: 2 | - |
| Olmo-Hybrid-7B | hidden from every token after it | -4: 15, -3: 2, -2: 8, -1: 6, +1: 8, +4: 1 | - |
| Olmo-Hybrid-7B | hidden from the last tokens, all layers (not in the grid) | -4: 12, -3: 11, -2: 21, -1: 16, +1: 3, +2: 3, +3: 3, +4: 2 | - |
| Qwen3-32B | nothing hidden (all items) | - | - |
| Qwen3-32B | hidden from the last tokens | -4: 9, -3: 30, -2: 58, -1: 77, +1: 49, +2: 28, +3: 18, +4: 9 | - |
| Qwen3-32B | hidden from every token after it | -4: 7, -3: 13, -2: 20, -1: 37, +1: 34, +2: 26, +3: 8, +4: 12 | ' none' ×2 |
| OLMo-3-7B-I | nothing hidden (all items) | - | - |
| OLMo-3-7B-I | hidden from the last tokens | -3: 10, -2: 18, -1: 33, +1: 12, +2: 9, +3: 8, +4: 6 | ' There' ×1, ' None' ×2 |
| OLMo-3-7B-I | hidden from every token after it | -4: 2, -2: 7, -1: 9, +1: 13, +2: 5, +3: 1, +4: 2 | '<|endoftext|>' ×23, ' (' ×2, ' None' ×2 |
| Gemma 4 31B-it | nothing hidden (all items) | - | - |
| Gemma 4 31B-it | hidden from the last tokens | -4: 33, -3: 43, -2: 55, -1: 86, +1: 4, +2: 1, +3: 3 | - |
| Gemma 4 31B-it | hidden from every token after it | -4: 13, -3: 15, -2: 32, -1: 30, +1: 26, +2: 17, +3: 15, +4: 7 | - |
