"""readme_draft: a DRAFT of the README update (Dan's post-run brief of 23 Oct, section 3), generated from the grid.

Reads (no run, no result file besides the grid's outputs):
  results/cross_model/<latest>/grid.csv  every number on the page (scripts/cross_model_grid.py)
  results/cross_model/<latest>/grid.md   the lens block, the grid table, its legend and footnotes, embedded as they are
  results/jobq/ledger*.jsonl             the night's runs: jobs started since --since (their --name and new results)
  figures/archive/cross_model/*.png              the merged figures (scripts/cross_model_figures.py), matched to a finding by
                                         their claim-named file names at run time (FIGURE_RULES); unmatched ones are
                                         listed in the cross-model section, none dropped
  VERIFIED.md, predictions/README.md, jobs/*/*.yaml   the status line, the scorecard, the specs of the mapping table
Writes drafts/README_<UTC stamp>.md, never README.md. Prints the path and the sections left as placeholders, no value.

Numbers: only from grid.csv; this file's own text has none (the decisions in the choices list aside). Rounded to whole
percent or points half to even (Python's round) from grid.csv's one decimal; grid.md rounds the unrounded value, so a
grid.csv value ending in .5 can show one point apart from grid.md.

Which rows: the main lens's rows (grid.csv's lens column without "listed beside") of each finding's grid settings;
breakdown rows (a " · " setting: per topic, per family) are not judged here. A model's state for a finding, from its
cells' verdict words: holds (some cell holds, none fails), fails (some fails, none holds), mixed (both), unclear (only
not interpretable / inconclusive), values only (only open), not testable, missing.

How sure (HOW_SURE, the same text on the page): strong iff it holds on three or more models, of both architectures,
on two separate runs (draws, formats, long context) on at least two of them, and no cell of the finding fails, fails a
control or is inconclusive; open iff it holds on no model, or fails (or is mixed) on as many models as it holds on;
medium otherwise. The reason printed is the condition that decided it.

uv run python scripts/readme_draft.py [--grid DIR] [--since ISO] [--out DIR]
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import fnmatch
import io
import json
import re
import subprocess
import sys
import textwrap
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import cross_model_grid as G

REPO = G.REPO
SINCE = "2026-10-22T19:30:00+00:00"  # the night of 22-23 Oct (coordinator, 23 Oct)
FINDINGS = tuple(f for f in G.FINDINGS if f.key != "gate")
GATE = G.FINDING["gate"]
MODEL_BY_LABEL = {m.label: m for m in G.MODELS}
FINDING_BY_NAME = {f.name: f for f in G.ALL_FINDINGS}  # the 23 Oct C1-C3 findings too (readme_build)
SHORT = {"27b": "27B", "9b": "9B", "olmo_hybrid": "Olmo-Hybrid", "32b": "32B", "olmo": "OLMo-3", "muse": "Muse",
         "gemma": "Gemma", "122b": "122B"}  # fmt: skip
ARCH = {"hybrid": "hybrids", "attention": "attention-only models"}
STATES = ("holds", "fails", "mixed", "unclear", "values only", "not testable", "missing")
BAD = ("fails", "not interpretable", "inconclusive")  # any such cell keeps a finding from "strong"
WORD_ORDER = ("holds", "fails", "inconclusive", "not interpretable", "open", "not testable", "missing")
MAX_BULLETS = 8
BESIDE = ", listed beside)"  # grid.csv's lens column for a run with another lens than the main one

HOW_SURE = (
    "**strong**: holds on three or more models, of both architectures (hybrid and attention-only), on two separate "
    "runs (draws, formats, long context) on at least two of them, and no cell of the finding fails, fails a control "
    "or is inconclusive · **open**: holds on no model, or fails (or is mixed) on as many models as it holds on · "
    "**medium**: everything in between. The reason given is the condition that decided it."
)
STATE_RULE = (
    "A model's state for a finding, from the verdicts of its cells (every draw and setting, main lens): holds = some "
    "cell holds and none fails; fails = some fails and none holds; mixed = both; unclear = only failed controls or "
    "the rule's own 'inconclusive'; values only = only cells without a committed rule; not testable = no lens, the "
    "gate or competence failed; missing = did not run or no saved verdict."
)

# Figures: (glob on the lower-case file name, finding key or "depth" / "gate"); the first match wins
FIGURE_RULES = (
    ("*layer_gap*", "f8"), ("*depth*", "depth"), ("*late_read*", "f4"), ("*block*", "f4"), ("*name*digit*", "f3"),
    ("*digit*name*", "f3"), ("*count*", "f6"), ("*list_order*", "f6"), ("*identity*", "f5"), ("*order_label*", "f5"),
    ("*push*", "f7"), ("*writ*", "f8"), ("*stated*", "f2"), ("*lens_part*", "f2"), ("*lens_claim*", "f2"),
    ("*gate*", "gate"), ("*remov*", "f1"), ("*knock*", "f1"),
)  # fmt: skip


# ---------------------------------------------------------------- what the page says in words (no numbers)


@dataclass(frozen=True)
class Text:
    metric: tuple[tuple[str, str], ...]  # (part of the setting, plain label of the key number)
    low_is_good: bool  # the claim wants the key number low (e.g. % right with the read blocked)
    did: tuple[str, ...]  # what we did, from README.md of 22 Oct
    weak: tuple[str, ...]  # weak spots that do not come from the grid
    means: str


TEXT = {
    "f1": Text(
        (("", "more lost by recall than by the lookup"),), False,
        ("While the bridge forms (the middle layers), removed the J-space (the part of a hidden state the lens reads) "
         "and counted the answers still right, for recalls and for lookups; controls: the same removal with the fit "
         "rotated, or a random dictionary of the same size.",
         "Zach's version on his generator's tasks: a knock-out of the lens's top words, judged by his rule (questions "
         "answered from memory must lose more than questions answered from the prompt)."),
        ("The animal-suite removal has no committed rule: its cell shows the gap with an interval chosen after seeing "
         "the data (see the choices below).",
         "Some removal runs dropped the random-dictionary control (too large next to the model on one GPU); their "
         "control gate reads the rotated control alone."),
        "a lookup in the prompt does not need the J-space; the other findings ask what it uses instead.",
    ),
    "f2": Text(
        (("", "of lookups switched by the lens-readable part"),), True,
        ("Changed the stated bridge (Jack's pet: cow → pig) and pasted back only one part of the change it causes, at "
         "one cell chosen from a lens-free map: the part the lens can read, or everything else.",
         "Control: the same lens-readable part must switch recall from that stated bridge, else the cell is not "
         "interpretable. Prose scenes on topic draws, and tables and JSON tool outputs."),
        ("The lens's read at the bridge's own sentence sits mostly on the bridge's word itself; the gate read after "
         "the word (the lens block below) asks whether the lens reads more than the word.",
         "The recall control is weak on some topics; the verdict is the pre-registered pooled one."),
        "the lookup reads the bridge where it is stated, not through the part the lens reads.",
    ),
    "f3": Text(
        (("", "right with the digit hidden from the last tokens"),), True,
        ("Hid one part of the answer's sentence from the last tokens: the sentence without its name, or the sentence "
         "without its digit (a lone digit token leaks through its neighbours, so these two are the decisive pair); "
         "the same parts of another sentence as the control.",
         "Several draws of scenes, and prose, markdown tables and JSON tool outputs."),
        ("Why the question's tokens read the name (for instance, to pick the bridge among the listed entities) is not "
         "tested.",),
        "the last tokens fetch the answer's digit; the name is looked up earlier, by the question's tokens.",
    ),
    "f4": Text(
        (("", "right with the read blocked"),), True,
        ("Stopped the last tokens from attending to the answer's sentence (in every attention layer; on "
         "attention-only models, every layer) and counted the answers still right, against guessing among the list's "
         "digits.",
         "Controls: block another sentence instead; on the hybrids, block the DeltaNet layers instead. Also in tables "
         "and JSON, and with long neutral filler between the list and the question."),
        ("Recall stays right by construction (the blocked sentence is not on its path): a control, not a finding.",
         "The bar is the guessing rate, so a model that drops to guessing but not below fails the rule (the grid "
         "footnotes it 'at chance').",
         "The long context is neutral filler, not a real document."),
        "the route around the J-space ends in an ordinary attention read of the answer's sentence by the last tokens.",
    ),
    "f5": Text(
        (("1st-2nd", "order label lead"), ("3rd on", "identity lead")), False,
        ("Two prompts list the same entities in a different order; copied the donor prompt's last two tokens into the "
         "original at one layer. Each possible answer is a different digit, so the answer shows what the copied "
         "tokens pointed to.",
         "Rule fixed in advance: for the 1st and 2nd asked sentence the place must beat the identity; from the 3rd on "
         "the identity must be at least as frequent (intervals over entities). Fresh draws, and longer lists."),
        ("One layer per model: Qwen3.6-27B's chosen after its first runs (repeated on later draws), the others by a "
         "fixed rule (the last layer where the donor's digit is still rare).",
         "The identity part is a modest margin on the larger Qwens, with many answers unchanged or elsewhere in the "
         "list.",
         "'Identity', not 'word': whether the identity is the lens's word form is the open question of the lens "
         "findings."),
        "this matches lookback work in the middle of the list and differs at its end (no positional pointer for the "
        "last items); new here: it holds when the bridge is recalled rather than named.",
    ),
    "f6": Text(
        (("", "of patched answers follow the order in the list"),), False,
        ("Built the lists so that the order in the list, the place in the text and counting from the end point to "
         "different sentences: a filler sentence moves, or the donor list has one sentence more or fewer; then the "
         "same patch of the last tokens.",),
        ("The tests pool all asked sentences, so their signal comes mostly from the 1st and 2nd.",
         "On some models the decisive layers are the swept layers where the donor's digit is still rare, applied by "
         "the grid (see the choices below)."),
        "the label counts entities in the list, not token positions.",
    ),
    "f7": Text(
        (("", "of lookups switched by the lens push"),), True,
        ("Pushed the hidden state at the stated bridge's sentence or word toward another animal's lens word, over a "
         "sweep of layers and sizes; chose the cell on recall alone (the push must switch recall, a random push must "
         "not, and questions off the bridge's path must not move), then read the lookups there.",
         "Two rules, both reported: the pre-registered one (the valid cell with the most recall) and an amendment "
         "written knowing the old data (only cells after the early layers)."),
        ("One topic (the animal suite) and strong pushes (several times a typical change).",
         "The amendment was written knowing the old data, so the pre-registered rule stays the main one.",
         "A single direction (the lens's word difference) is pushed; a lookup could still use a lens-readable feature "
         "it does not reach."),
        "the lens can write a stated bridge where it sits and recall follows; the lookup does not follow a bridge "
        "written that way.",
    ),
    "f8": Text(
        (("", "of lookups the lens push writes"),), True,
        ("At the stated-bridge test's cell, pushed the lens direction; the cell counts only where the push writes "
         "recall (the positive control); then read whether it writes the lookup.",
         "At the last tokens, the fitted position code's test also pushed the lens direction: values only, no "
         "committed rule."),
        ("At the last tokens the lens arm has no rule, and its positive control exists in one topic only.",
         "For a recall the bridge's identity and the answer coincide, so a late push may carry the answer itself "
         "rather than the bridge."),
        "where the lens can be shown to write the bridge, the lookup still does not use that form: the lookup's bridge "
        "sits in a part of the representation the lens does not write.",
    ),
}  # fmt: skip

QUESTION = (
    "**The question.** To answer a two-step question, a model first finds an entity in between (the **bridge**), then "
    "uses it to get the answer. A **J-lens** reads a model's hidden states as words. Does the model use the bridge in "
    'the form the lens reads, or by another route? Example: "Which locker belongs to the animal known for oinking?" '
    "→ bridge *pig* → answer: the pig's locker number, stated in the prompt (a **lookup**; a **recall** takes the "
    "answer from memory). Models: {models}."
)
LINKS = (
    "[Dan's predictions vs results](predictions/) · [plan (Google Doc)](https://docs.google.com/document/d/"
    "1bqqdXePTUXQGlowVjk73sPfJkbV_tsu0RNNX-BiTYUc/edit?usp=drivesdk) · [run log](EXPERIMENTS.md) · [old README with "
    "every number](HISTORY.md) · [how to run](DEVELOPER.md)"
)
NEGATIVE_KEPT = (
    "From before 23 Oct: the fitted position code only overrides the lookup (finding 8); a late attention head's "
    "read-out of the model's own errors is near-tautological, and the OLMo post-training ladder shows no difference "
    "(the longshots of the README before 23 Oct); colour-word answers and Gemma's random patch fail their controls "
    "(finding 5); random damage instead of blocking was not testable (finding 4)."
)
CHOICES_KEPT = (  # README.md of 22 Oct, slides renamed to findings, result numbers left to the old README
    ("Finding 5: the split by the asked sentence (the pooled pre-registered test was mixed)",
     "Confirmed as a rule fixed in advance on fresh scenes"),
    ("Finding 5: layer 50 on Qwen3.6-27B (the other models follow a fixed rule)", "Repeated on two more draws of scenes"),
    ("Finding 2: counting a topic only when its own recall control passes",
     "Stricter than the pre-registered pooled rule"),
    ("Finding 3: animals on Qwen3-32B's second draw, which missed the competence gate by a rounding margin",
     "Run post hoc with the gate lowered; same verdicts. The gate now rounds to two decimals"),
    ("Finding 7: reading the cells that pass the off-path check",
     "The decisive cell fixed in advance failed that check. The main rule (the off-path check before the maximum) was "
     "fixed after seeing these data; the amendment (from layer 20 on) was added knowing them, before the rerun's "
     "results were opened. The main rule stays main; both verdicts are reported"),
    ("Finding 2, the doubled run: the cell fixed in advance (the first map's choice); on Qwen3.5-9B the 27B's layers "
     "scaled by depth", "Fixed before those runs"),
    ("Finding 4: the first-sentence bias as a fall-back to the order label",
     "Dropped from the story; its control was not testable"),
    ("Batch 12 opened before Dan's predictions (his request, 22 Oct)", "His answers count as written after the results"),
    ("Finding 8: the position code's natural-size test allowed 1x or 2x",
     "Passes only at 2x; we read it as an override"),
    ("Finding 2's rule: one decisive cell, chosen from the lens-free map",
     "Amended on 22 Oct, after the runs started and before any result was opened"),
)  # fmt: skip
CHOICES_NIGHT = (  # decisions of the night of 22-23 Oct, in plain words (commits named for checking)
    "**Lens gate v2, where the lens is read**: only where the bridge's word is not: after the word in the bridge's own "
    "sentence (in prose, its closing period; decisive) and over the context without any mention of either bridge "
    "(reported); the same bars as v1. Set after seeing that v1's read sat on the bridge's own word, before any v2 run. "
    "v1 still opens the stated-bridge test; v2 is informational: if it fails, 'the lens reads the bridge' becomes 'the "
    "lens reads the bridge's word where it stands' (Dan, 22 Oct 23:20; 2b0701f, c2add04).",
    "**When an arm of the layer-gap test 'stops'**: at a layer where every valid cell's Wilson upper bound is below 5% "
    "of lookups (it keeps moving while some cell's lower bound is above 5%); the gap holds if the full patch stops at "
    "least six layers after the lens push and still moves lookups where the lens push stopped. Four arms on the same "
    "scenes (lens push, full patch, input-embedding push, random push), each with its own off-path check; set before "
    "the rerun, which replaced a first version stopped part-way (c2add04).",
    "**The keep-answer gate on Gemma and Muse**: in the stated-bridge test the lookups must keep their answer under "
    "the lens-part patch on at least 80% of items, else the cell is not interpretable. Added because a random patch "
    "of the same size breaks most of Gemma's answers (finding 5's control); set before any Gemma or Muse "
    "stated-bridge run (c2add04).",
    "**The primary lens**: where we fit our own J++ with the published recipe (Qwen3-32B, OLMo-3-7B-I; 64 prompts), "
    "every claim is judged on it; Zach's fits and the plain J-lens are listed beside it, never switched in silently. "
    "Decided by Dan (23 Oct ~00:30) after the plain J-lens results on Qwen3-32B were seen, before the J++ pins and any "
    "J++ run (e50b1dc, 193c060, 2f3c320).",
    "**The stated-bridge verdict's layer grid (a fix)**: its decisive cell is searched on the map's coarse grid (every "
    "sixteenth of the depth), not on every 4th layer, which never met the parts run's layers on Muse, met them at one "
    "layer on Gemma and skipped half the grid on the 32-layer models (the 64-layer models are unchanged). Found before "
    "any Muse, Gemma or OLMo J++ stated-bridge verdict ran; those runs were requeued (076edbb, 65f8dba).",
    "**OLMo-3-7B-I's lens push in raw prompts**: the chat format leaves too few fresh scenes OLMo answers right, so the "
    "raw-prompt run was fixed as OLMo's decisive cell before any OLMo J++ result, behind a short smoke check that "
    "stops it if the raw prompts' unedited answers differ from its competence run; the chat copy is not run (fe8f12f, "
    "f9f06b8).",
    "**Qwen3.5-122B at batch 16**: its read-heavy steps run 16 prompts per batch (J-space removal 8), to fit the night "
    "on the rented H200s (Dan, 23 Oct ~01:20); the originals queued at batch 4 were cancelled before running and "
    "requeued as copies; no rule, layer or item changed (d286f2c, cc02033).",
    "**Seven verdict words**: holds, fails, inconclusive (the rule itself says so; no control failed), not "
    "interpretable (a control failed: which), not testable (no lens, the gate or competence failed), missing (did not "
    "run, failed, or no saved verdict: why), open (values shown under no committed rule). 'Open' is its own word for "
    "the descriptive cells (the animal-suite J-space removal, the last-token lens arm), never 'missing' for that "
    "reason; the lens push's main rule keeps its own 'inconclusive' where the lookup moves between 10% and 30% (Dan, "
    "23 Oct; 3b8e3cc, 978cbdc).",
    "**Finding 1's interval**: the animal-suite removal has no committed rule, so its cell is descriptive: the share "
    "of lookups right minus the share of recalls right with the J-space removed (clean question). Its 95% interval: "
    "the bridge animals drawn with replacement, separately for the lookups and the recalls (unpaired), 4000 times "
    "with seed 0; the interval is the 2.5th to 97.5th percentile of the differences. Chosen after seeing the data; "
    "accepted by Dan (23 Oct; 978cbdc).",
    "**Finding 8, stated bridge, in the grid**: the cell holds iff the lens push writes recall and not the lookup at "
    "the stated-bridge cell; recall not written means no positive control (not interpretable). Written by the grid "
    "agent, accepted by Dan (23 Oct).",
    "**Finding 6's decisive layers** on Qwen3.5-9B, Qwen3-32B, Muse, Gemma and Qwen3.5-122B: the swept layers where "
    "the donor's digit is still rare (Wilson upper bound below 10%), the specs' rule applied by the grid. Accepted by "
    "Dan (23 Oct).",
    "**Finding 4, first draws**: judged by the late-read rule fixed on 22 Oct for the second draws (the first draws "
    "ran under an older rule); a late read that fails with its interval around chance is footnoted 'at chance' "
    "(Dan, 23 Oct).",
)
WORDS = (
    ("**bridge**", "The entity found in the first step", "\"the animal known for oinking\" → pig"),
    ("**recall / lookup**", "The answer comes from the model's memory / from a sentence in the prompt",
     "how many legs a pig has / \"The pig's locker is 3.\""),
    ("**J-lens, J-space**", "A tool that reads hidden states as words ([Gurnee et al. 2026](https://transformer-"
     "circuits.pub/2026/workspace/index.html)); the part of a hidden state it reads; J++ is its refined fit", ""),
    ("**lens push**", "Add the lens's direction from one word to another (pig → cow) to a hidden state", ""),
    ("**patch**", "Copy hidden states from a donor prompt into the original prompt, at chosen tokens and one layer, "
     "and see which answer comes out", ""),
    ("**blocking**", "Stop chosen tokens from attending to one sentence, in chosen layers", ""),
    ("**question tokens / last tokens**", "The words of the question / the chat-template tokens after the user's text, "
     "up to the answer (11 on the Qwen models, 7 on OLMo-3)", ""),
    ("**positive control**", "A place where a method is known to work, so that a null result elsewhere means "
     "something", ""),
    ("**hybrid / attention-only**", "Attention layers mixed with DeltaNet layers (a compressed running memory) / "
     "attention in every layer", ""),
)  # fmt: skip


# ---------------------------------------------------------------- grid.csv


@dataclass(frozen=True)
class Cell:
    """One grid.csv row of a finding's grid setting (part: '1st-2nd' / '3rd on' for finding 5, else '')."""

    model: str
    finding: str
    setting: str
    part: str
    main: bool
    word: str
    verdict: str
    value: float | None  # percent or points, as grid.csv
    unit: str  # "%" or "pts"
    ci: tuple[float, float] | None
    n: int | None
    control: str
    path: str


