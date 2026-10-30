"""paper_swap_n53 (Zach's session, 2026-10-30, prereg amendment 72, note 53): note 39 with energy-matched controls, on the
paper's 90 two-hop prompts (data/probe_swap.json), at the main band only, J++ only.

Note 39's arms 7 and 5R are rank-matched, not energy-matched: span(A) holds more of the bridge atoms' energy than a random
letter-token span of the same size. This run adds the energy-matched controls (amendment 72, note 53):
  arm 7E   bridge_randE   arm 3 (bridge atoms orthogonalised to a span, renormalised, swapped) with the span of random
                          letter tokens drawn in order with random.Random('n53:' + item) (never an A or name token), the
                          first k of them, k the smallest prefix whose bridge-energy share reaches A's. Matched per item, as
                          note 44's Rcap: share = mean over the main band's layers of the mean over the two unit bridge
                          atoms of the squared norm of their projection onto the span; the draw is capped at 8 x |A| tokens
                          (all of them if none reaches; logged as not reached).
  arm 5R2  bridge_onlyR2  arm 5R (bridge atoms projected onto a random span, renormalised, swapped) with 2 x |A| tokens;
  arm 5R4  bridge_onlyR4  and 4 x |A|. Nested: the first |A|, 2|A|, 4|A| draws of random.Random('n39r:' + item) over 5R's
                          pool (random.sample's draws are prefix-stable; asserted per item: the first |A| are 5R's tokens).
  arm 7 seeds 2, 3        bridge_randA2 / bridge_randA3: arm 7 with random.Random('n53rand<s>:<target>:<item>') (seed 1 =
                          note 39's arm 7, random.Random('n39rand:<target>:<item>'), rerun here).
  1nf, 3nf, 5nf           bridge_nf / bridge_noA_nf / bridge_onlyA_nf: arms 1, 3 and 5 at every position from 1 except the
                          final one (the arm's edit masked at the last position), with arm 1's and arm 5's matched-norm
                          nulls masked the same way (same seeds as the all-position nulls).
Rerun in the same job and checked against the stored rows (check.json): the clean row, arm 1 and its null, arms 3, 5, 7 and
arm 5's null against note 39's run, arm 5R against the note 39 5R run (same item, lens, window, arm, null; every stored
field compared).
Two batched forwards per item, each padded with unedited rows to note 39's 12-row shape (clean + 8 arms + 3 nulls), so the
stored rows can be reproduced exactly:
  batch A: clean, arms 1, 3, 5, 7, 5R, 5R2, 5R4, 7 seed 2, 7 seed 3, nulls of arms 1 and 5;
  batch B: clean, arm 7E, 1nf, 3nf, 5nf, nulls of 1nf and 5nf, 5 unedited pads.
Items: the finished note 39 run's eligible primary items, its prompt end. Same code paths as paper_swap_decomp,
paper_swap_6b and paper_swap_5r (imported, unchanged). Logged per item and layer (atoms.jsonl): ranks and bridge-energy
shares of A, the three arm-7 spans, 5R, 5R2, 5R4 and 7E, and 7E's k.

python scripts/paper_swap_n53.py --name N --why W --prev NOTE39_RUN --prev5r NOTE39_5R_RUN [--items A B ... | --limit K]
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins  # noqa: E402
from scripts import paper_swap_6b as S6  # noqa: E402
from scripts import paper_swap_decomp as D  # noqa: E402

ARM7E = "bridge_randE"
ARMS_A = ("bridge", "bridge_noA", "bridge_onlyA", "bridge_randA", "bridge_onlyR", "bridge_onlyR2", "bridge_onlyR4",
          "bridge_randA2", "bridge_randA3")  # fmt: skip
NULLS_A = ("bridge", "bridge_onlyA")
ARMS_B = (ARM7E, "bridge_nf", "bridge_noA_nf", "bridge_onlyA_nf")
NULLS_B = ("bridge_nf", "bridge_onlyA_nf")
NF_BASE = {"bridge_nf": "bridge", "bridge_noA_nf": "bridge_noA", "bridge_onlyA_nf": "bridge_onlyA"}
NULL_SEED_ARM = {"bridge": "bridge", "bridge_onlyA": "bridge_onlyA", "bridge_nf": "bridge", "bridge_onlyA_nf": "bridge_onlyA"}
# arm -> (span key, mode) for the atoms; the span keys index the per-layer bases
SPAN_OF = {"bridge_noA": ("scrub", "orth"), "bridge_onlyA": ("scrub", "proj"), "bridge_randA": ("rand", "orth"),
           "bridge_randA2": ("rand2", "orth"), "bridge_randA3": ("rand3", "orth"), ARM7E: ("E", "orth"),
           "bridge_onlyR": ("R", "proj"), "bridge_onlyR2": ("R2", "proj"), "bridge_onlyR4": ("R4", "proj")}  # fmt: skip
BATCH = 1 + len(D.ARMS) + len(D.NULL_ARMS)  # note 39's 12-row batch
E_CAP = 8  # arm 7E's draw: at most 8 x |A| tokens
CHECK_N39 = [("clean", False), ("bridge", False), ("bridge", True), ("bridge_noA", False), ("bridge_onlyA", False),
             ("bridge_onlyA", True), ("bridge_randA", False)]  # fmt: skip
CHECK_N39R = [("bridge_onlyR", False)]
assert len(ARMS_A) + len(NULLS_A) + 1 == BATCH and len(ARMS_B) + len(NULLS_B) + 1 <= BATCH


def share(B: torch.Tensor, Q: torch.Tensor) -> float:
    """The bridge atoms' energy share in span(Q): mean over B's unit rows of |B Q|^2 (Q orthonormal [d, r])."""
    return float((B @ Q).pow(2).sum(-1).mean())


def energy_matched_k(B_by_layer: dict, V_by_layer: dict, target: float) -> tuple[int, float, bool]:
    """Smallest prefix k of the drawn rows whose bridge-energy share, averaged over the layers, is >= target. One QR per
    layer of the drawn rows' unit vectors gives every prefix's share (nested spans); a column within the span of the
    earlier ones (|R_jj| <= 1e-6 max) adds nothing. Returns (k, the QR share at k, reached)."""
    cum = None
    for la, B in B_by_layer.items():
        Q, R = torch.linalg.qr(V_by_layer[la].double().T)
        dg = R.diagonal().abs()
        c = (B.double() @ Q).pow(2) * (dg > dg.max() * 1e-6)[None, :]
        c = c.cumsum(-1).mean(0)
        cum = c if cum is None else cum + c
    cum = cum / len(B_by_layer)
    hit = (cum >= target).nonzero()
    k = int(hit[0]) + 1 if hit.numel() else int(cum.shape[0])
    return k, float(cum[k - 1]), bool(hit.numel())


def nf_mask(edits: dict) -> dict:
    """Restrict each layer's edit to every position from 1 except the final one."""
    for e in edits.values():
        e.mask = e.mask.clone()
        e.mask[-1] = False
        assert bool(e.mask.any()), "no position left to edit"
    return edits


