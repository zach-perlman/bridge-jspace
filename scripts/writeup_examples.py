"""writeup_examples: real prompts and the model's real answers for each experiment of the write-up, as text.

uv run python scripts/writeup_examples.py            # writes docs/writeup/examples.md
uv run python scripts/writeup_examples.py --check    # exit 1 if docs/writeup/examples.md is stale

Every quoted string is read from a data or run file by code, its path printed beside it; nothing is retyped. Examples
are drawn with random.Random(SEED) from each experiment's whole population (no filter on the outcome: failures stay
in), on the Qwen 27B (the registered main model). Items in Dan's hand-check sample (docs/review/review_views.yaml,
fixed_sample, seed 29) are marked.

Public data only: the multi-hop sets the repo keeps out (.gitignore: jsuite v3 / v4 / v5 items and data/sd_v1/facts.jsonl,
"Redwood asks multi-hop sets not be posted") are never quoted; their sections say what the condition is and what is
missing. Model answers are the runs' stored top tokens, decoded with the pinned tokenizer; where a run stores only a class
(the conflict test), the class is shown with the answer it names.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from functools import cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from bridge_jspace.review import checks as RC  # noqa: E402
from bridge_jspace.review import items as RI  # noqa: E402

OUT = REPO / "docs" / "writeup" / "examples.md"
SEED = 11
MODEL = "qwen3.6-27b"
NAME = "Qwen 27B"
V2 = "data/tasks_v2/jsuite_v2_test_chat/items.jsonl"
BAND_RUN = "results/ablate_v2/jsuite_v2_test_chat_ko_cand2_v1"
POINTER_RUN = "results/jswap/jswap_pointer_v2_s150_v1"
CODE_RUN = "results/x6_routes/x53_7_routes_code_27b_l"
VIEWS = "docs/review/review_views.yaml"
# the sets the repo keeps out (.gitignore); a section built on one says so and quotes nothing from it
RESTRICTED = ("data/tasks_v2/jsuite_v3", "data/tasks_v2/jsuite_v4", "data/tasks_v2/jsuite_v5", "data/sd_v1/facts.jsonl")
READER = {"PP": "lookup", "PM": "recall"}
MEMORY = ("PM", "PA", "PN", "TM", "TA", "TN")  # scripts/ptr_intervals.py: the pointer swap's memory families, pooled


# ---- reading -----------------------------------------------------------------------------------------------------
def jsonl(path: str) -> list[dict]:
    return [json.loads(line) for line in (REPO / path).read_text().splitlines() if line.strip()]


@cache
def v2_items() -> dict[str, dict]:
    return {it["id"]: it for it in jsonl(V2)}


@cache
def hand_checked() -> set[tuple[str, str]]:
    """(run name, scene) of every item in the hand-check's fixed sample (seed 29)."""
    fs = RI.spec()["fixed_sample"]
    return {(e["run"].split("/")[-1], e["scene"]) for items in fs["views"].values() for e in items}


def hc(run: str) -> str:
    """How many of the hand-check sample's items come from this run (each marked where shown)."""
    k = sum(r == run.split("/")[-1] for r, _ in hand_checked())
    if not k:
        return " · hand-check sample (seed 29): none from this run"
    return f" · hand-check sample (seed 29): {k} scene{'s' * (k != 1)} of this run, marked where shown"


def mark(run: str, scene: str) -> str:
    return " · in the hand-check sample (seed 29)" if (run.split("/")[-1], scene) in hand_checked() else ""


def tok(t) -> str:
    """A stored top token, decoded with the pinned tokenizer, as inline code."""
    return f"`{json.dumps(RC.piece(MODEL, int(t)))}`"


def decode(ids: list[int]) -> str:
    return RC.tokenizer(MODEL).decode([int(i) for i in ids], skip_special_tokens=False)


