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
         "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "k": X.K_MAIN,
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "probe", "run"])
    ap.add_argument("--name")
    ap.add_argument("--why", default="")
    a = ap.parse_args()
    if a.stage == "plan":
        from scripts import statement_positions as SP

        _, counts = build_cases(SP.load_tokenizer())
        print(json.dumps(counts, indent=1))
    else:
        stage_run(a.name, a.why, probe_only=a.stage == "probe")


if __name__ == "__main__":
    main()
