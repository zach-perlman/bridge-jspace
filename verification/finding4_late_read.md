# Finding 4 hand-check: the lookup ends in a late attention read by the last tokens

For Dan and Zach, to check by hand from Fri 23 Oct. Finding 4 is frozen in [README.md](../README.md) and is not in [VERIFIED.md](../VERIFIED.md): it stays UNVERIFIED until you add it. Every number here is either copied from README.md or recounted from the saved runs README.md cites. Nothing from the night of 22-23 Oct was opened. The recount and raw-row sections are printed by `scripts/verification_packets.py` (read-only, no GPU) and pasted unedited.

## 1. The claim

README, findings table, row 4: **"A lookup ends in a late attention read of the answer's sentence by the last tokens."** Key evidence: "read blocked: 0-9% right on 4 models (guessing 20%), also in tables, JSON and after ~2000 tokens of filler; Gemma 22-23%". How sure: 🟢 two draws of scenes on 5 models; Gemma drops to guessing, not below (misses the 20% bar by 2 points) · frozen.

Slide 3, in short: "stop the last tokens from attending to the answer's sentence and the lookup drops to guessing, on all five models. Only the attention layers matter."

Worked example (item `countries-RL-e5f0-0009`, row 5 of 5a). The list is "The China file is in drawer 1. The Germany file is in drawer 9. The Canada file is in drawer 7. The Peru file is in drawer 8. The Thailand file is in drawer 2." The question is "Which drawer holds the file on the country whose capital is Berlin?", and the answer is 9. In every attention layer, the last tokens are stopped from attending to "The Germany file is in drawer 9." The model then answers 1, China's digit. Guessing among the list's five digits would be right 20% of the time. Row 7 shows the control: the same kind of block in the DeltaNet layers only, where the answer stays right.

How the runs name things:

- **family**: `RL` = memory → prompt (the bridge is recalled from a cue, its digit looked up in the list). `DL` = named → prompt. `RR` = memory → memory (recall). For recall, the hidden sentence is not on the answer's path, so it is a control by construction, not a finding (README weak spot).
- **source** (what is hidden): `lookup` is the answer's sentence. `lookup_off` is another sentence of the list with the same token length (the control).
- **dest**: `final` = every token after the user turn (`<|im_end|>`, the assistant header, the empty think block, `Answer:` and the appended space where the answer is read). This is README's "the last tokens".
- **layers**:
  - `all` = every layer.
  - `attn` = the 16 full-attention layers of Qwen3.6-27B (3, 7, …, 63; manifest `layer_sets`).
  - `gdn` = its 48 DeltaNet layers; blocking there is the control for "only the attention layers matter".
  - Qwen3-32B has attention in every layer, so its runs have `all` only.
- **Blocking**: exact. In attention layers, the dest-to-source attention logits are set to −inf in every head. In DeltaNet layers (mode `value`), the source's values are removed from the dest's output. The first token is never blocked. Indirect routes through other tokens stay open (manifest field `knockout`).
- **Which items count**: only items whose unedited row (`source == "none"`) is right.
- **Labels**: **right** = `top == tok_A`; **list** = another digit of the list (`top in conf_toks`; the run's `conf` field); **off** = anything else.

"Late": on the 27B's first draw the same run also blocks bands of layers (`band00-31`, `band32-47`, `band48-63`, and their `:attn` and `:gdn` parts; rows in the run's `analysis-*/summary.md`). Slide 8's depth figure shows where each model's read sits. README quotes no band numbers, so this packet checks only the cells blocked in every layer.

Decision rules:

- **First draws** (`scripts/attn_knockout.py` docstring, fixed before any 27B run in `jobs/d2/*.yaml`):
  - A cell is NEEDED if accuracy drops ≥ 20 points and the paired bootstrap 95% lower bound of acc(control) − acc(cell) is ≥ 10 points. The control is `lookup_off` at the same destination, layers and mode.
  - It is NOT NEEDED if the Wilson 95% lower bound of its accuracy is ≥ 90%. Otherwise it is PARTIAL.
