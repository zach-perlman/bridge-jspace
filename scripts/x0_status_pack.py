"""x0_status_pack: four plain-language X0 figures for a status update (Dan, 24 Oct), from existing rows only. Writes
figures/status_2026-10-24/{f1_readers, f2_depth, f3_dictionaries, f4_order, f5_atoms, f6_digits, f7_probe}.png and data.csv. UNVERIFIED.

F1  the pre-registered layers (9B L12, 27B L32): flips lost (points of all items) without the J++ part and without a
    random part of the same size, per reader; the rule's verdict and the graded contrast C under each model.
F2  extra flips lost by relative depth, lookup and recall, valid cells only.
F3  extra flips lost against the share of the change removed: J++, and W_U / W_E / random atoms as one grey band.
F4  the share of lookups the whole edit flips, locker sentence before vs after the pick sentence.
F5  extra flips lost against the number of J++ atoms removed (25-200), at the pre-registered layer.
F6  the digit check: J++ over letter tokens vs every token, and the digit directions alone (locker-before).
F7  the probes at the bridge's word (9B, 27B): the answer digit, the locker sentence's index, the bridge's identity.
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
          ("qwen3.6-27b", "Qwen3.6-27B", "x0_necessity_27b_chat", "x0_kmatch_27b"),
          ("qwen3.5-122b-a10b", "Qwen3.5-122B", "qwen35_122b_x0_necessity_r2", "qwen35_122b_x0_necessity_r2"))  # fmt: skip
RUNS = ", ".join(m[2] for m in MODELS)
BIG = (
    "122B: FP8 weights, mixture of experts, J++ fitted on the bf16 weights, 2x H100 (hardware gate 0.998); its k-curve, "
    "dictionaries and digit arm come from its X0 run (k = 25-100)."
)
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
    fig, axes = plt.subplots(1, len(MODELS), figsize=(18, 6.2), sharey=True)
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
        ax.text(0.5, -0.15, f"{label.split('-')[1]}, layer {la}: {verdict}", transform=ax.transAxes, ha="center",
                fontsize=12, weight="bold")  # fmt: skip
        ax.grid(axis="y", color="#e8e8e8")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("flips lost (percentage points of all items)")
    axes[0].set_ylim(0, 70)
    handles = [plt.Rectangle((0, 0), 1, 1, color=F.LOOKUP), plt.Rectangle((0, 0), 1, 1, color=F.RECALL),
               plt.Rectangle((0, 0), 1, 1, color=grey)]  # fmt: skip
    labels = ["lookup: J++ part removed", "recall: J++ part removed", "random part of the same size removed"]
    head(fig, "Removing the J++ part costs recall far more than lookup",
         "At the layers fixed before the run, removing the J++ part of the bridge change costs recalls many flips "
         "and lookups few.\nA flip = the answer changes to the edited bridge's answer. Extra loss = flips lost without the "
         "J++ part minus flips lost without a random part of the same size.", handles, labels)  # fmt: skip
    foot(fig, [f"n = 200 scenes per model (both readers on the same items); {CI}. Unverified. {BIG}",
               "Verdict by the rule fixed in advance (lookup extra loss ≤ 0.10 and recall dependence ≥ 0.30). Runs: "
               f"results/x0_necessity/: {RUNS}."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.08, 1, 0.86))
    fig.savefig(OUT / "f1_readers.png", dpi=150, facecolor="white")
    plt.close(fig)


def f2(plt, F, color, grey) -> None:
    """Extra flips lost by relative depth, lookup and recall, valid cells only; the 'not needed' band; the values at
    the pre-registered layer."""
    fig, axes = plt.subplots(1, len(MODELS), figsize=(18, 5.8), sharey=True)
    invalid = []
    for ax, (target, label, run, _) in zip(axes, MODELS, strict=True):
        r = XF.Run(run)
        cells = r.cells("chat")
        n_layers = pins.TARGETS[target]["n_layers"]
        layers = sorted({k[1] for k in cells})
        ax.axhspan(0, X.AROUND_EXCESS, color="#f1f1f1", lw=0, zorder=0)
        ax.text(0.99, X.AROUND_EXCESS / 2, "counts as 'not needed'", transform=ax.get_yaxis_transform(), ha="right",
                va="center", fontsize=8.5, color="#888888")  # fmt: skip
        ax.axhline(X.THROUGH_EXCESS, color="#bbbbbb", lw=0.8, ls=":")
        ax.text(0.99, X.THROUGH_EXCESS + 0.01, "counts as 'needed'", transform=ax.get_yaxis_transform(), ha="right",
                va="bottom", fontsize=8.5, color="#888888")  # fmt: skip
        ax.axhline(0, color="black", lw=0.6)
        series = {}
        for w in X.READERS:
            pts = [(100 * la / n_layers, cells[("chat", la, w, *X.MAIN)]) for la in layers]
            bad = [la for la in layers if not cells[("chat", la, w, *X.MAIN)]["valid"]]
            if bad:
                invalid.append(f"{label.split('-')[1]} {NAME[w]}s at layers {bad[0]}-{bad[-1]}" if len(bad) > 1
                               else f"{label.split('-')[1]} {NAME[w]}s at layer {bad[0]}")  # fmt: skip
            d = [x for x, c in pts if c["valid"]]
            y = [c["excess"][0] for _, c in pts if c["valid"]]
            ax.fill_between(d, [c["excess"][1] for _, c in pts if c["valid"]], [c["excess"][2] for _, c in pts if c["valid"]],
                            color=color[w], alpha=0.13, lw=0)  # fmt: skip
            ax.plot(d, y, "-o", color=color[w], lw=2.2, ms=4)
            series[w] = dict(zip(d, y, strict=True))
            for x, c in pts:
                lo, hi = c["excess"][1], c["excess"][2]
                record("f2", target, run, round(x * n_layers / 100), w, "extra loss", c["excess"][0], lo, hi, c["n"])
        both = sorted(set(series[X.LOOKUP]) & set(series[X.RECALL]))
        ax.fill_between(both, [series[X.LOOKUP][x] for x in both], [series[X.RECALL][x] for x in both], color="#9e9e9e",
                        alpha=0.08, lw=0)  # fmt: skip
        pred = X.PREDICTED[target]
        pd = 100 * pred / n_layers
        ax.axvline(pd, color="#999999", lw=1, ls="--")
        lk, rc = cells[("chat", pred, X.LOOKUP, *X.MAIN)], cells[("chat", pred, X.RECALL, *X.MAIN)]
        ax.annotate(f"layer {pred}:\nlookup {lk['excess'][0]:.2f}\nrecall {rc['excess'][0]:.2f}", (pd, 0.42), xytext=(-6, 0),
                    textcoords="offset points", fontsize=10, va="center", ha="right",
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85))  # fmt: skip
        top = ax.secondary_xaxis(
            "top", functions=(lambda x, n=n_layers: x * n / 100, lambda la, n=n_layers: 100 * la / n)
        )
        top.set_xticks(layers[::2])
        top.tick_params(labelsize=8, colors="#888888")
        top.set_xlabel("layer", fontsize=8.5, color="#888888")
        ax.set_title(label, pad=24)
        ax.set_xlabel("depth (% of the model's layers)")
        ax.grid(color="#eeeeee")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("extra flips lost\nvs. a random part of the same size")
    axes[0].set_ylim(-0.2, 1.0)
    h = [plt.Line2D([], [], color=F.LOOKUP, lw=2.2), plt.Line2D([], [], color=F.RECALL, lw=2.2)]
    head(fig, "27B: both readers depend on the J++ part up to L26; from L28 only recall does",
         "9B: recall depends more at every layer. 122B: both readers depend on it up to L30; at L33 only recall does. "
         "Extra flips lost = flips lost when the J++ part of the change is removed minus flips lost when a random part of "
         "the same size is removed (share of the edit's flips). Dashed line: the layer fixed before the run.", h,
         ["lookup", "recall"])  # fmt: skip
    foot(fig, [f"Not enough flips to measure (the whole edit flips < 30% or < 30 items), not drawn: {'; '.join(invalid)}.",
               f"n = 200 scenes per layer; {CI}. Unverified. On the 27B the lookup's profile tracks the share of the change "
               "J++ takes (Spearman 0.79). No chat template: can't test (the models open a think block or answer in "
               f"markdown). {BIG} Runs: {RUNS}."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.10, 1, 0.85))
    fig.savefig(OUT / "f2_depth.png", dpi=150, facecolor="white")
    plt.close(fig)


def f5(plt, F, color, grey) -> None:
    """Extra flips lost against the number of J++ atoms removed, at the pre-registered layer (the k-match runs)."""
    fig, axes = plt.subplots(1, len(MODELS), figsize=(18, 5.6), sharey=True)
    for ax, (target, label, _, kmatch) in zip(axes, MODELS, strict=True):
        r = XF.Run(kmatch)
        la = X.PREDICTED[target]
        cells = r.cells("chat")
        ax.axhspan(0, X.AROUND_EXCESS, color="#f1f1f1", lw=0, zorder=0)
        ax.axhline(X.THROUGH_EXCESS, color="#bbbbbb", lw=0.8, ls=":")
        ax.axhline(0, color="black", lw=0.6)
        for w in X.READERS:
            pts = sorted((k, c) for (rr, l2, ww, d, k, omp), c in cells.items()
                         if l2 == la and ww == w and d == "jpp" and omp == "signed")  # fmt: skip
            ks = [k for k, _ in pts]
            ax.fill_between(ks, [c["excess"][1] for _, c in pts], [c["excess"][2] for _, c in pts], color=color[w],
                            alpha=0.13, lw=0)  # fmt: skip
            ax.plot(ks, [c["excess"][0] for _, c in pts], "-o", color=color[w], lw=2.2, ms=5)
            for k, c in pts:
                record("f5", target, kmatch, la, w, f"extra loss, J++ k={k}", c["excess"][0], c["excess"][1],
                       c["excess"][2], c["n"])  # fmt: skip
                last = k == max(ks)
                ax.annotate(f"{c['excess'][0]:.2f}", (k, c["excess"][0]),
                            xytext=(8, 0) if last else (0, 8 if w == X.RECALL else -15), textcoords="offset points",
                            ha="left" if last else "center", va="center" if last else "baseline", fontsize=9,
                            color=color[w])  # fmt: skip
        ax.set_xscale("log")
        ax.set_xticks([25, 50, 100, 200], ["25", "50", "100", "200"])
        ax.minorticks_off()
        ax.set_title(f"{label}, layer {la}")
        ax.set_xlabel("J++ atoms removed")
        ax.grid(color="#eeeeee")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("extra flips lost\nvs. a random part of the same size")
    axes[0].set_ylim(-0.3, 1.0)
    h = [plt.Line2D([], [], color=F.LOOKUP, lw=2.2, marker="o"), plt.Line2D([], [], color=F.RECALL, lw=2.2, marker="o")]
    head(fig, "On the 27B, with more J++ atoms the lookup needs J++ too",
         "The J++ part grown from 25 to 200 atoms at the layer fixed before the run. The 9B's and the 122B's lookups stay "
         "at or below a random part of the same size at every size; the 27B's rises to the recall's level.", h,
         ["lookup", "recall"])  # fmt: skip
    foot(fig, [f"n = 200 scenes per point; {CI}. Light band: 0 to 0.10, counts as 'not needed'; dotted line: 0.20, "
               f"counts as 'needed'. Unverified. Descriptive, added after the data. {BIG} Runs: qwen35_9b_x0_kmatch, "
               "x0_kmatch_27b, qwen35_122b_x0_necessity_r2."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.06, 1, 0.82))
    fig.savefig(OUT / "f5_atoms.png", dpi=150, facecolor="white")
    plt.close(fig)


DIGIT = {"qwen3.5-9b": "qwen35_9b_x0_digit_r2", "qwen3.6-27b": "x0_digit_27b_r2",
         "qwen3.5-122b-a10b": "qwen35_122b_x0_necessity_r2"}  # fmt: skip


def f6(plt, F, color, grey) -> None:
    """The digit check, locker-before items: extra flips lost with J++ over letter tokens vs every token (digits
    included) at 25 / 50 / 100 atoms, and with the 10 digit directions alone."""
    import json

    fig, axes = plt.subplots(1, len(MODELS), figsize=(18, 5.6), sharey=True)
    xs = {"jppdig": 0, 25: 1, 50: 2, 100: 3}
    for ax, (target, label, _, _) in zip(axes, MODELS, strict=True):
        run = DIGIT[target]
        path = sorted((X.RESULTS / run).glob("strata-*/strata.json"))[-1]
        rows = [s for s in json.loads(path.read_text())["strata"]
                if s["feature"] == "org locker vs asked pick" and s["value"] == "before" and s["omp"] == "signed"]  # fmt: skip
        ax.axhspan(0, X.AROUND_EXCESS, color="#f1f1f1", lw=0, zorder=0)
        ax.axhline(X.THROUGH_EXCESS, color="#bbbbbb", lw=0.8, ls=":")
        ax.axhline(0, color="black", lw=0.6)
        for w in X.READERS:
            for d, ls in (("jpp", "-"), ("jppall", "--")):
                pts = sorted((s["k"], s) for s in rows if s["reader"] == w and s["dict"] == d)
                x = [xs[k] for k, _ in pts]
                ax.plot(x, [s["excess"][0] for _, s in pts], ls, marker="o", color=color[w], lw=2.2 if d == "jpp" else 1.6,
                        ms=5, alpha=1 if d == "jpp" else 0.8)  # fmt: skip
                for k, s in pts:
                    record("f6", target, run, X.PREDICTED[target], w, f"extra loss, {d} k={k}, locker before",
                           s["excess"][0], s["excess"][1], s["excess"][2], s["n"])  # fmt: skip
            dig = next(s for s in rows if s["reader"] == w and s["dict"] == "jppdig")
            ax.errorbar(xs["jppdig"], dig["excess"][0], yerr=[[dig["excess"][0] - dig["excess"][1]],
                        [dig["excess"][2] - dig["excess"][0]]], fmt="s", color=color[w], ms=7, capsize=3)  # fmt: skip
            record("f6", target, run, X.PREDICTED[target], w, "extra loss, digit directions only, locker before",
                   dig["excess"][0], dig["excess"][1], dig["excess"][2], dig["n"])  # fmt: skip
        ax.set_xticks(list(xs.values()), ["10 digit\ndirections only", "25 atoms", "50 atoms", "100 atoms"])
        ax.set_title(f"{label}, layer {X.PREDICTED[target]}")
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("extra flips lost\nvs. a random part of the same size")
    axes[0].set_ylim(-0.3, 1.0)
    h = [plt.Line2D([], [], color=F.LOOKUP, lw=2.2, marker="o"), plt.Line2D([], [], color=F.RECALL, lw=2.2, marker="o"),
         plt.Line2D([], [], color="#777777", lw=2.2), plt.Line2D([], [], color="#777777", lw=1.6, ls="--")]  # fmt: skip
    head(fig, "Adding the digit tokens to J++ changes nothing",
         "Items where the locker sentence comes before the pick sentence (where lookups flip). J++ over letter-bearing "
         "tokens (as in X0) and over every token, digits included, give the same extra loss; the 10 digit directions alone "
         "give none.", h, ["lookup", "recall", "J++, letter tokens", "J++, every token"])  # fmt: skip
    foot(fig, [f"n = 85-101 scenes per point (locker-before items of the X0 scenes); {CI}. Light band: 0 to "
               "0.10, counts as 'not needed'; dotted line: 0.20, counts as 'needed'. Unverified. Descriptive, added after "
               "the data (the pre-stated reading: if digits made the lookup 'needed', X0's lookup result was the excluded "
               f"digit). {BIG} Runs: qwen35_9b_x0_digit_r2, x0_digit_27b_r2, qwen35_122b_x0_necessity_r2."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.07, 1, 0.80))
    fig.savefig(OUT / "f6_digits.png", dpi=150, facecolor="white")
    plt.close(fig)


PROBES = {"qwen3.5-9b": ("Qwen3.5-9B", "qwen35_9b_x0_probe"), "qwen3.6-27b": ("Qwen3.6-27B", "x0_probe_27b")}


def f7(plt, F, color, grey) -> None:
    """The probes on the X0 items (descriptive): accuracy per target, locker before vs after, beside the best baseline."""
    import json

    from scripts import x0_probe as P

    targets = list(P.TARGETS)
    fig, axes = plt.subplots(1, len(PROBES), figsize=(14, 5.6), sharey=True)
    for ax, (target, (label, run)) in zip(axes, PROBES.items(), strict=True):
        blob = json.loads(sorted((P.RESULTS / run).glob("probe-*/probe.json"))[-1].read_text())
        rows = {(r["target"], r["stratum"]): r for r in blob["rows"] if r["subset"] == "x0"}
        for i, tg in enumerate(targets):
            for j, order in enumerate(("before", "after")):
                r = rows[(tg, order)]
                x = i * 2.6 + j
                v, lo, hi = r["probe"]
                base = max([r["chance"]] + [r[k][0] for k in ("majority", "structure", "layout") if k in r])
                ax.bar(x, v, width=0.9, color=F.LOOKUP if order == "before" else "#c9b6dd", edgecolor="white")
                ax.errorbar(x, v, yerr=[[v - lo], [hi - v]], color="#333333", capsize=3, lw=1)
                ax.plot([x - 0.45, x + 0.45], [base, base], color="black", lw=1.6)
                ax.text(x, hi + 0.03, f"{v:.2f}", ha="center", fontsize=10)
                record("f7", target, run, blob["manifest"]["layer"], "-", f"probe accuracy, {tg}, locker {order}", v, lo,
                       hi, r["n"])  # fmt: skip
                record("f7", target, run, blob["manifest"]["layer"], "-", f"best baseline, {tg}, locker {order}", base)
        ax.set_xticks([i * 2.6 + 0.5 for i in range(len(targets))], ["answer digit", "which sentence\nholds the locker",
                                                                     "bridge identity\n(control)"])  # fmt: skip
        ax.set_title(f"{label}, layer {blob['manifest']['layer']}")
        ax.set_ylim(0, 1.1)
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("cross-validated accuracy")
    h = [plt.Rectangle((0, 0), 1, 1, color=F.LOOKUP), plt.Rectangle((0, 0), 1, 1, color="#c9b6dd"),
         plt.Line2D([], [], color="black", lw=1.6)]  # fmt: skip
    head(fig, "The bridge word holds where its locker is; the locker number is not detected at this n",
         "A linear probe at the bridge word (org run, X0 items) reads which sentence holds the bridge's locker when that "
         "sentence comes before the pick; the answer digit is not detected at this n.", h,
         ["locker sentence before the pick", "after the pick", "best baseline (chance, majority, pick index, layout)"])  # fmt: skip
    foot(fig, ["n = 99-101 scenes per bar; (a) and (b) cross-validated by bridge entity, (c) by scene; " + CI + ". The "
               "identity control reaches only 0.67-0.87 here: the probes are data-starved (a run on 1,500 fresh scenes is "
               "done, unopened). Unverified. Descriptive, added after the data. Runs: results/x0_probe/x0_probe_27b, "
               "qwen35_9b_x0_probe."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.08, 1, 0.84))
    fig.savefig(OUT / "f7_probe.png", dpi=150, facecolor="white")
    plt.close(fig)


def f3(plt, F, color, grey) -> None:
    fig, axes = plt.subplots(2, len(MODELS), figsize=(18, 9), sharey=True)
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
                ax.plot(xs_d, [p[1]["excess"][0] for p in pts[d]], "-o" if len(xs_d) == 1 else "-", color="#9e9e9e", lw=1,
                        ms=4)  # fmt: skip
                if len(xs_d) == 1:  # one atom count only (the 122B): its interval as an error bar
                    c = pts[d][0][1]
                    ax.errorbar(xs_d, [c["excess"][0]], yerr=[[c["excess"][0] - c["excess"][1]], [c["excess"][2] - c["excess"][0]]],
                                color="#9e9e9e", capsize=2, lw=1)  # fmt: skip
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
    head(fig, "It is J++, not any dictionary; the 27B lookup needs more J++ atoms, the 122B's does not",
         "Each dictionary's 25-200 atoms removed at the pre-registered layer. Extra flips lost = flips lost minus those "
         "lost to a random part of the same size.", h,
         ["J++ (lookup)", "J++ (recall)", "logit lens (W_U), input embeddings (W_E), random atoms"])  # fmt: skip
    foot(fig, [f"n = 200 scenes per point; {CI}; grey = each of the three other dictionaries with its interval. "
               f"Unverified. {BIG} Runs: qwen35_9b_x0_kmatch, x0_kmatch_27b, qwen35_122b_x0_necessity_r2."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.06, 1, 0.89))
    fig.savefig(OUT / "f3_dictionaries.png", dpi=150, facecolor="white")
    plt.close(fig)


def f4(plt, F, color, grey) -> None:
    from bridge_jspace.stats import wilson

    fig, ax = plt.subplots(figsize=(13, 5.8))
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
            labels.append(f"locker {order}\npick")
            record(
                "f4", target, run, la, X.LOOKUP, f"share flipped by the whole edit, locker {order} pick", p, lo, hi, n
            )
        ax.text(i * 3 + 0.5, -0.17, f"{label}, layer {la}", transform=ax.get_xaxis_transform(), ha="center",
                va="top", fontsize=11, weight="bold")  # fmt: skip
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
               f"after the data. Runs: {RUNS}."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.07, 1, 0.86))
    fig.savefig(OUT / "f4_order.png", dpi=150, facecolor="white")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt, F, color, grey = style()
    f1(plt, F, color, grey)
    f2(plt, F, color, grey)
    f3(plt, F, color, grey)
    f4(plt, F, color, grey)
    f5(plt, F, color, grey)
    f6(plt, F, color, grey)
    f7(plt, F, color, grey)
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
