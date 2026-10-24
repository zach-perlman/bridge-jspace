"""x0_massmean (Dan, 24 Oct ~20:05; descriptive, added after data; the last causal test this week): does the lookup read
the address or the value at the bridge's word through their mass-mean directions?

Ridge directions fit on standardised features weight low-variance dimensions (x0_amnesic's P held 1-2% of ||Δ||²);
mass-mean directions are known to be more causal than regression-probe directions (Marks & Tegmark 2023). On the fresh
scenes' org states at the bridge's word (x0_probe_power's d1_topics_v4 states, locker-before):
  A  the address: the class means of the locker sentence's index minus the grand mean, raw activation space,
     orthonormalised (rank = classes - 1);
  V  the value: the same for the locker number (the lookup's answer digit).
Arms on the single-change Δ (x0_single_*: only the asked pick changes) at the model's X0 layer, both readers, X0's
top-token read, the items whose org and alt locker sentences both come before the asked pick:
  whole; no_A (Δ - AΔ), no_V, no_AV (Δ minus its projection on span(A, V)), each against X0's rand_sub at its own share;
  keep_AV (the projection alone) against the random part alone at the same share.
Per reader: S per arm, dependence 1 - S_no / S_whole against the random one (excess, paired), S_keep / S_whole against
S_rand / S_whole; each subspace's share of ||Δ||²; 95% CIs from a cluster bootstrap over bridge entities (10,000
resamples, seed 0).
Pre-stated reading (Dan): the lookup loses flips under A (or V) while the recall does not -> "the lookup uses the address
(or the value)"; no arm changes the lookup -> "the lookup's channel is not a low-rank linear readout of the address or
the value; what it is stays open".

uv run python scripts/x0_massmean.py run --name x0_massmean_27b --single x0_single_27b_r2 --states x0_probe_v4_27b
uv run python scripts/x0_massmean.py verdict --name x0_massmean_27b
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_amnesic as AM
from scripts import x0_necessity as X
from scripts import x0_probe as P
from scripts import x0_strata as ST

EXP = "x0_massmean"
RESULTS = pins.RESULTS_DIR / EXP
REMOVE = ("A", "V", "AV")
ARMS = ("whole", *(f"no_{s}" for s in REMOVE), *(f"no_{s}_rand" for s in REMOVE), "keep_AV", "keep_rand")
NOTE = "Descriptive, added after data (Dan, 24 Oct ~20:05); not part of X0's rule."


def mass_mean(x: np.ndarray, labels: list) -> np.ndarray:
    """An orthonormal basis [d, classes - 1] of the class means minus the grand mean (raw space)."""
    mu = x.mean(0)
    means = np.stack(
        [x[[i for i, v in enumerate(labels) if v == c]].mean(0) - mu for c in sorted(set(labels), key=str)]
    )
    u, s, _ = np.linalg.svd(means.T, full_matrices=False)
    return u[:, : int((s > s.max() * 1e-8).sum())]


def subspaces(states_run: str) -> tuple[dict[str, np.ndarray], dict]:
    """A, V and span(A, V) from a probe run's locker-before org states."""
    src = P.RESULTS / states_run
    items = X.read_jsonl(src / "items.jsonl")
    keep = [i for i, it in enumerate(items) if it["order"] == "before"]
    h = np.load(src / "states.npz")["h"].astype(np.float64)[keep]
    a = mass_mean(h, [items[i]["locker_index"] for i in keep])
    v = mass_mean(h, [items[i]["answer"] for i in keep])
    u, s, _ = np.linalg.svd(np.concatenate([a, v], 1), full_matrices=False)
    av = u[:, : int((s > s.max() * 1e-8).sum())]
    info = {"states_run": states_run, "n": len(keep), "rank": {"A": a.shape[1], "V": v.shape[1], "AV": av.shape[1]}}
    return {"A": a, "V": v, "AV": av}, info


