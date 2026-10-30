"""joint_figures_breadth (Zach, 27 Oct): the root README's figures for Zach's half (Findings 4 and 5), in
scripts/story_style.py's visual language and the joint vocabulary (check_figure_terms.JOINT_RETIRED), drawn with
scripts/joint_figures.py's helpers. Every plotted number comes from docs/breadth/data.csv.

  figures/shared/j6_datasets.png      recalled answers need the lens part on every dataset Zach built
  figures/shared/j7_where.png         where the removal must act: the bridge's mention at middle layers, the question deeper
  data/figures/shared/data_breadth.csv     every plotted number with its data.csv key

uv run python scripts/joint_figures_breadth.py     (CPU only; reads docs/breadth/data.csv)
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts import joint_figures as J  # noqa: E402
from scripts import story_style as S  # noqa: E402

DATA = J.OUT / "data_breadth.csv"
ROWS: list[dict] = []
# (name on the figures, data.csv model, colour, marker): Zach's three models with an effect on every test
# the models' colours on j6 (Dan ~20:00: two clearly different colours for the Qwens, no greys)
MODELS3 = (("Qwen 27B", "q27", "#e08a1e", "o"), ("Qwen 9B", "q9", "#2b7bba", "o"), ("Nemotron Lightning", "nl", "#009e73", "o"))


def cell(zb: dict, m: str, key: str) -> tuple[float, str, str] | None:
    r = zb.get((m, key))
    return (J.num(r["value"]), r["lo"], r["hi"]) if r else None


def record(fig: str, model: str, quantity: str, key: str, v) -> None:
    ROWS.append({"figure": fig, "model": model, "quantity": quantity, "value": v[0], "lo": v[1], "hi": v[2], "n": "",
                 "source": f"docs/breadth/data.csv | {key}"})  # fmt: skip


J6_ROWS = (("toy puzzles (3 seeds)", ("toy.{m}.s1", "toy.{m}.s2", "toy.{m}.s3")),
           ("natural fact chains (3 seeds)", ("nat.{m}.s1", "nat.{m}.s2", "nat.{m}.s3")),
           ("natural passages, popular\nand rare bridges", ("natplus.{m}",)),
           ("earlier main set", ("v1.{m}",)), ("main set", ("ko.{m}.mk",)))  # fmt: skip
# the logit lens's own directions removed instead, wherever that control ran (one band on the figure)
J6_CONTROLS = ("toy.{m}.u", "nat.{m}.u", "natplus.{m}.u", "v1.{m}.u", "ko.{m}.u")


def _j6(plt, fig_id: str, codes: tuple[str, ...]):
    """Five rows (Dan ~20:00): each dataset Zach built, seeds averaged (dot = mean over the data seeds, thin line = their
    range; a 95% whisker where data.csv has one); per model a colour and a small offset, the value at the dot; one light
    band near zero for the logit lens's own directions removed instead, over every model drawn."""
    zb = J.breadth()
    models = [t for t in sorted(MODELS3, key=lambda t: ("q9", "q27", "nl").index(t[1])) if t[1] in codes]
    off = {m: (len(models) - 1) / 2 * 0.34 - i * 0.34 for i, (_n, m, *_) in enumerate(models)}
    fig = plt.figure(figsize=(S.WIDTH, 5.6))
    ax = fig.add_axes((0.30, 0.19, 0.66, 0.63))
    S.title(fig, "Recalled answers need the lens part on every dataset we built",
            "Lens part taken out everywhere. Seeds averaged: dot = mean, thin line = seed range; thick = 95% interval.")  # fmt: skip
    ctrl = []
    for m in codes:
        for key in J6_CONTROLS:
            u = cell(zb, m, key.format(m=m))
            if u is not None:
                ctrl.append((u[0], key.format(m=m), m))
    lo_c, hi_c = min(c[0] for c in ctrl), max(c[0] for c in ctrl)
    ax.axvspan(lo_c, hi_c, color="#ececec", lw=0, zorder=0)
    ax.text(lo_c + 0.5, 0.98, f"control: the logit lens's own directions removed instead ({lo_c:+.0f} to {hi_c:+.0f})", fontsize=S.FONT,
            color=S.COL["muted"], va="center")  # fmt: skip
    for v, key, m in ((lo_c, *next((k, mm) for x, k, mm in ctrl if x == lo_c)), (hi_c, *next((k, mm) for x, k, mm in ctrl if x == hi_c))):
        ROWS.append({"figure": fig_id, "model": {c: n for n, c, *_ in MODELS3}[m], "quantity": "logit-lens control band edge (pp)", "value": v, "lo": "",
                     "hi": "", "n": "", "source": f"docs/breadth/data.csv | {key}"})  # fmt: skip
    for i, (label, keys) in enumerate(J6_ROWS):
        for name, m, col, _mk in models:
            got = [(k.format(m=m), cell(zb, m, k.format(m=m))) for k in keys]
            got = [(k, v) for k, v in got if v is not None]
            if not got:
                continue
            y = -i + off[m]
            vals = [v[0] for _k, v in got]
            mean = sum(vals) / len(vals)
            if len(got) > 1:  # the range over seeds
                ax.plot([min(vals), max(vals)], [y, y], color=col, lw=1.2, zorder=2)
                right = max(vals)
                ROWS.append({"figure": fig_id, "model": name, "quantity": f"{label.replace(chr(10), ' ')}: mean over seeds (pp)",
                             "value": round(mean, 1), "lo": round(min(vals), 1), "hi": round(max(vals), 1), "n": len(vals),
                             "source": "docs/breadth/data.csv | " + "; ".join(k for k, _v in got) + " (mean; lo / hi = range)"})  # fmt: skip
            else:
                k, v = got[0]
                right = J.num(v[2]) if v[1] not in ("", None) else mean
                if v[1] not in ("", None):  # its 95% interval
                    ax.plot([J.num(v[1]), J.num(v[2])], [y, y], color=col, lw=2.0, zorder=2)
                record(fig_id, name, f"{label.replace(chr(10), ' ')}: recalled minus lookup, pp", k, v)
            ax.plot([mean], [y], "o", ms=7, color=col, zorder=3)
            ax.text(right + 1.0, y, f"{mean:.0f}", va="center", fontsize=S.FONT, color=col)
    ax.set_yticks([-i for i in range(len(J6_ROWS))], [label for label, _k in J6_ROWS])
    ax.set_ylim(-len(J6_ROWS) + 0.4, 1.2)
    ax.set_xlim(-6, 62)
    ax.set_xticks([0, 20, 40, 60])
    ax.axvline(0, color="#999999", lw=0.8, zorder=1)
    ax.set_xlabel("percentage points more lost on recalled than on lookup answers")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    hs = [plt.Line2D([], [], marker="o", ls="", color=col, ms=7) for _n, _m, col, _mk in models]
    J.legend_below(fig, hs, [n for n, *_ in models], 0.0, len(models))
    return fig


