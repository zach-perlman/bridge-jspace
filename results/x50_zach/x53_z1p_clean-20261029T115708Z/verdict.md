# Z1-P on the 9B, without the passages whose lookup passage holds the bridge's true value (UNVERIFIED)

Dan, verbatim: "CPU check first (verification): Z1-P on the 9B without the 60 passages where the bridge's true value stands in the lookup's passage as another entity's value: rule verbatim on the remaining 140; report beside the full-set number in the Z1 card, both ways." (Dan 12:50, batch53.yaml docs_1250 item 0)

Rule (Z1's, verbatim): Per model: gap >= 0.3 and lookup extra loss <= 0.10 -> "the split holds on his passages"; lookup >= 0.20 -> "the lookup follows the lens here"; else in between. Order split (after the gate, before the data): items where the bridge's fact sentence comes before the pointer sentence vs after. "The order pattern replicates" if the lookup's switch under the whole change is >= 2x higher fact-first than fact-after (both CIs), as in our 65-89 % vs 9-19 %. Hard-read stratum (v3 flag): the gap within hard-read items within 0.15 of the easy items -> "not a lookup-difficulty effect".

As computed: Extra loss = X0's excess = Jdep - Rdep = (S_no_jpp_rand - S_no_jpp) / S_whole per reader over the chosen passages (J++: signed OMP, k = 25); switch = the top token is the first token of the other entity's answer; gap = the M reader's extra loss minus the K reader's on the same cluster-bootstrap draws (over the original bridge entity, 10,000 resamples, seed 0, 95% intervals). Point estimates decide (EPS 1e-9); an undefined extra loss (no switch under the whole change) holds no clause ("can't tell"). X0's validity bar (S_whole >= 0.30 and >= 30 switches) per reader beside, not in the rule. Muse: the rule at L26 and at L36, both reported. Z1 order: the K reader's whole-change switch share, fact-first vs fact-after by the original bridge's fact sentence (K passage) against the pointer sentence; replicates iff fact-first >= 2 x fact-after (point estimates; each stratum's interval beside, and whether they separate). Hard-read: no flag in v2, so not tested.

Excluded (60 of 200 chosen passages): the run's chosen passages (gate.json order) whose lookup (K) original passage holds the recall's (M) original answer, the bridge's true value, as a whole word, case-insensitive (bridge_jspace.review.items.word_in; the verify check of review/verify_checks.json, recomputed and its count and listed ids asserted); a passage is one paired item (K and M rows), so both readers' rows of an excluded passage are dropped. Ids in excluded.json.

| set | layer | passages (entities) | K (lookup) extra loss | M (recall) extra loss | gap M - K | verdict |
|---|---|---|---|---|---|---|
| full | 12 | 200 (129) | -0.05 [-0.13, 0.03] | 0.59 [0.51, 0.67] | 0.64 [0.51, 0.76] | **the split holds on his passages** |
| without the 60 | 12 | 140 (100) | -0.07 [-0.17, 0.03] | 0.56 [0.46, 0.67] | 0.63 [0.49, 0.78] | **the split holds on his passages** |

L12: the full set recomputed here matches the stored verdict x52_z1p-20261029T081112Z (verdict, n, gap): True.
L12 full: order fact-first 0.60 [0.50, 0.70] (n 96), fact-after 0.05 [0.01, 0.09] (n 104); replicates True; X0's validity bar K True, M True.
L12 clean: order fact-first 0.58 [0.44, 0.70] (n 66), fact-after 0.05 [0.01, 0.11] (n 74); replicates True; X0's validity bar K True, M True.

Status: UNVERIFIED until a human adds it to VERIFIED.md.
