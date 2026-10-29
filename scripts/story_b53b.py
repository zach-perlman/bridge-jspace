"""Batch 53's README figures for Part III and Part IV (Dan's README brief, 29 Oct 12:50, docs_1250 item 2: "the address
in code and tool output (53.7 probe; routes and monitor when they land)" and "the Lightning attention blocks (53.4 +
span), one card"). Both unverified until hand-checked.

  fig21_code_tool         53.7, adapted design (Dan 12:10, decisions_1210: a lookup-only gate; the recall is not part
                          of this test). A: the locker probe at the bridge word, locker-first scenes, in code and in tool
                          output, against its layout baseline, the prose probe marked. B: the routes test, another item
                          moved, at L: the position share without the address against without a random part of its
                          size, and with only the address against only a random part. Five model slots; a cell without
                          a verdict keeps its slot with a grey label ("running", "not run", "not tested: gate ...").
  fig22_attention_blocks  53.4 and its follow-up (Dan's 11:25 control span): on Lightning, the share of the whole change's
                          switches cut when later positions cannot attend to the bridge word in attention block 19, 26,
                          both, every attention block after L, and the control; then the span from the bridge word to
                          the scene's end in blocks 19 and 26 against the control span. Lightning hollow (gate chosen
                          after its 60-scene pre-check); the 9B, 27B and Muse "not applicable", the 122B "not run", as in
                          the ledger's card.

Every plotted number is recorded for figures/story/data.csv with its source file; record_card_numbers() records the
numbers the two cards quote that the figures do not draw (figure "cards").
"""

from __future__ import annotations

import json
from pathlib import Path

from scripts import story_style as S
from scripts.story_b50 import caption

R = S.REPO / "results"
# 53.7: the newest verdict first; a (model, format) cell is taken from the first verdict that holds it, so a verdict
# under the lookup-only gate (decisions_1210) wins over the earlier two-reader one. The 27B's probe ran before 12:10
# under X0's gate on both readers and passed both: "adapted design" only (Dan 13:15, answers_1315 item 4). Only the
# combined verdicts are cited (coordinator, 29 Oct): the probe's over the 9B (115640Z), the routes test's over both
# models in code (120413Z, which replaces 115759Z); the tool-output routes' combined verdict is not written yet
PROBES_537 = (R / "x0_probe" / "x53_7_probe-20261029T115640Z" / "verdict.json",
              R / "x0_probe" / "x53_7_probe-20261029T110647Z" / "verdict.json")  # fmt: skip
ROUTES_537 = (R / "x6_routes" / "x53_7_routes-20261029T120413Z" / "verdict.json",)
# cells without a combined verdict yet (the coordinator, 29 Oct ~13:20): the routes test in tool output, both models
RUNNING_537 = {"probe": {("qwen3.6-27b", "code"), ("qwen3.6-27b", "tool")},
               "routes": {("qwen3.5-9b", "tool"), ("qwen3.6-27b", "tool")}}  # fmt: skip
ATTNBLOCK = R / "x53_attnblock" / "x53_attnblock-20261029T091303Z" / "verdict.json"
# the follow-up with Dan's 11:25 control (one placement; the first run, x53_attnspan-20261029T102727Z, superseded); the
# verdict rewritten at Dan's 13:15 (answers_1315) with the scenes where the clean answer survives the span block beside
# the label (the rest identical to x53_attnspan_c-20261029T105304Z)
ATTNSPAN = R / "x53_attnblock" / "x53_attnspan_c-20261029T121412Z" / "verdict.json"

LT = "nemotron-3.5-lightning"
MODELS = (("qwen3.5-9b", "9B"), ("qwen3.6-27b", "27B"), ("muse-glimmer-30b", "Muse"), (LT, "Lightning"),
          ("qwen3.5-122b-a10b", "122B"))  # fmt: skip
