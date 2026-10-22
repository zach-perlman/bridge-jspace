"""The README's figures (2026-10-21): one plain figure per claim, read from the saved runs under results/ (no GPU).

Each figure answers one question in its title, uses the README's names, and keeps numbers and n in the README caption.
  f1_two_routes.png       Zach's suite: the lens push and the J-space knock-out, lookup vs recall families
  f2_stated_bridge.png    D1: which part of a stated bridge's change switches the answer (n=80, layers 32-40)
  f3_early_push.png       D4: the early lens push (layer 20, 8x), wording B, 100 per family
  f4_late_read.png        D2: the answer's statement hidden from the last tokens, attention vs DeltaNet layers
  f5_slot_by_layer.png    D3: patched last tokens, word / slot / alt digit by layer (pointer_v4)
  f6_slot_counts.png      D3: order vs place, from the start vs from the end (pointer_v4x, layer 50)
  f7_pointer_push.png     D3b: the pointer direction vs the lens direction (layer 48)

uv run python scripts/readme_figures.py [--out figures/readme_1021]
"""

from __future__ import annotations

import argparse
import collections
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
LOOKUP, RECALL, DIGIT, GREY, LIGHT = "#eb6834", "#2a78d6", "#1baf7a", "#9aa0a6", "#c9c8c3"
INK, INK2, SURF, GRID = "#0b0b0b", "#52514e", "#ffffff", "#e6e5e0"
plt.rcParams.update({"font.size": 10, "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK, "axes.titlesize": 11, "axes.titleweight": "bold"})  # fmt: skip
NAMES = {"BL": "prompt → prompt", "RL": "memory → prompt", "BR": "prompt → memory", "RR": "memory → memory"}


def load(*p: str) -> dict:
    return json.loads(RES.joinpath(*p, "summary.json").read_text())


def rows(*p: str, file: str) -> list[dict]:
    return [json.loads(x) for x in RES.joinpath(*p, file).read_text().splitlines()]


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    p = k / n
    d = 1 + z * z / n
    m = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, m - h), min(1.0, m + h)


def style(ax, axis: str = "x") -> None:
    ax.set_facecolor(SURF)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis=axis, color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def bar_ci(ax, x, p, lo, hi, color, width=0.6, horizontal=False, label=None) -> None:
    lo, hi = min(lo, p), max(hi, p)  # rounding at 0% / 100% can put a bound a hair inside the point
    if horizontal:
        ax.barh(x, 100 * p, height=width, color=color, label=label)
        ax.errorbar(100 * p, x, xerr=[[100 * (p - lo)], [100 * (hi - p)]], fmt="none", ecolor=INK2, lw=1, capsize=2)
    else:
        ax.bar(x, 100 * p, width=width, color=color, label=label)
        ax.errorbar(x, 100 * p, yerr=[[100 * (p - lo)], [100 * (hi - p)]], fmt="none", ecolor=INK2, lw=1, capsize=2)
        ax.text(x, 100 * hi + 1.5, f"{100 * p:.0f}%", ha="center", va="bottom", fontsize=8.5, color=INK)


def save(fig, out: Path, name: str) -> None:
    fig.savefig(out / name, dpi=160, facecolor=SURF, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out / name)


def f1_two_routes(out: Path) -> None:
    fams = ["BL", "RL", "BR", "RR"]
    write = load("read_write", "dose_v1")["families"]
    ko = load("ablate_pilot", "abl_rot_v1")["families"]
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.0), sharey=True, gridspec_kw={"wspace": 0.12})
    ys = list(range(len(fams)))
    for y, f in zip(ys, fams, strict=True):
        col = LOOKUP if f.endswith("L") else RECALL
        w = write[f]["write"]
        lens = max(v["flips"] for k, v in w.items() if "/lens_" in k)
        rnd = max(v["flips"] for k, v in w.items() if "/random_" in k)
        axes[0].barh(y, 100 * lens, height=0.6, color=col)
        axes[0].scatter([100 * rnd], [y], marker="|", s=120, color=INK2, zorder=3)
        acc = ko[f"{f}/clean"]["accuracy"]
        axes[1].barh(y, 100 * acc["jspace"], height=0.6, color=col)
        axes[1].scatter([100 * acc["random"]], [y], marker="|", s=120, color=INK2, zorder=3)
    for ax in axes:
        style(ax)
        ax.set_xlim(0, 105)
    axes[0].set_yticks(ys, [NAMES[f] for f in fams])
    axes[0].invert_yaxis()
    axes[0].set_title("Push along the lens direction", loc="left")
    axes[0].set_xlabel("% of answers switched (| = random push)")
    axes[1].set_title("Remove the J-space", loc="left")
    axes[1].set_xlabel("% still right (| = random removal)")
    handles = [plt.Rectangle((0, 0), 1, 1, color=LOOKUP), plt.Rectangle((0, 0), 1, 1, color=RECALL)]
    fig.legend(handles, ["answer looked up in the prompt", "answer recalled from memory"], loc="lower center",
               ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.2))  # fmt: skip
    save(fig, out, "f1_two_routes.png")


