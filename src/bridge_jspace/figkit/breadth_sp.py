"""The breadth README's figures (figures/breadth/, Zach's set) on styles-plot, for the readme target. Every number is a
row of docs/breadth/data.csv (scripts/report_breadth.py, readers in scripts/breadth_data.py), read by key; the old
builder (scripts/fig_neel.py) drew them on the pod. Models are rows in the vocabulary's order (the old figures sorted
them by strength and coloured them by model: here a colour is a role), conditions are columns or lanes, verdict texts
stay in the README (Dan, 7 Nov). Fig. 6 is the root README's r4_pointer (figures/readme/04_pointer.png: the same
pointer runs and the probe's subspace; one figure, linked from both READMEs); fig11_scorecard becomes a markdown table and is not drawn.

uv run python -m bridge_jspace.figkit.breadth_sp [ids...]
"""

from __future__ import annotations

import csv
import re
import sys
from functools import cache

import styles_plot as sp

from bridge_jspace import figdata as D
from bridge_jspace.figkit import layout as L
from bridge_jspace.figkit import readme_sp as RS
from bridge_jspace.figkit.writeup_sp_base import REPO, vocab


def ids() -> dict[str, str]:
    """Breadth id (data.csv's model column) -> the vocabulary's model key."""
    return {e.id: e.key for e in vocab().entities("models")}


def b(key: str):
    return D.b(key)


@cache
def _n() -> dict[str, int]:
    """data.csv's n column by key (D.b carries value, lo, hi only)."""
    with (REPO / "docs/breadth/data.csv").open() as f:
        return {r["key"]: int(float(r["n"])) for r in csv.DictReader(f) if r["n"]}


def n_of(key: str) -> int | None:
    return _n().get(key)


def est(c, cell, key, label=False, interval=True) -> sp.Est:
    lo, hi = (c[1], c[2]) if interval and c[1] is not None else (None, None)
    return sp.Est(c[0], lo, hi, cell=cell, key=key, label=label)


def models_with(pattern: str) -> list[tuple[str, str]]:
    """(breadth id, model key) in the vocabulary's order, for the models whose key `pattern.format(id)` exists."""
    return [(i, m) for i, m in ids().items() if b(pattern.format(i))]


# ---- fig01: needed --------------------------------------------------------------------------------------------------
CONTROLS01 = (("rot", "rotated"), ("u", "logit lens"), ("pc", "PCA"))
FINALS = (("K", "the fact in the passage", "lookup"), ("P", "a new made-up fact in the passage", "lookup"),
          ("A", "the answer word on another entity", "recall"),
          ("N", "nothing in the passage, no lures", "recall"), ("M", "recall, lures present", "recall"))  # fmt: skip


def fig01_needed() -> sp.Figure:
    """(top) Per model, M − K under the lens part's top-10 knock-out at the model's band, against the same knock-out
    rotated, the logit lens's top 10, and the same norm along the top principal directions (grey). (bottom) For the
    three strong models, the points lost by where the answer is (stated facts in the lookup's colour, the rest in the
    recall's)."""
    v = vocab()
    rows = models_with("ko.{}.mk")
    lens = {m: est(b(f"ko.{i}.mk"), f"mk.{i}", f"ko.{i}.mk", label=True) for i, m in rows}
    series = [sp.Series("control", {m: est(c, f"mk.{i}", f"ko.{i}.{k}", interval=True)
                                    for i, m in rows if (c := b(f"ko.{i}.{k}"))}, control=name)
              for k, name in CONTROLS01]  # fmt: skip
    # one column per arm: grey dots of different controls in one column could not be told apart
    top = sp.DotTable([m for _i, m in rows], [
        sp.DotColumn("lens part knocked out", "gap", (-8, 72), (0, 30, 60), series=[sp.Series("neutral", lens, word="lens part knocked out")]),
        *(sp.DotColumn(s.control, "gap", (-8, 72), (0, 30, 60), series=[s]) for s in series),
    ])  # fmt: skip
    strong = [(i, m) for i, m in rows if i in ("q9", "q27", "nl")]
    vb = v.with_entities("finals", [(k, name) for k, name, _r in FINALS])
    cols = []
    for i, m in strong:
        cells = {"lookup": {}, "recall": {}}
        for k, _name, role in FINALS:
            c = b(f"ko.{i}.lost{k}")
            if c:
                cells[role][k] = sp.Est(c[0], cell=f"lost.{i}", key=f"ko.{i}.lost{k}", label=True)
        cols.append(sp.DotColumn(v.entity("models", m).name, "drop", (-2, 62), (0, 30, 60),
                                 series=[sp.Series("lookup", cells["lookup"]), sp.Series("recall", cells["recall"])]))  # fmt: skip
    bottom = sp.DotTable([k for k, *_ in FINALS], cols, kind="finals",
                         note="accuracy drop under the lens part's top-10 knock-out, by where the answer is")  # fmt: skip
    return sp.Figure("breadth_fig01_needed", vb).add(top, bottom)


