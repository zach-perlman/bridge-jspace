# Hypotheses ledger: what we committed to, and what happened

Every hypothesis and claim the project committed to in writing, with its source, what it predicted (verbatim), the test that decided it, the verdict and the numbers. Failed and withdrawn ones stay. Grouped by hypothesis, not by date.

**Verdicts.** **held** · **held in part** · **failed** · **withdrawn** · **not tested in the final design** · **not separable** (every test in the final design predicts the same outcome under both hypotheses) · **favored, not proven** (where two hypotheses come apart, the data follow this one; no test was built to separate them). A verdict cites its source: a data-file key (each number carries its `<!-- src -->` comment), a pre-registration amendment ([breadth prereg](../breadth/prereg_replication_1022.md)), a predictions entry ([predictions/](../../predictions/README.md)), or the results ledger ([EXPERIMENTS.md](../archive/EXPERIMENTS.md)). Without one the status is "not tested in the final design". Brackets are 95% bootstrap intervals over bridges. Breadth numbers are points (M − K: recall accuracy drop minus stated-fact drop under the knock-out); depth numbers are shares.

**Sources of the hypotheses.** Three plan documents, quoted here and not added to the repo: the proposal "Which intermediates live in the J-space?" (19 Oct 2026, with the 16 Oct one-pager), the sprint plan (20 Oct) and the progress report (22 Oct, Zach's half; 27 Oct, Dan's half).

Models in the order every figure uses: Qwen 9B, Qwen 27B, Muse 30B, Lightning, Qwen 122B; then the breadth-only models.

## Context: what the proposal started from

The 16 Oct one-pager (Qwen3.6-27B) reported, before the sprint:
- **B1.** "A recalled bridge acts through the J-space": swapping its J-space part flipped many more answers than swapping the rest.
- **B2–B3.** In the "brew" colour-table lookup, the bridge acted through the rest, not the J-space part; the lens still picked the intermediate out, but its direction wrote it far less often than a fitted direction.

These are not re-tested here as stated; the final design's tests are below. Their numbers are in the one-pager, not in this repo's data files.

## The proposal (19 Oct): H0–H3

Design: a 2 × 2 of use × answer source, each cell with the intermediate stated and recalled. Predicted "inside": H1 the top row, H2 the left column, H3 the top-left only, H0 only where stated.

### H0, deflationary: **failed** for recalled entities; **held in part** for computed numbers

- **Predicted (verbatim):** "inside" only means the intermediate's own word direction, mainly for linear relations.
- **Decided by:** keeping the bridge's own-word directions during the knock-out (the sprint plan's kill test: recall damage that disappears when the subject's own word is kept; kill bar 0.75 restored); the never-named bridge; numbers computed from the passage keying a recall ("H0 head-on", [prereg amendment 57](../breadth/prereg_replication_1022.md)).
- **Numbers.**
  - Share restored by keeping the own word (v2): 9B {{b|keepown.q9}}, 27B {{b|keepown.q27}}, Lightning {{b|keepown.nl}}, Ministral {{b|keepown.mi}}; on the toy suite 9B {{b|keepown.toy.q9}}, 27B {{b|keepown.toy.q27}}. All below the 0.75 kill bar.
  - A bridge never named (its one passing mention deleted) adds to the recall's drop: 9B {{bci|r.q9}}, 27B {{bci|r.q27}}, Lightning {{bci|r.nl}}.
  - H0 head-on, a computed number keying a recall, minus a read one (points; within 10 = H0 holds for numbers): 27B counted {{bci|mod2.q27.numbers.paper10.KM-PM}}, computed {{bci|mod2.q27.numbers.paper10.AM-PM}}; 9B computed {{bci|mod2.q9.numbers.paper10.AM-PM}} and Lightning computed {{bci|mod2.nl.numbers.paper10.AM-PM}}, where the rotated and logit-lens controls also cost computed chains more, so neither pre-registered outcome is met.
- **Read.** For recalled entities the dependence is not the bridge's own word. For numbers computed from the passage, the 27B needs no more than for a read number; the 9B and Lightning give no reading. A bridge entity the model computes (rather than reads or recalls) was not tested on the final dataset (see C3).
- **Links:** [breadth README §2 and §6](../breadth/README.md); prereg amendments 55 (keep-own on v2), 57 (H0 head-on), 58 note 9 (never-named bridges).

