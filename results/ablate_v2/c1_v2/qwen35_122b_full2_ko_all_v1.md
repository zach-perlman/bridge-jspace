# C1 on tasks_v2 / qwen35_122b_full2_ko_all_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 99 | 99 | 99 | 100 | 99 | 99 |
| L0-46 | paper10 | 90 [83-95] (n=143) | 80 [68-90] (n=100) | 63 [51-73] (n=143) | 58 [48-68] (n=100) | 86 [80-93] (n=136) | 51 [40-61] (n=136) |
| L0-46 | paper10_rot | 93 [89-97] (n=143) | 75 [63-86] (n=100) | 66 [55-76] (n=143) | 85 [74-94] (n=100) | 89 [83-95] (n=136) | 60 [48-72] (n=136) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 98 | 99 | 100 | 98 | 100 |
| L0-46 | paper10 | 89 [82-96] (n=76) | 74 [56-88] (n=58) | 61 [48-73] (n=76) | 62 [48-79] (n=58) | 82 [68-92] (n=65) | 45 [30-58] (n=65) |
| L0-46 | paper10_rot | 92 [86-97] (n=76) | 74 [57-89] (n=58) | 70 [57-82] (n=76) | 90 [80-97] (n=58) | 86 [76-96] (n=65) | 63 [47-76] (n=65) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 | 100 | 99 |
| L0-46 | paper10 | 90 [80-97] (n=67) | 88 [78-97] (n=42) | 66 [49-79] (n=67) | 52 [37-67] (n=42) | 90 [84-96] (n=71) | 56 [42-69] (n=71) |
| L0-46 | paper10_rot | 94 [89-99] (n=67) | 76 [61-91] (n=42) | 63 [46-76] (n=67) | 79 [62-93] (n=42) | 92 [86-97] (n=71) | 56 [44-69] (n=71) |


## Margin-matched gap under paper10 at L0-46 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 4.88, M->P 4.31, P->M 3.88, M->M 4.06. Loss (points) by quartile of that margin (cuts 3.50, 4.38, 5.00), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 7 (n=14) | 16 (n=25) | 6 (n=49) | 11 (n=55) |
| M->P | 46 (n=24) | 17 (n=29) | 4 (n=24) | 9 (n=23) |
| P->M | 64 (n=56) | 25 (n=44) | 13 (n=23) | 10 (n=20) |
| M->M | 42 (n=31) | 46 (n=35) | 56 (n=16) | 22 (n=18) |
| prompt-final, pooled | 32 (n=38) | 17 (n=54) | 5 (n=73) | 10 (n=78) |
| memory-final, pooled | 56 (n=87) | 34 (n=79) | 31 (n=39) | 16 (n=38) |

Memory-final minus prompt-final, items pooled per group: raw 25; reweighted to the prompt-final margins 17, to the memory-final margins 19; matched within 0.25-logit margin bins 19 [10-29] (234 of 243 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L0-46: losses P->P 10, M->P 19, P->M 36, M->M 42, C->P 13, C->M 49; memory-final minus prompt-final 25 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit da2afb2.
