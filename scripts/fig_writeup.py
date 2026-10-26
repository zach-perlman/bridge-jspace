"""fig_writeup (Zach, 2026-10-26): the write-up figures, read from the same result files as docs/digest.md (through
scripts/results_digest.py's readers, so a figure and the digest cannot disagree). Writes figures/writeup/*.png.

  fig1_knockout   M - K under the top-10 J++ removal at each model's band, with its three controls
  fig2_pointer    what the mention's J-part carries (27B, 9B, Lightning): swaps from other contexts, own name, probe
  fig3_dose       M - K and the J-part swap against the share of the residual removed (K = 10 / 30 / 100)
  fig4_lookup     the answer-position lens timeline: where the swapped entity's attribute appears
  fig5_profiles   M - K by depth (dev, all relations), the chosen band shaded

python scripts/fig_writeup.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
from scripts import results_digest as D  # noqa: E402

RES, OUT = ROOT / "results", ROOT / "figures" / "writeup"
# categorical slots 1-4 in fixed order (validated, light surface; the two light hues always carry a label and a shape)
J, LOGIT, ROT, SIZE = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
PROBE, PASTE = "#6250d6", "#898781"  # slot 7 for the probe subspace; paste is a reference, in muted ink
INK, INK2, MUTED, GRID, AXIS, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": INK2, "axes.edgecolor": AXIS, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.titlelocation": "left"})  # fmt: skip

HEAD = ["Qwen3.6-27B", "Qwen3.5-9B", "Nemotron-3.5-Lightning"]
SHORT = {"Qwen3.6-27B": "Qwen 27B", "Qwen3.5-9B": "Qwen 9B", "Nemotron-3.5-Lightning": "Nemotron Lightning",
         "Nemotron-3.5-Bolt": "Nemotron Bolt", "DeepSeek-V4-Flash": "DeepSeek V4 Flash", "Ministral-3-14B": "Ministral 14B",
         "OLMo-3-32B (base, Q&A)": "OLMo-3 32B base", "Muse-Glimmer-30B": "Muse 30B", "Qwen3.5-122B": "Qwen 122B"}  # fmt: skip
MOD = {m[0]: m for m in D.MODELS}


def style(ax, grid="x"):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.grid(axis=grid, color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def note(fig, text, y=0.01):
    fig.text(0.01, y, text, fontsize=7.5, color=MUTED, va="bottom", ha="left")


def dotrows(ax, rows, series, xlim):
    """rows: [(label, {key: (value, ci or None)})]; series: [(key, label, colour, marker)], drawn top to bottom."""
    k = len(series)
    offs = [(i - (k - 1) / 2) * 0.2 for i in range(k)]
    for r, (_, vals) in enumerate(rows):
        for (key, _lab, col, mk), off in zip(series, offs, strict=True):
            v = vals.get(key)
            if v is None:
                continue
            y = r + off
            if v[1]:
                ax.plot(v[1], [y, y], color=col, lw=2, solid_capstyle="round", zorder=2)
            ax.plot(v[0], y, mk, color=col, ms=7, mec=SURF, mew=1.5, zorder=3)
            ax.text(max(v[0], v[1][1] if v[1] else v[0]) + 1.2, y, f"{v[0]:+.0f}", va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.set_ylim(len(rows) - 0.5, -0.6)
    ax.set_xlim(*xlim)
    ax.axvline(0, color=AXIS, lw=1, zorder=1)


def fig1() -> None:
    order = ["Qwen3.6-27B", "Qwen3.5-9B", "Nemotron-3.5-Lightning", "DeepSeek-V4-Flash", "Ministral-3-14B",
             "Nemotron-3.5-Bolt", "OLMo-3-32B (base, Q&A)", "Muse-Glimmer-30B", "Qwen3.5-122B"]  # fmt: skip
    rows = []
    for m in order:
        lab, ko, band, *_r = MOD[m]
        pc = _r[4]
        g = lambda run, c: (lambda x: (x["d"], x["ci"]) if x else None)(D.mk(run, c))  # noqa: E731
        rows.append((f"{SHORT[m]}  {band}", {"j": g(ko, "paper10"), "rot": g(ko, "paper10_rot"), "u": g(ko, "unembed10"),
                                             "pc": g(pc, "paper10_pcasize") if pc else None}))  # fmt: skip
    series = [("j", "J++ lens, top 10 directions", J, "o"), ("u", "logit lens, top 10 (control)", LOGIT, "s"),
              ("rot", "J++ directions, randomly rotated (control)", ROT, "D"),
              ("pc", "same-size removal, top principal directions (control)", SIZE, "^")]  # fmt: skip
    fig, ax = plt.subplots(figsize=(10, 6.4))
    style(ax)
    dotrows(ax, rows, series, (-8, 75))
    for y in (2.5, 5.5):
        ax.axhline(y, color=GRID, lw=1.2)
    ax.set_xlabel("recall answers lost minus stated-fact answers lost (M - K), points")
    fig.legend(handles=[plt.Line2D([], [], ls="", marker=mk, color=c, ms=7, label=lab) for _k, lab, c, mk in series],
               loc="upper left", bbox_to_anchor=(0.01, 0.93), ncol=2, frameon=False, fontsize=8)  # fmt: skip
    fig.suptitle("Removing 10 J++ directions at one band breaks recalled facts, not stated ones: J-specific in three models, two families",
                 x=0.01, ha="left", fontweight="bold", fontsize=10.5)  # fmt: skip
    note(fig, "Test set, all 8 relations, all starts; one band per model, fixed on dev before the test run. 95% bootstrap over bridges (seed 0).\n"
              "Size-matched control: removes the same norm as the J++ removal along the top-256 principal directions (not run for the last four).\n"
              "Qwen 122B: by answer probability its M - K is +2 (greedy accuracy +48). OLMo: base model, Q&A format. Muse: the logit lens shares much of it.")  # fmt: skip
    fig.tight_layout(rect=(0, 0.09, 1, 0.88))
    fig.savefig(OUT / "fig1_knockout.png", dpi=180)


def fig2() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.6), sharey=True)
    # three runs, each read against its own J-part swap: (group label, [(row label, key)])
    groups = [("pointer run (amendment 51)", [("J-part swap, donor from its own passage", "p:swap"),
                                              ("J-part from one neutral sentence about D", "p:swap_neutral"),
                                              ("  the same, without the entity's own-word rows", "p:swap_noown"),
                                              ("  the same, randomly rotated", "p:swap_neutral_rot"),
                                              ("  logit-lens part of the neutral sentence", "p:swap_neutral_u"),
                                              ("whole residual of the neutral sentence (paste)", "p:paste_neutral")]),
              ("cross-relation run (amendment 47)", [("J-part from a passage on the same relation", "x:swap_srel"),
                                                     ("J-part from a passage on another relation", "x:swap_xrel")]),
              ("probe run (amendment 48; probe-valid relations)", [("J-part swap (J++ top 10)", "q:swap"),
                                                                    ("probe subspace swap (top <= 10 directions)", "q:swap_probe")])]  # fmt: skip
    look = {"p:swap": (J, "o"), "p:swap_neutral": (J, "o"), "p:swap_noown": (J, "o"), "p:swap_neutral_rot": (ROT, "D"),
            "p:swap_neutral_u": (LOGIT, "s"), "p:paste_neutral": (PASTE, "v"), "x:swap_srel": (J, "o"), "x:swap_xrel": (J, "o"),
            "q:swap": (J, "o"), "q:swap_probe": (PROBE, "P")}  # fmt: skip
    ys, labels, seps, heads, y = {}, [], [], [], 0.0
    for gi, (glab, rows) in enumerate(groups):
        if gi:
            seps.append(y - 0.1)
            y += 0.4
        heads.append((y - 0.55, glab))
        for lab, key in rows:
            ys[key] = y
            labels.append((y, lab))
            y += 1
    for ax, m in zip(axes, HEAD, strict=True):
        src = {"p": (D.load(RES / "jswap" / dict(D.POINTER)[m] / "summary.json"), "memory"),
               "x": (D.load(RES / "jswap" / MOD[m][8] / "summary.json"), "memory"),
               "q": (D.load(RES / "probe_ceiling" / MOD[m][6] / "summary.json"), "memory_valid")}  # fmt: skip
        style(ax)
        for key, yy in ys.items():
            s, fam = src[key[0]]
            c = s[f"{fam}/{key[2:]}"]
            v, ci = c["transfer"], c["ci"]
            col, mk = look[key]
            if ci:
                ax.plot(ci, [yy, yy], color=col, lw=2, solid_capstyle="round")
            ax.plot(v, yy, mk, color=col, ms=7, mec=SURF, mew=1.5, zorder=3)
            ax.text((ci[1] if ci else v) + 1.5, yy, f"{v:+.0f}", va="center", fontsize=7.5, color=INK2)
        for sy in seps:
            ax.axhline(sy, color=GRID, lw=1.2)
        for hy, hl in heads:
            ax.text(-4, hy, hl, fontsize=7.5, color=MUTED, va="center", style="italic")
        ax.axvline(0, color=AXIS, lw=1)
        ax.set_yticks([a for a, _ in labels], [b for _, b in labels])
        ax.set_ylim(y - 0.5, -1.0)
        ax.set_xlim(-5, 100)
        ax.set_title(f"{SHORT[m]}  ({MOD[m][2]})")
        ax.set_xlabel("answers moved to the donor's (transfer, points)")
    fig.suptitle("At the mention, the J-part carries which entity it is, whatever context it came from; a probe that reads the attribute does not carry it",
                 x=0.01, ha="left", fontweight="bold", fontsize=10.5)  # fmt: skip
    note(fig, "Memory finals pooled; the last token of the mention, across the model's band. Three separate runs, each with its own items: the pointer run (150 random\n"
              "per word, n 624-898), the cross-relation run (n 198-374) and the probe run (relations where the probe beats chance by >= 10 points, n 420-891).\n"
              "Transfer: % of items answering with the donor's attribute minus % with a third entity's. 95% bootstrap over bridges (seed 0).")  # fmt: skip
    fig.tight_layout(rect=(0, 0.09, 1, 0.94))
    fig.savefig(OUT / "fig2_pointer.png", dpi=180)


def fig3() -> None:
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.8))
    for ax in (a, b):
        style(ax, "both")
    # the K series
    for lab, ko_band, sw_band, size_ko, size_sw, ks in D.DOSE:
        xs, ys, rs, xs2, ys2 = [], [], [], [], []
        for k, ko, cj, cr, _cu, sw in ks:
            j, r = D.mk(ko, cj), D.mk(ko, cr)
            if j:
                xs.append(D.share(size_ko, f"jlens_top{k}"))
                ys.append(j["d"])
                rs.append(r["d"])
                a.annotate(f"K {k}", (xs[-1], ys[-1]), xytext=(5, -10), textcoords="offset points", fontsize=7, color=MUTED)
            p = D.pooled(sw)
            if p and "memory/swap" in p:
                xs2.append(D.share(size_sw, f"jlens_top{k}"))
                ys2.append(p["memory/swap"]["transfer"])
                b.annotate(f"K {k}", (xs2[-1], ys2[-1]), xytext=(5, -10), textcoords="offset points", fontsize=7, color=MUTED)
        a.plot(xs, ys, "-o", color=J, lw=2, ms=7, mec=SURF, mew=1.5)
        a.plot(xs, rs, "D", color=ROT, ms=6, mec=SURF, mew=1.2)
        a.text(xs[-1] + 0.6, ys[-1], SHORT[lab], va="center", fontsize=8.5, color=INK)
        if xs2:
            b.plot(xs2, ys2, "-o", color=J, lw=2, ms=7, mec=SURF, mew=1.5)
            b.text(xs2[-1] + 0.6, ys2[-1], f"{SHORT[lab]} ({sw_band})", va="center", fontsize=8.5, color=INK)
    # K = 10 points of the other models
    for lab, run in D.SIZE:
        if lab in [d[0] for d in D.DOSE]:
            continue
        ko = MOD[lab][1]
        j, r, x = D.mk(ko), D.mk(ko, "paper10_rot"), D.share(run, "jlens_top10")
        a.plot(x, j["d"], "o", color=J, ms=7, mec=SURF, mew=1.5)
        a.plot(x, r["d"], "D", color=ROT, ms=6, mec=SURF, mew=1.2)
        a.text(x + 0.6, j["d"], SHORT[lab], va="center", fontsize=8.5, color=INK)
        if lab in dict(D.POINTER):
            s = D.load(RES / "jswap" / dict(D.POINTER)[lab] / "summary.json")
            b.plot(x, s["memory/swap"]["transfer"], "o", color=J, ms=7, mec=SURF, mew=1.5)
            left = lab == "Qwen3.5-9B"  # beside the 27B's point: label to the left
            b.text(x - 0.6 if left else x + 0.6, s["memory/swap"]["transfer"], SHORT[lab], va="center", ha="right" if left else "left",
                   fontsize=8.5, color=INK)  # fmt: skip
    a.set_title("A  Knock-out (test): M - K, points")
    b.set_title("B  J-part swap at the mention: transfer, points")
    for ax in (a, b):
        ax.set_xlabel("share of the residual norm the top-K J++ removal takes (median over the band)")
        ax.set_xlim(0, 32)
    a.set_ylim(-3, 60)
    b.set_ylim(-3, 75)
    a.plot([], [], "D", color=ROT, ms=6, label="same K, randomly rotated (control)")
    a.plot([], [], "-o", color=J, ms=7, label="top-K J++ directions")
    a.legend(loc="upper left", frameon=False, fontsize=8)
    fig.suptitle("Fixed K is not a fixed dose: Bolt's top 10 removes far less of the residual than the others', and its effect grows with K; Ministral's does not",
                 x=0.01, ha="left", fontweight="bold", fontsize=11)  # fmt: skip
    note(fig, "K = 10 / 30 / 100 for Bolt and Ministral (amendments 52, 53); K = 10 for the others. B: memory finals pooled; Bolt and the K = 10 points at the\n"
              "knock-out band, Ministral at mid depth (L20-25), where its J++ lens reads the attribute. Rotated swaps are within 1 point of 0 at every K.\n"
              "95% bootstrap intervals in docs/digest.md.")  # fmt: skip
    fig.tight_layout(rect=(0, 0.1, 1, 0.93))
    fig.savefig(OUT / "fig3_dose.png", dpi=180)


def fig4() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.0), sharey=True)
    for ax, m in zip(axes, HEAD, strict=True):
        tl = D.load(RES / "jswap" / dict(D.POINTER)[m] / "summary.json")["timeline_memory"]
        lays = sorted({int(k.split("/L")[1]) for k in tl})
        ser = lambda c, k: [tl[f"{c}/L{la}"][k] for la in lays]  # noqa: E731
        lo, hi = map(int, MOD[m][2][1:].split("-"))
        style(ax, "y")
        ax.axvspan(lo - 0.5, hi + 0.5, color=GRID, alpha=0.7, lw=0)
        ax.text((lo + hi) / 2, 101, "edit band", ha="center", fontsize=7.5, color=MUTED)
        ax.plot(lays, ser("none", "kept"), color=INK2, lw=2, label="unedited: X's answer")
        ax.plot(lays, ser("swap_neutral", "donor"), color=J, lw=2, label="J-part from a neutral sentence about D: D's answer")
        ax.plot(lays, ser("swap", "donor"), color=J, lw=2, ls=(0, (3, 2)), label="J-part from D's passage: D's answer")
        ax.axhline(50, color=AXIS, lw=0.8, ls=":")
        ax.set_ylim(0, 104)
        ax.set_title(SHORT[m])
        ax.set_xlabel("layer (lens read at the answer position)")
        ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    axes[0].set_ylabel("% of items whose lens top pick is that answer")
    axes[0].legend(loc="upper left", frameon=False, fontsize=7.5)
    fig.suptitle("The edit is at the mention; the swapped entity's attribute appears at the answer position after the band, where the original's does",
                 x=0.01, ha="left", fontweight="bold", fontsize=11)  # fmt: skip
    note(fig, "Memory finals pooled, 150 random items per word (amendment 51); the J++ lens's top pick among the answer candidates at the answer position.")
    fig.tight_layout(rect=(0, 0.05, 1, 0.92))
    fig.savefig(OUT / "fig4_lookup.png", dpi=180)


PROFILES = [("Qwen3.6-27B", "jsuite_v2_dev_chat_profile_rs40_cand2_v1"), ("Qwen3.5-9B", "qwen35_9b_jsuite_v2_dev_chat_profile_rs40_cand2_v1"),
            ("Nemotron-3.5-Lightning", "nem35l_jsuite_v2_dev_chat_profile_rs40_cand2_v1"),
            ("Ministral-3-14B", "min14_jsuite_v2_dev_chat_profile_rs40_cand2_v1"),
            ("Nemotron-3.5-Bolt", "nem35b_jsuite_v2_dev_chat_profile_cand2_v1"),
            ("DeepSeek-V4-Flash", "dsv4f_jsuite_v2_dev_chat_profile_cand2_v1")]  # fmt: skip


def fig5() -> None:
    fig, axes = plt.subplots(2, 3, figsize=(13, 6.4), sharey=True)
    for ax, (m, run) in zip(axes.flat, PROFILES, strict=True):
        s = D.load(RES / "ablate_v2" / "profile" / f"{run}.json")
        man = D.load(RES / "ablate_v2" / run / "manifest.json") or {}
        bands = sorted(s["bands"].values(), key=lambda b: b["depth"][0])
        mid = [100 * (b["depth"][0] + b["depth"][1]) / 2 for b in bands]
        style(ax, "y")
        lo, hi = map(int, MOD[m][2][1:].split("-"))
        n = s["n_layers"]
        ax.axvspan(100 * lo / n, 100 * (hi + 1) / n, color=GRID, alpha=0.7, lw=0)
        for c, col, mk, lab in (("paper10", J, "o", "J++ top 10"), ("unembed10", LOGIT, "s", "logit lens top 10"),
                                ("paper10_rot", ROT, "D", "J++ rotated")):  # fmt: skip
            y = [b[c]["M-K"] for b in bands]
            ax.plot(mid, y, "-", color=col, lw=2, label=lab, marker=mk, ms=5, mec=SURF, mew=1)
            bad = [i for i, b in enumerate(bands) if b[c]["loss"]["K"] >= 20]  # stated facts break too: not a split
            ax.plot([mid[i] for i in bad], [y[i] for i in bad], mk, color=col, mfc=SURF, ms=6, mew=1.5, ls="")
        ax.axhline(0, color=AXIS, lw=1)
        sampled = "all relations, 40 random per word" if man.get("sample_per_word") else "first 40 per word (countries only)"
        ax.set_title(f"{SHORT[m]}  (band {MOD[m][2]})", fontsize=9.5)
        ax.text(0.01, 0.97, sampled, transform=ax.transAxes, fontsize=7, color=MUTED, va="top")
        ax.set_xlim(0, 100)
    for ax in axes[1]:
        ax.set_xlabel("depth of the 1/8-wide removal window (% of layers, midpoint)")
    for ax in axes[:, 0]:
        ax.set_ylabel("M - K, points (dev)")
    axes[0, 0].legend(loc="upper right", frameon=False, fontsize=7.5)
    fig.suptitle("M - K by depth (dev): large and J-specific at mid depth in the Qwens and Lightning, small or late elsewhere",
                 x=0.01, ha="left", fontweight="bold", fontsize=11)  # fmt: skip
    note(fig, "Dev set (disjoint from test); top-10 removal in windows 1/8 of the layers wide, overlapping; no intervals drawn (n ~80 per final per window). Shaded: the band\n"
              "used on test. The all-relation picks match it except the 9B's: L16-19 (its test band L12-16 was carried over from the first facts set). Hollow: stated facts (K) also lose >= 20 points.",
         y=0.005)  # fmt: skip
    fig.tight_layout(rect=(0, 0.06, 1, 0.94))
    fig.savefig(OUT / "fig5_profiles.png", dpi=180)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in (fig1, fig2, fig3, fig4, fig5):
        f()
        print(f.__name__, "ok")