def grid_setting(f: G.Finding, s: str) -> tuple[str, str] | None:
    """(grid setting, part) of a grid.csv setting; None for a breakdown row (per topic, per family) or an unknown one."""
    if s in f.settings:
        return s, ""
    if " · " in s:
        return None
    for cand in sorted(f.settings, key=len, reverse=True):
        if s.startswith(cand + ", "):
            return cand, s[len(cand) + 2 :]
    return None


def parse_row(r: dict[str, str]) -> Cell | None:
    m, f = MODEL_BY_LABEL.get(r["model"]), FINDING_BY_NAME.get(r["finding"])
    if m is None or f is None:
        return None
    gs = grid_setting(f, r["setting"])
    word = next((w for w in G.VERDICTS if r["verdict"].startswith(w)), None)
    if gs is None or word is None:
        return None
    val, unit = None, "%"
    if r["value"].strip():
        num, unit = r["value"].split()
        val = float(num)
    ci = None
    if r["95% CI"].strip():
        lo, hi = r["95% CI"].strip("[]").split(",")
        ci = (float(lo), float(hi))
    return Cell(m.key, f.key, gs[0], gs[1], not r["lens"].endswith(BESIDE), word, r["verdict"], val, unit, ci,
                int(r["n"]) if r["n"].strip() else None, r["chance or control level"], r["result path"])  # fmt: skip


