"""The data the figures read, and nothing that draws: the sources (data/figures/depth/data.csv, docs/breadth/data.csv,
docs/depth/x0_numbers.json, data/figures/writeup/data.csv), the model order, names and short ids, and the few
constants and accessors the styles-plot builders (figkit/*_sp*.py) and the status registry share. Moved verbatim from
the retired figure kit (figkit/data.py, specs.py, writeup_figs.py, claim_figs.py, curve_figs.py, deck_figs.py,
depth_figs.py, terms.py, exemplars.py); nothing on a figure is typed: a builder asks this module for a cell
(value, lo, hi) by its source row.
"""

from __future__ import annotations

import csv
import json
import re
from functools import cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

# ---- models -----------------------------------------------------------------------------------------------------------
DAN = [("qwen3.5-9b", "Qwen 9B"), ("qwen3.6-27b", "Qwen 27B"), ("muse-glimmer-30b", "Muse 30B"),
       ("nemotron-3.5-lightning", "Lightning ○"), ("qwen3.5-122b-a10b", "Qwen 122B")]  # fmt: skip
ZACH = [("q27", "Qwen 27B"), ("q9", "Qwen 9B"), ("nl", "Lightning"), ("ds", "DeepSeek"), ("mi", "Ministral"),
        ("nb", "Bolt"), ("ol", "OLMo"), ("mu", "Muse 30B"), ("q122", "Qwen 122B")]  # fmt: skip
NAMES = {n for _, n in DAN} | {n for _, n in ZACH}
SHORT = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse", "qwen3.5-122b-a10b": "122b"}
ZK = {"qwen3.5-9b": "q9", "qwen3.6-27b": "q27", "muse-glimmer-30b": "mu", "nemotron-3.5-lightning": "nl",
      "qwen3.5-122b-a10b": "q122"}  # fmt: skip
TWIN_MODELS = (("q9", "Qwen 9B"), ("q27", "Qwen 27B"), ("nl", "Lightning"))
NOT_CLAIMED = {"mu": "not claimed: shared with the logit lens", "q122": "not claimed: gone when scored by probability"}


def hollow(model: str, lowered_test: bool = False) -> bool:
    """After the data, for the depth tests only (one layer, routes, address, last token): Lightning; the 122B where its
    gate was lowered (routes, address, swap). Lightning's breadth tests (band test, made-up-fact set, pointer, Fig. 10, 11,
    5a) were registered before their data (docs/breadth/prereg_replication_1022.md; Dan, 7 Nov): their status is in
    data/figures/status.csv, not here."""
    return model == "nemotron-3.5-lightning" or (lowered_test and model == "qwen3.5-122b-a10b")


# ---- the sources ------------------------------------------------------------------------------------------------------
def _f(x):
    try:
        return float(x) if x not in (None, "") else None
    except ValueError:
        return None


@cache
def story() -> dict:
    out = {}
    with (REPO / "data/figures/depth/data.csv").open() as f:
        for r in csv.DictReader(f):
            v = _f(r["value"])
            if v is not None:
                out[(r["figure"], r["model"], r["quantity"])] = (v, _f(r["lo"]), _f(r["hi"]))
    return out


@cache
def breadth() -> dict:
    with (REPO / "docs/breadth/data.csv").open() as f:
        return {
            r["key"]: (_f(r["value"]), _f(r["lo"]), _f(r["hi"]))
            for r in csv.DictReader(f)
            if _f(r["value"]) is not None
        }


@cache
def x0() -> dict:
    out = {}
    for k, d in json.loads((REPO / "docs/depth/x0_numbers.json").read_text()).items():
        nums = [
            float(x.replace("−", "-"))
            for x in re.findall(r"[−-]?\d+\.\d+", str(d.get("text", "") if isinstance(d, dict) else d))
        ]
        if nums:
            out[k] = (nums[0], nums[1] if len(nums) > 2 else None, nums[2] if len(nums) > 2 else None)
    return out


def s(model: str, quantity: str, figure: str | None = None, prefix: bool = False):
    """A data/figures/depth/data.csv cell by model and quantity (exact, or the first quantity starting with it)."""
    for (fig, m, q), v in story().items():
        if m == model and (figure is None or fig == figure) and (q.startswith(quantity) if prefix else q == quantity):
            return v
    return None


