"""x0_figures: the X0 review figures from the finished runs in results/x0_necessity/ (jobs/c3/X0.md). Writes a new
results/x0_necessity/figures-<UTC>/ with one PNG per figure and data.csv (every drawn number with its run). UNVERIFIED.

- overview: columns 9B and 27B, rows chat / nochat / raw. Lookup and recall excess (J++ k = 25 minus its random part)
  by layer with 95% CIs and labels; at the pre-registered layer the rule's verdict and the graded contrast C = recall
  excess - lookup excess (paired bootstrap over entities). A panel without rows says why (gate, with the model's most
  common first output; not run yet).
- detail_<run>_<rendering>: switch rates, dependences, excess, every dictionary's excess and share, by layer.
- kmatch: at the pre-registered layer, each dictionary's dependence against the share of ||Δ||² it removes (all k),
  with the random subspace's dependence at the same shares as the reference (added after data).
- share: J++ share of ||Δ||² against J++ dependence across valid layers, per model and reader (added after data).
- asked_first: excess by layer on all items and on the asked-first subset (no upstream change in Δ; added after data).

The lookup-vs-recall difference is called a graded contrast; "split" only where the labels say lookup around and recall
through at the same layer.
"""

from __future__ import annotations

import argparse
import collections
import csv
import io
import json
import shutil
import statistics
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X

MODELS = (("qwen3.5-9b", "Qwen3.5-9B"), ("qwen3.6-27b", "Qwen3.6-27B"))
ROWS = (
    ("chat", "chat template, thinking off"),
    ("nochat", "no chat template, thinking off"),
    ("raw", "no chat template, thinking not disabled"),
)
RUNS = {("qwen3.5-9b", "chat"): "qwen35_9b_x0_necessity", ("qwen3.5-9b", "raw"): "qwen35_9b_x0_necessity",
        ("qwen3.5-9b", "nochat"): "qwen35_9b_x0_nochat_digit",
        ("qwen3.6-27b", "chat"): "x0_necessity_27b_chat", ("qwen3.6-27b", "raw"): "x0_necessity_27b_notemplate",
        ("qwen3.6-27b", "nochat"): "x0_nochat_digit_27b"}  # fmt: skip
KMATCH = {"qwen3.5-9b": "qwen35_9b_x0_kmatch", "qwen3.6-27b": "x0_kmatch_27b"}
DICT_NAME = {"jpp": "J++", "wu": "W_U", "we": "W_E", "rand": "random atoms"}
DICT_STYLE = {"jpp": ("-", "o"), "wu": ("--", "s"), "we": (":", "^"), "rand": ("-.", "v")}
MARK = {"through": dict(marker="o", fillstyle="full"), "around": dict(marker="o", fillstyle="none"),
        "mixed": dict(marker="D", fillstyle="full"), "can't tell": dict(marker="X", fillstyle="full")}  # fmt: skip
GRID, MUTED, INK = "#e8e8e8", "#7a7a7a", "#222222"
CSV_FIELDS = ("figure", "model", "run", "rendering", "subset", "layer", "reader", "dict", "k", "omp", "quantity",
              "value", "lo", "hi", "n")  # fmt: skip


class Run:
    """One X0 run's rows, cells and shares (loaded once)."""

    def __init__(self, name: str):
        self.name, self.dir = name, X.RESULTS / name
        self.manifest = json.loads((self.dir / "manifest.json").read_text())
        self.gate = (
            json.loads((self.dir / "gate.json").read_text())["gate"] if (self.dir / "gate.json").exists() else {}
        )
        self.rows = X.read_jsonl(self.dir / "outcomes.jsonl")
        self.competence = X.read_jsonl(self.dir / "competence.jsonl")
        share: dict[tuple, list[float]] = collections.defaultdict(list)
        rshare: dict[tuple, list[float]] = collections.defaultdict(list)
        for r in X.read_jsonl(self.dir / "shares.jsonl"):
            key = (r["rendering"], r["layer"], r["dict"], r["k"], r["omp"])
            share[key].append(r["share"])
            rshare[key].append(r["rand_share"])
        self.share = {k: statistics.median(v) for k, v in share.items()}
        self.rand_share = {k: statistics.median(v) for k, v in rshare.items()}
        self._cells: dict[tuple[str, str], dict] = {}

    def cells(self, rend: str, subset: str = "all") -> dict[tuple, dict]:
        if (rend, subset) not in self._cells:
            rows = [r for r in self.rows if r["rendering"] == rend and (subset == "all" or not r["upstream"])]
            self._cells[(rend, subset)] = X.cells_of(rows) if rows else {}
        return self._cells[(rend, subset)]


