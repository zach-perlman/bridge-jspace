# Batch 50 Z1P: our change-removal on Zach's passages (UNVERIFIED)

Z1-P (no Q-line: Dan's morning brief, 29 Oct) (batch 52 coverage: no prediction: Z1's rule (verbatim, first scored on the K items, results/x50_zach/z1-20261028T161649Z) applied now to the P items (Dan's morning brief, 29 Oct)). Items: jsuite_v2_test_chat (and jsuite_v2nb_test_chat only if short), words ('PP', 'PM'), leak filter. Cluster bootstrap over the bridge entity (10000, seed 0).

Rule (fixed in advance): Per model: gap >= 0.3 and lookup extra loss <= 0.10 -> "the split holds on his passages"; lookup >= 0.20 -> "the lookup follows the lens here"; else in between. Order split (after the gate, before the data): items where the bridge's fact sentence comes before the pointer sentence vs after. "The order pattern replicates" if the lookup's switch under the whole change is >= 2x higher fact-first than fact-after (both CIs), as in our 65-89 % vs 9-19 %. Hard-read stratum (v3 flag): the gap within hard-read items within 0.15 of the easy items -> "not a lookup-difficulty effect".

As computed: Extra loss = X0's excess = Jdep - Rdep = (S_no_jpp_rand - S_no_jpp) / S_whole per reader over the chosen passages (J++: signed OMP, k = 25); switch = the top token is the first token of the other entity's answer; gap = the M reader's extra loss minus the K reader's on the same cluster-bootstrap draws (over the original bridge entity, 10,000 resamples, seed 0, 95% intervals). Point estimates decide (EPS 1e-9); an undefined extra loss (no switch under the whole change) holds no clause ("can't tell"). X0's validity bar (S_whole >= 0.30 and >= 30 switches) per reader beside, not in the rule. Muse: the rule at L26 and at L36, both reported. Z1 order: the K reader's whole-change switch share, fact-first vs fact-after by the original bridge's fact sentence (K passage) against the pointer sentence; replicates iff fact-first >= 2 x fact-after (point estimates; each stratum's interval beside, and whether they separate). Hard-read: no flag in v2, so not tested.

| model | run | status | layer | n (entities) | K extra loss | M extra loss | gap | verdict | K S_whole | M S_whole |
|---|---|---|---|---|---|---|---|---|---|---|
| muse-glimmer-30b | muse30_x53_z1p | not tested (gate; numbers descriptive only) | 26 | 200 (120) | 0.04 [0.00, 0.14] | 0.81 [0.72, 0.90] | 0.77 [0.63, 0.89] | the split holds on his passages | 0.12 [0.09, 0.18] | 0.48 [0.42, 0.55] |

## muse-glimmer-30b (muse30_x53_z1p)

Gate: O's read accuracy {'K': 0.78125, 'M': 0.8584558823529411} over 544 passages, pass False; over Zach's kept passages {'cases': 195, 'org_read_accuracy': {'K': 0.9743589743589743, 'M': 0.882051282051282}, 'pass': True, 'eligible': 110}; eligible 240, chosen 200 (sets {'jsuite_v2_test_chat': 120, 'jsuite_v2nb_test_chat': 80}); counts {"jsuite_v2_test_chat": {"passages": 358, "pair_drops": {}, "drops": {"no candidate aligns (the patch token is not at one index in O and S)": 85, "no other entity with another answer": 3}, "cases": 270}, "jsuite_v2nb_test_chat": {"passages": 358, "pair_drops": {}, "drops": {"no candidate aligns (the patch token is not at one index in O and S)": 83, "no other entity with another answer": 1}, "cases": 274}}.

L26: routes {"K": {"none": {"original": 199, "switch": 1}, "whole": {"original": 165, "switch": 25, "other": 10}, "no_jpp": {"original": 168, "switch": 23, "other": 9}, "no_jpp_rand": {"original": 170, "switch": 24, "other": 6}}, "M": {"none": {"original": 200}, "whole": {"switch": 97, "original": 90, "other": 11, "lure": 2}, "no_jpp": {"original": 181, "other": 11, "switch": 7, "lure": 1}, "no_jpp_rand": {"switch": 86, "original": 97, "other": 15, "lure": 2}}}
L26 order: fact-first 0.21 [0.13, 0.30] (n 98), fact-after 0.04 [0.01, 0.08] (n 102); ratio 5.46; replicates True; intervals separate True. Hard-read: no hard-read flag in v2 (not tested).

Beside (Zach's stored rows, band L36-42): full muse30_jsuite_v2_test_chat_ko_cand2_v1: paper10 M-K 0.52 [0.42, 0.62] (joined 110), paper10_rot M-K -0.01 [-0.03, 0.00] (joined 110)

