# 47.13: does the address probe predict the lookup's errors?

Batch 47, test 47.13 (jobs/c3/batch47.yaml, amendment 4; Q47.13, Dan: 65%). Unedited scenes where the lookup answers wrong, from the varied-scene runs (x0b_v2; the d1 sets hold almost no lookup errors, see the script's docstring); the slot probe trained on the scenes the lookup gets right (per format and locker order, the wrong item's entity held out) against the slot of the wrong answer; the lens's top item at the bridge word from the gpu stage. Cluster bootstrap over bridge items (10000, seed 0). UNVERIFIED.

Rule (fixed in advance): "The address predicts the error" if the probe's slot matches the wrong answer's slot in >= 0.5 of wrong items (chance ~ 0.33 with three lockers; the layout baseline beside), and the lens's top item at the bridge word is still the right item in >= 0.8 of those.

| model | run | status | wrong items (with a slot / with a probe; entities) | chance | probe matches the wrong slot | majority | layout | structure | probe = gold slot | lens top item right: matched / all | holds |
|---|---|---|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | nem35l_x52_errors | scored | 105 (100 / 105; 40) | 0.19 | 0.05 [0.01, 0.09] | 0.20 [0.12, 0.28] | 0.11 [0.06, 0.17] | 0.15 [0.10, 0.21] | 0.64 [0.55, 0.72] | 1.00 [1.00, 1.00] / 0.99 [0.95, 1.00] | no () |

Over the wrong items that have a slot (a locker statement states the answered digit):

| model | n | probe | majority | layout | structure |
|---|---|---|---|---|---|
| nemotron-3.5-lightning | 100 | 0.05 [0.01, 0.10] | 0.21 [0.13, 0.30] | 0.12 [0.06, 0.18] | 0.16 [0.10, 0.23] |

By format and by locker order (descriptive):

| model | split | n | probe matches the wrong slot | majority | layout | probe = gold slot |
|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | json | 33 | 0.06 [0.00, 0.15] | 0.21 [0.06, 0.37] | 0.15 [0.00, 0.28] | 0.64 [0.48, 0.80] |
| nemotron-3.5-lightning | prose | 29 | 0.03 [0.00, 0.12] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.83 [0.70, 0.94] |
| nemotron-3.5-lightning | table | 43 | 0.05 [0.00, 0.12] | 0.33 [0.20, 0.49] | 0.16 [0.07, 0.27] | 0.51 [0.33, 0.67] |
| nemotron-3.5-lightning | after | 20 | 0.05 [0.00, 0.18] | 0.20 [0.00, 0.44] | 0.10 [0.00, 0.24] | 0.05 [0.00, 0.15] |
| nemotron-3.5-lightning | before | 85 | 0.05 [0.01, 0.09] | 0.20 [0.12, 0.28] | 0.12 [0.05, 0.18] | 0.78 [0.67, 0.87] |

The probe on the right scenes (entity-held-out CV accuracy per group; descriptive):

| model | format | order | right scenes | entities | wrong items | probe | CV accuracy | majority share |
|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | json | after | 86 | 21 | 4 | yes | 0.10 | 0.20 |
| nemotron-3.5-lightning | json | before | 290 | 28 | 29 | yes | 0.68 | 0.24 |
| nemotron-3.5-lightning | prose | after | 264 | 50 | 4 | yes | 0.29 | 0.29 |
| nemotron-3.5-lightning | prose | before | 726 | 60 | 25 | yes | 0.68 | 0.33 |
| nemotron-3.5-lightning | table | after | 247 | 52 | 12 | yes | 0.21 | 0.25 |
| nemotron-3.5-lightning | table | before | 739 | 61 | 31 | yes | 0.77 | 0.22 |
