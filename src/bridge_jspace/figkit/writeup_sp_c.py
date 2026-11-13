"""The write-up figures styles-plot 0.1.6 can draw (Dan, 7 Nov, grammar decisions 1, 2 and 4): a second estimate of one
role in its own column (fig06), a 100% stack with its numbers in text columns beside it (fig07; stacks carry no
whiskers), a depth sweep whose points fixed in advance carry their own vertical whiskers (appB_f15), and appB_f18 as
the depth README's fig21 (the same cells). Same data accessors as the figkit builders; writeup_sp.FIGS takes them in."""

from __future__ import annotations

import dataclasses

import styles_plot as sp

from bridge_jspace import figdata as CV
from bridge_jspace import figdata as D
from bridge_jspace import figdata as S
from bridge_jspace.figkit.writeup_sp_base import ZK, est, need, vocab

DAN = [m for m, _ in D.DAN]
GAP = "gap: recall − lookup"


def _id(m: str) -> str:
    return vocab().entity("models", m).id


# ---- Fig. 6: nine models -------------------------------------------------------------------------------------------------
NINE = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning", "qwen3.5-122b-a10b", "deepseek",
        "ministral", "bolt", "olmo")  # fmt: skip
SWAPKEY = {"ds": "swap.ds.mid.swap", "mi": "swap.mi.mid.swap"}  # (deck_figs.f_nine)


# rows by the bar fixed before the main runs (amendment 33: gap >= 30, rotated and logit-lens controls < 10)
BANDS = (("Passes the bar", ("qwen3.5-9b", "qwen3.6-27b", "nemotron-3.5-lightning")),
         ("Fails on a control", ("muse-glimmer-30b", "qwen3.5-122b-a10b")),
         ("Fails on the gap", ("ministral", "deepseek", "bolt", "olmo")))  # fmt: skip
NINE_ROWS = tuple(m for _, ms in BANDS for m in ms)
# docs/breadth/prereg_replication_1022.md, amendment 33: "M - K >= 30 with the logit-lens and rotated controls < 10"
GAP_BAR, CONTROL_BAR = 30, 10


def _nine_cells(key: str, cell: str, label: bool = True) -> dict:
    """One estimate per model from docs/breadth/data.csv (`key` with {k}); "not run" where no run exists."""
    out = {}
    for m in NINE_ROWS:
        k = _id(m)
        c = D.b(key.format(k=k))
        out[m] = sp.Missing("not run") if c is None else est(c, f"{cell}.{k}", key=key.format(k=k), label=label)
    return out


def _verdict(m: str) -> str:
    """The bar's verdict on one model from its data (gap >= 30, both controls < 10), checked against its band."""
    k = _id(m)
    gap = need(D.b(f"ko.{k}.mk"), f"gap {k}")[0] >= GAP_BAR
    ctrl = max(need(D.b(f"ko.{k}.{c}"), f"{c} {k}")[0] for c in ("rot", "u")) < CONTROL_BAR
    word = {(True, True): "passes", (True, False): "fails: control", (False, True): "fails: gap"}.get(
        (gap, ctrl), "fails: gap and control")
    band = next(b for b, ms in BANDS if m in ms)
    assert (word == "passes") == (band == "Passes the bar"), (m, word, band)
    return word


