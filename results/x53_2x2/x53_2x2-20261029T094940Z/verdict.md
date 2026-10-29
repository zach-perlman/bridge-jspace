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

## 9B: pending (no run qwen35_9b_x53_2x2 here)

## 27B (x53_2x2_27b, L32; relation for the word cells: None)

Rule across cells: **can't tell: (Q-after, word), (Q-before, word) without a label**. Cross-check: **can't tell (a cell without numbers)**.

| cell | gate (O read acc. lookup / recall) | n | recall: 51.12 label | lookup: 51.12 label | conflict test lookup: extra loss beyond random | recall: extra loss | recall e2/e1 | recall e3 | recall answer word not read |
|---|---|---|---|---|---|---|---|---|---|
| (Q-after, number) | 0.9967 / 0.9767 | 200 | **the lens effect is the entity** | the lens effect is the entity | 0.14 [0.08, 0.20] (mixed) | 0.74 [0.66, 0.80] (through) | 0.93 [0.85, 0.99] | 0.03 [0.01, 0.05] | 0.79 [0.72, 0.86] |
| (Q-before, number) | 1.0 / 0.885 | 200 | **the lens effect is the entity** | the answer word is not read at the bridge word (lens rank > 50 on >= 90 % of items) | 0.22 [0.15, 0.31] (through) | 0.56 [0.46, 0.65] (through) | 0.91 [0.81, 0.98] | 0.01 [0.00, 0.02] | 0.77 [0.69, 0.84] |
| (Q-after, word) | - | - | pending | | | | | | |
| (Q-before, word) | - | - | pending | | | | | | |

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

## Lightning: pending (no run nem35l_x53_2x2 here)

Status: UNVERIFIED until a human adds it to VERIFIED.md.
