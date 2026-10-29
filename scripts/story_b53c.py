"""Batch 53's monitor figure for Part III (the coordinator, 29 Oct ~13:50: 53.2, "the scope answer", a card next to the
lens-blindness card; Dan's 12:50 restructure, docs_1250). Unverified until hand-checked.

  fig23_monitor  53.2, monitor (b): trained probes (logistic, held-out bridge items, 5 seeds x 5-fold) for which locker
                 sentence holds the bridge's locker (target (b), "the address"), at the last token of the main test, at
                 the layer where the full state peaks (as the verdict's per-layer table): the full state, the J++ part,
                 a random part of the same size and a random part of the same energy, with 25 (A) and 100 (B) lens
                 directions; under each model the rule's label (the brief's, fixed in advance, worded per Dan 11:40)
                 and Dan's 13:15 energy rule's. Five model slots; Lightning hollow (gate chosen after its 60-scene
                 pre-check); the 122B "not run". Monitor (a), the lens readout, is the lens-blindness card's (cited, not
                 drawn here).

Every plotted number is recorded for figures/story/data.csv with its source file; record_card_numbers() records the
numbers the card quotes that the figure does not draw (figure "cards").
"""

from __future__ import annotations

import json
from pathlib import Path

from matplotlib.patches import Patch

from scripts import story_style as S
from scripts.story_b50 import caption

R = S.REPO / "results"
X53_MONITOR = R / "x53_monitor" / "x53_monitor-20261029T124428Z" / "x53_monitor.json"
LT = "nemotron-3.5-lightning"
MODELS = (("qwen3.5-9b", "9B"), ("qwen3.6-27b", "27B"), ("muse-glimmer-30b", "Muse"), (LT, "Lightning"),
          ("qwen3.5-122b-a10b", "122B"))  # fmt: skip
NOT_RUN = {"qwen3.5-122b-a10b": "not run"}
KS = (25, 100)
GREY = S.COL["muted"]
FULL_COL = "#4a4a4a"
# (feature key prefix, page words, colour, hatch)
FEATS = (("full", "the full state", FULL_COL, None), ("jpp", "the J++ part", S.MARK_COL["jpp"], None),
         ("rand", "a random part (same size)", S.COL["control"], None),
         ("erand", "a random part (same energy)", "#8c8c8c", "////"))  # fmt: skip
# the verdict's short labels in the page's words, per target (Dan 11:40 for the address; the verdict's own
# generalisation for the other targets)
TARGET_WORDS = {"b": "the address", "c": "the lookup's answer digit", "a": "which item is the bridge",
                "d": "the recall's answer"}  # fmt: skip


def rel(path: Path) -> str:
    return str(path.relative_to(S.REPO))


def page_label(label: str, target: str) -> str:
    """A rule label as the page writes it: X named, Dan's 'random reads it too' sentence for the address."""
    x = TARGET_WORDS[target]
    if label == "random reads it too":
        if target == "b":
            return (
                "the address is linearly decodable from many subspaces, J++ included; the lens readout does not show it"
            )
        return f"{x} is linearly decodable from many subspaces, J++ included"
    if label == "under-represented in the lens directions":
        return f"{x} is under-represented in the lens directions"
    return label[:-2] + f" {x}" if label.endswith(" X") else label


def fig_label(label: str) -> str:
    """A rule label in the figure's short words (no 'J++' alone, no 'random directions': the glossary)."""
    return {"J-space blind to X": "J-space blind", "J-space carries X": "J-space carries",
            "random reads it too": "random parts read it too", "under-represented in the lens directions":
            "under-represented in the lens directions",
            "no different from random directions of the same energy": "no different from random (same energy)"}.get(
        label, label)  # fmt: skip


def peak(cell: dict) -> int:
    """The layer index where the full state peaks (the first, as the verdict's per-layer table)."""
    acc = cell["full"]["acc"]
    return max(range(len(acc)), key=lambda i: (acc[i], -i))


def value(cell: dict, key: str, i: int) -> tuple[float, float, float]:
    a = cell[key]
    return (a["acc"][i], a["ci"][i][0], a["ci"][i][1])