def fig06_nine_models() -> sp.Figure:
    """Nine models in three bands by the bar fixed before the main runs: the recall − lookup gap
    under the knock-out against the bar of 30, and what each same-size control costs against the limit of 10, one
    panel per control (one grey dot per line: the grammar gives a second control its own panel)."""
    gap = sp.DotColumn("Recall minus lookup gap", "nine_gap", (0, 70), (0, 30, 60), weight=1.4, labels="right",
                       series=[sp.Series("neutral", _nine_cells("ko.{k}.mk", "gap"), word="Recall minus lookup gap")],
                       rules=[sp.Rule(GAP_BAR, "bar: gap ≥ {} points", unit="nine_bar", key="nine.bar.gap")])  # fmt: skip

    def control(key, cell, header, name, unit):
        """One control panel on the shared 0-45 scale (Muse's logit-lens whisker ends at 40), the limit labelled over
        the panel. A cost over the limit stays grey: brick is the answer span's colour in the post (one meaning per
        colour), so brief 5's brick failing control is not drawn; its dot past the dashed limit shows it."""
        return sp.DotColumn(header, "nine_control", (0, 45), (0, 20, 40), labels="right",
                            series=[sp.Series("control", _nine_cells(key, cell), control=name)],
                            rules=[sp.Rule(CONTROL_BAR, "limit: {} points", unit=unit, key="nine.bar.control")])

    rot = control("ko.{k}.rot", "rot", "rotated part", "rotated", "nine_bar")
    logit = control("ko.{k}.u", "logit", "logit-lens directions", "logit lens", "nine_limit")
    # brief 5: each verdict a header over its band's rows (styles-plot 0.2.3 row groups), rows one height; the bands
    # are checked against the data
    assert all(_verdict(m) for m in NINE_ROWS)
    groups = [sp.RowGroup(band, ms) for band, ms in BANDS]
    table = sp.DotTable(list(NINE_ROWS), [gap, sp.Gutter(), sp.ColumnGroup("Cost of same-size controls",
                                                                          [rot, sp.Gutter(0.22), logit])],
                        kind="nine", groups=groups)  # fmt: skip
    return sp.Figure("fig06_nine_models", vocab(),
                     subtitle="method: knock-out, band of middle layers · data: known-fact set").add(table)


def nine_tests(fid: str) -> sp.Figure:
    """The README's nine-model figure (f3_nine_models; its text cites the swap): four columns in the bar's order, the
    gap under the knock-out, the larger of the rotated and logit-lens controls, the gap scored by the answer's
    probability, and the answers moved by another entity's lens part swapped in. The write-up draws
    fig06_nine_models instead."""
    rot, logit = {}, {}
    for m in NINE_ROWS:
        k = _id(m)
        r_, u_ = need(D.b(f"ko.{k}.rot"), f"rot {k}"), need(D.b(f"ko.{k}.u"), f"u {k}")
        code, c = ("rot", r_) if r_[0] >= u_[0] else ("u", u_)
        (rot if code == "rot" else logit)[m] = est(c, f"ctrl.{k}", key=f"ko.{k}.{code}", label=True)
    swap = {}
    for m in NINE_ROWS:
        k = _id(m)
        key = SWAPKEY.get(k, f"swap.{k}.swap")
        c = D.b(key)
        swap[m] = sp.Missing("not run") if c is None else est(c, f"swap.{k}", key=key, label=True)
    cols = [
        sp.DotColumn("Gap under the knock-out", "points", (-5, 80), (0, 30, 60), weight=1.15,
                     rules=[sp.Rule(GAP_BAR, "bar: {}", unit="points", key="nine.bar.gap")],
                     series=[sp.Series("neutral", _nine_cells("ko.{k}.mk", "gap"), word="Gap under the knock-out")]),
        sp.DotColumn("Larger control", "points", (-5, 50), (0, 20, 40), weight=1.2,
                     series=[sp.Series("control", rot, control="rotated", word="rotated"),
                             sp.Series("control", logit, control="logit lens", word="logit lens")],
                     rules=[sp.Rule(CONTROL_BAR, "bar: {}", unit="points", key="nine.bar.control")]),
        sp.DotColumn("Gap scored by probability", "points", (-5, 80), (0, 30, 60), weight=1.15,
                     series=[sp.Series("neutral", _nine_cells("ko.{k}.soft", "soft"), word="Gap scored by probability")]),
        sp.DotColumn("Swap", "moved", (-5, 100), (0, 40, 80), series=[sp.Series("lens", swap, word="Swap")]),
    ]  # fmt: skip
    row_sub = {ms[0]: band for band, ms in BANDS}
    return sp.Figure(fid, vocab()).add(sp.DotTable(list(NINE_ROWS), cols, kind="nine", row_sub=row_sub))

# ---- Fig. 7: the two routes ----------------------------------------------------------------------------------------------
ROUTE_Q = "another item moved, whole: {} share"


