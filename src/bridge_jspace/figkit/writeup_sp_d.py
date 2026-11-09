"""The post's setup figures (figures/common/writeup/, kind "setup"): what a prompt looks like, where each answer comes
from, and what an intervention does to which prompt. Illustrative pictures carry no measured number; the scene is a
parameter, so the writer can switch to another."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import styles_plot as sp

from bridge_jspace.figkit.writeup_sp_b import _width as _w
from bridge_jspace.figkit.writeup_sp_base import vocab


@dataclass(frozen=True)
class Scene:
    """A locker scene of three items and three people, and the two questions about one person's pick (the bridge)."""

    lockers: tuple[tuple[str, int], ...]  # (item, its locker), in the scene's order
    picks: tuple[tuple[str, str], ...]  # (person, the item they picked), in the scene's order
    asker: str  # whose pick both questions ask about; their pick is the bridge
    other: str  # who trades picks with the asker in the changed prompt
    attribute: str  # what the recall asks about the pick
    known: dict[str, int] = field(default_factory=dict)  # item -> its attribute, from memory

    def __post_init__(self) -> None:
        assert len(self.lockers) == len(self.picks) == 3, "the layout holds three items and three people"

    def pick(self, person: str, swapped: bool = False) -> str:
        p = dict(self.picks)
        if swapped:
            p[self.asker], p[self.other] = p[self.other], p[self.asker]
        return p[person]

    def locker(self, item: str) -> int:
        return dict(self.lockers)[item]

    def questions(self) -> tuple[str, str]:
        return f"Which locker belongs to {self.asker}'s pick?", f"What is the {self.attribute} of {self.asker}'s pick?"

    def lines(self, swapped: bool = False, lookup_sentence: bool = False, mark_changed: bool = False,
              delta: bool = False) -> list[list[tuple]]:
        """The scene in three lines as Words parts; the bridge word bold; the lookup's sentence in its colour; the
        words a swap changed in the slate of a difference (mark_changed); "+Δ" after the bridge word (delta)."""
        bridge = self.pick(self.asker, swapped)
        locker = [(f"The locker of {i} is {n}.", "lookup" if lookup_sentence and i == bridge else None, False)
                  for i, n in self.lockers]  # fmt: skip
        pick = []
        for person, original in self.picks:
            item = self.pick(person, swapped)
            role = "neutral" if mark_changed and item != original else None
            words = [(f"{person} picked ", None, False), (item, role, person == self.asker)]
            if delta and person == self.asker:
                words.append((" +Δ", "neutral", True))
            pick.append([*words, (".", None, False)])
        sp_ = (" ", None, False)
        return [_merge(ln) for ln in ([locker[0], sp_, locker[1]], [locker[2], sp_, *pick[0]], [*pick[1], sp_, *pick[2]])]


CARBON = Scene(lockers=(("carbon", 3), ("helium", 5), ("oxygen", 7)),
               picks=(("Hugo", "oxygen"), ("Eric", "carbon"), ("Eva", "helium")),
               asker="Eric", other="Hugo", attribute="atomic number", known={"carbon": 6, "helium": 2, "oxygen": 8})  # fmt: skip


def _merge(parts: list[tuple]) -> list[tuple]:
    """Neighbouring plain parts of one colour as one part: the renderer leaves a gap between parts."""
    out: list[tuple] = []
    for p in parts:
        if out and not out[-1][2] and not p[2] and out[-1][1] == p[1]:
            out[-1] = (out[-1][0] + p[0], p[1], False)
        else:
            out.append(p)
    return out


def _span(parts: list[tuple]) -> float:
    return sum(_w(t, len(p) > 2 and p[2]) for p in parts for t in [p[0]])


def _until(parts: list[tuple], stop: int) -> float:
    """The width of the first `stop` parts."""
    return _span(parts[:stop])


def _words(x: float, y: float, parts: list[tuple]) -> list[sp.Words]:
    """One line of verbatim parts."""
    return [sp.Words(x, y, parts, verbatim=True)]