# ---- fig03: robust --------------------------------------------------------------------------------------------------
RELATIONS = ("countries", "languages", "people", "cities", "companies", "landmarks", "dishes", "animals")
STARTS = (("startP", "start P (read)"), ("startT", "start T (tracked)"), ("startM", "start M (recalled)"))
REPLICATIONS = (("mk", "run of record"), ("r2", "rendering 2"), ("r3", "rendering 3"), ("halfA", "test half A"),
                ("halfB", "test half B"), ("soft", "scored by probability"))  # fmt: skip


def _by_condition(kind, conds, key, cid, rows, rot=None, lim=(-8, 100)):
    """Rows are conditions, columns the strong models: M − K per condition, the rotated knock-out grey where run."""
    cols = []
    for i, m in rows:
        lens, ctrl = {}, {}
        for c, _name in conds:
            v_ = b(key.format(i, c))
            if v_:
                lens[c] = est(v_, f"{cid}.{i}", key.format(i, c), label=True)
            r = b(rot.format(i, c)) if rot else None
            if r:
                ctrl[c] = est(r, f"{cid}.{i}", rot.format(i, c), interval=False)
        series = [sp.Series("control", ctrl, control="rotated")] if ctrl else []
        cols.append(sp.DotColumn(vocab().entity("models", m).name, "gap", lim, (0, 40, 80),
                                 series=[*series, sp.Series("neutral", lens, word=vocab().entity("models", m).name)]))  # fmt: skip
    return sp.DotTable([c for c, _n in conds], cols, kind=kind)


def _strong():
    return [(i, m) for i, m in models_with("ko.{}.mk") if i in ("q9", "q27", "nl")]


def fig03a_robust() -> sp.Figure:
    """For the three strong models, M − K under the top-10 knock-out on every relation (the rotated knock-out grey).
    fig03_robust split in two (too tall for the readme target with the never-named table: Dan's rule, split)."""
    rel = tuple((r, r) for r in RELATIONS)
    v = vocab().with_entities("relations", rel)
    return sp.Figure("breadth_fig03a_robust", v).add(
        _by_condition("relations", rel, "ko.{}.rel.{}", "robust", _strong(), rot="ko.{}.rel.{}.rot")
    )


def fig03b_robust() -> sp.Figure:
    """For the three strong models, M − K on every start and the replications (renderings, test halves, scored by
    probability); below, its own table: the extra recall drop when the bridge is never named (RM − MM, start R; Dan
    7 Nov: a different quantity, its own axis)."""
    rows = _strong()
    v = vocab().with_entities("checks", STARTS + REPLICATIONS)
    never = {m: est(c, f"never.{i}", f"r.{i}", label=True) for i, m in rows if (c := b(f"r.{i}"))}
    never_t = sp.DotTable([m for _i, m in rows], [sp.DotColumn("bridge never named", "extra_loss", (-8, 40), (0, 15, 30),
                                                               series=[sp.Series("neutral", never, word="bridge never named")])])  # fmt: skip
    return sp.Figure("breadth_fig03b_robust", v).add(
        _by_condition("checks", STARTS + REPLICATIONS, "ko.{}.{}", "robust", rows), never_t
    )


