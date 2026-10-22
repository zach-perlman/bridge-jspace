"""pointer_v4 (D3, 2026-10-21): pointer_v1's scenes with many more entities and wordings. pointer_v1 has 16 animals and 6
elements, one wording each, and items of one entity are correlated (D3b: intra-entity correlation ~0.2, effective n ~73
of 175), so more scenes of the same entities add little; more entities and more wordings do.

Scene (pointer_v1's design, unchanged): 5 statements binding an entity to a digit (1-9), in a seeded order; three
families on the same scenes: memory -> prompt (RL: a recalled cue -> the lookup), named -> prompt (DL), memory -> memory
(RR: the cue -> a recalled digit fact; a pointer is useless there: the null). Alt prompts as pointer_v1: "dissoc" (bridge
alt q_s at the slot k where the org prompt has p, with a digit absent from the org prompt: none / identity / position /
value are four distinct digits), "same" (q_b in its slot with its digit, the rest reshuffled: no change under any
hypothesis), "redigit" (q_b's digit replaced by the value).

Topics: candidates in four domains; the entity probe (a quick 27B gate, stage probe) keeps an entity iff its cue ->
entity, entity -> fact and cue -> fact prompts are all answered right; a domain is usable iff >= 16 entities pass; the
first three usable domains in the order below are used (fixed before the probe):
  countries  "the country whose capital is Lima"; fact: the first digit of the international dialling code
  sports     "the sport played with a puck"; fact: players per side (1 for individual sports)
  animals    "the animal known for hooting" (pointer_v1's 16 and 24 more); fact: legs
  body       "the body part that makes urine" (backup); fact: how many a human has (1 or 2)
  (Musical instruments were a candidate: only five string instruments are one token, so they are not used.)
Wording: 3 statement templates and 3 question templates per family and domain (e.g. "The France file is in drawer 5." /
"Drawer 5 holds the France file." / "The file on France is kept in drawer 5."). A scene uses one statement template and
one question template for all its prompts, so the alt prompts stay token-aligned; the asked and the alt entity have
cues of the same token length and different recalled facts.

Held-out split (data/pointer_v4/split.json, written once at make): per domain a seeded third of the probe-passing
entities, and statement template 2 and question template 2, are held out. The fit set (memory -> prompt only, for fitted
readouts such as D3b's pointer direction) uses only the other entities (asked, alt and filler) and templates 0-1, so a
fit never sees a held-out entity or wording. Main items record their cut: held-out entity, held-out wording, both, or
neither. Cap: the asked entity cycles through the domain's askable entities in seeded rounds and a domain has at most 12
scenes per askable entity, so no entity is asked in more than 1/12 of a domain's scenes.

Sets: main (up to 300 scenes per domain, RL/DL/RR, all entities and wordings, seed 841), fit (up to 200 per domain, RL,
fit entities and wordings, seed 842). Files: data/pointer_v4/<set>/<domain>_<family>_e5f0.json.

Stages:  probe --name N --why W (GPU; before make: results/pointer_v4/N/probe.json)
         make --probe N (tokenizer only; writes split.json and both sets)   [--no-probe: every candidate, a smoke,
         only with BJ_POINTER_V4_DATA set elsewhere]   verify   check --set S
         manifest --set S [S ...] --name N --why W [--limit K]   competence --name N (GPU; pointer_v1's competence)
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
from scripts import pointer_v1 as PV
from scripts import suite_v1 as S

EXP = "pointer_v4"
DATA = Path(os.environ.get("BJ_POINTER_V4_DATA", str(pins.DATA_DIR / EXP)))  # a smoke writes elsewhere
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES = PV.FAMILIES  # RL, DL, RR
SOURCES = PV.SOURCES
HYPOTHESES = PV.HYPOTHESES
DIGITS = PV.DIGITS  # 1-9, as pointer_v1
N_ENT = 5
LEVEL = "e5f0"
SETS: dict[str, dict[str, Any]] = {
    "main": {"seed": 841, "n": 300, "families": FAMILIES, "split": "all"},
    # 21 Oct, night: a second draw of main's design (same entities, wordings and split) to check the headline numbers
    # are not one draw's; made with `make_set --set seed2` after the split existed
    "seed2": {"seed": 844, "n": 300, "families": FAMILIES, "split": "all"},
    # 22 Oct, evening (Dan): a third draw for the pre-registered confirmation of finding 5 on fresh scenes
    "seed3": {"seed": 845, "n": 300, "families": FAMILIES, "split": "all"},
    "fit": {"seed": 842, "n": 200, "families": ("RL",), "split": "fit"},
}
CAP = 12  # scenes per askable entity at most: with >= 12 askable entities, none is asked in > 1/12 of the scenes
SPLIT_SEED = 843
HELD_OUT_SHARE = 1 / 3
HELD_OUT_TEMPLATE = 2  # the statement and question template held out of every fit
MIN_ENTITIES = 16
N_DOMAINS = 3

# ---- candidates (entity: (recalled digit, cue phrase)); the probe decides which are used ----------------------------
# Every entity (and every capital) is one token after a space in Qwen3.6-27B's tokenizer: make and check assert it.
COUNTRIES = {  # first digit of the international dialling code; cue: the capital
    "France": (3, "Paris"), "Italy": (3, "Rome"), "Spain": (3, "Madrid"), "Germany": (4, "Berlin"),
    "Japan": (8, "Tokyo"), "Egypt": (2, "Cairo"), "Peru": (5, "Lima"), "Norway": (4, "Oslo"), "Greece": (3, "Athens"),
    "Russia": (7, "Moscow"), "China": (8, "Beijing"), "Canada": (1, "Ottawa"), "Ireland": (3, "Dublin"),
    "Austria": (4, "Vienna"), "Poland": (4, "Warsaw"), "Portugal": (3, "Lisbon"), "Thailand": (6, "Bangkok"),
    "Kenya": (2, "Nairobi"), "Cuba": (5, "Havana"), "Australia": (6, "Canberra"), "Sweden": (4, "Stockholm"),
    "Finland": (3, "Helsinki"), "Hungary": (3, "Budapest"), "Belgium": (3, "Brussels"), "Turkey": (9, "Ankara"),
    "Iran": (9, "Tehran"), "Iraq": (9, "Baghdad"), "Philippines": (6, "Manila"), "Indonesia": (6, "Jakarta"),
    "Chile": (5, "Santiago"), "Venezuela": (5, "Caracas"), "Denmark": (4, "Copenhagen"), "Korea": (8, "Seoul"),
    "Pakistan": (9, "Islamabad"), "Syria": (9, "Damascus"), "Lebanon": (9, "Beirut"),
}  # fmt: skip
SPORTS = {  # players per side (individual sports 1); cue: "the sport <phrase>" (6 or 7 tokens with the frame)
    "basketball": (5, "with slam dunks"), "hockey": (6, "played with a puck"), "polo": (4, "played on horseback"),
    "baseball": (9, "with home runs and innings"), "volleyball": (6, "with spikes over a net"),
    "softball": (9, "with an underhand pitch"), "surfing": (1, "of riding ocean waves"),
    "climbing": (1, "of scaling rock walls"), "pool": (1, "with cues and pockets"), "diving": (1, "of springboard dives"),
    "bowling": (1, "of knocking down pins"), "tennis": (1, "of the Wimbledon championships"),
    "skiing": (1, "on snowy slopes with poles"), "chess": (1, "of kings and checkmate"),
    "golf": (1, "of putters and greens"), "boxing": (1, "fought with gloves in rings"),
    "swimming": (1, "of freestyle and butterfly"), "fencing": (1, "with foils and masks"),
    "squash": (1, "with shuttlecocks"), "skating": (1, "of figure skating jumps"), "sailing": (1, "of yachts and regattas"),
    "wrestling": (1, "of pins and takedowns"), "marathon": (1, "of long road races"),
}  # fmt: skip
ANIMALS = {  # legs; cue: "the animal known for <phrase>" (pointer_v1's 16 and 24 more)
    **{a: (legs, cue) for a, (legs, cue) in PV.ANIMALS.items()},
    "snake": (0, "hissing"), "dolphin": (0, "its clicks"), "tick": (8, "sucking blood"), "owl": (2, "hooting"),
    "goat": (4, "climbing cliffs"), "elephant": (4, "its trunk"), "fish": (0, "its gills"),
    "whale": (0, "spouting water"), "shark": (0, "its sharp fins"), "ant": (6, "its anthills"),
    "beetle": (6, "its hard shell"), "moth": (6, "circling lamps"), "eagle": (2, "its talons"), "crow": (2, "cawing"),
    "camel": (4, "its humps"), "tiger": (4, "its orange stripes"), "bear": (4, "hibernating"),
    "rabbit": (4, "its long ears"), "deer": (4, "its antlers"), "worm": (0, "wriggling underground"),
    "butterfly": (6, "its caterpillars"), "mosquito": (6, "its itchy bites"), "fox": (4, "its bushy tail"),
    "bat": (2, "hanging upside down"),
}  # fmt: skip
BODY = {  # how many a human has; cue: "the body part <phrase>" (backup domain)
    "heart": (1, "that pumps blood"), "liver": (1, "that makes bile"), "tongue": (1, "that tastes food"),
    "bladder": (1, "that stores urine"), "brain": (1, "that does the thinking"), "stomach": (1, "that digests food"),
    "skull": (1, "that protects the brain"), "nose": (1, "that smells scents"), "spine": (1, "made of stacked vertebrae"),
    "forehead": (1, "above the eyebrows"), "kidney": (2, "that makes urine"), "eyebrow": (2, "above each eye"),
    "cheek": (2, "that blushes"), "lung": (2, "that breathes air"), "knee": (2, "that bends the leg"),
    "elbow": (2, "that bends the arm"), "ankle": (2, "joining foot and leg"), "wrist": (2, "joining hand and arm"),
    "thumb": (2, "that is opposable"), "eye": (2, "that sees colours"), "ear": (2, "that hears sounds"),
}  # fmt: skip

SPEC: dict[str, dict[str, Any]] = {  # in order of preference: the first N_DOMAINS usable ones are used
    "countries": {
        "candidates": COUNTRIES, "cue": "the country whose capital is {c}", "name": "{e}",
        "statements": ("The {e} file is in drawer {d}.", "Drawer {d} holds the {e} file.",
                       "The file on {e} is kept in drawer {d}."),
        "lookups": ("Which drawer holds the file on {x}?", "In which drawer is the file on {x}?",
                    "What drawer keeps the file on {x}?"),
        "recalls": ("What is the first digit of the international dialling code of {x}?",
                    "Which digit does the international dialling code of {x} start with?",
                    "The international dialling code of {x} begins with which digit?"),
        "hop_cue": "Which country has {c} as its capital?",
    },
    "sports": {
        "candidates": SPORTS, "cue": "the sport {c}", "name": "{e}",
        "statements": ("The {e} trophy is in cabinet {d}.", "Cabinet {d} holds the {e} trophy.",
                       "The trophy for {e} is kept in cabinet {d}."),
        "lookups": ("Which cabinet holds the trophy for {x}?", "In which cabinet is the trophy for {x}?",
                    "What cabinet keeps the trophy for {x}?"),
        "recalls": ("How many players per side play {x}?", "In {x}, how many players does each side field?",
                    "What is the number of players per side in {x}?"),
        "hop_cue": "What is the sport {c}?",
    },
    "animals": {
        "candidates": ANIMALS, "cue": "the animal known for {c}", "name": "the {e}",
        "statements": ("The {e}'s locker is {d}.", "Locker {d} belongs to the {e}.",
                       "The {e} keeps its things in locker {d}."),
        "lookups": ("Which locker belongs to {x}?", "In which locker does {x} keep its things?",
                    "What locker is used by {x}?"),
        "recalls": ("How many legs does {x} have?", "What is the number of legs of {x}?", "How many legs has {x} got?"),
        "hop_cue": "Which animal is known for {c}?",
    },
    "body": {
        "candidates": BODY, "cue": "the body part {c}", "name": "the {e}",
        "statements": ("The {e} chart is in folder {d}.", "Folder {d} holds the {e} chart.",
                       "The chart on the {e} is kept in folder {d}."),
        "lookups": ("Which folder holds the chart on {x}?", "In which folder is the chart on {x}?",
                    "What folder keeps the chart on {x}?"),
        "recalls": ("How many of {x} does a human have?", "In a human, how many are there of {x}?",
                    "A human has how many of {x}?"),
        "hop_cue": "What is the body part {c}?",
    },
}  # fmt: skip


def split_file() -> Path:
    return DATA / "split.json"


def load_split() -> dict[str, Any] | None:
    f = split_file()
    return json.loads(f.read_text()) if f.exists() else None


def _domains() -> dict[str, dict[str, Any]]:
    """The domains in use with their entities: the probe-passing pools in split.json once make has run, else every
    candidate of every domain (before make)."""
    sp = load_split()
    if sp is None:
        return {d: {**s, "entities": dict(s["candidates"])} for d, s in SPEC.items()}
    return {
        d: {**SPEC[d], "entities": {e: SPEC[d]["candidates"][e] for e in sp["domains"][d]["pool"]}} for d in sp["used"]
    }


DOMAINS = _domains()


def rec(domain: str, e: str) -> int:
    return SPEC[domain]["candidates"][e][0]


def cue_of(domain: str, e: str) -> str:
    return SPEC[domain]["cue"].format(c=SPEC[domain]["candidates"][e][1])


def name_of(domain: str, e: str) -> str:
    return SPEC[domain]["name"].format(e=e)


# ---- judge (probe, competence) --------------------------------------------------------------------------------------

_said_v1 = PV.said


def said(text: str, kind: str) -> str | None:
    """pointer_v1's judge: the first digit (or number word) of the first non-empty line, or the first entity of the
    domain named by `kind` there."""
    if kind not in SPEC:
        return _said_v1(text, kind)
    lower = {w.lower(): w for w in SPEC[kind]["candidates"]}
    return next((lower[t] for t in re.findall(r"[a-z]+", S.first_line(text)) if t in lower), None)


# ---- the entity probe -----------------------------------------------------------------------------------------------


def probe_prompts() -> list[dict]:
    """Per candidate, no context: cue -> entity, entity -> fact, cue -> fact (the memory -> memory chain)."""
    out = []
    for d, spec in SPEC.items():
        for e, (fact, c) in spec["candidates"].items():
            out += [
                {"domain": d, "entity": e, "step": "cue", "question": spec["hop_cue"].format(c=c), "expected": e,
                 "kind": d},
                {"domain": d, "entity": e, "step": "fact", "question": spec["recalls"][0].format(x=name_of(d, e)),
                 "expected": str(fact), "kind": "digit"},
                {"domain": d, "entity": e, "step": "chain", "question": spec["recalls"][0].format(x=cue_of(d, e)),
                 "expected": str(fact), "kind": "digit"},
            ]  # fmt: skip
    return out


def probe_result(rows: list[dict]) -> dict[str, Any]:
    """Per domain: passing entities (all three steps right), failures by step, usable (>= MIN_ENTITIES pass); and the
    domains used (the first N_DOMAINS usable ones in SPEC's order)."""
    out: dict[str, Any] = {"domains": {}}
    for d in SPEC:
        per: dict[str, dict[str, bool]] = collections.defaultdict(dict)
        for r in rows:
            if r["domain"] == d:
                per[r["entity"]][r["step"]] = r["correct"]
        passed = sorted(e for e, v in per.items() if all(v.values()))
        fail = {e: sorted(s for s, ok in v.items() if not ok) for e, v in per.items() if not all(v.values())}
        out["domains"][d] = {"pass": passed, "fail": fail, "n_pass": len(passed), "n_candidates": len(per),
                             "usable": len(passed) >= MIN_ENTITIES}  # fmt: skip
    out["used"] = [d for d in SPEC if out["domains"][d]["usable"]][:N_DOMAINS]
    return out


def stage_probe(name: str, why: str) -> None:
    import torch

    from bridge_jspace.model import load_model
    from scripts.exp03_brew_swaps import write_jsonl

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    prompts = probe_prompts()
    manifest = {
        "exp": EXP, "run": name, "kind": "entity probe", "why": why, "model": pins.model_pin(),
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_prompts": len(prompts),
        "format": f"{chat.format_note()}; the question and the instruction alone (no context)",
        "judge": "pointer_v1's: the first digit or number word (or the domain's entity) in the first non-empty line of 8 "
        "greedy tokens",
        "rule": f"an entity enters pointer_v4 iff its cue -> entity, entity -> fact and cue -> fact prompts are all right; "
        f"a domain is usable iff >= {MIN_ENTITIES} entities pass; the first {N_DOMAINS} usable domains in the order "
        f"{list(SPEC)} are used",
    }  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    for p in prompts:
        p["ids"] = S.ids(tok, chat.chat_text(tok, f"{p['question']} {S.INSTRUCTION}"))
    by_len: dict[int, list[dict]] = collections.defaultdict(list)
    for p in prompts:
        by_len[len(p["ids"])].append(p)
    for group in by_len.values():
        for i in range(0, len(group), 64):
            chunk = group[i : i + 64]
            texts = model.generate_batch(torch.tensor([p["ids"] for p in chunk], device="cuda"), 8, [{}] * len(chunk))
            for p, t in zip(chunk, texts, strict=True):
                p["continuation"], p["said"] = t, said(t, p["kind"])
                p["correct"] = (p["said"] or "").lower() == p["expected"].lower()
    rows = [{k: v for k, v in p.items() if k != "ids"} for p in prompts]
    write_jsonl(out_dir / "items.jsonl", rows)
    result = probe_result(rows)
    (out_dir / "probe.json").write_text(json.dumps(result, indent=2) + "\n")
    lines = [
        f"used: {result['used']}",
        "",
        "| domain | candidates | pass | usable | failed (step) |",
        "|---|---|---|---|---|",
    ]
    lines += [f"| {d} | {r['n_candidates']} | {r['n_pass']} | {r['usable']} | {json.dumps(r['fail'])} |"
              for d, r in result["domains"].items()]  # fmt: skip
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")
    print((out_dir / "summary.md").read_text())


# ---- scenes ---------------------------------------------------------------------------------------------------------


def make_split(probe: dict[str, Any] | None, tok) -> dict[str, Any]:
    """Pools (probe-passing), each pool's seeded held-out third, the held-out template, the cue token lengths."""
    used = probe["used"] if probe else list(SPEC)[:N_DOMAINS]
    out: dict[str, Any] = {"used": used, "domains": {}}
    for d in used:
        pool = sorted(probe["domains"][d]["pass"]) if probe else sorted(SPEC[d]["candidates"])
        order = list(pool)
        random.Random(SPLIT_SEED + list(SPEC).index(d)).shuffle(order)
        n_out = round(len(order) * HELD_OUT_SHARE)
        out["domains"][d] = {
            "pool": pool, "held_out_entities": sorted(order[:n_out]), "fit_entities": sorted(order[n_out:]),
            "held_out_template": HELD_OUT_TEMPLATE, "cue_tokens": {e: len(S.ids(tok, " " + cue_of(d, e))) for e in pool},
        }  # fmt: skip
    return out


def pair_ok(domain: str, a: str, b: str, cue_len: dict[str, int]) -> bool:
    return a != b and cue_len[a] == cue_len[b] and rec(domain, a) != rec(domain, b)


def make_scene(rng: random.Random, domain: str, pool: list[str], q_b: str, a: int, k: int, cue_len: dict[str, int],
               templates: tuple[int, int]) -> dict[str, Any]:  # fmt: skip
    """pointer_v1's scene with q_b given: q_s a partner of q_b (same cue length, another fact) at slot c, p at k."""
    q_s = rng.choice([e for e in pool if pair_ok(domain, q_b, e, cue_len)])
    rest = [e for e in pool if e not in (q_b, q_s)]
    distinct = [e for e in rest if rec(domain, e) not in (rec(domain, q_b), rec(domain, q_s))]
    p = rng.choice(distinct or rest)
    more = rng.sample([e for e in rest if e != p], N_ENT - 3)
    c = rng.choice([s for s in range(N_ENT) if s not in (a, k)])
    order: list[str] = [""] * N_ENT
    order[a], order[k], order[c] = q_b, p, q_s
    for s, e in zip([s for s in range(N_ENT) if not order[s]], more, strict=True):
        order[s] = e
    recalled = {rec(domain, e) for e in order}
    crit = {rec(domain, e) for e in (q_b, q_s, p)}
    soft = [d for d in DIGITS if d not in recalled]
    pool_d, policy = (soft, "soft") if len(soft) >= N_ENT + 1 else ([d for d in DIGITS if d not in crit], "hard")
    digits = rng.sample(pool_d, N_ENT)
    value = rng.choice([d for d in pool_d if d not in digits])
    s_order = rng.sample([e for e in order if e != q_s], N_ENT - 1)
    s_order.insert(k, q_s)
    s_digits = rng.sample([d for d in pool_d if d != value], N_ENT - 1)
    s_digits.insert(k, value)
    while True:
        m_order = rng.sample([e for e in order if e != q_b], N_ENT - 1)
        m_order.insert(a, q_b)
        m_digits = rng.sample([d for d in pool_d if d != digits[a]], N_ENT - 1)
        m_digits.insert(a, digits[a])
        if m_order != order:
            break
    r_digits = list(digits)
    r_digits[a] = value
    return {"q_b": q_b, "q_s": q_s, "p": p, "slots": {"query": a, "identity": c, "position": k}, "order": order,
            "digits": digits, "value": value, "policy": policy, "templates": templates,
            "dissoc": (s_order, s_digits), "same": (m_order, m_digits), "redigit": (list(order), r_digits)}  # fmt: skip


def statements(domain: str, t: int, order: list[str], digits: list[int]) -> list[str]:
    return [SPEC[domain]["statements"][t].format(e=e, d=d) for e, d in zip(order, digits, strict=True)]


def family_items(
    sc: dict[str, Any], domain: str, i: int, families: tuple[str, ...], held_out: set[str]
) -> dict[str, dict]:
    """The families' items on one scene (pointer_v1's schema), plus the wording, the statements and the held-out cut."""
    spec = SPEC[domain]
    t, u = sc["templates"]
    q_b, q_s, p = sc["q_b"], sc["q_s"], sc["p"]
    order, digits = sc["order"], sc["digits"]
    look = dict(zip(order, digits, strict=True))
    base_st = statements(domain, t, order, digits)
    recalled = {e: rec(domain, e) for e in order}
    ent_out, tpl_out = q_b in held_out, HELD_OUT_TEMPLATE in (t, u)
    out = {}
    for fam in families:
        lookup = fam != "RR"
        tmpl = (spec["lookups"] if lookup else spec["recalls"])[u]
        target = name_of if fam == "DL" else cue_of
        question, alt_q = tmpl.format(x=target(domain, q_b)), tmpl.format(x=target(domain, q_s))
        answer = look[q_b] if lookup else rec(domain, q_b)
        sources = {}
        for src in SOURCES:
            s_order, s_digits = sc[src]
            s_look = dict(zip(s_order, s_digits, strict=True))
            if src == "dissoc":
                pred = ({"none": look[q_b], "identity": look[q_s], "position": look[p], "value": s_look[q_s]} if lookup
                        else {"none": rec(domain, q_b), "identity": rec(domain, q_s), "position": rec(domain, p),
                              "value": rec(domain, q_s)})  # fmt: skip
                s_q, s_query, s_answer = alt_q, q_s, (s_look[q_s] if lookup else rec(domain, q_s))
            else:
                pred = {h: answer for h in HYPOTHESES}
                if src == "redigit" and lookup:
                    pred["value"] = s_look[q_b]
                s_q, s_query, s_answer = question, q_b, (s_look[q_b] if lookup else rec(domain, q_b))
            st = statements(domain, t, s_order, s_digits)
            sources[src] = {"context": " ".join(st), "statements": st, "question": s_q, "answer": str(s_answer),
                            "entities": s_order, "digits": s_digits, "query": s_query,
                            "query_slot": s_order.index(s_query), "predictions": {h: str(v) for h, v in pred.items()}}  # fmt: skip
        pd = sources["dissoc"]["predictions"]
        keys = HYPOTHESES if lookup else ("none", "identity", "position")
        item = {
            "id": f"{domain}-{fam}-{LEVEL}-{i:04d}", "family": fam, "domain": domain, "level": LEVEL,
            "scene": f"{domain}-{LEVEL}-{i:04d}", "n_entities": N_ENT, "n_filler": 0, "entities": order,
            "digits": digits, "recalled": recalled, "query": q_b, "cue": target(domain, q_b), "slots": sc["slots"],
            "context": " ".join(base_st), "statements": base_st, "question": question, "answer": str(answer),
            "answer_kind": "digit", "sources": sources, "distinct": len({pd[h] for h in keys}) == len(keys),
            "digit_policy": sc["policy"], "collisions": sorted({x for x in digits if x in recalled.values()}),
            "templates": {"statement": t, "question": u}, "held_out_entity": ent_out, "held_out_template": tpl_out,
            "cut": "both" if ent_out and tpl_out else "entity" if ent_out else "template" if tpl_out else "neither",
        }  # fmt: skip
        if fam != "DL":
            item["hop1"] = {"question": spec["hop_cue"].format(c=spec["candidates"][q_b][1]), "answer": q_b,
                            "kind": domain}  # fmt: skip
            hop2 = (spec["lookups"] if lookup else spec["recalls"])[u].format(x=name_of(domain, q_b))
            item["hop2"] = {"question": hop2, "answer": str(answer), "kind": "digit"}
        out[fam] = item
    return out


def set_plan(which: str, split: dict[str, Any], domain: str) -> tuple[list[str], list[int], list[str], int]:
    """(entity pool, templates, askable entities, number of scenes) of one domain in a set."""
    info = split["domains"][domain]
    if SETS[which]["split"] == "fit":
        pool, tpls = info["fit_entities"], [x for x in range(3) if x != HELD_OUT_TEMPLATE]
    else:
        pool, tpls = info["pool"], [0, 1, 2]
    cue_len = info["cue_tokens"]
    askable = [e for e in pool if any(pair_ok(domain, e, f, cue_len) for f in pool)]
    return pool, tpls, askable, min(SETS[which]["n"], CAP * len(askable))


def generate(which: str, split: dict[str, Any]) -> dict[str, tuple[Path, list[dict], str]]:
    """label -> (file, items, generator note); tokenizer-free given split.json."""
    spec = SETS[which]
    out: dict[str, tuple[Path, list[dict], str]] = {}
    pairs = [(a, k) for a in range(N_ENT) for k in range(N_ENT) if a != k]
    for domain in split["used"]:
        pool, tpls, askable, n = set_plan(which, split, domain)
        assert len(askable) >= 2, f"{domain}: fewer than 2 askable entities"
        cue_len = split["domains"][domain]["cue_tokens"]
        held = set(split["domains"][domain]["held_out_entities"])
        seed = spec["seed"] * 100 + list(SPEC).index(domain)
        rng = random.Random(seed)
        cells: dict[str, list[dict]] = collections.defaultdict(list)
        seen: set[str] = set()
        q_round: list[str] = []
        slot_round: list[tuple[int, int]] = []
        for i in range(n):
            if not q_round:  # the asked entity cycles through the askable pool in seeded rounds: the cap
                q_round = rng.sample(askable, len(askable))
            q_b = q_round.pop()
            for _ in range(50):  # contexts never repeat within a domain
                if not slot_round:
                    slot_round = rng.sample(pairs, len(pairs))
                a, k = slot_round.pop()
                sc = make_scene(rng, domain, pool, q_b, a, k, cue_len, (rng.choice(tpls), rng.choice(tpls)))
                key = " ".join(statements(domain, sc["templates"][0], sc["order"], sc["digits"]))
                if key not in seen:
                    break
            else:
                raise AssertionError(f"{domain}: no new scene for {q_b}")
            seen.add(key)
            for fam, item in family_items(sc, domain, i, spec["families"], held).items():
                cells[fam].append(item)
        note = f"scripts/pointer_v4.py make (set {which}, seed {seed}: {domain}, {len(pool)} entities, {len(askable)} asked)"
        for fam, items in cells.items():
            label = f"{domain}_{fam}_{LEVEL}"
            out[label] = (DATA / which / f"{label}.json", items, note)
    return out


def set_files(which: str) -> dict[str, Path]:
    return {
        f"{d}_{f}_{LEVEL}": DATA / which / f"{d}_{f}_{LEVEL}.json" for d in DOMAINS for f in SETS[which]["families"]
    }


def level_name(level: str) -> str:
    return "5 statements, 3 wordings per topic"


# ---- checks (tokenizer only) ----------------------------------------------------------------------------------------


def check_tokens(tok) -> None:
    for d, spec in SPEC.items():
        bad = [e for e in spec["candidates"] if len(S.ids(tok, " " + e)) != 1]
        assert not bad, f"{d}: not one token: {bad}"
    bad = [c for _, c in COUNTRIES.values() if len(S.ids(tok, " " + c)) != 1]
    assert not bad, f"countries: capitals not one token: {bad}"


def check_item(tok, item: dict) -> dict[str, bool]:
    base = S.ids(tok, S.render(tok, item["context"], item["question"]))
    out: dict[str, bool] = {}
    for src, s in item["sources"].items():
        ids = S.ids(tok, S.render(tok, s["context"], s["question"]))
        out[f"{src}_aligned"] = len(ids) == len(base) and bool(S.changed(base, ids))
    pd, dg, sl = item["sources"]["dissoc"]["predictions"], item["digits"], item["slots"]
    if item["family"] != "RR":
        out["predictions"] = (len(set(pd.values())) == 4 and pd["position"] == str(dg[sl["position"]])
                              and pd["identity"] == str(dg[sl["identity"]]) and int(pd["value"]) not in dg)  # fmt: skip
    else:
        out["predictions"] = pd["none"] != pd["identity"]
    out["statements"] = item["context"] == " ".join(item["statements"])
    return out


def write_set(path: Path, items: list[dict], note: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; data files are written once"
    head = {"family": items[0]["family"], "domain": items[0]["domain"], "level": items[0]["level"], "generator": note,
            "format": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)
    path.write_text(json.dumps(head, indent=1)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")


def stage_make(probe_run: str | None) -> None:
    from bridge_jspace.data import sha256_of

    tok = PV.tokenizer()
    check_tokens(tok)
    assert load_split() is None, f"{split_file()} exists; the split is written once"
    probe_path = RESULTS / probe_run / "probe.json" if probe_run else None
    split = make_split(json.loads(probe_path.read_text()) if probe_path else None, tok)
    split["probe"] = {"run": probe_run, "sha256": sha256_of(probe_path) if probe_path else None}
    split["rule"] = (f"held out per domain: a third of the pool (seed {SPLIT_SEED}) and template {HELD_OUT_TEMPLATE} "
                     "(statement and question); the fit set uses neither")  # fmt: skip
    split_file().parent.mkdir(parents=True, exist_ok=True)
    split_file().write_text(json.dumps(split, indent=1) + "\n")
    print("wrote", split_file(), "used", split["used"], {d: len(v["pool"]) for d, v in split["domains"].items()})
    for which in ("main", "fit"):
        for _label, (path, items, note) in generate(which, split).items():
            write_set(path, items, note)
            print("wrote", path, len(items))


def stage_make_set(which: str) -> None:
    """A set added after the split was written (seed2): the same split, entities and wordings, a new draw."""
    tok = PV.tokenizer()
    check_tokens(tok)
    split = load_split()
    assert split, "no split.json: run make first"
    for _label, (path, items, note) in generate(which, split).items():
        write_set(path, items, note)
        print("wrote", path, len(items))


def stage_verify() -> None:
    split = load_split()
    assert split, "no split.json: run make first"
    for which in SETS:
        for label, (path, items, _) in generate(which, split).items():
            same = PV.load_file(path) == items
            print(which, label, "same" if same else "DIFFERENT")
            assert same, f"{label}: the generator no longer reproduces {path}"


def stage_check(which: str) -> None:
    tok = PV.tokenizer()
    check_tokens(tok)
    split = load_split()
    assert split, "no split.json: run make first"
    report: dict[str, Any] = {}
    for label, path in set_files(which).items():
        items = PV.load_file(path)
        stats: collections.Counter = collections.Counter()
        for it in items:
            for k, v in check_item(tok, it).items():
                stats[k] += bool(v)
        n = len(items)
        asked = collections.Counter(it["query"] for it in items)
        dom = items[0]["domain"]
        held = set(split["domains"][dom]["held_out_entities"])
        fit_leak = which == "fit" and any(
            set(it["entities"]) & held or HELD_OUT_TEMPLATE in it["templates"].values() for it in items
        )
        report[label] = {
            "n": n, **stats, "entities_asked": len(asked), "max_share_asked": round(max(asked.values()) / n, 4),
            "wordings": dict(sorted(collections.Counter(f"{it['templates']['statement']}/{it['templates']['question']}"
                                                        for it in items).items())),
            "cuts": dict(collections.Counter(it["cut"] for it in items)), "fit_sees_held_out": fit_leak,
            "prompts_unique": len({it["context"] + it["question"] for it in items}),
        }  # fmt: skip
        print(label, json.dumps(report[label]))
        for k in ("dissoc_aligned", "same_aligned", "redigit_aligned", "predictions", "statements"):
            assert stats[k] == n, f"{label}: {k} {stats[k]}/{n}"
        # the cap is a count; with fewer than CAP askable entities equal shares exceed 1/CAP and that is fine
        assert max(asked.values()) <= CAP, f"{label}: an entity is asked more than {CAP} times"
        assert report[label]["max_share_asked"] <= max(1 / CAP, 1 / len(asked)) + 1e-9, f"{label}: shares unequal"
        assert report[label]["prompts_unique"] == n, f"{label}: repeated prompts"
        assert not fit_leak, f"{label}: the fit set contains a held-out entity or wording"
    out = DATA / f"check_{which}.json"
    out.write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", out)


def stage_manifest(name: str, why: str, sets: list[str], limit: int | None) -> None:
    from bridge_jspace.data import sha256_of

    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    files = {f"{s}/{label}": f for s in sets for label, f in set_files(s).items()}
    root = pins.REPO_ROOT
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
         "model": pins.model_pin(), "sets": sets, "split": str(split_file()),
         "items": {k: {"file": str(f.relative_to(root)) if f.is_relative_to(root) else str(f), "sha256": sha256_of(f)}
                   for k, f in files.items()},
         "limit": limit,
         "format": f"pointer_v1's: {chat.format_note()}; context, newline, question and instruction as the user turn",
         "prompts": "base; each source (dissoc, same, redigit); hop1 (cue -> entity, with the base context) and hop2 "
         "(the lookup with the entity named, or the recalled fact) for RL and RR",
         "judge_mode": PV.judge_mode(), "judge": f"pointer_v1's: {PV.judge_rule()} (the domain's entities for hop1)",
         "eligibility": "pointer_swap and pointer_fit use items with every prompt right"}  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    PV.RESULTS = RESULTS  # pointer_v1's competence, with this module's judge (its domains are not pointer_v1's)
    PV.said = said
    PV.stage_competence(name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["probe", "make", "make_set", "verify", "check", "manifest", "competence"])
    ap.add_argument("--set", dest="sets", nargs="+", choices=list(SETS), default=["main"])
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--probe", default=None, help="make: the entity-probe run whose passing entities are used")
    ap.add_argument("--no-probe", action="store_true", help="make: every candidate (a smoke; set BJ_POINTER_V4_DATA)")
    ap.add_argument("--limit", type=int, default=None, help="manifest: the first K items per file (a smoke)")
    args = ap.parse_args()
    if args.stage == "probe":
        assert args.name, "probe needs --name"
        assert args.why, "probe needs --why"
        stage_probe(args.name, args.why)
    elif args.stage == "make":
        assert bool(args.probe) != args.no_probe, "make needs --probe RUN or --no-probe"
        assert not (args.no_probe and DATA == pins.DATA_DIR / EXP), (
            "--no-probe writes only outside data/ (BJ_POINTER_V4_DATA)"
        )
        stage_make(args.probe)
    elif args.stage == "make_set":
        for s in args.sets:
            stage_make_set(s)
    elif args.stage == "verify":
        stage_verify()
    elif args.stage == "check":
        for s in args.sets:
            stage_check(s)
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why, args.sets, args.limit)
    else:
        assert args.name, "competence needs --name"
        stage_competence(args.name)
