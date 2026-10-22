# C1 on tasks_v2 / full2_ko_pos_context_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 30 [22-37] (n=152) | 83 [76-90] (n=101) | 28 [17-38] (n=152) | 99 [97-100] (n=101) | 72 [62-80] (n=144) | 76 [68-83] (n=144) |
| L12-20 | paper10_rot | 100 [100-100] (n=152) | 96 [92-99] (n=101) | 97 [93-99] (n=152) | 98 [94-100] (n=101) | 100 [100-100] (n=144) | 98 [95-100] (n=144) |
| L32-40 | paper10 | 100 [100-100] (n=152) | 95 [91-99] (n=101) | 89 [81-95] (n=152) | 100 [100-100] (n=101) | 99 [98-100] (n=144) | 89 [82-94] (n=144) |
| L32-40 | paper10_rot | 100 [100-100] (n=152) | 99 [97-100] (n=101) | 99 [97-100] (n=152) | 100 [100-100] (n=101) | 100 [100-100] (n=144) | 99 [96-100] (n=144) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 29 [18-38] (n=84) | 86 [78-93] (n=57) | 27 [16-40] (n=84) | 100 [100-100] (n=57) | 68 [55-80] (n=68) | 76 [65-86] (n=68) |
| L12-20 | paper10_rot | 100 [100-100] (n=84) | 95 [88-100] (n=57) | 95 [90-99] (n=84) | 98 [94-100] (n=57) | 100 [100-100] (n=68) | 99 [95-100] (n=68) |
| L32-40 | paper10 | 100 [100-100] (n=84) | 93 [84-98] (n=57) | 87 [76-96] (n=84) | 100 [100-100] (n=57) | 100 [100-100] (n=68) | 93 [85-98] (n=68) |
| L32-40 | paper10_rot | 100 [100-100] (n=84) | 98 [94-100] (n=57) | 100 [100-100] (n=84) | 100 [100-100] (n=57) | 100 [100-100] (n=68) | 100 [100-100] (n=68) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L12-20 | paper10 | 31 [21-40] (n=68) | 80 [65-92] (n=44) | 28 [14-41] (n=68) | 98 [92-100] (n=44) | 75 [66-83] (n=76) | 75 [64-86] (n=76) |
| L12-20 | paper10_rot | 100 [100-100] (n=68) | 98 [92-100] (n=44) | 99 [95-100] (n=68) | 98 [93-100] (n=44) | 100 [100-100] (n=76) | 97 [93-100] (n=76) |
| L32-40 | paper10 | 100 [100-100] (n=68) | 98 [93-100] (n=44) | 91 [84-97] (n=68) | 100 [100-100] (n=44) | 99 [95-100] (n=76) | 86 [75-94] (n=76) |
| L32-40 | paper10_rot | 100 [100-100] (n=68) | 100 [100-100] (n=44) | 97 [94-100] (n=68) | 100 [100-100] (n=44) | 100 [100-100] (n=76) | 97 [92-100] (n=76) |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.75, M->P 4.38, P->M 4.62, M->M 4.50. Loss (points) by quartile of that margin (cuts 3.75, 5.00, 5.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=6) | 0 (n=23) | 0 (n=56) | 0 (n=67) |
| M->P | 14 (n=36) | 0 (n=25) | 0 (n=29) | 0 (n=11) |
| P->M | 22 (n=50) | 10 (n=49) | 5 (n=22) | 0 (n=31) |
| M->M | 0 (n=36) | 0 (n=33) | 0 (n=20) | 0 (n=12) |
| prompt-final, pooled | 12 (n=42) | 0 (n=48) | 0 (n=85) | 0 (n=78) |
| memory-final, pooled | 13 (n=86) | 6 (n=82) | 2 (n=42) | 0 (n=43) |

Memory-final minus prompt-final, items pooled per group: raw 5; reweighted to the prompt-final margins 2, to the memory-final margins 3; matched within 0.25-logit margin bins 4 [0-8] (244 of 253 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 0, M->P 5, P->M 11, M->M 0, C->P 1, C->M 11; memory-final minus prompt-final 3 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 1249d90.
