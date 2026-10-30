"""T (batch 42, Dan 26 Oct ~11:55): the pointer directions beyond simple scenes, read from the runs that have landed.

Varied scenes (x0b_generalize --pointer): the lookup's and the recall's extra loss without the pointer directions (alf,
4 atoms, fit on the simple scenes, not refit) against a random part of their share, at the layer fixed in advance;
pooled, per format and json + table. Natural passages (x5_natural --pointer): x5_natural_split's pointer cells, the
passages whose original fact sentence comes before the bridge's mention. Q42.1-3 count the models over their bars; a
model whose run is missing or stopped at its gate is "not tested". Cluster bootstrap over bridge entities (10,000
resamples, seed 0). CPU only. UNVERIFIED.

uv run python scripts/t_pointer.py          # every model whose runs are in results/
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x5_natural_split as NS

RESULTS = pins.RESULTS_DIR / "t_pointer"
X0B, NAT = pins.RESULTS_DIR / "x0b_generalize", pins.RESULTS_DIR / "x5_natural"
RUNS = {  # model: (x0b run, x5_natural run), the T job specs' names
    "qwen3.5-9b": ("qwen35_9b_x0b_v2_ptr", "qwen35_9b_x5_natural_ptr"),
    "qwen3.6-27b": ("x0b_v2_ptr_27b", "x5_natural_ptr_27b"),
    "qwen3.5-122b-a10b": ("qwen35_122b_x0b_v2_ptr", "qwen35_122b_x5_natural_ptr"),
    "muse-glimmer-30b": ("muse30b_x0b_v2_ptr", "muse30b_x5_natural_ptr"),
}
ALF = NS.PARTS["alf"]
BARS = {"q42_1": 0.20, "q42_2": 0.15, "q42_3": 0.15}  # batch 42, fixed in advance
SUBSETS = {"pooled": ("prose", "json", "table"), "json + table": ("json", "table"),
           "prose": ("prose",), "json": ("json",), "table": ("table",)}  # fmt: skip


def alf_cells(rows: list[dict], scenes: set[str], n_boot: int) -> dict[str, dict]:
    """Per reader, the pointer arm's cell (whole / without alf / without a same-size random part (control)) on these scenes."""
    return NS.cells(rows, scenes, n_boot, "alf")


def varied(run: str, n_boot: int) -> dict | None:
    src = X0B / run
    if not (src / "outcomes.jsonl").exists():
        return None
    m = json.loads((src / "manifest.json").read_text())
    fmt = {c["scene"]: c["format"] for c in X.read_jsonl(src / "cases.jsonl")}
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl") if r["layer"] == m["predicted"]]
    if not any(r["dict"] == ALF[0] for r in rows):
        return None
    done = {r["scene"] for r in rows if r["arm"] == "whole"}
    out = {"run": run, "layer": m["predicted"], "pointer_from": m.get("pointer_from")}
    for name, formats in SUBSETS.items():
        scenes = {s for s in done if fmt[s] in formats}
        if len({r["entity"] for r in rows if r["scene"] in scenes}) >= 2:
            out[name] = {"n": len(scenes), **alf_cells(rows, scenes, n_boot)}
    return out


def natural(run: str, n_boot: int) -> dict | None:
    """The fact-first passages; None when the run has not landed, {"gate": False} when it stopped at its gate."""
    src = NAT / run
    if not src.exists():
        return None
    if not (src / "outcomes.jsonl").exists():
        return {"gate": False}
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    rows = X.read_jsonl(src / "outcomes.jsonl")
    done = {r["scene"] for r in rows if r["arm"] == "whole"}
    first = {s for s in done if NS.placement(cases[s])["original"] == "before"}
    return {"run": run, "n": len(first), **alf_cells(rows, first, n_boot)}


def cell_of(r: dict, q: str) -> dict | None:
    if q == "q42_3":
        return r["natural"]
    return (r["varied"] or {}).get("pooled" if q == "q42_1" else "json + table")


def count(per_model: dict[str, dict], q: str) -> dict:
    """How many models pass a question's bar; models without the cell are listed as not tested."""
    passed, tested = [], []
    for model, r in per_model.items():
        c = cell_of(r, q)
        if not c or "gate" in c:
            continue
        tested.append(model)
        ex = c[X.LOOKUP]["excess"]
        if ex[0] >= BARS[q] and (q != "q42_3" or ex[1] > 0):
            passed.append(model)
    n = len(passed)
    option = "(a) all four" if n == 4 else "(b) three" if n == 3 else "(c) one or two" if n else "(d) none"
    return {"passed": passed, "tested": tested, "option": option, "final": len(tested) == len(RUNS)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    per_model = {}
    for model, (x0b, nat) in RUNS.items():
        per_model[model] = {"varied": varied(x0b, a.n_boot), "natural": natural(nat, a.n_boot)}
    qs = {q: count(per_model, q) for q in BARS}
    out = RESULTS / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = ["# T: the pointer directions beyond simple scenes (batch 42)", "",
             f"Extra loss without the pointer directions minus without a random part of their share; cluster bootstrap over "
             f"bridge entities ({a.n_boot} resamples). Natural: passages whose original fact sentence comes before the "
             f"bridge's mention. UNVERIFIED.", "",
             "| model | scenes | n | lookup switches (whole) | lookup extra loss | recall extra loss |", "|---|---|---|---|---|---|"]  # fmt: skip
    for model, r in per_model.items():
        cells = {**{k: v for k, v in (r["varied"] or {}).items() if isinstance(v, dict)}, "natural": r["natural"]}
        if not r["varied"]:
            lines.append(f"| {model} | varied | – | – | not landed | – |")
        if not r["natural"] or "gate" in r["natural"]:
            why = "not landed" if not r["natural"] else "not tested (stopped at its gate)"
            lines.append(f"| {model} | natural | – | – | {why} | – |")
        for name, c in cells.items():
            if c and "gate" not in c:
                lk, rc = c[X.LOOKUP], c[X.RECALL]
                lines.append(
                    f"| {model} | {name} | {c['n']} | {lk['switched_whole']} | {ci(lk['excess'])} | {ci(rc['excess'])} |"
                )
    lines.append("")
    for q, v in qs.items():
        lines.append(f"{q.upper().replace('_', '.')}: bar {BARS[q]}; passed {', '.join(v['passed']) or 'none'} of "
                     f"{len(v['tested'])} tested -> {v['option']}{'' if v['final'] else ' (not all models landed)'}.")  # fmt: skip
    (out / "verdict.json").write_text(json.dumps({"models": per_model, "questions": qs, "bars": BARS}, indent=1) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
