# Figures for the depth ledger (docs/depth/EXPERIMENTS.md)

Built by `make readme` with [styles-plot](https://github.com/danorel/styles-plot) (vocabulary: [plotstyle.toml](../../../plotstyle.toml); statuses: [data/figures/status.csv](../../../data/figures/status.csv)). File names follow the document's order (figkit/layout.py); `_meta/` holds each figure's sidecar, `_sheets/` the contact sheets.

| № | figure | what it shows | status |
|---|---|---|---|
| 01 | <a href="01_item_not_answer.png"><img src="01_item_not_answer.png" width="260" alt="01_item_not_answer"></a> | The recall's drop without the lens part is the item, not its answer | 2 of 5 cells post hoc · UNVERIFIED |
| 02 | <a href="02_lightning_layers.png"><img src="02_lightning_layers.png" width="260" alt="02_lightning_layers"></a> | Lightning's layer sweep and the conflict test by layer | all post hoc · UNVERIFIED |
| 03 | <a href="03_ladder.png"><img src="03_ladder.png" width="260" alt="03_ladder"></a> | The recall needs the lens part once its other copies go; the lookup never | 2 of 5 cells post hoc · UNVERIFIED |
| 04 | <a href="04_follows_both.png"><img src="04_follows_both.png" width="260" alt="04_follows_both"></a> | Every recall follows both; on the 27B and Muse it mostly stays put | 1 of 4 cells post hoc · UNVERIFIED |
| 05 | <a href="05_number_answer.png"><img src="05_number_answer.png" width="260" alt="05_number_answer"></a> | With a number answer the recall follows the entity | 2 of 5 cells post hoc · UNVERIFIED |
| 06 | <a href="06_answer_map.png"><img src="06_answer_map.png" width="260" alt="06_answer_map"></a> | 0.651<!-- src: results/x52_atoms/report-20261030T094628Z/verdict.md \| 122B e1 (recall's view :: 0.688 [0.651 --> |

- **Read.**
  - On the main test the two bridge words carry about a fifth (9B, 27B, Lightning) to two fifths (Muse) of the rebuilt energy, the answer words almost none (none at all on Lightning).

<details><summary>The result in full, more reading and caveats</summary>

- **Caveats.**
  - The classifier was hand-checked on 5 items per model (blind on Muse's main test only) and misses non-English answer words.
  - On the fact passages the bridge names carry 0.02-0.03 and the descriptions' words dominate (see the report).

</details>

### Where is the answer readable through the lens, and can it be written there? <a id="b52-b"></a>

`ledger only` *Used in: not in the README (its rebuild).*

Test batch 52 B · opened 29 Oct · status: rule fixed in advance · hand-check: not in sample · files: `results/x52_answer_map/x52_write2x-20261029T074907Z/write2x.md` · recompute: `scripts/x52_answer_map.py` (the command in its docstring) · also: Lightning's main set 29 Oct

<details><summary>Question, data, method, rule and figure</summary>

- **Question.** For each reader, on our scenes and on the fact passages, is the answer word readable through the lens before the answer is computed, and does writing its lens directions change the answer?
- **Why we asked.** The answer control found the answer word not read at our bridge word but read at the fact passages' description; where else is it readable, and is it used there?
- **Data.** Our main test, 200 per model (Lightning at L14, a coverage run, no prediction); the fact passages, 158 / 166 / 157 (Lightning's read pending).
- **Method.** Read: the answer word's rank in the lens readout at the bridge word, its earlier mention, the question and the last token, every second layer before the answer layer. Write: at the most readable cell, the answer word's lens directions at one and two times a real change's size, against a random part and a frequency-matched part of the same size; the whole change at that cell as the reference.

- **Rule, fixed in advance.** "“Readable”: the answer word in the lens top-5 on ≥ 0.5 of items at some layer before the answer layer. “Usable”: writing its directions changes the answer on ≥ 0.3 of items with the random control ≤ 0.10. Report the four combinations per reader, per dataset." No prediction.

Readable and usable, per reader and data set:

![On the fact passages the answer is readable and usable; on ours rarely | 2 of 5 cells post hoc · UNVERIFIED |
| 07 | <a href="07_value_formats.png"><img src="07_value_formats.png" width="260" alt="07_value_formats"></a> | In prose, JSON and tables the lookup never takes the value | 1 of 4 cells post hoc · UNVERIFIED |
| 08 | <a href="08_identity_code.png"><img src="08_identity_code.png" width="260" alt="08_identity_code"></a> | Centered, the code moves lookups beyond random; raw, little or none | UNVERIFIED |
| 09 | <a href="09_subset27b.png"><img src="09_subset27b.png" width="260" alt="09_subset27b"></a> | On its position scenes the 27B's address brings fewer answers back | UNVERIFIED |
| 10 | <a href="10_report_first_position.png"><img src="10_report_first_position.png" width="260" alt="10_report_first_position"></a> | Reworded, the report reads slot 1 on every model tested | 1 of 3 cells post hoc · UNVERIFIED |
| 11 | <a href="11_last_token_swap.png"><img src="11_last_token_swap.png" width="260" alt="11_last_token_swap"></a> | The bridge word's code works at the last token only on Muse | 1 of 4 cells post hoc · UNVERIFIED |
| 12 | <a href="12_last_conflict.png"><img src="12_last_conflict.png" width="260" alt="12_last_conflict"></a> | At the read peak no lookup goes through the lens part | 2 of 5 cells post hoc · UNVERIFIED |
| 13 | <a href="13_last_conflict_words.png"><img src="13_last_conflict_words.png" width="260" alt="13_last_conflict_words"></a> | Near the output the test is uninformative; read peaks differ | 1 of 4 cells post hoc · UNVERIFIED |
| 14 | <a href="14_attention_blocks.png"><img src="14_attention_blocks.png" width="260" alt="14_attention_blocks"></a> | Two attention blocks carry a third of Lightning's lookup switch | all post hoc · UNVERIFIED |
| 15 | <a href="15_fact_answer_control.png"><img src="15_fact_answer_control.png" width="260" alt="15_fact_answer_control"></a> | Named: both recalls mixed; described: the 27B's reads as the answer | UNVERIFIED |
| 16 | <a href="16_every_layer.png"><img src="16_every_layer.png" width="260" alt="16_every_layer"></a> | Over every layer up to L, fact-after lookups follow the lens part | 1 of 3 cells post hoc · UNVERIFIED |
| 17 | <a href="17_fact_routes.png"><img src="17_fact_routes.png" width="260" alt="17_fact_routes"></a> | On the fact passages the lookup rarely takes the position route | 3 of 5 cells post hoc · UNVERIFIED |
| 18 | <a href="18_read_window.png"><img src="18_read_window.png" width="260" alt="18_read_window"></a> | On the 9B the fact passages are read over our layers; on the 27B not | 1 of 3 cells post hoc · UNVERIFIED |
| 19 | <a href="19_person_probe.png"><img src="19_person_probe.png" width="260" alt="19_person_probe"></a> | No probe reads who picked an item at its locker sentence | 2 of 4 cells post hoc · UNVERIFIED |
| 20 | <a href="20_any_item.png"><img src="20_any_item.png" width="260" alt="20_any_item"></a> | The animal-fit address does not carry over to other items as ruled | 1 of 4 cells post hoc · UNVERIFIED |
| 21 | <a href="21_described_gap.png"><img src="21_described_gap.png" width="260" alt="21_described_gap"></a> | The breadth track's removal everywhere hits the recall more; the depth track's gap is unclear | 2 of 5 cells post hoc · UNVERIFIED |
