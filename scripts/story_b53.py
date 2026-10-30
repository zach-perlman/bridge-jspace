"""Batch 53's README figures for Part I (Dan's restructure brief, 29 Oct 12:50, docs_1250: "New Part I card from today
(backs bullet 2): lens identity vs address (53.6) ... Part I: the order cell (53.1, 27B vs 122B)").

  fig19_identity_address  53.6: the recall under the lens part toward item B plus the address swap toward item C's
                          locker, and under each part by itself: the shares answering B's, C's, the original or another
                          answer, one group per model (9B, 27B, Muse, Lightning, 122B). Lightning hatched: its gate was
                          chosen after its 60-scene pre-check was seen; a model without a run keeps its slot, grey.
  fig20_order_cell        53.1's number cells: the conflict test's switches lost without the lens part beyond random,
                          lookup and recall, with the question after the scene (the main test) and before it; right,
                          the lookup's paired difference, before minus after (Dan 11:25). A question-first cell that
                          missed its gate keeps its row with a grey "not tested: gate". The paired difference's rule was
                          set after the 27B's two cells were seen (its mark open), before the 122B ran.

record_card_numbers adds the numbers the two cards quote that the figures do not draw (figure "cards"). Every plotted
number is recorded for data/figures/depth/data.csv with its source file.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from scripts import story_style as S
from scripts.story_b50 import B122_NOTE, caption

FIVE = (
    ("qwen3.5-9b", "9B"),
    ("qwen3.6-27b", "27B"),
    ("muse-glimmer-30b", "Muse"),
    ("nemotron-3.5-lightning", "Lightning"),
    ("qwen3.5-122b-a10b", "122B"),
)
LT = "nemotron-3.5-lightning"
LT_HATCH = "Lightning hatched / open: its gate chosen after the 60-scene pre-check was seen."
B_COL, C_COL = S.MARK_COL["jpp"], S.MARK_COL["address"]


def rel(path: Path) -> str:
    return str(path.relative_to(S.REPO))


def by_target(verdicts: tuple[Path, ...]) -> dict[str, tuple[dict, Path]]:
    """target -> (its model entry, the verdict file), a later verdict overriding an earlier one."""
    out = {}
    for p in verdicts:
        for m in json.loads(p.read_text())["models"]:
            out[m["target"]] = (m, p)
    return out


# fig19: the recall's answers per arm (x53_identity_address's PM cells), drawn top to bottom in each model's group
ARMS = (("both", "both parts"), ("lens", "the lens part by itself"), ("addr", "the address by itself"))
ANSWERS = (
    ("B", "B's answer", {"color": B_COL}),
    ("C", "C's answer", {"color": C_COL}),
    ("original", "the original answer", S.ORIGINAL),
    ("other", "another answer", {"color": S.COL["other"]}),
)
ID_TITLE = "Pulled two ways, the recall moves under both levers or barely at all"
ID_SUB = "The recall's answers with the lens part toward item B and the address toward item C's locker, at L"


def build_identity_address(verdicts: tuple[Path, ...], out_name: str = "fig19_identity_address",
                           absent: dict[str, str] | None = None) -> str:  # fmt: skip
    """fig19 from x53_identity_address verdicts; a model in none of them keeps its slot with absent's grey label."""
    data = by_target(verdicts)
    absent = absent or {}
    plt = S.setup()
    top_in, bar_in, gap_in, bottom_in = 0.9, 0.3, 0.42, 2.0
    h = top_in + len(FIVE) * (len(ARMS) * bar_in + gap_in) + bottom_in
    fig, ax = plt.subplots(figsize=(S.WIDTH, h))
    fig.subplots_adjust(left=0.2, right=0.84, top=1 - top_in / h, bottom=bottom_in / h)
    S.title(fig, ID_TITLE, ID_SUB)
    step = len(ARMS) + 1.4  # rows per group, the header's room included
    ticks, labels = [], []
    for i, (t, name) in enumerate(FIVE):
        y0 = -i * step
        ax.text(0.0, y0 + 0.9, name, fontsize=12, weight="bold", va="center", ha="left")
        if t not in data:
            ax.text(0.0, y0, absent.get(t, "not run"), fontsize=S.FONT, color=S.COL["muted"], va="center")
            continue
        m, p = data[t]
        hollow = t == LT
        cells = m["cells"]["PM"]
        n = cells["both"]["n"]
        ax.text(1.02, y0 + 0.9, f"n = {n}" + (f"  {S.STATUS_GLYPH['after']}" if hollow else ""), va="center",
                fontsize=S.FONT - 1, color=S.COL["muted"])  # fmt: skip
        ax.text(1.02, y0, f"the rule: {m['label']}", va="center", fontsize=S.FONT - 1, color=S.COL["muted"])
        S.record(out_name, t, "the rule's label (B's share against twice C's)", m["label"], n=n, source=rel(p))
        S.record(out_name, t, "scenes used", n, source=rel(p))
        for j, (arm, arm_text) in enumerate(ARMS):
            y, x = y0 - j, 0.0
            ticks.append(y)
            labels.append(arm_text)
            for key, what, style in ANSWERS:
                v, lo, hi = cells[arm][key]
                col = style.get("color", style.get("facecolor"))
                edge = style.get("edgecolor", col)
                kw = {"facecolor": "white", "edgecolor": edge, "hatch": "////", "lw": 1.0} if hollow else style
                ax.barh(y, v, left=x, height=0.72, zorder=2, **kw)
                if v >= 0.07:
                    dark = key in ("B", "C") and not hollow
                    box = {"facecolor": "white", "edgecolor": "none", "pad": 1.0} if hollow else None
                    ax.text(x + v / 2, y, f"{v:.2f}", ha="center", va="center", fontsize=S.LABEL_PT, bbox=box,
                            color="white" if dark else "#222222", zorder=4)  # fmt: skip
                S.record(out_name, t, f"the recall's answers, {arm_text}: {what}", round(v, 4), round(lo, 4),
                         round(hi, 4), n=cells[arm]["n"], source=rel(p))  # fmt: skip
                x += v
    ax.set_yticks(ticks, labels, fontsize=S.FONT)
    ax.set_ylim(-(len(FIVE) - 1) * step - len(ARMS) + 0.4, 1.45)
    ax.set_xlim(0, 1.0)
    ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
    ax.set_xlabel("share of the recall's answers")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    handles = [plt.Rectangle((0, 0), 1, 1, **{k: v for k, v in s.items() if k != "lw"}) for _, _, s in ANSWERS]
    fig.legend(handles, [w for _, w, _ in ANSWERS], loc="lower left", bbox_to_anchor=(0.01, 0.95 / h), ncol=4,
               frameon=False, fontsize=S.FONT - 1, handlelength=1.2, columnspacing=1.2)  # fmt: skip
    missing = [f"{name}: {absent.get(t, 'not run')}" for t, name in FIVE if t not in data]
    caption(fig, ["B: the item the lens part points to; C: the item whose locker the address points to (dose 2). "
                  "Twice as many B's as C's answers would mean the recall follows the lens part; twice as many C's, "
                  "the address; otherwise both.", LT_HATCH + (" " + "; ".join(missing) + "." if missing else "")],
            0.72)  # fmt: skip
    S.save(fig, out_name)
    return out_name


