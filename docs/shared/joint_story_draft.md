Draft for the Neel drop-in, 27 Oct; UNVERIFIED; numbers cited to their files

# Joint story draft: breadth (Zach) and depth (Dan)

**The joint story is now the root [README.md](../../README.md), the one source of truth.** This file keeps the working notes behind it (term map, overlap table, theses); the critic's lists are in [joint_review_notes.md](joint_review_notes.md).

v2, on danorel (5782c055) after the critic's 22 findings. Nothing here is hand-checked; no number below is established. Interpretations that go beyond a file's own reading are marked "reading".

**Source keys.** D = data/figures/depth/data.csv (figure, model, quantity; or the `numbers` key). Z = docs/breadth/data.csv (`key` column). E l.N = EXPERIMENTS.md line N (one run per line). P45 = predictions/2026-10-26_dan.md (the "Result" line under the question). SBO = docs/split_by_order.md. X0D = docs/x0_details.md. DR = docs/depth/README.md. ZR = docs/breadth/README.md. DG = docs/digest.md. CS = docs/archive/claims_skeleton.md. JS = results/jswap/<run>/summary.json (Zach's stored swap summaries; cells he has not reported). G = docs/shared/grid.csv.

**Status tags.** [FA] fixed in advance (pre-registered rule / amendment). [AD] after the data (descriptive, post hoc, gate lowered, or judged against thresholds written for other models). [US] unsourced (only in prose or a message, not in a results-derived file). A tag after a number applies to the test that produced it.

**Sites.** Ours: one layer, the bridge token only, fixed in advance per model: 9B L12, 27B L32, 122B L33, Muse L26 (P45 batch 39 preamble). His: a band, every token: 27B L32-40, 9B L12-16, Lightning L27-33, Muse L36-42, 122B L39-45 (ZR §7 table). On the 9B and 27B our layer is the first layer of his band; on Muse and the 122B the sites do not overlap.

**Dates.** Experiments freeze Wed 28 Oct evening; hand check Thu 29 Oct (STATUS.md, d0ee653b).

## 1. Term map

| Ours (depth) | His (breadth) | Same thing? | Proposed shared word |
|---|---|---|---|
| **recall**: "How many legs does Iris's pick have?" (answer from memory) | **M final** (the attribute is never stated) | Yes in role. Ours is a templated toy scene; his a passage over real facts. | **recall** (keep), "M final" as his dataset label |
| **lookup**: "Which locker belongs to Iris's pick?" (a number bound in the prompt) | **K final** (the attribute is stated in the passage); on his toy suite also "prompt lookup (thing -> locker)" (E l.73) | Partly. Both read the answer from the prompt, but ours reads an item-locker *binding*, his K reads a stated *attribute sentence*. Only his toy-suite step 2 is our task. | **in-context read** for the reader; keep "lookup" only for our locker task |
| **the change** (add the bridge token's hidden-state difference Δ, one layer, one token) | **swap** (replace the J-part of the mention's last token with another entity's), **paste** (whole residual), **knock-out** (project out top-10 J++ at every token of a band) | No. Our change-removal asks which part of a *transplanted difference* carries its effect; his swap asks the same of a transplanted J-part; his knock-out removes directions from the model's own run. | **transplant** (ours, his swap/paste) vs **knock-out** (his) |
| **J++ part**: 25 signed-OMP J++ atoms that best rebuild Δ | **J-part**: span of the top-10 J++ directions at that token; **complement** (swap_comp) = everything but the J-part | Same lens, different selection (fit to Δ vs top-10 read) and size (25 vs 10) | **J++ part (25, fit to Δ)** / **J++ top-10 span** |
| **extra loss**: share of switches lost without a part minus without a random part of the same share; **gap** = recall − lookup | **M − K**: recall points lost minus stated-fact points lost under the knock-out | Both are "recall cost minus in-context cost"; units differ (fraction of switches beyond a random part vs accuracy points with separate rotated / logit-lens / PCA controls) | **J-specific cost** (state the unit) |
| **pointer** = the **order pointer**: 4 mass-mean directions at the bridge token coding which locker sentence is the item's; outside J++ | **pointer** = the J-part as a context-free pointer to *which entity* (ZR §4) | **Opposite meanings**: his is inside J++ and codes identity; ours is outside J++ and codes order | **entity code** (his), **order pointer** (ours); never bare "pointer" |
| "the lookup" = a reader | "the fact is looked up later" = a stage (the attribute appears at the answer position: after the band on the Qwens, at L32 inside L27-33 on Lightning; ZR §4); "lookups kept" = K/P finals unchanged under his swap | Different | **attribute retrieval** (his stage); "in-context read kept" for "lookups kept" |
| k = number of OMP atoms (25 / 50 / 100) | K = number of top directions (1-300; K\*); also **K** = the stated-fact final | His "K" means two things | **d** = number of directions; K only for the final |
| **layer L** (one layer; L/2, L/4 for sweeps) | **band**: 4 (9B late L26-29) to 12 layers (Bolt L42-53) (ZR §3, §7) | Different site sizes | **site = (layers, tokens)**, e.g. "L12 @ bridge token" vs "L12-16 @ all tokens" |
| **switch** | **transfer** (donor − third) | Analogous outcomes | keep both, name the unit |
| **identity / position / value** (routes answers) | "which entity it is" | His "entity" ≈ our "identity" | **identity** |
| **random part** (same share of ‖Δ‖²) | **rotated**; **size-matched** (same norm along top principal directions) | Both size controls | **size-matched control** (say which) |
| fixed in advance / after the data | pre-registered (amendments 1-57) / after the data | Same | **fixed in advance / after the data** |
| readable (probe), needed (removal), written | readable, carried, needed (ZR §4; CS) | Same axis | **readable / carried / needed**; our change-removal is a *carried* test (reading, §3c) |

## 2. Overlap table

| Question | His evidence | Our evidence | Status (his / ours) | Verdict |
|---|---|---|---|---|
| **Recall vs in-context split** | M − K +50.9 [46, 55] 27B, +42.6 [37, 49] 9B, +53.1 [48, 59] Lightning; stated facts lose 2.6 / 5.0 / 3.7 (Z ko.*.mk, *.klost). Toy suite, the locker lookup step alone keeps 99-100% vs recall 55-63% (27B, E l.73) | Gap 0.53 [0.42, 0.61] 9B, 0.60 [0.50, 0.69] 27B, 0.32 [0.20, 0.43] 122B, 0.85 [0.68, 0.98] Muse; lookup −0.03 / 0.14 / 0.00 / −0.10 (D fig01). X0's strict rule "not confirmed" on the 27B (lookup 0.14 > 0.10; X0D pre-registered tests). Clean design, locker first: 0.23 / 0.53 / 0.38, 2 of 3 (P45 Q45.10) | [FA] / [FA] | **agree** on the direction on the 9B and 27B; ours has a strict-rule miss (27B) and a clean-design miss (9B) |
| **J++ specificity and controls** | Rotated +2.7 / +1.8 / +3.6; logit lens +1.9 / +1.4 / +8.7; same-size PCA 0.24 / 0.17 / 0.15 of the effect (Z ko.*.rot, .u, .pcr) | Recall extra loss: J++ 0.37 / 0.61 / 0.26 / 0.66 vs same-size PCA 0.13 / 0.16 / 0.21 / 0.18 vs logit lens 0.00 / 0.01 / −0.01 / 0.01 (D fig02; 9B / 27B / 122B / Muse). Positive control failed: chemical symbols 27B 0.15, bar 0.20 (DR §6) | [FA] / [FA] | **agree** on the Qwen 9B/27B; both weak on the 122B (ours PCA close; his logit lens +11.8, Z ko.q122.u) |
| **The in-context reader under transplants** | J-part swap: transfer +63.0 / +63.9 / +44.8 on recall (Z swap.*.swap), stated reads kept: 27B PK 99.1%, TK 100% (E l.166); 9B PK 95.8%, TK 96.6% (E l.165). **Complement swap (all but the J-part) moves the stated read**: 27B PK +24.6 [18.6, 31.0], TK +27.3 [20.2, 34.9]; 9B PK +13.9 [7.8, 20.4], TK +1.7 [−11.1, 13.6]; Lightning PK −0.4, TK +2.9, paste also ≈ 0 (JS jswap_v2_v1, qwen35_9b_jswap_v2_v1, nem35l_jswap_v2_v1) | Removing the J++ part leaves the lookup's switches (lookup extra loss above); the lookup answers by identity or position, value share 0.00 on all four (D fig05 whole). Adding only the J++ part moves *neither* reader: lookup identity 0.00 and its random part ~0 (D fig05 keep_jpp, keep_jpp_rand); recall C2 0.07 / 0.02 / 0.10 / 0.02 vs random 0.02 / 0.00 / 0.04 / 0.00 (D numbers rtk_C2_keep_jpp_recall_follows_s_*) | [FA] swap; [AD] complement on K (stored, unreported) / [FA] routes, [AD] keep-only | **partly agree**: on the 27B and 9B what redirects the in-context read lies outside the J++ top-10 (his complement) and the lookup's switch survives J++ removal (ours). Keep-only J++ is too small a dose to act on either reader, so it is not reader evidence. Lightning: nothing at the mention moves its stated read |
| **Earlier / passing mentions** | Deleting the one passing mention adds knock-out loss: 27B +17.6 [10, 26], 9B +11.6 [5, 19], Muse +10.1 [2, 18], Lightning +4.0 [−3, 11], 122B +1.7 [−5, 8] (Z r.*), although the knock-out also removes J++ at that mention ("a passing name protects ~15-20 points", E l.170; named once, the dependence sits "mostly elsewhere", E l.179). Knock-out at the bridge's mention alone, recalled start: 27B +5.8, 9B +10.1, Lightning +1.4 (Z pos.*.M.bridge; reading: for the recalled start the only mention is the passing one) | 45p: with its locker first, removing J++ at the new item's earlier mention loses 0.25 [0.16, 0.34] / 0.41 [0.32, 0.53] / 0.42 [0.26, 0.63] beyond random (9B / 27B / Muse; P45 Q45.13) | [FA] (amendment 35; prediction failed on 27B and 9B) / [FA] | **partly**: both find a mention lowers the recall's dependence on the bridge site. The routes differ: ours runs through J++ at the mention, his survives J++ removal at it. Lightning, 122B ≈ 0 on his side; untested on ours |
| **Depth** | Mid band: read bridges need the mention (9B start P: mention +47.7, question +4.3 of +50.4; Z pos.q9.P.*). Late band: question only (9B L26-29 +52.6 of +53.1, mention +0.2; Lightning L33-39 +52.6 of +61.6; 27B L52-60 question +47.1, mention +2.9; Z late.*, pos.q27late.*), but largely shared with the logit lens: 9B +27.5 of +53.1, Lightning +22.9 of +61.6 (Z late.q9.all.u, late.nl.all.u); 9B stated facts lose 9 (E l.245) | 45q (clean, locker after): locker-sentence copy at L switches 0.70 / 0.74 / 0.76 of S's lookups, bridge-word change 0.17 / 0.01 / 0.01 (P45 Q45.12). 9B sweep: bridge change 0.93 (L4) → 0.36 (L8) → 0.17 (L12) → 0.02 (L16) (D fig03b). Locker-first main test: the bridge change still switches 65-89% of lookups (DR §2) | [FA] (amendments 30, 36, 37, 57) / [FA] (45q rule), [AD] (sweep) | **partly**: same shape ("later tokens take over from the bridge token"), different readers and destinations; his late effect is half logit-lens-shared |
| **Margin / probability** | By probability +50.3 / +35.3 / +44.1; Muse +49.4; **122B +1.7 [0, 4]** (Z ko.*.soft) | Logit-difference gap 0.48 / 0.47 / 0.33 / 0.61 (D fig01b ld_gap_*); p_alt gap 0.51 / 0.53 / 0.34 / 0.73 (X0D "switch as a probability") | [FA] / [FA] ld (P45 Q39.1; D fig11 "fixed"), [AD] p_alt | **agree** except the 122B (**conflict**, different sites) |
| **Chat template** | 9B raw-text QA M − P +38 vs chat +42 on jsuite v1 (E l.140, amendment 26: M − P, not M − K); 27B not testable (thinks, E l.141); 9B base in raw text M − K +35 [30, 40] on v2 (E l.163, judged post hoc) | Our fixed test (Q45.8) was "(d) not tested" (both models missed the 0.80 gate). Descriptive reruns at gate 0.75: gap 0.52 [0.39, 0.62] 9B, 0.62 [0.49, 0.74] 27B (P45 45i'; D s01c). Routes runs without the template passed the 0.80 gate: value 0 of 300 on both (P45 Q45.8; D fig11) | [FA] (9B, v1) / [AD] split, routes descriptive | **agree in direction, weakly**: on our side only after the data; on his only the 9B |
| **Muse** | v2 M − K +59.9 [55, 65], but the logit lens gives +34.6 (Z ko.mu.mk, ko.mu.u; E l.169 "logit-lens control FAILS badly"). Toy suite: gap 7 (E l.87); bridge removed 90-100% yet accuracy 91%, back at rank 0 two layers on (E l.99). Swap: L14-20 +50.3; L36-42 "uninformative" (paste moved nothing either); L7-13 TM +15.6 [2.6, 29.4] (E l.161) | Gap 0.85 [0.68, 0.98]; recall J++ 0.66 vs logit lens 0.01 (D fig01, fig02); 45q link from about L/2 (copy at L/2 0.47; P45 Q45.12) | [AD] (v2 judged post hoc; swaps exploratory) / [FA] | **conflict on lens specificity at different layers** (his needed but half logit-lens-shared at L36-42; ours J++-specific at L26); "not needed" is toy-suite only. 45r drafted to compare them (Q45.16) |
| **122B** | v2 M − K +48.5 greedy but +1.7 by probability (Z ko.q122.mk, .soft); L24-30 only +4.2 (E l.173). Toy suite: accuracy under the knock-out 86% at L39-45; the bridge's rank returns 4 layers on only at L24-30, where removal was 16% / 60% (E l.110, "redundant routes or a rebuild", descriptive). Swap (jsuite v1) +44.3, stated reads kept 97-100% (E l.162) | Gap 0.32 [0.20, 0.43]; J++ 0.26 vs PCA 0.21 (not specific, D fig02); routes and fresh scenes at gate 0.75, after the data (DR §3 note; SBO) | [AD] (v2 post hoc) / [FA] main, [AD] routes | **partly / conflict**: both weak, each with a failed control; neither should build on it |
| **9B** | Split +42.6; mid-band dependence at the mention; no rebuild (span rank 7 → 636, accuracy 47%; E l.111) | Gap 0.53 main test, but the clean design misses (0.23 [0.14, 0.31], bar 0.3; P45 Q45.10) and the one-pick fresh-scene rerun gives recall 0.12 (SBO; duplicate-pick design, both lockers first, Q45.2 caveat) | [FA] / [FA] | **partly**: his 9B is clean; ours is fragile in locker-first scenes (reading: consistent with §3d) |
| **More directions on the 27B** | Stated facts lost on the 27B: 2.0 at K 10, 20.0 at K 100 (by probability 6.4 → 37.9; Z dose.q27.k10.K, k100.K, *.sK). Generic: "more directions add damage that is not specific"; Lightning stated facts lose 50 by probability at 100, DeepSeek 17 (ZR §5) | 27B lookup extra loss 0.12 / 0.30 / 0.60 at k 25 / 50 / 100; another scene's 100 atoms −0.01 (D fig02b); about 0 on the other models (P45 Q45.9) | [FA] (amendment 54) / [FA] (45k: "can't tell") | **different findings**: his cost at 100 is generic damage across models; ours is 27B-only and specific to the scene's own atoms |

## 3. Candidate joint theses (recomputed after the fixes)

### a. Double dissociation

Claim: removing J++ costs recall, not the in-context reader; removing the order pointer costs the lookup's position answers, much less the recall; his J-part swap moves recall while in-context reads keep their answer.

- **Verdict: partly supported.** The J++ side has known misses. The pointer side holds on three of four models, not the 27B. The swap side now has a mirror: on the Qwens the stated read moves with the complement, not the J-part.
- Deciding numbers:
  - J++ side: recall vs lookup extra loss 0.50 / 0.74 / 0.32 / 0.75 vs −0.03 / 0.14 / 0.00 / −0.10 (D fig01) [FA]. His toy-suite locker step keeps 99-100% vs recall 55-63% (E l.73) [FA].
  - Pointer side (sanity swap): lookup extra loss without the pointer 0.31 / 0.15 / 0.26 / 0.28 vs recall 0.12 / 0.15 / 0.14 / 0.03 (D s10, 9B / 27B / 122B / Muse) [AD; replicated in advance on the 9B and Muse per DR §4].
  - Swap side: J-part swap moves recall (+63.0 / +63.9), stated reads kept (99.1% / 95.8% PK). The complement moves the stated read instead: PK +24.6 (27B), +13.9 (9B) (JS) [FA swap, AD complement].
- Strongest counter-evidence:
  - X0's strict rule is "not confirmed" on the 27B (lookup 0.14). The 9B misses the clean design (0.23) and gives recall 0.12 in the one-pick rerun. The 122B is not specific against PCA (0.26 vs 0.21) (X0D; P45 Q45.10; SBO; D fig02).
  - The lookup's J++-independence is measurable only where the locker comes first (lookups switched 9-19% when it comes after; X0D Tier 0).
  - DR §6 limits: "reader and answer source (prompt vs memory) confounded". The positive control (chemical symbols) failed (27B 0.15, bar 0.20).
  - On the 27B the pointer costs recall as much as the lookup (0.15 vs 0.15). His stated reads are attribute sentences, not our binding; Lightning's stated read moves under no transplant at the mention.
- Credence: **low-medium** (J++ half medium, pointer half medium-low).
- Best figure: figures/depth/fig05_routes.png, with figures/breadth/fig05_carries.png.

### b. The model holds the entity twice

Claim: a lens-readable code the recall reads, and a code outside the lens (plus an order pointer) the lookup reads.

- **Verdict: weakly supported.** The lens-readable entity code is well supported (his). Something outside the J++ top-10 redirects the in-context read on the Qwens (his complement, our routes). Our "identity outside J++" is not specific, and the recall also uses the identity direction, so the split is not clean.
- Deciding numbers:
  - Neutral-donor J-part transfers 1.094 / 1.099 of the same-passage swap (Z ptr.q27.neutral, ptr.q9.neutral) [FA].
  - Complement swap moves the 27B stated read +24.6 / +27.3 (PK / TK) vs the J-part +0.9 / 0.0 (JS jswap_v2_v1) [AD].
  - Removing J++ + pointer + identity outside J++ leaves 0.07 / 0.18 / 0.52 of lookups switching (9B / 27B / Muse), against 0.16 / 0.38 / 0.59 with a wrong-pair direction in place of identity (D fig10; DR §5) [FA arms; the bar was out of reach, P45 Q40.1]. The 122B arms are at gate 0.75, after the data, with no wrong-pair control (0.22; DR §5).
  - 45e: identity outside J++ cuts identity answers only 0.06 / 0.12 / 0.04 beyond the wrong pair (bar 0.15; P45 Q45.7) [FA, failed].
- Strongest counter-evidence:
  - The recall loses a lot without the identity direction: 0.44 [0.34, 0.55] (27B), 0.39 [0.28, 0.49] (Muse); 0.09 (9B), 0.12 (122B) (DR §5; P45 Q40.3). The same direction serves both readers on two models.
  - On the 27B, removing the J++ part cuts identity answers from 0.66 to 0.45 vs 0.70 for a random part (D fig02b no_jpp, no_jpp_rand), so part of the lookup's identity route is lens-readable.
  - His complement also carries position and binding (his own reading of the Lightning paste, ZR §4), so it does not isolate an entity code.
- Credence: **low.**
- Best figure: figures/depth/fig10_what_is_left.png.

### c. "Carried, not needed"

Claim: our change-removal and his knock-out disagree on Muse and the 122B, the two models where he found the bridge rebuilt after removal.

- **Verdict: partly supported, narrower than stated.**
  - "Not needed" holds only on his toy suite (Muse gap 7, E l.87; 122B accuracy 86%, E l.110). On v2 his knock-out costs Muse +59.9 and the 122B +48.5 greedy.
  - The live disagreement on Muse is lens specificity at different layers: his logit lens gives +34.6 of +59.9 at L36-42; our J++ part vs logit lens is 0.66 vs 0.01 at L26.
  - On the 122B both sides are weak.
- Reading (not tested): our change-removal asks which part of a transplanted Δ carries the switch. That makes it a *carried* test (like his swap), not a *needed* test (like his knock-out).
- Deciding numbers:
  - Muse: ours 0.66 vs 0.01 (D fig02) [FA]; his +59.9 / +34.6 (Z ko.mu.mk, ko.mu.u) [AD, post hoc]; toy gap 7 (E l.87).
  - 122B: ours J++ 0.26 vs PCA 0.21 (D fig02) [FA]; his +48.5 greedy / +1.7 by probability (Z) [AD].
- 45r (drafted, not queued; jobs/c3/x45r_*.yaml, Q45.16) tests this on Muse.
  - Dan's decisions [US: given in the coordinator's message of 27 Oct, not yet in the committed specs, which still name L26 and L36-42 with a two-sided "within 10"]: the rule reads his knock-out on band L23-29 with all controls against our stored L26 gap 0.85. "Within 10" is one-sided: his J++ M − K minus logit-lens M − K ≤ 10.
  - GPU estimate in the committed specs: 0.25 + 0.6 (+0.55 optional) h.
- Strongest counter-evidence: different sites (L26 vs L36-42; L33 vs L39-45 / L24-30); the 122B rebuild is descriptive and seen at L24-30, not at its band (E l.110).
- Credence: **medium** for "our test is a carried test"; **low** for "Muse/122B carry but do not need J++".
- Best figure: none shows both; nearest figures/breadth/fig08_readable.png next to figures/depth/fig02_specificity.png.

### d. Earlier mentions

Claim: our 45p (the recall reads the earlier mention's J++) vs his passing-mention results.

- **Verdict: partly supported, on one statement only:** an earlier mention lowers the recall's dependence on the bridge site. The routes disagree. Ours goes through J++ at the mention. His protection survives the knock-out removing J++ at the mention (E l.170, l.179), and knocking out the passing mention alone costs little (27B +5.8, Lightning +1.4; Z pos.*.M.bridge, reading).
- Deciding numbers:
  - 45p: 0.25 / 0.41 / 0.42 beyond random, 0.26 / 0.49 / 0.49 beyond another item's token; the lookup moves at most 0.01 (P45 Q45.13) [FA].
  - With the locker first, the recall needs J++ at the bridge less on every model: 0.35 / 0.67 / 0.20 / 0.68 vs 0.65 / 0.81 / 0.41 / 0.80 (SBO) [AD].
  - His RM − MM: 27B +17.6, 9B +11.6, Muse +10.1, Lightning +4.0 [−3, 11], 122B +1.7 [−5, 8] (Z r.*) [FA; it predicted ≤ 10 and failed on the 27B and 9B].
- Where Lightning breaks it: no protection (+4.0), as on the 122B (+1.7) and the 9B base (−1; E l.170). We have no Lightning runs; no 45p on the 122B. Our 122B still shows the order effect (0.20 vs 0.41).
- Strongest counter-evidence: the designs differ (deleting a sentence changes competence by 5-20 points, E l.170, vs an in-place edit); no common unit.
- Credence: **low-medium.**
- Best figure: figures/depth/fig03c_earlier_mention.png.

### e. Information moves later with depth

Claim: our 45q (the link moves into the locker sentences by L) vs his late bands (the dependence moves from the mention to the question).

- **Verdict: partly supported, weak as a joint claim.** The shape is shared; the readers, destinations and conditions differ.
- Deciding numbers:
  - Ours: the 9B bridge-word change switches 0.93 / 0.36 / 0.17 / 0.02 of lookups at L4 / 8 / 12 / 16, the locker-sentence copy 0.03 / 0.48 / 0.70 / 0.59 (D fig03b) [AD]. 45q holds 3 of 3 [FA], on clean locker-after scenes only. In locker-first main-test scenes the bridge change still switches 65-89% of lookups at L (DR §2).
  - His: mid band, 9B mention +33.6, question +6.2 of +42.6 (Z pos.q9.all.*). Late band: question +52.6, mention +0.2 (Z late.q9.*) [FA, amendment 57]. The late effect is shared with the logit lens (+27.5 of +53.1 on the 9B, +22.9 of +61.6 on Lightning; Z late.*.all.u), and the 9B's stated facts lose 9 there (E l.245).
- Cross-check (reading), stated as carried, not needed: at the 9B's L12 the recall's switch still travels through the bridge token's J++ part (clean, locker after, 0.79; X0D 45m). His recall needs the mention there (+33.6 at L12-16). In clean locker-after scenes the lookup's switch has already left the bridge token.
- Strongest counter-evidence:
  - Different readers and destinations.
  - Muse makes its link from about L/2 (P45 Q45.12).
  - "Moves rightward with depth" is the default for a causal transformer.
  - Our first test (45b) was a design error and is withdrawn (P45 Q45.5).
  - His late dependence is half logit-lens-shared.
- Credence: **low-medium** for the shape, **low** as a joint mechanism.
- Best figure: figures/depth/fig03b_layers.png, with figures/breadth/fig04_where.png.

### f. Methods lessons

- **Verdict: supported as lessons, not as findings.**
- Removal size vs number of directions:
  - Bolt's top 10 remove 5.6% of the residual vs 12.7-19.6% elsewhere (Z size.*). Bolt at 100: J++ +31 vs same-size PCA +24; DeepSeek +29 vs +26 (ZR §5) [FA].
  - More directions add generic damage on his side (Lightning stated facts −50 by probability at 100; ZR §5).
  - Ours: the 27B lookup's loss at k 100 is specific to the scene's own atoms (another scene's: −0.01; D fig02b) and absent on the other models (P45 Q45.9).
  - Lesson: report removal size and a same-size control at every d, and say whether a large-d cost is generic or specific. The two tracks' 27B large-d results are not the same finding.
- Readable vs carried vs needed:
  - His: OLMo carries (swap +41) but does not need (+5) (ZR §4); probe subspace +8.3 vs J++ +74.8 (Z probe.q27.*).
  - Ours: a probe reads the order pointer in 0.92-0.99 of scenes (layout alone 0.53; DR §4; D v4_b_before_9b 0.97); the lens does not. Removing it cuts position answers to near zero on the Qwens and halves them on Muse (0.27 vs 0.55; D fig05).
- Bar reachability: two of our fixed questions were out of reach at their share (P45 Q40.1, Q45.1); his plateau rule judged specificity by greedy answers (ZR §8).
- Credence: **high** (as lessons).
- Best figure: figures/breadth/fig09_dose.png.

### Internal tensions

- **His, 24 Oct vs 26 Oct.**
  - 24 Oct (E l.153, l.157): the J-part "carr[ies] the recalled attribute, not the identity (lookups stay)".
  - 26 Oct (E l.214, l.224; ZR §4): it carries "which entity it is".
  - ZR §1 still says knocked-out models "still know which entity it is, but not its fact". Its evidence is that they rarely name the bridge, which does not show the model knows the entity.
  - His own complement result suggests a resolution: stated reads are kept under the J-part swap because they move with the complement (27B +24.6), not because the J-part lacks identity.
- **Ours.**
  - DR "In one minute": "Recall uses the part the lens can read on all four models by rules fixed in advance (clean design: two of three)". But X0's strict rule is "not confirmed" on the 27B, because its *lookup* loses 0.14 (bar 0.10; DR §1). The 9B misses the clean design (0.23) and the one-pick replication (0.12).
  - DR §1 calls the logit-difference score not fixed in advance; Q39.1 was committed before computing and D fig11 marks it "fixed".
  - 45b's score stays "right" though its claim is withdrawn (P45 Q45.5).
- **Across tracks.** Muse: our J++-specific split at L26 vs his logit-lens-shared knock-out at L36-42. The two cannot both be the model-level summary until 45r reads them at overlapping layers.

## 4. Unique findings and what not to claim

**Ours (depth):**

1. The lookup never answers with the moved value; it splits between identity and position. Identity / position: 9B 0.48 / 0.51, 27B 0.66 / 0.34, 122B 0.61 / 0.38, Muse 0.44 / 0.54; value 0.00 on all four (D fig05 whole) [FA routes; 122B gate 0.75, AD].
2. An order pointer outside the lens.
   - A probe reads it at 0.92-0.99 (DR §4).
   - Removing it cuts position answers to 0.08 / 0.06 / 0.05 / 0.27 vs 0.54 / 0.25 / 0.36 / 0.55 for a random part (D fig05) [AD; replicated in advance on the 9B and Muse].
   - A fixed write moves the lookup to the target locker: at s = 2, 0.46 / 0.24 / 0.50 / 0.52 of writes; at s = 4, 0.73 / 0.50 / 0.66 / 0.52; a random direction 0.00-0.01 (X0D "The pointer: removed, added alone, written"). DR §4: "a quarter to a half of the writes at a real change's size" [AD].
   - The fixed-in-advance dose s = 1 was below a real change (s\* 1.04-2.76) and moved almost nothing (0.02 / 0.00 / 0.01 / 0.05 over random; P45 Q44.1, a design error).
3. On clean locker-after scenes the binding is made in the locker sentences: copy 0.70 / 0.74 / 0.76 vs bridge 0.17 / 0.01 / 0.01 (P45 Q45.12) [FA].
4. When its locker comes first, the recall reads the item's earlier mention through J++ (P45 Q45.13) [FA].
5. What the prompt names first matters.
   - The rule fixed in advance on what the pointer marks came out "mixed": the neutral sentence also cuts it on the 9B and 27B (P45 Q45.3) [FA].
   - After the data, with the whole change, a pick sentence naming an item first moves the Qwens' lookup to identity: 0.85-0.97 of answers vs 0.54 / 0.65 (X0D 45a table) [AD]. This is a whole-change share, not a pointer measurement.

**His (breadth):**

1. The split on three models from two families with the full control set, three renderings and row-identical clean reruns on the 27B and 9B (ZR §1-2; Z ko.*) [FA].
2. A context-free entity code: a neutral one-sentence donor works as well (1.09 / 1.10 / 1.01). It is not the answer token: swap_noans +63.1 vs swap +63.0 (E l.177) [FA].
3. Decodable is not carried: probe subspace +8 / +6 / +2 vs J++ +75 / +80 / +62 (ZR §4) [FA].
4. Three hops, mostly on Lightning: it meets the pre-registered last-hop rule on v2, a second seed and the natural set (P→P→M +60 vs M→M→P −2 on v2; ZR §6) [FA]. Caveats:
   - The 27B misses P→P→M on both seeds (+8 [−4, 21], +9 [−4, 23]), and its M→M→P loses +20, not predicted.
   - Lightning's controls explain part of two cells: M→P→M rotated +29, logit lens +28 on v2; P→P→M logit lens +32 on the natural set.
   - The 9B cannot be read. Lightning's counting costs +12, a failed prediction (ZR §6, §8).
   - A number computed from the passage needs no J++ to be reported (0 / 0 / 0; ZR §6) [FA].
5. Graded across nine models, with size-matched dose controls (Bolt, DeepSeek) and a late-band question dependence in two families, half shared with the logit lens (ZR §3, §5; Z late.*.u) [FA].

**Neither of us should claim:**

- That J++ is "the" workspace, or that it is necessary for all recall (CS).
- Anything model-level about the 122B: his probability score fails (+1.7); our PCA control nearly matches J++.
- That Muse does or does not "need" J++ before 45r. Ours is J++-specific at L26; his is half logit-lens-shared at L36-42; "not needed" is toy-suite only.
- That identity outside J++ is a specific code (45e failed, 0 of 3), or that the recall and lookup use separate identity codes (the recall loses 0.44 / 0.39 without the identity direction).
- That the order pointer exists in natural text: the simple-scene pointer barely transfers (P45 Q42.1); a refit pointer is found on the 9B and Muse only (X0D 45d).
- That the two tracks' large-d 27B costs are one finding.
- Any result as established: all are UNVERIFIED; our predictions score a mean Brier 0.32, worse than always answering 50% (DR §7).

## 5. Questions for Neel

Each question is tied to a decision due before the experiments freeze (Wed 28 Oct evening) or the hand check (Thu 29 Oct) (STATUS.md, d0ee653b).

1. **One well-checked mechanism on fewer models, or the broad map of where it holds?** Decision before the freeze: where the last GPU hours go (45r on Muse, 45s on Lightning once Zach's lens file arrives [US: coordinator message], or nothing), and which spine the joint write-up takes.
   - The only models where both methods sit at the same site are the 9B and 27B. Each has a known miss on our side: the 27B misses the strict lookup bar; the 9B misses the clean design.
   - Muse is our largest gap but conflicts with his on lens specificity.
2. **Is "carried vs needed" a finding or a methods footnote, and is 45r the right last experiment?** Decision before the freeze: queue 45r (0.25 + 0.6 GPU-h in the committed specs, + 0.55 optional; jobs/c3/x45r_*.yaml; Q45.16 still has no Dan answer) or drop it.
   - Under Dan's decisions [US], 45r reads his knock-out on L23-29 with every control against our stored L26 gap, one-sided "within 10".
   - Neel's answer decides whether §3c goes in the abstract.
3. **Is the toy locker setting acceptable for the mechanism if the split itself replicates on natural text?** Decision before the hand check: whether mechanism claims are scoped "in templated scenes".
   - Our split in natural passages: 9B 0.52, 27B 0.27, 122B 0.44; Muse not testable (10 lookup switches) (G "natural passages").
   - The pointer must be refit per format (X0D 45d). His split holds on natural passages (ZR §2).
4. **Which control would most change his view of the lens-invisible order pointer?** Decision before the freeze: which one control we cite (or run on CPU) to defend Fig. 7. Options:
   - P_cf shares about 2 of 4 directions with the mass-mean pointer (P45 Q43.1);
   - writes at a real change's size (s = 2: 0.24-0.52; X0D);
   - a wrong-pair direction of the same size (failed for identity, P45 Q45.7);
   - the pointer measured on his toy-suite locker items (not run).
5. **(optional) Which word wins for "pointer"?** Decision before the hand check: the shared glossary (§1: "entity code" vs "order pointer").

## Critic's list

Moved to [joint_review_notes.md](joint_review_notes.md). The joint story itself is now the root [README.md](../../README.md).
