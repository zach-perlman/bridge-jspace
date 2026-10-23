# C1 on tasks_v2 / olmoh7_big2_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 98 | 100 | 100 |
| L4-8 | paper10 | 95 [91-97] (n=256) | 84 [76-92] (n=90) | 93 [88-96] (n=256) | 87 [78-94] (n=90) |
| L4-8 | paper10_rot | 97 [95-99] (n=256) | 93 [87-98] (n=90) | 98 [97-100] (n=256) | 94 [88-99] (n=90) |
| L12-16 | paper10 | 98 [97-100] (n=256) | 94 [88-98] (n=90) | 96 [93-99] (n=256) | 93 [86-98] (n=90) |
| L12-16 | paper10_rot | 98 [97-100] (n=256) | 97 [92-100] (n=90) | 98 [97-100] (n=256) | 97 [92-100] (n=90) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L4-8 | paper10 | 94 [89-98] (n=133) | 88 [75-97] (n=33) | 92 [86-97] (n=133) | 91 [79-100] (n=33) |
| L4-8 | paper10_rot | 98 [95-100] (n=133) | 91 [78-100] (n=33) | 100 [100-100] (n=133) | 94 [83-100] (n=33) |
| L12-16 | paper10 | 98 [96-100] (n=133) | 97 [89-100] (n=33) | 97 [94-100] (n=133) | 94 [84-100] (n=33) |
| L12-16 | paper10_rot | 98 [95-100] (n=133) | 97 [89-100] (n=33) | 98 [96-100] (n=133) | 97 [90-100] (n=33) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 96 | 100 | 100 |
| L4-8 | paper10 | 95 [91-98] (n=123) | 82 [71-91] (n=57) | 93 [87-97] (n=123) | 84 [73-93] (n=57) |
| L4-8 | paper10_rot | 96 [93-99] (n=123) | 95 [88-100] (n=57) | 97 [93-99] (n=123) | 95 [89-100] (n=57) |
| L12-16 | paper10 | 98 [96-100] (n=123) | 93 [85-98] (n=57) | 94 [90-98] (n=123) | 93 [86-98] (n=57) |
| L12-16 | paper10_rot | 99 [98-100] (n=123) | 96 [91-100] (n=57) | 98 [96-100] (n=123) | 96 [91-100] (n=57) |


## Margin-matched gap under paper10 at L4-8 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.27, M->P 2.68, P->M 5.52, M->M 4.35. Loss (points) by quartile of that margin (cuts 2.83, 5.30, 7.65), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 21 (n=47) | 4 (n=57) | 0 (n=71) | 0 (n=81) |
| M->P | 22 (n=46) | 5 (n=21) | 7 (n=14) | 0 (n=9) |
| P->M | 27 (n=52) | 4 (n=70) | 3 (n=70) | 0 (n=64) |
| M->M | 38 (n=29) | 4 (n=25) | 0 (n=18) | 0 (n=18) |
| prompt-final, pooled | 22 (n=93) | 4 (n=78) | 1 (n=85) | 0 (n=90) |
| memory-final, pooled | 31 (n=81) | 4 (n=95) | 2 (n=88) | 0 (n=82) |

Memory-final minus prompt-final, items pooled per group: raw 2; reweighted to the prompt-final margins 3, to the memory-final margins 3; matched within 0.25-logit margin bins 2 [-2-7] (337 of 346 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L4-8: losses P->P 5, M->P 13, P->M 7, M->M 13; memory-final minus prompt-final 1 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit c18c70a.
