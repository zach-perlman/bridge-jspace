# C1 on tasks_v2 / qwen35_9b_natural_v1_chat_ko_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L12-16 | paper10 | 86 [80-92] (n=175) | 92 [88-96] (n=181) | 45 [36-54] (n=175) | 61 [50-70] (n=181) |
| L12-16 | paper10_rot | 89 [84-94] (n=175) | 95 [91-98] (n=181) | 98 [96-100] (n=175) | 99 [98-100] (n=181) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L12-16 | paper10 | 86 [80-92] (n=175) | 92 [88-96] (n=181) | 45 [36-54] (n=175) | 61 [50-70] (n=181) |
| L12-16 | paper10_rot | 89 [84-94] (n=175) | 95 [91-98] (n=181) | 98 [96-100] (n=175) | 99 [98-100] (n=181) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L12-16 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.12, M->P 3.12, P->M 4.00, M->M 5.38. Loss (points) by quartile of that margin (cuts 2.25, 4.12, 5.88), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 26 (n=69) | 11 (n=37) | 0 (n=41) | 4 (n=28) |
| M->P | 16 (n=63) | 4 (n=52) | 8 (n=26) | 0 (n=40) |
| P->M | 79 (n=42) | 62 (n=52) | 39 (n=49) | 41 (n=32) |
| M->M | 73 (n=11) | 55 (n=38) | 26 (n=65) | 37 (n=67) |
| prompt-final, pooled | 21 (n=132) | 7 (n=89) | 3 (n=67) | 1 (n=68) |
| memory-final, pooled | 77 (n=53) | 59 (n=90) | 32 (n=114) | 38 (n=99) |

Memory-final minus prompt-final, items pooled per group: raw 37; reweighted to the prompt-final margins 46, to the memory-final margins 41; matched within 0.25-logit margin bins 41 [35-47] (353 of 356 memory-final items have a same-bin partner) points.

Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses P->P 13, M->P 8, P->M 55, M->M 39; memory-final minus prompt-final 37 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 3bc4e9e.
