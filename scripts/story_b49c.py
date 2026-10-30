"""README figure for batch 49 (part c): 49.3's pooled probe, drawn from its verdict folder only (x49_probe.py's
`verdict` writes x49_3-<UTC>/x49_3.json), in story_b47a's look; every plotted number recorded for
data/figures/depth/data.csv with the verdict file as the source.

  49.3  x49_probe.py   x49_3-<UTC>/x49_3.json   the locker-after link: a person mark pooled over the locker sentence?

The title is the claim, built from the verdict's labels so it reads true for any outcome (pass `title` once Dan has
worded it); the rule's bars are thin labelled lines; every cell is fixed in advance (filled marks). A verdict json
holding "planted": true (the tests' fake verdicts) gets "PLANTED" at the head of its subtitle.

    from scripts import story_b49c as C
    C.build_pooled(Path("results/x49_probe/x49_3-<UTC>"), "fig27_pooled")
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import readme_story_figures as F
from scripts import story_b47a as A
from scripts import story_style as S
from scripts import x49_probe as P

TWO = (("qwen3.5-9b", "9b"), ("muse-glimmer-30b", "muse"))  # 49.3 runs on the 9B and Muse
POOLED_COL, TOKEN_COL = "#222222", S.COL["lookup"]
READING = {"distributed": "distributed person mark", "flag": "a picked-flag", "neither": "neither at the sentence",
           "between": "in between", "uninterpretable": "control above chance", "pending": "pending"}  # fmt: skip


def pooled_title(models: list[dict]) -> str:
    labels = [m["label"] for m in models if m["status"] == "tested"]
    if not labels:
        return "A pooled probe at the locker sentence: no model tested yet"
    if all(lab == "distributed" for lab in labels):
        return "Who picked the item is spread over the locker sentence"
    if all(lab == "flag" for lab in labels):
        return "The locker sentence carries a picked-flag, not a person"
    if all(lab == "neither" for lab in labels):
        return "No person mark at the locker sentence: the link is made elsewhere"
    return "A pooled probe at the locker sentence: the models differ"


def cell(m: dict, layer: str, probe: str, view: str, stratum: str) -> list | None:
    c = m["results"][layer]["probes"][probe].get(view, {}).get(stratum)
    return c["accuracy"] if c else None


def best_token(m: dict, layer: str, probe: str) -> tuple[str, list] | None:
    """The rule key whose locker-after cell is highest (the per-token clause's binding cell), with its interval."""
    cells = [(k, cell(m, layer, probe, k, "after")) for k in m["rule_keys"]]
    cells = [(k, v) for k, v in cells if v and v[0] == v[0]]
    return max(cells, key=lambda kv: kv[1][0]) if cells else None


def build_pooled(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """49.3 (x49_probe verdict, x49_3.json): one row per model and layer (L, L // 2). (a) the picker probe (i): on the
    sentence mean (black), at its best single token (purple; the rule needs every token <= 60), and the pooled probe
    in locker-first scenes (grey; must be at chance), chance 33 dotted; (b) the picked-flag probe (ii), the same three
    marks, chance 50 dotted; (c) the rule's reading at that layer."""
    src = verdict_dir / "x49_3.json"
    blob = json.loads(src.read_text())
    by, fid, source = A.by_target(blob["models"]), A.fig_id(out_name), F.rel(src)
    rows: list[tuple[str, str, str | None]] = []  # (target, short, layer)
    for target, short in TWO:
        m = by.get(target, {"status": "pending"})
        layers = [str(la) for la in sorted(m.get("layers", []), reverse=True)] if m["status"] == "tested" else [None]
        rows += [(target, short, la) for la in layers]
    grey = S.COL["control"]
    legend = ([Line2D([], [], marker="o", ls="", color=POOLED_COL, ms=8),
               Line2D([], [], marker="o", ls="", color=TOKEN_COL, ms=8),
               Line2D([], [], marker="o", ls="", color=grey, ms=8)],
              ["sentence mean", "best single token", "sentence mean, locker before the pick"])  # fmt: skip
    note = "PLANTED data, not a result. " if blob.get("planted") else ""
    fig, (a, b, c) = A.frame(
        title or pooled_title(blob["models"]),
        note + "Clean scenes, the locker sentence after the pick: probes read from that sentence's states (every token, "
        "and their mean) at L and L/2. Right (%), the item held out, 95% intervals, all fixed in advance; dotted: "
        "chance. Rule: a spread person mark if the mean ≥ 85 with every token ≤ 60; a picked-flag if (b) ≥ 85 while "
        "(a) ≤ 50.",
        (1, 1, 0.62), A.ROW_IN * len(rows), legend=legend)  # fmt: skip
    A.row_panels((a, b, c), len(rows))
    for ax, name, chance in ((a, "(a) who picked it", 100 / 3), (b, "(b) picked by the asked person", 50.0)):
        A.pct_axis(ax, "probe right (%)", lim=(-4, 106))
        A.panel_title(ax, name)
        ax.axvline(chance, color="#999999", ls=":", lw=1.0, zorder=0)
    A.bar(a, 85, "≥ 85")
    A.bar(a, 60, "≤ 60", side="left")
    A.bar(b, 85, "≥ 85", side="left")
    A.text_column(c, "reading")
    labels = []
    for i, (target, short, la) in enumerate(rows):
        y = -i
        m = by.get(target, {"status": "pending", "label": "pending"})
        if la is None:
            labels.append(F.name_of(short))
            c.text(0.04, y, READING["pending"], va="center")
            for ax in (a, b):
                A.status_text(ax, y, READING["pending"])
            S.record(fid, target, "49.3: the rule's reading", "pending", source=source)
            continue
        n = m["results"][la]["probes"]["picker"][P.POOLED]["after"]["n"]
        labels.append(f"{F.name_of(short)}, L{la}\nn = {n}")
        lab = m["rules"][la]["label"]
        c.text(0.04, y, READING.get(lab, lab), va="center")
        S.record(fid, target, f"49.3: the rule's reading at L{la}", lab, source=source)
        for ax, probe, what in ((a, "picker", "(i) the picker"), (b, "asked", "(ii) picked by the asked person")):
            marks = [("sentence mean, locker after the pick", cell(m, la, probe, P.POOLED, "after"), POOLED_COL, 0.2)]
            best = best_token(m, la, probe)
            if best:
                marks.append((f"best single token ({best[0]}), locker after the pick", best[1], TOKEN_COL, 0.0))
            marks.append(("sentence mean, locker before the pick (control)", cell(m, la, probe, P.POOLED, "before"),
                          grey, -0.2))  # fmt: skip
            for quantity, v, col, dy in marks:
                pt = A.iv(v, 100)
                if v is None or pt is None:
                    continue
                S.dot(ax, 0, y + dy, pt, col, size=7)
                S.record(fid, target, f"49.3, L{la}: {what}, {quantity} (right)", *v, n=n, source=source)
    a.set_yticks([-i for i in range(len(rows))], labels)
    S.save(fig, out_name)
    return out_name
