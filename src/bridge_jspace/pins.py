"""Pinned external inputs and repo paths. Changing any pin needs a new manifest.

The QWEN_*/LENS_* constants are the Qwen3.6-27B + J-lens pins used by scripts/exp01-02 (part B);
configs/models/qwen3.6-27b.yaml repeats them for the YAML-configured experiments (part A), and
tests/test_pins.py checks the two agree.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
RESULTS_DIR = REPO_ROOT / "results"
FIGURES_DIR = REPO_ROOT / "figures"
CACHE_DIR = REPO_ROOT / "cache"

QWEN_REPO = "Qwen/Qwen3.6-27B"
QWEN_REVISION = "6a9e13bd6fc8f0983b9b99948120bc37f49c13e9"

LENS_REPO = "neuronpedia/jacobian-lens"
# 9fa267f841d62aa468dab5b9b38c3dc45a82d863 until 2026-10-20: a history rewrite of neuronpedia/jacobian-lens removed it
# (404 from a fresh machine). e166deb serves the byte-identical files: LFS sha256 of the J++ file bbef480b... =
# FROZEN_LENS_SHA256 and of the oracle adapter 7d4b301e... = ORACLE_ADAPTER_SHA256 (checked on load, as before).
LENS_REVISION = "e166deb5ad540932100ef803c8c9bcc2a5453694"
LENS_FILE = "qwen3.6-27b/jlens/Salesforce-wikitext/Qwen3.6-27B_jacobian_lens_n1000.pt"
JPP_FILE = "qwen3.6-27b/jpp/Salesforce-wikitext/Qwen3.6-27B_jpp_lens.pt"  # same repo, revision and format
LENS_FILES = {"jlens": LENS_FILE, "jpp": JPP_FILE}  # part B's lens choice (exp01 variant, exp02 from its probes)
# workspace-lenses: the paper's recipe (n=25 pile-10k prompts, target layer 62 = n_layers - 2), a J-lens and its
# matched RelP pair (R-lens), plus the template lens (one direction per word or phrase per layer). Part B's exp05.
WS_LENS_REPO = "camilablank/workspace-lenses"
WS_LENS_REVISION = "d740106d1e0f95456dc8718fba2895e9c8ffd6ef"
TEMPLATE_LENS_FILE = "qwen3.6-27b/template-lens/templates.safetensors"
TEMPLATE_WORDS_FILE = "qwen3.6-27b/template-lens/template_words.txt"
# The lens is frozen (Zach, 2026-10-19; README Decisions): part B's runs use the published J++ (neuronpedia/jacobian-lens,
# JPP_FILE at LENS_REVISION), no further lens fitting or lens comparisons in headline runs. Its file's sha256 is checked
# on load (lens.py), so a changed upload cannot slip in under the same name. Another target names its own frozen lens
# ("frozen_lens" in TARGETS; default "jpp") and sha256 (see below the TARGETS table).
FROZEN_LENS = "jpp"
FROZEN_LENS_SHA256 = "bbef480b41028e156c4aa3c334ad32d1b76a4017ef3a7245eecf776bf2b58f8f"
LENS_SOURCES = {  # every J-format lens part B can load: name -> (repo, file, revision)
    "jlens": (LENS_REPO, LENS_FILE, LENS_REVISION),
    "jpp": (LENS_REPO, JPP_FILE, LENS_REVISION),
    "ws_jlens": (WS_LENS_REPO, "qwen3.6-27b/j-lens/lens.pt", WS_LENS_REVISION),
    "ws_rlens": (WS_LENS_REPO, "qwen3.6-27b/r-lens/lens.pt", WS_LENS_REVISION),
    # exp19's chat-fitted J++ (fit_v3 chat64: 64 UltraChat texts, the fit_v2 chat router, J++ recipe otherwise),
    # exported to this format by scripts/exp19_fit_data/export_lens.py (fp16, max rel. err 4.4e-4). Held-out macro
    # pass@10 .716 (published J++ .714). A "local" lens: (path under the repo, sha256).
    "jpp_chat64": (
        "local",
        "cache/exp19/lenses/Qwen3.6-27B_jpp_chat64.pt",
        "0b320ad5205a5c3a70dbdb8752a594dba76828e3ec02066c6786e5a98680d0dd",
    ),
}

# solarkyle/jspace-lenses: third-party plain J-lenses in the jlens library's format (J per source layer), 100
# WikiText-103 prompts each, bf16 fits (its README). The only lens for Mistral-Small-24B-Instruct-2501 (README: "validation
# in progress"); the 27B's and Gemma 4 31B-it's are bridges, the same third party's lens on models we already ran (Zach,
# 2026-10-21: verify C1 and C2 on a second family; Gemma: is its breakage the model or our fit?).
SOLAR_LENS_REPO = "solarkyle/jspace-lenses"
SOLAR_LENS_REVISION = "f5767d1bb4cb25ed65a8ed16eb47a6e6a1f0a0bc"
# Mistral's own chat template minus its default system prompt, which names Paris and France (answers in our tasks) and
# today's date (prompts would change daily): no system turn unless a message gives one, as the other targets' templates.
MISTRAL_CHAT_TEMPLATE = (
    "{{- bos_token }}"
    "{%- if messages[0]['role'] == 'system' %}{{- '[SYSTEM_PROMPT]' + messages[0]['content'] + '[/SYSTEM_PROMPT]' }}"
    "{%- set loop_messages = messages[1:] %}{%- else %}{%- set loop_messages = messages %}{%- endif %}"
    "{%- for message in loop_messages %}"
    "{%- if message['role'] == 'user' %}{{- '[INST]' + message['content'] + '[/INST]' }}"
    "{%- elif message['role'] == 'system' %}{{- '[SYSTEM_PROMPT]' + message['content'] + '[/SYSTEM_PROMPT]' }}"
    "{%- elif message['role'] == 'assistant' %}{{- message['content'] + eos_token }}"
    "{%- else %}{{- raise_exception('Only user, system and assistant roles are supported!') }}{%- endif %}"
    "{%- endfor %}"
)

# Muse Glimmer 30B's chat template, edited (applied to the tokenizer's own template, each edit checked to apply once): no
# "Current date" line (prompts would change daily); reasoning strength "low" instead of the default "high" (levels: low /
# medium / high / xhigh); the generation prompt opens the answer channel to the user directly ("<|start|>assistant
# to=user<|message|>"), so the prefill "Answer:" follows as for every target (Qwen: empty think block; Gemma: empty
# thought channel). Its default system line ("You are a helpful AI assistant." and the knowledge cutoff) is kept.
# gpt-oss-20b's harmony template (Zach, 2026-10-23): drop the current-date line (prompts must not change by day), set the
# default reasoning effort to low, and open the assistant turn on the final channel, so the model answers directly
# (no analysis channel), as the other models answer after their templates' generation prompts.
GPTOSS_TEMPLATE_EDITS = [
    ('    {{- "Current date: " + strftime_now("%Y-%m-%d") + "\\n\\n" }}\n', '    {{- "\\n" }}\n'),
    ('        {%- set reasoning_effort = "medium" %}', '        {%- set reasoning_effort = "low" %}'),
    ("{%- if add_generation_prompt -%}\n<|start|>assistant\n{%- endif -%}", "{%- if add_generation_prompt -%}\n<|start|>assistant<|channel|>final<|message|>\n{%- endif -%}"),
]
MUSE_TEMPLATE_EDITS = [
    (
        "    {%- if current_date is defined and current_date -%}\n"
        "        {{- '\\nCurrent date: ' + current_date + '.' -}}\n"
        "    {%- elif strftime_now is defined -%}\n"
        "        {{- '\\nCurrent date: ' + strftime_now('%Y-%m-%d') + '.' -}}\n"
        "    {%- endif -%}\n",
        "",
    ),
    ("reasoning_strength else 'high' -%}", "reasoning_strength else 'low' -%}"),
    ("{%- if add_generation_prompt -%}\n    {{- '<|start|>assistant' -}}", "{%- if add_generation_prompt -%}\n    {{- '<|start|>assistant to=user<|message|>' -}}"),
]

# Part B's target model. BJ_TARGET picks it; the default is Qwen3.6-27B, the model of every run before the Gemma port,
# whose pins, paths and lenses above stay as they are. Another target loads its own model and lenses, keeps its caches
# under cache/<target>/ and names its runs with its own prefix. A "local" lens is (path under the repo, sha256): a lens
# we fit ourselves, not on the Hub.
TARGETS: dict[str, dict[str, Any]] = {
    "qwen3.6-27b": {
        "repo": QWEN_REPO,
        "revision": QWEN_REVISION,
        "n_layers": 64,
        "norm_gain": "one_plus_weight",  # Qwen3.5-family RMSNorm scales by 1 + weight
        "bos": False,  # Qwen's tokenizer adds no BOS; raw text is tokenized as is
        "run_prefix": "",
        "lenses": LENS_SOURCES,
    },
    "gemma-4-31b-it": {
        "repo": "google/gemma-4-31B-it",
        "revision": "842da3794eaa0b77d5f08bae87a17459d91ff475",
        "n_layers": 60,
        "norm_gain": "weight",  # Gemma4RMSNorm scales by weight
        "bos": True,  # Gemma needs <bos> first; the chat template writes it, raw text gets it prepended
        "run_prefix": "gemma4it_",
        # Fit on this model with the published recipe (no published lens is fit on the instruction-tuned model): J++
        # with safety-research/jpp_lens@93f02cd as neuronpedia's fit-jpp-lens.sh (64 wikitext prompts, target layer 59),
        # converted with their convert-jpp-lens.py. Recall@10 (macro, their evals on this model): 0.62, vs 0.40 for
        # neuronpedia's base-model J-lens and 0.51 for the pooled lens; eval_ranks_pass_at_k.csv sits beside it. No
        # J-lens: the human chose J++ only for this target, so stages that compare lenses run with J++ alone.
        "lenses": {
            "jpp": (
                "local",
                "cache/gemma-4-31b-it/lenses/jpp/gemma-4-31B-it_jpp_lens.pt",
                "0b092e9371c3ce79c203e8f9a17ae10e956797d62a8fa0b29a46ab1311de0902",
            ),
        },
    },
    # Qwen3.5-9B (post-trained; same tokenizer file as Qwen3.6-27B, chat templates equal for one user turn): a
    # smaller-model comparison (Zach, 2026-10-19). Its published J++ (neuronpedia, converted from koayon/jpp-lenses,
    # 64 wikitext prompts, target layer 31) is its frozen lens, sha256-checked on load like the 27B's.
    "qwen3.5-9b": {
        "repo": "Qwen/Qwen3.5-9B",
        "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
        "n_layers": 32,
        "norm_gain": "one_plus_weight",
        "bos": False,
        "run_prefix": "qwen35_9b_",
        "lenses": {
            "jpp": (
                LENS_REPO,
                "qwen3.5-9b/jpp/Salesforce-wikitext/Qwen3.5-9B_jpp_lens.pt",
                "e166deb5ad540932100ef803c8c9bcc2a5453694",
            ),
        },
        "frozen_lens_sha256": "8cda12f7ddf11e70fcfc69a47a9574f626fe084c67807a4781f4f67106e739c5",
    },
    # Dan's "qwen3-32b" (neuronpedia's plain J-lens, sha256 0af5ccf2; D1 on a second model, 22 Oct) is main's
    # "qwen3-32b-jlens" below since the merge into main (27 Oct 2026); its old runs (qwen3_32b_) are in LEGACY_PREFIXES.
    # Qwen3-32B with OUR J++ (Dan, 23 Oct): every lens result on J++. Primary lens (Dan, 23 Oct ~00:30, fixed before any
    # J++ result): ours, the published recipe (safety-research/jpp_lens@93f02cd) on 64 WikiText prompts x 128 tokens (2
    # shards x 32 on 2x H200, one router, seed 0, merged; the merge checked exact on Qwen3.5-0.8B), skip 16, target = the
    # last block, rlens LRP, 8 experts, source layers 16-51 only; Zach's 32-prompt fit is reported alongside when shared;
    # no silent switch. Published: huggingface.co/danorel/Qwen3-32B-jpp-lens (commit 8d43d036, public), fp16 export.
    # lens_layers: the plain J-lens runs' grid (every 4th layer) inside the fit's 16-51, so the stages read the same cells.
    # Since the merge into main (27 Oct 2026) its local copy lives under cache/qwen3-32b-jpp/ (this target's cache
    # folder): main's qwen3-32b (Zach's 32-prompt J++, sha256 6fbc0386) keeps cache/qwen3-32b/lenses/jpp/. Same file.
    "qwen3-32b-jpp": {
        "repo": "Qwen/Qwen3-32B",
        "revision": "9216db5781bf21249d130ec9da846c4624c16137",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "qwen3_32b_jpp_",
        "frozen_lens": "jpp",
        "lens_layers": list(range(16, 52, 4)),
        "lenses": {
            "jpp": (
                "local",
                "cache/qwen3-32b-jpp/lenses/jpp/Qwen3-32B_jpp_lens.pt",
                "7d6856b60c958ee7a088f4afed3ed39ffbc8b88b69ad5a7a3c7e33290e64e781",
            ),
        },
        "frozen_lens_sha256": "7d6856b60c958ee7a088f4afed3ed39ffbc8b88b69ad5a7a3c7e33290e64e781",
    },
    # Gemma 4 31B-it with neuronpedia's published J++ fit on the BASE model (google/gemma-4-31B; 64 wikitext prompts,
    # target layer 59): no published lens is fit on the instruction-tuned model, and our own (gemma-4-31b-it above) was
    # lost with the old box. A stand-in (Zach, 2026-10-20): results on this target say what a base-model lens sees and
    # steers in the chat model; the country prompts are its positive control.
    "gemma-4-31b-it-baselens": {
        "repo": "google/gemma-4-31B-it",
        "revision": "842da3794eaa0b77d5f08bae87a17459d91ff475",
        "n_layers": 60,
        "norm_gain": "weight",
        "bos": True,
        "run_prefix": "gemma4itb_",
        "lenses": {
            "jpp": (
                LENS_REPO,
                "gemma-4-31b/jpp/Salesforce-wikitext/gemma-4-31B_jpp_lens.pt",
                "e166deb5ad540932100ef803c8c9bcc2a5453694",
            ),
        },
        "frozen_lens_sha256": "ef50bc54b04738e558b7d86847889bb5d60437e45276b1952e73da91b4e9f5fc",
    },
    # Gemma 4 31B-it with a J++ we fit on it (Zach asked, 2026-10-20 overnight; the base-model lens above failed the
    # positive control, and the old local fit was lost): the published recipe (safety-research/jpp_lens@93f02cd; 64
    # wikitext texts x 128 tokens, skip 16, target = the final block, LRP rlens, 8 experts, readout weights on the fit:0
    # items graded on this model) at source layers 24-45, every 3rd, only; scripts/lens_fit/gemma_it_fit_full.sh, exported
    # by scripts/lens_fit/export_jpp_lens.py. Readout pass@10 on the fit items, per layer, 0.35-0.53; held-out numbers in results/lens_fit/gemma_it_refit/.
    "gemma-4-31b-it-refit": {
        "repo": "google/gemma-4-31B-it",
        "revision": "842da3794eaa0b77d5f08bae87a17459d91ff475",
        "n_layers": 60,
        "norm_gain": "weight",
        "bos": True,
        "run_prefix": "gemma4itr_",
        "lenses": {
            "jpp": (
                "local",
                "cache/gemma-4-31b-it-refit/lenses/jpp/gemma-4-31B-it_jpp_lens.pt",
                "323733a9bec124c7a037a6839191bd545eb00d1d47bfffde6b92e1e638117408",
            ),
        },
        "frozen_lens_sha256": "323733a9bec124c7a037a6839191bd545eb00d1d47bfffde6b92e1e638117408",
    },
    # Gemma 4 31B-it with a J++ we fit on it at every source layer 0-58 (Zach asked, 2026-10-21: match Qwen3.6-27B's
    # every-layer published lens; the 24-45 every-3rd fit above stays for its runs): the same recipe (64 wikitext texts x
    # 128 tokens, skip 16, target = the final block, LRP rlens, 8 experts, readout weights on fit:0 items graded on this
    # model), scripts/queues/gemma_full_1021.sh. Gate: held-out macro pass@10 0.5284 PASS layers 24-45.
    "gemma-4-31b-it-full": {
        "repo": "google/gemma-4-31B-it",
        "revision": "842da3794eaa0b77d5f08bae87a17459d91ff475",
        "n_layers": 60,
        "norm_gain": "weight",
        "bos": True,
        "run_prefix": "gemma4itf_",
        "lenses": {
            "jpp": ("local", "cache/gemma-4-31b-it-full/lenses/jpp/gemma-4-31B-it_jpp_lens.pt", "d16d81d8751ad69df3493c0b3ea7410da97f69abfb07ee115600ad21ef9ef30a"),
        },
        "frozen_lens_sha256": "d16d81d8751ad69df3493c0b3ea7410da97f69abfb07ee115600ad21ef9ef30a",
    },
    # Qwen3-32B (dense, full attention in every layer: separates architecture from family; Zach, 2026-10-20/21): a J++ we
    # fit on it at every source layer 0-62 (32 wikitext prompts, the safety-research/jpp_lens@93f02cd recipe, on the
    # 2x H200 box, scripts/queues/h200_q32_shard_1021.sh + h200_q32_merge_1021.sh (2 shards)); held-out readout macro recall@10: {'Qwen3-32B_jpp_lens': 0.638, 'pooled_lens': 0.519} (gate: J++ >= 0.45).
    "qwen3-32b": {
        "repo": "Qwen/Qwen3-32B",
        "revision": "9216db5781bf21249d130ec9da846c4624c16137",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "qwen3_32b_",
        "lenses": {
            "jpp": ("local", "cache/qwen3-32b/lenses/jpp/Qwen3-32B_jpp_lens.pt", "6fbc03865ec674a2d2f346b23ea8220a7c7e2b0b3922d1afd1b300f455d3253e"),
        },
        "frozen_lens_sha256": "6fbc03865ec674a2d2f346b23ea8220a7c7e2b0b3922d1afd1b300f455d3253e",
    },
    # Qwen3.5-122B-A10B (MoE, 10B active) in Qwen's official FP8 release: the largest model with a published J++ that
    # fits one H200 (Zach, 2026-10-20, quick experiment L5; Neel: try a larger model early). Same tokenizer file as
    # Qwen3.6-27B; its J++ (neuronpedia, target layer 47) was fit on the bf16 weights, so FP8 activations differ
    # slightly from the lens's fitting runs.
    "qwen3.5-122b-a10b": {
        "repo": "Qwen/Qwen3.5-122B-A10B-FP8",
        "revision": "a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9",
        "n_layers": 48,
        "norm_gain": "one_plus_weight",
        "bos": False,
        "run_prefix": "qwen35_122b_",
        "lenses": {
            "jpp": (
                LENS_REPO,
                "qwen3.5-122b-a10b/jpp/Salesforce-wikitext/Qwen3.5-122B-A10B_jpp_lens.pt",
                "e166deb5ad540932100ef803c8c9bcc2a5453694",
            ),
        },
        "frozen_lens_sha256": "b771e50244c81a3f315987ca2b8e88a58f670e3fed934dd21e3bfec4a3c05e53",
    },
    # Mistral-Small-24B-Instruct-2501 (released 2025-01-30; dense, 40 blocks): the second model family (Zach, 2026-10-21,
    # after Gemma proved untestable with the knock-out). Its only lens is solarkyle's plain J-lens (not J++; 100 WikiText
    # prompts), so it is this target's frozen lens; the bridge target qwen3.6-27b-solarlens tells whether the lens type
    # moves the 27B's result. The snapshot skips the Mistral-format consolidated.safetensors (the HF shards are loaded);
    # the tokenizer loads with fix_mistral_regex (transformers warns the shipped pre-tokenizer regex is wrong).
    "mistral-small-24b-2501": {
        "repo": "mistralai/Mistral-Small-24B-Instruct-2501",
        "revision": "9527884be6e5616bdd54de542f9ae13384489724",
        "n_layers": 40,
        "norm_gain": "weight",  # MistralRMSNorm scales by weight
        "bos": True,  # <s> first; the chat template writes it, raw text gets it prepended
        "run_prefix": "mistral24_",
        "snapshot_ignore": ["consolidated.safetensors"],
        "tokenizer_kwargs": {"fix_mistral_regex": True},
        "chat_template": MISTRAL_CHAT_TEMPLATE,
        "frozen_lens": "jlens",
        "lenses": {"jlens": (SOLAR_LENS_REPO, "mistral-small-24b-instruct-2501/lens.pt", SOLAR_LENS_REVISION)},
        "frozen_lens_sha256": "6bda03097bf949788be3d2115c4635cc49c8217fdfa9e1d6d4832ac8ff531fec",
    },
    # Bridges (Zach, 2026-10-21): solarkyle's plain J-lens on Qwen3.6-27B (does the 27B's C1 hold with the lens type and
    # fitter Mistral gets?) and on Gemma 4 31B-it (does an independent lens also wreck Gemma's plain text?).
    "qwen3.6-27b-solarlens": {
        "repo": QWEN_REPO,
        "revision": QWEN_REVISION,
        "n_layers": 64,
        "norm_gain": "one_plus_weight",
        "bos": False,
        "run_prefix": "q27solar_",
        "frozen_lens": "jlens",
        "lenses": {"jlens": (SOLAR_LENS_REPO, "qwen3.6-27b/lens.pt", SOLAR_LENS_REVISION)},
        "frozen_lens_sha256": "55e1ec5c8565bbebe77c6c0eb3c6f725327e71a098038e0ec650cfd8152bdad6",
    },
    "gemma-4-31b-it-solarlens": {
        "repo": "google/gemma-4-31B-it",
        "revision": "842da3794eaa0b77d5f08bae87a17459d91ff475",
        "n_layers": 60,
        "norm_gain": "weight",
        "bos": True,
        "run_prefix": "gemma4its_",
        "frozen_lens": "jlens",
        "lenses": {"jlens": (SOLAR_LENS_REPO, "gemma-4-31b-it/lens.pt", SOLAR_LENS_REVISION)},
        "frozen_lens_sha256": "d53742a3b15b3a9fe396ca8a58dca6cc6c05b688f2b4c3ccb1595d6d22f8b1ec",
    },
    # Muse Glimmer 30B (Meta Superintelligence Lab, released 2026-08; dense, 52 blocks, local/global attention 3:1,
    # logit softcap with an output multiplier): the second model family from 2026-10-22, replacing Mistral (Zach: a newer
    # model with a better published lens). Frozen lens: eyes-ml's published plain J-lens (neuronpedia's fitter, 900
    # WikiText prompts, target = the final block, fit on a byte-identical copy of these weights). Zach: if this lens is not
    # good enough, consider fitting our own J++. The final norm scales by weight (the blocks' norms by 1 + weight).
    # 2026-10-22 (Zach): our own J++ is fit and becomes Muse's lens of record (target muse-glimmer-30b, prefix muse30_,
    # added by scripts/queues/h200_muse_fit_1022.sh); this J-lens target (prefix muse30j_) runs the gate and comparisons.
    # Muse Glimmer 30B with our own J++ (Zach, 2026-10-22; its lens of record): the safety-research/jpp_lens@93f02cd recipe
    # (+ scripts/lens_fit/jpp_lens_muse_1022.patch), 32 WikiText prompts, one shard, source layers 0-50, target the final
    # block; scripts/queues/h200_muse_fit_1022.sh. held-out macro pass@10: {'Muse-Glimmer-30B_jpp_lens': 0.959, 'logit': 0.67, 'pooled_lens': 0.893}.
    "muse-glimmer-30b": {
        "repo": "meta-models/Muse-Glimmer-30B",
        "revision": "cec94fcfd6512f2cfe708138c32533b346ea4f69",
        "n_layers": 52,
        "norm_gain": "weight",
        "bos": True,
        "run_prefix": "muse30_",
        "chat_template_edits": MUSE_TEMPLATE_EDITS,
        "lenses": {"jpp": ("local", "cache/muse-glimmer-30b/lenses/jpp/Muse-Glimmer-30B_jpp_lens.pt", "90fc5e52e8d765b729c4f894273fec5084fd3030db38b1b9b187cf67a1df8a12")},
        "frozen_lens_sha256": "90fc5e52e8d765b729c4f894273fec5084fd3030db38b1b9b187cf67a1df8a12",
    },
    # Is C1's strength the lens or the model? (Zach, 2026-10-22, docs/prereg_replication_1022.md amendment 3.) Qwen3-32B
    # with neuronpedia's published plain J-lens (557 WikiText prompts) beside our 32-prompt J++; and Qwen3-8B (dense,
    # standard attention like Qwen3-32B, unlike the hybrid 27B and 9B) with its published plain J-lens (461 prompts).
    # allenai/Olmo-Hybrid-Instruct-DPO-7B (Gated DeltaNet linear attention in 24 blocks, full attention in 8; the Olmo architecture pair, prereg amendment 6B; Zach, 2026-10-22): our own J++, the
    # safety-research/jpp_lens@93f02cd recipe (+ scripts/lens_fit/jpp_lens_olmo_hybrid_1022.patch), 32 WikiText prompts, one
    # shard, source layers 0-30, target the final block; scripts/queues/h200_olmo_fit_1022.sh. held-out macro pass@10: {'Olmo-Hybrid-Instruct-DPO-7B_jpp_lens': 0.605, 'logit': 0.399, 'pooled_lens': 0.491}.
    "olmo-hybrid-7b": {
        "repo": "allenai/Olmo-Hybrid-Instruct-DPO-7B",
        "revision": "ec62da5af0106ab4e83a60e07c4796ff358fd204",
        "n_layers": 32,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmoh7_",
        "lenses": {"jpp": ("local", "cache/olmo-hybrid-7b/lenses/jpp/Olmo-Hybrid-Instruct-DPO-7B_jpp_lens.pt", "b8dd5d16ba1ee7318c943ec1f3def36aed30f286185724c55afcb14a350c25dc")},
        "frozen_lens_sha256": "b8dd5d16ba1ee7318c943ec1f3def36aed30f286185724c55afcb14a350c25dc",
    },
    # allenai/Olmo-3-7B-Instruct-DPO (dense: sliding-window attention in 24 blocks, full attention in 8; the Olmo architecture pair, prereg amendment 6B; Zach, 2026-10-22): our own J++, the
    # safety-research/jpp_lens@93f02cd recipe (+ scripts/lens_fit/jpp_lens_olmo_hybrid_1022.patch), 32 WikiText prompts, one
    # shard, source layers 0-30, target the final block; scripts/queues/h200_olmo_fit_1022.sh. held-out macro pass@10: {'Olmo-3-7B-Instruct-DPO_jpp_lens': 0.487, 'logit': 0.384, 'pooled_lens': 0.427}.
    "olmo-3-7b": {
        "repo": "allenai/Olmo-3-7B-Instruct-DPO",
        "revision": "b33130b7de49f0c2553b5c2b3bc8409ff3e627d1",
        "n_layers": 32,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmo3d7_",
        "lenses": {"jpp": ("local", "cache/olmo-3-7b/lenses/jpp/Olmo-3-7B-Instruct-DPO_jpp_lens.pt", "1ca44bf5938b400b64a32bf9585b5e4cedb6a10249005b0cb6643f9115e94c11")},
        "frozen_lens_sha256": "1ca44bf5938b400b64a32bf9585b5e4cedb6a10249005b0cb6643f9115e94c11",
    },
    # gpt-oss-20b before its J++ exists (Zach, 2026-10-23: the non-Qwen generality model): competence and smoke runs; the
    # fit (scripts/queues/h200_gptoss_fit_1023.sh) registers "gpt-oss-20b" with the same run prefix. MoE (32 experts, 4
    # active), 24 blocks alternating sliding-window (128) and full attention with learned sinks: eager attention (sdpa
    # has no sinks); MXFP4 experts dequantized to bf16 on load, as the J++ fitter's environment does.
    # gpt-oss-20b with our own J++ (Zach, 2026-10-23, prereg amendment 8): the safety-research/jpp_lens@93f02cd recipe with the
    # LN rule only (+ scripts/lens_fit/jpp_lens_gptoss_1023.patch), 32 WikiText prompts, source layers 0-22, target the final
    # block; scripts/queues/h200_gptoss_1023.sh. .
    "gpt-oss-20b": {
        "repo": "openai/gpt-oss-20b",
        "revision": "6cee5e81ee83917806bbde320786a8fb61efebee",
        "n_layers": 24,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "gptoss20_",
        "snapshot_ignore": ["metal/*", "original/*"],
        "chat_template_edits": GPTOSS_TEMPLATE_EDITS,
        "attn": "eager",
        "dequantize_mxfp4": True,
        "lenses": {"jpp": ("local", "cache/gpt-oss-20b/lenses/jpp/gpt-oss-20b_jpp_lens.pt", "2902332d4852b27868db7f92182b1b006728b866bb2f1e25b58baedbf22ff077")},
        "frozen_lens_sha256": "2902332d4852b27868db7f92182b1b006728b866bb2f1e25b58baedbf22ff077",
    },
    # gpt-oss-20b with neuronpedia's published plain J-lens (Zach, 2026-10-23, prereg amendment 8b): a labelled comparison
    # lens after our LN-rule-only J++ failed the plain-text gate and read the model's own next token at 0.00-0.24 of
    # positions (logit lens 0.08-0.97). 457 WikiText prompts (converged), source layers 0-22.
    "gpt-oss-20b-jlens": {
        "repo": "openai/gpt-oss-20b",
        "revision": "6cee5e81ee83917806bbde320786a8fb61efebee",
        "n_layers": 24,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "gptoss20j_",
        "snapshot_ignore": ["metal/*", "original/*"],
        "chat_template_edits": GPTOSS_TEMPLATE_EDITS,
        "attn": "eager",
        "dequantize_mxfp4": True,
        "frozen_lens": "jlens",
        "lenses": {"jlens": ("neuronpedia/jacobian-lens", "gpt-oss-20b/jlens/Salesforce-wikitext/gpt-oss-20b_jacobian_lens.pt",
                             "e166deb5ad540932100ef803c8c9bcc2a5453694")},  # fmt: skip
        "frozen_lens_sha256": "2a8abf062eae4b6d39618b1237ad6945db437affd8c2122a09689114571553be",
    },
    "gpt-oss-20b-prefit": {
        "repo": "openai/gpt-oss-20b",
        "revision": "6cee5e81ee83917806bbde320786a8fb61efebee",
        "n_layers": 24,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "gptoss20_",
        "snapshot_ignore": ["metal/*", "original/*"],
        "chat_template_edits": GPTOSS_TEMPLATE_EDITS,
        "attn": "eager",
        "dequantize_mxfp4": True,
        "lenses": {},
    },
    # Aleph-Alpha/Kolibri-1 (Aleph Alpha, 2026-10-03; MoE, 78B total / 3.46B active, FP8 weights; sliding-window and
    # full attention; prereg amendment 28; Zach, 2026-10-24): needs transformers >= 5.20 (/workspace/ext/kolibri_env).
    # Lens: our J++ (Jacobians on the FP8 checkpoint dequantized to bf16, r+moe, 64 WikiText prompts, layers 0-48;
    # readout weights on the FP8 model; scripts/queues/h200_kolfit_1024.sh, amendment 28 note 2). held-out macro pass@10: {'Kolibri-1_jpp_lens': 0.484, 'logit': 0.447, 'pooled_lens': 0.274}.
    "kolibri-1": {
        "repo": "Aleph-Alpha/Kolibri-1",
        "revision": "5bb7075ba22db733e3834b1c71d2245537cc14ed",
        "n_layers": 50,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "kol1_",
        "lenses": {"jpp": ("local", "cache/kolibri-1/lenses/jpp/Kolibri-1_jpp_lens.pt", "cc8d19282258a20416d7fd106ad20a784ce8f1fd80983d12b8bfc7f2e245ac54")},
        "frozen_lens_sha256": "cc8d19282258a20416d7fd106ad20a784ce8f1fd80983d12b8bfc7f2e245ac54",
    },
    # Kolibri-1 with the same fit's pooled RelP lens (no expert weighting; the kind of every published neuronpedia
    # jpp lens): its secondary lens (amendment 28 note 2).
    "kolibri-1-pooled": {
        "repo": "Aleph-Alpha/Kolibri-1",
        "revision": "5bb7075ba22db733e3834b1c71d2245537cc14ed",
        "n_layers": 50,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "kol1p_",
        "lenses": {"jpp": ("local", "cache/kolibri-1-pooled/lenses/jpp/Kolibri-1_pooled_lens.pt", "fef79744e08be7ea1af1e21db1b0177565dd1f8c73c9cdf3e0d5cfe4535d7ada")},
        "frozen_lens_sha256": "fef79744e08be7ea1af1e21db1b0177565dd1f8c73c9cdf3e0d5cfe4535d7ada",
    },
    # Qwen/Qwen3.5-9B-Base (Qwen3.5 hybrid: Gated DeltaNet linear attention and full attention, base, pre-trained only; base vs instruct on matched lenses, prereg amendment 27; Zach, 2026-10-24): our own J++, the
    # safety-research/jpp_lens@93f02cd recipe (as patched in /workspace/ext/jpp_lens), 32 WikiText prompts, one shard,
    # source layers 0-30, target the final block; scripts/queues/h200_q9fit_1024.sh. held-out macro pass@10: {'Qwen3.5-9B-Base_jpp_lens': 0.621, 'logit': 0.402, 'pooled_lens': 0.483}.
    "qwen3.5-9b-base": {
        "repo": "Qwen/Qwen3.5-9B-Base",
        "revision": "68c46c4b3498877f3ef123c856ecfde50c39f404",
        "n_layers": 32,
        "norm_gain": "one_plus_weight",
        "bos": False,
        "run_prefix": "qwen35_9bb_",
        "lenses": {"jpp": ("local", "cache/qwen3.5-9b-base/lenses/jpp/Qwen3.5-9B-Base_jpp_lens.pt", "d80ffa435c1e5e0a7afa26e8e653df47f81085f64330429b1e023d8c99b55adf")},
        "frozen_lens_sha256": "d80ffa435c1e5e0a7afa26e8e653df47f81085f64330429b1e023d8c99b55adf",
    },
    # Qwen/Qwen3.5-9B (Qwen3.5 hybrid: Gated DeltaNet linear attention and full attention, instruct; base vs instruct on matched lenses, prereg amendment 27; Zach, 2026-10-24): our own J++, the
    # safety-research/jpp_lens@93f02cd recipe (as patched in /workspace/ext/jpp_lens), 32 WikiText prompts, one shard,
    # source layers 0-30, target the final block; scripts/queues/h200_q9fit_1024.sh. held-out macro pass@10: {'Qwen3.5-9B_jpp_lens': 0.625, 'logit': 0.391, 'pooled_lens': 0.495}.
    "qwen3.5-9b-ourjpp": {
        "repo": "Qwen/Qwen3.5-9B",
        "revision": "c202236235762e1c871ad0ccb60c8ee5ba337b9a",
        "n_layers": 32,
        "norm_gain": "one_plus_weight",
        "bos": False,
        "run_prefix": "qwen35_9boj_",
        "lenses": {"jpp": ("local", "cache/qwen3.5-9b-ourjpp/lenses/jpp/Qwen3.5-9B_jpp_lens.pt", "690f19e7caba242b5aa027d7d4c326f546b98bd2c720bd8fdee772965f49f7eb")},
        "frozen_lens_sha256": "690f19e7caba242b5aa027d7d4c326f546b98bd2c720bd8fdee772965f49f7eb",
    },
    # allenai/Olmo-3-1125-32B (OLMo 3 32B base, Ai2, 2025-11; dense, 64 blocks, sliding-window and full attention,
    # post-norm sublayers; Apache-2.0): the non-Qwen dense model with a published J++ by the J++ authors (Ayonrinde &
    # Lindsey; neuronpedia recall@10 50.0%; rlens, 64 WikiText prompts, target layer 63), prereg amendment 31 (Zach,
    # 2026-10-24). A base model: module 1 in raw-text framing. BOS as the tokenizer defines it (the J++ fit prepended it).
    "olmo-3-32b": {
        "repo": "allenai/Olmo-3-1125-32B",
        "revision": "c2b61dae89a1ad10e4ad5653d0e46b590902607b",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmo32_",
        "lenses": {"jpp": (LENS_REPO, "olmo-3-1125-32b/jpp/Salesforce-wikitext/Olmo-3-1125-32B_jpp_lens.pt", "e166deb5ad540932100ef803c8c9bcc2a5453694")},
        "frozen_lens_sha256": "bf3efcf2007fb8ff9683ae23833027dd16d674aecc4ff9e6f0e66d14210e4466",
    },
    # The same model with the plain J-lens of the same repo (the paper's own lens): the secondary lens (amendment 31).
    "olmo-3-32b-jlens": {
        "repo": "allenai/Olmo-3-1125-32B",
        "revision": "c2b61dae89a1ad10e4ad5653d0e46b590902607b",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmo32j_",
        "frozen_lens": "jlens",
        "lenses": {"jlens": (LENS_REPO, "olmo-3-1125-32b/jlens/Salesforce-wikitext/Olmo-3-1125-32B_jacobian_lens.pt", "e166deb5ad540932100ef803c8c9bcc2a5453694")},
        "frozen_lens_sha256": "c6ee7d22c3a224fd1a6f9bb66ee9d23c7c4ac678f2f554e0f3815bbe0540a508",
    },
    "qwen3-32b-jlens": {
        "repo": "Qwen/Qwen3-32B",
        "revision": "9216db5781bf21249d130ec9da846c4624c16137",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "qwen3_32bj_",
        "frozen_lens": "jlens",
        "lenses": {"jlens": (LENS_REPO, "qwen3-32b/jlens/Salesforce-wikitext/Qwen3-32B_jacobian_lens.pt", LENS_REVISION)},
        "frozen_lens_sha256": "0af5ccf2e1c251bedc202607a7ca214f3b9f60980bab73d67a3d0b887db213d8",
    },
    "qwen3-8b-jlens": {
        "repo": "Qwen/Qwen3-8B",
        "revision": "b968826d9c46dd6066d109eabc6255188de91218",
        "n_layers": 36,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "qwen3_8b_",
        "frozen_lens": "jlens",
        "lenses": {"jlens": (LENS_REPO, "qwen3-8b/jlens/Salesforce-wikitext/Qwen3-8B_jacobian_lens.pt", LENS_REVISION)},
        "frozen_lens_sha256": "1e1f96c3b63ac46731a78658304c8857ef08992351268f0c78893361692059c3",
    },
    "muse-glimmer-30b-jlens": {
        "repo": "meta-models/Muse-Glimmer-30B",
        "revision": "cec94fcfd6512f2cfe708138c32533b346ea4f69",
        "n_layers": 52,
        "norm_gain": "weight",
        "bos": True,  # <|begin_of_text|> first; the chat template writes it, raw text gets it prepended
        "run_prefix": "muse30j_",
        "chat_template_edits": MUSE_TEMPLATE_EDITS,
        "frozen_lens": "jlens",
        "lenses": {"jlens": ("eyes-ml/Muse-Glimmer-30B_jacobian-lens", "Muse-Glimmer-30B_jacobian_lens.pt", "71d8434fbd38c8b5d70e1ff1ff2095d5da926c34")},
        "frozen_lens_sha256": "397dc00807a8f72d9d21feaeedeba7fb9e7c50e5c80efc317f37e8cd9c833300",
    },
    # Bridge for Muse (Zach, 2026-10-22): neuronpedia's published plain J-lens for Qwen3.6-27B (1000 WikiText prompts,
    # the fitter family of Muse's lens): does the 27B's C1 hold with a plain J-lens?
    "qwen3.6-27b-jlens": {
        "repo": QWEN_REPO,
        "revision": QWEN_REVISION,
        "n_layers": 64,
        "norm_gain": "one_plus_weight",
        "bos": False,
        "run_prefix": "q27jlens_",
        "frozen_lens": "jlens",
        "lenses": {"jlens": (LENS_REPO, LENS_FILE, LENS_REVISION)},
        "frozen_lens_sha256": "1718c8c52dd8a9dad03738d4d625937c1fbba10be325b872ed446c7290fc11e1",
    },
    # Qwen3.5-0.8B: smoke tests only (same qwen3_5 hybrid architecture as Qwen3.6-27B, 24 layers, full attention at
    # every 4th), so new part B scripts run end to end on a spare GPU before a 27B run. Never a headline target.
    "qwen3.5-0.8b": {
        "repo": "Qwen/Qwen3.5-0.8B",
        "revision": "2fc06364715b967f1860aea9cf38778875588b17",
        "n_layers": 24,
        "norm_gain": "one_plus_weight",
        "bos": False,
        "run_prefix": "qwen35_08b_",
        "lenses": {
            "jpp": (LENS_REPO, "qwen3.5-0.8b/jpp/Salesforce-wikitext/Qwen3.5-0.8B_jpp_lens.pt", LENS_REVISION),
        },
        "frozen_lens_sha256": "39bf7690b7e1d917ccff9c0fd7418abeaa02fe334691edfb7e814ee890b99c06",
    },
    # OLMo-3-7B post-training ladder, base -> SFT -> DPO -> Instruct (Dan's D5b, 2026-10-20: does the memory/prompt split
    # exist before post-training?). Olmo3ForCausalLM, 32 layers, d 4096, untied lm_head; sliding-window attention
    # (4096) except full attention at 3, 7, ..., 31. Post-sublayer norms (OLMo 2 style: block l outputs h + norm(attn(h)),
    # then + norm(mlp(.)); no input norms): the block output is the raw residual stream, as the lens hooks it, and the
    # final norm (Olmo3RMSNorm) scales by weight. One tokenizer for plain text (cl100k-style, 100278 ids); the base
    # tokenizer has no BOS and no chat template, the post-trained ones name <|endoftext|> as BOS but neither their chat
    # template nor tokenizer(text) writes it, so no BOS anywhere.
    # Lenses: mhough/olmo3-jacobian-lenses, plain J-lenses (NOT J++) in jlens's save format (J, source_layers,
    # n_prompts, d_model; fp16), one per checkpoint, fit with the same recipe on the same 616 wikitext-103 train prompts
    # (128 tokens, skip 16, target = block 31) at source layers 0, 3, ..., 30 only ("lens_layers"). JLens reads them as
    # they are (no conversion). Their key is "jlens", named by "frozen_lens": FROZEN_LENS below is this key on these
    # targets (and its sha256 is checked on load), so a run records the J-lens as "jlens", never as J++; scripts that use
    # the lens restrict their layers to LENS_LAYERS.
    "olmo-3-7b-base": {
        "repo": "allenai/Olmo-3-1025-7B",
        "revision": "a81bae42db3975be1671e27b9c9a56da1a9f980f",
        "n_layers": 32,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmo3_7b_base_",
        "frozen_lens": "jlens",
        "lens_layers": list(range(0, 31, 3)),
        "lenses": {
            "jlens": (
                "mhough/olmo3-jacobian-lenses",
                "lenses/olmo-3-1025-7b.pt",
                "d15b6af0058e89e78d40847c945b6e4dc7fbfe82",
            ),
            # neuronpedia's independent fit of the base model at every layer 0-30 (568 wikitext prompts, sha256
            # 0683d9725bc9c09881c56784ee1371956ad5793b41731ea1213f025757073183): a cross-check, never the ladder's lens
            "np_jlens": (
                LENS_REPO,
                "olmo-3-1025-7b/jlens/Salesforce-wikitext/Olmo-3-1025-7B_jacobian_lens.pt",
                "e166deb5ad540932100ef803c8c9bcc2a5453694",
            ),
        },
        "frozen_lens_sha256": "afa868bc9b4456fc2827fbc0e7c03e92d51843aea89bb76d273cd3525035602e",
    },
    "olmo-3-7b-sft": {
        "repo": "allenai/Olmo-3-7B-Instruct-SFT",
        "revision": "e1452fc572d51966ff4aaeb25118b891eb93e549",
        "n_layers": 32,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmo3_7b_sft_",
        "frozen_lens": "jlens",
        "lens_layers": list(range(0, 31, 3)),
        "lenses": {
            "jlens": (
                "mhough/olmo3-jacobian-lenses",
                "lenses/olmo-3-7b-instruct-sft.pt",
                "d15b6af0058e89e78d40847c945b6e4dc7fbfe82",
            ),
        },
        "frozen_lens_sha256": "f215ecf21b6558252d936dc37d22a1ceca356ebe29608aab6026965c05052899",
    },
    "olmo-3-7b-dpo": {
        "repo": "allenai/Olmo-3-7B-Instruct-DPO",
        "revision": "b33130b7de49f0c2553b5c2b3bc8409ff3e627d1",
        "n_layers": 32,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmo3_7b_dpo_",
        "frozen_lens": "jlens",
        "lens_layers": list(range(0, 31, 3)),
        "lenses": {
            "jlens": (
                "mhough/olmo3-jacobian-lenses",
                "lenses/olmo-3-7b-instruct-dpo.pt",
                "d15b6af0058e89e78d40847c945b6e4dc7fbfe82",
            ),
        },
        "frozen_lens_sha256": "0b407ba5b0d9efdd4cfce979a2b2e26d33b4b0bfc60a8025f2a4308f02ccd6fb",
    },
    "olmo-3-7b-instruct": {
        "repo": "allenai/Olmo-3-7B-Instruct",
        "revision": "6e5971d9eba42665f5bd5a0fcf047f299ce1dccc",
        "n_layers": 32,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmo3_7b_instruct_",
        "frozen_lens": "jlens",
        "lens_layers": list(range(0, 31, 3)),
        "lenses": {
            "jlens": (
                "mhough/olmo3-jacobian-lenses",
                "lenses/olmo-3-7b-instruct.pt",
                "d15b6af0058e89e78d40847c945b6e4dc7fbfe82",
            ),
        },
        "frozen_lens_sha256": "b847dbba1406dc019adaeec09d971c60574c18dc28f031a93e8b43fa028b2774",
    },
    # OLMo-3-7B-Instruct with OUR J++ (Dan, 23 Oct: every lens result on J++), every layer 0-30 (no lens_layers: the
    # depth-scaled grid, every 2nd layer, as the 9B). The published recipe (safety-research/jpp_lens@93f02cd), 64 WikiText
    # prompts x 128 tokens, one shard on an A100 80GB, router seed 0, skip 16, target = the last block, rlens LRP, 8 experts;
    # the fp16 export done by hand (the job passed --note positionally). Primary lens (Dan, 23 Oct ~00:30): ours, the
    # published recipe on 64 prompts; Zach's fit reported alongside when shared; no silent switch. HF:
    # danorel/Olmo-3-7B-Instruct-jpp-lens @ fd8f1d4e89e32081c722442d784bda70bf15170e. Fit record:
    # results/lens_fit/olmo3_7b_instruct_jpp_20261023-100523.
    "olmo-3-7b-instruct-jpp": {
        "repo": "allenai/Olmo-3-7B-Instruct",
        "revision": "6e5971d9eba42665f5bd5a0fcf047f299ce1dccc",
        "n_layers": 32,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmo3_7b_instruct_jpp_",
        "frozen_lens": "jpp",
        "lenses": {
            "jpp": (
                "local",
                "cache/olmo-3-7b-instruct/lenses/jpp/Olmo-3-7B-Instruct_jpp_lens.pt",
                "6847cfb38a14d7cf0049efff80364d051d69ec91998e44177e7fb5b4b9732451",
            ),
        },
        "frozen_lens_sha256": "6847cfb38a14d7cf0049efff80364d051d69ec91998e44177e7fb5b4b9732451",
    },
    # Olmo-Hybrid-7B Instruct (Dan, 23 Oct): the non-Qwen DeltaNet hybrid, paired with OLMo-3-7B-Instruct (same family,
    # tokenizer and chat template; softmax attention in every layer) to separate architecture from family. Lens-free
    # findings only (late read, name vs digit). The DPO checkpoint is the final Olmo Hybrid Instruct (Ai2 released no
    # RLVR stage for it; OLMo-3-7B-Instruct is DPO + RLVR). OlmoHybridForCausalLM (transformers >= 5.3), 32 layers, d 3840:
    # Gated DeltaNet in 24 (OlmoHybridGatedDeltaNet), full attention without RoPE at 3, 7, ..., 31; post-sublayer norms on
    # attention blocks, input norms on DeltaNet blocks; final norm scales by weight; no BOS (as OLMo-3).
    # No lens: "lenses" is empty (port_smoke skips its lens check) and no layer has a map (check_lens_layers refuses).
    "olmo-hybrid-7b-instruct-dpo": {
        "repo": "allenai/Olmo-Hybrid-Instruct-DPO-7B",
        "revision": "ec62da5af0106ab4e83a60e07c4796ff358fd204",
        "n_layers": 32,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "olmo_hybrid_7b_",
        "lens_layers": [],
        "lenses": {},
    },
}
# DeepSeek-V4-Flash's chat format, thinking off, as deepseek-ai's encoding/encoding_dsv4.py encode_messages(...,
# thinking_mode="chat") renders system / user / assistant turns (read from its source and its chat-mode test, not run):
# BOS, a system turn raw, each user turn "<｜User｜>" + content then "<｜Assistant｜></think>" when an assistant turn or the
# generation follows, each assistant turn its content + EOS. The tokenizer ships no chat template (2026-10-25).
DEEPSEEK_V4_CHAT_TEMPLATE = (
    "{{- bos_token }}"
    "{%- for m in messages %}"
    "{%- if m['role'] == 'system' %}{{- m['content'] }}"
    "{%- elif m['role'] == 'user' %}{{- '<｜User｜>' + m['content'] }}"
    "{%- if loop.last or messages[loop.index0 + 1]['role'] == 'assistant' %}{{- '<｜Assistant｜></think>' }}{%- endif %}"
    "{%- elif m['role'] == 'assistant' %}{{- m['content'] + '<｜end▁of▁sentence｜>' }}"
    "{%- else %}{{- raise_exception('Only system, user and assistant roles are supported!') }}{%- endif %}"
    "{%- endfor %}"
)

# 2026-10-25 (non-Qwen families, Zach): DeepSeek-V4-Flash (MoE, 284B total / 13B active, FP8, 160 GB; two GPUs) with
# its published J++ (Ayonrinde & Lindsey, via neuronpedia), and Ministral 3 14B Instruct (dense, BF16 repo; its
# tokenizer needs fix_mistral_regex; its template without the default system prompt) with our own J++ (fit pending).
TARGETS["deepseek-v4-flash"] = {
    "repo": "deepseek-ai/DeepSeek-V4-Flash",
    "revision": "60d8d70770c6776ff598c94bb586a859a38244f1",
    "n_layers": 43,
    "norm_gain": "weight",
    "bos": True,
    "run_prefix": "dsv4f_",
    "split_gpus": 14,  # blocks 0-13 on cuda:0 (was 22), so it fits beside Ministral on GPU 0 (2026-10-25, amendment 39 note 2)
    "attn": "eager",  # DeepseekV4 supports eager only (per-head attention sinks; transformers 5.17), 2026-10-25
    "chat_template": DEEPSEEK_V4_CHAT_TEMPLATE,
    "lenses": {"jpp": (LENS_REPO, "deepseek-v4-flash/jpp/Salesforce-wikitext/DeepSeek-V4-Flash_jpp_lens.pt", "e166deb5ad540932100ef803c8c9bcc2a5453694")},
    "frozen_lens_sha256": "e7dc42a68afb8411c4cba01605ce51eec17d7ad0f3150009173224e96864633e",
}
TARGETS["ministral-3-14b"] = {
    "repo": "mistralai/Ministral-3-14B-Instruct-2512-BF16",
    "revision": "3cea74c1ebaf5ce5f5a2553de470e2ceab825142",
    "n_layers": 40,
    "norm_gain": "weight",
    "bos": True,
    "run_prefix": "min14_",
    "snapshot_ignore": ["consolidated.safetensors"],
    "tokenizer_kwargs": {"fix_mistral_regex": True},
    "chat_template": MISTRAL_CHAT_TEMPLATE,
    "lenses": {"jpp": ("local", "cache/ministral-3-14b/lenses/jpp/Ministral-3-14B-Instruct-2512-BF16_jpp_lens.pt", "45977bd89f5310ec93726d69c198dd788b64b77c8f3b5884ef21fc58652ed3e3")},  # our J++ (h200_minfit_1025.sh); held-out macro pass@10: {'Ministral-3-14B-Instruct-2512-BF16_jpp_lens': 0.651, 'logit': 0.461, 'pooled_lens': 0.545}
    "frozen_lens_sha256": "45977bd89f5310ec93726d69c198dd788b64b77c8f3b5884ef21fc58652ed3e3",
}

# 2026-10-25 (amendment 40): NVIDIA Nemotron 3.5 Lightning 30B-A3B (hybrid: 52 blocks, each one Mamba-2, attention or MoE
# mixer; final norm norm_f, a plain weight). Its tokenizer adds no BOS (add_bos_token false) and its chat template writes
# none, so bos False. Thinking off via the template's enable_thinking (chat.chat_text). No published lens, and the J++
# fitter has no Mamba rules: (superseded 2026-10-25, amendment 45: our J++ with the LN rule alone, no plain J-lens); its sha256 replaces the None placeholders when the fit ends (scripts/queues/h200_nem_1025.sh).
TARGETS["nemotron-3.5-lightning"] = {
    "repo": "nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
    "revision": "a9904d24bcc1d289a1950fa9d2b978c47cf903b9",
    "n_layers": 52,
    "norm_gain": "weight",
    "bos": False,
    "run_prefix": "nem35l_",
    "use_kernels": True,  # HF-hub kernels (kernels-community/mamba-ssm & co.): 9-12x the torch Mamba path; WikiText NLL 2.4642 vs 2.4634 (amendment 42)
    "frozen_lens": "jpp",  # our J++, LN rule only (amendment 45; Zach: no plain J-lenses)
    "lenses": {"jpp": ("local", "cache/nemotron-3.5-lightning/lenses/jpp/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jpp_lens.pt", "3306b6e4f0f4ba039cde5f902aeb3ef6ae8b775a7abc1b999f6cbc0b7d534f44")},  # our J++, LN rule only (h200_nemfit_1025.sh); held-out macro pass@10: {'NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16_jpp_lens': 0.587, 'logit': 0.443, 'pooled_lens': 0.481}
    "frozen_lens_sha256": "3306b6e4f0f4ba039cde5f902aeb3ef6ae8b775a7abc1b999f6cbc0b7d534f44",
}

# 2026-10-25 (amendment 40, note 1): NVIDIA Nemotron 3.5 Bolt 74B-A9B, the language model of its multimodal checkpoint
# (88 blocks: Mamba-2, attention, and MoE blocks of per-layer sizes; final norm norm_f), built by NVIDIA's own code at the
# pinned revision (model._remote_lm), over two GPUs. No BOS, thinking off, our plain J-lens: as Lightning's.
TARGETS["nemotron-3.5-bolt"] = {
    "repo": "nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16",
    "revision": "e09a4cedb1787db1760375ee5539f222cae0c672",
    "n_layers": 88,
    "norm_gain": "weight",
    "bos": False,
    "run_prefix": "nem35b_",
    "split_gpus": 44,
    "tokenizer_kwargs": {"trust_remote_code": False},  # its tokenizer_config names a remote AutoProcessor; the tokenizer needs none
    "remote_lm": {
        "config": "configuration_nemotron_h_puzzle.NemotronHPuzzleConfig",
        "model": "modeling_nemotron_h_puzzle.NemotronHPuzzleForCausalLM",
        "config_key": "llm_config",
        "key_mapping": {r"^language_model\.backbone\.": "model.", r"^language_model\.": ""},
        # amendment 44: the prebuilt HF-hub mamba-ssm, the revision transformers fetched for Lightning
        "hub_mamba": {"repo": "kernels-community/mamba-ssm", "revision": "28017f36635a6b94d911333812beeed5dd901ac0"},
    },
    "frozen_lens": "jpp",  # our J++ (amendment 45; Zach: no plain J-lenses); fit not yet built
    "lenses": {"jpp": ("local", "cache/nemotron-3.5-bolt/lenses/jpp/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16_jpp_lens.pt", "a29ea5bf92976c202c65a72a3a0e139bfd19ea68353722bbab78a094d8e24040")},  # our J++, LN rule only (h200_nemfit_1025.sh); held-out macro pass@10: {'NVIDIA-Nemotron-3.5-Bolt-74B-A9B-BF16_jpp_lens': 0.8, 'logit': 0.658, 'pooled_lens': 0.751}
    "frozen_lens_sha256": "a29ea5bf92976c202c65a72a3a0e139bfd19ea68353722bbab78a094d8e24040",
}

# 2026-10-25: the 9B split over two GPUs (blocks 0-15 on cuda:0, 16-31 on cuda:1), to check model.split_gpus against the
# one-GPU runs before DeepSeek-V4-Flash (which needs two GPUs) relies on it.
TARGETS["qwen3.5-9b-split"] = {**TARGETS["qwen3.5-9b"], "split_gpus": 16, "run_prefix": "qwen35_9bsplit_"}

# Run-name prefixes shared by two lenses since danorel was merged into main (27 Oct 2026; main kept every key). Dan's
# Qwen3-32B J-lens runs were made as his target "qwen3-32b" and named qwen3_32b_, the prefix of main's "qwen3-32b"
# (Zach's J++). Runs are written once, so the names stay: such a run resolves to its key by the lens sha256 its manifest
# records (run_target); None, a run that records no lens, resolves to Dan's key (his lens-free runs; the checkpoint is
# the same under every Qwen3-32B key). New runs take the live prefixes (check_run_name): Dan's J-lens is
# "qwen3-32b-jlens" (qwen3_32bj_). This is the one overlap of a legacy and a live prefix (tests/test_pins_keys.py).
LEGACY_PREFIXES: dict[str, dict[str | None, str]] = {
    "qwen3_32b_": {
        "0af5ccf2e1c251bedc202607a7ca214f3b9f60980bab73d67a3d0b887db213d8": "qwen3-32b-jlens",  # Dan's runs
        "6fbc03865ec674a2d2f346b23ea8220a7c7e2b0b3922d1afd1b300f455d3253e": "qwen3-32b",  # Zach's runs
        None: "qwen3-32b-jlens",
    },
}

TARGET = os.environ.get("BJ_TARGET", "qwen3.6-27b")
assert TARGET in TARGETS, f"BJ_TARGET={TARGET!r}: not one of {sorted(TARGETS)}"
MODEL_REPO: str = TARGETS[TARGET]["repo"]
MODEL_REVISION: str = TARGETS[TARGET]["revision"]
N_LAYERS: int = TARGETS[TARGET]["n_layers"]
RUN_PREFIX: str = TARGETS[TARGET]["run_prefix"]
# The layers the target's frozen lens has a map at; None: the layers the scripts use all have one (every pin before the
# OLMo ladder), so nothing is restricted.
LENS_LAYERS: list[int] | None = None
if TARGET != "qwen3.6-27b":
    CACHE_DIR = REPO_ROOT / "cache" / TARGET
    LENS_SOURCES = TARGETS[TARGET]["lenses"]
    FROZEN_LENS = TARGETS[TARGET].get("frozen_lens", FROZEN_LENS)
    FROZEN_LENS_SHA256 = TARGETS[TARGET].get("frozen_lens_sha256", FROZEN_LENS_SHA256)
    LENS_LAYERS = TARGETS[TARGET].get("lens_layers")


def on_lens(layers) -> tuple[int, ...]:
    """`layers` that have a map in the target's frozen lens, in order (all of them when LENS_LAYERS is None)."""
    return tuple(la for la in layers if LENS_LAYERS is None or la in LENS_LAYERS)


