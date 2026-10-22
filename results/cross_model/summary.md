# Cross-model replication summary (unverified; one data seed; written by scripts/cross_model_summary.py)

## C1: memory steps need the J-space, prompt lookups don't (knock-out at each model's held-out-chosen band)

| model | lens | band | loss P→P / M→P / C→P | loss P→M / M→M / C→M | gap (≥30) | controls | C1-graded | no-guess gap | unembedding gap | keep-own restored (kill ≥75%) | extra control seeds (min acc) | plain-text +nats top-10 / random |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen3.6-27B | published J++ | L32-40 | 0 / 13 / 6 | 41 / 45 / 41 | 36 | ok | **HOLDS** | 34 | 0 | 20% | 96, 97 | +0.30 / +0.07 |
| Qwen3-32B | our J++ (32 prompts) | - | - | - | - | - | - | - | - | - | - | - |
| Muse Glimmer 30B | our J++ (32 prompts) | - | - | - | - | - | - | - | - | - | - | +0.27 / +0.03 |
| Qwen3.5-9B | published J++ | - | - | - | - | - | - | - | - | - | - | - |
| Gemma 4 31B-it | our J++ (64 prompts) | L48-56 | 93 / 93 / 91 | 90 / 93 / 86 | -1 | ok | **n/a (untestable)** | -1 | 0 | - | - | +9.25 / +0.01 UNTESTABLE |

## C2: the lens writes bridges (two-step steering at the question / final positions)

| model | band | C2-graded (M→M best vs M→P best) | C2-relative | C2' (narrow): P→P vs P→M; C→P vs C→M (cross-validated writes) |
|---|---|---|---|---|
| Qwen3.6-27B | current | FAILS (40 vs 36) | inconclusive: sites carry the bridge only partly | **HOLDS**: P 1→18; C 0→17 |

The 27B's C2' is the data the rule was read off (not evidence); the other models are the test.
