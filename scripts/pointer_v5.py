"""pointer_v5 (D3, 2026-10-21): does the last tokens' statement address survive word answers and longer lists?
The two boring explanations of D3's "same statement slot": a trick for copying a digit, and a property of 5-item
lists. Here the same scenes are built with digit answers and with colour words, with 5 and with 8 statements.

Scene: pointer_v4's entities (85, 3 topics, held-out split) in N = 5 or 8 statements (set len12: 12); one wording of 3
per scene (pointer_v4's for digits, the colour wordings below for words, the same index; wording 2 is pointer_v4's
held-out one). Each scene is built twice on the same entities and slots: values are digits 0-9 (level e<N>-digit) or
colour words (e<N>-word: 11 colours, one token each with a leading space under Qwen3.6-27B's and OLMo-3's tokenizers;
set len12: words only, 16 colours).
The alt prompt asks about bridge alt (q_s), at slot k; the org prompt has q_s at slot c and the asked entity at a
(a, c, k distinct). Predictions: none / identity (the org value of q_s) / position (the org value at slot k) / value
(the alt answer, not in the org prompt). Families: memory -> prompt (RL), named -> prompt (DL). Controls: "same" (q_b
in its slot with its value, the rest reshuffled) and "redigit" (the asked value replaced). Digit values avoid the
recalled digits of q_b and q_s where the pool allows (pointer_v4x's rule). Cap: the asked entity cycles through the
askable pool.

Sets: main, up to 150 scenes per topic and list length, seed 871 (5 and 8 statements, digits and words). Files:
data/pointer_v5/<set>/<topic>_<family>_<level>.json.
  len8   (22 Oct, night; finding 5 on longer lists) main's 8-statement design on a fresh draw, seed 872: e8-digit and
         e8-word on the same scenes, 11 colours.
  len12  (the same night) 12 statements, seed 873: colour words only (12 distinct values and an alt answer absent from
         the org prompt need 13; digits 0-9 are 10), from 16 colours: the 11 above and gold, silver, cyan, violet,
         beige (the first five of a list fixed before the tokenizer check: gold, silver, cyan, violet, beige, navy, teal,
         tan, ...; each one token after a space under Qwen3.6-27B's tokenizer, which Qwen3.5-9B shares); answer kind
         "colour16", judged on those 16.
  Per file the seed is <set seed> * 100 + 10 * <topic index in pointer_v4's SPEC> + N.

Stages:  make [--set S] | verify (every set) | check [--set S] (tokenizer only; BJ_TARGET picks the tokenizer)
         manifest [--set S] --name N --why W [--limit K] | competence --name N (GPU)
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import chat, pins
from bridge_jspace.run_switches import switches
from scripts import pointer_v1 as PV
from scripts import pointer_v4 as P4
from scripts import suite_v1 as S

EXP = "pointer_v5"
DATA = Path(os.environ.get("BJ_POINTER_V5_DATA", str(pins.DATA_DIR / EXP)))
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES = ("RL", "DL")
DOMAINS = P4.DOMAINS
SIZES = (5, 8)
KINDS = ("digit", "word")
DIGITS = tuple(str(d) for d in range(10))
COLOURS = ("red", "blue", "green", "black", "white", "pink", "brown", "grey", "orange", "purple", "yellow")
COLOURS16 = (*COLOURS, "gold", "silver", "cyan", "violet", "beige")
WORD_POOLS = {"colour": COLOURS, "colour16": COLOURS16}  # a word item's answer kind -> its values (and its judge's)
CAP = P4.CAP
# a set's list lengths, answer kinds and word pool default to main's: SIZES, KINDS, "colour"
SETS: dict[str, dict[str, Any]] = {
    "main": {"seed": 871, "n": 150},
    "len8": {"seed": 872, "n": 150, "sizes": (8,)},
    "len12": {"seed": 873, "n": 150, "sizes": (12,), "kinds": ("word",), "words": "colour16"},
}
WORDS: dict[str, dict[str, tuple[str, ...]]] = {  # colour wordings, index-matched to pointer_v4's
    "countries": {
        "statements": ("The {e} file is in the {d} drawer.", "The {d} drawer holds the {e} file.",
                       "The file on {e} is kept in the {d} drawer."),
        "lookups": ("Which colour is the drawer that holds the file on {x}?",
                    "What colour is the drawer with the file on {x}?",
                    "The file on {x} is in a drawer of which colour?"),
    },
    "animals": {
        "statements": ("The {e}'s locker is {d}.", "The {d} locker belongs to the {e}.",
                       "The {e} keeps its things in the {d} locker."),
        "lookups": ("What colour is the locker of {x}?", "Which colour is the locker that belongs to {x}?",
                    "In a locker of which colour does {x} keep its things?"),
    },
    "body": {
        "statements": ("The {e} chart is in the {d} folder.", "The {d} folder holds the {e} chart.",
                       "The chart on the {e} is kept in the {d} folder."),
        "lookups": ("Which colour is the folder that holds the chart on {x}?",
                    "What colour is the folder with the chart on {x}?",
                    "The chart on {x} is in a folder of which colour?"),
    },
}  # fmt: skip


def templates(domain: str, kind: str) -> dict[str, tuple[str, ...]]:
    return P4.SPEC[domain] if kind == "digit" else WORDS[domain]


def statements(domain: str, kind: str, t: int, ents: list[str], values: list[str]) -> list[str]:
    tpl = templates(domain, kind)["statements"][t]
    return [tpl.format(e=e, d=v) for e, v in zip(ents, values, strict=True)]


def said(text: str, kind: str) -> str | None:
    """pointer_v4's judge; for colour answers, the first colour word of the first non-empty line, among the colours
    of the item's pool (WORD_POOLS[kind]: main's 11 for "colour", 16 for "colour16")."""
    if kind in WORD_POOLS:
        pool = WORD_POOLS[kind]
        return next((w for w in re.findall(r"[a-z]+", S.first_line(text).lower()) if w in pool), None)
    return P4.said(text, kind)


def same_control(rng: random.Random, ents: list[str], values: list[str], a: int, pool: list[str]) -> tuple[list, list]:
    n = len(ents)
    while True:  # q_b in its slot with its value, the rest reshuffled and revalued
        m_ents = rng.sample([e for e in ents if e != ents[a]], n - 1)
        m_ents.insert(a, ents[a])
        m_vals = rng.sample([v for v in pool if v != values[a]], n - 1)
        m_vals.insert(a, values[a])
        if m_ents != ents:
            return m_ents, m_vals


def values_for(rng: random.Random, pool: list[str], n: int, k: int) -> dict[str, Any]:
    """Org values, the alt answer (not among them), the alt values (the answer at k), the same control's pool."""
    vals = rng.sample(pool, n)
    value = rng.choice([v for v in pool if v not in vals])
    alt = rng.sample([v for v in pool if v != value], n - 1)
    alt.insert(k, value)
    return {"values": vals, "value": value, "alt": alt}


