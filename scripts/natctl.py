"""natctl (Zach, 2026-10-23, prereg amendment 16): what the knock-out's memory-final loss is about.

natural_v1 / natplus compare a prompt-final hop (a NEW fact read from the passage) with a memory-final hop (a KNOWN
fact recalled), so "prompt vs memory" is confounded with "new vs known fact" and with "is the answer word in the
prompt" (observationally, memory-final items whose answer word happens to sit in the passage lose 15-25 points less).
natctl crosses them, with the same chains and questions as natplus (countries -> continent, people -> nationality,
cities -> country; popular and rare bridges; three wordings; coherent passages; chat framing). Final hop F:
  P  the passage states a new fact about every entity (never the real value); the answer is the bridge's (natplus P)
  K  the passage states the TRUE fact about every entity ("Peru is in South America."); the question asks the real
     property, the same question as M
  M  recall: no final-hop fact about the bridge, distractor entities' new facts only, the answer word nowhere in the
     passage
  A  as M, but exactly one distractor's new fact has the answer word as its value (the answer is copyable)
Start S: P (a fictional person's binding) or M (an indirect description; the bridge is in the passage only when the
final hop is keyed by it, F in P/K). Words SF: PP, PK, PM, PA, MP, MK, MM, MA. Readings: K vs M (does stating the true
fact rescue recall?), A vs M (answer availability by design), K vs P (a known vs a new fact, both in the prompt).
Animals are left out (their prompt answers need a case change). Items carry answer_vocab for the candidate read. The
four final-hop versions of a chain share one scene (same passage otherwise), so eligibility (every prompt of the
scene right) compares P, K, M and A on the same chains.

python scripts/natctl.py --name natctl_v1 --seed 1201
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

from scripts import natplus as NP  # noqa: E402
from scripts import natural_v1 as N  # noqa: E402

DATA = N.DATA
KFACT = {  # the true fact, stated with the answer verbatim
    "countries": ["{x} is in {a}.", "{x} lies in {a}.", "{x} is a country in {a}."],
    "people": ["{x} was {a}.", "By nationality, {x} was {a}.", "{x} was {a} by birth."],
    "cities": ["{x} is in {a}.", "{x} is a city in {a}.", "{x} lies in {a}."],
}
WORDS = ("PP", "PK", "PM", "PA", "MP", "MK", "MM", "MA")


def make(name: str, seed: int, n_scenes: int) -> None:
    rng = random.Random(seed)
    types = {k: v for k, v in NP.TYPES.items() if k in KFACT}
    banned = {b for t in NP.TYPES.values() for b in t["facts"]} | {v[0] for t in NP.TYPES.values() for v in t["facts"].values()}
    banned |= {w for n in NP.PEOPLE_NAMES + N.ABSENT_NAMES for w in n.split()} | {"Olympic", "Olympics", "continent", "zoo"}
    paras = [[re.sub(r"(\d) ?: ?(\d)", r"\1:\2", s_) for s_ in run] for run in NP.real_paragraphs(banned)]
    items, k = [], 0
    for tname, t in types.items():
        facts = t["facts"]
        vocab = sorted({v[0] for v in facts.values()})
        for level, knobs in N.LEVELS.items():
            for x in sorted(facts):
                for rep in range(n_scenes):
                    for group in ("P", "M"):
                        k += 1
                        w = rng.randrange(3)
                        real = facts[x][0]
                        others = sorted(set(facts) - {x})
                        rng.shuffle(others)
                        others.sort(key=lambda o: facts[o][0] == real)  # distractors with other real answers first
                        ents = [x] + others[: knobs["entities"] - 1]
                        persons = rng.sample(NP.PEOPLE_NAMES, len(ents))
                        newv = {e: rng.choice([a for a in vocab if a != facts[e][0]]) for e in ents}  # new facts (P)
                        # distractor new facts that avoid the bridge's real answer (M), and one that carries it (A)
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
                        else:
                            d1 = f"the {noun} {'who' if tname == 'people' else 'that'} {rel}"
                            q1 = t["q1M"][w].format(noun=noun, rel=rel)
                            binds = [t["bind"][w].format(p=p, x=e) for p, e in zip(persons[1:], ents[1:], strict=True)]
                        pf = lambda e, a: t["pfact"][w].format(x=e, X=e[0].upper() + e[1:], a=a, al=a.lower(), an=N.an(a))  # noqa: E731
                        cap = lambda s_: s_[0].upper() + s_[1:]  # noqa: E731
                        for F in ("P", "K", "M", "A"):
                            if F == "P":
                                final, ans, fin_facts = "P", newv[x], [pf(e, newv[e]) for e in ents]
                            elif F == "K":
                                final, ans, fin_facts = "M", real, [KFACT[tname][w].format(x=e, a=facts[e][0]) for e in ents]
                            elif F == "M":
                                final, ans, fin_facts = "M", real, [pf(e, avoid[e]) for e in ents[1:]]
                            else:
                                final, ans = "M", real
                                fin_facts = [pf(e, real if e == carrier else avoid[e]) for e in ents[1:]]
                            ctx = NP.passage(random.Random(order_seed), genre, binds + fin_facts, para)
                            present = re.search(r"\b" + re.escape(ans) + r"\b", ctx) is not None
                            bridge_in = re.search(r"\b" + re.escape(x) + r"\b", ctx) is not None
                            assert F not in ("M",) or not present, (x, F, ans)
                            assert F != "A" or ctx.count(ans) >= 1
                            assert not (group == "M" and F in ("M", "A")) or not bridge_in, (x, F)
                            q2 = t["q2" + final][w]
                            whole = q2.format(d=d1, D=cap(d1))
                            same = [e for e in ents[1:] if ((newv[e] if F == "P" else facts[e][0]) == ans)]
                            items.append({
                                "id": f"nc:chat:{group}{F}-L{level}-{k:04d}", "word": group + F, "final_source": final,
                                "control": F, "domain": tname, "format": "prose", "genre": genre, "framing": "chat",
                                "wording": w, "popularity": facts[x][2], "context": ctx, "question": whole, "answer": ans,
                                "kind": "open", "answer_kind": "open", "answer_vocab": vocab, "answer_in_passage": present,
                                "steps": [{"question": q1, "answer": x, "kind": "open", "source": group,
                                           "alts": sorted({x, N.FIRST_NAMES.get(x, x)})},
                                          {"question": q2.format(d=x, D=x), "answer": ans, "kind": "open", "source": F,
                                           "cand_vocab": vocab}],
                                "bridge": x, "bridges": [x], "start_desc": d1,
                                "guess_question": q2.format(d=t["unknown"], D=cap(t["unknown"])),
                                "scene": f"nc:{tname}:{group}-L{level}-{x}-{rep}", "level": level, "knobs": knobs,  # one scene for P/K/M/A
                                "numbers": "words", "c_op": None,
                                "chance_same_answer": round(len(same) / max(1, len(ents) - 1), 3),
                                "entities": ents, "real": real,
                            })  # fmt: skip
    out = DATA / f"{name}_chat"
    assert not out.exists(), f"{out} exists; sets are written once"
    out.mkdir(parents=True)
    (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "manifest.json").write_text(json.dumps({"set": out.name, "seed": seed, "n": len(items), "git_commit": commit,
                                                   "script": "scripts/natctl.py"}, indent=2) + "\n")  # fmt: skip
    print(f"{out.name}: {len(items)} items", dict(collections.Counter(it["word"] for it in items)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--seed", type=int, default=1201)
    ap.add_argument("--scenes", type=int, default=1)
    a = ap.parse_args()
    make(a.name, a.seed, a.scenes)
