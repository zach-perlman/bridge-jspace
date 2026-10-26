"""Hand-check pack (Dan, 26 Oct): six Qwen3.5-9B headline numbers at layer 12, each recounted item by item from its
run's per-item files (cases.jsonl, outcomes.jsonl; no verdict or aggregate file is read) and compared with
figures/story/data.csv at 2 decimals; then 10 items per number (random.Random(0).sample over the recount's items sorted
by scene) shown as the model saw them: each prompt decoded token by token from its stored ids with the pinned tokenizer,
the token where the change is added marked ⟦word⟧, and per arm the stored outcome with its answer token decoded.
Items, prompts and tokens come from the review dashboard's code (src/bridge_jspace/review/). CPU only.

uv run python scripts/handcheck_pack.py      # docs/handcheck_pack.md (generated; do not hand-edit)
"""

from __future__ import annotations

import random
import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.review import checks as C
from bridge_jspace.review import items as I
from bridge_jspace.review.recount import data_csv
from scripts import x0_necessity as X
from scripts import x0_strata as ST

MODEL, LAYER = "qwen3.5-9b", 12
OUT = I.REPO / "docs" / "handcheck_pack.md"
N_SHOW, SEED = 10, 0
READERS = ("PP", "PM")
NAME = {"PP": "lookup", "PM": "recall"}
X0_RUN = "results/x0_necessity/qwen35_9b_x0_necessity"
RT_RUN = "results/x6_routes/qwen35_9b_x6_routes"
X8_RUN = "results/x8_write/qwen35_9b_x8_write"
# stored arm -> the review view's label for it (docs/review_views.yaml)
X0_ARMS = {"whole": "whole", "no_part": "without J++", "no_rand": "without its random part"}
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
    rows = [["reader", "n", "S_whole", "S_no_part (without J++)", "S_no_rand (without its random part)",
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


def decoded(top: int) -> str:
    return C.piece(MODEL, top).strip()


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
def prompt(ids: list[int], pos: int | None) -> list[str]:
    """The prompt decoded token by token (exactly the full decode), ⟦ ⟧ around the token at pos, ␣ = the space token
    the read appends (chat read: one forward of the prompt plus a digit's space token; not stored in cases.jsonl)."""
    parts = [C.piece(MODEL, t) for t in ids]
    assert "".join(parts) == C.tokenizer(MODEL).decode(ids, skip_special_tokens=False), "per-token decode differs"
    if pos is not None:
        core = parts[pos].lstrip()
        parts[pos] = parts[pos][: len(parts[pos]) - len(core)] + f"⟦{core}⟧"
    return ["```text", "".join(parts) + SPACE, "```", ""]


def recall_tail(case: dict) -> list[str]:
    a, b = case["readers"]["PP"]["ids"]["org"], case["readers"]["PM"]["ids"]["org"]
    i = next(i for i, (x, y) in enumerate(zip(a, b, strict=False)) if x != y)
    assert i > case["pos"]
    return [f"Recall prompt: the same first {i} tokens (so the same ⟦{case['bridge']}⟧ at token {case['pos']}), then:",
            "", "```text", C.tokenizer(MODEL).decode(b[i:], skip_special_tokens=False) + SPACE, "```", ""]  # fmt: skip


def token_diffs(case: dict) -> str:
    o, a = case["readers"]["PP"]["ids"]["org"], case["readers"]["PP"]["ids"]["alt"]
    if len(o) != len(a):
        return f"the prompts have {len(o)} and {len(a)} tokens"
    return "; ".join(f"{i}: `{C.piece(MODEL, x)!r}` → `{C.piece(MODEL, y)!r}`" for i, (x, y) in enumerate(zip(o, a, strict=True)) if x != y)  # fmt: skip


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


def card_routes(it: dict, arms: list[str]) -> list[str]:
    c = it["case"]
    o = C.LOCKER.findall(c["context"])
    s = C.LOCKER.findall(c["cf_context"])
    b = c["cf_bridge"]
    slot = [x for x, _ in s].index(b)
    e = c["expect"]
    exp = (f"identity {e['identity']} ({b}'s locker in the original prompt); position {e['position']} (the original "
           f"prompt's locker sentence {slot + 1}, {o[slot][0]}'s: where {b}'s locker sentence sits in the changed prompt); "
           f"value {e['value']} ({b}'s new locker in the changed prompt, not in the original); original {e['original']} "
           f"({c['bridge']}'s locker, the original answer). Re-derived from the two prompts: "
           f"{'the same' if c2_expect(c) == e else 'DIFFERENT: ' + str(c2_expect(c))}.")  # fmt: skip
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


def draw(pool: list[dict]) -> list[dict]:
    return random.Random(SEED).sample(pool, min(N_SHOW, len(pool)))


def commit() -> str:
    def git(*a: str) -> str:
        return subprocess.run(["git", *a], cwd=I.REPO, capture_output=True, text=True).stdout.strip()

    dirty = git("status", "--porcelain", "--", "scripts/handcheck_pack.py", "src/bridge_jspace/review",
                "docs/review_views.yaml", X0_RUN, RT_RUN, X8_RUN, "figures/story/data.csv")  # fmt: skip
    return git("rev-parse", "--short", "HEAD") + (" (with uncommitted changes)" if dirty else "")


def render(nums: list[Number], sha: str) -> str:
    t = pins.TARGETS[MODEL]
    lines = ["# Hand-check pack: six Qwen3.5-9B headline numbers", "",
             f"Generated by `uv run python scripts/handcheck_pack.py` at commit {sha}; do not hand-edit (rerun the script). "
             f"Qwen3.5-9B, layer {LAYER}. Inputs: the runs' per-item files only (cases.jsonl, outcomes.jsonl), read with "
             "the review dashboard's loaders (src/bridge_jspace/review/, docs/review_views.yaml); no verdict or aggregate "
             "file is read. Each recount is compared with the `numbers` rows of figures/story/data.csv at 2 decimals "
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
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    nums = numbers()
    for n in nums:
        n.sample = draw(n.pool)
    OUT.write_text(render(nums, commit()))
    for n in nums:
        for h in n.headline():
            print(f"{n.no}. {h['key']}: recount {h['recount']} | data.csv {h['data']} | match {h['match']}")
        print(f"   all {len(n.checks)} keys of number {n.no} match: {all(c['match'] for c in n.checks)}")
    print("wrote", OUT.relative_to(I.REPO))


if __name__ == "__main__":
    main()
