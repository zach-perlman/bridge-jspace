# C1 on tasks_v2 / qwen3_32b_full3_ko_steps_v1 (rule fixed in scripts/c1_v2.py)

Accuracy % on the whole question [95% CI over bridge entities]; unedited first.

## all formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L44-52 | paper10 | - | - | - | - | - | - |
| L44-52 | paper10_rot | - | - | - | - | - | - |

## text formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L44-52 | paper10 | - | - | - | - | - | - |
| L44-52 | paper10_rot | - | - | - | - | - | - |

## structured formats

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan | nan |
| L44-52 | paper10 | - | - | - | - | - | - |
| L44-52 | paper10_rot | - | - | - | - | - | - |

## secondary stratum (planets, three-step words), all formats

| band | condition | P->P->P | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|
| - | unedited | nan | nan | nan | nan | nan |
| L44-52 | paper10 | - | - | - | - | - |
| L44-52 | paper10_rot | - | - | - | - | - |

## step1 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 86 | 88 | 90 |
| L44-52 | paper10 | 100 | 100 | 99 | 86 | 97 | 88 |
| L44-52 | paper10_rot | 98 | 100 | 100 | 92 | 94 | 93 |

## step2 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L44-52 | paper10 | 98 | 99 | 97 | 100 | 100 | 99 |
| L44-52 | paper10_rot | 98 | 99 | 100 | 100 | 100 | 100 |

## step3 alone (all formats)

| band | condition | P->P->P | P->P->M | P->M->P | M->P->P | M->P->M | M->M->P |
|---|---|---|---|---|---|---|---|
| - | unedited | 100 | 100 | 100 | 100 | 100 | 100 |
| L44-52 | paper10 | 100 | 81 | 100 | 100 | 91 | 100 |
| L44-52 | paper10_rot | 100 | 100 | 100 | 100 | 100 | 100 |


Rule at L44-52: losses ; memory-final minus prompt-final - points (>= 30 needed); controls within 10 points: no -> C1-graded n/a (no whole-question rows at this band)
Original strict C1 (reported): n/a. Output from commit 50be071.
