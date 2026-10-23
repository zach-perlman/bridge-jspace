# C1 on tasks_v2 / olmoh7_natural_v1_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 98 | 99 |
| L4-8 | paper10 | 95 [91-99] (n=105) | 84 [76-91] (n=89) | 86 [78-92] (n=105) | 90 [81-97] (n=89) |
| L4-8 | paper10_rot | 94 [90-98] (n=105) | 91 [83-97] (n=89) | 94 [90-98] (n=105) | 97 [92-100] (n=89) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 98 | 99 |
| L4-8 | paper10 | 95 [91-99] (n=105) | 84 [76-91] (n=89) | 86 [78-92] (n=105) | 90 [81-97] (n=89) |
| L4-8 | paper10_rot | 94 [90-98] (n=105) | 91 [83-97] (n=89) | 94 [90-98] (n=105) | 97 [92-100] (n=89) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L4-8 | paper10 | - | - | - | - |
| L4-8 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L4-8 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 4.44, M->P 4.16, P->M 3.19, M->M 4.44. Loss (points) by quartile of that margin (cuts 2.19, 4.09, 5.77), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 14 (n=28) | 0 (n=21) | 0 (n=25) | 0 (n=31) |
| M->P | 45 (n=20) | 14 (n=21) | 6 (n=18) | 3 (n=30) |
| P->M | 31 (n=36) | 7 (n=29) | 0 (n=25) | 0 (n=15) |
| M->M | 43 (n=14) | 4 (n=26) | 3 (n=29) | 0 (n=20) |
| prompt-final, pooled | 27 (n=48) | 7 (n=42) | 2 (n=43) | 2 (n=61) |
| memory-final, pooled | 34 (n=50) | 5 (n=55) | 2 (n=54) | 0 (n=35) |

Memory-final minus prompt-final, items pooled per group: raw 2; reweighted to the prompt-final margins 1, to the memory-final margins 1; matched within 0.25-logit margin bins 2 [-6-8] (194 of 194 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L4-8: losses P->P 4, M->P 16, P->M 12, M->M 9; memory-final minus prompt-final 1 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit c34be5d.
