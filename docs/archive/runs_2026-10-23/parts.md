# Stated-bridge parts runs, opened 23 Oct evening (UNVERIFIED)

Words: lookup = PP question, recall = PM question. "Switches" means the top token becomes the other bridge's answer after the patch. The lens part is the lens-readable part of the stated bridge's change (jspace); the rest is the change minus it (not_jspace). rest@size is the rest rescaled per row to the lens part's norm (not_jspace_matched). rand_sub is a random slice of the change with the lens part's share of its size; not_rand_sub is the change minus that slice. A valid cell is one in transit on the lens-free map. Rates are Wilson 95%; n = 180 per family unless stated. For every A2/A4 cell quoted, the rates I recomputed from `outcomes.jsonl` match `verdict.md`.

## A2 rest size, Qwen3.6-27B (`d1_rest_size_27b_r2`)
- **Tests:** shrink the rest to the lens part's size. Does it still switch lookups? If not, the lens part's silence on lookups may be only its size.
- **Rule:** at context:32, H-form iff rest@size lookups have lower bound ≥20% and the lens part's upper bound is ≤5%. H-size iff rest@size has upper bound ≤10%.
- **Verdict: H-size** at all 3 cells and in all 3 topics (`results/d1_verdict/d1_rest_size_parts_27b_r2_20261023-140151/verdict.md`).
- **Lookups at context:32:** whole 82% [75, 87], lens part 1% [0, 3], rest 79% [73, 85], **rest@size 1% [0, 3] (1/180)**, rand_sub 0% [0, 2].
- **Recalls, same cell:** lens part 38% [32, 46], rest@size 0% [0, 2], rand_sub 0% [0, 2]. At equal size the lens part moves recalls and the rest moves nothing.
- **not_rand_sub (reported only):** without a random lens-sized slice, lookups stay at 83% and recalls at 80%. Without the lens part, lookups stay at 79% but recalls fall to 27% [21, 34]. So the lens part is needed for recalls, not for lookups.
- **Dan Q20.6:** "above 20%". Wrong (1%).
- **Odd:** none. context:32 and :36 reproduce `d1_topics2_parts_27b` within 2 points (recomputed). The lens part is 10% of the change's squared norm (median).

## A2 rest size, Qwen3.5-9B (`qwen35_9b_d1_rest_size_r2`)
- **Tests and rule:** as the 27B, at decisive cell context:16.
- **Verdict: H-size** at all 3 cells. Per topic (reported only): elements H-size, animals and greek inconclusive (`results/d1_verdict/qwen35_9b_d1_rest_size_parts_r2_20261023-135432/verdict.md`).
- **Lookups at context:16:** whole 56% [48, 63], lens part 1% [0, 3], rest 53% [46, 60], **rest@size 3% [1, 6] (5/180)**, rand_sub 0% [0, 2].
- **Recalls:** lens part 56% [48, 63], rest@size 1% [0, 3], rand_sub 2% [1, 5].
- **not_rand_sub:** lookups 53%, recalls 63% [56, 70]. Without the lens part: lookups 53%, recalls 11% [7, 16]. Same pattern as the 27B.
- **Dan Q20.6:** "above 20%". Wrong (3%).
- **Odd:** rest@size peaks at context:18 at 5% [3, 9], still under the 10% bar. context:16 and :18 reproduce `qwen35_9b_d1_topics2_parts` within 2 points.

## A4 late switch, Qwen3.5-122B, prose (`qwen35_122b_d1_late_parts`, 2x H100)
- **Tests:** past layer 24, where finding 2 failed, does the lens part go quiet on lookups at layers 33 and 36 while still switching recalls?
- **Rule:** late switch iff, at some valid cell, the lens part's lookup upper bound is ≤5%, the rest switches ≥30% of lookups, the lens part switches ≥30% of recalls (point) and beats rand_sub, and it stays ≤10% at the later valid cells. Fails iff the lens part's lookup lower bound is ≥20% at every valid cell.
- **Verdict: inconclusive.** The lookup split holds at bind_bridge:33, context:33 and context:36, but the recall control fails at all three. One topic (elements) holds at bind_bridge:33, reported only (`results/d1_verdict/qwen35_122b_d1_late_parts_20261023-135212/verdict.md`).
- **Lens part on lookups:** bb:30 15% [11, 21] → bb:33 **0% [0, 2]**; ctx:30 16% [11, 22] → ctx:33 1% [0, 3] → ctx:36 0% [0, 2]. The rest at the three 33/36 cells: 42%, 98%, 68%. rand_sub ≤3%.
- **Lens part on recalls:** bb:33 **26% [20, 33] (47/180; 30% needs 54)**, ctx:33 21% [16, 28], ctx:36 8% [5, 13]. rand_sub 1-3%; the whole copy 78-95%. rest@size on lookups: 3%, 8%, 9%.
- **Dan:** Q17.1 "0-20%" right (0-16%). Q17.2 "20-30%" partly (21-37% at layers 30/33, 8-12% at 36). Q17.3 "0-5%" right (rand_sub at ctx:33: 1% of lookups, 2% of recalls). Q20.7 "yes" (rest@size >20%) wrong (3-9%).
- **The layer-30 check, recomputed** from `results/statement_positions/{qwen35_122b_d1_topics2_parts,qwen35_122b_d1_late_parts}/outcomes.jsonl`, H200 → H100:
  - Lens part on recalls: ctx:30 36.1 → 29.4, bb:30 40.6 → 36.7.
  - Lens part on lookups: ctx:30 19.4 → 16.1, ctx:24 29.4 → 33.9 (up), bb:30 15.6 → 15.0.
  - The whole copy moves ±1.
