"""Example selection for exp12: groups by where (and whether) the J-lens reads the bridge, from a run's saved grids.

A word "is read" at a position when it is top-1 in its pool in at least `seen` (default half) of the band layers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from bridge_jspace.examples import Example, Group, load_jsonl, sample
from bridge_jspace.items import load_labelled_items, word_ids
from scripts.exp12_position_map.experiment import load_grids


def item_stats(grids: dict, meta: dict, band_rows: list[int]) -> dict[str, dict[str, Any]]:
    """Per item: band share of the bridge / distractor top-1 at the true last token, and the bridge's best share at
    any earlier token."""
    out = {}
    for name, m in meta.items():
        g = grids.get(name)
        if g is None or "bridge_pool" not in g:
            continue
        b = (g["bridge_pool"][band_rows] == 1).mean(0)  # [positions]
        d = (g["distractor_pool"][band_rows] == 1).mean(0)
        earlier = b[:-1]
        best = int(np.argmax(earlier)) if earlier.size else None
        out[name] = {
            "last": float(b[-1]),
            "earlier_best": float(earlier.max()) if earlier.size else 0.0,
            "earlier_best_token": m["tokens"][best] if best is not None else "",
            "distractor_last": float(d[-1]),
        }
    return out


def select(source_run: Path, p: dict[str, Any], tok) -> tuple[list[Group], list[Example]]:
    manifest = json.loads((source_run / "manifest.json").read_text())
    sp = manifest["config"]["params"]
    items = {it["name"]: it for it in load_labelled_items(Path(sp["labels_file"]), sp["labels_sha256"])}
    meta = {m["name"]: m for m in load_jsonl(source_run / "items.jsonl")}
    layers = json.loads((source_run / "layers.json").read_text())
    lo, hi = p["band"]
    rows = {r: [i for i, layer in enumerate(layers[r]) if lo <= layer <= hi] for r in layers}
    js = item_stats(load_grids(source_run / "grids_jlens.npz"), meta, rows["jlens"])
    ps = item_stats(load_grids(source_run / "grids_jpp.npz"), meta, rows["jpp"]) if "jpp" in layers else {}
    seen = p.get("seen", 0.5)
    eligible = [n for n in meta if meta[n]["status"] == "eligible" and n in js]

    defs = [
        ("seen_last", "Seen at the last token",
         f"Eligible; the J-lens has the bridge top-1 in >= {seen:.0%} of layers {lo}-{hi} at the last token.",
         [n for n in eligible if js[n]["last"] >= seen]),
        ("seen_earlier", "Seen only earlier in the prompt",
         f"Eligible; missed at the last token (< {seen:.0%}) but on top at some earlier token (>= {seen:.0%}).",
         [n for n in eligible if js[n]["last"] < seen <= js[n]["earlier_best"]]),
        ("unseen", "Not seen anywhere",
         f"Eligible; the J-lens never has the bridge top-1 in >= {seen:.0%} of layers {lo}-{hi} at any token.",
         [n for n in eligible if max(js[n]["last"], js[n]["earlier_best"]) < seen]),
        ("distractor_wins", "Distractor above the bridge",
         "Eligible; at the last token the same-category distractor is top-1 in more band layers than the bridge.",
         [n for n in eligible if js[n]["distractor_last"] > js[n]["last"]]),
        ("readers_disagree", "J-lens and J++ disagree",
         "Eligible; at the last token the two lenses' band shares for the bridge differ by >= 0.5.",
         [n for n in eligible if n in ps and abs(js[n]["last"] - ps[n]["last"]) >= 0.5]),
        ("model_wrong", "Model answers wrong",
         "Part B's clean_wrong: the model's top word is not the answer. Does the lens still see the bridge?",
         [n for n in meta if meta[n]["status"] == "clean_wrong" and n in js]),
    ]  # fmt: skip
    groups, examples = [], []
    for key, title, definition, names in defs:
        groups.append(Group(key, title, definition, len(names)))
        for n in sample(names, p["per_group"], p["seed_examples"]):
            it, s = items[n], js[n]
            why = (
                f"J-lens bridge top-1 in {s['last']:.0%} of band layers at the last token, best earlier "
                f"{s['earlier_best']:.0%} (at `{s['earlier_best_token'].strip()}`), distractor {s['distractor_last']:.0%}"
                + (f"; J++ at the last token {ps[n]['last']:.0%}" if n in ps else "")
                + "."
            )
            examples.append(
                Example(
                    name=n,
                    group=key,
                    prompt=it["prompt"].rstrip() if sp["strip_trailing_space"] else it["prompt"],
                    words={
                        "bridge": it["intermediate"],
                        "answer": it["answer"],
                        "distractor": it["swap_to"],
                        "swap_answer": it["swap_answer"],
                    },
                    word_ids=word_ids(tok, it),
                    why=why,
                    info={"category": it["category"], "status (B)": it["status"], "label (B)": it["label"] or "-"},
                )
            )
    return groups, examples
