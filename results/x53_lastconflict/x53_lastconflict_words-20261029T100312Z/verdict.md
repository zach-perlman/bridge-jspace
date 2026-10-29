# 53.3b: the last-token conflict test on word answers

Batch 53, test 53.3b (jobs/c3/batch53.yaml test_53_3b; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). Zach's named-bridge passages (Z1-P's items: PP = the lookup copies a made-up word the passage states; PM = the recall, the same answer vocabulary); the change at the last token at each reader's own answer layer minus 1, 2, 3 and 51.10's read peak. UNVERIFIED.

Rule per reader and layer (53.3's): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between"; 53.3's validity bar (S_whole >= 0.3, >= 30 switches) applied.

Rule across readers: "copy bypasses the lens" if at answer - 1 and - 2 the recall is "through the lens" and the lookup "outside" on >= 3 of 4 models; "digits only" if on words the lookup goes through the lens like the recall; else in between.

As computed: 53.3's (the loss beyond random = (S_no_rand - S_no_jpp) / S_whole; the rest alone = S_no_jpp / S_whole, the same vector); a cell under 53.3's validity bar is "invalid" and counts for neither clause; per model a clause holds when it holds at both answer - 1 and - 2 with all four cells valid; "digits only" read as the lookup and the recall both "through the lens" at both layers, on >= 3 of 4 models, as the first clause; the answer layer = the plain logit lens at O's last token (51.10's settle rule: the layer from which O's answer token stays top through the last layer, the lower median over the passages); a layer without a J++ map is dropped and named.

**Across readers: pending (1 of 4 models)** (copy bypasses on 0 of 1 models run, digits only on 1).

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.6-27b | lookup | 62 (answer L63 - 1) | 200 (118) | 0.99 [0.98, 1.00] | 0.04 [0.01, 0.06] | 0.92 [0.88, 0.95] | 0.78 [0.72, 0.83] | 0.88 [0.84, 0.92] | 0.04 [0.01, 0.06] | **through the lens** | yes |
| qwen3.6-27b | lookup | 61 (answer L63 - 2) | 200 (118) | 0.98 [0.97, 1.00] | 0.21 [0.16, 0.27] | 0.94 [0.91, 0.97] | 0.25 [0.20, 0.31] | 0.74 [0.68, 0.80] | 0.22 [0.16, 0.27] | **through the lens** | yes |
| qwen3.6-27b | lookup | 60 (read peak) | 200 (118) | 0.97 [0.95, 0.99] | 0.26 [0.20, 0.32] | 0.83 [0.78, 0.88] | 0.04 [0.01, 0.07] | 0.58 [0.51, 0.65] | 0.27 [0.21, 0.33] | **through the lens** | yes |
| qwen3.6-27b | recall | 62 (answer L63 - 1) | 200 (118) | 0.99 [0.98, 1.00] | 0.00 [0.00, 0.00] | 0.96 [0.93, 0.98] | 0.89 [0.83, 0.93] | 0.96 [0.94, 0.99] | 0.00 [0.00, 0.00] | **through the lens** | yes |
| qwen3.6-27b | recall | 61 (answer L63 - 2) | 200 (118) | 0.98 [0.97, 1.00] | 0.02 [0.00, 0.04] | 0.89 [0.85, 0.93] | 0.48 [0.41, 0.56] | 0.88 [0.84, 0.93] | 0.02 [0.00, 0.04] | **through the lens** | yes |
| qwen3.6-27b | recall | 60 (answer L63 - 3) | 200 (118) | 0.94 [0.90, 0.97] | 0.01 [0.00, 0.02] | 0.60 [0.53, 0.67] | 0.34 [0.27, 0.41] | 0.64 [0.56, 0.71] | 0.01 [0.00, 0.02] | **through the lens** | yes |
| qwen3.6-27b | recall | 56 (read peak) | 200 (118) | 0.90 [0.86, 0.94] | 0.04 [0.01, 0.07] | 0.60 [0.53, 0.67] | 0.14 [0.09, 0.18] | 0.62 [0.54, 0.70] | 0.04 [0.02, 0.08] | **through the lens** | yes |

Per model (answer - 1 and - 2): qwen3.6-27b: copy bypasses no, digits only yes {"lookup answer-1": "through", "lookup answer-2": "through", "recall answer-1": "through", "recall answer-2": "through"}.

- qwen3.6-27b (x53_3b_27b): answer layer (never settled, layers without a lens map) {'lookup': (63, 0, []), 'recall': (63, 0, [])}

## The check: 53.3's lookup on the locker scenes at its own answer layer minus 1 and minus 3

| model | reader | layer (why) | n | whole | without the lens part | without a random part | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.6-27b | lookup | 60 (read peak) | 69 | 0.45 [0.35, 0.55] | 0.09 [0.03, 0.15] | 0.14 [0.08, 0.21] | 0.13 [0.03, 0.25] | 0.19 [0.07, 0.33] | **in between** | yes |
| qwen3.6-27b | lookup | 58 (answer L61 - 3) | 69 | 0.29 [0.21, 0.37] | 0.26 [0.17, 0.35] | 0.20 [0.12, 0.29] | -0.20 [-0.36, -0.05] | 0.90 [0.74, 1.00] | **computes outside the lens at the last token** | no |

Figure: x53_lastconflict_words.png
