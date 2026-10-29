"""x47_verbal (batch 47, test 47.0; jobs/c3/batch47.yaml; Neel's question; descriptive, not sealed): is the pointer
verbalizable? Read through the J++ lens, does a pointer write say anything, and can the lens's atoms express it?

Inputs, per model at the layer fixed in advance (9B L12, 27B L32, Muse L26): the pointer means mu_k and U (x0_massmean
pointer_means / subspaces' Alf, fit on the fresh scenes x6_routes.STATES, never refit); the identity directions
mu_alt - mu_org (x0_massmean.entity_means, the item pair of each routes scene, as x6_routes --identity); the routes
test's original prompts O (x6_routes' generator, C2 scenes, the locker sentences first): the first N_ITEMS scenes of
x8_write's run (its eligible items, in its order, rebuilt from the generator and checked against its rows), and the
real bridge-word state h at the layer (one forward of O as x8_write reads it). The write is x8_write's: h + s (mu_k -
mu_j) at s = 2, j the bridge item's locker slot, both k != j. Null: N_RAND Gaussian directions (seed RAND_SEED), each
scaled to the norm of the write it stands in for; the identity direction at the same norm is the positive comparison.

(a) read-through: the lens readout (x0's path: JLens.readout = the final norm and lm_head of J_L h, every token) of h
    alone, of h + the write, of h + the identity direction, of h + each random vector. Per readout the rank (1 = top,
    over the whole vocabulary) of the best token of an ordinal set (ORDINAL, every single-token spelling with and
    without a leading space and capital) and of the digits, the rank of the written locker's digit, of the new item's
    name, and the top 20 tokens. Also, descriptive, the readout of each direction alone (U +/-, the writes, identity,
    random): what the lens says about the direction itself.
(b) reconstruction: the project's nonneg OMP (bridge_jspace.omp.nonneg_omp) over the lens's unit atoms at the layer,
    k = 25 and 100, every non-special token (unrestricted) and the letter tokens (the main test's restriction), on each
    U direction (both signs), each write mu_k - mu_j (k, j in slots 0-2), the identity directions (the first ID_MAX
    distinct item pairs) and the random null: ||P x||^2 / ||x||^2 and the atoms picked (tokens).
(c) blindness: KL(lens readout of h || of h + the write) per (item, write), against the random vectors of the same
    norm and the identity direction of the same norm; beside it, x8_write's lookup answers on the same writes.

Summary statistics (fixed here, before any run): for a per-case quantity (a case = one item and one write), the
statistic is its median over cases; the null distribution is the same median computed with random vector i in place of
the write, i = 1..N_RAND; ranks are "beyond the null" below the null's 5th percentile, KL above its 95th. Case-level
shares (each case against its own N_RAND random vectors) with cluster-bootstrap intervals over bridge items (10,000,
seed 0) are reported beside. Reconstruction: the mean share over the writes and over U +/- (the pointer: the larger of
the two) against the random null's mean share. Readings (the spec's, per model): "not verbalizable" = reconstruction at
k = 25 (unrestricted) <= 2x the null, the ordinal statistic not (<= 20 and beyond the null), and the KL statistic within
the null's 95th percentile; "partly verbalizable" = an ordinal or digit statistic <= 20 and beyond the null, or
reconstruction >= 3x the null; else "neither". Over the models: "not verbalizable" if all three are, "partly
verbalizable" if any is.

uv run python scripts/x47_verbal.py plan                     # CPU, the target's tokenizer (BJ_TARGET): items and tokens
BJ_TARGET=qwen3.5-9b uv run python scripts/x47_verbal.py run --name qwen35_9b_x47_verbal       # GPU
uv run python scripts/x47_verbal.py summary --runs qwen35_9b_x47_verbal x47_verbal_27b muse30_x47_verbal
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x6_routes as R
from scripts import x8_write as W

EXP = "x47_verbal"
RESULTS = pins.RESULTS_DIR / EXP
S_WRITE = 2.0  # the write's dose: h + 2 (mu_k - mu_j), x8_write's s = 2
N_ITEMS, N_RAND, RAND_SEED = 100, 200, 4701
KS = (25, 100)
TOP = 20
ID_MAX = 50  # identity directions reconstructed (distinct item pairs, in item order)
N_ATOMS_SHOWN = 15
ATOMS_LISTED = 5  # in verbal.md (all N_ATOMS_SHOWN in omp.jsonl)
EXAMPLES, EXAMPLES_SEED = 10, 0
ORDINAL = ("first", "second", "third", "1", "2", "3", "next", "last", "earlier", "later", "before", "after", "one",
           "two", "three")  # fmt: skip
X8_RUN = {
    "qwen3.5-9b": "qwen35_9b_x8_write",
    "qwen3.6-27b": "x8_write_27b",
    "muse-glimmer-30b": "muse30b_x8_write",
    "nemotron-3.5-lightning": "nem35l_x52_write",
}  # fmt: skip (Lightning: batch 52 C coverage)
RUN_NAME = {"qwen3.5-9b": "qwen35_9b_x47_verbal", "qwen3.6-27b": "x47_verbal_27b",
            "muse-glimmer-30b": "muse30_x47_verbal", "nemotron-3.5-lightning": "nem35l_x52_verbal"}  # fmt: skip
NAME = {"qwen3.5-9b": "Qwen3.5-9B", "qwen3.6-27b": "Qwen3.6-27B", "muse-glimmer-30b": "Muse Glimmer 30B",
        "nemotron-3.5-lightning": "Nemotron 3.5 Lightning"}  # fmt: skip
RECON_RATIO_NOT, RECON_RATIO_PARTLY, TOP_RANK = 2.0, 3.0, 20
LO_PCT, HI_PCT = 5.0, 95.0
# the sanity swap (J++ and U removed together; x6_routes --bothoff, C0): figures/story/data.csv, fig10
DATA_CSV = pins.REPO_ROOT / "figures" / "story" / "data.csv"
SANITY = "sanity swap, lookups still switching without J++ part + pointer: "


# ---- the items and the tokens (CPU) -------------------------------------------------------------------------------


def x8_items(target: str, n: int) -> tuple[list[str], dict[tuple[str, int | None], dict]]:
    """The first n scenes of x8_write's run in its order, and its lookup rows at s = 2 by (scene, k)."""
    rows = X.read_jsonl(W.RESULTS / X8_RUN[target] / "outcomes.jsonl")
    scenes = list(dict.fromkeys(r["scene"] for r in rows))[:n]
    lk = {(r["scene"], r["k"]): r for r in rows
          if r["reader"] == X.LOOKUP and r["kind"] == "write" and r["s"] == S_WRITE}  # fmt: skip
    none = {r["scene"]: r for r in rows if r["reader"] == X.LOOKUP and r["kind"] == "none"}
    for s in scenes:
        lk[(s, None)] = none[s]
    return scenes, lk


