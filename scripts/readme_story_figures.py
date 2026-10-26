"""README v2's figures (Dan, 25 Oct: one story, figures that read at a glance) into figures/story/ (SVG + PNG) and
figures/story/data.csv, in story_style's look. Fig. 0 and Fig. 3 are schematics (no data); the others read the run
files (X0 cells, verdicts) or docs/x0_numbers.json, and record every plotted number.

uv run python scripts/readme_story_figures.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import story_style as S
from scripts import x0_figures as XF
from scripts import x0_necessity as X

N = S.numbers()
MAIN_RUNS = {
    "9b": "qwen35_9b_x0_necessity",
    "27b": "x0_necessity_27b_chat",
    "122b": "qwen35_122b_x0_necessity_r2",
    "muse": "muse30b_x0_necessity",
}
# Muse's natural passages: the lookup switches in few of them, so its interval is too wide for a gap label (Dan, 26 Oct)
NO_GAP_LABEL = {("muse", "Natural passages")}
# Fig. 5's depth curve: Muse's main test at more layers (muse_depth, after the data), once it is in results/
DEPTH_RUNS = {"muse": "muse30b_x0_necessity_depth"}


def depth_run(m: str) -> str:
    run = DEPTH_RUNS.get(m)
    return run if run and (X.RESULTS / run / "outcomes.jsonl").exists() else MAIN_RUNS[m]


NEEDS = 0.30  # the lookup "still needs J++" where its extra loss is at least this (Dan's Q35.1 bar), for Fig. 5's shade


def latest(path: Path, pattern: str):
    found = sorted(path.glob(pattern))
    return json.loads(found[-1].read_text()) if found else None


def fig0(plt) -> None:
    """The setup: the prompt as sentence boxes, the bridge word, where the change is added, the two questions."""
    fig = plt.figure(figsize=(S.WIDTH, 3.5))
    ax = fig.add_axes((0, 0, 1, 0.9))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 40)
    ax.axis("off")
    S.title(fig, "One prompt, two questions about the same in-between word")
    sents = ["The locker of the frog is 5.", "The locker of the tick is 2.", "Iris picked the frog."]
    x = 2.0
    for i, s in enumerate(sents):
        w = 2.2 + 0.93 * len(s)
        ax.add_patch(plt.Rectangle((x, 27), w, 7, fc="#f5f5f5", ec="#bbbbbb", lw=1))
        if i == 2:
            ax.text(x + 1.1, 30.5, "Iris picked the ", va="center", fontsize=11)
            ax.text(x + 1.1 + 0.93 * 16.3, 30.5, "frog", va="center", fontsize=11, weight="bold", color="#b23b3b",
                    bbox=dict(boxstyle="round,pad=0.15", fc="#fde3e3", ec="none"))  # fmt: skip
            bx = x + 1.1 + 0.93 * 18
        else:
            ax.text(x + 1.1, 30.5, s, va="center", fontsize=11)
        x += w + 1.5
    ax.annotate("the change is added here (frog → tick, at one layer)", (bx, 26.6), (40, 19.5), fontsize=10.5,
                color="#b23b3b", ha="left", va="center",
                arrowprops=dict(arrowstyle="->", color="#b23b3b", lw=1.4))  # fmt: skip
    ax.text(bx, 36.2, "the bridge", fontsize=10, color="#b23b3b", ha="center")
    for y, name, q, a, col in ((10.5, "Lookup", "Which locker belongs to Iris's pick?", "5, written in the prompt", S.COL["lookup"]),
                               (3.0, "Recall", "How many legs does Iris's pick have?", "4, from the model's memory", S.COL["recall"])):  # fmt: skip
        ax.text(3, y, f"{name}:", fontsize=11, weight="bold", color=col, va="center")
        ax.text(15, y, q, fontsize=11, va="center")
        ax.text(62, y, f"→ {a}", fontsize=11, va="center", color=col)
    S.save(fig, "fig0_setup")


def fig1(plt) -> None:
    """Hero: per model, the lookup's and the recall's J++ extra loss in each setting, joined; the gap printed."""
    rows = [("Simple scenes,\ntwo people swap picks", "lk_excess_{m}", "rc_excess_{m}", "contrast_{m}", {}),
            ("Simple scenes, only the asked\nperson's pick changes", "single_lk_excess_{m}", "single_rc_excess_{m}",
             "single_contrast_{m}", {"9b": "after", "27b": "after"}),
            ("Matched scenes,\ntwo people swap picks", "comp_two_fmno_lk_{m}", "comp_two_fmno_rc_{m}", None,
             {"9b": "after", "27b": "after", "122b": "after", "muse": "after"}),
            ("Matched scenes, only the asked\nperson's pick changes", "comp_one_fmno_lk_{m}", "comp_one_fmno_rc_{m}",
             None, {"9b": "after", "27b": "after", "122b": "after", "muse": "after"}),
            ("Varied scenes", "x0b_lk_excess_{m}", "x0b_rc_excess_{m}", "x0b_c_{m}", {}),
            ("Natural passages", "nat_lk_excess_{m}", "nat_rc_excess_{m}", "nat_gap_{m}", {})]  # fmt: skip
    fig, axes = plt.subplots(1, len(S.MODELS), figsize=(S.WIDTH, 5.9), sharey=True)
    fig.subplots_adjust(left=0.295, right=0.995, top=0.80, bottom=0.10, wspace=0.10)
    S.title(fig, "Recall needs the J++ part; the lookup mostly doesn't")
    for ax, (target, m, name) in zip(axes, S.MODELS, strict=True):
        S.extra_axis(ax)
        ax.set_title(name, fontsize=10.5, weight="bold")
        for i, (label, lk_k, rc_k, gap_k, kinds) in enumerate(rows):
            y = -i
            lk, rc = S.parse(N.get(lk_k.format(m=m))), S.parse(N.get(rc_k.format(m=m)))
            if label == "Varied scenes":
                lk, rc = x0b_cell(target, X.LOOKUP), x0b_cell(target, X.RECALL)
            kind = kinds.get(m, "fixed")
            if lk is None or rc is None:
                rerun = latest(pins.RESULTS_DIR / "x5_natural" / "qwen35_9b_x5_natural_g75", "verdict-*/verdict.json")
                if label == "Natural passages" and m == "9b" and rerun:
                    lk, rc = rerun["main"]["excess"][X.LOOKUP], rerun["main"]["excess"][X.RECALL]
                    kind = "rerun"
                else:
                    ax.text(0.4, y, "not tested: gate" if label == "Natural passages" else "not run", ha="center",
                            va="center", fontsize=9.5, color=S.COL["muted"])  # fmt: skip
                    continue
            ax.plot([lk[0], rc[0]], [y, y], color="#cccccc", lw=2.2, zorder=1, ls="--" if kind == "rerun" else "-")
            S.dot(ax, 0, y, lk, S.COL["lookup"], kind)
            S.dot(ax, 0, y, rc, S.COL["recall"], kind)
            g = S.parse(N.get(gap_k.format(m=m))) if gap_k else None
            gap = g[0] if g and kind != "rerun" else rc[0] - lk[0]
            if (m, label) not in NO_GAP_LABEL:
                ax.text(
                    (lk[0] + rc[0]) / 2,
                    y + 0.3,
                    f"gap {gap:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    color="#444444",
                )
            for w, v in ((X.LOOKUP, lk), (X.RECALL, rc)):
                S.record("fig1", target, f"{label.replace(chr(10), ' ')}: {'lookup' if w == X.LOOKUP else 'recall'} extra loss",
                         *v, source=lk_k.format(m=m) if w == X.LOOKUP else rc_k.format(m=m))  # fmt: skip
            S.record(
                "fig1",
                target,
                f"{label.replace(chr(10), ' ')}: gap",
                round(gap, 4),
                source=gap_k.format(m=m) if gap_k else "recall minus lookup",
            )
        ax.set_ylim(-len(rows) + 0.4, 0.7)
        ax.grid(axis="x", color="#eeeeee")
    axes[0].set_yticks([-i for i in range(len(rows))], [r[0] for r in rows])
    axes[0].tick_params(axis="y", length=0)
    colour = [plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=7),
              plt.Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=7)]  # fmt: skip
    grey = "#8a8a8a"
    style = [plt.Line2D([], [], marker="o", ls="", mfc=grey, mec=grey, ms=7),
             plt.Line2D([], [], marker="o", ls="", mfc="white", mec=grey, ms=7, mew=1.5),
             plt.Line2D([], [], marker="o", ls="--", mfc="white", mec=grey, color=grey, ms=7, mew=1.5)]  # fmt: skip
    fig.legend(colour, ["lookup", "recall"], loc="upper left", bbox_to_anchor=(0.0, 0.945), ncol=2, frameon=False,
               fontsize=9.5, handletextpad=0.3, columnspacing=1.2)  # fmt: skip
    fig.legend(style, ["fixed in advance", "after the data", "rerun with a lowered gate"], loc="upper left",
               bbox_to_anchor=(0.0, 0.905), ncol=3, frameon=False, fontsize=9.5, handletextpad=0.3,
               columnspacing=1.2)  # fmt: skip
    S.save(fig, "fig1_readers")


def x0b_cell(target: str, reader: str):
    """X0b's pooled cell at the layer fixed in advance (its verdict's cells), as (v, lo, hi)."""
    run = {"qwen3.5-9b": "qwen35_9b_x0b_v2", "qwen3.6-27b": "x0b_v2_27b", "qwen3.5-122b-a10b": "qwen35_122b_x0b_v2",
           "muse-glimmer-30b": "muse30b_x0b_v2"}[target]  # fmt: skip
    v = latest(pins.RESULTS_DIR / "x0b_generalize" / run, "verdict-*/verdict.json")
    assert v is not None, f"no X0b verdict for {run}"
    c = next(c for c in v["cells"] if c["layer"] == X.PREDICTED[target] and c["reader"] == reader and c["dict"] == "jpp"
             and c["k"] == X.K_MAIN and c["omp"] == "signed")  # fmt: skip
    return tuple(c["excess"])


def parts_cells() -> dict[str, dict[str, dict]]:
    """Fig. 2's cells per model: part -> {lookup, recall, share, kind}; from the parts runs' verdicts and the main
    runs' X0 cells (logit lens, input embeddings, random: two people swap picks)."""
    out: dict[str, dict[str, dict]] = {}
    runs = {"9b": ("qwen35_9b_x0_pcaeq", "qwen35_9b_x0_parts", "qwen35_9b_x0_jppother"),
            "27b": ("x0_pcaeq_27b", "x0_parts_27b", "x0_jppother_27b"),
            "122b": ("qwen35_122b_x0_parts", "qwen35_122b_x0_parts", "qwen35_122b_x0_jppother"),
            "muse": ("muse30b_x0_parts", "muse30b_x0_parts", "muse30b_x0_jppother")}  # fmt: skip
    for m, (pcaeq, word, other) in runs.items():
        cells: dict[str, dict] = {}
        for run, parts in ((pcaeq, ("jpp", "jwo", "pca_eq")), (word, ("w",)), (other, ("jpp_other",))):
            v = latest(pins.RESULTS_DIR / "x0_parts" / run, "verdict-*/verdict.json")
            for r in (v or {}).get("rows", []):
                if r["part"] in parts:
                    c = cells.setdefault(r["part"], {"share": r["median_share"], "source": run})
                    c["lookup" if r["reader"] == X.LOOKUP else "recall"] = r["excess"]
        run = XF.Run(MAIN_RUNS[m])
        layer = X.PREDICTED[{k: t for t, k, _ in S.MODELS}[m]]
        allc = run.cells("chat")
        for d in ("wu", "we", "rand"):
            key = ("chat", layer, X.LOOKUP, d, X.K_MAIN, "signed")
            if key in allc:
                cells[d] = {"lookup": allc[key]["excess"], "recall": allc[("chat", layer, X.RECALL, d, X.K_MAIN, "signed")]["excess"],
                            "share": run.share.get(("chat", layer, d, X.K_MAIN, "signed")), "source": MAIN_RUNS[m]}  # fmt: skip
        out[m] = cells
    return out