# ---- fig05: carries -------------------------------------------------------------------------------------------------
SWAP_CONTROLS = (("paste", "the whole state swapped in"), ("swap_comp", "the rest swapped in"),
                 ("swap_rot", "rotated"), ("swap_u", "logit lens"))  # fmt: skip


def _swap_key(i: str) -> str | None:
    for stem in (f"swap.{i}", f"swap.{i}.mid"):
        if b(f"{stem}.swap"):
            return stem
    return None


def fig05_carries() -> sp.Figure:
    """Per model, the answers moved to another entity's attribute when the lens part at the bridge's mention is
    swapped in from that entity (its top 10 directions), against the whole state pasted, everything but the lens part
    swapped, the swap rotated, and the logit-lens part (grey). Bolt and Ministral at their mid band, K = 10."""
    rows = [(i, m, s) for i, m in ids().items() if (s := _swap_key(i))]
    lens = {m: est(b(f"{s}.swap"), f"swap.{i}", f"{s}.swap", label=True) for i, m, s in rows}
    series = [sp.Series("control", {m: est(c, f"swap.{i}", f"{s}.{k}") for i, m, s in rows if (c := b(f"{s}.{k}"))},
                        control=name) for k, name in SWAP_CONTROLS]  # fmt: skip
    # one column per arm, as fig01
    t = sp.DotTable([m for _i, m, _s in rows], [
        sp.DotColumn("another entity's lens part swapped in", "moved", (-6, 80), (0, 30, 60),
                     series=[sp.Series("lens", lens)]),
        *(sp.DotColumn(s.control, "moved", (-6, 80), (0, 30, 60), series=[s]) for s in series)])  # fmt: skip
    # B: is it just the answer token? The swap, the swap with the answer's direction taken out, the answer's direction
    # alone, and that direction rotated (grey), for the 27B and 9B (P → M finals)
    v = vocab().with_entities("answer_swaps", ANS)
    cols = []
    for i in ("q27", "q9"):
        lens = {k: est(c, f"ans.{i}", f"ans.{i}.{k}", label=True) for k, _n in ANS[:3] if (c := b(f"ans.{i}.{k}"))}
        rot = {k: est(c, f"ans.{i}", f"ans.{i}.{k}", label=True) for k, _n in ANS[3:] if (c := b(f"ans.{i}.{k}"))}
        cols.append(sp.DotColumn(v.entity("models", ids()[i]).name, "moved", (-6, 90), (0, 30, 60),
                                 series=[sp.Series("lens", lens), sp.Series("control", rot, control="rotated")]))  # fmt: skip
    b_ = sp.DotTable(
        [k for k, _n in ANS], cols, kind="answer_swaps", note="the answer's direction in the swapped lens part"
    )
    return sp.Figure("breadth_fig05_carries", v).add(t, b_)


ANS = (("swap", "the whole lens part (top 10)"), ("swap_noans", "the lens part minus the answer's direction"),
       ("swap_ans", "the answer's direction only"), ("swap_ans_rot", "the answer's direction, rotated"))  # fmt: skip


# ---- fig09: dose ----------------------------------------------------------------------------------------------------
DOSES = (1, 3, 10, 30, 100, 300)


def fig09_dose() -> sp.Figure:
    """Per model and number of lens directions knocked out (columns: 1 to 300), M − K, the rotated knock-out of the
    same size grey (its interval was not kept)."""
    rows = models_with("dose.{}.k10")
    cols = []
    for k in DOSES:
        lens, rot = {}, {}
        for i, m in rows:
            c = b(f"dose.{i}.k{k}")
            if c:
                lens[m] = est(c, f"dose.{i}", f"dose.{i}.k{k}", label=False)
            r = b(f"dose.{i}.k{k}.rot")
            if r:
                rot[m] = est(r, f"dose.{i}", f"dose.{i}.k{k}.rot", interval=False)
        cols.append(sp.DotColumn(f"{k} lens directions", "gap", (-8, 80), (0, 30, 60),
                                 series=[sp.Series("control", rot, control="rotated"), sp.Series("neutral", lens, word=f"{k} lens directions")]))  # fmt: skip
    return sp.Figure("breadth_fig09_dose", vocab()).add(sp.DotTable([m for _i, m in rows], cols))


