"""jsuite_v4cc (Zach, 2026-10-29, prereg amendment 58 note 24): v4's people items with cue-conflict descriptions, to block the
memory twin's shortcut.

In v4 a description's own words can point at the memory twin's answer without the person ("the person who wrote Things
Fall Apart" -> Nigerian). Here every bridge has two descriptions:
  conflict  its most salient association is another nationality (the cue), so a shortcut gives a wrong answer
            ("the person who wrote A Passage to India": cue Indian, answer English)
  aligned   its association is the person's own nationality ("the person who wrote Howards End")
A right memory answer on a conflict description needs the person; a cue answer is the shortcut caught. Same person, two
description types: the comparison is within person.
Everything else is v4's (scripts/jsuite_v4.py): six people per scene with made-up values from the nationality vocabulary,
the two binding wordings, the bridge's fact rotated through the positions, stem exclusions, MP / MM / H1 / RG / RO.
Distractors are drawn from these bridges and v4's people. People outside v3's tables carry their facts on the item
(extra_facts; scripts/jswap.table). Facts are well known and were checked by hand when written; the model's own hop 1
(H1) and hop 2 alone gate them per model.

python scripts/jsuite_v4cc.py [--seed 4101] -> data/tasks_v2/jsuite_v4cc_test_chat (MP, MM), data/tasks_v2/jsuite_v4ctlcc_test_chat
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
import jsuite_v4 as V4  # noqa: E402

DATA = ROOT / "data" / "tasks_v2"
# name, nationality, other names, conflict clause, its cue, aligned clause
CC = [
    ("Forster", "English", ["E. M. Forster"], "wrote A Passage to India", "Indian", "wrote Howards End"),
    ("Kipling", "English", ["Rudyard Kipling"], "wrote The Jungle Book, set in the jungles of India", "Indian", "wrote Puck of Pook's Hill, set in Sussex"),
    ("Mann", "German", ["Thomas Mann"], "wrote Death in Venice", "Italian", "wrote Buddenbrooks, about a merchant family in Lübeck"),
    ("Bizet", "French", ["Georges Bizet"], "composed the opera Carmen, set in Seville", "Spanish", "composed L'Arlésienne, set in Provence"),
    ("Puccini", "Italian", ["Giacomo Puccini"], "composed the opera Madama Butterfly, set in Nagasaki", "Japanese", "composed the opera Tosca, set in Rome"),
    ("Verdi", "Italian", ["Giuseppe Verdi"], "composed the opera Aida, set in ancient Egypt", "Egyptian", "composed the opera Rigoletto, set in Mantua"),
    ("Rossini", "Italian", ["Gioachino Rossini"], "composed the opera The Barber of Seville", "Spanish", "was born in the Adriatic town of Pesaro"),
    ("Mendelssohn", "German", ["Felix Mendelssohn"], "composed the Italian Symphony", "Italian", "founded the Leipzig Conservatory"),
    ("Ravel", "French", ["Maurice Ravel"], "composed the Spanish-flavoured Boléro", "Spanish", "composed Le Tombeau de Couperin"),
    ("Rimsky-Korsakov", "Russian", ["Nikolai Rimsky-Korsakov"], "composed the Capriccio Espagnol", "Spanish", "composed the opera The Tale of Tsar Saltan"),
    ("Tchaikovsky", "Russian", ["Pyotr Tchaikovsky"], "composed the Capriccio Italien", "Italian", "composed the 1812 Overture"),
    ("Haydn", "Austrian", ["Joseph Haydn"], "composed the London symphonies", "English", "composed the Austrian imperial anthem"),
    ("Mozart", "Austrian", ["Wolfgang Amadeus Mozart"], "composed The Marriage of Figaro, set near Seville", "Spanish",
     "served as court musician to the Prince-Archbishop of Salzburg"),
    ("Dvorak", "Czech", ["Dvořák", "Antonín Dvořák"], "composed the New World Symphony while living in America", "American", "composed the Slavonic Dances"),
    ("Shakespeare", "English", ["William Shakespeare"], "wrote Hamlet, about a prince of Denmark", "Danish", "wrote the history play Henry V"),
    ("Hemingway", "American", ["Ernest Hemingway"], "wrote For Whom the Bell Tolls, set in the Spanish Civil War", "Spanish", "was born in Oak Park, Illinois"),
    ("Christie", "English", ["Agatha Christie"], "wrote Death on the Nile", "Egyptian", "created the village sleuth Miss Marple"),
    ("Byron", "English", ["Lord Byron"], "died at Missolonghi while supporting the Greek War of Independence", "Greek", "took his seat in the House of Lords"),
    ("Van Gogh", "Dutch", ["Vincent van Gogh"], "painted sunflowers in Arles in the south of France", "French", "painted The Potato Eaters, about peasants in Nuenen"),
    ("Picasso", "Spanish", ["Pablo Picasso"], "co-founded Cubism in Paris", "French", "painted Guernica, about a Basque town bombed in the Spanish Civil War"),
    ("Leone", "Italian", ["Sergio Leone"], "directed westerns set in the American Old West", "American", "began his career at Rome's Cinecittà studios"),
    ("Hitchcock", "English", ["Alfred Hitchcock"], "directed Psycho and Vertigo in Hollywood", "American", "directed The Lady Vanishes for a London studio"),
    ("Lloyd Webber", "English", ["Andrew Lloyd Webber", "Webber"], "composed the musical Evita, about Argentina's first lady", "Argentine",
     "was knighted by Queen Elizabeth II"),
    ("Sullivan", "English", ["Arthur Sullivan"], "composed the comic opera The Mikado, set in Japan", "Japanese", "partnered with Gilbert at London's Savoy Theatre"),
    ("Irving", "American", ["Washington Irving"], "wrote Tales of the Alhambra", "Spanish", "wrote The Legend of Sleepy Hollow"),
    ("Wilde", "Irish", ["Oscar Wilde"], "wrote The Picture of Dorian Gray, set in London", "English", "was born in Dublin"),
    ("Forman", "Czech", ["Miloš Forman", "Milos Forman"], "directed Amadeus, about the Austrian composer Mozart", "Austrian", "led the Czechoslovak New Wave"),
    ("Luhrmann", "Australian", ["Baz Luhrmann"], "directed Moulin Rouge!, set in Paris", "French", "directed the film Australia"),
    ("Twain", "American", ["Mark Twain"], "wrote The Prince and the Pauper, set in Tudor England", "English",
     "wrote Adventures of Huckleberry Finn, set along the Mississippi"),
    ("Utzon", "Danish", ["Jørn Utzon"], "designed the Sydney Opera House", "Australian", "designed Bagsværd Church near Copenhagen"),
    ("Bartholdi", "French", ["Frédéric Bartholdi"], "designed the Statue of Liberty in New York Harbor", "American", "sculpted the Lion of Belfort"),
    ("Pearl Buck", "American", ["Buck", "Pearl S. Buck"], "wrote The Good Earth, about a Chinese farmer", "Chinese", "was born in Hillsboro, West Virginia"),
    ("Blixen", "Danish", ["Karen Blixen", "Isak Dinesen"], "wrote Out of Africa, about her coffee farm in Kenya", "Kenyan", "lived at Rungstedlund, north of Copenhagen"),
    ("Lean", "English", ["David Lean"], "directed Doctor Zhivago, set in revolutionary Russia", "Russian", "directed Brief Encounter, set at an English railway station"),
    ("Greene", "English", ["Graham Greene"], "wrote The Quiet American", "American", "wrote Brighton Rock"),
    ("Chopin", "Polish", ["Frédéric Chopin"], "spent most of his career in Paris", "French", "composed polonaises and mazurkas"),
    ("Canaletto", "Italian", [], "painted views of London and the Thames", "English", "painted the canals of Venice"),
    ("Holbein", "German", ["Hans Holbein"], "was court painter to Henry VIII of England", "English", "was born in Augsburg"),
    ("Columbus", "Italian", ["Christopher Columbus"], "sailed for the Spanish crown", "Spanish", "was born in Genoa"),
    ("Magellan", "Portuguese", ["Ferdinand Magellan"], "led a Spanish expedition around the world", "Spanish", "served in the Portuguese navy in Africa and Asia"),
    ("Vespucci", "Italian", ["Amerigo Vespucci"], "gave his name to the Americas", "American", "was born in Florence"),
    ("Cuarón", "Mexican", ["Cuaron", "Alfonso Cuarón"], "directed Harry Potter and the Prisoner of Azkaban", "English", "directed Roma, set in Mexico City"),
    ("del Toro", "Mexican", ["Guillermo del Toro", "Toro"], "directed Pan's Labyrinth, set in Francoist Spain", "Spanish", "was born in Guadalajara"),
    ("von Trier", "Danish", ["Lars von Trier", "Trier"], "directed Dancer in the Dark, set in America", "American", "co-founded the Dogme 95 movement in Copenhagen"),
    ("Wenders", "German", ["Wim Wenders"], "directed Paris, Texas", "American", "directed Wings of Desire, set in Berlin"),
    ("Verhoeven", "Dutch", ["Paul Verhoeven"], "directed RoboCop, set in Detroit", "American", "directed Soldier of Orange, about the Dutch resistance"),
    ("Bertolucci", "Italian", ["Bernardo Bertolucci"], "directed The Last Emperor, about China's Puyi", "Chinese", "directed The Conformist, set in Fascist Italy"),
    ("Garbo", "Swedish", ["Greta Garbo"], "was a star of Hollywood's MGM studio", "American", "was born in Stockholm"),
    ("Chaplin", "English", ["Charlie Chaplin"], "made his films in Hollywood", "American", "was born in London"),
    ("Marco Polo", "Italian", ["Polo"], "served at the court of Kublai Khan", "Chinese", "was born in Venice"),
]


def main(a) -> None:
    rng = random.Random(a.seed)
    tabs = T3.tables()
    t = tabs["people"]
    table = json.loads((ROOT / "data" / "v3_bridges.json").read_text())
    alias_of = {r["answer"]: r.get("answer_aliases") or [] for r in table}
    vocab = sorted({v[0] for v in t["facts"].values()})
    cc = {name: {"nat": nat, "alts": alts, "descs": [conf, ali], "types": ["conflict", "aligned"], "cue": cue} for name, nat, alts, conf, cue, ali in CC}
    for name, r in cc.items():
        assert r["nat"] in vocab and r["cue"] in vocab and r["cue"] != r["nat"], name
        if name in t["facts"]:
            assert t["facts"][name][0] == r["nat"], (name, t["facts"][name][0], r["nat"])
    old = {b: t["facts"][b][0] for b in t["facts"] if b not in cc}
    v3desc = {r["bridge"]: [d["clause"] for d in r["descriptions"]] for r in table if r["relation"] == "people"}
    nat = {**old, **{n: r["nat"] for n, r in cc.items()}}
    clauses = {**{b: v3desc.get(b, []) for b in old}, **{n: r["descs"] for n, r in cc.items()}}
    pool = sorted(nat)
    noun = "person"
    desc_of = {b: [f"the {noun} who {c}" for c in clauses[b]] for b in pool}
    extra = {n: [r["nat"], [], "cc"] for n, r in cc.items() if n not in t["facts"]}
    strip = lambda e: e[4:] if e.startswith("the ") else e  # noqa: E731  (v4's filler bans, plus these bridges' names)
    banned = {strip(b) for tt in tabs.values() for b in tt["facts"]} | {v[0] for tt in tabs.values() for v in tt["facts"].values()}
    banned |= {al for tt in tabs.values() for r in tt["meta"].values() for al in r["answer_aliases"]}
    banned |= {w for n in V3.NP.PEOPLE_NAMES + V3.N.ABSENT_NAMES for w in n.split()}
    banned |= {w for xs in V3.CONT.values() for w in xs} | {w for n in pool for w in n.split()} | set(vocab)
    banned |= {"Olympic", "Olympics", "continent", "nationality", "film", "films", "podcast", "biopic", "actor", "journalist"}
    deck = V3.Deck(rng, V3.JF.clean_paras(banned))
    items, skipped = [], collections.Counter()
    k, pos_counter = 0, collections.Counter()
    for x in sorted(cc):
        real_x = cc[x]["nat"]
        for di, clause in enumerate(cc[x]["descs"]):
            desc = desc_of[x][di]
            if V4.stems(clause) & V4.stems(x):
                skipped["X shares a stem with its description"] += 1
                continue
            for w in (0, 1):
                fact_tpl, q_tpl = (t["pfact"][1], t["q2P"][1]) if w == 0 else V4.REL2["people"]
                ok = [b for b in pool if b != x and not (V4.stems(clause) & V4.stems(b)) and not (V4.stems(x) & V4.stems(b))]
                others = rng.sample(ok, V4.K - 1)
                ents = [x, *others]
                vals = None
                for _ in range(200):  # distinct values, none an entity's own nationality, none X's, never X's cue
                    cand = rng.sample([v for v in vocab if v not in (real_x, cc[x]["cue"])], V4.K)
                    if all(cand[i] != nat[e] for i, e in enumerate(ents)):
                        vals = dict(zip(ents, cand, strict=True))
                        break
                if vals is None:
                    skipped["no value draw"] += 1
                    continue
                for _ in range(50):
                    para = deck.deal(V4.N_FILLER)
                    if not (V4.stems(" ".join(para)) & V4.stems(clause)):
                        break
                else:
                    skipped["filler leak"] += 1
                    continue
                pos = pos_counter[w] % V4.K
                pos_counter[w] += 1
                order = [e for e in ents if e != x]
                rng.shuffle(order)
                order.insert(pos, x)
                genre = rng.choice(sorted(V3.N.GENRES))
                ctx = V4.splice(rng, genre, [V4.fact(fact_tpl, e, vals[e]) for e in order], para)
                if not all(len(re.findall(r"(?i)\b" + re.escape(e) + r"\b", ctx)) == 1 for e in ents):
                    skipped["an entity name not exactly once"] += 1
                    continue
                if V3.words_in(ctx, [real_x]):
                    skipped["X's nationality in the passage"] += 1
                    continue
                q1 = t["q1M"][1].format(noun=noun, rel=clause)
                q_mp = q_tpl.format(d=desc, D=V3.sentence(desc))
                q_mm = t["q2M"][1 - w].format(d=desc, D=V3.sentence(desc))
                alts = sorted({x, *cc[x]["alts"]})
                base = {"module": "facts", "start": "M", "domain": "people", "relation": "people", "format": "prose", "genre": genre,
                        "framing": "chat", "wording": w, "rep": w, "level": 2, "split": "test", "popularity": "cc", "half": "A", "context": ctx,
                        "kind": "open", "answer_kind": "open", "answer_vocab": vocab, "bridge": x, "bridges": [x], "start_desc": desc,
                        "desc_index": di, "cc_type": cc[x]["types"][di], "cue": cc[x]["cue"] if di == 0 else None, "skip_cue": None,
                        "real": real_x, "entities": order, "passage_values": vals, "bridge_position": pos, "eponymous": False,
                        "name_reveals_answer": False, "bridge_in_passage": True, "bridge_mentions": 1,
                        "entity_descs": {e: desc_of[e] for e in ents}, "extra_facts": {e: extra[e] for e in ents if e in extra},
                        "knobs": {"entities": V4.K, "filler": V4.N_FILLER}, "set_version": "v4", "subset": "cc"}  # fmt: skip
                hop1 = {"question": q1, "answer": x, "kind": "open", "source": "M", "alts": alts}
                uid = f"{k:05d}"
                items.append({**base, "id": f"j3:chat:v4cc:MP-w{w}-{uid}", "word": "MP", "final": "P", "final_source": "P", "control": "P",
                              "scene": f"v4cc:MP:{uid}", "question": q_mp, "answer": vals[x], "answer_aliases": alias_of.get(vals[x], []),
                              "answer_in_passage": True, "memory_answer": real_x,
                              "steps": [hop1, {"question": q_tpl.format(d=x, D=V3.sentence(x)), "answer": vals[x], "kind": "open", "source": "P",
                                               "cand_vocab": vocab}],
                              "guess_question": q_tpl.format(d=t["unknown"], D=V3.sentence(t["unknown"]))})  # fmt: skip
                items.append({**base, "id": f"j3:chat:v4cc:MM-w{w}-{uid}", "word": "MM", "final": "M", "final_source": "M", "control": "M",
                              "scene": f"v4cc:MM:{uid}", "question": q_mm, "answer": real_x, "answer_aliases": alias_of.get(real_x, []),
                              "answer_in_passage": False, "memory_answer": real_x,
                              "steps": [hop1, {"question": t["q2M"][1 - w].format(d=x, D=V3.sentence(x)), "answer": real_x, "kind": "open",
                                               "source": "M", "cand_vocab": vocab}],
                              "guess_question": t["q2M"][1 - w].format(d=t["unknown"], D=V3.sentence(t["unknown"]))})  # fmt: skip
                ctrl = {**base, "answer_in_passage": False, "steps": [], "guess_question": None, "memory_answer": real_x}
                items.append({**ctrl, "id": f"j3:chat:v4cc:H1-w{w}-{uid}", "word": "H1", "final": "B", "final_source": "M", "control": "H1",
                              "scene": f"v4cc:H1:{uid}", "context": "", "question": q1, "answer": x, "answer_aliases": alts, "answer_vocab": pool})  # fmt: skip
                items.append({**ctrl, "id": f"j3:chat:v4cc:RG-w{w}-{uid}", "word": "RG", "final": "B", "final_source": "P", "control": "RG",
                              "scene": f"v4cc:RG:{uid}", "question": f"Which of the people mentioned above {clause}?", "answer": x,
                              "answer_aliases": alts, "answer_vocab": pool})  # fmt: skip
                items.append({**ctrl, "id": f"j3:chat:v4cc:RO-w{w}-{uid}", "word": "RO", "final": "P", "final_source": "P", "control": "RO",
                              "scene": f"v4cc:RO:{uid}", "question": q_tpl.format(d="the person", D=V3.sentence("the person")), "answer": vals[x],
                              "answer_aliases": alias_of.get(vals[x], []), "answer_in_passage": True})  # fmt: skip
                k += 1
    ids = [it["id"] for it in items]
    assert len(ids) == len(set(ids)), "duplicate ids"
    out, ctl = DATA / f"{a.name}_test_chat", DATA / "jsuite_v4ctlcc_test_chat"  # the controls' name v4_split expects
    for d in (out, ctl):
        assert not d.exists(), f"{d} exists; sets are written once"
        d.mkdir(parents=True)
    (out / "items.jsonl").write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items if it["word"] in ("MP", "MM")))
    (ctl / "items.jsonl").write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items if it["word"] not in ("MP", "MM")))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    man = {"set": out.name, "seed": a.seed, "n": len(items), "scenes": k, "bridges": len(cc), "git_commit": commit, "script": "scripts/jsuite_v4cc.py",
           "words": dict(collections.Counter(it["word"] for it in items)), "skipped": dict(skipped),
           "cc_types": dict(collections.Counter(it["cc_type"] for it in items if it["word"] == "MM"))}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(man, indent=2) + "\n")
    print(json.dumps(man, indent=1))
    for wd in ("MP", "MM", "H1", "RG", "RO"):
        x = next(i for i in items if i["word"] == wd)
        print(f"--- {wd} ({x['cc_type']}): {x['question']} -> {x['answer']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=4101)
    ap.add_argument("--name", default="jsuite_v4cc")
    main(ap.parse_args())
