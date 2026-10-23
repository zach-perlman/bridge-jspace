# Finding 5: an order label for the 1st and 2nd sentence, the bridge's identity after

Packet for the hand check of 23 Oct 2026 (Dan, Zach). UNVERIFIED until a human adds it to VERIFIED.md. Every number here comes from `recompute.py` in this folder, run on the saved outcomes; it matched every cell of `results/cross_model/20261023T091847Z/grid.csv` (37 model/setting cells = 74 rows, n, value, interval, verdict and layer). An earlier, longer packet for the 27B and 32B only is `verification/finding5_label_identity.md` (22-23 Oct).

## The claim in plain words

Two prompts list the same five entities in a different order and ask about different entities (the original about one, the donor about another). We copy the donor's hidden states at the last two tokens (":" of "Answer:" and the space after it) into the original run, at one layer. Every possible outcome is a different digit, so the answer shows what the copied tokens carried: the original's own answer (nothing moved), the digit of the original's sentence at the same place k as the donor's asked sentence (an order label, "position"), the digit of the original's sentence about the donor's entity (the bridge's identity), or the donor's own digit (the copy came too late, "value"). When the donor asks its 1st or 2nd sentence, the answer goes to the same place far more often than to the same entity; from the 3rd sentence on, it goes to the same entity at least as often as to the same place.

## The rule, fixed before the runs

`scripts/finding5_confirm.py` docstring, committed at 6538445 (22 Oct 18:50 +0200) with the first specs that use it; `jobs/d3/qwen3_32b_d3v4_seed2_swap.yaml`:

> memory -> prompt, the donor's last two tokens copied at the decisive layer, items split by the place k of the donor's asked statement; A: 1st and 2nd pooled, position - identity with its entity-cluster 95% lower bound > 0; B: 3rd-5th pooled, identity - position >= 0 (point) with its lower bound >= -0.05; confirms iff A and B, partly if one, fails if neither. [...] Decisive layer: the last of 48, 49, 50 whose donor-digit share has its Wilson upper bound < 0.10 (the fixed rule the other models' layers follow), read before the split.

Lists of 8 and 12 sentences: the same rule with B pooling the 3rd to the last sentence, generalised at 3c0daa1 (22 Oct 23:55 +0200) before any 8- or 12-sentence run. Qwen3.6-27B: layer 50 fixed (chosen after its first runs); every other model and the 27B's longer lists: the donor-digit rule over the run's swept layers. Intervals: the original's asked entity resampled with replacement within its topic, 4,000 draws, seed 0. The grid calls "confirms" holds and "partly" fails (partly). Muse's draw-1 spec adds a gate: a same-size random push at the last two tokens must change at most 30% of answers.

## Headline (recomputed)

- 37 cells (8 models x draws 1-3 and lists of 8 and 12; Olmo-Hybrid draw 3 and Gemma's longer lists have no run): 36 hold, 1 fails partly (Qwen3-32B draw 1).
- 1st-2nd sentence, position minus identity: +24 to +98 points (27B +69 to +98, 32B +73 to +92, 122B +30 to +80, Muse +56 to +79, Olmo-Hybrid +52 to +79, 9B +51 to +57, OLMo-3 +40 to +51, Gemma +24 to +33).
- 3rd on, identity minus position: +5 to +50 points; smallest on Muse at 12 sentences (+4.6 [+0.0, +10.2]) and on the 27B and 32B (+12 to +32).
- Qwen3-32B draw 1: +92 / +2.9 [-5.5, +10.7]: B misses its -5 bar by half a point.
- The same-size random push changes 0-17% of answers on every model but Gemma, where it changes 98-99% (reported; only Muse draw 1's spec makes it decisive; the 27B's draw 1 has no random-push row at layer 50).

## Worked examples (random items, `random.Random(0)` over the sorted ids of each half, Qwen3.6-27B's third draw: fresh scenes, rule fixed before the run, layer 50)

Reproduce with `uv run python verification/finding5_2026-10-23/recompute.py --example`. Run `results/pointer_swap/d3v4_seed3_swap_27b/`; the prompts are in `data/pointer_v4/seed3/countries_RL_e5f0.json`.

Item `countries-RL-e5f0-0017` (the donor asks its 1st sentence):

- Original: "Drawer 4 holds the Japan file. Drawer 1 holds the Russia file. Drawer 2 holds the Lebanon file. Drawer 6 holds the Greece file. Drawer 5 holds the Syria file. In which drawer is the file on the country whose capital is Beirut?" Answer 2 (Lebanon).
- Donor: "Drawer 7 holds the Greece file. Drawer 1 holds the Syria file. Drawer 5 holds the Japan file. Drawer 2 holds the Russia file. Drawer 4 holds the Lebanon file. In which drawer is the file on the country whose capital is Athens?" Asks its 1st sentence (Greece), answer 7.
- Outcomes: 2 = nothing moved, 4 = the original's 1st sentence (position), 6 = the original's Greece sentence (identity), 7 = the donor's digit (value).
- Patched answer: 4, the order label.

Item `countries-RL-e5f0-0260` (the donor asks its 3rd sentence):

- Original: "Drawer 6 holds the Thailand file. Drawer 2 holds the Turkey file. Drawer 8 holds the Ireland file. Drawer 7 holds the Austria file. Drawer 9 holds the Venezuela file. What drawer keeps the file on the country whose capital is Caracas?" Answer 9.
- Donor: asks about the capital Vienna (Austria), its 3rd sentence, answer 1.
- Outcomes: 9 = nothing moved, 8 = position, 7 = identity, 1 = value.
- Patched answer: 9, nothing moved. This is a real draw: from the 3rd sentence on, many answers do not move (27B draw 3: 27% unchanged, 37% identity, 22% position).

## Where the numbers come from

- `results/pointer_swap/<run>/outcomes.jsonl`, one row per item, condition and layer: `family`, `domain`, `name` (item id), `layer`, `group`, `source`, `level`, `top`, `role`. Decisive rows: `family == "RL"`, `source == "dissoc"`, `group == "last"`, the decisive layer; for 8 and 12 sentences `level == "e8-digit"` / `"e12-word"`.
- k (the place of the donor's asked sentence) and the entity cluster come from the item files pinned in `manifest.json` (`items`, sha256-checked by the script): `slots.position + 1` and `domain:query`.
- The saved verdicts the grid read are in `results/finding5_confirm/<run>_<stamp>/verdict.json`; four cells (27B draws 1-2, 32B draw 1, Muse draw 1) were computed by the grid from the outcomes. The recompute ignores both and starts from the outcomes.
- The run behind every cell is in `recompute.py` (`RUNS`) and in README, "Runs", finding 5.
