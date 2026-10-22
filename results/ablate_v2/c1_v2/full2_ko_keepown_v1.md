# C1 on tasks_v2 / full2_ko_keepown_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 [100-100] (n=152) | 87 [79-94] (n=101) | 57 [43-70] (n=152) | 53 [35-67] (n=101) | 96 [92-99] (n=144) | 58 [45-71] (n=144) |
| L32-40 | paper10_rot | 100 [100-100] (n=152) | 97 [93-100] (n=101) | 95 [91-99] (n=152) | 97 [92-100] (n=101) | 99 [98-100] (n=144) | 98 [95-100] (n=144) |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 [100-100] (n=84) | 84 [71-93] (n=57) | 57 [42-73] (n=84) | 53 [33-70] (n=57) | 100 [100-100] (n=68) | 59 [42-76] (n=68) |
| L32-40 | paper10_rot | 100 [100-100] (n=84) | 96 [91-100] (n=57) | 95 [88-100] (n=84) | 98 [94-100] (n=57) | 100 [100-100] (n=68) | 99 [95-100] (n=68) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L32-40 | paper10 | 100 [100-100] (n=68) | 91 [78-100] (n=44) | 56 [40-74] (n=68) | 55 [34-71] (n=44) | 92 [85-97] (n=76) | 57 [41-70] (n=76) |
| L32-40 | paper10_rot | 100 [100-100] (n=68) | 98 [92-100] (n=44) | 96 [91-100] (n=68) | 95 [84-100] (n=44) | 99 [95-100] (n=76) | 97 [93-100] (n=76) |


Keep-own-word kill test at L32-40 (memory-final words): P->M unedited 100 / paper10 57 / keep-own 64 (its control 96), M->M unedited 100 / paper10 53 / keep-own 63 (its control 100); restored 20% of the damage (>= 75% kills C1); control within 10: yes -> C1 survives

## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.75, M->P 4.38, P->M 4.62, M->M 4.50. Loss (points) by quartile of that margin (cuts 3.75, 5.00, 5.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 0 (n=6) | 0 (n=23) | 0 (n=56) | 0 (n=67) |
| M->P | 31 (n=36) | 8 (n=25) | 0 (n=29) | 0 (n=11) |
| P->M | 64 (n=50) | 47 (n=49) | 32 (n=22) | 13 (n=31) |
| M->M | 61 (n=36) | 42 (n=33) | 45 (n=20) | 17 (n=12) |
| prompt-final, pooled | 26 (n=42) | 4 (n=48) | 0 (n=85) | 0 (n=78) |
| memory-final, pooled | 63 (n=86) | 45 (n=82) | 38 (n=42) | 14 (n=43) |

Memory-final minus prompt-final, items pooled per group: raw 40; reweighted to the prompt-final margins 31, to the memory-final margins 34; matched within 0.25-logit margin bins 37 [30-44] (244 of 253 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L32-40: losses P->P 0, M->P 13, P->M 43, M->M 47, C->P 4, C->M 42; memory-final minus prompt-final 39 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 1249d90.
