"""pointer_v4x (D3, 2026-10-21): pointer_v2's "filler moved" and pointer_v3's "one statement more / fewer" scenes, rebuilt
on pointer_v4's topics (countries, animals, body parts: 85 probe-passing entities), its 3 x 3 wordings and its held-out
split (data/pointer_v4/split.json). pointer_v2 and pointer_v3 had 22 entities and one wording, and their pre-registered
cells (tokens after the question, layers 44-52 together) read "alt answer" or "mixed" because the digit arrives by
layer 52; "order" and "counted from the start" rested on single layers. Here the same separations get ~4x the entities,
three wordings, entity-cluster intervals and a primary cell fixed on the last two tokens at layers 48 and 50.

Scene: pointer_v4's statements in one wording plus filler sentences of exactly that wording's statement length (8-12
tokens, checked by make/check), so every context is a grid of equal cells. Three types, separate scenes (levels):
  e5-off    pointer_v2's OFFSET SHIFT: org and alt prompts have one filler each, in different cells, so bridge alt keeps
            its ORDER index k in the alt prompt but sits at the token offset of the org's k'-th statement (k' != k).
            Predictions: none / identity (bridge alt's statement) / position (the org's k-th: order) / token (the org's
            k'-th: the same place in the text) / value (the alt prompt's answer, not in the org prompt).
  e5more    pointer_v3: the alt prompt has 6 statements (org 5 statements + 2 fillers, alt 6 + 1): the k-th from the
  e5fewer   start, the k-th from the end and the same token position name three different org statements.
            Predictions: none / identity / position (from the start) / end (from the end) / token / value.
Families: memory -> prompt (RL) and named -> prompt (DL); memory -> memory is not built (its predictions are recalled
facts, none of these pointers apply). Controls in the data: "same" (q_b in its slot with its digit, the rest reshuffled
and redigited, the org prompt's filler places) and "redigit". Digits 0-9; no org or alt digit equals the recalled digit
of q_b, q_s or the pointed-at entities where the pool allows (pointer_v2's soft/hard; pointer_v3's hard set).
Asked and alt entity: same cue token length (pointer_v4's pairs), so the alt prompts stay token-aligned. Cap: the
asked entity cycles through the askable pool in seeded rounds; at most 12 scenes per askable entity per (topic, type).
Each item records its wording and its cut against pointer_v4's held-out split (entity / wording / both / neither).

Sets: main, up to 150 scenes per (topic x type), seed 851. Files: data/pointer_v4x/main/<topic>_<family>_<level>.json.

Stages:  make | verify | check (tokenizer only) | manifest --name N --why W [--limit K] | competence --name N (GPU)
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.run_switches import switches
from scripts import pointer_v1 as PV
from scripts import pointer_v2 as P2
from scripts import pointer_v3 as P3
from scripts import pointer_v4 as P4
from scripts import suite_v1 as S

EXP = "pointer_v4x"
DATA = Path(os.environ.get("BJ_POINTER_V4X_DATA", str(pins.DATA_DIR / EXP)))
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES = ("RL", "DL")
DOMAINS = P4.DOMAINS  # pointer_v4's topics in use (split.json)
TYPES = ("off", "more", "fewer")
LEVELS = {"off": "e5-off", "more": "e5more", "fewer": "e5fewer"}
DIGITS = tuple(range(10))
N_ENT = 5
CAP = P4.CAP
SETS: dict[str, dict[str, Any]] = {"main": {"seed": 851, "n": 150}}
# A statement's token length per (topic, wording) on Qwen3.6-27B's tokenizer, with and without a leading space (the
# same for every entity and digit; make and check assert it), and filler sentences of each length: no digits, no
# entity of any topic, no drawer / cabinet / locker / folder words, no question words.
STMT_TOKENS = {"countries": (9, 8, 11), "animals": (8, 8, 10), "body": (9, 8, 12)}
FILLER = {
    8: P2.FILLER["animals"],
    9: (*P2.FILLER["elements"], "The hallway lights were dimmed early tonight.",
        "The meeting ran long and everyone left tired.", "The library closed early because of the holiday.",
        "The train stopped briefly at the small station.", "The rain stopped just before the parade began.",
        "The visitors waited patiently outside the main entrance."),
    10: ("The printer in the office jammed twice today.", "The garden gate squeaked whenever it was opened.",
         "The new curtains made the room feel much warmer.", "The bus was late again on the rainy afternoon.",
         "The ferry crossing was delayed by thick morning fog.", "The school choir practised every evening that month.",
         "The power went out briefly during the evening storm.", "The carpet in the hallway was replaced last spring.",
         "The weekend market opened an hour later than usual."),
    11: ("The kettle whistled loudly in the empty kitchen.", "The festival drew a large crowd to the old square.",
         "The museum added a new wing over the summer months.", "The bakery sold out of bread before the lunch hour.",
         "The streetlights came on a little earlier than usual.", "The parcel arrived a day later than had been promised.",
         "The noise from the road kept everyone awake that night.", "The tea had gone cold by the time anyone noticed.",
         "The sky cleared slowly after a long and grey morning.", "The old mill was turned into a small concert hall.",
         "The staff room was tidied up before the inspection.", "The workmen finished the roof just before the storm."),
    12: ("The neighbours repainted their fence a pale shade of green.", "The office lift was out of order for the whole week.",
         "The window cleaner came by on a bright and windy morning.", "The garden hose was left out in the sun all day.",
         "The heating came on as soon as the evening turned cold.", "The new bench by the pond was painted a deep blue.",
         "The station clock had stopped at some point in the night.", "The cafe changed its menu at the start of the season.",
         "The quiz night at the pub was cancelled at short notice.", "The roads were gritted early ahead of the cold snap."),
}  # fmt: skip


def fillers_for(domain: str, t: int) -> tuple[str, ...]:
    return FILLER[STMT_TOKENS[domain][t]]


def context(domain: str, t: int, ents: list[str], digits: list[int], fill: list[str], cells: tuple[int, ...]) -> str:
    """Statements in order with the filler sentences in the given cells (the first filler cell gets fill[0], ...)."""
    st = iter(P4.statements(domain, t, ents, digits))
    fl = iter(fill)
    return " ".join(next(fl) if g in cells else next(st) for g in range(len(ents) + len(cells)))


def slot_plan(rng: random.Random, n: int, typ: str) -> list[int]:
    """The base query's slot: first / middle / last in seeded blocks, among the slots the type's layouts allow."""
    ok = [a for a in range(N_ENT) if (P2.layouts(a, N_ENT, True) if typ == "off" else P3.layouts(typ, a))]
    classes = {"first": [a for a in ok if a == 0], "last": [a for a in ok if a == N_ENT - 1],
               "middle": [a for a in ok if 0 < a < N_ENT - 1]}  # fmt: skip
    names = [c for c, v in classes.items() if v]
    out: list[int] = []
    while len(out) < n:
        block = list(names)
        rng.shuffle(block)
        out += [rng.choice(classes[b]) for b in block]
    return out[:n]


def same_control(rng: random.Random, ents: list[str], digits: list[int], a: int, pool: list[int]) -> tuple[list, list]:
    while True:  # q_b in its slot with its digit, the rest reshuffled and redigited
        m_ents = rng.sample([e for e in ents if e != ents[a]], N_ENT - 1)
        m_ents.insert(a, ents[a])
        m_digits = rng.sample([d for d in pool if d != digits[a]], N_ENT - 1)
        m_digits.insert(a, digits[a])
        if m_ents != ents:
            return m_ents, m_digits


def scene_off(rng: random.Random, domain: str, pool: list[str], q_b: str, a: int, cue_len: dict, t: int) -> dict:
    """pointer_v2's offset shift (one filler, another cell in the alt prompt) with pointer_v4's entities."""
    f_o, f_a, k, kp, c = rng.choice(P2.layouts(a, N_ENT, True))
    assert c is not None  # with_identity: bridge alt is in the org prompt
    q_s = rng.choice([e for e in pool if P4.pair_ok(domain, q_b, e, cue_len)])
    rest = [e for e in pool if e not in (q_b, q_s)]
    crit = (P4.rec(domain, q_b), P4.rec(domain, q_s))
    p_ord = rng.choice([e for e in rest if P4.rec(domain, e) not in crit] or rest)
    rest = [e for e in rest if e != p_ord]
    p_tok = rng.choice([e for e in rest if P4.rec(domain, e) not in (*crit, P4.rec(domain, p_ord))] or rest)
    more = rng.choice([e for e in rest if e != p_tok])
    ents: list[str] = [""] * N_ENT
    ents[a], ents[k], ents[kp], ents[c] = q_b, p_ord, p_tok, q_s
    ents[next(s for s in range(N_ENT) if not ents[s])] = more
    recalled = {e: P4.rec(domain, e) for e in ents}
    hard = {recalled[e] for e in (q_b, q_s, p_ord, p_tok)}
    soft = [d for d in DIGITS if d not in set(recalled.values())]
    dpool, policy = (soft, "soft") if len(soft) >= N_ENT + 1 else ([d for d in DIGITS if d not in hard], "hard")
    digits = rng.sample(dpool, N_ENT)
    value = rng.choice([d for d in dpool if d not in digits])
    alt = rng.sample([e for e in ents if e != q_s], N_ENT - 1)
    alt.insert(k, q_s)
    alt_digits = rng.sample([d for d in dpool if d != value], N_ENT - 1)
    alt_digits.insert(k, value)
    fill = [rng.choice(fillers_for(domain, t))]
    slots = {"query": a, "identity": c, "position": k, "token": kp}
    return {"ents": ents, "digits": digits, "value": value, "alt": alt, "alt_digits": alt_digits, "fill": fill,
            "f_org": (f_o,), "f_alt": (f_a,), "slots": slots, "k": k, "policy": policy, "recalled": recalled,
            "same": same_control(rng, ents, digits, a, dpool)}  # fmt: skip


def scene_more_fewer(rng: random.Random, domain: str, pool: list[str], typ: str, q_b: str, a: int, cue_len: dict,
                     t: int) -> dict:  # fmt: skip
    """pointer_v3's one statement more / fewer with pointer_v4's entities."""
    f_org, f_alt, k, (st, en, tk), c = rng.choice(P3.layouts(typ, a))
    q_s = rng.choice([e for e in pool if P4.pair_ok(domain, q_b, e, cue_len)])
    rest = rng.sample([e for e in pool if e not in (q_b, q_s)], N_ENT - 2)
    ents: list[str] = [""] * N_ENT
    ents[a], ents[c] = q_b, q_s
    for s, e in zip([s for s in range(N_ENT) if not ents[s]], rest, strict=True):
        ents[s] = e
    others = [e for e in ents if e != q_s]
    if typ == "more":
        others = rng.sample([*others, rng.choice([e for e in pool if e not in ents])], N_ENT)
    else:
        others = rng.sample(others, N_ENT - 2)
    alt = list(others)
    alt.insert(k, q_s)
    recalled = {e: P4.rec(domain, e) for e in {*ents, *alt}}
    hard = {recalled[e] for e in (q_b, q_s, ents[st], ents[en])}
    dpool = [d for d in DIGITS if d not in hard]
    digits = rng.sample(dpool, N_ENT)
    value = rng.choice([d for d in dpool if d not in digits])
    alt_digits = rng.sample([d for d in dpool if d != value], len(alt) - 1)
    alt_digits.insert(k, value)
    fill = rng.sample(fillers_for(domain, t), max(P3.FILLERS[typ]))
    slots = {"query": a, "identity": c, "position": st, "end": en, "token": tk}
    return {"ents": ents, "digits": digits, "value": value, "alt": alt, "alt_digits": alt_digits, "fill": fill,
            "f_org": f_org, "f_alt": f_alt, "slots": slots, "k": k, "policy": "hard", "recalled": recalled,
            "same": same_control(rng, ents, digits, a, dpool)}  # fmt: skip


def items_for(sc: dict, domain: str, typ: str, i: int, templates: tuple[int, int], held: set[str]) -> dict[str, dict]:
    spec = P4.SPEC[domain]
    t, u = templates
    ents, digits, sl = sc["ents"], sc["digits"], sc["slots"]
    q_b, q_s = ents[sl["query"]], ents[sl["identity"]]
    look = dict(zip(ents, digits, strict=True))
    alt_look = dict(zip(sc["alt"], sc["alt_digits"], strict=True))
    level = LEVELS[typ]
    m_ents, m_digits = sc["same"]
    r_digits = list(digits)
    r_digits[sl["query"]] = sc["value"]
    ent_out, tpl_out = q_b in held, P4.HELD_OUT_TEMPLATE in (t, u)

    def ctx(e: list[str], d: list[int], cells: tuple[int, ...]) -> str:
        return context(domain, t, e, d, sc["fill"], cells)

    out = {}
    for fam in FAMILIES:
        target = P4.name_of if fam == "DL" else P4.cue_of
        question, alt_q = (spec["lookups"][u].format(x=target(domain, e)) for e in (q_b, q_s))
        pred = {"none": look[q_b], "identity": look[q_s], "position": digits[sl["position"]]}
        if "end" in sl:
            pred["end"] = digits[sl["end"]]
        pred["token"] = digits[sl["token"]]
        pred["value"] = alt_look[q_s]
        pred_s = {h: str(v) for h, v in pred.items()}
        answer = str(look[q_b])

        def src(e: list[str], d: list[int], cells: tuple[int, ...], q: str, query: str, ans: str, preds: dict) -> dict:
            return {"context": ctx(e, d, cells), "statements": P4.statements(domain, t, e, d), "question": q,
                    "answer": ans, "entities": e, "digits": d, "query": query, "query_slot": e.index(query),
                    "filler_cells": list(cells), "predictions": preds}  # fmt: skip

        sources = {
            "dissoc": src(sc["alt"], sc["alt_digits"], sc["f_alt"], alt_q, q_s, str(alt_look[q_s]), pred_s),
            "same": src(m_ents, m_digits, sc["f_org"], question, q_b, answer, {h: answer for h in pred_s}),
            "redigit": src(ents, r_digits, sc["f_org"], question, q_b, str(sc["value"]),
                           {h: answer for h in pred_s} | {"value": str(sc["value"])}),
        }  # fmt: skip
        item = {
            "id": f"{domain}-{fam}-{level}-{i:04d}", "family": fam, "domain": domain, "level": level, "type": typ,
            "scene": f"{domain}-{level}-{i:04d}", "n_entities": N_ENT, "n_filler": len(sc["f_org"]),
            "filler_cells": list(sc["f_org"]), "entities": ents, "digits": digits, "recalled": sc["recalled"],
            "query": q_b, "cue": target(domain, q_b), "slots": sl, "context": ctx(ents, digits, sc["f_org"]),
            "statements": P4.statements(domain, t, ents, digits), "question": question, "answer": answer,
            "answer_kind": "digit", "sources": sources, "distinct": len(set(pred_s.values())) == len(pred_s),
            "digit_policy": sc["policy"], "collisions": sorted({x for x in digits if x in sc["recalled"].values()}),
            "templates": {"statement": t, "question": u}, "held_out_entity": ent_out, "held_out_template": tpl_out,
            "cut": "both" if ent_out and tpl_out else "entity" if ent_out else "template" if tpl_out else "neither",
        }  # fmt: skip
        if fam == "RL":
            item["hop1"] = {"question": spec["hop_cue"].format(c=spec["candidates"][q_b][1]), "answer": q_b,
                            "kind": domain}  # fmt: skip
            item["hop2"] = {"question": spec["lookups"][u].format(x=P4.name_of(domain, q_b)), "answer": answer,
                            "kind": "digit"}  # fmt: skip
        out[fam] = item
    return out


def generate(which: str, split: dict[str, Any]) -> dict[str, tuple[Path, list[dict], str]]:
    """label -> (file, items, generator note); tokenizer-free given pointer_v4's split.json."""
    spec = SETS[which]
    out: dict[str, tuple[Path, list[dict], str]] = {}
    for domain in split["used"]:
        info = split["domains"][domain]
        pool, cue_len = info["pool"], info["cue_tokens"]
        held = set(info["held_out_entities"])
        askable = [e for e in pool if any(P4.pair_ok(domain, e, f, cue_len) for f in pool)]
        n = min(spec["n"], CAP * len(askable))
        for ti, typ in enumerate(TYPES):
            seed = spec["seed"] * 100 + 10 * list(P4.SPEC).index(domain) + ti
            rng = random.Random(seed)
            plan = slot_plan(rng, n, typ)
            cells: dict[str, list[dict]] = collections.defaultdict(list)
            seen: set[str] = set()
            q_round: list[str] = []
            for i in range(n):
                if not q_round:  # the cap: the asked entity cycles through the askable pool
                    q_round = rng.sample(askable, len(askable))
                q_b = q_round.pop()
                for _ in range(50):  # contexts never repeat within a (topic, type)
                    templates = (rng.randrange(3), rng.randrange(3))
                    if typ == "off":
                        sc = scene_off(rng, domain, pool, q_b, plan[i], cue_len, templates[0])
                    else:
                        sc = scene_more_fewer(rng, domain, pool, typ, q_b, plan[i], cue_len, templates[0])
                    key = context(domain, templates[0], sc["ents"], sc["digits"], sc["fill"], sc["f_org"])
                    if key not in seen:
                        break
                else:
                    raise AssertionError(f"{domain} {typ}: no new scene for {q_b}")
                seen.add(key)
                for fam, item in items_for(sc, domain, typ, i, templates, held).items():
                    cells[fam].append(item)
            note = f"scripts/pointer_v4x.py make (set {which}, seed {seed}: {domain}, type {typ}, {len(askable)} asked)"
            for fam, items in cells.items():
                label = f"{domain}_{fam}_{LEVELS[typ]}"
                out[label] = (DATA / which / f"{label}.json", items, note)
    return out


