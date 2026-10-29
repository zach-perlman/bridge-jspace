# 53.1: the 2x2, question position x answer type (UNVERIFIED; no prediction)

Batch 53, test 53.1 (jobs/c3/batch53.yaml). The brief's 53.1, verbatim:

```
53.1 (top) The 2x2: question position x answer type, our locker scenes.
  Models: 9B, then 27B, then Lightning if its gate passes.
  Cells: (Q-after, number) = the main test as is; (Q-before, number): the same
  scenes with both questions placed before the scene ("Question: ... Scene:
  ..."), digits kept; (Q-after, word) and (Q-before, word): the recall asks a
  relation with a one-token word answer instead of the atomic number. Choose the
  relation on the 9B before any test: one-token answers, the 9B's accuracy
  >= 0.8, the answer word must not share a token with any spelling, initial or
  symbol of the item (the atoms classifier's bridge classes). Lookup questions
  unchanged.
  Per cell: the main gate; the conflict test at L; 51.12's arms with the readout
  check first; the atom inventory (batch 52 A) on 50 items.
  Rule per cell: 51.12's labels (entity / answer / mixed / answer word not read).
  Rule across cells:
  - "position": (Q-before, number) is answer or mixed and (Q-after, word) is
    entity;
  - "readability": (Q-after, word) is answer or mixed and (Q-before, number)
    is entity;
  - "both": each single change gives mixed and (Q-before, word) gives answer;
  - "neither": all four entity.
  Cross-check, decisive for the story: the conflict test's lookup loses <= 0.10
  beyond random in all four cells ("the pointer does not depend on the
  question"); report per cell.
```

51.12's rule (x51_answer): Per model, per reader: "the lens effect is the entity": arm 2 keeps >= 0.7 of arm 1's extra loss and arm 3 costs <= 0.10 beyond random. "The lens effect is the answer": arm 2 falls to <= 0.3 of arm 1 and arm 3 alone costs >= 0.5 of arm 1. Else: mixed, report both shares. Amendment (Dan 20:20): before the arms, the lens readout check at the bridge word; the verdict says which case held, either 'the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items)' or the arm-based entity / answer / mixed (never 'void by construction'). Z2: arm 3 is read against its controls (a same-size random part and a frequency-matched part), not against zero.

Dan 11:10 (batch53.yaml next_1110, item 3), verbatim: "Rule: the conflict test's, verbatim; across: "the pointer does not depend on the question's position" if the lookup loses <= 0.10 in both cells on a model." As computed: the conflict test's lookup extra loss beyond random (X0's excess, point estimate) in (Q-after, number) and (Q-before, number); 'does not hold' names a tested cell above 0.10; 'can't tell' while a cell is untested and none is above. Kept apart from the brief's rule across cells.

As computed: see scripts/x53_2x2.py's docstring (cells, relation, gate, conflict test, 51.12 arms, atoms). The cell's label is the recall's 51.12 label (51.12's decisive E1 reader); the lookup's beside. Cluster bootstrap over the bridge entity (10000, seed 0).

## 9B (qwen35_9b_x53_2x2, L12; relation for the word cells: animals/class)

Across the number cells (Dan 11:10): **can't tell: (Q-before, number) not tested**.

Rule across cells (the brief's): **can't tell: (Q-before, number), (Q-after, word), (Q-before, word) without a label (patterns the labelled cells leave open: position, readability, both, neither)**. Cross-check: **can't tell (a cell without numbers; the tested ones <= 0.10)**.

Word cells: relation animals/class (question 'What class of animal is {d}?'), on the 191 scenes it answers, not 600 (Dan 10:20: coverage >= 150 on the 9B, then accuracy >= 0.80); checked and short of 150 scenes: animals/young 17, elements/state 107, greek/vowel 121; items dropped for a clash with their own spelling, initial or symbol: ['mouse']. The recall's O read accuracy on (Q-after, word) = 0.3822 on qwen3.5-9b (>= 0.80: False; the 9B's decides).

Descriptive context (results/x53_2x2/diag_words-20261029T095338Z, CPU, no rule): what the recall's first word was: (Q-after, word) the asked pick itself (the animal) 236; the class (right) 145; another class word 1 (of 382 recall prompts) | (Q-before, word) the class (right) 351; the asked pick itself (the animal) 19; another class word 12 (of 382 recall prompts).

