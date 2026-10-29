"""README figures from Dan's figures brief (28 Oct ~18:30), steps 3-4, in the mark system of scripts/story_b50.py.

  fig07b_verbal      E8: the address swap through the lens (47.0, x47_verbal summary and run folders) against the 200
                     random draws, the identity change as the positive control; a before/after arrow plot, two panels
                     (rank, share rebuilt) both in units of the random band, one row per model (Dan's Fig. 7b briefs,
                     28 Oct ~21:00 and 21:10)
  fig09a_transfer    the split carries over: lookup's and recall's extra loss without the J++ part by text format
  fig09b_refit       Part IV: the address fit on simple scenes vs refit per format (45d verdicts)

Every plotted number is recorded for figures/story/data.csv with its source file; the random draws' 95% range is
recomputed from the run folders' per-draw files (null.npz, omp.jsonl) exactly as scripts/x47_verbal.py summarizes them,
and their median / mean is checked against the summary before anything is drawn.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import readme_story_figures as F
from scripts import story_style as S
from scripts.story_b50 import B122, B122_NOTE, INK, LOOKUP, MODELS, NULL, SHORT, caption, rel

ADDRESS, IDENTITY = S.MARK_COL["address"], S.MARK_COL["identity"]
K = 25  # lens directions in the share rebuilt (47.0 (b), the README's number)


def n_tag(ax, text: str) -> None:
    ax.text(1.0, 1.015, text, transform=ax.transAxes, ha="right", va="bottom", fontsize=S.FONT - 1,
            color=S.COL["muted"], zorder=8)  # fmt: skip


# Fig. 7b's strip: the random grey at 75% on white, opaque
BAND_GREY = tuple(0.75 * c + 0.25 for c in to_rgb(NULL))


# ---- fig07b: the lens is blind to the address ----------------------------------------------------------------------


def verbal_nulls(run_dir: Path) -> dict:
    """From one 47.0 run folder: the 200 random draws' medians over the cases of (i) the best ordinal word's rank and
    (ii) the new item's name rank on the identity cases (as scripts/x47_verbal.against_null), and (iii) the share 25
    lens directions rebuild of each random draw (dictionary 'all'), each as the draws' array."""
    nz = np.load(run_dir / "null.npz")
    keys = list(zip(nz["scene"].tolist(), nz["k"].tolist(), strict=True))
    has = {(r["scene"], r["k"]) for r in map(json.loads, (run_dir / "readouts.jsonl").read_text().splitlines())
           if r["arm"] == "identity"}  # fmt: skip
    idx = [i for i, key in enumerate(keys) if key in has]
    omp = [json.loads(line) for line in (run_dir / "omp.jsonl").read_text().splitlines()]
    return {"ordinal": np.median(nz["best_ordinal"], axis=1), "name": np.median(nz["alt_name"][:, idx], axis=1),
            "share": np.array([r["share"] for r in omp if r["kind"] == "random" and r["dict"] == "all" and r["k"] == K])}  # fmt: skip


def rank_score(median: float, null: np.ndarray) -> dict:
    """The rank panel's score (Dan's Fig. 7b brief, 28 Oct ~21:00): z = (ln m - ln r) / w, with r the change's median
    rank over the cases, m the median of the random draws' median ranks and w the half-width of the draws' band: half
    the 95% range of ln rank over the draws, (ln p97.5 - ln p2.5) / 2, p2.5 and p97.5 the draws' 2.5th and 97.5th
    percentiles of rank (the band recorded on the rank scale; ln of the percentiles, so the drawn band is exactly that
    one). Positive = the lens ranks the word above the random vectors; the log base cancels. The band maps to
    [(ln m - ln p97.5) / w, (ln m - ln p2.5) / w]: 2 wide by construction, centred on 0 up to the draws' asymmetry
    about their median."""
    m = float(np.median(null))
    lo, hi = (float(x) for x in np.percentile(null, [2.5, 97.5]))
    w = (np.log(hi) - np.log(lo)) / 2
    return {"z": float((np.log(m) - np.log(median)) / w), "w": float(w),
            "band": (float((np.log(m) - np.log(hi)) / w), float((np.log(m) - np.log(lo)) / w))}  # fmt: skip


def share_score(share: float, null: np.ndarray) -> dict:
    """The share panel's score (Dan's round 3, 28 Oct 21:10): z = (share - m) / w, with m the median of the random
    draws' shares and w half their 95% range, (p97.5 - p2.5) / 2. The band maps to [(p2.5 - m) / w, (p97.5 - m) / w]:
    2 wide by construction, centred on 0 up to the draws' asymmetry about their median."""
    m = float(np.median(null))
    lo, hi = (float(x) for x in np.percentile(null, [2.5, 97.5]))
    w = (hi - lo) / 2
    return {"z": float((share - m) / w), "w": w, "m": m, "band": ((lo - m) / w, (hi - m) / w)}


def arrow(ax, y: float, z: float, col: str, hollow: bool = False) -> None:
    """One change as an arrow from 0 (what a random vector of the same size does) to its score z, the tip at z; an
    arrow too short for a shaft is its head alone, centred on z. hollow (Lightning, after the data): a dashed shaft and
    an open head."""
    if abs(z) >= 0.6:
        props = {"arrowstyle": "-|>,head_length=0.7,head_width=0.35", "color": col, "lw": 2.4, "shrinkA": 0,
                 "shrinkB": 0}  # fmt: skip
        if hollow:
            props |= {"facecolor": "white", "linestyle": (0, (3, 1.5)), "lw": 1.8}
        ax.annotate("", xy=(z, y), xytext=(0, y), zorder=3, arrowprops=props)
    else:
        ax.plot([z], [y], ">" if z >= 0 else "<", ms=9, color=col, mfc="white" if hollow else col, mew=1.5, zorder=4)


