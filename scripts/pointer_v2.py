"""pointer_v2: scenes that make D3's pointer result decisive (Dan's D3 v2, 2026-10-21). On the first night (UNVERIFIED),
patching the alt prompt's tokens after the question at layers 44-50 gave the answer at the same statement SLOT more
often than the answer of bridge alt's statement (29% vs 9%, memory -> prompt, animals + elements), then the alt
prompt's own answer from ~52. Two things were left open:

  1. Is the slot an ORDER index (the k-th statement) or a TOKEN position (whatever sits at that offset)? In pointer_v1
     every statement had the same length and there was no filler, so the two always coincided.
  2. Is the late "alt prompt's own answer" the digit carried as content (H-value), or a pointer to the answer token
     that only works when that digit is in the prompt (reflexive, Mixing Mechanisms)? In pointer_v1 the alt answer
     was never in the org prompt, so a reflexive pointer had nothing to point at.

Scene: pointer_v1's statements (animals: "The cow's locker is 5."; elements: "The carbon card is in locker 5.") plus
ONE filler sentence of exactly a statement's token length (8 / 9 tokens, checked by make/check), so the context is a
grid of N + 1 equal cells: the filler takes one cell, the statements the others in their order. Families as pointer_v1
(memory -> prompt RL, named -> prompt DL, memory -> memory RR), only the question differs. Only the topics that passed
d3_competence_27b's gate (animals, elements). Lookup digits are 0-9.

Three item types per scene (separate files: level e<N>-<type>, e.g. e5-off), sharing the org prompt (same scene id) so they can be
compared item by item. In each, the alt prompt (stored as source "dissoc", so pointer_swap runs it unchanged) asks
about bridge alt q_s, states it as its k-th statement, and gives it a digit:
  off  OFFSET SHIFT: the alt prompt puts the filler in another cell than the org prompt, so q_s keeps ORDER index k but
       sits at another TOKEN offset, and the org prompt's statement at that offset is its k'-th (k' != k).
       Predictions: none d(q_b) / identity d(q_s) / position d(org k-th) [order slot] / token d(org k'-th) [same token
       position] / value v (absent from the org prompt): five distinct digits.
  pln  PLAIN (pointer_v1's design with the filler in the same cell in both prompts): none / identity / position (=
       token) / value v absent. The reference for 'ref'.
  ref  REFLEXIVE: as 'pln', but the alt prompt's own answer is a digit the org prompt also has, bound to another
       entity (its k'-th statement): none / identity / position / value = d(org k'-th). A pointer to the answer token
       (reflexive) can only produce that digit when it is in the prompt, the digit carried as content (value) also
       when it is not: the two are separated by comparing the 'value' share of ref against pln on the same scenes
       (paired), not within one item (their outputs coincide).
At N = 3 (secondary level) four distinct statements are impossible, so bridge alt is NOT in the org prompt (identity
recorded as "-"): off gives none / position / token / value, pln none / position / value, ref none / position / value
(= the org prompt's k'-th digit); and the query is the first or the last statement only (see slot_classes).

Controls in the data: "same" (q_b in its own cell with its digit, the other statements reshuffled and redigited, filler
in the org prompt's cell): every hypothesis predicts answer org; "redigit" (the org prompt with q_b's digit replaced
by v). Run-time controls are pointer_swap's (random push of the same size, another topic's prompt).

Power: the base query's slot cycles first / middle / last in equal thirds (middle = a random inner slot), so main (N = 5,
180 scenes per topic) has 60 per (topic x family x type x slot class) before the competence gate, which pointer_swap
applies per scene across all three types (so ~42 remain at the gate's ~70% for elements); N = 3 has 120 per topic (60
per slot class, first and last). Digit policy: no digit of the org or alt prompt equals the recalled digit of q_b, q_s or the two
pointed-at entities (hard); soft where the pool allows (as pointer_v1, recorded per item).

Stages:  make --set S | verify | check --set S (tokenizer only) | manifest --set S [S ...] --name N --why W [--limit K]
         competence --name N (GPU; pointer_v1's competence on these files)
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import pointer_v1 as PV
from scripts import suite_v1 as S

DATA = pins.DATA_DIR / "pointer_v2"
RESULTS = pins.RESULTS_DIR / "pointer_v2"
FAMILIES = PV.FAMILIES
DOMAINS = ("animals", "elements")  # the topics that passed d3_competence_27b's gate in every family
TYPES = ("off", "pln", "ref")
DIGITS = tuple(range(10))
SETS: dict[str, dict[str, Any]] = {
    "main": {"seed": 801, "n": 180, "n_ent": 5},
    "n3": {"seed": 802, "n": 120, "n_ent": 3},
}
# Filler sentences of exactly one statement's token length (with and without a leading space): animals' statements are
# 8 tokens, elements' 9. No digits, entities, names or question words.
FILLER = {
    "animals": ("The clock on the wall was slow.", "The door to the shed was open.", "The lamp in the hall flickered.",
                "The paper was left on the step.", "The road was wet after the rain.", "The stairs creaked at night.",
                "The wind picked up in the evening.", "The bridge was closed for urgent repairs.",
                "The market was busy on Saturday morning.", "The park was very quiet at dawn.",
                "The river was calm early that morning.", "The snow melted slowly by the evening.",
                "The street was lined with old trees.", "The table was set early for dinner.",
                "The town hall bell rang twice today.", "The weather was mild all week long.",
                "The boat left the harbor very early.", "The car park was nearly full again.",
                "The kitchen window looked onto the yard.", "The film at the cinema started late.",
                "The morning was grey and very still.", "The room still smelled of fresh paint.",
                "The shop on the corner reopened today."),
    "elements": ("The clock on the wall was slow again.", "The door to the shed was left open.",
                 "The paper was left on the front step.", "The road was wet after the long rain.",
                 "The stairs creaked loudly at night.", "The wind picked up late in the evening.",
                 "The cafe was full by noon that day.", "The music next door was far too loud."),
}  # fmt: skip


def grid(k: int, f: int) -> int:
    """The cell of the k-th statement when the filler takes cell f."""
    return k + (k >= f)


def order(g: int, f: int) -> int | None:
    """The statement index in cell g (None: the filler's cell)."""
    return None if g == f else g - (g > f)


def slot_classes(rng: random.Random, n: int, n_ent: int) -> list[int]:
    """The base query's slot per scene: first, middle, last in equal thirds (seeded blocks), middle a random inner slot.
    At N = 3 first and last only: one filler cell shifts a statement by one cell, so the token-pointed statement is a
    neighbour of the order-pointed one, and with the query in the middle that neighbour is the query itself."""
    out: list[int] = []
    while len(out) < n:
        block = ["first", "middle", "last"] if n_ent > 3 else ["first", "last"]
        rng.shuffle(block)
        out += [0 if b == "first" else n_ent - 1 if b == "last" else rng.randrange(1, n_ent - 1) for b in block]
    return out[:n]


def layouts(a: int, n_ent: int, with_identity: bool) -> list[tuple[int, int, int, int, int | None]]:
    """Every (f_org, f_alt, k, k', c) valid for a base query at slot a: k != a; the alt's cell for its k-th statement
    is not the org filler's; k' (the org statement at that cell) differs from a and k; c (bridge alt's org slot) is a
    fourth slot, or None at N = 3 (bridge alt not in the org prompt)."""
    out = []
    for f_o in range(n_ent + 1):
        for f_a in range(n_ent + 1):
            if f_a == f_o:
                continue
            for k in range(n_ent):
                kp = order(grid(k, f_a), f_o)
                if k == a or kp is None or kp in (a, k):
                    continue
                if not with_identity:
                    out.append((f_o, f_a, k, kp, None))
                    continue
                out += [(f_o, f_a, k, kp, c) for c in range(n_ent) if c not in (a, k, kp)]
    return out


def pick(rng: random.Random, domain: str, n_ent: int) -> tuple[str, str, str, str, list[str]]:
    """q_b, q_s (recalled digits differ), the order-pointed and the token-pointed entities (recalled digits unlike both
    where the pool allows), and the rest (N = 5: one more; N = 3: none, bridge alt is not in the org prompt)."""
    pool = list(PV.DOMAINS[domain]["entities"])
    while True:
        q_b, q_s = rng.sample(pool, 2)
        if PV.rec(domain, q_b) != PV.rec(domain, q_s):
            break
    rest = [e for e in pool if e not in (q_b, q_s)]
    crit = (PV.rec(domain, q_b), PV.rec(domain, q_s))
    distinct = [e for e in rest if PV.rec(domain, e) not in crit]
    p_ord = rng.choice(distinct or rest)
    rest = [e for e in rest if e != p_ord]
    distinct = [e for e in rest if PV.rec(domain, e) not in (*crit, PV.rec(domain, p_ord))]
    p_tok = rng.choice(distinct or rest)
    rest = [e for e in rest if e != p_tok]
    more = rng.sample(rest, n_ent - 4) if n_ent >= 5 else []
    return q_b, q_s, p_ord, p_tok, more


def context(domain: str, ents: list[str], digits: list[int], filler: str, f: int) -> str:
    st = [PV.DOMAINS[domain]["statement"].format(e=e, d=d) for e, d in zip(ents, digits, strict=True)]
    st.insert(f, filler)
    return " ".join(st)


def make_scene(rng: random.Random, domain: str, n_ent: int, a: int) -> dict[str, Any]:
    with_id = n_ent >= 5
    f_o, f_a, k, kp, c = rng.choice(layouts(a, n_ent, with_id))
    q_b, q_s, p_ord, p_tok, more = pick(rng, domain, n_ent)
    ents: list[str] = [""] * n_ent
    ents[a], ents[k], ents[kp] = q_b, p_ord, p_tok
    if c is not None:
        ents[c] = q_s
    for s, e in zip([s for s in range(n_ent) if not ents[s]], rng.sample(more, len(more)), strict=True):
        ents[s] = e
    recalled = {e: PV.rec(domain, e) for e in {*ents, q_s}}
    crit = {recalled[e] for e in (q_b, q_s, p_ord, p_tok)}
    soft = [d for d in DIGITS if d not in set(recalled.values())]
    pool, policy = (soft, "soft") if len(soft) >= n_ent + 1 else ([d for d in DIGITS if d not in crit], "hard")
    digits = rng.sample(pool, n_ent)
    value = rng.choice([d for d in pool if d not in digits])
    # the alt prompt: q_s as its k-th statement; the others (N = 5: the org entities but q_s; N = 3: two of the three)
    others = [e for e in ents if e != q_s]
    others = rng.sample(others, n_ent - 1)
    alt = list(others)
    alt.insert(k, q_s)
    alt_rest = rng.sample([d for d in pool if d != value], n_ent - 1)
    ref_digit = digits[kp]
    ref_rest = rng.sample([d for d in pool if d != ref_digit], n_ent - 1)
    while True:  # the 'same' control: q_b in its slot with its digit, the rest reshuffled and redigited
        m_ents = rng.sample([e for e in ents if e != q_b], n_ent - 1)
        m_ents.insert(a, q_b)
        m_digits = rng.sample([d for d in pool if d != digits[a]], n_ent - 1)
        m_digits.insert(a, digits[a])
        if m_ents != ents:
            break
    filler = rng.choice(FILLER[domain])
    return {
        "q_b": q_b, "q_s": q_s, "p_ord": p_ord, "p_tok": p_tok, "ents": ents, "digits": digits, "value": value,
        "a": a, "c": c, "k": k, "kp": kp, "f_org": f_o, "f_alt": f_a, "filler": filler, "policy": policy,
        "recalled": recalled, "alt": alt, "alt_digits": {"off": [*alt_rest[:k], value, *alt_rest[k:]],
                                                          "pln": [*alt_rest[:k], value, *alt_rest[k:]],
                                                          "ref": [*ref_rest[:k], ref_digit, *ref_rest[k:]]},
        "same": (m_ents, m_digits),
    }  # fmt: skip


def items_for(sc: dict[str, Any], domain: str, n_ent: int, i: int) -> dict[tuple[str, str], dict]:
    """(family, type) -> item."""
    d = PV.DOMAINS[domain]
    q_b, q_s = sc["q_b"], sc["q_s"]
    ents, digits = sc["ents"], sc["digits"]
    look = dict(zip(ents, digits, strict=True))
    base_ctx = context(domain, ents, digits, sc["filler"], sc["f_org"])
    out = {}
    for fam in FAMILIES:
        lookup = fam != "RR"
        if fam == "DL":
            question, alt_q = d["DL"].format(e=q_b), d["DL"].format(e=q_s)
        else:
            question, alt_q = d[fam].format(cue=PV.cue(domain, q_b)), d[fam].format(cue=PV.cue(domain, q_s))
        answer = look[q_b] if lookup else PV.rec(domain, q_b)
        rec = sc["recalled"]
        m_ents, m_digits = sc["same"]
        r_digits = list(digits)
        r_digits[sc["a"]] = sc["value"]
        for typ in TYPES:
            level = f"e{n_ent}-{typ}"
            f_alt = sc["f_alt"] if typ == "off" else sc["f_org"]
            alt_digits = sc["alt_digits"][typ]
            alt_look = dict(zip(sc["alt"], alt_digits, strict=True))
            if lookup:
                pred = {"none": look[q_b], "identity": look.get(q_s, "-"), "position": digits[sc["k"]]}
                if typ == "off":
                    pred["token"] = digits[sc["kp"]]
                pred["value"] = alt_look[q_s]
            else:
                pred = {"none": rec[q_b], "identity": rec[q_s], "position": rec[ents[sc["k"]]]}
                if typ == "off":
                    pred["token"] = rec[ents[sc["kp"]]]
                pred["value"] = rec[q_s]
            pred_s = {h: str(v) for h, v in pred.items()}
            keys = [h for h in pred_s if pred_s[h] != "-" and not (fam == "RR" and h == "value")]
            sources = {
                "dissoc": {"context": context(domain, sc["alt"], alt_digits, sc["filler"], f_alt), "question": alt_q,
                           "answer": str(alt_look[q_s] if lookup else rec[q_s]), "entities": sc["alt"],
                           "digits": alt_digits, "query": q_s, "query_slot": sc["k"], "filler_cell": f_alt,
                           "predictions": pred_s},
                "same": {"context": context(domain, m_ents, m_digits, sc["filler"], sc["f_org"]), "question": question,
                         "answer": str(answer), "entities": m_ents, "digits": m_digits, "query": q_b,
                         "query_slot": sc["a"], "filler_cell": sc["f_org"],
                         "predictions": {h: str(answer) for h in pred_s}},
                "redigit": {"context": context(domain, ents, r_digits, sc["filler"], sc["f_org"]), "question": question,
                            "answer": str(sc["value"] if lookup else answer), "entities": ents, "digits": r_digits,
                            "query": q_b, "query_slot": sc["a"], "filler_cell": sc["f_org"],
                            "predictions": {h: str(answer) for h in pred_s} | ({"value": str(sc["value"])} if lookup else {})},
            }  # fmt: skip
            slots = {"query": sc["a"], "identity": sc["c"], "position": sc["k"], "token": sc["kp"] if typ == "off" else None,
                     "value_in_org": sc["kp"] if typ == "ref" else None}  # fmt: skip
            item = {
                "id": f"{domain}-{fam}-{level}-{i:04d}", "family": fam, "domain": domain, "level": level, "type": typ,
                "scene": f"{domain}-e{n_ent}-{i:04d}", "n_entities": n_ent, "n_filler": 1, "filler_cell": sc["f_org"],
                "entities": ents, "digits": digits, "recalled": rec, "query": q_b,
                "cue": q_b if fam == "DL" else PV.cue(domain, q_b), "slots": slots,
                "context": base_ctx, "question": question, "answer": str(answer), "answer_kind": "digit",
                "sources": sources, "distinct": len({pred_s[h] for h in keys}) == len(keys),
                "digit_policy": sc["policy"], "collisions": sorted({x for x in digits if x in rec.values()}),
            }  # fmt: skip
            if fam != "DL":
                item["hop1"] = {"question": d["hop_cue"].format(cue=PV.cue(domain, q_b)), "answer": q_b, "kind": domain}
                hop2 = d["DL"].format(e=q_b) if lookup else d["hop_recall"].format(e=q_b)
                item["hop2"] = {"question": hop2, "answer": str(answer), "kind": "digit"}
            out[(fam, typ)] = item
    return out


def generate(which: str) -> dict[str, tuple[Path, list[dict], str]]:
    spec = SETS[which]
    n_ent = spec["n_ent"]
    out: dict[str, tuple[Path, list[dict], str]] = {}
    for di, domain in enumerate(DOMAINS):
        seed = spec["seed"] * 100 + di
        rng = random.Random(seed)
        plan = slot_classes(rng, spec["n"], n_ent)
        cells: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
        seen: set[str] = set()
        i = 0
        while i < spec["n"]:
            sc = make_scene(rng, domain, n_ent, plan[i])
            key = context(domain, sc["ents"], sc["digits"], sc["filler"], sc["f_org"])
            if key in seen:
                continue
            seen.add(key)
            for ft, item in items_for(sc, domain, n_ent, i).items():
                cells[ft].append(item)
            i += 1
        note = f"scripts/pointer_v2.py make --set {which} (seed {seed}: {domain}, {n_ent} statements + 1 filler)"
        for (fam, typ), items in cells.items():
            label = f"{domain}_{fam}_e{n_ent}-{typ}"
            out[label] = (DATA / which / f"{label}.json", items, note)
    return out


def set_files(which: str) -> dict[str, Path]:
    n_ent = SETS[which]["n_ent"]
    return {
        f"{d}_{f}_e{n_ent}-{t}": DATA / which / f"{d}_{f}_e{n_ent}-{t}.json"
        for d in DOMAINS
        for f in FAMILIES
        for t in TYPES
    }


TYPE_NAME = {
    "off": "the filler sentence in another place in the alt prompt (order and token position split)",
    "pln": "the filler sentence in the same place in both prompts",
    "ref": "the alt prompt's answer also in the org prompt",
}


def level_name(level: str) -> str:
    """'e5-off' -> '5 statements + 1 filler, ...' (pointer_swap's figure titles)."""
    base, _, typ = level.partition("-")
    return f"{base[1:]} statements + 1 filler, {TYPE_NAME[typ]}"


# ---- checks (tokenizer only) ----------------------------------------------------------------------------------------


def check_filler(tok) -> None:
    for domain, pool in FILLER.items():
        n = len(
            S.ids(tok, " " + PV.DOMAINS[domain]["statement"].format(e=next(iter(PV.DOMAINS[domain]["entities"])), d=5))
        )
        for s in pool:
            assert len(S.ids(tok, s)) == n == len(S.ids(tok, " " + s)), f"{domain}: filler {s!r} is not {n} tokens"


def cells_of(tok, item: dict, ctx: str, question: str) -> tuple[list[int], list[int], tuple[int, int]]:
    """ids, each context sentence's first token index (statements and filler in text order), the question's span."""
    from bridge_jspace.tokens import raw_encoding

    text = S.render(tok, ctx, question)
    enc = raw_encoding(tok, text, offsets=True)
    offs = enc["offset_mapping"]
    start = text.index(ctx)
    sents, pos = [], start
    for sent in ctx.split(". "):
        sent = sent if sent.endswith(".") else sent + "."
        j = text.index(sent, pos)
        sents.append(PV.token_index(offs, j))
        pos = j + len(sent)
    q0 = text.rindex("\n" + question) + 1
    return list(enc["input_ids"]), sents, (PV.token_index(offs, q0), PV.token_index(offs, q0 + len(question) - 1))


def check_item(tok, item: dict) -> dict[str, bool]:
    ids, starts, q = cells_of(tok, item, item["context"], item["question"])
    width = {starts[i + 1] - starts[i] for i in range(len(starts) - 1)}
    out = {"equal_cells": len(width) == 1}
    for src, s in item["sources"].items():
        s_ids, s_starts, s_q = cells_of(tok, item, s["context"], s["question"])
        diff = S.changed(ids, s_ids) if len(ids) == len(s_ids) else None
        out[f"{src}_aligned"] = bool(diff) and s_starts == starts and s_q == q
    pd = item["sources"]["dissoc"]["predictions"]
    sl, ents, dg = item["slots"], item["entities"], item["digits"]
    lookup = item["family"] != "RR"
    alt = item["sources"]["dissoc"]
    f_o, f_a = item["filler_cell"], alt["filler_cell"]
    k = sl["position"]
    ok = alt["entities"][k] == alt["query"] and ents[sl["query"]] == item["query"]
    if lookup:
        ok = ok and pd["position"] == str(dg[k]) and pd["none"] == str(dg[sl["query"]])
        if item["type"] == "off":
            kp = order(grid(k, f_a), f_o)
            assert kp is not None, f"{item['id']}: the alt statement sits in the org filler's cell"
            ok = ok and kp == sl["token"] and pd["token"] == str(dg[kp]) and kp != k and f_a != f_o
            # the token offsets: the alt's k-th statement starts where the org's k'-th does
            a_starts = cells_of(tok, item, alt["context"], alt["question"])[1]
            ok = ok and a_starts[grid(k, f_a)] == starts[grid(kp, f_o)]
        if item["type"] == "ref":
            ok = ok and pd["value"] == str(dg[sl["value_in_org"]])
        else:
            ok = ok and int(pd["value"]) not in dg
        if item["n_entities"] >= 5:
            ok = ok and pd["identity"] == str(dg[ents.index(alt["query"])])
        else:
            ok = ok and pd["identity"] == "-" and alt["query"] not in ents
    keys = [h for h, x in pd.items() if x != "-" and not (not lookup and h == "value")]
    out["permutation"] = ok
    out["predictions_distinct"] = len({pd[h] for h in keys}) == len(keys) if lookup else pd["none"] != pd["identity"]
    crit = {item["recalled"][e] for e in (item["query"], alt["query"], ents[k])}
    if item["type"] == "off":
        crit.add(item["recalled"][ents[sl["token"]]])
    out["hard_collision_free"] = not (set(dg) & crit) and not (set(alt["digits"]) & crit)
    return out


def stage_make(which: str) -> None:
    tok = PV.tokenizer()
    check_filler(tok)
    for _label, (path, items, note) in generate(which).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        assert not path.exists(), f"{path} exists; data files are written once"
        head = {"family": items[0]["family"], "domain": items[0]["domain"], "level": items[0]["level"],
                "generator": note, "format": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
        body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)
        path.write_text(json.dumps(head, indent=1)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")
        print("wrote", path, len(items))


def stage_verify() -> None:
    for which in SETS:
        for label, (path, items, _) in generate(which).items():
            if not path.exists():
                print(which, label, "no file yet")
                continue
            same = PV.load_file(path) == items
            print(which, label, "same" if same else "DIFFERENT")
            assert same, f"{label}: the generator no longer reproduces {path}"


def stage_check(which: str) -> None:
    tok = PV.tokenizer()
    check_filler(tok)
    report: dict[str, Any] = {}
    for label, path in set_files(which).items():
        items = PV.load_file(path)
        stats: collections.Counter = collections.Counter()
        slot_class: collections.Counter = collections.Counter()
        for it in items:
            for k, v in check_item(tok, it).items():
                stats[k] += bool(v)
            a, n = it["slots"]["query"], it["n_entities"]
            slot_class["first" if a == 0 else "last" if a == n - 1 else "middle"] += 1
        n = len(items)
        report[label] = {"n": n, **stats, "slot_class": dict(slot_class),
                         "prompts_unique": len({it["context"] + it["question"] for it in items})}  # fmt: skip
        print(label, json.dumps(report[label]))
        must = [
            "equal_cells",
            "dissoc_aligned",
            "same_aligned",
            "redigit_aligned",
            "permutation",
            "hard_collision_free",
        ]
        for k in must:
            assert stats[k] == n, f"{label}: {k} {stats[k]}/{n}"
        if label.split("_")[1] != "RR":
            assert stats["predictions_distinct"] == n, f"{label}: predictions not distinct"
        assert report[label]["prompts_unique"] == n, label
    out = DATA / f"check_{which}.json"
    out.write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", out)


def stage_manifest(name: str, why: str, sets: list[str], limit: int | None) -> None:
    from bridge_jspace.data import sha256_of

    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    files = {f"{s}/{label}": f for s in sets for label, f in set_files(s).items()}
    m = {"exp": "pointer_v2", "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
         "model": pins.model_pin(), "switches": switches(), "sets": sets,
         "items": {k: {"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(f)} for k, f in files.items()},
         "limit": limit, "format": "pointer_v1's competence: base, each source, the steps alone; greedy and answer read",
         "eligibility": "pointer_swap uses items with every prompt right"}  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    PV.RESULTS = RESULTS  # pointer_v1's competence, reading this run's manifest and writing under results/pointer_v2
    PV.stage_competence(name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest", "competence"])
    ap.add_argument("--set", dest="sets", nargs="+", choices=list(SETS), default=["main"])
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    if args.stage == "make":
        for s in args.sets:
            stage_make(s)
    elif args.stage == "verify":
        stage_verify()
    elif args.stage == "check":
        for s in args.sets:
            stage_check(s)
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why, args.sets, args.limit)
    else:
        assert args.name, "competence needs --name"
        stage_competence(args.name)
