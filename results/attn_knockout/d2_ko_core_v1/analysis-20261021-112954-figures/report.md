# attn_knockout / d2_ko_core_v1: analysis

EXP d2_ko_core_v1 @ 43f2f49 | model Qwen3.6-27B | n={'prompt → prompt': 60, 'prompt → memory': 60, 'memory → prompt': 60, 'memory → memory': 60} org prompts per family | seeds=[0]

Claim tested: When the question tokens and/or the final template positions cannot read the lookup statement ("The cow's locker is 5.") directly, does memory → prompt (recalled bridge -> in-prompt lookup) break while memory → memory (same scenes, recall from memory) survives; which destinations must see it, and in which 8-layer window, through attention or DeltaNet layers?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 7% [3, 16] (n=60)   Baseline: org prompt unedited 100% (60/60)   Control: a statement like the one giving the answer, off the path 100% [94, 100] (n=60); a random span 100% [94, 100] (n=60)
Where the answer goes: 67% [54, 77] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: 100% [94, 100] (n=60)
By layer kind: hidden in every attention layer only: 8% [4, 18] (n=60); hidden in every DeltaNet layer only: 100% [94, 100] (n=60)

Figures: all_layers.png, all_layers.svg, windows.png, windows.svg, norm_ratio.png, norm_ratio.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.97, median 0.997; an unedited row moves by up to 0.28 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 11 of 47880 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.970 of normal) and the controls (0.972), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Not here: with n < 35 (no cell this small) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 4/60).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): prompt → prompt: passed (the statement giving the answer NEEDED, the statement giving the bridge NEEDED); prompt → memory: passed (the statement giving the bridge NEEDED); memory → prompt: passed (the statement giving the answer NEEDED)
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory NOT NEEDED; holds = True
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = True; the reverse (question words relay it): False. Per family: prompt → prompt: last tokens NEEDED, question words NOT NEEDED; memory → prompt: last tokens NEEDED, question words NOT NEEDED
- The statement giving the bridge, by destination: prompt → prompt: the question words NEEDED, the last tokens before the answer NOT NEEDED, the question words and the last tokens NEEDED, everything after it NEEDED; prompt → memory: the question words NEEDED, the last tokens before the answer PARTIAL, the question words and the last tokens NEEDED, everything after it NEEDED
- Where in depth (layer sets that are NEEDED): prompt → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in every attention layer; prompt → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in layers 48-55, layers 48-55 (attention layers only); NEEDED in every attention layer; prompt → prompt, the statement giving the bridge hidden from the question words: NEEDED in every attention layer; prompt → prompt, the statement giving the bridge hidden from the question words and the last tokens: NEEDED in every attention layer; prompt → memory, the statement giving the bridge hidden from the question words: NEEDED in every attention layer; prompt → memory, the statement giving the bridge hidden from the question words and the last tokens: NEEDED in every attention layer; memory → prompt, the statement giving the answer hidden from the last tokens before the answer: NEEDED in every attention layer; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: NEEDED in every attention layer

Not interpretable / caveats: no control cell drops >= 20 points

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

| Q | Dan's prediction | Result (this run) | Verdict |
|---|---|---|---|
| Q2.1 memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every layer: % keeping answer org | 5% (from 95%) | 7% [3, 16] (n=60) | right (unedited 100%) |
| Q2.2 same, hidden only from the question words | 85% | 100% [94, 100] (n=60) | wrong: no drop at all |
| Q2.3 the 8-layer window that hurts memory → prompt most | 48-56 | lowest window, hidden from the last tokens: layers 48-55 98% [91, 100] (n=60); from both: layers 48-55 85% [74, 92] (n=60) | right window, but small: no single 8-layer window breaks memory → prompt (the read is redundant across layers; see the cumulative cuts) |
| Q2.4 memory → memory with the locker statement of bridge org hidden | 95% | lowest over the destinations 100% [94, 100] (n=60) | right (100%) |
| Q2.5 the statement giving the bridge hidden from the question words: which loses answer org more | prompt → prompt | prompt → prompt 58% [46, 70] (n=60), prompt → memory 18% [11, 30] (n=60) | wrong: prompt → memory loses more (guessing differs: prompt → prompt can pick one of the 3 lockers in the prompt) |
| Q2.6 which kind of layer runs the lookup | attention | memory → prompt, hidden from the last tokens in the 16 attention layers only: 8% [4, 18] (n=60); in the 48 DeltaNet layers only: 100% [94, 100] (n=60) | right |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H_answer_site | prompt → prompt and memory → prompt: (lookup, final, all) accuracy <= 40% (NEEDED) and (lookup, question, all) >= 90% (not NEEDED); memory → memory and prompt → memory: every lookup cell (question / final / both / after, mode value) >= 95%; the lookup->final window eff... | last tokens: memory → prompt 7%, prompt → prompt 3%; question words: memory → prompt 100%, prompt → prompt 100%; memory → memory/prompt → memory lowest 100%; windows below 32 NEEDED: none; 40-55 windows NEEDED/PARTIAL: ['win48-55'] | holds |
| H_relay | prompt → prompt and memory → prompt: (lookup, question, all) NEEDED and (lookup, final, all) not NEEDED. Prior 0.2 | relay holds = False | fails |
| H_both_routes | neither question nor final alone is NEEDED but both is (redundant routes). Prior 0.3 | last tokens alone: needed | fails |
| H_binding | prompt → prompt and prompt → memory: (binding, question, all) NEEDED; prompt → memory: (binding, final, all) >= 90%. Pointer variant (H_ptr, prior 0.35): prompt → prompt also needs (binding, final, all) (NEEDED or PARTIAL) while prompt → memory does not | question words: prompt → prompt 58%, prompt → memory 18% ({'prompt → prompt': 'needed', 'prompt → memory': 'needed'}); prompt → memory last tokens 87%; pointer variant: prompt → prompt last tokens 100% (not_needed) | partly (prompt → memory last tokens below 90%) |
| H_kind | no prior direction: the attention-only and DeltaNet-only halves of the needed windows are reported; the answer-site read is predicted to need the 2 attention layers of its window (>= 2/3 of the window's accuracy drop)... | memory → prompt: attention layers only 8%, DeltaNet only 100%; prompt → prompt: attention layers only 3%, DeltaNet only 100% | holds |
| positive_control | every path source at (after, all, mode absent): accuracy <= 30% (lockers: one of 3 in the prompt; prompt → memory binding: legs guessable ~45%, so <= 60% there) | {"prompt → prompt": true, "prompt → memory": true, "memory → prompt": true} | holds |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>user
Frank's pet is a turkey. Liam's pet is a spider. Laura's pet is a lion. The lion's locker is 5. The turkey's locker is 7. The spider's locker is 9.
Which locker belongs to the animal known for its roar? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

memory → prompt, org prompt RL-0318. What was done: memory → prompt, the statement giving the answer hidden from the question words and the last tokens in all 64 layers (the statement: "The lion's locker is 5."). Unedited the model answers '5' (answer org '5'); with the statement hidden it answers '9', another answer that is in the prompt (the prompt's other answers: ['7', '9']). log p(answer org): -0.004 -> -3.590.

