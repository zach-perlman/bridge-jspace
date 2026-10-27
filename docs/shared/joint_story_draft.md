Draft for the Neel drop-in, 27 Oct; UNVERIFIED; numbers cited to their files

# Joint story draft: breadth (Zach) and depth (Dan)

Built from the files at cc56ffb0. Nothing here is hand-checked; no number below is established. Interpretations that go beyond a file's own reading are marked "reading".

**Source keys.** D = figures/story/data.csv (figure, model, quantity; or the `numbers` key). Z = docs/breadth/data.csv (`key` column). E l.N = EXPERIMENTS.md line N (one run per line). P45 = predictions/2026-10-26_dan.md (the "Result" line under the question). SBO = docs/split_by_order.md. X0D = docs/x0_details.md. DR = docs/depth/README.md. ZR = docs/breadth/README.md. DG = docs/digest.md. CS = docs/claims_skeleton.md.

**Status tags.** [FA] fixed in advance (pre-registered rule / amendment). [AD] after the data (descriptive, post hoc, gate lowered, or judged against thresholds written for other models). [US] unsourced (only in prose or the brief, not in a results-derived file). A tag after a number applies to the test that produced it.

**Sites.** Ours: one layer, the bridge token only, fixed in advance per model: 9B L12, 27B L32, 122B L33, Muse L26 (P45 batch 39 preamble). His: a band, every token: 27B L32-40, 9B L12-16, Lightning L27-33, Muse L36-42, 122B L39-45 (ZR §7 table). On the 9B and 27B our layer is the first layer of his band; on Muse and the 122B the sites do not overlap.

## 1. Term map

