"""Example selection for exp10 (lens-eval multihop): groups by which readers have the bridge in their top 10 at the last
token at some layer (exp10's pass@10; a bridge listed in several forms counts if any form is), and by what the bridge
is (a number, a letter, named in the prompt), from multihop_ranks.jsonl. Single-token bridges only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bridge_jspace.examples import Example, Group, load_jsonl, sample
from bridge_jspace.pins import lens_eval_multihop_items
from bridge_jspace.readout import word_tokens
from scripts.exp10_lens_sanity.experiment import bridge_in_prompt, bridge_kind


def select(source_run: Path, p: dict[str, Any], tok) -> tuple[list[Group], list[Example]]:
    sp = json.loads((source_run / "manifest.json").read_text())["config"]["params"]
    items = {it["name"]: it for it in lens_eval_multihop_items()}
    meta = {m["name"]: m for m in load_jsonl(source_run / "multihop_items.jsonl")}
    best: dict[str, dict[str, int]] = {}  # name -> reader -> min rank over the bridge's forms
    for r in load_jsonl(source_run / "multihop_ranks.jsonl"):
        if meta[r["name"]]["all_single_token"]:
            b = best.setdefault(r["name"], {})
            b[r["reader"]] = min(b.get(r["reader"], r["min_rank"]), r["min_rank"])
    k = p.get("k", 10)
    hit = {n: {rd: v < k for rd, v in b.items()} for n, b in best.items()}
    names = sorted(hit)
    defs = [
        ("all_see", "All readers see it", f"Logit lens, J-lens and J++ all have the intermediate in their top {k}.",
         [n for n in names if all(hit[n].values())]),
        ("lenses_only", "Only the lenses see it", f"J-lens or J++ in their top {k}, the logit lens not.",
         [n for n in names if not hit[n]["logit"] and (hit[n].get("jlens") or hit[n].get("jpp"))]),
        ("jpp_not_jlens", "J++ sees it, the J-lens does not", f"J++ in its top {k}, the J-lens not.",
         [n for n in names if hit[n].get("jpp") and not hit[n].get("jlens")]),
        ("none_see", "No reader sees it", f"No reader has the intermediate in its top {k} at any layer.",
         [n for n in names if not any(hit[n].values())]),
        ("model_wrong", "Model answers wrong", "The model's greedy next token is not the target's first token.",
         [n for n in names if not meta[n]["model_correct"]]),
        ("number_bridge", "The bridge is a number", "A form of the bridge is a numeral or a number word ('6', 'four', "
         "'third'): the lenses read these worse than the logit lens.",
         [n for n in names if bridge_kind(items[n]["intermediates"]) == "number"]),
        ("letter_bridge", "The bridge is a letter", "Every form of the bridge is one letter (a chemical symbol).",
         [n for n in names if bridge_kind(items[n]["intermediates"]) == "letter"]),
        ("bridge_in_prompt", "The prompt names the bridge", "A form of the bridge is written in the prompt as a word.",
         [n for n in names if bridge_in_prompt(items[n]["prompt"], items[n]["intermediates"])]),
    ]  # fmt: skip
    groups, examples = [], []
    for key, title, definition, members in defs:
        groups.append(Group(key, title, definition, len(members)))
        for n in sample(members, p["per_group"], p["seed_examples"]):
            it = items[n]
            bridge, answer = it["intermediates"][0], it["target"]
            ranks = ", ".join(f"{rd} {v}" for rd, v in best[n].items())
            examples.append(
                Example(
                    name=n,
                    group=key,
                    prompt=it["prompt"].rstrip() if sp["strip_trailing_space"] else it["prompt"],
                    words={"bridge": bridge, "answer": answer},
                    word_ids={
                        "bridge": list(word_tokens(tok, bridge).ids),
                        "answer": list(word_tokens(tok, answer).ids),
                    },
                    why=f"best rank over layers at the last token: {ranks} (0 = top).",
                    info={"other intermediates": ", ".join(it["intermediates"][1:]) or "-"},
                )
            )
    return groups, examples