def read_grid(text: str) -> tuple[list[Cell], int]:
    """The main lens's cells of every finding's grid settings, and the number of rows not used (breakdowns, beside)."""
    cells, skipped = [], 0
    for r in csv.DictReader(io.StringIO(text)):
        c = parse_row(r)
        if c is None or not c.main:
            skipped += 1
            continue
        cells.append(c)
    return cells, skipped


RESULT_FILES = {"rows.jsonl", "summary.json", "verdict.json", "outcomes.jsonl", "cases.jsonl"}


def run_key(path: str) -> str:
    """The run a cell's numbers come from (its folder; analysis-* subfolders are the same run)."""
    p = path.split(" (")[0]
    parts = [x for x in p.split("/") if x and not x.startswith("analysis-")]
    if parts and parts[-1] in RESULT_FILES:
        parts = parts[:-1]
    return "/".join(parts)


STAMPED = re.compile(r"(.+?)(?:_e\d+-[a-z]+)?_\d{8}-\d{6}")  # <run>[_<level>]_<stamp> (d1_verdict, finding5_confirm)


def run_names(path: str) -> set[str]:
    """Run names a cell's result path can name (a folder, <run>_<stamp>, <run>.json)."""
    out = set()
    for seg in re.split(r"[/:]", path.split(" (")[0]):
        out.add(seg.removesuffix(".json"))
        if m := STAMPED.fullmatch(seg):
            out.add(m.group(1))
    return out


