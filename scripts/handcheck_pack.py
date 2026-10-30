"""Hand-check pack (Dan, 26 Oct): six Qwen3.5-9B headline numbers at layer 12, each recounted item by item from its
run's per-item files (cases.jsonl, outcomes.jsonl; no verdict or aggregate file is read) and compared with
data/figures/depth/data.csv at 2 decimals; then 10 items per number (random.Random(0).sample over the recount's items sorted
by scene) shown as the model saw them: each prompt decoded token by token from its stored ids with the pinned tokenizer,
the token where the change is added marked ⟦word⟧, and per arm the stored outcome with its answer token decoded.
Items, prompts and tokens come from the review dashboard's code (src/bridge_jspace/review/). CPU only.

After the six, the batch-45 additions (Dan, 26 Oct ~21:45; UNVERIFIED): 45a's routes with a pick sentence prepended (9B,
V0 vs V2), 45b's bridge-word vs locker-sentence patches (9B, 27B) and 45d's refit removal in the table format (Muse).
Their runs are not in docs/review/review_views.yaml: each has its own loader from the run's per-item files, its recount is
compared with the run's verdict / table file (not in data.csv), and 5 items each are drawn the same way.

Then 45m, 45q and 45p (Dan 27 Oct ~14:40; UNVERIFIED), each on the 9B, the 27B and Muse (each test's rule counts all
three): each part loads its run's per-item files, recounts the rule's numbers against the verdict file the predictions
cite, and shows 10 items drawn as the six numbers draw, with the patched positions marked from the stored ones
(⟦bridge:…⟧, ⟦locker:…⟧, ⟦new:…⟧, ⟦control:…⟧, as the 45p verify pack) and each arm's stored answer for both readers.
The stored positions are re-derived from the decoded tokens and compared, for every item of every run.

uv run python scripts/handcheck_pack.py      # docs/review/handcheck_pack.md (generated; do not hand-edit)
"""

from __future__ import annotations

import math
import random
import re
import subprocess
import sys
import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.review import checks as C
from bridge_jspace.review import items as I
from bridge_jspace.review.recount import data_csv
from scripts import x0_necessity as X
from scripts import x0_strata as ST

MODEL, LAYER = "qwen3.5-9b", 12
OUT = I.REPO / "docs" / "review" / "handcheck_pack.md"
N_SHOW, SEED = 10, 0
READERS = ("PP", "PM")
NAME = {"PP": "lookup", "PM": "recall"}
X0_RUN = "results/x0_necessity/qwen35_9b_x0_necessity"
RT_RUN = "results/x6_routes/qwen35_9b_x6_routes"
X8_RUN = "results/x8_write/qwen35_9b_x8_write"
# stored arm -> the review view's label for it (docs/review/review_views.yaml)
X0_ARMS = {"whole": "whole", "no_part": "without J++", "no_rand": "without a same-size random part (control)"}
RT_ARMS = {
    "whole": "whole",
    "no_alf": "without the pointer directions",
    "no_alf_rand": "without the pointer's random part",
}
ROUTES = ("identity", "position", "value", "original", "other")
X8_CLASSES = ("target", "original", "third", "other")
NUM = re.compile(r"[−-]?\d+(?:\.\d+)?")
SPACE = "␣"


@dataclass
class Number:
    no: int
    title: str
    claim: str
    keys: tuple[str, ...]  # the headline's data.csv keys (the summary rows)
    source: str
    table: list[list[str]]
    notes: list[str]
    checks: list[dict]
    every: list[list[str]]
    pool: list[dict]
    card: Callable[[dict], list[str]]
    sample: list[dict] = field(default_factory=list)

    def headline(self) -> list[dict]:
        got = [c for c in self.checks if c["key"] in self.keys]
        assert [c["key"] for c in got] == list(self.keys), (self.no, self.keys)
        return got


# ------------------------------------------------------------------------------------------------ numbers and data.csv
def f2(x: float) -> str:
    return f"{x:.2f}".replace("-", "−")


def f4(x: float) -> str:
    return f"{x:.4f}".replace("-", "−")


def ci(v: float, lo_hi: tuple[float, float]) -> str:
    return f"{f2(v)} [{f2(lo_hi[0])}, {f2(lo_hi[1])}]"


def check(key: str, recount: str) -> dict:
    """The recount written as data.csv writes it (2 decimals and its CI, a count, a percentage) against data.csv's
    numbers row of the key: every number in the two texts equal."""
    data = data_csv()[0].get(key)

    def nums(s: str) -> list[str]:
        return [x.replace("−", "-") for x in NUM.findall(s)]

    ok = data is not None and nums(data) == nums(recount)
    return {"key": key, "recount": recount, "data": "(no row)" if data is None else data, "match": ok}


def yes(ok: bool) -> str:
    return "yes" if ok else "**no**"


def share_ci(hits: list[int], entities: list[str]) -> tuple[float, float]:
    """The share's 95% interval, cluster bootstrap over the bridge entity as the runs' verdicts (10,000 draws, seed 0)."""
    return X.interval(X.resampled_rates({"x": hits}, entities)["x"])


# ----------------------------------------------------------------------------------------- the main test (x0, 1 2 6)
def x0_pool() -> list[dict]:
    """The main test's scenes, one item per scene with both readers' rows (the review's main_swap view)."""
    got = sorted((it for it in I.items("main_swap", MODEL) if it["reader"] == "PP"), key=lambda it: it["scene"])
    assert got, "no main-test items"
    for it in got:
        assert (it["run"], it["layer"]) == (X0_RUN, LAYER), it["id"]
        assert all(it["rows"][w][lab] is not None for w in READERS for lab in ("unedited", *X0_ARMS.values())), it["id"]
    return got


def order_of(it: dict) -> str:
    """Where the original bridge's locker sentence sits relative to the asked pick (x0_strata, the keys' split)."""
    return ST.features(it["case"])["org locker vs asked pick"]


def gap(pool: list[dict]) -> dict:
    """Per reader S_arm = k / n and the extra loss (1 - S_no_part / S_whole) - (1 - S_no_rand / S_whole); the gap =
    recall's - lookup's; intervals on paired resamples of both readers (X.resampled_rates, as the runs)."""
    n = len(pool)
    sw = {(w, a): [int(it["rows"][w][lab]["switched"]) for it in pool] for w in READERS for a, lab in X0_ARMS.items()}
    k = {key: sum(v) for key, v in sw.items()}
    s = {key: v / n for key, v in k.items()}
    lost = {(w, a): float(X.dependence(s[(w, "whole")], s[(w, a)])) for w in READERS for a in ("no_part", "no_rand")}
    ex = {w: lost[(w, "no_part")] - lost[(w, "no_rand")] for w in READERS}
    ents = [it["rows"]["PP"]["whole"]["entity"] for it in pool]
    rr = X.resampled_rates({f"{w}|{a}": v for (w, a), v in sw.items()}, ents)
    boot = {w: X.dependence(rr[f"{w}|whole"], rr[f"{w}|no_part"]) - X.dependence(rr[f"{w}|whole"], rr[f"{w}|no_rand"])
            for w in READERS}  # fmt: skip
    return {"n": n, "k": k, "s": s, "lost": lost, "ex": ex, "ex_ci": {w: X.interval(boot[w]) for w in READERS},
            "gap": ex["PM"] - ex["PP"], "gap_ci": X.interval(boot["PM"] - boot["PP"])}  # fmt: skip


def gap_table(g: dict) -> tuple[list[list[str]], list[str]]:
    n, k, s = g["n"], g["k"], g["s"]
    rows = [["reader", "n", "S_whole", "S_no_part (without J++)", "S_no_rand (without a same-size random part (control))",
             "1 − S_no_part / S_whole", "1 − S_no_rand / S_whole", "extra loss [CI]"]]  # fmt: skip
    for w in READERS:
        rows.append([NAME[w], str(n), *(f"{k[(w, a)]}/{n} = {s[(w, a)]:.3f}" for a in X0_ARMS),
                     f4(g["lost"][(w, "no_part")]), f4(g["lost"][(w, "no_rand")]), ci(g["ex"][w], g["ex_ci"][w])])  # fmt: skip
    rows.append(["gap (recall − lookup)", "", "", "", "", "", "", f"**{ci(g['gap'], g['gap_ci'])}**"])
    arith = [f"{NAME[w]}: (1 − {k[(w, 'no_part')]}/{k[(w, 'whole')]}) − (1 − {k[(w, 'no_rand')]}/{k[(w, 'whole')]}) = "
             f"({k[(w, 'no_rand')]} − {k[(w, 'no_part')]}) / {k[(w, 'whole')]} = {f4(g['ex'][w])}" for w in READERS]  # fmt: skip
    arith.append(f"gap = {f4(g['ex']['PM'])} − ({f4(g['ex']['PP'])}) = {f4(g['gap'])} → {f2(g['gap'])}")
    return rows, arith


def x0_every(pool: list[dict]) -> list[list[str]]:
    head = ["scene", "bridge → changed", "order", *(f"{NAME[w]} {a}" for w in READERS for a in X0_ARMS)]
    rows = [[it["scene"], f"{it['case']['bridge']} → {it['case']['cf_bridge']}", order_of(it),
             *(str(it["rows"][w][lab]["switched"]) for w in READERS for lab in X0_ARMS.values())] for it in pool]  # fmt: skip
    total = ["**total switched**", "", "", *(str(sum(int(it["rows"][w][lab]["switched"]) for it in pool))
                                            for w in READERS for lab in X0_ARMS.values())]  # fmt: skip
    return [head, *rows, total]


def role_agrees(pool: list[dict]) -> tuple[int, int]:
    rows = [r for it in pool for w in READERS for r in it["rows"][w].values() if r is not None]
    return sum(bool(r["switched"]) == (r["role"] == "b") for r in rows), len(rows)


def number_gap(no: int, pool: list[dict], title: str, claim: str, key: str, prefix: str, extra: list[str]) -> Number:
    g = gap(pool)
    table, arith = gap_table(g)
    agree, rows = role_agrees(pool)
    notes = [
        "Extra loss per reader: " + "; ".join(arith) + ".",
        "Every S counts all n items, also those the whole change did not switch (an arm can switch an item the whole "
        "change left alone). CI: cluster bootstrap over the original bridge entity, 10,000 resamples, seed 0, both "
        "readers on the same draws (the runs' own X.resampled_rates).",
        f"Cross-check: the stored `switched` equals (stored role = b) on {agree} of {rows} stored rows.",
    ]
    if prefix == "sbo_swap_before":
        checks = [check(key, ci(g["gap"], g["gap_ci"])),
                  check(f"{prefix}_lk_9b", ci(g["ex"]["PP"], g["ex_ci"]["PP"])),
                  check(f"{prefix}_rc_9b", ci(g["ex"]["PM"], g["ex_ci"]["PM"])),
                  check(f"{prefix}_n_9b", str(g["n"])),
                  check(f"{prefix}_lksw_9b", f"{100 * g['s'][('PP', 'whole')]:.0f}%")]  # fmt: skip
    else:
        checks = [check(key, ci(g["gap"], g["gap_ci"])),
                  *(check(f"{'lk' if w == 'PP' else 'rc'}_excess_9b", ci(g["ex"][w], g["ex_ci"][w])) for w in READERS),
                  *(check(f"{'lk' if w == 'PP' else 'rc'}_{name}_9b", str(g["k"][(w, a)])) for w in READERS
                    for a, name in (("whole", "whole"), ("no_part", "noj"), ("no_rand", "norand")))]  # fmt: skip
    return Number(no, title, claim, (key,), X0_RUN, table, extra + notes, checks, x0_every(pool), pool, card_x0)


def number_order(pool: list[dict]) -> Number:
    groups = {o: [it for it in pool if order_of(it) == o] for o in ("before", "after")}
    other = [it for it in pool if order_of(it) not in groups]
    table = [
        ["original bridge's locker sentence vs the asked pick", "n", "lookups switched by the whole change", "share"]
    ]
    checks = []
    for o, mine in groups.items():
        k = sum(int(it["rows"]["PP"]["whole"]["switched"]) for it in mine)
        table.append([o, str(len(mine)), str(k), f"{100 * k / len(mine):.0f}%"])
        checks += [check(f"lk_order_{o}_9b_k", str(k)), check(f"lk_order_{o}_9b_n", str(len(mine))),
                   check(f"lk_order_{o}_9b", f"{100 * k / len(mine):.0f}%")]  # fmt: skip
    dash = sum(I.sentence_order(it["case"])["original"] == order_of(it) for it in pool)
    notes = [f"Split: scripts/x0_strata.py features 'org locker vs asked pick' (the keys' source, x0_details); {len(other)} "
             f"scenes in neither group. Cross-check: the review dashboard's own split (items.sentence_order) agrees on "
             f"{dash} of {len(pool)} scenes."]  # fmt: skip
    every = [["scene", "order", "locker sentence / asked pick (sentence no.)", "lookup whole: role", "switched"]]
    for it in pool:
        lk, pk = sentence_numbers(it["case"])
        r = it["rows"]["PP"]["whole"]
        every.append([it["scene"], order_of(it), f"{lk} / {pk}", r["role"], str(r["switched"])])
    every.append(["**total switched**", "", "", "", " · ".join(f"{r[0]} {r[2]}" for r in table[1:])])
    return Number(2, "Sentence order: lookups switched, locker sentence before vs after the asked pick",
                  "On the 9B's main test the whole change switches 86 of 100 lookups where the original bridge's locker "
                  "sentence comes before the asked person's pick sentence, and 19 of 100 where it comes after.",
                  ("lk_order_before_9b_k", "lk_order_after_9b_k"), X0_RUN, table, notes, checks, every, pool,
                  card_order)  # fmt: skip


# ----------------------------------------------------------------------------------------------- routes (x6, 3 4)
def routes_pool() -> list[dict]:
    """The routes test's C2 scenes (another item moved), the lookup's rows; whole / no_alf / no_alf_rand are from the
    main run (the keep-only run joined by the review view is not used here)."""
    got = sorted((it for it in I.items("routes", MODEL) if it["reader"] == "PP" and it["condition"] == "C2"),
                 key=lambda it: it["scene"])  # fmt: skip
    assert got, "no routes items"
    for it in got:
        assert (it["run"], it["layer"]) == (RT_RUN, LAYER), it["id"]
        for lab in ("unedited", *RT_ARMS.values()):
            r = it["rows"]["PP"][lab]
            assert r is not None, (it["id"], lab)
            assert "_run" not in r, (it["id"], lab)  # from the main run, not the joined keep-only run
    return got


