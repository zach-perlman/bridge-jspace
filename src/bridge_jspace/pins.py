"""Pinned external inputs and repo paths. Changing any pin needs a new manifest.

The QWEN_*/LENS_* constants are the Qwen3.6-27B + J-lens pins used by scripts/exp01-02 (part B);
configs/models/qwen3.6-27b.yaml repeats them for the YAML-configured experiments (part A), and
tests/test_pins.py checks the two agree.
"""

from __future__ import annotations

import hashlib
import json
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
LENS_SOURCES = {  # every J-format lens part B can load: name -> (repo, file, revision)
    "jlens": (LENS_REPO, LENS_FILE, LENS_REVISION),
    "jpp": (LENS_REPO, JPP_FILE, LENS_REVISION),
    "ws_jlens": (WS_LENS_REPO, "qwen3.6-27b/j-lens/lens.pt", WS_LENS_REVISION),
    "ws_rlens": (WS_LENS_REPO, "qwen3.6-27b/r-lens/lens.pt", WS_LENS_REVISION),
}
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
BIND_RECALL_FILE = DATA_DIR / "bind_recall.json"  # exp09_make_items.py: recalled vs bound bridge countries
BIND_RECALL_SHA256 = "89a8c62f4e9b43d328af7de0f7ba6994b53c187448767a916a5c3a5b97148204"
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


def wikitext_rows() -> list[str]:
    return load_pinned_items(WIKITEXT_FILE, WIKITEXT_SHA256)  # type: ignore[return-value]


def lens_eval_multihop_items() -> list[dict[str, Any]]:
    return load_pinned_items(LENS_EVAL_MULTIHOP_FILE, LENS_EVAL_MULTIHOP_SHA256)
