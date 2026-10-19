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
# on load (lens.py), so a changed upload cannot slip in under the same name.
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
}
TARGET = os.environ.get("BJ_TARGET", "qwen3.6-27b")
assert TARGET in TARGETS, f"BJ_TARGET={TARGET!r}: not one of {sorted(TARGETS)}"
MODEL_REPO: str = TARGETS[TARGET]["repo"]
MODEL_REVISION: str = TARGETS[TARGET]["revision"]
N_LAYERS: int = TARGETS[TARGET]["n_layers"]
RUN_PREFIX: str = TARGETS[TARGET]["run_prefix"]
if TARGET != "qwen3.6-27b":
    CACHE_DIR = REPO_ROOT / "cache" / TARGET
    LENS_SOURCES = TARGETS[TARGET]["lenses"]


def model_pin() -> dict[str, str]:
    """The target model as manifests record it."""
    return {"target": TARGET, "repo": MODEL_REPO, "revision": MODEL_REVISION, "dtype": "bfloat16", "attn": "sdpa"}


def check_run_name(name: str) -> None:
    """A run of a non-default target is named with its prefix, so its results never pass for Qwen's."""
    assert name.startswith(RUN_PREFIX), f"BJ_TARGET={TARGET}: run names start with {RUN_PREFIX!r}, got {name!r}"


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
