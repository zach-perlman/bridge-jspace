# Pre-registration: replicating C1 and C2 on Mistral-Small-24B-2501 and Qwen3-32B (Zach, 2026-10-22 ~01:00 UTC)

Written after the queues were set (commits ccee329, 81796bb) and before any Mistral-Small-24B-Instruct-2501 or
Qwen3-32B result exists: no Mistral run has started, and Qwen3-32B's lens fit has only just started. Seen so far: every
Qwen3.6-27B result, including C2 on full_v8 (wm2_full2_v2), and every Gemma 4 31B-it result.

**Why.** The 27B is a single model. C1 failed on Gemma in a way that says nothing about C1: the knock-out wrecks Gemma's
plain text. So the claims need a second family (Mistral, lab and architecture unlike Qwen's) and a second Qwen
(Qwen3-32B, another generation).

**Models and lenses.**
- Mistral: solarkyle's plain J-lens (third party, 100 WikiText prompts; not J++). It is the only lens for this model.
- Qwen3-32B: our every-layer J++ (32 fit prompts).

The procedure is the 27B's, with depths scaled to each model (scripts/queues/h200_mistral_core_1022.sh,
h200_q32_core_1021.sh).

## C1: memory steps need the J-space, prompt lookups don't

- **Test.** C1-graded, as fixed in scripts/c1_v2.py (unchanged): gap >= 30 points with controls within 10. It runs at
  the middle band chosen on the model's own ctrl_v8 sweep (scripts/choose_band.py, unchanged), on full_v8.
- **Replicates on a model** if C1-graded HOLDS there and the model is testable (below).
- **Untestable gate (new, fixed now).** A model is "untestable with this knock-out", with no C1 verdict, if top-10
  removal at its relative-depth band both:
  - raises plain-text loss by >= 2.0 nats over unedited (scripts/removal_textloss.py), and
  - leaves the rotated control within 0.3 nats of unedited.

  The relative-depth bands are Mistral 20-25 and Qwen3-32B 32-40. For reference: Gemma 30-38 gives +9.25 nats (rotated
  +0.01); the 27B 32-40 gives +0.31 (rotated +0.08).
- **The lens bridge, for Mistral.** First run the 27B's C1 at 32-40 with solarkyle's plain 27B lens (q27solar_full2_ko_v1).
  - If C1-graded FAILS there, a Mistral C1 failure is not evidence against C1: lens type and fitter are confounded.
    A Mistral HOLD still counts.
  - If C1-graded HOLDS there, Mistral's verdict counts either way.

## C2: the lens writes bridges

- **Reported, unchanged.** The pre-registered C2-graded and C2-relative (scripts/c2_graded.py), on each model's two-step
  steering run on full_v8 (mistral24_wm2_full2_v1, qwen3_32b_wm2_full2_v1).
- **Confirmatory test: C2' (narrow), fixed now (scripts/c2_narrow.py).**
  - *Claim.* A bridge stated in the prompt (P) or computed in it (C) is written by its own lens direction only when the
    last step recalls from memory (X->M), not when it looks the answer up (X->P).
  - *Rule.* Use the cross-validated own-direction write, all cases. For each source X in {P, C}, X passes if all three
    hold:
    - X->M >= X->P + 10 points;
    - X->M >= 3 x X->P;
    - the lower end of X->M's best-cell 95% interval is >= the upper end of X->P's.
  - *Verdict.* HOLDS if both P and C pass, PARTIAL if one passes, FAILS if neither. UNDERPOWERED if any of the four words
    has < 30 cases.
  - *The drop-guessable split* is reported as a robustness check.
  - *The 27B* (wm2_full2_v2) is the data this rule was read off. There it HOLDS:
    - P: 1 -> 18 [14-30];
    - C: 0 -> 17 [11-33].

    That result is not evidence for the rule.
  - *Recalled bridges* (M->P, M->M) are reported, not tested. On the 27B they are written either way: 31 and 31.

## Wording fixed in advance

- **C1 "replicates on a second family"** only if Mistral C1-graded HOLDS, Mistral is testable, and the bridge does not
  undercut a failure.
- **C1 "replicates within Qwen"** only if Qwen3-32B C1-graded HOLDS.
- **C2' "replicates"** on a model only if it HOLDS there.
- **Every number** is one data seed (ctrl_v8 seed 712; full_v8 seeds 713-715) and one run. The rotated-control seeds
  and keep-own run after the core, in each model's rest queue.

## Amendment 1 (Zach, 2026-10-22 ~02:45 UTC): Muse Glimmer 30B replaces Mistral

- **What was seen when this was decided:**
  - Mistral's lens check and plain-text gate. It passed: +0.33 nats at top-10, rotated control +0.18.
  - Mistral's held-out ctrl_v8 sweep. The plain-lens knock-out barely moved anything: memory words kept 81-99% at every
    window, the largest memory-minus-lookup loss was 12 points, and the rule chose 6-11.
  - Mistral's test-set C1 had not been seen.
- **Mistral's status.** Its test-set C1 (mistral24_full2_ko_v1) finishes and is reported as "Mistral, third-party
  plain J-lens (100 prompts)". It is not the second-family test, and none of its other runs go ahead.
- **Second family: Muse Glimmer 30B** (meta-models/Muse-Glimmer-30B@cec94fc, Meta, released 2026-08, dense, 52 blocks).
  - *Lens.* Its published plain J-lens: eyes-ml/Muse-Glimmer-30B_jacobian-lens@71d8434, neuronpedia's fitter, 900
    WikiText prompts, fit on a byte-identical copy of the weights.
  - *Procedure.* Every rule above applies unchanged at Muse's depths:
    - the untestable gate at the relative band 26-32;
    - C1-graded at the band chosen on its ctrl_v8 sweep;
    - C2' on muse30_wm2_full2_v1.
- **The lens bridge** is now neuronpedia's plain J-lens for Qwen3.6-27B (1000 prompts; the fitter family of Muse's lens),
  in run q27jlens_full2_ko_v1 at 32-40.
  - If C1-graded FAILS there, a Muse C1 failure is not evidence against C1.
  - A Muse HOLD counts either way.
- **"Is the J-lens good enough" (Zach: if not, consider our own J++).** The decision is made with Zach, before Muse's
  test-set C1 is opened. It uses:
  - Muse's lens-agreement curve, against the 27B's J-lens and J++ (scripts/lens_agreement.py);
  - the 27B bridge.

  If a J++ is fit, J++ becomes Muse's lens of record, matching the other models, and both lenses are reported.

## Amendment 2 (Zach, 2026-10-22 ~02:55 UTC): our own J++ for Muse; the J-lens bridge dropped

- **Muse's lens of record is a J++ we fit**, as for every other model:
  - recipe: Qwen3-32B's, 32 WikiText prompts, safety-research/jpp_lens@93f02cd plus
    scripts/lens_fit/jpp_lens_muse_1022.patch (LRP class registry only, checked by scripts/lens_fit/check_muse_lrp.py);
  - target muse-glimmer-30b, run prefix muse30_.
- **Its published plain J-lens** (target muse-glimmer-30b-jlens, prefix muse30j_) runs only the lens check and the
  plain-text gate, as a comparison.
- **The 27B J-lens bridge is dropped** (Zach). It was there to interpret a plain-J-lens result, and Muse is now judged
  with a J++.
- **What was seen when this was decided:**
  - the 27B's lens-agreement curves: plain J-lens about the logit lens in the middle layers, J++ about +0.08 above it;
  - no Muse result of any kind.
- **Every rule above applies to Muse with the J++:**
  - the untestable gate at 26-32 (muse30_textloss_top_v1);
  - C1-graded at the ctrl_v8-chosen band;
  - C2' on muse30_wm2_full2_v1.

## Amendment 3 (Zach, 2026-10-22 ~17:00 UTC): where does C1 hold, and do the positive results survive their confounds?

- **What was seen when this was written:**
  - C1 on the test set: 27B HOLDS (gap 36), Qwen3-32B FAILS (22; a control 13 off), Muse FAILS (7 with our J++, 4 with
    its published J-lens);
  - C2 at the aligned band: Qwen3-32B HOLDS on all three rules, the 27B C2' HOLDS with C2-graded / -relative failing;
  - the removal-size check: on the 27B the top-10 J-lens removal takes ~1.5x the residual share of the top-10
    unembedding one, on Qwen3-32B the same share.
- **Nothing has been seen** of: the 9B, Qwen3-8B, Qwen3-32B with its published J-lens, layers 54-62 on Qwen3-32B, or
  the 27B's size-matched control.

**Predictions:**

1. **Architecture.** The hybrid linear-attention Qwen models (27B; Qwen3.5-9B, 24 of 32 layers linear) show C1;
   standard-attention Qwen models (Qwen3-32B; Qwen3-8B) don't.
   - Supported if the 9B's C1-graded (published J++, every model's procedure) HOLDS and Qwen3-8B's (published J-lens,
     5-layer windows sliding by 2 as the 9B, bands scaled from 64 to 36 blocks) FAILS.
   - Refuted if the 9B FAILS, or Qwen3-8B HOLDS.
2. **Lens.** Qwen3-32B's test-set C1 at its chosen band 44-52, with neuronpedia's published J-lens (557 prompts) in
   place of our 32-prompt J++.
   - A gap within 8 points of 22 -> the lens does not explain Qwen3-32B's weaker effect.
   - A gap >= 30 -> our fit understated it.
3. **C2 at late layers, a direct push on the answer?** Qwen3-32B's lens_add at the final position, single layers
   54-62 (the 27B's aligned run already falls to 0% at 56-60).
   - If M->M's best flips at 58-62 fall below half its layer-52 value (72%), the aligned-band C2 is not read as a
     direct output effect.
   - Otherwise it is flagged as possibly one.
4. **The 27B's specificity, size-matched.**
   - Choosing K: the unembedding K whose median removed share at layers 32-40 (scripts/removal_size.py, WikiText) is
     closest to the J-lens top-10's.
   - Run: unembedK + unembedK_rot at 32-40 on full_v8.
   - Specificity holds size-matched if that knock-out's gap is <= 10 (J-lens: 36).

## Amendment 4 (Zach, 2026-10-22 ~17:05 UTC): Qwen3-8B dropped

Qwen3-8B was dropped before it ran; no data from it exists. Prediction 1 (architecture) now rests on the 9B's C1-graded
alone, beside Qwen3-32B's existing result: supported if the 9B HOLDS, refuted if it FAILS.

## Amendment 5 (Zach, 2026-10-22 ~17:45 UTC): Muse's late-layer check

- **Seen when this was written:** Muse's aligned-band steering (22-32, final): C2-graded and C2-relative HOLD, C2'
  FAILS. Lens_add flips at the final position by single layer (M->M) rise to 67% at layer 32, the band's end.
- **The check:** Muse's lens_add at the final position, single layers 34-50 (muse30_wm2_full2_late_v1), with the same
  rule as prediction 3. If M->M's best flips at 46-50 fall below half its layer-32 value (67%), the aligned-band C2
  is not read as a direct output effect. Otherwise it is flagged.

## Amendment 6 (Zach, 2026-10-22 ~21:30 UTC): fresh data seed, the Olmo architecture pair, the Muse diagnostic

- **Seen when this was written:** every result in results/cross_model/summary.md, plus the 9B's C1 (gap 38, controls
  within 10), its specificity (logit lens -3), keep-own (26% restored), three control seeds, and its C2 at the
  pre-registered band 14-20 (C2-graded, C2-relative and C2' HOLD).
- **Nothing has been seen** of: the fresh set fresh_v8s2 (generated for this amendment, never run), either Olmo model,
  or the Muse diagnostic.

**A. Fresh data seed (the Day 3 plan's rule: a gap within 10 of 30, or models that disagree; both now true).**
- Data: fresh_v8s2 = full_v8's two-step recipe with seeds 721 / 722 / 723 (cf tier, levels 0-3; knock-out tier levels
  0-1; knock-out tier levels 2-3), merged by scripts/merge_tasks_sets.py: 1,072 items, the same per-word counts as
  full_v8. No prompt or context is shared with full_v8, full_v8b or ctrl_v8. The entity pool is the generator's fixed
  lists, so this resamples scenes, wordings, formats and numbers, not entities.
- Models and fixed bands (no re-choice): the 27B L32-40, the 9B L12-16, Qwen3-32B L44-52; each model's lens of record;
  competence on fresh_v8s2 first; paper10 and paper10_rot; scored by scripts/c1_v2.py, unchanged.
- Predictions: the 27B and the 9B HOLD C1-graded; Qwen3-32B's gap lands within 10 of 22.
- What follows: if the 27B or the 9B falls below 30, C1 is reported as a graded trend with intervals, not by the
  threshold (Day 3 fallback). Either way both data seeds are reported.

**B. Architecture: the Olmo pair.**
- Models: allenai/Olmo-Hybrid-Instruct-DPO-7B (Gated DeltaNet linear-attention layers plus full attention) and
  allenai/Olmo-3-7B-Instruct-DPO (dense: sliding-window plus full attention), DPO checkpoints on both sides (the hybrid
  has no RL-stage instruct model). Revisions are pinned in src/bridge_jspace/pins.py when registered.
- Lens: our own J++ on each, Qwen3-32B's and Muse's recipe (32 WikiText prompts, safety-research/jpp_lens@93f02cd,
  plus any LRP entries the Olmo classes need, each checked value-exact against the stock forward before fitting).
- Procedure: as every model. Lens check; plain-text loss under the knock-out (untestable if top-10 adds >= 2 nats with
  the rotated control within 0.3); competence on ctrl_v8 and full_v8; the middle band chosen on ctrl_v8 by
  scripts/choose_band.py with 5-layer windows sliding by 2 (as the 9B, also 32 blocks); C1-graded on full_v8 at that
  band; then the logit-lens specificity control, keep-own and two more control seeds; steering as every model.
- Power floor: if a model answers fewer than 30 items right on any of P->P, M->P, P->M, M->M of full_v8, its C1 is
  reported as descriptive only.
- Prediction (architecture): C1-graded HOLDS on Olmo-Hybrid and FAILS on Olmo-3.
  - Supported if both happen.
  - Refuted if Olmo-Hybrid FAILS (a linear-attention hybrid is not enough) or Olmo-3 HOLDS (a dense model can show it).

**C. The Muse diagnostic (descriptive; mechanism).** On items right unedited of full_v8's memory-final words (P->M,
M->M), for Muse at L36-42 and the 27B at L32-40 (reference):
- (a) the bridge's rank in the lens readout at each band layer at the question's last token and the final position;
- (b) the share of items whose bridge is among the top-10 directions the knock-out removes at those positions, at one
  or more band layers;
- (c) under the band knock-out, the bridge's lens rank 2 and 4 layers after the band.
- Reading: if (b) is below 20% on Muse and at least 50% on the 27B, the knock-out mostly misses Muse's bridge (the
  cross-model C1 difference is partly the tool's reach). If (b) is at least 50% on Muse, Muse's recall survives removal
  of its bridge's lens directions (redundant routes). Otherwise mixed.

**D. Descriptive additions.** The 9B: removal size at L12-16 (scripts/removal_size.py) and, if its J++ top-10 takes more
than 1.2x the residual share of the logit-lens top-10, the logit-lens top-K matched in share; the dose (top 1-100 and
rotated) at L12-16 on full_v8's 2x2 words. The 27B: the same dose at L32-40.

## Amendment 7 (Zach, 2026-10-23 ~01:10 UTC): a powered Olmo test and a third data seed for the 9B

- **Seen when this was written:** every result through Olmo-Hybrid's steering (EXPERIMENTS.md, 22 Oct): the fresh seed
  (27B 34, 9B 23, Qwen3-32B 17), the Olmo pair below the 30-item floor (Olmo-Hybrid gap 7 at L4-8, Olmo-3 -6 at
  L10-14), Olmo-Hybrid's dose (<= 7 at any K), the Muse diagnostic.
- **Nothing has been seen** of: the sets made for this amendment (olmo_big_v8, fresh_v8s3), or any run on them.

**A. The Olmo pair, powered.** Amendment 6B's test failed its power floor (24 and 20 items on M->P / M->M).
- Data: olmo_big_v8, the full_v8 generator on the 2x2 words only (P->P, P->M, M->P, M->M) with more scenes: the cf tier
  80 scenes per group x level (levels 0-3, seed 741), the knock-out tiers 60 (levels 0-1, seed 742; levels 2-3 P-start
  only, seed 743). No prompt shared with full_v8, full_v8b, ctrl_v8 or fresh_v8s2.
- Runs: competence on olmo_big_v8; C1 at each model's band already chosen on ctrl_v8 (Olmo-Hybrid L4-8, Olmo-3 L10-14;
  no re-choice) and, descriptive, at L12-16 (the 9B's relative depth); paper10 and paper10_rot; scripts/c1_v2.py.
- The test is amendment 6B's, now powered (floor 30 items on each rule word): the architecture prediction is supported
  if Olmo-Hybrid HOLDS and Olmo-3 FAILS; refuted if Olmo-Hybrid FAILS or Olmo-3 HOLDS.
- Our expectation after 22 Oct's descriptive results: both FAIL. If so, C1's strong form is scoped to the Qwen3.5/3.6
  hybrids. Gaps are reported with 95% bootstrap intervals over bridge entities, and pooled with full_v8 if both exist.

**B. A third data seed for the 9B** (its two seeds gave 38 [25-51] and 23 [13-33]).
- Data: fresh_v8s3, fresh_v8s2's recipe on seeds 731-733 (1,072 items). Competence; C1 at L12-16; paper10 and
  paper10_rot; scripts/c1_v2.py.
- Reported: the third gap with its interval, and the gap pooled over all three seeds. No new threshold: C1 for the 9B is
  read as the pooled graded gap (Day 3 fallback, already triggered).

## Amendment 8 (Zach, 2026-10-23 ~02:30 UTC): gpt-oss-20b, a non-Qwen model from a third lab

- **Why:** every non-Qwen model so far shows no strong need for the J-space (Muse 7; the Olmo pair underpowered), and a
  reviewer can say the non-Qwen models tested are weak or small. gpt-oss-20b (OpenAI, Aug 2025; MoE, 32 experts, 4
  active, 24 blocks alternating sliding-window and full attention) is a strong, widely used model from another lab.
- **Seen when this was written:** a 36-item smoke of its competence (gptoss_smoke_1023, seed 751): steps alone all right;
  whole questions P->P / P->M 100%, M->M 67%, M->P 0-33% (n=3 per cell). No knock-out, write or lens data.
- **Setup:** the harmony template opened on the final channel with reasoning effort low and no date line
  (pins.GPTOSS_TEMPLATE_EDITS), eager attention (learned sinks), MXFP4 experts dequantized to bf16.
- **Lens:** our own J++, the same recipe (32 WikiText prompts, every source layer 0-22, target the final block), with
  the LN rule only: gpt-oss has no dense gated MLP, and its routed experts keep standard gradients, which is what the
  rlens preset does to routed experts in every MoE model (scripts/lens_fit/jpp_lens_gptoss_1023.patch adds the "ln" preset
  and GptOssRMSNorm, checked value-exact before fitting).
- **Procedure:** as every model: the gate; competence on ctrl_v8 and olmo_big_v8 (amendment 7's powered 2x2 set, for the
  M->P pool); the band on ctrl_v8 with 4-layer windows sliding by 2; C1 at that band on olmo_big_v8, plus the logit-lens
  control, keep-own, and steering. Power floor 30 items per rule word.
- **Prediction:** given every non-Qwen result so far, C1-graded FAILS (gap < 30). A gap >= 30 would show strong J-space
  dependence outside the Qwen family. Either way: the write asymmetry (M->M writes > M->P writes) is expected, as in all
  six models so far.

## Amendment 7b (Zach, 2026-10-23 ~03:15 UTC): olmo_big_v8 without counterfactuals; gpt-oss steering on full_v8

- **What changed and why:** olmo_big_v8's cf tier (counterfactual search, single core) was still running after 2 h, with
  every Olmo and gpt-oss run waiting on it. The C1 runs of amendments 7A and 8 now use olmo_big_v8nc: the same generator,
  domains, levels and scene counts, on seeds 744 / 745 / 746, without counterfactual fields (2,000 items: 560 P->P, 560
  P->M, 440 M->P, 440 M->M; recall-start items at levels 0-3; no prompt or context shared with full_v8, full_v8b,
  ctrl_v8, fresh_v8s2 or fresh_v8s3). Counterfactual fields only matter for steering, not for C1.
- gpt-oss's steering uses full_v8 (with counterfactuals), as every other model's steering did; its competence on full_v8
  is added. Nothing else in amendments 7 and 8 changes (bands, rules, floors, predictions).
- **Seen when this was written:** no knock-out, competence or steering result on either big set.

## Amendment 8b (Zach, 2026-10-23 ~04:30 UTC): gpt-oss with the published plain J-lens, after our J++ failed the gate

- **Seen when this was written:** our J++ (LN rule only) fails the gate at L10-13: plain-text loss 3.38 nats unedited,
  top-1 +3.00, top-10 +4.73, rotated top-10 -0.04 (gptoss20_textloss_top_v1). Descriptive follow-ups
  (gptoss20_textloss_diag_v1, gptoss20_removal_size_v1): skipping sink positions +4.50; the logit lens's top-10 +1.37
  (rotated +2.24); the J++ top-10 takes 11% of the residual norm (other models 11-13%). On the same WikiText rows the J++
  puts the model's own next token in its top 10 at 0.00-0.02 of positions at layers 10-17 and 0.24 at layer 22, where the
  logit lens gets 0.03-0.49 and 0.97 (gptoss20_lens_agreement_v1); every other model's J++ is at or near the logit lens.
  So the gate failure may be this lens, not gpt-oss. No knock-out, write or lens-agreement data with the J-lens below.
- **What is added:** neuronpedia's published plain J-lens for gpt-oss-20b (neuronpedia/jacobian-lens@e166deb5,
  gpt-oss-20b/jlens/Salesforce-wikitext, sha256 2a8abf06..., 457 WikiText prompts), target gpt-oss-20b-jlens, prefix
  gptoss20j_. A labelled comparison lens (as Muse's and the 27B's plain J-lenses), not a J++.