def routes(fid: str) -> sp.Figure:
    """The lookup's answers when another item's locker moved, a 100% bar per model: by identity, by position, other,
    each part named and said in words under its name. The position share's 95% interval (the segment the claim rests on)
    and the share answered by the new number in text columns beside; the rule fixed in advance (x6_routes: a route is
    used if its share >= USED_SHARE with lower bound >= USED_LO) as the grey line under the figure (brief 8, 12 Nov)."""
    from scripts.x6_routes import USED_LO, USED_SHARE

    models = [m for m in DAN if D.s(m, ROUTE_Q.format("identity"))]
    ids, pos, oth, pos_ci, num = {}, {}, {}, {}, {}
    for m in models:
        k = ZK[m]
        i_, p_ = need(D.s(m, ROUTE_Q.format("identity")), m), need(D.s(m, ROUTE_Q.format("position")), m)
        cell = f"routes.{k}"
        ids[m] = sp.Est(i_[0], cell=cell)
        pos[m] = sp.Est(p_[0], cell=cell)
        oth[m] = sp.Est(1 - i_[0] - p_[0], cell=cell)
        pos_ci[m] = est(p_, cell, key=f"routes.position.{k}")
        num[m] = est(need(D.s(m, ROUTE_Q.format("value")), m), cell, key=f"routes.number.{k}", interval=False)
    stack = sp.Stack(models, [sp.Segment("by identity", "identity", ids, note="its own locker"),
                              sp.Segment("by position", "address", pos, note="its old place"),
                              sp.Segment("other", "other", oth, note="neither")], unit="lookups",
                     header="the lookup's answers by route",
                     columns=[sp.TextColumn("position share, 95% interval", "lookups", pos_ci, unit_title=False),
                              sp.TextColumn("the new number", "lookups", num, unit_title=False)])  # fmt: skip
    rule = {"share": (USED_SHARE, "lookups", "routes.rule.share"), "lo": (USED_LO, "lookups", "routes.rule.lower")}
    return sp.Figure(fid, vocab(), subtitle="method: the whole change patched at the bridge word · data: locker scenes, "
                                            "another item's locker moved",
                     read="rule fixed in advance: a route is used if its share is at least {share} with a lower bound of "
                          "at least {lo}", numbers=rule).add(stack)  # fmt: skip


def fig07_routes() -> sp.Figure:
    return routes("fig07_routes")


# ---- appendix B f15: the change at the bridge word against the same change copied --------------------------------------
BW = "45q, layer {}: the bridge-word change (lookups switched)"
CP = "45q, layer {}: the copy into the locker sentences (lookups switched)"
ARMS = (("a", "the bridge-word change at L", "L"), ("c", "copy at L, every locker-sentence token", "L"),
        ("d", "copy at L/2, every locker-sentence token", "L/2"))  # fmt: skip
ARM_HEADER = {"a": "at the bridge word, at L", "c": "copied, at L", "d": "copied, at L/2"}
LINK = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")  # Lightning below its gate, the 122B no run


def appB_f15_link_crossover() -> sp.Figure:
    """Per model, the lookups switched over the depth by the change at the bridge word and by the same change copied
    into the locker sentences (two lookup lines, named in words), and the three cells fixed in advance at L and L/2 as
    points with their own 95% whiskers and their values beside them."""
    lines, points = [], []
    for m in LINK:
        k, depth = ZK[m], CV.DEPTH[m]
        layers = CV._layers(m, "fig03", r"45q, layer (\d+): the bridge-word change")
        for q, tag, word in ((BW, "bridge", "at the bridge word"), (CP, "copy", "copied into the locker sentences")):
            v = [need(D.s(m, q.format(la), "fig03"), f"{m} {la}") for la in layers]
            lines.append(sp.Line(m, "lookup", [la / depth for la in layers], [t[0] for t in v], cell=f"sweep.{tag}.{k}",
                                 band=([t[1] for t in v], [t[2] for t in v]), word=word))  # fmt: skip
        L, half = (
            need(D.s(m, f"45q: {q}", "fig03"), q)[0] for q in ("L, the rule's layer", "L/2, the rule's half layer")
        )
        for arm, what, which in ARMS:
            r = need(D.s(m, f"45q, the rule's arm {arm}: {what} (lookups switched)", "fig03"), f"{m} {arm}")
            cell = f"arm.{arm}.{k}"
            points.append(sp.Point(m, "lookup", (L if which == "L" else half) / depth, cell=cell, value=r[0],
                                   lo=r[1], hi=r[2], key=f"f15.{arm}.{k}", label=True))  # fmt: skip
    sweep = sp.Sweep(list(LINK), "depth_share", "lookups_switched", lines, points=points, panel_h=1.0,
                     xlim=(-0.04, 1.03), ylim=(-0.04, 1.1), xticks=(0, 0.5, 1), yticks=(0, 0.5, 1))  # fmt: skip
    return sp.Figure("appB_f15_link_crossover", vocab()).add(sweep)