# ---------------------------------------------------------------- how sure


def model_state(words: Iterable[str]) -> str:
    w = set(words)
    if "holds" in w:
        return "mixed" if "fails" in w else "holds"
    if "fails" in w:
        return "fails"
    if w & {"not interpretable", "inconclusive"}:
        return "unclear"
    if "open" in w:
        return "values only"
    return "not testable" if "not testable" in w else "missing"


def states(cells: list[Cell]) -> dict[str, str]:
    by: dict[str, list[str]] = collections.defaultdict(list)
    for c in cells:
        by[c.model].append(c.word)
    return {m.key: model_state(by.get(m.key, [])) for m in G.MODELS}


def where(cells: Iterable[Cell]) -> str:
    """'Gemma (draw 3), Muse (draw 1 / 8 sentences)': models in the grid's order, their settings in the finding's."""
    by: dict[str, list[str]] = collections.defaultdict(list)
    for c in cells:
        if show(c.setting) not in by[c.model]:
            by[c.model].append(show(c.setting))
    return ", ".join(f"{SHORT[m.key]} ({' / '.join(by[m.key])})" for m in G.MODELS if m.key in by)


def names(keys: Iterable[str], short: bool = True) -> str:
    ks = set(keys)
    return ", ".join((SHORT[m.key] if short else m.label) for m in G.MODELS if m.key in ks)


@dataclass
class Judgement:
    finding: G.Finding
    cells: list[Cell]
    state: dict[str, str]
    level: str
    reasons: list[str] = field(default_factory=list)


def judge(f: G.Finding, cells: list[Cell]) -> Judgement:
    """HOW_SURE on the finding's main cells."""
    cs = [c for c in cells if c.finding == f.key]
    st = states(cs)
    hold = [m for m in G.MODELS if st[m.key] == "holds"]
    fail = [m for m in G.MODELS if st[m.key] in ("fails", "mixed")]
    bad = {w: [c for c in cs if c.word == w] for w in BAD}
    runs = {m.key: {run_key(c.path) for c in cs if c.model == m.key and c.word == "holds"} for m in hold}
    repeated = [m for m in hold if len(runs[m.key]) >= 2]
    archs = {m.arch for m in hold}
    if not hold or len(fail) >= len(hold):
        if hold:
            why = (f"fails on at least as many models as it holds on (fails: {names(m.key for m in fail)}; holds: "
                   f"{names(m.key for m in hold)})")  # fmt: skip
        elif fail:
            why = f"fails on {names(m.key for m in fail)}, holds nowhere"
        elif "values only" in st.values():
            why = "no committed rule: values only"
        elif "unclear" in st.values():
            why = "nowhere judged: a control failed or the rule says inconclusive"
        else:
            why = "not judged on any model yet"
        return Judgement(f, cs, st, "open", [why])
    reasons = []
    if bad["fails"]:
        reasons.append(f"fails on {where(bad['fails'])}")
    if bad["not interpretable"]:
        reasons.append(f"a control failed on {where(bad['not interpretable'])}")
    if bad["inconclusive"]:
        reasons.append(f"the rule says inconclusive on {where(bad['inconclusive'])}")
    if len(hold) < 3:
        reasons.append(f"holds on fewer than three models ({names(m.key for m in hold)})")
    if len(archs) < 2:
        reasons.append(f"holds on {ARCH[next(iter(archs))]} only")
    if len(repeated) < 2:
        reasons.append("holds on a second run on fewer than two models")
    if reasons:
        return Judgement(f, cs, st, "medium", reasons)
    return Judgement(f, cs, st, "strong", ["holds on both architectures and on a second run; no cell fails, fails a "
                                           "control or is inconclusive"])  # fmt: skip


# ---------------------------------------------------------------- numbers, words


def r0(x: float) -> int:
    return round(x)  # half to even, as round() in tests/test_cross_model_grid.py


def fmt_value(x: float, unit: str) -> str:
    return f"{r0(x)}%" if unit == "%" else f"{r0(x):+d} pts"