def check_lens_layers(layers) -> None:
    """Assert every layer in `layers` has a map in the target's frozen lens (before a run writes anything)."""
    missing = [la for la in layers if not on_lens((la,))]
    assert not missing, (
        f"BJ_TARGET={TARGET}: layers {missing} have no {FROZEN_LENS} map; its lens layers are {LENS_LAYERS}"
    )


def git_state() -> dict[str, Any]:
    """2026-10-26 (amendment 49 note 1): the working tree at run start, so a run whose code was not yet committed shows
    as such: HEAD, tracked files that differ from it, untracked scripts, and a hash of the diff."""
    import subprocess

    def git(*a: str) -> str:
        return subprocess.run(["git", *a], capture_output=True, text=True, cwd=REPO_ROOT).stdout

    dirty = [line[3:] for line in git("status", "--porcelain", "--untracked-files=no").splitlines() if line.strip()]
    new = [line[3:] for line in git("status", "--porcelain", "--untracked-files=all", "--", "scripts", "src").splitlines()
           if line.startswith("??") and line.endswith((".py", ".sh"))]  # fmt: skip
    diff = git("diff", "HEAD", "--", "scripts", "src")
    return {"head": git("rev-parse", "HEAD").strip(), "dirty_files": dirty, "untracked_scripts": new,
            "code_diff_sha256": hashlib.sha256(diff.encode()).hexdigest() if diff else None}  # fmt: skip


