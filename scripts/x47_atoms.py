"""x47_atoms (batch 47, test 47.1; jobs/c3/batch47.yaml, design and rule fixed in advance; Q47.1 in
predictions/2026-10-28_dan.md): where does the lookup's identity route live, outside the lens or outside the 25 atoms
the recall uses?

The change Δ = h_S - h_O at the bridge word and layer L (9B L12, 27B L32, Muse L26), its signed OMP over the J++ lens's
letter-token atoms with K = 100 (X0's OMP: x0_necessity.fit / x0_parts.omp_atoms; greedy, so atoms 1-25 are the
k = 25 picks). The parts, each removed from Δ (an arm) against a random part of the same share of ||Δ||^2 (X0's random
subspace, seed 888 + L):
  1-25          P25 Δ, the J++ part (the existing no_jpp arm; x0_necessity's ("jpp", 25, "signed"))
  1-100         P100 Δ (no_jpp100; ("jpp", 100, "signed"))
  26-100        P100 Δ - P25 Δ: what atoms 26-100 add beyond atoms 1-25 (Δ's component in their span projected off
                atoms 1-25). Removing it keeps P25 Δ exactly; the 1-25 and 26-100 removals add up to the 1-100 removal.
  ratoms75own   75 random lens atoms per item (letter-token atoms outside its 100 OMP picks, seed RATOM_SEED and the
                scene id): Δ's component in their span projected off atoms 1-25 (count matched, its own share)
  ratoms75      the same direction scaled to the 26-100 slice's share of ||Δ||^2 (count and share matched: the spec's
                dumbest way 2; the scale alpha per item recorded, alpha > 1 where the random atoms hold less)
The GPU work is in the existing scripts: x6_routes run --jpp-ks 25 100 --atom-slices (routes, another item moved, C2,
300 scenes; identity / position / value classification) and x0_necessity run --curve-dicts jpp --curve-k 100
--atom-slices (the main test, 200 scenes, both readers); both call slices_with_geometry. Per item they record each
slice's share of ||Δ||^2, alpha, and the mean cos^2 of the spans with the pointer directions U (||P U||_F^2 / rank U):
atoms 1-25, 1-100, the 26-100 slice's and the random atoms' removed directions.

Rule (stage verdict; fixed in advance, as computed in the job specs' decision_rule): per model, on routes C2 the
identity fall beyond random = identity share(no_jpp26_100_rand) - identity share(no_jpp26_100) (lookup), on the main test
the recall's extra loss without 26-100 (X0's excess). (a) "beyond the 25": fall >= 0.30 with its paired CI's lower bound
> 0 and the recall's extra loss <= 0.10; (b) "continuum": fall >= 0.20 and the recall's extra loss >= 0.20; (c)
"outside the lens": fall < 0.10. (a) for the batch: on >= 2 of 3 models. Point estimates decide (EPS 1e-9 at the bars);
cluster-bootstrap CIs over the bridge items (10,000, seed 0) beside them.

SEALED: the jobs write per-item outputs only. verdict refuses until predictions/2026-10-28_dan.md holds Dan's Q47.1
answer at the committed HEAD; x6_routes' and x0_necessity's own verdict / examples stages refuse on these runs too.

uv run python scripts/x47_atoms.py verdict      # CPU, after Dan's Q47.1: the rule, the shares, the verify-pack view
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import subprocess
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

EXP = "x47_atoms"
RESULTS = pins.RESULTS_DIR / EXP
SPEC = "jobs/c3/batch47.yaml"
PREDICTIONS = "predictions/2026-10-28_dan.md"
QUESTION = "Q47.1"
K_KEEP, K_ALL = X.K_MAIN, 100  # atoms 1-25 kept, 1-100 the OMP
N_RAND_ATOMS = K_ALL - K_KEEP  # 75
RATOM_SEED = 4701
# the new parts: name -> x0_necessity's (dict, k, fit) key
SLICE_KEYS = {"jpp26_100": ("jpp26_100", N_RAND_ATOMS, "slice"), "ratoms75": ("ratoms75", N_RAND_ATOMS, "scaled"),
              "ratoms75own": ("ratoms75own", N_RAND_ATOMS, "own")}  # fmt: skip
# per part: label, the routes run's part name (arms no_<p>, no_<p>_rand), the main test's (dict, k, fit)
PARTS = (("1-25", "jpp", ("jpp", K_KEEP, "signed")), ("1-100", "jpp100", ("jpp", K_ALL, "signed")),
         ("26-100", "jpp26_100", SLICE_KEYS["jpp26_100"]),
         ("random atoms, same share", "ratoms75", SLICE_KEYS["ratoms75"]),
         ("random atoms, own share", "ratoms75own", SLICE_KEYS["ratoms75own"]))  # fmt: skip
DECISIVE = "26-100"
ROUTE_ARMS = ("whole", *(a for _, p, _ in PARTS for a in (f"no_{p}", f"no_{p}_rand")))
MODELS = ("qwen3.6-27b", "qwen3.5-9b", "muse-glimmer-30b")  # the queue's order
ROUTES_RUNS = {"qwen3.6-27b": "x6_routes_x47_1_27b", "qwen3.5-9b": "qwen35_9b_x6_routes_x47_1",
               "muse-glimmer-30b": "muse30_x6_routes_x47_1"}  # fmt: skip
MAIN_RUNS = {"qwen3.6-27b": "x47_1_main_27b", "qwen3.5-9b": "qwen35_9b_x47_1_main",
             "muse-glimmer-30b": "muse30_x47_1_main"}  # fmt: skip
FALL_A, FALL_B, FALL_C = 0.30, 0.20, 0.10
RECALL_A, RECALL_B = 0.10, 0.20
MODELS_MIN = 2
EPS = 1e-9  # a value exactly at a bar counts as at the bar
LABELS = {"a": "(a) beyond the 25", "b": "(b) continuum", "c": "(c) outside the lens"}
RULE = ("per model: (a) \"the lookup's identity route sits in lens atoms beyond the recall's 25\" if without atoms "
        "26-100 identity answers fall >= 0.30 beyond the random part (paired CI excluding 0) and the recall's extra loss "
        "without 26-100 is <= 0.10; (b) \"continuum\" if both readers lose >= 0.20 beyond random without 26-100; (c) "
        "\"outside the lens\" if identity answers fall < 0.10 beyond random; (a) for the batch on >= 2 of 3 models")  # fmt: skip
READER_NAME = {X.LOOKUP: "lookup", X.RECALL: "recall"}


# ---- sealed until Dan's answer -------------------------------------------------------------------------------------


def answer_in(text: str, question: str) -> str:
    """The 'Dan:' line of the question's own block (from the line that begins with its bold id to the next bold
    question) in a predictions file's text; '' if none."""
    start = re.search(rf"^\*\*{re.escape(question)}\*\*", text, re.M)
    block = text[start.end() :].split("\n**Q", 1)[0] if start else ""
    m = re.search(r"^Dan:(.*)$", block, re.M)
    return m.group(1).strip() if m else ""


