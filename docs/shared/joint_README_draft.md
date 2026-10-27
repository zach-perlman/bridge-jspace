Draft skeleton, 27 Oct; UNVERIFIED (nothing hand-checked). Experiments freeze Wed 28 Oct evening; hand check Thu 29 Oct (STATUS.md, d0ee653b)

# Recall reads the lens; the lookup goes around it

*In a two-hop question, does the model use the part of the bridge entity that the J++ lens can read, and does that depend on whether the answer must come from memory or is in the prompt?*

Zach's breadth track ([docs/breadth/README.md](../breadth/README.md)) and Dan's depth track ([docs/depth/README.md](../depth/README.md)). Terms: [joint_story_draft.md §1](joint_story_draft.md).

**Source keys.**
- Z = docs/breadth/data.csv (key)
- D = figures/story/data.csv (figure / key)
- E l.N = EXPERIMENTS.md line N
- P45 / P46 = predictions/2026-10-26_dan.md / predictions/2026-10-27_dan.md (on danorel, df10f56f)
- JS = results/jswap/<run>/summary.json
- G = docs/shared/grid.csv

## In one minute

- **Answers that must come from memory need the lens-readable part of the bridge; answers in the prompt do not.** This holds with both methods on the Qwen 9B and 27B, and with the knock-out on Lightning. Limits: the 27B misses our strict bar, and our positive control failed.
- **Moving that part moves the recall, not the lookup.** A swapped J-part carries the recall to the other entity, while lookups keep their answer (≥ 95%). Our lookup never answers with the moved value.
- **The lookup uses what the lens cannot see:** identity outside J++ and an order pointer. This is ours only, in simple scenes; about half of the route is unexplained.
- **The methods disagree on Muse and the 122B.** On Muse, the knock-out's dependence is half shared with the logit lens, while our change-removal is J++-specific. 45r (Q46.1) tests this at mid depth; it is not run.

## Setup

![One prompt, two questions about the same bridge](../../figures/story/fig00_setup.png)

A two-hop question asks about a bridge entity: "the composer who wrote The Magic Flute" (Mozart), or "Iris's pick" (a frog).

- **Two readers.** Memory (our **recall**, his **M final**) or the prompt (our **lookup**, a locker number bound to the item; his **K final**, a stated fact).
- **The lens.** J++.
- **Three tools.**
  - **Knock-out** (his): remove the top-10 J++ directions at every token of a band. Does the model *need* them?
  - **Change-removal** (ours): add the bridge token's hidden-state change at one layer, without its J++ part (25 directions). Does the change *travel through* it?
  - **J-part swap** (his): replace the mention's top-10 J++ span with another entity's. Is it *sufficient*?
- **Sites.** Ours: one layer (9B L12, 27B L32, 122B L33, Muse L26). His: bands (9B L12-16, 27B L32-40, Lightning L27-33, Muse L36-42, 122B L39-45). They overlap only on the 9B and 27B.

## Claim 1. Answers that must come from memory need the lens-readable part; answers in the prompt do not

**Evidence.**

| | 9B | 27B | Lightning | 122B | Muse |
|---|---|---|---|---|---|
| Change-removal gap (recall − lookup extra loss; D fig01 contrast_*) | 0.53 [0.42, 0.61] | 0.60 [0.50, 0.69] | GAP -> 45s (Q46.2) | 0.32 [0.20, 0.43] | 0.85 [0.68, 0.98] |
| Knock-out M − K, points (Z ko.*.mk) | +42.6 [37, 49] | +50.9 [46, 55] | +53.1 [48, 59] | +48.5 [44, 54] | +59.9 [55, 65] |