@cache
def renderer():
    """scripts/tasks_v2.py render with the pinned tokenizer: the text the fact-passage runs fed the model."""
    from transformers import AutoTokenizer

    from bridge_jspace import pins
    from scripts import tasks_v2 as TV

    t = pins.TARGETS[MODEL]
    tk = AutoTokenizer.from_pretrained(t["repo"], revision=t["revision"])
    return lambda item: TV.render(tk, item)


# ---- writing -----------------------------------------------------------------------------------------------------
def code(text: str) -> list[str]:
    fence = "````" if "```" in text else "```"
    return [fence + "text", text.rstrip("\n"), fence]


def shorten(context: str, keep: tuple[str, ...]) -> str:
    """The passage's first line, then only the sentences that name one of `keep`; "…" for each run left out."""
    out: list[str] = []
    for k, line in enumerate(context.split("\n")):
        if k == 0:
            out.append(line)
            continue
        kept: list[str] = []
        for sent in re.split(r"(?<=[.!?]) ", line):
            if any(w and w in sent for w in keep):
                kept.append(sent)
            elif not kept or kept[-1] != "…":
                kept.append("…")
        line = " ".join(kept)
        if line != "…" or out[-1] != "…":
            out.append(line)
    return "\n".join(out)


def lure(top: int, item_id: str) -> str:
    """A wrong answer whose token starts a word of the passage: that word (the passage's own value, a lure)."""
    t = RC.piece(MODEL, int(top)).strip()
    m = re.search(rf"\b{re.escape(t)}\w*", v2_items()[item_id]["context"]) if len(t) > 1 else None
    return f" (starts `{m.group(0)}`, a word in the passage)" if m else ""


def table(head: list[str], rows: list[list[str]]) -> list[str]:
    return ["| " + " | ".join(head) + " |", "|" + "---|" * len(head), *("| " + " | ".join(r) + " |" for r in rows)]


def withheld(lines: list[str], what: str, figure: str, generator: str, runs: list[str], rows_exist: list[str]) -> None:
    lines += [f"_{what} ({figure})._ Withheld: multi-hop set not posted in the public repo (`.gitignore`; rebuild with "
              f"`{generator}`)."]  # fmt: skip
    for r in runs:
        have = [f for f in rows_exist if (REPO / r / f).exists()]
        lines.append(f"- `{r}`: " + (f"per-item rows in the repo ({', '.join(f'`{f}`' for f in have)}), their prompts "
                                     "withheld" if have else "source missing: run rows not in the repo"))  # fmt: skip
    lines.append("")


