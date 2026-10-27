# Opened 23 Oct: B4 absent-entity donor, lens push on Gemma and Qwen3-32B, Gemma J-space removal (all UNVERIFIED)

## 1. B4: the donor asks about an entity the original never mentions (Qwen3.6-27B, layer 50). Verdict: ORDER

- **What it tests.** The donor's list puts a new entity x at its asked place k_d, and the donor asks about x. x appears nowhere in the original. The donor's last 2 tokens are copied into the original at layer 50. If the original then answers with its own sentence at place k_d, the patch carries an order label. If it answers with its 1st sentence, the patch is a fallback.
- **Rule.** Memory → prompt decides. D = share of order answers minus share of fallback answers, over k_d 2-5, leaving out originals that ask about their own 1st sentence. The 95% CI is an entity-cluster bootstrap (4,000 draws, seed 0). The verdict is "order" iff D's lower bound is above 0 and above the random push's upper bound.
- **Verdict** (scripts/absent_entity.py): **order**. D = **+48 [+43, +52] pts**, n = 453 decisive items (757 memory → prompt items kept). The random push gives D = −0.2 [−0.7, 0.0] and leaves 99.8% of answers unchanged. The same-entity control changes 0.5% [0.2, 1.4] of answers.

  | k_d | n | D [95% CI] | order | fallback (1st) | unchanged | other digit | donor's digit |
  |---|---|---|---|---|---|---|---|
  | 2 | 114 | +95 [+91, +98] | 95% | 0% | 4% | 2% | 0% |
  | 3 | 113 | +45 [+34, +55] | 47% | 2% | 28% | 23% | 0% |
  | 4 | 116 | +21 [+14, +28] | 21% | 0% | 39% | 41% | 0% |
  | 5 | 110 | +30 [+21, +40] | 31% | 1% | 44% | 25% | 0% |

  Pooled over the 453: order 48% [44, 53], fallback 0.7% [0.2, 1.9], unchanged 28% [24, 33], other digit 22% [19, 27], donor's digit 0% (Wilson CIs).
- **Ordinary finding-5 donor on the same items** (reported, not decisive): D = +40 [+35, +45], or +38 [+32, +44] without the 145 items where the donor's entity is the original's 1st sentence. Per k_d: +93 / +27 / +12 / +29. The absent donor scores at least as high at every k_d, and clearly higher at k_d 3 (+45 vs +27) and k_d 4 (+21 vs +12). Named → prompt (reported) is also "order": D = +25 [+21, +28], but most of its answers stay unchanged at k_d 3-5 (74-80%).
- **Excluded originals that ask about their own 1st sentence** (n = 151). The patch gives order 43% [35, 51], the 1st sentence (which is also their own answer) 19% [13, 25], and another digit 38% [31, 46]. At k_d 2, 97% are order. The random push leaves 100% unchanged.
- **Smoke donor-read check.** 30 of 30 new donors were answered right unedited: 100% [89, 100] against the 80% bar, and the gate printed RUN. In the full run 1,521 of 1,528 were right. All 7 misses were memory → prompt (6 of them body) and were dropped.
- **Dan's predictions.**
  - Q23.1 "more of the 1st sentence": **WRONG**. The same place got 48%; the 1st sentence got 0.7%.
  - Q23.2, k_d 3-5 (n = 339): own answer 37% [32, 42] (Dan said 50%), same place 33% [28, 38] (Dan 20%), 1st or 2nd sentence 2.1% [1.0, 4.2] (Dan 30%; my count). The same place is far less common than at k_d 2 (95%). Score: **PARTLY**. Right that the own answer comes first (though it is not clearly above the same place) and that the same place drops after k_d 2. Wrong on the 30% going to the first sentences.
- **Odd things.**
  - "Other digit" is not noise. 77 of its 100 cases at k_d 3-5 are the original's digit one place away from k_d (my count). So the place label is blurry past place 2.
  - k_d 4 is lower than k_d 5 for both donors and both families.
  - pointer_swap's own summary: copying layers 44-52 at once (instead of layer 50 alone) gives the donor's own digit, which is absent from the original, on 44% [40, 47] of memory → prompt items. This sits outside B4's rule.
- **Files.**
  - Verdict: results/absent_entity/d3_absent_entity_27b_r2_20261023-150258/verdict.md and verdict.json (families.RL: by_k, ordinary, original_asks_1st).
  - Run: results/pointer_swap/d3_absent_entity_27b_r2/ (checks.jsonl, outcomes.jsonl, summary.md).
  - Smoke: results/pointer_swap/d3_absent_entity_27b_smoke/checks.jsonl and log/jobq/d3_absent_entity_27b_smoke/log.txt.
  - The Q23.2 and "other digit" breakdowns: /private/tmp/claude-502/-Users-danorel-Workspace-Research-mats-bridge-jspace/fa0f527d-6031-4147-8bc3-75ed29692476/scratchpad/b4_other_digit.py

## 2. Lens push at the stated bridge, Qwen3-32B with J++ (qwen3_32b_jpp_d4_where). Verdict: H-AROUND

- **What it tests.** We push the lens direction (bridge X minus bridge I) at the sentence (s) or the word (w) where a bridge is stated. Does the recall from a stated bridge (prompt → memory, BR) switch to X while the lookup (prompt → prompt, BL) does not?
- **Rule v2.** A cell is kept iff:
  - BR switches to X in ≥ 30% of items, with a lower bound ≥ 20%;
  - the random push switches ≤ 5% of BR and ≤ 5% of BL;
  - the lens push changes ≤ 10% of the off-path answers (RL and RR).

  The primary cell is the kept cell with the highest BR. H-around iff BL ≤ 10% and the scene-paired BR − BL has a lower bound ≥ 20 pts. v2.1 is the same, using layers ≥ 20 only.