def c2_expect(case: dict) -> dict[str, int]:
    """The digit each route predicts, from the two prompts: identity = the changed pick's locker in O; position = O's
    digit in the slot where the changed pick's locker sentence sits in S; value = its new digit in S; original = O's
    answer (x6_routes.scenes, C2)."""
    o, s = C.LOCKER.findall(case["context"]), C.LOCKER.findall(case["cf_context"])
    b = case["cf_bridge"]
    slot = [x for x, _ in s].index(b)
    return {"identity": int(dict(o)[b]), "position": int(o[slot][1]), "value": int(dict(s)[b]),
            "original": int(dict(o)[case["bridge"]])}  # fmt: skip


def decoded(top: int, model: str = MODEL) -> str:
    return C.piece(model, top).strip()


def arm_name(arm: str) -> str:
    return arm if RT_ARMS[arm] == arm else f"{RT_ARMS[arm]} ({arm})"


def route_counts(pool: list[dict], arm: str) -> dict[str, int]:
    return {rt: sum(I.route_class(it["rows"]["PP"][RT_ARMS[arm]], "C2") == rt for it in pool) for rt in ROUTES}


def decoded_agrees(pool: list[dict], arms: list[str]) -> tuple[int, int]:
    """The route re-derived from the decoded top token and the case's expect, against the stored route."""
    pairs = [(it, it["rows"]["PP"][RT_ARMS[a]]) for it in pool for a in arms]
    return sum(C.route_of(decoded(r["top"]), it["case"]["expect"], "C2") == r["route"] for it, r in pairs), len(pairs)


def routes_every(pool: list[dict], arms: list[str]) -> list[list[str]]:
    head = ["scene", "bridge → changed pick", *(f"{a}: route (decoded top)" for a in arms)]
    rows = [[it["scene"], f"{it['case']['bridge']} → {it['case']['cf_bridge']}",
             *(f"{it['rows']['PP'][RT_ARMS[a]]['route']} ({decoded(it['rows']['PP'][RT_ARMS[a]]['top'])})" for a in arms)]
            for it in pool]  # fmt: skip
    totals = [", ".join(f"{rt} {c}" for rt, c in route_counts(pool, a).items()) for a in arms]
    return [head, *rows, ["**totals**", "", *totals]]


def number_routes(pool: list[dict]) -> Number:
    n = len(pool)
    k = route_counts(pool, "whole")
    ents = [it["rows"]["PP"]["whole"]["entity"] for it in pool]
    table = [["route of the lookup's answer (whole change)", "k of n", "share [CI]", "key"]]
    checks = []
    for rt in ROUTES:
        hits = [int(it["rows"]["PP"]["whole"]["route"] == rt) for it in pool]
        text = ci(k[rt] / n, share_ci(hits, ents))
        key = f"rt_C2_whole_{rt}_9b" if rt != "other" else ""
        table.append([rt, f"{k[rt]}/{n}", text, key or "(none)"])
        if key:
            checks.append(check(key, text))
    agree, total = decoded_agrees(pool, ["whole"])
    same = sum(c2_expect(it["case"]) == it["case"]["expect"] for it in pool)
    notes = [f"Cross-checks: the route re-derived from the decoded top token agrees with the stored route on {agree} of "
             f"{total} rows; the stored expect (the digit per route) equals the one re-derived from the two prompts on "
             f"{same} of {n} scenes. CI: cluster bootstrap over the bridge item, 10,000 resamples, seed 0."]  # fmt: skip
    return Number(3, "Routes, C2 (another item moved): which digit the lookup gives under the whole change",
                  "On the 9B, when another item moved, the lookup follows the moved item's identity 0.48, its locker "
                  "sentence's position 0.51, and never the new value (0.00).",
                  ("rt_C2_whole_identity_9b", "rt_C2_whole_position_9b", "rt_C2_whole_value_9b"), RT_RUN, table, notes,
                  checks, routes_every(pool, ["whole"]), pool,
                  lambda it: card_routes(it, ["whole"]))  # fmt: skip


def number_pointer(pool: list[dict]) -> Number:
    n = len(pool)
    ents = [it["rows"]["PP"]["whole"]["entity"] for it in pool]
    table = [["arm", *ROUTES, "position share [CI]", "key"]]
    checks = []
    for arm in RT_ARMS:
        k = route_counts(pool, arm)
        hits = [int(it["rows"]["PP"][RT_ARMS[arm]]["route"] == "position") for it in pool]
        text = ci(k["position"] / n, share_ci(hits, ents))
        key = f"rt_C2_{arm}_position_9b"
        table.append([arm_name(arm), *(f"{k[rt]}/{n}" for rt in ROUTES), text, key])
        checks.append(check(key, text))
    agree, total = decoded_agrees(pool, list(RT_ARMS))
    notes = [f"Cross-check: the route re-derived from the decoded top token agrees with the stored route on {agree} of "
             f"{total} rows (three arms). The pointer directions: 4 directions fit on the probe's fresh scenes (Alf); "
             "the random part has the same share of the change's squared norm."]  # fmt: skip
    return Number(4, "Position without the pointer directions vs without a random part of their size",
                  "On the 9B, C2: without the pointer directions the lookup gives the position answer in 0.08 of scenes, "
                  "without a random part of the same share in 0.54.",
                  ("rt_C2_no_alf_position_9b", "rt_C2_no_alf_rand_position_9b"), RT_RUN, table, notes, checks,
                  routes_every(pool, list(RT_ARMS)), pool,
                  lambda it: card_routes(it, list(RT_ARMS)))  # fmt: skip


# ------------------------------------------------------------------------------------------------- writes (x8, 5)
def x8_pool(kind: str, s: int) -> list[dict]:
    got = [it for it in I.items("x8_writes", MODEL)
           if it["reader"] == "PP" and it["x8"]["kind"] == kind and it["x8"]["s"] == s]  # fmt: skip
    for it in got:
        assert (it["run"], it["layer"]) == (X8_RUN, LAYER), it["id"]
    return sorted(got, key=lambda it: (it["scene"], it["x8"]["k"]))


def slot_digits(case: dict) -> list[str]:
    return [d for _, d in C.LOCKER.findall(case["context"])]


def x8_class(it: dict, top: int) -> str:
    """The class re-derived from the decoded top token: slot k's digit = target, slot j's = original (x8_write.classify)."""
    d, digits, j, k = decoded(top), slot_digits(it["case"]), it["x8"]["j"], it["x8"]["k"]
    third = ({0, 1, 2} - {j, k}).pop()
    return next((n for n, s in (("target", k), ("original", j), ("third", third)) if d == digits[s]), "other")


def x8_row(it: dict) -> dict:
    return it["rows"]["PP"][f"{it['x8']['kind']} s = {it['x8']['s']:g}"]


def number_write(pool: list[dict]) -> Number:
    table = [["arm", "s", "n (scenes × 2 target slots)", *X8_CLASSES, "target share [CI]", "key"]]
    checks = []
    for kind, s, key in (("write", 2, "x8_t2_9b"), ("random", 1, "x8_rand1_9b"), ("random", 4, "x8_rand4_9b")):
        mine = pool if (kind, s) == ("write", 2) else x8_pool(kind, s)
        k = {c: sum(x8_row(it)["class"] == c for it in mine) for c in X8_CLASSES}
        hits = [int(x8_row(it)["class"] == "target") for it in mine]
        text = ci(k["target"] / len(mine), share_ci(hits, [x8_row(it)["entity"] for it in mine]))
        what = "write" if kind == "write" else "random direction (control)"
        table.append([what, str(s), str(len(mine)), *(str(k[c]) for c in X8_CLASSES), text, key])
        checks.append(check(key, text))
    agree = sum(x8_class(it, x8_row(it)["top"]) == x8_row(it)["class"] for it in pool)
    joined = sum(C.check_joined(it)[0] == C.PASS for it in pool)
    rand_s = I.read_json(f"{X8_RUN}/manifest.json")["rand_s"]
    assert 2 not in rand_s, rand_s
    notes = [f"Cross-checks: the class re-derived from the decoded top token agrees with the stored class on {agree} of "
             f"{len(pool)} writes at s = 2; the stored entity is the joined routes case's bridge and j its locker slot on "
             f"{joined} of {len(pool)}. The run has no random direction at s = 2 (its manifest: rand_s = {rand_s}); the "
             "controls are the random directions of the same norm at s = 1 and 4. CI: cluster bootstrap over the bridge "
             "item, 10,000 resamples, seed 0."]  # fmt: skip
    every = [["scene", "j → k (slot of the bridge → slot written to)", "slot digits", "top (decoded)", "class"]]
    for it in pool:
        r = x8_row(it)
        every.append([it["scene"], f"{it['x8']['j']} → {it['x8']['k']}", " ".join(slot_digits(it["case"])),
                      decoded(r["top"]), r["class"]])  # fmt: skip
    every.append(["**totals**", "", "", "", ", ".join(f"{c} {sum(x8_row(it)['class'] == c for it in pool)}"
                                                     for c in X8_CLASSES)])  # fmt: skip
    return Number(5, "The write at s = 2: the lookup's target share",
                  "On the 9B, writing 2 (μ_k − μ_j) at the bridge word (μ = the pointer's class means of slots k and j) "
                  "sends the lookup to locker k in 0.46 of writes (all slot pairs).",
                  ("x8_t2_9b",), X8_RUN, table, notes, checks, every, pool, card_write)  # fmt: skip


# ------------------------------------------------------------------------------------------------------- the cards
def prompt(ids: list[int], pos: int | None, model: str = MODEL, runs: list[tuple[int, int]] | tuple = ()) -> list[str]:
    """The prompt decoded token by token (exactly the full decode), ⟦ ⟧ around the token at pos, « » around each
    token run [start, end) in runs, ␣ = the space token the read appends (chat read: one forward of the prompt plus a
    digit's space token; not stored in cases.jsonl). A marked token's leading whitespace stays outside the marks."""
    parts = [C.piece(model, t) for t in ids]
    assert "".join(parts) == C.tokenizer(model).decode(ids, skip_special_tokens=False), "per-token decode differs"

    def wrap(i: int, j: int, opening: str, closing: str) -> None:
        core = parts[i].lstrip()
        parts[i] = parts[i][: len(parts[i]) - len(core)] + opening + core
        parts[j - 1] += closing

    for i, j in runs:
        assert pos is None or not i <= pos < j, "the bridge token inside a marked run"
        wrap(i, j, "«", "»")
    if pos is not None:
        wrap(pos, pos + 1, "⟦", "⟧")
    return ["```text", "".join(parts) + SPACE, "```", ""]


def recall_tail(case: dict) -> list[str]:
    a, b = case["readers"]["PP"]["ids"]["org"], case["readers"]["PM"]["ids"]["org"]
    i = next(i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y)
    assert i > case["pos"]
    return [f"Recall prompt: the same first {i} tokens (so the same ⟦{case['bridge']}⟧ at token {case['pos']}), then:",
            "", "```text", C.tokenizer(MODEL).decode(b[i:], skip_special_tokens=False) + SPACE, "```", ""]  # fmt: skip


def token_diffs(case: dict, model: str = MODEL) -> str:
    o, a = case["readers"]["PP"]["ids"]["org"], case["readers"]["PP"]["ids"]["alt"]
    if len(o) != len(a):
        return f"the prompts have {len(o)} and {len(a)} tokens"
    return "; ".join(f"{i}: `{C.piece(model, x)!r}` → `{C.piece(model, y)!r}`" for i, (x, y) in enumerate(zip(o, a, strict=True)) if x != y)  # fmt: skip


def prompts(case: dict, changed: bool = True, recall: bool = False) -> list[str]:
    out = [f"Original prompt, lookup (the model reads this; ⟦ ⟧ = token {case['pos']}, where the change is added):", "",
           *prompt(case["readers"]["PP"]["ids"]["org"], case["pos"])]  # fmt: skip
    if recall:
        out += recall_tail(case)
    if changed:
        out += [f"Changed prompt, lookup (the change, its state minus the original's at layer {LAYER}, is taken at token "
                f"{case['pos']}):", "", *prompt(case["readers"]["PP"]["ids"]["alt"], case["pos"]),
                f"Tokens that differ (index: original → changed): {token_diffs(case)}.", ""]  # fmt: skip
    return out


def md_table(rows: list[list[str]]) -> list[str]:
    def cell(x: str) -> str:
        return x.replace("|", "\\|")

    return ["| " + " | ".join(map(cell, rows[0])) + " |", "|" + "---|" * len(rows[0]),
            *("| " + " | ".join(map(cell, r)) + " |" for r in rows[1:])]  # fmt: skip


def x0_answer(case: dict, w: str, r: dict) -> str:
    rd = case["readers"][w]
    if r["role"] == "A":
        return f"`{C.piece(MODEL, rd['tok_A'])!r}` original answer"
    if r["role"] == "b":
        return f"`{C.piece(MODEL, rd['tok_b'])!r}` changed answer"
    return "another token (the run stores no top token)"


def card_x0(it: dict) -> list[str]:
    c = it["case"]
    exp = " ".join(f"{NAME[w].capitalize()}: {c['readers'][w]['question']} original answer {c['readers'][w]['answer']} "
                   f"(token `{C.piece(MODEL, c['readers'][w]['tok_A'])!r}`), changed answer {c['readers'][w]['cf_answer']} "
                   f"(token `{C.piece(MODEL, c['readers'][w]['tok_b'])!r}`)." for w in READERS)  # fmt: skip
    rows = [
        [
            "reader",
            "arm",
            "stored role",
            "switched",
            "answer token (decoded from the role)",
            "p(original)",
            "p(changed)",
        ]
    ]
    for w in READERS:
        for lab in ("unedited", *X0_ARMS.values()):
            r = it["rows"][w][lab]
            rows.append([NAME[w], "before the change" if lab == "unedited" else lab, r["role"], str(r["switched"]),
                         x0_answer(c, w, r), f"{r['p_org']:.3f}", f"{r['p_alt']:.3f}"])  # fmt: skip
    return [*prompts(c, recall=True), f"Expected: {exp}", "", *md_table(rows)]