def j6_datasets(plt):
    """The README's version: Qwen 9B, Qwen 27B and Nemotron Lightning (Zach's finding)."""
    return _j6(plt, "j6", ("q9", "q27", "nl"))


def j6_datasets_qwen(plt):
    """The call doc's copy: the two Qwens only."""
    return _j6(plt, "j6_qwen", ("q9", "q27"))


def j7_where(plt):
    """Two panels (a middle band of layers, a deeper band); rows per model (Qwen 9B, Qwen 27B, Nemotron Lightning): the
    removal at every token, only in the question, only at the bridge's mention; recalled minus lookup answers that turn
    wrong (pp), all bridges, with 95% intervals."""
    zb = J.breadth()
    fig = plt.figure(figsize=(S.WIDTH, 5.6))
    S.title(fig, "On the Qwens, middle layers need the mention; deeper, the question",
            "Remove everywhere at some tokens only: recalled minus lookup answers that turn wrong (pp), all bridges")  # fmt: skip
    modes = (("every token", J.RECALLED), ("only in the question", S.COL["position"]),
             ("only at the bridge's mention", S.COL["identity"]))  # fmt: skip
    bands = {"q27": ("32-40", "52-60"), "q9": ("12-16", "26-29"), "nl": ("27-33", "33-39")}
    order = [(n, m) for n, m, *_ in sorted(MODELS3, key=lambda t: ("q9", "q27", "nl").index(t[1]))]
    axes = (fig.add_axes((0.20, 0.17, 0.36, 0.66)), fig.add_axes((0.62, 0.17, 0.36, 0.66)))
    for c, (depth, ax) in enumerate(zip(("middle", "deeper"), axes, strict=True)):
        for g, (name, m) in enumerate(order):
            keys = (f"pos.{m}.all.all", f"pos.{m}.all.question", f"pos.{m}.all.bridge") if c == 0 else \
                (f"late.{m}.all", f"late.{m}.question", f"late.{m}.bridge")  # fmt: skip
            y0 = -g * 4.2
            for i, ((mode, col), k) in enumerate(zip(modes, keys, strict=True)):
                v = cell(zb, m, k)
                assert v is not None
                J.bar(ax, y0 - i, v[0], v[1], v[2], col, "fixed", h=0.75)
                ax.text(max(v[0], J.num(v[2])) + 2, y0 - i, f"{v[0]:.0f}", va="center", fontsize=S.FONT, color="#333333")
                record("j7", name, f"{depth} band (L{bands[m][c]}), {mode}: recalled minus lookup, pp", k, v)
            ax.text(74, y0 + 0.75, f"layers {bands[m][c]}", ha="right", va="center", fontsize=S.FONT, color=S.COL["muted"])
        ax.set_xlim(-3, 75)
        ax.set_ylim(-11.0, 1.4)
        ax.axvline(0, color="#999999", lw=0.8)
        ax.set_xticks([0, 25, 50, 75])
        ax.set_yticks([-g * 4.2 - 1 for g in range(len(order))], [n for n, _ in order] if c == 0 else [])
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
        ax.set_title(f"{depth} layers", fontsize=S.FONT + 1, loc="left")
        ax.set_xlabel("recalled minus lookup lost (pp)")
    hs = [plt.Rectangle((0, 0), 1, 1, color=col) for _m, col in modes]
    J.legend_below(fig, hs, [mode for mode, _c in modes], 0.0, 3)
    return fig


FIGURES = (("j6_datasets", j6_datasets), ("j6_datasets_qwen", j6_datasets_qwen), ("j7_where", j7_where))


def main() -> None:
    ROWS.clear()
    plt = S.setup()
    for name, draw in FIGURES:
        fig = draw(plt)
        J.save(fig, name)
        plt.close(fig)
    DATA.write_text(J.data_text(ROWS))
    print(f"{len(FIGURES)} figures in {J.OUT.relative_to(REPO)}; {len(ROWS)} rows in {DATA.relative_to(REPO)}")


if __name__ == "__main__":
    main()
