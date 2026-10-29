# 53.2 addendum (Qwen3.5-122B-A10B): the monitor test

UNVERIFIED. rule fixed in advance in jobs/c3/batch53.yaml (53.2); no prediction. Spec: jobs/c3/batch53.yaml (53.2); jobs/c3/x53_monitor_*.yaml.

## Coverage flags: Qwen3.5-122B-A10B

- Coverage run (Dan 12:20, jobs/c3/batch53.yaml fallback_1220): same rule, no new rule, no prediction; an addendum to the four models' verdict, not part of it.
- L33 (the main test's X0 r2 run, qwen35_122b_x0_necessity_r2) is the 27B's relative depth carried over (33/48), not a layer fixed for the 122B on its own data.
- The checkpoint is FP8 (Qwen/Qwen3.5-122B-A10B-FP8); the J++ lens was fit on the bf16 weights.
- Mixture of experts, ~10B parameters active per token, split over 2 GPUs (BJ_DEVICE_MAP=auto).
- The bridge word's state on the recall's prompt differs from the lookup's (identical prefixes) by up to this relative norm (main: max 0.082, 9 of 200 items over 0.02; json: max 0.153, 82 of 310 items over 0.02): kernel numerics of the FP8 / MoE forward on prompts of different lengths; every probe reads B on the lookup's prompt.

Rule (verbatim): "J-space blind to X" if the J++ probe is within 0.10 of the random subspace at every layer while the full residual reaches >= 0.8 at some layer; "J-space carries X" if J++ >= 0.8 and >= 0.3 above random; else in between.

As computed: per model, dataset, position, target and k, on point estimates (accuracy over rows and 5 seeds of 5-fold CV, each seed a random assignment of the groups to the folds), over every cached layer (every second layer from L0); logistic probes, C = 1.0 for every feature (sklearn's objective, standardised features, scipy L-BFGS); (b), (c) on held-out entities; (a), (d) on held-out scenes (a held-out entity is an unseen class there). CIs: cluster bootstrap over the bridge entity (10,000, seed 0).

Dan's changes before scoring (jobs/c3/batch53.yaml critic_1125, verbatim): "53.2 changes, before scoring: headline targets (b) slot and (c) lookup digit; (a) and (d) are positive controls. Add a fixed J++ subspace (the k atoms most frequent on the training folds) and an energy-matched random subspace beside the current ones. Check one cell against sklearn."

So: the headline targets are (b) and (c); (a) and (d) are positive controls (their rule outcome below, under their own heading). The decisive label is the brief's (the per-state J++ part vs a random subspace of the same k). Beside it: (i) the same rule verbatim with the J++ entries replaced by the fixed J++ subspace (fix_k: per training fold the span of the k atoms most frequent among the training rows' first k OMP atoms, ties the smaller token id; the held-out rows projected on it unchanged) against the same random_k; (ii) Dan's 13:15 energy rule (below) on the per-state J++ part against the energy-matched random subspace (erand_k: dimension r = round(the J++_k part's median share of ||h||^2 at that layer and row set, over all rows, label-free, x d), the first r columns of the random_k frame; a Haar r-dimensional subspace keeps r / d of ||h||^2 in expectation; rescaling a k-dimensional part instead would change nothing, the probes standardise every feature).

Dan 13:15, fixed before the verdict (jobs/c3/batch53.yaml answers_1315, verbatim): "53.2, fixed before the verdict: if J++ is >= 0.10 below the energy-matched random while the full state is >= 0.8, the label is "the address is under-represented in the lens directions" (stronger than blind), not an energy artefact. If J++ is within 0.10 of the energy-matched random, "no different from random directions of the same energy"."

Applied beside the decisive labels, on the per-state J++ part vs the energy-matched random: 'under-represented in the lens directions' if at some layer where the full state is >= 0.8 J++ is >= 0.10 below the energy-matched random (the agent's reading of 'while', flagged); 'no different from random directions of the same energy' if J++ is within 0.10 of it at every layer (as 53.2's 'within 0.10', flagged); else in between; where both hold exactly at the bar, under-represented. 'The address' is Dan's word for the slot; for the other targets the same thresholds with the target named ('<X> is under-represented in the lens directions'), flagged. The 11:40 labels on the fixed-k random stay as they are.