def dan_answer(question: str = QUESTION, rev: str = "HEAD") -> str:
    """Dan's committed answer to the question in the predictions file at `rev` ('' if none or not committed)."""
    text = subprocess.run(["git", "show", f"{rev}:{PREDICTIONS}"], cwd=pins.REPO_ROOT, capture_output=True, text=True,
                          check=False).stdout  # fmt: skip
    return answer_in(text, question)


def require_answer(question: str = QUESTION) -> str:
    """Dan's committed answer, or stop: a batch-47 test's results stay closed until it is committed."""
    answer = dan_answer(question)
    if not answer:
        raise SystemExit(f"sealed: {PREDICTIONS} has no committed answer to {question} (its 'Dan:' line is empty at "
                         "HEAD); verdicts, tables and examples run after it")  # fmt: skip
    return answer


# ---- the parts (GPU in the run scripts; CPU here) ------------------------------------------------------------------


def random_atoms(n_atoms: int, picked, scene: str, k: int = N_RAND_ATOMS, seed: int = RATOM_SEED) -> list[int]:
    """k distinct dictionary rows drawn uniformly (a stream keyed by seed and the scene id) from the n_atoms rows
    outside `picked` (the item's OMP atoms)."""
    picked = {int(p) for p in picked}
    assert n_atoms - len(picked) >= k, f"{n_atoms} atoms, {len(picked)} picked: fewer than {k} left"
    draw = random.Random(f"x47_1|{seed}|{scene}").sample(range(n_atoms), min(n_atoms, k + len(picked)))
    out = [a for a in draw if a not in picked][:k]
    assert len(out) == k
    return out


