"""exp04_brew_positions: which positions after the start line does brew's second lookup read the intermediate from?

exp04's window copy (C's activations at all 21 positions after the start line, one layer of 36-50 at a time) makes the
model answer f(X). exp08 found the lenses read the intermediate at only a few of those positions, from layer 36: the
newline after "assistant" (position 14), the "\\n\\n" after "</think>" (18), and less so "the" (4) and the last token
":" (20). This run copies C's activations at a subset of the positions only, lens-free, as exp04:

  all               the 21 positions (reproduces exp04's full copy)
  reading           4, 14, 18, 20: where exp08's lenses read I
  all_but_reading   the other 17
  assistant_nl      14 alone
  think_nl          18 alone
Control: the off-path counterfactual O's copy at the same positions (reading, assistant_nl, think_nl). Items: the bank
and fresh items eligible as in exp04. Per item, a copy's step score is the share of window layers giving f(X).

Stages (the manifest is written before the run and is write-once):
  manifest --name N --why "..."
  run N
"""

import argparse
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import paired_bootstrap_diff, wilson
from scripts.exp03_brew_swaps import ITEM_SETS, MAX_NEW_TOKENS, answer_colour, regime_positions, spans, write_jsonl
from scripts.exp04_brew_parts import AddRows
from scripts.exp04_brew_patch import EXP, RESULTS, SOURCES, category, prepare
from scripts.exp07_step_code import MAPS, PARTS_RUNS, WINDOW

TEST_SETS = ("fresh", "bank")
# exp08: where the lenses read I (indices into the 21 positions after the start line), on Qwen3.6-27B. Another
# target's come from its own exp08 run.
READING: tuple[int, ...] = {"qwen3.6-27b": (4, 14, 18, 20)}.get(pins.TARGET, ())
GROUPS = {
    "all": tuple(range(21)),
    "reading": READING,
    "all_but_reading": tuple(i for i in range(21) if i not in READING),
    "assistant_nl": (14,),
    "think_nl": (18,),
}
CONTROLLED = ("reading", "assistant_nl", "think_nl")  # groups also copied from O
N_BOOT, BOOT_SEED = 2000, 0


