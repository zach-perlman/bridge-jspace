"""Typed experiment configs loaded from YAML, with dotted CLI overrides.

Method-specific knobs go in `params` (free-form) so new experiments don't require touching this file.
Promote a knob to a typed field only once several experiments share it.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator

EXP_ID = re.compile(r"^exp\d{2}_[a-z0-9_]+$")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LensConfig(_Strict):
    repo: str = "neuronpedia/jacobian-lens"
    revision: str
    filename: str


class ModelConfig(_Strict):
    name: str
    revision: str  # pinned: a model change needs a new manifest
    dtype: str = "bfloat16"
    device_map: str = "auto"
    # Reader name -> lens file, e.g. {"jlens": ..., "jpp": ...}. The logit lens needs no file.
    lenses: dict[str, LensConfig] = Field(default_factory=dict)


class ExperimentConfig(_Strict):
    name: str  # experiment id, expNN_name
    target: str  # "module:Class" of the Experiment subclass
    seed: int = 0
    results_dir: str = "results"
    model: ModelConfig
    params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def _exp_id(cls, v: str) -> str:
        if not EXP_ID.match(v):
            raise ValueError(f"experiment name must look like expNN_name, got {v!r}")
        return v


def _set_dotted(d: dict[str, Any], key: str, value: Any) -> None:
    *parents, leaf = key.split(".")
    for p in parents:
        d = d.setdefault(p, {})
        if not isinstance(d, dict):
            raise ValueError(f"Override {key!r}: {p!r} is not a mapping")
    d[leaf] = value


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def load_config(path: str | Path, overrides: list[str] | None = None) -> ExperimentConfig:
    """Load YAML config with dotted overrides (`a.b.c=value`, values parsed as YAML).

    `model:` may be a path to a model YAML (relative to cwd, else to the config file), and
    `model=<path>` on the CLI swaps the whole model before `model.x=...` overrides apply.
    """
    path = Path(path)
    raw = _load_yaml(path)
    parsed = []
    for ov in overrides or []:
        key, sep, val = ov.partition("=")
        if not sep:
            raise ValueError(f"Override must be key=value, got {ov!r}")
        parsed.append((key.strip(), yaml.safe_load(val)))
    for key, val in parsed:
        if key == "model":
            raw["model"] = val
    if isinstance(raw.get("model"), str):
        mpath = Path(raw["model"])
        if not mpath.exists():
            mpath = path.parent / mpath
        raw["model"] = _load_yaml(mpath)
    for key, val in parsed:
        if key != "model":
            _set_dotted(raw, key, val)
    return ExperimentConfig.model_validate(raw)
