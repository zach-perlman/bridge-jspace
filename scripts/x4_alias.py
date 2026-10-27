"""x4_alias (X4, jobs/c3/X4.md): does the lookup's independence from the J++ part need the locker key to match the
bridge word verbatim?

Scenes: alias_pointer_v1's main scenes (5 entities, their locker statements in one surface form per condition, paired
by scene): animals in English (same, the verbatim reference) and in French / Spanish / German (xlang, translated);
elements in English (same) and by chemical symbol (syn, the positive control: the match needs knowledge). X0's frame is
added by this harness (Dan, 24 Oct ~21:00): after the 5 statements, 3 people each pick one entity in English ("Iris
picked the dog."); the lookup asks "Which locker belongs to Iris's pick?", the recall "How many legs does Iris's pick
have?" (animals) or "What is the atomic number of Iris's pick?" (elements), on the identical context. The alt (single
change): the asked person's pick becomes an entity nobody picks (one of the 2 unpicked; its first mention is then its own
locker statement), one token at the bridge's position. People, picks, their order and the alt are drawn per scene from a
seed shared by the scene's conditions, so a scene's conditions differ only in the statements' text.

Eligibility per reader (Dan): every item gets both readers on the identical edit; a reader's cells use the items where
it answers org and alt right (said and read) and, for the recall, where its org and alt answers differ (animals: only
bird <-> mammal pairs). Gate: unedited org accuracy (decisive read) >= 0.80 per condition and reader.

Stages:
  plan     tokenizer only: cases per condition, drops, recall-eligible pairs
  probe    GPU, forward passes only: org states at the bridge word, the predicted layer; probe (b) for the index of the
           bridge's locker statement within each condition (cross-validated by entity) and trained on the verbatim
           scenes, tested on the translated / symbol scenes (transfer)
  run      GPU: X0's arms at the bridge word (whole, without the J++ part k = 25, without a random part of its share)
  verdict  CPU: lookup excess per condition, the paired difference alias - verbatim (bootstrap over entities), the
           graded rules of X4.md; the recall's cells on its eligible items
"""

from __future__ import annotations

import argparse
import collections
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X

EXP = "x4_alias"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "X4.md"
DATA = pins.DATA_DIR / "alias_pointer_v1" / "main"
CONDITIONS = {"animals": ("same", "xlang"), "elements": ("same", "syn")}
PEOPLE = ("Iris", "Noah", "Peter", "Maria", "Liam", "Ella", "Oscar", "Rose", "Sam", "Beth", "Kate", "Victor")
N_PICKS, SEED = 3, 2910
RECALL_Q = {"animals": "How many legs does {p}'s pick have?", "elements": "What is the atomic number of {p}'s pick?"}
LOOKUP_Q = "Which locker belongs to {p}'s pick?"
HOLD, NOT_NEEDED = 0.20, 0.10  # graded rules on excess(alias) - excess(verbatim), X4.md
C_MIN = 30  # items eligible for both readers below which C is not reported (X4.md)


def load(domain: str, condition: str) -> list[dict]:
    """alias_pointer_v1's DL items of one domain and condition (one per scene): the statements in that surface form."""
    name = f"{domain}_DL_e5f0{'' if condition == 'same' else '-' + condition}.json"
    data = json.loads((DATA / name).read_text())
    return data if isinstance(data, list) else data["items"]


def frame(item: dict, domain: str) -> dict:
    """X0's frame on one scene: the people, their picks, the asked person, the alt item (an unpicked entity), all drawn
    from the scene's own seed (shared by its conditions)."""
    from scripts import tasks_v2 as T

    rng = random.Random(f"{SEED}|{domain}|{item['scene']}")
    ents = list(item["entities"])
    people = rng.sample(PEOPLE, N_PICKS)
    picked = rng.sample(ents, N_PICKS)
    asked = rng.randrange(N_PICKS)
    free = [e for e in ents if e not in picked]
    rng.shuffle(free)
    dom = T.DOMAINS[domain]
    picks = [f"{p} picked {T.ref(dom, e)}." for p, e in zip(people, picked, strict=True)]
    return {"people": people, "picked": picked, "asked": asked, "alt_options": free, "picks": picks}