- **The question held fixed, only the source varied (his).**
  - M vs K is the same question with the fact stated or not.
  - Reporting a number, recalled minus read from the passage: +14.8 / +13.3 / +4.8. Computed by arithmetic: 0.0 / 0.0 / 0.0. (9B / 27B / Lightning; Z mod.*.numbers.paper10.MR-PR, AR-PR.)
  - Three hops ending in a recall vs a read:
    - Lightning P→P→M +59.9 vs M→M→P −1.9;
    - the 27B the other way, P→P→M +8.2 vs M→M→P +20.5.
    - (Z mod.*.threehop.paper10.PPM-PPP, MMP-PPP.)
- **Controls.** Ours: J++ vs same-size PCA recall loss 0.37 / 0.61 vs 0.13 / 0.16 (9B / 27B; D fig02); logit-difference gap 0.48 / 0.47 (D fig01b). His: rotated +1.8 / +2.7 / +3.6, logit lens +1.4 / +1.9 / +8.7, by probability +35.3 / +50.3 / +44.1 (9B / 27B / Lightning; Z ko.*.rot, .u, .soft).
- **What this is about.** In our design reader and answer source are confounded (DR §6); his tests hold the question fixed and vary the source.
- **Limits.** The 27B's lookup loses 0.14 (bar 0.10): X0's strict rule "not confirmed" (DR §1). Our positive control failed (27B 0.15, bar 0.20; DR §6). The clean design holds on 2 of 3, the 9B at 0.23 (P45 Q45.10). Lightning misses two number predictions (Z mod.nl.numbers.*).

![Removing 10 J++ directions breaks recalled facts, not stated ones](../breadth/figures/fig01_needed.png)

**Status.** Both main tests fixed in advance; the number and three-hop tests fixed in advance (ZR §6). **Credence:** medium-high on the 9B, 27B and Lightning.

## Claim 2. Moving that part moves the recall, not the lookup

**Evidence.**
- **His J-part swap** (fixed in advance): recall transfer +63.9 / +63.0 / +44.8 (9B / 27B / Lightning; Z swap.*.swap); lookups kept: PK 95.8% / 99.1% / ≥ 98% (E l.165, l.166, l.209). A neutral one-sentence donor works as well (1.10 / 1.09 / 1.01; Z ptr.*.neutral).
- **Our routes test** (fixed in advance): with another item's locker moved, the lookup answers by identity or position, never the value. Identity / position / value: 9B 0.48 / 0.51 / 0.00, 27B 0.66 / 0.34 / 0.00, Muse 0.44 / 0.54 / 0.00 (D fig05 whole). Adding only the J++ part gives 0.00 identity answers (D fig05 keep_jpp).
- **The rest of the residual** (after the data; his stored summaries, not in his report): all but the J-part moves the 27B's stated read +24.6 [18.6, 31.0] (PK) and the 9B's +13.9 (JS jswap_v2_v1, qwen35_9b_jswap_v2_v1). GAP -> Zach's confirmation.

**Limits.** Adding only the J++ part barely moves the recall either (0.07 / 0.02 / 0.02 vs random 0.02 / 0.00 / 0.00; D numbers rtk_C2_keep_jpp_recall_follows_s_*): too small a dose to separate readers. His lookup is a stated attribute; ours a bound number.

![A swapped J-part moves the answer to the other entity](../breadth/figures/fig05_carries.png)

**Credence:** medium-high (9B, 27B, Lightning for the swap; 9B, 27B, Muse for routes).

## Claim 3. The lookup uses what the lens cannot see

**Evidence (ours only).**
- **An order pointer.** A probe reads it in 0.92-0.99 of scenes (layout alone 0.53; DR §4). Removing its 4 directions cuts position answers to 0.08 / 0.06 / 0.27 vs 0.54 / 0.25 / 0.55 for a random part (9B / 27B / Muse; D fig05 no_alf) [after the data; replicated in advance on the 9B and Muse]. A write at s = 2 sends the lookup to the target in 0.46 / 0.24 / 0.52 of writes (X0D) [after the data].
- **Identity outside J++.** Removing J++, the pointer and identity together leaves 0.07 / 0.18 / 0.52 of lookups switching, against 0.16 / 0.38 / 0.59 with a wrong-pair direction (DR §5).