def f2_stated_bridge(out: Path) -> None:
    cells = load("statement_positions", "d1_parts_n80_v1")["cells"]
    parts = [("full", "the whole change", INK2), ("jspace", "only its lens-readable part", RECALL),
             ("not_jspace", "everything except that part", LOOKUP)]  # fmt: skip
    groups = [("BL", "bridge stated in the prompt,\nanswer looked up in the prompt"),
              ("BR", "bridge stated in the prompt,\nanswer recalled from memory")]  # fmt: skip
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    style(ax, "y")
    for gi, (fam, _) in enumerate(groups):
        c = cells[f"{fam}/context/primary"]
        n = c["n"] * len(c["layers"])
        for pi, (key, label, col) in enumerate(parts):
            k = round(c["flip"]["means"][key] * n)
            bar_ci(ax, gi + (pi - 1) * 0.26, *wilson(k, n), col, width=0.24, label=label if gi == 0 else None)
    ax.set_xticks(range(len(groups)), [g for _, g in groups])
    ax.set_ylim(0, 105)
    ax.set_ylabel("% of answers switched")
    ax.set_title("Paste one part of the alt prompt's change into the org prompt", loc="left")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3)
    save(fig, out, "f2_stated_bridge.png")


def f3_early_push(out: Path) -> None:
    hit, n = collections.Counter(), collections.Counter()
    for r in rows("early_push", "d4_push_wording_b_v1", file="outcomes.jsonl"):
        if r.get("kind") != "push" or r.get("subset") != "b" or "prompt" in r:
            continue
        if str(r["layer"]) == "20" and r["scale"] == 8.0:
            n[(r["family"], r["dir"])] += 1
            hit[(r["family"], r["dir"])] += r["role"] == "b"
    fams = ["RL", "RR", "BL", "BR"]
    fig, ax = plt.subplots(figsize=(8.0, 3.2))
    style(ax, "y")
    for i, f in enumerate(fams):
        col = RECALL if f.startswith("R") else LOOKUP
        bar_ci(ax, i - 0.17, *wilson(hit[(f, "lens")], n[(f, "lens")]), col, width=0.32)
        bar_ci(ax, i + 0.17, *wilson(hit[(f, "random")], n[(f, "random")]), LIGHT, width=0.32)
    ax.set_xticks(range(len(fams)), [NAMES[f].replace(" → ", "\n→ ") for f in fams])
    ax.set_ylim(0, 105)
    ax.set_ylabel("% of answers switched")
    ax.set_title("Push the subject phrase toward another animal's word (layer 20)", loc="left")
    handles = [plt.Rectangle((0, 0), 1, 1, color=RECALL), plt.Rectangle((0, 0), 1, 1, color=LOOKUP),
               plt.Rectangle((0, 0), 1, 1, color=LIGHT)]  # fmt: skip
    ax.legend(handles, ["bridge recalled: lens push", "bridge stated: lens push", "random push"], frameon=False,
              loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3)  # fmt: skip
    save(fig, out, "f3_early_push.png")