def s_match(model: str, pattern: str, figure: str | None = None):
    """(quantity, cell) of the first story row whose quantity matches the regex."""
    for (fig, m, q), v in story().items():
        if m == model and (figure is None or fig == figure) and re.match(pattern, q):
            return q, v
    return None


def b(key: str):
    return breadth().get(key)


def x(key: str):
    return x0().get(key)


@cache
def writeup_data() -> dict:
    """data/figures/writeup/data.csv (scripts/writeup_data.py) by key: (value, lo, hi)."""
    path = REPO / "data" / "figures" / "writeup" / "data.csv"
    if not path.exists():
        return {}
    with path.open() as f:
        return {r["key"]: (_f(r["value"]), _f(r["lo"]), _f(r["hi"])) for r in csv.DictReader(f)}


def w(key: str):
    """A write-up data cell (value, lo, hi), or None."""
    return writeup_data().get(key)


@cache
def _ns() -> dict:
    path = REPO / "data" / "figures" / "writeup" / "data.csv"
    if not path.exists():
        return {}
    with path.open() as f:
        return {r["key"]: int(r["n"]) for r in csv.DictReader(f) if r["n"]}


def writeup_n(key: str) -> int | None:
    return _ns().get(key)


@cache
def _quantities() -> dict:
    path = REPO / "data" / "figures" / "writeup" / "data.csv"
    if not path.exists():
        return {}
    with path.open() as f:
        return {r["key"]: r["quantity"] for r in csv.DictReader(f)}


_PRINTED: set = set()


@cache
def _csv_rows() -> dict:
    with (REPO / "data/figures/depth/data.csv").open(newline="") as f:
        return {(r["figure"], r["model"], r["quantity"]): r for r in csv.DictReader(f)}


def _num(x: str):
    try:
        return float(x)
    except ValueError:
        return None


def row_value(figure: str, model: str, quantity: str):
    """(value, lo, hi) from data.csv; every row read is printed once with its source, so the plotted numbers can be checked."""
    r = _csv_rows()[(figure, model, quantity)]
    v, lo, hi = _num(r["value"]), _num(r["lo"]), _num(r["hi"])
    if (figure, model, quantity) not in _PRINTED:
        _PRINTED.add((figure, model, quantity))
        print(f"{figure} | {model} | {quantity} = {r['value']}" + (f" [{r['lo']}, {r['hi']}]" if r["lo"] else "") + f" n={r['n']} | {r['source']}")
    return v, lo, hi


def _shift_cells(path: str, model: str) -> list[tuple[float, float]]:
    """(shift, random) at dose 2 for the five start lockers, from a verdict's cells (the 27B and the 122B have no data.csv rows)."""
    d = json.loads((REPO / path).read_text())
    m = next(x for x in d["models"] if x["target"] == model)
    out = []
    for k in range(1, 6):
        c = m["cells"]["shifts"][f"2|v|{k}"]
        print(f"{path} | {model} | shifts 2|v|{k} (n={c['n']}) shift={c['shift'][0]} random={c['random'][0]}")
        out.append((c["shift"][0], c["random"][0]))
    return out


def _layers(model: str, figure: str, pattern: str) -> list[int]:
    return sorted({int(m.group(1)) for (f, mo, q) in story() if f == figure and mo == model and (m := re.match(pattern, q))})


# ---- controls -----------------------------------------------------------------------------------------------------------
def largest(m: str) -> tuple[str, float] | None:
    """Zach's largest same-size control in M - K, as (key, value): the max of rotated (rot), logit lens (u) and PCA (pc,
    or the size-matched ratio x mk)."""
    pc, pcr, mk = b(f"ko.{m}.pc"), b(f"ko.{m}.pcr"), b(f"ko.{m}.mk")
    vals = {k: v[0] for k, v in (("rot", b(f"ko.{m}.rot")), ("u", b(f"ko.{m}.u"))) if v}
    if pc:
        vals["pc"] = pc[0]
    elif pcr and mk:
        vals["pc"] = pcr[0] * mk[0]
    return max(vals.items(), key=lambda kv: kv[1]) if vals else None


def ctrl(m: str) -> float | None:
    """The value of the largest same-size control in M - K (see largest)."""
    top = largest(m)
    return top[1] if top else None


