# C1 on tasks_v2 / muse30_natplus_v1_chat_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 97 [95-99] (n=281) | 98 [96-100] (n=211) | 30 [24-37] (n=281) | 38 [30-46] (n=211) |
| L36-42 | paper10_rot | 97 [95-99] (n=281) | 97 [94-99] (n=211) | 98 [96-99] (n=281) | 98 [95-100] (n=211) |
| L36-42 | unembed10 | 95 [92-98] (n=281) | 98 [95-99] (n=211) | 49 [41-57] (n=281) | 65 [57-73] (n=211) |
| L36-42 | unembed10_rot | 96 [94-98] (n=281) | 96 [94-99] (n=211) | 98 [96-100] (n=281) | 99 [98-100] (n=211) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 97 [95-99] (n=281) | 98 [96-100] (n=211) | 30 [24-37] (n=281) | 38 [30-46] (n=211) |
| L36-42 | paper10_rot | 97 [95-99] (n=281) | 97 [94-99] (n=211) | 98 [96-99] (n=281) | 98 [95-100] (n=211) |
| L36-42 | unembed10 | 95 [92-98] (n=281) | 98 [95-99] (n=211) | 49 [41-57] (n=281) | 65 [57-73] (n=211) |
| L36-42 | unembed10_rot | 96 [94-98] (n=281) | 96 [94-99] (n=211) | 98 [96-100] (n=281) | 99 [98-100] (n=211) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - |
| L36-42 | unembed10 | - | - | - | - |
| L36-42 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.62, M->P 1.56, P->M 1.88, M->M 2.25. Loss (points) by quartile of that margin (cuts 1.00, 1.81, 2.50), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 7 (n=97) | 1 (n=71) | 0 (n=74) | 0 (n=39) |
| M->P | 6 (n=68) | 0 (n=57) | 0 (n=42) | 0 (n=44) |
| P->M | 90 (n=60) | 71 (n=78) | 60 (n=83) | 60 (n=60) |
| M->M | 84 (n=37) | 61 (n=36) | 64 (n=59) | 51 (n=79) |
| prompt-final, pooled | 7 (n=165) | 1 (n=128) | 0 (n=116) | 0 (n=83) |
| memory-final, pooled | 88 (n=97) | 68 (n=114) | 62 (n=142) | 55 (n=139) |

Memory-final minus prompt-final, items pooled per group: raw 64; reweighted to the prompt-final margins 68, to the memory-final margins 65; matched within 0.25-logit margin bins 65 [60-69] (489 of 492 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.62, M->P 1.56, P->M 1.88, M->M 2.25. Loss (points) by quartile of that margin (cuts 1.00, 1.81, 2.50), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 13 (n=97) | 0 (n=71) | 0 (n=74) | 0 (n=39) |
| M->P | 6 (n=68) | 2 (n=57) | 0 (n=42) | 0 (n=44) |
| P->M | 75 (n=60) | 58 (n=78) | 41 (n=83) | 30 (n=60) |
| M->M | 59 (n=37) | 50 (n=36) | 34 (n=59) | 16 (n=79) |
| prompt-final, pooled | 10 (n=165) | 1 (n=128) | 0 (n=116) | 0 (n=83) |
| memory-final, pooled | 69 (n=97) | 55 (n=114) | 38 (n=142) | 22 (n=139) |

Memory-final minus prompt-final, items pooled per group: raw 40; reweighted to the prompt-final margins 47, to the memory-final margins 41; matched within 0.25-logit margin bins 41 [36-45] (489 of 492 memory-final items have a same-bin partner) points.

Rule at L36-42: losses P->P 3, M->P 2, P->M 69, M->M 62; memory-final minus prompt-final 63 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit df93f52.
