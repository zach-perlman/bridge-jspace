# x52_atoms: what is inside the top-25 atoms of the lens part (batch 52 A; descriptive; no rule; UNVERIFIED)

Per item: Δ's 25 signed-OMP atoms over the J++ letter dictionary at L; each atom's class (automatic, scripts/x52_atoms.py classify); per item the class shares of the 25 atoms and of the rebuilt energy (the energy an atom adds when it enters, over the part's share of ||Δ||^2); means over items with 95 % cluster-bootstrap intervals over the bridge entity (10,000, seed 0). E1: one Δ serves both readers (identical prompts through the bridge word), so the two views differ only in which answer class is the reader's own. Z2: each reader its own Δ; both ask for the same answer, so 'answer_other' is empty. Chance: the class shares of 2,000 random letter tokens (seed 0) in the same items and views.

Classes: `bridge` the original bridge word; `new_bridge` the new bridge word; `scene_item` another item named in the scene; `person` a person's name in the scene; `answer_own` the reader's answer word; `answer_other` the other reader's answer word; `same_class` a same-class word not in the scene; `function` function words and punctuation; `other` other

Sources: qwen3.5-9b: {'e1': 'qwen35_9b_x52_atoms_fwd', 'z2': 'qwen35_9b_x52_atoms_fwd'}; qwen3.6-27b: {'e1': 'x52_atoms_fwd_27b', 'z2': 'x52_atoms_fwd_27b'}; muse-glimmer-30b: {'e1': 'muse30_x52_atoms_fwd', 'z2': 'muse30_x52_atoms_fwd'}

## Share of the rebuilt energy

| model | set | reader view | n (entities) | bridge | new_bridge | scene_item | person | answer_own | answer_other | same_class | function | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 9B | e1 | lookup | 50 (29) | 0.111 [0.091, 0.130] | 0.110 [0.093, 0.124] | 0.001 [0.000, 0.002] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.002] | 0.003 [0.001, 0.007] | 0.010 [0.004, 0.017] | 0.765 [0.739, 0.796] |
| 9B | e1 | recall | 50 (29) | 0.111 [0.091, 0.130] | 0.110 [0.093, 0.124] | 0.001 [0.000, 0.002] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.002] | 0.000 [0.000, 0.000] | 0.003 [0.001, 0.007] | 0.010 [0.004, 0.017] | 0.765 [0.739, 0.796] |
| 9B | z2 | lookup | 50 (41) | 0.017 [0.006, 0.031] | 0.015 [0.004, 0.029] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.004 [0.000, 0.008] | 0.006 [0.003, 0.010] | 0.957 [0.941, 0.973] |
| 9B | z2 | recall | 50 (41) | 0.015 [0.004, 0.029] | 0.016 [0.005, 0.029] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.004 [0.000, 0.009] | 0.006 [0.002, 0.010] | 0.959 [0.943, 0.975] |
| 27B | e1 | lookup | 50 (30) | 0.101 [0.075, 0.126] | 0.113 [0.096, 0.134] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.002] | 0.002 [0.000, 0.006] | 0.009 [0.004, 0.016] | 0.774 [0.739, 0.808] |
| 27B | e1 | recall | 50 (30) | 0.101 [0.075, 0.126] | 0.113 [0.096, 0.134] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.002] | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.006] | 0.009 [0.004, 0.016] | 0.774 [0.739, 0.808] |
| 27B | z2 | lookup | 50 (45) | 0.007 [0.000, 0.018] | 0.011 [0.003, 0.022] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.005] | 0.000 [0.000, 0.000] | 0.003 [0.000, 0.007] | 0.005 [0.002, 0.009] | 0.972 [0.957, 0.986] |
| 27B | z2 | recall | 50 (45) | 0.011 [0.002, 0.021] | 0.011 [0.003, 0.022] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.003 [0.000, 0.007] | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.006] | 0.008 [0.004, 0.013] | 0.966 [0.952, 0.979] |
| Muse | e1 | lookup | 50 (26) | 0.184 [0.165, 0.198] | 0.190 [0.168, 0.212] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.004 [0.001, 0.008] | 0.012 [0.007, 0.017] | 0.609 [0.584, 0.642] |
| Muse | e1 | recall | 50 (26) | 0.184 [0.165, 0.198] | 0.190 [0.168, 0.212] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.000] | 0.004 [0.001, 0.008] | 0.012 [0.007, 0.017] | 0.609 [0.584, 0.642] |
| Muse | z2 | lookup | 50 (44) | 0.010 [0.002, 0.021] | 0.006 [0.002, 0.011] | 0.001 [0.000, 0.004] | 0.000 [0.000, 0.000] | 0.008 [0.002, 0.016] | 0.000 [0.000, 0.000] | 0.004 [0.001, 0.010] | 0.013 [0.007, 0.019] | 0.957 [0.945, 0.970] |
| Muse | z2 | recall | 50 (44) | 0.011 [0.004, 0.021] | 0.008 [0.003, 0.014] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.012 [0.005, 0.020] | 0.000 [0.000, 0.000] | 0.003 [0.000, 0.007] | 0.009 [0.004, 0.014] | 0.957 [0.944, 0.970] |

