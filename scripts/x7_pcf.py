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
import re
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


def pairs(tok, n: int, seed: int = SEED, moves: frozenset[int] | None = None) -> tuple[list[dict], collections.Counter]:
    """n pairs O / S: the same scene, the bridge's locker sentence trading places with another item's, digits kept;
    `moves` (batch 45c): only pairs whose two slots are exactly these (e.g. {1, 2}: the second and third)."""
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
        if moves is not None and {order.index(A), order.index(other)} != moves:
            dropped["outside the slots asked for"] += 1
            continue
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


MAX_MOVES = 3  # natural pairs per passage at most (seeded choice of the target slots)


def natural_pairs(tok, seed: int = SEED) -> tuple[list[dict], collections.Counter]:
    """Natural passages (x5_natural's set and cases): the sentence with the bridge's first mention moved to another
    place in its paragraph, still before the binding sentence, its words unchanged; per pair the lookup prompts of O and
    S and the bridge word's token index (in the binding sentence) in each. Passages that allow no move are counted."""
    from bridge_jspace.tokens import raw_encoding
    from scripts import statement_positions as SP
    from scripts import tasks_v2 as T
    from scripts import x5_natural as N

    items = {pp["scene"]: pp for pp, _ in N.load()[0]}
    cases, _ = N.build_cases(tok)
    rng = random.Random(seed)
    out, why = [], collections.Counter({"passages": len(cases)})
    for c in cases:
        ctx, bridge = c["context"], c["bridge"]
        sents = N.sentences(ctx)
        bind = next(s for s in sents if N.names(s, bridge) and not N.values_in(s, c["vocab"]))
        first = next(s for s in sents if N.names(s, bridge))
        if first == bind:
            why["the binding sentence is the first mention"] += 1
            continue
        para = next(line for line in ctx.split("\n") if first in line)
        ps = [s for s in re.split(r"(?<=[.!?])\s+", para) if s]
        if " ".join(ps) != para or first not in ps:
            why["the paragraph does not split cleanly"] += 1
            continue
        f = ps.index(first)
        b = ps.index(bind) if bind in ps else len(ps)
        targets = [t for t in range(b) if t != f]
        if not targets:
            why["no other place before the binding sentence"] += 1
            continue
        why["passages that allow a move"] += 1
        for t in sorted(rng.sample(targets, min(MAX_MOVES, len(targets)))):
            moved = ps[:f] + ps[f + 1 :]
            moved.insert(t, first)
            s_ctx = ctx.replace(para, " ".join(moved))
            ids, at = {}, {}
            for v, cc in (("org", ctx), ("alt", s_ctx)):
                text = T.render(tok, {**items[c["scene"]], "context": cc})
                enc = raw_encoding(tok, text, offsets=True)
                w0 = text.index(cc) + cc.index(bind) + bind.rindex(bridge)
                ids[v], at[v] = list(enc["input_ids"]), SP.tokens_in(enc["offset_mapping"], w0, w0 + len(bridge))
            if len(at["org"]) != 1 or len(at["alt"]) != 1:
                why["the bridge is not one token"] += 1
                continue
            out.append({"scene": c["scene"], "relation": c["relation"], "bridge": bridge, "move": [f, t],
                        "ids": ids, "pos": {"org": at["org"][0], "alt": at["alt"][0]}})  # fmt: skip
    why["pairs"] = len(out)
    return out, why


def principal_cos2(p: np.ndarray, q: np.ndarray) -> list[float]:
    """cos² of the principal angles between the column spans of two orthonormal bases (largest first)."""
    return [float(s) ** 2 for s in np.linalg.svd(p.T @ q, compute_uv=False)]


def top_pcs(x: np.ndarray, rank: int = RANK) -> np.ndarray:
    """The top `rank` components of a centered PCA of the rows of x, as an orthonormal [d, rank] basis."""
    _, _, vt = np.linalg.svd(x - x.mean(0), full_matrices=False)
    return vt[:rank].T