def f4_late_read(out: Path) -> None:
    run = RES / "attn_knockout" / "d2_v4_late_read"
    rr = rows("attn_knockout", "d2_v4_late_read", file="rows.jsonl")
    ok = {r["id"] for r in rr if r["source"] == "none" and r["correct"]}
    dom = {c["id"]: c.get("domain") for c in map(json.loads, (run / "cases.jsonl").read_text().splitlines())}
    k, n = collections.Counter(), collections.Counter()
    for r in rr:
        if r["id"] in ok and r["source"] == "lookup" and r.get("mode", "value") == "value" and r["dest"] == "final":
            key = (r["family"], r["layers"], dom.get(r["id"]))
            n[key] += 1
            k[key] += r["kept"]
    topics = [("countries", "countries"), ("animals", "animals"), ("body", "body parts")]
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    style(ax, "y")
    for i, (d, _) in enumerate(topics):
        bar_ci(ax, i - 0.17, *wilson(k[("RL", "attn", d)], n[("RL", "attn", d)]), LOOKUP, width=0.32)
        bar_ci(ax, i + 0.17, *wilson(k[("RL", "gdn", d)], n[("RL", "gdn", d)]), LIGHT, width=0.32)
    ax.set_xticks(range(len(topics)), [t for _, t in topics])
    ax.set_ylim(0, 112)
    ax.set_ylabel("% still right")
    ax.set_title("Hide the answer's statement from the last tokens (memory → prompt)", loc="left")
    handles = [plt.Rectangle((0, 0), 1, 1, color=LOOKUP), plt.Rectangle((0, 0), 1, 1, color=LIGHT)]
    ax.legend(handles, ["hidden in every attention layer (16 layers)", "hidden in every DeltaNet layer (48 layers)"],
              frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)  # fmt: skip
    save(fig, out, "f4_late_read.png")


def f5_slot_by_layer(out: Path) -> None:
    rates = load("pointer_swap", "d3v4_swap_topics")["rates"]
    layers = sorted(int(k.split("|")[4]) for k in rates if k.startswith("RL|all|e5f0|last|") and k.endswith("|dissoc")
                    and k.split("|")[4].isdigit())  # fmt: skip
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    style(ax, "y")
    for role, label, col in (("position", "the same slot in the org prompt (pointer)", LOOKUP),
                             ("identity", "bridge alt's own statement (word)", RECALL),
                             ("value", "the alt prompt's answer (digit)", DIGIT)):  # fmt: skip
        c = [rates[f"RL|all|e5f0|last|{la}|dissoc"][role] for la in layers]
        ax.plot(layers, [100 * x[0] for x in c], color=col, lw=2, marker="o", ms=4, label=label)
        ax.fill_between(layers, [100 * x[1] for x in c], [100 * x[2] for x in c], color=col, alpha=0.15, lw=0)
    ax.set_xlabel("layer patched (Qwen3.6-27B has 64)")
    ax.set_ylabel("% of patched answers")
    ax.set_ylim(0, 100)
    ax.set_title("Patch the alt prompt's last two tokens into the org prompt", loc="left")
    ax.legend(frameon=False, loc="upper left")
    save(fig, out, "f5_slot_by_layer.png")


def f6_slot_counts(out: Path) -> None:
    rates = load("pointer_swap", "d3v4x_swap_main")["rates"]
    start, end, place = (
        ("position", "same number,\nfrom the start"),
        ("end", "same number,\nfrom the end"),
        ("token", "same place\nin the text"),
    )
    panels = [("e5-off", "a filler sentence moved", [("position", "same number\nin the list"), place]),
              ("e5more", "alt has one statement more", [start, end, place]),
              ("e5fewer", "alt has one statement fewer", [start, end, place])]  # fmt: skip
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.0), sharey=True, gridspec_kw={"wspace": 0.08,
                                                                              "width_ratios": [2, 3, 3]})  # fmt: skip
    for ax, (lv, title, bars) in zip(axes, panels, strict=True):
        style(ax, "y")
        d = rates[f"RL|all|{lv}|last|50|dissoc"]
        for i, (role, _) in enumerate(bars):
            bar_ci(ax, i, *d[role][:3], LOOKUP if role == "position" else LIGHT, width=0.6)
        ax.set_xticks(range(len(bars)), [b for _, b in bars], fontsize=9)
        ax.set_title(title, loc="left", fontsize=10)
    axes[0].set_ylabel("% of patched answers")
    axes[0].set_ylim(0, 60)
    save(fig, out, "f6_slot_counts.png")


def f7_pointer_push(out: Path) -> None:
    sets = [("d3b_replicate_fresh_27b", "fresh scenes\n(22 entities)"),
            ("d3v4_fit_main", "new entities, new wording\n(85 entities)")]  # fmt: skip
    fig, ax = plt.subplots(figsize=(6.5, 3.0))
    style(ax, "y")
    for i, (run, _) in enumerate(sets):
        p = load("pointer_fit", run)["primary"]
        for j, (key, col) in enumerate((("slot", LOOKUP), ("lens", RECALL), ("random", LIGHT))):
            bar_ci(ax, i + (j - 1) * 0.26, *p[key][:3], col, width=0.24)
    ax.set_xticks(range(len(sets)), [s for _, s in sets])
    ax.set_ylim(0, 60)
    ax.set_ylabel("% moved to the target statement")
    ax.set_title("Push the last tokens toward another slot (layer 48)", loc="left")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (LOOKUP, RECALL, LIGHT)]
    ax.legend(handles, ["learned pointer direction", "lens word direction", "random direction"], frameon=False,
              loc="upper right")  # fmt: skip
    save(fig, out, "f7_pointer_push.png")


