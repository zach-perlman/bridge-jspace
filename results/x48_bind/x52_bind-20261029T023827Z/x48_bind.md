# 48.3: forward binding at the locker sentence, outside the lens?

Batch 48, test 48.3 (jobs/c3/batch48.yaml; batch 52 C coverage, no prediction: coverage run on an already-scored rule; rule first scored in results/x48_bind/x48_bind-20261028T113120Z; the all-models count covers the given runs only, not re-scored). Probe = which of the scene's three people picked the item, read at the locker sentence's item / number token (ridge, the sentence's item held out, 5 folds seed 0; chance 0.33); lens share = the written contrast's J++ k = 25 share (median) against 20 Gaussian directions' (mean); the write = s (mu_asked - mu_picker) at both tokens, read by both readers. Cluster bootstrap over bridge entities (10000, seed 0). UNVERIFIED.

Rule (fixed in advance): forward binding at the locker sentence, outside the lens: probe >= 0.85 in locker-after and <= 0.5 in locker-first; the person contrast's J++ share (k = 25) <= 2x a random direction's; the write sends >= 0.3 of lookups to the written item's locker (random <= 0.05); on both models. As computed: the probe and lens clauses hold on a model at at least one token; the write clause at some s with its random control at that s; the recall's move with the same bars (reported, Q48.3's second question).

**Verdict: does not hold** (Q48.3 no; the write moves the recall too: no, by model {'qwen3.6-27b': False}): 0 of 1 models hold; failed: x48_bind_27b.

| model | run | status | holds | tokens holding | write (lookup) | recall moves | why |
|---|---|---|---|---|---|---|---|
| qwen3.6-27b | x48_bind_27b | tested | no | none | no | no | item: probe after 0.496 < 0.85, before 0.284 <= 0.5; share 0.1250 <= 2.0 x 0.0685; number: probe after 0.307 < 0.85, before 0.353 <= 0.5; share 0.1251 <= 2.0 x 0.0685; lookup s = 1: target 0.000 < 0.3, random 0.000 <= 0.05; s = 2: target 0.010 < 0.3, random 0.000 <= 0.05; recall s = 1: target 0.000 < 0.3, random 0.000 <= 0.05; s = 2: target 0.000 < 0.3, random 0.000 <= 0.05 |

Probes (accuracy, chance 0.33): the rule's cells (the asked item's sentence in locker-after / locker-first scenes), every sentence of the stratum beside, and the after-trained probe on the before states (transfer).

| model | token | after (rule) | before (rule) | after, all sentences | before, all | transfer (rule cell) | transfer, all |
|---|---|---|---|---|---|---|---|
| qwen3.6-27b | item | 0.50 [0.43, 0.56] (n 335) | 0.28 [0.22, 0.35] (n 303) | 0.46 [0.43, 0.50] (n 1147) | 0.28 [0.25, 0.32] (n 1175) | 0.27 [0.20, 0.35] (n 303) | 0.32 [0.29, 0.35] (n 1175) |
| qwen3.6-27b | number | 0.31 [0.26, 0.35] (n 335) | 0.35 [0.29, 0.42] (n 303) | 0.30 [0.28, 0.32] (n 1147) | 0.30 [0.28, 0.32] (n 1175) | 0.34 [0.29, 0.40] (n 303) | 0.33 [0.30, 0.35] (n 1175) |

Lens share of the written person contrast (J++ k = 25 signed OMP; median over the written scenes) against random directions' (mean), and the contrast's norm (median).

| model | token | contrast share | random share | 2x random | norm | written scenes |
|---|---|---|---|---|---|---|
| qwen3.6-27b | item | 0.1250 | 0.0685 | 0.1370 | 22.76295 | 134 |
| qwen3.6-27b | number | 0.1251 | 0.0685 | 0.1370 | 16.4579 | 134 |

The write (locker-after scenes of half B): per arm the lookup's answer class (target = the written item's locker, original = O's answer) and the recall's (target = the written item's attribute; scenes whose attribute equals the bridge's are left out), and the share still right (O's answer).

| model | reader | n (same attribute) | arm | target | original | other | right |
|---|---|---|---|---|---|---|---|
| qwen3.6-27b | lookup | 103 (0) | none | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.6-27b | lookup | 103 (0) | w1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.6-27b | lookup | 103 (0) | w2 | 0.01 [0.00, 0.03] | 0.99 [0.97, 1.00] | 0.00 [0.00, 0.00] | 0.99 [0.97, 1.00] |
| qwen3.6-27b | lookup | 103 (0) | r1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.6-27b | lookup | 103 (0) | r2 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.6-27b | recall | 100 (3) | none | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.6-27b | recall | 100 (3) | w1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.6-27b | recall | 100 (3) | w2 | 0.00 [0.00, 0.00] | 0.99 [0.97, 1.00] | 0.01 [0.00, 0.03] | 0.99 [0.97, 1.00] |
| qwen3.6-27b | recall | 100 (3) | r1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| qwen3.6-27b | recall | 100 (3) | r2 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |

Write minus random (target rate, paired): qwen3.6-27b lookup s = 1: 0.00 [0.00, 0.00]; qwen3.6-27b lookup s = 2: 0.01 [0.00, 0.03]; qwen3.6-27b recall s = 1: 0.00 [0.00, 0.00]; qwen3.6-27b recall s = 2: 0.00 [0.00, 0.00].

Arms: none = O unedited; w1 = s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens; w2 = s = 2 (mu_Iris - mu_Jack); r1 = a random vector of the s = 1 write's norm, per token; r2 = a random vector of the s = 2 write's norm, per token.

Scenes and fit (descriptive):

- qwen3.6-27b (x48_bind_27b, L32): 774 scenes ({'main': {'run': 'x0_necessity_27b_chat', 'scenes_at_L': 200, 'groups': {'before': 101, 'after': 99}}, '45m': {'run': 'x45m_fresh_27b', 'scenes_at_L': 574, 'groups': {'before': 202, 'after': 236, 'mixed': 136}}}; dropped none); 46 bridge entities in halves A / B; locker-after {'scenes': 335, 'A': 158, 'B': 177}; write candidates in B 134 (dropped {"no other person's locker sentence after both picks": 90}; no mean none); written 134; 59 names, names with means {'item': 59, 'number': 59}; strata {'before': 1175, 'after': 1147}; numbers {'digits': 410, 'words': 364}.
