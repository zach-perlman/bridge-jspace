# attn_knockout / d2_ko_sweep_v1: analysis

EXP d2_ko_sweep_v1 @ 43f2f49 | model Qwen3.6-27B | n={'prompt → prompt': 30, 'prompt → memory': 30, 'memory → prompt': 30, 'memory → memory': 30} org prompts per family | seeds=[0]

Claim tested: Over which layers must the lookup statement stay readable from the final positions (and the binding statement from the question tokens) for prompt → prompt and memory → prompt to keep their answer, compared with the copy's transit band (44-52) and the lens's write failure (32-52)?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 7% [2, 21] (n=30)   Baseline: org prompt unedited 100% (30/30)   Control: a statement like the one giving the answer, off the path 100% [89, 100] (n=30); a random span 100% [89, 100] (n=30)
Where the answer goes: 63% [46, 78] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: 100% [89, 100] (n=30)
Depth: hidden in layers 0-7 100%; hidden in layers 0-15 100%; hidden in layers 0-23 100%; hidden in layers 0-31 100%; hidden in layers 0-39 100%; hidden in layers 0-47 100%; hidden in layers 0-55 60%; hidden in layers 8-63 7%; hidden in layers 16-63 7%; hidden in layers 24-63 7%; hidden in layers 32-63 10%; hidden in layers 40-63 7%; hidden in layers 48-63 17%; hidden in layers 56-63 100%

Figures: all_layers.png, all_layers.svg, windows.png, windows.svg, cuts.png, cuts.svg, norm_ratio.png, norm_ratio.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.97, median 0.997; an unedited row moves by up to 0.28 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 3 of 15930 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.970 of normal) and the controls (0.971), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Yes here: with n < 35 (cells with n = [30]) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 2/30).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): prompt → prompt: passed (the statement giving the answer NEEDED, the statement giving the bridge NEEDED); prompt → memory: passed (the statement giving the bridge NEEDED); memory → prompt: passed (the statement giving the answer NEEDED)
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory PARTIAL; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = True; the reverse (question words relay it): False. Per family: prompt → prompt: last tokens NEEDED, question words PARTIAL; memory → prompt: last tokens NEEDED, question words PARTIAL
- The statement giving the bridge, by destination: prompt → prompt: the question words NEEDED, the last tokens before the answer PARTIAL, the question words and the last tokens NEEDED, everything after it NEEDED; prompt → memory: the question words NEEDED, the last tokens before the answer PARTIAL, the question words and the last tokens NEEDED, everything after it NEEDED
- Where in depth (layer sets that are NEEDED): prompt → prompt, the statement giving the answer hidden from the last tokens before the answer: hiding it from layer L to the last breaks answer org for L up to 48; hiding it in layers 0 to L-1 breaks answer org from L = 56; prompt → prompt, the statement giving the answer hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 48; hiding it in layers 0 to L-1 breaks answer org from L = 56; prompt → prompt, the statement giving the bridge hidden from the question words: hiding it from layer L to the last breaks answer org for L up to 24; hiding it in layers 0 to L-1 breaks answer org from L = 32; prompt → prompt, the statement giving the bridge hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 24; hiding it in layers 0 to L-1 breaks answer org from L = 32; prompt → memory, the statement giving the bridge hidden from the question words: hiding it from layer L to the last breaks answer org for L up to 16; hiding it in layers 0 to L-1 breaks answer org from L = 32; prompt → memory, the statement giving the bridge hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 32; hiding it in layers 0 to L-1 breaks answer org from L = 32; memory → prompt, the statement giving the answer hidden from the last tokens before the answer: hiding it from layer L to the last breaks answer org for L up to 48; hiding it in layers 0 to L-1 breaks answer org from L = 56; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 48; hiding it in layers 0 to L-1 breaks answer org from L = 56

Not interpretable / caveats: no control cell drops >= 20 points. n = [30] per cell: NOT NEEDED is unreachable by the rule (a 100% cell is PARTIAL)

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

