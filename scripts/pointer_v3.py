"""pointer_v3 (D3, "start or end", 2026-10-21): is the statement-slot pointer counted from the START or from the END of
the statement list? (UNVERIFIED background: patching the alt prompt's last tokens at layers 44-50 gives "the answer at
the same statement slot" more often than the answer of bridge alt's statement; pointer_v2 separates order from token
position. Here the alt prompt has one statement MORE or one FEWER than the org prompt, so "the k-th statement from the
start" and "the k-th statement from the end" name different org statements.)

Scene: pointer_v1's statements (animals: "The cow's locker is 5."; elements: "The carbon card is in locker 5.") and filler
sentences of exactly a statement's token length (pointer_v2's pools), so every context is a grid of equal cells. The org
prompt has N = 5 statements; the alt prompt has N + 1 ("more") or N - 1 ("fewer"). Fillers keep the total length equal,
so the question and the tokens after it stay aligned: "more" = org 5 statements + 2 fillers, alt 6 statements + 1
filler (7 cells); "fewer" = org 5 statements + 1 filler, alt 4 statements + 2 fillers (6 cells). The alt prompt asks about
bridge alt q_s, its k-th statement (k from the start), which is its (M - 1 - k)-th from the end (M = its statement count).

Five distinct org statements, one per hypothesis (the filler places are chosen so that all three pointers differ):
  none      d(q_b)                 the org prompt keeps its answer
  identity  d(q_s)                 the answer of bridge alt's statement in the org prompt (bridge alt as a word / key)
  position  d(org k-th from the start)   the slot counted from the start
  end       d(org k-th from the end)     the slot counted from the end
  token     d(org statement at the token offset of the alt's k-th statement)   the same token position
  value     v, a digit not in the org prompt    the alt prompt's own answer
With one statement more or fewer, a filler arrangement where start, end and token point at three different org
statements always exists for some k (make() picks uniformly among them); so all three pointers are separated, and the
org prompt's five statements are exactly: the asked one, bridge alt's, and the three pointed-at ones.

Families on the same scenes (pointer_v1's): memory -> prompt (RL), named -> prompt (DL), memory -> memory (RR, contrast;
its predictions are recalled facts). Controls in the data: "same" (q_b in its slot with its digit, the rest reshuffled
and redigited, same filler places: every hypothesis predicts the base answer) and "redigit" (q_b's digit replaced by
v). Digit policy: lookup digits 0-9; no org or alt digit equals the recalled digit of q_b, q_s or the start- and
end-pointed entities (hard); the token-pointed entity's recalled digit may coincide (recorded in "collisions").

Sets: main, 120 scenes per (domain x "more"/"fewer"), seed 821; the base query's slot cycles first / middle / last
(middle = a random inner slot) where the layouts allow it. Levels "e5more" and "e5fewer" (separate scenes).

Stages:  make --set main | verify | check --set main (tokenizer only) | manifest --name N --why W [--limit K]
         competence --name N (GPU; pointer_v1's competence on these files)
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import pointer_v1 as PV
from scripts import pointer_v2 as P2
from scripts import suite_v1 as S

DATA = pins.DATA_DIR / "pointer_v3"
RESULTS = pins.RESULTS_DIR / "pointer_v3"
FAMILIES = PV.FAMILIES
DOMAINS = P2.DOMAINS  # animals, elements: the topics that passed the earlier gates in every family
TYPES = ("more", "fewer")
DIGITS = tuple(range(10))
N_ENT = 5
FILLERS = {"more": (2, 1), "fewer": (1, 2)}  # (org fillers, alt fillers): equal cell counts
SETS: dict[str, dict[str, Any]] = {"main": {"seed": 821, "n": 120}}


def stmt_cells(total: int, fillers: tuple[int, ...]) -> list[int]:
    """The cells holding statements, in order, when `fillers` are filler cells."""
    return [g for g in range(total) if g not in fillers]


def pointers(typ: str, f_org: tuple[int, ...], f_alt: tuple[int, ...], k: int) -> tuple[int, int, int] | None:
    """(start, end, token): the org statement index each pointer names for the alt's k-th statement, or None if one is
    undefined (outside the org list, or the org cell at that token offset holds a filler)."""
    m = N_ENT + (1 if typ == "more" else -1)
    total = N_ENT + FILLERS[typ][0]
    org, alt = stmt_cells(total, f_org), stmt_cells(total, f_alt)
    start = k if k < N_ENT else None
    end = N_ENT - 1 - (m - 1 - k)
    end = end if 0 <= end < N_ENT else None
    g = alt[k]
    token = org.index(g) if g in org else None
    if start is None or end is None or token is None:
        return None
    return start, end, token


def layouts(typ: str, a: int) -> list[tuple[tuple[int, ...], tuple[int, ...], int, tuple[int, int, int], int]]:
    """Every (org filler cells, alt filler cells, k, (start, end, token), c) with the three pointers distinct, the base
    query a and bridge alt's org slot c the two remaining statements."""
    n_f_org, n_f_alt = FILLERS[typ]
    total = N_ENT + n_f_org
    m = N_ENT + (1 if typ == "more" else -1)
    out = []
    for f_org in itertools.combinations(range(total), n_f_org):
        for f_alt in itertools.combinations(range(total), n_f_alt):
            for k in range(m):
                p = pointers(typ, f_org, f_alt, k)
                if p is None or len(set(p)) < 3 or a in p:
                    continue
                rest = [s for s in range(N_ENT) if s != a and s not in p]
                out += [(f_org, f_alt, k, p, c) for c in rest]
    return out


