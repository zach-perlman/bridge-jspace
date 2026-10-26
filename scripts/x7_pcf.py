"""x7_pcf (P_cf, Dan 26 Oct ~10:45 and ~11:55; batch 43): a pointer found without slot labels.

Simple scenes (x6_routes' generator, animals) at the layer fixed in advance: pairs that differ only in where the bridge
item's locker sentence sits ("same item moved" with the same digits: the bridge's locker sentence trades places with
another item's, every digit kept, so the lookup's answer does not change). Per pair the bridge word's state difference
(S - O) at that layer; PCA (centered) over the pairs; P_cf = the top 4 components, with the variance explained by 1-8.
Compared with the mass-mean pointer directions (Alf: x0_massmean over the probe's fresh scenes, not refit) by principal
angles (cos², and their mean over the 4; a random 4-dimensional subspace gives about 4 / d). Descriptive: P_cf's share
inside each pair's own 25-atom J++ span (signed OMP of the pair's difference), the mean over pairs.
Writes results/x7_pcf/<name>/{pcf.npz, report.json, report.md}; `x6_routes run --alf-from x7_pcf/<name>` then runs the
routes test with P_cf in place of Alf. UNVERIFIED.

uv run python scripts/x7_pcf.py run --name x7_pcf_27b     # GPU; BJ_TARGET picks the model
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
from scripts import x6_routes as R

EXP = "x7_pcf"
RESULTS = pins.RESULTS_DIR / EXP
SEED, N_PAIRS, RANK, SHOW = 4301, 1000, 4, 8


def pairs(tok, n: int, seed: int = SEED) -> tuple[list[dict], collections.Counter]:
    """n pairs O / S: the same scene, the bridge's locker sentence trading places with another item's, digits kept."""
    from scripts import suite_v1 as S
    from scripts import tasks_v2 as T

    legs = T.DOMAINS["animals"].values
    animals = sorted(a for a in legs if R.one_token(tok, a) and 0 <= legs[a] <= 9)
    people = sorted(p for p in S.PEOPLE if R.one_token(tok, p))
    rng = random.Random(seed)
    out, dropped = [], collections.Counter()
    i = 0
    while len(out) < n:
        i += 1
        assert i < 100 * n, f"the generator cannot fill {n} pairs: {dropped}"
        A, B, C = rng.sample(animals, 3)
        a, b, c = rng.sample(range(1, 10), 3)
        asked, p1, p2 = rng.sample(people, 3)
        order = rng.sample([A, B, C], 3)
        val = {A: a, B: b, C: c}
        picks = rng.sample([(asked, A), (p1, B), (p2, C)], 3)
        other = rng.choice([B, C])
        sw = {A: other, other: A}
        o = R.context([(x, val[x]) for x in order], picks)
        s = R.context([(sw.get(x, x), val[sw.get(x, x)]) for x in order], picks)
        case, why = R.encode(tok, o, s, asked, A, A, legs, {"switch": a, "original": a}, "C1s", f"C1s-{i:04d}")
        if case is None:
            dropped[why] += 1
            continue
        case["slots"] = {"org": order.index(A), "alt": order.index(other)}
        out.append(case)
    return out, dropped


def principal_cos2(p: np.ndarray, q: np.ndarray) -> list[float]:
    """cos² of the principal angles between the column spans of two orthonormal bases (largest first)."""
    return [float(s) ** 2 for s in np.linalg.svd(p.T @ q, compute_uv=False)]


def stage_run(name: str, n: int = N_PAIRS) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import x0_massmean as MM
    from scripts.x0_parts import omp_atoms

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "pairs": n,
         "rank": RANK, "pca": "centered, over the pairs' bridge-word differences S - O", "alf_from": R.STATES[target],
         "seeds": {"pairs": SEED}, "note": "Dan 26 Oct ~10:45 / ~11:55; batch 43; descriptive until its answers"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    cases, dropped = pairs(model.tokenizer, n)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k not in ("space", "readers")} for c in cases])
    with torch.no_grad():
        diffs = []
        for c in progress(cases, f"S - O at layer {layer} (pair)"):
            ids = c["readers"][X.LOOKUP]["ids"]
            h = {v: model.run(torch.tensor([ids[v]], device="cuda"), record=(layer,))[1][layer][c["pos"]].float()
                 for v in ("org", "alt")}  # fmt: skip
            diffs.append((h["alt"] - h["org"]).to("cuda"))
        x = torch.stack(diffs)
        jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
        atoms = omp_atoms(jdic, x, X.K_MAIN)
    xd = x.double().cpu().numpy()
    centered = xd - xd.mean(0)
    _, s, vt = np.linalg.svd(centered, full_matrices=False)
    var = (s**2 / (s**2).sum()).tolist()
    p = vt[:RANK].T  # [d, RANK]
    alf = MM.subspaces(R.STATES[target])[0]["Alf"]
    cos2 = principal_cos2(p, alf)
    pt = torch.tensor(p, dtype=torch.float64, device="cuda")
    in_jpp = []
    for i in range(len(cases)):
        q, _ = torch.linalg.qr(jdic[atoms[i]].T.double())
        in_jpp.append(float(((q.T @ pt) ** 2).sum()) / RANK)
    report = {"run": name, "model": target, "layer": layer, "pairs": len(cases), "dropped": dict(dropped),
              "variance_explained": var[:SHOW], "variance_explained_cum": np.cumsum(var[:SHOW]).tolist(),
              "cos2_with_alf": cos2, "mean_cos2_with_alf": float(np.mean(cos2)), "random_mean_cos2": RANK / p.shape[0],
              "alf_rank": int(alf.shape[1]), "share_in_jpp_span": {"mean": float(np.mean(in_jpp)),
                                                                  "median": float(np.median(in_jpp))}}  # fmt: skip
    np.savez_compressed(out / "pcf.npz", P=p.astype(np.float32), mean=xd.mean(0).astype(np.float32), var=np.array(var))
    (out / "report.json").write_text(json.dumps(report, indent=1) + "\n")
    pct = ", ".join(f"{k + 1}: {100 * v:.1f}%" for k, v in enumerate(var[:SHOW]))
    lines = [f"# P_cf, a pointer without slot labels: {name}", "",
             f"Model {target}, layer {layer}; {len(cases)} pairs (the bridge's locker sentence trades places with another "
             f"item's, digits kept); PCA centered over the bridge word's S - O. UNVERIFIED.", "",
             f"- Variance explained by components 1-{SHOW}: {pct}.",
             f"- Principal angles with the mass-mean pointer directions (rank {alf.shape[1]}): cos² "
             + ", ".join(f"{v:.3f}" for v in cos2) + f"; mean {np.mean(cos2):.3f} (a random subspace: {RANK / p.shape[0]:.4f}).",
             f"- P_cf's share inside each pair's 25-atom J++ span: mean {np.mean(in_jpp):.3f}, median "
             f"{np.median(in_jpp):.3f} (descriptive)."]  # fmt: skip
    (out / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run"])
    ap.add_argument("--name")
    ap.add_argument("--n", type=int, default=N_PAIRS)
    a = ap.parse_args()
    if a.stage == "plan":
        from scripts import statement_positions as SP

        cases, dropped = pairs(SP.load_tokenizer(), a.n)
        print(len(cases), "pairs;", dict(dropped), cases[0]["context"], "|", cases[0]["cf_context"], sep="\n")
    else:
        stage_run(a.name, a.n)


if __name__ == "__main__":
    main()