Dan's wording, fixed before the verdict (jobs/c3/batch53.yaml additions_1140 item 2, verbatim): "report two monitors separately. (a) The lens readout (top words): cite 47.0, unchanged. (b) The trained probe on J++ coordinates vs random vs full. If the random subspace also decodes the slot ("random reads it too"), the wording is: "the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it" — not "J-space is blind". Only "J-space blind" if J++ is within 0.10 of random AND random is under 0.8 while the full state is >= 0.8."

Applied: 'J-space blind to X' only if J++ is within 0.10 of random at every layer AND the random subspace stays under 0.8 at every layer (the agent's reading of 'random is under 0.8', flagged) while the full state reaches >= 0.8 at some layer. Where J++ is within 0.10 of random everywhere and the full state reaches 0.8 but so does random ('random reads it too'), the slot's label is Dan's sentence: "the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it"; for the other targets the agent writes '<X> is linearly decodable from many subspaces, J++ included' (the lens-readout clause is 47.0's, which is about the address). 'carries' and 'in between' as in the brief. Notes column: 'random reads it too' where that case opens; 'full < 0.8' where the full residual never reaches 0.8 (then neither 'blind' nor 'carries' can open).

## Monitor (a): the lens readout (top words)

Cited, unchanged: 47.0 ('is the pointer verbalizable?'; results/x47_verbal/summary-20261028T033646Z/verbal.md for Qwen3.5-9B, Qwen3.6-27B and Muse Glimmer 30B; results/x47_verbal/summary-20261029T005548Z/verbal.md for Nemotron 3.5 Lightning): read 'not verbalizable' on all four models. No new numbers here. 47.0 has no run on Qwen3.5-122B-A10B: nothing is cited for it.

## Monitor (b): the trained probe on J++ coordinates vs random vs full

At a glance, the headline targets' decisive labels (k = 25 / 100; blind = 'J-space blind to X', carries = 'J-space carries X', many = random reads it too: Dan's sentence for the slot, 'decodable from many subspaces, J++ included' for the digit; between = in between). Full wording and the arms beside in the tables below.

| model | dataset | (b) its locker slot at B | (b) its locker slot at T | (c) lookup's digit at B | (c) lookup's digit at T |
|---|---|---|---|---|---|
| Qwen3.5-122B-A10B | main | between / between | blind / between | between / between | many / many |
| Qwen3.5-122B-A10B | json | between / between | blind / blind | between / between | many / many |

Beside, Dan 13:15's energy rule on the same cells (per-state J++ vs the energy-matched random; under = 'under-represented in the lens directions', same energy = 'no different from random directions of the same energy', between = in between):

| model | dataset | (b) its locker slot at B | (b) its locker slot at T | (c) lookup's digit at B | (c) lookup's digit at T |
|---|---|---|---|---|---|
| Qwen3.5-122B-A10B | main | between / same energy | under / under | same energy / same energy | same energy / same energy |
| Qwen3.5-122B-A10B | json | between / between | under / under | same energy / same energy | same energy / same energy |

### Headline: (b) the bridge's locker slot and (c) the lookup's answer digit