def slot_plan(rng: random.Random, n: int, typ: str) -> list[int]:
    """The base query's slot: first / middle / last in seeded thirds, among the slots the layouts allow."""
    ok = [a for a in range(N_ENT) if layouts(typ, a)]
    classes = {"first": [a for a in ok if a == 0], "last": [a for a in ok if a == N_ENT - 1],
               "middle": [a for a in ok if 0 < a < N_ENT - 1]}  # fmt: skip
    names = [c for c, v in classes.items() if v]
    out: list[int] = []
    while len(out) < n:
        block = list(names)
        rng.shuffle(block)
        out += [rng.choice(classes[b]) for b in block]
    return out[:n]


def make_scene(rng: random.Random, domain: str, typ: str, a: int) -> dict[str, Any]:
    f_org, f_alt, k, (st, en, tk), c = rng.choice(layouts(typ, a))
    pool_ents = list(PV.DOMAINS[domain]["entities"])
    while True:  # q_b and q_s with different recalled digits (memory -> memory's none vs identity)
        q_b, q_s = rng.sample(pool_ents, 2)
        if PV.rec(domain, q_b) != PV.rec(domain, q_s):
            break
    rest = rng.sample([e for e in pool_ents if e not in (q_b, q_s)], N_ENT - 2)
    ents: list[str] = [""] * N_ENT
    ents[a], ents[c] = q_b, q_s
    for s, e in zip([s for s in range(N_ENT) if not ents[s]], rest, strict=True):
        ents[s] = e
    recalled = {e: PV.rec(domain, e) for e in pool_ents}
    hard = {recalled[e] for e in (q_b, q_s, ents[st], ents[en])}
    pool = [d for d in DIGITS if d not in hard]
    digits = rng.sample(pool, N_ENT)
    value = rng.choice([d for d in pool if d not in digits])
    # the alt prompt: q_s as its k-th statement; "more": the org entities but q_s plus one entity not in the org prompt;
    # "fewer": three of the four other org entities
    others = [e for e in ents if e != q_s]
    if typ == "more":
        extra = [e for e in pool_ents if e not in ents]
        others = rng.sample([*others, rng.choice(extra)], N_ENT)
    else:
        others = rng.sample(others, N_ENT - 2)
    alt = list(others)
    alt.insert(k, q_s)
    alt_digits = rng.sample([d for d in pool if d != value], len(alt) - 1)
    alt_digits.insert(k, value)
    while True:  # the 'same' control
        m_ents = rng.sample([e for e in ents if e != q_b], N_ENT - 1)
        m_ents.insert(a, q_b)
        m_digits = rng.sample([d for d in pool if d != digits[a]], N_ENT - 1)
        m_digits.insert(a, digits[a])
        if m_ents != ents:
            break
    n_fill = max(FILLERS[typ])
    fill = rng.sample(P2.FILLER[domain], n_fill)
    return {"q_b": q_b, "q_s": q_s, "ents": ents, "digits": digits, "value": value, "a": a, "c": c, "k": k,
            "start": st, "end": en, "token": tk, "f_org": f_org, "f_alt": f_alt, "fill": fill, "alt": alt,
            "alt_digits": alt_digits, "same": (m_ents, m_digits), "recalled": recalled}  # fmt: skip


