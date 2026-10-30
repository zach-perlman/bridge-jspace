# x52_atoms: what is inside the top-25 atoms of the lens part (batch 52 A; descriptive; no rule; UNVERIFIED)

Per item: Δ's 25 signed-OMP atoms over the J++ letter dictionary at L; each atom's class (automatic, scripts/x52_atoms.py classify); per item the class shares of the 25 atoms and of the rebuilt energy (the energy an atom adds when it enters, over the part's share of ||Δ||^2); means over items with 95 % cluster-bootstrap intervals over the bridge entity (10,000, seed 0). E1: one Δ serves both readers (identical prompts through the bridge word), so the two views differ only in which answer class is the reader's own. Z2: each reader its own Δ; both ask for the same answer, so 'answer_other' is empty. Chance: the class shares of 2,000 random letter tokens (seed 0) in the same items and views.

Classes: `bridge` the original bridge word; `new_bridge` the new bridge word; `scene_item` another item named in the scene; `person` a person's name in the scene; `answer_own` the reader's answer word; `answer_other` the other reader's answer word; `same_class` a same-class word not in the scene; `function` function words and punctuation; `other` other

Sources: qwen3.5-122b-a10b: {'e1': 'qwen35_122b_x52_atoms_fwd'}

## Share of the rebuilt energy

| model | set | reader view | n (entities) | bridge | new_bridge | scene_item | person | answer_own | answer_other | same_class | function | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 122B | e1 | lookup | 50 (27) | 0.152 [0.128, 0.176] | 0.153 [0.130, 0.179] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.003 [0.001, 0.006] | 0.004 [0.002, 0.007] | 0.688 [0.651, 0.724] |
| 122B | e1 | recall | 50 (27) | 0.152 [0.128, 0.176] | 0.153 [0.130, 0.179] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.003 [0.001, 0.006] | 0.004 [0.002, 0.007] | 0.688 [0.651, 0.724] |

## Share of the 25 atoms

| model | set | reader view | n (entities) | bridge | new_bridge | scene_item | person | answer_own | answer_other | same_class | function | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 122B | e1 | lookup | 50 (27) | 0.043 [0.037, 0.050] | 0.040 [0.035, 0.046] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.004 [0.001, 0.008] | 0.006 [0.002, 0.010] | 0.907 [0.897, 0.916] |
| 122B | e1 | recall | 50 (27) | 0.043 [0.037, 0.050] | 0.040 [0.035, 0.046] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.004 [0.001, 0.008] | 0.006 [0.002, 0.010] | 0.907 [0.897, 0.916] |
| 122B | e1 | chance | | 0.0003 | 0.0003 | 0.0000 | 0.0000 | 0.0002 | 0.0002 | 0.0009 | 0.0077 | 0.9904 |

## Items with at least one atom of the class

| model | set | reader view | n (entities) | bridge | new_bridge | scene_item | person | answer_own | answer_other | same_class | function | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 122B | e1 | lookup | 50 | 46 | 44 | 0 | 0 | 0 | 0 | 5 | 7 | 50 |
| 122B | e1 | recall | 50 | 46 | 44 | 0 | 0 | 0 | 0 | 5 | 7 | 50 |

## The two bridge classes by how they matched (pooled share of rebuilt energy; the share of their atoms whose sign points the expected way: original -, new +)

| model | set | view | class | match | atoms | energy | sign as expected |
|---|---|---|---|---|---|---|---|
| 122B | e1 | lookup | bridge | alias | 14 | 0.0420 | 1.00 |
| 122B | e1 | lookup | bridge | first token | 2 | 0.0078 | 1.00 |
| 122B | e1 | lookup | bridge | initial | 12 | 0.0162 | 0.92 |
| 122B | e1 | lookup | bridge | key | 24 | 0.0849 | 1.00 |
| 122B | e1 | lookup | bridge | part | 1 | 0.0006 | 1.00 |
| 122B | e1 | lookup | bridge | prefix | 1 | 0.0015 | 1.00 |
| 122B | e1 | lookup | new_bridge | alias | 13 | 0.0453 | 1.00 |
| 122B | e1 | lookup | new_bridge | first token | 1 | 0.0029 | 1.00 |
| 122B | e1 | lookup | new_bridge | initial | 6 | 0.0062 | 0.83 |
| 122B | e1 | lookup | new_bridge | key | 28 | 0.0963 | 1.00 |
| 122B | e1 | lookup | new_bridge | prefix | 2 | 0.0058 | 1.00 |

## 'other' by detail (pooled share of rebuilt energy)

- 122B e1 lookup: {'none': 0.6838}; median part share of ||Δ||^2 0.236

## Hand check (the lookup's view)

Blindness: the 9B / 27B labels (hand-20261028T235223Z) are NOT blind. While the bridge-spelling rules (prefix / initial / part, Chinese names) were being written, the labeller had seen the classifier's labels on the first atoms of 4 of the 5 27B items (P2-L0-0008, 0051, 0084, 0097) and 1 of the 5 9B items (P2-L0-0016), and the rules were shaped on such items; that folder's write_labels.py docstring ('without the classifier's output') is wrong on this point. Muse's labels (hand-20261028T235654Z) are blind: Muse's atoms were first seen on its sheet, after the classifier was committed (11ee8c6f), and the classifier was not changed afterwards. Z2 (hand-20261029T000000Z, the lookup's own passage; not asked for by the brief, added because Z2's answer words come in other languages and as prefixes): not blind (some of its items were among the Z2 examples already printed with the classifier's labels); the classifier was not changed after it.

- 9B e1: 121 / 125 atoms agree (0.968; Cohen's kappa 0.8548) over 5 items; hand classes {'bridge': 6, 'new_bridge': 7, 'other': 108, 'function': 4}; disagreements (hand -> classifier: tokens): {"function -> other": ["и", "ни", "مع", "ein"]}
- 27B e1: 119 / 125 atoms agree (0.952; Cohen's kappa 0.7339) over 5 items; hand classes {'new_bridge': 5, 'bridge': 4, 'other': 111, 'function': 4, 'answer_other': 1}; disagreements (hand -> classifier: tokens): {"function -> other": [" Ты", " və", " 에서", " των"], "other -> function": [">i"], "bridge -> other": ["EEEE"]}
- Muse e1: 117 / 125 atoms agree (0.936; Cohen's kappa 0.7553) over 5 items; hand classes {'new_bridge': 7, 'bridge': 8, 'other': 103, 'function': 5, 'same_class': 2}; disagreements (hand -> classifier: tokens): {"function -> other": ["We'll", "』の", "”等", " επίσης", "/other"], "new_bridge -> other": [" nitride"], "same_class -> other": ["Zn", "铅"]}
- 9B z2: 118 / 125 atoms agree (0.944; Cohen's kappa 0.3523) over 5 items; hand classes {'answer_own': 3, 'other': 116, 'new_bridge': 1, 'function': 5}; disagreements (hand -> classifier: tokens): {"answer_own -> other": ["土耳其", " jap", " Suomen"], "function -> other": [" ся", " Ihnen", " gibi", "和他的"]}
- 27B z2: 123 / 125 atoms agree (0.984; Cohen's kappa 0.496) over 5 items; hand classes {'other': 122, 'new_bridge': 1, 'same_class': 1, 'function': 1}; disagreements (hand -> classifier: tokens): {"same_class -> other": ["福州"], "function -> other": [" kerana"]}
- Muse z2: 118 / 125 atoms agree (0.944; Cohen's kappa 0.3451) over 5 items; hand classes {'other': 120, 'function': 2, 'bridge': 1, 'answer_own': 2}; disagreements (hand -> classifier: tokens): {"other -> function": ["(SO", "s", "*M"], "answer_own -> other": [" russa", " чеш"], "function -> other": ["sein"], "other -> same_class": [" Sebastian"]}

## Run checks

- qwen3.5-122b-a10b|qwen35_122b_x52_atoms_fwd: {"target": "qwen3.5-122b-a10b", "layer": 33, "e1_delta": {"max_abs_delta_lookup_minus_recall": 0.078125, "max_abs_delta": 0.8134765625, "max_rel_norm_lookup_minus_recall": 0.1440059095621109, "median_rel_norm_lookup_minus_recall": 0.0}, "letters": 242132, "e1_PP_fit_max_abs_diff": 0.0, "e1_x0_share_max_abs_gap": 5.000000000032756e-06, "e1_x0_share_items": 50, "e1_51_12_answer_atoms_items_agree": [50, 50], "e1_x0_atoms_same_25_items": [7, 7], "e1_recall_delta_atoms_in_common": {"all_25": 45, "items": 50, "min": 1, "median": 25.0}}