def model_pin() -> dict[str, str]:
    """The target model as manifests record it, with the prompt format (chat.FORMAT, BJ_FORMAT) its prompts use."""
    from bridge_jspace import chat

    pin = {"target": TARGET, "repo": MODEL_REPO, "revision": MODEL_REVISION, "dtype": "bfloat16",
           "attn": TARGETS[TARGET].get("attn", "sdpa"), "prompt_format": chat.FORMAT}  # fmt: skip
    if TARGETS[TARGET].get("use_kernels"):
        pin["kernels"] = "hub"
    return pin


def run_target(name: str, lens_sha256: str | None = None) -> str:
    """The TARGETS key a run name belongs to: that of the longest live run prefix it starts with ("qwen3.6-27b" when
    none does), except where LEGACY_PREFIXES lists that prefix: there the lens its manifest records decides
    (`lens_sha256`; None for a lens-free run). KeyError for a legacy prefix that never had that lens."""
    live = max(((t["run_prefix"], k) for k, t in TARGETS.items() if t["run_prefix"] and name.startswith(t["run_prefix"])),
               key=lambda pk: len(pk[0]), default=("", "qwen3.6-27b"))  # fmt: skip
    legacy = max((p for p in LEGACY_PREFIXES if name.startswith(p)), key=len, default="")
    if legacy and len(legacy) >= len(live[0]):
        by_sha = LEGACY_PREFIXES[legacy]
        if lens_sha256 not in by_sha:
            raise KeyError(f"{name!r}: run prefix {legacy!r} had no lens with sha256 {lens_sha256!r}")
        return by_sha[lens_sha256]
    return live[1]


