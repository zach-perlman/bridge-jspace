# 47.0b: margins of the non-switchers (descriptive)

Unedited logit margin, logit(original) − logit(changed), of the items the whole change switches against those it does not, at the layer fixed in advance (chat). Means with 95% cluster-bootstrap intervals over bridge items (10000 resamples, seed 0); the difference on paired draws. AUC: the chance a random stayer's margin is above a random switcher's (0.5 = the margin does not tell them apart). UNVERIFIED.

| design | model (layer) | reader | scenes | n switch / stay | margin, switchers | margin, stayers | stayers − switchers | median switch / stay | AUC |
|---|---|---|---|---|---|---|---|---|---|
| main test | Qwen3.5-9B (L12) | lookup | all | 105 / 95 | 3.70 [3.47, 3.96] | 3.71 [3.40, 3.97] | 0.01 [−0.39, 0.33] | 3.88 / 3.88 | 0.50 |
| main test | Qwen3.5-9B (L12) | lookup | locker before the pick | 86 / 14 | 4.03 [3.81, 4.26] | 4.10 [3.66, 4.61] | 0.07 [−0.43, 0.58] | 4.06 / 4.19 | 0.50 |
| main test | Qwen3.5-9B (L12) | recall | all | 197 / 3° | 3.80 [3.43, 4.10] | 2.85 [1.00, 5.44] | −0.94 [−2.82, 1.65] | 3.75 / 2.12 | 0.33 |
| main test | Qwen3.5-9B (L12) | recall | locker before the pick | 100 / 0° | 3.92 [3.57, 4.21] | – | – | 3.94 / – | – |
| main test | Qwen3.6-27B (L32) | lookup | all | 86 / 114 | 7.23 [6.94, 7.53] | 7.77 [7.55, 7.96] | 0.54 [0.24, 0.82] | 7.34 / 7.94 | 0.60 |
| main test | Qwen3.6-27B (L32) | lookup | locker before the pick | 77 / 24 | 7.49 [7.14, 7.82] | 7.93 [7.51, 8.40] | 0.45 [−0.08, 0.98] | 7.62 / 7.78 | 0.60 |
| main test | Qwen3.6-27B (L32) | recall | all | 150 / 50 | 6.13 [5.76, 6.42] | 6.68 [6.35, 7.00] | 0.55 [0.18, 0.95] | 6.25 / 6.75 | 0.59 |
| main test | Qwen3.6-27B (L32) | recall | locker before the pick | 75 / 26 | 6.29 [5.87, 6.64] | 6.40 [5.96, 6.83] | 0.11 [−0.40, 0.63] | 6.25 / 6.31 | 0.51 |
| main test | Muse Glimmer 30B (L26) | lookup | all | 70 / 130 | 3.45 [3.20, 3.75] | 3.74 [3.56, 3.91] | 0.29 [−0.08, 0.61] | 3.62 / 3.88 | 0.57 |
| main test | Muse Glimmer 30B (L26) | lookup | locker before the pick | 60 / 32 | 3.71 [3.51, 3.93] | 4.03 [3.61, 4.41] | 0.32 [−0.14, 0.75] | 3.88 / 4.12 | 0.61 |
| main test | Muse Glimmer 30B (L26) | recall | all | 117 / 83 | 5.27 [4.68, 5.72] | 5.26 [4.70, 5.75] | −0.01 [−0.53, 0.52] | 5.19 / 5.38 | 0.51 |
| main test | Muse Glimmer 30B (L26) | recall | locker before the pick | 47 / 45 | 5.50 [4.83, 5.92] | 5.49 [4.91, 6.04] | −0.01 [−0.53, 0.61] | 5.25 / 5.44 | 0.48 |
| clean design | Qwen3.5-9B (L12) | lookup | all | 216 / 201 | 4.03 [3.86, 4.21] | 3.51 [3.35, 3.68] | −0.52 [−0.72, −0.33] | 4.25 / 3.62 | 0.37 |
| clean design | Qwen3.5-9B (L12) | lookup | locker before the pick | 182 / 34 | 4.23 [4.07, 4.40] | 3.66 [3.35, 4.00] | −0.57 [−0.93, −0.20] | 4.38 / 3.75 | 0.34 |
| clean design | Qwen3.5-9B (L12) | recall | all | 411 / 6° | 3.61 [3.28, 3.90] | 4.46 [2.91, 6.02] | 0.85 [−0.52, 2.35] | 3.62 / 4.31 | 0.62 |
| clean design | Qwen3.5-9B (L12) | recall | locker before the pick | 214 / 2° | 3.59 [3.24, 3.88] | 3.19 [2.25, 4.12] | −0.40 [−1.53, 0.77] | 3.62 / 3.19 | 0.40 |
| clean design | Qwen3.6-27B (L32) | lookup | all | 222 / 352 | 7.78 [7.64, 7.92] | 7.91 [7.77, 8.03] | 0.13 [−0.05, 0.28] | 7.84 / 8.06 | 0.55 |
| clean design | Qwen3.6-27B (L32) | lookup | locker before the pick | 219 / 67 | 7.79 [7.66, 7.94] | 8.08 [7.81, 8.34] | 0.29 [0.00, 0.57] | 7.88 / 8.12 | 0.59 |
| clean design | Qwen3.6-27B (L32) | recall | all | 445 / 129 | 6.06 [5.79, 6.29] | 6.58 [6.24, 6.88] | 0.52 [0.15, 0.89] | 6.12 / 6.69 | 0.58 |
| clean design | Qwen3.6-27B (L32) | recall | locker before the pick | 236 / 50 | 5.85 [5.55, 6.13] | 6.20 [5.89, 6.56] | 0.35 [−0.03, 0.82] | 5.88 / 6.50 | 0.55 |
| clean design | Muse Glimmer 30B (L26) | lookup | all | 131 / 278 | 4.75 [4.61, 4.90] | 4.81 [4.69, 4.96] | 0.07 [−0.11, 0.25] | 4.75 / 4.81 | 0.53 |
| clean design | Muse Glimmer 30B (L26) | lookup | locker before the pick | 129 / 75 | 4.75 [4.61, 4.90] | 4.91 [4.65, 5.20] | 0.16 [−0.16, 0.48] | 4.75 / 4.75 | 0.55 |
| clean design | Muse Glimmer 30B (L26) | recall | all | 293 / 116 | 5.40 [4.78, 5.81] | 5.23 [4.75, 5.67] | −0.17 [−0.55, 0.25] | 5.38 / 5.19 | 0.47 |
| clean design | Muse Glimmer 30B (L26) | recall | locker before the pick | 133 / 71 | 5.37 [4.60, 5.89] | 5.30 [4.78, 5.81] | −0.07 [−0.62, 0.57] | 5.38 / 5.19 | 0.48 |

