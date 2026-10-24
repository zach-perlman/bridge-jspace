"""x0_status_pack: four plain-language X0 figures for a status update (Dan, 24 Oct), from existing rows only. Writes
figures/status_2026-10-24/{f1_readers, f2_depth, f3_dictionaries, f4_order, f5_atoms, f6_digits, f7_probe, f8_address}.png and data.csv. UNVERIFIED.

F1  the pre-registered layers (9B L12, 27B L32): flips lost (points of all items) without the J++ part and without a
    random part of the same size, per reader; the rule's verdict and the graded contrast C under each model.
F2  extra flips lost by relative depth, lookup and recall, valid cells only.
F3  extra flips lost against the share of the change removed: J++, and W_U / W_E / random atoms as one grey band.
F4  the share of lookups the whole edit flips, locker sentence before vs after the pick sentence.
F5  extra flips lost against the number of J++ atoms removed (25-200), at the pre-registered layer.
F6  the digit check: J++ over letter tokens vs every token, and the digit directions alone (locker-before).
F7  the probes at the bridge's word (9B, 27B; 1,500 fresh scenes): the answer digit, the locker sentence, identity.
F8  the probe's address read on patched states: the J++ part of the change vs the rest (single-change pairs).
F9  the address readout follows the item's first mention (the duplicate pick).
F10 the graded contrast C under the two-change and the one-change edit.
F11 the parts of the change (word, J++ without the word, PCA, J++).
F12 the mass-mean address and value subspaces.
F13 X0b: pooled and by format.
F14 PCA at J++'s share and the word-orthogonal J++ part.
F15 J++, the pointer directions and the layer's main directions, per reader.
F16 X4: the lookup per key form and D per entity.
F17 X0b's items: word, J++ without the word, J++.
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
    "122B: FP8 weights, mixture of experts, J++ fitted on the bf16 weights, 2x H100 (hardware gate 0.998); its curve "
    "over the number of J++ directions, the dictionaries and the digit check come from its main-test run (25-100)."
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
    """The figure's small print, without run names (Dan, 25 Oct: they belong in the README's run table and data.csv)."""
    import re

    lines = [re.sub(r"\s*Runs?: .*$", "", line, flags=re.S) for line in lines]
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


PROBES = {"qwen3.5-9b": ("Qwen3.5-9B", "qwen35_9b_x0_probe_v4"), "qwen3.6-27b": ("Qwen3.6-27B", "x0_probe_v4_27b")}
AMNESIC = {"qwen3.5-9b": ("Qwen3.5-9B", "qwen35_9b_x0_amnesic"), "qwen3.6-27b": ("Qwen3.6-27B", "x0_amnesic_27b")}


def f7(plt, F, color, grey) -> None:
    """The probes on the X0 items (descriptive): accuracy per target, locker before vs after, beside the best baseline."""
    import json

    from scripts import x0_probe as P

    targets = list(P.TARGETS)
    fig, axes = plt.subplots(1, len(PROBES), figsize=(14, 5.6), sharey=True)
    for ax, (target, (label, run)) in zip(axes, PROBES.items(), strict=True):
        blob = json.loads(sorted((P.RESULTS / run).glob("probe-*/probe.json"))[-1].read_text())
        rows = {(r["target"], r["stratum"]): r for r in blob["rows"] if r["subset"] == "all"}
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
    head(fig, "The bridge word holds where its locker is, and more weakly the locker number",
         "Linear probes at the bridge word (org run, 1,500 fresh scenes) when the locker sentence comes before the pick: "
         "which sentence holds the bridge's locker, almost always; the locker number, above chance, also with the "
         "sentence factored out. When the locker sentence comes after the pick, neither.", h,
         ["locker sentence before the pick", "after the pick", "best baseline (chance, majority, pick index, layout)"])  # fmt: skip
    foot(fig, ["n = 742-758 scenes per bar (d1_topics_v4, fresh, seed 2411); the answer digit and the locker sentence "
               "cross-validated by bridge entity, identity by scene; " + CI + ". Unverified. Descriptive, added after "
               "the data. Runs: results/x0_probe/x0_probe_v4_27b, qwen35_9b_x0_probe_v4."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.08, 1, 0.84))
    fig.savefig(OUT / "f7_probe.png", dpi=150, facecolor="white")
    plt.close(fig)


def f8(plt, F, color, grey) -> None:
    """The probe's address on the single-change pairs: how often probe (b) reads the alt bridge's locker sentence from
    the alt state and from h_org plus the J++ part of the change, or plus the rest, at 25 and 100 atoms."""
    import json

    bars = (("alt (org + Δ)", "the whole change"), ("org + J++ part, k = 25", "J++ part\n(25 directions)"),
            ("org + rest, k = 25", "the rest\n(25 directions)"), ("org + J++ part, k = 100", "J++ part\n(100 directions)"),
            ("org + rest, k = 100", "the rest\n(100 directions)"))  # fmt: skip
    fig, axes = plt.subplots(1, len(AMNESIC), figsize=(14, 5.6), sharey=True)
    pair = {}
    for ax, (target, (label, run)) in zip(axes, AMNESIC.items(), strict=True):
        from scripts.x0_details import latest_patched

        path = latest_patched(run, "address")
        blob = json.loads(path.read_text())
        res, energy = blob["results"], blob["results"]["energy"]
        pair[label] = (res["pair right"][0], blob["probe"], path.parent.name)
        for i, (key, _) in enumerate(bars):
            v, lo, hi = res[f"{key}: reads the alt's"]
            col = "#d9a441" if "J++" in key else "#9e9e9e" if "rest" in key else "#555555"
            ax.bar(i, v, width=0.7, color=col, edgecolor="white")
            ax.errorbar(i, v, yerr=[[v - lo], [hi - v]], color="#333333", capsize=3, lw=1)
            ax.text(i, hi + 0.03, f"{v:.2f}", ha="center", fontsize=10.5)
            if key in energy:
                e = energy[key]
                ax.text(i, -0.27, f"{100 * e['share_of_delta']:.0f}% of the change\n{100 * e['share_in_probe_subspace']:.1f}% of its "
                        "address", ha="center", va="top", fontsize=8.5, color="#666666", transform=ax.get_xaxis_transform())  # fmt: skip
            record("f8", target, run, "-", "-", f"reads the alt's locker sentence: {key}", v, lo, hi, blob["n"])
        ax.set_xticks(range(len(bars)), [b[1] for b in bars], fontsize=9.5)
        ax.set_title(f"{label} (n = {blob['n']} pairs)")
        ax.set_ylim(0, 1.0)
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
    axes[0].set_ylabel("probe points at the new pick's\nlocker sentence")
    head(fig, "The pointer is in the rest of the change, not in its J++ part",
         "A probe for 'which sentence holds the bridge's locker', read at the bridge word on the original state plus a "
         "part of an edit that changes one pick (both locker sentences before the pick). Under each bar: the part's share "
         "of the change, and of the change's component in the probe's own directions.")  # fmt: skip
    both = "; ".join(f"{k} {v[0]:.2f}" for k, v in pair.items())
    foot(fig, [f"Probe trained on fresh scenes' locker-before states, cross-fitted by bridge entity; {CI}. On the same pairs the probe gets both the original and the edited state "
               f"right in {both}; a layout-only classifier gets 0 by construction. Unverified. Descriptive, added after the "
               f"data. Runs: results/x0_amnesic/*/{{{', '.join(v[2] for v in pair.values())}}}."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.13, 1, 0.84))
    fig.savefig(OUT / "f8_address.png", dpi=150, facecolor="white")
    plt.close(fig)


SINGLE = {"qwen3.5-9b": "qwen35_9b_x0_single_r2", "qwen3.6-27b": "x0_single_27b_r2"}


def f9(plt, F, color, grey) -> None:
    """The duplicate pick: on the single-change pairs, what the alt state's address readout points at, by where the alt
    item's earlier mentions sit (top); the lookup's switch rate by the alt item's first earlier mention (bottom, at
    ceiling). Dan's fixes (~21:10): a legend and colours per row, the ceiling and the pooling said, the 9B read first."""
    import json

    from scripts.x0_details import latest_patched

    groups = (("after", "the other picker\ncomes after the pick"),
              ("before, the other pick is the latest earlier mention", "both earlier:\nlocker sentence first"),
              ("before, the alt locker is the latest earlier mention", "both earlier:\nother pick first"))  # fmt: skip
    top_cols = ((("alt right", "#4a7fb5", "points at the new pick's locker sentence")),
                ("alt state reads the other pick sentence", "#bdbdbd", "points at the other person's pick sentence"))  # fmt: skip
    bottom_cols = (("whole", F.LOOKUP, "lookup switched, the whole edit"),
                   ("without the J++ part", "#c9b6dd", "lookup switched, without the J++ part"))  # fmt: skip
    fig, axes = plt.subplots(2, len(AMNESIC), figsize=(14, 10), sharey="row")
    read = {}
    for col_i, (target, (label, run)) in enumerate(AMNESIC.items()):
        ax = axes[0, col_i]
        dup = json.loads(latest_patched(run, "address").read_text())["results"]["duplicate_pick_split"]
        for i, (key, _) in enumerate(groups):
            d = dup[key]
            for j, (m, col, what) in enumerate(top_cols):
                v, lo, hi = d[m]
                x = i + (j - 0.5) * 0.36
                ax.bar(x, v, width=0.34, color=col, edgecolor="white")
                ax.errorbar(x, v, yerr=[[v - lo], [hi - v]], color="#333333", capsize=3, lw=1)
                ax.text(x, hi + 0.03, f"{v:.2f}", ha="center", fontsize=10)
                record("f9", target, run, "-", "-", f"alt state {what}: {key}", v, lo, hi, d["n"])
        ax.set_xticks(range(len(groups)), [f"{g[1]}\n(n = {dup[g[0]]['n']})" for g in groups], fontsize=9.5)
        ax.set_title(f"{label}: where the probe points on the edited state", fontsize=11, pad=30)
        ax.set_ylim(0, 1.15)
        bx = axes[1, col_i]
        fm_path = sorted((X.RESULTS / SINGLE[target]).glob("first-mention-*/first_mention.json"))[-1]
        fm = [r for r in json.loads(fm_path.read_text())["rows"] if r["reader"] == X.LOOKUP]
        for i, r in enumerate(fm):
            for j, (arm, col, what) in enumerate(bottom_cols):
                v, lo, hi = r[arm]
                x = i + (j - 0.5) * 0.36
                bx.bar(x, v, width=0.34, color=col, edgecolor="white")
                bx.errorbar(x, v, yerr=[[v - lo], [hi - v]], color="#333333", capsize=3, lw=1)
                bx.text(x, hi + 0.03, f"{v:.2f}", ha="center", fontsize=10)
                record("f9", target, SINGLE[target], X.PREDICTED[target], X.LOOKUP, f"lookup {what}, first mention: "
                       f"{r['first']}", v, lo, hi, r["n"])  # fmt: skip
        bx.set_xticks(
            range(len(fm)), [f"first mention:\n{r['first']} sentence (n = {r['n']})" for r in fm], fontsize=9.5
        )
        bx.set_title(f"{label}: lookups switched to the new pick's locker", fontsize=11, pad=30)
        bx.set_ylim(0, 1.15)
        for a_ in (ax, bx):
            a_.grid(axis="y", color="#eeeeee")
            a_.set_axisbelow(True)
        other = next(r for r in fm if r["first"] == "other pick")
        read[label] = (dup[groups[2][0]]["alt state reads the other pick sentence"][0], other["whole"][0])
    axes[0, 0].set_ylabel("share of pairs")
    axes[1, 0].set_ylabel("share of lookups switched")
    axes[0, 0].legend([plt.Rectangle((0, 0), 1, 1, color=c) for _, c, _ in top_cols], [w for _, _, w in top_cols],
                      loc="lower left", bbox_to_anchor=(0, 1.01), ncol=2, frameon=False, fontsize=10)  # fmt: skip
    axes[1, 0].legend([plt.Rectangle((0, 0), 1, 1, color=c) for _, c, _ in bottom_cols], [w for _, _, w in bottom_cols],
                      loc="lower left", bbox_to_anchor=(0, 1.01), ncol=2, frameon=False, fontsize=10)  # fmt: skip
    nine, twenty_seven = read["Qwen3.5-9B"], read["Qwen3.6-27B"]
    head(fig, "The bridge word points at the item's first mention; the lookup still switches when that pointer is wrong",
         f"When the new pick was already picked by another person earlier in the scene, the probe points at that pick "
         f"sentence (no locker number in it) in {nine[0]:.2f} of the pairs on the 9B, and the lookup still switches to the "
         f"right locker in {nine[1]:.2f}; the 27B: {twenty_seven[0]:.2f} and {twenty_seven[1]:.2f}. Top: where the probe for "
         "'which sentence holds the locker' points. Bottom: lookups switched; this row sits at ceiling, so it shows that "
         "the wrong pointer does not stop the lookup, not how strongly the lookup depends on anything.")  # fmt: skip
    foot(fig, [f"Edits that change one pick, both locker sentences before the pick; probe trained on fresh scenes' "
               f"locker-before states, cross-fitted by bridge entity; {CI}. In the main test's scenes the first mention is "
               "always the locker sentence. Unverified. After the data (Dan's duplicate-pick check and "
               "cross-tab). Runs: results/x0_amnesic/*/probe-patched-* (address); results/x0_necessity/*_single_r2/"
               "first-mention-*."])  # fmt: skip
    fig.subplots_adjust(left=0.06, right=0.98, top=0.76, bottom=0.12, hspace=0.75, wspace=0.12)
    fig.savefig(OUT / "f9_first_mention.png", dpi=150, facecolor="white")
    plt.close(fig)


