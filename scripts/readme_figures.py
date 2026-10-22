"""The README's figures: one plain figure per claim, read from the saved runs under results/ (no GPU).

Each figure states its finding in a bold title, says what was done in a grey line under it, names every control in the
legend, and uses the README's words; numbers, n and run names stay in the README caption.
  f0_patch_example.png    how a patch is read: org / alt prompts and the three possible answers (real pointer_v1 item)
  f1_two_routes.png       Zach's suite: the lens push and the J-space knock-out, lookup vs recall families
  f2_stated_bridge.png    D1: which part of a stated bridge's change switches the answer (n=80, layers 32-40)
  f3_early_push.png       D4: the early lens push (layer 20, 8x), wording B, 100 per family
  f4_late_read.png        D2: the answer's statement hidden from the last tokens, attention vs DeltaNet layers
  f5_slot_by_layer.png    D3: patched last tokens, word / slot / alt digit by layer (pointer_v4)
  f6_slot_counts.png      D3: order vs place, from the start vs from the end (pointer_v4x, layer 50)
  f7_pointer_push.png     D3b: the pointer direction vs the lens direction (layer 48)
  f8_shifts.png           D3 v6: the same slot under a shift in the text and a shift before the question
  f9_olmo_slot.png        D3 on OLMo-3-7B-Instruct by layer
  f10_late_read_models.png D2 on five models
  f11_natural_errors.png  D5a: head 51/22 on the model's own errors
  f12_address_models.png  D3 pooled over asked statements, five models (not on the README page: f14 splits it)
  f13_mechanism.png       d3b_mechanism_27b: path, natural dose, necessity
  f14_slot_by_target.png  D3 split by the statement the alt prompt asks, five models

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
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
LOOKUP, RECALL, DIGIT, GREY, LIGHT = "#eb6834", "#2a78d6", "#1baf7a", "#9aa0a6", "#c9c8c3"
INK, INK2, SURF, GRID = "#0b0b0b", "#52514e", "#ffffff", "#e6e5e0"
SLOT, WORD = LOOKUP, RECALL  # D3 figures: the same slot (orange), bridge alt's own statement (blue), alt digit (green)
plt.rcParams.update({"font.size": 10, "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK, "axes.titlesize": 10, "axes.titleweight": "bold"})  # fmt: skip
NAMES = {"BL": "prompt → prompt", "RL": "memory → prompt", "BR": "prompt → memory", "RR": "memory → memory"}
D3_ROLES = (("position", "the same slot in the org list", SLOT), ("identity", "bridge alt's own statement (word)", WORD),
            ("value", "alt prompt's own answer (digit)", DIGIT))  # fmt: skip


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


def ci3(v) -> tuple[float, float, float]:
    """(rate, lo, hi) from a saved [rate, lo, hi, ...] list."""
    return v[0], v[1], v[2]


def style(ax, axis: str = "x") -> None:
    ax.set_facecolor(SURF)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis=axis, color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def head(ax, title: str, sub: str | None = None, above: float = 0) -> None:
    """The finding (bold) and what was done (grey) above `ax`, left-aligned; `above` skips a panel title (points)."""
    y = 8 + above
    if sub:
        ax.annotate(sub, (0, 1), xycoords="axes fraction", xytext=(0, y), textcoords="offset points", fontsize=9,
                    color=INK2, va="bottom", ha="left", linespacing=1.3)  # fmt: skip
        y += 13 * (sub.count("\n") + 1) + 4
    ax.annotate(title, (0, 1), xycoords="axes fraction", xytext=(0, y), textcoords="offset points", fontsize=12,
                fontweight="bold", va="bottom", ha="left")  # fmt: skip


def box(color: str, edge: str | None = None, hatch: str | None = None) -> Rectangle:
    return Rectangle((0, 0), 1, 1, facecolor=color, edgecolor=edge or color, hatch=hatch, lw=1)


def bar_ci(ax, x, p, lo, hi, color, width=0.6, horizontal=False, label=None, fs=8.5, edge=None, hatch=None) -> None:
    lo, hi = min(lo, p), max(hi, p)  # rounding at 0% / 100% can put a bound a hair inside the point
    if horizontal:
        ax.barh(x, 100 * p, height=width, color=color, label=label, edgecolor=edge, hatch=hatch)
        ax.errorbar(100 * p, x, xerr=[[100 * (p - lo)], [100 * (hi - p)]], fmt="none", ecolor=INK2, lw=1, capsize=2)
        ax.text(100 * hi + 1.5, x, f"{100 * p:.0f}%", ha="left", va="center", fontsize=fs, color=INK)
    else:
        ax.bar(x, 100 * p, width=width, color=color, label=label, edgecolor=edge, hatch=hatch, lw=1 if edge else 0)
        ax.errorbar(x, 100 * p, yerr=[[100 * (p - lo)], [100 * (hi - p)]], fmt="none", ecolor=INK2, lw=1, capsize=2)
        ax.text(x, 100 * hi + 1.5, f"{100 * p:.0f}%", ha="center", va="bottom", fontsize=fs, color=INK)


def save(fig, out: Path, name: str) -> None:
    fig.savefig(out / name, dpi=160, facecolor=SURF, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print("wrote", out / name)


def f0_patch_example(out: Path) -> None:
    """The pointer_v1 item shown under Datasets: org and alt lists, the patch, and the three answers it can give."""
    org = [("bee", 3), ("chicken", 1), ("spider", 7), ("lion", 9), ("cat", 2)]
    alt = [("chicken", 3), ("spider", 7), ("lion", 5), ("cat", 1), ("bee", 9)]
    fig, ax = plt.subplots(figsize=(10, 3.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.55, 4.1)
    ax.axis("off")
    x0, w, gap = 1.25, 1.02, 0.1
    rows_ = [(3.15, "org prompt", org, "Which locker belongs to the animal\nknown for making honey?", "3", 2),
             (1.75, "alt prompt", alt, "Which locker belongs to the animal\nknown for its roar?", "5", 2)]  # fmt: skip
    for y, name, items, q, ans, _ in rows_:
        ax.text(0, y, name, ha="left", va="center", fontsize=10, fontweight="bold")
        for i, (e, d) in enumerate(items):
            x = x0 + i * (w + gap)
            edge, lw, face = LIGHT, 1, "#f6f6f4"
            if name == "org prompt" and i == 2:
                edge, lw, face = SLOT, 2.5, SURF
            if name == "org prompt" and e == "lion":
                edge, lw, face = WORD, 2.5, SURF
            if name == "alt prompt" and e == "lion":
                edge, lw, face = INK, 2, "#fff4e0"
            ax.add_patch(FancyBboxPatch((x, y - 0.3), w, 0.6, boxstyle="round,pad=0.02,rounding_size=0.08", fc=face,
                                        ec=edge, lw=lw))  # fmt: skip
            ax.text(x + w / 2, y, f"{e}: {d}", ha="center", va="center", fontsize=9)
            if name == "org prompt":
                ax.text(
                    x + w / 2, y + 0.42, ["1st", "2nd", "3rd", "4th", "5th"][i], ha="center", fontsize=8, color=INK2
                )
        qx = x0 + 5 * (w + gap) + 0.1
        ax.text(qx, y, q, ha="left", va="center", fontsize=8.5, color=INK2, linespacing=1.2)
        ax.text(9.75, y, f"→ {ans}", ha="left", va="center", fontsize=10, fontweight="bold")
    ax.text(x0 + 2 * (w + gap) + w / 2, 1.75 - 0.42, "asked: lion, 3rd in alt", ha="center", va="top", fontsize=8,
            color=INK)  # fmt: skip
    ax.add_patch(FancyArrowPatch((9.5, 1.95), (9.5, 2.95), arrowstyle="-|>", mutation_scale=14, color=INK, lw=1.5,
                                 connectionstyle="arc3,rad=0.0"))  # fmt: skip
    ax.text(9.43, 2.45, "copy the last 2 tokens\nat one layer", ha="right", va="center", fontsize=8.5, color=INK,
            linespacing=1.2)  # fmt: skip
    ax.text(0, 0.72, "The patched org prompt now answers:", ha="left", va="center", fontsize=9.5, fontweight="bold")
    outs = [("7", "org's 3rd statement: the same slot as the asked one", SLOT, 0.0, 0.2),
            ("9", "lion's statement in org: bridge alt's own statement (word)", WORD, 0.0, -0.3),
            ("5", "alt's own answer: the digit itself", DIGIT, 6.2, 0.2),
            ("3", "org's own answer: unchanged", GREY, 6.2, -0.3)]  # fmt: skip
    for d, txt, col, x, y in outs:
        ax.add_patch(FancyBboxPatch((x, y - 0.18), 0.3, 0.36, boxstyle="round,pad=0.02,rounding_size=0.06", fc=col,
                                    ec=col))  # fmt: skip
        ax.text(x + 0.15, y, d, ha="center", va="center", fontsize=10, color=SURF, fontweight="bold")
        ax.text(x + 0.42, y, txt, ha="left", va="center", fontsize=8.5, color=INK)
    head(ax, "How a patch is read: each possible answer is a different digit",
         "Two prompts with the same animals in a different order. We copy the alt prompt's last two tokens into the org "
         "prompt at one layer\nand read which digit comes out. Every D3 figure below counts these outcomes.")  # fmt: skip
    save(fig, out, "f0_patch_example.png")


def f1_two_routes(out: Path) -> None:
    fams = ["BL", "RL", "BR", "RR"]
    write = load("read_write", "dose_v1")["families"]
    ko = load("ablate_pilot", "abl_rot_v1")["families"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.0), sharey=True, gridspec_kw={"wspace": 0.12})
    ys = list(range(len(fams)))
    for y, f in zip(ys, fams, strict=True):
        col = LOOKUP if f.endswith("L") else RECALL
        w = write[f]["write"]
        lens = max(v["flips"] for k, v in w.items() if "/lens_" in k)
        rnd = max(v["flips"] for k, v in w.items() if "/random_" in k)
        axes[0].barh(y, 100 * lens, height=0.6, color=col)
        axes[0].text(100 * max(lens, rnd) + 2.5, y, f"{100 * lens:.0f}%", va="center", fontsize=8.5)
        axes[0].scatter([100 * rnd], [y], marker="|", s=200, linewidths=2.5, color=INK, zorder=3)
        acc = ko[f"{f}/clean"]["accuracy"]
        axes[1].barh(y, 100 * acc["jspace"], height=0.6, color=col)
        axes[1].text(100 * acc["jspace"] + 2, y, f"{100 * acc['jspace']:.0f}%", va="center", fontsize=8.5)
        axes[1].scatter([100 * acc["random"]], [y], marker="|", s=200, linewidths=2.5, color=INK, zorder=3)
    for ax in axes:
        style(ax)
        ax.set_xlim(0, 112)
    axes[0].set_yticks(ys, [NAMES[f] for f in fams])
    axes[0].invert_yaxis()
    axes[0].set_title("Push toward another animal's lens word", loc="left")
    axes[0].set_xlabel("% of answers that switch")
    axes[1].set_title("Remove the J-space", loc="left")
    axes[1].set_xlabel("% of answers still right")
    head(axes[0], "Recall goes through the J-space; a lookup in the prompt goes around it",
         "Qwen3.6-27B, animal suite, layers 32-40. Rows: where the bridge comes from → where the answer comes from.",
         above=18)  # fmt: skip
    handles = [box(LOOKUP), box(RECALL), Line2D([], [], color=INK, marker="|", ls="", ms=12, mew=2.5)]
    fig.legend(handles, ["answer looked up in the prompt", "answer recalled from memory",
                         "control: the same edit along a random direction"], loc="lower center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, -0.17))  # fmt: skip
    save(fig, out, "f1_two_routes.png")


def f2_stated_bridge(out: Path) -> None:
    cells = load("statement_positions", "d1_parts_n80_v1")["cells"]
    parts = [("full", "the whole change", INK2), ("jspace", "only the part the lens can read", RECALL),
             ("not_jspace", "everything except that part", LOOKUP)]  # fmt: skip
    groups = [("BL", "answer looked up in the prompt\n(prompt → prompt)"),
              ("BR", "answer recalled from memory\n(prompt → memory)")]  # fmt: skip
    fig, ax = plt.subplots(figsize=(8, 3.2))
    style(ax, "y")
    for gi, (fam, _) in enumerate(groups):
        c = cells[f"{fam}/context/primary"]
        n = c["n"] * len(c["layers"])
        for pi, (key, label, col) in enumerate(parts):
            k = round(c["flip"]["means"][key] * n)
            bar_ci(ax, gi + (pi - 1) * 0.26, *wilson(k, n), col, width=0.24, label=label if gi == 0 else None)
    ax.set_xticks(range(len(groups)), [g for _, g in groups])
    ax.set_ylim(0, 105)
    ax.set_ylabel("% of answers that switch")
    head(ax, "A stated bridge: the part the lens reads does nothing for a lookup",
         "Qwen3.6-27B, layers 32-40. Swap the bridge stated in the prompt (Jack's pet: cow → pig) and paste one part of\n"
         "the hidden-state change it causes into the original prompt.")  # fmt: skip
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=3)
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
    for x, txt in ((0.5, "bridge recalled from memory"), (2.5, "bridge stated in the prompt")):
        ax.annotate(txt, (x, 0), xycoords=("data", "axes fraction"), xytext=(0, -42), textcoords="offset points",
                    ha="center", fontsize=9, fontweight="bold", color=INK2)  # fmt: skip
    ax.set_ylim(0, 105)
    ax.set_ylabel("% of answers that switch")
    head(ax, "An early lens push moves a recalled bridge, not a stated one",
         "Qwen3.6-27B, layer 20: push the words that name the bridge (\"the animal known for mooing\", \"Jack's pet\")\n"
         "toward another animal's lens word.")  # fmt: skip
    handles = [box(RECALL), box(LOOKUP), box(LIGHT)]
    ax.legend(handles, ["lens push, bridge recalled", "lens push, bridge stated", "control: random push, same size"],
              frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=3)  # fmt: skip
    save(fig, out, "f3_early_push.png")


def f4_late_read(out: Path) -> None:
    run = RES / "attn_knockout" / "d2_v4_late_read"
    rr = rows("attn_knockout", "d2_v4_late_read", file="rows.jsonl")
    ok = {r["id"] for r in rr if r["source"] == "none" and r["correct"]}
    dom = {c["id"]: c.get("domain") for c in map(json.loads, (run / "cases.jsonl").read_text().splitlines())}
    k, n = collections.Counter(), collections.Counter()
    for r in rr:
        if r["id"] in ok and r["source"] in ("lookup", "lookup_off") and r.get("mode", "value") == "value" \
                and r["dest"] == "final":  # fmt: skip
            key = (r["source"], r["family"], r["layers"], dom.get(r["id"]))
            n[key] += 1
            k[key] += r["kept"]
    topics = [("countries", "countries"), ("animals", "animals"), ("body", "body parts")]
    fig, ax = plt.subplots(figsize=(8.0, 3.0))
    style(ax, "y")
    for i, (d, _) in enumerate(topics):
        for j, (src, layers, col, edge, hatch) in enumerate((("lookup", "attn", LOOKUP, None, None),
                                                             ("lookup", "gdn", LIGHT, None, None),
                                                             ("lookup_off", "attn", SURF, INK2, "///"))):  # fmt: skip
            key = (src, "RL", layers, d)
            bar_ci(ax, i + (j - 1) * 0.26, *wilson(k[key], n[key]), col, width=0.24, edge=edge, hatch=hatch)
    ax.set_xticks(range(len(topics)), [t for _, t in topics])
    ax.set_ylim(0, 115)
    ax.set_ylabel("% of answers still right")
    head(ax, "The lookup reads its statement late, through the attention layers",
         "Qwen3.6-27B (16 attention + 48 DeltaNet layers), memory → prompt. The last tokens are blocked from seeing one "
         "statement.")  # fmt: skip
    handles = [box(LOOKUP), box(LIGHT), box(SURF, INK2, "///")]
    ax.legend(handles, ["answer's statement,\nevery attention layer", "answer's statement,\nevery DeltaNet layer",
                        "control: another statement,\nevery attention layer"],
              frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, fontsize=9)  # fmt: skip
    save(fig, out, "f4_late_read.png")


def d3_cells(run: str) -> dict[int, dict]:
    rates = load("pointer_swap", run)["rates"]
    return {int(k.split("|")[4]): v for k, v in rates.items()
            if k.startswith("RL|all|e5f0|last|") and k.endswith("|dissoc") and k.split("|")[4].isdigit()}  # fmt: skip


def d3_by_layer(ax, run: str, layers: list[int] | None = None) -> None:
    """Three outcome lines by layer with 95% bands; shades the layers where the alt digit has already arrived (its
    share > 10%)."""
    cells = d3_cells(run)
    layers = layers or sorted(cells)
    i = next(t for t, la in enumerate(layers) if cells[la]["value"][0] > 0.10)
    ax.axvspan((layers[i - 1] + layers[i]) / 2, layers[-1] + 0.6, color=DIGIT, alpha=0.08, lw=0)
    for role, label, col in D3_ROLES:
        c = [cells[la][role] for la in layers]
        ax.plot(layers, [100 * x[0] for x in c], color=col, lw=2.2, marker="o", ms=4, label=label)
        ax.fill_between(layers, [100 * x[1] for x in c], [100 * x[2] for x in c], color=col, alpha=0.15, lw=0)
    ax.set_xlim(layers[0] - 0.6, layers[-1] + 0.6)
    ax.set_ylabel("% of patched answers")
    ax.legend(frameon=False, loc="upper left", fontsize=9)


def f5_slot_by_layer(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 3.4))
    style(ax, "y")
    d3_by_layer(ax, "d3v4_swap_topics")
    ax.set_xlabel("layer patched (Qwen3.6-27B has 64)")
    ax.set_ylim(0, 100)
    head(ax, "Before the digit arrives, the patched answer goes mostly to the same slot",
         "Qwen3.6-27B, memory → prompt. The alt prompt's last two tokens are copied into the org prompt at one layer "
         "(see the example\nabove). Green band: the alt digit has already reached the last tokens. The rest of the "
         "answers are unchanged.")  # fmt: skip
    save(fig, out, "f5_slot_by_layer.png")


def f6_slot_counts(out: Path) -> None:
    rates = load("pointer_swap", "d3v4x_swap_main")["rates"]
    start, end, place = (
        ("position", "k-th from\nthe start"),
        ("end", "k-th from\nthe end"),
        ("token", "same place\nin the text"),
    )
    panels = [("e5-off", "a filler line moved", [("position", "k-th in\nthe list"), place]),
              ("e5more", "alt has 6 statements", [start, end, place]),
              ("e5fewer", "alt has 4 statements", [start, end, place])]  # fmt: skip
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.0), sharey=True, gridspec_kw={"wspace": 0.08,
                                                                              "width_ratios": [2, 3, 3]})  # fmt: skip
    for ax, (lv, title, bars) in zip(axes, panels, strict=True):
        style(ax, "y")
        d = rates[f"RL|all|{lv}|last|50|dissoc"]
        for i, (role, _) in enumerate(bars):
            bar_ci(ax, i, *ci3(d[role]), SLOT if role == "position" else LIGHT, width=0.6)
        ax.set_xticks(range(len(bars)), [b for _, b in bars], fontsize=9)
        ax.set_title(title, loc="left", fontsize=9.5)
    axes[0].set_ylabel("% of patched answers")
    axes[0].set_ylim(0, 60)
    head(axes[0], "The slot is counted by order in the list, from its start",
         "Qwen3.6-27B, layer 50; the org list has 5 statements. The alt prompt asks its k-th statement, and the lists "
         "are built so\nthat three ways of counting point to three different org statements; each bar: share of answers "
         "that went there.",
         above=16)  # fmt: skip
    save(fig, out, "f6_slot_counts.png")


def f7_pointer_push(out: Path) -> None:
    sets = [("d3b_replicate_fresh_27b", "fresh scenes\n(22 entities)"),
            ("d3v4_fit_main", "new entities, unseen wording\n(85 entities)")]  # fmt: skip
    fig, ax = plt.subplots(figsize=(7.5, 3.0))
    style(ax, "y")
    for i, (run, _) in enumerate(sets):
        p = load("pointer_fit", run)["primary"]
        for j, (key, col) in enumerate((("slot", SLOT), ("lens", RECALL), ("random", LIGHT))):
            bar_ci(ax, i + (j - 1) * 0.26, *ci3(p[key]), col, width=0.24)
    ax.set_xticks(range(len(sets)), [s for _, s in sets])
    ax.set_ylim(0, 60)
    ax.set_ylabel("% moved to the target statement")
    head(
        ax,
        "A fitted slot direction can move the answer; the lens direction cannot",
        "Qwen3.6-27B, layer 48. The last tokens are pushed toward another slot, by as much as a real patch changes them.",
    )
    handles = [box(c) for c in (SLOT, RECALL, LIGHT)]
    ax.legend(handles, ["slot direction (fitted from slot averages)", "lens direction of the target's word",
                        "random direction"], frameon=False, loc="upper right", fontsize=9)  # fmt: skip
    save(fig, out, "f7_pointer_push.png")


def f8_shifts(out: Path) -> None:
    """D3 v6: under an extra sentence before the list (place in the text shifts) or before the question (distance back
    shifts), the same slot vs the moved statement; Qwen3.6-27B at layer 50, Qwen3.5-9B at layer 18 (its only swept layer
    before the alt digit arrives), OLMo-3-7B-Instruct at layer 18."""
    runs = [
        ("d3v6_swap_27b", "50", "Qwen3.6-27B (layer 50)"),
        ("qwen35_9b_d3v6_swap_r2", "18", "Qwen3.5-9B (layer 18)"),
        ("olmo3_7b_instruct_d3v6_swap", "18", "OLMo-3-7B (layer 18)"),
    ]
    fig, axes = plt.subplots(1, len(runs), figsize=(13, 3.2), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, (run, la, title) in zip(axes, runs, strict=True):
        style(ax, "y")
        rates = load("pointer_swap", run)["rates"]
        for i, (lv, moved) in enumerate((("e5-abs", "token"), ("e5-rel", "back"))):
            d = rates[f"RL|all|{lv}|last|{la}|dissoc"]
            bar_ci(ax, i - 0.17, *ci3(d["position"]), SLOT, width=0.32)
            bar_ci(ax, i + 0.17, *ci3(d[moved]), LIGHT, width=0.32)
        ax.set_xticks([0, 1], ["sentence added\nbefore the list", "sentence added\nbefore the question"])
        ax.set_title(title, loc="left", fontsize=9.5)
        ax.set_ylim(0, 65)
    axes[0].set_ylabel("% of patched answers")
    head(axes[0], "The slot is an order index: it survives both shifts",
         "One extra sentence, in one of the two prompts only. Before the list: every statement moves in the text. "
         "Before the\nquestion: every statement moves farther from the question. Their order in the list stays.",
         above=16)  # fmt: skip
    handles = [box(c) for c in (SLOT, LIGHT)]
    fig.legend(handles, ["the same number in the list", "the statement now at the same place in the text / the same "
                         "distance before the question"], loc="lower center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, -0.17), fontsize=9)  # fmt: skip
    save(fig, out, "f8_shifts.png")


def f9_olmo_slot(out: Path) -> None:
    """D3 on OLMo-3-7B-Instruct: word / slot / alt digit by layer (layers placed by function, 16-21)."""
    fig, ax = plt.subplots(figsize=(8.5, 3.4))
    style(ax, "y")
    d3_by_layer(ax, "olmo3_7b_instruct_d3v4_swap_fn", [16, 17, 18, 19, 20, 21])
    ax.set_xlabel("layer patched (OLMo-3-7B has 32)")
    ax.set_ylim(0, 60)
    head(ax, "OLMo-3-7B: before the digit arrives, slot and word tie",
         "OLMo-3-7B-Instruct, memory → prompt, the same patch as in fig. 5 (layers chosen before the run).\n"
         "Green band: the alt digit has already reached the last tokens.")  # fmt: skip
    save(fig, out, "f9_olmo_slot.png")


def kept_all_layers(run: str, fam: str = "RL", layers: str = "all", source: str = "lookup") -> tuple[int, int]:
    """(kept, n): one statement (`source`) hidden from the tokens after the question in `layers`, unedited-right items."""
    rr = rows("attn_knockout", run, file="rows.jsonl")
    ok = {r["id"] for r in rr if r["source"] == "none" and r["correct"]}
    sel = [r for r in rr if r["id"] in ok and r["family"] == fam and r["source"] == source and r["dest"] == "final"
           and r["layers"] == layers and r.get("mode", "value") == "value"]  # fmt: skip
    return sum(r["kept"] for r in sel), len(sel)


def f10_late_read_models(out: Path) -> None:
    """D2 across models: memory -> prompt still right with the statement hidden from the last tokens in every
    attention layer (and, for the hybrids, in every DeltaNet layer), and the off-path statement control."""
    models = [("Qwen3.6-27B\n(hybrid)", "d2_v4_late_read", True), ("Qwen3.5-9B\n(hybrid)", "qwen35_9b_d2_v4_late_read_r2", True),
              ("OLMo-3-7B\nInstruct", "olmo3_7b_instruct_d2_v4_late_read_v3", False),
              ("OLMo-3-7B\nSFT", "olmo3_7b_sft_d2_v4_late_read_v2", False),
              ("OLMo-3-7B\nDPO", "olmo3_7b_dpo_d2_v4_late_read_v2", False)]  # fmt: skip
    fig, ax = plt.subplots(figsize=(9.5, 3.2))
    style(ax, "y")
    for i, (_, run, hybrid) in enumerate(models):
        attn = "attn" if hybrid else "all"
        bar_ci(ax, i - 0.26, *wilson(*kept_all_layers(run, layers=attn)), LOOKUP, width=0.24)
        if hybrid:
            bar_ci(ax, i, *wilson(*kept_all_layers(run, layers="gdn")), LIGHT, width=0.24)
        else:
            ax.text(i, 3, "no DeltaNet layers", ha="center", va="bottom", fontsize=7.5, color=INK2, style="italic",
                    rotation=90)  # fmt: skip
        bar_ci(ax, i + 0.26, *wilson(*kept_all_layers(run, layers=attn, source="lookup_off")), SURF, width=0.24,
               edge=INK2, hatch="///")  # fmt: skip
    ax.set_xticks(range(len(models)), [m for m, _, _ in models])
    ax.set_ylim(0, 115)
    ax.set_ylabel("% of answers still right")
    head(
        ax,
        "The same on every model tested: blocking the attention layers breaks the lookup",
        "memory → prompt; the last tokens are blocked from seeing one statement. OLMo has attention in every layer.",
    )
    handles = [box(LOOKUP), box(LIGHT), box(SURF, INK2, "///")]
    ax.legend(handles, ["answer's statement,\nevery attention layer", "answer's statement,\nevery DeltaNet layer",
                        "control: another statement,\nevery attention layer"], frameon=False, loc="upper center",
              bbox_to_anchor=(0.5, -0.25), ncol=3, fontsize=9)  # fmt: skip
    save(fig, out, "f10_late_read_models.png")


def f11_natural_errors(out: Path) -> None:
    """D5a without a patch: where layer 51 head 22 looks on the model's own wrong vs right answers."""
    rr = rows("d5a_natural_errors", "d5a_natural_errors_27b", file="rows.jsonl")
    wrong = [r for r in rr if not r["right"] and r["answered"] is not None and r["answered"] != r["asked"]]
    right = [r for r in rr if r["right"]]

    def share(sel: list[dict], target: str) -> tuple[float, float, float]:
        return wilson(sum(r["heads"]["51:22"]["top"] == r[target] for r in sel), len(sel))

    fig, ax = plt.subplots(figsize=(7.5, 3.0))
    style(ax, "y")
    bar_ci(ax, 0 - 0.17, *share(wrong, "answered"), LOOKUP, width=0.32)
    bar_ci(ax, 0 + 0.17, *share(wrong, "asked"), RECALL, width=0.32)
    bar_ci(ax, 1, *share(right, "asked"), RECALL, width=0.32)
    ax.set_xticks([0, 1], [f"{len(wrong)} prompts the model gets wrong\n(it outputs another statement's digit)",
                           f"{len(right)} prompts the model\ngets right"])  # fmt: skip
    ax.set_ylim(0, 112)
    ax.set_ylabel("% of prompts")
    head(ax, "Head 51/22 looks at the statement the output digit comes from",
         f"Qwen3.6-27B, no patch: {len(rr)} unedited lookup prompts. Bars: how often layer 51, head 22 attends most to "
         "that\nstatement from the last token. Near-tautological: each digit appears once per scene, so the output "
         "already names it.")  # fmt: skip
    ax.legend([box(LOOKUP), box(RECALL)], ["the statement the wrong answer comes from", "the statement that was asked"],
              frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2)  # fmt: skip
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
        cells = d3_cells(run)
        pre = {la: d for la, d in cells.items() if d["value"][2] < 0.10 and d["none"][0] < 0.95}
        la, d = max(pre.items(), key=lambda t: t[1]["position"][0])
        bar_ci(ax, i - 0.17, *ci3(d["position"]), SLOT, width=0.32)
        bar_ci(ax, i + 0.17, *ci3(d["identity"]), WORD, width=0.32)
        labels.append(f"{name}\nlayer {la}")
    ax.set_xticks(range(len(models)), labels, fontsize=8.5)
    ax.set_ylim(0, 70)
    ax.set_ylabel("% of patched answers")
    head(
        ax,
        "Pooled over asked statements: slot vs word by model",
        "memory → prompt, last two tokens; fig. 14 splits it.",
    )
    ax.legend([box(SLOT), box(WORD)], ["the same slot", "bridge alt's own statement (word)"], frameon=False,
              loc="upper right")  # fmt: skip
    save(fig, out, "f12_address_models.png")


