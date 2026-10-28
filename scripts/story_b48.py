"""Batch 48's README figures (docs/depth/README.md; jobs/c3/batch48.yaml, Q48.1-Q48.5): one figure per test, drawn
from that test's verdict folder only, in story_style's look. Each builder reads the verdict's json, records every
plotted number (story_style.record, source = the verdict file) and saves through story_style.save; the title is the
claim, built from the verdict so it reads true for any outcome (or passed in). A verdict json holding "planted": true
(the tests' and previews' fake verdicts, never a real run's) gets "PLANTED" at the head of its subtitle.

Colours beyond story_style's: the J++ part (or its removal) red, the whole change near-black. Every arm here is fixed
in advance (filled marks); the rule's bars are thin lines, labelled.

    from scripts import story_b48 as F
    F.build_das(Path("results/x48_das/verdict-<UTC>"), "fig21_das")
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from bridge_jspace import pins
from scripts import story_style as S

LOOKUP, RECALL = "PP", "PM"  # x0_necessity.READERS
ORDER = (("qwen3.5-9b", "9B", "Qwen3.5-9B"), ("qwen3.6-27b", "27B", "Qwen3.6-27B"),
         ("muse-glimmer-30b", "Muse", "Muse Glimmer 30B"))  # fmt: skip
TWO = (ORDER[0], ORDER[2])  # 48.2-48.4 run on the 9B and Muse only
JPP = "#b23b3b"  # the J++ part, or the change without it
WHOLE = "#222222"  # the whole change
FIXED = "All arms fixed in advance; thin lines: the rule's bars."


# ---- shared ---------------------------------------------------------------------------------------------------------


def rel(path: Path) -> str:
    return str(path.relative_to(pins.REPO_ROOT)) if path.is_relative_to(pins.REPO_ROOT) else str(path)


def fig_id(out_name: str) -> str:
    return out_name.split("_", 1)[0]


def ok(v: Any) -> bool:
    """A [v, lo, hi] (or a bare number) with a finite point estimate."""
    x = v[0] if isinstance(v, list) and v else v
    return isinstance(x, int | float) and not math.isnan(x)


def pct(v: list | float) -> tuple[float, float, float]:
    """[v, lo, hi] (or a bare v, no interval) as percent; a missing bound -> the point."""
    if not isinstance(v, list):
        return 100 * v, 100 * v, 100 * v
    lo, hi = (v[1] if ok([v[1]]) else v[0]), (v[2] if ok([v[2]]) else v[0])
    return 100 * v[0], 100 * lo, 100 * hi


def lead(blob: dict, text: str) -> str:
    return ("PLANTED data, not results. " if blob.get("planted") else "") + text


def name_list(names: list[str]) -> str:
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def record(fid: str, target: str, quantity: str, v, n=None, source: str = "") -> None:
    if isinstance(v, list):
        S.record(fid, target, quantity, v[0], v[1] if len(v) > 1 else None, v[2] if len(v) > 2 else None, n=n,
                 source=source)  # fmt: skip
    else:
        S.record(fid, target, quantity, v, n=n, source=source)


def legend(fig, handles, labels, y: float, ncol: int = 3) -> None:
    """One legend under the subtitle (readme_story_figures.legend's look)."""
    fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.0, y), frameon=False, handletextpad=0.4,
               ncol=ncol, columnspacing=1.2, handlelength=1.6)  # fmt: skip


def bar(ax, x: float, y0: float, y1: float, color: str = "#555555") -> None:
    """The rule's bar on a row group: a thin vertical line."""
    ax.plot([x, x], [y0, y1], color=color, lw=1.0, zorder=1, solid_capstyle="butt")


def forest(ax, groups: list[dict], models: tuple, xlim: tuple[float, float], gap: float = 0.6) -> dict:
    """Rows of dots, x in percent. Each group: a header row ('header', 'color'), one row per model (y tick label = the
    model's short name), a right-aligned rule label on the header row ('rule') and the bar ('bars': [(x, colour)])
    spanning the model rows. 'cells': {target: [(value, colour, dy[, marker])] or a str (a cell state)}. Returns each
    (group index, target)'s row y."""
    y, ticks, labels, rows = 0.0, [], [], {}
    for gi, g in enumerate(groups):
        ax.text(xlim[0], y + 0.4, g["header"], ha="left", va="top", color=g.get("color", "#222222"), weight="bold",
                linespacing=1.0)  # fmt: skip
        if g.get("rule"):
            ax.text(xlim[1], y + 0.4, g["rule"], ha="right", va="top", color="#555555")
        y -= 0.85 * g["header"].count("\n")
        top = y - 0.5
        for target, short, _ in models:
            y -= 1
            ticks.append(y)
            labels.append(short)
            cell = g["cells"].get(target)
            if isinstance(cell, str):
                ax.text(xlim[0] + 0.02 * (xlim[1] - xlim[0]), y, cell, va="center", color=S.COL["muted"])
                continue
            for v, color, dy, *mk in cell or []:
                mark(ax, y + dy, pct(v), color, mk[0] if mk else "o")
            rows[(gi, target)] = y
        for x, color in g.get("bars", []):
            bar(ax, x, top, y - 0.45, color)
        y -= 1 + gap
    ax.set_yticks(ticks, labels)
    ax.set_ylim(y + gap + 0.4, 0.6)
    ax.set_xlim(*xlim)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#eeeeee")
    ax.spines["left"].set_visible(False)
    return rows


def mark(ax, y: float, v: tuple[float, float, float], color: str, marker: str = "o", size: float = 7) -> None:
    """A filled mark (fixed in advance) with its 95% whisker."""
    ax.plot([v[1], v[2]], [y, y], color=color, lw=1.6, zorder=2, solid_capstyle="butt")
    ax.plot([v[0]], [y], marker, ms=size, color=color, zorder=3)


def finish(fig, out_name: str) -> str:
    S.save(fig, out_name)
    return out_name


# ---- 48.1: DAS at the bridge word ----------------------------------------------------------------------------------