def context(domain: str, ents: list[str], digits: list[int], fill: list[str], fillers: tuple[int, ...]) -> str:
    """Statements in order with the filler sentences in the given cells (the first filler cell gets fill[0], ...)."""
    st = iter(PV.DOMAINS[domain]["statement"].format(e=e, d=d) for e, d in zip(ents, digits, strict=True))
    fl = iter(fill)
    total = len(ents) + len(fillers)
    return " ".join(next(fl) if g in fillers else next(st) for g in range(total))


def items_for(sc: dict[str, Any], domain: str, typ: str, i: int) -> dict[str, dict]:
    d = PV.DOMAINS[domain]
    q_b, q_s, ents, digits = sc["q_b"], sc["q_s"], sc["ents"], sc["digits"]
    look = dict(zip(ents, digits, strict=True))
    alt_look = dict(zip(sc["alt"], sc["alt_digits"], strict=True))
    rec = sc["recalled"]
    level = f"e{N_ENT}{typ}"
    base_ctx = context(domain, ents, digits, sc["fill"], sc["f_org"])
    alt_ctx = context(domain, sc["alt"], sc["alt_digits"], sc["fill"], sc["f_alt"])
    m_ents, m_digits = sc["same"]
    r_digits = list(digits)
    r_digits[sc["a"]] = sc["value"]
    out = {}
    for fam in FAMILIES:
        lookup = fam != "RR"
        if fam == "DL":
            question, alt_q = d["DL"].format(e=q_b), d["DL"].format(e=q_s)
        else:
            question, alt_q = d[fam].format(cue=PV.cue(domain, q_b)), d[fam].format(cue=PV.cue(domain, q_s))
        if lookup:
            pred = {"none": look[q_b], "identity": look[q_s], "position": digits[sc["start"]],
                    "end": digits[sc["end"]], "token": digits[sc["token"]], "value": alt_look[q_s]}  # fmt: skip
        else:
            pred = {"none": rec[q_b], "identity": rec[q_s], "position": rec[ents[sc["start"]]],
                    "end": rec[ents[sc["end"]]], "token": rec[ents[sc["token"]]], "value": rec[q_s]}  # fmt: skip
        answer = look[q_b] if lookup else rec[q_b]
        pred_s = {h: str(v) for h, v in pred.items()}
        keys = [h for h in pred_s if not (fam == "RR" and h == "value")]
        sources = {
            "dissoc": {"context": alt_ctx, "question": alt_q, "answer": str(alt_look[q_s] if lookup else rec[q_s]),
                       "entities": sc["alt"], "digits": sc["alt_digits"], "query": q_s, "query_slot": sc["k"],
                       "filler_cells": list(sc["f_alt"]), "predictions": pred_s},
            "same": {"context": context(domain, m_ents, m_digits, sc["fill"], sc["f_org"]), "question": question,
                     "answer": str(answer), "entities": m_ents, "digits": m_digits, "query": q_b, "query_slot": sc["a"],
                     "filler_cells": list(sc["f_org"]), "predictions": {h: str(answer) for h in pred_s}},
            "redigit": {"context": context(domain, ents, r_digits, sc["fill"], sc["f_org"]), "question": question,
                        "answer": str(sc["value"] if lookup else answer), "entities": ents, "digits": r_digits,
                        "query": q_b, "query_slot": sc["a"], "filler_cells": list(sc["f_org"]),
                        "predictions": {h: str(answer) for h in pred_s} | ({"value": str(sc["value"])} if lookup else {})},
        }  # fmt: skip
        item = {
            "id": f"{domain}-{fam}-{level}-{i:04d}", "family": fam, "domain": domain, "level": level, "type": typ,
            "scene": f"{domain}-{level}-{i:04d}", "n_entities": N_ENT, "n_filler": len(sc["f_org"]),
            "filler_cells": list(sc["f_org"]), "entities": ents, "digits": digits,
            "recalled": {e: rec[e] for e in {*ents, *sc["alt"]}}, "query": q_b,
            "cue": q_b if fam == "DL" else PV.cue(domain, q_b),
            "slots": {"query": sc["a"], "identity": sc["c"], "position": sc["start"], "end": sc["end"],
                      "token": sc["token"]},
            "context": base_ctx, "question": question, "answer": str(answer), "answer_kind": "digit",
            "sources": sources, "distinct": len({pred_s[h] for h in keys}) == len(keys),
            "collisions": sorted({x for x in digits if x in {rec[e] for e in ents}}),
        }  # fmt: skip
        if fam != "DL":
            item["hop1"] = {"question": d["hop_cue"].format(cue=PV.cue(domain, q_b)), "answer": q_b, "kind": domain}
            hop2 = d["DL"].format(e=q_b) if lookup else d["hop_recall"].format(e=q_b)
            item["hop2"] = {"question": hop2, "answer": str(answer), "kind": "digit"}
        out[fam] = item
    return out


