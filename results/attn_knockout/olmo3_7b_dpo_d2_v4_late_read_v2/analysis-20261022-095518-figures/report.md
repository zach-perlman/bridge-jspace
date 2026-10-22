# attn_knockout / olmo3_7b_dpo_d2_v4_late_read_v2: analysis

EXP olmo3_7b_dpo_d2_v4_late_read_v2 @ 9ac2657 | model Olmo-3-7B-Instruct-DPO | n={'named → prompt': 300, 'memory → prompt': 100} org prompts per family | seeds=[0]

Claim tested: D5b: olmo3_7b_instruct_d2_v4_late_read_v3's grid on the DPO checkpoint

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 1% [0, 5] (n=100)   Baseline: org prompt unedited 100% (100/100)   Control: a statement like the one giving the answer, off the path 100% [96, 100] (n=100); a random span 99% [95, 100] (n=100)
Where the answer goes: 94% [88, 97] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: -
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 1% [0, 3] (n=100 / k=34 / t=9); countries 1% [0, 3] (Wilson [0, 5]; n=100 / k=34 / t=9)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, band4.png, band4.svg, topics.png, topics.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.50, median 1.000; an unedited row moves by up to 0.12 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 33 of 30880 rows (only attention layers are blocked here: no DeltaNet output to rescale).
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 1/100).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): 
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory -; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: memory → prompt: last tokens NEEDED, question words NEEDED
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): named → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-15; named → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 16-23; named → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-15, layers 16-23; memory → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-15, layers 8-11; memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 16-23; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-15, layers 16-23, layers 8-11

Not interpretable / caveats: no control cell drops >= 20 points

## Per topic (entity-cluster intervals; the off-path control: Wilson)