- **Verdict** (the run's own, under v2 and v2.1, same cell): **H-around**. Primary cell is the word, layer 24, 8x: BR 59% [49, 68], BL 5% [2, 11], BR − BL = +54 [+45, +64] pts over 100 scenes. The random push switches BL 0% [0, 4]; off-path RL and RR change 3% [1, 8] each.
- **Valid cells by layer** (all at 8x; BR / BL):
  - Word: layer 24 59 / 5; layer 28 47 [38, 57] / 4 [2, 10]; layer 32 37 [28, 47] / 0 [0, 4].
  - Sentence: layer 24 47 [38, 57] / 3 [1, 8]; layer 28 37 [28, 47] / 5 [2, 11].
  - No valid cell at layers 16-20 (BR ≤ 26%) or at 36-44 (the push changes 12-25% of off-path RR).
- **Control and anchor.** The random push switches 0-1% of BR and BL at every valid cell. Slide-6 anchor (question phrase, layer 20, 8x): recalls RL 47% and RR 51% (the 27B's slide had 73 / 84); stated BL and BR 0%.
- **Dan's prediction.** No direct one: his Q15.7 answer ("depends on J++ quality") was about J-space removal. It is consistent, though: this J++ beats the logit lens by the most (+0.43, Q15.7). The agents' prior was H-around 0.45 per model with a valid cell.
- **Odd.** BL is 3-5% (lower bound 1-2%) at the valid cells at layers 24-28, rather than the flat 0% seen on the 27B and 9B. It stays under the 10% bar.
- **Files.** results/early_push_where/qwen3_32b_jpp_d4_where/summary.json (decision, cells) and summary.md; analysis-v2.1-20261023T101946Z/; where.png.

## 3. Lens push at the stated bridge, Gemma 4 31B-it with Zach's J++ (gemma4itf_d4_where). Verdict: NO VALID CELL

- **What it tests and rule.** Same as section 2. n = 87 scenes per family: 13 of the 100 drawn were dropped as token-unaligned.
- **Verdict** (v2 and v2.1): **"no valid cell: the lens does not write a stated bridge at its sentence"**. BL cannot be interpreted.
- **Numbers.** The best BR at the sentence or word is 14% [8, 23] (sentence, layer 26, 8x), and the random push gets 11% [6, 20] at that same cell. Every other cell is ≤ 6%. BL is ≤ 8% everywhere, and equals the random push at layer 26.
- **At the question phrase** (reported, outside the rule): the push switches recalls up to RR 40% [31, 51] (layer 23). It also switches stated lookups: BL 47% [37, 58] at layer 19 (random 5%) and 41% at layer 23. The slide-6 anchor was not computed, because Gemma's grid has no layer 20.
- **Dan's prediction (Q15.7, "depends on J++ quality").** Consistent. Gemma's J++ beats the logit lens by only +0.07 macro, the smallest margin in results/lens_table/20261023T091623Z/table.md, and it gives no valid cell. This is one model, so it is only weak support.
- **Odd.**
  - On Gemma the push at the question moves lookups about as much as recalls. On Qwen3-32B it moves 0-3% of lookups.
  - The random push is not inert at early layers: at the question phrase, layer 11, it switches 32% of RL.
  - The spec warned in advance that Gemma breaks under most interventions.
- **Files.** results/early_push_where/gemma4itf_d4_where/summary.json, summary.md, analysis-v2.1-20261023T131030Z/, selection.json (the dropped scenes).

## 4. J-space removal on Gemma (gemma4itf_abl_rot_v1). Finding 1 cannot be tested on Gemma

- **What it is.** Removing the J-space part of the residual (25-atom OMP over Zach's J++, at layers 30, 33 and 36) collapses every family to 0-1% right: BL, BR, RL and RR, clean and hop, and the one-hop country controls too (log p −14 to −18). The rotated removal keeps 100% everywhere, so gate G2 passes.
- **Verdict.** There is no verdict code. By the rule's split measure (my computation): gap = mean(BL, RL) − mean(BR, RR) = **+0.5 pts [0, +1.5]** (item bootstrap, 4,000 draws, seed 0). By the letter of the rule that is "absent". In fact it is a floor effect: everything breaks, so the recall-vs-lookup split cannot be tested here. The spec expected "not interpretable".
- **Files.** results/ablate_pilot/gemma4itf_abl_rot_v1/summary.md, summary.json and rows.jsonl.

## Takeaway

1. **B4.** With nothing to point to, the layer-50 patch carries a place label, not a fallback to the 1st sentence: D = +48 [+43, +52] vs a random push near 0. The label is sharp at place 2 (95%). At places 3-5 it is blurry (often one place off) and competes with the original's own answer. Dan's Q23.1 is wrong; Q23.2 is partly right.
2. **Finding 7** (the push writes recall, not the lookup) holds on Qwen3-32B at valid cells (BR 59% vs BL 5%). On Gemma the J++ push does not even write recall at the stated sentence (no valid cell), so Gemma gives no evidence either way.
3. **Gemma J-space removal** destroys every answer, one-hop included, while the rotated control is untouched. Gemma cannot test finding 1's split, and its J++ is the weakest lens relative to the logit lens.
