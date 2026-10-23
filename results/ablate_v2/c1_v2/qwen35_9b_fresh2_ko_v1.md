# C1 on tasks_v2 / qwen35_9b_fresh2_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 99 |
| L12-16 | paper10 | 97 [94-100] (n=116) | 92 [83-100] (n=37) | 71 [60-81] (n=116) | 73 [58-87] (n=37) | 97 [93-100] (n=102) | 69 [57-79] (n=102) |
| L12-16 | paper10_rot | 97 [94-100] (n=116) | 97 [90-100] (n=37) | 94 [89-99] (n=116) | 100 [100-100] (n=37) | 98 [95-100] (n=102) | 99 [97-100] (n=102) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 98 |
| L12-16 | paper10 | 98 [96-100] (n=64) | 100 [100-100] (n=21) | 70 [56-85] (n=64) | 76 [58-95] (n=21) | 98 [93-100] (n=45) | 69 [54-82] (n=45) |
| L12-16 | paper10_rot | 95 [89-100] (n=64) | 100 [100-100] (n=21) | 92 [85-98] (n=64) | 100 [100-100] (n=21) | 100 [100-100] (n=45) | 98 [92-100] (n=45) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-16 | paper10 | 96 [90-100] (n=52) | 81 [62-100] (n=16) | 71 [57-84] (n=52) | 69 [42-88] (n=16) | 96 [91-100] (n=57) | 68 [55-81] (n=57) |
| L12-16 | paper10_rot | 100 [100-100] (n=52) | 94 [77-100] (n=16) | 96 [91-100] (n=52) | 100 [100-100] (n=16) | 96 [92-100] (n=57) | 100 [100-100] (n=57) |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.75, M->P 2.12, P->M 3.00, M->M 2.38. Loss (points) by quartile of that margin (cuts 1.75, 2.75, 3.50), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 8 (n=25) | 0 (n=35) | 4 (n=27) | 0 (n=29) |
| M->P | 23 (n=13) | 0 (n=10) | 0 (n=10) | 0 (n=4) |
| P->M | 68 (n=28) | 36 (n=28) | 19 (n=27) | 0 (n=33) |
| M->M | 31 (n=13) | 25 (n=12) | 29 (n=7) | 20 (n=5) |
| prompt-final, pooled | 13 (n=38) | 0 (n=45) | 3 (n=37) | 0 (n=33) |
| memory-final, pooled | 56 (n=41) | 32 (n=40) | 21 (n=34) | 3 (n=38) |

Memory-final minus prompt-final, items pooled per group: raw 25; reweighted to the prompt-final margins 25, to the memory-final margins 25; matched within 0.25-logit margin bins 26 [20-34] (151 of 153 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 3, M->P 8, P->M 29, M->M 27, C->P 3, C->M 30; memory-final minus prompt-final 23 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): holds. Output from commit b15a1e7.
