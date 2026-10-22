# C1 on tasks_v2 / muse30j_full2_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 100 [100-100] (n=123) | 100 [100-100] (n=69) | 94 [89-98] (n=123) | 97 [92-100] (n=69) | 100 [100-100] (n=118) | 94 [89-98] (n=118) |
| L36-42 | paper10_rot | 100 [100-100] (n=123) | 100 [100-100] (n=69) | 95 [88-100] (n=123) | 99 [95-100] (n=69) | 100 [100-100] (n=118) | 97 [93-99] (n=118) |
| L26-32 | paper10 | 100 [100-100] (n=123) | 100 [100-100] (n=69) | 100 [100-100] (n=123) | 97 [92-100] (n=69) | 99 [97-100] (n=118) | 98 [95-100] (n=118) |
| L26-32 | paper10_rot | 100 [100-100] (n=123) | 100 [100-100] (n=69) | 99 [97-100] (n=123) | 99 [95-100] (n=69) | 99 [97-100] (n=118) | 99 [97-100] (n=118) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 100 [100-100] (n=64) | 100 [100-100] (n=39) | 94 [85-100] (n=64) | 95 [86-100] (n=39) | 100 [100-100] (n=55) | 91 [80-98] (n=55) |
| L36-42 | paper10_rot | 100 [100-100] (n=64) | 100 [100-100] (n=39) | 95 [89-100] (n=64) | 100 [100-100] (n=39) | 100 [100-100] (n=55) | 95 [88-100] (n=55) |
| L26-32 | paper10 | 100 [100-100] (n=64) | 100 [100-100] (n=39) | 100 [100-100] (n=64) | 100 [100-100] (n=39) | 100 [100-100] (n=55) | 96 [90-100] (n=55) |
| L26-32 | paper10_rot | 100 [100-100] (n=64) | 100 [100-100] (n=39) | 98 [94-100] (n=64) | 100 [100-100] (n=39) | 100 [100-100] (n=55) | 98 [93-100] (n=55) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 100 [100-100] (n=59) | 100 [100-100] (n=30) | 95 [89-100] (n=59) | 100 [100-100] (n=30) | 100 [100-100] (n=63) | 97 [92-100] (n=63) |
| L36-42 | paper10_rot | 100 [100-100] (n=59) | 100 [100-100] (n=30) | 95 [87-100] (n=59) | 97 [88-100] (n=30) | 100 [100-100] (n=63) | 98 [95-100] (n=63) |
| L26-32 | paper10 | 100 [100-100] (n=59) | 100 [100-100] (n=30) | 100 [100-100] (n=59) | 93 [82-100] (n=30) | 98 [95-100] (n=63) | 100 [100-100] (n=63) |
| L26-32 | paper10_rot | 100 [100-100] (n=59) | 100 [100-100] (n=30) | 100 [100-100] (n=59) | 97 [89-100] (n=30) | 98 [95-100] (n=63) | 100 [100-100] (n=63) |


## Margin-matched gap under paper10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.25, M->P 4.00, P->M 4.38, M->M 4.56. Loss (points) by quartile of that margin (cuts 3.44, 4.62, 5.62), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=16) | 0 (n=26) | 0 (n=41) | 0 (n=40) |
| M->P | 0 (n=29) | 0 (n=14) | 0 (n=13) | 0 (n=13) |
| P->M | 18 (n=38) | 0 (n=35) | 0 (n=22) | 0 (n=28) |
| M->M | 13 (n=15) | 0 (n=22) | 0 (n=20) | 0 (n=12) |
| prompt-final, pooled | 0 (n=45) | 0 (n=40) | 0 (n=54) | 0 (n=53) |
| memory-final, pooled | 17 (n=53) | 0 (n=57) | 0 (n=42) | 0 (n=40) |

Memory-final minus prompt-final, items pooled per group: raw 5; reweighted to the prompt-final margins 4, to the memory-final margins 5; matched within 0.25-logit margin bins 5 [2-8] (187 of 192 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L36-42: losses P->P 0, M->P 0, P->M 6, M->M 3, C->P 0, C->M 6; memory-final minus prompt-final 4 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): holds. Output from commit b4cce0a.
