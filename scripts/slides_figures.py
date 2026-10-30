"""The deck's depth-track figures (Dan's brief, 29 Oct ~20:40: "turn the root README into the deck's skeleton") into
figures/archive/slides/ (PNG + SVG each). CPU only, from committed files: the story figures (figures/depth/*.png, themselves
built from data/figures/depth/data.csv), data/figures/depth/data.csv, and the per-item run files the depth README cites.

  d1_split      the conflict test (fig01), the lens part's atoms (fig18), parts of the same size (fig02): one page
  d2_address    the address: probe / removal / swap (fig07), code and tool output (fig21), the lens readout of the
                swap (fig07b), the trained-probe monitor (fig23)
  d4_limits     where it breaks, drawn from data.csv: (a) lookup extra loss at 25 / 50 / 100 lens directions, 27B vs
                122B (fig02b rows); (b) Zach's named passages, true vs made-up facts (ledger_zach_named rows); (c) the
                question-position cells (fig20 rows)
  ex_d1..ex_d3  one real item each, the first in file order that switches under the whole change (no search)

d1 and d2 place the story figures' own PNGs side by side (same colours and marks by construction); they are not
re-plotted. Every figure holding a 29 Oct number carries a "pending hand-check" tag.

uv run python scripts/slides_figures.py
"""

from __future__ import annotations

import ast
import csv
import json
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[1]
STORY = REPO / "figures" / "depth"
OUT = REPO / "figures" / "archive" / "slides"
DATA = STORY / "data.csv"
COL = {"lookup": "#6a4bd6", "recall": "#3a3a3a", "band": "#f0f0f0", "muted": "#666666", "tag": "#b8433a"}
MODELS = (("qwen3.5-9b", "9B"), ("qwen3.6-27b", "27B"), ("muse-glimmer-30b", "Muse"),
          ("nemotron-3.5-lightning", "Lightning ○"), ("qwen3.5-122b-a10b", "122B"))  # fmt: skip
PENDING = "pending hand-check"
EX = {  # the per-item files each example box reads
    "ex_d1": REPO / "results/x0_necessity/qwen35_9b_x0_necessity",
    "ex_d2": REPO / "results/x47_verbal/qwen35_9b_x47_verbal/examples.json",
    "ex_d3": REPO / "results/x51_jread/qwen35_9b_x51_10",
}


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", facecolor="white")
    fig.savefig(OUT / f"{name}.png", dpi=150, facecolor="white")
    plt.close(fig)
    print("wrote", OUT / f"{name}.png")