def load(name: str) -> Run | None:
    return Run(name) if (X.RESULTS / name / "manifest.json").exists() else None


def first_output(run: Run, rend: str) -> str:
    """The most common start of the unedited org answers (greedy, first 8 characters) and its share."""
    said = [r["greedy"][:8] for r in run.competence if r["rendering"] == rend and r["variant"] == "org"]
    if not said:
        return ""
    top, n = collections.Counter(said).most_common(1)[0]
    return f"most common start of the answer: {top!r} ({100 * n / len(said):.0f}%)"


def why_empty(run: Run | None, rend: str) -> str:
    if run is None:
        return "not run yet"
    g = run.gate.get(rend)
    if g is not None and g["cases"] and not g["pass"]:
        acc = ", ".join(f"{w} {100 * g['org_accuracy'][w]:.0f}%" for w in X.READERS)
        said = ", ".join(f"{w} {100 * g['said_accuracy'][w]:.0f}%" for w in X.READERS)
        return (f"can't test: gate failed\nunder the decisive read: {acc} (bar 80%)\ngreedy text right: {said}\n"
                f"{first_output(run, rend)}")  # fmt: skip
    if g is not None and g["cases"] and not g["enough"]:
        return f"can't test: {g['eligible']} eligible scenes (< {X.N_MIN})"
    return "running"


def contrast(run: Run, rend: str, la: int) -> list[float]:
    """C = recall excess - lookup excess at a layer (J++ k = 25), the same entity draws for both readers."""
    boot, point = {}, {}
    for w in X.READERS:
        mine = [r for r in run.rows if r["rendering"] == rend and r["layer"] == la and r["reader"] == w]
        whole = {r["scene"]: r["switched"] for r in mine if r["arm"] == "whole"}
        arm = {(r["arm"], r["scene"]): r["switched"] for r in mine
               if (r["dict"], r["k"], r["omp"]) == X.MAIN and r["arm"] in ("no_part", "no_rand")}  # fmt: skip
        ent = {r["scene"]: r["entity"] for r in mine}
        scenes = sorted(whole)
        sw = {"whole": [whole[s] for s in scenes], **{a: [arm[(a, s)] for s in scenes] for a in ("no_part", "no_rand")}}
        rr = X.resampled_rates(sw, [ent[s] for s in scenes])
        s = {k: sum(v) / len(scenes) for k, v in sw.items()}
        point[w] = float(X.dependence(s["whole"], s["no_part"]) - X.dependence(s["whole"], s["no_rand"]))
        boot[w] = X.dependence(rr["whole"], rr["no_part"]) - X.dependence(rr["whole"], rr["no_rand"])
    return [point[X.RECALL] - point[X.LOOKUP], *X.interval(boot[X.RECALL] - boot[X.LOOKUP])]


# ---- drawing --------------------------------------------------------------------------------------------------------


def style() -> Any:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts.figs import common as F

    F.apply()
    plt.rcParams.update({"axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "axes.labelsize": 10, "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 8.5})  # fmt: skip
    return plt, F


def layer_axes(ax, target: str, top_label: bool) -> None:
    grid, pred, n_layers = X.LAYERS[target], X.PREDICTED[target], pins.TARGETS[target]["n_layers"]
    ax.set_xlim(min(grid) - 1, max(grid) + 1)
    ax.set_xticks(grid)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.axvspan(pred - 0.9, pred + 0.9, color="#fff3c4", zorder=0, lw=0)
    top = ax.secondary_xaxis("top", functions=(lambda x: 100 * x / n_layers, lambda d: d * n_layers / 100))
    top.set_xticks([round(100 * la / n_layers) for la in grid[::2]])
    top.tick_params(labelsize=8, colors=MUTED)
    if top_label:
        top.set_xlabel(f"depth, % of {n_layers} layers", fontsize=9, color=MUTED)


