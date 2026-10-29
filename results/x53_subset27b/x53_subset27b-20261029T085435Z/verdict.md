# 53.5: the 27B on its position-route scenes

Batch 53, test 53.5 (jobs/c3/batch53.yaml, Dan 29 Oct 09:30; written 20261029T085435Z). CPU only, existing outcomes. No prediction. UNVERIFIED.

Rule (fixed in advance, verbatim):

> Keep the scenes where the 27B's lookup goes by position under the whole change; recompute on them: position without the address vs random, the address alone, the swap at s = 2. Rule: "same mechanism, used less" if the address alone brings >= 0.25 of position answers back and its removal leaves <= 0.10 (the 9B's pattern); "the 27B differs" otherwise. Same subset on the 9B beside.

As computed:
- Subset: the routes test's C1 and C2 scenes (C0 has no position answer) where the lookup's answer under the whole change is the position route's digit (x6_routes' label "position"), from the keep-only run, which has every arm below on the same forward pass per scene. Rule read on C1 + C2 pooled; each condition beside.
- back = position share with the address alone (keep_alf) / with the whole change (1 on the subset by construction); left = position share without the address (no_alf). The rule is applied verbatim to these raw shares (back >= 0.25, left <= 0.1); the differences from the random parts are beside, not in the rule.
- The swap at s = 2: x8_write's writes h + s (mu_k - mu_j) at the bridge word of the original prompt, both k != j, on the routes test's C2 items (same generator, seed and eligibility; scene ids and bridge items match all 300); the share the lookup follows (target). x8_write has no random write at s = 2; the random write at s = 4 (twice the norm) is beside. The swap has no clause in the rule.
- Cluster bootstrap over the bridge items (10000 resamples, seed 0), paired across arms.

## Result

**27B: the 27B differs.** back = 0.22 [0.15, 0.29], left = 0.08 [0.04, 0.11].
9B beside (same subset logic on its own position-route scenes): the pattern holds; back = 0.46 [0.39, 0.53], left = 0.06 [0.04, 0.09].

Position share on the subset (lookup), per arm:

| model | scenes | n (C1 + C2) | whole | without the address | without a random part | random minus without the address | the address alone | a random part alone | alone minus random |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | C1 + C2 | 232 (31 items) | 1.00 [1.00, 1.00] | 0.08 [0.04, 0.11] | 0.37 [0.30, 0.42] | 0.29 [0.24, 0.33] | 0.22 [0.15, 0.29] | 0.01 [0.00, 0.03] | 0.21 [0.15, 0.27] |
| Qwen3.6-27B | C1 | 131 (31 items) | 1.00 [1.00, 1.00] | 0.02 [0.00, 0.04] | 0.07 [0.03, 0.11] | 0.05 [0.02, 0.09] | 0.28 [0.20, 0.36] | 0.01 [0.00, 0.02] | 0.27 [0.20, 0.35] |
| Qwen3.6-27B | C2 | 101 (29 items) | 1.00 [1.00, 1.00] | 0.16 [0.09, 0.22] | 0.75 [0.64, 0.84] | 0.59 [0.49, 0.68] | 0.14 [0.07, 0.21] | 0.01 [0.00, 0.03] | 0.13 [0.07, 0.19] |
| Qwen3.5-9B | C1 + C2 | 340 (31 items) | 1.00 [1.00, 1.00] | 0.06 [0.04, 0.09] | 0.45 [0.41, 0.50] | 0.39 [0.34, 0.43] | 0.46 [0.39, 0.53] | 0.02 [0.01, 0.04] | 0.44 [0.36, 0.51] |
| Qwen3.5-9B | C1 | 187 (31 items) | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 0.04 [0.02, 0.08] | 0.04 [0.02, 0.08] | 0.60 [0.53, 0.66] | 0.04 [0.02, 0.07] | 0.56 [0.49, 0.62] |
| Qwen3.5-9B | C2 | 153 (29 items) | 1.00 [1.00, 1.00] | 0.14 [0.09, 0.20] | 0.95 [0.90, 0.98] | 0.80 [0.74, 0.86] | 0.29 [0.21, 0.39] | 0.00 [0.00, 0.00] | 0.29 [0.21, 0.39] |

