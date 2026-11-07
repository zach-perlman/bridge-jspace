"""One caption per figure (docs pass, 7 Nov): every figure set keeps its captions in figures/<set>/_meta/captions.toml,
keyed by the figure's file stem. A document template writes `{{caption|<set>/<stem>}}` under the image; the README
builders (scripts/readme_root.py, scripts/readme_build.py) expand it before their own placeholders, so the same PNG
has the same caption on every page. A caption may hold the builders' own placeholders and src comments."""

from __future__ import annotations

import json
import re
import tomllib
from functools import cache

from bridge_jspace.figkit.layout import FIGURES, META

PH = re.compile(r"\{\{caption\|([\w-]+)/([\w-]+)\}\}")


def path(group: str):
    return FIGURES / group / META / "captions.toml"


@cache
def load(group: str) -> dict[str, str]:
    p = path(group)
    return tomllib.loads(p.read_text()) if p.exists() else {}


def caption(group: str, stem: str) -> str:
    try:
        return load(group)[stem]
    except KeyError:
        raise KeyError(f"no caption for figures/{group}/{stem}.png in {path(group)}") from None


def expand(text: str) -> str:
    """Every {{caption|set/stem}} as the italic caption line."""
    return PH.sub(lambda m: f"*{caption(m.group(1), m.group(2))}*", text)


def write(group: str, captions: dict[str, str]) -> None:
    """The set's caption file, in its figures' order (a TOML basic string per figure)."""
    from bridge_jspace.figkit.layout import names

    order = list(names(group).values())
    keys = sorted(captions, key=lambda k: order.index(k) if k in order else len(order))
    lines = ["# One caption per figure, keyed by its file stem (src/bridge_jspace/figkit/captions.py).", ""]
    lines += [f"{k} = {json.dumps(captions[k], ensure_ascii=False)}" for k in keys]
    path(group).write_text("\n".join(lines) + "\n")
    load.cache_clear()
