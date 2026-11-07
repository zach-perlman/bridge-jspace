"""Real examples as images (README brief, 7 Nov, §2): one card per test, each an item picked by a stated rule (never by
its outcome), with the prompt's real text, the bridge word in bold and each reader's answer before and under each
operation, read from the per-item run files. The rule and the item id are printed on the card; the README gives each
card's population rate beside it (by key, in figures/examples/_meta/captions.toml).

  E1 depth   the main test (two people swap picks), Qwen 27B: results/x0_necessity/x0_necessity_27b_chat/
  E2 breadth a fact passage with the final fact stated (lookup) and without it (recall), Qwen 27B, jsuite v2 test:
             data/tasks_v2/jsuite_v2_test_chat/items.jsonl + results/ablate_v2/jsuite_v2_test_chat_ko_cand2_v1/rows.jsonl
  E3 chains  three three-hop chains about one entity (P → P → P, P → M → M, M → P → M), Qwen 27B: the same items file +
             results/ablate_v2/jsuite_v2_test_chat_threehop_ko_cand2_v1/rows.jsonl
  E4 routes  the routes test, another item moved (C2), Qwen 9B: results/x6_routes/qwen35_9b_x6_routes/

Nothing is rerun: an answer the files do not store as text (a knocked-out breadth answer) is its first token, decoded
with the model's tokenizer from the local cache.

uv run python scripts/examples.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import OrderedDict
from functools import cache
from pathlib import Path

import styles_plot as sp

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace.figkit import layout as L  # noqa: E402
from bridge_jspace.figkit.writeup_sp_base import vocab  # noqa: E402

GROUP, TARGET = "examples", "readme"
DEPTH = REPO / "results/x0_necessity/x0_necessity_27b_chat"
ROUTES = REPO / "results/x6_routes/qwen35_9b_x6_routes"
ITEMS = REPO / "data/tasks_v2/jsuite_v2_test_chat/items.jsonl"
KO = REPO / "results/ablate_v2/jsuite_v2_test_chat_ko_cand2_v1/rows.jsonl"
THREE = REPO / "results/ablate_v2/jsuite_v2_test_chat_threehop_ko_cand2_v1/rows.jsonl"
MAIN = ("jpp", 25, "signed")  # the main test's lens part (scripts/x0_necessity.py MAIN)
READER = {"PP": ("lookup", "lookup"), "PM": ("recall", "recall")}
BREADTH_ARMS = (("none", "before"), ("paper10", "the lens part removed everywhere"),
                ("paper10_rot", "a rotated part removed everywhere"))  # fmt: skip


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
                   note=f"Picked by rule: the main test's first scene in its per-item file ({rel(DEPTH)}/outcomes.jsonl), "
                        f"Qwen 27B, layer {layer} · item {first}")  # fmt: skip
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
    pm = next(i for i in items if i["word"] == "PM" and "PK" in scenes[i["scene"]] and i["id"] in have
              and scenes[i["scene"]]["PK"]["id"] in have)  # fmt: skip
    pk = scenes[pm["scene"]]["PK"]
    stated = [ln for ln in pk["context"].split("\n") if ln not in pm["context"].split("\n")]
    repo = json.loads((KO.parent / "manifest.json").read_text())["model"]["repo"]
    passage: list[tuple] = []
    for ln in pk["context"].split("\n"):
        text = ln.removeprefix("- ")
        if ln in stated:
            passage.append((text + " ", "lookup"))
        elif pm["bridge"] in text:
            passage += [*bold(text, pm["bridge"]), (" ", None)]
        else:
            passage.append((text + " ", None))
    parts = [passage,
             [("Recall:", "recall", True), (" the same passage without the lines in the lookup's colour.", None)],
             [("Question (both):", None, True), (f" {pk['question']}", None)]]  # fmt: skip
    answers: dict[str, dict[str, str]] = {"lookup": {}, "recall": {}}
    for r in rows:
        for item, reader in ((pk, "lookup"), (pm, "recall")):
            for cond, col in BREADTH_ARMS:
                if r["id"] == item["id"] and r["condition"] == cond:
                    answers[reader][col] = _breadth_answer(r, item["answer"], repo)
    card = sp.Card(prompt=parts, columns=[c for _, c in BREADTH_ARMS],
                   rows=[sp.CardRow("lookup", "lookup", answers["lookup"]),
                         sp.CardRow("recall", "recall", answers["recall"])],
                   note=f"Picked by rule: the first final-from-memory item in {rel(ITEMS)} whose pair (the same scene "
                        f"with the final fact stated) both passed the gate, Qwen 27B; the removal at layers "
                        f"{_band(rows)} · items {pk['id']}, {pm['id']}")  # fmt: skip
    return sp.Figure("e2_fact_passage", vocab(), direct_labels=True).add(card)


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
    key, chain = next((k, g) for k, g in groups.items()
                      if len(g) == len(CHAINS) and all(g[w]["id"] in right_before for w in g))  # fmt: skip
    repo = json.loads((THREE.parent / "manifest.json").read_text())["model"]["repo"]
    fig = sp.Figure("e3_chains", vocab(), direct_labels=True)
    for w in CHAINS:
        it = chain[w]
        hops = " → ".join(f"{c} ({LETTER[c]})" for c in w)
        reader = "recall" if w[-1] == "M" else "lookup"
        ans = {col: _breadth_answer(r, it["answer"], repo) for r in rows if r["id"] == it["id"]
               for cond, col in BREADTH_ARMS if r["condition"] == cond}  # fmt: skip
        ctx = " ".join(ln.removeprefix("- ") for ln in it["context"].split("\n"))
        prompt = [[(f"{' → '.join(w)}:", None, True), (f" {hops}.", None)], bold(ctx, it["bridge"]),
                  [("Question:", None, True), (f" {it['question']}", None)]]  # fmt: skip
        fig.add(sp.Card(prompt=prompt, columns=[c for _, c in BREADTH_ARMS],
                        rows=[sp.CardRow(reader, reader, ans)],
                        note=(f"Picked by rule: the first entity in {rel(ITEMS)} with all three chain types, each "
                              f"answered right before any removal, Qwen 27B · {key} · item {it['id']}")))  # fmt: skip
    return fig


# ---- E4: the routes test --------------------------------------------------------------------------------------------
ROUTE_ROLE = {"identity": "identity", "position": "address", "value": None}
ROUTE_ARMS = (("none", "before"), ("whole", "the whole change"), ("no_jpp", "without the lens part"),
              ("no_alf", "without the address"))  # fmt: skip


def e4_routes() -> sp.Figure:
    rows = jsonl(ROUTES / "outcomes.jsonl")
    first = next(r for r in rows if r["condition"] == "C2")["scene"]
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
    pred = [(f"{k} route: locker {case['expect'][k]}", ROUTE_ROLE[k]) for k in ("identity", "position", "value")]
    predicted: list[tuple] = [("Predicted:", None, True), (" ", None)]
    for i, (text, role) in enumerate(pred):
        predicted.append((text + (" · " if i < len(pred) - 1 else "."), role, True))
    prompt = [bold(case["context"], case["bridge"]),
              [("Lookup:", "lookup", True), (f" {rd['question']}", None)],
              [("The change:", None, True), (f" the bridge word's state comes from the scene with another item moved: "
                                             f"{case['cf_context']}", None)],
              predicted]  # fmt: skip
    card = sp.Card(prompt=prompt, columns=[c for _, c in ROUTE_ARMS], rows=[sp.CardRow("lookup", "lookup", ans)],
                   note=f"Picked by rule: the first scene of the routes test's 'another item moved' condition in "
                        f"{rel(ROUTES)}/outcomes.jsonl, Qwen 9B · item {first}")  # fmt: skip
    return sp.Figure("e4_routes", vocab(), direct_labels=True).add(card)


FIGS = {"e1_locker_scene": e1_locker_scene, "e2_fact_passage": e2_fact_passage, "e3_chains": e3_chains,
        "e4_routes": e4_routes}  # fmt: skip


if __name__ == "__main__":
    failed = L.build(GROUP, FIGS, TARGET, ids=sys.argv[1:] or None)
    sys.exit(1 if failed else 0)