# ---- fig04: where ---------------------------------------------------------------------------------------------------
WHERE = (("all", "every token"), ("bridge", "the bridge's mention"), ("context", "the passage"),
         ("question", "the question"))  # fmt: skip


def fig04_where() -> sp.Figure:
    """(top) Per model, M − K on dev by the depth of the knocked-out window (each window at the middle of its depth,
    with its interval); (bottom) M − K when the knock-out acts only at some tokens (columns): every token, the bridge's
    mention, the passage around it, the question (all starts pooled). The rotated knock-out at the same windows is the
    grey line."""
    rows = models_with("pos.{}.all.all")
    cols = []
    for w, header in WHERE:
        cells = {m: est(c, f"pos.{i}", f"pos.{i}.all.{w}", label=True) for i, m in rows if (c := b(f"pos.{i}.all.{w}"))}
        cols.append(
            sp.DotColumn(header, "gap", (-8, 70), (0, 30, 60), series=[sp.Series("neutral", cells, word=header)])
        )
    lines, prof_rows = [], []
    for i, m in ids().items():
        rx = re.compile(rf"^prof\.{i}\.(L\d+-\d+)$")
        win = sorted((d[0], v_) for k, v_ in D.breadth().items() if rx.match(k) and (d := b(f"{k}.depth")))
        if not win:
            continue
        prof_rows.append(m)
        x = [d for d, _v in win]
        lines.append(sp.Line(m, "neutral", x, [v_[0] for _d, v_ in win], cell=f"prof.{i}",
                             band=([v_[1] for _d, v_ in win], [v_[2] for _d, v_ in win])))  # fmt: skip
        rot = sorted((d[0], r[0]) for k, _v in D.breadth().items() if rx.match(k)
                     and (d := b(f"{k}.depth")) and (r := b(f"{k}.rot")))  # fmt: skip
        if rot:  # the rotated knock-out at the same windows (styles-plot 0.1.6: a grey line names its control)
            lines.append(sp.Line(m, "control", [d for d, _r in rot], [r for _d, r in rot], cell=f"prof.{i}",
                                 control="rotated"))  # fmt: skip
    sweep = sp.Sweep(prof_rows, "depth_share", "gap", lines, xlim=(0, 1), panel_h=0.9)
    return sp.Figure("breadth_fig04_where", vocab()).add(sweep, sp.DotTable([m for _i, m in rows], cols))


# ---- fig02: datasets ------------------------------------------------------------------------------------------------
DATASETS = (("toy1", "toy.{}.s1", "toy puzzles, data seed 1", "toy.{}.u"), ("toy2", "toy.{}.s2", "toy puzzles, data seed 2", None),
            ("toy3", "toy.{}.s3", "toy puzzles, data seed 3", None),
            ("nat1", "nat.{}.s1", "natural fact chains, seed 1", "nat.{}.u"), ("nat2", "nat.{}.s2", "natural fact chains, seed 2", None),
            ("nat3", "nat.{}.s3", "natural fact chains, seed 3", None),
            ("natplus", "natplus.{}", "natplus, rare and popular bridges", "natplus.{}.u"),
            ("v1", "v1.{}", "suite v1, three relations", "v1.{}.u"), ("v1r2", "v1.{}.s2", "suite v1, rendering 2", None),
            ("v2", "ko.{}.mk", "suite v2, eight relations", "ko.{}.u"), ("v2r2", "ko.{}.r2", "suite v2, rendering 2", None),
            ("v2r3", "ko.{}.r3", "suite v2, rendering 3", None))  # fmt: skip
VARIANTS = (("pop", "natplus.{}.pop", "natplus popular bridges"), ("rare", "natplus.{}.rare", "natplus rare bridges"),
            ("prefill", "v1.{}.prefill", "suite v1, the answer prefilled"), ("qa", "v1.{}.qa", "suite v1, raw Q&A"),
            ("base", "ko.{}base.mk", "suite v1 Q&A, the base model"), ("jlens", "v1.{}.jlens", "suite v1, the plain J-lens"))  # fmt: skip