## Share of the 25 atoms

| model | set | reader view | n (entities) | bridge | new_bridge | scene_item | person | answer_own | answer_other | same_class | function | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 9B | e1 | lookup | 50 (29) | 0.047 [0.039, 0.055] | 0.044 [0.036, 0.051] | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.003 [0.001, 0.006] | 0.008 [0.004, 0.013] | 0.896 [0.884, 0.909] |
| 9B | e1 | recall | 50 (29) | 0.047 [0.039, 0.055] | 0.044 [0.036, 0.051] | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.000] | 0.003 [0.001, 0.006] | 0.008 [0.004, 0.013] | 0.896 [0.884, 0.909] |
| 9B | e1 | chance | | 0.0004 | 0.0003 | 0.0000 | 0.0000 | 0.0002 | 0.0002 | 0.0012 | 0.0077 | 0.9900 |
| 9B | z2 | lookup | 50 (41) | 0.006 [0.003, 0.010] | 0.007 [0.002, 0.014] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.005] | 0.009 [0.004, 0.014] | 0.975 [0.968, 0.982] |
| 9B | z2 | recall | 50 (41) | 0.005 [0.002, 0.009] | 0.006 [0.002, 0.011] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.005] | 0.006 [0.002, 0.011] | 0.980 [0.974, 0.986] |
| 9B | z2 | chance | | 0.0006 | 0.0004 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0004 | 0.0077 | 0.9908 |
| 27B | e1 | lookup | 50 (30) | 0.041 [0.031, 0.051] | 0.040 [0.034, 0.048] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.002] | 0.001 [0.000, 0.003] | 0.010 [0.004, 0.015] | 0.908 [0.891, 0.923] |
| 27B | e1 | recall | 50 (30) | 0.041 [0.031, 0.051] | 0.040 [0.034, 0.048] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.002] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.010 [0.004, 0.015] | 0.908 [0.891, 0.923] |
| 27B | e1 | chance | | 0.0003 | 0.0003 | 0.0000 | 0.0000 | 0.0002 | 0.0001 | 0.0009 | 0.0077 | 0.9903 |
| 27B | z2 | lookup | 50 (45) | 0.003 [0.000, 0.007] | 0.007 [0.002, 0.013] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.004] | 0.006 [0.003, 0.010] | 0.981 [0.971, 0.990] |
| 27B | z2 | recall | 50 (45) | 0.005 [0.001, 0.009] | 0.006 [0.002, 0.011] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.004] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.010 [0.005, 0.016] | 0.976 [0.968, 0.984] |
| 27B | z2 | chance | | 0.0006 | 0.0005 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0004 | 0.0078 | 0.9907 |
| Muse | e1 | lookup | 50 (26) | 0.057 [0.051, 0.063] | 0.057 [0.050, 0.063] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.006 [0.002, 0.011] | 0.018 [0.010, 0.024] | 0.862 [0.852, 0.875] |
| Muse | e1 | recall | 50 (26) | 0.057 [0.051, 0.063] | 0.057 [0.050, 0.063] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.003] | 0.000 [0.000, 0.000] | 0.006 [0.002, 0.011] | 0.018 [0.010, 0.024] | 0.862 [0.852, 0.875] |
| Muse | e1 | chance | | 0.0006 | 0.0003 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0020 | 0.0084 | 0.9887 |
| Muse | z2 | lookup | 50 (44) | 0.006 [0.002, 0.011] | 0.005 [0.002, 0.009] | 0.002 [0.000, 0.004] | 0.000 [0.000, 0.000] | 0.005 [0.002, 0.008] | 0.000 [0.000, 0.000] | 0.003 [0.001, 0.007] | 0.015 [0.009, 0.021] | 0.964 [0.955, 0.973] |
| Muse | z2 | recall | 50 (44) | 0.006 [0.002, 0.011] | 0.007 [0.003, 0.012] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.007 [0.003, 0.012] | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.004] | 0.010 [0.005, 0.016] | 0.967 [0.959, 0.976] |
| Muse | z2 | chance | | 0.0006 | 0.0007 | 0.0000 | 0.0001 | 0.0000 | 0.0000 | 0.0005 | 0.0083 | 0.9898 |

