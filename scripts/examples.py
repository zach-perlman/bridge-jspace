"""Real examples as images (README brief, 7 Nov, §2): one card per test, each an item picked by a stated rule (E2 and E4 by
their outcome, said on the card), with the prompt's real text, the bridge word in bold and each reader's answer before and under each
operation, read from the per-item run files. The rule and the item id are printed on the card; the README gives each
card's population rate beside it (by key, in the caption stores figures/{depth,breadth}/examples/_meta/captions.toml).
The cards go by track (figkit/layout.py): E1, E4 to figures/depth/examples/, E2, E3 to figures/breadth/examples/;
figures/common/examples/ (cards that span both tracks) is empty and gets its index only.

  E1 depth   the main test (two people swap picks), Qwen 27B: results/x0_necessity/x0_necessity_27b_chat/
  E2 breadth a fact passage with the final fact stated (lookup) and without it (recall), Qwen 27B, jsuite v2 test;
             picked by its outcome (Dan, 8 Nov: show a flip), said on the card, its rate in the caption:
             data/tasks_v2/jsuite_v2_test_chat/items.jsonl + results/ablate_v2/jsuite_v2_test_chat_ko_cand2_v1/rows.jsonl
  E3 chains  three three-hop chains about one entity (P → P → P, P → M → M, M → P → M), Qwen 27B: the same items file +
             results/ablate_v2/jsuite_v2_test_chat_threehop_ko_cand2_v1/rows.jsonl
  E4 routes  the routes test, another item moved (C2), Qwen 9B: results/x6_routes/qwen35_9b_x6_routes/; picked by its
             outcome (brief 6, 11 Nov: the columns must differ), said on the card, its rate in the caption

Nothing is rerun: an answer the files do not store as text (a knocked-out breadth answer) is its first token, decoded
with the model's tokenizer from the local cache.

uv run python scripts/examples.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, OrderedDict
from functools import cache
from pathlib import Path

import numpy as np
import styles_plot as sp

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO))  # scripts.x0_massmean (E5)
from bridge_jspace.figkit import layout as L  # noqa: E402
from bridge_jspace.figkit.writeup_sp_base import vocab  # noqa: E402

GROUPS, TARGET = ("depth/examples", "breadth/examples", "common/examples"), "readme"
DEPTH = REPO / "results/x0_necessity/x0_necessity_27b_chat"
ROUTES = REPO / "results/x6_routes/qwen35_9b_x6_routes"
ITEMS = REPO / "data/tasks_v2/jsuite_v2_test_chat/items.jsonl"
KO = REPO / "results/ablate_v2/jsuite_v2_test_chat_ko_cand2_v1/rows.jsonl"
THREE = REPO / "results/ablate_v2/jsuite_v2_test_chat_threehop_ko_cand2_v1/rows.jsonl"
MAIN = ("jpp", 25, "signed")  # the main test's lens part (scripts/x0_necessity.py MAIN)
READER = {"PP": ("lookup", "lookup"), "PM": ("recall", "recall")}
BREADTH_ARMS = (("none", "before"), ("paper10", "lens part removed"), ("paper10_rot", "rotated part removed"))  # fmt: skip


def jsonl(p: Path) -> list[dict]:
    return [json.loads(line) for line in p.open()]


def rel(p: Path) -> str:
    return str(p.relative_to(REPO))


@cache
def tokenizer(repo: str):
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(repo, local_files_only=True)


def bold(text: str, word: str, at: int | None = None) -> list[tuple]:
    """The text as prompt parts with one occurrence of `word` bold (the one starting at `at`, else the last)."""
    i = at if at is not None else text.rfind(word)
    return [(text[:i], None), (word, None, True), (text[i + len(word) :], None)]


# ---- E1: the depth main test -----------------------------------------------------------------------------------------
def e1_locker_scene() -> sp.Figure:
    rows = jsonl(DEPTH / "outcomes.jsonl")
    layer = _main_layer()
    first = next(r for r in rows if r["layer"] == layer)["scene"]
    case = next(c for c in jsonl(DEPTH / "cases.jsonl") if c["scene"] == first and c["rendering"] == "chat")
    asked = re.match(r"Which locker belongs to (\w+)'s pick", case["readers"]["PP"]["question"]).group(1)
    sentence = f"{asked} picked the {case['bridge']}"
    at = case["context"].index(sentence) + len(sentence) - len(case["bridge"])
    columns = ["before", "the whole change", "without the lens part", "without a random part"]
    arm_of = {("-", "none"): "before", ("-", "whole"): "the whole change", (MAIN, "no_part"): "without the lens part",
              (MAIN, "no_rand"): "without a random part"}  # fmt: skip
    answers: dict[str, dict[str, str]] = {r: {} for r in READER}
    for r in rows:
        if r["scene"] != first or r["layer"] != layer:
            continue
        key = ("-", r["arm"]) if r["dict"] == "-" else ((r["dict"], r["k"], r["omp"]), r["arm"])
        col = arm_of.get(key)
        if col is None:
            continue
        rd = case["readers"][r["reader"]]
        answers[r["reader"]][col] = {"A": f"{rd['answer']} (the {case['bridge']}'s)",
                                     "b": f"{rd['cf_answer']} (the {case['cf_bridge']}'s)"}.get(
            r["role"], f"neither {rd['answer']} nor {rd['cf_answer']}")  # fmt: skip
    prompt = [bold(case["context"], case["bridge"], at),
              [("Lookup:", "lookup", True), (f" {case['readers']['PP']['question']}", None)],
              [("Recall:", "recall", True), (f" {case['readers']['PM']['question']}", None)],
              [("The change:", None, True), (f" at layer {layer}, the bridge word's state comes from the same scene "
                                             f"with {asked} picking the {case['cf_bridge']}.", None)]]  # fmt: skip
    card = sp.Card(prompt=prompt, columns=columns,
                   rows=[sp.CardRow(*READER[r], answers[r]) for r in READER],
                   note=f"Qwen 27B · layer {layer}")
    write_keys({"e1.items": (first, "id", f"rule: the main test's first scene in {rel(DEPTH)}/outcomes.jsonl, "
                                         f"Qwen 27B, layer {layer}")})  # fmt: skip
    return sp.Figure("e1_locker_scene", vocab(), direct_labels=True).add(card)


def _main_layer() -> int:
    """The main test's layer for the 27B (its L in docs/depth/x0_numbers.json, read from the same outcomes file)."""
    x0 = json.loads((REPO / "docs/depth/x0_numbers.json").read_text())
    return int(x0["layer_27b"]["text"])


