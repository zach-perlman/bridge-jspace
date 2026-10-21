# attn_knockout / d2_ko_tie_country_v1: analysis

EXP d2_ko_tie_country_v1 @ 43f2f49 | model Qwen3.6-27B | n={'prompt → prompt → memory': 25, 'prompt → memory → prompt': 25, 'countries: memory → memory': 25, 'countries: prompt → memory': 25} org prompts per family | seeds=[0]

Claim tested: In the three-step families, where the use of the bridge and the source of the answer come apart, and in the paper-style countries (B bound, R recalled), which statements must the question and final positions read directly, and when?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: prompt → memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 0% [0, 13] (n=25)   Baseline: org prompt unedited 100% (25/25)   Control: a statement like the one giving the answer, off the path 100% [87, 100] (n=25); a random span 100% [87, 100] (n=25)
Where the answer goes: 92% [75, 98] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Depth: hidden in layers 0-7 100%; hidden in layers 0-15 100%; hidden in layers 0-23 100%; hidden in layers 0-31 100%; hidden in layers 0-39 100%; hidden in layers 0-47 40%; hidden in layers 0-55 0%; hidden in layers 8-63 0%; hidden in layers 16-63 0%; hidden in layers 24-63 0%; hidden in layers 32-63 0%; hidden in layers 40-63 0%; hidden in layers 48-63 0%; hidden in layers 56-63 96%

Figures: all_layers.png, all_layers.svg, windows.png, windows.svg, cuts.png, cuts.svg, norm_ratio.png, norm_ratio.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.52, median 0.926; an unedited row moves by up to 0.22 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 35 of 19116 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.963 of normal) and the controls (0.966), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Yes here: with n < 35 (cells with n = [17, 19, 25]) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=BRL, source=lookup, dest=final, layers=all, mode=value (expect 0/25).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): prompt → prompt → memory: passed (the statement giving the answer NEEDED, the statement giving the bridge NEEDED); prompt → memory → prompt: passed (the statement giving the answer NEEDED, the statement giving the bridge NEEDED); countries: prompt → memory: passed (the statement giving the bridge NEEDED)
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt -, memory → memory -; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = False; the reverse (question words relay it): False. Per family: prompt → prompt → memory: last tokens NEEDED, question words NEEDED; prompt → memory → prompt: last tokens NEEDED, question words PARTIAL
- The statement giving the bridge, by destination: prompt → prompt → memory: the question words NEEDED, the last tokens before the answer PARTIAL, the question words and the last tokens NEEDED, everything after it NEEDED; prompt → memory → prompt: the question words NEEDED, the last tokens before the answer PARTIAL, the question words and the last tokens NEEDED, everything after it NEEDED
- Where in depth (layer sets that are NEEDED): prompt → prompt → memory, the statement giving the answer hidden from the question words: hiding it from layer L to the last breaks answer org for L up to 32; hiding it in layers 0 to L-1 breaks answer org from L = 48; prompt → prompt → memory, the statement giving the answer hidden from the last tokens before the answer: hiding it from layer L to the last breaks answer org for L up to 32; hiding it in layers 0 to L-1 breaks answer org from L = 40; NEEDED in layers 32-39, layers 32-39 (attention layers only); prompt → prompt → memory, the statement giving the answer hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 40; hiding it in layers 0 to L-1 breaks answer org from L = 40; NEEDED in layers 32-39, layers 32-39 (attention layers only); prompt → prompt → memory, the statement giving the bridge hidden from the question words: hiding it from layer L to the last breaks answer org for L up to 8; hiding it in layers 0 to L-1 breaks answer org from L = 32; prompt → prompt → memory, the statement giving the bridge hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 8; hiding it in layers 0 to L-1 breaks answer org from L = 24; prompt → memory → prompt, the statement giving the answer hidden from the last tokens before the answer: hiding it from layer L to the last breaks answer org for L up to 48; hiding it in layers 0 to L-1 breaks answer org from L = 48; NEEDED in layers 40-47, layers 40-47 (attention layers only), layers 48-55, layers 48-55 (attention layers only); prompt → memory → prompt, the statement giving the answer hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 48; hiding it in layers 0 to L-1 breaks answer org from L = 48; NEEDED in layers 40-47, layers 40-47 (attention layers only), layers 48-55, layers 48-55 (attention layers only); prompt → memory → prompt, the statement giving the bridge hidden from the question words: hiding it from layer L to the last breaks answer org for L up to 8; hiding it in layers 0 to L-1 breaks answer org from L = 32; prompt → memory → prompt, the statement giving the bridge hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 8; hiding it in layers 0 to L-1 breaks answer org from L = 32; countries: prompt → memory, the statement giving the bridge hidden from the question words: hiding it from layer L to the last breaks answer org for L up to 24; hiding it in layers 0 to L-1 breaks answer org from L = 24; countries: prompt → memory, the statement giving the bridge hidden from the last tokens before the answer: hiding it from layer L to the last breaks answer org for L up to 32; hiding it in layers 0 to L-1 breaks answer org from L = 56; countries: prompt → memory, the statement giving the bridge hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 32; hiding it in layers 0 to L-1 breaks answer org from L = 24

