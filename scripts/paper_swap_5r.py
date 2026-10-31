"""paper_swap_5r (Zach, 2026-10-30, prereg amendment 67, note 39 arm 5R): a random-projection control for note 39's
sufficiency arm.

Arm 5R (bridge_onlyR): note 39's arm 5 (bridge_onlyA: the bridge atoms projected onto span(A), renormalised, swapped)
with span(A) replaced by the span of as many random letter tokens as A has (random.Random('n39r:' + item), never an A
or name token; the pool is the model's letter tokens, as arm 7's). Run with arms 1 (bridge) and 5 (bridge_onlyA), arm
1's matched-norm null and arm 5's (both note 39's, same seeds), on the finished note 39 run's eligible primary items, at
the main band and at arm 1's median-onset window per lens (paper_swap_read's rule on the stored rows). Same code paths as
paper_swap_decomp and paper_swap_6b (imported, unchanged); each window's batch is padded with unedited rows to note 39's
12-row shape, so arms 1 and 5 and the nulls can be checked against the stored rows exactly (check.json). Logged per
layer: the rank of span(A) and of the random span (atoms.jsonl).

python scripts/paper_swap_5r.py --name N --why W --prev NOTE39_RUN [--items A B ... | --limit K]
"""

from __future__ import annotations

import argparse
import json
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

ARM5R = "bridge_onlyR"
ARMS = ("bridge", "bridge_onlyA", ARM5R)
NULLS = ("bridge", "bridge_onlyA")  # arm 1's null (the reading's) and arm 5's (note 39's A3; descriptive)
CHECKED = [("bridge", False), ("bridge_onlyA", False), ("bridge", True), ("bridge_onlyA", True)]