RAN_537 = ("qwen3.5-9b", "qwen3.6-27b")  # 53.7's models (Dan 11:10: 27B then 9B)
FORMATS = (("code", "code"), ("tool", "tool output"))
NOT_RUN_H = 0.5  # fig21: a model 53.7 did not run keeps half a row
TARGET, STRATUM = "locker sentence", "before"  # probe (b), locker before the pick (x0_probe v4's headline)
PROBE_COL, POS_COL, CTL_COL = S.COL["position"], S.COL["position"], S.COL["control"]
GREY = S.COL["muted"]
WHITE = {"boxstyle": "square,pad=0.1", "fc": "white", "ec": "none"}  # a label over the bar lines
# fig22's rows: (verdict key, arm, label); the span rows read the follow-up's 83 scenes where the control fits
BLOCK_ARMS = (("b19", "block 19"), ("b26", "block 26"), ("both", "blocks 19 and 26"),
              ("after", "every attention block after L"), ("control", "control: another token, both blocks"))  # fmt: skip
SPAN_ARMS = (("span", "the span, blocks 19 and 26"), ("span_ctrl", "control span, same length"),
             ("both", "the bridge word, both blocks (rerun)"))  # fmt: skip
NOT_LT = {"qwen3.5-9b": "not applicable: a test of Lightning's blocks",
          "qwen3.6-27b": "not applicable: a test of Lightning's blocks",
          "muse-glimmer-30b": "not applicable: a test of Lightning's blocks", "qwen3.5-122b-a10b": "not run"}  # fmt: skip


def rel(path: Path) -> str:
    return str(path.relative_to(S.REPO))


def tokens(x: float) -> int | float:
    """A median token count as a count when whole (the page shows 9, not 9.00)."""
    return int(x) if float(x).is_integer() else x


def runs_537(paths: tuple[Path, ...]) -> dict[tuple[str, str], tuple[dict, Path]]:
    """(model, format) -> (run, its verdict path), the first verdict in paths that holds the cell."""
    out: dict[tuple[str, str], tuple[dict, Path]] = {}
    for p in paths:
        for r in json.loads(p.read_text())["runs"]:
            out.setdefault((r["model"], r["format"]), (r, p))
    return out


def probe_row(rows: list[dict], stratum: str = STRATUM, target: str = TARGET) -> dict:
    return next(r for r in rows if r["subset"] == "all" and r["stratum"] == stratum and r["target"] == target)


def cell_status(kind: str, model: str, fmt: str, got: dict) -> str:
    """A 53.7 cell's status: the verdict's own ('tested', 'not tested (gate x < 0.80)'), else running / not run."""
    if (model, fmt) in got:
        run = got[(model, fmt)][0]
        st = run["status"] if kind == "probe" else run["status"]["C2"]
        return st
    return "running" if (model, fmt) in RUNNING_537[kind] else "not run"


def hbar(ax, y: float, v, col: str, h: float, hollow: bool = False, label: bool = True) -> None:
    """A horizontal share bar with its 95% whisker and its value right of the whisker (as Fig. 7's)."""
    kw = {"facecolor": "white", "edgecolor": col, "lw": 1.4} if hollow else {"color": col, "lw": 0}
    ax.barh(y, v[0], height=h, zorder=2, **kw)
    ax.plot([v[1], v[2]], [y, y], color="#1e1e1e", lw=1.2, zorder=3, solid_capstyle="butt")
    if label:
        ax.text(max(v[0], v[2]) + 0.025, y, f"{v[0]:.2f}", va="center", fontsize=S.LABEL_PT,
                color=GREY if col == CTL_COL else "#1e1e1e")  # fmt: skip


def slots_537() -> list[tuple[str, str, str | None]]:
    """fig21's rows top to bottom: (model, row label, format or None for a model 53.7 did not run)."""
    out = []
    for t, name in MODELS:
        if t in RAN_537:
            out += [(t, f"{name} · {word}", fmt) for fmt, word in FORMATS]
        else:
            out.append((t, name, None))
    return out