def check_run_name(name: str) -> None:
    """A run of a non-default target is named with its prefix, so its results never pass for Qwen's; a raw-format run
    (BJ_FORMAT=raw) has "_raw" in its name and a chat-format run does not, so the two never pass for each other."""
    from bridge_jspace import chat

    assert name.startswith(RUN_PREFIX), f"BJ_TARGET={TARGET}: run names start with {RUN_PREFIX!r}, got {name!r}"
    raw = "_raw" in name
    assert raw == (chat.FORMAT == "raw"), (
        f"BJ_FORMAT={chat.FORMAT}: run names {'need' if chat.FORMAT == 'raw' else 'must not have'} '_raw', got {name!r}"
    )


# The oracle lens (exp15): a LoRA on Qwen3.6-27B, same repo and revision; run s3d.rl.ddp600.s0 (see its run.json).
ORACLE_DIR = "qwen3.6-27b/oracle"
ORACLE_ADAPTER_SHA256 = "7d4b301e002246af3c3f2bb6e768f8fa62f8aac2c231a0bd02a8d4f9ecafd9aa"
# The NLA (exp16): a separate verbalizer, av_base (Qwen3.6-27B with its warm-start LoRA merged) + one GRPO adapter.
NLA_REPO = "ceselder/qwen3.6-27b-nla-rl"
NLA_REVISION = "5a13b7ec21a69fcdd0fb24d5edbe96a92aef4b9f"
NLA_ADAPTER = "av_rl_adapters/iter_000400"  # WorkspaceBench's choice; trained on layer-42 activations
NLA_ADAPTER_SHA256 = "b54e23e4e36dbd04023b307e3abfd4618b5db2b31b8e7c650a957ebb1c90c358"