def draw_excess(ax, run: Run, rend: str, F, subset: str = "all", ls: str = "-", band: bool = True) -> list[int]:
    """Lookup and recall excess by layer: solid over valid cells, thin dashed through invalid ones, label markers."""
    cells = run.cells(rend, subset)
    done = sorted({k[1] for k in cells})
    color = {X.LOOKUP: F.LOOKUP, X.RECALL: F.RECALL}
    for w in X.READERS:
        cs = [cells[(rend, la, w, *X.MAIN)] for la in done]
        y = np.array([c["excess"][0] for c in cs], dtype=float)
        ok = np.array([c["valid"] for c in cs])
        ax.plot(done, np.where(ok, y, np.nan), ls, color=color[w], lw=2)
        ax.plot(done, y, "--", color=color[w], lw=1, alpha=0.5)
        if band:
            ax.fill_between(done, [c["excess"][1] if c["valid"] else np.nan for c in cs],
                            [c["excess"][2] if c["valid"] else np.nan for c in cs], color=color[w], alpha=0.12, lw=0)  # fmt: skip
        for la, c in zip(done, cs, strict=True):
            if np.isfinite(c["excess"][0]):
                yv = max(c["excess"][0], -0.42)
                ax.plot(la, yv, ls="none", color=color[w], ms=7, markeredgewidth=1.5, markerfacecoloralt="white",
                        alpha=1 if c["valid"] else 0.55, **MARK[c["label"]])  # fmt: skip
                if yv != c["excess"][0]:
                    ax.annotate(f"{c['excess'][0]:.2f}", (la, yv), xytext=(4, 2), textcoords="offset points",
                                fontsize=7.5, color=color[w])  # fmt: skip
    return done


def thresholds(ax) -> None:
    for v in (X.AROUND_EXCESS, X.THROUGH_EXCESS):
        ax.axhline(v, color="#b0b0b0", lw=1, ls=":")
    ax.axhline(0, color="black", lw=0.6)


def empty(ax, text: str) -> None:
    ax.text(0.5, 0.5, text, transform=ax.transAxes, ha="center", va="center", fontsize=9.5, color=MUTED,
            bbox=dict(boxstyle="round,pad=0.6", fc="#f6f6f6", ec="#dddddd"))  # fmt: skip


def caption(fig, F, text: str) -> None:
    fig.text(0.01, 0.006, text, fontsize=8.5, color=F.CAPTION_INK, va="bottom", linespacing=1.4)


def rows_out(
    fig_name: str, run: Run, rend: str, subset: str, cells: dict, quantities=("S_whole", "Jdep", "Rdep", "excess")
):
    out = []
    for (rr, la, w, d, k, omp), c in sorted(cells.items()):
        for q in quantities:
            v = c[q] if isinstance(c[q], list) else [c[q], None, None]
            out.append({"figure": fig_name, "model": run.manifest["model"]["target"], "run": run.name, "rendering": rr,
                        "subset": subset, "layer": la, "reader": w, "dict": d, "k": k, "omp": omp, "quantity": q,
                        "value": v[0], "lo": v[1], "hi": v[2], "n": c["n"]})  # fmt: skip
    return out


