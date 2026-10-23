"""jsuite_numbers (Zach, 2026-10-23, prereg amendment 24): module 2 of the combined suite, numbers as intermediates
(ctxcomp_v1 redesigned after its competence and knock-out pilots, amendment 21 notes).

The intermediate X (2-8) is a number; its start S says where it comes from:
  P  stated in the passage ("Mia visited 5 cities.")
  K  counted from the passage ("Mia visited Rome, Oslo, Lima, Cairo and Quito."): X is never written
  A  computed by arithmetic from the passage ("Mia had 9 stamps and gave 4 of them to a friend."): only the operands
  M  recalled from memory ("the number of legs of the spider", "the number of days in a week")
The final step F uses X:
  R  report it ("How many cities did Mia visit?"); R items have their own passages, without the locker list
  L  a lookup keyed by X in a digit-labelled list ("Locker 5 belongs to Kate."; "Who owns the locker whose number
     equals the number of cities Mia visited?"): no number -> ordinal mapping (ctxcomp_v1's seat row needed one, and
     even a stated number's seat lookup lost as much as a recall on the 9B)
  M  a recall keyed by X (the month or the planet at that position; Greek letters dropped, hardest to compose)
Words SF: PR PL PM KR KL KM AR AL AM MR ML MM. L and M of a start share a scene (the passage with the locker list);
R has its own scene. Eligibility per item (amendment 21 note 2). Two other people get other values (never X). X is
never written in K, A or M passages except as one of the eight locker labels (L and M scenes). Real WikiText filler
(no digits, no month or planet names; no "notes" genre, whose header names a month). Chat framing, kind open, own candidate vocabularies; locker owners are single tokens in
the 27B and 9B tokenizers, months and planets have distinct first tokens.

python scripts/jsuite_numbers.py --name jsuite_v1_numbers --seed 2401 [--reps 8]
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
from scripts import tasks_v2 as T  # noqa: E402

DATA = N.DATA
XS = range(2, 9)
NAMES = ["Leo", "Ana", "Ben", "Sam", "Max", "Tom", "Jack", "Kate", "Paul", "Theo", "Anna", "John", "Lisa", "Emma",
         "Adam", "Eric", "Carl", "Gary", "Sean", "Tim", "Dan", "Bob", "Joe", "Ted", "Amy", "Kim", "Lee", "Roy", "Ali",
         "Jon", "Ken", "Lou", "Tony", "Jane", "Ryan", "Ian", "Ada"]  # single tokens (no leading space) for the 27B and
# 9B tokenizers, so seat owners never share a first token; names that are common words (Will, Mark, Rose) left out
ABSENT = ["Quinn", "Wanda", "Odette"]
COUNT_CATS = {  # (verb past, verb base, plural noun, items, how an item is listed)
    "cities": ("visited", "visit", "cities", ["Rome", "Oslo", "Lima", "Cairo", "Paris", "Tokyo", "Delhi", "Quito", "Dakar",
                                              "Hanoi", "Vienna", "Dublin", "Lisbon", "Seoul", "Nairobi", "Havana"], "{x}"),
    "fruits": ("packed", "pack", "fruits", ["apple", "pear", "fig", "plum", "peach", "lemon", "mango", "kiwi", "grape",
                                           "melon", "lime", "orange"], "{a} {x}"),
    "birds": ("spotted", "spot", "birds", ["robin", "heron", "crow", "swan", "owl", "finch", "hawk", "wren", "gull",
                                          "eagle", "dove", "stork"], "{a} {x}"),
}  # fmt: skip
ARITH_CATS = {  # (sentence, descriptor of X, report question, op)
    "stamps": ("{p} had {a} stamps and gave {b} of them to a friend.", "the number of stamps {p} had left",
               "How many stamps did {p} have left?", "-"),
    "postcards": ("{p} sent {a} postcards on Monday and {b} more on Tuesday.", "the total number of postcards {p} sent",
                  "How many postcards did {p} send in total?", "+"),
    "coins": ("{p} found {a} coins in the garden and {b} more in the car.", "the total number of coins {p} found",
              "How many coins did {p} find in total?", "+"),
}  # fmt: skip
LOCKER_Q = ("Who owns the locker whose number equals {n}?", "Whose locker has the number that equals {n}?")
LOCKER_STEP = "Who owns locker {x}?"
EXTRA_M = {7: [("the number of days in a week", "How many days are in a week?")]}
M_FINALS = ("planets", "months")  # Greek letters dropped (hardest to compose on both models); elements share first tokens
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August",
                                      "September"], 1)}  # fmt: skip
MONTH_Q = ("Which month of the year is at the position equal to {n}?", "Which month's position in the year equals {n}?")
MONTH_STEP = "Which month is month number {x} of the year?"
DIGITS = [str(d) for d in range(1, 10)]


def listing(items: list[str], form: str) -> str:
    xs = [form.format(x=x, a=N.an(x)) for x in items]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def m_things() -> dict[int, list[tuple[str, str]]]:
    """Memory starts: (domain, thing) whose number (legs, sides, wheels, strings) is X."""
    out = collections.defaultdict(list)
    for d in ("animals", "shapes", "vehicles", "instruments"):
        for thing, v in T.DOMAINS[d].values.items():
            if v in XS:
                out[v].append((d, thing))
    return out


def start_fact(rng, S: str, person: str, x: int, cat: str, avoid: int | None = None) -> tuple[str, str, str] | None:
    """(passage sentence, descriptor of X, report question) for a person's value x under start S (P, K or A); for A,
    neither operand is x or `avoid` (the target's X, so it is never written); None if no such operands exist."""
    if S in ("P", "K"):
        past, base, noun, items, form = COUNT_CATS[cat]
        desc, q = f"the number of {noun} {person} {past}", f"How many {noun} did {person} {base}?"
        if S == "P":
            return f"{person} {past} {x} {noun}.", desc, q
        return f"{person} {past} {listing(rng.sample(items, x), form)}.", desc, q
    sent, desc, q, op = ARITH_CATS[cat]
    pairs = [(a, a - x) if op == "-" else (a, x - a) for a in (range(x + 1, 10) if op == "-" else range(1, x))]
    pairs = [(a, b) for a, b in pairs if b >= 1 and not {a, b} & {x, avoid}]
    if not pairs:
        return None
    a, b = rng.choice(pairs)
    sent = re.sub(r"\b1 (postcard|coin|stamp)s\b", r"1 \1", sent.format(p=person, a=a, b=b))  # "1 postcard"
    return sent, desc.format(p=person), q.format(p=person)


def make(name: str, seed: int, reps: int) -> None:
    rng = random.Random(seed)
    banned = set(NAMES + ABSENT) | {i for c in COUNT_CATS.values() for i in c[3]} | {"locker", "lockers"} | set(MONTHS) | {"Mars", "Venus", "Mercury", "Jupiter", "Saturn", "Uranus", "Neptune"}
    paras = [p for p in NP.real_paragraphs(banned) if not any(re.search(r"\d", s) for s in p)]
    mt = m_things()
    items, k = [], 0
    for S in ("P", "K", "A", "M"):
        for x in XS:
            for rel in M_FINALS:
                for rep in range(reps):
                    k += 1
                    w = rng.randrange(2)
                    people = rng.sample(NAMES, 11)
                    seat_owners, cast = people[:8], people[8:]
                    cats = COUNT_CATS if S in ("P", "K", "M") else ARITH_CATS
                    cat = rng.choice(sorted(cats))
                    facts, desc, rq = [], None, None
                    if S == "M":  # the passage still has three people with stated values, none equal to X
                        for p_, v in zip(cast, rng.sample([v for v in XS if v != x], 3), strict=True):
                            facts.append(start_fact(rng, "P", p_, v, cat)[0])
                        opts = [("dom", d, thing) for d, thing in mt[x]] + [("extra", dsc, q_) for dsc, q_ in EXTRA_M.get(x, [])]
                        kind_, a_, b_ = rng.choice(opts)
                        if kind_ == "dom":
                            dom = T.DOMAINS[a_]
                            desc, rq = dom.prop_phrase.format(x=T.ref(dom, b_)), dom.prop_q[w].format(x=T.ref(dom, b_))
                        else:
                            desc, rq = a_, b_
                    else:
                        while (f0 := start_fact(rng, S, cast[0], x, cat)) is None:  # A: a category whose op fits x
                            cat = rng.choice(sorted(cats))
                        f0, desc, rq = f0
                        facts.append(f0)
                        pool = [v for v in XS if v != x]
                        for p_ in cast[1:]:
                            while (fd := start_fact(rng, S, p_, (v := rng.choice(pool)), cat, avoid=x)) is None:
                                pass
                            pool.remove(v)
                            facts.append(fd[0])
                    lockers = [f"Locker {i + 1} belongs to {seat_owners[i]}." for i in range(8)]
                    genre = rng.choice(sorted(g for g in N.GENRES if g != "notes"))  # its header "Meeting notes, 14 March." names a month
                    para = rng.choice([p for p in paras if len(p) >= 3])[:3]
                    r_seed = rng.random()
                    ctx_r = NP.passage(random.Random(r_seed), genre, facts, para)  # R: no locker list
                    lock_block = " ".join(lockers)
                    ctx_lm = NP.passage(random.Random(r_seed), genre, facts + [lock_block], para)  # L and M: with the list
                    if S != "P":
                        assert not re.search(rf"\b{x}\b", ctx_r), (S, x, ctx_r)  # X itself is never written
                    absent = rng.choice(ABSENT)
                    if S == "A":
                        gdesc, grq = ARITH_CATS[cat][1].format(p=absent), ARITH_CATS[cat][2].format(p=absent)
                    else:
                        c = COUNT_CATS[cat]
                        gdesc, grq = f"the number of {c[2]} {absent} {c[0]}", f"How many {c[2]} did {absent} {c[1]}?"
                    if rel == "months":
                        by_num, mvocab, rdesc, rstep = {v: m for m, v in MONTHS.items()}, sorted(MONTHS), MONTH_Q, MONTH_STEP
                    else:
                        mdom = T.DOMAINS[rel]
                        by_num = {v: t for t, v in mdom.values.items()}
                        mvocab = sorted({t[0].upper() + t[1:] for t in mdom.values})
                        rdesc, rstep = mdom.reverse_desc, mdom.reverse_q.replace("{n}", "{x}")
                    finals = {
                        "R": (rq, str(x), DIGITS, None, grq),
                        "L": (LOCKER_Q[w].format(n=desc), seat_owners[x - 1], sorted(seat_owners),
                              LOCKER_STEP.format(x=x), LOCKER_Q[w].format(n=gdesc)),
                        "M": (rdesc[w].format(n=desc), by_num[x][0].upper() + by_num[x][1:], mvocab,
                              rstep.format(x=x), rdesc[w].format(n=gdesc)),
                    }
                    for F, (q, ans, vocab, step2, guess) in finals.items():
                        steps = [{"question": rq, "answer": str(x), "kind": "open", "source": S, "alts": [str(x)],
                                  "cand_vocab": DIGITS}]  # fmt: skip
                        if step2:
                            steps.append({"question": step2, "answer": ans, "kind": "open", "source": F, "cand_vocab": vocab})
                        items.append({
                            "id": f"jn:chat:{S}{F}-{k:04d}", "word": S + F, "start": S, "final": F, "domain": cat,
                            "relation": {"R": "report", "L": "lockers", "M": rel}[F], "format": "prose", "genre": genre,
                            "framing": "chat", "wording": w, "context": ctx_r if F == "R" else ctx_lm, "question": q, "answer": ans,
                            "kind": "open", "answer_kind": "open", "answer_vocab": vocab, "steps": steps,
                            "bridge": str(x), "bridges": [str(x)], "x": x, "start_desc": desc, "guess_question": guess,
                            "scene": f"jn:{S}-{x}-{rel}-{rep}-{'R' if F == 'R' else 'LM'}", "level": 0, "knobs": {"entities": 3, "filler": 3},
                            "numbers": "digits", "c_op": None, "chance_same_answer": 0.0,
                            "answer_in_passage": bool(re.search(rf"\b{re.escape(ans)}\b", ctx_r if F == "R" else ctx_lm)),
                        })  # fmt: skip
    out = DATA / f"{name}_chat"
    assert not out.exists(), f"{out} exists; sets are written once"
    out.mkdir(parents=True)
    (out / "items.jsonl").write_text("".join(json.dumps(it) + "\n" for it in items))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    (out / "manifest.json").write_text(json.dumps({"set": out.name, "seed": seed, "reps": reps, "n": len(items),
                                                   "git_commit": commit, "script": "scripts/jsuite_numbers.py"}, indent=2) + "\n")  # fmt: skip
    print(f"{out.name}: {len(items)} items", dict(collections.Counter(it["word"] for it in items)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--seed", type=int, default=2401)
    ap.add_argument("--reps", type=int, default=8)
    a = ap.parse_args()
    make(a.name, a.seed, a.reps)