ARROW_DY = 0.13  # the swap's arrow above the row's centre, the item change's below
BAND_EDGE = 0.25  # a row's own 95% range may sit at most this far off the drawn strip's +-1 (checked)


def own_band(ax, y: float, band: tuple[float, float], target: str, key: str, own: list) -> None:
    """The strip's check: a row's own 95% range within BAND_EDGE of +-1 (asserted on the 9B, 27B and Muse). Lightning's,
    where it misses, is drawn on its arrow's line as a thin hatched band of its own and listed in `own`."""
    if all(abs(e - s) <= BAND_EDGE for e, s in zip(band, (-1, 1), strict=True)):
        return
    assert target == F.LT[0], (target, key, band)
    ax.fill_between([band[0], band[1]], y - 0.055, y + 0.055, facecolor="none", edgecolor="#9a9a9a", hatch="////",
                    lw=0.6, zorder=2)  # fmt: skip
    own.append(key)


LT_VERBAL = S.REPO / "results" / "x47_verbal" / "summary-20261029T005548Z"  # Lightning's 47.0 (batch 52 coverage)


def build_verbal(verbal_dir: Path, report_dir: Path, out_name: str = "fig07b_verbal",
                 lightning: Path | None = LT_VERBAL) -> str:  # fmt: skip
    """Fig. 7b (E8), Dan's round 3 (28 Oct 21:10): a before/after arrow plot, two panels, one row per model (9B, 27B,
    Muse, and Lightning from its own summary folder `lightning`, hollow: its gate was chosen after its pre-check was
    seen) holding both changes as arrows from 0 in z units: the address swap (orange) and, as the positive control, an
    identity change (blue). One grey strip from -1 to +1 on each panel: the 95% range of the random vectors of the same
    norm (each row's own range is within BAND_EDGE of it, checked; z is centred on the random median). (1) Rank through
    the lens (47.0 (a), descriptive; rank_score): the swap's best-ranked position word (any of x47_verbal.ORDINAL), the
    identity change's new item's name, each against the same 200 random vectors scored on its own word. (2) Share
    rebuilt by 25 lens directions (47.0 (b); share_score); one set of random draws per model serves both changes. The
    27B's report (47.10) is recorded (e8_report) and said in one caption sentence."""
    vpath, rpath = verbal_dir / "verbal.json", report_dir / "x47_10.json"
    vblob, rblob = json.loads(vpath.read_text()), json.loads(rpath.read_text())
    vsrc, rsrc = rel(vpath), rel(rpath)
    models = dict(vblob["models"])
    srcs = dict.fromkeys(models, vsrc)
    if lightning is not None:
        lpath = lightning / "verbal.json"
        models[F.LT[0]] = json.loads(lpath.read_text())["models"][F.LT[0]]
        srcs[F.LT[0]] = rel(lpath)
    plt = S.setup()
    rows = [(t, m) for t, m, _ in (*MODELS, F.LT) if t in models]
    row_in, top_in, bottom_in = 0.85, 1.75, 0.95 + 0.75 * (lightning is not None)
    h = top_in + row_in * len(rows) + bottom_in
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, h), sharey=True, sharex=True)
    left = 0.235 if lightning is not None else 0.19  # "Nemotron 3.5 Lightning" is the longest row name
    fig.subplots_adjust(left=left, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.08)
    ys = {t: -i for i, (t, _) in enumerate(rows)}
    a, b = axes
    n_rand, words, label_9b, raw, own = set(), set(), {}, {}, []
    for t, _m in rows:
        r, y = models[t], ys[t]
        hollow, vs = t == F.LT[0], srcs[t]
        nulls = verbal_nulls(S.REPO / r["run"])
        a_o, a_i = r["a"]["write|best_ordinal"], r["a"]["identity|alt_name"]
        bb = r["b"][f"all|{K}"]
        # the per-draw arrays reproduce the summary before anything is drawn
        assert np.isclose(np.median(nulls["ordinal"]), a_o["null_median_of_medians"]), t
        assert np.isclose(np.median(nulls["name"]), a_i["null_median_of_medians"]), t
        assert np.isclose(nulls["share"].mean(), bb["random_mean"]), t
        n_rand |= {len(nulls["ordinal"]), len(nulls["name"]), len(nulls["share"])}
        mpath = S.REPO / r["run"] / "manifest.json"
        ordinal = tuple(json.loads(mpath.read_text())["ordinal"])  # the words the swap's best rank is taken over
        words.add(ordinal)
        S.record(out_name, t, "47.0 (a) position words the swap's best rank is taken over", len(ordinal),
                 source=rel(mpath))  # fmt: skip
        src_null = rel(S.REPO / r["run"] / "null.npz")
        for key, v, null, col, dy, what, n in (
            ("ordinal", a_o, nulls["ordinal"], ADDRESS, ARROW_DY, "best ordinal word's rank, h + pointer write",
             r["n_cases"]),
            ("name", a_i, nulls["name"], IDENTITY, -ARROW_DY, "new item's name rank, h + identity change",
             r["n_identity_cases"]),
        ):  # fmt: skip
            lo, hi = np.percentile(null, [2.5, 97.5])
            S.record(out_name, t, f"47.0 (a) {what} (median; null cut, null median)", v["median"], v["null_cut"],
                     v["null_median_of_medians"], n=n, source=vs)  # fmt: skip
            S.record(out_name, t, f"47.0 (a) {what}: the random draws' 95% range (2.5th, 97.5th percentile)",
                     float(np.median(null)), float(lo), float(hi), n=len(null), source=src_null)  # fmt: skip
            sc = rank_score(v["median"], null)
            own_band(a, y + dy, sc["band"], t, key, own)
            arrow(a, y + dy, sc["z"], col, hollow)
            S.record(out_name, t, f"47.0 (a) {what}: half-width w of the random draws' band, (ln 97.5th - ln 2.5th "
                     "percentile) / 2", sc["w"], n=len(null), source=src_null)  # fmt: skip
            S.record(out_name, t, f"47.0 (a) {what}: z = (ln random median - ln median) / w (lo, hi: the random "
                     "draws' 95% range in z)", sc["z"], *sc["band"], n=n, source=src_null)  # fmt: skip
            if t == rows[0][0]:
                label_9b[key] = (sc["z"], sc["band"])
        lo, hi = np.percentile(nulls["share"], [2.5, 97.5])
        src_omp = rel(S.REPO / r["run"] / "omp.jsonl")
        S.record(out_name, t, f"47.0 (b) share rebuilt by {K} lens directions: random draws (mean; mean, 95th pct)",
                 bb["random_mean"], bb["random_mean"], bb["random_p95"], source=vs)  # fmt: skip
        S.record(out_name, t, f"47.0 (b) share rebuilt by {K} lens directions: the random draws' 95% range",
                 float(nulls["share"].mean()), float(lo), float(hi), n=len(nulls["share"]), source=src_omp)  # fmt: skip
        raw[t] = {}
        for key, col, dy in (("pointer", ADDRESS, ARROW_DY), ("identity_mean", IDENTITY, -ARROW_DY)):
            S.record(out_name, t, f"47.0 (b) share rebuilt by {K} lens directions: {key}", bb[key], source=vs)
            # the same random draws for both changes: one median and band per model
            sc = share_score(bb[key], nulls["share"])
            own_band(b, y + dy, sc["band"], t, key, own)
            arrow(b, y + dy, sc["z"], col, hollow)
            S.record(out_name, t, f"47.0 (b) share rebuilt by {K} lens directions: {key}: z = (share - random median) "
                     "/ w, w half the random draws' 95% range (lo, hi: that range in z)", sc["z"], *sc["band"],
                     n=len(nulls["share"]), source=src_omp)  # fmt: skip
            raw[t][key] = (bb[key], sc["m"], sc["z"])
        S.record(out_name, t, f"47.0 (b) share rebuilt by {K} lens directions: the random draws' median",
                 raw[t]["pointer"][1], n=len(nulls["share"]), source=src_omp)  # fmt: skip
        S.record(out_name, t, f"47.0 (b) share rebuilt by {K} lens directions: pointer / random mean", bb["ratio"],
                 source=vs)  # fmt: skip
    assert len(n_rand) == 1, n_rand
    assert len(words) == 1, words
    n_rand, ordinal = n_rand.pop(), words.pop()
    # Dan's round 3: the swap's arrow ends inside the strip, the item change's far right, on both panels (the 9B, 27B
    # and Muse; Lightning's share-rebuilt arrow ends just outside the strip, said in the caption)
    for t, _ in rows:
        if t != F.LT[0]:
            assert abs(raw[t]["pointer"][2]) < 1, (t, raw[t])
        assert raw[t]["identity_mean"][2] > 10, (t, raw[t])
    lt_out = F.LT[0] in raw and abs(raw[F.LT[0]]["pointer"][2]) >= 1
    S.title(fig, "The lens reads which item is at the bridge, not where its locker sits",
            f"An address swap and an item change through the J++ lens, against {n_rand} random vectors of the same "
            "size")  # fmt: skip
    # the two in-plot words, on the 9B row only, checked against its numbers: the swap inside the strip, the identity
    # change at least ten units beyond it
    (z_swap, _), (z_item, _) = label_9b["ordinal"], label_9b["name"]
    assert abs(z_swap) < 1, label_9b
    assert z_item >= 10, label_9b
    y0 = ys[rows[0][0]]
    a.text(1.4, y0 + ARROW_DY, "address swap: inside the strip", ha="left", va="center", color=ADDRESS,
           fontsize=S.FONT, zorder=4)  # fmt: skip
    a.text(1.4, y0 - ARROW_DY - 0.08, "item change: far outside", ha="left", va="top", color=IDENTITY,
           fontsize=S.FONT, zorder=4)  # fmt: skip
    # Dan (21:50): the right panel names its arrows too
    b.text(1.4, y0 + ARROW_DY, "address swap", ha="left", va="center", color=ADDRESS, fontsize=S.FONT, zorder=4)
    b.text(1.4, y0 - ARROW_DY - 0.08, "item change", ha="left", va="top", color=IDENTITY, fontsize=S.FONT, zorder=4)
    for ax, title, xlabel in (
        (a, "Rank through the lens", "how far above random vectors the lens\nranks the word, in units of the strip (z)"),
        (b, "Share rebuilt", f"how far above random vectors {K} lens\ndirections rebuild it, in units of the strip (z)"),
    ):  # fmt: skip
        ax.axvspan(-1, 1, color=BAND_GREY, lw=0, zorder=1)
        ax.axvline(0, color="#999999", lw=0.8, zorder=1.5)
        ax.set_title(title, fontsize=12, weight="bold", loc="left", pad=22)
        ax.set_xlabel(xlabel)
    a.set_xlim(-3, 26)
    a.set_xticks([-1, 0, 1, 5, 10, 15, 20, 25], ["", "0", "", "5", "10", "15", "20", "25"])
    ns = sorted({models[t]["n_cases"] for t, _ in rows})
    for ax in axes:
        n_tag(ax, f"n = {ns[0] if len(ns) == 1 else ', '.join(map(str, ns))}  descriptive")
        ax.grid(axis="x", color="#eeeeee")
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
    a.set_ylim(-len(rows) + 0.5, 0.5)
    a.set_yticks(list(ys.values()), [F.NAMES[m] for _, m in rows])
    # the 27B's report (47.10, question last): one caption sentence, not a panel
    m = next(x for x in rblob["models"]
             if x["status"] == "tested" and "report" in x["orders"]["last"].get("readers", {}))  # fmt: skip
    o = m["orders"]["last"]
    rd, lens = o["readers"]["report"], o["lens"]["report"]
    for v, quantity, n in ((rd["alf"]["excess"], "47.10: the report's extra loss without the address", rd["n"]),
                           (rd["jpp"]["excess"], "47.10: the report's extra loss without the J++ part", rd["n"]),
                           (lens["top5_ordinal"], "47.10: lens top-5 holds the right ordinal (report prompt)",
                            lens["n"])):  # fmt: skip
        S.record("e8_report", m["target"], quantity, *v, n=n, source=rsrc)
    hs = [Line2D([], [], color=ADDRESS, lw=2.4, marker=">", ms=8),
          Line2D([], [], color=IDENTITY, lw=2.4, marker=">", ms=8), Patch(fc=BAND_GREY, ec="none")]  # fmt: skip
    F.legend(fig, hs, ["address swap", "item change (the positive control)", "random vectors' 95%"], 1 - 0.74 / h,
             ncol=3)  # fmt: skip
    # Dan (21:55): no caption; z and the strip are defined in the README's Setup, the 27B's report is E8's Result. Dan's
    # figures brief (29 Oct 10:00): with Lightning, one caption line on each model's status
    if F.LT[0] in raw:
        status = "9B, 27B, Muse: descriptive. Lightning: descriptive, dashed"
        status += "; its address swap's share rebuilt ends just past the strip" if lt_out else ""
        status += "; hatched: its own random range, where it sits off the strip." if own else "."
        caption(fig, [status, F.LT_NOTE], 0.7)
    S.save(fig, out_name)
    return out_name