def build_code_tool(probes: tuple[Path, ...] = PROBES_537, routes: tuple[Path, ...] = ROUTES_537,
                    out_name: str = "fig21_code_tool") -> str:  # fmt: skip
    """fig21_code_tool from 53.7's probe and routes verdicts (newest first)."""
    got_p, got_r = runs_537(probes), runs_537(routes)
    rows = slots_537()
    # a format row is one unit high (B's two arms, each with its random part); a model 53.7 did not run, NOT_RUN_H
    heights = [1.0 if fmt else NOT_RUN_H for _, _, fmt in rows]
    ys = [-(sum(heights[:i]) + heights[i] / 2) for i in range(len(rows))]
    plt = S.setup()
    top_in, unit_in, bottom_in = 1.75, 0.8, 2.45
    h = top_in + unit_in * sum(heights) + bottom_in
    fig = plt.figure(figsize=(S.WIDTH, h))
    S.title(fig, "Code and tool output: the address is readable; in code it carries less",
            "A: a probe at the bridge word, locker before the pick. B: without the address, or with only the address, at L.")  # fmt: skip
    box = (bottom_in / h, unit_in * sum(heights) / h)
    a = fig.add_axes((0.215, box[0], 0.29, box[1]))
    b = fig.add_axes((0.565, box[0], 0.33, box[1]), sharey=a)
    head = {"fontsize": 12, "weight": "bold", "va": "bottom", "linespacing": 1.05}
    fig.text(0.01, 1 - 1.4 / h, "A  A probe reads the address", **head)
    fig.text(0.53, 1 - 1.4 / h, "B  Without the address, fewer\n     position answers", **head)
    ns_a, ns_b = [], []
    first_a = first_b = True
    for (t, _, fmt), y in zip(rows, ys, strict=True):
        if fmt is None:
            for ax in (a, b):
                ax.text(0.02, y, "not run", va="center", fontsize=S.FONT, color=GREY)
            S.record(out_name, t, "code and tool output: not run", "not run", source=rel(probes[0]))
            continue
        # A: the probe against its layout baseline, the prose probe marked
        st = cell_status("probe", t, fmt, got_p)
        S.record(out_name, t, f"code and tool output, {fmt}: the probe's status", st,
                 source=rel(got_p[(t, fmt)][1]) if (t, fmt) in got_p else rel(probes[0]))  # fmt: skip
        if st != "tested":
            run = got_p.get((t, fmt), (None, None))[0]
            hollow = bool(run and run.get("hollow"))
            text = st.replace("not tested (", "not tested: ").rstrip(")") if st.startswith("not tested") else st
            a.text(0.02, y, text + (f"  {S.STATUS_GLYPH['after']}" if hollow else ""), va="center", fontsize=S.FONT,
                   color=GREY)  # fmt: skip
        else:
            run, p = got_p[(t, fmt)]
            r, prose = probe_row(run["rows"]), probe_row(run["prose_v4_rows"])
            hbar(a, y + 0.13, r["probe"], PROBE_COL, 0.36)
            hbar(a, y - 0.22, r["layout"], "white", 0.15)
            a.patches[-1].set(edgecolor="#9a9a9a", hatch="////", lw=0.6)
            a.plot([prose["probe"][0]] * 2, [y + 0.13 - 0.25, y + 0.13 + 0.25], color="#1e1e1e", lw=1.6, zorder=4)
            src = rel(p)
            S.record(out_name, t, f"code and tool output, {fmt}: the locker probe at the bridge word, locker-first scenes",
                     *r["probe"], n=r["n"], source=src)  # fmt: skip
            S.record(out_name, t, f"code and tool output, {fmt}: the locker probe's layout baseline, locker-first scenes",
                     *r["layout"], n=r["n"], source=src)  # fmt: skip
            S.record(out_name, t, f"code and tool output, {fmt}: the locker probe in prose, locker-first scenes (stored)",
                     *prose["probe"], n=prose["n"], source=src)  # fmt: skip
            ns_a.append(str(r["n"]))
            if first_a:  # the panel names its marks once, on its first drawn row
                a.text(0.03, y + 0.13, "probe", va="center", fontsize=S.LABEL_PT, color="white", zorder=5)
                a.text(r["layout"][2] + 0.21, y - 0.22, "layout", va="center", fontsize=S.LABEL_PT, color=GREY)
                a.text(prose["probe"][0], y + 0.42, "prose", ha="center", va="bottom", fontsize=S.LABEL_PT,
                       color="#1e1e1e")  # fmt: skip
                first_a = False
        # B: the routes test, another item moved
        st = cell_status("routes", t, fmt, got_r)
        S.record(out_name, t, f"code and tool output, {fmt}: the routes test's status (another item moved)", st,
                 source=rel(got_r[(t, fmt)][1]) if (t, fmt) in got_r else rel(routes[0]))  # fmt: skip
        if st != "tested":
            b.text(0.02, y, st, va="center", fontsize=S.FONT, color=GREY)
            continue
        run, p = got_r[(t, fmt)]
        cells = run["cells"]
        for dy, arm, ctl, word in ((0.22, "no_alf", "no_alf_rand", "without the address"),
                                   (-0.2, "keep_alf", "keep_alf_rand", "only the address")):  # fmt: skip
            got, rand = cells[f"C2|{arm}"], cells[f"C2|{ctl}"]
            gp = got["share"]["position"]
            hbar(b, y + dy + 0.07, gp, POS_COL, 0.17)
            hbar(b, y + dy - 0.1, rand["share"]["position"], CTL_COL, 0.07)
            b.text(max(gp[0], gp[2]) + 0.17, y + dy + 0.07, word, va="center", fontsize=S.LABEL_PT, color="#1e1e1e")
            S.record(out_name, t, f"code and tool output, {fmt}: another item moved, {arm}: position share",
                     *got["share"]["position"], n=got["n"], source=rel(p))  # fmt: skip
            S.record(out_name, t, f"code and tool output, {fmt}: another item moved, {ctl}: position share",
                     *rand["share"]["position"], n=rand["n"], source=rel(p))  # fmt: skip
        ns_b.append(str(cells["C2|no_alf"]["n"]))
        if first_b:
            nr = cells["C2|no_alf_rand"]["share"]["position"]
            b.text(nr[2] + 0.17, y + 0.22 - 0.1, "random", va="center", fontsize=S.LABEL_PT, color=GREY)
            first_b = False
    a.set_yticks(ys, [lab for _, lab, _ in rows])
    a.set_ylim(-sum(heights), 0)
    for ax in (a, b):
        ax.set_xlim(0, 1.15)
        ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.spines["bottom"].set_bounds(0, 1)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#eeeeee")
        ax.set_axisbelow(True)
    b.tick_params(axis="y", labelleft=False)
    a.set_xlabel("share of scenes")
    b.set_xlabel("position answers (share)")
    S.panel_tag(a, ", ".join(ns_a), "after")
    S.panel_tag(b, ", ".join(ns_b), "fixed")
    caption(fig, ["Adapted design: a lookup-only gate (the lookup says and reads both prompts right on at least 0.80 of "
                  "the scenes); the recall is not part of this test. The 9B's code probe: that gate set after the data "
                  f"({S.STATUS_GLYPH['after']}). The 27B's probe ran under the earlier gate on both readers and passed "
                  "both. The routes test in tool output and the monitor: running.",
                  "Tool output: the scene as a tool's reply in prose, its bridge word about 250 tokens later than in a "
                  "prose prompt. B: another item moved; the address removed or added is the one fit on prose, carried "
                  "over; grey: a random part of the same size. Muse, Lightning and the 122B: not run."], 1.6)  # fmt: skip
    S.save(fig, out_name)
    return out_name


