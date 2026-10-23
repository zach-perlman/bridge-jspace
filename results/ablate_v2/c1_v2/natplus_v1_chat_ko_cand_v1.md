# C1 on tasks_v2 / natplus_v1_chat_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 99 |
| L32-40 | paper10 | 95 [92-97] (n=420) | 90 [87-93] (n=366) | 42 [37-48] (n=420) | 42 [35-49] (n=366) |
| L32-40 | paper10_rot | 96 [95-98] (n=420) | 97 [95-99] (n=366) | 98 [97-99] (n=420) | 98 [96-99] (n=366) |
| L32-40 | unembed10 | 99 [98-100] (n=420) | 99 [98-100] (n=366) | 99 [97-100] (n=420) | 99 [99-100] (n=366) |
| L32-40 | unembed10_rot | 99 [97-100] (n=420) | 99 [98-100] (n=366) | 99 [98-100] (n=420) | 98 [97-99] (n=366) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 99 |
| L32-40 | paper10 | 95 [92-97] (n=420) | 90 [87-93] (n=366) | 42 [37-48] (n=420) | 42 [35-49] (n=366) |
| L32-40 | paper10_rot | 96 [95-98] (n=420) | 97 [95-99] (n=366) | 98 [97-99] (n=420) | 98 [96-99] (n=366) |
| L32-40 | unembed10 | 99 [98-100] (n=420) | 99 [98-100] (n=366) | 99 [97-100] (n=420) | 99 [99-100] (n=366) |
| L32-40 | unembed10_rot | 99 [97-100] (n=420) | 99 [98-100] (n=366) | 99 [98-100] (n=420) | 98 [97-99] (n=366) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L32-40 | paper10 | - | - | - | - |
| L32-40 | paper10_rot | - | - | - | - |
| L32-40 | unembed10 | - | - | - | - |
| L32-40 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.38, M->P 5.50, P->M 5.25, M->M 5.38. Loss (points) by quartile of that margin (cuts 3.38, 5.62, 7.12), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 21 (n=96) | 0 (n=76) | 0 (n=100) | 1 (n=148) |
| M->P | 29 (n=99) | 2 (n=96) | 4 (n=82) | 3 (n=89) |
| P->M | 76 (n=119) | 57 (n=115) | 45 (n=118) | 50 (n=68) |
| M->M | 75 (n=91) | 62 (n=114) | 44 (n=99) | 44 (n=62) |
| prompt-final, pooled | 25 (n=195) | 1 (n=172) | 2 (n=182) | 2 (n=237) |
| memory-final, pooled | 75 (n=210) | 59 (n=229) | 45 (n=217) | 47 (n=130) |

Memory-final minus prompt-final, items pooled per group: raw 50; reweighted to the prompt-final margins 49, to the memory-final margins 50; matched within 0.25-logit margin bins 49 [45-53] (773 of 786 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L32-40 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 6.38, M->P 5.50, P->M 5.25, M->M 5.38. Loss (points) by quartile of that margin (cuts 3.38, 5.62, 7.12), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 3 (n=96) | 0 (n=76) | 0 (n=100) | 0 (n=148) |
| M->P | 3 (n=99) | 0 (n=96) | 0 (n=82) | 0 (n=89) |
| P->M | 5 (n=119) | 0 (n=115) | 0 (n=118) | 0 (n=68) |
| M->M | 0 (n=91) | 0 (n=114) | 0 (n=99) | 0 (n=62) |
| prompt-final, pooled | 3 (n=195) | 0 (n=172) | 0 (n=182) | 0 (n=237) |
| memory-final, pooled | 3 (n=210) | 0 (n=229) | 0 (n=217) | 0 (n=130) |

Memory-final minus prompt-final, items pooled per group: raw 0; reweighted to the prompt-final margins -0, to the memory-final margins -0; matched within 0.25-logit margin bins -1 [-3-0] (773 of 786 memory-final items have a same-bin partner) points.

Rule at L32-40: losses P->P 5, M->P 10, P->M 58, M->M 57; memory-final minus prompt-final 50 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): fails. Output from commit 2b95595.
