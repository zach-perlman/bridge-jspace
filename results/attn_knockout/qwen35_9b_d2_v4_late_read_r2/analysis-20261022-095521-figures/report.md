# attn_knockout / qwen35_9b_d2_v4_late_read_r2: analysis

EXP qwen35_9b_d2_v4_late_read_r2 @ 0c0c675 | model Qwen3.5-9B | n={'memory → prompt': 300, 'named → prompt': 300, 'memory → memory': 200} org prompts per family | seeds=[0]

Claim tested: On Qwen3.5-9B, when the answer's statement is hidden from the last tokens in every attention layer, does a lookup in the prompt break (as on the 27B: 2-13% kept) while hiding it in every DeltaNet layer changes nothing (27B: 100%)?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 2% [1, 5] (n=300)   Baseline: org prompt unedited 100% (300/300)   Control: a statement like the one giving the answer, off the path 100% [99, 100] (n=300); a random span 100% [99, 100] (n=300)
Where the answer goes: 97% [94, 98] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: 94% [90, 97] (n=200)
By layer kind: hidden in every attention layer only: 3% [1, 5] (n=300); hidden in every DeltaNet layer only: 100% [98, 100] (n=300)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every attention layer: pooled 3% [1, 5] (n=300 / k=79 / t=9); animals 6% [2, 11] (Wilson [3, 12]; n=100 / k=28 / t=9); body 1% [0, 3] (Wilson [0, 5]; n=100 / k=15 / t=9); countries 1% [0, 3] (Wilson [0, 5]; n=100 / k=36 / t=9)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every DeltaNet layer: pooled 100% [99, 100] (n=300 / k=79 / t=9); animals 100% [100, 100] (Wilson [96, 100]; n=100 / k=28 / t=9); body 99% [97, 100] (Wilson [95, 100]; n=100 / k=15 / t=9); countries 100% [100, 100] (Wilson [96, 100]; n=100 / k=36 / t=9)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 2% [1, 4] (n=300 / k=79 / t=9); animals 6% [2, 11] (Wilson [3, 12]; n=100 / k=28 / t=9); body 0% [0, 0] (Wilson [0, 4]; n=100 / k=15 / t=9); countries 1% [0, 3] (Wilson [0, 5]; n=100 / k=36 / t=9)
Per topic: named → prompt, the statement giving the answer hidden from the last tokens before the answer in every attention layer: pooled 6% [4, 9] (n=300 / k=79 / t=9); animals 10% [4, 17] (Wilson [6, 17]; n=100 / k=28 / t=9); body 2% [0, 5] (Wilson [1, 7]; n=100 / k=15 / t=9); countries 7% [2, 13] (Wilson [3, 14]; n=100 / k=36 / t=9)
Per topic: named → prompt, the statement giving the answer hidden from the last tokens before the answer in every DeltaNet layer: pooled 100% [100, 100] (n=300 / k=79 / t=9); animals 100% [100, 100] (Wilson [96, 100]; n=100 / k=28 / t=9); body 100% [100, 100] (Wilson [96, 100]; n=100 / k=15 / t=9); countries 100% [100, 100] (Wilson [96, 100]; n=100 / k=36 / t=9)
Per topic: memory → memory, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 94% [90, 98] (n=200 / k=43 / t=9); animals 91% [83, 97] (Wilson [84, 95]; n=100 / k=28 / t=9); body 97% [94, 100] (Wilson [92, 99]; n=100 / k=15 / t=9)
H-general (memory → prompt, last tokens: every attention layer <= 20% and every DeltaNet layer >= 90% in each topic, on the entity-cluster bounds): holds (animals: holds; body: holds; countries: holds)
H-general (named → prompt, last tokens: every attention layer <= 20% and every DeltaNet layer >= 90% in each topic, on the entity-cluster bounds): holds (animals: holds; body: holds; countries: holds)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, band4.png, band4.svg, norm_ratio.png, norm_ratio.svg, topics.png, topics.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.41, median 0.978; an unedited row moves by up to 0.19 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 62 of 100800 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.968 of normal) and the controls (0.972), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 7/300).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): 
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory NOT NEEDED; holds = True
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: memory → prompt: last tokens NEEDED, question words NEEDED
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): memory → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-15, layers 0-15 (attention layers only), layers 8-11; NEEDED in every attention layer; memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 16-23, layers 16-23 (attention layers only); NEEDED in every attention layer; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-15, layers 0-15 (attention layers only), layers 16-23, layers 16-23 (attention layers only), layers 8-11; NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-15, layers 0-15 (attention layers only); NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 16-23; NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-15, layers 0-15 (attention layers only), layers 16-23; NEEDED in every attention layer