| Q | Dan's prediction | Result (this run) | Verdict |
|---|---|---|---|
| Q2.1 memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every layer: % keeping answer org | 5% (from 95%) | 7% [2, 21] (n=30) | right (unedited 100%) |
| Q2.2 same, hidden only from the question words | 85% | 100% [89, 100] (n=30) | wrong: no drop at all |
| Q2.3 the 8-layer window that hurts memory → prompt most | 48-56 | lowest window, hidden from the last tokens: layers 48-55 100% [89, 100] (n=30); from both: layers 48-55 90% [74, 97] (n=30); hidden in a block of layers: layers 0-7 100%; layers 0-15 100%; layers 0-23 100%; layers 0-31 100%; layers 0-39 100%; layers 0-47 100%; layers 0-55 60%; layers 8-63 7%; layers 16-63 7%; layers 24-63 7%; layers 32-63 10%; layers 40-63 7%; layers 48-63 17%; layers 56-63 100% | right window, but small: no single 8-layer window breaks memory → prompt (the read is redundant across layers; see the cumulative cuts) |
| Q2.4 memory → memory with the locker statement of bridge org hidden | 95% | lowest over the destinations 100% [89, 100] (n=30) | right (100%) |
| Q2.5 the statement giving the bridge hidden from the question words: which loses answer org more | prompt → prompt | prompt → prompt 63% [46, 78] (n=30), prompt → memory 27% [14, 44] (n=30) | wrong: prompt → memory loses more (guessing differs: prompt → prompt can pick one of the 3 lockers in the prompt) |

## Late attention read, per family (the statement giving the answer hidden from the last tokens)

| family | question words, all layers | all layers | every attention layer | every DeltaNet layer | late attention read |
|---|---|---|---|---|---|
| prompt → prompt | 100% (PARTIAL) | 3% (NEEDED) | - | - | - |
| prompt → memory | 100% (PARTIAL) | 100% (PARTIAL) | - | - | - |
| memory → prompt | 100% (PARTIAL) | 7% (NEEDED) | - | - | - |
| memory → memory | 100% (PARTIAL) | 100% (PARTIAL) | - | - | null (memory) |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H_late_band | memory → prompt and prompt → prompt lookup->final: suf_max_needed >= 40 and pre_min_needed >= 48 (blocking [0, 40) does not matter, blocking [40, 64) does): the band lies in 40-56. Prior 0.5 | memory → prompt: blocking from L on breaks up to L = 48; blocking before L breaks from L = 56; prompt → prompt: blocking from L on breaks up to L = 48; blocking before L breaks from L = 56 | holds |
| H_early_band | memory → prompt lookup->final or ->question: pre_min_needed <= 32 and suf_max_needed <= 32. Prior 0.25 | memory → prompt: suffix up to 48, prefix from 56 | fails |
| H_spread | no single prefix or suffix cut below the full set is NEEDED (redundant reads across depth). Prior 0.25 | memory → prompt cumulative cuts NEEDED: ['pre56', 'suf08', 'suf16', 'suf24', 'suf32', 'suf40', 'suf48'] | fails |
| H_binding_band | prompt → prompt and prompt → memory binding->question: needed before layer 32 (pre_min_needed <= 32 or a stride-4 window below 32 NEEDED). prompt → prompt vs prompt → memory the same band (prior 0.6); prompt → prompt later than prompt → memory (the lookup dereferences a pointer late, prior 0.4) | binding -> question words, NEEDED from prefix L = {'prompt → prompt': 32, 'prompt → memory': 32} | holds |
| RR_null | memory → memory and prompt → memory: every lookup cell >= 95% at every layer set | lowest memory → memory/prompt → memory lookup cell 100% | holds |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>user
Liam's pet is a chicken. Henry's pet is a horse. Eva's pet is a bee. The bee's locker is 7. The chicken's locker is 1. The horse's locker is 5.
Which locker belongs to Henry's pet? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

prompt → prompt, org prompt BL-0037. What was done: prompt → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers (the statement: "The horse's locker is 5."). Unedited the model answers '5' (answer org '5'); with the statement hidden it answers '7', another answer that is in the prompt (the prompt's other answers: ['1', '7']). log p(answer org): -0.002 -> -2.655.