Per condition, the rule's two inputs: Qwen3.6-27B C1 back 0.28 [0.20, 0.36], left 0.02 [0.00, 0.04] (pattern holds); Qwen3.6-27B C2 back 0.14 [0.07, 0.21], left 0.16 [0.09, 0.22] (pattern does not hold); Qwen3.5-9B C1 back 0.60 [0.53, 0.66], left 0.00 [0.00, 0.00] (pattern holds); Qwen3.5-9B C2 back 0.29 [0.21, 0.39], left 0.14 [0.09, 0.20] (pattern does not hold).

Read beside the label (descriptive, not in the rule): the 27B's back CI [0.15, 0.29] contains the bar 0.25. Without a random part of the address's share, C1 keeps 0.07 [0.03, 0.11] (Qwen3.6-27B), 0.04 [0.02, 0.08] (Qwen3.5-9B) of its position answers, so in C1 the removal clause does not separate the address from a random part of its share; in C2 the removal beyond random is 0.59 [0.49, 0.68] (Qwen3.6-27B), 0.80 [0.74, 0.86] (Qwen3.5-9B).

The swap at s = 2 (C2 scenes; lookup's share per write; 2 writes per scene):

| model | scenes | writes | follows the swap (target) | stays (original) | third | random write at s = 4: target |
|---|---|---|---|---|---|---|
| Qwen3.6-27B | position-route subset (n 101; bridge slot j: 0: 12, 1: 43, 2: 46) | 202 | 0.23 [0.18, 0.29] | 0.71 [0.65, 0.78] | 0.05 [0.03, 0.09] | 0.00 [0.00, 0.02] |
| Qwen3.6-27B | the other C2 scenes (n 199; bridge slot j: 0: 77, 1: 68, 2: 54) | 398 | 0.25 [0.19, 0.31] | 0.71 [0.64, 0.78] | 0.04 [0.03, 0.06] | 0.01 [0.00, 0.01] |
| Qwen3.6-27B | all C2 (n 300; bridge slot j: 0: 89, 1: 111, 2: 100) | 600 | 0.24 [0.20, 0.29] | 0.71 [0.66, 0.76] | 0.05 [0.03, 0.06] | 0.01 [0.00, 0.01] |
| Qwen3.5-9B | position-route subset (n 153; bridge slot j: 0: 20, 1: 58, 2: 75) | 306 | 0.40 [0.36, 0.43] | 0.57 [0.52, 0.61] | 0.03 [0.01, 0.04] | 0.00 [0.00, 0.00] |
| Qwen3.5-9B | the other C2 scenes (n 147; bridge slot j: 0: 73, 1: 50, 2: 24) | 294 | 0.52 [0.46, 0.58] | 0.35 [0.28, 0.42] | 0.10 [0.06, 0.13] | 0.00 [0.00, 0.00] |
| Qwen3.5-9B | all C2 (n 300; bridge slot j: 0: 93, 1: 108, 2: 99) | 600 | 0.46 [0.42, 0.50] | 0.46 [0.42, 0.50] | 0.06 [0.04, 0.08] | 0.00 [0.00, 0.00] |

Checks:
- Qwen3.6-27B: the routes run x6_routes_27b (its own forward pass on the same scenes) puts 230 of the 232 subset scenes on the position route (233 position scenes there in all); its position share without the address on the subset: 0.08.
- Qwen3.5-9B: the routes run qwen35_9b_x6_routes (its own forward pass on the same scenes) puts 340 of the 340 subset scenes on the position route (340 position scenes there in all); its position share without the address on the subset: 0.06.
- Descriptive: the 27B's subset scenes read on the 9B (same scene id and bridge item; n 206): whole 0.89 [0.85, 0.93], without the address 0.07 [0.03, 0.11], the address alone 0.54 [0.45, 0.62].

Figure: x53_subset27b.png. Status: UNVERIFIED (exploration day; nothing into the README).
