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
D3_ROLES = (("position", "the same position in the original list", SLOT), ("identity", "the statement about the donor's entity (identity)", WORD),
            ("value", "the donor's own answer (its digit)", DIGIT))  # fmt: skip


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
    rows_ = [(3.15, "original prompt", org, "Which locker belongs to the animal\nknown for making honey?", "3", 2),
             (1.75, "donor prompt", alt, "Which locker belongs to the animal\nknown for its roar?", "5", 2)]  # fmt: skip
    for y, name, items, q, ans, _ in rows_:
        ax.text(0, y, name.replace(" ", "\n"), ha="left", va="center", fontsize=10, fontweight="bold", linespacing=1.1)
        for i, (e, d) in enumerate(items):
            x = x0 + i * (w + gap)
            edge, lw, face = LIGHT, 1, "#f6f6f4"
            if name == "original prompt" and i == 2:
                edge, lw, face = SLOT, 2.5, SURF
            if name == "original prompt" and e == "lion":
                edge, lw, face = WORD, 2.5, SURF
            if name == "donor prompt" and e == "lion":
                edge, lw, face = INK, 2, "#fff4e0"
            ax.add_patch(FancyBboxPatch((x, y - 0.3), w, 0.6, boxstyle="round,pad=0.02,rounding_size=0.08", fc=face,
                                        ec=edge, lw=lw))  # fmt: skip
            ax.text(x + w / 2, y, f"{e}: {d}", ha="center", va="center", fontsize=9)
            if name == "original prompt":
                ax.text(
                    x + w / 2, y + 0.42, ["1st", "2nd", "3rd", "4th", "5th"][i], ha="center", fontsize=8, color=INK2
                )
        qx = x0 + 5 * (w + gap) + 0.1
        ax.text(qx, y, q, ha="left", va="center", fontsize=8.5, color=INK2, linespacing=1.2)
        ax.text(9.75, y, f"→ {ans}", ha="left", va="center", fontsize=10, fontweight="bold")
    ax.text(x0 + 2 * (w + gap) + w / 2, 1.75 - 0.42, "asked: lion, 3rd in the donor list", ha="center", va="top", fontsize=8,
            color=INK)  # fmt: skip
    ax.add_patch(FancyArrowPatch((9.5, 1.95), (9.5, 2.95), arrowstyle="-|>", mutation_scale=14, color=INK, lw=1.5,
                                 connectionstyle="arc3,rad=0.0"))  # fmt: skip
    ax.text(9.43, 2.45, "copy the last 2 tokens\nat one layer", ha="right", va="center", fontsize=8.5, color=INK,
            linespacing=1.2)  # fmt: skip
    ax.text(
        0, 0.72, "After the copy, the original prompt answers:", ha="left", va="center", fontsize=9.5, fontweight="bold"
    )
    outs = [("7", "its 3rd statement: the same position as the one asked", SLOT, 0.0, 0.2),
            ("9", "its statement about lion: the donor's entity (identity)", WORD, 0.0, -0.3),
            ("5", "the donor's own answer: the digit itself", DIGIT, 6.2, 0.2),
            ("3", "its own answer: unchanged", GREY, 6.2, -0.3)]  # fmt: skip
    for d, txt, col, x, y in outs:
        ax.add_patch(FancyBboxPatch((x, y - 0.18), 0.3, 0.36, boxstyle="round,pad=0.02,rounding_size=0.06", fc=col,
                                    ec=col))  # fmt: skip
        ax.text(x + 0.15, y, d, ha="center", va="center", fontsize=10, color=SURF, fontweight="bold")
        ax.text(x + 0.42, y, txt, ha="left", va="center", fontsize=8.5, color=INK)
    head(ax, "How a patch is read: each possible answer is a different digit",
         "Two prompts with the same animals in a different order. We copy the donor prompt's last two tokens into the original "
         "prompt at one layer\nand read which digit comes out. Every figure of slide 4 counts these outcomes.")  # fmt: skip
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
    """D4: at layer 20 (8x), the lens push on the subject phrase vs editing the input word itself (E-name: the subject
    phrase replaced by 'the X') and a random push, per family."""
    hit, n = collections.Counter(), collections.Counter()
    for r in rows("early_push", "d4_push_wording_b_v1", file="outcomes.jsonl"):
        if "prompt" in r:
            continue
        if r.get("kind") == "edit" and r.get("edit") == "E-name":
            key = (r["family"], "edit")
        elif r.get("kind") == "push" and r.get("subset") == "b" and str(r["layer"]) == "20" and r["scale"] == 8.0:
            key = (r["family"], r["dir"])
        else:
            continue
        n[key] += 1
        hit[key] += r["role"] == "b"
    fams = ["RL", "RR", "BL", "BR"]
    fig, ax = plt.subplots(figsize=(8.5, 3.2))
    style(ax, "y")
    for i, f in enumerate(fams):
        col = RECALL if f.startswith("R") else LOOKUP
        bar_ci(ax, i - 0.27, *wilson(hit[(f, "edit")], n[(f, "edit")]), INK2, width=0.25, fs=7.5)
        bar_ci(ax, i, *wilson(hit[(f, "lens")], n[(f, "lens")]), col, width=0.25, fs=7.5)
        bar_ci(ax, i + 0.27, *wilson(hit[(f, "random")], n[(f, "random")]), LIGHT, width=0.25, fs=7.5)
    ax.set_xticks(range(len(fams)), [NAMES[f].replace(" → ", "\n→ ") for f in fams])
    for x, txt in ((0.5, "bridge recalled from memory"), (2.5, "bridge stated in the prompt")):
        ax.annotate(txt, (x, 0), xycoords=("data", "axes fraction"), xytext=(0, -42), textcoords="offset points",
                    ha="center", fontsize=9, fontweight="bold", color=INK2)  # fmt: skip
    ax.set_ylim(0, 112)
    ax.set_ylabel("% of answers that switch")
    head(ax, "An early lens push is not an input edit: it moves only a recalled bridge",
         "Qwen3.6-27B, layer 20: push the words that name the bridge (\"the animal known for mooing\", \"Jack's pet\")\n"
         "toward another animal's lens word, or edit those words to name the other animal (\"the sheep\").")  # fmt: skip
    handles = [box(INK2), box(RECALL), box(LOOKUP), box(LIGHT)]
    ax.legend(handles, ["input words edited", "lens push, bridge recalled", "lens push, bridge stated",
                        "control: random push"], frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.3),
              ncol=4, fontsize=9)  # fmt: skip
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


def d3_by_layer(ax, run: str, layers: list[int] | None = None, legend: bool = True) -> None:
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
    if legend:
        ax.legend(frameon=False, loc="upper left", fontsize=9)


