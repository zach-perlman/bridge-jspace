"""Example selection for exp11: groups by whether the J-lens reads the bridge at the last token, from ranks.jsonl."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from bridge_jspace.examples import Example, Group, load_jsonl, probe_swap_info, sample
from bridge_jspace.items import load_labelled_items, word_ids


def select(source_run: Path, p: dict[str, Any], tok) -> tuple[list[Group], list[Example]]:
    sp = json.loads((source_run / "manifest.json").read_text())["config"]["params"]
    items = {it["name"]: it for it in load_labelled_items(Path(sp["labels_file"]), sp["labels_sha256"])}
    meta = {m["name"]: m for m in load_jsonl(source_run / "items.jsonl")}
    rows = {(r["name"], r["reader"]): r for r in load_jsonl(source_run / "ranks.jsonl")}
    lo, hi = p["band"]

    def share(name: str, reader: str, role: str) -> float | None:
        r = rows.get((name, reader))
        if r is None or r[f"{role}_pool"] is None:
            return None
        band = [i for i, layer in enumerate(r["layers"]) if lo <= layer <= hi]
        return float(np.mean([r[f"{role}_pool"][i] == 1 for i in band]))

    seen = p.get("seen", 0.5)
    eligible = [n for n, m in meta.items() if m["status"] == "eligible"]
    j = {n: share(n, "jlens", "bridge") or 0.0 for n in meta}
    jp = {n: share(n, "jpp", "bridge") for n in meta}
    d = {n: share(n, "jlens", "distractor") or 0.0 for n in meta}
    defs = [
        ("seen_last", "Seen at the last token",
         f"Answered correctly; the J-lens has the bridge ranked first among the entities in >= {seen:.0%} of layers {lo}-{hi} at the last token.",
         [n for n in eligible if j[n] >= seen]),
        ("missed_last", "Missed at the last token",
         f"Answered correctly; the J-lens has the bridge ranked first among the entities in < {seen:.0%} of layers {lo}-{hi} at the last token.",
         [n for n in eligible if j[n] < seen]),
        ("distractor_wins", "Distractor above the bridge",
         "Answered correctly; the same-category distractor is ranked first among the entities in more band layers than the bridge.",
         [n for n in eligible if d[n] > j[n]]),
        ("readers_disagree", "J-lens and J++ disagree",
         "Answered correctly; the two lenses' band shares for the bridge differ by >= 0.5.",
         [n for n in eligible if (v := jp[n]) is not None and abs(j[n] - v) >= 0.5]),
        ("model_wrong", "Model answers wrong",
         "The model does not give the answer. Does the lens still see the bridge?",
         [n for n, m in meta.items() if m["status"] == "clean_wrong"]),
    ]  # fmt: skip
    groups, examples = [], []
    for key, title, definition, names in defs:
        groups.append(Group(key, title, definition, len(names)))
        for n in sample(names, p["per_group"], p["seed_examples"]):
            it = items[n]
            jpp = f"; J++ {jp[n]:.0%}" if jp[n] is not None else ""
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
                    why=f"J-lens bridge ranked first among the entities in {j[n]:.0%} of band layers at the last token, distractor {d[n]:.0%}{jpp}.",
                    info=probe_swap_info(it),
                )
            )
    return groups, examples