# ---- E2: a fact passage, stated vs recalled ----------------------------------------------------------------------------
def _breadth_answer(row: dict, expected: str, repo: str) -> str:
    if row["correct"]:
        return expected
    return f"{tokenizer(repo).decode([row['top_id']]).strip()}… (wrong)"


def e2_fact_passage() -> sp.Figure:
    items = jsonl(ITEMS)
    rows = jsonl(KO)
    have = {r["id"] for r in rows}
    scenes: dict[str, dict] = {}
    for i in items:
        scenes.setdefault(i["scene"], {})[i["word"]] = i
    correct = {(r["id"], r["condition"]): r["correct"] for r in rows}

    def flips(pm: dict) -> bool:
        """The pattern the card shows (Dan, 8 Nov: show a flip): both right before, the recall wrong with the lens part
        removed and right with a rotated part removed, the lookup right throughout."""
        pk = scenes[pm["scene"]]["PK"]
        return (all(correct.get((pk["id"], c)) for c, _ in BREADTH_ARMS)
                and correct.get((pm["id"], "none")) and not correct.get((pm["id"], "paper10"), True)
                and correct.get((pm["id"], "paper10_rot")))  # fmt: skip

    pairs = [i for i in items if i["word"] == "PM" and "PK" in scenes[i["scene"]] and i["id"] in have
             and scenes[i["scene"]]["PK"]["id"] in have]  # fmt: skip
    pm = next(i for i in pairs if flips(i))
    pk = scenes[pm["scene"]]["PK"]
    # how typical the card is: the pairs both right before, and those that show its pattern (the caption's N of M)
    both_right = [i for i in pairs if correct.get((i["id"], "none")) and correct.get((scenes[i["scene"]]["PK"]["id"], "none"))]
    write_keys({"e2.pairs_both_right": (len(both_right), "count", f"{rel(ITEMS)} + {rel(KO)}: final-from-memory items "
                                        "whose stated pair is in the run, both answers right before the removal"),
                "e2.pairs_flip": (sum(flips(i) for i in both_right), "count", f"{rel(ITEMS)} + {rel(KO)}: of those, the "
                                  "recall wrong with the lens part removed and right with a rotated part removed, the "
                                  "lookup right throughout")})  # fmt: skip
    # the two passages differ sentence by sentence (a passage may be one paragraph): the lookup's states the facts the
    # recall's replaces with filler about the same entities
    lookup_s, recall_s = _sentences(pk["context"]), _sentences(pm["context"])
    stated = [s for s in lookup_s if s not in recall_s]
    repo = json.loads((KO.parent / "manifest.json").read_text())["model"]["repo"]
    bridge = pm["bridge"]
    # the chain the card spells out (Dan, 8 Nov: "how the lookup works" must be visible): hop 1 names the bridge in
    # both passages; hop 2, the bridge's fact, is the stated sentence about the bridge, in the lookup's passage only
    hop1 = next(s for s in lookup_s if bridge in s and s in recall_s)
    hop2 = next(s for s in stated if bridge in s)
    def prompt(label: str, role: str, sentences: list[str]) -> list[tuple]:
        """One reader's real prompt, cut to the sentences that name the bridge (in order; … = the rest), then the
        question: the bridge bold where hop 1 names it, the stated fact (hop 2) in the lookup's colour."""
        out: list[tuple] = [(label, role, True), (" ", None)]
        named = [s for s in sentences if bridge in s]
        if sentences[0] not in named:
            out.append(("… ", None))
        for s in named:
            text = s.removeprefix("- ")
            if s == hop1:
                out += bold(text, bridge, text.index(bridge))
            elif s == hop2:
                out.append((text, "lookup"))
            else:
                out.append((text, None))
            out.append((" … ", None))
        return [*out, (pk["question"], None)]

    parts = [prompt("Lookup prompt:", "lookup", lookup_s), prompt("Recall prompt:", "recall", recall_s)]
    answers: dict[str, dict[str, str]] = {"lookup": {}, "recall": {}}
    for r in rows:
        for item, reader in ((pk, "lookup"), (pm, "recall")):
            for cond, col in BREADTH_ARMS:
                if r["id"] == item["id"] and r["condition"] == cond:
                    answers[reader][col] = _breadth_answer(r, item["answer"], repo)
    card = sp.Card(prompt=parts, columns=[c for _, c in BREADTH_ARMS],
                   rows=[sp.CardRow("lookup", "lookup", answers["lookup"]),
                         sp.CardRow("recall", "recall", answers["recall"])],
                   note="Qwen 27B · … = the rest of the letter")
    write_keys({"e2.items": (f"{pk['id']} {pm['id']}", "id",
                             f"rule (picked by its outcome, to show the typical flip): the first final-from-memory "
                             f"item in {rel(ITEMS)} whose recall turns wrong with the lens part removed and stays "
                             f"right with a rotated part removed, its stated pair's lookup right throughout; Qwen "
                             f"27B, removal at layers {_band(rows)}")})  # fmt: skip
    return sp.Figure("e2_fact_passage", vocab(), direct_labels=True).add(card)


