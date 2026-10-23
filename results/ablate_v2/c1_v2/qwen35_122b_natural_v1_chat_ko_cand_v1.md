# C1 on tasks_v2 / qwen35_122b_natural_v1_chat_ko_cand_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L24-30 | paper10 | 93 [89-96] (n=231) | 84 [79-89] (n=244) | 97 [94-99] (n=231) | 96 [91-100] (n=244) |
| L24-30 | paper10_rot | 95 [92-97] (n=231) | 95 [91-98] (n=244) | 98 [96-100] (n=231) | 98 [95-100] (n=244) |
| L24-30 | unembed10 | 96 [93-98] (n=231) | 96 [93-98] (n=244) | 99 [98-100] (n=231) | 98 [97-100] (n=244) |
| L24-30 | unembed10_rot | 97 [95-99] (n=231) | 96 [93-99] (n=244) | 99 [97-100] (n=231) | 99 [98-100] (n=244) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 |
| L24-30 | paper10 | 93 [89-96] (n=231) | 84 [79-89] (n=244) | 97 [94-99] (n=231) | 96 [91-100] (n=244) |
| L24-30 | paper10_rot | 95 [92-97] (n=231) | 95 [91-98] (n=244) | 98 [96-100] (n=231) | 98 [95-100] (n=244) |
| L24-30 | unembed10 | 96 [93-98] (n=231) | 96 [93-98] (n=244) | 99 [98-100] (n=231) | 98 [97-100] (n=244) |
| L24-30 | unembed10_rot | 97 [95-99] (n=231) | 96 [93-99] (n=244) | 99 [97-100] (n=231) | 99 [98-100] (n=244) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L24-30 | paper10 | - | - | - | - |
| L24-30 | paper10_rot | - | - | - | - |
| L24-30 | unembed10 | - | - | - | - |
| L24-30 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L24-30 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.12, M->P 5.25, P->M 6.38, M->M 7.38. Loss (points) by quartile of that margin (cuts 4.00, 6.38, 7.62), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 17 (n=86) | 3 (n=73) | 0 (n=38) | 0 (n=34) |
| M->P | 33 (n=92) | 9 (n=65) | 2 (n=49) | 3 (n=38) |
| P->M | 20 (n=41) | 0 (n=77) | 0 (n=66) | 0 (n=47) |
| M->M | 43 (n=21) | 0 (n=35) | 0 (n=81) | 0 (n=107) |
| prompt-final, pooled | 25 (n=178) | 6 (n=138) | 1 (n=87) | 1 (n=72) |
| memory-final, pooled | 27 (n=62) | 0 (n=112) | 0 (n=147) | 0 (n=154) |

Memory-final minus prompt-final, items pooled per group: raw -8; reweighted to the prompt-final margins -1, to the memory-final margins -2; matched within 0.25-logit margin bins -1 [-3-1] (472 of 475 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L24-30 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 5.12, M->P 5.25, P->M 6.38, M->M 7.38. Loss (points) by quartile of that margin (cuts 4.00, 6.38, 7.62), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 10 (n=86) | 0 (n=73) | 0 (n=38) | 0 (n=34) |
| M->P | 10 (n=92) | 0 (n=65) | 0 (n=49) | 0 (n=38) |
| P->M | 2 (n=41) | 1 (n=77) | 0 (n=66) | 0 (n=47) |
| M->M | 19 (n=21) | 0 (n=35) | 0 (n=81) | 0 (n=107) |
| prompt-final, pooled | 10 (n=178) | 0 (n=138) | 0 (n=87) | 0 (n=72) |
| memory-final, pooled | 8 (n=62) | 1 (n=112) | 0 (n=147) | 0 (n=154) |

Memory-final minus prompt-final, items pooled per group: raw -3; reweighted to the prompt-final margins -1, to the memory-final margins -0; matched within 0.25-logit margin bins 0 [-1-1] (472 of 475 memory-final items have a same-bin partner) points.

Rule at L24-30: losses P->P 7, M->P 16, P->M 3, M->M 4; memory-final minus prompt-final -8 points (>= 30 needed); controls within 10 points: yes -> C1-graded FAILS
Original strict C1 (reported): fails. Output from commit 6ba91f2.
