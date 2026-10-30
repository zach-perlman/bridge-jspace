"""paper_swap_6b (Zach, 2026-10-30, prereg amendment 65 second addendum, note 39): the overlap diagnostic and arm 6b.

In note 39's 9B and Lightning runs the A1 guard failed on arm 6 (a same-domain category, e.g. languages for capitals).
The hypothesis (untested): those spans overlap the intermediate's own directions, so arm 6 also removes the bridge.

overlap  (descriptive; lens files only, no forward pass: the unembedding rows and the final norm's gain are read from the
         checkpoint's safetensors, the J++ from its file, the vectors computed as JLens.vectors). For each closed-vocabulary
         item and main-band layer, the share of the bridge atoms' energy (intermediate and swap_to unit J++ vectors; the
         mean of the two rows' squared projections) inside:
           A (the item's scrub set); arm 6's span (note 39's off set); each unrelated-pool category span (colour, shape,
           unit, occupation, weekday, month, number, state of matter; never the item's own answer type), both full (the
           category's first tokens minus A and the name tokens) and count-matched to A (the set arm 6b would use);
           20 random letter-token spans of A's size (random.Random('n39ov:<target>:<item>:<k>'); never A or a name token).
         Arm 6b's category: the pool category whose COUNT-MATCHED span has the smallest share (mean over main-band layers;
         ties by the pool order), its tokens count-matched to A: subsampled with random.Random('n39b:' + item), or padded
         from random letter tokens with the same generator. Written to <run>/overlap.json, frozen for `rerun`.
rerun    note 39's arms 1 (bridge), 3 (bridge_noA), 6b (bridge_off6b: arm 3 with arm 6b's span) and 7 (bridge_randA) and
         arm 1's matched-norm null, on the finished note 39 run's eligible primary items, at the main band and at arm 1's
         median-onset window (the reader's rule on that run's rows, per lens). Same code paths as paper_swap_decomp
         (imported, unchanged: its gate, atoms, clamps, seeds, batched first-token read); each window's batch is
         padded with unedited rows to note 39's 12-row shape, so the stored rows reproduce exactly (9B smoke: bit-identical). Arms 1, 3, 7 and the null are
         checked against the stored note 39 rows (check.json: identical flips and ranks, max |delta log p| difference).

python scripts/paper_swap_6b.py overlap --name N
python scripts/paper_swap_6b.py rerun --name N --why W --prev NOTE39_RUN --overlap OVERLAP_RUN [--items A B ... | --limit K]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import statistics
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from scripts import paper_swap_decomp as D  # noqa: E402

POOL = ("colour", "shape", "unit", "occupation", "weekday", "month", "number", "state_of_matter")
N_RAND = 20
ARM6B = "bridge_off6b"
RERUN_ARMS = ("bridge", "bridge_noA", ARM6B, "bridge_randA")
RERUN_NULLS = ("bridge",)
CHECKED = ("bridge", "bridge_noA", "bridge_randA")  # plus the bridge null


# ---- lens vectors without the model -----------------------------------------------------------------------------


class _Head:
    def __init__(self, weight):
        self.weight = weight


class _Hf:
    def __init__(self, weight):
        self.lm_head = _Head(weight)


class LensOnly:
    """What JLens needs from the model (the unembedding rows and the final norm's gain), from the safetensors."""

    def __init__(self, device: str):
        from huggingface_hub import snapshot_download
        from safetensors import safe_open

        t = pins.TARGETS[pins.TARGET]
        path = Path(snapshot_download(pins.MODEL_REPO, revision=pins.MODEL_REVISION, local_files_only=True, ignore_patterns=t.get("snapshot_ignore")))
        index = json.loads(next(path.glob("*.index.json")).read_text())["weight_map"]
        norm_keys = [k for k in ("model.language_model.norm.weight", "model.norm.weight", "backbone.norm_f.weight") if k in index]
        assert "lm_head.weight" in index and len(norm_keys) == 1, f"lm_head / final norm keys not found: {norm_keys}"

        def get(key):
            with safe_open(str(path / index[key]), framework="pt", device="cpu") as f:
                return f.get_tensor(key)

        self.hf = _Hf(get("lm_head.weight").to(device))  # bf16, as the loaded model's
        w = get(norm_keys[0]).to(device).float()
        self._gain = 1.0 + w if t["norm_gain"] == "one_plus_weight" else w
        self.norm_key = norm_keys[0]

    def norm_gain(self) -> torch.Tensor:
        return self._gain


def letter_ids(tokenizer, vocab: int) -> list[int]:
    """model.letter_token_ids() without the model: non-special ids (of the lm_head's range) whose decode has a letter."""
    from bridge_jspace.model import _HAS_LETTER

    decoded = tokenizer.batch_decode([[i] for i in range(vocab)])
    special = frozenset(tokenizer.all_special_ids) | frozenset(int(i) for i in tokenizer.added_tokens_decoder)
    return [i for i, s in enumerate(decoded) if i not in special and _HAS_LETTER.search(s)]


def count_matched(cat_tokens: list[int], n: int, barred: set[int], letters: list[int], item: str) -> tuple[list[int], int]:
    """Arm 6b's rule: the category's tokens (minus barred) subsampled to n with Random('n39b:' + item), or all of them
    padded from random letter tokens with the same generator. Returns (tokens, number padded)."""
    rng = random.Random("n39b:" + item)
    pool = sorted(set(cat_tokens) - barred)
    if len(pool) >= n:
        return sorted(rng.sample(pool, n)), 0
    pad = sorted(set(letters) - barred - set(pool))
    return sorted(pool + rng.sample(pad, n - len(pool))), n - len(pool)


def shares(V: torch.Tensor, B: torch.Tensor) -> float:
    """Mean over B's unit rows of the squared norm of their projection onto span(V's rows); the span's basis is
    rank-revealing as nn_swap's basis() (singular values above 1e-6 of the largest), via the Gram matrix in double."""
    V, B = V.double(), B.double()
    lam, U = torch.linalg.eigh(V @ V.T)
    keep = lam > lam.max() * 1e-12
    c = U[:, keep].T @ (V @ B.T)  # [r, 2]
    return float(((c**2) / lam[keep, None]).sum(0).mean())


@torch.no_grad()
def overlap(a) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.tokens import concept_token, load_tokenizer

    target = pins.TARGET
    pins.check_run_name(a.name)
    out_dir = D.RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    out_dir.mkdir(parents=True, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    vocab = D.load_vocab()
    lens_name = "jpp"
    manifest = {"exp": D.EXP, "run": a.name, "kind": "overlap", "note": "prereg amendment 65 second addendum, note 39", "target": target,
                "lens": {lens_name: list(pins.LENS_SOURCES[lens_name])}, "vocabulary_sha256": D.VOCAB_SHA256, "main_band": D.wname(*D.MAIN_BAND[target]),
                "pool": list(POOL), "n_rand": N_RAND, "device": device, "command": " ".join(sys.argv), "git_state": pins.git_state(),
                "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    t0 = time.time()
    lm = LensOnly(device)
    lens = JLens(lm, lens_name)
    tok = load_tokenizer()
    letters = letter_ids(tok, lm.hf.lm_head.weight.shape[0])
    print(f"[{a.name}] lens and unembedding loaded ({lm.norm_key}), {len(letters)} letter tokens, {time.time() - t0:.0f}s", flush=True)
    layers = list(range(D.MAIN_BAND[target][0], D.MAIN_BAND[target][1] + 1))
    tt = {cat: [int(i) for i in vocab["type_tokens"][target][cat]] for cat in POOL}
    vec = lambda la, ids: lens.vectors(la, torch.tensor(ids, device=device))  # noqa: E731
    items_out: dict = {}
    for name, row in vocab["items"].items():
        if not row["closed_vocabulary"]:
            continue
        it = next(x for x in D_items() if x["name"] == name)
        toks = row["tokens"][target]
        scrub, excluded = toks["scrub"], toks["excluded"]
        n = len(scrub)
        barred = set(scrub) | set(excluded)
        try:
            bt = [concept_token(tok, it["intermediate"]), concept_token(tok, it["swap_to"])]
        except ValueError:
            items_out[name] = {"skipped": "no single-token intermediate or swap_to"}
            continue
        pool = [c for c in POOL if c != row["answer_type"]]
        cm = {c: count_matched(tt[c], n, barred, letters, name) for c in pool}
        full = {c: sorted(set(tt[c]) - barred) for c in pool}
        rpool = sorted(set(letters) - barred)
        rand = [sorted(random.Random(f"n39ov:{target}:{name}:{k}").sample(rpool, n)) for k in range(N_RAND)]
        per_layer = {}
        for la in layers:
            B = vec(la, bt)
            r = {"A": shares(vec(la, scrub), B), "arm6": shares(vec(la, toks["off"]), B)}
            r.update({f"cm:{c}": shares(vec(la, cm[c][0]), B) for c in pool})
            r.update({f"full:{c}": shares(vec(la, full[c]), B) for c in pool if full[c]})
            r["rand"] = [shares(vec(la, s), B) for s in rand]
            per_layer[la] = r
        mean = {k: statistics.mean(per_layer[la][k] for la in layers) for k in per_layer[layers[0]] if k != "rand"}
        mean["rand_mean"] = statistics.mean(statistics.mean(per_layer[la]["rand"]) for la in layers)
        mean["rand_max"] = statistics.mean(max(per_layer[la]["rand"]) for la in layers)
        rand_item = [statistics.mean(per_layer[la]["rand"][k] for la in layers) for k in range(N_RAND)]
        pick = min(pool, key=lambda c: (mean[f"cm:{c}"], POOL.index(c)))
        items_out[name] = {
            "set": D.item_set(vocab, name, target), "answer_type": row["answer_type"], "n_A": n, "bridge_tokens": bt,
            "per_layer": per_layer, "mean": mean, "rand_per_span_mean": rand_item,
            "arm6_above_all_random": mean["arm6"] > max(rand_item),
            "arm6b": {"category": pick, "tokens": cm[pick][0], "padded": cm[pick][1], "share": mean[f"cm:{pick}"],
                      "above_all_random": mean[f"cm:{pick}"] > max(rand_item)},
        }  # fmt: skip
    blob = {"manifest": manifest, "items": items_out}
    (out_dir / "overlap.json").write_text(json.dumps(blob, indent=1) + "\n")
    summ = summarize(items_out)
    summ["overlap_sha256"] = hashlib.sha256((out_dir / "overlap.json").read_bytes()).hexdigest()
    summ["seconds"] = round(time.time() - t0)
    (out_dir / "summary.json").write_text(json.dumps(summ, indent=2) + "\n")
    print_summary(target, summ)


def D_items() -> list[dict]:
    from bridge_jspace.data import load_items

    if not hasattr(D_items, "_items"):
        D_items._items = load_items()  # type: ignore[attr-defined]
    return D_items._items  # type: ignore[attr-defined]


def summarize(items_out: dict) -> dict:
    """Medians over the primary items (each item's value = its mean over main-band layers)."""
    P = {n: r for n, r in items_out.items() if r.get("set") == "primary"}
    med = lambda xs: statistics.median(xs) if xs else None  # noqa: E731
    out: dict = {"n_primary": len(P)}
    out["median_share"] = {k: med([r["mean"][k] for r in P.values() if k in r["mean"]])
                           for k in ["A", "arm6", "rand_mean", "rand_max"] + [f"cm:{c}" for c in POOL] + [f"full:{c}" for c in POOL]}  # fmt: skip
    out["median_share_arm6b"] = med([r["arm6b"]["share"] for r in P.values()])
    out["median_ratio_arm6_over_random"] = med([r["mean"]["arm6"] / r["mean"]["rand_mean"] for r in P.values()])
    out["median_ratio_arm6b_over_random"] = med([r["arm6b"]["share"] / r["mean"]["rand_mean"] for r in P.values()])
    out["median_ratio_A_over_random"] = med([r["mean"]["A"] / r["mean"]["rand_mean"] for r in P.values()])
    out["items_arm6_above_all_20_random"] = sum(r["arm6_above_all_random"] for r in P.values())
    out["items_arm6b_above_all_20_random"] = sum(r["arm6b"]["above_all_random"] for r in P.values())
    cats: dict = {}
    for r in P.values():
        cats[r["arm6b"]["category"]] = cats.get(r["arm6b"]["category"], 0) + 1
    out["arm6b_categories"] = cats
    out["arm6b_padded_items"] = sum(bool(r["arm6b"]["padded"]) for r in P.values())
    out["arm6b_padded_tokens_median"] = med([r["arm6b"]["padded"] for r in P.values()])
    by_type: dict = {}
    for r in P.values():
        by_type.setdefault(r["answer_type"], []).append(r)
    out["by_answer_type"] = {t: {"n": len(rs), "A": med([r["mean"]["A"] for r in rs]), "arm6": med([r["mean"]["arm6"] for r in rs]),
                                 "arm6b": med([r["arm6b"]["share"] for r in rs]), "rand_mean": med([r["mean"]["rand_mean"] for r in rs])}
                             for t, rs in sorted(by_type.items())}  # fmt: skip
    return out


def print_summary(target: str, s: dict) -> None:
    f = lambda x: "n/a" if x is None else f"{x:.3f}"  # noqa: E731
    m = s["median_share"]
    print(f"# note 39 overlap diagnostic, {target}: primary items {s['n_primary']}; bridge-atom energy share inside each span, "
          "median over items of the mean over main-band layers")
    print(f"overlap {target}: A {f(m['A'])} | arm 6 {f(m['arm6'])} | arm 6b {f(s['median_share_arm6b'])} | random (mean of 20) "
          f"{f(m['rand_mean'])} | random (max of 20) {f(m['rand_max'])}")
    print(f"overlap {target}: ratio to random: A {f(s['median_ratio_A_over_random'])}, arm 6 {f(s['median_ratio_arm6_over_random'])}, "
          f"arm 6b {f(s['median_ratio_arm6b_over_random'])}; items above all 20 random spans: arm 6 {s['items_arm6_above_all_20_random']}, "
          f"arm 6b {s['items_arm6b_above_all_20_random']} of {s['n_primary']}")
    print(f"overlap {target}: pool (count-matched) " + ", ".join(f"{c} {f(m['cm:' + c])}" for c in POOL))
    print(f"overlap {target}: pool (full category) " + ", ".join(f"{c} {f(m['full:' + c])}" for c in POOL))
    print(f"overlap {target}: arm 6b categories {s['arm6b_categories']}; padded items {s['arm6b_padded_items']} (median padded tokens {s['arm6b_padded_tokens_median']})")
    for t, r in s["by_answer_type"].items():
        print(f"  {t:16s} n {r['n']:2d}  A {f(r['A'])}  arm6 {f(r['arm6'])}  arm6b {f(r['arm6b'])}  random {f(r['rand_mean'])}")


# ---- the rerun --------------------------------------------------------------------------------------------------


def onset_windows(prev_dir: Path, lenses) -> dict[str, str | None]:
    """Arm 1's median-onset window per lens on the finished run's primary items (paper_swap_read's rule)."""
    from scripts.paper_swap_read import Run

    run = Run(prev_dir, n_boot=0)
    P = run.names("primary")
    return {ln: run.median_onset_window(ln, P) for ln in lenses}


@torch.no_grad()
def rerun(a) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from scripts.exp02_swaps import prepare

    target = pins.TARGET
    pins.check_run_name(a.name)
    out_dir = D.RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    prev_dir, ov_dir = D.RES / a.prev, D.RES / a.overlap
    prev_manifest = json.loads((prev_dir / "manifest.json").read_text())
    prev_summary = json.loads((prev_dir / "summary.json").read_text())
    assert prev_manifest["target"] == target and json.loads((ov_dir / "manifest.json").read_text())["target"] == target
    ov_raw = (ov_dir / "overlap.json").read_bytes()
    ov = json.loads(ov_raw)["items"]
    vocab = D.load_vocab()
    lenses = D.LENSES.get(target, ("jpp",))
    onset = onset_windows(prev_dir, lenses)
    main = D.MAIN_BAND[target]
    wins = [(*main, True)] + sorted({(int(w.split("-")[0]), int(w.split("-")[1]), False) for w in onset.values() if w})
    prev_items = [json.loads(x) for x in (prev_dir / "items.jsonl").read_text().splitlines() if x.strip()]
    names = [r["name"] for r in prev_items if r["status"] == "eligible" and r["set"] == "primary"]
    if a.items:
        names = [n for n in names if n in a.items]
    names = names[: a.limit or None]
    prompt_end = prev_summary["gate"]["prompt_end"]
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "exp": D.EXP, "run": a.name, "kind": "rerun_6b", "why": a.why, "note": "prereg amendment 65 second addendum, note 39",
        "target": target, "model": pins.model_pin(), "lenses": {ln: list(pins.LENS_SOURCES[ln]) for ln in lenses},
        "prev_run": a.prev, "overlap_run": a.overlap, "overlap_sha256": hashlib.sha256(ov_raw).hexdigest(),
        "vocabulary_sha256": D.VOCAB_SHA256, "windows": [D.wname(s, e) for s, e, _ in wins], "main_band": D.wname(*main),
        "median_onset_windows": onset, "arms": list(RERUN_ARMS), "null_arms": list(RERUN_NULLS), "prompt_end": prompt_end,
        "items": names, "arm6b": "overlap.json's per-item category and tokens (selected on the J++ lens; used for every lens)",
        "command": " ".join(sys.argv), "git_state": pins.git_state(), "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    t0 = time.time()
    model = load_model()
    lens_objs = {ln: JLens(model, ln) for ln in lenses}
    letters = model.letter_token_ids().tolist()
    items = {it["name"]: (i, it) for i, it in enumerate(D_items())}
    layers_all = sorted({la for s, e, _ in wins for la in range(s, e + 1)})
    print(f"[{a.name}] loaded {time.time() - t0:.0f}s; windows {manifest['windows']} (median onset {onset}); {len(names)} items", flush=True)
    rows, item_rows, geo_diffs = [], [], []
    for name in names:
        index, item = items[name]
        row, prepared = prepare(model, D.NoProbes(), item, layers_all, "greedy_c", prompt_end)
        row.update(index=index, set="primary")
        item_rows.append(row)
        if row["status"] != "eligible":
            print(f"[{a.name}] {name}: status {row['status']} now (eligible in {a.prev}); skipped", flush=True)
            continue
        ids, clean_h, answer_ids, swap_ids = prepared
        toks = vocab["items"][name]["tokens"][target]
        barred = set(toks["scrub"]) | set(toks["excluded"])
        sets = {
            "scrub": toks["scrub"],
            "rand": sorted(random.Random(f"n39rand:{target}:{name}").sample(sorted(t for t in letters if t not in barred), len(toks["scrub"]))),
            "off6b": ov[name]["arm6b"]["tokens"],
        }  # fmt: skip
        assert len(sets["off6b"]) == len(sets["scrub"]) and not set(sets["off6b"]) & barred
        ids_ = {"answer": answer_ids, "swap": swap_ids, "swap_eq": D.number_twin_ids(model, item["swap_answer"])}
        for lens_name, lens in lens_objs.items():
            bt = torch.tensor([model.concept_token(item["intermediate"]), model.concept_token(item["swap_to"])], device="cuda")
            atoms, Qs = {}, {}
            if lens_name == "jpp":  # the overlap file's geometry (lens files only) recomputed with the loaded model
                for la in range(main[0], main[1] + 1):
                    got = shares(lens.vectors(la, torch.tensor(toks["scrub"], device="cuda")), lens.vectors(la, bt))
                    geo_diffs.append(abs(got - ov[name]["per_layer"][str(la)]["A"]))
            for la in layers_all:
                B = lens.vectors(la, bt)
                Qs[la] = {k: D.basis(lens.vectors(la, torch.tensor(v, device="cuda"))) for k, v in sets.items()}
                atoms[("bridge", la)] = B
                atoms[("bridge_noA", la)], _ = D.arm_atoms(B, Qs[la]["scrub"], "orth")
                atoms[("bridge_randA", la)], _ = D.arm_atoms(B, Qs[la]["rand"], "orth")
                atoms[(ARM6B, la)], _ = D.arm_atoms(B, Qs[la]["off6b"], "orth")
            for s, e, is_main in wins:
                wl = list(range(s, e + 1))
                plan = [(arm, False) for arm in RERUN_ARMS] + [(arm, True) for arm in RERUN_NULLS]
                row_edits, meta = [{}], []
                for arm, null in plan:
                    seed = D.NULL_SEED + 1000 * index + D.arm_index(arm) if null else None
                    edits, skipped = D.build_edits(arm, wl, atoms, clean_h, Qs, seed)
                    row_edits.append(edits)
                    meta.append((arm, null, skipped))
                # padded with unedited rows to note 39's batch shape (clean + 8 arms + 3 nulls), so that the stored rows
                # can be reproduced exactly (batched kernels depend on the batch shape, not on the other rows' values)
                row_edits += [{}] * (1 + len(D.ARMS) + len(D.NULL_ARMS) - len(row_edits))
                logits = D.batched_logits(model, ids, row_edits)
                for r, (arm, null, skipped) in enumerate(meta, start=1):
                    rows.append({"name": name, "index": index, "set": "primary", "lens": lens_name, "window": D.wname(s, e), "start": s,
                                 "end": e, "main": is_main, "arm": arm, "null": null, **D.read_row(model, logits[r], logits[0], ids_),
                                 **D.edit_stats(row_edits[r]), "layers_skipped": skipped})  # fmt: skip
        print(f"[{a.name}] {name} {time.time() - t0:.0f}s", flush=True)
    D.write_jsonl(out_dir / "items.jsonl", item_rows)
    D.write_jsonl(out_dir / "rows.jsonl", rows)
    check = stored_check(rows, prev_dir)
    check["overlap_geometry_max_abs_diff"] = max(geo_diffs) if geo_diffs else None  # share in span(A): overlap.json vs the loaded model
    (out_dir / "check.json").write_text(json.dumps(check, indent=2) + "\n")
    summary = {"items": len(names), "rows": len(rows), "windows": manifest["windows"], "check": check, "seconds": round(time.time() - t0),
               "reader": f"python scripts/paper_swap_read6b.py {D.RES.relative_to(pins.REPO_ROOT)}/{a.prev} {D.RES.relative_to(pins.REPO_ROOT)}/{a.name}"}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def stored_check(rows: list[dict], prev_dir: Path) -> dict:
    """Arms 1, 3, 7 and arm 1's null against note 39's stored rows (same item, lens, window, arm, null)."""
    key = lambda o: (o["name"], o["lens"], o["window"], o["arm"], o["null"])  # noqa: E731
    prev = {key(o): o for o in map(json.loads, (prev_dir / "rows.jsonl").read_text().splitlines()) if o["arm"] in CHECKED}
    out: dict = {}
    for arm, null in [(a, False) for a in CHECKED] + [("bridge", True)]:
        pairs = [(o, prev[key(o)]) for o in rows if o["arm"] == arm and o["null"] == null and key(o) in prev]
        if not pairs:
            continue
        out[f"{arm}{'/null' if null else ''}"] = {
            "n": len(pairs), "same_flip": sum(o["flip"] == p["flip"] for o, p in pairs),
            "same_swap_rank": sum(o["swap_rank"] == p["swap_rank"] for o, p in pairs),
            "flip_rate_rerun": sum(o["flip"] for o, _ in pairs) / len(pairs), "flip_rate_stored": sum(p["flip"] for _, p in pairs) / len(pairs),
            "max_abs_dlogp_diff": max(abs(o["dlogp_swap"] - p["dlogp_swap"]) for o, p in pairs),
        }  # fmt: skip
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["overlap", "rerun"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", default="")
    ap.add_argument("--prev", help="rerun: the finished note 39 run (results/paper_swap_decomp/<prev>)")
    ap.add_argument("--overlap", help="rerun: the overlap run whose arm 6b sets are used")
    ap.add_argument("--items", nargs="+")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    if args.stage == "overlap":
        overlap(args)
    else:
        assert args.prev and args.overlap and args.why, "rerun needs --prev, --overlap and --why"
        rerun(args)