| cell | gate (O read acc. lookup / recall) | n | recall: 51.12 label | lookup: 51.12 label | conflict test lookup: extra loss beyond random | recall: extra loss | recall e2/e1 | recall e3 | recall answer word not read |
|---|---|---|---|---|---|---|---|---|---|
| (Q-after, number) | 0.95 / 0.8683 | 200 | **the lens effect is the entity** | can't tell (arm 1 has no extra loss beyond random) | -0.05 [-0.09, 0.00] (around) | 0.50 [0.41, 0.57] (through) | 0.95 [0.90, 0.99] | 0.00 [0.00, 0.00] | 0.56 [0.47, 0.66] |
| (Q-before, number) | 0.955 / 0.7633 | - | not tested (gate 0.76 < 0.80) | | | | | | |
| (Q-after, word) | 0.9476 / 0.3822 | - | not tested (the relation's 9B accuracy < 0.80) | | | | | | |
| (Q-before, word) | 0.9686 / 0.9162 | - | not tested (the relation's 9B accuracy < 0.80) | | | | | | |

### (Q-after, number)

- lookup: rates none 0.01 [0.00, 0.02], whole 0.53 [0.45, 0.62], no_jpp 0.41 [0.34, 0.52], no_jpp_rand 0.39 [0.31, 0.49], no_jpp_A 0.41 [0.33, 0.51], no_jpp_A_rand 0.40 [0.32, 0.50], no_A 0.53 [0.45, 0.62], no_A_rand 0.51 [0.43, 0.61]; extra e1 -0.05 [-0.09, 0.00], e2 -0.02 [-0.07, 0.04], e3 -0.04 [-0.08, -0.01]; readout: top-50 O 0.14 [0.08, 0.20], S 0.10 [0.06, 0.13], not read 0.77 [0.70, 0.83] (case arms); arm rule: can't tell (arm 1 has no extra loss beyond random); X0's validity bar True
- recall: rates none 0.00 [0.00, 0.00], whole 0.98 [0.97, 1.00], no_jpp 0.46 [0.38, 0.55], no_jpp_rand 0.95 [0.92, 0.98], no_jpp_A 0.49 [0.41, 0.58], no_jpp_A_rand 0.95 [0.93, 0.98], no_A 0.98 [0.97, 1.00], no_A_rand 0.98 [0.97, 1.00]; extra e1 0.50 [0.41, 0.57], e2 0.47 [0.39, 0.55], e3 0.00 [0.00, 0.00]; readout: top-50 O 0.28 [0.16, 0.40], S 0.27 [0.20, 0.33], not read 0.56 [0.47, 0.66] (case arms); arm rule: the lens effect is the entity; X0's validity bar True
- atoms (lookup's view, n 50): energy shares bridge 0.11 [0.09, 0.13], new bridge 0.12 [0.09, 0.15], own answer 0.00 [0.00, 0.00], other answer 0.00 [0.00, 0.00], other 0.75 [0.71, 0.80]; part's share median 0.224
- atoms (recall's view, n 50): energy shares bridge 0.11 [0.09, 0.13], new bridge 0.12 [0.09, 0.15], own answer 0.00 [0.00, 0.00], other answer 0.00 [0.00, 0.00], other 0.75 [0.71, 0.80]; part's share median 0.224
- against the stored main test (qwen35_9b_x0_necessity): recall: whole 200/200, arm 1 extra loss rerun 0.497 vs stored 0.497; lookup: whole 199/200, arm 1 extra loss rerun -0.047 vs stored -0.029

## 27B (x53_2x2_27b, L32; relation for the word cells: animals/class)

Across the number cells (Dan 11:10): **does not hold: the lookup loses > 0.10 beyond random in (Q-after, number) (0.14), (Q-before, number) (0.22)**.

Rule across cells (the brief's): **can't tell: (Q-after, word), (Q-before, word) without a label (patterns the labelled cells leave open: readability, neither)**. Cross-check: **does not hold: the lookup loses > 0.10 beyond random in (Q-after, number) (0.14), (Q-before, number) (0.22)**.

Word cells: relation animals/class (question 'What class of animal is {d}?'), on the 191 scenes it answers, not 600 (Dan 10:20: coverage >= 150 on the 9B, then accuracy >= 0.80); checked and short of 150 scenes: animals/young 17, elements/state 107, greek/vowel 121; items dropped for a clash with their own spelling, initial or symbol: ['mouse']. The recall's O read accuracy on (Q-after, word) = 0.7592 on qwen3.6-27b (>= 0.80: False; the 9B's decides).

| cell | gate (O read acc. lookup / recall) | n | recall: 51.12 label | lookup: 51.12 label | conflict test lookup: extra loss beyond random | recall: extra loss | recall e2/e1 | recall e3 | recall answer word not read |
|---|---|---|---|---|---|---|---|---|---|
| (Q-after, number) | 0.9967 / 0.9767 | 200 | **the lens effect is the entity** | the lens effect is the entity | 0.14 [0.08, 0.20] (mixed) | 0.74 [0.66, 0.80] (through) | 0.93 [0.85, 0.99] | 0.03 [0.01, 0.05] | 0.79 [0.72, 0.86] |
| (Q-before, number) | 1.0 / 0.885 | 200 | **the lens effect is the entity** | the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) | 0.22 [0.15, 0.31] (through) | 0.56 [0.46, 0.65] (through) | 0.91 [0.81, 0.98] | 0.01 [0.00, 0.02] | 0.77 [0.69, 0.84] |
| (Q-after, word) | 1.0 / 0.7592 | - | not tested (the relation's 9B accuracy < 0.80) | | | | | | |
| (Q-before, word) | 1.0 / 0.9895 | - | not tested (the relation's 9B accuracy < 0.80) | | | | | | |

### (Q-after, number)

- lookup: rates none 0.00 [0.00, 0.00], whole 0.43 [0.37, 0.50], no_jpp 0.35 [0.29, 0.42], no_jpp_rand 0.41 [0.35, 0.48], no_jpp_A 0.36 [0.30, 0.43], no_jpp_A_rand 0.41 [0.35, 0.48], no_A 0.43 [0.37, 0.50], no_A_rand 0.42 [0.36, 0.49]; extra e1 0.14 [0.08, 0.20], e2 0.12 [0.06, 0.18], e3 -0.01 [-0.04, 0.00]; readout: top-50 O 0.07 [0.03, 0.11], S 0.04 [0.02, 0.06], not read 0.90 [0.85, 0.93] (case arms); arm rule: the lens effect is the entity; X0's validity bar True
- recall: rates none 0.00 [0.00, 0.00], whole 0.75 [0.68, 0.81], no_jpp 0.17 [0.12, 0.25], no_jpp_rand 0.73 [0.67, 0.79], no_jpp_A 0.22 [0.15, 0.30], no_jpp_A_rand 0.73 [0.68, 0.79], no_A 0.73 [0.66, 0.79], no_A_rand 0.75 [0.68, 0.81]; extra e1 0.74 [0.66, 0.80], e2 0.69 [0.59, 0.77], e3 0.03 [0.01, 0.05]; readout: top-50 O 0.12 [0.04, 0.19], S 0.12 [0.08, 0.15], not read 0.79 [0.72, 0.86] (case arms); arm rule: the lens effect is the entity; X0's validity bar True
- atoms (lookup's view, n 50): energy shares bridge 0.13 [0.10, 0.15], new bridge 0.14 [0.12, 0.17], own answer 0.00 [0.00, 0.00], other answer 0.00 [0.00, 0.00], other 0.72 [0.68, 0.76]; part's share median 0.154
- atoms (recall's view, n 50): energy shares bridge 0.13 [0.10, 0.15], new bridge 0.14 [0.12, 0.17], own answer 0.00 [0.00, 0.01], other answer 0.00 [0.00, 0.00], other 0.72 [0.68, 0.76]; part's share median 0.154
- against the stored main test (x0_necessity_27b_chat): recall: whole 200/200, arm 1 extra loss rerun 0.740 vs stored 0.740; lookup: whole 200/200, arm 1 extra loss rerun 0.140 vs stored 0.140

### (Q-before, number)

- lookup: rates none 0.00 [0.00, 0.00], whole 0.49 [0.43, 0.56], no_jpp 0.33 [0.27, 0.40], no_jpp_rand 0.43 [0.38, 0.51], no_jpp_A 0.34 [0.29, 0.42], no_jpp_A_rand 0.45 [0.39, 0.51], no_A 0.48 [0.43, 0.55], no_A_rand 0.49 [0.43, 0.56]; extra e1 0.22 [0.15, 0.31], e2 0.20 [0.11, 0.30], e3 0.01 [0.00, 0.03]; readout: top-50 O 0.04 [0.02, 0.08], S 0.04 [0.02, 0.06], not read 0.92 [0.88, 0.95] (case not_read); arm rule: the lens effect is the entity; X0's validity bar True
- recall: rates none 0.00 [0.00, 0.00], whole 0.97 [0.95, 0.99], no_jpp 0.40 [0.32, 0.49], no_jpp_rand 0.94 [0.90, 0.98], no_jpp_A 0.46 [0.37, 0.57], no_jpp_A_rand 0.95 [0.92, 0.98], no_A 0.97 [0.94, 0.99], no_A_rand 0.97 [0.95, 0.99]; extra e1 0.56 [0.46, 0.65], e2 0.51 [0.39, 0.60], e3 0.01 [0.00, 0.02]; readout: top-50 O 0.14 [0.07, 0.22], S 0.11 [0.08, 0.14], not read 0.77 [0.69, 0.84] (case arms); arm rule: the lens effect is the entity; X0's validity bar True
- atoms (recall's view, n 50): energy shares bridge 0.15 [0.13, 0.18], new bridge 0.13 [0.10, 0.15], own answer 0.00 [0.00, 0.00], other answer 0.00 [0.00, 0.00], other 0.70 [0.67, 0.75]; part's share median 0.169
- atoms (lookup's view, n 50): energy shares bridge 0.15 [0.12, 0.17], new bridge 0.13 [0.10, 0.15], own answer 0.00 [0.00, 0.00], other answer 0.00 [0.00, 0.00], other 0.72 [0.69, 0.75]; part's share median 0.168

## 122B (qwen35_122b_x53_2x2, L33; relation for the word cells: None)

Across the number cells (Dan 11:10): **the pointer does not depend on the question's position (lookup <= 0.10 beyond random in both number cells)**.

Rule across cells (the brief's): **can't tell: (Q-after, word), (Q-before, word) without a label (patterns the labelled cells leave open: none)**. Cross-check: **can't tell (a cell without numbers; the tested ones <= 0.10)**.

| cell | gate (O read acc. lookup / recall) | n | recall: 51.12 label | lookup: 51.12 label | conflict test lookup: extra loss beyond random | recall: extra loss | recall e2/e1 | recall e3 | recall answer word not read |
|---|---|---|---|---|---|---|---|---|---|
| (Q-after, number) | 0.9917 / 0.85 | 200 | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items)** | the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) | 0.01 [-0.06, 0.08] (around) | 0.27 [0.17, 0.38] (through) | 0.98 [0.86, 1.18] | 0.01 [-0.01, 0.04] | 1.00 [1.00, 1.00] |
| (Q-before, number) | 0.9983 / 0.84 | 200 | **the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items)** | the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) | -0.03 [-0.11, 0.05] (around) | 0.31 [0.22, 0.39] (through) | 0.87 [0.73, 1.02] | 0.03 [0.00, 0.06] | 1.00 [1.00, 1.00] |
| (Q-after, word) | - | - | stopped (Dan 11:10: the wording fails) | | | | | | |
| (Q-before, word) | - | - | stopped (Dan 11:10: the wording fails) | | | | | | |

### (Q-after, number)

- lookup: rates none 0.01 [0.00, 0.02], whole 0.43 [0.38, 0.50], no_jpp 0.36 [0.31, 0.43], no_jpp_rand 0.36 [0.31, 0.43], no_jpp_A 0.36 [0.31, 0.42], no_jpp_A_rand 0.36 [0.31, 0.43], no_A 0.44 [0.39, 0.51], no_A_rand 0.45 [0.39, 0.51]; extra e1 0.01 [-0.06, 0.08], e2 0.01 [-0.07, 0.10], e3 0.01 [-0.03, 0.05]; readout: top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], not read 1.00 [1.00, 1.00] (case not_read); arm rule: the lens effect is the entity; X0's validity bar True
- recall: rates none 0.01 [0.00, 0.04], whole 0.93 [0.88, 0.96], no_jpp 0.59 [0.49, 0.69], no_jpp_rand 0.84 [0.78, 0.89], no_jpp_A 0.61 [0.53, 0.70], no_jpp_A_rand 0.85 [0.79, 0.90], no_A 0.91 [0.86, 0.95], no_A_rand 0.92 [0.88, 0.95]; extra e1 0.27 [0.17, 0.38], e2 0.26 [0.18, 0.35], e3 0.01 [-0.01, 0.04]; readout: top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], not read 1.00 [1.00, 1.00] (case not_read); arm rule: the lens effect is the entity; X0's validity bar True
- atoms (lookup's view, n 50): energy shares bridge 0.18 [0.15, 0.20], new bridge 0.16 [0.14, 0.19], own answer 0.00 [0.00, 0.00], other answer 0.00 [0.00, 0.00], other 0.65 [0.62, 0.68]; part's share median 0.229
- atoms (recall's view, n 50): energy shares bridge 0.18 [0.15, 0.20], new bridge 0.16 [0.14, 0.19], own answer 0.00 [0.00, 0.00], other answer 0.00 [0.00, 0.00], other 0.65 [0.62, 0.68]; part's share median 0.229
- against the stored main test (qwen35_122b_x0_necessity_r2): recall: whole 193/200, arm 1 extra loss rerun 0.270 vs stored 0.315; lookup: whole 194/200, arm 1 extra loss rerun 0.011 vs stored 0.000

### (Q-before, number)

- lookup: rates none 0.00 [0.00, 0.00], whole 0.54 [0.47, 0.61], no_jpp 0.47 [0.41, 0.55], no_jpp_rand 0.46 [0.39, 0.53], no_jpp_A 0.48 [0.42, 0.55], no_jpp_A_rand 0.46 [0.40, 0.53], no_A 0.54 [0.47, 0.61], no_A_rand 0.54 [0.47, 0.61]; extra e1 -0.03 [-0.11, 0.05], e2 -0.05 [-0.11, 0.02], e3 0.00 [0.00, 0.00]; readout: top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], not read 1.00 [1.00, 1.00] (case not_read); arm rule: can't tell (arm 1 has no extra loss beyond random); X0's validity bar True
- recall: rates none 0.01 [0.00, 0.02], whole 0.98 [0.96, 1.00], no_jpp 0.64 [0.54, 0.72], no_jpp_rand 0.94 [0.89, 0.97], no_jpp_A 0.70 [0.62, 0.78], no_jpp_A_rand 0.96 [0.93, 0.99], no_A 0.95 [0.92, 0.98], no_A_rand 0.98 [0.96, 1.00]; extra e1 0.31 [0.22, 0.39], e2 0.27 [0.19, 0.35], e3 0.03 [0.00, 0.06]; readout: top-50 O 0.00 [0.00, 0.00], S 0.00 [0.00, 0.00], not read 1.00 [1.00, 1.00] (case not_read); arm rule: the lens effect is the entity; X0's validity bar True
- atoms (recall's view, n 50): energy shares bridge 0.20 [0.18, 0.23], new bridge 0.19 [0.16, 0.22], own answer 0.00 [0.00, 0.01], other answer 0.00 [0.00, 0.00], other 0.60 [0.56, 0.64]; part's share median 0.265
- atoms (lookup's view, n 50): energy shares bridge 0.18 [0.15, 0.22], new bridge 0.20 [0.18, 0.22], own answer 0.00 [0.00, 0.00], other answer 0.00 [0.00, 0.00], other 0.61 [0.57, 0.66]; part's share median 0.261

## Muse: pending (no run muse30_x53_2x2 here)

## Lightning: pending (no run nem35l_x53_2x2 here)

Status: UNVERIFIED until a human adds it to VERIFIED.md.