| model | dataset | position | target | k | decisive: J++ (per state) vs random | beside: fixed J++ vs random | beside: J++ vs energy-matched random (Dan 13:15) | full / J++ / fixed / random / e-random / PCA max | notes |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.65 / 0.57 / 0.52 / 0.53 / 0.61 / 0.65 | full < 0.8 |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | B | (b) its locker slot | 100 | in between | in between | no different from random directions of the same energy | 0.65 / 0.63 / 0.56 / 0.58 / 0.63 / 0.63 | full < 0.8 |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.12 / 0.15 / 0.14 / 0.14 / 0.13 / 0.13 | full < 0.8 |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.12 / 0.14 / 0.13 / 0.13 / 0.13 / 0.12 | full < 0.8 |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | T | (b) its locker slot | 25 | J-space blind to X | J-space blind to X | the address is under-represented in the lens directions | 0.96 / 0.73 / 0.74 / 0.71 / 0.91 / 0.87 |  |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | T | (b) its locker slot | 100 | in between | the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it | the address is under-represented in the lens directions | 0.96 / 0.85 / 0.86 / 0.85 / 0.94 / 0.94 | fixed: random reads it too |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | in between | no different from random directions of the same energy | 0.99 / 1.00 / 0.96 / 0.99 / 0.99 / 1.00 | decisive: random reads it too |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | in between | no different from random directions of the same energy | 0.99 / 1.00 / 0.99 / 1.00 / 0.99 / 1.00 | decisive: random reads it too |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | B | (b) its locker slot | 25 | in between | in between | in between | 0.62 / 0.42 / 0.32 / 0.38 / 0.54 / 0.53 | full < 0.8 |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | B | (b) its locker slot | 100 | in between | in between | in between | 0.62 / 0.56 / 0.43 / 0.45 / 0.59 / 0.54 | full < 0.8 |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | B | (c) lookup's digit | 25 | in between | in between | no different from random directions of the same energy | 0.25 / 0.15 / 0.12 / 0.14 / 0.17 / 0.12 | full < 0.8 |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | B | (c) lookup's digit | 100 | in between | in between | no different from random directions of the same energy | 0.25 / 0.17 / 0.14 / 0.14 / 0.21 / 0.19 | full < 0.8 |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | T | (b) its locker slot | 25 | J-space blind to X | J-space blind to X | the address is under-represented in the lens directions | 0.80 / 0.46 / 0.48 / 0.48 / 0.74 / 0.66 |  |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | T | (b) its locker slot | 100 | J-space blind to X | J-space blind to X | the address is under-represented in the lens directions | 0.80 / 0.66 / 0.64 / 0.64 / 0.77 / 0.75 |  |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 0.96 / 0.96 / 0.94 / 0.95 / 0.97 / 0.96 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | the lookup's answer digit is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 0.96 / 0.97 / 0.97 / 0.96 / 0.96 / 0.97 | decisive: random reads it too; fixed: random reads it too |

Each decisive label at one layer (carries: the first layer with J++ >= 0.8 and J++ - random >= 0.3; otherwise the layer where the full residual peaks). Accuracy [95% CI].