DATA = REPO / "data/figures/examples/data.csv"


def write_keys(rows: dict[str, tuple]) -> None:
    """Merge keyed counts into data/figures/examples/data.csv (key, value, unit, source), the captions' source."""
    import csv

    have: dict[str, dict] = {}
    if DATA.exists():
        with DATA.open() as f:
            have = {r["key"]: r for r in csv.DictReader(f)}
    for k, (v, unit, src) in rows.items():
        have[k] = {"key": k, "value": v, "unit": unit, "source": src}
    DATA.parent.mkdir(parents=True, exist_ok=True)
    with DATA.open("w", newline="") as f:
        w = csv.DictWriter(f, ["key", "value", "unit", "source"], lineterminator="\n")
        w.writeheader()
        w.writerows(have[k] for k in sorted(have))


def _sentences(context: str) -> list[str]:
    """A passage's lines, each split into its sentences."""
    return [s for s in re.split(r"(?<=[.!?])\s+|\n+", context) if s.strip()]


def _band(rows: list[dict]) -> str:
    return next(r["band"] for r in rows if r["condition"] == "paper10")


# ---- E3: three chains about one entity --------------------------------------------------------------------------------
CHAINS = ("PPP", "PMM", "MPM")
LETTER = {"P": "read in the passage", "M": "recalled", "C": "computed"}