def generate(which: str) -> dict[str, tuple[Path, list[dict], str]]:
    spec = SETS[which]
    out: dict[str, tuple[Path, list[dict], str]] = {}
    for di, domain in enumerate(DOMAINS):
        for ti, typ in enumerate(TYPES):
            seed = spec["seed"] * 100 + 10 * di + ti
            rng = random.Random(seed)
            plan = slot_plan(rng, spec["n"], typ)
            cells: dict[str, list[dict]] = collections.defaultdict(list)
            seen: set[str] = set()
            i = 0
            while i < spec["n"]:
                sc = make_scene(rng, domain, typ, plan[i])
                key = context(domain, sc["ents"], sc["digits"], sc["fill"], sc["f_org"])
                if key in seen:
                    continue
                seen.add(key)
                for fam, item in items_for(sc, domain, typ, i).items():
                    cells[fam].append(item)
                i += 1
            note = (
                f"scripts/pointer_v3.py make --set {which} (seed {seed}: {domain}, alt prompt with one statement {typ})"
            )
            for fam, items in cells.items():
                label = f"{domain}_{fam}_e{N_ENT}{typ}"
                out[label] = (DATA / which / f"{label}.json", items, note)
    return out


def set_files(which: str) -> dict[str, Path]:
    return {
        f"{d}_{f}_e{N_ENT}{t}": DATA / which / f"{d}_{f}_e{N_ENT}{t}.json"
        for d in DOMAINS
        for f in FAMILIES
        for t in TYPES
    }


def level_name(level: str) -> str:
    """'e5more' -> '5 statements, the alt prompt has 6' (pointer_swap's figure titles)."""
    typ = level[2:]
    return f"5 statements, the alt prompt has {N_ENT + 1 if typ == 'more' else N_ENT - 1}"


# ---- checks (tokenizer only) ----------------------------------------------------------------------------------------


def check_item(tok, item: dict) -> dict[str, bool]:
    """Equal cells; every source token-aligned with the org prompt (same length, same question span); the predictions'
    slots; the token pointer's org statement starts exactly where the alt's k-th statement starts."""
    ids, starts, q = P2.cells_of(tok, item, item["context"], item["question"])
    width = {starts[i + 1] - starts[i] for i in range(len(starts) - 1)}
    out = {"equal_cells": len(width) == 1}
    alt = item["sources"]["dissoc"]
    for src, s in item["sources"].items():
        s_ids, _s_starts, s_q = P2.cells_of(tok, item, s["context"], s["question"])
        out[f"{src}_aligned"] = len(s_ids) == len(ids) and s_q == q and bool(S.changed(ids, s_ids))
    a_starts = P2.cells_of(tok, item, alt["context"], alt["question"])[1]  # every cell (statements and fillers)
    org_cells = stmt_cells(len(starts), tuple(item["filler_cells"]))
    alt_cells = stmt_cells(len(a_starts), tuple(alt["filler_cells"]))
    sl, k = item["slots"], alt["query_slot"]
    m = len(alt["entities"])
    pd, dg = alt["predictions"], item["digits"]
    out["pointers"] = (
        sl["position"] == k
        and sl["end"] == N_ENT - 1 - (m - 1 - k)
        and a_starts[alt_cells[k]] == starts[org_cells[sl["token"]]]
        and len({sl["query"], sl["identity"], sl["position"], sl["end"], sl["token"]}) == 5
        and alt["entities"][k] == alt["query"] == item["entities"][sl["identity"]]
    )
    if item["family"] != "RR":
        out["predictions"] = (
            pd["position"] == str(dg[sl["position"]]) and pd["end"] == str(dg[sl["end"]])
            and pd["token"] == str(dg[sl["token"]]) and int(pd["value"]) not in dg
            and len(set(pd.values())) == len(pd)
        )  # fmt: skip
    else:
        out["predictions"] = pd["none"] != pd["identity"]
    rec = item["recalled"]
    hard = {
        rec[e] for e in (item["query"], alt["query"], item["entities"][sl["position"]], item["entities"][sl["end"]])
    }
    out["hard_collision_free"] = not (set(dg) & hard) and not (set(alt["digits"]) & hard)
    return out