# ---- sections ----------------------------------------------------------------------------------------------------
def twin_set(lines: list[str]) -> None:
    """The band test's fact passages: a lookup twin (the fact in the passage) and its recall twin (the fact from memory),
    same scene, question and answer; the knock-out (lens part removed over layers 32-40) and its rotated control."""
    rows = jsonl(f"{BAND_RUN}/rows.jsonl")
    by = {(r["id"], r["condition"]): r for r in rows}
    ids = {r["id"] for r in rows}
    pairs = sorted(i for i in ids if ":PK-" in i and i.replace(":PK-", ":PM-") in ids)
    rng = random.Random(SEED)
    picked = rng.sample(pairs, 2)
    conds = (
        ("none", "unedited"),
        ("paper10", "knock-out: the lens part taken out"),
        ("paper10_rot", "rotated control"),
    )
    lines += ["## 1. Twin set: fact passages", "",
              f"Population: every lookup / recall twin pair the band test read (`{BAND_RUN}`, families `PK` / `PM`, "
              f"paired by scene) · model {NAME} · seed {SEED} · n = {len(pairs)} pairs{hc(BAND_RUN)}.", "",
              "The two twins share the question and the answer. In the lookup twin the passage holds the last fact; in "
              "the recall twin it does not, and the answer must come from memory. Answers are the run's top first token "
              f"(`{BAND_RUN}/rows.jsonl`, `top_id`, decoded); right or wrong is the run's own `correct`.", ""]  # fmt: skip
    for n, pk in enumerate(picked):
        pm = pk.replace(":PK-", ":PM-")
        a, b = v2_items()[pk], v2_items()[pm]
        lines += [f"### Pair {n + 1}: bridge **{a['bridge']}**", "",
                  f"Question (both twins): `{a['question']}` → expected `{a['answer']}`; lookup twin: in the passage; "
                  "recall twin: from memory.", ""]  # fmt: skip
        if n == 0:
            lines += [f"Lookup twin, the full prompt as the model read it (`{V2}` → `{pk}`, rendered by "
                      "`scripts/tasks_v2.py` `render`):", "", *code(renderer()(a)), ""]  # fmt: skip
        else:
            lines += [f"Lookup twin, shortened (full text: `{V2}` → `{pk}` → `context`):", "",
                      *code(shorten(a["context"], (a["bridge"],))), ""]  # fmt: skip
        lines += [f"Recall twin, shortened (full text: `{V2}` → `{pm}` → `context`):", "",
                  *code(shorten(b["context"], (b["bridge"],))), ""]  # fmt: skip
        cells = []
        for c, label in conds:
            cell = []
            for i in (pk, pm):
                r = by.get((i, c))
                ok = "right" if r and r["correct"] else ("wrong" + lure(r["top_id"], i) if r else "")
                cell.append(f"{tok(r['top_id'])} {ok}" if r else "source missing")
            cells.append([label, *cell])
        lines += [*table(["condition", "lookup twin answers", "recall twin answers"], cells), ""]
    lines += ["Answer span kept: not run on this set; see the twin set below.", ""]
    withheld(
        lines,
        "The registered twin set: knock-out, rotated, answer span kept",
        "Fig. 4, Fig. 10a",
        "scripts/jsuite_v4.py --seed 4001",
        ["results/ablate_v2/jsuite_v4_test_chat_ko41_cand2_v1"],
        ["rows.jsonl"],
    )
    withheld(lines, "The codename set: the answer span alone removed", "Fig. 10c", "scripts/jsuite_v5al.py --seed 5201",
             ["results/ablate_v2/jsuite_v5al_test_chat_ko57_cand2_v1"], ["rows.jsonl"])  # fmt: skip


def x0_cell(case: dict, reader: str, r: dict | None) -> str:
    """The conflict test stores a class, not the token: A = the original scene's answer, b = the changed scene's."""
    if r is None:
        return "source missing"
    q = case["readers"][reader]
    return {"A": f"`{q['answer']}` (original answer)", "b": f"`{q['cf_answer']}` (changed scene's answer)"}.get(
        r["role"], "another token (not stored)"
    )


def by_scene(items: list[dict]) -> dict[str, dict[str, dict]]:
    out: dict[str, dict[str, dict]] = {}
    for it in items:
        out.setdefault(it["scene"], {})[it["reader"]] = it
    return out


def scene_block(lines: list[str], n: int, scene: str, its: dict[str, dict], run: str, full: bool, cells,
                label: str = "") -> None:  # fmt: skip
    case = next(iter(its.values()))["case"]
    pp, pm = case["readers"]["PP"], case["readers"]["PM"]
    lines += [f"### Scene {n + 1}{', ' + label if label else ''}: `{scene}`, bridge **{case['bridge']}**"
              f"{mark(run, scene)}", ""]  # fmt: skip
    if full and "ids" in pp:
        lines += [f"Lookup, the full prompt as the model read it (`{run}/cases.jsonl` → `{scene}` → "
                  "`readers.PP.ids.org`, decoded):", "", *code(decode(pp["ids"]["org"])), ""]  # fmt: skip
    else:
        lines += [f"Scene (`{run}/cases.jsonl` → `{scene}` → `context`):", "", *code(case["context"]), ""]
    if case.get("cf_context"):
        lines += ["Changed scene (`cf_context`), whose bridge state is patched in:", "", *code(case["cf_context"]), ""]
    lines += [f"Lookup: `{pp['question']}` → `{pp['answer']}` (in the scene). Recall: `{pm['question']}` → "
              f"`{pm['answer']}` (from memory).", ""]  # fmt: skip
    lines += [*table(["condition", "lookup answers", "recall answers"], cells(case)), ""]


