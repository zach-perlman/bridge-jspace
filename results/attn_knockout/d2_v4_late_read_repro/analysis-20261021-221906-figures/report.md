# attn_knockout / d2_v4_late_read_repro: analysis

EXP d2_v4_late_read_repro @ unknown | model Qwen3.6-27B | n={'memory → prompt': 300, 'named → prompt': 300, 'memory → memory': 300} org prompts per family | seeds=[0]

Claim tested: Does d2_v4_late_read reproduce: the same items and, per cell, the same kept counts (or within bf16 noise)?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 9% [6, 12] (n=300)   Baseline: org prompt unedited 100% (300/300)   Control: a statement like the one giving the answer, off the path 100% [99, 100] (n=300); a random span 100% [99, 100] (n=300)
Where the answer goes: 88% [84, 91] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: 93% [90, 96] (n=300)
By layer kind: hidden in every attention layer only: 9% [6, 12] (n=300); hidden in every DeltaNet layer only: 100% [99, 100] (n=300)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every attention layer: pooled 9% [6, 11] (n=300 / k=85 / t=9); animals 13% [8, 19] (Wilson [8, 21]; n=100 / k=34 / t=9); body 2% [0, 5] (Wilson [1, 7]; n=100 / k=15 / t=9); countries 11% [6, 16] (Wilson [6, 19]; n=100 / k=36 / t=9)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every DeltaNet layer: pooled 100% [100, 100] (n=300 / k=85 / t=9); animals 100% [100, 100] (Wilson [96, 100]; n=100 / k=34 / t=9); body 100% [100, 100] (Wilson [96, 100]; n=100 / k=15 / t=9); countries 100% [100, 100] (Wilson [96, 100]; n=100 / k=36 / t=9)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 9% [6, 11] (n=300 / k=85 / t=9); animals 12% [7, 18] (Wilson [7, 20]; n=100 / k=34 / t=9); body 2% [0, 5] (Wilson [1, 7]; n=100 / k=15 / t=9); countries 12% [7, 17] (Wilson [7, 20]; n=100 / k=36 / t=9)
Per topic: named → prompt, the statement giving the answer hidden from the last tokens before the answer in every attention layer: pooled 11% [8, 15] (n=300 / k=85 / t=9); animals 16% [9, 23] (Wilson [10, 24]; n=100 / k=34 / t=9); body 1% [0, 3] (Wilson [0, 5]; n=100 / k=15 / t=9); countries 17% [11, 24] (Wilson [11, 26]; n=100 / k=36 / t=9)
Per topic: named → prompt, the statement giving the answer hidden from the last tokens before the answer in every DeltaNet layer: pooled 100% [100, 100] (n=300 / k=85 / t=9); animals 100% [100, 100] (Wilson [96, 100]; n=100 / k=34 / t=9); body 100% [100, 100] (Wilson [96, 100]; n=100 / k=15 / t=9); countries 100% [100, 100] (Wilson [96, 100]; n=100 / k=36 / t=9)
Per topic: memory → memory, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 99% [98, 100] (n=300 / k=85 / t=9); animals 98% [95, 100] (Wilson [93, 99]; n=100 / k=34 / t=9); body 100% [100, 100] (Wilson [96, 100]; n=100 / k=15 / t=9); countries 100% [100, 100] (Wilson [96, 100]; n=100 / k=36 / t=9)
H-general (memory → prompt, last tokens: every attention layer <= 20% and every DeltaNet layer >= 90% in each topic, on the entity-cluster bounds): holds (animals: holds; body: holds; countries: holds)
H-general (named → prompt, last tokens: every attention layer <= 20% and every DeltaNet layer >= 90% in each topic, on the entity-cluster bounds): partly (animals: point; body: holds; countries: point)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, norm_ratio.png, norm_ratio.svg, topics.png, topics.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.51, median 0.995; an unedited row moves by up to 0.19 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 38 of 75600 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.967 of normal) and the controls (0.972), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 26/300).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): memory → prompt: passed (the statement giving the answer NEEDED); named → prompt: passed (the statement giving the answer NEEDED)
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory PARTIAL; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: memory → prompt: last tokens NEEDED, question words PARTIAL
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 32-47, layers 32-47 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-31, layers 0-31 (attention layers only); NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-31, layers 0-31 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer

