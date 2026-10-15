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


# ---- part B: exp02 swaps (v4, layers 24-40, n=77) and exp03 brew ------------------------------------------------

EXP02 = R / "exp02_swaps"
EXP03 = R / "exp03_brew_swaps"


def exp02_flips(run, condition, null=False, band="24-40"):
    """exp02_swaps/<run>/outcomes.jsonl: {item: flip} for one condition, band and null flag (flip = the greedy
    continuation has the swap answer and not the clean answer; one row per eligible item)."""
    rows = jsonl(EXP02 / run / "outcomes.jsonl")
    return {
        o["name"]: o["flip"] for o in rows if o["condition"] == condition and o["band"] == band and o["null"] == null
    }


def exp02_rate(run, condition, null=False, band="24-40"):
    """Share of eligible items whose swap flips: mean of exp02_flips."""
    f = exp02_flips(run, condition, null, band)
    return float(np.mean(list(f.values()))), len(f)


def exp02_max_null(run):
    """The highest flip rate of any matched-norm random-direction control in the run (null == true rows)."""
    conditions = {o["condition"] for o in jsonl(EXP02 / run / "outcomes.jsonl")}
    return max(exp02_rate(run, c, null=True)[0] for c in conditions)


def exp02_paired_diff(run, a, b):
    """Mean over items of flip(a) - flip(b), same items (the point estimate of the paired bootstrap)."""
    fa, fb = exp02_flips(run, a), exp02_flips(run, b)
    return float(np.mean([fa[n] - fb[n] for n in fa]))


def exp02_bridge_types():
    """PLACES and PEOPLE as listed in scripts/exp02_figures.py (read as literals, not imported)."""
    import ast

    tree = ast.parse((R.parent / "scripts/exp02_figures.py").read_text())
    sets = {
        t.id: ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        for t in node.targets
        if isinstance(t, ast.Name) and t.id in ("PLACES", "PEOPLE")
    }
    return sets["PLACES"], sets["PEOPLE"]


def exp02_rate_by_type(run, kind):
    """J-part flip rate over items whose bridge (items.jsonl `intermediate`) is a place, a person, or anything else."""
    places, people = exp02_bridge_types()
    bridge = {m["name"]: m["intermediate"] for m in jsonl(EXP02 / run / "items.jsonl")}
    pick = {"place": lambda e: e in places, "person": lambda e: e in people}.get(
        kind, lambda e: e not in places and e not in people
    )
    f = {n: v for n, v in exp02_flips(run, "jpart").items() if pick(bridge[n])}
    return float(np.mean(list(f.values()))), len(f)


def exp02_jpp_superset():
    """main_v4 J-part (24-40): items the J-lens flips and J++ does not, and the reverse."""
    jl, jp = exp02_flips("main_v4_jlens", "jpart"), exp02_flips("main_v4_jpp", "jpart")
    return sum(jl[n] and not jp[n] for n in jl), sum(jp[n] and not jl[n] for n in jl)


def exp03_rate(run, lens, kind, regime, null=False, amp=1, scale=None, field="flip"):
    """exp03_brew_swaps/<run>/outcomes.jsonl: share of rows (one per eligible item) with `field` true, for one lens,
    kind, regime, null flag, amplification and steering scale."""
    rows = [
        o
        for o in jsonl(EXP03 / run / "outcomes.jsonl")
        if (o["lens"], o["kind"], o["regime"], o["null"], o.get("amp", 1), o.get("scale"))
        == (lens, kind, regime, null, amp, scale)
    ]
    return float(np.mean([o[field] for o in rows])), len(rows)


def exp03_changed(run, lens, kind, regime, null, amp=1, scale=None):
    """Share of rows whose answer changed (not kept_clean): the random-direction null's 'answer changed' rate."""
    rate, n = exp03_rate(run, lens, kind, regime, null, amp, scale, field="kept_clean")
    return 1 - rate, n