def overview(out: Path, data: list[dict]) -> Path:
    plt, F = style()
    fig, axes = plt.subplots(len(ROWS), len(MODELS), figsize=(15, 13), sharey=True)
    for j, (target, label) in enumerate(MODELS):
        for i, (rend, rend_label) in enumerate(ROWS):
            ax = axes[i, j]
            layer_axes(ax, target, i == 0)
            ax.set_ylim(-0.47, 1.1)
            thresholds(ax)
            ax.set_title(f"{label} · {rend_label}", pad=22 if i == 0 else 6)
            if j == 0:
                ax.set_ylabel("excess (J++ minus random)")
            if i == len(ROWS) - 1:
                ax.set_xlabel("layer of the patch (bridge's word)")
            run = load(RUNS[(target, rend)])
            if run is not None and run.manifest.get("descriptive") and run.cells(rend):  # amendment 3
                g = run.gate[rend]
                acc = ", ".join(f"{'lookup' if w == X.LOOKUP else 'recall'} {100 * g['org_accuracy'][w]:.0f}%"
                                for w in X.READERS)  # fmt: skip
                ax.set_title(f"{label} · {rend_label} · DESCRIPTIVE (digit read, amendment 3)", pad=6, fontsize=10)
                ax.text(0.98, 0.96, f"gate (not required here): {acc}", transform=ax.transAxes, ha="right", va="top",
                        fontsize=8, color=MUTED)  # fmt: skip
            if run is None or not run.cells(rend):
                empty(ax, why_empty(run, rend))
                continue
            done = draw_excess(ax, run, rend, F)
            cells = run.cells(rend)
            data += rows_out("overview", run, rend, "all", {k: c for k, c in cells.items() if k[3:] == X.MAIN})
            for la in done:
                if X.split(cells[(rend, la, X.LOOKUP, *X.MAIN)], cells[(rend, la, X.RECALL, *X.MAIN)]):
                    ax.annotate("split", (la, 1.02), ha="center", fontsize=8, color=F.LOOKUP, weight="bold")
            pred = X.PREDICTED[target]
            if pred in done:
                c = contrast(run, rend, pred)
                v = X.verdict(cells[(rend, pred, X.LOOKUP, *X.MAIN)], cells[(rend, pred, X.RECALL, *X.MAIN)])
                data.append({"figure": "overview", "model": target, "run": run.name, "rendering": rend, "subset": "all",
                             "layer": pred, "reader": "PM-PP", "dict": "jpp", "k": X.K_MAIN, "omp": "signed",
                             "quantity": "graded_contrast_C", "value": c[0], "lo": c[1], "hi": c[2], "n": None})  # fmt: skip
                ax.text(0.02, 0.04, f"at L{pred}: rule → {v.upper()}\ngraded contrast C = {c[0]:.2f} [{c[1]:.2f}, "
                        f"{c[2]:.2f}]", transform=ax.transAxes, fontsize=9, color=INK, va="bottom",
                        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#dddddd"))  # fmt: skip
            n = sorted({c["n"] for c in cells.values()})
            ax.text(0.98, 0.04, f"n = {n[0]} scenes", transform=ax.transAxes, ha="right", fontsize=8, color=MUTED)
    handles = [plt.Line2D([], [], color=F.LOOKUP, lw=2, label="lookup"), plt.Line2D([], [], color=F.RECALL, lw=2,
               label="recall")] + [plt.Line2D([], [], ls="none", color=INK, ms=7, markeredgewidth=1.4,
               markerfacecoloralt="white", label=k, **v) for k, v in MARK.items()]  # fmt: skip
    fig.legend(handles=handles, loc="upper center", ncol=6, frameon=False, bbox_to_anchor=(0.5, 0.955))
    fig.suptitle("X0 · does removing the bridge edit's J++ part cost the lookup and the recall, beyond a random part of "
                 "the same share? · UNVERIFIED", fontsize=13, x=0.01, ha="left", weight="bold")  # fmt: skip
    caption(fig, F, "excess = J++ dependence − random dependence; dependence = 1 − S(part removed) / S(whole edit). "
            "Bands: 95% bootstrap over bridge entities.\nLabels: around = excess ≤ 0.10 (upper CI ≤ 0.20); through = J++ "
            "dependence ≥ 0.30 and excess ≥ 0.20 (lower CI ≥ 0.10); can't tell (×, dashed) = the whole edit switches "
            "< 30% or < 30 items.\nYellow: the pre-registered layer (9B L12, 27B L32); C = recall excess − lookup excess "
            "there, paired. 'split' only where the labels say lookup around and recall through at the same layer.")  # fmt: skip
    fig.tight_layout(rect=(0, 0.06, 1, 0.94), h_pad=2.2, w_pad=2.5)
    return save(fig, plt, out, "overview")


def detail(out: Path, run: Run, rend: str, data: list[dict]) -> Path:
    plt, F = style()
    target = run.manifest["model"]["target"]
    cells = run.cells(rend)
    done = sorted({k[1] for k in cells})
    color = {X.LOOKUP: F.LOOKUP, X.RECALL: F.RECALL}
    name = {X.LOOKUP: "lookup", X.RECALL: "recall"}
    data += rows_out(f"detail_{run.name}_{rend}", run, rend, "all", cells,
                     ("S_whole", "S_no_part", "S_no_rand", "Jdep", "Rdep", "excess"))  # fmt: skip
    fig, axes = plt.subplots(2, 3, figsize=(18, 10.5), sharex=True)
    (a_s, a_dep, a_ex), (a_lk, a_rc, a_sh) = axes
    for i, ax in enumerate(axes.flat):
        layer_axes(ax, target, i < 3)
    for ax in axes[1]:
        ax.set_xlabel("layer of the patch (bridge's word)")

    def c(la, w, d=X.MAIN):
        return cells[(rend, la, w, *d)]

    def ser(w, key, d=X.MAIN, i=0):
        return [c(la, w, d)[key][i] for la in done]

    for w in X.READERS:
        for key, ls, what in (("S_whole", "-", "whole edit"), ("S_no_part", "--", "J++ part removed")):
            a_s.plot(done, ser(w, key), ls, color=color[w], lw=2, marker="o" if ls == "-" else None, ms=4,
                     label=f"{name[w]}: {what}")  # fmt: skip
            a_s.fill_between(done, ser(w, key, i=1), ser(w, key, i=2), color=color[w], alpha=0.12, lw=0)
        for key, ls, what in (("Jdep", "-", "J++ part removed"), ("Rdep", ":", "random part removed")):
            a_dep.plot(done, ser(w, key), ls, color=color[w], lw=2, marker="o" if ls == "-" else None, ms=4,
                       label=f"{name[w]}: {what}")  # fmt: skip
    a_s.axhline(X.VALID_S, color="#b0b0b0", lw=1, ls=":")
    a_s.set(
        ylim=(0, 1.05), ylabel="share switched to the alt answer", title="A  How often the edit switches the answer"
    )
    a_s.legend(loc="upper right", frameon=False)
    a_dep.axhline(0, color="black", lw=0.6)
    a_dep.set(ylim=(-0.2, 1.05), ylabel="share of switches lost", title="B  Switches lost: J++ part vs random part")
    a_dep.legend(loc="upper right", frameon=False)
    draw_excess(a_ex, run, rend, F)
    thresholds(a_ex)
    a_ex.set(ylim=(-0.47, 1.1), ylabel="excess (J++ minus random)", title="C  Excess and the label at each layer")
    for ax, w, tag in ((a_lk, X.LOOKUP, "D"), (a_rc, X.RECALL, "E")):
        for d, (ls, mk) in DICT_STYLE.items():
            dd = (d, X.K_MAIN, "signed")
            ax.plot(done, ser(w, "excess", dd), ls, marker=mk, ms=4, lw=2.2 if d == "jpp" else 1.4,
                    color=color[w] if d == "jpp" else "#9a9a9a", label=DICT_NAME[d])  # fmt: skip
        thresholds(ax)
        ax.set(ylim=(-0.47, 1.1), ylabel="excess (dictionary minus its random)",
               title=f"{tag}  {name[w].capitalize()}: J++ against other dictionaries (k = 25)")  # fmt: skip
        ax.legend(loc="upper right", frameon=False, ncol=2)
    for d, (ls, mk) in DICT_STYLE.items():
        a_sh.plot(done, [run.share[(rend, la, d, X.K_MAIN, "signed")] for la in done], ls, marker=mk, ms=4,
                  color=INK if d == "jpp" else "#9a9a9a", lw=2 if d == "jpp" else 1.4, label=DICT_NAME[d])  # fmt: skip
    a_sh.set(ylim=(0, 0.45), ylabel="median share of ||Δ||² removed", title="F  How much of the edit 25 atoms take")
    a_sh.legend(loc="upper right", frameon=False, ncol=2)
    n = sorted({x["n"] for x in cells.values()})
    fig.suptitle(f"X0 · {target} · {rend} · patch at the bridge's word · n = {n[0]} scenes per cell · UNVERIFIED",
                 fontsize=13, x=0.01, ha="left", weight="bold")  # fmt: skip
    caption(fig, F, "Dependence = 1 − S(part removed) / S(whole edit); excess = a dictionary's dependence minus that of "
            "a random subspace of the same share of ||Δ||² (per item). Bands: 95% bootstrap over bridge entities.\n"
            "Labels as in the overview. Yellow: the pre-registered layer.")  # fmt: skip
    fig.tight_layout(rect=(0, 0.05, 1, 0.95), w_pad=4, h_pad=2.5)
    return save(fig, plt, out, f"detail_{run.name}_{rend}")


def kmatch(out: Path, data: list[dict]) -> Path:
    """Dependence on each dictionary against the removed share, at the pre-registered layer, chat. Added after data."""
    plt, F = style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharey=True)
    for j, (target, label) in enumerate(MODELS):
        runs = [r for r in (load(KMATCH[target]), load(RUNS[(target, "chat")])) if r is not None]
        pred = X.PREDICTED[target]
        for i, w in enumerate(X.READERS):
            ax = axes[i, j]
            ax.grid(color=GRID, lw=0.8)
            ax.set_axisbelow(True)
            ax.set_title(f"{label} · L{pred} · {'lookup' if w == X.LOOKUP else 'recall'}")
            src = runs[0] if runs else None
            if src is None or not src.cells("chat"):
                empty(ax, "not run yet")
                continue
            cells = src.cells("chat")
            ref = []
            for d, (ls, mk) in DICT_STYLE.items():
                pts = sorted((src.share[("chat", pred, d, k, omp)], c, k) for (rr, la, ww, dd, k, omp), c in cells.items()
                             if la == pred and ww == w and dd == d and omp == "signed")  # fmt: skip
                if not pts:
                    continue
                xs = [p[0] for p in pts]
                ax.plot(xs, [p[1]["Jdep"][0] for p in pts], ls, marker=mk, ms=6, lw=2.2 if d == "jpp" else 1.5,
                        color=(F.LOOKUP if w == X.LOOKUP else F.RECALL) if d == "jpp" else "#8a8a8a",
                        label=DICT_NAME[d])  # fmt: skip
                ax.fill_between(xs, [p[1]["Jdep"][1] for p in pts], [p[1]["Jdep"][2] for p in pts],
                                color=F.LOOKUP if d == "jpp" and w == X.LOOKUP else "#8a8a8a", alpha=0.08, lw=0)  # fmt: skip
                for x, c, k in pts:
                    ax.annotate(f"k={k}", (x, c["Jdep"][0]), xytext=(4, 4), textcoords="offset points", fontsize=7,
                                color=MUTED)  # fmt: skip
                    ref.append((x, c["Rdep"][0]))
                    data.append({"figure": "kmatch", "model": target, "run": src.name, "rendering": "chat",
                                 "subset": "all", "layer": pred, "reader": w, "dict": d, "k": k, "omp": "signed",
                                 "quantity": "Jdep_vs_share", "value": c["Jdep"][0], "lo": c["Jdep"][1],
                                 "hi": c["Jdep"][2], "n": c["n"]})  # fmt: skip
            ref.sort()
            ax.plot([r[0] for r in ref], [r[1] for r in ref], ".", color="#c0c0c0", ms=5,
                    label="random subspace, same share")  # fmt: skip
            ax.axhline(0, color="black", lw=0.6)
            ax.set(xlim=(0, None), ylim=(-0.15, 1.05))
            if i == 1:
                ax.set_xlabel("median share of ||Δ||² removed")
            if j == 0:
                ax.set_ylabel("dependence (share of switches lost)")
            ax.legend(loc="upper left", frameon=False, fontsize=8)
            ax.text(0.98, 0.03, f"run {src.name}", transform=ax.transAxes, ha="right", fontsize=7.5, color=MUTED)
    fig.suptitle("X0 · added after data · is it J++ or any dictionary, at an equal removed share? · UNVERIFIED",
                 fontsize=13, x=0.01, ha="left", weight="bold")  # fmt: skip
    caption(fig, F, "Each point: one dictionary at one k (signed OMP over the letter-token atoms), its dependence against "
            "the median share of ||Δ||² it removes; grey dots: a random subspace of the same share (each point's own "
            "null).\nAt an equal removed share the random subspace is the same reference for every dictionary. Bands: "
            "95% bootstrap over bridge entities. Chat, the pre-registered layer.")  # fmt: skip
    fig.tight_layout(rect=(0, 0.05, 1, 0.95), h_pad=2.5)
    return save(fig, plt, out, "kmatch")