def f17_by_layer_models(out: Path) -> None:
    """D3 on five models: the three outcomes of the last-two-token patch by layer (memory -> prompt, pooled over asked
    statements); the green band marks the layers where the alt digit has arrived."""
    models = [("Qwen3.6-27B (64 layers)", "d3v4_swap_topics", [40, 44, 46, 48, 50, 52, 56]),
              ("Qwen3-32B (64 layers)", "qwen3_32b_d3v4_swap_r2", None),
              ("Qwen3.5-9B (32 layers)", "qwen35_9b_d3v4_swap_r2", None),
              ("OLMo-3-7B (32 layers)", "olmo3_7b_instruct_d3v4_swap_fn", [16, 17, 18, 19, 20, 21]),
              ("Gemma 4 31B (60 layers)", "gemma4it_d3v4_swap_v2_r2", None)]  # fmt: skip
    fig, axes = plt.subplots(1, len(models), figsize=(15, 3.3), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, (name, run, layers) in zip(axes, models, strict=True):
        style(ax, "y")
        d3_by_layer(ax, run, layers, legend=False)
        ax.set_title(name, loc="left", fontsize=9.5)
        ax.set_ylabel("")
    axes[0].set_ylim(0, 100)
    axes[0].set_ylabel("% of patched answers")
    axes[2].set_xlabel("layer at which the last two tokens are copied")
    head(axes[0], "On every model a short window before the digit arrives, where the patch moves the answer to another "
         "statement",
         "memory → prompt; the donor prompt's last two tokens are copied into the original prompt at one layer (see the example "
         "above). Green band: the donor's\ndigit has already reached the last tokens, so the copy carries the answer itself. "
         "The rest of the answers are unchanged.", above=16)  # fmt: skip
    fig.legend([box(c) for _, _, c in D3_ROLES], [lab for _, lab, _ in D3_ROLES], loc="lower center", ncol=3,
               frameon=False, bbox_to_anchor=(0.5, -0.13))  # fmt: skip
    save(fig, out, "f17_by_layer_models.png")


def f5_slot_by_layer(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 3.4))
    style(ax, "y")
    d3_by_layer(ax, "d3v4_swap_topics")
    ax.set_xlabel("layer patched (Qwen3.6-27B has 64)")
    ax.set_ylim(0, 100)
    head(ax, "Before the digit arrives, the patched answer goes mostly to the same position in the list",
         "Qwen3.6-27B, memory → prompt. The donor prompt's last two tokens are copied into the original prompt at one layer "
         "(see the example\nabove). Green band: the donor's digit has already reached the last tokens. The rest of the "
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
              ("e5more", "donor list has 6 statements", [start, end, place]),
              ("e5fewer", "donor list has 4 statements", [start, end, place])]  # fmt: skip
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
    head(axes[0], "The position label counts by order in the list, from its start",
         "Qwen3.6-27B, layer 50; the original list has 5 statements. The donor prompt asks its k-th statement, and the lists "
         "are built so\nthat three ways of counting point to three different original statements; each bar: share of answers "
         "that went there.",
         above=16)  # fmt: skip
    save(fig, out, "f6_slot_counts.png")


def f7_pointer_push(out: Path) -> None:
    sets = [("d3b_replicate_fresh_27b", "Qwen3.6-27B, layer 48\nfresh scenes"),
            ("d3v4_fit_main", "Qwen3.6-27B, layer 48\nnew entities and wording"),
            ("olmo3_7b_instruct_d3b_fit_v2", "OLMo-3-7B, layer 18\nnew entities and wording")]  # fmt: skip
    fig, ax = plt.subplots(figsize=(9, 3.0))
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
        "A fitted position direction can move the answer on Qwen3.6-27B; the lens direction cannot",
        "The last tokens are pushed toward another position, by as much as a real patch changes them; held-out scenes.",
    )
    handles = [box(c) for c in (SLOT, RECALL, LIGHT)]
    ax.legend(handles, ["position direction (fitted from position averages)", "lens direction of the target's word",
                        "random direction"], frameon=False, loc="upper right", fontsize=9)  # fmt: skip
    save(fig, out, "f7_pointer_push.png")


def f8_shifts(out: Path) -> None:
    """D3 v6: under an extra sentence before the list (place in the text shifts) or before the question (distance back
    shifts), the same slot vs the moved statement; Qwen3.6-27B at layer 50, Qwen3.5-9B at layer 18 and Gemma 4 at layer
    40 (their only swept layers before the alt digit arrives), OLMo-3-7B-Instruct at layer 18."""
    runs = [
        ("d3v6_swap_27b", "50", "Qwen3.6-27B (layer 50)"),
        ("qwen35_9b_d3v6_swap_r2", "18", "Qwen3.5-9B (layer 18)"),
        ("olmo3_7b_instruct_d3v6_swap", "18", "OLMo-3-7B (layer 18)"),
        ("gemma4it_d3v6_swap_r2", "40", "Gemma 4 31B (layer 40)"),
    ]
    fig, axes = plt.subplots(1, len(runs), figsize=(15, 3.2), sharey=True, gridspec_kw={"wspace": 0.08})
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
    head(axes[0], "The order label counts order in the list: it survives both shifts",
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
    head(ax, "OLMo-3-7B: before the digit arrives, position and identity tie",
         "OLMo-3-7B-Instruct, memory → prompt, the same patch as in fig. 5 (layers chosen before the run).\n"
         "Green band: the donor's digit has already reached the last tokens.")  # fmt: skip
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
              ("Qwen3-32B\n(attention only)", "qwen3_32b_d2_v4_late_read_v2_r2", False),
              ("OLMo-3-7B\nInstruct", "olmo3_7b_instruct_d2_v4_late_read_v3", False),
              ("OLMo-3-7B\nSFT", "olmo3_7b_sft_d2_v4_late_read_v2", False),
              ("OLMo-3-7B\nDPO", "olmo3_7b_dpo_d2_v4_late_read_v2", False),
              ("Gemma 4 31B\n(sliding\n+ global)", "gemma4it_d2_v4_late_read_v3_r2", False)]  # fmt: skip
    fig, ax = plt.subplots(figsize=(12, 3.2))
    style(ax, "y")
    for i, (_, run, hybrid) in enumerate(models):
        attn = "attn" if hybrid else "all"
        bar_ci(ax, i - 0.26, *wilson(*kept_all_layers(run, layers=attn)), LOOKUP, width=0.24, fs=7.5)
        if hybrid:
            bar_ci(ax, i, *wilson(*kept_all_layers(run, layers="gdn")), LIGHT, width=0.24, fs=7.5)
        else:
            ax.text(i, 3, "no DeltaNet layers", ha="center", va="bottom", fontsize=7.5, color=INK2, style="italic",
                    rotation=90)  # fmt: skip
        bar_ci(ax, i + 0.26, *wilson(*kept_all_layers(run, layers=attn, source="lookup_off")), SURF, width=0.24, fs=7.5,
               edge=INK2, hatch="///")  # fmt: skip
    ax.set_xticks(range(len(models)), [m for m, _, _ in models])
    ax.set_ylim(0, 115)
    ax.set_ylabel("% of answers still right")
    ax.axhline(20, color=INK, lw=1, ls=":")
    ax.annotate("guessing among\nthe list's 5 digits", (1.0, 20), xycoords=("axes fraction", "data"), xytext=(4, 0),
                textcoords="offset points", ha="left", va="center", fontsize=8, color=INK)  # fmt: skip
    head(ax, "On every model tested, blocking the attention layers breaks the lookup down to guessing",
         "memory → prompt; the last tokens are blocked from seeing one statement. 72-96% of the answers then go to another "
         "digit of the list.\nQwen3-32B, OLMo and Gemma have attention in every layer.")  # fmt: skip
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
    head(ax, "Layer 51, head 22 looks at the statement the output digit comes from",
         f"Qwen3.6-27B, no edit: {len(rr)} lookup prompts as they are. Bars: how often layer 51, head 22 attends most to "
         "that\nstatement from the last token. Near-tautological: each digit appears once per scene, so the output "
         "already names it.")  # fmt: skip
    ax.legend([box(LOOKUP), box(RECALL)], ["the statement the wrong answer comes from", "the statement that was asked"],
              frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2)  # fmt: skip
    save(fig, out, "f11_natural_errors.png")