def stage_manifest(name: str, why: str) -> None:
    from bridge_jspace.tokens import load_tokenizer
    from scripts.exp07_step_code import tokenized

    pins.check_run_name(name)
    assert READING, f"no exp08 reading positions for {pins.TARGET} yet"
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    maps = {}
    for run in MAPS:
        summary = RESULTS / run / "summary.json"
        window = json.loads(summary.read_text())["decision"]["windows"]["after_start"]
        assert tuple(window) == WINDOW, f"{run}'s window {window} is not {WINDOW}"
        maps[run] = {"summary_sha256": sha256_of(summary), "window_after_start": window}
    tokenizer = load_tokenizer()
    ids, positions = tokenized(tokenizer, ITEM_SETS["fresh"][2]()[0])
    labels = [tokenizer.decode([ids[p]]) for p in positions]
    manifest = {
        "exp": EXP,
        "run": name,
        "kind": "patch_positions",
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": "Copying the counterfactual's activations at which positions after the start line makes the model "
        "take X as the step: the positions where exp08's lenses read the intermediate, or the others?",
        "why": why,
        "model": pins.model_pin(),
        "items": {
            s: {"file": str(ITEM_SETS[s][0].relative_to(pins.REPO_ROOT)), "sha256": ITEM_SETS[s][1]} for s in TEST_SETS
        },
        "eligibility": "as exp04 (B answers A, C answers c, O answers A; C and O token-aligned with B)",
        "window": {"layers": list(WINDOW), "maps": maps},
        "positions": {"tokens after the start line": labels, "groups": {g: list(p) for g, p in GROUPS.items()}},
        "groups_from": "exp08_brew_read/read_v1: J++ and the J-lens rank I first of the 12 colours at positions 14 and 18 "
        "(and less at 4 and 20) from layer 36, on the same items",
        "copy": "δ = h_C - h_B at the group's positions only, one window layer at a time (exp04's copy restricted)",
        "controls": "the off-path counterfactual O's copy at the same positions, for " + ", ".join(CONTROLLED),
        "outcome": "the continuation's first palette colour as a role, as exp04 (b = f(X), c, X, I, A, ...)",
        "decision": {
            "step_score": "per item, the share of window layers at which the copy gives f(X); differences are paired "
            "bootstraps over items (95%)",
            "carries": "fresh items primary, bank replication: a group alone carries the step if its C copy's step "
            "score exceeds its O copy's (CI above 0), for each of " + ", ".join(CONTROLLED),
            "needed": "the reading positions are needed if all - all_but_reading is above 0 (CI)",
            "reproduce": "'all' must reproduce exp04's full-copy rows (parts_window_fresh, parts_window) item for item",
        },
        "deviations": [
            "The groups were chosen from exp08's readouts on the same items; this run tests them causally.",
            "Each window layer is copied on its own, as in exp04.",
        ],
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


@torch.no_grad()
def stage_run(name: str) -> None:
    from bridge_jspace.model import load_model

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "outcomes.jsonl").exists(), f"{out_dir} already has results; results are write-once"
    for run, info in manifest["window"]["maps"].items():
        assert sha256_of(RESULTS / run / "summary.json") == info["summary_sha256"], f"{run} changed since the manifest"
    model = load_model()
    tokenizer: Any = model.tokenizer
    cases, item_rows = [], []
    for set_name in TEST_SETS:
        item_file, _, load_items = ITEM_SETS[set_name]
        assert sha256_of(item_file) == manifest["items"][set_name]["sha256"], f"{set_name} items changed"
        items = load_items()
        palette = sorted({c for it in items for c in it["table"]} | {it["answer"] for it in items})
        for index, item in enumerate(items):
            prep = prepare(item, index, tokenizer)
            row: dict[str, Any] = {"set": set_name, "name": item["name"], "status": prep["status"]}
            item_rows.append(row)
            if prep["status"] != "ok":
                continue
            cfs = prep["cfs"]
            ids = torch.tensor([prep["ids"]], device="cuda")
            source_ids = {s: torch.tensor([prep["sources"][s]["ids"]], device="cuda") for s in SOURCES}
            colours = {"clean": answer_colour(model.generate(ids, MAX_NEW_TOKENS)[1], palette)}
            for s in SOURCES:
                colours[s] = answer_colour(model.generate(source_ids[s], MAX_NEW_TOKENS)[1], palette)
            ok = colours == {"clean": cfs["roles"]["A"], "cf": cfs["cf"]["answer"], "off": cfs["off"]["answer"]}
            row["status"] = "eligible" if ok else "not_eligible"
            if not ok:
                continue
            positions = regime_positions("after_start", prep["offsets"], spans(item, prep["text"]))
            assert len(positions) == 21, f"{item['name']}: {len(positions)} positions after the start line"
            _, clean_h = model.run(ids, record=WINDOW)
            delta = {}
            for s in SOURCES:
                _, source_h = model.run(source_ids[s], record=WINDOW)
                delta[s] = {layer: source_h[layer][positions] - clean_h[layer][positions] for layer in WINDOW}
            cases.append(
                {
                    "set": set_name,
                    "name": item["name"],
                    "ids": ids,
                    "roles": cfs["roles"],
                    "palette": palette,
                    "positions": positions,
                    "delta": delta,
                    "h_norm": {layer: clean_h[layer][positions].norm(dim=-1) for layer in WINDOW},
                }
            )
            del clean_h
    print(f"{len(cases)} eligible items", flush=True)
    outcomes = []
    for case in cases:
        for layer in WINDOW:
            for group, members in GROUPS.items():
                for source in SOURCES if group in CONTROLLED else ("cf",):
                    idx = list(members)
                    delta = case["delta"][source][layer][idx]
                    at = [case["positions"][i] for i in idx]
                    _, text, _ = model.generate(case["ids"], MAX_NEW_TOKENS, {layer: AddRows(delta, at)})
                    colour = answer_colour(text, case["palette"])
                    ratio = float((delta.norm(dim=-1) / case["h_norm"][layer][idx]).mean())
                    outcomes.append(
                        {
                            "set": case["set"],
                            "name": case["name"],
                            "layer": layer,
                            "group": group,
                            "source": source,
                            "continuation": text,
                            "colour": colour,
                            "role": category(colour, case["roles"]),
                            "edit_ratio": round(ratio, 4),
                        }
                    )
        print(f"{case['name']}: done ({len(outcomes)} outcomes)", flush=True)
    write_jsonl(out_dir / "items.jsonl", item_rows)
    write_jsonl(out_dir / "outcomes.jsonl", outcomes)
    summary = summarize(outcomes)
    summary["items"] = {s: sum(c["set"] == s for c in cases) for s in TEST_SETS}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    write_summary_md(out_dir / "summary.md", name, summary)
    print((out_dir / "summary.md").read_text())


def step_scores(outcomes: list[dict], **where) -> dict[str, float]:
    """Per item, the share of window layers at which the matching copies give f(X)."""
    hits: dict[str, list[bool]] = {}
    for o in outcomes:
        if all(o.get(k) == v for k, v in where.items()):
            hits.setdefault(o["name"], []).append(o["role"] == "b")
    return {n: sum(v) / len(v) for n, v in hits.items()}