## Items with at least one atom of the class

| model | set | reader view | n (entities) | bridge | new_bridge | scene_item | person | answer_own | answer_other | same_class | function | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 9B | e1 | lookup | 50 | 45 | 43 | 1 | 0 | 0 | 1 | 4 | 10 | 50 |
| 9B | e1 | recall | 50 | 45 | 43 | 1 | 0 | 1 | 0 | 4 | 10 | 50 |
| 9B | z2 | lookup | 50 | 8 | 8 | 0 | 0 | 0 | 0 | 3 | 10 | 50 |
| 9B | z2 | recall | 50 | 6 | 8 | 0 | 0 | 0 | 0 | 3 | 8 | 50 |
| 27B | e1 | lookup | 50 | 39 | 42 | 0 | 0 | 0 | 1 | 1 | 11 | 50 |
| 27B | e1 | recall | 50 | 39 | 42 | 0 | 0 | 1 | 0 | 1 | 11 | 50 |
| 27B | z2 | lookup | 50 | 3 | 7 | 0 | 0 | 1 | 0 | 2 | 8 | 50 |
| 27B | z2 | recall | 50 | 5 | 7 | 0 | 0 | 2 | 0 | 1 | 11 | 50 |
| Muse | e1 | lookup | 50 | 49 | 49 | 0 | 0 | 0 | 1 | 6 | 19 | 50 |
| Muse | e1 | recall | 50 | 49 | 49 | 0 | 0 | 1 | 0 | 6 | 19 | 50 |
| Muse | z2 | lookup | 50 | 8 | 6 | 2 | 0 | 6 | 0 | 4 | 17 | 50 |
| Muse | z2 | recall | 50 | 8 | 9 | 0 | 0 | 9 | 0 | 2 | 13 | 50 |

## The two bridge classes by how they matched (pooled share of rebuilt energy; the share of their atoms whose sign points the expected way: original -, new +)