° fewer than 10 items in a group: its mean and interval are noise.

Checks:
- main test, qwen3.5-9b: lookup: max |ld| spread of 'none' across layers = 0.25; lookup: unedited margins <= 0 (org not on top) = 1; recall: max |ld| spread of 'none' across layers = 0.25; recall: unedited margins <= 0 (org not on top) = 0
- main test, qwen3.6-27b: lookup: max |ld| spread of 'none' across layers = 0.188; lookup: unedited margins <= 0 (org not on top) = 0; recall: max |ld| spread of 'none' across layers = 0.25; recall: unedited margins <= 0 (org not on top) = 0
- main test, muse-glimmer-30b: lookup: max |ld| spread of 'none' across layers = 0.0; lookup: unedited margins <= 0 (org not on top) = 1; recall: max |ld| spread of 'none' across layers = 0.0; recall: unedited margins <= 0 (org not on top) = 0
- clean design, qwen3.5-9b: lookup: max |ld| spread of 'none' across layers = 0.0; lookup: unedited margins <= 0 (org not on top) = 0; recall: max |ld| spread of 'none' across layers = 0.0; recall: unedited margins <= 0 (org not on top) = 2
- clean design, qwen3.6-27b: lookup: max |ld| spread of 'none' across layers = 0.0; lookup: unedited margins <= 0 (org not on top) = 0; recall: max |ld| spread of 'none' across layers = 0.0; recall: unedited margins <= 0 (org not on top) = 0
- clean design, muse-glimmer-30b: lookup: max |ld| spread of 'none' across layers = 0.0; lookup: unedited margins <= 0 (org not on top) = 0; recall: max |ld| spread of 'none' across layers = 0.0; recall: unedited margins <= 0 (org not on top) = 0
