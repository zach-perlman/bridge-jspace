"""jsuite_v2 (Zach, 2026-10-24, prereg amendment 33): the combined suite, version 2. ONE dataset holding every module
(field "module"); the only separate sets are the split (dev for band choice, test) and, derived later, the framings
(natural_v1.py derive-qa / derive-prefill), since a run uses one split and one framing.

Modules:
  facts     two-hop fact chains (module 1 redesigned, below); words S+F, S in P M T, F in P K M A N (15 words)
  threehop  natural3's three-hop chains (cities / people -> country -> continent; jsuite_threehop's drops); words PPP..MMM
  numbers   jsuite_numbers' numbers as intermediates; its words SF prefixed "n" (nPR nPL nPM ... nMM) so no word is shared
            across modules
Eligibility is per module (facts: the scene rule; threehop and numbers: per item), set by the word subset a run uses.

Facts, changes from v1 (the dataset audit of 2026-10-24):
  - 8 relations (scripts/jsuite_v2_tables.py REL2): countries -> continent, countries -> language, people -> nationality,
    cities -> country, companies -> country, landmarks -> country, dishes -> country, animals -> class; one scene per
    bridge, level and start (v1: 3 relations, 65 bridges, 2 scenes each).
  - Finals P (a new fictional fact; values from the answer vocabulary), K (the true fact stated), M (recall: other
    entities carry fictional-relation values from the answer vocabulary, never the bridge's, so they can act as lures),
    A (as M, one other entity carries the bridge's real value), N (new: recall with no answer-vocabulary word anywhere in
    the passage: every final-hop sentence is a neutral sentence; M - N measures lure capture).
  - The bridge is named the same number of times in every final of a start: in P and K by its own final-hop sentence, in
    M, A and N by a neutral sentence (v1: P/K passages named it twice, M/A once; the recalled start's MP/MK passages named
    it and MM/MA never did).
  - Test bridges in two halves (A, B) by relation and popularity: an independent replication on disjoint facts.
  - Filler: WikiText runs dealt without replacement (cycled), not drawn with replacement.
  - Primary contrast M - K (same question, same answer; the fact recalled vs stated).

python scripts/jsuite_v2.py --name jsuite_v2 --seed 2601 [--scenes 1] [--threehop-scenes 2] [--numbers-reps 8]
  [--split-from jsuite_v2]   (2026-10-25, amendment 38: a second rendering keeps that set's facts dev / test split and test
  halves exactly; only the passages, filler, wordings and orders are redrawn with --seed)
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import jsuite_facts as JF  # noqa: E402
from scripts import jsuite_numbers as JN  # noqa: E402
from scripts import jsuite_v2_tables as TB  # noqa: E402
from scripts import natplus as NP  # noqa: E402
from scripts import natural3 as N3  # noqa: E402
from scripts import natural_v1 as N  # noqa: E402

DATA = N.DATA
FINALS = "PKMAN"
cap = JF.cap


class Deck:
    """Filler runs of at least `need` sentences, dealt without replacement and reshuffled when exhausted."""

    def __init__(self, rng: random.Random, paras: list[list[str]]):
        self.rng, self.paras, self.decks = rng, paras, {}

    def deal(self, need: int) -> list[str]:
        d = self.decks.setdefault(need, [])
        if not d:
            d.extend(p for p in self.paras if len(p) >= need)
            self.rng.shuffle(d)
        run = d.pop()
        st = self.rng.randrange(len(run) - need + 1)
        return run[st : st + need]


def split_halves(rng: random.Random, facts: dict) -> tuple[dict[str, str], dict[str, str]]:
    """dev / test per relation and popularity (alternate, shuffled), and the test bridges' halves A / B."""
    split, half = {}, {}
    for pop in ("popular", "rare"):
        xs = sorted(x for x, v in facts.items() if v[2] == pop)
        rng.shuffle(xs)
        test = []
        for i, x in enumerate(xs):
            split[x] = "dev" if i % 2 else "test"
            if split[x] == "test":
                test.append(x)
        for i, x in enumerate(test):
            half[x] = "AB"[i % 2]
    return split, half


def words_in(text: str, words: list[str]) -> list[str]:
    return [w for w in words if re.search(r"(?i)\b" + re.escape(w) + r"\b", text)]


