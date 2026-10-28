# Figure vocabulary

One vocabulary across every figure the README or docs/x0_details.md shows (Dan, 26 Oct ~21:50 and ~22:45): Figs. 0-11, 1b and 3b (8b until batch 45, now Fig. 8 (a)), the supplementary figures (s01, s01b, s02, s05, s08, s10), x0_figures' overview, details, kmatch, kcurve, share and asked_first, and the digit check (f6). Scope: every figure label, legend, subtitle, caption and README caption (figure alt texts, "*Fig. N.*" lines, table headers) uses only the canonical strings; prose keeps the exceptions named in the table. `tests/test_readme_build.py` fails on a banned variant in any of these figures' drawn text and in the captions (`docs/drafts/readme_v5_captions.md` until Tuesday's merge, then README.md).

| Concept | Canonical label | Banned variants |
|---|---|---|
| the 25 lens directions | "J++ part" | "J++" alone as a part name, "lens's part", "lens-readable part" (prose may keep "the part the lens can read" once, in In one minute) |
| our 4 position directions | "pointer"; refit ones "refit pointer"; label-free ones "label-free pointer" | "our pointer", "pointer directions", "pointer part", Alf, U |
| identity outside J++ | "identity outside J++" | "idout", "identity direction" (except in its definition) |
| the matched control | "random part (same size)"; for writes "random direction (same size)" | "random part, same size", "random directions", "random part of its size", "J++ size" |
| random lens directions (a dictionary, Fig. 2 only) | "random lens directions": random directions picked by the same OMP at their own (smaller) share, not the matched control (Dan ~22:40); also where s02 and the x0 details show that dictionary (Dan 27 Oct ~11:45; was "random atoms") | "random directions", "random atoms" |
| PCA control | "PCA directions (same size)" | "main directions", "the layer's main directions" |
| removing / keeping | "without the X", "only the X", "whole change" | "part removed", "no J++", "keep-only", "X alone", "edit" |
| answer classes | "identity", "position", "value", "original answer", "other"; on the main-page figures "identity" only as "identity route", "identity answers" or "identity change" (Dan, 28 Oct ~20:30; `scripts/check_figure_terms.py`) | "unchanged", "original" (alone); a bare "identity" on a main-page figure |
| prompts | "original prompt", "changed prompt" | "swapped", "Changed" as a row title without "prompt", O / S in figures |
| lockers | "first / second / third locker" | slot numbers, "slot" |
| sentence order | "locker before the pick", "locker after the pick" | "locker first/after" (prose may use "locker-first scenes" after defining it once) |
| scene sets | "main test (two people swap picks)", "one-pick scenes (only the asked pick changes)", "routes test", "sanity swap", "same item moved", "another item moved", "varied scenes: prose / JSON / table", "natural passages" | C0 / C1 / C2, "json", "simple" alone, "Same test", "one-change scenes" |
| neutral-sentence test | "a sentence before the first locker", "a sentence between the lockers and the picks" | B1 / B2 |
| metrics | "extra loss" (0-1, defined in the subtitle wherever it appears); "gap"; "code shift (positions)", written β only after "code shift"; "dose (× a real change)" | "J++ extra loss", "Jdep", "s", "s*", "beta" alone |
| shares | answer and switch shares in %, 0-100: "lookups switched (%)", "lookup answers (%)", "lookups still switching (%)" | the same quantities on 0-1 axes, "position share" |
| cell states | "not tested (gate)"; "not run"; "too few switches (k of n)" | "not in this test", "queued", "queued (if time)", "not measurable" |
| status | filled "fixed in advance"; open "after the data"; "° gate lowered to 0.75 after the data". Legend only if a figure has both statuses; otherwise one phrase in the subtitle | "fixed in advance (main test)", "° gate lowered after the data" |

Added for the x0 details figures (26 Oct ~23:00, the same words; Dan to confirm):

| Concept | Canonical label | Banned variants |
|---|---|---|
| the other dictionaries | "logit-lens directions" (W_U), "input-embedding directions" (W_E), "random lens directions"; the J++ dictionary at k directions: "J++ part"; the lens itself: "the J++ lens" | "W_U", "W_E" |
| X0's metrics | "extra loss"; "switches lost" (1 − switched without the part / switched with the whole change, in %); "gap" | "excess", "dependence", "J-dependence", "graded contrast", "C = ..." |
| run codes | none on a figure (a run's name as provenance stays) | "X0" |

Added for the batch-45 figures (27 Oct ~00:30, the README v5 figures; Dan to confirm):

| Concept | Canonical label | Banned variants |
|---|---|---|
| 45m's scenes | "clean one-pick scenes" (the asked pick changes to an added locker item nobody picks; no duplicate pick) | "45m" on a figure |
| 45e's control | "wrong pair": mean differences of other item pairs (same domain), at the share of identity outside J++ | "wrong-pair control" as a row label |
| 45b's arms (Fig. 3b) | "the bridge-word change"; "copy at the locker sentences: every token" / "the item's tokens only"; "copy at the number or period only" (the changed prompt's states put into the original prompt) | "S patched into O", arm letters (a, c, d) |
| cell states | "not counted (k switches)": a cell under X0's 30-switch bar that the rule fixed in advance does not count (Fig. 9's 45d panel); "pending" (Fig. 11: ○, a run still queued) | – |

Added for the figures after the overnight queue (27 Oct ~01:05; Dan to confirm):

| Concept | Canonical label | Banned variants |
|---|---|---|
| the J++ part's size | "25 / 50 / 100 directions" (Fig. 2b, 45k; Dan 27 Oct ~11:20) | "atoms" for it, "k = 100" on a figure |
| atom | not used: a synonym of "direction" (the lens's atoms are its directions); Fig. 2's dictionary is "random lens directions" (row above) | "atom(s)" for the J++ part's directions |
| 45q's arms (Fig. 3b once 45q is in) | "copy at the item's own tokens", "copy at the other locker-sentence tokens", "copy at the number or the period only"; "copy at L without the J++ part" / "without a random part (same size)"; the rule's arms "at L: the bridge-word change" / "at L: copy at every locker-sentence token"; "L" and "L/2" for the layer fixed in advance and half of it | arm codes (li, lr, lv, lf, c_nojpp) |
| 45p's arms (Fig. 3c or its supplement) | "(1) without the J++ part at the bridge word", "(2) (1), and without it at the earlier mention", "(3) (1), and without a random part (same size) there", "(4) (1), and without it at another item's mention" | a1-a4 |
| cell states | "not tested" (Fig. 10's 122B wrong pair; Fig. 11's "–": not run or not counted) | – |
| retired on figures and captions | – | "first-mentioned", "part removed", "ablation", "Q45", run ids (scripts/check_figure_terms.py) |

Typography: arrows are drawn as "→" and "↔" (Dan's "->" and "<->"), the dose as "×". A canonical string may wrap over lines on a figure; it is still the same string.
