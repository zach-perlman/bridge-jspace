# statement_positions / d1_map_n80_v1: analysis

EXP statement_positions/d1_map_n80_v1 @ 3b8db6e (dirty tree) | model Qwen/Qwen3.6-27B | n=80 per family (prompt → prompt; prompt → memory; memory → prompt; memory → memory; prompt → prompt → memory; prompt → memory → prompt; countries: memory → memory; countries: prompt → memory) | seeds=[0]
Claim tested: Where in the prompt (which positions) and up to which layer does a patch from the alt prompt change the answer to answer alt?

Headline (prompt → prompt): % of original answers that become the alternative answer (answer org → answer alt) after a patch from the alt prompt at the whole context, layer 36 = 86% [77%, 92%]   Baseline (the same patch at the question and all after it): 6% [3%, 14%]   Control (random push, same size): 0% [0%, 5%]

Transit cells (rule: % of original answers that become the alternative answer (answer org → answer alt) >= 50%, Wilson lower bound above every control): {"prompt → prompt": {"the whole context": [32, 34, 36, 38, 40, 44], "question and all after it": [52], "last tokens before the answer": [52]}, "prompt → memory": {"sentence stating bridge org": [32, 34, 36, 38], "the bridge org word": [32, 34, 36, 38], "the whole context": [32, 34, 36, 38]}, "memory → prompt": {"question and all after it": [36, 38, 40, 44, 48, 52], "last tokens before the answer": [48, 52]}, "prompt → prompt → memory": {"the whole context": [32, 34, 38]}, "prompt → memory → prompt": {"the whole context": [32, 34]}, "countries: memory → memory": {"question and all after it": [36, 38, 40, 44, 48, 52], "last tokens before the answer": [48, 52]}, "countries: prompt → memory": {"sentence stating bridge org": [32, 34, 36, 38], "the bridge org word": [32, 34, 36, 38], "the whole context": [32, 34, 36, 38], "question and all after it": [40, 44, 48, 52], "last tokens before the answer": [48, 52]}}
Handoff: {"prompt → prompt": {"last_statement_transit": {"the whole context": 44}, "first_question_transit": 52}, "prompt → memory": {"last_statement_transit": {"sentence stating bridge org": 38, "the bridge org word": 38, "the whole context": 38}, "first_question_transit": null}, "memory → prompt": {"last_statement_transit": {}, "first_question_transit": 36}, "prompt → prompt → memory": {"last_statement_transit": {"the whole context": 38}, "first_question_transit": null}, "prompt → memory → prompt": {"last_statement_transit": {"the whole context": 34}, "first_question_transit": null}, "countries: memory → memory": {"last_statement_transit": {}, "first_question_transit": 36}, "countries: prompt → memory": {"last_statement_transit": {"sentence stating bridge org": 38, "the bridge org word": 38, "the whole context": 38}, "first_question_transit": 40}}

Against the first map: {"both": 54, "only_old": 4, "only_new": 5, "neither": 353}; disagreements: {"only_old": ["countries: prompt → memory: sentence stating bridge org, layer 40: 56% -> 45%", "countries: prompt → memory: sentence stating bridge org, layer 44: 53% -> 40%", "countries: prompt → memory: the bridge org word, layer 40: 56% -> 45%", "countries: prompt → memory: the bridge org word, layer 44: 53% -> 42%"], "only_new": ["prompt → memory: sentence stating bridge org, layer 36: 34% -> 50%", "prompt → memory: sentence stating bridge org, layer 38: 38% -> 50%", "prompt → memory: the bridge org word, layer 36: 38% -> 50%", "prompt → memory: the bridge org word, layer 38: 38% -> 50%", "prompt → prompt → memory: the whole context, layer 38: 44% -> 50%"]}

Figures: results/statement_positions/d1_map_n80_v1/analysis-20261021-133151-figures/heatmap_copy_flips.png, results/statement_positions/d1_map_n80_v1/analysis-20261021-133151-figures/copy_flips_by_layer.png, results/statement_positions/d1_map_n80_v1/analysis-20261021-133151-figures/map_confirmation.png

Gates:
- identity (the org prompt's own states patched back in) keeps the org prompt's top token: 100% of 1280; logit-margin difference from an unedited read in the same batch: max 0.0
- the alt prompt's states patched at every position at the first map layer give the alt prompt's top token: 100% of 640 (logit-margin difference max 2.0, bf16 batch rounding)
- memory-bridge families (alt prompt differs only in the question): patches at the statements are exactly zero (causality violations: 0); 640 of them read anyway: difference from the identity max 0.0
- read vs greedy agreement: 99.93% of 13000 edited runs (rule: >= 99%)

Recomputed from the saved outputs == the run's summary.json: {"transit": true, "handoff": true, "sanity": true, "validation": true}

Status: UNVERIFIED