PROBE_SWAP_FILE = DATA_DIR / "probe_swap.json"
PROBE_SWAP_SHA256 = "a0edd27ca23f7b4d0fbe90448c2ddcc7457a3d812121bf024ed12a032ff86796"
BREW_FILE = DATA_DIR / "brew_intermediates.json"  # WorkspaceBench's brew_intermediates bank (part B's exp03)
BREW_SHA256 = "183be95d4182c373674786b7610820520e56434fb0c15a75a62dad854bed9d83"
BREW_FRESH_FILE = DATA_DIR / "brew_fresh.json"  # exp03_make_items.py: held-out items in the bank's format, ungated
BREW_FRESH_SHA256 = "1e20ed25b3727842acba0806b346d91d991db1fa31f42f514e537fb3ab000d3c"
BREW_FIT_FILE = DATA_DIR / "brew_fit.json"  # exp03_make_items.py: exp07's fitting items, never a bank or fresh prompt
BREW_FIT_SHA256 = "b9ab169a50bf576d71c074b31516f283e3163366d8ce2aea0907addbdf0e2659"
BREW_TEST_FILE = DATA_DIR / "brew_test.json"  # exp03_make_items.py: exp18 v3's held-out items (no bank/fresh/fit)
BREW_TEST_SHA256 = "40f07001d080af30bbd6396c554f90e2b350108f7a0bfb7e7bae1a5fc1e250d0"
BIND_RECALL_FILE = DATA_DIR / "bind_recall.json"  # exp09_make_items.py: recalled vs bound bridge countries
BIND_RECALL_SHA256 = "bbb1cfa8e95b6a83ec1c6003fc3a05c5c1fba195cff6a5cb7e3ea968dce59029"
BIND_LOOKUP_FILE = DATA_DIR / "bind_lookup.json"  # exp09_make_items.py --lookup: family L (bind, then a table)
BIND_LOOKUP_SHA256 = "dec730702c8805ac96699f9b2553cc06a7fa5d0090132b62a96ab6d84936fed3"
BIND_LOOKUP_V2_FILE = DATA_DIR / "bind_lookup_v2.json"  # the same L items asked "... has the colour"
BIND_LOOKUP_V2_SHA256 = "0883e3e5aa3dcecb41295a1324d6e366ba1bb766d6bd97b5b378a97cf4beae45"
RECALL_LOOKUP_FILE = DATA_DIR / "recall_lookup.json"  # exp09 family RL: recalled bridge, in-context lookup
RECALL_LOOKUP_SHA256 = "d6905b4445032dab8ca3a2e8fff74588750175e004af1c31b3a235f44d15703f"
USE_SOURCE_FILE = DATA_DIR / "use_source.json"  # Phase 3: LM, RM, BT, RT (what uses the bridge vs the answer's source)
USE_SOURCE_SHA256 = "cffddf8fc2995b9c221e518805e996fa32a861b114a2b50f06e1334f0d8acacf"
WIKITEXT_FILE = DATA_DIR / "wikitext103_test.json"  # generic text for part B's residual covariance (exp06)
WIKITEXT_SHA256 = "a6b5b17a576932fbb570a96b0f5b6a65ced408690a2dce749a8c56f980bbcc0f"
LENS_EVAL_MULTIHOP_FILE = DATA_DIR / "lens_eval_multihop.json"
LENS_EVAL_MULTIHOP_SHA256 = "50b7e4c9255291c0ca2a8e94615be9f44531fa57bb1a844e4f9616056d987416"
# SQuAD v1.1 dev (Rajpurkar et al. 2016; CC BY-SA 4.0), the raw upstream file at a pinned commit of the dataset's
# site repo (the site's own copy has the same sha256). Not committed: downloaded once into cache/ (REPO_ROOT's, not a
# target's CACHE_DIR); scripts/natural_read.py make derives NATURAL_READ_FILE from it (finding 4 on natural text).
SQUAD_DEV_URL = ("https://raw.githubusercontent.com/rajpurkar/SQuAD-explorer/240e165ab706d95bd4323653bb92421f446208cf/"
                 "dataset/dev-v1.1.json")  # fmt: skip