def f10(plt, F, color, grey) -> None:
    """The headline C (recall extra loss minus lookup extra loss) at the pre-registered layer, under the two-change edit
    (X0, pre-registered verdicts) and the one-change edit (after data), per model."""
    fig, ax = plt.subplots(figsize=(11, 5.6))
    xs, labels = [], []
    for i, (target, label, run, _) in enumerate(MODELS):
        la = X.PREDICTED[target]
        for j, (edit, src, col) in enumerate((("edit changes\ntwo picks", run, "#555555"),
                                              ("edit changes\none pick", SINGLE.get(target), "#a8a8a8"))):  # fmt: skip
            x = i * 3 + j
            xs.append(x)
            labels.append(f"{edit.split(' (')[0]}")
            if src is None:
                ax.text(x, 0.03, "not run", ha="center", fontsize=9.5, color="#888888", rotation=90, va="bottom")
                continue
            c = XF.contrast(XF.Run(src), "chat", la)
            ax.bar(x, c[0], width=0.8, color=col, edgecolor="white")
            ax.errorbar(x, c[0], yerr=[[c[0] - c[1]], [c[2] - c[0]]], color="#333333", capsize=3, lw=1)
            ax.text(x, c[2] + 0.02, f"{c[0]:.2f}", ha="center", fontsize=10.5)
            record("f10", target, src, la, "recall-lookup", f"C, {edit}", c[0], c[1], c[2])
        ax.text(i * 3 + 0.5, -0.2, f"{label}, layer {la}", transform=ax.get_xaxis_transform(), ha="center", va="top",
                fontsize=11, weight="bold")  # fmt: skip
    ax.set_xticks(xs, labels, fontsize=9.5)
    ax.axhline(0, color="black", lw=0.6)
    ax.set_ylim(0, 0.9)
    ax.set_ylabel("recall-lookup gap\n(recall's extra loss minus lookup's)")
    ax.grid(axis="y", color="#eeeeee")
    ax.set_axisbelow(True)
    head(fig, "Recall needs the J++ part far more than lookup does, on all three models",
         "The recall-lookup gap at the layer fixed in advance: how many more of its answer switches the recall loses than "
         "the lookup when the J++ part of the bridge change is removed (each against a random part of the same size).")  # fmt: skip
    foot(fig, [f"n = 200 scenes per bar; {CI}. Two picks: as fixed in advance (two people swap picks); one pick: only "
               "the asked person's pick changes (after the data; not run on the 122B). Unverified."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.1, 1, 0.82))
    fig.savefig(OUT / "f10_contrast.png", dpi=150, facecolor="white")
    plt.close(fig)