def f8_shifts(out: Path) -> None:
    """D3 v6: under an extra sentence before the list (place in the text shifts) or before the question (distance back
    shifts), the same slot vs the moved statement; Qwen3.6-27B at layer 50, OLMo-3-7B-Instruct at layer 18."""
    runs = [
        ("d3v6_swap_27b", "50", "Qwen3.6-27B (layer 50)"),
        ("olmo3_7b_instruct_d3v6_swap", "18", "OLMo-3-7B (layer 18)"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.2), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, (run, la, title) in zip(axes, runs, strict=True):
        style(ax, "y")
        rates = load("pointer_swap", run)["rates"]
        for i, (lv, moved, _) in enumerate((("e5-abs", "token", "sentence added\nbefore the list"),
                                                ("e5-rel", "back", "sentence added\nbefore the question"))):  # fmt: skip
            d = rates[f"RL|all|{lv}|last|{la}|dissoc"]
            bar_ci(ax, i - 0.17, *d["position"][:3], LOOKUP, width=0.32)
            bar_ci(ax, i + 0.17, *d[moved][:3], LIGHT, width=0.32)
        ax.set_xticks([0, 1], ["sentence added\nbefore the list", "sentence added\nbefore the question"])
        ax.set_title(title, loc="left", fontsize=10)
        ax.set_ylim(0, 65)
    axes[0].set_ylabel("% of patched answers")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (LOOKUP, LIGHT)]
    fig.legend(handles, ["the same number in the list", "the statement the shift lines up (same place / same distance)"],
               loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.12))  # fmt: skip
    save(fig, out, "f8_shifts.png")


def f9_olmo_slot(out: Path) -> None:
    """D3 on OLMo-3-7B-Instruct: word / slot / alt digit by layer (layers placed by function, 16-21)."""
    rates = load("pointer_swap", "olmo3_7b_instruct_d3v4_swap_fn")["rates"]
    layers = [16, 17, 18, 19, 20, 21]
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    style(ax, "y")
    for role, label, col in (("position", "the same slot in the org prompt (pointer)", LOOKUP),
                             ("identity", "bridge alt's own statement (word)", RECALL),
                             ("value", "the alt prompt's answer (digit)", DIGIT)):  # fmt: skip
        c = [rates[f"RL|all|e5f0|last|{la}|dissoc"][role] for la in layers]
        ax.plot(layers, [100 * x[0] for x in c], color=col, lw=2, marker="o", ms=4, label=label)
        ax.fill_between(layers, [100 * x[1] for x in c], [100 * x[2] for x in c], color=col, alpha=0.15, lw=0)
    ax.set_xlabel("layer patched (OLMo-3-7B has 32)")
    ax.set_ylabel("% of patched answers")
    ax.set_ylim(0, 60)
    ax.set_title("OLMo-3-7B-Instruct: patch the alt prompt's last two tokens", loc="left")
    ax.legend(frameon=False, loc="upper left")
    save(fig, out, "f9_olmo_slot.png")


def kept_all_layers(run: str, fam: str = "RL", layers: str = "all") -> tuple[int, int]:
    """(kept, n): the answer's statement hidden from the tokens after the question in `layers`, unedited-right items."""
    rr = rows("attn_knockout", run, file="rows.jsonl")
    ok = {r["id"] for r in rr if r["source"] == "none" and r["correct"]}
    sel = [r for r in rr if r["id"] in ok and r["family"] == fam and r["source"] == "lookup" and r["dest"] == "final"
           and r["layers"] == layers and r.get("mode", "value") == "value"]  # fmt: skip
    return sum(r["kept"] for r in sel), len(sel)