### H1, use: **not separable** from H2 on the main tests; where they come apart, the data follow H2

- **Predicted (verbatim):** an intermediate the model recalls a fact about is inside; one used to look something up in the prompt is outside.
- **Decided by:** the depth conflict test: one bridge word, two readers in the same scene (a recall question and a lookup question); the change between two prompts patched at one layer, with or without its lens part. Switches lost beyond a random part of the same size. This test does not separate H1 from H2: the recall reader answers from memory and the lookup reader from the scene, so the bridge's use and the answer's source coincide here too, as they do on the breadth track's two-step finals.
- **Numbers.** Recall: 9B {{x|rc_excess_9b}}, 27B {{x|rc_excess_27b}}, Muse {{x|rc_excess_muse}}, Lightning {{s|nemotron-3.5-lightning|conflict: recall, switches lost beyond a random part}} (post hoc), 122B {{x|rc_excess_122b}}. Lookup: 9B {{x|lk_excess_9b}}, 27B {{x|lk_excess_27b}}, Muse {{x|lk_excess_muse}}, Lightning {{s|nemotron-3.5-lightning|conflict: lookup, switches lost beyond a random part}} (post hoc), 122B {{x|lk_excess_122b}}.
- **Read.** The recall needs the lens part and the lookup does not, on every model (the 27B's lookup also loses a little; "in part" in the depth README's claim 1). Both H1 and H2 predict this. Where the two come apart, the data follow H2 (see H2).
- **Links:** [depth README, claim 1](../depth/README.md).

### H2, answer source: **favored, not proven**

- **Predicted (verbatim):** a recalled answer keeps it inside; an answer read from the prompt puts it outside.
- **Decided by:** no test in the final design was built to separate H2 from H1; on the main tests (the breadth two-step finals, the depth conflict test) they predict the same cells. Two results come apart from H1, and both follow H2:
  - **The lure finals (breadth, 27B).** The bridge is still used to recall, so H1 predicts the full drop; the answer word sits once in the prompt, on another entity, so H2 predicts a smaller one. Accuracy drop under the knock-out, points: the answer word on another entity (A) {{b|ko.q27.lostA}}, nothing stated (N) {{b|ko.q27.lostN}}; for reference, fact stated (K) {{b|ko.q27.lostK}}, a new made-up fact stated (P) {{b|ko.q27.lostP}}, recall (M) {{b|ko.q27.lostM}}.
  - **The true-fact passages (depth, card z1).** The bridge is used to look up a fact the passage states and the model also knows; H1 predicts a lookup outside the lens part. The 9B's and the 27B's lookups follow the lens part instead: switches lost beyond a random part {{s|qwen3.5-9b|Z1: lookup, switches lost beyond a random part}} and {{s|qwen3.6-27b|Z1: lookup, switches lost beyond a random part}}.
