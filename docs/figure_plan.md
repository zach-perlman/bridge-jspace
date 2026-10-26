# Figure plan for README v4 (Dan, 26 Oct ~16:45)

One figure, one claim, in story order. The title is the claim. The subtitle, one line on the figure, says how to read it. The caption in the README is one short line saying what to look at. All numbers come from `scripts/readme_story_figures.py`, which reads the run files and writes every plotted number to `figures/story/data.csv` (figure rows) next to the README's keys (rows `numbers`). No number is typed by hand.

New file names (`figures/story/figNN_*.png`) leave the 26 Oct files (`fig0_setup.png` … `fig11_order.png`) in place, untouched until Friday. Supplementary figures go to `figures/supp/` and are linked from Appendix A.

## Shared visual language (Step 2)

- **Colours.** Lookup purple `#6a4bd6`. Recall dark grey `#3a3a3a`. Identity blue, position orange, value green, unchanged light grey (`#c8c8c8`). Random controls: light grey markers or thin bars.
- **Status, one encoding everywhere.** Filled = fixed in advance; open = after the data; `°` after the label = rerun with a gate lowered after the data. There are no dashed status lines and no hatching.
- **Words.**
  - Lockers are called first / second / third.
  - The write's strength is the dose, × the size of a real change.
  - "A random part of the same size" replaces C2, keep-only, J++ size and †.
- **Models.** Qwen3.5-9B, Qwen3.6-27B, Qwen3.5-122B, Muse Glimmer 30B, in that order, everywhere.
- **Sizes.** 880 px wide (8.8 in at 100 px/in). Fonts ≥ 11 pt. The same x range for the same quantity: extra loss −0.2 to 1, shares 0 to 1.
- **Numbers on the plot** only where they carry the claim.

## Figures