- **Second draws** (`jobs/d2/d2_late_read_seed2_27b.yaml` and `jobs/d2/qwen3_32b_d2_late_read_seed2.yaml`, fixed on 22 Oct before the runs). Scope: memory → prompt, topics pooled, items right unedited. The result replicates iff all of these hold:
  - the answer's sentence hidden from the last tokens in every attention layer leaves ≤ 20% right (point) with Wilson upper bound ≤ 30%;
  - the other sentence hidden there keeps ≥ 90% right (Wilson lower bound ≥ 85%);
  - on the 27B only, hiding the answer's sentence in every DeltaNet layer instead keeps ≥ 90% right.

## 2. Result files and rows

| Model | Draw (data) | Run folder | Saved analysis | Memory → prompt items | In this packet |
|---|---|---|---|---|---|
| Qwen3.6-27B (revision 6a9e13bd) | first (`data/pointer_v4/main`) | `results/attn_knockout/d2_v4_late_read/` | `analysis-20261021T200355Z/summary.md` | 300 | main run: recount and 20 raw rows |
| Qwen3.6-27B | second (`data/pointer_v4/seed2`) | `results/attn_knockout/d2_late_read_seed2_27b/` | `analysis-20261022T171236Z/summary.md` | 300 | recount |
| Qwen3-32B (revision 9216db57) | first (`main`) | `results/attn_knockout/qwen3_32b_d2_v4_late_read_v2_r2/` | `analysis-20261022T121815Z/summary.md` (analysed locally, README note) | 300 | recount and 20 raw rows |
| Qwen3-32B | second (`seed2`) | `results/attn_knockout/qwen3_32b_d2_late_read_seed2/` | `analysis-20261022T171213Z/summary.md` | 299 of 300 right unedited | recount |

n: 100 scenes per topic and family, three topics (countries, animals, body parts). Seeds: the scenes come from the data set's own draw (main or seed2); the control spans use seed 0 and the bootstrap seed 0 (manifest `seeds`).

The files are the same as for finding 3: `manifest.json`, `cases.jsonl`, `rows.jsonl`, `check.json` and `cases_report.json`. Here the run's own analysis sits in `analysis-*/summary.md` and `.json`.

Rows behind the claim, in `rows.jsonl`:

- `family == "RL"`, `source == "lookup"`, `dest == "final"`, `layers == "all"` and `mode == "value"`. On the 27B, the second draw's pre-registered cell is `layers == "attn"`; on the first draw it gives the same 9%.
- Controls:
  - `source == "lookup_off"` with the same filter;
  - on the 27B, `source == "lookup"` with `layers == "gdn"`;
  - on the 27B's first draw, `family == "RR"` (recall).
- Only items whose `source == "none"` row has `correct == true`.

Not in this packet, and not opened for it:

- Qwen3.5-9B, OLMo-3-7B and Gemma 4: `qwen35_9b_d2_v4_late_read_r2`, `olmo3_7b_{instruct,sft,dpo}_d2_v4_late_read_*`, `gemma4it_d2_v4_late_read_v3_r2`, and the `*_d2_late_read_seed2` runs of those three.
- Tables and JSON (`d2_formats_27b`, `qwen3_32b_d2_formats`, scored by `scripts/d2_formats.py`).
- The long context (`qwen35_9b_d2_late_read_long`).
- The random-damage control (`primacy_noise/d2_primacy_noise_27b`; README: not testable).

## 3. Recompute

Run everything from the repo root. No GPU is needed.

1. The run's own analysis: `uv run python scripts/attn_knockout.py summarise --name d2_v4_late_read`, then the same for `d2_late_read_seed2_27b`, `qwen3_32b_d2_v4_late_read_v2_r2` and `qwen3_32b_d2_late_read_seed2`. It writes a new `analysis-<UTC stamp>/` folder (`summary.md`, `summary.json`) inside the run folder; nothing is overwritten. The headline is the row `| RL | lookup | final | all | value | …`. I did not run it while preparing this packet, to add nothing to results/.
2. An independent, read-only recount from rows.jsonl and cases.jsonl: `uv run python scripts/verification_packets.py headline --finding 4 --run d2_v4_late_read`, and the same for the other three runs. Its output is in 3b. While preparing this packet, every line of it was compared by script with the saved `analysis-*/summary.md` named above: n, rate, Wilson interval and the share of other list digits ("confusion") agree on all lines of the four runs.
3. By hand, with plain python3 (no repo code), from the repo root:

