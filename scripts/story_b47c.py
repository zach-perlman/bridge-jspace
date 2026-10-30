"""README figures for batch 47 (part c): one figure per test, each drawn from that test's verdict folder (the json its
`verdict` stage writes) in story_style's look, every plotted number recorded for data/figures/depth/data.csv.

  47.14 x47_chain.py      x47_14-<UTC>/x47_14.json            Fig. 21: chained addresses (hall, then locker)
  47.11 x47_agnostic.py   x47_11-<UTC>/x47_11.json            Fig. 22: the pointer on fruits and names
  47.12 x47_twodefs.py    x47_12-<UTC>/x47_12.json            Fig. 23: two definitions of the lens part
  47.15 x47_source.py     x47_15-<UTC>/x47_15.json            Fig. 24: one question, two sources
  47.16 x47_distance.py   x47_16-<UTC>/x47_16.json            Fig. 25: filler sentences before the picks
  D4    x47_depth_cpu.py  persistence-<UTC>/persistence.json  Fig. 26: the address across depth

The title is the claim, built from the verdict's labels so it reads true for any outcome (pass `title` once Dan has
worded it); the rule's bars are thin labelled lines; every cell is fixed in advance (filled marks). The panels, rows
and helpers are story_b47a's; at most 3 panels, 4 legend entries and 2 subtitle lines per figure. Tested on planted
verdicts and on the two opened ones (tests/test_story_b47c.py); readme_story_figures draws them once their verdict
folders are named there.

    from scripts import story_b47c as B
    B.build_chain(Path("results/x47_chain/x47_14-<UTC>"), "fig21_chained_addresses")   # into figures/depth/
"""

from __future__ import annotations

import itertools
import json
import sys
import textwrap
from pathlib import Path

from matplotlib.lines import Line2D
from matplotlib.transforms import blended_transform_factory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import readme_story_figures as F
from scripts import story_b47a as A
from scripts import story_style as S

NOTE = ""  # put before every subtitle (the planted previews set "PLANTED data, not results. ")
SUB_LINES = 2  # subtitle lines at most
ROW_IN = 1.0  # inches per model row (three marks per row)
SHORT = {"qwen3.5-9b": "9B", "qwen3.6-27b": "27B", "qwen3.5-122b-a10b": "122B", "muse-glimmer-30b": "Muse"}
GREY = S.COL["control"]
fig_id, by_target, iv, bar, panel_title = A.fig_id, A.by_target, A.iv, A.bar, A.panel_title


def frame(title: str, sub: str, ratios: tuple[float, ...], body_in: float, legend=None, **kw):
    """story_b47a's frame with this module's NOTE first and the subtitle held to SUB_LINES lines."""
    keep = (NOTE + sub).replace("J++ ", "J++ ")
    n = len(textwrap.wrap(keep, A.WRAP, break_on_hyphens=False))
    assert n <= SUB_LINES, f"subtitle on {n} lines (at most {SUB_LINES}): {NOTE + sub!r}"
    return A.frame(title, NOTE + sub, ratios, body_in, legend=legend, **kw)


def shown(models: list[dict]) -> list[tuple[str, str]]:
    """(target, short key) of the models in the verdict, in story_style's order (9B, 27B, 122B, Muse)."""
    have = {m["target"] for m in models}
    return [(t, m) for t, m, _ in S.MODELS if t in have]


def names(targets: list[str]) -> str:
    """'the 9B and Muse', 'the 27B, the 9B and Muse'."""
    out = [SHORT[t] if t == "muse-glimmer-30b" else f"the {SHORT[t]}" for t in targets]
    return out[0] if len(out) == 1 else ", ".join(out[:-1]) + " and " + out[-1]


def handle(color: str, marker: str = "o", ms: float = 8, **kw) -> Line2D:
    return Line2D([], [], marker=marker, ls="", color=color, ms=ms, **kw)


def mark(ax, y: float, v: tuple[float, float, float] | None, color: str, marker: str = "o", ms: float = 8) -> None:
    """A dot (or another marker) with its 95% interval, horizontal; nothing for a missing point."""
    if v is None:
        return
    ax.plot([v[1], v[2]], [y, y], color=color, lw=1.6, zorder=2, solid_capstyle="butt")
    ax.plot([v[0]], [y], marker, ms=ms, color=color, zorder=3)