def das_title(models: list[dict]) -> str:
    """The claim from rules (a)-(d) on the tested models (all of them must hold for the plain claim)."""
    names: dict[str, str] = {t: n for t, n, _ in ORDER}
    if models and all(m["rules"]["fallback_no_low_dimensional_mediator"] for m in models):
        return "No small subspace at the bridge word carries the lookup"
    a: list[str] = [str(names.get(m["target"], m["target"])) for m in models if m["rules"]["a"]]
    b = all(m["rules"]["b"] for m in models)
    if models and len(a) == len(models):
        return "Two readers, two subspaces; the recall's lies in the J++ part" if b else (
            "Two readers, two subspaces at the bridge word")  # fmt: skip
    if a:
        return f"Two readers, two subspaces on the {name_list(a)} only"
    return "The two readers do not use two separate subspaces"


def rules_met(m: dict) -> str:
    met = [f"({k})" for k in "abcd" if m["rules"][k]]
    return "rules met: " + (" ".join(met) if met else "none")


def build_das(verdict_dir: Path, out_name: str = "fig21_das", title: str | None = None) -> str:
    """48.1 (scripts/x48_das.py verdict: verdict.json). Top: the switches a learned subspace carries by its size k, per
    model (the lookup's subspace on the lookup, the recall's on the recall; a random subspace and one trained on
    shuffled answers in grey; a diamond: the other reader's subspace at its chosen k); the large dot is the chosen k.
    Bottom left: each subspace's share of the change inside the item's J++ part (25 directions). Bottom right: the
    lookup's subspace against the pointer, outside every known part, and its identity answers when another item moved."""
    path = verdict_dir / "verdict.json"
    blob = json.loads(path.read_text())
    src, fid = rel(path), fig_id(out_name)
    by = {m["target"]: m for m in blob["models"]}
    plt = S.setup()
    h = 10.2
    fig = plt.figure(figsize=(S.WIDTH, h))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.1], left=0.08, right=0.98, top=1 - 2.3 / h, bottom=0.05,
                          hspace=0.42, wspace=0.12)  # fmt: skip
    top, inner, other = fig.add_subplot(gs[0, :]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])
    S.title(fig, title or das_title(blob["models"]), lead(blob,
            "Fixed in advance; 95% intervals over bridge items.\n"
            "A subspace of k directions, learned at the bridge word, carries the changed prompt into the\n"
            "original prompt; large dot: the k the rule reads. Thin lines: the rule's bars (own ≥ 70 at k ≤ 16,\n"
            "the other reader's ≤ 25)."))  # fmt: skip
    readers = ((LOOKUP, "lookup", S.COL["lookup"]), (RECALL, "recall", S.COL["recall"]))
    for i, (target, _, name) in enumerate(ORDER):
        x0 = 5 * i
        top.text(x0 + 1.5, 112, name, ha="center", va="bottom", weight="bold")
        m = by.get(target)
        if m is None:
            top.text(x0 + 1.5, 50, "not run", ha="center", color=S.COL["muted"])
            continue
        top.text(x0 + 1.5, 103, rules_met(m), ha="center", va="bottom", color=S.COL["muted"])
        ks = [int(k) for k in m["ks"]]
        xs = [x0 + j for j in range(len(ks))]
        bar_x = [x for x, k in zip(xs, ks, strict=True) if k <= 16]
        for yb in (70, 25):
            top.plot([bar_x[0] - 0.3, bar_x[-1] + 0.3], [yb, yb], color="#555555", lw=1.0, zorder=1)
        chosen = {w: m["readers"][w]["k"] for w, _, _ in readers}
        for w, word, col in readers:
            t = m["readers"][w]["test"]
            for arm, key, color, mk in (("random", "random_iia", S.COL["control"], "o"),
                                        ("shuffled", "shuffled_iia", S.COL["control"], "^")):  # fmt: skip
                by_k: dict[str, list] = t.get(key) or {}
                pts = [(x, by_k[str(k)]) for x, k in zip(xs, ks, strict=True) if str(k) in by_k]
                top.plot([x for x, _ in pts], [100 * v[0] for _, v in pts], color=color, lw=1.0, marker=mk, ms=4,
                         zorder=1)  # fmt: skip
                for k, v in ((k, by_k[str(k)]) for k in ks if str(k) in by_k):
                    record(fid, target, f"48.1, {word}'s switches under a {arm} subspace, k = {k}", v, n=t["n"],
                           source=src)  # fmt: skip
            own = [(x, k, t["own_iia"][str(k)]) for x, k in zip(xs, ks, strict=True)]
            top.plot([x for x, _, _ in own], [100 * v[0] for _, _, v in own], color=col, lw=1.6, zorder=2)
            for x, k, v in own:
                lo, hi = pct(v)[1:]
                top.plot([x, x], [lo, hi], color=col, lw=1.4, zorder=2)
                top.plot([x], [100 * v[0]], "o", ms=9 if k == chosen[w] else 4.5, color=col, zorder=3)
                record(fid, target, f"48.1, {word}'s switches under the {word}'s subspace, k = {k}", v, n=t["n"],
                       source=src)  # fmt: skip
            other_w = RECALL if w == LOOKUP else LOOKUP
            xk = xs[ks.index(chosen[other_w])] + (0.18 if w == LOOKUP else -0.18)
            cv = t["cross_iia"]
            lo, hi = pct(cv)[1:]
            top.plot([xk, xk], [lo, hi], color=col, lw=1.4, zorder=3)
            top.plot([xk], [100 * cv[0]], "D", ms=7, color=col, mec="white", mew=0.8, zorder=4)
            record(fid, target, f"48.1, {word}'s switches under the other reader's subspace (k = {chosen[other_w]})",
                   cv, n=t["n"], source=src)  # fmt: skip
        for k, r in m["rules"].items():
            if k in "abcd" or k == "fallback_no_low_dimensional_mediator":
                record(fid, target, f"48.1: rule ({k}) holds" if len(k) == 1 else "48.1: no small subspace (fallback)",
                       int(bool(r)), source=src)  # fmt: skip
    top.set_xticks([5 * i + j for i in range(len(ORDER)) for j in range(4)], ["1", "4", "16", "64"] * len(ORDER))
    top.set_xlim(-0.6, 5 * len(ORDER) - 1.4)
    top.set_ylim(-4, 104)
    top.set_yticks([0, 50, 100], ["0", "50", "100"])
    top.grid(axis="y", color="#eeeeee")
    top.set_xlabel("subspace size k (directions)")
    top.set_ylabel("switches carried (%)")
    hs = [Line2D([], [], color=S.COL["lookup"], marker="o", ms=6, lw=1.6),
          Line2D([], [], color=S.COL["recall"], marker="o", ms=6, lw=1.6),
          Line2D([], [], color="#7a7a7a", marker="D", ls="", ms=6),
          Line2D([], [], color=S.COL["control"], marker="o", ms=4, lw=1.0),
          Line2D([], [], color=S.COL["control"], marker="^", ms=4, lw=1.0)]  # fmt: skip
    legend(fig, hs, ["lookup's subspace, lookups", "recall's subspace, recalls", "the other reader's subspace",
                     "random subspace (same k)", "trained on shuffled answers"], 1 - 1.3 / h)  # fmt: skip
    # bottom: where each subspace sits (shares of its change), at the chosen k
    models = ORDER
    cells: dict[str, dict[str, Any]] = {k: {} for k in ("rc_in", "lk_in", "rnd_in", "cos2", "outside", "identity")}
    for target, _, _ in models:
        m = by.get(target)
        if m is None:
            for c in cells.values():
                c[target] = "not run"
            continue
        g = m["geometry"]
        kl, kr = m["readers"][LOOKUP]["k"], m["readers"][RECALL]["k"]
        rl, rr, rnd = f"R_{LOOKUP}_k{kl}", f"R_{RECALL}_k{kr}", f"rand_k{kr}"
        cos2 = g[rl]["cos2_U"]
        route = m["routes"].get(rl, {}).get("identity")
        quantities = (("rc_in", g[rr]["in_jpp25"], S.COL["recall"], "the recall's subspace: share inside the J++ part"),
                      ("lk_in", g[rl]["in_jpp25"], S.COL["lookup"], "the lookup's subspace: share inside the J++ part"),
                      ("rnd_in", g[rnd]["in_jpp25"], S.COL["control"], "a random subspace: share inside the J++ part"),
                      ("cos2", cos2, S.COL["lookup"], "the lookup's subspace: overlap with the pointer (cos²)"),
                      ("outside", g[rl]["outside_union"], S.COL["lookup"],
                       "the lookup's subspace: share outside the J++ part, pointer and input-embedding directions"),
                      ("identity", route, S.COL["lookup"],
                       "the lookup's subspace only: identity answers, another item moved"))  # fmt: skip
        for key, v, col, what in quantities:
            if v is None or not ok(v):
                cells[key][target] = "not tested"
                continue
            cells[key][target] = [(v, col, 0.0)]
            record(fid, target, f"48.1, {what}", v, source=src)
    forest(inner, [
        {"header": "recall's subspace", "color": S.COL["recall"], "rule": "≥ 50", "bars": [(50, S.COL["recall"])],
         "cells": cells["rc_in"]},
        {"header": "lookup's subspace", "color": S.COL["lookup"], "rule": "≤ 20", "bars": [(20, S.COL["lookup"])],
         "cells": cells["lk_in"]},
        {"header": "random subspace", "color": "#8a8a8a", "rule": "≤ 15", "bars": [(15, "#8a8a8a")],
         "cells": cells["rnd_in"]},
    ], models, (0, 100))  # fmt: skip
    inner.set_title("Each subspace's change: share\ninside the J++ part (%)", fontsize=S.FONT, loc="left",
                    weight="bold")  # fmt: skip
    forest(other, [
        {"header": "overlap with the pointer (cos²)", "rule": "≥ 50", "color": S.COL["lookup"],
         "bars": [(50, "#555555")], "cells": cells["cos2"]},
        {"header": "outside the J++ part, pointer\nand input-embedding directions", "rule": "≥ 50",
         "color": S.COL["lookup"], "bars": [(50, "#555555")], "cells": cells["outside"]},
        {"header": "identity answers when\nanother item moved", "rule": "≥ 30", "color": S.COL["lookup"],
         "bars": [(30, "#555555")], "cells": cells["identity"]},
    ], models, (0, 100))  # fmt: skip
    other.set_title("The lookup's subspace (%)\n", fontsize=S.FONT, loc="left", weight="bold")
    for ax in (inner, other):
        ax.set_xticks([0, 50, 100], ["0", "50", "100"])
    return finish(fig, out_name)


