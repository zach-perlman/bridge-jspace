# A1 size, dose, L16 split, A5 shared code: opened 23 Oct, all UNVERIFIED

Conventions. Every file below is under `results/early_push_where/<run>/`. A lookup counts when the prompt → prompt answer switches to the other bridge's answer. A recall counts when the prompt → memory answer switches. Brackets are 95% CIs. "4x"/"8x" are the lens push's sizes, and "size-matched" means cut to that size. "Word" is the stated bridge's word, which decides the verdict; "sentence" is reported only, except on the 122B, where the spec makes it decisive too. The "Verdict: H-around …" line at the top of each summary.md comes from the older where-rule, not from these specs, so I left it out. Verdicts are the ones the runs' own code wrote to summary.json. "Dan right/wrong" is my scoring; the batches are not scored in the predictions file yet.

## d4_layer_gap_perp_27b (Qwen3.6-27B, n=100 scenes × 4 families, layers 12-34)
- **Tests:** at the word, does the patch keep moving lookups after the lens push stops (layer 20) once its lens-readable part is removed and it is cut to the lens push's size?
- **Rule:** H-direction if it stops at least 6 layers after the lens push and still moves lookups at layer 20. H-dose if it stops within 2 layers of the lens push, or before it.
- **Verdict:** **H-dose**. It stops at 12, before the lens push (20); the full patch stops at 28 (`summary.json` perp_test.w).
- **Headline:** without its lens-readable part, the patch moves 0% [0, 4] of lookups at every layer, at 4x and 8x, and every cell is valid. Its recalls at the word also stay low, at most 26% (`summary.md`).
- **Controls:** lens push 8x: 19% [13, 28] at L16, 0% [0, 4] at L20. Random push 0% [0, 4] everywhere. Full patch 65% [55, 74] at L20 and 24% [17, 33] at L26 (`summary.md`). The removed part is 25% of the patch's squared norm at L20 (`summary.json` scene_patch.perp_removed).
- **Sentence (reported):** H-direction, with 52% [42, 62] of lookups but 95% [89, 98] of recalls at L20 8x, so it is not lookup-specific (perp_test.s). The sentence version puts its whole norm on the word and the full stop (dose spec, note 1), so per token it is larger than the word version.
- **Dan:** Q20.1 "layer 28" is **wrong** (it never moves lookups). Q20.5 "no", i.e. it will not move recalls as much as lookups, is **wrong** where it can be measured: at the sentence, recalls are above lookups.
- **Odd:** the lens push's 8x cells at L20-28 fail the off-path check (memory → prompt changed 14% at L20). Its stop at 20 therefore rests on the 4x cells.

## d4_layer_gap_dose_27b (Qwen3.6-27B, n=100, the same scenes)
- **Tests:** is the 27B's layer gap only size? The patch's direction (lens-readable part kept) is cut to the lens push's size.
- **Rule:** the same bars, 6 and 2 layers.
- **Verdict:** **H-direction**: it stops at 28, 8 layers after the lens push at 20 (`summary.json` dose_test.w). The sentence is also H-direction (stop 32). The layer gap replicates: H-gap at both word and sentence (layer_gap).
- **Headline (word, 8x):** 34% [25, 44] at L16, 44% [35, 54] at L18, 20% [13, 29] at L20, 13% [8, 21] at L24, 9% [5, 16] at L26, 0% at L28. **At 4x it is 0% at every layer**, so the verdict rests on 8x alone (`summary.md`).
- **Controls:** lens push at L20 0% [0, 4] at both sizes. Random 0% [0, 4]. The L20 8x cell is valid (memory → prompt and memory → memory changed 5% each; `summary.json` cells). Recalls in that cell are 78% [69, 85], against 20% of lookups, so it is not lookup-specific. I computed that from the cells; the rule does not use it.
- **Replication:** item for item, it gives the same answers as d4_layer_gap_v2_27b: lens push 19197/19200, full patch 9598/9600 (`summary.md`).
- **Dan:** Q16.1 "layer 28; 85-90%": the stop layer is **right**, the share is **wrong** (20%). Q16.2 "3-10x" is **wrong**: the full patch at the word, L20, is 12.28x the 1x lens push (`summary.json` scene_patch), about 1.5x the 8x push, so "1-3x".