| model | dataset | position | target | k | decisive label | layer | full | J++ | random | fixed J++ | e-random | PCA | chance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-122B-A10B | main | B | (b) its locker slot | 25 | in between | L38 | 0.65 [0.61, 0.69] | 0.57 [0.52, 0.61] | 0.51 [0.48, 0.54] | 0.52 [0.48, 0.56] | 0.61 [0.58, 0.63] | 0.64 [0.61, 0.67] | 0.32 [0.30, 0.35] |
| Qwen3.5-122B-A10B | main | B | (b) its locker slot | 100 | in between | L38 | 0.65 [0.61, 0.69] | 0.62 [0.57, 0.66] | 0.58 [0.55, 0.61] | 0.56 [0.53, 0.60] | 0.62 [0.59, 0.65] | 0.63 [0.59, 0.67] | 0.32 [0.30, 0.35] |
| Qwen3.5-122B-A10B | main | B | (c) lookup's digit | 25 | in between | L14 | 0.12 [0.09, 0.14] | 0.11 [0.09, 0.13] | 0.11 [0.10, 0.13] | 0.12 [0.10, 0.15] | 0.10 [0.09, 0.12] | 0.12 [0.10, 0.14] | 0.14 [0.10, 0.17] |
| Qwen3.5-122B-A10B | main | B | (c) lookup's digit | 100 | in between | L14 | 0.12 [0.09, 0.14] | 0.13 [0.10, 0.16] | 0.12 [0.10, 0.14] | 0.11 [0.08, 0.14] | 0.11 [0.09, 0.13] | 0.08 [0.06, 0.11] | 0.14 [0.10, 0.17] |
| Qwen3.5-122B-A10B | main | T | (b) its locker slot | 25 | J-space blind to X | L40 | 0.96 [0.95, 0.98] | 0.73 [0.69, 0.77] | 0.71 [0.69, 0.73] | 0.74 [0.70, 0.76] | 0.91 [0.89, 0.93] | 0.87 [0.84, 0.90] | 0.32 [0.30, 0.35] |
| Qwen3.5-122B-A10B | main | T | (b) its locker slot | 100 | in between | L40 | 0.96 [0.95, 0.98] | 0.85 [0.83, 0.88] | 0.85 [0.83, 0.87] | 0.86 [0.84, 0.88] | 0.94 [0.93, 0.96] | 0.94 [0.93, 0.96] | 0.32 [0.30, 0.35] |
| Qwen3.5-122B-A10B | main | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L46 | 0.99 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.99, 1.00] | 0.96 [0.95, 0.98] | 0.99 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.14 [0.10, 0.17] |
| Qwen3.5-122B-A10B | main | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L46 | 0.99 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.98, 1.00] | 0.99 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.14 [0.10, 0.17] |
| Qwen3.5-122B-A10B | json | B | (b) its locker slot | 25 | in between | L36 | 0.62 [0.58, 0.65] | 0.42 [0.39, 0.46] | 0.38 [0.34, 0.41] | 0.30 [0.25, 0.34] | 0.54 [0.50, 0.57] | 0.53 [0.49, 0.56] | 0.19 [0.16, 0.22] |
| Qwen3.5-122B-A10B | json | B | (b) its locker slot | 100 | in between | L36 | 0.62 [0.58, 0.65] | 0.56 [0.52, 0.59] | 0.44 [0.41, 0.47] | 0.43 [0.38, 0.49] | 0.59 [0.55, 0.62] | 0.52 [0.48, 0.56] | 0.19 [0.16, 0.22] |
| Qwen3.5-122B-A10B | json | B | (c) lookup's digit | 25 | in between | L36 | 0.25 [0.22, 0.28] | 0.15 [0.12, 0.18] | 0.14 [0.12, 0.16] | 0.11 [0.09, 0.14] | 0.17 [0.15, 0.20] | 0.11 [0.10, 0.13] | 0.08 [0.06, 0.10] |
| Qwen3.5-122B-A10B | json | B | (c) lookup's digit | 100 | in between | L36 | 0.25 [0.22, 0.28] | 0.17 [0.14, 0.19] | 0.14 [0.12, 0.15] | 0.13 [0.11, 0.16] | 0.21 [0.18, 0.24] | 0.19 [0.16, 0.23] | 0.08 [0.06, 0.10] |
| Qwen3.5-122B-A10B | json | T | (b) its locker slot | 25 | J-space blind to X | L44 | 0.80 [0.77, 0.84] | 0.43 [0.39, 0.47] | 0.48 [0.44, 0.51] | 0.42 [0.39, 0.46] | 0.74 [0.70, 0.77] | 0.66 [0.62, 0.70] | 0.19 [0.16, 0.22] |
| Qwen3.5-122B-A10B | json | T | (b) its locker slot | 100 | J-space blind to X | L44 | 0.80 [0.77, 0.84] | 0.66 [0.62, 0.70] | 0.64 [0.61, 0.67] | 0.64 [0.60, 0.69] | 0.77 [0.73, 0.80] | 0.75 [0.72, 0.79] | 0.19 [0.16, 0.22] |
| Qwen3.5-122B-A10B | json | T | (c) lookup's digit | 25 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L44 | 0.96 [0.95, 0.98] | 0.96 [0.94, 0.97] | 0.88 [0.86, 0.89] | 0.94 [0.93, 0.95] | 0.97 [0.95, 0.98] | 0.96 [0.95, 0.98] | 0.08 [0.06, 0.10] |
| Qwen3.5-122B-A10B | json | T | (c) lookup's digit | 100 | the lookup's answer digit is linearly decodable from many subspaces, J++ included | L44 | 0.96 [0.95, 0.98] | 0.97 [0.96, 0.98] | 0.96 [0.95, 0.97] | 0.97 [0.95, 0.98] | 0.96 [0.95, 0.98] | 0.97 [0.95, 0.98] | 0.08 [0.06, 0.10] |