Not interpretable / caveats: no control cell drops >= 20 points

## Per topic (entity-cluster intervals; the off-path control: Wilson)

| family | hidden from | layers | topic | n / k / t | answer org kept [95%, entity cluster] | Wilson | control | drop, control - cell [95%, entity cluster] |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 12% [7, 18] | [7, 20] | 100% | +88 [+82, +93] |
| memory → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| memory → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 12% [7, 17] | [7, 20] | 100% | +88 [+83, +93] |
| memory → prompt | the last tokens before the answer | every attention layer | animals | 100 / 34 / 9 | 13% [8, 19] | [8, 21] | 100% | +87 [+81, +92] |
| memory → prompt | the last tokens before the answer | every attention layer | body | 100 / 15 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| memory → prompt | the last tokens before the answer | every attention layer | countries | 100 / 36 / 9 | 11% [6, 16] | [6, 19] | 100% | +89 [+84, +94] |
| memory → prompt | the last tokens before the answer | layers 0-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-47 | animals | 100 / 34 / 9 | 79% [71, 87] | [70, 86] | 100% | +21 [+13, +29] |
| memory → prompt | the last tokens before the answer | layers 32-47 | body | 100 / 15 / 9 | 90% [83, 96] | [83, 94] | 100% | +10 [+4, +17] |
| memory → prompt | the last tokens before the answer | layers 32-47 | countries | 100 / 36 / 9 | 84% [77, 91] | [76, 90] | 100% | +16 [+9, +23] |
| memory → prompt | the last tokens before the answer | layers 32-47 (attention layers only) | animals | 100 / 34 / 9 | 78% [70, 86] | [69, 85] | 100% | +22 [+14, +30] |
| memory → prompt | the last tokens before the answer | layers 32-47 (attention layers only) | body | 100 / 15 / 9 | 90% [83, 96] | [83, 94] | 100% | +10 [+4, +17] |
| memory → prompt | the last tokens before the answer | layers 32-47 (attention layers only) | countries | 100 / 36 / 9 | 83% [75, 90] | [74, 89] | 100% | +17 [+10, +25] |
| memory → prompt | the last tokens before the answer | layers 32-47 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-47 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-47 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 48-63 | animals | 100 / 34 / 9 | 24% [17, 32] | [17, 33] | 100% | +76 [+68, +83] |
| memory → prompt | the last tokens before the answer | layers 48-63 | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | layers 48-63 | countries | 100 / 36 / 9 | 25% [17, 34] | [18, 34] | 100% | +75 [+66, +83] |
| memory → prompt | the last tokens before the answer | layers 48-63 (attention layers only) | animals | 100 / 34 / 9 | 23% [16, 31] | [16, 32] | 100% | +77 [+69, +84] |
| memory → prompt | the last tokens before the answer | layers 48-63 (attention layers only) | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | layers 48-63 (attention layers only) | countries | 100 / 36 / 9 | 22% [15, 29] | [15, 31] | 100% | +78 [+71, +85] |
| memory → prompt | the last tokens before the answer | layers 48-63 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 48-63 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 48-63 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | every DeltaNet layer | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | every DeltaNet layer | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 6% [2, 10] | [3, 12] | 100% | +94 [+90, +98] |
| memory → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 5% [1, 9] | [2, 11] | 100% | +95 [+91, +99] |
| memory → prompt | the question words and the last tokens | every attention layer | animals | 100 / 34 / 9 | 6% [2, 10] | [3, 12] | 100% | +94 [+90, +98] |
| memory → prompt | the question words and the last tokens | every attention layer | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the question words and the last tokens | every attention layer | countries | 100 / 36 / 9 | 10% [5, 15] | [6, 17] | 100% | +90 [+85, +95] |
| memory → prompt | the question words and the last tokens | layers 0-31 | animals | 100 / 34 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| memory → prompt | the question words and the last tokens | layers 0-31 | body | 100 / 15 / 9 | 96% [91, 100] | [90, 98] | 100% | +4 [+0, +9] |
| memory → prompt | the question words and the last tokens | layers 0-31 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 0-31 (attention layers only) | animals | 100 / 34 / 9 | 92% [86, 98] | [85, 96] | 100% | +8 [+2, +14] |
| memory → prompt | the question words and the last tokens | layers 0-31 (attention layers only) | body | 100 / 15 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| memory → prompt | the question words and the last tokens | layers 0-31 (attention layers only) | countries | 100 / 36 / 9 | 95% [89, 99] | [89, 98] | 100% | +5 [+1, +11] |
| memory → prompt | the question words and the last tokens | layers 0-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 0-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 0-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 32-47 | animals | 100 / 34 / 9 | 43% [33, 52] | [34, 53] | 100% | +57 [+48, +67] |
| memory → prompt | the question words and the last tokens | layers 32-47 | body | 100 / 15 / 9 | 37% [27, 47] | [28, 47] | 100% | +63 [+53, +73] |
| memory → prompt | the question words and the last tokens | layers 32-47 | countries | 100 / 36 / 9 | 45% [36, 54] | [36, 55] | 100% | +55 [+46, +64] |
| memory → prompt | the question words and the last tokens | layers 32-47 (attention layers only) | animals | 100 / 34 / 9 | 41% [32, 50] | [32, 51] | 100% | +59 [+50, +68] |
| memory → prompt | the question words and the last tokens | layers 32-47 (attention layers only) | body | 100 / 15 / 9 | 40% [29, 51] | [31, 50] | 100% | +60 [+49, +71] |
| memory → prompt | the question words and the last tokens | layers 32-47 (attention layers only) | countries | 100 / 36 / 9 | 45% [35, 55] | [36, 55] | 100% | +55 [+45, +65] |
| memory → prompt | the question words and the last tokens | layers 32-47 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 32-47 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 32-47 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 48-63 | animals | 100 / 34 / 9 | 13% [7, 20] | [8, 21] | 100% | +87 [+80, +93] |
| memory → prompt | the question words and the last tokens | layers 48-63 | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the question words and the last tokens | layers 48-63 | countries | 100 / 36 / 9 | 10% [4, 16] | [6, 17] | 100% | +90 [+84, +96] |
| memory → prompt | the question words and the last tokens | layers 48-63 (attention layers only) | animals | 100 / 34 / 9 | 13% [7, 20] | [8, 21] | 100% | +87 [+80, +93] |
| memory → prompt | the question words and the last tokens | layers 48-63 (attention layers only) | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the question words and the last tokens | layers 48-63 (attention layers only) | countries | 100 / 36 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
| memory → prompt | the question words and the last tokens | layers 48-63 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 48-63 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 48-63 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | every DeltaNet layer | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | every DeltaNet layer | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | all 64 layers | animals | 100 / 34 / 9 | 86% [79, 93] | [78, 91] | 100% | +14 [+7, +21] |
| memory → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 89% [79, 97] | [81, 94] | 100% | +11 [+3, +21] |
| memory → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 95% [91, 99] | [89, 98] | 100% | +5 [+1, +9] |
| memory → prompt | the question words | every attention layer | animals | 100 / 34 / 9 | 89% [82, 95] | [81, 94] | 100% | +11 [+5, +18] |
| memory → prompt | the question words | every attention layer | body | 100 / 15 / 9 | 89% [79, 97] | [81, 94] | 100% | +11 [+3, +21] |
| memory → prompt | the question words | every attention layer | countries | 100 / 36 / 9 | 89% [82, 95] | [81, 94] | 100% | +11 [+5, +18] |
| memory → prompt | the question words | layers 0-31 | animals | 100 / 34 / 9 | 94% [89, 99] | [88, 97] | 100% | +6 [+1, +11] |
| memory → prompt | the question words | layers 0-31 | body | 100 / 15 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| memory → prompt | the question words | layers 0-31 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 0-31 (attention layers only) | animals | 100 / 34 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| memory → prompt | the question words | layers 0-31 (attention layers only) | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words | layers 0-31 (attention layers only) | countries | 100 / 36 / 9 | 95% [89, 99] | [89, 98] | 100% | +5 [+1, +11] |
| memory → prompt | the question words | layers 0-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-47 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 32-47 | body | 100 / 15 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| memory → prompt | the question words | layers 32-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-47 (attention layers only) | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 32-47 (attention layers only) | body | 100 / 15 / 9 | 96% [89, 100] | [90, 98] | 100% | +4 [+0, +11] |
| memory → prompt | the question words | layers 32-47 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-47 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-47 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-47 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | every DeltaNet layer | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | every DeltaNet layer | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | everything after it | all 64 layers | animals | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 99% | +99 [+97, +100] |
| memory → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 17% [10, 24] | [11, 26] | 100% | +83 [+76, +90] |
| named → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 18% [12, 25] | [12, 27] | 100% | +82 [+75, +88] |
| named → prompt | the last tokens before the answer | every attention layer | animals | 100 / 34 / 9 | 16% [9, 23] | [10, 24] | 100% | +84 [+77, +91] |
| named → prompt | the last tokens before the answer | every attention layer | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | every attention layer | countries | 100 / 36 / 9 | 17% [11, 24] | [11, 26] | 100% | +83 [+76, +89] |
| named → prompt | the last tokens before the answer | layers 0-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-63 | animals | 100 / 34 / 9 | 13% [7, 19] | [8, 21] | 100% | +87 [+81, +93] |
| named → prompt | the last tokens before the answer | layers 48-63 | body | 100 / 15 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the last tokens before the answer | layers 48-63 | countries | 100 / 36 / 9 | 4% [1, 8] | [2, 10] | 100% | +96 [+92, +99] |
| named → prompt | the last tokens before the answer | layers 48-63 (attention layers only) | animals | 100 / 34 / 9 | 12% [7, 18] | [7, 20] | 100% | +88 [+82, +93] |
| named → prompt | the last tokens before the answer | layers 48-63 (attention layers only) | body | 100 / 15 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the last tokens before the answer | layers 48-63 (attention layers only) | countries | 100 / 36 / 9 | 3% [0, 6] | [1, 8] | 100% | +97 [+94, +100] |
| named → prompt | the last tokens before the answer | layers 48-63 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-63 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-63 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | every DeltaNet layer | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | every DeltaNet layer | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 24% [15, 34] | [17, 33] | 100% | +76 [+66, +85] |
| named → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 20% [11, 29] | [13, 29] | 100% | +80 [+71, +89] |
| named → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 17% [10, 25] | [11, 26] | 100% | +83 [+75, +90] |
| named → prompt | the question words and the last tokens | every attention layer | animals | 100 / 34 / 9 | 22% [13, 32] | [15, 31] | 100% | +78 [+68, +87] |
| named → prompt | the question words and the last tokens | every attention layer | body | 100 / 15 / 9 | 13% [7, 20] | [8, 21] | 100% | +87 [+80, +93] |
| named → prompt | the question words and the last tokens | every attention layer | countries | 100 / 36 / 9 | 16% [9, 23] | [10, 24] | 100% | +84 [+77, +91] |
| named → prompt | the question words and the last tokens | layers 0-31 | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words and the last tokens | layers 0-31 | body | 100 / 15 / 9 | 42% [30, 54] | [33, 52] | 100% | +58 [+46, +70] |
| named → prompt | the question words and the last tokens | layers 0-31 | countries | 100 / 36 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
| named → prompt | the question words and the last tokens | layers 0-31 (attention layers only) | animals | 100 / 34 / 9 | 4% [1, 8] | [2, 10] | 100% | +96 [+92, +99] |
| named → prompt | the question words and the last tokens | layers 0-31 (attention layers only) | body | 100 / 15 / 9 | 80% [67, 91] | [71, 87] | 100% | +20 [+9, +33] |
| named → prompt | the question words and the last tokens | layers 0-31 (attention layers only) | countries | 100 / 36 / 9 | 41% [30, 52] | [32, 51] | 100% | +59 [+48, +70] |
| named → prompt | the question words and the last tokens | layers 0-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 32-47 | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 32-47 | body | 100 / 15 / 9 | 89% [85, 93] | [81, 94] | 100% | +11 [+7, +15] |
| named → prompt | the question words and the last tokens | layers 32-47 | countries | 100 / 36 / 9 | 92% [86, 97] | [85, 96] | 100% | +8 [+3, +14] |
| named → prompt | the question words and the last tokens | layers 32-47 (attention layers only) | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 32-47 (attention layers only) | body | 100 / 15 / 9 | 91% [86, 96] | [84, 95] | 100% | +9 [+4, +14] |
| named → prompt | the question words and the last tokens | layers 32-47 (attention layers only) | countries | 100 / 36 / 9 | 92% [86, 97] | [85, 96] | 100% | +8 [+3, +14] |
| named → prompt | the question words and the last tokens | layers 32-47 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 32-47 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 32-47 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 48-63 | animals | 100 / 34 / 9 | 12% [7, 18] | [7, 20] | 100% | +88 [+82, +93] |
| named → prompt | the question words and the last tokens | layers 48-63 | body | 100 / 15 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words and the last tokens | layers 48-63 | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words and the last tokens | layers 48-63 (attention layers only) | animals | 100 / 34 / 9 | 12% [7, 18] | [7, 20] | 100% | +88 [+82, +93] |
| named → prompt | the question words and the last tokens | layers 48-63 (attention layers only) | body | 100 / 15 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words and the last tokens | layers 48-63 (attention layers only) | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words and the last tokens | layers 48-63 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 48-63 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 48-63 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | every DeltaNet layer | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | every DeltaNet layer | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | all 64 layers | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 23% [12, 34] | [16, 32] | 100% | +77 [+66, +88] |
| named → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | every attention layer | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | every attention layer | body | 100 / 15 / 9 | 47% [33, 61] | [38, 57] | 100% | +53 [+39, +67] |
| named → prompt | the question words | every attention layer | countries | 100 / 36 / 9 | 6% [2, 11] | [3, 12] | 100% | +94 [+89, +98] |
| named → prompt | the question words | layers 0-31 | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | layers 0-31 | body | 100 / 15 / 9 | 42% [30, 54] | [33, 52] | 100% | +58 [+46, +70] |
| named → prompt | the question words | layers 0-31 | countries | 100 / 36 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
| named → prompt | the question words | layers 0-31 (attention layers only) | animals | 100 / 34 / 9 | 4% [1, 8] | [2, 10] | 100% | +96 [+92, +99] |
| named → prompt | the question words | layers 0-31 (attention layers only) | body | 100 / 15 / 9 | 81% [69, 92] | [72, 87] | 100% | +19 [+8, +31] |
| named → prompt | the question words | layers 0-31 (attention layers only) | countries | 100 / 36 / 9 | 40% [29, 51] | [31, 50] | 100% | +60 [+49, +71] |
| named → prompt | the question words | layers 0-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-47 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words | layers 32-47 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words | layers 32-47 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-47 (attention layers only) | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words | layers 32-47 (attention layers only) | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words | layers 32-47 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-47 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-47 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | every DeltaNet layer | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | every DeltaNet layer | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | everything after it | all 64 layers | animals | 100 / 34 / 9 | 23% [13, 33] | [16, 32] | 100% | +77 [+67, +87] |
| named → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 23% [16, 30] | [16, 32] | 100% | +77 [+70, +84] |
| named → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 25% [17, 33] | [18, 34] | 100% | +75 [+67, +83] |
| memory → memory | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | every attention layer | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the last tokens before the answer | every attention layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | every attention layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-31 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-47 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 32-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-47 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-47 (attention layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 32-47 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-47 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-47 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-47 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-63 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-63 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-63 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-63 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-63 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-63 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-63 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | every DeltaNet layer | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | every DeltaNet layer | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 89% [80, 97] | [81, 94] | 100% | +11 [+3, +20] |
| memory → memory | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 91% [82, 98] | [84, 95] | 99% | +8 [+2, +17] |
| memory → memory | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | every attention layer | animals | 100 / 34 / 9 | 91% [82, 98] | [84, 95] | 100% | +9 [+2, +18] |
| memory → memory | the question words and the last tokens | every attention layer | body | 100 / 15 / 9 | 91% [82, 98] | [84, 95] | 100% | +9 [+2, +18] |
| memory → memory | the question words and the last tokens | every attention layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-31 | animals | 100 / 34 / 9 | 93% [86, 99] | [86, 97] | 100% | +7 [+1, +14] |
| memory → memory | the question words and the last tokens | layers 0-31 | body | 100 / 15 / 9 | 92% [85, 98] | [85, 96] | 99% | +7 [+2, +14] |
| memory → memory | the question words and the last tokens | layers 0-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-31 (attention layers only) | animals | 100 / 34 / 9 | 96% [91, 100] | [90, 98] | 100% | +4 [+0, +9] |
| memory → memory | the question words and the last tokens | layers 0-31 (attention layers only) | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 0-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 97% [92, 100] | [92, 99] | 99% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 0-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 32-47 | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 32-47 | body | 100 / 15 / 9 | 93% [85, 99] | [86, 97] | 100% | +7 [+1, +15] |
| memory → memory | the question words and the last tokens | layers 32-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 32-47 (attention layers only) | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 32-47 (attention layers only) | body | 100 / 15 / 9 | 91% [80, 99] | [84, 95] | 100% | +9 [+1, +20] |
| memory → memory | the question words and the last tokens | layers 32-47 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 32-47 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 32-47 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 32-47 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-63 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-63 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-63 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-63 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-63 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-63 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-63 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | every DeltaNet layer | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | every DeltaNet layer | body | 100 / 15 / 9 | 97% [92, 100] | [92, 99] | 99% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | all 64 layers | animals | 100 / 34 / 9 | 94% [87, 99] | [88, 97] | 100% | +6 [+1, +13] |
| memory → memory | the question words | all 64 layers | body | 100 / 15 / 9 | 92% [85, 98] | [85, 96] | 100% | +8 [+2, +15] |
| memory → memory | the question words | all 64 layers | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | every attention layer | animals | 100 / 34 / 9 | 95% [90, 99] | [89, 98] | 100% | +5 [+1, +10] |
| memory → memory | the question words | every attention layer | body | 100 / 15 / 9 | 94% [88, 99] | [88, 97] | 100% | +6 [+1, +12] |
| memory → memory | the question words | every attention layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 0-31 | animals | 100 / 34 / 9 | 96% [91, 100] | [90, 98] | 100% | +4 [+0, +9] |
| memory → memory | the question words | layers 0-31 | body | 100 / 15 / 9 | 93% [86, 99] | [86, 97] | 100% | +7 [+1, +14] |
| memory → memory | the question words | layers 0-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 0-31 (attention layers only) | animals | 100 / 34 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| memory → memory | the question words | layers 0-31 (attention layers only) | body | 100 / 15 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| memory → memory | the question words | layers 0-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 0-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 0-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words | layers 0-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-47 | body | 100 / 15 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| memory → memory | the question words | layers 32-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-47 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-47 (attention layers only) | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words | layers 32-47 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-47 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-47 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-47 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-63 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-63 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-63 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-63 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-63 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-63 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-63 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | every DeltaNet layer | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | every DeltaNet layer | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 99% | +1 [+0, +3] |
| memory → memory | the question words | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | everything after it | all 64 layers | animals | 100 / 34 / 9 | 89% [78, 98] | [81, 94] | 100% | +11 [+2, +22] |
| memory → memory | everything after it | all 64 layers | body | 100 / 15 / 9 | 94% [86, 100] | [88, 97] | 100% | +6 [+0, +14] |
| memory → memory | everything after it | all 64 layers | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | layers 0-31 | layers 32-47 | layers 48-63 | 48-63, attention only | 48-63, DeltaNet only | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|---|---|---|---|---|
| memory → prompt | 90% (PARTIAL) | 9% (NEEDED) | 100% (NOT NEEDED) | 84% (PARTIAL) | 17% (NEEDED) | 15% (NEEDED) | 100% (NOT NEEDED) | 9% (NEEDED) | 100% (NOT NEEDED) | no |
| named → prompt | 8% (NEEDED) | 12% (NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 6% (NEEDED) | 5% (NEEDED) | 100% (NOT NEEDED) | 11% (NEEDED) | 100% (NOT NEEDED) | yes |
| memory → memory | 95% (NOT NEEDED) | 99% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 99% (NOT NEEDED) | 100% (NOT NEEDED) | null (memory) |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H-same | the same item ids per family; per (family, destination, layer set) the kept counts differ by <= 2 items. Prior 0.85 | see summary.json | - |