def set_files(which: str) -> dict[str, Path]:
    return {f"{d}_{f}_{lv}": DATA / which / f"{d}_{f}_{lv}.json" for d in DOMAINS for f in FAMILIES
            for lv in LEVELS.values()}  # fmt: skip


def level_name(level: str) -> str:
    """pointer_swap's figure titles."""
    return {"e5-off": "5 statements + 1 filler, the filler in another place in the alt prompt (order and token split)",
            "e5more": "5 statements, the alt prompt has 6 (start, end and token split)",
            "e5fewer": "5 statements, the alt prompt has 4 (start, end and token split)"}[level]  # fmt: skip


# ---- checks (tokenizer only) ----------------------------------------------------------------------------------------


def check_lengths(tok) -> None:
    """Every statement (any entity, digit, wording) and every filler has its pinned token length, with and without a
    leading space."""
    for d in DOMAINS:
        for t, tmpl in enumerate(P4.SPEC[d]["statements"]):
            n = STMT_TOKENS[d][t]
            for e in DOMAINS[d]["entities"]:
                s = tmpl.format(e=e, d=7)
                assert len(S.ids(tok, s)) == n == len(S.ids(tok, " " + s)), f"{d} wording {t}: {s!r} is not {n} tokens"
    for n, pool in FILLER.items():
        for s in pool:
            assert len(S.ids(tok, s)) == n == len(S.ids(tok, " " + s)), f"filler {s!r} is not {n} tokens"
            assert not any(ch.isdigit() for ch in s), s


