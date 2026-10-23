# C1 on tasks_v2 / fresh3_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 [100-100] (n=142) | 87 [77-95] (n=101) | 61 [46-74] (n=142) | 47 [29-64] (n=101) | 94 [90-98] (n=143) | 56 [43-69] (n=143) |
| L32-40 | paper10_rot | 100 [100-100] (n=142) | 98 [95-100] (n=101) | 99 [97-100] (n=142) | 100 [100-100] (n=101) | 100 [100-100] (n=143) | 95 [88-99] (n=143) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 [100-100] (n=86) | 90 [83-98] (n=51) | 60 [45-77] (n=86) | 53 [34-72] (n=51) | 96 [91-100] (n=74) | 50 [35-66] (n=74) |
| L32-40 | paper10_rot | 100 [100-100] (n=86) | 100 [100-100] (n=51) | 98 [94-100] (n=86) | 100 [100-100] (n=51) | 100 [100-100] (n=74) | 93 [83-100] (n=74) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 [100-100] (n=56) | 84 [69-96] (n=50) | 61 [42-77] (n=56) | 40 [21-61] (n=50) | 93 [85-98] (n=69) | 62 [47-78] (n=69) |
| L32-40 | paper10_rot | 100 [100-100] (n=56) | 96 [90-100] (n=50) | 100 [100-100] (n=56) | 100 [100-100] (n=50) | 100 [100-100] (n=69) | 97 [92-100] (n=69) |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.75, M->P 4.62, P->M 4.81, M->M 4.38. Loss (points) by quartile of that margin (cuts 4.00, 5.12, 5.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=9) | 0 (n=29) | 0 (n=47) | 0 (n=57) |
| M->P | 32 (n=34) | 7 (n=28) | 0 (n=25) | 0 (n=14) |
| P->M | 67 (n=45) | 49 (n=41) | 21 (n=24) | 3 (n=32) |
| M->M | 55 (n=38) | 50 (n=34) | 53 (n=17) | 58 (n=12) |
| prompt-final, pooled | 26 (n=43) | 4 (n=57) | 0 (n=72) | 0 (n=71) |
| memory-final, pooled | 61 (n=83) | 49 (n=75) | 34 (n=41) | 18 (n=44) |

Memory-final minus prompt-final, items pooled per group: raw 40; reweighted to the prompt-final margins 33, to the memory-final margins 35; matched within 0.25-logit margin bins 37 [30-46] (239 of 243 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 0, M->P 13, P->M 39, M->M 53, C->P 6, C->M 44; memory-final minus prompt-final 40 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 588a050.
