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

### Amendment 56 note 1 (Zach, 2026-10-27 05:01 UTC, before D runs): D approved

- **Approval:** Zach, 2026-10-27 ~01:00 ET: "Yes you can delete bolts cache after."
- **The chain:** scripts/queues/h200_ds_1027.sh.
  - It waits for Bolt's pointer test and drops Bolt's cache (/workspace/scratch/cache_drop.py) only if that test
    finished; otherwise it stops and keeps the cache.
  - It then downloads DeepSeek-V4-Flash at its pinned revision, runs amendment 54's dose grid at L18-23 (150 per word,
    seed 0), and runs the mention / question split at the K with the largest J-specific excess below the specificity
    limit.
  - The excess and limit are computed by fig_neel.dose_readings, the same code as every other model's readings.
- **Not approved yet:** OLMo would need DeepSeek's cache dropped too, so it is not queued.

### Amendment 56 note 2 (Zach, 2026-10-27 06:23 UTC, committed as the run started): lens-kind check on the 9B, in GPU 0's idle window

- **The confound:** the Qwens are knocked out with published J++ lenses; the Nemotrons, Ministral and Muse with our own
  fits (32 WikiText prompts).
- **The run (GPU 0):** the 9B's v2 facts knock-out at L12-16 with our own J++ fit (qwen3.5-9b-ourjpp: the jpp_lens
  recipe, 32 WikiText prompts; held-out pass@10 0.625 vs 0.391 for the logit lens), all eligible items, paper10 /
  rotated / logit lens / its rotation, as the 9B's headline.
- **Reading:** our fit's M − K within 10 of the published lens's (+43) means the lens kind does not drive the
  magnitude on this model. A larger gap is reported as a lens effect. On v1 the two differed by about 3.
- **Bolt's pointer job** (waiting) is relaunched to wait for this run too.

## Amendment 57 (Zach, 2026-10-27 07:49 UTC, before any run below): H0 head-on with a powered numbers set, a second three-hop seed, late-band positions for the 9B and Lightning

- **Why (Zach, 2026-10-27 ~03:45 ET: "What else to queue? U have until around noon"):**
  - The v2 numbers module (amendment 56 A) settles the report question: a number computed from the passage needs no
    J++ to be reported. It cannot answer H0 head-on, which is whether a computed number that the model then *uses* to
    recall something routes through J++. Those cells (KM, AM, and the lookups KL, AL) had 3-35 eligible items per model,
    because composing two steps is hard.
  - The three-hop result rests on one data seed per model.
  - Section 3's "late in depth, the dependence moves to the question" has the 27B, Ministral and the 122B. It has no
    late band for the 9B or Lightning.
- **Seen when this was written:**
  - Amendment 56 A's module results on the 27B, 9B and Lightning (EXPERIMENTS.md).
  - The dev depth profiles (amendment 42), including Lightning at L42-48: stated facts lose 74 points and recall 71,
    so M - K is about -2.
  - The new set's generation counts. No model output on it.
- **A. A larger numbers set and a second three-hop seed.**
  - **Set:** jsuite_v2nb, made by `scripts/jsuite_v2.py --name jsuite_v2nb --seed 2701 --numbers-reps 80` at commit
    3761c39. Only its test split's numbers and three-hop modules are used; its facts module is not.
  - **Numbers:** 6,709 items, 526-581 per word (v2: about 59). Only the lookup and recall finals: nPL nPM nKL nKM nAL
    nAM nML nMM. The report words are already powered on v2.
  - **Three-hop:** 911 items (105-120 per word), a new seed of natural3's chains.
  - **Procedure, per model:**
    - competence on those 16 words (`natural_v1.py competence --words ... --read cand2 --hop1 gen`);
    - then the knock-out as amendment 56 A: paper10 / rotated / logit lens / its rotation, per-item eligibility, cand2;
      numbers with the digit dictionary;
    - a smoke of one item per word first; scored by jsuite2_score.
  - **Models:** the 27B (L32-40), Lightning (L27-33), and the 9B (L12-16, numbers only: its three-hop was unreadable
    on v2).
  - **Predictions (numbers), loss = points lost among items right unedited:**
    1. **H0 head-on.** A number counted or computed from the passage that keys a recall needs no more J++ than a read
       one: loss(KM) and loss(AM) each within 10 of loss(PM). If either is at least loss(PM) + 15, with its rotated
       control within 10 of PM's, the computed number itself routes through J++: H0 is false for numbers in that model.
    2. **Final-hop rule** (amendment 24, prediction 2): SM - SL >= 20 for each start S in P, K, A, M.
    3. **Computation feeding a lookup** (amendment 24, prediction 3): KL and AL each within 10 of PL.
    - A word with fewer than 30 eligible items is reported with its n and not read.
  - **Predictions (three-hop), as amendment 56:** the chains ending in a recall (PPM, MPM, PMM, MMM) lose more than
    PPP; MPP and PMP do not. This is a replication on a new data seed.
- **B. Late-band positions for the 9B and Lightning.**
  - **Band, picked on dev:** the latest dev-profile window (amendment 42's profiles) where stated facts lose at most 10
    points and J++ M - K is at least 15. That gives the 9B L26-29 (81-91% depth; dev M - K +28, logit lens +22) and
    Lightning L33-39 (64-75%; dev M - K +50, logit lens +5).
  - Amendment 37 A's rule (81-94% depth) would put Lightning at L42-48, where the removal breaks stated facts too
    (dev above), so no position split could be read there. The 9B's pick coincides with the rule.
  - **Runs:** the all-token knock-out (paper10 / rotated / logit lens / its rotation), and question-only and
    bridge-mention-only (paper10 / rotated), on jsuite_v2_test_chat, the 15 facts words, each model's record v2 test
    competence (`scripts/queues/h200_depth_1025.sh`; run names carry the band).
  - **Readings as amendments 37 A and 41:**
    - a mode's M - K as a share of the band's all-token M - K, not read if that is below 15;
    - question >= 2/3: the dependence sits in the question at this depth;
    - bridge >= 2/3: it sits at the mention.
- **Order:** after amendment 56 D's DeepSeek chain, which holds both GPUs (`scripts/queues/h200_h0nb_1027.sh`).
  - GPU 0: the 27B (competence, numbers, three-hop), then the 9B's late band.
  - GPU 1: Lightning (competence, numbers, three-hop), the 9B's numbers (competence, knock-out), then Lightning's
    late band.

### Amendment 57 note 1 (Zach, 2026-10-27 12:40 UTC, before any run below): Muse through the dose grid and the position split

- **Why:** GPU 1 is free after amendment 57's chain, and GPU 0 will be after the 9B's late band. Of the models still
  cached, Muse is the only testable one with no dose grid, no size-matched control and no position split (scorecard
  cells "not run").
- **Seen when this was written:**
  - Muse's v2 knock-out at L36-42: M - K +60, rotated +3, logit lens +35.
  - Its earlier-dataset results (toy 7; natural and natplus mostly shared with the logit lens).
  - No dose, size-matched or position data for Muse.
- **A. Dose grid (GPU 1, now).** Amendment 54's grid at L36-42: removal sizes, then the test knock-out at K
  1/3/10/30/100/300 with rotated, size-matched and logit-lens controls, 150 random items per word (seed 0).
  - Script: `scripts/queues/h200_dose_muse_1027.sh`, a copy of h200_dose_1026.sh with Muse added to its models.
  - Readings: amendment 54 and note 1, computed by fig_neel.dose_readings.
  - Reported beside each: the logit lens at the same K. The question for Muse is whether any K gives a J-specific
    excess (J++ minus the larger of rotated and size-matched) that the logit lens does not also produce.
- **B. Position split (GPU 0, after the 9B's late band).** Question-only and bridge-mention-only knock-outs at
  L36-42 (paper10 / rotated), all eligible items, as amendments 37 A and 41 (`scripts/queues/h200_h0nb_1027.sh` pos
  steps).
  - Readings: a mode's M - K as a share of the all-token +60 (muse30_jsuite_v2_test_chat_ko_cand2_v1);
    question >= 2/3 means the question, bridge >= 2/3 means the mention.

### Amendment 57 note 2 (Zach, 2026-10-27 13:05 UTC, before any run below): Muse not run; clean-checkout reruns instead

- **Muse (note 1) did not run.** Its weights (meta-models/Muse-Glimmer-30B) are no longer cached; only its lens is.
  - Both jobs stopped at model load and produced no output.
  - Downloading the weights (about 60 GB, with 35 GB free) needs a cache drop. That needs Zach's OK, so it was not done.
- **Instead, the last check before calling a result positive:** amendment 57's new results rerun from the clean worktree
  /workspace/clean_bridge at HEAD, with the same commands. Run names carry "clean_", and each rerun is compared row by
  row with its run of record, as amendment 50 (`scripts/queues/h200_clean57_1027.sh`).
  - **GPU 0:** the 27B on jsuite_v2nb: competence on the 16 words, then the numbers and three-hop knock-outs.
  - **GPU 1:** the 9B's late band L26-29 (all-token, question-only, bridge-only, with the record v2 competence). Then
    the 9B on jsuite_v2nb's numbers (competence, knock-out).
  - **Expectation:** row-identical, as the 27B's and 9B's earlier clean reruns were. Any differing row is reported with
    its count and the rerun's headline.
- **Lightning is not rerun.** Its earlier clean rerun reproduced the headline but not every row, because its inputs
  differed (amendment 56 B).

### Amendment 57 note 3 (Zach, 2026-10-27 14:19 UTC, before any run below): Lightning's late band from the clean checkout

- **Seen when this was written:** note 2's 9B reruns, all row-identical to their runs of record (late band L26-29:
  14,100 / 8,460 / 8,460 rows; jsuite_v2nb competence 17,872 items and numbers 6,545 rows; every log-probability
  equal). The 27B's reruns are still running.
- **Run (GPU 1, free until about 16:00 UTC):** Lightning's late band L33-39 (all-token, question-only, bridge-only;
  its record v2 competence) from the clean worktree, still at 9722621. It is not moved while GPU 0's reruns use it.
  `scripts/queues/h200_clean57_1027.sh` late step, compared row by row.
- **Expectation:** row-identical. Amendment 56 B's determinism check gave identical rows for Lightning when the
  eligibility and batching were the same, and here they are.

### Amendment 57 note 4 (Zach, 2026-10-27 17:17 UTC, before any run below): Muse's runs move to Dan's queue

- **Approval (Zach, 2026-10-27 ~11:40 ET):** "Go ahead and also queue muse". This answers Dan's docs/shared/gaps.md:
  - his 45r runs may use this knock-out on Muse;
  - note 1's Muse runs may go on his queue.
- **Where:** Muse's weights are cached on Dan's box, not on ours. Note 1's two runs become job specs in his framework
  (jobs/c3/x57_dose_muse.yaml and jobs/c3/x57_pos_muse.yaml) with unchanged designs, run names and readings.
  - **Dose grid:** amendment 54's grid at L36-42, 150 per word (seed 0), BJ_GRAM_PROJ=1 as every other model's dose
    run. Then jsuite2_score and soft_score.
  - **Position split:** question-only and bridge-only at L36-42 (paper10 / rotated), all eligible items, QR projection
    as the record run.
- **What changes:** the hardware. These run on an H100, while the record Muse run (M − K +60) ran on our H200.
  - Each dose run compares its own conditions within itself, so the hardware change does not touch those comparisons.
  - The position shares divide by the record run's +60; a cross-hardware difference of a few rows would move a share
    by about 0.01.
- **Overlap:** Dan's x45r_ko_band_muse (the size-matched control at L36-42 on all items) ran already. The dose grid's
  top10_pcasize on 150 items per word is reported beside it; neither replaces the other.

### Amendment 57 note 5 (Zach, 2026-10-27 18:06 UTC, before any run below): Muse on our box after all

- **Why (Zach, 2026-10-27 ~14:00 ET):** "can you queue muse here? ... Just do the work on our box and stuff."
  - Note 1's Muse runs come back to our box.
  - The specs on Dan's queue (note 4) are marked do-not-enqueue on main, so the work is not done twice.
- **Space:** Muse's weights (meta-models/Muse-Glimmer-30B at pins.py's revision, 59.6 GB) need room; the box has
  33 GB free.
  - DeepSeek-V4-Flash's cache (149 GB) is dropped. Its pre-registered runs are all done and logged (amendment 56 D),
    and it can be re-downloaded.
  - It is dropped with /workspace/scratch/cache_drop.py, the tool used for Bolt, which deletes only the files no other
    model references.
- **Runs:** as note 1, unchanged, after a smoke on the largest K.
  - GPU 1: the dose grid at L36-42 (scripts/queues/h200_dose_muse_1027.sh dose:muse30).
  - GPU 0: question-only and bridge-only at L36-42 (scripts/queues/h200_h0nb_1027.sh pos steps).
  - Both use the record run's H200, so note 4's hardware caveat no longer applies.
- **Readings:** note 1's.

### Amendment 58 (Zach, 2026-10-27 22:05 UTC, before any run below): how good is each model, actually

- **Why:** at the 27 Oct drop-in, Neel doubted that open models can do three-hop recall and asked how good each model
  really is at our tasks, with shortcuts ruled out. A read-only audit of the stored competence runs (27 Oct) found:
  - three-hop chains with a read hop near chance for most models;
  - all-memory chains high through shortcuts;
  - number lookups near chance.
- **Plan (agreed with Zach, 27 Oct; each part gets its own note before it runs):**
  - a competence card per model and task;
  - the headline re-scored on clean subsets (CPU);
  - the knock-out on the never-named start;
  - a difficulty-matched hard read;
  - a capitals relation whose commonest answer is under 5%;
  - filler tokens and repeats;
  - later: knowledge conflict, an external shortcut-free two-hop set, a computed-entity bridge.
- **Changes to earlier claims, fixed now:**
  - Three-hop becomes a secondary analysis on Qwen 27B only, and only if it passes the competence bar of note 2.
  - The H0 numbers test is reported as inconclusive, except reporting a computed number where competence is high.

#### Amendment 58 note 1 (Zach, 2026-10-27 22:05 UTC, before the run): raw greedy replies to every item

- **What:** scripts/greedy_all.py. The model's greedy reply (up to 24 new tokens, unedited) to every item's whole question
  in jsuite_v2_test_chat: 5,370 fact, 1,007 three-hop and 703 number items, eligible or not.
  - Prompts are exactly the competence and knock-out prompts (tasks_v2.render: thinking off, "Answer:" prefilled).
  - Prompts of one length are batched without padding.
