"""x5_natural (Dan, 25 Oct ~00:20; X3's natural passages): does the recall-lookup gap hold on Zach's natural passages?

Data: data/tasks_v2/jsuite_v2_1_test_chat (copied from zach/v8-breadth-1021; PROVENANCE.txt), module facts, start P,
358 scenes (test halves A / B). One passage for both readers: the PP item's passage. Lookup = the PP question (the
answer is the passage's value for the bridge); recall = the PM question on that same passage (the answer comes from
memory; the passage's value for the bridge is a made-up lure from the same answer vocabulary).
Alt (one change): in the asked person's binding sentence (the one sentence that names the bridge and no answer value),
the bridge -> another entity of the scene with its own fact sentence in the passage, whose passage value (the alt's
lookup answer) and memory value (the alt's recall answer, from the set's `real` field) both differ from the org's;
the bridge is one token at one position in org and alt; the first alt candidate in the scene's entity order.
Read (cand2): the top token among the first tokens (after 'Answer:', with the leading space, either case) of the
relation's answer vocabulary; switched iff it is the alt answer's; org and alt first tokens distinct. The recall's
lure: the read lands on the passage value of the edited bridge (reported separately).
Gate: per reader, the unedited org read right >= 0.80 (--gate: a lowered, descriptive gate after the data, Dan 25 Oct
~13:20); eligible: both readers say and read org and alt right (X0).
At the model's X0 layer (27B L32, 9B L12), Δ = h_alt - h_org at the bridge word; arms whole / without the J++ part
(k = 25, signed) / without a random part of its share; both readers on the identical patch.
Rule (graded, from the brief): the recall-lookup gap >= 0.30 with lower CI >= 0.15 holds; <= 0.10 fails; otherwise
mixed. By relation and by half: descriptive. Cluster bootstrap over bridge entities (10,000 resamples, seed 0).

uv run python scripts/x5_natural.py plan                         # tokenizer only
uv run python scripts/x5_natural.py run --name x5_natural_27b    # GPU, then the verdict
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X

EXP = "x5_natural"
RESULTS = pins.RESULTS_DIR / EXP
SET = "jsuite_v2_1_test_chat"
ITEMS = pins.DATA_DIR / "tasks_v2" / SET / "items.jsonl"
GEN_TOKENS = 8
HOLD_GAP, HOLD_LO, FAIL_GAP = 0.30, 0.15, 0.10
NOTE = "Fixed in advance (Dan, 25 Oct ~00:20; spec jobs/c3/x5_natural.yaml; prediction: batch 31, Q31.6)."


def sentences(context: str) -> list[str]:
    """The passage's sentences (split at line breaks and sentence ends)."""
    return [s for s in re.split(r"\n|(?<=[.!?])\s+", context) if s.strip()]


def values_in(sent: str, vocab: list[str]) -> list[str]:
    low = sent.lower()
    return [v for v in vocab if re.search(rf"\b{re.escape(v.lower())}\b", low)]


def names(sent: str, entity: str) -> bool:
    return re.search(rf"\b{re.escape(entity)}\b", sent) is not None


def load() -> tuple[list[tuple[dict, dict]], dict]:
    """(PP, PM) pairs of module facts, start P, in scene order; and real[relation][entity] from every item of the set."""
    items = [json.loads(line) for line in ITEMS.open()]
    real: dict[str, dict[str, str]] = collections.defaultdict(dict)
    for it in items:
        if it.get("bridge") and it.get("real"):
            real[it["relation"]][it["bridge"]] = it["real"]
    by = collections.defaultdict(dict)
    for it in items:
        if it["module"] == "facts" and it["start"] == "P" and it["word"] in ("PP", "PM"):
            by[it["scene"]][it["word"]] = it
    pairs = [(by[s]["PP"], by[s]["PM"]) for s in sorted(by) if set(by[s]) == {"PP", "PM"}]
    return pairs, real


def first_tokens(tok, value: str) -> set[int]:
    """The value's first token after 'Answer:' (leading space), as written and lower case."""
    from scripts import suite_v1 as S

    return {S.ids(tok, " " + value)[0], S.ids(tok, " " + value.lower())[0]}