PARTS = {
    "qwen3.5-9b": ("Qwen3.5-9B, layer 12", "qwen35_9b_x0_parts"),
    "qwen3.6-27b": ("Qwen3.6-27B, layer 32", "x0_parts_27b"),
}
MASSMEAN = {"qwen3.5-9b": ("Qwen3.5-9B, layer 12", "qwen35_9b_x0_massmean"),
            "qwen3.6-27b": ("Qwen3.6-27B, layer 32", "x0_massmean_27b")}  # fmt: skip
X0B = {
    "qwen3.5-9b": ("Qwen3.5-9B, layer 12", "qwen35_9b_x0b_v2"),
    "qwen3.6-27b": ("Qwen3.6-27B, layer 32", "x0b_v2_27b"),
}


def bars(ax, groups: list[str], series: list[tuple[str, str, list]], target: str, fig_name: str, run: str) -> None:
    """Grouped bars with 95% CIs: series = (name, colour, [[v, lo, hi] or None per group])."""
    k = len(series)
    for j, (name, col, vals) in enumerate(series):
        for i, v in enumerate(vals):
            if v is None:
                continue
            x = i + (j - (k - 1) / 2) * (0.8 / k)
            ax.bar(x, v[0], width=0.8 / k * 0.95, color=col, edgecolor="white")
            ax.errorbar(x, v[0], yerr=[[v[0] - v[1]], [v[2] - v[0]]], color="#333333", capsize=3, lw=1)
            ax.text(x, max(v[2], v[0]) + 0.03, f"{v[0]:.2f}", ha="center", fontsize=9.5)
            record(fig_name, target, run, "-", name, groups[i].replace("\n", " "), v[0], v[1], v[2])
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xticks(range(len(groups)), groups, fontsize=9.5)
    ax.grid(axis="y", color="#eeeeee")
    ax.set_axisbelow(True)