SQUAD_DEV_FILE = REPO_ROOT / "cache" / "natural_read" / "squad" / "dev-v1.1.json"
SQUAD_DEV_SHA256 = "95aa6a52d5d6a735563366753ca50492a658031da74f301ac5238b03966972c9"
NATURAL_READ_FILE = DATA_DIR / "natural_read_v1" / "items.json"  # natural_read.py make: one question per paragraph
NATURAL_READ_SHA256 = "60b8527dc63c2fff3217d40ece1a7f8405a46aa3946f8d7f36f2d475eab21cc9"
ENTITY_PROMPTS_FILE = DATA_DIR / "entity_prompts.json"
ENTITY_PROMPTS_TOPUP_FILE = DATA_DIR / "entity_prompts_topup.json"
ENTITY_PROMPTS_MORE_DIR = DATA_DIR / "entity_prompts_more"  # round 3: part files, merged in name order


def load_pinned_items(path: Path, sha256: str) -> list[dict[str, Any]]:
    """`items` of a pinned JSON file; raises if the file no longer matches its pin."""
    blob = path.read_bytes()
    got = hashlib.sha256(blob).hexdigest()
    if got != sha256:
        raise ValueError(f"{path} sha256 {got} != pinned {sha256}")
    return json.loads(blob)["items"]