def fmt_ci(ci: tuple[float, float] | None, unit: str) -> str:
    if ci is None:
        return ""
    return f"[{r0(ci[0])}, {r0(ci[1])}]" if unit == "%" else f"[{r0(ci[0]):+d}, {r0(ci[1]):+d}]"


def fmt_range(lo: float, hi: float, unit: str) -> str:
    if r0(lo) == r0(hi):
        return fmt_value(lo, unit)
    if unit != "%":
        return f"{r0(lo):+d} to {r0(hi):+d} pts"
    return f"{r0(lo)}-{r0(hi)}%" if r0(lo) >= 0 else f"{r0(lo)}% to {r0(hi)}%"


def fmt_cell(c: Cell) -> str:
    assert c.value is not None
    ci = fmt_ci(c.ci, c.unit)
    return fmt_value(c.value, c.unit) + (f" {ci}" if ci else "") + ("" if c.n is None else f", n={c.n}")


def partly(m: re.Match[str]) -> str:
    a, b = (("holds" if x == "True" else "does not") for x in m.groups())
    return f"partly: the 1st-2nd part {a}, the 3rd-on part {b}"


PLAIN: tuple[tuple[re.Pattern[str], str | Callable[[re.Match[str]], str]], ...] = (
    (re.compile(r"\bH-(?:around|where): "), ""),
    (re.compile(r"\bgate G2\b"), "control gate"),
    (re.compile(r"\bG2\b"), "the control gate"),
    (re.compile(r"\bpartly: A (True|False), B (True|False)"), partly),
    *((re.compile(rf"\b{code}/clean\b"), name) for name, code in G.REMOVAL),
)


def plain(text: str) -> str:
    """Internal codes in grid text (verdict reasons, footnotes) in plain words."""
    for pat, rep in PLAIN:
        text = pat.sub(rep, text)
    return text


def why(c: Cell) -> str:
    """The short reason of a cell that is not a plain holds / fails / open."""
    if c.word in ("missing", "not testable"):
        text = G.md_cell([G.Row(c.model, c.finding, c.setting, verdict=c.verdict, md_text="")])[0]
        reason = text.split(": ", 1)[1] if ": " in text else ""
        return "see grid.csv" if reason == "see csv" else reason
    if c.word in ("not interpretable", "inconclusive", "fails"):
        inner = c.verdict[len(c.word) :].strip()
        inner = inner[1:-1] if inner.startswith("(") and inner.endswith(")") else inner
        return textwrap.shorten(plain(inner), 110, placeholder=" …")
    return ""


def reasons_of(cells: Iterable[Cell], model: str) -> list[str]:
    """A model's reasons over its cells that are not holds / open; 'no spec' only when it is the only one."""
    rs = list(dict.fromkeys(r for c in cells if c.model == model and c.word not in ("holds", "open") and (r := why(c))))
    return [r for r in rs if r != "no spec"] or rs


def show(setting: str) -> str:
    """A setting in prose: the lens gate's 'v1 (at the word)' as 'at the word'."""
    m = re.fullmatch(r"v\d \((.+)\)", setting)
    return m.group(1) if m else setting


def anchor(title: str) -> str:
    """GitHub's heading anchor."""
    return re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")


def title(f: G.Finding) -> str:
    return f"{f.number}. {f.name}"


def cell_text(s: str) -> str:
    return s.replace("|", "/")


# ---------------------------------------------------------------- sections


def evidence(j: Judgement) -> str:
    """Key evidence: the range of the key number where the finding holds and its weakest cell (all from grid.csv)."""
    tx = TEXT[j.finding.key]
    out = []
    for part, label in tx.metric:
        pool = [c for c in j.cells if c.part == part and c.value is not None]
        units = collections.Counter(c.unit for c in pool)
        pool = [c for c in pool if units and c.unit == units.most_common(1)[0][0]]
        held = [c for c in pool if c.word == "holds"]
        use = held or pool
        if not use:
            out.append(f"{label}: no values yet")
            continue
        vals = [c.value for c in use if c.value is not None]
        s = f"{fmt_range(min(vals), max(vals), use[0].unit)} {label}"
        if held:
            weak = (max if tx.low_is_good else min)(held, key=lambda c: c.value or 0.0)
            s += f" where it holds (weakest: {SHORT[weak.model]}, {show(weak.setting)}: {fmt_cell(weak)})"
            if opn := [c.value for c in pool if c.word == "open" and c.value is not None]:
                s += f"; values only, no committed rule: {fmt_range(min(opn), max(opn), use[0].unit)}"
        else:
            kind = "values only, no committed rule" if all(c.word == "open" for c in use) else "it holds nowhere"
            ns = [c.n for c in use if c.n is not None]
            s += f" ({kind}" + (f"; n={min(ns)}-{max(ns)})" if ns and min(ns) != max(ns) else
                                f"; n={ns[0]})" if ns else ")")  # fmt: skip
        out.append(s)
    chance = {m.group(1) for c in j.cells for m in [re.search(r"\bchance (\d+(?:\.\d+)?)%", c.control)] if m}
    if len(chance) == 1:
        out[-1] += f"; chance {r0(float(chance.pop()))}%"
    return "; ".join(out)


def models_line(st: dict[str, str], short: bool = True) -> str:
    groups = [(s, [k for k, v in st.items() if v == s]) for s in STATES]
    return " · ".join(f"{s}: {names(ks, short)}" for s, ks in groups if ks)


def glance(js: list[Judgement]) -> list[str]:
    hyb = ", ".join(f"{SHORT[m.key]} = {m.label}" for m in G.MODELS if m.arch == "hybrid")
    att = ", ".join(f"{SHORT[m.key]} = {m.label}" for m in G.MODELS if m.arch == "attention")
    out = ["## Findings at a glance", "",
           "Key evidence: grid.csv's numbers (% of items or points, [95% CI], n). How sure, by a fixed rule on the "
           f"grid's verdicts ([the rule](#how-sure-the-rule)): {HOW_SURE}", "",
           "| # | Finding | Key evidence | How sure | Models |", "|---|---|---|---|---|"]  # fmt: skip
    for j in js:
        f = j.finding
        reason = "; ".join(j.reasons[:2]) + ("; …" if len(j.reasons) > 2 else "")
        out.append(f"| {f.number} | [{f.name}](#{anchor(title(f))}) | {cell_text(evidence(j))} | **{j.level}**: "
                   f"{cell_text(reason)} | {cell_text(models_line(j.state))} |")  # fmt: skip
    out += ["", f"Hybrids: {hyb}. Attention-only: {att}.", ""]
    return out


@dataclass
class Bullet:
    key: str  # the finding's key ("" for a merged bullet)
    head: str  # the finding's name, or the merged bullet's label
    body: str  # " (settings): verdicts"
    words: set[str]
    sub: list[Bullet] = field(default_factory=list)  # a merged bullet's findings, nested one level

    @property
    def text(self) -> str:
        if self.sub:
            return f"- **{self.head}**:\n" + "\n".join("  " + b.text for b in self.sub)
        return f"- **{self.head}**{self.body}."