def f11(plt, F, color, grey) -> None:
    """The parts of the one-change edit removed (each against a random part of its own share): the word alone, J++ with
    the word's tokens banned, the layer's top-2,000 PCA directions, J++."""
    import json

    order = (("w", "the word only"), ("jw", "J++ without\nthe word"), ("pca", "PCA of the layer\n(top 2,000)"),
             ("jpp", "J++"))  # fmt: skip
    fig, axes = plt.subplots(1, len(PARTS), figsize=(14, 5.6), sharey=True)
    for ax, (target, (label, run)) in zip(axes, PARTS.items(), strict=True):
        path = sorted((pins.RESULTS_DIR / "x0_parts" / run).glob("verdict-*/verdict.json"))[-1]
        rows = {(r["part"], r["reader"]): r for r in json.loads(path.read_text())["rows"]}
        groups = [f"{name}\n({100 * rows[(d, X.LOOKUP)]['median_share']:.0f}% of the change)" for d, name in order]
        bars(ax, groups, [("lookup", F.LOOKUP, [rows[(d, X.LOOKUP)]["excess"] for d, _ in order]),
                          ("recall", F.RECALL, [rows[(d, X.RECALL)]["excess"] for d, _ in order])], target, "f11", run)  # fmt: skip
        ax.set_title(label)
        ax.set_ylim(-0.2, 1.0)
    axes[0].set_ylabel("extra flips lost\nvs. a random part of the same size")
    h = [plt.Rectangle((0, 0), 1, 1, color=F.LOOKUP), plt.Rectangle((0, 0), 1, 1, color=F.RECALL)]
    head(fig, "The recall's loss is J++ beyond the word; the layer's PCA directions cost both readers",
         "Parts of the one-change edit removed at the pre-registered layer. The bridge word alone carries little; J++ with "
         "the bridge's own tokens banned costs the recall as much as J++; a PCA dictionary of the layer, at about twice "
         "J++'s share, costs the lookup too, so it is not reader-specific.", h, ["lookup", "recall"])  # fmt: skip
    foot(fig, [f"n = 200 single-change items per model; {CI}. 'The word only': least squares on the J++ directions of the "
               "org and alt bridge tokens and their one-token variants. The parts are not at equal shares (under each "
               "group). Unverified. Descriptive, added after the data (Dan's audit). Runs: results/x0_parts/*."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.07, 1, 0.80))
    fig.savefig(OUT / "f11_parts.png", dpi=150, facecolor="white")
    plt.close(fig)


