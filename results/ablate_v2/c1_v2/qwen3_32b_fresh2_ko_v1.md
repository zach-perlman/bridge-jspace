# C1 on tasks_v2 / qwen3_32b_fresh2_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L44-52 | paper10 | 99 [97-100] (n=121) | 92 [87-98] (n=50) | 77 [65-87] (n=121) | 80 [67-89] (n=50) | 96 [91-99] (n=91) | 82 [72-91] (n=91) |
| L44-52 | paper10_rot | 100 [100-100] (n=121) | 92 [86-100] (n=50) | 96 [91-99] (n=121) | 100 [100-100] (n=50) | 96 [91-99] (n=91) | 92 [86-98] (n=91) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L44-52 | paper10 | 100 [100-100] (n=60) | 84 [70-96] (n=25) | 77 [63-88] (n=60) | 80 [62-95] (n=25) | 100 [100-100] (n=41) | 78 [66-90] (n=41) |
| L44-52 | paper10_rot | 100 [100-100] (n=60) | 88 [75-100] (n=25) | 95 [87-100] (n=60) | 100 [100-100] (n=25) | 98 [92-100] (n=41) | 93 [82-100] (n=41) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L44-52 | paper10 | 98 [94-100] (n=61) | 100 [100-100] (n=25) | 77 [63-89] (n=61) | 80 [62-95] (n=25) | 92 [84-98] (n=50) | 86 [73-96] (n=50) |
| L44-52 | paper10_rot | 100 [100-100] (n=61) | 96 [89-100] (n=25) | 97 [91-100] (n=61) | 100 [100-100] (n=25) | 94 [86-100] (n=50) | 92 [83-98] (n=50) |


## Margin-matched gap under paper10 at L44-52 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 10.88, M->P 6.75, P->M 7.38, M->M 8.19. Loss (points) by quartile of that margin (cuts 6.62, 8.50, 10.50), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=4) | 0 (n=10) | 3 (n=36) | 0 (n=71) |
| M->P | 16 (n=25) | 0 (n=11) | 0 (n=8) | 0 (n=6) |
| P->M | 50 (n=46) | 7 (n=44) | 7 (n=28) | 0 (n=3) |
| M->M | 64 (n=11) | 9 (n=22) | 6 (n=16) | 0 (n=1) |
| prompt-final, pooled | 14 (n=29) | 0 (n=21) | 2 (n=44) | 0 (n=77) |
| memory-final, pooled | 53 (n=57) | 8 (n=66) | 7 (n=44) | 0 (n=4) |

Memory-final minus prompt-final, items pooled per group: raw 19; reweighted to the prompt-final margins 9, to the memory-final margins 17; matched within 0.25-logit margin bins 15 [6-23] (159 of 171 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L44-52: losses P->P 1, M->P 8, P->M 23, M->M 20, C->P 4, C->M 18; memory-final minus prompt-final 17 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): holds. Output from commit 2d65551.