| # | Claim = title | What to look at = caption | Encodings | data.csv | To supplementary |
|---|---|---|---|---|---|
| 0 | One prompt, two questions about the same bridge word | The change comes from a second prompt (Iris picked the tick) and is added at the bridge word. | Sentence boxes; the bridge in red. A second line shows the changed prompt and an arrow to where its difference is added. Lookup purple, recall grey. | none (schematic) | – |
| 1 | Recall needs the lens-readable part; the lookup mostly does not | Per row, the gap between the purple and grey dots. | Subtitle: "Extra loss: 0 = the reader does not need the J++ part, 1 = every switch needs it. Grey band: not needed (below 0.1)." 4 rows: main test (fixed in advance); the same on the logit difference; varied scenes; natural passages. The gap label sits at the right end of each row. Muse's natural row shows the recall only, with "lookup: too few switches". The 9B's natural row is open + °. | `fig01` rows; `lk_excess_<m>`, `rc_excess_<m>`, `contrast_<m>`, `ld_lk_<m>`, `ld_rc_<m>`, `ld_gap_<m>`, X0b verdict cells, `x0b_c_<m>`, `nat_*_<m>`, `natg75_*_9b` | rows "only the asked person's pick changes" and "matched" → `supp/s01_split_more_scenes.png` |
| 2 | No other part of the same size costs the recall as much as J++ | J++ is the only row where the recall dot sits far right. | 2×2 panels, one per model, each with its own row labels carrying the share: "J++ (19% of the change)". 4 rows: J++; the layer's main directions at J++'s size; logit-lens directions; random directions. Recall open dot with CI, lookup small purple dot. Subtitle names the scene sets: the first two rows use one-change scenes, the last two the main test. | `fig02` rows; `pcaeq_*` keys | J++ without the word's directions, the word alone, J++ fitted to another scene, input embeddings → `supp/s02_parts_all.png` |
| 3 | Lookups follow the change mostly when the locker sentence comes first | The bars before vs after the pick, per model. | Purple bars with Wilson CIs, "k of n" labels; grey dots for the recall; x axis "locker before / after the pick". | `fig03` rows; `lk_order_<o>_<m>_k` / `_n` | – |
| 4 | Each route predicts a different locker | Follow the three arrows: identity, position and the new value point at different lockers. | Original and changed prompt as locker boxes labelled first / second / third locker. The moved sentence is highlighted in the changed prompt. Arrows in route colours run from each route to the locker it predicts (value: the changed prompt's new number). | none (schematic) | – |
| 5 | The lookup follows identity or position, never the value | Orange shrinks without the pointer and appears with the pointer alone. Only J++ gives nothing. | Stacked bars, 4 rows per model: whole change; without the pointer directions; only the pointer directions; only the J++ part. Under each part's bar, a thin grey bar shows the position share with a random part of the same size. Percent labels only for identity and position ≥ 10. The 122B title carries °. | `fig05` rows; `rt_*`, `rtg_*`, `rtk_*` keys | without J++ and its random part → `supp/s05_routes_all_arms.png` |
| 6 | Position answers appear with depth, once the lookup stops needing J++ | Orange points rise where the purple line falls below the band. | Subtitle: "Candidate, after the data. Purple shading: layers where the lookup still needs J++ (extra loss ≥ 0.3)." x axis = layer number, no floating ticks. Top: J++ extra loss, points with CIs, no connecting line. Bottom: position share. | `fig06` rows | – |
| 7 | One fixed vector written at the bridge sends the lookup to its locker | Left: the target share rises past dose 1. Right: what a changed recall names. | Left, one panel per model: x = dose (× a real change's size, per pair s / s\*), vertical line at 1. y = share of lookups to the written locker. Thin lines per locker pair, a thick line for their mean, grey for the random direction. Right: one 100% bar per model for the recall changed under the strongest write: target item / third item / other. | `fig07` rows; `x8_t*`, `x8_rand*`, `x8_sreal_*`, `x8_rc_target_<m>` | the per-pair line styles (solid / dashed) are dropped. The second-vs-third pair is shown in Fig. 8. |
| 8 | Our pointer directions separate the first-mentioned item from the rest | (a) The loss is large only when the bridge's locker sentence opens the prompt. (c) No variant reaches the 0.5 line. | (a) Lookup's extra loss without the pointer, by group (see the question below). (b) Only the pointer part: position share for moves to or from the first locker vs moves between the second and third (grey: whole change). (c) Neutral-sentence test: the code's shift in positions, B1 and B2 per model, dashed line at 0.5 = "shifted"; the 122B and Muse filled in as they land. (d) The label-free pointer's overlap with ours (mean cos²) per model. | `fig08` rows; `fs_*`, `pm_*`, `x8_order_*`, P_cf reports | – |
| 9 | The split carries over to other texts; our pointer does not | Black stays near 0 in every row; orange shrinks outside simple scenes. | Subtitle: "Black: the lookup without J++ (the split). Orange: the lookup without our pointer directions, fit on simple scenes and not refit." The 9B natural cell reads "not tested (gate)". | `fig09` rows; `tptr_*` | – |
| 10 | About half of the lookups still switch with J++ and the pointer removed | Each purple dot against its grey random dot. | One panel. x = models; per model two removals, J++ + pointer and J++ + pointer + identity outside J++, each with its share of the change in the label. Each has a grey dot beside it for a random part of the same size. y = lookups still switching in the sanity swap. The 122B shows "not in this test" for the identity removal. | `fig10` rows; `rtc_left_*`, `rtd_left_*`, `rtd_randleft_*`, `rtd_share_*` | the dotted bars fixed in advance (Q34, Q36, Q40) and the "switches lost" panel → `supp/s10_removed_together_bars.png` |
| 11 | What held where | One row per claim, in story order. | 11 rows: the split; the split on the logit difference; varied scenes; natural passages; never the value; the pointer is needed; the pointer alone gives position; a write moves the lookup; the recall follows the write; the first-mentioned item, not the position in the text; transfer. Each cell has a symbol (✓ held, ~ partial, ✗ no, – not tested) and a small "a" for after the data. | `fig11` rows | – |

## Open question for Dan (Fig. 8 a, and the wording "first-mentioned item")

The three groups in the current Fig. 9a are defined by the bridge's locker sentence:
- (a) it opens the prompt;
- (b) it is the first locker sentence, but a pick sentence comes before it;
- (c) another item's locker sentence comes first.

They do not map onto "bridge named first / another item named first / neither". In (b), the pick sentence that opens the prompt names the bridge (or the changed bridge) in 123 of 201 one-change scenes (9B).

Regrouped by which item the first sentence names, the lookup's extra loss without the pointer (CPU, after the data, descriptive; scratchpad `fs_named_split.py`):

| First sentence | 9B | 27B | 122B | Muse |
|---|---|---|---|---|
| bridge named first, its locker sentence | 0.66 (n 41) | 0.24 (37) | 0.52 (25) | 0.51 (39) |
| bridge named first, in a pick sentence | 0.24 (17) | 0.07 (14) | 0.18 (17) | 0.21 (14) |
| another item named first | 0.11 / 0.60 (9 / 5) | 0.00 (19) | 0.12 / 0.00 (8 / 4) | 0.00 (14) |

So the loss is largest when the bridge's locker sentence opens the prompt. Being named first in a pick sentence counts for much less. Default for Fig. 8a: these three regrouped rows, with the labels above. The claim stays "first-mentioned item" (B shows order, not text position), with the caveat that the first mention counts most as a locker sentence.

## Interpretation notes

- "Figures are regenerated from data.csv only": read here as one script that computes every plotted number from the run files and records it in data.csv as it draws. Recounts from the per-item files are in the verify pack.
- Fig. 2 mixes scene sets, as now. J++ and the main directions come from the parts runs (only the asked pick changes); logit lens and random come from the main test (two people swap picks). The subtitle says so; the † goes.