EXP04 = R / "exp04_brew_patch"  # runs: patch_map / parts_window (bank items), patch_map_fresh / parts_window_fresh


def exp04_role_rate(source, group, layer, role, run="patch_map"):
    """exp04 outcomes.jsonl: share of rows (one per eligible item) for one source (cf / off), position group and
    layer whose answer has that role (b = f(X), c = the counterfactual's answer, A = the original answer, I = the
    original intermediate)."""
    rows = [
        o
        for o in jsonl(EXP04 / run / "outcomes.jsonl")
        if (o["source"], o["group"], o["layer"]) == (source, group, layer)
    ]
    return float(np.mean([o["role"] == role for o in rows])), len(rows)


def exp04_max_off_changed(run="patch_map"):
    """The highest share of answers the off-path control's patch changes, over every group and layer."""
    cells = {}
    for o in jsonl(EXP04 / run / "outcomes.jsonl"):
        if o["source"] == "off":
            cells.setdefault((o["group"], o["layer"]), []).append(o["role"] != "A")
    return max(float(np.mean(v)) for v in cells.values())


def wilson_bounds(k, n, z=1.959964):
    p, d = k / n, 1 + z * z / n
    centre, half = (p + z * z / (2 * n)) / d, z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return centre - half, centre + half


def exp04_window(group, run="patch_map"):
    """exp04 outcomes.jsonl: the manifest's window rule, recomputed. The layers where the counterfactual's copy (cf)
    gives f(X) more often than c and more often than the off-path copy changes the answer at all, 95% Wilson
    intervals not overlapping; "first-last" when every second layer in between is in it."""
    cells = {}
    for o in jsonl(EXP04 / run / "outcomes.jsonl"):
        if o["group"] == group:
            cells.setdefault((o["source"], o["layer"]), []).append(o["role"])
    window = []
    for layer in sorted({layer for _, layer in cells}):
        cf, off = cells["cf", layer], cells["off", layer]
        b_low = wilson_bounds(cf.count("b"), len(cf))[0]
        c_high = wilson_bounds(cf.count("c"), len(cf))[1]
        changed_high = wilson_bounds(sum(r != "A" for r in off), len(off))[1]
        if b_low > c_high and b_low > changed_high:
            window.append(layer)
    if window and window == list(range(window[0], window[-1] + 1, 2)):
        return f"{window[0]}-{window[-1]}"
    return ",".join(map(str, window)) or "none"


def exp04_items_with_step(run="patch_map", window=range(36, 51, 2)):
    """exp04 outcomes.jsonl: items whose copy after the start line gives f(X) at one window layer or more."""
    hit = {}
    for o in jsonl(EXP04 / run / "outcomes.jsonl"):
        if (o["source"], o["group"]) == ("cf", "after_start") and o["layer"] in window:
            hit[o["name"]] = hit.get(o["name"], False) or o["role"] == "b"
    return sum(hit.values())


def exp04_step_score(part, lens=None, null=False, run="parts_window"):
    """exp04 parts_window outcomes.jsonl: per item, the share of window layers (36-50) at which copying that part of
    the counterfactual's difference gives f(X) (role "b"); then the mean over items. The full copy has lens None."""
    rows = [
        o
        for o in jsonl(EXP04 / run / "outcomes.jsonl")
        if o["part"] == part and o["source"] == "cf" and o["lens"] == lens and o["null"] == null
    ]
    per_item = {}
    for o in rows:
        per_item.setdefault(o["name"], []).append(o["role"] == "b")
    return float(np.mean([np.mean(v) for v in per_item.values()])), len(per_item)


def exp04_parts_role_share(part, role, lens=None, null=False, run="parts_window_fresh"):
    """exp04 parts outcomes.jsonl: the share of item x window-layer cells at which copying that part gives the role."""
    rows = [
        o
        for o in jsonl(EXP04 / run / "outcomes.jsonl")
        if o["part"] == part and o["source"] == "cf" and o["lens"] == lens and o["null"] == null
    ]
    return float(np.mean([o["role"] == role for o in rows]))


