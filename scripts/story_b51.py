"""README figures from batch 51's opened verdicts, redrawn for Dan's rethink (28 Oct ~21:45: "the other main graphs are
very hard to read"): one figure = one sentence, the contrast the claim rests on drawn directly, at most three series per
panel, every line labelled at its right end in its own colour on every panel (no legend box), models in the order 9B,
27B, Muse, in the mark system of scripts/story_style.py.

  fig16_dose           51.1 (x51_dose/x51_1-<UTC>/verdict.json): each part of the change added by itself at a dose;
                       A: the J++ part's switches beyond its random twin; B: the rest's lookup switches with and
                       without the address (against the rest without a random part of the address's share)
  fig14_learned        51.3 (x51_das/verdict-<UTC>/verdict.json): the learned address at four directions on all three
                       models: the switches it carries, then how much of the hand-built address lies inside it
  s14_learned_sizes    51.3: the supplement, each learned subspace's switches carried by its number of directions

Every plotted number is recorded for figures/story/data.csv with the verdict json as its source.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import story_style as S
from scripts.story_b50 import INK, LOOKUP, MODELS, NULL, SHORT, caption, rel

ADDRESS = S.MARK_COL["address"]
LABEL_PT = S.LABEL_PT
NAME = {t: name for t, _, name in MODELS} | {"nemotron-3.5-lightning": "Nemotron 3.5 Lightning"}
LT_ROW = ("nemotron-3.5-lightning", "lightning")  # batch 52: the fourth row, hollow (its gate chosen after the data)


def whisker_line(ax, xs, vals, col: str, marker: str, dx: float = 0.0, ls: str = "-", hollow: bool = False,
                 ms: float = 6.5, lw: float = 1.8) -> None:  # fmt: skip
    """One series: a line through the point estimates, each with its 95% whisker and the operation's mark."""
    x = np.asarray(xs, dtype=float) + dx
    v = np.asarray(vals, dtype=float)
    ax.plot(x, v[:, 0], color=col, ls=ls, lw=lw, zorder=3)
    for xi, (_, lo, hi) in zip(x, v, strict=True):
        ax.plot([xi, xi], [lo, hi], color=col, lw=1.1, zorder=3, solid_capstyle="butt")
    ax.plot(x, v[:, 0], marker, ls="", ms=ms, color=col, mfc="white" if hollow else col, mec=col, mew=1.4, zorder=4)


def n_tag(ax, text: str) -> None:
    ax.text(1.0, 1.02, text, transform=ax.transAxes, ha="right", va="bottom", fontsize=S.FONT - 1,
            color=S.COL["muted"], zorder=8)  # fmt: skip


def head(fig, x: float, y_in: float, bold: str, sub: str) -> None:
    """A column's heading: the part in bold, the quantity in muted type under it (y_in inches from the top)."""
    h = fig.get_figheight()
    fig.text(x, 1 - y_in / h, bold, ha="left", va="bottom", fontsize=12, weight="bold")
    fig.text(x, 1 - (y_in + 0.05) / h, sub, ha="left", va="top", fontsize=S.FONT - 1, color=S.COL["muted"])


# ---- fig16: the dose curves (51.1) ----------------------------------------------------------------------------------

LOOKUP_BAR = 0.10  # rule (i): the lookup's switches beyond random at every dose under the loss bar
RECALL_SWITCH, RECALL_BAR = 0.30, 0.20  # rule (ii): at the first dose where the recall switches >= 0.3, >= 0.2 beyond


def key(x: float) -> str:
    return f"{x:g}"


def shaded_any(blob: dict) -> bool:
    """Whether any tested model has a single-part arm whose plain-text loss passes the verdict's bar (the caption's
    one line, and the room for it, only then)."""
    arms = [f"J({key(a)},0)" for a in blob["alphas"]] + [f"J(0,{key(b)})" for b in blob["betas"]]
    return any(not m["loss"]["under_bar"][arm] for m in blob["models"] if m["status"] == "tested" for arm in arms)