BAR30 = 30  # the plan's bar, fixed in advance (docs/breadth/prereg_replication_1022.md, C1)


def fig02_datasets() -> sp.Figure:
    """The two Qwens on every dataset built (each dataset's own recall-minus-read contrast under the lens part's
    top-10 knock-out at the same band), the logit lens's top 10 beside where it ran, against the plan's 30-point bar;
    below, what moves it (bridge popularity, prefill, raw Q&A, the base model, the plain J-lens)."""
    v = vocab()
    qwens = [(i, m) for i, m in ids().items() if i in ("q9", "q27")]
    rule = [sp.Rule(BAR30, "bar fixed in advance: {}", unit="gap", key="breadth.bar30")]
    cols = []
    for i, m in qwens:
        lens, ctrl = {}, {}
        for row, key, _name, u in DATASETS:
            if c := b(key.format(i)):
                lens[row] = est(c, f"data.{i}", key.format(i))
            if u and (c := b(u.format(i))):
                ctrl[row] = est(c, f"data.{i}", u.format(i))
        for row, key, _name in VARIANTS:  # what moves it: rows under the datasets (one table keeps the figure wide)
            if c := b(key.format(i)):
                lens[row] = est(c, f"var.{i}", key.format(i))
        name = v.entity("models", m).name
        cols += [sp.DotColumn(name, "gap", (-8, 62), (0, 30, 60), series=[sp.Series("neutral", lens, word=name)], rules=rule),
                 sp.DotColumn(f"{name}: logit lens", "gap", (-8, 62), (0, 30, 60),
                              series=[sp.Series("control", ctrl, control="logit lens")])]  # fmt: skip
    vv = v.with_entities("datasets", [(r, n) for r, _k, n, _u in DATASETS] + [(r, n) for r, _k, n in VARIANTS])
    rows = [r for r, *_ in DATASETS] + [r for r, *_ in VARIANTS]
    return sp.Figure("breadth_fig02_datasets", vv).add(sp.DotTable(rows, cols, kind="datasets"))


def fig02b_datasets() -> sp.Figure:
    """fig02's panel B (its own file: with panel A the figure is too tall for the readme target): the other models
    on the datasets they ran, each dataset's own contrast, against the plan's 30-point bar."""
    return sp.Figure("breadth_fig02b_datasets", vocab()).add(
        _others([sp.Rule(BAR30, "bar fixed in advance: {}", unit="gap", key="breadth.bar30")])
    )


# fig02 B: the other models on the datasets they ran; each dataset's own contrast (the same keys fig_neel's F04 B read)
OTHER_DS = (("toy", "toy puzzles"), ("toy2", "toy, data seed 2"), ("natural", "natural chains"), ("natplus", "natplus"),
            ("v1", "suite v1"), ("v2", "suite v2"))  # fmt: skip
OTHER_KEY = {
    ("q32", "toy"): "old.q32.qwen3_32b_full2_ko_v1", ("q32", "toy2"): "old.q32.qwen3_32b_fresh2_ko_v1",
    ("q122", "toy"): "old.q122.qwen35_122b_full2_ko_v1", ("q122", "v1"): "v1.q122", ("q122", "v2"): "ko.q122.mk",
    ("mu", "toy"): "old.mu.muse30_full2_ko_v1", ("mu", "natplus"): "natplus.mu", ("mu", "v1"): "v1.mu",
    ("mu", "v2"): "ko.mu.mk",
    ("oh7", "toy"): "old.oh7.olmoh7_big2_ko_v1", ("oh7", "natural"): "old.oh7.olmoh7_natural_v1_chat_ko_v1",
    ("o7", "toy"): "old.o7.olmo3d7_big2_ko_v1", ("o7", "natural"): "old.o7.olmo3d7_natural_v1_chat_ko_v1",
    ("ol", "v1"): "v1.ol", ("ol", "v2"): "ko.ol.mk",
}  # fmt: skip