| family | hidden from | layers | topic | n / k / t | answer org kept [95%, entity cluster] | Wilson | control | drop, control - cell [95%, entity cluster] |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 | countries | 100 / 34 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| memory → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 34 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| memory → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 34 / 9 | 96% [91, 100] | [90, 98] | 100% | +4 [+0, +9] |
| memory → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 34 / 9 | 37% [28, 47] | [28, 47] | 100% | +63 [+53, +72] |
| memory → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 34 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| memory → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 34 / 9 | 5% [1, 11] | [2, 11] | 99% | +94 [+86, +99] |
| memory → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 34 / 9 | 14% [8, 20] | [9, 22] | 99% | +85 [+78, +92] |
| memory → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 34 / 9 | 59% [48, 69] | [49, 68] | 98% | +39 [+28, +50] |
| memory → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 34 / 9 | 81% [72, 89] | [72, 87] | 100% | +19 [+11, +28] |
| memory → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 34 / 9 | 96% [91, 100] | [90, 98] | 100% | +4 [+0, +9] |
| memory → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 34 / 9 | 38% [29, 49] | [29, 48] | 100% | +62 [+51, +71] |
| memory → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 34 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| memory → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | all 64 layers | countries | 100 / 34 / 9 | 21% [13, 30] | [14, 30] | 98% | +77 [+67, +86] |
| memory → prompt | the question words | layers 0-3 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 0-15 | countries | 100 / 34 / 9 | 21% [13, 30] | [14, 30] | 98% | +77 [+67, +86] |
| memory → prompt | the question words | layers 4-7 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 8-11 | countries | 100 / 34 / 9 | 60% [49, 71] | [50, 69] | 98% | +38 [+27, +49] |
| memory → prompt | the question words | layers 12-15 | countries | 100 / 34 / 9 | 92% [87, 97] | [85, 96] | 100% | +8 [+3, +13] |
| memory → prompt | the question words | layers 16-19 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | everything after it | all 64 layers | countries | 100 / 34 / 9 | 7% [2, 13] | [3, 14] | 98% | +91 [+85, +96] |
| named → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 34 / 9 | 10% [4, 17] | [6, 17] | 100% | +90 [+83, +96] |
| named → prompt | the last tokens before the answer | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | animals | 100 / 34 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| named → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 15 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| named → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 34 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| named → prompt | the last tokens before the answer | layers 16-23 | animals | 100 / 34 / 9 | 39% [29, 50] | [30, 49] | 100% | +61 [+50, +71] |
| named → prompt | the last tokens before the answer | layers 16-23 | body | 100 / 15 / 9 | 48% [35, 60] | [38, 58] | 100% | +52 [+40, +65] |
| named → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 34 / 9 | 68% [60, 76] | [58, 76] | 100% | +32 [+24, +40] |
| named → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
| named → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 13% [6, 21] | [8, 21] | 100% | +87 [+79, +94] |
| named → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 34 / 9 | 9% [4, 14] | [5, 16] | 100% | +91 [+86, +96] |
| named → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 34 / 9 | 94% [88, 99] | [88, 97] | 100% | +6 [+1, +12] |
| named → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 15 / 9 | 96% [89, 100] | [90, 98] | 100% | +4 [+0, +11] |
| named → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 34 / 9 | 95% [89, 99] | [89, 98] | 100% | +5 [+1, +11] |
| named → prompt | the question words and the last tokens | layers 0-15 | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 | body | 100 / 15 / 9 | 8% [2, 16] | [4, 15] | 100% | +92 [+84, +98] |
| named → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 34 / 9 | 81% [71, 89] | [72, 87] | 100% | +19 [+11, +29] |
| named → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 15 / 9 | 79% [67, 89] | [70, 86] | 100% | +21 [+11, +33] |
| named → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 34 / 9 | 81% [73, 89] | [72, 87] | 100% | +19 [+11, +27] |
| named → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 34 / 9 | 82% [74, 89] | [73, 88] | 100% | +18 [+11, +26] |
| named → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 15 / 9 | 77% [67, 87] | [68, 84] | 100% | +23 [+13, +33] |
| named → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 34 / 9 | 84% [75, 92] | [76, 90] | 100% | +16 [+8, +25] |
| named → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 34 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| named → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 15 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| named → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 34 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| named → prompt | the question words and the last tokens | layers 16-23 | animals | 100 / 34 / 9 | 38% [27, 49] | [29, 48] | 100% | +62 [+51, +73] |
| named → prompt | the question words and the last tokens | layers 16-23 | body | 100 / 15 / 9 | 50% [38, 61] | [40, 60] | 100% | +50 [+39, +62] |
| named → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 34 / 9 | 66% [58, 74] | [56, 75] | 100% | +34 [+26, +42] |
| named → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | all 64 layers | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 13% [6, 22] | [8, 21] | 100% | +87 [+78, +94] |
| named → prompt | the question words | all 64 layers | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | layers 0-3 | animals | 100 / 34 / 9 | 94% [88, 99] | [88, 97] | 100% | +6 [+1, +12] |
| named → prompt | the question words | layers 0-3 | body | 100 / 15 / 9 | 96% [89, 100] | [90, 98] | 100% | +4 [+0, +11] |
| named → prompt | the question words | layers 0-3 | countries | 100 / 34 / 9 | 95% [89, 99] | [89, 98] | 100% | +5 [+1, +11] |
| named → prompt | the question words | layers 0-15 | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | layers 0-15 | body | 100 / 15 / 9 | 12% [5, 21] | [7, 20] | 100% | +88 [+79, +95] |
| named → prompt | the question words | layers 0-15 | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | layers 4-7 | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words | layers 4-7 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | animals | 100 / 34 / 9 | 81% [71, 89] | [72, 87] | 100% | +19 [+11, +29] |
| named → prompt | the question words | layers 8-11 | body | 100 / 15 / 9 | 79% [67, 89] | [70, 86] | 100% | +21 [+11, +33] |
| named → prompt | the question words | layers 8-11 | countries | 100 / 34 / 9 | 82% [74, 89] | [73, 88] | 100% | +18 [+11, +26] |
| named → prompt | the question words | layers 12-15 | animals | 100 / 34 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| named → prompt | the question words | layers 12-15 | body | 100 / 15 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| named → prompt | the question words | layers 12-15 | countries | 100 / 34 / 9 | 89% [82, 95] | [81, 94] | 100% | +11 [+5, +18] |
| named → prompt | the question words | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | everything after it | all 64 layers | animals | 100 / 34 / 9 | 14% [7, 23] | [9, 22] | 100% | +86 [+77, +93] |
| named → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 22% [16, 29] | [15, 31] | 100% | +78 [+71, +84] |
| named → prompt | everything after it | all 64 layers | countries | 100 / 34 / 9 | 16% [10, 23] | [10, 24] | 100% | +84 [+77, +90] |

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|
| memory → prompt | 21% (NEEDED) | 1% (NEEDED) | - | - | - |
| named → prompt | 5% (NEEDED) | 4% (NEEDED) | - | - | - |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|