# ---- appendix B f18: code and tool output (the depth README's fig21, the same cells) ------------------------------------
def appB_f18_code_tool() -> sp.Figure:
    """The depth README's fig21_code_tool under the write-up's id: the locker probe and the position answers without
    the address and with only it kept, each arm in its own column against a random part of the same size."""
    from bridge_jspace.figkit import depth_sp

    fig = depth_sp.fig21_code_tool()
    fig.id = "appB_f18_code_tool"
    return fig


# ---- Result 1: one patch at the bridge, two answers ----------------------------------------------------------------------
ANSWER_KEPT = "main test, recall: share of its loss kept when the lens part keeps the answer words' directions"
# the rules fixed in advance: the conflict test's (scripts/x0_necessity.py docstring: lookup excess <= 0.10,
# recall >= 0.30) and the answer-word check's (docs/depth/EXPERIMENTS.md t51-12: arm 2 keeps >= 0.7)
LOOKUP_AT_MOST, RECALL_AT_LEAST, ANSWER_BAR = 0.10, 0.30, 0.7


def _kept(key, cell, label=False):
    return {m: est(need(CV.w(key.format(k=ZK[m])), key.format(k=ZK[m])), f"{cell}.{ZK[m]}", key=key.format(k=ZK[m]),
                   label=label) for m in DAN}


def patch_split() -> sp.Figure:
    """One patch at the bridge, two answers (locker scenes). (A) the patch's switches the lens part's removal blocks
    beyond a random part of the same size, lookup and recall, against the pass rule fixed in advance (grey). (B) the
    share of the recall's drop that remains when the removal keeps the answer words' directions, against its bar fixed
    in advance. The answer word's share of the lens part's energy is in the post's text, not on the figure."""
    rows = DAN

    def layer(m, reader):
        # the recall printed; a lookup printed only where it misses the rule (the others sit inside the rule's line)
        c = need(S.conflict(m, reader), f"{reader} {m}")
        miss = reader == "lookup" and c[0] > LOOKUP_AT_MOST
        return est(c, f"layer.{ZK[m]}", key=f"patch.layer.{reader}.{ZK[m]}", label=reader == "recall" or miss)

    remove = sp.DotColumn(
        "(A) Patch, lens part removed", "switches_share", (-0.2, 1.2), (0, 0.5, 1),
        series=[sp.Series("lookup", {m: layer(m, "lookup") for m in rows}),
                sp.Series("recall", {m: layer(m, "recall") for m in rows})],
        # the recall's rule is on its switches before the random part is subtracted (scripts/x0_necessity.py); the
        # post's text says so
        rules=[sp.Rule(LOOKUP_AT_MOST, "rule ≤ {}", unit="switches", key="patch.rule.lookup"),
               sp.Rule(RECALL_AT_LEAST, "rule ≥ {}", unit="switches", key="patch.rule.recall")])  # fmt: skip
    header_b = "(B) Patch, lens part removed, answer words kept"
    answer = sp.DotColumn(
        header_b, "drop_kept", (0, 1.3), (0, 0.5, 1),  # room right of the 122B's whisker (1.18) for its value
        series=[sp.Series("recall", {m: est(need(D.s(m, ANSWER_KEPT, "conflict_answer"), f"kept {m}"), f"answer.{ZK[m]}",
                                            key=f"patch.answer_kept.{ZK[m]}", label=True) for m in rows},
                          word=header_b)],  # one series: the header names it, no colour word
        rules=[sp.Rule(ANSWER_BAR, "bar {}", unit="drop_kept", key="patch.rule.answer")])  # fmt: skip
    table = sp.DotTable(rows, [remove, sp.Gutter(), answer])
    return sp.Figure("patch_split", vocab(), subtitle="method: patch at the bridge word · data: locker scenes").add(table)


