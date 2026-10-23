# C1 on tasks_v2 / olmo3d7_natplus_v1_chat_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L10-14 | paper10 | 82 [76-88] (n=175) | 90 [82-96] (n=77) | 87 [82-92] (n=175) | 94 [87-99] (n=77) |
| L10-14 | paper10_rot | 91 [87-95] (n=175) | 90 [81-96] (n=77) | 93 [88-97] (n=175) | 99 [96-100] (n=77) |
| L10-14 | unembed10 | 94 [90-97] (n=175) | 92 [86-97] (n=77) | 98 [96-100] (n=175) | 99 [96-100] (n=77) |
| L10-14 | unembed10_rot | 93 [89-96] (n=175) | 96 [91-100] (n=77) | 99 [97-100] (n=175) | 100 [100-100] (n=77) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L10-14 | paper10 | 82 [76-88] (n=175) | 90 [82-96] (n=77) | 87 [82-92] (n=175) | 94 [87-99] (n=77) |
| L10-14 | paper10_rot | 91 [87-95] (n=175) | 90 [81-96] (n=77) | 93 [88-97] (n=175) | 99 [96-100] (n=77) |
| L10-14 | unembed10 | 94 [90-97] (n=175) | 92 [86-97] (n=77) | 98 [96-100] (n=175) | 99 [96-100] (n=77) |
| L10-14 | unembed10_rot | 93 [89-96] (n=175) | 96 [91-100] (n=77) | 99 [97-100] (n=175) | 100 [100-100] (n=77) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L10-14 | paper10 | - | - | - | - |
| L10-14 | paper10_rot | - | - | - | - |
| L10-14 | unembed10 | - | - | - | - |
| L10-14 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L10-14 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.00, M->P 3.56, P->M 3.75, M->M 4.69. Loss (points) by quartile of that margin (cuts 1.19, 3.69, 5.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 27 (n=60) | 37 (n=38) | 3 (n=33) | 0 (n=44) |
| M->P | 12 (n=16) | 25 (n=24) | 0 (n=19) | 0 (n=18) |
| P->M | 27 (n=37) | 20 (n=50) | 6 (n=50) | 0 (n=38) |
| M->M | 21 (n=14) | 12 (n=17) | 0 (n=24) | 0 (n=22) |
| prompt-final, pooled | 24 (n=76) | 32 (n=62) | 2 (n=52) | 0 (n=62) |
| memory-final, pooled | 25 (n=51) | 18 (n=67) | 4 (n=74) | 0 (n=60) |

Memory-final minus prompt-final, items pooled per group: raw -4; reweighted to the prompt-final margins -3, to the memory-final margins -3; matched within 0.25-logit margin bins -1 [-7-5] (240 of 252 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L10-14 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.00, M->P 3.56, P->M 3.75, M->M 4.69. Loss (points) by quartile of that margin (cuts 1.19, 3.69, 5.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 17 (n=60) | 0 (n=38) | 0 (n=33) | 2 (n=44) |
| M->P | 12 (n=16) | 17 (n=24) | 0 (n=19) | 0 (n=18) |
| P->M | 5 (n=37) | 2 (n=50) | 0 (n=50) | 0 (n=38) |
| M->M | 7 (n=14) | 0 (n=17) | 0 (n=24) | 0 (n=22) |
| prompt-final, pooled | 16 (n=76) | 6 (n=62) | 0 (n=52) | 2 (n=62) |
| memory-final, pooled | 6 (n=51) | 1 (n=67) | 0 (n=74) | 0 (n=60) |

Memory-final minus prompt-final, items pooled per group: raw -5; reweighted to the prompt-final margins -5, to the memory-final margins -4; matched within 0.25-logit margin bins -4 [-9--1] (240 of 252 memory-final items have a same-bin partner) points.

Rule at L10-14: losses P->P 18, M->P 10, P->M 13, M->M 6; memory-final minus prompt-final -4 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 2b95595.
