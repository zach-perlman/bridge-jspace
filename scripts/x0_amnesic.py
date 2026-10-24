"""x0_amnesic (Dan's item 6, 24 Oct ~18:45; descriptive, added after data): does the bridge edit act on the readers
through the subspace where a linear probe reads the address (the index of the bridge's locker sentence)?

The probe-(b) subspace P: one-hot ridge on the org states at the bridge's word of fresh scenes (x0_probe_power's
d1_topics_v4 states, locker-before; penalty by entity-held-out CV), its decision directions in raw state space centered
across classes (rank = classes - 1). On the single-change items (x0_single_*: the asked pick becomes another person's,
nothing else changes), at the model's X0 layer, Δ = h_alt - h_org at the bridge's word, and arms on the org run:
  whole (Δ); no_probe (Δ - PΔ); no_rand (Δ minus a random-subspace part of PΔ's share, X0's rand_sub);
  probe_only (PΔ: sufficiency); rand_only (the random part alone, at the same share: the agent's matched control).
Both readers on the identical patch, X0's top-token read. Per reader and locker order (before is primary): S per arm,
the probe dependence 1 - S_no_probe / S_whole against the random one, and S_probe_only / S_whole against
S_rand_only / S_whole; 95% CIs from a cluster bootstrap over bridge entities (10,000 resamples, seed 0).
The run also saves, per item, h_org, Δ and the J++ parts of Δ at k = 25 and 100 (signed OMP, X0's letter atoms), so
the probe can be read on h_alt and on patched states on the CPU (Dan's items 2 and 3).

uv run python scripts/x0_amnesic.py run --name x0_amnesic_27b --single x0_single_27b_r2 --probe x0_probe_v4_27b
uv run python scripts/x0_amnesic.py verdict --name x0_amnesic_27b
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
from scripts import x0_necessity as X
from scripts import x0_probe as P
from scripts import x0_strata as ST

EXP = "x0_amnesic"
RESULTS = pins.RESULTS_DIR / EXP
ARMS = ("whole", "no_probe", "no_rand", "probe_only", "rand_only")
K_SAVE = (25, 100)
NOTE = "Descriptive, added after data (Dan, 24 Oct ~18:45, item 6); not part of X0's rule."


def probe_basis(probe_run: str) -> tuple[np.ndarray, dict]:
    """The probe-(b) subspace from a probe run's locker-before states, and how well that probe reads (CV)."""
    src = P.RESULTS / probe_run
    z = np.load(src / "states.npz")
    items = X.read_jsonl(src / "items.jsonl")
    keep = [i for i, it in enumerate(items) if it["order"] == "before"]
    x = z["h"].astype(np.float64)[keep]
    y = [items[i]["locker_index"] for i in keep]
    ents = [items[i]["entity"] for i in keep]
    rel = P.select_penalty(x, y, ents)
    pred, _, _ = P.cv_predict(x, y, ents, True)
    q = P.subspace(x, y, rel)
    info = {"probe_run": probe_run, "n": len(y), "classes": sorted(set(y)), "penalty": rel, "rank": q.shape[1],
            "cv_accuracy": float(np.mean([p == t for p, t in zip(pred, y, strict=True)]))}  # fmt: skip
    return q, info


def stage_run(name: str, single: str, probe_run: str) -> Path:
    import torch

    from bridge_jspace.lens import JLens
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
    scenes = sorted(
        {r["scene"] for r in X.read_jsonl(X.RESULTS / single / "outcomes.jsonl") if r["rendering"] == "chat"}
    )
    q_np, info = probe_basis(probe_run)
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "note": NOTE,
         "single": single, "single_code": sm["code"], "set": sm["set"], "layer": layer, "items": len(scenes),
         "probe": info, "arms": list(ARMS), "k_saved": list(K_SAVE), "model": pins.model_pin(), "code": git_state(),
         "lens": X.lens_record(), "seeds": {"random_subspace": f"{X.SUBSPACE_SEED} + layer (CPU)",
                                            "bootstrap": X.BOOT_SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print(json.dumps(info), flush=True)
    X.ALT = "single"
    model = load_model()
    lens = JLens(model, "jpp")
    cases, _ = X.build_cases(model.tokenizer, sm["set"])
    by_scene = {c["scene"]: c for c in cases if c["rendering"] == "chat"}
    cases = [by_scene[s] for s in scenes]
    order = {c["scene"]: ST.features(c)["org locker vs asked pick"] for c in cases}
    ws = X.whitespace_mask(model)
    digits = torch.tensor(X.digit_ids(model.tokenizer), device="cuda")
    with torch.no_grad():
        h_org, deltas = [], []
        for c in progress(cases, "Δ at the bridge's word (case)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {
                v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]]
                for v in ("org", "alt")
            }
            h_org.append(h["org"].float())
            deltas.append((h["alt"] - h["org"]).float())
        x = torch.stack(deltas)
        q = torch.tensor(q_np, dtype=torch.float32, device="cuda")
        part = (x @ q) @ q.T
        share = part.norm(dim=-1) ** 2 / (x.norm(dim=-1) ** 2).clamp_min(1e-30)
        basis = SP.random_basis(x.shape[1], torch.Generator().manual_seed(X.SUBSPACE_SEED + layer)).to("cuda")
        rand = SP.random_subspace_part(x, share, basis)
        arms = {"whole": x, "no_probe": x - part, "no_rand": x - rand, "probe_only": part, "rand_only": rand}
        dic = X.dictionary("jpp", layer, model, lens, model.letter_token_ids())
        jparts = {k: X.fit(dic, x, k, "signed") for k in K_SAVE}
        rows = []
        for i, c in enumerate(progress(cases, f"reads at layer {layer} (case)")):
            for w, rd in c["readers"].items():
                edits = [{}] + [{layer: AddRows(arms[a][i : i + 1], [c["pos"]])} for a in ARMS]
                logits, _ = X.read_logits(model, rd["ids"]["org"], edits, "chat", c["space"], ws)
                for a, lg in zip(("none", *ARMS), logits, strict=True):
                    rows.append({"scene": c["scene"], "entity": c["bridge"], "reader": w, "order": order[c["scene"]],
                                 "arm": a, "share": round(float(share[i]), 5), **X.read_row(lg, rd, digits)})  # fmt: skip
    X.write_jsonl(out / "outcomes.jsonl", rows)
    f16 = lambda t: t.cpu().numpy().astype(np.float16)  # noqa: E731  (size; every value here is far below fp16's max)
    np.savez_compressed(out / "states.npz", scene=np.array(scenes), h_org=f16(torch.stack(h_org)), delta=f16(x),
                        probe_basis=q_np, **{f"jpp_k{k}": f16(v) for k, v in jparts.items()})  # fmt: skip
    print("wrote", out, flush=True)
    return out


