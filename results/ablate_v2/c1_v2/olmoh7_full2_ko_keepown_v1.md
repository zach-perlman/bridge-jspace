# C1 on tasks_v2 / olmoh7_full2_ko_keepown_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 96 | 100 | 100 | 100 | 100 |
| L4-8 | paper10 | 96 [90-99] (n=70) | 79 [62-93] (n=24) | 90 [84-96] (n=70) | 75 [54-95] (n=24) | 96 [89-100] (n=51) | 90 [82-98] (n=51) |
| L4-8 | paper10_rot | 97 [92-100] (n=70) | 88 [71-100] (n=24) | 100 [100-100] (n=70) | 96 [88-100] (n=24) | 100 [100-100] (n=51) | 88 [79-96] (n=51) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L4-8 | paper10 | 95 [88-100] (n=39) | 80 [50-100] (n=10) | 87 [77-97] (n=39) | 80 [50-100] (n=10) | 96 [86-100] (n=25) | 88 [74-100] (n=25) |
| L4-8 | paper10_rot | 100 [100-100] (n=39) | 90 [70-100] (n=10) | 100 [100-100] (n=39) | 100 [100-100] (n=10) | 100 [100-100] (n=25) | 88 [75-100] (n=25) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 93 | 100 | 100 | 100 | 100 |
| L4-8 | paper10 | 97 [88-100] (n=31) | 79 [57-100] (n=14) | 94 [86-100] (n=31) | 71 [50-93] (n=14) | 96 [86-100] (n=26) | 92 [81-100] (n=26) |
| L4-8 | paper10_rot | 94 [81-100] (n=31) | 86 [64-100] (n=14) | 100 [100-100] (n=31) | 93 [80-100] (n=14) | 100 [100-100] (n=26) | 88 [74-100] (n=26) |


Keep-own-word kill test at L4-8 (memory-final words): P->M unedited 100 / paper10 90 / keep-own 97 (its control 96), M->M unedited 100 / paper10 75 / keep-own 92 (its control 100); restored 69% of the damage (>= 75% kills C1); control within 10: yes -> C1 survives

## Margin-matched gap under paper10 at L4-8 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.42, M->P 4.00, P->M 5.54, M->M 6.08. Loss (points) by quartile of that margin (cuts 3.40, 5.60, 8.05), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 15 (n=13) | 6 (n=18) | 0 (n=27) | 0 (n=12) |
| M->P | 22 (n=9) | 29 (n=7) | 0 (n=3) | 0 (n=5) |
| P->M | 33 (n=18) | 5 (n=19) | 0 (n=15) | 0 (n=18) |
| M->M | 75 (n=8) | 0 (n=3) | 0 (n=2) | 0 (n=11) |
| prompt-final, pooled | 18 (n=22) | 12 (n=25) | 0 (n=30) | 0 (n=17) |
| memory-final, pooled | 46 (n=26) | 5 (n=22) | 0 (n=17) | 0 (n=29) |

Memory-final minus prompt-final, items pooled per group: raw 6; reweighted to the prompt-final margins 5, to the memory-final margins 6; matched within 0.25-logit margin bins -5 [-18-10] (71 of 94 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L4-8: losses P->P 4, M->P 17, P->M 10, M->M 25, C->P 4, C->M 10; memory-final minus prompt-final 7 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit cf1a709.
