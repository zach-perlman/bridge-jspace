# Lens check: every model's lens scored the same way (scripts/lens_fit/lens_check.py)

Held-out macro pass@10 (jpp_lens's readout evals, items the model answers right). J++ / logit lens / J++ minus logit.

| model | items | every fitted layer | 7 layers at 1/8-7/8 depth | C1 rule band |
|---|---|---|---|---|
| Qwen3.6-27B (published J++) | 329 | 0.717 / 0.436 / +0.282 | 0.595 / 0.340 / +0.255 | 0.503 / 0.199 / +0.304 |
| Gemma 4 31B-it (our J++, 64 prompts) | 244 | 0.633 / 0.560 / +0.073 | 0.523 / 0.329 / +0.194 | 0.367 / 0.019 / +0.349 |
| Qwen3-32B (our J++, 32 prompts) | 301 | 0.638 / 0.351 / +0.287 | 0.474 / 0.201 / +0.272 | 0.360 / 0.054 / +0.306 |
| Qwen3.5-9B (published J++) | 309 | 0.630 / 0.391 / +0.240 | 0.590 / 0.326 / +0.263 | 0.413 / 0.093 / +0.320 |

Relative-depth layers: {"Qwen3.6-27B (published J++)": [8, 16, 24, 32, 40, 48, 56], "Gemma 4 31B-it (our J++, 64 prompts)": [8, 15, 23, 30, 38, 45, 53], "Qwen3-32B (our J++, 32 prompts)": [8, 16, 24, 32, 40, 48, 56], "Qwen3.5-9B (published J++)": [4, 8, 12, 16, 20, 24, 28]}
