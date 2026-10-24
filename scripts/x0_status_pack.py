"""x0_status_pack: four plain-language X0 figures for a status update (Dan, 24 Oct), from existing rows only. Writes
figures/status_2026-10-24/{f1_readers, f2_depth, f3_dictionaries, f4_order}.png and data.csv. UNVERIFIED.

F1  the pre-registered layers (9B L12, 27B L32): flips lost (points of all items) without the J++ part and without a
    random part of the same size, per reader; the rule's verdict and the graded contrast C under each model.
F2  share of flips lost by relative depth: lookup and recall without the J++ part; grey band = without a random part.
F3  extra flips lost against the share of the change removed: J++, and W_U / W_E / random atoms as one grey band.
F4  the share of lookups the whole edit flips, locker sentence before vs after the pick sentence.
"""

from __future__ import annotations

import csv
import io
import sys
import textwrap
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_descriptive as D
from scripts import x0_figures as XF
from scripts import x0_necessity as X
from scripts import x0_strata as ST

OUT = pins.REPO_ROOT / "figures" / "status_2026-10-24"
MODELS = (("qwen3.5-9b", "Qwen3.5-9B", "qwen35_9b_x0_necessity", "qwen35_9b_x0_kmatch"),
          ("qwen3.6-27b", "Qwen3.6-27B", "x0_necessity_27b_chat", "x0_kmatch_27b"))  # fmt: skip
NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}
CI = "95% CIs: bootstrap over bridge entities (10,000 resamples)"
rows_csv: list[dict] = []


def style():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from scripts.figs import common as F

    F.apply()
    plt.rcParams.update({"axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "axes.labelsize": 11, "xtick.labelsize": 10, "ytick.labelsize": 10, "legend.fontsize": 10})  # fmt: skip
    return plt, F, {X.LOOKUP: F.LOOKUP, X.RECALL: F.RECALL}, "#bdbdbd"


def wrap(text: str, fig, size: float) -> str:
    """Wrap to the figure's width (about 1.9 characters per point of width at this font size)."""
    width = int(fig.get_figwidth() * 72 / (size * 0.56))
    return "\n".join(textwrap.fill(part, width) for part in text.split("\n"))


def head(fig, title: str, subtitle: str, handles=None, labels=None) -> None:
    """Title, subtitle, and the figure's one legend in its own row under the subtitle."""
    fig.suptitle(title, x=0.01, y=0.985, ha="left", fontsize=15, weight="bold")
    sub = wrap(subtitle, fig, 10.5)
    fig.text(0.01, 0.935, sub, ha="left", va="top", fontsize=10.5, color="#555555")
    if handles:
        y = 0.935 - 0.032 * (sub.count("\n") + 1) * 9.0 / fig.get_figheight()
        fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.005, y), ncol=len(handles), frameon=False)


def foot(fig, lines: list[str]) -> None:
    text = "\n".join(wrap(line, fig, 8.5) for line in lines)
    fig.text(0.01, 0.01, text, ha="left", va="bottom", fontsize=8.5, color="#666666", linespacing=1.4)


def record(fig_name, model, run, layer, reader, what, v, lo=None, hi=None, n=None):
    rows_csv.append({"figure": fig_name, "model": model, "run": run, "layer": layer, "reader": reader,
                     "quantity": what, "value": v, "lo": lo, "hi": hi, "n": n})  # fmt: skip