# ---- fig09a / fig09b: the transfer, one message each ----------------------------------------------------------------

FORMATS = (("simple", "simple scenes"), ("prose", "prose"), ("json", "JSON"), ("table", "table"),
           ("natural", "natural\npassages"))  # fmt: skip
LABEL = {k: v.replace("\n", " ") for k, v in FORMATS}
EXCEPTION = 0.20  # a lookup extra loss at least this gets its number beside it (the brief's "one exception")


def rows_axis(ax, labels: list[str], first: bool) -> None:
    ax.set_ylim(-len(labels) + 0.45, 0.55)
    ax.tick_params(axis="y", length=0)
    if first:
        ax.set_yticks([-i for i in range(len(labels))], labels)
    else:
        ax.tick_params(axis="y", labelleft=False)


def build_transfer(out_name: str = "fig09a_transfer") -> str:
    """Fig. 9a: per model (9B, 27B, Muse, Lightning, 122B), the recall's and the lookup's extra loss without the J++ part by
    text format: simple scenes (docs/x0_numbers.json), prose / JSON / table (varied scenes) and natural passages with
    the fact first (run files, readme_story_figures.transfer_cells; Lightning's from its X0b verdict,
    readme_story_figures.lightning_transfer); the 0.10 band. A cell whose whole change switches fewer than 30 lookups is
    omitted and listed in the caption; hollow: the 9B's natural run had its gate lowered after the data, and every
    Lightning cell (its gate chosen after the pre-check was seen). The 122B (Dan's 11:30) from the same run files
    (transfer_cells), at its gate: filled."""
    plt = S.setup()
    slots = (*MODELS, F.LT, B122)
    top_in, body_in, bottom_in = 1.55, 3.3, 1.45
    h = top_in + body_in + bottom_in
    fig, axes = plt.subplots(1, len(slots), figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.16, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.10)
    S.title(fig, "The split carries over to other texts",
            "Extra loss without the J++ part, beyond a random part (same size), by text format")  # fmt: skip
    omitted: list[tuple[str, str]] = []
    for k, (ax, (target, m, name)) in enumerate(zip(axes, slots, strict=True)):
        S.extra_axis(ax)
        ax.set_title(name if k == 0 else SHORT[m], fontsize=12, weight="bold", loc="left")
        lt = m == "lightning"
        cells = {w: F.lightning_transfer(w) if lt else F.transfer_cells(target, w) for w in (F.X.RECALL, F.X.LOOKUP)}
        for i, (sc, _) in enumerate(FORMATS):
            sw = cells[F.X.LOOKUP].get((sc, "switched"))
            after = lt or (sc == "natural" and bool(cells[F.X.LOOKUP].get(("x5", "after"))))
            for w, col, dy, word in ((F.X.RECALL, INK, 0.16, "recall"), (F.X.LOOKUP, LOOKUP, -0.16, "lookup")):
                v = cells[w].get((sc, "jpp"))
                if v is None and lt:  # Lightning's empty rows say why in the panel
                    if w == F.X.RECALL:
                        ax.text(0.4, -i, cells[w][(sc, "why")], ha="center", va="center", color=S.COL["muted"])
                    continue
                if v is None:
                    omitted.append(("not run", f"{SHORT[m]} {LABEL[sc]} {word}"))
                    continue
                if w == F.X.LOOKUP and sw is not None and sw[0] < F.VALID_SWITCHES:
                    omitted.append(("too few switches", f"{SHORT[m]} {LABEL[sc]} lookup"))
                    S.record("fig09a", target, f"{sc}: lookup switches with the whole change", sw[0], n=sw[1],
                             source=cells[w][(sc, "src")])  # fmt: skip
                    continue
                ax.plot([v[1], v[2]], [-i + dy] * 2, color=col, lw=1.5, zorder=3, solid_capstyle="butt")
                ax.plot([v[0]], [-i + dy], S.MARK["remove"], ms=7, color=col, mfc="white" if after else col, mew=1.5,
                        zorder=4)  # fmt: skip
                S.record("fig09a", target, f"{word} extra loss without the J++ part: {sc}",
                         *[round(x, 4) for x in v], n=sw[1] if sw and sc != "simple" else None,
                         source=cells[w][(sc, "src")])  # fmt: skip
                if w == F.X.LOOKUP and v[0] >= EXCEPTION:
                    ax.text(v[2] + 0.04, -i + dy, f"{v[0]:.2f}", va="center", fontsize=S.FONT - 1, color=col)
                if i == 0:  # Dan's rethink (~21:45): each panel names its two series at its first row
                    ax.text(max(v[2], 0.0) + 0.05, -i + dy, word, va="center", fontsize=S.FONT - 1, color=col)
        rows_axis(ax, [lab for _, lab in FORMATS], k == 0)
        ax.grid(axis="x", color="#eeeeee")
    hs = [Line2D([], [], marker="o", ls="", color=INK, ms=7), Line2D([], [], marker="o", ls="", color=LOOKUP, ms=7),
          Patch(fc=S.COL["band"], ec="none")]  # fmt: skip
    F.legend(fig, hs, ["recall", "lookup", "the lookup's 0.10 bar"], 1 - 0.74 / h, ncol=3)
    # Dan (21:55): one caption line, the omitted cells; hollow (a gate lowered after the data) is in the README's Setup
    why = {r: [c for rr, c in omitted if rr == r] for r, _ in omitted}
    line = "; ".join(f"omitted, {r}: {', '.join(cs)}" for r, cs in why.items())
    caption(fig, [line[0].upper() + line[1:] + "." if line else "", F.LT_NOTE, B122_NOTE], bottom_in - 0.62)
    S.save(fig, out_name)
    return out_name


