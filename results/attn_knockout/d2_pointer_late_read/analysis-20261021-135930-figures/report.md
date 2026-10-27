# attn_knockout / d2_pointer_late_read: analysis

EXP d2_pointer_late_read @ ca14894 | model Qwen3.6-27B | n={'memory → prompt': 175, 'named → prompt': 175, 'memory → memory': 175} org prompts per family | seeds=[0]

Claim tested: On pointer_v1's locker scenes (5 entities, animals and elements), when the last tokens before the answer cannot read the statement giving the answer, does memory → prompt still lose answer org, and does named → prompt (the entity named in the question) too; is the read in layers 48-63 and through attention layers, as on the animal scenes; and does memory → memory stay untouched?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 11% [8, 17] (n=175)   Baseline: org prompt unedited 100% (175/175)   Control: a statement like the one giving the answer, off the path 99% [97, 100] (n=175); a random span 100% [98, 100] (n=175)
Where the answer goes: 86% [80, 91] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: 96% [92, 98] (n=175)
By layer kind: hidden in every attention layer only: 11% [8, 17] (n=175); hidden in every DeltaNet layer only: 99% [97, 100] (n=175)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, norm_ratio.png, norm_ratio.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.58, median 0.996; an unedited row moves by up to 0.25 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 73 of 32550 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.967 of normal) and the controls (0.971), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 20/175).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): memory → prompt: passed (the statement giving the answer NEEDED); named → prompt: passed (the statement giving the answer NEEDED)
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory NOT NEEDED; holds = True
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: memory → prompt: last tokens NEEDED, question words PARTIAL
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 32-47, layers 32-47 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-31, layers 0-31 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer

Not interpretable / caveats: no control cell drops >= 20 points

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | layers 0-31 | layers 32-47 | layers 48-63 | 48-63, attention only | 48-63, DeltaNet only | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|---|---|---|---|---|
| memory → prompt | 88% (PARTIAL) | 11% (NEEDED) | 100% (NOT NEEDED) | 87% (PARTIAL) | 19% (NEEDED) | 19% (NEEDED) | 100% (NOT NEEDED) | 11% (NEEDED) | 99% (NOT NEEDED) | no |
| named → prompt | 1% (NEEDED) | 13% (NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 11% (NEEDED) | 11% (NEEDED) | 100% (NOT NEEDED) | 13% (NEEDED) | 100% (NOT NEEDED) | yes |
| memory → memory | 99% (NOT NEEDED) | 99% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 99% (NOT NEEDED) | 100% (NOT NEEDED) | null (memory) |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H_late_read | memory → prompt and named → prompt each: the statement giving the answer hidden from the last tokens in all 64 layers keeps answer org <= 40% (NEEDED); hidden only in layers 48-63 <= 60% (NEEDED or PARTIAL); only in 0... | memory → prompt: all layers 11%, late band 19%, middle band 87%, early band 100%, every attention layer 11%, every DeltaNet layer 99%; named → prompt: all layers 13%, late band 11%, middle band 100%, early band 100%, every attention layer 13%, every DeltaNet layer 100% | partly |
| H_named_earlier | named → prompt already needs the statement in layers 32-47 (middle band NEEDED): with the entity named, the lookup can start earlier. Prior 0.3 | named → prompt: middle band NOT NEEDED | fails |
| H_question_free | both lookup families keep >= 90% with the statement hidden from the question words only (animal scenes: 100%). Prior 0.75 | memory → prompt 88%, named → prompt 1% | fails |
| H_null | memory → memory: every cell >= 95% (animal scenes: 100%). Prior 0.9 | memory → memory: lowest cell 96% | holds |
| positive_control | every lookup family with the statement hidden from everything after it and removed from the DeltaNet recurrence: <= 30% (5 lockers in the prompt: guessing gives ~20%) | {"memory → prompt": true, "named → prompt": true} | holds |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>user
The nitrogen card is in locker 5. The carbon card is in locker 3. The hydrogen card is in locker 9. The lithium card is in locker 7. The oxygen card is in locker 2.
Which locker holds the oxygen card? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

named → prompt, org prompt elements-DL-e5f0-0093. What was done: named → prompt, the statement giving the answer hidden from the question words and the last tokens in all 64 layers (the statement: 'The oxygen card is in locker 2.'). Unedited the model answers '2' (answer org '2'); with the statement hidden it answers '1', another answer that is in the prompt (the prompt's other answers: ['3', '5', '7', '9']). log p(answer org): -0.001 -> -2.809.