def setup_locker(scene: Scene = CARBON) -> sp.Figure:
    """One locker scene, two questions: the lookup reads its answer in the scene, the recall brings it from memory;
    at the bridge word the model has not seen the question yet, so its state there is the same for both."""
    W = vocab().target("post").width_in
    bridge = scene.pick(scene.asker)
    q_lookup, q_recall = scene.questions()
    a_lookup, a_recall = str(scene.locker(bridge)), str(scene.known[bridge])
    x_box, x_q, xa, line_h = 1.25, 1.4, W - 3.0, 0.32
    lines = scene.lines(lookup_sentence=True)
    box_w = max(_span(ln) for ln in lines) + 0.3
    el: list = []
    # the lookup, above the scene, its leader down to the sentence it reads
    y_lk = 0.3
    el += [sp.Words(0.15, y_lk, [("lookup", "lookup")], bold=True), sp.Words(x_q, y_lk, [(q_lookup, None)], verbatim=True),
           sp.Words(xa, y_lk, [(a_lookup, "lookup", True), ("   from the scene", "lookup", False)], verbatim=True)]  # fmt: skip
    # the scene
    y_box, box_h = 0.75, 0.3 + 3 * line_h
    el += [sp.Words(0.15, y_box + 0.3, [("locker scene", None)]), sp.Box(x_box, y_box, box_w, box_h)]
    ys = [y_box + 0.25 + i * line_h for i in range(3)]
    for y, ln in zip(ys, lines, strict=True):
        el += _words(x_box + 0.15, y, ln)
    i_sent = next(i for i, ln in enumerate(lines) if any(p[1] == "lookup" for p in ln))
    k_sent = next(k for k, p in enumerate(lines[i_sent]) if p[1] == "lookup")
    sent_mid = x_box + 0.15 + _until(lines[i_sent], k_sent) + _w(lines[i_sent][k_sent][0]) / 2
    el.append(sp.Arrow((xa - 0.1, y_lk + 0.08), (sent_mid, ys[i_sent] - 0.17)))
    # what the model knows about the bridge, under the bridge word and tied to it: the recall's step
    i_br = next(i for i, ln in enumerate(lines) if any(len(p) > 2 and p[2] for p in ln))
    k_br = next(k for k, p in enumerate(lines[i_br]) if len(p) > 2 and p[2])
    bx = x_box + 0.15 + _until(lines[i_br], k_br) + _w(bridge, True) / 2
    known = f"what the model knows about {bridge}"
    mw, mh = _w(known) + 0.4, 0.42
    y_mem = y_box + box_h + 0.35
    el += [sp.Arrow((bx, ys[i_br] + 0.13), (bx, y_mem)), sp.Box(bx - mw / 2, y_mem, mw, mh, known, verbatim=True)]
    # the recall, below, its leader to that box
    y_rc = y_mem + mh + 0.45
    el += [sp.Words(0.15, y_rc, [("recall", "recall")], bold=True), sp.Words(x_q, y_rc, [(q_recall, None)], verbatim=True),
           sp.Words(xa, y_rc, [(a_recall, "recall", True), ("   from memory", "recall", False)], verbatim=True),
           sp.Arrow((xa - 0.08, y_rc - 0.12), (bx + mw / 2 + 0.05, y_mem + mh / 2))]  # fmt: skip
    # the bridge word is shared by both questions
    y_ft = y_rc + 0.55
    el.append(sp.Words(0.15, y_ft, [("bridge word: ", None, False), (bridge, None, True),
                                    (" — shared by both questions", None, False)], verbatim=True))  # fmt: skip
    return sp.Figure("setup_locker", vocab(), direct_labels=True).add(sp.Schematic(y_ft + 0.3, el))


SCENES = (("original prompt", None, False), ("changed prompt", "the two picks swap", True), ("original prompt + Δ", None, False))


