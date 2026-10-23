# Finding 3: the last tokens read the answer's digit, not the entity's name

Packet for the hand check of 23 Oct 2026 (Dan, Zach). UNVERIFIED until a human adds it to VERIFIED.md. Every number here comes from `recompute.py` in this folder, run on the saved rows; it matched every cell of `results/cross_model/20261023T091847Z/grid.csv` (45 of 45). An earlier, longer packet for the 27B and 32B only is `verification/finding3_name_vs_digit.md` (22-23 Oct).

## The claim in plain words

The model sees a list of five sentences, each binding an entity to a digit ("The ankle chart is in folder 5."), and a question that names the entity only through a cue it must recall ("the body part joining foot and leg"). To answer, the last tokens of the prompt (from the end of the user turn to the "Answer: " where the digit is read) have to take the digit from the right sentence. We stop those last tokens from attending to part of the answer's sentence, in every layer. If we hide the sentence but leave its digit visible, the model stays right; if we hide the sentence but leave its name visible, the model drops to guessing. So the last tokens fetch the digit; the name is used earlier.

Why two "sentence without X" conditions and not "the name alone" / "the digit alone": a lone digit token leaks through its neighbours (README: hiding only the digit still leaves 7-44% right; not recomputed here), so the decisive pair hides everything in the sentence except one part.

## The rule, fixed before the runs

Sentence lists (draws 1-3), `scripts/d2_parts.py` docstring, amended before any of its results were read and committed at 5cb6a87 (22 Oct 16:23 +0200), the same commit as the first spec `jobs/d2/d2_parts_v2_27b.yaml`:

> valid-split: lookup_off_nodigit and lookup_off_noname keep >= 0.90 right at both destinations
> H-digit-final-split: right(noname, final) <= 0.35 and right(nodigit, final) >= 0.70

Prose, tables and JSON, `jobs/d2/d2_formats_27b.yaml` at 444500e (22 Oct 20:23 +0200, before those runs):

> Finding 3 (name vs digit) holds in a format iff scripts/d2_parts.py's valid-split holds and H-digit-final-split holds for MP (H-name-q-split decisive only where the question is testable).

In words: count only lookups whose bridge is recalled (memory -> prompt) and that the model answers right unedited; "right" = the top token is the answer's digit. If the same parts of another sentence (off the answer's path) hidden from the question's tokens or from the last tokens keep less than 90% right, the cell is not interpretable. Otherwise it holds iff the sentence without its name hidden from the last tokens leaves at most 35% right and the sentence without its digit hidden there keeps at least 70%.

## Headline (recomputed)

- Sentence lists, three draws: 0-11% right with the digit hidden on seven models (27B 10-11%, 9B 1-2%, Olmo-Hybrid 10-11%, 122B 7-9%, 32B 1.5-4%, OLMo-3 0-5%, Muse 1-3%); Gemma 27-29%; with the name hidden instead 85-97% stay right. Every draw cell holds (21 of 21).
- Prose, tables, JSON: 18 of 24 cells hold, Muse prose fails (2 of 5 right), three small cells not interpretable (Olmo-Hybrid prose and JSON, OLMo-3 prose: the off-path control at the question's tokens is 86-89%), Muse tables and JSON not testable (no item answered right).
- 45 cells: 39 holds, 1 fails, 3 not interpretable, 2 not testable. Three cells have no run (27B, Olmo-Hybrid, 122B draw 3: no spec).

## Worked example (random item, `random.Random(0)` over the sorted ids of the 27B's first draw, memory -> prompt, right unedited)

Reproduce with `python3 verification/finding3_2026-10-23/recompute.py --example`. Item `body-RL-e5f0-0103`, run `results/attn_knockout/d2_parts_v2_27b/`:

Prompt: "The brain chart is in folder 7. The ankle chart is in folder 5. The elbow chart is in folder 4. The wrist chart is in folder 3. The eye chart is in folder 8. Which folder holds the chart on the body part joining foot and leg? Answer with a single word and nothing else." Answer: 5 (ankle).

| Hidden from the last tokens, every layer | Model's answer |
|---|---|
| nothing | 5 (right) |
| the whole answer's sentence "The ankle chart is in folder 5." | 7 (the brain chart's digit) |
| that sentence without its name (the digit "5" and the rest hidden, "ankle" visible) | 7 |
| that sentence without its digit (the name and the rest hidden, "5" visible) | 5 (right) |
| another sentence without its name ("The eye chart is in folder 8." minus "eye") | 5 (right) |
| another sentence without its digit | 5 (right) |

## Where the numbers come from

- Draw runs: `results/attn_knockout/<run>/rows.jsonl` (one row per item and condition: `family`, `id`, `source`, `dest`, `layers`, `top`, `correct`) and `cases.jsonl` (`prompt`, `answer`, `tok_A`, `conf_toks`, `sources`, `source_text`). Filter: `family == "RL"`, `layers == "all"`, items whose `source == "none"` row is correct.
- Format runs: the same with `family == "MP"`, split by the format in `cases.jsonl` `wording` (prose / table / json).
- The run behind every cell is listed in `recompute.py` (`RUNS`) and in README, "Runs", finding 3; the grid's own index is `results/cross_model/20261023T091847Z/sources.txt`.
- Seeds: the scenes come from each data set's draw (`data/pointer_v4/main`, `seed2`, `seed3`; `data/tasks_v2/d2_formats_v1`, seed 31); the off-path spans use seed 0 (manifest `seeds`).
