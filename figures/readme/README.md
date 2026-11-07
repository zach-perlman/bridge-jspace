# Figures for the root README

Built by `make readme` with [styles-plot](https://github.com/danorel/styles-plot) (vocabulary: [plotstyle.toml](../../plotstyle.toml); statuses: [data/figures/status.csv](../../data/figures/status.csv)). File names follow the document's order (figkit/layout.py); `_meta/` holds each figure's sidecar, `_sheets/` the contact sheets.

| № | figure | what it shows | status |
|---|---|---|---|
| 01 | <a href="01_tools.png"><img src="01_tools.png" width="260" alt="01_tools"></a> | Three tools, one target: the lens part at the bridge. | UNVERIFIED |
| 02 | <a href="02_main_split.png"><img src="02_main_split.png" width="260" alt="02_main_split"></a> | Taking the lens part out breaks recalled answers, not lookup ones | 3 of 10 cells post hoc · UNVERIFIED |
| 02b | <a href="02b_main_split_gaps.png"><img src="02b_main_split_gaps.png" width="260" alt="02b_main_split_gaps"></a> | The gap is far above the largest same-size control on every model in the band test, and above zero on every model at one layer | 3 of 10 cells post hoc · UNVERIFIED |
| 03 | <a href="03_controls.png"><img src="03_controls.png" width="260" alt="03_controls"></a> | Random, rotated, logit-lens and PCA directions cost far less than the lens part | 2 of 5 cells post hoc · UNVERIFIED |
| 03b | <a href="03b_controls_layer.png"><img src="03b_controls_layer.png" width="260" alt="03b_controls_layer"></a> | At one layer the lens part blocks more of the recall's switches than any same-size control on four models | UNVERIFIED |
| 04 | <a href="04_pointer.png"><img src="04_pointer.png" width="260" alt="04_pointer"></a> | Another entity's lens part moves the recall from any context, a probe's subspace that reads the fact does not | UNVERIFIED |
| 05 | <a href="05_atoms.png"><img src="05_atoms.png" width="260" alt="05_atoms"></a> | The lens part's 25 directions are the two bridge words, almost never the answer word | 1 of 5 cells post hoc · UNVERIFIED |
| 06 | <a href="06_address_read_remove.png"><img src="06_address_read_remove.png" width="260" alt="06_address_read_remove"></a> | A probe reads the address, and removing the lens part leaves it | 3 of 10 cells post hoc · UNVERIFIED |
| 07 | <a href="07_address_swap_lens.png"><img src="07_address_swap_lens.png" width="260" alt="07_address_swap_lens"></a> | A swap of the address moves the lookup; the lens misses it | 4 of 10 cells post hoc · UNVERIFIED |
| 08 | <a href="08_routes.png"><img src="08_routes.png" width="260" alt="08_routes"></a> | The patch moves the lookup by identity or by position, never by the value | 2 of 5 cells post hoc · UNVERIFIED |
| 09 | <a href="09_sentence_order.png"><img src="09_sentence_order.png" width="260" alt="09_sentence_order"></a> | The bridge word redirects the lookup when the locker sentence came first; both orders matter (post hoc) | 11 of 15 cells post hoc · UNVERIFIED |
| 10 | <a href="10_two_codes.png"><img src="10_two_codes.png" width="260" alt="10_two_codes"></a> | Without the address the position route goes; without the lens part the identity route turns to position (post hoc) | all post hoc · UNVERIFIED |
| 11 | <a href="11_monitor.png"><img src="11_monitor.png" width="260" alt="11_monitor"></a> | At the last token the lens part reads the address worse than a random part of the same energy | 1 of 5 cells post hoc · UNVERIFIED |
| 12 | <a href="12_last_token.png"><img src="12_last_token.png" width="260" alt="12_last_token"></a> | At the last token the lens reads the entity, and the answer does not go through it | 1 of 5 cells post hoc · UNVERIFIED |
| 13 | <a href="13_nine_models.png"><img src="13_nine_models.png" width="260" alt="13_nine_models"></a> | Across nine models the lens part is carried, needed, or both: graded | 4 of 18 cells post hoc · UNVERIFIED |
| 14 | <a href="14_directions.png"><img src="14_directions.png" width="260" alt="14_directions"></a> | With more lens directions removed, the 27B's lookup has more switches blocked | UNVERIFIED |
| 15 | <a href="15_facts.png"><img src="15_facts.png" width="260" alt="15_facts"></a> | On passages whose fact the model knows, the lookup follows the lens part; with made-up facts, less so | 1 of 4 cells post hoc · UNVERIFIED |
| 16 | <a href="16_order.png"><img src="16_order.png" width="260" alt="16_order"></a> | With the question before the scene, the 27B's lookup leans a little more on the lens part; the other models missed the gate | 3 of 7 cells post hoc · UNVERIFIED |
| 17 | <a href="17_where.png"><img src="17_where.png" width="260" alt="17_where"></a> | Middle layers need the bridge's mention; deeper layers, the question | UNVERIFIED |