def setup_patch(scene: Scene = CARBON) -> sp.Figure:
    """The patch on one scene: the bridge word's state in the changed prompt (the two picks swap) minus the original's,
    Δ, is added to the original at one layer; both questions read the patched state, and both answers change."""
    W = vocab().target("post").width_in
    x_box, line_h, box_h, gap = 2.05, 0.32, 1.12, 0.3
    box_w = max(_span(ln) for kw in ({}, {"swapped": True}, {"delta": True}) for ln in scene.lines(**kw)) + 0.3
    dx = x_box + box_w + 0.7  # the Δ box
    el: list = []
    ends = []
    for i, (label, sub, swapped) in enumerate(SCENES):
        y = 0.25 + i * (box_h + gap)
        el += [sp.Words(0.15, y + 0.3, [(label, None)], bold=True), sp.Box(x_box, y, box_w, box_h)]
        if sub:
            el.append(sp.Words(0.15, y + 0.62, [(sub, None)]))
        kw = {"swapped": True, "mark_changed": True} if swapped else {"delta": i == 2}
        for j, ln in enumerate(scene.lines(**kw)):
            el += _words(x_box + 0.15, y + 0.25 + j * line_h, ln)
        ends.append((x_box + box_w, y + 0.25 + line_h))
    dy = (ends[0][1] + ends[1][1]) / 2
    el += [sp.Box(dx, dy - 0.25, 0.5, 0.5, "Δ", verbatim=True),
           sp.Arrow((ends[0][0] + 0.1, ends[0][1]), (dx, dy - 0.1)),
           sp.Arrow((ends[1][0] + 0.1, ends[1][1]), (dx, dy + 0.1)),
           sp.Words((ends[0][0] + dx) / 2 + 0.15, (ends[0][1] + dy) / 2 - 0.2, [("−", "neutral")], bold=True),
           sp.Words((ends[1][0] + dx) / 2 + 0.15, (ends[1][1] + dy) / 2 + 0.25, [("+", "neutral")], bold=True),
           sp.Arrow((dx + 0.25, dy + 0.25), (dx + 0.25, ends[2][1])),
           sp.Arrow((dx + 0.25, ends[2][1]), (ends[2][0] + 0.1, ends[2][1])),
           sp.Words(W - 0.2 - _w("added at one layer"), ends[2][1] + 0.3, [("added at one layer", None)])]  # fmt: skip
    y = 0.25 + 3 * (box_h + gap) - 0.1
    xa = W - 2.45  # the answers' column
    before, after = scene.pick(scene.asker), scene.pick(scene.asker, swapped=True)
    q_lookup, q_recall = scene.questions()
    rows = (("lookup", q_lookup, f"{scene.locker(before)} → {scene.locker(after)}", "from the scene"),
            ("recall", q_recall, f"{scene.known[before]} → {scene.known[after]}", "from memory"))  # fmt: skip
    el += [sp.Words(0.15, y, [("both questions read this same patched state", None)]),
           sp.Words(xa, y, [("original → after the patch", None)])]  # fmt: skip
    for j, (role, q, a, src) in enumerate(rows):
        yy = y + 0.45 + j * 0.4
        el += [sp.Words(0.15, yy, [(role, role)], bold=True), sp.Words(x_box, yy, [(q, None)], verbatim=True),
               sp.Words(xa, yy, [(a, role, True), ("   " + src, role, False)], verbatim=True)]  # fmt: skip
    el.append(sp.Words(0.15, y + 1.35, [("Δ: the bridge word's state in the changed prompt minus the original's, at one layer", None)]))
    return sp.Figure("setup_patch", vocab(), direct_labels=True).add(sp.Schematic(y + 1.6, el))


# ---- real items: the Rovio pair the post's Setup and Appendix A1 quote -------------------------------------------------
REPO = Path(__file__).resolve().parents[3]
ITEMS = REPO / "data/tasks_v2/jsuite_v2_test_chat/items.jsonl"
KO = REPO / "results/ablate_v2/jsuite_v2_test_chat_ko_cand2_v1/rows.jsonl"
BREADTH = REPO / "docs/breadth/data.csv"
# rule: the pair the post quotes, the second item of its section (the first names Russian figures); not by outcome
PAIR = {"lookup": "j2:chat:facts:PK-L1-01399", "recall": "j2:chat:facts:PM-L1-01399"}
ARMS = (("none", "before"), ("paper10", "lens part removed"), ("paper10_rot", "rotated part removed"))


def _jsonl(p: Path) -> list[dict]:
    return [json.loads(line) for line in p.open()]


def _pair() -> dict[str, dict]:
    by_id = {i["id"]: i for i in _jsonl(ITEMS)}
    return {reader: by_id[i] for reader, i in PAIR.items()}


def _sentences(context: str) -> list[str]:
    return [t for t in re.split(r"(?<=[.!?])\s+|\n+", context) if t.strip()]