- **Procedure:** the lens-agreement check (descriptive); the same gate at L10-13 (top-10 >= 2 nats with rotated within
  0.3 -> untestable). If testable: the band on ctrl_v8 (4-layer windows sliding by 2, scripts/choose_band.py); C1 at that
  band and at 12-15 on olmo_big_v8nc; c1_v2's C1-graded rule; the logit-lens control; one control seed. Competence runs
  are the model's own (gptoss20_*), lens-independent. Power floor 30 items per rule word.
- **Reading:** a J-lens C1 result is reported as plain-J-lens evidence, next to the 27B's own J-lens vs J++ bridge. If the
  J-lens also fails the gate, gpt-oss is untestable by the knock-out with both lenses; its steering (amendment 8, our J++)
  still runs. Prediction unchanged: C1-graded FAILS.

### 8b addendum (Zach, 2026-10-23 ~04:25 UTC): steering with the J-lens too

- **Seen when this was written:** the J-lens fails the gate (top-1 +2.85, top-10 +3.42, rotated +0.05;
  gptoss20j_textloss_top_v1), so gpt-oss is untestable by the knock-out with both lenses. The J-lens reads the model's
  next token far better than our J++ (0.85 vs 0.24 at L22). Our J++ steering (amendment 8) is running; none of its
  results, nor the copy sweep's, have been looked at.
- **Added:** the same steering with the J-lens (target gpt-oss-20b-jlens): write_max at 10-15 on full_v8, then the
  aligned band from its own copy sweep, scored by c2_graded / c2_narrow as every model. Reported next to the J++
  steering as a lens comparison; neither replaces the other. Expectation unchanged: M->M writes > M->P writes.

## Amendment 9 (Zach, 2026-10-23 ~06:25 UTC): overnight: seeds for the thin cells, the diagnostic on every testable model, C2 on a fresh seed

- **Seen when this was written:** everything in EXPERIMENTS.md through commit 00a2949: the 122B's C1 (gap 9 at L39-45, -3
  at L24-30), its logit-lens control, dose and diagnostic (bridge removed, still answered: the Muse pattern); gpt-oss
  untestable with both lenses; the existing all-layer knock-out rows (Muse 0-50 leaves recall intact; the 27B, 9B and
  Qwen3-32B collapse on every word). Nothing on the runs below.
- **A. Data seeds**, C1 at each model's fixed band, c1_v2's rule, power floor 30 items per rule word:
  the 27B on fresh_v8s3 at L32-40 (gaps so far 36, 34); Qwen3-32B on fresh_v8s3 at L44-52 (22, 17); Muse on fresh_v8s2
  at L36-42 (7); the 122B on fresh_v8s2 at L39-45 and L24-30 (9, -3). Predictions: the 27B HOLDS; Qwen3-32B FAILS with a
  gap of 10-30; Muse and the 122B FAIL with gaps under 15.
- **B. The diagnostic** (scripts/muse_diag.py, amendment 6C's procedure; descriptive), n 60 per memory-final word at
  each model's C1 band on its C1 set of record: the 9B at L12-16 (full_v8), Qwen3-32B at L44-52 (full_v8), Olmo-Hybrid
  at L4-8 and Olmo-3 at L10-14 (olmo_big_v8nc). Expectation: the 9B like the 27B (removing the bridge costs accuracy),
  the Olmos like Muse and the 122B (removed, still answered), Qwen3-32B between.
- **C. C2 on a fresh data seed** (fresh_v8s2, with counterfactuals), each model's full_v8 write_max settings, scored by
  c2_graded and c2_narrow: the 9B at 14-20 (full_v8: C2-graded HOLDS, 72 vs 8), Muse at 23-33 (HOLDS, 56 vs 6), the
  27B at 28-40 (FAILS, 40 vs 36). Prediction: the same verdicts.
- **D.** The 122B with the knock-out at every lens layer (L0-46), paper10 and rotated, on full_v8_two: the row every
  other model has (descriptive).
- Order: GPU 0 runs B, then A for the 27B, Muse (and C for Muse), Qwen3-32B, then D; GPU 1, after the 122B steering, runs
  A for the 122B, then C for the 9B and the 27B.
- **9 note (~06:35 UTC):** Qwen3-32B's weights were deleted on 2026-10-23 to free disk (Zach's OK); re-fetching 62 GB
  would leave ~13 GB on the shared disk. Its seed (A) and its diagnostic (B) are dropped; no Qwen3-32B data was taken.
