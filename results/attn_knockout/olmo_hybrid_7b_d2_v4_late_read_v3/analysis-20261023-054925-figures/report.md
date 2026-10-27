# attn_knockout / olmo_hybrid_7b_d2_v4_late_read_v3: analysis

EXP olmo_hybrid_7b_d2_v4_late_read_v3 @ unknown | model Olmo-Hybrid-Instruct-DPO-7B | n={'named → prompt': 300, 'memory → prompt': 100} org prompts per family | seeds=[0]

Claim tested: On Olmo-Hybrid-7B Instruct (32 layers: Gated DeltaNet in 24, full attention without RoPE in 8), when the answer's statement is hidden from the last tokens, does a lookup in the prompt (memory -> prompt, named -> prompt) break while a recall (memory -> memory) does not, as on Qwen3.6-27B and OLMo-3-7B? In which 4-layer band must the statement stay visible?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 7% [3, 14] (n=100)   Baseline: org prompt unedited 100% (100/100)   Control: a statement like the one giving the answer, off the path 99% [95, 100] (n=100); a random span 100% [96, 100] (n=100)
Where the answer goes: 71% [61, 79] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: -
By layer kind: hidden in every attention layer only: 8% [4, 15] (n=100); hidden in every DeltaNet layer only: 99% [95, 100] (n=100)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every attention layer: pooled 8% [2, 15] (n=100 / k=36 / t=9); countries 8% [2, 15] (Wilson [4, 15]; n=100 / k=36 / t=9)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every DeltaNet layer: pooled 99% [97, 100] (n=100 / k=36 / t=9); countries 99% [97, 100] (Wilson [95, 100]; n=100 / k=36 / t=9)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 7% [2, 13] (n=100 / k=36 / t=9); countries 7% [2, 13] (Wilson [3, 14]; n=100 / k=36 / t=9)
Per topic: named → prompt, the statement giving the answer hidden from the last tokens before the answer in every attention layer: pooled 8% [5, 11] (n=300 / k=85 / t=9); animals 10% [5, 15] (Wilson [6, 17]; n=100 / k=34 / t=9); body 1% [0, 3] (Wilson [0, 5]; n=100 / k=15 / t=9); countries 12% [6, 19] (Wilson [7, 20]; n=100 / k=36 / t=9)
Per topic: named → prompt, the statement giving the answer hidden from the last tokens before the answer in every DeltaNet layer: pooled 100% [100, 100] (n=300 / k=85 / t=9); animals 100% [100, 100] (Wilson [96, 100]; n=100 / k=34 / t=9); body 100% [100, 100] (Wilson [96, 100]; n=100 / k=15 / t=9); countries 100% [100, 100] (Wilson [96, 100]; n=100 / k=36 / t=9)
H-general (memory → prompt, last tokens: every attention layer <= 20% and every DeltaNet layer >= 90% in each topic, on the entity-cluster bounds): holds (countries: holds)
H-general (named → prompt, last tokens: every attention layer <= 20% and every DeltaNet layer >= 90% in each topic, on the entity-cluster bounds): holds (animals: holds; body: holds; countries: holds)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, band4.png, band4.svg, norm_ratio.png, norm_ratio.svg, topics.png, topics.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.57, median 1.000; an unedited row moves by up to 0.25 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 89 of 50072 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.979 of normal) and the controls (0.983), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 7/100).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): 
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory -; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: memory → prompt: last tokens NEEDED, question words NEEDED
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): named → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-15, layers 0-15 (attention layers only), layers 8-11; NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 16-23, layers 16-23 (attention layers only); NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-15, layers 0-15 (attention layers only), layers 16-23, layers 16-23 (attention layers only), layers 8-11; NEEDED in every attention layer; memory → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-15, layers 0-15 (attention layers only), layers 0-15 (DeltaNet layers only), layers 8-11; NEEDED in every attention layer, every DeltaNet layer; memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 16-23, layers 16-23 (attention layers only), layers 16-19; NEEDED in every attention layer; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-15, layers 0-15 (attention layers only), layers 0-15 (DeltaNet layers only), layers 16-23, layers 16-23 (attention layers only), layers 8-11, layers 16-19; NEEDED in every attention layer, every DeltaNet layer

Not interpretable / caveats: no control cell drops >= 20 points

## Per topic (entity-cluster intervals; the off-path control: Wilson)

