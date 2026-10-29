# 53.3b: the last-token conflict test on word answers

Batch 53, test 53.3b (jobs/c3/batch53.yaml test_53_3b; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). Zach's named-bridge passages (Z1-P's items: PP = the lookup copies a made-up word the passage states; PM = the recall, the same answer vocabulary); the change at the last token at each reader's own answer layer minus 1, 2, 3 and 51.10's read peak. UNVERIFIED.

Rule per reader and layer (53.3's): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between"; 53.3's validity bar (S_whole >= 0.3, >= 30 switches) applied.

Rule across readers: "copy bypasses the lens" if at answer - 1 and - 2 the recall is "through the lens" and the lookup "outside" on >= 3 of 4 models; "digits only" if on words the lookup goes through the lens like the recall; else in between.

As computed: 53.3's (the loss beyond random = (S_no_rand - S_no_jpp) / S_whole; the rest alone = S_no_jpp / S_whole, the same vector); a cell under 53.3's validity bar is "invalid" and counts for neither clause; per model a clause holds when it holds at both answer - 1 and - 2 with all four cells valid; "digits only" read as the lookup and the recall both "through the lens" at both layers, on >= 3 of 4 models, as the first clause; the answer layer = the plain logit lens at O's last token (51.10's settle rule: the layer from which O's answer token stays top through the last layer, the lower median over the passages); a layer without a J++ map is dropped and named.

**Across readers: pending (1 of 4 models)** (copy bypasses on 0 of 1 models run, digits only on 1).

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | lookup | 30 (answer L31 - 1) | 112 (86) | 0.79 [0.71, 0.86] | 0.08 [0.04, 0.13] | 0.51 [0.42, 0.60] | 0.59 [0.50, 0.68] | 0.55 [0.44, 0.64] | 0.10 [0.05, 0.17] | **through the lens** | yes |
| qwen3.5-9b | lookup | 29 (answer L31 - 2) | 112 (86) | 0.53 [0.43, 0.62] | 0.18 [0.11, 0.25] | 0.38 [0.29, 0.46] | 0.14 [0.08, 0.21] | 0.37 [0.23, 0.53] | 0.34 [0.22, 0.46] | **through the lens** | yes |
| qwen3.5-9b | lookup | 28 (answer L31 - 3) | 112 (86) | 0.44 [0.35, 0.53] | 0.16 [0.09, 0.23] | 0.23 [0.15, 0.31] | 0.12 [0.06, 0.19] | 0.16 [0.05, 0.29] | 0.37 [0.23, 0.51] | **in between** | yes |
| qwen3.5-9b | lookup | 24 (read peak) | 112 (86) | 0.34 [0.25, 0.43] | 0.21 [0.13, 0.28] | 0.21 [0.14, 0.29] | 0.04 [0.01, 0.08] | 0.03 [-0.06, 0.12] | 0.61 [0.44, 0.77] | **in between** | yes |
| qwen3.5-9b | recall | 30 (answer L31 - 1) | 112 (86) | 0.96 [0.93, 0.99] | 0.03 [0.00, 0.06] | 0.65 [0.56, 0.75] | 0.83 [0.75, 0.90] | 0.65 [0.55, 0.75] | 0.03 [0.00, 0.06] | **through the lens** | yes |
| qwen3.5-9b | recall | 29 (answer L31 - 2) | 112 (86) | 0.72 [0.63, 0.81] | 0.07 [0.03, 0.13] | 0.43 [0.32, 0.53] | 0.09 [0.04, 0.14] | 0.49 [0.37, 0.62] | 0.10 [0.04, 0.17] | **through the lens** | yes |
| qwen3.5-9b | recall | 28 (answer L31 - 3) | 112 (86) | 0.32 [0.23, 0.42] | 0.01 [0.00, 0.03] | 0.16 [0.09, 0.24] | 0.04 [0.01, 0.07] | 0.47 [0.29, 0.65] | 0.03 [0.00, 0.09] | **through the lens** | yes |
| qwen3.5-9b | recall | 24 (read peak) | 112 (86) | 0.18 [0.10, 0.26] | 0.02 [0.00, 0.05] | 0.12 [0.06, 0.20] | 0.01 [0.00, 0.03] | 0.60 [0.35, 0.83] | 0.10 [0.00, 0.24] | **invalid (through the lens)** | no |

Per model (answer - 1 and - 2): qwen3.5-9b: copy bypasses no, digits only yes {"lookup answer-1": "through", "lookup answer-2": "through", "recall answer-1": "through", "recall answer-2": "through"}.

- qwen3.5-9b (qwen35_9b_x53_3b): answer layer (never settled, layers without a lens map) {'lookup': (31, 0, []), 'recall': (31, 0, [])}

## The check: 53.3's lookup on the locker scenes at its own answer layer minus 1 and minus 3

| model | reader | layer (why) | n | whole | without the lens part | without a random part | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-9b | lookup | 28 (answer L29 - 1) | 75 | 0.84 [0.77, 0.91] | 0.15 [0.07, 0.23] | 0.31 [0.19, 0.42] | 0.19 [0.11, 0.26] | 0.17 [0.08, 0.26] | **in between** | yes |
| qwen3.5-9b | lookup | 26 (answer L29 - 3) | 75 | 0.73 [0.63, 0.84] | 0.27 [0.16, 0.38] | 0.31 [0.18, 0.45] | 0.05 [-0.02, 0.13] | 0.36 [0.23, 0.50] | **in between** | yes |

Figure: x53_lastconflict_words.png
