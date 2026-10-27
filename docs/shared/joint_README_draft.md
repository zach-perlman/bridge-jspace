Draft skeleton, 27 Oct; UNVERIFIED (nothing hand-checked). Experiments freeze Wed 28 Oct evening; hand check Thu 29 Oct (STATUS.md, d0ee653b)

# Recall reads the lens; the lookup goes around it

*In a two-hop question, does the model use the part of the bridge entity that the J++ lens can read, and does that depend on whether the answer must come from memory or is in the prompt?*

Zach's [breadth](../breadth/README.md) and Dan's [depth](../depth/README.md) tracks; terms as in [joint_story_draft.md §1](joint_story_draft.md).

**Sources.** Z docs/breadth/data.csv; D figures/story/data.csv; E l.N EXPERIMENTS.md; P45 / P46 predictions/2026-10-26_dan.md / 2026-10-27_dan.md (danorel df10f56f); JS results/jswap/<run>/summary.json.

## In one minute

- **Answers that must come from memory need the lens-readable part of the bridge; answers in the prompt do not.**
  - Both methods find this on the Qwen 9B and 27B; the knock-out alone finds it on Lightning.
  - Limits: the 27B misses our strict lookup bar; the 9B misses our clean design (0.23) and replication (0.12); our positive control failed.
- **Swapping that part moves the recall, not the in-context read.** Zach's J-part swap, fixed in advance on the 9B and 27B.
- **Our lookup uses an order pointer the lens cannot see**, on the 9B and Muse in simple scenes. Identity outside J++ is not shown to be specific, and about half of the route is unexplained.
- **The methods disagree on Muse and the 122B.**
  - On Muse, more than half of the knock-out's effect is shared with the logit lens, while our change-removal is J++-specific.
  - 45r (Q46.1) would test this at mid depth; it is not run.

## Setup

![One prompt, two questions about the same bridge](../../figures/story/fig00_setup.png)

A two-hop question about a bridge entity ("the composer who wrote The Magic Flute"; "Iris's pick").

- **Two readers.** From memory: our **recall**, his **M final**. In the prompt (**in-context read**): our **lookup** (a bound locker number), his **K final** (a stated fact).
- **Three tools.**
  - **Knock-out** (his): top-10 J++ directions removed at every token of a band. *Needed?*
  - **Change-removal** (ours): the bridge token's change added at one layer, minus its 25-direction J++ part. *Does the change travel through J++?*
  - **J-part swap** (his): the mention's top-10 J++ span replaced by another entity's. *Sufficient?*
- **Sites.** Ours: one token, one layer (9B L12, 27B L32, 122B L33, Muse L26; Lightning L30 for 45s, 3a4637ad). His: every token, a band (L12-16, L32-40, Lightning L27-33, Muse L36-42, 122B L39-45). Layers overlap on the 9B and 27B; L30 is inside Lightning's band.
- **Words.** **Entity code** = his J-part (inside J++; which entity). **Order pointer** = ours (4 directions outside J++; which locker sentence).

## Claim 1. Answers that must come from memory need the lens-readable part; answers in the prompt do not

| | 9B | 27B | Lightning | 122B | Muse |
|---|---|---|---|---|---|
| Change-removal gap, recall − lookup (D fig01 contrast_*) | 0.53 [0.42, 0.61] | 0.60 [0.50, 0.69] | GAP -> 45s (Q46.2) | 0.32 [0.20, 0.43] | 0.85 [0.68, 0.98] |
| Knock-out M − K, points (Z ko.*.mk) | +42.6 [37, 49] | +50.9 [46, 55] | +53.1 [48, 59] | +48.5 [44, 54]° | +59.9 [55, 65]° |

° After the data (v2 not pre-registered for these models; E l.167, l.169).

**Source varied, question fixed (his).**
- M vs K is one question with the fact stated or not.
- Reporting a number, recalled minus read: +14.8 / +13.3 / +4.8; computed: 0.0 / 0.0 / 0.0 (9B / 27B / Lightning; Z mod.*.numbers.paper10.MR-PR, AR-PR).
- Three hops ending in a recall vs a read: Lightning P→P→M +59.9 vs M→M→P −1.9; the 27B reversed, +8.2 vs +20.5 (Z mod.*.threehop.paper10.PPM-PPP, MMP-PPP).

**Controls.**
- Ours: J++ vs same-size PCA, recall loss 0.37 / 0.61 vs 0.13 / 0.16 (9B / 27B; D fig02); logit-difference gap 0.48 / 0.47 (D fig01b).
- His (9B / 27B / Lightning; Z ko.*.rot, .u, .soft): rotated +1.8 / +2.7 / +3.6; logit lens +1.4 / +1.9 / +8.7; by probability +35.3 / +50.3 / +44.1. Lightning's probability reading was chosen after its grid (ZR §5).