def stage_run(name: str, single: str, states_run: str) -> Path:
    import torch

    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import statement_positions as SP
    from scripts.exp04_brew_parts import AddRows

    pins.check_run_name(name)
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    sm = json.loads((X.RESULTS / single / "manifest.json").read_text())
    assert sm["alt"] == "single", f"{single} is not a single-change run"
    layer = sm["predicted"]
    basis_np, info = subspaces(states_run)
    X.ALT = "single"
    model = load_model()
    tok = model.tokenizer
    cases, _ = X.build_cases(tok, sm["set"])
    by_scene = {c["scene"]: c for c in cases if c["rendering"] == "chat"}
    scenes = sorted(
        {r["scene"] for r in X.read_jsonl(X.RESULTS / single / "outcomes.jsonl") if r["rendering"] == "chat"}
    )
    feats = {s: ST.features(by_scene[s]) for s in scenes}
    scenes = [
        s
        for s in scenes
        if feats[s]["org locker vs asked pick"] == "before" and feats[s]["alt locker vs asked pick"] == "before"
    ]
    cases = [by_scene[s] for s in scenes]
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "note": NOTE,
         "single": single, "single_code": sm["code"], "set": sm["set"], "layer": layer, "items": len(scenes),
         "subspaces": info, "arms": list(ARMS), "model": pins.model_pin(), "code": git_state(),
         "items_rule": "single-change items whose org and alt locker sentences both come before the asked pick",
         "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)", "bootstrap": X.BOOT_SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print(json.dumps(info), len(scenes), "items", flush=True)
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(tok), device="cuda")
    with torch.no_grad():
        deltas = []
        for c in progress(cases, "Δ at the bridge's word (case)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {
                v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]]
                for v in ("org", "alt")
            }
            deltas.append((h["alt"] - h["org"]).float())
        x = torch.stack(deltas)
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to("cuda")
        arms, shares = {"whole": x}, {}
        for s in REMOVE:
            q = torch.tensor(basis_np[s], dtype=torch.float32, device="cuda")
            part = (x @ q) @ q.T
            share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            rand = SP.random_subspace_part(x, share, basis)
            arms[f"no_{s}"], arms[f"no_{s}_rand"] = x - part, x - rand
            shares[s] = share.cpu().tolist()
            if s == "AV":
                arms["keep_AV"], arms["keep_rand"] = part, rand
        rows = []
        for i, c in enumerate(progress(cases, f"reads at layer {layer} (case)")):
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[a][i : i + 1], [c["pos"]])} for a in ARMS]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                for a, lg in zip(("none", *ARMS), logits, strict=True):
                    rows.append({"scene": c["scene"], "entity": c["bridge"], "reader": w, "arm": a,
                                 **{f"share_{s}": round(shares[s][i], 5) for s in REMOVE}, **X.read_row(lg, rd, digits)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    print("wrote", out, flush=True)
    return out


def stage_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    sub = m["subspaces"]
    lines = [f"# Mass-mean address (A) and value (V) subspaces: remove or keep only ({name})", "",
             f"{NOTE} Model {m['model']['target']}, layer {m['layer']}, {m['items']} single-change items of {m['single']} "
             f"(both locker sentences before the pick); A rank {sub['rank']['A']}, V rank {sub['rank']['V']}, span(A, V) "
             f"rank {sub['rank']['AV']}, from {sub['states_run']} (locker-before, n = {sub['n']}). Bootstrap over bridge "
             f"entities ({n_boot} resamples). UNVERIFIED.", "",
             "| reader | S_whole | arm | median share of ‖Δ‖² | S_arm | S_rand | dependence | random dependence | excess |",
             "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob = []
    for w in X.READERS:
        mine = [r for r in rows if r["reader"] == w]
        scenes = sorted({r["scene"] for r in mine})
        got = {(r["scene"], r["arm"]): r["switched"] for r in mine}
        ent = {r["scene"]: r["entity"] for r in mine}
        sw = {a: [got[(s, a)] for s in scenes] for a in ARMS}
        r_ = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot)
        s = {a: float(np.mean(sw[a])) for a in ARMS}
        res = {"reader": w, "n": len(scenes), "switched_whole": int(sum(sw["whole"])), "S": s}
        for sp in REMOVE:
            share = float(np.median([r[f"share_{sp}"] for r in mine if r["arm"] == "whole"]))
            dep, rdep = AM.with_ci(X.dependence, s, r_, f"no_{sp}"), AM.with_ci(X.dependence, s, r_, f"no_{sp}_rand")
            ex = AM.paired(X.dependence, s, r_, f"no_{sp}", f"no_{sp}_rand")
            res[sp] = {"share": share, "dep": dep, "rand_dep": rdep, "excess": ex}
            lines.append(f"| {'lookup' if w == X.LOOKUP else 'recall'} | {s['whole']:.2f} ({res['switched_whole']}) | "
                         f"remove {sp} | {share:.4f} | {s[f'no_{sp}']:.2f} | {s[f'no_{sp}_rand']:.2f} | {ci(dep)} | "
                         f"{ci(rdep)} | {ci(ex)} |")  # fmt: skip
        keep, krand = AM.with_ci(AM.of_whole, s, r_, "keep_AV"), AM.with_ci(AM.of_whole, s, r_, "keep_rand")
        diff = AM.paired(AM.of_whole, s, r_, "keep_AV", "keep_rand")
        res["keep"] = {"keep_AV": keep, "keep_rand": krand, "difference": diff}
        lines.append(f"| {'lookup' if w == X.LOOKUP else 'recall'} | {s['whole']:.2f} ({res['switched_whole']}) | keep only "
                     f"(A + V) | {res['AV']['share']:.4f} | {s['keep_AV']:.2f} | {s['keep_rand']:.2f} | kept / whole "
                     f"{ci(keep)} | random kept / whole {ci(krand)} | {ci(diff)} |")  # fmt: skip
        blob.append(res)
    lines += ["", "Pre-stated reading (Dan): the lookup loses flips under A (or V) while the recall does not -> 'the lookup "
              "uses the address (or the value)'; no arm changes the lookup -> 'the lookup's channel is not a low-rank "
              "linear readout of the address or the value; what it is stays open'."]  # fmt: skip
    (out / "verdict.json").write_text(json.dumps({"run": name, "manifest": m, "rows": blob}, indent=1) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["run", "verdict"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--single", default="x0_single_27b_r2")
    ap.add_argument("--states", default="x0_probe_v4_27b")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "run":
        stage_run(a.name, a.single, a.states)
    stage_verdict(a.name, a.n_boot)


if __name__ == "__main__":
    main()