# ---- 48.2: attribute enrichment at the bridge token (A) and the late MLPs (B) ---------------------------------------

ENRICH_A = {"holds": "The J++ part keys the recall's attribute",
            "does not hold": "No sign the J++ part keys the recall's attribute"}  # fmt: skip
ENRICH_B = {"holds": "late MLPs at the bridge word fetch it", "does not hold": "late MLPs at the bridge word do not"}


def enrich_title(verdict: dict) -> str:
    a, b = ENRICH_A.get(verdict["A"]), ENRICH_B.get(verdict["B"])
    if a and b:
        return f"{a}; {b}"
    if a:
        return a
    if b:
        return {
            "holds": "Late MLPs at the bridge word fetch the recall's attribute",
            "does not hold": "Late MLPs at the bridge word do not fetch the recall's attribute",
        }[verdict["B"]]
    return "Attribute enrichment at the bridge word (pending)"


ARMS_A = (("whole", "whole change", WHOLE), ("no_rand", "without a random part (same size)", S.COL["control"]),
          ("no_jpp", "without the J++ part", JPP))  # fmt: skip


def mark_v(ax, x: float, v: tuple[float, float, float], color: str, marker: str = "o", size: float = 6) -> None:
    """A filled mark with a vertical 95% whisker."""
    ax.plot([x, x], [v[1], v[2]], color=color, lw=1.3, zorder=2)
    ax.plot([x], [v[0]], marker, ms=size, color=color, zorder=3)


