"""x47_twodefs (batch 47, test 47.12; jobs/c3/batch47.yaml amendment 4, rule fixed in advance; Q47.12 in
predictions/2026-10-28_dan.md): two definitions of the lens part on the same scenes.

The main test's scenes (two people swap their picks; each model's main-test X0 run at the layer fixed in advance, its
eligible scenes rebuilt as x47_cumulative.select does for its "main" design), the change Δ = h_S - h_O at the bridge
token at L, X0's arms (whole / without the part / without a random part of the part's share) with the part defined
two ways at the same token and layer, both as a projection out of Δ:
  omp25        (i) ours: the 25 signed-OMP atoms of Δ over the J++ lens's letter-token unit vectors (x0_necessity.fit;
               the existing no_part arm)
  top10        (ii) Zach's: the projection of Δ onto the span of the 10 J++ directions with the highest lens logits
               (bridge_jspace.ablate.top_span_removal on Δ, his code path: LensDictionary over the same lens file and
               letter tokens, never a protected atom, the protected set being the reader's clean top-10 tokens at the
               read position as ablate_v2 sets it; so (ii) is per reader, (i) is one part for both)
  top10_state  descriptive: the same 10 directions chosen at S's bridge-token state h_S (what the lens reads at that
               token in the changed prompt), Δ projected onto their span
Each part against a random part of its own share of ||Δ||^2 (X0's random subspace, seed 888 + L). Both readers read the
same prompt O with the edit; switch = the top token is S's answer's first token (X0's chat read).

Reading (as computed; the job specs' decision_rule carries it): per model and definition, X0's cells at L (switch rate
per arm; Jdep = 1 - S_no_part / S_whole; Rdep the same with the random part; extra loss = Jdep - Rdep; a cell is valid
if S_whole >= 0.30 with >= 30 switches), and the gap = the recall's extra loss minus the lookup's (the main test's
"contrast", x0_figures.contrast: the same cluster-bootstrap draws for both readers, 10,000, seed 0). Rule (verbatim):
"Definitions agree" if the gap under (ii) is within 0.15 of (i) on both models. Q47.12 per model: yes if
|gap(top10) - gap(omp25)| <= 0.15 (point estimates, EPS 1e-9); no otherwise; "can't tell" if a cell of either
definition is invalid. Reported beside: each part's share of ||Δ||^2 (per item and median), the atoms (ii) picks and
how many of them are among (i)'s 25, how often the protection displaced a top-10 atom, (ii') the same numbers, the
rerun whole arm against the source run's stored one.

SEALED: the run writes per-item files only; verdict and view refuse until predictions/2026-10-28_dan.md holds Dan's
committed Q47.12 answer at HEAD.

BJ_TARGET=qwen3.5-9b uv run python scripts/x47_twodefs.py plan                             # CPU, the target's tokenizer
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_twodefs.py run --name qwen35_9b_x47_twodefs # GPU (sealed)
uv run python scripts/x47_twodefs.py verdict      # CPU, after Dan's Q47.12
uv run python scripts/x47_twodefs.py view         # CPU, after Dan's Q47.12: 10 random items, seed 0
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.run_switches import switches
from scripts import x0_necessity as X
from scripts import x45b_binding as B
from scripts import x47_atoms as A
from scripts import x47_cumulative as C

EXP = "x47_twodefs"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = pins.REPO_ROOT / "jobs" / "c3" / "batch47.yaml"
PREDICTIONS = A.PREDICTIONS
QUESTION = "Q47.12"
RENDERING, DESIGN = "chat", "main"
SOURCES = B.MAIN_RUN  # target -> the main-test X0 run (x47_cumulative's "main" design)
RUNS = {"qwen3.5-9b": "qwen35_9b_x47_twodefs", "muse-glimmer-30b": "muse30_x47_twodefs"}
K_OMP, K_TOP, K_PROTECT = X.K_MAIN, 10, 10
# definition -> X0's (dict, k, fit) key of its rows
DEFS = {
    "omp25": ("jpp", K_OMP, "signed"),
    "top10": ("paper10", K_TOP, "top"),
    "top10_state": ("paper10", K_TOP, "top_hS"),
}
DEF_TEXT = {"omp25": "(i) ours: the 25 signed-OMP atoms of Δ (J++ letter-token atoms)",
            "top10": "(ii) Zach's: the span of the 10 J++ directions with the highest lens logits of Δ, never a protected atom (ablate.top_span_removal)",
            "top10_state": "descriptive: the 10 directions chosen at S's bridge-token state h_S, Δ projected onto their span"}  # fmt: skip
DECISIVE = ("omp25", "top10")
AGREE = 0.15
EPS = 1e-9  # a value exactly at a bar counts as at the bar
RULE = '"Definitions agree" if the gap under (ii) is within 0.15 of (i) on both models'
ARMS = ("none", "whole", *(f"{d}:{a}" for d in DEFS for a in ("no_part", "no_rand")))
READER_NAME = C.READER_NAME


# ---- the parts (GPU in the run; CPU in tests) ----------------------------------------------------------------------


def omp_dictionary(model, lens, layer: int, letters):
    """Our dictionary: the J++ lens's unit vectors of the letter tokens at the layer (x0_necessity's "jpp")."""
    return lens.vectors(layer, letters)


def zach_dictionary(model, lens, layer: int, letters):
    """His dictionary: ablate.LensDictionary over the same lens file and letter tokens, built as ablate_v2 builds it
    (Wg = W_U[letters] * the final norm's gain, J_l)."""
    from bridge_jspace.ablate import LensDictionary

    wg = model.hf.lm_head.weight[letters].float() * model.norm_gain()
    return LensDictionary(wg, lens.J(layer))


def span_projection(atoms, x):
    """x [m, d] projected onto the span of its own unit atoms [m, k, d] (QR, as top_span_removal projects)."""
    import torch

    q, _ = torch.linalg.qr(atoms.transpose(1, 2).double())
    return (q @ (q.transpose(1, 2) @ x.double().unsqueeze(2))).squeeze(2).float()


def top_parts(dic, x, h_s, protected, k: int = K_TOP) -> dict[str, Any]:
    """(ii) and (ii') for one item and reader: x = Δ [1, d], h_s = S's bridge-token state [1, d], protected = the
    dictionary rows never chosen (his protected set; a [p] long tensor or None). Returns the parts [1, d], the atoms
    (dictionary rows) each chose, and the atoms (ii) would have chosen without the protection."""
    import torch

    from bridge_jspace.ablate import top_span_removal

    groups = [(torch.tensor([0], device=x.device), protected)] if protected is not None and protected.numel() else None
    part, top = top_span_removal(dic, x, k, protected=groups, return_chosen=True)
    _, free = top_span_removal(dic, x, k, protected=None, return_chosen=True)
    _, top_s = top_span_removal(dic, h_s, k, protected=groups, return_chosen=True)
    part_s = span_projection(dic.atoms(top_s), x)
    return {"top10": part, "top10_state": part_s, "atoms_top10": top[0].tolist(), "atoms_top10_state": top_s[0].tolist(),
            "atoms_unprotected": free[0].tolist()}  # fmt: skip


def protected_rows(clean_logits, row_of, k: int = K_PROTECT):
    """His protected set for one reader's prompt: the dictionary rows of the clean read's top-k tokens (ablate_v2:
    `row_of[t][row_of[t] >= 0]` of `clean.topk(10)`); tokens outside the dictionary (digits) fall away."""
    t = clean_logits.topk(k).indices
    rows = row_of[t]
    return rows[rows >= 0]


def stage_plan() -> dict:
    """Tokenizer only: the target's main-test items as x47_cumulative.select rebuilds them, their counts."""
    from scripts import x45m

    tok = x45m.tokenizer()
    layer = X.PREDICTED[pins.TARGET]
    items, counts = C.select(tok, DESIGN, SOURCES[pins.TARGET], layer)
    counts.update({"target": pins.TARGET, "reads_per_reader": len(ARMS), "arms": list(ARMS)})
    folder = RESULTS / f"plan-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{pins.RUN_PREFIX.rstrip('_')}"
    folder.mkdir(parents=True)
    lines = [f"# 47.12 plan on {pins.TARGET} (L{layer}): 5 of the main test's {len(items)} items (seed {X.EXAMPLES_SEED}), "
             "the lookup's O prompt as the model reads it; ⟦bridge:…⟧ the bridge token, ⟦other:…⟧ the other changed pick "
             "token (S changes it too; no arm patches it). Counts in plan.json.", ""]  # fmt: skip
    for i in C.example_indices(len(items), 5):
        it = items[i]
        lines += [f"## {it['scene']} ({it['group']}): bridge {it['entity']} -> {it['cf_bridge']}, token {it['pos']}", "",
                  "```", C.item_marked(it, X.LOOKUP), "```", ""]  # fmt: skip
    (folder / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    (folder / "prompts.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(counts, indent=2, ensure_ascii=False))
    print("wrote", folder)
    return counts


def stage_run(name: str, why: str) -> Path:
    import torch

    from bridge_jspace import chat
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts import x0_parts as XP
    from scripts import x6_routes as R
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    assert chat.FORMAT == "chat", "47.12 renders X0's chat prompts: run with BJ_FORMAT unset"
    target = pins.TARGET
    assert target in RUNS, f"47.12 runs on {sorted(RUNS)}, not {target}"
    layer, run_main = X.PREDICTED[target], SOURCES[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    src = X.RESULTS / run_main
    m = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "test": "47.12",
         "spec": "jobs/c3/batch47.yaml (47.12, amendment 4)", "question": f"{QUESTION} ({PREDICTIONS})",
         "inputs": {str(p.relative_to(pins.REPO_ROOT)): X.sha256_of(p)
                    for p in (SPEC, *(src / f for f in ("manifest.json", "cases.jsonl", "outcomes.jsonl")))},
         "source": run_main, "layer": layer, "definitions": DEF_TEXT, "keys": {d: list(k) for d, k in DEFS.items()},
         "k": {"omp": K_OMP, "top": K_TOP, "protected": K_PROTECT}, "arms": list(ARMS),
         "protection": "per reader: the dictionary rows of the clean read's top-10 tokens at the read position (ablate_v2), "
                       "never chosen by (ii) and (ii'); digits are not letter tokens, so they fall away",
         "random_part": f"X0's random subspace at each part's share of ||Δ||^2, seed {X.SUBSPACE_SEED} + layer",
         "items_rule": "the main-test run's scenes at L (chat), the items its unedited run made eligible, rebuilt and "
                       "aligned as x47_cumulative.select (design main); eligibility is never recounted",
         "read": "X0's chat read: the prompt with a digit's space token appended; switch = top token is S's answer",
         "gap": "the recall's extra loss minus the lookup's (x0_figures.contrast), per definition", "rule": RULE,
         "bars": {"agree": AGREE}, "seeds": {"bootstrap": X.BOOT_SEED, "examples": X.EXAMPLES_SEED,
                                             "random_subspace": f"{X.SUBSPACE_SEED} + layer"}, "n_boot": X.N_BOOT,
         "sealed": f"no verdict in the run; results closed until {PREDICTIONS} holds Dan's {QUESTION} answer"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    print("wrote", out / "manifest.json", flush=True)

    R.warm_cusolver()
    model = load_model()
    tok = model.tokenizer
    items, counts = C.select(tok, DESIGN, run_main, layer)
    (out / "plan.json").write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n")
    X.write_jsonl(out / "cases.jsonl", items)
    print(json.dumps(counts, ensure_ascii=False), flush=True)
    assert items, "no items"
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device=model.device)
    lens = JLens(model, "jpp")
    letters = model.letter_token_ids()
    jdic = omp_dictionary(model, lens, layer, letters)
    zd = zach_dictionary(model, lens, layer, letters)
    row_of = torch.full((len(model.decoded),), -1, dtype=torch.long, device=model.device)
    row_of[letters.to(model.device)] = torch.arange(letters.numel(), device=model.device)
    basis = None
    rows, shares = [], []
    with torch.no_grad():
        for it in progress(items, f"47.12 at L{layer} (item)"):
            ids = it["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device=model.device), record=(layer,))[1][layer][it["pos"]].float()
                 for v in ("org", "alt")}  # fmt: skip
            x = (h["alt"] - h["org"])[None].to(jdic.device)
            if basis is None:
                basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to(x.device)
            total = (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            part_i = X.fit(jdic, x, K_OMP, "signed").float()
            atoms_i = XP.omp_atoms(jdic, x, K_OMP)[0].tolist()
            for w, rd in it["readers"].items():
                clean, _ = X.read_logits(model, rd["ids"]["org"], [{}], RENDERING, it["space"], ws)
                prot = protected_rows(clean[0], row_of)
                tp = top_parts(zd, x, h["alt"][None].to(x.device), prot)
                parts = {"omp25": part_i, "top10": tp["top10"], "top10_state": tp["top10_state"]}
                arms: dict[str, Any] = {"whole": x}
                rec = {"scene": it["scene"], "reader": w, "norm": round(float(x.norm()), 4), "atoms_omp25": atoms_i,
                       "atoms_top10": tp["atoms_top10"], "atoms_top10_state": tp["atoms_top10_state"],
                       "protected_rows": prot.tolist(), "top10_displaced_by_protection": len(set(tp["atoms_unprotected"]) - set(tp["atoms_top10"])),
                       "overlap_top10_in_omp25": len(set(tp["atoms_top10"]) & set(atoms_i)),
                       "overlap_top10_state_in_omp25": len(set(tp["atoms_top10_state"]) & set(atoms_i)),
                       "overlap_top10_state_in_top10": len(set(tp["atoms_top10_state"]) & set(tp["atoms_top10"]))}  # fmt: skip
                for d, part in parts.items():
                    share = part.norm(dim=-1) ** 2 / total
                    rand = SP.random_subspace_part(x, share, basis)
                    arms[f"{d}:no_part"], arms[f"{d}:no_rand"] = x - part, x - rand
                    rec[f"share_{d}"] = round(float(share[0]), 5)
                    rec[f"rand_share_{d}"] = round(float(rand.norm() ** 2 / total[0]), 5)
                shares.append(rec)
                names = [a for a in ARMS if a != "none"]
                edits = [{}] + [{layer: AddRows(arms[a], [it["pos"]])} for a in names]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, RENDERING, it["space"], ws)
                base = {"scene": it["scene"], "domain": it["domain"], "entity": it["entity"], "rendering": RENDERING,
                        "layer": layer, "reader": w, "upstream": it["upstream"], "group": it["group"]}  # fmt: skip
                for a, lg in zip(ARMS, logits, strict=True):
                    d, _, arm = a.partition(":")
                    key = DEFS[d] if arm else ("-", 0, "-")
                    rows.append({**base, "dict": key[0], "k": key[1], "omp": key[2], "arm": arm or a, "definition": d if arm else None,
                                 "top_text": tok.decode([int(lg.argmax())]), **X.read_row(lg, rd, digits)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    X.write_jsonl(out / "shares.jsonl", shares)
    print(f"wrote {out}: {len(rows)} reads of {len(items)} items (sealed: no verdict)", flush=True)
    return out


# ---- verdict and view (CPU, sealed) ---------------------------------------------------------------------------------


def unsealed() -> str:
    answer = A.dan_answer(QUESTION)
    assert answer, f"sealed: {PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


def gap_of(rows: list[dict], layer: int, key: tuple, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    """One definition's cells (X0's, both readers) and the gap = recall extra loss - lookup extra loss with its
    paired cluster-bootstrap interval (the same entity draws for both readers, as x0_figures.contrast)."""
    cells = X.cells_of([r for r in rows if r["rendering"] == RENDERING and r["layer"] == layer
                        and (r["arm"] == "whole" or (r["dict"], r["k"], r["omp"]) == key)], n_boot)  # fmt: skip
    boot, point = {}, {}
    for w in X.READERS:
        mine = [r for r in rows if r["rendering"] == RENDERING and r["layer"] == layer and r["reader"] == w]
        whole = {r["scene"]: r["switched"] for r in mine if r["arm"] == "whole"}
        arm = {(r["arm"], r["scene"]): r["switched"] for r in mine
               if (r["dict"], r["k"], r["omp"]) == key and r["arm"] in ("no_part", "no_rand")}  # fmt: skip
        ent = {r["scene"]: r["entity"] for r in mine}
        scenes = sorted(whole)
        sw = {"whole": [whole[s] for s in scenes], **{a: [arm[(a, s)] for s in scenes] for a in ("no_part", "no_rand")}}
        rr = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot)
        s = {k: sum(v) / len(scenes) for k, v in sw.items()}
        boot[w] = X.dependence(rr["whole"], rr["no_part"]) - X.dependence(rr["whole"], rr["no_rand"])
        point[w] = float(X.dependence(s["whole"], s["no_part"]) - X.dependence(s["whole"], s["no_rand"]))
    lk, rc = cells[(RENDERING, layer, X.LOOKUP, *key)], cells[(RENDERING, layer, X.RECALL, *key)]
    return {"lookup": lk, "recall": rc, "valid": bool(lk["valid"] and rc["valid"]),
            "gap": [point[X.RECALL] - point[X.LOOKUP], *X.interval(boot[X.RECALL] - boot[X.LOOKUP])]}  # fmt: skip


def model_rule(defs: dict[str, dict]) -> dict[str, Any]:
    """One model: the gap under (ii) against (i), both valid: agree iff |difference| <= AGREE (point estimates)."""
    i, ii = defs[DECISIVE[0]], defs[DECISIVE[1]]
    if not (i["valid"] and ii["valid"]):
        return {"answer": "can't tell", "agree": False, "why": "an invalid cell (X0: S_whole < 0.30 or < 30 switches)"}
    diff = ii["gap"][0] - i["gap"][0]
    return {"answer": "yes" if abs(diff) <= AGREE + EPS else "no", "agree": abs(diff) <= AGREE + EPS,
            "difference": diff, "why": f"gap (ii) {ii['gap'][0]:.3f} − gap (i) {i['gap'][0]:.3f} = {diff:+.3f}"}  # fmt: skip


def share_summary(shares: list[dict]) -> dict[str, Any]:
    out: dict[str, Any] = {"n": len(shares)}
    for d in DEFS:
        v = [s[f"share_{d}"] for s in shares if f"share_{d}" in s]
        out[f"median_share_{d}"] = float(np.median(v)) if v else None
    for k in (
        "overlap_top10_in_omp25",
        "overlap_top10_state_in_omp25",
        "overlap_top10_state_in_top10",
        "top10_displaced_by_protection",
    ):
        v = [s[k] for s in shares if k in s]
        out[f"mean_{k}"] = float(np.mean(v)) if v else None
    v = [s["top10_displaced_by_protection"] for s in shares if "top10_displaced_by_protection" in s]
    out["items_with_protection_displacing"] = int(sum(x > 0 for x in v))
    return out


def model_result(run: str, n_boot: int = X.N_BOOT) -> dict[str, Any]:
    src = RESULTS / run
    if not (src / "manifest.json").exists() or not (src / "outcomes.jsonl").exists():
        target = {r: t for t, r in RUNS.items()}.get(run)
        assert target, f"no 47.12 run {run!r} here, and it is not one of the job specs' runs {sorted(RUNS.values())}"
        return {
            "run": run,
            "target": target,
            "status": "pending",
            "answer": "pending",
            "why": "the run has no manifest or outcomes here",
        }
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    cases = X.read_jsonl(src / "cases.jsonl")
    defs = {d: gap_of(rows, m["layer"], tuple(key), n_boot) for d, key in DEFS.items()}
    stored = {c["scene"]: c["stored"]["whole"] for c in cases}
    agree = {}
    for w in X.READERS:
        pairs = [(r["switched"], stored[r["scene"]].get(w)) for r in rows if r["arm"] == "whole" and r["reader"] == w]
        agree[READER_NAME[w]] = {"n": len(pairs), "agree": sum(a == b for a, b in pairs), "rerun": sum(a for a, _ in pairs),
                                 "stored": sum(b or 0 for _, b in pairs)}  # fmt: skip
    return {"run": run, "target": m["model"]["target"], "layer": m["layer"], "source": m["source"], "status": "tested",
            "definitions": defs, **model_rule(defs), "shares": share_summary(X.read_jsonl(src / "shares.jsonl")),
            "whole_vs_stored": agree, "plan": json.loads((src / "plan.json").read_text())}  # fmt: skip


def fmt(v) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def verdict_lines(models: list[dict], answer: str, n_boot: int) -> list[str]:
    tested = [m for m in models if m["status"] == "tested"]
    batch = "agree" if tested and all(m["agree"] for m in tested) and len(tested) == len(models) else (
        "do not agree" if any(m.get("answer") == "no" for m in tested) else "pending / can't tell")  # fmt: skip
    lines = ["# 47.12: two definitions of the lens part on the same scenes", "",
             f"Batch 47, test 47.12 (jobs/c3/batch47.yaml, amendment 4; {QUESTION}, Dan: {answer}). The main test's scenes, Δ "
             "at the bridge token at L; X0's arms with the part defined as (i) our 25 OMP atoms of Δ and (ii) Zach's top-10 "
             "lens directions (his code path on Δ, same lens file), each against a random part of its share; gap = the "
             f"recall's extra loss − the lookup's; cluster bootstrap over bridge items ({n_boot}, seed {X.BOOT_SEED}). "
             "UNVERIFIED.", "", f"Rule (fixed in advance): {RULE}.", "",
             f"**The definitions {batch}** (" + "; ".join(f"{m['target']}: {m.get('answer')}" for m in models) + ").", "",
             "| model | n | definition | lookup S_whole | lookup extra loss | recall extra loss | gap | valid | median share of ‖Δ‖² |",
             "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | | pending ({m['why']}) | | | | | | |")
            continue
        for d, c in m["definitions"].items():
            sh = m["shares"].get(f"median_share_{d}")
            lines.append(f"| {m['target']} | {c['lookup']['n']} | {d} | {c['lookup']['S_whole'][0]:.2f} | {fmt(c['lookup']['excess'])} | "
                         f"{fmt(c['recall']['excess'])} | {fmt(c['gap'])} | {'yes' if c['valid'] else 'no'} | "
                         f"{'-' if sh is None else f'{sh:.3f}'} |")  # fmt: skip
        lines.append(f"| {m['target']} | | (ii) − (i) | | | | {m['why']} | | |")
    lines += ["", "Definitions: " + "; ".join(f"{d} = {t}" for d, t in DEF_TEXT.items()) + ".", "",
              "Switch rates per arm (S_whole, S without the part, S without its random part), per reader and definition:", "",
              "| model | reader | definition | S_whole | S_no_part | S_no_rand | Jdep | Rdep |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for d, c in m["definitions"].items():
            for w in ("lookup", "recall"):
                cell = c[w]
                lines.append(f"| {m['target']} | {w} | {d} | {cell['S_whole'][0]:.2f} | {cell['S_no_part'][0]:.2f} | "
                             f"{cell['S_no_rand'][0]:.2f} | {fmt(cell['Jdep'])} | {fmt(cell['Rdep'])} |")  # fmt: skip
    lines += ["", "The atoms (per item and reader; means): how many of (ii)'s 10 are among (i)'s 25, (ii')'s among (i)'s and "
              "among (ii)'s, how often the protection (the clean read's top-10 at the read position) displaced a top-10 atom; "
              "the rerun whole arm against the source run's stored one:", ""]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        s = m["shares"]
        lines.append(f"- {m['target']} ({m['run']}, from {m['source']}, L{m['layer']}, {m['plan']['items']} items of "
                     f"{m['plan']['items_at_L']} at L): (ii) in (i) {s['mean_overlap_top10_in_omp25']:.2f} of 10; (ii') in (i) "
                     f"{s['mean_overlap_top10_state_in_omp25']:.2f}; (ii') in (ii) {s['mean_overlap_top10_state_in_top10']:.2f}; "
                     f"protection displaced an atom on {s['items_with_protection_displacing']} of {s['n']} reads (mean "
                     f"{s['mean_top10_displaced_by_protection']:.2f}); whole vs stored: " + "; ".join(
                         f"{w} {a['agree']} of {a['n']} agree (rerun {a['rerun']}, stored {a['stored']})" for w, a in m["whole_vs_stored"].items()))  # fmt: skip
    return lines


def stage_verdict(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    answer = unsealed()
    models = [model_result(r, n_boot) for r in runs]
    targets = [m["target"] for m in models]
    assert len(set(targets)) == len(targets), f"one run per model: {targets}"
    models += [{"run": f"({RUNS[t]})", "target": t, "status": "pending", "answer": "pending", "why": "no run given"}
               for t in RUNS if t not in targets]  # fmt: skip
    out = RESULTS / f"x47_12-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, answer, n_boot)
    (out / "x47_12.json").write_text(json.dumps({"runs": runs, "dan": answer, "models": models}, indent=1) + "\n")
    (out / "x47_12.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def view_lines(run: str, k: int = X.K_EXAMPLES, seed: int = X.EXAMPLES_SEED) -> list[str]:
    """k random items of the run (seed 0): each reader's O prompt as the model reads it with the bridge token marked
    (x47_cumulative's marks), each arm's answer and the parts' shares."""
    src = RESULTS / run
    m = json.loads((src / "manifest.json").read_text())
    cases = X.read_jsonl(src / "cases.jsonl")
    reads = {(r["scene"], r["reader"], r["definition"], r["arm"]): r for r in X.read_jsonl(src / "outcomes.jsonl")}
    shares = {(s["scene"], s["reader"]): s for s in X.read_jsonl(src / "shares.jsonl")}
    lines = [f"## {run} ({m['model']['target']}, L{m['layer']}; from {m['source']}): {min(k, len(cases))} random items of "
             f"{len(cases)} (seed {seed})", ""]  # fmt: skip
    for i in C.example_indices(len(cases), k, seed):
        it = cases[i]
        lines += [
            f"### {it['scene']} ({it['domain']}, {it['group']}): bridge {it['entity']} → {it['cf_bridge']}, token {it['pos']}",
            "",
        ]
        for w, rd in it["readers"].items():
            s = shares.get((it["scene"], w), {})
            lines += [f"**{READER_NAME[w]}** ({rd['id']}): O's answer {rd['answer']}, S's answer {rd['cf_answer']}; shares of ‖Δ‖²: "
                      + ", ".join(f"{d} {s.get(f'share_{d}', '-')}" for d in DEFS), "", "```", C.item_marked(it, w), "```", "",
                      "| arm | definition | top token | role | switched |", "|---|---|---|---|---|"]  # fmt: skip
            for a in ARMS:
                d, _, arm = a.partition(":")
                r = reads[(it["scene"], w, d if arm else None, arm or a)]
                lines.append(f"| {arm or a} | {d if arm else ''} | {r['top_text']!r} | {r['role']} | {r['switched']} |")
            lines.append("")
    return lines


def stage_view(runs: list[str]) -> Path:
    unsealed()
    out = RESULTS / f"view-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = ["# 47.12 verify-pack view: prompts exactly as the model reads them (the read appends the digit's space token); "
             "⟦bridge:…⟧ the bridge token, where the change (or the arm's part of it) is added at L; ⟦other:…⟧ the other "
             "changed pick token (S changes it too; no arm patches it). UNVERIFIED.", ""]  # fmt: skip
    for run in runs:
        if (RESULTS / run / "outcomes.jsonl").exists():
            lines += view_lines(run)
    (out / "view.md").write_text("\n".join(lines) + "\n")
    print(out / "view.md")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "verdict", "view"])
    ap.add_argument("--name", help="run: the run name (results/x47_twodefs/<name>/)")
    ap.add_argument("--why", default="batch 47, test 47.12 (jobs/c3/batch47.yaml amendment 4; Q47.12, sealed)")
    ap.add_argument("--runs", nargs="+", default=list(RUNS.values()), help="verdict / view: the 47.12 runs")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        assert a.name, "run needs --name"
        stage_run(a.name, a.why)
    elif a.stage == "verdict":
        stage_verdict(a.runs, a.n_boot)
    else:
        stage_view(a.runs)


if __name__ == "__main__":
    main()
