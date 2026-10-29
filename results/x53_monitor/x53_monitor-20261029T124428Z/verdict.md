# 53.2, the monitor test: what a J-space readout can decode vs the full state

UNVERIFIED. rule fixed in advance in jobs/c3/batch53.yaml (53.2); no prediction. Spec: jobs/c3/batch53.yaml (53.2); jobs/c3/x53_monitor_*.yaml.

Rule (verbatim): "J-space blind to X" if the J++ probe is within 0.10 of the random subspace at every layer while the full residual reaches >= 0.8 at some layer; "J-space carries X" if J++ >= 0.8 and >= 0.3 above random; else in between.

As computed: per model, dataset, position, target and k, on point estimates (accuracy over rows and 5 seeds of 5-fold CV, each seed a random assignment of the groups to the folds), over every cached layer (every second layer from L0); logistic probes, C = 1.0 for every feature (sklearn's objective, standardised features, scipy L-BFGS); (b), (c) on held-out entities; (a), (d) on held-out scenes (a held-out entity is an unseen class there). CIs: cluster bootstrap over the bridge entity (10,000, seed 0).

Dan's changes before scoring (jobs/c3/batch53.yaml critic_1125, verbatim): "53.2 changes, before scoring: headline targets (b) slot and (c) lookup digit; (a) and (d) are positive controls. Add a fixed J++ subspace (the k atoms most frequent on the training folds) and an energy-matched random subspace beside the current ones. Check one cell against sklearn."

So: the headline targets are (b) and (c); (a) and (d) are positive controls (their rule outcome below, under their own heading). The decisive label is the brief's (the per-state J++ part vs a random subspace of the same k). Beside it: (i) the same rule verbatim with the J++ entries replaced by the fixed J++ subspace (fix_k: per training fold the span of the k atoms most frequent among the training rows' first k OMP atoms, ties the smaller token id; the held-out rows projected on it unchanged) against the same random_k; (ii) Dan's 13:15 energy rule (below) on the per-state J++ part against the energy-matched random subspace (erand_k: dimension r = round(the J++_k part's median share of ||h||^2 at that layer and row set, over all rows, label-free, x d), the first r columns of the random_k frame; a Haar r-dimensional subspace keeps r / d of ||h||^2 in expectation; rescaling a k-dimensional part instead would change nothing, the probes standardise every feature).

Dan 13:15, fixed before the verdict (jobs/c3/batch53.yaml answers_1315, verbatim): "53.2, fixed before the verdict: if J++ is >= 0.10 below the energy-matched random while the full state is >= 0.8, the label is "the address is under-represented in the lens directions" (stronger than blind), not an energy artefact. If J++ is within 0.10 of the energy-matched random, "no different from random directions of the same energy"."

Applied beside the decisive labels, on the per-state J++ part vs the energy-matched random: 'under-represented in the lens directions' if at some layer where the full state is >= 0.8 J++ is >= 0.10 below the energy-matched random (the agent's reading of 'while', flagged); 'no different from random directions of the same energy' if J++ is within 0.10 of it at every layer (as 53.2's 'within 0.10', flagged); else in between; where both hold exactly at the bar, under-represented. 'The address' is Dan's word for the slot; for the other targets the same thresholds with the target named ('<X> is under-represented in the lens directions'), flagged. The 11:40 labels on the fixed-k random stay as they are.

Dan's wording, fixed before the verdict (jobs/c3/batch53.yaml additions_1140 item 2, verbatim): "report two monitors separately. (a) The lens readout (top words): cite 47.0, unchanged. (b) The trained probe on J++ coordinates vs random vs full. If the random subspace also decodes the slot ("random reads it too"), the wording is: "the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it" — not "J-space is blind". Only "J-space blind" if J++ is within 0.10 of random AND random is under 0.8 while the full state is >= 0.8."

Applied: 'J-space blind to X' only if J++ is within 0.10 of random at every layer AND the random subspace stays under 0.8 at every layer (the agent's reading of 'random is under 0.8', flagged) while the full state reaches >= 0.8 at some layer. Where J++ is within 0.10 of random everywhere and the full state reaches 0.8 but so does random ('random reads it too'), the slot's label is Dan's sentence: "the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it"; for the other targets the agent writes '<X> is linearly decodable from many subspaces, J++ included' (the lens-readout clause is 47.0's, which is about the address). 'carries' and 'in between' as in the brief. Notes column: 'random reads it too' where that case opens; 'full < 0.8' where the full residual never reaches 0.8 (then neither 'blind' nor 'carries' can open).

## Monitor (a): the lens readout (top words)

Cited, unchanged: 47.0 ('is the pointer verbalizable?'; results/x47_verbal/summary-20261028T033646Z/verbal.md for Qwen3.5-9B, Qwen3.6-27B and Muse Glimmer 30B; results/x47_verbal/summary-20261029T005548Z/verbal.md for Nemotron 3.5 Lightning): read 'not verbalizable' on all four models. No new numbers here.

## Monitor (b): the trained probe on J++ coordinates vs random vs full

At a glance, the headline targets' decisive labels (k = 25 / 100; blind = 'J-space blind to X', carries = 'J-space carries X', many = random reads it too: Dan's sentence for the slot, 'decodable from many subspaces, J++ included' for the digit; between = in between). Full wording and the arms beside in the tables below.

| model | dataset | (b) its locker slot at B | (b) its locker slot at T | (c) lookup's digit at B | (c) lookup's digit at T |
|---|---|---|---|---|---|
| Qwen3.5-9B | main | between / between | blind / between | between / between | between / many |
| Qwen3.5-9B | json | between / between | between / between | between / between | between / many |
| Qwen3.6-27B | main | between / between | between / between | between / between | many / between |
| Qwen3.6-27B | json | between / between | between / between | between / between | many / many |
| Muse-Glimmer-30B | main | between / between | blind / between | between / between | between / many |
| Muse-Glimmer-30B | json | between / between | between / between | between / between | between / many |
| Nemotron-3.5-Lightning | main | between / between | between / between | between / between | many / many |
| Nemotron-3.5-Lightning | json | between / between | between / between | between / between | between / many |

Beside, Dan 13:15's energy rule on the same cells (per-state J++ vs the energy-matched random; under = 'under-represented in the lens directions', same energy = 'no different from random directions of the same energy', between = in between):

| model | dataset | (b) its locker slot at B | (b) its locker slot at T | (c) lookup's digit at B | (c) lookup's digit at T |
|---|---|---|---|---|---|
| Qwen3.5-9B | main | between / same energy | under / under | same energy / same energy | under / under |
| Qwen3.5-9B | json | between / between | between / between | same energy / same energy | between / between |
| Qwen3.6-27B | main | between / between | under / under | same energy / same energy | between / between |
| Qwen3.6-27B | json | between / between | between / between | same energy / same energy | between / between |
| Muse-Glimmer-30B | main | between / between | under / under | same energy / same energy | under / between |
| Muse-Glimmer-30B | json | between / between | between / between | same energy / same energy | under / under |
| Nemotron-3.5-Lightning | main | between / between | under / under | same energy / same energy | same energy / same energy |
| Nemotron-3.5-Lightning | json | between / same energy | between / between | same energy / same energy | same energy / same energy |

### Headline: (b) the bridge's locker slot and (c) the lookup's answer digit

