# attn_knockout / qwen3_32b_d2_v4_late_read_v2_r2: analysis

EXP qwen3_32b_d2_v4_late_read_v2_r2 @ 0c0c675 | model Qwen3-32B | n={'memory → prompt': 300, 'named → prompt': 300} org prompts per family | seeds=[0]

Claim tested: On Qwen3-32B, when the answer's statement is hidden from the last tokens, does a lookup in the prompt break while a recall does not, and in which 4-layer band must the statement stay visible?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 3% [2, 6] (n=300)   Baseline: org prompt unedited 100% (300/300)   Control: a statement like the one giving the answer, off the path 100% [99, 100] (n=300); a random span 100% [98, 100] (n=300)
Where the answer goes: 93% [89, 95] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: -
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 3% [1, 6] (n=300 / k=82 / t=9); animals 2% [0, 5] (Wilson [1, 7]; n=100 / k=31 / t=9); body 1% [0, 3] (Wilson [0, 5]; n=100 / k=15 / t=9); countries 7% [2, 13] (Wilson [3, 14]; n=100 / k=36 / t=9)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, band4.png, band4.svg, topics.png, topics.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.63, median 1.000; an unedited row moves by up to 0.42 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 41 of 75080 rows (only attention layers are blocked here: no DeltaNet output to rescale).
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 10/300).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): 
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory -; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: memory → prompt: last tokens NEEDED, question words NEEDED
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): memory → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 32-47, layers 40-43; memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 52-55; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 32-47, layers 48-63, layers 40-43, layers 52-55; named → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 32-47; named → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 52-55; named → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 32-47, layers 48-63, layers 52-55

Not interpretable / caveats: no control cell drops >= 20 points

## Per topic (entity-cluster intervals; the off-path control: Wilson)

