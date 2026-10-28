# Figure plan

## v6 style rules (Dan's README v6 brief, §5; 28 Oct)

Every README figure, as it is restyled for v6 (one experiment card E1–E16, one figure each):

- **Title** = the conclusion, one line, no numbers (no digit at all, so no model sizes either).
- **Subtitle** = the mechanics, one line.
- **n and status** as a small label in the top-right of each panel: "n 300 per model · ● fixed in advance" (filled glyph = fixed in advance, open ○ = after the data; "schematic" on a schematic). `story_style.panel_tag`.
- **Fixed colours**, never a hue reused for another meaning: lookup purple, recall dark grey, random / control light grey, identity blue, position orange, value green (shown even when 0, with a "0" label), the J++ part one hue and the address another. The original answer is an empty (outlined) segment, so light grey stays the control's alone (`story_style.EMPTY`).
- **Models** in the order 9B, 27B, Muse; the 122B only in supplements.
- **Axes**: shares on [0, 1]; layers as a fraction of depth when models share a panel, as the layer index when there is one model per panel.
- **95% intervals** always drawn (whiskers on bars, bands on lines).
- **Not interpretable** (the whole change switches < 0.30 of a reader): the same hatched shading in every figure (`story_style.NI_SWITCH`, `NI_SHADE`, `not_interpretable`).
- **At most two panels** per figure.
- **Words**: lookup, recall, bridge, swap (not write), address (not pointer), in all figure text.

`scripts/check_figure_terms.py` tests the testable part on the figures in its `V6_FIGS` (a figure joins when it is restyled): no digit in the title, title and subtitle one line each, at most two panels, no "pointer" or "write". It also lists, without failing, the other README titles that still hold a digit.

**Iteration 2 (Dan, 28 Oct ~15:40).** The README's main figures are exactly `README_NAMES` (fig00_setup, fig01_split, fig01c_zeroing, fig05b_identity_outside, fig05_routes, fig07_writes, fig09b_six_lockers, fig07b_verbal, fig03_order, fig03d_depth_map, fig06b_anatomy, fig11_scorecard, fig05c_described_bridge, fig09_transfer); every other figure is still drawn, keeps its file, and sits on the second sheet (`SHEET_MORE`). All fourteen are in `V6_FIGS`, and the checker also fails on: "without it" / "only it" / "with it", "beside", "reading", "(band: 95%)", "random or layout control", "below random", "lookups sent to the target locker", a test number (45.x–49.x), a run name (x0_, x6_, x8_, x45, x47, x48), "C0" / "C2", and "Rule:" in a subtitle. Number words in titles are fine, digits are not. The words used on the figures: lookup · recall · the change · whole change · the J++ part · a random part (same size) · the address · identity / position / value · the swap · switched · answers kept · the original answer. Full model names in the first panel, "9B" / "27B" / "Muse" after it. Shares are on 0–1; "pp" only for differences. Each panel's corner shows "n = 758, 758, 657" and the status glyph, with no words. The value is a legend line ("value: 0.00 in every row"), never a box per row. A title or subtitle that is too wide shrinks to fit (`story_style.fit`). fig05c and fig09_transfer keep their panels (3 and 8).

