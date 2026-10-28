"""x47_depth_cpu (batch 47 amendment 3, D4: depth from cached states; jobs/c3/batch47.yaml D4, rules verbatim; Q-depth
in predictions/2026-10-28_dan.md). CPU only, from a 47.8 run's files (scripts/x47_anatomy.py: cache/bases.npz,
cache/fit_states.npz, fit.json, norms.jsonl, cases.jsonl) and its verdict folder.

Stages (each refuses until the predictions file holds Dan's committed Q-depth answer at HEAD):
  persistence   Is the address one code across depth? For every pair of sweep layers the principal angles between U_l
                and U_l' (mean cos^2 = ||U_l^T U_l'||_F^2 / min(rank)); the window = the sweep layers where the slot
                probe is >= 0.8. Rule (D4, verbatim): "persistent" if the mean cos^2 >= 0.5 across the window (over
                every pair of window layers), "re-encoded" if it drops below 0.2 between adjacent sampled layers (of the
                window); neither: "mixed". The same for I_l, read as Id_l (the fit half's entity mass-mean basis, the
                subspace behind each scene's rank-1 I part) over the window where the identity probe is >= 0.8.
  embedding     When does the lens's identity stop being the embedding? Per layer the median over test scenes of the
                share of the W_E-25 part of Delta inside the J++-25 atoms' span, and of the J++ part inside the W_E
                atoms' (norms.jsonl); the overlap = the larger of the two medians; the first sweep layer where it falls
                below 0.2, compared with l_J from the 47.8 verdict (pending without one).
  binding       Forward binding by layer (48.3's probe): at each cached locker sentence's item token and number token,
                a ridge probe (x0_probe's, entities = the items held out) for which person picked that item (3 classes,
                chance 1 / 3), per cached layer. 47.8's scenes are all locker-first, so this is 48.3's control by
                construction (the sentence precedes the picks and must sit at chance); the locker-after half needs the
                48.3 / D1 jobs' own cache and is reported "pending" here.
  table         The cross-track alignment table: per model l_probe, l_P, l_J (the 47.8 verdict), l_R per reader (D2:
                --lr-json {"<target>": {"lookup": l, "recall": l}}, else pending), Zach's mid and late bands
                (docs/breadth/README.md), D4's persistence label and the embedding layer.

uv run python scripts/x47_depth_cpu.py persistence --runs qwen35_9b_x47_anatomy
uv run python scripts/x47_depth_cpu.py embedding --runs qwen35_9b_x47_anatomy --verdict results/x47_anatomy/x47_8-<UTC>
uv run python scripts/x47_depth_cpu.py binding --runs qwen35_9b_x47_anatomy
uv run python scripts/x47_depth_cpu.py table --runs ... --verdict results/x47_anatomy/x47_8-<UTC> [--lr-json FILE]
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_necessity as X
from scripts import x0_probe as PR
from scripts import x47_anatomy as A

EXP = "x47_depth_cpu"
RESULTS = pins.RESULTS_DIR / EXP
QUESTION = "Q-depth"
PERSIST_BAR, REENCODE_BAR, PROBE_BAR, OVERLAP_BAR = 0.5, 0.2, 0.8, 0.2
EPS = A.EPS
# Zach's bands (docs/breadth/README.md, Section 3 and the summary table; amendment 57 for the 9B's late band)
BANDS = {"qwen3.6-27b": {"mid": (32, 40), "late": (52, 60)}, "qwen3.5-9b": {"mid": (12, 16), "late": (26, 29)},
         "muse-glimmer-30b": {"mid": (36, 42), "late": (36, 42)}}  # fmt: skip
BANDS_SOURCE = "docs/breadth/README.md (Section 3's late-band table; the summary table's band per model)"
TOKEN_KINDS = ("item", "number")


def unsealed() -> str:
    answer = A.dan_answer(question=QUESTION)
    assert answer, f"sealed: {A.PREDICTIONS} has no committed answer to {QUESTION} (its 'Dan:' line is empty at HEAD)"
    return answer


# ---- (1) persistence ----------------------------------------------------------------------------------------------


def mean_cos2(a: np.ndarray, b: np.ndarray) -> float:
    """The mean squared cosine of the principal angles between the column spaces of a and b ([d, r], orthonormal):
    ||a^T b||_F^2 / min(rank a, rank b); 0 when either is empty."""
    r = min(a.shape[1], b.shape[1])
    return float(((a.T.astype(np.float64) @ b.astype(np.float64)) ** 2).sum() / r) if r else 0.0


def persistence_label(cos2: dict[tuple[int, int], float], window: list[int]) -> dict[str, Any]:
    """D4's rule on one basis: over the window's layers, persistent if the mean cos^2 over every pair >= PERSIST_BAR;
    re-encoded if it drops below REENCODE_BAR between adjacent window layers; both (or neither): mixed / not tested."""
    pairs = [(a, b) for i, a in enumerate(window) for b in window[i + 1 :]]
    if not pairs:
        return {"label": "not tested", "why": f"the window holds {len(window)} layer(s)", "window": window}
    mean = float(np.mean([cos2[p] for p in pairs]))
    adjacent = {f"{a}-{b}": cos2[(a, b)] for a, b in itertools.pairwise(window)}
    drop = [k for k, v in adjacent.items() if v < REENCODE_BAR - EPS]
    persistent, reencoded = mean >= PERSIST_BAR - EPS, bool(drop)
    label = "persistent" if persistent and not reencoded else "re-encoded" if reencoded and not persistent else "mixed"
    return {"label": label, "mean_cos2": mean, "adjacent": adjacent, "drops": drop, "window": window,
            "why": f"mean cos^2 over {len(pairs)} window pairs = {mean:.3f}; adjacent drops below {REENCODE_BAR}: {drop or 'none'}"}  # fmt: skip


def probe_window(fit: dict[str, Any], target: str, bar: float = PROBE_BAR) -> list[int]:
    """The sweep layers where the named probe's accuracy is >= bar."""
    return sorted(int(la) for la, f in fit["per_layer"].items() if f["probes"][target]["probe"][0] >= bar - EPS)


