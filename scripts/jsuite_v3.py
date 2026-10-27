"""jsuite_v3 (Zach, 2026-10-27, prereg amendment 58 note 4): the final two-hop facts set, built to address the confounds
found in the 27 Oct audit. Facts module only (three-hop and numbers stay in jsuite_v2). All bridges are test (the bands
were chosen on v2's dev split). Bridges, answers and descriptions: data/v3_bridges.json (scripts/v3_bridges_src.py).

Relations: people -> nationality, cities -> country, companies -> country, landmarks -> country, films -> director.
No answer is used by more than 5% of a relation's bridges; descriptions name no place, nationality, language, people,
food or answer-language title.

Starts (first letter of a word):
  P  read: a made-up person is bound to the bridge in the passage; the question asks about the person
  M  described: the question describes the bridge (recall); the passage names it once in passing
  W  described, and the passage also names a second, unbound entity of the same type in passing (no elimination)
  R  described, never named in the passage (finals M A N only)
  T  tracked: the bridge is the last stop of one of two interleaved sequences
  X  computed: the bridge is the entry at an arithmetic position ("number 5 minus 3") on a person's list
  Q  P rendered as a table of records;  J  P rendered as JSON records
  Y  counterfactual-bridge pair of P: the same passage with another entity in the bridge's place (pair_of = P item)
Finals (second letter; same question and answer unless noted):
  P  a made-up fact of another relation is stated; a different question (control)
  K  the true fact is stated for every entity
  M  recalled: other entities carry made-up facts of another relation; the bridge only a neutral mention
  A  as M, and one other entity carries the bridge's answer word
  N  recalled, no answer-vocabulary word anywhere
  H  hard read: every entity is linked to a made-up anchor of its type, and the anchor's (true) value is stated
  C  conflict: as K, but the bridge's stated value is a counterfactual (answer = the passage's value)
  D  conflict, every fact sentence attributed ("According to the conference handout, ...")
  E  conflict, the question asks "According to the notes, ..."
  F  conflict, attributed and "According to the notes"
  G  as D with the true value (the attribution control)
Levels: 1 = 3 entities, 2 filler sentences; 2 = 6 entities, 6 filler; 3 = 12 entities, 20 filler, the bridge's
sentences in the first third of the passage. Each scene is rendered twice (rep 0 and 1; rep 1 is a replication set).

python scripts/jsuite_v3.py --name jsuite_v3 --seed 3001
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import jsuite_facts as JF  # noqa: E402
from scripts import jsuite_v3_tables as T3  # noqa: E402
from scripts import natplus as NP  # noqa: E402
from scripts import natural_v1 as N  # noqa: E402

DATA = N.DATA
cap = JF.cap
LEVELS3 = {1: {"entities": 3, "filler": 2, "key_early": False}, 2: {"entities": 6, "filler": 6, "key_early": False},
           3: {"entities": 12, "filler": 20, "key_early": True}}  # fmt: skip
MATRIX = {"P": {1: "PKMANHCDEFG", 2: "PKMANHCDEFG", 3: "KMHCDEFG"}, "M": {1: "PKMANHCDEFG", 2: "PKMANHCDEFG"},
          "W": {1: "KMAN", 2: "KMAN"}, "R": {1: "MAN", 2: "MAN"}, "T": {1: "KM"}, "X": {1: "KM"},
          "Q": {1: "KMH"}, "J": {1: "KMH"}}  # fmt: skip  # Y: P level 1 K and M, paired (below)
ATTR = "From the conference handout: "
DISPLAY = {"Netherlands": "the Netherlands", "United States": "the United States", "United Arab Emirates": "the United Arab Emirates",
           "Czech Republic": "the Czech Republic"}  # how an answer reads inside a sentence


def disp(a: str) -> str:
    return DISPLAY.get(a, a)


def sentence(s: str) -> str:
    return s[0].upper() + s[1:]
NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
CONT = {  # answer -> region, for near / far counterfactuals (countries and nationalities)
    "Europe": ["Germany", "Austria", "France", "Italy", "Spain", "Portugal", "Russia", "Poland", "Hungary", "Czech Republic",
               "Netherlands", "Belgium", "Sweden", "Norway", "Denmark", "Finland", "Greece", "Ireland", "Switzerland", "United Kingdom",
               "German", "Austrian", "French", "Italian", "Spanish", "Portuguese", "Russian", "Polish", "Hungarian", "Czech", "Dutch",
               "Belgian", "Swedish", "Norwegian", "Danish", "Finnish", "Greek", "Irish", "Swiss", "English", "Denmark"],
    "Asia": ["Japan", "China", "India", "South Korea", "Thailand", "Vietnam", "Indonesia", "Malaysia", "Cambodia", "Taiwan", "Turkey",
             "Israel", "Jordan", "United Arab Emirates", "Japanese", "Chinese", "Indian", "Korean", "Turkish"],
    "Africa": ["Egypt", "Morocco", "South Africa", "Kenya", "Tanzania", "Nigeria", "Egyptian", "South African", "Kenyan", "Nigerian"],
    "Americas": ["United States", "Canada", "Mexico", "Brazil", "Argentina", "Peru", "Chile", "Colombia", "Venezuela", "Ecuador",
                 "American", "Canadian", "Mexican", "Brazilian", "Argentine", "Chilean", "Colombian", "Jamaican"],
    "Oceania": ["Australia", "Australian"],
}  # fmt: skip
REGION = {a: r for r, xs in CONT.items() for a in xs}


class Deck:
    """Filler runs of `need` sentences, dealt without replacement and reshuffled when exhausted; a need longer than every
    clean run is met by joining runs from different paragraphs."""

    def __init__(self, rng: random.Random, paras: list[list[str]]):
        self.rng, self.paras, self.decks = rng, paras, {}
        self.longest = max(len(p) for p in paras)

    def deal(self, need: int) -> list[str]:
        if need > self.longest:
            out: list[str] = []
            while len(out) < need:
                out += self.deal(min(self.longest, need - len(out)) if need - len(out) >= 2 else 2)
            return out[:need]
        d = self.decks.setdefault(need, [])
        if not d:
            d.extend(p for p in self.paras if len(p) >= need)
            self.rng.shuffle(d)
        run = d.pop()
        st = self.rng.randrange(len(run) - need + 1)
        return run[st : st + need]


def words_in(text: str, words) -> list[str]:
    return [w for w in words if re.search(r"(?i)\b" + re.escape(w) + r"\b", text)]


def splice(rng: random.Random, genre: str, facts: list[str], para: list[str], keys: set[int], key_early: bool) -> str:
    """JF.splice with the facts shuffled; with key_early, the facts at indices keys go into the first third of the
    filler boundaries and the rest anywhere (level 3: the bridge's sentences far from the question)."""
    order = list(range(len(facts)))
    rng.shuffle(order)
    third = max(1, (len(para) + 1) // 3)
    slot = {i: (rng.randrange(third) if key_early and i in keys else rng.randrange(len(para) + 1)) for i in order}
    order.sort(key=lambda i: slot[i])
    body, fi = [], 0
    for b in range(len(para) + 1):
        while fi < len(order) and slot[order[fi]] == b:
            body.append(facts[order[fi]])
            fi += 1
        if b < len(para):
            body.append(para[b])
    head, tail = N.GENRES[genre]
    if genre == "notes":
        return head + "\n" + "\n".join("- " + s for s in body) + "\n" + tail
    sep = "\n\n" if genre == "email" else "\n"
    return head + sep + " ".join(body) + sep + tail


def records(genre: str, fmt: str, triples: list[tuple[str, str, str]], para: list[str], rng: random.Random) -> str:
    """The table (Q) or JSON (J) rendering: the facts as subject / relation / object records (shuffled), the filler as
    notes."""
    triples = triples[:]
    rng.shuffle(triples)
    head, tail = N.GENRES[genre]
    if fmt == "table":
        rows = ["| subject | relation | object |", "|---|---|---|"] + [f"| {s} | {r} | {o} |" for s, r, o in triples]
        body = "\n".join(rows) + "\n\nNotes: " + " ".join(para)
    else:
        body = json.dumps({"records": [{"subject": s, "relation": r, "object": o} for s, r, o in triples], "notes": para}, indent=1)
    return f"{head}\n{body}\n{tail}"


def counterfactual(rng: random.Random, real: str, vocab: list[str], near: bool) -> tuple[str, bool]:
    """A wrong value: from the real answer's region when near (if any), else from another region; uniform when the
    relation has no regions (films). Returns (value, is_near)."""
    others = [a for a in vocab if a != real]
    reg = REGION.get(real)
    if reg is None:
        return rng.choice(others), False
    same = [a for a in others if REGION.get(a) == reg]
    diff = [a for a in others if REGION.get(a) not in (None, reg)]
    if near and same:
        return rng.choice(same), True
    return rng.choice(diff or others), False


def facts_items(rng: random.Random, tabs: dict, deck: Deck, reps: int) -> list[dict]:
    items: list[dict] = []
    k = 0
    for rel, t in tabs.items():
        facts, meta = t["facts"], t["meta"]
        alias_of = {r["answer"]: r["answer_aliases"] for r in meta.values()}
        vocab = sorted({v[0] for v in facts.values()})
        people = rel == "people"
        objs, sent, tdesc, tq = t["track"]
        tri = t["triple"]
        bridges = sorted(facts)
        halves = {}
        for pop in ("popular", "less_popular"):
            xs = [x for x in bridges if facts[x][2] == pop]
            rng.shuffle(xs)
            halves.update({x: "AB"[i % 2] for i, x in enumerate(xs)})
        for rep in range(reps):
            for start, levels in MATRIX.items():
                for level, finals in levels.items():
                    knobs = LEVELS3[level]
                    for x in bridges:
                        k += 1
                        w = rng.randrange(3)
                        real = facts[x][0]
                        pool = [e for e in bridges if e != x]
                        rng.shuffle(pool)
                        pool.sort(key=lambda o: facts[o][0] == real)  # entities sharing the bridge's answer last
                        n_ent = 6 if start == "T" else knobs["entities"]
                        ents = [x] + pool[: n_ent - 1]
                        rest = pool[n_ent - 1 :]
                        persons = rng.sample(NP.PEOPLE_NAMES, len(ents))
                        newv = {e: rng.choice([a for a in vocab if a != facts[e][0]]) for e in ents}
                        used = {facts[o][0] for o in ents}
                        alt = next((e for e in rest if facts[e][0] not in used), None)  # Y: the counterfactual bridge (its answer on no scene entity)
                        if alt is None:
                            continue
                        avoid = {e: rng.choice([a for a in vocab if a not in (facts[e][0], real, facts[alt][0])]) for e in ents}
                        carrier = next((e for e in ents[1:] if facts[e][0] != real), None)
                        genre = rng.choice(sorted(N.GENRES))
                        para = deck.deal(knobs["filler"])
                        lay = random.Random(rng.random())  # the passage layout, shared by every final of the scene
                        lay_seed = lay.random()
                        di = rng.randrange(len(facts[x][1]))
                        noun, clause = facts[x][1][di]
                        near = rng.random() < 0.5
                        cf, cf_near = counterfactual(rng, real, vocab, near)
                        taken = set(bridges) | set(vocab) | set(NP.PEOPLE_NAMES)
                        anc = {e: T3.anchor_name(t["anchor"], rng, taken) for e in ents}
                        d2 = next((e for e in rest if e != alt), None)  # W: the second, unbound entity named in passing
                        if carrier is None or d2 is None:
                            continue
                        expr = None
                        if start in ("P", "Q", "J"):
                            d1, q1 = t["pdesc"][w].format(p=persons[0]), t["q1P"][w].format(p=persons[0])
                            gd = t["pdesc"][w].format(p=rng.choice(N.ABSENT_NAMES))
                        elif start in ("M", "W", "R"):
                            d1, q1 = JF.m_desc(noun, clause, people)
                            gd = t["unknown"]
                        elif start == "X":
                            pos = rng.randrange(len(ents))
                            a_, b_ = rng.randrange(pos + 2, 10), None
                            b_ = a_ - (pos + 1)
                            expr = f"{NUMW[a_]} minus {NUMW[b_]}"
                            d1 = f"the {t['noun']} that is number {expr} on {persons[0]}'s list"
                            q1 = f"Which {t['noun']} is number {expr} on {persons[0]}'s list?"
                            gd = f"the {t['noun']} that is number {expr} on {rng.choice(N.ABSENT_NAMES)}'s list"
                        else:  # T
                            oa, ob = rng.sample(objs, 2)
                            d1, q1 = tdesc.format(o=oa), tq.format(o=oa)
                            gd = tdesc.format(o=rng.choice([o for o in objs if o not in (oa, ob)]))
                        bad = set(words_in(d1 + " " + q1, vocab))  # values the question itself names: never drawn as a made-up value
                        for e in ents:
                            while newv[e] in bad:
                                newv[e] = rng.choice([v for v in vocab if v != facts[e][0]])
                            while avoid[e] in bad:
                                avoid[e] = rng.choice([v for v in vocab if v not in (facts[e][0], real, facts[alt][0])])
                        while cf in bad:
                            cf, cf_near = counterfactual(rng, real, vocab, near)
                        for F in finals:
                            pairs = ((x, start), (alt, "Y")) if (start == "P" and level == 1 and F in "KM") else ((x, start),)
                            for bridge, wstart in pairs:
                                es = [bridge] + ents[1:]
                                breal = facts[bridge][0]
                                kf = lambda e, a: sentence(t["kfact"][w].format(x=e, X=cap(e), a=disp(a), al=a.lower(), an=N.an(a)))  # noqa: E731
                                pf = lambda e, a: sentence(t["pfact"][w].format(x=e, X=cap(e), a=disp(a), al=a.lower(), an=N.an(a)))  # noqa: E731
                                nf = lambda e, wi=w: sentence(t["nfact"][wi].format(x=e, X=cap(e)))  # noqa: E731
                                hl = lambda e, y: sentence(t["hlink"][w].format(x=e, X=cap(e), y=y))  # noqa: E731
                                trip, fin, keys = [], [], set()
                                ans, src, q2, mem = breal, "M", t["q2M"][w], None
                                if F == "P":
                                    ans, src, q2 = newv[x], "P", t["q2P"][w]
                                    fin = [pf(e, newv[e] if e != bridge else ans) for e in es]
                                    trip = [(e, tri["pfact"], newv[e] if e != bridge else ans) for e in es]
                                    keys = {0}
                                elif F in "KG":
                                    fin = [kf(e, facts[e][0]) for e in es]
                                    trip = [(e, tri["kfact"], facts[e][0]) for e in es]
                                    keys = {0}
                                elif F in "CDEF":
                                    ans, mem = cf, breal
                                    fin = [kf(e, facts[e][0] if e != bridge else cf) for e in es]
                                    keys = {0}
                                elif F in "MAN":
                                    if F == "N":
                                        fin = [nf(e) for e in es if not (start == "R" and e == bridge)]
                                    else:
                                        fin = [pf(e, breal if (F == "A" and e == carrier) else avoid[e]) for e in es[1:]]
                                        fin += [] if start == "R" else [nf(bridge)]
                                    trip = [(e, tri["pfact"], avoid[e]) for e in es[1:]] + [(bridge, "mentioned in", "the letters page")]
                                    keys = {len(fin) - 1} if start != "R" else set()
                                elif F == "H":
                                    fin, trip = [], []
                                    for e in es:
                                        fin += [hl(e, anc[e]), kf(anc[e], facts[e][0])]
                                        trip += [(e, tri["hlink"], anc[e]), (anc[e], tri["kfact"], facts[e][0])]
                                    keys = {0, 1}
                                if F in "DFG":
                                    fin = [ATTR + s for s in fin]
                                if start == "W":
                                    fin = fin + [nf(d2, (w + 1) % 3)]
                                # the bridge's binding (or list, or sequence) sentences, then the final's facts
                                if start in ("P", "Q", "J"):
                                    binds = [t["bind"][w].format(p=p, x=e, X=cap(e)) for p, e in zip(persons, es, strict=True)]
                                    btrip = [(p, tri["bind"], e) for p, e in zip(persons, es, strict=True)]
                                    bkeys = {0}
                                elif start == "X":
                                    order = es[:]
                                    lay2 = random.Random(lay_seed)
                                    lay2.shuffle(order)
                                    order.remove(bridge)
                                    order.insert(pos, bridge)
                                    binds = [f"On {persons[0]}'s list, " + ", ".join(f"number {NUMW[i + 1]} is {e}" for i, e in enumerate(order)) + "."]
                                    btrip, bkeys = [], {0}
                                elif start == "T":
                                    seq_a, seq_b = es[1:3] + [bridge], es[3:6]
                                    tr = random.Random(lay_seed)
                                    steps_a = [sent.format(pre=("" if i == 0 else tr.choice(JF.PRE[1:])), o=oa, e=e) for i, e in enumerate(seq_a)]
                                    steps_b = [sent.format(pre=("" if i == 0 else tr.choice(JF.PRE[1:])), o=ob, e=e) for i, e in enumerate(seq_b)]
                                    binds, ia, ib = [], 0, 0
                                    while ia < 3 or ib < 3:
                                        if ib == 3 or (ia < 3 and tr.random() < 0.5):
                                            binds.append(cap(steps_a[ia])); ia += 1  # noqa: E702
                                        else:
                                            binds.append(cap(steps_b[ib])); ib += 1  # noqa: E702
                                    btrip, bkeys = [], set()
                                else:  # M W R: the other entities are bound to people; the bridge is not
                                    binds = [t["bind"][w].format(p=p, x=e, X=cap(e)) for p, e in zip(persons[1:], es[1:], strict=True)]
                                    btrip = [(p, tri["bind"], e) for p, e in zip(persons[1:], es[1:], strict=True)]
                                    bkeys = set()
                                r2 = random.Random(lay_seed)
                                if start in ("Q", "J"):
                                    ctx = records(genre, "table" if start == "Q" else "json", btrip + trip, para, r2)
                                elif start == "T":
                                    fin_s = r2.sample(fin, len(fin))
                                    merged, ia, ib = [], 0, 0
                                    while ia < len(binds) or ib < len(fin_s):
                                        if ib == len(fin_s) or (ia < len(binds) and r2.random() < len(binds) / (len(binds) + len(fin_s))):
                                            merged.append(binds[ia]); ia += 1  # noqa: E702
                                        else:
                                            merged.append(fin_s[ib]); ib += 1  # noqa: E702
                                    ctx = JF.splice(r2, genre, merged, para, shuffle=False)
                                else:
                                    allf = binds + fin
                                    kidx = set(bkeys) | {len(binds) + i for i in keys}
                                    ctx = splice(r2, genre, allf, para, kidx, knobs["key_early"])
                                present = bool(words_in(ctx, [ans]))
                                n_bridge = len(re.findall(r"(?i)\b" + re.escape(bridge) + r"\b", ctx))
                                if F in "MN":
                                    assert not present, (rel, bridge, start, F, ans)
                                if F == "A":
                                    assert present, (rel, bridge, F)
                                if F == "N":
                                    assert not words_in(ctx, vocab), (rel, words_in(ctx, vocab))
                                if start == "R":
                                    assert n_bridge == 0, (rel, bridge, F)
                                else:
                                    assert n_bridge >= 1, (rel, bridge, start, F)
                                q2f = q2
                                if F in "EF":
                                    q2f = "According to the notes, " + (q2.replace("{D}", "{d}") if q2.startswith("{D}") else q2[0].lower() + q2[1:])
                                whole = q2f.format(d=d1, D=cap(d1))
                                word = wstart + F
                                it = {
                                    "id": f"j3:chat:facts:{word}-L{level}-r{rep}-{k:05d}", "module": "facts", "word": word,
                                    "start": wstart, "final": F, "final_source": src, "control": F, "domain": rel, "relation": rel,
                                    "format": {"Q": "table", "J": "json"}.get(start, "prose"), "genre": genre, "framing": "chat",
                                    "wording": w, "popularity": facts[bridge][2], "split": "test", "half": halves[bridge],
                                    "context": ctx, "question": whole, "answer": ans, "answer_aliases": alias_of.get(ans, []),
                                    "kind": "open", "answer_kind": "open", "answer_vocab": vocab, "answer_in_passage": present,
                                    "bridge_in_passage": n_bridge > 0, "bridge_mentions": n_bridge,
                                    "steps": [{"question": q1, "answer": bridge, "kind": "open", "source": start,
                                               "alts": sorted({bridge, *meta[bridge].get("bridge_alts", [])})},
                                              {"question": t["q2M"][w].format(d=bridge, D=cap(bridge)), "answer": breal, "kind": "open",
                                               "source": "M", "cand_vocab": vocab}],
                                    "bridge": bridge, "bridges": [bridge], "start_desc": d1, "desc_index": di,
                                    "skip_cue": meta[bridge]["skip_cues"][di] if start in ("M", "W", "R") else None,
                                    "guess_question": q2f.format(d=gd, D=cap(gd)),
                                    "scene": f"j3:{rel}:{start}-L{level}-{x}-r{rep}", "level": level, "knobs": knobs, "rep": rep,
                                    "numbers": "words", "c_op": expr, "entities": es, "real": breal,
                                    "memory_answer": mem, "conflict_value": cf if F in "CDEF" else None,
                                    "cf_near": cf_near if F in "CDEF" else None, "attributed": F in "DFG",
                                    "according_question": F in "EF", "anchors": [anc[e] for e in es] if F == "H" else None,
                                    "distractor_mention": d2 if start == "W" else None, "name_reveals_answer": meta[bridge]["name_reveals_answer"],
                                    "eponymous": False, "pair_of": (f"j3:chat:facts:P{F}-L{level}-r{rep}-{k:05d}" if wstart == "Y" else None),
                                }  # fmt: skip
                                items.append(it)
    return items


def probe_items(tabs: dict) -> list[dict]:
    """Closed-book skip-the-bridge probes: the final relation asked of the description's named cue (no passage)."""
    qt = {"people": "Which nationality is most associated with {c}?", "films": "Which film director is most associated with {c}?"}
    out = []
    for rel, t in tabs.items():
        vocab = sorted({v[0] for v in t["facts"].values()})
        for x, row in sorted(t["meta"].items()):
            for di, cue in enumerate(row["skip_cues"]):
                if not cue:
                    continue
                q = qt.get(rel, "Which country is most associated with {c}?").format(c=cue)
                out.append({"id": f"j3:probe:{rel}:{x}:{di}", "module": "probes", "word": "SK", "domain": rel, "relation": rel,
                            "format": "prose", "framing": "chat", "context": "", "question": q, "answer": row["answer"],
                            "answer_aliases": row["answer_aliases"], "kind": "open", "answer_kind": "open", "answer_vocab": vocab,
                            "bridge": x, "desc_index": di, "skip_cue": cue, "steps": [], "scene": f"j3:probe:{rel}:{x}:{di}",
                            "level": 1, "split": "test"})  # fmt: skip
    return out


def main(a) -> None:
    rng = random.Random(a.seed)
    tabs = T3.tables()
    strip = lambda e: e[4:] if e.startswith("the ") else e  # noqa: E731
    banned = {strip(b) for t in tabs.values() for b in t["facts"]} | {v[0] for t in tabs.values() for v in t["facts"].values()}
    banned |= {al for t in tabs.values() for r in t["meta"].values() for al in r["answer_aliases"]}
    banned |= {w for n in NP.PEOPLE_NAMES + N.ABSENT_NAMES for w in n.split()}
    banned |= {w for xs in CONT.values() for w in xs}
    banned |= {"Olympic", "Olympics", "continent", "nationality", "director", "film", "films", "company", "landmark", "list",
               "handout", "festival", "tour", "podcast", "exhibition"}  # fmt: skip
    deck = Deck(rng, JF.clean_paras(banned))
    items = facts_items(rng, tabs, deck, a.reps)
    probes = probe_items(tabs)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out = DATA / f"{a.name}_test_chat"
    assert not out.exists(), f"{out} exists; sets are written once"
    out.mkdir(parents=True)
    allit = items + probes
    ids = [it["id"] for it in allit]
    assert len(ids) == len(set(ids)), "duplicate ids"
    (out / "items.jsonl").write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in allit))
    man = {"set": out.name, "seed": a.seed, "reps": a.reps, "n": len(allit), "git_commit": commit, "script": "scripts/jsuite_v3.py",
           "matrix": MATRIX, "levels": {str(k): v for k, v in LEVELS3.items()},
           "words": dict(collections.Counter(it["word"] for it in allit)),
           "relations": dict(collections.Counter(it["relation"] for it in items)),
           "bridges": {rel: len(t["facts"]) for rel, t in tabs.items()}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(man, indent=2) + "\n")
    print(out.name, json.dumps({k: man[k] for k in ("n", "relations", "bridges")}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--seed", type=int, default=3001)
    ap.add_argument("--reps", type=int, default=2)
    main(ap.parse_args())