def build_attention_blocks(blocks: Path = ATTNBLOCK, span: Path = ATTNSPAN,
                           out_name: str = "fig22_attention_blocks") -> str:  # fmt: skip
    """fig22_attention_blocks from 53.4's verdict and its follow-up's (Dan's 11:25 control span)."""
    v, sp = json.loads(blocks.read_text()), json.loads(span.read_text())
    # rows top to bottom: (kind, model or section, arm key, label)
    rows: list[tuple[str, str, str, str]] = [("absent", t, "", name) for t, name in MODELS[:3]]
    rows.append(("head", LT, "", f"Lightning {S.STATUS_GLYPH['after']}: the bridge word, {v['readers']['lookup']['n']} "
                                  "scenes"))  # fmt: skip
    rows += [("block", LT, k, lab) for k, lab in BLOCK_ARMS]
    rows.append(("head", LT, "", f"Lightning {S.STATUS_GLYPH['after']}: the span to the scene's end, "
                                 f"{sp['readers']['lookup']['n']} scenes"))  # fmt: skip
    rows += [("span", LT, k, lab) for k, lab in SPAN_ARMS]
    rows.append(("absent", MODELS[4][0], "", MODELS[4][1]))
    plt = S.setup()
    top_in, row_in, bottom_in = 0.95, 0.42, 2.0
    h = top_in + row_in * len(rows) + bottom_in
    fig, ax = plt.subplots(figsize=(S.WIDTH, h))
    fig.subplots_adjust(left=0.37, right=0.97, top=1 - top_in / h, bottom=bottom_in / h)
    S.title(fig, "Two attention blocks carry part of Lightning's lookup, not all of it",
            "Share of the whole change's switches cut when later tokens cannot attend; dashed 0.6, dotted 0.3")  # fmt: skip
    ax.axvline(0, color="#999999", lw=0.8, zorder=1)
    for x, ls in ((0.6, "--"), (0.3, ":")):
        ax.axvline(x, color="#7a7a7a", lw=1.0, ls=ls, zorder=1)
    ticks, labels = [], []
    named = False
    for i, (kind, t, k, lab) in enumerate(rows):
        y = -i
        if kind == "head":  # a section's heading, over the plot from the left edge of its row labels
            ax.text(-0.55, y, lab, transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=S.FONT,
                    weight="bold", bbox=WHITE, zorder=6)  # fmt: skip
            continue
        ticks.append(y)
        if kind == "absent":
            labels.append(lab)
            ax.text(-0.08, y, NOT_LT[t], va="center", fontsize=S.FONT, color=GREY, bbox=WHITE, zorder=6)
            S.record(out_name, t, "attention blocks: not applicable or not run", NOT_LT[t], source=rel(blocks))
            continue
        labels.append(lab)
        src, part = (blocks, v) if kind == "block" else (span, sp)
        what = "the bridge word blocked" if kind == "block" else "the span follow-up"
        for dy, reader, col in ((0.14, "lookup", S.MARK_COL["lookup"]), (-0.14, "recall", S.MARK_COL["recall"])):
            r = part["readers"][reader]
            val = (r["cut"][k], *r["cut_ci"][k])
            ax.plot([val[1], val[2]], [y + dy] * 2, color=col, lw=1.5, zorder=3, solid_capstyle="butt")
            ax.plot([val[0]], [y + dy], "o", color=col, ms=7, mfc="white", mec=col, mew=1.6, zorder=4)  # hollow
            if reader == "lookup":
                ax.text(max(val[0], val[2]) + 0.03, y + dy, f"{val[0]:.2f}", va="center", fontsize=S.LABEL_PT,
                        color=col)  # fmt: skip
            S.record(out_name, LT, f"attention blocks, {what}, {reader}: switches cut, {lab}", *val, n=r["n"],
                     source=rel(src))  # fmt: skip
        if not named:  # the first drawn row names the two readers
            named = True
            ax.text(0.93, y + 0.14, "lookup", ha="right", va="center", fontsize=S.LABEL_PT, color=S.MARK_COL["lookup"])
            ax.text(0.93, y - 0.14, "recall", ha="right", va="center", fontsize=S.LABEL_PT, color=S.MARK_COL["recall"])
    ax.set_yticks(ticks, labels)
    ax.set_ylim(-len(rows) + 0.5, 0.5)
    ax.set_xlim(-0.1, 1.0)
    ax.set_xticks([0, 0.3, 0.6, 1.0], ["0", "0.3", "0.6", "1"])
    ax.set_xlabel("share of the whole change's switches cut")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    S.panel_tag(ax, f"{v['readers']['lookup']['n']}, {sp['readers']['lookup']['n']}", "after")  # Lightning's gate
    caption(fig, ["Lightning hollow: its gate chosen after its 60-scene pre-check was seen. Rule fixed in advance: two "
                  "blocks if both cut the lookup's switches by at least 0.6 and the control by at most 0.15; not through "
                  "attention if every attention block after L cuts under 0.3; both runs: in between.",
                  "The span: every token after the scene cannot attend to the span from the bridge word to the scene's "
                  "end; the control span: as long, ending before the bridge's sentence, on the "
                  f"{sp['readers']['lookup']['n']} of {v['readers']['lookup']['n']} scenes where it fits. The 9B, 27B "
                  "and Muse: not applicable; the 122B: not run."], 1.55)  # fmt: skip
    S.save(fig, out_name)
    return out_name