def atom_slices(jdic, x, scenes: list[str], fit_keep, fit_all, atoms, alf=None, seed: int = RATOM_SEED):
    """47.1's new parts of each row of x [n, d] (Δ at the bridge word), from its K = 100 signed-OMP picks `atoms`
    [n, >= 100] (rows of jdic, in OMP order) and X.fit's parts at k = 25 (fit_keep) and 100 (fit_all): jpp26_100 =
    fit_all - fit_keep (in atoms 1-100's span, orthogonal to atoms 1-25's: both up to rounding, recorded per row as
    slice_off_1_25 and slice_out_of_1_100 relative to ||Δ||, and asserted under 1e-2); ratoms75own = Δ's component
    in the span of 75 random atoms (random_atoms) projected off atoms 1-25; ratoms75 = that part scaled to jpp26_100's
    share of ||Δ||^2. Per row: each slice's share of ||Δ||^2, the scale alpha (None where the random atoms hold
    nothing), the random atoms, and with alf ([d, r], the pointer directions U) the mean cos^2 of the 26-100 slice's
    and the random atoms' removed directions with U. Returns ({part: [n, d]}, records)."""
    import torch

    total = (x.double().norm(dim=-1) ** 2).clamp_min(1e-30)
    u = R.orthonormal(alf) if alf is not None else None
    parts: dict[str, list] = {name: [] for name in SLICE_KEYS}
    recs = []
    for i, scene in enumerate(scenes):
        xi = x[i].double()
        q25 = R.orthonormal(jdic[atoms[i, :K_KEEP]].T)
        q100 = R.orthonormal(jdic[atoms[i, :K_ALL]].T)

        def off25(cols, q25=q25):  # columns projected off atoms 1-25's span
            return cols - q25 @ (q25.T @ cols)

        part = (fit_all[i] - fit_keep[i]).double()
        # X.fit's parts are float32 least-squares fits (ridge 1e-8): the slice is off atoms 1-25 and inside 1-100 up to
        # rounding, recorded per row (relative to ||Δ||); 1e-2 only catches a part that is not these atoms' fit at all
        off = {"slice_off_1_25": float((q25.T @ part).norm() / xi.norm().clamp_min(1e-30)),
               "slice_out_of_1_100": float((part - q100 @ (q100.T @ part)).norm() / xi.norm().clamp_min(1e-30))}  # fmt: skip
        assert off["slice_off_1_25"] < 1e-2, f"row {i}: the 26-100 slice is not orthogonal to atoms 1-25 ({off})"
        assert off["slice_out_of_1_100"] < 1e-2, f"row {i}: the 26-100 slice is not in atoms 1-100's span ({off})"
        q_slice = R.orthonormal(off25(jdic[atoms[i, K_KEEP:K_ALL]].T.double()))
        ids = random_atoms(jdic.shape[0], atoms[i, :K_ALL].tolist(), scene, seed=seed)
        q_rand = R.orthonormal(off25(jdic[torch.as_tensor(ids, device=jdic.device)].T.double()))
        own = q_rand @ (q_rand.T @ xi)
        s = {"share_1_25": float(fit_keep[i].double().norm() ** 2 / total[i]),
             "share_26_100": float(part.norm() ** 2 / total[i]), "share_1_100": float(fit_all[i].double().norm() ** 2 / total[i]),
             "share_ratoms75own": float(own.norm() ** 2 / total[i])}  # fmt: skip
        alpha = math.sqrt(s["share_26_100"] / s["share_ratoms75own"]) if s["share_ratoms75own"] > 1e-12 else None
        parts["jpp26_100"].append(part)
        parts["ratoms75own"].append(own)
        parts["ratoms75"].append(own * alpha if alpha is not None else torch.zeros_like(own))
        rec: dict[str, Any] = {k: round(v, 6) for k, v in s.items()}
        rec.update({"ratoms75_alpha": None if alpha is None else round(alpha, 6), "ratoms75_atoms": ids,
                    "ratoms_seed": seed, **{k: float(f"{v:.3g}") for k, v in off.items()}})  # fmt: skip
        if u is not None:
            for key, q in (("cos2_U_jpp26_100", q_slice), ("cos2_U_ratoms75", q_rand)):
                c = R._cos2(q, u.to(q.device))
                rec[key] = None if c is None else round(c, 6)
        recs.append(rec)
    return {k: torch.stack(v).to(x.dtype) for k, v in parts.items()}, recs


def slices_with_geometry(jdic, x, scenes: list[str], fit_keep, fit_all, alf, seed: int = RATOM_SEED):
    """atom_slices over the K = 100 picks (x0_parts.omp_atoms), with 45k's cos^2 of atoms 1-25's and 1-100's spans
    with U (x6_routes.jpp_geometry, which also checks that X.fit's parts lie in those spans) in each record."""
    from scripts import x0_parts as XP

    atoms = XP.omp_atoms(jdic, x, K_ALL)
    parts, recs = atom_slices(jdic, x, scenes, fit_keep, fit_all, atoms, alf, seed)
    geo = R.jpp_geometry(jdic, atoms, (K_KEEP, K_ALL), alf, [None] * len(scenes), {K_KEEP: fit_keep, K_ALL: fit_all})
    for rec, g in zip(recs, geo, strict=True):
        rec.update({k: v for k, v in g.items() if k.startswith("cos2_U")})
    return parts, recs


def pointer_basis(target: str):
    """U, the pointer directions fit on fresh scenes (x0_massmean on the probe's states; never refit): [d, r]."""
    from scripts import x0_massmean as MM

    return MM.subspaces(R.STATES[target])[0]["Alf"]