def kcurve(out: Path, data: list[dict]) -> Path:
    """Excess against the number of atoms k, per dictionary, at the pre-registered layer (chat; the k-match runs).
    Added after data."""
    plt, F = style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharey=True)
    for j, (target, label) in enumerate(MODELS):
        run = load(KMATCH[target])
        pred = X.PREDICTED[target]
        for i, w in enumerate(X.READERS):
            ax = axes[i, j]
            ax.grid(color=GRID, lw=0.8)
            ax.set_axisbelow(True)
            ax.set_title(f"{label} · L{pred} · {'lookup' if w == X.LOOKUP else 'recall'}")
            if run is None or not run.cells("chat"):
                empty(ax, "not run yet")
                continue
            cells = run.cells("chat")
            for d, (ls, mk) in DICT_STYLE.items():
                pts = sorted((k, c) for (rr, la, ww, dd, k, omp), c in cells.items()
                             if la == pred and ww == w and dd == d and omp == "signed")  # fmt: skip
                ks = [k for k, _ in pts]
                col = (F.LOOKUP if w == X.LOOKUP else F.RECALL) if d == "jpp" else "#8a8a8a"
                ax.plot(ks, [c["excess"][0] for _, c in pts], ls, marker=mk, ms=6, lw=2.2 if d == "jpp" else 1.5,
                        color=col, label=DICT_NAME[d])  # fmt: skip
                ax.fill_between(ks, [c["excess"][1] for _, c in pts], [c["excess"][2] for _, c in pts], color=col,
                                alpha=0.10, lw=0)  # fmt: skip
                for k, c in pts:
                    sh = run.share[("chat", pred, d, k, "signed")]
                    if d == "jpp":
                        ax.annotate(f"share {sh:.2f}", (k, c["excess"][0]), xytext=(5, 6), textcoords="offset points",
                                    fontsize=7.5, color=col)  # fmt: skip
                    data.append({"figure": "kcurve", "model": target, "run": run.name, "rendering": "chat",
                                 "subset": "all", "layer": pred, "reader": w, "dict": d, "k": k, "omp": "signed",
                                 "quantity": "excess", "value": c["excess"][0], "lo": c["excess"][1],
                                 "hi": c["excess"][2], "n": c["n"]})  # fmt: skip
            thresholds(ax)
            ax.set_xscale("log")
            ax.set_xticks([25, 50, 100, 200], ["25", "50", "100", "200"])
            ax.minorticks_off()
            ax.set(ylim=(-0.3, 1.0))
            if i == 1:
                ax.set_xlabel("atoms removed, k (log scale)")
            if j == 0:
                ax.set_ylabel("excess (dictionary minus a random subspace of its share)")
            ax.legend(loc="upper left", frameon=False, fontsize=8, ncol=2)
            ax.text(0.98, 0.03, f"run {run.name}", transform=ax.transAxes, ha="right", fontsize=7.5, color=MUTED)
    fig.suptitle("X0 · added after data · excess against the number of atoms, per dictionary · UNVERIFIED",
                 fontsize=13, x=0.01, ha="left", weight="bold")  # fmt: skip
    caption(fig, F, "Each dictionary's 25-200 atoms (signed OMP over the letter-token atoms) removed at the "
            "pre-registered layer; excess = its dependence minus that of a random subspace of the same share, per "
            "item.\nJ++ points carry the median share of ||Δ||² removed. Dotted lines: around ≤ 0.10, through ≥ 0.20. "
            "Bands: 95% bootstrap over bridge entities. Chat.")  # fmt: skip
    fig.tight_layout(rect=(0, 0.05, 1, 0.95), h_pad=2.5)
    return save(fig, plt, out, "kcurve")