def imposed_splits(name: str) -> dict[str, tuple[dict[str, str], dict[str, str]]]:
    """relation -> (split, half) of an existing set's facts module (both splits)."""
    out: dict = collections.defaultdict(lambda: ({}, {}))
    for sp in ("dev", "test"):
        for line in (DATA / f"{name}_{sp}_chat" / "items.jsonl").read_text().splitlines():
            it = json.loads(line)
            if it.get("module") == "facts":
                out[it["relation"]][0][it["bridge"]] = it["split"]
                if it.get("half"):
                    out[it["relation"]][1][it["bridge"]] = it["half"]
    return dict(out)


def facts_items(rng: random.Random, n_scenes: int, deck: Deck, imposed: dict | None = None) -> tuple[dict[str, list[dict]], dict[str, str]]:
    items, split_of = {"dev": [], "test": []}, {}
    k = 0
    for rel, t in TB.REL2.items():
        facts = t["facts"]
        if imposed is not None:
            split, half = imposed[rel]
            assert set(split) == set(facts), f"{rel}: the imposed split does not cover the facts"
        else:
            split, half = split_halves(rng, facts)
        split_of.update({f"{rel}:{x}": s for x, s in split.items()})
        vocab = sorted({v[0] for v in facts.values()})
        people = rel == "people"
        objs, sent, tdesc, tq = t["track"]
        for level, knobs in N.LEVELS.items():
            for x in sorted(facts):
                for rep in range(n_scenes):
                    for group in "PMT":
                        k += 1
                        w = rng.randrange(3)
                        real = facts[x][0]
                        pool = [e for e in facts if e != x and split[e] == split[x]]
                        rng.shuffle(pool)
                        pool.sort(key=lambda o: facts[o][0] == real)  # entities sharing the bridge's answer last
                        n_ent = 6 if group == "T" else knobs["entities"]
                        ents = [x] + pool[: n_ent - 1]
                        persons = rng.sample(NP.PEOPLE_NAMES, len(ents))
                        newv = {e: rng.choice([a for a in vocab if a != facts[e][0]]) for e in ents}
                        avoid = {e: rng.choice([a for a in vocab if a not in (facts[e][0], real)]) for e in ents[1:]}
                        carrier = next((e for e in ents[1:] if facts[e][0] != real), None)
                        if carrier is None or len(vocab) < 3:
                            continue
                        genre = rng.choice(sorted(N.GENRES))
                        para = deck.deal(knobs["filler"])
                        order_seed = rng.random()
                        noun, rel_desc = rng.choice(facts[x][1])
                        if group == "P":
                            d1, q1 = t["pdesc"][w].format(p=persons[0]), t["q1P"][w].format(p=persons[0])
                            binds = [t["bind"][w].format(p=p, x=e, X=cap(e)) for p, e in zip(persons, ents, strict=True)]
                            gd = t["pdesc"][w].format(p=rng.choice(N.ABSENT_NAMES))
                        elif group == "M":
                            d1, q1 = JF.m_desc(noun, rel_desc, people)
                            binds = [t["bind"][w].format(p=p, x=e, X=cap(e)) for p, e in zip(persons[1:], ents[1:], strict=True)]
                            gd = t["unknown"]
                        else:
                            oa, ob = rng.sample(objs, 2)
                            seq_a, seq_b = ents[1:3] + [x], ents[3:6]
                            steps_a = [sent.format(pre=("" if i == 0 else rng.choice(JF.PRE[1:])), o=oa, e=e) for i, e in enumerate(seq_a)]
                            steps_b = [sent.format(pre=("" if i == 0 else rng.choice(JF.PRE[1:])), o=ob, e=e) for i, e in enumerate(seq_b)]
                            merged, ia, ib = [], 0, 0
                            while ia < 3 or ib < 3:
                                if ib == 3 or (ia < 3 and rng.random() < 0.5):
                                    merged.append(steps_a[ia]); ia += 1  # noqa: E702
                                else:
                                    merged.append(steps_b[ib]); ib += 1  # noqa: E702
                            binds = [cap(s) for s in merged]
                            d1, q1 = tdesc.format(o=oa), tq.format(o=oa)
                            gd = tdesc.format(o=rng.choice([o for o in objs if o not in (oa, ob)]))
                        pf = lambda e, a: t["pfact"][w].format(x=e, X=cap(e), a=a, al=a.lower(), an=N.an(a))  # noqa: E731
                        kf = lambda e: t["kfact"][w].format(x=e, X=cap(e), a=facts[e][0], al=facts[e][0].lower(), an=N.an(facts[e][0]))  # noqa: E731
                        nf = lambda e: t["nfact"][w].format(x=e, X=cap(e))  # noqa: E731
                        for F in FINALS:
                            if F == "P":
                                src, ans, fin = "P", newv[x], [pf(e, newv[e]) for e in ents]
                            elif F == "K":
                                src, ans, fin = "M", real, [kf(e) for e in ents]
                            elif F == "M":
                                src, ans, fin = "M", real, [pf(e, avoid[e]) for e in ents[1:]] + [nf(x)]
                            elif F == "A":
                                src, ans = "M", real
                                fin = [pf(e, real if e == carrier else avoid[e]) for e in ents[1:]] + [nf(x)]
                            else:
                                src, ans, fin = "M", real, [nf(e) for e in ents]
                            r2 = random.Random(order_seed)
                            if group == "T":
                                fin_s = r2.sample(fin, len(fin))
                                merged_f, ia, ib = [], 0, 0
                                while ia < len(binds) or ib < len(fin_s):
                                    if ib == len(fin_s) or (ia < len(binds) and r2.random() < len(binds) / (len(binds) + len(fin_s))):
                                        merged_f.append(binds[ia]); ia += 1  # noqa: E702
                                    else:
                                        merged_f.append(fin_s[ib]); ib += 1  # noqa: E702
                                ctx = JF.splice(r2, genre, merged_f, para, shuffle=False)
                            else:
                                ctx = JF.splice(r2, genre, binds + fin, para, shuffle=True)
                            present = bool(words_in(ctx, [ans]))
                            n_bridge = len(re.findall(r"(?i)\b" + re.escape(x) + r"\b", ctx))
                            assert F not in "MN" or not present, (rel, x, F, ans)
                            assert F != "A" or present, (rel, x, F)
                            assert F != "N" or not words_in(ctx, vocab), (rel, x, words_in(ctx, vocab))
                            q2 = t["q2P"][w] if F == "P" else t["q2M"][w]
                            whole = q2.format(d=d1, D=cap(d1))
                            sp = split[x]
                            items[sp].append({
                                "id": f"j2:chat:facts:{group}{F}-L{level}-{k:05d}", "module": "facts", "word": group + F,
                                "start": group, "final": F, "final_source": src, "control": F, "domain": rel, "relation": rel,
                                "format": "prose", "genre": genre, "framing": "chat", "wording": w, "popularity": facts[x][2],
                                "split": sp, "half": half.get(x), "context": ctx, "question": whole, "answer": ans,
                                "kind": "open", "answer_kind": "open", "answer_vocab": vocab, "answer_in_passage": present,
                                "bridge_in_passage": n_bridge > 0, "bridge_mentions": n_bridge,
                                "steps": [{"question": q1, "answer": x, "kind": "open", "source": group,
                                           "alts": sorted({x, *TB.ALT.get(rel, {}).get(x, []), TB.FIRST_NAMES.get(x, N.FIRST_NAMES.get(x, x))})},
                                          {"question": q2.format(d=x, D=cap(x)), "answer": ans, "kind": "open", "source": F,
                                           "cand_vocab": vocab}],
                                "bridge": x, "bridges": [x], "start_desc": d1, "guess_question": q2.format(d=gd, D=cap(gd)),
                                "scene": f"j2:{rel}:{group}-L{level}-{x}-{rep}", "level": level, "knobs": knobs,
                                "numbers": "words", "c_op": None, "entities": ents, "real": real,
                                "eponymous": x in TB.EPONYMOUS.get(rel, []),  # the answer readable off the name (France -> French)
                            })  # fmt: skip
    return items, split_of


