# C1 on tasks_v2 / fresh2_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 [100-100] (n=152) | 87 [79-94] (n=92) | 64 [50-77] (n=152) | 54 [36-68] (n=92) | 95 [90-99] (n=143) | 62 [49-74] (n=143) |
| L32-40 | paper10_rot | 99 [98-100] (n=152) | 96 [92-99] (n=92) | 94 [88-99] (n=152) | 97 [90-100] (n=92) | 99 [98-100] (n=143) | 98 [95-100] (n=143) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 [100-100] (n=80) | 85 [76-94] (n=48) | 68 [54-81] (n=80) | 56 [35-74] (n=48) | 91 [84-98] (n=68) | 60 [45-74] (n=68) |
| L32-40 | paper10_rot | 100 [100-100] (n=80) | 96 [89-100] (n=48) | 95 [88-100] (n=80) | 98 [92-100] (n=48) | 100 [100-100] (n=68) | 97 [92-100] (n=68) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 [100-100] (n=72) | 89 [76-98] (n=44) | 61 [46-77] (n=72) | 52 [32-72] (n=44) | 99 [96-100] (n=75) | 63 [50-77] (n=75) |
| L32-40 | paper10_rot | 99 [95-100] (n=72) | 95 [88-100] (n=44) | 93 [86-99] (n=72) | 95 [85-100] (n=44) | 99 [96-100] (n=75) | 99 [96-100] (n=75) |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.81, M->P 4.69, P->M 4.69, M->M 4.62. Loss (points) by quartile of that margin (cuts 4.00, 5.12, 5.94), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=17) | 0 (n=22) | 0 (n=51) | 0 (n=62) |
| M->P | 34 (n=35) | 0 (n=22) | 0 (n=28) | 0 (n=7) |
| P->M | 60 (n=43) | 40 (n=48) | 16 (n=25) | 14 (n=36) |
| M->M | 50 (n=30) | 38 (n=34) | 65 (n=17) | 27 (n=11) |
| prompt-final, pooled | 23 (n=52) | 0 (n=44) | 0 (n=79) | 0 (n=69) |
| memory-final, pooled | 56 (n=73) | 39 (n=82) | 36 (n=42) | 17 (n=47) |

Memory-final minus prompt-final, items pooled per group: raw 34; reweighted to the prompt-final margins 30, to the memory-final margins 32; matched within 0.25-logit margin bins 33 [25-40] (241 of 244 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 0, M->P 13, P->M 36, M->M 46, C->P 5, C->M 38; memory-final minus prompt-final 34 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit d0fdb05.