def build_enrichment(verdict_dir: Path, out_name: str = "fig22_enrichment", title: str | None = None) -> str:
    """48.2 (scripts/x48_enrich.py verdict: x48_2.json). Left two panels (design A), per model: how far the legs probe
    (animals, entities held out) moves from the original item's attribute toward the changed item's, by layer, at the
    position the verdict reads (the bridge token if the probe reads the attribute there, else the last token), under
    the whole change, without the J++ part and without a random part (same size); grey: layers where the probe does not
    read the attribute; dotted: L + 4, where the rule starts. Right (design B): accuracy lost when MLP writes are
    replaced by their mean, per reader, with the two controls."""
    path = verdict_dir / "x48_2.json"
    blob = json.loads(path.read_text())
    src, fid = rel(path), fig_id(out_name)
    a_by = {m["target"]: m for m in blob["A"]}
    b_by = {m["target"]: m for m in blob["B"]}
    plt = S.setup()
    h = 7.6
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, h), gridspec_kw={"width_ratios": [1, 1, 1.25]})
    fig.subplots_adjust(left=0.08, right=0.98, top=1 - 2.35 / h, bottom=0.09, wspace=0.42)
    S.title(fig, title or enrich_title(blob["verdict"]), lead(blob,
            "Fixed in advance; 95% intervals over bridge items.\n"
            "Left: the legs probe moved from the original prompt's item to the changed one (%), by layer;\n"
            "grey: layers where it cannot read legs. Rule from L + 4 (dotted): whole and random part ≥ 60,\n"
            "without the J++ part ≤ 30. Right: accuracy lost with MLP writes replaced by their mean;\n"
            "rule: recall ≥ 40 (thin line), the rest within 10 (grey band)."), limit=86)  # fmt: skip
    for ax, (target, _, name) in zip(axes[:2], TWO, strict=True):
        m = a_by.get(target)
        ax.set_ylim(-5, 105)
        ax.set_yticks([0, 50, 100], ["0", "50", "100"])
        ax.grid(axis="y", color="#eeeeee")
        ax.set_xlabel("layer")
        if m is None or m["status"] != "tested":
            ax.set_title(name, fontsize=S.FONT, weight="bold")
            S.empty(ax, "not run")
            ax.set_xticks([])
            continue
        branch = m["branch"]
        ax.set_title(f"{name}\nat the {branch} token", fontsize=S.FONT, weight="bold")
        table = {int(k): v for k, v in m["tables"][branch].items()}
        layers = sorted(table)
        step = (layers[1] - layers[0]) / 2 if len(layers) > 1 else 1
        acc = {r["layer"]: r for r in m["accuracy"] if r["position"] == branch and r["domain"] == "animals"}
        for la in layers:
            if not table[la]["readable"]:
                ax.axvspan(la - step, la + step, color=S.COL["band"], lw=0, zorder=0)
            if la in acc:
                record(fid, target, f"48.2 A, layer {la}: probe held-out accuracy at the {branch} token",
                       acc[la]["held_out"], source=src)  # fmt: skip
        start = m["layer"] + 4
        ax.axvline(start, color="#555555", ls=":", lw=1.2, zorder=1)
        after = [la for la in layers if la >= start] or [start]
        for yb in (60, 30):
            ax.plot([after[0] - step, after[-1] + step], [yb, yb], color="#555555", lw=1.0, zorder=1)
        for dx, (arm, word, col) in zip((-0.25 * step, 0, 0.25 * step), ARMS_A, strict=True):
            pts = [(la, table[la]["rule_domain"][arm]) for la in layers if ok(table[la]["rule_domain"][arm])]
            ax.plot([la + dx for la, _ in pts], [100 * v[0] for _, v in pts], color=col, lw=1.4, zorder=2)
            for la, v in pts:
                mark_v(ax, la + dx, pct(v), col)
                record(fid, target, f"48.2 A, layer {la}: probe moved toward the changed item, {word}", v,
                       n=table[la]["rule_domain"]["n_read"], source=src)  # fmt: skip
        ax.set_xlim(layers[0] - 2 * step, layers[-1] + 2 * step)
        record(fid, target, "48.2 A: the rule holds", int(bool(m["holds"])), source=src)
    axes[0].set_ylabel("probe moved toward the changed item (%)")
    cells: list[dict[str, Any]] = [{}, {}, {}]
    for target, _, _ in TWO:
        m = b_by.get(target)
        for i, arm in enumerate(("bridge_late", "person_late", "bridge_early")):
            if m is None or m["status"] != "tested":
                cells[i][target] = "not run"
                continue
            cells[i][target] = [(m["readers"]["recall"]["drop"][arm], S.COL["recall"], 0.18),
                                (m["readers"]["lookup"]["drop"][arm], S.COL["lookup"], -0.18)]  # fmt: skip
            for w in ("recall", "lookup"):
                record(fid, target, f"48.2 B, {arm}: {w} accuracy lost", m["readers"][w]["drop"][arm],
                       n=m["readers"][w]["n"], source=src)  # fmt: skip
        if m is not None and m["status"] == "tested":
            record(fid, target, "48.2 B: the rule holds", int(bool(m["holds"])), source=src)
    ax = axes[2]
    ax.axvspan(-10, 10, color=S.COL["band"], lw=0, zorder=0)
    forest(ax, [
        {"header": "MLPs at the bridge word,\nlayers after L", "bars": [(40, S.COL["recall"])],
         "cells": cells[0]},
        {"header": "control: at the asked\nperson's name, after L", "cells": cells[1]},
        {"header": "control: at the bridge\nword, up to L/2", "cells": cells[2]},
    ], TWO, (-20, 100))  # fmt: skip
    ax.set_xticks([0, 50, 100], ["0", "50", "100"])
    ax.set_xlabel("accuracy lost (%)")
    ax.set_title("recall", fontsize=S.FONT, loc="left", color=S.COL["recall"], weight="bold")
    ax.set_title("lookup", fontsize=S.FONT, loc="center", color=S.COL["lookup"], weight="bold")
    legend(fig, [Line2D([], [], color=c, marker="o", ms=6, lw=1.4) for _, _, c in ARMS_A],
           [w for _, w, _ in ARMS_A], 1 - 1.55 / h)  # fmt: skip
    return finish(fig, out_name)


# ---- 48.3: forward binding at the locker sentence -------------------------------------------------------------------


def bind_title(verdict: dict) -> str:
    base = {"holds": "The locker sentence binds person to item, outside the lens",
            "does not hold": "No forward binding at the locker sentence (rule not met)"}.get(
        verdict["label"], "Forward binding at the locker sentence (pending)")  # fmt: skip
    moves = verdict["label"] == "holds" and verdict["recall_moves"]["answer"] == "yes"
    return base + ("; the recall moves too" if moves else "")


