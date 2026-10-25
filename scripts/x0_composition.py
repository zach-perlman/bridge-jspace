"""x0_composition (Dan, 25 Oct plan B1; descriptive, after the data, CPU only): the J++ part's extra loss per reader,
split by the swap (two people swap picks: the main test; only the asked pick changes: the one-pick runs and the
replication) and by sentence order (both the original and the new bridge's locker sentences before the asked pick;
only the original bridge's before; the original bridge's after), from the per-item outcome files at the layer fixed in
advance (25 J++ directions, signed OMP, against a random part of the same share; cluster bootstrap over bridge
entities, 10,000 resamples, seed 0); also by whether the asked pick is the bridge's first mention (README v2, table 3c;
the 122B added). The question: why the 9B recall's J++ loss is 0.06-0.12 on both-locker-first
scenes and 0.37 on all one-pick scenes. The pointer directions' scenes (x0_massmean_lf) are the one-pick runs' both-before
scenes; the script checks that and says so.

uv run python scripts/x0_composition.py --name x0_composition_<stamp>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.utils import git_state
from scripts import x0_necessity as X
from scripts import x0_strata as ST

EXP = "x0_composition"
RESULTS = pins.RESULTS_DIR / EXP
# model: (layer, [(swap, results dir)], the pointer directions' run)
RUNS = {
    "qwen3.5-9b": (12, [("two people swap", "x0_necessity/qwen35_9b_x0_necessity"),
                        ("only the asked pick", "x0_necessity/qwen35_9b_x0_single_r2"),
                        ("only the asked pick (replication, fresh scenes)", "x0_replicate/qwen35_9b_x0_replicate")],
                   "x0_massmean/qwen35_9b_x0_massmean_lf"),
    "qwen3.6-27b": (32, [("two people swap", "x0_necessity/x0_necessity_27b_chat"),
                         ("only the asked pick", "x0_necessity/x0_single_27b_r2"),
                         ("only the asked pick (replication, fresh scenes)", "x0_replicate/x0_replicate_27b")],
                    "x0_massmean/x0_massmean_lf_27b"),
    "qwen3.5-122b-a10b": (33, [("two people swap", "x0_necessity/qwen35_122b_x0_necessity_r2"),
                               ("only the asked pick", "x0_necessity/qwen35_122b_x0_single"),
                               ("only the asked pick (replication, fresh scenes)", "x0_replicate/qwen35_122b_x0_replicate")],
                          "x0_massmean/qwen35_122b_x0_massmean_grid"),
}  # fmt: skip
ORDERS = ("both locker sentences before the pick", "only the original's before", "the original's after")


def order_of(case: dict) -> str:
    f = ST.features(case)
    if f["org locker vs asked pick"] != "before":
        return ORDERS[2]
    return ORDERS[0] if f["alt locker vs asked pick"] == "before" else ORDERS[1]


def first_mention(case: dict) -> str:
    """'first mention: yes' if the asked pick sentence is the first sentence that names the original bridge."""
    q = case["readers"][X.LOOKUP]["question"]
    asked = re.search(r"([A-Z][a-z]+)'s pick", q).group(1)  # type: ignore[union-attr]
    sents = [s if s.endswith(".") else s + "." for s in case["context"].split(". ")]
    mine = next(i for i, s in enumerate(sents) if s.startswith(f"{asked} picked"))
    first = next(i for i, s in enumerate(sents) if re.search(rf"\b{re.escape(case['bridge'])}\b", s))
    return f"first mention: {'yes' if first == mine else 'no'}"


def cells(rows: list[dict], layer: int, scenes: set[str], n_boot: int) -> dict[str, dict]:
    """X0's J++ cell per reader on the given scenes (chat rendering, the given layer, k = 25, signed)."""
    mine = [r for r in rows if r["scene"] in scenes and r["rendering"] == "chat" and r["layer"] == layer]
    out = {}
    for key, c in X.cells_of(mine, n_boot).items():
        if key[3:] == ("jpp", X.K_MAIN, "signed"):
            out[key[2]] = c
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    out = RESULTS / a.name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": a.name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "note": "Descriptive, after the data (Dan, 25 Oct plan B1).", "code": git_state(), "n_boot": a.n_boot,
         "inputs": {t: [d for _, d in runs] for t, (_, runs, _) in RUNS.items()}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    table, lines = [], ["# J++ extra loss by swap and sentence order (descriptive, after the data)", "",
                        f"Layer fixed in advance; 25 J++ directions; cluster bootstrap ({a.n_boot} resamples). UNVERIFIED.", "",
                        "| model | swap | sentence order | n | lookup extra loss | recall extra loss | recall S_whole |",
                        "|---|---|---|---|---|---|---|"]  # fmt: skip
    notes = []
    for target, (layer, runs, mm) in RUNS.items():
        for swap, d in runs:
            src = pins.RESULTS_DIR / d
            if not (src / "outcomes.jsonl").exists():  # not run yet (the 122B's replication, x0_122b_b9)
                notes.append(f"{target}: {d} not run yet.")
                continue
            cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c["rendering"] == "chat"}
            rows = X.read_jsonl(src / "outcomes.jsonl")
            done = {
                r["scene"] for r in rows if r["rendering"] == "chat" and r["layer"] == layer and r["arm"] == "whole"
            }
            order = {s: order_of(cases[s]) for s in done}
            fm = {s: first_mention(cases[s]) for s in done}
            groups = [("all", set(done))] + [(o, {s for s in done if order[s] == o}) for o in ORDERS]
            groups += [(g, {s for s in done if fm[s] == g}) for g in ("first mention: yes", "first mention: no")]
            for o, scenes in groups:
                if not scenes:
                    continue
                c = cells(rows, layer, scenes, a.n_boot)
                row = {"model": target, "swap": swap, "order": o, "n": len(scenes), "run": d,
                       **{w: {k: c[w][k] for k in ("excess", "Jdep", "Rdep", "S_whole", "n")} for w in c}}  # fmt: skip
                table.append(row)
                fmt = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
                lines.append(f"| {target} | {swap} | {o} | {len(scenes)} | {fmt(c[X.LOOKUP]['excess'])} | "
                             f"{fmt(c[X.RECALL]['excess'])} | {c[X.RECALL]['S_whole'][0]:.2f} |")  # fmt: skip
            if swap == "only the asked pick":
                mm_scenes = {r["scene"] for r in X.read_jsonl(pins.RESULTS_DIR / mm / "outcomes.jsonl")}
                both = {s for s in done if order[s] == ORDERS[0]}
                notes.append(f"{target}: the pointer directions' scenes ({mm}, n = {len(mm_scenes)}) "
                             f"{'are' if mm_scenes == both else 'are NOT'} the one-pick run's both-before scenes "
                             f"(n = {len(both)}; overlap {len(mm_scenes & both)}).")  # fmt: skip
    lines += ["", *notes]
    (out / "composition.json").write_text(json.dumps({"manifest": m, "rows": table, "notes": notes}, indent=1) + "\n")
    (out / "composition.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
