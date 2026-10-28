"""jsuite_v4 (Zach, 2026-10-28, prereg amendment 58 note 14): a latent first hop whose bridge must be used.

Each item: a passage giving six entities of one relation (the bridge X and five others, all sharing one role noun) one
made-up value each ("The upcoming biopic casts a Swedish actor as Achebe."), and a question that names X only by a
description ("Which nationality is the actor cast as the person who wrote Arrow of God in the new film?"). The answer is
X's passage value: arbitrary per scene, so no remembered association reaches it, and the role noun alone cannot pick X.
Words (one item each; a scene per item):
  MP  the lookup: X's passage value (final P)
  MM  its recall twin on the identical passage and description: X's remembered attribute (final M)
  H1  hop 1 closed book: "Which person wrote Arrow of God?" with no passage (recall of the bridge)
  RG  hop 1 by recognition: "Which of the people mentioned above wrote Arrow of God?" (with the passage)
  RO  role noun only: the MP question with the description cut to "the person" (chance 1/6)
MP and MM also carry hop 1 (with the passage), hop 2 alone (the bridge named) and the no-description guess.
Design (Zach's answers, 28 Oct):
  - six entities per scene; people use the generic role "person";
  - values from the relation's answer vocabulary (shared with the remembered attributes), never an entity's own
    attribute and never X's;
  - two binding relations per entity type, one per wording;
  - the bridge's fact rotated through the six positions;
  - descriptions whose words share a 4-letter stem with any scene entity's name are excluded (X) or resampled away
    (others); fillers re-dealt while they contain a description word.
Every entity's descriptions are stored (entity_descs) for counterfactual prompts (scripts/nn_cf.py).

python scripts/jsuite_v4.py [--seed 4001] [--name jsuite_v4]   -> data/tasks_v2/jsuite_v4_test_chat
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

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT)]
import jsuite_v3 as V3  # noqa: E402
import jsuite_v3_tables as T3  # noqa: E402

DATA = ROOT / "data" / "tasks_v2"
K = 6  # entities per scene
N_FILLER = 6
PRON = {"people": "who", "cities": "that", "companies": "that", "landmarks": "that", "films": "that"}
PLURAL = {"people": "people", "cities": "cities", "companies": "companies", "landmarks": "landmarks", "films": "films"}
# wording 0: v3's binding relation (pfact[1] / q2P[1]); wording 1: a second made-up relation
REL2 = {
    "people": ("The new podcast about {x} is hosted by {an} {a} journalist.", "Which nationality is the journalist who hosts the new podcast about {d}?"),
    "cities": ("This year's student delegation to {x} comes from {a}.", "Which country does this year's student delegation to {d} come from?"),
    "companies": ("{X}'s new packaging supplier is based in {a}.", "In which country is the new packaging supplier of {d} based?"),
    "landmarks": ("The touring exhibition about {x} opens next in {a}.", "In which country does the touring exhibition about {d} open next?"),
    "films": ("The stage adaptation of {x} will be directed by {a}.", "Who will direct the stage adaptation of {d}?"),
}  # fmt: skip
STOP = {"the", "a", "an", "of", "who", "that", "which", "was", "is", "in", "to", "by", "and", "for", "with", "on", "at", "as", "from",
        "his", "her", "its", "their", "it", "this", "were", "be", "has", "have", "had"}


def article(a: str) -> str:
    return "an" if a[0].lower() in "aeiou" else "a"


def fact(tpl: str, e: str, a: str) -> str:
    return V3.sentence(tpl.format(x=e, X=V3.sentence(e), a=V3.disp(a), an=article(a)))


def stems(text: str) -> set[str]:
    return {w.lower()[:4] for w in re.findall(r"[A-Za-z]+", text) if len(w) >= 4 and w.lower() not in STOP}


def splice(rng: random.Random, genre: str, facts: list[str], para: list[str]) -> str:
    """The facts in the given order, interleaved with the filler at random boundaries (as jsuite_v3.splice)."""
    slots = sorted(rng.choices(range(len(para) + 1), k=len(facts)))
    body, fi = [], 0
    for b in range(len(para) + 1):
        while fi < len(facts) and slots[fi] == b:
            body.append(facts[fi])
            fi += 1
        if b < len(para):
            body.append(para[b])
    head, tail = V3.N.GENRES[genre]
    if genre == "notes":
        return head + "\n" + "\n".join("- " + s for s in body) + "\n" + tail
    sep = "\n\n" if genre == "email" else "\n"
    return head + sep + " ".join(body) + sep + tail


def main(a) -> None:
    rng = random.Random(a.seed)
    tabs = T3.tables()
    table = json.loads((ROOT / "data" / "v3_bridges.json").read_text())
    alias_of = {r["answer"]: r.get("answer_aliases") or [] for r in table}
    rows = {(r["relation"], r["bridge"]): r for r in table}
    strip = lambda e: e[4:] if e.startswith("the ") else e  # noqa: E731
    banned = {strip(b) for t in tabs.values() for b in t["facts"]} | {v[0] for t in tabs.values() for v in t["facts"].values()}
    banned |= {al for t in tabs.values() for r in t["meta"].values() for al in r["answer_aliases"]}
    banned |= {w for n in V3.NP.PEOPLE_NAMES + V3.N.ABSENT_NAMES for w in n.split()}
    banned |= {w for xs in V3.CONT.values() for w in xs}
    banned |= {"Olympic", "Olympics", "continent", "nationality", "director", "film", "films", "company", "landmark", "list",
               "handout", "festival", "tour", "podcast", "exhibition", "delegation", "supplier", "adaptation", "biopic", "actor",
               "journalist", "twin", "twinning", "studio", "documentary", "office"}  # fmt: skip
    deck = V3.Deck(rng, V3.JF.clean_paras(banned))
    items, skipped = [], collections.Counter()
    k = 0
    for rel in ("people", "cities", "companies", "landmarks", "films"):
        t = tabs[rel]
        noun = "person" if rel == "people" else t["noun"]
        vocab = sorted({v[0] for v in t["facts"].values()})
        bridges = sorted(b for (r, b) in rows if r == rel)
        desc_of = {b: [f"the {noun} {PRON[rel]} {d['clause']}" for d in rows[(rel, b)]["descriptions"]] for b in bridges}
        clause_of = {b: [d["clause"] for d in rows[(rel, b)]["descriptions"]] for b in bridges}
        pos_counter = collections.Counter()
        for x in bridges:
            real_x = t["facts"][x][0]
            for di, clause in enumerate(clause_of[x]):
                desc = desc_of[x][di]
                if stems(clause) & stems(x):
                    skipped["X shares a stem with its description"] += 1
                    continue
                for w in (0, 1):
                    fact_tpl, q_tpl = (t["pfact"][1], t["q2P"][1]) if w == 0 else REL2[rel]
                    ok = [b for b in bridges if b != x and not (stems(clause) & stems(b)) and not (stems(x) & stems(b))]
                    if len(ok) < K - 1:
                        skipped["too few distractors"] += 1
                        continue
                    others = rng.sample(ok, K - 1)
                    ents = [x, *others]
                    vals = None
                    for _ in range(200):  # distinct values, none an entity's own attribute, none X's attribute
                        cand = rng.sample([v for v in vocab if v != real_x], K)
                        if all(cand[i] != t["facts"][e][0] for i, e in enumerate(ents)):
                            vals = dict(zip(ents, cand, strict=True))
                            break
                    if vals is None:
                        skipped["no value draw"] += 1
                        continue
                    for _ in range(50):  # filler free of description words
                        para = deck.deal(N_FILLER)
                        if not (stems(" ".join(para)) & stems(clause)):
                            break
                    else:
                        skipped["filler leak"] += 1
                        continue
                    pos = pos_counter[(rel, w)] % K  # the bridge's fact rotated through the six positions
                    pos_counter[(rel, w)] += 1
                    order = [e for e in ents if e != x]
                    rng.shuffle(order)
                    order.insert(pos, x)
                    genre = rng.choice(sorted(V3.N.GENRES))
                    ctx = splice(rng, genre, [fact(fact_tpl, e, vals[e]) for e in order], para)
                    assert all(len(re.findall(r"(?i)\b" + re.escape(e) + r"\b", ctx)) == 1 for e in ents), (x, ctx)
                    assert not V3.words_in(ctx, [real_x]), (x, real_x)
                    q1 = t["q1M"][1].format(noun=noun, rel=clause)
                    q_mp = q_tpl.format(d=desc, D=V3.sentence(desc))
                    q_mm = t["q2M"][1 - w].format(d=desc, D=V3.sentence(desc))
                    alts = sorted({x, *rows[(rel, x)].get("bridge_alts", [])})
                    base = {"module": "facts", "start": "M", "domain": rel, "relation": rel, "format": "prose", "genre": genre,
                            "framing": "chat", "wording": w, "rep": w, "level": 2, "split": "test", "popularity": t["facts"][x][2],
                            "half": "A", "context": ctx, "kind": "open", "answer_kind": "open", "answer_vocab": vocab,
                            "bridge": x, "bridges": [x], "start_desc": desc, "desc_index": di, "skip_cue": None, "real": real_x,
                            "entities": order, "passage_values": vals, "bridge_position": pos, "eponymous": False,
                            "name_reveals_answer": rows[(rel, x)].get("name_reveals_answer", False), "bridge_in_passage": True,
                            "bridge_mentions": 1, "entity_descs": {e: desc_of[e] for e in ents},
                            "knobs": {"entities": K, "filler": N_FILLER}, "set_version": "v4"}  # fmt: skip
                    hop1 = {"question": q1, "answer": x, "kind": "open", "source": "M", "alts": alts}
                    uid = f"{k:05d}"
                    items.append({**base, "id": f"j3:chat:v4:MP-w{w}-{uid}", "word": "MP", "final": "P", "final_source": "P", "control": "P",
                                  "scene": f"v4:MP:{uid}", "question": q_mp, "answer": vals[x], "answer_aliases": alias_of.get(vals[x], []),
                                  "answer_in_passage": True, "memory_answer": real_x,
                                  "steps": [hop1, {"question": q_tpl.format(d=x, D=V3.sentence(x)), "answer": vals[x], "kind": "open",
                                                   "source": "P", "cand_vocab": vocab}],
                                  "guess_question": q_tpl.format(d=t["unknown"], D=V3.sentence(t["unknown"]))})  # fmt: skip
                    items.append({**base, "id": f"j3:chat:v4:MM-w{w}-{uid}", "word": "MM", "final": "M", "final_source": "M", "control": "M",
                                  "scene": f"v4:MM:{uid}", "question": q_mm, "answer": real_x, "answer_aliases": alias_of.get(real_x, []),
                                  "answer_in_passage": False, "memory_answer": real_x,
                                  "steps": [hop1, {"question": t["q2M"][1 - w].format(d=x, D=V3.sentence(x)), "answer": real_x, "kind": "open",
                                                   "source": "M", "cand_vocab": vocab}],
                                  "guess_question": t["q2M"][1 - w].format(d=t["unknown"], D=V3.sentence(t["unknown"]))})  # fmt: skip
                    ctrl = {**base, "answer_in_passage": False, "steps": [], "guess_question": None, "memory_answer": real_x}
                    items.append({**ctrl, "id": f"j3:chat:v4:H1-w{w}-{uid}", "word": "H1", "final": "B", "final_source": "M", "control": "H1",
                                  "scene": f"v4:H1:{uid}", "context": "", "question": q1, "answer": x, "answer_aliases": alts,
                                  "answer_vocab": bridges})  # fmt: skip
                    items.append({**ctrl, "id": f"j3:chat:v4:RG-w{w}-{uid}", "word": "RG", "final": "B", "final_source": "P", "control": "RG",
                                  "scene": f"v4:RG:{uid}", "question": f"Which of the {PLURAL[rel]} mentioned above {clause}?", "answer": x,
                                  "answer_aliases": alts, "answer_vocab": bridges})  # fmt: skip
                    role = f"the {noun}"
                    items.append({**ctrl, "id": f"j3:chat:v4:RO-w{w}-{uid}", "word": "RO", "final": "P", "final_source": "P", "control": "RO",
                                  "scene": f"v4:RO:{uid}", "question": q_tpl.format(d=role, D=V3.sentence(role)), "answer": vals[x],
                                  "answer_aliases": alias_of.get(vals[x], []), "answer_in_passage": True})  # fmt: skip
                    k += 1
    out = DATA / f"{a.name}_test_chat"
    assert not out.exists(), f"{out} exists; sets are written once"
    out.mkdir(parents=True)
    ids = [it["id"] for it in items]
    assert len(ids) == len(set(ids)), "duplicate ids"
    (out / "items.jsonl").write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    man = {"set": out.name, "seed": a.seed, "n": len(items), "scenes": k, "git_commit": commit, "script": "scripts/jsuite_v4.py",
           "words": dict(collections.Counter(it["word"] for it in items)), "skipped": dict(skipped),
           "relations": dict(collections.Counter(it["relation"] for it in items if it["word"] == "MP"))}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(man, indent=2) + "\n")
    print(json.dumps(man, indent=1))
    for wd in ("MP", "MM", "H1", "RG", "RO"):
        x = next(i for i in items if i["word"] == wd)
        print(f"--- {wd}: {x['question']} -> {x['answer']}")
    print(items[0]["context"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=4001)
    ap.add_argument("--name", default="jsuite_v4")
    main(ap.parse_args())