def manifest_record() -> dict:
    """What a 47.1 run's manifest records about the new parts (x6_routes and x0_necessity)."""
    return {"test": "47.1", "spec": SPEC, "question": f"{QUESTION} ({PREDICTIONS})", "k_keep": K_KEEP, "k_all": K_ALL,
            "omp": "signed (X.fit); atoms in OMP order (x0_parts.omp_atoms), the first 25 being the k = 25 picks",
            "parts": {"jpp26_100": "P100 Δ - P25 Δ (X.fit at 100 minus at 25): atoms 26-100's span projected off atoms 1-25",
                      "ratoms75own": f"Δ's component in the span of {N_RAND_ATOMS} random letter-token lens atoms "
                                     "(outside the item's 100 OMP picks) projected off atoms 1-25",
                      "ratoms75": "ratoms75own scaled to jpp26_100's share of ||Δ||^2 (alpha per item)"},
            "random_atoms_seed": f"{RATOM_SEED} and the scene id (x47_atoms.random_atoms)",
            "random_parts": f"X0's random subspace at each part's share of ||Δ||^2, seed {X.SUBSPACE_SEED} + layer",
            "sealed": f"no verdict in the job; results closed until {PREDICTIONS} holds Dan's {QUESTION}"}  # fmt: skip


# ---- numbers (CPU) -------------------------------------------------------------------------------------------------


def _ci(pt: float, boot) -> list[float]:
    return [pt, *X.interval(boot)]


def routes_numbers(rows: list[dict], n_boot: int = X.N_BOOT) -> dict | None:
    """A routes run's C2 rows: per arm the lookup's route shares and the recall's S-answer share (cluster-bootstrap
    CIs over the bridge items); per part the fall of each route's share beyond its random part (share(no_<p>_rand) -
    share(no_<p>), paired), and the 26-100 slice against the random lens atoms at its share (share(no_ratoms75) -
    share(no_jpp26_100)). None without C2 rows."""
    lk = [r for r in rows if r["condition"] == "C2" and r["reader"] == X.LOOKUP]
    rc = {
        (r["scene"], r["arm"]): int(r["switched"]) for r in rows if r["condition"] == "C2" and r["reader"] == X.RECALL
    }
    arms = [a for a in ROUTE_ARMS if any(r["arm"] == a for r in lk)]
    if "whole" not in arms:
        return None
    by = {a: {r["scene"]: r for r in lk if r["arm"] == a} for a in arms}
    scenes = sorted(set.intersection(*(set(v) for v in by.values())))
    ents = [by["whole"][s]["entity"] for s in scenes]
    sw = {f"{rt}|{a}": [int(by[a][s]["route"] == rt) for s in scenes] for a in arms for rt in R.ROUTES}
    sw.update({f"recall|{a}": [rc.get((s, a), 0) for s in scenes] for a in arms})
    rr = X.resampled_rates(sw, ents, n_boot)
    pt = {k: float(np.mean(v)) for k, v in sw.items()}

    def fall(rt: str, removed: str, control: str) -> list[float]:
        return _ci(pt[f"{rt}|{control}"] - pt[f"{rt}|{removed}"], rr[f"{rt}|{control}"] - rr[f"{rt}|{removed}"])

    falls = {label: {rt: fall(rt, f"no_{p}", f"no_{p}_rand") for rt in ("identity", "position", "value")}
             for label, p, _ in PARTS if f"no_{p}" in arms and f"no_{p}_rand" in arms}  # fmt: skip
    vs = ({rt: fall(rt, "no_jpp26_100", "no_ratoms75") for rt in ("identity", "position", "value")}
          if {"no_jpp26_100", "no_ratoms75"} <= set(arms) else None)  # fmt: skip
    return {"n": len(scenes), "entities": len(set(ents)),
            "shares": {a: {rt: _ci(pt[f"{rt}|{a}"], rr[f"{rt}|{a}"]) for rt in (*R.ROUTES, "recall")} for a in arms},
            "falls": falls, "vs_random_atoms": vs}  # fmt: skip


def main_numbers(rows: list[dict], layer: int, n_boot: int = X.N_BOOT) -> dict | None:
    """A main-test run's chat rows at L: per reader and part X0's cell (switch rates, Jdep, Rdep, extra loss, valid),
    and the 26-100 slice's switches lost minus the random lens atoms' at its share (paired). None without rows."""
    mine = [r for r in rows if r.get("rendering") == "chat" and r["layer"] == layer]
    if not mine:
        return None
    cells = X.cells_of(mine, n_boot)
    out: dict[str, Any] = {"readers": {}, "vs_random_atoms": {}}
    for w in X.READERS:
        out["readers"][w] = {label: cells[("chat", layer, w, *key)] for label, _, key in PARTS
                             if ("chat", layer, w, *key) in cells}  # fmt: skip
        sw: dict[str, dict[str, int]] = {"whole": {}, "slice": {}, "atoms": {}}
        ent: dict[str, str] = {}
        for r in mine:
            if r["reader"] != w:
                continue
            ent[r["scene"]] = r["entity"]
            key = (r["dict"], r["k"], r["omp"])
            if r["arm"] == "whole":
                sw["whole"][r["scene"]] = r["switched"]
            elif r["arm"] == "no_part" and key in (SLICE_KEYS["jpp26_100"], SLICE_KEYS["ratoms75"]):
                sw["slice" if key == SLICE_KEYS["jpp26_100"] else "atoms"][r["scene"]] = r["switched"]
        if sw["slice"] and sw["atoms"]:
            scenes = sorted(sw["whole"])
            s = {a: [v[sc] for sc in scenes] for a, v in sw.items()}
            rr = X.resampled_rates(s, [ent[sc] for sc in scenes], n_boot)
            m = {a: float(np.mean(v)) for a, v in s.items()}
            point = float(X.dependence(m["whole"], m["slice"]) - X.dependence(m["whole"], m["atoms"]))
            out["vs_random_atoms"][w] = _ci(
                point, X.dependence(rr["whole"], rr["slice"]) - X.dependence(rr["whole"], rr["atoms"])
            )
    return out