def f12_address_models(out: Path) -> None:
    """D3 across models: at each model's layer before the alt digit arrives (alt-digit upper bound < 10%) with the largest
    same-slot share, the same slot vs bridge alt's own statement (memory -> prompt, last two tokens)."""
    models = [("Qwen3.6-27B\n(hybrid)", "d3v4_swap_topics"), ("Qwen3-32B\n(attention only)", "qwen3_32b_d3v4_swap_r2"),
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
        "Pooled over asked statements: position vs identity by model",
        "memory → prompt, last two tokens; fig. 14 splits it.",
    )
    ax.legend([box(SLOT), box(WORD)], ["the same position", "the statement about the donor's entity (identity)"], frameon=False,
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
    ax.set_xticks([0, 1, 2], ["the target", "a position\nin between", "past the\ntarget"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("% of pushes\n(where the answer goes first)")
    ax.set_title(
        "a. A growing push from position a\ntoward position j: where does\nthe answer go first?",
        loc="left",
        fontsize=9.5,
    )
    ax = axes[1]
    style(ax, "y")
    t3 = a["T3"]
    for i, al in enumerate(("1.0", "2.0")):
        bar_ci(ax, i - 0.17, *ci3(t3[f"slot|{al}"]["rate"]), SLOT, width=0.32)
        bar_ci(ax, i + 0.17, *ci3(t3[f"random|{al}"]["rate"]), LIGHT, width=0.32)
    ax.set_xticks([0, 1], ["natural size\n(position a → position j)", "twice that"])
    ax.set_ylim(0, 100)
    ax.set_ylabel("% moved to the target statement")
    ax.set_title("b. How strong is it at the size\nthe model itself uses?", loc="left", fontsize=9.5)
    ax.legend([box(SLOT), box(LIGHT)], ["position direction", "random, same size"], frameon=False, loc="upper left",
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
    ax.set_title(
        "c. Does the model need it? Remove these 4 directions\nfrom the tokens after the question, layers 44-52",
        loc="left",
        fontsize=9.5,
    )
    ax.legend([box(SLOT), box(LIGHT), box(INK2)], ["the 4 position\ndirections", "4 random\ndirections", "the 4 directions\nof largest variance"],
              frameon=False, loc="center left", fontsize=8.5, bbox_to_anchor=(1.0, 0.5), labelspacing=1.2)  # fmt: skip
    head(axes[0], "The fitted position direction overrides the lookup; it is not shown to be the model's own address",
         "Qwen3.6-27B, layer 48, scenes not used for the fit, pre-registered. Position direction: the difference between "
         "the average last-token states of two list positions.", above=30)  # fmt: skip
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
              ("Qwen3.5-9B", "qwen35_9b_d3v4_swap_r2", 21), ("OLMo-3-7B", "olmo3_7b_instruct_d3v4_swap_fn", 18),
              ("Gemma 4 31B", "gemma4it_d3v4_swap_v2_r2", 40)]  # fmt: skip  # each model's last layer with alt digit UB < 10%
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
    axes[2].set_xlabel("where the donor's asked statement sits in the donor list (in the example: lion, 3rd)")
    head(axes[0], "An order label picks the 1st and 2nd statements; from the 3rd on, the bridge's identity picks",
         "memory → prompt, last two tokens patched at each model's layer before the donor's digit arrives. Items are grouped "
         "by the place of the\nasked statement in the donor list. Orange: the answer moved to the original statement at that "
         "same place. Blue: it moved to the original\nstatement about the donor's animal. Shaded: 1st and 2nd places, "
         "where the same place leads on every model.", above=16)  # fmt: skip
    fig.legend([box(SLOT), box(WORD)], ["the same position in the original list", "the statement about the donor's entity (identity)"],
               loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.15))  # fmt: skip
    save(fig, out, "f14_slot_by_target.png")


def f15_counts_models(out: Path) -> None:
    """D3 v4x on four models, each at its layer before the alt digit arrives: the k-th from the start, the k-th from the
    end and the same place in the text, under a moved filler and an alt list one statement longer or shorter."""
    models = [("Qwen3.6-27B", "d3v4x_swap_main", 50), ("Qwen3.5-9B", "qwen35_9b_d3v4x_swap_r2", 18),
              ("OLMo-3-7B", "olmo3_7b_instruct_d3v4x_swap", 18), ("Gemma 4 31B", "gemma4it_d3v4x_swap_r2", 40)]  # fmt: skip
    levels = [
        ("e5-off", "filler\nmoved"),
        ("e5more", "donor list\none longer"),
        ("e5fewer", "donor list\none shorter"),
    ]
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
         "memory → prompt, last two tokens, each model at its layer before the donor's digit arrives. The original list has 5 "
         "statements; the donor list is changed so that\nthree ways of counting point to three different original statements. "
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
    axes[1].set_xlabel("where the donor's asked statement sits in the donor list")
    head(axes[0], "With 8 statements and with colour-word answers: an order label for the 1st and 2nd, then the bridge's identity",
         "memory → prompt, last two tokens copied from a donor prompt, split by the asked statement. Colour words: \"The cow's locker is "
         "red.\"; on Qwen3.6-27B and Gemma their control (a donor prompt about the\nsame entity, which should change nothing) fails: 33% and 56% of answers change, so they are "
         "shown only for Qwen3.5-9B. Shaded: the 1st and 2nd places.", above=16)  # fmt: skip
    fig.legend([box(SLOT), box(WORD)], ["the same position in the original list", "the statement about the donor's entity (identity)"],
               loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.12))  # fmt: skip
    save(fig, out, "f16_slot_by_target_v5.png")


STAGE_MODELS = [  # name, architecture, layers, D3 run (pointer_v4), D2 run (late read)
    ("Qwen3.6-27B", "hybrid: 16 attention + 48 DeltaNet", 64, "d3v4_swap_topics", "d2_v4_late_read"),
    ("Qwen3-32B", "attention in every layer", 64, "qwen3_32b_d3v4_swap_r2", "qwen3_32b_d2_v4_late_read_v2_r2"),
    ("Qwen3.5-9B", "hybrid: 8 attention + 24 DeltaNet", 32, "qwen35_9b_d3v4_swap_r2", "qwen35_9b_d2_v4_late_read_r2"),
    ("OLMo-3-7B", "attention, 3 of 4 sliding", 32, "olmo3_7b_instruct_d3v4_swap_fn", "olmo3_7b_instruct_d2_v4_late_read_v3"),
    ("Gemma 4 31B", "attention, sliding + global", 60, "gemma4it_d3v4_swap_v2_r2", "gemma4it_d2_v4_late_read_v3_r2"),
]  # fmt: skip


def stages(d3: str, d2: str) -> dict:
    """One model's layer stages, memory -> prompt: the patch window (answers move, alt digit upper bound < 10%), the
    first layer where the alt digit reaches the last tokens (>= 10%), and the D2 layer bands that must stay open (the
    narrowest 'needed' bands, and the widest ones that contain them)."""
    import glob

    cells = d3_cells(d3)
    window = [la for la in sorted(cells) if cells[la]["none"][0] <= 0.90 and cells[la]["value"][2] < 0.10]
    digit = next(la for la in sorted(cells) if cells[la]["value"][0] >= 0.10)
    an = [a for a in sorted(glob.glob(str(RES / "attn_knockout" / d2 / "analysis-*-figures" / "summary.json")))
          if "partial" not in a]  # fmt: skip
    final = json.loads(Path(an[-1]).read_text())["claims"]["late_attention_read"]["RL"]["final"]
    needed = []
    for k, v in final.items():
        if k.startswith("band") and ":" not in k and v["verdict"] == "needed":
            a, b = (int(x) for x in k[4:].split("-"))
            needed.append((a, b))
    width = min(b - a for a, b in needed)
    return {
        "window": (window[0], window[-1]),
        "digit": digit,
        "read": max(needed, key=lambda t: t[1] - t[0]),
        "core": [t for t in needed if t[1] - t[0] == width],
    }


def f18_stages_models(out: Path) -> None:
    """Across models: where along the depth the patch window, the read (D2) and the digit's arrival sit."""
    fig, ax = plt.subplots(figsize=(11, 3.6))
    style(ax)
    for i, (_, _, nl, d3, d2) in enumerate(STAGE_MODELS):
        s = stages(d3, d2)

        def pct(layer: float, nl: int = nl) -> float:
            return 100 * layer / nl

        a, b = s["read"]
        ax.barh(i, pct(b + 1) - pct(a), left=pct(a), height=0.62, color=LIGHT)
        for a2, b2 in s["core"]:
            if (a2, b2) != (a, b):
                ax.barh(i, pct(b2 + 1) - pct(a2), left=pct(a2), height=0.62, color=GREY)
        w0, w1 = s["window"]
        ax.barh(i, pct(w1 + 1) - pct(w0), left=pct(w0), height=0.26, color=SLOT)
        ax.scatter([pct(s["digit"])], [i], marker="D", s=50, color=DIGIT, zorder=3)
        core = ", ".join(f"{a2}-{b2}" for a2, b2 in s["core"] if (a2, b2) != (a, b))
        win = f"{w0}" if w0 == w1 else f"{w0}-{w1}"
        ax.text(101, i, f"label or identity: {win} · read: {a}-{b}{f' (most {core})' if core else ''} · digit arrives: {s['digit']}",
                va="center", fontsize=8.5, color=INK)  # fmt: skip
    ax.set_yticks(range(len(STAGE_MODELS)), [f"{n} ({nl} layers)\n{arch}" for n, arch, nl, _, _ in STAGE_MODELS],
                  fontsize=8.5)  # fmt: skip
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("depth (% of the model's layers)")
    head(ax, "Where the stages sit along the depth, by model",
         "memory → prompt. Orange: layers where copying the last two tokens from a donor prompt moves the answer to another statement "
         "(label or identity). Grey: the layer block\nthe last tokens must be able to attend to the answer's statement in "
         "(blocking is tested in blocks of 8-16 layers, so it does not order the read against the orange window;\ndarker: "
         "the narrowest block that is needed alone). Green: the donor's digit has reached the last tokens.")  # fmt: skip
    save(fig, out, "f18_stages_models.png")


def f19_where_bridge(out: Path) -> None:
    """D1 map (Qwen3.6-27B, animal suite): copying one set of positions from a prompt with another bridge, by layer;
    a stated bridge (prompt -> prompt) vs a recalled one (memory -> prompt)."""
    rates = json.loads((RES / "statement_positions" / "d1_map_n80_v1" / "summary.json").read_text())["rates"]
    sets = [("context", "the statements", "#6250d6"), ("question", "the question", RECALL),
            ("final", "the last tokens", INK2)]  # fmt: skip
    panels = [("BL", "bridge stated in the prompt (prompt → prompt)"),
              ("RL", "bridge recalled from memory (memory → prompt)")]  # fmt: skip
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.2), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, (fam, title) in zip(axes, panels, strict=True):
        style(ax, "y")
        for key, label, col in sets:
            pts = sorted((r["layer"], r["cf"]["flips"]) for r in rates if r["family"] == fam and r["set"] == key)
            if fam == "RL" and key == "context":
                continue  # the statements are the same in both prompts: copying them is an exact no-op
            ax.plot([p[0] for p in pts], [100 * p[1][0] for p in pts], color=col, lw=2.2, marker="o", ms=4, label=label)
            ax.fill_between([p[0] for p in pts], [100 * max(p[1][1], 0) for p in pts], [100 * p[1][2] for p in pts],
                            color=col, alpha=0.15, lw=0)  # fmt: skip
        ax.set_title(title, loc="left", fontsize=9.5)
        ax.set_xlabel("layer (Qwen3.6-27B has 64)")
        ax.set_xticks(range(32, 53, 4))
    axes[0].set_ylim(0, 105)
    axes[0].set_ylabel("% of answers that switch")
    axes[0].legend(frameon=False, loc="center left", fontsize=9, title="positions copied", title_fontsize=9)
    head(axes[0], "A stated bridge waits at its statement until layer ~44; a recalled one sits at the question",
         "Qwen3.6-27B, animal suite: copy the hidden states of one group of tokens from a donor prompt with another bridge "
         "and count answers that switch.\nIn memory → prompt the statements are the same in both prompts, so copying "
         "them changes nothing and is not drawn.", above=16)  # fmt: skip
    save(fig, out, "f19_where_bridge.png")


