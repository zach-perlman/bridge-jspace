# Finding 4 on natural text: design (approved by Dan 23 Oct, amended before any run; nothing run)

Lens-free. Specs: `jobs/d2/{qwen36_27b,qwen35_9b,qwen3_32b,olmo3_7b_instruct}_d2_natural_read.yaml`. Code: `scripts/natural_read.py` (items, competence, verdict), `scripts/attn_knockout.py` (`--dataset natural_read_v1`, the same blocking as every finding 4 run). Status: designed, CPU dry run done, approved with amendments (Dan, 23 Oct: primary bar 10% / 20%, every eligible item, the eligibility funnel reported), not enqueued.

## What we test

Finding 4 says a lookup ends in a late attention read: when the last tokens before the answer cannot attend to the sentence that holds the answer, the lookup drops to guessing (0-9% right on the lists of seven models, chance 20%), while hiding another sentence keeps ~100%, and on the hybrids hiding that sentence in the DeltaNet layers instead keeps ~100%. All of that is on synthetic lists ("The pig's locker is 9.") and, once, ~2,000 tokens of neutral filler. Here the context is a real Wikipedia paragraph and the question is a human-written one.

Worked example (item NAT-0050, from the CPU dry run). Paragraph (5 sentences): "Since teachers can affect how students perceive the course materials, ... On teacher/course evaluations, it was found that teachers who have a positive disposition towards the course content tend to transfer their passion to receptive students. These teachers do not teach by rote ... One of the difficulties in this approach is that teachers may have repeatedly covered a curriculum until they begin to feel bored with the subject which in turn bores the students as well. ..." Question: "What gets transferred to students who are receptive to the teacher?" Answer: "passion". The answer's sentence is the second; the off-path sentence is the fourth (35 vs 28 tokens). We hide the second sentence from the last tokens and read the answer's first token " passion"; then the same with the fourth sentence hidden instead.

| What is hidden from the last tokens | Late read holds | Relay (another position reads the sentence and passes the answer on) |
|---|---|---|
| the answer's sentence, every attention layer | ≤ 10% right (primary bar) | > 20% right |
| another sentence of the paragraph | ≥ 90% right | ≥ 90% right |
| the answer's sentence, every DeltaNet layer (hybrids) | ≥ 90% right | ≥ 90% right |
| the answer's sentence, from every later token (floor) | ≤ 10% right | ≤ 10% right |

## Data: SQuAD v1.1 dev, and why