def conflict(m: str, reader: str):
    key = {"recall": "rc", "lookup": "lk"}[reader]
    return x(f"{key}_excess_{SHORT.get(m, '-')}") or s(m, f"conflict: {reader}, switches lost beyond a random part")


LAYER_CTRL = (("pca", "PCA", "PCA directions (same size): recall extra loss"),
              ("wu", "logit lens", "logit-lens directions: recall extra loss"),
              ("rand", "random", "random lens directions: recall extra loss"))  # fmt: skip


def layer_largest(m: str):
    """The one-layer half's lens part and its largest same-size control: (lens cell, key, name, control cell); None where
    the model has no one-layer row (Lightning)."""
    lens = s(m, "J++ part: recall extra loss", "fig02")
    ctrls = [(key, name, s(m, q, "fig02")) for key, name, q in LAYER_CTRL]
    ctrls = [c for c in ctrls if c[2]]
    if not lens or not ctrls:
        return None
    key, name, cell = max(ctrls, key=lambda c: c[2][0])
    return lens, key, name, cell


# ---- the depth README's quantities -------------------------------------------------------------------------------------
BOTH_Q = "post hoc, original locker sentence {} the pick, changed {}: lookups switched by the whole change"
ORDER_Q = "lookups switched by the whole change, locker sentence {}"
ZACH_L = {"qwen3.5-9b": 12, "qwen3.6-27b": 32, "muse-glimmer-30b": 26, "nemotron-3.5-lightning": 14}
ZACH_Q = "Zach's passages, L{}: lookups switched by the whole change, fact-{}"
DEPTH = {"qwen3.5-9b": 32, "qwen3.6-27b": 64, "muse-glimmer-30b": 52, "nemotron-3.5-lightning": 52, "qwen3.5-122b-a10b": 48}
GATE = 0.30
SWITCHES = "our removal, his passages: lookup switches under the whole change"
TWO_BY_TWO = [
    ("locker scenes", "our removal, our scenes (main test): gap",
     "our removal, our scenes (main test): the control (a random part of the same size instead), recall minus lookup"),
    ("fact passages", "our removal, his passages: gap",
     "our removal, his passages: the control (a random part of the same size instead), recall minus lookup"),
    ("locker scenes", "Zach's operation, our scenes (rung 6): recall's cost minus the lookup's, every scene",
     "Zach's operation, our scenes (rung 6): the control (a random part of the same size instead), recall minus lookup, "
     "every scene (kept with none minus kept with the random part)"),
    ("fact passages", "Zach's operation, his passages: his stored recall minus lookup",
     "Zach's operation, his passages: his rotated-direction control, recall minus lookup"),
]  # fmt: skip

# ---- the example scene (scripts/examples.py's E1 rule) ---------------------------------------------------------------
E1_RUN = REPO / "results/x0_necessity/x0_necessity_27b_chat"


@cache
def e1_words(n: int) -> tuple[str, ...]:
    """The last n words of E1's scene up to and including its bridge word (E1: the main test's first scene in its
    per-item file, Qwen 27B, at the main test's layer), for the tools figure's token axis."""
    layer = int(json.loads((REPO / "docs/depth/x0_numbers.json").read_text())["layer_27b"]["text"])
    with (E1_RUN / "outcomes.jsonl").open() as f:
        first = next(r["scene"] for r in map(json.loads, f) if r["layer"] == layer)
    with (E1_RUN / "cases.jsonl").open() as f:
        case = next(c for c in map(json.loads, f) if c["scene"] == first and c["rendering"] == "chat")
    asked = re.match(r"Which locker belongs to (\w+)'s pick", case["readers"]["PP"]["question"]).group(1)
    sentence = f"{asked} picked the {case['bridge']}"
    end = case["context"].index(sentence) + len(sentence)
    return tuple(case["context"][:end].split()[-n:])


# ---- words the builders fill in --------------------------------------------------------------------------------------------
READ_ALOUD = ("read: on {model}, removing the lens part everywhere drops recall {recall} points and lookup {lookup}; the gap is {gap}, "
              "the largest same-size control's {ctrl}")  # fmt: skip
RULE_BAR = "bar fixed in advance: {}"