def routes_items(tok, target: str, n: int) -> tuple[list[dict], dict[tuple[str, int | None], dict]]:
    """x8_write's first n items rebuilt from x6_routes' generator (C2, O prompts), each with its locker slots, the
    bridge's slot j, the digit token per slot and the new item's name token; asserts they are x8's (entity and j)."""
    from scripts import suite_v1 as S

    scenes, x8 = x8_items(target, n)
    cases, _ = R.scenes(tok, R.N_GEN)
    by = {c["scene"]: c for c in cases if c["condition"] == "C2"}
    out = []
    for s in scenes:
        c = dict(by[s])
        sl = W.slots_of(c["context"])
        j = [x for x, _ in sl].index(c["bridge"])
        assert x8[(s, None)]["entity"] == c["bridge"], f"{s}: not x8_write's item (entity)"
        assert x8[(s, None)]["j"] == j, f"{s}: not x8_write's item (slot)"
        c["j"] = j
        c["slot_digits"] = [d for _, d in sl]
        c["digit_tokens"] = [S.answer_token(tok, str(d), "digit") for _, d in sl]
        c["alt_name_token"] = S.ids(tok, " " + c["cf_bridge"])[0]
        out.append(c)
    return out, x8


def token_sets(tok) -> dict[str, dict[int, str]]:
    """Token id -> spelling for the ordinal set (every single-token spelling: as is, with a leading space, capitalized,
    both) and the digits (0-9, with and without a leading space)."""
    from scripts import suite_v1 as S

    def single(words) -> dict[int, str]:
        out: dict[int, str] = {}
        for w in words:
            for v in dict.fromkeys((w, " " + w, w.capitalize(), " " + w.capitalize())):
                t = S.ids(tok, v)
                if len(t) == 1:
                    out.setdefault(t[0], v)
        return out

    return {"ordinal": single(ORDINAL), "digits": single([str(d) for d in range(10)])}


# ---- per readout (torch; CPU in the tests) --------------------------------------------------------------------------


def ranks(logits, ids):
    """Rank (1 = top) of each token in ids [T] in each row of logits [B, V]: 1 + the number of tokens with a strictly
    higher logit. [B, T] long."""
    import torch

    srt = logits.sort(dim=-1).values  # ascending
    val = logits[:, ids].contiguous()
    higher = logits.shape[-1] - torch.searchsorted(srt, val, right=True)
    return higher + 1


def readout_stats(logits, logp_base, sets: dict[str, Any], target_tok, alt_tok, top: int = TOP) -> dict[str, Any]:
    """Per row of lens logits [B, V]: KL(base || row) (logp_base [V]; None: no KL), the best rank and its token in the
    ordinal set and in the digits (sets: name -> LongTensor of ids), the rank of the written locker's digit and of the
    new item's name (None: skipped), and the top `top` ids."""
    import torch

    out: dict[str, Any] = {}
    if logp_base is not None:
        logp = torch.log_softmax(logits.float(), dim=-1)
        out["kl"] = (logp_base.exp() * (logp_base - logp)).sum(-1)
    for name, ids in sets.items():
        r = ranks(logits, ids)
        best = r.min(dim=-1)
        out[f"best_{name}"], out[f"best_{name}_tok"] = best.values, ids[best.indices]
    if target_tok is not None:
        out["target_digit"] = ranks(logits, torch.tensor([target_tok], device=logits.device))[:, 0]
    if alt_tok is not None:
        out["alt_name"] = ranks(logits, torch.tensor([alt_tok], device=logits.device))[:, 0]
    out["top"] = logits.topk(top, dim=-1).indices
    return out