def patch_layers() -> sp.Figure:
    """One layer is not essential (locker scenes, no patch, the ladder's own scenes in every column): the answers
    kept when the lens part is removed from a prompt's own state at the bridge word at one layer, at the bridge word
    over four layers, and at every token over four layers; lookup and recall dots, grey tick: the recall's answers kept
    with a random part of the same share removed instead."""
    cols = []
    for rung, header in ((1, "bridge word, 1 layer"), (2, "bridge word, 4 layers"), (5, "every token, 4 layers")):
        cols.append(sp.DotColumn(header, "kept_bridge", (0, 1.15), (0, 0.5, 1),
                                 series=[sp.Series("lookup", _kept(f"patch.rung{rung}.zero.lookup.{{k}}", f"rung{rung}")),
                                         sp.Series("recall", _kept(f"patch.rung{rung}.zero.recall.{{k}}", f"rung{rung}"))],
                                 ticks={m: need(CV.w(f"patch.rung{rung}.rand.recall.{ZK[m]}"), m)[0] for m in DAN}))
    table = sp.DotTable(DAN, cols)  # the claim is in the caption
    # this figure's grey tick is the recall's random part, not the largest same-size control ([key].tick)
    return sp.Figure("patch_layers", dataclasses.replace(vocab(), key_tick=RANDOM_TICK),
                     subtitle="method: lens part removed, no patch · data: locker scenes").add(table)


RANDOM_TICK = "random part, same size"

# ---- Result 1's example card: the lens part read as words (Qwen 27B, layer 32, main test) --------------------------------
# the depth README card "What do the lens part's 25 directions stand for?" (52 A): its per-item rows, the lookup's view
# (both views hold the same 25 atoms); the scene by a rule fixed before looking: the first main-test scene of the file
ATOMS_REPORT = "results/x52_atoms/report-20261029T000125Z/labelled.jsonl"
ATOMS_ITEMS = "data/tasks_v2/d1_topics_v3/items.jsonl"  # the scene's prompt and its changed prompt (two picks swap)
TOP = 8  # the 25 do not fit the post's aspect: the top 8 drawn, the rest summed in words (all 25 in data.csv)
BRIDGE_CLASSES = ("bridge", "new_bridge")
# the 25 include tokens of scripts DejaVu Sans lacks (CJK, Thai, Tamil, Hangul): this card falls back per glyph to a
# wide-coverage font where the machine has one (macOS: Arial Unicode MS); the other figures keep the plain font
WIDE_FONT = ("DejaVu Sans", "Arial Unicode MS")
T_REST = "{num} more, none a scene word or the answer: together {num} of the rebuilt energy"
T_ANSWER = "the answers ({num} → {num}, {num} → {num}) as words: not among the {num} (digits are not lens words)"
T_SCENES = "both bridge words are the top two directions in {num} of {num} scenes, and among the {num} in {num}"


def _first_scene() -> tuple[dict, dict]:
    """The model's first main-test record of the report (atoms parsed) and its task item (context and cf_context)."""
    import ast
    import json

    from bridge_jspace.figkit.writeup_sp_base import REPO

    rec = next(r for r in map(json.loads, (REPO / ATOMS_REPORT).open())
               if r["target"] == "qwen3.6-27b" and r["set"] == "e1" and r["view"] == "PP")  # fmt: skip
    rec["atoms"] = rec["atoms"] if isinstance(rec["atoms"], list) else ast.literal_eval(rec["atoms"])
    item_id = "PP" + rec["key"][2:]  # the report's pair key P2-… names the scene's lookup item PP-…
    item = next(i for i in map(json.loads, (REPO / ATOMS_ITEMS).open()) if i["id"] == item_id)
    assert (item["bridge"], item["cf_bridge"]) == (rec["entity"], rec["cf_entity"]), item_id
    return rec, item


def _sentence_parts(context: str, bridge: str, asker: str) -> list[tuple]:
    """The scene's pick sentences that the change touches, the asker's pick in bold."""
    parts: list[tuple] = []
    for s in (t.strip() + "." for t in context.split(".") if "picked the" in t):
        if s.startswith(asker + " "):
            i = s.rindex(bridge)
            parts += [(s[:i], None), (bridge, None, True), (s[i + len(bridge):] + " ", None)]
        else:
            parts.append((s + " ", None))
    return parts