def model_label(routes: dict | None, main: dict | None) -> dict:
    """The rule on one model (point estimates, EPS at the bars). routes: routes_numbers (None: the routes gate failed
    or no run: not tested); main: main_numbers (None, or an invalid recall cell by X0's rule: (a) and (b) can't be read,
    (c) still is). The three clauses exclude each other by their bars."""
    if routes is None or DECISIVE not in routes["falls"]:
        return {"status": "not tested", "label": "not tested", "clauses": {}, "why": "no routes C2 rows (gate or run)"}
    fall = routes["falls"][DECISIVE]["identity"]
    rc = (main or {}).get("readers", {}).get(X.RECALL, {}).get(DECISIVE)
    c = fall[0] < FALL_C - EPS
    if rc is None or not rc["valid"]:
        why = "no main-test recall cell" if rc is None else "the main-test recall cell is invalid (X0's rule)"
        return {"status": "tested", "label": LABELS["c"] if c else "can't tell", "clauses": {"c": c},
                "identity_fall": fall, "recall_extra_loss": None, "why": why}  # fmt: skip
    ex = rc["excess"][0]
    clauses = {"a": fall[0] >= FALL_A - EPS and fall[1] > 0 and ex <= RECALL_A + EPS,
               "b": fall[0] >= FALL_B - EPS and ex >= RECALL_B - EPS, "c": c}  # fmt: skip
    held = [k for k in ("a", "b", "c") if clauses[k]]
    assert len(held) <= 1, f"clauses {held} hold together"
    why = (f"identity fall beyond random {fall[0]:.3f} [{fall[1]:.3f}, {fall[2]:.3f}]; recall extra loss "
           f"{ex:.3f} [{rc['excess'][1]:.3f}, {rc['excess'][2]:.3f}]")  # fmt: skip
    return {"status": "tested", "label": LABELS[held[0]] if held else "none of (a)-(c)", "clauses": clauses,
            "identity_fall": fall, "recall_extra_loss": rc["excess"], "why": why}  # fmt: skip


def batch_rule(models: list[dict]) -> dict:
    """(a) for the batch: on at least MODELS_MIN models; pending while too few are in to decide."""
    n_a = sum(m["label"] == LABELS["a"] for m in models)
    n_pending = sum(m["status"] == "pending" for m in models)
    label = "holds" if n_a >= MODELS_MIN else "does not hold" if n_a + n_pending < MODELS_MIN else "pending"
    return {"a_holds": label, "models_a": n_a, "models": len(models),
            "per_model": {m["target"]: m["label"] for m in models}}  # fmt: skip


def share_summary(recs: list[dict]) -> dict:
    """Each slice's share of ||Δ||^2 over the items (median), the 26-100 vs 1-25 check (dumbest way 1) and the mean
    cos^2 with U (dumbest way 3)."""

    def med(key: str) -> float | None:
        v = [r[key] for r in recs if r.get(key) is not None]
        return float(np.median(v)) if v else None

    def mean(key: str) -> float | None:
        v = [r[key] for r in recs if r.get(key) is not None]
        return float(np.mean(v)) if v else None

    both = [r for r in recs if r.get("share_1_25") is not None and r.get("share_26_100") is not None]
    return {"n": len(recs), **{f"median_{k}": med(k) for k in ("share_1_25", "share_26_100", "share_1_100",
                                                               "share_ratoms75own", "ratoms75_alpha")},
            "alpha_above_1": sum((r.get("ratoms75_alpha") or 0) > 1 for r in recs),
            "items_26_100_above_1_25": sum(r["share_26_100"] > r["share_1_25"] for r in both),
            "items_per_atom_order_holds": sum(r["share_26_100"] / N_RAND_ATOMS < r["share_1_25"] / K_KEEP for r in both),
            "median_per_atom_ratio": float(np.median([(r["share_26_100"] / N_RAND_ATOMS) / max(r["share_1_25"] / K_KEEP, 1e-30)
                                                      for r in both])) if both else None,
            **{f"mean_{k}": mean(k) for k in ("cos2_U_jpp25", "cos2_U_jpp100", "cos2_U_jpp26_100", "cos2_U_ratoms75")}}  # fmt: skip


