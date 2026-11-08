"""One caption per figure (docs pass, 7 Nov): every figure set keeps its captions in figures/<set>/_meta/captions.toml,
keyed by the figure's file stem (a set is its folder under figures/, e.g. depth/ledger). A document template writes
`{{caption|<set>/<stem>}}` under the image (`{{caption|depth/ledger/01_item_not_answer}}`); the README
builders (scripts/readme_root.py, scripts/readme_build.py) expand it before their own placeholders, so the same PNG
has the same caption on every page. A caption may hold the builders' own placeholders and src comments.

The README pages (root, depth, breadth) take short captions (readability brief, 8 Nov: at most 60 words, takeaway
first) from figures/<set>/_meta/captions_short.toml through `{{caption_short|<set>/<stem>}}`; only the figures they
show have one."""

from __future__ import annotations

import json
import re
import tomllib
from functools import cache

from bridge_jspace.figkit.layout import FIGURES, META

# the set may hold slashes (depth/ledger): the greedy group gives the stem the last path part
PH = re.compile(r"\{\{caption(_short)?\|([\w/-]+)/([\w-]+)\}\}")
SHORT = "captions_short.toml"


def path(group: str, store: str = "captions.toml"):
    return FIGURES / group / META / store


@cache
def load(group: str, store: str = "captions.toml") -> dict[str, str]:
    p = path(group, store)
    return tomllib.loads(p.read_text()) if p.exists() else {}


def caption(group: str, stem: str, short: bool = False) -> str:
    store = SHORT if short else "captions.toml"
    try:
        return load(group, store)[stem]
    except KeyError:
        raise KeyError(f"no caption for figures/{group}/{stem}.png in {path(group, store)}") from None


def expand(text: str) -> str:
    """Every {{caption|set/stem}} and {{caption_short|set/stem}} as the italic caption line."""
    return PH.sub(lambda m: f"*{caption(m.group(2), m.group(3), bool(m.group(1)))}*", text)


def write(group: str, captions: dict[str, str]) -> None:
    """The set's caption file, in its figures' order (a TOML basic string per figure)."""
    from bridge_jspace.figkit.layout import names

    order = list(names(group).values())
    keys = sorted(captions, key=lambda k: order.index(k) if k in order else len(order))
    lines = ["# One caption per figure, keyed by its file stem (src/bridge_jspace/figkit/captions.py).", ""]
    lines += [f"{k} = {json.dumps(captions[k], ensure_ascii=False)}" for k in keys]
    path(group).write_text("\n".join(lines) + "\n")
    load.cache_clear()