def stored_check(rows: list[dict], prev_dir: Path, which: list[tuple[str, bool]]) -> dict:
    """Rows of this run against a stored run's rows (same item, lens, window, arm, null): identical = every field the
    stored row has serialises the same (json); also flips, ranks and the largest |delta log p| difference."""
    key = lambda o: (o["name"], o["lens"], o["window"], o["arm"], o["null"])  # noqa: E731
    want = {a for a, _ in which}
    prev = {key(o): o for o in map(json.loads, (prev_dir / "rows.jsonl").read_text().splitlines()) if o["arm"] in want}
    out: dict = {}
    for arm, null in which:
        pairs = [(o, prev[key(o)]) for o in rows if o["arm"] == arm and o["null"] == null and key(o) in prev]
        if not pairs:
            continue
        diff_fields: dict = {}
        ident = 0
        for o, p in pairs:
            bad = [f for f in p if json.dumps(o.get(f)) != json.dumps(p[f])]
            ident += not bad
            for f in bad:
                diff_fields[f] = diff_fields.get(f, 0) + 1
        out[f"{arm}{'/null' if null else ''}"] = {
            "n": len(pairs), "identical_rows": ident, "differing_fields": diff_fields,
            "same_flip": sum(o["flip"] == p["flip"] for o, p in pairs),
            "same_swap_rank": sum(o["swap_rank"] == p["swap_rank"] for o, p in pairs),
            "flip_rate_rerun": sum(o["flip"] for o, _ in pairs) / len(pairs), "flip_rate_stored": sum(p["flip"] for _, p in pairs) / len(pairs),
            "max_abs_dlogp_diff": max(abs(o["dlogp_swap"] - p["dlogp_swap"]) for o, p in pairs),
        }  # fmt: skip
    return out


