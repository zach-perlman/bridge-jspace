# attn_knockout / d2_alias_late_read: analysis

EXP d2_alias_late_read @ unknown | model Qwen3.6-27B | n={'memory → prompt, statements in English': 120, 'named → prompt, statements in English': 120, 'memory → memory, statements in English': 120, 'memory → prompt, statements in French/Spanish/German': 60, 'named → prompt, statements in French/Spanish/German': 60, 'memory → memory, statements in French/Spanish/German': 60, 'named → prompt, statements name the chemical symbol': 60, 'memory → memory, statements name the chemical symbol': 60} org prompts per family | seeds=[0]

Claim tested: When the statement giving the answer names the entity in another language ("Die Kuh hat den Spind 5.") or by its chemical symbol ("The O card is in locker 5."), while the question stays English, do the last tokens before the answer still read that statement themselves, in layers 48-63, through attention, as they do on the same scenes in English?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, statements in English, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 8% [4, 14] (n=120)   Baseline: org prompt unedited 100% (120/120)   Control: a statement like the one giving the answer, off the path 99% [95, 100] (n=120); a random span 100% [97, 100] (n=120)
Where the answer goes: 90% [83, 94] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
By layer kind: hidden in every attention layer only: 8% [4, 14] (n=120); hidden in every DeltaNet layer only: 100% [97, 100] (n=120)

Figures: all_layers.png, all_layers.svg, bands.png, bands.svg, norm_ratio.png, norm_ratio.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.40, median 0.992; an unedited row moves by up to 0.31 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 93 of 40920 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.968 of normal) and the controls (0.971), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL-same, source=lookup, dest=final, layers=all, mode=value (expect 9/120).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): memory → prompt, statements in English: passed (the statement giving the answer NEEDED); memory → prompt, statements in French/Spanish/German: passed (the statement giving the answer NEEDED); named → prompt, statements in English: passed (the statement giving the answer NEEDED); named → prompt, statements name the chemical symbol: passed (the statement giving the answer NEEDED); named → prompt, statements in French/Spanish/German: passed (the statement giving the answer NEEDED)
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt -, memory → memory -; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: 
- The statement giving the bridge, by destination: 
- Where in depth (layer sets that are NEEDED): memory → prompt, statements in English, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 32-47, layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; memory → prompt, statements in English, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 32-47, layers 32-47 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, statements in English, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, statements in English, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-31, layers 0-31 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; memory → prompt, statements in French/Spanish/German, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 32-47, layers 32-47 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; memory → prompt, statements in French/Spanish/German, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 32-47, layers 32-47 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, statements in French/Spanish/German, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, statements in French/Spanish/German, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 0-31, layers 0-31 (attention layers only), layers 32-47, layers 32-47 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, statements name the chemical symbol, the statement giving the answer hidden from the last tokens before the answer: NEEDED in layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer; named → prompt, statements name the chemical symbol, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 32-47, layers 32-47 (attention layers only), layers 48-63, layers 48-63 (attention layers only); NEEDED in every attention layer