def persistence_of(bases: dict[str, np.ndarray], fit: dict[str, Any], layers: list[int]) -> dict[str, Any]:
    out: dict[str, Any] = {"layers": layers}
    for key, probe in (("U", "locker sentence"), ("Id", "bridge identity")):
        mats = {la: bases[f"{key}_L{la}"].astype(np.float64) for la in layers}
        cos2 = {(a, b): mean_cos2(mats[a], mats[b]) for i, a in enumerate(layers) for b in layers[i:]}
        full = {(b, a): v for (a, b), v in cos2.items()}
        cos2.update(full)
        out[key] = {"rank": {str(la): int(mats[la].shape[1]) for la in layers}, "probe": probe,
                    "matrix": [[round(cos2[(a, b)], 4) for b in layers] for a in layers],
                    **persistence_label(cos2, probe_window(fit, probe))}  # fmt: skip
    return out


# ---- (2) lens identity vs the embedding --------------------------------------------------------------------------


def embedding_of(norms: list[dict], layers: list[int], l_j: int | None) -> dict[str, Any]:
    per = {}
    for la in layers:
        mine = [n for n in norms if n["layer"] == la]
        we_in_j = float(np.median([n["WE_inside_J"] for n in mine])) if mine else float("nan")
        j_in_we = float(np.median([n["J_inside_WE"] for n in mine])) if mine else float("nan")
        per[str(la)] = {"n": len(mine), "WE_inside_J": we_in_j, "J_inside_WE": j_in_we, "overlap": max(we_in_j, j_in_we),
                        "share_WE": float(np.median([n["share_WE"] for n in mine])) if mine else float("nan"),
                        "share_J": float(np.median([n["share_J"] for n in mine])) if mine else float("nan")}  # fmt: skip
    below = next((la for la in layers if per[str(la)]["overlap"] < OVERLAP_BAR - EPS), None)
    return {"per_layer": per, "layer_below": below, "l_J": l_j,
            "vs_l_J": None if below is None or l_j is None else below - l_j,
            "reading": ("the lens reads the token (embedding) at every sweep layer" if below is None else
                        f"the overlap falls below {OVERLAP_BAR} at L{below}" + ("" if l_j is None else f"; l_J = L{l_j} ({below - l_j:+d} layers)"))}  # fmt: skip


# ---- (3) forward binding by layer --------------------------------------------------------------------------------


def person_labels(cases: list[dict]) -> list[list[str]]:
    """Per fit case, per locker slot (context order): the person who picked that slot's item."""
    from scripts import x6_routes as R
    from scripts import x8_write as W

    out = []
    for c in cases:
        picked = {item: person for person, item in R.PICK.findall(c["context"])}
        out.append([picked[item] for item, _ in W.slots_of(c["context"])])
    return out