def sentence_numbers(case: dict) -> tuple[int, int]:
    """1-based sentence numbers of the original bridge's locker sentence and the asked pick (as x0_strata splits)."""
    sents = [s if s.endswith(".") else s + "." for s in case["context"].split(". ")]
    asked = re.search(r"([A-Z][a-z]+)'s pick", case["readers"]["PP"]["question"]).group(1)  # type: ignore[union-attr]
    pick = next(i for i, s in enumerate(sents) if s.startswith(f"{asked} picked"))
    lock = next(i for i, s in enumerate(sents)
                if s.startswith("The locker of") and re.search(rf"\b{re.escape(case['bridge'])}\b", s))  # fmt: skip
    return lock + 1, pick + 1


def card_order(it: dict) -> list[str]:
    c = it["case"]
    lk, pk = sentence_numbers(c)
    sents = [s if s.endswith(".") else s + "." for s in c["context"].split(". ")]
    listed = " ".join(f"({i}) {s}" for i, s in enumerate(sents, 1))
    rows = [["arm", "stored role", "switched", "answer token (decoded from the role)", "p(original)", "p(changed)"]]
    for lab in ("unedited", "whole"):
        r = it["rows"]["PP"][lab]
        rows.append(["before the change" if lab == "unedited" else lab, r["role"], str(r["switched"]),
                     x0_answer(c, "PP", r), f"{r['p_org']:.3f}", f"{r['p_alt']:.3f}"])  # fmt: skip
    return [*prompts(c), f"Sentences of the original context: {listed}", "",
            f"The original bridge {c['bridge']}'s locker sentence is ({lk}), the asked pick is ({pk}): **{order_of(it)}**. "
            f"Lookup: original answer {c['readers']['PP']['answer']}, changed answer {c['readers']['PP']['cf_answer']}.",
            "", *md_table(rows)]  # fmt: skip


def route_expect(c: dict) -> str:
    """The digit each C2 route predicts, with where it comes from in the two prompts."""
    o = C.LOCKER.findall(c["context"])
    s = C.LOCKER.findall(c["cf_context"])
    b = c["cf_bridge"]
    slot = [x for x, _ in s].index(b)
    e = c["expect"]
    return (f"identity {e['identity']} ({b}'s locker in the original prompt); position {e['position']} (the original "
            f"prompt's locker sentence {slot + 1}, {o[slot][0]}'s: where {b}'s locker sentence sits in the changed prompt); "
            f"value {e['value']} ({b}'s new locker in the changed prompt, not in the original); original {e['original']} "
            f"({c['bridge']}'s locker, the original answer). Re-derived from the two prompts: "
            f"{'the same' if c2_expect(c) == e else 'DIFFERENT: ' + str(c2_expect(c))}.")  # fmt: skip


def card_routes(it: dict, arms: list[str]) -> list[str]:
    c = it["case"]
    e = c["expect"]
    exp = route_expect(c)
    rows = [["arm", "top token (decoded)", "stored route", "route re-derived from the decoded token"]]
    for a in ("none", *arms):
        r = it["rows"]["PP"]["unedited" if a == "none" else RT_ARMS[a]]
        name = "before the change" if a == "none" else arm_name(a)
        rows.append([name, f"`{C.piece(MODEL, r['top'])!r}`", r["route"], C.route_of(decoded(r["top"]), e, "C2")])
    return [*prompts(c), f"Lookup: {c['readers']['PP']['question']} The digit each route predicts: {exp}", "",
            *md_table(rows)]  # fmt: skip


def card_write(it: dict) -> list[str]:
    c, x8 = it["case"], it["x8"]
    slots = C.LOCKER.findall(c["context"])
    j, k = x8["j"], x8["k"]
    third = ({0, 1, 2} - {j, k}).pop()
    listed = "; ".join(f"slot {n}: the {x} → {d}" for n, (x, d) in enumerate(slots))
    rows = [["arm", "top token (decoded)", "stored class", "class re-derived from the decoded token"]]
    for lab, r in it["rows"]["PP"].items():
        rows.append([lab if lab != "unwritten" else "no write", f"`{C.piece(MODEL, r['top'])!r}`", r["class"],
                     x8_class(it, r["top"]) if lab != "unwritten" else "–"])  # fmt: skip
    return [*prompts(c, changed=False),
            f"Lookup: {c['readers']['PP']['question']} Locker sentences in order: {listed}. The write adds "
            f"{x8['s']:g} (μ_{k} − μ_{j}) at token {c['pos']} (norm {x8['norm']}), moving the pointer from slot {j} "
            f"(the bridge {c['bridge']}'s) to slot {k}: target {slots[k][1]}, original {slots[j][1]}, third "
            f"{slots[third][1]}. (No changed prompt: the write is a fixed vector. Without a write the stored class names "
            "the slot whose digit the answer is.)", "", *md_table(rows)]  # fmt: skip


# ------------------------------------------------------------------------------------- batch 45 (after the six numbers)
# Dan 26 Oct ~21:45. None of these runs is in docs/review/review_views.yaml: each has its own loader from the run's per-item
# files, and each recount is compared with the run's verdict / table file (not in data/figures/depth/data.csv).
N_SHOW_45 = 5
X45A_RUN = "results/x6_routes/qwen35_9b_x6_routes_x45a"
X45A_TABLE = "results/x6_routes/x45a-descriptive-20261026T202236Z/table.json"
X45A_SHOWN = ("V0", "V2")
X45B_RUNS = {"qwen3.5-9b": "results/x45b_binding/qwen35_9b_x45b_binding",
             "qwen3.6-27b": "results/x45b_binding/x45b_binding_27b"}  # fmt: skip
X45B_RATES = ("a", "b_half", "c", "d")  # the arms Dan asked for; none and S beside them as sanity
X45B_SHOWN = ("none", "a", "b_half", "c", "d", "S")
X45B_ALL = ("none", "a", "b_half", "b_quarter", "c", "d", "S")  # every arm the run reads (each item has all)
X45D_RUN, X45D_MODEL, X45D_FORMAT = "results/x0b_generalize/muse30b_x45d", "muse-glimmer-30b", "table"
X45D_ARMS = {
    "none": ("-", "none"),
    "whole": ("-", "whole"),
    "no_part": ("pcf", "no_part"),
    "no_rand": ("pcf", "no_rand"),
}
X45D_NAME = {"none": "before the change", "whole": "whole", "no_part": "without the refit basis (pcf no_part)",
             "no_rand": "without a same-size random part (control) (pcf no_rand)"}  # fmt: skip
LABEL = {"qwen3.5-9b": "Qwen3.5-9B", "qwen3.6-27b": "Qwen3.6-27B", "muse-glimmer-30b": "Muse Glimmer 30B"}
FLOAT_TOL = 1e-9  # the files store full-precision floats; the recount uses the same arithmetic


@dataclass
class Addition:
    tag: str
    title: str
    what: str
    model: str
    source: str
    ref: str
    items: str
    table: list[list[str]]
    notes: list[str]
    checks: list[dict]  # what, recount, file, match, head (a headline row)
    pool: list[dict]
    card: Callable[[dict], list[str]]
    sample: list[dict] = field(default_factory=list)


def newest(run: str, pattern: str) -> str:
    found = sorted((I.REPO / run).glob(pattern))
    assert found, f"{run}: no {pattern}"
    return str(found[-1].relative_to(I.REPO))


def kn(k: int, n: int) -> str:
    return f"{k} of {n}, {k / n:.2f}"


def check45(what: str, recount: str, file: str, ok: bool, head: bool = False) -> dict:
    return {"what": what, "recount": recount, "file": file, "match": ok, "head": head}


def role_of(top: int, rd: dict) -> str:
    """X0's role of a top token: b = the changed (S) answer's token, A = the original's, other."""
    return "b" if top == rd["tok_b"] else "A" if top == rd["tok_A"] else "other"


def runs_of(positions: list[int]) -> list[tuple[int, int]]:
    """Sorted token positions as maximal runs [start, end)."""
    out: list[tuple[int, int]] = []
    for p in sorted(positions):
        if out and out[-1][1] == p:
            out[-1] = (out[-1][0], p + 1)
        else:
            out.append((p, p + 1))
    return out


# 45a: first mention or first locker (x6_routes --prepend), the 9B
def x45a_pool() -> list[dict]:
    """45a's rule set, as x45a_descriptive.route_table: the base scenes present in every variant (lookup rows of the
    whole and keep_alf arms) whose pointer move involves slot 0 (to or from the first locker); one item per base scene
    with its case and lookup rows per variant."""
    cases = {(c["base_scene"], c["variant"]): c for c in I.read_jsonl(f"{X45A_RUN}/cases.jsonl")}
    lk = [r for r in I.read_jsonl(f"{X45A_RUN}/outcomes.jsonl") if r["reader"] == "PP" and r.get("variant")]
    rows = {(r["base_scene"], r["variant"], r["arm"]): r for r in lk}
    variants = sorted({r["variant"] for r in lk})
    ruled = [r for r in lk if r["arm"] in ("whole", "keep_alf")]
    bases = set.intersection(*({r["base_scene"] for r in ruled if r["variant"] == v} for v in variants))
    first = sorted({r["base_scene"] for r in ruled if 0 in r["move"]} & bases)
    return [{"scene": b, "id": b, "model": MODEL, "move": rows[(b, "V0", "whole")]["move"],
             "cases": {v: cases[(b, v)] for v in X45A_SHOWN},
             "rows": {(v, a): rows[(b, v, a)] for v in X45A_SHOWN for a in ("none", "whole")}} for b in first]  # fmt: skip


def x45a_number(pool: list[dict]) -> Addition:
    n = len(pool)
    ref = I.read_json(X45A_TABLE)[Path(X45A_RUN).name]["routes"]
    k = {v: {rt: sum(it["rows"][(v, "whole")]["route"] == rt for it in pool) for rt in ROUTES} for v in X45A_SHOWN}
    table = [["route (lookup, whole change)", *(f"{v}: k of n, share" for v in X45A_SHOWN),
              *(f"table.json {v}" for v in X45A_SHOWN)]]  # fmt: skip
    checks = [check45("n (base scenes in every variant, first-locker moves)", str(n), str(ref["n"]), n == ref["n"])]
    for rt in ROUTES:
        file = {v: ref["share"][f"whole|{v}"][rt] for v in X45A_SHOWN}
        table.append([rt, *(kn(k[v][rt], n) for v in X45A_SHOWN), *(f"{file[v]:.4f}" for v in X45A_SHOWN)])
        for v in X45A_SHOWN:
            ok = abs(k[v][rt] / n - file[v]) <= FLOAT_TOL
            checks.append(check45(f"{v} whole: {rt}", kn(k[v][rt], n), f"{file[v]:.4f}", ok, head=rt == "identity"))
    pairs = [(it, v, it["rows"][(v, a)]) for it in pool for v in X45A_SHOWN for a in ("none", "whole")]
    agree = sum(C.route_of(decoded(r["top"]), it["cases"][v]["expect"], "C2") == r["route"] for it, v, r in pairs)
    exp = sum(c2_expect(it["cases"][v]) == it["cases"][v]["expect"] for it in pool for v in X45A_SHOWN)
    pre = sum(it["cases"]["V2"]["context"].startswith(it["cases"]["V2"]["prepended"] + " ") for it in pool)
    notes = [f"Cross-checks: the route re-derived from the decoded top token agrees with the stored route on {agree} of "
             f"{len(pairs)} rows (V0 and V2, before the change and whole); the stored expect equals the one re-derived "
             f"from the two prompts on {exp} of {2 * n} cases; V2's original context starts with its prepended pick "
             f"sentence in {pre} of {n}.",
             "The table is descriptive, after the data (Dan 26 Oct ~21:20 / ~21:25; scripts/x45a_descriptive.py), not "
             "45a's rule (which reads the pointer part only, keep_alf)."]  # fmt: skip
    return Addition("A", "45a on the 9B: the whole change's routes with a pick sentence prepended (V0 vs V2)",
                    "Routes C2 scenes with one sentence before the context: V0 none (the control, a rerun), V2 a new "
                    "person's pick of a locker item other than the first. On the first-locker moves, the whole change's "
                    "lookup answers by route (identity 0.54 in V0, 0.96 in V2 in the table).",
                    MODEL, X45A_RUN, X45A_TABLE,
                    f"the {n} base scenes present in every variant V0-V4 whose pointer move (the original bridge's locker "
                    "slot → the changed pick's) involves slot 0", table, notes, checks, pool, card_45a)  # fmt: skip


def card_45a(it: dict) -> list[str]:
    m = it["move"]
    out = [f"The pointer's move: slot {m[0]} → slot {m[1]} (the original bridge's locker slot → the changed pick's; "
           "slots counted from 0).", ""]  # fmt: skip
    for v in X45A_SHOWN:
        c = it["cases"][v]
        what = "nothing prepended" if v == "V0" else f"prepended: “{c['prepended']}”"
        out += [f"**{v}** ({what}). Original prompt O, lookup (the model reads this; ⟦ ⟧ = token {c['pos']}, where "
                "the change is added):", "", *prompt(c["readers"]["PP"]["ids"]["org"], c["pos"]),
                f"The changed prompt S (the change is taken from it at token {c['pos']}) differs from O at tokens: "
                f"{token_diffs(c)}.", ""]  # fmt: skip
    c0, c2 = it["cases"]["V0"], it["cases"]["V2"]
    same = "the same in V2" if c2["expect"] == c0["expect"] else f"V2: {c2['expect']}"
    rows = [["variant", "arm", "top token (decoded)", "stored route", "route re-derived from the decoded token"]]
    for v in X45A_SHOWN:
        for a in ("none", "whole"):
            r = it["rows"][(v, a)]
            rows.append([v, "before the change" if a == "none" else a, f"`{C.piece(MODEL, r['top'])!r}`", r["route"],
                         C.route_of(decoded(r["top"]), it["cases"][v]["expect"], "C2")])  # fmt: skip
    return [*out, f"Lookup: {c0['readers']['PP']['question']} The digit each route predicts (V0): {route_expect(c0)} "
            f"Expect {same}.", "", *md_table(rows)]  # fmt: skip


# 45b: where the binding is made when the locker comes after the pick (x45b_binding), the 9B and the 27B
def x45b_pool(model: str) -> list[dict]:
    """Every item of the run (cases.jsonl: the main test's locker-after items), with the lookup's row per arm."""
    run = X45B_RUNS[model]
    rows = {(r["scene"], r["arm"]): r for r in I.read_jsonl(f"{run}/outcomes.jsonl") if r["reader"] == "PP"}
    out = []
    for c in sorted(I.read_jsonl(f"{run}/cases.jsonl"), key=lambda c: c["scene"]):
        assert all((c["scene"], a) in rows for a in X45B_ALL), c["scene"]
        out.append({"scene": c["scene"], "id": c["scene"], "model": model, "run": run, "case": c,
                    "rows": {a: rows[(c["scene"], a)] for a in X45B_ALL}})  # fmt: skip
    return out