def locker_of(item: dict) -> dict[str, int]:
    """entity -> its locker digit, from the scene's slots."""
    return {e: int(d) for e, d in zip(item["entities"], item["digits"], strict=True)}


def statement_index(item: dict) -> dict[str, int]:
    """entity -> the index of its locker statement among the context's statements (slot order)."""
    out = {}
    for i, s in enumerate(item["statements"]):
        hits = [e for e, w in item["surface"].items() if w in s.split()]
        hits = hits or [e for e, w in item["surface"].items() if w.lower() in s.lower()]
        assert len(hits) == 1, f"{item['id']}: statement {s!r} names {hits}"
        out[hits[0]] = i
    return out


def build(tok, domain: str, condition: str, item: dict, fr: dict) -> tuple[dict | None, str | None]:
    """One X4 case (X0's case layout) or the reason it is dropped."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    dom = T.DOMAINS[domain]
    ent_org = fr["picked"][fr["asked"]]
    person = fr["people"][fr["asked"]]
    lock, vals = locker_of(item), dom.values
    context = " ".join(item["statements"]) + " " + " ".join(fr["picks"])
    pick = fr["picks"][fr["asked"]]
    assert context.count(pick) == 1, f"{item['id']}: the asked pick is not once"
    why = "no unpicked entity aligns"
    for ent_alt in fr["alt_options"]:
        alt_pick = pick.replace(T.ref(dom, ent_org), T.ref(dom, ent_alt))
        alt_context = context.replace(pick, alt_pick)
        readers, pos = {}, None
        for w, q, ans, cf in ((X.LOOKUP, LOOKUP_Q, lock[ent_org], lock[ent_alt]),
                              (X.RECALL, RECALL_Q[domain], vals[ent_org], vals[ent_alt])):  # fmt: skip
            question = q.format(p=person)
            ids = {}
            for v, ctx, ent in (("org", context, ent_org), ("alt", alt_context, ent_alt)):
                text = T.render(tok, {"context": ctx, "question": question, "kind": "digit", "format": "prose"})
                enc = raw_encoding(tok, text, offsets=True)
                sent = alt_pick if v == "alt" else pick
                w0 = text.index(ctx) + ctx.index(sent) + sent.rindex(ent)
                ids[v] = (list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(ent)))
            (ids_org, p_org), (ids_alt, p_alt) = ids["org"], ids["alt"]
            if len(p_org) != 1 or p_alt != p_org or S.changed(ids_org, ids_alt) != [p_org[0]]:
                why = "the bridge or the alt is not one token at one position"
                break
            pos = p_org[0]
            tok_a, tok_b = (S.answer_token(tok, str(a), "digit") for a in (ans, cf))
            readers[w] = {"id": f"{w}-{domain}-{condition}-{item['scene']}", "question": question, "answer": str(ans),
                          "cf_answer": str(cf), "ids": {"org": ids_org, "alt": ids_alt}, "tok_A": tok_a, "tok_b": tok_b,
                          "upstream": False, "answers_differ": ans != cf}  # fmt: skip
        if len(readers) < 2:
            continue
        if any(
            readers[X.LOOKUP]["ids"][v][: pos + 1] != readers[X.RECALL]["ids"][v][: pos + 1] for v in ("org", "alt")
        ):
            why = "the readers' prompts differ before the bridge"
            continue
        idx = statement_index(item)
        return {"scene": f"{domain}|{item['scene']}", "rendering": "chat", "domain": domain, "condition": condition,
                "bridge": ent_org, "cf_bridge": ent_alt, "context": context, "cf_context": alt_context, "pos": pos,
                "upstream": False, "space": S.ids(tok, " "), "readers": readers, "asked_pick": fr["asked"],
                "locker_index": idx[ent_org], "alt_locker_index": idx[ent_alt],
                "surface": item["surface"][ent_org]}, None  # fmt: skip
    return None, why


def build_cases(tok) -> tuple[list[dict], dict]:
    cases, dropped = [], collections.Counter()
    for domain, conds in CONDITIONS.items():
        by_cond = {c: {it["scene"]: it for it in load(domain, c)} for c in conds}
        scenes = sorted(set.intersection(*(set(v) for v in by_cond.values())))
        for s in scenes:
            fr = frame(by_cond[conds[0]][s], domain)  # the frame comes from the scene, the same in every condition
            for c in conds:
                case, why = build(tok, domain, c, by_cond[c][s], fr)
                if case is None:
                    dropped[f"{domain}/{c}: {why}"] += 1
                else:
                    cases.append(case)
    counts = collections.Counter(f"{c['domain']}/{c['condition']}" for c in cases)
    recall_ok = collections.Counter(
        f"{c['domain']}/{c['condition']}" for c in cases if c["readers"][X.RECALL]["answers_differ"]
    )
    return cases, {"cases": dict(counts), "recall_answers_differ": dict(recall_ok), "dropped": dict(dropped),
                   "entities": {d: len({c["bridge"] for c in cases if c["domain"] == d}) for d in CONDITIONS}}  # fmt: skip


def eligible(cases: list[dict], comp: list[dict]) -> tuple[dict, dict[str, set]]:
    """Gate per condition and reader, and the eligible cases (scene keys, unique per condition) per condition and
    reader. The cases are keyed (`keyed`), as the competence rows are."""
    right = {(r["scene"], r["rendering"], r["reader"], r["variant"]): r for r in comp}
    gate, elig = {}, {}
    for key in sorted({f"{c['domain']}/{c['condition']}" for c in cases}):
        mine = [c for c in cases if f"{c['domain']}/{c['condition']}" == key]
        for w in X.READERS:
            acc = float(np.mean([right[(c["scene"], "chat", w, "org")]["read_right"] for c in mine]))
            ok = {c["scene"] for c in mine
                  if all(right[(c["scene"], "chat", w, v)]["right"] and right[(c["scene"], "chat", w, v)]["read_right"]
                         for v in ("org", "alt"))
                  and (w == X.LOOKUP or c["readers"][w]["answers_differ"])}  # fmt: skip
            gate[f"{key}/{w}"] = {"cases": len(mine), "org_accuracy": acc, "pass": acc >= X.GATE, "eligible": len(ok)}
            elig[f"{key}/{w}"] = ok if acc >= X.GATE else set()
    return gate, elig


def keyed(cases: list[dict]) -> list[dict]:
    """The cases with a scene key unique per condition (X0's code keys rows by scene)."""
    return [{**c, "scene": c["scene"] + "|" + c["condition"]} for c in cases]


def stage_run(name: str, why: str, probe_only: bool) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress

    pins.check_run_name(name)
    layer = X.PREDICTED[pins.TARGET]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "k": X.K_MAIN,
         "conditions": CONDITIONS, "picks": N_PICKS, "seed": SEED, "probe_only": probe_only,
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): __import__("bridge_jspace.data", fromlist=["sha256_of"]).sha256_of(p)
                    for p in (*sorted(DATA.glob("*_DL_*.json")), SPEC)},
         "gate": f"per condition and reader: >= {X.GATE} unedited org accuracy (decisive read)",
         "eligibility": "per reader: org and alt right (said and read); the recall also needs its answers to differ",
         "design": "jobs/c3/X4.md"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    cases, counts = build_cases(tok)
    cases = keyed(cases)
    print(json.dumps(counts, indent=1), flush=True)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in cases])
    states = []
    with torch.no_grad():
        for c in progress(cases, f"h_org at layer {layer} (case)"):
            ids = torch.tensor([c["readers"][X.LOOKUP]["ids"]["org"]], device="cuda")
            states.append(model.run(ids, record=(layer,))[1][layer][c["pos"]].float().cpu().numpy())
    np.savez_compressed(
        out / "states.npz", h=np.stack(states).astype(np.float16), scene=np.array([c["scene"] for c in cases])
    )
    if probe_only:
        return out
    ws = X.whitespace_mask(model)
    X.DIGIT_IDS.update(X.digit_ids(tok))
    comp = X.competence(model, cases, torch.tensor(X.digit_ids(tok), device="cuda"), ws)
    X.write_jsonl(out / "competence.jsonl", comp)
    gate, elig = eligible(cases, comp)
    (out / "gate.json").write_text(json.dumps({"counts": counts, "gate": gate}, indent=1) + "\n")
    print(json.dumps(gate, indent=1), flush=True)
    keep = {s for k, v in elig.items() for s in v}
    todo = [c for c in cases if c["scene"] in keep]
    X.DICTS, X.CURVE_DICTS, X.K_CURVE = ("jpp",), (), ()
    lens = JLens(model, "jpp")
    for s in range(0, len(todo), 500):
        X.run_rendering(model, lens, todo[s : s + 500], (layer,), layer, out, ws)
    X.write_jsonl(out / "eligible.jsonl", [{"key": k, "scenes": sorted(v)} for k, v in elig.items()])
    return out