def f12(plt, F, color, grey) -> None:
    """The mass-mean address (A) and value (V) subspaces removed from, or kept alone in, the one-change edit."""
    import json

    fig, axes = plt.subplots(1, len(MASSMEAN), figsize=(14, 5.6), sharey=True)
    for ax, (target, (label, run)) in zip(axes, MASSMEAN.items(), strict=True):
        path = sorted((pins.RESULTS_DIR / "x0_massmean" / run).glob("verdict-*/verdict.json"))[-1]
        rows = {r["reader"]: r for r in json.loads(path.read_text())["rows"]}
        share = rows[X.LOOKUP]["A"]["share"]
        groups = [
            f"remove A\n(address, {100 * share:.0f}%)",
            "remove V\n(value)",
            "remove A + V",
            "keep only A + V\n(minus random)",
        ]
        vals = {w: [rows[w]["A"]["excess"], rows[w]["V"]["excess"], rows[w]["AV"]["excess"], rows[w]["keep"]["difference"]]
                for w in X.READERS}  # fmt: skip
        bars(
            ax, groups, [("lookup", F.LOOKUP, vals[X.LOOKUP]), ("recall", F.RECALL, vals[X.RECALL])], target, "f12", run
        )
        ax.set_title(f"{label} (n = {rows[X.LOOKUP]['n']})")
        ax.set_ylim(-0.2, 1.0)
    axes[0].set_ylabel("extra flips lost (remove) or\nextra flips made (keep), vs. random")
    h = [plt.Rectangle((0, 0), 1, 1, color=F.LOOKUP), plt.Rectangle((0, 0), 1, 1, color=F.RECALL)]
    head(fig, "The mass-mean address subspace matters to the 9B's lookup, little to the 27B's",
         "Mass-mean subspaces from fresh scenes' bridge-word states: A for which sentence holds the locker (rank 4), V for the "
         "locker number (rank 8). Removed from the one-change edit, or kept alone, each against a random part of its own "
         "size. Reading pending (Dan).", h, ["lookup", "recall"])  # fmt: skip
    foot(fig, [f"Single-change items with both locker sentences before the pick; {CI}. Unverified. Descriptive, added after "
               "the data (Dan's last causal test this week). Runs: results/x0_massmean/*."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.07, 1, 0.80))
    fig.savefig(OUT / "f12_massmean.png", dpi=150, facecolor="white")
    plt.close(fig)


def f13(plt, F, color, grey) -> None:
    """X0b: the lookup's and the recall's extra loss pooled over every passing cell, and by format (locker-before)."""
    import json

    fig, axes = plt.subplots(1, len(X0B), figsize=(14, 5.6), sharey=True)
    for ax, (target, (label, run)) in zip(axes, X0B.items(), strict=True):
        root = pins.RESULTS_DIR / "x0b_generalize" / run
        v = json.loads(sorted(root.glob("verdict-*/verdict.json"))[-1].read_text())
        pred = v["predicted"]
        cells = {(c["layer"], c["reader"], c["dict"], c["k"], c["omp"]): c for c in v["cells"]}
        cross = {
            (r["format"], r["order"], r["reader"]): r
            for r in json.loads(sorted(root.glob("cross-*/cross.json"))[-1].read_text())
        }
        fmts = ("prose", "json", "table")
        groups = [f"pooled\n(n = {cells[(pred, X.LOOKUP, *X.MAIN)]['n']:,})",
                  *(f"{f}, locker before\n(n = {cross[(f, 'before', X.LOOKUP)]['n']})" for f in fmts)]  # fmt: skip
        series = [(name, col, [cells[(pred, w, *X.MAIN)]["excess"], *(cross[(f, "before", w)]["excess"] for f in fmts)])
                  for name, col, w in (("lookup", F.LOOKUP, X.LOOKUP), ("recall", F.RECALL, X.RECALL))]  # fmt: skip
        bars(ax, groups, series, target, "f13", run)
        ax.set_title(f"{label}: rule fixed in advance {v['verdict']}")
        ax.set_ylim(-0.2, 1.0)
        ax.axhspan(-0.2, X.AROUND_EXCESS, color="#f6f6f6", lw=0, zorder=0)
    axes[0].set_ylabel("extra flips lost\nvs. a random part of the same size")
    h = [plt.Rectangle((0, 0), 1, 1, color=F.LOOKUP), plt.Rectangle((0, 0), 1, 1, color=F.RECALL)]
    head(fig, "The recall-lookup gap holds in varied scenes",
         "7 topics x prose / JSON / tables x 3 difficulty levels; an edit that changes one pick; 75% of scenes with the "
         "locker sentence before the pick. Pooled over the cells where the model answers the unedited questions, and by "
         "format in locker-before scenes.", h, ["lookup", "recall"])  # fmt: skip
    foot(fig, [f"25 J++ directions at the layer fixed in advance; {CI}. Light band: 'not needed' (<= 0.10). The pooled "
               "rule (lookup extra loss <= 0.10, recall-lookup gap >= 0.20) was fixed before the run. Unverified."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.07, 1, 0.80))
    fig.savefig(OUT / "f13_x0b.png", dpi=150, facecolor="white")
    plt.close(fig)