def bullet(f: G.Finding, cs: list[Cell]) -> Bullet:
    """The finding's verdicts per model on the night's cells; each model's settings named only when several ran."""
    seen: dict[tuple[str, str], Cell] = {}
    for c in cs:
        seen.setdefault((c.model, c.setting), c)
    settings = sorted({c.setting for c in seen.values()}, key=f.settings.index)
    by: dict[str, list[Cell]] = collections.defaultdict(list)
    for c in seen.values():
        by[c.word].append(c)
    parts = []
    for w in WORD_ORDER:
        if w not in by:
            continue
        items = []
        for m in G.MODELS:
            mine = sorted((c for c in by[w] if c.model == m.key), key=lambda c: f.settings.index(c.setting))
            if not mine:
                continue
            reasons = list(dict.fromkeys(r for c in mine if w not in ("holds", "fails", "open") and (r := why(c))))
            sets = " / ".join(show(c.setting) for c in mine) if len(mine) < len(settings) else ""
            note = ": ".join(x for x in (sets, "; ".join(reasons)) if x)
            items.append(SHORT[m.key] + (f" ({note})" if note else ""))
        parts.append(f"{'values only (no committed rule)' if w == 'open' else w} on {', '.join(items)}")
    return Bullet(f.key, f.name, f" ({' / '.join(show(s) for s in settings)}): " + "; ".join(parts), set(by))


def merged(label: str, group: list[Bullet]) -> Bullet:
    return Bullet("", label, "", set().union(*(b.words for b in group)), group)


LENS_FREE = ("f3", "f4", "f5", "f6")  # merged before any lens finding when there are too many bullets
MERGES: tuple[tuple[Callable[[Bullet], bool], str], ...] = (
    (lambda b: b.words == {"holds"}, "Held on every model judged that night"),
    (lambda b: b.words <= {"missing"}, "Did not run, failed or no saved verdict"),
    (lambda b: b.key in LENS_FREE, "The lookup's mechanism (lens-free findings)"),
)


def what_changed(cells: list[Cell], runs: set[str], since: dt.datetime) -> tuple[list[str], list[str]]:
    """5-8 bullets from the grid's verdicts on the night's runs (one per finding; merged when there are more)."""
    head = ["## What changed on the night of 22-23 Oct", "",
            f"Runs started since {since:%d %b %H:%M} UTC (the queue ledgers), as the grid judges them; main lens. "
            "Each bullet: the finding, the settings run that night, the verdict per model.", ""]  # fmt: skip
    night = [c for c in cells if run_names(c.path) & runs]
    if not night:
        return [*head, f"- No grid cell comes from a run started since {since:%d %b %H:%M} UTC.", ""], ["what changed"]
    bullets = [bullet(f, cs) for f in G.FINDINGS if (cs := [c for c in night if c.finding == f.key])]
    for test, label in MERGES:
        if len(bullets) <= MAX_BULLETS:
            break
        group = [b for b in bullets if b.key and test(b)]
        if len(group) > 1:
            ids = {id(b) for b in group}
            bullets = [b for b in bullets if id(b) not in ids] + [merged(label, group)]
    if len(bullets) > MAX_BULLETS:
        bullets = [*bullets[: MAX_BULLETS - 1], merged("Also that night", bullets[MAX_BULLETS - 1 :])]
    return [*head, *(b.text for b in bullets), ""], []


def figures(repo: Path) -> dict[str, list[Path]]:
    """figures/archive/cross_model/*.png by finding key (FIGURE_RULES; the first match wins), unmatched under 'other'."""
    out: dict[str, list[Path]] = collections.defaultdict(list)
    for p in sorted((repo / "figures" / "archive" / "cross_model").glob("*.png")):
        key = next((k for pat, k in FIGURE_RULES if fnmatch.fnmatch(p.name.lower(), pat)), "other")
        out[key].append(p)
    return out


def fig_lines(paths: list[Path], repo: Path) -> list[str]:
    out = []
    for p in paths:
        alt = p.stem.removeprefix("f_").replace("_", " ")
        svg = p.with_suffix(".svg")
        out += [f"![{alt}]({p.relative_to(repo)})" + (f" ([SVG]({svg.relative_to(repo)}))" if svg.exists() else ""), ""]
    return out


def finding_section(j: Judgement, figs: list[Path], repo: Path, grid_link: str) -> tuple[list[str], list[str]]:
    f, tx = j.finding, TEXT[j.finding.key]
    out = [f"## {title(f)}", "",
           f"**How sure:** {j.level}: {'; '.join(j.reasons)}.", "",
           f"**Key evidence:** {evidence(j)}.", "",
           f"**Models:** {models_line(j.state, short=False)}.", ""]  # fmt: skip
    placeholders = []
    if figs:
        out += fig_lines(figs, repo)
    else:
        out += ["_No merged figure for this finding in figures/archive/cross_model/ yet._", ""]
        placeholders.append(f"figure: {title(f)}")
    out += ["**What we did**", *(f"- {d}" for d in tx.did), ""]
    weak = [f"- {SHORT[c.model]}, {c.setting}: {c.word}" + (f" ({w})" if (w := why(c)) else "") + "."
            for c in sorted({(c.model, c.setting): c for c in j.cells if c.word in BAD}.values(),
                            key=lambda c: ([m.key for m in G.MODELS].index(c.model), f.settings.index(c.setting)))]  # fmt: skip
    if opn := [c for c in j.cells if c.word == "open"]:
        weak.append(f"- Values only, no committed rule: {where(opn)}.")
    for state, label in (("not testable", "Not testable"), ("missing", "Not run or no saved verdict")):
        ms = [k for k, v in j.state.items() if v == state]
        if ms:
            weak.append(f"- {label}: " + ", ".join(f"{SHORT[k]} ({'; '.join(reasons_of(j.cells, k)) or state})"
                                                   for k in ms) + ".")  # fmt: skip
    out += ["**Weak spots**", *weak, *(f"- {w}" for w in tx.weak), ""]
    lead = {"strong": "", "medium": "Where it holds: ", "open": "Not settled. If it holds: "}[j.level]
    means = lead + (tx.means[0].upper() + tx.means[1:] if not lead else tx.means)
    out += [f"**What it means:** {means}", "", f"Every cell, with its n and interval: {grid_link}.", ""]
    return out, placeholders


def md_sections(text: str) -> dict[str, list[str]]:
    """grid.md by '## ' heading ('' = the part before the first)."""
    out: dict[str, list[str]] = {"": []}
    cur = ""
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        else:
            out[cur].append(line)
    return out


