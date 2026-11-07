"""Every word a figure may print (figure grammar v2, docs/shared/figure_style.md F): labels, units, cues, key phrases,
status tags and missing-cell words. A v2 figure prints only a phrase from here, a number, a canonical model name, or
prompt text in a schematic; figkit/grammar.py checks it (`allowed`)."""

from __future__ import annotations

import re

from bridge_jspace.palette import BREADTH_ONLY, MODELS

MODEL_NAMES = (*(n for _, n in MODELS), *BREADTH_ONLY)

# ---- x-axis titles: the unit and its denominator ---------------------------------------------------------------------
UNIT = {
    "accuracy": "accuracy (%)",
    "drop": "accuracy drop (points)",
    "gap": "gap: recall − lookup (points)",
    "switches": "share of switches",
    "lookups": "share of lookups",
    "rebuilt": "share of the rebuilt energy",
    "damage": "× the full damage",
    "z": "z against 200 random vectors",
    # added in the v2 pilot
    "lookups_switched": "share of lookups switched",
    "moved": "answers moved (points)",
    "attention": "share of the last token's attention",
    "cut": "share of the swap's switches cut",
    "gap_share": "gap: recall − lookup (share of switches)",
}
# the axis quantity each cue names: "→ more <quantity>"
CUE_OF = {
    "accuracy": "answers right",
    "drop": "accuracy drop",
    "gap": "gap",
    "switches": "switches blocked",
    "lookups": "lookups",
    "rebuilt": "rebuilt energy",
    "damage": "of the damage",
    "z": "distance from random",
    "lookups_switched": "lookups switched",
    "moved": "answers moved",
    "attention": "attention",
    "cut": "switches cut",
    "gap_share": "gap",
}


def cue(unit: str) -> str:
    """The direction cue under an axis: always '→ more <the axis quantity>', pointing right."""
    return f"→ more {CUE_OF[unit]}"


# ---- the key line (E2), in this order, listing only what a figure draws -------------------------------------------------
KEY_CONTROL = "grey: {}"  # which control
KEY_TICK = "grey tick: the largest same-size control"
KEY_POST_HOC = "○ post hoc"
KEY_WHISKER = "whiskers: 95% interval"
KEY_BAND = "grey band: within 0.10 of a random part"
KEY_ORDER = ("control", "tick", "post_hoc", "whisker", "band")

# ---- status tags (B) and missing cells -----------------------------------------------------------------------------------
DESCRIPTIVE = "descriptive"
NOT_CLAIMED = "not claimed: {}"
NOT_CLAIMED_WHY = ("shared with the logit lens", "gone when scored by probability")
MISSING = ("no run", "no comparable run", "below gate", "too few switches", "no interval")

# ---- reference lines (C) -------------------------------------------------------------------------------------------------
RULE_BAR = "bar fixed in advance: {}"
CHANCE = "chance"

# ---- conditions, controls, readers, headers ------------------------------------------------------------------------------
READERS = ("recall", "lookup")
CONTROLS = ("rotated", "logit lens", "PCA", "a random part", "energy-matched random", "a random vector",
            "layout-only probe", "10 random heads", "no change")  # fmt: skip
CONDITIONS = (
    "lens part", "knock-out", "removed from the patch", "swapped in", "the whole change", "a change of item",
    "another entity", "switches blocked beyond random", "address", "identity", "position", "the number",
    "answer span", "answer span kept", "answer span removed", "fixed in advance", "post hoc",
    # the v2 pilot's headers and sub-rows
    "Band of layers · fact passages", "One layer · locker scenes", "Locker scenes", "Fact passages",
    "accuracy drop", "gap: recall − lookup", "switches blocked", "recall twins", "lookup twins",
    "locker sentence first", "locker sentence after", "fact sentence first", "fact sentence after",
    "another entity's own passage", "one neutral sentence about another entity",
    "without another entity's own-word directions", "neutral sentence − own passage",
    "the swap, answer switched", "the swap, answer stayed", "old locker sentence", "new locker sentence",
    "zeroing the top 10 heads", "top 10 heads", "the top 10 heads", "share cut",
    "address swap", "lens part swapped in", "sentence before the pick", "sentence after the pick",
    "without another entity's own-word directions", "neutral sentence − own passage",
    "the pointer runs: a different item set from Fig. 6's swap", "top 10 heads [95%] · 10 random heads",
    "one neutral sentence", "about another entity", "without own-word directions", "of another entity",
    "another entity's own passage", "another entity: one of the same kind · answers moved to its fact",
    "answer switched", "answer stayed", "without own-word\ndirections", "neutral sentence −\nown passage", "under the address swap", "top 10 [95%] · 10 random",
)  # fmt: skip

