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

--mode layout_free (Dan, 24 Oct ~21:50): Alf, the address rebuilt after subtracting from each state the mean of its
layout group (which sentences before the asked pick are locker sentences, x0_probe.layout; groups of one item dropped),
beside A: remove A, remove Alf (each against the random part of its own share), keep only A, keep only Alf (each against
the random part alone), both readers, the same items. Pre-stated reading (Dan): if the 9B lookup effect disappears with
the layout-free A, the reading is "position information", not "address".

uv run python scripts/x0_massmean.py run --name x0_massmean_27b --single x0_single_27b_r2 --states x0_probe_v4_27b
uv run python scripts/x0_massmean.py run --name x0_massmean_lf_27b --single x0_single_27b_r2 --states x0_probe_v4_27b --mode layout_free
uv run python scripts/x0_massmean.py verdict --name x0_massmean_27b
"""

from __future__ import annotations

import argparse
import collections
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
# per mode: the subspaces removed, and the subspaces kept alone with the name of their random arm
MODES = {
    "main": {"remove": ("A", "V", "AV"), "keep": {"AV": "keep_rand"}},
    "layout_free": {"remove": ("A", "Alf"), "keep": {"A": "keep_A_rand", "Alf": "keep_Alf_rand"}},
    # the 122B grid (Dan, 25 Oct ~00:20): A, V and Alf removed and kept alone; pca: the layer's top-2,000 PCA directions at
    # Alf's share per item (x0_parts.equal_share), the reference at the same share
    "grid": {
        "remove": ("A", "V", "Alf", "pca"),
        "keep": {"A": "keep_A_rand", "V": "keep_V_rand", "Alf": "keep_Alf_rand"},
    },
}
NOTE = "Descriptive, added after data (Dan, 24 Oct ~20:05; layout-free arm ~21:50); not part of X0's rule."


def arms_of(mode: str) -> tuple[str, ...]:
    md = MODES[mode]
    rem = md["remove"]
    return ("whole", *(f"no_{s}" for s in rem), *(f"no_{s}_rand" for s in rem),
            *(a for s, r in md["keep"].items() for a in (f"keep_{s}", r)))  # fmt: skip


def mass_mean(x: np.ndarray, labels: list) -> np.ndarray:
    """An orthonormal basis [d, classes - 1] of the class means minus the grand mean (raw space)."""
    mu = x.mean(0)
    means = np.stack(
        [x[[i for i, v in enumerate(labels) if v == c]].mean(0) - mu for c in sorted(set(labels), key=str)]
    )
    u, s, _ = np.linalg.svd(means.T, full_matrices=False)
    return u[:, : int((s > s.max() * 1e-8).sum())]


def layout_free(states_run: str) -> tuple[list[dict], np.ndarray, np.ndarray, list[dict], collections.Counter]:
    """A probe run's locker-before org states: their items and states, and the states of the items whose layout group
    has more than one member with the group's mean taken out (the layout-free states Alf is fit on), with their items
    and the group sizes."""
    src = P.RESULTS / states_run
    items = X.read_jsonl(src / "items.jsonl")
    keep = [i for i, it in enumerate(items) if it["order"] == "before"]
    h = np.load(src / "states.npz")["h"].astype(np.float64)[keep]
    kept = [items[i] for i in keep]
    group = [P.layout(it["context"], it["pick_index"]) for it in kept]
    size = collections.Counter(group)
    multi = [j for j, g in enumerate(group) if size[g] > 1]
    res = h[multi].copy()
    for g in {group[j] for j in multi}:
        rows = [r for r, j in enumerate(multi) if group[j] == g]
        res[rows] -= res[rows].mean(0)
    return kept, h, res, [kept[j] for j in multi], size


def entity_means(states_run: str) -> dict[str, np.ndarray]:
    """Each bridge entity's mean layout-free state: D1's identity direction is mu_alt - mu_org (Dan 26 Oct ~11:55)."""
    _, _, res, items, _ = layout_free(states_run)
    ents = [it["entity"] for it in items]
    return {e: res[[i for i, x in enumerate(ents) if x == e]].mean(0) for e in sorted(set(ents))}


def subspaces(states_run: str) -> tuple[dict[str, np.ndarray], dict]:
    """A, V, span(A, V), Alf (A after subtracting each layout group's mean) and Id (the same, by the bridge's identity)
    from a probe run's locker-before org states."""
    kept, h, res, multi, size = layout_free(states_run)
    a = mass_mean(h, [it["locker_index"] for it in kept])
    v = mass_mean(h, [it["answer"] for it in kept])
    u, s, _ = np.linalg.svd(np.concatenate([a, v], 1), full_matrices=False)
    av = u[:, : int((s > s.max() * 1e-8).sum())]
    alf = mass_mean(res, [it["locker_index"] for it in multi])
    # the identity subspace (D1, Dan 26 Oct ~11:55: descriptive only, one arm)
    idn = mass_mean(res, [it["entity"] for it in multi])
    info = {"states_run": states_run, "n": len(kept),
            "rank": {"A": a.shape[1], "V": v.shape[1], "AV": av.shape[1], "Alf": alf.shape[1], "Id": idn.shape[1]},
            "layout_groups": {"groups": len(size), "items_kept": len(multi), "singletons_dropped": len(kept) - len(multi)},
            # mean squared cosine of the principal angles between A and Alf (1: the same subspace, 0: orthogonal)
            "A_Alf_overlap": float(((a.T @ alf) ** 2).sum() / min(a.shape[1], alf.shape[1]))}  # fmt: skip
    return {"A": a, "V": v, "AV": av, "Alf": alf, "Id": idn}, info