**How narrow.** Identity's specificity failed when fixed in advance (0.06 / 0.12 / 0.04, bar 0.15; P45 Q45.7). The pointer must be refit per format (P45 Q42.1). The recall also loses 0.44 / 0.39 without the identity direction (27B / Muse; DR §5). On the 27B the pointer costs both readers alike (0.15 / 0.15; D s10). Lightning: GAP -> 45s.

![The lookup follows identity or position, never the value](../../figures/story/fig05_routes.png)

**Credence:** medium (order pointer, simple scenes); low (identity outside the lens).

## Where the methods disagree

- **Muse.** Our change-removal at L26 is J++-specific: recall loss 0.66 vs 0.01 with the logit lens (D fig02) [fixed in advance]. His knock-out at L36-42 gives +59.9, of which the logit lens gives +34.6 (Z ko.mu.mk, ko.mu.u; E l.169) [after the data]; his toy suite barely moved Muse (gap 7; E l.87). Never run at the same depth: GAP -> 45r (Q46.1: his knock-out at L23-29 with all controls vs our L26 gap; not queued).
- **The 122B.** Ours is not specific against same-size PCA (0.26 vs 0.21; D fig02); his fails by probability (+1.7 vs +48.5 greedy; Z ko.q122.soft). Neither track claims it.

![The joint grid](../../figures/shared/grid.png)

## Methods lessons

- **Removal size, not the number of directions.**
  - Bolt's top 10 remove 5.6% of the residual vs 12.7-19.6% elsewhere (Z size.*). At 100 directions a same-size PCA removal nearly matches J++: Bolt +24 vs +31, DeepSeek +26 vs +29 (ZR §5).
  - The 27B costs at 100 directions are not a shared finding: his is generic damage (ZR §5), ours specific to the scene's own atoms (D fig02b).
- **Readable, carried, needed come apart.** OLMo carries (swap +41) but does not need (+5) (ZR §4). A probe reads the fact, but its subspace carries +8.3 vs J++ +74.8 (Z probe.q27.*). A probe reads our order pointer; the lens does not (DR §4).

## What did not hold

- **Ours** (fixed in advance; DR §6): the 27B strict rule; the 9B clean design and replication; the positive control; identity outside J++; a second-vs-third pointer; writes at s = 1; 45b (withdrawn).
- **His** (ZR §8): the 9B's second toy seed; steering (withdrawn); the plain J-lens; the never-named bridge; the 122B by probability; Muse's logit-lens share; Bolt; OLMo; the 27B's P→P→M; Lightning's numbers; H0 head-on.

## How we checked

- **Nothing is hand-checked yet.** The cross hand check is Thu 29 Oct (GAP -> item lists in docs/shared/gaps.md).
- **Ours:** an independent reimplementation reproduces the 9B main test on 20 of 20 items; the hand-check pack recounts 45m / 45q / 45p (STATUS.md); predictions score a mean Brier of 0.32 (DR §7).
- **His:** clean-checkout reruns are row-identical on the 27B and 9B (ZR §2); verify_kit recomputes M − K.

## Open questions

- **Early mentions.** Both see an earlier mention lower the bridge's role (ours 45p 0.25 / 0.41 / 0.42, P45 Q45.13; his +11.6 / +17.6 / +10.1, Z r.*), but the mechanisms differ (ours through J++ at the mention; his survives the knock-out there, E l.170), and Lightning (+4.0) and the 122B (+1.7) do not show it.
- Carried but not needed on Muse at mid depth? GAP -> 45r (Q46.1).
- Does our split hold on Lightning? GAP -> 45s (Q46.2-Q46.3; blocked on Zach's lens file).
- What is the other half of the lookup's route? Does the order pointer exist in natural text? (refit found on the 9B and Muse only; X0D 45d).