- **Models:** Qwen3.6-27B, Qwen3.5-9B, Nemotron 3.5 Lightning (smoke: 8 items per word on the 9B first).
- **Rule:** descriptive; raw text only. Scoring is note 2's, fixed before any reply is scored:
  - Strip one leading fixed phrase ("The answer is", "It is", "It's"), then whitespace and punctuation.
  - The reply is right if it then starts with the answer or one of its aliases (case-insensitive, accents folded).
  - Any other text before the answer, including reasoning, counts as wrong (Redwood's rule).
  - Alias tables are per relation, built from the candidate lists plus standard forms (adjective and noun forms,
    "Mammalia"-style class names). 50 replies per model are hand-checked against the rule; any change to the tables
    after that is logged.

#### Amendment 58 note 2 (Zach, 2026-10-27 22:40 UTC, before the run): filler tokens and repeats (Redwood's no-CoT tests)

- **Erratum to note 1:** jsuite v2 items use the "chat" framing (tasks_v2.render): one user turn with the passage, the
  question and NATURAL_CHAT_INSTRUCTION, thinking off, and no "Answer:" prefill. Note 1's prompts are these exact
  competence prompts; only its description of them was wrong.
- **What:** scripts/competence_variants.py, unedited accuracy under three prompt variants:
  - "none": the competence prompt;
  - "filler300": the question followed by the integers 1..300, then the instruction;
  - "repeat5": the question written five times.
- **Reads:** cand2 on the first generated token, and the greedy reply (24 tokens, scored by note 1's rule).
- **Set:** jsuite_v2_1_test_chat. Words:
  - never-named start: RM, RA, RN;
  - reference two-hop: PM, MM;
  - three-hop: all 8 chains;
  - numbers: all 12 words.
- **Models:** Qwen3.6-27B, Qwen3.5-9B, Lightning. Smoke first: 4 items per word on the 27B.
- **Rule:** descriptive. Reported per word and variant: accuracy with its 95% CI and the change from "none".
  - Three-hop and number cells are read with the real-composition share (accuracy − guess)/(1 − guess) ≥ 0.7 (Zach, 27 Oct).
  - Question: does content-free extra computation raise no-CoT competence on never-named two-hop, three-hop and number
    lookups, as Redwood found for frontier models?

#### Amendment 58 note 3 (Zach, 2026-10-27 23:05 UTC, before the run): answer-only removal

- **Why:** to test whether the headline is just the deletion of an answer that is linearly decodable at the bridge.
  The J++ lens reads the fact at the bridge's mention in most items, so the lens part could act by removing the
  answer's own directions rather than the entity pointer.
- **Conditions:** new in scripts/ablate_v2.py: ansJ, ansJ_rot, ansU and ansU_rot.
  - At every token and every layer of the model's band, remove the projection onto the span of the item's candidate
    answers' unit directions: the first tokens of every answer of its relation, both cases (cands2).
  - The span is the same at every position.
  - ansJ uses the J++ lens vectors at that layer; ansU uses the logit lens's (unembedding) directions.
  - "_rot" turns the removal vector by the same fixed random rotation as paper10_rot.
  - The rank is the number of candidate tokens in the dictionary, about 10-70 depending on the relation.
- **Items and models:** jsuite_v2_test_chat facts, all 15 words. Each model at its headline band, with the headline
  competence run and eligibility:
  - Qwen3.6-27B, L32-40;
  - Qwen3.5-9B, L12-16;
  - Lightning, L27-33.
  - paper10 is not rerun: its stored run on the same items is the comparison.
  - Smoke first: 4 items per word on the 9B.
- **Readings (M - K, bootstrap over bridges, as the headline):**
  - "Answer deletion explains most of it" if ansJ's M - K ≥ 0.5 × paper10's stored M - K, with ansJ_rot ≤ 10, in at least
    2 of 3 models. The "entity pointer" framing is then revised.
  - Otherwise the effect is not mostly the removal of the candidate answers' directions.
  - ansU is reported beside ansJ as the logit lens's version.

#### Amendment 58 note 4 (Zach, 2026-10-27 23:35 UTC, before any v3 run): jsuite v3

Note 3's v2 answer-only runs were cancelled before they started (Zach, 27 Oct, ~23:00 UTC); the test moves to v3.

- **Why:** the 27 Oct audit and Neel's feedback.
  - v2's described starts leak the answer through their cues.
  - Small answer sets: the commonest answer covered up to 42% of items.
  - Guessing by elimination.
  - The stated fact always agreed with memory.
  - The reading side was single-step.
- **Set:** data/tasks_v2/jsuite_v3_test_chat, built by scripts/jsuite_v3.py (seed 3001) from data/v3_bridges.json (scripts/v3_bridges_src.py).
  - **Bridges:** written by hand, with the 5 uncertain facts replaced and the rest checked by the author.
  - **Relations and bridges:** 234 bridges in 5 relations: people → nationality (63), cities → country (51), companies → country (40), landmarks → country (40), films → director (40).
  - **Answer balance:** no answer covers more than 5% of its relation (20+ answers per relation).
  - **Descriptions:** none names a place, nationality, language, people, food or answer-language title, or the answer.
  - **Excluded:** answers whose first tokens collide under any of the 5 tested tokenizers. They were swapped for other bridges.
  - **Not public:** the generated items stay out of the public repo (Redwood's request); the generator, tables and seed rebuild them exactly.
- **Starts:** P (made-up person), M (described, named once in passing), W (two passing mentions), R (never named), T (tracked),
  X (computed list position), Q / J (P as table / JSON), Y (counterfactual-bridge pairs of P level 1).
- **Finals:** P, K, M, A, N (as v2), plus:
  - H (hard read through a made-up anchor);
  - C, D, E, F (conflict: plain / attributed frame × neutral / "According to the notes" question; near or far counterfactual);
  - G (attributed, true).
- **Levels:**
  - 1 (3 entities, 2 filler sentences);
  - 2 (6 entities, 6 filler sentences);
  - 3 (12 entities, 20 filler sentences, the bridge's sentences in the first third).
- **Matrix:** scripts/jsuite_v3.py MATRIX; two renderings (rep 0 is run; rep 1 is held for replication).
- **Audit:** scripts/audit_v3.py, before any run; results/dataset_audit/jsuite_v3/. Every check passes:
  - absence and presence of the answer per final;
  - never-named;
  - the two-mention distractor;
  - the question never names the bridge or the answer;
  - conflict values;
  - counterfactual pairs identical except the bridge;
  - the computed position;
  - ids;
  - anchors;
  - first-token uniqueness for Qwen 27B, 9B, Lightning, Muse and Ministral.
- **Competence (rep 0; Qwen3.6-27B, Qwen3.5-9B, Lightning):**
  - (a) natural_v1 competence (whole, each hop alone, guess) on every K and M word (eligibility), plus RM;
  - (b) competence_variants "none" (cand2 and the greedy reply) on every word and the skip-the-bridge probes.
- **Eligibility (Zach, V4):** a scene counts if its K and M items (R: its M item) and each hop alone are right. Its
  other finals are scored on that scene, whatever their own correctness. Implemented as tasks_v2.eligible's optional
  scene_words, so existing runs are unchanged.
- **Knock-out matrix (rep 0, each model at its band):** paper10, paper10_rot, unembed10, paper10_pcasize, all words.
  - **Readings, fixed now:**
    - **Headline:** M − K ≥ 10 points with rotated ≤ 10, in at least 2 of 3 models. Primary on start P; the other starts reported.
    - **Hard read:** H's points lost under paper10 within 10 of paper10_rot, where H is difficulty-matched to M (unedited
      accuracy and median margin within M's range for that model). Otherwise "recall vs read" becomes "anything hard".
    - **Level 3:** the same rule for K and H at level 3.
    - **Conflict:** paper10 raises the share of answers giving the passage's (counterfactual) value by ≥ 10 points more
      than paper10_rot and paper10_pcasize, in at least 2 of 3 models. G vs K is reported as the attribution control.
    - **W vs M:** the guess-prompt accuracy on W, expected below M's (elimination removed); M − K reported on W.
    - **Y:** the share of Y items answered with the alternative bridge's value (counterfactual consistency, competence),
      against chance and the commonest answer.
    - **X:** read only where the real-composition share is ≥ 0.7.
    - **Formats (Q, J):** M − K and H as for P.
- **Ports to v3** (swap and pointer, answer-only removal, keep-own, position split, readout) and later tests (SOCRATES,
  monitoring) each get their own note before they run.

#### Amendment 58 note 5 (Zach, 2026-10-28 00:35 UTC, before any run below; no v3 knock-out or swap result seen): the ports to v3

- **Why (Zach, 27 Oct):** "port all the experiments over to our new v3 setup if it makes sense (do this carefully)".
  Each port keeps its v2 design, conditions and reading. Only these change: the set, the words v3 has, and note 4's
  eligibility.
- **Common to every port:**
  - **Set:** rendering 0 (jsuite_v3_test_chat).
  - **Eligibility:** each model's v3 competence run, with note 4's V4 scene rule over PK PM MK MM WK WM TK TM XK XM QK
    QM JK JM YK YM RM.
  - **Models and bands:** Qwen3.6-27B L32-40, Qwen3.5-9B L12-16, Lightning L27-33.
  - **Smoke first:** on the 9B, 2 items per word for every script, for the mechanics only.
- **Code (this commit):**
  - jswap, jswap_pointer, jswap_xrel and bridge_readout read v3's tables (scripts/jsuite_v3_tables.py) and words, and
    take v3's eligibility through jswap.v3_prompts.
  - On v3 only, the made-up-value parser accepts v3's display article ("a city in the Netherlands"). Without it, 3-9%
    of made-up values in cities, companies and landmarks went unparsed; with it, 100% of PP / PK / PM / PA / PN / TK /
    TM entities parse, checked on all v3 items.
  - v1 and v2 paths are unchanged.
- **1. Answer-only removal (note 3, moved here by note 4):**
  - **Conditions:** ansJ, ansJ_rot, ansU, ansU_rot, as note 3.
  - **Words:** PP PK PM PA PN MP MK MM MA MN TK TM WK WM WA WN RM RA RN.
  - **Comparison:** paper10 from the model's v3 knock-out matrix, on the same items.
  - **Reading:** note 3's ("answer deletion explains most of it" if ansJ's M − K ≥ 0.5 × paper10's, with ansJ_rot ≤ 10,
    in at least 2 of 3 models; primary on start P).
- **2. Swap (amendment 32):**
  - **Conditions:** swap, remove, swap_rot, swap_u, swap_comp, paste; every job.
  - **Words:** PP PK PM PA PN TK TM (v3 has no TP, TA or TN).
  - **Readings:** amendment 32's, on the memory finals PM PA PN TM, pooled and per word:
    - swap transfer ≥ 20 with a bootstrap interval above 0;
    - swap_rot and swap_u < 5;
    - PP and PK kept ≥ 80%.
- **3. Position split (amendments 36 and 57):**
  - **Conditions:** paper10 and paper10_rot under --positions bridge and under --positions question.
  - **Bands:** the headline band, and the deep band: 27B L52-60, 9B L26-29, Lightning L33-39.
  - **Words:** P, M, T and W starts × the finals above (no R: it has no mention).
  - **Measure:** each mode's paper10 M − K as a share of the knock-out matrix's all-position M − K at the headline band.
  - **Readings:** amendment 36's:
    - bridge-only, on P and T: < 1/3;
    - question-only, on M: ≥ 2/3;
    - P and T, question-only: ≥ 2/3 means re-retrieval from the question;
    - rotated < 10 in every mode;
    - not read where the reference M − K < 15.
- **4. What the mention carries (amendment 51, jswap_pointer):**
  - **Conditions:** neutral donor, own-word swap, timeline; 150 jobs per word (seed as v2); same words as 2.
  - **Readings:** amendment 51's:
    - swap_neutral ≥ 2/3 of swap means the J-part carries the entity whatever its context;
    - ≤ 1/3 means it depends on the passage;
    - not read if swap < 10.
- **5. Keep-own (amendment 55):**
  - **Conditions:** paper10, paper10_rot, paper10_keepown, paper10_keepown_rot; 150 items per word, seed 0.
  - **Band and words:** headline band; words as 1.
  - **Measure:** restored = 1 − (M − K under keepown) / (M − K under paper10).
  - **Readings:**
    - ≥ 0.75 kills C1 for that model;
    - ≤ 0.25 means the dependence is not the bridge's own word.
- **6. Cross-relation swap (amendment 47), redefined for v3:**
  - **Why redefined:** no two v3 relations share their entities, so v2's "other relation" cannot be built.
  - **The two contexts:**
    - "fact": the entity's own attribute is asked; K-final passages ("By nationality, D was Kenyan.").
    - "pfact": a made-up attribute about it is asked, with the same answer words; P-final passages ("The upcoming biopic
      casts a French actor as D.").
  - **Donors:** swap_srel takes D's J-part from another prompt of the item's own context, swap_xrel from one of the
    other.
  - **Not used:** mentions in M, A and N passages, which carry made-up-fact lures on other entities.
  - **Rows keep the donor prompt ids.** On CPU, the share of swap_xrel answers that equal D's made-up value in the
    donor passage is reported.
  - **Readings:** amendment 47's:
    - swap_xrel ≥ 2/3 of swap_srel on the memory finals means the J-part carries the entity, not the context's theme;
    - not read if swap_srel < 10.
  - **Status:** this is a different manipulation from v2's: a context about the entity versus a different relation. It
    is reported as a new test, not as a replication.
- **7. Bridge readout (descriptive):**
  - **Words:** PM, TM and PN, at the bridge's first mention.
  - **Readout:** J-lens and logit lens over the relation's candidates, every 2nd layer.
- **Not ported:**
  - **Probe swap:** it needs answers shared across many bridges, which v3's balance removes. The v2 result stands.
  - **Stays on v2:** the dose grid, the K sweeps, swap_ans, depth profiles, three-hop and numbers. v3 has no three-hop
    or number items.
- **Order and GPUs:** ports run beside the knock-out matrix. The models fit in memory side by side, and these runs are
  CPU-launch-bound.
  - **GPU 1:** 9B ports once its competence is written, then Lightning's, then the 27B's swap family.
  - **GPU 0:** the 27B's removal ports after its knock-out matrix.
  - **Priority within a model:** 1, 2, 3, 4, 5, 6, 7.

#### Amendment 58 note 6 (Zach, 2026-10-28 00:45 UTC, before any run below; no v3 knock-out result seen; the 9B's v3 competence seen): after the ports

Both GPUs are booked until about 08:00-09:00 UTC (the removal matrix, then note 5's ports). These runs follow, so no GPU
waits. Each was approved on 27 Oct as "later": the rendering-1 replication (note 4: "rep 1 is held for replication"),
then Muse and Ministral on v3, then Ministral's and Muse's cancelled note 1 / note 2 runs.

- **1. Rendering-1 replication (Qwen3.6-27B, Qwen3.5-9B, Lightning):**
  - **Data:** jsuite_v3r1_test_chat, the same bridges, starts, finals and levels as rendering 0, with its own draw of
    templates, filler, made-up values, anchors and entity orders.
  - **Runs:** natural_v1 competence on its K and M words plus RM (eligibility, note 4's V4 rule), then note 4's removal
    matrix: paper10, paper10_rot, unembed10, paper10_pcasize; all words; each model's band.
  - **Reading, fixed now:** the headline replicates in a model if, on rendering 1:
    - start P's M − K is ≥ 10 with rotated ≤ 10; and
    - it is within 10 points of rendering 0's.
  - Hard read, conflict and never-named are reported beside rendering 0's, as replications of direction.
- **2. Muse Glimmer 30B (L36-42) and Ministral 3 14B (L32-37) on v3, rendering 0:**
  - **Runs:** note 4's competence (a) and (b), probes, and removal matrix, unchanged.
  - **Reading:** note 4's readings per model. They are breadth: note 4's "2 of 3 models" bars stay on the three headline
    models.
- **3. Requeued (notes 1 and 2, unchanged):** Ministral's free-generation replies (greedy_all) and its filler/repeat
  run; Muse's filler/repeat run. Their free-generation run finished on 27 Oct.
- **Order (scripts/queues/h200_v3next_1028.sh), by priority:**
  - **Now, GPU 0:** the 9B's rendering-1 competence, beside the 27B's competence chain (about 20 GB beside 70 GB).
  - **GPU 1, after the ports queue A:** the 9B's rendering-1 removal matrix; rendering 1 for Lightning; Ministral v3;
    then Ministral's note 1 / note 2 runs.
  - **GPU 0, after the ports queue B:** rendering 1 for the 27B; Muse v3; then Muse's note 2 run.

#### Amendment 58 note 7 (Zach, 2026-10-28 01:16 UTC, before any run below; order only, designs unchanged)

- **Change:** rendering-1 replication moves to the end of the queues (Zach: "can't that wait to the end?"). Muse,
  Ministral and the requeued note 1 / note 2 runs come first; SOCRATES joins ahead of it once its design is approved.
- **Exception:** the 9B's rendering-1 removal matrix started at 01:11 on idle GPU 0 capacity (`h200v3n0b`) and runs to
  completion.
- **New queues:**
  - `h200v3nA-1028-0118`, GPU 1 after the ports: Ministral v3, its note 1 / note 2 runs, then rendering 1 for the 9B
    (skipped if done) and Lightning.
  - `h200v3nB-1028-0118`, GPU 0 after the ports: Muse v3 and its note 2 run, then rendering 1 for the 27B.
- **Update (01:24 UTC, Zach: "move rendering-1 runs to the very end"):** the exception is withdrawn. The 9B's rendering-1 run
  was stopped after 6 minutes; its partial output was moved to /workspace/scratch, unread. It runs from the end of GPU 1's
  queue with the others. Any later test (SOCRATES) is queued ahead of rendering 1.

#### Amendment 58 note 8 (Zach, 2026-10-28 02:35 UTC, before any removal-matrix result; no design change): the normal-equations projection for every v3 run from now

- **Why:** the v3 removal matrices ran at ~1 prompt/s, on track for 3-4 h each.
  - A benchmark on the box (m = 4,096 positions, d = 5,120, k = 10, double): the QR projection took 1,062 ms per call,
    the normal-equations projection 7.4 ms, with outputs equal to 3e-8.
  - The normal-equations projection is BJ_GRAM_PROJ=1, checked equal to ~1e-13 in amendment 52 note 1 and used in
    amendment 55's runs.
  - The 10-21 pad check had already found the removal bound by this per-position projection.
- **Done:**
  - Stopped (all ours): both removal matrices (27B at 565 of 12,306 prompts; 9B at ~520 of 10,189), the ports queues
    and the follow-on queues.
  - Partial outputs were moved to /workspace/scratch/killed_1028_gram, unread: the two matrices and the 9B's
    keep-own. Logs were renamed *.killed_gram.log.
  - Relaunched under the same job names with BJ_GRAM_PROJ=1. The matrices use note 4's arguments unchanged
    (scripts/queues/h200_v3ko_1028.sh); the queues are unchanged apart from the variable.
- **Already finished with QR:** the 9B's answer-only removal, position split (4 runs), swap and neutral-donor runs.
  They are kept; the two projections agree to float noise.

#### Amendment 58 note 9 (Zach, 2026-10-28 ~08:00 UTC, before any run below; mechanics smokes of nn_swap, nn_readout and the hop contrast ran first on the 9B, 2 items per word, outputs unread): never-named bridges

- **Why (Zach, 27-28 Oct; Neel's meeting):** the named-bridge results show how recall works once the model has an
  entity in hand. The paper's claim (Gurnee et al. 2026) and Neel's skepticism concern bridges the model must compute.
  v3's never-named start (RM) is that case: the question describes the bridge ("the novelist who wrote Arrow of God")
  and the passage never names it.
- **Seen when this was written:**
  - The 3 models' v3 competence: RM 40 / 54 / 66%. 36-46% of RM successes come with hop 1 alone wrong.
  - Clue-only questions right 74-82% (141 of 468 descriptions have a named clue).
  - The removal matrix: RM - MM ≈ 0 in all 3.
  - Every named-bridge port.
  - Nothing on never-named readouts or swaps.
- **Terms:** the "skip-the-bridge probes" are renamed **clue-only questions**. They are a behavioural test of whether
  the shortcut is available, not trained probes.
- **Models:** Qwen3.6-27B (L32-40), Qwen3.5-9B (L12-16), Lightning (L27-33); v3 rendering 0. Order: Lightning, the
  27B, the 9B (most eligible items first). Then Muse, then SOCRATES and Bolt (Zach). Ministral's note-6 removal matrix
  runs beside them (Zach: "if quick").
- **Items and eligibility (Zach 5a):**
  - Whole question right and both hops alone right: 112 / 135 / 196 RM items for 9B / 27B / Lightning (note 4's rule
    for R).
  - Every result is also split three ways (Zach 6a): clue-only question right (either of 2 wordings, Zach 8b), wrong,
    and no named clue.
- **Controls (Zach):** a control "passes" below 10 points throughout this note.
- **1. Composition contrast (ablate_v2 --kinds clean step1 step2; Zach 9a-12a):**
  - **Prompts:** RM's whole question and each hop alone, same passage. PM and MM are run the same way as references
    (PM's hop 2 is the same "What was the nationality of X?").
  - **Conditions:** paper10, paper10_rot, unembed10 at each model's band.
  - **Reading:** "composition needs the workspace beyond the final recall" if loss(RM whole) - loss(RM hop 2) ≥ 10 with
    the controls < 10. Hop 1's loss is reported beside it.
- **2. Readout (scripts/nn_readout.py; Zach 13a-16a):**
  - **Prompts and sites:** RM, MM and RM's hop 1 alone, read at the description's last token and at the final token,
    every 2nd layer.
  - **Lenses and candidates:** the J++ and logit lenses over the relation's bridges and its answers.
  - **Reading:** "bridge visible" if X is the top bridge at ≥ 3x chance at some layer at or before the layer where the
    attribute's top-1 rate peaks.
- **3. Swap (scripts/nn_swap.py; Zach 17-22):**
  - **Sites (Zach 17: a and b, plus the end of the question):**
    - the description's last token (main);
    - every description token;
    - the question's "?" token;
    - the prompt's last token.

    exp11 and exp14 read latent bridges at the last token from mid-late layers (27B L32-48), and swaps there worked
    only at L40-56.
  - **Donor D:** another bridge of the relation with a different answer and an eligible RM prompt of its own.
    - insert: D's slice from the neutral sentence;
    - latent: D's slice at the end of D's own description in one of its RM prompts (a computed bridge).
  - **Conditions:**
    - the transplant at k = 10, with rotated, random-subspace and logit-lens controls;
    - the dose at k = 30 and 100 (transplant and random-subspace; Zach: add);
    - the paper's clamp (X's and D's J-lens name vectors' coordinates exchanged at every position), with a
      norm-matched random-direction control.
  - **Layers (Zach 20: add the sweep):**
    - a sweep first, at the description's end and at the final token, on 80 items per word: windows of 4-8 layers
      across depth, transplant and random-subspace only;
    - then every condition at the band;
    - then at each site's best window. The best window is the window other than the band with the largest RM
      transplant, chosen by script.
  - **References (Zach 21: add):** MM swapped at its description and PM at its mention, in the same jobs. The named
    swap at the band is not rerun; the v3 port is the reference.
  - **Reading:**
    - transfer ≥ 20 with every control < 10 means "the computed bridge acts as a workspace entity";
    - ≤ 5 means "it does not";
    - in between is partial.
    - Reported beside PM's transfer at the same layers and site.
- **4. Trained linear probe for the bridge (Zach 7: is the bridge formed internally?):**
  - **Data:** activations at the description's last token, at the band and at the sweep windows' centres.
  - **Classifier:** a logistic regression over the relation's bridges.
  - **Leave-one-description-out:** both of an entity's descriptions appear across the M, W and R prompts, so for
    held-out description d the probe is trained only on prompts that use the other description (M and W starts, every
    final, and RM hop-1 prompts), and tested on RM prompts that use d.
  - **Use:** reported as the probe's top-1 accuracy (chance 1/k), and used to split the swap and contrast results into
    "bridge decoded" vs "not decoded".
  - **Order:** built and run after 1-3.
- **Not in this note:** SOCRATES (note 10), Muse, Bolt (with k 30 and 100), rendering 1 (last).

##### Amendment 58 note 9 addendum (Zach, 2026-10-28 ~08:00 UTC; before any run below. Seen: the never-named composition contrast for Lightning and the 9B, nothing else from note 9)

- **Dropped (Zach):** item 4, the trained linear probe. Decodable is not used, and it is not WorkspaceBench's standard.
  Its 3 jobs were cancelled before starting. scripts/nn_probe.py stays in the repo, unused.
- **Added (Zach: "add the 3 bridge tests"),** following WorkspaceBench's gating (Blank, Bhatia, Ong, Nanda): an item
  shows "uses the bridge" only if shortcuts fail, and the bridge is causal and necessary.
  1. **Wrong-bridge test (scripts/nn_wrongbridge.py, CPU).**
     - **Items:** RM items where hop 1 alone names a different bridge B' of the relation, with a different attribute.
     - **Measure:** is the whole question's answer B''s attribute ("own bridge"), B's, or other? Baseline: the model's
       rate of giving B''s attribute on the relation's other RM items.
     - **Reading:** "composes through its own bridge" if own-bridge minus baseline is ≥ 20 points with a 95% bootstrap
       interval (over bridges) above 0. A large "B's answer despite naming B'" share is read as a non-bridge route.
  2. **Final clause only (scripts/v3_finalclause.py → jsuite_v3fc_test_chat; competence_variants).**
     - **Prompts:** each RM question with the description cut to its role noun ("Which nationality was the
       novelist?"), same passage.
     - **Gate:** an item passes if this is wrong (cand2 and greedy).
     - **Gated subset:** eligible items whose guess prompt, clue-only questions (where a named clue exists) and
       final-clause-only question are all wrong. Note 9's swap and necessity results are reported on it beside all
       eligible items.
  3. **Necessity at the site (nn_swap --conds remove_k10 remove_k10_rot).**
     - **Edit:** the top-10 slice erased at the description's last token (and, separately, at the final token) at
       the band, with no donor. The control is the same-size change in a fixed random direction.
     - **Reading:** "the answer needs a bridge representation at the site" if RM loses ≥ 10 points more under
       remove_k10 than under remove_k10_rot. MM is reported at its description and PM at its mention (named: the 9B
       lost 47 at the mention in the v3 swap run).
- **Runs:** scripts/queues/h200_nnadd_1028.sh, per model after its note 9 queue. The wrong-bridge test runs now (CPU).

#### Amendment 58 note 10 (Zach, 2026-10-28 ~09:00 UTC, before any run below; a 2-item mechanics smoke ran first, unread): the paper's decomposition as the unifying frame; Bolt, targeted

- **Why (Zach, 28 Oct: "go ahead with it all"):**
  - Both tracks' tools are cells of one decomposition, the paper's (Gurnee et al. 2026: 61% / 28% / 6% for the J-space
    part / the remainder / the remainder with J-space clamped).
  - Take the real change at the entity's site (D's state from another prompt), split it into its lens part and the
    remainder, and measure each part's effect.
  - My swap is the lens-part cell; Dan's remove-from-the-patch is the remainder cell.
  - The split is run on the same v3 items for recalled vs stated answers and named vs never-named bridges.
- **Seen when this was written:** note 9's sweeps and the 9B's band results (the never-named site exists; a computed
  bridge's slice partly carries its entity). Nothing on this decomposition.
- **Conditions (scripts/nn_swap.py):** the patch Δ = h_D - h_X at the site, at every band layer. S is the span of the
  union of X's and D's top-10 J++ atoms there (≤ 20 dims, one subspace for every cell).
  - full: h_D;
  - lens: h_X + P_S Δ;
  - rem: h_X + Δ - P_S Δ;
  - remfix: the remainder, with the site's lens part held at its clean value (h_D - P_S h_D + P_S h_X,clean);
  - lensrand: the lens cell over a fixed random 20-dim subspace (control).
- **Donors:** insert (D from the neutral sentence) and latent (D's own never-named description end).
- **Items:**
  - RM: all eligible.
  - References, capped at 150 per word (seeded): MM, PM (named, recalled) and PK (named, stated).
  - Sites: the description's or mention's last token, and the whole span.
- **Models and layers:** the 9B at L12-16; the 27B at L32-40 and its best window L24-31; Lightning at L27-33 and its
  best window L21-26. The best windows come from note 9's sweeps.
- **Readings, fixed now (per model, word and site; not read if full < 10):**
  - "Travels through the workspace" if lens ≥ 2/3 x full and remfix ≤ 1/3 x full, with lensrand < 10 (the paper's
    pattern).
  - "Around it" if rem ≥ 2/3 x full.
  - Otherwise "mixed".
  - Expected: PM through, PK flat (lookups stay). RM is the question.
- **Order:**
  1. After each model's note 9 jobs, this decomposition.
  2. Muse's held v3 runs (competence variants, probes, removal matrix, filler/repeat).
  3. Bolt, targeted.
  4. Rendering 1, last.
- **Bolt (Zach: "don't skip it"; benchmarks compared first):**
  - Bolt is much stronger at reasoning (GPQA 88.8 vs 75.6) but only modestly at knowledge (AA-Omniscience 21.8 vs
    16.6), and ≈ Lightning on our v2 tasks.
  - It runs ~5x slower here, on both GPUs, so it is targeted. v3 competence on RM and its hops (eligibility); then
    note 9's never-named swap at its v2 band L42-53, k = 10 / 30 / 100 with every control, references capped at 80.
  - Disk: Bolt is ~150 GB and 125 GB is free. Ministral's (27 GB) and Muse's (56 GB) caches are dropped (Zach's OK,
    28 Oct) after Muse's runs end. Ministral's requeued note 1 / 2 runs are dropped with it.

##### Amendment 58 note 10 addendum (Zach, 2026-10-28 ~11:35 UTC; before any Bolt run. Seen: the 9B's and Lightning's decompositions, the 27B's not)

- **Fix to Bolt's queue.** As first written (h200_end_1028.sh, bolt mode), Bolt's competence and swap ran on RM only.
  That gave no references, against this note's "references capped at 80". Under --scene-words RM, a reference's
  scene (which holds no RM item) would also pass unchecked. Replaced before it started, under the same job name
  (scripts/queues/h200_end2_1028.sh):
  - competence on RM, MM and PM (about 40 min on Bolt instead of 12);
  - note 9's swap words RM MM PM, with MM and PM capped at 80 (seeded);
  - eligibility by the scene rule over RM MM PM: a scene passes when its own items of those words are right. PK and MK
    are not required, as they are under V3_SCENE for the other models: a slightly looser filter for Bolt's references,
    stated where they are reported.
- **Readings script:** scripts/nn_decomp_read.py applies this note's fixed rule to each decomposition run (writes
  results/nn_swap/RUN/readings.json). It reproduces the 9B's and Lightning's readings already reported.

#### Amendment 58 note 11 (Zach, 2026-10-28 ~18:45 UTC, before any run below; a mechanics smoke ran first on the 9B, 2 items per word: its rows were seen only as the scorers' mechanics check, n = 2, uninformative): bridge or answer; composition failures

- **Why (Zach, 28 Oct, on the plan: bridge vs answer with the layer-timing sweep; failures with readout and repair; Bolt as overnight filler; the second-wording replication of notes 9-10 moved to the very end):**
  - At the description's last token, where note 9 swaps the never-named bridge, the J++ lens also reads the answer:
    - top-1 9B 44-50% (chance 3.4%), 27B 64-68%, Lightning 53-64%;
    - the bridge's top-1 is 35-41 / 40-50 / 32-37% (chance 2.0%).
  - So note 9's transfer could be the answer moved rather than the bridge: the paper's "smuggled-in answer" confound, and what Neel's own replication found (answer swaps dominate).
  - paper10's lens part never picks the atoms of the model's own top-10 answer tokens. But other answer forms and nearby words can enter it, and atoms are not orthogonal.
  - The paper does not explain multi-hop failures. The 9B / 27B / Lightning have 51 / 46 / 65 RM items whose hop 1 and hop 2 alone are right and whose whole question is wrong (cand2; hop 1 by its generated name, as eligibility).
- **Seen when written:** notes 9-10's results, the readout above, and the counts of the composition split. Nothing from the conditions below.
- **1. Bridge or answer (scripts/nn_swap.py, new conditions):**
  - A is the span of the J++ atoms of every first token of every answer in v3: all relations, aliases too, with and without a leading space, as written and lowercased (477 tokens).
  - C is the span of as many fixed random atoms (seed 6100).
  - {src}_k10_noans: the transplant with no answer in it. Atoms are never chosen from A, and the change is projected off A. {src}_k10_noansctl: the same with C in place of A.
  - {src}_ans: the answer alone, h_X + P(h_D - h_X) over X's and D's own answer atoms. {src}_ansctl: the same over as many of C's atoms.
  - remove_k10_noans: the site's removal without its answer part.
  - src: insert (D from the neutral sentence) and latent (D's own computed bridge).
  - **Runs:** each model's band (9B L12-16, 27B L32-40, Lightning L27-33), at the description's last token; RM all eligible; MM and PM capped at 80 (seeded).
    - Seed 0 (notes 9-10's donors): insert_k10 and latent_k10 (a determinism check against note 9's run), and the new conditions.
    - Seeds 1 and 2 (new donors, --seed): insert and latent k10 with _rand, _rot and the new conditions; remove_k10, remove_k10_rot, remove_k10_noans.
  - **Reading** (scripts/nn_ans_read.py; RM, per model and donor, rows pooled over the 3 seeds; not read if k10 < 10):
    - "the bridge carries it" if noans >= 2/3 of k10;
    - "the answer carries it" if noans <= 1/3 of k10 and noansctl >= 2/3 of k10;
    - otherwise "mixed".
    - The answer alone "suffices" if ans >= 2/3 of k10 with ansctl < 10. It is reported beside, not as a verdict on the bridge.
    - Necessity without the answer: the kept share under remove_k10_noans, beside remove_k10 and remove_k10_rot.
    - MM and PM are reported the same way.
- **2. Timing (the paper's control; nn_swap --sweep, seed 0):**
  - Windows: note 9's sweep windows (9B 4-7, 8-11, 12-16, 17-20, 21-24, 25-28; 27B 8-15, 16-23, 24-31, 32-40, 41-48, 49-56, 57-62; Lightning 6-10, 11-15, 16-20, 21-26, 27-33, 34-39, 40-45, 46-50).
  - Conditions: insert_k10, insert_k10_noans, insert_ans, latent_k10, latent_k10_noans, latent_ans, insert_k10_rand.
  - Items: RM and PM, 80 per word (seeded).
  - **Reading:** each condition's onset is the first window with transfer >= 10. "The bridge acts before the answer" if noans's onset is at least one window earlier than ans's, per donor. (The paper: intermediate swaps act a median ~17% earlier in depth than answer swaps.)
- **3. Composition failures:**
  - **Items:** RM items with hop 1 and hop 2 alone right, split by the whole question into ok (112 / 135 / 196) and fail (51 / 46 / 65).
  - **a. Readout** (nn_readout --items composition; per-item ranks written):
    - What is read: the J++ lens and the logit lens, the bridge and the answer, at the description's end and the final token, every 2nd layer.
    - Reading (scripts/nn_fail_read.py), at the description's end: each item's top-1 share over the band's read layers. "The bridge is missing in failures" if ok - fail >= 10 points with a 95% bootstrap interval over bridges above 0 (J++). The same is applied to the answer, with the logit lens reported beside.
  - **b. Repair** (nn_swap --items fail; the band, the description's last token):
    - Conditions:
      - repair_k10: X's own lens part, from the neutral sentence about X;
      - its controls, repair_k10_rand and repair_k10_rot;
      - repair_k10_noans;
      - repair_full (the whole neutral state; a ceiling);
      - insert_k10: another bridge's lens part (entity-specific control).
    - Fix rate: the share answering X's answer.
    - Reading:
      - "writing the bridge into the workspace repairs composition" if repair_k10 minus the largest of its controls (rand, rot, insert_k10's rate of X's answer) is >= 20 points with a 95% bootstrap interval over bridges above 0;
      - "through the bridge, not the answer" if repair_k10_noans >= 2/3 of repair_k10.
- **4. Bolt (overnight filler only, after 1-3, if both GPUs are free):**
  - Note 9's sweep: insert_k10 and insert_k10_rand; RM, MM, PM at 80 per word; windows of 6 from L6 to L83; scene words RM MM PM (note 10 addendum).
  - Reading: a window where PM's transfer is >= 20 with random < 10 is "a window where Bolt's lens part carries a named bridge". RM's transfer there is read by note 9's rule.
- **Order:** 1 and 3a first (27B on GPU 0; 9B, then Lightning, on GPU 1), then 2, 3b, and 4 overnight. The second-wording replication of notes 9-10 comes at the very end (Zach).

##### Amendment 58 note 11 addendum (Zach, 2026-10-28 ~19:05 UTC; before any run below. Seen: item 1's band results pooled in all 3 models, item 3a's readout on the 9B and 27B, and this addendum's mechanics smoke, 2 items)

- **Why:** item 1 reads "mixed" in all 3 models, with "bridge" nowhere.
  - The answer-free swap keeps 1-2% of k10 (9B +0.3 of +40.5; 27B +0.5 of +30.1; Lightning +0.2 of +14.5), named bridges too.
  - But the same-size random scrub (477 atoms) also cuts 61-72% (keeps 39 / 39 / 28%), so it is too blunt to separate "the answer" from "a big cut into J-space".
- **Added (Zach: before the Bolt sweep):** the same rule at two narrower scrubs. Each is applied per item: atoms are never chosen from the scrubbed rows, and the change is projected off them. Each has as many fixed random atoms (C, seed 6100) as its control.
  - noansrel: the item's relation's answers (every form of every answer in its answer_vocab).
  - noansown: X's and D's own answers only.
  - Conditions: insert and latent k10_noansrel, _noansrelctl, k10_noansown, _noansownctl; remove_k10_noansrel; remove_k10_noansown.
  - Runs: note 11's three donor seeds, each model's band (scripts/queues/h200_n11b_1028.sh; runs {P}nn_ans2_L{band}_s{seed}_v1).
- **Reading (scripts/nn_ans_read.py, rows pooled with item 1's runs; fixed now):** per scrub, word and donor, item 1's rule. "Bridge" if scrub >= 2/3 of k10. "Answer" if scrub <= 1/3 of k10 and its control >= 2/3 of k10. Otherwise "mixed".
- **Order:** after items 2 and 3b on each GPU; then the Bolt sweep (item 4); the second-wording replication last.

#### Amendment 58 note 12 (Zach, 2026-10-28 ~19:40 UTC, before any split or run below): the relation after the bridge

- **Why (Zach, 28 Oct: "make it so the relation comes after whenever possible"; targeted, not everything; primary models 27B, 9B, Lightning, Bolt):**
  - Note 11 found every swap, removal and repair effect at the description's end runs through answer directions.
  - Most questions name the relation first ("Which nationality was the novelist who wrote Arrow of God?"), so the model can fetch the answer while it reads the description.
  - The test is to name the relation after it ("The novelist who wrote Arrow of God was of which nationality?").
- **Seen when written:** note 11's results (band, sweeps, repairs, failure readouts; the narrower scrubs not yet), the order counts (rendering 0 RM: 162 relation-after, 306 before), and rendering A's construction check. No result has been split by order.
- **1. The split (CPU, now):**
  - Note 11's runs on rendering 0 are re-read on the relation-after items alone and the relation-before items alone (nn_ans_read.py / nn_fail_read.py --order).
  - **Reading** (per model; 3 seeds pooled; the insert donor; RM):
    - (a) "Precomputed when the relation comes first" if, among composition successes, the answer's J++ top-1 at the description's end (band layers) is >= 10 points lower on relation-after items than on relation-before ones, with a 95% bootstrap interval over bridges above 0.
    - (b) On relation-after items:
      - "the bridge carries it when the answer can't be precomputed" if (a) holds and the answer-free swap keeps >= 1/3 of the normal swap;
      - "the lens part at the bridge carries its answer-relevant attributes whatever the order" if the answer-free swap keeps < 1/3.
    - Removal, repair, the failure readout and PM are reported split the same way. The subsets are small (about a third of items), so this is a first look; rendering A is the test.
- **2. Rendering A (scripts/v3_relafter.py → jsuite_v3ra_test_chat):**
  - Rendering 0's RM, MM and PM items, with the question, hop 2 alone and the guess question re-rendered by the relation's relation-after template (q2M[2]). Passages, ids, hops and vocabulary are unchanged (1,638 items: 1,079 re-rendered, 559 already relation-after). Added to build_v3.py.
  - **Runs** (scripts/queues/h200_ra_1028.sh; 27B L32-40, 9B L12-16, Lightning L27-33; Bolt after its sweep):
    - competence on RM MM PM (scene words RM MM PM, as Bolt's in note 10's addendum);
    - the composition readout (successes vs failures; bridge and answer);
    - note 11's band conditions at the description's last token on donor seeds 0 and 1: k10 with rand, rot; noans, noansrel, noansown with their controls; ans, ansctl; insert and latent; removal k10, rot, noans, noansrel, noansown;
    - note 11's repair on composition failures;
    - note 10's decomposition at the band (last token).
  - Bolt: competence on A, then the same at the window its sweep (note 11 item 4) finds by note 11's reading. If none, the readouts plus insert/latent k100 and the clamp at L42-53.
  - **Readings:**
    - note 11's (bridge / answer / mixed per scrub; repair; failure readout) and note 10's, on rendering A;
    - plus (a) above, read as rendering A vs rendering 0 on the same items (answer readability at the description's end, successes).
    - The headline question: on rendering A, does the answer-free swap (any scrub) keep >= 1/3 of the normal swap?
- **Not rerun:** the removal matrix, ports, conflict, hard read, and Muse / Ministral (question order does not bear on them). Rendering A stands in for the second-wording replication of notes 9-11 (Zach: "at the very end").

#### Amendment 58 note 13 (Zach, 2026-10-28 ~20:30 UTC, before any run below; a mechanics smoke ran first on the 9B (n = 3 MP items, 4 clamp items; rows seen only as the scorer's mechanics check, uninformative)): the latent first hop into an in-context second hop; the clamp's break-test

- **Why:**
  - Notes 11-12 found the J-space content that matters at a bridge is its remembered answer, whatever the question order.
  - Neel's explanation for his own null ("the dataset … had pairs like France and Paris, which were linearly related") also covers ours: a person's nationality is a salient remembered attribute.
  - The test without a remembered answer: a second hop to an arbitrary fact stated in the passage.
  - Rendering 0's MP items do this. The question describes the bridge; the passage gives each scene entity a made-up value ("The upcoming biopic casts a Swedish actor as Achebe. … a Mexican actor as Nobel.").
  - A swap at the description's end then has separable outcomes: D's passage value (the lookup followed a swapped-in identity), D's remembered attribute (D's memory bundle), or no change.
- **Seen when written:** notes 9-12's results, and the removal matrix's start-M cells. Under paper10, final P loses 12 / 13 / 5 (rotated 7 / 2 / 4) vs final M 56 / 65 / 50 (9B / 27B / Lightning). MP competence, and anything below, unseen.
- **Data:** scripts/v3_mp.py → jsuite_v3mp_test_chat (468 MP items; hop 2 is the passage lookup with the bridge named; every scene entity's passage value parsed and checked).
- **Runs** (scripts/queues/h200_mp_1028.sh; 9B L12-16, 27B L32-40, Lightning L27-33):
  - **1.** Competence on MP (words MP, scene words MP).
  - **2.** nn_swap on MP at the description's last token, donor seeds 0 and 1.
    - D: another entity of the same passage, whose passage value and remembered attribute both differ from X's passage value (and from each other).
    - Conditions: insert_k10, its controls _rand and _rot; insert_k10_noansrel; insert_k100; note 10's decomposition (full / lens / rem / remfix / lensrand, insert); necessity at the site (remove_k10, remove_k10_rot).
    - Classes: kept (X's passage value), donor (D's passage value), third (D's remembered attribute), xmem (X's remembered attribute), other.
  - **3.** The clamp's break-test on rendering 0's RM / MM / PM at the band, seed 0: clamp, clamp_null, and clamp_noans. clamp_noans is the clamp with X's and D's name vectors first made orthogonal to every answer direction (A, note 11).
- **Readings (scripts/nn_mp_read.py; nn_ans_read.py; fixed now):**
  - **MP, insert_k10, rows pooled over the 2 seeds:**
    - "the J-space carries the computed identity the lookup uses" if D's-passage-value share is >= 10 points above the larger control (paired, 95% bootstrap over bridges above 0) and above D's-attribute share;
    - "the J-space carries D's memory bundle" if D's-attribute share is >= 10 points above the larger control (interval above 0) and above D's-passage-value share;
    - "the identity the lookup uses lives outside the lens part" if neither, while full_insert moves >= 20 to D's passage value;
    - note 10's decomposition read on the D's-passage-value share.
    - "the lookup needs the lens part at the site" if kept under remove_k10_rot minus kept under remove_k10 is >= 10 (interval above 0).
  - **Clamp:** "the name coordinates carry something beyond the answer" if clamp_noans transfers (donor − third, RM) >= 10 with clamp_null < 10. "Not beyond the answer" if clamp_noans <= 1/3 of the clamp.
- **Order:** after rendering A on each GPU (27B on GPU 0; 9B, then Lightning, on GPU 1).

##### Amendment 58 note 13 addendum (Zach's OK pending; written 2026-10-28 ~20:40 UTC, before any MP swap result exists. Seen: the 9B's MP competence only)

- **Proposed:** note 13's MP readings are also made on the four relations where every passage entity shares the description's role noun (cities, companies, films, landmarks: 342 of 468 items).
  - In people items (126), the other entities have different roles, so the role noun alone ("the actor cast as the novelist") can pick the bridge without resolving the description.
  - The 9B's competence on the four relations: guess 31% (chance 33%); both hops right and whole right 217; both hops right and whole wrong 55.
- **If Zach approves:** the shared-role reading is primary, and the all-items reading (as note 13 fixed it) is reported beside it. If not, the all-items reading stays primary, with the shared-role one beside it.
- **Scoring:** scripts/nn_mp_read.py --relations cities companies films landmarks.

#### Amendment 58 note 14 (Zach, 2026-10-28 ~22:15 UTC, before any run below; a mechanics smoke ran first on the 9B with small limits (n = 2 per cell, seen only as the scorer's mechanics check); its first tries failed on the controls sharing the main set (moved to their own set) and on v3's eligibility pool (skipped for v4)): jsuite_v4, where the latent bridge must be used; readable vs used

- **Why (Zach, 28 Oct: "focus on latent multihop composition — the model computes the bridge internally and USES that bridge to compute the answer"; "what info is the lens actually surfacing wrt actual model latent computation?"):**
  - Notes 9-13 never showed bridge use. In recall items the answer comes with the entity's bundle at the description, every causal effect there is the answer's content (notes 11-12), and even the paper's clamp works only through answer directions (note 13, 9B).
  - v4 makes the bridge necessary. The answer is an arbitrary value the passage binds to each of six same-role entities.
  - The 9B's note 13 MP result showed the description's last token at L12-16 is not where a lookup's bridge travels (even the whole state moved ~5%). So v4 maps where it does, before asking what the lens sees there.
- **Seen when written:** note 13 on the 9B (MP band, clamp break-test) and the 27B's MP band (lens-part swap → D's passage value +6.6 [4.0, 9.5], below the bar; D's memory 0), v4's construction audit, and the smoke's mechanics. No v4 model output.
- **Data (scripts/jsuite_v4.py, seed 4001 → jsuite_v4_test_chat (MP, MM; sha 8ef8e386…) and jsuite_v4ctl_test_chat (H1, RG, RO;
  sha e09fa7c8…), in docs/v4_sha256.txt; Zach's design answers, 28 Oct):**
  - 874 scenes. Each scene has six entities of one relation sharing a role noun (people: "the person who …"), and a made-up value per entity from the relation's answer vocabulary. A value is never the entity's own attribute and never X's.
  - Two binding relations, one per wording. The bridge's fact is rotated through the six positions.
  - Name-stem overlaps are excluded. Every entity is mentioned exactly once, and X's attribute is absent from the passage (audit: all 874).
  - Words: MP (the lookup), MM (its recall twin, same passage and description), H1 (hop 1 closed book), RG (recognition among the passage's entities), RO (role noun only).
- **Gate (scripts/nn_swap.v4_split):**
  - ok: H1 right (cand2 or the greedy reply with the bridge's other names), hop 2 alone right, whole right, the no-description guess wrong.
  - fail: the same but the whole wrong.
  - Controls reported per model: RG vs H1 (recognition vs recall), RO and the guess vs chance 1/6.
- **Readout map (nn_readout --items v4):** the J++ lens and the logit lens rank the bridge (among the relation's bridges) and the item's own answer, at the description's end and the final token, every 2nd layer, for ok vs fail, MP and MM.
- **Stage 1, the counterfactual map (nn_swap --items v4ok, conditions full_cf and lensrand_cf):**
  - D: another scene entity whose remembered attribute differs from X's value and D's own value; for MM, D's attribute also differs from X's.
  - The counterfactual prompt is the same passage with the question about D (one of D's descriptions).
  - Its states are patched into X's run at the description's last token (last), the description's tokens right-aligned (span), or the final token (final), at every layer window. Windows: 27B 0-7 … 57-63; 9B 0-3 … 29-31; Lightning 0-5 … 46-51.
  - Donor seeds 0 and 1.
- **Stage 2:** note 10's decomposition (full, lens, rem, remfix, lensrand; S = X's and D's top-10 J++ atoms) at every cell meeting reading 1. If a word has no such cell, at its largest full_cf cell (descriptive).
- **Readings (scripts/nn_cf_read.py; primary: pairs whose counterfactual prompt the model answers with D's answer; all pairs beside):**
  1. "The bridge lives at (site, window)" if full_cf moves >= 20% of answers to D's answer (MP: D's passage value; MM: D's remembered attribute), lensrand_cf < 10%, and full − lensrand has a 95% bootstrap interval over bridges above 0.
  2. At such a cell, "through the lens part" if lens >= 2/3 of full, remfix <= 1/3 of full and lensrand < 10. "Around it" if rem >= 2/3 of full. Otherwise "mixed".
  3. **Readable vs used:** the readout map's J++ bridge top-1 at the hit cells' sites and layers, ok vs fail (the readout reading of note 11 applies: >= 10 points, interval above 0), compared with where reading 1 holds.
- **Comparison:** MP (the bridge must be used) vs MM (recall; notes 11-12's setting) on identical scenes and descriptions.
- **Models:** the 27B, 9B and Lightning overnight (scripts/queues/h200_v4_1028.sh). Bolt on Thursday: competence and readout, and the map if time allows.

##### Amendment 58 note 14 addendum (Zach, 2026-10-28 ~22:20 UTC; before any map result: the first map run failed at its last window)
- **Windows corrected.** The J-lens has no layer for the model's last block, so each map's last window ends one layer earlier: 27B 57-62, 9B 29-30, Lightning 46-50. Everything else is unchanged.
- **Order.** The runs go in seed-major order (Zach: the full seed-0 map first; scripts/queues/h200_v4b_1028.sh), with the same runs.

##### Amendment 58 note 15 (Zach, 2026-10-29 ~00:40 UTC; before any result): on v4, is the recall twin's lens part the bridge or the answer? (Dan's 51.12 rule)
- **Why.** Dan's 51.12 (unverified) finds the lens effect at the bridge is the answer on our v3 passages, and the entity on his locker scenes, whose answers are digits the lens mostly cannot read. v4's answers are words. At the 9B's final token (L21-24, L25-28) the recall twin (MM) needs note 10's lens part (rem 12.5 of full 27.9; 11.3 of 45.0) but the lens part alone moves little (1.7; 6.2).
- **Items.** v4ok, MM, donor seeds 0 and 1; primary: cf_ok pairs (note 14).
- **Cells.**
  - 9B: MM at last L4-7, L8-11, L12-16 and final L21-24, L25-28. These are note 14's stage-1 hits, minus the window ending at the lens's last layer, where the answer is formed.
  - 27B: every MM stage-1 hit at sites last and final, minus its last window (57-62).
- **Definitions.** Δ = h_D − h_X at the site. S = note 10's lens part. A = an answer set. C = as many of SEED_CTL's fixed random atoms. R = note 10's fixed random 20-dim subspace.
- **Arms (scripts/nn_swap.py):**
  - full_cf;
  - rem_cf (arm 1: without the lens part);
  - remrand_cf = h_X + Δ − P_R Δ (the random twin of arms 1 and 2);
  - remkeep{A}_cf = h_X + Δ − (I − P_A) P_S Δ (arm 2: without the lens part, its answer component kept);
  - noa{A}_cf = h_X + Δ − P_A Δ (arm 3: without the answer directions only);
  - noa{A}ctl_cf, the same with C in place of A.
- **Two answer sets (Zach: both).**
  - own: X's and D's own answers (note 11's narrowest scrub; Dan's A).
  - rel: every answer of the item's relation (note 11 addendum's noansrel).
- **Measures (donor shares, cf_ok pairs).**
  - e1 = (remrand − rem) / full.
  - e2 = (remrand − remkeep) / full.
  - e3 = (noactl − noa) / full.
  - 95% cluster bootstrap over bridges.
- **Rule: Dan's 51.12 rule, used verbatim (his "entity" read as "the bridge"), per model, cell and answer set.** Point estimates decide.
  - "The lens part is the bridge" if e2 >= 0.7 e1 and e3 <= 0.10.
  - "The lens part is the answer" if e2 <= 0.3 e1 and e3 >= 0.5 e1.
  - Otherwise "mixed". If e1 <= 0: "can't tell".
- **Readout check (Dan's amendment), reported first.**
  - The lens rank, over the letter tokens, of X's answer at h_X and D's answer at h_D, at the site and the band's first layer.
  - "The answer is not read at the site" if both rank > 50 on >= 90% of pairs.
- **Decisive cells.** The final cells, where the recall needs the lens part. The description-end cells are reported beside them.
- **Scorer.** scripts/nn_cf_read.py (note15_own, note15_rel).

##### Amendment 58 note 16 (Zach, 2026-10-29 ~00:40 UTC; before any result): the latent bridge with Dan's lens part
- **Why.** With note 10's lens part (X's and D's top-10 J++ atoms), the 9B's lookup bridge at the description's end goes around the lens (L4-7: lens 2.6 of full 26.0). Dan's lens part is fit to the change itself, so it catches any lens-readable part of the change. At his named bridge word (9B, L2-6) it alone moves both readers 0.60-0.96 (51.10, unverified). Does the latent bridge stay outside the lens under his definition?
- **Items and seeds.** As note 15; 9B only (Zach).
- **Cells.**
  - Site last, MP and MM, L4-7 and L8-11.
  - Positive check: final MM L29-30, where note 10's lens part alone moves 57.2 of 89.4.
- **Lens part (Dan's x0 / x45p).**
  - J = the signed OMP fit, k = 25, of Δ over the unit J++ vectors of the letter tokens and the ten digits (exp04_brew_parts.signed_omp; JLens.vectors), at each band layer.
  - Its random twin: Δ's projection on the first k columns of rotation(d, 888 + layer), k per row so it keeps the same share of ||Δ||² (Dan's random_subspace_part, copied).
- **Arms.** full_cf, jpp_cf (h_X + J), jpprand_cf, nojpp_cf (h_X + Δ − J), nojpprand_cf.
- **Readings (donor shares, cf_ok pairs).**
  1. Positive check: at final MM L29-30, jpp − jpprand >= 0.5 full. If it fails, readings 2 are void.
  2. Per cell (full >= 20):
     - "the bridge is in Dan's lens part" if jpp − jpprand >= 0.5 full (his write bar) and nojpprand − nojpp >= 1/3 full;
     - "outside it" if both are < 1/3 full;
     - else "mixed".
  3. Reported beside: the mean share of ||Δ||² that J holds.
- **Scorer.** scripts/nn_cf_read.py (note16).

##### Amendment 58 note 15 addendum (Zach, 2026-10-29 ~00:50 UTC; before any addendum result; note 15's first cell, final MM L21-24 seed 0, had been read: "answer")
- **Why.** Note 10's random control is a fixed random 20-dim subspace, which holds a tiny share of the change. Dan's control is a random part holding the same share of the change as the lens part. For "the recall needs the lens part", his is the right null (Zach: adopt it).
- **Arms (scripts/nn_swap.py), at note 15's 9B cells (MM at final L21-24, L25-28 and last L4-7, L8-11, L12-16), donor seeds 0 and 1, cf_ok pairs:**
  - full_cf, lens_cf, rem_cf (note 10);
  - lensshr_cf = h_X + Rs;
  - remshr_cf = h_X + Δ − Rs.
  - Here Rs is Δ's projection on the first k columns of rotation(d, 888 + layer), k per row chosen so it holds P_S Δ's share of ||Δ||² (Dan's random_subspace_part).
- **Reading (scripts/nn_cf_read.py, note15a).**
  - need = (remshr − rem) / full, with a 95% cluster bootstrap over bridges.
  - "Needed beyond a same-share random part" if need >= 0.30 and its interval is above 0. "Not needed beyond it" if need < 0.10. Otherwise "weak".
  - Reported beside: alone = (lens − lensshr) / full.
- **9B only.** A 2-item smoke runs first in the same queue (scripts/queues/h200_n15a_1029.sh).

##### Amendment 58 note 17 (Zach, 2026-10-29 ~02:10 UTC; before any result): the person or the looked-up answer? A value swap at the description's end (9B)
- **Why.** In v4 the passage comes before the question. By the description's end the model may already have looked up X's value (MP) or recalled X's attribute (MM). Note 14's counterfactual patch, a question about another person D, would then carry the answer and not the person. Note 15 shows this for MM from L12 on. For MP the lens cannot read the value there (2-4%, about chance), but it could sit outside the lens.
- **Donor (nn_swap --value-swap).** The same prompt and question about X; only the passage changes, giving X a new value.
  - The new value is drawn from the relation's answer vocabulary with random.Random(seed:id). It is not one of the passage's values, not X's remembered attribute, and has the same vowel or consonant start (for "a" / "an").
  - It is placed by replacing X's value, which appears exactly once.
  - Classes: donor = the new value; kept = X's old answer; MP third = X's remembered attribute; MM third = X's old passage value.
- **Cells.** v4ok, MP and MM, donor seeds 0 and 1, conditions full_cf and lensrand_cf.
  - Site last: L4-7, L8-11, L12-16.
  - Site span: L0-3, L4-7, L8-11, L12-16. The description text is identical in both prompts, so early layers are not a text swap here.
  - Site final: L21-24, L25-28, L29-30.
- **Pairs.** MP: pairs whose donor prompt the model answers with the new value (cf_ok). MM: all pairs (the donor prompt's right answer is still X's remembered attribute).
- **Readings, MP (scripts/nn_cf_read.py):**
  1. Positive check: at final L29-30 the whole patch moves >= 50% of answers to the new value. Otherwise readings 2 are void.
  2. Per description cell (last, span):
     - "carries the looked-up value": full_cf moves >= 20% to the new value, lensrand_cf < 10%, and full − lensrand has a 95% interval above 0 (note 14's reading 1);
     - "carries the person, not the value": < 5% moved while note 14's full_cf at that cell is >= 20%;
     - otherwise "partly".
- **MM (reported).** The share moved to the new passage value. Expected about 0: the recall's answer comes from memory.
- **Queue.** scripts/queues/h200_n17_1029.sh. GPU0, beside the 27B. A 2-item smoke runs first.

##### Amendment 58 notes 15 and 17, Lightning addendum (Zach, 2026-10-29 ~02:20 UTC; before any Lightning note 15 or 17 result; the 9B's note 15 results and its first note 17 smoke had been read)
- **Why.** A second family for tonight's two key tests. Lightning's v4 map has the 9B's shape: the description tokens are used L0-26, then the final token from L27-33.
- **Note 15 on Lightning.** Arms, answer sets and Dan's rule exactly as note 15.
  - Cells: every MM stage-1 hit at sites last and final minus Lightning's last window (46-50). Read from results/nn_swap/nn_cf_read/nem35l_v4_stage1.json: last L6-10, L11-15, L16-20, L21-26; final L34-39, L40-45.
  - Donor seeds 0 and 1.
- **Note 17 on Lightning.** The value swap exactly as note 17. Readings as note 17 with Lightning's windows:
  - Site last: L6-10, L11-15, L16-20, L21-26.
  - Site span: L0-5, L6-10, L11-15, L16-20, L21-26.
  - Site final: L34-39, L40-45, and L46-50, which is the positive check (>= 50% moved to the new value).
- **Queue.** scripts/queues/h200_n15n17L_1029.sh on GPU0, after the 9B's note 17 job, beside the 27B's stage 2. A 2-item smoke of each note runs first.

##### Amendment 58 note 17, 27B addendum, and note 18 (Zach, 2026-10-29 ~03:40 UTC; before any 27B note 17 or note 18 result; the 9B's note 17 result had been read: "the person, not the value" at all 7 description cells)
- **Note 17 on the 27B.** The value swap exactly as note 17 (MP cf_ok pairs; MM all pairs). Cells use the 27B's note 14 windows:
  - Site last: L8-15, L16-23, L24-31, L32-40.
  - Site span: L0-7, L8-15, L16-23, L24-31, L32-40.
  - Site final: L41-48, L49-56, and L57-62, which is the positive check (>= 50% moved to the new value).
  - Donor seeds 0 and 1. GPU1, after the 27B's note 15 job.
- **Note 18 (9B): the person or its position?**
  - **Why.** The value swap shows the description carries no looked-up value. What it carries could be the person, or the person's slot in the passage. Dan finds a slot code (his "address") that his lookups use.
  - **Donor (nn_swap --position-swap).** The same prompt and question about X. Only the passage changes: X's fact sentence trades places with another entity Z's (seeded). X keeps its value but sits in Z's old slot.
    - Pasting the donor's description-end state into the original run moves the answer to Z's value only if that state carries a slot: in the original passage, X's new slot holds Z.
    - Z's value is never X's value or X's remembered attribute.
    - Classes: donor = Z's value (the position route); kept = X's value (the person); MP third = X's remembered attribute.
    - cf_ok = the donor prompt is answered with X's value.
  - **Cells.** As note 17 on the 9B: last L4-7, L8-11, L12-16; span L0-3, L4-7, L8-11, L12-16; final L21-24, L25-28, L29-30. Donor seeds 0 and 1. Conditions full_cf and lensrand_cf. MP cf_ok pairs; MM all pairs, as a control.
  - **Readings, per description cell (MP):**
    - "the position, not the person": >= 20% moved to Z's value, lensrand_cf < 10%, and an interval above 0;
    - "the person, not its position": < 5% moved to Z's value at a cell where note 14's person swap moved >= 20%;
    - otherwise "partly".
  - **Final cells** are reported descriptively.
  - **No separate positive check.** The donor path is note 17's, whose check passed (93.4% at final L29-30). The swap is asserted to move X's sentence in every prompt.
  - GPU0, after the Lightning note 15/17 job. A 2-item smoke runs first.

##### Amendment 58 notes 15 addendum, 16 and 18: the 27B and Lightning (Zach delegated the overnight queue, 2026-10-29 ~03:45 UTC; before any 27B or Lightning result of these notes)
- **Why.** Every model gets every number. The tests, arms, conditions and readings are exactly as written for the 9B. Only the cells change, chosen by fixed rules from each model's note 14 stage 1 (results/nn_swap/nn_cf_read/{,nem35l_}v4_stage1.json).
- **Note 15 addendum (same-share control).** Cells = that model's note 15 cells: its MM stage-1 hits at sites last and final, minus its last window.
  - 27B: final L49-56; last L16-23, L24-31, L32-40.
  - Lightning: final L34-39, L40-45; last L6-10, L11-15, L16-20, L21-26.
- **Note 16 (Dan's lens part).** Cells: site last, MP and MM, at the first two windows that are stage-1 hits for both words.
  - 27B: L16-23, L24-31. Lightning: L6-10, L11-15.
  - Positive check: final MM at the model's last window (27B L57-62; Lightning L46-50).
- **Note 18 (position swap).** Windows as note 17 per model.
  - 27B: last L8-15 … L32-40; span L0-7 … L32-40; final L41-48, L49-56, L57-62.
  - Lightning: last L6-10 … L21-26; span L0-5 … L21-26; final L34-39, L40-45, L46-50.
- **All three notes.** Donor seeds 0 and 1. A 2-item smoke for each note runs first.
- **Queue.** scripts/queues/h200_rep_1029.sh.
  - Lightning on GPU0, after the 9B's note 18 job.
  - The 27B on GPU1, after its note 17 job.

##### Amendment 58 note 14, Bolt addendum (Zach's plan: Bolt on Thursday, competence and readout, the map if time allows)
- **Bolt** (88 layers; the J++ lens to L86; split over both GPUs).
  - Map windows: L0-9, L10-19, L20-29, L30-39, L40-49, L50-59, L60-69, L70-78, L79-86.
  - Everything else is as note 14 (competence MP MM, controls H1 RG RO, readout, stage-1 map).
- **Order.** Smoke, competence, controls, readout, then the map in seed-major order: last, final, span. Stage 2 is left for Zach.
- **Queue.** scripts/queues/h200_v4bolt_1029.sh. It starts once both GPUs are free.

##### Amendment 58 notes 19 and 20 (Zach, 2026-10-29 ~04:45 UTC; before any result): ablating the bridge on v4 (9B)
- **Note 19: resample ablation (nn_swap --resample).**
  - **Donor.** The donor prompt is another v4 passage's own question, seeded per item, with:
    - the same word and relation;
    - a different scene;
    - a bridge absent from X's passage, whose remembered attribute is neither one of X's passage values nor X's own.
  - **Patch.** Its states at the description (last token, or every description token right-aligned) are pasted into X's run over a band. The description then points at someone who is not in the passage.
  - **Classes:**
    - kept: X's answer;
    - donor: the new person's remembered attribute;
    - third: any other value of X's passage;
    - xmem: X's remembered attribute (MP) or X's passage value (MM);
    - other.
  - **Cells.** Last L4-7, L8-11, L12-16; span L0-3, L4-7, L8-11, L12-16; final L21-24, L25-28 (descriptive). Donor seeds 0 and 1; full_cf and lensrand_cf; all pairs.
  - **Readings, MP:**
    - "the lookup depends on the bridge state" at a description cell where note 14's person swap moved >= 20%, if X's answer falls by >= 20 points against no patch (lensrand_cf < 10%);
    - where the answers go: the class shares;
    - "they scatter into the passage" if "third" is the largest class after kept.
  - **MM (reported).** The share following the new person (the donor class), expected like the person swap.
- **Note 20: our headline removal test (ablate_v2 knock-out) on v4.**
  - **Prompts.** MP and MM on the 9B, kind clean, each item judged on its own (--tasks-per-word, level all), then v4's gate (--tasks-v4-h1).
  - **Removal.** At every token over the breadth band L12-16, under conditions paper10, paper10_rot, unembed10 and paper10_pcasize, read cand2.
  - **Reading.** The gap = MM's accuracy loss minus MP's under paper10, in points, with a 95% bootstrap over items.
    - "Recall needs the lens part more than the lookup (the headline replicates on v4)" if the gap is >= 10 with an interval above 0, and paper10_rot's gap is <= 1/3 of it.
    - Each word's losses and the controls are reported beside.
- **Queue.** scripts/queues/h200_abl_1029.sh. GPU1, beside the 27B chain, after Lightning's stage 2. A smoke of each runs first.

##### Amendment 58 note 15 addendum 2 (Zach, 2026-10-29 ~04:25 UTC; the 27B's note 15 final cell had been read: "answer"; no result of these arms seen): this answer, or any answer? (27B, the headline model)
- **Why.** Note 15's arm 3 control strips as many random atoms. Stripping X's and D's own answers costs about what stripping all of the relation's answers costs, so the lens part may carry "an answer of this kind" rather than this item's answer.
- **Arms.** As note 15, plus the same arms with two other answers of the relation in place of X's and D's ("oth": remkeepoth_cf, noaoth_cf, noaothctl_cf).
  - The two other answers are drawn with random.Random('oth:' + id).
  - They are never X's, D's or the third's answer, nor any value of X's passage.
  - Their control is as many of SEED_CTL's random atoms.
- **Cells.** The 27B's note 15 cells (final L49-56; last L16-23, L24-31, L32-40). Donor seeds 0 and 1, cf_ok pairs.
- **Reading (scripts/nn_cf_read.py, note15_spec).** Let d = e3(own) − e3(oth), with a 95% cluster bootstrap over bridges.
  - "This item's answer" if d >= 0.20 with its interval above 0 and e3(oth) <= 0.5 e3(own).
  - "Answer-ness (any answer of the relation)" if e3(oth) >= 0.7 e3(own).
  - Otherwise "partly specific".
  - Dan's rule is also applied to the oth set (note15_oth).
- **Queue.** scripts/queues/h200_n15b_1029.sh, on GPU0 after the 27B's stage 2, once >= 75 GB is free. A 2-item smoke runs first.

- Note 19 code fix (2026-10-29 05:10 UTC, before any result): the default answer classes looked up D's passage value before the resample override, and the resample donor is never in X's passage (KeyError in the smoke). The fix uses pv.get; no design change.

##### Amendment 58 notes 21-23 (Zach, 2026-10-29 ~06:00 UTC; before any result): is the J-space what the model will say? (9B, then the 27B)
- **Why.** The workspace paper's J-lens finds directions "poised to be verbalized" and calls them reportable. Our results so far fit a narrower reading: the J-space holds what the model is set to say (the recall twin's answer; late copies of the bridge), not every variable it computes with (the lookup's bridge goes around it).
- **Note 21: report vs use (nn_swap --report).**
  - **Report question.** Each v4ok MP item's hop-1 question over the same passage ("Which person wrote Things Fall Apart?"). The person is said, not used. The donor is the same question with D's description clause, D as note 14.
  - **Patch site.** The clause's last token, the same token as the lookup's description end.
  - **Answers.** Kept = X's name; donor = D's name; third = another entity of the passage. Candidates: the passage's names, first token with and without a leading space.
  - **Conditions.**
    - Dan's lens part (note 16): jpp_cf, jpprand_cf, nojpp_cf, nojpprand_cf. This is the primary lens part.
    - Beside it: note 10's top-10 part (lens_cf, rem_cf, lensrand_cf), which excludes the clean answer's top-10 output tokens. For a naming question these are the names, so it cannot carry X's name by construction.
    - Plus full_cf.
  - **Cells.**
    - 9B: last L4-7, L8-11, L12-16.
    - 27B: last L16-23, L24-31, L32-40.
    - Donor seeds 0 and 1.
  - **The lookup's counterpart** is note 16 (9B L4-7, L8-11; 27B L16-23, L24-31), plus the lookup with Dan's part at the missing cells (9B L12-16; 27B L32-40), run here.
  - **Reading per cell** (Dan's part; donor shares; cf_ok pairs). need = (nojpprand − nojpp) / full.
    - "the report needs the lens part" if the report's need >= 1/3;
    - "the use does not" if the lookup's need < 1/3;
    - "dissociation" if both hold at the cell.
    - Reported beside: alone = (jpp − jpprand) / full for both questions.
- **Note 22: the paper's clamp on v4** (conditions clamp, clamp_null, clamp_noans; v4ok MP and MM; cf_ok pairs).
  - **Bands.** 9B L4-11 and L12-16; 27B L16-31 and L32-40. Donor seeds 0 and 1.
  - **Readings:**
    - MM: "the clamp moves the recall" if >= 20% move to D's attribute and clamp_null < 10%; "through answer directions" if clamp_noans moves <= 1/3 of the clamp's share.
    - MP: "the clamp does not move the lookup" if < 10% move to D's passage value and less than 1/3 of MM's share.
- **Note 23: a trained read-out as the ceiling** (scripts/nn_probe_v4.py).
  - **Data.** The description-end state of every v4 MP and MM item, every 2nd layer.
  - **Split.** For a bridge with >= 2 distinct descriptions, the items using its second description (sorted) are held out.
  - **Read-outs.** Nearest class mean and logistic regression (300 steps, seed 0), scored top-1 among the relation's bridges (the readout's candidates). They are compared with the J++ lens's top-1 on the same held-out gated items.
  - **Readings (in the used window: 9B L4-16, 27B L8-40):**
    - "the bridge is represented beyond what the lens reads" if a read-out's held-out top-1 is >= 2x the lens's and >= 50% at some used layer;
    - "the person, not the description's words" if the held-out top-1 is >= 50% (the description is new to the read-out).
- **Queue.** scripts/queues/h200_rep2_1029.sh. 9B on GPU1 after the 9B ablations; 27B on GPU0 after the 27B note 15 addendum 2. A smoke of each note runs first.

##### Amendment 58 notes 21 and 23 addendum (Zach, 2026-10-29 ~06:00 UTC; before any note 21-23 result; the queued jobs were stopped before they ran)
- **Note 21: a second lens-part definition, applied the same way to both questions.**
  - Note 10's top-10 part excludes the clean answer's top-10 output tokens (the "skip rule"). For the report question those tokens are the names, so it cannot carry the name.
  - Added: the top-10 part without the skip rule (lensnp_cf, remnp_cf) and its same-share random twin (lensshrnp_cf, remshrnp_cf). They run for the report question and, at the same cells, for the lookup. The lookup now runs at every report cell with Dan's part and the np part, paired within its runs.
  - Reading per definition (Dan's part; np part): need = (twin − removal) / full. "The report needs it" if >= 1/3; "the use does not" if < 1/3; "dissociation" if both hold at a cell.
  - The skip-rule top-10 is reported as a footnote.
- **Note 23: the read-out, with two fixes.**
  - Two folds: hold out each bridge's second description (sorted), then its first. Accuracy is pooled over both folds.
  - A shuffled-label control: the same read-outs trained on permuted labels (seed 1); expected at chance.
  - 95% bootstrap intervals over bridges, gated items.
  - Readings unchanged, now read on the pooled folds. "Beyond the lens" also requires the shuffled control's top-1 to be below 2x chance.
- **Queue.** scripts/queues/h200_rep3_1029.sh replaces h200_rep2_1029.sh. Its jobs were stopped while waiting, before any run; logs renamed *.relaunched.log.

##### Amendment 58 notes 19-23 on every model before Bolt (Zach, 2026-10-29 ~06:20 UTC: "Lightning before Bolt; Bolt only if everything else has all its results"; before any 27B or Lightning result of these notes)
- **Notes 19-20 on the 27B and Lightning,** exactly as on the 9B.
  - Knock-out band: the model's breadth band (27B L32-40; Lightning L27-33).
  - Resample sites and bands:
    - 27B: last L8-15 … L32-40; span L0-7 … L32-40; final L41-48, L49-56.
    - Lightning: last L6-10 … L21-26; span L0-5 … L21-26; final L34-39, L40-45.
  - Queue: scripts/queues/h200_ablX_1029.sh.
- **Notes 21-23 (with their addendum) on Lightning,** exactly as on the 9B.
  - Report cells: last L6-10, L11-15, L16-20, L21-26.
  - Clamp bands: L6-20 (where the bridge is used) and L27-33 (the breadth band).
  - Queue: scripts/queues/h200_rep3L_1029.sh.
- **Bolt** waits for every one of these jobs.

##### Amendment 58 note 24 (Zach, 2026-10-29 ~07:30 UTC; the set was generated and checked for format only, no model run): cue-conflict descriptions, to block the memory twin's shortcut (9B, 27B)
- **Why.** A v4 description's own words can point at the memory twin's answer without the person ("wrote Things Fall Apart" -> Nigerian). The lookup is immune: its value is made up and bound to the name.
- **Set: jsuite_v4cc** (scripts/jsuite_v4cc.py, seed 4101; data/tasks_v2/jsuite_v4cc_test_chat sha256 9f7fe7254c0793a9…, controls jsuite_v4ctlcc_test_chat 9033a001ca5184ad…).
  - 50 people with an unambiguous nationality in v4's vocabulary. Each has two descriptions:
    - conflict: the description's salient association is another nationality, the cue ("wrote A Passage to India": cue Indian, answer English);
    - aligned: the association is the person's own ("wrote Howards End").
  - Facts are well known and were checked by hand when written.
  - v4's format otherwise: 6 people per scene, made-up values (never an entity's own nationality, never X's, never X's cue), two wordings. 198 scenes: 100 conflict, 98 aligned.
  - Words: MP, MM, H1, RG, RO. New people carry their facts on the item (scripts/jswap.table, extra_facts).
- **Runs per model** (9B, then the 27B):
  - competence MP MM, and controls H1 RG RO;
  - note 15's arms (own and rel) on MM at the model's decisive cells (9B final L21-24, L25-28, last L12-16; 27B final L49-56, last L24-31, L32-40), v4ok, donor seeds 0 and 1;
  - note 20's knock-out at the breadth band.
- **Readings (scripts/nn_cc_read.py, split by description type):**
  1. **Behaviour.** MM accuracy on conflict vs aligned descriptions (among items whose closed-book hop 1 and hop 2 alone are right). Among conflict MM errors: the share answering the cue, against the share any one wrong nationality would get by chance (1/33). "The shortcut is taken" if the cue share is >= 3x chance with a bootstrap interval above it.
  2. **Shortcut-free answer.** Dan's rule (note 15) on conflict MM items only, at the decisive final cells. If it says "the lens part is the answer" on conflict items, the lens holding the answer is not an artefact of the description's association. Aligned items are reported beside.
  3. **Knock-out.** The memory-vs-lookup loss gap (note 20) on conflict items and on aligned items. "The recall's lens dependence survives the shortcut block" if the conflict gap is >= 10 points with an interval above 0.
- **Queue.** scripts/queues/h200_cc_1029.sh, before Bolt. 9B on GPU1 beside the 27B chain; 27B on GPU1 after Lightning's last job. A smoke runs first.

##### Amendment 58 note 23 addendum 2 (Zach, 2026-10-29 ~16:40 UTC; note 23's read-outs were read: data-starved, held-out top-1 below the lens): the read-out with more training data
- **Why.** Note 23's read-outs had about 4 training examples per person, all from the person's other description. The J++ lens needs no training, so the comparison was not a ceiling.
- **Data.** Five extra v4 passage sets from scripts/jsuite_v4.py, unchanged, seeds 4002-4006 (names jsuite_v4p4002 … jsuite_v4p4006): the same people and descriptions in new passages. That gives about 24 training examples per description.
  - The extra sets only train. Their items with a held-out description are dropped.
  - The test items, the gate, the folds, the shuffled-label control, the bootstrap and the lens comparison are note 23's, on the original set.
- **Readings.** Note 23's, unchanged.
  - "The bridge is represented beyond what the lens reads": a read-out's held-out top-1 >= 2x the lens's and >= 50% at some used layer (9B L4-16), with the shuffled control below 2x chance.
  - "The person, not the description's words": held-out top-1 >= 50%.
- **Run.** 9B first (qwen35_9b_nn_probe_v4_v2, GPU1). The 27B only if Zach asks. Queue: scripts/queues/h200_probe2_1029.sh.

##### Amendment 58 note 24, Lightning addendum (Zach: "GPUs used optimally", 2026-10-29 ~16:30 UTC; before any Lightning note 24 run): note 24 exactly as on the 9B and 27B. Cells: final L34-39, L40-45 and last L21-26 (where note 15 found the lens part matters); knock-out band L27-33. Queue: scripts/queues/h200_cc_1029.sh nem35l, GPU1. Bolt waits for it.

##### Amendment 58 note 25 (Zach, 2026-10-29 ~17:30 UTC; before any run of it): priming at the bridge, from Dan's guess
- **Why.** Dan (29 Oct): a famous name brings its best-known attribute into the lens before any question (Aristotle -> Greek). Then "the J-space at the bridge holds the answer" could be the person's association rather than what the model will say.
- **Looked at before writing this (feasibility only).** Note 14's v4 readout on the 9B, description's end, J++ top-1:
  - MM (the answer is X's remembered attribute): 37-44% at L8-16 (chance 3.4).
  - MP (the answer is X's made-up passage value): 2-4% at every layer.
  - X's remembered attribute on MP prompts has never been read.
- **Test.** v4's lookup (MP) and its recall twin (MM) share the passage and the description. Only the question's frame differs:
  - MP: "Which nationality is the actor cast as the person who wrote Things Fall Apart in the new film?"
  - MM: "Which nationality was the person who wrote Things Fall Apart?"
  - On MP the model will say X's passage value, not X's remembered attribute.
- **Run.** scripts/nn_readout.py --items v4 --priming: note 14's readout (J++ and logit lens, every 2nd layer, the relation's answers as candidates, ties against the target), with three more targets per prompt:
  - other: on MP, X's remembered attribute; on MM, X's passage value;
  - third: an answer of the relation that appears nowhere in the scene (random.Random('third:' + id)), the chance control;
  - ctx: another entity's passage value (random.Random('ctx:' + id)).
- **Windows** (stage 1's hits for both words): description's end 9B L4-16, 27B L16-40, Lightning L6-26; final token 9B L21-30, 27B L49-62, Lightning L34-50. Even layers.
- **Statistic** (scripts/nn_priming_read.py). Per prompt and target, the share of window layers where the target is top-1.
  - Primary set: scenes whose MP and MM are both v4ok (paired). J++ lens.
  - rho = (MP other - MP third) / (MM attr - MM third) at the description's end.
  - Cluster bootstrap over bridges, 2000 draws.
- **Readings.**
  - Positive check: MM attr - MM third >= 10 points, interval above 0. Otherwise void.
  - "The bridge shows the person's attribute, whatever will be said": rho >= 0.7.
  - "The bridge shows what will be said": rho <= 0.3.
  - "Mixed" between; "unclear" if rho's interval holds both 0.3 and 0.7.
  - Final token: "the end shows what will be said" if MP attr (the passage value) - MP other >= 20 points.
  - Descriptive: the logit lens; all v4ok prompts unpaired; MM's other (X's passage value on recall prompts); ctx.
- **Order.** 9B now on GPU1 beside Bolt (it fits in the free memory); smoke of 8 prompts per family first. The 27B (GPU0) and Lightning (GPU1) after Bolt. Queue: scripts/queues/h200_prime_1029.sh.
- **Question order (Dan's 27B result, question first).** Not tested here. Every v4 prompt puts the passage first; results are scoped to that order.

#### Amendment 59 (Zach, 2026-10-29 ~18:45 UTC; before any run of it): what the J-space shows at the bridge, question order, Muse on v4
Context: Bolt's v4 run was cancelled (Zach: too slow, same family as Lightning); its cached weights were dropped (Zach's OK). Zach chose notes 26-28; no data-seed replication.

##### Note 26: what the J-space shows at the bridge (9B, 27B, Lightning; Muse after note 28's map)
One readout job per model (scripts/nn_readout.py; J++ and logit lens; every 2nd layer; sites: the description's last token and the final token).
- **(a) Top-20 tokens, descriptive.** Over the full vocabulary and over letter tokens only, for v4 MP and MM (gated, ok and fail) and for (b)'s prompts. The token categories and the analysis plan are fixed in an addendum before the dump is read. No verdict.
- **(b) Priming with no relation asked.** For scenes whose MM is v4ok, the closed-book naming question H1 ("Which person wrote Things Fall Apart?": no passage, no relation) and the recognition question RG (the passage, no relation).
  - Targets as note 25 (attr = X's remembered attribute, other = X's passage value, third = an answer absent from the scene), candidates = the relation's answers.
  - Window: note 25's description-end window per model.
  - rho_H1 = (H1 attr - H1 third) / (MM attr - MM third), paired by scene, from the same run; cluster bootstrap over bridges.
  - Readings: rho_H1 >= 0.7 "the remembered attribute is there with no relation asked (association)"; <= 0.3 "the asked relation brings it"; mixed between; unclear if the interval holds 0.3 and 0.7. RG reported beside (descriptive).
- **(c) Priming on cue-conflict descriptions** (jsuite_v4cc). MP and MM, all items, one more target: the description's cue (conflict items only; e.g. "designed the Statue of Liberty": cue American, answer French).
  - Primary subset: scenes whose named recall (MM hop 2 alone) is right in the model's cc competence run. Secondary: the v4_split-gated subset; all items.
  - Statistic at the description's end (note 25's window): d = top-1 share of X's remembered attribute minus the cue's, conflict items, MP and MM pooled (each word beside); cluster bootstrap over people.
  - Readings: "the person" if d >= 10 points with its interval above 0 and remembered >= 2x cue; "the description's words" if cue - remembered >= 10 points with its interval above 0; mixed otherwise. Aligned items' remembered-attribute share reported beside.
- Scorer: scripts/nn_bridge_read.py.

##### Note 27: question first (9B, 27B, Lightning)
- **Why.** Every v4 prompt puts the passage first. Dan (29 Oct, his test 53.1, rule set after the 27B's cells) finds the 27B's lookup leans more on the lens part with the question first (+0.11 [0.01, 0.22]); agents usually see the question before the tool output.
- **Set.** jsuite_v4qf_test_chat and jsuite_v4ctlqf_test_chat: v4's items unchanged except one flag that renders the question and its instruction first, then the passage, in the same user turn (scripts/jsuite_v4qf.py; sha256 recorded).
- **Runs per model.** Competence (MP MM, cand2, hop 1 by generation). The closed-book H1 gate reuses the v4 controls run (no passage, so order is irrelevant). Note 20's knock-out at the model's band (paper10, paper10_rot, unembed10, paper10_pcasize). Note 25's priming readout (descriptive here: at the description's end the passage is not yet read).
- **Readings.**
  1. "The split holds with the question first": MM - MP loss gap >= 10 points, interval above 0 (as note 20).
  2. Order effect on the lookup: items gated in both orders, per-item paper10 loss question-first minus passage-first, MP; cluster bootstrap over bridges. "The lookup leans more on the J-space with the question first" if >= 10 points with its interval above 0; "no order effect" if the interval lies within +-10; else unclear. MM beside.
  3. Competence by order reported.

##### Note 28: Muse Glimmer 30B on v4 (meta-models/Muse-Glimmer-30B, our J++, prefix muse30_)
- **The note 14 battery:** competence, controls (H1 RG RO), the readout map, stage 1 (full_cf / lensrand_cf; sites last, span, final; donor seeds 0 1; windows 0-5 6-11 12-17 18-23 24-29 30-35 36-41 42-47 48-50), stage 2 at stage 1's cells (as h200_v4_1028.sh).
- **Note 20's knock-out at two bands:** L36-42 (Muse's band since v2) and L26-32 (the 27B's and Lightning's relative depth, ~50-62%); both reported, each read by note 20's rule.
- **Note 25's priming:** windows by the rule that gives the other models' windows: the min-max of the bands that are stage 1 hits for both MP and MM, at site last (description end) and at site final.
- **Note 26 on Muse** with those windows.
- **Note 17's value swap** at site last over Muse's description windows (stage 1 last hits for MP), donor seeds 0 1.
- Two GPUs, a Muse process on each. Readings: each note's own.

##### Amendment 59 note 26 addendum (Zach, 2026-10-29 ~19:20 UTC; before any of note 26's top-20 dumps was read; a smoke's file was checked for format only): the analysis plan for (a)
- **Unit.** One top-20 list per item x site x lens x variant x even layer. Primary: J++, the letter-token variant, inside note 25's windows (description end and final; Muse by note 28's rule). Families: MP_ok, MP_fail, MM_ok, MM_fail, H1_mmok, RG_mmok; cue-conflict MP/MM.
- **Normalisation.** Decode; NFKC; note a leading space; strip non-word characters at both ends ("(N" -> N); casefold; script of the first letter; concept key = fold minus a trailing "s" / "'s".
- **Word match.** Token t matches word W if fold(t) is W or its plural or possessive; or t is the tokenizer's first token of " W" / "W" (lowercase too) with >= 3 letters; or t starts a word, has >= 4 letters and is a prefix of W. Tokens of 1-2 letters never match a word.
- **Categories** (first match wins, in this order):
  1. JUNK (no letter)
  2. FUNC (NLTK English stopwords)
  3. REAL (X's remembered attribute and its country/adjective aliases)
  4. PV_X (X's passage value)
  5. CUE (the cue, conflict items only)
  6. CTX_VAL (other entities' values)
  7. CLASS (other answers of the relation)
  8. BRIDGE (X's name words, >= 3 letters, not in the description)
  9. CTX_NAME (other entities' names)
  10. OCC (people: the description noun and a fixed synonym list, only when absent from the prompt)
  11. KNOW (content words >= 4 letters of X's other description, absent from the prompt)
  12. DESC (content words of the description)
  13. FRAME (question words outside the description, plus a fixed relation-type list)
  14. PASSAGE (other content words of the passage)
  15. CODE (code-like tokens)
  16. NONLATIN (matched to REAL / PV_X / CTX / CLASS by translated country and nationality names in 15 locales via babel; a match takes that category, flagged translated; unmatched = NONLATIN_OTHER)
  17. OTHER
- **Metrics.** Mean over items, cluster bootstrap over bridges (2000, seed 0): share of the top-20 per category; presence (in the top-20) by layer and anywhere in the window; first layer present.
- **Controls.** C1, shuffled item: this item's list scored against another bridge's REAL / BRIDGE / OCC / KNOW lists, same relation, different REAL. C2: the logit lens. C3: H1 vs MM. C4: MP vs MM paired by scene.
- **Readings** (description end, window, J++ letters):
  1. "Attribute cloud at the bridge": presence of REAL minus C1 >= 0.20, of OCC or KNOW minus C1 >= 0.15, and BRIDGE presence below REAL's.
  2. "Name first, then attributes": on items with both, the median first layer of BRIDGE is >= 4 layers before REAL's.
  3. "Class priming, not this person": REAL presence < 3x the mean per-value presence of CLASS.
  4. "Multilingual noise floor": NONLATIN_OTHER + CODE >= 0.3 of the list while translated content < 0.05 (reported as the lens's floor, not content).
  5. Token-level priming: REAL presence on MP and MM within +-0.10 (paired); PV_X at C1's level at the description end; PV_X ahead of REAL on MP at the final token.
  - Descriptive: success vs failure (REAL / BRIDGE on MM_fail vs MM_ok), cue vs REAL on conflict items, H1 vs MM, every variant and lens.
- **Hand check.** Blind, before reading the classifier's output: 5 items x 3 models x 2 sites, OTHER / NONLATIN_OTHER tokens labelled "about X" or not. If done by a model rather than a person, flagged as weaker evidence. Kappa per category.
- **Slides** (rules, not cherry-picked): stacked category shares per model and site (MP, MM, H1); presence-by-layer lines (REAL, BRIDGE, PV_X, OCC/KNOW, FRAME) with C1 dashed; a token wall for the first item per relation by id.
- Scorer: scripts/nn_topk_read.py.

#### Amendment 60 (Zach, 2026-10-29 ~20:30 UTC; before any of it is built or run): three v4-family sets
Zach's design choices, 29 Oct (multiple choice; each listed below where it applies). The cue-conflict readout (note 26 (c), 9B) found that the description's own words drive the J-space at the description's end (cue 86% vs the person's attribute 3% on descriptions without the cue word). These sets vary where the bridge comes from and what the hidden step is used for.

**Common to notes 29-31.**
- Built from scripts/jsuite_v4.py's pieces: data/v3_bridges.json entities with two descriptions each; v4's filler genres and splice; stem filter; X's position rotated.
- About 600 scenes per set; seeds 5001 (note 29), 5101 (note 30), 5201 (note 31). Passage first, one chat turn, test split.
- Item data stays out of the public repo, like v3 and v4.
- Models: 9B, 27B, Lightning.
- Per set and model:
  - competence (cand2; hop 1 by generation where hop 1 names an entity);
  - controls (competence_variants on the set's ctl set);
  - note 20's knock-out at the model's band (paper10, paper10_rot, unembed10, paper10_pcasize);
  - the readout with note 25's priming targets and note 26's top-20 dump, at the bridge site and the final token, in note 25's windows.
- A smoke runs first. Scorer: scripts/nn_v5_read.py.

##### Note 29: the remembered attribute as a key (jsuite_v5kn named, jsuite_v5kd described)
- **Entities and attribute.** People (nationality, as its country), cities, companies, landmarks (country). Films are dropped.
- **Passage.** Six lines "The delegation from <country> will wear <colour> badges."
  - The countries are X's country plus five other distinct countries; the colours come from a fixed list with distinct first tokens.
  - Filler as v4. No entity is named in the passage.
- **Words.**
  - MP, the key lookup:
    - named: "What colour badges will the delegation from <X>'s home country wear?" (cities: "...from the country where <X> is", companies: "...where <X> is based", landmarks: "...where <X> stands");
    - described: the same with X's description.
  - MM, the say-twin: "Which country is <X> from?" (described: X's description; wording per type). Answer: the country.
  - Steps:
    - named MP: [the say question, the direct key lookup "...from <country>..."];
    - named MM: [the say question, the say question];
    - described MP: [description -> entity, the named MP question, the direct key lookup];
    - described MM: [description -> entity, the named say question].
  - Guess: the same question about "an unnamed figure" (chance 1/6 for MP).
  - Controls set: H1 closed-book (named: the say question with no passage; described: description -> entity).
- **Gate:** v4_split (H1 right, step 2 right, guess wrong; ok / fail by the whole).
- **Readings** (knock-out on gated-ok items; bootstrap over items, 2000):
  1. "A remembered word that is used, not said, needs the J-space":
     - MP's paper10 loss minus the direct key lookup's (MP's last step, its own knock-out rows) >= 15 points, its interval above 0;
     - the same contrast under paper10_rot below 5;
     - MP's loss >= half of MM's.
     - "Goes around": that contrast < 10 with its interval's upper end < 15.
     - Mixed otherwise.
  2. MM - MP gap, as note 20.
  3. Priming.
     - At the name (named) or the description's end (described): the country's top-1 share among the countries on MP vs MM; rho = (MP key - MP third) / (MM attr - MM third) as note 25.
     - At MP's final token (descriptive): "the key shows before the value" if the country's top-1 share is >= 10 points above its third at a final-window layer before the first layer where the colour's share passes 50%.
- Named is primary. Described is secondary, read only where >= 100 items are gated ok per word.

##### Note 30: a true knowledge conflict (jsuite_v5kc)
- **Entities.** The same four country-type relations.
- **Descriptions.** v4's, kept only if no word names a country, nationality or city other than X's own (a fixed lexicon; the cue check).
- **Passage.**
  - Six attributed claims: "The club's notes say <E> was <value>." (people; others "...say <E> is in <country>").
  - X's value is false: a random other value of the relation's vocabulary, never X's true value or another value in the scene. The other five are true. Filler as v4.
- **Words.**
  - CN: plain, named ("Which nationality was <X>?"); CA: "According to the passage, ..." named; DN / DA: the same, described.
  - TN / TD: the same scene with X's claim true (plain question): the no-conflict control.
  - Steps: [description -> entity (described only), the named question], with the passage.
  - Controls set: H1 (closed-book description -> entity) and H2 (closed-book named recall).
- **Labels.** Each answer is passage (X's false value), memory (the true value) or other.
- **Eligibility.**
  - Scenes whose closed-book H2 is right (described: and H1).
  - The knock-out keeps every item of a scene whose control T is right (ablate_v2 --tasks-scene-words); the scorer restricts to the eligible scenes.
- **Readings.**
  1. Behaviour: passage share, plain vs "According to", named and described (paired by scene).
  2. Knock-out: paper10's passage-share shift minus rotated's and minus unembed10's, bootstrap over bridges. "The knock-out pushes answers to the passage" if >= 10 points with the interval above 0.
  3. The bridge by outcome (plain words, eligible).
     - Top-1 shares at the bridge site of the true value, the false value and an absent value (third), on passage-wins vs memory-wins.
     - "Memory channel": the true value's share on passage-wins within 10 points of memory-wins, and the false value's <= third + 3.
     - "Current belief": the false value's share on passage-wins >= third + 10.
     - "Memory strength": the true value's share lower on passage-wins by >= 10 points.
     - Beside (descriptive): AUC of memory-wins vs passage-wins from the bridge score (true minus false share), J++ and logit lens, against the closed-book H2 margin.
  4. Framing: plain vs "According to": the change in the bridge's true-value share (paired) beside the behaviour change.
  5. Final token: per-layer AUC onset (descriptive).

##### Note 31: the bridge from the context (jsuite_v5al)
- **Passage.** v4's (six people, made-up values for the relation) plus one binding sentence per person: "<E> goes by the codename <C>."
  - Codenames are invented two-syllable pseudo-words from a fixed syllable list, not real words or names. No stem shared with a scene entity; distinct first tokens. Unused codenames serve the guess.
- **Words.** v4's MP and MM with the description replaced by "the person codenamed <C>":
  - MP: "Which nationality is the actor cast as the person codenamed <C> in the new film?";
  - MM: "Which nationality was the person codenamed <C>?".
  - Steps: [hop 1 "Which person is codenamed <C>?" with the passage, v4's named hop 2].
  - Guess: an unused codename.
  - Controls set: H1 = hop 1 with the passage (the codename exists only there).
- **Gate:** v4_split.
- **Readings.**
  1. Split: the MM - MP knock-out gap >= 10 points, its interval above 0 (note 20).
  2. "Identity carries the attribute into the J-space": at the codename's last token, in the window, X's remembered attribute's top-1 share minus third >= 10 points with its interval above 0 (MP and MM pooled, paired as note 25).
     - rho_alias = (MP remembered - third) / (MM attr - third) beside.
     - Descriptive beside: v4 MM's description-end share, and the final token.
  3. The top-20 dump read by note 26's plan.

##### Amendment 60 addendum (Zach, 2026-10-29 ~21:05 UTC; before any v5 set was generated or run): confound controls
Zach asked whether extending v4 adds confounds (e.g. linear entity -> country relations). Controls added:
- **Note 29 (key).**
  - Entities whose name reveals the country are excluded: name_reveals_answer, or a country / nationality word in the name ("Air France", "Great Wall of China").
  - A closed-book prior control K0 ("What colour badges will the delegation from <country> wear?", no passage) measures any country -> colour prior; it should sit at chance. Items record flag_colour_match (the assigned colour is an iconic national colour of X's country), and reading 1 is also reported without those items.
  - Linear entity -> country relations do not reach the answer: the colour is assigned at random per scene, so the lookup's answer cannot be decoded from the entity.
  - The say-twin MM has its answer among the passage's six countries (recognition). Reading 1's "half of MM's loss" is a within-set comparison, and MM's loss is expected below v4 MM's.
- **Note 30 (conflict).**
  - The description cue lexicon adds about 150 well-known places mapped to their country ("Hollywood", "Seville"); a description naming a place of another country is dropped. Kept descriptions record desc_place_cue.
  - Named words are primary; described words are secondary, since a semantic cue can survive a lexicon.
  - Items carry entity_reals.
- **Note 31 (alias).**
  - Codenames are assigned to entities at random (seeded), so a codename's own sound cannot correlate with its entity's attribute.
  - Items carry entity_reals, and the readout adds the target ctxreal (another scene entity's real attribute).
  - Reading 2 adds a within-scene condition: X's attribute's top-1 share must exceed ctxreal's by >= 5 points, interval above 0. Otherwise the reading is "scene-level association, not this identity".
  - Phrasing: a positive reading means the attribute reaches the bridge through the in-context binding; it may be carried from the passage's mention of X's name.

#### Amendment 61 (Zach, 2026-10-29 ~20:50 UTC; after a four-agent red-team, before the rebuilt sets or these runs exist): rebuilt key and conflict sets; two knock-out tests
- **Red-team findings that led here.**
  - In the key set, X's country was the only one from its continent in 39% of scenes. On the 9B the lookup scored 79% there vs 68% with a shared continent.
  - The conflict set's "based in" made companies a poor conflict (1% memory answers), and only 27% of false values were plausible (same continent).
  - The knock-out band sits before the lookup's own answer forms at the final token (a timing confound).
  - Neel's "steering the model to say / not say a token" hypothesis is untested on v4.
- **The 9B runs already done on the first key and conflict sets** become pilots: they are reported as such, never pooled with the rebuilt sets. Those runs are the named key set's competence, controls and knock-out, and the conflict set's competence, controls and knock-out.

##### Notes 29b and 30b: the rebuilt sets
- **jsuite_v5kn2 / jsuite_v5kd2** (seed 5002): note 29 unchanged, except every scene has at least two distractor countries from X's continent (and one from its region where possible). Items record x_continent and n_same_continent; shortfalls are reported.
- **jsuite_v5kc2** (seed 5102): note 30 unchanged, except:
  - companies use "was founded in" (claim and question; table values checked for founding country);
  - X's false value comes from the same continent as the truth (false_same_continent recorded, fallback random);
  - descriptions with non-place cues to another country are dropped as well (leagues, prizes, "American aviator", ...).
- Readings: notes 29, 30 and the amendment 60 addendum, unchanged.
- Analysis-time strata, all sets, reported beside the readings:
  - key: each model's own K0 colour prior (items whose colour equals the model's closed-book reply) excluded;
  - per relation, plausibility, continent sharing;
  - three-way answer labels (memory / X's passage value / other);
  - candidates restricted to the scene's.

##### Note 32: the knock-out where the lookup's answer forms (timing)
- **Bands, by a rule on note 17's value swap at the final token (MP):**
  - the forming band (primary): the window whose value-swap share is nearest 50%, i.e. 9B L25-28 (55.1), 27B L49-56 (45.1), Lightning L34-39 (21.3; L40-45 is 97.0);
  - the formed band: the first window >= 90%, i.e. 9B L29-30, 27B L57-62, Lightning L40-45.
- **Runs:** note 20's knock-out on v4 (paper10, paper10_rot, unembed10, paper10_pcasize, all positions, v4 gate) at both bands, 9B, 27B, Lightning. Scorer scripts/nn_ko_read.py; bridge-clustered intervals beside.
- **Readings (forming band):**
  - "The lookup needs the J-space where its own answer forms" (the main split is partly timing): MP's paper10 loss minus its paper10_rot loss >= 20 points with the interval above 0.
  - "Timing does not explain the split": that difference < 10 with its upper end < 20.
  - Unclear otherwise. MM and the formed band reported beside.

##### Note 33: where the recall's need sits (description vs final token)
- **Runs:** note 20's knock-out at the main band (9B L12-16, 27B L32-40, Lightning L27-33), with removal restricted to:
  - desc: only the question's description of the bridge (start_desc's tokens; ablate_v2 --positions desc);
  - final: only the last token (--positions final).
  - Conditions paper10 and paper10_rot, v4 gate, 9B, 27B, Lightning.
- **Readings (MM; loss net of paper10_rot, as a share of note 20's all-position MM loss net of its rotated):**
  - "The need sits at the final token (saying)": final share >= 2/3 and desc share <= 1/3.
  - "At the description": desc share >= 2/3 and final share <= 1/3.
  - "Spread" otherwise. MP beside.

##### Amendment 61 addendum (Zach, 2026-10-29 ~21:25 UTC; before any run on jsuite_v5kn2 / v5kd2): a 3+3 continent split
The first build of v5kn2 / v5kd2 (">= 2 same-continent distractors"; sha256 4c515e74... / e87e5d96..., never run) made X's continent the passage's majority continent in 91% of scenes, a passage-only guessing cue (~27% vs 1/6). v5kn2 / v5kd2 are rebuilt in place with a 3+3 split:
- three countries from X's continent (X and two others);
- three from one other continent, so no continent is a majority.
- Where X's continent has too few countries in the vocabulary (Oceania: Australia only), use as many as exist, draw the rest so that no continent has more than three, and record "split_ok".
- Readings: unchanged. Scenes with split_ok false are reported beside and left out of the primary reading.

##### Amendment 61 note 33 addendum (Zach's position-split test, 2026-10-29 ~21:55 UTC; after the 9B's desc / final runs, before any mention run): the bridge's mention
The 9B's description-only and final-only runs account for about a third and none of the main band's recall need ("spread"). To complete the split: the same knock-out restricted to the bridge's mentions in the passage (ablate_v2 --positions bridge: the bridge name's tokens, where v4 names X in its fact sentence). Main band, paper10 and paper10_rot, v4 gate, 9B, 27B, Lightning. Descriptive: the mention's share beside the description's and the final token's.

#### Amendment 62 (Zach, 2026-10-30 ~01:20 UTC; before any of it is run): DeepSeek-V4-Flash after Muse
- **Model.** deepseek-ai/DeepSeek-V4-Flash (rev 60d8d70; MoE, 284B total / 13B active; FP8; both GPUs). Lens: its published J++ (Ayonrinde & Lindsey via neuronpedia; sha-pinned). Prefix dsv4f_.
- **Order and disk.** It starts once every Muse job has exited. Zach approved dropping Muse's cached weights first (56 GB); DeepSeek (160 GB) is then downloaded.
- **Runs.**
  - v4: competence, controls, and note 20's knock-out at its band L18-23 (pre-registered for DeepSeek since amendment 39; paper10, paper10_rot, unembed10, paper10_pcasize).
  - Note 25's priming readout with note 26's top-20 dump.
  - Note 31's alias set (competence, controls, knock-out, readout).
  - Note 29b's named key set (jsuite_v5kn2: competence, controls, knock-out, readout).
- **Windows.** No stage 1 map is run, so they are fixed now by relative depth, from the three main models' rule-derived windows: description end 15-55% of depth (L6-23), final token 70-95% (L30-40).
- **Readings:** each note's own. Smoke first.

#### Amendment 63 (Zach, 2026-10-30 ~03:35 UTC; before any code or run below): three tests after the literature check
Zach's MC answers (30 Oct ~03:10 UTC): build notes 34, 35 and 36; queue them after DeepSeek (amendment 62); the probe compares the monitor's view against controls, with the conflict-word read; the three-uses test is named only, capital, new arm only; the route swap uses an outside donor. Why: the literature check (30 Oct) found no J-lens work on memory vs context; trained probes decode an answer's source on other models and data (Brink et al. 2026; Zhao et al. 2024); and the J-space paper frames workspace content as "operated on by whatever function the new context supplies". These tests make the monitor claim a same-data comparison and test that framing directly.
- **Models and bands.** 9B L12-16, 27B L32-40, Lightning L27-33 (the knock-out and swap bands used throughout). One deterministic run per model. Intervals: 95% bootstrap over bridges (2000 resamples) unless stated otherwise. A smoke of at most 8 items per word on the 9B comes first.

##### Note 34: the provenance probe (jsuite_v5kc2)
- **Items.** CN and DN (plain question, conflict passage). Each item's label (memory or passage) comes from the existing competence run's unedited answer, as nn_v5_read.kc labels it; "other" items are dropped. CA, DA, TN and TD are not used for training.
- **Sites.**
  - s1: X in the question (named: the last token of X's name in the question; described: the description's last token).
  - s2: the last token of X's false value in its claim sentence in the passage.
  - s3: the final prompt token.
- **Layers.** Primary: the band, with features averaged over its layers. Descriptive: every 4th layer from 0.
- **Feature sets** (the same residual h at each site and layer):
  - F, the full state: h.
  - J, the monitor's view: h's coordinates in an orthonormal basis of the span of the J++ vectors of the relation's answer vocabulary at that layer (every value's first token; m dimensions).
  - R: a seeded random m-dimensional subspace (rotation 888 + layer).
  - U: the span of the same tokens' unembedding rows.
  - Z, a zero-shot monitor: the J++ logit of X's true value minus that of its false value at the site (no training).
- **Probe.** Logistic regression (L2; C picked by inner CV from 0.01, 0.1, 1, 10) on standardised features. 5-fold CV grouped by bridge (an entity's items in one fold). Named, described and pooled are scored separately. AUC on held-out folds.
- **Controls.** For F, labels shuffled within relation (5 permutations); its AUC must sit near 0.5.
- **Reading** (per model, at the band, site s1):
  - "monitor blind": AUC_J <= AUC_R + 0.05 and AUC_F >= AUC_J + 0.10, intervals not overlapping;
  - "monitor sees": AUC_J >= 0.70 and AUC_J >= AUC_R + 0.10;
  - otherwise "unclear".
  - s3 is read the same way; s2 is descriptive.
  - Claim across models: "a J-lens monitor cannot tell memory from passage, while the model state can" needs "monitor blind" on >= 2 of 3 models at s1, and AUC_F >= 0.70 at s1 or s3 on those models.
- **Claim read (add-on).** J++ top-20 (note 26's letters filter) at s2 on CN and DN, and at the same position on TN and TD (where the claim states X's true value), paired by scene.
  - The fixed list: false, fake, wrong, incorrect, untrue, myth, mistaken, mistake, error, lie, lies, fiction, fictional, hoax, rumor, rumour, misinformation, inaccurate, bogus, not, actually, allegedly, supposedly, claimed, claims. Matched case-insensitively on the stripped token, whole token only.
  - Measures: the share of items with at least one list word in the top-20, and the mean count; conflict minus true control.
  - Control: 25 vocabulary letter-tokens drawn with seed 34 (none on the list), the same contrast.
  - Reading:
    - "conflict seen": a contrast >= 10 points, interval above 0, and the control's contrast <= 1/3 of it;
    - "not seen": the interval includes 0;
    - otherwise "weak".

##### Note 35: one remembered fact, three uses (jsuite_v5kn2 and a new arm, named only)
- **Arm MC** ("compute"), on jsuite_v5kn2's named scenes (same passage and X):
  - Questions:
    - people: "What is the capital of {x}'s home country?";
    - cities: "What is the capital of the country where {x} is located?";
    - companies: "What is the capital of the country where {x} is based?";
    - landmarks: "What is the capital of the country where {x} stands?"
  - The answer is the capital of X's country. Candidates are the capitals of the passage's six countries (cand2).
  - The set is jsuite_v5kn2c, built by jsuite_v5key.py --compute. Ids are j3:chat:v5kn2c:<suffix> and pair with kn2's by suffix. The existing builds must reproduce byte for byte.
- **Capitals.** A fixed table written now for every country in the vocabulary (England and United Kingdom: London). A scene is dropped from MC (kn2 is untouched) when:
  - two of its six capitals share a first token (any of the three tokenizers, either case, with or without a leading space);
  - a capital shares a 4-letter stem with its own country's name, or is that name;
  - a capital shares a 4-letter stem with X's name.
- **Steps** (the competence gate, rendered with the scene's passage, as MP's):
  - the say question;
  - the direct capital, "What is the capital of {country}?".
  - The closed-book control set adds C0, the direct capital with no passage.
- **Knock-out.** ablate_v2 exactly as note 29b's named run (band; paper10, paper10_rot, unembed10, paper10_pcasize; --tasks-level all --kinds clean --read cand2; same batch), words MC only. The existing MP and MM rows (the v5key2 runs) are reused unchanged (same code path, deterministic).
- **Contrast.** MC's paper10 loss minus its direct-capital step's loss (its own knock-out rows), as note 29's MP contrast. Bootstrap over items, as note 29. Answer exclusion: MC items whose capital's first-token J++ row is among the removed top-10 at any band layer are dropped from the primary (reported both ways).
- **Reading** (per model):
  - MC "needs": contrast >= 15 points with its interval above 0; the same contrast under paper10_rot < 5; and MC's contrast minus the same contrast under paper10_pcasize >= 10.
  - "dissociation": MC "needs", MP does not ("goes around", or not beyond paper10_pcasize as on the 27B), and MC's minus MP's contrast >= 10 points, interval above 0, paired on scenes where both are gated ok.
  - "both need": MP needs too. "neither": MC does not need. Otherwise "unclear".
  - The J-space paper's framing predicts "both need"; ours predicts "dissociation".

##### Note 36: the route swap in the conflict (jsuite_v5kc2)
- **Items.** CN, CA, DN and DA with an unedited answer.
- **Donor D.** A bridge of the same relation from the set's pool, drawn with random.Random(scene suffix) and shared by the scene's four words. D is not among the scene's six entities. Its true value differs from X's true and false values and from the five other values in the passage. Its name token differs from X's.
- **Edit.** At every band layer, at site s1 (note 34): jswap_pointer's swap_neutral, with k = 10. X's top-10 J++ part is replaced by D's top-10 J++ part from the neutral sentence ("A reader asked a question about D in the letters page."). Controls: swap_neutral_rot, swap_neutral_u, paste_neutral.
- **Answers.** cand2 among the relation's vocabulary. Classes: donor (D's true value), memory (X's true value), passage (X's false value), other.
- **Primary.**
  - (a) Plain words (CN, DN): the donor share among items answered memory unedited, under swap_neutral minus under swap_neutral_rot.
  - (b) "According to" words (CA, DA): the same among items answered passage unedited.
  - (a) minus (b) is paired by scene.
- **Reading** (named and described separately, then pooled):
  - "route-conditional": (a) >= 20 points with its interval above 0, and (b) <= (a)/3 with the interval of (a) - (b) above 0;
  - "both routes move": (b) >= 2/3 of (a);
  - otherwise "unclear".
- **Descriptive.** The change in the passage and memory shares under the edit (does the edit move which source wins?), and the plain items answered passage unedited.

##### Amendment 63 addendum (Zach, 2026-10-30 ~04:20 UTC; after a red-team, before any full run; seen: only note 36's 9B smoke, n = 8 per word, as a mechanics check)
Zach's MC answer: "#2 fixed + slim #1". **Note 36 is dropped and not run.** Its result is mostly predictable from the C2 swap (memory recalls move 45-70 points; 27B lookups stay in 99%). Its two arms condition on different items: plain on items memory already won, "According to" on nearly all. Its code stays unused.

**Note 35 changes**
1. **Arm MC0: the MC question closed book (no passage).**
   - It sits in the control set (jsuite_v5kn2cctl). Candidates are the same six capitals.
   - It is gated on closed-book steps: H1 (the say question) and C0 (the direct capital).
   - Its knock-out is exactly MC's. Its contrast is MC0's paper10 loss minus C0's, from its own knock-out rows.
   - Why: MC's passage names X's country. MC could therefore route through the passage (find X's country's line, then the one-step capital of a named country). That would read as "goes around" without testing composition from memory.
2. **Joint readings** (per model; MC and MC0 each read with note 35's "needs" rule; "does not need" means a contrast < 10 with its interval's upper end < 15):
   - "memory computation needs it": MC0 needs and MC needs. With MP's existing reading, keys into the context are the exception.
   - "through the passage": MC0 needs, MC does not.
   - "only saying needs it": MC0 does not need.
   - otherwise "unclear".
   - Note 35's paired MC-vs-MP comparison is kept. MC0 is compared with MP on scenes gated ok for both, the same way.
3. **Margin matching** (descriptive, beside the primary). MC, MC0 and MP items are binned by their unedited cand2 margin (the right candidate's logit minus the best other's; 5 quantile bins of the pooled margins). Each arm's contrast is recomputed within bins and averaged with MP's bin weights. If margins are not recorded, this is reported as not available and not computed.
4. **Answer exclusion** covers every position the knock-out edits: all positions, every band layer.

**Note 34 changes**
1. **The primary reading is lens vs random** (the same dimension, both trained, the only fair pair):
   - "lens no better than random": AUC_J <= AUC_R + 0.05;
   - "lens better": AUC_J >= AUC_R + 0.10, intervals not overlapping;
   - otherwise "unclear".
   - The full-state comparison (AUC_F vs AUC_J) is no longer a reading.
2. **F is descriptive, beside a memory-strength baseline B:** the closed-book named recall's (H2, kc2ctl controls) answer margin for X, or its correctness if no margin is recorded. "F adds beyond memory strength" if AUC_F >= AUC_B + 0.10, intervals not overlapping.
3. **Time course** (descriptive): AUC_F and AUC_J at every 4th layer at s1 and s3. Beside it: the first layer at which the J++ top-1 among the candidates at s3 is the item's eventual answer for >= 50% of items.
4. **Unchanged:** the claim read (fixed list, shuffled control and reading), the sites, the items and the probe procedure.

**Runs.** After DeepSeek's EXIT: the 27B on GPU 0; Lightning then the 9B on GPU 1. Each model runs note 34 (extraction, then the reader) and note 35 (MC and MC0: competence, controls, knock-out, reader). A 9B smoke of at most 8 items per word comes first.

##### Amendment 63, second addendum (Zach, 2026-10-30 ~04:45 UTC; after the builders' 9B smokes, mechanics only, before any full run)
- **Note 35's answer exclusion: "any form" is the primary** (Zach's MC answer).
  - paper10 protects the dictionary rows of the clean top-10 output tokens at the answer position. So the capital's read token (its first token as the reply starts it) is never removed, and the letter of note 35 ("exact") excludes nothing.
  - Other forms of that first token (either case, with or without a leading space) were removed somewhere in about 50-70% of the smoke's items.
  - The primary therefore drops MC and MC0 items where any form was removed at any edited position and any band layer (scripts/nn_v5_mc_removed.py re-runs paper10 with the chosen rows written out; its reads reproduce the knock-out's).
  - "Exact" and "all items" are reported beside. The primary stratum is split_ok/anyform.
- **Implementation choices recorded** (no reading changes):
  - Note 35:
    - The knock-out uses --kinds clean step2, as note 29b's run did; the contrast needs the step rows.
    - MC0 sits in jsuite_v5kn2c with an empty context (its steps are exactly H1 and C0). It is gated by v4_split as MC is, which also requires the closed-book guess to be wrong.
    - The bootstrap is over bridges, as note 29's key() reader does.
    - Drops: 325 of 602 kn2 scenes are kept. Mexico City's stem rule removes every Mexico scene, and Bogota / Buenos Aires share a first token.
    - jsuite_v5kn2c sha d425909e, kn2cctl sha 24ab02e4. The existing builds reproduce byte for byte.
    - 28 MC passages' filler mentions "London"; they are recorded and reported beside.
  - Note 34:
    - The script is scripts/nn_provenance.py, because nn_probe.py already exists.
    - J, R and U are one block of coordinates per relation (zeros elsewhere; 236 columns). A single basis over all relations' tokens is reported beside.
    - B is the H2 closed-book cand2 margin, computed by the script (one value per bridge); correctness is reported beside.
    - The probe is a custom L-BFGS logistic regression on sklearn's objective (sklearn is not on the box).
    - Named is primary, as for this set family.

##### Amendment 63, correction (Zach's session, 2026-10-30 03:35 UTC; no run has started)
The clock times in the headers of amendment 63 and its two addenda are wrong: I misread the time zone. The commits are the record:
- amendment 63: 9dc2a241, 02:53 UTC;
- the first addendum: b65db57d, 03:11 UTC;
- the second addendum and the code: 134a3154, 03:31 UTC.

All are before any full run of notes 34 and 35; their jobs wait on DeepSeek's EXIT. The jobs are named "-1030-0055". The repo's earlier jobs use the box's UTC clock for their names; this one does not. The jobs were launched at 03:31 UTC (23:31 EDT, 29 Oct).

#### Amendment 64 (Zach, 2026-10-30 05:10 UTC by the box clock; before any code or run of it): note 37, answer kept vs answer only (v4)
Zach's MC answer (30 Oct, ~05:00 UTC): run "D" Friday morning, after notes 34-35. Why:
- Neel's "answer swaps dominate".
- paper10 protects only the clean top-10 output tokens' rows; other forms of the answer can still be removed (note 35's smoke).
- The two tracks disagree. Dan's one-layer test: keeping the answer word's directions keeps 0.92-0.98 of the recall's loss. Our note 15: the lens part's effect is the answer.

##### Note 37
- **Data.** v4 (jsuite_v4_test_chat), MP and MM, note 20's gate (v4_split), each model's main band: 9B L12-16, 27B L32-40, Lightning L27-33. --tasks-level all --kinds clean --read cand2, as note 20's runs.
- **Conditions:**
  - paper10_keepA (new): paper10's removal r at each edited position and layer, then r' = r - P_A r. A spans the J++ unit vectors at that layer of every form (either case, with or without a leading space) of every answer in the item's relation vocabulary: its cands2 rows, the rows ansJ uses. The answers' directions are thereby kept.
  - paper10_keepA_rot (new): r' turned by paper10_rot's rotation.
  - ansJ and ansJ_rot (existing, amendment 58 note 3, never run on v4): removing only the answer vocabulary's J++ span, at all positions.
  - ansU (existing): the same with the logit-lens rows (control).
- **Measures.** Loss (points among items right unedited) per twin and condition; gap = MM - MP; bootstrap over bridges (2000).
- **Reading** (per model):
  - "the recall's J-need is its answer's directions": MM's keepA loss minus keepA_rot loss <= 1/3 of MM's (paper10 - paper10_rot) loss, and the keepA gap < 10 with its interval's upper end < 15;
  - "beyond the answer": that ratio >= 2/3 and the keepA gap >= 10 with its interval above 0;
  - otherwise "partly".
  - Beside: ansJ's gap as a share of paper10's gap (v3 gave 0.56-0.75), with ansU as its control; and the answer log-prob change.
- **Descriptive.** The same on jsuite_v4cc's gated items, where the readout's top-1 is the cue, not the answer.
- **Order.** After notes 34-35 on each GPU; a 9B smoke (<= 8 items per word) first.

##### Amendment 64 addendum (Zach's session, 2026-10-30, before any full run of note 37; seen: only the builder's 9B smoke, n = 11 prompts, as a mechanics check)
- **The kept span A for paper10_keepA uses "every form"** (--keepA-forms every): the item's cands2 rows plus the same answers' first tokens with a leading space, either case.
  - Note 37's text says both "every form (either case, with or without a leading space)" and "its cands2 rows, the rows ansJ uses". On v4 these differ: cands2 holds only non-leading-space first tokens (often single letters), and the whole-word tokens appear only in the leading-space forms.
  - "Every form" matches the note's purpose and Zach's any-form choice for note 35.
  - ansJ, ansJ_rot and ansU keep cands2 only, as amendment 58 note 3.
- **paper10 and paper10_rot are rerun inside note 37's runs,** so every keepA comparison sits in one run with the same batches. The reader checks them against note 20's stored rows.
- **Loss** follows nn_ko_read (gated items). "Among items right unedited" is reported beside it.
- **The v4cc subset is reported four ways:** all, conflict, aligned and cue_top1. cue_top1 means the J++ top-1 share for the cue beats the item's answer at the description end, from nn_readout_v4cc.
- **When MM's (paper10 - paper10_rot) loss is <= 0, the ratio is "not read".**
- **Behaviour of existing conditions is unchanged.** keep_span defaults to None. A CPU unit check shows the new removal_edit is bit-identical, and a 9B smoke on old vs new code gave 66/66 shared rows bit-identical.

##### Amendment 62, cancelled (Zach, 2026-10-30 ~05:42 UTC; before any DeepSeek step ran)
Zach's MC answer: "Stop DeepSeek". After the novelty review, a mixture-of-experts breadth row ranks below the new experiments on the three main models; Neel's earlier advice was no mixture-of-experts side checks.
- The waiting job ds-1030-0125 was stopped before Muse's last step ended. Muse's weights were not dropped and DeepSeek was not downloaded. Its log is set aside as .cancelled; no EXIT was written.
- The waiting chains for notes 34, 35 and 37 were stopped (none had started) and relaunched with no DeepSeek wait (suffix -1030-0543). GPU 0 runs the 27B now; GPU 1 runs Lightning, then the 9B, after Muse's last step.

#### Amendment 65 (Zach, 2026-10-30, box clock at commit; before any code or run of it): notes 38-39, the answer line closed and tested on the paper's own prompts
Zach's MC answer (30 Oct ~06:05 UTC): "#1 Size loophole + paper's prompts". Why:
- Notes 11-13 show that the J-space paper's intermediate swaps act through the relation's answer directions. That is our strongest result with no prior version.
- Two loopholes are open:
  1. Note 11 never logged how much of the edit the scrub removes ("the scrub made the edit tiny").
  2. Its only scrub control is random atoms ("size, not semantics").
- The result has also never been run on the paper's own items (data/probe_swap.json, 90 two-hop prompts with the paper's swap targets).
- Design from /home/zach/scratch/redteam_1030/brainstorm_answer_line.md, sections B and A.
- Models: 27B, 9B, Lightning; Muse (its own J++) descriptive if it fits. One deterministic run per model.

##### Note 38 (first): closing the size and semantics loopholes of notes 11-13 (v3, existing items)
- **Items.** Note 11's own jobs: v3 rendering 0, RM and PM at each model's band, donor seed 0. The raw arms are rerun in-run and checked against note 11's stored rows.
- **New nn_swap conditions** (insert donor, k = 10):
  - insert_k10_noansrel_nm: the scrubbed edit rescaled per row to the unscrubbed edit's norm.
  - insert_k10_noansrel_x2 and _x4: dose.
  - insert_k10_noansoff: another relation's vocabulary scrubbed, count-matched (film-director surnames for the four country-type relations; demonyms for films).
  - insert_k10_noansform (people only): the country names scrubbed instead of the demonyms.
  - insert_relans: sufficiency, h_X + P_Arel(e).
  - clamp_noans_nm: clamp_noans's delta rescaled to the clamp's norm.
- **Logged per row:** ||P_Arel e||^2 / ||e||^2 and ||P_C e||^2 / ||e||^2.
- **Window sweep:** noansrel_nm and relans over note 11's sweep windows (RM and PM, 80 each).
- **Read.** cand2 transfer (donor - third), beyond rotated, as note 11.
- **Readings** (per model):
  - B1: noansrel_nm transfer <= 1/3 of the swap's -> "inert at matched size". If >= 1/3 -> "the null was partly a size effect", and the slide wording drops to "mostly".
  - B2: noansoff keeps >= 2/3 while noansrel keeps <= 1/3 -> "the scrub is specific to the asked relation".
  - B3: relans >= 2/3 of the swap -> "the answer subspace is sufficient".
  - B1 + B2 + B3 together give "necessary, sufficient, specific and size-controlled".
  - Descriptive: the norm shares, the dose curve, noansform, clamp_noans_nm.

##### Note 39 (second): the paper's 90 two-hop prompts, decomposed
- **Items.** data/probe_swap.json. The primary set is items whose answer type has a closed vocabulary of >= 8 values (capitals, languages, continents, colours, numbers, states of matter, first names, months, seasons, countries, US states, currencies, oceans). One-off answers are reported with the own-pair scrub only.
- **Category vocabularies** are written by a CPU agent from the type label alone, with no model access, and frozen before any run (sha256 recorded in a follow-up addendum before the smoke).
  - Each covers every form of each value's first token (case; with or without a leading space).
  - Every token of the item's intermediate and swap_to names is excluded.
  - Items whose answer type equals the intermediate's type go to a side table.
- **Gate.** exp02's: the clean greedy continuation has the answer and not the swap answer; single-token first-token scoring. Raw "stripped" prompts are primary; chat prefill is the fallback only for a model with fewer than 50 raw-eligible items.
- **Swap.** The paper's coordinate swap (SwapClamp on the unit J++ vectors of intermediate <-> swap_to, positions 1..), as exp02's raw_jlens.
- **Arms**, all at the same windows:
  1. bridge (the paper's swap);
  2. answer (answer <-> swap_answer);
  3. bridge_noA (bridge atoms orthogonalised to the category span A, then swapped);
  4. bridge_noA_nm (arm 3 rescaled per position to arm 1's edit norm);
  5. bridge_onlyA (the bridge atoms projected onto span(A), renormalised, swapped);
  6. bridge_offA (arm 3 with another category's vocabulary of the same count);
  7. bridge_randA (arm 3 with as many random letter-token atoms);
  8. bridge_ownA (only the own answer pair);
  9. the matched-norm null for arms 1, 2 and 5.
- **Windows.** The paper's cumulative windows from the workspace start:
  - 27B: L16 -> 20, 24, ..., 60;
  - 9B: L6 -> 8, 10, ..., 30;
  - Lightning: L8 -> 12, 16, ..., 48;
  - plus each model's main band (27B L24-40, exp02's).
- **Read.** Top-1 next token = swap_answer's first token ("flip"), with delta log p beside. Greedy check on the main band for arms 1, 2, 3 and 5. Logged per row: ||edit|| / ||h|| and the share of arm 1's edit inside span(A).
- **Lenses.** Published J++; on the 27B also the plain J-lens.
- **Bootstrap.** Clustered by answer category.
- **Readings** (per model):
  - A0: arm 1 at the main band flips >= 30 points above its null (exp02 found 49 on the 27B); otherwise that model's A readings are void.
  - A1 (primary), at the main band and at the window of arm 1's median onset: K = (arm 3 - null) / (arm 1 - null).
    - "answer-carried": K <= 1/3;
    - "intermediate beyond the answer": K >= 2/3;
    - otherwise "partly";
    - valid only if arms 6 and 7 keep >= 2/3 (otherwise "scrub not specific").
  - A2: arm 4 <= 1/3 of arm 1 confirms A1. If arm 4 >= 1/3 while arm 3 <= 1/3 -> "non-answer content is causal but small".
  - A3: "Frenchness is sufficient" if arm 5 >= 2/3 of arm 1 at the main band.
  - A4 (timing), with onset = the smallest window end at which an arm flips:
    - "the paper's timing replicates": median onset(answer) - onset(bridge) >= 2 layers, paired CI above 0;
    - "the timing lead is answer-category content": that, plus median onset(arm 5) <= onset(arm 1) + 1, plus arm 3 never above its null + 10.
  - Descriptive splits: word vs number answers; low vs high bridge/answer overlap; J++ vs plain J-lens on the 27B.
- **Held-out caveat.** The 27B's exp02/exp14 numbers were seen before (14-15 Oct), so only the 9B, Lightning and Muse results are a clean held-out test, and the slides say so.

##### Amendment 65 addendum, note 38 (before any full run; seen: the builder's two 9B smokes, n = 8, as mechanics checks only)
- **Implementation choices recorded** (no reading changes):
  - **Sweep arms.** The sweep adds insert_k10 (checked against note 11's stored sweep) and insert_k10_rot.
  - **"Beyond rotated".** Means transfer(cond) - transfer(insert_k10_rot); a share is beyond(cond) / beyond(insert_k10). Clamp arms are read beyond clamp_null.
  - **Not-read rule.** A model's readings are not read if the swap beyond rotated is under 10 (note 11's k10 < 10 rule).
  - **Words and the stored check.** Words are RM and PM only, so batches differ from note 11's (which had MM). The stored-row check reports identical-row counts.
  - **Logged shares.** share_rel and share_c are computed on clean states, averaged over band layers and site rows. The nm / x2 / x4 rescaling uses the in-run edit.
  - **clamp_ratio** = ||delta_noans||^2 / ||delta_clamp||^2 summed over positions, averaged over layers. This definition was fixed after smoke 1, because a per-position ratio blew up.
- **Other-relation vocabularies** (n38_vocab.json per run):
  - For the four country relations, the films relation's 27 director surnames; for films, people's 34 demonyms.
  - They are count-matched on atom rows (subsampled with Random("n38off:"+rel) or padded from C's atoms).
  - noansform (people) uses the 34 DEMONYM countries and is not count-matched.
- **Scope and behaviour.**
  - relans has no same-size control beyond share_c.
  - Muse is not included: it has no note 11 v3 jobs.
  - Existing conditions are byte-identical with the edited nn_swap.py (two 9B smokes, 28 existing conditions).

#### Amendment 66 (Zach, 2026-10-30, box clock at commit; before any GPU run of it): note 40, the first necessity test of "silent dissent"
Zach's MC answers (30 Oct ~06:40 UTC): five cells + the 1-peer cell; 27B, Lightning and 9B; mid band + the bridge pair + answer kept / answer only; J++ only. Design: /home/zach/scratch/redteam_1030/sd_necessity_design.md.
- **Setting.** Ni & Zou's plain transcript (arXiv 2610.02702 v2), ported in scripts/sd_prompts.py from their MIT code at commit fe78a9f. Their code is never imported or run.
- **Items.**
  - Their three 27B categories: landmark -> country -> capital; person -> birth city -> country; person -> undergrad university -> city.
  - Their bridge split and their known check, run per model; the test split; items right in round 0.
  - Items whose answers share a first token are left out of the edited reads.
  - TwoHopFact at its pinned revision (sha256 522d3764...).
- **Conversations.**
  - solo (round 0, no peers);
  - agree_vis and agree_hid (peers state the agent's own answer; earlier answer visible / hidden);
  - press_vis and press_hid (3 peers, answer pressure);
  - press1_vis (1 peer).
- **Edits**, at every position at the mid band (27B L32-40, 9B L12-16, Lightning L27-33):
  - paper10, paper10_rot, paper10_pcasize, unembed10;
  - bridgeJ and bridgeJ_ctrl (the item's own bridge forms vs the control fact's, minus both answers' forms);
  - paper10_keepA and ansJ (as note 37).
  - At their late band (27B L52-55, 9B L26-29, Lightning L42-45): paper10 and paper10_rot, descriptive.
- **Outcome.** The top token at the answer position, classed orig / peer / ctrl / other. Their 12-token outcome is run unedited only.
- **Readout.** J++ hit@100 (original bridge minus control bridge; original answer minus control answer), descriptive.
- **Readings** (sd_necessity_design.md section 4, implemented in scripts/nn_sd_read.py). Effects are paired by item; 95% bootstrap over bridges (2000, Random(0)); spec = the paper10 effect minus a control's on the same items.
  - **G0, 27B reproduction.** Unedited press_vis gives in within 10 points of 38.9% and press_hid within 10 of 72.7%. The first-token read must agree with the 12-token class on >= 90% per conversation. Otherwise every reading is labelled "protocol not reproduced".
  - **G1, the knock-out bites.** In solo, paper10's spec loss is >= 20 against every control, with the interval's lower end > 0. Otherwise that model has no necessity reading.
  - **G2, lookup spared.** paper10's loss in agree_vis and agree_hid is <= max(10, solo loss / 3). Otherwise R1-R3 are "not recall-specific".
  - **R1, per pressure cell, both required.** The spec give-in gain has a lower end > 0 against every control, and gain / loss >= 0.5. If the gain is specific but most lost answers are "other": "moves answers, not to the peers".
  - **R2.** f = the specific flip (paper10 minus paper10_rot) among items that held unedited.
    - "with its answer in view, holding is a lookup": f(vis) <= f(hid) / 3 and press_vis's spec-gain upper end < 10;
    - "it recomputes even with its answer in view": f(vis) >= 2/3 f(hid) and press_vis's spec-gain lower end > 0;
    - otherwise "partly"; not read if f(hid) <= 0.
  - **R3**, bridgeJ - bridgeJ_ctrl (gain in press_hid and press_vis; loss in solo), on items with both spans non-empty:
    - "the bridge's own directions are needed": lower end > 0;
    - "not the bridge's own direction": upper end < 5 and R1 holds;
    - otherwise "unclear".
  - **Descriptive:** the late band; the 1-peer cell; keepA and ansJ; without bridge-named items; per category.
- **Falsifiers** of the recall-vs-lookup prediction:
  - give-in rises equally with the answer visible and hidden;
  - rotated or same-size removal does as much;
  - most knock-out answers are "other".
- **Held-out caveat.** Their 27B rates are published, so the 9B and Lightning are the clean held-out tests.
- **Data.** data/sd_v1/facts.jsonl is derived from TwoHopFact (CC-BY). It is not committed (gitignored); it is rebuilt with scripts/sd_build.py facts from the pinned CSV.

##### Amendment 65 addendum, note 39 (before any full run of it; seen: one 9B smoke on 6 hand-picked items, mechanics only, results not interpreted)
- **Frozen vocabulary.** data/paper_answer_types.json, sha256 a93fc6342cf6fa1d59a5af9370e324bf40cc6cce5b030fe95312935f24b2abf0. Built by scripts/paper_answer_types_build.py with tokenizers only, before any note 39 forward pass; read-only, and the runner checks the hash.
  - probe_swap.json has no answer-type field, so each item's type was assigned from its question and answer text.
  - Primary set: 63 items. Side table: 3 (two by note 39's rule, plus ex2-city-continent-Sydney, whose answer is also the intermediate's token). Own-pair-only: 24.
  - Small closed sets were padded to >= 8 values with synonyms.
  - Lower-case and no-space first-token forms are kept (literal rule).
  - Each item's scrub set includes its own answer and swap answer.
  - Arm 6 uses off-category chains, matched to the scrub set's token count.
- **Main bands.** Each note 20 band extended earlier by 1/8 of depth, as exp02's L24-40 extends the 27B's L32-40: 9B L8-16, Lightning L20-33, Muse L29-42. Muse's windows follow Lightning's (both have 52 blocks).
- **Lenses.** Lightning and Muse use our own J++ (no published one exists); the 27B uses the published J++ plus the plain J-lens.
- **Choices.**
  - **Arm 4** is rescaled per position and layer to arm 1's edit on the same residual (exp02's matched-norm convention).
  - **"Flip"** means the swap answer is strictly rank 1 among word tokens; the raw top-1 and number twins are logged beside.
  - **Onset** is the median_high of arm 1's onsets.
  - **Arm 3 null:** arm 3 uses arm 1's null. A3 subtracts arm 5's own null.
  - **Bootstrap** clusters are answer types (about 13).
  - **Own-pair-only items** run arms 1, 2, 8 and the nulls.
  - **Section E** (composition) is not part of note 39.
- **27B reproduction gate.** Arm 1 at L24-40 must fall inside exp02 main_v4_jpp's Wilson 95% interval on the shared items, or the run stops before any window.
- **Seen before the freeze:** about 5 rows of exp02 main_v4_jpp outcomes, while checking that file's format.

##### Amendment 66 addendum (Zach, 2026-10-30, box clock at commit; before any note 40 result exists): our dataset practices applied to the silent-dissent items
Zach's MC answer: "All of it". Why: TwoHopFact's chains are mostly shortcut-prone. The final answer is reachable from the first entity without the bridge (person -> nationality; university -> country; landmark -> capital; person -> city). Their known check covers our first step, second step and whole, but not our guess control, name filter or a shortcut test.
- **A new gate stage per model** (closed book; greedy 12 tokens, their prompt prefix, alias match, as their known check). Prompts per item:
  - **guess:** the composed question with e1 replaced by a generic noun ("the person" / "the university" / "the landmark"). The item passes if the answer is NOT e3.
  - **direct (shortcut):** a direct e1 -> e3 question per category. Fixed templates:
    - person-birthcity-cntry: "{e1} is a citizen of the country of";
    - person-uguniv-hqcity: "The city most associated with {e1} is";
    - landmark-cntry-capital: "The city most associated with {e1} is".
    - The item is flagged shortcut-available if the answer matches e3. The templates are approximations and are reported as such.
- **Name/stem filter:** an item is dropped if e1 or e2 (any alias) contains e3 (any alias) as a word, or shares a 4-letter stem with it (e.g., "University of Chicago Law School" -> Chicago), in addition to their bridge-named flag.
- **Strata:**
  - **Gated** = their known check + guess wrong + name filter. G0-G2 and R1-R2 are primary on the gated set; the ungated (their) set is reported beside.
  - **No-shortcut** = gated and not flagged shortcut-available. **R3 (the bridge-specific test) is read only on the no-shortcut subset**, and needs >= 30 items per model; otherwise it is "not read (too few no-shortcut items)". R1-R2 are also reported on the no-shortcut and shortcut subsets, descriptively.
- **The knock-out runs are unchanged** (they run every known item); the strata are applied in the reader.

##### Amendment 65, second addendum, note 39 (Zach, 2026-10-30, box clock at commit; seen: note 39's 9B and Lightning readings, where the arm 6 guard failed, arm 6 keeping 0.11 and 0.15)
Zach's MC answer: "Overlap check + better control". Arm 6's other categories were drawn from the same domain as the answer type (e.g. languages for capitals). Our hypothesis, untested: those spans overlap the intermediate's own directions, so arm 6 also removes the bridge. Changes, fixed before any overlap is measured:
- **Overlap diagnostic** (descriptive; lens files only, no forward pass). For each item, model and main-band layer: the share of the energy of the bridge atoms (intermediate and swap_to unit J++ vectors) inside:
  - the answer span A;
  - arm 6's span;
  - each category span of an unrelated pool: colour, shape, unit, occupation, weekday, month, number, state of matter;
  - 20 random letter-token spans of A's size.
  A pool category is used only when it is not the item's own answer type.
- **Arm 6b, replacing arm 6 in the A1 validity guard.** For each item, the unrelated-pool category with the smallest bridge-atom share, count-matched to A's token count (subsampled with Random("n39b:"+item), or padded from random letter tokens). Ties go to the order listed above.
- **The guard is otherwise unchanged:** A1 is valid only if arm 6b AND arm 7 keep >= 2/3. Arm 7 is not changed. So Lightning's A1 stays invalid if arm 7 again keeps < 2/3.
- **Rerun** of arms 1, 3, 6b, 7 and the null on the primary items, at the main band and at arm 1's median-onset window, on the 9B, Lightning and 27B; Muse descriptive. Arm 1 and the null are rerun in the same job and checked against note 39's stored rows.
- **Reading.** A1 is re-read with arm 6b. The old arm 6 result is reported beside it, labelled "same-domain control, invalid as a guard".

##### Amendment 66, second addendum (Zach, 2026-10-30, box clock at commit; before any gated note 40 reading; seen: name-filter counts only, plus the builder's 8-item gate smoke)
Zach's MC answer: "Names as written". The registered name filter (any alias of e1/e2 contains any alias of e3) drops about half of the birth-city items, almost all through Wikidata disambiguation aliases ("Salzburg, Austria"). That is a format artefact: the bridge is never shown in the prompt.
- **The primary name filter is names as written:** e1, e2 and e3 with no alias lists, contained as a word or sharing a 4-letter stem (scripts/sd_gate.py name_drop_canonical, reader --name-rule canonical).
- **The alias-based rule is reported beside**, labelled as the originally registered rule.
- Everything else in the first addendum is unchanged: the guess control, the direct shortcut flag, the strata, R3 only on no-shortcut items with >= 30, and G0's like-for-like check on the ungated set.

#### Amendment 67 (Zach's session, 2026-10-30, box clock at commit; Zach delegated queueing to 12:00 ET; before any code or run of it): the skeptic's must-run checks on notes 37, 39 and 40
Source: /home/zach/scratch/redteam_1030/skeptic_1030.md (an adversarial read of tonight's results). Seen: notes 37, 38 and 39 readings; note 40's 9B gated and ungated readings and Lightning's ungated readings. Models: 9B, 27B, Lightning; one deterministic run each (Lightning's reruns are not bit-identical, as recorded).

##### Note 41: random-span placebo and output-side check for note 37 (v4, note 20's gate and bands; ablate_v2)
- **New conditions:**
  - **paper10_keepR (+ _rot):** as paper10_keepA, but the kept span R is spanned by the unit J++ vectors of N random letter-token rows. N = the item's A row count (rank-matched). Rows are drawn with Random("n41:" + item id), excluding A's rows and the protected rows.
  - **ansR (+ _rot):** as ansJ, but removing R's span at every position.
- **Output-side run.** A separate run with --positions final and conditions paper10, paper10_rot, ansJ, ansJ_rot.
- **Readings** (per model):
  - "**answer-specific keep**" if keepR's net MM loss (keepR - keepR_rot) >= 2/3 of paper10's net loss while keepA's ratio stays <= 1/3; "**size, not answers**" if keepR's ratio <= 1/3 as well; otherwise "partly".
  - "**answer-specific removal**" if ansR's gap <= 1/3 of ansJ's gap.
  - ansJ at the final token only: "**largely output-side**" if its gap is >= 1/2 of ansJ's all-position gap; "**upstream**" if <= 1/4; otherwise "mixed".

##### Note 42: position split for note 40's visible-answer effect (silent-dissent transcript; nn_sd_necessity)
- **New conditions** at the mid band:
  - **paper10_skipown (+ _rot):** paper10 at every position except the tokens of the agent's own earlier answer;
  - **paper10_onlyown (+ _rot):** only at those tokens.
- **Conversations:** press_vis and press1_vis. The gated set is primary (amendment 66 addenda, names as written). Models: 9B, Lightning, 27B.
- **Reading** (specific give-in gain, as R1):
  - "**a lookup disruption at the earlier answer**" if onlyown gives >= 2/3 of paper10's gain and skipown <= 1/3;
  - "**not at the earlier answer's tokens**" if skipown >= 2/3 and onlyown <= 1/3;
  - otherwise "both".
- **Descriptive:** whether the solo recall survives, and the give-in, by category.

##### Note 39 arm 5R: a random-projection control for sufficiency
- **Arm 5R:** the bridge atoms projected onto a random span of A's dimension (random letter tokens, Random("n39r:" + item), excluding A and the item's name tokens), renormalised, then swapped. It runs with the arm 6b reruns.
- **Reading:** "**sufficiency is answer-specific**" if arm 5 - arm 5R >= 1/3 of arm 1's net, with the interval above 0; otherwise "**not answer-specific**".
- **Descriptive:** sufficiency without the capital/language/country items.

##### Wording fixed now, whatever these show (the skeptic's list)
- **Note 40:** a 9B result (Lightning ungated null); neither "memory" nor "conformity"; the hidden case is "not readable"; R3 is not quoted (its n is at the threshold, and the control bridge moves the other way).
- **Note 37:** "the ~130-dim span of the relation's answer-word J++ vectors"; ansJ is all positions and unprotected; on Lightning about half of ansJ is shared with the logit lens.
- **Note 38:** Lightning RM fails the specificity guard; the answer part alone reproduces 86-112%; one donor seed.
- **Note 39:** sufficiency is not established on the 9B; it is driven by capital/language items; necessity is unreadable on Lightning.
- **Note 35:** not "Lightning dissociates". Composition needs the J-space about equally on Lightning and the 27B; Lightning's key lookup does not.

##### Amendment 67 addendum, note 41 (before any note 41 code runs; seen: the deepen agent's CPU numbers on the 9B silent-dissent rows (keepA's edit is ~0.05 of |h| vs paper10's ~0.085))
- **Energy-matched keeps.** Added: paper10_keepR2 and paper10_keepR4 (+ _rot each), random letter-token spans of 2x and 4x A's row count (same seeds, nested), together with keepR (1x).
- **Logged per row:** the fraction of paper10's removal energy that each kept span retains (A, R, R2, R4).
- **Primary reading** (replacing note 41's keepR rule; the ansR and final-only rules are unchanged):
  - **"answer-specific keep":** at the random keep whose retained energy is closest to (and not below) A's, the net MM loss ratio is >= 2/3, while keepA's is <= 1/3.
  - **"energy, not answers":** a random keep retaining no more energy than A has a ratio <= 1/3.
  - Otherwise **"partly"**.
- **Descriptive:** rescue as a function of retained energy, A vs the random keeps.

##### Amendment 66, third addendum (before any 27B note 40 reading; seen: the 9B gated and ungated readings, Lightning's ungated readings, and the deepen agent's 9B log-odds numbers)
- **Headroom-robust comparison** (a secondary reading, read on the 27B and Lightning gated sets; on the 9B only descriptive, since seen).
  - The knock-out's specific effect on holding is measured in log-odds: logit P(hold | paper10) - logit P(hold | paper10_rot), among items right in solo. It is computed for press_vis and press_hid, with an item-bootstrap over bridges.
  - **"Visible > hidden in log-odds":** the visible-minus-hidden difference has its interval below 0, i.e. the knock-out lowers holding more when the answer is visible.
  - **"Hidden >= visible":** the interval is above 0.
  - Otherwise **"no difference"**.
- **Bridge control.** R3 stays unquoted (amendment 67). If a bridgeJ_rot condition is run later, R3 is re-read against it.

#### Amendment 68 (Zach's session, 2026-10-30, box clock at commit; Zach delegated queueing to 12:00 ET; before any code or run of it): notes 43-45, the slate after the deepen, skeptic and frontier reviews
Sources: /home/zach/scratch/redteam_1030/next_deepen.md (E6, E7) and next_frontier.md (D1). Models 9B, 27B and Lightning, one deterministic run each (Lightning not bit-reproducible, as recorded); J++ only. Seen: every result logged up to note 39 on Muse.

##### Note 43: note 37 on a held-out v4 data draw (jsuite_v4p4002)
- **Pipeline:** competence, controls and the v4 gate as note 20's queue. The v4_split control-set mapping is fixed for the p4002 naming, behaviour-preserving for existing sets.
- **Conditions:** note 37's (paper10, paper10_rot, paper10_keepA, paper10_keepA_rot, ansJ, ansJ_rot, ansU; --keepA-forms every), plus note 41's keepR / keepR2 / keepR4 (+ _rot) and ansR (+ _rot) if note 41's code is committed before this run starts.
- **Reading.** "Replicates" = the same note 37 reading (and, if run, the same note 41 reading) per model as on seed 4001. The headline gap (MM - MP under paper10) is reported beside.

##### Note 44: answer or intermediate, on the closed-book capital question (jsuite_v5kn2c MC0; MC and the kn2 say twin as references; note 35's gate; main bands)
- **Conditions** (note 37's keep machinery):
  - keepCap: every form of every capital in note 35's table;
  - keepCty: every form of every country in kn2's say vocabulary, count-matched to keepCap's rows by seeded subsampling, Random("n44:" + item);
  - keepCapCty;
  - keepR at keepCap's retained energy (as note 41);
  - ansCap, ansCty, ansCty_rot.
  - paper10 and paper10_rot are rerun in-run.
- **Primary stratum:** all gated MC0 items. Note 35's anyform stratum is reported beside.
- **Rescue** = 1 - (net MM-like loss under keepX) / (net loss under paper10), on MC0's contrast as note 35's.
- **Readings** (27B and Lightning primary; 9B descriptive):
  - "answer only": rescue(keepCap) >= 2/3 and rescue(keepCty) <= 1/3;
  - "intermediate needed": rescue(keepCty) >= 2/3, or rescue(keepCap) <= 1/3 while rescue(keepCapCty) >= 2/3;
  - "both": keepCapCty >= 2/3 with each alone <= 1/3;
  - otherwise "unclear".
  - A rescue counts only if it beats keepR's by >= 0.33.
- **Beside:** ansCty's MC0 loss next to the say twin's loss, and the cross-overlap of the two spans.

##### Note 45: which named word the ablation needs, on the paper's own items
- **Items:**
  - the paper's lens-eval multilingual set (107 items, labels: language L, relation R, input-in-English I, output-in-English E);
  - the multihop set (data/lens_eval_multihop.json, 93 items, bridge = intermediates[0]);
  - the order-of-operations set, descriptive only.
  - The 7 multilingual items whose English pivot shares a first-token form with the target (cognates) are excluded from the pivot reading. No new item set is built.
- **Gate.** Raw completion, greedy 6 tokens, normalised prefix match; chat prefill only if a model has fewer than 50 raw-eligible items.
- **Read.** Delta log p and strict top-1 of the target's first token; a teacher-forced whole-target log p beside if built.
- **Conditions** at note 39's main bands:
  - paper10, paper10_rot, paper10_pcasize, unembed10;
  - keep_T (target);
  - keep_E, keep_I, keep_R, keep_L (multilingual); keep_B (multihop);
  - keep_ctl (a same-type word from another item, count-matched);
  - keepR (3 seeded draws, rank-matched);
  - rm_T, rm_E, rm_R, rm_L, rm_B, rm_ctl (+ _rot each), removal at all positions except the final one.
  - Early window (note 39's median onset): paper10, paper10_rot, keep_T, keep_E / keep_B.
  - Items where the kept word is in paper10's protected set are logged; the primary is on unprotected items.
- **Readings** (per set and model), with K = net loss under the keep / net loss under paper10:
  - **A0:** paper10 loss - max(rot, pcasize) >= 20 points with CI > 0; otherwise "the knock-out does not bite on this set".
  - **Validity:** K(keepR) >= 2/3 and K(keep_ctl) >= 2/3; otherwise "spans not specific".
  - **Multilingual:**
    - "English pivot carries it": K(E) <= 1/3 and K(T) >= 2/3;
    - "target word carries it": the reverse;
    - "shared concept": both <= 1/3;
    - "neither": both >= 2/3. Then R and L are read the same way.
    - Necessity: rm_E - rm_ctl >= 15 points with CI > 0 = "the English pivot is necessary" (the same for R and L).
  - **Multihop:**
    - "answer": K(T) <= 1/3 and K(B) >= 2/3; "bridge": the reverse;
    - early window: "the intermediate is needed early" if K_early(B) <= 1/3 and K_early(T) >= 2/3.
  - **Splits:** single- vs multi-token targets.
  - **Bootstrap** clustered by relation (multilingual) or answer type (multihop).

#### Amendment 69 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated queueing until 12:00 ET; before any code or run of it): notes 46-48, cheap replications for the idle GPU hours after the current queue
Seen before writing: note 41 on the 9B ("partly" keep; removal "not answer-specific"; "upstream"); note 45 on the 9B (A0 not met on every set); notes 38-40 and the arm 6b / 5R reruns. Order by research priority: note 44, note 42, then 46, 48, 47. Models 9B, 27B, Lightning; one deterministic run each.

##### Note 46: notes 37 and 41 on the codename set (jsuite_v5al; does the answer-direction account hold when the bridge is a passage-defined codename that evokes nothing?)
- **Knock-out:** the alias set's own command (note 31: words MP MM, kinds clean, the v4 gate with the v5alctl controls, main bands), with note 37's and note 41's conditions in one run: paper10, paper10_rot, keepA (+ _rot), keepR, R2, R4 (+ _rot), ansJ (+ _rot), ansR (+ _rot), ansU; --keepA-forms every.
- **Readings:** note 37's ("the recall's J-need is its answer's directions" etc.) and note 41's keep and removal rules, unchanged. A note 37 reading that differs from v4's is reported as such.

##### Note 47: note 40 on the silent-dissent dev split (replication and power for R1 and the no-shortcut R3)
- **Run:** the same knock-out (amendment 66; mid band; the same edits incl. keepA and ansJ; J++ only) on their dev split's known items. The gate (amendment 66 addenda, names as written primary) is applied by the reader.
- **Readings:** G1, G2, R1 and R2 on the gated dev items, and R3 on the dev no-shortcut items (>= 30), each read as note 40's.
- **"Replicates":** the same reading as on the test split. A pooled test+dev R3 is reported beside, descriptive.

##### Note 48: note 37 on a third v4 data draw (jsuite_v4p4003), with note 43's pipeline
- **Pipeline:** competence, controls and the gate, then note 37's and note 41's conditions.
- **"Replicates":** the same note 37 and note 41 readings per model as on seed 4001 (and as on p4002).
- With note 43, this gives three draws for note 37 (CLAUDE.md asks for >= 3 seeds before calling a result positive).

#### Amendment 70 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated queueing until 12:00 ET; registered before any note 43, 46 or 48 knock-out reading): note 41's keep reading at matched energy and in log-prob
Seen before writing:
- note 41's readings on seed 4001 for the 9B, 27B and Lightning;
- a post hoc CPU interpolation of seed 4001's stored rows (an agent's, not registered). Random keeps at keepA's own retained energy rescue about 0.42 / 0.34 / ~0 of the accuracy loss, and about 0.51 / 0.48 / 0.33 in answer log-prob. keepA rescues 0.93 / 0.95 / 0.91 and 0.96 / 0.97 / 1.02 (9B / 27B / Lightning).

Not seen: any knock-out reading of notes 43, 46 or 48. The 9B's p4002 knock-out was running at commit time, and its reader had not been run.

These forms are confirmatory only for notes 43, 46 and 48. On seed 4001 they are post hoc and labelled so.

- **Why.** Note 41's keep rule compares keepA with the nearest random keep that holds at least keepA's retained energy. On seed 4001 that keep (R2) held 10-14 points more of the removal's energy than keepA, so the registered rule favours "partly". The matched-energy form removes that offset.
- **Rule E (matched energy).**
  - R_rand(E_A) is the accuracy rescue of the random keeps (keepR, keepR2, keepR4, each net of its _rot as in note 41), linearly interpolated in retained energy at E_A, keepA's retained share of the removal.
  - If E_A lies outside the random keeps' energy range, the reading is "not interpolable" (no extrapolation).
  - "Answer-specific at matched energy": rescue(keepA) - R_rand(E_A) >= 0.33, with the bootstrap CI's lower end > 0 (note 41's item bootstrap, with the interpolation recomputed per resample). Otherwise "not shown at matched energy".
- **Rule L (log-prob).** The same comparison, with rescue measured in the gold answer's first-token log p on MM items: rescue_L(X) = 1 - (mean Delta log p under X, net of X_rot) / (mean Delta log p under paper10, net of paper10_rot). Same interpolation and thresholds.
- **Status.** Note 41's registered keep reading stays the primary for notes 43, 46 and 48. Rules E and L are registered secondaries, reported beside it. A "replicates" claim uses the registered rule. The removal reading (ansJ / ansR) and the final-only reading are unchanged.
- **Code.** The reader (nn_ko41_read.py, as used by notes 43 / 46 / 48) gains --matched-energy. It is built after this commit, and the registered output stays byte-identical.

#### Amendment 71 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated; registered before the 27B and Lightning note 44 readings, before any note 40 reading of the 27B, and before any note 47 reading): note 44's "either suffices" label; a held-margin secondary for notes 40 and 47; R3 inherits G2
Seen before writing:
- note 44 on the 9B (descriptive). Rescue was keepCap 0.92, keepCty 0.94, keepR 0.47, which mapped to "intermediate needed" because the rules have no both-suffice category.
- a post hoc skeptic pass on note 40's test split (9B and Lightning, gated, names as written). Among held press_vis items with clean margin > 0.5, paper10 minus the strongest control was +24 (9B) and +8 to +12 (Lightning), and keepA rescued 0.8 / ~1. Near-tie items (margin <= 0.5) were not rescued. These test-split numbers are post hoc and labelled so.

**Note 44.**
- Before the registered rules, if rescue(keepCap) >= 2/3 and rescue(keepCty) >= 2/3, each beating keepR's by >= 0.33, the reading is "either span suffices (the spans overlap)". It is reported with the two spans' cross-overlap and each span's retained energy.
- The registered label is printed beside it.
- This applies to the 27B and Lightning. On the 9B (already seen) it is post hoc.

**Notes 40 and 47: secondary reading M (held items with a real margin).**
- **Items:** gated items (names as written), press_vis, held in the unedited run (cls == orig) with clean margin > 0.5. The margin is the logit of the original answer's first token minus the peers' answer's, at the unedited answer read. A flip is cls != orig.
- **M1:** flip(paper10) - max(flip(paper10_rot), flip(paper10_pcasize), flip(unembed10)). "Specific caving on items held with a real margin" if >= 10 points with the bootstrap's lower end > 0 (note 40's bootstrap clustered by bridge).
- **M2:** keepA rescue = 1 - (flip(keepA) - flip(paper10_rot)) / (flip(paper10) - flip(paper10_rot)). "The answers' directions carry it" if >= 2/3, read only where M1 is met.
- The near-tie stratum (margin <= 0.5) and press1_vis are reported beside.
- **Status:** confirmatory for the 27B's test split (note 40) and every model's dev split (note 47); post hoc on the 9B's and Lightning's test split. Note 40's registered R1 stays the primary.

**R3 inherits G2.** Amendment 66 requires "not recall-specific" when G2 fails. The reader's R3 branch did not check G2 on the no-shortcut stratum. It now applies G2 on that stratum, and R3's label is "not recall-specific" when G2 fails there. This is a reader fix to match the registered rule. The 9B's test-split R3 is therefore "not recall-specific" (G2 fails on its no-shortcut stratum: agree_hid 23.3 vs solo 53.3).

#### Amendment 72 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated; before any code or run of it): notes 49-55, the last round

Seen before writing:
- notes 37, 38, 39 (+ 6b, 5R), 40 (gated), 41 and 45 on the 9B, 27B and Lightning, and note 44 on the 9B;
- two agents' post hoc CPU passes (not registered).
  - **Note 41, seed 4001:** interpolated random-keep rescue at keepA's energy (amendment 70). Per-relation keepR ratios were 0.55-0.78 on the 9B.
  - **Geometry:** in the J++ letter dictionary (9B L14, 27B L36), a protected output token's case and space variants have cosine 0.8-0.9 with it. Their span holds a median 0.73-0.81 of its energy (films about 0.46), against 0.01 for a random span.
  - **Note 39:** arms 7 and 5R are rank-matched, not energy-matched (A holds 1.3-2.4x a same-rank random span's bridge energy). Arm 1's flips come mostly from high-overlap items.
  - **Note 40:** the held-margin strata (amendment 71). The bridge span holds about twice the answers' energy that the control bridge's does.
  - **The paper's Fig. 22 data:** at medium strength the J ablation keeps plain-text top-1 agreement at 0.75 and the random control at 0.96.

Not seen: notes 42, 43, 46, 47 and 48; note 44 on the 27B and Lightning; any condition below.

Shared:
- One deterministic run per model: 9B, 27B and Lightning. Muse is descriptive where named.
- paper10 and paper10_rot are rerun in every job and checked against the stored rows (byte-identical on the Qwens, within run-to-run noise on Lightning).
- ratio(X) = (X - X_rot) / (paper10 - paper10_rot) on MM loss, within run; rescue = 1 - ratio.
- Item bootstrap as in note 41.
- Every keep and protection logs its retained energy share E_X of paper10's removal, |edit| / |h|, and its rank.

##### Note 49: the paper's output protection, sealed (v4 seed 4001, jsuite_v4_test_chat, note 20's gate, main bands, all positions)

**Conditions** (each + _rot):
- **paper10_protF.** The protected rows are paper10's plus the letter-dictionary rows of every form of each clean top-10 token. Forms follow note 45's rule: decoded and stripped; lower, capitalised and as-is; with and without a leading space; first token. The top-10 removed atoms are then chosen from the unprotected atoms, so ten are still removed per position.
- **paper10_protC.** protF plus every row with cosine >= 0.5 to a clean top-10 token's atom, at that layer (ablate_v2's own_rows rule applied to the decoded top-10).
- **paper10_keepT10.** keep_span = QR of the unit J++ vectors of protF's added rows plus the top-10 tokens' own rows. Label-free.
- **paper10_keepRT10.** A random letter-token keep rank-matched to keepT10. Seed Random("n49:" + item); it excludes T10's and the protected rows.
- **paper10_keepOwn.** Every form of the item's own answer (note 37's keepA forms).
- **paper10_keepSib.** Every form of one sibling answer of the same relation, with a distinct first token and the form count matched. Seed Random("n49sib:" + item).

Logged for protF and protC: the number of protected rows, and the share of paper10's answer-part energy (sum ||P_A r||^2) they still remove.

**Readings** (per model, MM):
- **R1 (primary):**
  - "the protection leaks through spellings": ratio(protF) <= 1/3 and protF's gap (MM - MP) < 15;
  - "not through spellings": ratio(protF) >= 2/3;
  - otherwise "partly".
  - protC is read by the same rule as "leaks through J++ neighbours".
- **R2:**
  - "the output candidates' directions": ratio(keepT10) <= 1/3 and rescue(keepT10) - rescue(keepRT10) >= 0.33, with CI > 0;
  - "beyond the candidates": ratio(keepT10) >= 2/3;
  - otherwise "partly".
- **R3:**
  - "this item's answer": rescue(keepOwn) - rescue(keepSib) >= 0.20 with CI > 0;
  - "the category": |difference| < 0.10 and rescue(keepOwn) >= 2/3;
  - otherwise "unclear".
- **Beside:** MP losses.

##### Note 50: the orthogonal placebo, the exact complement, and a rank-matched ansR (same job as note 49)

**Conditions** (each + _rot):
- **paper10_keepR4perp, paper10_keepR8perp.** Note 41's nested random rows (Random("n41:" + item); R8 is 8x A's row count, drawn the same way). Each span is projected off span(A) per layer and re-orthonormalised. Columns of norm < 1e-3 are dropped, and the rank is logged.
- **paper10_onlyA.** r' = P_A r under paper10's protection: only the answer part of the removal.
- **ansRk.** Random letter rows equal in count to ansJ's (cands2) rows. Seed Random("n50:" + item), excluding A's rows.
- **Logged:** alpha_X = 1 - sum ||P_A (r - P_X r)||^2 / sum ||P_A r||^2, the share of the removal's answer part that keep X retains. It is logged for A, R, R2, R4 (rebuilt from their seeds) and both perps.

**Readings** (per model, MM):
- **P1 (primary).** Take the perp keep with E closest to E_A and not below it.
  - "the placebo's rescue is its overlap with the answer span": rescue <= 1/3;
  - "non-answer J content rescues": rescue >= 2/3;
  - otherwise "partly";
  - "not matched" if both perps hold E < E_A.
- **P2.** P1 in answer first-token log p (amendment 70's rescue_L).
- **P3.** "The answer part is sufficient for the damage" if onlyA's net MM loss >= 2/3 of paper10's and onlyA's gap >= 2/3 of paper10's.
- **P4.** Note 41's removal rule with ansRk in place of ansR. This replaces the 9B's flawed removal reading (ansR had about twice ansJ's rank); both are reported.
- **Descriptive:** rescue against alpha for every keep.

##### Note 51: dose x keepA (v4 seed 4001, main bands)

**Conditions:**
- top30, top30_rot, top30_pcasize, top30_keepA, top30_keepA_rot;
- the same five for top100.
- topK carries paper10's protection (verified in the smoke).

E_A is logged at each K.

**Reading** (per K and model; read only where gap_K - pcasize gap_K >= 10):
- "the answer account holds at dose K": ratio(keepA) <= 1/3;
- "beyond the answer at dose K": ratio >= 2/3;
- otherwise "partly".

##### Note 52: note 44's spans residualised (jsuite_v5kn2c, as note 44)

**Conditions:**
- **keepCapPerp:** keepCap's span projected off keepCty's span per layer and re-orthonormalised.
- **keepCtyPerp:** the reverse.
- **keepShared:** span(Cap) ∩ span(Cty), estimated as the principal vectors with cosine >= 0.9.
- paper10 and paper10_rot are rerun.
- Each logs E and rank.

**Readings** (MC0, all gated; the 27B and Lightning primary, the 9B descriptive):
- "the capital carries it": rescue(keepCapPerp) >= 2/3 and rescue(keepCtyPerp) <= 1/3;
- "the country carries it": the reverse;
- "the shared part carries it": both <= 1/3 and rescue(keepShared) >= 2/3;
- "either suffices": both >= 2/3;
- otherwise "unclear".

##### Note 53: note 39 with energy-matched controls (the paper's 90 prompts, main band, J++; 9B, 27B, Lightning; Muse descriptive)

**Conditions:**
- **arm 7E:** arm 3 with random letter-token atoms added (Random("n53:" + item)) until their bridge-energy share reaches A's;
- **arm 5R2, arm 5R4:** arm 5R with 2x and 4x A's dimension, nested;
- **arm 7 seeds 2 and 3;**
- **arms 1, 3 and 5 at every position except the final one** (1nf, 3nf, 5nf);
- arm 1 and the null are rerun and checked against note 39's rows.

**Readings:**
- **E1:** A1 re-read with arm 7E as the guard. "Answer-carried survives energy matching" if arm 7E keeps >= 2/3 and K <= 1/3. If arm 7E keeps < 2/3: "scrub not specific at matched energy".
- **E2:** "Sufficiency is answer-specific at matched energy" if arm 5 - arm 5R_k >= 1/3 of arm 1's net with the interval above 0. Here 5R_k is the smallest nested 5R whose bridge-energy share is >= A's; it is "not matched" if none is.
- **E3 (descriptive):** arm 1nf / arm 1, and arm 5nf / arm 5. The swap's share that survives when the final position is not edited.
- The A1 guard spread over the three arm-7 seeds is reported.

##### Note 54: note 40's R3 de-confounded (silent dissent, gated, names as written; solo, press_vis and press_hid; 9B and Lightning, plus the 27B if its note 40 run completes; test and dev splits)

**Conditions** (mid band):
- bridgeJ;
- bridgeJ_rot;
- bridgeJ_ctrl;
- **bridgeJperp:** the bridge forms' unit vectors orthogonalised to the span of the item's two answers' forms before removal;
- paper10 and paper10_rot.

**Reading** (no-shortcut stratum, R3 inheriting G2 as amendment 71):
- "the bridge's own directions are needed": bridgeJperp - bridgeJ_ctrl >= 10 points with the lower end > 0, and bridgeJperp - bridgeJ_rot >= 10 points;
- otherwise "not shown".
- The gated-set result is reported beside.

##### Note 55: the paper's strengths, matched for generic damage (Fig. 22 + 24 on open models)

**Bands.** The paper's percent-of-depth bands, pct(l) = 100 l / (N - 1), taken inward:

| Model | Medium (54-79) | Heavy (42-88) |
|---|---|---|
| 9B | L17-24 | L14-27 |
| 27B | L35-49 | L27-55 |
| Lightning | L28-40 | L22-44 |

**Generic damage.** Plain-text top-1 agreement with the clean model (Fig. 22's metric):
- on the 64 pinned WikiText rows x 128 tokens that removal_textloss uses;
- and on 64 v4 passages, beside;
- under each condition. J conditions protect each position's own clean top-10.

**Dose conditions** at each band:
- J: top3, paper10, top30;
- PCA: pca3, pca10, pca30 (ablate_v2's variance dictionary);
- logit lens: unembed10, unembed30;
- paper10_rot.

**Tasks** (note 45's gate and reads):
- the paper's multilingual (ML), multihop (MH) and order-of-operations (OO, descriptive) sets;
- its released rhyme set (lens-eval poetry, same pinned source and licence; T = intermediates[0], S = line 1's last alphabetic word; sha recorded on download);
- keep_T and keep_E (ML) / keep_B (MH) / keep_S (rhyme) at medium.

**v4.** paper10, paper10_rot, paper10_pcasize, unembed10, keepA and keepA_rot at medium and heavy, on note 20's gated items.

**Readings:**
- **S (primary; per set, per strength):**
  - a* = paper10's text agreement; L_PCA(a*) = task loss interpolated linearly along the PCA dose by text agreement.
  - Delta_sel = L(paper10) - L_PCA(a*), bootstrapped over the set's clusters with the interpolation inside.
  - "J-selective at matched generic damage": Delta_sel >= 15 with CI > 0;
  - "not selective": Delta_sel < 10 and the CI includes 0;
  - otherwise "partly";
  - "not matched" if the PCA dose does not bracket a* (the nearest point is reported, with no reading).
  - The same against the logit-lens dose is reported beside, and so is the paper's own contrast (paper10 - rot).
- **V (v4, per strength):**
  - "C1 holds at the paper's strength": gap >= 20 with CI > 0, rotated gap <= 1/3 of it, and gap - max(pcasize gap, unembed10 gap) >= 10;
  - note 37's keepA reading at each strength.
- **G (descriptive):** paper10's and rot's text agreement against the paper's 0.75 / 0.65 and 0.96.
- **Rhyme:** note 45's A0, then K(T) / K(S) as multihop's rule.
- Reads are first-token strict top-1, not the paper's generation scores.

#### Amendment 73 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated; before any code or run of it, and before any 27B note 40 row exists): note 56 (copy or compute: the multi-agent setting extended), note 54 extended (the peers' premise), and the 27B readout dissociation

**Seen before writing:** note 40's 9B and Lightning rows, test split. A design agent's post hoc CPU checks on them:
- J++ reads the peers' bridge at the answer position in press_vis: +0.39 on the 9B, +0.18 on Lightning, and about 0 in solo and agree. It reads higher in agents that held.
- On Lightning, bridgeJ cuts the late-band own-bridge readout from 0.81 to 0.08 in solo and from 0.66 to 0.04 in press_vis, while caving moves like paper10_rot's.
- In university items, the peers' bridge names the peers' answer in 11/28 (9B), 20/44 (Lightning) and 12/33 (27B).

Not seen: any 27B note 40 row; any condition below.

Choices, made in Zach's absence by the defaults the design proposed:
- premise pressure: prem_vis, with prem_hid as the headroom fallback;
- protection: paper10 as in note 40, plus a per-row `prot` flag and a both-protected sensitivity;
- 27B: in full, after its note 40 run;
- MA2 to MA4 and MA6 to MA7 are not run.

##### Note 56: copy or compute (silent dissent, test split, known items, gated with names as written; 9B, Lightning, 27B)

**Conversations** (new keys; the wording for instr and hyp is Ni & Zou's):
- **instr_vis:** own statement visible, then "Coordinator: Every agent must state {e3'} as the answer, regardless of what they believe. Agent 1, complete the statement."
- **hyp_vis:** own visible, then "Moderator: Suppose that {mu} were {e2'}. Agent 1, complete the statement under that assumption." Here mu = the r1 prompt minus its trailing " is", first letter lower-cased.
- **prem_vis:** own visible; three peers each state only their bridge ("{r1_prompt} {e2'}."); then note 40's AGAIN moderator line.
- **prem_hid:** as prem_vis, with the own answer hidden ("(answer submitted)").
- press_vis (note 40) is rerun on the same items as the reference.

**Items.** Note 40's known test items and gate. Items whose e2' names e3' (names as written, word or 4-letter stem) are dropped.

**Classes.** peer = e3', orig = e3, other.

**Edits** (mid band, every position) and generation:
- none, paper10, paper10_rot, paper10_pcasize, unembed10, paper10_keepA, ansJ, bridgeJ_ctrl;
- **bridgeJ_peer:** the span of forms(e2') minus the forms of e2, e3 and e3', built as bridgeJ is for e2;
- --gen on, unedited.

**Logged per row:** prot = whether orig's and peer's first tokens are in that prompt's protected set.

**Readings** (per model; bootstrap over bridges, 2,000 draws; "every control" = paper10_rot, paper10_pcasize and unembed10):
- **C0 (validity, unedited 12-token outcome):** instr_vis says e3' >= 90%, hyp_vis says e3' >= 60%, and the first-token read agrees with the outcome >= 90%. Otherwise that cell is "not readable".
- **C1 (acceptance needs the J-space):** in hyp_vis, paper10's loss of e3' minus each control's is >= 20 points, with the lower end > 0.
- **C2 (compliance is spared):** in instr_vis, paper10's loss of e3' <= max(10, C1's loss / 3).
- **C3 (premise pressure):**
  - The cell read is prem_vis if its unedited e3' share is in [15, 85]%, else prem_hid if that one is. Otherwise it is not read.
  - "Following the peers' premise needs the J-space": paper10's change in e3' share, minus each control's, has its upper end < 0.
  - Beside it: the same items' press_vis change, which is answer pressure.
- **C4 (secondary):**
  - in hyp_vis, keepA's net loss as a share of paper10's; <= 1/3 = "acceptance needs the answer's directions";
  - bridgeJ_peer - bridgeJ_ctrl loss with lower end > 0 = "the stated premise's own directions are used".
- **D1 (descriptive):** the J++ readout of the agent's own bridge (orig - ctrl, hit@100, late band) in instr_vis against solo:
  - <= 1/3 of solo: "the readout tracks the agent's own computation";
  - >= 2/3: "it tracks the words in context".
- **D2 (descriptive):** where lost e3' goes in hyp_vis (orig or other).
- **Sensitivity:** C1 and C3 on items with both answers protected. A change of sign is reported as "confounded by protection".
- **Caveat stated now:** e3' is in context in instr_vis and is usually the clean top token, so C2 is partly built in by the protection.

##### Note 54, extended: the peers' premise, and every span's rotation (the same job as note 54)
- **Added conversation:** hop1_vis (existing key; the peers state their bridge and answer).
- **Added edits:** bridgeJ_ctrl_rot, bridgeJ_peer, bridgeJ_peer_rot.
- **Items:** --split all (test and dev). On the 27B, the no-shortcut and landmark items only.
- **Readings** (points, paired, bridge bootstrap):
  - **P1 (the peers' implied premise, press_vis):** [bridgeJ_peer - bridgeJ_ctrl] change in giving in.
    - "Used to conform": <= -5 with the upper end < 0, and bridgeJ_peer < bridgeJ_peer_rot.
    - "Readable, not used": |change| < 5 with the interval including 0.
    - Positive control first: own-bridge removal in solo loses >= 10 points against bridgeJ_rot. Without it, P1 is not read.
    - Landmark items are reported beside.
  - **P2:** the same in hop1_vis.
  - **R3':** on no-shortcut items, test and dev pooled (>= 30 per model): bridgeJ against both bridgeJ_rot and bridgeJ_ctrl, in solo loss and in press_vis gain. "The bridge's own directions are needed" if both lower ends are > 0 against both controls. It is read alongside note 54's bridgeJperp reading, which stays its primary.

##### The 27B readout dissociation (registered now, before the 27B note 40 rows exist)
- **Reading:** "the silent-dissent readout is not what holds" if both hold:
  - bridgeJ removes >= 2/3 of the late-band own-bridge readout (orig bridge - control bridge, J++ hit@100) among agents that gave in;
  - press_vis giving in under bridgeJ is within 5 points of paper10_rot's.
- It is re-read against bridgeJ_rot once note 54 runs on the 27B.
- The 9B and Lightning were seen, so for them it is descriptive.

##### Amendment 73, addendum (box clock at commit; before any note 56 run beyond the builder's 8-item 9B smokes, which are mechanics only)
Implementation choices made by the builder where the text was literal or open. They are recorded here before the full runs.
- **mu.** The first letter is lower-cased only when the r1 prompt starts with "The". This matches TwoHopFact's own mu (r2(r1(e1)).subject) on 6,060 of 6,061 facts. The literal rule would lower-case 1,810 person names ("ketanji Brown Jackson's ...").
- **C2's bound.** paper10's raw instr_vis loss is compared with max(10, paper10's raw hyp_vis loss / 3), following note 40's G2 convention. The version against C1's specific loss is printed beside it.
- **C4's keepA "net".** It is net of paper10_rot, since no keepA_rot is in the edit list.
- **C3's cell.** It is chosen by the unedited first-token e3' share. C0's 90% agreement gate applies to instr_vis and hyp_vis; the prem and press agreement is printed.
- **D1's solo rows** come from note 40's run of the same model (same items, prompts and read layers).
- **The peer-name filter** is applied in the reader (names as written, on e2' alone). The GPU runs the full test set.
- **press_vis** is rerun in-run as the reference. Its rows are not byte-identical to note 40's (batch composition), so no row-level diff against note 40 is read.

#### Amendment 74 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated; before any note 55 full run): note 55's S reading when the PCA dose cannot bracket
**Seen.** The builder's 9B smoke, on 8 WikiText texts. This is mechanics only, not a result.
- At medium, plain-text top-1 agreement was:
  - paper10 0.683;
  - pca3 / pca10 / pca30 0.178 / 0.076 / 0.023;
  - unembed10 / unembed30 0.791 / 0.772;
  - paper10_pcasize 0.619.
- At heavy, paper10 was 0.527, and pca3 0.056.
- So the registered PCA dose almost surely cannot bracket paper10's generic damage: the top principal directions carry the residual stream's outlier directions. S would read "not matched" everywhere.

No task loss under any edit was seen.

**Changes, fixed before the full runs:**
- **Doses.** unembed100 and unembed300 (the logit lens's top-K directions, with paper10's protection, as unembed10/30) are added to note 55's text and task doses at both bands.
- **S order** (per set and strength; all thresholds, the bootstrap and the "not matched" rule unchanged):
  1. along the PCA dose, as registered;
  2. if that does not bracket a*, along the logit-lens dose (unembed10 / 30 / 100 / 300);
  3. if neither brackets, a descriptive S2 along the line through paper10_rot and paper10_pcasize: two non-J removals of paper10's size, interpolated by text agreement. It is labelled "size-matched pair, descriptive", and no registered label is printed.
- The dose each reading used is printed on its line. Every dose's raw points are reported.

#### Amendment 75 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated; post hoc follow-up, registered before its runs): note 54's P1 de-confounded (the peers' premise orthogonalised to the answers)
**Seen.** Note 54 on the 9B (test and dev pooled):
- The primary bridgeJperp reading is "not shown" in solo, press_vis and press_hid (bridgeJperp - bridgeJ_rot = 0.0 in press_vis), while R3' (the unorthogonalised bridgeJ) reads "needed". So the agent's own bridge span is needed only through its answer component.
- P1 and P2 read "used to conform": bridgeJ_peer - bridgeJ_ctrl was -12.3 [-16.3, -8.5] in press_vis and -6.4 in hop1_vis, and -23.4 against bridgeJ_peer_rot.
- bridgeJ_peer is not orthogonalised to the answers. The peers' bridge forms (e.g. a city) can share J++ energy with the peers' answer (its country), the same confound that bridgeJperp removed from R3.

**New conditions** (mid band; the same items, conversations and split as note 54):
- bridgeJ_peerperp: the peers' bridge forms' unit vectors orthogonalised to the span of both answers' forms (e3 and e3'), as bridgeJperp does for e2;
- bridgeJ_peerperp_rot;
- with none, bridgeJ_ctrl and bridgeJ_peer rerun in the same run.

**Reading P1-perp** (press_vis primary, hop1_vis beside; gated, test and dev pooled; the solo positive control as P1):
- "the peers' premise itself is used to conform": bridgeJ_peerperp - bridgeJ_ctrl <= -5 with upper end < 0, and bridgeJ_peerperp < bridgeJ_peerperp_rot;
- "via its answer component": P1 is met, while |bridgeJ_peerperp - bridgeJ_ctrl| < 5 with the interval including 0;
- otherwise "partly".

**Models.** 9B (a new run with the conditions above), plus Lightning and the 27B: their note 54 runs, not yet started, get these conditions added. The 9B is a post hoc follow-up; on Lightning and the 27B the reading is confirmatory.

#### Amendment 76 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated; before note 56's Lightning and 27B runs): note 56's C4 premise reading de-confounded

**Seen.** Note 56 on the 9B (n 291):
- C1 met (hyp_vis spec loss 55.0 vs rotation);
- C2 met (instr_vis loss 7.6);
- C3 met in prem_hid (-15.5 vs rotation), while answer pressure on the same items gave +15.5;
- C4 bridgeJ_peer "the stated premise's own directions are used" (55.0 vs bridgeJ_ctrl).

bridgeJ_peer's span shares about 0.30 of its energy with the answers' span (note 54 smoke), so C4's premise reading is confounded in the same way as note 54's P1.

**Change.** Note 56's Lightning and 27B runs, which have not started, add bridgeJ_peerperp and bridgeJ_peerperp_rot (amendment 75's edits). The 9B gets a small follow-up run with none, bridgeJ_ctrl, bridgeJ_peer, bridgeJ_peerperp and bridgeJ_peerperp_rot on hyp_vis and prem_hid. That run is post hoc.

**Reading C4-perp** (hyp_vis primary, prem_hid beside):
- "the stated premise's own directions are used": the loss of e3' under bridgeJ_peerperp minus under bridgeJ_ctrl is >= 10 points with the lower end > 0, and exceeds bridgeJ_peerperp_rot's;
- "via its answer component": C4 is met while bridgeJ_peerperp - bridgeJ_ctrl < 5 with the interval including 0;
- otherwise "partly".

C1-C3 are unchanged.

#### Amendment 77 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated; before any code or run of it): 9B replications of notes 49/50 (draws p4002, p4003) and note 56 (dev split)
**Seen.**
- Notes 49 and 50 on the 9B, draw 4001:
  - R1 "not through spellings";
  - R2 "the output candidates' directions";
  - R3 "this item's answer";
  - P1 "the placebo's rescue is its overlap with the answer span";
  - P3 "the answer part is sufficient";
  - P4 "answer-specific removal".
- Note 56 on the 9B test split: C1, C2 and C3 met.

Not seen: any condition below on these draws or split.

**Why.** CLAUDE.md asks for at least 3 seeds and held-out data before a result is called positive. The bigger models' lanes are full until about 15:00 UTC, so the replications run on the 9B only, and they are reported as 9B-only.

**Runs:**
- **Notes 49 + 50** on jsuite_v4p4002 and jsuite_v4p4003 (9B). The same conditions, bands, gate and readers as amendment 72. Each draw's own competence and control runs (notes 43 / 48) are used.
- **Note 56** on the 9B's dev split, with the same conversations, edits, filter and readings as amendment 73 (C0-C4, D1, D2). D1's solo rows come from note 47's dev run.

**Readings.** "Replicates" means the same registered label per reading as on draw 4001 (notes 49/50) or on the test split (note 56). A changed label is reported as "does not replicate". No pooling across draws.

#### Amendment 78 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated; before any code or run of it, and before any 27B note 40 reading): skeptic pass 3 follow-ups (note 57) and a sharper dissociation reading

**Seen.** A skeptic pass (post hoc, CPU) on the 9B's notes 47, 49-51 and 54:
- **keepSib** makes the model say the sibling on 158/267 items. Keeping any candidate's span steers the model toward it.
- **keepT10's** top-10 contains the gold answer on 267/267 items. Its random twin is rank-matched, not energy-matched.
- **protF / protC** change the removal by only 0.2% / 1% of its energy.
- **onlyA** has no random "remove only this part" control.
- **Note 51** has no random keep at K30 / K100.
- **The note 54 dissociation:** among agents that held, bridgeJ makes 13% cave (+5.5 [0.7, 10.8] beyond bridgeJ_rot). This sits where the same edit breaks the solo answer.

##### Note 57: the controls the 9B's mechanism claims lacked (9B, v4 draw 4001, note 49's run settings; one ablate_v2 run)
**Conditions** (each + _rot):
- **paper10_onlyRperp:** r' = P_X r, where X is a random letter-token span orthogonalised to span(A) (note 50's construction) with rows added until its retained share of paper10's removal energy reaches E_A. It removes only a random, non-answer part of r at the answer part's energy.
- **topK_keepRE** for K = 30 and 100: a random keep (note 41's nested draws, rows added) energy-matched to topK_keepA's E_A at that K.
- **ansRe:** a random letter-token removal energy-matched to ansJ (rows added until its removed energy reaches ansJ's). Every removal logs edit_rel.
- **paper10_keepRivals:** every form of every candidate in the item's clean top-10 except the gold answer.
- **paper10_keepRandRivals:** forms of as many random same-relation answers (not the gold answer, not in the clean top-10), with the form count matched.

**Readings** (9B; MM; note 41's bootstrap):
- **S1 (sufficiency is answer-specific):** onlyA's net MM loss minus onlyRperp's >= 1/3 of paper10's net, with the lower end > 0. Otherwise "sufficiency not shown specific".
- **D1 (dose):** at each K, rescue(topK_keepA) - rescue(topK_keepRE) >= 0.33 with the lower end > 0: "answer-specific at dose K".
- **A1 (removal at matched energy):** ansRe's gap <= 1/3 of ansJ's: "answer-specific removal at matched energy".
- **T1 (descriptive):**
  - under keepRivals, the share of MM items whose output is a kept rival, against keepRandRivals' share of a kept random answer;
  - the gold answer's survival under each.
  - This describes the steering effect of keeping a candidate's span.

##### The 27B readout dissociation, sharpened (added before any 27B note 40 reading; amendment 73's reading is unchanged and stays registered)
- **D-held:** among press_vis agents that held unedited, the cave rate under bridgeJ minus under bridgeJ_rot (once note 54 runs on the 27B), and minus under bridgeJ_ctrl. It is split by whether the same item's solo answer survives bridgeJ.
- **Labels:**
  - "the readout's removal moves holders only where it breaks the recall": the cave excess is >= 5 points with the lower end > 0 in the solo-breaks stratum, and < 5 points with the interval including 0 in the solo-survives stratum;
  - "the readout's removal moves holders": the excess is met in both strata;
  - "not shown": otherwise.
- On the 9B and Lightning this reading is post hoc.

#### Amendment 79 (Zach's session, 2026-10-30, box clock at commit; Zach away and delegated; before any note 57 run on these models): note 57 on Lightning and the 27B
**Seen.**
- Note 57 on the 9B: S1, D1 and A1 met.
- Notes 49 and 50 on Lightning:
  - P1 / P2 "not matched": R8perp holds E 0.37, below E_A 0.49;
  - P3 "sufficient";
  - P4 "answer-specific removal".

Not seen: note 49 / 50 on the 27B (running at commit time), and any note 57 condition on Lightning or the 27B.

**Run.** Note 57's conditions, readings and reader, unchanged, on Lightning (main band L27-33) and the 27B (L32-40), with v4 draw 4001 and note 49's settings.
- onlyRperp's rows are added until E_A is reached. That gives Lightning's placebo question the energy match that note 50's fixed R4 / R8 perps lacked.
- Confirmatory on both models.
- Lightning is read beside its own rotations, since it is not bit-reproducible.