LT_X45D = S.REPO / "results" / "x0b_generalize" / "nem35l_x52_x45d" / "x45d-20261029T035250Z" / "verdict.json"


def build_refit(out_name: str = "fig09b_refit", lightning: Path | None = LT_X45D) -> str:
    """Fig. 9b (Part IV): per model (9B, 27B, Muse, and Lightning from its own verdict `lightning`, hollow: its gate
    was chosen after its pre-check was seen), the lookup's extra loss on prose / JSON / table without the address fit
    on simple scenes (open diamond) and without the address refit on half of that format's scenes, measured on the other
    half (circle; 45d, fixed in advance); the 0.10 band. A cell under X0's bar is omitted."""
    plt = S.setup()
    top_in, body_in, bottom_in = 1.55, 2.2, 1.6
    h = top_in + body_in + bottom_in
    models = (*MODELS, F.LT) if lightning is not None else MODELS
    fig, axes = plt.subplots(1, len(models), figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.12, right=0.975, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.10)
    S.title(fig, "The address must be refit for each text format",
            "The lookup's extra loss without the address, beyond a random part, on varied scenes")  # fmt: skip
    omitted = []
    formats = [f for f in FORMATS if f[0] in ("prose", "json", "table")]
    for k, (ax, (target, m, name)) in enumerate(zip(axes, models, strict=True)):
        S.extra_axis(ax)
        ax.set_title(name if k == 0 else SHORT[m], fontsize=12, weight="bold", loc="left")
        lt = m == "lightning"
        v, src = (json.loads(lightning.read_text()), rel(lightning)) if lt else F.x45d_verdict(m)
        rows_axis(ax, [lab for _, lab in formats], k == 0)
        ax.grid(axis="x", color="#eeeeee")
        if v is None:
            omitted.append(f"{SHORT[m]} (not run)")
            continue
        cells = {(c["format"], c["part"]): c for c in v["cells"] if c["reader"] == F.X.LOOKUP}
        for i, (fmt, _) in enumerate(formats):
            refit, simple = cells[(fmt, "pcf")], cells[(fmt, "alf")]
            assert refit["switched_whole"] == simple["switched_whole"], (m, fmt)
            S.record("fig09b_refit", target, f"(b) {fmt}: lookup switches with the whole change",
                     refit["switched_whole"], n=refit["n"], source=src)  # fmt: skip
            if not refit["valid"]:
                omitted.append(f"{SHORT[m]} {LABEL[fmt]}, too few switches ({refit['switched_whole']})")
                continue
            for c, simple_fit, dy, what in ((refit, False, 0.16, "the refit pointer"),
                                            (simple, True, -0.16, "the pointer fit on simple scenes")):  # fmt: skip
                e = c["excess"]
                ax.plot([e[1], e[2]], [-i + dy] * 2, color=ADDRESS, lw=1.5, zorder=3, solid_capstyle="butt")
                # the simple-scene fit: a diamond (open); the refit: a circle, filled except on Lightning (hollow)
                ax.plot([e[0]], [-i + dy], "D" if simple_fit else S.MARK["remove"], ms=6.5 if simple_fit else 7,
                        color=ADDRESS, mfc="white" if simple_fit or lt else ADDRESS, mew=1.5, zorder=4)  # fmt: skip
                S.record("fig09b_refit", target, f"(b) {fmt}: lookup extra loss without {what}", *e, n=c["n"],
                         source=src)  # fmt: skip
    hs = [Line2D([], [], marker="o", ls="", color=ADDRESS, ms=7),
          Line2D([], [], marker="D", ls="", color=ADDRESS, mfc="white", mec=ADDRESS, mew=1.5, ms=6.5),
          Patch(fc=S.COL["band"], ec="none")]  # fmt: skip
    F.legend(fig, hs, ["refit on the format", "fit on simple scenes", "the 0.10 bar"], 1 - 0.74 / h, ncol=3)
    lines = ["Diamond: the address fit on simple scenes, compared after the data; circle: refit, fixed in advance."]
    if lightning is not None:
        lines += ["9B, 27B, Muse: fixed in advance, ●. Lightning: the same rule, its circles hollow. " + F.LT_NOTE]
    lines += [f"Omitted: {'; '.join(omitted)}."] if omitted else []
    caption(fig, lines, bottom_in - 0.68)
    S.save(fig, out_name)
    return out_name