```python
import json

run = "results/attn_knockout/d2_v4_late_read"
rows = [json.loads(line) for line in open(f"{run}/rows.jsonl")]
cases = {c["id"]: c for c in map(json.loads, open(f"{run}/cases.jsonl"))}
ok = {(r["family"], r["id"]) for r in rows if r["source"] == "none" and r["correct"]}
for fam, src, layers in (
    ("RL", "lookup", "all"),
    ("RL", "lookup", "attn"),
    ("RL", "lookup_off", "all"),
    ("RL", "lookup", "gdn"),
    ("RR", "lookup", "all"),
):
    sel = [
        r
        for r in rows
        if r["family"] == fam
        and (fam, r["id"]) in ok
        and r["dest"] == "final"
        and r["mode"] == "value"
        and r["source"] == src
        and r["layers"] == layers
    ]
    right = sum(r["top"] == cases[r["id"]]["tok_A"] for r in sel)
    other_digit = sum(r["top"] in cases[r["id"]]["conf_toks"] for r in sel)
    print(
        f"{fam} {src:10s} {layers:4s} n={len(sel)} right={right} ({100 * right / len(sel):.0f}%) "
        f"another list digit={other_digit}"
    )
```

Expected output on `d2_v4_late_read`:

- `RL lookup all n=300 right=26 (9%) another list digit=265`
- `RL lookup attn n=300 right=26 (9%) another list digit=263`
- `RL lookup_off all n=300 right=300 (100%)`
- `RL lookup gdn n=300 right=300 (100%)`
- `RR lookup all n=300 right=298 (99%)`

### 3a. Expected numbers, as README states them

- **Answer's sentence hidden from the last tokens, memory → prompt:**
  - Qwen3.6-27B: 9% right on the first draw, 7% [5, 11] on the second;
  - Qwen3-32B: 3% on the first draw, 3% [2, 6] on the second;
  - guessing: 20%.
- **Another sentence hidden instead:** 100% right on every model.
- **DeltaNet layers blocked instead** (Qwen3.6-27B, both draws): 100%.
- **Where the wrong answers go:** 72-96% to another digit of the list (range over the five models).
- **Recall** (Qwen3.6-27B, memory → memory): stays right, 99%, by construction.
- **Verdicts:** on the first draws, the cell (memory → prompt, `lookup`, `final`, `all`) is NEEDED on both models; this is the last column of that row in the saved `summary.md`. README's "Done" table, on the second draws: "Both hold, on both models".

### 3b. Recount from rows.jsonl (pasted output)

**Qwen3.6-27B, first draw**

Run `d2_v4_late_read`: items per family {'DL': 300, 'RL': 300, 'RR': 300}, right unedited {'DL': 300, 'RL': 300, 'RR': 300}; rows where right (top = tok_A) and the row's `correct` disagree: 0.

| family | hidden | from | layers | n | right | right [Wilson 95%] | another list digit | off the list |
|---|---|---|---|---|---|---|---|---|
| DL | lookup | final | all | 300 | 36 | 12% [9, 16] | 81% | 7% |
| DL | lookup | final | attn | 300 | 34 | 11% [8, 15] | 81% | 8% |
| DL | lookup | final | gdn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off | final | attn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| DL | lookup_off | final | gdn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup | final | all | 300 | 26 | 9% [6, 12] | 88% | 3% |
| RL | lookup | final | attn | 300 | 26 | 9% [6, 12] | 88% | 4% |
| RL | lookup | final | gdn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off | final | attn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off | final | gdn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RR | lookup | final | all | 300 | 298 | 99% [98, 100] | 1% | 0% |
| RR | lookup | final | attn | 300 | 297 | 99% [97, 100] | 1% | 0% |
| RR | lookup | final | gdn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RR | lookup_off | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RR | lookup_off | final | attn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RR | lookup_off | final | gdn | 300 | 300 | 100% [99, 100] | 0% | 0% |

**Qwen3.6-27B, second draw**

Run `d2_late_read_seed2_27b`: items per family {'RL': 300}, right unedited {'RL': 300}; rows where right (top = tok_A) and the row's `correct` disagree: 0.