def _others(rule) -> sp.DotTable:
    rows = [(i, m) for i, m in ids().items() if any(k[0] == i for k in OTHER_KEY)]
    cols = []
    for ds, header in OTHER_DS:
        cells = {}
        for i, m in rows:
            key = OTHER_KEY.get((i, ds))
            c = b(key) if key else None
            cells[m] = est(c, f"other.{ds}.{i}", key, label=True) if c else sp.Missing("no run")
        cols.append(
            sp.DotColumn(
                header, "gap", (-10, 100), (0, 30, 60), series=[sp.Series("neutral", cells, word=header)], rules=rule
            )
        )
    return sp.DotTable([m for _i, m in rows], cols, note="other models on the datasets they ran")


# ---- sweeps: fig04's depth profile, fig07, fig08 ----------------------------------------------------------------------
def _layers(prefix: str, suffixes: tuple[str, ...], i: str) -> dict[str, list[tuple[int, float]]]:
    """{suffix: [(layer, value)]} for keys `<prefix>.<i>.L<layer>.<suffix>` in data.csv, by layer."""
    out: dict[str, list[tuple[int, float]]] = {s: [] for s in suffixes}
    rx = re.compile(rf"^{prefix}\.{i}\.L(\d+)\.(\w+)$")
    for key, (val, *_rest) in D.breadth().items():
        if (hit := rx.match(key)) and hit.group(2) in out:
            out[hit.group(2)].append((int(hit.group(1)), val))
    return {s: sorted(p) for s, p in out.items()}


def fig07_lookup() -> sp.Figure:
    """Per model and layer, the lens's top pick at the answer position: the attribute of the entity whose lens part
    was swapped in (from its own passage, or from one neutral sentence about it), against the unedited prompt (grey,
    its own attribute)."""
    rows = [(i, m) for i, m in ids().items() if _layers("look", ("swap",), i)["swap"]]
    lines = []
    for i, m in rows:
        pts = _layers("look", ("kept", "neutral", "swap"), i)
        for suf, role, word in (("swap", "lens", "another entity's own passage"),
                                ("neutral", "lens", "one neutral sentence about another entity"),
                                ("kept", "control", None)):  # fmt: skip
            if pts[suf]:
                x, y = zip(*pts[suf], strict=True)
                lines.append(
                    sp.Line(
                        m,
                        role,
                        list(x),
                        list(y),
                        cell=f"look.{i}",
                        word=word,
                        control="no change" if role == "control" else None,
                    )
                )
    return sp.Figure("breadth_fig07_lookup", vocab()).add(sp.Sweep([m for _i, m in rows], "layer", "top_pick", lines))


def fig08_readable() -> sp.Figure:
    """Per model and relative depth, how often the true attribute is ranked first among the relation's answers when
    read by the lens part (J++) at the bridge, against the logit lens (grey)."""
    rows = [(i, m) for i, m in ids().items() if (n := b(f"read.{i}.layers"))]
    lines = []
    for i, m in rows:
        n = b(f"read.{i}.layers")[0]
        pts = _layers("read", ("jlens", "logit"), i)
        for suf, role in (("jlens", "lens"), ("logit", "control")):
            if pts[suf]:
                x, y = zip(*pts[suf], strict=True)
                lines.append(
                    sp.Line(
                        m,
                        role,
                        [la / n for la in x],
                        list(y),
                        cell=f"read.{i}",
                        control="logit lens" if role == "control" else None,
                    )
                )
    return sp.Figure("breadth_fig08_readable", vocab()).add(sp.Sweep([m for _i, m in rows], "depth_share", "ranked_first",
                                                             lines, xlim=(0, 1)))  # fmt: skip


# ---- fig10: beyond two hops (Dan 7 Nov: split per panel) -------------------------------------------------------------
ARMS = (("paper10", "lens part knocked out", "neutral", None), ("paper10_rot", "rotated", "control", "rotated"),
        ("unembed10", "logit lens", "control", "logit lens"))  # fmt: skip