PCAEQ = {
    "qwen3.5-9b": ("Qwen3.5-9B, layer 12", "qwen35_9b_x0_pcaeq"),
    "qwen3.6-27b": ("Qwen3.6-27B, layer 32", "x0_pcaeq_27b"),
}
MASSMEAN_LF = {"qwen3.5-9b": ("Qwen3.5-9B, layer 12", "qwen35_9b_x0_massmean_lf"),
               "qwen3.6-27b": ("Qwen3.6-27B, layer 32", "x0_massmean_lf_27b")}  # fmt: skip
X4 = {
    "qwen3.5-9b": ("Qwen3.5-9B, layer 12", "qwen35_9b_x4_patch"),
    "qwen3.6-27b": ("Qwen3.6-27B, layer 32", "x4_patch_27b"),
}
X0BPARTS = {"qwen3.5-9b": ("Qwen3.5-9B, layer 12", "qwen35_9b_x0b_parts"),
            "qwen3.6-27b": ("Qwen3.6-27B, layer 32", "x0b_parts_27b")}  # fmt: skip


def parts_figure(plt, F, runs: dict, order: tuple, fig_name: str, out: str, title: str, sub: str, note: str) -> None:
    """Grouped bars of x0_parts verdict rows (one panel per model): each part's excess per reader, its share below."""
    import json

    fig, axes = plt.subplots(1, len(runs), figsize=(14, 5.6), sharey=True)
    for ax, (target, (label, run)) in zip(axes, runs.items(), strict=True):
        path = sorted((pins.RESULTS_DIR / "x0_parts" / run).glob("verdict-*/verdict.json"))[-1]
        rows = {(r["part"], r["reader"]): r for r in json.loads(path.read_text())["rows"]}
        groups = [f"{name}\n({100 * rows[(d, X.LOOKUP)]['median_share']:.0f}% of the change)" for d, name in order]
        bars(ax, groups, [("lookup", F.LOOKUP, [rows[(d, X.LOOKUP)]["excess"] for d, _ in order]),
                          ("recall", F.RECALL, [rows[(d, X.RECALL)]["excess"] for d, _ in order])], target, fig_name, run)  # fmt: skip
        ax.set_title(f"{label} (n = {rows[(order[0][0], X.LOOKUP)]['n']})")
        ax.set_ylim(-0.2, 1.0)
    axes[0].set_ylabel("extra flips lost\nvs. a random part of the same size")
    h = [plt.Rectangle((0, 0), 1, 1, color=F.LOOKUP), plt.Rectangle((0, 0), 1, 1, color=F.RECALL)]
    head(fig, title, sub, h, ["lookup", "recall"])
    foot(fig, [f"{CI}. {note} Unverified."])
    fig.tight_layout(rect=(0, 0.07, 1, 0.80))
    fig.savefig(OUT / out, dpi=150, facecolor="white")
    plt.close(fig)


def f14(plt, F, color, grey) -> None:
    """PCA at J++'s share (k per item), J++ without the word fit orthogonal to the word, and J++ (same items, same run)."""
    parts_figure(plt, F, PCAEQ, (("pca_eq", "the layer's main\ndirections (PCA)"),
                                 ("jwo", "J++ without the\nword's directions"), ("jpp", "J++")), "f14",
                 "f14_pcaeq.png", "At the same share, the layer's main directions and J++ without the word's directions "
                 "cost the recall far less than J++",
                 "An edit that changes one pick, at the layer fixed in advance; each part against a random part of its own "
                 "share. Main directions: the layer's top 2,000 principal directions, as many per scene as match its J++ "
                 "share. J++ without the word's directions: 25 J++ directions fit to the change after its word part is taken out.",
                 "200 scenes per model. After the data.")  # fmt: skip


