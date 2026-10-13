"""Experiment base class: one config in, one never-overwritten run directory out.

Run dir layout: results/<exp id>/<timestamp>/
    manifest.json  written BEFORE run(): resolved config, git sha/dirty, packages, argv, seed
    summary.json   headline numbers returned by run()
    *.jsonl, ...   raw per-item outputs written via self.save_*
"""

from __future__ import annotations

import json
import platform
import sys
import time
from abc import ABC, abstractmethod
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Any

from jlens import JacobianLens

from bridge_jspace.config import ExperimentConfig
from bridge_jspace.models import LoadedModel, load_lens, load_model
from bridge_jspace.utils import get_logger, git_state, package_versions, seed_everything


class Experiment(ABC):
    def __init__(self, cfg: ExperimentConfig, run_dir: str | Path | None = None):
        self.cfg = cfg
        self.params = cfg.params
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.run_dir = Path(run_dir or Path(cfg.results_dir) / cfg.name / stamp)
        self.log = get_logger(cfg.name)

    # ---- lazily built components (only what the experiment touches gets loaded) -------------

    @cached_property
    def model(self) -> LoadedModel:
        self.log.info(f"loading {self.cfg.model.name}@{self.cfg.model.revision[:8]}")
        return load_model(self.cfg.model)

    @cached_property
    def lenses(self) -> dict[str, JacobianLens]:
        """Configured lenses by reader name, maps already on the model's device."""
        lm = self.model.lm
        out = {}
        for name, lc in self.cfg.model.lenses.items():
            self.log.info(f"loading lens {name}: {lc.filename}")
            out[name] = load_lens(lc, lm.n_layers, lm.d_model, self.model.device)
        return out

    # ---- outputs ----------------------------------------------------------------------------

    def path(self, name: str) -> Path:
        return self.run_dir / name

    def save_jsonl(self, name: str, rows: list[dict[str, Any]]) -> Path:
        p = self.path(name)
        with p.open("w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
        self.log.info(f"wrote {len(rows)} rows -> {p}")
        return p

    def save_json(self, name: str, obj: Any) -> Path:
        p = self.path(name)
        p.write_text(json.dumps(obj, indent=2, default=str, ensure_ascii=False))
        return p

    # ---- lifecycle --------------------------------------------------------------------------

    def setup(self) -> None:
        seed_everything(self.cfg.seed)
        self.run_dir.mkdir(parents=True, exist_ok=False)  # never overwrite a run
        git = git_state()
        if git["dirty"]:
            self.log.warning("git tree is dirty: the manifest sha does not fully describe this run")
        self.save_json(
            "manifest.json",
            {
                "exp_id": self.cfg.name,
                "config": self.cfg.model_dump(),
                "git": git,
                "packages": package_versions(),
                "host": platform.node(),
                "python": sys.version.split()[0],
                "argv": sys.argv,
                "started": datetime.now().isoformat(timespec="seconds"),
            },
        )
        self._t0 = time.time()
        self.log.info(f"run dir: {self.run_dir}")

    @abstractmethod
    def run(self) -> dict[str, Any] | None:
        """Do the work; return summary metrics (saved to summary.json)."""

    def execute(self) -> dict[str, Any] | None:
        self.setup()
        summary = self.run()
        if summary is not None:
            self.save_json("summary.json", summary)
        self.log.info(f"done in {time.time() - self._t0:.1f}s -> {self.run_dir}")
        return summary
