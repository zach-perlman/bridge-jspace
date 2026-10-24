"""jsuite_facts (Zach, 2026-10-23, prereg amendment 23): module 1 of the combined suite, fact chains.

Relations: country -> continent, person -> nationality, city -> country (natplus's tables, popular and rare; animals
dropped: their prompt answers needed a case change). Words SF, start S then final hop F:
  S  P  read: a fictional person's binding in the passage gives the bridge ("Paul Whitaker was raised in Argentina")
     M  recalled: an indirect description ("the country that won the first FIFA World Cup in 1930")
     T  tracked (story memory): two objects move through places in interleaved sentences; the bridge is where one of
        them went last ("the country the sculpture exhibition went to last"); order is the only cue (no "finally")
  F  P  a new fact about every entity in the passage (never the real value); the answer is the bridge's
     K  the true fact about every entity stated in the passage
     M  recall: final-hop facts for the other entities only, none with the bridge's real value (the answer word absent)
     A  as M, but one other entity's fact carries the bridge's real value (the answer word present once)
The four finals of a chain share one scene and differ only in their final-hop sentences (natctl's design), so no
recall passage gives the bridge a value of the asked relation (natplus's PM lure) and M has the answer absent by
construction. Bridges are split per relation and popularity into dev and test halves (sets *_dev_chat, *_test_chat):
bands are chosen on dev only. Question templates fixed for grammar; filler is consecutive WikiText sentences that end
in . ! or ?, ASCII only, no digits. Hop 1 is checked at competence by generation (natural_v1 competence --hop1 gen),
since bridge names share first tokens in every tokenizer; final answers have distinct first tokens in all six.

python scripts/jsuite_facts.py --name jsuite_v1_facts --seed 2301 [--scenes 2] [--split-from jsuite_v1_facts]
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

from scripts import natctl as NC  # noqa: E402
from scripts import natplus as NP  # noqa: E402
from scripts import natural_v1 as N  # noqa: E402

DATA = N.DATA
RELS = ("countries", "people", "cities")
Q2M = {  # the true relation, three wordings (natplus's "Which continent is {d} on?" dropped)
    "countries": ["On which continent is {d}?", "Which continent is {d} in?", "{D} is on which continent?"],
    "people": ["What was the nationality of {d}?", "Which nationality was {d}?", "{D} was of which nationality?"],
    "cities": ["In which country is {d}?", "Which country is {d} in?", "{D} is in which country?"],
}
TRACK = {  # objects, the step sentence, the descriptor of where object o went last, the hop-1 question
    "countries": (["sculpture exhibition", "textile exhibition", "photography exhibition", "ceramics exhibition"],
                  "{pre}the {o} went to {e}.", "the country the {o} went to last", "Which country did the {o} go to last?"),
    "people": (["history podcast", "culture podcast", "biography podcast", "radio series"],
               "{pre}the {o} ran an episode on {e}.", "the person the {o} ran its latest episode on",
               "Who did the {o} run its latest episode on?"),
    "cities": (["jazz tour", "ballet tour", "circus tour", "choir tour"], "{pre}the {o} stopped in {e}.",
               "the city the {o} stopped in last", "Which city did the {o} stop in last?"),
}  # fmt: skip
PRE = ("", "Then ", "Next, ", "After that, ")
WORDS = tuple(s + f for s in "PMT" for f in "PKMA")


def cap(s: str) -> str:
    return s[0].upper() + s[1:]


def clean_paras(banned: set[str]) -> list[list[str]]:
    """natplus's real paragraphs, keeping runs of sentences that end in . ! ?, are ASCII and have no digits."""
    out = []
    for run in NP.real_paragraphs(banned):
        cur = []
        for s in run:
            s = re.sub(r"(\d) ?: ?(\d)", r"\1:\2", s)
            if s[-1] in ".!?" and s.isascii() and not re.search(r"\d", s):
                cur.append(s)
            else:
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
        if len(cur) >= 2:
            out.append(cur)
    return out


def splice(rng: random.Random, genre: str, facts: list[str], para: list[str], shuffle: bool) -> str:
    """The real sentences in order with the facts spliced in at random boundaries; the facts' own order is kept
    when shuffle is False (tracked sequences)."""
    facts = facts[:]
    if shuffle:
        rng.shuffle(facts)
    slots = sorted(rng.choices(range(len(para) + 1), k=len(facts)))
    body, fi = [], 0
    for i in range(len(para) + 1):
        while fi < len(facts) and slots[fi] == i:
            body.append(facts[fi])
            fi += 1
        if i < len(para):
            body.append(para[i])
    head, tail = N.GENRES[genre]
    if genre == "notes":
        return head + "\n" + "\n".join("- " + s for s in body) + "\n" + tail
    sep = "\n\n" if genre == "email" else "\n"
    return head + sep + " ".join(body) + sep + tail