| model | set | view | class | match | atoms | energy | sign as expected |
|---|---|---|---|---|---|---|---|
| 9B | e1 | lookup | bridge | alias | 6 | 0.0117 | 1.00 |
| 9B | e1 | lookup | bridge | first token | 5 | 0.0076 | 1.00 |
| 9B | e1 | lookup | bridge | initial | 15 | 0.0249 | 1.00 |
| 9B | e1 | lookup | bridge | key | 24 | 0.0548 | 1.00 |
| 9B | e1 | lookup | bridge | prefix | 9 | 0.0125 | 1.00 |
| 9B | e1 | lookup | new_bridge | alias | 5 | 0.0091 | 1.00 |
| 9B | e1 | lookup | new_bridge | first token | 2 | 0.0040 | 1.00 |
| 9B | e1 | lookup | new_bridge | initial | 11 | 0.0159 | 0.91 |
| 9B | e1 | lookup | new_bridge | key | 32 | 0.0735 | 1.00 |
| 9B | e1 | lookup | new_bridge | prefix | 5 | 0.0073 | 1.00 |
| 9B | z2 | lookup | bridge | initial | 1 | 0.0004 | 0.00 |
| 9B | z2 | lookup | bridge | key | 7 | 0.0182 | 1.00 |
| 9B | z2 | lookup | new_bridge | initial | 2 | 0.0012 | 0.00 |
| 9B | z2 | lookup | new_bridge | key | 5 | 0.0099 | 1.00 |
| 9B | z2 | lookup | new_bridge | prefix | 2 | 0.0036 | 0.50 |
| 9B | z2 | recall | bridge | key | 6 | 0.0168 | 1.00 |
| 9B | z2 | recall | new_bridge | key | 6 | 0.0119 | 1.00 |
| 9B | z2 | recall | new_bridge | prefix | 2 | 0.0036 | 1.00 |
| 27B | e1 | lookup | bridge | first token | 4 | 0.0115 | 1.00 |
| 27B | e1 | lookup | bridge | initial | 20 | 0.0382 | 1.00 |
| 27B | e1 | lookup | bridge | key | 17 | 0.0385 | 1.00 |
| 27B | e1 | lookup | bridge | part | 2 | 0.0032 | 1.00 |
| 27B | e1 | lookup | bridge | prefix | 8 | 0.0132 | 1.00 |
| 27B | e1 | lookup | new_bridge | alias | 2 | 0.0027 | 1.00 |
| 27B | e1 | lookup | new_bridge | first token | 3 | 0.0054 | 1.00 |
| 27B | e1 | lookup | new_bridge | initial | 21 | 0.0430 | 1.00 |
| 27B | e1 | lookup | new_bridge | key | 19 | 0.0547 | 1.00 |
| 27B | e1 | lookup | new_bridge | prefix | 5 | 0.0105 | 1.00 |
| 27B | z2 | lookup | bridge | key | 3 | 0.0071 | 1.00 |
| 27B | z2 | lookup | bridge | part | 1 | 0.0007 | 1.00 |
| 27B | z2 | lookup | new_bridge | initial | 3 | 0.0018 | 0.67 |
| 27B | z2 | lookup | new_bridge | key | 3 | 0.0053 | 1.00 |
| 27B | z2 | lookup | new_bridge | part | 1 | 0.0007 | 1.00 |
| 27B | z2 | lookup | new_bridge | prefix | 2 | 0.0031 | 0.50 |
| 27B | z2 | recall | bridge | key | 5 | 0.0105 | 1.00 |
| 27B | z2 | recall | bridge | part | 1 | 0.0007 | 1.00 |
| 27B | z2 | recall | new_bridge | initial | 2 | 0.0009 | 0.50 |
| 27B | z2 | recall | new_bridge | key | 3 | 0.0057 | 1.00 |
| 27B | z2 | recall | new_bridge | part | 1 | 0.0005 | 1.00 |
| 27B | z2 | recall | new_bridge | prefix | 2 | 0.0031 | 0.50 |
| Muse | e1 | lookup | bridge | initial | 23 | 0.0389 | 1.00 |
| Muse | e1 | lookup | bridge | key | 44 | 0.1426 | 1.00 |
| Muse | e1 | lookup | bridge | prefix | 4 | 0.0026 | 1.00 |
| Muse | e1 | lookup | new_bridge | alias | 2 | 0.0052 | 1.00 |
| Muse | e1 | lookup | new_bridge | initial | 24 | 0.0394 | 1.00 |
| Muse | e1 | lookup | new_bridge | key | 44 | 0.1512 | 1.00 |
| Muse | e1 | lookup | new_bridge | prefix | 1 | 0.0011 | 1.00 |
| Muse | z2 | lookup | bridge | initial | 3 | 0.0014 | 0.00 |
| Muse | z2 | lookup | bridge | key | 3 | 0.0058 | 1.00 |
| Muse | z2 | lookup | bridge | part | 1 | 0.0006 | 1.00 |
| Muse | z2 | lookup | bridge | prefix | 1 | 0.0030 | 1.00 |
| Muse | z2 | lookup | new_bridge | initial | 2 | 0.0011 | 1.00 |
| Muse | z2 | lookup | new_bridge | key | 1 | 0.0016 | 1.00 |
| Muse | z2 | lookup | new_bridge | prefix | 3 | 0.0022 | 1.00 |
| Muse | z2 | recall | bridge | initial | 3 | 0.0018 | 0.33 |
| Muse | z2 | recall | bridge | key | 4 | 0.0065 | 1.00 |
| Muse | z2 | recall | bridge | prefix | 1 | 0.0034 | 1.00 |
| Muse | z2 | recall | new_bridge | initial | 4 | 0.0025 | 0.75 |
| Muse | z2 | recall | new_bridge | key | 2 | 0.0027 | 1.00 |
| Muse | z2 | recall | new_bridge | prefix | 3 | 0.0021 | 1.00 |