def scene_case(tok, pp: dict, pm: dict, real: dict) -> tuple[dict | None, str]:
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    ctx, vocab, bridge, rel = pp["context"], pp["answer_vocab"], pp["bridge"], pp["relation"]
    if pm["answer_vocab"] != vocab:
        return None, "the readers' answer vocabularies differ"
    sents = sentences(ctx)
    bind = [s for s in sents if names(s, bridge) and not values_in(s, vocab)]
    if len(bind) != 1 or ctx.count(bind[0]) != 1:
        return None, "no unique binding sentence"
    bind_s = bind[0]
    org = {"lookup": pp["answer"], "recall": pm["answer"], "lure": pp["answer"]}
    tok_sets = {v: first_tokens(tok, v) for v in vocab}
    owner = {}
    for v, ts in tok_sets.items():
        for t in ts:
            if owner.setdefault(t, v) != v:
                return None, "two answer values share a first token"
    for alt in [e for e in pp["entities"] if e != bridge]:
        facts = [s for s in sents if names(s, alt) and len(values_in(s, vocab)) == 1]
        if len(facts) != 1 or alt not in real[rel]:
            continue
        a = {"lookup": values_in(facts[0], vocab)[0], "recall": real[rel][alt]}
        a["lure"] = a["lookup"]
        if a["lookup"] == org["lookup"] or a["recall"] == org["recall"] or a["recall"] not in vocab:
            continue
        i = bind_s.rindex(bridge)
        alt_ctx = ctx.replace(bind_s, bind_s[:i] + alt + bind_s[i + len(bridge) :])
        readers, pos = {}, None
        for w, it, key in ((X.LOOKUP, pp, "lookup"), (X.RECALL, pm, "recall")):
            ids, at = {}, {}
            for v, c, b in (("org", ctx, bridge), ("alt", alt_ctx, alt)):
                text = T.render(tok, {**it, "context": c})
                enc = raw_encoding(tok, text, offsets=True)
                sent = bind_s[:i] + b + bind_s[i + len(bridge) :] if v == "alt" else bind_s
                w0 = text.index(c) + c.index(sent) + i
                ids[v], at[v] = list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(b))
            if len(at["org"]) != 1 or at["alt"] != at["org"]:
                break
            diff = S.changed(ids["org"], ids["alt"])
            if not diff or at["org"][0] not in diff or (pos is not None and at["org"][0] != pos):
                break
            pos = at["org"][0]
            readers[w] = {"id": it["id"], "question": it["question"], "answer": org[key], "cf_answer": a[key],
                          "lure": org["lure"], "cf_lure": a["lure"], "ids": ids,
                          "upstream": min(diff) < pos}  # fmt: skip
        if len(readers) != 2 or any(readers[X.LOOKUP]["ids"][v][: pos + 1] != readers[X.RECALL]["ids"][v][: pos + 1]
                                    for v in ("org", "alt")):  # fmt: skip
            continue
        return {"scene": pp["scene"], "rendering": "chat", "domain": rel, "relation": rel, "half": pp["half"],
                "genre": pp["genre"], "bridge": bridge, "cf_bridge": alt, "context": ctx, "cf_context": alt_ctx,
                "pos": pos, "upstream": readers[X.LOOKUP]["upstream"], "space": [], "vocab": vocab,
                "readers": readers}, ""  # fmt: skip
    return None, "no alt entity fits (own fact sentence; both answers differ; one token at one position)"


def build_cases(tok) -> tuple[list[dict], dict]:
    pairs, real = load()
    cases, dropped = [], collections.Counter()
    for pp, pm in pairs:
        c, why = scene_case(tok, pp, pm, real)
        if c is None:
            dropped[why] += 1
        else:
            cases.append(c)
    return cases, {"scenes": len(pairs), "cases": len(cases), "dropped": dict(dropped),
                   "by_relation": dict(collections.Counter(c["relation"] for c in cases))}  # fmt: skip


def said(text: str, vocab: list[str]) -> str | None:
    """The first answer value in the greedy reply's first non-empty line (case-insensitive)."""
    from scripts import suite_v1 as S

    line = S.first_line(text).lower()
    hits = [(m.start(), v) for v in vocab if (m := re.search(rf"\b{re.escape(v.lower())}\b", line))]
    return min(hits)[1] if hits else None


def cand_read(lg, case: dict, tok_sets: dict) -> str:
    """The answer value whose first token (either case) has the highest logit."""
    best = {v: float(lg[sorted(ts)].max()) for v, ts in tok_sets.items()}
    return max(best, key=best.get)


def row_of(lg, rd: dict, tok_sets: dict) -> dict:
    top = cand_read(lg, None, tok_sets)
    return {"switched": int(top == rd["cf_answer"]), "org_read": int(top == rd["answer"]),
            "lure_alt": int(top == rd["cf_lure"]), "lure_org": int(top == rd["lure"]), "top": top}  # fmt: skip


def stage_plan() -> None:
    from scripts import statement_positions as SP

    cases, counts = build_cases(SP.load_tokenizer())
    print(json.dumps(counts, indent=1))
    for c in cases[:3]:
        print(
            c["scene"],
            c["bridge"],
            "->",
            c["cf_bridge"],
            {w: (r["answer"], r["cf_answer"]) for w, r in c["readers"].items()},
        )


