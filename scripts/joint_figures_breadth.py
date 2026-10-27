"""joint_figures_breadth (Zach, 27 Oct): the root README's figures for Zach's half (Findings 4 and 5), in
scripts/story_style.py's visual language and the joint vocabulary (check_figure_terms.JOINT_RETIRED), drawn with
scripts/joint_figures.py's helpers. Every plotted number comes from docs/breadth/data.csv.

  figures/shared/j6_datasets.png      recalled answers need the lens part on every dataset Zach built
  figures/shared/j7_where.png         where the removal must act: the bridge's mention at middle layers, the question deeper
  figures/shared/data_breadth.csv     every plotted number with its data.csv key

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
MODELS3 = (("Qwen 27B", "q27", "#3a3a3a", "o"), ("Qwen 9B", "q9", "#8a8a8a", "s"), ("Nemotron Lightning", "nl", "#2b7bba", "D"))


def cell(zb: dict, m: str, key: str) -> tuple[float, str, str] | None:
    r = zb.get((m, key))
    return (J.num(r["value"]), r["lo"], r["hi"]) if r else None


def record(fig: str, model: str, quantity: str, key: str, v) -> None:
    ROWS.append({"figure": fig, "model": model, "quantity": quantity, "value": v[0], "lo": v[1], "hi": v[2], "n": "",
                 "source": f"docs/breadth/data.csv | {key}"})  # fmt: skip


def j6_datasets(plt):
    """Rows: every dataset Zach built; per model, points lost more on recalled than on stated answers when the lens
    part is removed everywhere (each dataset's own contrast), with the logit lens's own directions as a grey tick where
    that control ran (on the first data seed of the puzzles and the chains)."""
    zb = J.breadth()
    rows = [("toy puzzles, data seed 1", "toy.{m}.s1", "toy.{m}.u"), ("toy puzzles, data seed 2", "toy.{m}.s2", None),
            ("toy puzzles, data seed 3", "toy.{m}.s3", None), ("natural fact chains, seed 1", "nat.{m}.s1", "nat.{m}.u"),
            ("natural fact chains, seed 2", "nat.{m}.s2", None), ("natural fact chains, seed 3", "nat.{m}.s3", None),
            ("natural set, popular and rare", "natplus.{m}", "natplus.{m}.u"), ("earlier main set", "v1.{m}", "v1.{m}.u"),
            ("main set", "ko.{m}.mk", "ko.{m}.u")]  # fmt: skip
    fig = plt.figure(figsize=(S.WIDTH, 5.6))
    ax = fig.add_axes((0.31, 0.2, 0.66, 0.6))
    S.title(fig, "Recalled answers need the lens part on every dataset we built",
            "Remove everywhere: pp lost more on recalled than on lookup answers.\n"
            "Grey tick: the logit lens's own directions removed instead (where it was run).")  # fmt: skip
    off = {"q27": -0.2, "q9": 0.0, "nl": 0.2}
    for i, (label, key, ukey) in enumerate(rows):
        y = -i
        for name, m, col, mk in MODELS3:
            k = key.format(m=m)
            v = cell(zb, m, k)
            if v is None:
                continue
            yy = y + off[m]
            if v[1] not in ("", None):
                ax.plot([J.num(v[1]), J.num(v[2])], [yy, yy], color=col, lw=1.4, zorder=2)
            ax.plot([v[0]], [yy], mk, ms=7, color=col, mec="white", mew=0.8, zorder=3)
            record("j6", name, f"{label}: recalled minus stated, points", k, v)
            if ukey:
                u = cell(zb, m, ukey.format(m=m))
                if u is not None:
                    ax.plot([u[0]], [yy], marker="|", ms=11, mew=2.2, color=S.COL["control"], ls="", zorder=2)
                    record("j6", name, f"{label}: logit lens's directions, points", ukey.format(m=m), u)
    ax.set_yticks([-i for i in range(len(rows))], [r[0] for r in rows])
    ax.set_ylim(-len(rows) + 0.5, 0.5)
    ax.set_xlim(-10, 75)
    ax.axvline(0, color="#999999", lw=0.8, zorder=0)
    ax.set_xticks([0, 25, 50, 75])
    ax.set_xlabel("pp more on recalled than on lookup answers")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    for b in (2.5, 5.5):
        ax.axhline(-b, color="#e4e4e4", lw=0.8, zorder=0)
    hs = [plt.Line2D([], [], marker=mk, ls="", color=col, ms=7) for _n, _m, col, mk in MODELS3]
    hs.append(plt.Line2D([], [], marker="|", ls="", color=S.COL["control"], ms=11, mew=2.2))
    J.legend_below(fig, hs, [n for n, *_ in MODELS3] + ["logit lens's directions"], 0.0, 4)
    return fig


def j7_where(plt):
    """Per model, two bands (middle layers, deeper layers): the removal at every token, only in the question, only at
    the bridge's mention; points lost more on recalled than on stated answers, all bridges, with 95% intervals."""
    zb = J.breadth()
    fig = plt.figure(figsize=(S.WIDTH, 6.8))
    S.title(fig, "Middle layers need the bridge's mention; deeper layers, the question",
            "Remove everywhere, but only at some tokens: pp lost more on recalled than on\n"
            "lookup answers, all bridges. Each model at a middle band and a deeper band of layers.")  # fmt: skip
    modes = (("every token", S.COL["control"]), ("only in the question", S.COL["position"]),
             ("only at the bridge's mention", S.COL["identity"]))  # fmt: skip
    bands = {"q27": ("L32-40", "L52-60"), "q9": ("L12-16", "L26-29"), "nl": ("L27-33", "L33-39")}
    tops = (0.62, 0.395, 0.17)
    for (name, m, _col, _mk), top in zip(MODELS3, tops, strict=True):
        keys = ((f"pos.{m}.all.all", f"pos.{m}.all.question", f"pos.{m}.all.bridge"),
                (f"late.{m}.all", f"late.{m}.question", f"late.{m}.bridge"))  # fmt: skip
        for c, (depth, ks) in enumerate(zip(("middle", "deeper"), keys, strict=True)):
            ax = fig.add_axes((0.08 + 0.47 * c, top, 0.4, 0.155))
            for i, ((mode, col), k) in enumerate(zip(modes, ks, strict=True)):
                v = cell(zb, m, k)
                J.bar(ax, -i, v[0], v[1], v[2], col, "fixed", h=0.62)
                ax.text(max(v[0], J.num(v[2])) + 2, -i, f"{v[0]:.0f}", va="center", fontsize=S.FONT, color="#333333")
                record("j7", name, f"{depth} band ({bands[m][c]}), {mode}: recalled minus stated, points", k, v)
            ax.set_xlim(-3, 75)
            ax.set_ylim(-2.6, 0.6)
            ax.axvline(0, color="#999999", lw=0.8)
            ax.set_yticks([])
            ax.spines["left"].set_visible(False)
            ax.set_xticks([0, 25, 50, 75])
            if top != tops[-1]:
                ax.set_xticklabels([])
            else:
                ax.set_xlabel("recalled minus lookup lost (pp)")
            head = f"{name}, {depth} {bands[m][c]}" if c == 0 else f"{depth} {bands[m][c]}"
            ax.set_title(head, fontsize=S.FONT + 1, loc="left", color="#222222" if c == 0 else S.COL["muted"], weight="bold" if c == 0 else "normal")
    hs = [plt.Rectangle((0, 0), 1, 1, color=col) for _m, col in modes]
    J.legend_below(fig, hs, [mode for mode, _c in modes], 0.0, 3)
    return fig


FIGURES = (("j6_datasets", j6_datasets), ("j7_where", j7_where))


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