def header(fig, title: str, sub: str, pending: bool) -> None:
    fig.text(0.01, 0.985, title, ha="left", va="top", fontsize=15, weight="bold")
    fig.text(0.01, 0.95, sub, ha="left", va="top", fontsize=10, color=COL["muted"])
    if pending:
        fig.text(0.99, 0.985, PENDING, ha="right", va="top", fontsize=10, color=COL["tag"],
                 bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": COL["tag"]})  # fmt: skip


def place(fig, rect: tuple[float, float, float, float], name: str, tag: str) -> None:
    ax = fig.add_axes(rect)
    ax.imshow(mpimg.imread(STORY / f"{name}.png"))
    ax.set_axis_off()
    ax.set_title(f"{tag}  (figures/depth/{name}.png)", fontsize=8, loc="left", color=COL["muted"])


def d1_split() -> None:
    fig = plt.figure(figsize=(16, 9))
    header(fig, "The lookup goes around the lens part of the bridge word; the recall goes through it",
           "Left: the conflict test, main test at L, five models. Right: what the lens part's 25 directions are; "
           "parts of the same size on the recall.", pending=True)  # fmt: skip
    place(fig, (0.01, 0.02, 0.50, 0.88), "fig01_split", "the conflict test")
    place(fig, (0.52, 0.47, 0.47, 0.43), "fig18_atoms", "the lens part's atoms")
    place(fig, (0.52, 0.02, 0.47, 0.43), "fig02_specificity", "parts of the same size")
    save(fig, "d1_split")


def d2_address() -> None:
    fig = plt.figure(figsize=(16, 10))
    header(fig, "The lookup reads an address: a probe finds it, a swap moves it, the lens cannot see it",
           "Top: probe, removal, swap (prose); code and tool output. Bottom: the lens readout of the swap; "
           "the trained probe on the lens part.", pending=True)  # fmt: skip
    place(fig, (0.01, 0.47, 0.48, 0.44), "fig07_writes", "A-C: probe, without the address, the swap by dose")
    place(fig, (0.51, 0.47, 0.48, 0.44), "fig21_code_tool", "code and tool output")
    place(fig, (0.01, 0.01, 0.48, 0.42), "fig07b_verbal", "D: the lens readout of the swap")
    place(fig, (0.51, 0.01, 0.48, 0.42), "fig23_monitor", "D: the trained probe, 25 / 100 lens directions")
    save(fig, "d2_address")


def rows() -> dict[tuple[str, str, str], tuple[float, float | None, float | None]]:
    out = {}
    with DATA.open() as f:
        for r in csv.DictReader(f):
            try:
                v = float(r["value"])
            except ValueError:
                continue
            lo = float(r["lo"]) if r["lo"] not in ("", None) else None
            hi = float(r["hi"]) if r["hi"] not in ("", None) else None
            out[(r["figure"], r["model"], r["quantity"])] = (v, lo, hi)
    return out


def bar(ax, x: float, cell, color: str, hollow: bool = False) -> None:
    v, lo, hi = cell
    ax.bar(x, v, 0.36, color="white" if hollow else color, edgecolor=color, linewidth=1.5)
    if lo is not None and hi is not None:
        ax.errorbar(x, v, yerr=[[v - lo], [hi - v]], color="black", capsize=3, lw=1)
    ax.text(x, max(v, hi or v) + 0.03, f"{v:.2f}", ha="center", va="bottom", fontsize=8)


def d4_limits() -> None:
    R = rows()
    fig, axs = plt.subplots(1, 3, figsize=(16, 6), gridspec_kw={"width_ratios": [1, 1.4, 1]})
    fig.subplots_adjust(top=0.80, bottom=0.16, left=0.05, right=0.99, wspace=0.28)
    header(
        fig,
        "Where it breaks",
        "(a) the 27B's lookup with more lens directions, against the 122B; (b) Zach's "
        "named passages; (c) asking the question before the scene. Whiskers: 95% intervals.",
        pending=True,
    )
    ax = axs[0]  # (a) fig02b
    for m, name, c in (("qwen3.6-27b", "27B", COL["lookup"]), ("qwen3.5-122b-a10b", "122B", "#b07a0a")):
        ks = (25, 50, 100)
        cells = [R[("fig02b", m, f"(a) main test, {k} directions: lookup extra loss")] for k in ks]
        ax.plot(ks, [c_[0] for c_ in cells], "-o", color=c, label=name)
        for k, (v, lo, hi) in zip(ks, cells, strict=True):
            if lo is not None and hi is not None:
                ax.vlines(k, lo, hi, color=c, lw=1)
            ax.text(k, v + 0.04, f"{v:.2f}", ha="center", fontsize=8, color=c)
    ax.axhspan(-0.10, 0.10, color=COL["band"], zorder=0)
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xticks((25, 50, 100))
    ax.set_xlabel("lens directions taken out")
    ax.set_ylabel("lookup: switches lost beyond a random part")
    ax.set_title("(a) the 27B's lookup at 25 / 50 / 100 lens directions", fontsize=10, loc="left")
    ax.legend(frameon=False, fontsize=9)
    ax = axs[1]  # (b) ledger_zach_named
    xs = []
    for i, (m, name) in enumerate(MODELS[:4]):
        for j, (facts, off) in enumerate((("true facts", -0.2), ("made-up facts", 0.2))):
            for reader, c, dx in (("lookup", COL["lookup"], 0.0),):
                q = f"Zach's named passages, {facts}, {reader}: switches lost beyond random"
                if ("ledger_zach_named", m, q) in R:
                    bar(ax, i + off + dx, R[("ledger_zach_named", m, q)], c, hollow=(j == 1) or m.startswith("nem"))
        xs.append(name)
    ax.set_xticks(range(len(xs)), xs)
    ax.axhline(0, color="black", lw=0.6)
    ax.axhspan(-0.10, 0.10, color=COL["band"], zorder=0)
    ax.set_ylabel("lookup: switches lost beyond random")
    ax.set_title("(b) Zach's named passages, lookup: true facts (filled) vs made-up (open)", fontsize=10, loc="left")
    ax = axs[2]  # (c) fig20
    for i, m in enumerate(("qwen3.6-27b", "qwen3.5-122b-a10b")):
        cell = R[("fig20_order_cell", m, "the lookup, question before minus after (paired)")]
        bar(ax, i, cell, COL["lookup"])
    ax.set_xticks((0, 1), ("27B", "122B"))
    ax.axhline(0, color="black", lw=0.6)
    ax.set_ylabel("lookup: question first minus question last (paired)")
    ax.set_title("(c) the question's position", fontsize=10, loc="left")
    for a in axs:
        a.margins(y=0.15)
    save(fig, "d4_limits")


def box(name: str, title: str, lines: list[str], source: str) -> None:
    text = "\n".join(w for ln in lines for w in (textwrap.wrap(ln, 96, subsequent_indent="    ") or [""]))
    n = text.count("\n") + 1
    fig = plt.figure(figsize=(12, 0.9 + 0.2 * n))
    fig.text(0.01, 1 - 0.25 / (0.9 + 0.2 * n), title, ha="left", va="top", fontsize=12, weight="bold")
    fig.text(0.015, 1 - 0.6 / (0.9 + 0.2 * n), text, ha="left", va="top", family="monospace", fontsize=9,
             bbox={"boxstyle": "square,pad=0.6", "fc": "white", "ec": "black"})  # fmt: skip
    fig.text(0.01, 0.01, textwrap.fill(source, 170), ha="left", va="bottom", fontsize=7, color=COL["muted"])
    save(fig, name)


def jl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def ex_d1() -> None:
    """The 9B's main test at L12: the first scene in examples.jsonl order whose recall and lookup both switch under the
    whole change (greedy answers stored for the whole change and without the lens part)."""
    run = EX["ex_d1"]
    layer = json.loads((run / "manifest.json").read_text()).get("predicted", 12)
    cases = {c["scene"]: c for c in jl(run / "cases.jsonl")}
    ex = [r for r in jl(run / "examples.jsonl") if r["layer"] == layer]
    out = {(r["scene"], r["reader"], r["arm"]): r["greedy"].strip() for r in ex}
    for scene in dict.fromkeys(r["scene"] for r in ex):
        c = cases[scene]
        rd = c["readers"] if isinstance(c["readers"], dict) else ast.literal_eval(c["readers"])
        whole = {k: out.get((scene, k, "-/0/-/whole")) for k in ("PP", "PM")}
        if all(whole[k] == str(rd[k]["cf_answer"]) for k in ("PP", "PM")):
            break
    else:
        raise SystemExit("ex_d1: no scene switches both readers under the whole change")
    lines = [f"prompt:          {c['context']}", f"changed prompt:  {c['cf_context']}", ""]
    for k, who in (("PP", "lookup"), ("PM", "recall")):
        lines += [f"{who}: {rd[k]['question']}",
                  f"    original answer {rd[k]['answer']}; changed prompt's answer {rd[k]['cf_answer']}",
                  f"    whole change: {out[(scene, k, '-/0/-/whole')]}    without the lens part: "
                  f"{out[(scene, k, 'jpp/25/signed/no_part')]}    without a random part: "
                  f"{out[(scene, k, 'jpp/25/signed/no_rand')]}"]  # fmt: skip
    box("ex_d1", f"D1 example: the 9B, main test at L{layer}, scene {scene}", lines,
        f"{run.relative_to(REPO)}/cases.jsonl and examples.jsonl (layer {layer}; the first scene in file order whose "
        "lookup and recall both switch under the whole change)")  # fmt: skip


def ex_d2() -> None:
    """The 9B's 47.0 examples (x8_write's writes at s = 2): the first item in examples.json order with a write that
    sends the lookup to the swapped-in locker; the lens's top five at the bridge word before and after."""
    path = EX["ex_d2"]
    for it in json.loads(path.read_text()):
        writes = it["writes"] if isinstance(it["writes"], list) else ast.literal_eval(it["writes"])
        hits = [w for w in writes if w["arm"] == "write" and w.get("x8_lookup_class") == "target"]
        if hits:
            w = hits[0]
            break
    else:
        raise SystemExit("ex_d2: no write moved the lookup to the target locker")
    digits = it["slot_digits"] if isinstance(it["slot_digits"], list) else ast.literal_eval(it["slot_digits"])
    top_h = it["lens_top_h"] if isinstance(it["lens_top_h"], list) else ast.literal_eval(it["lens_top_h"])
    prompt = it["prompt_O"].split("user\n", 1)[-1].split("<|im_end|>", 1)[0]
    j, k = int(it["j"]), int(w["k"])
    lines = [*prompt.splitlines(), "",
             f"lockers by sentence: {digits}; the bridge '{it['bridge']}' sits in sentence {j + 1} (locker {digits[j]})",
             f"the swap points to sentence {k + 1} (locker {digits[k]}), at about a real change's size (s = 2)",
             f"lookup answer: before {digits[j]}, after {w['x8_lookup_top']}",
             f"lens top five at the bridge word, before: {top_h[:5]}",
             f"lens top five at the bridge word, after:  {w['top'][:5]}"]  # fmt: skip
    box("ex_d2", f"D2 example: the 9B, routes scene {it['scene']}, the address swap", lines,
        f"{path.relative_to(REPO)} (47.0's stored examples, seed 0; the first item in file order whose swap sends the "
        "lookup to the swapped-in locker)")  # fmt: skip


def ex_d3() -> None:
    """The 9B's 51.10 run: the first locker-first item in cases.jsonl order whose recall switches under the
    whole-state patch at the last token (P3) at the read peak; the answer under the lens swap; the lens's top five at
    the last token (the J++ readout of the stored state, on the CPU)."""
    run = EX["ex_d3"]
    peak = json.loads((run / "peak.json").read_text())["peaks"]["recall"]
    cases = jl(run / "cases.jsonl")
    out = {(r["scene"], r["reader"], r["arm"]): r for r in jl(run / "outcomes.jsonl")
           if r["pos"] == "P3" and str(r["layer"]) == str(peak)}  # fmt: skip
    for c in cases:
        r = out.get((c["scene"], "PM", "whole"))
        if c["group"] == "locker-first" and r and int(r["switched"]):
            break
    else:
        raise SystemExit("ex_d3: no locker-first recall switches under the whole-state patch")
    rd = c["readers"] if isinstance(c["readers"], dict) else ast.literal_eval(c["readers"])
    swap = out[(c["scene"], "PM", "swap")]
    # the readout needs the gitignored states.npz and the 9B's W_U: computed once, then read from the committed cache
    cache = OUT / "ex_d3_readout.json"
    if (run / "states.npz").exists():
        import numpy as np
        import torch

        from scripts import review_jspace as RJ

        z = np.load(run / "states.npz")
        ro = RJ.readout("qwen3.5-9b")
        h = torch.tensor(z["h"][cases.index(c), 1, 0, 2, list(z["layers"]).index(peak)], dtype=torch.float32)[
            None
        ]  # recall, O, P3
        got = {"scene": c["scene"], "layer": peak,
               "top5": [ro.decode(t) for t in torch.topk(ro.lens(h, peak)[0], 5).indices.tolist()],
               "whole": ro.decode(int(r["top"])), "swap": ro.decode(int(swap["top"]))}  # fmt: skip
        OUT.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(got, indent=1, ensure_ascii=False) + "\n")
    got = json.loads(cache.read_text())
    assert got["scene"] == c["scene"], f"{cache}: another item"
    assert got["layer"] == peak, f"{cache}: another layer"
    lines = [f"prompt:          {c['context']}", f"changed prompt:  {c['cf_context']}",
             f"recall: {rd['PM']['question']}  (original {rd['PM']['answer']}, changed {rd['PM']['cf_answer']})", "",
             f"the lens's top five at the last token, L{peak}: {got['top5']}",
             f"whole-state patch at the last token: {got['whole']!r} (switched: {bool(int(r['switched']))})",
             f"lens swap at the last token:         {got['swap']!r} (switched: {bool(int(swap['switched']))})"]  # fmt: skip
    box("ex_d3", f"D3 example: the 9B, scene {c['scene']}, the recall at the last token", lines,
        f"{run.relative_to(REPO)}/cases.jsonl, outcomes.jsonl (P3, L{peak}) and states.npz (the J++ readout on the "
        "CPU, scripts/review_jspace.py); the first locker-first item in file order whose recall switches under the "
        "whole-state patch")  # fmt: skip


def main() -> None:
    d1_split()
    d2_address()
    d4_limits()
    ex_d1()
    ex_d2()
    ex_d3()


if __name__ == "__main__":
    main()