## d4_l16_split_27b_r2 (Qwen3.6-27B, n=100, layers 14/16/18)
- **Tests:** at L16, at the word, which part of the full patch moves lookups: its lens-readable part or the rest? Each part is pasted at its own size. A random subspace with the same share is the control.
- **Rule:** H-lens-part if the lens-readable part alone moves lookups (lower bound > 5%) in a valid cell. H-rest if that part is inert and the rest moves. The full patch has to move lookups for either verdict to count.
- **Verdict:** **H-lens-part**, at both word and sentence (`summary.json` split_test).
- **Headline (word, L16):** the lens-readable part moves 42% [33, 52] of lookups and 84% of recalls. The rest moves 0% [0, 4] of lookups and 16% of recalls. The random subspace with the same share (27%) moves 0% [0, 4] of both. The full patch moves 85% [77, 91], so the positive control passes. Every part's null is 0% [0, 4] and every cell is valid (`summary.md`).
- **Same at L14 and L18:** 39% vs 0% at L14, 20% vs 0% at L18.
- **Finer split (reported):** the projection on the two animals' own lens directions (15% of the norm) moves 0% [0, 4]; everything else moves 17% [11, 26]. So what moves lookups is lens-readable, but it does not lie along the bridge's own lens direction.
- **Dan:** Q16.3 "0-10% J-part, 80-90% rest" is **wrong**, reversed. Q16.4 "15-20%" is **wrong**: the share is 27%. Only the two animals' own lens directions come to 15%.
- **Odd:** the "Verdict: inconclusive" at the top of `summary.md` is the old where-rule, not this spec's rule.

## d4_shared_code_27b (A5; Qwen3.6-27B, 100 held-out scenes, 300 training scenes)
- **Tests:** build one direction per animal pair on other scenes: the mean residual at the other animal's word minus the mean at this one's. Remove its lens-readable part and push it at the word at the lens push's size. Does it move lookups?
- **Rule:** H-shared if, at 8x and in some valid cell, the lower bound is at least 20% while the lens push's upper bound is at most 5%. H-none if it is at most 5% (upper bound) everywhere and the dose run's size-matched patch moves lookups there.
- **Verdict:** **H-none**: the code is specific to each scene, not reusable (`summary.json` shared_test).
- **Headline (8x):** without its lens-readable part: 0% [0, 4] at L20, L24 and L28, all cells valid. With that part kept: 20% [13, 29], 11% [6, 19], 0%. Lens push 0% [0, 4] at all three; random 0%. The size-matched patch (dose run) gives 20% [13, 29] at L20 and 13% [8, 21] at L24.
- **Recalls (8x):** without the part 13%, 5%, 5%; with it 80%, 79%, 100% (`summary.md`).
- **Cosine with the lens push:** 0.31, 0.28, 0.42. Lens-readable share of the norm: 27%, 24%, 36% (`summary.md`). There were at least 40 training scenes per animal (`shared_code.json`).
- **Dan:** Q21.1 "30-40%" is **wrong** (0%). Q21.2 "about the same; recalls 70-100%" is **partly** right: the lookups are not the same (20% vs 0%), but the recalls are in range. Q21.3 "cosine 0.2-0.5" is **right**.
- **Odd:** all of the lens push's 8x cells are invalid (memory → prompt changed 14-21%, memory → memory 36% at L28), but the rule reads its rate anyway. The kept-part cell at L28 8x is also invalid (memory → memory 11%).

## qwen35_9b_d4_layer_gap_size (Qwen3.5-9B, n=100, every layer 6-22)
- **Tests:** three questions at the word: does the full patch outlast the lens push? Does the size-matched patch? Does the size-matched patch without its lens-readable part?
- **Rule:** bars of 3 and 1 layers; three verdicts at the word.
- **Verdicts (word, `summary.json`):**
  - Full patch: **H-gap** (lens push stops at 6, full patch at 11).
  - Size-matched: **H-dose** (stops at 6).
  - Without the lens-readable part: **H-dose** (stops at 6).
  - Sentence: H-gap, H-direction, inconclusive.
- **Headline (word, `summary.md`):** the full patch moves 78% [69, 85] at L6, 18% at L7, 13% [8, 21] at L9 and 1% at L10. Size-matched is at most 1% at every layer and both sizes; without its lens-readable part it is 0% everywhere. The lens push moves 0% [0, 4] at every layer 6-22; random 0%.
- **Size:** at L6 the full patch at the word is 18.74x the 1x lens push, about 2.3x the 8x push. The removed part is 40% of the norm (`summary.json` scene_patch).
- **Dan:** Q20.2 "lens till 6; full patch from 6; gap 3-6" is **partly** right. The lens push stop (6) and the full-patch gap (5) are right, but the size-matched patch has no gap.
- **Odd:**
  - The lens push never moves lookups here, so its "stop" is just the first grid layer.
  - The sentence's H-direction rests on one valid cell (L6 4x, 13% [8, 21]). Every size-matched sentence cell from L7 to L16 fails the off-path check (memory → memory up to 56%), so stop = 17 is set by missing valid cells.