def m_desc(noun: str, rel: str, people: bool) -> tuple[str, str]:
    """(descriptor, hop-1 question) for a recalled start; "is where ..." relations read "the country where ..."."""
    if rel.startswith("is where "):
        rest = rel[len("is where ") :]
        return f"the {noun} where {rest}", f"Which {noun} is the one where {rest}?"
    return f"the {noun} {'who' if people else 'that'} {rel}", f"Which {noun} {rel}?"


def split_bridges(rng: random.Random, facts: dict) -> dict[str, str]:
    """Each relation's bridges, per popularity stratum, alternately into dev and test (shuffled)."""
    out = {}
    for pop in ("popular", "rare"):
        xs = sorted(x for x, v in facts.items() if v[2] == pop)
        rng.shuffle(xs)
        for i, x in enumerate(xs):
            out[x] = "dev" if i % 2 else "test"
    return out


def make(name: str, seed: int, n_scenes: int, split_from: str | None = None) -> None:
    rng = random.Random(seed)
    banned = {b for t in NP.TYPES.values() for b in t["facts"]} | {v[0] for t in NP.TYPES.values() for v in t["facts"].values()}
    banned |= {w for n in NP.PEOPLE_NAMES + N.ABSENT_NAMES for w in n.split()} | {"Olympic", "Olympics", "continent", "exhibition", "podcast", "tour"}
    paras = clean_paras(banned)
    items = {"dev": [], "test": []}
    fixed_split = {}
    if split_from:
        for sp in ("dev", "test"):
            for line in (DATA / f"{split_from}_{sp}_chat" / "items.jsonl").read_text().splitlines():
                fixed_split[json.loads(line)["bridge"]] = sp
    k = 0
    for tname in RELS:
        t = NP.TYPES[tname]
        facts = t["facts"]
        split = split_bridges(rng, facts)
        if split_from:  # a rendering seed of an existing set: its dev/test split, the bridges unchanged
            split = {x: sp for x, sp in fixed_split.items() if x in facts}
            assert set(split) == set(facts), set(facts) ^ set(split)
        vocab = sorted({v[0] for v in facts.values()})
        people = tname == "people"
        for level, knobs in N.LEVELS.items():
            for x in sorted(facts):
                for rep in range(n_scenes):
                    for group in "PMT":
                        k += 1
                        w = rng.randrange(3)
                        real = facts[x][0]
                        pool = [e for e in facts if e != x and split[e] == split[x]]  # distractors from the same split
                        rng.shuffle(pool)
                        pool.sort(key=lambda o: facts[o][0] == real)  # other real answers first
                        n_ent = 6 if group == "T" else knobs["entities"]
                        ents = [x] + pool[: n_ent - 1]
                        persons = rng.sample(NP.PEOPLE_NAMES, len(ents))
                        newv = {e: rng.choice([a for a in vocab if a != facts[e][0]]) for e in ents}
                        avoid = {e: rng.choice([a for a in vocab if a not in (facts[e][0], real)]) for e in ents[1:]}
                        carrier = next((e for e in ents[1:] if facts[e][0] != real), None)
                        if carrier is None:
                            continue
                        genre = rng.choice(sorted(N.GENRES))
                        run_ = rng.choice([p for p in paras if len(p) >= knobs["filler"]])
                        st = rng.randrange(len(run_) - knobs["filler"] + 1)
                        para = run_[st : st + knobs["filler"]]
                        order_seed = rng.random()
                        noun, rel = rng.choice(facts[x][1])
                        if group == "P":
                            d1, q1 = t["pdesc"][w].format(p=persons[0]), t["q1P"][w].format(p=persons[0])
                            binds = [t["bind"][w].format(p=p, x=e) for p, e in zip(persons, ents, strict=True)]
                            gd = t["pdesc"][w].format(p=rng.choice(N.ABSENT_NAMES))
                        elif group == "M":
                            d1, q1 = m_desc(noun, rel, people)
                            binds = [t["bind"][w].format(p=p, x=e) for p, e in zip(persons[1:], ents[1:], strict=True)]
                            gd = t["unknown"]
                        else:  # T: two objects, three stops each, interleaved; the bridge is object A's last stop
                            objs, sent, desc, q = TRACK[tname]
                            oa, ob = rng.sample(objs, 2)
                            seq_a, seq_b = ents[1:3] + [x], ents[3:6]
                            steps_a = [sent.format(pre=("" if i == 0 else rng.choice(PRE[1:])), o=oa, e=e) for i, e in enumerate(seq_a)]
                            steps_b = [sent.format(pre=("" if i == 0 else rng.choice(PRE[1:])), o=ob, e=e) for i, e in enumerate(seq_b)]
                            merged, ia, ib = [], 0, 0
                            while ia < 3 or ib < 3:
                                if ib == 3 or (ia < 3 and rng.random() < 0.5):
                                    merged.append(steps_a[ia]); ia += 1  # noqa: E702
                                else:
                                    merged.append(steps_b[ib]); ib += 1  # noqa: E702
                            binds = [cap(s) for s in merged]
                            d1, q1, gd = desc.format(o=oa), q.format(o=oa), desc.format(o=rng.choice([o for o in objs if o not in (oa, ob)]))
                        pf = lambda e, a: t["pfact"][w].format(x=e, X=cap(e), a=a, al=a.lower(), an=N.an(a))  # noqa: E731
                        for F in "PKMA":
                            if F == "P":
                                final, ans, fin = "P", newv[x], [pf(e, newv[e]) for e in ents]
                            elif F == "K":
                                final, ans, fin = "M", real, [NC.KFACT[tname][w].format(x=e, a=facts[e][0]) for e in ents]
                            elif F == "M":
                                final, ans, fin = "M", real, [pf(e, avoid[e]) for e in ents[1:]]
                            else:
                                final, ans = "M", real
                                fin = [pf(e, real if e == carrier else avoid[e]) for e in ents[1:]]
                            r2 = random.Random(order_seed)
                            if group == "T":  # tracked steps keep their order; final-hop facts interleave at random
                                fin_s = r2.sample(fin, len(fin))
                                merged_f, ia, ib = [], 0, 0
                                while ia < len(binds) or ib < len(fin_s):
                                    if ib == len(fin_s) or (ia < len(binds) and r2.random() < len(binds) / (len(binds) + len(fin_s))):
                                        merged_f.append(binds[ia]); ia += 1  # noqa: E702
                                    else:
                                        merged_f.append(fin_s[ib]); ib += 1  # noqa: E702
                                ctx = splice(r2, genre, merged_f, para, shuffle=False)
                            else:
                                ctx = splice(r2, genre, binds + fin, para, shuffle=True)
                            present = re.search(r"\b" + re.escape(ans) + r"\b", ctx) is not None
                            bridge_in = re.search(r"\b" + re.escape(x) + r"\b", ctx) is not None
                            assert F != "M" or not present, (x, F, ans)
                            assert F != "A" or ctx.count(ans) >= 1
                            assert not (group == "M" and F in "MA") or not bridge_in, (x, F)
                            q2 = (t["q2P"][w] if final == "P" else Q2M[tname][w])
                            whole = q2.format(d=d1, D=cap(d1))
                            items[split[x]].append({
                                "id": f"js:facts:{group}{F}-L{level}-{k:05d}", "word": group + F, "start": group, "final": F,
                                "final_source": final, "control": F, "domain": tname, "format": "prose", "genre": genre,
                                "framing": "chat", "wording": w, "popularity": facts[x][2], "split": split[x], "context": ctx,
                                "question": whole, "answer": ans, "kind": "open", "answer_kind": "open", "answer_vocab": vocab,
                                "answer_in_passage": present, "bridge_in_passage": bridge_in,
                                "steps": [{"question": q1, "answer": x, "kind": "open", "source": group,
                                           "alts": sorted({x, N.FIRST_NAMES.get(x, x)})},
                                          {"question": q2.format(d=x, D=x), "answer": ans, "kind": "open", "source": F,
                                           "cand_vocab": vocab}],
                                "bridge": x, "bridges": [x], "start_desc": d1,
                                "guess_question": q2.format(d=gd, D=cap(gd)),
                                "scene": f"js:{tname}:{group}-L{level}-{x}-{rep}", "level": level, "knobs": knobs,
                                "numbers": "words", "c_op": None, "chance_same_answer": 0.0, "entities": ents, "real": real,
                            })  # fmt: skip
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    for sp, its in items.items():
        out = DATA / f"{name}_{sp}_chat"
        assert not out.exists(), f"{out} exists; sets are written once"
        out.mkdir(parents=True)
        (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in its))
        (out / "manifest.json").write_text(json.dumps({"set": out.name, "seed": seed, "scenes_per_bridge": n_scenes,
                                                       "split": sp, "split_from": split_from, "n": len(its), "git_commit": commit,
                                                       "script": "scripts/jsuite_facts.py"}, indent=2) + "\n")  # fmt: skip
        print(f"{out.name}: {len(its)} items", dict(collections.Counter(it["word"] for it in its)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--seed", type=int, default=2301)
    ap.add_argument("--scenes", type=int, default=2)
    ap.add_argument("--split-from", default=None, help="reuse an existing set's dev/test bridge split (a rendering seed)")
    a = ap.parse_args()
    make(a.name, a.seed, a.scenes, a.split_from)