**Limits.** Our reader and answer source are confounded (DR §6); his tests vary only the source. The 27B's lookup loses 0.14 (bar 0.10): X0 "not confirmed" (X0D pre-registered tests). Positive control failed (27B 0.15, bar 0.20; DR §6). Clean design 2 of 3, the 9B at 0.23 (P45 Q45.10); replication 0.12 (DR §6).

![Removing 10 J++ directions breaks recalled facts, not stated ones](../breadth/figures/fig01_needed.png)

**Status.** Fixed in advance: our main test, and his knock-out on the 9B, 27B and Lightning. After the data: the 122B and Muse knock-out.

**Credence.**
- Medium-high on the 9B and 27B.
- Lightning: medium, knock-out only (GAP -> 45s). Caveats: recalled-number prediction failed (+4.8 [0, 11], bar ≥ 10; ZR §6, §8); own lens fit; removal adds +1.67 nats (rotated +0.30; CS; ZR §7); clean rerun differs on 9 of 14075 rows (ZR §7); highest logit-lens control (+8.7); P→P→M partly logit-lens (+32 natural, +26 second seed; ZR §6).

## Claim 2. Swapping that part moves the recall, not the in-context read

**His J-part swap**, fixed in advance on the 9B and 27B:
- Recall transfer +63.9 / +63.0 (Z swap.q9.swap, swap.q27.swap).
- In-context read kept: 27B PK 99.1%; the 9B's PK still moves +4.4 [2.0, 6.8] (E l.165-166).
- A neutral one-sentence donor works as well: 1.10 / 1.09 (Z ptr.*.neutral).
- Lightning: +44.8, reads kept ≥ 98%. After the data and formally uninformative (paste ceiling +13.8 < 20; E l.209; prereg_replication_1022.md l.1175-1176).

**The rest of the residual** (after the data; his stored summaries, unreported). Everything but the J-part moves the stated read: 27B PK +24.6 [18.6, 31.0], TK +27.3 [20.2, 34.9]; 9B PK +13.9 [7.8, 20.4], TK +1.7 [−11.1, 13.6]; Lightning PK −0.4, TK +2.9 (JS jswap_v2_v1, qwen35_9b_jswap_v2_v1, nem35l_jswap_v2_v1). GAP -> Zach's confirmation.

**Context only (ours).** The routes test's whole change never makes the lookup answer the value (0.00 on 9B / 27B / Muse; D fig05), but adding only the J++ part moves neither reader (recall 0.07 / 0.02 / 0.02 vs random 0.02 / 0.00 / 0.00; D rtk_C2_keep_jpp_*), so it is not reader evidence.

![A swapped J-part moves the answer to the other entity](../breadth/figures/fig05_carries.png)

**Credence.** Medium-high on the 9B and 27B; Lightning not counted. Change from Dan's outline: claim 2 rests on Zach's swap alone, fixed in advance only on the 9B and 27B; our routes test is context.

## Claim 3. Our lookup uses an order pointer the lens cannot see (9B, Muse)

**Evidence (ours only).**
- A probe reads the order pointer in 0.92-0.99 of scenes (layout alone 0.53; DR §4).
- Removing its 4 directions cuts position answers to 0.08 / 0.27, vs 0.54 / 0.55 for a random part (9B / Muse; D fig05 no_alf) [after the data; replicated in advance].
- A write at s = 2 sends the lookup to the target in 0.46 / 0.52 of writes (X0D) [after the data].

**Weak or open.**
- **27B:** the order pointer alone gives position 0.09 (D fig05 keep_alf), the refit 0.08 (X0D 45d); it costs both readers alike (0.15 / 0.15; D s10).
- **Formats:** it must be refit per format (P45 Q42.1).
- **Lightning:** GAP -> no test planned (45s has no routes or order-pointer arms).
- **Identity outside J++ (low credence).** Specific on 0 of 3 (P45 Q45.7). Lookups still switching without J++ + order pointer + identity vs a wrong-pair direction instead (9B / 27B / Muse): 0.07 / 0.18 / 0.52 vs 0.15 / 0.39 / 0.57 (n 300); size-matched subset, after the data, 0.06 / 0.18 / 0.54 vs 0.16 / 0.38 / 0.59 (n 241 / 226 / 237; D s10b). On the 27B removing J++ cuts identity answers to 0.45 (random 0.70; D fig02b). The recall loses 0.44 / 0.39 without the identity direction (27B / Muse; DR §5).

![The lookup follows identity or position, never the value](../../figures/story/fig05_routes.png)

**Credence.** Medium (order pointer, 9B and Muse, simple scenes); low (identity outside J++).

## Where the methods disagree

- **Muse.** Ours at L26 is J++-specific (recall loss 0.66 vs logit lens 0.01; D fig02) [fixed in advance]. His at L36-42: the logit lens gives +34.6 of +59.9 (Z ko.mu.u; E l.169) [after the data]; his toy suite barely moved Muse (gap 7; E l.87). Never at the same depth: GAP -> 45r (Q46.1, not queued).
- **The 122B.** Ours is not specific against same-size PCA (0.26 vs 0.21; D fig02); his fails by probability (+1.7; Z ko.q122.soft). Neither claims it.

