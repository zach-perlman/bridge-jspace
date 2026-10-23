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
