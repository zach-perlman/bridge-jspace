# attn_knockout / olmo3_7b_instruct_d2_v4_late_read_v3: analysis

EXP olmo3_7b_instruct_d2_v4_late_read_v3 @ 9ac2657 | model Olmo-3-7B-Instruct | n={'named → prompt': 300, 'memory → prompt': 100} org prompts per family | seeds=[0]

Claim tested: On OLMo-3-7B-Instruct (32 layers, softmax attention in each; 3 of 4 sliding-window, 4096 tokens), when the answer's statement is hidden from the last tokens, does a lookup in the prompt (memory -> prompt, named -> prompt) break while a recall (memory -> memory) does not, as on Qwen3.6-27B? In which 4-layer band must the statement stay visible?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 0% [0, 4] (n=100)   Baseline: org prompt unedited 100% (100/100)   Control: a statement like the one giving the answer, off the path 100% [96, 100] (n=100); a random span 100% [96, 100] (n=100)
Where the answer goes: 96% [90, 98] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: -
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 0% [0, 0] (n=100 / k=34 / t=9); countries 0% [0, 0] (Wilson [0, 4]; n=100 / k=34 / t=9)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, band4.png, band4.svg, topics.png, topics.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.73, median 1.000; an unedited row moves by up to 0.22 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 16 of 30888 rows (only attention layers are blocked here: no DeltaNet output to rescale).
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 0/100).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): 
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory -; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: memory → prompt: last tokens NEEDED, question words NEEDED
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): named → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-15; named → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 16-23; named → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-15, layers 16-23; memory → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-15, layers 8-11; memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 16-23; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-15, layers 16-23, layers 8-11, layers 12-15

Not interpretable / caveats: no control cell drops >= 20 points

## Per topic (entity-cluster intervals; the off-path control: Wilson)