### Positive controls: (a) which item is the bridge and (d) the recall's answer

| model | dataset | position | target | k | decisive: J++ (per state) vs random | beside: fixed J++ vs random | beside: J++ vs energy-matched random (Dan 13:15) | full / J++ / fixed / random / e-random / PCA max | notes |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | B | (a) which item | 25 | in between | in between | no different from random directions of the same energy | 0.98 / 0.98 / 0.98 / 0.98 / 0.98 / 0.98 |  |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | which item is the bridge is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 0.98 / 0.98 / 0.98 / 0.98 / 0.98 / 0.98 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | B | (d) recall's answer | 25 | J-space carries X | in between | no different from random directions of the same energy | 1.00 / 1.00 / 0.99 / 0.99 / 1.00 / 0.99 |  |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | T | (a) which item | 25 | in between | in between | in between | 0.63 / 0.22 / 0.27 / 0.29 / 0.56 / 0.55 | full < 0.8 |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | T | (a) which item | 100 | in between | in between | in between | 0.63 / 0.35 / 0.45 / 0.50 / 0.59 / 0.66 | full < 0.8 |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | T | (d) recall's answer | 25 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 1.00 / 1.00 / 0.98 / 0.99 / 1.00 / 1.00 | fixed: random reads it too |
| Qwen3.5-122B-A10B | main (400 rows, 42 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 1.00 / 1.00 / 0.99 / 1.00 / 1.00 / 1.00 | fixed: random reads it too |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | B | (a) which item | 25 | in between | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | which item is the bridge is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | B | (d) recall's answer | 25 | in between | in between | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 |  |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is linearly decodable from many subspaces, J++ included | no different from random directions of the same energy | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | decisive: random reads it too; fixed: random reads it too |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | T | (a) which item | 25 | in between | in between | in between | 0.70 / 0.29 / 0.32 / 0.35 / 0.62 / 0.61 | full < 0.8 |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | T | (a) which item | 100 | in between | in between | in between | 0.70 / 0.48 / 0.57 / 0.56 / 0.67 / 0.65 | full < 0.8 |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | T | (d) recall's answer | 25 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 0.97 / 0.96 / 0.95 / 0.95 / 0.97 / 0.97 | fixed: random reads it too |
| Qwen3.5-122B-A10B | json (620 rows, 32 bridges) | T | (d) recall's answer | 100 | in between | the recall's answer is linearly decodable from many subspaces, J++ included | the recall's answer is under-represented in the lens directions | 0.97 / 0.97 / 0.96 / 0.97 / 0.97 / 0.97 | fixed: random reads it too |

Each decisive label at one layer (carries: the first layer with J++ >= 0.8 and J++ - random >= 0.3; otherwise the layer where the full residual peaks). Accuracy [95% CI].

| model | dataset | position | target | k | decisive label | layer | full | J++ | random | fixed J++ | e-random | PCA | chance |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.5-122B-A10B | main | B | (a) which item | 25 | in between | L0 | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.98 [0.95, 0.99] | 0.06 [0.00, 0.14] |
| Qwen3.5-122B-A10B | main | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.06 [0.00, 0.14] |
| Qwen3.5-122B-A10B | main | B | (d) recall's answer | 25 | J-space carries X | L38 | 0.95 [0.92, 0.98] | 0.98 [0.97, 0.99] | 0.67 [0.61, 0.72] | 0.85 [0.78, 0.90] | 0.96 [0.93, 0.98] | 0.91 [0.85, 0.95] | 0.13 [0.07, 0.22] |
| Qwen3.5-122B-A10B | main | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | L22 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.99 [0.98, 1.00] | 0.99 [0.97, 0.99] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] | 0.13 [0.07, 0.22] |
| Qwen3.5-122B-A10B | main | T | (a) which item | 25 | in between | L42 | 0.63 [0.50, 0.73] | 0.20 [0.11, 0.26] | 0.29 [0.22, 0.35] | 0.25 [0.18, 0.30] | 0.56 [0.44, 0.64] | 0.54 [0.41, 0.64] | 0.06 [0.00, 0.14] |
| Qwen3.5-122B-A10B | main | T | (a) which item | 100 | in between | L42 | 0.63 [0.50, 0.73] | 0.35 [0.22, 0.45] | 0.50 [0.39, 0.58] | 0.43 [0.33, 0.50] | 0.59 [0.46, 0.69] | 0.60 [0.47, 0.69] | 0.06 [0.00, 0.14] |
| Qwen3.5-122B-A10B | main | T | (d) recall's answer | 25 | in between | L46 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.97, 0.99] | 0.98 [0.97, 0.99] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.13 [0.07, 0.22] |
| Qwen3.5-122B-A10B | main | T | (d) recall's answer | 100 | in between | L46 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.99 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.13 [0.07, 0.22] |
| Qwen3.5-122B-A10B | json | B | (a) which item | 25 | in between | L0 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.09 [0.00, 0.25] |
| Qwen3.5-122B-A10B | json | B | (a) which item | 100 | which item is the bridge is linearly decodable from many subspaces, J++ included | L0 | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 1.00 [0.99, 1.00] | 0.09 [0.00, 0.25] |
| Qwen3.5-122B-A10B | json | B | (d) recall's answer | 25 | in between | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.25 [0.11, 0.46] |
| Qwen3.5-122B-A10B | json | B | (d) recall's answer | 100 | the recall's answer is linearly decodable from many subspaces, J++ included | L0 | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 1.00 [1.00, 1.00] | 0.25 [0.11, 0.46] |
| Qwen3.5-122B-A10B | json | T | (a) which item | 25 | in between | L42 | 0.70 [0.60, 0.76] | 0.25 [0.17, 0.30] | 0.35 [0.28, 0.40] | 0.32 [0.24, 0.36] | 0.62 [0.53, 0.68] | 0.61 [0.53, 0.67] | 0.09 [0.00, 0.25] |
| Qwen3.5-122B-A10B | json | T | (a) which item | 100 | in between | L42 | 0.70 [0.60, 0.76] | 0.43 [0.32, 0.49] | 0.56 [0.47, 0.62] | 0.57 [0.47, 0.62] | 0.67 [0.57, 0.73] | 0.63 [0.53, 0.70] | 0.09 [0.00, 0.25] |
| Qwen3.5-122B-A10B | json | T | (d) recall's answer | 25 | in between | L44 | 0.97 [0.96, 0.98] | 0.96 [0.95, 0.98] | 0.94 [0.92, 0.96] | 0.94 [0.92, 0.96] | 0.97 [0.96, 0.98] | 0.97 [0.95, 0.98] | 0.25 [0.11, 0.46] |
| Qwen3.5-122B-A10B | json | T | (d) recall's answer | 100 | in between | L44 | 0.97 [0.96, 0.98] | 0.97 [0.95, 0.98] | 0.97 [0.95, 0.98] | 0.96 [0.94, 0.97] | 0.97 [0.96, 0.98] | 0.97 [0.96, 0.98] | 0.25 [0.11, 0.46] |