def summarize(outcomes: list[dict]) -> dict:
    out: dict[str, Any] = {"sets": {}}
    for set_name in TEST_SETS:
        rows = [o for o in outcomes if o["set"] == set_name]
        if not rows:
            continue
        keys = [(g, s) for g in GROUPS for s in (SOURCES if g in CONTROLLED else ("cf",))]
        scores = {f"{g} {s}": step_scores(rows, group=g, source=s) for g, s in keys}

        def diff(a: str, b: str, scores=scores) -> tuple[float, float, float]:
            names = sorted(set(scores[a]) & set(scores[b]))
            return paired_bootstrap_diff(
                [scores[a][n] for n in names], [scores[b][n] for n in names], N_BOOT, BOOT_SEED
            )

        comparisons = {f"{g}: C - O": diff(f"{g} cf", f"{g} off") for g in CONTROLLED}
        comparisons["all - all_but_reading"] = diff("all cf", "all_but_reading cf")
        verdicts = {f"{g} carries the step": comparisons[f"{g}: C - O"][1] > 0 for g in CONTROLLED}
        verdicts["the reading positions are needed"] = comparisons["all - all_but_reading"][1] > 0
        by_layer = []
        for g, s in keys:
            for layer in WINDOW:
                cells = [o for o in rows if (o["group"], o["source"], o["layer"]) == (g, s, layer)]
                n = len(cells)
                count = {r: sum(o["role"] == r for o in cells) for r in ("A", "b", "c", "X", "I")}
                by_layer.append(
                    {"group": g, "source": s, "layer": layer, "n": n, **{r: wilson(k, n) for r, k in count.items()}}
                )
        collateral = {}
        for g, s in keys:
            cells = [o for o in rows if (o["group"], o["source"]) == (g, s)]
            collateral[f"{g} {s}"] = {r: sum(o["role"] == r for o in cells) / len(cells) for r in ("A", "X", "I")}
        before = {}
        with open(RESULTS / PARTS_RUNS[set_name] / "outcomes.jsonl") as f:
            for line in f:
                o = json.loads(line)
                if o["part"] == "full" and o["source"] == "cf":
                    before[o["name"], o["layer"]] = o["role"]
        now = {(o["name"], o["layer"]): o["role"] for o in rows if (o["group"], o["source"]) == ("all", "cf")}
        both = [k for k in now if k in before]
        out["sets"][set_name] = {
            "n": len({o["name"] for o in rows}),
            "step_scores": {k: statistics.mean(v.values()) for k, v in scores.items()},
            "comparisons": comparisons,
            "verdicts": verdicts,
            "collateral": collateral,
            "by_layer": by_layer,
            "reproduce_all": {"cells": len(both), "match": sum(before[k] == now[k] for k in both)},
        }
    return out


def write_summary_md(path: Path, run: str, summary: dict) -> None:
    pts = lambda d: f"{100 * d[0]:+.0f} [{100 * d[1]:+.0f}, {100 * d[2]:+.0f}]"  # noqa: E731
    lines = [f"# {EXP} / {run}", "", "Items: " + ", ".join(f"{k} {v}" for k, v in summary["items"].items()), ""]
    for set_name, s in summary["sets"].items():
        lines += [
            f"## {set_name} items (n={s['n']})",
            "",
            f"'all' reproduces exp04's full copy: {s['reproduce_all']['match']}/{s['reproduce_all']['cells']}",
            "",
            "| copy (group, source) | step score | A kept | X | I |",
            "|---|---|---|---|---|",
        ]
        for k, v in s["step_scores"].items():
            c = s["collateral"][k]
            lines.append(f"| {k} | {100 * v:.0f}% | {100 * c['A']:.0f}% | {100 * c['X']:.0f}% | {100 * c['I']:.0f}% |")
        lines += ["", "Paired differences in step score (pts, 95% CI):"]
        lines += [f"- {k}: {pts(v)}" for k, v in s["comparisons"].items()]
        lines += ["", "Verdicts (rules in the manifest):"]
        lines += [f"- {k}: {v}" for k, v in s["verdicts"].items()]
        lines += [""]
    path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stage", choices=["manifest", "run"])
    parser.add_argument("target", nargs="?", help="run: the run's folder name")
    parser.add_argument("--name", help="manifest: the run's folder name")
    parser.add_argument("--why", help="manifest: who chose this run and why")
    args = parser.parse_args()
    if args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why)
    else:
        assert args.target, "run needs the run's folder name"
        stage_run(args.target)
