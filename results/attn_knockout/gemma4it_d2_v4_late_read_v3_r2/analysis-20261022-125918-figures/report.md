# attn_knockout / gemma4it_d2_v4_late_read_v3_r2: analysis

EXP gemma4it_d2_v4_late_read_v3_r2 @ 0c0c675 | model gemma-4-31B-it | n={'memory → prompt': 300, 'named → prompt': 300, 'memory → memory': 300} org prompts per family | seeds=[0]

Claim tested: On Gemma 4 31B-it, when the answer's statement is hidden from the last tokens, does a lookup in the prompt break while a recall does not, and in which 4-layer band must the statement stay visible?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 23% [18, 28] (n=300)   Baseline: org prompt unedited 100% (300/300)   Control: a statement like the one giving the answer, off the path 100% [99, 100] (n=300); a random span 100% [99, 100] (n=300)
Where the answer goes: 75% [70, 80] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: 97% [95, 99] (n=300)
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 23% [18, 27] (n=300 / k=84 / t=9); animals 31% [23, 39] (Wilson [23, 41]; n=100 / k=34 / t=9); body 15% [8, 23] (Wilson [9, 23]; n=100 / k=14 / t=9); countries 22% [14, 31] (Wilson [15, 31]; n=100 / k=36 / t=9)
Per topic: memory → memory, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 100% [99, 100] (n=300 / k=84 / t=9); animals 100% [100, 100] (Wilson [96, 100]; n=100 / k=34 / t=9); body 100% [100, 100] (Wilson [96, 100]; n=100 / k=14 / t=9); countries 99% [97, 100] (Wilson [95, 100]; n=100 / k=36 / t=9)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, band4.png, band4.svg, topics.png, topics.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.78, median 1.000; an unedited row moves by up to 0.39 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 18 of 108000 rows (only attention layers are blocked here: no DeltaNet output to rescale).
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 68/300).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): 
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory NOT NEEDED; holds = True
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: memory → prompt: last tokens NEEDED, question words NOT NEEDED
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 30-44; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 30-44; named → prompt, the statement giving the answer hidden from the question words: NEEDED in layers 0-29; named → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 30-44; named → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-29, layers 30-44

Not interpretable / caveats: no control cell drops >= 20 points

## Per topic (entity-cluster intervals; the off-path control: Wilson)

