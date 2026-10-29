# Batch 50 Z1P: our change-removal on Zach's passages (UNVERIFIED)

Z1-P (no Q-line: Dan's morning brief, 29 Oct) (batch 52 coverage: no prediction: Z1's rule (verbatim, first scored on the K items, results/x50_zach/z1-20261028T161649Z) applied now to the P items (Dan's morning brief, 29 Oct)). Items: jsuite_v2_test_chat (and jsuite_v2nb_test_chat only if short), words ('PP', 'PM'), leak filter. Cluster bootstrap over the bridge entity (10000, seed 0).

Rule (fixed in advance): Per model: gap >= 0.3 and lookup extra loss <= 0.10 -> "the split holds on his passages"; lookup >= 0.20 -> "the lookup follows the lens here"; else in between. Order split (after the gate, before the data): items where the bridge's fact sentence comes before the pointer sentence vs after. "The order pattern replicates" if the lookup's switch under the whole change is >= 2x higher fact-first than fact-after (both CIs), as in our 65-89 % vs 9-19 %. Hard-read stratum (v3 flag): the gap within hard-read items within 0.15 of the easy items -> "not a lookup-difficulty effect".

As computed: Extra loss = X0's excess = Jdep - Rdep = (S_no_jpp_rand - S_no_jpp) / S_whole per reader over the chosen passages (J++: signed OMP, k = 25); switch = the top token is the first token of the other entity's answer; gap = the M reader's extra loss minus the K reader's on the same cluster-bootstrap draws (over the original bridge entity, 10,000 resamples, seed 0, 95% intervals). Point estimates decide (EPS 1e-9); an undefined extra loss (no switch under the whole change) holds no clause ("can't tell"). X0's validity bar (S_whole >= 0.30 and >= 30 switches) per reader beside, not in the rule. Muse: the rule at L26 and at L36, both reported. Z1 order: the K reader's whole-change switch share, fact-first vs fact-after by the original bridge's fact sentence (K passage) against the pointer sentence; replicates iff fact-first >= 2 x fact-after (point estimates; each stratum's interval beside, and whether they separate). Hard-read: no flag in v2, so not tested.

| model | run | status | layer | n (entities) | K extra loss | M extra loss | gap | verdict | K S_whole | M S_whole |
|---|---|---|---|---|---|---|---|---|---|---|
| nemotron-3.5-lightning | nem35l_x52_z1p | not tested (gate; numbers descriptive only) | 14 | 200 (133) | 0.03 [-0.10, 0.15] | 0.48 [0.41, 0.55] | 0.45 [0.30, 0.60] | the split holds on his passages | 0.38 [0.32, 0.45] | 0.84 [0.78, 0.88] |

## nemotron-3.5-lightning (nem35l_x52_z1p)

Gate: O's read accuracy {'K': 0.7939508506616257, 'M': 0.9224952741020794} over 529 passages, pass False; over Zach's kept passages {'cases': 203, 'org_read_accuracy': {'K': 1.0, 'M': 0.9605911330049262}, 'pass': True, 'eligible': 127}; eligible 249, chosen 200 (sets {'jsuite_v2_test_chat': 129, 'jsuite_v2nb_test_chat': 71}); counts {"jsuite_v2_test_chat": {"passages": 358, "pair_drops": {}, "drops": {"no candidate aligns (the patch token is not at one index in O and S)": 88, "no other entity with another answer": 3}, "cases": 267}, "jsuite_v2nb_test_chat": {"passages": 358, "pair_drops": {}, "drops": {"no candidate aligns (the patch token is not at one index in O and S)": 95, "no other entity with another answer": 1}, "cases": 262}}.

L14: routes {"K": {"none": {"original": 199, "switch": 1}, "whole": {"original": 112, "switch": 76, "other": 12}, "no_jpp": {"original": 138, "switch": 53, "other": 9}, "no_jpp_rand": {"original": 132, "switch": 55, "other": 13}}, "M": {"none": {"original": 200}, "whole": {"other": 7, "switch": 168, "original": 22, "lure": 3}, "no_jpp": {"lure": 8, "original": 111, "other": 9, "switch": 72}, "no_jpp_rand": {"other": 8, "switch": 152, "original": 35, "lure": 5}}}
L14 order: fact-first 0.66 [0.55, 0.77] (n 92), fact-after 0.14 [0.08, 0.21] (n 108); ratio 4.77; replicates True; intervals separate True. Hard-read: no hard-read flag in v2 (not tested).

Beside (Zach's stored rows, band L27-33): full nem35l_jsuite_v2_test_chat_ko_cand2_v1: paper10 M-K 0.70 [0.61, 0.78] (joined 127), paper10_rot M-K 0.02 [-0.02, 0.07] (joined 127)

