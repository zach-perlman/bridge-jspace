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

`varied` (45d, batch 45, jobs/c3/batch45.yaml; fixed in advance): the same method on the varied scenes (x0b_generalize's
aligned cases of tasks_v2 set x0b_v2), per format (prose, json, table). Per format the scenes are split in two halves
by bridge item (seed 0, disjoint items, split.json); on half 1 ("fit") the pairs: the bridge's locker statement trades places
with another item's (a prose sentence, a JSON object, a table row), each keeping its own number, both before the asked
pick so the bridge word sees both (in json / table every locker row then is; a swap of two statements after the pick
leaves the bridge word's state unchanged), at most MAX_MOVES partners per scene (seeded), the bridge one token at the
same index in O and S. Per format the PCA (centered, rank 4) of the bridge word's S - O: pcf_<format>.npz. Half 2
("test") is the main test: `x0b_generalize run --pcf-from x7_pcf/<name>`.

uv run python scripts/x7_pcf.py run --name x7_pcf_27b     # GPU; BJ_TARGET picks the model
uv run python scripts/x7_pcf.py varied-plan               # tokenizer only: the split, the pairs per format, examples
uv run python scripts/x7_pcf.py varied --name x45d_fit_27b  # GPU: the per-format bases
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
from bridge_jspace.run_switches import switches
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


FORMATS = ("prose", "json", "table")  # 45d: the varied scenes' formats, one basis each
SPLIT_SEED = 0  # 45d: the halves by bridge item


def locker_statement(item: dict, thing: str) -> str:
    """The whole locker statement of `thing` as tasks_v2 renders it in the item's format and number style."""
    from scripts import tasks_v2 as T

    n = item["facts"]["locker"][thing]
    word = T.num(n, item["numbers"])
    fmt = item["format"]
    if fmt == "prose":
        return f"The locker of {T.ref(T.DOMAINS[item['domain']], thing)} is {word}."
    if fmt == "json":
        return json.dumps({"item": thing, "locker": n if item["numbers"] == "digits" else word})
    assert fmt == "table", fmt
    return f"| {thing} | {word} |"


def statement_at(item: dict, thing: str) -> int:
    s = locker_statement(item, thing)
    assert item["context"].count(s) == 1, f"{item.get('id')}: {s!r} is not once in the context"
    return item["context"].index(s)


def before_pick(item: dict, thing: str) -> bool:
    """Whether thing's locker statement starts before the asked person's pick statement."""
    from scripts import x0b_generalize as B

    f = item["facts"]
    return statement_at(item, thing) < B.bridge_start(item, item["context"], f["x"])


def swap_lockers(item: dict, a: str, b: str) -> str:
    """The item's context with the locker statements of a and b trading places, each keeping its own number."""
    ctx = item["context"]
    (p, sp), (q, sq) = sorted((statement_at(item, t), locker_statement(item, t)) for t in (a, b))
    assert p + len(sp) <= q, f"{item.get('id')}: the two locker statements overlap"
    return ctx[:p] + sq + ctx[p + len(sp) : q] + sp + ctx[q + len(sq) :]


def split_items(bridges: list[str], seed: int = SPLIT_SEED) -> dict[str, list[str]]:
    """Two disjoint halves of the bridge items (a seeded permutation of the sorted items): "fit" (the first half,
    P_cf's pairs) and "test" (the rest, the main test)."""
    keys = sorted(set(bridges))
    perm = np.random.default_rng(seed).permutation(len(keys))
    fit = sorted(keys[i] for i in perm[: len(keys) // 2])
    return {"fit": fit, "test": sorted(set(keys) - set(fit))}


def varied_pairs(
    tok, cases: list[dict], items: dict[str, dict], seed: int = SEED, max_moves: int = MAX_MOVES
) -> tuple[list[dict], collections.Counter]:
    """Per varied scene (x0b_generalize's aligned cases; `items`: the lookup item per scene), pairs O / S: the bridge's
    locker statement trades places with another item's, both before the asked pick, numbers kept (the lookup's answer
    does not change); at most max_moves partners per scene (seeded). Per pair the lookup prompts' ids and the bridge's
    token index, the same in O and S (pairs where it is not are dropped and counted)."""
    from scripts import x0b_generalize as B

    rng = random.Random(seed)
    out, why = [], collections.Counter({"scenes": len(cases)})
    for c in cases:
        it = items[c["scene"]]
        x = it["facts"]["x"]
        assert x == c["bridge"], f"{c['scene']}: the case's bridge is not the item's"
        if not before_pick(it, x):
            why["the bridge's locker statement comes after the pick"] += 1
            continue
        partners = sorted(t for t in it["facts"]["locker"] if t != x and before_pick(it, t))
        if not partners:
            why["no other locker statement before the pick"] += 1
            continue
        why["scenes with a pair"] += 1
        ids_o, pos = c["readers"][X.LOOKUP]["ids"]["org"], c["pos"]
        for t in sorted(rng.sample(partners, min(max_moves, len(partners)))):
            s_ctx = swap_lockers(it, x, t)
            ids_s, at = B.encode(tok, it, s_ctx, x)
            if at != [pos] or len(ids_s) != len(ids_o):
                why["the bridge is not one token at the same index in O and S"] += 1
                continue
            if ids_s[pos:] != ids_o[pos:]:
                why["O and S differ from the bridge on"] += 1
                continue
            out.append({"scene": c["scene"], "format": c["format"], "level": c["level"], "domain": c["domain"],
                        "order": c["order"], "bridge": x, "partner": t, "pos": pos, "context": it["context"],
                        "cf_context": s_ctx, "ids": {"org": ids_o, "alt": ids_s}})  # fmt: skip
    why["pairs"] = len(out)
    return out, why


def in_half(c: dict, split: dict, half: str) -> bool:
    """Whether the case's bridge item is in the given half ("fit" / "test") of its format's split."""
    return c["bridge"] in split["formats"][c["format"]][half]


def varied_plan(tok, set_name: str) -> tuple[list[dict], dict, dict]:
    """Per format, the varied scenes' split by bridge item, and half 1's pairs (tokenizer only): pairs, split (per
    format the two halves' items and cases), counts."""
    from scripts import tasks_v2 as T
    from scripts import x0b_generalize as B

    cases, built = B.build_cases(tok, set_name)
    per = {}
    for f in FORMATS:
        mine = [c for c in cases if c["format"] == f]
        halves = split_items([c["bridge"] for c in mine])
        per[f] = {**halves, "cases": {h: sum(c["bridge"] in set(v) for c in mine) for h, v in halves.items()}}
    split = {"seed": SPLIT_SEED, "by": "bridge item, per format", "set": set_name, "formats": per,
             "aligned_cases": built["cases"]}  # fmt: skip
    items = {it["scene"]: it for it in T.load(set_name) if it["word"] == X.LOOKUP}
    pairs, why = varied_pairs(tok, [c for c in cases if c["format"] in per and in_half(c, split, "fit")], items)
    counts = {"pairs_per_format": dict(collections.Counter(p["format"] for p in pairs)), "why": dict(why)}
    return pairs, split, counts


def fit_basis(x: np.ndarray, rank: int = RANK) -> tuple[np.ndarray, np.ndarray, list[float]]:
    """P_cf's fit: the top `rank` components of a centered PCA of the rows of x ([d, rank] orthonormal), the mean, and
    the variance explained per component."""
    assert x.shape[0] > rank, f"{x.shape[0]} pairs for a rank-{rank} basis"
    _, s, vt = np.linalg.svd(x - x.mean(0), full_matrices=False)
    return vt[:rank].T, x.mean(0), (s**2 / (s**2).sum()).tolist()


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
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "pairs": n,
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
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "rank": RANK,
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


def stage_varied(name: str, set_name: str = "x0b_v2") -> Path:
    """45d's fit (module docstring): split.json, pairs.jsonl, pcf_<format>.npz and a descriptive report (variance
    explained, the split-half noise ceiling by scene, cos² of the principal angles with U and between the formats)."""
    import torch

    from bridge_jspace.model import load_model
    from bridge_jspace.utils import git_state, progress
    from scripts import x0_massmean as MM

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "run": name, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "model": pins.model_pin(), "switches": switches(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "set": set_name,
         "formats": list(FORMATS), "rank": RANK, "max_moves": MAX_MOVES,
         "split": f"per format, the aligned varied scenes (x0b_generalize.build_cases) in two halves by bridge item, seed "
                  f"{SPLIT_SEED}: fit (these pairs) and test (the main test, x0b_generalize --pcf-from)",
         "pairs": "the bridge's locker statement trades places with another item's, both before the asked pick, "
                  "numbers kept; the bridge one token at the same index in O and S",
         "pca": "centered, per format, over the pairs' bridge-word differences S - O", "alf_from": R.STATES[target],
         "seeds": {"split": SPLIT_SEED, "pairs": SEED}, "design": "jobs/c3/batch45.yaml, 45d (fixed in advance)"}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    pairs, split, counts = varied_plan(model.tokenizer, set_name)
    (out / "split.json").write_text(json.dumps({**split, "pairs": counts}, indent=1) + "\n")
    X.write_jsonl(out / "pairs.jsonl", [{k: v for k, v in p.items() if k != "ids"} for p in pairs])
    halves = {f: v["cases"] for f, v in split["formats"].items()}
    print(json.dumps({"cases": halves, **counts}, indent=1), flush=True)

    def state(ids: list[int], pos: int):
        return model.run(torch.tensor([ids], device="cuda"), record=(layer,))[1][layer][pos].float().cpu()

    diffs, h_org = [], {}
    with torch.no_grad():
        for p in progress(pairs, f"S - O at layer {layer} (pair)"):
            if p["scene"] not in h_org:  # O is shared by the scene's pairs
                h_org[p["scene"]] = state(p["ids"]["org"], p["pos"])
            diffs.append((state(p["ids"]["alt"], p["pos"]) - h_org[p["scene"]]).double().numpy())
    x = np.stack(diffs)
    alf = MM.subspaces(R.STATES[target])[0]["Alf"]
    report: dict = {"run": name, "model": target, "layer": layer, "split": {"seed": split["seed"], "cases": halves},
                    "counts": counts, "random_mean_cos2": RANK / x.shape[1], "alf_rank": int(alf.shape[1]), "formats": {}}  # fmt: skip
    bases = {}
    for f in FORMATS:
        idx = [i for i, p in enumerate(pairs) if p["format"] == f]
        p_f, mean, var = fit_basis(x[idx])
        bases[f] = p_f
        np.savez_compressed(out / f"pcf_{f}.npz", P=p_f.astype(np.float32), mean=mean.astype(np.float32),
                            var=np.array(var))  # fmt: skip
        cos2 = principal_cos2(p_f, alf)
        report["formats"][f] = {"pairs": len(idx), "scenes": len({pairs[i]["scene"] for i in idx}),
                                "bridge_items": len({pairs[i]["bridge"] for i in idx}),
                                "variance_explained": var[:SHOW], "variance_explained_cum": np.cumsum(var[:SHOW]).tolist(),
                                "split_half": split_half(x[idx], [pairs[i]["scene"] for i in idx]),
                                "cos2_with_alf": cos2, "mean_cos2_with_alf": float(np.mean(cos2))}  # fmt: skip
    report["between_formats"] = {f"{a}/{b}": float(np.mean(principal_cos2(bases[a], bases[b])))
                                 for i, a in enumerate(FORMATS) for b in FORMATS[i + 1 :]}  # fmt: skip
    (out / "report.json").write_text(json.dumps(report, indent=1) + "\n")
    lines = [f"# 45d's fit: a label-free basis per format in the varied scenes ({name})", "",
             f"Model {target}, layer {layer}; set {set_name}, half 1 of the bridge items (seed {SPLIT_SEED}); pairs: the "
             f"bridge's locker statement trades places with another item's, both before the asked pick, numbers kept; "
             f"PCA centered, rank {RANK}. Descriptive; the test is x0b_generalize --pcf-from. UNVERIFIED.", "",
             "| format | pairs | scenes | bridge items | variance explained 1-4 (cum.) | split-half mean cos² | "
             f"mean cos² with U (random {RANK / x.shape[1]:.4f}) |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for f, r in report["formats"].items():
        lines.append(f"| {f} | {r['pairs']} | {r['scenes']} | {r['bridge_items']} | "
                     f"{r['variance_explained_cum'][RANK - 1]:.3f} | {r['split_half']['mean_cos2']:.3f} | "
                     f"{r['mean_cos2_with_alf']:.3f} |")  # fmt: skip
    lines += ["", "Mean cos² between the formats' bases: "
              + ", ".join(f"{k} {v:.3f}" for k, v in report["between_formats"].items()) + "."]  # fmt: skip
    (out / "report.md").write_text("\n".join(lines) + "\n")
    print("wrote", out, flush=True)
    return out


def show_pair(p: dict) -> str:
    """O and S of one pair, the bridge's and the partner's locker statements as they differ (for the plan)."""
    i = next(k for k, (a, b) in enumerate(zip(p["context"], p["cf_context"], strict=True)) if a != b)
    j = len(p["context"]) - next(
        k for k, (a, b) in enumerate(zip(p["context"][::-1], p["cf_context"][::-1], strict=True)) if a != b
    )
    return f"[{p['format']}] {p['bridge']} <-> {p['partner']} at token {p['pos']}\n  O: ...{p['context'][i:j]}...\n  S: ...{p['cf_context'][i:j]}..."


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["plan", "run", "natural", "varied-plan", "varied"])
    ap.add_argument("--name")
    ap.add_argument("--n", type=int, default=N_PAIRS)
    ap.add_argument("--pcf", help="natural: the simple-scene P_cf run (results/x7_pcf/<run>) to compare with")
    ap.add_argument("--moves", default=None, metavar="J-K",
                    help="plan / run: only pairs whose bridge locker moves between these slots (45c: 1-2), rank 2, off U")  # fmt: skip
    ap.add_argument("--set", default="x0b_v2", help="varied: the tasks_v2 set of the varied scenes")
    a = ap.parse_args()
    moves = frozenset(int(v) for v in a.moves.split("-")) if a.moves else None
    if a.stage == "natural":
        stage_natural(a.name, a.pcf)
        return
    if a.stage == "varied":
        stage_varied(a.name, a.set)
        return
    if a.stage == "varied-plan":
        from scripts import statement_positions as SP

        made, split, counts = varied_plan(SP.load_tokenizer(), a.set)
        halves = {f: {"items": {h: len(v[h]) for h in ("fit", "test")}, "cases": v["cases"]}
                  for f, v in split["formats"].items()}  # fmt: skip
        print(json.dumps({"halves": halves, **counts}, indent=1))
        rng = random.Random(0)
        for f in FORMATS:
            mine = [p for p in made if p["format"] == f]
            for p in rng.sample(mine, min(2, len(mine))):
                print(show_pair(p))
        return
    if a.stage == "plan":
        from scripts import statement_positions as SP

        cases, dropped = pairs(SP.load_tokenizer(), a.n, moves=moves)
        print(len(cases), "pairs;", dict(dropped), cases[0]["context"], "|", cases[0]["cf_context"], sep="\n")
    else:
        stage_run(a.name, a.n, moves)


if __name__ == "__main__":
    main()