def f17(plt, F, color, grey) -> None:
    """X0b's items: the word part, J++ without the word (fit on the whole change), J++."""
    parts_figure(plt, F, X0BPARTS, (("w", "the word only"), ("jw", "J++ without\nthe word"), ("jpp", "J++")), "f17",
                 "f17_x0b_parts.png", "On X0b's 7 topics and 3 formats, the word part alone costs the recall little",
                 "X0b's single-change items at the pre-registered layer, each part against a random part of its own share. "
                 "'J++ without the word' was fit on the whole change: on X0's items it still holds about two thirds of the "
                 "word part's energy.",
                 "Descriptive, after the data (Dan's audit). Runs: results/x0_parts/*x0b_parts*.")  # fmt: skip


def f15(plt, F, color, grey) -> None:
    """The 9B's double dissociation (Dan, 25 Oct): J++, the layout-free pointer directions and the layer's PCA directions
    at J++'s share, each removed against a random part of its own share, per reader and model."""
    import json

    fig, axes = plt.subplots(1, len(PCAEQ), figsize=(14, 5.8), sharey=True)
    for ax, target in zip(axes, PCAEQ, strict=True):
        label, run = PCAEQ[target]
        path = sorted((pins.RESULTS_DIR / "x0_parts" / run).glob("verdict-*/verdict.json"))[-1]
        parts = {(r["part"], r["reader"]): r for r in json.loads(path.read_text())["rows"]}
        lf_run = MASSMEAN_LF[target][1]
        path = sorted((pins.RESULTS_DIR / "x0_massmean" / lf_run).glob("verdict-*/verdict.json"))[-1]
        lf = {r["reader"]: r for r in json.loads(path.read_text())["rows"]}
        groups = [f"J++ part\n({100 * parts[('jpp', X.LOOKUP)]['median_share']:.0f}% of the change; "
                  f"n = {parts[('jpp', X.LOOKUP)]['n']})",
                  f"pointer directions\n({100 * lf[X.LOOKUP]['Alf']['share']:.0f}%; n = {lf[X.LOOKUP]['n']})",
                  f"the layer's main directions\n({100 * parts[('pca_eq', X.LOOKUP)]['median_share']:.0f}%; "
                  f"n = {parts[('pca_eq', X.LOOKUP)]['n']})"]  # fmt: skip
        vals = {
            w: [parts[("jpp", w)]["excess"], lf[w]["Alf"]["excess"], parts[("pca_eq", w)]["excess"]] for w in X.READERS
        }
        bars(ax, groups, [("lookup", F.LOOKUP, vals[X.LOOKUP]), ("recall", F.RECALL, vals[X.RECALL])], target, "f15",
             f"{run} + {lf_run}")  # fmt: skip
        ax.set_title(label)
        ax.set_ylim(-0.2, 1.0)
    axes[0].set_ylabel("extra flips lost\nvs. a random part of the same size")
    h = [plt.Rectangle((0, 0), 1, 1, color=F.LOOKUP), plt.Rectangle((0, 0), 1, 1, color=F.RECALL)]
    head(fig, "On the 9B, removing the pointer directions costs the lookup and removing J++ costs the recall",
         "Three parts of an edit that changes one pick, each removed against a random part of its own share, at the layer "
         "fixed in advance. Pointer directions: the 4 directions that separate 'which sentence holds the locker' on fresh "
         "scenes, after each layout's average is taken out. On the 27B the pointer directions cost both readers.",
         h, ["lookup", "recall"])  # fmt: skip
    foot(fig, [f"{CI}. J++ and the main directions: 200 scenes; pointer directions: the 73 (9B) and 70 (27B) of them with "
               "both locker sentences before the pick. After the data; a replication fixed in advance is pending. "
               "Unverified."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.07, 1, 0.78))
    fig.savefig(OUT / "f15_pointer.png", dpi=150, facecolor="white")
    plt.close(fig)