def f20_olmo_ladder(out: Path) -> None:
    """OLMo-3-7B post-training ladder (SFT -> DPO -> Instruct): the late read (D2), the 1st / 2nd label and the bridge identity
    from the 3rd on (D3, layer 18), order vs place (D3 v4x, filler moved, layer 18)."""
    ladder = [("SFT", "olmo3_7b_sft_d2_v4_late_read_v2", "olmo3_7b_sft_d3v4_swap", "olmo3_7b_sft_d3v4x_swap"),
              ("DPO", "olmo3_7b_dpo_d2_v4_late_read_v2", "olmo3_7b_dpo_d3v4_swap", "olmo3_7b_dpo_d3v4x_swap"),
              ("Instruct", "olmo3_7b_instruct_d2_v4_late_read_v3", "olmo3_7b_instruct_d3v4_swap_fn",
               "olmo3_7b_instruct_d3v4x_swap")]  # fmt: skip
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.2), gridspec_kw={"wspace": 0.25})
    for i, (_, d2, d3, d3x) in enumerate(ladder):
        bar_ci(axes[0], i - 0.17, *wilson(*kept_all_layers(d2)), LOOKUP, width=0.32, fs=7.5)
        bar_ci(axes[0], i + 0.17, *wilson(*kept_all_layers(d2, source="lookup_off")), SURF, width=0.32, fs=7.5,
               edge=INK2, hatch="///")  # fmt: skip
        c = by_target(d3, 18)
        first2 = sum(c[k]["position"] for k in (0, 1)), sum(sum(c[k].values()) for k in (0, 1))
        rest = sum(c[k]["identity"] for k in c if k >= 2), sum(sum(c[k].values()) for k in c if k >= 2)
        bar_ci(axes[1], i - 0.17, *wilson(*first2), SLOT, width=0.32, fs=7.5)
        bar_ci(axes[1], i + 0.17, *wilson(*rest), WORD, width=0.32, fs=7.5)
        d = load("pointer_swap", d3x)["rates"]["RL|all|e5-off|last|18|dissoc"]
        bar_ci(axes[2], i - 0.17, *ci3(d["position"]), SLOT, width=0.32, fs=7.5)
        bar_ci(axes[2], i + 0.17, *ci3(d["token"]), LIGHT, width=0.32, fs=7.5)
    titles = [("Late read: statement blocked\nfrom the last tokens", "% still right",
               [box(LOOKUP), box(SURF, INK2, "///")], ["answer's statement", "control: another statement"]),
              ("Copy from a donor prompt,\nby the asked statement", "% of patched answers", [box(SLOT), box(WORD)],
               ["1st / 2nd: same position", "3rd-5th: the bridge's identity"]),
              ("How the label counts\n(filler moved)", "% of patched answers", [box(SLOT), box(LIGHT)],
               ["order in the list", "place in the text"])]  # fmt: skip
    for ax, (t, yl, h, labs) in zip(axes, titles, strict=True):
        style(ax, "y")
        ax.set_xticks(range(len(ladder)), [n for n, *_ in ladder])
        ax.set_title(t, loc="left", fontsize=9.5)
        ax.set_ylabel(yl)
        ax.set_ylim(0, 115)
        ax.legend(h, labs, frameon=False, loc="upper center", fontsize=8, ncol=1, bbox_to_anchor=(0.5, -0.12))
    head(axes[0], "OLMo-3-7B across post-training (SFT → DPO → Instruct): the same picture at every stage",
         "memory → prompt. Middle and right: the last two tokens copied from a donor prompt at layer 18 (before the donor's digit arrives).", above=30)  # fmt: skip
    save(fig, out, "f20_olmo_ladder.png")


