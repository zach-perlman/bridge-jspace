"""README figure for batch 49 (part b): the removal ladder (49.2), drawn from its verdict folder (the json
x49_ladder's `verdict` stage writes) in story_style's look, every plotted number recorded for data/figures/depth/data.csv.

  49.2  x49_ladder.py  x49_2-<UTC>/x49_2.json   the removal ladder: kept share by rung

One row per model (9B, 27B, Muse), one panel per sentence order (locker before / after the pick); in each panel the
changed prompt's answers kept (%) by rung, the recall and the lookup, each rung's random part (same size) beside it in
grey. The subtitle states the two definitions of rungs 5 and 6. The title is the claim, built from the verdict's rules
so it reads true for any outcome (pass `title` once Dan has worded it). Tested on a planted verdict
(tests/test_x49_ladder.py).
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import readme_story_figures as F
from scripts import story_b47a as A
from scripts import story_style as S

TARGETS = A.TARGETS  # 9B, 27B, Muse
ORDERS = (("locker-first", "locker before the pick"), ("locker-after", "locker after the pick"))
RUNGS = (1, 2, 3, 4, 5, 6)
TICKS = ["unedited", "1", "2", "3", "4", "5", "6"]  # x = 0 is the changed prompt as it is; x = r is rung r
READERS = (("recall", "o", -0.15), ("lookup", "s", 0.15))  # reader, marker, x offset of its removal
RAND_DX = 0.11  # the random beside its removal
RUNG_WORDS = ("1 the bridge word at L; 2 at L..L+3; 3 + the item's mention; 4 + the question; 5 every token, "
              "L..L+3; 6 every token, his band")  # fmt: skip
SUB = ("Clean one-pick scenes, on the changed prompt: removed at more and more tokens and layers, beside a random "
       "part (same size, grey) at each token. Answers unchanged (%), 95% intervals, fixed in advance. Rungs: "
       + RUNG_WORDS + ". Two definitions, not one: rung 5 takes out the 25 directions of the bridge's J++ part at "
       "every token; rung 6 each token's own top-10 J++ lens directions (Zach's).")  # fmt: skip
ROW_IN = 1.55  # inches per model row


def ladder_title(v: dict) -> str:
    """The claim from the rules over the models that ran every rung (9B, Muse)."""
    full = [m for m in v["models"] if m["status"] == "tested" and m.get("rules")]
    if not full:
        return "The removal ladder: no model has run every rung yet"
    n = len(full)
    only = sum(m["rules"]["only_everything"] for m in full)
    second = sum(m["rules"]["second_copy"] for m in full)
    never = sum(m["rules"]["lookup"] for m in full)
    if only == n:
        head = "The recall needs the J++ part only when every token loses it"
    elif second == n:
        head = "The recall's second copy of the J++ part is the item's earlier mention"
    else:
        head = f"The removal ladder: the recall needs the J++ part only at every token on {only} of {n}"
    tail = "; the lookup never" if never == n else ""
    return head + tail if len(head + tail) <= 86 else head


def build_ladder(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """49.2 (x49_ladder verdict, x49_2.json): rows = models, columns = the two sentence orders; per rung the recall's
    and the lookup's answers kept with the removal (the reader's colour) and with the random part beside it (grey)."""
    src = verdict_dir / "x49_2.json"
    v = json.loads(src.read_text())
    by, fid, source = A.by_target(v["models"]), A.fig_id(out_name), F.rel(src)
    grey = S.COL["control"]
    keep = (A.NOTE + SUB).replace("J++ ", "J++\u00a0")  # "J++ part" / "J++ lens" on one line (story_b47a.frame)
    lines = [x.replace("\u00a0", " ") for x in textwrap.wrap(keep, A.WRAP, break_on_hyphens=False)]
    legend_in = 0.42 + 0.20 * len(lines) + 0.14  # under the subtitle (story_b47a.frame's layout)
    top_in = legend_in + 0.34 + 0.40
    bottom_in = 0.75
    h = top_in + ROW_IN * len(TARGETS) + bottom_in
    plt = S.setup()
    fig, axes = plt.subplots(len(TARGETS), len(ORDERS), figsize=(S.WIDTH, h), sharex=True, sharey=True, squeeze=False)
    fig.subplots_adjust(left=0.13, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.08, hspace=0.42)
    S.title(fig, title or ladder_title(v), "\n".join(lines), limit=86)
    handles = [Line2D([], [], marker="o", ls="", color=S.COL["recall"], ms=7),
               Line2D([], [], marker="s", ls="", color=S.COL["lookup"], ms=7),
               Line2D([], [], marker="o", ls="", color=grey, ms=7)]  # fmt: skip
    F.legend(fig, handles, ["recall", "lookup", "random part (same size)"], 1 - legend_in / h)
    for i, (target, _) in enumerate(TARGETS):
        mod = by.get(target, {"status": "pending"})
        for j, (group, words) in enumerate(ORDERS):
            ax = axes[i][j]
            ax.set_ylim(-5, 108)
            ax.set_xlim(-0.6, len(RUNGS) + 0.6)
            ax.set_yticks([0, 50, 100], ["0", "50", "100"])
            ax.set_xticks(range(len(TICKS)), TICKS)
            ax.axvline(5.5, color=A.BAR, lw=1.0, ls=(0, (4, 3)))
            ax.grid(axis="y", color="#eeeeee")
            ax.set_axisbelow(True)
            n = mod["cells"]["recall"][group]["n"] if mod["status"] == "tested" else 0
            A.panel_title(ax, words + (f", n = {n}" if n else ""))
            if j == 0:
                ax.set_ylabel(f"{F.name_of(A.TARGETS[i][1])}\nunchanged (%)")
            if mod["status"] != "tested" or not n:
                A.status_text(ax, 50, "pending" if mod["status"] == "pending" else "no scenes")
                continue
            for reader, marker, dx in READERS:
                c = mod["cells"][reader][group]
                col = S.COL[reader]
                xs, ys = [], []
                for x, arm in [(0, "none"), *((r, f"zero{r}") for r in RUNGS)]:
                    if arm not in c["kept"]:
                        continue
                    k = c["kept"][arm]
                    xx = x + (dx if x else 0.0)
                    ax.plot([xx, xx], [100 * k[1], 100 * k[2]], color=col, lw=1.4, zorder=2)
                    ax.plot([xx], [100 * k[0]], marker, ms=6, color=col, zorder=3)
                    xs.append(xx)
                    ys.append(100 * k[0])
                    what = "S unedited" if arm == "none" else f"rung {x} removed"
                    S.record(
                        fid, target, f"49.2: {reader}'s answers kept, {group}, {what}", *k, n=c["n"], source=source
                    )
                    if arm != "none":
                        rk = c["kept"][f"rand{x}"]
                        rx = xx + (RAND_DX if dx > 0 else -RAND_DX)
                        ax.plot([rx, rx], [100 * rk[1], 100 * rk[2]], color=grey, lw=1.2, zorder=2)
                        ax.plot([rx], [100 * rk[0]], marker, ms=5, color=grey, zorder=2.5)
                        S.record(fid, target, f"49.2: {reader}'s answers kept, {group}, rung {x} random beside", *rk,
                                 n=c["n"], source=source)  # fmt: skip
                        S.record(fid, target, f"49.2: {reader}'s cost beyond random, {group}, rung {x}",
                                 *c["cost"][str(x)], n=c["n"], source=source)  # fmt: skip
                ax.plot(xs, ys, color=col, lw=0.9, alpha=0.6, zorder=1.5)
        if mod["status"] == "tested":
            rules = mod.get("rules")
            for key in ("second_copy", "only_everything", "lookup"):
                S.record(fid, target, f"49.2: rule '{key}' holds", "n/a (bridge-word rungs only)" if rules is None
                         else int(bool(rules[key])), source=source)  # fmt: skip
    for ax in axes[-1]:
        ax.set_xlabel("rung (more tokens and layers to the right)")
    S.save(fig, out_name)
    return out_name
