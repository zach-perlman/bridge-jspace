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

As computed: see scripts/x53_2x2.py's docstring (cells, relation, gate, conflict test, 51.12 arms, atoms). The cell's label is the recall's 51.12 label (51.12's decisive E1 reader); the lookup's beside. Cluster bootstrap over the bridge entity (10000, seed 0).

## 9B (qwen35_9b_x53_2x2, L12; relation for the word cells: animals/class)

Rule across cells: **can't tell: (Q-before, number), (Q-after, word), (Q-before, word) without a label**. Cross-check: **can't tell (a cell without numbers)**.

Word cells: relation animals/class (question 'What class of animal is {d}?'), on the 191 scenes it answers, not 600 (Dan 10:20: coverage >= 150 on the 9B, then accuracy >= 0.80); checked and short of 150 scenes: animals/young 17, elements/state 107, greek/vowel 121; items dropped for a clash with their own spelling, initial or symbol: ['mouse']. The recall's O read accuracy on (Q-after, word) = 0.3822 on qwen3.5-9b (>= 0.80: False; the 9B's decides).

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

Rule across cells: **can't tell: (Q-after, number), (Q-before, number), (Q-after, word), (Q-before, word) without a label**. Cross-check: **can't tell (a cell without numbers)**.

Word cells: relation animals/class (question 'What class of animal is {d}?'), on the 191 scenes it answers, not 600 (Dan 10:20: coverage >= 150 on the 9B, then accuracy >= 0.80); checked and short of 150 scenes: animals/young 17, elements/state 107, greek/vowel 121; items dropped for a clash with their own spelling, initial or symbol: ['mouse']. The recall's O read accuracy on (Q-after, word) = 0.7592 on qwen3.6-27b (>= 0.80: False; the 9B's decides).

| cell | gate (O read acc. lookup / recall) | n | recall: 51.12 label | lookup: 51.12 label | conflict test lookup: extra loss beyond random | recall: extra loss | recall e2/e1 | recall e3 | recall answer word not read |
|---|---|---|---|---|---|---|---|---|---|
| (Q-after, number) | - | - | pending | | | | | | |
| (Q-before, number) | - | - | pending | | | | | | |
| (Q-after, word) | 1.0 / 0.7592 | - | not tested (the relation's 9B accuracy < 0.80) | | | | | | |
| (Q-before, word) | 1.0 / 0.9895 | - | not tested (the relation's 9B accuracy < 0.80) | | | | | | |

## Lightning: pending (no run nem35l_x53_2x2 here)

Status: UNVERIFIED until a human adds it to VERIFIED.md.