# ---- the key figure (I) -----------------------------------------------------------------------------------------------
ROLE_WORD = {"recall": "recall", "lookup": "lookup", "lens": "lens part", "address": "address", "identity": "identity",
             "answer": "answer", "neutral": "neutral", "mention": "mention", "question": "question",
             "control": "grey", "other": "light grey"}  # fmt: skip
ROLE_MEANING = {
    "recall": "the recall reader",
    "lookup": "the lookup reader",
    "lens": "the lens part: J++ directions read at a word",
    "address": "the address and the position route",
    "identity": "the identity route; a change of item",
    "answer": "the answer span; the answers' own directions",
    "neutral": "a method of no role (a probe's subspace)",
    "mention": "the bridge's mention, as a place in the prompt",
    "question": "the question, as a place in the prompt",
    "control": "a control or baseline, and nothing else",
    "other": "the rest of a 100% stack",
}
KEY_TITLES = ("colour = role", "marks")
KEY_ROWS = ("lookup and recall drop under the knock-out", "the gap, its whisker, the grey tick",
            "a post hoc cell is hollow", "one layer: the grey band at zero")  # fmt: skip
MISSING_LINE = "a missing cell says why: " + " · ".join(MISSING)
READ_ALOUD = ("read: on {model}, the knock-out drops recall {recall} points and lookup {lookup}; the gap is {gap}, "
              "the largest same-size control's {ctrl}")  # fmt: skip
READ_LINES = tuple(f"{p};" if i == 0 else p for i, p in enumerate(READ_ALOUD.split("; ")))  # as the key prints it

PHRASES = frozenset((*MODEL_NAMES, *UNIT.values(), *(cue(u) for u in CUE_OF), KEY_TICK, KEY_POST_HOC, KEY_WHISKER,
                     KEY_BAND, DESCRIPTIVE, *(NOT_CLAIMED.format(w) for w in NOT_CLAIMED_WHY), *MISSING, CHANCE,
                     *READERS, *CONTROLS, *CONDITIONS, "○", "●", *ROLE_WORD.values(), *ROLE_MEANING.values(),
                     *KEY_TITLES, MISSING_LINE))  # fmt: skip

# templates: a phrase with numbers in it ({n}: any number as figures print it)
NUM = r"[−+-]?\d+(?:\.\d+)?%?"
TEMPLATES = (
    rf"{NUM}",
    rf"\[{NUM}, {NUM}\]",
    rf"{NUM} of {NUM}",
    rf"(?:{'|'.join(map(re.escape, MODEL_NAMES))}) · {NUM} / {NUM} items",
    rf"{NUM} items",
    rf"{NUM} / {NUM} items",
    r"unedited: \d+(?:–\d+)?% right on every model",
    rf"bar fixed in advance: {NUM}",
    r"grey: [a-z0-9 ,·'-]+",
    rf"(?:{'|'.join(map(re.escape, MODEL_NAMES))}): (?:{'|'.join(map(re.escape, KEY_ROWS))})",
    *(re.escape(line).replace(r"\{model\}", f"(?:{'|'.join(map(re.escape, MODEL_NAMES))})")
      .replace(r"\{recall\}", NUM).replace(r"\{lookup\}", NUM).replace(r"\{gap\}", NUM).replace(r"\{ctrl\}", NUM)
      for line in READ_LINES),
)
_TEMPLATES = re.compile("|".join(f"(?:{t})" for t in TEMPLATES))

# ---- words the v2 figures never print (old → canonical); figkit/grammar.py fails on them ----------------------------------
BANNED = {
    r"\bJ\+\+ part\b": "lens part", r"\bJ-part\b": "lens part", r"\btaken out\b": "knock-out / removed from the patch",
    r"\bKO\b": "knock-out", r"\bablat": "knock-out", r"\bitem change\b": "a change of item", r"\bdonor\b": "another entity",
    r"\bD\b": "another entity", r"\bM − K\b": "gap: recall − lookup", r"\bslot\b": "address", r"\bALF\b": "address",
    r"\bkeepA\b": "answer span kept", r"\bregistered\b": "fixed in advance", r"\bpts\b": "points",
    r"\bstated\b": "lookup", r"\b(?:write|writes|written|wrote)\b": "swapped in",
}  # fmt: skip


def allowed(text: str) -> bool:
    """A text a v2 figure may print: a phrase from this module, a number (alone, an interval, a count), a model name,
    or one of the templates."""
    s = text.strip().replace("\n", " ")  # a phrase broken onto two lines is the same phrase
    return not s or s in PHRASES or bool(_TEMPLATES.fullmatch(s))


def banned(text: str) -> list[str]:
    return [f"{rx} → {canon}" for rx, canon in BANNED.items() if re.search(rx, text)]
