"""alias_pointer_v1: pointer_v1's scenes with the statements written in another surface form (Dan's D3, 2026-10-21).
When a recalled bridge feeds an in-prompt lookup, does the lookup find the bridge's statement by the word (the token
the model recalls, "cow") or by meaning (any surface form of the same entity: "Kuh", "perro", "O")?

Background (UNVERIFIED): pointer_v1 / pointer_swap test what the question tokens carry in transit (the bridge's
identity, a pointer to its statement's position, or the looked-up value) by patching from a source prompt with
reordered statements. There every statement names the entity with the very token the model recalls ("The cow's locker
is 5." ... "Which locker belongs to the animal known for mooing?"), so a lexical key match (the token "cow" found again
in the context) and a match by meaning cannot be told apart. The J-lens reads the recalled word but cannot steer the
lookup (read_write); if the lookup works, and a patch still carries identity, when the statement names the entity in
another language or by an alias, the "around" route is not a lexical pointer to the token "cow".

Conditions (the statements' surface form; the question, the instruction and the chat template stay English):
  same   statements in English, pointer_v1's template ("The cow's locker is 5."): the in-run baseline
  xlang  statements in French, Spanish or German: one fixed language per entity (one where its name is one token),
         one template per language, all three 9 tokens whatever the article's gender: "Le cheval a le casier 5." /
         "El perro tiene la taquilla 5." / "Die Kuh hat den Spind 5." (animals; a scene mixes languages)
  syn    statements with an alias in the English template: the chemical symbol ("The O card is in locker 5.";
         elements)
Pools (written below, each choice commented): animals = the 8 of pointer_v1's 16 with a one-token French, Spanish or
German name that is not the English word; elements = pointer_v1's 6 with their symbols. Not built: animals x syn (only
kitty and hog are clean one-token synonyms; hen, mare, sow, ram, lamb are hyponyms, canine and cattle a hypernym and a
mass noun, hound, pooch, steed, swine 2 tokens), elements x xlang (only carbon has a one-token French / Spanish name,
French "lithium" is the English word, every German name is 2-3 tokens).

Scenes, families, sources, predictions: pointer_v1's (see its docstring), on these pools. N entities bound to digits;
families RL ("Which locker belongs to the animal known for mooing?"), DL ("... to the cow?": the entity named in
English) and RR ("How many legs does the animal known for mooing have?"; the contrast) on the same scenes; sources
dissoc / same / redigit, token-aligned with the base, with four distinct predictions for lookups (none, identity,
position, value; RR: none != identity); pointer_v1's digit-collision policy and slot balance. Each scene is generated
once and written in each of its domain's conditions, so the items of one scene differ across conditions only in the
statements' text: entities, digits, order, questions, answers, sources and predictions are identical (paired by scene).

Extra item fields (pointer_v1's schema otherwise, key for key): condition; surface (entity -> the word its statement
uses); language (entity -> en / fr / es / de); statements (in slot order; each source has its own); spans (char offsets
[start, end) in the user turn `context + "\\n" + question + " " + instruction`, which S.render wraps in the chat
template: statements in slot order, filler, question, tail = the instruction; in the rendered prompt the tail runs on
to the end: end of turn, assistant header, empty think block, "Answer:"; `rendered_spans` maps them); alias (RL and DL
in xlang / syn: the surface form alone, "Which animal is called « Kuh » in German? Answer in English." -> cow;
"What is the name of the element with the chemical symbol O?" -> oxygen). Levels carry the
condition, so pointer_swap's per-level cells and its "vs e5f0" contrasts are per condition against the English
baseline: e5f0 = same, e5f0-xlang, e5f0-syn (dev: e3f0 likewise).

Sets (each (set, level, domain) has its own seed; the conditions of a scene share it):
  main  N = 5, no filler, 400 scenes per (domain, condition, family), seed 711
  dev   pilot, never a headline: N = 3 and N = 5, no filler, 60 scenes per cell, seed 712
Files: data/alias_pointer_v1/<set>/<domain>_<family>_<level>.json, one item per line.

Gate (competence; fixed before any 27B run, jobs/d3/alias_competence_27b.yaml): an alias condition enters the patching
runs iff, in its domain on main (400 scenes per file), the base prompt's Wilson 95% lower bound is >= 0.80 in both
lookup families (RL and DL), the English baseline passes pointer_v1's rule (lower bound >= 0.85) in the same cells,
and at least 35 scenes are eligible (every prompt of every family right, in both conditions; 35 is the n at which a
control with no change can have a Wilson upper bound <= 0.10, as pointer_swap's rule asks).

Stages:  make --set S (write-once; tokenizer only)   verify (regenerates every set, must equal its files)
         check --set S (tokenizer only: pools, alignment, predictions, collisions, spans, conditions paired)
         manifest --set S [S ...] --name N --why W [--limit K]
         competence --name N (GPU; this script's own: pointer_v1's reads only its own files and has no alias step)
         examples --name N [--k 3] [--seed 0]     figures --name N (a new analysis-<stamp>-figures/ folder)
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

from bridge_jspace import pins
from bridge_jspace.run_switches import check_switches, switches
from scripts import pointer_v1 as PV
from scripts import suite_v1 as S

EXP = "alias_pointer_v1"
DATA = pins.DATA_DIR / EXP
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES, SOURCES, HYPOTHESES, DIGITS = PV.FAMILIES, PV.SOURCES, PV.HYPOTHESES, PV.DIGITS
CONDITIONS = ("same", "xlang", "syn")
SUFFIX = {"same": "", "xlang": "-xlang", "syn": "-syn"}
COND_NAME = {  # plain names for tables and figures (Dan, 2026-10-21)
    "same": "statements in English",
    "xlang": "statements in French/Spanish/German",
    "syn": "statements with the chemical symbol",
}
SETS: dict[str, dict[str, Any]] = {
    "main": {"seed": 711, "n": 400, "levels": {"e5f0": (5, 0)}},
    "dev": {"seed": 712, "n": 60, "levels": {"e3f0": (3, 0), "e5f0": (5, 0)}},
}
LANG_NAME = {"en": "English", "fr": "French", "es": "Spanish", "de": "German"}
INSTRUCTION = S.INSTRUCTION

# ---- pools ----------------------------------------------------------------------------------------------------------
# xlang: entity -> (language, article, word). The word is one token after a space in Qwen3.6-27B's tokenizer (make and
# check assert it); among the languages where it is, the choice prefers a word that is neither an English word nor a
# close cognate, and keeps the languages near balanced (3 Spanish, 3 French, 2 German). Article: nominative singular,
# one token at the context's start and after a space. Dropped (no one-token name, or the English word itself): frog
# (grenouille, rana, Frosch), wolf (loup, lobo; German "Wolf"), sheep (mouton, oveja, Schaf), lion (French "lion"; leon,
# Löwe), goose (oie, ganso, Gans), turkey (dinde, pavo, Truthahn), bee (abeille, abeja, Biene), spider (araignée, araña,
# Spinne). French vowel-initial nouns would also need an elided article (l'oie).
XLANG: dict[str, tuple[str, str, str]] = {
    "dog": ("es", "El", "perro"),  # chien (fr) and Hund (de) are one token too; Hund is a cognate of "hound"
    "cat": ("es", "El", "gato"),  # French "chat" is one token but it is the English word "chat"; Katze 2 tokens
    "chicken": ("es", "El", "pollo"),  # the chicken (bird and meat); poulet (fr) one token too; gallina, poule 2 tokens
    "horse": ("fr", "Le", "cheval"),  # caballo (es) and Pferd (de) one token too
    "mouse": ("fr", "La", "souris"),  # German "Maus" is one token but a near-spelling of "mouse"; ratón 2 tokens
    "pig": ("fr", "Le", "porc"),  # the only one-token name (cochon, cerdo, Schwein: 2); a cognate of "pork"
    "cow": ("de", "Die", "Kuh"),  # the only one-token name (vache, vaca: 2)
    "duck": ("de", "Die", "Ente"),  # the only one-token name (canard, pato: 2)
}
# One template per language, "<article> <word> has locker <d>.": the possessor as subject keeps every statement at 9
# tokens whatever the gender ("Le casier de la vache" / "du cheval", "de la vaca" / "del perro" differ in length).
# Locker: casier (fr), taquilla (es; "casillero" is 3 tokens and would break the equal length), Spind (de).
XLANG_TEMPLATE = {
    "fr": "{art} {w} a le casier {d}.",
    "es": "{art} {w} tiene la taquilla {d}.",
    "de": "{art} {w} hat den Spind {d}.",
}
# syn (elements): the chemical symbol, an exact alias (names one element, no hypernym), one token after a space.
SYMBOLS = {"hydrogen": "H", "helium": "He", "lithium": "Li", "carbon": "C", "nitrogen": "N", "oxygen": "O"}
DOMAINS: dict[str, dict[str, Any]] = {
    "animals": {
        **PV.DOMAINS["animals"],
        "entities": {a: PV.ANIMALS[a] for a in XLANG},  # legs and pointer_v1's cues
        "conditions": ("same", "xlang"),
        "alias_q": {"xlang": "Which animal is called « {w} » in {lang}? Answer in English."},  # suite_v1's TRANS step
    },
    "elements": {
        **PV.DOMAINS["elements"],
        "conditions": ("same", "syn"),
        "alias_q": {"syn": "What is the name of the element with the chemical symbol {w}?"},
    },
}


def rec(domain: str, e: str) -> int:
    return DOMAINS[domain]["entities"][e][0]


def cue(domain: str, e: str) -> str:
    return DOMAINS[domain]["entities"][e][1]


def surface(cond: str, e: str) -> str:
    """The word a statement uses for entity e in a condition."""
    if cond == "xlang":
        return XLANG[e][2]
    if cond == "syn":
        return SYMBOLS[e]
    return e


def language(cond: str, e: str) -> str:
    return XLANG[e][0] if cond == "xlang" else "en"


def statement(domain: str, cond: str, e: str, d: int) -> str:
    if cond == "xlang":
        lang, art, w = XLANG[e]
        return XLANG_TEMPLATE[lang].format(art=art, w=w, d=d)
    return DOMAINS[domain]["statement"].format(e=surface(cond, e), d=d)


def alias_question(domain: str, cond: str, e: str) -> str:
    return DOMAINS[domain]["alias_q"][cond].format(w=surface(cond, e), lang=LANG_NAME[language(cond, e)])


def level_of(base: str, cond: str) -> str:
    return base + SUFFIX[cond]


def level_name(level: str) -> str:
    """'e5f0-xlang' -> '5 statements in French/Spanish/German' (for pointer_swap's figure titles)."""
    base, _, suffix = level.partition("-")
    n_ent, n_fill = int(base[1]), int(base[3:])
    cond = suffix or "same"
    return f"{n_ent} {COND_NAME[cond]}" + (f", {n_fill} filler sentences" if n_fill else "")


def user_turn(context: str, question: str) -> str:
    """The user turn S.render wraps in the chat template."""
    return f"{context}\n{question} {INSTRUCTION}"


# ---- scenes (pointer_v1's logic on this module's pools) --------------------------------------------------------------


def pick_entities(rng: random.Random, domain: str, n_ent: int) -> tuple[str, str, str, list[str]]:
    """q_b, q_s (recalled digits differ, so RR's none and identity differ), p (a recalled digit unlike both when the
    pool has one), and n_ent - 3 more. As pointer_v1.pick_entities."""
    pool = list(DOMAINS[domain]["entities"])
    while True:
        q_b, q_s = rng.sample(pool, 2)
        if rec(domain, q_b) != rec(domain, q_s):
            break
    rest = [e for e in pool if e not in (q_b, q_s)]
    distinct = [e for e in rest if rec(domain, e) not in (rec(domain, q_b), rec(domain, q_s))]
    p = rng.choice(distinct or rest)
    more = rng.sample([e for e in rest if e != p], n_ent - 3)
    return q_b, q_s, p, more


def digit_pool(domain: str, scene: list[str], critical: list[str], n_ent: int) -> tuple[list[int], str]:
    """pointer_v1's collision policy: soft (avoid every scene entity's recalled digit) where the pool allows, else hard
    (avoid q_b's, q_s's and p's)."""
    soft = [d for d in DIGITS if d not in {rec(domain, e) for e in scene}]
    if len(soft) >= n_ent + 1:
        return soft, "soft"
    hard = [d for d in DIGITS if d not in {rec(domain, e) for e in critical}]
    assert len(hard) >= n_ent + 1, f"{domain}: not enough lookup digits"
    return hard, "hard"


def make_scene(rng: random.Random, domain: str, n_ent: int, n_fill: int, a: int, k: int) -> dict[str, Any]:
    """One scene, as pointer_v1.make_scene: the base (order, digits), the dissoc / same / redigit sources, the layout."""
    q_b, q_s, p, more = pick_entities(rng, domain, n_ent)
    c = rng.choice([s for s in range(n_ent) if s not in (a, k)])
    order: list[str] = [""] * n_ent
    order[a], order[k], order[c] = q_b, p, q_s
    free = [s for s in range(n_ent) if not order[s]]
    for s, e in zip(free, rng.sample(more, len(more)), strict=True):
        order[s] = e
    pool, policy = digit_pool(domain, order, [q_b, q_s, p], n_ent)
    digits = rng.sample(pool, n_ent)
    value = rng.choice([d for d in pool if d not in digits])
    others = rng.sample([e for e in order if e != q_s], n_ent - 1)  # dissoc: q_s at slot k, the value its digit
    s_order = list(others)
    s_order.insert(k, q_s)
    s_digits = rng.sample([d for d in pool if d != value], n_ent - 1)
    s_digits.insert(k, value)
    while True:  # same: q_b at slot a with its digit; the others reshuffled (a different order) and redigited
        rest = rng.sample([e for e in order if e != q_b], n_ent - 1)
        m_order = list(rest)
        m_order.insert(a, q_b)
        m_digits = rng.sample([d for d in pool if d != digits[a]], n_ent - 1)
        m_digits.insert(a, digits[a])
        if m_order != order:
            break
    r_digits = list(digits)
    r_digits[a] = value
    lay = S.layout(rng, n_ent, n_fill, S.FILLER)
    return {
        "q_b": q_b, "q_s": q_s, "p": p, "slots": {"query": a, "identity": c, "position": k},
        "order": order, "digits": digits, "value": value, "policy": policy, "layout": lay,
        "dissoc": (s_order, s_digits), "same": (m_order, m_digits), "redigit": (list(order), r_digits),
    }  # fmt: skip


def build(domain: str, cond: str, order: list[str], digits: list[int], lay: list[int | str], question: str):
    """(context, statements in slot order, spans in the user turn) of one prompt."""
    facts = [statement(domain, cond, e, d) for e, d in zip(order, digits, strict=True)]
    parts = S.weave(facts, lay)
    context = " ".join(parts)
    st: list[list[int]] = [[] for _ in facts]
    fill: list[list[int]] = []
    pos = 0
    for x, text in zip(lay, parts, strict=True):
        if isinstance(x, int):
            st[x] = [pos, pos + len(text)]
        else:
            fill.append([pos, pos + len(text)])
        pos += len(text) + 1
    return context, facts, turn_spans(context, question, st, fill)


def turn_spans(context: str, question: str, statements: list[list[int]], filler: list[list[int]]) -> dict:
    """Spans in the user turn: the context's statements and filler, the question, the tail (the instruction)."""
    q0 = len(context) + 1
    q1 = q0 + len(question)
    return {"statements": statements, "filler": filler, "question": [q0, q1], "tail": [q1, q1 + 1 + len(INSTRUCTION)]}


def family_items(sc: dict[str, Any], domain: str, cond: str, scene_no: str, base: str, n_fill: int) -> dict[str, dict]:
    """The three families' items on one scene in one condition (pointer_v1.family_items plus the extra fields)."""
    d = DOMAINS[domain]
    level = level_of(base, cond)
    q_b, q_s, p = sc["q_b"], sc["q_s"], sc["p"]
    order, digits, lay = sc["order"], sc["digits"], sc["layout"]
    look = dict(zip(order, digits, strict=True))
    recalled = {e: rec(domain, e) for e in order}
    collisions = sorted({x for x in digits if x in recalled.values()})
    out = {}
    for fam in FAMILIES:
        if fam == "DL":
            question, src_question = d["DL"].format(e=q_b), d["DL"].format(e=q_s)
        else:
            question, src_question = d[fam].format(cue=cue(domain, q_b)), d[fam].format(cue=cue(domain, q_s))
        lookup = fam != "RR"
        answer = look[q_b] if lookup else rec(domain, q_b)
        sources = {}
        for src in SOURCES:
            s_order, s_digits = sc[src]
            s_look = dict(zip(s_order, s_digits, strict=True))
            if src == "dissoc":
                pred = (
                    {"none": look[q_b], "identity": look[q_s], "position": look[p], "value": s_look[q_s]}
                    if lookup
                    else {"none": rec(domain, q_b), "identity": rec(domain, q_s), "position": rec(domain, p),
                          "value": rec(domain, q_s)}
                )  # fmt: skip
                s_q, s_query = src_question, q_s
                s_answer = s_look[q_s] if lookup else rec(domain, q_s)
            else:
                s_q, s_query = question, q_b
                s_answer = s_look[q_b] if lookup else rec(domain, q_b)
                pred = {h: answer for h in HYPOTHESES}
                if src == "redigit" and lookup:
                    pred["value"] = s_look[q_b]
            s_ctx, s_st, s_spans = build(domain, cond, s_order, s_digits, lay, s_q)
            sources[src] = {
                "context": s_ctx, "question": s_q, "answer": str(s_answer), "entities": s_order, "digits": s_digits,
                "query": s_query, "query_slot": s_order.index(s_query),
                "predictions": {h: str(v) for h, v in pred.items()}, "statements": s_st, "spans": s_spans,
            }  # fmt: skip
        pd = sources["dissoc"]["predictions"]
        keys = HYPOTHESES if lookup else ("none", "identity", "position")
        ctx, st, spans = build(domain, cond, order, digits, lay, question)
        item = {
            "id": f"{domain}-{fam}-{level}-{scene_no}", "family": fam, "domain": domain, "level": level,
            "scene": f"{domain}-{base}-{scene_no}", "n_entities": len(order), "n_filler": n_fill,
            "entities": order, "digits": digits, "recalled": recalled, "query": q_b,
            "cue": q_b if fam == "DL" else cue(domain, q_b), "slots": sc["slots"],
            "context": ctx, "question": question, "answer": str(answer), "answer_kind": "digit",
            "sources": sources, "distinct": len({pd[h] for h in keys}) == len(keys),
            "digit_policy": sc["policy"], "collisions": collisions,
        }  # fmt: skip
        if fam != "DL":
            item["hop1"] = {"question": d["hop_cue"].format(cue=cue(domain, q_b)), "answer": q_b, "kind": domain}
            hop2 = d["DL"].format(e=q_b) if lookup else d["hop_recall"].format(e=q_b)
            item["hop2"] = {"question": hop2, "answer": str(answer), "kind": "digit"}
        item |= {
            "condition": cond, "surface": {e: surface(cond, e) for e in order},
            "language": {e: language(cond, e) for e in order}, "statements": st, "spans": spans,
        }  # fmt: skip
        if cond != "same" and lookup:
            item["alias"] = {"question": alias_question(domain, cond, q_b), "answer": q_b, "kind": domain}
        out[fam] = item
    return out


def generate_cell(
    seed: int, domain: str, base: str, n_ent: int, n_fill: int, n: int, tag: str = ""
) -> dict[str, dict[str, list]]:
    """n scenes of one domain at one level, each written in every condition of the domain and every family:
    condition -> family -> items. Contexts never repeat within the cell. Scene numbers are `tag` + 4 digits (the set's
    initial, so item ids are unique across sets)."""
    rng = random.Random(seed)
    plan = PV.slot_plan(rng, n, n_ent)
    conds = DOMAINS[domain]["conditions"]
    out: dict[str, dict[str, list[dict]]] = {c: {f: [] for f in FAMILIES} for c in conds}
    seen: set[str] = set()
    i = 0
    while i < n:
        a, k = plan[i]
        sc = make_scene(rng, domain, n_ent, n_fill, a, k)
        key = json.dumps([sc["order"], sc["digits"], sc["layout"]])
        if key in seen:
            continue
        seen.add(key)
        for c in conds:
            for fam, item in family_items(sc, domain, c, f"{tag}{i:04d}", base, n_fill).items():
                out[c][fam].append(item)
        i += 1
    return out


def cell_seed(which: str, base: str, domain: str) -> int:
    spec = SETS[which]
    return spec["seed"] * 1000 + 10 * list(spec["levels"]).index(base) + list(DOMAINS).index(domain)


def generate(which: str, n: int | None = None) -> dict[str, tuple[Path, list[dict], str]]:
    """label -> (file, items, generator note) for a set; tokenizer-free (make/check assert the token properties)."""
    spec = SETS[which]
    out = {}
    for base, (n_ent, n_fill) in spec["levels"].items():
        for domain in DOMAINS:
            seed = cell_seed(which, base, domain)
            cells = generate_cell(seed, domain, base, n_ent, n_fill, n or spec["n"], tag=which[0])
            note = f"scripts/{EXP}.py make --set {which} (seed {seed}: {domain}, {n_ent} entities, {n_fill} filler)"
            for cond, fams in cells.items():
                for fam, items in fams.items():
                    label = f"{domain}_{fam}_{level_of(base, cond)}"
                    out[label] = (DATA / which / f"{label}.json", items, note)
    return out


def set_files(which: str) -> dict[str, Path]:
    spec = SETS[which]
    return {
        f"{d}_{f}_{level_of(lv, c)}": DATA / which / f"{d}_{f}_{level_of(lv, c)}.json"
        for lv in spec["levels"]
        for d in DOMAINS
        for c in DOMAINS[d]["conditions"]
        for f in FAMILIES
    }


def load_file(path: Path) -> list[dict]:
    return json.loads(path.read_text())["items"]


# ---- tokenizer checks -----------------------------------------------------------------------------------------------


def tokenizer():
    """Qwen3.6-27B's tokenizer from the local cache (pointer_v1's loader: a tokenizer-only snapshot is enough)."""
    return PV.tokenizer()


def n_tokens(tok, text: str) -> int:
    return len(S.ids(tok, text))


def check_pools(tok) -> dict[str, Any]:
    """Entities and surface forms one token after a space; one cue length per domain (cues name no pool entity, digit
    or number word); per (domain, condition) every statement the same token count, at the context's start and after a
    space, for every entity and digit; aliases differ from the English word and from each other."""
    report: dict[str, Any] = {}
    words = set(PV.NUMBER_WORDS) | set(PV.ORDINALS)
    for domain, d in DOMAINS.items():
        ents = d["entities"]
        bad = [e for e in ents if n_tokens(tok, " " + e) != 1]
        assert not bad, f"{domain}: not one token: {bad}"
        lengths = {e: n_tokens(tok, " " + c) for e, (_, c) in ents.items()}
        assert len(set(lengths.values())) == 1, f"{domain}: cue lengths differ: {lengths}"
        for _, c in ents.values():
            toks = set(re.findall(r"[a-z]+|\d", c.lower()))
            assert not toks & {x.lower() for x in ents}, f"{domain}: cue {c!r} names a pool entity"
            assert not toks & words, f"{domain}: cue {c!r} has a number word"
            assert not re.search(r"\d", c), f"{domain}: cue {c!r} has a digit"
        report[domain] = {"entities": len(ents), "cue_tokens": next(iter(lengths.values())),
                          "recalled": sorted({r for r, _ in ents.values()}), "conditions": {}}  # fmt: skip
        for cond in d["conditions"]:
            forms = {e: surface(cond, e) for e in ents}
            bad = [w for w in forms.values() if n_tokens(tok, " " + w) != 1]
            assert not bad, f"{domain}/{cond}: surface forms not one token: {bad}"
            assert len(set(forms.values())) == len(forms), f"{domain}/{cond}: two entities share a surface form"
            if cond != "same":
                same = [e for e, w in forms.items() if w.lower() == e.lower()]
                assert not same, f"{domain}/{cond}: the alias is the English word: {same}"
                hit = [e for e, w in forms.items() if w.lower() in {x.lower() for x in ents}]
                assert not hit, f"{domain}/{cond}: an alias is another entity's English name: {hit}"
            if cond == "xlang":
                arts = {art for _, art, _ in XLANG.values()}
                bad = [a for a in arts if n_tokens(tok, a) != 1 or n_tokens(tok, " " + a) != 1]
                assert not bad, f"{domain}: articles not one token: {bad}"
            counts = collections.Counter()
            for e in ents:
                for dg in DIGITS:
                    s = statement(domain, cond, e, dg)
                    counts[(n_tokens(tok, s), n_tokens(tok, " " + s))] += 1
            assert len(counts) == 1, f"{domain}/{cond}: statement token counts differ: {dict(counts)}"
            (first, later), _ = counts.most_common(1)[0]
            report[domain]["conditions"][cond] = {
                "statement_tokens": later, "statement_tokens_at_start": first,
                "surface": forms if cond != "same" else "the English word",
                "languages": dict(collections.Counter(language(cond, e) for e in ents)),
            }  # fmt: skip
    return report


def rendered_spans(tok, ctx: str, question: str, spans: dict) -> tuple[str, dict[str, Any]]:
    """The rendered prompt and the spans moved into it (char offsets; the tail runs to the prompt's end)."""
    text = S.render(tok, ctx, question)
    off = text.index(user_turn(ctx, question))
    out = {
        "statements": [[off + s, off + e] for s, e in spans["statements"]],
        "filler": [[off + s, off + e] for s, e in spans["filler"]],
        "question": [off + spans["question"][0], off + spans["question"][1]],
        "tail": [off + spans["tail"][0], len(text)],
    }
    return text, out


def prompt_layout(tok, ctx: str, question: str, statements: list[str], spans: dict) -> dict[str, Any]:
    """ids, each statement's first and last token, the question's tokens, and whether the recorded spans decode."""
    from bridge_jspace.tokens import raw_encoding

    text, rs = rendered_spans(tok, ctx, question, spans)
    enc = raw_encoding(tok, text, offsets=True)
    ids, offs = list(enc["input_ids"]), enc["offset_mapping"]
    starts = [PV.token_index(offs, s) for s, _ in rs["statements"]]
    ends = [PV.token_index(offs, e - 1) for _, e in rs["statements"]]
    q = (PV.token_index(offs, rs["question"][0]), PV.token_index(offs, rs["question"][1] - 1))
    chars = (
        all(text[s:e] == t for (s, e), t in zip(rs["statements"], statements, strict=True))
        and text[slice(*rs["question"])] == question
        and text[rs["tail"][0] : rs["tail"][0] + len(INSTRUCTION) + 1] == " " + INSTRUCTION
    )
    whole = (
        all(  # each statement is a run of whole tokens (the first may carry the space before it)
            tok.decode(ids[a : b + 1]) in (t, " " + t) for a, b, t in zip(starts, ends, statements, strict=True)
        )
        and tok.decode(ids[q[0] : q[1] + 1]) in (question, "\n" + question)
    )
    return {
        "ids": ids,
        "statement_starts": starts,
        "statement_ends": ends,
        "question": q,
        "spans_decode": chars and whole,
    }


def check_item(tok, item: dict) -> dict[str, Any]:
    """pointer_v1.check_item on this module's statements, plus the spans and the statements' text."""
    dom, cond = item["domain"], item["condition"]
    base = prompt_layout(tok, item["context"], item["question"], item["statements"], item["spans"])
    out: dict[str, Any] = {"spans_decode": base["spans_decode"]}
    allowed: set[int] = set()
    for st, en in zip(base["statement_starts"], base["statement_ends"], strict=True):
        allowed |= set(range(st, en + 1))
    q0, q1 = base["question"]
    allowed |= set(range(q0, q1 + 1))
    for src, s in item["sources"].items():
        lay = prompt_layout(tok, s["context"], s["question"], s["statements"], s["spans"])
        out["spans_decode"] = out["spans_decode"] and lay["spans_decode"]
        same_len = len(lay["ids"]) == len(base["ids"])
        diff = S.changed(base["ids"], lay["ids"]) if same_len else None
        out[f"{src}_aligned"] = (
            same_len
            and lay["statement_starts"] == base["statement_starts"]
            and lay["statement_ends"] == base["statement_ends"]
            and lay["question"] == base["question"]
            and bool(diff)
            and set(diff or []) <= allowed  # only statements and the question's cue may differ; the template never
        )
    texts_ok = item["statements"] == [
        statement(dom, cond, e, d) for e, d in zip(item["entities"], item["digits"], strict=True)
    ] and all(
        s["statements"] == [statement(dom, cond, e, d) for e, d in zip(s["entities"], s["digits"], strict=True)]
        for s in item["sources"].values()
    )
    look = dict(zip(item["entities"], item["digits"], strict=True))
    sl, ents, dg = item["slots"], item["entities"], item["digits"]
    d = item["sources"]["dissoc"]
    lookup = item["family"] != "RR"
    pd, q_s, p = d["predictions"], d["query"], ents[sl["position"]]
    perm = (
        ents[sl["query"]] == item["query"]
        and ents[sl["identity"]] == q_s
        and d["entities"][sl["position"]] == q_s
        and d["query_slot"] == sl["position"]
        and sorted(d["entities"]) == sorted(ents)
        and len(set(ents)) == len(ents)
    )
    if lookup:
        perm = perm and pd == {"none": str(look[item["query"]]), "identity": str(dg[sl["identity"]]),
                               "position": str(dg[sl["position"]]), "value": str(d["digits"][sl["position"]])}  # fmt: skip
        value_absent, distinct = int(pd["value"]) not in dg, len(set(pd.values())) == 4
    else:
        perm = perm and pd["none"] == str(item["recalled"][item["query"]]) and pd["position"] == str(rec(dom, p))
        value_absent, distinct = True, pd["none"] != pd["identity"]
    critical = {rec(dom, e) for e in (item["query"], q_s, p)}
    same, redigit = item["sources"]["same"], item["sources"]["redigit"]
    return out | {
        "statements_text": texts_ok,
        "permutation": perm,
        "value_absent": value_absent,
        "predictions_distinct": distinct,
        "hard_collision_free": not (set(dg) & critical) and int(d["digits"][sl["position"]]) not in critical,
        "soft_collision_free": not (set(dg) & set(item["recalled"].values())),
        "soft_promised": item["digit_policy"] == "soft",
        "same_noop": same["entities"][sl["query"]] == item["query"]
        and same["digits"][sl["query"]] == look[item["query"]]
        and same["context"] != item["context"]
        and len(set(same["predictions"].values())) == 1,
        "redigit_one_change": [x != y for x, y in zip(redigit["digits"], dg, strict=True)].count(True) == 1
        and redigit["entities"] == ents,
    }


TEXT_KEYS = ("id", "level", "context", "statements", "spans", "condition", "surface", "language", "alias")


def without_surface(item: dict) -> dict:
    """The item with every field that may differ across conditions removed (statement text and its bookkeeping)."""
    out = {k: v for k, v in item.items() if k not in TEXT_KEYS}
    out["sources"] = {s: {k: v for k, v in x.items() if k not in TEXT_KEYS} for s, x in item["sources"].items()}
    return out


def paired_conditions(items: list[dict]) -> dict[str, int]:
    """Items of one scene and family in different conditions are identical but for the statements' text."""
    groups: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for it in items:
        groups[(it["scene"], it["family"])].append(it)
    stats = collections.Counter()
    for (_, _), its in groups.items():
        conds = {it["condition"] for it in its}
        stats["groups"] += 1
        stats["complete"] += conds == set(DOMAINS[its[0]["domain"]]["conditions"]) and len(its) == len(conds)
        ref = without_surface(its[0])
        stats["identical_but_statements"] += all(without_surface(x) == ref for x in its[1:])
        stats["statements_differ"] += all(
            x["context"] != its[0]["context"] and x["statements"] != its[0]["statements"] for x in its[1:]
        )
    return dict(stats)


def stage_make(which: str) -> None:
    tok = tokenizer()
    print(json.dumps(check_pools(tok)))
    for _label, (path, items, note) in generate(which).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        assert not path.exists(), f"{path} exists; data files are written once"
        head = {"family": items[0]["family"], "domain": items[0]["domain"], "level": items[0]["level"],
                "condition": items[0]["condition"], "generator": note,
                "format": "\n\n".join((__doc__ or "").split("\n\n")[2:5])}  # fmt: skip
        body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)  # one item per line: grep-able, compact
        path.write_text(json.dumps(head, indent=1, ensure_ascii=False)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")
        print("wrote", path, len(items))


def stage_verify() -> None:
    """Every set regenerated from this code equals its files."""
    for which in SETS:
        for label, (path, items, _) in generate(which).items():
            if not path.exists():
                print(which, label, "no file yet")
                continue
            same = load_file(path) == items
            print(which, label, "same" if same else "DIFFERENT")
            assert same, f"{label}: the generator no longer reproduces {path}"


def stage_check(which: str) -> None:
    from bridge_jspace.utils import progress

    tok = tokenizer()
    report: dict[str, Any] = {"pools": check_pools(tok), "files": {}}
    everything: list[dict] = []
    for label, path in progress(list(set_files(which).items()), "files"):
        items = load_file(path)
        everything += items
        stats: collections.Counter = collections.Counter()
        slots = {k: collections.Counter() for k in ("query", "identity", "position")}
        answers, values, queries, langs = (collections.Counter() for _ in range(4))
        prompts, lengths = set(), []
        for it in items:
            for k, v in check_item(tok, it).items():
                stats[k] += bool(v)
            for k in slots:
                slots[k][it["slots"][k]] += 1
            answers[it["answer"]] += 1
            values[it["sources"]["dissoc"]["predictions"]["value"]] += 1
            queries[it["query"]] += 1
            langs[it["language"][it["query"]]] += 1
            text = S.render(tok, it["context"], it["question"])
            prompts.add(text)
            lengths.append(len(S.ids(tok, text)))
        n = len(items)
        r = {"n": n, **stats, "unique_prompts": len(prompts),
             "prompt_tokens(min,median,max)": (min(lengths), statistics.median(lengths), max(lengths)),
             "slots": {k: dict(sorted(v.items())) for k, v in slots.items()}, "answers": dict(sorted(answers.items())),
             "values": dict(sorted(values.items())), "queries": dict(queries.most_common()),
             "query_language": dict(langs)}  # fmt: skip
        print(label, json.dumps(r))
        must = ("dissoc_aligned", "same_aligned", "redigit_aligned", "permutation", "value_absent", "hard_collision_free",
                "same_noop", "redigit_one_change", "predictions_distinct", "spans_decode", "statements_text")  # fmt: skip
        for k in must:
            assert stats[k] == n, f"{label}: {k} {stats[k]}/{n}"
        assert stats["soft_collision_free"] >= stats["soft_promised"], f"{label}: soft policy broken"
        assert len(prompts) == n, f"{label}: repeated prompts"
        report["files"][label] = r
    paired = paired_conditions(everything)
    print("paired", json.dumps(paired))
    assert paired["groups"] == paired["complete"] == paired["identical_but_statements"] == paired["statements_differ"]
    report["paired_conditions"] = paired
    out = DATA / f"check_{which}.json"
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    print("wrote", out)


# ---- competence -----------------------------------------------------------------------------------------------------

PROMPT_KINDS = ("clean", *(f"src_{s}" for s in SOURCES), "hop1", "hop2", "alias")
GATE_MIN_SCENES = (
    35  # 3.84 / (35 + 3.84) <= 0.10: the smallest n where a no-change control can pass pointer_swap's rule
)
KIND_NAME = {  # plain column names (figure_terms.md)
    "clean": "org prompt", "src_dissoc": "alt prompt", "src_same": "control: same entity, reshuffled",
    "src_redigit": "control: answer digit changed", "hop1": "step: cue → entity", "hop2": "step: lookup or fact alone",
    "alias": "step: other form → English name",
}  # fmt: skip


def said(text: str, judge: str, aliases: dict[str, str]) -> str | None:
    """The first answer of the judge's kind in the first non-empty line: a digit (pointer_v1's: digits, number words,
    ordinals), or an entity of the domain named in English; with '+alias' also the prompt's surface forms (matched
    case-sensitively, so the symbol 'O' is not the letter 'o'), mapped to the English entity."""
    if judge == "digit":
        return PV.said(text, "digit")
    domain, _, extra = judge.partition("+")
    line = next((ln for ln in text.split("\n") if ln.strip()), "")
    english = {e.lower(): e for e in DOMAINS[domain]["entities"]}
    for w in re.findall(r"[^\W\d_]+", line):
        if w.lower() in english:
            return english[w.lower()]
        if extra and w in aliases:
            return aliases[w]
    return None


def item_prompts(it: dict) -> dict[str, tuple[str, str, str, str]]:
    """kind -> (context, question, expected answer, judge) for one item. hop1 (cue -> entity) also accepts the
    entity's surface form; the alias step (surface form -> entity) only the English name."""
    spec = {"clean": (it["context"], it["question"], it["answer"], "digit")}
    for s in SOURCES:
        src = it["sources"][s]
        spec[f"src_{s}"] = (src["context"], src["question"], src["answer"], "digit")
    for h in ("hop1", "hop2", "alias"):
        if h in it:
            judge = it[h]["kind"]
            if h == "hop1" and it["condition"] != "same":
                judge += "+alias"
            spec[h] = (it["context"], it[h]["question"], it[h]["answer"], judge)
    return spec


def stage_manifest(name: str, why: str, sets: list[str], limit: int | None) -> None:
    pins.check_run_name(name)
    from bridge_jspace.data import sha256_of

    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    files = {f"{s}/{label}": f for s in sets for label, f in set_files(s).items()}
    manifest = {
        "exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
        "model": pins.model_pin(), "switches": switches(), "sets": sets,
        "items": {k: {"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(f)} for k, f in files.items()},
        "limit": limit,
        "conditions": {c: COND_NAME[c] for c in CONDITIONS},
        "format": "suite_v1's: chat template, thinking off, 'Answer:' prefilled; the context, a newline, the question and "
        f"'{INSTRUCTION}' in one user turn",
        "prompts": "base; each source (dissoc, same, redigit) with its own context and question; hop1 (cue -> entity) "
        "and hop2 (the lookup with the entity named / the recalled fact) for RL and RR; alias (surface form -> English "
        "entity) for RL and DL in xlang / syn; every step with the base context",
        "judge": "the first answer of the prompt's kind in the first non-empty line of 8 greedy tokens (digits, number "
        "words and ordinals for digits; the domain's English names otherwise; hop1 in xlang / syn also the surface "
        "form, matched case-sensitively)",
        "answer_read": "suite_v1's: one forward with a digit answer's space token appended; p and margin of the answer's "
        "first token; whether the read's top token is the greedy answer",
        "gate": (__doc__ or "").split("Gate (")[1].split("\n\n")[0].split("): ", 1)[1].replace("\n", " "),
        "eligibility": "pointer_swap uses items with every prompt right (base, the three sources, the steps alone)",
    }  # fmt: skip
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print("wrote", path)


def gate(summary_labels: dict[str, dict], paired: dict[str, dict]) -> dict[str, dict]:
    """The docstring's gate per (set, domain, alias level): lookups' clean lower bound >= 0.80, the English baseline's
    >= 0.85, >= GATE_MIN_SCENES scenes eligible in every family of both conditions."""
    out = {}
    for label in summary_labels:
        which, rest = label.split("/")
        dom, fam, lv = rest.split("_")
        if "-" not in lv or fam != "RL":
            continue
        base = lv.split("-")[0]
        cells = {f: summary_labels.get(f"{which}/{dom}_{f}_{lv}") for f in ("RL", "DL")}
        eng = {f: summary_labels.get(f"{which}/{dom}_{f}_{base}") for f in ("RL", "DL")}
        if not all(cells.values()) or not all(eng.values()):
            continue
        lookups_ok = all(c["cells"]["clean"]["lo"] >= 0.80 for c in cells.values() if c)
        english_ok = all(c["cells"]["clean"]["lo"] >= 0.85 for c in eng.values() if c)
        n_eligible = paired.get(f"{which}/{dom}/{lv}", {}).get("eligible_scenes_both", 0)
        out[f"{which}/{dom}/{lv}"] = {
            "lookups_lo>=0.80": lookups_ok, "english_lo>=0.85": english_ok, "eligible_scenes_both": n_eligible,
            "passes": lookups_ok and english_ok and n_eligible >= GATE_MIN_SCENES,
        }  # fmt: skip
    return out


def summarise(rows: list[dict], labels: list[str]) -> dict[str, Any]:
    from bridge_jspace.stats import wilson

    summary: dict[str, Any] = {"labels": {}, "paired": {}}
    per_item_all: dict[str, dict[str, bool]] = collections.defaultdict(dict)
    meta: dict[str, dict] = {}
    for r in rows:
        per_item_all[r["id"]][r["kind"]] = r["correct"]
        meta[r["id"]] = r
    for label in labels:
        fr = [r for r in rows if r["label"] == label]
        if not fr:
            continue
        per_item = {i: per_item_all[i] for i in dict.fromkeys(r["id"] for r in fr)}
        cells = {}
        for kind in PROMPT_KINDS:
            got = [v[kind] for v in per_item.values() if kind in v]
            if got:
                cells[kind] = dict(zip(("rate", "lo", "hi"), wilson(sum(got), len(got)), strict=True)) | {"k": sum(got)}
        clean = [r for r in fr if r["kind"] == "clean"]
        summary["labels"][label] = {
            "n": len(per_item), "condition": fr[0]["condition"], "cells": cells,
            "eligible": sum(all(v.values()) for v in per_item.values()),
            "reliable": cells["clean"]["lo"] >= 0.85,
            "clean_median_p_answer": statistics.median(r["p_answer"] for r in clean),
            "read_agrees_with_greedy": statistics.mean((r["said"] or "").lower().startswith(r["read_top"].lower())
                                                       if r["read_top"] else False for r in fr),
        }  # fmt: skip
    # paired by scene: English vs the alias condition, per (set, domain, alias level)
    scenes: dict[tuple[str, str, str], dict[str, dict[str, list[bool]]]] = collections.defaultdict(
        lambda: collections.defaultdict(lambda: collections.defaultdict(list))
    )
    for i, kinds in per_item_all.items():
        r = meta[i]
        which = r["label"].split("/")[0]
        base = r["level"].split("-")[0]
        scenes[(which, r["domain"], base)][r["scene"]][r["condition"]].append(all(kinds.values()))
    clean_ok = {i: kinds.get("clean", False) for i, kinds in per_item_all.items()}
    for (which, dom, base), by_scene in sorted(scenes.items()):
        for cond in DOMAINS[dom]["conditions"][1:]:
            both = [s for s, v in by_scene.items() if "same" in v and cond in v]
            n_fam = len(FAMILIES)
            elig = sum(len(by_scene[s]["same"]) == len(by_scene[s][cond]) == n_fam and all(by_scene[s]["same"])
                       and all(by_scene[s][cond]) for s in both)  # fmt: skip
            pairs = {}
            for fam in FAMILIES:
                cnt = collections.Counter()
                for s in both:
                    a = clean_ok.get(f"{dom}-{fam}-{base}-{s.rsplit('-', 1)[1]}")
                    b = clean_ok.get(f"{dom}-{fam}-{base}{SUFFIX[cond]}-{s.rsplit('-', 1)[1]}")
                    if a is None or b is None:
                        continue
                    cnt["both" if a and b else "english_only" if a else "alias_only" if b else "neither"] += 1
                pairs[fam] = dict(cnt)
            summary["paired"][f"{which}/{dom}/{base}{SUFFIX[cond]}"] = {
                "scenes": len(both),
                "eligible_scenes_both": elig,
                "clean_by_family": pairs,
            }
    summary["gate"] = gate(summary["labels"], summary["paired"])
    return summary


def summary_md(s: dict) -> str:
    from bridge_jspace.plotting import family_label

    lines = ["| file | statements | question | n | " + " | ".join(KIND_NAME[k] for k in PROMPT_KINDS)
             + " | eligible | median p | read = greedy |",
             "|---" * (len(PROMPT_KINDS) + 7) + "|"]  # fmt: skip
    for label, x in s["labels"].items():
        c = x["cells"]
        cols = [
            f"{100 * c[k]['rate']:.0f}% [{100 * c[k]['lo']:.0f},{100 * c[k]['hi']:.0f}]" if k in c else "-"
            for k in PROMPT_KINDS
        ]
        fam = label.split("_")[1]
        lines.append(f"| {label} | {COND_NAME[x['condition']]} | {family_label(fam)} | {x['n']} | " + " | ".join(cols)
                     + f" | {x['eligible']} | {x['clean_median_p_answer']:.3f} | "
                     f"{100 * x['read_agrees_with_greedy']:.1f}% |")  # fmt: skip
    lines += ["", "Paired by scene (base prompt right): both / English only / other form only / neither", ""]
    for key, p in s["paired"].items():
        cells = "; ".join(f"{family_label(f)}: {v.get('both', 0)} / {v.get('english_only', 0)} / "
                          f"{v.get('alias_only', 0)} / {v.get('neither', 0)}" for f, v in p["clean_by_family"].items())  # fmt: skip
        lines.append(f"- {key}: {p['scenes']} scenes, {p['eligible_scenes_both']} eligible in both conditions; {cells}")
    lines += ["", "Gate (docstring rule): " + "; ".join(f"{k}: {'PASS' if v['passes'] else 'FAIL'} {v}"
                                                         for k, v in s["gate"].items())]  # fmt: skip
    return "\n".join(lines) + "\n"


def stage_competence(name: str) -> None:
    import torch

    from bridge_jspace.data import sha256_of
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts.exp03_brew_swaps import write_jsonl

    out_dir = RESULTS / name
    manifest = json.loads((out_dir / "manifest.json").read_text())
    check_switches(manifest)
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    for f, pin in manifest["items"].items():
        assert sha256_of(pins.REPO_ROOT / pin["file"]) == pin["sha256"], f"{f} changed since the manifest"
    model = load_model()
    tok = model.tokenizer
    t0 = time.time()
    prompts = []
    labels = list(manifest["items"])
    for label in labels:
        for it in load_file(pins.REPO_ROOT / manifest["items"][label]["file"])[: manifest.get("limit")]:
            aliases = {w: e for e, w in it["surface"].items() if w != e}
            for kind, (ctx, q, ans, judge) in item_prompts(it).items():
                prompts.append({"label": label, "family": it["family"], "domain": it["domain"], "level": it["level"],
                                "condition": it["condition"], "scene": it["scene"], "id": it["id"], "kind": kind,
                                "expected": ans, "answer_kind": "digit" if judge == "digit" else "word",
                                "judge": judge, "aliases": aliases, "ids": S.ids(tok, S.render(tok, ctx, q))})  # fmt: skip
    print(len(prompts), "prompts", flush=True)
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"])].append(p)
    chunks = [g[i : i + 64] for g in by_len.values() for i in range(0, len(g), 64)]
    for chunk in progress(chunks, "generate"):
        texts = model.generate_batch(torch.tensor([p["ids"] for p in chunk], device="cuda"), 8, [{}] * len(chunk))
        for p, text in zip(chunk, texts, strict=True):
            p["continuation"] = text
            p["said"] = said(text, p["judge"], p["aliases"])
            p["correct"] = (p["said"] or "").lower() == p["expected"].lower()
    t_gen = time.time() - t0
    S.read_answers(model, tok, prompts)
    t_read = time.time() - t0 - t_gen
    rows = [{k: v for k, v in p.items() if k not in ("ids", "forced", "aliases")} for p in prompts]
    write_jsonl(out_dir / "items.jsonl", rows)
    summary = summarise(rows, labels) | {"seconds_generate": round(t_gen), "seconds_read": round(t_read)}
    summary["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out_dir / "summary.md").write_text(summary_md(summary))
    print((out_dir / "summary.md").read_text())


# ---- examples and figures -------------------------------------------------------------------------------------------


def load_run(name: str) -> tuple[dict, list[dict], dict[str, dict]]:
    run_dir = RESULTS / name
    m = json.loads((run_dir / "manifest.json").read_text())
    rows = [json.loads(x) for x in (run_dir / "items.jsonl").read_text().splitlines()]
    items = {it["id"]: it for pin in m["items"].values() for it in load_file(pins.REPO_ROOT / pin["file"])}
    return m, rows, items


GROUP_DEFS = {
    "{c}_right": "base prompt answered right, {name}",
    "{c}_wrong": "base prompt answered wrong, {name}",
    "alias_wrong": "the alias step alone (surface form -> English name) answered wrong",
}


def stage_examples(name: str, k: int, seed: int) -> None:
    """results/alias_pointer_v1/<name>/examples.json: k examples per group (base prompt right / wrong per condition;
    the alias step wrong), sampled with a fixed seed, with the prompt exactly as fed and its spans."""
    try:
        from bridge_jspace.tokens import load_tokenizer

        tok = load_tokenizer()
    except Exception:
        tok = tokenizer()
    from bridge_jspace.plotting import family_label

    _, rows, items = load_run(name)
    groups: dict[str, list[dict]] = collections.defaultdict(list)
    defs: dict[str, str] = {}
    titles: dict[str, str] = {"alias_wrong": "alias step wrong"}
    for r in rows:
        if r["kind"] == "clean":
            outcome = "right" if r["correct"] else "wrong"
            g = f"{r['condition']}_{outcome}"
            groups[g].append(r)
            defs[g] = GROUP_DEFS["{c}_" + outcome].format(name=COND_NAME[r["condition"]])
            titles[g] = f"{COND_NAME[r['condition']]}: {outcome}"
        elif r["kind"] == "alias" and not r["correct"]:
            groups["alias_wrong"].append(r)
            defs["alias_wrong"] = GROUP_DEFS["alias_wrong"]
    rng = random.Random(seed)
    examples = []
    for g in sorted(groups):
        for r in rng.sample(groups[g], min(k, len(groups[g]))):
            it = items[r["id"]]
            q = it["alias"]["question"] if r["kind"] == "alias" else it["question"]
            sp = turn_spans(it["context"], q, it["spans"]["statements"], it["spans"]["filler"])  # same context
            text, rs = rendered_spans(tok, it["context"], q, sp)
            a = it["slots"]["query"]
            spans = [{"start": s, "end": e, "role": f"statement: {ent} as '{it['surface'][ent]}'"
                      + (" (the queried entity's)" if j == a else "")}
                     for j, ((s, e), ent) in enumerate(zip(rs["statements"], it["entities"], strict=True))]  # fmt: skip
            spans += [{"start": rs["question"][0], "end": rs["question"][1], "role": "question"},
                      {"start": rs["tail"][0], "end": rs["tail"][1], "role": "template tail"}]  # fmt: skip
            if r["kind"] == "clean" and it["cue"] in q:
                c0 = rs["question"][0] + q.index(it["cue"])
                spans.append({"start": c0, "end": c0 + len(it["cue"]), "role": "cue"})
            examples.append({
                "group": g, "family": it["family"], "family_name": family_label(it["family"]), "item_id": it["id"],
                "domain": it["domain"],
                "prompt": text, "spans": spans,
                "condition": f"{COND_NAME[it['condition']]}, question in English; unedited, 8 greedy tokens"
                + (" (the alias step alone)" if r["kind"] == "alias" else ""),
                "answers": {"clean": r["expected"], "edited": None, "model": r["said"],
                            "continuation": r["continuation"], "expected": {"right": r["expected"]}},
                "numbers": {"correct": r["correct"], "p_answer": r["p_answer"], "margin": r["margin"],
                            "read_top": r["read_top"]},
                "why": defs[g] + f" (expected {r['expected']!r}, said {r['said']!r})",
            })  # fmt: skip
    out = {"exp": EXP, "run": name, "seed": seed, "k": k,
           "groups": [{"key": g, "title": titles[g], "definition": defs[g], "n_total": len(v)}
                      for g, v in sorted(groups.items())], "examples": examples}  # fmt: skip
    path = RESULTS / name / "examples.json"
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("wrote", path, len(examples), "examples")


COND_STYLE = {"same": ("#2a78d6", "o"), "xlang": ("#eb6834", "s"), "syn": ("#1baf7a", "^")}


def stage_figures(name: str) -> Path:
    """Per domain: the base prompt's accuracy, and the share of items with every prompt right, per family and
    condition (Wilson 95%), main set, with the gate's 80% line."""
    import shutil

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    from bridge_jspace.plotting import INK, MUTED, family_label, finish, percent_axis, style_axes
    from bridge_jspace.stats import wilson

    run_dir = RESULTS / name
    s = json.loads((run_dir / "summary.json").read_text())
    for old in sorted(run_dir.glob("analysis-*-figures")):  # one figures folder per run
        assert old.is_dir(), old
        assert old.parent == run_dir, old
        shutil.rmtree(old)
    folder = run_dir / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}-figures"
    folder.mkdir()
    which = "main" if any(k.startswith("main/") for k in s["labels"]) else next(iter(s["labels"])).split("/")[0]
    doms = [d for d in DOMAINS if any(k.startswith(f"{which}/{d}_") for k in s["labels"])]
    fig, axes = plt.subplots(2, len(doms), figsize=(4.6 * len(doms), 6.4), sharey=True, squeeze=False)
    for j, dom in enumerate(doms):
        conds = DOMAINS[dom]["conditions"]
        for i, what in enumerate(("clean", "eligible")):
            ax = axes[i][j]
            style_axes(ax)
            for ci, cond in enumerate(conds):
                col, mk = COND_STYLE[cond]
                for fi, fam in enumerate(FAMILIES):
                    lv = next((k for k in s["labels"] if k.startswith(f"{which}/{dom}_{fam}_")
                               and s["labels"][k]["condition"] == cond), None)  # fmt: skip
                    if lv is None:
                        continue
                    x = s["labels"][lv]
                    r, lo, hi = (
                        (x["cells"]["clean"][q] for q in ("rate", "lo", "hi"))
                        if what == "clean"
                        else wilson(x["eligible"], x["n"])
                    )
                    xp = fi + (ci - (len(conds) - 1) / 2) * 0.22
                    ax.plot([xp, xp], [lo, hi], color=col, lw=2, solid_capstyle="round")
                    ax.plot(xp, r, mk, color=col, ms=8, mec="white", mew=1.5)
            if what == "clean" and conds != ("same",):
                ax.axhline(0.8, color=MUTED, lw=1, ls=(0, (4, 2)), zorder=1)
            ax.set_xticks(range(len(FAMILIES)), [family_label(f) for f in FAMILIES], fontsize=8.5, color=INK)
            ax.set_xlim(-0.5, len(FAMILIES) - 0.5)
            ax.set_ylim(-0.03, 1.04)
            percent_axis(ax)
            title = "org prompt right" if what == "clean" else "every prompt of the item right (usable)"
            ax.set_title(f"{dom}: {title}", fontsize=9, color=INK, loc="left")
            if j == 0:
                ax.set_ylabel("% of items", fontsize=9, color=INK)
    handles = [Line2D([], [], color=COND_STYLE[c][0], marker=COND_STYLE[c][1], lw=2, ms=8, mec="white",
                      label=COND_NAME[c]) for c in CONDITIONS if any(c in DOMAINS[d]["conditions"] for d in doms)]  # fmt: skip
    handles.append(Line2D([], [], color=MUTED, lw=1, ls=(0, (4, 2)), label="gate: lower bound 80%"))
    ns = "/".join(str(x) for x in sorted({x["n"] for lab, x in s["labels"].items() if lab.startswith(which)}))
    m = json.loads((run_dir / "manifest.json").read_text())
    pin = next(p for k, p in m["items"].items() if k.startswith(f"{which}/") and "_RL_" in k and "-" in k)
    it = load_file(pins.REPO_ROOT / pin["file"])[0]
    a = it["slots"]["query"]
    example = (f'"{it["statements"][a]} ... {it["question"]}" -> {it["answer"]} ({it["query"]} is written '
               f'"{it["surface"][it["query"]]}"; the same scene in English says "{it["query"]}").')  # fmt: skip
    path = folder / "competence_by_condition.png"
    finish(
        fig,
        path,
        "Can the model look up a statement that names the entity in another language or by its symbol?",
        f"{m['model']['repo'].split('/')[-1]}; {ns} scenes per family and form; bars: Wilson 95% intervals",
        handles=handles,
        ncols=2,
        handlelength=3,
        explain=[
            ("What we did", "Asked each question unedited (8 greedy tokens). Each scene's statements are written once "
             "in English and once in another form; the question is always English."),
            ("Example", example),
            ("How to read", "Dot = share right, bar = Wilson 95% interval. Top: the org prompt. Bottom: items whose "
             "org prompt, alt prompt, two control prompts and single steps are all right (usable for patching)."),
            ("Control", "Statements in English on the same scenes (blue): the other forms should stay close to it; "
             "the gate needs both lookup families' lower bound at or above the dashed line."),
        ],
    )  # fmt: skip
    print("wrote", path)
    return folder


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest", "competence", "examples", "figures"])
    ap.add_argument("--set", dest="sets", nargs="+", choices=list(SETS), default=["main"])
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None, help="manifest: the first K items per file (a smoke run)")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
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
    elif args.stage == "competence":
        assert args.name, "competence needs --name"
        stage_competence(args.name)
    elif args.stage == "examples":
        assert args.name, "examples needs --name"
        stage_examples(args.name, args.k, args.seed)
    else:
        assert args.name, "figures needs --name"
        stage_figures(args.name)
