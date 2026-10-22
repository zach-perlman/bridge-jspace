# C1 on tasks_v2 / qwen3_32b_full2_ko_keepown_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 98 | 100 | 100 | 100 | 100 |
| L44-52 | paper10 | 99 [97-100] (n=123) | 98 [95-100] (n=61) | 77 [63-87] (n=123) | 79 [61-91] (n=61) | 93 [88-97] (n=108) | 71 [59-80] (n=108) |
| L44-52 | paper10_rot | 99 [97-100] (n=123) | 95 [90-100] (n=61) | 94 [90-98] (n=123) | 98 [95-100] (n=61) | 99 [97-100] (n=108) | 87 [77-94] (n=108) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L44-52 | paper10 | 100 [100-100] (n=67) | 97 [92-100] (n=33) | 73 [59-85] (n=67) | 73 [50-91] (n=33) | 92 [82-100] (n=49) | 71 [54-83] (n=49) |
| L44-52 | paper10_rot | 100 [100-100] (n=67) | 97 [91-100] (n=33) | 94 [86-99] (n=67) | 97 [90-100] (n=33) | 98 [93-100] (n=49) | 82 [67-93] (n=49) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 96 | 100 | 100 | 100 | 100 |
| L44-52 | paper10 | 98 [94-100] (n=56) | 100 [100-100] (n=28) | 82 [65-93] (n=56) | 86 [71-97] (n=28) | 93 [87-98] (n=59) | 71 [55-84] (n=59) |
| L44-52 | paper10_rot | 98 [94-100] (n=56) | 93 [82-100] (n=28) | 95 [86-100] (n=56) | 100 [100-100] (n=28) | 100 [100-100] (n=59) | 92 [83-98] (n=59) |


Keep-own-word kill test at L44-52 (memory-final words): P->M unedited 100 / paper10 77 / keep-own 80 (its control 93), M->M unedited 100 / paper10 79 / keep-own 72 (its control 97); restored -10% of the damage (>= 75% kills C1); control within 10: yes -> C1 survives

## Margin-matched gap under paper10 at L44-52 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 10.75, M->P 7.00, P->M 7.38, M->M 7.62. Loss (points) by quartile of that margin (cuts 6.38, 8.50, 10.38), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 33 (n=3) | 0 (n=17) | 0 (n=30) | 0 (n=73) |
| M->P | 0 (n=30) | 0 (n=11) | 0 (n=10) | 0 (n=10) |
| P->M | 46 (n=39) | 16 (n=50) | 3 (n=29) | 20 (n=5) |
| M->M | 42 (n=24) | 11 (n=18) | 6 (n=18) | 0 (n=1) |
| prompt-final, pooled | 3 (n=33) | 0 (n=28) | 0 (n=40) | 0 (n=83) |
| memory-final, pooled | 44 (n=63) | 15 (n=68) | 4 (n=47) | 17 (n=6) |

Memory-final minus prompt-final, items pooled per group: raw 22; reweighted to the prompt-final margins 18, to the memory-final margins 21; matched within 0.25-logit margin bins 18 [10-23] (162 of 184 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L44-52: losses P->P 1, M->P 0, P->M 23, M->M 21, C->P 7, C->M 29; memory-final minus prompt-final 22 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit ab86c4e.