def module_items(fn, tmp: Path) -> list[dict]:
    """Run another module's generator into a temporary data dir and return its items."""
    for mod in (N3, JN):
        mod.DATA = tmp
    fn()
    out = []
    for d in sorted(tmp.iterdir()):
        if (d / "items.jsonl").exists():
            out += [json.loads(line) for line in (d / "items.jsonl").read_text().splitlines()]
    for mod in (N3, JN):
        mod.DATA = DATA
    return out


def main(a) -> None:
    rng = random.Random(a.seed)
    strip = lambda e: e[4:] if e.startswith("the ") else e  # noqa: E731
    banned = {strip(b) for t in TB.REL2.values() for b in t["facts"]} | {v[0] for t in TB.REL2.values() for v in t["facts"].values()}
    banned |= {w for ws in TB.DERIV.values() for w in ws} | {a for alts in TB.ALT.values() for xs in alts.values() for a in xs}
    banned |= {w for n in NP.PEOPLE_NAMES + N.ABSENT_NAMES for w in n.split()}
    banned |= {"Olympic", "Olympics", "continent", "exhibition", "podcast", "tour", "language", "cuisine", "dish", "company"}
    deck = Deck(rng, JF.clean_paras(banned))
    items, split_of = facts_items(rng, a.scenes, deck, imposed_splits(a.split_from) if a.split_from else None)
    # three-hop: jsuite_threehop's drops, natural3's generator; the split by the first bridge when it is a facts bridge
    with tempfile.TemporaryDirectory() as td:
        dropped = {"cities": [c for c, v in N3.CITIES.items() if v[0] == "South Africa"],
                   "people": [p for p, v in N3.PEOPLE.items() if v[0] == "South Africa"]}  # fmt: skip
        for c in dropped["cities"]:
            del N3.CITIES[c]
        for p in dropped["people"]:
            del N3.PEOPLE[p]
        N3.CONT.pop("South Africa", None)
        th = module_items(lambda: N3.make("j2three", a.seed + 1, a.threehop_scenes), Path(td))
    for it in th:
        first = it.get("bridges", [it.get("bridge")])[0]
        rel = "cities" if first in N3.CITIES else "people"
        sp = split_of.get(f"{rel}:{first}") or ("dev" if random.Random(it["scene"]).random() < 0.5 else "test")
        it.update(module="threehop", split=sp, half=None, id=it["id"].replace("nat3:", "j2:").replace(":chat:", ":chat:three:"))
        items[sp].append(it)
    with tempfile.TemporaryDirectory() as td:
        nu = module_items(lambda: JN.make("j2num", a.seed + 2, a.numbers_reps), Path(td))
    for it in nu:
        sp = "dev" if random.Random(it["scene"]).random() < 0.5 else "test"
        it.update(module="numbers", word="n" + it["word"], split=sp, half=None, id=it["id"].replace("jn:chat:", "j2:chat:num:"))
        items[sp].append(it)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    for sp, its in items.items():
        ids = [it["id"] for it in its]
        assert len(ids) == len(set(ids)), "duplicate ids"
        out = DATA / f"{a.name}_{sp}_chat"
        assert not out.exists(), f"{out} exists; sets are written once"
        out.mkdir(parents=True)
        (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in its))
        man = {"set": out.name, "seed": a.seed, "split_from": a.split_from, "split": sp, "n": len(its), "git_commit": commit, "script": "scripts/jsuite_v2.py",
               "modules": dict(collections.Counter(it["module"] for it in its)),
               "words": dict(collections.Counter(it["word"] for it in its)),
               "relations": dict(collections.Counter(it["relation"] for it in its if it["module"] == "facts")),
               "bridges": len({it["bridge"] for it in its if it["module"] == "facts"}),
               "halves": dict(collections.Counter(it["half"] for it in its if it["module"] == "facts")),
               "scenes_per_bridge": a.scenes, "threehop_scenes": a.threehop_scenes, "numbers_reps": a.numbers_reps,
               "threehop_dropped": dropped}  # fmt: skip
        (out / "manifest.json").write_text(json.dumps(man, indent=2) + "\n")
        print(out.name, json.dumps({k: man[k] for k in ("n", "modules", "relations", "bridges", "halves")}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--seed", type=int, default=2601)
    ap.add_argument("--scenes", type=int, default=1)
    ap.add_argument("--threehop-scenes", type=int, default=2)
    ap.add_argument("--numbers-reps", type=int, default=8)
    ap.add_argument("--split-from", help="keep this set's facts split and halves (a second rendering)")
    main(ap.parse_args())