- **How the drift bears on the verdict:** the drift is ±4-7 points, in both directions.
  - "Fails" is ruled out either way: lookups are at 0-1% at layers 33 and 36.
  - The recall miss at bb:33 (26% against the 30% bar, 7 items short) is inside the drift. On the H200 this cell could read as "late switch": the lens part's recall lower bound of 20% clears rand_sub's upper bound of 7%, and no later bind_bridge cell is valid.
  - ctx:33 (9 points short) and ctx:36 (22 points short) miss by more than the drift.

## A4 late switch, Qwen3.5-122B, tables and JSON (`qwen35_122b_d1_formats_late_parts_r2`)
- **Rule:** as the prose run, pooled over both formats. The valid cells are bb:30 and ctx:30/33/36.
- **Verdict: inconclusive.** The split holds at ctx:33 and ctx:36, and the recall control fails at both. By format: tables fail the same way at ctx:33; JSON is inconclusive (`results/d1_verdict/qwen35_122b_d1_formats_late_parts_r2_20261023-145142/verdict.md`).
- **Lens part on lookups:** bb:30 18% [13, 24], ctx:30 27% [21, 34], ctx:33 **1% [0, 3]**, ctx:36 1% [0, 4]. The rest: 32%, 82%, 99%, 78%.
- **Lens part on recalls:** ctx:33 23% [17, 29], ctx:36 8% [5, 13]. rand_sub ≤3%.
- **rest@size on lookups:** ctx:33 17% [12, 23], ctx:36 16% [11, 22], about twice the prose values. By A2's bars that is neither H-form nor H-size; this run's rule does not judge it.
- **not_rand_sub:**
  - At ctx:24, removing the lens part cuts lookups to 58% [51, 65], while removing a random slice of the same size leaves 100%. The lens part is needed for lookups there, which fits finding 2 failing at layer 24.
  - At ctx:33 the two give 99% and 98%, so the lens part is no longer needed.
- **Drift against the H200 formats run** at bb:30, ctx:30 and ctx:24 (recomputed): ≤2.3 points on the lens part, smaller than in prose.
- **Dan Q17.4:** "no, generalizes". Right that tables and JSON give the same answer as prose. He did not pick (a), (b) or (c).

## Gemma 4 31B-it, prose, second scene draw (`gemma4itf_d1_topics2_parts`)
- **Rule:** finding 2 at the map's cell, context:30. It replicates iff the lens part switches ≤10% of lookups and the rest ≥50%, with the recall control ≥30% and keep-answer ≥80%.
- **Verdict: replicates.** n = 167 (`results/d1_verdict/gemma4itf_d1_topics2_parts_20261023-123032/verdict.md`).
- **Lookups:** lens part 0% [0, 2], rest 83% [76, 88], whole 84%, rand_omp 0%.
- **Recalls:** lens part 40% [32, 47], rest 16% [11, 22]. Keep-answer under the lens part: 100% [98, 100].
- **By topic:** elements and greek replicate. Animals is not interpretable: its recall control is 20% [11, 33], n = 50.
- **Dan Q14.2:** "replicates". Right for Gemma.
- **Odd:** n is 167, not 180. The precheck found 182 eligible scenes; I did not check why the rest were dropped.

## Gemma 4 31B-it, tables and JSON (`gemma4itf_d1_formats_parts`)
- **Verdict:** pooled, replicates. n = 169 (`results/d1_verdict/gemma4itf_d1_formats_parts_20261023-133029/verdict.md`).
  - Lookups: lens part 0% [0, 2], rest 74% [67, 80].
  - Recalls: lens part 31% [25, 39]. The point clears the bar but the lower bound is under 30%.
  - Keep-answer: 100%.
- **By format:** tables replicate (n = 79, recalls 39% [29, 50]). JSON is not interpretable: its recall control is 24% [17, 34] (n = 90). By topic, animals and elements are not interpretable.
- **Flag:** the spec says finding 2 holds in tables and JSON "iff the pooled verdict and both format verdicts replicate". By its own rule it is not established on Gemma, even though the `verdict.md` headline reads "replicates".
- **Dan Q15.5:** "replicates". Partly right.

## Qwen3-32B (J++), tables and JSON (`qwen3_32b_jpp_d1_formats_parts`)
- **Verdict: not interpretable: the recall control fails.** Cell context:32, n = 180 (`results/d1_verdict/qwen3_32b_jpp_d1_formats_parts_20261023-122908/verdict.md`).
- **Lookups:** lens part 6% [3, 10], rest 92% [87, 95], whole 100%.
- **Recalls:** lens part **11% [7, 16]**, rest 88% [83, 92], whole 100%.
- The same holds in both formats and in every topic, and it repeats the prose run (recalls 9% [5, 16], n = 120).
- **Dan Q15.5:** "replicates". Wrong; the run cannot decide it.
- **Odd:** on this model the J++-readable part carries little of either question, and the rest carries both.

## Takeaway
1. **Size (A2):** shrunk to the lens part's size, the rest switches no lookups either (27B 1%, 9B 3%). By the pre-registered rule (H-size), the lens part's silence on lookups says nothing about its form. What does stand: at the same size the lens part switches recalls (38%, 56%) and the rest switches none. Also, removing the lens part kills recalls but not lookups, while removing a random slice of the same size changes neither (not_rand_sub, reported only).
2. **122B (A4):** past layer 30 the lens part goes silent on lookups in both scene sets (0-1%), so "finding 2 fails" is ruled out. But its pull on recalls also fades (26%, 21%, 8%) below the 30% bar, so the verdict is inconclusive. At bind_bridge:33 the miss is within the ±4-7-point H100/H200 drift.
3. **Other models:** Gemma replicates in prose and tables; JSON is not interpretable. Qwen3-32B is not interpretable again: its lens part switches 11% of recalls. All UNVERIFIED.
