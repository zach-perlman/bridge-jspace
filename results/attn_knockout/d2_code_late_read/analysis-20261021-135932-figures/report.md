# attn_knockout / d2_code_late_read: analysis

EXP d2_code_late_read @ ca14894 | model Qwen3.6-27B | n={'code: named → prompt': 120, 'code: list position → prompt': 120, 'code: 2-variable chain → prompt': 120, 'code: 3-variable chain → prompt': 120, 'code: memory → prompt': 60} org prompts per family | seeds=[0]

Claim tested: In code_pointer_v1's programs (lockers = {"cow": 5, ...} then a print whose key is named, read from a list position, passed through a 2- or 3-variable chain, or recalled from a cue), when the last tokens before the answer cannot read the dict entry giving the answer, is answer org lost; is the read in layers 48-63 and through attention; and does the recalled-fact family (memory → memory) stay untouched?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: code: named → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 47% [38, 56] (n=120)   Baseline: org prompt unedited 100% (120/120)   Control: a statement like the one giving the answer, off the path 100% [97, 100] (n=120); a random span 100% [97, 100] (n=120)
Where the answer goes: 47% [38, 56] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
By layer kind: hidden in every attention layer only: 48% [39, 56] (n=120); hidden in every DeltaNet layer only: 100% [97, 100] (n=120)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, norm_ratio.png, norm_ratio.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.50, median 0.996; an unedited row moves by up to 0.33 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 141 of 33480 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.988 of normal) and the controls (0.989), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=DK, source=lookup, dest=final, layers=all, mode=value (expect 56/120).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): code: named → prompt: passed (the statement giving the answer NEEDED); code: list position → prompt: passed (the statement giving the answer NEEDED); code: 2-variable chain → prompt: passed (the statement giving the answer NEEDED); code: 3-variable chain → prompt: passed (the statement giving the answer NEEDED); code: memory → prompt: passed (the statement giving the answer NEEDED)
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt -, memory → memory -; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: 
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): code: named → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; code: named → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-31, layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; code: list position → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; code: list position → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; code: 2-variable chain → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; code: 2-variable chain → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; code: 3-variable chain → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; code: 3-variable chain → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; code: memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 32-47, layers 32-47 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; code: memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 32-47, layers 32-47 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer

Not interpretable / caveats: code: named → prompt, control: the up to 3 tokens after the statement hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence: control breaks (79% [71, 85] (n=120)); code: 2-variable chain → prompt, control: the up to 3 tokens after the statement hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence: control breaks (71% [62, 78] (n=120)); code: 3-variable chain → prompt, control: the up to 3 tokens after the statement hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence: control breaks (69% [60, 77] (n=120))

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | layers 0-31 | layers 32-47 | layers 48-63 | 48-63, attention only | 48-63, DeltaNet only | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|---|---|---|---|---|
| code: named → prompt | 6% (NEEDED) | 47% (NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 50% (NEEDED) | 50% (NEEDED) | 100% (NOT NEEDED) | 48% (NEEDED) | 100% (NOT NEEDED) | yes |
| code: list position → prompt | 100% (NOT NEEDED) | 36% (NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 35% (NEEDED) | 36% (NEEDED) | 100% (NOT NEEDED) | 34% (NEEDED) | 100% (NOT NEEDED) | yes |
| code: 2-variable chain → prompt | 100% (NOT NEEDED) | 42% (NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 36% (NEEDED) | 35% (NEEDED) | 100% (NOT NEEDED) | 42% (NEEDED) | 100% (NOT NEEDED) | yes |
| code: 3-variable chain → prompt | 100% (NOT NEEDED) | 32% (NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 34% (NEEDED) | 34% (NEEDED) | 100% (NOT NEEDED) | 32% (NEEDED) | 100% (NOT NEEDED) | yes |
| code: memory → prompt | 90% (PARTIAL) | 27% (NEEDED) | 100% (NOT NEEDED) | 78% (NEEDED) | 37% (NEEDED) | 35% (NEEDED) | 100% (NOT NEEDED) | 25% (NEEDED) | 100% (NOT NEEDED) | no |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H_late_read | every lookup family (named key, list position, 2-variable chain, 3-variable chain, recalled key): the entry hidden from the last tokens in all 64 layers <= 40% (NEEDED); only in layers 48-63 <= 60% (NEEDED or PARTIAL)... | code: named → prompt: all layers 47%, late band 50%, middle band 100%, early band 100%, every attention layer 48%, every DeltaNet layer 100%; code: list position → prompt: all layers 36%, late band 35%, middle band 100%, early band 100%, every attention layer 34%, every DeltaNet layer 100%; code: 2-variable chain → prompt: all layers 42%, late band 36%, middle band 100%, early band 100%, every attention layer 42%, every DeltaNet layer 100%; code: 3-variable chain → prompt: all layers 32%, late band 34%, middle band 100%, early band 100%, every attention layer 32%, every DeltaNet layer 100%; code: memory → prompt: all layers 27%, late band 37%, middle band 78%, early band 100%, every attention layer 25%, every DeltaNet layer 100% | partly |
| H_question_free | every lookup family keeps >= 90% with the entry hidden from the question words only (here the question words include the print line, e.g. print(lockers[names[0]])). Prior 0.45 | code: named → prompt 6%, code: list position → prompt 100%, code: 2-variable chain → prompt 100%, code: 3-variable chain → prompt 100%, code: memory → prompt 90% | fails |
| H_chain_earlier | the 3-variable chain needs the entry in layers 32-47 already (middle band NEEDED). Prior 0.3 | code: 3-variable chain → prompt: middle band NOT NEEDED | fails |
| H_null | memory → memory (code): every cell >= 95%. Prior 0.85 |  | fails |
| positive_control | every lookup family with the entry hidden from everything after it and removed from the DeltaNet recurrence: <= 30% (5 entries) | {"code: named → prompt": true, "code: list position → prompt": true, "code: 2-variable chain → prompt": true, "code: 3-variable chain → prompt": true, "code: memory → prompt": true} | holds |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>user
```python
lockers = {"July": 0, "June": 4, "April": 9, "September": 8, "January": 3}
names = ["January", "September", "June", "July", "April"]
print(lockers[names[2]])
```
What does this Python code print? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

code: list position → prompt, org prompt months-IX-e5f0-0017. What was done: code: list position → prompt, the statement giving the answer hidden from everything after it in all 64 layers (the statement: '"June": 4'). Unedited the model answers '4' (answer org '4'); with the statement hidden it answers '0', another answer that is in the prompt (the prompt's other answers: ['0', '3', '8', '9']). log p(answer org): -0.009 -> -3.097.