def scene(rng: random.Random, domain: str, pool: list[str], q_b: str, cue_len: dict, n: int,
          kinds: tuple[str, ...] = KINDS, colours: tuple[str, ...] = COLOURS) -> dict:  # fmt: skip
    """One scene's entities and slots, and per answer kind in `kinds` its values (main's defaults draw in main's
    order, so its files are reproduced)."""
    k = rng.randrange(n)
    a, c = rng.sample([s for s in range(n) if s != k], 2)
    q_s = rng.choice([e for e in pool if P4.pair_ok(domain, q_b, e, cue_len)])
    others = rng.sample([e for e in pool if e not in (q_b, q_s)], n - 2)
    ents: list[str] = [""] * n
    ents[a], ents[c] = q_b, q_s
    for s, e in zip([s for s in range(n) if not ents[s]], others, strict=True):
        ents[s] = e
    alt = rng.sample([e for e in ents if e != q_s], n - 1)
    alt.insert(k, q_s)
    recalled = {e: P4.rec(domain, e) for e in ents}
    for avoid in ({recalled[q_b], recalled[q_s]}, {recalled[q_b]}, set()):
        dpool = [d for d in DIGITS if int(d) not in avoid]
        if len(dpool) >= n + 1:
            break
    out: dict[str, Any] = {"ents": ents, "alt": alt, "recalled": recalled, "slots": {"query": a, "identity": c,
                           "position": k}, "digit_policy": f"avoid {sorted(avoid)}"}  # fmt: skip
    for kind, vpool in (("digit", dpool), ("word", list(colours))):
        if kind not in kinds:
            continue
        v = values_for(rng, vpool, n, k)
        v["same"] = same_control(rng, ents, v["values"], a, vpool)
        out[kind] = v
    return out


