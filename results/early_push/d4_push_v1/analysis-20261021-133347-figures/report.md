# D4 main: early lens push vs editing the prompt (Qwen3.6-27B) — UNVERIFIED

(Written by the D4 agent; saved by the coordinator because the agent's tool could not write into results/. Numbers
recounted by the coordinator from outcomes.jsonl: memory → prompt, whole question, layer 24, 4x: 22/60 switched;
prompt → prompt 0/60; subject phrase only 20/60; question without the subject phrase 0/60; "add bridge alt next to the
cue" memory → prompt 60/60, prompt → prompt 0/60.)

**Short answer:** the pre-registered rule says "push writes the intermediate", but the run does not support that.
Test 1 could not run. Tests 2 and 3 called "write", but each fails a control built from edits of the input itself.
What the run shows is narrower: the early push only works on the subject phrase, and item by item it behaves most
like changing the cue in activation space.

## Smoke gate: passed

| Check | Result |
|---|---|
| Zero-size push leaves logits unchanged | max difference 0.0 logits over 1,512 rows |
| Alt prompt switches the answer (positive control) | 24/24 items |
| "Name bridge alt directly" switches the answer | 24/24 items |
| Earlier run's push reproduced (needed >= 95%) | 98.96% of 288 cells; main run 97.6% of 4,320 |

## Report

```
EXP early_push / d4_push_v1 @ 96c9ec2 | Qwen3.6-27B | n=60 per family (memory → prompt, prompt → prompt, memory → memory,
  prompt → memory on the same 60 scenes; countries 60+60) | seeds=[0]
Claim tested: the early lens push that switched memory → prompt answers acts like typing bridge alt into the
  question, not like writing the intermediate.
Headline: % of original answers that become the alternative answer, memory → prompt, tested push (whole question,
  layer 24, 4x) = 37% [26, 49] (Wilson)
  Baseline: question without the subject phrase 0% [0, 6]; subject phrase only 33% [23, 46]
  Control: random push of the same size 0% [0, 6]
Figures: fig1_where_the_push_works … fig5_collateral (this folder)
Three dumbest ways this could be wrong:
  1) The tested setting is weak (4x; prompt → prompt 0/60 there). Checked: at the strongest subject-phrase push
     (layer 16, 16x) the gap has the same sign, 47% vs 100%.
  2) High-dose rows are partly damage: 16x ~ 1.25 of the hidden-state norm; WikiText loss 2.33 -> 5.31 nats (random
     2.50). The tested 4x ~ 0.31 of the norm, loss 2.40 vs 2.34 random.
  3) bf16 batch noise: up to 0.94 logits across batches; effects are 18-100 points.
For the human to verify: outcomes.jsonl, kind=="push", dir=="lens", layer==24, scale==4.0, no "prompt" key:
  subset=="a": RL 22/60, BL 0/60; subset=="nb": RL 0/60; subset=="b": RL 20/60; kind=="edit", edit=="E-insert":
  RL 60/60, BL 0/60.
Status: UNVERIFIED
```

## The decision rule applied

| Test | Statistic [95% CI] | Rule's call | Usable? |
|---|---|---|---|
| 1. Agreement with "add bridge alt next to the cue" minus agreement with the alt-prompt patch (layers 32-48) | none | not testable | No: the edit switches 60/60, so no kappa; its validity check fails the same way |
| 2. Question without the subject phrase minus half the whole question | -18 [-24, -12] pts | write | Questionable: mentioning bridge alt elsewhere switches 0%, so injection also predicts "only at the subject phrase" |
| 2. Subject phrase only minus question without it | +33 [+22, +45] pts | — | Questionable |
| 3. prompt → prompt minus memory → prompt | -37 [-48, -25] pts | write | No: input edits show the same gap (embedding of bridge alt -52 [-63, -38]; bridge alt − bridge org embedding -62 [-73, -48]; text "add bridge alt next to the cue" -100) |

Verdict by the rule: "push writes the intermediate". Reading after the run (not pre-registered): not established.

## What the run does show
- The push only works on the subject phrase: up to 100% [94, 100] for memory → prompt (layer 16, 16x); the rest of
  the question and the last tokens give 0% at every layer and size; random pushes <= 10%.
- Item by item it agrees best with the same-layer patch from the alt prompt (Cohen's kappa +0.34 [+0.12, +0.55]);
  patch at layers 32-48 +0.17 [-0.07, +0.40]; embedding push +0.03; "swap the noun for bridge alt" -0.11.
- Later layers are mixed: closer to the alt prompt than to "name bridge alt directly" (write-like), closest to "swap
  the noun" (injection-like).
- The push carries less downstream than text edits: at layers 44-52 it moves the last tokens along the alt prompt's
  change by 0.35 on switched items vs 0.53 for "name bridge alt directly" and 0.01 for random.
- The run cannot separate "inject the word at the cue" from "write the bridge where it is recalled": for
  memory → prompt those are the same tokens.

## Dan's predictions vs results

| Question | Dan | Result | Match |
|---|---|---|---|
| Q4.1 Which version does the push match best? | push best, mention elsewhere worst | text edits switch every item (no per-item comparison); best graded match: same-layer patch (kappa +0.34); mention elsewhere 0% | partly |
| Q4.2 Do clue words matter? | yes | subject phrase 33-100%, rest 0% | yes |
| Q4.3 Does prompt → prompt move as much as memory → prompt? | memory → prompt slower | the opposite: 0% vs 37% (47% vs 100% at 16x) | no |
| Q4.4 Injection or real write? | real write | rule says write; its tests fail their controls | not established |

## Not interpretable or missing
- Test 1 and its validity check (the reference switches 100% of items).
- No agreement statistics for prompt → prompt, prompt → memory or countries (the push switches none or all).
- Lens readouts at layers 32-56 were not built.
- Text loss has no intervals (per-row values not saved).
