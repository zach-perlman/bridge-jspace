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
LENS_REVISION = "9fa267f841d62aa468dab5b9b38c3dc45a82d863"
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
    # Qwen3-32B (dense: softmax attention in all 64 layers; Qwen3 family, no DeltaNet), 22 Oct. Its lens (22 Oct, for D1 on
    # a second model): neuronpedia's plain J-lens (NOT J++; none is published for this model), fit on Qwen/Qwen3-32B with
    # the jlens recipe on 557 wikitext-103 prompts. Their note: the fit did not reach its stopping threshold (relative
    # standard error of the mean Jacobian ~13%, ~5% for their other lenses), so runs on this target must pass their own
    # positive control before a lens result counts. Key "jlens", named by "frozen_lens" as on OLMo; sha256 checked on load.
    "qwen3-32b": {
        "repo": "Qwen/Qwen3-32B",
        "revision": "9216db5781bf21249d130ec9da846c4624c16137",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "qwen3_32b_",
        "frozen_lens": "jlens",
        "lenses": {
            "jlens": (
                LENS_REPO,
                "qwen3-32b/jlens/Salesforce-wikitext/Qwen3-32B_jacobian_lens.pt",
                "e166deb5ad540932100ef803c8c9bcc2a5453694",
            ),
        },
        "frozen_lens_sha256": "0af5ccf2e1c251bedc202607a7ca214f3b9f60980bab73d67a3d0b887db213d8",
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
    # Qwen3.6-27B read with neuronpedia's plain J-lens (n1000) instead of J++: the within-model lens-type control (Dan,
    # 22 Oct night; Qwen3-32B and OLMo have plain J-lenses only). Same weights; the file exists from repo revision
    # e166deb5 on (absent at 9fa267f8); sha256 computed on the box.
    "qwen3.6-27b-jlens": {
        "repo": "Qwen/Qwen3.6-27B",
        "revision": "6a9e13bd6fc8f0983b9b99948120bc37f49c13e9",
        "n_layers": 64,
        "norm_gain": "one_plus_weight",
        "bos": False,
        "run_prefix": "qwen36_27b_jlens_",
        "frozen_lens": "jlens",
        "lenses": {
            "jlens": (
                "neuronpedia/jacobian-lens",
                "qwen3.6-27b/jlens/Salesforce-wikitext/Qwen3.6-27B_jacobian_lens_n1000.pt",
                "e166deb5ad540932100ef803c8c9bcc2a5453694",
            ),
        },
        "frozen_lens_sha256": "1718c8c52dd8a9dad03738d4d625937c1fbba10be325b872ed446c7290fc11e1",
    },
    # Muse Glimmer 30B (Meta, Apache 2.0; 22 Oct night, Dan): dense, 52 layers, sliding-window (2048) attention with a
    # full-attention layer every 4th, a multimodal checkpoint (MuseGlimmerForConditionalGeneration; the text decoder is
    # hf.model.language_model, transformers' own muse_glimmer), centered RMSNorm with a 1 + weight gain, <|begin_of_text|>.
    # Lens: Zach's J++ (zachperlman20/Muse-Glimmer-30B-jpp-lens, published 22 Oct night; source layers 0-50, fp16, cast
    # to fp32 by JLens.J; sha256 90fc5e52..., as Dan passed it on and as computed on the box). Zach's caveats: fit on 32
    # prompts, evaluated on 112 items, weak in the middle layers; its gate (lens_gate v1 / v2) decides whether D1 runs.
    "muse-glimmer-30b": {
        "repo": "meta-models/Muse-Glimmer-30B",
        "revision": "cec94fcfd6512f2cfe708138c32533b346ea4f69",
        "n_layers": 52,
        "norm_gain": "one_plus_weight",
        "bos": True,
        "run_prefix": "muse30b_",
        "lenses": {
            "jpp": (
                "zachperlman20/Muse-Glimmer-30B-jpp-lens",
                "Muse-Glimmer-30B_jpp_lens.pt",
                "68ecd838ad0b13653af7fac985995606f37911dc",
            ),
        },
        "frozen_lens_sha256": "90fc5e52e8d765b729c4f894273fec5084fd3030db38b1b9b187cf67a1df8a12",
    },
    # Gemma 4 31B-it with Zach's J++ fit at every layer 0-58 (target 59), published 22 Oct 2026 on the Hub (his gate:
    # 0.5284, PASS at layers 24-45). fp16 maps, cast to fp32 when used (JLens.J). Named as on his branch.
    "gemma-4-31b-it-full": {
        "repo": "google/gemma-4-31B-it",
        "revision": "842da3794eaa0b77d5f08bae87a17459d91ff475",
        "n_layers": 60,
        "norm_gain": "weight",
        "bos": True,
        "run_prefix": "gemma4itf_",
        "lenses": {
            "jpp": (
                "zachperlman20/gemma-4-31B-it-jpp-lens",
                "gemma-4-31B-it_jpp_lens.pt",
                "c3c4340e81e249f1ad7bc71b5db710cc0349cd76",
            ),
        },
        "frozen_lens_sha256": "d16d81d8751ad69df3493c0b3ea7410da97f69abfb07ee115600ad21ef9ef30a",
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


def model_pin() -> dict[str, str]:
    """The target model as manifests record it, with the prompt format (chat.FORMAT, BJ_FORMAT) its prompts use."""
    from bridge_jspace import chat

    return {"target": TARGET, "repo": MODEL_REPO, "revision": MODEL_REVISION, "dtype": "bfloat16", "attn": "sdpa",
            "prompt_format": chat.FORMAT}  # fmt: skip


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


def sha256_file(path: Path) -> str:
    """sha256 of a file, streamed (lens files are several GB)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()