def build_dose(verdict_dir: Path, out_name: str = "fig16_dose", lightning: Path | None = None,
               lightning_note: str = "") -> str:  # fmt: skip
    """Fig. 16 (51.1, fixed in advance), one row per model (9B, 27B, Muse; Lightning from its own verdict folder
    `lightning`, hollow, with `lightning_note` in the caption). A: the J++ part added by itself at dose α
    (× its size in the change): the recall's and the lookup's switches minus those of a random part of the same share
    at the same dose (paired 95% CIs); the random part is the grey band at zero, the lookup's 0.10 bar dotted; a ring
    at the first dose where the J++ part switches >= 0.3 of recalls, where rule (ii) is read. B: the rest of the
    change added by itself at dose β: the lookup's switches, and the same without the address against the same without
    a random part of the address's share (the verdict's paired control for the address; the rest's random complement
    moves the lookup about as much as the rest and is not the control for the address). Doses whose plain-text loss
    passes twice the whole change's would be shaded; the caption says how many."""
    vpath = verdict_dir / "verdict.json"
    blob = json.loads(vpath.read_text())
    alphas, betas = [float(a) for a in blob["alphas"]], [float(b) for b in blob["betas"]]
    tested = {m["target"]: m for m in blob["models"] if m["status"] == "tested"}
    srcs = dict.fromkeys(tested, rel(vpath))
    rows = [(t, m) for t, m, _ in MODELS if t in tested]
    shade = shaded_any(blob)
    if lightning is not None:
        lpath = lightning / "verdict.json"
        lblob = json.loads(lpath.read_text())
        assert (lblob["alphas"], lblob["betas"]) == (blob["alphas"], blob["betas"]), lpath
        tested |= {m["target"]: m for m in lblob["models"] if m["status"] == "tested" and m["target"] == LT_ROW[0]}
        srcs[LT_ROW[0]] = rel(lpath)
        rows += [LT_ROW] if LT_ROW[0] in tested else []
        shade = shade or shaded_any(lblob)
    plt = S.setup()
    top_in, row_in, gap_in = 1.75, 1.75, 0.7
    bottom_in = 0.75 + 0.3 * bool(shade) + 0.3 * bool(lightning_note and LT_ROW in rows)
    h = top_in + len(rows) * row_in + (len(rows) - 1) * gap_in + bottom_in
    fig, axes = plt.subplots(len(rows), 2, figsize=(S.WIDTH, h), squeeze=False,
                             gridspec_kw={"width_ratios": [1, 1], "hspace": gap_in / row_in})  # fmt: skip
    fig.subplots_adjust(left=0.085, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.14)
    S.title(fig, "By itself the J++ part moves the recall; the rest moves the lookup",
            "One part of the bridge word's change added at a dose (× its size in the change), at layer L")  # fmt: skip
    head(fig, axes[0, 0].get_position().x0, 1.05, "A  The J++ part by itself",
         "switches beyond a random part (same size)")  # fmt: skip
    head(fig, axes[0, 1].get_position().x0, 1.05, "B  The rest by itself",
         "lookups switched, with and without the address")  # fmt: skip
    shaded: list[str] = []
    for r, (target, m) in enumerate(rows):
        mod, src, hollow = tested[target], srcs[target], target == LT_ROW[0]
        n, rd, loss = mod["n"], mod["readers"], mod["loss"]
        a, b = axes[r]
        # ---- A: the J++ part by itself, beyond its random twin
        diffs = {w: [rd[w]["diff"][f"J({key(x)},0) - R({key(x)},0)"] for x in alphas] for w in ("recall", "lookup")}
        for x, v in zip(alphas, diffs["lookup"], strict=True):  # the verdict's rule (i) reads the same numbers
            assert abs(mod["rules"]["i"]["diff"][str(x)] - v[0]) < 1e-9, (target, x)
        # the band and the bar end at the last dose, so their end labels sit clear of them
        span = (0.3, alphas[-1] + 0.1)
        a.fill_between(span, [-0.02] * 2, [0.02] * 2, color=NULL, alpha=0.8, lw=0, zorder=1)
        a.plot(span, [LOOKUP_BAR] * 2, color=LOOKUP, ls=":", lw=1.2, zorder=2)
        flags = [not loss["under_bar"][f"J({key(x)},0)"] for x in alphas]
        for x, f in zip(alphas, flags, strict=True):
            if f:
                a.axvspan(x - 0.2, x + 0.2, **S.NI_SHADE)
                shaded.append(f"{SHORT[m]} α = {key(x)}")
        for w, col, dx in (("recall", INK, -0.035), ("lookup", LOOKUP, 0.035)):
            whisker_line(a, alphas, diffs[w], col, S.MARK["add"], dx=dx, hollow=hollow)
            for x, v in zip(alphas, diffs[w], strict=True):
                S.record(out_name, target, f"51.1 A: {w} switches with the J++ part by itself at dose {key(x)}, minus a "
                         "random part (same size) at the same dose", *v, n=n, source=src)  # fmt: skip
        first = mod["rules"]["ii"]["recall"]["first_alpha"]
        S.record(out_name, target, "51.1 (ii): first dose where the J++ part by itself switches >= 0.3 of recalls",
                 first, source=src)  # fmt: skip
        if first is not None:
            v = diffs["recall"][alphas.index(float(first))]
            a.plot([float(first) - 0.035], [v[0]], "o", ms=15, color=INK, mfc="none", mec=INK, mew=1.0, zorder=5)
        a.set_ylim(-0.78, 0.62)
        a.set_xlim(0.3, 4.05)
        a.spines["bottom"].set_bounds(alphas[0], alphas[-1])
        a.set_xticks(alphas, [key(x) for x in alphas])
        a.set_yticks([-0.5, 0, 0.5], ["−0.5", "0", "0.5"])
        a.grid(axis="y", color="#eeeeee")
        a.set_axisbelow(True)
        fails = [float(x) for x in mod["rules"]["i"]["alphas_failing"]]
        last = diffs["lookup"][-1][0]
        look = "lookup" if alphas[-1] not in fails else f"lookup {last:.2f}"
        S.record(out_name, target, "51.1 (i): doses where the lookup passes 0.10 beyond random", len(fails), source=src)
        S.end_labels(a, alphas[-1], [(diffs["recall"][-1][0], "recall", INK), (last, look, LOOKUP),
                                   (0.0, "random", S.COL["muted"]), (LOOKUP_BAR, "lookup bar", LOOKUP)],
                     pad=0.16)  # fmt: skip
        # ---- B: the rest by itself, with and without the address
        lk = rd["lookup"]["rate"]
        series = (("", "the rest", LOOKUP, S.MARK["add"], -0.012),
                  ("-U", "without the address", ADDRESS, S.MARK["remove"], 0.0),
                  ("-RU", "without a random part", "#8c8c8c", S.MARK["remove"], 0.012))  # fmt: skip
        ends = []
        for suffix, label, col, mk, dx in series:
            vals = [lk[f"J(0,{key(x)}){suffix}"] for x in betas]
            whisker_line(b, betas, vals, col, mk, dx=dx, hollow=hollow)
            ends.append((vals[-1][0], label, col))
            what = {"": "the rest by itself", "-U": "the rest by itself without the address",
                    "-RU": "the rest by itself without a random part of the address's share"}[suffix]  # fmt: skip
            for x, v in zip(betas, vals, strict=True):
                S.record(out_name, target, f"51.1 B: lookups switched, {what}, dose {key(x)}", *v, n=n, source=src)
        for x in betas:
            if not loss["under_bar"][f"J(0,{key(x)})"]:
                b.axvspan(x - 0.06, x + 0.06, **S.NI_SHADE)
                shaded.append(f"{SHORT[m]} β = {key(x)}")
        b.set_ylim(-0.03, 1.05)
        b.set_xlim(0.12, 2.6)
        b.spines["bottom"].set_bounds(betas[0], betas[-1])
        b.set_xticks(betas, [key(x) for x in betas])
        b.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
        b.grid(axis="y", color="#eeeeee")
        b.set_axisbelow(True)
        S.end_labels(b, betas[-1], ends, pad=0.09)
        S.record(out_name, target, "51.1: doses whose plain-text loss passes 2x the whole change's",
                 sum(not ok for ok in loss["under_bar"].values()), source=src)  # fmt: skip
        for ax in (a, b):
            n_tag(ax, f"n = {n}  {'○' if hollow else '●'}")
        a.text(0.0, 1.03, NAME[target], transform=a.transAxes, ha="left", va="bottom", fontsize=12, weight="bold")
        if r == len(rows) - 1:
            a.set_xlabel("dose of the J++ part (×)", loc="left")
            b.set_xlabel("dose of the rest (×)", loc="left")
    # Dan (21:55): definitions live in the README's Setup; one caption line only where this figure needs it
    lines = [f"Shaded: plain-text loss over twice the whole change's ({', '.join(shaded)})."] if shaded else []
    lines += [lightning_note] if lightning_note and LT_ROW in rows else []
    if lines:
        caption(fig, lines, bottom_in - 0.6)
    S.save(fig, out_name)
    return out_name


