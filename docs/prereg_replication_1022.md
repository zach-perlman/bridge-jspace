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