def binding_of(states: dict[str, np.ndarray], cases: list[dict], layers: list[int], n_boot: int) -> dict[str, Any]:
    """The person probe per cached layer and token kind over every locker sentence of the cached fit cases (rows =
    case x slot; entities = the slot's item, held out by x0_probe's grouped folds)."""
    labels = person_labels(cases)
    out: dict[str, Any] = {"layers": layers, "n_cases": len(cases), "order": "locker-first (48.3's control)",
                           "locker_after": "pending: 47.8's scenes are all locker-first; the locker-after half needs the 48.3 / D1 cache"}  # fmt: skip
    for la in layers:
        h = states[f"locker_L{la}"].astype(np.float64)  # [n, 3, 2, d]
        n = h.shape[0]
        items = [{"scene": f"{cases[i]['scene']}|{k}", "entity": slot_item(cases[i], k), "person": labels[i][k]}
                 for i in range(n) for k in range(3)]  # fmt: skip
        rec = {}
        for t, kind in enumerate(TOKEN_KINDS):
            x = h[:, :, t, :].reshape(n * 3, -1)
            rec[kind] = person_probe(x, items, n_boot)
        out[str(la)] = rec
    out["first_at_bar"] = {kind: next((la for la in layers if out[str(la)][kind]["probe"][0] >= PROBE_BAR - EPS), None)
                           for kind in TOKEN_KINDS}  # fmt: skip
    return out


def slot_item(c: dict, k: int) -> str:
    from scripts import x8_write as W

    return W.slots_of(c["context"])[k][0]


def person_probe(x: np.ndarray, items: list[dict], n_boot: int) -> dict[str, Any]:
    """x0_probe's ridge probe for the person (entities = items held out), with its majority baseline and cluster
    bootstrap over the items."""
    y = [it["person"] for it in items]
    ents = [it["entity"] for it in items]
    pred, outer, chosen = PR.cv_predict(x, y, ents, True)
    right = {"probe": [int(p == t) for p, t in zip(pred, y, strict=True)],
             "majority": [int(p == t) for p, t in zip(PR.baseline(y, outer), y, strict=True)]}  # fmt: skip
    r = X.resampled_rates(right, ents, n_boot)
    return {"n": len(y), "entities": len(set(ents)), "classes": len(set(y)), "chance": round(1 / len(set(y)), 4),
            "penalties": chosen, **{k: [float(np.mean(v)), *X.interval(r[k])] for k, v in right.items()}}  # fmt: skip


# ---- (4) the cross-track alignment table ------------------------------------------------------------------------


def band_text(band: tuple[int, int]) -> str:
    return f"L{band[0]}-{band[1]}"


def table_rows(verdict: dict | None, lr: dict[str, dict], d4: dict[str, dict]) -> list[dict[str, Any]]:
    """One row per model: l_probe, l_P, l_J from the 47.8 verdict, l_R per reader (D2), Zach's bands, D4's labels."""
    rows = []
    models = {m["target"]: m for m in (verdict or {}).get("models", [])}
    for target in A.RUNS:
        m = models.get(target)
        r = m["rules"] if m and m.get("status") == "tested" else None
        p = d4.get(target, {})
        rows.append({"model": target, "l_probe": r["l_probe"] if r else "pending", "l_P": r["l_P"] if r else "pending",
                     "l_J": r["l_J"] if r else "pending", "l_R_lookup": lr.get(target, {}).get("lookup", "pending"),
                     "l_R_recall": lr.get(target, {}).get("recall", "pending"),
                     "mid_band": band_text(BANDS[target]["mid"]), "late_band": band_text(BANDS[target]["late"]),
                     "address": p.get("persistence", {}).get("U", {}).get("label", "pending"),
                     "identity": p.get("persistence", {}).get("Id", {}).get("label", "pending"),
                     "embedding_below": p.get("embedding", {}).get("layer_below", "pending"),
                     "n_layers": pins.TARGETS[target]["n_layers"]})  # fmt: skip
    return rows


def table_lines(rows: list[dict[str, Any]]) -> list[str]:
    head = "| model | depth | l_probe (address formed) | l_P (address used) | l_J (lookup leaves the lens) | l_R lookup | l_R recall | Zach mid band | Zach late band | address across depth (D4) | identity subspace (D4) | lens = embedding until |"
    lines = [head, "|" + "---|" * 12]
    for r in rows:
        lines.append(f"| {r['model']} | {r['n_layers']} | {r['l_probe']} | {r['l_P']} | {r['l_J']} | {r['l_R_lookup']} | {r['l_R_recall']} | "
                     f"{r['mid_band']} | {r['late_band']} | {r['address']} | {r['identity']} | {r['embedding_below']} |")  # fmt: skip
    return lines


