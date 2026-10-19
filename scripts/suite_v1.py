"""suite_v1: part B's consolidated prompt suite (Zach, 2026-10-19: consolidate, balance, avoid linearly related bridge
-> answer pairs such as France -> Paris, high quality, enough items per family for useful intervals).

Every family asks one question whose answer needs an intermediate variable (the bridge), in the chat format
(bridge_jspace.chat: one user turn, thinking off, "Answer:" prefilled), with a counterfactual C that changes only the
bridge (to X) and an off-path control O that changes something the answer does not depend on. C and O line up with the
clean prompt token for token (checked here), so exp04/exp09's copy-and-split runs apply unchanged.

The 2x2 core (one pool of 16 animals; the same context in all four families, only the question differs):
  BL  bound -> lookup:    "Jack's pet is a cow. ... The cow's locker is 5. ... Which locker belongs to Jack's pet?"
  BR  bound -> recall:    same context, "How many legs does Jack's pet have?"
  RL  recalled -> lookup: same context, "Which locker belongs to the animal known for mooing?"
  RR  recalled -> recall: same context, "How many legs does the animal known for mooing have?"
  Lockers are odd digits, legs even (2, 4, 6, 8): the two answer sets never overlap, and legs is many-to-one (many
  animals have 4), so an answer cannot stand in for its bridge the way Paris stands in for France. C: the queried
  person's pet swapped with another's (B*), or the cue replaced by another animal's (R*); O: the lockers of the two
  animals off the path swapped. BL/BR and RL/RR items come in pairs with the same prompts up to the question.
Generality (both hops in the prompt):
  NAMES  "Alice's partner is Ben. ... Ben's sister is Grace. ... Who is the sister of Alice's partner?"
  CODE   a two-dictionary Python lookup, "What does this Python code print?"
  (BREW, brew's colour-table chain, keeps its own item files and pipeline: data/brew_test.json, brew_fresh.json.)

Stages:  make (data/suite_v1/*.json, write-once; tokenizer only)   check (alignment, uniqueness, balance; tokenizer)
         competence --name N (every item: clean, C, O and each hop alone, unedited; GPU)   report --name N
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins

DATA = pins.DATA_DIR / "suite_v1"
RESULTS = pins.RESULTS_DIR / "suite_v1"
FAMILIES = ("BL", "BR", "RL", "RR", "NAMES", "CODE")
N_PER_FAMILY = 400  # competence on every item; mechanistic runs sample >= 150 eligible (README: interval widths)
SEED = 101
INSTRUCTION = chat.QUESTION_INSTRUCTION
# Animals: single tokens after a space, consonant-initial (so "a cow" / "a duck" keep the article and the alignment),
# each with a 2-token cue naming it alone (bleating: sheep or goat; stripes: tiger or zebra; mane: lion or horse;
# buzzing: bee or fly were dropped). Legs as commonly stated.
ANIMALS = {  # animal: (legs, cue for "the animal known for {cue}")
    "dog": (4, "barking"),
    "cat": (4, "purring"),
    "frog": (4, "croaking"),
    "cow": (4, "mooing"),
    "horse": (4, "neighing"),
    "mouse": (4, "squeaking"),
    "wolf": (4, "howling"),
    "pig": (4, "oinking"),
    "sheep": (4, "its wool"),
    "lion": (4, "its roar"),
    "duck": (2, "quacking"),
    "goose": (2, "honking"),
    "chicken": (2, "clucking"),
    "turkey": (2, "gobbling"),
    "bee": (6, "making honey"),
    "spider": (8, "spinning webs"),
}
LEG_WEIGHTS = {
    2: 0.35,
    4: 0.45,
    6: 0.1,
    8: 0.1,
}  # the bridge's legs: every value present, bridges not dominated by bee/spider
LOCKERS: tuple[int, ...] = (1, 3, 5, 7, 9)
FEMALE = ['Alice', 'Anna', 'Beth', 'Clara', 'Diana', 'Emma', 'Eva', 'Fiona', 'Grace', 'Iris', 'Julia', 'Kate', 'Laura', 'Lily', 'Lucy', 'Maria', 'Mia', 'Nina', 'Olivia', 'Rose', 'Sara', 'Tara', 'Vera', 'Zoe', 'Ella', 'Ruby', 'Amy', 'Eve', 'Ivy']  # fmt: skip
MALE = [
    "Adam",
    "Ben",
    "Carl",
    "Dan",
    "David",
    "Eric",
    "Finn",
    "Frank",
    "Henry",
    "Ivan",
    "Jack",
    "James",
    "Leo",
    "Luke",
    "Mark",
    "Max",
    "Noah",
    "Oscar",
    "Paul",
    "Peter",
    "Sam",
    "Tom",
    "Victor",
    "Will",
    "Hugo",
    "Owen",
    "Liam",
    "Ryan",
    "Sean",
    "Kyle",
]
PEOPLE = FEMALE + MALE
CODE_KEYS = ("cat", "dog", "cow", "fox", "owl", "pig", "bee", "ant", "rat", "bat", "hen", "elk")
CODE_VALUES = ("apple", "pear", "lime", "berry", "banana", "fig", "book", "lamp", "door", "tree", "ship", "coin", "key",
               "ring", "cup", "hat", "box", "pen", "car", "map", "star", "boat", "drum", "rose")  # fmt: skip
DIGITS = tuple(range(1, 10))


def tokenizer():
    from bridge_jspace.tokens import load_tokenizer

    return load_tokenizer()


def render(tok, context: str, question: str) -> str:
    """The prompt as every run feeds it: the context, the question and the instruction in one user turn, thinking off,
    the assistant turn prefilled "Answer:"."""
    return chat.chat_text(tok, f"{context}\n{question} {INSTRUCTION}")


def ids(tok, text: str) -> list[int]:
    return tok(text, add_special_tokens=False).input_ids


# ---- the 2x2 core ---------------------------------------------------------------------------------------------------


def pick_bridge(rng: random.Random) -> str:
    legs = rng.choices(list(LEG_WEIGHTS), weights=list(LEG_WEIGHTS.values()))[0]
    return rng.choice([a for a, (n, _) in ANIMALS.items() if n == legs])


def core_scene(rng: random.Random) -> dict:
    """Three people with three pets (the bridge I, the counterfactual X with other legs than I, a third Z), each pet's
    locker (distinct odd digits), sentences in seeded orders; the clean, C (B and R versions) and O contexts."""
    bridge = pick_bridge(rng)
    x = rng.choice([a for a in ANIMALS if ANIMALS[a][0] != ANIMALS[bridge][0]])
    z = rng.choice([a for a in ANIMALS if a not in (bridge, x)])
    people = rng.sample(PEOPLE, 3)
    pets = [bridge, x, z]
    rng.shuffle(pets)  # who owns which, in sentence order
    lockers = dict(zip([bridge, x, z], rng.sample(LOCKERS, 3), strict=True))
    table_order = rng.sample([bridge, x, z], 3)

    def context(owner_pets: list[str], locks: dict[str, int]) -> str:
        own = " ".join(f"{p}'s pet is a {a}." for p, a in zip(people, owner_pets, strict=True))
        table = " ".join(f"The {a}'s locker is {locks[a]}." for a in table_order)
        return f"{own} {table}"

    holder = people[pets.index(bridge)]
    swapped = list(pets)
    i, j = pets.index(bridge), pets.index(x)
    swapped[i], swapped[j] = swapped[j], swapped[i]
    off_locks = dict(lockers)
    off_locks[x], off_locks[z] = lockers[z], lockers[x]
    return {
        "bridge": bridge,
        "x": x,
        "z": z,
        "holder": holder,
        "people": people,
        "pets": pets,
        "lockers": lockers,
        "context": context(pets, lockers),
        "cf_context_b": context(swapped, lockers),  # B*: the holder now owns X
        "off_context": context(pets, off_locks),  # X's and Z's lockers swapped: off I's path
    }


def core_items(rng: random.Random, n: int) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {f: [] for f in ("BL", "BR", "RL", "RR")}
    seen = set()
    k = 0
    while len(out["BL"]) < n:
        s = core_scene(rng)
        if s["context"] in seen:
            continue
        seen.add(s["context"])
        b, x, holder = s["bridge"], s["x"], s["holder"]
        cue_b, cue_x = ANIMALS[b][1], ANIMALS[x][1]
        legs_b, legs_x = ANIMALS[b][0], ANIMALS[x][0]
        lock_b, lock_x = s["lockers"][b], s["lockers"][x]
        base = {"scene": f"S-{k:04d}", "bridge": b, "cf_bridge": x, "third": s["z"], "context": s["context"],
                "off_context": s["off_context"], "people": s["people"], "pets": s["pets"], "lockers": s["lockers"]}  # fmt: skip
        hop1_b = {"question": f"Which animal is {holder}'s pet?", "answer": b, "kind": "animal"}
        hop1_r = {"question": f"Which animal is known for {cue_b}?", "answer": b, "kind": "animal"}
        hop2_l = {"question": f"Which locker belongs to the {b}?", "answer": str(lock_b), "kind": "digit"}
        hop2_r = {"question": f"How many legs does a {b} have?", "answer": str(legs_b), "kind": "digit"}
        q = {
            "BL": (f"Which locker belongs to {holder}'s pet?", None, lock_b, lock_x, hop1_b, hop2_l, holder),
            "BR": (f"How many legs does {holder}'s pet have?", None, legs_b, legs_x, hop1_b, hop2_r, holder),
            "RL": (f"Which locker belongs to the animal known for {cue_b}?",
                   f"Which locker belongs to the animal known for {cue_x}?", lock_b, lock_x, hop1_r, hop2_l, cue_b),
            "RR": (f"How many legs does the animal known for {cue_b} have?",
                   f"How many legs does the animal known for {cue_x} have?", legs_b, legs_x, hop1_r, hop2_r, cue_b),
        }  # fmt: skip
        for fam, (question, cf_question, ans, cf_ans, h1, h2, cue) in q.items():
            bound = fam.startswith("B")
            out[fam].append(
                {
                    "id": f"{fam}-{len(out[fam]):04d}",
                    "family": fam,
                    **base,
                    "cue": cue,
                    "question": question,
                    "cf_context": s["cf_context_b"] if bound else s["context"],
                    "cf_question": question if bound else cf_question,
                    "answer": str(ans),
                    "cf_answer": str(cf_ans),
                    "answer_kind": "digit",
                    "hop1": h1,
                    "hop2": h2,
                }
            )
        k += 1
    return out


# ---- generality families --------------------------------------------------------------------------------------------


def names_items(rng: random.Random, n: int) -> list[dict]:
    out, seen = [], set()
    while len(out) < n:
        f = rng.sample(FEMALE, 6)
        m = rng.sample(MALE, 3)
        askers, sisters = f[:3], f[3:]
        partner = dict(zip(askers, m, strict=True))
        sister = dict(zip(m, sisters, strict=True))
        q = rng.randrange(3)
        o = rng.choice([i for i in range(3) if i != q])
        z = next(i for i in range(3) if i not in (q, o))
        a_order, s_order = rng.sample(range(3), 3), rng.sample(range(3), 3)

        def context(part, sis, askers=askers, m=m, a_order=a_order, s_order=s_order) -> str:
            first = " ".join(f"{askers[i]}'s partner is {part[askers[i]]}." for i in a_order)
            second = " ".join(f"{m[i]}'s sister is {sis[m[i]]}." for i in s_order)
            return f"{first} {second}"

        cf_part = dict(partner)
        cf_part[askers[q]], cf_part[askers[o]] = partner[askers[o]], partner[askers[q]]
        off_sis = dict(sister)
        off_sis[m[o]], off_sis[m[z]] = sister[m[z]], sister[m[o]]
        ctx = context(partner, sister)
        if ctx in seen:
            continue
        seen.add(ctx)
        bridge, x = m[q], m[o]
        out.append(
            {
                "id": f"NAMES-{len(out):04d}",
                "family": "NAMES",
                "context": ctx,
                "cf_context": context(cf_part, sister),
                "off_context": context(partner, off_sis),
                "question": f"Who is the sister of {askers[q]}'s partner?",
                "cf_question": f"Who is the sister of {askers[q]}'s partner?",
                "cue": askers[q],
                "bridge": bridge,
                "cf_bridge": x,
                "third": m[z],
                "answer": sister[bridge],
                "cf_answer": sister[x],
                "answer_kind": "name",
                "hop1": {"question": f"Who is {askers[q]}'s partner?", "answer": bridge, "kind": "name"},
                "hop2": {"question": f"Who is {bridge}'s sister?", "answer": sister[bridge], "kind": "name"},
            }
        )
    return out


def code_items(rng: random.Random, n: int, keys: list[str], values: list[str]) -> list[dict]:
    out, seen = [], set()
    while len(out) < n:
        k = rng.sample(keys, 3)
        v = rng.sample(values, 3)
        d = rng.sample(DIGITS, 3)
        first = dict(zip(k, v, strict=True))
        second = dict(zip(v, d, strict=True))
        q = rng.randrange(3)
        o = rng.choice([i for i in range(3) if i != q])
        z = next(i for i in range(3) if i not in (q, o))
        o1, o2 = rng.sample(range(3), 3), rng.sample(range(3), 3)

        def code(x, sec, call="print(second[first[x]])", k=k, v=v, first=first, o1=o1, o2=o2) -> str:
            f_txt = ", ".join(f"'{k[i]}': '{first[k[i]]}'" for i in o1)
            s_txt = ", ".join(f"'{v[i]}': {sec[v[i]]}" for i in o2)
            return f"```python\nx = '{x}'\nfirst = {{{f_txt}}}\nsecond = {{{s_txt}}}\n{call}\n```"

        off_sec = dict(second)
        off_sec[v[o]], off_sec[v[z]] = second[v[z]], second[v[o]]
        ctx = code(k[q], second)
        if ctx in seen:
            continue
        seen.add(ctx)
        question = "What does this Python code print?"
        out.append(
            {
                "id": f"CODE-{len(out):04d}",
                "family": "CODE",
                "context": ctx,
                "cf_context": code(k[o], second),
                "off_context": code(k[q], off_sec),
                "question": question,
                "cf_question": question,
                "cue": k[q],
                "bridge": v[q],
                "cf_bridge": v[o],
                "third": v[z],
                "answer": str(second[v[q]]),
                "cf_answer": str(second[v[o]]),
                "answer_kind": "digit",
                "hop1": {"question": question, "answer": v[q], "kind": "fruit", "context": code(k[q], second, "print(first[x])")},
                "hop2": {"question": question, "answer": str(second[v[q]]), "kind": "digit",
                         "context": code(k[q], second, f"print(second['{v[q]}'])")},
            }
        )  # fmt: skip
    return out


# ---- stages ---------------------------------------------------------------------------------------------------------


def stage_make() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    tok = tokenizer()
    assert all(len(ids(tok, " " + a)) == 1 for a in ANIMALS), "an animal is not one token"
    assert all(len(ids(tok, " " + c)) == 2 for _, c in ANIMALS.values()), "a cue is not two tokens"
    assert all(len(ids(tok, " " + p)) == 1 for p in PEOPLE), "a name is not one token"
    keys = [w for w in CODE_KEYS if len(ids(tok, w)) == 1]  # inside quotes: no leading space
    values = [w for w in CODE_VALUES if len(ids(tok, w)) == 1]
    print("code keys", keys, "values", values)
    rng = random.Random(SEED)
    families = {**core_items(rng, N_PER_FAMILY), "NAMES": names_items(rng, N_PER_FAMILY),
                "CODE": code_items(rng, N_PER_FAMILY, keys, values)}  # fmt: skip
    for fam, items in families.items():
        path = DATA / f"{fam}.json"
        assert not path.exists(), f"{path} exists; data files are written once"
        blob = {"family": fam, "generator": f"scripts/suite_v1.py make (seed {SEED})", "format": (__doc__ or "").split("\n\n")[1],
                "items": items}  # fmt: skip
        path.write_text(json.dumps(blob, indent=1) + "\n")
        print("wrote", path, len(items))


def load(fam: str) -> list[dict]:
    return json.loads((DATA / f"{fam}.json").read_text())["items"]


def changed(a: list[int], b: list[int]) -> list[int] | None:
    if len(a) != len(b):
        return None
    return [i for i, (p, q) in enumerate(zip(a, b, strict=True)) if p != q]


def stage_check() -> None:
    """Alignment of C and O with the clean prompt, uniqueness, answer sanity and balance, per family."""
    tok = tokenizer()
    report: dict[str, Any] = {}
    for fam in FAMILIES:
        items = load(fam)
        stats = collections.Counter()
        answers, cf_answers, bridges, changed_n = (
            collections.Counter(),
            collections.Counter(),
            collections.Counter(),
            collections.Counter(),
        )
        prompts = set()
        for it in items:
            clean = ids(tok, render(tok, it["context"], it["question"]))
            cf = ids(tok, render(tok, it["cf_context"], it["cf_question"]))
            off = ids(tok, render(tok, it["off_context"], it["question"]))
            c, o = changed(clean, cf), changed(clean, off)
            stats["aligned"] += bool(c) and bool(o)
            stats["cf_differs"] += it["answer"] != it["cf_answer"]
            changed_n[(len(c) if c else None, len(o) if o else None)] += 1
            prompts.add(render(tok, it["context"], it["question"]))
            answers[it["answer"]] += 1
            cf_answers[it["cf_answer"]] += 1
            bridges[it["bridge"]] += 1
        stats["unique_prompts"] = len(prompts)
        report[fam] = {"n": len(items), **stats, "changed_tokens(cf,off)": {str(k): v for k, v in changed_n.items()},
                       "answers": dict(sorted(answers.items())), "bridges": dict(bridges.most_common()),
                       "distinct_bridges": len(bridges)}  # fmt: skip
        print(fam, json.dumps(report[fam]))
    (DATA / "check.json").write_text(json.dumps(report, indent=1) + "\n")


WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def first_line(text: str) -> str:
    return next((ln for ln in text.lower().split("\n") if ln.strip()), "")


def said(text: str, kind: str) -> str | None:
    line = first_line(text)
    if kind == "digit":
        for t in re.findall(r"[a-z]+|\d+", line):
            if t.isdigit():
                return t
            if t in WORDS:
                return str(WORDS.index(t))
        return None
    vocab = {"animal": ANIMALS, "name": PEOPLE, "fruit": CODE_VALUES}[kind]
    lower = {w.lower(): w for w in vocab}
    return next((lower[t] for t in re.findall(r"[a-z]+", line) if t in lower), None)


def stage_manifest(name: str, why: str) -> None:
    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    from bridge_jspace.data import sha256_of

    manifest = {
        "exp": "suite_v1",
        "run": name,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "why": why,
        "model": pins.model_pin(),
        "items": {f: {"file": str((DATA / f"{f}.json").relative_to(pins.REPO_ROOT)), "sha256": sha256_of(DATA / f"{f}.json")} for f in FAMILIES},
        "format": "chat template, thinking off, 'Answer:' prefilled; the context, a newline, the question and "
        f"'{INSTRUCTION}' in one user turn",
        "prompts": "clean, C (cf_context + cf_question), O (off_context + question), hop1 and hop2 (each step alone, "
        "with the item's context or the hop's own code)",
        "judge": "the first answer of the item's kind in the first non-empty line of the greedy continuation (digits "
        "and number words for digits; the family's name / animal / fruit vocabulary otherwise)",
        "generation": "greedy, 8 new tokens, prompts of one token length batched 64 at a time",
        "eligibility": "clean, C and O all answered (as exp09); reliable family: Wilson 95% lower bound of clean >= 0.85",
    }  # fmt: skip
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    import torch

    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.stats import wilson
    from scripts.exp03_brew_swaps import write_jsonl

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    for f, pin in manifest["items"].items():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{f} changed since the manifest"
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    prompts = []
    for fam in FAMILIES:
        for it in load(fam):
            spec = {
                "clean": (it["context"], it["question"], it["answer"], it["answer_kind"]),
                "cf": (it["cf_context"], it["cf_question"], it["cf_answer"], it["answer_kind"]),
                "off": (it["off_context"], it["question"], it["answer"], it["answer_kind"]),
                "hop1": (it["hop1"].get("context", it["context"]), it["hop1"]["question"], it["hop1"]["answer"], it["hop1"]["kind"]),
                "hop2": (it["hop2"].get("context", it["context"]), it["hop2"]["question"], it["hop2"]["answer"], it["hop2"]["kind"]),
            }  # fmt: skip
            for kind, (ctx, q, ans, akind) in spec.items():
                prompts.append({"family": fam, "id": it["id"], "kind": kind, "expected": ans, "answer_kind": akind,
                                "bridge": it["bridge"], "ids": ids(tok, render(tok, ctx, q))})  # fmt: skip
    print(len(prompts), "prompts", flush=True)
    by_len: dict[int, list[dict]] = {}
    for p in prompts:
        by_len.setdefault(len(p["ids"]), []).append(p)
    for group in by_len.values():
        for start in range(0, len(group), 64):
            chunk = group[start : start + 64]
            texts = model.generate_batch(torch.tensor([p["ids"] for p in chunk], device="cuda"), 8, [{}] * len(chunk))
            for p, text in zip(chunk, texts, strict=True):
                p["continuation"] = text
                p["said"] = said(text, p["answer_kind"])
                p["correct"] = p["said"] == p["expected"]
    print(f"generated in {time.time() - t0:.0f}s", flush=True)
    rows = [{k: v for k, v in p.items() if k != "ids"} for p in prompts]
    write_jsonl(out_dir / "items.jsonl", rows)
    summary: dict[str, Any] = {"families": {}}
    for fam in FAMILIES:
        fr = [r for r in rows if r["family"] == fam]
        per_item: dict[str, dict[str, bool]] = collections.defaultdict(dict)
        for r in fr:
            per_item[r["id"]][r["kind"]] = r["correct"]
        cells = {}
        for kind in ("clean", "cf", "off", "hop1", "hop2"):
            k = sum(v[kind] for v in per_item.values())
            cells[kind] = dict(zip(("rate", "lo", "hi"), wilson(k, len(per_item)), strict=True)) | {"k": k}
        elig = [i for i, v in per_item.items() if v["clean"] and v["cf"] and v["off"]]
        both = [v for v in per_item.values() if v["hop1"] and v["hop2"]]
        by_bridge = collections.defaultdict(list)
        for r in fr:
            if r["kind"] in ("hop1", "hop2"):
                by_bridge[r["bridge"]].append(r["correct"])
        summary["families"][fam] = {
            "n": len(per_item),
            "cells": cells,
            "eligible": len(elig),
            "clean_given_both_hops": (sum(v["clean"] for v in both), len(both)),
            "reliable": cells["clean"]["lo"] >= 0.85,
            "hop_accuracy_by_bridge": {b: round(statistics.mean(v), 3) for b, v in sorted(by_bridge.items())},
        }
    summary["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "| family | n | clean | C | O | hop1 | hop2 | eligible | reliable |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for fam, s in summary["families"].items():
        c = s["cells"]

        def fmt(x, n=s["n"]):
            return f"{x['k']}/{n} {100 * x['rate']:.0f}% [{100 * x['lo']:.0f},{100 * x['hi']:.0f}]"

        lines.append(f"| {fam} | {s['n']} | {fmt(c['clean'])} | {fmt(c['cf'])} | {fmt(c['off'])} | {fmt(c['hop1'])} | "
                     f"{fmt(c['hop2'])} | {s['eligible']} | {s['reliable']} |")  # fmt: skip
    lines += ["", "Hop accuracy by bridge (both hops alone):"]
    lines += [f"- {fam}: {json.dumps(s['hop_accuracy_by_bridge'])}" for fam, s in summary["families"].items()]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "check", "manifest", "competence"])
    ap.add_argument("--name")
    ap.add_argument("--why")
    args = ap.parse_args()
    if args.stage == "make":
        stage_make()
    elif args.stage == "check":
        stage_check()
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why)
    else:
        assert args.name, "competence needs --name"
        stage_competence(args.name)
