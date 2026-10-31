"""jsuite_v5al (Zach, 2026-10-29, prereg amendment 60 note 31): the bridge from the context.

v4's scenes (scripts/jsuite_v4.py) with the description of X replaced by an in-context codename. Each scene: six
entities of one relation, each with one made-up value via v4's fact templates ("The upcoming biopic casts a Swedish
actor as Achebe."), plus one binding sentence per entity ("Achebe goes by the codename Zorbel."), spliced into v4's
filler like the facts. The question names X only by its codename ("Which nationality is the actor cast as the person
codenamed Zorbel in the new film?"), so hop 1 (codename -> X) can only be read from the passage, and the answer is X's
passage value (MP) or X's remembered attribute (MM).
Words (one item each; a scene per item; ids j3:chat:v5al:<word>-w<wording>-<5 digits>):
  MP  the lookup: X's made-up passage value (final P)
  MM  its recall twin on the identical passage and codename: X's remembered attribute (final M)
  H1  (controls set) hop 1 WITH the passage: "Which person is codenamed Zorbel?" (the codename exists only there)
  RO  (controls set) role noun only: the MP question with "the person" (chance 1/6), as v4
MP and MM carry hop 1 (with the passage), v4's named hop 2, and the guess (the same question with a codename that is
not in the passage).
Design (amendment 60, note 31; Zach's answers, 29 Oct):
  - v4's relations minus films (people, cities, companies, landmarks), v4's role nouns, binding wordings (one per
    wording), value draws, filler genres, splice and distractor stem filter; X's fact rotated through the six positions;
  - beyond v4: no distractor's first token (its name as the answer is read, either case) is the first token of one of
    X's names, since hop 1 picks X among the passage's entities;
  - three scenes per bridge (wordings alternate: w = (bridge index + draw) % 2), about 600 scenes;
  - codenames: invented two-syllable pseudo-words (onset + vowel + coda syllables from the fixed lists below,
    capitalised). A codename is never a real word: the lowercased word and each of its 4-letter substrings must not be
    a word of /usr/share/dict/words, or, without that file, must not be a single token with a leading space in the
    Qwen3.5-9B tokenizer (the capitalised word too, against names). No codename is a name or answer word of v3's
    tables or shares a 4-letter stem with one; within a scene none shares a 4-letter stem with a scene entity's name or
    either of its v3 descriptions; the scene's six codenames and its unused (guess) codename have distinct first tokens
    (" " + codename) and distinct stems. First tokens (here and for distractors) are distinct under each of the note's
    models' tokenizers (Qwen3.5-9B, Qwen3.6-27B, Nemotron 3.5 Lightning). Codenames are drawn uniformly at random (seeded) and so assigned to
    entities at random, never by sound. Beyond the prereg: no codename opens with the first three letters of a
    country or nationality of the four relations' answers ("Korvan" would sound Korean);
  - the six binding sentences in a random order (X's balanced: each of the six places once per block of six scenes of a
    relation and wording), merged at random places among the facts (the facts keep their order);
    filler re-dealt while it shares a 4-letter stem with a codename or "code".
Every entity's real attribute (entity_reals, from data/v3_bridges.json) and v3 descriptions (entity_descs) are stored.

HF_HOME=/workspace/hf_cache python scripts/jsuite_v5al.py [--seed 5201] [--name jsuite_v5al]
  -> data/tasks_v2/jsuite_v5al_test_chat (MP, MM) and data/tasks_v2/jsuite_v5alctl_test_chat (H1, RO)
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
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
RELS = ("people", "cities", "companies", "landmarks")  # v4's minus films
DRAWS = 3  # scenes per bridge
TOKENIZER_TARGET = "qwen3.5-9b"  # pins target whose tokenizer runs the real-word rule
FIRST_TOKEN_TARGETS = ("qwen3.5-9b", "qwen3.6-27b", "nemotron-3.5-lightning")  # the note's models: distinct first tokens under each
DICT = Path("/usr/share/dict/words")
# the fixed syllable list: onset + vowel + coda ("Zor", "bel", "Kav", "rin"); a codename is two different syllables, the
# first's coda not the second's onset
ONSETS = ("b", "d", "f", "g", "k", "l", "m", "n", "p", "r", "s", "t", "v", "z")
VOWELS = ("a", "e", "i", "o", "u")
CODAS = ("k", "l", "m", "n", "r", "v")
SYLLABLES = tuple(o + v + c for o in ONSETS for v in VOWELS for c in CODAS)
BIND = "{E} goes by the codename {C}."


def tokenizers() -> tuple[dict, dict]:
    os.environ.setdefault("HF_HOME", "/workspace/hf_cache")
    from transformers import AutoTokenizer

    from bridge_jspace import pins

    pin = {t: {"repo": pins.TARGETS[t]["repo"], "revision": pins.TARGETS[t]["revision"]} for t in FIRST_TOKEN_TARGETS}
    toks = {t: AutoTokenizer.from_pretrained(p["repo"], revision=p["revision"], local_files_only=True) for t, p in pin.items()}
    return toks, pin


def codename_pool(toks: dict, names: set[str], name_stems: set[str], cue_prefixes: set[str]) -> tuple[list[str], dict[str, tuple], dict]:
    """Every codename that passes the real-word rule (Qwen3.5-9B's tokenizer) and the global name rules, with its first
    token (" " + codename) under each tokenizer of FIRST_TOKEN_TARGETS.
    Beyond the prereg's rule: no codename opens with the first three letters of an answer word of the four relations
    (a country or nationality: "Korvan" would sound Korean)."""
    tok = toks[TOKENIZER_TARGET]
    words = sorted({(s1 + s2).capitalize() for s1 in SYLLABLES for s2 in SYLLABLES if s1 != s2 and s1[-1] != s2[0]})
    subs = lambda lw: [lw[i : i + 4] for i in range(len(lw) - 3)]  # noqa: E731
    if DICT.exists():
        rule = f"dict: {DICT}"
        lex = {w.strip().lower() for w in DICT.read_text(errors="ignore").splitlines() if w.strip()}
        real = lambda w: w.lower() in lex or any(s in lex for s in subs(w.lower()))  # noqa: E731
    else:
        rule = f"tokenizer ({TOKENIZER_TARGET}): ' '+word (lowercased and capitalised) or ' '+any 4-letter substring is a single token"
        forms = sorted({f for w in words for f in [" " + w.lower(), " " + w, *(" " + s for s in subs(w.lower()))]})
        single = {f for f, ids in zip(forms, tok(forms, add_special_tokens=False).input_ids, strict=True) if len(ids) == 1}
        real = lambda w: any(f in single for f in [" " + w.lower(), " " + w, *(" " + s for s in subs(w.lower()))])  # noqa: E731
    reasons = collections.Counter()
    pool = []
    for w in words:
        if real(w):
            reasons["real word"] += 1
        elif w.lower() in names:
            reasons["a name or answer word"] += 1
        elif V4.stems(w) & name_stems:
            reasons["stem of a name or answer word"] += 1
        elif w.lower()[:3] in cue_prefixes:
            reasons["opens like a country or nationality"] += 1
        else:
            pool.append(w)
    heads = [[ids[0] for ids in tk([" " + w for w in pool], add_special_tokens=False).input_ids] for tk in toks.values()]
    first = {w: tuple(h[i] for h in heads) for i, w in enumerate(pool)}
    return pool, first, {"rule": rule, "candidates": len(words), "pool": len(pool), "rejected": dict(reasons)}


def draw_codenames(rng: random.Random, pool: list[str], first: dict[str, tuple], avoid: set[str], n: int) -> list[str] | None:
    """n codenames drawn uniformly at random from the pool: distinct first tokens (under each tokenizer), distinct
    stems, no stem in avoid."""
    chosen, firsts, sts = [], set(), set()
    for _ in range(20000):
        c = rng.choice(pool)
        st = V4.stems(c)
        heads = set(enumerate(first[c]))
        if c in chosen or heads & firsts or st & avoid or st & sts:
            continue
        chosen.append(c)
        firsts |= heads
        sts |= st
        if len(chosen) == n:
            return chosen
    return None


def count(word: str, text: str) -> int:
    return len(re.findall(r"(?i)\b" + re.escape(word) + r"\b", text))


def main(a) -> None:
    rng = random.Random(a.seed)
    toks, pin = tokenizers()
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
               "journalist", "twin", "twinning", "studio", "documentary", "office"}  # fmt: skip  (v4's filler bans)
    banned |= {"codename", "codenames", "codenamed", "code-name", "alias", "nickname"}  # v5al: the binding's words
    # codenames: no name or answer word of any v3 table (all relations, other names too) and no 4-letter stem of one
    name_words = set(banned) | {w for r in table for n in [r["bridge"], *r.get("bridge_alts", [])] for w in n.split()}
    names = {w.lower() for w in name_words}
    name_stems = set().union(*(V4.stems(w) for w in name_words))
    answers = {v for rel in RELS for v in [*(f[0] for f in tabs[rel]["facts"].values()),
                                           *(al for r in tabs[rel]["meta"].values() for al in r["answer_aliases"])]}
    cue_prefixes = {v.lower()[:3] for v in answers if len(v) >= 4 and v[:3].isalpha()}
    pool, first, pool_info = codename_pool(toks, names, name_stems, cue_prefixes)
    heads = lambda n: {(t, tk(v, add_special_tokens=False).input_ids[0]) for t, tk in toks.items() for v in (n, n.lower())}  # noqa: E731  (S.answer_token, "open")
    deck = V3.Deck(rng, V3.JF.clean_paras(banned))
    items, skipped = [], collections.Counter()
    k = 0
    for rel in RELS:
        t = tabs[rel]
        noun = "person" if rel == "people" else t["noun"]
        vocab = sorted({v[0] for v in t["facts"].values()})
        bridges = sorted(b for (r, b) in rows if r == rel)
        desc_of = {b: [f"the {noun} {V4.PRON[rel]} {d['clause']}" for d in rows[(rel, b)]["descriptions"]] for b in bridges}
        clause_of = {b: [d["clause"] for d in rows[(rel, b)]["descriptions"]] for b in bridges}
        real_of = {b: rows[(rel, b)]["answer"] for b in bridges}
        assert all(real_of[b] == t["facts"][b][0] for b in bridges), rel
        pos_counter = collections.Counter()
        bind_deck = collections.defaultdict(list)
        for bi, x in enumerate(bridges):
            real_x = t["facts"][x][0]
            heads_x = set().union(*(heads(n) for n in {x, *rows[(rel, x)].get("bridge_alts", [])}))
            for draw in range(DRAWS):
                w = (bi + draw) % 2
                fact_tpl, q_tpl = (t["pfact"][1], t["q2P"][1]) if w == 0 else V4.REL2[rel]
                # v4's distractor stem filter, and (v5al) no distractor whose first token (as read, any case) is one of X's
                # names': hop 1 is a pick among the passage's six entities, read by its first token (cand2)
                ok = [b for b in bridges if b != x and not (V4.stems(x) & V4.stems(b)) and not (heads(b) & heads_x)]
                if len(ok) < V4.K - 1:
                    skipped["too few distractors"] += 1
                    continue
                others = rng.sample(ok, V4.K - 1)
                ents = [x, *others]
                vals = None
                for _ in range(200):  # distinct values, none an entity's own attribute, none X's attribute (v4)
                    cand = rng.sample([v for v in vocab if v != real_x], V4.K)
                    if all(cand[i] != t["facts"][e][0] for i, e in enumerate(ents)):
                        vals = dict(zip(ents, cand, strict=True))
                        break
                if vals is None:
                    skipped["no value draw"] += 1
                    continue
                scene_stems = set().union(*(V4.stems(e) for e in ents), *(V4.stems(c) for e in ents for c in clause_of[e]))
                cns = draw_codenames(rng, pool, first, scene_stems, V4.K + 1)
                if cns is None:
                    skipped["no codename draw"] += 1
                    continue
                code = dict(zip(ents, cns[: V4.K], strict=True))  # random draws, so a random assignment
                unused = cns[V4.K]
                code_stems = {"code"} | set().union(*(V4.stems(c) for c in cns))
                for _ in range(50):  # filler free of the codenames' stems and "code" (v4: of the description's words)
                    para = deck.deal(V4.N_FILLER)
                    if not (V4.stems(" ".join(para)) & code_stems):
                        break
                else:
                    skipped["filler leak"] += 1
                    continue
                pos = pos_counter[(rel, w)] % V4.K  # the bridge's fact rotated through the six positions
                pos_counter[(rel, w)] += 1
                order = [e for e in ents if e != x]
                rng.shuffle(order)
                order.insert(pos, x)
                if not bind_deck[(rel, w)]:  # X's binding sentence: each of the six places once per block of six scenes, in random order
                    bind_deck[(rel, w)] = rng.sample(range(V4.K), V4.K)
                border = [e for e in ents if e != x]  # the other bindings in a random order
                rng.shuffle(border)
                border.insert(bind_deck[(rel, w)].pop(), x)
                facts = [V4.fact(fact_tpl, e, vals[e]) for e in order]
                binds = [BIND.format(E=V3.sentence(e), C=code[e]) for e in border]
                bslots = set(rng.sample(range(2 * V4.K), V4.K))  # where the bindings go among the facts
                fi, bj, merged = iter(facts), iter(binds), []
                for i in range(2 * V4.K):
                    merged.append(next(bj) if i in bslots else next(fi))
                genre = rng.choice(sorted(V3.N.GENRES))
                ctx = V4.splice(rng, genre, merged, para)
                if not all(count(e, ctx) == 2 for e in ents):
                    skipped["an entity name not exactly twice"] += 1
                    continue
                if not (all(count(code[e], ctx) == 1 for e in ents) and count(unused, ctx) == 0 and count("codename", ctx) == V4.K):
                    skipped["a codename not exactly once"] += 1
                    continue
                if V3.words_in(ctx, [real_x]):
                    skipped["X's attribute in the passage"] += 1
                    continue
                desc = f"the {noun} codenamed {code[x]}"
                gdesc = f"the {noun} codenamed {unused}"
                q1 = f"Which {noun} is codenamed {code[x]}?"
                q_mp = q_tpl.format(d=desc, D=V3.sentence(desc))
                q_mm = t["q2M"][1 - w].format(d=desc, D=V3.sentence(desc))
                assert desc in q_mp and desc in q_mm, (q_mp, q_mm)
                alts = sorted({x, *rows[(rel, x)].get("bridge_alts", [])})
                base = {"module": "facts", "start": "P", "domain": rel, "relation": rel, "format": "prose", "genre": genre,
                        "framing": "chat", "wording": w, "rep": w, "level": 2, "split": "test", "popularity": t["facts"][x][2],
                        "half": "A", "context": ctx, "kind": "open", "answer_kind": "open", "answer_vocab": vocab,
                        "bridge": x, "bridges": [x], "start_desc": desc, "desc_index": None, "skip_cue": None, "real": real_x,
                        "entities": order, "passage_values": vals, "bridge_position": pos, "eponymous": False,
                        "name_reveals_answer": rows[(rel, x)].get("name_reveals_answer", False), "bridge_in_passage": True,
                        "bridge_mentions": 2, "entity_descs": {e: desc_of[e] for e in ents},
                        "knobs": {"entities": V4.K, "filler": V4.N_FILLER}, "set_version": "v4",
                        "codename": code[x], "codenames": {e: code[e] for e in order}, "guess_codename": unused,
                        "entity_reals": {e: real_of[e] for e in order}, "binding_position": border.index(x),
                        "draw": draw}  # fmt: skip
                hop1 = {"question": q1, "answer": x, "kind": "open", "source": "P", "alts": alts}
                uid = f"{k:05d}"
                items.append({**base, "id": f"j3:chat:v5al:MP-w{w}-{uid}", "word": "MP", "final": "P", "final_source": "P", "control": "P",
                              "scene": f"v5al:MP:{uid}", "question": q_mp, "answer": vals[x], "answer_aliases": alias_of.get(vals[x], []),
                              "answer_in_passage": True, "memory_answer": real_x,
                              "steps": [hop1, {"question": q_tpl.format(d=x, D=V3.sentence(x)), "answer": vals[x], "kind": "open",
                                               "source": "P", "cand_vocab": vocab}],
                              "guess_question": q_tpl.format(d=gdesc, D=V3.sentence(gdesc))})  # fmt: skip
                items.append({**base, "id": f"j3:chat:v5al:MM-w{w}-{uid}", "word": "MM", "final": "M", "final_source": "M", "control": "M",
                              "scene": f"v5al:MM:{uid}", "question": q_mm, "answer": real_x, "answer_aliases": alias_of.get(real_x, []),
                              "answer_in_passage": False, "memory_answer": real_x,
                              "steps": [hop1, {"question": t["q2M"][1 - w].format(d=x, D=V3.sentence(x)), "answer": real_x, "kind": "open",
                                               "source": "M", "cand_vocab": vocab}],
                              "guess_question": t["q2M"][1 - w].format(d=gdesc, D=V3.sentence(gdesc))})  # fmt: skip
                ctrl = {**base, "answer_in_passage": False, "steps": [], "guess_question": None, "memory_answer": real_x}
                # H1: hop 1 with the passage (v4's H1 was closed book; here the codename exists only in the passage)
                items.append({**ctrl, "id": f"j3:chat:v5al:H1-w{w}-{uid}", "word": "H1", "final": "B", "final_source": "P", "control": "H1",
                              "scene": f"v5al:H1:{uid}", "question": q1, "answer": x, "answer_aliases": alts, "answer_in_passage": True,
                              "answer_vocab": bridges})  # fmt: skip
                role = f"the {noun}"
                items.append({**ctrl, "id": f"j3:chat:v5al:RO-w{w}-{uid}", "word": "RO", "final": "P", "final_source": "P", "control": "RO",
                              "scene": f"v5al:RO:{uid}", "question": q_tpl.format(d=role, D=V3.sentence(role)), "answer": vals[x],
                              "answer_aliases": alias_of.get(vals[x], []), "answer_in_passage": True})  # fmt: skip
                k += 1
    ids = [it["id"] for it in items]
    assert len(ids) == len(set(ids)), "duplicate ids"
    out = Path(a.data) / f"{a.name}_test_chat"
    ctl = Path(a.data) / f"{a.name}ctl_test_chat"
    for d in (out, ctl):
        assert not d.exists(), f"{d} exists; sets are written once"
        d.mkdir(parents=True)
    main_txt = "".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items if it["word"] in ("MP", "MM"))
    ctl_txt = "".join(json.dumps(it, ensure_ascii=False) + "\n" for it in items if it["word"] not in ("MP", "MM"))
    (out / "items.jsonl").write_text(main_txt)
    (ctl / "items.jsonl").write_text(ctl_txt)
    sha = {d.name: hashlib.sha256((d / "items.jsonl").read_bytes()).hexdigest() for d in (out, ctl)}
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--", "scripts/jsuite_v5al.py"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    man = {"set": out.name, "controls": ctl.name, "seed": a.seed, "n": len(items), "scenes": k, "git_commit": commit,
           "script": "scripts/jsuite_v5al.py", "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "script_uncommitted": bool(dirty), "items_sha256": sha, "tokenizers": {"real_word_rule": TOKENIZER_TARGET, "first_tokens": pin},
           "codenames": {**pool_info, "onsets": ONSETS, "vowels": VOWELS, "codas": CODAS},
           "words": dict(collections.Counter(it["word"] for it in items)), "skipped": dict(skipped),
           "relations": dict(collections.Counter(it["relation"] for it in items if it["word"] == "MP")),
           "wordings": dict(collections.Counter(str(it["wording"]) for it in items if it["word"] == "MP"))}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(man, indent=2) + "\n")
    print(json.dumps(man, indent=1))
    for wd in ("MP", "MM", "H1", "RO"):
        x = next(i for i in items if i["word"] == wd)
        print(f"--- {wd}: {x['question']} -> {x['answer']}")
    print(items[0]["context"])
    for d in (out, ctl):
        print(f"sha256 {sha[d.name]}  {d / 'items.jsonl'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=5201)
    ap.add_argument("--name", default="jsuite_v5al")
    ap.add_argument("--data", default=str(DATA), help="where the sets go (another directory for a dry run)")
    main(ap.parse_args())