# ---- fig14: the learned address (51.3) ------------------------------------------------------------------------------

K_ADDR = 4  # the learned address's size the rules read (49.8's k, 51.3 (iii))
SAME_ADDRESS = 0.6  # 49.8 (a) / 51.3 (iii): the learned address is ours when >= 0.6 of U's energy lies inside it


def build_learned(verdict_dir: Path, out_name: str = "fig14_learned") -> str:
    """Fig. 14 (51.3, fixed in advance), one row per model (9B, 27B, Muse), at the rules' four directions. A: the
    share of test pairs whose switch the learned address carries (interchange through it): the lookup's position
    switches (orange triangle), the same for a subspace learned on shuffled pairs (grey triangle) and a random one (grey
    band), and the recall moved by the learned address (dark triangle; its random subspace, grey band). B: the share
    of the hand-built address's energy inside the learned address (orange bar), inside the shuffled-pair subspace (grey
    bar) and inside a random one (k / d, printed), against the 0.6 bar for 'the same address'. 51.3 replaces 49.8's
    9B run (more pairs) and adds the 27B and Muse; the k sweep and the readers' own subspaces are the supplement."""
    vpath = verdict_dir / "verdict.json"
    blob = json.loads(vpath.read_text())
    src, k = rel(vpath), str(K_ADDR)
    models = {m["target"]: m for m in blob["models"]}
    rows = [t for t, _, _ in MODELS if t in models]
    plt = S.setup()
    top_in, row_in, bottom_in = 1.6, 1.05, 1.05
    h = top_in + row_in * len(rows) + bottom_in
    fig, (a, b) = plt.subplots(1, 2, figsize=(S.WIDTH, h), sharey=True, gridspec_kw={"width_ratios": [1.25, 1]})
    fig.subplots_adjust(left=0.215, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.10)
    S.title(fig, "A learned address carries the position route, mostly outside the hand-built one",
            "Four directions learned to carry the lookup's position switches, read on held-out pairs", limit=80)  # fmt: skip
    head(fig, a.get_position().x0, 0.98, "A  Switches the learned address carries", "share of test pairs")
    head(fig, b.get_position().x0, 0.98, "B  The hand-built address",
         "share of its energy inside each subspace")  # fmt: skip
    dy, half = 0.19, 0.07
    ns, whole = [], []
    for i, t in enumerate(rows):
        ad = models[t]["address"]
        te, geo = ad["test"], ad["geometry"]
        y = -i
        assert models[t]["rules_49_8"]["k"] == K_ADDR, t
        # A, the lookup's sub-row: random band, shuffled-pair subspace, the learned address
        rand, shuf, own = te["random_iia"][k], te["shuffled_iia"][k], te["own_iia"][k]
        cross, cross_rand = te["recall_cross"][k], te["recall_random"][k]
        for yy, rv in ((y + dy, rand), (y - dy, cross_rand)):
            a.fill_between([rv[1] - 0.012, rv[2] + 0.012], [yy - half] * 2, [yy + half] * 2, color=NULL, alpha=0.8,
                           lw=0, zorder=1)  # fmt: skip
        for v, col, yy in ((shuf, "#8c8c8c", y + dy), (own, ADDRESS, y + dy), (cross, INK, y - dy)):
            a.plot([v[1], v[2]], [yy] * 2, color=col, lw=1.5, zorder=3, solid_capstyle="butt")
            a.plot([v[0]], [yy], S.MARK["swap"], ms=9, color=col, zorder=4)
        for what, v in (("lookups' position switches carried by the learned address", own),
                        ("lookups' position switches carried by a subspace learned on shuffled pairs", shuf),
                        ("lookups' position switches carried by a random subspace", rand),
                        ("recalls moved by the learned address", cross),
                        ("recalls moved by a random subspace", cross_rand)):  # fmt: skip
            S.record(out_name, t, f"51.3: {what}, k = {k}, address test pairs", *v, n=te["n"], source=src)
        S.record(out_name, t, "51.3: recalls moved by the whole change, address test pairs", *te["recall_moved_whole"],
                 n=te["n"], source=src)  # fmt: skip
        ns.append(te["n"])
        whole.append(te["recall_moved_whole"][0])
        # direct labels on every row, each next to its mark: the learned address's above its mark (the shuffled
        # one's whisker can reach its left)
        a.text(own[0], y + dy + 0.13, "learned address", color=ADDRESS, fontsize=LABEL_PT, ha="right", va="bottom")
        a.text(
            shuf[2] + 0.03, y + dy, "shuffled pairs", color=S.COL["muted"], fontsize=LABEL_PT, ha="left", va="center"
        )
        a.text(max(cross[2], 0.02) + 0.03, y - dy, "recall moved", color=INK, fontsize=LABEL_PT, ha="left",
               va="center")  # fmt: skip
        # B: the hand-built address's energy inside each subspace
        g, gs, gr = geo[f"R_pos_k{k}"], geo[f"shuf_pos_k{k}"], geo[f"rand_k{k}"]
        assert abs(g["cos2_U"] - models[t]["rules_51_3"]["address_cos2_U_k4"]) < 1e-9, t
        for yy, v, col, label in ((y + dy, g["cos2_U"], ADDRESS, "learned"),
                                  (y - dy, gs["cos2_U"], NULL, "shuffled pairs")):  # fmt: skip
            b.barh(yy, v, height=2 * half + 0.04, color=col, lw=0, zorder=2)
            b.text(v + 0.015, yy, f"{v:.2f} {label}", color=ADDRESS if col == ADDRESS else S.COL["muted"],
                   fontsize=LABEL_PT, va="center", ha="left")  # fmt: skip
        S.record(out_name, t, f"51.3: the hand-built address's energy inside the learned address, k = {k}", g["cos2_U"],
                 n=g["n"], source=src)  # fmt: skip
        S.record(out_name, t, f"51.3: the hand-built address's energy inside a subspace learned on shuffled pairs, "
                 f"k = {k}", gs["cos2_U"], n=gs["n"], source=src)  # fmt: skip
        S.record(out_name, t, f"51.3: the hand-built address's energy inside a random subspace (k / d), k = {k}",
                 g["random_expectation"], n=gr["n"], source=src)  # fmt: skip
    for ax in (a, b):
        ax.set_ylim(-len(rows) + 0.45, 0.55)
        ax.set_xlim(0, 1.0)
        ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.grid(axis="x", color="#eeeeee")
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
    b.axvline(SAME_ADDRESS, color="#1e1e1e", ls=":", lw=1.2, zorder=1)
    b.text(SAME_ADDRESS + 0.015, 0.5, "same address\nfrom here", color="#1e1e1e", fontsize=LABEL_PT, va="top",
           ha="left")  # fmt: skip
    a.set_yticks([-i for i in range(len(rows))], [NAME[t] for t in rows])
    a.set_xlabel("share of test pairs")
    b.set_xlabel("share of the hand-built address's energy")
    nt = ", ".join(map(str, ns))
    n_tag(a, f"n = {nt} pairs  ●")
    n_tag(b, f"n = {nt} pairs  ●")
    # Dan (21:55): one caption line, only what this figure needs (the rest is in the README's Setup)
    caption(
        fig,
        [
            f"Recall moved: the whole change itself moves the recall in {' / '.join(f'{x:.2f}' for x in whole)} of "
            "these pairs."
        ],
        bottom_in - 0.6,
    )
    S.save(fig, out_name)
    return out_name