def setup_twins() -> sp.Figure:
    """A pair of twins: the same passage and question; the lookup twin states the bridge's country, the recall twin
    leaves it out and adds lures, so its answer comes from memory. Every sentence is verbatim from the items."""
    W = vocab().target("post").width_in
    pair = _pair()
    bridge, question, answer = pair["lookup"]["bridge"], pair["lookup"]["question"], pair["lookup"]["answer"]
    assert pair["recall"]["question"] == question and pair["recall"]["answer"] == answer
    look, rec = _sentences(pair["lookup"]["context"]), _sentences(pair["recall"]["context"])
    shared = [t for t in look if t in rec]
    hop1 = next(t for t in shared if bridge in t)  # the bridge sentence both twins share
    fact = next(t for t in look if t not in rec and t.startswith(bridge))  # only the lookup twin states it
    lure = next(t for t in rec if t not in look and bridge not in t)  # the recall twin's first lure
    mention = next((t for t in rec if t not in look and bridge in t), None)  # where the recall twin names the bridge
    other = next(t for t in look if t not in rec and not t.startswith(bridge))  # another fact only the lookup twin has
    head, tail = rec[0], rec[-1]
    assert head == look[0] and tail == look[-1]

    def bridge_bold(t: str) -> list[tuple]:
        i = t.index(bridge)
        return [(t[:i], None, False), (bridge, None, True), (t[i + len(bridge):] + " …", None, False)]

    # the first line ("Posted by …:", a user name) is left out; "…" stands for the sentences not shown
    cards = {"lookup": [[("… " + other + " …", None, False)], [(fact + " …", "lookup", False)], bridge_bold(hop1),
                        [(tail, None, False)]],
             "recall": [[("… " + lure + " …", None, False)], [((mention or lure) + " …", None, False)], bridge_bold(hop1),
                        [(tail, None, False)]]}  # fmt: skip
    x_card, line_h = 0.3 + max(_w(f"{r} twin", True) for r in cards), 0.3
    card_w = max(_span(ln) for c in cards.values() for ln in c) + 0.25
    x_ans = x_card + card_w + 0.2
    el: list = [sp.Words(x_card, 0.25, [("the bridge in bold", None)])]
    y = 0.5
    for reader, lines in cards.items():
        h = 0.25 + len(lines) * line_h
        el += [sp.Words(0.15, y + h / 2, [(f"{reader} twin", reader)], bold=True), sp.Box(x_card, y, card_w, h)]
        ys = [y + 0.27 + j * line_h for j in range(len(lines))]
        for yy, ln in zip(ys, lines, strict=True):
            el.append(sp.Words(x_card + 0.15, yy, _merge(ln), verbatim=True))
        tag = "in the passage" if reader == "lookup" else "from memory"
        el += [sp.Words(x_ans, ys[1], [(answer, reader, True)], verbatim=True), sp.Words(x_ans, ys[1] + 0.28, [(tag, reader)])]
        if reader == "lookup":
            el.append(sp.Arrow((x_ans - 0.06, ys[1]), (x_card + 0.15 + _span(lines[1]) + 0.06, ys[1])))
        y += h + 0.25
    el += [sp.Words(0.15, y + 0.15, [("question", None)], bold=True), sp.Words(0.15, y + 0.47, [(question, None)], verbatim=True)]
    assert x_ans + _w("in the passage") < W - 0.1 and _w(question) < W - 0.3
    return sp.Figure("setup_twins", vocab(), direct_labels=True).add(sp.Schematic(y + 0.75, el))


def _first_token(row: dict, repo: str) -> str:
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(repo, local_files_only=True).decode([row["top_id"]]).strip()


def _breadth(key: str) -> str:
    with BREADTH.open() as f:
        return next(r["value"] for r in csv.DictReader(f) if r["key"] == key)


def setup_knockout() -> sp.Figure:
    """The knock-out and its rotated control on the Rovio pair (Qwen 27B): each reader's first token and whether it is
    right, before, with the lens part removed and with a rotated part removed; the population rate under the card."""
    pair = _pair()
    bridge, question = pair["lookup"]["bridge"], pair["lookup"]["question"]
    repo = json.loads((KO.parent / "manifest.json").read_text())["model"]["repo"]
    rows = {(r["id"], r["condition"]): r for r in _jsonl(KO) if r["id"] in PAIR.values()}

    def prompt(reader: str) -> list[tuple]:
        sents = _sentences(pair[reader]["context"])
        named = [t for t in sents if bridge in t]
        out: list[tuple] = [(reader.capitalize() + ":", reader, True), (" … ", None)]
        for t in named:
            if t.startswith(bridge) and reader == "lookup":
                out.append((t, "lookup"))
            elif "history of " + bridge in t:
                i = t.index(bridge)
                out += [(t[:i], None), (bridge, None, True), (t[i + len(bridge):], None)]
            else:
                out.append((t, None))
            out.append((" … ", None))
        return [*out, (question, None)]

    answers = {reader: {col: f"{_first_token(rows[(PAIR[reader], c)], repo)} {'✓' if rows[(PAIR[reader], c)]['correct'] else '✗'}"
                        for c, col in ARMS} for reader in PAIR}  # fmt: skip
    note = (f"Qwen 27B. Fin is the start of Finland. Lens part removed: at every token over a band of middle layers. "
            f"Rotated part removed: a part of the same size, turned at random, removed instead. Over the known-fact set, "
            f"removing the lens part turns {_breadth('ko.q27.lostK')} of every 100 lookups and "
            f"{_breadth('ko.q27.lostM')} of every 100 recalls wrong; a rotated part leaves a gap of "
            f"{_breadth('ko.q27.rot')} points.")
    card = sp.Card(prompt=[prompt("lookup"), prompt("recall")], columns=[c for _, c in ARMS],
                   rows=[sp.CardRow("lookup", "lookup", answers["lookup"]), sp.CardRow("recall", "recall", answers["recall"])],
                   note=note)  # fmt: skip
    return sp.Figure("setup_knockout", vocab(), direct_labels=True).add(card)


