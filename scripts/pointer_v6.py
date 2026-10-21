"""pointer_v6 (D3, 2026-10-21): is the last tokens' address "the Nth statement", a place in the text, or a distance
back from the question? And do long statements make the count worse? (Dan's hypotheses, 21 Oct: a relative shift
matters more than an absolute one; longer sentences give more errors.)

Scene: pointer_v4's statements (85 entities, 3 topics, 3 x 3 wordings, held-out split) and one extra sentence of
exactly a statement's token length (pointer_v4x's fillers). The same scene is built under four layouts (levels), so
every level has the same entities, digits and questions:
  e5-still  the extra sentence in the same place (before the list or before the question) in the org and alt prompts
  e5-abs    ABSOLUTE SHIFT: the extra sentence before the list in one prompt only. Bridge alt's statement keeps its
            order index and its distance back from the question, and sits at the token position of the org statement
            next to the same slot (token).
  e5-rel    RELATIVE SHIFT: the extra sentence between the list and the question in one prompt only. Order index and
            token position stay; the distance back from the question names the org statement next to the same slot
            (back).
  e5-long   e5-still with every statement about twice as long: a trailing clause (the same clauses, cell by cell, in
            the org and alt prompts, so they stay token-aligned).
The moved statement m is the same org neighbour (k - 1 or k + 1) in e5-abs and e5-rel: with m = k + 1 the alt prompt
has the sentence before its list (abs) and the org prompt has it before its question (rel); with m = k - 1 the other
way round. e5-abs and e5-rel prompts differ in length by one sentence: pointer_swap patches them aligned from the end
(items carry align = "end").
Predictions: none / identity (bridge alt's statement in the org) / position (the org's k-th) / token (e5-abs) or back
(e5-rel) (the org's m-th) / value (the alt prompt's answer, not in the org prompt). Families: memory -> prompt (RL),
named -> prompt (DL). Controls in the data: "same" (q_b in its slot with its digit, the rest reshuffled and redigited,
the org layout) and "redigit". Cap: the asked entity cycles through the askable pool; at most 12 scenes per entity.

Sets: main, up to 150 scenes per topic (x 4 levels x 2 families), seed 861. Files:
data/pointer_v6/main/<topic>_<family>_<level>.json.

Stages:  make | verify | check (tokenizer only; BJ_TARGET picks the tokenizer) | manifest --name N --why W [--limit K]
         competence --name N (GPU) | errors --name N (CPU: plain answers right, long vs still, from a competence run)
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
from scripts import pointer_v2 as P2
from scripts import pointer_v4 as P4
from scripts import pointer_v4x as X

EXP = "pointer_v6"
DATA = Path(os.environ.get("BJ_POINTER_V6_DATA", str(pins.DATA_DIR / EXP)))
RESULTS = pins.RESULTS_DIR / EXP
FAMILIES = ("RL", "DL")
DOMAINS = P4.DOMAINS
LEVELS = ("e5-still", "e5-abs", "e5-rel", "e5-long")
DIGITS = tuple(range(10))
N_ENT = 5
CAP = P4.CAP
SETS: dict[str, dict[str, Any]] = {"main": {"seed": 861, "n": 150}}
# Trailing clauses for e5-long: no digits, no entity of any topic, no container or question words, no '. ' inside.
CLAUSES = (
    "as noted in the old inventory that was updated last spring",
    "according to the list that the office manager put up by the door",
    "as confirmed again during the review earlier this week",
    "as written on the faded label stuck to the side",
    "following the change that was agreed at the last staff meeting",
    "as recorded in the notebook on the shelf upstairs",
    "as everyone on the team was told during the morning briefing",
    "after the reorganisation that took place over the summer",
    "as shown on the printed sheet pinned to the noticeboard",
    "as the new assistant double-checked on their first day",
)
BANNED = ("drawer", "folder", "file", "chart", "locker", "cabinet", "kept", "holds", "which", "what", "where")


def lengthen(statement: str, clause: str) -> str:
    assert statement.endswith("."), statement
    return f"{statement[:-1]}, {clause}."


def statements(domain: str, t: int, ents: list[str], digits: list[int], clauses: list[str] | None) -> list[str]:
    st = P4.statements(domain, t, ents, digits)
    return [lengthen(s, c) for s, c in zip(st, clauses, strict=True)] if clauses else st


def context(stmts: list[str], filler: str, side: str | None) -> str:
    """The statements with the extra sentence before the list ("before"), before the question ("after") or nowhere."""
    return " ".join([*([filler] if side == "before" else []), *stmts, *([filler] if side == "after" else [])])


def sides(level: str, m: int, k: int, still: str) -> tuple[str | None, str | None]:
    """(org side, alt side) of the extra sentence for a level (the module docstring's layouts)."""
    if level in ("e5-still", "e5-long"):
        return still, still
    if level == "e5-abs":
        return (None, "before") if m == k + 1 else ("before", None)
    assert level == "e5-rel", level
    return ("after", None) if m == k + 1 else (None, "after")


def scene(rng: random.Random, domain: str, pool: list[str], q_b: str, cue_len: dict, t: int) -> dict:
    k = rng.randrange(N_ENT)
    m = rng.choice([x for x in (k - 1, k + 1) if 0 <= x < N_ENT])
    a, c = rng.sample([s for s in range(N_ENT) if s not in (k, m)], 2)
    q_s = rng.choice([e for e in pool if P4.pair_ok(domain, q_b, e, cue_len)])
    others = rng.sample([e for e in pool if e not in (q_b, q_s)], N_ENT - 2)
    ents: list[str] = [""] * N_ENT
    ents[a], ents[c] = q_b, q_s
    for s, e in zip([s for s in range(N_ENT) if not ents[s]], others, strict=True):
        ents[s] = e
    recalled = {e: P4.rec(domain, e) for e in ents}
    hard = {recalled[e] for e in (q_b, q_s, ents[k], ents[m])}
    soft = [d for d in DIGITS if d not in set(recalled.values())]
    dpool, policy = (soft, "soft") if len(soft) >= N_ENT + 1 else ([d for d in DIGITS if d not in hard], "hard")
    digits = rng.sample(dpool, N_ENT)
    value = rng.choice([d for d in dpool if d not in digits])
    alt = rng.sample([e for e in ents if e != q_s], N_ENT - 1)
    alt.insert(k, q_s)
    alt_digits = rng.sample([d for d in dpool if d != value], N_ENT - 1)
    alt_digits.insert(k, value)
    return {"ents": ents, "digits": digits, "value": value, "alt": alt, "alt_digits": alt_digits,
            "filler": rng.choice(X.fillers_for(domain, t)), "still": rng.choice(("before", "after")),
            "clauses": rng.sample(CLAUSES, N_ENT), "slots": {"query": a, "identity": c, "position": k}, "m": m,
            "policy": policy, "recalled": recalled, "same": X.same_control(rng, ents, digits, a, dpool)}  # fmt: skip


def items_for(sc: dict, domain: str, level: str, i: int, templates: tuple[int, int], held: set[str]) -> dict[str, dict]:
    spec = P4.SPEC[domain]
    t, u = templates
    ents, digits = sc["ents"], sc["digits"]
    k, m = sc["slots"]["position"], sc["m"]
    moved = {"e5-abs": "token", "e5-rel": "back"}.get(level)
    sl = dict(sc["slots"]) | ({moved: m} if moved else {})
    q_b, q_s = ents[sl["query"]], ents[sl["identity"]]
    look = dict(zip(ents, digits, strict=True))
    clauses = sc["clauses"] if level == "e5-long" else None
    org_side, alt_side = sides(level, m, k, sc["still"])
    m_ents, m_digits = sc["same"]
    r_digits = list(digits)
    r_digits[sl["query"]] = sc["value"]
    ent_out, tpl_out = q_b in held, P4.HELD_OUT_TEMPLATE in (t, u)

    def src(e: list[str], d: list[int], side: str | None, q: str, query: str, ans: str, preds: dict) -> dict:
        st = statements(domain, t, e, d, clauses)
        return {"context": context(st, sc["filler"], side), "statements": st, "question": q, "answer": ans,
                "entities": e, "digits": d, "query": query, "query_slot": e.index(query), "filler_side": side,
                "predictions": preds}  # fmt: skip

    out = {}
    for fam in FAMILIES:
        target = P4.name_of if fam == "DL" else P4.cue_of
        question, alt_q = (spec["lookups"][u].format(x=target(domain, e)) for e in (q_b, q_s))
        pred = {"none": look[q_b], "identity": look[q_s], "position": digits[k]}
        if moved:
            pred[moved] = digits[m]
        pred["value"] = sc["value"]
        pred_s = {h: str(v) for h, v in pred.items()}
        answer = str(look[q_b])
        sources = {
            "dissoc": src(sc["alt"], sc["alt_digits"], alt_side, alt_q, q_s, str(sc["value"]), pred_s),
            "same": src(m_ents, m_digits, org_side, question, q_b, answer, {h: answer for h in pred_s}),
            "redigit": src(ents, r_digits, org_side, question, q_b, str(sc["value"]),
                           {h: answer for h in pred_s} | {"value": str(sc["value"])}),
        }  # fmt: skip
        st = statements(domain, t, ents, digits, clauses)
        item = {
            "id": f"{domain}-{fam}-{level}-{i:04d}", "family": fam, "domain": domain, "level": level,
            "type": level.split("-")[1], "scene": f"{domain}-{i:04d}", "n_entities": N_ENT, "filler_side": org_side,
            "entities": ents, "digits": digits, "recalled": sc["recalled"], "query": q_b, "cue": target(domain, q_b),
            "slots": sl, "context": context(st, sc["filler"], org_side), "statements": st, "question": question,
            "answer": answer, "answer_kind": "digit", "sources": sources,
            "distinct": len(set(pred_s.values())) == len(pred_s), "digit_policy": sc["policy"],
            "collisions": sorted({x for x in digits if x in sc["recalled"].values()}),
            "templates": {"statement": t, "question": u}, "held_out_entity": ent_out, "held_out_template": tpl_out,
            "cut": "both" if ent_out and tpl_out else "entity" if ent_out else "template" if tpl_out else "neither",
        }  # fmt: skip
        if moved:
            item["align"] = "end"
        if fam == "RL":
            item["hop1"] = {"question": spec["hop_cue"].format(c=spec["candidates"][q_b][1]), "answer": q_b,
                            "kind": domain}  # fmt: skip
            item["hop2"] = {"question": spec["lookups"][u].format(x=P4.name_of(domain, q_b)), "answer": answer,
                            "kind": "digit"}  # fmt: skip
        out[fam] = item
    return out


def generate(which: str, split: dict[str, Any]) -> dict[str, tuple[Path, list[dict], str]]:
    """label -> (file, items, generator note); tokenizer-free given pointer_v4's split.json."""
    spec = SETS[which]
    cells: dict[str, list[dict]] = collections.defaultdict(list)
    notes: dict[str, str] = {}
    for domain in split["used"]:
        info = split["domains"][domain]
        pool, cue_len = info["pool"], info["cue_tokens"]
        held = set(info["held_out_entities"])
        askable = [e for e in pool if any(P4.pair_ok(domain, e, f, cue_len) for f in pool)]
        n = min(spec["n"], CAP * len(askable))
        seed = spec["seed"] * 100 + 10 * list(P4.SPEC).index(domain)
        rng = random.Random(seed)
        seen: set[str] = set()
        q_round: list[str] = []
        for i in range(n):
            if not q_round:  # the cap: the asked entity cycles through the askable pool
                q_round = rng.sample(askable, len(askable))
            q_b = q_round.pop()
            for _ in range(50):  # scenes never repeat within a topic
                templates = (rng.randrange(3), rng.randrange(3))
                sc = scene(rng, domain, pool, q_b, cue_len, templates[0])
                key = " ".join(P4.statements(domain, templates[0], sc["ents"], sc["digits"]))
                if key not in seen:
                    break
            else:
                raise AssertionError(f"{domain}: no new scene for {q_b}")
            seen.add(key)
            for level in LEVELS:
                for fam, item in items_for(sc, domain, level, i, templates, held).items():
                    label = f"{domain}_{fam}_{level}"
                    cells[label].append(item)
                    notes[label] = (
                        f"scripts/pointer_v6.py make (set {which}, seed {seed}: {domain}, {len(askable)} asked)"
                    )
    return {label: (DATA / which / f"{label}.json", items, notes[label]) for label, items in cells.items()}


def set_files(which: str) -> dict[str, Path]:
    return {f"{d}_{f}_{lv}": DATA / which / f"{d}_{f}_{lv}.json" for d in DOMAINS for f in FAMILIES for lv in LEVELS}


def level_name(level: str) -> str:
    """pointer_swap's figure titles."""
    return {"e5-still": "5 statements + 1 extra sentence in the same place in both prompts",
            "e5-abs": "5 statements, an extra sentence before the list in one prompt only (place in the text shifts)",
            "e5-rel": "5 statements, an extra sentence before the question in one prompt only (distance back shifts)",
            "e5-long": "5 long statements + 1 extra sentence in the same place"}[level]  # fmt: skip


# ---- checks (tokenizer only) ----------------------------------------------------------------------------------------


def check_clauses() -> None:
    names = {e.lower() for d in DOMAINS for e in DOMAINS[d]["entities"]}
    for c in CLAUSES:
        words = set(re.findall(r"[a-z]+", c.lower()))
        assert not any(ch.isdigit() for ch in c), c
        assert ". " not in c, c
        assert not words & (names | set(BANNED)), f"{c!r}: {words & (names | set(BANNED))}"


def starts_of(tok, item: dict, part: dict) -> tuple[int, list[int]]:
    """(prompt length in tokens, each statement's first token index), the extra sentence left out."""
    ids, starts, _ = P2.cells_of(tok, item, part["context"], part["question"])
    side = part["filler_side"]
    st = starts[1:] if side == "before" else starts[:-1] if side == "after" else starts
    assert len(st) == N_ENT, (item["id"], len(starts))
    return len(ids), st


def check_item(tok, item: dict) -> dict[str, bool]:
    """Equal cells (not e5-long); prepare() accepts the item (aligned, or aligned from the end for e5-abs / e5-rel);
    the moved statement sits where the level says (same token position, or same distance back); predictions."""
    from scripts import pointer_swap as PS

    org = {"context": item["context"], "question": item["question"], "filler_side": item["filler_side"]}
    alt = item["sources"]["dissoc"]
    n_o, s_o = starts_of(tok, item, org)
    n_a, s_a = starts_of(tok, item, alt)
    _, starts, _ = P2.cells_of(tok, item, item["context"], item["question"])
    out = {
        "equal_cells": item["level"] == "e5-long"
        or len({starts[j + 1] - starts[j] for j in range(len(starts) - 1)}) == 1
    }
    try:
        prep = PS.prepare(item, tok)
        out["prepare"] = True
        out["shift"] = (prep["shift"]["dissoc"] != 0) == (item.get("align") == "end")
        out["controls_aligned"] = prep["shift"]["same"] == prep["shift"]["redigit"] == 0
    except AssertionError:
        out["prepare"] = out["shift"] = out["controls_aligned"] = False
    sl, k = item["slots"], alt["query_slot"]
    ok = sl["position"] == k and alt["entities"][k] == alt["query"] == item["entities"][sl["identity"]]
    if item["level"] == "e5-abs":  # same token position as the org's m-th; same distance back as the org's k-th
        m = sl["token"]
        ok = ok and s_a[k] == s_o[m] and n_a - s_a[k] == n_o - s_o[k] and abs(m - k) == 1
    elif item["level"] == "e5-rel":  # same distance back as the org's m-th; same token position as the org's k-th
        m = sl["back"]
        ok = ok and n_a - s_a[k] == n_o - s_o[m] and s_a[k] == s_o[k] and abs(m - k) == 1
    else:
        ok = ok and n_a == n_o and s_a == s_o
    out["pointers"] = ok and len(set(sl.values())) == len(sl)
    pd, dg = alt["predictions"], item["digits"]
    out["predictions"] = (len(set(pd.values())) == len(pd) and int(pd["value"]) not in dg
                          and all(pd[h] == str(dg[sl[h]]) for h in ("position", "token", "back") if h in sl))  # fmt: skip
    clauses = None
    if item["level"] == "e5-long":
        clauses = [s[len(b) - 1 :].removeprefix(", ").removesuffix(".") for s, b in
                   zip(item["statements"], P4.statements(item["domain"], item["templates"]["statement"],
                                                         item["entities"], item["digits"]), strict=True)]  # fmt: skip
    out["statements"] = item["statements"] == statements(item["domain"], item["templates"]["statement"],
                                                         item["entities"], item["digits"], clauses)  # fmt: skip
    return out


def write_set(path: Path, items: list[dict], note: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; data files are written once"
    head = {"family": items[0]["family"], "domain": items[0]["domain"], "level": items[0]["level"], "generator": note,
            "format": (__doc__ or "").split("\n\n")[1]}  # fmt: skip
    body = ",\n".join(json.dumps(it, ensure_ascii=False) for it in items)
    path.write_text(json.dumps(head, indent=1)[:-2] + ',\n "items": [\n' + body + "\n ]\n}\n")


def stage_make() -> None:
    tok = PV.tokenizer()
    X.check_lengths(tok)
    check_clauses()
    split = P4.load_split()
    assert split, "pointer_v4's split.json is missing"
    for _label, (path, items, note) in generate("main", split).items():
        write_set(path, items, note)
        print("wrote", path, len(items))


def stage_verify() -> None:
    split = P4.load_split()
    assert split, "pointer_v4's split.json is missing"
    for label, (path, items, _) in generate("main", split).items():
        same = PV.load_file(path) == items
        print(label, "same" if same else "DIFFERENT")
        assert same, f"{label}: the generator no longer reproduces {path}"


def stage_check() -> None:
    """Every item under the target's tokenizer (BJ_TARGET); writes check_main.json (another target: check_main_<target>.json)."""
    tok = PV.tokenizer()
    if pins.TARGET == "qwen3.6-27b":  # the pinned lengths are the 27B tokenizer's
        X.check_lengths(tok)
    check_clauses()
    report: dict[str, Any] = {}
    for label, path in set_files("main").items():
        items = PV.load_file(path)
        stats: collections.Counter = collections.Counter()
        for it in items:
            for k, v in check_item(tok, it).items():
                stats[k] += bool(v)
        n = len(items)
        asked = collections.Counter(it["query"] for it in items)
        report[label] = {"n": n, **stats, "entities_asked": len(asked), "max_asked": max(asked.values()),
                         "wordings": len({(it["templates"]["statement"], it["templates"]["question"]) for it in items}),
                         "cuts": dict(collections.Counter(it["cut"] for it in items)),
                         "prompts_unique": len({it["context"] + it["question"] for it in items})}  # fmt: skip
        print(label, json.dumps(report[label]))
        if pins.TARGET == "qwen3.6-27b":
            for k in ("equal_cells", "prepare", "shift", "controls_aligned", "pointers", "predictions", "statements"):
                assert stats[k] == n, f"{label}: {k} {stats[k]}/{n}"
        assert report[label]["max_asked"] <= CAP, f"{label}: an entity is asked more than {CAP} times"
        assert report[label]["prompts_unique"] == n, label
    out = DATA / ("check_main.json" if pins.TARGET == "qwen3.6-27b" else f"check_main_{pins.TARGET}.json")
    out.write_text(json.dumps(report, indent=1) + "\n")
    print("wrote", out)


def stage_manifest(name: str, why: str, limit: int | None) -> None:
    from bridge_jspace.data import sha256_of

    pins.check_run_name(name)
    path = RESULTS / name / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    root = pins.REPO_ROOT
    files = {f"main/{label}": f for label, f in set_files("main").items()}
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "why": why,
         "model": pins.model_pin(), "sets": ["main"],
         "items": {k: {"file": str(f.relative_to(root)) if f.is_relative_to(root) else str(f), "sha256": sha256_of(f)}
                   for k, f in files.items()},
         "limit": limit, "format": f"pointer_v1's: {chat.format_note()}", "judge_mode": PV.judge_mode(),
         "judge": f"pointer_v1's: {PV.judge_rule()}",
         "prompts": "base; each source (dissoc, same, redigit); hop1 and hop2 for memory -> prompt",
         "eligibility": "pointer_swap uses scenes with every prompt right in every level"}  # fmt: skip
    path.write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", path)


def stage_competence(name: str) -> None:
    PV.RESULTS = RESULTS  # pointer_v1's competence with pointer_v4's judge (its topics are pointer_v4's)
    PV.said = P4.said
    PV.stage_competence(name)


def stage_errors(name: str) -> None:
    """Dan's "long statements give more errors": the share of org prompts answered right, e5-long vs e5-still, per
    family pooled over topics and per topic, with the difference's Newcombe 95% interval (the same scenes). Writes
    results/pointer_v6/<name>/analysis-<stamp>/errors.json."""
    from scripts.pointer_swap import newcombe

    run = RESULTS / name
    rows = [json.loads(x) for x in (run / "items.jsonl").read_text().splitlines()]
    k, n = collections.Counter(), collections.Counter()
    for r in rows:
        if r["kind"] != "clean":
            continue
        level = r["id"].split("-", 2)[2].rsplit("-", 1)[0]
        for cut in ("all", r["domain"]):
            n[(r["family"], cut, level)] += 1
            k[(r["family"], cut, level)] += bool(r["correct"])
    out: dict[str, Any] = {}
    for fam in FAMILIES:
        for cut in ("all", *DOMAINS):
            a, b = (fam, cut, "e5-long"), (fam, cut, "e5-still")
            if n[a] and n[b]:
                d = newcombe(k[a], n[a], k[b], n[b])
                out[f"{fam}|{cut}"] = {"long": [k[a], n[a]], "still": [k[b], n[b]], "long_minus_still": [round(x, 4) for x in d],
                                       "more_errors_on_long": d[2] < 0}  # fmt: skip
                print(f"{fam} {cut:10s} long {k[a]}/{n[a]}  still {k[b]}/{n[b]}  diff {100 * d[0]:+.1f} "
                      f"[{100 * d[1]:+.1f}, {100 * d[2]:+.1f}]")  # fmt: skip
    dest = run / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    dest.mkdir()
    (dest / "errors.json").write_text(json.dumps(out, indent=2) + "\n")
    print("wrote", dest / "errors.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["make", "verify", "check", "manifest", "competence", "errors"])
    ap.add_argument("--name")
    ap.add_argument("--why")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    if args.stage == "make":
        stage_make()
    elif args.stage == "verify":
        stage_verify()
    elif args.stage == "check":
        stage_check()
    elif args.stage == "manifest":
        assert args.name, "manifest needs --name"
        assert args.why, "manifest needs --why"
        stage_manifest(args.name, args.why, args.limit)
    else:
        assert args.name, f"{args.stage} needs --name"
        stage_competence(args.name) if args.stage == "competence" else stage_errors(args.name)