def f1(plt, F, color, grey) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2), sharey=True)
    for ax, (target, label, run, _) in zip(axes, MODELS, strict=True):
        r = XF.Run(run)
        la = X.PREDICTED[target]
        cells = D.all_cells([x for x in r.rows if x["rendering"] == "chat" and x["layer"] == la], X.N_BOOT)
        xs = np.arange(2)
        for i, w in enumerate(X.READERS):
            c = cells[("chat", la, w, *X.MAIN)]
            for j, (key, col, what) in enumerate((("drop_noD", color[w], "J++ part removed"),
                                                  ("drop_noRand", grey, "random part removed"))):  # fmt: skip
                v, lo, hi = (100 * t for t in c[key])
                x = xs[i] + (j - 0.5) * 0.36
                ax.bar(x, v, width=0.34, color=col, edgecolor="white")
                ax.errorbar(x, v, yerr=[[v - lo], [hi - v]], color="#333333", capsize=3, lw=1)
                ax.text(x, hi + 1.5, f"{v:.1f}", ha="center", fontsize=11, weight="bold" if j == 0 else "normal")
                record("f1", target, run, la, w, f"flips lost (points), {what}", v, lo, hi, c["n"])
        lk, rc = cells[("chat", la, X.LOOKUP, *X.MAIN)], cells[("chat", la, X.RECALL, *X.MAIN)]
        verdict = X.verdict(lk, rc)
        cc = XF.contrast(r, "chat", la)
        record("f1", target, run, la, "recall-lookup", "graded contrast C (excess)", cc[0], cc[1], cc[2])
        ax.set_xticks(xs, ["lookup", "recall"])
        ax.set_title(f"{label}, layer {la}")
        ax.text(0.5, -0.17, f"{label.split('-')[1]}: {verdict}   ·   recall − lookup extra loss C = {cc[0]:.2f} "
                f"[{cc[1]:.2f}, {cc[2]:.2f}]", transform=ax.transAxes, ha="center", fontsize=11)  # fmt: skip
        ax.grid(axis="y", color="#e8e8e8")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("flips lost (percentage points of all items)")
    axes[0].set_ylim(0, 70)
    handles = [plt.Rectangle((0, 0), 1, 1, color=F.LOOKUP), plt.Rectangle((0, 0), 1, 1, color=F.RECALL),
               plt.Rectangle((0, 0), 1, 1, color=grey)]  # fmt: skip
    labels = ["lookup: J++ part removed", "recall: J++ part removed", "random part of the same size removed"]
    head(fig, "Recall needs the J++ form; lookup much less",
         "At the layers fixed before the run, removing the J++-readable part of the bridge edit costs recalls many flips "
         "and lookups few.\nA flip = the answer changes to the edited bridge's answer. Extra loss = flips lost without the "
         "J++ part minus flips lost without a random part of the same size.", handles, labels)  # fmt: skip
    foot(fig, [f"n = 200 scenes per model (both readers on the same items); {CI}. Unverified.",
               "Verdict by the rule fixed in advance (lookup extra loss ≤ 0.10 and recall dependence ≥ 0.30). Runs: "
               "results/x0_necessity/qwen35_9b_x0_necessity, x0_necessity_27b_chat."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.08, 1, 0.80))
    fig.savefig(OUT / "f1_readers.png", dpi=150, facecolor="white")
    plt.close(fig)