def f21_name_vs_digit(out: Path) -> None:
    """d2_parts v2 on four models, memory -> prompt: % right with one part of the answer's statement hidden from the
    question's tokens or from the last tokens, in every layer."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts import d2_parts as P

    models = [("Qwen3.6-27B", "d2_parts_v2_27b"), ("Qwen3-32B", "qwen3_32b_d2_parts_v2"),
              ("Qwen3.5-9B", "qwen35_9b_d2_parts_v2"), ("OLMo-3-7B", "olmo3_7b_instruct_d2_parts_v2")]  # fmt: skip
    bars = [("lookup", "whole statement", INK2, None), ("lookup_name", "name only", RECALL, None),
            ("lookup_nodigit", "name + rest (all but the digit)", "#9cc1ee", None),
            ("lookup_digit", "digit only", DIGIT, None), ("lookup_noname", "digit + rest (all but the name)", "#93dcc0", None),
            ("lookup_off", "control: another statement", SURF, "///")]  # fmt: skip
    fig, axes = plt.subplots(2, 1, figsize=(12, 6.6), sharey=True, gridspec_kw={"hspace": 0.32})
    w = 0.13
    for ax, dest, title in zip(axes, ("question", "final"), ("hidden from the question's tokens", "hidden from the last tokens"),
                               strict=True):  # fmt: skip
        style(ax, "y")
        for i, (_, run) in enumerate(models):
            d = RES / "attn_knockout" / run
            cases = {c["id"]: c for c in map(json.loads, (d / "cases.jsonl").read_text().splitlines())}
            cl = P.cells([json.loads(x) for x in (d / "rows.jsonl").read_text().splitlines()], cases)
            for j, (src, _, col, hatch) in enumerate(bars):
                p, lo, hi = cl[("RL", src, dest)]["right"]
                bar_ci(ax, i + (j - 2.5) * w, p, lo, hi, col, width=w * 0.95, fs=7.5,
                       edge=INK2 if hatch else None, hatch=hatch)  # fmt: skip
        ax.axhline(20, color=INK, lw=1, ls=":")
        ax.set_xticks(range(len(models)), [m for m, _ in models])
        ax.set_title(title, loc="left", fontsize=9.5)
        ax.set_ylim(0, 115)
        ax.set_ylabel("% of answers still right")
    head(axes[0], "The question's tokens take the entity's name; the last tokens take the digit",
         "memory → prompt: one part of the answer's statement (\"The file on Greece is kept in drawer 1.\") is hidden in "
         "every layer. Dotted: guessing among the list's 5 digits.", above=16)  # fmt: skip
    fig.legend([box(c, INK2 if h else None, h) for _, _, c, h in bars], [lab for _, lab, _, _ in bars],
               loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.06), fontsize=9)  # fmt: skip
    save(fig, out, "f21_name_vs_digit.png")


C2_DIR = RES / "c2_cells" / "step_a_20261022"  # scripts/c2_cells.py select + reveal on the two sweeps


def f22_c2_positive_control(out: Path) -> None:
    """Sharp C2 step a: (left) where the lens push writes recall, by layer and topic (memory -> memory, the larger of
    1x / 2x), with the selection bar; (right) in the selected cells, lookups of statements 3-5: patch, lens, random,
    and the same lens push on recall."""
    sel = json.loads((C2_DIR / "cells.json").read_text())["cells"]
    rev = json.loads((C2_DIR / "reveal.json").read_text())
    topics = sorted({(c["run"], c["domain"]) for c in sel})
    names = {"c2_sweep_v4_27b": "85-entity set", "c2_sweep_v1_27b": "locker lists"}  # README datasets
    plain = {"body": "body parts"}
    cols = [LOOKUP, RECALL, DIGIT, "#6250d6", "#eda100", INK2]
    fig, axes = plt.subplots(1, 2, figsize=(13, 3.6), gridspec_kw={"wspace": 0.25, "width_ratios": [1.3, 1]})
    ax = axes[0]
    style(ax, "y")
    for (run, dom), col in zip(topics, cols, strict=False):
        cs = sorted((c for c in sel if (c["run"], c["domain"]) == (run, dom)), key=lambda c: c["layer"])
        ys = [100 * max(v["rate"] for v in c["rr_lens"].values()) for c in cs]
        ax.plot([c["layer"] for c in cs], ys, color=col, lw=2, marker="o", ms=4,
                label=f"{plain.get(dom, dom)} ({names.get(run, run)})")  # fmt: skip
        for c, y in zip(cs, ys, strict=True):
            if c["selected"]:
                ax.scatter([c["layer"]], [y], s=90, facecolors="none", edgecolors=INK, lw=1.5, zorder=4)
    ax.axhline(20, color=INK, lw=1, ls=":")
    ax.text(47.8, 21.5, "bar to pass: 20%", fontsize=8, color=INK2, ha="right")
    ax.set_xlabel("layer (of 64)")
    ax.set_ylabel("% of answers from memory\nswitched by the lens push")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_title("Where does the lens push change an answer from memory?\n(circled: cells that pass)", loc="left",
                 fontsize=9.5)  # fmt: skip
    ax = axes[1]
    style(ax, "y")
    prim = rev.get("primary", {})
    if "rates" in prim:
        r = prim["rates"]
        bars = [("patch", "copy from a\ndonor prompt\n(lookup)", INK2), ("lens", "lens push\n(lookup)", RECALL),
                ("random", "random push\n(lookup)", LIGHT), ("rr_lens", "lens push\n(answer from\nmemory)", LOOKUP)]  # fmt: skip
        for i, (key, _, col) in enumerate(bars):
            bar_ci(ax, i, r[key]["rate"], r[key]["lo"], r[key]["hi"], col, width=0.6)
        ax.set_xticks(range(len(bars)), [lab for _, lab, _ in bars], fontsize=8.5)
        cells = ", ".join(f"{d}, layer {la}" for _, d, la in rev["primary_cells"])
        verdict = "the lens moves no lookup" if prim["state"] == "holds" else f"result: {prim['state']}"
        ax.set_title(f"In the cell that passes ({cells}; 6 entities):\n{verdict}", loc="left", fontsize=9.5)
    else:
        ax.text(0.5, 0.5, "no cell passes", transform=ax.transAxes, ha="center", va="center", color=INK2)
        ax.set_title("Cells that pass: none", loc="left", fontsize=9.5)
    ax.set_ylim(0, 100)
    ax.set_ylabel("% switched to the\nother entity's answer")
    head(axes[0], "Is there a place where the lens can write the bridge at the last tokens? One: chemical elements, layers 40-44",
         "Qwen3.6-27B. Lens push: move the last tokens' hidden state along the lens direction from the bridge's word to "
         "another entity's word. A cell (topic, layer) passes if this\nswitches ≥ 20% of answers from memory (lower bound "
         "≥ 10%), a random push of the same size ≤ 5%, and a copy of the hidden state from a donor prompt ≥ 20%. Cells "
         "are chosen on\nanswers from memory alone; only then are the lookups read. Lookups count only when the asked "
         "sentence is the 3rd-5th in the list, where the bridge's identity picks it.", above=24)  # fmt: skip
    save(fig, out, "f22_c2_positive_control.png")


def f23_name_digit_draws(out: Path) -> None:
    """Name vs digit on two draws of pointer_v4's scenes (main, seed2) for Qwen3.6-27B and Qwen3-32B: % right with the
    whole statement, the statement without its digit, or without its name hidden, per destination and family."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts import d2_parts as P

    runs = [("Qwen3.6-27B", "d2_parts_v2_27b", "d2_parts_seed2_27b"),
            ("Qwen3-32B", "qwen3_32b_d2_parts_v2", "qwen3_32b_d2_parts_seed2")]  # fmt: skip
    hidden = [("lookup", "whole statement", INK2), ("lookup_nodigit", "all but the digit (name + rest)", "#9cc1ee"),
              ("lookup_noname", "all but the name (digit + rest)", "#93dcc0")]  # fmt: skip
    fams = [("DL", "named"), ("RL", "recalled")]

    def cells(run: str) -> dict:
        d = RES / "attn_knockout" / run
        cases = {c["id"]: c for c in map(json.loads, (d / "cases.jsonl").read_text().splitlines())}
        return P.cells([json.loads(x) for x in (d / "rows.jsonl").read_text().splitlines()], cases)

    cl = {run: cells(run) for _, a, b in runs for run in (a, b)}
    groups = [(m, fam, flab, a, b) for m, a, b in runs for fam, flab in fams]
    fig, axes = plt.subplots(2, 1, figsize=(12, 6.4), sharey=True, gridspec_kw={"hspace": 0.4})
    w = 0.13
    for ax, dest, title in zip(axes, ("question", "final"), ("hidden from the question's tokens",
                                                             "hidden from the last tokens"), strict=True):  # fmt: skip
        style(ax, "y")
        for i, (_, fam, _, a, b) in enumerate(groups):
            for j, (src, _, col) in enumerate(hidden):
                for k, (run, hatch) in enumerate(((a, None), (b, "///"))):
                    c = cl[run].get((fam, src, dest))
                    if c:
                        x, (p, lo, hi) = i + (2 * j + k - 2.5) * w, c["right"]
                        bar_ci(ax, x, p, lo, hi, col, width=w * 0.95, fs=7, edge=INK2 if hatch else None, hatch=hatch)
        ax.axhline(20, color=INK, lw=1, ls=":")
        ax.set_xticks(range(len(groups)), [f"{m}\n{flab} bridge" for m, _, flab, _, _ in groups])
        ax.set_title(title, loc="left", fontsize=9.5)
        ax.set_ylim(0, 115)
        ax.set_ylabel("% of answers still right")
    head(axes[0], "Name vs digit on a second draw of scenes: every verdict repeats",
         "The same test on new scenes of the same design (same entities and wordings, new lists). Solid: first draw; "
         "hatched: second draw. Dotted: guessing among the list's 5 digits.\nQwen3-32B, recalled bridge, second draw: "
         "2 of 3 topics (animals missed the competence gate by 0.0005; run afterwards alone, it gives the same).",
         above=24)  # fmt: skip
    handles = [box(c) for _, _, c in hidden] + [box(SURF, INK2), box(SURF, INK2, "///")]
    labels = [lab for _, lab, _ in hidden] + ["first draw", "second draw"]
    fig.legend(handles, labels, loc="lower center", ncol=5, frameon=False, bbox_to_anchor=(0.5, -0.05), fontsize=9)
    save(fig, out, "f23_name_digit_draws.png")


