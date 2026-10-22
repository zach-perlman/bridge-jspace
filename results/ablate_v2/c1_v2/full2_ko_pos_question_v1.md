# C1 on tasks_v2 / full2_ko_pos_question_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 56 [46-64] (n=152) | 95 [90-99] (n=101) | 52 [42-61] (n=152) | 94 [86-99] (n=101) | 70 [60-80] (n=144) | 66 [54-76] (n=144) |
| L12-20 | paper10_rot | 100 [100-100] (n=152) | 99 [97-100] (n=101) | 100 [100-100] (n=152) | 97 [93-100] (n=101) | 100 [100-100] (n=144) | 100 [100-100] (n=144) |
| L32-40 | paper10 | 100 [100-100] (n=152) | 87 [80-94] (n=101) | 89 [82-95] (n=152) | 62 [44-77] (n=101) | 97 [94-99] (n=144) | 85 [79-91] (n=144) |
| L32-40 | paper10_rot | 100 [100-100] (n=152) | 96 [92-99] (n=101) | 99 [97-100] (n=152) | 96 [90-100] (n=101) | 100 [100-100] (n=144) | 99 [98-100] (n=144) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 61 [48-71] (n=84) | 96 [89-100] (n=57) | 63 [53-73] (n=84) | 93 [83-100] (n=57) | 69 [55-83] (n=68) | 68 [56-80] (n=68) |
| L12-20 | paper10_rot | 100 [100-100] (n=84) | 100 [100-100] (n=57) | 100 [100-100] (n=84) | 96 [90-100] (n=57) | 100 [100-100] (n=68) | 100 [100-100] (n=68) |
| L32-40 | paper10 | 100 [100-100] (n=84) | 82 [69-93] (n=57) | 88 [79-96] (n=84) | 67 [46-82] (n=57) | 100 [100-100] (n=68) | 85 [77-92] (n=68) |
| L32-40 | paper10_rot | 100 [100-100] (n=84) | 96 [91-100] (n=57) | 99 [96-100] (n=84) | 98 [94-100] (n=57) | 100 [100-100] (n=68) | 99 [95-100] (n=68) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 50 [37-61] (n=68) | 93 [84-100] (n=44) | 38 [26-51] (n=68) | 95 [88-100] (n=44) | 71 [60-81] (n=76) | 64 [51-78] (n=76) |
| L12-20 | paper10_rot | 100 [100-100] (n=68) | 98 [92-100] (n=44) | 100 [100-100] (n=68) | 98 [92-100] (n=44) | 100 [100-100] (n=76) | 100 [100-100] (n=76) |
| L32-40 | paper10 | 100 [100-100] (n=68) | 93 [82-100] (n=44) | 91 [82-98] (n=68) | 57 [35-74] (n=44) | 95 [89-99] (n=76) | 86 [76-93] (n=76) |
| L32-40 | paper10_rot | 100 [100-100] (n=68) | 95 [88-100] (n=44) | 99 [96-100] (n=68) | 93 [81-100] (n=44) | 100 [100-100] (n=76) | 100 [100-100] (n=76) |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.75, M->P 4.38, P->M 4.62, M->M 4.50. Loss (points) by quartile of that margin (cuts 3.75, 5.00, 5.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=6) | 0 (n=23) | 0 (n=56) | 0 (n=67) |
| M->P | 31 (n=36) | 8 (n=25) | 0 (n=29) | 0 (n=11) |
| P->M | 14 (n=50) | 14 (n=49) | 9 (n=22) | 0 (n=31) |
| M->M | 58 (n=36) | 27 (n=33) | 35 (n=20) | 8 (n=12) |
| prompt-final, pooled | 26 (n=42) | 4 (n=48) | 0 (n=85) | 0 (n=78) |
| memory-final, pooled | 33 (n=86) | 20 (n=82) | 21 (n=42) | 2 (n=43) |

Memory-final minus prompt-final, items pooled per group: raw 16; reweighted to the prompt-final margins 12, to the memory-final margins 11; matched within 0.25-logit margin bins 13 [7-20] (244 of 253 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 0, M->P 13, P->M 11, M->M 38, C->P 3, C->M 15; memory-final minus prompt-final 18 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 1249d90.