def conflict_test(lines: list[str]) -> None:
    v = RI.view("main_swap")
    items = RI.items("main_swap", MODEL)
    scenes = by_scene(items)
    run = items[0]["run"]
    picked = random.Random(SEED).sample(sorted(scenes), 3)
    arms = (("unedited", "unedited"), ("whole", "the whole change"), ("without J++", "the whole change without the lens part"),
            ("without a same-size random part (control)", "the whole change without a random part of the same size"))  # fmt: skip
    lines += ["## 2. Locker scenes: the conflict test", "",
              f"Population: the test's item set (`{VIEWS}` view `main_swap`; `{run}`, layer {items[0]['layer']}) · "
              f"model {NAME} · seed {SEED} · n = {len(scenes)} scenes, each read by both questions{hc(run)}.", "",
              "The change: at one layer, the bridge word's state in the changed scene minus its state in the original is "
              "added to the original run, whole or without one part. "
              f"Answers: the run stores the class only (`{run}/outcomes.jsonl`, `role`).", ""]  # fmt: skip
    del v
    for n, s in enumerate(picked):
        its = scenes[s]

        def cells(case, its=its):
            return [[label, *(x0_cell(case, w, its[w]["rows"][w].get(a) if w in its else None) for w in ("PP", "PM"))]
                    for a, label in arms]  # fmt: skip

        scene_block(lines, n, s, its, run, n == 0, cells)


def route_cell(case: dict, reader: str, r: dict | None) -> str:
    if r is None:
        return "source missing"
    if reader == "PP":
        return f"{tok(r['top'])} ({r['route']})"
    return f"{tok(r['top'])} ({'follows the changed scene' if r['switched'] else 'unchanged'})"


def routes(lines: list[str]) -> None:
    items = [i for i in RI.items("routes", MODEL) if i["condition"] == "C2"]
    scenes = by_scene(items)
    run = items[0]["run"]
    picked = random.Random(SEED).sample(sorted(scenes), 2)
    arms = (("unedited", "unedited"), ("whole", "another item moved (whole change)"),
            ("without the pointer directions", "the same, without the address"),
            ("without the pointer's random part", "the same, without a random part of the address's size"))  # fmt: skip
    lines += ["## 3. Routes and the address swap", "",
              f"Population: another item moved (`C2`; `{VIEWS}` view `routes`; `{run}`) · model {NAME} · seed {SEED} · "
              f"n = {len(scenes)} scenes{hc(run)}.", "",
              "In the changed scene another item takes the bridge item's place. The lookup's answer names its route: "
              "identity (the bridge item's own locker in the changed scene), position (the locker now at its old place), "
              f"value (the moved item's new number). Answers: `{run}/outcomes.jsonl`, `top` decoded, `route`.", ""]  # fmt: skip
    for n, s in enumerate(picked):
        its = scenes[s]

        def cells(case, its=its):
            ex = case.get("expect", {})
            rows = [[label, *(route_cell(case, w, its[w]["rows"][w].get(a) if w in its else None) for w in ("PP", "PM"))]
                    for a, label in arms]  # fmt: skip
            rows.append(["what each route predicts (lookup)", ", ".join(f"{k} `{v}`" for k, v in ex.items()), ""])
            return rows

        scene_block(lines, n, s, its, run, n == 0, cells)
    address_swap(lines)
    code_tool(lines)


