# X0b (v2): does X0's lookup / recall contrast hold on a diverse set? (exploratory)

Written 24 Oct evening, before any X0b result. Design: Dan's generalization plan (step 3, ~16:45), his decisions of ~17:40 (no digits-vs-words factor), ~18:40 (7 domains with the harness alt, gate per cell, ~40 per cell, start before the batch-27 commit), ~18:45 (v2: order by design, one pooled rule with C, the k-curve, probe (b) on the X0b states) and ~19:30 (the rule's thresholds; probe (b)'s target). Code: `scripts/x0b_generalize.py`; data: `data/tasks_v2/x0b_v2/`; job: `jobs/c3/x0b_v2.yaml`.

## 1. Question

X0 found, at the bridge's word: recalls lose most of their flips when the J++ part of the bridge change is removed, lookups lose little (9B) or some (27B). With a single-change alt on the same scenes (descriptive, after data), the lookup's extra loss at k = 25 was 0.05 [0.01, 0.09] on the 27B (L32) and −0.02 on the 9B (L12); at k = 100, 0.49 and 0.12. Does the contrast hold across 7 domains, 3 formats and 3 difficulty levels?

## 2. Rule (pooled, pre-registered for X0b, exploratory)

At the predicted layer (27B L32, 9B L12), the word, chat, J++ k = 25 signed with the random part of its share, top-token read, pooled over the eligible items of the cells that pass the gate:
- lookup excess as in X0; the contrast C = recall excess − lookup excess, on the same items and the same resamples (cluster bootstrap over bridge entities, 10,000 resamples, seed 0);
- **holds** iff lookup excess ≤ 0.10 (upper CI ≤ 0.20) and C ≥ 0.20 (lower CI ≥ 0.10);
- **fails** iff lookup excess ≥ 0.20 or C's upper CI < 0.10;
- **can't tell** if either reader's cell is invalid (S_whole < 0.30 or < 30 switched); **mixed** otherwise.

What the outcomes mean (Dan, step 3): holds: the contrast generalizes beyond the d1 scenes; lookup excess ≥ 0.20: the 27B's moderate lookup dependence generalizes. The X0 verdicts (27B not confirmed, 9B confirmed) do not change whatever X0b shows. Descriptive: per-layer labels, the k-curve (k = 50, 100 at the predicted layer), the strata (format, level, domain, locker order, number style), probe (b).

## 3. Design

| | |
|---|---|
| Set | `x0b_v2`: tasks_v2 v8, seed 2410, PP and PM on one context per scene; all 7 domains; formats prose / json / table; levels 0-2 (entities 3 / 6 / 9, look-alikes and filler from level 1, paraphrased questions and hard cues at level 2); 70 scenes per domain x format x level (4,410) |
| Order by design | `--locker-before 0.75`: per scene, with probability 0.75 the bridge's locker statement comes before the asked pick (prose: the two statements swapped after the shuffle if needed; json / table: the lockers and picks blocks); drawn from its own seeded stream, so no other draw moves. Locker-after cells will mostly be "can't tell" for the lookup; they document the order effect |
| Alt | single change, built by the harness for every domain: the asked person's pick becomes another person's pick in the scene (the first by name whose locker and memory number both differ from the bridge's and whose name is one token at the bridge's position); nothing else changes |
| Position, layers | the asked person's bridge word; 27B L28 / 30 / 32 / 34, 9B L10 / 12 / 14 |
| Arms | whole; without the J++ part (k = 25 at every layer; 50 and 100 at the predicted layer); without a random part of the same share; X0's non-negative J++ arm at the predicted layer comes along |
| Gate | per cell (domain x format x level): unedited org accuracy under the decisive read ≥ 0.80 for both readers; a failing cell is "can't test" and left out of the pooled rule |
| Eligible | org and alt answered right by both readers (greedy text and decisive read), at most 40 per cell, in scene order |
| Probe (b) | org states at the bridge's word, predicted layer, every aligned scene; target: the bridge's locker statement's ordinal among the locker statements (the same target in every format); per format and order, one-hot ridge cross-validated by bridge entity (x0_probe's code); baselines: chance, majority, the asked pick's ordinal only, the visible layout only (how many locker statements precede the pick, of how many). Question: does the address appear in JSON and tables too? |

## 4. Data and its limits (from `plan`, tokenizer only, before any model run)

- 2,258 of 4,410 scenes align (median 47 per cell). Drops: the bridge or its alt is not one token at one position, mostly in shapes, vehicles, elements, planets and instruments; no other pick with a different locker and memory number (58).
- Order: before / after = 715 / 252 (prose), 241 / 69 (json), 737 / 244 (table).
- **JSON covers 3 domains only** (animals, Greek, shapes): there the name follows a quote with no space, and most names split into several tokens.
- **Entities: 61** (Dan asked for at least 100; the 7 domain tables hold 81 in all, and multi-token names drop out). Shapes cells hold 4-25 scenes.

## 5. Controls

- The random part at J++'s own share, per item and k.
- Both readers on the identical patch.
- The valid-cell bar (S_whole ≥ 0.30 and ≥ 30 switched), flagged per stratum.
- The per-cell competence gate.
- Probe (b): the locker-after scenes (control by construction), and the layout-only and pick-ordinal-only baselines.

## 6. Not tested

- Confirmatory claims per stratum: strata are descriptive.
- Other positions than the word, other dictionaries (W_U, W_E, random).

## Decision log

- v1 (`x0b_v1`, post-hoc order, X0's rule) was queued and cancelled before it ran, after Dan's v2 decisions (~18:45). Its data stays in `data/tasks_v2/x0b_v1/`, unused.
- The job runs the 27B and the 9B in parallel inside one 2-GPU job (one process per GPU), because the box's 2-GPU worker would otherwise run them one after the other on one GPU.
- tasks_v2 changes for X0b, both off by default: each item records its scene's facts (metadata only); `--locker-before` (the order knob).
- **The C threshold** (Dan, 24 Oct ~20:45): the brief's graded threshold for C is >= 0.30 with lower CI >= 0.15, to be used unless the run had started. x0b_v2 started at ~19:29 Paris (17:29 UTC), before this decision, so its rule keeps C >= 0.20 (lower CI >= 0.10) as written above; the brief's threshold is reported beside it, as a description.