def check_item(tok, item: dict) -> dict[str, bool]:
    """Equal cells; every source token-aligned (same length, same question span, something changed); each pointer
    names the org statement the design says (order / start / end by index, token by the alt statement's offset)."""
    ids, starts, q = P2.cells_of(tok, item, item["context"], item["question"])
    out = {"equal_cells": len({starts[i + 1] - starts[i] for i in range(len(starts) - 1)}) == 1}
    alt = item["sources"]["dissoc"]
    for name, s in item["sources"].items():
        s_ids, _, s_q = P2.cells_of(tok, item, s["context"], s["question"])
        out[f"{name}_aligned"] = len(s_ids) == len(ids) and s_q == q and bool(S.changed(ids, s_ids))
    a_starts = P2.cells_of(tok, item, alt["context"], alt["question"])[1]
    org_cells = P3.stmt_cells(len(starts), tuple(item["filler_cells"]))
    alt_cells = P3.stmt_cells(len(a_starts), tuple(alt["filler_cells"]))
    sl, k, m = item["slots"], alt["query_slot"], len(alt["entities"])
    ok = sl["position"] == k and alt["entities"][k] == alt["query"] == item["entities"][sl["identity"]]
    ok = ok and a_starts[alt_cells[k]] == starts[org_cells[sl["token"]]] and sl["token"] != sl["position"]
    if "end" in sl:
        ok = ok and sl["end"] == N_ENT - 1 - (m - 1 - k) and len({sl["position"], sl["end"], sl["token"]}) == 3
    out["pointers"] = ok and len(set(sl.values())) == len(sl)
    pd, dg = alt["predictions"], item["digits"]
    out["predictions"] = (len(set(pd.values())) == len(pd) and int(pd["value"]) not in dg
                          and all(pd[h] == str(dg[sl[h]]) for h in ("position", "end", "token") if h in sl))  # fmt: skip
    out["statements"] = item["statements"] == P4.statements(item["domain"], item["templates"]["statement"],
                                                            item["entities"], item["digits"])  # fmt: skip
    return out


