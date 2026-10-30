# Hand-check findings

A log of issues found during the manual hand-check (Dan's reading of the review tool's items), each with the check that followed it.
One entry per finding. A new finding is appended here, in this format, in the same commit as its check. Nothing here is a verified
result: see VERIFIED.md. Status: **closed** (checked, nothing to change or the change is made), **limitation** (a stated limit
remains), **not done** (a check is still open).

**Sample (30 Oct).** Hand-checked on a sample: 46 items across views a-g (5-10 per view, fixed in advance), all consistent; 6 issues (F1-F6) and 6 observations (O1-O6) below, none changes a headline claim.

## F1. The answer control used English answer words only

- **Found on.** Muse Glimmer 30B, layer 26, run `muse30_x51_12_e1_r2` (51.12 E1, the answer control), scene
  `P2-L0-0095`: atom 4 of the change's 25 atoms is `，三` (Chinese "three", the recall's original answer), classed "other"; atom 10 is
  ` oito` (Portuguese "eight", another number). The 51.12 label "the answer word is not read" rests on the English number word's lens
  rank (` three`: 61).
- **What.** The answer directions of arms 2 and 3 and the atom classifier contained English number words, ordinals and digits only, so
  an answer carried by a word in another language would have been removed with the rest of the lens part and counted as the item.
- **Check run.**
  - CPU, commit 9a34b0b5, `scripts/atoms_multilingual.py`, `results/atoms_multilingual/20261030T204008Z`: the saved atoms of the f5 items
    (250), classified again with number words 1-10 in eleven languages, Roman numerals (two letters or more),
    ordinals and digits.
  - GPU (H100 PCIe), commit 1d3655b8, `scripts/answer_translation_check.py`, `runs/answer_translation_check/muse-glimmer-30b/full`:
    the lens readout at layer 26 rebuilt for the 200 items of the run; the answer ranked as the best over its whole-token
    translations. Pre-flight matched (` three` 61, ` seven` 131; stored ranks 200 of 200).
- **Pre-set rule.** CPU: redraw f5 only if the answer share exceeds 0.05 of the lens part's energy on any model. GPU: flips of 5% of
  the items or fewer mean "translation does not change the verdict"; more than 5% is reported only.
- **Result.**
  - CPU: the answer carries at most 0.002 of the lens part's energy on average (f5 items; 8 of 250 have an answer atom, 5 of them in
    another language, e.g. `，三`, ` prima`). The 0.05 bar is not met on any model. For `P2-L0-0095` alone the answer atoms hold 0.07.
  - GPU, Muse: labels (not read / read) 199 / 1 before and after; 0 flips of 200, Wilson 95% interval [0, 0.019]. 188 of 200 items
    have an answer in a language with no single-token translation for some value (Japanese for 1, 6, 7, 8, 10; Ukrainian for 4, 8),
    so those translations could not be checked.
- **Summary for Zach (final, 30 Oct).** The answer control (51.12) used English number words as the answer directions. Redone with the answer in any language (single-token translations; about 100 directions per item against 15), post hoc, on the 9B, 27B and Muse (Lightning and the 122B not run):

  | model | (a) answer directions only, beyond a size-matched random part | (b) raw: "lens part out, answer kept" blocks, English -> any language | (b) beyond K random directions kept | label of the recall's arms |
  |---|---|---|---|---|
  | 9B | +0.005 [0.000, 0.018]: no | 0.503 -> 0.289 | -0.024 [-0.061, 0.011] | the item (entity) |
  | 27B | +0.040 [0.006, 0.082]: yes | 0.707 -> 0.467 | -0.015 [-0.059, 0.035] | mixed |
  | Muse | +0.085 [0.018, 0.154]: yes | 0.678 -> 0.483 | -0.009 [-0.074, 0.071] | mixed (the readout case "the answer word is not read" is unchanged: 0 of 200 labels flip) |

  The (b) shift, arm 2 blocking less with the larger answer set, is explained by the number of directions kept: random directions of the same count do the same. The labels therefore rest on (a): the item on the 9B, mixed on the 27B and Muse; the answer in other languages is a small part of the recall's switches there, not the whole of it. Rule (b) had no size control (Dan's design error); the K-random control was added afterwards.