def reading(ax, y: float, head: str, lines: list[str]) -> None:
    """A text-column cell: the reading in bold, the numbers behind it muted below, the block centred on the row."""
    if not lines:
        ax.text(0.04, y, head, va="center", weight="bold")
        return
    top = y + 0.15 + 0.11 * len(lines)  # the head about 0.3 row units, each muted line about 0.22
    ax.text(0.04, top, head, va="top", weight="bold")
    ax.text(0.04, top - 0.30, "\n".join(lines), va="top", color=S.COL["muted"], linespacing=1.1)


def pct(v: float) -> str:
    return f"{100 * v:.0f}"


# ---- 47.14: chained addresses ---------------------------------------------------------------------------------------


def chain_title(v: dict) -> str:
    tested = [m for m in v["models"] if m["status"] == "tested"]
    if not tested:
        return "Chained addresses: no model tested yet"
    n = len(tested)
    if all(m["holds"] for m in tested):
        return "Addresses chain: the hall's address at the locker digit carries position answers"
    k_probe = sum(m["clauses"]["probe"] and m["clauses"]["layout"] for m in tested)
    k_cut = sum(m["clauses"]["U_cut"] for m in tested)
    probe = ("The hall is readable at the locker digit" if k_probe == n else
             "The hall is not readable at the locker digit" if k_probe == 0 else
             f"The hall is readable at the locker digit on {k_probe} of {n}")  # fmt: skip
    cut = ("yet a random part cuts nearly as much" if k_cut == 0 else "and its address carries position" if k_cut == n
           else f"its address beats random on {k_cut} of {n}")  # fmt: skip
    return f"{probe}, {cut}" if k_cut in (0, n) else f"{probe}; {cut}"


LT_CHAIN = S.REPO / "results" / "x47_chain" / "x52_chain-20261029T023424Z" / "x47_14.json"  # the 27B; Lightning (gate)