def build_binding(verdict_dir: Path, out_name: str = "fig23_binding", title: str | None = None) -> str:
    """48.3 (scripts/x48_bind.py verdict: x48_bind.json). Left: the probe for who picked the item, at the locker
    sentence's item word and number, in locker-after and locker-first scenes (chance 33). Middle: the J++ part's share
    of the person direction written there, against a random direction's (bar: 2x random). Right: the write of the
    person direction at strength 1 and 2: lookups sent to the written item's locker and recalls naming its attribute,
    with a random direction of the same norm."""
    path = verdict_dir / "x48_bind.json"
    blob = json.loads(path.read_text())
    src, fid = rel(path), fig_id(out_name)
    by = {m["target"]: m for m in blob["models"] if m["status"] == "tested"}
    plt = S.setup()
    h = 6.9
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, h))
    fig.subplots_adjust(left=0.07, right=0.985, top=1 - 2.0 / h, bottom=0.12, wspace=0.35)
    S.title(fig, title or bind_title(blob["verdict"]), lead(blob,
            "Fixed in advance; 95% intervals over bridge items.\n"
            "Locker sentences after the pick: who picked this item, read by a probe (left); the J++ part's\n"
            "share of the person direction (middle); that direction written at the sentence (right).\n"
            "Thin lines: the rule's bars."), limit=86)  # fmt: skip
    probe: list[dict[str, Any]] = [{}, {}]
    share: list[dict[str, Any]] = [{}, {}]
    write: list[dict[str, Any]] = [{}, {}]
    hi = 1.0
    for target, _, _ in TWO:
        m = by.get(target)
        if m is None:
            for c in (*probe, *share, *write):
                c[target] = "not run"
            continue
        for i, cell in enumerate(("after", "before")):
            probe[i][target] = []
            for tok, dy, mk in (("item", 0.17, "o"), ("number", -0.17, "s")):
                v = m["probes"][tok][cell]["accuracy"]
                if ok(v):
                    probe[i][target].append((v, WHOLE, dy, mk))
                record(fid, target, f"48.3, probe at the {tok}, locker {cell} the pick (accuracy)", v,
                       n=m["probes"][tok][cell]["n"], source=src)  # fmt: skip
        for i, tok in enumerate(("item", "number")):
            c = m["clauses"]["tokens"][tok]
            share[i][target] = []
            if c["share"] is not None:
                share[i][target].append((c["share"], WHOLE, 0.17))
                hi = max(hi, 100 * c["share"])
            share[i][target].append((c["random_share"], S.COL["control"], -0.17))
            hi = max(hi, 200 * c["random_share"])
            record(fid, target, f"48.3, J++ part's share of the person direction at the {tok}", c["share"], source=src)
            record(fid, target, f"48.3, random direction's J++ part share at the {tok}", c["random_share"], source=src)
        for i, (w, col) in enumerate((("lookup", S.COL["lookup"]), ("recall", S.COL["recall"]))):
            arms = m["rates"][w].get("arms") or {}
            if not arms:
                write[i][target] = "no written scenes"
                continue
            write[i][target] = [(arms["w1"]["target"], col, 0.3, "s"), (arms["w2"]["target"], col, 0.1, "o"),
                                (arms["r1"]["target"], S.COL["control"], -0.1, "s"),
                                (arms["r2"]["target"], S.COL["control"], -0.3, "o")]  # fmt: skip
            for arm in ("w1", "w2", "r1", "r2"):
                what = ("the write" if arm[0] == "w" else "a random direction (same norm)") + f", strength {arm[1]}"
                record(fid, target, f"48.3, {w}: {what}, sent to the written item", arms[arm]["target"],
                       n=m["rates"][w]["n"], source=src)  # fmt: skip
        record(fid, target, "48.3: the rule holds", int(bool(m["holds"])), source=src)
    ax = axes[0]
    ax.axvline(100 / 3, color="#999999", ls=":", lw=1.0, zorder=0)
    forest(ax, [{"header": "locker after\nthe pick", "rule": "≥ 85", "bars": [(85, "#555555")], "cells": probe[0]},
                {"header": "locker before\nthe pick", "rule": "≤ 50", "bars": [(50, "#555555")], "cells": probe[1]}],
           TWO, (0, 100))  # fmt: skip
    ax.set_xlabel("probe right (%)\n(dotted: chance)")
    ax = axes[1]
    rows = forest(ax, [{"header": "item word", "cells": share[0]}, {"header": "number", "cells": share[1]}], TWO,
                  (0, min(100.0, 1.15 * hi)))  # fmt: skip
    for (gi, target), y in rows.items():
        m = by.get(target)
        if m is not None:
            bar(ax, 200 * m["clauses"]["tokens"][("item", "number")[gi]]["random_share"], y - 0.45, y + 0.45)
    ax.set_xlabel("J++ part share (%)\n(bar: 2 × random direction)")
    ax = axes[2]
    forest(ax, [{"header": "lookups sent to the\nwritten item's locker", "rule": "≥ 30", "color": S.COL["lookup"],
                 "bars": [(30, "#555555"), (5, S.COL["control"])], "cells": write[0]},
                {"header": "recalls naming the\nwritten item's number", "color": S.COL["recall"],
                 "bars": [(30, "#555555"), (5, S.COL["control"])], "cells": write[1]}], TWO, (0, 100))  # fmt: skip
    ax.set_xlabel("answers (%)\n(grey: random direction, ≤ 5)")
    for a in (axes[0], axes[2]):
        a.set_xticks([0, 50, 100], ["0", "50", "100"])
    for a, t in zip(axes, ("Who picked it?", "Inside the lens?", "The write"), strict=True):
        a.set_title(t, fontsize=S.FONT, weight="bold", loc="left")
    legend(fig, [Line2D([], [], color="#7a7a7a", marker="o", ls="", ms=6),
                 Line2D([], [], color="#7a7a7a", marker="s", ls="", ms=6)],
           ["left: item word; right: strength 2", "left: number; right: strength 1"], 1 - 1.25 / h, ncol=2)  # fmt: skip
    return finish(fig, out_name)


# ---- 48.4: what the copying heads pass ------------------------------------------------------------------------------