def x45b_number(model: str, pool: list[dict]) -> Addition:
    run = X45B_RUNS[model]
    ref_path = newest(run, "verdict-*/verdict.json")
    ref = I.read_json(ref_path)["readers"]["PP"]
    n = len(pool)
    hits = {a: sum(int(it["rows"][a]["switched"]) for it in pool) for a in X45B_ALL}
    n_s = hits["S"]
    of_s = {
        a: sum(int(it["rows"][a]["switched"]) & int(it["rows"]["S"]["switched"]) for it in pool) for a in ("c", "d")
    }
    layers = I.read_json(f"{run}/manifest.json")["arm_layers"]
    table = [["arm", "layer", "lookups switched: k of n, share", "verdict.json", "matches"]]
    checks = [check45("n (items)", str(n), str(ref["n"]), n == ref["n"])]
    for a in ("none", *X45B_RATES, "S"):
        ok = hits[a] == ref["hits"][a] and abs(hits[a] / n - ref["rate"][a][0]) <= FLOAT_TOL
        file = f"{ref['hits'][a]} of {ref['n']}, {ref['rate'][a][0]:.2f}"
        table.append([a, str(layers.get(a, "–")), kn(hits[a], n), file, yes(ok)])
        checks.append(check45(f"{a}: switched", kn(hits[a], n), file, ok, head=a in X45B_RATES))
    for a in ("c", "d"):
        ok = (of_s[a], n_s) == (ref["hits_of_S"][a], ref["S_switched"]) and abs(
            of_s[a] / n_s - ref["of_S"][a][0]
        ) <= FLOAT_TOL
        file = f"{ref['hits_of_S'][a]} of {ref['S_switched']}, {ref['of_S'][a][0]:.2f}"
        table.append([f"{a} among S's switches", str(layers[a]), kn(of_s[a], n_s), file, yes(ok)])
        checks.append(check45(f"{a}: share of S's switches", kn(of_s[a], n_s), file, ok))
    rows = [(it, it["rows"][a]) for it in pool for a in X45B_ALL]
    text = sum(C.piece(model, r["top"]) == r["top_text"] for _, r in rows)
    role = sum(role_of(r["top"], it["case"]["readers"]["PP"]) == r["role"] for it, r in rows)
    sw = sum(int(r["switched"]) == int(r["role"] == "b") for _, r in rows)
    notes = [f"Cross-checks over all {len(rows)} lookup rows ({len(X45B_ALL)} arms, b_quarter included): the decoded top "
             f"token equals the stored top_text on {text}; the role re-derived from the top token (S's answer's token "
             f"= b, O's = A) equals the stored role on {role}; switched equals (role = b) on {sw}.",
             f"Switch rate = k / n over all {n} items; c / d among S's switches = (items both S and the arm switch) / "
             "(items S switches). Rule (fixed in advance, scripts/x45b_binding.py): holds if c or d switches at least "
             "half of S's switches while a stays at or below 0.25."]  # fmt: skip
    short = LABEL[model].split("-")[-1]
    return Addition(f"B · {short}", f"45b on the {short}: the bridge word (a, b_half) vs the locker sentences (c, d)",
                    "On the main test's items whose original bridge's locker sentence comes after the asked pick: (a) the "
                    "bridge-word change at L, (b_half) at L/2, (c) S's states patched into O at every locker-sentence "
                    "token at L, (d) the same at L/2; S read on S. Lookup switch rates, and c / d as a share of S's "
                    "switches.", model, run, ref_path,
                    f"all {n} items of the run (cases.jsonl)", table, notes, checks, pool, card_45b)  # fmt: skip


def card_45b(it: dict) -> list[str]:
    c, m = it["case"], it["model"]
    rd = c["readers"]["PP"]
    layers = I.read_json(f"{it['run']}/manifest.json")["arm_layers"]
    what = {"none": "O unedited", "a": "bridge word, at L", "b_half": "bridge word, at L/2",
            "c": "S patched into the locker sentences, at L", "d": "S patched into the locker sentences, at L/2",
            "S": "S read on S, unedited"}  # fmt: skip
    rows = [["arm", "what", "layer", "top token (decoded)", "stored top_text", "stored role", "switched"]]
    for a in X45B_SHOWN:
        r = it["rows"][a]
        rows.append([a, what[a], str(layers.get(a, "–")), f"`{C.piece(m, r['top'])!r}`", f"`{r['top_text']!r}`",
                     r["role"], str(r["switched"])])  # fmt: skip
    return [f"O prompt, lookup ({LABEL[m]}; ⟦ ⟧ = token {c['pos']}, the bridge word, where a and b_half add the change; "
            f"« » = the {len(c['patched'])} locker-sentence tokens where c and d patch S's states in):", "",
            *prompt(rd["ids"]["org"], c["pos"], m, runs_of(c["patched"])),
            f"S (the swapped prompt: the changes are taken from it, and arm S reads it) differs from O at tokens: "
            f"{token_diffs(c, m)}.", "",
            f"Lookup: {rd['question']} O's answer {rd['answer']} (token `{C.piece(m, rd['tok_A'])!r}`), S's answer "
            f"{rd['cf_answer']} (token `{C.piece(m, rd['tok_b'])!r}`); a switch = the top token is S's answer's token "
            "(role b).", "", *md_table(rows)]  # fmt: skip


# 45d: the refit removal on Muse, the table format (x0b_generalize, pcf)
def x45d_pool() -> list[dict]:
    """The table-format scenes of the run at its layer, the lookup's rows: before the change, whole, and the refit
    basis's no_part / no_rand (as x0b_generalize.pcf_cells: the format from cases.jsonl by scene)."""
    cases = {c["scene"]: c for c in I.read_jsonl(f"{X45D_RUN}/cases.jsonl")}
    layer = I.read_json(f"{X45D_RUN}/manifest.json")["predicted"]
    rows: dict[tuple[str, str], dict] = {}
    for r in I.read_jsonl(f"{X45D_RUN}/outcomes.jsonl"):
        if r["layer"] != layer or r["reader"] != "PP" or cases[r["scene"]]["format"] != X45D_FORMAT:
            continue
        for name, key in X45D_ARMS.items():
            if (r["dict"], r["arm"]) == key:
                assert (r["scene"], name) not in rows, (r["scene"], name)
                rows[(r["scene"], name)] = r
    scenes = sorted({s for s, name in rows if name == "whole"})
    return [{"scene": s, "id": s, "model": X45D_MODEL, "layer": layer, "case": cases[s],
             "rows": {name: rows[(s, name)] for name in X45D_ARMS}} for s in scenes]  # fmt: skip


def x45d_number(pool: list[dict]) -> Addition:
    ref_path = newest(X45D_RUN, "x45d-*/verdict.json")
    blob = I.read_json(ref_path)
    cell = next(c for c in blob["cells"] if (c["format"], c["part"], c["reader"]) == (X45D_FORMAT, "pcf", "PP"))
    n = len(pool)
    sw = {a: [int(it["rows"][a]["switched"]) for it in pool] for a in ("whole", "no_part", "no_rand")}
    k = {a: sum(v) for a, v in sw.items()}
    s = {a: v / n for a, v in k.items()}
    ex = float(X.dependence(s["whole"], s["no_part"]) - X.dependence(s["whole"], s["no_rand"]))
    rr = X.resampled_rates(sw, [it["rows"]["whole"]["entity"] for it in pool])
    lo_hi = X.interval(X.dependence(rr["whole"], rr["no_part"]) - X.dependence(rr["whole"], rr["no_rand"]))
    file_k = {a: round(cell[f"S_{a}"][0] * cell["n"]) for a in ("no_part", "no_rand")}
    table = [["arm", "lookups switched: k of n, share", f"verdict.json ({X45D_FORMAT}, pcf, lookup)", "matches"]]
    checks = [check45("n (table-format items)", str(n), str(cell["n"]), n == cell["n"])]
    ok = k["whole"] == cell["switched_whole"]
    table.append(["whole", kn(k["whole"], n), f"switched_whole {cell['switched_whole']} of {cell['n']}", yes(ok)])
    checks.append(check45("whole: switched", kn(k["whole"], n), f"{cell['switched_whole']} of {cell['n']}", ok))
    for a in ("no_part", "no_rand"):
        ok = k[a] == file_k[a]
        file = f"S_{a} {cell[f'S_{a}'][0]:.4f} × {cell['n']} = {file_k[a]}"
        table.append([X45D_NAME[a], kn(k[a], n), file, yes(ok)])
        checks.append(check45(f"{X45D_NAME[a]}: switched", kn(k[a], n), file, ok))
    ok = all(abs(x - y) <= FLOAT_TOL for x, y in zip([ex, *lo_hi], cell["excess"], strict=True))
    ok &= blob["lookup_refit"][X45D_FORMAT] == cell["excess"]
    recount = f"({k['no_rand']} − {k['no_part']}) / {k['whole']} = {ci(ex, lo_hi)}"
    file = f"{ci(cell['excess'][0], (cell['excess'][1], cell['excess'][2]))}, {cell['switched_whole']} switched of {cell['n']}"
    table.append(["extra loss", recount, file, yes(ok)])
    checks.append(check45("extra loss (the rule's number)", recount, file, ok, head=True))
    rows = [(it, it["rows"][a]) for it in pool for a in X45D_ARMS]
    role = sum(role_of(r["top"], it["case"]["readers"]["PP"]) == r["role"] for it, r in rows)
    swr = sum(int(r["switched"]) == int(r["role"] == "b") for _, r in rows)
    notes = [f"Extra loss = (switches lost without the basis − lost without a same-size random part (control)) / whole switches = "
             f"(1 − {k['no_part']}/{k['whole']}) − (1 − {k['no_rand']}/{k['whole']}) = ({k['no_rand']} − {k['no_part']})"
             f" / {k['whole']} = {f4(ex)}. CI: cluster bootstrap over the bridge item, 10,000 resamples, seed 0 (the "
             "run's X.resampled_rates).",
             f"Cross-checks over all {len(rows)} lookup rows (4 arms): the role re-derived from the decoded top token "
             f"equals the stored role on {role}; switched equals (role = b) on {swr}.",
             "Items: the held-out half (per format, the bridge items not used to fit the basis) as the run built it; "
             f"layer {pool[0]['layer']}. Rule fixed in advance (batch45.yaml, 45d); the 30-switch minimum per format "
             "was decided after the first 45d results (Dan 26 Oct ~21:20) and does not touch this cell."]  # fmt: skip
    return Addition("C", "45d on Muse: the refit removal in the table format",
                    "Removing the refit basis (rank 4, fit on the other half of the varied scenes) costs the lookup in "
                    "the table format: extra loss 0.47 [0.34, 0.60] in the verdict.", X45D_MODEL, X45D_RUN, ref_path,
                    f"the {n} table-format items of the run (held-out half), the lookup", table, notes, checks, pool,
                    card_45d)  # fmt: skip


def card_45d(it: dict) -> list[str]:
    c, m = it["case"], it["model"]
    rd = c["readers"]["PP"]
    rows = [["arm", "top token (decoded)", "stored role", "role re-derived from the decoded token", "switched"]]
    for a in X45D_ARMS:
        r = it["rows"][a]
        rows.append([X45D_NAME[a], f"`{C.piece(m, r['top'])!r}`", r["role"], role_of(r["top"], rd), str(r["switched"])])
    return [f"{c['format']} format, level {c['level']}, {c['domain']}; the original bridge's locker {c['order']} the "
            f"pick. Original prompt, lookup ({LABEL[m]}; the model reads this; ⟦ ⟧ = token {c['pos']}, where the change "
            f"is added at layer {it['layer']}):", "", *prompt(rd["ids"]["org"], c["pos"], m),
            f"The changed prompt (the change is taken from it at token {c['pos']}) differs at tokens: {token_diffs(c, m)}.",
            "", f"Lookup: {rd['question']} Original answer {rd['answer']} (token `{C.piece(m, rd['tok_A'])!r}`), changed "
            f"answer {rd['cf_answer']} (token `{C.piece(m, rd['tok_b'])!r}`).", "", *md_table(rows)]  # fmt: skip


# ------------------------------------------------------------------- 45m, 45q, 45p (Dan 27 Oct ~14:40; after batch 45)
# Each test's rule counts the 9B, the 27B and Muse, so each model is its own part (as 45b's 9B and 27B above), with
# N_SHOW items drawn as the six numbers draw. Every prompt is marked from the run's stored positions, and those are
# re-derived from the decoded tokens and compared, for every item of the run. Each recount is compared with the verdict
# file the predictions cite (predictions/2026-10-26_dan.md, Q45.10 / Q45.12 / Q45.13).
QPM_MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b")
SHORT = {"qwen3.5-9b": "9B", "qwen3.6-27b": "27B", "muse-glimmer-30b": "Muse"}
X45M_RUNS = {"qwen3.5-9b": "results/x0_necessity/qwen35_9b_x45m_fresh",
             "qwen3.6-27b": "results/x0_necessity/x45m_fresh_27b",
             "muse-glimmer-30b": "results/x0_necessity/muse30b_x45m_fresh"}  # fmt: skip
X45M_REF = "results/x0_necessity/x45m-20261026T230628Z/x45m.json"
X45M_GROUPS = ("locker-before", "locker-after", "all")
X45M_LABEL = {"none": "unedited", **X0_ARMS}  # stored arm -> the main test's label, so gap() recounts 45m as test 1
X45Q_RUNS = {"qwen3.5-9b": "results/x45b_binding/qwen35_9b_x45q", "qwen3.6-27b": "results/x45b_binding/x45q_27b",
             "muse-glimmer-30b": "results/x45b_binding/muse30b_x45q"}  # fmt: skip
X45Q_REF = "results/x45b_binding/x45q-20261027T005345Z/x45q.json"
X45Q_LINK_REF = "results/x45b_binding/x45q-link-20261027T005346Z/link.json"
X45Q_ARMS = ("none", "a", "b_half", "b_quarter", "c", "d", "c_nojpp", "c_norand", "S")
X45Q_RULE_ARMS = ("none", "a", "b_half", "b_quarter", "c", "d", "S")  # x45q.json's; the link arms are in link.json
X45Q_LINK_ARMS = ("none", "c", "c_nojpp", "c_norand", "S")
X45Q_WHAT = {"none": "O unedited", "a": "the bridge-word change, at L", "b_half": "the bridge-word change, at L/2",
             "b_quarter": "the bridge-word change, at L/4", "c": "S copied into every locker-sentence token, at L",
             "d": "S copied into every locker-sentence token, at L/2",
             "c_nojpp": "c without each token's J++ part (k = 25, signed)",
             "c_norand": "c without a random part of each token's J++ share", "S": "S read on S, unedited"}  # fmt: skip