| family | hidden | from | layers | n | right | right [Wilson 95%] | another list digit | off the list |
|---|---|---|---|---|---|---|---|---|
| RL | lookup | final | all | 300 | 22 | 7% [5, 11] | 89% | 4% |
| RL | lookup | final | attn | 300 | 22 | 7% [5, 11] | 88% | 4% |
| RL | lookup | final | gdn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off | final | attn | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup_off | final | gdn | 300 | 300 | 100% [99, 100] | 0% | 0% |

**Qwen3-32B, first draw**

Run `qwen3_32b_d2_v4_late_read_v2_r2`: items per family {'DL': 300, 'RL': 300}, right unedited {'DL': 300, 'RL': 300}; rows where right (top = tok_A) and the row's `correct` disagree: 0.

| family | hidden | from | layers | n | right | right [Wilson 95%] | another list digit | off the list |
|---|---|---|---|---|---|---|---|---|
| DL | lookup | final | all | 300 | 9 | 3% [2, 6] | 95% | 2% |
| DL | lookup_off | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |
| RL | lookup | final | all | 300 | 10 | 3% [2, 6] | 93% | 4% |
| RL | lookup_off | final | all | 300 | 300 | 100% [99, 100] | 0% | 0% |

**Qwen3-32B, second draw**

Run `qwen3_32b_d2_late_read_seed2`: items per family {'RL': 300}, right unedited {'RL': 299}; rows where right (top = tok_A) and the row's `correct` disagree: 0.

| family | hidden | from | layers | n | right | right [Wilson 95%] | another list digit | off the list |
|---|---|---|---|---|---|---|---|---|
| RL | lookup | final | all | 299 | 10 | 3% [2, 6] | 94% | 3% |
| RL | lookup_off | final | all | 299 | 299 | 100% [99, 100] | 0% | 0% |

## 4. What to check by hand

1. **The block.** Read the manifest's `knockout` text. In `check.json`:
   - `noop_empty_source_max_abs` should be 0 (an empty block changes nothing);
   - the `posctl_*` fields are the hook's positive controls;
   - `passed` should be true.
2. **Layer sets.** In the 27B manifest, `layer_sets.attn` must be exactly the layers whose `layer_kinds` entry is `full_attention`, and `layer_sets.gdn` exactly the `linear_attention` ones.
3. **Destinations and spans.** For 3 rows of section 5, open the item in `cases.jsonl` by `id`:
   - `dests["final"]` must cover every token after the user turn, including the appended space;
   - `sources["lookup"]` must decode to the answer's sentence;
   - `sources["lookup_off"]` must decode to another sentence of the same token length.
4. **Labels.** In section 5, `label` must be right exactly when the top token is the answer, and must agree with the run's `correct` field. The recount found 0 disagreements over the recounted rows of the four runs.
5. **One cell by hand.** Use the snippet in section 3, and compare the two `summarise` outputs if you run them.

Three dumbest ways this could be wrong:

1. **Blocking breaks the model in general, not one read.** → The other sentence blocked at the same layers keeps 100%. On the 27B, blocking the answer's sentence in the DeltaNet layers also keeps 100%.
2. **"Drops to guessing" is really a collapse onto one fixed answer or off the list.** → Most wrong answers are other digits of the list (88% on the 27B, 93% on the 32B; column "another list digit" in 3b). README's note that they favour the 1st sentence on the 27B was dropped from the story; its control was not testable.
3. **The DeltaNet layers do not matter only because the prompts are short.** → Not tested by these runs. README: the long-context run on Qwen3.5-9B holds; Qwen3.6-27B was still running. Not opened for this packet.

## 5. 20 random raw rows

Each table is `random.Random(0).sample` over the rows behind the claim and their controls, in file order: (`lookup` or `lookup_off`) × (`all` or `attn`), plus (`lookup`, `gdn`) on the 27B; dest `final`; memory → prompt. `label` is computed from `top`, `tok_A` and `conf_toks`; `row correct` is the run's own field.

### 5a. Qwen3.6-27B (`d2_v4_late_read`)

Run `d2_v4_late_read` (Qwen/Qwen3.6-27B), rows.jsonl: population 1500 rows (lookup/final/all 300, lookup/final/attn 300, lookup/final/gdn 300, lookup_off/final/all 300, lookup_off/final/attn 300); `random.Random(0).sample(population, 20)` in file order. The prompt column is the user turn: the list (cut at 300 characters), then the question; the instruction "Answer with a single word and nothing else." after the question and the chat template around the turn are left out. Regenerate: `uv run python scripts/verification_packets.py rows --finding 4 --run d2_v4_late_read`.

