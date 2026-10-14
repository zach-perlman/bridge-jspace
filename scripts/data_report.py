"""What data we work with, recomputed from the files: `make data-report`.

Reads every dataset through the same sha256-checked loaders the experiments use, so the numbers printed here are
the numbers the experiments see. data/README.md explains each dataset; this script keeps its counts honest.
"""

from __future__ import annotations

import json
import statistics
from collections import Counter
from typing import Any

import yaml

from bridge_jspace.config import load_config
from bridge_jspace.items import load_labelled_items
from bridge_jspace.pins import REPO_ROOT, RESULTS_DIR, lens_eval_multihop_items

EXP11_CONFIG = REPO_ROOT / "scripts/exp11_bridge_vs_answer_by_layer/config.yaml"
EXP01_FILTER = RESULTS_DIR / "exp01_probes/v3/filter.jsonl"


def probe_swap_report(items: list[dict[str, Any]]) -> dict[str, Any]:
    """`items` are probe-swap items joined with part B's labels (status, label)."""
    cats = Counter(i["category"] for i in items)
    eligible = [i for i in items if i["status"] == "eligible"]
    bridges = Counter(i["intermediate"] for i in items)
    return {
        "n": len(items),
        "n_categories": len(cats),
        "category_sizes": dict(cats.most_common()),
        "categories_with_one_item": sum(v == 1 for v in cats.values()),
        "unique_bridges": len(bridges),
        "bridges_used_more_than_once": {k: v for k, v in bridges.most_common() if v > 1},
        "unique_answers": len({i["answer"] for i in items}),
        "prompts_ending_in_space": sum(i["prompt"].endswith(" ") for i in items),
        "status": dict(Counter(i["status"] for i in items).most_common()),
        "eligible": {
            "n": len(eligible),
            "n_categories": len({i["category"] for i in eligible}),
            "multihop_category": sum(i["category"] == "multihop" for i in eligible),
            "ending_in_space": sum(i["prompt"].endswith(" ") for i in eligible),
            "labels": dict(Counter(i["label"] for i in eligible).most_common()),
            "j_mediated_by_category": dict(
                Counter(i["category"] for i in eligible if i["label"] == "J-mediated").most_common()
            ),
        },
    }


def lens_eval_report(lens_eval: list[dict[str, Any]], probe_swap: list[dict[str, Any]]) -> dict[str, Any]:
    ps_prompts = {i["prompt"].strip() for i in probe_swap}
    ps_bridges = {i["intermediate"] for i in probe_swap}
    n_inter = Counter(len(i["intermediates"]) for i in lens_eval)
    return {
        "n": len(lens_eval),
        "intermediates_per_item": dict(sorted(n_inter.items())),
        "prompts_ending_in_space": sum(i["prompt"].endswith(" ") for i in lens_eval),
        "same_prompt_as_probe_swap": sum(i["prompt"].strip() in ps_prompts for i in lens_eval),
        "intermediate_word_in_prompt": sum(
            any(w.lower() in i["prompt"].lower() for w in i["intermediates"]) for i in lens_eval
        ),
        "bridges_shared_with_probe_swap": len({w for i in lens_eval for w in i["intermediates"]} & ps_bridges),
    }


def entity_prompts_report(filter_rows: list[dict[str, Any]] | None) -> dict[str, Any]:
    """Prompt files per round, and (if exp01 v3 ran) how many prompts per entity Qwen answered and the probe used."""
    from bridge_jspace import pins

    files = [
        pins.ENTITY_PROMPTS_FILE,
        pins.ENTITY_PROMPTS_TOPUP_FILE,
        *sorted(pins.ENTITY_PROMPTS_MORE_DIR.glob("*.json")),
    ]
    per_file = {}
    per_entity: Counter[str] = Counter()
    for f in files:
        d = json.loads(f.read_text())
        ents = d["entities"]
        per_file[str(f.relative_to(REPO_ROOT))] = {
            "round": d["meta"].get("round", 1),
            "entities": len(ents),
            "prompts": sum(len(v) for v in ents.values()),
        }
        for e, rows in ents.items():
            per_entity[e] += len(rows)
    out: dict[str, Any] = {
        "files": per_file,
        "entities": len(per_entity),
        "prompts": sum(per_entity.values()),
        "prompts_per_entity": _spread(list(per_entity.values())),
    }
    if filter_rows is not None:
        kept = Counter(r["entity"] for r in filter_rows if r["kept"])
        out["exp01_v3_filter"] = {
            "prompts_checked": len(filter_rows),
            "kept": sum(kept.values()),
            "kept_per_entity": _spread([kept.get(e, 0) for e in per_entity]),
            "entities_with_fewer_than_3_kept": sorted(e for e in per_entity if kept.get(e, 0) < 3),
        }
    return out