# ---- fig13: attention follows the address (49.7) --------------------------------------------------------------------

ATTN_SITES = ("last", "question")  # scripts/x49_attn.SITES; the decisive site is the last token
ATTN_ARMS = (("none", "no change"), ("swap", "the swap"), ("random", "a random vector"))


def mean_ci(values: np.ndarray, entities: list[str]) -> list[float]:
    """[mean, lo, hi], the 95% cluster bootstrap over bridge entities (scripts/x49_attn.mean_ci's)."""
    rr = F.X.resampled_rates({"v": np.asarray(values, dtype=float).tolist()}, list(entities), F.X.N_BOOT)
    return [float(np.mean(values)), *F.X.interval(rr["v"])]


def attention_roles(run_dir: Path) -> dict:
    """One 49.7 run read back as scripts/x49_attn.analyse reads it: per read-half pair, the last token's attention mass
    on slot j's and slot k's locker sentence under none / the swap / the random vector, the mean over the five candidate
    heads (heads.json, fit half); whether the lookup answered slot k's locker under the swap; the pairs' entities."""
    m = json.loads((run_dir / "manifest.json").read_text())
    items = [json.loads(x) for x in (run_dir / "cases.jsonl").read_text().splitlines()]
    rows = [json.loads(x) for x in (run_dir / "outcomes.jsonl").read_text().splitlines()]
    heads = json.loads((run_dir / "heads.json").read_text())["candidates"]
    a = np.load(run_dir / "attention.npz")
    layers = [int(x) for x in a["layers"]]
    p_item, p_k = a["pair_item"].astype(int), a["pair_k"].astype(int)
    p_j = np.array([items[i]["j"] for i in p_item])
    read = np.array([items[i]["half"] == "read" for i in p_item])
    lk = {(r["scene"], r["arm"], r["k"]): r for r in rows if r["reader"] == F.X.LOOKUP}
    swap_cls = np.array([lk[(items[i]["scene"], "swap", int(k))]["class"] for i, k in zip(p_item, p_k, strict=True)])
    rand_cls = np.array([lk[(items[i]["scene"], "random", int(k))]["class"] for i, k in zip(p_item, p_k, strict=True)])

    def slots(name: str, n: int) -> np.ndarray:  # [n, layers, heads, sites, 3 slots] (the parts summed)
        return a[name].astype(np.float32).reshape(n, len(layers), int(m["n_heads"]), len(ATTN_SITES), 3, 3).sum(-1)

    mass = {"none": slots("mass_none", len(items))[p_item], "swap": slots("mass_swap", len(p_item)),
            "random": slots("mass_random", len(p_item))}  # fmt: skip
    rows_ = np.arange(len(p_item))
    out = {}
    for arm, mm in mass.items():
        five = np.mean([mm[:, layers.index(c["layer"]), c["head"], 0] for c in heads], 0)  # [P, 3 slots]
        out[arm] = {"j": five[rows_, p_j][read], "k": five[rows_, p_k][read]}
    return {"roles": out, "switched": swap_cls[read] == "target", "random_k": rand_cls[read] == "target",
            "entities": [items[i]["entity"] for i in p_item[read]], "heads": heads}  # fmt: skip


