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
  directions in every language, with the size-matched random parts rebuilt) are **not done**.

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
- **Status.** Closed.