def build_chain(verdict_dir: Path, out_name: str, title: str | None = None, coverage: Path | None = LT_CHAIN) -> str:
    """47.14 (x47_chain verdict, x47_14.json): one row per model (9B, Muse; with `coverage`, batch 52's folder by
    explicit path: the 27B, and Lightning's slot, whose gate missed, so it keeps a grey row). The three-step question (which hall is
    the locker of the pick in?), the change at the digit of the bridge's locker sentence: (a) hall answers by position
    (%) under the whole change, without the hall address (U_num) and without a random part (same size); (b) with only
    the hall address or only the random part kept (the rule's bar at 15); (c) the reading: the hall probe beside its
    layout baseline, the cut beyond random against its bar (30) and only-the-address against 15."""
    src = verdict_dir / "x47_14.json"
    v = json.loads(src.read_text())
    by, fid = by_target(v["models"]), fig_id(out_name)
    srcs = dict.fromkeys(by, F.rel(src))
    if coverage is not None:  # a model the first verdict did not test, from its coverage run
        for m in json.loads(coverage.read_text())["models"]:
            if by.get(m["target"], {}).get("status") != "tested":
                by[m["target"]], srcs[m["target"]] = m, F.rel(coverage)
        v = {**v, "models": list(by.values())}
    rows_m = shown(list(by.values())) + ([(F.LT[0], F.LT[1])] if F.LT[0] in by else [])
    if coverage is not None and A.SLOT_122B[0] not in by:  # the fifth slot: 47.14 never ran on the 122B, a grey row
        by[A.SLOT_122B[0]], srcs[A.SLOT_122B[0]] = {"status": "not run"}, ""
        rows_m.append(A.SLOT_122B)
    pos = S.COL["position"]
    legend = ([handle(S.COL["recall"]), handle(pos), handle(GREY)],
              ["the whole change", "the hall address", "random part (same size)"])  # fmt: skip
    fig, (a, b, c) = frame(
        title or chain_title(v),
        "Which hall is the pick's locker in? The change at the bridge's locker digit, parts taken out or kept: hall "
        "answers by position (%), 95% intervals, fixed in advance.",
        (1, 0.8, 1.0), ROW_IN * len(rows_m), legend=legend,
        **({"left": 0.235, "bottom_in": A.BOTTOM_IN + 0.5} if coverage is not None else {}))  # fmt: skip
    A.row_panels((a, b, c), len(rows_m))
    A.pct_axis(a, "hall answers\nby position (%)", lim=(-4, 106))
    panel_title(a, "(a) taken out")
    A.pct_axis(b, "hall answers\nby position (%)", lim=(-4, 106))
    panel_title(b, "(b) only this kept")
    bar(b, 15, "≥ 15")
    A.text_column(c, "reading")
    labels = []
    for i, (target, m) in enumerate(rows_m):
        y, mod, source = -i, by[target], srcs[target]
        if mod["status"] == "not run":  # a grey slot: its label only, nothing recorded
            labels.append((m, ""))
            reading(c, y, "not run", [])
            for ax in (a, b):
                A.status_text(ax, y, "not run")
            continue
        if mod["status"] != "tested":
            labels.append((m, ""))
            S.record(fid, target, "47.14: status", mod["status"], source=source)
            gate = mod.get("gate") or {}
            low = min((gate.get("org_read_accuracy") or {}).values(), default=None)
            text = f"not tested: gate {low:.2f}" if mod["status"] == "not tested" and low is not None else mod["status"]
            if low is not None:
                S.record(fid, target, "47.14: the gate's lowest read accuracy on the original prompts", low,
                         source=source)  # fmt: skip
            reading(c, y, text, [])
            for ax in (a, b):
                A.status_text(ax, y, text)
            continue
        h, p = mod["hall"], mod["probe"]
        labels.append((m, f"n = {h['n']}"))
        for ax, arm, dy, col, what in ((a, "whole", 0.25, S.COL["recall"], "the whole change"),
                                       (a, "no_U", 0.0, pos, "without the hall address"),
                                       (a, "no_U_rand", -0.25, GREY, "without a random part (same size)"),
                                       (b, "keep_U", 0.13, pos, "only the hall address kept"),
                                       (b, "keep_U_rand", -0.13, GREY, "only a random part (same size) kept")):  # fmt: skip
            cell = h["routes"][arm]["position"]
            mark(ax, y + dy, iv(cell, 100), col)
            S.record(fid, target, f"47.14: hall answers by position, {what}", *cell, n=h["n"], source=source)
        cut = h["U_cut_beyond_random"]
        S.record(fid, target, "47.14: hall position answers cut beyond random (without the random part minus without "
                 "the hall address)", *cut, n=h["n"], source=source)  # fmt: skip
        S.record(fid, target, "47.14: hall probe at the locker digit", *p["probe"], n=p["n"], source=source)
        S.record(fid, target, "47.14: hall probe's layout baseline", *p["layout"], n=p["n"], source=source)
        S.record(fid, target, "47.14: the rule's reading", "holds" if mod["holds"] else "does not hold", source=source)
        reading(c, y, "holds" if mod["holds"] else "does not hold",
                [f"hall probe {pct(p['probe'][0])} (layout {pct(p['layout'][0])})",
                 f"cut beyond random {pct(cut[0])} (≥ 30)", f"only address {pct(h['keep_U_position'][0])} (≥ 15)"])  # fmt: skip
    A.model_labels(a, labels)
    if coverage is not None:  # Dan's figures brief (29 Oct 10:00): each model's status in one line
        status = "; ".join(f"{SHORT.get(t, 'Lightning')}: " + ("tested, fixed in advance" if by[t]["status"] == "tested"
                           else by[t]["status"] if by[t]["status"] == "not run" else "not tested (gate)")
                           for t, _ in rows_m)  # fmt: skip
        fig.text(0.01, 0.012, textwrap.fill(status + ".", 118), fontsize=S.FONT - 1, color=S.COL["muted"], va="bottom")
    S.save(fig, out_name)
    return out_name


# ---- 47.11: the item-agnostic pointer -------------------------------------------------------------------------------

TYPES = (("animals", "o", GREY, "animals (fit on them)"), ("fruits", "s", S.COL["position"], "fruits"),
         ("names", "D", S.COL["position"], "names"))  # fmt: skip
AGNOSTIC_LABEL = {"an address (U transfers)": "transfers", "U does not transfer": "does not transfer",
                  "slot x type (the refit passes)": "per-type code", "not tested": "not tested",
                  "neither U nor the refit (U' fails too)": "refit fails too"}  # fmt: skip


def agnostic_title(v: dict) -> str:
    tested = [m for m in v["models"] if m["status"] == "tested" and m["answer"] in ("yes", "no")]
    if not tested:
        return "The pointer on fruits and names: no model tested yet"
    k = sum(m["answer"] == "yes" for m in tested)
    if k == len(tested):
        return "The pointer is item-agnostic: fit on animals, it moves fruits and names too"
    if k == 0:
        return "The pointer fit on animals does not transfer to fruits and names"
    return f"The pointer fit on animals transfers to fruits and names on {k} of {len(tested)} models"