def of_whole(s_whole, s_arm):
    """S_arm / S_whole (nan where nothing switched with the whole edit)."""
    whole = np.asarray(s_whole, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.asarray(s_arm, dtype=float) / np.where(whole > 0, whole, np.nan)


def with_ci(f, s: dict, r: dict, arm: str) -> list[float]:
    """f(S_whole, S_arm) and its bootstrap interval."""
    return [float(f(s["whole"], s[arm])), *X.interval(f(r["whole"], r[arm]))]


def paired(f, s: dict, r: dict, a: str, b: str) -> list[float]:
    """f(.., a) - f(.., b) on the same resamples, and its interval."""
    return [float(f(s["whole"], s[a]) - f(s["whole"], s[b])), *X.interval(f(r["whole"], r[a]) - f(r["whole"], r[b]))]


def stage_verdict(name: str, n_boot: int = X.N_BOOT) -> Path:
    src = RESULTS / name
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "outcomes.jsonl")
    out = src / f"verdict-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir()
    ci = lambda v: f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"  # noqa: E731
    lines = [f"# Probe-(b) subspace: remove it, or keep only it ({name})", "",
             f"{NOTE} Model {m['model']['target']}, layer {m['layer']}, single-change items of {m['single']}; probe "
             f"subspace rank {m['probe']['rank']} from {m['probe']['probe_run']} (locker-before, n = {m['probe']['n']}, "
             f"CV accuracy {m['probe']['cv_accuracy']:.2f}). Bootstrap over bridge entities, {n_boot} resamples. "
             "UNVERIFIED.", "",
             "| locker vs pick | reader | n | median share of ‖Δ‖² in P | S_whole | S_no_probe | S_no_rand | probe dep. | "
             "random dep. | excess | S_probe_only / S_whole | S_rand_only / S_whole | difference |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    blob = []
    for order in ("before", "after"):
        for w in X.READERS:
            mine = [r for r in rows if r["reader"] == w and r["order"] == order]
            scenes = sorted({r["scene"] for r in mine})
            if not scenes:
                continue
            got = {(r["scene"], r["arm"]): r["switched"] for r in mine}
            ent = {r["scene"]: r["entity"] for r in mine}
            sw = {a: [got[(s, a)] for s in scenes] for a in ARMS}
            r_ = X.resampled_rates(sw, [ent[s] for s in scenes], n_boot)
            s = {a: float(np.mean(sw[a])) for a in ARMS}
            pdep, rdep = (with_ci(X.dependence, s, r_, a) for a in ("no_probe", "no_rand"))
            excess = paired(X.dependence, s, r_, "no_probe", "no_rand")
            fp, fr = (with_ci(of_whole, s, r_, a) for a in ("probe_only", "rand_only"))
            diff = paired(of_whole, s, r_, "probe_only", "rand_only")
            share = float(np.median([r["share"] for r in mine if r["arm"] == "whole"]))
            blob.append({"order": order, "reader": w, "n": len(scenes), "switched_whole": int(sum(sw["whole"])),
                         "S": s, "probe_dep": pdep, "rand_dep": rdep, "excess": excess, "probe_only": fp,
                         "rand_only": fr, "sufficiency_diff": diff, "median_share": share})  # fmt: skip
            flag = " ⚠" if sum(sw["whole"]) < X.VALID_N else ""
            lines.append(f"| {order} | {'lookup' if w == X.LOOKUP else 'recall'} | {len(scenes)} | {share:.4f} | "
                         f"{s['whole']:.2f} ({int(sum(sw['whole']))}{flag}) | {s['no_probe']:.2f} | {s['no_rand']:.2f} | "
                         f"{ci(pdep)} | {ci(rdep)} | {ci(excess)} | {ci(fp)} | {ci(fr)} | {ci(diff)} |")  # fmt: skip
    lines += ["", "⚠ = fewer than 30 items switched by the whole edit."]
    (out / "verdict.json").write_text(json.dumps({"run": name, "manifest": m, "rows": blob}, indent=1) + "\n")
    (out / "verdict.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["run", "verdict"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--single", default="x0_single_27b_r2")
    ap.add_argument("--probe", default="x0_probe_v4_27b")
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "run":
        stage_run(a.name, a.single, a.probe)
    stage_verdict(a.name, a.n_boot)


if __name__ == "__main__":
    main()