def build_monitor(path: Path = X53_MONITOR, out_name: str = "fig23_monitor") -> str:
    v = json.loads(path.read_text())
    res, src = v["results"], rel(path)
    plt = S.setup()
    bar_h, gap = 0.17, 0.02
    group = 4 * (bar_h + gap) + 0.62  # four bars and two label lines
    heights = [group if t in res else 0.5 for t, _ in MODELS]
    ys = [-(sum(heights[:i])) for i in range(len(MODELS))]  # each group's top
    top_in, unit_in, bottom_in = 1.85, 0.72, 1.55
    h = top_in + unit_in * sum(heights) + bottom_in
    fig = plt.figure(figsize=(S.WIDTH, h))
    S.title(
        fig,
        "The J++ part holds less of the address than random parts of its energy",
        "Trained probes at the last token of the main test: which locker sentence holds the bridge's locker.",
    )
    box = (bottom_in / h, unit_in * sum(heights) / h)
    axes = [fig.add_axes((0.135, box[0], 0.36, box[1])), fig.add_axes((0.6, box[0], 0.36, box[1]))]
    head = {"fontsize": 12, "weight": "bold", "va": "bottom"}
    fig.text(0.01, 1 - (top_in - 0.3) / h, "A  With twenty-five lens directions", **head)
    fig.text(0.53, 1 - (top_in - 0.3) / h, "B  With a hundred lens directions", **head)
    for ax, k in zip(axes, KS, strict=True):
        ns = []
        for (t, _), y0, hh in zip(MODELS, ys, heights, strict=True):
            if t not in res:
                ax.text(0.01, y0 - hh / 2, NOT_RUN[t], va="center", fontsize=S.FONT, color=GREY)
                S.record(out_name, t, f"the address at the last token, main test, {k} lens directions: not run",
                         "not run", source=src)  # fmt: skip
                continue
            r = res[t]["main"]
            cell = r["acc"]["T|b"]
            i = peak(cell)
            layer = r["layers"][i]
            hollow = t == LT
            for j, (pre, words, col, hatch) in enumerate(FEATS):
                key = "full" if pre == "full" else f"{pre}{k}"
                val = value(cell, key, i)
                y = y0 - 0.12 - j * (bar_h + gap)
                face = "white" if hollow and hatch is None else ("white" if hatch else col)
                edge = col if (hollow or hatch) else "none"
                ax.barh(y, val[0], height=bar_h, facecolor=face, edgecolor=edge, hatch=hatch, lw=1.2, zorder=2)
                ax.plot([val[1], val[2]], [y, y], color="#1e1e1e", lw=1.1, zorder=3, solid_capstyle="butt")
                ax.text(max(val[0], val[2]) + 0.02, y, f"{val[0]:.2f}", va="center", fontsize=S.LABEL_PT - 1,
                        color="#1e1e1e")  # fmt: skip
                S.record(out_name, t, f"the address at the last token, main test, {k} lens directions: {words}",
                         round(val[0], 4), round(val[1], 4), round(val[2], 4), n=r["n_rows"], source=src)  # fmt: skip
            rules = r["rules"]["T|b"]
            dec, ene = rules[f"k{k}"]["label"], rules[f"erand_k{k}"]["label"]
            yl = y0 - 0.12 - 4 * (bar_h + gap) - 0.04
            ax.text(0.015, yl, f"rule: {fig_label(dec)}", va="top", fontsize=S.LABEL_PT - 1, color="#1e1e1e")
            ax.text(0.015, yl - 0.27, f"energy rule: {fig_label(ene)}", va="top", fontsize=S.LABEL_PT - 1, color=GREY)
            S.record(out_name, t, f"the address at the last token, main test, {k} lens directions: the layer read "
                     "(where the full state peaks)", layer, source=src)  # fmt: skip
            S.record(out_name, t, f"the address at the last token, main test, {k} lens directions: the rule's label",
                     page_label(dec, "b"), source=src)  # fmt: skip
            S.record(out_name, t, f"the address at the last token, main test, {k} lens directions: the energy rule's "
                     "label", page_label(ene, "b"), source=src)  # fmt: skip
            ns.append(str(r["n_rows"]))
        ax.set_ylim(-sum(heights), 0.05)
        ax.set_xlim(0, 1.17)
        ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.spines["bottom"].set_bounds(0, 1)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#eeeeee")
        ax.set_axisbelow(True)
        ax.set_xlabel("probe accuracy (held-out bridge items)")
        S.panel_tag(ax, ", ".join(ns), "fixed")
    centres = [y0 - (hh / 2 if t not in res else 0.12 + 1.5 * (bar_h + gap)) for (t, _), y0, hh in
               zip(MODELS, ys, heights, strict=True)]  # fmt: skip
    axes[0].set_yticks(centres, [name for _, name in MODELS], fontsize=12)
    axes[1].set_yticks(centres, ["" for _ in MODELS])
    handles = [Patch(facecolor="white" if hatch else col, edgecolor=col if hatch else "none", hatch=hatch, lw=1.2)
               for _, _, col, hatch in FEATS]  # fmt: skip
    fig.legend(handles, [w for _, w, _, _ in FEATS], loc="upper left", bbox_to_anchor=(0.01, 1 - 0.75 / h), ncol=2,
               frameon=False, fontsize=S.FONT - 1)  # fmt: skip
    caption(fig, ["Logistic probes on held-out bridge items, five seeds of five folds, at the layer where the full state "
                  "peaks; whiskers: 95% intervals. Under each model: the rule's label (fixed in advance) and the "
                  "energy rule's (against a random part of the same energy; set after the first labels, before the "
                  "verdict).",
                  "Lightning hollow: its gate chosen after the 60-scene pre-check. 122B: not run."], 1.0)  # fmt: skip
    S.save(fig, out_name)
    return out_name


