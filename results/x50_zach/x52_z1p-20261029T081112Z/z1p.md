# Batch 50 Z1P: our change-removal on Zach's passages (UNVERIFIED)

Z1-P (no Q-line: Dan's morning brief, 29 Oct) (batch 52 coverage: no prediction: Z1's rule (verbatim, first scored on the K items, results/x50_zach/z1-20261028T161649Z) applied now to the P items (Dan's morning brief, 29 Oct)). Items: jsuite_v2_test_chat (and jsuite_v2nb_test_chat only if short), words ('PP', 'PM'), leak filter. Cluster bootstrap over the bridge entity (10000, seed 0).

Rule (fixed in advance): Per model: gap >= 0.3 and lookup extra loss <= 0.10 -> "the split holds on his passages"; lookup >= 0.20 -> "the lookup follows the lens here"; else in between. Order split (after the gate, before the data): items where the bridge's fact sentence comes before the pointer sentence vs after. "The order pattern replicates" if the lookup's switch under the whole change is >= 2x higher fact-first than fact-after (both CIs), as in our 65-89 % vs 9-19 %. Hard-read stratum (v3 flag): the gap within hard-read items within 0.15 of the easy items -> "not a lookup-difficulty effect".

As computed: Extra loss = X0's excess = Jdep - Rdep = (S_no_jpp_rand - S_no_jpp) / S_whole per reader over the chosen passages (J++: signed OMP, k = 25); switch = the top token is the first token of the other entity's answer; gap = the M reader's extra loss minus the K reader's on the same cluster-bootstrap draws (over the original bridge entity, 10,000 resamples, seed 0, 95% intervals). Point estimates decide (EPS 1e-9); an undefined extra loss (no switch under the whole change) holds no clause ("can't tell"). X0's validity bar (S_whole >= 0.30 and >= 30 switches) per reader beside, not in the rule. Muse: the rule at L26 and at L36, both reported. Z1 order: the K reader's whole-change switch share, fact-first vs fact-after by the original bridge's fact sentence (K passage) against the pointer sentence; replicates iff fact-first >= 2 x fact-after (point estimates; each stratum's interval beside, and whether they separate). Hard-read: no flag in v2, so not tested.

| model | run | status | layer | n (entities) | K extra loss | M extra loss | gap | verdict | K S_whole | M S_whole |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | qwen35_9b_x52_z1p | tested | 12 | 200 (129) | -0.05 [-0.13, 0.03] | 0.59 [0.51, 0.67] | 0.64 [0.51, 0.76] | the split holds on his passages | 0.32 [0.25, 0.38] | 0.81 [0.76, 0.86] |

## qwen3.5-9b (qwen35_9b_x52_z1p)

Gate: O's read accuracy {'K': 0.8, 'M': 0.8438095238095238} over 525 passages, pass True; over Zach's kept passages {'cases': 190, 'org_read_accuracy': {'K': 0.9947368421052631, 'M': 0.8894736842105263}, 'pass': True, 'eligible': 110}; eligible 231, chosen 200 (sets {'jsuite_v2_test_chat': 112, 'jsuite_v2nb_test_chat': 88}); counts {"jsuite_v2_test_chat": {"passages": 358, "pair_drops": {}, "drops": {"no candidate aligns (the patch token is not at one index in O and S)": 94, "no other entity with another answer": 3}, "cases": 261}, "jsuite_v2nb_test_chat": {"passages": 358, "pair_drops": {}, "drops": {"no candidate aligns (the patch token is not at one index in O and S)": 93, "no other entity with another answer": 1}, "cases": 264}}.

L12: routes {"K": {"none": {"original": 200}, "whole": {"original": 132, "switch": 63, "other": 5}, "no_jpp": {"original": 140, "switch": 56, "other": 4}, "no_jpp_rand": {"original": 144, "switch": 53, "other": 3}}, "M": {"none": {"original": 200}, "whole": {"switch": 163, "original": 31, "other": 5, "lure": 1}, "no_jpp": {"original": 143, "switch": 52, "other": 5}, "no_jpp_rand": {"original": 45, "switch": 148, "other": 6, "lure": 1}}}
L12 order: fact-first 0.60 [0.50, 0.70] (n 96), fact-after 0.05 [0.01, 0.09] (n 104); ratio 12.57; replicates True; intervals separate True. Hard-read: no hard-read flag in v2 (not tested).

Beside (Zach's stored rows, band L12-16): full qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1: paper10 M-K 0.32 [0.18, 0.45] (joined 110), paper10_rot M-K -0.09 [-0.15, -0.04] (joined 110)

