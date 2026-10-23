# C1 on tasks_v2 / olmoh7_natplus_v1_chat_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L4-8 | paper10 | 93 [89-96] (n=261) | 76 [69-84] (n=124) | 92 [89-96] (n=261) | 92 [86-97] (n=124) |
| L4-8 | paper10_rot | 92 [88-95] (n=261) | 87 [81-93] (n=124) | 97 [95-99] (n=261) | 99 [97-100] (n=124) |
| L4-8 | unembed10 | 95 [92-98] (n=261) | 93 [88-97] (n=124) | 98 [97-100] (n=261) | 97 [92-100] (n=124) |
| L4-8 | unembed10_rot | 95 [92-97] (n=261) | 95 [91-98] (n=124) | 97 [94-99] (n=261) | 100 [100-100] (n=124) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 100 | 100 | 100 |
| L4-8 | paper10 | 93 [89-96] (n=261) | 76 [69-84] (n=124) | 92 [89-96] (n=261) | 92 [86-97] (n=124) |
| L4-8 | paper10_rot | 92 [88-95] (n=261) | 87 [81-93] (n=124) | 97 [95-99] (n=261) | 99 [97-100] (n=124) |
| L4-8 | unembed10 | 95 [92-98] (n=261) | 93 [88-97] (n=124) | 98 [97-100] (n=261) | 97 [92-100] (n=124) |
| L4-8 | unembed10_rot | 95 [92-97] (n=261) | 95 [91-98] (n=124) | 97 [94-99] (n=261) | 100 [100-100] (n=124) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L4-8 | paper10 | - | - | - | - |
| L4-8 | paper10_rot | - | - | - | - |
| L4-8 | unembed10 | - | - | - | - |
| L4-8 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L4-8 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.67, M->P 2.43, P->M 1.91, M->M 2.98. Loss (points) by quartile of that margin (cuts 0.38, 2.46, 4.90), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 4 (n=46) | 16 (n=73) | 4 (n=80) | 0 (n=62) |
| M->P | 61 (n=23) | 28 (n=40) | 17 (n=24) | 3 (n=37) |
| P->M | 9 (n=90) | 12 (n=59) | 9 (n=55) | 0 (n=57) |
| M->M | 11 (n=35) | 15 (n=20) | 6 (n=33) | 3 (n=36) |
| prompt-final, pooled | 23 (n=69) | 20 (n=113) | 7 (n=104) | 1 (n=99) |
| memory-final, pooled | 10 (n=125) | 13 (n=79) | 8 (n=88) | 1 (n=93) |

Memory-final minus prompt-final, items pooled per group: raw -4; reweighted to the prompt-final margins -4, to the memory-final margins -6; matched within 0.25-logit margin bins -5 [-9--0] (355 of 385 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L4-8 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 2.67, M->P 2.43, P->M 1.91, M->M 2.98. Loss (points) by quartile of that margin (cuts 0.38, 2.46, 4.90), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 11 (n=46) | 8 (n=73) | 0 (n=80) | 0 (n=62) |
| M->P | 13 (n=23) | 15 (n=40) | 0 (n=24) | 0 (n=37) |
| P->M | 3 (n=90) | 2 (n=59) | 0 (n=55) | 0 (n=57) |
| M->M | 11 (n=35) | 0 (n=20) | 0 (n=33) | 0 (n=36) |
| prompt-final, pooled | 12 (n=69) | 11 (n=113) | 0 (n=104) | 0 (n=99) |
| memory-final, pooled | 6 (n=125) | 1 (n=79) | 0 (n=88) | 0 (n=93) |

Memory-final minus prompt-final, items pooled per group: raw -3; reweighted to the prompt-final margins -4, to the memory-final margins -4; matched within 0.25-logit margin bins -2 [-5--0] (355 of 385 memory-final items have a same-bin partner) points.

Rule at L4-8: losses P->P 7, M->P 24, P->M 8, M->M 8; memory-final minus prompt-final -7 points (>= 30 needed); controls within 10 points: no -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit df93f52.
