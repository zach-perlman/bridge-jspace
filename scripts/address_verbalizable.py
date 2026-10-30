"""address_verbalizable: can the J++ lens verbalize the address (the locker-slot pointer)? (POST HOC; Dan 30 Oct; CPU; descriptive + a pre-set rule.)

(a) the address-swap directions mu_k - mu_j x8_write adds (mu = the pointer class means of the model's probe states, x0_massmean.pointer_means,
    at the model's fixed layer), for every ordered slot pair (j, k), decomposed over the model's J++ letter dictionary with the same signed
    25-atom OMP as the depth view (x52_atoms.omp_atoms; dictionary = x52_atoms.cpu_dictionary's arithmetic: unit rows of (g W_U[t]) J_L).
(b) optional (--deltas NPZ): the real change's component inside the pointer directions (U U^T Delta, U = Alf, the subspace no_alf removes) for 30
    random C2 lookup scenes (seed 29), computed on a GPU box (scripts/address_verbalizable_delta.py), decomposed the same way. A digit / cardinal
    atom equal to a locker digit of the scene is "ambiguous" and counted separately.
Also per model: the share of the pointer subspace's energy the 25-atom J++ part captures (each unit basis direction of Alf, and the six mu_k - mu_j).

Position classes (a token is matched whole after stripping edge punctuation and spaces, NFKC, case-folded; letter tokens only, so lone digits
are not in the dictionary): ordinals of the slot (0-based and 1-based: values {k, k+1} for slot k, {j, j+1} for slot j) in eleven languages
(atoms_multilingual.ORDINAL, 1st/2nd/3rd, Roman II / III), cardinals of the slot index (same values; zero / one / two / three in eleven
languages), generic position words (first, last, middle, next, previous, before, after, former, latter, in eleven languages).

Controls: the base rate (share of dictionary atoms in each class); 100 random Gaussian vectors in the same space, same OMP (the 95th
percentile of the position-atom energy share and of the sign-correct-ordinal rate over the six slot-pair labels); a label shuffle: each
mu_k - mu_j scored against each of the five wrong pairs.

Pre-set rule (written to the manifest before the run): "verbalizable" only if, on at least 3 of 5 models, (1) the position atoms' energy share in (a)
(mean over the six ordered pairs, each vector scored against its own pair) exceeds the random 95th percentile, and (2) a sign-correct ordinal (the
pair's k with a + coefficient, or its j with a -; an ordinal whose value belongs to both slots is not counted) appears in the 25 atoms on most slot
pairs (>= 4 of 6) and above the shuffle rate. Otherwise: "not verbalizable by the J++ lens at this layer; consistent with the claim".

uv run python scripts/address_verbalizable.py [--deltas results/address_verbalizable_delta/<run>/deltas.npz --deltas-model muse-glimmer-30b]
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

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace import pins  # noqa: E402
from scripts import atoms_multilingual as M  # noqa: E402
from scripts import x0_massmean as MM  # noqa: E402
from scripts import x6_routes as R  # noqa: E402
from scripts import x52_atoms as A  # noqa: E402

EXP = "address_verbalizable"
MODELS = ("muse-glimmer-30b", "qwen3.5-9b", "qwen3.6-27b", "nemotron-3.5-lightning", "qwen3.5-122b-a10b")
N_RANDOM, SEED, K, N_SCENES = 100, 29, 25, 30
PAIRS = [(j, k) for j in range(3) for k in range(3) if j != k]  # ordered: the write is mu_k - mu_j
ROUTES = {"qwen3.5-9b": "qwen35_9b_x6_routes", "qwen3.6-27b": "x6_routes_27b", "muse-glimmer-30b": "muse30b_x6_routes",
          "nemotron-3.5-lightning": "nem35l_x52_routes", "qwen3.5-122b-a10b": "qwen35_122b_x6_routes_g75"}  # fmt: skip
ZERO = ["zero", "零", "ゼロ", "영", "ноль", "нуль", "null", "zéro", "cero", "zero", "zero"]
ZEROTH = ["zeroth", "第零"]
GENERIC = {  # generic position words, eleven languages (English first)
    "English": "first last middle next previous before after former latter",
    "Chinese": "首先 最后 中间 下一个 上一个 之前 之后 以前 以后 前者 后者",
    "Japanese": "最初 最後 中間 次 前 後 以前 以後 前者 後者",
    "Korean": "처음 마지막 중간 다음 이전 전 후 이후",
    "Russian": "последний средний следующий предыдущий перед после бывший",
    "Ukrainian": "останній середній наступний попередній перед після колишній",
    "German": "zuerst zuletzt letzte mitte mittlere nächste vorherige vorher vor nach nachher frühere ehemalige letztere",
    "French": "dernier dernière milieu suivant précédent avant après ancien",
    "Spanish": "último medio siguiente anterior antes después antiguo",
    "Portuguese": "último meio próximo anterior antes depois antigo",
    "Italian": "ultimo mezzo prossimo precedente prima dopo",
}  # fmt: skip


def lexicon() -> dict[str, dict]:
    """folded form -> {'ordinal': {values}, 'cardinal': {values}, 'generic': bool}, values 0-3."""
    lex: dict[str, dict] = collections.defaultdict(lambda: {"ordinal": set(), "cardinal": set(), "generic": False})
    for form, readings in M.LEXICON.items():
        for v, _lang, kind in readings:
            if v <= 3:
                key = "ordinal" if kind in ("ordinal", "roman") else "cardinal"
                lex[form][key].add(v)  # Roman forms stay in capitals in the lexicon
    for f in ZERO:
        lex[M.normalise(f).casefold()]["cardinal"].add(0)
    for f in ZEROTH:
        lex[M.normalise(f).casefold()]["ordinal"].add(0)
    for words in GENERIC.values():
        for w in words.split():
            lex[M.normalise(w).casefold()]["generic"] = True
    # a lone "I" is no ordinal (a letter / the pronoun): atoms_multilingual's rule keeps Roman numerals of two letters or more
    lex.pop("I", None)
    return {k: {**v} for k, v in lex.items()}


LEX = lexicon()


def info(token: str) -> dict | None:
    s = M.normalise(token)
    return LEX.get(s) or LEX.get(s.casefold())


def classes_of(decoded: list[str], ids: list[int]) -> dict[int, dict]:
    out = {}
    for t in ids:
        i = info(decoded[t])
        if i and (i["ordinal"] or i["cardinal"] or i["generic"]):
            out[t] = i
    return out


def relevant(i: dict, j: int, k: int) -> tuple[bool, str]:
    """(is it a position atom of the pair (j -> k), its side: 'k' / 'j' / 'both' / 'none' for the ordinals)."""
    kv, jv = {k, k + 1}, {j, j + 1}
    pos = bool(i["generic"] or i["ordinal"] & (kv | jv) or i["cardinal"] & (kv | jv))
    side = "none"
    if i["ordinal"]:
        in_k, in_j = bool(i["ordinal"] & kv), bool(i["ordinal"] & jv)
        side = "both" if in_k and in_j else "k" if in_k else "j" if in_j else "none"
    return pos, side


def score(chosen, coefs, gains, cls: dict[int, dict], j: int, k: int, exclude: set[int] | None = None) -> dict:
    """One vector's 25 atoms scored against the pair (j, k): the position atoms' energy share, the sign-correct ordinal, the atoms."""
    share, correct, amb_share, atoms = 0.0, False, 0.0, []
    for r in range(len(chosen)):
        t = int(chosen[r])
        i = cls.get(t)
        pos, side = relevant(i, j, k) if i else (False, "none")
        sign = "+" if coefs[r] > 0 else "-"
        ambiguous = bool(
            i
            and exclude
            and pos
            and i["cardinal"]
            and not i["ordinal"]
            and not i["generic"]
            and (i["cardinal"] & exclude)
        )
        if pos and not ambiguous:
            share += float(gains[r])
        if ambiguous:
            amb_share += float(gains[r])
        if side in ("k", "j") and not ambiguous and ((side == "k" and sign == "+") or (side == "j" and sign == "-")):
            correct = True
        atoms.append(
            {"rank": r + 1, "token_id": t, "sign": sign, "energy": round(float(gains[r]), 5), "pos": pos, "side": side}
        )
    return {"position_share": share, "ambiguous_share": amb_share, "sign_correct_ordinal": correct, "atoms": atoms}


def build_dictionary(target: str, layer: int):
    import torch
    from safetensors.torch import load_file

    tok = A.tokenizer_of(target)
    head = load_file(str(A.CACHE / target / "head.safetensors"))
    w_u, g = head["lm_head.weight"], head["norm.weight"].float()
    gain = 1.0 + g if pins.TARGETS[target]["norm_gain"] == "one_plus_weight" else g
    src = pins.TARGETS[target]["lenses"]["jpp"]
    path = REPO / src[1] if src[0] == "local" else A.lens_path(target)
    blob = torch.load(path, map_location="cpu", weights_only=True, mmap=True)
    assert layer in blob["source_layers"], (target, layer)
    jl = blob["J"][layer].to(torch.float32)
    letters, decoded = A.letter_ids(tok, w_u.shape[0])
    lt = torch.tensor(letters)
    dic = torch.empty(len(letters), w_u.shape[1])
    with torch.no_grad():
        for s in range(0, len(letters), 16384):
            rows = (w_u[lt[s : s + 16384]].float() * gain) @ jl
            dic[s : s + 16384] = torch.nn.functional.normalize(rows, dim=-1)
    return lt, dic, decoded, tok


def wilson_upper(k: int, n: int, z: float = 1.96) -> float:
    p = k / n
    d = 1 + z * z / n
    return min(1.0, (p + z * z / (2 * n) + z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d)


def run_model(target: str, deltas: dict | None) -> dict:
    import torch

    states = R.STATES[target]
    layer = int(json.loads((REPO / "results" / "x0_probe" / states / "manifest.json").read_text())["layer"])
    mu = {k: np.asarray(v, dtype=np.float64) for k, v in MM.pointer_means(states).items()}
    alf = MM.subspaces(states)[0]["Alf"]
    t0 = time.time()
    letters, dic, decoded, _tok = build_dictionary(target, layer)
    print(f"{target}: dictionary {tuple(dic.shape)} at L{layer} in {time.time() - t0:.0f}s", flush=True)
    d = dic.shape[1]
    assert mu[0].shape[0] == d == alf.shape[0], (mu[0].shape, d, alf.shape)
    cls = classes_of(decoded, letters.tolist())
    base = {"dictionary_tokens": len(letters), "ordinal_tokens": sum(1 for v in cls.values() if v["ordinal"]),
            "cardinal_tokens": sum(1 for v in cls.values() if v["cardinal"]), "generic_tokens": sum(1 for v in cls.values() if v["generic"]),
            "position_tokens": len(cls)}  # fmt: skip
    base["base_rate_any_position_class"] = round(len(cls) / len(letters), 6)
    # the vectors: 6 write directions, 2 Alf basis vectors (unit), N_RANDOM random with the writes' median norm
    writes = {f"{j}->{k}": mu[k] - mu[j] for j, k in PAIRS}
    norm = float(np.median([np.linalg.norm(v) for v in writes.values()]))
    rng = np.random.default_rng(SEED)
    rand = rng.standard_normal((N_RANDOM, d))
    rand *= norm / np.linalg.norm(rand, axis=1, keepdims=True)
    vecs = np.concatenate([np.stack(list(writes.values())), alf.T, rand]).astype(np.float32)
    extra = []
    if deltas is not None:
        extra = list(deltas["vec"])
        vecs = np.concatenate([vecs, np.stack(extra).astype(np.float32)])
    x = torch.from_numpy(vecs)
    chosen, coefs, gains, approx = A.omp_atoms(dic, x, K)
    letters_np = letters.numpy()
    chosen_ids = letters_np[chosen.numpy()]  # token ids [m, K]
    captured = ((approx.double().norm(dim=-1) ** 2) / (x.double().norm(dim=-1) ** 2)).numpy()
    nw, na = len(PAIRS), alf.shape[1]
    out: dict = {
        "layer": layer,
        "d": d,
        "base_rate": base,
        "norm_median_write": norm,
        "alf_rank": na,
        "seconds": round(time.time() - t0),
    }
    out["overlap"] = {"alf_basis_directions_captured": [round(float(c), 4) for c in captured[nw : nw + na]],
                      "alf_mean_captured": round(float(captured[nw : nw + na].mean()), 4),
                      "writes_captured": {p: round(float(c), 4) for p, c in zip(writes, captured[:nw], strict=True)},
                      "random_mean_captured": round(float(captured[nw + na : nw + na + N_RANDOM].mean()), 4)}  # fmt: skip

    def sc(row: int, j: int, k: int, excl=None) -> dict:
        return score(chosen_ids[row], coefs[row].numpy(), gains[row].numpy(), cls, j, k, excl)

    # (a) own pair; shuffle = the five wrong pairs; random = every pair label
    own, shuffle, per_pair = [], [], {}
    for row, (j, k) in enumerate(PAIRS):
        s = sc(row, j, k)
        own.append(s)
        wrong = [sc(row, jj, kk) for (jj, kk) in PAIRS if (jj, kk) != (j, k)]
        shuffle += wrong
        per_pair[f"{j}->{k}"] = {"position_share": round(s["position_share"], 5), "sign_correct_ordinal": s["sign_correct_ordinal"],
                                 "shuffle_position_share_mean": round(float(np.mean([w["position_share"] for w in wrong])), 5),
                                 "shuffle_sign_correct_rate": round(float(np.mean([w["sign_correct_ordinal"] for w in wrong])), 3),
                                 "top10": [{**a, "token": decoded[a["token_id"]], "class": {k_: (sorted(v) if isinstance(v, set) else v) for k_, v in (cls.get(a["token_id"]) or {}).items() if v}}
                                           for a in s["atoms"][:10]]}  # fmt: skip
    r0 = nw + na
    rand_share, rand_rate = [], []
    for r in range(N_RANDOM):
        ss = [sc(r0 + r, j, k) for (j, k) in PAIRS]
        rand_share.append(float(np.mean([s["position_share"] for s in ss])))
        rand_rate.append(float(np.mean([s["sign_correct_ordinal"] for s in ss])))
    a_share = float(np.mean([s["position_share"] for s in own]))
    a_rate = float(np.mean([s["sign_correct_ordinal"] for s in own]))
    sh_rate = float(np.mean([s["sign_correct_ordinal"] for s in shuffle]))
    p95_share, p95_rate = float(np.percentile(rand_share, 95)), float(np.percentile(rand_rate, 95))
    out["a"] = {"per_pair": per_pair, "position_share_mean": round(a_share, 5), "random_position_share_mean": round(float(np.mean(rand_share)), 5),
                "random_position_share_p95": round(p95_share, 5), "sign_correct_pairs": round(a_rate * nw), "sign_correct_rate": round(a_rate, 3),
                "shuffle_sign_correct_rate": round(sh_rate, 3), "random_sign_correct_rate_mean": round(float(np.mean(rand_rate)), 3),
                "random_sign_correct_rate_p95": round(p95_rate, 3),
                "shuffle_position_share_mean": round(float(np.mean([s["position_share"] for s in shuffle])), 5)}  # fmt: skip
    out["rule"] = {
        "share_above_random_p95": bool(a_share > p95_share),
        "sign_correct_on_most_pairs_above_shuffle": bool(round(a_rate * nw) >= 4 and a_rate > sh_rate),
    }
    out["rule"]["both"] = (
        out["rule"]["share_above_random_p95"] and out["rule"]["sign_correct_on_most_pairs_above_shuffle"]
    )
    # (b)
    if deltas is not None:
        rb = []
        rows = range(r0 + N_RANDOM, r0 + N_RANDOM + len(extra))
        for row, meta in zip(rows, deltas["meta"], strict=True):
            lockers = set(
                meta["locker_values"]
            )  # the digits of the scene's lockers: a cardinal atom with such a value is ambiguous
            s = sc(row, meta["j"], meta["k"], lockers)
            rb.append({"scene": meta["scene"], "j": meta["j"], "k": meta["k"], "position_share": round(s["position_share"], 5), "ambiguous_share": round(s["ambiguous_share"], 5),
                       "sign_correct_ordinal": s["sign_correct_ordinal"], "captured": round(float(captured[row]), 4),
                       "top10": [{**a, "token": decoded[a["token_id"]]} for a in s["atoms"][:10]]})  # fmt: skip
        out["b"] = {"n": len(rb), "position_share_mean": round(float(np.mean([r["position_share"] for r in rb])), 5),
                    "ambiguous_share_mean": round(float(np.mean([r["ambiguous_share"] for r in rb])), 5),
                    "sign_correct_scenes": int(sum(r["sign_correct_ordinal"] for r in rb)), "captured_mean": round(float(np.mean([r["captured"] for r in rb])), 4),
                    "items": rb, "three_random_items": random.Random(SEED).sample(rb, min(3, len(rb)))}  # fmt: skip
    del dic
    return out


def render(res: dict) -> str:
    def label(a: dict) -> str:
        c = a.get("class") or {}
        kinds = [k for k in ("ordinal", "cardinal", "generic") if c.get(k)]
        return "/".join(kinds) if kinds else "-"

    L = [
        "# Is the address verbalizable by the J++ lens? (post hoc, CPU)\n",
        f"Verdict by the pre-set rule: **{res['verdict']}** (models meeting both conditions: {res['models_meeting_both_conditions']} of {len(res['models'])})\n",
    ]
    for m, v in res["models"].items():
        a, o, r = v["a"], v["overlap"], v["rule"]
        L += [
            f"## {m} (L{v['layer']}, d = {v['d']})\n",
            f"Base rate: {v['base_rate']}\n",
            f"(a) position-atom energy share (mean over the six writes) {a['position_share_mean']} vs random 95th percentile {a['random_position_share_p95']} (random mean {a['random_position_share_mean']}, shuffle mean {a['shuffle_position_share_mean']}); "
            f"sign-correct ordinal on {a['sign_correct_pairs']} of 6 pairs (rate {a['sign_correct_rate']}) vs shuffle {a['shuffle_sign_correct_rate']}, random mean {a['random_sign_correct_rate_mean']} / 95th percentile {a['random_sign_correct_rate_p95']}; rule: {r}\n",
            f"Overlap: the 25-atom J++ part captures {o['alf_mean_captured']} of the pointer basis directions' energy ({o['alf_basis_directions_captured']}), the six writes {sorted(set(o['writes_captured'].values()))}, random vectors {o['random_mean_captured']}\n",
            "| pair (j->k) | position share | sign-correct ordinal | top-10 atoms (token sign energy class) |\n|---|---|---|---|",
        ]
        for pair, x in a["per_pair"].items():
            top = "; ".join(f"{t['token']!r} {t['sign']} {t['energy']:.4f} {label(t)}" for t in x["top10"])
            L.append(f"| {pair} | {x['position_share']} | {x['sign_correct_ordinal']} | {top} |")
        if "b" in v:
            b = v["b"]
            L += [
                "",
                f"(b) 30 random C2 scenes (seed 29): mean position share {b['position_share_mean']}, ambiguous (cardinal equal to a locker digit) {b['ambiguous_share_mean']}, sign-correct ordinal in {b['sign_correct_scenes']} of {b['n']} scenes, "
                f"the pointer component captured {b['captured_mean']}. Three random scenes (seed 29), raw:\n",
            ]
            for it in b["three_random_items"]:
                L.append(
                    f"- {it['scene']} j={it['j']} k={it['k']} share {it['position_share']} sign-correct {it['sign_correct_ordinal']}: "
                    + "; ".join(f"{t['token']!r} {t['sign']} {t['energy']:.4f}" for t in it["top10"])
                )
        L.append("")
    return "\n".join(L) + "\n"


def main() -> Path:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=",".join(MODELS))
    ap.add_argument("--deltas", type=Path)
    ap.add_argument("--deltas-model")
    a = ap.parse_args()
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / EXP / stamp
    out.mkdir(parents=True, exist_ok=False)
    manifest = {
        "exp": EXP,
        "written_utc": stamp,
        "script": "scripts/address_verbalizable.py",
        "post_hoc": True,
        "cpu": True,
        "models": a.models.split(","),
        "docstring": __doc__,
        "n_random": N_RANDOM,
        "seed": SEED,
        "k_atoms": K,
        "rule": "'verbalizable' only if on >= 3 of 5 models (1) the position atoms' energy share in (a) (mean over the six ordered pairs) exceeds the random 95th percentile and (2) a sign-correct ordinal appears in the 25 atoms on >= 4 of 6 slot pairs and above the shuffle rate; otherwise 'not verbalizable by the J++ lens at this layer; consistent with the claim'",
        "deltas": str(a.deltas) if a.deltas else None,
        "deltas_model": a.deltas_model,
        "git": __import__("subprocess")
        .run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True)
        .stdout.strip(),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))  # before the numbers
    deltas = None
    if a.deltas:
        z = np.load(a.deltas, allow_pickle=True)
        deltas = {"vec": z["vec"], "meta": json.loads(str(z["meta"]))}
    res: dict = {"models": {}}
    for target in a.models.split(","):
        res["models"][target] = run_model(target, deltas if target == a.deltas_model else None)
        (out / "tables.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float))
    n_both = sum(m["rule"]["both"] for m in res["models"].values())
    res["models_meeting_both_conditions"] = n_both
    res["verdict"] = (
        "verbalizable by the J++ lens"
        if n_both >= 3
        else "not verbalizable by the J++ lens at this layer; consistent with the claim"
    )
    (out / "tables.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float))
    (out / "tables.md").write_text(render(res))
    print(json.dumps({"verdict": res["verdict"], "n_both": n_both}), flush=True)
    return out


if __name__ == "__main__":
    main()
