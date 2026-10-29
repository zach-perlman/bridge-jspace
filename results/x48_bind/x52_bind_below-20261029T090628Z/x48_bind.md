# 48.3: forward binding at the locker sentence, outside the lens?

Batch 48, test 48.3 (jobs/c3/batch48.yaml; batch 52 C coverage, below gate (exploratory): Lightning's clean one-pick gate fails (recall 0.751 < 0.80, results/x0_necessity/nem35l_x45s_smoke_clean/gate.json); eligible items only; hollow, never in the claims table or grades; rules verbatim, no prediction (Dan's morning queue, 29 Oct); rule first scored in results/x48_bind/x48_bind-20261028T113120Z; the all-models count covers the given runs only, not re-scored). Probe = which of the scene's three people picked the item, read at the locker sentence's item / number token (ridge, the sentence's item held out, 5 folds seed 0; chance 0.33); lens share = the written contrast's J++ k = 25 share (median) against 20 Gaussian directions' (mean); the write = s (mu_asked - mu_picker) at both tokens, read by both readers. Cluster bootstrap over bridge entities (10000, seed 0). UNVERIFIED.

Rule (fixed in advance): forward binding at the locker sentence, outside the lens: probe >= 0.85 in locker-after and <= 0.5 in locker-first; the person contrast's J++ share (k = 25) <= 2x a random direction's; the write sends >= 0.3 of lookups to the written item's locker (random <= 0.05); on both models. As computed: the probe and lens clauses hold on a model at at least one token; the write clause at some s with its random control at that s; the recall's move with the same bars (reported, Q48.3's second question).

**Verdict: does not hold** (Q48.3 no; the write moves the recall too: no, by model {'nemotron-3.5-lightning': False}): 0 of 1 models hold; failed: nem35l_x52_bind_below.

| model | run | status | holds | tokens holding | write (lookup) | recall moves | why |
|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | nem35l_x52_bind_below | tested | no | none | no | no | item: probe after 0.371 < 0.85, before 0.316 <= 0.5; share 0.2345 > 2.0 x 0.0864; number: probe after 0.242 < 0.85, before 0.282 <= 0.5; share 0.1986 > 2.0 x 0.0864; lookup s = 1: target 0.000 < 0.3, random 0.000 <= 0.05; s = 2: target 0.000 < 0.3, random 0.022 <= 0.05; recall s = 1: target 0.000 < 0.3, random 0.000 <= 0.05; s = 2: target 0.000 < 0.3, random 0.000 <= 0.05 |

Probes (accuracy, chance 0.33): the rule's cells (the asked item's sentence in locker-after / locker-first scenes), every sentence of the stratum beside, and the after-trained probe on the before states (transfer).

| model | token | after (rule) | before (rule) | after, all sentences | before, all | transfer (rule cell) | transfer, all |
|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | item | 0.37 [0.31, 0.44] (n 248) | 0.32 [0.24, 0.39] (n 174) | 0.39 [0.35, 0.43] (n 793) | 0.29 [0.24, 0.33] (n 692) | 0.28 [0.22, 0.36] (n 174) | 0.27 [0.23, 0.32] (n 692) |
| nemotron-3.5-lightning | number | 0.24 [0.18, 0.30] (n 248) | 0.28 [0.21, 0.36] (n 174) | 0.24 [0.21, 0.28] (n 793) | 0.27 [0.24, 0.31] (n 692) | 0.21 [0.15, 0.27] (n 174) | 0.25 [0.21, 0.29] (n 692) |

Lens share of the written person contrast (J++ k = 25 signed OMP; median over the written scenes) against random directions' (mean), and the contrast's norm (median).

| model | token | contrast share | random share | 2x random | norm | written scenes |
|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | item | 0.2345 | 0.0864 | 0.1728 | 7.9273 | 70 |
| nemotron-3.5-lightning | number | 0.1986 | 0.0864 | 0.1728 | 5.7441 | 70 |

The write (locker-after scenes of half B): per arm the lookup's answer class (target = the written item's locker, original = O's answer) and the recall's (target = the written item's attribute; scenes whose attribute equals the bridge's are left out), and the share still right (O's answer).

| model | reader | n (same attribute) | arm | target | original | other | right |
|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | lookup | 45 (0) | none | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| nemotron-3.5-lightning | lookup | 45 (0) | w1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| nemotron-3.5-lightning | lookup | 45 (0) | w2 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| nemotron-3.5-lightning | lookup | 45 (0) | r1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| nemotron-3.5-lightning | lookup | 45 (0) | r2 | 0.02 [0.00, 0.08] | 0.98 [0.92, 1.00] | 0.00 [0.00, 0.00] | 0.98 [0.92, 1.00] |
| nemotron-3.5-lightning | recall | 39 (6) | none | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| nemotron-3.5-lightning | recall | 39 (6) | w1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| nemotron-3.5-lightning | recall | 39 (6) | w2 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| nemotron-3.5-lightning | recall | 39 (6) | r1 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| nemotron-3.5-lightning | recall | 39 (6) | r2 | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |

Write minus random (target rate, paired): nemotron-3.5-lightning lookup s = 1: 0.00 [0.00, 0.00]; nemotron-3.5-lightning lookup s = 2: −0.02 [−0.08, 0.00]; nemotron-3.5-lightning recall s = 1: 0.00 [0.00, 0.00]; nemotron-3.5-lightning recall s = 2: 0.00 [0.00, 0.00].

Arms: none = O unedited; w1 = s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens; w2 = s = 2 (mu_Iris - mu_Jack); r1 = a random vector of the s = 1 write's norm, per token; r2 = a random vector of the s = 2 write's norm, per token.

Scenes and fit (descriptive):

- nemotron-3.5-lightning (nem35l_x52_bind_below, L14): 495 scenes ({'main': {'run': 'nem35l_x52_conflict', 'scenes_at_L': 200, 'groups': {'after': 115, 'before': 85}}, '45m': {'run': 'nem35l_x52_fresh', 'scenes_at_L': 295, 'groups': {'after': 133, 'mixed': 73, 'before': 89}}}; dropped none); 42 bridge entities in halves A / B; locker-after {'scenes': 248, 'A': 132, 'B': 116}; write candidates in B 78 (dropped {"no other person's locker sentence after both picks": 67, "the candidate sentence's tokens are not one token each": 5}; no mean {'the asked person has fewer than 3 fit states': 6, 'the written person has fewer than 3 fit states': 2}); written 70; 59 names, names with means {'item': 56, 'number': 56}; strata {'before': 692, 'after': 793}; numbers {'words': 259, 'digits': 236}.