Not interpretable / caveats: no control cell drops >= 20 points

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(Dan's D2 questions were asked about the animal scenes; see the late-attention table below for this item set)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | layers 0-31 | layers 32-47 | layers 48-63 | 48-63, attention only | 48-63, DeltaNet only | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|---|---|---|---|---|
| memory → prompt, statements in English | 87% (PARTIAL) | 8% (NEEDED) | 100% (NOT NEEDED) | 79% (NEEDED) | 11% (NEEDED) | 12% (NEEDED) | 100% (NOT NEEDED) | 8% (NEEDED) | 100% (NOT NEEDED) | no |
| memory → prompt, statements in French/Spanish/German | 85% (PARTIAL) | 5% (NEEDED) | 100% (NOT NEEDED) | 75% (NEEDED) | 45% (NEEDED) | 48% (NEEDED) | 100% (NOT NEEDED) | 2% (NEEDED) | 100% (NOT NEEDED) | no |
| memory → memory, statements in English | 99% (NOT NEEDED) | 98% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 98% (NOT NEEDED) | 100% (NOT NEEDED) | null (memory) |
| memory → memory, statements name the chemical symbol | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | null (memory) |
| memory → memory, statements in French/Spanish/German | 98% (NOT NEEDED) | 98% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 98% (NOT NEEDED) | 100% (NOT NEEDED) | null (memory) |
| named → prompt, statements in English | 1% (NEEDED) | 10% (NEEDED) | 100% (NOT NEEDED) | 100% (NOT NEEDED) | 8% (NEEDED) | 8% (NEEDED) | 100% (NOT NEEDED) | 10% (NEEDED) | 100% (NOT NEEDED) | yes |
| named → prompt, statements name the chemical symbol | 27% (NEEDED) | 0% (NEEDED) | 100% (NOT NEEDED) | 95% (PARTIAL) | 0% (NEEDED) | 0% (NEEDED) | 100% (NOT NEEDED) | 0% (NEEDED) | 100% (NOT NEEDED) | yes |
| named → prompt, statements in French/Spanish/German | 0% (NEEDED) | 5% (NEEDED) | 100% (NOT NEEDED) | 88% (PARTIAL) | 7% (NEEDED) | 7% (NEEDED) | 100% (NOT NEEDED) | 5% (NEEDED) | 100% (NOT NEEDED) | no |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H_late_read_english | memory → prompt and named → prompt with English statements: late attention read (all-layer <= 40% NEEDED, layers 48-63 NEEDED or PARTIAL, layers 0-31 and 32-47 >= 90%, every attention layer NEEDED, every DeltaNet laye... | memory → prompt, statements in English: all layers 8%, late band 11%, middle band 79%, early band 100%, every attention layer 8%, every DeltaNet layer 100%; named → prompt, statements in English: all layers 10%, late band 8%, middle band 100%, early band 100%, every attention layer 10%, every DeltaNet layer 100% | partly |
| H_late_read_other_surface | the same in the other surface form (French/Spanish/German statements for animals; the chemical symbol for elements). Prior 0.45 | memory → prompt, statements in French/Spanish/German: all layers 5%, late band 45%, middle band 75%, early band 100%, every attention layer 2%, every DeltaNet layer 100%; named → prompt, statements in French/Spanish/German: all layers 5%, late band 7%, middle band 88%, early band 100%, every attention layer 5%, every DeltaNet layer 100% | fails |
| H_surface_earlier | in the other surface form the statement is also needed in layers 32-47 (middle band NEEDED): a translation or alias step happens before the fetch. Prior 0.25 | memory → prompt, statements in French/Spanish/German: middle band NEEDED, memory → memory, statements in French/Spanish/German: middle band NOT NEEDED, named → prompt, statements in French/Spanish/German: middle band PARTIAL | fails |
| H_null | memory → memory in both forms: every cell >= 95%. Prior 0.85 | memory → memory, statements in English: lowest cell 96%, memory → memory, statements name the chemical symbol: lowest cell 95%, memory → memory, statements in French/Spanish/German: lowest cell 98% | holds |
| positive_control | every lookup family, both forms, with the statement hidden from everything after it and removed from the DeltaNet recurrence: <= 30% | {"memory → prompt, statements in English": true, "memory → prompt, statements in French/Spanish/German": true, "named → prompt, statements in English": true, "named → prompt, statements name the chemical symbol": true, "named → prompt, statements in French/Spanish/German": true} | holds |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>user
The helium card is in locker 4. The nitrogen card is in locker 3. The lithium card is in locker 5. The hydrogen card is in locker 7. The oxygen card is in locker 9.
Which locker holds the helium card? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

named → prompt, statements in English, org prompt elements-DL-e5f0-m0045. What was done: named → prompt, statements in English, the statement giving the answer hidden from the question words in all 64 layers (the statement: 'The helium card is in locker 4.'). Unedited the model answers '4' (answer org '4'); with the statement hidden it answers '1', another answer that is in the prompt (the prompt's other answers: ['3', '5', '7', '9']). log p(answer org): -0.002 -> -4.293.