def write_set(path: Path, items: list[dict], note: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; data files are written once"
    head = {"family": items[0]["family"], "domain": items[0]["domain"], "level": items[0]["level"], "generator": note,
            "format": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)
    path.write_text(json.dumps(head, indent=1)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")


def stage_make() -> None:
    tok = PV.tokenizer()
    check_lengths(tok)
    split = P4.load_split()
    assert split, "pointer_v4's split.json is missing"
    for _label, (path, items, note) in generate("main", split).items():
        write_set(path, items, note)
        print("wrote", path, len(items))


def stage_verify() -> None:
    split = P4.load_split()
    assert split, "pointer_v4's split.json is missing"
    for label, (path, items, _) in generate("main", split).items():
        same = PV.load_file(path) == items
        print(label, "same" if same else "DIFFERENT")
        assert same, f"{label}: the generator no longer reproduces {path}"


def stage_check() -> None:
    tok = PV.tokenizer()
    check_lengths(tok)
    report: dict[str, Any] = {}
    for label, path in set_files("main").items():
        items = PV.load_file(path)
        stats: collections.Counter = collections.Counter()
        for it in items:
            for k, v in check_item(tok, it).items():
                stats[k] += bool(v)
        n = len(items)
        asked = collections.Counter(it["query"] for it in items)
        report[label] = {
            "n": n, **stats, "entities_asked": len(asked), "max_asked": max(asked.values()),
            "slot_class": dict(collections.Counter(slot_class(it) for it in items)),
            "wordings": len({(it["templates"]["statement"], it["templates"]["question"]) for it in items}),
            "cuts": dict(collections.Counter(it["cut"] for it in items)),
            "prompts_unique": len({it["context"] + it["question"] for it in items}),
        }  # fmt: skip
        print(label, json.dumps(report[label]))
        for k in ("equal_cells", "dissoc_aligned", "same_aligned", "redigit_aligned", "pointers", "predictions",
                  "statements"):  # fmt: skip
            assert stats[k] == n, f"{label}: {k} {stats[k]}/{n}"
        assert report[label]["max_asked"] <= CAP, f"{label}: an entity is asked more than {CAP} times"
        assert report[label]["prompts_unique"] == n, label
    out = DATA / "check_main.json"
    out.write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", out)


def slot_class(item: dict) -> str:
    """pointer_swap's slot classes of the base query."""
    a = item["slots"]["query"]
    return "first" if a == 0 else "last" if a == N_ENT - 1 else "middle"


def stage_manifest(name: str, why: str, limit: int | None) -> None:
    from bridge_jspace.data import sha256_of

    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    root = pins.REPO_ROOT
    files = {f"main/{label}": f for label, f in set_files("main").items()}
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
         "model": pins.model_pin(), "switches": switches(), "sets": ["main"],
         "items": {k: {"file": str(f.relative_to(root)) if f.is_relative_to(root) else str(f), "sha256": sha256_of(f)}
                   for k, f in files.items()},
         "limit": limit, "format": f"pointer_v1's: {chat.format_note()}", "judge_mode": PV.judge_mode(), "judge": f"pointer_v1's: {PV.judge_rule()}",
         "prompts": "base; each source (dissoc, same, redigit); hop1 and hop2 for memory -> prompt",
         "eligibility": "pointer_swap uses items with every prompt right"}  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    PV.RESULTS = RESULTS  # pointer_v1's competence with pointer_v4's judge (its topics are pointer_v4's)
    PV.said = P4.said
    PV.stage_competence(name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest", "competence"])
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    if args.stage == "make":
        stage_make()
    elif args.stage == "verify":
        stage_verify()
    elif args.stage == "check":
        stage_check()
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why, args.limit)
    else:
        assert args.name, "competence needs --name"
        stage_competence(args.name)
