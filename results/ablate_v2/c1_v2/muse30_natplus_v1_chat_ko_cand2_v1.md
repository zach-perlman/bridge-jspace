# C1 on tasks_v2 / muse30_natplus_v1_chat_ko_cand2_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 97 [95-99] (n=287) | 97 [95-99] (n=232) | 31 [25-38] (n=287) | 37 [28-45] (n=232) |
| L36-42 | paper10_rot | 97 [95-99] (n=287) | 97 [95-99] (n=232) | 98 [96-99] (n=287) | 97 [95-99] (n=232) |
| L36-42 | unembed10 | 95 [92-97] (n=287) | 98 [96-100] (n=232) | 49 [42-57] (n=287) | 64 [56-72] (n=232) |
| L36-42 | unembed10_rot | 97 [95-99] (n=287) | 97 [95-99] (n=232) | 99 [97-100] (n=287) | 99 [97-100] (n=232) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L36-42 | paper10 | 97 [95-99] (n=287) | 97 [95-99] (n=232) | 31 [25-38] (n=287) | 37 [28-45] (n=232) |
| L36-42 | paper10_rot | 97 [95-99] (n=287) | 97 [95-99] (n=232) | 98 [96-99] (n=287) | 97 [95-99] (n=232) |
| L36-42 | unembed10 | 95 [92-97] (n=287) | 98 [96-100] (n=232) | 49 [42-57] (n=287) | 64 [56-72] (n=232) |
| L36-42 | unembed10_rot | 97 [95-99] (n=287) | 97 [95-99] (n=232) | 99 [97-100] (n=287) | 99 [97-100] (n=232) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L36-42 | paper10 | - | - | - | - |
| L36-42 | paper10_rot | - | - | - | - |
| L36-42 | unembed10 | - | - | - | - |
| L36-42 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.50, M->P 1.62, P->M 1.88, M->M 2.31. Loss (points) by quartile of that margin (cuts 1.00, 1.81, 2.50), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 6 (n=103) | 1 (n=71) | 0 (n=74) | 0 (n=39) |
| M->P | 8 (n=72) | 0 (n=59) | 0 (n=50) | 0 (n=51) |
| P->M | 90 (n=60) | 69 (n=80) | 60 (n=85) | 58 (n=62) |
| M->M | 85 (n=40) | 66 (n=41) | 66 (n=61) | 51 (n=90) |
| prompt-final, pooled | 7 (n=175) | 1 (n=130) | 0 (n=124) | 0 (n=90) |
| memory-final, pooled | 88 (n=100) | 68 (n=121) | 62 (n=146) | 54 (n=152) |

Memory-final minus prompt-final, items pooled per group: raw 64; reweighted to the prompt-final margins 68, to the memory-final margins 65; matched within 0.25-logit margin bins 65 [60-69] (516 of 519 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L36-42 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 1.50, M->P 1.62, P->M 1.88, M->M 2.31. Loss (points) by quartile of that margin (cuts 1.00, 1.81, 2.50), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 13 (n=103) | 0 (n=71) | 0 (n=74) | 0 (n=39) |
| M->P | 6 (n=72) | 2 (n=59) | 0 (n=50) | 0 (n=51) |
| P->M | 75 (n=60) | 56 (n=80) | 41 (n=85) | 31 (n=62) |
| M->M | 62 (n=40) | 51 (n=41) | 36 (n=61) | 18 (n=90) |
| prompt-final, pooled | 10 (n=175) | 1 (n=130) | 0 (n=124) | 0 (n=90) |
| memory-final, pooled | 70 (n=100) | 55 (n=121) | 39 (n=146) | 23 (n=152) |

Memory-final minus prompt-final, items pooled per group: raw 40; reweighted to the prompt-final margins 47, to the memory-final margins 42; matched within 0.25-logit margin bins 41 [37-46] (516 of 519 memory-final items have a same-bin partner) points.

Rule at L36-42: losses P->P 2, M->P 3, P->M 68, M->M 63; memory-final minus prompt-final 63 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit 12bdc15.