X45P_RUNS = {"qwen3.5-9b": "results/x45p/qwen35_9b_x45p", "qwen3.6-27b": "results/x45p/x45p_27b",
             "muse-glimmer-30b": "results/x45p/muse30b_x45p"}  # fmt: skip
X45P_REF = "results/x45p/x45p-20261027T012017Z/x45p.json"
X45P_EXAMPLES = "results/x45p/x45p-20261027T012017Z/examples.md"
X45P_ARMS = ("none", "whole", "a1", "a2", "a3", "a4", "o2")
X45P_WHAT = {"none": "O unedited", "whole": "the whole change at the bridge word",
             "a1": "(1) base edit: the whole change minus its J++ part, at the bridge word",
             "a2": "(2) base edit + the new item's token(s) without their own J++ part",
             "a3": "(3) base edit + the same token(s) without a random part of the same share",
             "a4": "(4) base edit + the control item's token(s) without their own J++ part",
             "o2": "(2)'s item edit alone, no base edit"}  # fmt: skip
LOCKER_TEXT = re.compile(r"The locker of (?:the )?(.+?) is (.+?)\.")


def close(x: float, y: float) -> bool:
    return (math.isnan(x) and math.isnan(y)) or abs(x - y) <= FLOAT_TOL


def close_all(xs: list[float], ys: list[float]) -> bool:
    return len(xs) == len(ys) and all(close(float(x), float(y)) for x, y in zip(xs, ys, strict=True))


def ci_or_none(v: list[float]) -> str:
    return "undefined (the whole change switches none)" if math.isnan(v[0]) else ci(v[0], (v[1], v[2]))


def kn_ci(k: int, n: int, lo_hi: tuple[float, float] | list[float]) -> str:
    return f"{k} of {n}, {ci(k / n, (lo_hi[0], lo_hi[1]))}"


def marked_prompt(ids: list[int], model: str, marks: list[tuple[int, int, str]]) -> list[str]:
    """The prompt decoded token by token (exactly the full decode), ⟦label:…⟧ around each token run [start, end) in
    marks (as the 45p verify pack marks its examples), ␣ the space token the read appends. A run's leading whitespace
    stays outside its mark; runs must not overlap."""
    parts = [C.piece(model, t) for t in ids]
    assert "".join(parts) == C.tokenizer(model).decode(ids, skip_special_tokens=False), "per-token decode differs"
    last = -1
    for i, j, label in sorted(marks):
        assert last < i < j, f"marks overlap or are empty at token {i}"
        core = parts[i].lstrip()
        parts[i] = parts[i][: len(parts[i]) - len(core)] + f"⟦{label}:" + core
        parts[j - 1] += "⟧"
        last = j - 1
    return ["```text", "".join(parts) + SPACE, "```", ""]


def token_spans(ids: list[int], model: str) -> tuple[str, list[tuple[int, int]]]:
    """The prompt decoded token by token and each token's [start, end) characters in it."""
    parts = [C.piece(model, t) for t in ids]
    spans, at = [], 0
    for p in parts:
        spans.append((at, at + len(p)))
        at += len(p)
    return "".join(parts), spans


def over(spans: list[tuple[int, int]], a: int, b: int) -> list[int]:
    """The tokens whose (non-empty) characters overlap [a, b)."""
    return [i for i, (x, y) in enumerate(spans) if y > x and x < b and y > a]


def char_marks(spans: list[tuple[int, int]], positions: list[int]) -> list[list[int]]:
    """Each run of consecutive positions as the [start, end) characters it covers (the runs' stored 'marks')."""
    return [[spans[i][0], spans[j - 1][1]] for i, j in runs_of(positions)]


def bridge_bad(case: dict, model: str, bridge: str, new: str, last_marked: int) -> list[str]:
    """What disagrees with the stored bridge position: per reader, the tokens where O and S differ must be exactly
    [pos]; the token decodes to the bridge in O and to the new item in S; the recall's prompt equals the lookup's up to
    the last marked token (so the same positions are patched in both)."""
    bad, pos = [], case["pos"]
    for w in READERS:
        o, s = case["readers"][w]["ids"]["org"], case["readers"][w]["ids"]["alt"]
        diff = [i for i, (x, y) in enumerate(zip(o, s, strict=True)) if x != y] if len(o) == len(s) else None
        if diff != [pos]:
            bad.append(
                f"{NAME[w]}: O and S differ at {diff if diff is not None else 'different lengths'}, stored pos {pos}"
            )
    o, s = case["readers"]["PP"]["ids"]["org"], case["readers"]["PP"]["ids"]["alt"]
    if (C.piece(model, o[pos]).strip(), C.piece(model, s[pos]).strip()) != (bridge, new):
        bad.append(f"token {pos} decodes {C.piece(model, o[pos])!r} / {C.piece(model, s[pos])!r}, not {bridge} / {new}")
    a, b = case["readers"]["PP"]["ids"]["org"], case["readers"]["PM"]["ids"]["org"]
    if a[: last_marked + 1] != b[: last_marked + 1]:
        bad.append(f"the recall's prompt differs from the lookup's before token {last_marked}")
    return bad


def found_text(case: dict, model: str) -> tuple[str, list[tuple[int, int]], list[str]]:
    """The lookup's O decoded with each token's characters, and whether the stored rendered text is that decode."""
    text, spans = token_spans(case["readers"]["PP"]["ids"]["org"], model)
    stored = case["readers"]["PP"].get("text", {}).get("org")
    return text, spans, [] if stored is None or stored == text else ["the stored text is not the exact decode"]


def stored_rows(pool: list[dict], arms: tuple[str, ...]) -> tuple[int, list[str]]:
    """How many (item, reader, arm) answers are stored, and which are not."""
    missing = [f"{it['scene']} {NAME[w]} {a}" for it in pool for w in READERS for a in arms if it["rows"][w][a] is None]
    return len(pool) * len(READERS) * len(arms) - len(missing), missing


def rows_note(pool: list[dict], arms: tuple[str, ...]) -> str:
    have, missing = stored_rows(pool, arms)
    return (f"Stored answers: all {have} (item, reader, arm) rows are in outcomes.jsonl with a top token; none is "
            "recomputed." if not missing else
            f"Stored answers: {have} rows stored; NOT stored (shown as such on the cards): {', '.join(missing)}.")  # fmt: skip


def positions_check(pool: list[dict], what: str) -> tuple[dict, str]:
    """The items whose marked (stored) positions agree with the ones re-derived from the decoded tokens."""
    ok = sum(not it["bad"] for it in pool)
    bad = [f"{it['scene']}: {'; '.join(it['bad'])}" for it in pool if it["bad"]]
    note = f"Positions ({what}): agree on {ok} of {len(pool)} items." + (" Disagree: " + " · ".join(bad) if bad else "")
    got = check45("positions: marked = re-derived from the decoded tokens", f"{ok} of {len(pool)} items agree",
                  f"{len(pool)} items' stored positions", ok == len(pool), head=True)  # fmt: skip
    return {**got, "src": f"{pool[0]['run']}/cases.jsonl"}, note


def answer_cell(model: str, r: dict | None) -> str:
    return "not stored" if r is None else f"`{C.piece(model, r['top'])!r}`"


def expected(case: dict, model: str) -> str:
    return " ".join(f"{NAME[w].capitalize()}: {rd['question']} O's answer {rd['answer']} (token "
                    f"`{C.piece(model, rd['tok_A'])!r}`), S's answer {rd['cf_answer']} (token "
                    f"`{C.piece(model, rd['tok_b'])!r}`)." for w, rd in ((w, case["readers"][w]) for w in READERS))  # fmt: skip


def shared_tail(case: dict, model: str) -> list[str]:
    """The recall's O prompt after the tokens it shares with the lookup's."""
    a, b = case["readers"]["PP"]["ids"]["org"], case["readers"]["PM"]["ids"]["org"]
    i = next(i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y)
    return [f"O, recall: the same first {i} tokens (every mark above included), then:", "", "```text",
            C.tokenizer(model).decode(b[i:], skip_special_tokens=False) + SPACE, "```", ""]  # fmt: skip


def positions_line(it: dict, found: str) -> str:
    verdict = "**agree**" if not it["bad"] else "**DISAGREE**: " + "; ".join(it["bad"])
    return f"Positions, stored vs re-derived from the decoded tokens: {found} {verdict}."


def s_line(case: dict, model: str) -> str:
    return (f"S (both readers' prompts): O with these tokens changed (index: O → S): {token_diffs(case, model)}; every "
            "other token the same.")  # fmt: skip


# 45m: the clean one-pick design (x0_necessity --alt fresh): only the bridge token differs between O and S
def group_45m(case: dict) -> str:
    """locker-before / locker-after / mixed: the bridge's and the new item's locker sentences vs the asked pick
    (x0_strata's features, as 45m groups its scenes)."""
    f = ST.features(case)
    o, a = f["org locker vs asked pick"], f["alt locker vs asked pick"]
    return "locker-before" if o == a == "before" else "locker-after" if o == a == "after" else "mixed"


def x45m_pool(model: str) -> list[dict]:
    """45m's scored scenes: the chat cases with outcomes at the run's layer, one item per scene with both readers' rows
    (none, whole, and J++ k = 25 signed's no_part / no_rand) under the main test's labels."""
    run = X45M_RUNS[model]
    layer = I.read_json(f"{run}/manifest.json")["predicted"]
    cases = {c["scene"]: c for c in I.read_jsonl(f"{run}/cases.jsonl") if c["rendering"] == "chat"}
    rows: dict[tuple[str, str, str], dict] = {}
    for r in I.read_jsonl(f"{run}/outcomes.jsonl"):
        if r["rendering"] != "chat" or r["layer"] != layer or r["arm"] not in X45M_LABEL:
            continue
        if r["arm"] in ("no_part", "no_rand") and (r["dict"], r["k"], r["omp"]) != X.MAIN:
            continue
        key = (r["scene"], r["reader"], X45M_LABEL[r["arm"]])
        assert key not in rows, key
        rows[key] = r
    out = []
    for s in sorted({s for s, _, lab in rows if lab == "whole"}):
        c = cases[s]
        out.append({"scene": s, "id": s, "model": model, "run": run, "layer": layer, "case": c, "group": group_45m(c),
                    "bridge": c["bridge"], "new": c["cf_bridge"], "bad": bridge_bad(c, model, c["bridge"],
                                                                                    c["cf_bridge"], c["pos"]),
                    "rows": {w: {lab: rows.get((s, w, lab)) for lab in X45M_LABEL.values()} for w in READERS}})  # fmt: skip
    return out


def x45m_number(model: str, pool: list[dict]) -> Addition:
    ref = next(m for m in I.read_json(X45M_REF)["models"] if m["target"] == model)
    assert ref["run"] == Path(X45M_RUNS[model]).name, ref["run"]
    labs = list(X45M_LABEL.values())
    assert not stored_rows(pool, tuple(labs))[1], "45m: a stored row is missing; the recount needs every arm"
    table = [["scenes", "n", *(f"{NAME[w]} switched: whole / without J++ / without a same-size random part (control)" for w in READERS),
              *(f"{NAME[w]} extra loss [CI]" for w in READERS), "gap [CI]", "x45m.json gap", "matches"]]  # fmt: skip
    checks = []
    for g in X45M_GROUPS:
        mine = pool if g == "all" else [it for it in pool if it["group"] == g]
        cell = ref["cells"][g]
        with warnings.catch_warnings():  # an extra loss is nan where the whole change switches none (all-nan draws)
            warnings.simplefilter("ignore", RuntimeWarning)
            res = gap(mine)
        n, k = res["n"], res["k"]
        ok_k = n == cell["n"] and all(
            k[(w, "whole")] == cell[NAME[w]]["switched_whole"]
            and all(k[(w, a)] == round(cell[NAME[w]][f"S_{a}"][0] * n) for a in ("no_part", "no_rand"))
            for w in READERS)  # fmt: skip
        ex = {w: [res["ex"][w], *res["ex_ci"][w]] for w in READERS}
        gp = [res["gap"], *res["gap_ci"]]
        ok_ex = {w: close_all(ex[w], cell[NAME[w]]["excess"]) for w in READERS}
        ok_gap = close_all(gp, cell["gap"])
        table.append([g, str(n), *(" / ".join(str(k[(w, a)]) for a in X0_ARMS) for w in READERS),
                      *(ci_or_none(ex[w]) for w in READERS), ci_or_none(gp), ci_or_none(cell["gap"]),
                      yes(ok_k and all(ok_ex.values()) and ok_gap)])  # fmt: skip
        checks.append(check45(f"{g}: n and switched counts (both readers, three arms)", f"n {n}",
                              f"n {cell['n']}, switched_whole and S_no_part / S_no_rand × n", ok_k))  # fmt: skip
        for w in READERS:
            checks.append(check45(f"{g}: {NAME[w]}'s extra loss", ci_or_none(ex[w]), ci_or_none(cell[NAME[w]]["excess"]),
                                  ok_ex[w], head=g == "locker-before" and w == "PP"))  # fmt: skip
        checks.append(check45(f"{g}: gap", ci_or_none(gp), ci_or_none(cell["gap"]), ok_gap, head=g == "locker-before"))
    pos_check, pos_note = positions_check(pool, "the marked bridge token is the only token where O and S differ, for "
                                                "both readers, and decodes to the bridge in O and to the new item in S")  # fmt: skip
    checks.append(pos_check)
    rows = [(it, w, it["rows"][w][lab]) for it in pool for w in READERS for lab in labs]
    role = sum(role_of(r["top"], it["case"]["readers"][w]) == r["role"] for it, w, r in rows)
    sw = sum(int(r["switched"]) == int(r["role"] == "b") for _, _, r in rows)
    groups = {g: sum(it["group"] == g for it in pool) for g in ("locker-before", "locker-after", "mixed")}
    notes = ["Extra loss per reader = (1 − k_no_part / k_whole) − (1 − k_no_rand / k_whole) = (k_no_rand − k_no_part) "
             "/ k_whole (X0's Jdep − Rdep); gap = recall's − lookup's. CI: cluster bootstrap over the bridge item, 10,000 "
             "resamples, seed 0, both readers on the same draws (X.resampled_rates, as the run's verdict).",
             f"Groups (x0_strata's features, as scripts/x45m.py): locker-before {groups['locker-before']}, locker-after "
             f"{groups['locker-after']}, mixed {groups['mixed']} (mixed only in 'all'). Rule (fixed in advance): in "
             "locker-before scenes the gap at least 0.3 and the lookup's extra loss at most 0.10, on at least 2 of 3 "
             "models.",
             f"Cross-checks over all {len(rows)} rows (both readers, {len(labs)} arms): the role re-derived from the "
             f"decoded top token (S's answer's token = b, O's = A) equals the stored role on {role}; switched equals "
             f"(role = b) on {sw}.", rows_note(pool, tuple(labs)), pos_note]  # fmt: skip
    short = SHORT[model]
    return Addition(f"45m · {short}", f"45m on the {short}: the clean one-pick design (Q45.10)",
                    "One locker item that nobody picks is added to both prompts and S's asked pick changes from the "
                    "bridge to it, so only the bridge token differs between O and S. The change (h_S − h_O at the bridge "
                    "word at the layer fixed in advance) whole, without its J++ part (k = 25, signed), and without a "
                    "random part of the same share; both readers. The rule reads the locker-before scenes.",
                    model, X45M_RUNS[model], X45M_REF,
                    f"the {len(pool)} scenes with outcomes at layer {pool[0]['layer']} (the run's eligible scenes)",
                    table, notes, checks, pool, card_45m)  # fmt: skip