def share_scatter(out: Path, data: list[dict]) -> Path:
    """J++ share of ||Δ||² against J++ dependence across valid layers (chat). Added after data."""
    plt, F = style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    for ax, (target, label) in zip(axes, MODELS, strict=True):
        run = load(RUNS[(target, "chat")])
        ax.grid(color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        ax.set_title(f"{label} · chat")
        if run is None:
            empty(ax, "not run yet")
            continue
        cells = run.cells("chat")
        for w in X.READERS:
            pts = [(run.share[("chat", la, *X.MAIN)], c["Jdep"][0], la) for (rr, la, ww, *d), c in sorted(cells.items())
                   if ww == w and tuple(d) == X.MAIN and c["valid"]]  # fmt: skip
            xs, ys = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
            r = float(np.corrcoef(xs, ys)[0, 1]) if len(pts) >= 3 else float("nan")
            col = F.LOOKUP if w == X.LOOKUP else F.RECALL
            ax.plot(xs, ys, "o", color=col, ms=7, label=f"{'lookup' if w == X.LOOKUP else 'recall'} (Pearson r = "
                    f"{r:.2f}, {len(pts)} valid layers)")  # fmt: skip
            for x, y, la in pts:
                ax.annotate(f"L{la}", (x, y), xytext=(4, 3), textcoords="offset points", fontsize=7.5, color=col)
                data.append({"figure": "share", "model": target, "run": run.name, "rendering": "chat", "subset": "all",
                             "layer": la, "reader": w, "dict": "jpp", "k": X.K_MAIN, "omp": "signed",
                             "quantity": "Jdep_vs_jpp_share", "value": y, "lo": None, "hi": x, "n": None})  # fmt: skip
        ax.set(xlabel="J++ share of ||Δ||² (median over items)", ylim=(-0.05, 1.05))
        ax.legend(loc="lower right", frameon=False)
    axes[0].set_ylabel("J++ dependence")
    fig.suptitle("X0 · added after data · does the J++ dependence track how much of the edit J++ takes? · UNVERIFIED",
                 fontsize=13, x=0.01, ha="left", weight="bold")  # fmt: skip
    caption(fig, F, "One point per layer with a valid cell (whole edit switches ≥ 30% and ≥ 30 items), J++ at k = 25. "
            "On the 9B the share and the depth fall together, so share and depth cannot be told apart there.")  # fmt: skip
    fig.tight_layout(rect=(0, 0.05, 1, 0.94))
    return save(fig, plt, out, "share")


def asked_first(out: Path, data: list[dict]) -> Path:
    """Excess by layer on all items vs the asked-first subset (chat). Added after data."""
    plt, F = style()
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)
    for ax, (target, label) in zip(axes, MODELS, strict=True):
        layer_axes(ax, target, True)
        ax.set_ylim(-0.47, 1.1)
        thresholds(ax)
        run = load(RUNS[(target, "chat")])
        if run is None:
            empty(ax, "not run yet")
            continue
        draw_excess(ax, run, "chat", F, "all", "-", band=False)
        draw_excess(ax, run, "chat", F, "asked_first", ":", band=False)
        data += rows_out("asked_first", run, "chat", "asked_first",
                         {k: c for k, c in run.cells("chat", "asked_first").items() if k[3:] == X.MAIN})  # fmt: skip
        n_all = sorted({c["n"] for c in run.cells("chat").values()})[0]
        n_first = sorted({c["n"] for c in run.cells("chat", "asked_first").values()})[0]
        ax.set_title(f"{label} · chat · all items (solid, n = {n_all}) vs asked-first (dotted, n = {n_first})",
                     fontsize=10, pad=22)  # fmt: skip
        ax.set_xlabel("layer of the patch (bridge's word)")
    axes[0].set_ylabel("excess (J++ minus random)")
    handles = [plt.Line2D([], [], color=F.LOOKUP, lw=2, label="lookup"), plt.Line2D([], [], color=F.RECALL, lw=2,
               label="recall")] + [plt.Line2D([], [], ls="none", color=INK, ms=7, markeredgewidth=1.4,
               markerfacecoloralt="white", label=k, **v) for k, v in MARK.items()]  # fmt: skip
    fig.legend(handles=handles, loc="upper center", ncol=6, frameon=False, bbox_to_anchor=(0.5, 0.93))
    fig.suptitle("X0 · added after data · does the upstream change in Δ matter? (asked-first: the asked person's pick "
                 "comes before the other changed pick) · UNVERIFIED", fontsize=12, x=0.01, ha="left", weight="bold")  # fmt: skip
    caption(fig, F, "The alt swaps two people's picks; where the other changed sentence comes first, Δ at the asked word "
            "can carry that upstream change. Labels per subset; × = can't tell (the whole edit switches < 30% or < 30 "
            "items).")  # fmt: skip
    fig.tight_layout(rect=(0, 0.05, 1, 0.9))
    return save(fig, plt, out, "asked_first")


