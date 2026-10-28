# 48.3: forward binding at the locker sentence, outside the lens?

Batch 48, test 48.3 (jobs/c3/batch48.yaml; Q48.3, Dan: (a) · 60%; (b) · 60%). Probe = which of the scene's three people picked the item, read at the locker sentence's item / number token (ridge, the sentence's item held out, 5 folds seed 0; chance 0.33); lens share = the written contrast's J++ k = 25 share (median) against 20 Gaussian directions' (mean); the write = s (mu_asked - mu_picker) at both tokens, read by both readers. Cluster bootstrap over bridge entities (10000, seed 0). UNVERIFIED.

Rule (fixed in advance): forward binding at the locker sentence, outside the lens: probe >= 0.85 in locker-after and <= 0.5 in locker-first; the person contrast's J++ share (k = 25) <= 2x a random direction's; the write sends >= 0.3 of lookups to the written item's locker (random <= 0.05); on both models. As computed: the probe and lens clauses hold on a model at at least one token; the write clause at some s with its random control at that s; the recall's move with the same bars (reported, Q48.3's second question).

**Verdict: does not hold** (Q48.3 no; the write moves the recall too: no, by model {'qwen3.5-9b': False, 'muse-glimmer-30b': False}): 0 of 2 models hold; failed: qwen35_9b_x48_bind, muse30_x48_bind.

| model | run | status | holds | tokens holding | write (lookup) | recall moves | why |
|---|---|---|---|---|---|---|---|
| qwen3.5-9b | qwen35_9b_x48_bind | tested | no | none | no | no | item: probe after 0.365 < 0.85, before 0.331 <= 0.5; share 0.1881 > 2.0 x 0.0843; number: probe after 0.335 < 0.85, before 0.283 <= 0.5; share 0.1809 > 2.0 x 0.0843; lookup s = 1: target 0.000 < 0.3, random 0.000 <= 0.05; s = 2: target 0.000 < 0.3, random 0.014 <= 0.05; recall s = 1: target 0.000 < 0.3, random 0.000 <= 0.05; s = 2: target 0.000 < 0.3, random 0.000 <= 0.05 |
| muse-glimmer-30b | muse30_x48_bind | tested | no | none | no | no | item: probe after 0.363 < 0.85, before 0.311 <= 0.5; share 0.1032 <= 2.0 x 0.0529; number: probe after 0.392 < 0.85, before 0.319 <= 0.5; share 0.1028 <= 2.0 x 0.0529; lookup s = 1: target 0.015 < 0.3, random 0.000 <= 0.05; s = 2: target 0.015 < 0.3, random 0.000 <= 0.05; recall s = 1: target 0.016 < 0.3, random 0.000 <= 0.05; s = 2: target 0.016 < 0.3, random 0.000 <= 0.05 |

Probes (accuracy, chance 0.33): the rule's cells (the asked item's sentence in locker-after / locker-first scenes), every sentence of the stratum beside, and the after-trained probe on the before states (transfer).

| model | token | after (rule) | before (rule) | after, all sentences | before, all | transfer (rule cell) | transfer, all |
|---|---|---|---|---|---|---|---|
| qwen3.5-9b | item | 0.36 [0.30, 0.42] (n 266) | 0.33 [0.27, 0.39] (n 251) | 0.41 [0.37, 0.44] (n 933) | 0.29 [0.26, 0.32] (n 918) | 0.28 [0.22, 0.35] (n 251) | 0.31 [0.27, 0.35] (n 918) |
| qwen3.5-9b | number | 0.33 [0.27, 0.39] (n 266) | 0.28 [0.22, 0.35] (n 251) | 0.29 [0.25, 0.33] (n 933) | 0.28 [0.24, 0.31] (n 918) | 0.35 [0.28, 0.42] (n 251) | 0.33 [0.29, 0.37] (n 918) |
| muse-glimmer-30b | item | 0.36 [0.31, 0.42] (n 278) | 0.31 [0.25, 0.38] (n 235) | 0.34 [0.31, 0.39] (n 948) | 0.32 [0.28, 0.37] (n 879) | 0.33 [0.27, 0.40] (n 235) | 0.31 [0.27, 0.34] (n 879) |
| muse-glimmer-30b | number | 0.39 [0.34, 0.44] (n 278) | 0.32 [0.25, 0.39] (n 235) | 0.29 [0.26, 0.33] (n 948) | 0.33 [0.29, 0.37] (n 879) | 0.34 [0.29, 0.40] (n 235) | 0.30 [0.27, 0.33] (n 879) |

Lens share of the written person contrast (J++ k = 25 signed OMP; median over the written scenes) against random directions' (mean), and the contrast's norm (median).

| model | token | contrast share | random share | 2x random | norm | written scenes |
|---|---|---|---|---|---|---|
| qwen3.5-9b | item | 0.1881 | 0.0843 | 0.1685 | 7.735049999999999 | 94 |
| qwen3.5-9b | number | 0.1809 | 0.0843 | 0.1685 | 6.6771 | 94 |
| muse-glimmer-30b | item | 0.1032 | 0.0529 | 0.1058 | 87.8125 | 88 |
| muse-glimmer-30b | number | 0.1028 | 0.0529 | 0.1058 | 79.946 | 88 |

The write (locker-after scenes of half B): per arm the lookup's answer class (target = the written item's locker, original = O's answer) and the recall's (target = the written item's attribute; scenes whose attribute equals the bridge's are left out), and the share still right (O's answer).

| model | reader | n (same attribute) | arm | target | original | other | right |
|---|---|---|---|---|---|---|---|
| qwen3.5-9b | lookup | 70 (0) | none | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.5-9b | lookup | 70 (0) | w1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.5-9b | lookup | 70 (0) | w2 | 0.00 [0.00, 0.00] | 0.97 [0.93, 1.00] | 0.03 [0.00, 0.07] | 0.97 [0.93, 1.00] |
| qwen3.5-9b | lookup | 70 (0) | r1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.5-9b | lookup | 70 (0) | r2 | 0.01 [0.00, 0.06] | 0.97 [0.92, 1.00] | 0.01 [0.00, 0.04] | 0.97 [0.92, 1.00] |
| qwen3.5-9b | recall | 64 (6) | none | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.5-9b | recall | 64 (6) | w1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.5-9b | recall | 64 (6) | w2 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.5-9b | recall | 64 (6) | r1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.5-9b | recall | 64 (6) | r2 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| muse-glimmer-30b | lookup | 67 (0) | none | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| muse-glimmer-30b | lookup | 67 (0) | w1 | 0.01 [0.00, 0.05] | 0.99 [0.95, 1.00] | 0.00 [0.00, 0.00] | 0.99 [0.95, 1.00] |
| muse-glimmer-30b | lookup | 67 (0) | w2 | 0.01 [0.00, 0.04] | 0.99 [0.96, 1.00] | 0.00 [0.00, 0.00] | 0.99 [0.96, 1.00] |
| muse-glimmer-30b | lookup | 67 (0) | r1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| muse-glimmer-30b | lookup | 67 (0) | r2 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| muse-glimmer-30b | recall | 61 (6) | none | 0.02 [0.00, 0.05] | 0.97 [0.91, 1.00] | 0.02 [0.00, 0.06] | 0.97 [0.91, 1.00] |
| muse-glimmer-30b | recall | 61 (6) | w1 | 0.02 [0.00, 0.05] | 0.95 [0.84, 1.00] | 0.03 [0.00, 0.11] | 0.95 [0.84, 1.00] |
| muse-glimmer-30b | recall | 61 (6) | w2 | 0.02 [0.00, 0.05] | 0.93 [0.82, 1.00] | 0.05 [0.00, 0.13] | 0.93 [0.82, 1.00] |
| muse-glimmer-30b | recall | 61 (6) | r1 | 0.00 [0.00, 0.00] | 0.98 [0.95, 1.00] | 0.02 [0.00, 0.05] | 0.98 [0.95, 1.00] |
| muse-glimmer-30b | recall | 61 (6) | r2 | 0.00 [0.00, 0.00] | 0.97 [0.89, 1.00] | 0.03 [0.00, 0.11] | 0.97 [0.89, 1.00] |

Write minus random (target rate, paired): qwen3.5-9b lookup s = 1: 0.00 [0.00, 0.00]; qwen3.5-9b lookup s = 2: −0.01 [−0.06, 0.00]; qwen3.5-9b recall s = 1: 0.00 [0.00, 0.00]; qwen3.5-9b recall s = 2: 0.00 [0.00, 0.00]; muse-glimmer-30b lookup s = 1: 0.01 [0.00, 0.05]; muse-glimmer-30b lookup s = 2: 0.01 [0.00, 0.04]; muse-glimmer-30b recall s = 1: 0.02 [0.00, 0.05]; muse-glimmer-30b recall s = 2: 0.02 [0.00, 0.05].

Arms: none = O unedited; w1 = s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens; w2 = s = 2 (mu_Iris - mu_Jack); r1 = a random vector of the s = 1 write's norm, per token; r2 = a random vector of the s = 2 write's norm, per token.

Scenes and fit (descriptive):

- qwen3.5-9b (qwen35_9b_x48_bind, L12): 617 scenes ({'main': {'run': 'qwen35_9b_x0_necessity', 'scenes_at_L': 200, 'groups': {'after': 100, 'before': 100}}, '45m': {'run': 'qwen35_9b_x45m_fresh', 'scenes_at_L': 417, 'groups': {'before': 151, 'after': 166, 'mixed': 100}}}; dropped none); 46 bridge entities in halves A / B; locker-after {'scenes': 266, 'A': 140, 'B': 126}; write candidates in B 98 (dropped {"no other person's locker sentence after both picks": 67}; no mean {'the written person has fewer than 3 fit states': 2, 'the asked person has fewer than 3 fit states': 2}); written 94; 59 names, names with means {'item': 58, 'number': 58}; strata {'after': 933, 'before': 918}; numbers {'digits': 333, 'words': 284}.
- muse-glimmer-30b (muse30_x48_bind, L26): 609 scenes ({'main': {'run': 'muse30b_x0_necessity', 'scenes_at_L': 200, 'groups': {'after': 108, 'before': 92}}, '45m': {'run': 'muse30b_x45m_fresh', 'scenes_at_L': 409, 'groups': {'before': 143, 'after': 170, 'mixed': 96}}}; dropped none); 44 bridge entities in halves A / B; locker-after {'scenes': 278, 'A': 141, 'B': 137}; write candidates in B 105 (dropped {"no other person's locker sentence after both picks": 72, "the candidate sentence's tokens are not one token each": 3}; no mean {'the asked person has fewer than 3 fit states': 15, 'the written person has fewer than 3 fit states': 2}); written 88; 59 names, names with means {'item': 55, 'number': 55}; strata {'after': 948, 'before': 879}; numbers {'digits': 314, 'words': 295}.