def f24_where_bridge_topics(out: Path) -> None:
    """D1 map on four topics (Zach's generator, d1_topics_v1): where a stated bridge sits, by layer, for prompt ->
    prompt, on each model whose map has finished."""
    models = [("Qwen3.6-27B", "d1_topics_map_27b"), ("Qwen3-32B", "qwen3_32b_d1_topics_map")]
    models = [(m, r) for m, r in models if (RES / "statement_positions" / r / "summary.json").exists()]
    sets = [("bind_bridge", "the sentence stating the bridge", "#9b8ce8"), ("context", "the whole context", "#6250d6"),
            ("question", "the question", RECALL), ("final", "the last tokens", INK2)]  # fmt: skip
    fig, axes = plt.subplots(1, len(models), figsize=(5.6 * len(models), 3.3), sharey=True, squeeze=False,
                             gridspec_kw={"wspace": 0.08})  # fmt: skip
    for ax, (model, run) in zip(axes[0], models, strict=True):
        rates = json.loads((RES / "statement_positions" / run / "summary.json").read_text())["rates"]
        style(ax, "y")
        for key, label, col in sets:
            pts = sorted((r["layer"], r["cf"]["flips"]) for r in rates if r["family"] == "PP" and r["set"] == key
                         and r["layer"] >= 16)  # fmt: skip
            ax.plot(
                [p[0] for p in pts], [100 * p[1][0] for p in pts], color=col, lw=2.2, marker="o", ms=3.5, label=label
            )
            ax.fill_between([p[0] for p in pts], [100 * max(p[1][1], 0) for p in pts], [100 * p[1][2] for p in pts],
                            color=col, alpha=0.15, lw=0)  # fmt: skip
        ax.set_title(f"{model} (64 layers)", loc="left", fontsize=9.5)
        ax.set_xlabel("layer")
    axes[0][0].set_ylim(0, 105)
    axes[0][0].set_ylabel("% of lookups that switch")
    h, labs = axes[0][0].get_legend_handles_labels()
    fig.legend(
        h,
        labs,
        loc="lower center",
        ncol=4,
        frameon=False,
        bbox_to_anchor=(0.5, -0.12),
        fontsize=9,
        title="tokens copied from the donor prompt",
        title_fontsize=9,
    )
    head(axes[0][0], "Four topics: a stated bridge sits at its sentence, then over the context; only Qwen3.6-27B hands it to the question",
         "Zach's generator (animals, planets, chemical elements, Greek letters; 120 scenes), prompt → prompt (\"Which "
         "locker belongs to Clara's pick?\"):\ncopy one group of tokens from a donor prompt where Clara picked another "
         "thing, layer by layer, and count lookups that switch to the other thing's locker. The read position itself (the space after\n'Answer:') is never copied: on Qwen3-32B the bridge goes from the context straight there, past the question and the tokens before 'Answer:'.", above=24)  # fmt: skip
    save(fig, out, "f24_where_bridge_topics.png")


