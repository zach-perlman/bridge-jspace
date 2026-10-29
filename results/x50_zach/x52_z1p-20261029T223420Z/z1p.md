# Batch 50 Z1P: our change-removal on Zach's passages (UNVERIFIED)

Z1-P (no Q-line: Dan's morning brief, 29 Oct) (batch 52 coverage: no prediction: Z1's rule (verbatim, first scored on the K items, results/x50_zach/z1-20261028T161649Z) applied now to the P items (Dan's morning brief, 29 Oct)). Items: jsuite_v2_test_chat (and jsuite_v2nb_test_chat only if short), words ('PP', 'PM'), leak filter. Cluster bootstrap over the bridge entity (10000, seed 0).

Rule (fixed in advance): Per model: gap >= 0.3 and lookup extra loss <= 0.10 -> "the split holds on his passages"; lookup >= 0.20 -> "the lookup follows the lens here"; else in between. Order split (after the gate, before the data): items where the bridge's fact sentence comes before the pointer sentence vs after. "The order pattern replicates" if the lookup's switch under the whole change is >= 2x higher fact-first than fact-after (both CIs), as in our 65-89 % vs 9-19 %. Hard-read stratum (v3 flag): the gap within hard-read items within 0.15 of the easy items -> "not a lookup-difficulty effect".

As computed: Extra loss = X0's excess = Jdep - Rdep = (S_no_jpp_rand - S_no_jpp) / S_whole per reader over the chosen passages (J++: signed OMP, k = 25); switch = the top token is the first token of the other entity's answer; gap = the M reader's extra loss minus the K reader's on the same cluster-bootstrap draws (over the original bridge entity, 10,000 resamples, seed 0, 95% intervals). Point estimates decide (EPS 1e-9); an undefined extra loss (no switch under the whole change) holds no clause ("can't tell"). X0's validity bar (S_whole >= 0.30 and >= 30 switches) per reader beside, not in the rule. Muse: the rule at L26 and at L36, both reported. Z1 order: the K reader's whole-change switch share, fact-first vs fact-after by the original bridge's fact sentence (K passage) against the pointer sentence; replicates iff fact-first >= 2 x fact-after (point estimates; each stratum's interval beside, and whether they separate). Hard-read: no flag in v2, so not tested.

| model | run | status | layer | n (entities) | K extra loss | M extra loss | gap | verdict | K S_whole | M S_whole |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-122b-a10b | qwen35_122b_z1p | tested | 33 | 200 (126) | 0.02 [-0.07, 0.10] | 0.35 [0.28, 0.42] | 0.33 [0.23, 0.44] | the split holds on his passages | 0.33 [0.26, 0.39] | 0.74 [0.68, 0.80] |

## qwen3.5-122b-a10b (qwen35_122b_z1p)

Gate: O's read accuracy {'K': 0.9295238095238095, 'M': 0.9085714285714286} over 525 passages, pass True; over Zach's kept passages {'cases': 237, 'org_read_accuracy': {'K': 0.9873417721518988, 'M': 0.9324894514767933}, 'pass': True, 'eligible': 184}; eligible 377, chosen 200 (sets {'jsuite_v2_test_chat': 187, 'jsuite_v2nb_test_chat': 13}); counts {"jsuite_v2_test_chat": {"passages": 358, "pair_drops": {}, "drops": {"no candidate aligns (the patch token is not at one index in O and S)": 94, "no other entity with another answer": 3}, "cases": 261}, "jsuite_v2nb_test_chat": {"passages": 358, "pair_drops": {}, "drops": {"no candidate aligns (the patch token is not at one index in O and S)": 93, "no other entity with another answer": 1}, "cases": 264}}.

L33: routes {"K": {"none": {"original": 199, "switch": 1}, "whole": {"original": 123, "switch": 65, "other": 12}, "no_jpp": {"original": 141, "switch": 53, "other": 6}, "no_jpp_rand": {"original": 140, "switch": 54, "other": 6}}, "M": {"none": {"original": 200}, "whole": {"switch": 149, "original": 50, "lure": 1}, "no_jpp": {"original": 122, "switch": 78}, "no_jpp_rand": {"original": 69, "switch": 130, "lure": 1}}}
L33 order: fact-first 0.52 [0.42, 0.63] (n 103), fact-after 0.11 [0.05, 0.18] (n 97); ratio 4.62; replicates True; intervals separate True. Hard-read: no hard-read flag in v2 (not tested).

Beside (Zach's stored rows, band L39-45): full qwen35_122b_jsuite_v2_test_chat_ko_cand2_v1: paper10 M-K 0.47 [0.39, 0.55] (joined 184), paper10_rot M-K 0.01 [0.00, 0.02] (joined 184)

