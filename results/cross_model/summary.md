# Cross-model replication summary (unverified; one data seed; written by scripts/cross_model_summary.py)

## C1: memory steps need the J-space, prompt lookups don't (knock-out at each model's held-out-chosen band)

| model | lens | band | loss P→P / M→P / C→P | loss P→M / M→M / C→M | gap (≥30) | controls | C1-graded | no-guess gap | unembedding gap | keep-own restored (kill ≥75%) | extra control seeds (min acc) | plain-text +nats top-10 / random |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | published J++ | L32-40 | 0 / 13 / 6 | 41 / 45 / 41 | 36 | ok | **HOLDS** | 34 | 0 | 20% | 96, 97 | +0.30 / +0.07 |
| Qwen3-32B | our J++ (32 prompts) | L44-52 | 1 / 0 / 7 | 23 / 21 / 29 | 22 | NO | **FAILS** | 20 | 4 | -10% | 85, 86 | +0.13 / +0.02 |
| Muse Glimmer 30B | our J++ (32 prompts) | L36-42 | 0 / 0 / 0 | 11 / 3 / 8 | 7 | ok | **FAILS** | 7 | 7 | - | - | +0.27 / +0.03 |
| Qwen3.5-9B | published J++ | L12-16 | 3 / 7 / 1 | 37 / 49 / 36 | 38 | ok | **HOLDS** | 40 | - | - | - | - |
| Gemma 4 31B-it | our J++ (64 prompts) | L48-56 | 93 / 93 / 91 | 90 / 93 / 86 | -1 | ok | **n/a (untestable)** | -1 | 0 | - | - | +9.25 / +0.01 UNTESTABLE |

## C2: the lens writes bridges (two-step steering at the question / final positions)

| model | band | C2-graded (M→M best vs M→P best) | C2-relative | C2' (narrow): P→P vs P→M; C→P vs C→M (cross-validated writes) |
|---|---|---|---|---|
| Qwen3.6-27B | current | FAILS (40 vs 36) | inconclusive: sites carry the bridge only partly | **HOLDS**: P 1→18; C 0→17 |
| Qwen3.6-27B | aligned | FAILS (19 vs 0) | FAILS | **HOLDS**: P 0→11; C 0→18 |
| Qwen3-32B | current | FAILS (10 vs 12) | inconclusive: sites carry the bridge only partly | **FAILS**: P 5→16; C 0→2 |
| Qwen3-32B | aligned | HOLDS (75 vs 8) | HOLDS | **HOLDS**: P 0→23; C 0→29 |
| Muse Glimmer 30B | current | HOLDS (56 vs 6) | HOLDS | **FAILS**: P 11→14; C 3→17 |
| Muse Glimmer 30B | aligned | HOLDS (50 vs 10) | HOLDS | **FAILS**: P 13→8; C 5→17 |

The 27B's C2' is the data the rule was read off (not evidence); the other models are the test.
