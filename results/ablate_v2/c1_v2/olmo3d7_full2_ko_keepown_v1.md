# C1 on tasks_v2 / olmo3d7_full2_ko_keepown_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 95 | 100 | 100 | 100 | 100 |
| L10-14 | paper10 | 91 [80-98] (n=66) | 80 [67-100] (n=20) | 92 [86-98] (n=66) | 95 [80-100] (n=20) | 95 [86-100] (n=43) | 88 [80-95] (n=43) |
| L10-14 | paper10_rot | 91 [82-98] (n=66) | 95 [80-100] (n=20) | 100 [100-100] (n=66) | 100 [100-100] (n=20) | 95 [89-100] (n=43) | 91 [80-100] (n=43) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L10-14 | paper10 | 94 [82-100] (n=35) | 73 [50-100] (n=11) | 94 [87-100] (n=35) | 100 [100-100] (n=11) | 100 [100-100] (n=14) | 100 [100-100] (n=14) |
| L10-14 | paper10_rot | 94 [85-100] (n=35) | 91 [62-100] (n=11) | 100 [100-100] (n=35) | 100 [100-100] (n=11) | 93 [81-100] (n=14) | 79 [53-100] (n=14) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 89 | 100 | 100 | 100 | 100 |
| L10-14 | paper10 | 87 [67-100] (n=31) | 89 [73-100] (n=9) | 90 [79-100] (n=31) | 89 [62-100] (n=9) | 93 [81-100] (n=29) | 83 [71-95] (n=29) |
| L10-14 | paper10_rot | 87 [67-100] (n=31) | 100 [100-100] (n=9) | 100 [100-100] (n=31) | 100 [100-100] (n=9) | 97 [88-100] (n=29) | 97 [90-100] (n=29) |


Keep-own-word kill test at L10-14 (memory-final words): P->M unedited 100 / paper10 92 / keep-own 97 (its control 98), M->M unedited 100 / paper10 95 / keep-own 95 (its control 100); restored 30% of the damage (>= 75% kills C1); control within 10: yes -> C1 survives

## Margin-matched gap under paper10 at L10-14 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.62, M->P 5.75, P->M 9.62, M->M 9.00. Loss (points) by quartile of that margin (cuts 5.12, 7.81, 10.38), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 27 (n=22) | 0 (n=18) | 0 (n=12) | 0 (n=14) |
| M->P | 30 (n=10) | 0 (n=2) | 0 (n=4) | 0 (n=4) |
| P->M | 50 (n=8) | 6 (n=18) | 0 (n=17) | 0 (n=23) |
| M->M | 20 (n=5) | 0 (n=4) | 0 (n=10) | 0 (n=1) |
| prompt-final, pooled | 28 (n=32) | 0 (n=20) | 0 (n=16) | 0 (n=18) |
| memory-final, pooled | 38 (n=13) | 5 (n=22) | 0 (n=27) | 0 (n=24) |

Memory-final minus prompt-final, items pooled per group: raw -3; reweighted to the prompt-final margins 5, to the memory-final margins 3; matched within 0.25-logit margin bins 5 [-1-16] (58 of 86 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L10-14: losses P->P 9, M->P 15, P->M 8, M->M 5, C->P 5, C->M 12; memory-final minus prompt-final -6 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 2d65551.