def fig2(plt) -> None:
    parts = [("jpp", "J++"), ("jwo", "J++ without the\nword's directions"), ("w", "The word alone"),
             ("pca_eq", "Main directions at\nJ++'s share"), ("jpp_other", "J++ fitted to\nanother scene"),
             ("wu", "Logit lens †"), ("we", "Input embeddings †"), ("rand", "Random directions †")]  # fmt: skip
    cells = parts_cells()
    fig, axes = plt.subplots(1, len(S.MODELS), figsize=(S.WIDTH, 5.4), sharey=True)
    fig.subplots_adjust(left=0.205, right=0.995, top=0.80, bottom=0.10, wspace=0.12)
    S.title(fig, "No other part costs the recall as much as the scene's own J++")
    for ax, (target, m, name) in zip(axes, S.MODELS, strict=True):
        S.extra_axis(ax)
        ax.set_title(name, fontsize=10.5, weight="bold")
        for i, (p, label) in enumerate(parts):
            y = -i
            c = cells[m].get(p)
            if c is None or "recall" not in c:
                ax.text(0.4, y, "not run yet", ha="center", va="center", fontsize=9.5, color=S.COL["muted"])
                continue
            S.dot(ax, 0, y, c["recall"], S.COL["recall"], "after")
            ax.plot([c["lookup"][0]], [y], "o", ms=4.5, color=S.COL["lookup"], zorder=4)
            if c["share"] is not None:
                # a white box: a recall interval reaching the right edge (Muse's J++) must not read as a minus sign
                ax.text(1.0, y, f"{100 * c['share']:.0f}%", ha="right", va="center", fontsize=9.5, color=S.COL["muted"],
                        transform=ax.get_yaxis_transform(), zorder=5,
                        bbox=dict(boxstyle="square,pad=0.45", fc="white", ec="none"))  # fmt: skip
            S.record(
                "fig2", target, f"{label.replace(chr(10), ' ')}: recall extra loss", *c["recall"], source=c["source"]
            )
            S.record(
                "fig2", target, f"{label.replace(chr(10), ' ')}: lookup extra loss", *c["lookup"], source=c["source"]
            )
            if c["share"] is not None:
                S.record(
                    "fig2",
                    target,
                    f"{label.replace(chr(10), ' ')}: share of the change",
                    c["share"],
                    source=c["source"],
                )
        ax.set_ylim(-len(parts) + 0.4, 0.7)
        ax.grid(axis="x", color="#eeeeee")
    axes[0].set_yticks([-i for i in range(len(parts))], [p[1] for p in parts])
    axes[0].tick_params(axis="y", length=0)
    marks = [plt.Line2D([], [], marker="o", ls="", mfc="white", mec=S.COL["recall"], mew=1.6, ms=7),
             plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=4.5),
             plt.Line2D([], [], ls="", marker="")]  # fmt: skip
    fig.legend(marks, ["recall (95% CI)", "lookup", "grey % = the part's share of the change"], loc="upper left",
               bbox_to_anchor=(0.0, 0.94), ncol=3, frameon=False, fontsize=9.5, handletextpad=0.3)  # fmt: skip
    S.save(fig, "fig2_parts")