Not yet probed (a dataset or a pass missing): none.

## The main test's states vs 52 B's cache (lowest cosine over rows, any layer)

- Qwen3.5-122B-A10B: 52 B did not read this model (no cache to check against)

## Beside: each part's share of the state's squared norm (median over layers)

The J++ part is fit to each state (OMP picks the atoms that match it), the random subspace is fixed: the shares say how much of the state each feature keeps. The energy-matched random subspace's share and dimension (median over layers) beside.

| model | dataset | row set | J++25 | J++100 | random25 | random100 | e-random25 (dim) | e-random100 (dim) |
|---|---|---|---|---|---|---|---|---|
| Qwen3.5-122B-A10B | main | B | 0.099 | 0.170 | 0.008 | 0.033 | 0.098 (302) | 0.174 (519) |
| Qwen3.5-122B-A10B | main | T_lookup | 0.041 | 0.090 | 0.008 | 0.033 | 0.038 (124) | 0.086 (275) |
| Qwen3.5-122B-A10B | main | T_recall | 0.042 | 0.094 | 0.008 | 0.031 | 0.040 (127) | 0.094 (288) |
| Qwen3.5-122B-A10B | json | B | 0.089 | 0.152 | 0.008 | 0.032 | 0.085 (268) | 0.149 (453) |
| Qwen3.5-122B-A10B | json | T_lookup | 0.041 | 0.090 | 0.008 | 0.032 | 0.041 (123) | 0.088 (272) |
| Qwen3.5-122B-A10B | json | T_recall | 0.044 | 0.095 | 0.008 | 0.032 | 0.042 (135) | 0.092 (291) |