def architecture(cells: list[Cell]) -> str:
    """Only what the grid shows: per finding (and gate version), the states on hybrids vs attention-only models."""
    items: list[tuple[str, list[Cell]]] = [(f"finding {f.number}", [c for c in cells if c.finding == f.key])
                                           for f in FINDINGS]  # fmt: skip
    items += [(f"the lens gate, {show(s)}", [c for c in cells if c.finding == "gate" and c.setting == s])
              for s in GATE.settings]  # fmt: skip
    groups: dict[str, list[str]] = collections.defaultdict(list)
    for label, cs in items:
        st = states(cs)
        hold = {a: [m.key for m in G.MODELS if m.arch == a and st[m.key] == "holds"] for a in ARCH}
        fail = {a: [m.key for m in G.MODELS if m.arch == a and st[m.key] in ("fails", "mixed")] for a in ARCH}
        judged = [a for a in ARCH if hold[a] or fail[a]]
        failing = [a for a in ARCH if fail[a]]
        detail = "; ".join(f"{ARCH[a]}: " + ", ".join(x for x in (f"holds on {names(hold[a])}" if hold[a] else "",
                                                               f"fails on {names(fail[a])}" if fail[a] else "") if x)
                           for a in judged)  # fmt: skip
        if not judged:
            groups["none"].append(label)
        elif len(judged) == 1:
            groups["one"].append(f"{label} ({detail})")
        elif not failing:
            groups["same"].append(label)
        else:
            groups["both" if len(failing) == 2 else failing[0]].append(f"{label} ({detail})")
    hyb = names(m.key for m in G.MODELS if m.arch == "hybrid")
    att = names(m.key for m in G.MODELS if m.arch == "attention")
    s = (f"**What differs by architecture.** From grid.csv's verdicts (main lens; a model counts as judged where it "
         f"holds, fails or is mixed; a pattern here describes the grid, it does not test architecture). "
         f"Hybrids: {hyb}; attention-only: {att}.")  # fmt: skip
    for key, head in (("same", "Holds on every judged model of both architectures"),
                      ("attention", "Fails only on attention-only models"), ("hybrid", "Fails only on hybrids"),
                      ("both", "Fails on models of both architectures"), ("one", "Judged on one architecture only"),
                      ("none", "Not judged on either yet")):  # fmt: skip
        if groups[key]:
            s += f" {head}: {'; '.join(groups[key])}."
    return s + (" Size, family and architecture are confounded across these models: the grid shows where a finding "
                "holds, not why.")  # fmt: skip


def cross_model(grid_md: str, cells: list[Cell], figs: dict[str, list[Path]], repo: Path,
                grid_link: str) -> tuple[list[str], list[str]]:  # fmt: skip
    sec = md_sections(grid_md)
    placeholders = []
    legend = [plain(x) for x in sec[""] if x.startswith(("Cell: ", "Finding 1: "))]
    out = ["## Across models", "", architecture(cells), ""]
    if figs.get("depth"):
        out += [
            "Where the steps sit along the depth (patch outcomes by % of depth):",
            "",
            *fig_lines(figs["depth"], repo),
        ]
    for name, head, extra in (("Lens", "Lens", figs.get("gate", [])), ("The grid", "Every finding on every model", []),
                              ("Footnotes", "Footnotes", [])):  # fmt: skip
        out += [f"### {head}", ""]
        if name == "The grid":
            out += [f"From {grid_link}. {' '.join(legend)}".rstrip(), ""]
        if name in sec:
            body = [plain(x) for x in sec[name]]
            while body and not body[0].strip():
                body.pop(0)
            out += [*body, ""]
        else:
            out += [f"_No '{name}' section in grid.md._", ""]
            placeholders.append(f"cross-model: {name}")
        out += fig_lines(extra, repo)
    if figs.get("other"):
        out += ["### Other merged figures", "", *fig_lines(figs["other"], repo)]
    return out, placeholders


def negative(js: list[Judgement], gate: list[Cell]) -> list[str]:
    out = ["## Negative or not testable", "", NEGATIVE_KEPT, "", "From the grid (main lens; cells never specified, "
           "'no spec', are marked in the grid only):", ""]  # fmt: skip
    rows: list[tuple[str, list[Cell]]] = [(j.finding.name, j.cells) for j in js]
    rows += [(f"{GATE.name}, {show(s)}", [c for c in gate if c.setting == s]) for s in GATE.settings]
    for name, cs in rows:
        st = states(cs)
        parts = []
        for state in ("fails", "mixed", "unclear", "not testable", "missing"):
            items = []
            for k in [k for k, v in st.items() if v == state]:
                if state in ("fails", "mixed"):
                    where_ = " / ".join(
                        dict.fromkeys(show(c.setting) for c in cs if c.model == k and c.word == "fails")
                    )
                    one = len({c.setting for c in cs}) == 1  # the row is one setting (a gate version): not repeated
                    items.append(SHORT[k] + ("" if one else f" ({'fails on ' if state == 'mixed' else ''}{where_})"))
                    continue
                rs = reasons_of(cs, k)
                if state == "missing" and set(rs) <= {"no spec"}:
                    continue
                items.append(SHORT[k] + (f" ({'; '.join(rs)})" if rs else ""))
            if items:
                parts.append(f"{state} on {', '.join(items)}")
        if parts:
            out.append(f"- **{name}**: " + "; ".join(parts) + ".")
    return [*out, ""]


def choices() -> list[str]:
    out = ["## Choices made after seeing the data", "", "Kept from the README of 22 Oct:", "",
           "| Choice | What happened since |", "|---|---|"]  # fmt: skip
    out += [f"| {a} | {b} |" for a, b in CHOICES_KEPT]
    return [*out, "", "Added on the night of 22-23 Oct (decisions, not results):", "",
            *(f"- {c}" for c in CHOICES_NIGHT), ""]  # fmt: skip


def scorecard(repo: Path) -> list[str]:
    p = repo / "predictions" / "README.md"
    text = p.read_text() if p.exists() else ""
    table = [re.sub(r"\]\((?!https?:)([^)]+)\)", r"](predictions/\1)", x) for x in text.splitlines()
             if x.startswith("|")]  # fmt: skip
    total = [x for x in text.splitlines() if x.startswith("Total so far")]
    out = ["## Predictions scorecard", "",
           "Dan writes a guess under each question before any result is opened; the agents add the result and a "
           "verdict after. From [predictions/README.md](predictions/README.md):", ""]  # fmt: skip
    out += [*table, ""] if table else ["_predictions/README.md has no scorecard table._", ""]
    out += [*total, ""] if total else []
    return [*out, "**Batches 13-15** ([2026-10-23_dan.md](predictions/2026-10-23_dan.md), the night of 22-23 Oct): "
            "PLACEHOLDER, not scored: Dan's answers are not written yet. Score them after his answers are committed "
            "and before this draft becomes README.md.", ""]  # fmt: skip


def verified(repo: Path) -> str:
    """'A1, A2 (Danyil); B1 (Zach)' from VERIFIED.md's entries and who checked them."""
    p = repo / "VERIFIED.md"
    by: dict[str, list[str]] = collections.defaultdict(list)
    for block in re.split(r"^## ", p.read_text() if p.exists() else "", flags=re.M)[1:]:
        head = block.splitlines()[0]
        m = re.match(r"([A-Z]\d+)\.", head)
        if not m:
            continue
        who = re.search(r"\(verified [^,()]+, ([^)]+)\)", head) or re.search(r"\*\*Checked\*\* \(([^,]+),", block)
        by[who.group(1).strip() if who else "unnamed"].append(m.group(1))
    return "; ".join(f"{', '.join(ids)} ({name})" for name, ids in by.items()) or "none"


