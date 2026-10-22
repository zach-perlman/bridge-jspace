# Finding 3 hand-check: the question's tokens read the name, the last tokens read the digit

For Dan and Zach, to check by hand from Fri 23 Oct. Finding 3 is frozen in [README.md](../README.md) and is not in [VERIFIED.md](../VERIFIED.md): it stays UNVERIFIED until you add it. Every number here is either copied from README.md or recounted from the saved runs README.md cites. Nothing from the night of 22-23 Oct was opened. The recount and raw-row sections are printed by `scripts/verification_packets.py` (read-only, no GPU) and pasted unedited.

## 1. The claim

README, findings table, row 3: **"The question's tokens read the bridge's name; the last tokens read its digit."** (🟢 fixed in advance; two draws of scenes on 5 models; prose, tables and JSON on 2 models · frozen.)

Worked example (item `countries-RL-e5f0-0018`, row 20 of 5a). The list is "The France file is in drawer 4. The Syria file is in drawer 6. The Venezuela file is in drawer 1. The Finland file is in drawer 2. The Peru file is in drawer 7." The question is "Which drawer holds the file on the country whose capital is Lima?", and the answer is 7. The answer's sentence is "The Peru file is in drawer 7.": its name is "Peru" and its digit is "7". The test hides one part of that sentence from one group of tokens in every layer, then counts how often the model still answers 7. In row 20 the whole sentence is hidden from the last tokens, and the model answers 1 (Venezuela's digit).

**Wording to check in README.** The findings-table cell says "from the last tokens, the sentence without its digit hidden: 0-11% right; without its name: 82-100%". Slide 2 and the code say the reverse. Hiding the sentence **without its name** (`lookup_noname`: the digit and the other tokens hidden, the name visible) leaves 4-11% right. Hiding the sentence **without its digit** (`lookup_nodigit`: the name and the other tokens hidden, the digit visible) leaves 88-96%. Sources: slide 2, `scripts/d2_parts.py` (H-digit-final-split) and the recount in 3b. The weak spot "On Gemma … hiding the sentence except its digit still leaves 21-29% right" has the same problem, since slide 2 gives Gemma's 28-29% for the sentence without its name. This looks like a wording slip in README, not a problem in the data. Please confirm and correct README.

How the runs name things:

- **family**: `RL` = memory → prompt: the bridge is recalled from a cue ("the country whose capital is Lima") and its digit is looked up in the list. `DL` = named → prompt ("Which drawer holds the file on Peru?"). `RR` = memory → memory (recall; not used here).
- **source** (what is hidden): `lookup` is the answer's whole sentence, `lookup_nodigit` the sentence without its digit, `lookup_noname` the sentence without its name. The controls `lookup_off_nodigit` and `lookup_off_noname` hide the same parts of another sentence of the list with the same token length. The runs also hide the name alone (`lookup_name`) and the digit alone (`lookup_digit`). Those two are not decisive: the digit leaks through its neighbours (README weak spot: 7-44% right with only the digit hidden).
- **dest** (who may not read it): `question` = the question sentence and the instruction after it. `final` = every token after the user turn (`<|im_end|>`, the assistant header, the empty think block, `Answer:` and the appended space where the answer is read). README's "the last tokens" is `final`.
- **layers** `all`: blocked in every layer, except the first token, which is never blocked. In attention layers, the dest-to-source attention logits are set to −inf in every head. In the 27B's DeltaNet layers (mode `value`), the source's values are removed from the dest's output. Indirect routes through other tokens stay open (manifest field `knockout`).
- **Which items count**: only items whose unedited row (`source == "none"`) is right.
- **Labels**: **right** = the top token is the answer's token (`top == tok_A` in cases.jsonl). **list** = another digit of the list (`top in conf_toks`). **off** = anything else.

Decision rule (`scripts/d2_parts.py` docstring and `jobs/d2/d2_parts_v2_27b.yaml`). It was fixed on 22 Oct before any run. The leak-robust "split" tests were added at 16:40, before any d2_parts result was read. Scope: memory → prompt, topics pooled, Wilson 95% intervals over items.