# ---- summary statistics (CPU) ---------------------------------------------------------------------------------------


def against_null(
    pointer: np.ndarray, null: np.ndarray, entities: list[str], lower_better: bool, n_boot: int = X.N_BOOT
) -> dict:
    """pointer [n_cases], null [n_rand, n_cases]: the median over cases for the pointer and its null distribution (the
    same median with each random vector), the null's 5th (ranks) or 95th (KL) percentile and whether the pointer is
    beyond it; per case, the pointer beyond its own case's percentile of the n_rand random values, the share of such
    cases with a cluster-bootstrap interval over entities."""
    pct = LO_PCT if lower_better else HI_PCT
    stat = float(np.median(pointer))
    null_stats = np.median(null, axis=1)
    cut = float(np.percentile(null_stats, pct))
    beyond = stat < cut if lower_better else stat > cut
    case_cut = np.percentile(null, pct, axis=0)
    case_beyond = (pointer < case_cut) if lower_better else (pointer > case_cut)
    share = X.resampled_rates({"b": case_beyond.astype(int).tolist()}, entities, n_boot)["b"]
    return {"median": stat, "null_median_of_medians": float(np.median(null_stats)), "null_pct": pct,
            "null_cut": cut, "beyond": bool(beyond),
            "case_share_beyond": [float(case_beyond.mean()), *X.interval(share)],
            "case_null_cut_median": float(np.median(case_cut))}  # fmt: skip


def recon_summary(rows: list[dict]) -> dict:
    """Per dictionary and k: the mean share of the writes, of U +/-, of the identity directions and of the random
    null (and the null's 95th percentile), the pointer's share (the larger of the writes' and U's) and its ratio to the
    null's mean."""
    out: dict = {}
    for d in sorted({r["dict"] for r in rows}):
        for k in sorted({r["k"] for r in rows}):
            mine = [r for r in rows if r["dict"] == d and r["k"] == k]
            by = {
                kind: [r["share"] for r in mine if r["kind"] == kind] for kind in ("write", "U", "identity", "random")
            }
            mean = {kind: float(np.mean(v)) if v else float("nan") for kind, v in by.items()}
            pointer = max(mean["write"], mean["U"])
            out[f"{d}|{k}"] = {**{f"{kind}_mean": v for kind, v in mean.items()},
                               "random_p95": float(np.percentile(by["random"], HI_PCT)) if by["random"] else float("nan"),
                               "pointer": pointer, "ratio": pointer / mean["random"] if mean["random"] > 0 else float("nan"),
                               "identity_ratio": mean["identity"] / mean["random"] if mean["random"] > 0 else float("nan"),
                               "n": {kind: len(v) for kind, v in by.items()}}  # fmt: skip
    return out


def model_reading(a_ord: dict, a_dig: dict, recon_ratio_k25: float, kl: dict) -> dict:
    """The spec's labels for one model from (a) the ordinal and digit statistics, (b) the unrestricted k = 25 ratio and
    (c) the KL statistic (against_null outputs)."""
    named = {n: c["beyond"] and c["median"] <= TOP_RANK for n, c in (("ordinal", a_ord), ("digits", a_dig))}
    not_verbal = recon_ratio_k25 <= RECON_RATIO_NOT and not named["ordinal"] and not kl["beyond"]
    partly = named["ordinal"] or named["digits"] or recon_ratio_k25 >= RECON_RATIO_PARTLY
    label = "partly verbalizable" if partly else "not verbalizable" if not_verbal else "neither"
    why = (f"ordinal median rank {a_ord['median']:.0f} (null 5th pct {a_ord['null_cut']:.0f}); digits "
           f"{a_dig['median']:.0f} (null {a_dig['null_cut']:.0f}); reconstruction at k = 25 {recon_ratio_k25:.2f}x the "
           f"null; KL median {kl['median']:.3g} (null 95th pct {kl['null_cut']:.3g})")  # fmt: skip
    return {"label": label, "named": named, "kl_beyond_null": kl["beyond"], "why": why}


def overall(labels: dict[str, str]) -> str:
    """Over the models: not verbalizable if all are; partly verbalizable if any is (named); else mixed."""
    if labels and all(v == "not verbalizable" for v in labels.values()):
        return "not verbalizable"
    partly = [m for m, v in labels.items() if v == "partly verbalizable"]
    if partly:
        return "partly verbalizable (" + ", ".join(partly) + ")"
    return "mixed (neither label on every model)" if labels else "not landed"