PARTS = (("jpp", "J++ part", JPP), ("rest", "the rest (the change minus its J++ part)", WHOLE),
         ("address", "pointer", S.COL["position"]), ("random", "random part (same size)", S.COL["control"]))  # fmt: skip


def heads_title(verdict: dict) -> str:
    return {"holds": "The copying heads pass the rest at twice the J++ part or more",
            "does not hold": "The copying heads do not pass the rest at twice the J++ part"}.get(
        verdict["label"], "What the copying heads pass (pending)")  # fmt: skip


def build_heads(verdict_dir: Path, out_name: str = "fig24_heads", title: str | None = None) -> str:
    """48.4 (scripts/x48_heads.py verdict: x48_heads.json). One panel per model, one row per head (the five with the
    most attention from the last token to the bridge word, after L): how much of each part of the change the head's
    W_OV passes (median ||W_OV x|| / ||x||, 95% interval), the thin bar at 2x the J++ part's, the rule per head at the
    right."""
    path = verdict_dir / "x48_heads.json"
    blob = json.loads(path.read_text())
    src, fid = rel(path), fig_id(out_name)
    by = {m["target"]: m for m in blob["models"] if m["status"] == "tested"}
    plt = S.setup()
    h = 5.8
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, h))
    fig.subplots_adjust(left=0.17, right=0.94, top=1 - 2.45 / h, bottom=0.11, wspace=0.85)
    S.title(fig, title or heads_title(blob["verdict"]), lead(blob,
            "Fixed in advance; medians over items, 95% intervals.\n"
            "Each row: one of the five heads that copy most from the bridge word. How much of each part\n"
            "of the change the head passes; thin line: 2 × the J++ part. Rule: the rest at or past it\n"
            "(random part not above the rest) on 3 of 5 heads, on both models; right: per head."),
            limit=86)  # fmt: skip
    heads_all = [h_ for m in by.values() for h_ in m["selected_heads"]]
    xmax = max([h_["ov"][p][2] for h_ in heads_all for p, _, _ in PARTS if ok(h_["ov"][p]) and ok([h_["ov"][p][2]])]
               + [2 * h_["r"]["jpp"] for h_ in heads_all if ok(h_["r"]["jpp"])] + [0.1])  # fmt: skip
    for ax, (target, _, name) in zip(axes, TWO, strict=True):
        m = by.get(target)
        ax.set_xlim(0, 1.1 * xmax)
        ax.grid(axis="x", color="#eeeeee")
        ax.set_xlabel("passed: ‖W_OV x‖ / ‖x‖")
        if m is None:
            ax.set_title(name, fontsize=S.FONT, weight="bold")
            S.empty(ax, "not run")
            ax.set_yticks([])
            continue
        ax.set_title(f"{name}\n{m['heads_reading_rest']} of {m['heads']} heads pass the rest", fontsize=S.FONT,
                     weight="bold")  # fmt: skip
        heads = m["selected_heads"]
        for i, h_ in enumerate(heads):
            y = -i
            for dy, (p, word, col) in zip((0.27, 0.09, -0.09, -0.27), PARTS, strict=True):
                v = h_["ov"][p]
                if ok(v):
                    lo, hi = (v[1] if ok([v[1]]) else v[0]), (v[2] if ok([v[2]]) else v[0])
                    mark(ax, y + dy, (v[0], lo, hi), col, size=6)
                record(fid, target, f"48.4, layer {h_['layer']} head {h_['head']}: {word} passed", v,
                       n=h_["ov"]["n"], source=src)  # fmt: skip
            if ok(h_["r"]["jpp"]):
                bar(ax, 2 * h_["r"]["jpp"], y - 0.42, y + 0.42, "#222222")
            ax.text(1.03, y, "yes" if h_["rule"]["reads_rest"] else "no", transform=ax.get_yaxis_transform(),
                    va="center", color=S.COL["muted"])  # fmt: skip
            record(fid, target, f"48.4, layer {h_['layer']} head {h_['head']}: passes the rest (rule)",
                   int(bool(h_["rule"]["reads_rest"])), source=src)  # fmt: skip
        ax.set_yticks([-i for i in range(len(heads))], [f"layer {h_['layer']}, head {h_['head']}" for h_ in heads])
        ax.set_ylim(-len(heads) + 0.45, 0.55)
        ax.tick_params(axis="y", length=0)
        record(fid, target, "48.4: the rule holds", int(bool(m["holds"])), source=src)
    legend(fig, [Line2D([], [], color=c, marker="o", ls="", ms=6) for _, _, c in PARTS],
           [w for _, w, _ in PARTS], 1 - 1.2 / h, ncol=2)  # fmt: skip
    return finish(fig, out_name)


# ---- 48.5: the recall's second route --------------------------------------------------------------------------------

ROUTE2_ROWS = (("base", "(i) without the\nJ++ part"), ("write", "(ii) (i) and the\npointer write"),
               ("alone", "(iii) the pointer\nwrite only"), ("random", "(iv) (i) and a random\ndirection (same size)"))  # fmt: skip
ROUTE2_CLASSES = (("slot_k", "the written locker's item", S.COL["position"]),
                  ("changed", "the changed item", S.COL["identity"]), ("original", "original answer", S.COL["original"]),
                  ("other", "other", S.COL["other"]))  # fmt: skip


def route2_title(verdict: dict) -> str:
    return {"holds": "Without the J++ part, the pointer redirects the recall",
            "does not hold": "The pointer does not redirect the recall without the J++ part"}.get(
        verdict["label"], "Can the pointer redirect the recall? (pending)")  # fmt: skip


