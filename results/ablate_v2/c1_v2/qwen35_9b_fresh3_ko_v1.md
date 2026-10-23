# C1 on tasks_v2 / qwen35_9b_fresh3_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 99 | 100 | 100 | 100 |
| L12-16 | paper10 | 95 [91-99] (n=111) | 98 [93-100] (n=52) | 70 [56-83] (n=111) | 62 [43-79] (n=52) | 97 [94-100] (n=104) | 63 [51-74] (n=104) |
| L12-16 | paper10_rot | 93 [88-97] (n=111) | 96 [91-100] (n=52) | 96 [93-99] (n=111) | 98 [93-100] (n=52) | 95 [91-99] (n=104) | 91 [85-97] (n=104) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 99 [96-100] (n=70) | 100 [100-100] (n=25) | 69 [53-82] (n=70) | 52 [30-76] (n=25) | 96 [89-100] (n=51) | 57 [42-73] (n=51) |
| L12-16 | paper10_rot | 96 [91-100] (n=70) | 92 [79-100] (n=25) | 94 [88-99] (n=70) | 96 [86-100] (n=25) | 94 [88-100] (n=51) | 86 [74-96] (n=51) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 98 | 100 | 98 | 100 | 100 | 100 |
| L12-16 | paper10 | 90 [81-98] (n=41) | 96 [86-100] (n=27) | 73 [52-91] (n=41) | 70 [48-88] (n=27) | 98 [95-100] (n=53) | 70 [58-80] (n=53) |
| L12-16 | paper10_rot | 88 [77-97] (n=41) | 100 [100-100] (n=27) | 100 [100-100] (n=41) | 100 [100-100] (n=27) | 96 [90-100] (n=53) | 96 [91-100] (n=53) |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.88, M->P 2.44, P->M 2.75, M->M 2.94. Loss (points) by quartile of that margin (cuts 1.75, 2.88, 3.62), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 17 (n=24) | 0 (n=33) | 0 (n=25) | 0 (n=29) |
| M->P | 5 (n=19) | 0 (n=12) | 0 (n=12) | 0 (n=9) |
| P->M | 73 (n=30) | 21 (n=34) | 14 (n=22) | 0 (n=25) |
| M->M | 75 (n=12) | 36 (n=14) | 13 (n=15) | 36 (n=11) |
| prompt-final, pooled | 12 (n=43) | 0 (n=45) | 0 (n=37) | 0 (n=38) |
| memory-final, pooled | 74 (n=42) | 25 (n=48) | 14 (n=37) | 11 (n=36) |

Memory-final minus prompt-final, items pooled per group: raw 29; reweighted to the prompt-final margins 29, to the memory-final margins 29; matched within 0.25-logit margin bins 30 [22-38] (162 of 163 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 4, M->P 2, P->M 29, M->M 38, C->P 3, C->M 37; memory-final minus prompt-final 31 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit f3b1b41.
