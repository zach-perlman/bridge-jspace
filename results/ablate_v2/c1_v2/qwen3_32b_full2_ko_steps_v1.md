# C1 on tasks_v2 / qwen3_32b_full2_ko_steps_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L44-52 | paper10 | - | - | - | - | - | - |
| L44-52 | paper10_rot | - | - | - | - | - | - |

## text formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L44-52 | paper10 | - | - | - | - | - | - |
| L44-52 | paper10_rot | - | - | - | - | - | - |

## structured formats

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L44-52 | paper10 | - | - | - | - | - | - |
| L44-52 | paper10_rot | - | - | - | - | - | - |

## step1 alone (all formats)

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 97 | 100 | 97 | 98 | 98 |
| L44-52 | paper10 | 99 | 97 | 99 | 97 | 92 | 92 |
| L44-52 | paper10_rot | 100 | 100 | 100 | 100 | 99 | 99 |

## step2 alone (all formats)

| band | condition | P->P | M->P | P->M | M->M | C->P | C->M |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L44-52 | paper10 | 100 | 100 | 90 | 72 | 99 | 88 |
| L44-52 | paper10_rot | 100 | 100 | 100 | 93 | 100 | 99 |


Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L44-52: losses ; memory-final minus prompt-final - points (>= 30 needed); controls within 10 points: no -> C1-graded n/a (no whole-question rows at this band)
Original strict C1 (reported): n/a. Output from commit 50be071.