- **9 note 2 (~06:20 UTC, Zach's call):** dropped before any of their data: Muse's and the 122B's second C1 seeds (gaps 7
  and 9 with ~100 items per word; the 9B's seed-to-seed spread is about +-8, so a second seed cannot plausibly reach 30)
  and the 27B's C2 on fresh_v8s2 (3.2 GPU-hours to replicate a C2 that fails on full_v8). The time goes to a natural-text
  pilot (amendment 10). Kept: the diagnostic (B), the 27B's third seed (A), C2 on fresh_v8s2 for the 9B and Muse (C), and
  the 122B all-layer row (D).

## Amendment 10 (Zach, 2026-10-23 ~07:15 UTC): the bridge-in-context control and a natural-text pilot

- **Seen when this was written:** amendment 9's 27B third seed (gap 40, HOLDS) and the diagnostics on the 9B,
  Olmo-Hybrid and Olmo-3; an audit of full_v8: the bridge word appears in the context of 112/112 items of every two-step
  word, M->M and M->P included (every scene states the start thing's pick and locker), so an M-start step is recall
  among entities listed in the prompt. Guessability does not explain the split (c1_v2 --drop-guessable: 27B 34, Muse 7).
  Nothing on the sets below.
- **A. Bridge absent (toy suite).** full_v8_mmabs (scripts/mm_absent.py): full_v8's 152 M->M items with every sentence,
  row, record or entry naming the bridge removed; nothing else changes. Per model: competence on it, then the paper10
  knock-out and its rotation at the model's fixed C1 band(s) (27B L32-40, 9B L12-16, Muse L36-42, 122B L39-45 and
  L24-30), M->M only. Compared on items right unedited in both sets (bootstrap over bridge entities): M->M accuracy lost,
  bridge present (the C1 run of record) vs absent. Prediction: if the redundant models (Muse, 122B) fall back on the
  in-context bridge, their M->M loss rises by >= 15 points when it is absent; the breakers' (27B, 9B) changes less.
  Descriptive.
- **B. Natural-text pilot (natural_v1).** Hand-built chains for three bridge types; hop 2 is a many-to-one property, never
  a name alias of the bridge (Neel's capital/country finding), and hop-1 descriptions do not name the hop-2 answer:
  countries -> continent; people (single-token surnames) -> nationality; non-capital cities -> country. Per chain the
  same bridge in all four words: P start = a new fact about a fictional person in the passage ("Lucia Ferrer grew up in
  Brazil"); M start = an indirect real description ("the country that hosted the 2016 Summer Olympics"); M final = the
  real property; P final = a new fact in the passage with an answer from the same vocabulary, never equal to the real
  one ("Brazil's delegation will hold its next meeting in Asia"). The bridge is absent from M->M passages. Passages:
  templated genres (news, email, forum, conference notes) with real WikiText sentences as filler, at two levels. Two
  framings, each its own set: cloze (raw text, no chat template, the answer is the next token) and chat with no prefill
  (the model's own first token must be the answer). Per model and framing: competence (whole question and each hop
  alone, first-token read), then C1 at the model's fixed band (27B L32-40, 9B L12-16, Muse L36-42, 122B L39-45), paper10
  and rotated, scored by c1_v2's rule (gap >= 30, controls within 10, floor 30 items per rule word). Prediction: the
  27B and 9B keep a gap >= 20 in at least one framing; Muse and the 122B stay < 15. A breaker with gap < 10 in both
  framings would mean the split is a property of the toy suite, not of the models. Descriptive (a pilot).
- **10B note (~07:40 UTC, before any natural knock-out):** the plain cloze framing failed on the 9B's competence
  (qwen35_9b_natural_v1_cloze_competence_v1: whole question 1-11% on P->P, P->M; the read token was " the" or ":";
  a 120-item probe: stems 0-9% on three words, raw "Question:/Answer:" 17-53%, the 9B wanting a blank line after
  "Answer:"). The pretraining-style framing is now natural_v1_qa: the same items as raw text with a fixed two-example
  Question/Answer preamble (scripts/natural_v1.py derive-qa), read after "Answer:". The chat framing was 71-89% whole on
  the probe and is unchanged. C1 runs on natural_v1_chat and natural_v1_qa for the 9B, 27B, Muse and the 122B; a framing
  a model cannot do shows up as too few eligible items (the 30-item floor). Also added for 10A: the bridge-present
  control is rerun M->M only on full_v8 (all M->M items the model gets right, not only whole scenes), so present and
  absent compare on ~100 items rather than ~30.
- **10B note 2 (~10:15 UTC):** seen: natural_v1_chat C1 for the 9B (gap 37), the 27B (gap 51, HOLDS) and Muse (gap 85,
  HOLDS: memory-final 9-11% under the knock-out, prompt-final 91-97%, rotated 94-98%). The prediction that Muse stays
  under 15 is falsified. Checks added before reading anything further, each model on natural_v1_chat at its band: the
  logit-lens control (unembed10 and its rotation; scripts/c1_specificity.py) and each step alone (paper10 and rotated,
  kinds step1 step2). Leading alternative to rule in or out: Muse's toy-suite null is specific to digit answers (the toy
  suite's every answer is a digit; natural answers are words).
- **10B note 3 (~10:20 UTC):** seen: the 122B on natural_v1_chat at L39-45 loses 89-99 points on every word (prompt-final
  too; rotated within 10), so that band cannot test the split on natural text. Added after seeing it: the same C1 and
  the logit-lens control at the 122B's other band of record, L24-30 (its toy-suite C1 ran at both). The L39-45 controls
  are dropped.

## Amendment 11 (Zach, 2026-10-23 ~12:00 UTC): a second natural seed, and Muse at a mid-depth band

- **Seen when this was written:** amendment 10's results (EXPERIMENTS.md through 6842f86): natural_v1_chat gaps 27B 51,
  9B 37, Muse 85, all J++; logit-lens gaps 0, -5, 55; the 122B breaks on every word at both bands.
- **A. Second data seed.** natural_v2 = scripts/natural_v1.py make --seed 802 (same fact tables and templates; new
  scenes, fictional people, distractor entities, P-final facts, genres and filler). Chat framing only. The 27B (L32-40),
  9B (L12-16) and Muse (L36-42): competence, then C1 (paper10, rotated) scored by c1_v2. Prediction: each keeps a gap
  >= 20 (27B >= 30).
- **B. Muse at L16-22** (a band of its toy C1 run of record, mid-depth) on natural_v1_chat: paper10, paper10_rot,
  unembed10, unembed10_rot; c1_v2 and c1_specificity. Reading: a J++ gap >= 20 with a logit-lens gap < 10 would make
  Muse's natural dependence J-specific at mid depth; a J++ gap < 10 would mean it shows only at the late band, where
  it is mostly shared with the logit lens. Descriptive.
- **11 note (~12:30 UTC):** seen: the second seed (27B 44, 9B 38, Muse 85) and Muse at L16-22 (gap -5). Added, same
  procedure and prediction as 11A: a third natural seed, natural_v3 (seed 803), chat framing, for the 27B, 9B and Muse.

## Amendment 12 (Zach, 2026-10-23 ~13:00 UTC): the natural pilot on the Olmo pair

- **Seen when this was written:** amendments 10-11 (natural gaps over three seeds: 27B 51 / 44 / 42, 9B 37 / 38 / 37,
  both J-specific; Muse 85 x3 at its late band, mostly shared with the logit lens, -5 at L16-22). The Olmos' toy C1 was
  a powered null (gaps 1 and 4). Nothing on the Olmos with natural data.
- **Procedure:** natural_v1_chat for Olmo-Hybrid (L4-8) and Olmo-3 (L10-14), their bands of record: competence, then C1
  (paper10, rotated) by c1_v2, then the logit-lens control (unembed10, rotated) by c1_specificity.
- **Prediction:** both stay null (gap < 15), as on the toy suite. A J-specific gap >= 30 would mean the toy suite hid
  their dependence too.

## Amendment 13 (Zach, 2026-10-23 ~13:45 UTC): a format-robust read for the natural sets

- **Seen when this was written:** everything through amendment 12 (EXPERIMENTS.md through 95f5897), and checks on the
  natural chat runs: wrong first tokens are almost all wrong answers, not format tokens (Olmo-3: "The" 57 times);
  dropping guessable items leaves the gaps (27B 52, 9B 39, Muse 86); the answer protection shields the bridge on
  8-15% of natural rows (toy 0%).
- **What changes:** a second read, "cand": an answer is right if its first token scores highest among its relation's
  answers (for hop 1, among the relation's bridges and people's first names). Format tokens ("The", whitespace)
  cannot fail it. Competence (eligibility) and the knock-out both use it in these runs; every row also keeps the
  top-token read. Re-scored: the 27B on natural_v1_chat (the run of record) and natural_v1_qa (0% under the top read);
  the 122B on natural_v1_chat at L24-30 with the logit-lens control; then the 9B and Muse on natural_v1_chat.
- **Prediction:** the 27B / 9B / Muse gaps move by < 10 points (their prompt-final words already rule out a global
  format change); if the 122B's breakage is a format artefact, its prompt-final words recover under "cand".

## Amendment 14 (Zach, 2026-10-23 ~17:45 UTC): natplus, a wider natural set with rare bridges

- **Seen when this was written:** everything through amendment 13's launch (its candidate-read results not yet in).
- **Set:** natplus_v1_chat (scripts/natplus.py, seed 901): natural_v1's three relations with their bridges ("popular")
  plus 47 lesser-known ones ("rare": 16 countries, 18 people, 13 cities), and a fourth relation, animal -> class
  (popular only); three wordings per fact and question; facts spliced into windows of consecutive real WikiText
  sentences; the bridge absent from M->M passages; chat framing; 2,336 items (584 per word; 752 with rare bridges).
- **Procedure:** per model at its band (27B L32-40, 9B L12-16, Muse L36-42, Olmo-Hybrid L4-8, Olmo-3 L10-14):
  competence and the knock-out with the candidate-rank read (amendment 13); conditions paper10, paper10_rot,
  unembed10, unembed10_rot; c1_v2 (the rule), c1_specificity, and scripts/natplus_split.py (by popularity and
  relation, bootstrap over bridges).
- **Predictions:** the 27B and 9B keep gaps >= 30 and >= 20 overall, J-specific (logit-lens gap < 10); Muse >= 30 at
  its late band, mostly shared with the logit lens; the Olmos < 15. Neel's narrow-concept prediction (narrowly used
  concepts may not use the shared direction): supported if, in the 27B or 9B, the rare-bridge gap is >= 15 points
  below the popular-bridge gap with the intervals apart; against it if the two are within 10. Rare bridges the
  model does not know drop out at competence, so "rare" here means known but less frequent.

## Amendment 15 (Zach, 2026-10-23 ~19:20 UTC): three-step natural chains

- **Set:** nat3_v1_chat (scripts/natural3.py, seed 1101): city -> country -> continent and person -> home country ->
  continent, start entities balanced across continents; all 8 words (PPP ... MMM), 224 items each; prompt facts are new
  facts about fictional people / partner cities / film casting / delegations, never the real value; an entity a memory
  hop must recall is in the passage only when a later prompt hop is keyed by it; every answer is unique among the routes
  that swap hop 2 or 3 to the other source and the route that skips hop 2. Clean words (no adjacent memory hops): PPP,
  MPP, PMP, PPM, MPM. Skip-prone (a memorized composite can replace two memory hops): PMM, MMM, MMP.
- **Seen when this was written:** competence (candidate read) for the 9B and the 27B; no knock-out data. Whole-question
  accuracy (guess-prompt rate): 27B PPP 54 (36), MPP 62 (31), PMP 58 (29), PPM 82 (28), MPM 74 (25), MMP 67 (23),
  PMM 97, MMM 90; 9B 32-44 on the six words with a prompt hop (guess 22-29), PMM 95, MMM 90. The 9B cannot compose
  these chains latently (its PMM / MMM are the memorized composites) and is not run; the 27B is. Estimated share of the
  27B's right answers that are real composition rather than lucky 5-way guesses: PPP ~52%, MPP ~73%, PMP ~70%, PPM ~91%,
  MPM ~88%, MMP ~85%.
- **Procedure (27B, L32-40):** per-word eligibility (whole and every hop alone right), the candidate-rank read, paper10,
  paper10_rot, unembed10, unembed10_rot; scripts/nat3_score.py: each word's loss and its excess over PPP, bootstrap over
  start entities; secondary: --min-p 0.5 (confident items only). Muse is added if its competence is like the 27B's.
- **Hypotheses:** H-final (the final hop's source decides): PPM and MPM excess >= 20; MPP and PMP excess <= 10. The toy
  suite's pattern (MMP high too) is the discriminating case, with the skip-prone caveat; PMM and MMM are expected high
  under H-final (descriptive). J-specificity: the logit-lens excesses < 10.

## Amendment 16 (Zach, 2026-10-23 ~19:45 UTC): is the memory-final loss about recall, or about what the prompt holds?

- **Seen when this was written:** natural_v1 / natplus results so far, and an observational split: memory-final items
  whose answer word happens to appear in the passage (as another fact's value) lose 15-25 points less under the
  knock-out (27B P->M 42 vs 66, M->M 44 vs 58; 9B 42 vs 60, 30 vs 47; Muse similar). natplus's animal relation is left
  out of headline numbers: its prompt answers need a case change ("reptile house" -> "Reptile"), and its P->P loses 24.
- **Set:** natctl_v1_chat (scripts/natctl.py, seed 1201): natplus's countries, people and cities (popular and rare),
  three wordings, coherent passages; per chain four final hops sharing one scene: P (a new fact in the passage), K (the
  passage states the TRUE fact for every entity; the question is M's), M (recall; the answer word absent), A (recall;
  the answer word present once as a distractor's value); starts P and M; 2,048 items, 256 per word.
- **Procedure:** the 27B (L32-40) and 9B (L12-16): competence and knock-out with the candidate read, scene eligibility
  (all four versions of a chain right), paper10, paper10_rot, unembed10, unembed10_rot; scripts/natctl_score.py.
- **Predictions (27B, 9B):** stating the true fact rescues: K - M <= -25 (K's loss well below M's); the answer word's
  presence partly rescues: A - M <= -10; a known vs a new fact in the prompt matters little: |P - K| <= 10. If instead
  K ~ M, the dependence is about recalling known facts even when they are in the prompt, not about where the fact is.

## Amendment 17 (Zach, 2026-10-23 ~19:45 UTC): bands chosen on natural data

- **Why:** every natural run used the band chosen on the toy suite's ctrl_v8.
- **Dev set:** natplus_dev_chat (scripts/natplus.py, seed 902, one scene per bridge, level and start group), no
  passage shared with natplus_v1. Sweep (paper10, paper10_rot, n 100 per word, candidate read): the 27B windows of 9 by
  4 (L0-8 ... L52-60), the 9B windows of 5 by 2 (L0-4 ... L26-30), Muse windows of 7 by 3 (L0-6 ... L42-48).
- **Rule:** scripts/choose_band.py as on ctrl_v8 (most-broken memory-final words among windows whose rotated control
  keeps every word >= 90%). Also reported, descriptive: the window with the largest memory-final minus prompt-final gap.
  If a model's natural band differs from its toy band, C1 is rerun on natplus_v1_chat at the natural band.

## Amendment 18 (Zach, 2026-10-23 ~20:15 UTC): WorkspaceBench's wrong-bridge items, causally

- **Seen when this was written:** WorkspaceBench's README and items (camilablank/workspace-bench@ba33098, MIT): 100
  raw-text two-hop prompts on which Qwen3.6-27B resolves a wrong bridge B' and answers hop2(B') = A' (gated by the
  benchmark: >= 4/10 samples give A' and B'; injecting B' gives A', injecting B gives A). No run of ours on them.
  Also seen: natctl on the 9B (stating the true fact rescues the memory-final loss, K - M = -50) and the 27B's
  three-step results.
- **Procedure (scripts/wrong_bridge_causal.py, the 27B at L32-40):** teacher-forced log-probabilities of the full
  answers A' and A, edits on prompt positions only; knock-out paper10, paper10_rot, unembed10 and paper10_spare (never
  removing B''s surname-token direction); lens writes unit(v_B - v_B') and, as control, unit(v_C - v_B') (C another
  item's true bridge) at the band's layers, last position or the prompt span, alpha 0.1-0.8; the write cell chosen on
  even-indexed items by B's flip rate, scored on the odd ones. Screens (no edits) on the 9B, Muse and the 122B: which
  items they also answer through the wrong bridge; if >= 30 transfer to the 9B, the same causal test runs on them.
- **Predictions (27B):** the knock-out lowers logP(A') at least 2 nats more than its rotation does, and the margin
  logP(A') - logP(A) falls (interval below 0) while the rotated margin's interval covers 0; sparing B''s own direction
  recovers >= 30% of paper10's margin drop; writing the true bridge flips >= 20% of held-out items to A while the
  control person flips <= 5%. Together: the J-space carries the bridge the model actually uses, even a wrong one.
- **18 note (~20:25 UTC, after a 4-item smoke, before any real run):** writes at alpha 0.4 over all nine band layers
  destroy both answers (logP falls 29-38 nats), so flips stop meaning anything (the control person flipped as often
  as the true bridge). Changes: alphas 0.02 0.05 0.1 0.2 0.4 (0.8 dropped); writes at the band's middle layer alone
  ("mid") as well as jointly; the cross-validated cell is chosen (by B's flip rate on even items) only among
  non-destructive cells, where the better of the two answers loses < 3 nats on even items; every cell's B and C flip
  rates are also reported. Predictions unchanged.

## Amendment 19 (Zach, 2026-10-23 ~20:40 UTC): what the model says under the knock-out; two more natplus seeds

- **Seen when this was written:** amendments 13-18's results except the band sweeps, the 27B natctl and the 9B
  natplus: the 27B natplus gap 50 (popular 48, rare 55), the 9B natctl (K - M -50), the 27B three-step, the 27B
  wrong-bridge test (knock-out margin -2.5 vs rotated -0.5; held-out writes B 24% vs C 14%), and the wrong-bridge
  screens (9B 22 and Muse 23 of 100, under 30: no causal run on either; the test stays a 27B in-depth check).
- **A. Generation spot-check (scripts/gen_spot.py):** the candidate read scores the first token only. For the first
  25 eligible items per word (PP PM MP MM) of natplus_v1_chat, greedy 12-token replies unedited and under paper10,
  paper10_rot and unembed10 at the model's band (27B L32-40, 9B L12-16, Muse L36-42), edits on prompt positions only
  as in ablate_v2. Replies classed: answer, bridge (the bridge or one of its names: hop 1 given instead of hop 2),
  other_cand (another answer of the relation), other. Predictions, 27B: the first step's candidate read agrees with
  the knock-out run's rows on >= 95% of item x condition pairs; under paper10, > 50% of memory-final candidate-read
  failures name another answer of the relation and < 20% name the bridge; prompt-final replies stay right on >= 85%;
  rotated and unembed10 replies stay right on >= 90%. Muse: a visible share of its paper10 replies is "other" (its
  top-read gap was a third larger than its candidate-read gap). Descriptive, no rule.
- **B. Data seeds:** natplus_v2_chat (seed 903) and natplus_v3_chat (seed 904), made exactly as natplus_v1 (2 scenes
  per bridge; 2,336 items each, no passage shared with natplus_v1). The 27B at L32-40 and the 9B at L12-16 as
  amendment 14 (candidate read, paper10 / rot / unembed10 / rot, c1_v2, c1_specificity, natplus_split).
  Predictions: amendment 14's for each seed; the popular-rare comparison is also pooled over the three seeds.

## Amendment 20 (Zach, 2026-10-23 ~21:05 UTC): review fixes: the cand2 read, reruns, corrections

- **Seen when this was written:** a read-only review of today's code, data and results (three passes: datasets;
  scoring and eligibility; new scripts, queues and recomputed numbers). Every headline number recomputed from rows
  matched. All results of amendments 13-19 except the band sweeps and the 27B natctl.
- **Bug:** natural_v1.py competence accepted a first name at hop 1 only from natural_v1's FIRST_NAMES; natplus adds
  its 18 rare people's first names on import, which competence never does. Their hop 1 failed the candidate read, so
  most rare-person scenes starting from memory were never eligible (27B: 8 of 54). It touches natplus (every seed and
  dev), natctl and nat3 eligibility, not natural_v1-v3. The items' own alts were always right.
- **Flaw:** animals' prompt-final values are written lowercase and the model answers lowercase, while the candidate
  read compared capitalised tokens (27B: every PP and MP animal item fails the top read unedited).
- **New read cand2** (ablate_v2 and natural_v1 competence, --read cand2): every candidate in either case; right if the
  top candidate token is a form of the answer or, at hop 1, of one of the item's own names for the bridge. cand is
  unchanged; all reads are recorded.
- **Reruns under cand2**, as amendments 14, 15 and 19: natplus_v1_chat for the 27B (L32-40), 9B (L12-16) and Muse
  (L36-42); nat3_v1_chat for the 27B; gen_spot for the three (checked against these runs, TF32 as ablate_v2, and a
  reply class "lure" for PM: the value the shared passage gives the bridge itself, i.e. its PP answer);
  natplus_v2_chat for the 27B and 9B. Not rerun: the Olmos' natplus (null), natctl (its contrasts are within scenes;
  the missing scenes change its mix, noted). The cand runs stay on record, superseded for natplus and nat3.
  natplus_v3 is not run (see a).
- **Predictions:** amendments 14 and 15 unchanged; the 27B's people/rare memory-start n rises from ~8 to ~50; the
  popular-rare comparison is also reported without animals (every animal is popular).
- **Corrections:**
  (a) natplus_dev and natplus_v1-v3 share their chains (bridges, facts, hop-1 descriptions); only passages and
  wordings differ. A band chosen on dev is chosen on the test facts, so the band sweeps are descriptive, no C1 rerun at
  a natural band counts as a test, and the 27B sweep is dropped. natplus_v1-v3 are rendering seeds of one fact set;
  the intervals over bridges carry the fact sampling.
  (b) natplus (and natural_v1) PM passages give the bridge a made-up value from the same answer list under another
  relation (e.g. where its delegation meets next); MM passages never name the bridge. PM and MM are reported
  separately, and MM - MP is the lure-free gap. About 30% of memory-final passages also hold the answer word as
  another entity's value (conservative; natctl M has none).
  (c) Amendment 18's write and spare tests used each surname's first sub-token as its concept (fragments for 59 of
  100 B', e.g. Beethoven -> " Be"; two items' B and C share a token). Only 22 items have single-token, distinct B and
  B'. The write and spare results are withdrawn, not rerun; the knock-out result (no token choice) stands.
  (d) nat3: chains through South Africa are left out of scoring (nat3_score --drop; its name contains the answer
  Africa, and its first token is South America's).
  (e) Queues count failed steps and exit nonzero; gen_spot --check takes finished runs only; result directories are
  committed only once they have summary.json (commit 7546083 included partial rows of then-running runs).
- **20 note (~22:25 UTC, after the 9B's spot-check, before the 27B's and Muse's):** the first 25 eligible items per
  word were all countries (file order), so gen_spot now takes the first 25 per word and relation (--strata domain)
  and reports the most common wrong replies and the classes per relation. The 9B's spot-check is rerun this way
  (qwen35_9b_natplus_v1_chat_genspot_cand2_strat_v1). Seen: the 9B's first spot-check (its memory-final failures
  name another continent, almost always Europe; 394 of 400 first-step reads agree with the knock-out run).

## Amendment 21 (Zach, 2026-10-23 ~22:55 UTC): computations on the passage (ctxcomp_v1)

- **Why:** the TA review (23 Oct). "Prompt" has meant reading a stated fact. Do computations the model performs on
  the passage, whose result is never written, need the J-space? Gurnee et al. (2026, 3.5.1) find Claude's linewrap
  count automatic (a J-lens swap leaves the wrap unchanged) while its explicit report goes through the J-space.
- **Seen when this was written:** amendments 13-20's results (the 9B natplus cand2 gap 40; the 27B and 9B natctl:
  stating the true fact removes the loss); not yet the 27B and Muse cand2 natplus runs.
- **Set:** ctxcomp_v1_chat (scripts/ctxcomp.py, seed 2101): a number X in 2-8, stated in the passage (start P),
  counted from a list (K), computed by adding or subtracting two numbers in the passage (A), or recalled (M: legs,
  sides, wheels, strings); used by the final step: report it (R), a lookup keyed by X (P: whose seat is at that
  position, the row listed with ordinal words so the digit X is not in the passage), or a recall keyed by X (M: the
  planet, Greek letter or month at that position; elements dropped, Beryllium and Boron share a first token). 12 words x 84 items; R, P and M of one start share the passage
  (scene eligibility). X is never written in K, A or M passages; two other people get other values. The P final needs
  a digit -> ordinal step ("4" -> "fourth"), a small lexical mapping.
- **Procedure:** the 27B (L32-40) and 9B (L12-16): competence (cand2) and the knock-out (paper10, paper10_rot,
  unembed10, unembed10_rot) on the whole questions, cand2 read; descriptive: the J-lens rank of X's digit at the band.
- **Predictions** (loss = points lost among items right unedited; controls within 10):
  (1) *Final-hop rule (C1 extended):* for every start, loss(SM) - loss(SP) >= 20, including the computed starts K and A.
  (2) *Computation alone does not need the J-space:* loss(KP) and loss(AP) within 10 of loss(PP).
  (3) *Explicit report (the paper's flexible use):* loss(KR) and loss(AR) >= loss(PR) + 15.
  (2) and (3) can both hold (report differs from use). **Kill for the memory-vs-prompt framing:** loss(KP) or loss(AP)
  >= loss(PP) + 20 with controls within 10: then computations on the passage route through the J-space as recalls
  do, and the split is computed-or-recalled vs read, not memory vs prompt.
- **21 note (~22:50 UTC, before any ctxcomp knock-out data; only a 9B competence smoke running):** the knock-out's
  dictionary has been letter-bearing tokens only since ablate_v2 v1 (model.letter_token_ids), so a digit token's
  direction is never removed. ctxcomp's X is a number: a null on K or A could be the dictionary, not the J-space.
  Every ctxcomp knock-out is therefore run twice, with the standard dictionary and with digit tokens added
  (ablate_v2 --dict-digits; runs *_dd). Predictions apply to both; if they disagree, the digits run is the test of
  the number intermediates and the standard run the comparison with every earlier result.

## Amendment 22 (Zach, 2026-10-23 ~23:00 UTC): a probe ceiling for the J-lens (scripts/probe_vs_lens.py)

- **Why:** the TA review: probes can show what the J-lens cannot; how much of an intermediate does the J-lens explain,
  at which layer, and so where should edits go?
- **Seen when this was written:** ctxcomp's 9B competence smoke only (no knock-out, no activations).
- **Procedure:** ctxcomp_v1's eligible items per word (the 27B and 9B), unedited, last prompt position, every second
  layer (27B) or every layer (9B): a linear probe for X (5-fold over scenes) as the ceiling; the J-lens and logit-lens
  reads of X (no training, X's digit and number-word tokens); and the share of the class means' spread inside the span
  of those tokens' J-lens vectors (against a random subspace of equal size).
- **Expectations (descriptive, no rule):** the probe decodes X at the knock-out band for every start (>= 80% where
  the model is competent). If the J-lens reads X at the band for M starts but well below the probe for K and A starts,
  computed numbers sit mostly outside the lens-readable space, and a knock-out null on K and A says little about them
  (read with amendment 21's two dictionaries).
- **21 note 2 (~23:00 UTC, after the 9B's ctxcomp competence and a mechanical probe smoke, before any ctxcomp
  knock-out data):** the 9B reports X at 99-100% for every start and answers each lookup or recall alone at 72-100%
  (seats 100%, months 100%, planets 82%, Greek letters 72%), but composes them in one pass at 15-29% (seat lookup) and
  4-96% (recalls; months best, from a stated X 96%). Scene eligibility would leave about 5-12 items per word. Every
  ctxcomp knock-out therefore uses per-item eligibility (ablate_v2 --tasks-per-word: each item right on all its own
  prompts; runs *_pi), for both models; words are then compared on different items of the same scenes. Prediction 3
  (report) rests on the R words (about 84 items each); predictions 1 and 2 are reported with their n and called
  underpowered below 30 items per word, as for C1. probe_vs_lens takes every item whose X report is right
  (--select step1), since a probe of X needs X computed, not composed. If the 27B's competence also shows the seat
  lookup failing to compose, the P final is redesigned (ctxcomp_v2) before its knock-out is read.

## Amendment 23 (Zach, 2026-10-23 ~23:20 UTC): the combined suite, module 1 (fact chains, jsuite_v1_facts)

- **Why:** one item schema, eligibility rule and read for every model, built with the fixes of amendment 20 and the
  TA review (story memory as a third kind of start; a held-out band-choice split).
- **Seen when this was written:** all results through amendment 22's 9B probe (a computed X is not linearly
  decodable at the 9B's last position at L12-16; recalled X partly is), the 9B natplus cand2 runs, the 27B and 9B
  natctl.
- **Set:** scripts/jsuite_facts.py (seed 2301): country -> continent, person -> nationality, city -> country (natplus
  tables, popular and rare; animals dropped). Starts: P (a fictional person's binding), M (an indirect description),
  T (tracked: where one of two objects moving in interleaved sentences went last; story memory). Finals as natctl: P
  new fact, K true fact stated, M recall with the answer absent, A recall with the answer present once elsewhere; the
  four finals share a scene and differ only in final-hop sentences (no lure). 12 words. Bridges split per relation and
  popularity into dev (jsuite_v1_facts_dev_chat, 3,024 items) and test (jsuite_v1_facts_test_chat, 3,120 items), no
  bridge in both. Fixed question templates; filler sentences end in . ! ?, ASCII, no digits. Final answers have
  distinct first tokens in all six tokenizers (27B, 9B, Muse, 122B, Olmo-Hybrid, Olmo-3). Known: some recalled
  descriptions carry a language cue to the answer (La Scala, Blood Wedding).
- **Hop 1 by generation:** bridge names share first tokens in every tokenizer (e.g. 37 of 47 people), so competence
  checks hop 1 by its generated name too (natural_v1 competence --hop1 gen: greedy, 8 tokens, any of the item's names
  as a word); final answers keep the cand2 read.
- **Procedure:** test split at each model's pre-registered band (27B L32-40, 9B L12-16, Muse L36-42): competence
  (cand2, --hop1 gen), the knock-out (paper10, paper10_rot, unembed10, unembed10_rot) on the 12 words, scene
  eligibility, natctl_score-style contrasts per start; the dev split only for any band sweep.
- **Predictions:** for every start (P, M and T), K - M <= -30 and A - M < 0 (as natctl); within each start, M - P >= 20
  (the memory-final rule); T behaves as P (a passage-read bridge): TM - TP within 10 of PM - PP.

## Amendment 24 (Zach, 2026-10-23 ~23:45 UTC): the combined suite, module 2 (numbers, jsuite_v1_numbers)

- **Seen when this was written:** ctxcomp_v1 competence (27B and 9B) and the 9B's ctxcomp knock-outs with both
  dictionaries: computing a number from the passage and reporting it costs the 9B 1-2 points under the knock-out
  (KR, AR vs PR 0-1; n 83-84), reporting a recalled number 19-21 (rotated 2); the seat lookup composes poorly (27B
  19-43%, 9B 15-29%) and even a stated number's seat lookup lost as much as a recall on the 9B (the digit -> ordinal
  step); recall finals compose on the 27B (54-80%).
- **Set:** scripts/jsuite_numbers.py (seed 2401, 8 repetitions): starts P stated, K counted, A arithmetic, M recalled
  (toy domains plus "days in a week"); finals R report (own passages, no list), L a lookup keyed by the number in a
  digit-labelled list ("Locker 5 belongs to Kate"; no mapping step), M the month or planet at that position. 12 words
  x 112 items. No "notes" genre (its header names a month); no month or planet names in the filler.
- **Procedure:** competence first (27B and 9B; the knock-out runs only on words with >= 30 eligible items), then the
  knock-out at each model's band with both dictionaries (letters; --dict-digits), per-item eligibility.
- **Predictions:** (1) report: KR and AR within 10 of PR, MR >= PR + 15 (the 9B's ctxcomp pattern); (2) final rule:
  for each start, SM - SL >= 20; (3) computation feeding a lookup: KL and AL within 10 of PL.

## Amendment 25 (Zach, 2026-10-24 ~00:20 UTC): the combined suite, module 3 (three-hop, jsuite_v1_threehop)

- **Seen when this was written:** amendment 15's 27B three-step results (cand read) and the amendment 20 review
  (South Africa leak; rotated control > 10 on 5 of 8 words); not the cand2 rerun of nat3 (running).
- **Set:** scripts/jsuite_threehop.py (seed 2501): natural3's design with South Africa, Cape Town, Mandela and Tutu
  removed from its tables; everything else as nat3_v1.
- **Procedure:** the 27B only (the 9B and Muse do not compose three hops): competence (cand2, --hop1 gen) and the
  knock-out at L32-40 (paper10, paper10_rot, unembed10, unembed10_rot), per-item eligibility as nat3, nat3_score.
- **Predictions:** as amendment 15's post hoc reading, now stated in advance: read as knock-out minus rotation, the
  memory hops whose output is not in the prompt (PPM, MPM, MMP, PMM, MMM) each lose >= 15 more than PPP; MPP and PMP
  within 10 of PPP.

## Amendment 26 (Zach, 2026-10-24 ~00:35 UTC): framings of the combined suite (TA review: no chat template; prefills)

- **Sets:** jsuite_v1_facts_test_qa (raw text, natural_v1's two-example Question/Answer preamble, read after
  "Answer:") and jsuite_v1_facts_test_prefill (the chat turn with the assistant turn prefilled "Answer:", thinking off),
  both derived item for item from jsuite_v1_facts_test_chat (natural_v1.py derive-qa / derive-prefill; kind "word":
  the answer is read with a leading space).
- **Procedure:** as amendment 23 (cand2, --hop1 gen, scene eligibility, the same conditions and band) for the 27B and
  the 9B.
- **Prediction:** the framing changes no start's K - M or M - P by more than 10 points from the chat run (the
  memory-vs-prompt split is not a chat-template effect); if the prefill run differs, the chat run's answer position is
  the suspect (post-training placing information on template tokens).

## Amendment 27 (Zach, 2026-10-24 ~03:00 UTC): base vs instruct (Qwen3.5-9B-Base) and the 122B on module 1

- **Seen when this was written:** module 1 on the 27B (M - P +50, J-specific), 9B (+42) and Muse (+68, two thirds
  shared with the logit lens); module 2 on the 9B and 27B; the 9B's module 1 framings not yet.
- **A. Base vs instruct:** our own J++ fit with one recipe (scripts/queues/h200_q9fit_1024.sh: jpp_lens@93f02cd as
  patched, 32 WikiText prompts, layers 0-30) on Qwen3.5-9B-Base (target qwen3.5-9b-base) and on Qwen3.5-9B
  (qwen3.5-9b-ourjpp), so the two are compared on matched lenses (the published base lens is a plain J-lens, the
  published instruct lens J++). Then module 1 in raw-text framing (jsuite_v1_facts_test_qa; base models take no chat
  template) at the 9B's band L12-16, as amendment 23. The instruct 9B's published-J++ QA run is the reference.
- **Predictions:** the instruct-ourjpp run reproduces the published-J++ QA run within 10 points on M - P (our recipe
  works on Qwen3.5). Base vs instruct is two-sided: if post-training creates the dependence (the paper: post-training
  installs the Assistant's point of view in the workspace), the base's M - P is >= 15 points below the instruct's; if
  the dependence is a pretraining property, within 10.
- **B. The 122B on module 1:** Qwen3.5-122B-A10B (FP8) at its pre-registered C1 band L39-45, chat framing, as
  amendment 23. Prediction (from its toy and natural nulls and the redundancy diagnostic): M - P < 15.

## Amendment 28 (Zach, 2026-10-24 ~03:20 UTC): a strong non-Qwen model, Kolibri-1, with the paper's own lens

- **Why:** every model with a strong, J-specific memory-final dependence so far is a Qwen3.5/3.6 dense hybrid. The
  strongest open non-Qwen model that fits one H200 (chosen by benchmarks on 2026-10-23: GPQA Diamond 84.3 vs
  Qwen3.6-27B 87.8; LiveCodeBench v6 85.9 vs 83.9) is Kolibri-1 (Aleph Alpha, 2026-10-03; MoE 78B total / 3.46B
  active, FP8; sliding-window and full attention; Apache 2.0). No published lens exists for it.
- **Seen when this was written:** module 1 on the 27B, 9B and Muse; module 2 on the 27B and 9B; nothing on Kolibri.
- **Procedure (scripts/queues/h200_kol_1024.sh):** transformers >= 5.20 in a separate env; a plain J-lens fit with
  Anthropic's jlens (scripts/lens_fit/fit_jlens.py; 500 pinned WikiText rows; Neuronpedia's recipe otherwise); target
  kolibri-1; lens_agreement; plain-text gate (removal_textloss, top10 vs rotated, layers 15-35; as for Gemma and
  gpt-oss: untestable if the top-10 removal alone raises plain-text loss by >= 2 nats while the rotation stays within
  0.3); the band chosen on the jsuite dev split (bridges disjoint from the test split; choose_band on PP PM MP MM,
  windows of 7 layers by 3); module 1 on the test split at that band, as amendment 23.
- **Lens-matched comparison:** the 27B on module 1 with its published plain J-lens (target qwen3.6-27b-jlens) at
  L32-40.
- **Predictions:** Kolibri-1: if it passes the gate, M - P < 15 (as the other MoE, the 122B, which routed around the
  knock-out); a J-specific M - P >= 20 (logit-lens < 10) would show the dependence is not specific to the Qwen dense
  hybrids. The 27B with the plain J-lens: M - P >= 30 (the plain lens may be weaker than J++, as on Qwen3-32B).

## Amendment 29 (Zach, 2026-10-24 ~03:35 UTC): module 1 robustness: a second rendering seed and held-out bands

- **A. Rendering seed:** jsuite_v1_facts_s2 (scripts/jsuite_facts.py --seed 2302 --split-from jsuite_v1_facts): the
  same facts and dev/test split, new passages and wordings (no passage shared with seed 2301). Module 1 on its test
  split for the 27B (L32-40) and 9B (L12-16) as amendment 23. Prediction: each start's M - P and K - M within 10 points
  of seed 2301's.
- **B. Bands on held-out bridges:** the 27B (windows of 9 by 4) and 9B (windows of 5 by 2) swept on
  jsuite_v1_facts_dev_chat (bridges disjoint from the test split, unlike natplus_dev), choose_band on PP PM MP MM. If a
  model's dev band differs from its toy band, module 1's test split is rerun at the dev band and reported beside the
  toy-band run (the toy-band run stays the pre-registered test).
- **28 note (~03:15 UTC, before any Kolibri-1 data):** the lens plan above is revised. Every other model in the
  cross-model comparison uses J++ (published for the 27B and 9B; our own fits for Muse, Qwen3-32B and the Olmos), and
  lens type moves the result (Qwen3-32B: gap 12 with its plain J-lens vs 22 with J++), so a Kolibri-1 null under a
  plain J-lens could not be told from a weaker lens. J++ (our recipe, as for every model we fit) is Kolibri's primary
  lens; the plain J-lens (the paper's own method, with the 27B's plain-J-lens run beside it) is secondary. Order:
  feasibility first (scripts/queues/h200_kolchk_1024.sh): competence with thinking off on the test split (Kolibri's
  card reports reasoning-on benchmarks; if it cannot do the tasks without reasoning, nothing else runs), and whether a
  lens can be fit on the FP8 weights at all (both fitters need gradients through every block; if the FP8 kernels have
  no backward, the fit needs the dequantized bf16 weights on two GPUs). The band is still chosen on the dev split.
- **26 note (~03:40 UTC, after the 27B's QA competence and the 9B's QA and prefill runs):** in raw-text QA framing the
  instruct models do not answer: after "Answer:" the 27B generates "<think> Here's a thinking process" on ~99% of
  hop-1 prompts (hop 1 by generation right 1%, by the first-token candidate read 97%), so no tracked-start scene is
  eligible and the 27B's QA knock-out did not run; the 9B starts thinking on 6% and its top read trails the candidate
  read by 21 points (0.66 vs 0.87 whole). The candidate read ranks the relation's answers even when the model's mass is
  elsewhere, so raw text is off-policy for instruct models and their QA runs are reported as such (the 27B's: not
  testable this way). In chat and prefill framings the top and candidate reads agree within 1 point and module 1's
  knock-out gives the same contrasts under the strict top read (27B M - P 50 vs 51, 9B 42 vs 46). For amendment 27
  the instruct 9B (our J++) is also run in chat, its on-policy framing; the base's QA run is compared with it, and the
  instruct QA run is kept as the framing-matched check.
- **28 note 2 (~04:10 UTC, after Kolibri-1's test competence and the FP8 backward check, before any Kolibri lens or
  knock-out data):** seen: Kolibri-1 on the module 1 test split (chat, thinking off, cand2, hop 1 by generation; 3,120
  items): whole 0.79 (27B 0.96, 9B 0.83, Muse 0.80), hop 1 0.91, hop 2 0.99, answerable without hop 1 0.30 (27B 0.34);
  weakest words TP 0.43, TM 0.62, MP 0.71, MM 0.77. It does the tasks without reasoning. The FP8 backward fails (no
  autograd formula for the FP8 grouped expert matmul), so no lens can be fit on the FP8 weights. Plan
  (scripts/queues/h200_kolfit_1024.sh): our J++ recipe (as the 28 note), the Jacobians on the FP8 checkpoint
  dequantized to bf16 on load over both GPUs (jpp_cli --dequantize-fp8 --device-map auto, the path the J++ authors use
  for DeepSeek-V4; the dequantization is exact: one expert's weights equal a hand dequantization), with the published
  MoE lens's settings (the 122B's: lrp_mode r+moe, 64 WikiText prompts, 128 tokens, the first 16 positions skipped,
  every block but the last a source (0-48), the final block the target); 8 router clusters; grading, readout weights
  and the held-out evaluation on the FP8 model, the one the knock-outs run (as the 122B's bf16-fit lens is used on its
  FP8 weights). Kolibri's modules are added to a copy of jpp_lens (scripts/lens_fit/patch_jpp_lens_kolibri.py): its
  RMSNorm takes the Qwen2 LN rule (identical forward), its shared expert the gated-MLP rules, its routed experts the
  fused-experts loop (with the stock sentinel slot), and its ungated MoE block the backward-only x4 on the shared expert
  (no gate to detach). Checked on CPU (scripts/lens_fit/test_kolibri_*): on a tiny random Kolibri the patched forward
  equals stock to 4e-7, the block's gradient equals J_experts + 4 J_shared to 6e-8, the rules change a deep Jacobian row
  (cosine 0.86 with stock); on the real first two blocks, dequantized, the forward is within one bf16 ulp and every
  residual norm, shared expert, expert loop and MoE block is patched; jpp_cli runs end to end under transformers 5.20.
  The rows per pass (exact batching of the Jacobian's rows) are the widest of 128, 64, 32 that a 1-prompt smoke fits.
  **Found on the way:** every published neuronpedia "jpp" lens we use (27B and 9B: rlens; 122B: r+moe) is a pooled
  RelP lens (0 clusters, 64 prompts, no expert weighting; their provenance), while our own fits (Muse, Qwen3-32B,
  Gemma, the Olmos) registered the weighted J++. The cross-model table therefore mixes two lens kinds; reported as a
  caveat. Kolibri: the weighted J++ is primary (target kolibri-1, per the 28 note); the same fit's pooled lens is
  secondary (target kolibri-1-pooled, the published kind), run at the same dev-chosen band. Order: fit, the plain-text
  gate (amendment 28), lens check, dev competence and sweep (windows of 7 by 3), choose_band, the test knock-out, the
  pooled lens. Predictions as amendment 28. To free both GPUs for the fit, the 27B's seed-2 run (amendment 29 A) moves
  from GPU 0's overnight queue to GPU 1 after the fit.
- **27 note 2 (~04:10 UTC, during the 9B-Base fit, before any of its lens or knock-out data):** the published 9B
  "J++" is a pooled RelP lens (64 prompts, no expert weighting), not the weighted J++ that h200_q9fit_1024.sh
  registers (32 prompts). The weighted lenses stay the pre-registered primary for base vs instruct (they match each
  other), but the instruct-ourjpp vs published comparison is not like for like in lens kind. Each fit's pooled lens (32
  prompts) is kept (scripts/queues/keep_pooled_1024.sh); a run of the pooled instruct lens would be the like-for-like
  check (secondary, if GPU time allows).

## Amendment 30 (Zach, 2026-10-24 ~05:00 UTC): where the knock-out acts (position-restricted knock-outs, module 1)

- **Why:** every knock-out so far edits every position in the band. The memory-final dependence is consistent with a
  workspace holding recalled content and with a deflationary reading (directions that matter when the answer must be
  recalled, not when it can be copied); where along the prompt the removal must act separates readings (critique pass,
  2026-10-24).
- **Seen when this was written:** module 1 at every position for the 27B (M - P +50), 9B (+42) and Muse; the 9B's dev
  depth profile; no position-restricted run on module 1 (the --positions context / question sets exist since 2026-10-21;
  final and bridge are added now, scripts/ablate_v2.py outside_positions, CPU-checked on real prompts).
- **Procedure (scripts/queues/h200_pos_1024.sh):** the 27B at L32-40 and the 9B at L12-16 (their pre-registered bands),
  jsuite_v1_facts_test_chat, 12 words, paper10 and paper10_rot, cand2, the models' test competence, jsuite_score; one
  run per position set: context (the template prefix and passage, before the question), question (the question, the
  instruction and the template from there on), final (the answer position only), bridge (the bridge's mentions only:
  about 2 positions for read and tracked starts; a recalled start rarely names its bridge, so it is mostly unedited).
  Queued at the end of each GPU's queue.
- **Predictions (M - P, all starts, against the same model's every-position run):** question keeps >= 2/3 of the gap;
  context <= 1/3 (context removal may cost every final alike through hop 1, which M - P cancels); bridge-only (P and T
  starts) M - P < 10; final-only: no directional prediction (reported). The rotated control stays within 10 everywhere.
- **28 note 3 (~10:25 UTC, after Kolibri-1's lens and plain-text gate, before any Kolibri knock-out data):** seen:
  its lens is weak (held-out macro pass@10: J++ 0.484, pooled 0.274, logit lens 0.447; the 9B's J++ 0.62 against
  its logit lens 0.39-0.40), and the gate passes only by its letter: at layers 15-35 the top-10 removal adds 6.36 nats
  to Kolibri's plain-text loss (unedited 4.75) and the rotation adds 1.17, so the rule (untestable if top10 >= +2
  while the rotation stays within 0.3) lets it through because the rotation also hurts. Its J removal breaks plain
  text as much as Gemma's (+6.6, untestable), and Kolibri is fragile to a random edit of the same size. Reading fixed
  now: Kolibri's module 1 result at its dev band counts as a J-specific memory-final dependence only if (a) the
  prompt-final words (P final, all starts) lose <= 20 points under paper10, (b) M - P >= 20, and (c) the rotated and
  the logit-lens controls each give M - P < 10; if (a) fails it is reported as general breakage (not testable this
  way), and if (c) fails as not J-specific. The pooled-lens run is reported beside it, read the same way.

## Amendment 31 (Zach, 2026-10-24 ~15:00 UTC): a non-Qwen dense model with a published J++: OLMo-3 32B base

- **Why:** the J-specific memory-final dependence is so far shown only in Qwen models (27B, 9B, 122B); Kolibri-1 was
  not testable this way (note 3). OLMo-3 32B base (allenai/Olmo-3-1125-32B@c2b61da; Ai2, 2025-11; dense, 64 blocks,
  Apache-2.0) is the one dense non-Qwen model (Gemma excluded by the TA review, Llama by Zach) with a published J++ by the
  J++ authors (neuronpedia/jacobian-lens@e166deb, Ayonrinde & Lindsey; recall@10 50.0%, beside the 27B's 55.2% and the
  122B's 48.4%), fit by the recipe of the published Qwen lenses (rlens, 64 WikiText prompts, target layer 63).
- **Seen when this was written:** our Olmo-3-7B (instruct, our own weak J++: +0.10 over the logit lens) was null on the
  toy suite and both natural sets; no Olmo model has run module 1; the 122B was null on the toy suite but J-specific on
  module 1 (+37); the 9B's base model shows most of the instruct model's dependence (+34 vs +41); nothing on OLMo-3 32B.
- **Procedure (scripts/queues/h200_olmo32_1024.sh):** register olmo-3-32b (the published J++, frozen) and
  olmo-3-32b-jlens (the same repo's plain J-lens, secondary); BOS as the tokenizer defines it (the J++ fit prepended
  it); the plain-text gate (removal_textloss, top10 vs rotated, layers 20-44; amendment 28's rule); module 1 in raw-text
  framing (a base model takes no chat template): competence and the band sweep on jsuite_v1_facts_dev_qa (bridges
  disjoint from test; windows of 9 by 4, as the 27B; choose_band), then the test split jsuite_v1_facts_test_qa at that
  band (paper10 / rot / unembed10 / rot, 12 words, cand2, hop 1 by generation), jsuite_score; the plain J-lens at the
  same band.
- **Reading (as amendment 28 note 3):** a J-specific memory-final dependence if (a) the prompt-final words lose <= 20
  points under paper10, (b) M - P >= 20, and (c) the rotated and logit-lens controls each give M - P < 10; if (a) fails,
  general breakage (not testable this way); if (c) fails, not J-specific; otherwise a null.
- **Predictions:** none directional. If the dependence belongs to pretrained transformers generally, OLMo-3 32B meets
  (a)-(c); if it is a Qwen-family property, M - P < 10. The 7B's nulls (with a weak lens) and the 122B's module-1
  reversal of its toy null pull opposite ways.

## Amendment 32 (Zach, 2026-10-24 16:59 UTC, commit e12eb38): the J-subspace swap at the bridge's mention (a sufficiency test)

- **Why:** amendment 30 put the whole memory-final dependence of a read or tracked bridge on the bridge's own mention
  tokens, and the logit-lens control there removes nothing (27B and 9B, 0 points): the knock-out shows those J-directions
  are necessary. Whether they carry the recalled attribute (sufficiency) is untested; the old write experiments (C2)
  wrote the bridge's name direction at the question and final positions, where tonight's results put nothing.
- **Seen when this was written:** amendments 30's position runs (27B, 9B) and their logit-lens controls; nothing from
  this procedure.
- **Procedure (scripts/jswap.py):** module 1 test split (chat), the read and tracked starts (PP PK PM PA TP TK TM TA),
  the knock-out's eligibility; at the last token of each mention of the bridge X, in every band layer (9B L12-16, 27B
  L32-40), six patches after one clean forward: swap (X's top-10 J-part replaced by a donor D's, D another passage entity
  with a different answer), remove, swap_rot (the same-size change rotated), swap_u (the logit lens's top-10 directions),
  swap_comp (all but the J-part from D), paste (D's whole residual). Answers (the candidate read's pick) classed kept /
  donor / third (a third passage entity's answer, the chance of landing on any entity) / other; transfer index = donor %
  - third %, 95% bootstrap over bridges. An 8-per-word smoke first; the 9B, then the 27B.
- **Predictions:** if the J-part at the mention carries the recalled attribute: for the memory finals PM and TM, swap
  transfer >= 20 with a bootstrap interval above 0, and swap_rot and swap_u transfer < 5; the passage lookups PP, TP, PK,
  TK keep >= 80% (the entity's identity and its stated facts stay). Paste moves the lookups too (identity moves with the
  whole residual). If the swap's transfer is < 5 on PM and TM, the J-part is necessary but not sufficient (it is not
  where the attribute is held, or the attribute needs more than the top-10 span).

## Amendment 33 (Zach, 2026-10-24 17:23 UTC, commit 4464369): the combined suite v2, one dataset (jsuite_v2)

- **Why:** the dataset audit of 2026-10-24 (read-only, module 1 on the 27B): the effect survived every check (no leak;
  difficulty, length, genre, popularity, level do not explain it; 60 of 65 bridges positive), but it found (1) the P
  final asks a different, fictional relation, so M - K (same question and answer) is the clean contrast; (2) M-final
  passages offer only wrong answer words, so part of the M loss may be lure capture (the A final loses half as much);
  (3) the recalled start's MP/MK passages name the bridge and MM/MA never do, and P/K passages name the bridge twice to
  M/A's once; (4) the sample is 65 bridges, 34 answers, 3 relations (effective n ~225 memory-final items), and the second
  rendering seed reuses the same facts; (5) filler is drawn with replacement (786 sentences over 3,120 items). Zach asked
  for one combined dataset, the modules not separated unless needed.
- **Seen when this was written:** everything through amendment 32 and its 9B smoke; nothing on v2.
- **Design (scripts/jsuite_v2.py, tables scripts/jsuite_v2_tables.py):** one set per split (jsuite_v2_dev_chat,
  jsuite_v2_test_chat; framings derived later), field "module" in facts / threehop / numbers. Facts: 8 relations
  (countries -> continent, countries -> language, people -> nationality, cities -> country, companies -> country,
  landmarks -> country, dishes -> country, animals -> class), one scene per bridge, level and start; finals P K M A and N
  (recall with no answer-vocabulary word in the passage); the bridge named equally often in every final of a start (a
  neutral sentence where it has no final-hop fact); test bridges in halves A and B; filler dealt without replacement.
  Three-hop: natural3's chains (jsuite_threehop's drops). Numbers: jsuite_numbers' design, words prefixed "n". Scorer
  scripts/jsuite2_score.py; the knock-out also logs its top token and candidate pick (b4edc90).
- **Procedure:** competence (cand2, hop 1 by generation) on dev and test for the 27B and 9B; the facts words (15) at the
  pre-registered bands (27B L32-40, 9B L12-16), paper10 / rot / unembed10 / rot; the three-hop and numbers words in their
  own runs (per-item eligibility; numbers with --dict-digits), from the same set.
- **Predictions (facts, all starts, per model):** M - K >= 30 with the logit-lens and rotated controls < 10 (the
  dependence on new relations and 2-3x the bridges); M - P >= 20; each test half's M - K within 15 of the other (an
  independent replication on disjoint facts); M - N two-sided: >= 10 would say lures inflate the M loss, within 10 that
  they do not; per relation, M - K > 0 in at least 6 of 8.

## Amendment 34 (Zach, 2026-10-24 20:47 UTC, commit bea4877): the J-swap and readout on the 122B, and on v2

- **Seen when this was written:** amendment 32's J-swaps and readouts on the 27B, 9B (pre-registered) and on OLMo-3 32B
  and Muse (diagnostics: sufficient, not necessary); the 9B's v2 knock-out; nothing on these runs.
- **A. The 122B (jsuite_v1_facts_test_chat, L39-45, FP8):** scripts/bridge_readout.py and scripts/jswap.py as
  amendment 32. Predictions as amendment 32 (PM and TM swap transfer >= 20 with the interval above 0; rotated and
  logit-lens swaps < 5; lookups PP TP PK TK kept >= 80%); and necessity as its knock-out (the 122B lost +37 M - P on
  module 1), so "remove" at the mention alone is reported, no prediction.
- **B. v2 (jsuite_v2_test_chat):** the same two scripts adapted to v2's tables (scripts/jsuite_v2_tables.py) for the
  27B (L32-40) and 9B (L12-16); OLMo-3 32B's J-swap on jsuite_v2_test_qa at L12-20. Predictions per model, all starts:
  as amendment 32, plus the swap's transfer on the memory finals > 0 in at least 6 of the 8 relations; for OLMo the
  same sufficiency predictions (its knock-out was null; sufficiency without necessity is what its v1 diagnostic showed).

## Amendment 35 (Zach, 2026-10-24 20:53 UTC, commit 42ae4e0): v1 retired; jsuite_v2_1 is the dataset of record for new work

- **Decision (Zach):** the combined suite v1 (jsuite_v1_*) is retired for new runs; its files stay frozen because every
  result through amendment 34 references them. v1's one condition v2 lacked, a recalled start that never names the
  bridge (v1's MM / MA; the basis of amendment 30's "a recalled bridge's dependence sits in the question span"), is
  added to v2 as start R: scripts/jsuite_v2_1.py copies every v2 item unchanged (same ids: runs on v2 stay valid) and
  adds, for each v2 recalled-start memory item (MM, MA, MN), the same scene with its one neutral bridge sentence deleted
  (words RM, RA, RN; test 1,074 items, dev 1,026; scorer: RF - MF per final, R kept out of the start=all cells).
- **Predictions (when run):** all-position knock-out: RM - MM within 10 (two-sided; the dependence does not hinge on a
  passing mention); position-restricted knock-out (question only), if run: RM keeps >= 2/3 of its all-position loss
  (as v1's recalled bridge); MM two-sided (a passing mention may move part of the dependence to the mention).
- **Note 1 (Zach, 2026-10-24 ~21:20 UTC, before any R item ran):** v2.1 is v2 plus R with v2's items unchanged, so the
  other models run only the R items: scripts/natural_v1.py competence --words RM RA RN (candidate pools from the whole
  set), the knock-out on RM RA RN at the model's v2 band with its v2 conditions, and scripts/jsuite2_score.py --with,
  which scores the R run with the model's v2 run (it asserts model, lens, band, conditions, read and positions match and
  that the items are disjoint; on the 9B's v2 run split in two by start it reproduces the original scores exactly).
  Knock-out, eligibility and competence code is unchanged since the v2 runs (5c88cbc). Queued
  (scripts/queues/h200_v21r_1024.sh, after the GPU1 chain): the 27B (L32-40), the 122B (L39-45), the 9B base (raw text,
  L12-16). Same prediction per model: RM - MM within 10 points. Not run on Muse or OLMo-3 32B: R changes only the
  knock-out, and neither model's knock-out has shown a gap (Muse is added if its v2 run shows one). The 9B's full v2.1
  run stays queued; it re-runs every v2 item, so it also measures run-to-run agreement with the 9B's v2 run (reported,
  no prediction).

## Amendment 36 (Zach, 2026-10-24 ~23:25 UTC, before the run): where the 122B's knock-out acts (position-restricted, v2)

- **Seen when this was written:** the 122B's v1 knock-out (M - P +37, all positions) and its J-swap (amendment 34 A):
  removing the top-10 J-part at the last token of each bridge mention alone keeps PM 87.6% / TM 91.5% right (~10
  points lost; the 27B and 9B lose ~35-40 there), while swapping it moves the answer (+44 / +40); the 122B's v2
  competence; NOT its v2 all-position knock-out (running, L39-45), the reference here.
- **Procedure (scripts/queues/h200_posv2_1024.sh, after the GPU1 chain):** ablate_v2 --positions on the 122B at L39-45,
  jsuite_v2_test_chat, the 15 facts words with the v2 knock-out's eligibility (same items as the reference),
  paper10 and paper10_rot, cand2, scored by jsuite2_score; modes in order question (the question sentence on:
  question, instruction, template, answer position), context (everything before it: the passage), bridge (only the
  bridge's mention tokens; most bridges are one token, so this nearly repeats the J-swap's removal, on v2).
- **Measure:** per start, the mode's paper10 M - K as a share of the reference's (the all-position v2 run).
- **Predictions:** bridge, read and tracked starts (P, T): < 1/3 of the reference (as the J-swap's removal). Recalled
  start (M), question: >= 2/3 (as amendment 30 on the 27B and 9B). Read and tracked starts, question vs context:
  two-sided, readings fixed now: question >= 2/3 = the 122B re-retrieves the attribute from the question (unlike the
  27B and 9B); context >= 2/3 = it sits in the passage beyond the mention's tokens; neither >= 2/3 = spread over both.
  Rotated control < 10 in every mode. If the reference's M - K is < 15, the shares are not interpreted.
- **Note 1 (Zach, 2026-10-25 ~02:30 UTC, before these runs; seen: the 122B's question-only result (M - K share of its
  all-token v2 run: read 46%, tracked 69%, recalled 69%), nothing on the runs below):** for an even comparison, the same
  position-restricted knock-outs on v2 for the 27B (L32-40) and the 9B (L12-16): question, context, bridge, paper10 and
  paper10_rot, jsuite_v2_test_chat, the 15 facts words, each model's v2 test competence, jsuite2_score (M - K share of the
  model's own all-token v2 run); and the 122B's question-only with the logit-lens control (unembed10 / rot; its
  all-token logit-lens control was +12). Predictions (27B, 9B; as amendment 30 found on v1): read and tracked starts,
  bridge >= 2/3 and question < 1/3; recalled start, two-sided (v2 names the bridge once in passing, which the 27B's R
  result showed it partly uses): question >= 2/3 reads as v1. 122B logit-lens question-only: reported, no prediction.
  Known confound, not fixed by these runs: the bands sit at different relative depths (27B 50-62%, 9B 38-50%, 122B
  81-94%); a 122B-vs-smaller-Qwen difference in where the dependence sits may be depth, not model.

## Amendment 37 (Zach, 2026-10-25 02:35 UTC, commit 1dea5d7, before any run below): the overnight plan of day 6

- **Seen when this was written:** everything through amendment 36 note 1, including the 122B's question-only result at
  L39-45 (read 46%, tracked 69%, recalled 69% of its all-token M - K); not its context or bridge runs (running).
- **A. Depth-matched bands (the confound named in amendment 36 note 1).** Each model at the other's relative depth,
  with its own band's layer count, by rule: the 122B at L24-30 (the 27B's L32-40 = 50-62% of 64 layers, times 48), the
  27B at L52-60 (the 122B's L39-45 = 81-94% of 48, times 64). jsuite_v2_test_chat, the 15 facts words, each model's v2
  test competence: the all-token knock-out (paper10 / rot / unembed10 / rot) and the question-only and bridge-only
  knock-outs (paper10 / rot); scripts/queues/h200_depth_1025.sh (run names carry the band). Measure: per start, the
  mode's M - K as a share of the same band's all-token M - K; not interpreted if that is < 15. Readings, two-sided and
  fixed now. 122B at L24-30, read and tracked starts: bridge >= 2/3 and question < 1/3 = at the 27B's depth the 122B
  localizes like the 27B (the L39-45 difference is depth); question >= 2/3 = the 122B differs at matched depth. 27B
  at L52-60, read and tracked: question >= 2/3 = late layers put the dependence in the question in the 27B too (depth);
  bridge >= 2/3 and question < 1/3 = the 27B localizes at the mention even late (a model difference). If the 122B's
  all-token M - K at L24-30 is < 15, its dependence is late-only and only the 27B side is read.
- **B. v2 modules 2 and 3 (amendment 33's procedure, not yet run).** The 27B (L32-40) and the 9B (L12-16) on
  jsuite_v2_test_chat with their v2 test competence: three-hop (8 words, per-item eligibility) and numbers (12 words,
  per-item eligibility, --dict-digits), paper10 / rot / unembed10 / rot, cand2, jsuite2_score; a one-item-per-word smoke
  first (scripts/queues/h200_v2mod_1025.sh). Predictions as amendments 24 and 25. Numbers: KR and AR within 10 of PR,
  MR >= PR + 15; SM - SL >= 20 for each start; KL and AL within 10 of PL. Three-hop, read as knock-out minus rotation:
  PPM, MPM, MMP, PMM and MMM each lose >= 15 more than PPP; MPP and PMP within 10 of PPP.
- **C. Clean-checkout rerun of the v2 headline (CLAUDE.md), the 9B:** competence and the facts knock-out at L12-16 from
  a fresh checkout of HEAD (/workspace/clean_bridge moved to HEAD; scripts/queues/h200_clean_v2_1025.sh), compared row by
  row with the runs of record. Prediction: >= 99% of rows agree and M - K within 1 point.
- **D. OLMo-3 32B on v2 (raw text, L12-20), the facts knock-out as the others (h200_depth_1025.sh all with framing qa; the run name carries its band):** prediction null as
  on v1 (M - K < 15), testable if the K final loses <= 20.
- **Order (research priority per GPU):** GPU0 A (122B), B (9B), C, D; GPU1 A (27B), B (27B).
- **Note 1 (Zach, 2026-10-25 02:42 UTC, commit 572e818, before any run below; Zach asked whether we re-run data that does not need it):**
  (1) the 9B's full v2.1 run (amendment 35 note 1) is replaced by its R items only, as on the other models: C re-runs
  the 9B's v2 items from a clean checkout, so the full run's re-run of them was a second copy; its question-only run
  was also a duplicate of the 9B's v2 question-only run (amendment 36 note 1) and is replaced by a question-only run on
  the R items (scripts/queues/h200_rpos_1025.sh), scored with that v2 run (amendment 35's position prediction: RM keeps
  >= 2/3 of its all-token loss). (2) B is not new facts: v2's three-hop and numbers modules share their questions with
  v1's (928 of 1,007 three-hop and 412 of 703 numbers v2 items have a question that also appears in
  jsuite_v1_threehop_chat / jsuite_v1_numbers_chat; no passage-question pair is identical), so B is a re-rendering replication of amendments 24 and
  25 on new passages; moved to the end of each GPU's queue. (3) GPU0's chains are merged into one in the order A (122B
  L24-30), the 9B's v2 position runs (amendment 36 note 1), the 9B's R items and their question-only run, Muse's R
  items (amendment 35 note 1), C, D, B (9B).

## Amendment 38 (Zach, 2026-10-25 04:06 UTC, commit a2f27cd, before any run below): what the J-part at the mention carries; renderings

- **Seen when this was written:** everything through amendment 37 note 1, the 122B's L39-45 position runs and its
  L24-30 all-token run (M - K +4: late-only, so amendment 37 A's 122B side is not read), the 27B's v2 question-only
  run; a smoke of A on the 9B (n 2 per word; mechanics only, its numbers not used).
- **A. The answer-only swap (scripts/jswap.py --conds, scripts/queues/h200_ans_1025.sh).** jswap's swap never takes a
  protected direction (the clean top-10 at the answer position, which usually holds X's own answer), so what it moves
  is the J-part minus at least X's answer token. New conditions at the same positions and band: swap_ans (only the span
  of X's and D's answers' unit J-lens vectors, first tokens in both cases, swapped), swap_ans_u (the same with their
  logit-lens directions), swap_ans_rot (the same-size change in a fixed random direction), swap_noans (the top-10 J-part
  with both answers' tokens also protected). The 27B at L32-40 and the 9B at L12-16 on jsuite_v2_test_chat, read and
  tracked starts, the v2 knock-out's eligibility. Measure: transfer (donor - third) on the memory finals pooled (PM PA
  PN TM TA TN), per condition, beside swap's. Readings, two-sided, fixed now: swap_ans >= 2/3 of swap and swap_noans
  <= 1/3 = the J-part at the mention is the pre-fetched answer token; swap_noans >= 2/3 of swap = it carries the
  attribute through directions other than the answer's own (a bundle of related concepts), the answer token not needed;
  otherwise both. Predictions: swap_ans_u and swap_ans_rot transfer < 5; lookups (PP PK TP TK) kept >= 80% under
  swap_ans and swap_noans.
- **B. Two more renderings of v2's facts (scripts/jsuite_v2.py --split-from jsuite_v2; jsuite_v2r2 seed 2602,
  jsuite_v2r3 seed 2603):** v2's exact facts, dev / test split and test halves, new passages, filler, wordings and
  orders (0 of 5,370 test passages shared with v2 or with each other; the audit: equal bridge mentions, complete scenes).
  The 27B (L32-40) and the 9B (L12-16): competence on the 15 facts words, the facts knock-out (paper10 / rot /
  unembed10 / rot), jsuite2_score (scripts/queues/h200_rend_1025.sh). Predictions per model and rendering: M - K within
  10 of the model's v2 value (27B +51, 9B +43); rotated and logit-lens < 10; halves within 15.
- **Order:** GPU1 after its night chain: A 27B, B 27B r2, r3; GPU0 after its chain: A 9B, B 9B r2, r3.

## Amendment 39 (Zach, 2026-10-25 05:02 UTC, commit 4d21b30, before any non-Qwen test run): DeepSeek-V4-Flash and Ministral 3 14B on v2

- **Why (Zach):** every dependence claim so far is Qwen-only (OLMo-3 32B null; Muse mostly shared with the logit lens;
  Gemma 4, gpt-oss, Kolibri untestable). Two more families: Zach chose DeepSeek-V4-Flash (recent, Qwen3.6-27B-class
  on MMLU-Pro / GPQA; MoE) and Ministral 3 14B (dense; weaker, ~Qwen 9B or below); Instruct first, Base later only if
  Instruct shows the split; DeepSeek with J++ only.
- **Seen when this was written:** everything through amendment 38; the 122B's L24-30 runs; a Ministral smoke
  (competence, first 120 items, countries: memory and K finals 8/8, PP 4/8, TP 2/8); DeepSeek's chat format (below);
  the two-GPU split check (9B split over two GPUs vs one GPU, same settings: 270 of 270 rows identical, logp diff 0).
- **Models.** DeepSeek-V4-Flash @60d8d70 (MoE, 43 blocks, FP8, 160 GB): two GPUs (model.split_gpus, blocks 0-21 on
  cuda:0 with embeddings, final norm and lm_head, 22-42 on cuda:1, hooks bridged to cuda:0); chat with thinking off by
  pins.DEEPSEEK_V4_CHAT_TEMPLATE, equal to deepseek-ai's encoding_dsv4.encode_messages(thinking_mode="chat") on system /
  user / assistant turns (read from its source and its chat-mode test); published J++ (koayon/jpp-lenses@6c96867 via
  neuronpedia/jacobian-lens@e166deb; 64 prompts, source layers 0-41; sha256 e7dc42a6...). Ministral 3 14B Instruct
  (BF16 repo @3cea74c; dense, 40 blocks): tokenizer with fix_mistral_regex; pins.MISTRAL_CHAT_TEMPLATE (renders exactly
  as the official template given a system prompt; ours passes none, the official default names Paris and the date);
  our J++: scripts/lens_fit/fit_jpp.sh (safety-research/jpp_lens@93f02cd recipe, patched: Ministral3MLP and
  Ministral3RMSNorm registered, byte-identical to Mistral's, and Mistral tokenizers loaded with fix_mistral_regex), 32
  WikiText prompts, router 64, source layers 0-38, target the final block; its sha256 goes into pins when the fit ends.
- **Procedure (scripts/queues/h200_nq_1025.sh, OLMo's amendment 31 procedure on v2):** gate (removal_textloss, top10 vs
  rotated, the lens's layers at 31-69% depth; untestable if top10 adds >= 2 nats with the rotation <= 0.3); dev
  (competence on jsuite_v2_dev_chat's facts words; band sweep, windows round(9/64 n) wide sliding by round(4/64 n) inside
  the lens's layers, PP PM MP MM, paper10 and rot, n 100 per word; choose_band, as every model's band); test
  (competence on jsuite_v2_test_chat's facts words; the knock-out at the dev band, paper10 / rot / unembed10 / rot, the
  15 facts words; jsuite2_score); swap (jswap's six conditions, bridge_readout and jswap_by_relation at the dev band).
- **Predictions, per model.** Representation (as in all five families so far): at the dev band the J-lens reads the
  attribute at the mention above the logit lens, and the J-swap moves PM and TM (transfer >= 20, intervals above 0;
  rotated and logit-lens swaps < 5; lookups PP PK TP TK kept >= 80%). Dependence, two-sided, readings fixed now: M - K
  >= 30 with rotated and logit-lens < 10 = Qwen-like; M - K >= 30 with logit-lens >= 10 = Muse-like (partly shared);
  M - K < 15 = OLMo-like (no dependence); between 15 and 30 = weak, reported as such. A gate failure is reported and no
  knock-out claim is made for that model. Positions and R items follow only if M - K >= 15.
- **Order:** GPU1 after its rerun chain: Ministral's fit, gate, dev; then both GPUs: DeepSeek gate, dev, test, swap;
  then Ministral test, swap. Disk (Zach's approval): Muse's cache is deleted after its R rerun to fit DeepSeek's
  download, OLMo's after its v2 knock-out.

## Amendment 40 (Zach, 2026-10-25 05:22 UTC, before any Nemotron run): NVIDIA Nemotron 3.5 Lightning on v2, end of the queue

- **Why (Zach):** "Queue nemotron 3.5 bolt and lightning at the end of our queue." A third non-Qwen family, and the
  first hybrid with Mamba-2 state-space layers: Lightning 30B-A3B (2026-08; MoE, 52 blocks, each one Mamba-2,
  attention or MoE mixer; NVIDIA reports it at or above Qwen3.6-27B on several reasoning benchmarks, unverified here).
- **Seen when this was written:** everything through amendment 39; no Nemotron output of any kind (no smoke yet).
- **Model.** nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16 @a9904d2, transformers' native NemotronH (no remote
  code; the Mamba scan on transformers' torch path, mamba_ssm not installed); one GPU. Its tokenizer adds no BOS
  (add_bos_token false) and its chat template writes none: bos False. Thinking off by the template's enable_thinking
  (chat.chat_text). Final norm norm_f (a plain weight; model.final_norm).
- **Lens.** None is published, and the J++ fitter has no Mamba rules, so our plain J-lens: scripts/lens_fit/fit_jlens.py
  (Anthropic's jlens, amendment 28's recipe: 500 WikiText prompts, 128 tokens, first 16 positions skipped, every block
  below the last a source, the final block the target), --no-bos as the model reads text; its sha256 goes into pins when
  the fit ends. **Lens-kind caveat, fixed now:** the Qwen and DeepSeek numbers use J++, Ministral our J++, Lightning a
  plain J-lens; a gap between them is not read as a model difference unless a same-lens-kind comparison backs it.
- **Smoke, stop rule fixed now:** scripts/new_model_smoke.py (block count, unembed of the last block vs the model's
  logits, WikiText NLL, a chat rendering and its greedy answer) and competence on the first 120 dev items. The chain
  stops if the unembed's top-1 differs or plain-text NLL is >= 4 nats.
- **Procedure and predictions:** amendment 39's, unchanged (scripts/queues/h200_nq40_1025.sh is h200_nq_1025.sh with
  its --why strings marked amendment 40): gate, dev band by choose_band, test (paper10 / rot / unembed10 / rot, the 15
  facts words, jsuite2_score), swap (jswap, bridge_readout, jswap_by_relation). Readings: M - K >= 30 with rotated and
  logit-lens < 10 = Qwen-like; >= 30 with logit-lens >= 10 = Muse-like; < 15 = OLMo-like; 15-30 = weak. A gate failure
  is reported and no knock-out claim is made.
- **Order and disk:** scripts/queues/h200_nem_1025.sh on GPU 1: download once DeepSeek's download and OLMo's cache
  drop are done (66 GB; stop if under 80 GB free); smoke, fit and runs once DeepSeek's chain has finished (Ministral's
  test and swap then hold GPU 0).
- **Bolt (74B-A9B, 2026-10):** not queued by this amendment. Its checkpoint is a multimodal wrapper whose language
  model has heterogeneous MoE blocks and ships NVIDIA's own model code, and its 150 GB do not fit the disk next to
  DeepSeek's cache. It gets its own note here, with the loading path and the disk plan, before any Bolt run.

**Amendment 40, note 1 (Zach, 2026-10-25 05:58 UTC, before any Bolt run): Nemotron 3.5 Bolt 74B-A9B, last in the queue.**
Zach approved both open points ("Yes go ahead with that"): drop DeepSeek's cache after its runs, and run NVIDIA's own model
code for Bolt after reading it.
- **Model.** nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16 @e09a4ce, a multimodal checkpoint. Only its language model
  is loaded: NemotronHPuzzleForCausalLM from the repo's own code (modeling_nemotron_h*.py and configuration_nemotron_h*.py,
  read before use: model code only, its one side effect a checkpoint-key renaming backbone. -> model.). It has 88 blocks
  (40 Mamba-2, 40 MoE with 240-496 experts by layer, 8 attention) and hidden size 4096. The vision tower is left
  unloaded, and the run uses two GPUs (blocks 0-43 / 44-87). That code imports mamba_ssm's Triton gated RMSNorm
  unconditionally; this env has no mamba_ssm (not installed: the env is shared by the running chains). So
  model._gated_rmsnorm_shim registers mamba_ssm's pure-torch reference of that one function (equal to transformers'
  Zamba2RMSNormGated in fp32: max diff 0.0), and the Mamba scan takes the code's own torch path, as Lightning's does.
  CPU check without weights (scripts/bolt_load_check.py, results/checks/nem35b_load_check.txt): all 28,331 tensors of
  the class map to checkpoint keys, and the 394 unmatched checkpoint keys are all the vision tower's. Tokenizer:
  trust_remote_code False (TokenizersBackend), no BOS, thinking off: `<|im_start|>system\n<|im_end|>\n<|im_start|>user\n...
  <|im_end|>\n<|im_start|>assistant\n<think></think>Answer:`.
- **Lens, smoke, procedure, readings:** as Lightning's (amendment 40): our plain J-lens (fit_jlens --harness, 500
  prompts, --no-bos; dim_batch 64, 32 on out-of-memory), the same smoke stop rule, then h200_nq40_1025.sh gate, dev,
  test, swap on GPUs 0,1. The lens-kind caveat applies.
- **Order and disk (scripts/queues/h200_bolt_1025.sh):** DeepSeek's cache is dropped once its chain's DeepSeek part
  ends with 0 failures, else kept and the chain stops. Then the download (150 GB; stop if under 160 GB free). Runs start
  once DeepSeek's chain (Ministral's test and swap) and Lightning's chain have exited.
- **Fix to amendment 40 (no run affected):** the Lightning and Bolt pins placeholders now differ from Ministral's, which
  its fit script requires to be unique. The Lightning chain (h200nemL-1025-0522, still waiting before its download) was
  stopped and relaunched with the fix.

**Amendment 39, note 1 (Zach, 2026-10-25 08:37 UTC; no DeepSeek or Ministral knock-out, swap or band data seen):
two failures at start, fixed; new order.** (1) Ministral's J++ fit stopped before fitting: jpp_lens's rule patcher met
Mistral3RMSNorm (the multimodal projector's norm, not on the text path) with no rule registered. It is now registered
with _qwen2_rmsnorm_lrp_forward (its forward is line-for-line Qwen2RMSNorm's). The patcher was checked on an empty
Ministral on the CPU: 82 norms patched (2 per block, the final norm, the projector's), no error.
scripts/lens_fit/jpp_lens_ministral3.patch is regenerated. Its router (64 prompts, done before the failure) is reused.
The chain (h200nqA) was stopped, and its dev competence, cut off a minute in, was moved out of results. (2) DeepSeek's
chain (h200nqDS) failed at load in every step: transformers' DeepseekV4 supports no sdpa (per-head attention sinks).
pins sets attn eager for it, and pins.model_pin now records each target's attn (it recorded "sdpa" for every target,
gpt-oss's eager runs included). Its two empty result directories (manifests only) were moved out. (3) Order, both GPUs
being free: DeepSeek first (scripts/queues/h200_ds2_1025.sh: new_model_smoke with amendment 40's stop rule, then gate,
dev, test, swap). Then Ministral's whole procedure on GPU 0 (fit, gate, dev, test, swap; job h200min2), beside
Lightning on GPU 1, then Bolt. Lightning's chain had been released by DeepSeek's failure, and was stopped before its
smoke wrote anything. Bolt's guard held (DeepSeek's cache kept). Ministral's test competence
(min14_jsuite_v2_test_chat_competence_cand2_v1) ran early, at 06:31, for Zach's keep-or-replace question; its test
step reuses it. Procedures and readings unchanged.

**Amendment 39, note 2 (Zach, 2026-10-25 08:46 UTC; no DeepSeek knock-out, swap or band data seen): DeepSeek-V4's
residual streams.** The second chain's smoke stopped it as designed. The model is sound (WikiText NLL 1.79; "Paris";
greedy chat answer "Canberra"), but model.unembed(the last block's output) did not reproduce its logits (max diff 31.5,
top-1 differs). DeepSeek-V4's blocks carry 4 parallel residual streams [B, S, 4, D] (manifold hyper-connections),
collapsed by a learned head (hc_head) only before the final norm, and the harness had been reading the first stream.
Fix (model._streamed, inside model._forward_hooks, so every script's hooks): a hook sees the lens's residual, the mean
over the streams. That is the published DeepSeek-V4 J++'s convention (jpp_lens residual_streams.py: lens residual =
stream mean at every source layer and at the target; its Jacobian is for a uniform shift of the streams). What a hook
returns is lifted back by adding its change to the mean to every stream, so the mean moves exactly as edited and a
no-op edit leaves the streams bit-identical (unit check: identity edit equal; +1 edit moves the mean and each stream by
1; single-stream outputs untouched). This is the lift jpp_lens names for interventions but does not implement; the
knock-out and the swap act on the stream mean, through all 4 streams equally. new_model_smoke now compares the model's
own collapse (hc_head on the last block's streams) with its logits, reports the stream mean's top-1 beside it, and
checks that a no-op edit leaves the logits bit-identical. The stop rule adds: no-op diff must be 0. DeepSeek's split
moves to blocks 0-13 on cuda:0 (was 0-21) so it fits beside Ministral's fit on GPU 0; the two-GPU check on the 9B
(270 of 270 rows identical) is what makes the split point immaterial. Chain: scripts/queues/h200_ds3_1025.sh (waits
for 60 GB free on GPU 0 and 120 GB on GPU 1), then amendment 39's procedure unchanged. Lightning (relaunched as
h200nemL4) and Bolt (h200bolt3) wait on it. The second smoke's check file is kept in scratch (killed_1025).

**Amendment 39, note 3 (Zach, 2026-10-25 09:19 UTC; no Ministral lens or knock-out data seen): Ministral's fit ran out of
disk.** The relaunched fit (h200min2) fitted all 32 prompts (about 65 s each), then failed writing its final 14 GB
checkpoint: the disk was full (44 GB free beside DeepSeek's and Lightning's caches, and the fit's artifacts need more).
The chain's "No LN-rule patcher" line was the first attempt's, left in the same log. Fix without deleting anything: the
fit's working directory /workspace/ext/ministral-3-14b_fit is a symlink to /dev/shm (RAM, 125 GB free). Its router
(64 prompts) is kept; the exported lens goes to the repo cache on disk as before. If the box restarts mid-fit, the fit
reruns. h200min3 runs h200_minfit_1025.sh 0, then h200_nq_1025.sh 0 gate dev test swap, once h200min2 has exited.
h200min2's dev competence, run after its failed fit, is reused. Procedure and readings unchanged.

**Amendment 40, note 2 (Zach, 2026-10-25 15:49 UTC; no Lightning lens or knock-out data seen):** Lightning's smoke passed
(own logits reproduced exactly, "Paris", WikiText NLL 2.74 without BOS vs 2.81 with, greedy "Canberra"), and so did its
competence smoke (first 120 dev items: K and memory finals 1.00, TP 0.12, MP 0.62). Its J-lens fit then ran out of
GPU memory at once: with dim_batch 64, transformers' torch Mamba scan (mamba_ssm absent) asks for a 32 GB tensor. The
fit now runs with dim_batch 32, or 16 on out-of-memory, as Bolt's does. dim_batch is how many Jacobian rows one backward
pass takes, so it changes speed, not the estimate. The chain is relaunched as h200nemL5; Bolt's chain (paused) will
wait on it.

## Amendment 41 (Zach, 2026-10-25 16:26 UTC, before any run below): follow-ups for Ministral and DeepSeek

- **Why (Zach: "Queue what you think needs it", day 7 of 12):** both new families' dev bands came out late (Ministral
  L32-37, 80-93% depth; DeepSeek L36-41, 84-95%), and at late depth the bridge's mention no longer feeds the answer (the
  27B's L52-60 mention-only run: 1-14%; both new swaps, paste included: 0). Ministral's M - K was +23 (weak,
  J-specific). DeepSeek's band broke lookups as much as recall (K lost 74, M 75), so its +2 says nothing about the split.
- **Seen when this was written:** everything through amendment 40 note 2 and the runs logged in EXPERIMENTS.md up to
  5c92ebd: Ministral's and DeepSeek's full amendment-39 results, both dev sweeps, both readouts.
- **The lookup-sparing band rule (scripts/band_rule2.py, on dev sweeps only):** among windows where the rotation keeps
  every word >= 90% (choose_band's rule), also require J++ removal to keep both lookups (PP, MP) >= 80%. Pick the most
  broken memory finals (mean of PM and MM kept). Its picks: DeepSeek L27-32 (lookups >= 83%, memory mean 73%);
  Ministral L32-37 (unchanged); the 27B's v1 dev sweep L32-40 (its band of record); the 9B's v1 dev sweep L24-28 (not
  its L12-16). It was written after DeepSeek's band failed, so DeepSeek's L27-32 result is SECONDARY: amendment 39's
  result (uninformative) stays the primary record.
- **Ministral (scripts/queues/h200_min41_1025.sh, GPU 0; amendment 39 allows positions and R items at M - K >= 15):**
  question-only and bridge-mention-only knock-outs at L32-37 (paper10 / rot). v2.1's R items at L32-37, scored with
  its v2 run, and r_matched. The swap at mid depth L20-25, with jswap_by_relation. The mid depth is the 27B's L32-40
  relative depth (50-62%), times its 40 blocks.
- **DeepSeek (scripts/queues/h200_ds41_1025.sh, GPUs 0,1):** the test knock-out at L27-32 (paper10 / rot / unembed10
  / rot). Only if that M - K >= 15: question-only and bridge-mention-only at L27-32. The mid-depth swap at L22-27
  (50-62% of 43 blocks). Lightning's J-lens fit is stopped right after its first checkpoint (25 prompts; jlens resumes
  from it) and relaunched after (h200nemL6). Bolt's chain (h200bolt4) drops DeepSeek's cache only after this chain ends
  with 0 failures.
- **Readings, fixed now.** Knock-outs: amendment 39's M - K classes. Positions: the mode's M - K as a share of the
  same band's all-token M - K, not read if that is < 15. Question >= 2/3 = late-band dependence sits in the question,
  as in the 27B at L52-60. Bridge >= 2/3 = at the mention. R items: amendment 35's RM - MM within 10. Mid-depth swaps:
  transfer on PM and TM >= 20 with the rotated and logit-lens swaps < 5 and lookups kept >= 80% = the J-part at the
  mention carries the attribute in this family too. The paste ceiling is reported beside it, and a ceiling < 20 makes
  the swap uninformative.

## Amendment 42 (Zach, 2026-10-25 16:42 UTC, before any run below): depth profiles replace single-band choice; hub kernels for Nemotron

- **Why (Zach, day 7: "Are we not being careful or precise enough with our layer selection? ... I just want to do the
  best research sprint"):** one argmax band per model, chosen on memory finals and the rotation only, gave two
  uninformative non-Qwen tests. Both new families' picks were late, and DeepSeek's broke lookups too. Dev sweeps already
  show the effect is a function of depth. 27B: lookup-minus-memory gap +40-48 at 44-69% depth. 9B: +32-42 there, +56 at
  75-88%. Ministral: ~0 to 68%, then +12-20. DeepSeek: +2-13 to 81%, +30 at 77-88%, everything breaking at 84-95%.
  The old sweeps lack K finals, so they give M - P, not the primary M - K, and they have no logit-lens control per band.
- **Seen when this was written:** everything through amendment 41, Ministral's L32-37 question-only (M - K +24 of +23)
  and bridge-only (0) runs, the four dev sweeps' gaps above, the Mamba benchmark and validation below.
- **Depth profile (scripts/queues/h200_profile_1025.sh; scripts/profile_score.py):** on jsuite_v2_dev_chat, every
  window (amendment 39's widths and strides), words PP PK PM MP MK MM, n 40 per word, paper10 / paper10_rot /
  unembed10, cand2. Per band: M - K (memory finals PM MM vs stated true finals PK MK), M - P, bootstrap over bridges.
  Test band = scripts/profile_pick.py: among bands where the rotation costs <= 10 points on every final, the largest
  J-specific M - K (J++ M - K minus logit-lens M - K). Profiles are descriptive (dev, no prediction). The test runs at
  the pick are read by amendment 39's classes, and are SECONDARY to amendment 39's pre-registered results, which stand.
- **Runs.** DeepSeek (h200ds42, GPUs 0,1): profile; test knock-out at the pick unless it is L36-41; the mid-depth swap
  at L22-27 (replaces amendment 41's DeepSeek runs, which were stopped before starting). GPU 0 (h200qprof, after
  amendment 41's Ministral runs): Ministral's, the 9B's and the 27B's profiles, so all models get the same curve.
  Lightning (h200nemL6, after DeepSeek): smoke, fit, gate, profile, test and swap at the pick, mid-depth swap L26-32.
- **Nemotron's Mamba kernels:** transformers' torch Mamba path made Lightning's J-lens fit about 7.5 min per prompt
  (forward+backward, batch 8 x 128: 1.37 s); 500 prompts would take ~60 h. The HF-hub kernels (set_use_kernels:
  kernels-community/mamba-ssm and the hub's activation / norm / rotary kernels, prebuilt, nothing compiled) are 12.4x
  (forward) and 9.2x (forward+backward) faster. On 47 WikiText rows (128 tokens): NLL 2.4642 vs 2.4634, per-token
  |diff| mean 0.05, top-1 agreement 97.6%. pins sets use_kernels for Lightning; model_pin records it; fit_jlens
  --use-kernels; its jlens log now shows each prompt's time and the running mean's relative change.
- **Lightning's lens: 200 prompts, not 500 (a deviation from amendment 28's recipe, stated).** About 3 h with the
  kernels. Convergence is read from jlens's per-prompt relative change of the running mean; we report its value at the
  last prompts and the lens's readout check. Bolt stays paused: its code calls mamba_ssm directly and would need the
  hub kernels wired in; decided after Lightning's profile.

## Amendment 43 (Zach, 2026-10-25 16:59 UTC, before any run below): removal-size curves, DeepSeek's question-only run, renderings overnight

- **Why (Zach: "Yes queue what you think is worth it"):** the plan's "Strong" outcome needs a non-Qwen family at C1
  >= 30, J-specific. Top-10 may be too blunt for DeepSeek (its gate +1.68 nats; its L36-41 broke everything) and too
  weak for Ministral (+23). The Qwens already have removal-size curves (full2_dose_v1).
- **Dose (scripts/queues/h200_dose_1025.sh; descriptive, dev):** at each new model's profile pick: top1 / top3 /
  paper10 / top30, each with its rotation, PP PK PM MP MK MM, n 40, M - K per condition (profile_score.py). DeepSeek
  (h200dsdose, after h200ds42), Ministral (h200mindose, GPU 0, after its profile), Lightning (in its chain, after its
  profile).
- **DeepSeek question-only:** only if its test M - K at the pick is >= 15, the question-only knock-out there (paper10 /
  rot). Reading as amendment 37 A: question >= 2/3 = question-located, as the 27B at L52-60.
- **Renderings (amendment 38 B, pre-registered on 25 Oct 04:06 UTC, unchanged):** GPU 0 overnight (h200qrend, after
  the profiles): the 9B (L12-16) and the 27B (L32-40) on jsuite_v2r2 and jsuite_v2r3. Prediction: M - K within 10 of
  v2 (27B +51, 9B +43); rotated and logit lens < 10; halves within 15.
- **Correction to earlier readings:** ablate_v2's "question" mode removes from the question on, so it includes the
  instruction and the "Answer:" prefill. The ~half of a named-once recalled bridge's dependence that neither the
  passage-only nor the question-only run carries (9B) is therefore not in those tokens. It needs both spans at once:
  redundancy.

## Amendment 44 (Zach, 2026-10-25 17:13 UTC, before any Bolt run): Bolt with hub Mamba kernels, 100-prompt lens, the amendment-42 design

- **Why (Zach: "Bolt, not llama"):** Bolt is the next non-Qwen model, after Lightning (amendment 40 note 1's loading
  path, approved).
- **Kernels.** Bolt's own code imports mamba_ssm directly, so set_use_kernels cannot reach it. model._hub_mamba_ssm
  loads the prebuilt HF-hub mamba-ssm, at the revision transformers fetched for Lightning (kernels-community/mamba-ssm
  @28017f3), registers it as mamba_ssm and the submodules that code imports, and reports mamba_ssm available. Checked
  (imports only, a GPU visible): the code's fast path is on, with all five kernels present. Before any run, Bolt's
  chain compares kernels and the torch path on 32 WikiText rows (scripts/kernel_nll.py; BJ_NO_KERNELS=1 turns them
  off). It stops unless |mean NLL diff| <= 0.01 and top-1 agreement >= 0.95; Lightning's was 0.0008 and 97.6%.
- **Lens:** our plain J-lens on 100 prompts. The jlens README: "~100 prompts is usable", "quality saturates quickly";
  the paper used 1000. Flagged on Bolt's results. Lightning keeps 200.
- **Procedure (scripts/queues/h200_bolt_1025.sh):** smoke, kernel check, competence smoke, fit, gate, the dev depth
  profile, the dose curve at its pick, the test knock-out and swap at the pick, and the swap at mid depth L44-55 (50-62%
  of 88). Readings as amendments 39 and 42. Disk: DeepSeek's cache is dropped only once h200ds42 and h200dsdose both
  end with 0 failures. The 27B renderings (amendment 38 B) run after Bolt (h200qrend27).

**Amendment 44, note 1 (Zach, 2026-10-25 17:26 UTC, before either fit):** Lightning's and Bolt's plain J-lenses are fit
on 64 prompts, not 200 and 100. Zach asked whether fewer suffice. The paper's appendix (Methodological details,
Data: Amount) sweeps 1 to 1000 prompts and says "J-lens beats the logit lens and tuned lens baselines with as few as
10 prompts", with small gains beyond. Our J++ lenses at 32 prompts beat the logit lens clearly (Ministral held-out
pass@10 0.651 vs 0.461). 64 keeps a margin for the top-10 directions the knock-out uses, and saves ~2 h on Lightning's
fit and ~1.5 h on Bolt's, which now run in a row. Chains relaunched (h200nemL8, h200bolt6, h200qrend27b); nothing had
run in them.

**Amendment 44, note 2 (Zach, 2026-10-25 17:29 UTC, before either fit): 32 prompts.** Zach: "Do 32 prompts." Lightning's
and Bolt's plain J-lenses are fit on 32 prompts, as our J++ lenses were (the paper: the J-lens beats the logit lens with
as few as 10). Flagged on both models' results. Chains relaunched (h200nemL9, h200bolt7, h200qrend27c); nothing had run
in them.

## Amendment 45 (Zach, 2026-10-25 18:58 UTC, before any Nemotron lens is fit): no plain J-lenses; J++ for the Nemotrons

- **Zach: "Don't do plain j lenses anywhere."** Lightning's and Bolt's plain J-lens fits (amendments 40, 42, 44) are
  withdrawn before any ran (chains h200nemL9 and h200bolt7 stopped while waiting; no lens file exists). Earlier
  plain-J-lens runs (Muse's published J-lens comparison, gpt-oss's neuronpedia J-lens, Mistral-Small-24B's community
  J-lens, the 27B's q27jlens) are not used for any claim. Then Zach: "Go ahead. A": J++ for both Nemotrons; the
  `kernels` package (0.16.2, as the harness env) installed into jpp_lens's env (nothing else changed).
- **Lightning's J++ (scripts/queues/h200_nemfit_1025.sh):** Ministral's recipe (router 64 prompts, one shard of 32
  prompts, source layers 0-50, target the final block, merge, grade, readout weights, held-out evaluation, export,
  sha256 into pins). Changes:
  - The LN rule alone (--lrp-mode ln, gpt-oss's mode). The fitter refuses rlens because Nemotron has no gated MLPs
    (relu^2). The Mamba, attention and MoE layers keep standard gradients, as OLMo-Hybrid's GatedDeltaNet did. Checked
    on an empty Lightning: 53 norms patched (52 blocks + norm_f); the Mamba mixers' gated norms untouched.
  - jpp_lens patches: NemotronHRMSNorm registered with Qwen2's rule (its forward is line-for-line Qwen2RMSNorm's); for
    NemotronH, jlens.from_hf gets its layout (norm_f, embeddings) and no BOS, as the harness feeds it. The full diff
    is scripts/lens_fit/jpp_lens_bridge.patch.
  - The model is loaded from its pinned local snapshot (a9904d2): jpp_cli loads by name, which would resolve to the
    hub's latest revision.
  - The HF-hub mamba-ssm kernels (the harness's pinned kernel) via scripts/lens_fit/jpp_cli_hubmamba.py.
  - The working directory is in /dev/shm.
  The lens check (lens_agreement) follows, and the held-out pass@10 vs the logit lens is reported. Then amendment 42's
  design runs unchanged (gate, profile, dose, test and swap at the pick, mid-depth swap L26-32).
- **Bolt's J++:** pins switched to J++; its fit needs jpp_cli to load Bolt's own code over two GPUs. It gets its own
  note before it runs.

**Amendment 45, note 1 (Zach, 2026-10-25 18:59 UTC, before the fit):** the hub mamba-ssm kernel needs `einops`, which
jpp_lens's env lacked; installed at the harness env's version (0.8.2, nothing else changed). transformers 5.14.1 (that
env) loads NemotronH's kernels through lazy_load_kernel (mamba-ssm and causal-conv1d at "version 1", unpinned).
jpp_cli_hubmamba.py seeds that table with the harness's pinned build (kernels-community/mamba-ssm @28017f3 and its
causal-conv1d). Checked on an empty Lightning in that env: fast path on, the scan and conv from that build.

**Amendment 45, note 2 (Zach, 2026-10-25 19:06 UTC, before the fit): a quality gate on Lightning's J++.** If its held-out
macro pass@10 does not exceed the logit lens's, the chain stops before the gate, profile, knock-out or swap, and
nothing is claimed with that lens. Ministral's was 0.651 vs 0.461.

## Amendment 46 (Zach, 2026-10-25 19:17 UTC, before any Bolt run): Bolt's J++ and chain

- **Why:** Zach chose option A: J++ for both Nemotrons, no plain J-lens.
- **Bolt's J++ (scripts/queues/h200_boltfit_1025.sh):** Lightning's recipe (amendment 45 and its notes: LN rule alone,
  router 64, 32 prompts, the quality gate), source layers 0-86, two GPUs (jpp_cli --device-map auto). jpp_lens's
  get_hf_model (patch, scripts/lens_fit/jpp_lens_bridge.patch) builds Bolt's language model alone by its own code from
  the pinned snapshot (e09a4ce), as the harness does. Bolt's RMSNorm applies its weight in fp32 before the downcast, so
  its LN rule is Olmo3RMSNorm's. The class shares transformers' NemotronHRMSNorm name, so the rule is set in that
  process only. jpp_cli_hubmamba.py also reports mamba_ssm and causal_conv1d available, which Bolt's code checks before
  importing them. Checked on an empty Bolt in jpp_lens's env: fast path on; 89 norms patched (88 blocks + norm_f) with
  Olmo3's rule; patcher OK.
- **Chain (scripts/queues/h200_bolt_1025.sh, h200bolt8):** as amendment 44, with this fit in place of the plain
  J-lens: DeepSeek's cache dropped only after both DeepSeek chains end with 0 failures; download; after Lightning
  (h200nemL10); smoke and the kernel-vs-torch check; J++ fit and its quality gate; gate, profile, dose, test and swap at
  the pick, mid-depth swap L44-55. The 27B renderings run after Bolt (h200qrend27e).

## Amendment 47 (Zach, 2026-10-25 19:34 UTC, before any run below; a smoke of 2 items per word ran first for the mechanics, and its pooled numbers (n 12 memory items, 9B) were seen; they are not used): the cross-relation swap

- **Why (Zach: "Go ahead"):** Neel's replication found two-hop swaps dominated by answer swaps (linear relations). Our
  swap moves memory-final answers through the J-part at the bridge's mention, computed before the question is asked,
  and does so with both answers' token directions protected (amendment 38 A: swap_noans 100% of swap, 27B and 9B). But
  the donor's J-part comes from the same passage, which is themed on the asked relation (lures in its answer
  vocabulary). So it may carry only a theme-primed value, not the entity.
- **Design (scripts/jswap_xrel.py):** the two v2 relations with country bridges, countries (continent) and languages.
  The donor country D's J-part is taken from another test prompt where D is named: of the same relation (swap_srel) or
  of the other relation (swap_xrel, e.g. a continent-themed passage for a language question). Controls: jswap's swap
  (same prompt, reference), swap_xrel_rot, swap_xrel_u, paste_xrel (ceiling). The read and tracked starts; eligibility
  as the knock-out; the 27B at L32-40 and the 9B at L12-16.
- **Measure:** transfer (donor - third) on the memory finals pooled (PM PA PN TM TA TN), 95% bootstrap over bridges.
- **Readings, two-sided, fixed now:**
  - swap_xrel >= 2/3 of swap_srel = the mention's J-part carries the entity, not a theme-primed answer;
  - swap_xrel <= 1/3 of swap_srel = relation-primed;
  - otherwise mixed.
  - Not read if swap_srel < 10: the J-part does not transfer across prompts at all.
  - Predictions: swap_xrel_rot and swap_xrel_u < 5; lookups (PP PK TP TK) kept >= 80% under swap_xrel.
- **Run (scripts/queues/h200_xrel_1025.sh, GPU 0):** after the 9B renderings, the 9B then the 27B.

## Amendment 48 (Zach, 2026-10-25 20:40 UTC, before any run below; smokes on the 9B ran first for the mechanics, and their numbers were seen, listed under "Seen"): the TA's follow-ups, i.e. probability scoring, a variance control, a probe ceiling

- **Why (Zach: "Have we properly addressed the TAs comments … are we using probes as a ceiling where appropriate? Is
  logit lens and rotated a sufficient control?", then "Go ahead"):** the TA's notes of 23 Oct asked for sampling at
  temperature 1, probes as an upper ceiling, and precise interventions. Our controls so far are the rotated span (same
  size, random direction) and the logit lens (same selection rule, the unembedding's directions). Neither is a
  supervised ceiling, and neither asks whether the J++ split is just "remove the residual's biggest directions".
- **A. Probability scoring (scripts/soft_score.py; post hoc, on existing rows, already run, all numbers seen).** Points
  lost = 100 x (mean p unedited - mean p edited), where p is the answer's first-token probability. That is the
  expected accuracy under temperature-1 sampling, no thinking. Computed on the same eligible items as the candidate
  pick, and reported beside every hard M - K in the write-up as secondary. Where they disagree, the hard split is
  called a threshold effect. Seen, paper10 at each model's test band:

  | Model | soft M - K | hard M - K |
  |---|---|---|
  | 27B | +50 | +51 |
  | 9B | +35 | +43 |
  | Muse | +49 | +60 |
  | Ministral | +37 | +23 |
  | DeepSeek L18-23 | +21 | +18 |
  | 122B late band | +2 | +49 |

  For the 122B, soft K is lost 84: a global probability collapse that leaves the argmax in place on K.
- **B. Variance control (ablate_v2 conditions pca1, pca3, pca10).** At each band layer, a dictionary of the top 256
  principal directions of the residual, each with both signs. The directions come from 64 pinned WikiText rows of 128
  tokens, with the first position left out, centred. At each position, the K directions with the largest projection
  are removed (paper10's per-position top-K rule, over the residual's own highest-variance directions). No atoms are
  protected: paper10's protection indexes token rows, and principal directions have none.
  - Items: the test knock-out's items, band and eligibility, so the comparison is item-matched with paper10.
  - Removal size: scripts/removal_size.py --pca at the band layers, K = 1, 3, 10, beside paper10's and unembed10's.
  - Readings, fixed now:
    - The damage-matched dose is the pca dose whose K loss is nearest paper10's K loss (ties go to the smaller K).
    - If its M - K is <= 1/3 of paper10's, the J++ split is not a variance effect.
    - If it is >= 2/3, removing the residual's biggest directions gives the split too, so J++ is not needed for it.
    - Otherwise, mixed.
    - Not read if paper10's M - K < 10 at that band.
    - All doses are reported, hard and soft.
- **C. Probe ceiling (scripts/probe_ceiling.py).**
  - **Readout.** At the last token of an entity's first mention, a multinomial logistic probe per relation predicts
    the entity's value of the item's relation.
    - Train: every entity mention in the dev prompts, never a test bridge.
    - Test: the test bridges' first mention, starts P and T, finals M and N.
    - L2 penalty: chosen by entity-grouped 4-fold cross-validation at the band's middle layer.
    - Beside it, on the same items: the J++ lens's pick and the logit lens's pick among the relation's answer tokens.
    - Fact-table coverage: most relations hold one or two entities per value (cities 51 entities over 30 values;
      dishes 36 over 20; landmarks 42 over 27), so an unseen value can't be predicted. Test items, and CV held-out
      items, whose value no training entity has are left out.
    - A relation's probe is valid if its dev CV accuracy at the middle layer beats the held-out majority rate by
      0.10. This check uses dev data only.
    - Measure, per valid relation: the share of the probe's above-chance accuracy that J++ reads,
      (J++ - chance) / (probe - chance), at the band layers. It is also pooled over valid relations, weighted by test n.
    - Readings: >= 2/3 means the lens reads near the linear ceiling; <= 1/3 means the lens misses much of what is
      linearly present; otherwise, mixed.
    - Not read for a model with no valid relation. The ratio is not read where probe accuracy is <= chance + 0.10 on
      test.
    - With 33-60 entities per relation, the probe is data-starved. It is a ceiling only where valid, and J++ may beat
      it elsewhere. That case is reported as such, not as a ceiling result.
  - **Causal, at the band, at each mention of X (jswap's design, donor D from the same passage).**
    - Conditions:
      - swap: J++ top-10;
      - swap_probe: X's component in the probe subspace replaced by D's;
      - swap_probe_rot: the same-size change in a fixed random direction (seed 4242 + layer);
      - remove and remove_probe;
      - paste: the ceiling.
    - The probe subspace per relation and layer: the top min(10, values - 1) right singular vectors of the probe's
      centred class weights in residual units. It is smaller than J++'s 10 on relations with few values, and its
      size is reported.
    - Measure: transfer (donor - third) on the memory finals pooled (PM PA PN TM TA TN), 95% bootstrap over bridges.
      Pooled over all relations, and over valid relations (memory_valid, the one read).
    - Readings:
      - swap_probe >= swap: a supervised subspace carries at least what J++'s does, so the lens is a convenient basis,
        not a privileged one;
      - swap_probe <= 1/3 of swap: J++'s directions carry what the decodable subspace does not;
      - otherwise, mixed.
    - Predictions: swap_probe_rot < 5; lookups (PP PK TP TK) kept >= 80% under swap_probe and remove_probe.
    - Not read if swap < 10 or paste < 20.
- **Runs (scripts/queues/h200_ta_1025.sh).**
  - DeepSeek at L18-23 tonight, after its dose chain, before Lightning. Its cache is dropped for Bolt after that.
  - Monday after Bolt, beside the 27B renderings:
    - 27B at L32-40;
    - 9B at L12-16;
    - Ministral: probe at L20-25 (mid, where its swap transferred little) and pca at L32-37 (its test band).
  - Each logs to W&B and EXPERIMENTS.md.
- **Seen (9B, smokes; mechanics only; their items are in the 9B's real runs):**
  - probe_ceiling smoke 1: 2 items per word, readout at stride 8 before the CV fix.
    - Per relation, at L12-16, probe / J++: countries 0.85 / 0.84; cities 0.70 / 0.81; companies 0.40 / 0.90;
      people 0.33 / 0.77; animals 0.60 / 0.19.
    - Pooled memory transfer, n 12: swap +50, swap_probe +25, swap_probe_rot 0, paste +42.
  - Smoke 2: 1 item per word, after the CV fix.
  - pca smoke: dev, L12-16, 4 items per word (PK, PM). pca10 lost PK 3/4 and PM 4/4; paper10 lost PK 0/4 and PM 2/4.

**Amendment 48, note 1 (Zach, 2026-10-25 21:00 UTC, before any real run; smokes 2-4 on the 9B ran and were seen): a size-matched variance control replaces the pca dose.**
- **Why.** removal_size --pca on the 9B (L12, L14, L16; 16 WikiText rows; position 0 excluded) gives the median share
  of the residual norm removed:

  | Removal | L12 | L14 | L16 |
  |---|---|---|---|
  | J++ top-10 | 12.5% | 12.7% | 14.8% |
  | logit lens top-10 | 8.5% | 8.8% | 10.0% |
  | pca top-1 | 34% | 50% | 34% |
  | pca top-3 | 48% | 62% | 51% |
  | pca top-10 | 65% | 73% | 68% |

  A single principal direction already removes 3-4x what paper10 does. No pca dose is size-matched, and the
  damage-matched reading of amendment 48 B can't be met.
- **The primary variance control is now paper10_pcasize.** At each position, paper10's removal (same selection, same
  protection) is replaced by a removal of the same norm along the residual's top 256 principal directions (amendment
  48 B's), taken in order of |projection| at that position, the last one in part (ablate.size_matched_removal). The
  size match is exact on random data, to 1e-6. So paper10, paper10_rot and paper10_pcasize all remove the same amount
  at every position:
  - paper10 removes along the lens's directions;
  - paper10_rot removes a random direction;
  - paper10_pcasize removes along the residual's highest-variance content.
- **Readings, fixed now:**
  - paper10_pcasize M - K <= 1/3 of paper10's means the split is not a variance effect;
  - >= 2/3 means removing the same amount of the residual's biggest content gives it too;
  - otherwise, mixed.
  - Not read if paper10's M - K < 10.
  - pca1 is kept as a descriptive point (the largest principal direction at each position, 3-4x paper10's size).
    pca3 and pca10 are dropped.
- **Probe changes.**
  - The CV grid for L2 is widened to 1e-5 to 1, because smoke 2 picked the old grid's low edge (1e-4). Smoke 3 picks
    1e-5 for 5 of 8 relations, the edge again, and test accuracy moves by <= 0.05. Reported as is.
  - Each prompt is recorded once with all its mentions. In smoke 3 the J++ and logit-lens readouts were identical to
    smoke 2's.
- **Seen (9B, mechanics only):**
  - Smokes 2-3: probe-valid relations are cities, countries and languages. At L12-16, probe vs J++: cities 0.70 vs
    0.82, countries 0.85 vs 0.84, languages 0.62 vs 0.89. Pooled memory (n 6): swap +100, swap_probe +50,
    swap_probe_rot 0, paste +83.
  - Smoke 4: dev, L12-16, 4 items per word. Lost items: paper10 PK 0/4, PM 2/4; paper10_pcasize PK 0/4, PM 1/4;
    pca1 PK 1/4, PM 1/4.
- **Runs.** DeepSeek's job (h200dsta) and Monday's job (h200qta) were relaunched with these conditions before
  starting.

## Amendment 49 (Zach, 2026-10-26 00:45 UTC, before any run below): a seeded random half of the items for Bolt's test and swap and for the 27B's renderings

- **Why (Zach: "do we need that much data … just because it has more eligible items that doesn't mean we need to
  calculate it from all of them", then "Do it"):** our readings are threshold decisions. The 27B's v2 M - K has a CI of
  about +/-3.5 at ~890 items per final. Half the items gives about +/-5, which leads to the same decision on every
  reading in amendments 38 B, 39, 42 and 48. The full runs cost compute that the last day needs (Bolt runs across two
  GPUs; the renderings take ~5 GPU-hours).
- **How:** a seeded random sample per word replaces --n's "first n per word", which leans toward the first bridges and
  relations. It is implemented as ablate_v2 and jswap --sample-per-word N --sample-seed 0, with random.Random("0:WORD")
  over the word's sorted eligible item ids (ablate_v2) or over its jobs (jswap). A word with N or fewer keeps all of
  them, so the tracked-start words (n 13-60) keep every item. Both are recorded in the manifest.
- **Applies to:**
  - Bolt's test knock-out and its swap at the profile pick: 150 per word (h200_nq40_1025.sh reads
    /workspace/scratch/nem35b_sample.txt). Same conditions, same run names.
  - The 27B's renderings jsuite_v2r2 and jsuite_v2r3: 150 per word (about half). The conditions are paper10, paper10_rot
    and unembed10. unembed10_rot, the logit lens's own rotation, has been about 0 on every model and is dropped. Run
    names end in _s150.
- **Not changed:**
  - Lightning (its test and swap run at full n tonight);
  - Bolt's dev profile and dose (n 40 per word already), and its mid-depth swap L44-55 (inside its running chain);
  - the 27B and Ministral amendment-48 runs, already queued;
  - every run of record.
- **Readings:** unchanged, with the CIs the smaller n gives. If a reading's CI straddles its threshold because of the
  smaller n, it is reported as undecided, not re-run.

**Amendment 49, note 1 (Zach, 2026-10-26 01:05 UTC, before Bolt's profile; Zach: "Go ahead"): the dev profiles and doses held only the country relations.**
- **Found:** "first n per word" (--n 40) took each word's first eligible items. jsuite_v2_dev_chat lists the country
  relations first, so every v2 dev depth profile and dose so far ran on country bridges only:

  | Model | Items | Bridges | Mix |
  |---|---|---|---|
  | 27B | 240 | 24 | countries -> continent only |
  | 9B | 240 | 37 | 198 countries, 42 languages |
  | Ministral | 240 | 34 | 177 / 63 |
  | DeepSeek | 240 | 40 | 162 / 78 |
  | Lightning | 240 | 36 | 204 / 36 |

  amendment 39's sweeps (--n 100) also took people and a few cities.
- **What this changes:**
  - Every profile pick (DeepSeek L18-23, Ministral, Lightning L27-33) and every dose curve was chosen on country-bridge
    items; the 27B's on countries -> continent alone, a relation with 5 answers.
  - Any depth-profile or dose claim is about country bridges only.
  - Not changed: the test knock-outs, swaps, cross-relation swaps, probe and variance runs, which took every eligible
    item of all 8 relations.
- **Fix:**
  - Bolt's profile and dose (not yet run) take a seeded random 40 per word over all eligible items: h200_profile_1025.sh
    and h200_dose_1025.sh read /workspace/scratch/nem35b_sample_dev.txt, and use ablate_v2 --sample-per-word 40
    --sample-seed 0 with --n 1000.
  - Profile reruns on all relations (profile step "rs", run names ..._profile_rs40_...) for the 27B, 9B, Lightning
    and Ministral are queued for Monday if the write-up uses depth profiles. DeepSeek's cache is dropped, so its
    profile stays country-only, reported as such.
  - The picks already used for test runs are not revisited. They are dev choices, and the test runs they led to stand
    as run.
- **Also from this note (not experiment changes):**
  - manifests record the working tree (pins.git_state: dirty files, untracked scripts, code-diff hash);
  - queue waits need a numeric EXIT line;
  - Bolt's chain can restart past its disk check once the snapshot is on disk.

**Amendment 49, note 2 (Zach, 2026-10-26 03:15 UTC): Bolt's competence generates without a cache; the order changed.**
Bolt's first try passed its gates:
- smoke: unembed exact, no-op edit 0.0, plain text 2.39 nats;
- kernel check: NLL diff +0.0017, top-1 agreement 0.957.

It then stopped at the competence smoke. transformers' generate() hands Bolt's own code (NemotronHPuzzleForCausalLM) a
DynamicCache, and Bolt's Mamba blocks need their hybrid cache (AttributeError: conv_states). natural_v1's hop-1
generation now passes use_cache=False for a model built by its own code (pins remote_lm). Checked on a random-weight
8-block Bolt: the default fails as in the run, and use_cache=False gives the same tokens as a plain greedy loop.
Nothing else changes. The 27B's renderings (amendment 49), queued after Bolt, started when Bolt's chain exited.
Bolt's chain is relaunched to wait for them, then repeats its gates and continues as amendments 44, 46, 49 and
49 note 1.

## Amendment 50 (Zach, 2026-10-26 03:40 UTC, before any run below): Monday's queue after Bolt

- **Why:** Lightning's test (+53, J-specific, all relations) makes it the second family. Its evidence should match the
  Qwens': the same controls, data seeds and mechanism tests. CLAUDE.md also requires the 27B headline rerun from a clean
  checkout. Amendment 49 note 1 queued the all-relation profiles.
- **GPU 1 (job h200monL), after Bolt:**
  - Lightning's probe ceiling and variance control at L27-33 (amendment 48 and note 1, as the Qwens'), then its
    cross-relation swap at L27-33 (amendment 47; scripts/queues/h200_xrelm_1026.sh).
  - Lightning's renderings jsuite_v2r2 and jsuite_v2r3 at 150 per word (amendment 49: paper10 / rot / unembed10).
  - All-relation dev profiles (amendment 49 note 1, "rs", 40 per word) for Lightning and Ministral.
- **GPU 0 (job h200mon0), after Bolt:**
  - The 27B v2 headline from a clean checkout: scripts/queues/h200_clean27_1026.sh, a copy of amendment 37 C's (the
    9B's) with the 27B's target, band and batch (32, as the run of record), compared row by row with the run of
    record.
  - All-relation dev profiles for the 27B and the 9B.
- **Readings:** those of the amendments named, unchanged. The clean rerun passes if every shared row agrees
  (correct, correct_cand2, correct_top). Any difference is reported with its count, not explained away. The profiles
  are descriptive: the depth of the J-specific band on all relations, beside the country-only profile. Picks already
  used are not revisited.

## Amendment 51 (Zach, 2026-10-26 03:26 UTC, before any run below; a 9B smoke of 2 jobs per word ran first for the mechanics and its numbers were seen): what the mention's J-part carries (scripts/jswap_pointer.py)

- **Why (Zach: "Go ahead with 1-3"):** the cross-relation swap (amendment 47) and the probe swap (amendment 48) say the
  mention's J-part at mid depth carries which entity, and that the attribute is recalled later. Three open questions:
  1. Does this hold beyond the country relations?
  2. Is the J-part just the entity's name?
  3. Where is the attribute looked up?
- **Design:** jswap's jobs (same donors, thirds and positions, so `swap` reproduces jswap) on every facts relation,
  words PP PK PM PA PN TP TK TM TA TN, at the model's band, 150 random jobs per word (seed "0:WORD", amendment 49).
  1. **Context-free donor.** D's J-part comes from a one-sentence neutral prompt in the same chat framing: "A reader
     asked a question about D in the letters page.", a sentence the passages use. Conditions: swap_neutral, its
     same-size rotation (swap_neutral_rot), the logit lens's top-10 (swap_neutral_u), the whole residual
     (paste_neutral).
  2. **Own name.** Own-word rows are each entity's surface tokens plus every row with cosine >= 0.5 to its concept
     token (ablate_v2's keep_own rows).
     - swap_own swaps only the span of up to 10 own-word rows with the highest logits at each side.
     - swap_noown is jswap's swap with the own-word rows (and the answer's protected rows) never chosen.
  3. **Timeline.** Under none, swap and swap_neutral, the J++ lens's pick among the item's candidate answers at the
     answer position, at every lens layer from the band's first on.
- **Measure:** transfer (donor - third) on the memory finals pooled (PM PA PN TM TA TN), overall and per relation,
  95% bootstrap over bridges.
- **Readings, fixed now:**
  1. **Context-free donor.** swap_neutral >= 2/3 of swap means the J-part carries the entity whatever its context;
     <= 1/3 means what transfers depends on the passage; otherwise mixed. "General across relations" means >= 2/3 on at
     least 6 of the 8 relations where swap >= 10. Predictions: swap_neutral_rot and swap_neutral_u < 5; lookups
     (PP PK TP TK) kept >= 80% under every condition. Not read if swap < 10.
  2. **Own name.** swap_noown <= 1/3 of swap means what the J-part carries is the entity's own-word directions (its
     name, as the model will say it); >= 2/3 means it carries the entity beyond those directions; otherwise mixed.
     swap_own is reported beside it, descriptive.
  3. **Timeline (descriptive).** On memory items right unedited, the share whose lens pick at the answer position is
     X's answer (none) or D's (swap) at each layer. Also reported: the first layer from which D's answer leads in more
     than half the items.
- **Runs (scripts/queues/h200_ptr_1026.sh):** the 9B at L12-16 first (beside the 27B renderings, before Bolt). Then
  the 27B at L32-40 and Lightning at L27-33, after Monday's queue.

**Amendment 49, note 3 (Zach, 2026-10-26 05:15 UTC, before Bolt's relaunched chain): Bolt's MoE runs as grouped GEMMs; the equivalence check missed my bar and Zach chose to proceed.**
- **Found:** Bolt's own code (modeling_nemotron_h.py, NemotronHMoE.moe) loops over every routed expert of each of its
  40 MoE layers (240-496 experts). Each step has a torch.where sync and a no-op call for unused experts. Its 120-item
  competence smoke ran ~40x slower than Lightning's (17+ min vs 3.4 min); the chain would have taken days. That run was
  stopped at its competence smoke; the gates had passed.
- **Two replacements, set at load (model._patch_fast_moe; jpp_lens's Bolt loader as well):**
  - _fast_moe: the same expert calls on the same token rows in the same order, one sync per layer, unused experts
    skipped (their call adds zeros: no MLP bias). Bit-identical to NVIDIA's outputs and gradients on a real-size Bolt
    layer, but only 1.6x faster.
  - _grouped_moe: the experts' weights are stacked in place (+41 MB) and the layer runs as two torch._grouped_mm calls,
    summed over the k slots in a fixed order. About 49x faster on one layer, relative difference 2e-5 there, gradients
    flow. On the full model: 0.54 s vs 2.13 s for a 2 x 183-token forward.
- **The check (scripts/bolt_moe_check.py, results/checks/nem35b_moe_check.json, grouped vs the exact loop on the loaded
  Bolt):**
  - mean NLL on 16 WikiText rows: 2.2295 vs 2.2281 (diff +0.0014);
  - top-1 agreement: 0.959;
  - last-position top-1 on 16 dev chat prompts: 15 of 16;
  - max logit diff 1.75.

  The bar I wrote into the script before running it (|NLL diff| <= 0.01 and top-1 agreement >= 0.99) is **not met** on
  top-1 agreement. This is disclosed here, not redefined. For context, Bolt's own Mamba-kernel check (hub kernels vs
  the torch path, amendment 44) shows the same size of difference (NLL +0.0017, top-1 0.957, accepted at >= 0.95).
  Bolt's argmax is that sensitive to bf16 rounding in general.
- **Decision (Zach, option 1 of 3):** proceed with the grouped MoE for every Bolt run (harness and J++ fit). Bolt's
  numbers are reported as "Bolt with grouped-GEMM experts". Every Bolt condition uses the same implementation, so
  within-model contrasts compare like with like. The exact loop (4x slower, ~20 h for the chain) and dropping Bolt were
  the other options.
- **Order:** Bolt's chain is relaunched now (gates repeated). Monday's queue (amendment 50) and the pointer tests
  (amendment 51) wait for it, as before.

**Amendment 49, note 4 (Zach, 2026-10-26 08:40 UTC): a padded fast path for Bolt was tried, failed its own check, and was discarded; Bolt runs on exact-length batches.**
- **Why tried:** Bolt's forward costs ~0.5 s per call whatever the batch. Our scripts batch prompts of equal length
  only, so its competence and knock-outs ran as thousands of near-empty forwards.
- **What was tried:**
  - ablate_v2 --pad (right-padded batches) for Bolt's profile, dose and test knock-out, through a flag file
    (/workspace/scratch/nem35b_pad.txt);
  - a padded natural_v1 competence path for remote_lm models;
  - Bolt's dev profile, run in padded batches by scripts/queues/h200_padprof_1026.sh while its queue script was paused.
- **What went wrong:** the padded profile's unedited reads were right on 20 of 240 items. The exact-length competence
  run had all 240 right. Cause: Bolt's own forward ignores logits_to_keep and returns every position's logits.
  ablate.first_token_logits indexed the kept positions, so padded rows were read at the wrong positions. Exact-length
  reads take the last position and are unaffected; so is every other model, which honours logits_to_keep.
- **Done:**
  - The padded profile was discarded (moved to scratch/killed_1025/nem35b_profile_padded_BROKEN; nothing read from it).
  - The flag file was removed.
  - natural_v1's padded path is opt-in only (BJ_PADDED_COMPETENCE; not set anywhere).
  - Bolt's queue resumed on exact-length batches. Its profile is re-running as amendment 49 note 1 specifies
    (40 random per word over all relations).
  - first_token_logits now reads each row at its own last position when the model returns every position. Checked
    on a random-weight 8-block Bolt: padded reads give the same argmax as one-by-one reads (4 of 4).
  - The fast-competence check against the exact path never finished (stopped). No Bolt result uses a padded path.

## Amendment 52 (Zach, 2026-10-26 16:31 UTC, before any run below): is Bolt's dependence spread over more directions?

- **Why (Zach: "possible bolt didn't work because we didn't remove enough directions? M-K went up with more directions
  removed right?"):** Bolt's dev dose at L42-53 rose with K (top1 +1, top3 +1, top10 +8, top30 +15 [6, 24];
  rotations 0; K lost 0). The Qwens and Lightning saturate by K <= 10. Bolt's J-part swap (K = 10) carried +2.8 against
  a paste ceiling of +19.5. Both readings use K = 10, which may be too few directions for Bolt.
- **Design (scripts/queues/h200_boltk_1026.sh):** at L42-53, on the same 150 random items per word as Bolt's top-10 test
  (seed 0).
  - Removal sizes: removal_size.py --ks 10 30 100.
  - Knock-out: top30, top30_rot, top100, top100_rot, unembed30, unembed100.
  - J-part swap: jswap --k 30 and --k 100 (the swapped span is the top-K J++ directions; the other five conditions at
    that K).
- **Readings, fixed now:**
  - **Knock-out.** M - K at top100 >= 30, with its rotation <= 5 and the logit lens at 100 below half of it, means the
    dependence is distributed (more directions than K = 10). M - K < 15 at top100 means it is absent. Otherwise, weak.
    K (stated-fact) loss is reported beside each, and removal size beside each K.
  - **Swap.** The memory finals pooled. A K-part swap >= 2/3 of paste means the identity is in J-space, spread over K
    directions. <= 1/3 at K = 100 means it is not in J-space at that depth. Otherwise, partial.
  - Size caveat: a top-100 span takes more of the residual than top-10. The rotated K-span is the same-size control,
    and the logit lens at K is the same-rule control.

**Amendment 52, note 1 (Zach, 2026-10-26 17:56 UTC; Zach: "Can we speed it up?"): the K-span projection by the normal equations for Bolt's K = 30/100 runs.**
- **Why:** the first try ran at ~0.8 rows/s, about 5 h for the knock-out. ablate.top_span_removal projects each position on
  its top-K atoms through a batched fp64 QR of a d x K matrix, which dominates at K = 100.
- **Change:** with BJ_GRAM_PROJ=1, the same projection is computed by the K x K normal equations in fp64
  (A^T (A A^T + 1e-10 I)^-1 A x).
  - Speed: ~11x faster at K = 100 on random data (0.19 s vs 2.18 s per call), ~9x at K = 10.
  - Random data: equal to QR to 4e-13.
  - Real data (the 9B's J++ lens and WikiText residuals at L14, K = 10/30/100, J++ and identity dictionaries):
    per-position relative difference <= 1.3e-8.
  - QR stays the default. The flag is set only in scripts/queues/h200_boltk_1026.sh, so no earlier run or rerun is
    affected.
- **Discarded:** the first (QR) knock-out was stopped at 325 items and moved to
  scratch/killed_1025/nem35b_k30k100_qr_partial. Its interim numbers were seen (68 memory items, the shortest prompts
  first): M - K top30 +1.5, top30_rot 0, top100 +20.6, top100_rot +1.5, unembed30 0, unembed100 0, K lost 0. They are
  not used. The rerun covers the same 150 random items per word from the start. The removal sizes (K = 10/30/100) from
  the first try stand.

## Amendment 53 (Zach, 2026-10-26 22:10 UTC, before any run below): Ministral at K = 30 and 100

- **Why (Zach: "Go ahead"):** Bolt's "readable, not carried" at K = 10 reversed at K = 100. Its J-part swap rose
  2.8 -> 10.0 -> 41.3 with paste at 19.5, and its top-10 removal took only 5-7% of the residual (amendment 52).
  Ministral at mid depth (L20-25) is the remaining "readable, not carried" case:
  - J-part swap +1.8, paste +14.9, swap_comp +14.2;
  - J++ and a supervised probe read the attribute there, and neither subspace carries it (amendment 48).
  Its test M - K at L32-37 is +23 at K = 10.
- **Design (scripts/queues/h200_mink_1026.sh), normal-equations projection (amendment 52 note 1):**
  - The test knock-out at L32-37 with top30 / top100, their rotations and the logit lens at 30 and 100, on all eligible
    items as the K = 10 run.
  - Removal sizes at L20-25 and L32-37 (K 10/30/100).
  - The J-part swap at mid depth L20-25 with K = 30 and 100, all items as the K = 10 run.
- **Readings, fixed now, as amendment 52:**
  - **Knock-out.** Distributed if top100 M - K >= 2x its top-10 value (>= 46), with its rotation <= 5 and the logit
    lens at 100 below half of it. Unchanged if top100 is within 10 of +23. Otherwise, rising.
  - **Swap** (memory finals pooled).
    - A K = 100 J-part swap >= 2/3 of paste means the identity is in J-space, spread over K directions: Ministral is
      no longer a "readable, not carried" case.
    - <= 1/3 means it stays one.
    - Otherwise, partial.
    - Paste at L20-25 (+14.9) is below the old 20 bar. Amendment 49's lesson stands: paste is not a ceiling. The K-part
      swap is read against paste and beside swap_comp.

### Amendment 53 note 1 (Zach, 2026-10-26 22:23 UTC, after the K = 30 swap, before the K = 100 swap finished)

- The +14.9 / +14.2 / +1.8 quoted above are the PM cell alone (n 284, amendment 41), but the reading says "memory
  finals pooled". Pooled over PM PA PN TM TA TN (scripts/jswap_pool.py, n 1212), the K = 10 run gives paste +9.5
  [6.7, 12.6], swap_comp +8.4, J-part swap +2.6 [1.6, 3.7].
- The rule is a ratio to paste in the same table, so it stands as written on the pooled numbers: K = 100 swap >= 6.3
  (2/3 of 9.5) means distributed, <= 3.2 means it stays "readable, not carried", between is partial. The PM cell is
  reported beside it (bars 9.9 / 5.0).
- Seen before writing this: K = 30 pooled swap +3.5 [2.3, 4.9] (paste +9.5, swap_comp +8.4, rot +0.1, u +0.1); PM
  cell swap +2.9 [1.1, 4.9]. The K = 100 swap and the knock-out had not finished.

## Amendment 54 (Zach, 2026-10-26 23:00 UTC, before any run below; the 8-item smoke only): one dose grid for every model

- **Why (Zach: "Are our experiments uneven? Would it make sense to queue the remove 30, 100 directions on the other
  models? ... to see at what point it plateaus with adding more?"):**
  - K = 30 / 100 were run on the test set only for the two models that looked weak at K = 10 (Bolt, Ministral;
    amendments 52, 53). Raising K only where the effect was small is asymmetric.
  - The dev doses stop at K = 30 (Lightning, Ministral, DeepSeek, Bolt). The Qwens' doses are on the older full2 set.
  - Fixed K is not a fixed removal size: the top-10 J++ removal takes 6% of the residual in Bolt, 13-20% elsewhere.
- **Design** (scripts/queues/h200_dose_1026.sh; normal-equations projection as amendment 52 note 1; above K = 100 the
  removal is computed over fewer positions per chunk, which is exact, rows being independent; K <= 100 unchanged):
  - **Models,** each at its test band: Qwen 27B L32-40, Qwen 9B L12-16, Nemotron Lightning L27-33, Ministral L32-37,
    Nemotron Bolt L42-53. DeepSeek and OLMo-3 32B are not cached now. If they come back, the same design runs on them in
    a note to this amendment.
  - **Items:** the test set, a seeded random 150 per word (seed 0, Bolt's K-run sample), the 15 facts words, eligible
    items by each model's test competence.
  - **Conditions:**
    - J++ top K for K in {1, 3, 10, 30, 100, 300};
    - the same removal randomly rotated (same norm, random direction) at every K;
    - the same norm along the top-256 principal directions (topK_pcasize) at K in {10, 30, 100, 300};
    - the logit lens's top K at K in {10, 30, 100, 300}.
  - **Removal size** at the band for every K: J++, logit lens and top principal directions.
  - **Scoring:** jsuite2_score (M - K, start all, bootstrap over bridges, seed 0) and soft_score.
  - **Gap filling in the same queue:**
    - **(B) Position splits** where none exist: Lightning at L27-33 (paper10, rotated, logit lens; bridge mention only /
      the passage / the question on; all eligible items as its headline); Bolt at L42-53 (top100 and its rotation;
      bridge / question; 150 per word).
    - **(C) The clean-checkout rerun CLAUDE.md asks for,** for Lightning's headline (competence, then paper10 / rotated /
      logit lens / its rotation at L27-33, from a fresh worktree, compared row by row), as done for both Qwens.
- **Readings, fixed now:**
  - **Specificity limit:** the smallest K at which stated facts (K finals) lose more than 10 points, or the size-matched
    control's M - K exceeds half the J++ M - K. Readings below use only K under the limit.
  - **Plateau K\*:** the smallest K whose J++ M - K is >= 90% of the model's largest under the limit.
    - Concentrated if K\* <= 10.
    - Distributed if K\* >= 100.
    - Otherwise, intermediate.
  - **J-specific excess** at each K: the J++ M - K minus the larger of its rotated and size-matched M - K.
  - **Matched size** (descriptive): the J++ M - K and the excess at 15% and 20% removal share, interpolated linearly in
    share between neighbouring grid points, where both are under the limit.
- **Expectations,** written before any run:
  - **From the dev doses and the K runs:**
    - Lightning concentrated (dev top-1 +51, top-3 +54, top-10 +52, top-30 +42).
    - Ministral concentrated (dev 24 / 35 / 39 / 34 at K 1 / 3 / 10 / 30; test 23 / 24 / 19 at 10 / 30 / 100).
    - Bolt distributed (test 6 / 14 / 31 at 10 / 30 / 100).
  - **The Qwens, from the older full2 set:**
    - 27B: 20 / 33 / 36 / 46 / 60 at K 1 / 5 / 10 / 25 / 100, with lookups losing 12 at 100.
    - 9B: 31 / 37 / 38 / 35 / 48 at K 1 / 5 / 10 / 25 / 100.
    - So the 27B may keep rising until specificity breaks, and the 9B may be flat to 30 and then rise.
  - **What would change the story:**
    - If the 27B's K\* is >= 30 under the limit, "the Qwens are concentrated" is wrong. The claim becomes graded by
      matched size, not by K.
    - If Bolt's excess at matched size reaches Lightning's, Bolt is not weaker, only spread out.
- **Smoke, seen before this was committed** (8 items per word, PM and PK only, 27B at L32-40; it checked that K = 300
  fits in memory). Memory items right (of 8):
  - top300: 1;
  - top300_pcasize: 2 (stated facts 7 of 8);
  - top300_rot and unembed300: 7.
  - So the size-matched control may already break recall at K = 300. The specificity limit above was written with this
    in view; the readings were not changed by it.
- **Allocation:**
  - GPU 0: 27B, then 9B, then Lightning's clean rerun.
  - GPU 1: Lightning, Lightning's position split, then Ministral.
  - Then both GPUs: Bolt, then Bolt's position split.

### Amendment 54 note 1 (Zach, 2026-10-26 23:28 UTC, after Lightning's dose grid, before any other model's dose result)

- **Seen first:** Lightning's grid at L27-33.
  - J++ M − K at K 1 / 3 / 10 / 30 / 100 / 300: +46 / +50 / +51 / +54 / +54 / +69.
  - Greedy stated facts lose 1-5 at every K.
  - Rotated: +3 / +2 / +4 / +5 / +8 / +18.
  - Size-matched: +8 / +9 / +15 / +30 (K 10 / 30 / 100 / 300).
  - By probability, stated facts lose 8 / 10 / 10 / 29 / 50 / 56, and the soft M − K falls from +44 at K 10 to +18 at
    K 300.
- **The plateau reading as written uses the greedy J++ M − K and a greedy limit.** On Lightning:
  - no K reaches the limit, so the largest value is K 300's +69 and K\* = 300 ("distributed");
  - yet K 1 alone already gives +46;
  - the step at 300 comes with the rotated and size-matched controls rising too;
  - stated facts keep their top candidate but lose half their probability from K 30 on.
  - The pre-registered reading is still reported, as written, for every model.
- **Added now, as secondary readings for every model in the grid:**
  - **Excess plateau:** the plateau K\* computed on the J-specific excess (J++ M − K minus the larger of rotated and
    size-matched) instead of the raw J++ M − K. Same 90% rule, same concentrated / distributed bands.
  - **Probability limit:** the smallest K at which stated facts lose > 10 points by probability (soft score). Readings
    are also given only for K below it.
  - **Lightning under both:** the excess is 43 / 48 / 43 / 45 / 39 / 39, so the excess K\* = 1 (concentrated). Its
    probability limit is K 30.

### Amendment 54 note 2 (Zach, 2026-10-27 00:45 UTC, committed before the run started): Lightning's never-named bridge (R start), on the idle GPU

- **Gap:** the R start (amendment 35 note 1) was run for the 27B, 9B, 9B base, Ministral, Muse and the 122B, not for
  Lightning (the "not run" cell in the figure set's F05).
- **Run:** GPU 1 is idle from 00:45 until Bolt starts. scripts/queues/h200_v21r_1024.sh, step
  r:nemotron-3.5-lightning:nem35l_:27-33:16:
  - R-item competence;
  - the knock-out on RM RA RN at L27-33 with Lightning's v2 conditions (paper10 / rotated / logit lens / its rotation);
  - jsuite2_score of its v2 knock-out with the R run.
- **Reading, as amendment 35:** RM − MM, RA − MA and RN − MN, with 95% bootstrap over bridges.
  - Within 10 of 0: removing the bridge's one mention costs no extra recall loss.
  - Larger and positive: as the 27B (+18) and the 9B (+12).
- **Bolt waits for it:** chain C, which is only waiting, is relaunched with this job added to its waits (old log moved
  aside).

## Amendment 55 (Zach, 2026-10-27 01:11 UTC, before any run below): keep-own-word and swap dose on v2, in the GPU gaps

- **Why (Zach: "use both GPUs maximally"):** GPU 1 is idle until Bolt (amendment 54) starts. Two tests are still
  uneven across models.
  - **Keep-own-word (C1's second kill test, 10/21):** run only on the toy suite (27B restores 20%, 9B 26%, kill bar 75%),
    never on v2 or on a non-Qwen model.
  - **Swap dose:** the J-part swap at K = 30 / 100 exists only for Bolt and Ministral (amendments 52, 53).
- **Design (scripts/queues/h200_even_1027.sh):** each model at its v2 band, test set, 150 random items per word (seed 0,
  as amendment 54); normal-equations projection.
  - **Keep-own:** paper10, paper10_rot, paper10_keepown, paper10_keepown_rot. Keep-own is paper10 with the bridge's own
    word protected: its surface tokens and every dictionary row with them.
  - **Swap dose:** jswap at K = 10, 30, 100 on the same sample; memory finals pooled (scripts/jswap_pool.py).
  - **Order:**
    - now, GPU 1: Lightning, then the 9B (keep-own, then swaps);
    - after Bolt: the 27B and Ministral (keep-own), then the 27B's swaps.
  - An 8-item smoke of the keep-own conditions on v2 runs first.
- **Readings, fixed now:**
  - **Keep-own:** restored = 1 − (M − K under paper10_keepown) / (M − K under paper10), on the same items.
    - ≥ 0.75 kills C1 for that model (the 10/21 bar).
    - ≤ 0.25: the dependence is not the bridge's own word.
    - paper10_keepown_rot within 10 of 0.
  - **Swap dose:**
    - Grows if the K = 100 transfer is ≥ the K = 10 transfer + 10.
    - Saturated if within 10.
    - Paste and swap_comp reported beside it.

### Amendment 55 note 1 (Zach, 2026-10-27 01:13 UTC, before any run below): the overnight queue after Bolt

- **F0 (GPU 0, after amendment 54's Bolt chain):** amendment 55 on the 27B: keep-own, then the swap dose (K 10 / 30 / 100).
- **F1 (GPU 1, same wait):** amendment 55's keep-own on Ministral. Then **Lightning on the natural sets**, its first data
  outside jsuite v2, with the 10/23 recipes (scripts/queues/h200_natlight_1027.sh, a relabelled copy of
  h200_fix_1023.sh):
  - natplus_v1_chat: cand2 competence, knock-out at L27-33 (paper10 / rotated / logit lens / its rotation), c1_v2,
    c1_specificity, natplus_split.
    - Reading as amendments 14 and 20: the gap replicates if >= 30 with rotated within 10 and logit lens < 10.
    - Popular vs rare reported.
  - nat3_v1_chat (natural three-hop chains): per-word eligibility, nat3_score.
    - Reading: amendment 25's rule (a memory hop needs J-space when its output is not in the prompt) on Lightning's
      excess over PPP. The 27B's pattern is the comparison.
  - gen_spot on natplus (25 per word and relation): what Lightning says under the knock-out.
- **G (both GPUs, after F0 and F1): Bolt's pointer tests at K = 100.** scripts/jswap_pointer.py, now with --k
  (default 10, unchanged), at L42-53, 150 per word, as amendment 51.
  - The swap J-part, neutral donor, own-word split and timeline all use the top 100 J++ directions.
  - Readings as amendment 51: neutral donor >= 2/3 of the same-passage swap means context-free; the no-own-word share
    is read the same way; rotated and logit-lens swaps < 5.

## Amendment 56 (Zach, 2026-10-27 04:51 UTC, before any run below): the night of day 8-9

- **Why (Zach: "the best possible set of next moves ... until around noon"):** the proposal's own question (which
  intermediates live in J-space; H0) was last tested on the v1 modules and the toy suite. It has never been tested on v2
  or on a second family. Lightning's clean rerun was reproducible in its headline, not row for row; its cause is open.
- **A. v2 modules 2 and 3** (amendment 37 B's design, never run), scripts/queues/h200_v2mod_1027.sh: three-hop (8
  words) and numbers (12 words), per-item eligibility, paper10 / rotated / logit lens / its rotation, cand2 (numbers:
  digit dictionary), at each model's v2 band.
  - **Models:** the 27B, the 9B (their v2 test competence covers the modules), and Lightning. Lightning's eligibility
    comes from its clean-checkout competence run (nem35l_clean_..., 775f83d, all 7,080 items), copied into results/.
  - **Predictions, as amendments 24 and 25:**
    - Numbers: a counted (KR) or computed (AR) number reported within 10 of a read one (PR); a recalled one (MR)
      >= 10 above PR.
    - Three-hop: the chains with a memory hop whose output is not in the passage (PPM, MPM, PMM, MMM) lose more than
      PPP; MPP and PMP do not.
- **B. Lightning determinism check:** its facts knock-out at L27-33 rerun in the main repo at HEAD. Same eligibility
  (the clean competence), same conditions, batch and QR path as the clean rerun, compared row by row with it.
  - Identical rows: the clean-rerun differences came from eligibility and batching.
  - Differing rows: Lightning's kernels are not deterministic at this batch size.
- **C. Bolt's pointer tests at K = 100** (amendment 55 note 1), after A and B.
- **D. (Only with Zach's OK; it deletes Bolt's 140 GB cache.)** DeepSeek-V4-Flash at L18-23 through amendment 54's
  dose grid and readings, plus its mention / question split at the K where its J-specific excess peaks. Then, if time
  allows, OLMo-3 32B base (Q&A) at L12-20 the same way.
- **Order:**
  - GPU 0: (after the 27B swap dose) A on the 27B, then the 9B.
  - GPU 1: (after Lightning's natural sets) A on Lightning, then B.
  - Then C on both GPUs; then D if approved.

### Amendment 56 note 1 (Zach, 2026-10-27 05:00 UTC, before D runs): D approved

- **Approval:** Zach, 2026-10-27 ~01:00 ET: "Yes you can delete bolts cache after."
- **The chain:** scripts/queues/h200_ds_1027.sh.
  - It waits for Bolt's pointer test and drops Bolt's cache (/workspace/scratch/cache_drop.py) only if that test
    finished; otherwise it stops and keeps the cache.
  - It then downloads DeepSeek-V4-Flash at its pinned revision, runs amendment 54's dose grid at L18-23 (150 per word,
    seed 0), and runs the mention / question split at the K with the largest J-specific excess below the specificity
    limit.
  - The excess and limit are computed by fig_neel.dose_readings, the same code as every other model's readings.
- **Not approved yet:** OLMo would need DeepSeek's cache dropped too, so it is not queued.