EXP06 = R / "exp06_sigma_writes/sigma_v1"


def exp06_rate(task, lens, field="flip", **where):
    """exp06 outcomes.jsonl: share of rows (one per eligible item) of a task (matched / steer) and lens, matching the
    other keys (condition, or lam and scale; null), whose `field` (flip / kept_clean) is true."""
    rows = [
        o
        for o in jsonl(EXP06 / "outcomes.jsonl")
        if (o["task"], o["lens"]) == (task, lens) and all(o.get(k) == v for k, v in where.items())
    ]
    return float(np.mean([o[field] for o in rows])), len(rows)


def exp06_edit_size(lens, condition):
    """exp06 outcomes.jsonl: the median edit size (share of the residual norm) of a matched-swap condition."""
    sizes = [
        o["edit_ratio"]
        for o in jsonl(EXP06 / "outcomes.jsonl")
        if o["task"] == "matched" and (o["lens"], o["condition"], o["null"]) == (lens, condition, False)
    ]
    return float(np.median(sizes))


def exp04_variance_share(lens, what, run="parts_window"):
    """exp04 parts_window fve.jsonl: the median share of δ's variance in the part (or of a random direction's, chance)."""
    shares = [f["share"] for f in jsonl(EXP04 / run / "fve.jsonl") if (f["lens"], f["what"]) == (lens, what)]
    return float(np.median(shares))


EXP07 = R / "exp07_step_code/code_v1"


def exp07_step_score(item_set, direction, dose="copy", lens=None):
    """exp07 outcomes.jsonl: per item of a set (fresh / bank), the share of the 8 window layers at which the edit gives
    f(X) (role "b"); then the mean over items. dose "copy" is the copy's size, "code" the code's own."""
    per_item = {}
    for o in jsonl(EXP07 / "outcomes.jsonl"):
        if (o["set"], o["direction"], o["dose"], o["lens"]) == (item_set, direction, dose, lens):
            per_item.setdefault(o["name"], []).append(o["role"] == "b")
    return float(np.mean([np.mean(v) for v in per_item.values()])), len(per_item)


def exp07_read_accuracy(item_set, layer):
    """exp07 reads.jsonl: share of items whose own intermediate the code decodes from their activations at a layer."""
    rows = [r for r in jsonl(EXP07 / "reads.jsonl") if (r["set"], r["layer"]) == (item_set, layer)]
    return float(np.mean([r["decoded"] == r["I"] for r in rows]))