- **Effect on claims.** f5 unchanged. The 51.12 English verdicts are unchanged; the post hoc labels above are in the depth README (Part I row and caveat) and the EXPERIMENTS 51.12 table, tagged post hoc, with the figure `ledger_answer_control.png` redrawn (the English bars as before, the any-language bars hollow, the K-random twins as the control). One caveat line is in the answer-control section of the depth README.
- **Status.** Limitation (Lightning and the 122B not run). The label check is closed; the translated-arms check and its size control are done, post hoc, on the 9B, 27B and Muse (detail below).
  Post hoc attempt (30 Oct, `scripts/answer_arms_translated.py`, `runs/answer_arms_translated/muse-glimmer-30b/preflight_stop_20261030`):
  stopped at the pre-flight. The English-only set through the new driver reproduced the saved `muse30_x51_12_e1_r2` switches in
  3197 of 3200 rows, not all: three arm counts differ by 1 (recall `no_jpp_rand` 123 vs 122 saved, recall `no_A_rand` 117 vs 118,
  lookup `no_jpp_rand` 61 vs 62); all other counts equal. The all-languages arms were not run.
  Second gate (pre-set by Dan before the rerun, written to `runs/answer_arms_translated/muse-glimmer-30b/run2/manifest.json` first):
  the non-random arms must match the saved counts exactly, every random-twin arm within ±1 switch; for each differing row the
  top-1 vs top-2 logit margin in this run and in the saved run must both be < 0.5 ("numerical noise, confirmed"), else stop.
  Note: the saved run's manifest has `code.dirty = true` (sha 15938ce4), so the saved numbers were not produced from a clean checkout.
  Result: counts passed (same 3 rows differ, all random-twin arms, by 1). Margins: P2-L0-0037 recall `no_jpp_rand` 0.25 now / 0.0
  saved; P2-L0-0044 recall `no_A_rand` 0.125 / 0.125; P2-L0-0093 lookup `no_jpp_rand` 0.0 now (this row's standalone re-read
  gives a different top token than the driver's row, itself a tie) / 0.125 saved. The saved margins are not stored: they are inferred
  from the saved `ld` (alt minus org logit) because the top two were the alt and org answer tokens. All three below 0.5: numerical noise,
  confirmed. The all-languages arms then ran (post hoc; same run, items, layer 26, seed, lens; 200 items; answer directions 14.9 per
  item English, 102.0 all languages; share of ||Δ||² in A 0.0099 → 0.0521; size-matched random parts rebuilt).
  Pre-set rule (unchanged): the claim changes only if, on the recall, (a) arm 3 (answer directions only, all languages) beats its
  size-matched random part with the 95% interval excluding 0, or (b) arm 2 (without the lens part, answer directions kept) blocks a
  different share from the English-only arm with non-overlapping intervals. Result: (a) holds. Recall, arm 3, extra loss (S_rand − S_arm)/S_whole
  = 0.085, 95% cluster-bootstrap interval [0.018, 0.154] (English-only: −0.017 [−0.055, 0.014]); switches blocked 6 of 118 against −4
  for the random part. (b) does not hold: arm 2 blocks 0.678 [0.521, 0.788] English-only, 0.483 [0.362, 0.585] all languages (overlap).
  Lookup: unchanged ("can't tell": arm 1 has no extra loss beyond random). The code's label for the recall moves from "the lens effect
  is the entity" to "mixed" (arm 2 keeps 0.5 / 0.771 of arm 1's extra loss, below its 0.7 bar). By the pre-set rule the claim changes
  on Muse; the lower end of (a)'s interval is 0.018 and the random part's count is negative, so it is a thin margin. The README and deck
  are not edited; this needs your decision.
  Same check on the 9B and the 27B (30 Oct, post hoc, same driver, same two gates, same decision rules, same manifest text with no change, so the
  manifest's "what" line still says "Muse only"; weights downloaded to the pod; `runs/answer_arms_translated/qwen3.5-9b/run_qwen3.5-9b`,
  `runs/answer_arms_translated/qwen3.6-27b/run_qwen3.6-27b`; the saved runs `qwen35_9b_x51_12_e1_r2` and `x51_12_e1_27b_r2`, both with `code.dirty = true`, sha 15938ce4).
  9B: second gate passed (3199 of 3200 rows equal; one random-twin count differs by 1; P2-L0-0269 PP no_jpp_rand: saved 0, now 1, margin now 0.0, saved (inferred) 0.125; numerical noise, confirmed). Directions per item 14.9 English, 98.49 all languages. Recall: arm 3 extra +0.005 [+0.000, +0.018] all languages (+0.000 [+0.000, +0.000] English only), so (a) does not hold; arm 2 blocks 0.503 [0.416, 0.585] English only and 0.289 [0.212, 0.371] all languages, so (b) holds. By the pre-set rule the claim changes on the 9B: the recall's arm label the lens effect is the entity -> mixed; the lookup's can't tell (arm 1 has no extra loss beyond random) -> can't tell (arm 1 has no extra loss beyond random).
  27B: second gate passed (3199 of 3200 rows equal; one random-twin count differs by 1; P2-L0-0188 PM no_jpp_rand: saved 1, now 0, margin now 0.375, saved (inferred) 0.0; numerical noise, confirmed). Directions per item 14.86 English, 97.08 all languages. Recall: arm 3 extra +0.040 [+0.006, +0.082] all languages (+0.027 [+0.006, +0.054] English only), so (a) holds; arm 2 blocks 0.707 [0.596, 0.799] English only and 0.467 [0.356, 0.556] all languages, so (b) holds. By the pre-set rule the claim changes on the 27B: the recall's arm label the lens effect is the entity -> mixed; the lookup's the lens effect is the entity -> mixed.
  Limitation: Lightning and the 122B were not run (their weights were not downloaded; timebox). Muse, 9B and 27B all move to mixed on the recall; the README carries Muse only, the 9B and 27B results are here and not yet in the README or deck.

  **Design error in rule (b), logged (Dan 30 Oct):** rule (b) compared arm 2 across two answer-direction sets of different sizes (about 15 English, about 100 all languages) without a control for the number of directions kept; the pre-set rule had no size control. Post hoc control, `scripts/answer_arms_krand.py` (same runs, items, layer, seed, lens and reads as the arms check; `runs/answer_arms_krand/<model>/`): arm 2 with K random token directions kept instead of the answer directions (letter tokens that are whole alphabetic words of at least 2 letters, excluding the item's answer words in every language and its old and new bridge words; built with `answer_basis` over the lens vectors), K = the item's all-language count (mean 98-102) and, separately, its English count (mean 14.9); 5 draws per item, averaged. Pre-set: the (b) shift is answer-specific only if [all-language arm 2 minus its K-random twin] minus [English arm 2 minus its K-random twin] has a 95% interval excluding 0, else "(b) shift is explained by the number of kept directions" and the label rests on (a) alone. The gates passed (whole and both arm 2 counts within 1 of the saved run; the 27B first read in batches of 14 rows and missed by 3 on the English arm 2 (47 vs 44), so it was rerun reading 8 rows per batch as the saved run did, `krand_b8`, then equal).
  Muse: share of the whole change's switches blocked (recall): arm 2 English 0.675, its K-random twin 0.670; arm 2 all languages 0.479, its twin 0.482. Arm 2 minus twin: English +0.005 [-0.031, +0.038], all languages -0.003 [-0.054, +0.060]; the difference of the two (b beyond K-random) -0.009 [-0.074, +0.071]: (b) shift is explained by the number of kept directions.
  9B: share of the whole change's switches blocked (recall): arm 2 English 0.502, its K-random twin 0.499; arm 2 all languages 0.289, its twin 0.311. Arm 2 minus twin: English +0.003 [-0.018, +0.023], all languages -0.021 [-0.057, +0.010]; the difference of the two (b beyond K-random) -0.024 [-0.061, +0.011]: (b) shift is explained by the number of kept directions.
  27B: share of the whole change's switches blocked (recall): arm 2 English 0.707, its K-random twin 0.723; arm 2 all languages 0.467, its twin 0.497. Arm 2 minus twin: English -0.016 [-0.058, +0.017], all languages -0.031 [-0.067, +0.007]; the difference of the two (b beyond K-random) -0.015 [-0.059, +0.035]: (b) shift is explained by the number of kept directions.
  Result: the (b) shift is explained by the number of kept directions on all three models; random directions of the same count hold as much of the effect as the answer directions do. The labels rest on (a) alone: 9B entity ((a) +0.005 [0.000, 0.018] does not hold), 27B mixed ((a) +0.040 [0.006, 0.082]), Muse mixed ((a) +0.085 [0.018, 0.154]). This supersedes the paragraph above that read the 9B as changing by (b).

  | model | (a) arm 3, all languages, beyond its random part | (b) raw: arm 2 share blocked, English -> all languages | (b) beyond K-random | final label (recall) |
  |---|---|---|---|---|
  | 9B | +0.005 [0.000, 0.018] | 0.503 [0.416, 0.585] -> 0.289 [0.212, 0.371] | -0.024 [-0.061, +0.011] (not answer-specific) | entity |
  | 27B | +0.040 [0.006, 0.082] | 0.707 [0.596, 0.799] -> 0.467 [0.356, 0.556] | -0.015 [-0.059, +0.035] (not answer-specific) | mixed |
  | Muse | +0.085 [0.018, 0.154] | 0.678 [0.521, 0.788] -> 0.483 [0.362, 0.585] | -0.009 [-0.074, +0.071] (not answer-specific) | mixed |
  Lightning and the 122B were not run (limitation).

## F2. Recall route collision in C2

- **Found on.** Qwen3.5-9B, routes test C2 scenes, scene `C2-0538`: the position-route entity (deer, original slots deer / crow / bear) and the
  changed entity (bear) both have 4 legs, so a recall that follows the position gives the changed answer too.
- **What.** In the routes test's C2 scenes (another item moves), the entity at the slot the changed pick occupies, in the original
  prompt, can have the same answer as the changed item. A recall switch there cannot be told apart from following the position.
- **Check run.** CPU, commit d6e5605a (intervals and seed-29 examples added in 21415c60), `scripts/c2_route_collision.py`,
  `results/c2_route_collision/20261030T210732Z`; saved scenes and rows only.
- **Pre-set rule.** None for the collision count (descriptive). For the x8 swap claim the same class rule as before, recomputed on
  scenes where the swapped-in item's answer differs from both the third and the original item's.
- **Result.**
  - Collisions / n: 9B 114 / 300, 27B 108 / 300, 122B 129 / 300, Muse 93 / 300, Lightning 101 / 300 (31-43%).
  - The x8 claim "of the changed recalls, the share naming the swapped-in item's answer": on all scenes 0.85 (9B, n = 129,
    [0.79, 0.89]) and 0.85 (Lightning, n = 164, [0.79, 0.91]); on non-colliding scenes 0.82 (9B, n = 73, [0.74, 0.90]) and 0.81
    (Lightning, n = 91, [0.75, 0.89]) (cluster bootstrap over the bridge entity; `tables.json`, key `swap_claim`).
- **Effect on claims.** The x8 claim holds on non-colliding scenes; both numbers are in the depth README. No recall route claim is made
  in C2, and any future one must exclude colliding scenes (caveat added to the depth README).
- **Status.** Limitation.

- **Second check, the address swap's changed recalls (post hoc, CPU, `scripts/x8_target_legs_check.py`, `results/x8_target_legs_check/20261030T214423Z`).** The share of recalls changed by the swap,
  on all rows and on the rows where the target item's legs differ from the original item's (where a change is possible), 95% cluster-bootstrap
  intervals over the bridge entity; all rows -> non-colliding rows. Example `C2-0047` (bee and butterfly, 6 legs; 9B, 27B, 122B): the write to the
  bee slot is a collision. Random vectors are stored at s = 1 and 4 only. Per model (600 rows = 300 scenes x 2 targets): 9B: collisions 93/600 (0.155); write s = 1: 0.040 [0.022, 0.062] -> 0.045 [0.024, 0.072]; s = 2: 0.215 [0.165, 0.276] -> 0.243 [0.182, 0.322]; s = 4: 0.427 [0.374, 0.480] -> 0.477 [0.413, 0.548]; random s = 1: 0.005 [0.000, 0.016] -> 0.004 [0.000, 0.013], s = 4: 0.030 [0.011, 0.055] -> 0.022 [0.006, 0.044]. 27B: collisions 95/600 (0.158); write s = 1: 0.007 [0.000, 0.015] -> 0.008 [0.000, 0.018]; s = 2: 0.043 [0.015, 0.082] -> 0.045 [0.017, 0.084]; s = 4: 0.113 [0.066, 0.172] -> 0.127 [0.075, 0.191]; random s = 1: 0.000 [0.000, 0.000] -> 0.000 [0.000, 0.000], s = 4: 0.005 [0.000, 0.013] -> 0.006 [0.000, 0.015]. Muse: collisions 122/600 (0.203); write s = 1: 0.007 [0.000, 0.022] -> 0.008 [0.000, 0.028]; s = 2: 0.058 [0.029, 0.098] -> 0.061 [0.028, 0.104]; s = 4: 0.107 [0.064, 0.160] -> 0.109 [0.060, 0.174]; random s = 1: 0.003 [0.000, 0.009] -> 0.004 [0.000, 0.011], s = 4: 0.010 [0.000, 0.026] -> 0.011 [0.000, 0.030]. Lightning: collisions 99/600 (0.165); write s = 1: 0.020 [0.004, 0.041] -> 0.022 [0.005, 0.043]; s = 2: 0.273 [0.217, 0.329] -> 0.317 [0.254, 0.380]; s = 4: 0.398 [0.318, 0.473] -> 0.469 [0.383, 0.549]; random s = 1: 0.002 [0.000, 0.005] -> 0.000 [0.000, 0.000], s = 4: 0.013 [0.004, 0.024] -> 0.014 [0.005, 0.025]. 122B: collisions 94/600 (0.157); write s = 1: 0.032 [0.017, 0.051] -> 0.034 [0.018, 0.055]; s = 2: 0.227 [0.175, 0.291] -> 0.249 [0.186, 0.336]; s = 4: 0.447 [0.375, 0.526] -> 0.490 [0.402, 0.596]; random s = 1: 0.017 [0.004, 0.033] -> 0.014 [0.003, 0.029], s = 4: 0.032 [0.015, 0.053] -> 0.028 [0.011, 0.051].
  The all-rows share at s = 2 equals the README's reported value on every model. Pre-set rule: the non-colliding share differs from the reported one by
  at most 0.0441 (Lightning; 9B 0.028, 122B 0.022, 27B 0.002, Muse 0.002), under the bar 0.05, so the README gets a caveat line only. The
  draft is in `draft_readme.md` in that folder, not applied.

## F3. The bridge class held English words only

- **Found on.** Dan's hand-check (30 Oct), by the same reading as F1: the classes of the 25 atoms recognized the bridge word in English
  (and its spelling: first token, initial, prefix, alias), not its translations or symbol forms (crow / ворона / Krähe; gamma / γ / Γ; eta / η / Η).
- **What.** The saved old / new bridge classes are English rules; a bridge atom in another language was classed "other".
- **Check run.** CPU, post hoc, saved atoms, `scripts/bridge_multilingual.py`, `results/bridge_multilingual/20261030T213703Z` (same inputs, normalization and single-token rule as
  9a34b0b5). Forms: the 43 old / new bridge words of the f5 items in ten languages plus Greek names and symbols; the chemical symbols He / Li
  (case-sensitive, weak).
- **Pre-set rule.** An atom that is a bridge atom and an answer atom goes to "both", never to either; redraw f5 only if the bridge share changes by more
  than 0.05 on any model.
- **Result.** Bridge share (old + new bridge energy share, f5 items, 50 per model, 95% cluster-bootstrap interval over the bridge entity), English -> any
  language: 9B 0.221 [0.191, 0.246] -> 0.221 [0.191, 0.246]; 27B 0.214 [0.181, 0.248] -> 0.214 [0.181, 0.248]; Muse 0.374 [0.341, 0.400] -> 0.376 [0.346, 0.400]; Lightning 0.201 [0.169, 0.231] -> 0.205 [0.173, 0.234]; 122B 0.305 [0.269, 0.342] -> 0.305 [0.269, 0.342]. The largest change is 0.0038 (Lightning): the bar 0.05 is not met on any model. "Both": 0 on every model. Sign split: of the bridge
  energy, every atom is sign-correct (old bridge -, new bridge +) except 0.0007 on the 9B and 0.0014 on the 122B (sign-correct share equals the bridge share, English and any
  language, on the 27B and Muse; Lightning 0.201 -> 0.205). Newly classed atoms: 0 on the 9B, 27B and 122B; 2 distinct on Muse (` Helio`, ` Эта`) and 3 on Lightning
  (` loup`, `馬`, ` кот`); both views carry the same atoms, so the pooled counts in `tables.json` list each twice. The 5 largest: ` loup` (French, old bridge, -, 0.023), `馬`
  (Japanese, new bridge, +, 0.018), ` кот` (Russian, new bridge, +, 0.013), ` Helio` (Spanish, old bridge, -, 0.009), ` Эта` (Russian, new bridge, +, 0.004).
- **Effect on claims.** f5 is not redrawn. The bridge share goes up, by at most 0.004. I did not check the link to Claim 3 (the README's claim 3 is about
  the recall reading the item's earlier mention); the check only shows the English-only class undercounted the bridge by under 0.005.
- **Status.** Closed.

## Checked, not bugs

- **Muse `P2-L0-0095` (run `muse30_x51_12_e1_r2`, layer 26): the lookup did not switch.** Dan's reading: the locker sentence comes after
  the pick. The whole change does not switch the lookup (it stays on 6; original 6, changed 2). Not a labeling error.
- **Same item: the recall's blocked-beyond-random count is +0 in every arm.** The recall still switches to 7 without the lens part,
  without the lens part with the answer directions retained, and without the answer directions only, and equally without each
  same-size random part, so the item adds nothing to any arm's count. Consistent with the stored numbers; not a bug.
- **27B `C2-0128` (run `x6_routes_27b`), the lookup: identity under the whole change (5), position under pointer removal (2).** Not a
  bug: it is one of 0-3 such scenes per model. Post hoc, CPU, `scripts/c2_route_crosstab.py`, `results/c2_route_crosstab/20261030T212820Z`
  (lookup, C2, n = 300 scenes per model). Identity -> position without the pointer directions, beside the size-matched random part:
  9B 3 (random 18), 27B 2 (random 1; `C2-0128`, `C2-0200`), Muse 2 (random 6), Lightning 0 (random 10), 122B 0 (random 7). At or
  below the random arm on four models; on the 27B it is one scene above (2 vs 1). Without J++ the same cell is 35 / 36 / 8 / 22 / 26
  (random 17 / 0 / 4 / 11 / 5). Paired differences with 95% cluster-bootstrap intervals are in `tables.json` (`contrasts`); the
  README reports route shares per arm over all scenes (55 values compared, all equal), not scene-by-scene changes. A draft paragraph
  and table are in `draft_readme.md` in that folder, not applied.
- **Status.** Closed.

## Observations

### O1. The recall's route under J++ removal and the pointer, C2, non-colliding scenes (post hoc, descriptive)

- **Found on.** 122B, scene `C2-0418` (run `qwen35_122b_x6_routes_keeponly_g75`): the recall answers 2 (identity: the changed pick, a chicken)
  under the whole change; 6 (position: the butterfly now at that slot's old place) without J++ and with only the pointer directions.
- **What.** Whether the recall's answer goes to the position route when J++ or the pointer directions are changed, with a size-matched
  random arm beside each; on the scenes where identity and position cannot be confused (no collision, `scripts/c2_route_collision.py`).
- **Check run.** CPU, post hoc, `scripts/c2_recall_route_crosstab.py`, `results/c2_recall_route_crosstab/20261030T213031Z`. Saved x6_routes arms, C2, recall (PM), runs: 9B
  `qwen35_9b_x6_routes_keeponly`, 27B `x6_routes_keeponly_27b`, Muse `muse30b_x6_routes`, Lightning `nem35l_x52_routes`, 122B
  `qwen35_122b_x6_routes_keeponly_g75` (the runs that hold `keep_alf`; their own `whole`). Route of the recall's top token: identity = the
  changed item's legs, position = the legs of the item at that slot in the original, original, other (precedence in that order).
- **Pre-set rule.** None (descriptive).
- **Result.** n of non-colliding scenes (9B / 27B / Muse / Lightning / 122B): 186 / 192 / 207 / 199 / 171. In 93 / 95 / 122 / 99 / 94 of them the position
  item's legs equal the original answer, so position and original cannot be told apart there (they are read as position). On the scenes
  where the original, changed and position legs all differ, n = 93 / 97 / 85 / 100 / 77, identity -> position (arm, size-matched random in
  brackets): without J++ 8 (3) / 2 (0) / 0 (1) / 13 (1) / 6 (2); without the pointer
  1 (4) / 0 (0) / 0 (1) / 1 (5) / 3 (1); with only the pointer 4 (0) / 0 (0) / 0 (0) / 9 (0) / 3 (0).
  Position -> identity without the pointer: 6 (1) / 3 (0) / 0 (0) / 16 (4) / 4 (1). On all non-colliding scenes
  identity -> position with only the pointer is 76 (73) / 49 (51) / 32 (33) / 75 (68) / 71 (70), close to the random arm's; in the scenes where
  the position legs equal the original answer an original answer counts as position, which is why this cell is large. Full 4 x 4 tables per model, arm and subset in `tables.md`.
- **Effect on claims.** None; README and deck not edited.
- **Status.** Observation, not checked further.

### O2. Is the address verbalizable by the J++ lens? (post hoc, CPU + one GPU stage; pre-set rule)

- **Found on.** Dan's question (30 Oct): whether the address (the locker-slot pointer) is readable by the lens as a position word, rather than as a part of the representation the lens cannot read.
- **What.** (a) The six address-swap directions mu_k - mu_j (x8_write) decomposed over each model's J++ letter dictionary with the depth view's signed 25-atom OMP, scored
  against position classes (ordinals of slot k / j, 0- and 1-based, cardinals of the slot index, generic position words; eleven languages, whole-token rule). (b) For 30 random
  C2 scenes (seed 29), the real change's component inside the pointer directions (U U^T Delta, Alf), Muse only.
- **Check run.** CPU, post hoc, `scripts/address_verbalizable.py`, `results/address_verbalizable/20261030T214526Z`; heads of Muse, Lightning and the 122B fetched by byte range
  (`cache/x52_atoms/`, not committed); stage (b) on the H100 pod, `scripts/address_verbalizable_delta.py`, `results/address_verbalizable_delta/muse-glimmer-30b-20261030T214153Z`.
- **Pre-set rule** (written to the manifest first). "Verbalizable" only if on at least 3 of 5 models (1) the position atoms' energy share in (a) exceeds the random 95th percentile (100 random vectors,
  same norm, same OMP) and (2) a sign-correct ordinal (k with +, j with -) appears in the 25 atoms on at least 4 of 6 pairs and above the label shuffle. Otherwise "not verbalizable by the J++ lens at this layer; consistent with the claim".
- **Result.** Verdict by the rule: not verbalizable, 0 of 5 models meet either condition. 9B (L12): position-atom energy share 0.00000 vs random 95th percentile 0.00331; sign-correct ordinal on 0 of 6 pairs, shuffle 0.0, random mean 0.007; the 25-atom part captures 0.101 of the pointer basis energy (writes 0.078-0.082), random vectors 0.084; 27B (L32): position-atom energy share 0.00000 vs random 95th percentile 0.00000; sign-correct ordinal on 0 of 6 pairs, shuffle 0.0, random mean 0.01; the 25-atom part captures 0.068 of the pointer basis energy (writes 0.060-0.080), random vectors 0.067; Muse (L26): position-atom energy share 0.00000 vs random 95th percentile 0.00169; sign-correct ordinal on 0 of 6 pairs, shuffle 0.0, random mean 0.007; the 25-atom part captures 0.062 of the pointer basis energy (writes 0.059-0.066), random vectors 0.052; Lightning (L14): position-atom energy share 0.00058 vs random 95th percentile 0.00244; sign-correct ordinal on 0 of 6 pairs, shuffle 0.0, random mean 0.007; the 25-atom part captures 0.131 of the pointer basis energy (writes 0.073-0.112), random vectors 0.087; 122B (L33): position-atom energy share 0.00000 vs random 95th percentile 0.00000; sign-correct ordinal on 0 of 6 pairs, shuffle 0.0, random mean 0.0; the 25-atom part captures 0.100 of the pointer basis energy (writes 0.068-0.083), random vectors 0.100. (b) Muse: mean position-atom energy share 0.0010, ambiguous
  (cardinal equal to a locker digit) 0.0, the pointer component is captured 0.062; a sign-correct ordinal is among the 25 atoms in 5 of 30 scenes (random vectors: 0.7% per pair label); three of those scenes carry the atom ` erstes` ("first", German) with +, on moves to slot 0
  (the energy of each is about 0.003 of the vector). Per pair, the first ten atoms with sign and class, and three raw (b) scenes, are in `tables.md` of that folder.
- **Limits.** The 25-atom J++ part captures about as much of the address directions as of random vectors (0.06-0.13 vs 0.05-0.10), so the address lies almost entirely outside what the dictionary spans at these layers; the test has little power to
  find a weak position-word component. The atoms are the first ten selected (selection order, not sorted by energy). Digits are not letter tokens, so they are not in the dictionary. Only Muse has (b).
- **Effect on claims.** None; consistent with the claim that the address is outside the lens. README and deck not edited.
- **Status.** Observation.

### O3. Does the swap's "third" landing depend on the pair's distance? (post hoc, CPU)

- **Found on.** Lightning `C2-0111` (lookup, write 0 -> 2): original at s = 1, third (slot 1) at s = 2 and 4 (`example_C2_0111_lightning.json`).
- **What.** Third share (answers on the slot that is neither j nor k) for adjacent pairs (|k - j| = 1) against far pairs (|k - j| = 2), per model and dose, write and random arms; lookup, and the recall on non-colliding scenes (legs[k] != legs[j]).
- **Check run.** CPU, post hoc, `scripts/x8_pair_type.py`, `results/x8_pair_type/20261030T214905Z` (saved x8_write rows; 95% cluster-bootstrap intervals over the bridge entity; full class tables, n and the recall subsets in `tables.md`).
- **Pre-set prediction** (in the manifest first). An ordinal address predicts third share (far) > third share (adjacent), largest at s = 1 and falling at s = 4, and absent from the random arms. "Supported" only if far - adjacent excludes 0 on at least 3 of 5 models at s = 1 or 2 and the random arms show no such gap; otherwise "third is generic disruption".
- **Result.** By the rule: **third is generic disruption.** The write gap is above 0 on all 5 models at s = 1 or 2 (lookup), but the random arms also show one: the 27B at s = 4 (+0.019 [+0.001, +0.039]) and Muse at s = 4 (+0.043 [+0.013, +0.080]); the rule needs none. The dose pattern is not the predicted one: at s = 1 the gap is 0 on the 9B and 122B, +0.011 (27B), +0.026 (Lightning), +0.040 (Muse); it is largest at s = 2 or 4 (27B +0.237 at s = 4), not at s = 1, and it falls from s = 2 to s = 4 only on the 9B and Lightning (Muse is flat, 0.229 to 0.220; the 27B and 122B keep rising). Third share, adjacent / far, gap far - adjacent [95% interval], lookup (n per cell about 400 adjacent / 200 far):
    - 9B: write s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=2 0.010/0.172 gap +0.162 [+0.108, +0.216]; s=4 0.042/0.167 gap +0.125 [+0.069, +0.178]; random s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=4 0.000/0.000 gap +0.000 [+0.000, +0.000]
    - 27B: write s=1 0.000/0.011 gap +0.011 [+0.000, +0.025]; s=2 0.002/0.143 gap +0.141 [+0.103, +0.175]; s=4 0.049/0.286 gap +0.237 [+0.162, +0.307]; random s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=4 0.002/0.021 gap +0.019 [+0.001, +0.039]
    - Muse: write s=1 0.000/0.040 gap +0.040 [+0.018, +0.067]; s=2 0.032/0.261 gap +0.229 [+0.171, +0.288]; s=4 0.172/0.392 gap +0.220 [+0.143, +0.291]; random s=1 0.000/0.010 gap +0.010 [+0.000, +0.034]; s=4 0.003/0.045 gap +0.043 [+0.013, +0.080]
    - Lightning: write s=1 0.003/0.029 gap +0.026 [+0.003, +0.052]; s=2 0.018/0.162 gap +0.144 [+0.099, +0.192]; s=4 0.033/0.129 gap +0.095 [+0.049, +0.143]; random s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=4 0.000/0.000 gap +0.000 [+0.000, +0.000]
    - 122B: write s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=2 0.012/0.066 gap +0.054 [+0.019, +0.090]; s=4 0.065/0.188 gap +0.123 [+0.064, +0.185]; random s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=4 0.003/0.000 gap -0.003 [-0.009, +0.000]
  Recall, non-colliding scenes (n about 340 / 160): the write gap is above 0 at s = 1 or 2 on 2 of 5 models (Lightning +0.026 [+0.002, +0.052] at s = 2; the 9B's lower end is 0.0002 at s = 2), and the random arms show none; by the same rule: third is generic disruption. On the scenes where the three slots' legs all differ, the write gap is above 0 on 0 of 5 at s = 1 or 2. Recall:
    - 9B: write s=1 0.003/0.006 gap +0.003 [-0.008, +0.020]; s=2 0.006/0.025 gap +0.019 [+0.000, +0.042]; s=4 0.029/0.093 gap +0.064 [+0.026, +0.102]; random s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=4 0.006/0.006 gap +0.000 [-0.013, +0.018]
    - 27B: write s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=2 0.000/0.006 gap +0.006 [+0.000, +0.022]; s=4 0.000/0.019 gap +0.019 [+0.000, +0.041]; random s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=4 0.000/0.000 gap +0.000 [+0.000, +0.000]
    - Muse: write s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=2 0.006/0.006 gap -0.000 [-0.014, +0.018]; s=4 0.013/0.018 gap +0.006 [-0.022, +0.039]; random s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=4 0.000/0.000 gap +0.000 [+0.000, +0.000]
    - Lightning: write s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=2 0.009/0.035 gap +0.026 [+0.002, +0.052]; s=4 0.024/0.087 gap +0.063 [+0.026, +0.102]; random s=1 0.000/0.000 gap +0.000 [+0.000, +0.000]; s=4 0.000/0.000 gap +0.000 [+0.000, +0.000]
    - 122B: write s=1 0.000/0.006 gap +0.006 [+0.000, +0.023]; s=2 0.006/0.025 gap +0.019 [-0.003, +0.050]; s=4 0.017/0.056 gap +0.038 [+0.009, +0.074]; random s=1 0.000/0.006 gap +0.006 [+0.000, +0.023]; s=4 0.000/0.006 gap +0.006 [+0.000, +0.023]
- **Limits.** A far pair is a larger write than an adjacent one (the example's norms are 3.3 for 0 -> 1 and 4.0 for 0 -> 2 at s = 1; the random arm has the pair's norm), so distance and size are not separated; the random gap on the 27B and Muse at s = 4 is of that kind.
- **Effect on claims.** None; README and deck not edited.
- **Status.** Observation.

## F4. Z1-P (9B): passages where the lookup's changed answer is the true value of the original bridge

- **Found on.** 9B, `qwen35_9b_x52_z1p`, L12: sukiyaki-0 (b = Japan, which is sukiyaki's origin) and France-0 (b = Europe, France's continent).
- **What.** In these passages the lookup's changed answer b (the made-up value of the new bridge) equals the recall's original answer, the true value of the original bridge, so a lookup that falls back on memory of the original bridge looks like a switch.
- **Check run.** CPU, post hoc, `scripts/z1p_checks.py`, `results/z1p_checks/20261030T220056Z`; Z1's rule and computation (`x50_zach.layer_result`, paired cluster bootstrap over the original bridge entity, 10,000, seed 0).
- **Pre-set rule.** If the lookup's blocked-beyond-random moves by more than 0.05 or its interval stops including 0, report it as a change to the claim; otherwise a caveat line.
- **Result.** 23 of 200 passages (full-word equality; the first tokens are equal on the same 23). Blocked beyond random, 200 passages -> 177 without them: lookup -0.048 [-0.130, 0.034] -> -0.036 [-0.121, 0.050]; recall 0.589 [0.506, 0.673] -> 0.552 [0.464, 0.645]; gap 0.637 [0.511, 0.765] -> 0.588 [0.460, 0.720]; the rule still reads "the split holds on his passages". The lookup moves by 0.012 and its interval still includes 0.
- **Effect on claims.** A caveat line, not a change: the lookup number stays within 0.05 and includes 0; the recall number falls by 0.04 and the gap by 0.05.
- **Status.** Limitation.

### F4b. The recall's own passage
- **Check.** For every recall (PM) item, the recall's A and b as full words and as first tokens, in its own passage (original and changed).
- **Result.** A is absent from all 200 recall passages, as a word and as a first token. b is absent as a first token except one 1-character token, but as a full word it stands in the recall's own passage in 54 of 200 items (original and changed passage), as another entity's stated value (for example Adelaide-0: "India" in "This year's partner city for Barcelona is in India"). Without those 54 (n = 146): lookup -0.024 [-0.128, 0.086], recall 0.600 [0.500, 0.700], gap 0.624 [0.473, 0.775]. The lists are in `tables.json` (`F4b`).
- **Status.** Limitation (the recall's changed answer is available in its passage in 54 of 200 items; the number does not fall without them).

## F5. Z1-P (9B): answers read by a first token of one or two characters

- **Found on.** Huawei-0 ("A" = Austria), Uluru-0 ("E" = Ecuador).
- **What.** The count reads the answer's first token; when it has at most two characters ("A", "G", "Th") a token that starts another word reads as the answer.
- **Check run.** CPU count, `scripts/z1p_checks.py`, `results/z1p_checks/20261030T220056Z`: 96 items (scene x reader; 105 tokens, 83 scenes) have a stored tok_A or tok_b of at most two characters after stripping. GPU (H100 pod, the 9B loaded, `scripts/z1p_fulldecode.py`, `runs/z1p_fulldecode/20261030T221428Z`): those 96 items, greedy 4 tokens in each arm (none, whole, without the lens part, without a same-size random part) at L12, same Delta, same OMP and random part as the run; the stored first token was reproduced on 384 of 384 rows; each continuation labeled by the full word (original, changed, other).
- **Pre-set rule.** Recompute the z1p numbers if more than 5% of the arm rows change label.
- **Result.** 0 of 384 arm rows change label (0 in every arm; 0 ambiguous): the continuations are the whole words ("France", "Germany", "Thailand"), the same as the first token said. The rule is not triggered; the z1p numbers stand.
- **Effect on claims.** None.
- **Status.** Closed.

## F6. Z1-P (9B): the class rule, the display, the shared first token, the patch

- **Class rule.** The blocked-beyond-random count reads the answer's first token (`x50_zach.route` / `X.read_row`: top token = tok_b is the changed answer, = tok_A the original, else other). The review card's narrative compared the decoded top token with the whole answer word, so a first token read "another answer" while the arms table and the count said A or b (Mumbai-0, second passage: "Port" = A = Portugal under every arm, narrated "another answer"). Of 1,600 arm rows with a top token, 573 disagreed (lookup: unedited 94, whole 88, without the lens part 86, control 86; recall: unedited 61, whole 52, without 54, control 52); 0 after the fix in `bridge_jspace.review.page.answer_of`, which now follows the count's rule and names the word the token starts ("original answer (Mumbai's), the first token of 'Portugal'"). `tests/test_review.py` and `tests/test_review_questions.py` pass.
- **Shared first token.** 0 items have tok_A = tok_b (either reader); the encoder drops such passages ("O's and S's answers share their first token") and the verify check requires them to differ.
- **The four "only the scene's words differ" rows** (Mont Saint-Michel, Christ the Redeemer; two readers each): the check's word-level comparison flags tokens that are pieces of the landmark names. Mont Saint-Michel: index 77, "-M" (original) against " Rede" (changed), both inside the names ("Saint-Michel", "Christ the Redeemer"); Christ the Redeemer: indices 78 " Christ" / " the" and 79 " the" / " Col", inside the names too. They are not changes outside the landmark name; they fail the check because the check compares whole words. Without these two scenes (n = 198): lookup -0.048 [-0.129, 0.034], recall 0.584 [0.500, 0.669], gap 0.631 [0.504, 0.761] (full: -0.048 [-0.130, 0.034], 0.589 [0.506, 0.673], 0.637 [0.511, 0.765]).
- **Denominators.** The whole change switches 63 of 200 lookups and 163 of 200 recalls (no switch with no change). The lookup's -0.05 is 3 switches of 63 (56 still switch without the lens part, 53 without a same-size random part); the recall's 0.59 is 96 of 163 (52 and 148). The README's made-up-fact rows (Part V) do not state these denominators (its "lookups switched" row is for true facts). Draft, not applied: "Made-up facts, 9B: the whole change switches 63 of 200 lookups and 163 of 200 recalls; the blocked-beyond-random numbers are shares of those (the lookup's 3 of 63 more survive, the recall's 96 of 163 are blocked)."
- **The patch.** The change Delta = h_S - h_O is taken at one index, the last subtoken of the bridge name, and added to the original prompt's state there (`x50_zach` `AddRows` at `pos`, L12); `pos` is the span's last token in both prompts. Names with different token counts are not patched: the encoder requires equal prompt lengths, the name's last token at one index in O and S, and differences only inside the name, and drops a passage when no candidate bridge aligns (94 + 93 passages of the two sets: "no candidate aligns (the patch token is not at one index in O and S)"), so the kept passages pair names of equal token count. sukiyaki-0 (`jsuite_v2nb_test_chat`): "sukiyaki" = " su" (24) | "ki" (25) | "y" (26) | "aki" (27); "ratatouille" = " rat" (24) | "at" (25) | "ou" (26) | "ille" (27); both prompts have the length 220 (lookup) and 208 (recall); the patch index is 27 in both ("aki" -> "ille"); tokens 24-27 differ and no others.

### O4. Last token (51.10, view f): which writes move the answer from A to "other", and are those answers locker digits? (post hoc, CPU)

- **Found on.** Muse `P2-L0-0103`, recall: the lens swap, the rotated control and the random part at gain 2 all give "5", carbon's locker number in that scene, not the swapped-in entity's answer.
- **Claim wording changed (Dan 30 Oct).** README Part IV and the view's claim text: "does not move the answer" -> "does not switch it to the swapped-in entity's answer" (`docs/depth/README.template.md`, `docs/review/review_views.yaml`; `docs/review/verify_pack.md` regenerated). `docs/depth/EXPERIMENTS.md` still has the old wording in three places (the Lightning bullet, the "Why we asked" line and the 122B answer-map line); not changed.
- **Check run.** CPU, saved arms, `scripts/x51_10_other_answers.py`, `results/x51_10_other_answers/20261030T222427Z`. Over the items whose unedited answer is A, per arm at the last token at the reader's read peak: the share of items whose answer role is "other" (not A, not the swapped-in answer), 95% cluster bootstrap over the bridge entity; and how many of those answers are a digit equal to a locker number in the scene's context.
- **Result (recall, other-share [95% interval], items with "other", of which a locker digit).** 9B (n = 75): lens swap 0.053 [0.000, 0.125] (4 items, 1 a locker digit), random control 0.000 [0.000, 0.000] (0, 0), rotated control 0.040 [0.000, 0.091] (3, 0); 27B (n = 69): lens swap 0.015 [0.000, 0.046] (1 items, 0 a locker digit), random control 0.015 [0.000, 0.046] (1, 0), rotated control 0.029 [0.000, 0.075] (2, 0); Muse (n = 67): lens swap 0.045 [0.000, 0.089] (3 items, 2 a locker digit), random control 0.000 [0.000, 0.000] (0, 0), rotated control 0.030 [0.000, 0.071] (2, 1); Lightning (n = 58): lens swap 0.086 [0.020, 0.163] (5 items, 1 a locker digit), random control 0.017 [0.000, 0.057] (1, 0), rotated control 0.017 [0.000, 0.061] (1, 0). Lookup: 0 "other" under the lens swap and both controls on all four models.
  Flag (lens swap above both controls with intervals not overlapping): not raised on any model, either reader; Lightning's recall is the closest (swap 0.086 [0.020, 0.163] against 0.017 [0.000, 0.057] and 0.017 [0.000, 0.061]; the intervals overlap). Of the lens swap's "other" answers, 1 of 4 (9B), 0 of 1 (27B), 2 of 3 (Muse), 1 of 5 (Lightning) are a locker digit, and all of them are digits. Beside the question: the J++ part at gain 2 moves the recall to "other" more than its random part on Muse (0.224 [0.100, 0.357] against 0.045 [0.000, 0.095]; 6 of 15 are locker digits) and not on the 9B (0.200 against 0.120), the 27B or Lightning (0.293 against 0.207).
- **Effect on claims.** None beyond the wording. Nothing else was changed.
- **Status.** Observation.

### O5. View g recount: the four "no source" numbers (30 Oct)

- **Which.** Lightning's sentence-order counts: `lk_order_before_lightning_k` (73) and `_n` (85), `lk_order_after_lightning_k` (17) and `_n` (115); the two shares beside them (0.859, 0.148) matched `data.csv`.
- **Why.** `scripts/x0_details.py` builds `docs/depth/x0_numbers.json` (and so the `numbers` rows of `data.csv`) for the four original models only; Lightning's X0 conflict run (`nem35l_x52_conflict`, L14) was added later and its k and n were never written, only its shares (from a figure's rows).
- **Fix.** Traced to `results/x0_necessity/nem35l_x52_conflict/outcomes.jsonl` (whole-change lookups at L14 by the locker sentence's order; the recount's own counts) and added six keys (the share, k and n for before and after) to the generator, `docs/depth/x0_numbers.json` and the `numbers` tail of `data/figures/depth/data.csv`. Recount of view g: 30 rows, 0 no source, 0 mismatch.
- **Script paths (fixed, 30 Oct).** `scripts/x0_details.py` wrote to `docs/` and read its template from there; the page and its numbers moved to `docs/depth/`, so it could not be rerun. `DOCS` now points to `docs/depth`. Rerun as is: `docs/depth/x0_numbers.json` is reproduced key for key (5,390 keys, the six Lightning keys included) except `pred_n`, and `docs/depth/x0_details.md` is reproduced unchanged.
- **`pred_n`.** It is the number of scored predictions, read by `predictions_numbers()` from the calibration line of `predictions/README.md` ("Batches 25-46 so far (122 scored answers with a confidence): mean Brier 0.32 ... 59 of 122 top options happened"). That line now says 122; the saved file has 121, from before the line was updated. It feeds one README line (the section "How we checked", "Predictions: ... mean Brier 0.32 over 121 answers", with `pred_brier`, unchanged at 0.32) and its `data.csv` row. Regenerating would change that README number from 121 to 122 (the Brier stays 0.32); I did not regenerate it: the committed `x0_numbers.json` and `data.csv` still say 121, so the README is one behind `predictions/README.md` until you decide. No deck is in the repo; if the deck quotes "121" it would be the same one-behind number.
- **Status.** Closed.

### O6. Claim 10 (sentence order) with both orders: the original prompt's and the changed prompt's locker sentence (post hoc, CPU)

- **Note on the id.** Asked as O4; O4 was already taken (the x51_10 check), so this is O6.
- **Found on.** Muse `P2-L0-0208`, `P2-L0-0041`, `P2-L0-0040` (original after the pick, changed before, switched: confirmed, all three) and 27B `P2-L0-0152` (original before, changed after, not switched: confirmed).
- **What.** Claim 10 splits lookups by whether the original bridge's locker sentence came before the asked pick. The changed prompt swaps the pick to the new bridge, whose locker sentence sits elsewhere. The lookup's switch rate under the whole change in a 2x2 of the original bridge's locker sentence (before / after the pick) by the changed bridge's (before / after the same pick sentence).
- **Check run.** CPU, post hoc, `scripts/x0_order_2x2.py`, `results/x0_order_2x2/20261030T224216Z` (saved x0_necessity runs at each model's layer; 200 lookups per model, all in the 2x2; 95% cluster-bootstrap intervals over the original bridge entity; features from `x0_strata.features`: "org locker vs asked pick" and "alt locker vs asked pick").
- **Pre-set rule.** If the changed order's effect (averaged over the original order) is larger than the original order's on at least 3 of 5 models, with the intervals not overlapping, draft a reworded claim 10 naming the order that matters (or both); otherwise keep claim 10 and add the 2x2 as a caveat table.
- **Result.** Models where the changed order matters more with separate intervals: **0 of 5**. The original order's effect is the larger one on 4 of 5 (9B, 27B, Lightning, 122B); on Muse the changed order's is slightly larger, with overlapping intervals (+0.43 [+0.30, +0.52] against +0.38 [+0.30, +0.49]). Switch counts / n (rate [95% interval]) and the two effects (rate differences, 95% interval):

  | model | original before, changed before | original before, changed after | original after, changed before | original after, changed after | changed order's effect | original order's effect |
  |---|---|---|---|---|---|---|
  | 9B | 72/75 = 0.96 [0.92, 1.00] | 14/25 = 0.56 [0.33, 0.76] | 15/32 = 0.47 [0.33, 0.59] | 4/68 = 0.06 [0.01, 0.13] | +0.41 [+0.27, +0.54] | +0.50 [+0.37, +0.62] |
  | 27B | 66/69 = 0.96 [0.91, 1.00] | 11/32 = 0.34 [0.18, 0.52] | 8/38 = 0.21 [0.09, 0.35] | 1/61 = 0.02 [0.00, 0.06] | +0.40 [+0.29, +0.52] | +0.54 [+0.43, +0.64] |
  | Muse | 55/68 = 0.81 [0.72, 0.90] | 5/24 = 0.21 [0.06, 0.40] | 10/39 = 0.26 [0.10, 0.39] | 0/69 = 0.00 [0.00, 0.00] | +0.43 [+0.30, +0.52] | +0.38 [+0.30, +0.49] |
  | Lightning | 58/59 = 0.98 [0.94, 1.00] | 15/26 = 0.58 [0.38, 0.77] | 13/36 = 0.36 [0.22, 0.50] | 4/79 = 0.05 [0.01, 0.10] | +0.36 [+0.24, +0.49] | +0.57 [+0.45, +0.68] |
  | 122B | 51/53 = 0.96 [0.90, 1.00] | 25/32 = 0.78 [0.63, 0.94] | 12/33 = 0.36 [0.20, 0.57] | 1/82 = 0.01 [0.00, 0.04] | +0.27 [+0.16, +0.38] | +0.68 [+0.56, +0.80] |

  Both orders matter: the lookup switches mostly when both locker sentences came before the pick (0.81-0.98), rarely when both came after (0.00-0.06), and in between when they differ (0.21-0.78); the original order's contrast is the larger on four models.
- **Effect on claims.** Keep claim 10; the 2x2 is a caveat table (draft, not applied to the README or deck): claim 10's "locker-first" and "otherwise" groups mix the two changed-order cells (original before: 0.21-0.78 when the changed order is after, 0.81-0.98 when before).
- **Status.** Observation.