def build_second_route(verdict_dir: Path, out_name: str = "fig25_second_route", title: str | None = None) -> str:
    """48.5 (scripts/x48_route2.py verdict: x48_route2.json). One panel per model: the recall's answers on the
    informative writes under the four arms, stacked by what they name (the written locker's item first, its share with
    a 95% interval below the bar); thin bars: the rule's 30 under (ii) and 5 under (iv)."""
    path = verdict_dir / "x48_route2.json"
    blob = json.loads(path.read_text())
    src, fid = rel(path), fig_id(out_name)
    by = {m["target"]: m for m in blob["models"]}
    plt = S.setup()
    h = 6.2
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.22, right=0.985, top=1 - 2.15 / h, bottom=0.1, wspace=0.14)
    S.title(fig, title or route2_title(blob["verdict"]), lead(blob,
            "Fixed in advance; recall answers (%).\n"
            "Locker before the pick; the pointer written toward another locker on top of the change\n"
            "without the J++ part. Black: the written locker's item with its 95% interval; thin lines:\n"
            "the rule's bars, ≥ 30 under (ii) and ≤ 5 under (iv), on 2 of 3 models."), limit=86)  # fmt: skip
    for ax, (target, _, name) in zip(axes, ORDER, strict=True):
        m = by.get(target)
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1], ["0", "50", "100"])
        ax.set_ylim(-len(ROUTE2_ROWS) + 0.4, 0.5)
        ax.tick_params(axis="y", length=0)
        rc = (m or {}).get("readers", {}).get("recall", {}).get("informative", {})
        if m is None or m["status"] == "pending" or not rc.get("n"):
            ax.set_title(name, fontsize=S.FONT, weight="bold")
            S.empty(ax, "not run" if m is None or m["status"] == "pending" else "no informative writes")
            continue
        ax.set_title(f"{name}\nrule {'met' if m['holds'] else 'not met'}, n = {rc['n']}", fontsize=S.FONT,
                     weight="bold")  # fmt: skip
        for i, (kind, label) in enumerate(ROUTE2_ROWS):
            left = 0.0
            for cls, word, col in ROUTE2_CLASSES:
                v = rc["share"][kind][cls]
                ax.barh(-i, v[0], left=left, height=0.56, color=col, edgecolor="white", lw=0.8)
                if cls == "slot_k" and v[0] >= 0.12:
                    ax.text(v[0] / 2, -i + 0.02, f"{100 * v[0]:.0f}", ha="center", va="center", color="#222222")
                record(fid, target, f"48.5, {label.replace(chr(10), ' ')}: recall names {word}", v, n=rc["n"],
                       source=src)  # fmt: skip
                left += v[0]
            v = rc["share"][kind]["slot_k"]
            ax.plot([v[1], v[2]], [-i - 0.38] * 2, color="#222222", lw=1.4)
            ax.plot([v[0]], [-i - 0.38], "o", ms=5, color="#222222")
        for i, x in ((1, 0.30), (3, 0.05)):
            bar(ax, x, -i - 0.45, -i + 0.42, "#222222")
        record(fid, target, "48.5: the rule holds", int(bool(m["holds"])), source=src)
    axes[0].set_yticks([-i for i in range(len(ROUTE2_ROWS))], [r[1] for r in ROUTE2_ROWS])
    fig.supxlabel("recall answers (%)", x=0.6, y=0.01, fontsize=S.FONT)
    legend(fig, [Rectangle((0, 0), 1, 1, color=c) for _, _, c in ROUTE2_CLASSES],
           [w for _, w, _ in ROUTE2_CLASSES], 1 - 1.2 / h, ncol=4)  # fmt: skip
    return finish(fig, out_name)


# ---- E15 (v6): the five failed mechanism tests in one panel ---------------------------------------------------------

NEUTRAL = "#222222"  # a probe's or a head count's mark (not a reader)


def mechanism_groups(dirs: dict[str, Path]) -> list[dict]:
    """E15's rows from the five verdicts, each test's deciding number per model (the same fields the per-test builders
    read): 48.2 B the recall's accuracy lost with the bridge word's late MLPs mean-replaced (rule >= 40); 48.3 the probe
    for who picked the item at the locker sentence, locker after the pick (>= 85); 48.4 the heads passing the rest at
    twice the J++ part, of five (>= 3); 48.5 recalls naming the swapped locker's item under (ii) (>= 30); 47.6 (b)
    identity answers kept with the pick sentence blocked from the lockers (within 10 points of the whole change). Each
    group: header, measure, rule text, per model [(value [v, lo, hi] in fractions, colour, dy, marker)], n, bar(s)."""
    out = []
    p = dirs["48.2"] / "x48_2.json"
    b = {m["target"]: m for m in json.loads(p.read_text())["B"] if m["status"] == "tested"}
    out.append({"test": "48.2", "src": rel(p), "header": "Late MLPs at the bridge word carry the recall",
                "measure": "recall accuracy lost, those MLPs mean-replaced", "rule": "rule ≥ 40", "bar": 40,
                "cells": {t: [(m["readers"]["recall"]["drop"]["bridge_late"], S.COL["recall"], 0.0, "o")]
                          for t, m in b.items()},
                "n": {t: m["readers"]["recall"]["n"] for t, m in b.items()},
                "q": ["48.2 B, bridge_late: recall accuracy lost"]})  # fmt: skip
    p = dirs["48.3"] / "x48_bind.json"
    b = {m["target"]: m for m in json.loads(p.read_text())["models"] if m["status"] == "tested"}
    out.append({"test": "48.3", "src": rel(p), "header": "A person mark at the locker sentence",
                "measure": "probe for who picked it (● item word, ■ number; chance 33)", "rule": "rule ≥ 85",
                "bar": 85, "cells": {t: [(m["probes"]["item"]["after"]["accuracy"], NEUTRAL, 0.17, "o"),
                                         (m["probes"]["number"]["after"]["accuracy"], NEUTRAL, -0.17, "s")]
                                     for t, m in b.items()},
                "n": {t: m["probes"]["item"]["after"]["n"] for t, m in b.items()},
                "q": ["48.3, probe at the item, locker after the pick (accuracy)",
                      "48.3, probe at the number, locker after the pick (accuracy)"]})  # fmt: skip
    p = dirs["48.4"] / "x48_heads.json"
    b = {m["target"]: m for m in json.loads(p.read_text())["models"] if m["status"] == "tested"}
    out.append({"test": "48.4", "src": rel(p), "header": "Copying heads pass the rest at twice the J++ part",
                "measure": "heads that do, of the five that copy most (a count)", "rule": "rule ≥ 3 of 5", "bar": 60,
                "cells": {t: [(m["heads_reading_rest"] / m["heads"], NEUTRAL, 0.0, "D")] for t, m in b.items()},
                "n": {t: f"{m['heads']} heads" for t, m in b.items()},
                "q": ["48.4: heads passing the rest at twice the J++ part, share of the five"]})  # fmt: skip
    p = dirs["48.5"] / "x48_route2.json"
    b = {m["target"]: m for m in json.loads(p.read_text())["models"]
         if m["status"] == "tested" and m["readers"]["recall"]["informative"].get("n")}  # fmt: skip
    out.append({"test": "48.5", "src": rel(p), "header": "The address is the recall's second route",
                "measure": "recalls naming the item in the swap's target locker", "rule": "rule ≥ 30", "bar": 30,
                "cells": {t: [(m["readers"]["recall"]["informative"]["share"]["write"]["slot_k"], S.COL["recall"],
                               0.0, "o")] for t, m in b.items()},
                "n": {t: m["readers"]["recall"]["informative"]["n"] for t, m in b.items()},
                "q": ["48.5, (ii) (i) and the pointer write: recall names the written locker's item"]})  # fmt: skip
    p = dirs["47.6"] / "verdict.json"
    b = {t: r for t, r in json.loads(p.read_text())["b"].items() if r.get("status") == "tested"}
    out.append({"test": "47.6", "src": rel(p), "header": "Blocking the pick sentence removes position only",
                "measure": "identity answers kept with the block (bar: the whole change's, less 10 points)",
                "rule": "rule: at the bar or above", "bar": None,
                "cells": {t: [(r["b"]["lookup"]["rate"]["block/sentence/all|identity"], S.COL["identity"], 0.0, "o")]
                          for t, r in b.items()},
                "row_bar": {t: 100 * r["b"]["lookup"]["rate"]["none|identity"][0] - 10 for t, r in b.items()},
                "n": {t: r["n"] for t, r in b.items()},
                "q": ["47.6 (b) block/sentence/all: lookup identity share"]})  # fmt: skip
    return out