CHAINS = ("MMM", "PMM", "MPM", "PPM", "MMP", "MPP", "PMP")  # above PPM: the last hop is a recall
THREE = (("v2", "jsuite v2", "mod.{}.threehop.{}.{}-PPP"), ("nb", "second data seed", "mod2.{}.threehop.{}.{}-PPP"),
         ("nat3", "natural three-hop set", "nat3.{}.{}.{}"))  # fmt: skip


def _arm_columns(rows_keys, cell_of, key_of, unit, lim, ticks):
    """One column per arm (the knock-out, rotated, logit lens): one grey per column."""
    cols = []
    for arm, header, role, control in ARMS:
        cells = {}
        for rk in rows_keys:
            key = key_of(rk, arm)
            c = b(key) if key else None
            if c:
                cells[rk] = est(c, cell_of(rk), key, label=role != "control")
            elif role != "control":
                cells[rk] = sp.Missing("no run")
        cols.append(
            sp.DotColumn(
                header,
                unit,
                lim,
                ticks,
                series=[sp.Series(role, cells, control=control, word=header if role == "neutral" else None)],
            )
        )
    return cols


def fig10a1_beyond() -> sp.Figure:
    """Three hops whose last hop is a recall (the chains the plan predicts need the lens part)."""
    return _three("breadth_fig10a1_beyond", CHAINS[:4])


def fig10a2_beyond() -> sp.Figure:
    """Three hops whose last hop is read in the passage (the chains the plan predicts do not)."""
    return _three("breadth_fig10a2_beyond", CHAINS[4:])


THREE_HEAD = "three hops: each letter is one hop's source, P read in the passage, M recalled"


def _three(fid: str, chains: tuple[str, ...]) -> sp.Figure:
    """Three hops (README brief F6): per chain (rows; each letter one hop's source) and data set (lanes), the accuracy
    drop beyond the all-passage chain P → P → P under the lens part's top-10 knock-out, one axis per model (the 27B and
    Lightning; the 9B left out as before: its P → P → P alone loses most of its accuracy), the largest of its two
    same-size controls (rotated, logit lens) as the grey tick on the same axis. fig10a split by the last hop: one table
    of all seven chains is too tall for the readme target."""
    v = vocab().with_entities("chains", [(c, " → ".join(c)) for c in chains])
    knock, controls = ARMS[0][0], [arm for arm, *_ in ARMS[1:]]
    rks = [(c, ds) for c in chains for ds, *_ in THREE]
    cols = []
    for i in ("q27", "nl"):

        def key_of(rk, arm, i=i):
            chain, ds = rk
            pat = next(p for d, _n, p in THREE if d == ds)
            return pat.format(i, arm, chain) if ds != "nat3" or i == "nl" else None

        cells, ticks = {}, {}
        for rk in rks:
            key = key_of(rk, knock)
            c = b(key) if key else None
            cells[rk] = est(c, f"three.{rk[1]}.{i}", key, label=True) if c else sp.Missing("no run")
            ctl = [x[0] for arm in controls if (k := key_of(rk, arm)) and (x := b(k))]
            if ctl:
                ticks[rk] = max(ctl)
        cols.append(sp.DotColumn(v.entity("models", ids()[i]).name, "beyond_ppp", (-25, 110), (0, 40, 80),
                                 series=[sp.Series("neutral", cells, word=ARMS[0][1])], ticks=ticks))  # fmt: skip
    t = sp.DotTable(list(chains), [sp.ColumnGroup(THREE_HEAD, cols)], kind="chains",
                    lanes=[sp.Lane(ds, name) for ds, name, _p in THREE])  # fmt: skip
    return sp.Figure(fid, v).add(t)


NUMBERS = (("KR-PR", "v2", "counted, then reported"), ("AR-PR", "v2", "computed, then reported"),
           ("MR-PR", "v2", "recalled, then reported"), ("KM-PM", "nb", "counted, then used to recall"),
           ("AM-PM", "nb", "computed, then used to recall"), ("MM-ML", "nb", "recalled, then used to recall, not to look up"))  # fmt: skip