def form_key(c: dict) -> str:
    return f"{c['domain']}/{c['condition']}"


def stage_probe_fit(name: str, n_boot: int = X.N_BOOT) -> Path:
    """Probe (b), the index of the bridge's locker statement, on the run's org states: within each form (one-hot ridge,
    cross-validated by bridge entity; baselines chance, majority, the asked pick's position) and trained on the
    verbatim scenes, tested on the translated / symbol scenes of the same domain (transfer)."""
    from scripts import x0_probe as P

    src = RESULTS / name
    cases = X.read_jsonl(src / "cases.jsonl")
    z = np.load(src / "states.npz")
    h = z["h"].astype(np.float64)
    assert [str(s) for s in z["scene"]] == [c["scene"] for c in cases], "states and cases disagree"
    items = [{"entity": c["bridge"], "locker_index": c["locker_index"], "pick_index": c["asked_pick"], "form": form_key(c)}
             for c in cases]  # fmt: skip
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = [f"# X4 probe: the bridge's locker statement (its first mention), {name}", "",
             f"Descriptive (jobs/c3/X4.md). Org states at the bridge word; one-hot ridge; bootstrap over bridge entities "
             f"({n_boot} resamples). UNVERIFIED.", "", "## Within each form (cross-validated by bridge entity)", "",
             "| form | n | entities | probe | majority | pick position only | chance | probe - best baseline |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob: dict = {"run": name, "within": {}, "transfer": {}}
    for form in sorted({it["form"] for it in items}):
        idx = [i for i, it in enumerate(items) if it["form"] == form]
        r = P.score(h[idx], [items[i] for i in idx], "locker sentence", n_boot)
        blob["within"][form] = r
        lines.append(f"| {form} | {r['n']} | {r['entities']} | {ci(r['probe'])} | {ci(r['majority'])} | "
                     f"{ci(r['structure'])} | {r['chance']:.2f} | {ci(r['probe_minus_best'])} ({r['best_baseline']}) |")  # fmt: skip
    lines += ["", "## Transfer: trained on the verbatim scenes, tested on the other form (same domain)", "",
              "| domain | test form | n | accuracy | chance |", "|---|---|---|---|---|"]  # fmt: skip
    for domain, (same, alias) in CONDITIONS.items():
        tr = [i for i, it in enumerate(items) if it["form"] == f"{domain}/{same}"]
        te = [i for i, it in enumerate(items) if it["form"] == f"{domain}/{alias}"]
        if not tr or not te:
            continue
        y = [items[i]["locker_index"] for i in tr]
        rel = P.select_penalty(h[tr], y, [items[i]["entity"] for i in tr])
        pred = P.ridge(h[tr], y, h[te], (rel,))[0]
        right = [int(p_ == items[i]["locker_index"]) for p_, i in zip(pred, te, strict=True)]
        r_ = X.resampled_rates({"right": right}, [items[i]["entity"] for i in te], n_boot)["right"]
        acc = [float(np.mean(right)), *X.interval(r_)]
        chance = 1 / len({items[i]["locker_index"] for i in te})
        blob["transfer"][f"{domain}/{alias}"] = {"n": len(te), "accuracy": acc, "chance": chance, "penalty": rel}
        lines.append(f"| {domain} | {alias} | {len(te)} | {ci(acc)} | {chance:.2f} |")
    out = src / f"probe-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    (out / "probe.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "probe.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def excess_resamples(rows: list[dict], scenes: set, keys: list[str], pick: np.ndarray) -> tuple[float, np.ndarray]:
    """A reader's lookup-style excess (Jdep - Rdep, J++ k = 25) on the given scenes, and its value on each bootstrap
    resample of the entity keys (pick: [n_boot, n_keys] indices into keys), so that two forms share the draws."""
    arms = {"whole": ("-", 0, "-", "whole"), "no_part": ("jpp", X.K_MAIN, "signed", "no_part"),
            "no_rand": ("jpp", X.K_MAIN, "signed", "no_rand")}  # fmt: skip
    got = {(r["scene"], (r["dict"], r["k"], r["omp"], r["arm"])): r["switched"] for r in rows if r["scene"] in scenes}
    ent = {r["scene"]: r["entity"] for r in rows if r["scene"] in scenes}
    index = {e: i for i, e in enumerate(keys)}
    e_idx = np.array([index[ent[s]] for s in sorted(scenes)])
    counts = np.bincount(e_idx, minlength=len(keys)).astype(float)
    n_r = counts[pick].sum(1)
    rate, point = {}, {}
    for a, key in arms.items():
        v = np.array([got[(s, key)] for s in sorted(scenes)], dtype=float)
        sums = np.bincount(e_idx, weights=v, minlength=len(keys))
        rate[a] = sums[pick].sum(1) / np.where(n_r > 0, n_r, np.nan)
        point[a] = float(v.mean())
    ex = lambda r: X.dependence(r["whole"], r["no_part"]) - X.dependence(r["whole"], r["no_rand"])  # noqa: E731
    return float(ex(point)), ex(rate)


def rule(d: list[float]) -> str:
    if d[0] >= HOLD:
        return "needs a verbatim match"
    if d[0] <= NOT_NEEDED:
        return "does not need a verbatim match"
    return "mixed"


def stage_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl")}
    gate = json.loads((src / "gate.json").read_text())["gate"]
    elig = {r["key"]: set(r["scenes"]) for r in X.read_jsonl(src / "eligible.jsonl")}
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = [f"# X4 verdict: {name} ({m['model']['target']}, layer {m['layer']})", "",
             "jobs/c3/X4.md section 2. J++ k = 25 against a random part of its share; bootstrap over bridge entities "
             f"({n_boot} resamples, seed {X.BOOT_SEED}), the same draws for both forms of a domain. UNVERIFIED.", "",
             "## Gate (unedited org accuracy, decisive read, >= 0.80 per form and reader)", "",
             "| form / reader | cases | accuracy | pass | eligible |", "|---|---|---|---|---|"]  # fmt: skip
    lines += [
        f"| {k} | {g['cases']} | {g['org_accuracy']:.2f} | {g['pass']} | {g['eligible']} |" for k, g in gate.items()
    ]
    lines += ["", "## Cells per form and reader (each reader on its own eligible items; the recall's rows are a stability "
              "check, X4.md)", "",
              "| form | reader | n | S_whole | Jdep | Rdep | excess | label |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob: dict = {"run": name, "cells": {}, "rules": {}}
    for key in sorted(elig):
        domain, cond, w = key.split("/")
        mine = [r for r in rows if r["scene"] in elig[key] and r["reader"] == w]
        if not mine:
            continue
        c = X.cells_of(mine, n_boot)[("chat", m["layer"], w, *X.MAIN)]
        blob["cells"][key] = c
        lines.append(f"| {domain}/{cond} | {'lookup' if w == X.LOOKUP else 'recall'} | {c['n']} | {X.fmt3(c['S_whole'])} | "
                     f"{X.fmt3(c['Jdep'])} | {X.fmt3(c['Rdep'])} | {X.fmt3(c['excess'])} | {c['label']} |")  # fmt: skip
    per_lines = [
        "| domain | entity | n verbatim | n alias | excess verbatim | excess alias | D |",
        "|---|---|---|---|---|---|---|",
    ]
    notes: list[str] = []
    lines += ["", "## The graded rules (lookup)", "",
              "| domain | difference | value | reading |", "|---|---|---|---|"]  # fmt: skip
    for domain, (same, alias) in CONDITIONS.items():
        a, b = elig.get(f"{domain}/{same}/{X.LOOKUP}", set()), elig.get(f"{domain}/{alias}/{X.LOOKUP}", set())
        if not a or not b:
            lines.append(f"| {domain} | {alias} - {same} | can't test (a form failed its gate or has no items) | - |")
            continue
        keys = sorted({cases[s]["bridge"] for s in a | b})
        pick = np.random.default_rng(X.BOOT_SEED).integers(0, len(keys), size=(n_boot, len(keys)))
        lookups = [r for r in rows if r["reader"] == X.LOOKUP]
        ea, ra = excess_resamples(lookups, a, keys, pick)
        eb, rb = excess_resamples(lookups, b, keys, pick)
        d = [eb - ea, *X.interval(rb - ra)]
        reading = (
            rule(d)
            if alias == "xlang"
            else ("passes" if d[0] >= HOLD else "fails: the method may not see a lookup that needs J++")
        )
        per = []
        for e in keys:
            ae, be = {s for s in a if cases[s]["bridge"] == e}, {s for s in b if cases[s]["bridge"] == e}
            if ae and be:
                one = np.zeros((1, len(keys)), dtype=int)
                per.append({"entity": e, "n_verbatim": len(ae), "n_alias": len(be),
                            "excess_verbatim": excess_resamples(lookups, ae, keys, one)[0],
                            "excess_alias": excess_resamples(lookups, be, keys, one)[0]})  # fmt: skip
                per[-1]["D"] = per[-1]["excess_alias"] - per[-1]["excess_verbatim"]
        scene_d = scene_bootstrap(lookups, a, b, n_boot)
        blob["rules"][domain] = {"difference": d, "alias": alias, "reading": reading, "per_entity": per,
                                 "entities_D_positive": sum(x["D"] > 0 for x in per if x["D"] == x["D"]),
                                 "scene_bootstrap_within_these_entities": [d[0], *X.interval(scene_d)]}  # fmt: skip
        lines.append(f"| {domain} | excess ({alias}) - excess ({same}) | {ci(d)} | {reading} |")
        per_lines += [f"| {domain} | {x['entity']} | {x['n_verbatim']} | {x['n_alias']} | {x['excess_verbatim']:.2f} | "
                      f"{x['excess_alias']:.2f} | {x['D']:.2f} |" for x in per]  # fmt: skip
        notes.append(
            f"- {domain}: D > 0 for {blob['rules'][domain]['entities_D_positive']} of {len(per)} entities; the "
            f"entity-bootstrap interval {ci(d)} is unreliable with {len(keys)} clusters (fewer than 10); a "
            f"bootstrap over scenes, within these entities only: {ci(blob['rules'][domain]['scene_bootstrap_within_these_entities'])}."
        )
    lines += ["", "## Every entity (the unit; X4.md)", "", *per_lines, "", *notes]
    # C only on items eligible for both readers (>= C_MIN), X4.md
    lines += ["", "## C = recall excess - lookup excess, on items eligible for both readers", "",
              "| form | n | C |", "|---|---|---|"]  # fmt: skip
    blob["contrast"] = {}
    for form in sorted({k.rsplit("/", 1)[0] for k in elig}):
        both = elig.get(f"{form}/{X.LOOKUP}", set()) & elig.get(f"{form}/{X.RECALL}", set())
        if len(both) < C_MIN:
            lines.append(
                f"| {form} | {len(both)} | not reported (fewer than {C_MIN} items eligible for both readers) |"
            )
            continue
        sw = {f"{w}/{a_}": [] for w in X.READERS for a_ in ("whole", "no_part", "no_rand")}
        got = {
            (r["scene"], r["reader"], (r["dict"], r["k"], r["omp"], r["arm"])): r["switched"]
            for r in rows
            if r["scene"] in both
        }
        arm = {"whole": ("-", 0, "-", "whole"), "no_part": ("jpp", X.K_MAIN, "signed", "no_part"),
               "no_rand": ("jpp", X.K_MAIN, "signed", "no_rand")}  # fmt: skip
        scenes = sorted(both)
        for w in X.READERS:
            for a_, key in arm.items():
                sw[f"{w}/{a_}"] = [got[(s, w, key)] for s in scenes]
        r_ = X.resampled_rates(sw, [cases[s]["bridge"] for s in scenes], n_boot)
        pt = {k: float(np.mean(v)) for k, v in sw.items()}
        c = [float(reader_excess(pt, X.RECALL) - reader_excess(pt, X.LOOKUP)),
             *X.interval(reader_excess(r_, X.RECALL) - reader_excess(r_, X.LOOKUP))]  # fmt: skip
        blob["contrast"][form] = {"n": len(both), "C": c}
        lines.append(f"| {form} | {len(both)} | {ci(c)} |")
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    (out / "verdict.json").write_text(json.dumps(blob, indent=1) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    figure(out, blob, m)
    return out


def reader_excess(src: dict, w: str):
    """Jdep - Rdep for reader w from rates keyed '<reader>/<arm>' (points or bootstrap arrays)."""
    return X.dependence(src[f"{w}/whole"], src[f"{w}/no_part"]) - X.dependence(src[f"{w}/whole"], src[f"{w}/no_rand"])


def scene_bootstrap(rows: list[dict], a: set, b: set, n_boot: int) -> np.ndarray:
    """D = excess(b) - excess(a) on scene resamples within each form (within these entities only; X4.md)."""
    arms = {"whole": ("-", 0, "-", "whole"), "no_part": ("jpp", X.K_MAIN, "signed", "no_part"),
            "no_rand": ("jpp", X.K_MAIN, "signed", "no_rand")}  # fmt: skip
    got = {(r["scene"], (r["dict"], r["k"], r["omp"], r["arm"])): r["switched"] for r in rows}
    rng = np.random.default_rng(X.BOOT_SEED)

    def draws(scenes: set) -> np.ndarray:
        sc = sorted(scenes)
        v = {k: np.array([got[(s, key)] for s in sc], dtype=float) for k, key in arms.items()}
        idx = rng.integers(0, len(sc), size=(n_boot, len(sc)))
        r = {k: x[idx].mean(1) for k, x in v.items()}
        return X.dependence(r["whole"], r["no_part"]) - X.dependence(r["whole"], r["no_rand"])

    return draws(b) - draws(a)


def figure(out: Path, blob: dict, m: dict) -> Path:
    """D per entity (dots) with the pooled D and its entity-bootstrap interval, per domain."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    doms = [d for d in CONDITIONS if d in blob["rules"]]
    if not doms:
        return out
    fig, axes = plt.subplots(1, len(doms), figsize=(5.5 * len(doms), 4.8), sharey=True, squeeze=False)
    for ax, d in zip(axes[0], doms, strict=True):
        r = blob["rules"][d]
        per = r["per_entity"]
        ax.axhspan(-1, NOT_NEEDED, color="#f1f1f1", lw=0, zorder=0)
        ax.axhline(HOLD, color="#bbbbbb", lw=0.8, ls=":")
        ax.axhline(0, color="black", lw=0.6)
        for i, x in enumerate(per):
            ax.plot(i, x["D"], "o", color="#6a3d9a", ms=7)
            ax.text(i, x["D"] + 0.03, x["entity"], ha="center", fontsize=8.5, rotation=45)
        v, lo, hi = r["difference"]
        ax.errorbar(len(per) + 0.8, v, yerr=[[v - lo], [hi - v]], fmt="s", color="#333333", capsize=4, ms=8)
        ax.set_xticks([*range(len(per)), len(per) + 0.8], [""] * len(per) + ["pooled\n(entity bootstrap,\nunreliable < 10)"],
                      fontsize=8.5)  # fmt: skip
        ax.set_title(f"{d}: excess ({r['alias']}) - excess (verbatim)", fontsize=11)
        ax.set_ylim(-0.6, 1.0)
        ax.grid(axis="y", color="#eeeeee")
    axes[0][0].set_ylabel("D (lookup extra loss, alias minus verbatim)")
    fig.suptitle(f"X4, {m['model']['target']} layer {m['layer']}: D per bridge entity (UNVERIFIED)", fontsize=11)
    fig.tight_layout()
    path = out / "x4_D_per_entity.png"
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "probe", "run", "probe_fit", "verdict"])
    ap.add_argument("--name")
    ap.add_argument("--why", default="")
    a = ap.parse_args()
    if a.stage == "plan":
        from scripts import statement_positions as SP

        _, counts = build_cases(SP.load_tokenizer())
        print(json.dumps(counts, indent=1))
    elif a.stage == "probe_fit":
        stage_probe_fit(a.name)
    elif a.stage == "verdict":
        stage_verdict(a.name)
    else:
        stage_run(a.name, a.why, probe_only=a.stage == "probe")
        stage_probe_fit(a.name)
        if a.stage == "run":
            stage_verdict(a.name)


if __name__ == "__main__":
    main()