| model | dataset | position | target | k | decisive: J++ (per state) vs random | beside: fixed J++ vs random | beside: J++ vs energy-matched random (Dan 13:15) | full / J++ / fixed / random / e-random / PCA max | notes |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | main (400 rows, 43 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.71 / 0.61 / 0.58 / 0.61 / 0.68 / 0.72 | full < 0.8 |
| Qwen3.5-9B | main (400 rows, 43 bridges) | B | (b) its locker slot | 100 | in between | in between | no different from random directions of the same energy | 0.71 / 0.71 / 0.62 / 0.64 / 0.69 / 0.71 | full < 0.8 |
| Qwen3.5-9B | main (400 rows, 43 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.13 / 0.14 / 0.13 / 0.13 / 0.12 / 0.14 | full < 0.8 |
| Qwen3.5-9B | main (400 rows, 43 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.13 / 0.16 / 0.15 / 0.12 / 0.12 / 0.13 | full < 0.8 |
| Qwen3.5-9B | main (400 rows, 43 bridges) | T | (b) its locker slot | 25 | J-space blind to X | J-space blind to X | the address is under-represented in the lens directions | 0.88 / 0.63 / 0.66 / 0.65 / 0.83 / 0.77 |  |
| Qwen3.5-9B | main (400 rows, 43 bridges) | T | (b) its locker slot | 100 | in between | J-space blind to X | the address is under-represented in the lens directions | 0.88 / 0.74 / 0.73 / 0.77 / 0.86 / 0.82 |  |
| Qwen3.5-9B | main (400 rows, 43 bridges) | T | (c) lookup's digit | 25 | in between | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is under-represented in the lens directions | 1.00 / 0.97 / 0.90 / 0.94 / 1.00 / 1.00 | fixed: random reads it too |
| Qwen3.5-9B | main (400 rows, 43 bridges) | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is under-represented in the lens directions | 1.00 / 0.99 / 0.99 / 0.99 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-9B | json (620 rows, 32 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.57 / 0.34 / 0.32 / 0.40 / 0.52 / 0.53 | full < 0.8 |
| Qwen3.5-9B | json (620 rows, 32 bridges) | B | (b) its locker slot | 100 | in between | in between | in between | 0.57 / 0.50 / 0.36 / 0.45 / 0.54 / 0.53 | full < 0.8 |
| Qwen3.5-9B | json (620 rows, 32 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.17 / 0.12 / 0.13 / 0.13 / 0.16 / 0.10 | full < 0.8 |
| Qwen3.5-9B | json (620 rows, 32 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.17 / 0.13 / 0.12 / 0.15 / 0.16 / 0.16 | full < 0.8 |
| Qwen3.5-9B | json (620 rows, 32 bridges) | T | (b) its locker slot | 25 | in between | in between | in between | 0.56 / 0.41 / 0.43 / 0.43 / 0.54 / 0.54 | full < 0.8 |
| Qwen3.5-9B | json (620 rows, 32 bridges) | T | (b) its locker slot | 100 | in between | in between | in between | 0.56 / 0.47 / 0.48 / 0.50 / 0.56 / 0.51 | full < 0.8 |
| Qwen3.5-9B | json (620 rows, 32 bridges) | T | (c) lookup's digit | 25 | in between | the lookup's answer digit is linearly decodable from many subspaces, J++ included | in between | 0.93 / 0.91 / 0.83 / 0.84 / 0.92 / 0.92 | fixed: random reads it too |
| Qwen3.5-9B | json (620 rows, 32 bridges) | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | in between | 0.93 / 0.92 / 0.89 / 0.91 / 0.92 / 0.91 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.6-27B | main (400 rows, 45 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.73 / 0.64 / 0.59 / 0.61 / 0.70 / 0.73 | full < 0.8 |
| Qwen3.6-27B | main (400 rows, 45 bridges) | B | (b) its locker slot | 100 | in between | in between | in between | 0.73 / 0.70 / 0.64 / 0.67 / 0.72 / 0.72 | full < 0.8 |
| Qwen3.6-27B | main (400 rows, 45 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.26 / 0.18 / 0.14 / 0.13 / 0.18 / 0.13 | full < 0.8 |
| Qwen3.6-27B | main (400 rows, 45 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.26 / 0.14 / 0.15 / 0.14 / 0.20 / 0.18 | full < 0.8 |
| Qwen3.6-27B | main (400 rows, 45 bridges) | T | (b) its locker slot | 25 | in between | the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it | the address is under-represented in the lens directions | 0.99 / 0.78 / 0.83 / 0.81 / 0.95 / 0.92 | fixed: random reads it too |
| Qwen3.6-27B | main (400 rows, 45 bridges) | T | (b) its locker slot | 100 | in between | the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it | the address is under-represented in the lens directions | 0.99 / 0.85 / 0.92 / 0.92 / 0.98 / 0.98 | fixed: random reads it too |
| Qwen3.6-27B | main (400 rows, 45 bridges) | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | in between | in between | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too |
| Qwen3.6-27B | main (400 rows, 45 bridges) | T | (c) lookup's digit | 100 | in between | in between | in between | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Qwen3.6-27B | json (620 rows, 32 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.60 / 0.38 / 0.36 / 0.42 / 0.54 / 0.54 | full < 0.8 |
| Qwen3.6-27B | json (620 rows, 32 bridges) | B | (b) its locker slot | 100 | in between | in between | in between | 0.60 / 0.50 / 0.43 / 0.47 / 0.57 / 0.54 | full < 0.8 |
| Qwen3.6-27B | json (620 rows, 32 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.23 / 0.14 / 0.12 / 0.13 / 0.18 / 0.11 | full < 0.8 |
| Qwen3.6-27B | json (620 rows, 32 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.23 / 0.17 / 0.15 / 0.16 / 0.19 / 0.19 | full < 0.8 |
| Qwen3.6-27B | json (620 rows, 32 bridges) | T | (b) its locker slot | 25 | in between | in between | in between | 0.74 / 0.47 / 0.50 / 0.53 / 0.67 / 0.61 | full < 0.8 |
| Qwen3.6-27B | json (620 rows, 32 bridges) | T | (b) its locker slot | 100 | in between | in between | in between | 0.74 / 0.58 / 0.62 / 0.62 / 0.71 / 0.70 | full < 0.8 |
| Qwen3.6-27B | json (620 rows, 32 bridges) | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | in between | 1.00 / 1.00 / 1.00 / 0.99 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.6-27B | json (620 rows, 32 bridges) | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | in between | in between | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.71 / 0.59 / 0.54 / 0.57 / 0.69 / 0.69 | full < 0.8 |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | B | (b) its locker slot | 100 | in between | in between | in between | 0.71 / 0.68 / 0.61 / 0.61 / 0.70 / 0.70 | full < 0.8 |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.14 / 0.15 / 0.14 / 0.14 / 0.13 / 0.14 | full < 0.8 |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.14 / 0.15 / 0.14 / 0.13 / 0.12 / 0.13 | full < 0.8 |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | T | (b) its locker slot | 25 | J-space blind to X | in between | the address is under-represented in the lens directions | 0.94 / 0.69 / 0.70 / 0.69 / 0.89 / 0.85 |  |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | T | (b) its locker slot | 100 | in between | the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it | the address is under-represented in the lens directions | 0.94 / 0.80 / 0.81 / 0.83 / 0.93 / 0.91 | fixed: random reads it too |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | T | (c) lookup's digit | 25 | in between | in between | the lookup's answer digit is under-represented in the lens directions | 1.00 / 0.99 / 0.98 / 0.98 / 0.99 / 1.00 |  |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | in between | 1.00 / 1.00 / 0.99 / 1.00 / 1.00 / 0.99 | decisive: random reads it too; fixed: random reads it too |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.58 / 0.38 / 0.32 / 0.38 / 0.52 / 0.53 | full < 0.8 |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | B | (b) its locker slot | 100 | in between | in between | in between | 0.58 / 0.50 / 0.36 / 0.45 / 0.54 / 0.53 | full < 0.8 |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.28 / 0.14 / 0.13 / 0.14 / 0.20 / 0.13 | full < 0.8 |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.28 / 0.19 / 0.16 / 0.17 / 0.22 / 0.23 | full < 0.8 |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | T | (b) its locker slot | 25 | in between | in between | in between | 0.64 / 0.43 / 0.44 / 0.47 / 0.59 / 0.57 | full < 0.8 |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | T | (b) its locker slot | 100 | in between | in between | in between | 0.64 / 0.53 / 0.55 / 0.56 / 0.62 / 0.59 | full < 0.8 |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | T | (c) lookup's digit | 25 | in between | in between | the lookup's answer digit is under-represented in the lens directions | 0.99 / 0.99 / 0.99 / 0.99 / 1.00 / 0.99 |  |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is under-represented in the lens directions | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.99 | decisive: random reads it too; fixed: random reads it too |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.65 / 0.54 / 0.57 / 0.54 / 0.62 / 0.67 | full < 0.8 |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | B | (b) its locker slot | 100 | in between | in between | in between | 0.65 / 0.64 / 0.57 / 0.60 / 0.64 / 0.66 | full < 0.8 |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.12 / 0.15 / 0.14 / 0.13 / 0.13 / 0.12 | full < 0.8 |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.12 / 0.14 / 0.13 / 0.13 / 0.13 / 0.14 | full < 0.8 |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | T | (b) its locker slot | 25 | in between | J-space blind to X | the address is under-represented in the lens directions | 0.96 / 0.65 / 0.66 / 0.69 / 0.89 / 0.82 |  |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | T | (b) its locker slot | 100 | in between | the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it | the address is under-represented in the lens directions | 0.96 / 0.79 / 0.82 / 0.81 / 0.94 / 0.94 | fixed: random reads it too |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 0.99 / 0.98 / 0.97 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.57 / 0.41 / 0.37 / 0.37 / 0.51 / 0.52 | full < 0.8 |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | B | (b) its locker slot | 100 | in between | in between | no different from random directions of the same energy | 0.57 / 0.51 / 0.40 / 0.42 / 0.54 / 0.51 | full < 0.8 |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.20 / 0.13 / 0.12 / 0.12 / 0.17 / 0.10 | full < 0.8 |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.20 / 0.15 / 0.16 / 0.15 / 0.18 / 0.18 | full < 0.8 |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | T | (b) its locker slot | 25 | in between | in between | in between | 0.58 / 0.43 / 0.41 / 0.41 / 0.53 / 0.49 | full < 0.8 |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | T | (b) its locker slot | 100 | in between | in between | in between | 0.58 / 0.50 / 0.47 / 0.46 / 0.56 / 0.52 | full < 0.8 |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | T | (c) lookup's digit | 25 | in between | the lookup's answer digit is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 0.89 / 0.89 / 0.84 / 0.83 / 0.88 / 0.88 | fixed: random reads it too |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 0.89 / 0.90 / 0.86 / 0.87 / 0.89 / 0.88 | decisive: random reads it too; fixed: random reads it too |

Each decisive label at one layer (carries: the first layer with J++ >= 0.8 and J++ - random >= 0.3; otherwise the layer where the full residual peaks). Accuracy [95% CI].

| model | dataset | position | target | k | decisive label | layer | full | J++ | random | fixed J++ | e-random | PCA | chance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | main | B | (b) its locker slot | 25 | in between | L16 | 0.71 [0.67, 0.76] | 0.61 [0.57, 0.66] | 0.61 [0.57, 0.65] | 0.58 [0.53, 0.63] | 0.68 [0.65, 0.72] | 0.72 [0.68, 0.76] | 0.36 [0.31, 0.41] |
| Qwen3.5-9B | main | B | (b) its locker slot | 100 | in between | L16 | 0.71 [0.67, 0.76] | 0.71 [0.68, 0.74] | 0.64 [0.60, 0.68] | 0.62 [0.59, 0.65] | 0.69 [0.66, 0.73] | 0.71 [0.67, 0.75] | 0.36 [0.31, 0.41] |
| Qwen3.5-9B | main | B | (c) lookup's digit | 25 | in between | L0 | 0.13 [0.11, 0.16] | 0.10 [0.08, 0.13] | 0.12 [0.10, 0.14] | 0.12 [0.10, 0.14] | 0.12 [0.10, 0.14] | 0.14 [0.11, 0.17] | 0.12 [0.09, 0.15] |
| Qwen3.5-9B | main | B | (c) lookup's digit | 100 | in between | L0 | 0.13 [0.11, 0.16] | 0.12 [0.10, 0.14] | 0.12 [0.11, 0.14] | 0.12 [0.10, 0.15] | 0.12 [0.10, 0.13] | 0.12 [0.10, 0.14] | 0.12 [0.09, 0.15] |
| Qwen3.5-9B | main | T | (b) its locker slot | 25 | J-space blind to X | L20 | 0.88 [0.84, 0.91] | 0.60 [0.56, 0.64] | 0.65 [0.62, 0.68] | 0.64 [0.60, 0.68] | 0.83 [0.80, 0.86] | 0.77 [0.73, 0.80] | 0.36 [0.31, 0.41] |
| Qwen3.5-9B | main | T | (b) its locker slot | 100 | in between | L20 | 0.88 [0.84, 0.91] | 0.72 [0.69, 0.76] | 0.77 [0.74, 0.81] | 0.72 [0.68, 0.76] | 0.86 [0.83, 0.89] | 0.82 [0.78, 0.85] | 0.36 [0.31, 0.41] |
| Qwen3.5-9B | main | T | (c) lookup's digit | 25 | in between | L30 | 1.00 [0.99, 1.00] | 0.94 [0.92, 0.96] | 0.94 [0.93, 0.96] | 0.86 [0.84, 0.89] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.12 [0.09, 0.15] |
| Qwen3.5-9B | main | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L30 | 1.00 [0.99, 1.00] | 0.99 [0.98, 1.00] | 0.99 [0.99, 1.00] | 0.99 [0.98, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.12 [0.09, 0.15] |
| Qwen3.5-9B | json | B | (b) its locker slot | 25 | in between | L16 | 0.57 [0.53, 0.61] | 0.34 [0.30, 0.37] | 0.40 [0.36, 0.44] | 0.24 [0.20, 0.27] | 0.52 [0.48, 0.56] | 0.53 [0.49, 0.56] | 0.19 [0.16, 0.22] |
| Qwen3.5-9B | json | B | (b) its locker slot | 100 | in between | L16 | 0.57 [0.53, 0.61] | 0.49 [0.44, 0.53] | 0.45 [0.42, 0.49] | 0.36 [0.32, 0.39] | 0.54 [0.51, 0.57] | 0.52 [0.49, 0.55] | 0.19 [0.16, 0.22] |
| Qwen3.5-9B | json | B | (c) lookup's digit | 25 | in between | L16 | 0.17 [0.15, 0.20] | 0.12 [0.10, 0.14] | 0.12 [0.10, 0.13] | 0.12 [0.10, 0.14] | 0.16 [0.14, 0.18] | 0.10 [0.08, 0.12] | 0.08 [0.06, 0.10] |
| Qwen3.5-9B | json | B | (c) lookup's digit | 100 | in between | L16 | 0.17 [0.15, 0.20] | 0.13 [0.11, 0.16] | 0.15 [0.13, 0.17] | 0.12 [0.10, 0.14] | 0.16 [0.14, 0.19] | 0.16 [0.13, 0.18] | 0.08 [0.06, 0.10] |
| Qwen3.5-9B | json | T | (b) its locker slot | 25 | in between | L22 | 0.56 [0.53, 0.59] | 0.41 [0.36, 0.44] | 0.43 [0.39, 0.46] | 0.43 [0.40, 0.46] | 0.54 [0.50, 0.57] | 0.54 [0.51, 0.58] | 0.19 [0.16, 0.22] |
| Qwen3.5-9B | json | T | (b) its locker slot | 100 | in between | L22 | 0.56 [0.53, 0.59] | 0.47 [0.44, 0.50] | 0.49 [0.46, 0.52] | 0.48 [0.44, 0.51] | 0.56 [0.53, 0.59] | 0.50 [0.46, 0.54] | 0.19 [0.16, 0.22] |
| Qwen3.5-9B | json | T | (c) lookup's digit | 25 | in between | L28 | 0.93 [0.90, 0.94] | 0.91 [0.89, 0.94] | 0.84 [0.82, 0.86] | 0.83 [0.80, 0.85] | 0.92 [0.89, 0.94] | 0.91 [0.89, 0.93] | 0.08 [0.06, 0.10] |
| Qwen3.5-9B | json | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L28 | 0.93 [0.90, 0.94] | 0.92 [0.90, 0.94] | 0.90 [0.88, 0.92] | 0.89 [0.87, 0.91] | 0.92 [0.90, 0.94] | 0.91 [0.88, 0.93] | 0.08 [0.06, 0.10] |
| Qwen3.6-27B | main | B | (b) its locker slot | 25 | in between | L22 | 0.73 [0.70, 0.77] | 0.51 [0.47, 0.55] | 0.49 [0.46, 0.52] | 0.45 [0.41, 0.48] | 0.65 [0.62, 0.69] | 0.61 [0.57, 0.65] | 0.35 [0.30, 0.40] |
| Qwen3.6-27B | main | B | (b) its locker slot | 100 | in between | L22 | 0.73 [0.70, 0.77] | 0.60 [0.56, 0.65] | 0.60 [0.57, 0.63] | 0.50 [0.46, 0.54] | 0.69 [0.66, 0.73] | 0.69 [0.65, 0.73] | 0.35 [0.30, 0.40] |
| Qwen3.6-27B | main | B | (c) lookup's digit | 25 | in between | L56 | 0.26 [0.22, 0.30] | 0.12 [0.09, 0.15] | 0.13 [0.11, 0.14] | 0.11 [0.09, 0.14] | 0.18 [0.15, 0.20] | 0.11 [0.08, 0.14] | 0.10 [0.07, 0.14] |
| Qwen3.6-27B | main | B | (c) lookup's digit | 100 | in between | L56 | 0.26 [0.22, 0.30] | 0.12 [0.09, 0.14] | 0.12 [0.11, 0.14] | 0.15 [0.11, 0.18] | 0.20 [0.17, 0.23] | 0.17 [0.14, 0.20] | 0.10 [0.07, 0.14] |
| Qwen3.6-27B | main | T | (b) its locker slot | 25 | in between | L48 | 0.99 [0.98, 1.00] | 0.77 [0.73, 0.80] | 0.81 [0.79, 0.84] | 0.81 [0.78, 0.84] | 0.95 [0.94, 0.96] | 0.91 [0.89, 0.94] | 0.35 [0.30, 0.40] |
| Qwen3.6-27B | main | T | (b) its locker slot | 100 | in between | L48 | 0.99 [0.98, 1.00] | 0.85 [0.82, 0.88] | 0.92 [0.90, 0.94] | 0.90 [0.87, 0.92] | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.35 [0.30, 0.40] |
| Qwen3.6-27B | main | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L52 | 1.00 [1.00, 1.00] | 0.96 [0.95, 0.98] | 0.95 [0.94, 0.96] | 0.96 [0.94, 0.97] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.10 [0.07, 0.14] |
| Qwen3.6-27B | main | T | (c) lookup's digit | 100 | in between | L52 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.10 [0.07, 0.14] |
| Qwen3.6-27B | json | B | (b) its locker slot | 25 | in between | L36 | 0.60 [0.56, 0.63] | 0.37 [0.33, 0.41] | 0.42 [0.39, 0.46] | 0.35 [0.31, 0.39] | 0.53 [0.50, 0.56] | 0.53 [0.49, 0.57] | 0.19 [0.16, 0.22] |
| Qwen3.6-27B | json | B | (b) its locker slot | 100 | in between | L36 | 0.60 [0.56, 0.63] | 0.49 [0.46, 0.53] | 0.47 [0.45, 0.50] | 0.43 [0.39, 0.46] | 0.56 [0.53, 0.59] | 0.54 [0.50, 0.58] | 0.19 [0.16, 0.22] |
| Qwen3.6-27B | json | B | (c) lookup's digit | 25 | in between | L36 | 0.23 [0.20, 0.27] | 0.11 [0.09, 0.13] | 0.13 [0.11, 0.15] | 0.11 [0.09, 0.14] | 0.17 [0.16, 0.19] | 0.11 [0.09, 0.13] | 0.08 [0.06, 0.10] |
| Qwen3.6-27B | json | B | (c) lookup's digit | 100 | in between | L36 | 0.23 [0.20, 0.27] | 0.14 [0.11, 0.16] | 0.15 [0.14, 0.17] | 0.15 [0.12, 0.18] | 0.19 [0.17, 0.22] | 0.19 [0.17, 0.23] | 0.08 [0.06, 0.10] |
| Qwen3.6-27B | json | T | (b) its locker slot | 25 | in between | L48 | 0.74 [0.70, 0.78] | 0.46 [0.43, 0.50] | 0.52 [0.48, 0.55] | 0.46 [0.43, 0.49] | 0.67 [0.64, 0.70] | 0.61 [0.57, 0.65] | 0.19 [0.16, 0.22] |
| Qwen3.6-27B | json | T | (b) its locker slot | 100 | in between | L48 | 0.74 [0.70, 0.78] | 0.58 [0.54, 0.62] | 0.62 [0.59, 0.65] | 0.60 [0.56, 0.64] | 0.71 [0.68, 0.74] | 0.70 [0.66, 0.74] | 0.19 [0.16, 0.22] |
| Qwen3.6-27B | json | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L52 | 1.00 [0.99, 1.00] | 0.98 [0.97, 0.99] | 0.94 [0.93, 0.95] | 0.95 [0.93, 0.96] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.08 [0.06, 0.10] |
| Qwen3.6-27B | json | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L52 | 1.00 [0.99, 1.00] | 0.99 [0.98, 1.00] | 0.99 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.08 [0.06, 0.10] |
| Muse-Glimmer-30B | main | B | (b) its locker slot | 25 | in between | L14 | 0.71 [0.66, 0.75] | 0.48 [0.44, 0.53] | 0.49 [0.46, 0.52] | 0.46 [0.41, 0.50] | 0.67 [0.63, 0.71] | 0.63 [0.59, 0.68] | 0.33 [0.29, 0.37] |
| Muse-Glimmer-30B | main | B | (b) its locker slot | 100 | in between | L14 | 0.71 [0.66, 0.75] | 0.60 [0.56, 0.64] | 0.56 [0.52, 0.60] | 0.52 [0.49, 0.55] | 0.68 [0.64, 0.72] | 0.69 [0.65, 0.73] | 0.33 [0.29, 0.37] |
| Muse-Glimmer-30B | main | B | (c) lookup's digit | 25 | in between | L44 | 0.14 [0.12, 0.16] | 0.12 [0.10, 0.14] | 0.14 [0.12, 0.16] | 0.12 [0.10, 0.14] | 0.13 [0.11, 0.14] | 0.13 [0.10, 0.15] | 0.13 [0.10, 0.17] |
| Muse-Glimmer-30B | main | B | (c) lookup's digit | 100 | in between | L44 | 0.14 [0.12, 0.16] | 0.12 [0.09, 0.16] | 0.13 [0.11, 0.14] | 0.13 [0.11, 0.15] | 0.12 [0.10, 0.13] | 0.13 [0.11, 0.15] | 0.13 [0.10, 0.17] |
| Muse-Glimmer-30B | main | T | (b) its locker slot | 25 | J-space blind to X | L34 | 0.94 [0.92, 0.95] | 0.68 [0.65, 0.71] | 0.69 [0.66, 0.72] | 0.68 [0.63, 0.72] | 0.89 [0.86, 0.91] | 0.83 [0.80, 0.86] | 0.33 [0.29, 0.37] |
| Muse-Glimmer-30B | main | T | (b) its locker slot | 100 | in between | L34 | 0.94 [0.92, 0.95] | 0.80 [0.76, 0.83] | 0.83 [0.80, 0.86] | 0.80 [0.77, 0.84] | 0.92 [0.90, 0.94] | 0.89 [0.86, 0.92] | 0.33 [0.29, 0.37] |
| Muse-Glimmer-30B | main | T | (c) lookup's digit | 25 | in between | L40 | 1.00 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.95 [0.94, 0.96] | 0.95 [0.93, 0.97] | 0.99 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.13 [0.10, 0.17] |
| Muse-Glimmer-30B | main | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L40 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.99 [0.98, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.98, 1.00] | 0.13 [0.10, 0.17] |
| Muse-Glimmer-30B | json | B | (b) its locker slot | 25 | in between | L16 | 0.58 [0.54, 0.62] | 0.28 [0.25, 0.31] | 0.32 [0.29, 0.35] | 0.22 [0.19, 0.25] | 0.52 [0.48, 0.56] | 0.50 [0.46, 0.54] | 0.18 [0.16, 0.20] |
| Muse-Glimmer-30B | json | B | (b) its locker slot | 100 | in between | L16 | 0.58 [0.54, 0.62] | 0.45 [0.42, 0.49] | 0.40 [0.36, 0.44] | 0.30 [0.27, 0.33] | 0.54 [0.50, 0.58] | 0.51 [0.46, 0.55] | 0.18 [0.16, 0.20] |
| Muse-Glimmer-30B | json | B | (c) lookup's digit | 25 | in between | L28 | 0.28 [0.24, 0.31] | 0.14 [0.12, 0.16] | 0.13 [0.12, 0.15] | 0.13 [0.11, 0.14] | 0.20 [0.18, 0.22] | 0.13 [0.11, 0.15] | 0.08 [0.07, 0.10] |
| Muse-Glimmer-30B | json | B | (c) lookup's digit | 100 | in between | L28 | 0.28 [0.24, 0.31] | 0.19 [0.16, 0.22] | 0.17 [0.15, 0.19] | 0.16 [0.13, 0.19] | 0.22 [0.20, 0.25] | 0.23 [0.20, 0.26] | 0.08 [0.07, 0.10] |
| Muse-Glimmer-30B | json | T | (b) its locker slot | 25 | in between | L32 | 0.64 [0.61, 0.68] | 0.43 [0.40, 0.46] | 0.47 [0.43, 0.50] | 0.44 [0.40, 0.48] | 0.59 [0.56, 0.62] | 0.57 [0.53, 0.60] | 0.18 [0.16, 0.20] |
| Muse-Glimmer-30B | json | T | (b) its locker slot | 100 | in between | L32 | 0.64 [0.61, 0.68] | 0.53 [0.49, 0.56] | 0.56 [0.53, 0.59] | 0.55 [0.51, 0.58] | 0.62 [0.58, 0.65] | 0.59 [0.56, 0.62] | 0.18 [0.16, 0.20] |
| Muse-Glimmer-30B | json | T | (c) lookup's digit | 25 | in between | L36 | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.97 [0.96, 0.98] | 0.97 [0.96, 0.97] | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.08 [0.07, 0.10] |
| Muse-Glimmer-30B | json | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L36 | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.08 [0.07, 0.10] |
| Nemotron-3.5-Lightning | main | B | (b) its locker slot | 25 | in between | L24 | 0.65 [0.61, 0.69] | 0.54 [0.51, 0.58] | 0.54 [0.51, 0.58] | 0.57 [0.53, 0.62] | 0.61 [0.59, 0.64] | 0.65 [0.60, 0.69] | 0.35 [0.30, 0.39] |
| Nemotron-3.5-Lightning | main | B | (b) its locker slot | 100 | in between | L24 | 0.65 [0.61, 0.69] | 0.64 [0.61, 0.68] | 0.60 [0.57, 0.63] | 0.57 [0.53, 0.61] | 0.64 [0.61, 0.68] | 0.65 [0.62, 0.69] | 0.35 [0.30, 0.39] |
| Nemotron-3.5-Lightning | main | B | (c) lookup's digit | 25 | in between | L20 | 0.12 [0.09, 0.15] | 0.12 [0.10, 0.15] | 0.10 [0.09, 0.12] | 0.12 [0.10, 0.14] | 0.11 [0.08, 0.13] | 0.09 [0.07, 0.12] | 0.10 [0.08, 0.12] |
| Nemotron-3.5-Lightning | main | B | (c) lookup's digit | 100 | in between | L20 | 0.12 [0.09, 0.15] | 0.12 [0.10, 0.15] | 0.12 [0.10, 0.14] | 0.11 [0.09, 0.13] | 0.13 [0.10, 0.16] | 0.14 [0.11, 0.16] | 0.10 [0.08, 0.12] |
| Nemotron-3.5-Lightning | main | T | (b) its locker slot | 25 | in between | L34 | 0.96 [0.94, 0.97] | 0.65 [0.61, 0.69] | 0.64 [0.61, 0.66] | 0.59 [0.55, 0.63] | 0.88 [0.86, 0.90] | 0.82 [0.79, 0.86] | 0.35 [0.30, 0.39] |
| Nemotron-3.5-Lightning | main | T | (b) its locker slot | 100 | in between | L34 | 0.96 [0.94, 0.97] | 0.79 [0.75, 0.83] | 0.80 [0.78, 0.84] | 0.82 [0.79, 0.86] | 0.94 [0.92, 0.95] | 0.94 [0.92, 0.96] | 0.35 [0.30, 0.39] |
| Nemotron-3.5-Lightning | main | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L34 | 1.00 [1.00, 1.00] | 0.99 [0.99, 1.00] | 0.91 [0.90, 0.93] | 0.96 [0.95, 0.98] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.10 [0.08, 0.12] |
| Nemotron-3.5-Lightning | main | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L34 | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.10 [0.08, 0.12] |
| Nemotron-3.5-Lightning | json | B | (b) its locker slot | 25 | in between | L20 | 0.57 [0.52, 0.61] | 0.41 [0.38, 0.44] | 0.37 [0.34, 0.41] | 0.30 [0.26, 0.34] | 0.51 [0.46, 0.55] | 0.52 [0.48, 0.55] | 0.20 [0.17, 0.22] |
| Nemotron-3.5-Lightning | json | B | (b) its locker slot | 100 | in between | L20 | 0.57 [0.52, 0.61] | 0.51 [0.48, 0.54] | 0.42 [0.39, 0.45] | 0.39 [0.36, 0.43] | 0.54 [0.50, 0.58] | 0.51 [0.47, 0.55] | 0.20 [0.17, 0.22] |
| Nemotron-3.5-Lightning | json | B | (c) lookup's digit | 25 | in between | L20 | 0.20 [0.18, 0.22] | 0.12 [0.10, 0.14] | 0.12 [0.11, 0.13] | 0.12 [0.10, 0.14] | 0.16 [0.14, 0.18] | 0.09 [0.08, 0.11] | 0.09 [0.08, 0.11] |
| Nemotron-3.5-Lightning | json | B | (c) lookup's digit | 100 | in between | L20 | 0.20 [0.18, 0.22] | 0.14 [0.12, 0.16] | 0.15 [0.14, 0.16] | 0.13 [0.12, 0.15] | 0.18 [0.16, 0.20] | 0.18 [0.16, 0.20] | 0.09 [0.08, 0.11] |
| Nemotron-3.5-Lightning | json | T | (b) its locker slot | 25 | in between | L34 | 0.58 [0.55, 0.61] | 0.43 [0.40, 0.46] | 0.40 [0.37, 0.43] | 0.34 [0.32, 0.37] | 0.53 [0.50, 0.56] | 0.46 [0.43, 0.50] | 0.20 [0.17, 0.22] |
| Nemotron-3.5-Lightning | json | T | (b) its locker slot | 100 | in between | L34 | 0.58 [0.55, 0.61] | 0.50 [0.48, 0.53] | 0.46 [0.43, 0.48] | 0.45 [0.43, 0.48] | 0.55 [0.52, 0.59] | 0.52 [0.49, 0.55] | 0.20 [0.17, 0.22] |
| Nemotron-3.5-Lightning | json | T | (c) lookup's digit | 25 | in between | L44 | 0.89 [0.86, 0.91] | 0.89 [0.86, 0.91] | 0.81 [0.78, 0.83] | 0.83 [0.80, 0.85] | 0.88 [0.85, 0.90] | 0.88 [0.85, 0.91] | 0.09 [0.08, 0.11] |
| Nemotron-3.5-Lightning | json | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L44 | 0.89 [0.86, 0.91] | 0.90 [0.87, 0.92] | 0.86 [0.83, 0.88] | 0.86 [0.84, 0.88] | 0.88 [0.86, 0.91] | 0.88 [0.85, 0.90] | 0.09 [0.08, 0.11] |

### Positive controls: (a) which item is the bridge and (d) the recall's answer

| model | dataset | position | target | k | decisive: J++ (per state) vs random | beside: fixed J++ vs random | beside: J++ vs energy-matched random (Dan 13:15) | full / J++ / fixed / random / e-random / PCA max | notes |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | main (400 rows, 43 bridges) | B | (a) which item | 25 | in between | in between | no different from random directions of the same energy | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.98 |  |
| Qwen3.5-9B | main (400 rows, 43 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | which item is the bridge is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.99 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-9B | main (400 rows, 43 bridges) | B | (d) recall's answer | 25 | J-space carries X | in between | no different from random directions of the same energy | 1.00 / 1.00 / 0.98 / 0.98 / 1.00 / 0.99 |  |
| Qwen3.5-9B | main (400 rows, 43 bridges) | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 0.99 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-9B | main (400 rows, 43 bridges) | T | (a) which item | 25 | in between | in between | in between | 0.80 / 0.55 / 0.51 / 0.45 / 0.76 / 0.65 | full < 0.8 |
| Qwen3.5-9B | main (400 rows, 43 bridges) | T | (a) which item | 100 | in between | in between | in between | 0.80 / 0.61 / 0.76 / 0.69 / 0.78 / 0.83 | full < 0.8 |
| Qwen3.5-9B | main (400 rows, 43 bridges) | T | (d) recall's answer | 25 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 1.00 / 1.00 / 1.00 / 0.99 / 1.00 / 1.00 | fixed: random reads it too |
| Qwen3.5-9B | main (400 rows, 43 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | fixed: random reads it too |
| Qwen3.5-9B | json (620 rows, 32 bridges) | B | (a) which item | 25 | in between | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Qwen3.5-9B | json (620 rows, 32 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | which item is the bridge is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-9B | json (620 rows, 32 bridges) | B | (d) recall's answer | 25 | in between | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Qwen3.5-9B | json (620 rows, 32 bridges) | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-9B | json (620 rows, 32 bridges) | T | (a) which item | 25 | in between | in between | which item is the bridge is under-represented in the lens directions | 0.88 / 0.77 / 0.47 / 0.49 / 0.85 / 0.71 |  |
| Qwen3.5-9B | json (620 rows, 32 bridges) | T | (a) which item | 100 | in between | J-space blind to X | which item is the bridge is under-represented in the lens directions | 0.88 / 0.79 / 0.76 / 0.77 / 0.86 / 0.89 |  |
| Qwen3.5-9B | json (620 rows, 32 bridges) | T | (d) recall's answer | 25 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | in between | 0.94 / 0.94 / 0.93 / 0.92 / 0.94 / 0.94 | fixed: random reads it too |
| Qwen3.5-9B | json (620 rows, 32 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | in between | 0.94 / 0.94 / 0.94 / 0.94 / 0.94 / 0.94 | fixed: random reads it too |
| Qwen3.6-27B | main (400 rows, 45 bridges) | B | (a) which item | 25 | J-space carries X | in between | no different from random directions of the same energy | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.99 |  |
| Qwen3.6-27B | main (400 rows, 45 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | in between | no different from random directions of the same energy | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.99 | decisive: random reads it too |
| Qwen3.6-27B | main (400 rows, 45 bridges) | B | (d) recall's answer | 25 | J-space carries X | in between | no different from random directions of the same energy | 1.00 / 1.00 / 0.98 / 0.97 / 1.00 / 1.00 |  |
| Qwen3.6-27B | main (400 rows, 45 bridges) | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too |
| Qwen3.6-27B | main (400 rows, 45 bridges) | T | (a) which item | 25 | in between | in between | in between | 0.74 / 0.49 / 0.36 / 0.31 / 0.67 / 0.50 | full < 0.8 |
| Qwen3.6-27B | main (400 rows, 45 bridges) | T | (a) which item | 100 | in between | in between | in between | 0.74 / 0.50 / 0.62 / 0.58 / 0.70 / 0.79 | full < 0.8 |
| Qwen3.6-27B | main (400 rows, 45 bridges) | T | (d) recall's answer | 25 | in between | in between | in between | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Qwen3.6-27B | main (400 rows, 45 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | in between | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | fixed: random reads it too |
| Qwen3.6-27B | json (620 rows, 32 bridges) | B | (a) which item | 25 | in between | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Qwen3.6-27B | json (620 rows, 32 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | which item is the bridge is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.6-27B | json (620 rows, 32 bridges) | B | (d) recall's answer | 25 | J-space carries X | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Qwen3.6-27B | json (620 rows, 32 bridges) | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.6-27B | json (620 rows, 32 bridges) | T | (a) which item | 25 | in between | J-space blind to X | which item is the bridge is under-represented in the lens directions | 0.82 / 0.49 / 0.55 / 0.47 / 0.76 / 0.69 |  |
| Qwen3.6-27B | json (620 rows, 32 bridges) | T | (a) which item | 100 | in between | J-space blind to X | which item is the bridge is under-represented in the lens directions | 0.82 / 0.64 / 0.78 / 0.71 / 0.79 / 0.80 |  |
| Qwen3.6-27B | json (620 rows, 32 bridges) | T | (d) recall's answer | 25 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.99 | fixed: random reads it too |
| Qwen3.6-27B | json (620 rows, 32 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | in between | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.99 | fixed: random reads it too |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | B | (a) which item | 25 | in between | in between | no different from random directions of the same energy | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.97 |  |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | in between | no different from random directions of the same energy | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.99 | decisive: random reads it too |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | B | (d) recall's answer | 25 | J-space carries X | in between | no different from random directions of the same energy | 1.00 / 1.00 / 0.98 / 0.99 / 1.00 / 1.00 |  |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | B | (d) recall's answer | 100 | in between | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | T | (a) which item | 25 | in between | in between | in between | 0.59 / 0.28 / 0.25 / 0.27 / 0.51 / 0.46 | full < 0.8 |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | T | (a) which item | 100 | in between | in between | in between | 0.59 / 0.36 / 0.44 / 0.44 / 0.55 / 0.58 | full < 0.8 |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | T | (d) recall's answer | 25 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 1.00 / 1.00 / 1.00 / 0.99 / 1.00 / 1.00 | fixed: random reads it too |
| Muse-Glimmer-30B | main (400 rows, 44 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | fixed: random reads it too |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | B | (a) which item | 25 | in between | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | which item is the bridge is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | B | (d) recall's answer | 25 | J-space carries X | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | T | (a) which item | 25 | in between | J-space blind to X | which item is the bridge is under-represented in the lens directions | 0.86 / 0.30 / 0.33 / 0.37 / 0.77 / 0.62 |  |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | T | (a) which item | 100 | in between | J-space blind to X | which item is the bridge is under-represented in the lens directions | 0.86 / 0.46 / 0.60 / 0.62 / 0.82 / 0.84 |  |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | T | (d) recall's answer | 25 | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 0.99 / 0.99 / 0.99 / 0.98 / 0.99 / 0.99 | decisive: random reads it too; fixed: random reads it too |
| Muse-Glimmer-30B | json (776 rows, 35 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 1.00 | fixed: random reads it too |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | B | (a) which item | 25 | in between | in between | which item is the bridge is under-represented in the lens directions | 0.99 / 0.98 / 0.98 / 0.98 / 0.99 / 0.97 |  |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | which item is the bridge is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 0.99 / 0.99 / 0.99 / 0.99 / 0.99 / 0.99 | decisive: random reads it too; fixed: random reads it too |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | B | (d) recall's answer | 25 | J-space carries X | in between | the recall's answer is under-represented in the lens directions | 1.00 / 1.00 / 0.97 / 0.97 / 1.00 / 1.00 |  |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | T | (a) which item | 25 | in between | in between | in between | 0.68 / 0.51 / 0.26 / 0.28 / 0.61 / 0.42 | full < 0.8 |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | T | (a) which item | 100 | in between | in between | in between | 0.68 / 0.53 / 0.53 / 0.53 / 0.65 / 0.74 | full < 0.8 |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | T | (d) recall's answer | 25 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 1.00 / 1.00 / 1.00 / 0.99 / 1.00 / 1.00 | fixed: random reads it too |
| Nemotron-3.5-Lightning | main (400 rows, 43 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | fixed: random reads it too |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | B | (a) which item | 25 | in between | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | which item is the bridge is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | B | (d) recall's answer | 25 | J-space carries X | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | T | (a) which item | 25 | in between | J-space blind to X | which item is the bridge is under-represented in the lens directions | 0.93 / 0.80 / 0.45 / 0.46 / 0.89 / 0.76 |  |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | T | (a) which item | 100 | in between | which item is the bridge is linearly decodable from many subspaces, J++ included | which item is the bridge is under-represented in the lens directions | 0.93 / 0.86 / 0.79 / 0.81 / 0.91 / 0.93 | fixed: random reads it too |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | T | (d) recall's answer | 25 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 0.99 / 0.99 / 0.97 / 0.96 / 0.99 / 0.98 | fixed: random reads it too |
| Nemotron-3.5-Lightning | json (830 rows, 30 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 0.99 / 0.99 / 0.99 / 0.98 / 0.99 / 0.99 | fixed: random reads it too |

Each decisive label at one layer (carries: the first layer with J++ >= 0.8 and J++ - random >= 0.3; otherwise the layer where the full residual peaks). Accuracy [95% CI].

| model | dataset | position | target | k | decisive label | layer | full | J++ | random | fixed J++ | e-random | PCA | chance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | main | B | (a) which item | 25 | in between | L0 | 0.99 [0.97, 1.00] | 0.99 [0.97, 0.99] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.98 [0.97, 0.99] | 0.07 [0.00, 0.18] |
| Qwen3.5-9B | main | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.07 [0.00, 0.18] |
| Qwen3.5-9B | main | B | (d) recall's answer | 25 | J-space carries X | L14 | 0.96 [0.93, 0.98] | 0.98 [0.96, 0.99] | 0.68 [0.63, 0.71] | 0.88 [0.82, 0.92] | 0.97 [0.95, 0.98] | 0.89 [0.83, 0.93] | 0.20 [0.08, 0.36] |
| Qwen3.5-9B | main | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | L2 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.20 [0.08, 0.36] |
| Qwen3.5-9B | main | T | (a) which item | 25 | in between | L20 | 0.80 [0.70, 0.87] | 0.46 [0.35, 0.54] | 0.42 [0.32, 0.50] | 0.51 [0.41, 0.58] | 0.76 [0.65, 0.83] | 0.65 [0.52, 0.75] | 0.07 [0.00, 0.18] |
| Qwen3.5-9B | main | T | (a) which item | 100 | in between | L20 | 0.80 [0.70, 0.87] | 0.59 [0.46, 0.69] | 0.68 [0.56, 0.76] | 0.76 [0.66, 0.82] | 0.78 [0.68, 0.85] | 0.78 [0.68, 0.86] | 0.07 [0.00, 0.18] |
| Qwen3.5-9B | main | T | (d) recall's answer | 25 | in between | L24 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.98 [0.97, 0.99] | 0.99 [0.98, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.20 [0.08, 0.36] |
| Qwen3.5-9B | main | T | (d) recall's answer | 100 | in between | L24 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.98, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.20 [0.08, 0.36] |
| Qwen3.5-9B | json | B | (a) which item | 25 | in between | L0 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.09 [0.00, 0.25] |
| Qwen3.5-9B | json | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.09 [0.00, 0.25] |
| Qwen3.5-9B | json | B | (d) recall's answer | 25 | in between | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.25 [0.11, 0.46] |
| Qwen3.5-9B | json | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.25 [0.11, 0.46] |
| Qwen3.5-9B | json | T | (a) which item | 25 | in between | L30 | 0.88 [0.80, 0.92] | 0.77 [0.65, 0.83] | 0.49 [0.39, 0.55] | 0.38 [0.29, 0.44] | 0.85 [0.76, 0.90] | 0.71 [0.56, 0.80] | 0.09 [0.00, 0.25] |
| Qwen3.5-9B | json | T | (a) which item | 100 | in between | L30 | 0.88 [0.80, 0.92] | 0.79 [0.66, 0.86] | 0.77 [0.67, 0.83] | 0.76 [0.65, 0.83] | 0.86 [0.78, 0.91] | 0.89 [0.83, 0.93] | 0.09 [0.00, 0.25] |
| Qwen3.5-9B | json | T | (d) recall's answer | 25 | in between | L30 | 0.94 [0.93, 0.96] | 0.94 [0.92, 0.97] | 0.91 [0.89, 0.94] | 0.91 [0.89, 0.94] | 0.94 [0.92, 0.96] | 0.93 [0.92, 0.95] | 0.25 [0.11, 0.46] |
| Qwen3.5-9B | json | T | (d) recall's answer | 100 | in between | L30 | 0.94 [0.93, 0.96] | 0.94 [0.91, 0.96] | 0.94 [0.92, 0.96] | 0.94 [0.92, 0.96] | 0.94 [0.93, 0.96] | 0.94 [0.92, 0.96] | 0.25 [0.11, 0.46] |
| Qwen3.6-27B | main | B | (a) which item | 25 | J-space carries X | L32 | 0.81 [0.71, 0.87] | 0.92 [0.87, 0.95] | 0.60 [0.52, 0.66] | 0.87 [0.80, 0.92] | 0.89 [0.83, 0.93] | 0.75 [0.64, 0.83] | 0.05 [0.00, 0.15] |
| Qwen3.6-27B | main | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.05 [0.00, 0.15] |
| Qwen3.6-27B | main | B | (d) recall's answer | 25 | J-space carries X | L30 | 0.98 [0.96, 0.99] | 1.00 [0.99, 1.00] | 0.63 [0.57, 0.67] | 0.82 [0.74, 0.88] | 0.98 [0.96, 0.99] | 0.86 [0.80, 0.91] | 0.16 [0.09, 0.26] |
| Qwen3.6-27B | main | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | L10 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.16 [0.09, 0.26] |
| Qwen3.6-27B | main | T | (a) which item | 25 | in between | L62 | 0.74 [0.62, 0.82] | 0.49 [0.36, 0.59] | 0.30 [0.23, 0.35] | 0.27 [0.20, 0.33] | 0.67 [0.55, 0.75] | 0.45 [0.33, 0.55] | 0.05 [0.00, 0.15] |
| Qwen3.6-27B | main | T | (a) which item | 100 | in between | L62 | 0.74 [0.62, 0.82] | 0.50 [0.37, 0.60] | 0.58 [0.46, 0.67] | 0.53 [0.42, 0.62] | 0.70 [0.58, 0.78] | 0.79 [0.68, 0.86] | 0.05 [0.00, 0.15] |
| Qwen3.6-27B | main | T | (d) recall's answer | 25 | in between | L58 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.99 [0.98, 1.00] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.16 [0.09, 0.26] |
| Qwen3.6-27B | main | T | (d) recall's answer | 100 | in between | L58 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.16 [0.09, 0.26] |
| Qwen3.6-27B | json | B | (a) which item | 25 | in between | L0 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.09 [0.00, 0.25] |
| Qwen3.6-27B | json | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.09 [0.00, 0.25] |
| Qwen3.6-27B | json | B | (d) recall's answer | 25 | J-space carries X | L32 | 0.98 [0.96, 0.99] | 0.99 [0.98, 1.00] | 0.67 [0.61, 0.72] | 0.90 [0.83, 0.94] | 0.99 [0.97, 0.99] | 0.93 [0.88, 0.96] | 0.25 [0.11, 0.46] |
| Qwen3.6-27B | json | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.25 [0.11, 0.46] |
| Qwen3.6-27B | json | T | (a) which item | 25 | in between | L40 | 0.82 [0.74, 0.87] | 0.47 [0.36, 0.55] | 0.47 [0.38, 0.53] | 0.55 [0.46, 0.62] | 0.72 [0.64, 0.78] | 0.69 [0.60, 0.75] | 0.09 [0.00, 0.25] |
| Qwen3.6-27B | json | T | (a) which item | 100 | in between | L40 | 0.82 [0.74, 0.87] | 0.64 [0.52, 0.72] | 0.69 [0.60, 0.75] | 0.78 [0.72, 0.82] | 0.78 [0.70, 0.83] | 0.79 [0.70, 0.85] | 0.09 [0.00, 0.25] |
| Qwen3.6-27B | json | T | (d) recall's answer | 25 | in between | L56 | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.98 [0.98, 0.99] | 0.99 [0.98, 0.99] | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.25 [0.11, 0.46] |
| Qwen3.6-27B | json | T | (d) recall's answer | 100 | in between | L56 | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.99 [0.98, 1.00] | 0.99 [0.98, 1.00] | 0.99 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.25 [0.11, 0.46] |
| Muse-Glimmer-30B | main | B | (a) which item | 25 | in between | L0 | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.96 [0.93, 0.98] | 0.05 [0.01, 0.08] |
| Muse-Glimmer-30B | main | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.99 [0.97, 1.00] | 0.05 [0.01, 0.08] |
| Muse-Glimmer-30B | main | B | (d) recall's answer | 25 | J-space carries X | L18 | 0.98 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.68 [0.61, 0.73] | 0.87 [0.81, 0.92] | 1.00 [0.99, 1.00] | 0.93 [0.89, 0.95] | 0.17 [0.10, 0.28] |
| Muse-Glimmer-30B | main | B | (d) recall's answer | 100 | in between | L6 | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 0.17 [0.10, 0.28] |
| Muse-Glimmer-30B | main | T | (a) which item | 25 | in between | L34 | 0.59 [0.44, 0.68] | 0.26 [0.16, 0.33] | 0.27 [0.18, 0.33] | 0.23 [0.16, 0.29] | 0.51 [0.37, 0.60] | 0.41 [0.28, 0.50] | 0.05 [0.01, 0.08] |
| Muse-Glimmer-30B | main | T | (a) which item | 100 | in between | L34 | 0.59 [0.44, 0.68] | 0.36 [0.22, 0.45] | 0.44 [0.31, 0.53] | 0.44 [0.32, 0.53] | 0.55 [0.40, 0.64] | 0.57 [0.41, 0.67] | 0.05 [0.01, 0.08] |
| Muse-Glimmer-30B | main | T | (d) recall's answer | 25 | in between | L40 | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.98, 0.99] | 0.98 [0.96, 0.99] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.17 [0.10, 0.28] |
| Muse-Glimmer-30B | main | T | (d) recall's answer | 100 | in between | L40 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.17 [0.10, 0.28] |
| Muse-Glimmer-30B | json | B | (a) which item | 25 | in between | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 0.06 [0.00, 0.12] |
| Muse-Glimmer-30B | json | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.06 [0.00, 0.12] |
| Muse-Glimmer-30B | json | B | (d) recall's answer | 25 | J-space carries X | L20 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.68 [0.63, 0.72] | 0.96 [0.93, 0.98] | 1.00 [0.99, 1.00] | 0.97 [0.94, 0.99] | 0.23 [0.09, 0.40] |
| Muse-Glimmer-30B | json | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.23 [0.09, 0.40] |
| Muse-Glimmer-30B | json | T | (a) which item | 25 | in between | L48 | 0.86 [0.78, 0.91] | 0.26 [0.19, 0.32] | 0.28 [0.23, 0.31] | 0.26 [0.21, 0.30] | 0.76 [0.68, 0.82] | 0.48 [0.39, 0.56] | 0.06 [0.00, 0.12] |
| Muse-Glimmer-30B | json | T | (a) which item | 100 | in between | L48 | 0.86 [0.78, 0.91] | 0.43 [0.34, 0.50] | 0.62 [0.54, 0.67] | 0.60 [0.52, 0.66] | 0.82 [0.74, 0.87] | 0.84 [0.76, 0.89] | 0.06 [0.00, 0.12] |
| Muse-Glimmer-30B | json | T | (d) recall's answer | 25 | the recall's answer is linearly decodable from many subspaces, J++ included | L34 | 0.99 [0.99, 1.00] | 0.98 [0.97, 0.99] | 0.91 [0.87, 0.94] | 0.92 [0.88, 0.95] | 0.99 [0.99, 1.00] | 0.98 [0.96, 0.99] | 0.23 [0.09, 0.40] |
| Muse-Glimmer-30B | json | T | (d) recall's answer | 100 | in between | L34 | 0.99 [0.99, 1.00] | 0.99 [0.98, 1.00] | 0.99 [0.98, 0.99] | 0.99 [0.98, 0.99] | 0.99 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.23 [0.09, 0.40] |
| Nemotron-3.5-Lightning | main | B | (a) which item | 25 | in between | L0 | 0.99 [0.97, 0.99] | 0.97 [0.94, 0.98] | 0.98 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.99 [0.97, 0.99] | 0.97 [0.94, 0.99] | 0.04 [0.00, 0.11] |
| Nemotron-3.5-Lightning | main | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 0.99 [0.97, 0.99] | 0.99 [0.97, 0.99] | 0.99 [0.97, 0.99] | 0.99 [0.97, 0.99] | 0.99 [0.97, 0.99] | 0.99 [0.97, 0.99] | 0.04 [0.00, 0.11] |
| Nemotron-3.5-Lightning | main | B | (d) recall's answer | 25 | J-space carries X | L20 | 0.98 [0.96, 0.99] | 0.99 [0.97, 1.00] | 0.60 [0.53, 0.66] | 0.87 [0.81, 0.91] | 0.98 [0.97, 0.99] | 0.94 [0.91, 0.97] | 0.21 [0.08, 0.37] |
| Nemotron-3.5-Lightning | main | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | L38 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.99 [0.98, 0.99] | 0.99 [0.97, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.21 [0.08, 0.37] |
| Nemotron-3.5-Lightning | main | T | (a) which item | 25 | in between | L48 | 0.68 [0.57, 0.77] | 0.51 [0.39, 0.60] | 0.28 [0.22, 0.33] | 0.21 [0.15, 0.26] | 0.61 [0.49, 0.69] | 0.37 [0.27, 0.45] | 0.04 [0.00, 0.11] |
| Nemotron-3.5-Lightning | main | T | (a) which item | 100 | in between | L48 | 0.68 [0.57, 0.77] | 0.51 [0.39, 0.60] | 0.51 [0.41, 0.59] | 0.51 [0.40, 0.58] | 0.65 [0.54, 0.74] | 0.74 [0.64, 0.82] | 0.04 [0.00, 0.11] |
| Nemotron-3.5-Lightning | main | T | (d) recall's answer | 25 | in between | L34 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.89 [0.86, 0.91] | 0.88 [0.85, 0.91] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.21 [0.08, 0.37] |
| Nemotron-3.5-Lightning | main | T | (d) recall's answer | 100 | in between | L34 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.99 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.21 [0.08, 0.37] |
| Nemotron-3.5-Lightning | json | B | (a) which item | 25 | in between | L0 | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.05 [0.00, 0.14] |
| Nemotron-3.5-Lightning | json | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.05 [0.00, 0.14] |
| Nemotron-3.5-Lightning | json | B | (d) recall's answer | 25 | J-space carries X | L20 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.63 [0.58, 0.67] | 0.89 [0.86, 0.92] | 1.00 [0.99, 1.00] | 0.91 [0.87, 0.94] | 0.18 [0.06, 0.34] |
| Nemotron-3.5-Lightning | json | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.18 [0.06, 0.34] |
| Nemotron-3.5-Lightning | json | T | (a) which item | 25 | in between | L50 | 0.93 [0.89, 0.96] | 0.77 [0.71, 0.81] | 0.43 [0.38, 0.47] | 0.42 [0.34, 0.48] | 0.87 [0.81, 0.90] | 0.73 [0.65, 0.80] | 0.05 [0.00, 0.14] |
| Nemotron-3.5-Lightning | json | T | (a) which item | 100 | in between | L50 | 0.93 [0.89, 0.96] | 0.86 [0.79, 0.90] | 0.81 [0.75, 0.85] | 0.76 [0.69, 0.81] | 0.90 [0.85, 0.93] | 0.93 [0.89, 0.96] | 0.05 [0.00, 0.14] |
| Nemotron-3.5-Lightning | json | T | (d) recall's answer | 25 | in between | L46 | 0.99 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.95 [0.92, 0.96] | 0.97 [0.95, 0.98] | 0.99 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.18 [0.06, 0.34] |
| Nemotron-3.5-Lightning | json | T | (d) recall's answer | 100 | in between | L46 | 0.99 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.99 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.18 [0.06, 0.34] |


Not yet probed (a dataset or a pass missing): none.

## The main test's states vs 52 B's cache (lowest cosine over rows, any layer)

- Qwen3.5-9B: 1.00000 over 16 layers (B, T lookup, T recall)
- Qwen3.6-27B: 1.00000 over 32 layers (B, T lookup, T recall)
- Muse-Glimmer-30B: 1.00000 over 26 layers (B, T lookup, T recall)
- Nemotron-3.5-Lightning: 1.00000 over 26 layers (B, T lookup, T recall)

## Beside: each part's share of the state's squared norm (median over layers)

The J++ part is fit to each state (OMP picks the atoms that match it), the random subspace is fixed: the shares say how much of the state each feature keeps. The energy-matched random subspace's share and dimension (median over layers) beside.

| model | dataset | row set | J++25 | J++100 | random25 | random100 | e-random25 (dim) | e-random100 (dim) |
|---|---|---|---|---|---|---|---|---|
| Qwen3.5-9B | main | B | 0.099 | 0.183 | 0.006 | 0.024 | 0.095 (385) | 0.177 (727) |
| Qwen3.5-9B | main | T_lookup | 0.040 | 0.099 | 0.006 | 0.024 | 0.042 (165) | 0.101 (404) |
| Qwen3.5-9B | main | T_recall | 0.044 | 0.104 | 0.006 | 0.025 | 0.046 (171) | 0.103 (418) |
| Qwen3.5-9B | json | B | 0.087 | 0.163 | 0.006 | 0.025 | 0.081 (333) | 0.161 (640) |
| Qwen3.5-9B | json | T_lookup | 0.043 | 0.100 | 0.006 | 0.023 | 0.047 (175) | 0.107 (410) |
| Qwen3.5-9B | json | T_recall | 0.048 | 0.112 | 0.006 | 0.024 | 0.053 (201) | 0.115 (463) |
| Qwen3.6-27B | main | B | 0.064 | 0.140 | 0.005 | 0.020 | 0.064 (329) | 0.139 (711) |
| Qwen3.6-27B | main | T_lookup | 0.028 | 0.068 | 0.005 | 0.020 | 0.029 (145) | 0.070 (350) |
| Qwen3.6-27B | main | T_recall | 0.033 | 0.076 | 0.005 | 0.020 | 0.034 (170) | 0.075 (388) |
| Qwen3.6-27B | json | B | 0.055 | 0.125 | 0.005 | 0.020 | 0.049 (257) | 0.114 (576) |
| Qwen3.6-27B | json | T_lookup | 0.029 | 0.070 | 0.005 | 0.020 | 0.027 (147) | 0.068 (357) |
| Qwen3.6-27B | json | T_recall | 0.034 | 0.077 | 0.006 | 0.020 | 0.034 (169) | 0.076 (389) |
| Muse-Glimmer-30B | main | B | 0.078 | 0.157 | 0.004 | 0.016 | 0.074 (490) | 0.150 (989) |
| Muse-Glimmer-30B | main | T_lookup | 0.041 | 0.097 | 0.004 | 0.015 | 0.043 (270) | 0.099 (646) |
| Muse-Glimmer-30B | main | T_recall | 0.061 | 0.140 | 0.004 | 0.016 | 0.063 (401) | 0.145 (936) |
| Muse-Glimmer-30B | json | B | 0.063 | 0.134 | 0.004 | 0.016 | 0.060 (413) | 0.129 (858) |
| Muse-Glimmer-30B | json | T_lookup | 0.041 | 0.097 | 0.004 | 0.015 | 0.044 (271) | 0.100 (643) |
| Muse-Glimmer-30B | json | T_recall | 0.060 | 0.140 | 0.004 | 0.015 | 0.062 (399) | 0.146 (930) |
| Nemotron-3.5-Lightning | main | B | 0.118 | 0.257 | 0.008 | 0.037 | 0.116 (312) | 0.256 (688) |
| Nemotron-3.5-Lightning | main | T_lookup | 0.091 | 0.204 | 0.009 | 0.037 | 0.093 (245) | 0.209 (549) |
| Nemotron-3.5-Lightning | main | T_recall | 0.101 | 0.219 | 0.009 | 0.038 | 0.101 (263) | 0.219 (581) |
| Nemotron-3.5-Lightning | json | B | 0.113 | 0.254 | 0.009 | 0.037 | 0.113 (299) | 0.252 (679) |
| Nemotron-3.5-Lightning | json | T_lookup | 0.099 | 0.219 | 0.009 | 0.038 | 0.101 (265) | 0.221 (587) |
| Nemotron-3.5-Lightning | json | T_recall | 0.107 | 0.229 | 0.009 | 0.037 | 0.112 (289) | 0.237 (625) |

## The probe against sklearn (critic_1125: one cell)

results/x53_monitor/sklearn_check-20261029T104330Z: qwen35_9b_x53_monitor main test, T, (c), L20, full: ours 0.8985 vs sklearn 0.8995 (diff -0.0010; predictions agree 0.999); B, (b), L16, jpp25: ours 0.6125 vs sklearn 0.6135 (diff -0.0010; predictions agree 0.999)

## Report

EXP x53_monitor (53.2) @ c31a652e | models Qwen3.5-9B, Qwen3.6-27B, Muse-Glimmer-30B, Nemotron-3.5-Lightning | n: Qwen3.5-9B main 400 rows (200 scenes, 43 bridge entities); Qwen3.5-9B json 620 rows (310 scenes, 32 bridge entities); Qwen3.6-27B main 400 rows (200 scenes, 45 bridge entities); Qwen3.6-27B json 620 rows (310 scenes, 32 bridge entities); Muse-Glimmer-30B main 400 rows (200 scenes, 44 bridge entities); Muse-Glimmer-30B json 776 rows (388 scenes, 35 bridge entities); Nemotron-3.5-Lightning main 400 rows (200 scenes, 43 bridge entities); Nemotron-3.5-Lightning json 830 rows (415 scenes, 30 bridge entities) | seeds: probe splits 0-4, random subspaces 888 + layer + 1000 x seed, bootstrap 0

Claim tested (monitor (b)): a trained probe on the J++ lens part of the state decodes the bridge's slot (b) and the lookup's digit (c) well above a random subspace of the same size (carries), or no better than it while the full residual decodes them and the random subspace does not (blind); (a) and (d) are positive controls.

Three dumbest ways this could be wrong:
1) The J++ part is fit to each state while the random subspace is fixed, so J++ keeps more of the state (see the norm shares) and can beat random on energy alone, not because the lens is special. Checked beside (critic_1125): the energy-matched random subspace (same median energy share) and the fixed J++ subspace (no per-state fit) each get the same rule; PCA top-k is drawn in every panel.
2) (a) and (d) are probed on held-out scenes, not entities (a held-out entity is an unseen class); the probe can then read the bridge's identity and map it to the recall's answer, so (d) at the bridge word is identity, not the answer computed. Not checked beyond the grouping; (b) and (c) are on held-out entities.
3) One C for every feature: the full residual and J++ (fit in the training span, up to n_train dimensions) and the k-dimensional random / PCA features are regularised differently in effect; a low full-residual ceiling (e.g. the slot at the bridge word) can be the probe, not the state. Not checked (the brief fixes the same regularisation); the solver itself is checked against sklearn on one cell (above).

For the human to verify: the rule from the per-layer accuracies in x53_monitor.json (results[<model>][<set>]['acc']['<B|T>|<a-d>'][<feature>]); one cell end to end by rerunning `scripts/x53_monitor.py probe --name <run> --states-root <dir with the pulled states>` (deterministic; cache/x53_monitor/<run>/<set>.npz holds per row [right, held out] over the 5 seeds).

Status: UNVERIFIED (exploration day; nothing into the README).

Figures: x53_monitor_main.png, x53_monitor_json.png (accuracy by layer; columns the headline (b), (c) then the positive controls (a), (d), rows model x position; full black, J++ per state purple, fixed J++ light purple, random light grey, energy-matched random dark grey, PCA green; k = 25 solid, k = 100 dashed; chance dotted; panel label = the decisive rule per k). Per-layer accuracies, CIs and chance: x53_monitor.json.

