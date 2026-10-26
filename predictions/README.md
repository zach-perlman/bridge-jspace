# Dan's predictions

Before any result is opened, Dan writes a guess under each question (`Dan:`). After the run, the agents add their pre-registered prior, the result and a verdict under it. Dan's answers are never edited; each file names the commits that hold them.

One file per day, by the day the batch was set up and run:

| Day | File | Batches | What was asked | Right / partly / wrong / not decidable |
|---|---|---|---|---|
| 20 Oct | [2026-10-20_dan.md](2026-10-20_dan.md) | 1 (runs the night of 20-21 Oct) | Where a stated bridge sits; blocking the read of the answer's statement; what a patch of the last tokens carries (the word, the statement's place, the digit); is an early lens push the same as editing the input | 6 / 7 / 5 / 2 (20) |
| 21 Oct | [2026-10-21_dan.md](2026-10-21_dan.md) | 2-5 | The read and the pointer in Python code and other languages; counted from the start or the end; a fitted pointer direction; 85 entities and 9 wordings; plain-text prompts; OLMo | 22 / 19 / 28 / 1 (70) |
| 22 Oct | [2026-10-22_dan.md](2026-10-22_dan.md) | 6-12 | Five models; the OLMo post-training ladder; is the fitted direction the model's own address; a positive control for the lens; name vs digit; the stated bridge on four topics; where the lens writes a stated bridge; finding 5 and the late read on fresh scenes; a random-damage control | 24 / 9 / 11 / 4 (48) |
| 23 Oct | [2026-10-23_dan.md](2026-10-23_dan.md) | 13-15 | The night of 22-23 Oct: the lens beyond its own word; every lens result on J++ (Qwen3-32B and OLMo with our fits, Gemma and Muse with Zach's); Olmo-Hybrid; longer lists; a third draw; tables and JSON for the stated bridge; Qwen3.5-122B, the whole grid | 8 / 7 / 4 / 1 (20) |
| 24 Oct | [2026-10-24_dan.md](2026-10-24_dan.md) | 25-30 | X0 (C3's split at a fixed layer, raw text, W_U / W_E / random against J++, more atoms); the digit check and Qwen3.5-122B; the probes at the bridge word and the probe subspace as an edit; X0b; the mass-mean subspaces; X4 (the key in another language or as a symbol); PCA at J++'s share | new format: Brier and calibration (below) |
| 25 Oct | [2026-10-25_dan.md](2026-10-25_dan.md) | 31-38 | The overnight grid (the 9B replication fixed in advance, the 122B, natural passages); which route the lookup follows (identity, position, value); J++ directions fitted to another scene; J++ and the pointer directions removed together; the routes at more layers; the pointer with a random part of J++'s size; one part added alone; Muse Glimmer 30B, the held-out family | new format: Brier and calibration (below) |
| 26 Oct | [2026-10-26_dan.md](2026-10-26_dan.md) | 39-44 | The split on the logit difference instead of switches; the 27B's gap within terciles of the change's shift; the identity direction (D1); where the route is read (D2, withdrawn); the pointer directions beyond simple scenes (T); a pointer found without slot labels (P_cf); writing the pointer | 39, 40, 42, 43, 44 scored; 41 withdrawn |

Total so far (batches 1-24): 60 right, 42 partly, 48 wrong, 8 not decidable, of 158 scored questions (38% right). This scorecard is kept as it is and not rescored.

**From batch 25 on (Dan, 24 Oct).**
- Each question lists its outcomes as options.
- Dan answers with one option and a confidence from 50 / 60 / 70 / 80 / 90%, with an optional one-line why.
- "50%, no prior" is a valid answer. A skipped question is recorded as skipped and not scored.
- Each answer is scored by its Brier score, (confidence − outcome)², where the outcome is 1 if the chosen option happened. Lower is better: always answering "50%, no prior" scores 0.25.
- Exact numbers are optional. A range is scored by whether it covers the result (covered / not), apart from the Brier score.
- Descriptive questions on data Dan has already seen (e.g. X-fig) are scored separately, not in the totals.

Calibration, by confidence bucket, across batches from 25 on (filled as results come in):

| Confidence | Answers | Happened | Share happened | Mean Brier |
|---|---|---|---|---|
| 40% | 2 | 0 | 0.00 | 0.16 |
| 50% | 4 | 1 | 0.25 | 0.25 |
| 60% | 12 | 6 | 0.50 | 0.26 |
| 70% | 33 | 11 | 0.33 | 0.36 |
| 75% | 1 | 1 | 1.00 | 0.06 |
| 80% | 26 | 11 | 0.42 | 0.39 |
| 85% | 5 | 5 | 1.00 | 0.02 |
| 90% | 20 | 10 | 0.50 | 0.41 |
| 95% | 2 | 1 | 0.50 | 0.45 |
| 100% | 1 | 1 | 1.00 | 0.00 |

Batches 25-44 so far (106 scored answers with a confidence): mean Brier 0.34 ("50%, no prior" everywhere would score 0.25); 47 of 106 top options happened. Not in the Brier totals: Q25.5 and Q25.10 (no confidence given; both wrong) and Q25.12 (X-fig, descriptive). Rows at 75%, 85% and 95% hold answers given off the 50-90% scale. Multi-option answers are scored on their top option. Q28.6 scored by Dan (25 Oct). Q32.4 unanswered, Q32.9, Q39.2 and Q44.2 void (can't tell); batch 41 withdrawn before answers. Q40.1 scored as written, with Dan's note that its bar was out of reach at the union's share (a design error in the question). All of batches 25-44 scored.

**Open:** batch 12 (opened early at Dan's request; answers count as written after the results). Batches 13-15 are scored (23 Oct); the runs still pending then are named in each verdict.