def build_agnostic(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """47.11 (x47_agnostic verdict, x47_11.json): one row per model (9B, Muse); per item type (animals, the reference;
    fruits; names) (a) lookup position answers lost without the pointer (fit on animals, not refit) beyond a random
    part (same size), bar 30; (b) position answers with only the pointer kept, bar 15; (c) the reading per new type
    (when the fixed pointer fails, its refit per type: 'a code per item type' if the refit passes)."""
    src = verdict_dir / "x47_11.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    rows_m = shown(v["models"])
    legend = ([handle(col, mk, 8 if mk != "D" else 7) for _, mk, col, _ in TYPES], [lab for *_, lab in TYPES])
    fig, (a, b, c) = frame(
        title or agnostic_title(v),
        "Routes test with animals, fruits or names as the items; the pointer fit on animals, never refit. Lookup "
        "answers by position (%), 95% intervals, fixed in advance.",
        (1, 1, 0.85), ROW_IN * len(rows_m), legend=legend)  # fmt: skip
    A.row_panels((a, b, c), len(rows_m))
    A.pct_axis(a, "position answers lost\nbeyond random (%)", lim=(-20, 106))
    panel_title(a, "(a) without the pointer")
    bar(a, 30, "≥ 30")
    A.pct_axis(b, "position answers (%)", lim=(-4, 106))
    panel_title(b, "(b) only the pointer")
    bar(b, 15, "≥ 15")
    A.text_column(c, "reading")
    labels = []
    for i, (target, m) in enumerate(rows_m):
        y, mod = -i, by[target]
        S.record(fid, target, "47.11: the rule's answer", mod["answer"], source=source)
        if mod["status"] != "tested":
            labels.append((m, ""))
            reading(c, y, mod["status"], [])
            for ax in (a, b):
                A.status_text(ax, y, mod["status"])
            continue
        nums = mod["numbers"]
        labels.append((m, f"n = {nums['animals']['fixed']['n']}" if nums.get("animals") else ""))
        for (kind, mk, col, _), dy in zip(TYPES, (0.25, 0.0, -0.25), strict=True):
            f = (nums.get(kind) or {}).get("fixed") or {}
            if not f.get("n"):
                continue
            ms = 8 if mk != "D" else 7
            mark(a, y + dy, iv(f["position_fall"], 100), col, mk, ms)
            mark(b, y + dy, iv(f["keep_position"], 100), col, mk, ms)
            S.record(fid, target, f"47.11: {kind}: position answers lost without the pointer beyond random",
                     *f["position_fall"], n=f["n"], source=source)  # fmt: skip
            S.record(fid, target, f"47.11: {kind}: position answers, only the pointer kept", *f["keep_position"],
                     n=f["n"], source=source)  # fmt: skip
        head = {"yes": "item-agnostic", "no": "not item-agnostic"}.get(mod["answer"], str(mod["answer"]))
        lines = []
        for kind, lab in mod["labels"].items():
            lines.append(f"{kind}: {AGNOSTIC_LABEL.get(lab['label'], lab['label'])}")
            S.record(fid, target, f"47.11: {kind}: the rule's reading", lab["label"], source=source)
        reading(c, y, head, lines)
    A.model_labels(a, labels)
    S.save(fig, out_name)
    return out_name


# ---- 47.12: two definitions of the lens part ------------------------------------------------------------------------

DEFS = (("omp25", "(i)"), ("top10", "(ii)"))
AGREE = 0.15  # the rule: the gap under (ii) within 0.15 of (i)


def twodefs_title(v: dict) -> str:
    tested = [m for m in v["models"] if m.get("answer") in ("yes", "no")]
    if not tested:
        return "Two definitions of the J++ part: no model tested yet"
    k = sum(m["answer"] == "yes" for m in tested)
    if k == len(tested):
        return "Two definitions of the J++ part agree on the recall–lookup gap"
    if k == 0:
        return "Two definitions of the J++ part give different recall–lookup gaps"
    return f"Two definitions of the J++ part agree on the recall–lookup gap on {k} of {len(tested)} models"


def build_twodefs(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """47.12 (x47_twodefs verdict, x47_12.json): one row per model (9B, Muse). Main test, at the bridge word at L:
    the recall's and the lookup's extra loss without the part defined (a) as ours (25 signed-OMP lens directions fit to
    the change) and (b) as the 10 lens directions with the highest logits; (c) the gap (recall minus lookup) under
    each, the band (i) +- 0.15 the rule's 'agree'."""
    src = verdict_dir / "x47_12.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    rows_m = shown(v["models"])
    gap_col = S.COL["muted"]  # not a reader: grey, its own markers
    hs, ls = F.reader_handles(S.setup())
    legend = ([*hs, handle(gap_col, "D", 6.5), handle(gap_col, "s", 7)], [*ls, "gap (i)", "gap (ii)"])
    fig, (a, b, c) = frame(
        title or twodefs_title(v),
        "Main test. (i) the J++ part, 25 lens directions fit to the change; (ii) the 10 with the top lens logits. "
        "Extra loss, 95% intervals, fixed in advance; shaded: (i)'s gap ± 0.15.",
        (1, 1, 1), 0.85 * len(rows_m), legend=legend)  # fmt: skip
    A.row_panels((a, b, c), len(rows_m))
    for ax, name in ((a, "(a) (i) the J++ part"), (b, "(b) (ii) top 10 by logit")):
        S.extra_axis(ax, label=False)
        ax.set_xlabel("extra loss")
        panel_title(ax, name)
    c.set_xlim(-0.4, 1.0)
    c.axvline(0, color="#999999", lw=0.8, zorder=1)
    c.set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
    c.grid(axis="x", color="#eeeeee")
    c.set_xlabel("gap (recall − lookup)")
    panel_title(c, "(c) the gap")
    labels = []
    for i, (target, m) in enumerate(rows_m):
        y, mod = -i, by[target]
        S.record(fid, target, "47.12: the rule's answer", mod.get("answer", mod["status"]), source=source)
        if mod["status"] != "tested":
            labels.append((m, ""))
            for ax in (a, b, c):
                A.status_text(ax, y, mod["status"])
            continue
        d = mod["definitions"]
        n = d["omp25"]["recall"]["n"]
        head = {"yes": "agree", "no": "differ", "can't tell": "can't tell"}.get(mod["answer"], mod["answer"])
        labels.append((m, f"n = {n}, {head}"))
        for ax, (key, tag) in zip((a, b), DEFS, strict=True):
            for w, dy in (("recall", 0.16), ("lookup", -0.16)):
                cell = d[key][w]["excess"]
                p = iv(cell)
                if p is not None:
                    S.dot(ax, 0, y + dy, p, S.COL[w], size=8)
                    S.record(fid, target, f"47.12: {w}'s extra loss, {tag} {key}", *cell, n=d[key][w]["n"],
                             source=source)  # fmt: skip
        g1 = iv(d["omp25"]["gap"])
        if g1 is not None:
            c.fill_between([g1[0] - AGREE, g1[0] + AGREE], y - 0.36, y + 0.36, color=S.COL["shade"], lw=0, zorder=0.5)
        for (key, tag), dy, mk in zip(DEFS, (0.14, -0.14), ("D", "s"), strict=True):
            g = iv(d[key]["gap"])
            if g is None:
                continue
            mark(c, y + dy, g, gap_col, mk, 7 if mk == "D" else 7.5)
            S.record(fid, target, f"47.12: gap (recall's extra loss minus the lookup's), {tag} {key}", *d[key]["gap"],
                     n=n, source=source)  # fmt: skip
    A.model_labels(a, labels)
    S.save(fig, out_name)
    return out_name


# ---- 47.15: one question, two sources -------------------------------------------------------------------------------

SOURCE_LABEL = {"lookup": "like a lookup", "recall": "like a recall", "neither": "neither",
                "can't tell": "can't tell"}  # fmt: skip


def source_title(v: dict) -> str:
    label = v["batch"]["label"]
    if label == "follows the source":
        return "The part the answer needs follows its source, not the question"
    if label == "follows the question":
        return "The part the answer needs follows the question, not its source"
    tested = [m for m in v["models"] if m["status"] == "tested"]
    if not tested:
        return "One question, two sources: no model tested yet"
    k = sum(m["verdict"] == "follows the source" for m in tested)
    return f"One question, two sources: the part follows the source on {k} of {len(tested)} models"


def build_source(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """47.15 (x47_source verdict, x47_15.json): one row per model (27B, 9B, Muse), the decisive placement (the
    attribute sentences after the picks). The legs question asked from the text (the passage's false count) or from
    memory: extra loss without (a) the J++ part, (b) the pointer + identity outside J++, the rule's bars at 0.10 and
    0.30; (c) each condition's reading (like a lookup / like a recall) and the model's verdict."""
    src = verdict_dir / "x47_15.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    rows_m = shown(v["models"])
    conds = (("text", "from the text", S.COL["lookup"], 0.16), ("memory", "from memory", S.COL["recall"], -0.16))
    legend = ([handle(col) for _, _, col, _ in conds], [lab for _, lab, _, _ in conds])
    fig, (a, b, c) = frame(
        title or source_title(v),
        "“How many legs?” over a passage with false counts, answered from the text or from memory. Extra loss "
        "at the bridge word; (b): the pointer + identity outside J++. 95% intervals.",
        (1, 1, 0.8), ROW_IN * len(rows_m), legend=legend)  # fmt: skip
    A.row_panels((a, b, c), len(rows_m))
    for ax, part, name in ((a, "jpp", "(a) the J++ part"), (b, "ui", "(b) pointer + identity")):
        S.extra_axis(ax, label=False)
        ax.set_xlabel("extra loss without " + ("it" if part == "jpp" else "them"))
        panel_title(ax, name)
        bar(ax, 0.10, "≤ 0.10", side="left")
        bar(ax, 0.30, "≥ 0.30")
    A.text_column(c, "reading")
    labels = []
    for i, (target, m) in enumerate(rows_m):
        y, mod = -i, by[target]
        if mod["status"] != "tested":
            labels.append((m, ""))
            S.record(fid, target, "47.15: status", mod["status"], source=source)
            reading(c, y, mod["status"], [])
            for ax in (a, b):
                A.status_text(ax, y, mod["status"])
            continue
        cells = mod["placements"]["after"]["conditions"]
        labels.append((m, f"n = {cells['text']['n']}"))
        lines = []
        for cond, lab, col, dy in conds:
            cell = cells[cond]
            lines.append(f"{lab.split()[-1]}: {SOURCE_LABEL.get(cell['label'], cell['label'])}")
            S.record(fid, target, f"47.15: {lab}: the rule's reading", cell["label"], source=source)
            for ax, part, what in ((a, "jpp", "the J++ part"), (b, "ui", "the pointer + identity outside J++")):
                p = iv(cell["extra"].get(part))
                if p is None:
                    continue
                S.dot(ax, 0, y + dy, p, col, size=8)
                S.record(fid, target, f"47.15: {lab}: extra loss without {what}", *cell["extra"][part], n=cell["n"],
                         source=source)  # fmt: skip
        reading(c, y, mod["verdict"], lines)
        S.record(fid, target, "47.15: the model's verdict", mod["verdict"], source=source)
    A.model_labels(a, labels)
    S.save(fig, out_name)
    return out_name


# ---- 47.16: distance ------------------------------------------------------------------------------------------------

KS = (0, 5, 20, 50)
DIST_LABEL = {"distance-robust address": "robust", "address near, identity far": "near, identity far",
              "none of the three": "none of the three"}  # fmt: skip
DIST_SERIES = (("position", "position answers", S.COL["position"], "o"),
               ("identity", "identity answers", S.COL["identity"], "o"),
               ("probe", "probe", S.COL["recall"], "s"),
               ("swap", "pointer swap", S.COL["lookup"], "D"))  # fmt: skip


def dist_reading(label: str) -> str:
    if label.startswith("breaks at k = "):
        return f"breaks at {label.removeprefix('breaks at k = ')} fillers"
    return DIST_LABEL.get(label, label)


def distance_title(v: dict) -> str:
    tested = [m for m in v["models"] if m["status"] in ("tested", "not tested")]
    if not tested:
        return "Filler sentences before the picks: no model tested yet"
    labels = {m["label"] for m in tested}
    if labels == {"distance-robust address"}:
        return f"The pointer's address survives 50 filler sentences on {names([m['target'] for m in tested])}"
    parts = [f"{SHORT[m['target']]} {dist_reading(m['label'])}" for m in sorted(tested, key=_order)]
    return "Filler sentences before the picks: " + "; ".join(parts)


def _order(m: dict) -> int:
    return [t for t, _, _ in S.MODELS].index(m["target"])


def build_distance(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """47.16 (x47_distance verdict, x47_16.json): one panel per model (9B, Muse); against the filler sentences
    between the locker sentences and the picks (0, 5, 20, 50): lookup answers by position and by identity under the
    whole change, the probe finding the bridge's locker sentence and the pointer swap reaching its locker (%), 95%
    intervals; a k whose gate failed (or was not run) is marked; under each panel the rule's reading."""
    src = verdict_dir / "x47_16.json"
    v = json.loads(src.read_text())
    by, fid, source = by_target(v["models"]), fig_id(out_name), F.rel(src)
    rows_m = shown(v["models"])
    legend = ([Line2D([], [], marker=mk, color=col, ms=7 if mk != "D" else 6, lw=1.4) for _, _, col, mk in DIST_SERIES],
              [lab for _, lab, _, _ in DIST_SERIES], 4)  # fmt: skip
    fig, axes = frame(
        title or distance_title(v),
        "Routes test, filler sentences between the locker sentences and the picks: lookup answers under the whole "
        "change, the probe, the pointer swap (%). 95% intervals.",
        tuple(1.0 for _ in rows_m), 2.3, legend=legend, left=0.12, bottom_in=1.0)  # fmt: skip
    for ax, (target, m) in zip(axes, rows_m, strict=True):
        mod = by[target]
        ax.set_title(F.name_of(m), fontsize=S.FONT, weight="bold")
        ax.set_ylim(-4, 104)
        ax.set_yticks(*F.PCT)
        ax.grid(axis="y", color="#eeeeee")
        ax.set_xlim(-0.4, len(KS) - 0.6)
        ax.set_xticks(range(len(KS)), [str(k) for k in KS])
        ax.set_xlabel("filler sentences")
        S.record(fid, target, "47.16: the rule's reading", mod.get("label", mod["status"]), source=source)
        if mod["status"] == "pending":
            S.empty(ax, "pending")
            continue
        cells, probes = mod.get("cells") or {}, mod.get("probes") or {}
        for (key, lab, col, mk), dx in zip(DIST_SERIES, (-0.12, -0.04, 0.04, 0.12), strict=True):
            xs, ys = [], []
            for j, k in enumerate(KS):
                cell, probe = cells.get(str(k)), probes.get(str(k))
                if cell is None or probe is None:
                    continue
                val = {"position": cell["routes"]["whole"]["position"], "identity": cell["routes"]["whole"]["identity"],
                       "probe": probe["probe"], "swap": cell["swap"]["write"]}[key]  # fmt: skip
                r = iv(val, 100)
                if r is None:
                    continue
                ax.plot([j + dx] * 2, [r[1], r[2]], color=col, lw=1.4, zorder=2)
                xs.append(j + dx)
                ys.append(r[0])
                n = cell["swap"]["n"] if key == "swap" else probe["n"] if key == "probe" else cell["n"]
                S.record(fid, target, f"47.16: {lab} at {k} filler sentences", *val, n=n, source=source)
            ax.plot(xs, ys, marker=mk, ms=7 if mk != "D" else 6, color=col, lw=1.4, zorder=3)
        for j, k in enumerate(KS):
            if str(k) not in cells:
                failed = mod.get("stopped_at") == k
                ax.text(j, 50, "gate\nfailed" if failed else "not run", ha="center", va="center", color=S.COL["muted"])
        ax.text(0.0, -0.27, dist_reading(mod.get("label", mod["status"])), transform=ax.transAxes, ha="left", va="top",
                weight="bold")  # fmt: skip
    axes[0].set_ylabel("lookup answers, probe (%)")
    S.save(fig, out_name)
    return out_name


# ---- D4: the address across depth -----------------------------------------------------------------------------------

DEPTH_LABEL = {"persistent": "one code", "re-encoded": "re-encoded", "mixed": "mixed", "not tested": "not tested"}
PERSIST_BAR, REENCODE_BAR = 0.5, 0.2


def depth_title(v: dict) -> str:
    us = {t: r["U"]["label"] for t, r in v["models"].items()}
    order = [t for t, _, _ in S.MODELS if t in us]
    if not order:
        return "The address across depth: no model read yet"
    if all(us[t] == "re-encoded" for t in order):
        return f"The address is re-encoded across depth on {names(order)}, not one code"
    if all(us[t] == "persistent" for t in order):
        return f"The address is one code across depth on {names(order)}"
    return "The address across depth: " + ", ".join(f"{DEPTH_LABEL[us[t]]} on {names([t])}" for t in order)


def build_depth(verdict_dir: Path, out_name: str, title: str | None = None) -> str:
    """D4 (x47_depth_cpu persistence stage, persistence.json): one panel per model (9B, Muse). The address (the
    locker sentence's mass-mean basis U_l, refit at each sampled layer) and its overlap with the next sampled layer's
    (mean cos^2 of the principal angles), the probe's window shaded, the mean over every pair of window layers as a
    line across the window; the rule's bars: one code if that mean >= 0.5, re-encoded if one adjacent step < 0.2."""
    src = verdict_dir / "persistence.json"
    v = json.loads(src.read_text())
    fid, source = fig_id(out_name), F.rel(src)
    rows_m = [(t, m) for t, m, _ in S.MODELS if t in v["models"]]
    pos = S.COL["position"]
    legend = ([Line2D([], [], marker="o", color=pos, ms=6, lw=1.4), Line2D([], [], color=S.COL["recall"], lw=2.2)],
              ["next sampled layer", "mean over all window pairs"])  # fmt: skip
    fig, axes = frame(
        title or depth_title(v),
        "The address refit at each sampled layer: its overlap (mean cos², 0–1) with the next layer's. Shaded: "
        "where the probe finds the bridge's locker sentence (≥ 80%).",
        tuple(1.0 for _ in rows_m), 2.3, legend=legend, left=0.11, bottom_in=1.05)  # fmt: skip
    for ax, (target, m) in zip(axes, rows_m, strict=True):
        r = v["models"][target]
        u, layers = r["U"], [int(x) for x in r["layers"]]
        ax.set_title(F.name_of(m), fontsize=S.FONT, weight="bold")
        ax.set_ylim(0, 1.04)
        ax.set_yticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        ax.set_xlim(layers[0] - 1, layers[-1] + 1)
        ax.set_xticks([t for t in range(0, layers[-1] + 1, 10) if t >= layers[0] - 1])
        ax.set_xlabel("layer")
        win = [int(x) for x in u["window"]]
        if win:
            ax.axvspan(win[0], win[-1], color=S.COL["band"], lw=0, zorder=0)
        mat = u["matrix"]
        xs, ys = [], []
        for (i, la), (j, lb) in itertools.pairwise(enumerate(layers)):
            xs.append((la + lb) / 2)
            ys.append(mat[i][j])
            S.record(fid, target, f"D4: the address's overlap (mean cos^2), layers {la}-{lb}", float(mat[i][j]),
                     source=source)  # fmt: skip
        ax.plot(xs, ys, marker="o", ms=6, color=pos, lw=1.4, zorder=3)
        # the bars' labels at the right end, the persistent bar's above its line and the re-encoded bar's below
        tr = blended_transform_factory(ax.transAxes, ax.transData)
        for y, text, dy, va in ((PERSIST_BAR, "one code ≥ 0.5", 0.015, "bottom"),
                                (REENCODE_BAR, "re-encoded < 0.2", -0.015, "top")):  # fmt: skip
            ax.axhline(y, color=A.BAR, lw=1.1, ls=(0, (4, 3)), zorder=1.8)
            ax.text(0.99, y + dy, text, transform=tr, ha="right", va=va, color=A.BAR)
        mean = u.get("mean_cos2")
        if mean is not None and win:
            ax.plot([win[0], win[-1]], [mean] * 2, color=S.COL["recall"], lw=2.2, zorder=2.5)
            S.record(fid, target, "D4: the address's mean overlap over every pair of window layers", mean,
                     n=len(win), source=source)  # fmt: skip
        S.record(fid, target, "D4: the rule's reading (the address)", u["label"], source=source)
        drops = ", ".join(d.replace("-", "–") for d in u.get("drops") or [])
        ax.text(0.0, -0.25, DEPTH_LABEL.get(u["label"], u["label"]), transform=ax.transAxes, ha="left", va="top",
                weight="bold")  # fmt: skip
        detail = ([f"mean {mean:.2f}"] if mean is not None else []) + ([f"step < 0.2 at {drops}"] if drops else [])
        ax.text(0.0, -0.36, "; ".join(detail), transform=ax.transAxes, ha="left", va="top", color=S.COL["muted"])
    axes[0].set_ylabel("overlap (cos²)")
    S.save(fig, out_name)
    return out_name


TESTS = {
    "47.14": ("scripts/x47_chain.py", build_chain, "fig21_chained_addresses"),
    "47.11": ("scripts/x47_agnostic.py", build_agnostic, "fig22_item_agnostic"),
    "47.12": ("scripts/x47_twodefs.py", build_twodefs, "fig23_two_definitions"),
    "47.15": ("scripts/x47_source.py", build_source, "fig24_two_sources"),
    "47.16": ("scripts/x47_distance.py", build_distance, "fig25_distance"),
    "D4": ("scripts/x47_depth_cpu.py", build_depth, "fig26_address_depth"),
}