def items_for(sc: dict, domain: str, n: int, kind: str, i: int, tw: tuple[int, int], held: set[str],
              words: str = "colour") -> dict[str, dict]:  # fmt: skip
    """The families' items of one scene and answer kind; `words`: the word items' answer kind (WORD_POOLS key)."""
    tpl = templates(domain, kind)
    t, u = tw
    ents, sl = sc["ents"], sc["slots"]
    v = sc[kind]
    vals, value = v["values"], v["value"]
    q_b, q_s = ents[sl["query"]], ents[sl["identity"]]
    look = dict(zip(ents, vals, strict=True))
    level = f"e{n}-{kind}"
    answer_kind = "digit" if kind == "digit" else words
    m_ents, m_vals = v["same"]
    r_vals = list(vals)
    r_vals[sl["query"]] = value
    ent_out, tpl_out = q_b in held, P4.HELD_OUT_TEMPLATE in (t, u)

    def src(e: list[str], d: list[str], q: str, query: str, ans: str, preds: dict) -> dict:
        st = statements(domain, kind, t, e, d)
        return {"context": " ".join(st), "statements": st, "question": q, "answer": ans, "entities": e, "digits": d,
                "query": query, "query_slot": e.index(query), "predictions": preds}  # fmt: skip

    out = {}
    for fam in FAMILIES:
        target = P4.name_of if fam == "DL" else P4.cue_of
        question, alt_q = (tpl["lookups"][u].format(x=target(domain, e)) for e in (q_b, q_s))
        pred = {"none": look[q_b], "identity": look[q_s], "position": vals[sl["position"]], "value": value}
        answer = look[q_b]
        sources = {
            "dissoc": src(sc["alt"], v["alt"], alt_q, q_s, value, pred),
            "same": src(m_ents, m_vals, question, q_b, answer, {h: answer for h in pred}),
            "redigit": src(ents, r_vals, question, q_b, value, {h: answer for h in pred} | {"value": value}),
        }
        st = statements(domain, kind, t, ents, vals)
        item = {
            "id": f"{domain}-{fam}-{level}-{i:04d}", "family": fam, "domain": domain, "level": level, "type": kind,
            "scene": f"{domain}-n{n}-{i:04d}", "n_entities": n, "entities": ents, "digits": vals,
            "recalled": sc["recalled"], "query": q_b, "cue": target(domain, q_b), "slots": dict(sl),
            "context": " ".join(st), "statements": st, "question": question, "answer": answer,
            "answer_kind": answer_kind, "sources": sources, "distinct": len(set(pred.values())) == len(pred),
            "digit_policy": sc["digit_policy"] if kind == "digit" else "colours",
            "templates": {"statement": t, "question": u}, "held_out_entity": ent_out, "held_out_template": tpl_out,
            "cut": "both" if ent_out and tpl_out else "entity" if ent_out else "template" if tpl_out else "neither",
        }  # fmt: skip
        if fam == "RL":
            spec = P4.SPEC[domain]
            item["hop1"] = {"question": spec["hop_cue"].format(c=spec["candidates"][q_b][1]), "answer": q_b,
                            "kind": domain}  # fmt: skip
            item["hop2"] = {"question": tpl["lookups"][u].format(x=P4.name_of(domain, q_b)), "answer": answer,
                            "kind": answer_kind}  # fmt: skip
        out[fam] = item
    return out