def record_card_numbers(path: Path = X53_MONITOR) -> None:
    """The numbers and labels the monitor card quotes that fig23 does not draw (figure "cards"), from the verdict's
    json: the scenes; the address at the bridge word and on the JSON scenes; the lookup's answer digit at the last token
    (100 lens directions) and at the bridge word; the positive controls at the bridge word."""
    v = json.loads(path.read_text())
    res, src = v["results"], rel(path)

    def best(r: dict, cell: str, key: str = "full") -> float:
        return round(max(r["acc"][cell][key]["acc"]), 4)

    b_full, c_full, many = [], [], 0
    for t, r2 in res.items():
        for ds, words in (("main", "main test"), ("json", "JSON scenes")):
            r = r2[ds]
            S.record("cards", t, f"monitor, {words}: rows, bridge items", f"{r['n_rows']} rows, {r['n_entities']} "
                     "bridge items", source=src)  # fmt: skip
            rb = r["rules"]["B|b"]
            S.record("cards", t, f"monitor, {words}: the address at the bridge word, the full state at its best layer",
                     best(r, "B|b"), n=r["n_rows"], source=src)  # fmt: skip
            S.record("cards", t, f"monitor, {words}: the address at the bridge word, the rule's label (25 / 100 lens "
                     "directions)", f"{rb['k25']['label']} / {rb['k100']['label']}", source=src)  # fmt: skip
            b_full.append(best(r, "B|b"))
            rc = r["rules"]["T|c"]["k100"]["label"]
            many += rc == "random reads it too"
            S.record("cards", t, f"monitor, {words}: the lookup's answer digit at the last token, 100 lens directions, "
                     "the rule's label", page_label(rc, "c"), source=src)  # fmt: skip
            S.record("cards", t, f"monitor, {words}: the lookup's answer digit at the bridge word, the full state at "
                     "its best layer", best(r, "B|c"), n=r["n_rows"], source=src)  # fmt: skip
            c_full.append(best(r, "B|c"))
            ec = r["rules"]["B|c"]
            S.record("cards", t, f"monitor, {words}: the lookup's answer digit at the bridge word, the energy rule's "
                     "label (25 / 100 lens directions)", f"{ec['erand_k25']['label']} / {ec['erand_k100']['label']}",
                     source=src)  # fmt: skip
        j = r2["json"]
        jb = j["rules"]["T|b"]
        S.record("cards", t, "monitor, JSON scenes: the address at the last token, the full state at its best layer",
                 best(j, "T|b"), n=j["n_rows"], source=src)  # fmt: skip
        S.record("cards", t, "monitor, JSON scenes: the address at the last token, the rule's label (25 / 100 lens "
                 "directions)", f"{jb['k25']['label']} / {jb['k100']['label']}", source=src)  # fmt: skip
        S.record("cards", t, "monitor, JSON scenes: the address at the last token, the energy rule's label (25 / 100 "
                 "lens directions)", f"{jb['erand_k25']['label']} / {jb['erand_k100']['label']}", source=src)  # fmt: skip
        m = r2["main"]
        for tgt in ("a", "d"):  # the positive controls at the bridge word, main test, 25 lens directions
            S.record("cards", t, f"monitor, main test, positive control ({TARGET_WORDS[tgt]}) at the bridge word, 25 "
                     "lens directions: the J++ part at its best layer", best(m, f"B|{tgt}", "jpp25"), n=m["n_rows"],
                     source=src)  # fmt: skip
            S.record("cards", t, f"monitor, main test, positive control ({TARGET_WORDS[tgt]}) at the bridge word, 25 "
                     "lens directions: the rule's label", page_label(m["rules"][f"B|{tgt}"]["k25"]["label"], tgt),
                     source=src)  # fmt: skip
        S.record("cards", t, "monitor, main test: the lookup's answer digit at the bridge word, chance",
                 round(m["acc"]["B|c"]["chance"]["acc"][0], 2), source=src)  # fmt: skip
    cells = sum(len(r2) for r2 in res.values())
    S.record("cards", "across models", "monitor: the address at the bridge word, the full state at its best layer, "
             "lowest over models and scene sets", min(b_full), source=src)  # fmt: skip
    S.record("cards", "across models", "monitor: the address at the bridge word, the full state at its best layer, "
             "highest over models and scene sets", max(b_full), source=src)  # fmt: skip
    S.record("cards", "across models", "monitor: the lookup's answer digit at the bridge word, the full state at its "
             "best layer, highest over models and scene sets", max(c_full), source=src)  # fmt: skip
    S.record("cards", "across models", "monitor: the lookup's answer digit at the last token, 100 lens directions: "
             "cells whose label is 'decodable from many subspaces'", f"{many} of {cells}", source=src)  # fmt: skip
    S.record("cards", "across models", "monitor: probes (seeds x folds)",
             f"{v['probe']['seeds']} x {v['probe']['folds']}", source=src)  # fmt: skip