def spec_folders(repo: Path) -> dict[str, set[str]]:
    idx: dict[str, set[str]] = collections.defaultdict(set)
    for p in repo.glob("jobs/*/*.yaml"):
        for run in set(re.findall(r"--name (\w+)", p.read_text())):
            idx[run].add(f"jobs/{p.parent.name}/")
    return idx


def appendix(rows: list[dict[str, str]], repo: Path) -> list[str]:
    idx = spec_folders(repo)
    specs: dict[str, set[str]] = collections.defaultdict(set)
    rules: dict[str, set[str]] = collections.defaultdict(set)
    for r in rows:
        f = FINDING_BY_NAME.get(r["finding"])
        if f is None:
            continue
        if r["rule id"]:
            rules[f.key].add(r["rule id"])
        for run in run_names(r["result path"]):
            specs[f.key] |= idx.get(run, set())
    out = ["## Appendix", "", "### Mapping: names, internal codes, scripts, specs", "",
           "The only place internal codes appear. Rule ids: grid.md's mapping table states each rule.", "",
           "| # | Finding | Internal codes | Scripts | Specs | Rule ids |", "|---|---|---|---|---|---|"]  # fmt: skip
    for f in G.FINDINGS:
        out.append(f"| {f.number or '-'} | {f.name} | {f.codes} | {f.scripts} | "
                   f"{', '.join(sorted(specs[f.key])) or '-'} | {', '.join(sorted(rules[f.key])) or '-'} |")  # fmt: skip
    out += ["", "### How sure: the rule", "", HOW_SURE, "", STATE_RULE, "",
            "Rows used: the main lens's (grid.csv's lens column without 'listed beside'), each finding's grid settings; "
            "per-topic and per-family breakdown rows are not judged here. Separate runs: separate result folders. "
            "Numbers: grid.csv's, rounded half to even.", "",
            "### Words we use", "", "| Word | Meaning | Example |", "|---|---|---|",
            *(f"| {a} | {b} | {c} |" for a, b, c in WORDS), ""]  # fmt: skip
    return out


# ---------------------------------------------------------------- the night's runs, the draft


def when(s: str) -> dt.datetime:
    t = dt.datetime.fromisoformat(s)
    return t if t.tzinfo else t.replace(tzinfo=dt.UTC)


def night_runs(repo: Path, since: dt.datetime) -> set[str]:
    """Run names of the jobs started since `since` (else ended since, without a start): their --name and new results."""
    runs: set[str] = set()
    for p in sorted((repo / "results" / "jobq").glob("ledger*.jsonl")):
        for line in p.read_text().splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(r, dict):
                continue
            t = r.get("started_at") or r.get("ended_at")
            if not t or when(t) < since:
                continue
            runs |= set(re.findall(r"--name (\w+)", r.get("command") or ""))
            runs |= {d.rstrip("/").split("/")[-1] for d in r.get("new_results") or []}
    return runs


def git_head(repo: Path) -> str:
    p = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                       check=False)  # fmt: skip
    return p.stdout.strip() or "-"


def latest_grid(repo: Path) -> Path | None:
    dirs = sorted(d for d in (repo / "results" / "cross_model").glob("*") if (d / "grid.csv").exists())
    return dirs[-1] if dirs else None


@dataclass
class Draft:
    text: str
    placeholders: list[str]


def draft(grid_dir: Path, repo: Path = REPO, since: dt.datetime | None = None, now: dt.datetime | None = None) -> Draft:
    since = since or when(SINCE)
    now = now or dt.datetime.now(dt.UTC)
    repo, grid_dir = repo.resolve(), grid_dir.resolve()
    csv_text = (grid_dir / "grid.csv").read_text()
    grid_md = (grid_dir / "grid.md").read_text() if (grid_dir / "grid.md").exists() else ""
    cells, _ = read_grid(csv_text)
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    js = [judge(f, cells) for f in FINDINGS]
    figs = figures(repo)
    rel = grid_dir.relative_to(repo) if grid_dir.is_relative_to(repo) else grid_dir
    grid_link = f"[grid.md]({rel}/grid.md) · [grid.csv]({rel}/grid.csv)"
    built = re.search(r"Built by scripts/cross_model_grid\.py at (.+?) \((\S+)\)", grid_md)
    models = (", ".join(m.label for m in G.MODELS if m.arch == "hybrid") + " (hybrids); "
              + ", ".join(m.label for m in G.MODELS if m.arch == "attention") + " (attention-only)")  # fmt: skip
    placeholders = [] if grid_md else ["grid.md (not found)"]
    out = ["<!-- DRAFT written by scripts/readme_draft.py; every number from grid.csv; links resolve from the repo "
           "root (this file becomes README.md only by hand) -->", "", "# bridge-jspace", "",
           QUESTION.format(models=models), "",
           f"> **Status, {now.day} {now:%b %Y}: draft, exploration.** Generated at {git_head(repo)} from the grid in "
           f"`{rel}` (built at {built.group(1) if built else 'an unknown commit'}). Nothing on this page is "
           f"human-verified except the entries of [VERIFIED.md](VERIFIED.md): {verified(repo)}.", "",
           LINKS + f" · {grid_link}", ""]  # fmt: skip
    out += glance(js)
    lines, ph = what_changed(cells, night_runs(repo, since), since)
    out += lines
    placeholders += ph
    for j in js:
        lines, ph = finding_section(j, figs.get(j.finding.key, []), repo, grid_link)
        out += ["---", "", *lines]
        placeholders += ph
    lines, ph = cross_model(grid_md, cells, figs, repo, grid_link)
    out += ["---", "", *lines]
    placeholders += ph
    out += ["---", "", *negative(js, [c for c in cells if c.finding == "gate"]), *choices(), *scorecard(repo)]
    out += ["---", "", *appendix(rows, repo)]
    placeholders.append("predictions: batches 13-15")
    return Draft(re.sub(r"\n{3,}", "\n\n", "\n".join(out)).rstrip() + "\n", placeholders)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument(
        "--grid", default=None, help="a results/cross_model/<stamp>/ folder (default: the latest with grid.csv)"
    )
    ap.add_argument("--since", default=SINCE, help="the night's runs: jobs started at or after this time (ISO)")
    ap.add_argument("--out", default=None, help="folder for README_<stamp>.md (default: drafts/)")
    ap.add_argument("--repo", default=str(REPO), help=argparse.SUPPRESS)  # tests: a synthetic repo
    a = ap.parse_args(argv)
    repo = Path(a.repo)
    grid_dir = Path(a.grid) if a.grid else latest_grid(repo)
    if grid_dir is None:
        print("no results/cross_model/<stamp>/grid.csv: nothing written")
        return 1
    now = dt.datetime.now(dt.UTC)
    d = draft(grid_dir, repo, when(a.since), now)
    out_dir = Path(a.out) if a.out else repo / "drafts"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"README_{now:%Y%m%dT%H%M%SZ}.md"
    path.write_text(d.text)
    print("wrote", path)
    print("placeholders:", "; ".join(d.placeholders) or "none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
