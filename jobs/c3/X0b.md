# X0b: does X0's lookup / recall contrast hold on a diverse set? (exploratory)

Written 24 Oct evening, before any X0b result. Design: Dan's generalization plan (step 3, 24 Oct ~16:45), the 24 Oct ~17:40 order and number-style decisions, and his answers of 24 Oct ~18:40 (below). Code: `scripts/x0b_generalize.py`; data: `data/tasks_v2/x0b_v1/`; job: `jobs/c3/x0b_v1.yaml`.

## 1. Question

X0 found, at the bridge's word: recalls lose most of their flips when the J++ part of the bridge change is removed, lookups lose little (9B) or some (27B). With a single-change alt on the same scenes, the 27B lookup's extra loss at L32 was 0.05 [0.01, 0.09] (descriptive, after data). Does this hold across 7 domains, 3 formats and 3 difficulty levels, or is it a property of the simple d1 scenes?

## 2. Rule (exploratory; X0's rule, reported, not a verdict on C3)

At the predicted layer (27B L32, 9B L12), the word, chat, J++ k = 25 signed, the random part of its share, top-token read, pooled over the eligible items:
- confirmed iff lookup excess ≤ 0.10 and recall Jdep ≥ 0.30; killed iff lookup excess ≥ 0.20 or recall Jdep < 0.20; else not confirmed; can't tell if either cell is invalid (S_whole < 0.30 or < 30 switched).
- Labels per reader and layer as X0 (around / through / mixed / can't tell). 95% CIs from a cluster bootstrap over bridge entities (10,000 resamples, seed 0).

What each outcome means (Dan, step 3):
- lookup excess ≤ 0.10: the 27B's moderate lookup dependence in X0 depends on scene features (or on the two-change alt), not a general property;
- lookup excess ≥ 0.20: the moderate dependence generalizes;
- in between: mixed, read with the strata.

The X0 verdicts (27B not confirmed, 9B confirmed) do not change whatever X0b shows.

## 3. Design

| | |
|---|---|
| Set | `x0b_v1`: tasks_v2 v8, seed 2410, PP and PM on one context per scene; all 7 domains (animals, planets, elements, Greek, shapes, vehicles, instruments); formats prose / json / table; levels 0-2 (entities 3 / 6 / 9, look-alike distractors and filler from level 1, paraphrased questions and hard cues at level 2); 70 scenes per domain x format x level (4,410 scenes) |
| Alt | single change, built by the harness for every domain: the asked person's pick becomes another person's pick in the scene (the first by name whose locker and memory number both differ from the bridge's and whose name is one token at the bridge's position); nothing else changes |
| Position, layers | the asked person's bridge word; 27B L28 / 30 / 32 / 34, 9B L10 / 12 / 14 (X0's predicted layers inside) |
| Arms | whole, without the J++ part (k = 25 signed OMP over the letter-token atoms), without a random part of the same share; X0's non-negative J++ arm at the predicted layer comes along (descriptive) |
| Gate | per cell (domain x format x level): unedited org accuracy under the decisive read ≥ 0.80 for both readers; a failing cell is "can't test" and left out of the pooled rule |
| Eligible | org and alt answered right by both readers (greedy text and decisive read), at most 40 per cell, in scene order |
| Strata (descriptive) | format, level, domain, the bridge's locker statement before / after the asked pick statement (post hoc: the generator shuffles prose lines and json / table blocks, about 50/50 in every format), number style (digits / words, as generated; not a design factor) |

Dan's answers (24 Oct ~18:40): all 7 domains with the harness alt; order stratified post hoc; gate per cell, ~40 per cell; the run may start before the batch-27 commit, and no X0b result is opened or summarized before it.

Dropped after Dan's decision of ~17:40: the digits-vs-words factor (the budget goes to more scenes per cell).

## 4. Data and its limits (from `plan`, tokenizer only, before any model run)

- 2,258 of 4,410 scenes align (median 47 per cell). Drops: the bridge or its alt is not one token at one position (2,094; mostly shapes, vehicles, elements, planets, instruments), no other pick with a different locker and memory number (58).
- **JSON covers 3 domains only** (animals, Greek, shapes): there the name follows a quote with no space, and most names split into several tokens. Elements, instruments, planets and vehicles have no JSON cases.
- **Entities: 61** (Dan asked for at least 100; the 7 domain tables hold 81 in all, and multi-token names drop out). Shapes cells hold 4-25 scenes.
- Order: before / after is 478 / 489 (prose), 151 / 159 (json), 497 / 484 (table).

## 5. Controls

- The random part at J++'s own share (per item).
- Both readers on the identical patch.
- The valid-cell bar (S_whole ≥ 0.30 and ≥ 30 switched), per stratum flagged.
- The per-cell competence gate.

## 6. Not tested

- Whether any stratum is "around" or "through" in a confirmatory sense: strata are descriptive.
- Other positions than the word, other dictionaries (W_U, W_E, random), the k-curve.

## Decision log

- 24 Oct evening (agent, before the run): the X0b job runs the 27B and the 9B in parallel inside one 2-GPU job (one process per GPU), because the box's single 2-GPU worker (needed for the 122B) would otherwise run them one after the other on one GPU.