- **Read.** The drop tracks where the answer is, not how the bridge is used. Two cases on one or two models, neither designed as a test of H2 against H1: favored, not proven.
- **Links:** [breadth README §1](../breadth/README.md); [depth ledger, card z1](../depth/EXPERIMENTS.md#z1).

### H3, any retrieval from context: **failed**

- **Predicted (verbatim):** outside whenever a lookup in the prompt appears anywhere in its chain ("fits our country results best so far").
- **Decided by:** three-hop chains (each hop read in the passage P or recalled M), accuracy drop beyond the all-passage chain P → P → P ([prereg amendments 56, 57](../breadth/prereg_replication_1022.md)).
- **Numbers.** P → M → M, which starts with a lookup, still drops beyond P → P → P: 27B {{bci|mod.q27.threehop.paper10.PMM-PPP}} (second seed {{bci|mod2.q27.threehop.paper10.PMM-PPP}}), Lightning {{bci|mod.nl.threehop.paper10.PMM-PPP}} (second seed {{bci|mod2.nl.threehop.paper10.PMM-PPP}}).
- **Read.** Failed on both models that can be read: on the 27B and on Lightning, P → M → M starts with a lookup in the prompt, so H3 puts its bridge outside and predicts no drop beyond P → P → P; it still drops beyond it, on both seeds. The one chain that fits H3 is the 27B's P → P → M ({{bci|mod.q27.threehop.paper10.PPM-PPP}}; second seed {{bci|mod2.q27.threehop.paper10.PPM-PPP}}): it ends in a recall, yet its interval includes zero. The 9B's chains cannot be read (its all-passage chain alone drops {{b|mod.q9.threehop.paper10.loss.PPP}}).
- **Links:** [breadth README §6](../breadth/README.md).

## The sprint plan (20 Oct): C1–C3

### C1, memory steps need the J-space, prompt lookups don't: **held**, graded across models

- **Predicted (verbatim):** steps that retrieve from memory need the J-space; steps that retrieve from the prompt don't. Kill test: a digit-answer prompt step losing beyond controls on ≥ 2 settings or models; or recall damage that disappears when the subject's own word is kept. Gates: competence ≥ 80%; a same-size random removal keeps ≥ 90%.
- **Decided by:** the breadth knock-out on jsuite v2 (top 10 J++ directions at one mid-depth band), [prereg amendments 33, 39, 40, 42, 48](../breadth/prereg_replication_1022.md); the kill test by keep-own (H0 above).
- **Numbers (M − K).** 9B {{bci|ko.q9.mk}}, 27B {{bci|ko.q27.mk}}, Muse {{bci|ko.mu.mk}} (of which the logit lens's own 10 directions take {{b|ko.mu.u}}), Lightning {{bci|ko.nl.mk}}, 122B {{bci|ko.q122.mk}} (by probability {{b|ko.q122.soft}}); DeepSeek {{b|ko.ds.mk}}, Ministral {{b|ko.mi.mk}}, Bolt {{b|ko.nb.mk}}, OLMo {{b|ko.ol.mk}}. Controls on the 27B: rotated {{b|ko.q27.rot}}, logit lens {{b|ko.q27.u}}; the same norm along the top principal directions costs {{b|ko.q27.pcr}} of the effect.
- **Read.** Strong and specific on the 9B, the 27B and Lightning; weaker, shared with the logit lens, or absent by probability on the others. The kill test did not fire (keep-own restores below 0.75).
- **Links:** [breadth README §1, §7](../breadth/README.md).

### C2, reading ≠ using (the lens steers recall-used bridges, not lookup-used ones): **withdrawn** (24 Oct)

- **Predicted (verbatim):** the lens reads a lookup-used bridge but can't steer it; it steers the same bridge when it is used for recall. Kill test: the lens flips ≥ 3× random for a lookup-used bridge, in transit layers, on a new model or setting.
- **Decided by:** the 24 Oct re-score of every steering run with a breakage gate on every cell ([EXPERIMENTS.md, 2026-10-24 "CORRECTION … c2rescore"](../archive/EXPERIMENTS.md)): most cells broke more than 10% of answers, and the steering claims beyond the 9B and the 27B suite were withdrawn. The swap of the bridge mention's lens part replaced it as the sufficiency test ([prereg amendment 32](../breadth/prereg_replication_1022.md)).
- **What survives.** "Read ≠ use" in another form: a swapped lens part carries the entity (27B transfer {{bci|swap.q27.swap}}; rotated {{b|swap.q27.swap_rot}}), and OLMo carries the entity (swap {{b|swap.ol.swap}}) without needing it (knock-out {{b|ko.ol.mk}}).
- **Links:** [breadth README §4, §8](../breadth/README.md).

### C2′, a stated or computed bridge is written only when a recall uses it: **held in part**

- **Predicted (verbatim, [prereg](../breadth/prereg_replication_1022.md), 22 Oct):** a bridge stated in the prompt (P) or computed in it (C) is written by its own lens direction only when the last step recalls from memory (X->M), not when it looks the answer up (X->P).
- **Decided by:** scripts/c2_narrow.py on each model's steering run, then the 24 Oct re-score ([EXPERIMENTS.md](../archive/EXPERIMENTS.md)).
- **Read.** Before the re-score: HOLDS on the 27B, the 9B and Qwen3-32B ([prereg amendments 3, 6](../breadth/prereg_replication_1022.md)), FAILS on Muse ([amendment 5](../breadth/prereg_replication_1022.md)). After the re-score's breakage gate: the 27B's and the 9B's HOLDS become PARTIAL, Qwen3-32B's does not survive. No data-file key holds these verdicts; the steering runs are not in the final design.

### C3, computed bridges sit in the J-space beyond their own word: **not tested in the final design**

- **Predicted (verbatim):** computed bridges (typo, translation) that feed a recall sit in the J-space beyond their own word, so H0 is false.
- **Status.** Tested only on the 20 Oct pilot set (suite_v1, 27B, [EXPERIMENTS.md 2026-10-20, computed and rwcomp rows](../archive/EXPERIMENTS.md)), before the dataset of record; not re-run on jsuite v2. The breadth README states it: "We have not tested, on v2, a bridge entity that the model computes rather than reads or recalls." Numbers computed from the passage are covered under H0.
- Note: Dan's depth claims live in `jobs/c3/` (named after the depth question "C3: the split"); that is not this C3.

## Pre-registered tests

### Architecture (22 Oct): C1 holds on Olmo-Hybrid-7B and fails on Olmo-3-7B: **failed**

- **Predicted (verbatim, [prereg amendment 6B](../breadth/prereg_replication_1022.md)):** C1-graded HOLDS on Olmo-Hybrid and FAILS on Olmo-3. Supported if both happen; refuted if Olmo-Hybrid FAILS or Olmo-3 HOLDS.
- **Decided by:** the powered test of [amendment 7A](../breadth/prereg_replication_1022.md) (olmo_big_v8), [EXPERIMENTS.md 2026-10-23](../archive/EXPERIMENTS.md).
- **Numbers (gap, points).** Olmo-Hybrid 7B {{b|old.oh7.olmoh7_big2_ko_v1}}, Olmo-3 7B {{b|old.o7.olmo3d7_big2_ko_v1}}: neither holds, so the hybrid-architecture prediction is refuted.
- **Within Qwen (amendments 3, 4):** the hybrid Qwen3.5-9B holds C1 (above) and the dense Qwen3-32B stays below the bar ({{b|old.q32.qwen3_32b_full2_ko_v1}} and {{b|old.q32.qwen3_32b_fresh2_ko_v1}}): **held** within Qwen, not across families.

### The Muse puzzle (22 Oct): removal barely touches Muse's recalls while writing redirects them: **did not reproduce** on jsuite v2

- **As stated (progress report, 22 Oct, verbatim):** "the knock-out barely touches recalls, while writing redirects 43–50%. Two readings: the knock-out never removes the bridge, or Muse carries it redundantly." (The 43–50% is the report's steering number, not in this repo's data files.) The diagnostic was pre-registered ([amendment 6C](../breadth/prereg_replication_1022.md)).
- **Numbers.** On the toy suite Muse's gap is {{b|old.mu.muse30_full2_ko_v1}}; on jsuite v2 it is {{bci|ko.mu.mk}}, of which the logit lens's own 10 directions take {{b|ko.mu.u}}.
- **Read.** The puzzle did not reproduce on jsuite v2: there the removal does break Muse's recalls ({{bci|ko.mu.mk}}), but {{b|ko.mu.u}} of it is shared with the logit lens, so the dependence is not specific to J++. The writing half of the puzzle rested on steering cells withdrawn on 24 Oct (C2).

### Gemma 4 31B: **not tested in the final design** (untestable)

- **Rule ([prereg](../breadth/prereg_replication_1022.md), 22 Oct):** a model is untestable with this knock-out if top-10 removal raises plain-text loss by ≥ 2.0 nats over unedited, with the rotated control within 0.3.
- **Numbers.** Plain-text cross-entropy added by the top-10 removal: Gemma 4 31B-it {{b|text.gemma}}; also gpt-oss-20b {{b|text.gptoss}} and Kolibri-1 {{b|text.kol}}.

## Longshots (sprint plan, 20 Oct)

### A pointer readout that steers the lookup (depth): **held in part**

- **Predicted (verbatim):** if the "around" route is pointers (binding or lookback IDs), build a pointer readout that steers the lookup.
- **Decided by:** the depth address tests (depth claims 6, 7, 9).
- **Numbers.**
  - Removing the address cuts position answers: 9B {{x|rt_C2_no_alf_position_9b}} and 27B {{x|rt_C2_no_alf_position_27b}}, against a random part of the same size {{x|rt_C2_no_alf_rand_position_9b}} and {{x|rt_C2_no_alf_rand_position_27b}}.
  - Swapping it (s = 2) moves the lookup to the target: 9B {{s|qwen3.5-9b|lookup target share, mean over locker pairs, s = 2}}, 27B {{s|qwen3.6-27b|lookup target share, mean over locker pairs, s = 2}}, Muse {{s|muse-glimmer-30b|lookup target share, mean over locker pairs, s = 2}}, Lightning {{s|nemotron-3.5-lightning|lookup target share, mean over locker pairs, s = 2}} (post hoc), 122B {{x|x8_t2_122b}} (post hoc).
  - Adding the address alone brings position answers back on the 9B ({{x|rtk_C2_keep_alf_position_9b}}) and Muse ({{x|rtk_C2_keep_alf_position_muse}}), not on the 27B ({{x|rtk_C2_keep_alf_position_27b}}).
  - The lens cannot read it: share rebuilt by 25 lens directions, 9B {{s|qwen3.5-9b|47.0 (b) share rebuilt by 25 lens directions: pointer}}, 27B {{s|qwen3.6-27b|47.0 (b) share rebuilt by 25 lens directions: pointer}}, Muse {{s|muse-glimmer-30b|47.0 (b) share rebuilt by 25 lens directions: pointer}}.
- **Read.** The address can be read (by a probe, not the lens), removed and swapped; added alone it fails on the 27B.
- **Links:** [depth README, claims 6, 7, 9](../depth/README.md).

### The OLMo-3-7B post-training ladder (base, SFT, DPO, Instruct): **not tested in the final design**

- **Predicted (verbatim):** does the split exist before post-training?
- **Status.** The 22 Oct ladder runs on OLMo SFT and DPO asked other questions (a slot phase and the late read; [predictions/2026-10-22_dan.md, Q6.15–Q6.16](../../predictions/2026-10-22_dan.md)), not the recall/lookup split. Related evidence on another family: the Qwen3.5-9B base model's split is {{b|v1.q9base.qa}} against the instruct model's {{b|v1.q9inst.qa}} (same format and lens; [prereg amendment 27](../breadth/prereg_replication_1022.md)), so on that model the split is mostly from pretraining.

## Feedback (Neel, 19 Oct)

- **"H0 is probably false": held** for recalled entities (see H0).
- **"The suite is too toy": answered.** The split holds on natural passages and the dataset of record (jsuite v2), [breadth README §2](../breadth/README.md).
- **"Try a larger model early": answered.** The 122B ran on v2 ({{bci|ko.q122.mk}}; by probability {{b|ko.q122.soft}}).
- **Narrow, rare concepts should differ: failed.** natplus, popular vs rare bridges: 9B {{b|natplus.q9.pop}} vs {{b|natplus.q9.rare}}, 27B {{b|natplus.q27.pop}} vs {{b|natplus.q27.rare}}.
- **No MoE-routing or verbalizer side checks: followed.**

## Zach's design ideas

- **The hop letters.** Each hop of a chain is P (read in the passage), M (recalled) or C (computed from the question); the breadth tests compare chain types such as P → M against M → P, and three-hop chains against P → P → P ([breadth README, Setup and §6](../breadth/README.md); prereg amendments 21, 25, 56).
- **The dataset ladder.** Toy puzzles → natural fact chains and natplus (rare bridges) → jsuite v1 → jsuite v2, the dataset of record (amendments 33, 35) → jsuite v4, the twin set: six people described, not named, with codename, conflict and key variants (amendment 58 note 14).
- **The specificity battery.** Every knock-out has same-size controls: the removal rotated to a random direction, the logit lens's own top 10, the same norm along the residual's top principal directions, and keeping the bridge's own word (27B: rotated {{b|ko.q27.rot}}, logit lens {{b|ko.q27.u}}, principal directions {{b|ko.q27.pcr}} of the effect, keep-own restores {{b|keepown.q27}}).

## Publication note

The three plan documents (the proposal, the sprint plan, the progress report) are quoted here and not added to the public repo (a call for Dan).