def card_45m(it: dict) -> list[str]:
    c, m = it["case"], it["model"]
    f = ST.features(c)
    rows = [["reader", "arm", "top token (decoded)", "stored role", "role re-derived from the top token", "switched",
             "p(O's answer)", "p(S's answer)"]]  # fmt: skip
    for w in READERS:
        for lab in X45M_LABEL.values():
            r = it["rows"][w][lab]
            name = "before the change" if lab == "unedited" else lab
            rows.append([NAME[w], name, "not stored", "–", "–", "–", "–", "–"] if r is None else
                        [NAME[w], name, answer_cell(m, r), r["role"], role_of(r["top"], c["readers"][w]),
                         str(r["switched"]), f"{r['p_org']:.3f}", f"{r['p_alt']:.3f}"])  # fmt: skip
    pos = c["pos"]
    diff = {w: [i for i, (x, y) in enumerate(zip(c["readers"][w]["ids"]["org"], c["readers"][w]["ids"]["alt"],
                                                 strict=False)) if x != y] for w in READERS}  # fmt: skip
    return [f"**{it['group']}**: the bridge's locker sentence comes {f['org locker vs asked pick']} the asked pick, the "
            f"new item's {f['alt locker vs asked pick']}. Added locker sentence, in O and S: “{c['fresh']['sentence']}” "
            f"(the new item {c['fresh']['item']}: nobody picks it in O; in S the asked person picks it).", "",
            f"O, lookup ({LABEL[m]}; the model reads this; ⟦bridge:…⟧ = token {pos}, where the change is added at "
            f"layer {it['layer']}):", "", *marked_prompt(c["readers"]["PP"]["ids"]["org"], m, [(pos, pos + 1, "bridge")]),
            *shared_tail(c, m), s_line(c, m), "",
            positions_line(it, f"bridge: stored pos {pos}; the tokens where O and S differ: lookup {diff['PP']}, "
                               f"recall {diff['PM']}."), "",
            f"Expected: {expected(c, m)}", "", *md_table(rows)]  # fmt: skip


# 45q: on 45m's clean locker-after scenes, the bridge-word change vs S copied into the locker sentences (x45b_binding)
def lockers_found(case: dict, model: str) -> tuple[list[list[int]], list[str]]:
    """The locker sentences' tokens re-derived from the lookup's decoded O ('The locker of [the] <item> is <n>.' in the
    text, the tokens overlapping each), and what disagrees with the stored ones: the sentences, their positions, the
    patched and source positions, the character marks; and the bridge's stored position and mark."""
    text, spans, bad = found_text(case, model)
    found_m = list(LOCKER_TEXT.finditer(text))
    found = [over(spans, x.start(), x.end()) for x in found_m]
    if [x.group(0) for x in found_m] != case["lockers"]["sentences"]:
        bad.append(f"locker sentences {[x.group(0) for x in found_m]} ≠ stored {case['lockers']['sentences']}")
    if found != case["lockers"]["org"]:
        bad.append(f"locker tokens {found} ≠ stored {case['lockers']['org']}")
    if [p for f in found for p in f] != case["patched"] or case["source"] != case["patched"]:
        bad.append("the stored patched / source positions are not the locker tokens")
    if [x for f in found for x in char_marks(spans, f)] != case["marks"]["lockers"]:
        bad.append("the stored locker marks are not the locker tokens' characters")
    if [list(spans[case["pos"]])] != case["marks"]["bridge"]:
        bad.append("the stored bridge mark is not the bridge token's characters")
    if any(p == case["pos"] for f in found for p in f):
        bad.append("the bridge token is inside a locker sentence")
    last = max([case["pos"], *(p for f in found for p in f)])
    return found, bad + bridge_bad(case, model, case["entity"], case["cf_bridge"], last)


def x45q_pool(model: str) -> list[dict]:
    """Every item of the run (cases.jsonl: 45m's locker-after scenes), with both readers' rows for the arms shown."""
    run = X45Q_RUNS[model]
    rows: dict[tuple[str, str, str], dict] = {}
    for r in I.read_jsonl(f"{run}/outcomes.jsonl"):
        if r["arm"] in X45Q_ARMS:
            key = (r["scene"], r["reader"], r["arm"])
            assert key not in rows, key
            rows[key] = r
    out = []
    for c in sorted(I.read_jsonl(f"{run}/cases.jsonl"), key=lambda c: c["scene"]):
        found, bad = lockers_found(c, model)
        out.append({"scene": c["scene"], "id": c["scene"], "model": model, "run": run, "case": c,
                    "bridge": c["entity"], "new": c["cf_bridge"], "found": found, "bad": bad,
                    "rows": {w: {a: rows.get((c["scene"], w, a)) for a in X45Q_ARMS} for w in READERS}})  # fmt: skip
    return out


def x45q_number(model: str, pool: list[dict]) -> Addition:
    run = X45Q_RUNS[model]
    name = Path(run).name
    ref = next(m for m in I.read_json(X45Q_REF)["models"] if m["run"] == name)
    link = I.read_json(X45Q_LINK_REF)["runs"][name]["readers"]
    man = I.read_json(f"{run}/manifest.json")
    layers = {**man["arm_layers"], "c_nojpp": man["layer"], "c_norand": man["layer"]}
    assert not stored_rows(pool, X45Q_ARMS)[1], "45q: a stored row is missing; the recount needs every arm"
    n = len(pool)
    ents = [it["rows"]["PP"]["none"]["entity"] for it in pool]
    sw = {(w, a): [int(it["rows"][w][a]["switched"]) for it in pool] for w in READERS for a in X45Q_ARMS}
    for w in READERS:
        for a in ("c", "d"):
            sw[(w, f"{a}&S")] = [x & y for x, y in zip(sw[(w, a)], sw[(w, "S")], strict=True)]
    k = {key: sum(v) for key, v in sw.items()}
    boot = X.resampled_rates({f"{w}|{a}": v for (w, a), v in sw.items()}, ents)
    rate = {(w, a): [k[(w, a)] / n, *X.interval(boot[f"{w}|{a}"])] for w in READERS for a in X45Q_ARMS}
    of_s = {}
    for w in READERS:
        for a in ("c", "d"):
            with np.errstate(divide="ignore", invalid="ignore"):
                ratio = boot[f"{w}|{a}&S"] / np.where(boot[f"{w}|S"] > 0, boot[f"{w}|S"], np.nan)
            of_s[(w, a)] = [k[(w, f"{a}&S")] / k[(w, "S")], *X.interval(ratio)]
    file = ref["readers"]
    table = [["arm", "what", "layer", "lookup: switched, share [CI]", "recall: switched, share [CI]", "file (lookup)",
              "matches"]]  # fmt: skip
    checks = [check45("n (items)", str(n), str(file["PP"]["n"]), n == file["PP"]["n"] == file["PM"]["n"])]
    for a in X45Q_ARMS:
        ok, src = {}, {}
        for w in READERS:
            ok[w], src[w] = True, []
            if a in X45Q_RULE_ARMS:
                ok[w] &= k[(w, a)] == file[w]["hits"][a] and close_all(rate[(w, a)], file[w]["rate"][a])
                src[w].append(f"x45q.json {kn_ci(file[w]['hits'][a], n, file[w]['rate'][a][1:])}")
            if a in X45Q_LINK_ARMS:
                ok[w] &= close_all(rate[(w, a)], link[w][a])
                src[w].append(f"link.json {ci(link[w][a][0], (link[w][a][1], link[w][a][2]))}")
        texts = {w: kn_ci(k[(w, a)], n, rate[(w, a)][1:]) for w in READERS}
        table.append([a, X45Q_WHAT[a], str(layers.get(a, "–")), texts["PP"], texts["PM"], "; ".join(src["PP"]),
                      yes(all(ok.values()))])  # fmt: skip
        ref = X45Q_REF if a in X45Q_RULE_ARMS else X45Q_LINK_REF
        checks += [{**check45(f"{a}: {NAME[w]} switched", texts[w], "; ".join(src[w]), ok[w],
                              head=a == "a" and w == "PP"), "src": ref} for w in READERS]  # fmt: skip
    for a in ("c", "d"):
        ok = {w: k[(w, f"{a}&S")] == file[w]["hits_of_S"][a] and k[(w, "S")] == file[w]["S_switched"]
              and close_all(of_s[(w, a)], file[w]["of_S"][a]) for w in READERS}  # fmt: skip
        texts = {w: kn_ci(k[(w, f"{a}&S")], k[(w, "S")], of_s[(w, a)][1:]) for w in READERS}
        src = {w: f"x45q.json {kn_ci(file[w]['hits_of_S'][a], file[w]['S_switched'], file[w]['of_S'][a][1:])}"
               for w in READERS}  # fmt: skip
        table.append([f"{a} among S's switches", "items both S and the arm switch / items S switches",
                      str(layers[a]), texts["PP"], texts["PM"], src["PP"], yes(all(ok.values()))])  # fmt: skip
        checks += [{**check45(f"{a} among S's switches: {NAME[w]}", texts[w], src[w], ok[w],
                              head=a == "c" and w == "PP"), "src": X45Q_REF} for w in READERS]  # fmt: skip
    pos_check, pos_note = positions_check(pool, "the marked bridge token is the only token where O and S differ, for "
                                                "both readers; the marked locker tokens are those of every 'The locker "
                                                "of … is ….' sentence in the decoded prompt, equal to the stored "
                                                "lockers, patched and source positions and character marks")  # fmt: skip
    checks.append(pos_check)
    rows = [(it, w, it["rows"][w][a]) for it in pool for w in READERS for a in X45Q_ARMS]
    text = sum(C.piece(model, r["top"]) == r["top_text"] for _, _, r in rows)
    role = sum(role_of(r["top"], it["case"]["readers"][w]) == r["role"] for it, w, r in rows)
    swr = sum(int(r["switched"]) == int(r["role"] == "b") for _, _, r in rows)
    notes = ["Lookup decides, recall descriptive. Switch = the top token is S's answer's token. Rule (45b's, fixed in "
             "advance): (c) or (d) switches at least half of the lookups S switches while (a) stays at or below 0.25, "
             "on at least 2 of 3 models. The link arms (c_nojpp, c_norand) are reported beside it (link.json), not in "
             "it. CI: cluster bootstrap over the bridge item, 10,000 resamples, seed 0 (X.resampled_rates; c / d among "
             "S's switches = the ratio of the resampled shares, as the run's verdict).",
             f"Cross-checks over all {len(rows)} rows (both readers, {len(X45Q_ARMS)} arms): the decoded top token "
             f"equals the stored top_text on {text}; the role re-derived from the top token equals the stored role on "
             f"{role}; switched equals (role = b) on {swr}.", rows_note(pool, X45Q_ARMS), pos_note]  # fmt: skip
    short = SHORT[model]
    return Addition(f"45q · {short}", f"45q on the {short}: the bridge word vs the locker sentences, clean scenes "
                    "(Q45.12)", "On 45m's scenes whose bridge's locker sentence comes after the asked pick: the "
                    "bridge-word change at L, L/2, L/4 (a, b_half, b_quarter) against S's states copied into every "
                    "locker-sentence token at L or L/2 (c, d), and the copy without its J++ part or without a random part "
                    "of the same share (c_nojpp, c_norand, at L); S read on S.", model, run,
                    f"{X45Q_REF} and {X45Q_LINK_REF}", f"all {n} items of the run (cases.jsonl)", table, notes, checks,
                    pool, card_45q)  # fmt: skip


def card_45q(it: dict) -> list[str]:
    c, m = it["case"], it["model"]
    f, pos = c["features"], c["pos"]
    marks = [(pos, pos + 1, "bridge"), *((i, j, "locker") for sent in c["lockers"]["org"] for i, j in runs_of(sent))]
    rows = [["reader", "arm", "what", "layer (stored)", "top token (decoded)", "stored top_text", "stored role",
             "switched"]]  # fmt: skip
    for w in READERS:
        for a in X45Q_ARMS:
            r = it["rows"][w][a]
            rows.append([NAME[w], a, X45Q_WHAT[a], "not stored", "not stored", "–", "–", "–"] if r is None else
                        [NAME[w], a, X45Q_WHAT[a], "–" if r["layer"] is None else str(r["layer"]), answer_cell(m, r),
                         f"`{r['top_text']!r}`", r["role"], str(r["switched"])])  # fmt: skip
    found = "; ".join(
        f"{s} → tokens {p[0]}–{p[-1]}" for s, p in zip(c["lockers"]["sentences"], it["found"], strict=False)
    )
    return [f"The bridge's locker sentence comes {f['org locker vs asked pick']} the asked pick, the new item's "
            f"{f['alt locker vs asked pick']}. Added locker sentence, in O and S: “{c['fresh']['sentence']}”.", "",
            f"O, lookup ({LABEL[m]}; the model reads this; ⟦bridge:…⟧ = token {pos}, where a, b_half and b_quarter add "
            f"the change; ⟦locker:…⟧ = the {len(c['lockers']['org'])} locker sentences, {len(c['patched'])} tokens, "
            "where c, d, c_nojpp and c_norand copy S's states in):", "", *marked_prompt(c["readers"]["PP"]["ids"]["org"], m, marks),
            *shared_tail(c, m), s_line(c, m), "",
            positions_line(it, f"bridge: stored pos {pos}, the only token where O and S differ; locker sentences found "
                               f"in the decoded prompt: {found}; stored: the same sentences at tokens "
                               f"{', '.join(f'{p[0]}–{p[-1]}' for p in c['lockers']['org'])}."), "",
            f"Expected: {expected(c, m)}", "", *md_table(rows)]  # fmt: skip