# ---- s14: the learned subspaces by size (51.3, the supplement to Fig. 14) -------------------------------------------

SUBSPACES = (("lookup", "The lookup's own subspace", LOOKUP), ("recall", "The recall's own subspace", INK),
             ("address", "The learned address (lookup's position switches)", ADDRESS))  # fmt: skip


def build_sizes(verdict_dir: Path, out_name: str = "s14_learned_sizes") -> str:
    """Supplement to Fig. 14 (51.3): one row per learned subspace (the lookup's own and the recall's own on the pooled
    identity pairs, the learned address on the address pairs), one column per model (9B, 27B, Muse); per panel the
    share of test pairs whose switch the subspace carries by its number of directions k (the sizes 51.3 trained), the
    same learned on shuffled pairs (grey, hollow) and a random subspace (the grey band; 0.00 at every k, asserted). A
    ring on the size the rule read (the reader's chosen k on the select split; the address's four)."""
    vpath = verdict_dir / "verdict.json"
    blob = json.loads(vpath.read_text())
    src = rel(vpath)
    models = {m["target"]: m for m in blob["models"]}
    cols = [(t, m) for t, m, _ in MODELS if t in models]
    plt = S.setup()
    top_in, row_in, gap_in, bottom_in = 1.4, 1.45, 0.85, 0.75
    h = top_in + len(SUBSPACES) * row_in + (len(SUBSPACES) - 1) * gap_in + bottom_in
    fig, axes = plt.subplots(len(SUBSPACES), len(cols), figsize=(S.WIDTH, h), sharey=True, squeeze=False,
                             gridspec_kw={"hspace": gap_in / row_in})  # fmt: skip
    fig.subplots_adjust(left=0.075, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.12)
    S.title(fig, "Sixteen learned directions carry the lookup's switch; the recall needs more",
            "Share of test pairs whose switch a learned subspace carries, by its number of directions", limit=80)  # fmt: skip
    for r, (name, heading, col) in enumerate(SUBSPACES):
        for c, (t, m) in enumerate(cols):
            ax, mod = axes[r, c], models[t]
            rd = mod["identity"]["readers"]
            te, chosen = {"lookup": (rd["PP"]["test"], rd["PP"]["k"]), "recall": (rd["PM"]["test"], rd["PM"]["k"]),
                          "address": (mod["address"]["test"], K_ADDR)}[name]  # fmt: skip
            ks = sorted(int(k) for k in te["own_iia"])
            x = list(range(len(ks)))
            assert all(te["random_iia"][str(k)][0] < 0.02 for k in ks), (t, name)
            ax.fill_between([-0.3, len(ks) - 0.7], [-0.015] * 2, [0.015] * 2, color=NULL, alpha=0.8, lw=0, zorder=1)
            ends = []
            for key_, lc, hollow, label in (("own_iia", col, False, "learned"),
                                            ("shuffled_iia", "#8c8c8c", True, "shuffled")):  # fmt: skip
                vals = [te[key_][str(k)] for k in ks]
                whisker_line(ax, x, vals, lc, S.MARK["swap"], hollow=hollow, ms=6, lw=1.6)
                ends.append((vals[-1][0], label, lc))
                what = "a subspace learned on shuffled pairs" if hollow else "its own learned subspace"
                for k, v in zip(ks, vals, strict=True):
                    S.record(out_name, t, f"51.3: {name}, {what}, k = {k}: switches carried, test pairs", *v,
                             n=te["n"], source=src)  # fmt: skip
            ends.append((0.0, "random", S.COL["muted"]))
            v = te["own_iia"][str(chosen)][0]
            ax.plot([ks.index(chosen)], [v], "o", ms=14, color=col, mfc="none", mec=col, mew=1.0, zorder=5)
            S.record(out_name, t, f"51.3: {name}, the k the rule read", chosen, source=src)
            ax.set_xlim(-0.3, len(ks) - 1 + 1.25)
            ax.set_ylim(-0.03, 1.05)
            S.end_labels(ax, len(ks) - 1, ends, pad=0.22)
            ax.set_xticks(x, [str(k) for k in ks])
            ax.spines["bottom"].set_bounds(0, len(ks) - 1)
            ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
            ax.grid(axis="y", color="#eeeeee")
            ax.set_axisbelow(True)
            n_tag(ax, f"n = {te['n']}  ●")
            if c == 0:
                ax.text(0.0, 1.2, heading, transform=ax.transAxes, ha="left", va="bottom", fontsize=12,
                        weight="bold", color=col)  # fmt: skip
            ax.text(0.0, 1.03, NAME[t] if c == 0 else SHORT[m], transform=ax.transAxes, ha="left", va="bottom",
                    fontsize=S.FONT, weight="bold")  # fmt: skip
            if r == len(SUBSPACES) - 1:
                ax.set_xlabel("directions (k)")
    axes[len(SUBSPACES) // 2, 0].set_ylabel("share of test pairs")
    S.save(fig, out_name, supp=True)
    return out_name