def record_card_numbers(probes: tuple[Path, ...] = PROBES_537, routes: tuple[Path, ...] = ROUTES_537,
                        blocks: Path = ATTNBLOCK, span: Path = ATTNSPAN) -> None:  # fmt: skip
    """The numbers the two cards quote that the figures do not draw, under figure "cards"."""
    got_p, got_r = runs_537(probes), runs_537(routes)
    for (t, fmt), (run, p) in got_p.items():
        g = run["gate"]
        if "lookup_right_share" in g:  # the lookup-only gate (decisions_1210), as the verdict states it (3 decimals)
            S.record("cards", t, f"53.7, {fmt}: the probe's gate, the lookup says and reads both prompts right",
                     f"{g['lookup_right_share']:.3f} ({g['cases']} scenes)", n=g["cases"], source=rel(p))  # fmt: skip
        else:  # X0's earlier gate on both readers: the unedited prompt's chat read
            acc = g["org_read_accuracy"]
            S.record("cards", t, f"53.7, {fmt}: the probe's gate (earlier design), lookup / recall read right",
                     f"{acc['PP']:.3f} / {acc['PM']:.3f}", n=g["cases"], source=rel(p))  # fmt: skip
        S.record("cards", t, f"53.7, {fmt}: the probe's scenes (one token at one position in both prompts)",
                 g["cases"], source=rel(p))  # fmt: skip
        if run["status"] != "tested":
            continue
        r = probe_row(run["rows"])
        S.record("cards", t, f"53.7, {fmt}: the probe's scenes, locker before the pick", r["n"], source=rel(p))
        S.record("cards", t, f"53.7, {fmt}: the probe's bridge entities, locker before the pick", r["entities"],
                 source=rel(p))  # fmt: skip
        for stratum, target, what in (("after", TARGET, "locker sentence, locker-after scenes (the control)"),
                                      ("before", "answer digit", "answer digit, locker-first scenes")):  # fmt: skip
            r = probe_row(run["rows"], stratum, target)
            S.record("cards", t, f"53.7, {fmt}: the probe, {what}", *r["probe"], n=r["n"], source=rel(p))
            base = r.get("best_baseline") or "majority"
            if isinstance(r.get(base), list):  # a baseline of its own; "chance" is the class count's alone
                S.record("cards", t, f"53.7, {fmt}: the probe's best baseline ({base}), {what}", *r[base], n=r["n"],
                         source=rel(p))  # fmt: skip
            S.record("cards", t, f"53.7, {fmt}: chance, {what}", round(r["chance"], 2), source=rel(p))
    for (t, fmt), (run, p) in got_r.items():
        g = run["gate"]["gate"]["C2"]
        S.record("cards", t, f"53.7, {fmt}: the routes test's gate, another item moved (lookup-only)",
                 f"{g['lookup_right_share']:.3f} ({g['cases']} scenes)", n=g["cases"], source=rel(p))  # fmt: skip
        S.record("cards", t, f"53.7, {fmt}: the routes test, the recall's read right (descriptive)",
                 round(g["descriptive"]["org_read_accuracy"]["PM"], 3), source=rel(p))  # fmt: skip
        whole = run["cells"]["C2|whole"]
        S.record("cards", t, f"53.7, {fmt}: the routes test's items, another item moved", whole["n"], source=rel(p))
        S.record("cards", t, f"53.7, {fmt}: another item moved, the whole change: the routes the rule counts as used",
                 ", ".join(whole["used"]), source=rel(p))  # fmt: skip
        for route in ("identity", "position", "value"):
            S.record("cards", t, f"53.7, {fmt}: another item moved, the whole change: {route} share",
                     *whole["share"][route], n=whole["n"], source=rel(p))  # fmt: skip
        c0 = run["c0_check"]
        S.record("cards", t, f"53.7, {fmt}: the sanity swap's lookup switch (against the reference)",
                 f"{c0['c0_lookup_switch']:.3f} vs {c0['reference']:.3f}", source=rel(p))  # fmt: skip
        # Dan 13:15 (answers_1315 item 4): U carried over from prose, not refit; the run's manifest names the prose
        # probe run it was fit on (x6_routes.stage_run, x0_massmean on that run's states at L)
        man = R / "x6_routes" / run["run"] / "manifest.json"
        S.record("cards", t, f"53.7, {fmt}: the routes test's address, fit on (the prose probe run)",
                 json.loads(man.read_text())["alf_from"], source=rel(man))  # fmt: skip
    v, sp = json.loads(blocks.read_text()), json.loads(span.read_text())
    lk = v["readers"]["lookup"]
    S.record("cards", LT, "53.4: scenes, bridge entities", f"{lk['n']} scenes, {lk['entities']} bridge entities",
             source=rel(blocks))  # fmt: skip
    S.record("cards", LT, "53.4: lookups switched by the whole change", lk["switched"]["none"], n=lk["n"],
             source=rel(blocks))  # fmt: skip
    for k, lab in BLOCK_ARMS:
        S.record("cards", LT, f"53.4: the lookup keeps its clean answer, {lab}", lk["clean_kept"][k], n=lk["n"],
                 source=rel(blocks))  # fmt: skip
    S.record("cards", LT, "53.4: the rule (lookup)", v["label"]["label"], source=rel(blocks))
    sl = sp["readers"]["lookup"]
    S.record("cards", LT, "53.4 span: the rule (lookup)", sp["label"], source=rel(span))
    S.record("cards", LT, "53.4 span: scenes where the control fits, bridge entities",
             f"{sl['n']} scenes, {sl['entities']} bridge entities", source=rel(span))  # fmt: skip
    S.record("cards", LT, "53.4 span: scenes dropped (no control fits)", sp["selection"]["dropped_scenes"],
             source=rel(span))  # fmt: skip
    S.record("cards", LT, "53.4 span: share of the rule's scenes whose lookup switches under the whole change",
             sl["S"]["none"], n=sl["n"], source=rel(span))  # fmt: skip
    for k, lab in SPAN_ARMS:
        S.record("cards", LT, f"53.4 span: the lookup keeps its clean answer, {lab}", sl["clean_kept"][k], n=sl["n"],
                 source=rel(span))  # fmt: skip
    for key, lab in (("rule", "the rule's scenes"), ("dropped", "the dropped scenes")):
        S.record("cards", LT, f"53.4 span: median span length in tokens, {lab}",
                 tokens(sp["selection"]["median_span_tokens"][key]), source=rel(span))  # fmt: skip
    for key, lab in (("span", "the span"), ("control", "the control span")):
        S.record("cards", LT, f"53.4 span: median distance from the end of {lab} to the question",
                 tokens(sp["to_question_median"][key]), source=rel(span))  # fmt: skip
    al, nc = sp["beside_all"]["lookup"], sp["beside_no_control"]["lookup"]
    S.record("cards", LT, "53.4 span: lookup switches cut by the span, all scenes", al["cut"]["span"],
             *al["cut_ci"]["span"], n=al["n"], source=rel(span))  # fmt: skip
    S.record("cards", LT, "53.4 span: lookup switches cut by the span, scenes without a control",
             nc["cut"]["span"], *nc["cut_ci"]["span"], n=nc["n"], source=rel(span))  # fmt: skip
    S.record("cards", LT, "53.4 span: share of the scenes without a control whose lookup switches",
             nc["S"]["none"], n=nc["n"], source=rel(span))  # fmt: skip
    # Dan 13:15 (answers_1315): descriptive, beside the label (computed on every rule scene)
    sv = sp["clean_survives_span"]
    sl2 = sv["lookup"]
    S.record("cards", LT, "53.4 span: the rule's scenes where the lookup's clean answer survives the span block",
             f"{sv['scenes']} of {sv['of']}", n=sv["scenes"], source=rel(span))  # fmt: skip
    S.record("cards", LT, "53.4 span: bridge entities, the scenes where the clean answer survives",
             sl2["entities"], source=rel(span))  # fmt: skip
    for k, lab in (("span", "the span"), ("span_ctrl", "the control span")):
        S.record("cards", LT, f"53.4 span, the scenes where the clean answer survives: lookup switches cut by {lab}",
                 sl2["cut"][k], *sl2["cut_ci"][k], n=sl2["n"], source=rel(span))  # fmt: skip