def e3_chains() -> sp.Figure:
    items = jsonl(ITEMS)
    rows = jsonl(THREE)
    # eligible: answered right before any removal (the run has no gate of its own; its unedited accuracy is 98-100%)
    right_before = {r["id"] for r in rows if r["condition"] == "none" and r["correct"]}
    groups: OrderedDict[str, dict] = OrderedDict()
    for i in items:
        if i["word"] in CHAINS:
            groups.setdefault(re.sub(r":(PPP|PMM|MPM)-", ":X-", i["scene"]), {})[i["word"]] = i
    chain = next(g for g in groups.values()
                      if len(g) == len(CHAINS) and all(g[w]["id"] in right_before for w in g))  # fmt: skip
    repo = json.loads((THREE.parent / "manifest.json").read_text())["model"]["repo"]
    fig = sp.Figure("e3_chains", vocab(), direct_labels=True)
    ids: list[str] = []
    for w in CHAINS:
        it = chain[w]
        reader = "recall" if w[-1] == "M" else "lookup"
        ans = {col: _breadth_answer(r, it["answer"], repo) for r in rows if r["id"] == it["id"]
               for cond, col in BREADTH_ARMS if r["condition"] == cond}  # fmt: skip
        # the chain itself, each hop's answer with where it comes from (Dan, 8 Nov: the passage alone is unreadable)
        chain_parts: list[tuple] = [(f"{' → '.join(w)}:", None, True), (" ", None)]
        for n, step in enumerate(it["steps"]):
            where = "in the passage" if step["source"] == "P" else "from memory"
            chain_parts += [(" → " if n else "", None), (step["answer"], None, step["answer"] == it["bridge"]),
                            (f" ({where})", None)]  # fmt: skip
        # the prompt cut to the sentences that state a hop read in the passage; … is the rest
        read = [s["answer"] for s in it["steps"] if s["source"] == "P"]
        sents = _sentences(" ".join(ln.removeprefix("- ") for ln in it["context"].split("\n")))
        kept = [s for s in sents if any(a in s for a in read)]
        text: list[tuple] = [("… ", None)] if kept and sents[0] != kept[0] else []
        for s in kept:
            text += [*(bold(s, it["bridge"], s.index(it["bridge"])) if it["bridge"] in s else [(s, None)]),
                     (" … ", None)]  # fmt: skip
        prompt = [chain_parts, [*text, (it["question"], None)]]
        fig.add(sp.Card(prompt=prompt, columns=[c for _, c in BREADTH_ARMS],
                        rows=[sp.CardRow(reader, reader, ans)], note="Qwen 27B · … = the rest of the post"))
        ids.append(it["id"])
    write_keys({"e3.items": (" ".join(ids), "id", f"rule: the first entity in {rel(ITEMS)} with all three chain "
                                                   f"types, each answered right before any removal, Qwen 27B")})  # fmt: skip
    return fig


# ---- E4: the routes test --------------------------------------------------------------------------------------------
ROUTE_ROLE = {"identity": "identity", "position": "address", "value": None}
ROUTE_ARMS = (("none", "before"), ("whole", "the whole change"), ("no_jpp", "without the lens part"),
              ("no_alf", "without the address"))  # fmt: skip


def _route_shown(routes: dict) -> bool:
    """The pattern the card shows (brief 6, 11 Nov: the columns must differ): the whole change sends the lookup to the
    position route, it stays there without the lens part, and without the address it leaves it (back to the original
    or to the identity route)."""
    return (routes.get("whole") == "position" and routes.get("no_jpp") == "position"
            and routes.get("no_alf") in ("original", "identity"))  # fmt: skip