## The probe against sklearn (critic_1125: one cell)

results/x53_monitor/sklearn_check-20261029T104330Z: qwen35_9b_x53_monitor main test, T, (c), L20, full: ours 0.8985 vs sklearn 0.8995 (diff -0.0010; predictions agree 0.999); B, (b), L16, jpp25: ours 0.6125 vs sklearn 0.6135 (diff -0.0010; predictions agree 0.999)

## Report

EXP x53_monitor (53.2) @ e3e69427 | models Qwen3.5-122B-A10B | n: Qwen3.5-122B-A10B main 400 rows (200 scenes, 42 bridge entities); Qwen3.5-122B-A10B json 620 rows (310 scenes, 32 bridge entities) | seeds: probe splits 0-4, random subspaces 888 + layer + 1000 x seed, bootstrap 0

Claim tested (monitor (b)): a trained probe on the J++ lens part of the state decodes the bridge's slot (b) and the lookup's digit (c) well above a random subspace of the same size (carries), or no better than it while the full residual decodes them and the random subspace does not (blind); (a) and (d) are positive controls.

Three dumbest ways this could be wrong:
1) The J++ part is fit to each state while the random subspace is fixed, so J++ keeps more of the state (see the norm shares) and can beat random on energy alone, not because the lens is special. Checked beside (critic_1125): the energy-matched random subspace (same median energy share) and the fixed J++ subspace (no per-state fit) each get the same rule; PCA top-k is drawn in every panel.
2) (a) and (d) are probed on held-out scenes, not entities (a held-out entity is an unseen class); the probe can then read the bridge's identity and map it to the recall's answer, so (d) at the bridge word is identity, not the answer computed. Not checked beyond the grouping; (b) and (c) are on held-out entities.
3) One C for every feature: the full residual and J++ (fit in the training span, up to n_train dimensions) and the k-dimensional random / PCA features are regularised differently in effect; a low full-residual ceiling (e.g. the slot at the bridge word) can be the probe, not the state. Not checked (the brief fixes the same regularisation); the solver itself is checked against sklearn on one cell (above).

For the human to verify: the rule from the per-layer accuracies in x53_monitor.json (results[<model>][<set>]['acc']['<B|T>|<a-d>'][<feature>]); one cell end to end by rerunning `scripts/x53_monitor.py probe --name <run> --states-root <dir with the pulled states>` (deterministic; cache/x53_monitor/<run>/<set>.npz holds per row [right, held out] over the 5 seeds).

Status: UNVERIFIED (exploration day; nothing into the README).

Figures: x53_monitor_main.png, x53_monitor_json.png (accuracy by layer; columns the headline (b), (c) then the positive controls (a), (d), rows model x position; full black, J++ per state purple, fixed J++ light purple, random light grey, energy-matched random dark grey, PCA green; k = 25 solid, k = 100 dashed; chance dotted; panel label = the decisive rule per k). Per-layer accuracies, CIs and chance: x53_monitor.json.