def latest_verdict(parts_run: str) -> dict | None:
    """The newest scripts/d1_verdict.py output for a parts run (results/d1_verdict/<run>_<stamp>/verdict.json)."""
    found = sorted((RES / "d1_verdict").glob(f"{parts_run}_*/verdict.json"))
    return json.loads(found[-1].read_text()) if found else None


def f25_stated_bridge_topics(out: Path) -> None:
    """D1 on four topics at the decisive cell (chosen from the lens-free map): the lookup's whole change, its
    lens-readable part and the rest, and the recall's lens-readable part (the positive control), per model; then the
    lens-readable part and the rest per topic and per number style."""
    models = [("Qwen3.6-27B", "d1_topics_parts_27b"), ("Qwen3-32B", "qwen3_32b_d1_topics_parts")]
    vs = [(m, v) for m, run in models if (v := latest_verdict(run))]
    if not vs:
        return
    bars = [("lookup", "full", "lookup: the whole change", INK2, None),
            ("lookup", "jspace", "lookup: only the part the lens can read", RECALL, None),
            ("lookup", "not_jspace", "lookup: everything except that part", LOOKUP, None),
            ("recall", "jspace", "recall: only the part the lens can read\n(the positive control)", "#9cc1ee", "///")]  # fmt: skip
    fig, axes = plt.subplots(1, 3, figsize=(15, 3.6), gridspec_kw={"wspace": 0.22, "width_ratios": [1, 1.6, 0.9]})
    ax = axes[0]
    style(ax, "y")
    w = 0.2
    for i, (_, v) in enumerate(vs):
        for j, (block, p, _, col, hatch) in enumerate(bars):
            r = v[block][p]
            bar_ci(ax, i + (j - 1.5) * w, r[0], r[1], r[2], col, width=w * 0.95, fs=7.5, edge=INK2 if hatch else None,
                   hatch=hatch)  # fmt: skip
    ax.set_xticks(
        range(len(vs)), [f"{m}\n({v['cell']['set']}, layer {v['cell']['layer']})" for m, v in vs], fontsize=8.5
    )
    ax.set_ylim(0, 112)
    ax.set_ylabel("% of answers that switch")
    ax.set_title("All four topics", loc="left", fontsize=9.5)
    for ax, key, title in (
        (axes[1], "by_topic", "By topic"),
        (axes[2], "by_numbers", "By how the scene writes numbers"),
    ):
        style(ax, "y")
        groups = [(m, val, cells) for m, v in vs for val, cells in v[key].items()]
        for i, (_, _, cells) in enumerate(groups):
            for j, (name, col, hatch) in enumerate((("PP_jspace", RECALL, None), ("PP_not_jspace", LOOKUP, None),
                                                    ("PM_jspace", "#9cc1ee", "///"))):  # fmt: skip
                r = cells.get(name)
                if r and r[3]:
                    bar_ci(ax, i + (j - 1) * 0.27, r[0], r[1], r[2], col, width=0.25, fs=6.5,
                           edge=INK2 if hatch else None, hatch=hatch)  # fmt: skip
        ax.set_xticks(range(len(groups)), [f"{val}\n{m.split('-')[-1]}" for m, val, _ in groups],
                      fontsize=7.5)  # fmt: skip
        ax.set_ylim(0, 112)
        ax.set_title(title, loc="left", fontsize=9.5)
        ax.axhline(30, color=INK, lw=1, ls=":")
    head(axes[0], "Four topics, two models: the part of a stated bridge the lens reads, and the lookup",
         "Zach's generator (animals, planets, chemical elements, Greek letters; 120 scenes). Swap the thing Clara picked "
         "and paste one part of the change it causes, at the cell chosen from\nthe map without the lens. Lookup: \"Which "
         "locker belongs to Clara's pick?\"; recall: the pick's number from memory (legs, position from the Sun, atomic number, place in the alphabet). Dotted: the 30% bar the recall control must pass.",
         above=24)  # fmt: skip
    fig.legend([box(c, INK2 if h else None, h) for *_, c, h in bars], [lab for _, _, lab, _, _ in bars],
               loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.14), fontsize=8.5)  # fmt: skip
    save(fig, out, "f25_stated_bridge_topics.png")