def stored_check(rows: list[dict], prev_dir: Path) -> dict:
    """Arms 1 and 5 and their nulls against note 39's stored rows (same item, lens, window, arm, null)."""
    key = lambda o: (o["name"], o["lens"], o["window"], o["arm"], o["null"])  # noqa: E731
    want = {a for a, _ in CHECKED}
    prev = {key(o): o for o in map(json.loads, (prev_dir / "rows.jsonl").read_text().splitlines()) if o["arm"] in want}
    out: dict = {}
    for arm, null in CHECKED:
        pairs = [(o, prev[key(o)]) for o in rows if o["arm"] == arm and o["null"] == null and key(o) in prev]
        if pairs:
            out[f"{arm}{'/null' if null else ''}"] = {
                "n": len(pairs), "same_flip": sum(o["flip"] == p["flip"] for o, p in pairs),
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
    prev_dir = D.RES / a.prev
    prev_manifest = json.loads((prev_dir / "manifest.json").read_text())
    prev_summary = json.loads((prev_dir / "summary.json").read_text())
    assert prev_manifest["target"] == target
    vocab = D.load_vocab()
    lenses = D.LENSES.get(target, ("jpp",))
    onset = S6.onset_windows(prev_dir, lenses)
    main_band = D.MAIN_BAND[target]
    wins = [(*main_band, True)] + sorted({(int(w.split("-")[0]), int(w.split("-")[1]), False) for w in onset.values() if w})
    prev_items = [json.loads(x) for x in (prev_dir / "items.jsonl").read_text().splitlines() if x.strip()]
    names = [r["name"] for r in prev_items if r["status"] == "eligible" and r["set"] == "primary"]
    if a.items:
        names = [n for n in names if n in a.items]
    names = names[: a.limit or None]
    prompt_end = prev_summary["gate"]["prompt_end"]
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "exp": D.EXP, "run": a.name, "kind": "rerun_5r", "why": a.why, "note": "prereg amendment 67, note 39 arm 5R",
        "target": target, "model": pins.model_pin(), "lenses": {ln: list(pins.LENS_SOURCES[ln]) for ln in lenses},
        "prev_run": a.prev, "vocabulary_sha256": D.VOCAB_SHA256, "windows": [D.wname(s, e) for s, e, _ in wins],
        "main_band": D.wname(*main_band), "median_onset_windows": onset, "arms": list(ARMS), "null_arms": list(NULLS),
        "arm5R": "arm 5 with span(A) replaced by the span of len(A) random letter tokens, random.Random('n39r:' + item), "
                 "never an A or name token", "prompt_end": prompt_end, "items": names,
        "command": " ".join(sys.argv), "git_state": pins.git_state(), "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }  # fmt: skip
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    t0 = time.time()
    model = load_model()
    lens_objs = {ln: JLens(model, ln) for ln in lenses}
    letters = model.letter_token_ids().tolist()
    items = {it["name"]: (i, it) for i, it in enumerate(S6.D_items())}
    layers_all = sorted({la for s, e, _ in wins for la in range(s, e + 1)})
    print(f"[{a.name}] loaded {time.time() - t0:.0f}s; windows {manifest['windows']} (median onset {onset}); {len(names)} items", flush=True)
    rows, item_rows, atom_rows = [], [], []
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
        rset = sorted(random.Random("n39r:" + name).sample(sorted(t for t in letters if t not in barred), len(toks["scrub"])))
        sets = {"scrub": toks["scrub"], "R": rset}
        ids_ = {"answer": answer_ids, "swap": swap_ids, "swap_eq": D.number_twin_ids(model, item["swap_answer"])}
        for lens_name, lens in lens_objs.items():
            bt = torch.tensor([model.concept_token(item["intermediate"]), model.concept_token(item["swap_to"])], device="cuda")
            atoms, Qs = {}, {}
            for la in layers_all:
                B = lens.vectors(la, bt)
                Qs[la] = {k: D.basis(lens.vectors(la, torch.tensor(v, device="cuda"))) for k, v in sets.items()}
                atoms[("bridge", la)] = B
                atoms[("bridge_onlyA", la)], nA = D.arm_atoms(B, Qs[la]["scrub"], "proj")
                atoms[(ARM5R, la)], nR = D.arm_atoms(B, Qs[la]["R"], "proj")
                atom_rows.append({"name": name, "lens": lens_name, "layer": la, "n": len(rset), "rank_A": int(Qs[la]["scrub"].shape[1]),
                                  "rank_R": int(Qs[la]["R"].shape[1]), "bridge_norm_in_A": nA, "bridge_norm_in_R": nR})  # fmt: skip
            for s, e, is_main in wins:
                wl = list(range(s, e + 1))
                plan = [(arm, False) for arm in ARMS] + [(arm, True) for arm in NULLS]
                row_edits, meta = [{}], []
                for arm, null in plan:
                    seed = D.NULL_SEED + 1000 * index + D.arm_index(arm) if null else None
                    edits, skipped = D.build_edits(arm, wl, atoms, clean_h, Qs, seed)
                    row_edits.append(edits)
                    meta.append((arm, null, skipped))
                row_edits += [{}] * (1 + len(D.ARMS) + len(D.NULL_ARMS) - len(row_edits))  # note 39's 12-row batch shape
                logits = D.batched_logits(model, ids, row_edits)
                for r, (arm, null, skipped) in enumerate(meta, start=1):
                    rows.append({"name": name, "index": index, "set": "primary", "lens": lens_name, "window": D.wname(s, e), "start": s,
                                 "end": e, "main": is_main, "arm": arm, "null": null, **D.read_row(model, logits[r], logits[0], ids_),
                                 **D.edit_stats(row_edits[r]), "layers_skipped": skipped})  # fmt: skip
        print(f"[{a.name}] {name} {time.time() - t0:.0f}s", flush=True)
    D.write_jsonl(out_dir / "items.jsonl", item_rows)
    D.write_jsonl(out_dir / "rows.jsonl", rows)
    D.write_jsonl(out_dir / "atoms.jsonl", atom_rows)
    check = stored_check(rows, prev_dir)
    (out_dir / "check.json").write_text(json.dumps(check, indent=2) + "\n")
    rel = D.RES.relative_to(pins.REPO_ROOT)
    summary = {"items": len(names), "rows": len(rows), "windows": manifest["windows"], "check": check, "seconds": round(time.time() - t0),
               "reader": f"python scripts/paper_swap_read5r.py {rel}/{a.prev} {rel}/{a.name}"}  # fmt: skip
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--why", required=True)
    ap.add_argument("--prev", required=True, help="the finished note 39 run (results/paper_swap_decomp/<prev>)")
    ap.add_argument("--items", nargs="+")
    ap.add_argument("--limit", type=int, default=0)
    main(ap.parse_args())