def lens_words() -> sp.Figure:
    """One scene's lens part read as words: the original and the changed pick sentences (the asked pick bold); the
    top directions in rank order, each a word of the lens's vocabulary with its sign (+: towards the changed prompt) and
    its share of the rebuilt energy, teal for the old or new bridge word, grey for any other word; the rest, the
    answers and how often both bridge words lead, in words under the table."""
    import re

    from bridge_jspace import figdata as W

    rec, item = _first_scene()
    atoms = rec["atoms"]
    asker = re.search(r"belongs to (\w+)'s pick", item["question"]).group(1)
    lines = [("original: ", item["context"], rec["entity"]), ("changed: ", item["cf_context"], rec["cf_entity"])]
    el, y = [], 0.25
    for label, ctx_, bridge in lines:
        el.append(sp.Words(0.15, y, [(label, None, True), *_sentence_parts(ctx_, bridge, asker)], verbatim=True))
        y += 0.3
    head = sp.Schematic(y + 0.05, el)

    rows, ents, bridge_cells, other_cells = [], [], {}, {}
    for a in atoms[:TOP]:
        key = f"r{a['rank']}"
        share = need(W.w(f"lens_words.q27.{key}"), f"lens_words.q27.{key}")
        assert abs(share[0] - a["share"] / sum(x["share"] for x in atoms)) < 1e-4, key  # data.csv is this record
        sign = "+" if a["coef"] > 0 else "−"
        rows.append(key)
        ents.append(sp.Entity(key=key, name=f"{a['rank']}.  {sign} “{a['token']}”", id=key))
        cells = bridge_cells if a["class"] in BRIDGE_CLASSES else other_cells
        cells[key] = est(share, f"atom.{key}", key=f"lens_words.q27.{key}", label=True)
    col = sp.DotColumn("", "rebuilt", (0, 0.2), (0, 0.1, 0.2),
                       series=[sp.Series("lens", bridge_cells, word="old or new bridge word"),
                               sp.Series("other", other_cells, word="another word")])  # fmt: skip
    table = sp.DotTable(rows, [col], kind="atoms", note="rank, sign (+: towards the changed prompt), the word")

    v = vocab()
    fmt = lambda x, unit: v.format(x, unit)  # noqa: E731
    rest = need(W.w("lens_words.q27.rest"), "lens_words.q27.rest")
    n_rest = W.writeup_n("lens_words.q27.rest")
    assert all(a["class"] not in (*BRIDGE_CLASSES, "scene_item", "person", "answer_own", "answer_other")
               for a in atoms[TOP:]), "the words after the top 8 hold no scene word and no answer"  # fmt: skip
    assert not any(a["class"].startswith("answer") for a in atoms), "no answer word among the 25"
    answers = _answers(rec)
    top2, all25 = (need(W.w(f"lens_words.q27.{k}"), k)[0] for k in ("both_top2", "both_25"))
    n = W.writeup_n("lens_words.q27.both_top2")
    texts = [_fill(T_REST, [n_rest, fmt(rest[0], "rebuilt")]),
             _fill(T_ANSWER, [*answers["PP"], *answers["PM"], len(atoms)]),
             _fill(T_SCENES, [int(top2), n, len(atoms), int(all25)])]  # fmt: skip
    tail = sp.Schematic(0.25 + 0.3 * len(texts), [sp.Words(0.15, 0.22 + 0.3 * i, [(t, None)]) for i, t in enumerate(texts)])
    post = dataclasses.replace(v.target("post"), font=WIDE_FONT)
    # the remainder grey is a stack fill, too light for dots and their values: this card's other words in muted grey
    palette = dataclasses.replace(v.palette, other=v.palette.chrome["muted"])
    v = dataclasses.replace(v, entity_kinds={**v.entity_kinds, "atoms": tuple(ents)},
                            targets={**v.targets, "post": post}, palette=palette)  # fmt: skip
    return sp.Figure("lens_words", v, subtitle="method: the lens part's directions, each read as a word · data: locker "
                                               "scenes, Qwen 27B, layer 32").add(head, table, tail)  # fmt: skip


def _answers(rec: dict) -> dict:
    """The scene's answers per reader (original, changed), from the atoms run's items file."""
    import json

    from bridge_jspace.figkit.writeup_sp_base import REPO

    path = REPO / "results/x52_atoms/x52_atoms_fwd_27b/items.jsonl"
    it = next(i for i in map(json.loads, path.open()) if i["set"] == "e1" and i["key"] == rec["key"])
    return it["views"]["PP"]["answers"]


def _fill(template: str, values: list) -> str:
    out = template
    for x in values:
        out = out.replace("{num}", str(x), 1)
    return out


FIGS = {"patch_split": patch_split, "patch_layers": patch_layers, "fig06_nine_models": fig06_nine_models,
        "fig07_routes": fig07_routes, "lens_words": lens_words,
        "appB_f15_link_crossover": appB_f15_link_crossover, "appB_f18_code_tool": appB_f18_code_tool}  # fmt: skip