## 'other' by detail (pooled share of rebuilt energy)

- 9B e1 lookup: {'none': 0.7639}; median part share of ||Δ||^2 0.223
- 9B z2 lookup: {'in the prompt': 0.0561, 'none': 0.9012}; median part share of ||Δ||^2 0.194
- 9B z2 recall: {'in the prompt': 0.0567, 'none': 0.9017}; median part share of ||Δ||^2 0.191
- 27B e1 lookup: {'answer kind': 0.0009, 'none': 0.7673}; median part share of ||Δ||^2 0.144
- 27B z2 lookup: {'in the prompt': 0.0536, 'none': 0.9182}; median part share of ||Δ||^2 0.158
- 27B z2 recall: {'in the prompt': 0.0594, 'none': 0.9062}; median part share of ||Δ||^2 0.154
- Muse e1 lookup: {'answer kind': 0.0018, 'none': 0.6002}; median part share of ||Δ||^2 0.139
- Muse z2 lookup: {'answer kind': 0.0013, 'in the prompt': 0.0726, 'none': 0.8836}; median part share of ||Δ||^2 0.119
- Muse z2 recall: {'answer kind': 0.0009, 'in the prompt': 0.0751, 'none': 0.8823}; median part share of ||Δ||^2 0.118

## Hand check (the lookup's view)

Blindness: the 9B / 27B labels (hand-20261028T235223Z) are NOT blind. While the bridge-spelling rules (prefix / initial / part, Chinese names) were being written, the labeller had seen the classifier's labels on the first atoms of 4 of the 5 27B items (P2-L0-0008, 0051, 0084, 0097) and 1 of the 5 9B items (P2-L0-0016), and the rules were shaped on such items; that folder's write_labels.py docstring ('without the classifier's output') is wrong on this point. Muse's labels (hand-20261028T235654Z) are blind: Muse's atoms were first seen on its sheet, after the classifier was committed (11ee8c6f), and the classifier was not changed afterwards. Z2 (hand-20261029T000000Z, the lookup's own passage; not asked for by the brief, added because Z2's answer words come in other languages and as prefixes): not blind (some of its items were among the Z2 examples already printed with the classifier's labels); the classifier was not changed after it.

