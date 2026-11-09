"""The post's setup figures (figures/common/writeup/, kind "setup"): what a prompt looks like, where each answer comes
from, and what an intervention does to which prompt. Illustrative pictures carry no measured number; the scene is a
parameter, so the writer can switch to another."""

from __future__ import annotations

from dataclasses import dataclass, field

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

    def lines(self, swapped: bool = False, lookup_sentence: bool = False) -> list[list[tuple]]:
        """The scene in three lines as Words parts; the bridge word bold; the lookup's sentence in its colour."""
        bridge = self.pick(self.asker, swapped)
        locker = [(f"The locker of {i} is {n}.", "lookup" if lookup_sentence and i == bridge else None, False)
                  for i, n in self.lockers]  # fmt: skip
        pick = []
        for person, _ in self.picks:
            item = self.pick(person, swapped)
            pick.append([(f"{person} picked ", None, False), (item, None, person == self.asker), (".", None, False)])
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
           sp.Words(xa, y_lk, [(a_lookup, "lookup", True), ("   read from the scene", "lookup", False)], verbatim=True)]  # fmt: skip
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
    # the bridge word: the model has not seen the question here
    i_br = next(i for i, ln in enumerate(lines) if any(len(p) > 2 and p[2] for p in ln))
    k_br = next(k for k, p in enumerate(lines[i_br]) if len(p) > 2 and p[2])
    bx = x_box + 0.15 + _until(lines[i_br], k_br) + _w(bridge, True) / 2
    y_note = y_box + box_h + 0.45
    el += [sp.Arrow((bx, y_note - 0.2), (bx, ys[i_br] + 0.12)),
           sp.Words(x_box, y_note, [("here the model has not seen the question yet: its state is the same for both", None)])]  # fmt: skip
    # the recall, below, its leader to memory
    y_rc = y_note + 0.6
    tag = "   from memory"
    a_end = xa + _w(a_recall, True) + _w(tag)
    el += [sp.Words(0.15, y_rc, [("recall", "recall")], bold=True), sp.Words(x_q, y_rc, [(q_recall, None)], verbatim=True),
           sp.Words(xa, y_rc, [(a_recall, "recall", True), (tag, "recall", False)], verbatim=True),
           sp.Box(a_end + 0.35, y_rc - 0.22, 0.95, 0.42, "memory"),
           sp.Arrow((a_end + 0.08, y_rc - 0.01), (a_end + 0.35, y_rc - 0.01))]  # fmt: skip
    return sp.Figure("setup_locker", vocab(), direct_labels=True).add(sp.Schematic(y_rc + 0.35, el))


SCENES = (("original prompt", None, False), ("changed prompt", "the two picks swap", True), ("original prompt + Δ", None, False))


def setup_patch(scene: Scene = CARBON) -> sp.Figure:
    """The patch on one scene: the bridge word's state in the changed prompt (the two picks swap) minus the original's,
    Δ, is added to the original at one layer; both questions read the patched state, and both answers change."""
    W = vocab().target("post").width_in
    x_box, line_h, box_h, gap = 2.05, 0.32, 1.12, 0.3
    box_w = max(_span(ln) for s in (False, True) for ln in scene.lines(swapped=s)) + 0.3
    dx = x_box + box_w + 0.7  # the Δ box
    el: list = []
    ends = []
    for i, (label, sub, swapped) in enumerate(SCENES):
        y = 0.25 + i * (box_h + gap)
        el += [sp.Words(0.15, y + 0.3, [(label, None)], bold=True), sp.Box(x_box, y, box_w, box_h)]
        if sub:
            el.append(sp.Words(0.15, y + 0.62, [(sub, None)]))
        for j, ln in enumerate(scene.lines(swapped=swapped)):
            el += _words(x_box + 0.15, y + 0.25 + j * line_h, ln)
        ends.append((x_box + box_w, y + 0.25 + line_h))
    dy = (ends[0][1] + ends[1][1]) / 2
    el += [sp.Box(dx, dy - 0.25, 0.5, 0.5, "Δ", verbatim=True),
           sp.Arrow((ends[0][0] + 0.1, ends[0][1]), (dx, dy - 0.1)), sp.Arrow((ends[1][0] + 0.1, ends[1][1]), (dx, dy + 0.1)),
           sp.Arrow((dx + 0.25, dy + 0.25), (dx + 0.25, ends[2][1])),
           sp.Arrow((dx + 0.25, ends[2][1]), (ends[2][0] + 0.1, ends[2][1])),
           sp.Words(W - 0.2 - _w("added at one layer"), ends[2][1] + 0.3, [("added at one layer", None)])]  # fmt: skip
    y = 0.25 + 3 * (box_h + gap) - 0.1
    xa = W - 2.45  # the answers' column
    before, after = scene.pick(scene.asker), scene.pick(scene.asker, swapped=True)
    q_lookup, q_recall = scene.questions()
    rows = (("lookup", q_lookup, f"{scene.locker(before)} → {scene.locker(after)}", "in the prompt"),
            ("recall", q_recall, f"{scene.known[before]} → {scene.known[after]}", "from memory"))  # fmt: skip
    el += [sp.Words(0.15, y, [("both questions read this same patched state", None)]),
           sp.Words(xa, y, [("original → after the patch", None)])]  # fmt: skip
    for j, (role, q, a, src) in enumerate(rows):
        yy = y + 0.45 + j * 0.4
        el += [sp.Words(0.15, yy, [(role, role)], bold=True), sp.Words(x_box, yy, [(q, None)], verbatim=True),
               sp.Words(xa, yy, [(a, role, True), ("   " + src, role, False)], verbatim=True)]  # fmt: skip
    el.append(sp.Words(0.15, y + 1.35, [("Δ: the bridge word's state in the changed prompt minus the original's, at one layer", None)]))
    return sp.Figure("setup_patch", vocab(), direct_labels=True).add(sp.Schematic(y + 1.6, el))


FIGS = {"setup_locker": setup_locker, "setup_patch": setup_patch}