def f26_where_lens_writes(out: Path) -> None:
    """D4 v2 (early_push_where d4_where_27b): % switched to the other bridge's answer by layer, per push position, the
    four families under the lens push at the primary cell's scale (8x without one); the random push's highest family
    dotted; the primary cell circled."""
    path = RES / "early_push_where" / "d4_where_27b" / "summary.json"
    if not path.exists():
        return
    sm = json.loads(path.read_text())
    dec = sm["decision"]
    sc = dec["primary"]["scale"] if dec.get("primary") else 8.0
    cells = {(c["family"], c["subset"], c["layer"], c["scale"], c["dir"]): c for c in sm["cells"]}
    fams = [("BR", "prompt → memory (stated bridge, recall)", RECALL, "-"),
            ("BL", "prompt → prompt (stated bridge, lookup)", LOOKUP, "-"),
            ("RR", "memory → memory (recalled bridge, recall)", RECALL, "--"),
            ("RL", "memory → prompt (recalled bridge, lookup)", LOOKUP, "--")]  # fmt: skip
    subs = [("b", "the question's words\n(where slide 6 pushed)"), ("s", "the sentence stating the bridge"),
            ("w", "the bridge's word in that sentence"), ("c", "the whole context")]  # fmt: skip
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.4), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, (sub, title) in zip(axes, subs, strict=True):
        style(ax, "y")
        layers = sorted({k[2] for k in cells if k[1] == sub})
        for fam, _, col, ls in fams:
            pts = [
                (la, cells[(fam, sub, la, sc, "lens")]["to_x"]) for la in layers if (fam, sub, la, sc, "lens") in cells
            ]
            ax.plot([p[0] for p in pts], [100 * p[1][0] for p in pts], color=col, ls=ls, lw=2, marker="o", ms=3)
        rnd = [(la, max(cells[(f, sub, la, sc, "random")]["to_x"][0] for f, *_ in fams if (f, sub, la, sc, "random") in cells))
               for la in layers]  # fmt: skip
        ax.plot([p[0] for p in rnd], [100 * p[1] for p in rnd], color=INK2, ls=":", lw=1.5)
        p = dec.get("primary")
        if p and p["subset"] == sub:
            ax.scatter([p["layer"]], [100 * p["br"]], s=120, facecolors="none", edgecolors=INK, lw=1.5, zorder=5)
        ax.set_title(title, loc="left", fontsize=9.5)
        ax.set_xlabel("layer (of 64)")
        ax.set_ylim(0, 105)
    axes[0].set_ylabel("% switched to the\nother bridge's answer")
    handles = [Line2D([], [], color=c, ls=ls, lw=2) for _, _, c, ls in fams] + [Line2D([], [], color=INK2, ls=":")]
    labels = [lab for _, lab, _, _ in fams] + ["random push of the same size (highest family)"]
    fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.2), fontsize=9)
    head(axes[0], f"Where can a lens push write a bridge? Qwen3.6-27B, animal suite, push {sc:g}x",
         "Push the hidden state along the lens direction from the bridge's word to another animal's, at one group of "
         "tokens and one layer. Circled: the cell chosen on\nprompt → memory rows alone (the rule fixed before the run); "
         f"verdict: {dec['verdict']}.", above=26)  # fmt: skip
    save(fig, out, "f26_where_lens_writes.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="figures/readme_1021")
    out = ROOT / ap.parse_args().out
    out.mkdir(parents=True, exist_ok=True)
    for f in (f0_patch_example, f1_two_routes, f2_stated_bridge, f3_early_push, f4_late_read, f5_slot_by_layer,
              f6_slot_counts, f7_pointer_push, f8_shifts, f9_olmo_slot, f10_late_read_models, f11_natural_errors,
              f12_address_models, f13_mechanism, f14_slot_by_target, f15_counts_models,
              f16_slot_by_target_v5, f17_by_layer_models, f18_stages_models, f19_where_bridge,
              f20_olmo_ladder, f21_name_vs_digit, f22_c2_positive_control, f23_name_digit_draws,
              f24_where_bridge_topics, f25_stated_bridge_topics, f26_where_lens_writes):  # fmt: skip
        f(out)