| family | hidden from | layers | topic | n / k / t | answer org kept [95%, entity cluster] | Wilson | control | drop, control - cell [95%, entity cluster] |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 31 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| memory → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 7% [2, 13] | [3, 14] | 100% | +93 [+87, +98] |
| memory → prompt | the last tokens before the answer | layers 0-3 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-19 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-35 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-35 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-47 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-47 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 36-39 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 36-39 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 40-43 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 40-43 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 40-43 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 44-47 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 44-47 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 48-51 | animals | 100 / 31 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the last tokens before the answer | layers 48-51 | body | 100 / 15 / 9 | 94% [86, 99] | [88, 97] | 100% | +6 [+1, +14] |
| memory → prompt | the last tokens before the answer | layers 48-51 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the last tokens before the answer | layers 48-63 | animals | 100 / 31 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | layers 48-63 | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | layers 48-63 | countries | 100 / 36 / 9 | 7% [2, 13] | [3, 14] | 100% | +93 [+87, +98] |
| memory → prompt | the last tokens before the answer | layers 52-55 | animals | 100 / 31 / 9 | 25% [17, 34] | [18, 34] | 100% | +75 [+66, +83] |
| memory → prompt | the last tokens before the answer | layers 52-55 | body | 100 / 15 / 9 | 44% [29, 57] | [35, 54] | 100% | +56 [+43, +71] |
| memory → prompt | the last tokens before the answer | layers 52-55 | countries | 100 / 36 / 9 | 43% [33, 53] | [34, 53] | 100% | +57 [+47, +67] |
| memory → prompt | the last tokens before the answer | layers 56-59 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 56-59 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the last tokens before the answer | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 60-63 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 60-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 60-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 31 / 9 | 7% [2, 13] | [3, 14] | 100% | +93 [+87, +98] |
| memory → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 2% [0, 5] | [1, 7] | 98% | +96 [+92, +99] |
| memory → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 8% [3, 15] | [4, 15] | 100% | +92 [+85, +97] |
| memory → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 31 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 0-31 | animals | 100 / 31 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| memory → prompt | the question words and the last tokens | layers 0-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 0-31 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 99% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 31 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 32-35 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 32-35 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 32-47 | animals | 100 / 31 / 9 | 22% [13, 32] | [15, 31] | 100% | +78 [+68, +87] |
| memory → prompt | the question words and the last tokens | layers 32-47 | body | 100 / 15 / 9 | 64% [50, 77] | [54, 73] | 97% | +33 [+20, +47] |
| memory → prompt | the question words and the last tokens | layers 32-47 | countries | 100 / 36 / 9 | 15% [9, 23] | [9, 23] | 100% | +85 [+77, +91] |
| memory → prompt | the question words and the last tokens | layers 36-39 | animals | 100 / 31 / 9 | 84% [76, 92] | [76, 90] | 100% | +16 [+8, +24] |
| memory → prompt | the question words and the last tokens | layers 36-39 | body | 100 / 15 / 9 | 95% [90, 99] | [89, 98] | 100% | +5 [+1, +10] |
| memory → prompt | the question words and the last tokens | layers 36-39 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 40-43 | animals | 100 / 31 / 9 | 80% [72, 87] | [71, 87] | 100% | +20 [+13, +28] |
| memory → prompt | the question words and the last tokens | layers 40-43 | body | 100 / 15 / 9 | 87% [78, 94] | [79, 92] | 100% | +13 [+6, +22] |
| memory → prompt | the question words and the last tokens | layers 40-43 | countries | 100 / 36 / 9 | 57% [47, 67] | [47, 66] | 100% | +43 [+33, +53] |
| memory → prompt | the question words and the last tokens | layers 44-47 | animals | 100 / 31 / 9 | 89% [83, 95] | [81, 94] | 100% | +11 [+5, +17] |
| memory → prompt | the question words and the last tokens | layers 44-47 | body | 100 / 15 / 9 | 91% [83, 97] | [84, 95] | 100% | +9 [+3, +17] |
| memory → prompt | the question words and the last tokens | layers 44-47 | countries | 100 / 36 / 9 | 92% [87, 97] | [85, 96] | 100% | +8 [+3, +13] |
| memory → prompt | the question words and the last tokens | layers 48-51 | animals | 100 / 31 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| memory → prompt | the question words and the last tokens | layers 48-51 | body | 100 / 15 / 9 | 94% [86, 99] | [88, 97] | 100% | +6 [+1, +14] |
| memory → prompt | the question words and the last tokens | layers 48-51 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 48-63 | animals | 100 / 31 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the question words and the last tokens | layers 48-63 | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the question words and the last tokens | layers 48-63 | countries | 100 / 36 / 9 | 7% [2, 13] | [3, 14] | 100% | +93 [+87, +98] |
| memory → prompt | the question words and the last tokens | layers 52-55 | animals | 100 / 31 / 9 | 27% [18, 36] | [19, 36] | 100% | +73 [+64, +82] |
| memory → prompt | the question words and the last tokens | layers 52-55 | body | 100 / 15 / 9 | 44% [29, 57] | [35, 54] | 100% | +56 [+43, +71] |
| memory → prompt | the question words and the last tokens | layers 52-55 | countries | 100 / 36 / 9 | 43% [33, 53] | [34, 53] | 100% | +57 [+47, +67] |
| memory → prompt | the question words and the last tokens | layers 56-59 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 56-59 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 60-63 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 60-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 60-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | all 64 layers | animals | 100 / 31 / 9 | 24% [14, 34] | [17, 33] | 99% | +75 [+64, +85] |
| memory → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 63% [49, 76] | [53, 72] | 97% | +34 [+21, +48] |
| memory → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 9% [3, 16] | [5, 16] | 100% | +91 [+84, +97] |
| memory → prompt | the question words | layers 0-3 | animals | 100 / 31 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-31 | animals | 100 / 31 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| memory → prompt | the question words | layers 0-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-31 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 99% | +1 [+0, +3] |
| memory → prompt | the question words | layers 4-7 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 8-11 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 12-15 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-19 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-19 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 20-23 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | animals | 100 / 31 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-35 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-35 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-47 | animals | 100 / 31 / 9 | 22% [13, 32] | [15, 31] | 100% | +78 [+68, +87] |
| memory → prompt | the question words | layers 32-47 | body | 100 / 15 / 9 | 66% [52, 79] | [56, 75] | 97% | +31 [+19, +45] |
| memory → prompt | the question words | layers 32-47 | countries | 100 / 36 / 9 | 14% [7, 22] | [9, 22] | 100% | +86 [+78, +93] |
| memory → prompt | the question words | layers 36-39 | animals | 100 / 31 / 9 | 83% [75, 91] | [74, 89] | 100% | +17 [+9, +25] |
| memory → prompt | the question words | layers 36-39 | body | 100 / 15 / 9 | 95% [90, 99] | [89, 98] | 100% | +5 [+1, +10] |
| memory → prompt | the question words | layers 36-39 | countries | 100 / 36 / 9 | 97% [93, 100] | [92, 99] | 100% | +3 [+0, +7] |
| memory → prompt | the question words | layers 40-43 | animals | 100 / 31 / 9 | 80% [72, 87] | [71, 87] | 100% | +20 [+13, +28] |
| memory → prompt | the question words | layers 40-43 | body | 100 / 15 / 9 | 89% [81, 96] | [81, 94] | 100% | +11 [+4, +19] |
| memory → prompt | the question words | layers 40-43 | countries | 100 / 36 / 9 | 56% [46, 66] | [46, 65] | 100% | +44 [+34, +54] |
| memory → prompt | the question words | layers 44-47 | animals | 100 / 31 / 9 | 90% [84, 95] | [83, 94] | 100% | +10 [+5, +16] |
| memory → prompt | the question words | layers 44-47 | body | 100 / 15 / 9 | 93% [88, 97] | [86, 97] | 100% | +7 [+3, +12] |
| memory → prompt | the question words | layers 44-47 | countries | 100 / 36 / 9 | 92% [87, 97] | [85, 96] | 100% | +8 [+3, +13] |
| memory → prompt | the question words | layers 48-51 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-51 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 52-55 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 52-55 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 56-59 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 56-59 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 60-63 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 60-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 60-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | everything after it | all 64 layers | animals | 100 / 31 / 9 | 8% [3, 14] | [4, 15] | 99% | +91 [+85, +96] |
| memory → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 7% [3, 11] | [3, 14] | 97% | +90 [+85, +94] |
| memory → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 14% [7, 22] | [9, 22] | 100% | +86 [+78, +93] |
| named → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 31 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
| named → prompt | the last tokens before the answer | layers 0-3 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-35 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-35 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 36-39 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 36-39 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 40-43 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 40-43 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 40-43 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 44-47 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 44-47 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-51 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-51 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-63 | animals | 100 / 31 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | layers 48-63 | body | 100 / 15 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the last tokens before the answer | layers 48-63 | countries | 100 / 36 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
| named → prompt | the last tokens before the answer | layers 52-55 | animals | 100 / 31 / 9 | 32% [24, 41] | [24, 42] | 100% | +68 [+59, +76] |
| named → prompt | the last tokens before the answer | layers 52-55 | body | 100 / 15 / 9 | 43% [32, 55] | [34, 53] | 100% | +57 [+45, +68] |
| named → prompt | the last tokens before the answer | layers 52-55 | countries | 100 / 36 / 9 | 44% [35, 54] | [35, 54] | 100% | +56 [+46, +65] |
| named → prompt | the last tokens before the answer | layers 56-59 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 56-59 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 60-63 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 60-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 60-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 31 / 9 | 12% [6, 19] | [7, 20] | 100% | +88 [+81, +94] |
| named → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 17% [10, 24] | [11, 26] | 100% | +83 [+76, +90] |
| named → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 14% [7, 22] | [9, 22] | 100% | +86 [+78, +93] |
| named → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-31 | animals | 100 / 31 / 9 | 78% [69, 86] | [69, 85] | 100% | +22 [+14, +31] |
| named → prompt | the question words and the last tokens | layers 0-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-31 | countries | 100 / 36 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| named → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 32-35 | animals | 100 / 31 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 32-35 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 32-47 | animals | 100 / 31 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words and the last tokens | layers 32-47 | body | 100 / 15 / 9 | 27% [19, 35] | [19, 36] | 100% | +73 [+65, +81] |
| named → prompt | the question words and the last tokens | layers 32-47 | countries | 100 / 36 / 9 | 5% [1, 9] | [2, 11] | 100% | +95 [+91, +99] |
| named → prompt | the question words and the last tokens | layers 36-39 | animals | 100 / 31 / 9 | 90% [85, 95] | [83, 94] | 100% | +10 [+5, +15] |
| named → prompt | the question words and the last tokens | layers 36-39 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 40-43 | animals | 100 / 31 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| named → prompt | the question words and the last tokens | layers 40-43 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 40-43 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 44-47 | animals | 100 / 31 / 9 | 89% [84, 94] | [81, 94] | 100% | +11 [+6, +16] |
| named → prompt | the question words and the last tokens | layers 44-47 | body | 100 / 15 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| named → prompt | the question words and the last tokens | layers 44-47 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 48-51 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 48-51 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 48-63 | animals | 100 / 31 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words and the last tokens | layers 48-63 | body | 100 / 15 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words and the last tokens | layers 48-63 | countries | 100 / 36 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
| named → prompt | the question words and the last tokens | layers 52-55 | animals | 100 / 31 / 9 | 35% [26, 44] | [26, 45] | 100% | +65 [+56, +74] |
| named → prompt | the question words and the last tokens | layers 52-55 | body | 100 / 15 / 9 | 44% [33, 55] | [35, 54] | 100% | +56 [+45, +67] |
| named → prompt | the question words and the last tokens | layers 52-55 | countries | 100 / 36 / 9 | 46% [37, 56] | [37, 56] | 100% | +54 [+44, +63] |
| named → prompt | the question words and the last tokens | layers 56-59 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 56-59 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 60-63 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 60-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 60-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | all 64 layers | animals | 100 / 31 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 11% [6, 17] | [6, 19] | 100% | +89 [+83, +94] |
| named → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | layers 0-3 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-31 | animals | 100 / 31 / 9 | 79% [70, 87] | [70, 86] | 100% | +21 [+13, +30] |
| named → prompt | the question words | layers 0-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-31 | countries | 100 / 36 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| named → prompt | the question words | layers 4-7 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 12-15 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 12-15 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-35 | animals | 100 / 31 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words | layers 32-35 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-47 | animals | 100 / 31 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | layers 32-47 | body | 100 / 15 / 9 | 26% [18, 34] | [18, 35] | 100% | +74 [+66, +82] |
| named → prompt | the question words | layers 32-47 | countries | 100 / 36 / 9 | 6% [2, 11] | [3, 12] | 100% | +94 [+89, +98] |
| named → prompt | the question words | layers 36-39 | animals | 100 / 31 / 9 | 90% [85, 95] | [83, 94] | 100% | +10 [+5, +15] |
| named → prompt | the question words | layers 36-39 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 40-43 | animals | 100 / 31 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| named → prompt | the question words | layers 40-43 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 40-43 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 44-47 | animals | 100 / 31 / 9 | 90% [85, 95] | [83, 94] | 100% | +10 [+5, +15] |
| named → prompt | the question words | layers 44-47 | body | 100 / 15 / 9 | 95% [90, 99] | [89, 98] | 100% | +5 [+1, +10] |
| named → prompt | the question words | layers 44-47 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 48-51 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-51 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 52-55 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 52-55 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 56-59 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 56-59 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 60-63 | animals | 100 / 31 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 60-63 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 60-63 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | everything after it | all 64 layers | animals | 100 / 31 / 9 | 22% [14, 31] | [15, 31] | 100% | +78 [+69, +86] |
| named → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 34% [26, 42] | [25, 44] | 100% | +66 [+58, +74] |
| named → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 37% [27, 47] | [28, 47] | 100% | +63 [+53, +73] |

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|
| memory → prompt | 32% (NEEDED) | 3% (NEEDED) | - | - | - |
| named → prompt | 4% (NEEDED) | 3% (NEEDED) | - | - | - |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H-late-read | statement hidden from the tokens after the question in every layer: memory -> prompt still right upper bound <= 20%, memory -> memory lower bound >= 85%. Prior 0.65 | see summary.json | - |
| H-band | the band whose blocking alone breaks memory -> prompt most lies in the last half of the layers. Prior 0.6 | see summary.json | - |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>user
The mouse keeps its things in locker 5. The bee keeps its things in locker 1. The ant keeps its things in locker 2. The mosquito keeps its things in locker 7. The worm keeps its things in locker 9.
Which locker belongs to the animal known for wriggling underground? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

memory → prompt, org prompt animals-RL-e5f0-0031. What was done: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers (the statement: 'The worm keeps its things in locker 9.'). Unedited the model answers '9' (answer org '9'); with the statement hidden it answers '2', another answer that is in the prompt (the prompt's other answers: ['1', '2', '5', '7']). log p(answer org): -0.000 -> -15.007.