# fig20: 53.1's two number cells (x53_2x2's qa_num / qb_num)
CELLS = (("qa_num", "after"), ("qb_num", "before"))
ORDER_TITLE = "Question first, one model's lookup leans more on the lens part"
ORDER_SUB = "Switches lost without the lens part beyond a random part, question after or before the scene; at L"


def gate_label(cell: dict) -> str:
    """A number cell without numbers: its own gate (the recall's read on the original prompts)."""
    return f"not tested: gate {cell['gate']['org_read_accuracy']['PM']:.3f}"


def build_order_cell(verdict: Path, out_name: str = "fig20_order_cell") -> str:
    """fig20 from the combined x53_2x2 verdict (every model in one file)."""
    data = by_target((verdict,))
    src = rel(verdict)
    plt = S.setup()
    top_in, row_in, bottom_in = 0.95, 0.36, 2.3
    step = len(CELLS) + 1.0
    h = top_in + row_in * len(FIVE) * step + bottom_in
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(S.WIDTH, h), sharey=True, gridspec_kw={"width_ratios": [1.55, 1]})
    fig.subplots_adjust(left=0.2, right=0.97, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.08)
    S.title(fig, ORDER_TITLE, ORDER_SUB)
    S.extra_axis(ax, label=False)
    ax.set_xlabel("switches lost beyond random")
    ticks, labels = [], []
    for i, (t, name) in enumerate(FIVE):
        y0 = -i * step
        ax.text(-0.02, y0 + 0.85, name, transform=ax.get_yaxis_transform(), fontsize=12, weight="bold", ha="right",
                va="center")  # fmt: skip
        if t not in data:
            ax.text(0.0, y0 - 0.5, "not run", fontsize=S.FONT, color=S.COL["muted"], va="center")
            continue
        m = data[t][0]
        hollow = t == LT
        for j, (key, pos) in enumerate(CELLS):
            y = y0 - j
            ticks.append(y)
            labels.append(f"question {pos}")
            c = m["cells"][key]
            S.record(out_name, t, f"question {pos} the scene: scenes", c["gate"]["cases"], source=src)
            if c.get("status") != "tested":
                ax.text(-0.15, y, gate_label(c), fontsize=S.FONT - 1, color=S.COL["muted"], va="center")
                S.record(out_name, t, f"question {pos} the scene: the recall's gate (read right on the original "
                         "prompts)", c["gate"]["org_read_accuracy"]["PM"], n=c["gate"]["cases"], source=src)  # fmt: skip
                continue
            S.record(out_name, t, f"question {pos} the scene: items tested", c["gate"]["chosen"], source=src)
            for reader, col, dy in (("lookup", S.MARK_COL["lookup"], 0.15), ("recall", S.MARK_COL["recall"], -0.15)):
                v = c["lookup_extra"] if reader == "lookup" else c["readers"]["recall"]["extra"]["1"]
                ax.plot([v[1], v[2]], [y + dy] * 2, color=col, lw=1.6, zorder=2, solid_capstyle="butt")
                ax.plot([v[0]], [y + dy], "o", color=col, ms=7, mfc="white" if hollow else col, mec=col, mew=1.6,
                        zorder=3)  # fmt: skip
                S.record(out_name, t, f"question {pos} the scene: {reader}, switches lost beyond a random part",
                         round(v[0], 4), round(v[1], 4), round(v[2], 4), n=c["readers"][reader]["n"],
                         source=src)  # fmt: skip
        p = m.get("paired") or {}
        yp = y0 - 0.5
        if p.get("diff"):
            d = p["diff"]
            # the paired rule (Dan 11:25) came after the 27B's two cells were seen and before the 122B ran
            after = t == "qwen3.6-27b"
            ax2.plot([d[1], d[2]], [yp, yp], color=S.MARK_COL["lookup"], lw=1.6, zorder=2, solid_capstyle="butt")
            ax2.plot([d[0]], [yp], "o", color=S.MARK_COL["lookup"], ms=7, mfc="white" if after else S.MARK_COL["lookup"],
                     mec=S.MARK_COL["lookup"], mew=1.6, zorder=3)  # fmt: skip
            word = "order effect" if p["holds"] else "interval includes 0"
            ax2.text(d[0], yp + 0.4, word, fontsize=S.FONT - 1, color=S.COL["muted"], ha="center", va="bottom")
            S.record(out_name, t, "the lookup, question before minus after (paired)", round(d[0], 4), round(d[1], 4),
                     round(d[2], 4), n=p["n"], source=src)  # fmt: skip
            S.record(out_name, t, "the lookup, question before minus after: scenes both cells read", p["n"],
                     source=src)  # fmt: skip
            S.record(out_name, t, "the lookup, question before minus after: the rule's label", p["text"].split(":")[0]
                     .split(" (")[0], source=src)  # fmt: skip
        else:
            ax2.text(-0.23, yp, "not tested: question-first gate", fontsize=S.FONT - 1, color=S.COL["muted"],
                     va="center", bbox={"boxstyle": "square,pad=0.1", "fc": "white", "ec": "none"})  # fmt: skip
    ax.set_yticks(ticks, labels, fontsize=S.FONT)
    ax.set_ylim(-(len(FIVE) - 1) * step - len(CELLS) + 0.4, 1.3)
    ax.tick_params(axis="y", length=0)
    ax2.set_xlim(-0.25, 0.45)
    ax2.axvline(0, color="#999999", lw=0.8, zorder=1)
    ax2.set_xticks([-0.2, 0, 0.2, 0.4], ["−0.2", "0", "0.2", "0.4"])
    ax2.set_xlabel("lookup: before minus after")
    ax2.tick_params(axis="y", length=0)
    g = "#7a7a7a"  # S.status_handles' grey, with the line colour set too (its open mark leaves it to the colour cycle)
    handles = [plt.Line2D([], [], marker="o", ls="", color=S.MARK_COL[r], ms=7) for r in ("lookup", "recall")]
    handles += [plt.Line2D([], [], marker="o", ls="", color=g, ms=7),
                plt.Line2D([], [], marker="o", ls="", color=g, mfc="white", mec=g, mew=1.6, ms=7)]  # fmt: skip
    fig.legend(handles, ["lookup", "recall", S.STATUS_TEXT["fixed"], S.STATUS_TEXT["after"]], loc="lower left",
               bbox_to_anchor=(0.01, 1.08 / h), ncol=4, frameon=False, fontsize=S.FONT - 1)  # fmt: skip
    caption(fig, ["Grey band: the lookup's 0.10 bar. Not tested: the question-first cell's recall missed the 0.80 "
                  "gate (9B, Muse, Lightning). Right: the lookup's loss with the question first minus after, on the "
                  "scenes both cells read; open: that rule was set after the 27B's two cells were seen, before the "
                  "122B ran.", LT_HATCH + " " + B122_NOTE], 1.0)  # fmt: skip
    S.save(fig, out_name)
    return out_name