| family | hidden from | layers | topic | n / k / t | answer org kept [95%, entity cluster] | Wilson | control | drop, control - cell [95%, entity cluster] |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| memory → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 | countries | 100 / 34 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| memory → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 34 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| memory → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 34 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| memory → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 34 / 9 | 28% [20, 37] | [20, 37] | 100% | +72 [+63, +80] |
| memory → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 34 / 9 | 90% [84, 96] | [83, 94] | 100% | +10 [+4, +16] |
| memory → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 34 / 9 | 3% [0, 7] | [1, 8] | 99% | +96 [+91, +100] |
| memory → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 34 / 9 | 9% [4, 15] | [5, 16] | 99% | +90 [+82, +96] |
| memory → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 34 / 9 | 53% [42, 63] | [43, 62] | 100% | +47 [+37, +58] |
| memory → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 34 / 9 | 74% [65, 82] | [65, 82] | 100% | +26 [+18, +35] |
| memory → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 34 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| memory → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 34 / 9 | 29% [21, 38] | [21, 39] | 100% | +71 [+62, +79] |
| memory → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 34 / 9 | 91% [85, 96] | [84, 95] | 100% | +9 [+4, +15] |
| memory → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | all 64 layers | countries | 100 / 34 / 9 | 14% [7, 21] | [9, 22] | 99% | +85 [+76, +93] |
| memory → prompt | the question words | layers 0-3 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 0-15 | countries | 100 / 34 / 9 | 14% [7, 21] | [9, 22] | 99% | +85 [+76, +93] |
| memory → prompt | the question words | layers 4-7 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 8-11 | countries | 100 / 34 / 9 | 56% [45, 66] | [46, 65] | 100% | +44 [+34, +55] |
| memory → prompt | the question words | layers 12-15 | countries | 100 / 34 / 9 | 87% [81, 92] | [79, 92] | 100% | +13 [+8, +19] |
| memory → prompt | the question words | layers 16-19 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | everything after it | all 64 layers | countries | 100 / 34 / 9 | 4% [1, 8] | [2, 10] | 98% | +94 [+89, +98] |
| named → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 34 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
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
| named → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 34 / 9 | 98% [93, 100] | [93, 99] | 100% | +2 [+0, +7] |
| named → prompt | the last tokens before the answer | layers 16-23 | animals | 100 / 34 / 9 | 38% [28, 49] | [29, 48] | 100% | +62 [+51, +72] |
| named → prompt | the last tokens before the answer | layers 16-23 | body | 100 / 15 / 9 | 43% [30, 56] | [34, 53] | 100% | +57 [+44, +70] |
| named → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 34 / 9 | 59% [51, 67] | [49, 68] | 100% | +41 [+33, +49] |
| named → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 8% [4, 13] | [4, 15] | 100% | +92 [+87, +96] |
| named → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 12% [5, 19] | [7, 20] | 100% | +88 [+81, +95] |
| named → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 34 / 9 | 9% [4, 14] | [5, 16] | 100% | +91 [+86, +96] |
| named → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 34 / 9 | 95% [91, 99] | [89, 98] | 100% | +5 [+1, +9] |
| named → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 15 / 9 | 96% [89, 100] | [90, 98] | 100% | +4 [+0, +11] |
| named → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 34 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| named → prompt | the question words and the last tokens | layers 0-15 | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 | body | 100 / 15 / 9 | 13% [6, 21] | [8, 21] | 100% | +87 [+79, +94] |
| named → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 34 / 9 | 82% [72, 90] | [73, 88] | 100% | +18 [+10, +28] |
| named → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 15 / 9 | 80% [68, 91] | [71, 87] | 100% | +20 [+9, +32] |
| named → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 34 / 9 | 85% [78, 91] | [77, 91] | 100% | +15 [+9, +22] |
| named → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 34 / 9 | 82% [74, 89] | [73, 88] | 100% | +18 [+11, +26] |
| named → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 15 / 9 | 79% [68, 88] | [70, 86] | 100% | +21 [+12, +32] |
| named → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 34 / 9 | 81% [72, 89] | [72, 87] | 100% | +19 [+11, +28] |
| named → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 34 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| named → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 34 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | the question words and the last tokens | layers 16-23 | animals | 100 / 34 / 9 | 36% [26, 47] | [27, 46] | 100% | +64 [+53, +74] |
| named → prompt | the question words and the last tokens | layers 16-23 | body | 100 / 15 / 9 | 44% [31, 57] | [35, 54] | 100% | +56 [+43, +69] |
| named → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 34 / 9 | 59% [51, 66] | [49, 68] | 100% | +41 [+34, +49] |
| named → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | all 64 layers | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 14% [7, 22] | [9, 22] | 100% | +86 [+78, +93] |
| named → prompt | the question words | all 64 layers | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | layers 0-3 | animals | 100 / 34 / 9 | 95% [91, 99] | [89, 98] | 100% | +5 [+1, +9] |
| named → prompt | the question words | layers 0-3 | body | 100 / 15 / 9 | 96% [89, 100] | [90, 98] | 100% | +4 [+0, +11] |
| named → prompt | the question words | layers 0-3 | countries | 100 / 34 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| named → prompt | the question words | layers 0-15 | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | layers 0-15 | body | 100 / 15 / 9 | 15% [8, 23] | [9, 23] | 100% | +85 [+77, +92] |
| named → prompt | the question words | layers 0-15 | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | layers 4-7 | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words | layers 4-7 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | animals | 100 / 34 / 9 | 82% [72, 90] | [73, 88] | 100% | +18 [+10, +28] |
| named → prompt | the question words | layers 8-11 | body | 100 / 15 / 9 | 80% [68, 91] | [71, 87] | 100% | +20 [+9, +32] |
| named → prompt | the question words | layers 8-11 | countries | 100 / 34 / 9 | 85% [78, 91] | [77, 91] | 100% | +15 [+9, +22] |
| named → prompt | the question words | layers 12-15 | animals | 100 / 34 / 9 | 93% [88, 97] | [86, 97] | 100% | +7 [+3, +12] |
| named → prompt | the question words | layers 12-15 | body | 100 / 15 / 9 | 95% [90, 99] | [89, 98] | 100% | +5 [+1, +10] |
| named → prompt | the question words | layers 12-15 | countries | 100 / 34 / 9 | 87% [80, 94] | [79, 92] | 100% | +13 [+6, +20] |
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
| named → prompt | everything after it | all 64 layers | animals | 100 / 34 / 9 | 13% [6, 21] | [8, 21] | 100% | +87 [+79, +94] |
| named → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 19% [13, 26] | [13, 28] | 100% | +81 [+74, +87] |
| named → prompt | everything after it | all 64 layers | countries | 100 / 34 / 9 | 15% [8, 23] | [9, 23] | 100% | +85 [+77, +92] |

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|
| memory → prompt | 14% (NEEDED) | 0% (NEEDED) | - | - | - |
| named → prompt | 5% (NEEDED) | 4% (NEEDED) | - | - | - |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H-late-read | statement hidden from the last tokens in every layer: memory -> prompt still right <= 20% (upper bound) pooled, memory -> memory >= 90% (lower bound). Prior 0.7 | see summary.json | - |
| H-band | the band whose blocking alone breaks memory -> prompt most lies at or after layer 16 (the last third or the 4-layer bands 16-27). Prior 0.6 | see summary.json | - |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>system
You are a helpful function-calling AI assistant. You do not currently have access to any functions. <functions></functions><|im_end|>
<|im_start|>user
The Japan file is in drawer 2. The Kenya file is in drawer 6. The Venezuela file is in drawer 3. The Thailand file is in drawer 7. The Iran file is in drawer 1.
Which drawer holds the file on the country whose capital is Caracas? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
Answer: 
```

memory → prompt, org prompt countries-RL-e5f0-0021. What was done: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers (the statement: 'The Venezuela file is in drawer 3.'). Unedited the model answers '3' (answer org '3'); with the statement hidden it answers '2', another answer that is in the prompt (the prompt's other answers: ['1', '2', '6', '7']). log p(answer org): -0.000 -> -8.072.