Not interpretable / caveats: countries: prompt → memory, control: the up to 3 tokens after the statement hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence: control breaks (53% [31, 74] (n=17)). n = [17, 19, 25] per cell: NOT NEEDED is unreachable by the rule (a 100% cell is PARTIAL)

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

(none of Dan's D2 questions is measured in this run)

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|
| prompt → prompt → memory | 60% (NEEDED) | 20% (NEEDED) | - | - | - |
| prompt → memory → prompt | 100% (PARTIAL) | 0% (NEEDED) | - | - | - |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H_BLR_early | prompt → prompt → memory (lookup, question, all) NEEDED and its lookup->final pre_min_needed <= 40 (read earlier than prompt → prompt's, to leave depth for the recall). Prior 0.5 | question words 60% (needed); last tokens NEEDED from prefix L = 40 | holds |
| H_BRL_like_BL | prompt → memory → prompt (lookup, final, all) NEEDED and (lookup, question, all) not NEEDED (the row read at the answer site). Prior 0.55 | last tokens 0% (needed); question words 100% (partial; n too small for NOT NEEDED) | holds |
| H_country_B | countries: prompt → memory (binding, question, all) NEEDED; (binding, final, all) >= 90%. Prior 0.6 | question words 12% (needed); last tokens 52% | partly (the last tokens read it too) |
| H_country_R_null | countries: memory → memory (binding: the statement only naming the bridge) >= 95% in every cell (the recall does not read it). Prior 0.8 | lowest cell over every destination and layer set 96% | holds |
| positive_control | path sources at (after, all, mode absent) <= 30% (countries: prompt → memory <= 40%: capitals of 3 countries guessable from the prompt's countries) | {"prompt → prompt → memory": true, "prompt → memory → prompt": true, "countries: prompt → memory": true} | holds |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>user
Tara's pet is a sheep. Laura's pet is a spider. Ivy's pet is a chicken. Animals with 6 legs use locker 9. Animals with 8 legs use locker 5. Animals with 4 legs use locker 3. Animals with 2 legs use locker 7.
Which locker does Tara's pet use? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

prompt → memory → prompt, org prompt BRL-0228. What was done: prompt → memory → prompt, the statement giving the answer hidden from the question words and the last tokens in all 64 layers and removed from the DeltaNet recurrence (the statement: 'Animals with 4 legs use locker 3.'). Unedited the model answers '3' (answer org '3'); with the statement hidden it answers '4', another answer that is in the prompt (the prompt's other answers: ['5', '7', '9']). log p(answer org): -0.327 -> -7.249.