def record_card_numbers(id_verdict: Path, order_verdict: Path, brief: Path = S.REPO / "jobs" / "c3" / "batch53.yaml"):
    """The numbers the two cards quote that fig19 / fig20 do not draw (figure "cards"): Dan's 12:10 descriptive range
    for 53.6, and 53.1's denominator and the 122B's rerun caveat (Dan 12:40, wording_531)."""
    ids = by_target((id_verdict,))
    src = rel(id_verdict)
    # Dan's "(0.25-0.30 each)" on the 9B and Lightning and "(<= 0.11)" on the 27B and Muse
    for pair, targets, ends in (("the 9B and Lightning", ("qwen3.5-9b", LT), ("smallest", "largest")),
                                ("the 27B and Muse", ("qwen3.6-27b", "muse-glimmer-30b"), ("largest",))):  # fmt: skip
        shares = [ids[t][0]["cells"]["PM"]["both"][k][0] for t in targets for k in ("B", "C")]
        for which in ends:
            v = min(shares) if which == "smallest" else max(shares)
            S.record("cards", pair, f"53.6: both parts, {pair}: the {which} of B's and C's shares", round(v, 4),
                     source=src)  # fmt: skip
    across = json.loads(id_verdict.read_text())["across"]
    S.record("cards", "across models", "53.6: across models, the rule", across["label"], source=src)
    for t, v in across["per_model"].items():
        S.record("cards", t, "53.6: across models, wanted", v["wanted"], source=src)

    order = by_target((order_verdict,))
    src = rel(order_verdict)
    both = [t for t, (m, _) in order.items() if all(m["cells"][k].get("status") == "tested" for k, _ in CELLS)]
    S.record("cards", "across models", "53.1: models where both number cells passed their gates", len(both),
             source=src)  # fmt: skip
    S.record("cards", "across models", "53.1: of those, models with order dependence",
             sum(bool(order[t][0]["paired"].get("holds")) for t in both), source=src)  # fmt: skip
    for t, (m, _) in order.items():  # Dan 11:10, across the number cells; the verdict's words before its reason
        S.record("cards", t, "53.1: the lookup at most 0.10 beyond random in both number cells",
                 m["position"]["text"].split(":")[0].split(" (")[0], source=src)  # fmt: skip
        d = (m.get("paired") or {}).get("diff")
        if d:  # Dan 13:15 (answers_1315 item 3): "lower bound +0.01", signed, as he wrote it
            S.record("cards", t, "53.1: the lookup, question before minus after (paired): the interval's lower bound",
                     f"{d[1]:+.2f}", source=src)  # fmt: skip
    agree = order["qwen3.5-122b-a10b"][0]["cells"]["qa_num"]["agreement"]
    for reader in ("recall", "lookup"):
        w = agree[reader]["whole"]
        S.record("cards", "qwen3.5-122b-a10b", f"53.1: the rerun's question-after cell, {reader}: items whose whole "
                 "change agrees with the stored run", w["agree_switch"], n=w["n"], source=src)  # fmt: skip
    S.record("cards", "qwen3.5-122b-a10b", "53.1: the rerun's question-after cell: items compared",
             agree["recall"]["whole"]["n"], source=src)  # fmt: skip
    arm1 = agree["recall"]["extra_loss_arm1"]
    S.record("cards", "qwen3.5-122b-a10b", "53.1: the recall's loss beyond random without the lens part, stored run → "
             "rerun", f"{arm1['stored']:.3f} → {arm1['rerun']:.3f}", source=src)  # fmt: skip
    noise = re.search(r"~±(\d\.\d+) run-to-run noise", brief.read_text())
    S.record("cards", "qwen3.5-122b-a10b", "53.1: run-to-run noise beyond the bootstrap (Dan's estimate)",
             f"~±{noise.group(1)}", source=rel(brief))  # fmt: skip