| family | hidden from | layers | topic | n / k / t | answer org kept [95%, entity cluster] | Wilson | control | drop, control - cell [95%, entity cluster] |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 7% [2, 13] | [3, 14] | 99% | +92 [+86, +97] |
| memory → prompt | the last tokens before the answer | every attention layer | countries | 100 / 36 / 9 | 8% [2, 15] | [4, 15] | 99% | +91 [+84, +97] |
| memory → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 36 / 9 | 71% [59, 82] | [61, 79] | 100% | +29 [+18, +41] |
| memory → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 36 / 9 | 18% [10, 26] | [12, 27] | 100% | +82 [+74, +90] |
| memory → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 15% [8, 23] | [9, 23] | 100% | +85 [+77, +92] |
| memory → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | every DeltaNet layer | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 6% [2, 10] | [3, 12] | 97% | +91 [+86, +96] |
| memory → prompt | the question words and the last tokens | every attention layer | countries | 100 / 36 / 9 | 5% [1, 9] | [2, 11] | 99% | +94 [+89, +98] |
| memory → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [-3, +3] |
| memory → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 36 / 9 | 20% [12, 29] | [13, 29] | 95% | +75 [+66, +83] |
| memory → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 37% [28, 45] | [28, 47] | 99% | +62 [+53, +71] |
| memory → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 67% [58, 76] | [57, 75] | 97% | +30 [+21, +40] |
| memory → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 36 / 9 | 17% [10, 24] | [11, 26] | 99% | +82 [+75, +89] |
| memory → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 36 / 9 | 83% [76, 90] | [74, 89] | 99% | +16 [+9, +23] |
| memory → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 36 / 9 | 73% [62, 83] | [64, 81] | 100% | +27 [+17, +38] |
| memory → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 36 / 9 | 17% [9, 25] | [11, 26] | 100% | +83 [+75, +91] |
| memory → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 15% [8, 23] | [9, 23] | 100% | +85 [+77, +92] |
| memory → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | every DeltaNet layer | countries | 100 / 36 / 9 | 69% [60, 78] | [59, 77] | 97% | +28 [+19, +38] |
| memory → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 21% [13, 30] | [14, 30] | 96% | +75 [+66, +83] |
| memory → prompt | the question words | every attention layer | countries | 100 / 36 / 9 | 35% [27, 43] | [26, 45] | 99% | +64 [+56, +72] |
| memory → prompt | the question words | layers 0-3 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [-3, +3] |
| memory → prompt | the question words | layers 0-15 | countries | 100 / 36 / 9 | 20% [12, 28] | [13, 29] | 96% | +76 [+67, +84] |
| memory → prompt | the question words | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 35% [27, 43] | [26, 45] | 99% | +64 [+56, +72] |
| memory → prompt | the question words | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 72% [63, 81] | [63, 80] | 97% | +25 [+17, +34] |
| memory → prompt | the question words | layers 4-7 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 8-11 | countries | 100 / 36 / 9 | 19% [12, 27] | [13, 28] | 99% | +80 [+72, +88] |
| memory → prompt | the question words | layers 12-15 | countries | 100 / 36 / 9 | 84% [77, 91] | [76, 90] | 99% | +15 [+8, +22] |
| memory → prompt | the question words | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | every DeltaNet layer | countries | 100 / 36 / 9 | 73% [64, 82] | [64, 81] | 97% | +24 [+16, +33] |
| memory → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 5% [1, 9] | [2, 11] | 83% | +78 [+68, +87] |
| named → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 3% [0, 6] | [1, 8] | 100% | +97 [+94, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 11% [5, 18] | [6, 19] | 100% | +89 [+82, +95] |
| named → prompt | the last tokens before the answer | every attention layer | animals | 100 / 34 / 9 | 10% [5, 15] | [6, 17] | 100% | +90 [+85, +95] |
| named → prompt | the last tokens before the answer | every attention layer | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | every attention layer | countries | 100 / 36 / 9 | 12% [6, 19] | [7, 20] | 100% | +88 [+81, +94] |
| named → prompt | the last tokens before the answer | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 15 / 9 | 95% [91, 98] | [89, 98] | 100% | +5 [+2, +9] |
| named → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 36 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| named → prompt | the last tokens before the answer | layers 16-23 | animals | 100 / 34 / 9 | 42% [33, 52] | [33, 52] | 100% | +58 [+48, +67] |
| named → prompt | the last tokens before the answer | layers 16-23 | body | 100 / 15 / 9 | 11% [7, 15] | [6, 19] | 100% | +89 [+85, +93] |
| named → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 36 / 9 | 33% [24, 42] | [25, 43] | 100% | +67 [+58, +76] |
| named → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | animals | 100 / 34 / 9 | 42% [32, 53] | [33, 52] | 100% | +58 [+47, +68] |
| named → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 10% [6, 15] | [6, 17] | 100% | +90 [+85, +94] |
| named → prompt | the last tokens before the answer | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 33% [24, 42] | [25, 43] | 100% | +67 [+58, +76] |
| named → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | every DeltaNet layer | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | every DeltaNet layer | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | every DeltaNet layer | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 7% [3, 12] | [3, 14] | 100% | +93 [+88, +97] |
| named → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 27% [19, 36] | [19, 36] | 100% | +73 [+64, +81] |
| named → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 8% [3, 13] | [4, 15] | 100% | +92 [+87, +97] |
| named → prompt | the question words and the last tokens | every attention layer | animals | 100 / 34 / 9 | 6% [2, 11] | [3, 12] | 100% | +94 [+89, +98] |
| named → prompt | the question words and the last tokens | every attention layer | body | 100 / 15 / 9 | 13% [6, 22] | [8, 21] | 100% | +87 [+78, +94] |
| named → prompt | the question words and the last tokens | every attention layer | countries | 100 / 36 / 9 | 10% [5, 15] | [6, 17] | 100% | +90 [+85, +95] |
| named → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 0-15 | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 | body | 100 / 15 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
| named → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 29% [19, 39] | [21, 39] | 100% | +71 [+61, +81] |
| named → prompt | the question words and the last tokens | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 5% [1, 9] | [2, 11] | 100% | +95 [+91, +99] |
| named → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | animals | 100 / 34 / 9 | 80% [69, 89] | [71, 87] | 100% | +20 [+11, +31] |
| named → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 34 / 9 | 22% [14, 30] | [15, 31] | 100% | +78 [+70, +86] |
| named → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 15 / 9 | 66% [55, 76] | [56, 75] | 100% | +34 [+24, +45] |
| named → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 36 / 9 | 49% [41, 58] | [39, 59] | 100% | +51 [+42, +59] |
| named → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 34 / 9 | 90% [82, 97] | [83, 94] | 100% | +10 [+3, +18] |
| named → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 15 / 9 | 83% [75, 90] | [74, 89] | 100% | +17 [+10, +25] |
| named → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 36 / 9 | 72% [64, 80] | [63, 80] | 100% | +28 [+20, +36] |
| named → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 34 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| named → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 15 / 9 | 93% [88, 97] | [86, 97] | 100% | +7 [+3, +12] |
| named → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 36 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| named → prompt | the question words and the last tokens | layers 16-23 | animals | 100 / 34 / 9 | 36% [28, 44] | [27, 46] | 100% | +64 [+56, +72] |
| named → prompt | the question words and the last tokens | layers 16-23 | body | 100 / 15 / 9 | 5% [2, 9] | [2, 11] | 100% | +95 [+91, +98] |
| named → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 36 / 9 | 28% [19, 37] | [20, 37] | 100% | +72 [+63, +81] |
| named → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | animals | 100 / 34 / 9 | 37% [29, 46] | [28, 47] | 100% | +63 [+54, +71] |
| named → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 6% [2, 10] | [3, 12] | 100% | +94 [+90, +98] |
| named → prompt | the question words and the last tokens | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 28% [19, 37] | [20, 37] | 100% | +72 [+63, +81] |
| named → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | every DeltaNet layer | animals | 100 / 34 / 9 | 82% [73, 90] | [73, 88] | 100% | +18 [+10, +27] |
| named → prompt | the question words and the last tokens | every DeltaNet layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | every DeltaNet layer | countries | 100 / 36 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | the question words | all 64 layers | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 9% [4, 14] | [5, 16] | 100% | +91 [+86, +96] |
| named → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | every attention layer | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | every attention layer | body | 100 / 15 / 9 | 29% [19, 39] | [21, 39] | 100% | +71 [+61, +81] |
| named → prompt | the question words | every attention layer | countries | 100 / 36 / 9 | 4% [1, 8] | [2, 10] | 100% | +96 [+92, +99] |
| named → prompt | the question words | layers 0-3 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 0-3 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 0-3 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 0-15 | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | layers 0-15 | body | 100 / 15 / 9 | 9% [4, 14] | [5, 16] | 100% | +91 [+86, +96] |
| named → prompt | the question words | layers 0-15 | countries | 100 / 36 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | layers 0-15 (attention layers only) | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | layers 0-15 (attention layers only) | body | 100 / 15 / 9 | 29% [19, 39] | [21, 39] | 100% | +71 [+61, +81] |
| named → prompt | the question words | layers 0-15 (attention layers only) | countries | 100 / 36 / 9 | 4% [1, 8] | [2, 10] | 100% | +96 [+92, +99] |
| named → prompt | the question words | layers 0-15 (DeltaNet layers only) | animals | 100 / 34 / 9 | 81% [71, 90] | [72, 87] | 100% | +19 [+10, +29] |
| named → prompt | the question words | layers 0-15 (DeltaNet layers only) | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 0-15 (DeltaNet layers only) | countries | 100 / 36 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | the question words | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 4-7 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | animals | 100 / 34 / 9 | 22% [14, 30] | [15, 31] | 100% | +78 [+70, +86] |
| named → prompt | the question words | layers 8-11 | body | 100 / 15 / 9 | 64% [53, 75] | [54, 73] | 100% | +36 [+25, +47] |
| named → prompt | the question words | layers 8-11 | countries | 100 / 36 / 9 | 47% [38, 56] | [38, 57] | 100% | +53 [+44, +62] |
| named → prompt | the question words | layers 12-15 | animals | 100 / 34 / 9 | 91% [83, 98] | [84, 95] | 100% | +9 [+2, +17] |
| named → prompt | the question words | layers 12-15 | body | 100 / 15 / 9 | 83% [75, 90] | [74, 89] | 100% | +17 [+10, +25] |
| named → prompt | the question words | layers 12-15 | countries | 100 / 36 / 9 | 75% [67, 83] | [66, 82] | 100% | +25 [+17, +33] |
| named → prompt | the question words | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-23 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (attention layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (attention layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (attention layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (DeltaNet layers only) | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (DeltaNet layers only) | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-31 (DeltaNet layers only) | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | every DeltaNet layer | animals | 100 / 34 / 9 | 82% [72, 91] | [73, 88] | 100% | +18 [+9, +28] |
| named → prompt | the question words | every DeltaNet layer | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | every DeltaNet layer | countries | 100 / 36 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | everything after it | all 64 layers | animals | 100 / 34 / 9 | 13% [6, 20] | [8, 21] | 100% | +87 [+80, +94] |
| named → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 32% [24, 41] | [24, 42] | 99% | +67 [+58, +75] |
| named → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 13% [7, 20] | [8, 21] | 99% | +86 [+79, +93] |

## Dan's predictions (predictions/2026-10-20_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|
| memory → prompt | 21% (NEEDED) | 7% (NEEDED) | 8% (NEEDED) | 99% (NOT NEEDED) | - |
| named → prompt | 4% (NEEDED) | 5% (NEEDED) | 8% (NEEDED) | 100% (NOT NEEDED) | - |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H-late-read | statement hidden from the last tokens in every layer: memory -> prompt still right <= 20% (upper bound) pooled, memory -> memory >= 90% (lower bound). Prior 0.7 (copied from olmo3_7b_instruct_d2_v4_late_read_v3) | see summary.json | - |
| H-band | the band whose blocking alone breaks memory -> prompt most lies at or after layer 16 (the last third or the 4-layer bands 16-27). Prior 0.6 (copied from olmo3_7b_instruct_d2_v4_late_read_v3) | see summary.json | - |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The file on Portugal is kept in drawer 5. The file on Austria is kept in drawer 9. The file on Italy is kept in drawer 2. The file on Spain is kept in drawer 8. The file on Philippines is kept in drawer 7.
In which drawer is the file on the country whose capital is Vienna? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

memory → prompt, org prompt countries-RL-e5f0-0016. What was done: memory → prompt, the statement giving the answer hidden from the question words in all 64 layers (the statement: 'The file on Austria is kept in drawer 9.'). Unedited the model answers '9' (answer org '9'); with the statement hidden it answers '5', another answer that is in the prompt (the prompt's other answers: ['2', '5', '7', '8']). log p(answer org): -0.000 -> -5.434.

