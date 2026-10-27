# C1 on tasks_v2 / nem35l_natplus_v1_chat_ko_cand2_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 99 | 99 | 100 |
| L27-33 | paper10 | 97 [95-99] (n=304) | 97 [95-99] (n=329) | 37 [31-45] (n=304) | 55 [46-63] (n=329) |
| L27-33 | paper10_rot | 95 [93-97] (n=304) | 94 [91-97] (n=329) | 94 [91-96] (n=304) | 98 [97-100] (n=329) |
| L27-33 | unembed10 | 96 [94-98] (n=304) | 97 [95-99] (n=329) | 85 [81-89] (n=304) | 93 [89-96] (n=329) |
| L27-33 | unembed10_rot | 96 [94-98] (n=304) | 96 [94-98] (n=329) | 91 [87-94] (n=304) | 96 [94-98] (n=329) |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 99 | 99 | 99 | 100 |
| L27-33 | paper10 | 97 [95-99] (n=304) | 97 [95-99] (n=329) | 37 [31-45] (n=304) | 55 [46-63] (n=329) |
| L27-33 | paper10_rot | 95 [93-97] (n=304) | 94 [91-97] (n=329) | 94 [91-96] (n=304) | 98 [97-100] (n=329) |
| L27-33 | unembed10 | 96 [94-98] (n=304) | 97 [95-99] (n=329) | 85 [81-89] (n=304) | 93 [89-96] (n=329) |
| L27-33 | unembed10_rot | 96 [94-98] (n=304) | 96 [94-98] (n=329) | 91 [87-94] (n=304) | 96 [94-98] (n=329) |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L27-33 | paper10 | - | - | - | - |
| L27-33 | paper10_rot | - | - | - | - |
| L27-33 | unembed10 | - | - | - | - |
| L27-33 | unembed10_rot | - | - | - | - |


## Margin-matched gap under paper10 at L27-33 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.50, M->P 3.75, P->M 2.75, M->M 3.88. Loss (points) by quartile of that margin (cuts 1.50, 3.50, 4.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 4 (n=90) | 3 (n=67) | 0 (n=47) | 0 (n=100) |
| M->P | 2 (n=86) | 3 (n=71) | 1 (n=72) | 0 (n=100) |
| P->M | 58 (n=100) | 69 (n=112) | 55 (n=62) | 63 (n=30) |
| M->M | 38 (n=47) | 50 (n=82) | 41 (n=140) | 53 (n=60) |
| prompt-final, pooled | 3 (n=176) | 3 (n=138) | 1 (n=119) | 0 (n=200) |
| memory-final, pooled | 52 (n=147) | 61 (n=194) | 45 (n=202) | 57 (n=90) |

Memory-final minus prompt-final, items pooled per group: raw 51; reweighted to the prompt-final margins 52, to the memory-final margins 51; matched within 0.25-logit margin bins 52 [47-56] (583 of 633 memory-final items have a same-bin partner) points.

## Margin-matched gap under unembed10 at L27-33 (reported, outside the rule; added after the rule)

Median unedited answer margin (logits): P->P 3.50, M->P 3.75, P->M 2.75, M->M 3.88. Loss (points) by quartile of that margin (cuts 1.50, 3.50, 4.75), n per cell:

| word | Q1 (least confident) | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| P->P | 7 (n=90) | 3 (n=67) | 0 (n=47) | 0 (n=100) |
| M->P | 6 (n=86) | 1 (n=71) | 0 (n=72) | 0 (n=100) |
| P->M | 26 (n=100) | 14 (n=112) | 2 (n=62) | 0 (n=30) |
| M->M | 34 (n=47) | 5 (n=82) | 2 (n=140) | 0 (n=60) |
| prompt-final, pooled | 6 (n=176) | 2 (n=138) | 0 (n=119) | 0 (n=200) |
| memory-final, pooled | 29 (n=147) | 10 (n=194) | 2 (n=202) | 0 (n=90) |

Memory-final minus prompt-final, items pooled per group: raw 8; reweighted to the prompt-final margins 8, to the memory-final margins 8; matched within 0.25-logit margin bins 7 [4-10] (583 of 633 memory-final items have a same-bin partner) points.

Rule at L27-33: losses P->P 2, M->P 2, P->M 62, M->M 45; memory-final minus prompt-final 52 points (>= 30 needed); controls within 10 points: yes -> C1-graded HOLDS
Original strict C1 (reported): holds. Output from commit b83f3cc.