def address_swap(lines: list[str]) -> None:
    items = RI.items("x8_writes", MODEL)
    write = [i for i in items if i["x8"].get("kind") == "write" and i["x8"].get("s") == 2]
    rand = {(i["scene"], i["reader"], i["x8"]["j"], i["x8"]["k"]): i for i in items
            if i["x8"].get("kind") == "random" and i["x8"].get("s") == 4}  # fmt: skip
    run = write[0]["run"]
    keys = sorted({(i["scene"], i["x8"]["j"], i["x8"]["k"]) for i in write})
    picked = random.Random(SEED).sample(keys, 2)
    lines += ["### The address swap", "",
              f"Population: every (scene, from slot, to slot) of the swap at 2× (`{VIEWS}` view `x8_writes`; `{run}`) · "
              f"model {NAME} · seed {SEED} · n = {len(keys)}{hc(run)}.", "",
              "The bridge word's address is moved from its own locker slot toward another slot's (2× the distance "
              "between the two slots' mean states); the control adds a random direction (4× its size). Answers: "
              f"`{run}/outcomes.jsonl`, `top` decoded; lookup: which slot's digit, recall: changed or not.", ""]  # fmt: skip
    for s, j, k in picked:
        w = {i["reader"]: i for i in write if (i["scene"], i["x8"]["j"], i["x8"]["k"]) == (s, j, k)}
        case = next(iter(w.values()))["case"]
        lines += [f"Scene `{s}`, bridge **{case['bridge']}**, from slot {j} to slot {k}{mark(run, s)}:", "",
                  *code(case["context"]), ""]  # fmt: skip

        def cell(it, label):
            r = (it or {}).get("rows", {}).get(it["reader"], {}).get(label) if it else None
            if r is None:
                return "source missing"
            what = (
                re.sub(r"slot(\d)", r"slot \1", r["class"])
                if "class" in r
                else ("changed" if r["changed"] else "unchanged")
            )
            return f"{tok(r['top'])} ({what})"

        rows = [
            ["unedited", *(cell(w.get(x), "unwritten") for x in ("PP", "PM"))],
            ["address swap, 2×", *(cell(w.get(x), "write s = 2") for x in ("PP", "PM"))],
            ["random direction, 4× (control)", *(cell(rand.get((s, x, j, k)), "random s = 4") for x in ("PP", "PM"))],
        ]
        q = case["readers"]
        lines += [f"Lookup: `{q['PP']['question']}`. Recall: `{q['PM']['question']}`.", "",
                  *table(["condition", "lookup answers", "recall answers"], rows), ""]  # fmt: skip


def code_tool(lines: list[str]) -> None:
    cases = [c for c in jsonl(f"{CODE_RUN}/cases.jsonl") if c["condition"] == "C2"]
    out = {
        (o["scene"], o["reader"], o["arm"]): o for o in jsonl(f"{CODE_RUN}/outcomes.jsonl") if o["condition"] == "C2"
    }
    done = sorted({s for s, _, _ in out})
    s = random.Random(SEED).choice(done)
    case = next(c for c in cases if c["scene"] == s)
    lines += ["### The same scenes as code", "",
              f"Population: another item moved, the scene as a Python dict (`{CODE_RUN}`) · model {NAME} · "
              f"seed {SEED} · n = {len(done)} scenes{hc(CODE_RUN)}.", "",
              f"The full prompt as the model read it (`{CODE_RUN}/cases.jsonl` → `{s}` → `readers.PP.ids.org`, decoded):",
              "", *code(decode(case["readers"]["PP"]["ids"]["org"])), ""]  # fmt: skip
    rows = []
    for a, label in (
        ("none", "unedited"),
        ("whole", "another item moved"),
        ("no_alf", "the same, without the address"),
    ):
        rows.append([label, *(route_cell(case, w, out.get((s, w, a))) for w in ("PP", "PM"))])
    lines += [*table(["condition", "lookup answers", "recall answers"], rows), ""]