**Figures brief (Dan, 28 Oct ~18:30), steps 1-2.** One mark system: colour = who or what (`story_style.MARK_COL`: recall dark, lookup purple, the J++ part teal, the address orange, identity blue, a random part grey), mark = the operation (`story_style.MARK`: removed from the change ●, taken out of a prompt's own state ✕, added by itself ◆, the swap ▲, the whole state ■), one panel per model in the order 9B, 27B, Muse; defined once in fig00b_marks. The checker adds: "cannot report" / "not run" / "not tested" never inside a frame of a main-page figure (`FRAME_RETIRED`), and only the mark system's hues on `MARK_FIGS`. Omitted cells and hollow marks are said in caption lines under the plot; hollow has one meaning per figure, said there. `README_NAMES` (at most fourteen): fig00_setup, fig00b_marks, fig12_two_by_two, fig09a_transfer, fig01_split, fig01d_ladder (E2, replacing fig01c_zeroing), fig05b, fig05, fig07, fig09b_six_lockers, fig07b_verbal (two panels, the identity change as the positive control; the 27B's report is E8's Result sentence), fig03_order (with B, Zach's passages), fig03d, fig06b_anatomy (with the 27B). On the second sheet: fig01c, fig05c and fig09b_refit (Part IV links), fig11 (the breadth page's; with the 2×2 and Z1 "degree" rows), fig13_attention and fig14_learned (Appendix links; over the cap), fig09_transfer (every model). Builders: `scripts/story_b50.py`, `scripts/story_b50b.py`.

**Fig. 5b / 5d brief (Dan, 28 Oct ~20:30).** E3's card shows `fig05d_routes_lens`: the routes test (47.1, fixed in advance), one panel per lens slice taken out (directions 1–25, 26–100, 1–100), two rows per model, the identity route's and the position route's answers lost beyond a random part of the same share (the verdict's routes falls), the random part's own cost as a grey band (recomputed from the routes runs' per-item rows, whose falls must equal the verdict's), the 0.10 band, the 27B's 1–100 identity bar labelled as redundant copies. `fig05b_identity_outside` keeps its main panel (the main test, five parts, both readers), drops the inset, and moves to the second sheet, linked from E1. The checker adds "identity" on a `V6_FIGS` figure only as "identity route", "identity answers" or "identity change".

**Fig. 4 / 5 brief (Dan, 28 Oct ~20:30).** One drawing of the routes test (`readme_story_figures.routes_drawing`): each predicted locker in its route's colour (identity and position on the original prompt's lockers, the value on the changed prompt's new number), the moved sentence outlined dark and dashed, the original answer empty, the two pick sentences; no "schematic" tag, no locker header row. In full on Fig. 5's left panel with the three routes defined in one line under the plot; small (boxes and colours only, no value colour) on Fig. 5d; Fig. 4 (`supp/s04_routes_design`) is the same drawing larger, off the main page and linked once from Appendix A. Fig. 5's right panel is unchanged.

