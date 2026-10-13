"""Pinned external data and repo paths. Changing any pin needs a new manifest.

Model and lens pins (repo, revision, file) live in configs/models/*.yaml.
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

PROBE_SWAP_FILE = DATA_DIR / "probe_swap.json"
PROBE_SWAP_SHA256 = "a0edd27ca23f7b4d0fbe90448c2ddcc7457a3d812121bf024ed12a032ff86796"
LENS_EVAL_MULTIHOP_FILE = DATA_DIR / "lens_eval_multihop.json"
LENS_EVAL_MULTIHOP_SHA256 = "50b7e4c9255291c0ca2a8e94615be9f44531fa57bb1a844e4f9616056d987416"
ENTITY_PROMPTS_FILE = DATA_DIR / "entity_prompts.json"


def load_pinned_items(path: Path, sha256: str) -> list[dict[str, Any]]:
    """`items` of a pinned JSON file; raises if the file no longer matches its pin."""
    blob = path.read_bytes()
    got = hashlib.sha256(blob).hexdigest()
    if got != sha256:
        raise ValueError(f"{path} sha256 {got} != pinned {sha256}")
    return json.loads(blob)["items"]


def probe_swap_items() -> list[dict[str, Any]]:
    return load_pinned_items(PROBE_SWAP_FILE, PROBE_SWAP_SHA256)


def lens_eval_multihop_items() -> list[dict[str, Any]]:
    return load_pinned_items(LENS_EVAL_MULTIHOP_FILE, LENS_EVAL_MULTIHOP_SHA256)