@torch.no_grad()
def main(a) -> None:
    from bridge_jspace.lens import JLens
    from bridge_jspace.model import load_model
    from scripts.exp02_swaps import prepare

    target = pins.TARGET
    pins.check_run_name(a.name)
    out_dir = D.RES / a.name
    assert not (out_dir / "summary.json").exists(), f"{out_dir} has results; runs are written once"
    prev_dir, prev5r_dir = D.RES / a.prev, D.RES / a.prev5r
    prev_manifest = json.loads((prev_dir / "manifest.json").read_text())
    prev_summary = json.loads((prev_dir / "summary.json").read_text())
    assert prev_manifest["target"] == target and json.loads((prev5r_dir / "manifest.json").read_text())["target"] == target
    vocab = D.load_vocab()
    lens_name = "jpp"  # note 53: J++ only
    main_band = D.MAIN_BAND[target]
    win = D.wname(*main_band)
    layers = list(range(main_band[0], main_band[1] + 1))
    prev_items = [json.loads(x) for x in (prev_dir / "items.jsonl").read_text().splitlines() if x.strip()]
    names = [r["name"] for r in prev_items if r["status"] == "eligible" and r["set"] == "primary"]
    if a.items:
        names = [n for n in names if n in a.items]
    names = names[: a.limit or None]
    prompt_end = prev_summary["gate"]["prompt_end"]
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "exp": D.EXP, "run": a.name, "kind": "n53", "why": a.why, "note": "prereg amendment 72, note 53 (note 39 with energy-matched controls)",
        "target": target, "model": pins.model_pin(), "lenses": {lens_name: list(pins.LENS_SOURCES[lens_name])},
        "prev_run": a.prev, "prev_5r_run": a.prev5r, "vocabulary_sha256": D.VOCAB_SHA256, "windows": [win], "main_band": win,
        "arms_batch_A": list(ARMS_A), "nulls_batch_A": list(NULLS_A), "arms_batch_B": list(ARMS_B), "nulls_batch_B": list(NULLS_B),
        "batch_rows": BATCH, "prompt_end": prompt_end, "items": names,
        "seeds": {"arm7_s1": "random.Random('n39rand:<target>:<item>') (note 39's arm 7)",
                  "arm7_s2_s3": "random.Random('n53rand<s>:<target>:<item>'), s = 2, 3",
                  "5R_5R2_5R4": "the first |A|, 2|A|, 4|A| draws of random.Random('n39r:' + item) (5R's)",
                  "7E": f"the first k of {E_CAP} x |A| draws of random.Random('n53:' + item)",
                  "nulls": "note 39's: NULL_SEED + 1000 * item index + arm index (nf nulls: their all-position arm's seed)"},
        "arm7E_rule": "k = the smallest prefix whose bridge-energy share (mean over the main band's layers of the mean over the "
                      "two unit bridge atoms of |projection|^2) is >= A's on the same measure; capped at 8|A| (not reached: all 8|A|)",
        "nf": "every position from 1 except the final one",
        "command": " ".join(sys.argv), "git_state": pins.git_state(), "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    t0 = time.time()
    torch.cuda.reset_peak_memory_stats()
    model = load_model()
    lens = JLens(model, lens_name)
    letters = model.letter_token_ids().tolist()
    items = {it["name"]: (i, it) for i, it in enumerate(S6.D_items())}
    print(f"[{a.name}] loaded {time.time() - t0:.0f}s; window {win}; {len(names)} items", flush=True)
    rows, item_rows, atom_rows, item_e = [], [], [], []
    for name in names:
        index, item = items[name]
        row, prepared = prepare(model, D.NoProbes(), item, layers, "greedy_c", prompt_end)
        row.update(index=index, set="primary")
        item_rows.append(row)
        if row["status"] != "eligible":
            print(f"[{a.name}] {name}: status {row['status']} now (eligible in {a.prev}); skipped", flush=True)
            continue
        ids, clean_h, answer_ids, swap_ids = prepared
        toks = vocab["items"][name]["tokens"][target]
        n = len(toks["scrub"])
        barred = set(toks["scrub"]) | set(toks["excluded"])
        pool = sorted(t for t in letters if t not in barred)
        r_draw = random.Random("n39r:" + name).sample(pool, 4 * n)
        rset = sorted(random.Random("n39r:" + name).sample(pool, n))  # paper_swap_5r's arm 5R, verbatim
        assert sorted(r_draw[:n]) == rset, f"{name}: 5R's tokens are not the first |A| of the nested draw"
        e_draw = random.Random("n53:" + name).sample(pool, E_CAP * n)
        sets = {
            "scrub": toks["scrub"],
            "rand": sorted(random.Random(f"n39rand:{target}:{name}").sample(pool, n)),  # note 39's arm 7, verbatim
            "rand2": sorted(random.Random(f"n53rand2:{target}:{name}").sample(pool, n)),
            "rand3": sorted(random.Random(f"n53rand3:{target}:{name}").sample(pool, n)),
            "R": rset, "R2": sorted(r_draw[: 2 * n]), "R4": sorted(r_draw),
        }  # fmt: skip
        assert set(sets["R"]) <= set(sets["R2"]) <= set(sets["R4"])
        ids_ = {"answer": answer_ids, "swap": swap_ids, "swap_eq": D.number_twin_ids(model, item["swap_answer"])}
        bt = torch.tensor([model.concept_token(item["intermediate"]), model.concept_token(item["swap_to"])], device="cuda")
        Bs = {la: lens.vectors(la, bt) for la in layers}
        Qs: dict = {la: {k: D.basis(lens.vectors(la, torch.tensor(v, device="cuda"))) for k, v in sets.items()} for la in layers}
        # arm 7E: energy-matched to A's share, averaged over the band's layers
        shareA = sum(share(Bs[la], Qs[la]["scrub"]) for la in layers) / len(layers)
        e_t = torch.tensor(e_draw, device="cuda")
        k, qr_share, reached = energy_matched_k(Bs, {la: lens.vectors(la, e_t) for la in layers}, shareA)
        sets["E"] = sorted(e_draw[:k])
        for la in layers:
            Qs[la]["E"] = D.basis(lens.vectors(la, torch.tensor(sets["E"], device="cuda")))
        shareE = sum(share(Bs[la], Qs[la]["E"]) for la in layers) / len(layers)
        item_e.append({"name": name, "n_A": n, "k_E": k, "k_E_over_n_A": k / n, "reached": reached, "share_A": shareA,
                       "share_E_qr": qr_share, "share_E": shareE})  # fmt: skip
        atoms: dict = {}
        for la in layers:
            B = Bs[la]
            atoms[("bridge", la)] = B
            arow = {"name": name, "lens": lens_name, "layer": la, "n_A": n, "k_E": k}
            for arm, (sk, mode) in SPAN_OF.items():
                atoms[(arm, la)], norms = D.arm_atoms(B, Qs[la][sk], mode)
                arow[f"{arm}_atom_norms"] = norms
            for sk, Q in Qs[la].items():
                arow[f"rank_{sk}"], arow[f"share_{sk}"] = int(Q.shape[1]), share(B, Q)
            atom_rows.append(arow)
        for batch, arms, nulls in (("A", ARMS_A, NULLS_A), ("B", ARMS_B, NULLS_B)):
            plan = [(arm, False) for arm in arms] + [(arm, True) for arm in nulls]
            row_edits, meta = [{}], []
            for arm, null in plan:
                seed = D.NULL_SEED + 1000 * index + D.arm_index(NULL_SEED_ARM[arm]) if null else None
                edits, skipped = D.build_edits(NF_BASE.get(arm, arm), layers, atoms, clean_h, Qs, seed)
                if arm in NF_BASE:
                    nf_mask(edits)
                row_edits.append(edits)
                meta.append((arm, null, skipped))
            row_edits += [{}] * (BATCH - len(row_edits))  # note 39's 12-row batch shape
            logits = D.batched_logits(model, ids, row_edits)
            for r, (arm, null, skipped) in enumerate(meta, start=1):
                rows.append({"name": name, "index": index, "set": "primary", "lens": lens_name, "window": win, "start": main_band[0],
                             "end": main_band[1], "main": True, "arm": arm, "null": null, **D.read_row(model, logits[r], logits[0], ids_),
                             **D.edit_stats(row_edits[r]), "layers_skipped": skipped, "batch": batch,
                             "positions": "all_but_final" if arm in NF_BASE else "all"})  # fmt: skip
            if batch == "A":  # note 39's clean row (batch A's row 0)
                rows.append({"name": name, "index": index, "set": "primary", "lens": lens_name, "window": win, "start": main_band[0],
                             "end": main_band[1], "main": True, "arm": "clean", "null": False, **D.read_row(model, logits[0], logits[0], ids_),
                             "layers_skipped": []})  # fmt: skip
        flips = " ".join(f"{o['arm']}{'/null' if o['null'] else ''}={int(o['flip'])}" for o in rows if o["name"] == name and o["arm"] != "clean")
        print(f"[{a.name}] {name}: k_E {k} (|A| {n}, share A {shareA:.3f}, 7E {shareE:.3f}); {flips} {time.time() - t0:.0f}s", flush=True)
    D.write_jsonl(out_dir / "items.jsonl", item_rows)
    D.write_jsonl(out_dir / "rows.jsonl", rows)
    D.write_jsonl(out_dir / "atoms.jsonl", atom_rows)
    D.write_jsonl(out_dir / "energy7e.jsonl", item_e)
    check = {"note39": stored_check(rows, prev_dir, CHECK_N39), "note39_5r": stored_check(rows, prev5r_dir, CHECK_N39R),
             "arm7E_qr_vs_basis_share_max_abs_diff": max((abs(e["share_E_qr"] - e["share_E"]) for e in item_e), default=None)}  # fmt: skip
    (out_dir / "check.json").write_text(json.dumps(check, indent=2) + "\n")
    rel = D.RES.relative_to(pins.REPO_ROOT)
    summary = {"items": len(names), "rows": len(rows), "windows": [win], "check": check, "seconds": round(time.time() - t0),
               "peak_gpu_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2),
               "peak_gpu_reserved_gb": round(torch.cuda.max_memory_reserved() / 2**30, 2),
               "arm7E_not_reached": sum(not e["reached"] for e in item_e),
               "arm7E_k_over_nA_median": sorted(e["k_E_over_n_A"] for e in item_e)[len(item_e) // 2] if item_e else math.nan,
               "command": manifest["command"], "git_state": manifest["git_state"],
               "reader": f"python scripts/paper_swap_read53.py {rel}/{a.prev} {rel}/{a.name}"}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--prev", required=True, help="the finished note 39 run (results/paper_swap_decomp/<prev>)")
    ap.add_argument("--prev5r", required=True, help="the finished note 39 arm 5R run (results/paper_swap_decomp/<prev5r>)")
    ap.add_argument("--items", nargs="+")
    ap.add_argument("--limit", type=int, default=0)
    main(ap.parse_args())
