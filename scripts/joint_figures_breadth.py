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
    """Rows: every dataset Zach built, grouped by model (Qwen 9B, Qwen 27B, Nemotron Lightning); recalled minus lookup
    answers that turn wrong (pp) when the lens part is removed everywhere (each dataset's own contrast), a dark dot with
    its 95% interval where data.csv has one, and the logit lens's own directions as a grey tick where that control ran."""
    zb = J.breadth()
    rows = [("toy puzzles, seed 1", "toy.{m}.s1", "toy.{m}.u"), ("toy puzzles, seed 2", "toy.{m}.s2", None),
            ("toy puzzles, seed 3", "toy.{m}.s3", None), ("natural fact chains, seed 1", "nat.{m}.s1", "nat.{m}.u"),
            ("natural fact chains, seed 2", "nat.{m}.s2", None), ("natural fact chains, seed 3", "nat.{m}.s3", None),
            ("natural set", "natplus.{m}", "natplus.{m}.u"), ("earlier main set", "v1.{m}", "v1.{m}.u"),
            ("main set", "ko.{m}.mk", "ko.{m}.u")]  # fmt: skip
    order = [(n, m) for n, m, *_ in sorted(MODELS3, key=lambda t: ("q9", "q27", "nl").index(t[1]))]
    placed, y = [], 0.0
    for name, m in order:
        have = [(label, key, ukey) for label, key, ukey in rows if cell(zb, m, key.format(m=m)) is not None]
        placed.append((name, m, y, have))
        y -= len(have) + 1.2
    fig = plt.figure(figsize=(S.WIDTH, 2.0 + 0.24 * -y))
    ax = fig.add_axes((0.36, 0.95 / fig.get_figheight(), 0.61, 0.24 * -y / fig.get_figheight()))
    S.title(fig, "Recalled answers need the lens part on every dataset we built",
            "Remove everywhere: recalled minus lookup answers that turn wrong (pp); grey: logit-lens control")  # fmt: skip
    ticks, labels = [], []
    tr = J.F.blend(fig, ax)
    for name, m, y0, have in placed:
        ax.text(0.01, y0 - 0.1, name, transform=tr, fontsize=S.FONT + 1, weight="bold", va="center")
        for i, (label, key, ukey) in enumerate(have):
            yy = y0 - 1.1 - i
            k = key.format(m=m)
            v = cell(zb, m, k)
            assert v is not None
            if v[1] not in ("", None):
                ax.plot([J.num(v[1]), J.num(v[2])], [yy, yy], color=J.RECALLED, lw=1.5, zorder=2)
            ax.plot([v[0]], [yy], "o", ms=7, color=J.RECALLED, zorder=3)
            record("j6", name, f"{label}: recalled minus lookup, pp", k, v)
            if ukey:
                u = cell(zb, m, ukey.format(m=m))
                if u is not None:
                    ax.plot([u[0]], [yy], marker="|", ms=11, mew=2.2, color=S.COL["control"], ls="", zorder=2)
                    record("j6", name, f"{label}: logit lens's directions, pp", ukey.format(m=m), u)
            ticks.append(yy)
            labels.append(label)
    ax.set_yticks(ticks, labels)
    ax.set_ylim(y + 0.6, 0.4)
    ax.set_xlim(-10, 75)
    ax.axvline(0, color="#999999", lw=0.8, zorder=0)
    ax.set_xticks([0, 25, 50, 75])
    ax.set_xlabel("recalled minus lookup answers that turn wrong (pp)")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    hs = [plt.Line2D([], [], marker="o", ls="", color=J.RECALLED, ms=7),
          plt.Line2D([], [], marker="|", ls="", color=S.COL["control"], ms=11, mew=2.2)]  # fmt: skip
    J.legend_below(fig, hs, ["the lens part taken out (95% interval where computed)", "the logit lens's own directions"],
                   0.0, 2)  # fmt: skip
    return fig


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
