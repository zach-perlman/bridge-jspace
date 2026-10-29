# 53.3b: the last-token conflict test on word answers

Batch 53, test 53.3b (jobs/c3/batch53.yaml test_53_3b; no prediction (batch 53: every rule fixed in Dan's brief, 29 Oct 09:30, before any run)). Zach's named-bridge passages (Z1-P's items: PP = the lookup copies a made-up word the passage states; PM = the recall, the same answer vocabulary); the change at the last token at each reader's own answer layer minus 1, 2, 3 and 51.10's read peak. UNVERIFIED.

Rule per reader and layer (53.3's): per reader and layer: "computes outside the lens at the last token" if the loss without the lens part is <= 0.10 beyond random and the rest alone switches >= 0.7 of the whole; "through the lens" if the loss is >= 0.30 beyond random; else "in between"; 53.3's validity bar (S_whole >= 0.3, >= 30 switches) applied.

Rule across readers: "copy bypasses the lens" if at answer - 1 and - 2 the recall is "through the lens" and the lookup "outside" on >= 3 of 4 models; "digits only" if on words the lookup goes through the lens like the recall; else in between.

As computed: 53.3's (the loss beyond random = (S_no_rand - S_no_jpp) / S_whole; the rest alone = S_no_jpp / S_whole, the same vector); a cell under 53.3's validity bar is "invalid" and counts for neither clause; per model a clause holds when it holds at both answer - 1 and - 2 with all four cells valid; "digits only" read as the lookup and the recall both "through the lens" at both layers, on >= 3 of 4 models, as the first clause; the answer layer = the plain logit lens at O's last token (51.10's settle rule: the layer from which O's answer token stays top through the last layer, the lower median over the passages); a layer without a J++ map is dropped and named.

**Across readers: pending (1 of 4 models)** (copy bypasses on 0 of 1 models run, digits only on 0).

| model | reader | layer (why) | n (entities) | whole | without the lens part | without a random part | the lens part alone | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|---|
| muse-glimmer-30b ○ | lookup | 48 (answer L49 - 1) | 120 (85) | 0.96 [0.92, 0.99] | 0.07 [0.03, 0.13] | 0.83 [0.76, 0.90] | 0.69 [0.60, 0.78] | 0.79 [0.71, 0.87] | 0.08 [0.03, 0.13] | **through the lens** | yes |
| muse-glimmer-30b ○ | lookup | 47 (answer L49 - 2) | 120 (85) | 0.97 [0.93, 0.99] | 0.17 [0.10, 0.24] | 0.80 [0.72, 0.87] | 0.48 [0.40, 0.57] | 0.66 [0.56, 0.74] | 0.17 [0.11, 0.25] | **through the lens** | yes |
| muse-glimmer-30b ○ | lookup | 46 (answer L49 - 3) | 120 (85) | 0.97 [0.93, 0.99] | 0.22 [0.15, 0.29] | 0.86 [0.79, 0.92] | 0.33 [0.25, 0.42] | 0.66 [0.58, 0.75] | 0.22 [0.15, 0.30] | **through the lens** | yes |
| muse-glimmer-30b ○ | lookup | 32 (read peak) | 120 (85) | 0.27 [0.19, 0.34] | 0.24 [0.17, 0.32] | 0.23 [0.15, 0.30] | 0.01 [0.00, 0.03] | -0.06 [-0.16, 0.00] | 0.91 [0.79, 1.00] | **invalid (computes outside the lens at the last token)** | no |
| muse-glimmer-30b ○ | recall | 48 (answer L49 - 1) | 120 (85) | 0.95 [0.91, 0.98] | 0.00 [0.00, 0.00] | 0.71 [0.62, 0.79] | 0.76 [0.68, 0.83] | 0.75 [0.66, 0.83] | 0.00 [0.00, 0.00] | **through the lens** | yes |
| muse-glimmer-30b ○ | recall | 47 (answer L49 - 2) | 120 (85) | 0.95 [0.91, 0.98] | 0.02 [0.00, 0.04] | 0.65 [0.56, 0.74] | 0.59 [0.51, 0.68] | 0.67 [0.57, 0.76] | 0.02 [0.00, 0.05] | **through the lens** | yes |
| muse-glimmer-30b ○ | recall | 46 (answer L49 - 3) | 120 (85) | 0.95 [0.91, 0.98] | 0.02 [0.00, 0.04] | 0.68 [0.59, 0.76] | 0.57 [0.48, 0.66] | 0.69 [0.60, 0.78] | 0.02 [0.00, 0.04] | **through the lens** | yes |
| muse-glimmer-30b ○ | recall | 40 (read peak) | 120 (85) | 0.90 [0.84, 0.95] | 0.01 [0.00, 0.03] | 0.71 [0.63, 0.79] | 0.40 [0.31, 0.50] | 0.78 [0.70, 0.86] | 0.01 [0.00, 0.03] | **through the lens** | yes |

Per model (answer - 1 and - 2): muse-glimmer-30b: copy bypasses no, digits only yes {"lookup answer-1": "through", "lookup answer-2": "through", "recall answer-1": "through", "recall answer-2": "through"}.

○ muse-glimmer-30b: below gate (exploratory): Z1-P's gate on muse-glimmer-30b fails ({'K': 0.78125, 'M': 0.8584558823529411} < 0.80); its eligible passages only; hollow, rules verbatim, no prediction
- muse-glimmer-30b (muse30_x53_3b): answer layer (never settled, layers without a lens map) {'lookup': (49, 2, []), 'recall': (49, 0, [])}

## The check: 53.3's lookup on the locker scenes at its own answer layer minus 1 and minus 3

| model | reader | layer (why) | n | whole | without the lens part | without a random part | loss beyond random | rest / whole | label | valid |
|---|---|---|---|---|---|---|---|---|---|---|
| muse-glimmer-30b | lookup | 34 (answer L35 - 1) | 68 | 0.96 [0.90, 1.00] | 0.94 [0.88, 0.99] | 0.93 [0.87, 0.98] | -0.02 [-0.05, 0.00] | 0.98 [0.95, 1.00] | **computes outside the lens at the last token** | yes |
| muse-glimmer-30b | lookup | 32 (read peak) | 68 | 0.88 [0.82, 0.95] | 0.88 [0.82, 0.95] | 0.88 [0.82, 0.95] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | **computes outside the lens at the last token** | yes |

Figure: x53_lastconflict_words.png
