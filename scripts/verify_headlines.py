"""Recompute part A's headline numbers straight from the raw run files, for a human to check before VERIFIED.md.

Deliberately independent of the experiment code: only json / csv / numpy, one short function per number, each with
the file and formula in its docstring. Prints the recomputed value next to the value claimed in README.md.

    uv run python scripts/verify_headlines.py
"""

import json
from pathlib import Path

import numpy as np

R = Path(__file__).resolve().parents[1] / "results"
EXP10 = R / "exp10_lens_sanity/20261013-205936"  # Qwen3.6-27B, space stripped
EXP11 = R / "exp11_bridge_vs_answer_by_layer/20261014-092835"  # Qwen3.6-27B, prompts as published
EXP12 = R / "exp12_position_map/20261014-095358"  # Qwen3.6-27B, prompts as published
BAND = (32, 48)  # layers averaged over


def jsonl(path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


# ---- exp11: last prompt token -----------------------------------------------------------------


def exp11_band_share(reader, role, label=None):
    """exp11 ranks.jsonl: for each eligible item (items.jsonl status == "eligible", optionally one part B label),
    the share of layers 32-48 where `<role>_pool` == 1 (top-1 in its pool); then the mean over items."""
    meta = {m["name"]: m for m in jsonl(EXP11 / "items.jsonl")}
    names = [n for n, m in meta.items() if m["status"] == "eligible" and (label is None or m["label"] == label)]
    rows = {r["name"]: r for r in jsonl(EXP11 / "ranks.jsonl") if r["reader"] == reader}
    vals = []
    for n in names:
        r = rows[n]
        band = [i for i, layer in enumerate(r["layers"]) if BAND[0] <= layer <= BAND[1]]
        vals.append(np.mean([r[f"{role}_pool"][i] == 1 for i in band]))
    return float(np.mean(vals)), len(vals)


# ---- exp12: every prompt position -----------------------------------------------------------------


def exp12_load(reader):
    """grids_<reader>.npz holds, per item and field, a [layers, positions] array of ranks (key "<item>|<field>");
    items.jsonl gives each position's offset from the last content token; layers.json the layer of each row."""
    meta = {m["name"]: m for m in jsonl(EXP12 / "items.jsonl")}
    layers = json.loads((EXP12 / "layers.json").read_text())[reader]
    band = [i for i, layer in enumerate(layers) if BAND[0] <= layer <= BAND[1]]
    z = np.load(EXP12 / f"grids_{reader}.npz")
    eligible = [n for n, m in meta.items() if m["status"] == "eligible"]
    return meta, layers, band, z, eligible


def exp12_share_at_offset(reader, role, offset):
    """Mean over eligible items of: share of layers 32-48 with `<role>_pool` == 1 at that offset."""
    meta, _, band, z, eligible = exp12_load(reader)
    vals = []
    for n in eligible:
        if offset in meta[n]["offsets"]:
            col = meta[n]["offsets"].index(offset)
            vals.append(np.mean(z[f"{n}|{role}_pool"][band, col] == 1))
    return float(np.mean(vals)), len(vals)


def exp12_missed_rescued(reader):
    """Items whose bridge is top-1 in < half of layers 32-48 at the true last token (last column): how many, and
    the share of them with the bridge (and, as control, the distractor) top-1 in >= half the band layers at some
    earlier token."""
    _, _, band, z, eligible = exp12_load(reader)
    missed = rescued = control = 0
    for n in eligible:
        b = (z[f"{n}|bridge_pool"][band] == 1).mean(0)  # share per position
        d = (z[f"{n}|distractor_pool"][band] == 1).mean(0)
        if b[-1] < 0.5:
            missed += 1
            rescued += b[:-1].max() >= 0.5
            control += d[:-1].max() >= 0.5
    return missed, rescued / missed, control / missed


def exp12_first_layer_half(reader, role, offset):
    """First layer at which at least half of the eligible items have `<role>_pool` == 1 at that offset."""
    meta, layers, _, z, eligible = exp12_load(reader)
    top = [
        z[f"{n}|{role}_pool"][:, meta[n]["offsets"].index(offset)] == 1
        for n in eligible
        if offset in meta[n]["offsets"]
    ]
    share = np.mean(top, axis=0)
    return layers[int(np.argmax(share >= 0.5))]


# ---- exp10: lens-eval multihop, pass@10 -------------------------------------------------------------


def exp10_pass10(reader):
    """multihop_ranks.jsonl: per item, the share of its intermediates with min_rank < 10 (0-based rank, best over
    layers at the last token); mean over items whose intermediates are all single tokens (multihop_items.jsonl)."""
    meta = {m["name"]: m for m in jsonl(EXP10 / "multihop_items.jsonl")}
    per_item = {}
    for r in jsonl(EXP10 / "multihop_ranks.jsonl"):
        if r["reader"] == reader and meta[r["name"]]["all_single_token"]:
            per_item.setdefault(r["name"], []).append(r["min_rank"] < 10)
    return float(np.mean([np.mean(v) for v in per_item.values()])), len(per_item)


def main():
    checks = [
        ("exp10", "27B stripped, pass@10, J++", exp10_pass10("jpp")[0], 0.75),
        ("exp10", "27B stripped, pass@10, logit lens", exp10_pass10("logit")[0], 0.51),
        ("exp10", "27B stripped, pass@10, J-lens", exp10_pass10("jlens")[0], 0.57),
        ("exp11", "bridge top-1 among entities, L32-48, J-lens", exp11_band_share("jlens", "bridge")[0], 0.59),
        ("exp11", "bridge top-1, J++", exp11_band_share("jpp", "bridge")[0], 0.56),
        ("exp11", "bridge top-1, logit lens", exp11_band_share("logit", "bridge")[0], 0.26),
        ("exp11", "distractor top-1, J-lens", exp11_band_share("jlens", "distractor")[0], 0.06),
        ("exp11", "answer top-1 among answers, J-lens", exp11_band_share("jlens", "answer")[0], 0.41),
        ("exp11", "bridge top-1, J-lens, J-mediated items", exp11_band_share("jlens", "bridge", "J-mediated")[0], 0.79),
        ("exp11", "bridge top-1, J-lens, 'neither' items", exp11_band_share("jlens", "bridge", "neither")[0], 0.49),
        ("exp12", "bridge top-1 at offset -1, J-lens", exp12_share_at_offset("jlens", "bridge", -1)[0], 0.66),
        ("exp12", "bridge top-1 at offset 0, J-lens", exp12_share_at_offset("jlens", "bridge", 0)[0], 0.56),
        ("exp12", "answer top-1 at offset 0, J-lens", exp12_share_at_offset("jlens", "answer", 0)[0], 0.41),
        ("exp12", "missed at the last token, J-lens (count)", exp12_missed_rescued("jlens")[0], 26),
        ("exp12", "... of those, bridge on top earlier", exp12_missed_rescued("jlens")[1], 0.73),
        ("exp12", "... distractor on top earlier (control)", exp12_missed_rescued("jlens")[2], 0.35),
        ("exp12", "half of items: bridge at -1, first layer", exp12_first_layer_half("jlens", "bridge", -1), 23),
        ("exp12", "half of items: answer at 0, first layer", exp12_first_layer_half("jlens", "answer", 0), 44),
    ]
    width = max(len(c[1]) for c in checks)
    for exp, what, got, claimed in checks:
        ok = round(got, 2) == round(claimed, 2) if isinstance(claimed, float) else got == claimed
        shown = f"{got:.4f}" if isinstance(got, float) else str(got)
        print(f"{'OK  ' if ok else 'DIFF'} {exp}  {what:<{width}}  recomputed {shown:>8}  README {claimed}")
    n11 = exp11_band_share("jlens", "bridge")[1]
    n12 = exp12_share_at_offset("jlens", "bridge", -1)[1]
    print(
        f"\nitems: exp11 eligible n={n11}, exp12 eligible at offset -1 n={n12}, exp10 single-token n={exp10_pass10('jpp')[1]}"
    )


if __name__ == "__main__":
    main()