![The joint grid](../../figures/shared/grid.png)

## Methods lessons

- **Removal size, not the number of directions.** Bolt's top 10 remove 5.6% of the residual vs 12.7-19.6% elsewhere (Z size.*); at 100, same-size PCA nearly matches J++ (Bolt +24 vs +31, DeepSeek +26 vs +29; ZR §5). The 27B's 100-direction costs are not shared: his generic (ZR §5), ours specific to the scene's atoms (D fig02b).
- **Readable, carried, needed come apart.** OLMo carries (swap +41) without needing (+5) (ZR §4); a probe's subspace carries +8.3 vs J++ +74.8 (Z probe.q27.*); a probe reads our order pointer, the lens does not (DR §4).

## What did not hold

- **Ours** (DR §6; P45): 27B strict rule; 9B clean design and replication; positive control; a recall route through the order pointer; identity outside J++; second-vs-third order pointer; copied link outside the lens (27B); a cause for the 27B's loss with more directions; order-pointer transfer (Q42.1); writes at s = 1; 45b (withdrawn).
- **His** (ZR §8): 9B second toy seed; steering (withdrawn); plain J-lens; never-named bridge; 122B by probability; Muse's logit-lens share; Bolt incl. "distributed"; OLMo; 27B P→P→M; 9B three-hop (unreadable); Lightning's numbers and +47 (not replicated); amendment-24 final-hop rule; computation feeding a lookup (27B, Lightning); H0 head-on.

## How we checked

- **Nothing is hand-checked yet.** The cross hand check is Thu 29 Oct (item lists: docs/shared/gaps.md).
- **Ours.**
  - An independent reimplementation reproduces the 9B main test, 20 of 20 items (DR §7).
  - docs/handcheck_pack.md recounts 45m, 45q and 45p (90 cards; recounts match).
  - Predictions score a mean Brier of 0.32, "worse than always answering 50%" (DR §7).
- **His.** Clean-checkout reruns are row-identical on the 27B and 9B (ZR §2); docs/verify_kit.md recomputes M − K.

## Open questions

- **Early mentions.** In both, a mention lowers the recall's dependence on the bridge site (9B / 27B / Muse: ours 45p 0.25 / 0.41 / 0.42, P45 Q45.13; his RM − MM +11.6 / +17.6 / +10.1, Z r.*, a failed "within 10" prediction, E l.170). No common unit; the mechanisms differ; Lightning (+4.0) and the 122B (+1.7) do not show it.
- Muse at mid depth: GAP -> 45r (Q46.1). Lightning: GAP -> 45s (Q46.2-Q46.3; blocked on Zach's lens file).
- The other half of the lookup's route; the order pointer in natural text (refit only on the 9B and Muse; X0D 45d).

## Critic's list (skeleton pass)

1. Lightning swap formally uninformative (paste ceiling +13.8 < 20). — **fixed**: tagged after the data, formally uninformative; Lightning dropped from claim 2's credence.
2. Routes and keep-only J++ are not reader evidence; claim 2 rests on Zach's swap. — **fixed**: moved to "Context only", with a one-line note on the change from Dan's outline.
3. Muse and 122B knock-out cells and Lightning's probability reading are after the data. — **fixed**: table footnote and Status line; probability reading tagged.
4. Lightning's credence rests on the knock-out alone; six caveats. — **fixed**: "Lightning: medium, knock-out only (GAP -> 45s)" with all six caveats.
5. Claim 3 headline overstated. — **fixed**: scoped to the order pointer on the 9B and Muse; identity low credence; 27B weaknesses listed.
6. Hand-check pack citation; Brier wording. — **fixed**: cites docs/handcheck_pack.md; DR §7's wording kept.
7. One-sided complement selection. — **fixed**: 9B CI, 9B TK and Lightning PK / TK added; tag and GAP kept.
8. Bare "pointer". — **fixed**: "order pointer" / "entity code" throughout; Setup has a warning on words.
9. "Lightning: GAP -> 45s" under claim 3. — **fixed**: "GAP -> no test planned".
10. Identity vs wrong pair mixed populations. — **fixed**: n 300 like for like; size-matched subset separately, after the data.
11. Early mentions: no common unit; failed prediction. — **fixed**: shared statement only; triples labelled; failed prediction noted.
12. "Half shared" → "more than half". — **fixed**.
13. "What did not hold" incomplete. — **fixed**: all listed items added.
14. One minute: the 9B clean-design miss and replication. — **fixed**.
15. Sites overlap in layers only; 45s at L30. — **fixed** in Setup.
16. "lookups kept" while the 9B PK moves +4.4. — **fixed**: "in-context read kept", with +4.4 [2.0, 6.8].
17. "not confirmed" cited to DR §1. — **fixed**: cited to X0D's pre-registered tests table.