def stage_run(name: str, gate_min: float = X.GATE, pointer: bool = False, alf_from: str | None = None) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "note": NOTE,
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "set": SET,
         "inputs": {str(ITEMS.relative_to(pins.REPO_ROOT)): X.sha256_of(ITEMS)}, "layer": layer, "k": X.K_MAIN,
         "gate": gate_min, "gate_fixed_in_advance": X.GATE, "read": "cand2: the top first token (either case) among the relation's answer vocabulary",
         "rule": f"gap >= {HOLD_GAP} with lower CI >= {HOLD_LO} holds; <= {FAIL_GAP} fails; otherwise mixed",
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    lens = JLens(model, "jpp")
    tok = model.tokenizer
    cases, counts = build_cases(tok)
    ws = X.whitespace_mask(model)
    sets = {c["scene"]: {v: first_tokens(tok, v) for v in c["vocab"]} for c in cases}
    comp = []
    with torch.no_grad():
        for c in progress(cases, "competence (case)"):
            for w, rd in c["readers"].items():
                ids = torch.tensor([rd["ids"]["org"], rd["ids"]["alt"]], device="cuda")
                texts = model.generate_batch(ids, GEN_TOKENS, [{}, {}])
                for i, (v, gold) in enumerate((("org", rd["answer"]), ("alt", rd["cf_answer"]))):
                    lg, _ = X.read_logits(model, rd["ids"][v], [{}], "chat", [], ws)
                    comp.append({"scene": c["scene"], "reader": w, "variant": v, "greedy": texts[i],
                                 "said": said(texts[i], c["vocab"]), "right": said(texts[i], c["vocab"]) == gold,
                                 "read": cand_read(lg[0], c, sets[c["scene"]]),
                                 "read_right": cand_read(lg[0], c, sets[c["scene"]]) == gold})  # fmt: skip
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in cases])
    right = {(r["scene"], r["reader"], r["variant"]): r for r in comp}
    acc = {w: float(np.mean([right[(c["scene"], w, "org")]["read_right"] for c in cases])) for w in X.READERS}
    ok = [c for c in cases if all(right[(c["scene"], w, v)]["right"] and right[(c["scene"], w, v)]["read_right"]
                                  for w in X.READERS for v in ("org", "alt"))]  # fmt: skip
    gate = {
        "counts": counts,
        "org_read_accuracy": acc,
        "pass": all(a >= gate_min for a in acc.values()),
        "eligible": len(ok),
    }
    (out / "gate.json").write_text(json.dumps(gate, indent=2) + "\n")
    print(json.dumps(gate, indent=2), flush=True)
    if not gate["pass"] or not ok:
        raise SystemExit(f"gate failed or no eligible items: {gate}")
    cases = ok
    letters = model.letter_token_ids()
    jdic = lens.vectors(layer, letters)
    with torch.no_grad():
        deltas = []
        for c in progress(cases, "Δ at the bridge's word (case)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]].to("cuda")
                 for v in ("org", "alt")}  # fmt: skip
            deltas.append((h["alt"] - h["org"]).float())
        x = torch.stack(deltas)
        part = X.fit(jdic, x, X.K_MAIN, "signed")
        share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to("cuda")
        arms = {X.WHOLE: x, ("jpp", X.K_MAIN, "signed", "no_part"): x - part,
                ("jpp", X.K_MAIN, "signed", "no_rand"): x - SP.random_subspace_part(x, share, basis)}  # fmt: skip
        if pointer:  # T (Dan 26 Oct ~11:55): the pointer directions fit on the simple scenes, not refit
            from scripts import x0_massmean as MM
            from scripts.x6_routes import STATES

            pbasis = (np.load(pins.RESULTS_DIR / alf_from / "pcf.npz")["P"] if alf_from  # P_cf_nat (batch 43)
                      else MM.subspaces(STATES[target])[0]["Alf"])  # fmt: skip
            alf = torch.tensor(pbasis, dtype=torch.float32, device="cuda")
            ptr = (x @ alf) @ alf.T
            psh = ptr.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            r = alf.shape[1]
            arms[("alf", r, "signed", "no_part")] = x - ptr
            arms[("alf", r, "signed", "no_rand")] = x - SP.random_subspace_part(x, psh, basis)
            m["pointer_from"] = alf_from or STATES[target]
        keys = list(arms)
        rows = []
        for i, c in enumerate(progress(cases, f"reads at layer {layer} (case)")):
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[key][i : i + 1], [c["pos"]])} for key in keys]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", [], ws)
                base = {"scene": c["scene"], "domain": c["relation"], "entity": c["bridge"], "rendering": "chat",
                        "layer": layer, "reader": w, "upstream": c["upstream"], "relation": c["relation"],
                        "half": c["half"], "share": round(float(share[i]), 5)}  # fmt: skip
                for key, lg in zip([("-", 0, "-", "none"), *keys], logits, strict=True):
                    d_, k_, fit_, arm = key
                    rows.append(
                        {**base, "dict": d_, "k": k_, "omp": fit_, "arm": arm, **row_of(lg, rd, sets[c["scene"]])}
                    )
    X.write_jsonl(out / "outcomes.jsonl", rows)
    m["items"] = len(cases)
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", out, flush=True)
    return out