def stage_make(which: str) -> None:
    tok = PV.tokenizer()
    P2.check_filler(tok)
    for _label, (path, items, note) in generate(which).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        assert not path.exists(), f"{path} exists; data files are written once"
        head = {"family": items[0]["family"], "domain": items[0]["domain"], "level": items[0]["level"],
                "generator": note, "format": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
        body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)
        path.write_text(json.dumps(head, indent=1)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")
        print("wrote", path, len(items))


def stage_verify() -> None:
    for which in SETS:
        for label, (path, items, _) in generate(which).items():
            if not path.exists():
                print(which, label, "no file yet")
                continue
            same = PV.load_file(path) == items
            print(which, label, "same" if same else "DIFFERENT")
            assert same, f"{label}: the generator no longer reproduces {path}"


def stage_check(which: str) -> None:
    tok = PV.tokenizer()
    P2.check_filler(tok)
    report: dict[str, Any] = {}
    for label, path in set_files(which).items():
        items = PV.load_file(path)
        stats: collections.Counter = collections.Counter()
        slot_class: collections.Counter = collections.Counter()
        for it in items:
            for k, v in check_item(tok, it).items():
                stats[k] += bool(v)
            a = it["slots"]["query"]
            slot_class["first" if a == 0 else "last" if a == N_ENT - 1 else "middle"] += 1
        n = len(items)
        report[label] = {"n": n, **stats, "slot_class": dict(slot_class),
                         "prompts_unique": len({it["context"] + it["question"] for it in items})}  # fmt: skip
        print(label, json.dumps(report[label]))
        for k in ("equal_cells", "dissoc_aligned", "same_aligned", "redigit_aligned", "pointers", "predictions",
                  "hard_collision_free"):  # fmt: skip
            assert stats[k] == n, f"{label}: {k} {stats[k]}/{n}"
        assert report[label]["prompts_unique"] == n, label
    out = DATA / f"check_{which}.json"
    out.write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", out)


def stage_manifest(name: str, why: str, limit: int | None) -> None:
    from bridge_jspace.data import sha256_of

    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    files = {f"main/{label}": f for label, f in set_files("main").items()}
    m = {"exp": "pointer_v3", "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
         "model": pins.model_pin(), "sets": ["main"],
         "items": {k: {"file": str(f.relative_to(pins.REPO_ROOT)), "sha256": sha256_of(f)} for k, f in files.items()},
         "limit": limit, "format": "pointer_v1's competence: base, each source, the steps alone; greedy and answer read",
         "eligibility": "pointer_swap uses items with every prompt right"}  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    PV.RESULTS = RESULTS  # pointer_v1's competence, reading this run's manifest and writing under results/pointer_v3
    PV.stage_competence(name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest", "competence"])
    ap.add_argument("--set", default="main", choices=list(SETS))
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    if args.stage == "make":
        stage_make(args.set)
    elif args.stage == "verify":
        stage_verify()
    elif args.stage == "check":
        stage_check(args.set)
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why, args.limit)
    else:
        assert args.name, "competence needs --name"
        stage_competence(args.name)