Not interpretable / caveats: no control cell drops >= 20 points

## Per topic (entity-cluster intervals; the off-path control: Wilson)

| family | hidden from | layers | topic | n / k / t | answer org kept [95%, entity cluster] | Wilson | control | drop, control - cell [95%, entity cluster] |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 28 / 9 | 6% [2, 11] | [3, 12] | 100% | +94 [+89, +98] |
| memory → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| memory → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | every attention layer | animals | 100 / 28 / 9 | 6% [2, 11] | [3, 12] | 100% | +94 [+89, +98] |
| memory → prompt | the last tokens before the answer | every attention layer | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | every attention layer | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | layers 0-3 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 0-15 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 0-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-19 | animals | 100 / 28 / 9 | 95% [91, 99] | [89, 98] | 100% | +5 [+1, +9] |
| memory → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 16-23 | animals | 100 / 28 / 9 | 58% [50, 67] | [48, 67] | 100% | +42 [+33, +50] |
| memory → prompt | the last tokens before the answer | layers 16-23 | body | 100 / 15 / 9 | 61% [46, 74] | [51, 70] | 100% | +39 [+26, +54] |
| memory → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 36 / 9 | 48% [40, 56] | [38, 58] | 100% | +52 [+44, +60] |
| memory → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | animals | 100 / 28 / 9 | 63% [54, 72] | [53, 72] | 100% | +37 [+28, +46] |
| memory → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 64% [49, 77] | [54, 73] | 100% | +36 [+23, +51] |
| memory → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 49% [39, 59] | [39, 59] | 100% | +51 [+41, +61] |
| memory → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 28 / 9 | 95% [91, 99] | [89, 98] | 100% | +5 [+1, +9] |
| memory → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 15 / 9 | 92% [85, 98] | [85, 96] | 100% | +8 [+2, +15] |
| memory → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 36 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| memory → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-31 | animals | 100 / 28 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| memory → prompt | the last tokens before the answer | layers 24-31 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | animals | 100 / 28 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| memory → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | every DeltaNet layer | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | every DeltaNet layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 28 / 9 | 5% [1, 10] | [2, 11] | 99% | +94 [+88, +99] |
| memory → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 5% [1, 10] | [2, 11] | 100% | +95 [+90, +99] |
| memory → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 3% [0, 6] | [1, 8] | 99% | +96 [+92, +99] |
| memory → prompt | the question words and the last tokens | every attention layer | animals | 100 / 28 / 9 | 8% [3, 15] | [4, 15] | 100% | +92 [+85, +97] |
| memory → prompt | the question words and the last tokens | every attention layer | body | 100 / 15 / 9 | 3% [0, 8] | [1, 8] | 100% | +97 [+92, +100] |
| memory → prompt | the question words and the last tokens | every attention layer | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 28 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 0-15 | animals | 100 / 28 / 9 | 47% [37, 57] | [38, 57] | 99% | +52 [+42, +62] |
| memory → prompt | the question words and the last tokens | layers 0-15 | body | 100 / 15 / 9 | 57% [42, 72] | [47, 66] | 100% | +43 [+28, +58] |
| memory → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 36 / 9 | 56% [47, 64] | [46, 65] | 99% | +43 [+34, +52] |
| memory → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | animals | 100 / 28 / 9 | 53% [44, 62] | [43, 62] | 100% | +47 [+38, +56] |
| memory → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 62% [46, 78] | [52, 71] | 100% | +38 [+22, +54] |
| memory → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 63% [54, 72] | [53, 72] | 100% | +37 [+28, +46] |
| memory → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | animals | 100 / 28 / 9 | 96% [91, 100] | [90, 98] | 99% | +3 [+0, +8] |
| memory → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 92% [83, 99] | [85, 96] | 100% | +8 [+1, +17] |
| memory → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 95% [89, 99] | [89, 98] | 100% | +5 [+1, +11] |
| memory → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 28 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| memory → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [-3, +3] |
| memory → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 28 / 9 | 73% [64, 82] | [64, 81] | 99% | +26 [+16, +36] |
| memory → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 15 / 9 | 80% [66, 92] | [71, 87] | 100% | +20 [+8, +34] |
| memory → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 36 / 9 | 81% [73, 89] | [72, 87] | 100% | +19 [+11, +27] |
| memory → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 28 / 9 | 90% [84, 95] | [83, 94] | 100% | +10 [+5, +16] |
| memory → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 15 / 9 | 95% [90, 99] | [89, 98] | 100% | +5 [+1, +10] |
| memory → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 36 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| memory → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 28 / 9 | 94% [90, 98] | [88, 97] | 100% | +6 [+2, +10] |
| memory → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 16-23 | animals | 100 / 28 / 9 | 58% [49, 68] | [48, 67] | 100% | +42 [+32, +51] |
| memory → prompt | the question words and the last tokens | layers 16-23 | body | 100 / 15 / 9 | 58% [43, 71] | [48, 67] | 100% | +42 [+29, +57] |
| memory → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 36 / 9 | 48% [40, 56] | [38, 58] | 100% | +52 [+44, +60] |
| memory → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | animals | 100 / 28 / 9 | 63% [54, 72] | [53, 72] | 100% | +37 [+28, +46] |
| memory → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 63% [49, 76] | [53, 72] | 100% | +37 [+24, +51] |
| memory → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 49% [39, 59] | [39, 59] | 100% | +51 [+41, +61] |
| memory → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 28 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| memory → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 15 / 9 | 91% [84, 97] | [84, 95] | 100% | +9 [+3, +16] |
| memory → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 36 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| memory → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-31 | animals | 100 / 28 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| memory → prompt | the question words and the last tokens | layers 24-31 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | animals | 100 / 28 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| memory → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | every DeltaNet layer | animals | 100 / 28 / 9 | 95% [89, 99] | [89, 98] | 99% | +4 [+0, +10] |
| memory → prompt | the question words and the last tokens | every DeltaNet layer | body | 100 / 15 / 9 | 92% [83, 99] | [85, 96] | 100% | +8 [+1, +17] |
| memory → prompt | the question words and the last tokens | every DeltaNet layer | countries | 100 / 36 / 9 | 94% [88, 99] | [88, 97] | 100% | +6 [+1, +12] |
| memory → prompt | the question words | all 64 layers | animals | 100 / 28 / 9 | 54% [45, 62] | [44, 63] | 100% | +46 [+38, +55] |
| memory → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 70% [53, 85] | [60, 78] | 100% | +30 [+15, +47] |
| memory → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 60% [51, 69] | [50, 69] | 99% | +39 [+29, +49] |
| memory → prompt | the question words | every attention layer | animals | 100 / 28 / 9 | 63% [54, 73] | [53, 72] | 100% | +37 [+27, +46] |
| memory → prompt | the question words | every attention layer | body | 100 / 15 / 9 | 75% [60, 88] | [66, 82] | 100% | +25 [+12, +40] |
| memory → prompt | the question words | every attention layer | countries | 100 / 36 / 9 | 67% [59, 74] | [57, 75] | 100% | +33 [+26, +41] |
| memory → prompt | the question words | layers 0-3 | animals | 100 / 28 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-15 | animals | 100 / 28 / 9 | 51% [43, 59] | [41, 61] | 100% | +49 [+41, +57] |
| memory → prompt | the question words | layers 0-15 | body | 100 / 15 / 9 | 70% [53, 85] | [60, 78] | 100% | +30 [+15, +47] |
| memory → prompt | the question words | layers 0-15 | countries | 100 / 36 / 9 | 62% [52, 71] | [52, 71] | 99% | +37 [+27, +47] |
| memory → prompt | the question words | layers 0-15 (attention layers only) | animals | 100 / 28 / 9 | 63% [54, 73] | [53, 72] | 100% | +37 [+27, +46] |
| memory → prompt | the question words | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 75% [60, 88] | [66, 82] | 100% | +25 [+12, +40] |
| memory → prompt | the question words | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 67% [58, 75] | [57, 75] | 100% | +33 [+25, +42] |
| memory → prompt | the question words | layers 0-15 (DeltaNet layers only) | animals | 100 / 28 / 9 | 96% [91, 100] | [90, 98] | 99% | +3 [+0, +8] |
| memory → prompt | the question words | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 92% [82, 100] | [85, 96] | 100% | +8 [+0, +18] |
| memory → prompt | the question words | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 96% [91, 100] | [90, 98] | 100% | +4 [+0, +9] |
| memory → prompt | the question words | layers 4-7 | animals | 100 / 28 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| memory → prompt | the question words | layers 4-7 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 8-11 | animals | 100 / 28 / 9 | 72% [64, 80] | [63, 80] | 100% | +28 [+20, +36] |
| memory → prompt | the question words | layers 8-11 | body | 100 / 15 / 9 | 82% [69, 94] | [73, 88] | 100% | +18 [+6, +31] |
| memory → prompt | the question words | layers 8-11 | countries | 100 / 36 / 9 | 80% [72, 88] | [71, 87] | 100% | +20 [+12, +28] |
| memory → prompt | the question words | layers 12-15 | animals | 100 / 28 / 9 | 95% [90, 99] | [89, 98] | 100% | +5 [+1, +10] |
| memory → prompt | the question words | layers 12-15 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 12-15 | countries | 100 / 36 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| memory → prompt | the question words | layers 16-19 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | every DeltaNet layer | animals | 100 / 28 / 9 | 95% [89, 99] | [89, 98] | 99% | +4 [+0, +9] |
| memory → prompt | the question words | every DeltaNet layer | body | 100 / 15 / 9 | 92% [82, 100] | [85, 96] | 100% | +8 [+0, +18] |
| memory → prompt | the question words | every DeltaNet layer | countries | 100 / 36 / 9 | 95% [89, 99] | [89, 98] | 100% | +5 [+1, +11] |
| memory → prompt | everything after it | all 64 layers | animals | 100 / 28 / 9 | 2% [0, 6] | [1, 7] | 98% | +96 [+91, +100] |
| memory → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 5% [1, 10] | [2, 11] | 99% | +94 [+89, +98] |
| memory → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 28 / 9 | 11% [5, 18] | [6, 19] | 100% | +89 [+82, +95] |
| named → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the last tokens before the answer | every attention layer | animals | 100 / 28 / 9 | 10% [4, 17] | [6, 17] | 100% | +90 [+83, +96] |
| named → prompt | the last tokens before the answer | every attention layer | body | 100 / 15 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the last tokens before the answer | every attention layer | countries | 100 / 36 / 9 | 7% [2, 13] | [3, 14] | 100% | +93 [+87, +98] |
| named → prompt | the last tokens before the answer | layers 0-3 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-23 | animals | 100 / 28 / 9 | 74% [65, 83] | [65, 82] | 100% | +26 [+17, +35] |
| named → prompt | the last tokens before the answer | layers 16-23 | body | 100 / 15 / 9 | 85% [77, 91] | [77, 91] | 100% | +15 [+9, +23] |
| named → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 36 / 9 | 76% [68, 83] | [67, 83] | 100% | +24 [+17, +32] |
| named → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | animals | 100 / 28 / 9 | 73% [65, 81] | [64, 81] | 100% | +27 [+19, +35] |
| named → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 87% [79, 93] | [79, 92] | 100% | +13 [+7, +21] |
| named → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 81% [74, 88] | [72, 87] | 100% | +19 [+12, +26] |
| named → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | every DeltaNet layer | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | every DeltaNet layer | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 28 / 9 | 20% [12, 28] | [13, 29] | 100% | +80 [+72, +88] |
| named → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 24% [18, 29] | [17, 33] | 100% | +76 [+71, +82] |
| named → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 15% [8, 23] | [9, 23] | 100% | +85 [+77, +92] |
| named → prompt | the question words and the last tokens | every attention layer | animals | 100 / 28 / 9 | 23% [14, 32] | [16, 32] | 100% | +77 [+68, +86] |
| named → prompt | the question words and the last tokens | every attention layer | body | 100 / 15 / 9 | 22% [15, 29] | [15, 31] | 100% | +78 [+71, +85] |
| named → prompt | the question words and the last tokens | every attention layer | countries | 100 / 36 / 9 | 14% [7, 22] | [9, 22] | 100% | +86 [+78, +93] |
| named → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-15 | animals | 100 / 28 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 | body | 100 / 15 / 9 | 8% [3, 13] | [4, 15] | 100% | +92 [+87, +97] |
| named → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | animals | 100 / 28 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 19% [12, 27] | [13, 28] | 100% | +81 [+73, +88] |
| named → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 28 / 9 | 69% [57, 81] | [59, 77] | 100% | +31 [+19, +43] |
| named → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 15 / 9 | 96% [92, 100] | [90, 98] | 100% | +4 [+0, +8] |
| named → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 36 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| named → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 28 / 9 | 79% [71, 87] | [70, 86] | 100% | +21 [+13, +29] |
| named → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 15 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| named → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 36 / 9 | 87% [81, 93] | [79, 92] | 100% | +13 [+7, +19] |
| named → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 28 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 15 / 9 | 93% [86, 98] | [86, 97] | 100% | +7 [+2, +14] |
| named → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 36 / 9 | 80% [71, 88] | [71, 87] | 100% | +20 [+12, +29] |
| named → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-23 | animals | 100 / 28 / 9 | 69% [61, 78] | [59, 77] | 100% | +31 [+22, +39] |
| named → prompt | the question words and the last tokens | layers 16-23 | body | 100 / 15 / 9 | 86% [80, 91] | [78, 91] | 100% | +14 [+9, +20] |
| named → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 36 / 9 | 77% [70, 84] | [68, 84] | 100% | +23 [+16, +30] |
| named → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | animals | 100 / 28 / 9 | 73% [65, 81] | [64, 81] | 100% | +27 [+19, +35] |
| named → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 87% [79, 93] | [79, 92] | 100% | +13 [+7, +21] |
| named → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 81% [74, 88] | [72, 87] | 100% | +19 [+12, +26] |
| named → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | every DeltaNet layer | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | every DeltaNet layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | all 64 layers | animals | 100 / 28 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 8% [3, 13] | [4, 15] | 100% | +92 [+87, +97] |
| named → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | every attention layer | animals | 100 / 28 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | every attention layer | body | 100 / 15 / 9 | 23% [14, 33] | [16, 32] | 100% | +77 [+67, +86] |
| named → prompt | the question words | every attention layer | countries | 100 / 36 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | layers 0-3 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-15 | animals | 100 / 28 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | layers 0-15 | body | 100 / 15 / 9 | 8% [3, 13] | [4, 15] | 100% | +92 [+87, +97] |
| named → prompt | the question words | layers 0-15 | countries | 100 / 36 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | layers 0-15 (attention layers only) | animals | 100 / 28 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 22% [13, 32] | [15, 31] | 100% | +78 [+68, +87] |
| named → prompt | the question words | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | layers 0-15 (DeltaNet layers only) | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 4-7 | animals | 100 / 28 / 9 | 69% [57, 81] | [59, 77] | 100% | +31 [+19, +43] |
| named → prompt | the question words | layers 4-7 | body | 100 / 15 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| named → prompt | the question words | layers 4-7 | countries | 100 / 36 / 9 | 95% [91, 99] | [89, 98] | 100% | +5 [+1, +9] |
| named → prompt | the question words | layers 8-11 | animals | 100 / 28 / 9 | 79% [71, 87] | [70, 86] | 100% | +21 [+13, +29] |
| named → prompt | the question words | layers 8-11 | body | 100 / 15 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| named → prompt | the question words | layers 8-11 | countries | 100 / 36 / 9 | 88% [82, 94] | [80, 93] | 100% | +12 [+6, +18] |
| named → prompt | the question words | layers 12-15 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 12-15 | body | 100 / 15 / 9 | 96% [89, 100] | [90, 98] | 100% | +4 [+0, +11] |
| named → prompt | the question words | layers 12-15 | countries | 100 / 36 / 9 | 91% [86, 96] | [84, 95] | 100% | +9 [+4, +14] |
| named → prompt | the question words | layers 16-19 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | every DeltaNet layer | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | every DeltaNet layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | everything after it | all 64 layers | animals | 100 / 28 / 9 | 19% [11, 28] | [13, 28] | 100% | +81 [+72, +89] |
| named → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 27% [21, 33] | [19, 36] | 100% | +73 [+67, +79] |
| named → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 13% [7, 20] | [8, 21] | 100% | +87 [+80, +93] |
| memory → memory | the last tokens before the answer | all 64 layers | animals | 100 / 28 / 9 | 91% [83, 97] | [84, 95] | 100% | +9 [+3, +17] |
| memory → memory | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| memory → memory | the last tokens before the answer | every attention layer | animals | 100 / 28 / 9 | 94% [88, 99] | [88, 97] | 100% | +6 [+1, +12] |
| memory → memory | the last tokens before the answer | every attention layer | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the last tokens before the answer | layers 0-3 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-3 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 0-15 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-15 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 0-15 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 4-7 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 8-11 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 12-15 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 16-19 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 16-19 | body | 100 / 15 / 9 | 99% [96, 100] | [95, 100] | 100% | +1 [+0, +4] |
| memory → memory | the last tokens before the answer | layers 16-23 | animals | 100 / 28 / 9 | 95% [88, 100] | [89, 98] | 100% | +5 [+0, +12] |
| memory → memory | the last tokens before the answer | layers 16-23 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the last tokens before the answer | layers 16-23 (attention layers only) | animals | 100 / 28 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| memory → memory | the last tokens before the answer | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 20-23 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-27 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-31 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 28-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | every DeltaNet layer | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | every DeltaNet layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | all 64 layers | animals | 100 / 28 / 9 | 90% [82, 96] | [83, 94] | 99% | +9 [+3, +16] |
| memory → memory | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | every attention layer | animals | 100 / 28 / 9 | 89% [81, 95] | [81, 94] | 100% | +11 [+5, +19] |
| memory → memory | the question words and the last tokens | every attention layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 0-3 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-3 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 0-15 | animals | 100 / 28 / 9 | 94% [87, 99] | [88, 97] | 99% | +5 [+1, +11] |
| memory → memory | the question words and the last tokens | layers 0-15 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 0-15 (attention layers only) | animals | 100 / 28 / 9 | 94% [88, 98] | [88, 97] | 100% | +6 [+2, +12] |
| memory → memory | the question words and the last tokens | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 4-7 | animals | 100 / 28 / 9 | 98% [93, 100] | [93, 99] | 100% | +2 [+0, +7] |
| memory → memory | the question words and the last tokens | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → memory | the question words and the last tokens | layers 8-11 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 8-11 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 12-15 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 16-19 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 16-19 | body | 100 / 15 / 9 | 99% [96, 100] | [95, 100] | 100% | +1 [+0, +4] |
| memory → memory | the question words and the last tokens | layers 16-23 | animals | 100 / 28 / 9 | 93% [84, 99] | [86, 97] | 100% | +7 [+1, +16] |
| memory → memory | the question words and the last tokens | layers 16-23 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 16-23 (attention layers only) | animals | 100 / 28 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| memory → memory | the question words and the last tokens | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 99% [96, 100] | [95, 100] | 100% | +1 [+0, +4] |
| memory → memory | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 20-23 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-27 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-31 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 28-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | every DeltaNet layer | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | every DeltaNet layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | all 64 layers | animals | 100 / 28 / 9 | 93% [85, 98] | [86, 97] | 99% | +6 [+1, +13] |
| memory → memory | the question words | all 64 layers | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [-3, +3] |
| memory → memory | the question words | every attention layer | animals | 100 / 28 / 9 | 95% [89, 99] | [89, 98] | 100% | +5 [+1, +11] |
| memory → memory | the question words | every attention layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 0-3 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 0-3 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 0-15 | animals | 100 / 28 / 9 | 94% [87, 99] | [88, 97] | 99% | +5 [+1, +11] |
| memory → memory | the question words | layers 0-15 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [-3, +3] |
| memory → memory | the question words | layers 0-15 (attention layers only) | animals | 100 / 28 / 9 | 95% [89, 99] | [89, 98] | 100% | +5 [+1, +11] |
| memory → memory | the question words | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 0-15 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [-3, +3] |
| memory → memory | the question words | layers 4-7 | animals | 100 / 28 / 9 | 98% [93, 100] | [93, 99] | 100% | +2 [+0, +7] |
| memory → memory | the question words | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → memory | the question words | layers 8-11 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 12-15 | animals | 100 / 28 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-19 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-23 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-23 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-23 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 20-23 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-27 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-31 (attention layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-31 (DeltaNet layers only) | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 28-31 | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | every DeltaNet layer | animals | 100 / 28 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | every DeltaNet layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [-3, +3] |
| memory → memory | everything after it | all 64 layers | animals | 100 / 28 / 9 | 90% [82, 96] | [83, 94] | 99% | +9 [+3, +17] |
| memory → memory | everything after it | all 64 layers | body | 100 / 15 / 9 | 96% [93, 99] | [90, 98] | 100% | +4 [+1, +7] |

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|
| memory → prompt | 61% (NEEDED) | 2% (NEEDED) | 3% (NEEDED) | 100% (NOT NEEDED) | - |
| named → prompt | 3% (NEEDED) | 5% (NEEDED) | 6% (NEEDED) | 100% (NOT NEEDED) | - |
| memory → memory | 96% (NOT NEEDED) | 94% (PARTIAL) | 96% (NOT NEEDED) | 100% (NOT NEEDED) | null (memory) |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H-attn | memory -> prompt, statement hidden from the tokens after the question in every attention layer: still right upper bound <= 25%; in every DeltaNet layer: lower bound >= 85%; memory -> memory >= 85% in both. Prior 0.65 | see summary.json | - |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>user
Drawer 7 holds the Cuba file. Drawer 4 holds the Canada file. Drawer 6 holds the Kenya file. Drawer 8 holds the Iraq file. Drawer 9 holds the Chile file.
What drawer keeps the file on the country whose capital is Santiago? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

memory → prompt, org prompt countries-RL-e5f0-0031. What was done: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers (the statement: 'Drawer 9 holds the Chile file.'). Unedited the model answers '9' (answer org '9'); with the statement hidden it answers '6', another answer that is in the prompt (the prompt's other answers: ['4', '6', '7', '8']). log p(answer org): -0.014 -> -4.803.