# ---- the verdict and the verify-pack view (CPU) --------------------------------------------------------------------


def _run_dir(exp: str, name: str) -> Path:
    return pins.RESULTS_DIR / exp / name


def model_result(target: str, routes_run: str, main_run: str, n_boot: int = X.N_BOOT) -> dict:
    """One model's two runs: pending (a run not here), or the numbers, shares and the rule."""
    rsrc, msrc = _run_dir(R.EXP, routes_run), _run_dir(X.EXP, main_run)
    missing = [str(p) for p in (rsrc, msrc) if not (p / "manifest.json").exists()]
    if missing:
        return {"target": target, "runs": [routes_run, main_run], "status": "pending", "label": "pending",
                "why": f"no manifest: {', '.join(missing)}"}  # fmt: skip
    rm, mm = (json.loads((p / "manifest.json").read_text()) for p in (rsrc, msrc))
    for m, name in ((rm, routes_run), (mm, main_run)):
        assert m["model"]["target"] == target, f"{name} is a {m['model']['target']} run, not {target}'s"
        assert m.get("x47_1"), f"{name} is not a 47.1 run (--atom-slices)"
    layer = mm["predicted"]
    assert rm["layer"] == layer, f"{routes_run} at L{rm['layer']}, {main_run} at L{layer}"
    rgate = json.loads((rsrc / "gate.json").read_text())["gate"] if (rsrc / "gate.json").exists() else {}
    mgate = (
        json.loads((msrc / "gate.json").read_text())["gate"].get("chat", {}) if (msrc / "gate.json").exists() else {}
    )
    routes = routes_numbers(X.read_jsonl(rsrc / "outcomes.jsonl"), n_boot) if rgate.get("C2", {}).get("pass") else None
    main = main_numbers(X.read_jsonl(msrc / "outcomes.jsonl"), layer, n_boot)
    lab = model_label(routes, main)
    norms = [r for r in X.read_jsonl(rsrc / "norms.jsonl") if r.get("condition") == "C2"]
    atoms = X.read_jsonl(msrc / "atoms.jsonl")
    return {"target": target, "runs": [routes_run, main_run], "layer": layer, **lab, "routes": routes, "main": main,
            "gates": {"routes_C2": rgate.get("C2"), "main_chat": mgate},
            "shares": {"routes": share_summary(norms), "main": share_summary(atoms)}}  # fmt: skip


def fmt(v) -> str:
    if v is None or v[0] is None or (isinstance(v[0], float) and math.isnan(v[0])):
        return "-"
    return f"{v[0]:.2f} [{v[1]:.2f}, {v[2]:.2f}]"


def f3(v) -> str:
    return "-" if v is None else f"{v:.3f}"


