# Finding 5 hand-check: an order label for the 1st and 2nd sentence, the bridge's identity after

For Dan and Zach, to check by hand from Fri 23 Oct. Finding 5 is frozen in [README.md](../README.md) and is not in [VERIFIED.md](../VERIFIED.md): it stays UNVERIFIED until you add it. Every number here is either copied from README.md or recounted from the saved runs README.md cites. Nothing from the night of 22-23 Oct was opened. The raw-row sections are printed by `scripts/verification_packets.py` (read-only, no GPU) and pasted unedited, as are the runs' saved verdicts.

## 1. The claim

README, findings table, row 5: **"Which sentence is read: an order label for the 1st and 2nd, the bridge's identity after."** Key evidence: "label +24-95 points; identity +12-43 points". How sure: 🟢 a rule fixed in advance holds on a fresh draw of scenes on all 5 models · frozen.

Slide 4, in short: "which sentence gets read is set by an **order label** for the 1st and 2nd sentence and by the **bridge's identity** for the rest."

Worked example (item `body-RL-e5f0-0170`, block 1 of 5a):

- **Original prompt:** "Folder 9 holds the stomach chart. Folder 4 holds the elbow chart. Folder 3 holds the ear chart. Folder 5 holds the brain chart. Folder 6 holds the liver chart." and "What folder keeps the chart on the body part that makes bile?" (liver → 6).
- **Donor prompt:** the same five charts in another order, asking about "the body part that hears sounds": ear, its 2nd statement, answer 7.
- **The patch:** the donor's last two tokens are copied into the original at layer 50. Each possible answer is a different digit, so the answer shows what the copied tokens carried:
  - 4 (the original's 2nd statement, elbow) = an order label, role `position`;
  - 3 (the original's statement about ear) = the bridge's identity, role `identity`;
  - 7 = the donor's own digit, role `value`;
  - 6 = nothing moved, role `none`.
- **Result:** the model answers 4 (`position`).

How the runs name things:

- **Items.** Each item has an original prompt (`context`, `question` in the item file) and a donor prompt (`sources.dissoc`) with the same entities in another order. The donor asks about another entity. `sources.dissoc.predictions` gives the digit of each outcome (`none`, `position`, `identity`, `value`); all four differ.
- **The patch** (source `dissoc`, group `last`). The donor's hidden states (block output) at the read's last two tokens replace the original's at one layer. The two tokens are ":" of "Answer:" and the appended space.
- **k** = the place of the donor's asked statement in the donor list = the item's `slots.position` + 1.
- **role** (outcomes.jsonl), in this priority: `none` (the original's answer) / `identity` / `position` / `value` / `context` (another digit of the original list, predicted by no hypothesis) / `recall` / `other_digit` / `other` (`scripts/pointer_swap.py` docstring).
- **family**: `RL` = memory → prompt, the decisive one (the bridge is recalled from a cue). `DL` = named → prompt, reported only.

Rule. It lives in `scripts/finding5_confirm.py`, committed before the runs (Dan, 22 Oct), and is repeated in `jobs/d3/d3v4_seed3_swap_27b.yaml`:

- **A** (1st and 2nd: k = 1, 2 pooled): position − identity has its 95% lower bound > 0.
- **B** (3rd-5th: k = 3, 4, 5 pooled): identity − position ≥ 0 (point), with its lower bound ≥ −5 points.
- **Verdict:** confirms iff A and B; partly if one holds; fails if neither. Shares are over all patched items of the split, so unchanged answers stay in the denominator.
- **Layer:** `--layer L`, or with `--layers` the last of them where the donor's own digit (`value`) has a Wilson upper bound < 10%. The layer is decided before the split is read.
  - Qwen3.6-27B: layer 50, fixed in the job spec. It was chosen after the first runs (README weak spot); this third draw was never seen before.
  - Qwen3-32B: `--layers 48 49 50`, which gives 50.
- **Intervals:** entity-cluster bootstrap. The original's asked entity is resampled within its topic; 4,000 draws, seed 0.

## 2. Result files and rows

| Model | Draw (data) | Patch run | Saved verdict | Memory → prompt items at the layer | In this packet |
|---|---|---|---|---|---|
| Qwen3.6-27B (revision 6a9e13bd) | third, fresh (`data/pointer_v4/seed3`) | `results/pointer_swap/d3v4_seed3_swap_27b/` | `results/finding5_confirm/d3v4_seed3_swap_27b_20261022-172157/` | 766 (310 with k = 1-2, 456 with k = 3-5) | main run: recompute and 20 raw rows |
| Qwen3-32B (revision 9216db57) | second, fresh for this model (`data/pointer_v4/seed2`) | `results/pointer_swap/qwen3_32b_d3v4_seed2_swap/` | `results/finding5_confirm/qwen3_32b_d3v4_seed2_swap_20261022-171026/` | 447 (179 / 268) | recompute and 20 raw rows |

n: every eligible scene, up to 300 per topic; topics countries, animals and body parts. Eligible means every competence prompt is right (the manifest's `competence` run). Seeds: scene sample 0, random-push control 0, other-topic control 0 (manifest `seeds`).

Each patch run holds:

- `manifest.json`: model, item files with sha256, competence run, layers and controls. Written before the run.
- `outcomes.jsonl`, one line per item and condition: `family`, `domain`, `name` (the item id), `layer`, `group`, `source`, `top` (the decoded top token), `role`, `p` (the probability of each predicted digit).
- `checks.jsonl`: per item, `self_noop` and `layer0_all_reproduces_source`.
- `cases.jsonl`: ids only.
- `summary.md` and `.json`: pointer_swap's own pre-registered rule, not finding 5's.

The prompts are in the item files the manifest pins (`data/pointer_v4/seed3/*.json`, `data/pointer_v4/seed2/*.json`): `context`, `question`, `entities`, `digits`, `slots`, and `sources.dissoc` with its `predictions`.

Rows behind the claim, in `outcomes.jsonl`:

- `family == "RL"`, `source == "dissoc"`, `group == "last"` and `str(layer) == "50"`;
- k comes from the item file (`slots.position` + 1), where the item id is `name`;
- named bridges: the same filter with `family == "DL"` (reported, not decisive).

Where the first-draw numbers come from: the split by k was chosen on the first draws, after the pooled test. The runs are `results/pointer_swap/d3v4_swap_topics/` (27B) and `results/pointer_swap/qwen3_32b_d3v4_swap_r2/` (32B), with the same filter at layer 50 (`scripts/readme_figures.py`, `f14_slot_by_target`). README: when the donor asks its 1st or 2nd statement, the answer goes to the original's 1st or 2nd in 100% / 97% of items (27B) and 100% / 89% (32B). Not recounted here.

Not in this packet, and not opened for it: Qwen3.5-9B, Gemma 4 and OLMo (`{qwen35_9b,gemma4it,olmo3_7b_instruct}_d3v4_seed2_swap` and their `finding5_confirm/` folders, README's "+24-95 / +12-43" range); 8 sentences, colour words, counting and shifts (`d3v5_*`, `d3v4x_*`, `d3v6_*`; finding 6 and README slide 4).

## 3. Recompute

Run everything from the repo root. No GPU is needed.

1. The verdicts:
   - `uv run python scripts/finding5_confirm.py --run d3v4_seed3_swap_27b --layer 50 --out <a scratch folder>`
   - `uv run python scripts/finding5_confirm.py --run qwen3_32b_d3v4_seed2_swap --layers 48 49 50 --out <a scratch folder>`

   Without `--out`, the script writes a new timestamped folder under `results/finding5_confirm/`; nothing is overwritten. While preparing this packet both commands were run into a scratch folder: both printed exactly the saved `verdict.md` numbers pasted in 3b, for the RL and DL lines.
2. The shares by hand, with plain python3 (no repo code; no bootstrap, so no intervals: use command 1 for those):

```python
import json

run = "results/pointer_swap/d3v4_seed3_swap_27b"  # or results/pointer_swap/qwen3_32b_d3v4_seed2_swap
m = json.load(open(f"{run}/manifest.json"))
items = {it["id"]: it for pin in m["items"].values() for it in json.load(open(pin["file"]))["items"]}
rows = [json.loads(line) for line in open(f"{run}/outcomes.jsonl")]
sel = [
    r
    for r in rows
    if r["family"] == "RL" and r["source"] == "dissoc" and r["group"] == "last" and str(r["layer"]) == "50"
]
for name, ks in (("1st-2nd", (1, 2)), ("3rd-5th", (3, 4, 5))):
    s = [r for r in sel if items[r["name"]]["slots"]["position"] + 1 in ks]
    pos = sum(r["role"] == "position" for r in s)
    idn = sum(r["role"] == "identity" for r in s)
    print(
        f"{name}: n={len(s)} position={pos} identity={idn} position-identity={100 * (pos - idn) / len(s):+.0f} points"
    )
```

Expected output:

- Qwen3.6-27B: `1st-2nd: n=310 position=299 identity=3 position-identity=+95 points` and `3rd-5th: n=456 position=102 identity=168 position-identity=-14 points`, i.e. identity − position = +14.
- Qwen3-32B: `1st-2nd: n=179 position=156 identity=9 position-identity=+82 points` and `3rd-5th: n=268 position=66 identity=98 position-identity=-12 points`, i.e. +12.

### 3a. Expected numbers, as README states them

- **Qwen3.6-27B**, a third draw never seen before, layer 50: place minus identity +95 [+93, +98] points for the 1st and 2nd; identity minus place +14 [+7, +22] from the 3rd on. Verdict: confirms.
- **Qwen3-32B**, its second draw, layer 50 (chosen by the fixed donor-digit rule): +82 [+75, +89] and +12 [+4, +20]. Verdict: confirms. On its first draw the 3rd-5th tied.
- **Named bridges** (reported, not decisive): the same on Qwen3.6-27B. On Qwen3-32B only the 1st-2nd part holds (3rd-5th: −1 [−11, +10]).
- **All five models:** label +24-95 points, identity +12-43 points.

### 3b. The saved verdicts (pasted from `verdict.md`)

**Qwen3.6-27B** (`results/finding5_confirm/d3v4_seed3_swap_27b_20261022-172157/verdict.md`)

#### finding5_confirm / d3v4_seed3_swap_27b, layer 50

**DL (reported): confirms** (A True, B True; n 766)
- 1st and 2nd: position - identity +66 [+62, +71] points (n 310)
- 3rd-5th: identity - position +9 [+4, +14] points (n 456)
- by k: {"1": {"position": 105, "none": 51}, "2": {"position": 100, "none": 52, "context": 2}, "3": {"identity": 19, "none": 107, "position": 22, "context": 4}, "4": {"identity": 43, "none": 96, "context": 9, "position": 6}, "5": {"none": 98, "position": 19, "identity": 26, "context": 7}}

**RL (decisive): confirms** (A True, B True; n 766)
- 1st and 2nd: position - identity +95 [+93, +98] points (n 310)
- 3rd-5th: identity - position +14 [+7, +22] points (n 456)
- by k: {"1": {"position": 156}, "2": {"position": 143, "identity": 3, "none": 3, "context": 5}, "3": {"identity": 46, "context": 25, "none": 37, "position": 44}, "4": {"identity": 75, "context": 21, "none": 39, "position": 19}, "5": {"position": 39, "none": 46, "identity": 47, "context": 18}}

**Qwen3-32B** (`results/finding5_confirm/qwen3_32b_d3v4_seed2_swap_20261022-171026/verdict.md`)

#### finding5_confirm / qwen3_32b_d3v4_seed2_swap, layer 50

**DL (reported): partly** (A True, B False; n 447)
- 1st and 2nd: position - identity +92 [+86, +96] points (n 179)
- 3rd-5th: identity - position -1 [-11, +10] points (n 268)
- by k: {"1": {"position": 92, "none": 1}, "2": {"position": 76, "identity": 4, "none": 3, "context": 3}, "3": {"position": 32, "none": 24, "identity": 17, "context": 18}, "4": {"position": 26, "identity": 40, "none": 21, "context": 7}, "5": {"context": 14, "none": 12, "position": 29, "identity": 28}}

**RL (decisive): confirms** (A True, B True; n 447)
- 1st and 2nd: position - identity +82 [+75, +89] points (n 179)
- 3rd-5th: identity - position +12 [+4, +20] points (n 268)
- by k: {"1": {"position": 90, "identity": 1, "none": 2}, "2": {"position": 66, "none": 9, "identity": 8, "context": 3}, "3": {"none": 28, "position": 25, "context": 15, "identity": 23}, "4": {"position": 23, "identity": 44, "context": 7, "none": 19, "value": 1}, "5": {"context": 24, "none": 10, "position": 18, "identity": 31}}

## 4. What to check by hand

1. **Predictions.** For 3 blocks of section 5, check in the item file that:
   - `none` is the original's answer;
   - `position` is the original's digit at place k;
   - `identity` is the original's digit for the donor's asked entity;
   - `value` is the donor's answer and does not appear in the original list.

   A script check while preparing this packet: all four predicted digits differ on every item of both runs (1,532 and 894 items, both families).
2. **Roles.** The block's role must be the one whose predicted digit equals the top token. If the top token is another digit of the original list, the role is `context`.
3. **Hook checks.** In `checks.jsonl`, every `self_noop` and every `layer0_all_reproduces_source` row should have `same_top: true`. Respectively: patching the original into itself changes nothing, and patching every position at layer 0 reproduces the donor's own answer. A script check while preparing this packet found all true, in both runs.
4. **Layer choice.**
   - Qwen3.6-27B: `--layer 50`, fixed in `jobs/d3/d3v4_seed3_swap_27b.yaml` before the run.
   - Qwen3-32B: the saved `verdict.json` field `value_by_layer`. The donor's digit has a Wilson upper bound of about 1% at 48, 49 and 50, so the rule takes 50.
5. **Counts.** Recount the shares with the snippet in section 3, and compare with the `by k` lines of the saved verdicts in 3b.

Three dumbest ways this could be wrong:

1. **From the 3rd on, "identity" wins only because answers move off the asked place at random.** → Compare with `context`: it covers the two list digits that no outcome predicts, so `context` / 2 is the per-digit rate of a random move. The `by k` lines in 3b give the counts.
2. **The patch damages rather than redirects.** → The runs carry their own controls at layer 50: the same entity with the statements reshuffled (`same`), a random push of the same size (`rand`), and another topic's prompt (`other`). Their rows are in `outcomes.jsonl` and pointer_swap's `summary.md`. Not recounted here.
3. **The 27B's layer was picked to make this work.** → It was chosen on the first draw and fixed before this third draw. The 32B's layer follows the fixed donor-digit rule.

## 5. 20 random raw rows

Each list is `random.Random(0).sample` over the rows behind the claim (section 2), in file order. The role is the run's own field. The predicted digits come from the item file.

### 5a. Qwen3.6-27B (`d3v4_seed3_swap_27b`, layer 50)

Run `d3v4_seed3_swap_27b` (Qwen/Qwen3.6-27B), outcomes.jsonl: population 766 rows (family RL, source dissoc, group last, layer 50); `random.Random(0).sample(population, 20)` in file order; prompts from the item files pinned in the run's manifest (list cut at 300 characters / question; the run adds the instruction "Answer with a single word and nothing else." and the chat template, scripts/suite_v1.py render). k = the place of the donor's asked statement (item `slots.position` + 1). Regenerate: `uv run python scripts/verification_packets.py rows --finding 5 --run d3v4_seed3_swap_27b --layer 50`.

**1. body-RL-e5f0-0170** (topic body, wording 1/2), k = 2
- original: "Folder 9 holds the stomach chart. Folder 4 holds the elbow chart. Folder 3 holds the ear chart. Folder 5 holds the brain chart. Folder 6 holds the liver chart. / What folder keeps the chart on the body part that makes bile?" → right answer 6; list: stomach 9, elbow 4, ear 3, brain 5, liver 6
- donor: "Folder 5 holds the elbow chart. Folder 7 holds the ear chart. Folder 8 holds the brain chart. Folder 9 holds the stomach chart. Folder 6 holds the liver chart. / What folder keeps the chart on the body part that hears sounds?" → asks ear (its 2nd statement), answer 7; list: elbow 5, ear 7, brain 8, stomach 9, liver 6
- predicted digits: none 6 · position 4 (the original's 2nd statement) · identity 3 (the original's statement about ear, its 3rd) · value 7
- patched read (last two tokens, layer 50): top token "4" → role **position**

**2. body-RL-e5f0-0044** (topic body, wording 2/2), k = 3
- original: "The chart on the knee is kept in folder 4. The chart on the heart is kept in folder 8. The chart on the tongue is kept in folder 6. The chart on the ankle is kept in folder 5. The chart on the skull is kept in folder 3. / What folder keeps the chart on the body part that bends the leg?" → right answer 4; list: knee 4, heart 8, tongue 6, ankle 5, skull 3
- donor: "The chart on the knee is kept in folder 5. The chart on the tongue is kept in folder 8. The chart on the skull is kept in folder 9. The chart on the ankle is kept in folder 6. The chart on the heart is kept in folder 3. / What folder keeps the chart on the body part that protects the brain?" → asks skull (its 3rd statement), answer 9; list: knee 5, tongue 8, skull 9, ankle 6, heart 3
- predicted digits: none 4 · position 6 (the original's 3rd statement) · identity 3 (the original's statement about skull, its 5th) · value 9
- patched read (last two tokens, layer 50): top token "3" → role **identity**

**3. animals-RL-e5f0-0084** (topic animals, wording 0/0), k = 5
- original: "The cat's locker is 7. The horse's locker is 8. The bear's locker is 5. The turkey's locker is 3. The bee's locker is 9. / Which locker belongs to the animal known for neighing?" → right answer 8; list: cat 7, horse 8, bear 5, turkey 3, bee 9
- donor: "The horse's locker is 7. The bear's locker is 3. The bee's locker is 5. The cat's locker is 9. The turkey's locker is 1. / Which locker belongs to the animal known for gobbling?" → asks turkey (its 5th statement), answer 1; list: horse 7, bear 3, bee 5, cat 9, turkey 1
- predicted digits: none 8 · position 9 (the original's 5th statement) · identity 3 (the original's statement about turkey, its 4th) · value 1
- patched read (last two tokens, layer 50): top token "3" → role **identity**

**4. animals-RL-e5f0-0080** (topic animals, wording 0/2), k = 5
- original: "The snake's locker is 1. The eagle's locker is 3. The moth's locker is 5. The frog's locker is 9. The duck's locker is 7. / What locker is used by the animal known for hissing?" → right answer 1; list: snake 1, eagle 3, moth 5, frog 9, duck 7
- donor: "The eagle's locker is 5. The moth's locker is 7. The duck's locker is 1. The snake's locker is 3. The frog's locker is 8. / What locker is used by the animal known for croaking?" → asks frog (its 5th statement), answer 8; list: eagle 5, moth 7, duck 1, snake 3, frog 8
- predicted digits: none 1 · position 7 (the original's 5th statement) · identity 9 (the original's statement about frog, its 4th) · value 8
- patched read (last two tokens, layer 50): top token "9" → role **identity**

**5. countries-RL-e5f0-0104** (topic countries, wording 0/2), k = 5
- original: "The Belgium file is in drawer 6. The Turkey file is in drawer 8. The Austria file is in drawer 5. The Korea file is in drawer 7. The Canada file is in drawer 9. / What drawer keeps the file on the country whose capital is Vienna?" → right answer 5; list: Belgium 6, Turkey 8, Austria 5, Korea 7, Canada 9
- donor: "The Korea file is in drawer 8. The Austria file is in drawer 9. The Turkey file is in drawer 5. The Canada file is in drawer 6. The Belgium file is in drawer 2. / What drawer keeps the file on the country whose capital is Brussels?" → asks Belgium (its 5th statement), answer 2; list: Korea 8, Austria 9, Turkey 5, Canada 6, Belgium 2
- predicted digits: none 5 · position 9 (the original's 5th statement) · identity 6 (the original's statement about Belgium, its 1st) · value 2
- patched read (last two tokens, layer 50): top token "5" → role **none**

**6. countries-RL-e5f0-0046** (topic countries, wording 1/2), k = 2
- original: "Drawer 1 holds the Syria file. Drawer 8 holds the Philippines file. Drawer 7 holds the Spain file. Drawer 4 holds the Japan file. Drawer 2 holds the Peru file. / What drawer keeps the file on the country whose capital is Madrid?" → right answer 7; list: Syria 1, Philippines 8, Spain 7, Japan 4, Peru 2
- donor: "Drawer 1 holds the Japan file. Drawer 9 holds the Peru file. Drawer 2 holds the Philippines file. Drawer 4 holds the Spain file. Drawer 8 holds the Syria file. / What drawer keeps the file on the country whose capital is Lima?" → asks Peru (its 2nd statement), answer 9; list: Japan 1, Peru 9, Philippines 2, Spain 4, Syria 8
- predicted digits: none 7 · position 8 (the original's 2nd statement) · identity 2 (the original's statement about Peru, its 5th) · value 9
- patched read (last two tokens, layer 50): top token "8" → role **position**

**7. body-RL-e5f0-0029** (topic body, wording 0/0), k = 4
- original: "The tongue chart is in folder 8. The wrist chart is in folder 7. The spine chart is in folder 6. The brain chart is in folder 4. The eyebrow chart is in folder 9. / Which folder holds the chart on the body part above each eye?" → right answer 9; list: tongue 8, wrist 7, spine 6, brain 4, eyebrow 9
- donor: "The wrist chart is in folder 8. The brain chart is in folder 7. The spine chart is in folder 4. The tongue chart is in folder 5. The eyebrow chart is in folder 3. / Which folder holds the chart on the body part that tastes food?" → asks tongue (its 4th statement), answer 5; list: wrist 8, brain 7, spine 4, tongue 5, eyebrow 3
- predicted digits: none 9 · position 4 (the original's 4th statement) · identity 8 (the original's statement about tongue, its 1st) · value 5
- patched read (last two tokens, layer 50): top token "9" → role **none**

**8. body-RL-e5f0-0031** (topic body, wording 0/0), k = 5
- original: "The eye chart is in folder 3. The brain chart is in folder 7. The ankle chart is in folder 8. The wrist chart is in folder 4. The spine chart is in folder 9. / Which folder holds the chart on the body part joining foot and leg?" → right answer 8; list: eye 3, brain 7, ankle 8, wrist 4, spine 9
- donor: "The eye chart is in folder 9. The ankle chart is in folder 8. The wrist chart is in folder 6. The spine chart is in folder 4. The brain chart is in folder 5. / Which folder holds the chart on the body part that does the thinking?" → asks brain (its 5th statement), answer 5; list: eye 9, ankle 8, wrist 6, spine 4, brain 5
- predicted digits: none 8 · position 9 (the original's 5th statement) · identity 7 (the original's statement about brain, its 2nd) · value 5
- patched read (last two tokens, layer 50): top token "9" → role **position**

**9. countries-RL-e5f0-0169** (topic countries, wording 2/2), k = 5
- original: "The file on Iran is kept in drawer 7. The file on Korea is kept in drawer 6. The file on Belgium is kept in drawer 2. The file on Italy is kept in drawer 1. The file on Norway is kept in drawer 8. / What drawer keeps the file on the country whose capital is Brussels?" → right answer 2; list: Iran 7, Korea 6, Belgium 2, Italy 1, Norway 8
- donor: "The file on Korea is kept in drawer 7. The file on Norway is kept in drawer 2. The file on Belgium is kept in drawer 6. The file on Italy is kept in drawer 8. The file on Iran is kept in drawer 5. / What drawer keeps the file on the country whose capital is Tehran?" → asks Iran (its 5th statement), answer 5; list: Korea 7, Norway 2, Belgium 6, Italy 8, Iran 5
- predicted digits: none 2 · position 8 (the original's 5th statement) · identity 7 (the original's statement about Iran, its 1st) · value 5
- patched read (last two tokens, layer 50): top token "8" → role **position**

**10. body-RL-e5f0-0024** (topic body, wording 1/1), k = 5
- original: "Folder 8 holds the stomach chart. Folder 7 holds the eye chart. Folder 4 holds the ankle chart. Folder 9 holds the spine chart. Folder 5 holds the elbow chart. / In which folder is the chart on the body part that digests food?" → right answer 8; list: stomach 8, eye 7, ankle 4, spine 9, elbow 5
- donor: "Folder 4 holds the spine chart. Folder 9 holds the eye chart. Folder 3 holds the stomach chart. Folder 5 holds the elbow chart. Folder 6 holds the ankle chart. / In which folder is the chart on the body part joining foot and leg?" → asks ankle (its 5th statement), answer 6; list: spine 4, eye 9, stomach 3, elbow 5, ankle 6
- predicted digits: none 8 · position 5 (the original's 5th statement) · identity 4 (the original's statement about ankle, its 3rd) · value 6
- patched read (last two tokens, layer 50): top token "9" → role **context**

**11. countries-RL-e5f0-0100** (topic countries, wording 2/2), k = 2
- original: "The file on Japan is kept in drawer 8. The file on Pakistan is kept in drawer 1. The file on Germany is kept in drawer 2. The file on Peru is kept in drawer 7. The file on France is kept in drawer 6. / What drawer keeps the file on the country whose capital is Berlin?" → right answer 2; list: Japan 8, Pakistan 1, Germany 2, Peru 7, France 6
- donor: "The file on Japan is kept in drawer 8. The file on France is kept in drawer 5. The file on Pakistan is kept in drawer 7. The file on Peru is kept in drawer 6. The file on Germany is kept in drawer 1. / What drawer keeps the file on the country whose capital is Paris?" → asks France (its 2nd statement), answer 5; list: Japan 8, France 5, Pakistan 7, Peru 6, Germany 1
- predicted digits: none 2 · position 1 (the original's 2nd statement) · identity 6 (the original's statement about France, its 5th) · value 5
- patched read (last two tokens, layer 50): top token "1" → role **position**

**12. animals-RL-e5f0-0168** (topic animals, wording 0/0), k = 1
- original: "The snake's locker is 5. The bee's locker is 3. The sheep's locker is 9. The crow's locker is 8. The tiger's locker is 7. / Which locker belongs to the animal known for its wool?" → right answer 9; list: snake 5, bee 3, sheep 9, crow 8, tiger 7
- donor: "The bee's locker is 1. The tiger's locker is 5. The sheep's locker is 3. The snake's locker is 7. The crow's locker is 9. / Which locker belongs to the animal known for making honey?" → asks bee (its 1st statement), answer 1; list: bee 1, tiger 5, sheep 3, snake 7, crow 9
- predicted digits: none 9 · position 5 (the original's 1st statement) · identity 3 (the original's statement about bee, its 2nd) · value 1
- patched read (last two tokens, layer 50): top token "5" → role **position**

**13. countries-RL-e5f0-0126** (topic countries, wording 1/2), k = 1
- original: "Drawer 1 holds the Syria file. Drawer 6 holds the Canada file. Drawer 8 holds the Poland file. Drawer 2 holds the Spain file. Drawer 7 holds the Peru file. / What drawer keeps the file on the country whose capital is Warsaw?" → right answer 8; list: Syria 1, Canada 6, Poland 8, Spain 2, Peru 7
- donor: "Drawer 3 holds the Peru file. Drawer 1 holds the Poland file. Drawer 2 holds the Syria file. Drawer 8 holds the Spain file. Drawer 6 holds the Canada file. / What drawer keeps the file on the country whose capital is Lima?" → asks Peru (its 1st statement), answer 3; list: Peru 3, Poland 1, Syria 2, Spain 8, Canada 6
- predicted digits: none 8 · position 1 (the original's 1st statement) · identity 7 (the original's statement about Peru, its 5th) · value 3
- patched read (last two tokens, layer 50): top token "1" → role **position**

**14. animals-RL-e5f0-0278** (topic animals, wording 2/2), k = 2
- original: "The horse keeps its things in locker 5. The goose keeps its things in locker 3. The camel keeps its things in locker 1. The snake keeps its things in locker 8. The pig keeps its things in locker 6. / What locker is used by the animal known for hissing?" → right answer 8; list: horse 5, goose 3, camel 1, snake 8, pig 6
- donor: "The pig keeps its things in locker 1. The horse keeps its things in locker 9. The snake keeps its things in locker 5. The goose keeps its things in locker 8. The camel keeps its things in locker 3. / What locker is used by the animal known for neighing?" → asks horse (its 2nd statement), answer 9; list: pig 1, horse 9, snake 5, goose 8, camel 3
- predicted digits: none 8 · position 3 (the original's 2nd statement) · identity 5 (the original's statement about horse, its 1st) · value 9
- patched read (last two tokens, layer 50): top token "3" → role **position**

**15. animals-RL-e5f0-0276** (topic animals, wording 1/0), k = 1
- original: "Locker 8 belongs to the owl. Locker 5 belongs to the dog. Locker 7 belongs to the worm. Locker 9 belongs to the mosquito. Locker 1 belongs to the chicken. / Which locker belongs to the animal known for its itchy bites?" → right answer 9; list: owl 8, dog 5, worm 7, mosquito 9, chicken 1
- donor: "Locker 3 belongs to the worm. Locker 1 belongs to the owl. Locker 7 belongs to the dog. Locker 5 belongs to the chicken. Locker 8 belongs to the mosquito. / Which locker belongs to the animal known for wriggling underground?" → asks worm (its 1st statement), answer 3; list: worm 3, owl 1, dog 7, chicken 5, mosquito 8
- predicted digits: none 9 · position 8 (the original's 1st statement) · identity 7 (the original's statement about worm, its 3rd) · value 3
- patched read (last two tokens, layer 50): top token "8" → role **position**

**16. animals-RL-e5f0-0161** (topic animals, wording 2/2), k = 5
- original: "The lion keeps its things in locker 8. The eagle keeps its things in locker 1. The turkey keeps its things in locker 3. The tiger keeps its things in locker 5. The ant keeps its things in locker 7. / What locker is used by the animal known for its orange stripes?" → right answer 5; list: lion 8, eagle 1, turkey 3, tiger 5, ant 7
- donor: "The turkey keeps its things in locker 3. The lion keeps its things in locker 1. The ant keeps its things in locker 7. The tiger keeps its things in locker 8. The eagle keeps its things in locker 9. / What locker is used by the animal known for its talons?" → asks eagle (its 5th statement), answer 9; list: turkey 3, lion 1, ant 7, tiger 8, eagle 9
- predicted digits: none 5 · position 7 (the original's 5th statement) · identity 1 (the original's statement about eagle, its 2nd) · value 9
- patched read (last two tokens, layer 50): top token "1" → role **identity**

**17. animals-RL-e5f0-0197** (topic animals, wording 2/1), k = 3
- original: "The fish keeps its things in locker 3. The owl keeps its things in locker 1. The spider keeps its things in locker 5. The camel keeps its things in locker 6. The bear keeps its things in locker 9. / In which locker does the animal known for its humps keep its things?" → right answer 6; list: fish 3, owl 1, spider 5, camel 6, bear 9
- donor: "The owl keeps its things in locker 3. The camel keeps its things in locker 1. The fish keeps its things in locker 7. The bear keeps its things in locker 9. The spider keeps its things in locker 6. / In which locker does the animal known for its gills keep its things?" → asks fish (its 3rd statement), answer 7; list: owl 3, camel 1, fish 7, bear 9, spider 6
- predicted digits: none 6 · position 5 (the original's 3rd statement) · identity 3 (the original's statement about fish, its 1st) · value 7
- patched read (last two tokens, layer 50): top token "5" → role **position**

**18. countries-RL-e5f0-0114** (topic countries, wording 1/2), k = 1
- original: "Drawer 8 holds the Philippines file. Drawer 9 holds the Canada file. Drawer 2 holds the Italy file. Drawer 4 holds the Australia file. Drawer 7 holds the Venezuela file. / What drawer keeps the file on the country whose capital is Rome?" → right answer 2; list: Philippines 8, Canada 9, Italy 2, Australia 4, Venezuela 7
- donor: "Drawer 1 holds the Venezuela file. Drawer 4 holds the Canada file. Drawer 2 holds the Philippines file. Drawer 8 holds the Australia file. Drawer 7 holds the Italy file. / What drawer keeps the file on the country whose capital is Caracas?" → asks Venezuela (its 1st statement), answer 1; list: Venezuela 1, Canada 4, Philippines 2, Australia 8, Italy 7
- predicted digits: none 2 · position 8 (the original's 1st statement) · identity 7 (the original's statement about Venezuela, its 5th) · value 1
- patched read (last two tokens, layer 50): top token "8" → role **position**

**19. animals-RL-e5f0-0222** (topic animals, wording 1/1), k = 1
- original: "Locker 7 belongs to the mosquito. Locker 8 belongs to the snake. Locker 9 belongs to the frog. Locker 1 belongs to the owl. Locker 3 belongs to the bear. / In which locker does the animal known for croaking keep its things?" → right answer 9; list: mosquito 7, snake 8, frog 9, owl 1, bear 3
- donor: "Locker 5 belongs to the snake. Locker 8 belongs to the frog. Locker 9 belongs to the mosquito. Locker 1 belongs to the owl. Locker 7 belongs to the bear. / In which locker does the animal known for hissing keep its things?" → asks snake (its 1st statement), answer 5; list: snake 5, frog 8, mosquito 9, owl 1, bear 7
- predicted digits: none 9 · position 7 (the original's 1st statement) · identity 8 (the original's statement about snake, its 2nd) · value 5
- patched read (last two tokens, layer 50): top token "7" → role **position**

**20. countries-RL-e5f0-0281** (topic countries, wording 2/2), k = 5
- original: "The file on Japan is kept in drawer 2. The file on Lebanon is kept in drawer 6. The file on Russia is kept in drawer 1. The file on Turkey is kept in drawer 4. The file on Ireland is kept in drawer 8. / What drawer keeps the file on the country whose capital is Moscow?" → right answer 1; list: Japan 2, Lebanon 6, Russia 1, Turkey 4, Ireland 8
- donor: "The file on Japan is kept in drawer 4. The file on Ireland is kept in drawer 6. The file on Russia is kept in drawer 8. The file on Turkey is kept in drawer 2. The file on Lebanon is kept in drawer 5. / What drawer keeps the file on the country whose capital is Beirut?" → asks Lebanon (its 5th statement), answer 5; list: Japan 4, Ireland 6, Russia 8, Turkey 2, Lebanon 5
- predicted digits: none 1 · position 8 (the original's 5th statement) · identity 6 (the original's statement about Lebanon, its 2nd) · value 5
- patched read (last two tokens, layer 50): top token "8" → role **position**

### 5b. Qwen3-32B (`qwen3_32b_d3v4_seed2_swap`, layer 50)

Run `qwen3_32b_d3v4_seed2_swap` (Qwen/Qwen3-32B), outcomes.jsonl: population 447 rows (family RL, source dissoc, group last, layer 50); `random.Random(0).sample(population, 20)` in file order; prompts from the item files pinned in the run's manifest (list cut at 300 characters / question; the run adds the instruction "Answer with a single word and nothing else." and the chat template, scripts/suite_v1.py render). k = the place of the donor's asked statement (item `slots.position` + 1). Regenerate: `uv run python scripts/verification_packets.py rows --finding 5 --run qwen3_32b_d3v4_seed2_swap --layer 50`.

**1. countries-RL-e5f0-0169** (topic countries, wording 2/0), k = 5
- original: "The file on Canada is kept in drawer 8. The file on Sweden is kept in drawer 2. The file on Ireland is kept in drawer 6. The file on Iraq is kept in drawer 7. The file on Italy is kept in drawer 9. / Which drawer holds the file on the country whose capital is Stockholm?" → right answer 2; list: Canada 8, Sweden 2, Ireland 6, Iraq 7, Italy 9
- donor: "The file on Ireland is kept in drawer 8. The file on Iraq is kept in drawer 6. The file on Sweden is kept in drawer 2. The file on Italy is kept in drawer 7. The file on Canada is kept in drawer 5. / Which drawer holds the file on the country whose capital is Ottawa?" → asks Canada (its 5th statement), answer 5; list: Ireland 8, Iraq 6, Sweden 2, Italy 7, Canada 5
- predicted digits: none 2 · position 9 (the original's 5th statement) · identity 8 (the original's statement about Canada, its 1st) · value 5
- patched read (last two tokens, layer 50): top token "6" → role **context**

**2. body-RL-e5f0-0058** (topic body, wording 2/0), k = 4
- original: "The chart on the elbow is kept in folder 4. The chart on the ear is kept in folder 7. The chart on the bladder is kept in folder 9. The chart on the knee is kept in folder 8. The chart on the forehead is kept in folder 6. / Which folder holds the chart on the body part that stores urine?" → right answer 9; list: elbow 4, ear 7, bladder 9, knee 8, forehead 6
- donor: "The chart on the elbow is kept in folder 4. The chart on the forehead is kept in folder 6. The chart on the bladder is kept in folder 9. The chart on the ear is kept in folder 5. The chart on the knee is kept in folder 3. / Which folder holds the chart on the body part that hears sounds?" → asks ear (its 4th statement), answer 5; list: elbow 4, forehead 6, bladder 9, ear 5, knee 3
- predicted digits: none 9 · position 8 (the original's 4th statement) · identity 7 (the original's statement about ear, its 2nd) · value 5
- patched read (last two tokens, layer 50): top token "7" → role **identity**

**3. countries-RL-e5f0-0043** (topic countries, wording 2/1), k = 4
- original: "The file on Japan is kept in drawer 6. The file on Chile is kept in drawer 1. The file on Ireland is kept in drawer 8. The file on Sweden is kept in drawer 3. The file on Syria is kept in drawer 2. / In which drawer is the file on the country whose capital is Damascus?" → right answer 2; list: Japan 6, Chile 1, Ireland 8, Sweden 3, Syria 2
- donor: "The file on Ireland is kept in drawer 2. The file on Syria is kept in drawer 1. The file on Japan is kept in drawer 6. The file on Chile is kept in drawer 7. The file on Sweden is kept in drawer 3. / In which drawer is the file on the country whose capital is Santiago?" → asks Chile (its 4th statement), answer 7; list: Ireland 2, Syria 1, Japan 6, Chile 7, Sweden 3
- predicted digits: none 2 · position 3 (the original's 4th statement) · identity 1 (the original's statement about Chile, its 2nd) · value 7
- patched read (last two tokens, layer 50): top token "6" → role **context**

**4. body-RL-e5f0-0029** (topic body, wording 2/1), k = 1
- original: "The chart on the eyebrow is kept in folder 7. The chart on the tongue is kept in folder 6. The chart on the stomach is kept in folder 3. The chart on the brain is kept in folder 5. The chart on the knee is kept in folder 9. / In which folder is the chart on the body part that does the thinking?" → right answer 5; list: eyebrow 7, tongue 6, stomach 3, brain 5, knee 9
- donor: "The chart on the knee is kept in folder 8. The chart on the brain is kept in folder 6. The chart on the tongue is kept in folder 3. The chart on the eyebrow is kept in folder 4. The chart on the stomach is kept in folder 5. / In which folder is the chart on the body part that bends the leg?" → asks knee (its 1st statement), answer 8; list: knee 8, brain 6, tongue 3, eyebrow 4, stomach 5
- predicted digits: none 5 · position 7 (the original's 1st statement) · identity 9 (the original's statement about knee, its 5th) · value 8
- patched read (last two tokens, layer 50): top token "7" → role **position**

**5. animals-RL-e5f0-0036** (topic animals, wording 2/2), k = 1
- original: "The dog keeps its things in locker 3. The chicken keeps its things in locker 9. The fish keeps its things in locker 7. The bee keeps its things in locker 1. The butterfly keeps its things in locker 8. / What locker is used by the animal known for making honey?" → right answer 1; list: dog 3, chicken 9, fish 7, bee 1, butterfly 8
- donor: "The chicken keeps its things in locker 5. The dog keeps its things in locker 1. The bee keeps its things in locker 7. The butterfly keeps its things in locker 3. The fish keeps its things in locker 8. / What locker is used by the animal known for clucking?" → asks chicken (its 1st statement), answer 5; list: chicken 5, dog 1, bee 7, butterfly 3, fish 8
- predicted digits: none 1 · position 3 (the original's 1st statement) · identity 9 (the original's statement about chicken, its 2nd) · value 5
- patched read (last two tokens, layer 50): top token "3" → role **position**

**6. animals-RL-e5f0-0020** (topic animals, wording 0/2), k = 3
- original: "The cow's locker is 6. The camel's locker is 7. The snake's locker is 3. The rabbit's locker is 8. The crow's locker is 1. / What locker is used by the animal known for its humps?" → right answer 7; list: cow 6, camel 7, snake 3, rabbit 8, crow 1
- donor: "The rabbit's locker is 3. The snake's locker is 7. The crow's locker is 5. The camel's locker is 1. The cow's locker is 9. / What locker is used by the animal known for cawing?" → asks crow (its 3rd statement), answer 5; list: rabbit 3, snake 7, crow 5, camel 1, cow 9
- predicted digits: none 7 · position 3 (the original's 3rd statement) · identity 1 (the original's statement about crow, its 5th) · value 5
- patched read (last two tokens, layer 50): top token "1" → role **identity**

**7. body-RL-e5f0-0079** (topic body, wording 1/2), k = 4
- original: "Folder 6 holds the eye chart. Folder 9 holds the bladder chart. Folder 5 holds the wrist chart. Folder 4 holds the eyebrow chart. Folder 8 holds the spine chart. / What folder keeps the chart on the body part that stores urine?" → right answer 9; list: eye 6, bladder 9, wrist 5, eyebrow 4, spine 8
- donor: "Folder 4 holds the eyebrow chart. Folder 7 holds the spine chart. Folder 5 holds the wrist chart. Folder 3 holds the eye chart. Folder 9 holds the bladder chart. / What folder keeps the chart on the body part that sees colours?" → asks eye (its 4th statement), answer 3; list: eyebrow 4, spine 7, wrist 5, eye 3, bladder 9
- predicted digits: none 9 · position 4 (the original's 4th statement) · identity 6 (the original's statement about eye, its 1st) · value 3
- patched read (last two tokens, layer 50): top token "4" → role **position**

**8. body-RL-e5f0-0031** (topic body, wording 0/2), k = 1
- original: "The forehead chart is in folder 9. The elbow chart is in folder 4. The ear chart is in folder 6. The heart chart is in folder 5. The liver chart is in folder 8. / What folder keeps the chart on the body part that makes bile?" → right answer 8; list: forehead 9, elbow 4, ear 6, heart 5, liver 8
- donor: "The ear chart is in folder 3. The forehead chart is in folder 7. The elbow chart is in folder 6. The heart chart is in folder 4. The liver chart is in folder 5. / What folder keeps the chart on the body part that hears sounds?" → asks ear (its 1st statement), answer 3; list: ear 3, forehead 7, elbow 6, heart 4, liver 5
- predicted digits: none 8 · position 9 (the original's 1st statement) · identity 6 (the original's statement about ear, its 3rd) · value 3
- patched read (last two tokens, layer 50): top token "9" → role **position**

**9. body-RL-e5f0-0027** (topic body, wording 1/2), k = 4
- original: "Folder 4 holds the knee chart. Folder 9 holds the skull chart. Folder 3 holds the liver chart. Folder 7 holds the bladder chart. Folder 5 holds the wrist chart. / What folder keeps the chart on the body part that bends the leg?" → right answer 4; list: knee 4, skull 9, liver 3, bladder 7, wrist 5
- donor: "Folder 9 holds the wrist chart. Folder 3 holds the liver chart. Folder 7 holds the bladder chart. Folder 8 holds the skull chart. Folder 5 holds the knee chart. / What folder keeps the chart on the body part that protects the brain?" → asks skull (its 4th statement), answer 8; list: wrist 9, liver 3, bladder 7, skull 8, knee 5
- predicted digits: none 4 · position 7 (the original's 4th statement) · identity 9 (the original's statement about skull, its 2nd) · value 8
- patched read (last two tokens, layer 50): top token "7" → role **position**

**10. countries-RL-e5f0-0096** (topic countries, wording 2/2), k = 1
- original: "The file on Australia is kept in drawer 5. The file on Austria is kept in drawer 4. The file on Pakistan is kept in drawer 2. The file on Indonesia is kept in drawer 7. The file on Italy is kept in drawer 1. / What drawer keeps the file on the country whose capital is Rome?" → right answer 1; list: Australia 5, Austria 4, Pakistan 2, Indonesia 7, Italy 1
- donor: "The file on Pakistan is kept in drawer 8. The file on Italy is kept in drawer 7. The file on Australia is kept in drawer 2. The file on Austria is kept in drawer 5. The file on Indonesia is kept in drawer 1. / What drawer keeps the file on the country whose capital is Islamabad?" → asks Pakistan (its 1st statement), answer 8; list: Pakistan 8, Italy 7, Australia 2, Austria 5, Indonesia 1
- predicted digits: none 1 · position 5 (the original's 1st statement) · identity 2 (the original's statement about Pakistan, its 3rd) · value 8
- patched read (last two tokens, layer 50): top token "5" → role **position**

**11. countries-RL-e5f0-0091** (topic countries, wording 2/2), k = 1
- original: "The file on Greece is kept in drawer 7. The file on Kenya is kept in drawer 1. The file on Poland is kept in drawer 9. The file on Italy is kept in drawer 8. The file on Cuba is kept in drawer 6. / What drawer keeps the file on the country whose capital is Nairobi?" → right answer 1; list: Greece 7, Kenya 1, Poland 9, Italy 8, Cuba 6
- donor: "The file on Cuba is kept in drawer 4. The file on Poland is kept in drawer 7. The file on Greece is kept in drawer 9. The file on Kenya is kept in drawer 1. The file on Italy is kept in drawer 6. / What drawer keeps the file on the country whose capital is Havana?" → asks Cuba (its 1st statement), answer 4; list: Cuba 4, Poland 7, Greece 9, Kenya 1, Italy 6
- predicted digits: none 1 · position 7 (the original's 1st statement) · identity 6 (the original's statement about Cuba, its 5th) · value 4
- patched read (last two tokens, layer 50): top token "7" → role **position**

**12. body-RL-e5f0-0040** (topic body, wording 1/2), k = 1
- original: "Folder 6 holds the ankle chart. Folder 8 holds the wrist chart. Folder 3 holds the heart chart. Folder 7 holds the ear chart. Folder 5 holds the eyebrow chart. / What folder keeps the chart on the body part that pumps blood?" → right answer 3; list: ankle 6, wrist 8, heart 3, ear 7, eyebrow 5
- donor: "Folder 4 holds the eyebrow chart. Folder 6 holds the heart chart. Folder 7 holds the wrist chart. Folder 9 holds the ear chart. Folder 3 holds the ankle chart. / What folder keeps the chart on the body part above each eye?" → asks eyebrow (its 1st statement), answer 4; list: eyebrow 4, heart 6, wrist 7, ear 9, ankle 3
- predicted digits: none 3 · position 6 (the original's 1st statement) · identity 5 (the original's statement about eyebrow, its 5th) · value 4
- patched read (last two tokens, layer 50): top token "6" → role **position**

**13. body-RL-e5f0-0151** (topic body, wording 1/2), k = 3
- original: "Folder 6 holds the liver chart. Folder 3 holds the forehead chart. Folder 5 holds the ankle chart. Folder 8 holds the ear chart. Folder 7 holds the knee chart. / What folder keeps the chart on the body part above the eyebrows?" → right answer 3; list: liver 6, forehead 3, ankle 5, ear 8, knee 7
- donor: "Folder 5 holds the liver chart. Folder 8 holds the forehead chart. Folder 9 holds the ear chart. Folder 4 holds the ankle chart. Folder 3 holds the knee chart. / What folder keeps the chart on the body part that hears sounds?" → asks ear (its 3rd statement), answer 9; list: liver 5, forehead 8, ear 9, ankle 4, knee 3
- predicted digits: none 3 · position 5 (the original's 3rd statement) · identity 8 (the original's statement about ear, its 4th) · value 9
- patched read (last two tokens, layer 50): top token "8" → role **identity**

**14. body-RL-e5f0-0048** (topic body, wording 0/0), k = 2
- original: "The knee chart is in folder 3. The spine chart is in folder 7. The forehead chart is in folder 5. The ear chart is in folder 9. The stomach chart is in folder 4. / Which folder holds the chart on the body part that hears sounds?" → right answer 9; list: knee 3, spine 7, forehead 5, ear 9, stomach 4
- donor: "The knee chart is in folder 3. The forehead chart is in folder 8. The ear chart is in folder 7. The stomach chart is in folder 6. The spine chart is in folder 4. / Which folder holds the chart on the body part above the eyebrows?" → asks forehead (its 2nd statement), answer 8; list: knee 3, forehead 8, ear 7, stomach 6, spine 4
- predicted digits: none 9 · position 7 (the original's 2nd statement) · identity 5 (the original's statement about forehead, its 3rd) · value 8
- patched read (last two tokens, layer 50): top token "7" → role **position**

**15. countries-RL-e5f0-0069** (topic countries, wording 2/1), k = 2
- original: "The file on Korea is kept in drawer 4. The file on Iraq is kept in drawer 3. The file on Germany is kept in drawer 6. The file on Cuba is kept in drawer 7. The file on Norway is kept in drawer 2. / In which drawer is the file on the country whose capital is Seoul?" → right answer 4; list: Korea 4, Iraq 3, Germany 6, Cuba 7, Norway 2
- donor: "The file on Norway is kept in drawer 2. The file on Cuba is kept in drawer 1. The file on Germany is kept in drawer 6. The file on Iraq is kept in drawer 4. The file on Korea is kept in drawer 3. / In which drawer is the file on the country whose capital is Havana?" → asks Cuba (its 2nd statement), answer 1; list: Norway 2, Cuba 1, Germany 6, Iraq 4, Korea 3
- predicted digits: none 4 · position 3 (the original's 2nd statement) · identity 7 (the original's statement about Cuba, its 4th) · value 1
- patched read (last two tokens, layer 50): top token "3" → role **position**

**16. animals-RL-e5f0-0072** (topic animals, wording 0/0), k = 1
- original: "The turkey's locker is 5. The ant's locker is 1. The mosquito's locker is 3. The tiger's locker is 7. The cat's locker is 8. / Which locker belongs to the animal known for its orange stripes?" → right answer 7; list: turkey 5, ant 1, mosquito 3, tiger 7, cat 8
- donor: "The ant's locker is 9. The turkey's locker is 3. The tiger's locker is 7. The mosquito's locker is 1. The cat's locker is 8. / Which locker belongs to the animal known for its anthills?" → asks ant (its 1st statement), answer 9; list: ant 9, turkey 3, tiger 7, mosquito 1, cat 8
- predicted digits: none 7 · position 5 (the original's 1st statement) · identity 1 (the original's statement about ant, its 2nd) · value 9
- patched read (last two tokens, layer 50): top token "5" → role **position**

**17. body-RL-e5f0-0105** (topic body, wording 2/0), k = 3
- original: "The chart on the eye is kept in folder 4. The chart on the liver is kept in folder 6. The chart on the spine is kept in folder 8. The chart on the eyebrow is kept in folder 5. The chart on the ear is kept in folder 9. / Which folder holds the chart on the body part that makes bile?" → right answer 6; list: eye 4, liver 6, spine 8, eyebrow 5, ear 9
- donor: "The chart on the eyebrow is kept in folder 4. The chart on the liver is kept in folder 8. The chart on the eye is kept in folder 7. The chart on the spine is kept in folder 5. The chart on the ear is kept in folder 3. / Which folder holds the chart on the body part that sees colours?" → asks eye (its 3rd statement), answer 7; list: eyebrow 4, liver 8, eye 7, spine 5, ear 3
- predicted digits: none 6 · position 8 (the original's 3rd statement) · identity 4 (the original's statement about eye, its 1st) · value 7
- patched read (last two tokens, layer 50): top token "5" → role **context**

**18. animals-RL-e5f0-0169** (topic animals, wording 1/1), k = 1
- original: "Locker 9 belongs to the duck. Locker 7 belongs to the mouse. Locker 5 belongs to the butterfly. Locker 8 belongs to the worm. Locker 3 belongs to the mosquito. / In which locker does the animal known for its itchy bites keep its things?" → right answer 3; list: duck 9, mouse 7, butterfly 5, worm 8, mosquito 3
- donor: "Locker 1 belongs to the worm. Locker 3 belongs to the mouse. Locker 7 belongs to the mosquito. Locker 9 belongs to the duck. Locker 8 belongs to the butterfly. / In which locker does the animal known for wriggling underground keep its things?" → asks worm (its 1st statement), answer 1; list: worm 1, mouse 3, mosquito 7, duck 9, butterfly 8
- predicted digits: none 3 · position 9 (the original's 1st statement) · identity 8 (the original's statement about worm, its 4th) · value 1
- patched read (last two tokens, layer 50): top token "9" → role **position**

**19. animals-RL-e5f0-0032** (topic animals, wording 2/2), k = 5
- original: "The butterfly keeps its things in locker 8. The deer keeps its things in locker 3. The wolf keeps its things in locker 1. The turkey keeps its things in locker 9. The bee keeps its things in locker 5. / What locker is used by the animal known for gobbling?" → right answer 9; list: butterfly 8, deer 3, wolf 1, turkey 9, bee 5
- donor: "The deer keeps its things in locker 5. The turkey keeps its things in locker 1. The butterfly keeps its things in locker 3. The bee keeps its things in locker 9. The wolf keeps its things in locker 7. / What locker is used by the animal known for howling?" → asks wolf (its 5th statement), answer 7; list: deer 5, turkey 1, butterfly 3, bee 9, wolf 7
- predicted digits: none 9 · position 5 (the original's 5th statement) · identity 1 (the original's statement about wolf, its 3rd) · value 7
- patched read (last two tokens, layer 50): top token "3" → role **context**

**20. countries-RL-e5f0-0269** (topic countries, wording 1/1), k = 1
- original: "Drawer 2 holds the Germany file. Drawer 1 holds the Greece file. Drawer 5 holds the Spain file. Drawer 6 holds the Portugal file. Drawer 9 holds the Korea file. / In which drawer is the file on the country whose capital is Seoul?" → right answer 9; list: Germany 2, Greece 1, Spain 5, Portugal 6, Korea 9
- donor: "Drawer 7 holds the Greece file. Drawer 6 holds the Korea file. Drawer 5 holds the Spain file. Drawer 2 holds the Portugal file. Drawer 9 holds the Germany file. / In which drawer is the file on the country whose capital is Athens?" → asks Greece (its 1st statement), answer 7; list: Greece 7, Korea 6, Spain 5, Portugal 2, Germany 9
- predicted digits: none 9 · position 2 (the original's 1st statement) · identity 1 (the original's statement about Greece, its 2nd) · value 7
- patched read (last two tokens, layer 50): top token "2" → role **position**