def f16(plt, F, color, grey) -> None:
    """X4: the lookup's excess per key form (top), and D per entity (bottom), both models."""
    import json

    fig, axes = plt.subplots(2, len(X4), figsize=(14, 9.5), sharey="row")
    forms = (("animals", "same", "animals,\nverbatim"), ("animals", "xlang", "animals,\ntranslated"),
             ("elements", "same", "elements,\nverbatim"), ("elements", "syn", "elements,\nchemical symbol"))  # fmt: skip
    for j, (target, (label, run)) in enumerate(X4.items()):
        v = json.loads(sorted((pins.RESULTS_DIR / "x4_alias" / run).glob("verdict-*/verdict.json"))[-1].read_text())
        ax = axes[0, j]
        groups = [f"{name}\n(n = {v['cells'][f'{d}/{f}/{X.LOOKUP}']['n']})" for d, f, name in forms]
        bars(ax, groups, [("lookup", F.LOOKUP, [v["cells"][f"{d}/{f}/{X.LOOKUP}"]["excess"] for d, f, _ in forms])],
             target, "f16", run)  # fmt: skip
        ax.set_title(label)
        ax.set_ylim(-0.2, 0.5)
        ax.axhspan(-0.2, X.AROUND_EXCESS, color="#f6f6f6", lw=0, zorder=0)
        ax = axes[1, j]
        for i, domain in enumerate(("animals", "elements")):
            r = v["rules"][domain]
            ds = [e["D"] for e in r["per_entity"]]
            xs = [i + (k - (len(ds) - 1) / 2) * 0.06 for k in range(len(ds))]
            ax.plot(xs, ds, "o", color=grey, ms=7)
            d0, lo, hi = r["difference"]
            ax.errorbar(i + 0.35, d0, yerr=[[d0 - lo], [hi - d0]], fmt="D", color="black", capsize=4)
            ax.text(i + 0.42, d0, f"{d0:.2f} [{lo:.2f}, {hi:.2f}]\npositive: {r['entities_D_positive']} of {len(ds)}",
                    va="center", fontsize=9)  # fmt: skip
            record("f16", target, run, "-", "D", domain, d0, lo, hi)
        ax.axhline(0, color="black", lw=0.6)
        ax.axhline(0.20, color="#999999", lw=0.8, ls="--")
        ax.set_xticks(
            [0, 1], ["animals: translated\nminus verbatim", "elements: symbol minus\nverbatim (positive control)"]
        )
        ax.set_xlim(-0.5, 1.9)
        ax.set_ylim(-0.2, 0.5)
        ax.grid(axis="y", color="#eeeeee")
    axes[0, 0].set_ylabel("lookup: extra flips lost\nvs. a random part of the same size")
    axes[1, 0].set_ylabel("difference in the lookup's extra loss\n(dots: one per animal or element)")
    h = [plt.Rectangle((0, 0), 1, 1, color=F.LOOKUP),
         plt.Line2D([], [], marker="o", color=grey, ls=""), plt.Line2D([], [], marker="D", color="black", ls="")]  # fmt: skip
    sym = {t_: json.loads(sorted((pins.RESULTS_DIR / "x4_alias" / r_).glob("verdict-*/verdict.json"))[-1].read_text())
           ["rules"]["elements"] for t_, (_, r_) in X4.items()}  # fmt: skip
    s27 = sym["qwen3.6-27b"]
    head(fig, "With the locker key in another language, the lookup still does not need the J++ part",
         "The locker statements name the item in English, in French / Spanish / German (animals), or by chemical symbol "
         "(elements, the positive control); picks stay in English. Bottom: the lookup's extra loss with the other key "
         "minus with the English key; dashed line: 0.20, the bar set in advance.", h,
         ["lookup's extra loss", "difference, one animal or element", "difference, all"])  # fmt: skip
    foot(fig, [f"{CI}; with 8 animals and 6 elements this interval is unreliable. Light band: 'not needed' (<= 0.10). "
               f"The symbol control is below its bar on the 27B ({s27['difference'][0]:.2f} [{s27['difference'][1]:.2f}, "
               f"{s27['difference'][2]:.2f}] vs 0.20) but positive for {s27['entities_D_positive']} of "
               f"{len(s27['per_entity'])} elements; null on the 9B. Unverified."])  # fmt: skip
    fig.tight_layout(rect=(0, 0.05, 1, 0.86))
    fig.savefig(OUT / "f16_x4.png", dpi=150, facecolor="white")
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
                    ax.annotate(f"{k} directions: {c['excess'][0]:.2f}", (x, c["excess"][0]), xytext=(6, -14 if k == 100 else 6),
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
    head(fig, "Logit-lens, input-embedding and random directions do nothing; only J++ separates the readers",
         "25-200 directions of each dictionary removed at the layer fixed in advance. Extra flips lost = answer switches "
         "lost minus those lost to a random part of the same size. On the 27B, the lookup needs J++ too at 100 directions.",
         h, ["J++ (lookup)", "J++ (recall)", "logit lens, input embeddings, random directions"])  # fmt: skip
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
    head(fig, "Lookups move only when the locker sentence comes first",
         "The edit at the bridge's word flips a lookup mostly when the locker sentence comes before the pick sentence "
         "(\"The locker of the frog is 5.\" … \"Iris picked the frog.\").")  # fmt: skip
    foot(fig, ["Whole edit, no part removed; the main test's scenes at the layers fixed in advance; 95% Wilson "
               "intervals. Unverified. "
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
    f8(plt, F, color, grey)
    f9(plt, F, color, grey)
    f10(plt, F, color, grey)
    f11(plt, F, color, grey)
    f12(plt, F, color, grey)
    f13(plt, F, color, grey)
    f14(plt, F, color, grey)
    f15(plt, F, color, grey)
    f16(plt, F, color, grey)
    f17(plt, F, color, grey)
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