## olmo3_7b_instruct_jpp_d4_layer_gap_size_raw (OLMo-3-7B, our J++, raw prompts, n=100, layers 6-22)
- **Tests and rule:** the same as the 9B, word for word. The gate and the 5-scene smoke passed, since the chain only reaches this run if they do and the smoke folder exists.
- **Verdicts (word, `summary.json`):**
  - Full patch: **H-gap** (lens push stops at 6, full patch at 15).
  - Size-matched: **inconclusive** (stops at 10, gap 4, but it does not move lookups at 6).
  - Without the lens-readable part: **inconclusive** (stops at 16).
  - Sentence: inconclusive, H-direction, H-direction.
- **Headline (word, `summary.md`):** the full patch moves 44% [35, 54] at L6, 29% at L8, 11% [6, 19] at L10 and 3-4% at L11-12. Size-matched is at most 5% [2, 11] (L10 8x, an invalid cell). Without its lens-readable part it is at most 2%. The lens push moves 0% at every layer; random 0%.
- **Sentence, without the part:** 11% [6, 19] of lookups and 57% [47, 66] of recalls at L11 8x, so it is not lookup-specific (perp_test.s).
- **Removed part:** only 12-21% of the norm here (the 27B: 22-34%).
- **Dan:** Q20.3 "yes; yes" is **partly** right. The full-patch gap holds (9 layers), but the size-matched patches barely move lookups at the word.
- **Odd:** both inconclusive word verdicts come from cells with 1-2 lookups out of 100 (upper bound above 5%), plus the lens push's stop sitting on the first grid layer. Read plainly, nothing size-matched moves lookups at the word.

## qwen35_122b_d4_layer_gap_size (Qwen3.5-122B-A10B FP8, 2x H100, n=94, every layer 24-39)
- **Tests and rule:** as on the 9B, with bars of 5 and 2 layers; word and sentence are both decisive.
- **Verdicts (`summary.json`):**
  - Word: full patch **inconclusive** (lens push stops at 29, full patch at 33, gap 4). Size-matched **H-direction** (stops at 34). Without the lens-readable part **H-dose** (stops at 24).
  - Sentence: **H-no-gap, H-dose, H-dose** (every arm stops at 35).
- **Headline (word, 8x, `summary.md`):**
  - Size-matched: 46% [36, 56] at L27, 34% [25, 44] at L29, 21% [14, 31] at L30, 1% [0, 6] at L31-33, 0% from L34.
  - Without its lens-readable part: 0% [0, 4] at every layer.
  - Full patch: 38% at L29, 21% at L30, at most 1% from L31.
  - Lens push: 5% [2, 12] at L27, 0% from L29. Random: 0%.
- **At L29:** the size-matched patch moves 34% of lookups and 88% [80, 93] of recalls, so it is not lookup-specific.
- **Dan:** Q20.4 "yes" (they still move lookups at L33-38) is **wrong**: at most 1% at the word and 2% at the sentence. Even the full patch is at most 1% there.
- **Odd:**
  - The H-direction verdict hangs on 1 lookup out of 94 at each of L31, L32 and L33 (upper bound 6%). Count those as stopped and the arm stops at 31, a gap of 2, which is H-dose.
  - The "band at L33-38 where only the patch moves lookups" that the spec assumes does not appear in this run.
  - Unedited answers are all right, but the unedited logits are up to 2.70 off the clean run (`timing.json`; split over two H100s). The lens push matches the H200 run item for item on 5953/6016 (`summary.json` replication).

## Overall takeaway
1. On the 27B, every size-matched test agrees: what moves lookups at the word sits **inside** the lens-readable part. With it, the patch moves 20% at L20; without it, 0% at every layer. At L16 the lens-readable part moves 42% and the rest 0%. The shared code moves lookups only with that part kept. But it does not lie along the bridge's own lens direction: the lens push and that projection both move 0% from L20.
2. The 27B's layer gap is not pure size (dose run: H-direction, though only at 8x). On the 9B and OLMo nothing at the lens push's size moves lookups at the word at any layer, so there the gap is size. On the 122B, H-direction at the word hangs on single items out of 94, and nothing moves lookups from L31 on.
3. Most of Dan's predictions were wrong: he expected the part the lens cannot read to carry the effect, and the data say the reverse. He was right on the 27B dose stop (L28), the 9B lens-push and full-patch stops, the shared code's cosine and its recall share. Nothing here is verified.