def verdict_lines(models: list[dict], batch: dict, answer: str, n_boot: int) -> list[str]:
    lines = ["# 47.1: where does the lookup's identity route live?", "",
             f"Batch 47, test 47.1 ({SPEC}; {QUESTION}, Dan: {answer}). Δ at the bridge word and L; signed OMP over the "
             "J++ lens's letter-token atoms with K = 100; each part removed against a random part of the same share of "
             f"||Δ||^2; cluster bootstrap over the bridge items ({n_boot}, seed {X.BOOT_SEED}). UNVERIFIED.", "",
             f"Rule (fixed in advance): {RULE}.", "",
             f"**(a) for the batch: {batch['a_holds']}** ({batch['models_a']} of {batch['models']} models; at least "
             f"{MODELS_MIN} needed).", "",
             "| model | runs | routes C2 n | identity fall beyond random, 26-100 (routes) | recall extra loss, 26-100 "
             "(main) | lookup extra loss, 26-100 (main; beside) | label |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            lines.append(f"| {m['target']} | {', '.join(m['runs'])} | pending ({m['why']}) | | | | |")
            continue
        n = m["routes"]["n"] if m["routes"] else "-"
        lk = ((m["main"] or {}).get("readers", {}).get(X.LOOKUP, {}).get(DECISIVE) or {}).get("excess")
        lines.append(f"| {m['target']} | {', '.join(m['runs'])} | {n} | {fmt(m.get('identity_fall'))} | "
                     f"{fmt(m.get('recall_extra_loss'))} | {fmt(lk)} | **{m['label']}** |")  # fmt: skip
    lines += ["", "Routes test, another item moved (C2), lookup: route shares per arm (the recall's S-answer share in "
              "the last column).", "", "| model | arm | " + " | ".join(R.ROUTES) + " | recall S |",
              "|---|---|" + "---|" * (len(R.ROUTES) + 1)]  # fmt: skip
    for m in models:
        if m["status"] == "pending" or not m["routes"]:
            continue
        for arm, s in m["routes"]["shares"].items():
            lines.append(f"| {m['target']} | {arm} | " + " | ".join(fmt(s[rt]) for rt in (*R.ROUTES, "recall")) + " |")
    lines += ["", "Falls beyond each part's random part (share without the random part minus share without the part, "
              "paired), and the 26-100 slice against the random lens atoms at its share (count and share matched).", "",
              "| model | part | identity | position | value |", "|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending" or not m["routes"]:
            continue
        for label, f in m["routes"]["falls"].items():
            lines.append(
                f"| {m['target']} | {label} | {fmt(f['identity'])} | {fmt(f['position'])} | {fmt(f['value'])} |"
            )
        vs = m["routes"]["vs_random_atoms"]
        if vs:
            lines.append(f"| {m['target']} | 26-100 vs random atoms | {fmt(vs['identity'])} | {fmt(vs['position'])} | "
                         f"{fmt(vs['value'])} |")  # fmt: skip
    lines += ["", "Main test (two people swap picks), X0's cells at L: switch rates and extra loss (switches lost "
              "without the part minus without its random part, over the whole change's switches).", "",
              "| model | reader | part | n | S_whole | S without | S without random | extra loss | valid |",
              "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending" or not m["main"]:
            continue
        for w, cells in m["main"]["readers"].items():
            for label, c in cells.items():
                lines.append(f"| {m['target']} | {READER_NAME[w]} | {label} | {c['n']} | {c['S_whole'][0]:.2f} | "
                             f"{c['S_no_part'][0]:.2f} | {c['S_no_rand'][0]:.2f} | {fmt(c['excess'])} | "
                             f"{'yes' if c['valid'] else 'no'} |")  # fmt: skip
            vs = m["main"]["vs_random_atoms"].get(w)
            if vs:
                lines.append(f"| {m['target']} | {READER_NAME[w]} | switches lost: 26-100 minus random atoms | | | | | "
                             f"{fmt(vs)} | |")  # fmt: skip
    lines += ["", "Each slice's share of ||Δ||^2 (median over items), the 26-100 vs 1-25 check (dumbest way 1: items "
              "where 26-100 holds more than 1-25; items where per atom 26-100 holds less, i.e. OMP order is a quality "
              "order), the random atoms' own share and scale alpha, and the mean cos^2 with U (dumbest way 3; "
              "||P U||_F^2 / rank U).", "",
              "| model | scenes | n | 1-25 | 26-100 | 1-100 | random atoms (own) | alpha: median; items > 1 | items "
              "26-100 > 1-25 | items per-atom order holds | cos^2 U: 1-25 | 1-100 | 26-100 | random atoms |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for m in models:
        if m["status"] == "pending":
            continue
        for where, s in m["shares"].items():
            if not s["n"]:
                continue
            lines.append(f"| {m['target']} | {where} | {s['n']} | {f3(s['median_share_1_25'])} | "
                         f"{f3(s['median_share_26_100'])} | {f3(s['median_share_1_100'])} | "
                         f"{f3(s['median_share_ratoms75own'])} | {f3(s['median_ratoms75_alpha'])}; {s['alpha_above_1']} | "
                         f"{s['items_26_100_above_1_25']} | {s['items_per_atom_order_holds']} | "
                         f"{f3(s['mean_cos2_U_jpp25'])} | {f3(s['mean_cos2_U_jpp100'])} | "
                         f"{f3(s['mean_cos2_U_jpp26_100'])} | {f3(s['mean_cos2_U_ratoms75'])} |")  # fmt: skip
    lines += ["", "Labels: " + "; ".join(f"{m['target']}: {m['label']} ({m.get('why', '')})" for m in models) + ".",
              "If (c) holds on the 27B: its K = 100 loss is a size effect of the whole removal, and the 27B stays "
              "\"misses the strict rule, cause not found\" (the spec's reading)."]  # fmt: skip
    return lines


def item_rows(models: list[dict]) -> list[dict]:
    """Per item and scene set, each slice's share of the change, alpha and the cos^2 with U (the per-item report)."""
    keys = ("share_1_25", "share_26_100", "share_1_100", "share_ratoms75own", "ratoms75_alpha", "cos2_U_jpp25",
            "cos2_U_jpp100", "cos2_U_jpp26_100", "cos2_U_ratoms75")  # fmt: skip
    out = []
    for m in models:
        if m["status"] == "pending":
            continue
        rsrc, msrc = _run_dir(R.EXP, m["runs"][0]), _run_dir(X.EXP, m["runs"][1])
        for where, recs in (("routes C2", [r for r in X.read_jsonl(rsrc / "norms.jsonl") if r.get("condition") == "C2"]),
                            ("main test", X.read_jsonl(msrc / "atoms.jsonl"))):  # fmt: skip
            out += [{"model": m["target"], "scenes": where, "scene": r["scene"], **{k: r.get(k) for k in keys}}
                    for r in recs]  # fmt: skip
    return out


def marked(decode, ids: list[int], pos: int) -> str:
    return R.marked(decode, ids, pos)


def example_lines(target: str, routes_run: str, main_run: str, decode, k: int = X.K_EXAMPLES,
                  seed: int = X.EXAMPLES_SEED) -> list[str]:  # fmt: skip
    """The verify-pack view of one model: k random items (seed) of each run, each reader's prompt as the model reads
    it with the patch position in ⟦...⟧ (the read appends the digit's space token), and every arm's answer (the top
    token at the read; the routes lookup's route; the main test's greedy text where the run kept one)."""
    lines = [f"## {target}", ""]
    for exp, run in ((R.EXP, routes_run), (X.EXP, main_run)):
        src = _run_dir(exp, run)
        rows = X.read_jsonl(src / "outcomes.jsonl")
        if exp == X.EXP:
            layer = json.loads((src / "manifest.json").read_text())["predicted"]
            rows = [r for r in rows if r.get("rendering") == "chat" and r["layer"] == layer]
        cases = {c["scene"]: c for c in X.read_jsonl(src / "cases.jsonl") if c.get("rendering", "chat") == "chat"}
        greedy = {(g["scene"], g["reader"], g["arm"]): g["greedy"] for g in X.read_jsonl(src / "examples.jsonl")}
        items = list(dict.fromkeys(r["scene"] for r in rows))
        what = "routes test, another item moved (C2)" if exp == R.EXP else "main test (two people swap picks)"
        lines += [f"### {what}: {run}, {min(k, len(items))} random items of {len(items)} (seed {seed})", ""]
        for i in sorted(random.Random(seed).sample(range(len(items)), min(k, len(items)))):
            c = cases[items[i]]
            lines += [f"#### {c['scene']}: bridge {c['bridge']} → {c['cf_bridge']}, token {c['pos']}"
                      + (f"; expected digits {c['expect']}" if "expect" in c else ""), ""]  # fmt: skip
            for w, rd in c["readers"].items():
                mine = [r for r in rows if r["scene"] == c["scene"] and r["reader"] == w]
                lines += [f"**{READER_NAME[w]}**: O's answer {rd['answer']}, S's answer {rd['cf_answer']}", "", "O, as read:",
                          "", "```", marked(decode, rd["ids"]["org"], c["pos"]), "```", "",
                          "| arm | answer (top token) | route | switched | greedy |", "|---|---|---|---|---|"]  # fmt: skip
                for r in mine:
                    arm = r["arm"] if exp == R.EXP or r["arm"] in ("none", "whole") else (
                        f"{r['arm']} {r['dict']}/{r['k']}/{r['omp']}")  # fmt: skip
                    # X0 keeps greedy texts of its example items under "<dict>/<k>/<fit>/<arm>" (whole: "-/0/-/whole")
                    g = (greedy.get((c["scene"], w, "/".join(map(str, (r["dict"], r["k"], r["omp"], r["arm"])))))
                         if exp == X.EXP else None)  # fmt: skip
                    lines.append(f"| {arm} | {decode([r['top']])!r} | {r.get('route') or ''} | {r['switched']} | "
                                 f"{'' if g is None else repr(g)} |")  # fmt: skip
                lines.append("")
    return lines


def stage_verdict(n_boot: int = X.N_BOOT, decode_for=None) -> Path:
    answer = require_answer(QUESTION)
    models = [model_result(t, ROUTES_RUNS[t], MAIN_RUNS[t], n_boot) for t in MODELS]
    batch = batch_rule(models)
    out = RESULTS / f"x47_1-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    lines = verdict_lines(models, batch, answer, n_boot)
    (out / "x47_1.json").write_text(json.dumps({"dan": answer, "batch": batch, "models": models}, indent=1) + "\n")
    (out / "x47_1.md").write_text("\n".join(lines) + "\n")
    items = item_rows(models)
    if items:
        with (out / "x47_1_items.csv").open("w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(items[0]))
            wr.writeheader()
            wr.writerows(items)
    ex = ["# 47.1 verify pack: prompts as the model reads them (the read appends the digit's space token); ⟦...⟧ the "
          "bridge word, where the change (or the arm's part of it) is added at L. UNVERIFIED.", ""]  # fmt: skip
    for m in models:
        if m["status"] != "pending":
            ex += example_lines(m["target"], *m["runs"], decode=(decode_for or default_decode)(m["target"]))
    (out / "examples.md").write_text("\n".join(ex) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def default_decode(target: str):
    from bridge_jspace.review import checks as RC

    tk = RC.tokenizer(target)
    return lambda ids: tk.decode([int(t) for t in ids], skip_special_tokens=False)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["verdict"])
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    stage_verdict(a.n_boot)


if __name__ == "__main__":
    main()