| # | item id | prompt (list / question) | hidden span | from | layers | top token | answer | label | row `correct` |
|---|---|---|---|---|---|---|---|---|---|
| 1 | body-RL-e5f0-0061 | The chart on the wrist is kept in folder 8. The chart on the stomach is kept in folder 6. The chart on the liver is kept in folder 3. The chart on the eyebrow is kept in folder 4. The chart on the heart is kept in folder 7. / In which folder is the chart on the body part above each eye? | `lookup_off`: "The chart on the heart is kept in folder 7." | final | attn | "4" (id 19) | 4 | right | true |
| 2 | body-RL-e5f0-0077 | The chart on the knee is kept in folder 3. The chart on the bladder is kept in folder 4. The chart on the brain is kept in folder 6. The chart on the ankle is kept in folder 5. The chart on the skull is kept in folder 9. / What folder keeps the chart on the body part joining foot and leg? | `lookup_off`: "The chart on the skull is kept in folder 9." | final | all | "5" (id 20) | 5 | right | true |
| 3 | animals-RL-e5f0-0017 | Locker 5 belongs to the deer. Locker 3 belongs to the dog. Locker 1 belongs to the fish. Locker 7 belongs to the turkey. Locker 6 belongs to the worm. / Which locker belongs to the animal known for barking? | `lookup`: "Locker 3 belongs to the dog." | final | attn | "5" (id 20) | 3 | list | false |
| 4 | body-RL-e5f0-0006 | The chart on the wrist is kept in folder 5. The chart on the ear is kept in folder 3. The chart on the eyebrow is kept in folder 7. The chart on the ankle is kept in folder 9. The chart on the heart is kept in folder 6. / In which folder is the chart on the body part above each eye? | `lookup`: "The chart on the eyebrow is kept in folder 7." | final | all | "5" (id 20) | 7 | list | false |
| 5 | countries-RL-e5f0-0009 | The China file is in drawer 1. The Germany file is in drawer 9. The Canada file is in drawer 7. The Peru file is in drawer 8. The Thailand file is in drawer 2. / Which drawer holds the file on the country whose capital is Berlin? | `lookup`: "The Germany file is in drawer 9." | final | attn | "1" (id 16) | 9 | list | false |
| 6 | body-RL-e5f0-0105 | Folder 6 holds the stomach chart. Folder 5 holds the brain chart. Folder 3 holds the forehead chart. Folder 4 holds the ear chart. Folder 7 holds the liver chart. / In which folder is the chart on the body part above the eyebrows? | `lookup`: "Folder 3 holds the forehead chart." | final | all | "5" (id 20) | 3 | list | false |
| 7 | body-RL-e5f0-0069 | The chart on the stomach is kept in folder 7. The chart on the forehead is kept in folder 6. The chart on the skull is kept in folder 8. The chart on the elbow is kept in folder 3. The chart on the bladder is kept in folder 9. / Which folder holds the chart on the body part that bends the arm? | `lookup`: "The chart on the elbow is kept in folder 3." | final | gdn | "3" (id 18) | 3 | right | true |
| 8 | body-RL-e5f0-0024 | Folder 9 holds the eyebrow chart. Folder 6 holds the knee chart. Folder 4 holds the skull chart. Folder 5 holds the ankle chart. Folder 3 holds the elbow chart. / Which folder holds the chart on the body part that bends the leg? | `lookup_off`: "Folder 3 holds the elbow chart." | final | all | "6" (id 21) | 6 | right | true |
| 9 | body-RL-e5f0-0101 | The chart on the knee is kept in folder 8. The chart on the stomach is kept in folder 3. The chart on the liver is kept in folder 4. The chart on the forehead is kept in folder 7. The chart on the eyebrow is kept in folder 9. / What folder keeps the chart on the body part above each eye? | `lookup_off`: "The chart on the forehead is kept in folder 7." | final | all | "9" (id 24) | 9 | right | true |
| 10 | body-RL-e5f0-0048 | The spine chart is in folder 4. The tongue chart is in folder 7. The heart chart is in folder 6. The ear chart is in folder 8. The ankle chart is in folder 3. / In which folder is the chart on the body part that hears sounds? | `lookup_off`: "The tongue chart is in folder 7." | final | attn | "8" (id 23) | 8 | right | true |
| 11 | countries-RL-e5f0-0039 | The Greece file is in drawer 2. The Iran file is in drawer 5. The Poland file is in drawer 1. The Austria file is in drawer 8. The France file is in drawer 7. / Which drawer holds the file on the country whose capital is Paris? | `lookup`: "The France file is in drawer 7." | final | gdn | "7" (id 22) | 7 | right | true |
| 12 | animals-RL-e5f0-0091 | Locker 2 belongs to the mouse. Locker 9 belongs to the dog. Locker 7 belongs to the sheep. Locker 1 belongs to the spider. Locker 3 belongs to the moth. / Which locker belongs to the animal known for spinning webs? | `lookup`: "Locker 1 belongs to the spider." | final | attn | "3" (id 18) | 1 | list | false |
| 13 | countries-RL-e5f0-0006 | The Turkey file is in drawer 1. The Egypt file is in drawer 9. The Japan file is in drawer 6. The Hungary file is in drawer 4. The Spain file is in drawer 7. / In which drawer is the file on the country whose capital is Cairo? | `lookup_off`: "The Turkey file is in drawer 1." | final | attn | "9" (id 24) | 9 | right | true |
| 14 | animals-RL-e5f0-0059 | Locker 1 belongs to the elephant. Locker 9 belongs to the bee. Locker 3 belongs to the moth. Locker 5 belongs to the wolf. Locker 8 belongs to the goose. / Which locker belongs to the animal known for howling? | `lookup`: "Locker 5 belongs to the wolf." | final | all | "3" (id 18) | 5 | list | false |
| 15 | body-RL-e5f0-0015 | The stomach chart is in folder 8. The tongue chart is in folder 5. The ear chart is in folder 3. The brain chart is in folder 9. The liver chart is in folder 4. / Which folder holds the chart on the body part that makes bile? | `lookup`: "The liver chart is in folder 4." | final | attn | "8" (id 23) | 4 | list | false |
| 16 | animals-RL-e5f0-0059 | Locker 1 belongs to the elephant. Locker 9 belongs to the bee. Locker 3 belongs to the moth. Locker 5 belongs to the wolf. Locker 8 belongs to the goose. / Which locker belongs to the animal known for howling? | `lookup_off`: "Locker 9 belongs to the bee." | final | all | "5" (id 20) | 5 | right | true |
| 17 | animals-RL-e5f0-0039 | Locker 5 belongs to the rabbit. Locker 9 belongs to the ant. Locker 8 belongs to the tiger. Locker 1 belongs to the crow. Locker 7 belongs to the snake. / Which locker belongs to the animal known for its anthills? | `lookup`: "Locker 9 belongs to the ant." | final | gdn | "9" (id 24) | 9 | right | true |
| 18 | countries-RL-e5f0-0054 | The China file is in drawer 5. The Egypt file is in drawer 6. The Lebanon file is in drawer 8. The Spain file is in drawer 1. The Chile file is in drawer 7. / What drawer keeps the file on the country whose capital is Madrid? | `lookup_off`: "The Lebanon file is in drawer 8." | final | all | "1" (id 16) | 1 | right | true |
| 19 | body-RL-e5f0-0002 | The elbow chart is in folder 4. The skull chart is in folder 9. The stomach chart is in folder 5. The eye chart is in folder 8. The bladder chart is in folder 7. / In which folder is the chart on the body part that digests food? | `lookup_off`: "The skull chart is in folder 9." | final | attn | "5" (id 20) | 5 | right | true |
| 20 | countries-RL-e5f0-0018 | The France file is in drawer 4. The Syria file is in drawer 6. The Venezuela file is in drawer 1. The Finland file is in drawer 2. The Peru file is in drawer 7. / Which drawer holds the file on the country whose capital is Lima? | `lookup`: "The Peru file is in drawer 7." | final | all | "1" (id 16) | 7 | list | false |

