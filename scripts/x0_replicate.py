"""x0_replicate (Dan, 25 Oct morning item 4; fixed in advance): does the 9B's double dissociation replicate on fresh
scenes? Removing the J++ part costs the recall and not the lookup; removing the layout-free pointer directions (Alf)
costs the lookup and not the recall.

Items: d1_topics_v5 (a fresh seed of d1_topics_v3's generator settings; no scene shared with v3 or v4), the edit that
changes only the asked pick (X0's single-change alt), chat rendering, scenes whose org and alt locker sentences both come
before the asked pick (the items x0_massmean's Alf result came from), eligible as in X0 (both readers say and read the org
and alt answers right; X0's gate at 0.80 on these cases), the first 200 in scene order. At the model's X0 layer (9B L12,
decisive; 27B L32 alongside, descriptive), Δ = h_alt - h_org at the bridge word, three parts, each removed against X0's
rand_sub part of its own share, both readers on the identical patch, X0's top-token read:
  jpp     X0's J++ part (signed OMP over the letter atoms, k = 25);
  alf     the projection on Alf, fit on the old fresh scenes' states (x0_probe_v4; x0_massmean.subspaces), not refit;
  pca_eq  the layer's top-2,000 PCA directions at the item's J++ share (x0_parts.equal_share; x0_parts.pca_dictionary).
Rule (Dan, 25 Oct; decisive on the 9B): holds iff
  J++:  recall excess >= 0.20 with lower CI > 0, and lookup excess <= 0.10;
  Alf:  lookup excess >= 0.20 with lower CI > 0, and recall excess <= 0.10 or at most half the lookup's;
point estimates elsewhere; CIs from X0's cluster bootstrap over bridge entities (10,000 resamples, seed 0). PCA at J++'s
share is reported beside them (descriptive). In the same run (Dan, 25 Oct ~00:20), two keep-only arms, both readers:
the word part alone (x0_parts' w) and the J++ part orthogonal to the word alone (jwo), each against the random part of
its share alone.

uv run python scripts/x0_replicate.py run --name qwen35_9b_x0_replicate        # GPU (BJ_TARGET=qwen3.5-9b), then verdict
uv run python scripts/x0_replicate.py verdict --name qwen35_9b_x0_replicate    # CPU
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_massmean as MM
from scripts import x0_necessity as X
from scripts import x0_parts as XP
from scripts import x0_strata as ST

EXP = "x0_replicate"
RESULTS = pins.RESULTS_DIR / EXP
SET = "d1_topics_v5"
STATES = {"qwen3.5-9b": "qwen35_9b_x0_probe_v4", "qwen3.6-27b": "x0_probe_v4_27b"}
PARTS = (("jpp", X.K_MAIN, "signed"), ("alf", 0, "proj"), ("pca_eq", 0, "eq"))
KEEP = (("w", 0, "lsq"), ("jwo", X.K_MAIN, "signed"))  # pasted alone (keep-only arms)
DECISIVE = "qwen3.5-9b"
RULE = ("holds iff J++: recall excess >= 0.20 with lower CI > 0 and lookup excess <= 0.10; and Alf: lookup excess >= 0.20 "
        "with lower CI > 0 and recall excess <= 0.10 or at most half the lookup's (point estimates where no CI is named)")  # fmt: skip
NOTE = "Fixed in advance (Dan, 25 Oct morning item 4; spec jobs/c3/x0_replicate.yaml; prediction: batch 31)."


def both_before(c: dict) -> bool:
    f = ST.features(c)
    return f["org locker vs asked pick"] == "before" and f["alt locker vs asked pick"] == "before"


def stage_run(name: str) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    layer, states_run = X.PREDICTED[target], STATES[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    items = pins.DATA_DIR / "tasks_v2" / SET / "items.jsonl"
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "note": NOTE,
         "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(), "set": SET,
         "inputs": {str(items.relative_to(pins.REPO_ROOT)): X.sha256_of(items)}, "layer": layer,
         "decisive": target == DECISIVE, "alt": "single", "items_rule": "chat; org and alt locker sentences both before "
         "the asked pick; eligible as in X0; the first N in scene order", "n": {"items": X.N_ITEMS, "min": X.N_MIN},
         "gate": X.GATE, "parts": [list(p) for p in PARTS], "keep": [list(p) for p in KEEP], "alf_from": states_run, "rule": RULE,
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED,
                   "pca_held_out": XP.HELD_SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    X.ALT = "single"
    model = load_model()
    lens = JLens(model, "jpp")
    tok = model.tokenizer
    cases, counts = X.build_cases(tok, SET)
    cases = [c for c in cases if c["rendering"] == "chat" and both_before(c)]
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device="cuda")
    comp = X.competence(model, cases, digits, ws)
    gate, eligible = X.gate_and_eligible(cases, comp)
    X.write_jsonl(out / "competence.jsonl", comp)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "space"} for c in cases])
    (out / "gate.json").write_text(
        json.dumps({"counts": counts, "both_before": len(cases), "gate": gate}, indent=2) + "\n"
    )
    print(json.dumps(gate["chat"], indent=2), flush=True)
    cases = eligible["chat"]
    if not cases:
        raise SystemExit(f"gate failed or too few eligible items: {gate['chat']}")

    alf = torch.tensor(MM.subspaces(states_run)[0]["Alf"], dtype=torch.float32, device="cuda")
    pca, pca_info = XP.pca_dictionary(model, layer)
    letters = model.letter_token_ids()
    jdic = lens.vectors(layer, letters)
    with torch.no_grad():
        h_org, deltas = [], []
        for c in progress(cases, "Δ at the bridge's word (case)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]].to("cuda")
                 for v in ("org", "alt")}  # fmt: skip
            h_org.append(h["org"].float())
            deltas.append((h["alt"] - h["org"]).float())
        x = torch.stack(deltas)
        parts = {"jpp": X.fit(jdic, x, X.K_MAIN, "signed"), "alf": (x @ alf) @ alf.T}
        jshare = parts["jpp"].norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
        parts["pca_eq"], k_eq = XP.equal_share(pca, x, jshare)
        words, _ = XP.word_parts(lens, tok, layer, letters, jdic, cases, x, {"jwo"})
        parts.update(words)
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to("cuda")
        arms, shares = {X.WHOLE: x}, []
        for d, k, fit in PARTS:
            share = parts[d].norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            arms[(d, k, fit, "no_part")] = x - parts[d]
            arms[(d, k, fit, "no_rand")] = x - SP.random_subspace_part(x, share, basis)
            shares += [{"scene": c["scene"], "dict": d, "share": round(float(share[i]), 5),
                        **({"k_eq": int(k_eq[i])} if d == "pca_eq" else {})} for i, c in enumerate(cases)]  # fmt: skip
        for d, k, fit in KEEP:
            share = parts[d].norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            arms[(d, k, fit, "keep_part")] = parts[d]
            arms[(d, k, fit, "keep_rand")] = SP.random_subspace_part(x, share, basis)
            shares += [
                {"scene": c["scene"], "dict": d, "share": round(float(share[i]), 5)} for i, c in enumerate(cases)
            ]
        keys = list(arms)
        rows = []
        for i, c in enumerate(progress(cases, f"reads at layer {layer} (case)")):
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[key][i : i + 1], [c["pos"]])} for key in keys]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                base = {"scene": c["scene"], "domain": c["domain"], "entity": c["bridge"], "rendering": "chat",
                        "layer": layer, "reader": w, "upstream": c["upstream"]}  # fmt: skip
                for key, lg in zip([("-", 0, "-", "none"), *keys], logits, strict=True):
                    d_, k_, fit_, arm = key
                    rows.append({**base, "dict": d_, "k": k_, "omp": fit_, "arm": arm, **X.read_row(lg, rd, digits)})
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "shares.jsonl", shares)
    f16 = lambda t: t.cpu().numpy().astype(np.float16)  # noqa: E731
    np.savez_compressed(out / "states.npz", scene=np.array([c["scene"] for c in cases]), h_org=f16(torch.stack(h_org)),
                        delta=f16(x), **{f"part_{d}": f16(parts[d]) for d, _, _ in (*PARTS, *KEEP)})  # fmt: skip
    m["pca"] = pca_info
    m["items"] = len(cases)
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print("wrote", out, flush=True)
    return out


def rule(cells: dict) -> dict:
    """The rule's clauses on cells[(part, reader)] = [excess, lo, hi]."""
    jl, jr = cells[("jpp", X.LOOKUP)], cells[("jpp", X.RECALL)]
    al, ar = cells[("alf", X.LOOKUP)], cells[("alf", X.RECALL)]
    jpp = jr[0] >= 0.20 and jr[1] > 0 and jl[0] <= 0.10
    ptr = al[0] >= 0.20 and al[1] > 0 and (ar[0] <= 0.10 or ar[0] <= al[0] / 2)
    return {"jpp_clause": jpp, "pointer_clause": ptr, "holds": jpp and ptr}