def save(fig, plt, out: Path, stem: str) -> Path:
    path = out / f"{stem}.png"
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)
    print(path, flush=True)
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None, help="overview detail kmatch kcurve share asked_first")
    ap.add_argument("--publish", action="store_true", help="also copy the PNGs and data.csv to figures/x0_necessity/")
    a = ap.parse_args()
    want = set(a.only or ("overview", "detail", "kmatch", "kcurve", "share", "asked_first"))
    out = X.RESULTS / f"figures-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    data: list[dict] = []
    if "overview" in want:
        overview(out, data)
    if "detail" in want:
        for key, name in RUNS.items():
            run = load(name)
            if run is not None and run.cells(key[1]):
                detail(out, run, key[1], data)
    if "kcurve" in want:
        kcurve(out, data)
    if "kmatch" in want:
        kmatch(out, data)
    if "share" in want:
        share_scatter(out, data)
    if "asked_first" in want:
        asked_first(out, data)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_FIELDS)
    w.writeheader()
    w.writerows(data)
    (out / "data.csv").write_text(buf.getvalue())
    if a.publish:  # figures/<exp>/: the copies the README shows (DEVELOPER.md), with the folder they came from
        dest = pins.REPO_ROOT / "figures" / X.EXP
        dest.mkdir(parents=True, exist_ok=True)
        for f in [*out.glob("*.png"), out / "data.csv"]:
            shutil.copy2(f, dest / f.name)
        (dest / "SOURCE.md").write_text(f"Copied from `{out.relative_to(pins.REPO_ROOT)}` by scripts/x0_figures.py "
                                        "--publish.\n")  # fmt: skip
        print(dest)
    print(out)


if __name__ == "__main__":
    main()
