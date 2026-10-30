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
  Same check on the 9B and the 27B (30 Oct, post hoc, same driver, same two gates, same decision rules, same manifest text with no change, so the
  manifest's "what" line still says "Muse only"; weights downloaded to the pod; `runs/answer_arms_translated/qwen3.5-9b/run_qwen3.5-9b`,
  `runs/answer_arms_translated/qwen3.6-27b/run_qwen3.6-27b`; the saved runs `qwen35_9b_x51_12_e1_r2` and `x51_12_e1_27b_r2`, both with `code.dirty = true`, sha 15938ce4).
  9B: second gate passed (3199 of 3200 rows equal; one random-twin count differs by 1; P2-L0-0269 PP no_jpp_rand: saved 0, now 1, margin now 0.0, saved (inferred) 0.125; numerical noise, confirmed). Directions per item 14.9 English, 98.49 all languages. Recall: arm 3 extra +0.005 [+0.000, +0.018] all languages (+0.000 [+0.000, +0.000] English only), so (a) does not hold; arm 2 blocks 0.503 [0.416, 0.585] English only and 0.289 [0.212, 0.371] all languages, so (b) holds. By the pre-set rule the claim changes on the 9B: the recall's arm label the lens effect is the entity -> mixed; the lookup's can't tell (arm 1 has no extra loss beyond random) -> can't tell (arm 1 has no extra loss beyond random).
  27B: second gate passed (3199 of 3200 rows equal; one random-twin count differs by 1; P2-L0-0188 PM no_jpp_rand: saved 1, now 0, margin now 0.375, saved (inferred) 0.0; numerical noise, confirmed). Directions per item 14.86 English, 97.08 all languages. Recall: arm 3 extra +0.040 [+0.006, +0.082] all languages (+0.027 [+0.006, +0.054] English only), so (a) holds; arm 2 blocks 0.707 [0.596, 0.799] English only and 0.467 [0.356, 0.556] all languages, so (b) holds. By the pre-set rule the claim changes on the 27B: the recall's arm label the lens effect is the entity -> mixed; the lookup's the lens effect is the entity -> mixed.
  Limitation: Lightning and the 122B were not run (their weights were not downloaded; timebox). Muse, 9B and 27B all move to mixed on the recall; the README carries Muse only, the 9B and 27B results are here and not yet in the README or deck.

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