# ---- stages -------------------------------------------------------------------------------------------------------


def load_run(run: str) -> dict[str, Any]:
    src = A.RESULTS / run
    assert (src / "fit.json").exists(), f"{run}: no 47.8 fit record here"
    assert (src / "cache" / "bases.npz").exists(), f"{run}: no 47.8 cache here"
    m = json.loads((src / "manifest.json").read_text())
    return {"run": run, "target": m["model"]["target"], "layers": [int(x) for x in m["layers"]], "manifest": m,
            "fit": json.loads((src / "fit.json").read_text()), "src": src}  # fmt: skip


def out_dir(stage: str) -> Path:
    out = RESULTS / f"{stage}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    out.mkdir(parents=True)
    return out


def verdict_rules(verdict_dir: Path | None) -> dict[str, dict]:
    if verdict_dir is None or not (verdict_dir / "x47_8.json").exists():
        return {}
    blob = json.loads((verdict_dir / "x47_8.json").read_text())
    return {m["target"]: m["rules"] for m in blob["models"] if m.get("status") == "tested"}


def stage_persistence(runs: list[str]) -> Path:
    answer = unsealed()
    out = out_dir("persistence")
    res, lines = {}, [f"# D4 (1): is the address one code across depth? ({QUESTION}, Dan: {answer}). UNVERIFIED.", "",
                      f"Rule (D4, verbatim): persistent if the mean cos^2 of the principal angles >= {PERSIST_BAR} across the window "
                      f"where the slot probe is >= {PROBE_BAR}; re-encoded if it drops below {REENCODE_BAR} between adjacent sampled "
                      "layers. The same for I_l, read as the fit half's entity mass-mean basis Id_l over the identity probe's window.", "",
                      "| model | basis | rank | window | mean cos^2 | adjacent drops | label |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for run in runs:
        r = load_run(run)
        bases = dict(np.load(r["src"] / "cache" / "bases.npz"))
        p = persistence_of(bases, r["fit"], r["layers"])
        res[r["target"]] = {"run": run, **p}
        for key in ("U", "Id"):
            b = p[key]
            ranks = sorted(set(b["rank"].values()))
            lines.append(f"| {r['target']} | {key} | {ranks} | {b['window']} | {b.get('mean_cos2', float('nan')):.3f} | "
                         f"{b.get('drops') or 'none'} | {b['label']} |")  # fmt: skip
    (out / "persistence.json").write_text(json.dumps({"dan": answer, "models": res}, indent=1) + "\n")
    (out / "persistence.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_embedding(runs: list[str], verdict_dir: Path | None) -> Path:
    answer = unsealed()
    out = out_dir("embedding")
    rules = verdict_rules(verdict_dir)
    res, lines = {}, [f"# D4 (2): when does the lens's identity stop being the embedding? ({QUESTION}, Dan: {answer}). UNVERIFIED.", "",
                      "Per layer the median over test scenes of the W_E-25 part of Delta inside the J++-25 atoms' span and of the "
                      f"J++ part inside the W_E atoms'; overlap = the larger; the first sweep layer below {OVERLAP_BAR} against l_J.", "",
                      "| model | layer | n | W_E inside J++ | J++ inside W_E | overlap | share J++ | share W_E |", "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for run in runs:
        r = load_run(run)
        norms = X.read_jsonl(r["src"] / "norms.jsonl")
        l_j = rules.get(r["target"], {}).get("l_J")
        e = embedding_of(norms, r["layers"], l_j)
        res[r["target"]] = {"run": run, **e}
        for la, v in e["per_layer"].items():
            lines.append(f"| {r['target']} | {la} | {v['n']} | {v['WE_inside_J']:.3f} | {v['J_inside_WE']:.3f} | {v['overlap']:.3f} | "
                         f"{v['share_J']:.3f} | {v['share_WE']:.3f} |")  # fmt: skip
    lines += ["", *[f"- {t}: {v['reading']}" + ("" if v["l_J"] is not None else " (l_J pending: no 47.8 verdict given)")
                    for t, v in res.items()]]  # fmt: skip
    (out / "embedding.json").write_text(json.dumps({"dan": answer, "models": res}, indent=1) + "\n")
    (out / "embedding.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_binding(runs: list[str], n_boot: int) -> Path:
    answer = unsealed()
    out = out_dir("binding")
    res, lines = {}, [f"# D4 (3): forward binding by layer, 48.3's person probe on the cached locker-sentence tokens ({QUESTION}, Dan: {answer}). UNVERIFIED.", "",
                      "47.8's scenes are locker-first: the control by construction (the sentence precedes the picks; chance 1/3). "
                      "The locker-after half is pending (the 48.3 / D1 cache).", "",
                      "| model | layer | token | n | probe | majority | chance |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    for run in runs:
        r = load_run(run)
        states = dict(np.load(r["src"] / "cache" / "fit_states.npz"))
        cached = [int(x) for x in r["manifest"]["cache"]["layers_locker"]]
        fit_cases = [c for c in X.read_jsonl(r["src"] / "cases.jsonl") if c["half"] == "fit"]
        n_lock = states[f"locker_L{cached[0]}"].shape[0]
        b = binding_of(states, fit_cases[:n_lock], cached, n_boot)
        res[r["target"]] = {"run": run, **b}
        for la in cached:
            for kind in TOKEN_KINDS:
                v = b[str(la)][kind]
                lines.append(
                    f"| {r['target']} | {la} | {kind} | {v['n']} | {A.fmt(v['probe'])} | {A.fmt(v['majority'])} | {v['chance']} |"
                )
        lines.append(f"| {r['target']} | first at {PROBE_BAR} | | | {b['first_at_bar']} | | |")
    (out / "binding.json").write_text(json.dumps({"dan": answer, "models": res}, indent=1) + "\n")
    (out / "binding.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def stage_table(runs: list[str], verdict_dir: Path | None, lr_json: Path | None, n_boot: int) -> Path:
    answer = unsealed()
    out = out_dir("table")
    verdict = (
        json.loads((verdict_dir / "x47_8.json").read_text())
        if verdict_dir and (verdict_dir / "x47_8.json").exists()
        else None
    )
    lr = json.loads(lr_json.read_text()) if lr_json else {}
    rules = verdict_rules(verdict_dir)
    d4: dict[str, dict] = {}
    for run in runs:
        if not (A.RESULTS / run / "fit.json").exists():
            continue
        r = load_run(run)
        bases = dict(np.load(r["src"] / "cache" / "bases.npz"))
        norms = X.read_jsonl(r["src"] / "norms.jsonl")
        d4[r["target"]] = {"persistence": persistence_of(bases, r["fit"], r["layers"]),
                           "embedding": embedding_of(norms, r["layers"], rules.get(r["target"], {}).get("l_J"))}  # fmt: skip
    rows = table_rows(verdict, lr, d4)
    lines = [f"# D4 (4): the cross-track alignment table ({QUESTION}, Dan: {answer}). UNVERIFIED.", "",
             f"l_probe / l_P / l_J from the 47.8 verdict ({verdict_dir or 'pending'}); l_R from D2 ({lr_json or 'pending'}); "
             f"Zach's bands from {BANDS_SOURCE}; the D4 labels from this run's cached bases and norms.", "", *table_lines(rows)]  # fmt: skip
    (out / "table.json").write_text(
        json.dumps({"dan": answer, "rows": rows, "d4": d4, "verdict": str(verdict_dir), "lr": lr}, indent=1) + "\n"
    )
    (out / "table.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["persistence", "embedding", "binding", "table"])
    ap.add_argument(
        "--runs", nargs="+", default=list(A.RUNS.values()), help="the 47.8 runs (results/x47_anatomy/<run>)"
    )
    ap.add_argument("--verdict", type=Path, help="the 47.8 verdict folder (l_J, l_P, l_probe)")
    ap.add_argument("--lr-json", type=Path, help='D2s l_R per model: {"<target>": {"lookup": l, "recall": l}}')
    ap.add_argument("--n-boot", type=int, default=X.N_BOOT)
    a = ap.parse_args()
    runs = [r for r in a.runs if (A.RESULTS / r / "fit.json").exists()] if a.stage != "table" else a.runs
    if a.stage == "persistence":
        stage_persistence(runs)
    elif a.stage == "embedding":
        stage_embedding(runs, a.verdict)
    elif a.stage == "binding":
        stage_binding(runs, a.n_boot)
    else:
        stage_table(runs, a.verdict, a.lr_json, a.n_boot)


if __name__ == "__main__":
    main()