def probe_swap_items() -> list[dict[str, Any]]:
    return load_pinned_items(PROBE_SWAP_FILE, PROBE_SWAP_SHA256)


def brew_items() -> list[dict[str, Any]]:
    return load_pinned_items(BREW_FILE, BREW_SHA256)


def brew_fresh_items() -> list[dict[str, Any]]:
    return load_pinned_items(BREW_FRESH_FILE, BREW_FRESH_SHA256)


def brew_fit_items() -> list[dict[str, Any]]:
    return load_pinned_items(BREW_FIT_FILE, BREW_FIT_SHA256)


def bind_recall_items() -> list[dict[str, Any]]:
    return load_pinned_items(BIND_RECALL_FILE, BIND_RECALL_SHA256)


def bind_lookup_items() -> list[dict[str, Any]]:
    return load_pinned_items(BIND_LOOKUP_FILE, BIND_LOOKUP_SHA256)


def bind_lookup_v2_items() -> list[dict[str, Any]]:
    return load_pinned_items(BIND_LOOKUP_V2_FILE, BIND_LOOKUP_V2_SHA256)


def recall_lookup_items() -> list[dict[str, Any]]:
    return load_pinned_items(RECALL_LOOKUP_FILE, RECALL_LOOKUP_SHA256)


def use_source_items() -> list[dict[str, Any]]:
    return load_pinned_items(USE_SOURCE_FILE, USE_SOURCE_SHA256)


def brew_test_items() -> list[dict[str, Any]]:
    return load_pinned_items(BREW_TEST_FILE, BREW_TEST_SHA256)


def wikitext_rows() -> list[str]:
    return load_pinned_items(WIKITEXT_FILE, WIKITEXT_SHA256)  # type: ignore[return-value]


def lens_eval_multihop_items() -> list[dict[str, Any]]:
    return load_pinned_items(LENS_EVAL_MULTIHOP_FILE, LENS_EVAL_MULTIHOP_SHA256)


def natural_read_items() -> list[dict[str, Any]]:
    return load_pinned_items(NATURAL_READ_FILE, NATURAL_READ_SHA256)


def sha256_file(path: Path) -> str:
    """sha256 of a file, streamed (lens files are several GB)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()