# 45p: with the new item's locker first, the base edit at the bridge plus an edit at the new item's earlier mention
def item_tokens(spans: list[tuple[int, int]], m: re.Match) -> list[int]:
    return over(spans, *m.span(1))


def items_found(case: dict, model: str) -> tuple[dict[str, list[int]], list[str]]:
    """The new item's and the control item's tokens re-derived from the lookup's decoded O (the item's name inside its
    'The locker of [the] <item> is <n>.' sentence; control: the first such sentence whose item is neither the bridge
    nor the new item), and what disagrees with the stored positions, items and character marks."""
    text, spans, bad = found_text(case, model)
    lockers = list(LOCKER_TEXT.finditer(text))
    mine = [x for x in lockers if x.group(1) == case["cf_bridge"]]
    ctl = next((x for x in lockers if x.group(1) not in (case["entity"], case["cf_bridge"])), None)
    found = {"new": item_tokens(spans, mine[0]) if len(mine) == 1 else [],
             "control": item_tokens(spans, ctl) if ctl else []}  # fmt: skip
    if len(mine) != 1:
        bad.append(f"the new item has {len(mine)} locker sentences in the decoded prompt")
    if ctl is None or ctl.group(1) != case["control"]["item"]:
        bad.append(f"control item {None if ctl is None else ctl.group(1)!r} ≠ stored {case['control']['item']!r}")
    for part in ("new", "control"):
        p = found[part]
        if p != case[part]["positions"]:
            bad.append(f"{part} tokens {p} ≠ stored {case[part]['positions']}")
        if "".join(C.piece(model, case["readers"]["PP"]["ids"]["org"][i]) for i in p).strip() != case[part]["item"]:
            bad.append(f"the {part} tokens do not decode to exactly {case[part]['item']!r}")
        if char_marks(spans, p) != case["marks"][part]:
            bad.append(f"the stored {part} mark is not the {part} tokens' characters")
    if [list(spans[case["pos"]])] != case["marks"]["bridge"]:
        bad.append("the stored bridge mark is not the bridge token's characters")
    if not found["new"] or max(found["new"]) >= case["pos"]:
        bad.append("the new item's tokens are not before the bridge word")
    if len({case["pos"], *found["new"], *found["control"]}) != 1 + len(found["new"]) + len(found["control"]):
        bad.append("the marked positions overlap")
    last = max([case["pos"], *found["new"], *found["control"]])
    return found, bad + bridge_bad(case, model, case["entity"], case["cf_bridge"], last)


def marks_45p(case: dict) -> list[tuple[int, int, str]]:
    return [(case["pos"], case["pos"] + 1, "bridge"), *((i, j, "new") for i, j in runs_of(case["new"]["positions"])),
            *((i, j, "control") for i, j in runs_of(case["control"]["positions"]))]  # fmt: skip


def verify_pack_prompts(run: str) -> dict[tuple[str, str], str]:
    """The run's marked O prompts in the 45p verify pack (X45P_EXAMPLES, written by scripts/x45p.py from the stored
    character marks): (scene, reader) -> the text between its fences."""
    lines = (I.REPO / X45P_EXAMPLES).read_text().split("\n")
    out: dict[tuple[str, str], str] = {}
    section = scene = reader = ""
    i = 0
    while i < len(lines):
        x = lines[i]
        if x.startswith("## "):
            section = x[3:].split(":")[0]
        elif x.startswith("### "):
            scene = x[4:].split(" ")[0]
        elif x.startswith(("**lookup**", "**recall**")):
            reader = "PP" if x.startswith("**lookup**") else "PM"
        elif x == "```" and section == Path(run).name:
            j = lines.index("```", i + 1)
            out[(scene, reader)] = "\n".join(lines[i + 1 : j])
            i = j
        i += 1
    return out


def x45p_pool(model: str) -> list[dict]:
    """Every item of the run (cases.jsonl: 45m's scenes whose new item's locker sentence comes before the asked pick),
    with both readers' rows per arm."""
    run = X45P_RUNS[model]
    rows: dict[tuple[str, str, str], dict] = {}
    for r in I.read_jsonl(f"{run}/outcomes.jsonl"):
        key = (r["scene"], r["reader"], r["arm"])
        assert key not in rows, key
        rows[key] = r
    out = []
    for c in sorted(I.read_jsonl(f"{run}/cases.jsonl"), key=lambda c: c["scene"]):
        found, bad = items_found(c, model)
        out.append({"scene": c["scene"], "id": c["scene"], "model": model, "run": run, "case": c,
                    "bridge": c["entity"], "new": c["cf_bridge"], "found": found, "bad": bad,
                    "rows": {w: {a: rows.get((c["scene"], w, a)) for a in X45P_ARMS} for w in READERS}})  # fmt: skip
    return out


def x45p_number(model: str, pool: list[dict]) -> Addition:
    run = X45P_RUNS[model]
    ref = next(m for m in I.read_json(X45P_REF)["models"] if m["run"] == Path(run).name)
    assert not stored_rows(pool, X45P_ARMS)[1], "45p: a stored row is missing; the recount needs every arm"
    n = len(pool)
    ents = [it["rows"]["PM"]["none"]["entity"] for it in pool]
    sw = {(w, a): [int(it["rows"][w][a]["switched"]) for it in pool] for w in READERS for a in X45P_ARMS}
    k = {key: sum(v) for key, v in sw.items()}
    boot = X.resampled_rates({f"{w}|{a}": v for (w, a), v in sw.items()}, ents)
    loss, diff = {}, {}
    for w in READERS:
        dep = {a: X.dependence(boot[f"{w}|a1"], boot[f"{w}|{a}"]) for a in ("a2", "a3", "a4")}
        point = {a: 1 - k[(w, a)] / k[(w, "a1")] if k[(w, "a1")] else math.nan for a in dep}
        loss[w] = {a: [point[a], *X.interval(dep[a])] for a in dep}
        diff[w] = {f"2-{j}": [point["a2"] - point[f"a{j}"], *X.interval(dep["a2"] - dep[f"a{j}"])] for j in (3, 4)}
    file = {w: ref["readers"][NAME[w]] for w in READERS}
    table = [["arm", "what", "recall: switched (k of n)", "lookup: switched", "x45p.json (recall / lookup)", "matches"]]
    checks = [check45("n (items)", str(n), str(file["PM"]["n"]), n == file["PM"]["n"] == file["PP"]["n"])]
    for a in X45P_ARMS:
        ok = all(k[(w, a)] == file[w]["hits"][a] for w in READERS)
        table.append([a, X45P_WHAT[a], kn(k[("PM", a)], n), kn(k[("PP", a)], n),
                      f"{file['PM']['hits'][a]} / {file['PP']['hits'][a]}", yes(ok)])  # fmt: skip
        checks.append(check45(f"{a}: switched (recall / lookup)", f"{k[('PM', a)]} / {k[('PP', a)]}",
                              f"{file['PM']['hits'][a]} / {file['PP']['hits'][a]}", ok, head=a == "a1"))  # fmt: skip
    for a in ("a2", "a3", "a4"):
        ok = all(close_all(loss[w][a], file[w]["loss"][a]) for w in READERS)
        text = f"{ci_or_none(loss['PM'][a])}; {ci_or_none(loss['PP'][a])}"
        src = f"{ci_or_none(file['PM']['loss'][a])}; {ci_or_none(file['PP']['loss'][a])}"
        table.append([f"loss_{a[1]} = 1 − S_{a[1]} / S_1", "", ci_or_none(loss["PM"][a]), ci_or_none(loss["PP"][a]), src,
                      yes(ok)])  # fmt: skip
        checks.append(check45(f"loss_{a[1]} (recall; lookup)", text, src, ok))
    for d, bar in (("2-3", 0.2), ("2-4", 0.15)):
        ok = all(close_all(diff[w][d], file[w]["diff"][d]) for w in READERS)
        what = f"loss_2 − loss_{d[-1]}"
        table.append([what, f"the rule's bar: at least {bar} (recall)", ci_or_none(diff["PM"][d]),
                      ci_or_none(diff["PP"][d]), f"{ci_or_none(file['PM']['diff'][d])}; {ci_or_none(file['PP']['diff'][d])}",
                      yes(ok)])  # fmt: skip
        checks.append(check45(f"recall: {what}", ci_or_none(diff["PM"][d]), ci_or_none(file["PM"]["diff"][d]),
                              ok and close_all(diff["PP"][d], file["PP"]["diff"][d]), head=True))  # fmt: skip
    both = {a: sum(all(it["rows"][w][a]["right"] for w in READERS) for it in pool) for a in ("none", "o2")}
    ok = all(both[a] == ref["o_alone"][a]["both_right"] for a in both)
    table.append(["o2 / none: both readers read O right", "top token = O's answer, both readers",
                  f"o2 {both['o2']} of {n}; none {both['none']} of {n}", "",
                  f"{ref['o_alone']['o2']['both_right']} / {ref['o_alone']['none']['both_right']}", yes(ok)])  # fmt: skip
    checks.append(check45("both readers right: o2 / none", f"{both['o2']} / {both['none']}",
                          f"{ref['o_alone']['o2']['both_right']} / {ref['o_alone']['none']['both_right']}", ok))  # fmt: skip
    pos_check, pos_note = positions_check(pool, "the marked bridge token is the only token where O and S differ, for "
                                                "both readers; the marked new and control tokens are exactly the item's "
                                                "name inside its locker sentence in the decoded prompt (control: the "
                                                "first locker sentence whose item is neither the bridge nor the new "
                                                "item), equal to the stored positions and character marks; the new "
                                                "item's tokens come before the bridge word")  # fmt: skip
    checks.append(pos_check)
    by_scene = {it["scene"]: it for it in pool}
    shown = verify_pack_prompts(run)
    same = sum(s in by_scene and txt == marked_prompt(by_scene[s]["case"]["readers"][w]["ids"]["org"], model,
                                                     marks_45p(by_scene[s]["case"]))[1].replace(SPACE, " ")
               for (s, w), txt in shown.items())  # fmt: skip
    vp_scenes = {s for s, _ in shown}
    drawn = vp_scenes == {it["scene"] for it in draw(pool)}
    checks.append(check45("marked prompts (both readers) = the run's verify pack", f"{same} of {len(shown)} prompts",
                          f"{X45P_EXAMPLES} ({len(vp_scenes)} items)", bool(shown) and same == len(shown)))  # fmt: skip
    rows = [(it, w, it["rows"][w][a]) for it in pool for w in READERS for a in X45P_ARMS]
    text = sum(C.piece(model, r["top"]) == r["top_text"] for _, _, r in rows)
    role = sum(role_of(r["top"], it["case"]["readers"][w]) == r["role"] for it, w, r in rows)
    swr = sum(int(r["switched"]) == int(r["role"] == "b") for _, _, r in rows)
    right = sum(int(r["right"]) == int(r["top"] == it["case"]["readers"][w]["tok_A"]) for it, w, r in rows)
    notes = ["The recall decides, the lookup beside it. loss_k = 1 − S_k / S_1 (S_k the switch rate under arm k, S_1 "
             "the base edit's); rule (fixed in advance): loss_2 − loss_3 at least 0.2 and loss_2 − loss_4 at least "
             "0.15 on the recall, a model with fewer than 30 base-edit recall switches not tested; at least 2 of 3 "
             "models. CI: cluster bootstrap over the bridge item, 10,000 resamples, seed 0 (X.resampled_rates, paired "
             "across arms, as the run's verdict).",
             f"Cross-checks over all {len(rows)} rows (both readers, {len(X45P_ARMS)} arms): the decoded top token "
             f"equals the stored top_text on {text}; the role re-derived from the top token equals the stored role on "
             f"{role}; switched equals (role = b) on {swr}; right equals (top = O's answer's token) on {right}.",
             rows_note(pool, X45P_ARMS), pos_note,
             f"The marked prompts here (from the stored token positions) equal the run's verify pack ({X45P_EXAMPLES}, "
             f"marked from the stored character spans) on {same} of {len(shown)} prompts: its {len(vp_scenes)} items, "
             "both readers" + ("; they are the 10 items drawn here." if drawn else ".")]  # fmt: skip
    short = SHORT[model]
    return Addition(f"45p · {short}", f"45p on the {short}: the new item's earlier mention, its locker first (Q45.13)",
                    "On 45m's scenes whose new item's locker sentence comes before the asked pick: (1) the base edit "
                    "(the bridge-word change without its J++ part), then on top of it the new item's token(s) in its "
                    "locker sentence without their own J++ part (2), without a random part of the same share (3), or "
                    "the control item's token(s) without their J++ part (4); all at the layer fixed in advance, on O.",
                    model, run, X45P_REF, f"all {n} items of the run (cases.jsonl)", table, notes, checks, pool,
                    card_45p)  # fmt: skip


def card_45p(it: dict) -> list[str]:
    c, m = it["case"], it["model"]
    pos, ctl = c["pos"], c["control"]
    marks = marks_45p(c)
    rows = [["reader", "arm", "what", "top token (decoded)", "stored top_text", "switched", "right (O's answer)"]]
    for w in READERS:
        for a in X45P_ARMS:
            r = it["rows"][w][a]
            rows.append([NAME[w], a, X45P_WHAT[a], "not stored", "–", "–", "–"] if r is None else
                        [NAME[w], a, X45P_WHAT[a], answer_cell(m, r), f"`{r['top_text']!r}`", str(r["switched"]),
                         str(r["right"])])  # fmt: skip
    fd = it["found"]
    return [f"New item {c['new']['item']}: its locker sentence “{c['new']['sentence']}” comes before the asked pick. "
            f"Control item {ctl['item']} (“{ctl['sentence']}”, {ctl['vs_new']} the new item's, {ctl['vs_asked_pick']} "
            "the asked pick).", "",
            f"O, lookup ({LABEL[m]}; the model reads this; ⟦bridge:…⟧ = token {pos}, where the base edit (a1–a4) and "
            "the whole change go; ⟦new:…⟧ = the new item's token(s), edited in a2, a3 and o2; ⟦control:…⟧ = the "
            "control item's token(s), edited in a4):", "", *marked_prompt(c["readers"]["PP"]["ids"]["org"], m, marks),
            *shared_tail(c, m), s_line(c, m), "",
            positions_line(it, f"bridge: stored pos {pos}, the only token where O and S differ; new item found at "
                               f"tokens {fd['new']} (stored {c['new']['positions']}); control at {fd['control']} "
                               f"(stored {ctl['positions']})."), "",
            f"Expected: {expected(c, m)}", "", *md_table(rows)]  # fmt: skip


