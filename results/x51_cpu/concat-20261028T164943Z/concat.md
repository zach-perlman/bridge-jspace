# 49.3 concatenation probe (batch 51, CPU item 4)

After 49.3 (descriptive extension, its rule's bars). The lookup's O prompt in the clean-design scenes; per locker sentence with a picker, the states of all its tokens concatenated in token-role blocks (x49_probe's keys: w:The, w:locker, w:of, [w:the], item, w:is, [w:space], number, w:., and Muse's item_pre; zeros where a sentence lacks a role). Probes and scoring are x49_probe.probe_view unchanged: 48.3's ridge (standardized features, the penalty by an inner CV), out of fold over 5 folds with whole locker items held out (seed 0), trained and scored within the stratum. (i) the picker of the scene's three people (chance 1/3; rule cell: the asked item's sentence in locker-after scenes); (ii) picked by the asked person (balanced accuracy, chance 0.5). Control: the same in locker-first scenes ('before'). Cluster bootstrap over the sentence's item (10,000, seed 0). Label per layer on the points: person if (i) >= 0.85; flag if (ii) >= 0.85 with (i) <= 0.5; chance if both <= chance + 0.1; else in between; a person / flag label with the control above chance reads not interpretable. A model: person (flag) at either layer, chance at both, else in between. UNVERIFIED.

| model | label | layer | dims | (i) picker, locker-after | (i) locker-first | (i) other sentences, after | (ii) asked, locker-after | (ii) locker-first | layer's label |
|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | chance | L6 | 36864 | 0.31 [0.24, 0.38] (n 166) | 0.25 [0.18, 0.32] (n 151) | 0.28 [0.23, 0.33] (n 422) | 0.50 [0.50, 0.50] (n 588, pos 166) | 0.50 [0.50, 0.50] (n 563) | chance |
| qwen3.5-9b | chance | L12 | 36864 | 0.41 [0.37, 0.46] (n 166) | 0.30 [0.23, 0.39] (n 151) | 0.29 [0.25, 0.33] (n 422) | 0.50 [0.50, 0.50] (n 588, pos 166) | 0.50 [0.50, 0.50] (n 563) | chance |
| muse-glimmer-30b | chance | L13 | 66560 | 0.27 [0.22, 0.32] (n 170) | 0.37 [0.29, 0.46] (n 143) | 0.27 [0.23, 0.31] (n 430) | 0.50 [0.49, 0.51] (n 600, pos 170) | 0.50 [0.50, 0.50] (n 531) | chance |
| muse-glimmer-30b | chance | L26 | 66560 | 0.34 [0.28, 0.41] (n 170) | 0.27 [0.20, 0.36] (n 143) | 0.29 [0.25, 0.34] (n 430) | 0.50 [0.50, 0.51] (n 600, pos 170) | 0.50 [0.50, 0.50] (n 531) | chance |

The E10 / E11 sentence per model:

- qwen3.5-9b: not readable from the locker sentence, even all its tokens together: the link is made elsewhere.
- muse-glimmer-30b: not readable from the locker sentence, even all its tokens together: the link is made elsewhere.

Keys (block order): qwen3.5-9b ['w:The', 'w:locker', 'w:of', 'w:the', 'item', 'w:is', 'w:space', 'number', 'w:.']; muse-glimmer-30b ['w:The', 'w:locker', 'w:of', 'w:the', 'item_pre', 'item', 'w:is', 'w:space', 'number', 'w:.']
