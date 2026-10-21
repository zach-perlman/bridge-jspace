# attn_knockout / d2_smoke_27b: analysis

EXP d2_smoke_27b @ 43f2f49 | model Qwen3.6-27B | n={'prompt → prompt': 4, 'prompt → memory': 4, 'memory → prompt': 4, 'memory → memory': 4, 'prompt → prompt → memory': 4, 'prompt → memory → prompt': 4, 'countries: memory → memory': 4, 'countries: prompt → memory': 4} org prompts per family | seeds=[0]

Claim tested: Does the exact edge knock-out (bridge_jspace.knockout) run on Qwen3.6-27B for every condition type, with an exact no-op, a passing positive control, and a throughput that fits tonight's D2 budget?

Terms: org prompt = the unedited prompt; bridge org / answer org = its bridge and answer; 'hidden from' = those positions cannot read the statement directly (attention scores masked; DeltaNet layers: its values removed); accuracy = % of org prompts still giving answer org (100% unedited, by selection).

Headline: memory → prompt, the statement giving the answer hidden from the last tokens before the answer in all 64 layers: answer org kept in 0% [0, 49] (n=4)   Baseline: org prompt unedited 100% (4/4)   Control: a statement like the one giving the answer, off the path 100% [51, 100] (n=4); a random span 100% [51, 100] (n=4)
Where the answer goes: 25% [5, 70] of original answers become another statement's answer in the same prompt (another locker the prompt states or implies)
Contrast: memory → memory (the same org prompts up to the question; the answer comes from memory), the same statement hidden from the question words and the last tokens: 100% [51, 100] (n=4)

Figures: all_layers.png, all_layers.svg, norm_ratio.png, norm_ratio.svg

Three dumbest ways this could be wrong:
1) bf16 noise near ties decides cells. Checked: unedited p(answer org) min 0.64, median 0.990; an unedited row moves by up to 0.28 logits when other rows in its batch are knocked (check.json), so every knocked row is scored against the unedited row of its own batch.
2) Hiding any span this size breaks the model. Checked: the control spans (a same-kind statement off the path, a random span, the tokens after the statement) lose answer org in 16 of 3754 rows; the DeltaNet output at the blocked positions shrinks alike for the statement (0.966 of normal) and the controls (0.968), so the layer's output rescaling does not favour the statement.
3) The pre-registered rule mislabels cells at small n. Yes here: with n < 35 (cells with n = [3, 4]) a cell where every org prompt keeps answer org cannot reach the Wilson lower bound of 90% and is labelled PARTIAL instead of NOT NEEDED; read those by their accuracy. The positive control (the statement removed from every later position and from the DeltaNet recurrence) does break every family whose answer needs the statement (below).

For the human to verify: rows.jsonl, keep rows whose item's source='none' row has correct=true; count correct=true with family=RL, source=lookup, dest=final, layers=all, mode=value (expect 0/4).

Status: UNVERIFIED

## Pre-registered decision rule

> accuracy drop >= 20% and paired bootstrap 95% lower bound of acc(control) - acc(cell) >= 10% -> NEEDED; Wilson 95% lower bound of accuracy >= 90% -> NOT NEEDED; otherwise PARTIAL (manifest.json 'decision'; job spec decision_rule).