def exp07_diagnostic(what, lens=None):
    """exp07 diagnostics.jsonl: the median of one diagnostic over items and layers."""
    values = [d["value"] for d in jsonl(EXP07 / "diagnostics.jsonl") if (d["lens"], d["what"]) == (lens, what)]
    return float(np.median(values))


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
        ("exp02", "J-part flips, J++ (main_v4_jpp)", exp02_rate("main_v4_jpp", "jpart")[0], 0.52),
        ("exp02", "J-part flips, J-lens (main_v4_jlens)", exp02_rate("main_v4_jlens", "jpart")[0], 0.35),
        ("exp02", "remainder flips, J++", exp02_rate("main_v4_jpp", "remainder")[0], 0.08),
        ("exp02", "remainder flips, J-lens", exp02_rate("main_v4_jlens", "remainder")[0], 0.12),
        ("exp02", "remainder, J-space held, J++", exp02_rate("main_v4_jpp", "remainder_clamped")[0], 0.01),
        ("exp02", "remainder, J-space held, J-lens", exp02_rate("main_v4_jlens", "remainder_clamped")[0], 0.04),
        ("exp02", "raw lens vectors, J++", exp02_rate("main_v4_jpp", "raw_jlens")[0], 0.49),
        ("exp02", "raw lens vectors, J-lens", exp02_rate("main_v4_jlens", "raw_jlens")[0], 0.40),
        ("exp02", "full probe (lens-free)", exp02_rate("main_v4_jpp", "full_probe")[0], 0.27),
        (
            "exp02",
            "highest random-direction control, either lens",
            max(map(exp02_max_null, ("main_v4_jpp", "main_v4_jlens"))),
            0.03,
        ),
        ("exp02", "J-part minus remainder, J++ (pts)", exp02_paired_diff("main_v4_jpp", "jpart", "remainder"), 0.44),
        ("exp02", "J-part minus remainder, J-lens", exp02_paired_diff("main_v4_jlens", "jpart", "remainder"), 0.23),
        ("exp02", "matched-alignment flips, J++", exp02_rate("matched_v4_jpp", "jpart_matched")[0], 0.14),
        ("exp02", "matched-alignment flips, J-lens", exp02_rate("matched_v4_jlens", "jpart_matched")[0], 0.10),
        ("exp02", "J-part minus matched, J++", exp02_paired_diff("matched_v4_jpp", "jpart", "jpart_matched"), 0.38),
        (
            "exp02",
            "J-part minus matched, J-lens",
            exp02_paired_diff("matched_v4_jlens", "jpart", "jpart_matched"),
            0.25,
        ),
        ("exp02", "J-part at the cue phrase, J++", exp02_rate("main_v4_jpp_pos-cue", "jpart")[0], 0.31),
        ("exp02", "J-part at the cue phrase, J-lens", exp02_rate("main_v4_jlens_pos-cue", "jpart")[0], 0.19),
        ("exp02", "J-part at offset -1 only, J++", exp02_rate("main_v4_jpp_pos-prev", "jpart")[0], 0.09),
        ("exp02", "J-part, bridge a place, J++", exp02_rate_by_type("main_v4_jpp", "place")[0], 0.88),
        ("exp02", "J-part, bridge a person, J++", exp02_rate_by_type("main_v4_jpp", "person")[0], 0.86),
        ("exp02", "J-part, bridge anything else, J++", exp02_rate_by_type("main_v4_jpp", "other")[0], 0.25),
        ("exp02", "J-part, bridge a person, J-lens", exp02_rate_by_type("main_v4_jlens", "person")[0], 0.14),
        ("exp02", "items J-lens flips and J++ does not (count)", exp02_jpp_superset()[0], 0),
        ("exp02", "items J++ flips and J-lens does not (count)", exp02_jpp_superset()[1], 13),
        (
            "exp03",
            "start swap S->S' x3, 8-24, J++",
            exp03_rate("swap_amp", "jpp", "start", "start_line", amp=3)[0],
            0.61,
        ),
        ("exp03", "start swap x3, J-lens", exp03_rate("swap_amp", "jlens", "start", "start_line", amp=3)[0], 0.17),
        (
            "exp03",
            "start swap x3, random direction, J++",
            exp03_rate("swap_amp", "jpp", "start", "start_line", True, 3)[0],
            0.01,
        ),
        (
            "exp03",
            "intermediate swap x3 after start, J++",
            exp03_rate("swap_amp", "jpp", "swap", "after_start", amp=3)[0],
            0.0,
        ),
        (
            "exp03",
            "intermediate swap x3 every position, J++",
            exp03_rate("swap_amp", "jpp", "swap", "all", amp=3)[0],
            0.03,
        ),
        (
            "exp03",
            "fresh items: start-line steer 3%, J++",
            exp03_rate("fresh_steer", "jpp", "steer_start", "start_line", scale=0.03)[0],
            0.63,
        ),
        (
            "exp03",
            "fresh items: start-line steer 3%, J-lens",
            exp03_rate("fresh_steer", "jlens", "steer_start", "start_line", scale=0.03)[0],
            0.30,
        ),
        (
            "exp03",
            "fresh items: random direction 3%, flips, J++",
            exp03_rate("fresh_steer", "jpp", "steer_start", "start_line", True, scale=0.03)[0],
            0.0,
        ),
        (
            "exp03",
            "fresh items: random direction 3%, answer changed, J++",
            exp03_changed("fresh_steer", "jpp", "steer_start", "start_line", True, scale=0.03)[0],
            0.0,
        ),
        ("exp04", "after the start line, layer 36: f(X)", exp04_role_rate("cf", "after_start", 36, "b")[0], 0.11),
        ("exp04", "after the start line, layer 46: f(X)", exp04_role_rate("cf", "after_start", 46, "b")[0], 0.48),
        ("exp04", "after the start line, layer 50: f(X)", exp04_role_rate("cf", "after_start", 50, "b")[0], 0.48),
        ("exp04", "after the start line, layer 52: c", exp04_role_rate("cf", "after_start", 52, "c")[0], 0.71),
        ("exp04", "the start line, layer 46: original answer", exp04_role_rate("cf", "start_line", 46, "A")[0], 1.0),
        ("exp04", "rule lines, layer 24: c", exp04_role_rate("cf", "rules", 24, "c")[0], 0.95),
        ("exp04", "rule lines, layer 40: original answer", exp04_role_rate("cf", "rules", 40, "A")[0], 0.84),
        ("exp04", "off-path control, most answers changed", exp04_max_off_changed(), 0.02),
        ("exp04", "parts: step score, whole copy", exp04_step_score("full")[0], 0.31),
        ("exp04", "parts: J++ I/X lens coordinates", exp04_step_score("lens2", "jpp")[0], 0.0),
        ("exp04", "parts: J++ all but those", exp04_step_score("not_lens2", "jpp")[0], 0.31),
        ("exp04", "parts: J++ J-space part (25 atoms)", exp04_step_score("jspace", "jpp")[0], 0.0),
        ("exp04", "parts: J++ all but the J-space part", exp04_step_score("not_jspace", "jpp")[0], 0.26),
        ("exp04", "parts: J-lens all but the J-space part", exp04_step_score("not_jspace", "jlens")[0], 0.24),
        ("exp04", "parts: J++ J-space share of δ's variance", exp04_variance_share("jpp", "jspace"), 0.08),
        ("exp04", "parts: J++ J-space share of a random direction's", exp04_variance_share("jpp", "chance"), 0.07),
        ("exp04", "window, after the start line", exp04_window("after_start"), "36-50"),
        ("exp04", "window, the last token", exp04_window("last"), "46,50"),
        ("exp04", "items giving f(X) at a window layer", exp04_items_with_step(), 52),
        ("exp04", "after the start line, layer 40: I", exp04_role_rate("cf", "after_start", 40, "I")[0], 0.29),
        ("exp04", "after the start line, layer 48: I", exp04_role_rate("cf", "after_start", 48, "I")[0], 0.16),
        ("exp04", "fresh: window, after the start line", exp04_window("after_start", "patch_map_fresh"), "36-50"),
        ("exp04", "fresh: window, the last token", exp04_window("last", "patch_map_fresh"), "44-50"),
        ("exp04", "fresh: items giving f(X) at a window layer", exp04_items_with_step("patch_map_fresh"), 97),
        (
            "exp04",
            "fresh: after the start line, layer 36: f(X)",
            exp04_role_rate("cf", "after_start", 36, "b", "patch_map_fresh")[0],
            0.10,
        ),
        (
            "exp04",
            "fresh: after the start line, layer 48: f(X)",
            exp04_role_rate("cf", "after_start", 48, "b", "patch_map_fresh")[0],
            0.52,
        ),
        (
            "exp04",
            "fresh: after the start line, layer 52: c",
            exp04_role_rate("cf", "after_start", 52, "c", "patch_map_fresh")[0],
            0.68,
        ),
        (
            "exp04",
            "fresh: after the start line, layer 38: I",
            exp04_role_rate("cf", "after_start", 38, "I", "patch_map_fresh")[0],
            0.43,
        ),
        (
            "exp04",
            "fresh: after the start line, layer 50: I",
            exp04_role_rate("cf", "after_start", 50, "I", "patch_map_fresh")[0],
            0.07,
        ),
        ("exp04", "fresh: off-path control, most answers changed", exp04_max_off_changed("patch_map_fresh"), 0.06),
        ("exp04", "fresh parts: step score, whole copy", exp04_step_score("full", run="parts_window_fresh")[0], 0.31),
        (
            "exp04",
            "fresh parts: J++ I/X lens coordinates",
            exp04_step_score("lens2", "jpp", run="parts_window_fresh")[0],
            0.0,
        ),
        (
            "exp04",
            "fresh parts: J++ all but those",
            exp04_step_score("not_lens2", "jpp", run="parts_window_fresh")[0],
            0.31,
        ),
        (
            "exp04",
            "fresh parts: J++ J-space part (25 atoms)",
            exp04_step_score("jspace", "jpp", run="parts_window_fresh")[0],
            0.0,
        ),
        (
            "exp04",
            "fresh parts: J++ all but the J-space part",
            exp04_step_score("not_jspace", "jpp", run="parts_window_fresh")[0],
            0.28,
        ),
        (
            "exp04",
            "fresh parts: J-lens all but the J-space part",
            exp04_step_score("not_jspace", "jlens", run="parts_window_fresh")[0],
            0.26,
        ),
        (
            "exp04",
            "fresh parts: J++ all but the J-space part, I",
            exp04_parts_role_share("not_jspace", "I", "jpp"),
            0.28,
        ),
        ("exp04", "fresh parts: J++ J-space part, I", exp04_parts_role_share("jspace", "I", "jpp"), 0.01),
        (
            "exp04",
            "fresh parts: J++ J-space share of δ's variance",
            exp04_variance_share("jpp", "jspace", "parts_window_fresh"),
            0.08,
        ),
        (
            "exp04",
            "fresh parts: J++ J-space share of a random direction's",
            exp04_variance_share("jpp", "chance", "parts_window_fresh"),
            0.07,
        ),
        ("exp06", "matched J++: J-part", exp06_rate("matched", "jpp", condition="jpart", null=False)[0], 0.52),
        (
            "exp06",
            "matched J++: isotropic rest",
            exp06_rate("matched", "jpp", condition="jpart_matched", null=False)[0],
            0.14,
        ),
        (
            "exp06",
            "matched J++: Σ-shaped rest",
            exp06_rate("matched", "jpp", condition="jpart_matched_sigma", null=False)[0],
            0.12,
        ),
        ("exp06", "matched J-lens: J-part", exp06_rate("matched", "jlens", condition="jpart", null=False)[0], 0.35),
        (
            "exp06",
            "matched J-lens: isotropic rest",
            exp06_rate("matched", "jlens", condition="jpart_matched", null=False)[0],
            0.10,
        ),
        (
            "exp06",
            "matched J-lens: Σ-shaped rest",
            exp06_rate("matched", "jlens", condition="jpart_matched_sigma", null=False)[0],
            0.14,
        ),
        (
            "exp06",
            "matched J++: Σ-shaped rest's null",
            exp06_rate("matched", "jpp", condition="jpart_matched_sigma", null=True)[0],
            0.04,
        ),
        (
            "exp06",
            "matched J++: Σ-shaped rest, answer kept",
            exp06_rate("matched", "jpp", "kept_clean", condition="jpart_matched_sigma", null=False)[0],
            0.44,
        ),
        ("exp06", "matched J++: J-part edit size", exp06_edit_size("jpp", "jpart"), 0.016),
        ("exp06", "matched J++: Σ-shaped rest edit size", exp06_edit_size("jpp", "jpart_matched_sigma"), 0.17),
        ("exp06", "steer J++ 3%: λ = 1 (the lens)", exp06_rate("steer", "jpp", lam=1.0, scale=0.03)[0], 0.63),
        ("exp06", "steer J++ 3%: λ = 0.5", exp06_rate("steer", "jpp", lam=0.5, scale=0.03)[0], 0.13),
        ("exp06", "steer J++ 3%: λ = 0", exp06_rate("steer", "jpp", lam=0.0, scale=0.03)[0], 0.03),
        ("exp06", "steer J++ 5%: λ = 1 (the lens)", exp06_rate("steer", "jpp", lam=1.0, scale=0.05)[0], 0.49),
        ("exp06", "steer J++ 5%: λ = 0", exp06_rate("steer", "jpp", lam=0.0, scale=0.05)[0], 0.21),
        ("exp06", "steer J-lens 3%: λ = 1 (the lens)", exp06_rate("steer", "jlens", lam=1.0, scale=0.03)[0], 0.30),
        ("exp06", "steer J-lens 3%: λ = 0.5", exp06_rate("steer", "jlens", lam=0.5, scale=0.03)[0], 0.01),
        ("exp06", "steer J++ 3%: random direction", exp06_rate("steer", "jpp", null=True, scale=0.03)[0], 0.0),
        ("exp07", "fresh: items", exp07_step_score("fresh", "copy")[1], 154),
        ("exp07", "fresh: the copy", exp07_step_score("fresh", "copy")[0], 0.31),
        ("exp07", "fresh: code", exp07_step_score("fresh", "code")[0], 0.34),
        ("exp07", "fresh: random", exp07_step_score("fresh", "random")[0], 0.0),
        ("exp07", "fresh: code at its own size", exp07_step_score("fresh", "code", "code")[0], 0.04),
        ("exp07", "fresh: J++ lens direction", exp07_step_score("fresh", "lens", lens="jpp")[0], 0.01),
        ("exp07", "fresh: J++ Σ-shaped lens direction", exp07_step_score("fresh", "sigma_0.0", lens="jpp")[0], 0.01),
        ("exp07", "fresh: J++ code's J-space part", exp07_step_score("fresh", "code_jspace", lens="jpp")[0], 0.0),
        ("exp07", "fresh: J++ code's rest", exp07_step_score("fresh", "code_rest", lens="jpp")[0], 0.29),
        ("exp07", "fresh: J-lens code's rest", exp07_step_score("fresh", "code_rest", lens="jlens")[0], 0.27),
        ("exp07", "bank: items", exp07_step_score("bank", "copy")[1], 82),
        ("exp07", "bank: the copy", exp07_step_score("bank", "copy")[0], 0.31),
        ("exp07", "bank: code", exp07_step_score("bank", "code")[0], 0.25),
        ("exp07", "bank: J++ code's rest", exp07_step_score("bank", "code_rest", lens="jpp")[0], 0.20),
        ("exp07", "bank: J-lens code's rest", exp07_step_score("bank", "code_rest", lens="jlens")[0], 0.18),
        ("exp07", "fresh: the code reads I, layer 40", exp07_read_accuracy("fresh", 40), 0.92),
        ("exp07", "fresh: the code reads I, layer 50", exp07_read_accuracy("fresh", 50), 0.76),
        ("exp07", "code norm over the copy's", exp07_diagnostic("code norm over copy norm"), 0.45),
        ("exp07", "J++: cosine of the code to the lens direction", exp07_diagnostic("cos code~lens", "jpp"), 0.02),
        ("exp07", "J++: J-space share of the code", exp07_diagnostic("code jspace share", "jpp"), 0.09),
        ("exp07", "J++: J-space share of a random direction", exp07_diagnostic("chance", "jpp"), 0.07),
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
