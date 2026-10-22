"""pointer_mechanism (D3b, 2026-10-22): is the fitted slot direction the model's own statement address, or just a
direction that happens to move the answer?

Background (UNVERIFIED): pointer_fit fits, at the tokens after the question, the difference of class means between
items asking statement j and items asking statement a; pushed at the norm of a real patch it moves the lookup to
statement j (42% fresh scenes, 31% new entities / wording), while random, shuffled-label and lens directions of the
same norm move nothing, and a 4-dimensional subspace shared by all those tokens keeps most of the effect. That shows a
direction that WORKS; it does not show that the model USES it as an address. Six tests, Qwen3.6-27B, pointer_v4:

  fit      pointer_v4's fit set (fit entities and wordings, memory -> prompt, answered right): hidden states at every
           token after the question, layers 44-52, labelled by the asked statement's slot (0-4); per layer the class
           means mu_c [5, P, d], the grand mean m, the 4-dimensional slot basis (top principal directions of the class-
           mean deviations over all P tokens), the top-4 directions of overall variance, a random 4-dim basis.
  T1 geometry   is the address an ordered axis? Distances between the 5 class means (over all tokens) vs |i - j|:
           Spearman rho over the 10 pairs; a label-permutation null (200 shuffles). The last token's means on the top
           two principal directions are saved for a figure.
  T2 dose path  pushing from slot a toward a slot j with |j - a| >= 2 along mu_j - mu_a (its natural size times alpha,
           alpha = 0.25 ... 3), where does the answer first leave statement a: to j, to a slot in between, beyond j,
           or to the other side? An ordered address passes through the slots in between.
  T3 natural dose   the alt prompt's target slot j (pointer_fit's design), pushed by exactly mu_j - mu_a (alpha 1) and
           twice that, vs a random direction of the same per-token norm: does the address steer at the size the model
           itself uses?
  T4 necessity  remove the 4-dim slot subspace's deviation from the grand mean at every token after the question at
           every layer 44-52 (h <- h - P_B(h - m)); controls: the same with a random 4-dim basis and with the top-4
           directions of overall variance. Does the lookup (memory -> prompt) lose its answer while recall (memory ->
           memory) keeps it?
  T5 reader     during T3's pushes, the attention from the last token of layer 51 head 22 (and 59:21, 59:3): does the
           head move to the statement the push points at?
  T6 words      is the slot code like the words "first" / "2" / "three"? Cosine of each slot's deviation (last token)
           with the unembedding and J-lens vectors of ordinal, digit and number-word tokens vs random tokens.

Decision rule (fixed before the run; jobs/d3/d3b_mechanism_27b.yaml). Wilson 95% on items unless said; held-out items
only (asked entity or wording outside the fit); memory -> prompt primary, memory -> memory the control.
  H-axis (T1): rho >= 0.8 at layer 48 and the permutation p < 0.05.
  H-path (T2): among paths whose first departure lands on a statement of the prompt, the share landing strictly between
    a and j has its lower bound above the chance share (the slots in between / the 4 other slots, averaged), and the
    share landing on the other side of a has upper bound <= 0.15. H-jump: the share landing on j itself has lower
    bound >= 0.5 and the in-between share is not above chance.
  H-natural (T3): at alpha 1 (or 2) the slot-target rate's lower bound >= 0.10 and above the random push's upper bound.
  H-necessary (T4): with the slot subspace removed, memory -> prompt keeps answer org on <= 70% (upper bound), at least
    20 points below both control removals (paired item bootstrap lower bound > 0), and memory -> memory keeps >= 90%.
  H-reader (T5): on the alpha-2 pushes that moved the answer to j, head 51/22's top statement is j on >= 50% (lower
    bound), above its share on the random pushes' rows (upper bound).
  T6 is descriptive. Each hypothesis is reported holds / does not hold / not testable (n < 35 rows).

Stages:  run --name N --why W [--n-test 150] [--rr-n 50] [--primary-layer 48]   analyze --name N (CPU)
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from bridge_jspace.data import sha256_of
from bridge_jspace.stats import wilson
from scripts import d5a_head_pointer as D
from scripts import pointer_fit as PF
from scripts import pointer_swap as PS
from scripts import pointer_v4 as P4
from scripts import suite_v1 as S

EXP = "pointer_mechanism"
RESULTS = pins.RESULTS_DIR / EXP
LAYERS = (44, 45, 46, 47, 48, 49, 50, 51, 52)
HEADS = ("51:22", "59:21", "59:3")
ALPHAS = (0.25, 0.5, 1.0, 1.5, 2.0, 3.0)
N_PERM, PERM_SEED, NULL_SEED = 200, 0, 0
WORDS = {"ordinal": (" first", " second", " third", " fourth", " fifth"), "digit": ("1", "2", "3", "4", "5"),
         "number": (" one", " two", " three", " four", " five")}  # fmt: skip
BATCH = PS.BATCH


def cfg_of(args) -> dict[str, Any]:
    return {"data": "pointer_v4", "domains": list(P4.DOMAINS), "competence": args.competence, "n_test": args.n_test,
            "rr_n": args.rr_n, "fit_limit": None, "primary_layer": args.primary_layer}  # fmt: skip


# ---- pure helpers (tests/test_pointer_mechanism.py) ---------------------------------------------------------------


def spearman(x: list[float], y: list[float]) -> float:
    def ranks(v: list[float]) -> list[float]:
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2
            i = j + 1
        return r

    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry, strict=True))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def axis_rho(mu: torch.Tensor) -> tuple[float, list[list[float]]]:
    """Spearman rho between |i - j| and the distance of class means i, j (summed over tokens), and the distances."""
    c = mu.shape[0]
    dist = [[float((mu[i] - mu[j]).norm()) for j in range(c)] for i in range(c)]
    pairs = [(i, j) for i in range(c) for j in range(i + 1, c)]
    return spearman([abs(i - j) for i, j in pairs], [dist[i][j] for i, j in pairs]), dist


def landing(a: int, j: int, s: int) -> str:
    """Where a path from slot a toward slot j first lands at slot s: target / between / beyond / other side."""
    if s == j:
        return "target"
    lo, hi = sorted((a, j))
    if lo < s < hi:
        return "between"
    if (s - a) * (j - a) > 0:
        return "beyond"
    return "other side"


def remove_deviation(h: torch.Tensor, m: torch.Tensor, basis: torch.Tensor) -> torch.Tensor:
    """h [P, d] minus the part of (h - m) inside the row span of an orthonormal basis [k, d] (mean ablation in it)."""
    return h - PF.project(h - m, basis)


class Remove:
    def __init__(self, positions: list[int], m: torch.Tensor, basis: torch.Tensor):
        self.positions, self.m, self.basis = positions, m, basis

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        out = h.clone()
        out[self.positions] = remove_deviation(h[self.positions], self.m.to(h.dtype), self.basis.to(h.dtype))
        return out


# ---- the run ----------------------------------------------------------------------------------------------------------


def slot_of(item: dict, digit: str | None) -> int | None:
    digits = [str(d) for d in item["digits"]]
    return digits.index(digit) if digit in digits else None


@torch.no_grad()
def stage_run(name: str, why: str, cfg: dict) -> None:
    from bridge_jspace.knockout import capture_attention
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from bridge_jspace.utils import progress
    from scripts.early_push import forward_rows
    from scripts.exp03_brew_swaps import write_jsonl

    pins.check_run_name(name)
    out_dir = RESULTS / name
    out_dir.mkdir(parents=True, exist_ok=True)
    assert not (out_dir / "manifest.json").exists(), f"{out_dir} exists; runs are written once"
    files = PF.input_files(cfg)
    m_ = {"exp": EXP, "run": name, "why": why, "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "model": pins.model_pin(), "config": cfg, "layers": list(LAYERS), "alphas": list(ALPHAS), "heads": list(HEADS),
          "inputs": {PF.rel(p): sha256_of(p) for p in files}, "seeds": {"perm": PERM_SEED, "null": NULL_SEED},
          "decision": (__doc__ or "").split("Decision rule")[1].split("Stages:")[0].strip()}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(m_, indent=2) + "\n")
    model = load_model()
    tok = model.tokenizer
    lens = JLens(model, pins.FROZEN_LENS)
    digit_tok = {S.ids(tok, str(d))[0]: str(d) for d in range(10)}
    split = PF.pools(cfg)
    t0 = time.time()
    # fit
    feats: dict[int, list[torch.Tensor]] = {la: [] for la in LAYERS}
    labels: list[int] = []
    preps = [(it, PS.prepare(it, tok)) for it in PF.fit_items(cfg)]
    by_len: dict[int, list] = collections.defaultdict(list)
    for it, p in preps:
        by_len[len(p["read_ids"]["base"])].append((it, p))
    for chunk in progress([g[i : i + BATCH] for g in by_len.values() for i in range(0, len(g), BATCH)], "collect"):
        ids = torch.tensor([p["read_ids"]["base"] for _, p in chunk], device="cuda")
        logits, rec = forward_rows(model, ids, [{}] * len(chunk), LAYERS)
        for ri, (it, p) in enumerate(chunk):
            if digit_tok.get(int(logits[ri].argmax())) != it["answer"] or it["query"] not in split[it["domain"]][0]:
                continue
            for la in LAYERS:
                feats[la].append(rec[la][ri, p["groups"]["final"]].half().cpu())
            labels.append(it["slots"]["query"])
    y = torch.tensor(labels, device="cuda")
    fits: dict[int, dict[str, torch.Tensor]] = {}
    geo: dict[str, Any] = {"n_fit": len(labels), "per_slot": [int((y == c).sum()) for c in range(5)], "layers": {}}
    gperm = torch.Generator().manual_seed(PERM_SEED)
    for la in LAYERS:
        x = torch.stack(feats[la]).cuda().float()
        mu, m = PF.class_means(x, y)
        g = torch.Generator(device="cuda").manual_seed(NULL_SEED + la)
        fits[la] = {"mu": mu, "m": m, "slot4": PF.between_basis(mu, m, 4), "var4": PF.data_span(x, m, 4),
                    "rand4": torch.linalg.qr(torch.randn(x.shape[-1], 4, device="cuda", generator=g))[0].T}  # fmt: skip
        rho, dist = axis_rho(mu)
        null = []
        for _ in range(N_PERM):
            mu_p, _ = PF.class_means(x, y[torch.randperm(len(y), generator=gperm).to(y.device)])
            null.append(axis_rho(mu_p)[0])
        last = mu[:, -1] - m[-1]
        b2 = PF.top_directions(last, 2)
        ev = torch.linalg.svdvals(last)
        geo["layers"][la] = {"rho": round(rho, 4), "perm_p": round((1 + sum(r >= rho for r in null)) / (1 + N_PERM), 4),
                             "null_rho_95": round(sorted(null)[int(0.95 * N_PERM)], 4),
                             "distances": [[round(v, 2) for v in row] for row in dist],
                             "last_token_pc2": [[round(float(v), 3) for v in row] for row in (last @ b2.T)],
                             "last_token_pc1_share": round(float(ev[0] ** 2 / (ev**2).sum()), 4)}  # fmt: skip
        del x
    # T6 words: last-token slot deviations vs token vectors
    la0 = cfg["primary_layer"]
    dev = PF.unit_rows(fits[la0]["mu"][:, -1] - fits[la0]["m"][-1])
    W = model.hf.get_output_embeddings().weight.float()
    gen = torch.Generator(device="cuda").manual_seed(NULL_SEED)
    words: dict[str, Any] = {}
    rand_ids = torch.randint(0, W.shape[0], (500,), device="cuda", generator=gen)
    for kind, ws in WORDS.items():
        t = torch.tensor([S.ids(tok, w)[0] for w in ws], device="cuda")
        for space, vec in (("unembedding", PF.unit_rows(W[t])), ("lens", PF.unit_rows(lens.vectors(la0, t)))):
            words[f"{kind}/{space}"] = [[round(float(v), 4) for v in row] for row in dev @ vec.T]
    for space, vec in (("unembedding", PF.unit_rows(W[rand_ids])), ("lens", PF.unit_rows(lens.vectors(la0, rand_ids)))):
        words[f"random_max_abs_median/{space}"] = round(float((dev @ vec.T).abs().max(1).values.median()), 4)
    geo["words"] = words
    (out_dir / "geometry.json").write_text(json.dumps(geo, indent=2) + "\n")
    # tests
    tests = []
    for c in PF.test_items(cfg):
        try:
            PS.prepare(c, tok)
            tests.append(c)
        except AssertionError:
            pass
    hs = [tuple(int(v) for v in h.split(":")) for h in HEADS]
    att_layers = sorted({la for la, _ in hs})
    rows: list[dict] = []
    L = cfg["primary_layer"]
    for ci, c in enumerate(progress(tests, "tests")):
        p = PS.prepare(c, tok)
        fin = p["groups"]["final"]
        stmts = D.statement_tokens(p, c)
        a, j_alt = c["slots"]["query"], c["slots"]["position"]
        f = fits[L]
        jobs: list[tuple[dict, dict]] = [({"test": "unedited"}, {})]
        # T4 necessity
        for bname in ("slot4", "rand4", "var4"):
            jobs.append(({"test": "T4", "removed": bname},
                         {la: Remove(fin, fits[la]["m"], fits[la][bname]) for la in LAYERS}))  # fmt: skip
        if c["family"] == "RL":
            gen = torch.Generator(device="cuda").manual_seed(NULL_SEED + 7919 * ci)
            dm = f["mu"][j_alt] - f["mu"][a]
            for alpha in (1.0, 2.0):  # T3 natural dose (and T5 reads)
                jobs.append(({"test": "T3", "dir": "slot", "alpha": alpha, "target": j_alt},
                             {L: PS.AddRows(alpha * dm, fin)}))  # fmt: skip
                jobs.append(({"test": "T3", "dir": "random", "alpha": alpha, "target": j_alt},
                             {L: PS.AddRows(PS.null_rows(alpha * dm, gen), fin)}))  # fmt: skip
            for j in range(5):  # T2 dose path toward every slot >= 2 away
                if abs(j - a) < 2:
                    continue
                for alpha in ALPHAS:
                    jobs.append(({"test": "T2", "alpha": alpha, "target": j},
                                 {L: PS.AddRows(alpha * (f["mu"][j] - f["mu"][a]), fin)}))  # fmt: skip
        read = torch.tensor([p["read_ids"]["base"]], device="cuda")
        for start in range(0, len(jobs), BATCH):
            chunk = jobs[start : start + BATCH]
            probs: dict[int, torch.Tensor] = {}
            with capture_attention(model, att_layers, [len(p["read_ids"]["base"]) - 1], probs):
                logits, _ = forward_rows(model, read, [e for _, e in chunk])
            for ri, (tags, _) in enumerate(chunk):
                digit = digit_tok.get(int(logits[ri].argmax()))
                heads = {}
                for la, h in hs:
                    masses = [float(probs[la][ri, h, 0][s_].sum()) for s_ in stmts]
                    heads[f"{la}:{h}"] = max(range(len(masses)), key=lambda i, ms=masses: ms[i])
                rows.append({"id": c["id"], "family": c["family"], "domain": c["domain"], "entity": c["query"],
                             **PS.wording_of(c), "asked": a, **tags, "digit": digit, "answered": slot_of(c, digit),
                             "kept": digit == c["answer"], "heads": heads})  # fmt: skip
    write_jsonl(out_dir / "rows.jsonl", rows)
    (out_dir / "check.json").write_text(json.dumps({"tests": len(tests), "rows": len(rows),
                                                    "seconds": round(time.time() - t0)}, indent=2) + "\n")  # fmt: skip
    stage_analyze(name)


# ---- analysis ---------------------------------------------------------------------------------------------------------


def share(rows: list[dict], hit) -> dict[str, Any]:
    k, n = sum(bool(hit(r)) for r in rows), len(rows)
    p, lo, hi = wilson(k, n) if n else (float("nan"),) * 3
    return {"k": k, "n": n, "rate": [round(p, 4), round(lo, 4), round(hi, 4)]}


def paired_boot(a: list[float], b: list[float], n_boot: int = 2000, seed: int = 0) -> list[float]:
    rng = random.Random(seed)
    n = len(a)
    if not n:
        return [float("nan")] * 3
    d = sorted(sum(a[i] - b[i] for i in (rng.randrange(n) for _ in range(n))) / n for _ in range(n_boot))
    return [round(sum(a) / n - sum(b) / n, 4), round(d[int(0.025 * n_boot)], 4), round(d[int(0.975 * n_boot) - 1], 4)]


def analyse(rows: list[dict], geo: dict, primary: int) -> dict[str, Any]:
    out: dict[str, Any] = {}
    g = geo["layers"][str(primary)] if str(primary) in geo["layers"] else geo["layers"][primary]
    out["H-axis"] = {"rho": g["rho"], "perm_p": g["perm_p"], "holds": g["rho"] >= 0.8 and g["perm_p"] < 0.05}
    # T2
    paths: dict[tuple[str, int], list[dict]] = collections.defaultdict(list)
    for r in rows:
        if r["test"] == "T2":
            paths[(r["id"], r["target"])].append(r)
    first: list[str] = []
    chance: list[float] = []
    for (_, j), rs in paths.items():
        rs.sort(key=lambda r: r["alpha"])
        a = rs[0]["asked"]
        hit = next((r for r in rs if r["answered"] is not None and r["answered"] != a), None)
        if hit:
            first.append(landing(a, j, hit["answered"]))
            chance.append((abs(j - a) - 1) / 4)
    n = len(first)
    cnt = collections.Counter(first)
    between = wilson(cnt["between"], n) if n else (float("nan"),) * 3
    other = wilson(cnt["other side"], n) if n else (float("nan"),) * 3
    target = wilson(cnt["target"], n) if n else (float("nan"),) * 3
    ch = sum(chance) / n if n else float("nan")
    out["T2"] = {"paths": len(paths), "departed": n, "first_landing": dict(cnt), "chance_between": round(ch, 4),
                 "between": [round(v, 4) for v in between], "target": [round(v, 4) for v in target],
                 "other_side": [round(v, 4) for v in other]}  # fmt: skip
    out["H-path"] = n >= 35 and between[1] > ch and other[2] <= 0.15
    out["H-jump"] = n >= 35 and target[1] >= 0.5 and between[0] <= ch
    # T3 / T5
    t3 = [r for r in rows if r["test"] == "T3"]
    out["T3"] = {}
    for alpha in (1.0, 2.0):
        for d in ("slot", "random"):
            sel = [r for r in t3 if r["alpha"] == alpha and r["dir"] == d]
            out["T3"][f"{d}|{alpha}"] = share(sel, lambda r: r["answered"] == r["target"])
    out["H-natural"] = any(out["T3"][f"slot|{al}"]["n"] >= 35 and out["T3"][f"slot|{al}"]["rate"][1] >= 0.10
                           and out["T3"][f"slot|{al}"]["rate"][1] > out["T3"][f"random|{al}"]["rate"][2]
                           for al in (1.0, 2.0))  # fmt: skip
    moved = [r for r in t3 if r["alpha"] == 2.0 and r["dir"] == "slot" and r["answered"] == r["target"]]
    rand = [r for r in t3 if r["alpha"] == 2.0 and r["dir"] == "random"]
    out["T5"] = {h: {"moved_rows_head_on_target": share(moved, lambda r, h=h: r["heads"][h] == r["target"]),
                     "random_rows_head_on_target": share(rand, lambda r, h=h: r["heads"][h] == r["target"]),
                     "unedited_head_on_asked": share([r for r in rows if r["test"] == "unedited" and r["family"] == "RL"],
                                                     lambda r, h=h: r["heads"][h] == r["asked"])} for h in HEADS}  # fmt: skip
    t5 = out["T5"][HEADS[0]]
    out["H-reader"] = (t5["moved_rows_head_on_target"]["n"] >= 35 and t5["moved_rows_head_on_target"]["rate"][1] >= 0.5
                       and t5["moved_rows_head_on_target"]["rate"][1] > t5["random_rows_head_on_target"]["rate"][2])  # fmt: skip
    # T4
    out["T4"] = {}
    for fam in ("RL", "RR"):
        by_id: dict[str, dict[str, bool]] = collections.defaultdict(dict)
        for r in rows:
            if r["test"] == "T4" and r["family"] == fam:
                by_id[r["id"]][r["removed"]] = r["kept"]
        ids = [i for i, v in by_id.items() if len(v) == 3]
        cell = {b: share([{"k": by_id[i][b]} for i in ids], lambda r: r["k"]) for b in ("slot4", "rand4", "var4")}
        for b in ("rand4", "var4"):
            cell[f"slot4_minus_{b}"] = paired_boot(
                [float(by_id[i]["slot4"]) for i in ids], [float(by_id[i][b]) for i in ids]
            )
        out["T4"][fam] = cell
    rl, rr = out["T4"]["RL"], out["T4"].get("RR", {})
    out["H-necessary"] = (rl["slot4"]["n"] >= 35 and rl["slot4"]["rate"][2] <= 0.70
                          and all(rl[f"slot4_minus_{b}"][0] <= -0.20 and rl[f"slot4_minus_{b}"][2] < 0 for b in ("rand4", "var4"))
                          and bool(rr) and rr["slot4"]["rate"][1] >= 0.90)  # fmt: skip
    out["T6"] = geo.get("words", {})
    return out


def stage_analyze(name: str) -> Path:
    run = RESULTS / name
    m = json.loads((run / "manifest.json").read_text())
    geo = json.loads((run / "geometry.json").read_text())
    rows = [json.loads(x) for x in (run / "rows.jsonl").read_text().splitlines()]
    a = analyse(rows, geo, m["config"]["primary_layer"])
    dest = run / f"analysis-{time.strftime('%Y%m%d-%H%M%S')}"
    dest.mkdir()
    (dest / "summary.json").write_text(json.dumps(a, indent=2) + "\n")
    print(json.dumps({k: v for k, v in a.items() if k.startswith("H-")}))
    print("wrote", dest)
    return dest


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["run", "analyze"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why")
    ap.add_argument("--competence", default="d3v4_competence_27b")
    ap.add_argument("--n-test", type=int, default=150)
    ap.add_argument("--rr-n", type=int, default=50)
    ap.add_argument("--primary-layer", type=int, default=48)
    args = ap.parse_args()
    if args.stage == "run":
        assert args.why, "run needs --why"
        stage_run(args.name, args.why, cfg_of(args))
    else:
        stage_analyze(args.name)