def lenses_report() -> dict[str, Any]:
    """Lens files per model config (fitting corpus and size are documented in data/README.md)."""
    out = {}
    for f in sorted((REPO_ROOT / "configs/models").glob("*.yaml")):
        m = yaml.safe_load(f.read_text())
        out[m["name"]] = {name: lens["filename"].split("/")[-1] for name, lens in m.get("lenses", {}).items()}
    return out


def _spread(xs: list[int]) -> dict[str, float]:
    return {"min": min(xs), "median": statistics.median(xs), "max": max(xs)} if xs else {}


def build_report() -> dict[str, Any]:
    p = load_config(EXP11_CONFIG).params
    probe_swap = load_labelled_items(REPO_ROOT / p["labels_file"], p["labels_sha256"])
    filter_rows = (
        [json.loads(x) for x in EXP01_FILTER.read_text().splitlines() if x.strip()] if EXP01_FILTER.exists() else None
    )
    return {
        "probe_swap": probe_swap_report(probe_swap),
        "lens_eval_multihop": lens_eval_report(lens_eval_multihop_items(), probe_swap),
        "entity_prompts": entity_prompts_report(filter_rows),
        "lenses": lenses_report(),
    }


def format_report(r: dict[str, Any]) -> str:
    ps, le, ep = r["probe_swap"], r["lens_eval_multihop"], r["entity_prompts"]
    el = ps["eligible"]
    lines = [
        "== probe-swap two-hop items (data/probe_swap.json + part B labels) — exp02, exp11, exp12",
        f"items {ps['n']} in {ps['n_categories']} categories ({ps['categories_with_one_item']} with a single item); "
        f"{ps['unique_bridges']} unique bridges, {ps['unique_answers']} unique answers; "
        f"{ps['prompts_ending_in_space']} prompts end in a space",
        f"category sizes: {_fmt(ps['category_sizes'])}",
        f"bridges used more than once: {_fmt(ps['bridges_used_more_than_once'])}",
        f"status (part B): {_fmt(ps['status'])}",
        f"eligible {el['n']} in {el['n_categories']} categories ({el['multihop_category']} in 'multihop'; "
        f"{el['ending_in_space']} end in a space)",
        f"eligible labels (part B exp02 main): {_fmt(el['labels'])}",
        f"J-mediated by category: {_fmt(el['j_mediated_by_category'])}",
        "",
        "== lens-eval multihop (data/lens_eval_multihop.json) — exp10",
        f"items {le['n']}; intermediates per item {_fmt(le['intermediates_per_item'])}; "
        f"{le['prompts_ending_in_space']} prompts end in a space",
        f"overlap with probe-swap: {le['same_prompt_as_probe_swap']} identical prompts, "
        f"{le['bridges_shared_with_probe_swap']} shared bridges; "
        f"{le['intermediate_word_in_prompt']} prompts contain their intermediate word",
        "",
        "== entity prompts (data/entity_prompts*.json) — part B probes, exp01",
        f"{ep['entities']} entities, {ep['prompts']} prompts; per entity {_fmt(ep['prompts_per_entity'])}",
        *[
            f"  {f}: round {v['round']}, {v['entities']} entities, {v['prompts']} prompts"
            for f, v in ep["files"].items()
        ],
    ]
    if "exp01_v3_filter" in ep:
        fl = ep["exp01_v3_filter"]
        lines.append(
            f"exp01 v3 filter: {fl['kept']} of {fl['prompts_checked']} prompts kept (Qwen answered as expected); "
            f"kept per entity {_fmt(fl['kept_per_entity'])}; fewer than 3 kept: {fl['entities_with_fewer_than_3_kept'] or 'none'}"
        )
    lines += ["", "== lens files per model config (fitting data: data/README.md)"]
    lines += [f"  {m}: {_fmt(v) or '-'}" for m, v in r["lenses"].items()]
    return "\n".join(lines)


def _fmt(d: dict[str, Any]) -> str:
    return ", ".join(f"{k} {v}" for k, v in d.items())


if __name__ == "__main__":
    import sys

    report = build_report()
    print(json.dumps(report, indent=2) if sys.argv[1:] == ["--json"] else format_report(report))