def f13_mechanism(out: Path) -> None:
    """d3b_mechanism_27b: (a) the dose path's first landing, (b) the push at its natural size and twice it vs random,
    (c) removing the 4-dim slot subspace vs random and top-variance removals. The ordinal-word cosines (T6) are
    descriptive and stay in the README text."""
    import glob

    run = RES / "pointer_mechanism" / "d3b_mechanism_27b"
    a = json.loads(Path(sorted(glob.glob(str(run / "analysis-*" / "summary.json")))[-1]).read_text())
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.4), gridspec_kw={"wspace": 0.3, "width_ratios": [1.1, 1, 1.3]})
    ax = axes[0]
    style(ax, "y")
    t2 = a["T2"]
    n = t2["departed"]
    for i, key in enumerate(("target", "between", "beyond")):
        k = t2["first_landing"].get(key, 0)
        bar_ci(ax, i, *wilson(k, n), SLOT if key == "target" else LIGHT, width=0.6)
    ch = 100 * t2["chance_between"]
    ax.plot([0.62, 1.38], [ch, ch], color=INK, lw=1.2, ls=":")
    ax.text(1.4, ch, f"chance\n({ch:.0f}%)", va="center", fontsize=8, color=INK)
    ax.set_xticks([0, 1, 2], ["the target", "a slot\nin between", "past the\ntarget"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("% of pushes (first new answer)")
    ax.set_title("a. Push slot a toward slot j, growing:\nwhere does the answer go first?", loc="left", fontsize=9.5)
    ax = axes[1]
    style(ax, "y")
    t3 = a["T3"]
    for i, al in enumerate(("1.0", "2.0")):
        bar_ci(ax, i - 0.17, *ci3(t3[f"slot|{al}"]["rate"]), SLOT, width=0.32)
        bar_ci(ax, i + 0.17, *ci3(t3[f"random|{al}"]["rate"]), LIGHT, width=0.32)
    ax.set_xticks([0, 1], ["natural size\n(slot a → slot j)", "twice that"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("% moved to the target statement")
    ax.set_title("b. How strong is it at the size\nthe model itself uses?", loc="left", fontsize=9.5)
    ax.legend([box(SLOT), box(LIGHT)], ["slot direction", "random, same size"], frameon=False, loc="upper left",
              fontsize=8.5)  # fmt: skip
    ax = axes[2]
    style(ax, "y")
    t4 = a["T4"]
    for i, fam in enumerate(("RL", "RR")):
        for j, (b, col) in enumerate((("slot4", SLOT), ("rand4", LIGHT), ("var4", INK2))):
            bar_ci(ax, i + (j - 1) * 0.27, *ci3(t4[fam][b]["rate"]), col, width=0.25, fs=7.5)
    ax.set_xticks([0, 1], ["memory → prompt\n(lookup)", "memory → memory\n(recall)"])
    ax.set_ylim(0, 112)
    ax.set_ylabel("% of answers still right")
    ax.set_title("c. Does the model need it? Remove 4 dims\nafter the question, layers 44-52", loc="left", fontsize=9.5)
    ax.legend([box(SLOT), box(LIGHT), box(INK2)], ["the slot\nsubspace", "random\n4 dims", "top-variance\n4 dims"],
              frameon=False, loc="center left", fontsize=8.5, bbox_to_anchor=(1.0, 0.5), labelspacing=1.2)  # fmt: skip
    head(axes[0], "The fitted slot direction overrides the lookup; it is not shown to be the model's own address",
         "Qwen3.6-27B, layer 48, held-out scenes, pre-registered. Slot direction: the difference between the average "
         "last-token states of two slots.", above=30)  # fmt: skip
    save(fig, out, "f13_mechanism.png")


def by_target(run: str, layer: int, level: str | None = None) -> dict[int, collections.Counter]:
    """memory -> prompt, last two tokens, one layer (and one level, if given): per alt target statement k, the count of
    each patched outcome."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts import pointer_swap as PS

    m = json.loads((RES / "pointer_swap" / run / "manifest.json").read_text())
    items = {it["id"]: it for its in PS.load_items(m).values() for it in its}
    c: dict[int, collections.Counter] = collections.defaultdict(collections.Counter)
    for r in rows("pointer_swap", run, file="outcomes.jsonl"):
        if (r["family"] == "RL" and r["source"] == "dissoc" and r["group"] == "last" and str(r["layer"]) == str(layer)
                and level in (None, r["level"])):  # fmt: skip
            c[items[r["name"]]["slots"]["position"]][r["role"]] += 1
    return dict(c)


def slot_word_panel(ax, c: dict[int, collections.Counter]) -> None:
    """Same slot (orange) and word (blue) shares by asked statement, 95% bands; the 1st and 2nd places shaded."""
    ks = sorted(c)
    xs = [k + 1 for k in ks]
    ax.axvspan(0.5, 2.5, color=SLOT, alpha=0.07, lw=0)
    for role, col in (("position", SLOT), ("identity", WORD)):
        ci = [wilson(c[k][role], sum(c[k].values())) for k in ks]
        ax.plot(xs, [100 * p for p, _, _ in ci], color=col, lw=2.2, marker="o", ms=4)
        ax.fill_between(xs, [100 * lo for _, lo, _ in ci], [100 * hi for _, _, hi in ci], color=col, alpha=0.15, lw=0)
    n_per = round(sum(sum(c[k].values()) for k in ks) / len(ks))
    ax.text(0.98, 0.97, f"~{n_per} per point", transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color=INK2)
    ax.set_xticks(xs, [str(x) for x in xs], fontsize=8.5)
    ax.set_xlim(0.6, xs[-1] + 0.4)


def f14_slot_by_target(out: Path) -> None:
    """D3 by the statement the alt prompt asks: share of patched answers at the same slot and at bridge alt's own
    statement, memory -> prompt, each model at its layer before the digit arrives; one panel per model."""
    models = [("Qwen3.6-27B", "d3v4_swap_topics", 50), ("Qwen3-32B", "qwen3_32b_d3v4_swap_r2", 50),
              ("Qwen3.5-9B", "qwen35_9b_d3v4_swap_r2", 22), ("OLMo-3-7B", "olmo3_7b_instruct_d3v4_swap_fn", 19),
              ("Gemma 4 31B", "gemma4it_d3v4_swap_v2_r2", 40)]  # fmt: skip
    fig, axes = plt.subplots(1, len(models), figsize=(13, 3.3), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, (name, run, la) in zip(axes, models, strict=True):
        style(ax, "y")
        c = by_target(run, la)
        ks = sorted(c)
        xs = [k + 1 for k in ks]
        ax.axvspan(0.5, 2.5, color=SLOT, alpha=0.07, lw=0)
        for role, col in (("position", SLOT), ("identity", WORD)):
            ci = [wilson(c[k][role], sum(c[k].values())) for k in ks]
            ax.plot(xs, [100 * p for p, _, _ in ci], color=col, lw=2.2, marker="o", ms=4)
            ax.fill_between(
                xs, [100 * lo for _, lo, _ in ci], [100 * hi for _, _, hi in ci], color=col, alpha=0.15, lw=0
            )
        unchanged = sum(c[k]["none"] for k in ks) / sum(sum(c[k].values()) for k in ks)
        n_per = round(sum(sum(c[k].values()) for k in ks) / len(ks))
        ax.set_title(f"{name}, layer {la}", loc="left", fontsize=9.5)
        ax.text(0.98, 0.97, f"~{n_per} per point\n{100 * unchanged:.0f}% unchanged", transform=ax.transAxes, ha="right",
                va="top", fontsize=7.5, color=INK2)  # fmt: skip
        ax.set_xticks(range(1, 6), ["1st", "2nd", "3rd", "4th", "5th"], fontsize=8.5)
        ax.set_xlim(0.6, 5.4)
    axes[0].set_ylim(0, 105)
    axes[0].set_ylabel("% of patched answers")
    axes[2].set_xlabel("where the alt question's answer sits in the alt list (in fig. 0: lion, 3rd)")
    head(axes[0], "The slot label covers the 1st and 2nd statements; from the 3rd on, the word steers",
         "memory → prompt, last two tokens patched at each model's layer before the alt digit arrives. Items are grouped "
         "by the place of the\nasked statement in the alt list. Orange: the answer moved to the org statement at that "
         "same place. Blue: it moved to the org\nstatement about alt's bridge animal. Shaded: 1st and 2nd places, "
         "where the same place wins on every model.", above=16)  # fmt: skip
    fig.legend([box(SLOT), box(WORD)], ["the same slot in the org list", "bridge alt's own statement (word)"],
               loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.15))  # fmt: skip
    save(fig, out, "f14_slot_by_target.png")


def f15_counts_models(out: Path) -> None:
    """D3 v4x on four models, each at its layer before the alt digit arrives: the k-th from the start, the k-th from the
    end and the same place in the text, under a moved filler and an alt list one statement longer or shorter."""
    models = [("Qwen3.6-27B", "d3v4x_swap_main", 50), ("Qwen3.5-9B", "qwen35_9b_d3v4x_swap_r2", 18),
              ("OLMo-3-7B", "olmo3_7b_instruct_d3v4x_swap", 18), ("Gemma 4 31B", "gemma4it_d3v4x_swap_r2", 40)]  # fmt: skip
    levels = [("e5-off", "filler\nmoved"), ("e5more", "alt has\n6 statements"), ("e5fewer", "alt has\n4 statements")]
    roles = [("position", SLOT), ("end", INK2), ("token", LIGHT)]
    fig, axes = plt.subplots(1, len(models), figsize=(14, 3.4), sharey=True, gridspec_kw={"wspace": 0.06})
    for ax, (name, run, la) in zip(axes, models, strict=True):
        style(ax, "y")
        rates = load("pointer_swap", run)["rates"]
        for i, (lv, _) in enumerate(levels):
            d = rates[f"RL|all|{lv}|last|{la}|dissoc"]
            for j, (role, col) in enumerate(roles):
                if (
                    role == "end" and lv == "e5-off"
                ):  # one filler moved: the k-th from the end is the k-th from the start
                    continue
                bar_ci(ax, i + (j - 1) * 0.27, *ci3(d[role]), col, width=0.25, fs=7)
        ax.set_xticks(range(len(levels)), [t for _, t in levels], fontsize=8.5)
        ax.set_title(f"{name}, layer {la}", loc="left", fontsize=9.5)
    axes[0].set_ylim(0, 50)
    axes[0].set_ylabel("% of patched answers")
    head(axes[0], "On every model the label counts by order in the list, not by place in the text",
         "memory → prompt, last two tokens, each model at its layer before the alt digit arrives. The org list has 5 "
         "statements; the alt list is changed so that\nthree ways of counting point to three different org statements. "
         "\"From the start\" beats \"from the end\" in the pre-registered test (pooled and in 2 of 3 topics) only on "
         "Qwen3.6-27B.", above=16)  # fmt: skip
    fig.legend([box(c) for _, c in roles], ["k-th from the start of the list", "k-th from the end of the list",
                                            "the same place in the text"], loc="lower center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, -0.12))  # fmt: skip
    save(fig, out, "f15_counts_models.png")


def f16_slot_by_target_v5(out: Path) -> None:
    """pointer_v5: the f14 split with 8 statements (three models) and with colour-word answers (Qwen3.5-9B, the one
    model whose same-entity control holds for colour words), each at its layer before the alt digit arrives."""
    panels = [("Qwen3.6-27B, 8 statements, layer 50", "d3v5_swap_27b", 50, "e8-digit"),
              ("Qwen3.5-9B, 8 statements, layer 18", "qwen35_9b_d3v5_swap_r2", 18, "e8-digit"),
              ("Gemma 4 31B, 8 statements, layer 40", "gemma4it_d3v5_swap_r2", 40, "e8-digit"),
              ("Qwen3.5-9B, colour words, layer 22", "qwen35_9b_d3v5_swap_r2", 22, "e5-word")]  # fmt: skip
    fig, axes = plt.subplots(1, len(panels), figsize=(14, 3.3), sharey=True,
                             gridspec_kw={"wspace": 0.06, "width_ratios": [8, 8, 8, 5]})  # fmt: skip
    for ax, (title, run, la, lv) in zip(axes, panels, strict=True):
        style(ax, "y")
        slot_word_panel(ax, by_target(run, la, lv))
        ax.set_title(title, loc="left", fontsize=9.5)
    axes[0].set_ylim(0, 105)
    axes[0].set_ylabel("% of patched answers")
    axes[1].set_xlabel("where the alt question's answer sits in the alt list")
    head(axes[0], "With 8 statements and with colour-word answers: a label for the 1st and 2nd, then the word",
         "memory → prompt, last two tokens, the same patch and split as fig. 14. Colour words: \"The cow's locker is "
         "red.\"; on Qwen3.6-27B and Gemma their same-entity\ncontrol fails (33% and 56% of answers change), so they are "
         "shown only for Qwen3.5-9B. Shaded: the 1st and 2nd places.", above=16)  # fmt: skip
    fig.legend([box(SLOT), box(WORD)], ["the same slot in the org list", "bridge alt's own statement (word)"],
               loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.12))  # fmt: skip
    save(fig, out, "f16_slot_by_target_v5.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="figures/readme_1021")
    out = ROOT / ap.parse_args().out
    out.mkdir(parents=True, exist_ok=True)
    for f in (f0_patch_example, f1_two_routes, f2_stated_bridge, f3_early_push, f4_late_read, f5_slot_by_layer,
              f6_slot_counts, f7_pointer_push, f8_shifts, f9_olmo_slot, f10_late_read_models, f11_natural_errors,
              f12_address_models, f13_mechanism, f14_slot_by_target, f15_counts_models,
              f16_slot_by_target_v5):  # fmt: skip
        f(out)