def split_half(x: np.ndarray, groups: list[str], seed: int = 0) -> dict:
    """The noise ceiling (Dan 26 Oct ~12:55): the top-RANK PCA fit on two random halves of the groups (passages or
    pairs; seed 0), and the mean cos² of the principal angles between the halves."""
    keys = sorted(set(groups))
    pick = set(np.asarray(keys)[np.random.default_rng(seed).permutation(len(keys))[: len(keys) // 2]].tolist())
    a = [i for i, g in enumerate(groups) if g in pick]
    b = [i for i, g in enumerate(groups) if g not in pick]
    cos2 = principal_cos2(top_pcs(x[a]), top_pcs(x[b]))
    return {"rows": [len(a), len(b)], "groups": [len(pick), len(keys) - len(pick)], "cos2": cos2,
            "mean_cos2": float(np.mean(cos2)), "seed": seed}  # fmt: skip


def stage_run(name: str, n: int = N_PAIRS, moves: frozenset[int] | None = None) -> Path:
    """--moves (batch 45c, Dan 26 Oct ~18:30): pairs whose bridge locker moves between these slots only (1-2: the
    second and third); the differences are projected off the mass-mean pointer directions U before the PCA (the basis
    is orthogonal to U by construction) and the rank is 2."""
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
    rank = RANK if moves is None else 2
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "pairs": n,
         "rank": rank, "pca": "centered, over the pairs' bridge-word differences S - O", "alf_from": R.STATES[target],
         "moves": sorted(moves) if moves else None,
         "orthogonal_to_U": "the differences projected off U (Alf) before the PCA" if moves else None,
         "seeds": {"pairs": SEED}, "note": "Dan 26 Oct ~10:45 / ~11:55; batch 43 (--moves: batch 45c)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    cases, dropped = pairs(model.tokenizer, n, moves=moves)
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
    alf = MM.subspaces(R.STATES[target])[0]["Alf"]
    if moves is not None:  # 45c: the basis outside U
        xd = xd - (xd @ alf) @ alf.T
    centered = xd - xd.mean(0)
    _, s, vt = np.linalg.svd(centered, full_matrices=False)
    var = (s**2 / (s**2).sum()).tolist()
    p = vt[:rank].T  # [d, rank]
    cos2 = principal_cos2(p, alf)
    pt = torch.tensor(p, dtype=torch.float64, device="cuda")
    in_jpp = []
    for i in range(len(cases)):
        q, _ = torch.linalg.qr(jdic[atoms[i]].T.double())
        in_jpp.append(float(((q.T @ pt) ** 2).sum()) / rank)
    report = {"run": name, "model": target, "layer": layer, "pairs": len(cases), "dropped": dict(dropped),
              "variance_explained": var[:SHOW], "variance_explained_cum": np.cumsum(var[:SHOW]).tolist(),
              "cos2_with_alf": cos2, "mean_cos2_with_alf": float(np.mean(cos2)), "random_mean_cos2": rank / p.shape[0],
              "split_half": split_half(xd, [c["scene"] for c in cases]),
              "alf_rank": int(alf.shape[1]), "share_in_jpp_span": {"mean": float(np.mean(in_jpp)),
                                                                  "median": float(np.median(in_jpp))}}  # fmt: skip
    np.savez_compressed(out / "pcf.npz", P=p.astype(np.float32), mean=xd.mean(0).astype(np.float32), var=np.array(var))
    (out / "report.json").write_text(json.dumps(report, indent=1) + "\n")
    pct = ", ".join(f"{k + 1}: {100 * v:.1f}%" for k, v in enumerate(var[:SHOW]))
    lines = [f"# P_cf, a pointer without slot labels: {name}", "",
             f"Model {target}, layer {layer}; {len(cases)} pairs (the bridge's locker sentence trades places with another "
             f"item's, digits kept); PCA centered over the bridge word's S - O. UNVERIFIED.", "",
             f"- Variance explained by components 1-{SHOW}: {pct}.",
             f"- Split-half noise ceiling (two random halves by {'passage' if 'counts' in report else 'pair'}, seed 0): "
             f"mean cos² {report['split_half']['mean_cos2']:.3f} ({report['split_half']['rows'][0]} / "
             f"{report['split_half']['rows'][1]} rows).",
             f"- Principal angles with the mass-mean pointer directions (rank {alf.shape[1]}): cos² "
             + ", ".join(f"{v:.3f}" for v in cos2) + f"; mean {np.mean(cos2):.3f} (a random subspace: {rank / p.shape[0]:.4f}).",
             f"- P_cf's share inside each pair's 25-atom J++ span: mean {np.mean(in_jpp):.3f}, median "
             f"{np.median(in_jpp):.3f} (descriptive)."]  # fmt: skip
    (out / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    return out


def stage_natural(name: str, pcf_run: str) -> Path:
    """P_cf_nat (batch 43's natural-passage step, Dan 26 Oct ~11:25): the same PCA over natural pairs (natural_pairs),
    the bridge word read in the binding sentence; its principal angles with P_cf (x7_pcf/<pcf_run>) and with Alf."""
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
         "model": pins.model_pin(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "rank": RANK,
         "pairs_from": "x5_natural's passages: the bridge's first-mention sentence moved within its paragraph, still "
                       f"before the binding sentence, words unchanged (at most {MAX_MOVES} moves per passage)",
         "pcf_run": pcf_run, "alf_from": R.STATES[target], "seeds": {"moves": SEED}}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    cases, why = natural_pairs(model.tokenizer)
    X.write_jsonl(out / "cases.jsonl", [{k: v for k, v in c.items() if k != "ids"} for c in cases])
    with torch.no_grad():
        diffs = []
        for c in progress(cases, f"S - O at layer {layer} (natural pair)"):
            h = {v: model.run(torch.tensor([c["ids"][v]], device="cuda"), record=(layer,))[1][layer][c["pos"][v]].float()
                 for v in ("org", "alt")}  # fmt: skip
            diffs.append((h["alt"] - h["org"]).to("cuda"))
        x = torch.stack(diffs)
        jdic = JLens(model, "jpp").vectors(layer, model.letter_token_ids())
        atoms = omp_atoms(jdic, x, X.K_MAIN)
    xd = x.double().cpu().numpy()
    _, s, vt = np.linalg.svd(xd - xd.mean(0), full_matrices=False)
    var = (s**2 / (s**2).sum()).tolist()
    p = vt[:RANK].T
    pcf = np.load(pins.RESULTS_DIR / EXP / pcf_run / "pcf.npz")["P"].astype(np.float64)
    alf = MM.subspaces(R.STATES[target])[0]["Alf"]
    cos_pcf, cos_alf = principal_cos2(p, pcf), principal_cos2(p, alf)
    pt = torch.tensor(p, dtype=torch.float64, device="cuda")
    in_jpp = []
    for i in range(len(cases)):
        q, _ = torch.linalg.qr(jdic[atoms[i]].T.double())
        in_jpp.append(float(((q.T @ pt) ** 2).sum()) / RANK)
    report = {"run": name, "model": target, "layer": layer, "counts": dict(why),
              "passages_allowing_a_move": why["passages that allow a move"], "pairs": len(cases),
              "variance_explained": var[:SHOW], "cos2_with_pcf": cos_pcf, "mean_cos2_with_pcf": float(np.mean(cos_pcf)),
              "split_half": split_half(xd, [c["scene"] for c in cases]),
              "cos2_with_alf": cos_alf, "mean_cos2_with_alf": float(np.mean(cos_alf)),
              "random_mean_cos2": RANK / p.shape[0],
              "share_in_jpp_span": {"mean": float(np.mean(in_jpp)), "median": float(np.median(in_jpp))}}  # fmt: skip
    np.savez_compressed(out / "pcf.npz", P=p.astype(np.float32), mean=xd.mean(0).astype(np.float32), var=np.array(var))
    (out / "report.json").write_text(json.dumps(report, indent=1) + "\n")
    pct = ", ".join(f"{k + 1}: {100 * v:.1f}%" for k, v in enumerate(var[:SHOW]))
    lines = [f"# P_cf_nat, the pointer from natural passages: {name}", "",
             f"Model {target}, layer {layer}; {why['passages that allow a move']} of {why['passages']} passages allow a "
             f"move ({dict(why)}); {len(cases)} pairs; PCA centered over the bridge word's S - O. UNVERIFIED.", "",
             f"- Variance explained by components 1-{SHOW}: {pct}.",
             f"- Split-half noise ceiling (two random halves by {'passage' if 'counts' in report else 'pair'}, seed 0): "
             f"mean cos² {report['split_half']['mean_cos2']:.3f} ({report['split_half']['rows'][0]} / "
             f"{report['split_half']['rows'][1]} rows).",
             f"- cos² of the principal angles with P_cf ({pcf_run}): " + ", ".join(f"{v:.3f}" for v in cos_pcf)
             + f"; mean {np.mean(cos_pcf):.3f}. With the mass-mean pointer directions: mean {np.mean(cos_alf):.3f} "
             f"(a random subspace: {RANK / p.shape[0]:.4f}).",
             f"- P_cf_nat's share inside each pair's 25-atom J++ span: mean {np.mean(in_jpp):.3f} (descriptive)."]  # fmt: skip
    (out / "report.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "natural"])
    ap.add_argument("--name")
    ap.add_argument("--n", type=int, default=N_PAIRS)
    ap.add_argument("--pcf", help="natural: the simple-scene P_cf run (results/x7_pcf/<run>) to compare with")
    ap.add_argument("--moves", default=None, metavar="J-K",
                    help="plan / run: only pairs whose bridge locker moves between these slots (45c: 1-2), rank 2, off U")  # fmt: skip
    a = ap.parse_args()
    moves = frozenset(int(v) for v in a.moves.split("-")) if a.moves else None
    if a.stage == "natural":
        stage_natural(a.name, a.pcf)
        return
    if a.stage == "plan":
        from scripts import statement_positions as SP

        cases, dropped = pairs(SP.load_tokenizer(), a.n, moves=moves)
        print(len(cases), "pairs;", dict(dropped), cases[0]["context"], "|", cases[0]["cf_context"], sep="\n")
    else:
        stage_run(a.name, a.n, moves)


if __name__ == "__main__":
    main()