| v6 card | Figure | Title | Status | Source (results/) |
|---|---|---|---|---|
| E3 | `fig05d_routes_lens` | The lookup's identity route runs outside the lens; the position route never touches it | fixed in advance (47.1's routes falls); the random part's own cost descriptive | x47_atoms/x47_1-*, x6_routes/*_x47_1 |
| E5 | `fig05_routes` | The lookup takes the identity route or the position route, never the value | left: the routes test drawn (`routes_drawing`; Fig. 4 is `supp/s04_routes_design`, the same drawing larger), the three routes defined under the plot; right: fixed in advance | x6_routes main runs (whole, without the address, its random part) |
| E12 | `fig06b_anatomy` | The address forms early; identity route first, position route later | fixed in advance (47.8) | x47_anatomy/x47_8-* |
| E1 | `fig01_split` | Recall follows the J++ part of the bridge; the lookup mostly does not | fixed in advance; the 122B in `supp/s01`, the other settings stay `fig01b_settings` (kept separate), the locker-before gap moved to `supp/s03_order_split` | x0_necessity main runs |
| E1 (link) | `fig05b_identity_outside` | Only the J++ part costs the recall; no single part costs the lookup | J++ part and PCA after the data (one-pick scenes); 26–100, logit-lens and random lens directions fixed in advance; Fig. 2 and Fig. 5b merged, the 122B in `supp/s02`; the inset moved to Fig. 5d (Dan ~20:30) | x0_parts, x0_necessity main runs, x47_atoms/x47_1-* |
| E6 | `fig07_writes` | The address carries the position route; swapping it moves the lookup | three panels: (A) probe after the data, (B) removal / address only fixed in advance, (C) swap fixed in advance; the recall's answers under the swap in `supp/s07_recall_follows_swap` | x0_probe v4, x6_routes (+ keeponly), x8_write |
| E10 | `fig03_order` | Locker after the pick: the link is made in the locker sentences | (A) order split after the data; (B) 45q sweep after the data, its rule's arms fixed in advance; old Fig. 3 (with the 122B and the extra-loss panel) in `supp/s03_order_split` | x0_necessity main runs; x45b_binding/x45q-* |
| E8 | `fig07b_verbal` | The lens is blind to the address | three panels (iteration 2): read-through (47.0 (a), the right ordinal word's rank) and share rebuilt (47.0 (b)), descriptive; the 27B's report (47.10, fixed in advance; the 9B and Muse fail the report gate); 47.0's KL and identity ranks in `supp/s07b_lens_readout` | x47_verbal/summary-*, x47_report/x47_10-* |
| E11 | `fig03d_depth_map` | Locker after the pick: the lookup leaves the bridge word early | fixed in advance (D1, D2); the 9B, both sentence orders, both readers as row pairs | x47_depthmap/depth-* |
| E15 | `fig15_mechanisms` | Every mechanism we proposed for the split failed its rule | fixed in advance; one row group per test (48.2 B, 48.3, 48.4, 48.5, 47.6 (b)) against its rule's bar | x48_enrich, x48_bind, x48_heads, x48_route2, x47_edges |
| E2 | `fig01c_zeroing` | Taking the J++ part out of the changed prompt's state leaves the recall's answers in place | fixed in advance (47.5); two panels, answers kept on 0–1, the bar at 0.8 "followed if above" | x47_zero/x47_5-* |
| Claims | `fig11_scorecard` | Ten claims on three models: what held, in part, or failed | iteration 2: claims 1, 2, 3, 4a, 4b, 5, 6, 7, 8, 9a, 10, 11 on 9B / 27B / Muse (`FIG11_IDS`); per cell, the claims table's reading (agent's, UNVERIFIED); `figures/story/claims_scorecard.csv` (v5's `scorecard.csv` stays: the joint figures and the shared grid read its claim names) | claims_scorecard.csv |

## README v5 (27 Oct, after the overnight queue; draft, UNVERIFIED)

Figure → claim (its title) → status → source. Built by `scripts/readme_story_figures.py` (`figures/story/`, `figures/supp/`, every plotted number in `figures/story/data.csv`; Fig. 11 from `figures/story/scorecard.csv`); `scripts/check_figure_terms.py` checks the retired terms. Status: fixed in advance (filled marks), after the data (open), ° gate lowered to 0.75 after the data.

| Figure | Claim (title) | Status | Source (results/) |
|---|---|---|---|
| 0 `fig00_setup` | One prompt, two questions about the same bridge word | schematic | – |
| 1 `fig01_split` | Recall needs the J++ part of the bridge; the lookup mostly does not | fixed in advance; the locker-before gap column after the data | x0_necessity main runs; x0_composition/split-by-order-* |
| 1b `fig01b_settings` | In every setting, recall needs the J++ part more than the lookup does | fixed in advance (clean one-pick scenes: 45m); the 9B's natural passages ° | x0_logit_diff, x0_necessity/x45m-*, x0b_generalize, x5_natural |
| 2 `fig02_specificity` | No other part of the same size costs the recall as much as the J++ part | J++ part and PCA after the data; the other two panels fixed in advance | x0_parts, x0_necessity main runs |
| 2b `fig02b_k_curve` | Why a bigger J++ part costs the 27B lookup: can't tell | (a) main test after the data; (b) 45k fixed in advance, Q45.9 (d) can't tell; Muse from run r4 (can't tell there too); 'directions' for the J++ part's size | x0_necessity/*kmatch* and main runs; x6_routes/*x45k*, x6_routes/x45k-* |
| 3 `fig03_order` | Lookups follow the change mostly when the locker sentence comes first | (a) after the data; (b) main test after the data, clean one-pick scenes fixed in advance | x0_necessity main runs; split-by-order-*; x45m-* |
| 3b `fig03b_layers` | On clean scenes with the locker after the pick, the locker sentences make the link | 45q's rule fixed in advance, holds 3 of 3; the layer sweep after the data: the copy makes the link by L on the Qwens, from about L/2 on Muse | x45b_binding/x45q-*, x45q-link-*, x45q-sweep-* |
| 3c `fig03c_earlier_mention` | The recall reads the item's earlier mention when its locker came first | 45p fixed in advance, holds 3 of 3; both readers filled, apart by colour | x45p/x45p-* |
| 4 `fig04_routes_design` | Each route predicts a different locker | schematic | – |
| 5 `fig05_routes` | The lookup follows identity or position, never the value | fixed in advance; the 122B ° | x6_routes |
| 6 `fig06_depth` | Position answers appear with depth, once the lookup stops needing the J++ part | candidate, after the data | x0_necessity, x6_routes sweeps |
| 7 `fig07_writes` | One fixed vector written at the bridge sends the lookup to its locker | writes fixed in advance; the recall's split after the data | x8_write |
| 8 `fig08_first_locker` | The pointer marks the first locker in a clean layout | after the data | x6_routes/x45a-descriptive-*, x8_write |
| 9 `fig09_transfer` | The split carries over to other texts; the pointer must be refit for each format | fixed in advance (the 9B's natural passages °); (b) 45d fixed in advance | x0b_generalize, x5_natural, x0b_generalize/*x45d* |
| 10 `fig10_what_is_left` | J++ part, pointer and identity outside J++ stop most 9B and 27B lookups, not Muse's | fixed in advance; the 122B ° (identity row; no wrong-pair control: not tested); the wrong pair on the scenes where it reached 0.9 of identity's share (size check, after the data) | x6_routes (bothoff, d1, *x45e_dom*, qwen35_122b_x6_routes_d1_g75), x6_routes/x45e-size-* |
| 11 `fig11_scorecard` | What held where | per cell ("a": after the data; "–": not tested); no 45b row (a design error, Dan 27 Oct ~11:20) | figures/story/scorecard.csv (its data.csv key column) |
| s01, s01b, s02, s05, s08, s10 | the supplements of Figs. 1, 1b, 2, 5, 8 and 10 (as before) | as their figures | as their figures |
| s01c `s01c_no_chat_template` | Without the chat template the split is still there (after the data) | after the data, ° (45i'; Q45.8 stays not tested at gate 0.80) | x0_necessity/*x45i_main_nochat*_g75, x6_routes/*x45i_nochat* |
| s03b `s03b_layers_45b` | Locker after the pick: what moves the lookup at each layer (the main test's items) | after the data (45b's sweep; a design error: its changed prompt differs after the bridge word) | x45b_binding/*sweep_v2* |
| s10b `s10b_what_is_left_all_scenes` | Fig. 10 with the wrong pair on every scene | as Fig. 10 (45e as scored) | as Fig. 10 |

## README v4 (Dan, 26 Oct ~16:45; kept for reference)

One figure, one claim, in story order. The title is the claim. The subtitle, one line on the figure, says how to read it. The caption in the README is one short line saying what to look at. All numbers come from `scripts/readme_story_figures.py`, which reads the run files and writes every plotted number to `figures/story/data.csv` (figure rows) next to the README's keys (rows `numbers`). No number is typed by hand.

New file names (`figures/story/figNN_*.png`); the 26 Oct files (`fig0_setup.png` … `fig11_order.png`) are in `figures/archive/` since 27 Oct. Supplementary figures go to `figures/supp/` and are linked from Appendix A.

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

**Changes after Dan's mock-ups (~17:15).**
- Fig. 1 is the main test alone, with rows = models and the gap with its interval at the right.
- New Fig. 1b, "In every setting, recall needs J++ more than the lookup does": one panel per setting, with rows = models.
  - The settings are the logit difference, only the asked person's pick changes, varied scenes and natural passages.
  - Muse's natural-passage lookup reads "too few (10 of 60)" and its gap "–".
  - The "matched" rows stay in `supp/s01`.
- Fig. 2 follows the same layout: one panel per part, with rows = models and the share of the change in each row label.

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