def fig3(plt) -> None:
    """The routes design: the original prompt's locker slots, the swapped prompt (another item moved), and the
    answer each route predicts."""
    fig = plt.figure(figsize=(S.WIDTH, 3.9))
    ax = fig.add_axes((0, 0, 1, 0.88))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 44)
    ax.axis("off")
    S.title(fig, "The routes test: each route predicts a different locker")
    rows = (("Original prompt", 33, [("duck", "4"), ("rabbit", "3"), ("goose", "2")], "Beth picked the goose."),
            ("Swapped prompt", 21, [("rabbit", "7"), ("duck", "4"), ("goose", "2")], "Beth picked the rabbit."))  # fmt: skip
    for label, y, slots, pick in rows:
        ax.text(1, y + 2.5, label, fontsize=10.5, weight="bold", va="center")
        for j, (item, digit) in enumerate(slots):
            x = 22 + 17 * j
            hl = label == "Swapped prompt" and item == "rabbit"
            ax.add_patch(plt.Rectangle((x, y), 15.5, 5.5, fc="#fff4e6" if hl else "#f5f5f5", ec="#bbbbbb", lw=1))
            ax.text(x + 7.75, y + 2.75, f"slot {j + 1}: {item} {digit}", ha="center", va="center", fontsize=10)
        ax.text(74, y + 2.75, pick, fontsize=10.5, va="center")
    routes = (("identity", "3: the rabbit's locker in the original", S.COL["identity"]),
              ("position", "4: what slot 1 holds in the original", S.COL["position"]),
              ("value", "7: the new digit in the swapped prompt", S.COL["value"]),
              ("unchanged", "2: the original answer (the goose)", "#8f8f8f"))  # fmt: skip
    ax.text(1, 14.5, "The change at 'goose' comes from the swapped prompt's 'rabbit'; the lookup is asked on the original:",
            fontsize=10.5, va="center")  # fmt: skip
    for k, (name, what, col) in enumerate(routes):
        x, y = 3 + 48 * (k % 2), 8.2 - 5.6 * (k // 2)
        ax.add_patch(plt.Rectangle((x, y - 1.6), 2.6, 3.2, fc=col, ec="none"))
        ax.text(x + 4, y, f"{name} → {what}", fontsize=10.2, va="center")
    S.save(fig, "fig3_routes_design")


ARMS4 = (("whole", "whole change"), ("no_jpp", "without J++"), ("no_jpp_rand", "without random (J++ size)"),
         ("no_alf", "without the pointer"), ("no_alf_rand", "without random (pointer size)"))  # fmt: skip
ROUTES = (
    ("identity", "identity"),
    ("position", "position"),
    ("value", "value"),
    ("original", "unchanged"),
    ("other", "other"),
)
ROUTE_COL = {"identity": S.COL["identity"], "position": S.COL["position"], "value": S.COL["value"],
             "original": S.COL["original"], "other": S.COL["other"]}  # fmt: skip


KEEP4 = (("keep_alf", "only the pointer part"), ("keep_alf_rand", "only random (pointer size)"),
         ("keep_jpp", "only the J++ part"), ("keep_jpp_rand", "only random (J++ size)"))  # fmt: skip


def fig4(plt) -> None:
    """Another item moved, at the layer fixed in advance: route shares per arm, the removals (x6_routes) above and each
    part added alone (x6_routes_keeponly) below; the 122B's runs after the data (gate 0.75), hatched."""
    runs = (("qwen3.5-9b", "Qwen3.5-9B", "qwen35_9b_x6_routes", "qwen35_9b_x6_routes_keeponly", "fixed"),
            ("qwen3.6-27b", "Qwen3.6-27B", "x6_routes_27b", "x6_routes_keeponly_27b", "fixed"),
            ("qwen3.5-122b-a10b", "Qwen3.5-122B", "qwen35_122b_x6_routes_g75", "qwen35_122b_x6_routes_keeponly_g75",
             "rerun"),
            ("muse-glimmer-30b", "Muse Glimmer 30B", "muse30b_x6_routes", "muse30b_x6_routes", "fixed"))  # fmt: skip
    ys = [-i for i in range(len(ARMS4))] + [-len(ARMS4) - 0.6 - i for i in range(len(KEEP4))]
    labels = [a[1] for a in ARMS4] + [a[1] for a in KEEP4]
    fig, axes = plt.subplots(1, len(runs), figsize=(S.WIDTH, 5.4), sharey=True)
    fig.subplots_adjust(left=0.28, right=0.985, top=0.80, bottom=0.10, wspace=0.14)
    S.title(fig, "The lookup follows identity or position, never the value")
    for ax, (target, name, run, keep_run, kind) in zip(axes, runs, strict=True):
        ax.set_title(name, fontsize=10.5, weight="bold")
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1], ["0", "50", "100"])
        ax.axhline(-len(ARMS4) + 0.2, color="#bbbbbb", lw=0.8)
        for source, arms, y0 in ((run, ARMS4, ys[: len(ARMS4)]), (keep_run, KEEP4, ys[len(ARMS4) :])):
            v = latest(pins.RESULTS_DIR / "x6_routes" / source, "verdict-*/verdict.json")
            if v is None:
                ax.text(
                    0.5,
                    (y0[0] + y0[-1]) / 2,
                    "not run yet",
                    ha="center",
                    va="center",
                    fontsize=10,
                    color=S.COL["muted"],
                )
                continue
            rows = {(r["condition"], r["arm"]): r for r in v["rows"]}
            for y, (arm, _) in zip(y0, arms, strict=True):
                r = rows.get(("C2", arm))
                if r is None:
                    continue
                left = 0.0
                for route, _ in ROUTES:
                    sh = r["share"][route][0]
                    ax.barh(y, sh, left=left, height=0.72, color=ROUTE_COL[route], edgecolor="white", lw=0.8,
                            hatch="//" if kind == "rerun" else None)  # fmt: skip
                    if sh >= 0.15:
                        ax.text(left + sh / 2, y, f"{100 * sh:.0f}", ha="center", va="center", fontsize=9,
                                color="white" if route in ("identity", "value") else "#222222")  # fmt: skip
                    S.record("fig4", target, f"another item moved, {arm}: {route} share", *r["share"][route], n=r["n"],
                             source=source)  # fmt: skip
                    left += sh
        ax.set_ylim(ys[-1] - 0.6, 0.6)
    fig.supxlabel("% of lookup answers", x=0.63, y=0.01, fontsize=10.5)
    axes[0].set_yticks(ys, labels)
    axes[0].tick_params(axis="y", length=0)
    hs = [plt.Rectangle((0, 0), 1, 1, color=ROUTE_COL[r]) for r, _ in ROUTES[:4]]
    fig.legend(hs, [n for _, n in ROUTES[:4]], loc="upper left", bbox_to_anchor=(0.005, 0.935), ncol=4, frameon=False,
               fontsize=10, handlelength=1.2)  # fmt: skip
    S.save(fig, "fig4_routes")