| family | hidden from | layers | topic | n / k / t | answer org kept [95%, entity cluster] | Wilson | control | drop, control - cell [95%, entity cluster] |
|---|---|---|---|---|---|---|---|---|
| memory → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 31% [23, 39] | [23, 41] | 100% | +69 [+61, +77] |
| memory → prompt | the last tokens before the answer | all 64 layers | body | 100 / 14 / 9 | 15% [8, 23] | [9, 23] | 100% | +85 [+77, +92] |
| memory → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 22% [14, 31] | [15, 31] | 100% | +78 [+69, +86] |
| memory → prompt | the last tokens before the answer | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-3 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-29 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-29 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-29 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 30-44 | animals | 100 / 34 / 9 | 70% [61, 79] | [60, 78] | 100% | +30 [+21, +39] |
| memory → prompt | the last tokens before the answer | layers 30-44 | body | 100 / 14 / 9 | 30% [21, 40] | [22, 40] | 100% | +70 [+60, +79] |
| memory → prompt | the last tokens before the answer | layers 30-44 | countries | 100 / 36 / 9 | 58% [49, 67] | [48, 67] | 100% | +42 [+33, +51] |
| memory → prompt | the last tokens before the answer | layers 32-35 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-35 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 36-39 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 36-39 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 40-43 | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the last tokens before the answer | layers 40-43 | body | 100 / 14 / 9 | 85% [75, 93] | [77, 91] | 100% | +15 [+7, +25] |
| memory → prompt | the last tokens before the answer | layers 40-43 | countries | 100 / 36 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| memory → prompt | the last tokens before the answer | layers 44-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 44-47 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 45-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 45-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 45-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 48-51 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 48-51 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 52-55 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 52-55 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 56-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 56-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 19% [12, 26] | [13, 28] | 100% | +81 [+74, +88] |
| memory → prompt | the question words and the last tokens | all 64 layers | body | 100 / 14 / 9 | 7% [3, 12] | [3, 14] | 100% | +93 [+88, +97] |
| memory → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 18% [11, 26] | [12, 27] | 100% | +82 [+74, +89] |
| memory → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 0-29 | animals | 100 / 34 / 9 | 71% [61, 80] | [61, 79] | 100% | +29 [+20, +39] |
| memory → prompt | the question words and the last tokens | layers 0-29 | body | 100 / 14 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| memory → prompt | the question words and the last tokens | layers 0-29 | countries | 100 / 36 / 9 | 83% [75, 91] | [74, 89] | 100% | +17 [+9, +25] |
| memory → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 14 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 30-44 | animals | 100 / 34 / 9 | 66% [57, 74] | [56, 75] | 100% | +34 [+26, +43] |
| memory → prompt | the question words and the last tokens | layers 30-44 | body | 100 / 14 / 9 | 25% [17, 33] | [18, 34] | 100% | +75 [+67, +83] |
| memory → prompt | the question words and the last tokens | layers 30-44 | countries | 100 / 36 / 9 | 52% [43, 61] | [42, 62] | 100% | +48 [+39, +57] |
| memory → prompt | the question words and the last tokens | layers 32-35 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 32-35 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 36-39 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 36-39 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 40-43 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 40-43 | body | 100 / 14 / 9 | 87% [79, 94] | [79, 92] | 100% | +13 [+6, +21] |
| memory → prompt | the question words and the last tokens | layers 40-43 | countries | 100 / 36 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| memory → prompt | the question words and the last tokens | layers 44-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 44-47 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 45-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 45-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 45-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 48-51 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 48-51 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 52-55 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 52-55 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 56-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 56-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | all 64 layers | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words | all 64 layers | body | 100 / 14 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-3 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-29 | animals | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words | layers 0-29 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 0-29 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 4-7 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 8-11 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 12-15 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-19 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 20-23 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 30-44 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 30-44 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 30-44 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-35 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-35 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 36-39 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 36-39 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 40-43 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 40-43 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 40-43 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 44-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 44-47 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 45-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 45-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 45-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-51 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-51 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 52-55 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 52-55 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 56-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 56-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | everything after it | all 64 layers | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | everything after it | all 64 layers | body | 100 / 14 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| memory → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 28% [20, 35] | [20, 37] | 100% | +72 [+65, +80] |
| named → prompt | the last tokens before the answer | all 64 layers | body | 100 / 14 / 9 | 13% [7, 19] | [8, 21] | 100% | +87 [+81, +93] |
| named → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 18% [11, 26] | [12, 27] | 100% | +82 [+74, +89] |
| named → prompt | the last tokens before the answer | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-29 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-29 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-29 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 30-44 | animals | 100 / 34 / 9 | 75% [66, 83] | [66, 82] | 100% | +25 [+17, +34] |
| named → prompt | the last tokens before the answer | layers 30-44 | body | 100 / 14 / 9 | 45% [39, 51] | [36, 55] | 100% | +55 [+49, +61] |
| named → prompt | the last tokens before the answer | layers 30-44 | countries | 100 / 36 / 9 | 60% [52, 68] | [50, 69] | 100% | +40 [+32, +48] |
| named → prompt | the last tokens before the answer | layers 32-35 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-35 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 36-39 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 36-39 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 40-43 | animals | 100 / 34 / 9 | 95% [90, 99] | [89, 98] | 100% | +5 [+1, +10] |
| named → prompt | the last tokens before the answer | layers 40-43 | body | 100 / 14 / 9 | 82% [75, 89] | [73, 88] | 100% | +18 [+11, +25] |
| named → prompt | the last tokens before the answer | layers 40-43 | countries | 100 / 36 / 9 | 95% [91, 99] | [89, 98] | 100% | +5 [+1, +9] |
| named → prompt | the last tokens before the answer | layers 44-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 44-47 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 45-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 45-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 45-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-51 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-51 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 52-55 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 52-55 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 56-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 56-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 27% [19, 35] | [19, 36] | 100% | +73 [+65, +81] |
| named → prompt | the question words and the last tokens | all 64 layers | body | 100 / 14 / 9 | 9% [3, 16] | [5, 16] | 100% | +91 [+84, +97] |
| named → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 22% [14, 31] | [15, 31] | 100% | +78 [+69, +86] |
| named → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 0-29 | animals | 100 / 34 / 9 | 23% [16, 30] | [16, 32] | 100% | +77 [+70, +84] |
| named → prompt | the question words and the last tokens | layers 0-29 | body | 100 / 14 / 9 | 48% [34, 63] | [38, 58] | 100% | +52 [+37, +66] |
| named → prompt | the question words and the last tokens | layers 0-29 | countries | 100 / 36 / 9 | 32% [24, 40] | [24, 42] | 100% | +68 [+60, +76] |
| named → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 30-44 | animals | 100 / 34 / 9 | 62% [52, 72] | [52, 71] | 100% | +38 [+28, +48] |
| named → prompt | the question words and the last tokens | layers 30-44 | body | 100 / 14 / 9 | 39% [31, 48] | [30, 49] | 100% | +61 [+52, +69] |
| named → prompt | the question words and the last tokens | layers 30-44 | countries | 100 / 36 / 9 | 48% [40, 57] | [38, 58] | 100% | +52 [+43, +60] |
| named → prompt | the question words and the last tokens | layers 32-35 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 32-35 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 36-39 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 36-39 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 40-43 | animals | 100 / 34 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | the question words and the last tokens | layers 40-43 | body | 100 / 14 / 9 | 86% [81, 91] | [78, 91] | 100% | +14 [+9, +19] |
| named → prompt | the question words and the last tokens | layers 40-43 | countries | 100 / 36 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| named → prompt | the question words and the last tokens | layers 44-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 44-47 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 45-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 45-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 45-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 48-51 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 48-51 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 52-55 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 52-55 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 56-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 56-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | all 64 layers | animals | 100 / 34 / 9 | 23% [16, 30] | [16, 32] | 100% | +77 [+70, +84] |
| named → prompt | the question words | all 64 layers | body | 100 / 14 / 9 | 50% [36, 65] | [40, 60] | 100% | +50 [+35, +64] |
| named → prompt | the question words | all 64 layers | countries | 100 / 36 / 9 | 47% [38, 57] | [38, 57] | 100% | +53 [+43, +62] |
| named → prompt | the question words | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-3 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 0-29 | animals | 100 / 34 / 9 | 23% [16, 30] | [16, 32] | 100% | +77 [+70, +84] |
| named → prompt | the question words | layers 0-29 | body | 100 / 14 / 9 | 64% [50, 77] | [54, 73] | 100% | +36 [+23, +50] |
| named → prompt | the question words | layers 0-29 | countries | 100 / 36 / 9 | 48% [38, 58] | [38, 58] | 100% | +52 [+42, +62] |
| named → prompt | the question words | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 4-7 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 12-15 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 28-31 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 30-44 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 30-44 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 30-44 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-35 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-35 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 36-39 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 36-39 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 40-43 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 40-43 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 40-43 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 44-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 44-47 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 45-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 45-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 45-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-51 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-51 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 52-55 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 52-55 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 56-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 56-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | everything after it | all 64 layers | animals | 100 / 34 / 9 | 13% [7, 21] | [8, 21] | 100% | +87 [+79, +93] |
| named → prompt | everything after it | all 64 layers | body | 100 / 14 / 9 | 7% [2, 13] | [3, 14] | 100% | +93 [+87, +98] |
| named → prompt | everything after it | all 64 layers | countries | 100 / 36 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| memory → memory | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | all 64 layers | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | all 64 layers | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-3 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-3 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-29 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 0-29 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 0-29 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 4-7 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 4-7 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 8-11 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 12-15 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 16-19 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 20-23 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 20-23 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-27 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 28-31 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 28-31 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 28-31 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the last tokens before the answer | layers 30-44 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the last tokens before the answer | layers 30-44 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 30-44 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-35 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-35 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 32-35 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the last tokens before the answer | layers 36-39 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 36-39 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 40-43 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 40-43 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 40-43 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 44-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 44-47 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 45-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 45-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 45-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-51 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-51 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 52-55 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 52-55 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 56-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 56-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the last tokens before the answer | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 93% [88, 97] | [86, 97] | 100% | +7 [+3, +12] |
| memory → memory | the question words and the last tokens | all 64 layers | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | all 64 layers | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-3 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-3 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 0-29 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 0-29 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 0-29 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 4-7 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 4-7 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [-3, +3] |
| memory → memory | the question words and the last tokens | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 8-11 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 12-15 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → memory | the question words and the last tokens | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 16-19 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → memory | the question words and the last tokens | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 20-23 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 20-23 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-27 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 28-31 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words and the last tokens | layers 28-31 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 28-31 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 30-44 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 30-44 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 30-44 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 32-35 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 32-35 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 32-35 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words and the last tokens | layers 36-39 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 36-39 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 40-43 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 40-43 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 40-43 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 44-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 44-47 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 45-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 45-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 45-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-51 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-51 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 52-55 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 52-55 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 56-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 56-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words and the last tokens | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | all 64 layers | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | all 64 layers | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | all 64 layers | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 0-3 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 0-3 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 0-29 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 0-29 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 0-29 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 4-7 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 4-7 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 99% | +0 [-3, +3] |
| memory → memory | the question words | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 8-11 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 8-11 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 12-15 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 12-15 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → memory | the question words | layers 16-19 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-19 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 16-19 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → memory | the question words | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 20-23 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 20-23 | countries | 100 / 36 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → memory | the question words | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-27 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 24-27 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 28-31 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 28-31 | countries | 100 / 36 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | the question words | layers 30-44 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 30-44 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 30-44 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-35 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-35 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 32-35 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 36-39 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 36-39 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 36-39 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 40-43 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 40-43 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 40-43 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 44-47 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 44-47 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 44-47 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 45-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 45-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 45-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-51 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-51 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 48-51 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 52-55 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 52-55 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 52-55 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 56-59 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 56-59 | body | 100 / 14 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | the question words | layers 56-59 | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → memory | everything after it | all 64 layers | animals | 100 / 34 / 9 | 93% [87, 98] | [86, 97] | 99% | +6 [+1, +13] |
| memory → memory | everything after it | all 64 layers | body | 100 / 14 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → memory | everything after it | all 64 layers | countries | 100 / 36 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|
| memory → prompt | 98% (NOT NEEDED) | 23% (NEEDED) | - | - | - |
| named → prompt | 40% (NEEDED) | 20% (NEEDED) | - | - | - |
| memory → memory | 99% (NOT NEEDED) | 100% (NOT NEEDED) | - | - | null (memory) |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H-late-read | statement hidden from the tokens after the question in every layer: memory -> prompt still right upper bound <= 20%, memory -> memory lower bound >= 85%. Prior 0.65 | see summary.json | - |
| H-band | the band whose blocking alone breaks memory -> prompt most lies in the last half of the layers. Prior 0.6 | see summary.json | - |

## Worked example (examples.json, group path_breaks)

```
<bos><|turn>user
Folder 6 holds the liver chart. Folder 4 holds the eye chart. Folder 7 holds the skull chart. Folder 5 holds the eyebrow chart. Folder 9 holds the ear chart.
What folder keeps the chart on the body part that makes bile? Answer with a single word and nothing else.<turn|>
<|turn>model
<|channel>thought
<channel|>Answer: 
```

memory → prompt, org prompt body-RL-e5f0-0045. What was done: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers (the statement: 'Folder 6 holds the liver chart.'). Unedited the model answers '6' (answer org '6'); with the statement hidden it answers '2', another answer that is in the prompt (the prompt's other answers: ['4', '5', '7', '9']). log p(answer org): 0.000 -> -4.520.