def build_attention(verdict_dir: Path, out_name: str = "fig13_attention") -> str:
    """Fig. 13: per model (9B, 27B, Muse), the last token's attention mass on slot j's (the original) and slot k's (the
    swapped-in) locker sentence, the mean of the five candidate heads over the read half's pairs (49.7, fixed in
    advance): no change, the swap on pairs whose lookup answered slot k (solid) and on pairs whose answer stayed
    (lighter), the random vector on the switched pairs (grey band); beside it the share of lookups answering slot k.
    Checked against the verdict: five times the mean move on the switched pairs equals its 'sums five'."""
    vpath = verdict_dir / "verdict.json"
    v = {r["target"]: r for r in json.loads(vpath.read_text())["results"] if r.get("status") == "tested"}
    plt = S.setup()
    top_in, body_in, bottom_in = 1.85, 2.6, 1.5
    h = top_in + body_in + bottom_in
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, h), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.985, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.10)
    S.title(fig, "Attention follows the address swap, even where the answer stays",
            "Last token's attention on each locker sentence, mean of five heads; read half of the items")  # fmt: skip
    omitted, w = [], 0.2
    for k_ax, (ax, (target, m, name)) in enumerate(zip(axes, MODELS, strict=True)):
        ax.set_title(name if k_ax == 0 else SHORT[m], fontsize=12, weight="bold", loc="left", pad=20)
        r = v.get(target)
        if r is None:
            omitted.append(f"{SHORT[m]} (not run)")
            continue
        run_dir = S.REPO / "results" / "x49_attn" / r["run"]
        d = attention_roles(run_dir)
        sw, ents = d["switched"], np.array(d["entities"])
        move = (d["roles"]["swap"]["k"] - d["roles"]["swap"]["j"]) - (d["roles"]["none"]["k"] - d["roles"]["none"]["j"])
        assert np.isclose(5 * move[sw].mean(), r["sites"]["last"]["sums"]["five"][0], atol=1e-3), target
        src = rel(run_dir / "attention.npz")
        for gi, role in enumerate(("j", "k")):
            x0 = gi
            groups = (("none", sw, 0.25, -w, "no change, switched pairs"), ("swap", sw, 1.0, 0.0, "the swap, answer switched"),
                      ("swap", ~sw, 0.55, w, "the swap, answer stayed"))  # fmt: skip
            for arm, sel, alpha, dx, what in groups:
                ci = mean_ci(d["roles"][arm][role][sel], ents[sel].tolist())
                ax.bar(x0 + dx, ci[0], width=w * 0.92, color=LOOKUP, alpha=alpha, lw=0, zorder=2)
                ax.plot([x0 + dx] * 2, ci[1:], color="#1e1e1e", lw=1.0, zorder=3)
                S.record("fig13", target, f"attention mass on slot {role}'s locker sentence, {what} (mean of five heads, "
                         "read half)", *[round(x, 4) for x in ci], n=int(sel.sum()), source=src)  # fmt: skip
            ci = mean_ci(d["roles"]["random"][role][sw], ents[sw].tolist())
            lo, hi = ci[1] - 0.008, ci[2] + 0.008
            ax.fill_between([x0 - 1.6 * w, x0 + 1.6 * w], [lo] * 2, [hi] * 2, color=NULL, alpha=0.8, lw=0, zorder=1.5)
            S.record("fig13", target, f"attention mass on slot {role}'s locker sentence, a random vector, switched pairs "
                     "(mean of five heads, read half)", *[round(x, 4) for x in ci], n=int(sw.sum()), source=src)  # fmt: skip
        share = r["switch_share"]
        ax.bar(2, share[0], width=w * 0.92, color=LOOKUP, zorder=2)
        ax.plot([2, 2], share[1:], color="#1e1e1e", lw=1.0, zorder=3)
        ax.fill_between([2 - 1.6 * w, 2 + 1.6 * w], [0] * 2, [0.012] * 2, color=NULL, alpha=0.8, lw=0, zorder=1.5)
        S.record("fig13", target, "lookups answering slot k's locker under the swap (read half)", *share,
                 n=r["read_pairs"], source=rel(vpath))  # fmt: skip
        S.record("fig13", target, "lookups answering slot k's locker under a random vector (read half)",
                 r["lookup_shares"]["random"]["target"], n=r["read_pairs"], source=rel(vpath))  # fmt: skip
        ax.set_xticks([0, 1, 2], ["old\nlocker", "new\nlocker", "lookups\nmoved"])
        ax.tick_params(axis="x", length=0)
        ax.set_xlim(-0.55, 2.45)
        ax.set_ylim(0, 1.0)
        ax.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
        ax.grid(axis="y", color="#eeeeee")
        ax.set_axisbelow(True)
        n_tag(ax, f"n = {int(sw.sum())} / {int((~sw).sum())} pairs  ●")
    axes[0].set_ylabel("attention mass / share")
    hs = [Patch(fc=LOOKUP, alpha=0.25, ec="none"), Patch(fc=LOOKUP, ec="none"), Patch(fc=LOOKUP, alpha=0.55, ec="none"),
          Patch(fc=NULL, alpha=0.8, ec="none")]  # fmt: skip
    F.legend(fig, hs, ["no change", "the swap, answer switched", "the swap, answer stayed", "a random vector"],
             1 - 0.74 / h, ncol=2)  # fmt: skip
    lines = [
        "Old locker: the bridge item's own; new: the one the swap points to. n: pairs whose lookup answered the new "
        "locker under the swap / pairs whose answer stayed. The five heads: the most locker-attending heads after L, "
        "chosen on the fit half; the single best head is in the test's own figures."
    ]
    lines += [f"Omitted: {'; '.join(omitted)}."] if omitted else []
    caption(fig, lines, bottom_in - 0.75)
    S.save(fig, out_name)
    return out_name