def build_mechanisms(dirs: dict[str, Path], out_name: str = "fig15_mechanisms", title: str | None = None) -> str:
    """E15 (v6): one panel, one row group per failed mechanism test (48.2, 48.3, 48.4, 48.5, 47.6 (b)), one row per
    tested model in the order 9B, 27B, Muse: the test's deciding number (percent, 95% whisker; 48.4 is a count of five
    heads, no interval) against its rule's bar (dashed). The per-test figures are fig10b-e and fig09c."""
    groups = mechanism_groups(dirs)
    fid = fig_id(out_name)
    plt = S.setup()
    rows_n = sum(2 + len(g["cells"]) for g in groups)
    h = 1.25 + 0.3 * rows_n + 0.55
    fig, ax = plt.subplots(figsize=(S.WIDTH, h))
    fig.subplots_adjust(left=0.1, right=0.86, top=1 - 1.0 / h, bottom=0.55 / h)
    S.title(fig, title or "Every mechanism we proposed for the split failed its rule",
            "Each test's deciding number per model against its rule's bar (dashed); whiskers: 95% intervals.")  # fmt: skip
    y, ticks, labels = 0.0, [], []
    for g in groups:
        ax.text(0, y, g["header"], ha="left", va="center", weight="bold", fontsize=S.FONT + 0.5)
        ax.text(100, y, g["rule"], ha="right", va="center", color="#111111", fontsize=S.FONT)
        ax.text(0, y - 0.8, g["measure"], ha="left", va="center", color=S.COL["muted"], fontsize=S.FONT - 0.5)
        y -= 1.8
        top = y + 0.5
        for target, short, _ in ORDER:
            if target not in g["cells"]:
                continue
            ticks.append(y)
            labels.append(short)
            for (v, col, dy, mk), q in zip(g["cells"][target], g["q"], strict=True):
                vv = pct(v)
                if isinstance(v, list):
                    ax.plot([vv[1], vv[2]], [y + dy] * 2, color=col, lw=1.6, zorder=2, solid_capstyle="butt")
                ax.plot([vv[0]], [y + dy], mk, ms=7 if mk != "D" else 6.5, color=col, zorder=3)
                text = f"{round(vv[0] / 20)} of 5" if g["test"] == "48.4" else f"{vv[0]:.0f}"
                ax.text(max(vv[2], vv[0]) + 1.5, y + dy, text, va="center", fontsize=S.FONT - 1, color=col)
                record(fid, target, q, v,
                       n=g["n"][target] if isinstance(g["n"][target], int) else None, source=g["src"])  # fmt: skip
            n = g["n"][target]
            ax.text(1.005, y, f"n {n}", transform=ax.get_yaxis_transform(), va="center", fontsize=S.FONT - 1,
                    color=S.COL["muted"])  # fmt: skip
            if g["bar"] is None:
                xb = g["row_bar"][target]
                ax.plot([xb, xb], [y - 0.42, y + 0.42], color=BAR_COL, lw=1.2, ls=(0, (3, 2)), zorder=1)
                record(fid, target, f"{g['test']}: the rule's bar (whole change's identity share less 0.10)",
                       xb / 100, source=g["src"])  # fmt: skip
            y -= 1
        if g["bar"] is not None:
            ax.plot([g["bar"]] * 2, [top, y + 0.5], color=BAR_COL, lw=1.2, ls=(0, (3, 2)), zorder=1)
        y -= 0.5
    ax.set_xlim(-1.5, 100)
    ax.set_xticks([0, 50, 100], ["0", "50", "100"])
    ax.set_xlabel("percent")
    ax.set_ylim(y + 0.6, 0.6)
    ax.set_yticks(ticks, labels)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#eeeeee")
    ax.spines["left"].set_visible(False)
    S.panel_tag(ax, None, "fixed")
    return finish(fig, out_name)


BAR_COL = "#111111"  # a rule's bar (story_b47b.BAR)


# test id -> (the script whose verdict the figure reads, its builder, its README figure name)
TESTS = {"48.1": ("scripts/x48_das.py", build_das, "fig21_das"),
         "48.2": ("scripts/x48_enrich.py", build_enrichment, "fig22_enrichment"),
         "48.3": ("scripts/x48_bind.py", build_binding, "fig23_binding"),
         "48.4": ("scripts/x48_heads.py", build_heads, "fig24_heads"),
         "48.5": ("scripts/x48_route2.py", build_second_route, "fig25_second_route")}  # fmt: skip