- Positive control (the statement the answer needs, hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence): prompt → prompt: FAILED (the statement giving the answer NEEDED, the statement giving the bridge PARTIAL); prompt → memory: passed (the statement giving the bridge NEEDED); memory → prompt: passed (the statement giving the answer NEEDED); prompt → prompt → memory: passed (the statement giving the answer NEEDED, the statement giving the bridge NEEDED); prompt → memory → prompt: passed (the statement giving the answer NEEDED, the statement giving the bridge NEEDED); countries: prompt → memory: passed (the statement giving the bridge NEEDED)
- Claim C1a (memory → prompt loses answer org while memory → memory keeps it, the statement giving the answer hidden from both destinations): memory → prompt NEEDED, memory → memory PARTIAL; holds = False
- Claim C1b (the last tokens before the answer read the statement giving the answer themselves; the question words do not need it): holds = True; the reverse (question words relay it): False. Per family: prompt → prompt: last tokens NEEDED, question words PARTIAL; memory → prompt: last tokens NEEDED, question words PARTIAL; prompt → prompt → memory: last tokens NEEDED, question words PARTIAL; prompt → memory → prompt: last tokens NEEDED, question words PARTIAL
- The statement giving the bridge, by destination: prompt → prompt: the question words PARTIAL, the last tokens before the answer PARTIAL, the question words and the last tokens PARTIAL, everything after it NEEDED; prompt → memory: the question words NEEDED, the last tokens before the answer PARTIAL, the question words and the last tokens NEEDED, everything after it NEEDED; prompt → prompt → memory: the question words NEEDED, the last tokens before the answer PARTIAL, the question words and the last tokens NEEDED, everything after it NEEDED; prompt → memory → prompt: the question words PARTIAL, the last tokens before the answer PARTIAL, the question words and the last tokens PARTIAL, everything after it NEEDED
- Where in depth (layer sets that are NEEDED): prompt → prompt, the statement giving the answer hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 48; hiding it in layers 0 to L-1 breaks answer org from L = 56; NEEDED in every attention layer; prompt → prompt, the statement giving the bridge hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 16; hiding it in layers 0 to L-1 breaks answer org from L = 48; prompt → memory, the statement giving the bridge hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 24; hiding it in layers 0 to L-1 breaks answer org from L = 32; NEEDED in every attention layer; memory → prompt, the statement giving the answer hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 48; hiding it in layers 0 to L-1 breaks answer org from L = 56; NEEDED in every attention layer; prompt → prompt → memory, the statement giving the answer hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 32; hiding it in layers 0 to L-1 breaks answer org from L = 48; NEEDED in every attention layer; prompt → prompt → memory, the statement giving the bridge hidden from the question words and the last tokens: hiding it in layers 0 to L-1 breaks answer org from L = 32; NEEDED in every attention layer; prompt → memory → prompt, the statement giving the answer hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 48; hiding it in layers 0 to L-1 breaks answer org from L = 48; NEEDED in layers 40-47, layers 40-47 (attention layers only), layers 48-55, layers 48-55 (attention layers only); NEEDED in every attention layer; countries: prompt → memory, the statement giving the bridge hidden from the question words and the last tokens: hiding it from layer L to the last breaks answer org for L up to 32; hiding it in layers 0 to L-1 breaks answer org from L = 32; NEEDED in every attention layer

Not interpretable / caveats: prompt → prompt → memory, control: a statement like the one giving the bridge, off the path hidden from the question words in all 64 layers: control breaks (75% [30, 95] (n=4)); prompt → prompt → memory, control: a statement like the one giving the bridge, off the path hidden from the question words and the last tokens in layers 24-31: control breaks (75% [30, 95] (n=4)); prompt → prompt → memory, control: a statement like the one giving the bridge, off the path hidden from the question words and the last tokens in layers 0-31: control breaks (75% [30, 95] (n=4)); prompt → prompt → memory, control: a statement like the one giving the bridge, off the path hidden from the question words and the last tokens in layers 0-47: control breaks (75% [30, 95] (n=4)); prompt → prompt → memory, control: a statement like the one giving the bridge, off the path hidden from the question words and the last tokens in layers 16-63: control breaks (75% [30, 95] (n=4)); prompt → prompt → memory, control: a statement like the one giving the bridge, off the path hidden from the question words and the last tokens in all 64 layers and removed from the DeltaNet recurrence: control breaks (75% [30, 95] (n=4)); prompt → memory → prompt, control: a statement like the one giving the answer, off the path hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence: control breaks (75% [30, 95] (n=4)); countries: memory → memory, control: a statement like the one giving the bridge, off the path hidden from everything after it in all 64 layers: control breaks (75% [30, 95] (n=4)); countries: memory → memory, control: a random span of the same length hidden from the question words and the last tokens in all 64 layers: control breaks (75% [30, 95] (n=4)); countries: memory → memory, control: a random span of the same length hidden from everything after it in all 64 layers: control breaks (75% [30, 95] (n=4)); countries: memory → memory, control: a random span of the same length hidden from the question words and the last tokens in layers 0-31: control breaks (75% [30, 95] (n=4)); countries: memory → memory, control: a random span of the same length hidden from the question words and the last tokens in layers 0-47: control breaks (75% [30, 95] (n=4)); countries: memory → memory, control: a random span of the same length hidden from the question words and the last tokens in layers 0-55: control breaks (75% [30, 95] (n=4)); countries: memory → memory, control: a random span of the same length hidden from the question words and the last tokens in every DeltaNet layer: control breaks (75% [30, 95] (n=4)); countries: prompt → memory, control: the up to 3 tokens after the statement hidden from everything after it in all 64 layers and removed from the DeltaNet recurrence: control breaks (33% [6, 79] (n=3)). n = [3, 4] per cell: NOT NEEDED is unreachable by the rule (a 100% cell is PARTIAL). n = 4 per family: a gate run, not interpreted

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D2)