def additions_qpm() -> list[Addition]:
    """45m, 45q and 45p, each on the 9B, the 27B and Muse."""
    return [
        *(x45m_number(m, x45m_pool(m)) for m in QPM_MODELS),
        *(x45q_number(m, x45q_pool(m)) for m in QPM_MODELS),
        *(x45p_number(m, x45p_pool(m)) for m in QPM_MODELS),
    ]


def additions() -> list[Addition]:
    return [x45a_number(x45a_pool()), *(x45b_number(m, x45b_pool(m)) for m in X45B_RUNS), x45d_number(x45d_pool())]


def render_45(adds: list[Addition]) -> list[str]:
    lines = ["## Batch 45 additions (UNVERIFIED)", "",
             "Batch-45 numbers for Dan's Tuesday check (added 26 Oct ~21:45). UNVERIFIED. They are not in "
             "data/figures/depth/data.csv: each recount is compared with its run's verdict or table file named below (counts "
             "exactly, shares and extra losses to 1e-9), written as k of n and the share next to the file's number. 45a's "
             "table is descriptive, after the data; 45b's and 45d's numbers are their runs' verdicts. None of these runs is "
             "in docs/review/review_views.yaml, so each part loads its run's per-item files (cases.jsonl, outcomes.jsonl) "
             f"itself. Then {N_SHOW_45} items per part drawn with `random.Random({SEED}).sample(items, {N_SHOW_45})` over "
             "the recount's items sorted by scene, decoded as above (⟦ ⟧ the token where the change is added, ␣ the space "
             "token the read appends) with each run's own model's tokenizer at its pinned revision.", ""]  # fmt: skip
    return lines + parts_lines(adds, N_SHOW_45)


def parts_lines(adds: list[Addition], n_show: int) -> list[str]:
    """The parts' summary of headline checks, then per part its recount, checks and drawn items' cards."""
    lines: list[str] = []
    summary = [["part", "number", "file", "file's number", "recount", "matches"]]
    for a in adds:
        for c in a.checks:
            if c["head"]:
                summary.append([a.tag, c["what"], f"`{c.get('src', a.ref)}`", c["file"], c["recount"], yes(c["match"])])
    lines += [*md_table(summary), ""]
    bad = [(a.tag, c) for a in adds for c in a.checks if not c["match"]]
    lines += ["Every other number checked below matches its file too." if not bad else
              "Mismatches: " + "; ".join(f"{t}: {c['what']} file {c['file']}, recount {c['recount']}" for t, c in bad), ""]  # fmt: skip
    for a in adds:
        lines += [f"### {a.tag}. {a.title}", "", f"**What.** {a.what}", "",
                  f"**Model:** {LABEL[a.model]} · **run:** `{a.source}` · **compared with:** `{a.ref}` · **items:** "
                  f"{a.items}", "", "#### Recount", "", *md_table(a.table), "", *(f"- {x}" for x in a.notes), "",
                  f"**Matches the file: {yes(all(c['match'] for c in a.checks))}**", "",
                  *md_table([["number", "recount", "file", "matches"]]
                            + [[c["what"], c["recount"], c["file"], yes(c["match"])] for c in a.checks]), "",
                  f"#### {len(a.sample)} random items", "",
                  f"`random.Random({SEED}).sample(items, {n_show})` over the {len(a.pool)} items sorted by "
                  + ("base scene." if a.tag == "A" else "scene."), ""]  # fmt: skip
        for i, it in enumerate(a.sample, 1):
            c = it.get("case") or it["cases"]["V0"]
            bridge = c.get("bridge", c.get("entity"))  # 45b's cases name the original bridge "entity"
            head = f"##### {a.tag} {i} · {'base ' if a.tag == 'A' else ''}scene {it['scene']} · bridge {bridge}"
            lines += [head + f" (changed: {c['cf_bridge']})", "", *a.card(it), ""]
    return lines


def render_qpm(adds: list[Addition]) -> list[str]:
    lines = ["## 45m, 45q and 45p (UNVERIFIED)", "",
             "Added for Dan's hand-check (27 Oct ~14:40). UNVERIFIED. Each test's rule counts the 9B, the 27B and Muse, "
             f"so each model is its own part: 3 tests × 3 models, {N_SHOW} items each, drawn with "
             f"`random.Random({SEED}).sample(items, {N_SHOW})` over the run's items sorted by scene (the six numbers' "
             "draw). Each part loads its run's per-item files (cases.jsonl, outcomes.jsonl) itself; its recount is "
             "compared with the verdict file that predictions/2026-10-26_dan.md cites (Q45.10, Q45.12, Q45.13): counts "
             "exactly, shares, extra losses and their CIs to 1e-9. Prompts are decoded from the stored token ids with "
             "each run's own model's tokenizer at its pinned revision, exactly as the model reads them (chat template "
             "included; ␣ the space token the read appends, after which the answer token is read). In all three tests O "
             "and S differ only at the bridge token, so S is given as that one token's change. Marks, as the 45p verify "
             f"pack ({X45P_EXAMPLES}): ⟦bridge:…⟧ the bridge word; ⟦locker:…⟧ each locker sentence's tokens (45q); "
             "⟦new:…⟧ the new item's token(s) in its locker sentence and ⟦control:…⟧ the control item's (45p); a marked "
             "token's leading space stays outside its mark, and a mark closes after its last whole token (where a "
             "sentence's final '.' shares a token with the newline, as Muse's '.\\n', the ⟧ starts the next line). The "
             "marks are the run's stored positions (cases.jsonl); "
             "each is re-derived from the decoded tokens (the tokens where O and S differ; the 'The locker of … is ….' "
             "sentences and the items' names found in the decoded text) and compared, for every item of every run: the "
             "result is on each card and counted in each part's checks. Each arm's answer is the run's stored top token "
             "(outcomes.jsonl), decoded; nothing is recomputed, and an answer the files do not hold would show as "
             "'not stored'.", ""]  # fmt: skip
    return lines + parts_lines(adds, N_SHOW)


# ------------------------------------------------------------------------------------------------------- the pack
def numbers() -> list[Number]:
    pool = x0_pool()
    before = [it for it in pool if order_of(it) == "before"]
    rt = routes_pool()
    return [
        number_gap(1, pool, "The main-test gap (recall extra loss minus lookup extra loss)",
                   "On the 9B's main test (two people swap picks), removing the J++ part costs the recall more switches "
                   "than the lookup, against a random part of the same share: gap 0.53 [0.42, 0.61].",
                   "contrast_9b", "", []),
        number_order(pool),
        number_routes(rt),
        number_pointer(rt),
        number_write(x8_pool("write", 2)),
        number_gap(6, before, "The locker-first gap (T0.2)",
                   "On the 9B's main test, restricted to the scenes whose original bridge's locker sentence comes before "
                   "the asked pick (locker-first), the gap is 0.34 [0.23, 0.43].",
                   "sbo_swap_before_gap_9b", "sbo_swap_before",
                   ["Items: the main test's scenes whose x0_strata 'org locker vs asked pick' is before (the split of "
                    "scripts/x0_split_by_order.py); the same arms and formula as number 1."]),
    ]  # fmt: skip


def draw(pool: list[dict], n: int = N_SHOW) -> list[dict]:
    return random.Random(SEED).sample(pool, min(n, len(pool)))


def commit() -> str:
    def git(*a: str) -> str:
        return subprocess.run(["git", *a], cwd=I.REPO, capture_output=True, text=True).stdout.strip()

    dirty = git("status", "--porcelain", "--", "scripts/handcheck_pack.py", "src/bridge_jspace/review",
                "docs/review/review_views.yaml", X0_RUN, RT_RUN, X8_RUN, "data/figures/depth/data.csv", X45A_RUN,
                str(Path(X45A_TABLE).parent), *X45B_RUNS.values(), X45D_RUN, *X45M_RUNS.values(),
                *X45Q_RUNS.values(), *X45P_RUNS.values(), *(str(Path(p).parent) for p in (X45M_REF, X45Q_REF,
                                                                                          X45Q_LINK_REF, X45P_REF)))  # fmt: skip
    return git("rev-parse", "--short", "HEAD") + (" (with uncommitted changes)" if dirty else "")


def render(nums: list[Number], sha: str, adds: list[Addition] | tuple = (), more: list[Addition] | tuple = ()) -> str:
    t = pins.TARGETS[MODEL]
    lines = ["# Hand-check pack: six Qwen3.5-9B headline numbers", "",
             f"Generated by `uv run python scripts/handcheck_pack.py` at commit {sha}; do not hand-edit (rerun the script). "
             f"Qwen3.5-9B, layer {LAYER}. Inputs: the runs' per-item files only (cases.jsonl, outcomes.jsonl), read with "
             "the review dashboard's loaders (src/bridge_jspace/review/, docs/review/review_views.yaml); no verdict or aggregate "
             "file is read. Each recount is compared with the `numbers` rows of data/figures/depth/data.csv at 2 decimals "
             f"(the value and its CI). Tokens are decoded with tokenizer.json of {t['repo']} at revision {t['revision']} "
             "(src/bridge_jspace/pins.py). Status: UNVERIFIED until a human adds it to VERIFIED.md.", "",
             "**How to recount by hand.** Each section gives the recount first: every k is the number of items whose "
             "stored outcome (outcomes.jsonl) is switched, or has the route or class named, out of the n items in its "
             "'every item' list, and the headline is computed from those counts with the formula written out; tally a "
             "column of that list to recount a k. Then come 10 items drawn with `random.Random(0).sample(items, 10)` over "
             "the recount's items sorted by scene. For each, read the original prompt (decoded from the stored token ids "
             "exactly as the model read it; ⟦ ⟧ marks the token where the change is added; ␣ is the space token the read "
             "step appends, after which the answer token is read), work out the expected answers from the text yourself "
             "(lookup: the locker digit of the asked person's pick; recall: the asked pick's fact from memory; routes and "
             "writes: the digit each route or slot predicts), then check each arm's decoded answer token against them "
             "and against the stored label. A stored label that disagrees with the decoded token or with your reading is "
             "a finding: note the scene.", "",
             "## Summary", ""]  # fmt: skip
    summary = [["#", "number", "key", "data.csv", "recount", "matches data.csv"]]
    for n in nums:
        for h in n.headline():
            summary.append([str(n.no), n.title, f"`{h['key']}`", h["data"], h["recount"], yes(h["match"])])
    lines += [*md_table(summary), ""]
    bad = [(n.no, c) for n in nums for c in n.checks if not c["match"]]
    lines += ["Every other key checked below (counts, each reader's extra loss, the other routes, the controls) matches too." if not bad else
              "Mismatches: " + "; ".join(f"{no}: `{c['key']}` data.csv {c['data']}, recount {c['recount']}" for no, c in bad), ""]  # fmt: skip
    seen: dict[tuple, int] = {}
    for n in nums:
        lines += [f"## {n.no}. {n.title}", "", f"**Claim.** {n.claim}", "",
                  f"**Key:** {' / '.join(f'`{k}`' for k in n.keys)} · **source run:** `{n.source}` · **n:** "
                  f"{len(n.pool)} items", "",
                  "### Recount", "", *md_table(n.table), ""]  # fmt: skip
        lines += [*(f"- {x}" for x in n.notes), ""]
        rows = [["key", "data.csv", "recount", "matches"]] + [
            [f"`{c['key']}`", c["data"], c["recount"], yes(c["match"])] for c in n.checks
        ]
        lines += [f"**Matches data.csv: {yes(all(c['match'] for c in n.checks))}**", "", *md_table(rows), ""]
        lines += [f"<details><summary>Every item (n = {len(n.pool)})</summary>", "", *md_table(n.every), "",
                  "</details>", ""]  # fmt: skip
        # one seed over the same scene list draws the same scenes (also over two rows per scene: random.sample's draws
        # for 2n are the draws for n with one more bit), so later numbers can repeat an earlier number's scenes
        scenes = tuple(it["scene"] for it in n.sample)
        same = (
            f" The same scenes as number {seen[scenes]} (the same seed over the same scenes)." if scenes in seen else ""
        )
        seen.setdefault(scenes, n.no)
        lines += [f"### {len(n.sample)} random items", "",
                  f"`random.Random({SEED}).sample(items, {N_SHOW})` over the {len(n.pool)} items sorted by scene"
                  + (" and target slot" if n.no == 5 else "") + f".{same}", ""]  # fmt: skip
        for i, it in enumerate(n.sample, 1):
            c = it["case"]
            head = f"#### {n.no}.{i} · scene {it['scene']} · bridge {c['bridge']}"
            head += f" (changed: {c['cf_bridge']})" if n.no != 5 else f" · write slot {it['x8']['j']} → {it['x8']['k']}"
            lines += [head, "", *n.card(it), ""]
    lines += render_45(list(adds)) if adds else []
    lines += render_qpm(list(more)) if more else []
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    nums = numbers()
    for n in nums:
        n.sample = draw(n.pool)
    adds = additions()
    for a in adds:
        a.sample = draw(a.pool, N_SHOW_45)
    more = additions_qpm()
    for a in more:
        a.sample = draw(a.pool)
    OUT.write_text(render(nums, commit(), adds, more))
    for n in nums:
        for h in n.headline():
            print(f"{n.no}. {h['key']}: recount {h['recount']} | data.csv {h['data']} | match {h['match']}")
        print(f"   all {len(n.checks)} keys of number {n.no} match: {all(c['match'] for c in n.checks)}")
    for a in (*adds, *more):
        for c in a.checks:
            if c["head"]:
                print(f"{a.tag}. {c['what']}: recount {c['recount']} | file {c['file']} | match {c['match']}")
        print(f"   all {len(a.checks)} numbers of {a.tag} match {a.ref}: {all(c['match'] for c in a.checks)}")
    print("wrote", OUT.relative_to(I.REPO))


if __name__ == "__main__":
    main()