def stage_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    shares = X.read_jsonl(src / "shares.jsonl")
    cells = X.cells_of(rows, n_boot)
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    ex = {(k[3], k[2]): c["excess"] for k, c in cells.items()}
    r = rule(ex)
    med = {d: statistics.median(s["share"] for s in shares if s["dict"] == d) for d, _, _ in (*PARTS, *KEEP)}
    label = {"jpp": "J++ (k = 25)", "alf": "pointer directions (Alf, not refit)", "pca_eq": "PCA at J++'s share"}
    lines = [f"# Replication of the 9B's double dissociation: {name}", "",
             f"{NOTE} Model {m['model']['target']} ({'decisive' if m['decisive'] else 'descriptive'}), layer {m['layer']}, "
             f"{m.get('items')} items of {m['set']} (single change, both locker sentences before the pick). Bootstrap over "
             f"bridge entities ({n_boot} resamples). UNVERIFIED.", "",
             "| part | reader | median share of ‖Δ‖² | S_whole | S_no | S_noRand | Jdep | Rdep | excess | label |",
             "|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob = []
    for d, _, _ in PARTS:
        for w in X.READERS:
            key = next(k for k in cells if k[2] == w and k[3] == d)
            c = cells[key]
            blob.append({"part": d, "reader": w, "median_share": med[d], **c})
            lines.append(f"| {label[d]} | {'lookup' if w == X.LOOKUP else 'recall'} | {med[d]:.3f} | {c['S_whole'][0]:.2f} | "
                         f"{c['S_no_part'][0]:.2f} | {c['S_no_rand'][0]:.2f} | {X.fmt3(c['Jdep'])} | {X.fmt3(c['Rdep'])} | "
                         f"{X.fmt3(c['excess'])} | {c['label']} |")  # fmt: skip
    word = "HOLDS" if r["holds"] else "DOES NOT HOLD"
    lines += ["", f"## Rule ({'decisive' if m['decisive'] else 'descriptive'}): {word}", "", f"Rule: {RULE}.",
              f"J++ clause: {'met' if r['jpp_clause'] else 'not met'}; pointer clause: "
              f"{'met' if r['pointer_clause'] else 'not met'}."]  # fmt: skip
    kept = XP.keep_cells(rows, n_boot)
    lines += ["", "## Pasted alone (descriptive): switches as a share of the whole change's, against the random part alone", "",
              "| part | reader | n | kept / whole | random kept / whole | difference |", "|---|---|---|---|---|---|"]  # fmt: skip
    lines += [f"| {'the word part' if k['part'] == 'w' else 'J++ orthogonal to the word'} | "
              f"{'lookup' if k['reader'] == X.LOOKUP else 'recall'} | {k['n']} | {X.fmt3(k['kept'])} | {X.fmt3(k['rand_kept'])} | "
              f"{X.fmt3(k['difference'])} |" for k in kept]  # fmt: skip
    (out / "verdict.json").write_text(
        json.dumps({"run": name, "manifest": m, "rows": blob, "rule": r, "kept": kept}, indent=1) + "\n"
    )
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["run", "verdict"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "run":
        stage_run(a.name)
    stage_verdict(a.name, a.n_boot)


if __name__ == "__main__":
    main()