def f10_late_read_models(out: Path) -> None:
    """D2 across models: memory -> prompt still right with the statement hidden from the last tokens in every
    attention layer (and, for the hybrids, in every DeltaNet layer)."""
    models = [("Qwen3.6-27B\n(hybrid)", "d2_v4_late_read", True), ("Qwen3.5-9B\n(hybrid)", "qwen35_9b_d2_v4_late_read_r2", True),
              ("OLMo-3-7B\nInstruct", "olmo3_7b_instruct_d2_v4_late_read_v3", False),
              ("OLMo-3-7B\nSFT", "olmo3_7b_sft_d2_v4_late_read_v2", False),
              ("OLMo-3-7B\nDPO", "olmo3_7b_dpo_d2_v4_late_read_v2", False)]  # fmt: skip
    fig, ax = plt.subplots(figsize=(8.5, 3.2))
    style(ax, "y")
    for i, (_, run, hybrid) in enumerate(models):
        bar_ci(ax, i - 0.17, *wilson(*kept_all_layers(run, layers="attn" if hybrid else "all")), LOOKUP, width=0.32)
        if hybrid:
            bar_ci(ax, i + 0.17, *wilson(*kept_all_layers(run, layers="gdn")), LIGHT, width=0.32)
    ax.set_xticks(range(len(models)), [m for m, _, _ in models])
    ax.set_ylim(0, 112)
    ax.set_ylabel("% still right")
    ax.set_title("Hide the answer's statement from the last tokens (memory → prompt)", loc="left")
    handles = [plt.Rectangle((0, 0), 1, 1, color=LOOKUP), plt.Rectangle((0, 0), 1, 1, color=LIGHT)]
    ax.legend(handles, ["hidden in every attention layer", "hidden in every DeltaNet layer (hybrids only)"],
              frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2)  # fmt: skip
    save(fig, out, "f10_late_read_models.png")


def f11_natural_errors(out: Path) -> None:
    """D5a without a patch: where layer 51 head 22 looks on the model's own wrong vs right answers."""
    rr = rows("d5a_natural_errors", "d5a_natural_errors_27b", file="rows.jsonl")
    wrong = [r for r in rr if not r["right"] and r["answered"] is not None and r["answered"] != r["asked"]]
    right = [r for r in rr if r["right"]]

    def share(sel: list[dict], target: str) -> tuple[float, float, float]:
        return wilson(sum(r["heads"]["51:22"]["top"] == r[target] for r in sel), len(sel))

    fig, ax = plt.subplots(figsize=(6.5, 3.0))
    style(ax, "y")
    bar_ci(ax, 0 - 0.17, *share(wrong, "answered"), LOOKUP, width=0.32)
    bar_ci(ax, 0 + 0.17, *share(wrong, "asked"), RECALL, width=0.32)
    bar_ci(ax, 1, *share(right, "asked"), RECALL, width=0.32)
    ax.set_xticks(
        [0, 1], [f"model answers wrong\n({len(wrong)} answers)", f"model answers right\n({len(right)} answers)"]
    )
    ax.set_ylim(0, 112)
    ax.set_ylabel("% of answers")
    ax.set_title("Which statement does head 51/22 look at most?", loc="left")
    handles = [plt.Rectangle((0, 0), 1, 1, color=LOOKUP), plt.Rectangle((0, 0), 1, 1, color=RECALL)]
    ax.legend(handles, ["the statement the (wrong) answer comes from", "the right statement"], frameon=False,
              loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2)  # fmt: skip
    save(fig, out, "f11_natural_errors.png")


def f12_address_models(out: Path) -> None:
    """D3 across models: at each model's layer before the alt digit arrives (alt-digit upper bound < 10%) with the largest
    same-slot share, the same slot vs bridge alt's own statement (memory -> prompt, last two tokens)."""
    models = [("Qwen3.6-27B\n(hybrid)", "d3v4_swap_topics"), ("Qwen3-32B\n(dense)", "qwen3_32b_d3v4_swap_r2"),
              ("Qwen3.5-9B\n(hybrid)", "qwen35_9b_d3v4_swap_r2"), ("OLMo-3-7B\nInstruct", "olmo3_7b_instruct_d3v4_swap_fn"),
              ("Gemma 4\n31B-it", "gemma4it_d3v4_swap_v2_r2")]  # fmt: skip
    fig, ax = plt.subplots(figsize=(8.5, 3.2))
    style(ax, "y")
    labels = []
    for i, (name, run) in enumerate(models):
        rates = load("pointer_swap", run)["rates"]
        cells = {int(k.split("|")[4]): v for k, v in rates.items()
                 if k.startswith("RL|all|e5f0|last|") and k.endswith("|dissoc") and k.split("|")[4].isdigit()}  # fmt: skip
        pre = {la: d for la, d in cells.items() if d["value"][2] < 0.10 and d["none"][0] < 0.95}
        la, d = max(pre.items(), key=lambda t: t[1]["position"][0])
        bar_ci(ax, i - 0.17, *d["position"][:3], LOOKUP, width=0.32)
        bar_ci(ax, i + 0.17, *d["identity"][:3], RECALL, width=0.32)
        labels.append(f"{name}\nlayer {la}")
    ax.set_xticks(range(len(models)), labels, fontsize=8.5)
    ax.set_ylim(0, 70)
    ax.set_ylabel("% of patched answers")
    ax.set_title("Patched last tokens, before the digit arrives: address or word?", loc="left")
    handles = [plt.Rectangle((0, 0), 1, 1, color=LOOKUP), plt.Rectangle((0, 0), 1, 1, color=RECALL)]
    ax.legend(handles, ["the same slot (address)", "bridge alt's own statement (word)"], frameon=False,
              loc="upper right")  # fmt: skip
    save(fig, out, "f12_address_models.png")


