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
