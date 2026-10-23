# C1 on tasks_v2 / qwen35_9b_full2_ko_pos_context_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 99 | 100 | 100 | 100 |
| L6-10 | paper10 | 92 [86-96] (n=119) | 58 [43-73] (n=43) | 74 [64-83] (n=119) | 86 [70-98] (n=43) | 90 [83-95] (n=105) | 77 [67-85] (n=105) |
| L6-10 | paper10_rot | 98 [95-100] (n=119) | 91 [81-98] (n=43) | 94 [84-99] (n=119) | 98 [92-100] (n=43) | 100 [100-100] (n=105) | 94 [90-98] (n=105) |
| L12-16 | paper10 | 100 [100-100] (n=119) | 95 [89-100] (n=43) | 76 [67-86] (n=119) | 91 [76-100] (n=43) | 99 [97-100] (n=105) | 83 [75-90] (n=105) |
| L12-16 | paper10_rot | 99 [97-100] (n=119) | 91 [82-98] (n=43) | 94 [89-98] (n=119) | 95 [89-100] (n=43) | 100 [100-100] (n=105) | 97 [93-100] (n=105) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L6-10 | paper10 | 97 [92-100] (n=65) | 59 [40-75] (n=22) | 75 [63-87] (n=65) | 86 [65-100] (n=22) | 92 [83-100] (n=51) | 88 [80-96] (n=51) |
| L6-10 | paper10_rot | 98 [95-100] (n=65) | 95 [85-100] (n=22) | 94 [84-100] (n=65) | 95 [85-100] (n=22) | 100 [100-100] (n=51) | 96 [91-100] (n=51) |
| L12-16 | paper10 | 100 [100-100] (n=65) | 95 [85-100] (n=22) | 71 [56-85] (n=65) | 86 [65-100] (n=22) | 100 [100-100] (n=51) | 88 [79-96] (n=51) |
| L12-16 | paper10_rot | 98 [94-100] (n=65) | 95 [85-100] (n=22) | 94 [87-99] (n=65) | 95 [85-100] (n=22) | 100 [100-100] (n=51) | 98 [94-100] (n=51) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 98 | 100 | 100 | 100 |
| L6-10 | paper10 | 85 [74-94] (n=54) | 57 [40-75] (n=21) | 72 [60-83] (n=54) | 86 [65-100] (n=21) | 87 [77-96] (n=54) | 67 [50-81] (n=54) |
| L6-10 | paper10_rot | 98 [94-100] (n=54) | 86 [70-100] (n=21) | 94 [84-100] (n=54) | 100 [100-100] (n=21) | 100 [100-100] (n=54) | 93 [86-98] (n=54) |
| L12-16 | paper10 | 100 [100-100] (n=54) | 95 [88-100] (n=21) | 83 [69-96] (n=54) | 95 [82-100] (n=21) | 98 [94-100] (n=54) | 78 [65-89] (n=54) |
| L12-16 | paper10_rot | 100 [100-100] (n=54) | 86 [71-100] (n=21) | 94 [89-100] (n=54) | 95 [85-100] (n=21) | 100 [100-100] (n=54) | 96 [90-100] (n=54) |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.75, M->P 2.12, P->M 2.62, M->M 2.88. Loss (points) by quartile of that margin (cuts 1.62, 2.62, 3.62), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=24) | 0 (n=33) | 0 (n=37) | 0 (n=25) |
| M->P | 11 (n=18) | 0 (n=9) | 0 (n=7) | 0 (n=9) |
| P->M | 40 (n=35) | 40 (n=25) | 10 (n=31) | 0 (n=28) |
| M->M | 18 (n=11) | 12 (n=8) | 6 (n=17) | 0 (n=7) |
| prompt-final, pooled | 5 (n=42) | 0 (n=42) | 0 (n=44) | 0 (n=34) |
| memory-final, pooled | 35 (n=46) | 33 (n=33) | 8 (n=48) | 0 (n=35) |

Memory-final minus prompt-final, items pooled per group: raw 18; reweighted to the prompt-final margins 19, to the memory-final margins 18; matched within 0.25-logit margin bins 19 [13-25] (161 of 162 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 0, M->P 5, P->M 23, M->M 9, C->P 1, C->M 17; memory-final minus prompt-final 14 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 6c0760e.