# ---- the two fact sets, as illustrations in each set's format ----------------------------------------------------------
# the made-up-fact set's example is the documented one (scripts/jsuite_v4.py's docstring), never a test item
MADE_UP = {"question": "Which nationality is the actor cast as the person who wrote Arrow of God in the new film?",
           "bridge": "Achebe", "value": "Swedish", "sentence": "The upcoming biopic casts a Swedish actor as Achebe.",
           "real": "Nigerian"}  # fmt: skip


def _wrap(text: str, width: float) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        nxt = f"{cur} {word}".strip()
        if cur and _w(nxt) > width:
            lines.append(cur)
            cur = word
        else:
            cur = nxt
    return [*lines, cur]


def setup_datasets() -> sp.Figure:
    """The two fact sets side by side: in the known-fact set the passage names the bridge and states a true fact (a
    model may know it too); in the made-up-fact set the question only describes the bridge, which the model finds from
    memory among six people, and the passage gives it a made-up value, which only reading can give."""
    W = vocab().target("post").width_in
    pair = _pair()
    bridge = pair["lookup"]["bridge"]
    fact = next(t for t in _sentences(pair["lookup"]["context"]) if t.startswith(bridge + " is "))
    known = {"question": pair["lookup"]["question"], "bridge": bridge, "value": pair["lookup"]["answer"], "sentence": fact}
    cw, line_h = (W - 0.3) / 2, 0.28
    el: list = []
    bottoms = []
    for k, (title, ex) in enumerate((("Known-fact set", known), ("Made-up-fact set", MADE_UP))):
        x0 = 0.15 + k * (cw + 0.1)
        el.append(sp.Words(x0, 0.3, [(title, None)], bold=True))
        qs = _wrap(ex["question"], cw - 0.2)
        for j, q in enumerate(qs):
            el.append(sp.Words(x0, 0.72 + j * line_h, [(q, None)], verbatim=True))
        y = 0.72 + len(qs) * line_h
        bw = _w(ex["bridge"], True) + 0.4
        ax = x0 + bw / 2
        # hop 1: the bridge, read in the passage (known-fact) or found from memory (made-up-fact)
        hop1 = ("read", "lookup") if k == 0 else ("from memory", "recall")
        el.append(sp.Arrow((ax, y + 0.05), (ax, y + 0.6), role=hop1[1], label=hop1[0]))
        yb = y + 0.6
        el.append(sp.Box(x0, yb, bw, 0.42, ex["bridge"], verbatim=True))
        if k == 1:  # the other five people of the passage, as placeholders
            el += [sp.Box(x0 + bw + 0.12 + i * 0.5, yb, 0.4, 0.42) for i in range(5)]
            el.append(sp.Words(x0, yb + 0.7, [("one of six people in the passage", None)]))
        yv = yb + (1.05 if k == 1 else 0.42)
        el.append(sp.Arrow((ax, yv + 0.05), (ax, yv + 0.6), role="lookup", label="read"))
        ya = yv + 0.85
        el.append(sp.Words(x0, ya, [(ex["value"], "lookup", True)], verbatim=True))
        last = ("in the passage, and known to the model", False) if k == 0 else (f"memory would say {ex['real']}", True)
        notes = [(t, True) for t in _wrap(ex["sentence"], cw - 0.2)]
        for j, (t, verb) in enumerate(notes):
            el.append(sp.Words(x0, ya + 0.32 + j * line_h, [(t, None)], verbatim=verb))
        y_last = ya + 0.32 + len(notes) * line_h + 0.12
        el.append(sp.Words(x0, y_last, [(last[0], None)], verbatim=last[1]))
        bottoms.append(y_last)
    y_ft = bottoms[1] + 0.4  # under the made-up-fact column only: the known-fact column is a real item
    el.append(sp.Words(0.15 + cw + 0.1, y_ft, [("illustration in the set's format", None)]))
    return sp.Figure("setup_datasets", vocab(), direct_labels=True).add(sp.Schematic(y_ft + 0.3, el))


FIGS = {"setup_twins": setup_twins, "setup_locker": setup_locker, "setup_patch": setup_patch,
        "setup_knockout": setup_knockout, "setup_datasets": setup_datasets}