def e4_routes() -> sp.Figure:
    rows = jsonl(ROUTES / "outcomes.jsonl")
    routes: OrderedDict[str, dict] = OrderedDict()
    for r in rows:
        if r["condition"] == "C2" and r["reader"] == "PP":
            routes.setdefault(r["scene"], {})[r["arm"]] = r["route"]
    first = next(sc for sc, rt in routes.items() if _route_shown(rt))
    case = next(c for c in jsonl(ROUTES / "cases.jsonl") if c["scene"] == first)
    rd = case["readers"]["PP"]

    def said(r: dict) -> str:
        if r["arm"] == "none" or r["route"] == "original":
            return f"{rd['answer']} (the original)"
        if r["route"] in ROUTE_ROLE:
            return f"{case['expect'][r['route']]} ({r['route']} route)"
        return "another locker"

    cols = dict(ROUTE_ARMS)
    ans = {cols[r["arm"]]: said(r) for r in rows if r["scene"] == first and r["reader"] == "PP" and r["arm"] in cols}
    # which sentence each route reads its locker from (brief 6): identity, the moved item's own sentence in this scene;
    # position, the sentence in the slot the moved item's sentence holds in the changed scene; value, the moved item's
    # new number, which only the changed scene has
    ex, item = case["expect"], case["cf_bridge"]
    here = [x for x in _sentences(case["context"]) if x.startswith("The locker of")]
    there = [x for x in _sentences(case["cf_context"]) if x.startswith("The locker of")]
    own = next(x for x in here if f"the {item} is " in x)
    moved = next(x for x in there if f"the {item} is " in x)
    slot = here[there.index(moved)]
    assert own.endswith(f" {ex['identity']}."), (own, ex)
    assert slot.endswith(f" {ex['position']}."), (slot, ex)
    assert moved.endswith(f" {ex['value']}."), (moved, ex)
    lines = [("identity", f"locker {ex['identity']}", f": the {item}'s own sentence here, “{own}”"),
             ("position", f"locker {ex['position']}", f": the sentence in the slot the {item}'s holds in the changed "
                                                       f"scene, “{slot}”"),
             ("value", f"locker {ex['value']}", f": the {item}'s number in the changed scene only, “{moved}”")]  # fmt: skip
    routes_lines = [[(f"{k} route → {where}", ROUTE_ROLE[k], True), (rest, None)] for k, where, rest in lines]
    prompt = [bold(case["context"], case["bridge"]),
              [("Lookup:", "lookup", True), (f" {rd['question']}", None)],
              [("The change:", None, True), (f" the bridge word's state comes from the scene with another item moved: "
                                             f"{case['cf_context']}", None)],
              *routes_lines]  # fmt: skip
    card = sp.Card(prompt=prompt, columns=[c for _, c in ROUTE_ARMS], rows=[sp.CardRow("lookup", "lookup", ans)],
                   note="Qwen 9B · picked by its outcome, to show the typical case")
    src = f"{rel(ROUTES)}/outcomes.jsonl"
    write_keys({"e4.items": (first, "id", f"rule (picked by its outcome, to show the typical case): the first scene of "
                                         f"the routes test's 'another item moved' condition in {src}, Qwen 9B, lookup, "
                                         "whose whole change goes to the position route, stays there without the lens "
                                         "part and leaves it without the address (original or identity)"),
                "e4.pairs_all": (len(routes), "count", f"{src}: the 'another item moved' condition's scenes (lookup)"),
                "e4.pairs_position": (sum(rt.get("whole") == "position" for rt in routes.values()), "count",
                                      f"{src}: of those, the whole change sends the lookup to the position route"),
                "e4.pairs_shown": (sum(_route_shown(rt) for rt in routes.values()), "count",
                                   f"{src}: of those, the lookup also stays on the position route without the lens "
                                   "part and leaves it without the address (back to the original or to identity)")})  # fmt: skip
    return sp.Figure("e4_routes", vocab(), direct_labels=True).add(card)


# ---- E5: how the address is found --------------------------------------------------------------------------------------
PROBE = REPO / "results/x0_probe/qwen35_9b_x0_probe_v4"  # the 9B's address (x6_routes.STATES): x0_massmean.subspaces
E5_SEED = 0  # the scene split (fit half / held-out half), fixed before looking at the projection