| Q | Dan's prediction | Result (this run) | Verdict |
|---|---|---|---|
| Q2.1 memory → prompt, the statement giving the answer hidden from the last tokens before the answer in every layer: % keeping answer org | 5% (from 95%) | 0% [0, 49] (n=4) | right (unedited 100%) |
| Q2.2 same, hidden only from the question words | 85% | 100% [51, 100] (n=4) | close |
| Q2.4 memory → memory with the locker statement of bridge org hidden | 95% | lowest over the destinations 100% [51, 100] (n=4) | right (100%) |
| Q2.5 the statement giving the bridge hidden from the question words: which loses answer org more | prompt → prompt | prompt → prompt 75% [30, 95] (n=4), prompt → memory 25% [5, 70] (n=4) | wrong: prompt → memory loses more (guessing differs: prompt → prompt can pick one of the 3 lockers in the prompt) |

## The agent's priors (job spec hypotheses), checked

Predictions are quoted from the job spec (written before the run). Their shorthand: lookup = the statement giving the answer, binding = the statement giving the bridge; question = the question words, final = the last tokens before the answer; (statement, destination, all) = hidden in all 64 layers; win A-B = layers A-B only; suf L = layers L-63; pre L = layers 0 to L-1; NEEDED / NOT NEEDED / PARTIAL as in the rule above.

| hypothesis | prediction (job spec) | result | verdict |
|---|---|---|---|
| H-noop | check.json noop_empty_source_max_abs == 0 (an empty source span leaves the answer read bit-for-bit unchanged; 0.8B smoke: 0.0) | noop_empty_source_max_abs = 0.0 | holds |
| H-posctl | check.json posctl_last_reads_nothing_max_abs and posctl_context_erased_absent_max_abs < 0.1 logits with the same top token (0.8B smoke: 0.0 and 0.0, vs 2.4 unhooked) | 0.0 and 0.0 logits (unhooked 12.8) | holds |
| H-throughput | timing.json rows_per_second >= 15 (assumed 20; 0.8B smoke 106 rows/s, overhead of a batch knocked at every layer 1.8x on the 0.8B, expected <= 1.3x on the 27B where the DeltaNet mixer is ~27% of a layer) | 34.45 rows/s | holds |

## Worked example (examples.json, group path_breaks)

```
<|im_start|>user
Eric's pet is a goose. Hugo's pet is a lion. Iris's pet is a sheep. Animals with 6 legs use locker 7. Animals with 8 legs use locker 3. Animals with 2 legs use locker 5. Animals with 4 legs use locker 1.
Which locker does Eric's pet use? Answer with a single word and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

prompt → memory → prompt, org prompt BRL-0080. What was done: prompt → memory → prompt, the statement giving the answer hidden from the question words and the last tokens in all 64 layers and removed from the DeltaNet recurrence (the statement: 'Animals with 2 legs use locker 5.'). Unedited the model answers '5' (answer org '5'); with the statement hidden it answers '1', another answer that is in the prompt (the prompt's other answers: ['1', '3', '7']). log p(answer org): -0.056 -> -8.164.