### 5b. Qwen3-32B (`qwen3_32b_d2_v4_late_read_v2_r2`)

Run `qwen3_32b_d2_v4_late_read_v2_r2` (Qwen/Qwen3-32B), rows.jsonl: population 600 rows (lookup/final/all 300, lookup_off/final/all 300); `random.Random(0).sample(population, 20)` in file order. The prompt column is the user turn: the list (cut at 300 characters), then the question; the instruction "Answer with a single word and nothing else." after the question and the chat template around the turn are left out. Regenerate: `uv run python scripts/verification_packets.py rows --finding 4 --run qwen3_32b_d2_v4_late_read_v2_r2`.

| # | item id | prompt (list / question) | hidden span | from | layers | top token | answer | label | row `correct` |
|---|---|---|---|---|---|---|---|---|---|
| 1 | body-RL-e5f0-0114 | The chart on the skull is kept in folder 6. The chart on the knee is kept in folder 7. The chart on the stomach is kept in folder 8. The chart on the ear is kept in folder 4. The chart on the bladder is kept in folder 5. / In which folder is the chart on the body part that bends the leg? | `lookup`: "The chart on the knee is kept in folder 7." | final | all | "6" (id 21) | 7 | list | false |
| 2 | countries-RL-e5f0-0016 | The file on Portugal is kept in drawer 5. The file on Austria is kept in drawer 9. The file on Italy is kept in drawer 2. The file on Spain is kept in drawer 8. The file on Philippines is kept in drawer 7. / In which drawer is the file on the country whose capital is Vienna? | `lookup`: "The file on Austria is kept in drawer 9." | final | all | "5" (id 20) | 9 | list | false |
| 3 | animals-RL-e5f0-0028 | The cat's locker is 8. The horse's locker is 3. The eagle's locker is 7. The duck's locker is 1. The mosquito's locker is 9. / Which locker belongs to the animal known for quacking? | `lookup_off`: "The horse's locker is 3." | final | all | "1" (id 16) | 1 | right | true |
| 4 | body-RL-e5f0-0035 | The chart on the elbow is kept in folder 8. The chart on the ear is kept in folder 7. The chart on the forehead is kept in folder 4. The chart on the eye is kept in folder 6. The chart on the wrist is kept in folder 9. / Which folder holds the chart on the body part above the eyebrows? | `lookup_off`: "The chart on the eye is kept in folder 6." | final | all | "4" (id 19) | 4 | right | true |
| 5 | countries-RL-e5f0-0068 | Drawer 6 holds the Korea file. Drawer 3 holds the Kenya file. Drawer 7 holds the Norway file. Drawer 4 holds the Chile file. Drawer 1 holds the Iran file. / Which drawer holds the file on the country whose capital is Tehran? | `lookup_off`: "Drawer 3 holds the Kenya file." | final | all | "1" (id 16) | 1 | right | true |
| 6 | countries-RL-e5f0-0054 | The China file is in drawer 5. The Egypt file is in drawer 6. The Lebanon file is in drawer 8. The Spain file is in drawer 1. The Chile file is in drawer 7. / What drawer keeps the file on the country whose capital is Madrid? | `lookup_off`: "The Lebanon file is in drawer 8." | final | all | "1" (id 16) | 1 | right | true |
| 7 | countries-RL-e5f0-0007 | The file on Egypt is kept in drawer 4. The file on Korea is kept in drawer 7. The file on Iran is kept in drawer 5. The file on Japan is kept in drawer 1. The file on Philippines is kept in drawer 3. / In which drawer is the file on the country whose capital is Tehran? | `lookup`: "The file on Iran is kept in drawer 5." | final | all | "4" (id 19) | 5 | list | false |
| 8 | body-RL-e5f0-0062 | Folder 4 holds the stomach chart. Folder 5 holds the bladder chart. Folder 8 holds the knee chart. Folder 3 holds the skull chart. Folder 9 holds the elbow chart. / In which folder is the chart on the body part that protects the brain? | `lookup`: "Folder 3 holds the skull chart." | final | all | "9" (id 24) | 3 | list | false |
| 9 | countries-RL-e5f0-0048 | Drawer 1 holds the Spain file. Drawer 2 holds the Norway file. Drawer 8 holds the Finland file. Drawer 6 holds the Russia file. Drawer 7 holds the Pakistan file. / What drawer keeps the file on the country whose capital is Oslo? | `lookup`: "Drawer 2 holds the Norway file." | final | all | "2" (id 17) | 2 | right | true |
| 10 | body-RL-e5f0-0098 | The forehead chart is in folder 6. The eye chart is in folder 9. The brain chart is in folder 3. The elbow chart is in folder 4. The skull chart is in folder 5. / What folder keeps the chart on the body part that bends the arm? | `lookup`: "The elbow chart is in folder 4." | final | all | "6" (id 21) | 4 | list | false |
| 11 | countries-RL-e5f0-0113 | The file on Spain is kept in drawer 1. The file on Australia is kept in drawer 4. The file on France is kept in drawer 7. The file on Indonesia is kept in drawer 5. The file on Pakistan is kept in drawer 8. / In which drawer is the file on the country whose capital is Jakarta? | `lookup_off`: "The file on France is kept in drawer 7." | final | all | "5" (id 20) | 5 | right | true |
| 12 | body-RL-e5f0-0011 | Folder 4 holds the tongue chart. Folder 8 holds the skull chart. Folder 6 holds the ear chart. Folder 3 holds the bladder chart. Folder 7 holds the stomach chart. / In which folder is the chart on the body part that tastes food? | `lookup_off`: "Folder 6 holds the ear chart." | final | all | "4" (id 19) | 4 | right | true |
| 13 | countries-RL-e5f0-0065 | Drawer 7 holds the Russia file. Drawer 9 holds the Thailand file. Drawer 5 holds the Canada file. Drawer 4 holds the Egypt file. Drawer 3 holds the Japan file. / What drawer keeps the file on the country whose capital is Bangkok? | `lookup`: "Drawer 9 holds the Thailand file." | final | all | "3" (id 18) | 9 | list | false |
| 14 | animals-RL-e5f0-0098 | The mouse keeps its things in locker 5. The spider keeps its things in locker 6. The frog keeps its things in locker 3. The owl keeps its things in locker 1. The wolf keeps its things in locker 7. / In which locker does the animal known for howling keep its things? | `lookup`: "The wolf keeps its things in locker 7." | final | all | "1" (id 16) | 7 | list | false |
| 15 | body-RL-e5f0-0050 | The elbow chart is in folder 7. The tongue chart is in folder 3. The eyebrow chart is in folder 8. The stomach chart is in folder 4. The eye chart is in folder 6. / In which folder is the chart on the body part that tastes food? | `lookup`: "The tongue chart is in folder 3." | final | all | "4" (id 19) | 3 | list | false |
| 16 | animals-RL-e5f0-0098 | The mouse keeps its things in locker 5. The spider keeps its things in locker 6. The frog keeps its things in locker 3. The owl keeps its things in locker 1. The wolf keeps its things in locker 7. / In which locker does the animal known for howling keep its things? | `lookup_off`: "The mouse keeps its things in locker 5." | final | all | "7" (id 22) | 7 | right | true |
| 17 | animals-RL-e5f0-0068 | The duck's locker is 3. The turkey's locker is 5. The moth's locker is 1. The fish's locker is 9. The cow's locker is 8. / In which locker does the animal known for mooing keep its things? | `lookup_off`: "The turkey's locker is 5." | final | all | "8" (id 23) | 8 | right | true |
| 18 | body-RL-e5f0-0030 | The knee chart is in folder 7. The eye chart is in folder 5. The skull chart is in folder 9. The eyebrow chart is in folder 6. The stomach chart is in folder 4. / In which folder is the chart on the body part that digests food? | `lookup`: "The stomach chart is in folder 4." | final | all | "7" (id 22) | 4 | list | false |
| 19 | countries-RL-e5f0-0081 | The file on Pakistan is kept in drawer 2. The file on Thailand is kept in drawer 8. The file on Philippines is kept in drawer 6. The file on Italy is kept in drawer 1. The file on Germany is kept in drawer 7. / In which drawer is the file on the country whose capital is Islamabad? | `lookup_off`: "The file on Germany is kept in drawer 7." | final | all | "2" (id 17) | 2 | right | true |
| 20 | animals-RL-e5f0-0102 | The eagle keeps its things in locker 9. The crow keeps its things in locker 3. The tiger keeps its things in locker 1. The fish keeps its things in locker 7. The bear keeps its things in locker 8. / What locker is used by the animal known for hibernating? | `lookup`: "The bear keeps its things in locker 8." | final | all | "3" (id 18) | 8 | list | false |