def f2(plt, F, color, grey) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.8), sharey=True, sharex=True)
    for ax, (target, label, run, _) in zip(axes, MODELS, strict=True):
        r = XF.Run(run)
        cells = r.cells("chat")
        n_layers = pins.TARGETS[target]["n_layers"]
        layers = sorted({k[1] for k in cells})
        depth = [100 * la / n_layers for la in layers]
        valid = [(d, [cells[("chat", la, w, *X.MAIN)] for w in X.READERS]) for d, la in zip(depth, layers, strict=True)]
        valid = [(d, [c for c in cs if c["valid"]]) for d, cs in valid]
        valid = [(d, cs) for d, cs in valid if cs]
        ax.fill_between([d for d, _ in valid], [min(c["Rdep"][1] for c in cs) for _, cs in valid],
                        [max(c["Rdep"][2] for c in cs) for _, cs in valid], color=grey, alpha=0.6, lw=0)  # fmt: skip
        for w in X.READERS:
            cs = [cells[("chat", la, w, *X.MAIN)] for la in layers]
            ys = [c["Jdep"][0] for c in cs]
            ax.plot(depth, ys, "-", color=color[w], lw=2.2)
            for d, c in zip(depth, cs, strict=True):
                ax.plot(d, c["Jdep"][0], "o", ms=6, color=color[w], mfc=color[w] if c["valid"] else "white")
                v, lo, hi = c["Jdep"]
                record("f2", target, run, round(d * n_layers / 100), w, "flips lost without J++ (share)", v, lo, hi,
                       c["n"])  # fmt: skip
        pred = X.PREDICTED[target]
        pd = 100 * pred / n_layers
        ax.axvline(pd, color="#999999", lw=1, ls="--")
        lk, rc = cells[("chat", pred, X.LOOKUP, *X.MAIN)], cells[("chat", pred, X.RECALL, *X.MAIN)]
        ax.annotate(f"layer {pred}: recall {rc['Jdep'][0]:.2f}, lookup {lk['Jdep'][0]:.2f}", (pd, 1.0), xytext=(4, 0),
                    textcoords="offset points", fontsize=10, va="top")  # fmt: skip
        ax.set_title(label)
        ax.set_xlabel("depth (% of the model's layers)")
        ax.grid(color="#eeeeee")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("share of flips lost")
    axes[0].set_ylim(-0.1, 1.05)
    h = [plt.Line2D([], [], color=F.LOOKUP, lw=2.2), plt.Line2D([], [], color=F.RECALL, lw=2.2),
         plt.Rectangle((0, 0), 1, 1, color=grey, alpha=0.6)]  # fmt: skip
    head(fig, "Where in depth: recall keeps needing the J++ form; the lookup's need falls with depth",
         "Share of the edit's flips lost when the J++ part is removed, by depth. The grey band is the same for a random "
         "part of the same size;\nthe gap above it is the extra loss. Dashed line: the layer fixed before the run.", h,
         ["lookup, J++ part removed", "recall, J++ part removed", "random part removed (valid cells, both readers)"])  # fmt: skip
    foot(fig, ["Hollow markers: invalid cells (the whole edit flips < 30% or < 30 items). On the 27B the lookup's profile "
               "tracks the share of the change J++ takes (Spearman 0.79).",
               f"n = 200 scenes per layer; {CI}. Unverified. Runs: qwen35_9b_x0_necessity, x0_necessity_27b_chat."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.08, 1, 0.80))
    fig.savefig(OUT / "f2_depth.png", dpi=150, facecolor="white")
    plt.close(fig)


def f3(plt, F, color, grey) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), sharey=True)
    for j, (target, label, _, kmatch) in enumerate(MODELS):
        r = XF.Run(kmatch)
        la = X.PREDICTED[target]
        cells = r.cells("chat")
        for i, w in enumerate(X.READERS):
            ax = axes[i, j]
            pts = {d: sorted((r.share[("chat", la, d, k, "signed")], c, k) for (rr, l2, ww, dd, k, omp), c in cells.items()
                             if l2 == la and ww == w and dd == d and omp == "signed")
                   for d in ("jpp", "wu", "we", "rand")}  # fmt: skip
            for d in ("wu", "we", "rand"):
                xs_d = [p[0] for p in pts[d]]
                ax.fill_between(xs_d, [p[1]["excess"][1] for p in pts[d]], [p[1]["excess"][2] for p in pts[d]],
                                color=grey, alpha=0.45, lw=0)  # fmt: skip
                ax.plot(xs_d, [p[1]["excess"][0] for p in pts[d]], "-", color="#9e9e9e", lw=1)
            xs = [p[0] for p in pts["jpp"]]
            ax.fill_between(xs, [p[1]["excess"][1] for p in pts["jpp"]], [p[1]["excess"][2] for p in pts["jpp"]],
                            color=color[w], alpha=0.12, lw=0)  # fmt: skip
            ax.plot(xs, [p[1]["excess"][0] for p in pts["jpp"]], "-o", color=color[w], lw=2.2, ms=5)
            for x, c, k in pts["jpp"]:
                v, lo, hi = c["excess"]
                record("f3", target, kmatch, la, w, f"extra loss, J++ k={k}", v, lo, hi, c["n"])
                if k in (25, 100):
                    ax.annotate(f"{k} atoms: {c['excess'][0]:.2f}", (x, c["excess"][0]), xytext=(6, -14 if k == 100 else 6),
                                textcoords="offset points", fontsize=10, color=color[w])  # fmt: skip
            ax.axhline(0, color="black", lw=0.6)
            ax.set_title(f"{label}, layer {la}, {NAME[w]}")
            ax.grid(color="#eeeeee")
            ax.set_axisbelow(True)
            if i == 1:
                ax.set_xlabel("share of the change removed")
            if j == 0:
                ax.set_ylabel("extra flips lost\nvs. a random part of the same size")
    axes[0, 0].set_ylim(-0.3, 1.0)
    h = [plt.Line2D([], [], color=F.LOOKUP, lw=2.2, marker="o"), plt.Line2D([], [], color=F.RECALL, lw=2.2, marker="o"),
         plt.Rectangle((0, 0), 1, 1, color=grey, alpha=0.6)]  # fmt: skip
    head(fig, "It is J++, not any dictionary; the 27B lookup needs more J++ atoms",
         "Each dictionary's 25-200 atoms removed at the pre-registered layer. Extra flips lost = flips lost minus those "
         "lost to a random part of the same size.", h,
         ["J++ (lookup)", "J++ (recall)", "logit lens (W_U), input embeddings (W_E), random atoms"])  # fmt: skip
    foot(fig, [f"n = 200 scenes per point; {CI}; grey = each of the three other dictionaries with its interval. "
               "Unverified. Runs: qwen35_9b_x0_kmatch, x0_kmatch_27b."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.05, 1, 0.86))
    fig.savefig(OUT / "f3_dictionaries.png", dpi=150, facecolor="white")
    plt.close(fig)