def stage_run(name: str, single: str, states_run: str, mode: str = "main") -> Path:
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
         "subspaces": info, "mode": mode, "arms": list(arms_of(mode)), "model": pins.model_pin(), "code": git_state(),
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
                v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]].to("cuda")
                for v in ("org", "alt")
            }
            deltas.append((h["alt"] - h["org"]).float())
        x = torch.stack(deltas)
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to("cuda")
        md, names = MODES[mode], arms_of(mode)
        arms, shares = {"whole": x}, {}
        for s in md["remove"]:
            if s == "pca":  # at Alf's share, item by item (Alf comes first in the grid's remove list)
                from scripts import x0_parts as XP

                pca, info["pca"] = XP.pca_dictionary(model, layer)
                part, _ = XP.equal_share(pca, x, torch.tensor(shares["Alf"], device="cuda"))
            else:
                q = torch.tensor(basis_np[s], dtype=torch.float32, device="cuda")
                part = (x @ q) @ q.T
            share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
            rand = SP.random_subspace_part(x, share, basis)
            arms[f"no_{s}"], arms[f"no_{s}_rand"] = x - part, x - rand
            shares[s] = share.cpu().tolist()
            if s in md["keep"]:
                arms[f"keep_{s}"], arms[md["keep"][s]] = part, rand
        rows = []
        for i, c in enumerate(progress(cases, f"reads at layer {layer} (case)")):
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[a][i : i + 1], [c["pos"]])} for a in names]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                for a, lg in zip(("none", *names), logits, strict=True):
                    rows.append({"scene": c["scene"], "entity": c["bridge"], "reader": w, "arm": a,
                                 **{f"share_{s}": round(shares[s][i], 5) for s in md["remove"]}, **X.read_row(lg, rd, digits)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")  # with the PCA dictionary's record (grid)
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
    mode = m.get("mode", "main")
    md, names = MODES[mode], arms_of(mode)
    lf = sub.get("layout_groups")
    lines = [f"# Mass-mean address (A) and value (V) subspaces: remove or keep only ({name}, mode {mode})", "",
             f"{NOTE} Model {m['model']['target']}, layer {m['layer']}, {m['items']} single-change items of {m['single']} "
             f"(both locker sentences before the pick); A rank {sub['rank']['A']}, V rank {sub['rank']['V']}, span(A, V) "
             f"rank {sub['rank']['AV']}"
             + (f", layout-free A (Alf) rank {sub['rank']['Alf']} from {lf['items_kept']} states in {lf['groups']} layout "
                f"groups ({lf['singletons_dropped']} single-item groups dropped; A-Alf overlap, mean squared cosine of the "
                f"principal angles, {sub['A_Alf_overlap']:.3f})" if lf else "")
             + f", from {sub['states_run']} (locker-before, n = {sub['n']}). Bootstrap over bridge entities ({n_boot} "
             "resamples). UNVERIFIED.", "",
             "| reader | S_whole | arm | median share of ‖Δ‖² | S_arm | S_rand | dependence | random dependence | excess |",
             "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob = []
    for w in X.READERS:
        mine = [r for r in rows if r["reader"] == w]
        scenes = sorted({r["scene"] for r in mine})
        got = {(r["scene"], r["arm"]): r["switched"] for r in mine}
        ent = {r["scene"]: r["entity"] for r in mine}
        sw = {a: [got[(s, a)] for s in scenes] for a in names}
        r_ = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot)
        s = {a: float(np.mean(sw[a])) for a in names}
        res = {"reader": w, "n": len(scenes), "switched_whole": int(sum(sw["whole"])), "S": s}
        for sp in md["remove"]:
            share = float(np.median([r[f"share_{sp}"] for r in mine if r["arm"] == "whole"]))
            dep, rdep = AM.with_ci(X.dependence, s, r_, f"no_{sp}"), AM.with_ci(X.dependence, s, r_, f"no_{sp}_rand")
            ex = AM.paired(X.dependence, s, r_, f"no_{sp}", f"no_{sp}_rand")
            res[sp] = {"share": share, "dep": dep, "rand_dep": rdep, "excess": ex}
            lines.append(f"| {'lookup' if w == X.LOOKUP else 'recall'} | {s['whole']:.2f} ({res['switched_whole']}) | "
                         f"remove {sp} | {share:.4f} | {s[f'no_{sp}']:.2f} | {s[f'no_{sp}_rand']:.2f} | {ci(dep)} | "
                         f"{ci(rdep)} | {ci(ex)} |")  # fmt: skip
        for sp, rand in md["keep"].items():
            keep, krand = AM.with_ci(AM.of_whole, s, r_, f"keep_{sp}"), AM.with_ci(AM.of_whole, s, r_, rand)
            diff = AM.paired(AM.of_whole, s, r_, f"keep_{sp}", rand)
            # "keep" (main mode's only kept subspace, span(A, V)) is the key x0_details and the status pack read
            res["keep" if sp == "AV" else f"keep_{sp}"] = {f"keep_{sp}": keep, "keep_rand": krand, "difference": diff}
            lines.append(f"| {'lookup' if w == X.LOOKUP else 'recall'} | {s['whole']:.2f} ({res['switched_whole']}) | keep "
                         f"only {'(A + V)' if sp == 'AV' else sp} | {res[sp]['share']:.4f} | {s[f'keep_{sp}']:.2f} | "
                         f"{s[rand]:.2f} | kept / whole {ci(keep)} | random kept / whole {ci(krand)} | {ci(diff)} |")  # fmt: skip
        blob.append(res)
    if mode == "main":
        lines += ["", "Pre-stated reading (Dan): the lookup loses flips under A (or V) while the recall does not -> 'the "
                  "lookup uses the address (or the value)'; no arm changes the lookup -> 'the lookup's channel is not a "
                  "low-rank linear readout of the address or the value; what it is stays open'."]  # fmt: skip
    elif mode == "grid":
        lk, rc = (next(r for r in blob if r["reader"] == w)["Alf"]["excess"] for w in X.READERS)
        branch = ("(a) lookup-specific" if lk[0] >= 0.20 and lk[1] > 0 and (rc[0] <= 0.10 or rc[0] <= lk[0] / 2) else
                  "(c) neither" if lk[1] <= 0 else "(b) both readers" if lk[0] >= 0.10 and rc[0] >= 0.10 else "(d) none of these")  # fmt: skip
        lines += ["", "Rule (Dan, 25 Oct ~00:20, the 9B / 27B thresholds; batch 31's Q31.5): Alf removed is (a) lookup-specific "
                  "iff lookup excess >= 0.20 (lower CI > 0) and recall <= 0.10 or at most half the lookup's; (b) both readers "
                  "iff both lose >= 0.10 and not (a); (c) neither iff the lookup's lower CI <= 0; else (d). This run: lookup "
                  f"{ci(lk)}, recall {ci(rc)} -> {branch}."]  # fmt: skip
    else:
        lk = next(r for r in blob if r["reader"] == X.LOOKUP)["Alf"]["excess"]
        gone = lk[1] <= 0
        lines += ["", "Pre-stated reading (Dan, ~21:50; no prediction committed before the run): if the 9B lookup effect "
                  "disappears with the layout-free A, the reading is 'position information', not 'address'. 'Disappears' "
                  "(set by the agent before the run, Q28.1's criterion): the lookup's excess with Alf removed has a lower "
                  f"CI <= 0. This run: {ci(lk)} -> {'disappears' if gone else 'does not disappear'}"
                  + ("." if "9b" in m["model"]["target"] else " (the reading is stated for the 9B; reported here only).")]  # fmt: skip
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
    ap.add_argument("--mode", choices=list(MODES), default="main")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "run":
        stage_run(a.name, a.single, a.states, a.mode)
    stage_verdict(a.name, a.n_boot)


if __name__ == "__main__":
    main()
