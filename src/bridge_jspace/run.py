"""CLI: `uv run bj-run scripts/<exp>/config.yaml [key.sub=value ...]`."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from bridge_jspace.config import load_config
from bridge_jspace.experiment import Experiment


def import_object(path: str) -> Any:
    module, sep, attr = path.partition(":")
    if not sep:
        raise ValueError(f"Expected 'module:attr', got {path!r}")
    obj: Any = importlib.import_module(module)
    for part in attr.split("."):
        obj = getattr(obj, part)
    return obj


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config")
    ap.add_argument("overrides", nargs="*", help="dotted overrides, e.g. model=configs/models/qwen3.6-27b.yaml")
    args = ap.parse_args(argv)

    load_dotenv()
    # Make `scripts.*` importable when running from the repo root.
    sys.path.insert(0, str(Path.cwd()))
    cfg = load_config(args.config, args.overrides)
    cls = import_object(cfg.target)
    if not (isinstance(cls, type) and issubclass(cls, Experiment)):
        raise TypeError(f"{cfg.target} is not an Experiment subclass")
    cls(cfg).execute()


if __name__ == "__main__":
    main()