- valid-split: `lookup_off_nodigit` and `lookup_off_noname` keep ≥ 90% right at both destinations.
- H-digit-final-split (the last tokens read the digit): right(`lookup_noname`, final) ≤ 35% and right(`lookup_nodigit`, final) ≥ 70%.
- H-name-q-split (the question's tokens read the name): applies only if the question is testable, i.e. right(`lookup`, question) ≤ 70%. Then right(`lookup_nodigit`, question) ≤ right(`lookup`, question) + 15 points and right(`lookup_noname`, question) ≥ 85%.

## 2. Result files and rows

| Model | Draw (data) | Run folder | Memory → prompt items | In this packet |
|---|---|---|---|---|
| Qwen3.6-27B (revision 6a9e13bd) | first (`data/pointer_v4/main`) | `results/attn_knockout/d2_parts_v2_27b/` | 300 | main run: recount and 20 raw rows |
| Qwen3.6-27B | second (`data/pointer_v4/seed2`) | `results/attn_knockout/d2_parts_seed2_27b/` | 300 | recount |
| Qwen3-32B (revision 9216db57) | first (`main`) | `results/attn_knockout/qwen3_32b_d2_parts_v2/` | 300 | recount and 20 raw rows |
| Qwen3-32B | second (`seed2`) | `results/attn_knockout/qwen3_32b_d2_parts_seed2/` | 199 of 200 right unedited (countries and body parts: animals missed the memory → prompt competence gate by 0.0005; named → prompt keeps all three topics, 300 items) | recount |

n: 100 scenes per topic and family, three topics (countries, animals, body parts). Seeds: the scenes come from the data set's own draw (main or seed2); the control spans use seed 0 (manifest `seeds`).

Each run folder holds:

- `manifest.json`: model repo and revision, data files with sha256, sources and destinations. Written before the run.
- `cases.jsonl`, one line per item: `id`, `family`, `prompt` as fed, `answer`, `tok_A`, `conf_answers`, `conf_toks`, `sources` (the token positions of each span), `source_text`, `dests`.
- `rows.jsonl`, one line per item and condition: `family`, `id`, `source`, `dest`, `layers`, `mode`, `top` (the top token id), `correct`, `conf`, `logp`, `dlogp`.
- `parts_summary.md` and `.json`: d2_parts.py's table and verdicts, saved 22 Oct.
- `cases_report.json`: the competence gate per topic.
- `check.json`: the hook's no-op and positive-control checks.

Rows behind the claim, in `rows.jsonl`:

- `family == "RL"`, `layers == "all"`, `dest` in (`question`, `final`), and `source` in (`lookup`, `lookup_nodigit`, `lookup_noname`, `lookup_off_nodigit`, `lookup_off_noname`);
- only items whose `source == "none"` row has `correct == true`;
- reported, not decisive: the same filter with `family == "DL"` (named bridge).

Not in this packet, and not opened for it:

- The README's other models for this finding, Qwen3.5-9B, OLMo-3-7B and Gemma 4: `qwen35_9b_d2_parts_v2`, `olmo3_7b_instruct_d2_parts_v2`, `gemma4it_d2_parts_v2`, and their `*_d2_parts_seed2` runs.
- The tables and JSON runs (`d2_formats_27b`, `qwen3_32b_d2_formats`, scored by `scripts/d2_formats.py`).
- The post-hoc Qwen3-32B animals run (presumably `qwen3_32b_d2_parts_seed2_animals`; README labels it post hoc).

## 3. Recompute

Run everything from the repo root. No GPU is needed.

1. The run's own analysis: `uv run python scripts/d2_parts.py --name d2_parts_v2_27b`, then the same with `--name d2_parts_seed2_27b`, `--name qwen3_32b_d2_parts_v2` and `--name qwen3_32b_d2_parts_seed2`. It prints the table. It also **rewrites** `parts_summary.json` and `parts_summary.md` in the run folder, which are tracked in git. Afterwards `git status --short results/attn_knockout/` should list nothing, which means it reproduced the saved files byte for byte. I did not run it while preparing this packet, to leave results/ untouched.
2. An independent, read-only recount from rows.jsonl and cases.jsonl: `uv run python scripts/verification_packets.py headline --finding 3 --run d2_parts_v2_27b`, and the same for the other three runs. It shares no code with d2_parts.py; Wilson comes from `bridge_jspace.stats`. Its output is in 3b. While preparing this packet, every line of it was compared by script with the saved `parts_summary.md`: n, rate, interval and error split agree on all RL and DL lines of the four runs.
3. By hand, with plain python3 (no repo code), from the repo root:

```python
import json

run = "results/attn_knockout/d2_parts_v2_27b"
rows = [json.loads(line) for line in open(f"{run}/rows.jsonl")]
cases = {c["id"]: c for c in map(json.loads, open(f"{run}/cases.jsonl"))}
ok = {r["id"] for r in rows if r["family"] == "RL" and r["source"] == "none" and r["correct"]}
for src in ("lookup", "lookup_noname", "lookup_nodigit", "lookup_off_noname", "lookup_off_nodigit"):
    for dest in ("final", "question"):
        sel = [
            r
            for r in rows
            if r["family"] == "RL"
            and r["id"] in ok
            and r["layers"] == "all"
            and r["source"] == src
            and r["dest"] == dest
        ]
        right = sum(r["top"] == cases[r["id"]]["tok_A"] for r in sel)
        print(f"{src:20s} {dest:9s} n={len(sel)} right={right} ({100 * right / len(sel):.0f}%)")
```

Expected output on `d2_parts_v2_27b`:

- `lookup final n=300 right=25 (8%)`
- `lookup question n=300 right=270 (90%)`
- `lookup_noname final n=300 right=33 (11%)`
- `lookup_noname question n=300 right=300 (100%)`
- `lookup_nodigit final n=300 right=263 (88%)`
- `lookup_nodigit question n=300 right=270 (90%)`
- every `lookup_off_*` line: 300 right out of 300.

### 3a. Expected numbers, as README states them

- **Last tokens, memory → prompt, first draw** (four models: Qwen3.6-27B, Qwen3-32B, Qwen3.5-9B, OLMo):
  - the sentence without its name hidden: 2-11% right, as low as with the whole sentence hidden;
  - the sentence without its digit hidden: 88-96%;
  - the same parts of another sentence hidden (controls): 99-100%.
- **Last tokens, second draw:** without its name 10% (Qwen3.6-27B) and 4% (Qwen3-32B); without its digit 88% and 94%.
- **Question's tokens, memory → prompt:**
  - Qwen3.6-27B stays at 90% right with the whole sentence hidden, so the question is not testable there ("the recalled bridge skips this step").
  - Qwen3-32B drops to 32% (second draw: 37%). On its second draw, hiding the sentence without its digit gives 38%; hiding it without its name gives 100%.
- **Named → prompt (reported):** 5-12% right with the name hidden from the question's tokens, on all four models, the 27B included.
- **Verdicts** (d2_parts.py, saved `parts_summary.md`, first draw): for memory → prompt, H-digit-final-split holds on both models. H-name-q-split holds on Qwen3-32B and is not testable on Qwen3.6-27B. README: on the second draws "every verdict repeats" on both models.

### 3b. Recount from rows.jsonl (pasted output)

**Qwen3.6-27B, first draw**

Run `d2_parts_v2_27b`: items per family {'DL': 300, 'RL': 300, 'RR': 300}, right unedited {'DL': 300, 'RL': 300, 'RR': 300}; rows where right (top = tok_A) and the row's `correct` disagree: 0.

| family | hidden | from | layers | n | right | right [Wilson 95%] | another list digit | off the list |
|---|---|---|---|---|---|---|---|---|
| DL | lookup | final | all | 300 | 35 | 12% [9, 16] | 82% | 7% |
| DL | lookup | question | all | 300 | 26 | 9% [6, 12] | 1% | 90% |
| DL | lookup_nodigit | final | all | 300 | 299 | 100% [98, 100] | 0% | 0% |
| DL | lookup_nodigit | question | all | 300 | 24 | 8% [5, 12] | 1% | 91% |
| DL | lookup_noname | final | all | 300 | 39 | 13% [10, 17] | 77% | 10% |
| DL | lookup_noname | question | all | 300 | 295 | 98% [96, 99] | 1% | 0% |
| DL | lookup_off_nodigit | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_nodigit | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_noname | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_noname | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup | final | all | 300 | 25 | 8% [6, 12] | 88% | 3% |
| RL | lookup | question | all | 300 | 270 | 90% [86, 93] | 10% | 0% |
| RL | lookup_nodigit | final | all | 300 | 263 | 88% [83, 91] | 12% | 0% |
| RL | lookup_nodigit | question | all | 300 | 270 | 90% [86, 93] | 10% | 0% |
| RL | lookup_noname | final | all | 300 | 33 | 11% [8, 15] | 81% | 8% |
| RL | lookup_noname | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off_nodigit | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off_nodigit | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off_noname | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off_noname | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |

**Qwen3.6-27B, second draw**

Run `d2_parts_seed2_27b`: items per family {'DL': 300, 'RL': 300, 'RR': 300}, right unedited {'DL': 300, 'RL': 300, 'RR': 300}; rows where right (top = tok_A) and the row's `correct` disagree: 0.

| family | hidden | from | layers | n | right | right [Wilson 95%] | another list digit | off the list |
|---|---|---|---|---|---|---|---|---|
| DL | lookup | final | all | 300 | 26 | 9% [6, 12] | 83% | 9% |
| DL | lookup | question | all | 300 | 22 | 7% [5, 11] | 3% | 90% |
| DL | lookup_nodigit | final | all | 300 | 298 | 99% [98, 100] | 1% | 0% |
| DL | lookup_nodigit | question | all | 300 | 22 | 7% [5, 11] | 2% | 90% |
| DL | lookup_noname | final | all | 300 | 30 | 10% [7, 14] | 80% | 10% |
| DL | lookup_noname | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_nodigit | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_nodigit | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_noname | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_noname | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup | final | all | 300 | 22 | 7% [5, 11] | 88% | 4% |
| RL | lookup | question | all | 300 | 275 | 92% [88, 94] | 8% | 0% |
| RL | lookup_nodigit | final | all | 300 | 263 | 88% [83, 91] | 12% | 0% |
| RL | lookup_nodigit | question | all | 300 | 274 | 91% [88, 94] | 8% | 0% |
| RL | lookup_noname | final | all | 300 | 30 | 10% [7, 14] | 82% | 8% |
| RL | lookup_noname | question | all | 300 | 299 | 100% [98, 100] | 0% | 0% |
| RL | lookup_off_nodigit | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off_nodigit | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off_noname | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off_noname | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |

**Qwen3-32B, first draw**

Run `qwen3_32b_d2_parts_v2`: items per family {'DL': 300, 'RL': 300}, right unedited {'DL': 300, 'RL': 300}; rows where right (top = tok_A) and the row's `correct` disagree: 0.

| family | hidden | from | layers | n | right | right [Wilson 95%] | another list digit | off the list |
|---|---|---|---|---|---|---|---|---|
| DL | lookup | final | all | 300 | 9 | 3% [2, 6] | 95% | 2% |
| DL | lookup | question | all | 300 | 13 | 4% [3, 7] | 1% | 95% |
| DL | lookup_nodigit | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_nodigit | question | all | 300 | 13 | 4% [3, 7] | 0% | 95% |
| DL | lookup_noname | final | all | 300 | 9 | 3% [2, 6] | 95% | 2% |
| DL | lookup_noname | question | all | 300 | 293 | 98% [95, 99] | 1% | 2% |
| DL | lookup_off_nodigit | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_nodigit | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_noname | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_noname | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup | final | all | 300 | 10 | 3% [2, 6] | 93% | 4% |
| RL | lookup | question | all | 300 | 96 | 32% [27, 37] | 18% | 50% |
| RL | lookup_nodigit | final | all | 300 | 288 | 96% [93, 98] | 4% | 0% |
| RL | lookup_nodigit | question | all | 300 | 96 | 32% [27, 37] | 19% | 49% |
| RL | lookup_noname | final | all | 300 | 12 | 4% [2, 7] | 92% | 4% |
| RL | lookup_noname | question | all | 300 | 298 | 99% [98, 100] | 0% | 0% |
| RL | lookup_off_nodigit | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off_nodigit | question | all | 300 | 296 | 99% [97, 99] | 1% | 0% |
| RL | lookup_off_noname | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off_noname | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |

**Qwen3-32B, second draw**

Run `qwen3_32b_d2_parts_seed2`: items per family {'DL': 300, 'RL': 200}, right unedited {'DL': 300, 'RL': 199}; rows where right (top = tok_A) and the row's `correct` disagree: 0.

| family | hidden | from | layers | n | right | right [Wilson 95%] | another list digit | off the list |
|---|---|---|---|---|---|---|---|---|
| DL | lookup | final | all | 300 | 8 | 3% [1, 5] | 97% | 1% |
| DL | lookup | question | all | 300 | 5 | 2% [1, 4] | 2% | 96% |
| DL | lookup_nodigit | final | all | 300 | 298 | 99% [98, 100] | 1% | 0% |
| DL | lookup_nodigit | question | all | 300 | 6 | 2% [1, 4] | 2% | 96% |
| DL | lookup_noname | final | all | 300 | 8 | 3% [1, 5] | 95% | 2% |
| DL | lookup_noname | question | all | 300 | 291 | 97% [94, 98] | 1% | 2% |
| DL | lookup_off_nodigit | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_nodigit | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_noname | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off_noname | question | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup | final | all | 199 | 4 | 2% [1, 5] | 93% | 5% |
| RL | lookup | question | all | 199 | 74 | 37% [31, 44] | 12% | 51% |
| RL | lookup_nodigit | final | all | 199 | 188 | 94% [90, 97] | 5% | 1% |
| RL | lookup_nodigit | question | all | 199 | 76 | 38% [32, 45] | 13% | 49% |
| RL | lookup_noname | final | all | 199 | 7 | 4% [2, 7] | 91% | 6% |
| RL | lookup_noname | question | all | 199 | 199 | 100% [98, 100] | 0% | 0% |
| RL | lookup_off_nodigit | final | all | 199 | 199 | 100% [98, 100] | 0% | 0% |
| RL | lookup_off_nodigit | question | all | 199 | 199 | 100% [98, 100] | 0% | 0% |
| RL | lookup_off_noname | final | all | 199 | 199 | 100% [98, 100] | 0% | 0% |
| RL | lookup_off_noname | question | all | 199 | 199 | 100% [98, 100] | 0% | 0% |

## 4. What to check by hand

1. **Spans.** Pick 3 rows of section 5 and open each item in `cases.jsonl` by `id`. Decode `ids` at `sources[<source>]` with the run's tokenizer: `AutoTokenizer.from_pretrained(<repo>, revision=<revision>)`, with both values from `manifest.json`.
   - `lookup_noname` must be the answer's sentence minus exactly its name token(s).
   - `lookup_nodigit` must be the sentence minus exactly its digit.
   - The `lookup_off_*` spans must be the same parts of another sentence. `source_text` gives the intended text.
2. **Destinations.** `dests["final"]` must cover every token after the user turn, including the appended space. `dests["question"]` must cover the question sentence and the instruction.
3. **Labels.** In section 5, `label` must be right exactly when the top token is the answer, and must agree with the run's own `correct` field. The recount found 0 disagreements over the recounted rows of the four runs.
4. **One cell by hand.** Use the snippet in section 3 on memory → prompt, `lookup_noname`, final, and on its control `lookup_off_noname`, final.
5. **Eligibility.** In `cases_report.json`, a family enters a topic iff its competence lower bound is ≥ 0.85 (`gate_lower_bounds`, `families`). Every family should enter every topic, with one exception: on the Qwen3-32B second draw, animals enter for named → prompt only. There the memory → prompt lower bound is 0.8495 (README: missed by 0.0005).

Three dumbest ways this could be wrong:

1. **The spans are not what their names say.** For example, `lookup_noname` also hides part of the name, or misses the digit. → Check 1.
2. **Blocking damages the model rather than removing one read.** → The controls on another sentence keep 99-100% at the same destinations (3b). `check.json` holds the hook's no-op and positive-control checks.
3. **The answer is scored on the wrong token** (e.g. "7" vs " 7"). → Every unedited memory → prompt row is right (300 of 300 on three runs, 199 of 200 on the fourth), so `tok_A` is the token the model actually emits.

## 5. 20 random raw rows

Each table is `random.Random(0).sample` over the rows behind the claim (section 2), in file order. `label` is computed from `top`, `tok_A` and `conf_toks`; `row correct` is the run's own field.

### 5a. Qwen3.6-27B (`d2_parts_v2_27b`)

Run `d2_parts_v2_27b` (Qwen/Qwen3.6-27B), rows.jsonl: population 3000 rows (lookup/final/all 300, lookup/question/all 300, lookup_nodigit/final/all 300, lookup_nodigit/question/all 300, lookup_noname/final/all 300, lookup_noname/question/all 300, lookup_off_nodigit/final/all 300, lookup_off_nodigit/question/all 300, lookup_off_noname/final/all 300, lookup_off_noname/question/all 300); `random.Random(0).sample(population, 20)` in file order. The prompt column is the user turn: the list (cut at 300 characters), then the question; the instruction "Answer with a single word and nothing else." after the question and the chat template around the turn are left out. Regenerate: `uv run python scripts/verification_packets.py rows --finding 3 --run d2_parts_v2_27b`.

| # | item id | prompt (list / question) | hidden span | from | layers | top token | answer | label | row `correct` |
|---|---|---|---|---|---|---|---|---|---|
| 1 | body-RL-e5f0-0061 | The chart on the wrist is kept in folder 8. The chart on the stomach is kept in folder 6. The chart on the liver is kept in folder 3. The chart on the eyebrow is kept in folder 4. The chart on the heart is kept in folder 7. / In which folder is the chart on the body part above each eye? | `lookup_off_nodigit`: "The chart on the heart is kept in folder 7. without '7'" | final | all | "4" (id 19) | 4 | right | true |
| 2 | body-RL-e5f0-0077 | The chart on the knee is kept in folder 3. The chart on the bladder is kept in folder 4. The chart on the brain is kept in folder 6. The chart on the ankle is kept in folder 5. The chart on the skull is kept in folder 9. / What folder keeps the chart on the body part joining foot and leg? | `lookup_nodigit`: "The chart on the ankle is kept in folder 5. without '5'" | question | all | "3" (id 18) | 5 | list | false |
| 3 | animals-RL-e5f0-0017 | Locker 5 belongs to the deer. Locker 3 belongs to the dog. Locker 1 belongs to the fish. Locker 7 belongs to the turkey. Locker 6 belongs to the worm. / Which locker belongs to the animal known for barking? | `lookup_noname`: "Locker 3 belongs to the dog. without 'dog'" | final | all | "2" (id 17) | 3 | off | false |
| 4 | body-RL-e5f0-0006 | The chart on the wrist is kept in folder 5. The chart on the ear is kept in folder 3. The chart on the eyebrow is kept in folder 7. The chart on the ankle is kept in folder 9. The chart on the heart is kept in folder 6. / In which folder is the chart on the body part above each eye? | `lookup`: "The chart on the eyebrow is kept in folder 7." | question | all | "7" (id 22) | 7 | right | true |
| 5 | countries-RL-e5f0-0009 | The China file is in drawer 1. The Germany file is in drawer 9. The Canada file is in drawer 7. The Peru file is in drawer 8. The Thailand file is in drawer 2. / Which drawer holds the file on the country whose capital is Berlin? | `lookup_noname`: "The Germany file is in drawer 9. without 'Germany'" | question | all | "9" (id 24) | 9 | right | true |
| 6 | body-RL-e5f0-0105 | Folder 6 holds the stomach chart. Folder 5 holds the brain chart. Folder 3 holds the forehead chart. Folder 4 holds the ear chart. Folder 7 holds the liver chart. / In which folder is the chart on the body part above the eyebrows? | `lookup`: "Folder 3 holds the forehead chart." | question | all | "5" (id 20) | 3 | list | false |
| 7 | body-RL-e5f0-0069 | The chart on the stomach is kept in folder 7. The chart on the forehead is kept in folder 6. The chart on the skull is kept in folder 8. The chart on the elbow is kept in folder 3. The chart on the bladder is kept in folder 9. / Which folder holds the chart on the body part that bends the arm? | `lookup_off_noname`: "The chart on the stomach is kept in folder 7. without 'stomach'" | question | all | "3" (id 18) | 3 | right | true |
| 8 | body-RL-e5f0-0024 | Folder 9 holds the eyebrow chart. Folder 6 holds the knee chart. Folder 4 holds the skull chart. Folder 5 holds the ankle chart. Folder 3 holds the elbow chart. / Which folder holds the chart on the body part that bends the leg? | `lookup_nodigit`: "Folder 6 holds the knee chart. without '6'" | question | all | "5" (id 20) | 6 | list | false |
| 9 | body-RL-e5f0-0101 | The chart on the knee is kept in folder 8. The chart on the stomach is kept in folder 3. The chart on the liver is kept in folder 4. The chart on the forehead is kept in folder 7. The chart on the eyebrow is kept in folder 9. / What folder keeps the chart on the body part above each eye? | `lookup_nodigit`: "The chart on the eyebrow is kept in folder 9. without '9'" | question | all | "7" (id 22) | 9 | list | false |
| 10 | body-RL-e5f0-0048 | The spine chart is in folder 4. The tongue chart is in folder 7. The heart chart is in folder 6. The ear chart is in folder 8. The ankle chart is in folder 3. / In which folder is the chart on the body part that hears sounds? | `lookup_off_nodigit`: "The tongue chart is in folder 7. without '7'" | question | all | "8" (id 23) | 8 | right | true |
| 11 | countries-RL-e5f0-0039 | The Greece file is in drawer 2. The Iran file is in drawer 5. The Poland file is in drawer 1. The Austria file is in drawer 8. The France file is in drawer 7. / Which drawer holds the file on the country whose capital is Paris? | `lookup_off_noname`: "The Iran file is in drawer 5. without 'Iran'" | final | all | "7" (id 22) | 7 | right | true |
| 12 | animals-RL-e5f0-0091 | Locker 2 belongs to the mouse. Locker 9 belongs to the dog. Locker 7 belongs to the sheep. Locker 1 belongs to the spider. Locker 3 belongs to the moth. / Which locker belongs to the animal known for spinning webs? | `lookup_noname`: "Locker 1 belongs to the spider. without 'spider'" | question | all | "1" (id 16) | 1 | right | true |
| 13 | countries-RL-e5f0-0006 | The Turkey file is in drawer 1. The Egypt file is in drawer 9. The Japan file is in drawer 6. The Hungary file is in drawer 4. The Spain file is in drawer 7. / In which drawer is the file on the country whose capital is Cairo? | `lookup_off_nodigit`: "The Turkey file is in drawer 1. without '1'" | final | all | "9" (id 24) | 9 | right | true |
| 14 | animals-RL-e5f0-0059 | Locker 1 belongs to the elephant. Locker 9 belongs to the bee. Locker 3 belongs to the moth. Locker 5 belongs to the wolf. Locker 8 belongs to the goose. / Which locker belongs to the animal known for howling? | `lookup`: "Locker 5 belongs to the wolf." | question | all | "5" (id 20) | 5 | right | true |
| 15 | body-RL-e5f0-0015 | The stomach chart is in folder 8. The tongue chart is in folder 5. The ear chart is in folder 3. The brain chart is in folder 9. The liver chart is in folder 4. / Which folder holds the chart on the body part that makes bile? | `lookup_noname`: "The liver chart is in folder 4. without 'liver'" | question | all | "4" (id 19) | 4 | right | true |
| 16 | animals-RL-e5f0-0059 | Locker 1 belongs to the elephant. Locker 9 belongs to the bee. Locker 3 belongs to the moth. Locker 5 belongs to the wolf. Locker 8 belongs to the goose. / Which locker belongs to the animal known for howling? | `lookup_nodigit`: "Locker 5 belongs to the wolf. without '5'" | question | all | "5" (id 20) | 5 | right | true |
| 17 | animals-RL-e5f0-0039 | Locker 5 belongs to the rabbit. Locker 9 belongs to the ant. Locker 8 belongs to the tiger. Locker 1 belongs to the crow. Locker 7 belongs to the snake. / Which locker belongs to the animal known for its anthills? | `lookup_off_noname`: "Locker 5 belongs to the rabbit. without 'rabbit'" | question | all | "9" (id 24) | 9 | right | true |
| 18 | countries-RL-e5f0-0054 | The China file is in drawer 5. The Egypt file is in drawer 6. The Lebanon file is in drawer 8. The Spain file is in drawer 1. The Chile file is in drawer 7. / What drawer keeps the file on the country whose capital is Madrid? | `lookup_nodigit`: "The Spain file is in drawer 1. without '1'" | question | all | "1" (id 16) | 1 | right | true |
| 19 | body-RL-e5f0-0002 | The elbow chart is in folder 4. The skull chart is in folder 9. The stomach chart is in folder 5. The eye chart is in folder 8. The bladder chart is in folder 7. / In which folder is the chart on the body part that digests food? | `lookup_off_nodigit`: "The skull chart is in folder 9. without '9'" | question | all | "5" (id 20) | 5 | right | true |
| 20 | countries-RL-e5f0-0018 | The France file is in drawer 4. The Syria file is in drawer 6. The Venezuela file is in drawer 1. The Finland file is in drawer 2. The Peru file is in drawer 7. / Which drawer holds the file on the country whose capital is Lima? | `lookup`: "The Peru file is in drawer 7." | final | all | "1" (id 16) | 7 | list | false |

### 5b. Qwen3-32B (`qwen3_32b_d2_parts_v2`)

Run `qwen3_32b_d2_parts_v2` (Qwen/Qwen3-32B), rows.jsonl: population 3000 rows (lookup/final/all 300, lookup/question/all 300, lookup_nodigit/final/all 300, lookup_nodigit/question/all 300, lookup_noname/final/all 300, lookup_noname/question/all 300, lookup_off_nodigit/final/all 300, lookup_off_nodigit/question/all 300, lookup_off_noname/final/all 300, lookup_off_noname/question/all 300); `random.Random(0).sample(population, 20)` in file order. The prompt column is the user turn: the list (cut at 300 characters), then the question; the instruction "Answer with a single word and nothing else." after the question and the chat template around the turn are left out. Regenerate: `uv run python scripts/verification_packets.py rows --finding 3 --run qwen3_32b_d2_parts_v2`.

| # | item id | prompt (list / question) | hidden span | from | layers | top token | answer | label | row `correct` |
|---|---|---|---|---|---|---|---|---|---|
| 1 | body-RL-e5f0-0064 | The chart on the knee is kept in folder 7. The chart on the skull is kept in folder 8. The chart on the ear is kept in folder 9. The chart on the spine is kept in folder 5. The chart on the brain is kept in folder 6. / What folder keeps the chart on the body part that does the thinking? | `lookup_off_nodigit`: "The chart on the ear is kept in folder 9. without '9'" | final | all | "6" (id 21) | 6 | right | true |
| 2 | body-RL-e5f0-0085 | Folder 7 holds the stomach chart. Folder 3 holds the ear chart. Folder 5 holds the wrist chart. Folder 9 holds the knee chart. Folder 6 holds the bladder chart. / Which folder holds the chart on the body part that hears sounds? | `lookup_nodigit`: "Folder 3 holds the ear chart. without '3'" | question | all | "7" (id 22) | 3 | list | false |
| 3 | animals-RL-e5f0-0024 | Locker 2 belongs to the snake. Locker 5 belongs to the ant. Locker 3 belongs to the rabbit. Locker 1 belongs to the wolf. Locker 7 belongs to the worm. / Which locker belongs to the animal known for its long ears? | `lookup_noname`: "Locker 3 belongs to the rabbit. without 'rabbit'" | final | all | "5" (id 20) | 3 | list | false |
| 4 | body-RL-e5f0-0006 | The chart on the wrist is kept in folder 5. The chart on the ear is kept in folder 3. The chart on the eyebrow is kept in folder 7. The chart on the ankle is kept in folder 9. The chart on the heart is kept in folder 6. / In which folder is the chart on the body part above each eye? | `lookup`: "The chart on the eyebrow is kept in folder 7." | question | all | "3" (id 18) | 7 | list | false |
| 5 | countries-RL-e5f0-0009 | The China file is in drawer 1. The Germany file is in drawer 9. The Canada file is in drawer 7. The Peru file is in drawer 8. The Thailand file is in drawer 2. / Which drawer holds the file on the country whose capital is Berlin? | `lookup_noname`: "The Germany file is in drawer 9. without 'Germany'" | question | all | "9" (id 24) | 9 | right | true |
| 6 | body-RL-e5f0-0117 | The ear chart is in folder 9. The knee chart is in folder 6. The spine chart is in folder 5. The liver chart is in folder 3. The skull chart is in folder 4. / Which folder holds the chart on the body part that protects the brain? | `lookup`: "The skull chart is in folder 4." | question | all | "4" (id 19) | 4 | right | true |
| 7 | body-RL-e5f0-0076 | Folder 8 holds the elbow chart. Folder 4 holds the skull chart. Folder 9 holds the wrist chart. Folder 5 holds the liver chart. Folder 6 holds the eye chart. / What folder keeps the chart on the body part that sees colours? | `lookup_off_noname`: "Folder 8 holds the elbow chart. without 'elbow'" | question | all | "6" (id 21) | 6 | right | true |
| 8 | body-RL-e5f0-0026 | The heart chart is in folder 5. The eyebrow chart is in folder 3. The spine chart is in folder 7. The elbow chart is in folder 6. The skull chart is in folder 4. / What folder keeps the chart on the body part above each eye? | `lookup_nodigit`: "The eyebrow chart is in folder 3. without '3'" | question | all | "4" (id 19) | 3 | list | false |
| 9 | body-RL-e5f0-0112 | The chart on the stomach is kept in folder 8. The chart on the skull is kept in folder 5. The chart on the ear is kept in folder 7. The chart on the heart is kept in folder 3. The chart on the spine is kept in folder 6. / Which folder holds the chart on the body part that pumps blood? | `lookup_nodigit`: "The chart on the heart is kept in folder 3. without '3'" | question | all | "3" (id 18) | 3 | right | true |
| 10 | body-RL-e5f0-0052 | Folder 3 holds the bladder chart. Folder 5 holds the brain chart. Folder 4 holds the tongue chart. Folder 9 holds the eye chart. Folder 8 holds the knee chart. / In which folder is the chart on the body part that does the thinking? | `lookup_off_nodigit`: "Folder 9 holds the eye chart. without '9'" | question | all | "5" (id 20) | 5 | right | true |
| 11 | countries-RL-e5f0-0042 | Drawer 8 holds the Poland file. Drawer 3 holds the Peru file. Drawer 1 holds the Pakistan file. Drawer 6 holds the Thailand file. Drawer 2 holds the Indonesia file. / Which drawer holds the file on the country whose capital is Islamabad? | `lookup_off_noname`: "Drawer 3 holds the Peru file. without 'Peru'" | final | all | "1" (id 16) | 1 | right | true |
| 12 | animals-RL-e5f0-0117 | The wolf's locker is 8. The owl's locker is 1. The camel's locker is 3. The mosquito's locker is 5. The whale's locker is 7. / What locker is used by the animal known for spouting water? | `lookup_noname`: "The whale's locker is 7. without 'whale'" | question | all | "7" (id 22) | 7 | right | true |
| 13 | countries-RL-e5f0-0006 | The Turkey file is in drawer 1. The Egypt file is in drawer 9. The Japan file is in drawer 6. The Hungary file is in drawer 4. The Spain file is in drawer 7. / In which drawer is the file on the country whose capital is Cairo? | `lookup_off_nodigit`: "The Turkey file is in drawer 1. without '1'" | final | all | "9" (id 24) | 9 | right | true |
| 14 | animals-RL-e5f0-0078 | The moth keeps its things in locker 3. The goose keeps its things in locker 9. The eagle keeps its things in locker 8. The cow keeps its things in locker 7. The goat keeps its things in locker 5. / In which locker does the animal known for its talons keep its things? | `lookup`: "The eagle keeps its things in locker 8." | question | all | "9" (id 24) | 8 | list | false |
| 15 | body-RL-e5f0-0016 | Folder 6 holds the tongue chart. Folder 4 holds the skull chart. Folder 7 holds the eyebrow chart. Folder 3 holds the wrist chart. Folder 9 holds the forehead chart. / Which folder holds the chart on the body part joining hand and arm? | `lookup_noname`: "Folder 3 holds the wrist chart. without 'wrist'" | question | all | "3" (id 18) | 3 | right | true |
| 16 | animals-RL-e5f0-0078 | The moth keeps its things in locker 3. The goose keeps its things in locker 9. The eagle keeps its things in locker 8. The cow keeps its things in locker 7. The goat keeps its things in locker 5. / In which locker does the animal known for its talons keep its things? | `lookup_nodigit`: "The eagle keeps its things in locker 8. without '8'" | question | all | "9" (id 24) | 8 | list | false |
| 17 | animals-RL-e5f0-0051 | Locker 8 belongs to the cow. Locker 3 belongs to the butterfly. Locker 7 belongs to the sheep. Locker 2 belongs to the fish. Locker 1 belongs to the deer. / What locker is used by the animal known for its antlers? | `lookup_off_noname`: "Locker 3 belongs to the butterfly. without 'butterfly'" | question | all | "1" (id 16) | 1 | right | true |
| 18 | countries-RL-e5f0-0059 | Drawer 1 holds the Japan file. Drawer 7 holds the China file. Drawer 6 holds the Finland file. Drawer 9 holds the France file. Drawer 2 holds the Austria file. / In which drawer is the file on the country whose capital is Helsinki? | `lookup_nodigit`: "Drawer 6 holds the Finland file. without '6'" | question | all | "5" (id 20) | 6 | off | false |
| 19 | body-RL-e5f0-0002 | The elbow chart is in folder 4. The skull chart is in folder 9. The stomach chart is in folder 5. The eye chart is in folder 8. The bladder chart is in folder 7. / In which folder is the chart on the body part that digests food? | `lookup_off_nodigit`: "The skull chart is in folder 9. without '9'" | question | all | "5" (id 20) | 5 | right | true |
| 20 | countries-RL-e5f0-0019 | The file on Cuba is kept in drawer 3. The file on Australia is kept in drawer 2. The file on Spain is kept in drawer 4. The file on Korea is kept in drawer 1. The file on Pakistan is kept in drawer 7. / In which drawer is the file on the country whose capital is Islamabad? | `lookup`: "The file on Pakistan is kept in drawer 7." | final | all | "1" (id 16) | 7 | list | false |