def sanity_swap() -> dict:
    """The lookups still switching in the sanity swap with J++ and U removed together, and with a random part of the
    same size, per model (figures/story/data.csv, fig10; x6_routes --bothoff)."""
    out: dict = {}
    for r in csv.DictReader(DATA_CSV.open()):
        if r["figure"] == "fig10" and r["quantity"].startswith(SANITY):
            arm = "part" if r["quantity"].endswith("the part") else "random"
            out.setdefault(r["model"], {})[arm] = [float(r["value"]), float(r["lo"]), float(r["hi"])]
            out[r["model"]]["source"] = r["source"]
    return out


# ---- the run (GPU) ------------------------------------------------------------------------------------------------


def stage_run(name: str, n_items: int = N_ITEMS, n_rand: int = N_RAND) -> Path:
    import torch

    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.omp import nonneg_omp
    from bridge_jspace.run_switches import switches
    from bridge_jspace.utils import git_state, progress
    from scripts import x0_massmean as MM

    pins.check_run_name(name)
    target = pins.model_pin()["target"]
    layer = X.PREDICTED[target]
    out = RESULTS / name
    out.mkdir(parents=True, exist_ok=False)
    m = {"exp": EXP, "test": "47.0 (jobs/c3/batch47.yaml)", "run": name, "descriptive": True, "sealed": False,
         "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "model": pins.model_pin(),
         "switches": switches(), "code": git_state(), "lens": X.lens_record(), "layer": layer, "s": S_WRITE,
         "n_items": n_items, "n_rand": n_rand, "ks": list(KS), "id_max": ID_MAX, "seeds": {"random": RAND_SEED,
         "scenes": R.SEED, "examples": EXAMPLES_SEED, "bootstrap": X.BOOT_SEED}, "mu_from": R.STATES[target],
         "items_from": f"results/x8_write/{X8_RUN[target]}", "ordinal": list(ORDINAL)}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    dev = model.device
    cases, x8 = routes_items(tok, target, n_items)
    sets_ = token_sets(tok)
    sets = {k: torch.tensor(sorted(v), device=dev) for k, v in sets_.items()}
    mu = {k: torch.tensor(v, dtype=torch.float32, device=dev) for k, v in MM.pointer_means(R.STATES[target]).items()}
    alf = torch.tensor(MM.subspaces(R.STATES[target])[0]["Alf"], dtype=torch.float32, device=dev)
    ent = {e: torch.tensor(v, dtype=torch.float32, device=dev) for e, v in MM.entity_means(R.STATES[target]).items()}
    lens = JLens(model, "jpp")
    d = alf.shape[0]
    rand = torch.nn.functional.normalize(
        torch.randn(n_rand, d, generator=torch.Generator().manual_seed(RAND_SEED)), dim=-1
    )
    rand = rand.to(dev)

    def unit_identity(c: dict):
        if c["bridge"] in ent and c["cf_bridge"] in ent:
            u = ent[c["cf_bridge"]] - ent[c["bridge"]]
            return u / u.norm()
        return None

    dec = model.decoded
    case_rows, base_rows, keys = [], [], []
    null = {k: [] for k in ("kl", "best_ordinal", "best_digits", "target_digit", "alt_name")}
    reads = []
    with torch.no_grad():
        for c in progress(cases, f"states and readouts at layer {layer} (item)"):
            ids = c["readers"][X.LOOKUP]["ids"]["org"] + c["space"]  # O as x8_write reads it (chat: the space appended)
            logits, rec = model.run(torch.tensor([ids], device=dev), record=(layer,))
            reads.append(int(logits.argmax()) == x8[(c["scene"], None)]["top"])
            h = rec[layer][c["pos"]].to(dev)
            base = lens.readout(h[None], layer)
            logp_base = torch.log_softmax(base[0].float(), dim=-1)
            st = readout_stats(base, None, sets, None, c["alt_name_token"])
            base_rows.append({"scene": c["scene"], "entity": c["bridge"], "arm": "base",
                              "best_ordinal": int(st["best_ordinal"][0]), "best_ordinal_tok": dec[int(st["best_ordinal_tok"][0])],
                              "best_digits": int(st["best_digits"][0]), "alt_name": int(st["alt_name"][0]),
                              "top": [dec[int(t)] for t in st["top"][0]]})  # fmt: skip
            u = unit_identity(c)
            for k in (x for x in W.SLOTS if x != c["j"]):
                w = S_WRITE * (mu[k] - mu[c["j"]])
                nrm = w.norm()
                vecs = [h + w] + ([h + nrm * u] if u is not None else []) + [h[None] + nrm * rand]
                stack = torch.cat([v if v.dim() == 2 else v[None] for v in vecs])
                st = readout_stats(
                    lens.readout(stack, layer), logp_base, sets, c["digit_tokens"][k], c["alt_name_token"]
                )
                arms = ["write"] + (["identity"] if u is not None else [])
                lk = x8[(c["scene"], k)]
                for i, arm in enumerate(arms):
                    case_rows.append({"scene": c["scene"], "entity": c["bridge"], "k": k, "j": c["j"], "arm": arm,
                                      "norm": round(float(nrm), 4), "kl": float(st["kl"][i]),
                                      **{f: int(st[f][i]) for f in ("best_ordinal", "best_digits", "target_digit", "alt_name")},
                                      "best_ordinal_tok": dec[int(st["best_ordinal_tok"][i])],
                                      "best_digits_tok": dec[int(st["best_digits_tok"][i])],
                                      "top": [dec[int(t)] for t in st["top"][i]],
                                      "x8_lookup_class": lk["class"], "x8_lookup_top": dec[lk["top"]]})  # fmt: skip
                r0 = len(arms)
                for f in null:
                    null[f].append(st[f][r0:].float().cpu().numpy())
                keys.append((c["scene"], k, c["bridge"]))
        X.write_jsonl(out / "readouts.jsonl", base_rows + case_rows)
        arrays: dict[str, Any] = {f: np.stack(v, axis=1) for f, v in null.items()}  # [n_rand, n_cases]
        arrays.update(scene=np.array([s for s, _, _ in keys]), k=np.array([k for _, k, _ in keys]),
                      entity=np.array([e for _, _, e in keys]))  # fmt: skip
        np.savez_compressed(out / "null.npz", **arrays)
        m["read_check"] = {"items": len(reads), "same_top_as_x8": int(sum(reads))}
        # the directions alone, and the vectors reconstructed
        vec: list[tuple[str, str, Any]] = []
        for i in range(alf.shape[1]):
            vec += [(f"U{i}+", "U", alf[:, i]), (f"U{i}-", "U", -alf[:, i])]
        for j in W.SLOTS:
            for k in W.SLOTS:
                if j != k:
                    vec.append((f"mu{k}-mu{j}", "write", mu[k] - mu[j]))
        pairs = list(dict.fromkeys((c["bridge"], c["cf_bridge"]) for c in cases if unit_identity(c) is not None))
        vec += [(f"id {a}->{b}", "identity", ent[b] - ent[a]) for a, b in pairs[:ID_MAX]]
        vec += [(f"random{i}", "random", rand[i]) for i in range(n_rand)]
        stack = torch.stack([v / v.norm() for *_, v in vec])
        dir_rows = []
        for s0 in range(0, len(vec), 64):
            st = readout_stats(lens.readout(stack[s0 : s0 + 64], layer), None, sets, None, None)
            for i in range(st["top"].shape[0]):
                name_, kind, _ = vec[s0 + i]
                dir_rows.append({"name": name_, "kind": kind, "best_ordinal": int(st["best_ordinal"][i]),
                                 "best_ordinal_tok": dec[int(st["best_ordinal_tok"][i])],
                                 "best_digits": int(st["best_digits"][i]), "best_digits_tok": dec[int(st["best_digits_tok"][i])],
                                 "top": [dec[int(t)] for t in st["top"][i]] if kind != "random" else None})  # fmt: skip
        X.write_jsonl(out / "direction.jsonl", dir_rows)
        every = torch.tensor([i for i in range(len(dec)) if i not in model.special_ids], device=dev)
        omp_rows = []
        for dname, tokens in (("letters", model.letter_token_ids().to(dev)), ("all", every)):
            dic = lens.vectors(layer, tokens)
            for name_, kind, v in progress(vec, f"nonneg OMP over {dname} atoms (vector)"):
                x = (v / v.norm()).to(dic.device)
                for k in KS:
                    idx, coefs = nonneg_omp(dic, x, k)
                    rec_ = coefs @ dic[idx] if len(idx) else torch.zeros_like(x)
                    row = {"name": name_, "kind": kind, "dict": dname, "k": k, "atoms": len(idx),
                           "share": float(rec_.norm() ** 2 / x.norm() ** 2)}  # fmt: skip
                    if kind != "random":
                        order = coefs.argsort(descending=True)[:N_ATOMS_SHOWN]
                        row["top_atoms"] = [[dec[int(tokens[idx[o]])], round(float(coefs[o]), 4)] for o in order]
                    omp_rows.append(row)
            del dic
            torch.cuda.empty_cache()
        X.write_jsonl(out / "omp.jsonl", omp_rows)
    (out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    examples(out, cases, base_rows, case_rows, tok)
    print("wrote", out, flush=True)
    return out


def examples(out: Path, cases: list[dict], base_rows: list[dict], case_rows: list[dict], tok) -> None:
    """The verify-pack view: EXAMPLES random items (seed EXAMPLES_SEED), the prompt O as the model reads it with the
    write position in ⟦...⟧, the slots' digits, and per write the lens's top tokens (h alone, h + the write, h + the
    identity direction), the ordinal rank, the KL, and x8_write's lookup answer under the same write."""
    decode = lambda ids: tok.decode([int(t) for t in ids], skip_special_tokens=False)  # noqa: E731
    base = {r["scene"]: r for r in base_rows}
    lines = [f"# Examples: {out.name}", "", f"{EXAMPLES} random items (seed {EXAMPLES_SEED}) of {len(cases)}. The write "
             f"h + {S_WRITE:g} (mu_k - mu_j) is added at ⟦...⟧; the lens reads the same position. UNVERIFIED.", ""]  # fmt: skip
    blob = []
    for c in random.Random(EXAMPLES_SEED).sample(cases, min(EXAMPLES, len(cases))):
        rd = c["readers"][X.LOOKUP]
        mine = [r for r in case_rows if r["scene"] == c["scene"]]
        e = {"scene": c["scene"], "prompt_O": R.marked(decode, rd["ids"]["org"] + c["space"], c["pos"]),
             "bridge": c["bridge"], "new_item": c["cf_bridge"], "slot_digits": c["slot_digits"], "j": c["j"],
             "lens_top_h": base[c["scene"]]["top"], "writes": mine}  # fmt: skip
        blob.append(e)
        lines += [f"## {c['scene']}: bridge {c['bridge']!r} in slot {c['j']}, digits by slot {c['slot_digits']}", "",
                  "```", e["prompt_O"], "```", "", f"Lens top {TOP}, h alone: {e['lens_top_h']}", ""]  # fmt: skip
        for r in mine:
            lines.append(f"- {r['arm']} to slot {r['k']} (norm {r['norm']}): best ordinal rank {r['best_ordinal']} "
                         f"({r['best_ordinal_tok']!r}), KL {r['kl']:.3g}; x8 lookup answer {r['x8_lookup_top']!r} "
                         f"({r['x8_lookup_class']}); top {TOP}: {r['top']}")  # fmt: skip
        lines.append("")
    (out / "examples.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    (out / "examples.md").write_text("\n".join(lines) + "\n")


# ---- the summary (CPU) ----------------------------------------------------------------------------------------------


def run_summary(src: Path, n_boot: int = X.N_BOOT) -> dict:
    """One model's run read back: (a) the ordinal / digit / written digit / new item's name statistics for the write
    and the identity direction against the random null, (c) the KL, (b) the reconstruction table, the directions'
    own readouts, and x8_write's lookup answers on the same writes."""
    m = json.loads((src / "manifest.json").read_text())
    rows = X.read_jsonl(src / "readouts.jsonl")
    nz = np.load(src / "null.npz")
    keys = list(zip(nz["scene"].tolist(), nz["k"].tolist(), strict=True))
    ents = nz["entity"].tolist()
    by = {(r["scene"], r["k"], r["arm"]): r for r in rows if r["arm"] != "base"}
    write = {f: np.array([by[(s, k, "write")][f] for s, k in keys], dtype=float)
             for f in ("kl", "best_ordinal", "best_digits", "target_digit", "alt_name")}  # fmt: skip
    has_id = [i for i, (s, k) in enumerate(keys) if (s, k, "identity") in by]
    ident = {f: np.array([by[(keys[i][0], keys[i][1], "identity")][f] for i in has_id], dtype=float)
             for f in ("kl", "alt_name", "best_ordinal")}  # fmt: skip
    run = str(src.relative_to(pins.REPO_ROOT)) if src.is_relative_to(pins.REPO_ROOT) else str(src)
    out: dict = {"run": run, "target": m["model"]["target"], "layer": m["layer"],
                 "n_cases": len(keys), "n_items": len(set(s for s, _ in keys)), "n_identity_cases": len(has_id),
                 "read_check": m.get("read_check"), "a": {}, "c": {}}  # fmt: skip
    for f in ("best_ordinal", "best_digits", "target_digit", "alt_name"):
        out["a"][f"write|{f}"] = against_null(write[f], nz[f], ents, lower_better=True, n_boot=n_boot)
    if has_id:
        e_id = [ents[i] for i in has_id]
        out["a"]["identity|alt_name"] = against_null(ident["alt_name"], nz["alt_name"][:, has_id], e_id, True, n_boot)
        out["a"]["identity|best_ordinal"] = against_null(ident["best_ordinal"], nz["best_ordinal"][:, has_id], e_id,
                                                         True, n_boot)  # fmt: skip
        out["c"]["identity"] = against_null(ident["kl"], nz["kl"][:, has_id], e_id, lower_better=False, n_boot=n_boot)
    out["c"]["write"] = against_null(write["kl"], nz["kl"], ents, lower_better=False, n_boot=n_boot)
    base = [r for r in rows if r["arm"] == "base"]
    out["a"]["h alone|best_ordinal median"] = float(np.median([r["best_ordinal"] for r in base]))
    out["a"]["h alone|best_digits median"] = float(np.median([r["best_digits"] for r in base]))
    cls = [by[(s, k, "write")]["x8_lookup_class"] for s, k in keys]
    out["x8_lookup_at_s2"] = {c: cls.count(c) / len(cls) for c in ("target", "original", "third", "other")}
    out["b"] = recon_summary(X.read_jsonl(src / "omp.jsonl"))
    out["b_atoms"] = {r["name"]: r["top_atoms"] for r in X.read_jsonl(src / "omp.jsonl")
                      if r["kind"] in ("U", "write") and r["dict"] == "all" and r["k"] == KS[0]}  # fmt: skip
    dirs = X.read_jsonl(src / "direction.jsonl")
    rnd = np.array([r["best_ordinal"] for r in dirs if r["kind"] == "random"], dtype=float)
    rnd_d = np.array([r["best_digits"] for r in dirs if r["kind"] == "random"], dtype=float)
    out["direction"] = {"null_p5_best_ordinal": float(np.percentile(rnd, LO_PCT)),
                        "null_p5_best_digits": float(np.percentile(rnd_d, LO_PCT)),
                        "vectors": [{k: r[k] for k in ("name", "kind", "best_ordinal", "best_ordinal_tok", "best_digits",
                                                        "best_digits_tok", "top")} for r in dirs if r["kind"] != "random"]}  # fmt: skip
    out["reading"] = model_reading(out["a"]["write|best_ordinal"], out["a"]["write|best_digits"],
                                   out["b"][f"all|{KS[0]}"]["ratio"], out["c"]["write"])  # fmt: skip
    return out


def fmt_ci(v: list[float]) -> str:
    return "–" if v[0] != v[0] else f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def summary_lines(blob: dict) -> list[str]:
    """The table (one column per model), the readings, the sanity swap line and a draft sentence."""
    models = blob["models"]
    cols = list(models)
    head = "| | " + " | ".join(f"{NAME.get(t, t)} (L{models[t]['layer']})" for t in cols) + " |"

    def row(label: str, f) -> str:
        return f"| {label} | " + " | ".join(f(models[t]) for t in cols) + " |"

    def vs(c: dict, digits: int = 0) -> str:
        return (f"{c['median']:.{digits}f} (null {'5th' if c['null_pct'] < 50 else '95th'} pct "
                f"{c['null_cut']:.{digits}f}){' beyond' if c['beyond'] else ''}")  # fmt: skip

    k0, k1 = KS
    lines = [head, "|---|" + "---|" * len(cols),
             row("items / cases (write to each other locker)", lambda r: f"{r['n_items']} / {r['n_cases']}"),
             row("x8's lookup on these writes at s = 2: to the written locker", lambda r: f"{r['x8_lookup_at_s2']['target']:.2f}"),
             row("(a) best ordinal-token rank, h alone (median)", lambda r: f"{r['a']['h alone|best_ordinal median']:.0f}"),
             row("(a) best ordinal-token rank, h + write (median)", lambda r: vs(r["a"]["write|best_ordinal"])),
             row("(a) best digit rank, h + write (median)", lambda r: vs(r["a"]["write|best_digits"])),
             row("(a) the written locker's digit, rank (median)", lambda r: vs(r["a"]["write|target_digit"])),
             row("(a) cases with the ordinal rank beyond their own null", lambda r: fmt_ci(r["a"]["write|best_ordinal"]["case_share_beyond"])),
             row("(a) positive control: new item's name rank, h + identity", lambda r: vs(r["a"]["identity|alt_name"]) if "identity|alt_name" in r["a"] else "–"),
             row(f"(b) share reconstructed, k = {k0}, every token: writes / U± / identity / random",
                 lambda r: " / ".join(f"{r['b'][f'all|{k0}'][f'{x}_mean']:.3f}" for x in ("write", "U", "identity", "random"))),
             row(f"(b) pointer / random, k = {k0} (every token; letters)",
                 lambda r: f"{r['b'][f'all|{k0}']['ratio']:.2f}x; {r['b'][f'letters|{k0}']['ratio']:.2f}x"),
             row(f"(b) pointer / random, k = {k1} (every token; letters)",
                 lambda r: f"{r['b'][f'all|{k1}']['ratio']:.2f}x; {r['b'][f'letters|{k1}']['ratio']:.2f}x"),
             row(f"(b) identity / random, k = {k0} (every token)", lambda r: f"{r['b'][f'all|{k0}']['identity_ratio']:.2f}x"),
             row("(c) KL(h || h + write) (median)", lambda r: vs(r["c"]["write"], 3)),
             row("(c) KL(h || h + identity, same norm) (median)", lambda r: vs(r["c"]["identity"], 3) if "identity" in r["c"] else "–"),
             row("(c) cases with KL beyond their own null", lambda r: fmt_ci(r["c"]["write"]["case_share_beyond"])),
             row("reading", lambda r: r["reading"]["label"])]  # fmt: skip
    sw = blob["sanity_swap"]
    order = [t for t in (*NAME,) if t in sw]
    lines += ["", f"Over the models: **{blob['overall']}**.", "",
              "Sanity swap (the other reading of Neel's question, augmenting the lens with the pointer): with J++ and U "
              "removed together the lookup still switches in " + " / ".join(f"{sw[t]['part'][0]:.2f}" for t in order)
              + " of the sanity-swap scenes (" + " / ".join(NAME[t] for t in order) + "; a random part of the same size: "
              + " / ".join(f"{sw[t]['random'][0]:.2f}" for t in order) + "; figures/story/data.csv, fig10, runs "
              + ", ".join(sw[t]["source"] for t in order) + ").", ""]  # fmt: skip
    for t in cols:
        lines.append(f"- {NAME.get(t, t)}: {models[t]['reading']['label']}: {models[t]['reading']['why']}.")
    lines += ["", f"Atoms the OMP picks first (every token, k = {k0}; the {ATOMS_LISTED} largest coefficients):"]
    for t in cols:
        lines += [f"- {NAME.get(t, t)}, {v}: " + ", ".join(repr(a) for a, _ in atoms[:ATOMS_LISTED])
                  for v, atoms in models[t]["b_atoms"].items()]  # fmt: skip
    return [*lines, "", "Draft sentence for the README's monitoring bullet (for Dan to edit): " + draft_sentence(blob)]


def draft_sentence(blob: dict) -> str:
    """One sentence from the numbers, worded by the overall reading (a draft; README claims are Dan's)."""
    ms = [blob["models"][t] for t in (*NAME,) if t in blob["models"]]
    moved = " / ".join(f"{m['x8_lookup_at_s2']['target']:.2f}" for m in ms)
    ratio = " / ".join(f"{m['b'][f'all|{KS[0]}']['ratio']:.1f}x" for m in ms)
    ords = " / ".join(f"{m['a']['write|best_ordinal']['median']:.0f}" for m in ms)
    kl_out = sum(m["c"]["write"]["beyond"] for m in ms)
    head = (f"Read through the J++ lens, a pointer write that sends the lookup to the written locker in {moved} of "
            f"cases leaves the best ordinal word at rank {ords} (median)")  # fmt: skip
    if blob["overall"] == "not verbalizable":
        return (f"{head}, the lens's own directions rebuild it no better than random ones ({ratio} the random share at "
                f"{KS[0]} directions), and the lens's readout moves no more than under a random vector of the same size: "
                f"a lens monitor would not see the pointer.")  # fmt: skip
    return (f"{head}; reconstruction by {KS[0]} lens directions is {ratio} a random direction's; the readout moves "
            f"beyond random on {kl_out} of {len(ms)} models ({blob['overall']}).")  # fmt: skip


def stage_summary(runs: list[str], n_boot: int = X.N_BOOT) -> Path:
    from bridge_jspace.utils import git_state

    out = RESULTS / f"summary-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    models, missing = {}, []
    for r in runs:
        src = RESULTS / r
        if not (src / "omp.jsonl").exists():
            missing.append(r)
            continue
        s = run_summary(src, n_boot)
        models[s["target"]] = s
    blob = {"exp": EXP, "test": "47.0", "descriptive": True, "code": git_state(), "runs": runs, "missing": missing,
            "models": models, "sanity_swap": sanity_swap(),
            "overall": overall({t: s["reading"]["label"] for t, s in models.items()})}  # fmt: skip
    (out / "verbal.json").write_text(json.dumps(blob, indent=1, ensure_ascii=False) + "\n")
    md = ["# 47.0: is the pointer verbalizable? (descriptive)", "",
          f"J++ lens at the layer fixed in advance; the write h + {S_WRITE:g} (mu_k - mu_j) at the bridge word of the routes "
          f"test's original prompts (x8_write's items); null: {N_RAND} random directions of the same norm (seed "
          f"{RAND_SEED}); statistics are medians over cases against the null's medians (scripts/x47_verbal.py). "
          "UNVERIFIED.", "", *(summary_lines(blob) if models else ["No run landed."]),
          *(["", f"Missing: {', '.join(missing)}."] if missing else [])]  # fmt: skip
    (out / "verbal.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    print(out)
    return out


# ---- the plan (CPU, the tokenizer) ----------------------------------------------------------------------------------


def stage_plan(n_items: int = N_ITEMS) -> dict:
    """On the target's tokenizer (BJ_TARGET; the cached files on a machine without weights): the items rebuilt and
    checked against x8_write's rows, the identity directions available, and the token sets."""
    from scripts import x0_massmean as MM
    from scripts import x45m

    target = pins.TARGET
    tok = x45m.tokenizer()
    cases, _ = routes_items(tok, target, n_items)
    ent = MM.entity_means(R.STATES[target])
    ids = [c for c in cases if c["bridge"] in ent and c["cf_bridge"] in ent]
    sets = token_sets(tok)
    out = {"target": target, "layer": X.PREDICTED[target], "items": len(cases), "identity_items": len(ids),
           "identity_pairs": len({(c["bridge"], c["cf_bridge"]) for c in ids}),
           "slots_j": {j: sum(c["j"] == j for c in cases) for j in W.SLOTS},
           "ordinal_tokens": sorted(sets["ordinal"].values()), "digit_tokens": sorted(sets["digits"].values()),
           "example": cases[0]["context"]}  # fmt: skip
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="stage", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--n-items", type=int, default=N_ITEMS)
    p = sub.add_parser("run")
    p.add_argument("--name", required=True)
    p.add_argument("--n-items", type=int, default=N_ITEMS)
    p.add_argument("--n-rand", type=int, default=N_RAND)
    p = sub.add_parser("summary")
    p.add_argument("--runs", nargs="+", default=list(RUN_NAME.values()))
    p.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan(a.n_items)
    elif a.stage == "run":
        stage_run(a.name, a.n_items, a.n_rand)
    else:
        stage_summary(a.runs, a.n_boot)


if __name__ == "__main__":
    main()