def generate(which: str, split: dict[str, Any]) -> dict[str, tuple[Path, list[dict], str]]:
    """label -> (file, items, generator note); tokenizer-free given pointer_v4's split.json."""
    spec = SETS[which]
    sizes, kinds, words = set_layout(which)
    cells: dict[str, list[dict]] = collections.defaultdict(list)
    notes: dict[str, str] = {}
    for domain in split["used"]:
        info = split["domains"][domain]
        pool, cue_len = info["pool"], info["cue_tokens"]
        held = set(info["held_out_entities"])
        askable = [e for e in pool if any(P4.pair_ok(domain, e, f, cue_len) for f in pool)]
        for n in sizes:
            count = min(spec["n"], CAP * len(askable))
            seed = spec["seed"] * 100 + 10 * list(P4.SPEC).index(domain) + n
            rng = random.Random(seed)
            seen: set[str] = set()
            q_round: list[str] = []
            for i in range(count):
                if not q_round:  # the cap: the asked entity cycles through the askable pool
                    q_round = rng.sample(askable, len(askable))
                q_b = q_round.pop()
                for _ in range(50):  # scenes never repeat within a topic and list length
                    tw = (rng.randrange(3), rng.randrange(3))
                    sc = scene(rng, domain, pool, q_b, cue_len, n, kinds, WORD_POOLS[words])
                    key = " ".join(statements(domain, kinds[0], tw[0], sc["ents"], sc[kinds[0]]["values"]))
                    if key not in seen:
                        break
                else:
                    raise AssertionError(f"{domain} n={n}: no new scene for {q_b}")
                seen.add(key)
                for kind in kinds:
                    for fam, item in items_for(sc, domain, n, kind, i, tw, held, words).items():
                        label = f"{domain}_{fam}_e{n}-{kind}"
                        cells[label].append(item)
                        notes[label] = f"scripts/pointer_v5.py make (set {which}, seed {seed}: {domain}, n={n})"
    return {label: (DATA / which / f"{label}.json", items, notes[label]) for label, items in cells.items()}


def set_layout(which: str) -> tuple[tuple[int, ...], tuple[str, ...], str]:
    """(list lengths, answer kinds, word pool) of a set; main's by default."""
    spec = SETS[which]
    return spec.get("sizes", SIZES), spec.get("kinds", KINDS), spec.get("words", "colour")


def set_levels(which: str) -> tuple[str, ...]:
    sizes, kinds, _ = set_layout(which)
    return tuple(f"e{n}-{k}" for n in sizes for k in kinds)


def set_files(which: str) -> dict[str, Path]:
    levels = set_levels(which)
    return {f"{d}_{f}_{lv}": DATA / which / f"{d}_{f}_{lv}.json" for d in DOMAINS for f in FAMILIES for lv in levels}


def level_name(level: str) -> str:
    """pointer_swap's figure titles."""
    n, kind = level[1:].split("-")
    return f"{n} statements, {'digit' if kind == 'digit' else 'colour-word'} answers"


# ---- checks (tokenizer only) ----------------------------------------------------------------------------------------


def check_item(tok, item: dict) -> dict[str, bool]:
    """prepare() accepts the item (every source token-aligned); predictions distinct and the alt answer absent from the
    org prompt; word items: every value's answer token distinct; statements regenerate."""
    from scripts import pointer_swap as PS

    out = {}
    try:
        PS.prepare(item, tok)
        out["prepare"] = True
    except AssertionError:
        out["prepare"] = False
    pd, vals, sl = item["sources"]["dissoc"]["predictions"], item["digits"], item["slots"]
    out["predictions"] = (len(set(pd.values())) == len(pd) and pd["value"] not in vals
                          and pd["position"] == vals[sl["position"]] and pd["identity"] == vals[sl["identity"]])  # fmt: skip
    kind = PS.answer_kind(item)
    words = {*vals, *pd.values()}
    out["answer_tokens"] = len({S.answer_token(tok, w, kind) for w in words}) == len(words)
    out["statements"] = item["statements"] == statements(item["domain"], item["type"], item["templates"]["statement"],
                                                         item["entities"], vals)  # fmt: skip
    return out


