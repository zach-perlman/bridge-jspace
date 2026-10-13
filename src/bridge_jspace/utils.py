from __future__ import annotations

import json
import logging
import os
import random
import subprocess
from collections.abc import Iterable
from importlib import metadata

import numpy as np
import torch
from tqdm import tqdm


def progress[T](iterable: Iterable[T], desc: str, total: int | None = None) -> Iterable[T]:
    """tqdm bar with rate and ETA; redraws at most every 5 s so tee'd log files stay readable."""
    return tqdm(iterable, desc=desc, total=total, mininterval=5, dynamic_ncols=True)


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)  # noqa: NPY002 - third-party code uses the global RNG
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def git_state() -> dict[str, str | bool]:
    def _git(*args: str) -> str:
        return subprocess.run(["git", *args], capture_output=True, text=True, check=False).stdout.strip()

    return {"sha": _git("rev-parse", "HEAD"), "dirty": bool(_git("status", "--porcelain"))}


def package_versions() -> dict[str, str | None]:
    """Versions of the packages a result depends on; jlens also gets its git commit."""
    out: dict[str, str | None] = {}
    for name in ("torch", "transformers", "flash-linear-attention", "jlens", "numpy"):
        try:
            out[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            out[name] = None
    try:
        direct = json.loads(metadata.distribution("jlens").read_text("direct_url.json") or "{}")
        out["jlens_commit"] = direct.get("vcs_info", {}).get("commit_id")
    except metadata.PackageNotFoundError:
        out["jlens_commit"] = None
    out["torch_cuda"] = torch.version.cuda
    out["gpu"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    return out


def get_logger(name: str = "bridge_jspace") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", "%H:%M:%S"))
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
    return logger


def resolve_dtype(name: str) -> torch.dtype:
    dtypes = {"bfloat16": torch.bfloat16, "float16": torch.float16, "float32": torch.float32}
    if name not in dtypes:
        raise ValueError(f"Unsupported dtype {name!r}; expected one of {list(dtypes)}")
    return dtypes[name]