def fig5(plt) -> None:
    """Top: the J++ extra loss by depth (valid X0 cells); bottom: the position share (another item moved, whole change)
    at each layer the routes test ran; one shaded band per model, from the first layer measured to the last where the
    lookup's J++ extra loss is at least NEEDS; the x-axis on the tested depth range."""
    routes = {"9b": (("qwen35_9b_x6_routes_l6", 6, "fixed"), ("qwen35_9b_x6_routes_sweep_l8", 8, "fixed"),
                     ("qwen35_9b_x6_routes_sweep_l10", 10, "fixed"), ("qwen35_9b_x6_routes", 12, "fixed")),
              "27b": (("x6_routes_l16_27b", 16, "fixed"), ("x6_routes_sweep_l20_27b", 20, "fixed"),
                      ("x6_routes_sweep_l24_27b", 24, "fixed"), ("x6_routes_sweep_l28_27b", 28, "fixed"),
                      ("x6_routes_27b", 32, "fixed")),
              "122b": (("qwen35_122b_x6_routes_sweep_l24_g75", 24, "rerun"), ("qwen35_122b_x6_routes_l27_g75", 27, "rerun"),
                       ("qwen35_122b_x6_routes_sweep_l30_g75", 30, "rerun"), ("qwen35_122b_x6_routes_g75", 33, "rerun"),
                       ("qwen35_122b_x6_routes_sweep_l36_g75", 36, "rerun")),
              # Muse: L34 not tested (the sanity swap moved the lookup in no scene; batch 38's G2)
              "muse": (("muse30b_x6_routes_l13", 13, "fixed"), ("muse30b_x6_routes", 26, "fixed"))}  # fmt: skip
    fig, axes = plt.subplots(2, len(S.MODELS), figsize=(S.WIDTH, 5.6), sharex="col",
                             gridspec_kw={"height_ratios": [1.25, 1]})  # fmt: skip
    fig.subplots_adjust(left=0.095, right=0.985, top=0.84, bottom=0.10, wspace=0.14, hspace=0.26)
    # Dan's wording (25 Oct ~23:00), 86 characters
    S.title(fig, "Position answers appear with depth; on the 9B and 122B where the lookup stops needing J++", limit=90)
    for j, (target, m, name) in enumerate(S.MODELS):
        top, bot = axes[0, j], axes[1, j]
        n_layers = pins.TARGETS[target]["n_layers"]
        cells = XF.Run(depth_run(m)).cells("chat")
        layers = sorted({k[1] for k in cells})
        top.axhspan(S.XLIM[0], S.NOT_NEEDED, color=S.COL["band"], lw=0, zorder=0)
        span = []
        for w, col in ((X.LOOKUP, S.COL["lookup"]), (X.RECALL, S.COL["recall"])):
            pts = [(100 * la / n_layers, cells[("chat", la, w, *X.MAIN)], la) for la in layers]
            pts = [(d, c, la) for d, c, la in pts if c["valid"]]
            top.plot([d for d, _, _ in pts], [c["excess"][0] for _, c, _ in pts], "-o", color=col, lw=2, ms=3.5)
            top.fill_between([d for d, _, _ in pts], [c["excess"][1] for _, c, _ in pts], [c["excess"][2] for _, c, _ in pts],
                             color=col, alpha=0.12, lw=0)  # fmt: skip
            for _, c, la in pts:
                S.record("fig5", target, f"layer {la}: {'lookup' if w == X.LOOKUP else 'recall'} J++ extra loss", *c["excess"],
                         n=c["n"], source=depth_run(m))  # fmt: skip
            last_d, last_y = pts[-1][0], pts[-1][1]["excess"][0]
            if w == X.LOOKUP:
                # one band per model: from the first layer measured to the last where the lookup needs J++ (>= NEEDS)
                need = [d for d, c, _ in pts if c["excess"][0] >= NEEDS]
                half = (pts[1][0] - pts[0][0]) / 2
                if need:
                    for ax in (top, bot):
                        ax.axvspan(pts[0][0] - half, max(need) + half, color="#efe9fb", lw=0, zorder=0)
                top.text(
                    last_d - 1, max(last_y - 0.1, -0.17), "lookup", color=col, fontsize=9.5, ha="right", va="center"
                )
            else:
                top.text(
                    last_d - 1, min(last_y + 0.1, 0.95), "recall", color=col, fontsize=9.5, ha="right", va="center"
                )
            span += [pts[0][0], last_d]
        top.set_ylim(*S.XLIM)
        top.set_title(name, fontsize=10.5, weight="bold")
        top.grid(axis="y", color="#eeeeee")
        bot.set_ylim(0, 1)
        if not any(latest(pins.RESULTS_DIR / "x6_routes" / r, "verdict-*/verdict.json") for r, _, _ in routes[m]):
            S.empty(bot, "routes test\nnot run yet")
        for run, layer, kind in routes[m]:
            v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json")
            d = 100 * layer / n_layers
            r = next((r for r in (v or {}).get("rows", []) if r["condition"] == "C2" and r["arm"] == "whole"), None)
            if r is None:
                continue
            pos = r["share"]["position"]
            bot.plot([d, d], [pos[1], pos[2]], color=S.COL["position"], lw=1.6, ls="--" if kind == "rerun" else "-")
            bot.plot(
                [d],
                [pos[0]],
                "o",
                ms=7.5,
                mfc=S.COL["position"] if kind == "fixed" else "white",
                mec=S.COL["position"],
                mew=1.6,
            )
            S.record(
                "fig5",
                target,
                f"layer {layer}: position share (another item moved, whole change)",
                *pos,
                n=r["n"],
                source=run,
            )
        bot.grid(axis="y", color="#eeeeee")
        tested = [*span, *(100 * layer / n_layers for _, layer, _ in routes[m])]
        bot.set_xlim(min(tested) - 4, max(tested) + 4)
        bot.set_xlabel("depth (% of layers)")
        # the routes test's layers as a top axis of the bottom panel (labels beside the points overlapped)
        layer_axis = bot.secondary_xaxis("top")
        layer_axis.set_xticks(
            [100 * layer / n_layers for _, layer, _ in routes[m]], [str(layer) for _, layer, _ in routes[m]]
        )
        layer_axis.tick_params(labelsize=9, colors=S.COL["muted"], length=2)
    axes[0, 0].set_ylabel("J++ extra loss")
    axes[1, 0].set_ylabel("position share")
    for ax in axes[:, 1:].flat:
        ax.tick_params(labelleft=False)
    S.save(fig, "fig5_depth")