- 9B e1: 121 / 125 atoms agree (0.968; Cohen's kappa 0.8548) over 5 items; hand classes {'bridge': 6, 'new_bridge': 7, 'other': 108, 'function': 4}; disagreements (hand -> classifier: tokens): {"function -> other": ["и", "ни", "مع", "ein"]}
- 27B e1: 119 / 125 atoms agree (0.952; Cohen's kappa 0.7339) over 5 items; hand classes {'new_bridge': 5, 'bridge': 4, 'other': 111, 'function': 4, 'answer_other': 1}; disagreements (hand -> classifier: tokens): {"function -> other": [" Ты", " və", " 에서", " των"], "other -> function": [">i"], "bridge -> other": ["EEEE"]}
- Muse e1: 117 / 125 atoms agree (0.936; Cohen's kappa 0.7553) over 5 items; hand classes {'new_bridge': 7, 'bridge': 8, 'other': 103, 'function': 5, 'same_class': 2}; disagreements (hand -> classifier: tokens): {"function -> other": ["We'll", "』の", "”等", " επίσης", "/other"], "new_bridge -> other": [" nitride"], "same_class -> other": ["Zn", "铅"]}
- 9B z2: 118 / 125 atoms agree (0.944; Cohen's kappa 0.3523) over 5 items; hand classes {'answer_own': 3, 'other': 116, 'new_bridge': 1, 'function': 5}; disagreements (hand -> classifier: tokens): {"answer_own -> other": ["土耳其", " jap", " Suomen"], "function -> other": [" ся", " Ihnen", " gibi", "和他的"]}
- 27B z2: 123 / 125 atoms agree (0.984; Cohen's kappa 0.496) over 5 items; hand classes {'other': 122, 'new_bridge': 1, 'same_class': 1, 'function': 1}; disagreements (hand -> classifier: tokens): {"same_class -> other": ["福州"], "function -> other": [" kerana"]}
- Muse z2: 118 / 125 atoms agree (0.944; Cohen's kappa 0.3451) over 5 items; hand classes {'other': 120, 'function': 2, 'bridge': 1, 'answer_own': 2}; disagreements (hand -> classifier: tokens): {"other -> function": ["(SO", "s", "*M"], "answer_own -> other": [" russa", " чеш"], "function -> other": ["sein"], "other -> same_class": [" Sebastian"]}

## Run checks

- qwen3.5-9b|qwen35_9b_x52_atoms_fwd: {"target": "qwen3.5-9b", "layer": 12, "e1_delta": {"max_abs_delta_lookup_minus_recall": 0.0, "max_abs_delta": 2.9765625, "max_rel_norm_lookup_minus_recall": 0.0, "median_rel_norm_lookup_minus_recall": 0.0}, "z2_delta": {}, "letters": 242132, "e1_PP_fit_max_abs_diff": 0.0, "e1_x0_share_max_abs_gap": 5.000000000032756e-06, "e1_x0_share_items": 50, "e1_51_12_answer_atoms_items_agree": [50, 50], "e1_x0_atoms_same_25_items": [6, 6], "e1_recall_delta_atoms_in_common": {"all_25": 50, "items": 50, "min": 25, "median": 25.0}, "z2_K_fit_max_abs_diff": 0.0, "z2_M_fit_max_abs_diff": 0.0, "z2_x0_share_max_abs_gap": null, "z2_x0_share_items": 0, "z2_51_12_answer_atoms_items_agree": [100, 100], "z2_x0_atoms_same_25_items": [0, 0]}
- qwen3.6-27b|x52_atoms_fwd_27b: {"target": "qwen3.6-27b", "layer": 32, "e1_delta": {"max_abs_delta_lookup_minus_recall": 0.75, "max_abs_delta": 8.96875, "max_rel_norm_lookup_minus_recall": 0.03438575938344002, "median_rel_norm_lookup_minus_recall": 0.0}, "z2_delta": {}, "letters": 242132, "e1_PP_fit_max_abs_diff": 0.0, "e1_x0_share_max_abs_gap": 5.0000000000050004e-06, "e1_x0_share_items": 50, "e1_51_12_answer_atoms_items_agree": [50, 50], "e1_x0_atoms_same_25_items": [3, 3], "e1_recall_delta_atoms_in_common": {"all_25": 37, "items": 50, "min": 4, "median": 25.0}, "z2_K_fit_max_abs_diff": 0.0, "z2_M_fit_max_abs_diff": 0.0, "z2_x0_share_max_abs_gap": null, "z2_x0_share_items": 0, "z2_51_12_answer_atoms_items_agree": [100, 100], "z2_x0_atoms_same_25_items": [0, 0]}
- muse-glimmer-30b|muse30_x52_atoms_fwd: {"target": "muse-glimmer-30b", "layer": 26, "e1_delta": {"max_abs_delta_lookup_minus_recall": 0.0, "max_abs_delta": 54.0, "max_rel_norm_lookup_minus_recall": 0.0, "median_rel_norm_lookup_minus_recall": 0.0}, "z2_delta": {}, "letters": 190773, "e1_PP_fit_max_abs_diff": 0.0, "e1_x0_share_max_abs_gap": 5.0000000000050004e-06, "e1_x0_share_items": 50, "e1_51_12_answer_atoms_items_agree": [50, 50], "e1_x0_atoms_same_25_items": [0, 0], "e1_recall_delta_atoms_in_common": {"all_25": 50, "items": 50, "min": 25, "median": 25.0}, "z2_K_fit_max_abs_diff": 0.0, "z2_M_fit_max_abs_diff": 0.0, "z2_x0_share_max_abs_gap": null, "z2_x0_share_items": 0, "z2_51_12_answer_atoms_items_agree": [0, 0], "z2_x0_atoms_same_25_items": [0, 0]}