def _address_projection() -> tuple[list[int], list[np.ndarray], dict]:
    """The address as the routes test builds it (x0_massmean.subspaces: each locker-before state minus its layout
    group's mean, then the mean per place of the item's locker sentence; the span of the means' differences), refit on
    one half of the scenes (a seeded shuffle of scene ids); the other half's states projected on it. Returns the
    places, each place's held-out points on the averages' first two principal components, and the caption's numbers
    (the nearest-average rate in the full span, not in the 2D view)."""
    import random

    from scripts import x0_massmean as MM
    from scripts import x0_probe as P

    kept, h, _res, _items, _size = MM.layout_free(PROBE.name)
    scenes = sorted({it["scene"] for it in kept})
    random.Random(E5_SEED).shuffle(scenes)
    fit_sc = set(scenes[: len(scenes) // 2])

    def free(idx: list[int]) -> tuple[np.ndarray, list[dict]]:  # layout-free within the half; singleton groups out
        group = [P.layout(kept[i]["context"], kept[i]["pick_index"]) for i in idx]
        size = Counter(group)
        keep = [j for j, g in enumerate(group) if size[g] > 1]
        res = h[[idx[j] for j in keep]].copy()
        for g in {group[j] for j in keep}:
            rows = [r for r, j in enumerate(keep) if group[j] == g]
            res[rows] -= res[rows].mean(0)
        return res, [kept[idx[j]] for j in keep]

    rf, itf = free([i for i, it in enumerate(kept) if it["scene"] in fit_sc])
    rh, ith = free([i for i, it in enumerate(kept) if it["scene"] not in fit_sc])
    places = sorted({it["locker_index"] for it in itf})
    means = np.stack([rf[[k for k, it in enumerate(itf) if it["locker_index"] == q]].mean(0) for q in places])
    centred = means - means.mean(0)
    _u, sv, vt = np.linalg.svd(centred, full_matrices=False)
    span = vt[: int((sv > sv.max() * 1e-8).sum())]  # the address: the span of the averages' differences
    xy = (rh - means.mean(0)) @ span.T  # each held-out state's part along the address (rows: components by size)
    lab = np.array([it["locker_index"] for it in ith])
    nearest = np.array(places)[np.argmin(((xy[:, None, :] - (centred @ span.T)[None]) ** 2).sum(-1), 1)]
    nums = {"n_fit": len(itf), "n_held": len(ith), "places": len(places), "rank": len(span),
            "var_pc12": float((sv[:2] ** 2).sum() / (sv**2).sum()),
            "acc": float((nearest == lab).mean()), "acc_majority": max(Counter(lab.tolist()).values()) / len(lab)}  # fmt: skip
    return places, [xy[lab == q][:, :2] for q in places], nums


def _scene(order: tuple[str, str, str]) -> list[list[tuple]]:
    """A three-locker scene on two lines, the elephant's locker sentence bold, Ruby's pick last (verbatim words)."""
    num = {"elephant": 3, "owl": 5, "turkey": 8}
    sents = [(f"The locker of the {x} is {num[x]}.", None, x == "elephant") for x in order]
    return [[sents[0], (" ", None), sents[1]], [sents[2], (" Ruby picked the elephant.", None)]]


def e5_address() -> sp.Figure:
    """How the address is found (critic's briefs 7 and 7b, 11 Nov). Top: one scene, Ruby's pick the elephant, with the
    elephant's locker sentence at place 1, 2 and 3 (real sentences); the bridge word's state averaged over many scenes
    per place; the three averages into the address, the differences between them. The note: the average for each
    layout (which sentences before the pick are locker sentences) is subtracted first, before the averages per place
    (x0_massmean.layout_free, then subspaces). The swap, as Figure 9 does it: add average, place 3 minus average,
    place 1 at Ruby's bridge word; it reads as place 3; her lookup answers with the turkey's locker. Bottom: the 9B's
    held-out states on the averages' first two principal components, one panel per place (a colour is a role, so each
    place gets its own panel, the other places grey). Nothing claims a shape for the code."""
    layer = json.loads((PROBE / "manifest.json").read_text())["layer"]
    orders = (("elephant", "owl", "turkey"), ("owl", "elephant", "turkey"), ("owl", "turkey", "elephant"))
    el: list = [sp.Words(0.2, 0.15, [("for example, three places", None, True)]),
                sp.Words(5.65, 0.15, [("averaged over many scenes", None)])]  # fmt: skip
    mids = []
    for i, order in enumerate(orders):
        y = 0.45 + 0.9 * i
        lines = _scene(order)
        el += [sp.Box(0.2, y, 5.0, 0.75), sp.Words(0.32, y + 0.2, lines[0], verbatim=True),
               sp.Words(0.32, y + 0.5, lines[1], verbatim=True), sp.Arrow((5.25, y + 0.375), (5.6, y + 0.375)),
               sp.Box(5.65, y + 0.1, 2.0, 0.55, f"average, place {i + 1}")]  # fmt: skip
        mids.append(y + 0.375)
    el += [sp.Box(8.3, 1.2, 2.3, 1.05, role="address"),
           sp.Words(8.45, 1.45, [("the address:", "address")]),
           sp.Words(8.45, 1.72, [("differences between", "address")]),
           sp.Words(8.45, 1.99, [("the averages", "address")])]  # fmt: skip
    el += [sp.Arrow((7.7, m), (8.25, 1.725)) for m in mids]
    el += [sp.Words(0.2, 3.3, [("we first subtract the average for each layout (which sentences before the pick are "
                                "locker sentences),", None)]),
           sp.Words(0.2, 3.57, [("because the layout alone hints at the answer", None)])]  # fmt: skip
    # the swap, drawn: Ruby's bridge word at place 1, plus the difference of two averages, read as place 3
    y = 4.25
    el += [sp.Words(0.2, 4.0, [("swap", "address", True)]),
           sp.Box(0.2, y, 2.55, 0.55, "Ruby's elephant at place 1"),
           sp.Arrow((2.8, y + 0.275), (6.25, y + 0.275), role="address", label="+ (average, place 3 − average, place 1)"),
           sp.Box(6.3, y, 1.65, 0.55, "reads as place 3"), sp.Arrow((8.0, y + 0.275), (8.25, y + 0.275)),
           sp.Box(8.3, y, 2.3, 0.55, "lookup: the turkey's locker"),
           sp.Words(0.2, 5.15, [("swap", "address", True), (": Ruby's elephant sits at place 1. We add (average, place 3 "
                                                            "− average, place 1) to her bridge word.", None)]),
           sp.Words(0.2, 5.42, [("Her lookup now answers with the locker sentence at place 3, the turkey's.", None)])]  # fmt: skip
    places, clouds, nums = _address_projection()
    panels = []
    for q, xy in zip(places, clouds, strict=True):
        rest = np.concatenate([c for p, c in zip(places, clouds, strict=True) if p != q])
        panels.append(sp.ScatterPanel([sp.Cloud("the other places", "control", rest, cell=f"rest.{q}"),
                                       sp.Cloud(f"place {q + 1}", "address", xy, cell=f"place.{q}")],
                                      embedding="PCA", header=f"place {q + 1}"))  # fmt: skip
    src = f"{rel(PROBE)}/states.npz + items.jsonl (layer {layer})"
    write_keys({"e5.items": (f"seed {E5_SEED}", "id", f"rule (fixed before the projection was drawn): {src}, the "
                                                  "items whose locker sentence comes before the asked pick; scene ids "
                                                  f"shuffled by random.Random({E5_SEED}), the first half fits the "
                                                  "averages, the second half is projected"),
                "e5.layer": (layer, "count", f"{src}: the 9B's layer fixed in advance (manifest.json layer)"),
                "e5.places": (nums["places"], "count", f"{src}: places of the item's locker sentence in the passage "
                                                       "(sentence 1 to 5, before the asked pick)"),
                "e5.n_fit": (nums["n_fit"], "count", f"{src}: items fitting the averages"),
                "e5.n_held": (nums["n_held"], "count", f"{src}: held-out items projected"),
                "e5.var_pc12": (round(nums["var_pc12"], 3), "share", f"{src}: the averages' variance on the two "
                                                                    "principal components drawn"),
                "e5.acc": (round(nums["acc"], 3), "share", f"{src}: held-out items whose part along the address "
                                                         f"(refit on the other half, rank {nums['rank']}) is nearest their "
                                                         "own place's average"),
                "e5.acc_majority": (round(nums["acc_majority"], 3), "share", f"{src}: the same by always guessing the "
                                                                          "most common place")})  # fmt: skip
    return sp.Figure("e5_address", vocab()).add(sp.Schematic(5.65, el), sp.Scatter(panels, panel_h=2.4))


FIGS = {"e1_locker_scene": e1_locker_scene, "e2_fact_passage": e2_fact_passage, "e3_chains": e3_chains,
        "e4_routes": e4_routes, "e5_address": e5_address}  # fmt: skip


if __name__ == "__main__":
    failed = [f for g in GROUPS for f in L.build(g, FIGS, TARGET, ids=sys.argv[1:] or None)]
    sys.exit(1 if failed else 0)