def sentence_order(lines: list[str]) -> None:
    items = RI.items("sentence_order", MODEL)
    scenes = by_scene(items)
    run = items[0]["run"]
    first = sorted(s for s, its in scenes.items() if next(iter(its.values()))["order"].get("original") == "before")
    after = sorted(s for s, its in scenes.items() if next(iter(its.values()))["order"].get("original") == "after")
    rng = random.Random(SEED)
    lines += ["## 4. Sentence order", "",
              f"Population: the conflict test's scenes split by where the bridge item's locker sentence sits (`{VIEWS}` "
              f"view `sentence_order`; `{run}`) · model {NAME} · seed {SEED} · n = {len(first)} locker sentence first, "
              f"{len(after)} after the pick{hc(run)}.", ""]  # fmt: skip
    for n, (label, pool) in enumerate((("locker sentence first", first), ("locker sentence after the pick", after))):
        if not pool:
            lines += [f"{label}: source missing", ""]
            continue
        s = rng.choice(pool)
        its = scenes[s]

        def cells(case, its=its):
            return [[lab, *(x0_cell(case, w, its[w]["rows"][w].get(a) if w in its else None) for w in ("PP", "PM"))]
                    for a, lab in (("unedited", "unedited"), ("whole", "the whole change"))]  # fmt: skip

        scene_block(lines, n, s, its, run, False, cells, label)


def one_hop(lines: list[str]) -> None:
    lines += ["## 5. One-hop question: the city's directions", ""]
    withheld(lines, "One-hop question on the city: its directions, the same made orthogonal to the answers, the "
             "answers' own directions", "Fig. 11", "scripts/sd_build.py facts",
             ["results/sd_necessity/sd62_ko_test_v1", "results/sd_necessity/sd67_ko_test_v1"], ["rows.jsonl"])  # fmt: skip


def pointer(lines: list[str]) -> None:
    rows = jsonl(f"{POINTER_RUN}/rows.jsonl")
    neutral = json.loads((REPO / POINTER_RUN / "manifest.json").read_text())["neutral"]
    mem = [r for r in rows if r["family"] in MEMORY]
    ok = sorted({r["id"] for r in mem if r["condition"] == "none" and r["cls"] == "kept" and r["third"]})
    by = {(r["id"], r["condition"]): r for r in mem}
    picked = random.Random(SEED).sample(ok, 2)
    conds = (
        ("none", "unedited"),
        ("swap", "D's lens part, from D's mention in this passage"),
        ("swap_neutral", "D's lens part, from one neutral sentence"),
        ("swap_neutral_rot", "the same, rotated (control)"),
    )
    lines += ["## 6. Pointer swap: another entity's lens part", "",
              f"Population: the recall items right unedited with a third entity to tell chance from transfer "
              f"(`{POINTER_RUN}`, memory families pooled, as `scripts/ptr_intervals.py`) · model {NAME} · seed {SEED} · "
              f"n = {len(ok)}{hc(POINTER_RUN)}.", "",
              "At the bridge's mentions, layers 32-40, its lens part is replaced by another entity D's. D's part comes "
              "from D's own mention in the same passage, or from one neutral sentence about D, run as its own prompt:", "",
              *code(neutral), "", f"(`{POINTER_RUN}/manifest.json` → `neutral`; `{{}}` is D.) Answers: "
              f"`{POINTER_RUN}/rows.jsonl`, `pick` decoded, `cls`: kept (the bridge's answer), donor (D's), third, other.",
              ""]  # fmt: skip
    for n, i in enumerate(picked):
        r0, it = by[(i, "none")], v2_items()[i]
        lines += [f"### Item {n + 1}: bridge **{r0['x']}**, D = **{r0['donor']}**", "",
                  f"Passage, shortened (full text: `{V2}` → `{i}` → `context`):", "",
                  *code(shorten(it["context"], (r0["x"], r0["donor"]))), "",
                  f"Question: `{it['question']}` → `{r0['ax']}` (from memory); D's answer would be `{r0['ad']}`.", ""]  # fmt: skip
        cells = []
        for c, label in conds:
            r = by.get((i, c))
            cells.append([label, f"{tok(r['pick'])} ({r['cls']})" if r else "source missing"])
        lines += [*table(["condition", "recall answers"], cells), ""]