def fig6(plt) -> None:
    """Top: the sanity swap's lookup extra loss without J++, without the pointer directions, without both (batch 34's
    bar dotted); bottom: the switches lost without the pointer directions, with J++, with a random part of J++'s share
    (batch 36's bar: the random union + 0.15, dotted). The recall as small grey dots."""
    runs = (("qwen3.5-9b", "9b", "Qwen3.5-9B", "qwen35_9b_x6_routes_bothoff", "qwen35_9b_x6_routes_bothoff_ctrl", "fixed"),
            ("qwen3.6-27b", "27b", "Qwen3.6-27B", "x6_routes_bothoff_27b", "x6_routes_bothoff_ctrl_27b", "fixed"),
            ("qwen3.5-122b-a10b", "122b", "Qwen3.5-122B", "qwen35_122b_x6_routes_bothoff_g75",
             "qwen35_122b_x6_routes_bothoff_ctrl_g75", "rerun"),
            ("muse-glimmer-30b", "muse", "Muse Glimmer 30B", "muse30b_x6_routes", "muse30b_x6_routes", "fixed"))  # fmt: skip
    parts = (("jpp", "without J++"), ("alf", "without the pointer"), ("both", "without both"))
    ctrl = (
        ("alf", "pointer"),
        ("alf + J++", "pointer + J++"),
        ("alf + random (J++ share)", "pointer + random\n(J++'s share)"),
    )
    fig, axes = plt.subplots(2, len(runs), figsize=(S.WIDTH, 5.6), sharey="row")
    fig.subplots_adjust(left=0.19, right=0.995, top=0.80, bottom=0.09, wspace=0.10, hspace=0.66)
    S.title(fig, "Removing J++ and the pointer directions together")
    for j, (target, _, name, run, ctrl_run, kind) in enumerate(runs):
        top, bot = axes[0, j], axes[1, j]
        S.extra_axis(top)
        top.set_title(name, fontsize=10.5, weight="bold")
        v = latest(pins.RESULTS_DIR / "x6_routes" / run, "verdict-*/verdict.json")
        ex = {(x["condition"], x["reader"], x["part"]): x for x in (v or {}).get("extra", [])}
        if not ex:
            S.empty(top, "pending")
        else:
            for i, (p, label) in enumerate(parts):
                lk, rc = ex[("C0", X.LOOKUP, p)]["excess"], ex[("C0", X.RECALL, p)]["excess"]
                top.plot([rc[0]], [-i - 0.22], "o", ms=4.5, color="#9a9a9a", zorder=3)
                S.dot(top, 0, -i, lk, S.COL["lookup"], "rerun" if kind == "rerun" else "fixed")
                S.record("fig6", target, f"the sanity swap, lookup extra loss {label}", *lk, source=run)
                S.record("fig6", target, f"the sanity swap, recall extra loss {label}", *rc, source=run)
            bar = ex[("C0", X.LOOKUP, "alf")]["excess"][0] + 0.15
            top.plot([bar, bar], [-2.35, -1.65], color="#333333", lw=1.6, ls=":")
            S.record("fig6", target, "batch 34's bar (pointer alone + 0.15)", round(bar, 4), source=run)
        top.set_ylim(-len(parts) + 0.4, 0.6)
        bot.set_xlim(0, 1)
        bot.set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        bot.set_xlabel("switches lost")
        bot.grid(axis="x", color="#eeeeee")
        cv = latest(pins.RESULTS_DIR / "x6_routes" / ctrl_run, "verdict-*/verdict.json") if ctrl_run else None
        cc = {(x["condition"], x["reader"], x["arm"]): x for x in (cv or {}).get("ctrl", [])}
        if not cc:
            S.empty(bot, "not run")
        else:
            for i, (arm, label) in enumerate(ctrl):
                lk, rc = cc[("C0", X.LOOKUP, arm)]["lost"], cc[("C0", X.RECALL, arm)]["lost"]
                bot.plot([rc[0]], [-i - 0.22], "o", ms=4.5, color="#9a9a9a", zorder=3)
                S.dot(bot, 0, -i, lk, S.COL["lookup"], kind)
                S.record(
                    "fig6",
                    target,
                    f"the sanity swap, lookup switches lost: {label.replace(chr(10), ' ')}",
                    *lk,
                    source=ctrl_run,
                )
                S.record(
                    "fig6",
                    target,
                    f"the sanity swap, recall switches lost: {label.replace(chr(10), ' ')}",
                    *rc,
                    source=ctrl_run,
                )
            bar = cc[("C0", X.LOOKUP, "alf + random (J++ share)")]["lost"][0] + 0.15
            bot.plot([bar, bar], [-1.35, -0.65], color="#333333", lw=1.6, ls=":")
            S.record("fig6", target, "batch 36's bar (pointer + random + 0.15)", round(bar, 4), source=ctrl_run)
        bot.set_ylim(-len(ctrl) + 0.4, 0.6)
    axes[0, 0].set_yticks([-i for i in range(len(parts))], [p[1] for p in parts])
    axes[1, 0].set_yticks([-i for i in range(len(ctrl))], [c[1] for c in ctrl])
    for ax in axes[:, 0]:
        ax.tick_params(axis="y", length=0)
    marks = [plt.Line2D([], [], marker="o", ls="", color=S.COL["lookup"], ms=7),
             plt.Line2D([], [], marker="o", ls="", color="#9a9a9a", ms=4.5),
             plt.Line2D([], [], ls=":", color="#333333", lw=1.6)]  # fmt: skip
    fig.legend(marks, ["lookup (95% CI)", "recall", "bar fixed in advance"], loc="upper left",
               bbox_to_anchor=(0.0, 0.945), ncol=3, frameon=False, fontsize=9.5, handletextpad=0.3)  # fmt: skip
    S.save(fig, "fig6_both_removed")


def main() -> None:
    plt = S.setup()
    for f in (fig0, fig1, fig2, fig3, fig4, fig5, fig6):
        f(plt)
    S.write_data()
    print(S.OUT)


if __name__ == "__main__":
    main()