def gap(rows: list[dict], n_boot: int) -> dict:
    """The recall-lookup gap (recall excess - lookup excess) with a paired cluster bootstrap over bridge entities."""
    sw, ent = {}, {}
    scenes = sorted({r["scene"] for r in rows})
    got = {(r["scene"], r["reader"], r["arm"]): r["switched"] for r in rows}
    for r in rows:
        ent[r["scene"]] = r["entity"]
    for w in X.READERS:
        for a in ("whole", "no_part", "no_rand"):
            sw[f"{w}|{a}"] = [got[(s, w, a)] for s in scenes]
    rr = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot)
    s = {k: float(np.mean(v)) for k, v in sw.items()}

    def excess(src, w):
        return X.dependence(src[f"{w}|whole"], src[f"{w}|no_part"]) - X.dependence(
            src[f"{w}|whole"], src[f"{w}|no_rand"]
        )

    point = {w: float(excess(s, w)) for w in X.READERS}
    boot = {w: excess(rr, w) for w in X.READERS}
    g = boot[X.RECALL] - boot[X.LOOKUP]
    return {"n": len(scenes), "entities": len(set(ent.values())),
            "excess": {w: [point[w], *X.interval(boot[w])] for w in X.READERS},
            "gap": [point[X.RECALL] - point[X.LOOKUP], *X.interval(g)]}  # fmt: skip


def label(g: list[float]) -> str:
    return "holds" if g[0] >= HOLD_GAP and g[1] >= HOLD_LO else "fails" if g[0] <= FAIL_GAP else "mixed"


def stage_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = [r for r in X.read_jsonl(src / "outcomes.jsonl")
            if r["arm"] in ("whole", "no_part", "no_rand") and r["dict"] in ("jpp", "-")]  # fmt: skip
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    main = gap(rows, n_boot)
    lines = [f"# Natural passages: {name}", "", f"{NOTE} Model {m['model']['target']}, layer {m['layer']}, {main['n']} items, "
             f"{main['entities']} bridge entities. Bootstrap over bridge entities ({n_boot} resamples). UNVERIFIED.", "",
             f"## Rule: {label(main['gap']).upper()} (gap {ci(main['gap'])})", "", f"Rule: {m['rule']}.", "",
             f"Lookup excess {ci(main['excess'][X.LOOKUP])}; recall excess {ci(main['excess'][X.RECALL])}.", "",
             "## By relation and by half (descriptive)", "", "| subset | n | lookup excess | recall excess | gap |",
             "|---|---|---|---|---|"]  # fmt: skip
    subsets = {}
    for key in ("relation", "half"):
        for v in sorted({r[key] for r in rows}):
            sub = [r for r in rows if r[key] == v]
            if len({r["entity"] for r in sub}) < 2:
                continue
            subsets[f"{key}={v}"] = g = gap(sub, n_boot)
            lines.append(
                f"| {key} = {v} | {g['n']} | {ci(g['excess'][X.LOOKUP])} | {ci(g['excess'][X.RECALL])} | {ci(g['gap'])} |"
            )
    lure = {a: float(np.mean([r["lure_alt"] for r in rows if r["reader"] == X.RECALL and r["arm"] == a]))
            for a in ("whole", "no_part", "no_rand")}  # fmt: skip
    lines += ["", "## The recall's lure (separate outcome)", "", "Share of recall reads on the passage's value for the edited "
              "bridge: " + ", ".join(f"{a} {v:.2f}" for a, v in lure.items()) + "."]  # fmt: skip
    (out / "verdict.json").write_text(json.dumps({"run": name, "manifest": m, "main": main, "label": label(main["gap"]),
                                                  "subsets": subsets, "lure": lure}, indent=1) + "\n")  # fmt: skip
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict"])
    ap.add_argument("--name")
    ap.add_argument("--gate", type=float, default=X.GATE, help="run: a lowered, descriptive read-accuracy gate")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    ap.add_argument("--pointer", action="store_true", help="run: also the pointer directions as a part (T)")
    ap.add_argument("--alf-from", default=None, help="run, with --pointer: the basis from results/<path>/pcf.npz")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
        return
    if a.stage == "run":
        stage_run(a.name, a.gate, a.pointer, a.alf_from)
    stage_verdict(a.name, a.n_boot)


if __name__ == "__main__":
    main()