def fig10b_beyond() -> sp.Figure:
    """Numbers: per final (rows: how the number was made and what it is used for), the accuracy drop beyond the same
    final with the number read from the passage, per model (lanes), under the knock-out and its two controls. The
    reported rows are jsuite v2, the rows used to recall the larger second set (jsuite v2nb)."""
    models = [(i, ids()[i]) for i in ("q9", "q27", "nl")]  # the vocabulary's order
    v = vocab().with_entities("finals_n", [(c, name) for c, _ds, name in NUMBERS])
    ds_of = {c: ds for c, ds, _n in NUMBERS}

    def key_of(rk, arm):
        contrast, i = rk
        return f"{'mod' if ds_of[contrast] == 'v2' else 'mod2'}.{i}.numbers.{arm}.{contrast}"

    rks = [(c, i) for c, *_ in NUMBERS for i, _m in models]
    cols = _arm_columns(rks, lambda rk: f"num.{ds_of[rk[0]]}.{rk[1]}", key_of, "beyond_read", (-25, 75), (0, 30, 60))
    t = sp.DotTable([c for c, *_ in NUMBERS], cols, kind="finals_n",
                    lanes=[sp.Lane(i, v.entity("models", m).name) for i, m in models])  # fmt: skip
    return sp.Figure("breadth_fig10b_beyond", v).add(t)


REPLIES = (("right", "still right"), ("lure", "a lure in the passage"), ("other_cand", "another valid answer"),
           ("other", "something else"), ("bridge", "the bridge's name"))  # fmt: skip
FINALS_GEN = (("PM", "P → M"), ("MM", "M → M"))


def fig10c_beyond() -> sp.Figure:
    """What the model says instead: per model and final (lanes), the share of greedy replies under the knock-out in
    each class (columns; five classes: a dot table of shares, no stack), on natplus, with the number of replies."""
    rows = [(i, m) for i, m in ids().items() if b(f"gen.{i}.PM.right")]
    cols = []
    for k, header in REPLIES:
        cells = {(m, w): est(c, f"gen.{i}", f"gen.{i}.{w}.{k}", label=True)
                 for i, m in rows for w, _n in FINALS_GEN if (c := b(f"gen.{i}.{w}.{k}"))}  # fmt: skip
        cols.append(
            sp.DotColumn(header, "replies", (-5, 105), (0, 50, 100), series=[sp.Series("neutral", cells, word=header)])
        )
    n = {(m, w): sp.Est(float(c), key=f"gen.{i}.{w}.n", cell=f"gen.{i}")
         for i, m in rows for w, _n in FINALS_GEN if (c := n_of(f"gen.{i}.{w}.right"))}  # fmt: skip
    cols.append(sp.TextColumn("replies", "replies_n", n))
    t = sp.DotTable([m for _i, m in rows], cols, lanes=[sp.Lane(w, name) for w, name in FINALS_GEN],
                    note="generated replies on natplus under the knock-out")  # fmt: skip
    return sp.Figure("breadth_fig10c_beyond", vocab()).add(t)



FIGS = {"fig01_needed": fig01_needed, "fig03a_robust": fig03a_robust, "fig03b_robust": fig03b_robust,
        "fig04_where": fig04_where, "fig05_carries": fig05_carries, "fig09_dose": fig09_dose,
        "fig02_datasets": fig02_datasets, "fig02b_datasets": fig02b_datasets, "fig10a1_beyond": fig10a1_beyond,
        "fig10a2_beyond": fig10a2_beyond, "fig10b_beyond": fig10b_beyond, "fig10c_beyond": fig10c_beyond,
        "fig07_lookup": fig07_lookup, "fig08_readable": fig08_readable}  # fmt: skip


def build(ids_=None) -> list[str]:
    """Save the breadth set strict into figures/breadth/ (numbered files, figkit/layout.py). Returns the failures."""
    return L.build("breadth", FIGS, RS.TARGET, ids_)


if __name__ == "__main__":
    sys.exit(1 if build(sys.argv[1:] or None) else 0)
