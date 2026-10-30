# Hand-check findings

A log of issues found during the manual hand-check (Dan's reading of the review tool's items), each with the check that followed it.
One entry per finding. A new finding is appended here, in this format, in the same commit as its check. Nothing here is a verified
result: see VERIFIED.md. Status: **closed** (checked, nothing to change or the change is made), **limitation** (a stated limit
remains), **not done** (a check is still open).

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
- **Effect on claims.** f5 unchanged. The 51.12 verdicts are unchanged. One caveat line added to the answer-control section of the depth
  README ("The answer control used English answer words only ...").
- **Status.** Limitation. The label check is closed. The arms with translated answer directions (arms 2 and 3 rebuilt with the answer
  directions in every language, with the size-matched random parts rebuilt): done, post hoc, Muse only; the pre-set rule says the claim
  changes (see below); README and deck not yet edited.
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