# ---- fig14: learned subspaces (48.1, 49.8) --------------------------------------------------------------------------


def build_learned(das_dir: Path, pos_dir: Path, out_name: str = "fig14_learned") -> str:
    """Fig. 14, the 9B (48.1 and 49.8, fixed in advance): (1) own interchange accuracy by subspace size k on the test
    pairs: the lookup's and the recall's own learned subspace (48.1) and the learned address (49.8: the lookup's
    position answers; the recall moved by it), each against a random and a shuffled subspace; (2) the hand-built
    address U's and the swap directions W's energy inside the learned address, against a random subspace (k / d) and
    the shuffled one. The 27B and Muse wait for 51.3 (sealed)."""
    dpath, ppath = das_dir / "verdict.json", pos_dir / "verdict.json"
    das = next(m for m in json.loads(dpath.read_text())["models"] if m["target"] == "qwen3.5-9b")
    pos = next(m for m in json.loads(ppath.read_text())["models"] if m["target"] == "qwen3.5-9b")
    dsrc, psrc, target = rel(dpath), rel(ppath), "qwen3.5-9b"
    plt = S.setup()
    top_in, body_in, bottom_in = 2.3, 2.7, 1.25
    h = top_in + body_in + bottom_in
    fig, (a, b) = plt.subplots(1, 2, figsize=(S.WIDTH, h), gridspec_kw={"width_ratios": [1.35, 1]})
    fig.subplots_adjust(left=0.09, right=0.985, top=1 - top_in / h, bottom=bottom_in / h, wspace=0.28)
    S.title(fig, "A learned address overlaps the hand-built one and is read by both readers",
            "Qwen3.5-9B: subspaces learned to carry each reader's switch, and one learned for the address", limit=80)  # fmt: skip
    series = [(das["readers"]["PP"]["test"], "own_iia", LOOKUP, "-", "the lookup's own subspace", dsrc),
              (das["readers"]["PM"]["test"], "own_iia", INK, "-", "the recall's own subspace", dsrc),
              (pos["test"], "own_iia", ADDRESS, "-", "the learned address: lookup", psrc),
              (pos["test"], "recall_cross", INK, "--", "the learned address: recall moved", psrc)]  # fmt: skip
    for blob, key, col, ls, label, src in series:
        ks = sorted(blob[key], key=int)
        xs = [int(k) * (1.1 if key == "recall_cross" else 1.0) for k in ks]
        vals = [blob[key][k] for k in ks]
        a.plot(xs, [x[0] for x in vals], color=col, ls=ls, lw=1.8, zorder=3)
        for x, k, val in zip(xs, ks, vals, strict=True):
            a.plot([x, x], val[1:], color=col, lw=1.2, zorder=3)
            a.plot([x], [val[0]], S.MARK["swap"], ms=7, color=col, zorder=4)
            S.record("fig14", target, f"{label}: k = {k}, test pairs", *[round(v_, 4) for v_ in val],
                     n=blob["n"], source=src)  # fmt: skip
        if key == "own_iia":
            sh = [blob["shuffled_iia"][k][0] for k in ks]
            a.plot(xs, sh, color=col, ls=":", lw=1.4, zorder=2)
            for k in ks:
                S.record("fig14", target, f"{label}, a shuffled subspace: k = {k}", *blob["shuffled_iia"][k],
                         n=blob["n"], source=src)  # fmt: skip
                S.record("fig14", target, f"{label}, a random subspace: k = {k}", *blob["random_iia"][k], n=blob["n"],
                         source=src)  # fmt: skip
    a.fill_between([0.8, 80], [0] * 2, [0.02] * 2, color=NULL, alpha=0.8, lw=0, zorder=1)
    a.set_xscale("log", base=2)
    a.set_xlim(0.8, 80)
    a.set_xticks([1, 2, 4, 8, 16, 64], ["1", "2", "4", "8", "16", "64"])
    a.set_xlabel("subspace size k")
    a.set_ylim(0, 1.02)
    a.set_yticks([0, 0.5, 1], ["0", "0.5", "1"])
    a.set_ylabel("switches carried (share)")
    a.grid(axis="y", color="#eeeeee")
    a.set_title("Interchange through the subspace", fontsize=12, weight="bold", loc="left", pad=20)
    n_tag(
        a, f"n = {das['readers']['PP']['test']['n']}, {das['readers']['PM']['test']['n']}, {pos['test']['n']} pairs  ●"
    )
    ks = [k for k in pos["ks"]]
    wbar = 0.28
    for i, k in enumerate(ks):
        g, gs = pos["geometry"][f"R_pos_k{k}"], pos["geometry"][f"shuf_pos_k{k}"]
        for dx, key, alpha, what in ((-wbar / 2, "cos2_U", 1.0, "the hand-built address U"),
                                     (wbar / 2, "cos2_W", 0.55, "the swap directions W")):  # fmt: skip
            b.bar(i + dx, g[key], width=wbar * 0.92, color=ADDRESS, alpha=alpha, lw=0, zorder=2)
            b.plot([i + dx - wbar * 0.46, i + dx + wbar * 0.46], [gs[key]] * 2, color="#1e1e1e", ls=":", lw=1.4,
                   zorder=3)  # fmt: skip
            S.record("fig14", target, f"energy of {what} inside the learned address, k = {k}", g[key], n=g["n"],
                     source=psrc)  # fmt: skip
            S.record("fig14", target, f"energy of {what} inside a shuffled subspace, k = {k}", gs[key], n=gs["n"],
                     source=psrc)  # fmt: skip
        b.fill_between([i - wbar * 1.1, i + wbar * 1.1], [0] * 2, [max(g["random_expectation"], 0.006)] * 2, color=NULL,
                       alpha=0.8, lw=0, zorder=1.5)  # fmt: skip
        S.record("fig14", target, f"energy inside a random subspace (k / d), k = {k}", g["random_expectation"],
                 source=psrc)  # fmt: skip
    b.set_xticks(range(len(ks)), [f"k = {k}" for k in ks])
    b.tick_params(axis="x", length=0)
    b.set_xlim(-0.6, len(ks) - 0.4)
    b.set_ylim(0, 0.5)
    b.set_yticks([0, 0.25, 0.5], ["0", "0.25", "0.5"])
    b.set_ylabel("share of energy inside")
    b.grid(axis="y", color="#eeeeee")
    b.set_title("Overlap with the address", fontsize=12, weight="bold", loc="left", pad=20)
    n_tag(b, f"n = {pos['test']['n']} pairs  ●")
    hs = [Line2D([], [], color=LOOKUP, lw=1.8, marker=S.MARK["swap"], ms=6),
          Line2D([], [], color=INK, lw=1.8, marker=S.MARK["swap"], ms=6),
          Line2D([], [], color=ADDRESS, lw=1.8, marker=S.MARK["swap"], ms=6),
          Line2D([], [], color=INK, lw=1.8, ls="--", marker=S.MARK["swap"], ms=6),
          Patch(fc=ADDRESS, ec="none"), Patch(fc=ADDRESS, alpha=0.55, ec="none"),
          Line2D([], [], color="#555555", ls=":", lw=1.4), Patch(fc=NULL, alpha=0.8, ec="none")]  # fmt: skip
    F.legend(fig, hs, ["the lookup's own subspace", "the recall's own subspace", "the learned address: lookup",
                       "the learned address: recall moved", "the hand-built address", "the swap directions",
                       "a shuffled subspace", "a random subspace"], 1 - 0.74 / h, ncol=2)  # fmt: skip
    caption(fig, ["Qwen3.6-27B and Muse: wait for their learned-subspace runs (sealed). Muse's earlier run, on few "
                  "pairs: the supplement."], 0.42)  # fmt: skip
    S.save(fig, out_name)
    return out_name
