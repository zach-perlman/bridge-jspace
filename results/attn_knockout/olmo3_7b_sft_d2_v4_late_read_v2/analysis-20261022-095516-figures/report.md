# attn_knockout / olmo3_7b_sft_d2_v4_late_read_v2: analysis

EXP olmo3_7b_sft_d2_v4_late_read_v2 @ 9ac2657 | model Olmo-3-7B-Instruct-SFT | n={'named → prompt': 300, 'memory → prompt': 100} org prompts per family | seeds=[0]

Claim tested: D5b: olmo3_7b_instruct_d2_v4_late_read_v3's grid on the SFT checkpoint

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 1% [0, 5] (n=100)   Baseline: org prompt unedited 100% (100/100)   Control: a statement like the one giving the answer, off the path 100% [96, 100] (n=100); a random span 99% [95, 100] (n=100)
Where the answer goes: 99% [95, 100] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: -
Per topic: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: pooled 1% [0, 3] (n=100 / k=34 / t=9); countries 1% [0, 3] (Wilson [0, 5]; n=100 / k=34 / t=9)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, band4.png, band4.svg, topics.png, topics.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.45, median 0.998; an unedited row moves by up to 0.16 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 32 of 30896 rows (only attention layers are blocked here: no DeltaNet output to rescale).
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 1/100).

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
| memory → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| memory → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 0-15 | countries | 100 / 34 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| memory → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 34 / 9 | 95% [91, 99] | [89, 98] | 100% | +5 [+1, +9] |
| memory → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 34 / 9 | 94% [90, 98] | [88, 97] | 100% | +6 [+2, +10] |
| memory → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 34 / 9 | 16% [9, 24] | [10, 24] | 100% | +84 [+76, +91] |
| memory → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 34 / 9 | 87% [80, 93] | [79, 92] | 100% | +13 [+7, +20] |
| memory → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 34 / 9 | 3% [0, 7] | [1, 8] | 99% | +96 [+90, +100] |
| memory → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 34 / 9 | 20% [12, 27] | [13, 29] | 99% | +79 [+72, +86] |
| memory → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 34 / 9 | 64% [56, 72] | [54, 73] | 99% | +35 [+27, +43] |
| memory → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 34 / 9 | 76% [68, 84] | [67, 83] | 100% | +24 [+16, +32] |
| memory → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 34 / 9 | 93% [88, 97] | [86, 97] | 100% | +7 [+3, +12] |
| memory → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 34 / 9 | 16% [9, 24] | [10, 24] | 100% | +84 [+76, +91] |
| memory → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 34 / 9 | 87% [80, 93] | [79, 92] | 100% | +13 [+7, +20] |
| memory → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| memory → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | all 64 layers | countries | 100 / 34 / 9 | 38% [29, 47] | [29, 48] | 98% | +60 [+50, +70] |
| memory → prompt | the question words | layers 0-3 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| memory → prompt | the question words | layers 0-15 | countries | 100 / 34 / 9 | 38% [29, 47] | [29, 48] | 98% | +60 [+50, +70] |
| memory → prompt | the question words | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 99% | -1 [-3, +0] |
| memory → prompt | the question words | layers 8-11 | countries | 100 / 34 / 9 | 66% [57, 75] | [56, 75] | 99% | +33 [+24, +42] |
| memory → prompt | the question words | layers 12-15 | countries | 100 / 34 / 9 | 88% [83, 93] | [80, 93] | 100% | +12 [+7, +17] |
| memory → prompt | the question words | layers 16-19 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 16-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 20-23 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 24-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | the question words | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| memory → prompt | everything after it | all 64 layers | countries | 100 / 34 / 9 | 6% [2, 11] | [3, 12] | 99% | +93 [+88, +97] |
| named → prompt | the last tokens before the answer | all 64 layers | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | body | 100 / 15 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the last tokens before the answer | all 64 layers | countries | 100 / 34 / 9 | 10% [4, 17] | [6, 17] | 100% | +90 [+83, +96] |
| named → prompt | the last tokens before the answer | layers 0-3 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-3 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 0-15 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 0-15 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 8-11 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 12-15 | body | 100 / 15 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 12-15 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 16-19 | animals | 100 / 34 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| named → prompt | the last tokens before the answer | layers 16-19 | body | 100 / 15 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| named → prompt | the last tokens before the answer | layers 16-19 | countries | 100 / 34 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | the last tokens before the answer | layers 16-23 | animals | 100 / 34 / 9 | 11% [5, 17] | [6, 19] | 100% | +89 [+83, +95] |
| named → prompt | the last tokens before the answer | layers 16-23 | body | 100 / 15 / 9 | 34% [22, 45] | [25, 44] | 100% | +66 [+55, +78] |
| named → prompt | the last tokens before the answer | layers 16-23 | countries | 100 / 34 / 9 | 47% [39, 55] | [38, 57] | 100% | +53 [+45, +61] |
| named → prompt | the last tokens before the answer | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 20-23 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the last tokens before the answer | layers 20-23 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the last tokens before the answer | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 24-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the last tokens before the answer | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | all 64 layers | animals | 100 / 34 / 9 | 8% [3, 14] | [4, 15] | 100% | +92 [+86, +97] |
| named → prompt | the question words and the last tokens | all 64 layers | body | 100 / 15 / 9 | 16% [10, 23] | [10, 24] | 100% | +84 [+77, +90] |
| named → prompt | the question words and the last tokens | all 64 layers | countries | 100 / 34 / 9 | 9% [4, 15] | [5, 16] | 100% | +91 [+85, +96] |
| named → prompt | the question words and the last tokens | layers 0-3 | animals | 100 / 34 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| named → prompt | the question words and the last tokens | layers 0-3 | body | 100 / 15 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | the question words and the last tokens | layers 0-3 | countries | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 0-15 | animals | 100 / 34 / 9 | 1% [0, 3] | [0, 5] | 100% | +99 [+97, +100] |
| named → prompt | the question words and the last tokens | layers 0-15 | body | 100 / 15 / 9 | 16% [8, 25] | [10, 24] | 100% | +84 [+75, +92] |
| named → prompt | the question words and the last tokens | layers 0-15 | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words and the last tokens | layers 4-7 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 4-7 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 8-11 | animals | 100 / 34 / 9 | 85% [76, 93] | [77, 91] | 100% | +15 [+7, +24] |
| named → prompt | the question words and the last tokens | layers 8-11 | body | 100 / 15 / 9 | 82% [71, 92] | [73, 88] | 100% | +18 [+8, +29] |
| named → prompt | the question words and the last tokens | layers 8-11 | countries | 100 / 34 / 9 | 92% [86, 97] | [85, 96] | 100% | +8 [+3, +14] |
| named → prompt | the question words and the last tokens | layers 12-15 | animals | 100 / 34 / 9 | 79% [71, 87] | [70, 86] | 100% | +21 [+13, +29] |
| named → prompt | the question words and the last tokens | layers 12-15 | body | 100 / 15 / 9 | 79% [69, 88] | [70, 86] | 100% | +21 [+12, +31] |
| named → prompt | the question words and the last tokens | layers 12-15 | countries | 100 / 34 / 9 | 86% [78, 93] | [78, 91] | 100% | +14 [+7, +22] |
| named → prompt | the question words and the last tokens | layers 16-19 | animals | 100 / 34 / 9 | 97% [94, 100] | [92, 99] | 100% | +3 [+0, +6] |
| named → prompt | the question words and the last tokens | layers 16-19 | body | 100 / 15 / 9 | 95% [90, 99] | [89, 98] | 100% | +5 [+1, +10] |
| named → prompt | the question words and the last tokens | layers 16-19 | countries | 100 / 34 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | the question words and the last tokens | layers 16-23 | animals | 100 / 34 / 9 | 12% [6, 18] | [7, 20] | 100% | +88 [+82, +94] |
| named → prompt | the question words and the last tokens | layers 16-23 | body | 100 / 15 / 9 | 33% [21, 44] | [25, 43] | 100% | +67 [+56, +79] |
| named → prompt | the question words and the last tokens | layers 16-23 | countries | 100 / 34 / 9 | 42% [34, 50] | [33, 52] | 100% | +58 [+50, +66] |
| named → prompt | the question words and the last tokens | layers 20-23 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 20-23 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words and the last tokens | layers 20-23 | countries | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words and the last tokens | layers 24-27 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-27 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 24-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | animals | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | body | 100 / 15 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words and the last tokens | layers 28-31 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | all 64 layers | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | all 64 layers | body | 100 / 15 / 9 | 24% [15, 34] | [17, 33] | 100% | +76 [+66, +85] |
| named → prompt | the question words | all 64 layers | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | layers 0-3 | animals | 100 / 34 / 9 | 96% [92, 99] | [90, 98] | 100% | +4 [+1, +8] |
| named → prompt | the question words | layers 0-3 | body | 100 / 15 / 9 | 97% [92, 100] | [92, 99] | 100% | +3 [+0, +8] |
| named → prompt | the question words | layers 0-3 | countries | 100 / 34 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words | layers 0-15 | animals | 100 / 34 / 9 | 2% [0, 5] | [1, 7] | 100% | +98 [+95, +100] |
| named → prompt | the question words | layers 0-15 | body | 100 / 15 / 9 | 23% [14, 33] | [16, 32] | 100% | +77 [+67, +86] |
| named → prompt | the question words | layers 0-15 | countries | 100 / 34 / 9 | 0% [0, 0] | [0, 4] | 100% | +100 [+100, +100] |
| named → prompt | the question words | layers 4-7 | animals | 100 / 34 / 9 | 99% [97, 100] | [95, 100] | 100% | +1 [+0, +3] |
| named → prompt | the question words | layers 4-7 | body | 100 / 15 / 9 | 98% [95, 100] | [93, 99] | 100% | +2 [+0, +5] |
| named → prompt | the question words | layers 4-7 | countries | 100 / 34 / 9 | 100% [100, 100] | [96, 100] | 100% | +0 [+0, +0] |
| named → prompt | the question words | layers 8-11 | animals | 100 / 34 / 9 | 85% [76, 93] | [77, 91] | 100% | +15 [+7, +24] |
| named → prompt | the question words | layers 8-11 | body | 100 / 15 / 9 | 83% [73, 92] | [74, 89] | 100% | +17 [+8, +27] |
| named → prompt | the question words | layers 8-11 | countries | 100 / 34 / 9 | 93% [87, 98] | [86, 97] | 100% | +7 [+2, +13] |
| named → prompt | the question words | layers 12-15 | animals | 100 / 34 / 9 | 94% [89, 98] | [88, 97] | 100% | +6 [+2, +11] |
| named → prompt | the question words | layers 12-15 | body | 100 / 15 / 9 | 96% [91, 100] | [90, 98] | 100% | +4 [+0, +9] |
| named → prompt | the question words | layers 12-15 | countries | 100 / 34 / 9 | 92% [87, 97] | [85, 96] | 100% | +8 [+3, +13] |
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
| named → prompt | everything after it | all 64 layers | animals | 100 / 34 / 9 | 14% [7, 22] | [9, 22] | 100% | +86 [+78, +93] |
| named → prompt | everything after it | all 64 layers | body | 100 / 15 / 9 | 25% [17, 34] | [18, 34] | 100% | +75 [+66, +83] |
| named → prompt | everything after it | all 64 layers | countries | 100 / 34 / 9 | 15% [9, 22] | [9, 23] | 100% | +85 [+78, +91] |

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|
| memory → prompt | 38% (NEEDED) | 1% (NEEDED) | - | - | - |
| named → prompt | 9% (NEEDED) | 4% (NEEDED) | - | - | - |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|

