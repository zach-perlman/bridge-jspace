# C1 on tasks_v2 / qwen35_9b_full2_ko_keepown_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 99 | 100 | 100 | 100 |
| L12-16 | paper10 | 97 [94-100] (n=119) | 93 [85-98] (n=43) | 62 [51-74] (n=119) | 51 [30-71] (n=43) | 99 [97-100] (n=105) | 64 [52-75] (n=105) |
| L12-16 | paper10_rot | 99 [97-100] (n=119) | 91 [81-98] (n=43) | 95 [91-98] (n=119) | 95 [89-100] (n=43) | 99 [97-100] (n=105) | 95 [91-99] (n=105) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 100 [100-100] (n=65) | 95 [85-100] (n=22) | 60 [46-74] (n=65) | 50 [32-68] (n=22) | 98 [93-100] (n=51) | 69 [55-83] (n=51) |
| L12-16 | paper10_rot | 98 [94-100] (n=65) | 95 [85-100] (n=22) | 92 [84-98] (n=65) | 91 [78-100] (n=22) | 100 [100-100] (n=51) | 96 [91-100] (n=51) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 98 | 100 | 100 | 100 |
| L12-16 | paper10 | 94 [88-100] (n=54) | 90 [78-100] (n=21) | 65 [50-80] (n=54) | 52 [22-79] (n=21) | 100 [100-100] (n=54) | 59 [44-73] (n=54) |
| L12-16 | paper10_rot | 100 [100-100] (n=54) | 86 [68-100] (n=21) | 98 [95-100] (n=54) | 100 [100-100] (n=21) | 98 [94-100] (n=54) | 94 [88-100] (n=54) |


Keep-own-word kill test at L12-16 (memory-final words): P->M unedited 99 / paper10 62 / keep-own 69 (its control 94), M->M unedited 100 / paper10 51 / keep-own 67 (its control 95); restored 26% of the damage (>= 75% kills C1); control within 10: yes -> C1 survives

## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.75, M->P 2.12, P->M 2.62, M->M 2.88. Loss (points) by quartile of that margin (cuts 1.62, 2.62, 3.62), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 4 (n=24) | 3 (n=33) | 3 (n=37) | 0 (n=25) |
| M->P | 17 (n=18) | 0 (n=9) | 0 (n=7) | 0 (n=9) |
| P->M | 66 (n=35) | 52 (n=25) | 16 (n=31) | 11 (n=28) |
| M->M | 45 (n=11) | 88 (n=8) | 47 (n=17) | 14 (n=7) |
| prompt-final, pooled | 10 (n=42) | 2 (n=42) | 2 (n=44) | 0 (n=34) |
| memory-final, pooled | 61 (n=46) | 61 (n=33) | 27 (n=48) | 11 (n=35) |

Memory-final minus prompt-final, items pooled per group: raw 36; reweighted to the prompt-final margins 38, to the memory-final margins 36; matched within 0.25-logit margin bins 38 [30-46] (161 of 162 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 3, M->P 7, P->M 37, M->M 49, C->P 1, C->M 36; memory-final minus prompt-final 38 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit 6c0760e.