def conflict_passage(lines: list[str]) -> None:
    lines += ["## 7. Conflict passage: the passage's claim against memory", ""]
    withheld(lines, "A passage that attributes a false value to the bridge (the claim sentence template is in "
             "`scripts/jsuite_v5kc.py` `CLAIM`): the answer, and the bridge's readout", "the conflict-passage test",
             "scripts/jsuite_v5kc.py", ["results/ablate_v2/jsuite_v5kc2_test_chat_ko_cand2_v1",
                                        "results/nn_readout/nn_readout_v5kc2_v1"], ["rows.jsonl"])  # fmt: skip


def last_token(lines: list[str]) -> None:
    items = RI.items("last_token", MODEL)
    scenes = by_scene(items)
    run = items[0]["run"]
    picked = random.Random(SEED).sample(sorted(scenes), 2)
    arms = (
        ("unedited", "unedited"),
        ("lens swap", "the lens part swapped in (1×)"),
        ("its random control", "a random part of its size (control)"),
        ("whole-state patch", "the whole state patched in"),
    )
    lines += ["## 8. Last token: the lens part against the whole state", "",
              f"Population: the locker-first scenes read at the last token (`{VIEWS}` view `last_token`; `{run}`) · model "
              f"{NAME} · seed {SEED} · n = {len(scenes)} scenes{hc(run)}.", "",
              "At the last token, at the probe's best layer, the changed scene's lens part (or its whole state) replaces "
              f"the original's. Answers: `{run}/outcomes.jsonl`, `top` decoded.", ""]  # fmt: skip
    for n, s in enumerate(picked):
        its = scenes[s]

        def cells(case, its=its):
            out = []
            for a, label in arms:
                c = []
                for w in ("PP", "PM"):
                    r = its[w]["rows"][w].get(a) if w in its else None
                    c.append(
                        f"{tok(r['top'])} ({'switched' if r['switched'] else 'unchanged'})" if r else "source missing"
                    )
                out.append([label, *c])
            return out

        scene_block(lines, n, s, its, run, n == 0, cells)


def agents(lines: list[str]) -> None:
    lines += ["## 9. Agent transcripts: copy, pick, verify, produce", ""]
    withheld(lines, "Multi-agent transcripts on the same facts (copy a given answer, pick the true one of two, verify a "
             "claim, produce the answer alone)", "Fig. A1", "scripts/sd_build.py facts",
             ["results/sd_necessity/sd59_ko_test_v1", "results/sd_necessity/sd65_ko_test_v1"], ["rows.jsonl"])  # fmt: skip


SECTIONS = (twin_set, conflict_test, routes, sentence_order, one_hop, pointer, conflict_passage, last_token, agents)


def build() -> str:
    lines = ["# Examples: what the model reads, and what it answers", "",
             "Generated by `scripts/writeup_examples.py`; do not edit by hand. Status: UNVERIFIED.", "",
             f"Every example is drawn by `random.Random({SEED})` from the experiment's whole population, with no filter on "
             "the outcome. Prompts and answers are read from the files named beside them; answers are the model's top "
             "token in each condition. Sets the repo keeps out of public view are described, not quoted.", ""]  # fmt: skip
    for s in SECTIONS:
        s(lines)
    return "\n".join(lines).rstrip("\n") + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    text = build()
    if a.check:
        ok = OUT.exists() and OUT.read_text() == text
        print("docs/writeup/examples.md is " + ("current" if ok else "stale: run scripts/writeup_examples.py"))
        return 0 if ok else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(REPO)} ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
