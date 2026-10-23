# C1 on tasks_v2 / qwen35_9b_natural_v1_chat_ko_steps_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |

## text formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |

## structured formats

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan |
| L12-16 | paper10 | - | - | - | - |
| L12-16 | paper10_rot | - | - | - | - |

## step1 alone (all formats)

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 90 | 100 | 70 |
| L12-16 | paper10 | 91 | 82 | 91 | 32 |
| L12-16 | paper10_rot | 100 | 84 | 100 | 71 |

## step2 alone (all formats)

| band | condition | P->P | M->P | P->M | M->M |
|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 99 | 100 |
| L12-16 | paper10 | 97 | 96 | 45 | 47 |
| L12-16 | paper10_rot | 100 | 100 | 99 | 99 |


Specificity control: no unembed10 rows in this run. Every model gets one (2026-10-21): ablate_v2 --conditions unembed10 unembed10_rot on the same items, then scripts/c1_specificity.py.

Rule at L12-16: losses ; memory-final minus prompt-final - points (>= 30 needed); controls within 10 points: no -> C1-graded n/a (no whole-question rows at this band)
Original strict C1 (reported): n/a. Output from commit d2cbf82.