def f4(plt, F, color, grey) -> None:
    from bridge_jspace.stats import wilson

    fig, ax = plt.subplots(figsize=(10, 5.8))
    xs, labels = [], []
    for i, (target, label, run, _) in enumerate(MODELS):
        r = XF.Run(run)
        la = X.PREDICTED[target]
        rows = [x for x in r.rows if x["rendering"] == "chat" and x["layer"] == la and x["reader"] == X.LOOKUP
                and x["arm"] == "whole"]  # fmt: skip
        cases = {c["scene"]: c for c in X.read_jsonl(r.dir / "cases.jsonl") if c["rendering"] == "chat"}
        for j, order in enumerate(("before", "after")):
            mine = [x for x in rows if ST.features(cases[x["scene"]])["org locker vs asked pick"] == order]
            k, n = sum(x["switched"] for x in mine), len(mine)
            p, lo, hi = (100 * t for t in wilson(k, n))
            x = i * 3 + j
            ax.bar(x, p, width=0.8, color=F.LOOKUP if order == "before" else "#c9b6dd", edgecolor="white")
            ax.errorbar(x, p, yerr=[[p - lo], [hi - p]], color="#333333", capsize=3, lw=1)
            ax.text(x, hi + 2, f"{p:.0f}%\n({k} of {n})", ha="center", fontsize=10.5)
            xs.append(x)
            labels.append(f"{label}, layer {la}\nlocker {order} pick")
            record(
                "f4", target, run, la, X.LOOKUP, f"share flipped by the whole edit, locker {order} pick", p, lo, hi, n
            )
    ax.set_xticks(xs, labels, fontsize=10)
    ax.set_ylim(0, 105)
    ax.set_ylabel("lookups flipped by the whole edit (%)")
    ax.grid(axis="y", color="#eeeeee")
    ax.set_axisbelow(True)
    head(fig, "What moves lookups: sentence order",
         "The edit at the bridge's word flips a lookup mostly when the locker sentence comes before the pick sentence "
         "(\"The locker of the frog is 5.\" … \"Iris picked the frog.\").")  # fmt: skip
    foot(fig, ["Whole edit, no part removed; X0 items at the pre-registered layers; 95% Wilson intervals. Unverified. "
               "Descriptive, added "
               "after the data. Runs: qwen35_9b_x0_necessity, x0_necessity_27b_chat."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.06, 1, 0.84))
    fig.savefig(OUT / "f4_order.png", dpi=150, facecolor="white")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt, F, color, grey = style()
    f1(plt, F, color, grey)
    f2(plt, F, color, grey)
    f3(plt, F, color, grey)
    f4(plt, F, color, grey)
    buf = io.StringIO()
    w = csv.DictWriter(
        buf, fieldnames=["figure", "model", "run", "layer", "reader", "quantity", "value", "lo", "hi", "n"]
    )
    w.writeheader()
    w.writerows(rows_csv)
    (OUT / "data.csv").write_text(buf.getvalue())
    print(OUT)


if __name__ == "__main__":
    main()