def f13_mechanism(out: Path) -> None:
    """d3b_mechanism_27b: (a) the dose path's first landing, (b) the push at its natural size and twice it vs random,
    (c) removing the 4-dim slot subspace vs random and top-variance removals, (d) slot code vs ordinal-word directions."""
    import glob

    run = RES / "pointer_mechanism" / "d3b_mechanism_27b"
    a = json.loads(Path(sorted(glob.glob(str(run / "analysis-*" / "summary.json")))[-1]).read_text())
    words = json.loads((run / "geometry.json").read_text())["words"]["ordinal/unembedding"]
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.4), gridspec_kw={"wspace": 0.35, "width_ratios": [1.1, 1, 1.2, 1]})
    ax = axes[0]
    style(ax, "y")
    t2 = a["T2"]
    n = t2["departed"]
    for i, key in enumerate(("target", "between", "beyond")):
        k = t2["first_landing"].get(key, 0)
        bar_ci(ax, i, *wilson(k, n), LOOKUP if key == "target" else LIGHT, width=0.6)
    ax.axhline(100 * t2["chance_between"], color=INK2, lw=1, ls=":")
    ax.set_xticks([0, 1, 2], ["the target", "a slot\nin between", "past the\ntarget"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("% of first landings")
    ax.set_title("a. Push from slot a toward slot j:\nwhere does the answer go first?", loc="left", fontsize=9.5)
    ax = axes[1]
    style(ax, "y")
    t3 = a["T3"]
    for i, al in enumerate(("1.0", "2.0")):
        bar_ci(ax, i - 0.17, *t3[f"slot|{al}"]["rate"], LOOKUP, width=0.32)
        bar_ci(ax, i + 0.17, *t3[f"random|{al}"]["rate"], LIGHT, width=0.32)
    ax.set_xticks([0, 1], ["natural size", "twice natural"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("% moved to the target statement")
    ax.set_title("b. Slot direction (orange) vs\nrandom (grey), same size", loc="left", fontsize=9.5)
    ax = axes[2]
    style(ax, "y")
    t4 = a["T4"]
    for i, (fam, _) in enumerate((("RL", "memory → prompt\n(lookup)"), ("RR", "memory → memory\n(recall)"))):
        for j, (b, col) in enumerate((("slot4", LOOKUP), ("rand4", LIGHT), ("var4", INK2))):
            bar_ci(ax, i + (j - 1) * 0.26, *t4[fam][b]["rate"], col, width=0.24)
    ax.set_xticks([0, 1], ["memory → prompt\n(lookup)", "memory → memory\n(recall)"])
    ax.set_ylim(0, 112)
    ax.set_ylabel("% still right")
    ax.set_title("c. Remove 4 dims at layers 44-52:\nslot (orange), random, top variance", loc="left", fontsize=9.5)
    ax = axes[3]
    im = ax.imshow(words, cmap="RdBu_r", vmin=-0.13, vmax=0.13)
    ax.set_xticks(range(5), ["first", "second", "third", "fourth", "fifth"], fontsize=8, rotation=30)
    ax.set_yticks(range(5), [f"slot {i + 1}" for i in range(5)], fontsize=8)
    ax.set_title("d. Slot code vs the words'\noutput directions (cosine)", loc="left", fontsize=9.5)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    save(fig, out, "f13_mechanism.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="figures/readme_1021")
    out = ROOT / ap.parse_args().out
    out.mkdir(parents=True, exist_ok=True)
    for f in (f1_two_routes, f2_stated_bridge, f3_early_push, f4_late_read, f5_slot_by_layer, f6_slot_counts, f8_shifts, f9_olmo_slot,
              f7_pointer_push, f10_late_read_models, f11_natural_errors, f12_address_models, f13_mechanism):  # fmt: skip
        f(out)