def write_set(path: Path, items: list[dict], note: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; data files are written once"
    head = {"family": items[0]["family"], "domain": items[0]["domain"], "level": items[0]["level"], "generator": note,
            "format": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)
    path.write_text(json.dumps(head, indent=1)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")


def stage_make(which: str) -> None:
    split = P4.load_split()
    assert split, "pointer_v4's split.json is missing"
    for _label, (path, items, note) in generate(which, split).items():
        write_set(path, items, note)
        print("wrote", path, len(items))


def stage_verify() -> None:
    split = P4.load_split()
    assert split, "pointer_v4's split.json is missing"
    for which in SETS:
        for label, (path, items, _) in generate(which, split).items():
            same = PV.load_file(path) == items
            print(which, label, "same" if same else "DIFFERENT")
            assert same, f"{label}: the generator no longer reproduces {path}"


def stage_check(which: str) -> None:
    """Every item of a set under the target's tokenizer (BJ_TARGET); writes check_<set>.json (another target:
    check_<set>_<target>.json)."""
    tok = PV.tokenizer()
    report: dict[str, Any] = {}
    for label, path in set_files(which).items():
        items = PV.load_file(path)
        stats: collections.Counter = collections.Counter()
        for it in items:
            for k, v in check_item(tok, it).items():
                stats[k] += bool(v)
        n = len(items)
        asked = collections.Counter(it["query"] for it in items)
        report[label] = {"n": n, **stats, "entities_asked": len(asked), "max_asked": max(asked.values()),
                         "wordings": len({(it["templates"]["statement"], it["templates"]["question"]) for it in items}),
                         "prompts_unique": len({it["context"] + it["question"] for it in items})}  # fmt: skip
        print(label, json.dumps(report[label]))
        if pins.TARGET == "qwen3.6-27b":
            for k in ("prepare", "predictions", "answer_tokens", "statements"):
                assert stats[k] == n, f"{label}: {k} {stats[k]}/{n}"
        assert report[label]["max_asked"] <= CAP, f"{label}: an entity is asked more than {CAP} times"
        assert report[label]["prompts_unique"] == n, label
    out = DATA / (f"check_{which}.json" if pins.TARGET == "qwen3.6-27b" else f"check_{which}_{pins.TARGET}.json")
    out.write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", out)


def stage_manifest(name: str, why: str, limit: int | None, which: str) -> None:
    from bridge_jspace.data import sha256_of

    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    root = pins.REPO_ROOT
    files = {f"{which}/{label}": f for label, f in set_files(which).items()}
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
         "model": pins.model_pin(), "switches": switches(), "sets": [which],
         "items": {k: {"file": str(f.relative_to(root)) if f.is_relative_to(root) else str(f), "sha256": sha256_of(f)}
                   for k, f in files.items()},
         "limit": limit, "format": f"pointer_v1's: {chat.format_note()}", "judge_mode": PV.judge_mode(),
         "judge": f"pointer_v1's: {PV.judge_rule()}; colour answers: the first colour word of the first line",
         "prompts": "base; each source (dissoc, same, redigit); hop1 and hop2 for memory -> prompt",
         "eligibility": "pointer_swap uses scenes with every prompt right in both answer kinds"}  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    PV.RESULTS = RESULTS  # pointer_v1's competence with this module's judge (pointer_v4's, plus colour words)
    PV.said = said
    PV.stage_competence(name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest", "competence"])
    ap.add_argument("--set", dest="which", choices=list(SETS), default="main", help="make, check, manifest")
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    if args.stage == "make":
        stage_make(args.which)
    elif args.stage == "verify":
        stage_verify()
    elif args.stage == "check":
        stage_check(args.which)
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why, args.limit, args.which)
    else:
        assert args.name, "competence needs --name"
        stage_competence(args.name)