| Ours (depth) | His (breadth) | Same thing? | Proposed shared word |
|---|---|---|---|
| **recall**: "How many legs does Iris's pick have?" (answer from memory) | **M final** (memory final; the attribute is never stated) | Yes in role. Ours is a templated toy scene; his a passage over real facts. | **recall** (keep), "M final" as his dataset label |
| **lookup**: "Which locker belongs to Iris's pick?" (answer is a number bound in the prompt) | **K final** (the attribute is stated in the passage); on his toy suite also "prompt lookup (thing -> locker)" (E l.73) | Partly. Both read the answer from the prompt, but ours reads an item-locker *binding*, his K reads a stated *attribute sentence*. Only his toy-suite step 2 is our task. | **in-context read** (or "stated read") for the reader; keep "lookup" only for our locker task |
| **the change** (add the bridge token's hidden-state difference Δ, one layer, one token) | **swap** (replace the J-part of the mention's last token with another entity's), **paste** (whole residual), **knock-out** (project out top-10 J++ at every token of a band) | No. Our change-removal asks which part of a *transplanted difference* carries its effect; his swap asks the same of a transplanted J-part; his knock-out removes directions from the model's own run. | **transplant** (ours, his swap/paste) vs **knock-out** (his) |
| **J++ part**: 25 signed-OMP J++ atoms that best rebuild Δ | **J-part**: span of the top-10 J++ directions at that token | Same lens, different selection (fit to Δ vs top-10 read) and size (25 vs 10) | **J++ part (25, fit to Δ)** / **J++ top-10 span** |
| **extra loss**: share of switches lost without a part minus without a random part of the same share; **gap** = recall − lookup | **M − K**: recall points lost minus stated-fact points lost under the knock-out | Both are "recall cost minus in-context cost", but ours is a fraction of switches beyond a random part, his accuracy points with rotated / logit-lens / PCA controls run separately | **J-specific cost** (state unit: fraction of switches vs points) |
| **pointer** = the **order pointer**: 4 mass-mean directions at the bridge token that code which locker sentence is the item's; outside J++ | **pointer** = the J-part as a context-free pointer to *which entity* (ZR §4) | **Opposite meanings**: his pointer is inside J++ and codes identity; ours is outside J++ and codes order | **entity code** (his) and **order pointer** (ours); never bare "pointer" |
| "the lookup" = a reader (question type) | "the fact is looked up later" = a processing stage (the attribute appears at the answer position after the band, ZR §4); "lookups kept" = K/P finals unchanged under his swap | Different | **attribute retrieval** (his stage); "in-context read kept" for his "lookups kept" |
| k = number of OMP atoms (25 / 50 / 100) | K = number of top directions (1-300; K\* plateau); also **K** = the stated-fact final | His "K" means two things | **d** = number of directions; K only for the final |
| **layer L** (one layer; L/2, L/4 for sweeps) | **band** (6-9 consecutive layers); "mid band", "late band" | Different site sizes | **site = (layers, tokens)**, e.g. "L12 @ bridge token" vs "L12-16 @ all tokens" |
| **switch** (the model gives the changed prompt's answer) | **transfer** (share answering the donor's fact minus a third entity's) | Analogous outcome measures | keep both, name the unit |
| **identity / position / value** (routes test answers) | "which entity it is" | His "entity" ≈ our "identity" | **identity** |
| **random part** (same share of ‖Δ‖²) | **rotated** removal; **size-matched** = same norm along top principal directions | Both are size controls; ours matched per item | **size-matched control** (say which) |
| fixed in advance / after the data | pre-registered (amendments 1-57) / after the data | Same | **fixed in advance / after the data** |
| readable (probe), needed (removal), written (writes) | readable, carried, needed (ZR §4; CS "Methods lessons") | Same axis | **readable / carried / needed**, with our change-removal counted as a *carried* test (reading, §3c) |

## 2. Overlap table

| Question | His evidence | Our evidence | Status (his / ours) | Verdict |
|---|---|---|---|---|
| **Recall vs in-context split** | M − K +50.9 [46, 55] 27B, +42.6 [37, 49] 9B, +53.1 [48, 59] Lightning; stated facts lose 2.6 / 5.0 / 3.7 (Z ko.q27.mk, ko.q9.mk, ko.nl.mk, *.klost). Toy suite, locker lookup step alone 99-100% kept vs recall 55-63% (27B, E l.73) | Gap 0.53 [0.42, 0.61] 9B, 0.60 [0.50, 0.69] 27B, 0.32 [0.20, 0.43] 122B, 0.85 [0.68, 0.98] Muse; lookup extra loss −0.03 / 0.14 / 0.00 / −0.10 (D fig01 gap, lookup extra loss). Clean design, locker first: 0.23 / 0.53 / 0.38, 2 of 3 pass (P45 Q45.10) | [FA] / [FA] (main), [FA] (clean) | **agree** on the 9B and 27B; scope differs (his 3 models strong, ours 4 models incl. Muse and 122B) |
| **J++ specificity and controls** | Rotated +2.7 / +1.8 / +3.6; logit lens +1.9 / +1.4 / +8.7; same-size PCA 0.24 / 0.17 / 0.15 of the effect (Z ko.*.rot, .u, .pcr; 27B / 9B / Lightning) | Recall extra loss: J++ 0.37 / 0.61 / 0.26 / 0.66 vs same-size PCA 0.13 / 0.16 / 0.21 / 0.18 vs logit lens 0.00 / 0.01 / −0.01 / 0.01 (D fig02; 9B / 27B / 122B / Muse) | [FA] / [FA] | **agree** on the Qwen 9B/27B; both weak on the 122B (ours PCA close; his logit lens +11.8, Z ko.q122.u) |
| **The in-context reader under his swap vs our routes** | J-part swap moves recall (transfer +63.0 27B, +63.9 9B, +44.8 Lightning; Z swap.*.swap) while in-context reads are kept: 27B PP 100, PK 99.1, TP 100, TK 100% (E l.166); 9B PP 98.8, PK 95.8, TP 98.2, TK 96.6% (E l.165) | Adding only the J++ part gives 0.00 identity answers on all four models (D fig05 keep_jpp identity share); lookup answers by identity or position, value share 0.00 on all four (D fig05 whole: value share) | [FA] / [FA] (routes), [AD] (keep-only arms; DR §3: "the rest after the data") | **agree**: J++ alone does not redirect the in-context reader in either design. His 24 Oct reading ("not the identity") conflicts with his own 26 Oct reading; ours supplies a route (identity outside J++ + order pointer) |
| **Earlier / passing mentions** | Deleting the one passing mention adds recall loss: 27B +17.6 [10, 26], 9B +11.6 [5, 19], Muse +10.1 [2, 18], Lightning +4.0 [−3, 11], 122B +1.7 [−5, 8] (Z r.*); rotated / logit lens within [−2, +3] (E l.170) | 45p: with its locker first, removing J++ at the new item's earlier mention loses 0.25 [0.16, 0.34] / 0.41 [0.32, 0.53] / 0.42 [0.26, 0.63] beyond random (9B / 27B / Muse; P45 Q45.13) | [FA] (amendment 35; prediction failed on 27B and 9B) / [FA] | **partly**: same direction on 9B, 27B, Muse; Lightning and 122B ≈ 0 on his side, untested on ours |
| **Depth** | Mid band: read bridges need the mention (9B start P: mention +47.7, question +4.3 of +50.4; Z pos.q9.P.*). Late band: question only (9B L26-29 +52.6 of +53.1, mention +0.2; Lightning L33-39 +52.6 of +61.6; 27B L52-60 question +47.1, mention +2.9; Z late.*, pos.q27late.*) | 45q (clean, locker after): locker-sentence copy at L switches 0.70 / 0.74 / 0.76 of S's lookups, bridge-word change 0.17 / 0.01 / 0.01 (P45 Q45.12); 9B sweep: bridge change 0.93 (L4) → 0.36 (L8) → 0.17 (L12) → 0.02 (L16) (D fig03b) | [FA] (amendments 30, 36, 37, 57) / [FA] (45q rule), [AD] (sweep) | **partly**: same shape ("the bridge token stops mattering, later tokens hold it"), different readers and destinations |
| **Margin / probability** | By probability +50.3 / +35.3 / +44.1; Muse +49.4; **122B +1.7 [0, 4]** (Z ko.*.soft) | Logit-difference gap 0.48 / 0.47 / 0.33 / 0.61 (D fig01b ld_gap_*); p_alt gap 0.51 / 0.53 / 0.34 / 0.73 (X0D "switch as a probability") | [FA] / [FA] for ld (P45 Q39.1; D fig11 "fixed"), [AD] for p_alt | **agree** except the 122B (**conflict**, different sites) |
| **Chat template** | 9B raw-text QA +38 vs chat +42 (E l.140, amendment 26); 27B not testable (thinks, E l.141); 9B base in raw text +35 [30, 40] (E l.163, judged post hoc) | Without the template (gate lowered to 0.75): gap 0.52 [0.39, 0.62] 9B, 0.62 [0.49, 0.74] 27B; value answers 0 of 300 on both (P45 45i'; D s01c, fig11) | [FA] (9B) / [AD] | **agree** (9B both; 27B only ours) |
| **Muse** | v2 M − K +59.9 [55, 65] but logit lens +34.6 (Z ko.mu.mk, ko.mu.u); toy suite gap 7, "barely moves at any depth" (E l.87); bridge removed 90-100% yet accuracy 91%, back at rank 0 two layers on (E l.99); swap carries only at L14-20 (+50.3), nothing at L36-42 (E l.161) | Gap 0.85 [0.68, 0.98]; recall J++ 0.66 vs logit lens 0.01 (D fig01, fig02); 45q link from about L/2 (copy at L/2 0.47; P45 Q45.12) | [AD] (v2 judged post hoc; L14-20 swap exploratory) / [FA] | **conflict** on "needed"; agree on "carried" at mid depth (see §3c) |
| **122B** | v2 M − K +48.5 greedy but +1.7 by probability (Z ko.q122.mk, .soft); L24-30 only +4.2 (E l.173); toy suite: bridge removed, accuracy 86%, rebuilt (E l.110); swap carries +44.3, in-context reads kept 97-100% (E l.162) | Gap 0.32 [0.20, 0.43]; J++ 0.26 vs PCA 0.21 recall extra loss (not specific, D fig02); fresh one-pick replication recall 0.06 (SBO); routes gate lowered to 0.75 (DR §3 table note) | [AD] (v2 post hoc) / [FA] main, [AD] routes | **partly / conflict**: both weak and both have a failed control; neither should build on it |
| **9B** | Split +42.6; mid-band dependence at the mention; no rebuild (span rank 7 → 636, accuracy 47%; E l.111) | Gap 0.53 main test, but clean design misses (0.23 [0.14, 0.31], bar 0.3; P45 Q45.10) and the fresh-scene replication fails (recall 0.12; SBO "replication, fresh scenes") | [FA] / [FA] | **partly**: his 9B is clean; ours is fragile in locker-first scenes (reading: consistent with §3d) |
| **Directions: 25 vs 100 on the 27B** | Stated facts lost on the 27B: 2.0 at K 10, 6.9 at K 30, 20.0 at K 100 (by probability 6.4 → 15.0 → 37.9; Z dose.q27.k10.K, k30.K, k100.K, *.sK) | 27B lookup extra loss 0.12 / 0.30 / 0.60 at k 25 / 50 / 100; another scene's 100 atoms −0.01 (D fig02b (a), jppother100) | [FA] (amendment 54) / [FA] (45k: "can't tell") | **agree**: both find the 27B's in-context reader starts to depend on J++ directions at ~100 |

## 3. Candidate joint theses (tested against the files)

### a. Double dissociation

Claim: removing J++ costs recall, not the in-context reader; removing the order pointer costs the lookup's position answers, much less the recall; his J-part swap moves recall while in-context reads keep their answer.

- **Verdict: partly supported.** The J++ side holds in both tracks; the pointer side holds on three of four models, not on the 27B.
- Deciding numbers:
  - J++ side: recall vs lookup extra loss 0.50 / 0.74 / 0.32 / 0.75 vs −0.03 / 0.14 / 0.00 / −0.10 (D fig01) [FA]. His toy-suite locker step 99-100% kept vs recall 55-63% (E l.73) [FA].
  - Pointer side (sanity swap): lookup extra loss without the pointer 0.31 / 0.15 / 0.26 / 0.28 vs recall 0.12 / 0.15 / 0.14 / 0.03 (D s10, 9B / 27B / 122B / Muse) [AD; replicated in advance on the 9B and Muse per DR §4]. Position share without the pointer 0.08 / 0.06 / 0.05 / 0.27 vs without a random part 0.54 / 0.25 / 0.36 / 0.55 (D fig05 no_alf, no_alf_rand).
  - Swap side: transfer +63.0 / +63.9 with in-context reads kept 95.8-100% (Z swap.q27.swap, swap.q9.swap; E l.165-166) [FA].
- Strongest counter-evidence:
  - The 27B: the pointer costs recall as much as the lookup (0.15 vs 0.15, D s10), and the 27B lookup misses the strict J++ rule (0.14, bar 0.10; DR §1).
  - Our lookup's J++-independence is measurable only where the locker comes first: the change switches 9-19% of lookups when the locker comes after (X0D split table). So the "lookup does not need J++" half rests on locker-first scenes.
  - His "kept" readers are stated-attribute finals, not our binding lookup; only his toy-suite step 2 is the same task.
- Credence: **medium** (J++ half high, pointer half medium-low).
- Best figure: figures/story/fig05_routes.png (pointer removal, both readers); pair with docs/breadth/figures/fig05_carries.png.

### b. The model holds the entity twice

Claim: a lens-readable code the recall reads, and a code outside the lens (plus an order pointer) the lookup reads.

- **Verdict: partly supported.** The lens-readable entity code is well supported on his side. The "second code outside the lens" is not shown to be specific.
- Deciding numbers:
  - His entity code is context-free: a J-part from one neutral sentence transfers 1.094 / 1.099 times the same-passage swap (Z ptr.q27.neutral, ptr.q9.neutral) [FA].
  - Ours: J++ alone gives 0.00 identity answers on all four models (D fig05 keep_jpp) [AD]. So whatever the lookup reads for identity is mostly outside our J++ part.
  - Removing J++ + pointer + identity outside J++ leaves 0.07 / 0.18 / 0.22 / 0.52 of lookups switching vs 0.38 / 0.67 / 0.41 / 0.82 for a random part (D fig10) [FA arms, bar out of reach: P45 Q40.1].
  - 45e: identity outside J++ cuts identity answers only 0.06 / 0.12 / 0.04 more than a wrong-pair direction (bar 0.15; P45 Q45.7) [FA, failed]; size-checked 0.08 / 0.14 / 0.05 (D fig10) [AD].
- Strongest counter-evidence:
  - On the 27B, removing the J++ part (25 atoms) cuts identity answers from 0.66 to 0.45 vs 0.70 with a random part (D fig02b no_jpp, no_jpp_rand). Its identity answers fall 0.31 more from k 25 to 100 (D fig02b, 45k) [FA rule, "can't tell"]. So on the 27B part of the identity route is lens-readable.
  - About half the route is unexplained on Muse (0.52 left; D fig10). The "outside" code is a rank-1 class-mean direction, not a fitted subspace.
  - His Lightning paste moves less than the J-part swap "because it also overwrites position and binding" (ZR §4). That is consistent with a second code, but it is his reading, not a test.
- Credence: **low-medium.**
- Best figure: figures/story/fig10_what_is_left.png.

### c. "Carried, not needed"

Claim: our change-removal and his knock-out disagree on Muse and the 122B, the two models where he found the bridge rebuilt after removal.

- **Verdict: partly supported.** The disagreement is real on Muse on his toy suite, weaker on v2, and the 122B is too weak on both sides to read.
- Reading (not tested): our change-removal asks which part of a transplanted Δ carries the switch. That makes it a *carried* test, like his swap, not a *needed* test like his knock-out. Seen this way, the two tracks agree on "carried" and differ only on "needed".
- Deciding numbers:
  - Muse, ours: recall J++ extra loss 0.66 vs logit lens 0.01 (D fig02) [FA].
  - Muse, his toy suite: knock-out gap 7 (E l.87). The bridge is removed in 90-100% of items yet accuracy stays 91%, and the bridge is back at rank 0 two layers on (E l.99) [pre-registered reading "redundant routes"].
  - Muse, his swap: carries at L14-20 (+50.3; E l.161) [AD, exploratory band].
  - 122B: toy-suite accuracy under the knock-out 86% (E l.110) [AD]. On v2, +48.5 greedy but +1.7 by probability (Z ko.q122.mk, ko.q122.soft) [AD, post hoc thresholds]. Swap carries +44.3 (E l.162) [FA]. Ours: J++ 0.26 vs PCA 0.21 (D fig02) [FA].
- Strongest counter-evidence:
  - On v2 his knock-out *does* cost Muse +59.9 and the 122B +48.5 greedy (Z ko.mu.mk, ko.q122.mk). The "rebuilt" result is from the toy suite (E l.99, l.110), and M→M loss there was only 6 (Muse) and 9 (122B) points (E l.116).
  - The sites differ: Muse L26 vs L36-42; 122B L33 vs L39-45 / L24-30.
  - Our 122B result is not J-specific against PCA, so "carried in J++" is itself weak there.
- Credence: **medium** for "our test is a carried test and the tracks agree on carried". **Low** for "Muse/122B do not need J++".
- Best figure: none shows both. The nearest is docs/breadth/figures/fig08_readable.png (readable ≠ needed) next to figures/story/fig02_specificity.png.

### d. Earlier mentions

Claim: our 45p (the recall reads the earlier mention's J++) vs his passing-mention results.

- **Verdict: partly supported.** On the three models both tracks touched (9B, 27B, Muse), both find that an earlier mention gives the recall a second, lens-readable source. Lightning and the 122B break it on his side.
- Deciding numbers:
  - Ours (45p): removing J++ at the earlier mention loses 0.25 / 0.41 / 0.42 beyond random and 0.26 / 0.49 / 0.49 beyond another item's token. The lookup moves at most 0.01 (P45 Q45.13) [FA, 3 of 3].
  - Ours, consistent with 45p: with the locker first, the recall needs J++ at the bridge less on every model, 0.35 / 0.67 / 0.20 / 0.68 vs 0.65 / 0.81 / 0.41 / 0.80 with the locker after (SBO, two people swap) [AD].
  - His RM − MM: 27B +17.6 [10, 26], 9B +11.6 [5, 19], Muse +10.1 [2, 18], Lightning +4.0 [−3, 11], 122B +1.7 [−5, 8] (Z r.q27, r.q9, r.mu, r.nl, r.q122) [FA amendment 35; it predicted ≤ 10 everywhere and failed on the 27B and 9B]. His controls are J-specific (rotated / logit lens within [−2, +3], E l.170). Never named, the 9B's dependence sits wholly in the question (E l.179).
- Where they agree: the 9B, 27B and Muse in direction; both findings are J++-specific.
- Where Lightning breaks it: deleting the mention costs Lightning nothing extra (+4.0 [−3, 11]), as for the 122B (+1.7) and the 9B base (−1, E l.170). We have no Lightning runs and no 45p on the 122B. Our 122B still shows the order effect (0.20 vs 0.41, SBO), so the two contrasts (delete the mention / remove J++ at it) need not agree.
- Strongest counter-evidence: the designs differ (deleting a sentence changes competence by 5-20 points, E l.170, vs an in-place edit). His effect is +4 to +18 points, ours a fraction of switches; no common unit.
- Credence: **medium.**
- Best figure: figures/story/fig03c_earlier_mention.png.

### e. Information moves later with depth

Claim: our 45q (the link moves into the locker sentences by L) vs his late bands (the dependence moves from the mention to the question).

- **Verdict: partly supported.** The shape is the same, but the readers and destinations differ. One cross-check lines up on the 9B at L12.
- Deciding numbers:
  - Ours, 9B (D fig03b, 45q sweep) [AD]: the bridge-word change switches 0.93 / 0.36 / 0.17 / 0.02 of lookups at L4 / 8 / 12 / 16, while the locker-sentence copy switches 0.03 / 0.48 / 0.70 / 0.59. The 45q rule holds 3 of 3 [FA].
  - His, 9B: mid band, mention +33.6 and question +6.2 of +42.6 (Z pos.q9.all.*). Late band L26-29, question +52.6 and mention +0.2 (Z late.q9.*) [FA, amendment 57].
  - His, 27B L52-60: question +47.1, mention +2.9 (Z pos.q27late.*) [FA].
- Cross-check (reading): at the 9B's L12 the *recall* still needs the bridge token in both tracks. Ours: locker-after recall extra loss 0.79 in the clean design (X0D 45m table). His: mention +33.6 at L12-16. The *lookup's* link has already left the bridge token by then (ours). So the lookup binds earlier than the recall moves its dependence.
- Strongest counter-evidence:
  - Different readers (our lookup, his recall) and different destinations (locker sentences after the bridge vs the question).
  - Muse makes the link from about L/2, not by L (P45 Q45.12).
  - "Moves rightward with depth" is the default for a causal transformer, so the shared claim is weak unless the layer at which each reader stops needing the bridge token is compared on the same items.
  - Our first test of this (45b) was a design error; its claim is withdrawn (P45 Q45.5 sanity check).
- Credence: **medium** for the shape, **low** as a joint mechanistic claim.
- Best figure: figures/story/fig03b_layers.png, with docs/breadth/figures/fig04_where.png.

### f. Methods lessons

- **Verdict: supported as lessons; not as findings.**
- Removal size vs number of directions:
  - Bolt's top 10 remove 5.6% of the residual vs 12.7-19.6% elsewhere (Z size.nb vs size.q9, size.mi).
  - Bolt at 100 directions: J++ +31 vs same-size PCA +24. DeepSeek: +29 vs +26 (ZR §5) [FA, amendments 54, 56].
  - Ours: the 27B lookup's extra loss rises 0.12 → 0.30 → 0.60 at k 25 → 50 → 100, while another scene's 100 atoms cost −0.01 (D fig02b) [FA, 45k: cause "can't tell"]. His 27B stated facts rise 2.0 → 20.0 points from K 10 to K 100 (Z dose.q27.k10.K, dose.q27.k100.K).
  - Both tracks therefore see the 27B's in-context reader start to depend on J++ at ~100 directions. Neither knows why.
- Readable vs carried vs needed:
  - His: OLMo carries (swap +41) but does not need (+5) (ZR §4). A probe reads the fact but its subspace carries +8.3 vs J++ +74.8 (Z probe.q27.probe, probe.q27.swap).
  - Ours: a probe reads the order pointer in 0.92-0.99 of scenes (layout alone 0.53; DR §4; 9B v4 0.97, D numbers v4_b_before_9b). The lens does not read it, yet removing it stops position answers (D fig05).
  - Readable-by-lens, readable-by-probe, carried and needed come apart in both tracks.
- Bar-reachability: two of our fixed-in-advance questions were out of reach at their share (P45 Q40.1, Q45.1). His dose plateau rule judged specificity by greedy answers (ZR §8).
- Strongest counter-evidence: none against the lessons. The risk is presenting a lesson as a finding.
- Credence: **high** (as lessons).
- Best figure: docs/breadth/figures/fig09_dose.png, with figures/story/fig02b_k_curve.png.

### Internal tensions

- **His, 24 Oct vs 26 Oct.**
  - 24 Oct (E l.153, l.157, amendment 32): the J-part "carr[ies] the recalled attribute, not the identity (lookups stay)".
  - 26 Oct (E l.214, l.224, amendment 51; ZR §4 title): it "carries which entity it is" (neutral donor 1.09-1.10).
  - ZR §1 still says that under the knock-out the models "still know which entity it is, but not its fact". The only support given is that they rarely name the bridge (1% / 5% / 1%), which does not show they know the entity. If the J-part carries identity, knocking it out should remove identity.
  - Our routes test suggests a resolution: in-context reads are kept because they read identity and order *outside* J++, not because J++ lacks identity.
- **Ours.**
  - DR "In one minute" says recall uses the J++ part "on all four models by rules fixed in advance", but the 27B fails the strict rule (lookup 0.14 > 0.10; DR §1), the 9B fails the clean design (0.23) and its replication (recall 0.12; DR §6).
  - DR §1 says the logit-difference score is not fixed in advance, but Q39.1 was committed before computing and D fig11 marks it "fixed".
  - 45b's score stays "right" although its claim is withdrawn (P45 Q45.5).
- **Across tracks.** Our Muse reading (needs J++, gap 0.85) and his (shares 35 of 60 with the logit lens; toy gap 7) cannot both be the model-level summary.

## 4. Unique findings and what not to claim

**Ours (depth), each standing alone:**

1. The lookup never answers with the moved value; it splits between identity and position. Identity / position: 9B 0.48 / 0.51, 27B 0.66 / 0.34, 122B 0.61 / 0.38, Muse 0.44 / 0.54; value 0.00 on all four (D fig05 whole) [FA routes; 122B gate 0.75, AD].
2. An order pointer outside the lens. A probe reads it at 0.92-0.99 (DR §4). Removing it cuts position answers to 0.08 / 0.06 / 0.05 / 0.27 vs 0.54 / 0.25 / 0.36 / 0.55 for a random part (D fig05) [AD; replicated in advance on the 9B and Muse]. A fixed write at 4× moves the lookup to the target in 0.73 / 0.50 / 0.66 / 0.52 of writes, a random direction 0.00-0.01 (P45 Q44.1, descriptive). At a real change's size it barely moves (target − random 0.02 / 0.00 / 0.01 / 0.05; P45 Q44.1) [FA, failed: dose below a real change, a design error].
3. On clean locker-after scenes the binding is made in the locker sentences: copy 0.70 / 0.74 / 0.76 vs bridge 0.17 / 0.01 / 0.01 (P45 Q45.12) [FA].
4. When its locker comes first, the recall reads the item's earlier mention through J++ (P45 Q45.13) [FA].
5. The pointer marks the first locker in a clean layout. A sentence naming an item first moves the Qwens' lookup to identity: 0.85-0.97 of answers vs 0.54 / 0.65 (X0D 45a table) [rule FA, result "mixed"].

**His (breadth), each standing alone:**

1. The split on three models from two families with the full control set, three renderings and row-identical clean reruns on the 27B and 9B (ZR §1-2; Z ko.*) [FA].
2. A context-free entity code: a neutral one-sentence donor works as well (1.09 / 1.10 / 1.01). It is not the answer token: swap_noans +63.1 vs swap +63.0 (E l.177) [FA].
3. Decodable is not carried: probe subspace +8 / +6 / +2 vs J++ +75 / +80 / +62 (ZR §4) [FA].
4. Beyond two hops, the last hop decides. Lightning P → P → M +60 vs M → M → P −2 (v2, ZR §6 table). A number computed from the passage needs no J++ to be reported (27B / 9B / Lightning 0 / 0 / 0, ZR §6) [FA].
5. Graded across nine models, with size-matched dose controls (Bolt, DeepSeek) and late-band question dependence in two families (ZR §3, §5) [FA].

**Neither of us should claim:**

- That J++ is "the" workspace, or that it is necessary for all recall (CS "What we are not claiming").
- Anything model-level about the 122B. His probability score fails (+1.7). Our PCA control nearly matches J++ and the replication recall is 0.06 (SBO).
- That Muse "needs" J++. The two tracks conflict, and the sites differ.
- That identity outside J++ is a specific code (45e failed, 0 of 3).
- That the order pointer exists in natural text. The simple-scene pointer barely transfers (0.05-0.15 in varied scenes, P45 Q42.1). A refit pointer is found on the 9B and Muse only (X0D 45d).
- That the in-context reader is J++-free at large k on the 27B.
- That our change-removal and his knock-out measure the same thing.
- Any result as established: all are UNVERIFIED. Our predictions score a mean Brier 0.32, worse than always answering 50% (DR §7).

## 5. Questions for Neel

Each question is tied to a decision due Friday. The GPU freeze is tonight, Tue 21:00 [US: from the team's plan, not a results file].

1. **One well-checked mechanism on fewer models, or the broad map of where it holds?** Decision: the spine of the joint write-up. Either (i) his §1 + §4 with our routes/pointer as "what the in-context reader uses instead" on the 9B/27B, where our layer is inside his band, or (ii) a nine-model map with the mechanism as an appendix. Our evidence is strongest on the 9B, 27B and Muse; his on the 27B, 9B and Lightning. The only shared clean pair is the two Qwens.
2. **Is "carried vs needed" a finding or a methods footnote? Is 45r the right last experiment before the freeze?** Decision: whether §3c goes in the abstract, and whether 45r runs. [US: 45r has no spec in jobs/, predictions/ or docs/ at cc56ffb0; Dan must state it in one line before asking.] The test that would turn §3c from a reading into a result is our change-removal and his knock-out on the same items at the same site. Candidates: Muse at L26 with an all-token knock-out, or his 27B items at L32 with our transplant.
3. **Is the toy locker setting acceptable for the mechanism if the split itself replicates on natural text?** Decision: whether mechanism claims are scoped "in templated scenes". The split holds in every setting, weaker outside simple scenes (DR §1). The pointer must be refit per format: 0.18-0.24 on the 9B, at most 0.13 on the 27B (X0D 45d) [FA]. His split holds on natural passages (ZR §2).
4. **Which control would most change his view of the lens-invisible order pointer?** Decision: which single control we cite (or run after the freeze on CPU) to defend Fig. 7. Options:
   - a pointer found with no labels: P_cf shares about 2 of 4 directions with the mass-mean pointer (P45 Q43.1);
   - a wrong-pair / size-matched direction, already failed for identity (P45 Q45.7);
   - a write at a real change's size (failed: P45 Q44.1);
   - the pointer's removal measured on his toy-suite locker items.
5. **(optional) Which word wins for "pointer"?** Decision: the shared glossary before the merge of the two READMEs (§1 proposes "entity code" vs "order pointer").

## Critic's list

(pending)