SQuAD v1.1 dev (Rajpurkar et al. 2016; CC BY-SA 4.0 per the dataset's site; 10,570 questions on 2,067 paragraphs of 48 Wikipedia articles). Every question has its answer as a marked span of the paragraph, so the answer's sentence is found from the span, not guessed; three annotators give their spans, so we can require that they agree on the first word. The dev set is public and small (4.9 MB).

Not SQuAD v2.0: it adds unanswerable questions on the same kind of paragraphs, which this test does not use. Not TwoHopFact: it has no passages; each fact is one template sentence ("The developer of X is Y."), so an in-context version is a list again (it is `twohop_pilot.py`'s "both facts in the prompt" condition). The natural two-hop variant would be HotpotQA (dev, distractor setting; CC BY-SA 4.0): 2 gold paragraphs and 8 distractors per question, already cut into sentences with the supporting sentences marked, so one can hide the bridge's sentence and the answer's sentence separately. Not built or pinned here; not before 30 Oct (Dan, 23 Oct).

Pin. Raw file: `https://raw.githubusercontent.com/rajpurkar/SQuAD-explorer/240e165ab706d95bd4323653bb92421f446208cf/dataset/dev-v1.1.json`, sha256 `95aa6a52d5d6a735563366753ca50492a658031da74f301ac5238b03966972c9` (the site's own copy has the same sha256), kept in `cache/natural_read/squad/` (not committed). Derived items: `data/natural_read_v1/items.json`, sha256 `60b8527dc63c2fff3217d40ece1a7f8405a46aa3946f8d7f36f2d475eab21cc9`. Both in `pins.py` and `data/SOURCES.md`; `tests/test_pins.py` rebuilds the items from the raw file when it is cached.

## How items are built

Prompt: the paragraph, a newline, the question and "Answer with a few words copied from the text and nothing else." as one user turn, in each model's chat template, thinking off, "Answer:" prefilled (the format of every finding 4 run). The paragraph is cut into sentences by a rule-based splitter (a break after . ! ? followed by a capital, a digit or a quote; never after an abbreviation, a single letter or a word with an inner period such as U.S.). The answer's sentence is the one that contains the answer's span.

Filters, all tokenizer-free so every model starts from the same items: the answer (a leading "the/a/an" dropped) starts with a letter at a word start and has at most 4 words; every annotator's answer starts with the same word; no other word of paragraph or question shares the answer's first word's first 5 letters (so "instances" is dropped when "instance" appears elsewhere: the model could answer from another sentence and be scored wrong); paragraphs of 4+ sentences and at most 1,200 characters; the answer's sentence has 5+ words. Off-path sentence: two or more sentences away from the answer's (the adjacent one is the likeliest to hold a pronoun's antecedent), character length within 0.75-1.33 of the answer's, the closest, seeded tie-break. One question per paragraph (seeded), so no two items share a paragraph. Swap partner: another article's paragraph with no word sharing that prefix. Result: 718 items, 48 articles; 1,266 of 10,570 questions passed.

Per tokenizer (in the knockout builder): an answer whose first token has under 3 characters and is not its whole first word is left out (a short piece many words begin with). 27B and 9B (one tokenizer file): 632 of 718 kept; Qwen3-32B and OLMo-3: 628. Full prompts are 109-374 tokens (median 204) on the Qwen models, 132-377 (median 223) on OLMo-3.

Per model (competence run, the first GPU stage of each spec), four prompts per item: the paragraph; the answer's sentence alone; the paragraph without the answer's sentence; another article's paragraph. An item is eligible if, with the paragraph, the answer's first token is on top and the greedy answer (12 tokens) contains a gold answer; with the sentence alone, the first token is on top; and without the sentence, it is not. So the sentence is enough and needed, and the answer is not known from memory or the rest of the paragraph. The knockout run takes every eligible item (no cap; Dan, 23 Oct). The competence summary and the verdict report the funnel per model: built → eligible, with how many items each criterion drops in order (short first token; first token not on top with the paragraph; greedy answer wrong; the sentence alone not enough; still answered without the sentence) and how many fail each criterion on its own.

Not covered (kept as Dan decided, 23 Oct): items whose answer needs a neighbouring sentence (a pronoun's antecedent, a subject named earlier) fail "the sentence alone" and are dropped, so the verdict is about answers one sentence gives on its own. The funnel's "the sentence alone not enough" count is how many such items each model loses.

## Scoring and baselines

Score: the answer's first token after "Answer:" is the model's top token, as in every finding 4 run (one forward per condition). The competence run checks that, on the unedited prompt, this first token stands for the whole answer (greedy answer right). There is no list of candidate answers, so the 20% chance of the lists does not exist.

Baselines, all on the knockout run's items: (1) the floor, the answer's sentence hidden from every later token in every layer (on hybrids also removed from the DeltaNet recurrence), which should match deleting the sentence: wrong by construction for text deletion, so it is the in-model check that hiding equals removing; (2) the question after another article's paragraph, unedited (the "unedited-but-shuffled" control, kept as built; no within-paragraph shuffle: Dan, 23 Oct): what the model answers with a paragraph of the same shape and no answer in it; (3) the blocked answers scored against another item's answer (a fixed shuffle of the answer key): how often a wrong answer scores "right" by accident on first tokens. (2) and (3) are reported, not decisive.

## The blocking

The same exact edge knockout as finding 4 (`bridge_jspace.knockout`): in an attention layer, the logits from the destination tokens to the source sentence set to minus infinity; in a DeltaNet layer, the destination's output recomputed with the source's values zeroed (keys, betas and decays kept), so only the direct source-to-destination terms go. "The last tokens" are every token after the user's text: 11 on the Qwen models (`<|im_end|>`, newline, `<|im_start|>`, `assistant`, newline, `<think>`, two newlines, `</think>`, two newlines, `Answer`, `:`), 7 on OLMo-3 (the same without the think block). This is the "final" set of every earlier finding 4 run, not literally the last 1-2 tokens.

Layers: every attention layer (27B: 16 of 64; 9B: 8 of 32; Qwen3-32B and OLMo-3: all layers, which are all attention). Hybrids also get the answer's sentence hidden from the last tokens in every DeltaNet layer instead. Also run, reported only: the sentence hidden from the question words (all layers). Knocked reads per item: 14 on the hybrids, 6 on the dense models.

## n and power

Every eligible item per model (at most 632 or 628; at least 100 right unedited to be testable). On the lists, the gap between the answer's sentence hidden (0-9%) and another sentence hidden (98-100%) is ~90 points; any n above ~20 detects that. The n matters for the bars' interval widths (Wilson 95%). Primary bar: a 10% point has upper bound 17.4% at n = 100, 14.9% at n = 200, 13.9% at n = 300, and passes the 20% upper bar from n = 54; so from the minimum n of 100 the point estimate (≤ 10%) is what decides. Secondary bar: a 20% point has upper bound 28.9% at n = 100, 26% at n = 200. Control: at 90% its lower bound is 82.6% at n = 100, 85.1% at n = 200, 86.1% at n = 300 (bar 85%); at n = 100 it needs ≥ 92%. Items are clustered by article (48), so an article-cluster bootstrap interval of the decisive cell is reported, not decisive.

## The rule (pre-registered in each spec; `natural_read.judge`)

Amended by Dan on 23 Oct, before any run. On items right unedited in the knockout run, PRIMARY verdict: the late read holds iff the answer's sentence hidden from the last tokens in every attention layer leaves ≤ 10% right with the Wilson upper bound ≤ 20%, AND the off-path sentence hidden there keeps ≥ 90% right with the Wilson lower bound ≥ 85%, AND (hybrids) the answer's sentence hidden from the last tokens in every DeltaNet layer instead keeps ≥ 90% right. SECONDARY verdict, for comparability with the grid: the same with finding 4's bar, ≤ 20% right with the upper bound ≤ 30%. Both are in the verdict's summary (`verdict.json`, `verdict.md`) and on its figure.

Why 10% / 20%: on the lists 20% was guessing among five digits; here the floor is ~0% by construction (the text deletion is wrong on every eligible item) and ≤ 10% in the model by the validity condition below, so finding 4's bar would let up to a fifth of the items survive through another route and still "hold". The secondary verdict keeps the comparison with the lists.

Not interpretable (both verdicts) if: the floor (sentence hidden from every later token, every layer) leaves > 10% right, i.e. hiding does not remove the sentence; or the off-path control fails (< 90% or lower bound < 85%). Not testable if fewer than 100 items are right unedited.

## Three dumbest ways this could be wrong

1. The first-token score credits a wrong answer that starts like the right one, or misses a right answer phrased differently ("The passion..."). Mitigations: the 5-letter prefix filter (no other word of the prompt starts like the answer), all annotators start their answer with the same word, short first tokens dropped, greedy answer checked at competence. Remaining check: baseline (3) above; `rows.jsonl` keeps each blocked read's top token, so 20 random items (seed 0) can be read by hand.
2. The answer is known without reading the sentence (SQuAD is Wikipedia; large models have read it). Then "still right with the sentence hidden" measures memory, not a relay. Mitigation: items must be wrong with the sentence deleted; check: the floor ≤ 10% and the swapped-paragraph baseline near 0.
3. The off-path sentence is not neutral in real text (it may name the subject the answer's sentence refers to with "it" or "they"), so the control could fail for linguistic reasons, not because blocking breaks the model. Mitigation: it is two or more sentences away; check: if the control fails, the run is not interpretable rather than a failure of the finding, and the verdict reports the off-path sentence hidden from every later token (how much the answer depends on it at all).

## Cost and what was run

Nothing on a GPU. CPU only: the item build (`natural_read.py make`) and a dry run (`natural_read.py dryrun`) on the 27B's, Qwen3-32B's and OLMo-3's tokenizers (every case built, no model forward). Estimates from the late-read seed2 runs (`results/jobq/ledger_sesterce-a100x4.jsonl`: 27B 26.7 reads/s at 84 tokens, ~2,200 token-reads/s) and the 27B's seed2 competence (12,480 prompts in 11 min), at the most items each model can have (632 / 628): 27B ~0.45 h, 9B ~0.2 h, Qwen3-32B ~0.4 h, OLMo-3 ~0.15 h; specs ask 0.6 / 0.3 / 0.5 / 0.2 GPU-h and 75 / 40 / 75 / 30 GB (a forward holds one item's ≤ 15 rows, so memory does not grow with n).

## Decisions (Dan, 23 Oct, before any run)

- Bar: primary 10% / 20%; finding 4's 20% / 30% reported as secondary.
- The "another article's paragraph" control kept as built; no within-paragraph shuffle.
- Eligibility kept (the answer's sentence enough on its own); the funnel is reported, and coreference-dependent items are not covered.
- n: every eligible item, no cap.

## Next steps

- HotpotQA two-hop variant (hide the bridge's sentence and the answer's sentence separately): not before 30 Oct.
