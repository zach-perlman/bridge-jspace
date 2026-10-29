"""ledger_figures: the figures of docs/depth/EXPERIMENTS.md's cards (Dan, 29 Oct 01:15) that no README figure covers,
into figures/ledger/ (PNG + SVG), in figures/story's visual system (scripts/story_style.py: colour = reader or part,
mark = operation, grey = random, whiskers = 95% intervals, hollow = after the data; the title is the finding). Every
plotted number is read from its verdict file and recorded with S.record (figure id "ledger_<name>") for
figures/story/data.csv; scripts/readme_story_figures.py's main() calls build_all() before it writes data.csv. Not on
the README's contact sheet.

uv run python -m scripts.readme_story_figures      # rebuilds every figure and data.csv, these included
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from scripts import story_style as S

OUT = S.REPO / "figures" / "ledger"
R = S.REPO / "results"
INK, LOOKUP, JPP, ADDRESS, NULL = (S.MARK_COL[k] for k in ("recall", "lookup", "jpp", "address", "null"))
MODEL3 = (("qwen3.5-9b", "Qwen3.5-9B"), ("qwen3.6-27b", "Qwen3.6-27B"), ("muse-glimmer-30b", "Muse Glimmer 30B"))
# the display names (a lookup only: iterate SLOT_MODELS for the four slots, FIVE where the 122B has a slot)
SHORT = {"qwen3.5-9b": "9B", "qwen3.6-27b": "27B", "muse-glimmer-30b": "Muse", "nemotron-3.5-lightning": "Lightning",
         "qwen3.5-122b-a10b": "122B"}  # fmt: skip

ANSWER = R / "x51_answer" / "x51_12-20261028T201842Z" / "verdict.json"
ANSWER_LIGHTNING = R / "x51_answer" / "x52_answer-20261029T002056Z" / "verdict.json"
ANSWER_122B = R / "x51_answer" / "x52_answer-20261029T112359Z" / "verdict.json"  # the 122B's E1 (coverage, Dan 11:30)
ADDR = R / "x51_addr" / "verdict-20261028T215138Z" / "verdict.json"
DAS = R / "x51_das" / "verdict-20261028T194630Z" / "verdict.json"
HEADS = R / "x51_heads" / "x51_2-20261028T190358Z" / "verdict.json"
HEADS_L = R / "x51_heads" / "x52_heads-20261029T015136Z" / "verdict.json"  # Lightning's coverage run
CARRIER = R / "x51_carrier" / "x51_7-20261028T171646Z" / "verdict.json"
CARRIER_L = R / "x51_carrier" / "x52_carrier-20261029T014338Z" / "verdict.json"  # Lightning's coverage run
TRAVEL = R / "x51_travel" / "x51_4-20261028T173333Z" / "verdict.json"
TRAVEL_L = R / "x51_travel" / "x52_travel-20261029T012517Z" / "verdict.json"  # Lightning's coverage run
Z1 = R / "x50_zach" / "z1-20261028T161649Z" / "z1.json"
Z3 = R / "x50_zach" / "z3-20261028T163053Z" / "z3.json"
Z3_27B = R / "x50_zach" / "x52_z3-20261029T024151Z" / "z3.json"  # the 27B's coverage run (L32)
Z3_L = R / "x50_zach" / "x52_z3-20261029T013329Z" / "z3.json"  # Lightning's coverage run (L14, L27)
CLEAN = R / "checks" / "clean49_9b.json"
LAYER = R / "x51_lightning" / "nem35l_x52_layer_r2" / "layer.json"
CONFLICT = R / "x0_necessity" / "nem35l_x52_conflict" / "verdict-20261029T001612Z" / "verdict.json"
CONFLICT_122B = R / "x0_necessity" / "qwen35_122b_x0_necessity_r2" / "verdict-20261024T171509Z" / "verdict.json"
MAIN = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse"}  # docs/x0_numbers.json's suffixes


def rel(p: Path) -> str:
    return str(p.relative_to(S.REPO))


def load(p: Path) -> dict:
    return json.loads(p.read_text())


# Dan's figures brief (29 Oct 10:00): four model slots on every per-model figure, in the tables' order; a model without
# a result keeps its slot with a short grey label; below-gate results hollow, labelled "below gate". Each figure's slots
# go to figures/ledger/slots.json ("data" where the figure records a number for the model, else what grey() or
# below_gate() registered); scripts/check_ledger.py checks them against the card's table.
SLOT_MODELS = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning")
LT = "nemotron-3.5-lightning"
# Dan 11:30 (q122b_1130): the 122B (FP8; MoE, ~10B active) as a fifth slot, only in the figures of cards where it has a
# verdict; the other figures keep four slots (a not-run 122B needs none)
B122 = "qwen3.5-122b-a10b"
FIVE = (*SLOT_MODELS, B122)
SLOTS_FILE = OUT / "slots.json"
_SLOTS: dict[str, dict[str, str]] = {}
GREY = "#9a9a9a"


def grey(name: str, model: str, label: str, ax=None, x: float = 0.0, y: float = 0.0, **kw) -> None:
    """A model's empty slot: registered as grey with its label, and drawn at (x, y) on ax when given."""
    _SLOTS.setdefault(name, {})[SHORT[model]] = "grey: " + " ".join(label.split())
    if ax is not None:
        ax.text(x, y, label, color=GREY, va="center", fontsize=kw.pop("fontsize", S.LABEL_PT - 1), **kw)


def below_gate(name: str, model: str) -> None:
    """A model plotted below its gate (hollow ○, labelled "below gate")."""
    _SLOTS.setdefault(name, {})[SHORT[model]] = "below gate"


def title_size(ax) -> float:
    """A panel title's font size by the panel's width (five panels beside long row labels need a smaller one)."""
    width = ax.get_position().width
    return 12 if width >= 0.16 else 10.5 if width >= 0.125 else 9.5


def grey_panel(name: str, model: str, label: str, ax) -> None:
    """A whole panel for a model without a result: its name as the title, the grey label in the middle, no axes."""
    ax.set_title(SHORT[model], fontsize=title_size(ax), weight="bold", loc="left", color=GREY)
    # tick_params, not set_ticks: the panel may share an axis with the data panels
    ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    ax.set_xlabel("")
    ax.grid(False)
    for side in ax.spines.values():
        side.set_visible(False)
    grey(name, model, label, ax, 0.5, 0.5, ha="center", transform=ax.transAxes, wrap=True)


def note_slot(fig, name: str, model: str = "qwen3.5-122b-a10b", label: str = "not run") -> None:
    """A model's grey slot on a one-axis figure (rows or stacks, no panel per model): registered as grey and named in a
    grey line at the figure's bottom left (Dan 12:50: a grey labelled slot where a model did not run)."""
    grey(name, model, label)
    fig.text(0.005, 0.006, f"{SHORT[model]}: {label}", ha="left", va="bottom", color=GREY, fontsize=S.LABEL_PT - 1)


def slots_of(name: str) -> dict[str, str]:
    """The figure's four slots: what grey() / below_gate() registered, else "data" where the figure recorded a number
    for the model (S.record), else missing."""
    have = {r["model"] for r in S.ROWS if r["figure"] == name}
    reg = _SLOTS.get(name, {})
    out = {}
    for t in FIVE:
        if SHORT[t] in reg:
            out[SHORT[t]] = reg[SHORT[t]]
        elif t in have:
            out[SHORT[t]] = "data"
    return out


def save(fig, name: str) -> str:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", facecolor="white")
    fig.savefig(OUT / f"{name}.png", dpi=200, facecolor="white")
    S.plt.close(fig)
    every = json.loads(SLOTS_FILE.read_text()) if SLOTS_FILE.exists() else {}
    every[name] = slots_of(name)
    SLOTS_FILE.write_text(json.dumps(dict(sorted(every.items())), indent=1, ensure_ascii=False) + "\n")
    return name


def whisker(ax, y: float, v, col: str, hollow: bool = False, size: float = 7.0, marker: str = "o") -> None:
    ax.plot([v[1], v[2]], [y, y], color=col, lw=1.6, zorder=2, solid_capstyle="butt")
    ax.plot([v[0]], [y], marker, ms=size, mfc="white" if hollow else col, mec=col, mew=1.5, zorder=3)


def rows_axis(ax, labels: list[str]) -> None:
    ax.set_ylim(-len(labels) + 0.4, 0.6)
    ax.set_yticks([-i for i in range(len(labels))], labels)
    ax.tick_params(axis="y", length=0)


def zero_band(ax, lo: float = -0.2, hi: float = 1.05) -> None:
    ax.set_xlim(lo, hi)
    ax.axvline(0, color="#999999", lw=0.8, zorder=1)
    ax.grid(axis="x", color="#eeeeee")


# ---- the answer control (51.12, and Lightning's coverage run) -------------------------------------------------------


def answer_control(plt) -> str:
    """The recall's three arms per model (without the lens part; the same with the answer words' directions kept; the
    answer directions only), each beyond a random part; Zach's described bridge (Z2) beside in grey, withdrawn."""
    arms = (("1", "without the lens part"), ("2", "lens part out, answer kept"), ("3", "answer directions only"))
    sources = [(ANSWER, m) for m in load(ANSWER)["models"] if m["set"] == "e1"]
    sources += [(ANSWER_LIGHTNING, m) for m in load(ANSWER_LIGHTNING)["models"] if m["set"] == "e1"]
    sources += [(ANSWER_122B, m) for m in load(ANSWER_122B)["models"] if m["set"] == "e1" and m["target"] == B122]
    order = FIVE
    sources.sort(key=lambda s: order.index(s[1]["target"]))
    blocks = []
    for path, m in sources:
        rc = m["readers"]["recall"]
        blocks.append((SHORT[m["target"]], [(lab, rc["extra"][k]) for k, lab in arms], INK, False))
        for k, lab in arms:
            S.record("ledger_answer_control", m["target"], f"main test, recall, switches lost beyond random: {lab}",
                     *rc["extra"][k], n=rc["n"], source=rel(path))  # fmt: skip
    for m in load(ANSWER)["models"]:
        if m["set"] == "z2":
            rc = m["readers"]["recall"]
            blocks.append((f"{SHORT[m['target']]}, Zach's described bridge (withdrawn)",
                           [(lab, rc["extra"][k]) for k, lab in arms], NULL, True))  # fmt: skip
            for k, lab in arms:
                S.record("ledger_answer_control", m["target"], f"Zach's described bridge, recall: {lab}",
                         *rc["extra"][k], n=rc["n"], source=rel(ANSWER))  # fmt: skip
    n_rows = sum(len(b[1]) + 1 for b in blocks)
    fig, ax = plt.subplots(figsize=(S.WIDTH, 0.27 * n_rows + 1.6))
    fig.subplots_adjust(left=0.36, right=0.97, top=1 - 1.05 / fig.get_figheight(), bottom=0.6 / fig.get_figheight())
    S.title(fig, "The recall's loss without the lens part is the item, not its answer",
            "Recall: switches lost beyond a random part (same size), main test at L; whiskers 95%")  # fmt: skip
    y, ticks, labels = 0.0, [], []
    for name, arms_v, col, z2 in blocks:
        ax.text(-0.19, y, name, fontsize=S.FONT, weight="bold", color=S.COL["muted"] if z2 else "#222222", va="center")
        y -= 1
        for lab, v in arms_v:
            whisker(ax, y, v, col)
            ticks.append(y)
            labels.append(lab)
            y -= 1
    ax.set_yticks(ticks, labels)
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(y + 0.4, 0.6)
    zero_band(ax, -0.2, 1.0)
    ax.set_xlabel("switches lost beyond a random part")
    return save(fig, "ledger_answer_control")


# ---- the address: size and shape (51.11) ----------------------------------------------------------------------------


def address_shape(plt) -> str:
    """Top: part 1's own interchange accuracy of the learned code against its dimension k, one line per number of
    lockers, the random code dashed (9B, Muse). Bottom: part 3's midpoint swaps from slot 1 and slot 6: the share sent
    to the midpoint slot, beside the full swap's share sent to its target."""
    v = load(ADDR)
    by = {m["target"]: m for m in v["models"] if m.get("part1") and m["part1"].get("S")}
    fig, axes = plt.subplots(2, 4, figsize=(S.WIDTH, 6.6))
    fig.subplots_adjust(left=0.09, right=0.97, top=0.84, bottom=0.08, hspace=0.55, wspace=0.35)
    S.title(fig, "Muse's code grows with the lockers, the 9B's does not; midpoints fail",
            "Top: learned code's accuracy by size k, per number of lockers; bottom: swaps to the midpoint slot")  # fmt: skip
    shades = {"3": "#f5c48a", "4": "#eaa04f", "6": "#c9731a", "8": "#8a4a0b"}
    absent = {"qwen3.6-27b": "part 2 only\n(parts 1, 3 not\ndesigned); its\nswap in the table",
              LT: "not tested:\nDAS port\ndropped"}  # fmt: skip
    for j, t in enumerate(SLOT_MODELS):
        if t not in by:
            grey_panel("ledger_address_shape", t, absent[t], axes[0, j])
            axes[1, j].axis("off")
            continue
        m = by[t]
        ax = axes[0, j]
        ax.set_title(SHORT[t], fontsize=12, weight="bold", loc="left")
        items = []
        for s, cell in m["part1"]["S"].items():
            c = cell.get("curve")
            if not c:
                continue
            ks = c["ks"]
            vals = [c["R"][str(k)] for k in ks]
            ax.plot(ks, [x[0] for x in vals], "-o", color=shades.get(s, ADDRESS), ms=4, lw=1.6)
            ax.plot(ks, [c["rand"][str(k)][0] for k in ks], "--", color=NULL, lw=1.2)
            items.append((vals[-1][0], f"{s} lockers", shades.get(s, ADDRESS)))
            for k, x in zip(ks, vals, strict=True):
                S.record("ledger_address_shape", m["target"], f"part 1, {s} lockers: learned code's own-IIA at k = {k}",
                         *x, n=c["n"], source=rel(ADDR))  # fmt: skip
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlim(0.5, 9.5)
        ax.set_xticks([1, 2, 3, 4, 5, 7])
        ax.set_xlabel("code size k (directions)")
        if j == 0:
            ax.set_ylabel("position switches carried")
        S.end_labels(ax, 7, items, pad=0.3)
        ax.text(7.3, 0.03, "random code", color=S.COL["muted"], fontsize=S.LABEL_PT, va="bottom")
        ax = axes[1, j]
        cells = m["part3"]["cells"]
        bars = [("from slot 1", cells["1|mid|2"]["midpoint"], cells["1|full|2"]["far"]),
                ("from slot 6", cells["6|mid|2"]["midpoint"], cells["6|full|2"]["far"])]  # fmt: skip
        for i, (lab, mid, full) in enumerate(bars):
            for dx, val, col, what in ((-0.18, mid, ADDRESS, "midpoint swap: lands on the midpoint slot"),
                                       (0.18, full, "#f3d3a8", "full swap: lands on its target")):  # fmt: skip
                ax.bar(i + dx, val[0], width=0.34, color=col, edgecolor=ADDRESS, lw=0.8)
                ax.plot([i + dx, i + dx], [val[1], val[2]], color="#333333", lw=1.2)
                S.record("ledger_address_shape", m["target"], f"part 3, dose 2, {lab}: {what}", *val,
                         n=cells["1|mid|2"]["n"], source=rel(ADDR))  # fmt: skip
        ax.set_xticks([0, 1], ["slot 1", "slot 6"])
        ax.set_xlabel("swapped from")
        ax.set_ylim(0, 1.0)
        if j == 0:
            ax.set_ylabel("share of lookups")
            ax.text(-0.36, 0.86, "dark: the midpoint swap, on the midpoint\nlight: the full swap, on its target",
                    fontsize=S.LABEL_PT, color=S.COL["muted"])  # fmt: skip
    note_slot(fig, "ledger_address_shape")
    return save(fig, "ledger_address_shape")


# ---- learned subspaces (51.3) ---------------------------------------------------------------------------------------


def learned(plt) -> str:
    """Per model, the learned subspace's own interchange accuracy on test pairs against its size k, for the recall and
    the lookup; a random subspace of the same size dashed."""
    v = load(DAS)
    by = {m["target"]: m for m in v["models"]}
    fig, axes = plt.subplots(1, 5, figsize=(S.WIDTH, 3.6), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.93, top=0.72, bottom=0.17, wspace=0.3)
    S.title(fig, "Learned subspaces carry each reader's item switch; random ones none",
            "Switches carried by a learned subspace of size k on held-out entities; dashed: random subspace")  # fmt: skip
    grey_panel("ledger_learned", LT, "dropped:\nDAS port", axes[3])
    for ax, (t, name) in zip(axes, MODEL3, strict=False):
        ax.set_title(SHORT[t], fontsize=12, weight="bold", loc="left")
        readers = by[t]["identity"]["readers"]
        items = []
        for key, col, word in (("PM", INK, "recall"), ("PP", LOOKUP, "lookup")):
            test = readers[key]["test"]
            ks = sorted(int(k) for k in test["own_iia"])
            vals = [test["own_iia"][str(k)] for k in ks]
            ax.plot(ks, [x[0] for x in vals], "-o", color=col, ms=4.5, lw=1.6)
            for k, x in zip(ks, vals, strict=True):
                ax.plot([k, k], [x[1], x[2]], color=col, lw=1.0)
                S.record("ledger_learned", t, f"{word}: test own-IIA at k = {k}", *x, n=test["n"], source=rel(DAS))
            ax.plot(ks, [test["random_iia"][str(k)][0] for k in ks], "--", color=NULL, lw=1.2)
            items.append((vals[-1][0], word, col))
        ax.set_xscale("log", base=2)
        ax.set_xticks([4, 16, 128], ["4", "16", "128"])
        ax.set_xlim(3, 220)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("subspace size k")
        S.end_labels(ax, 128, items, pad=8)
    axes[0].set_ylabel("switches carried")
    grey_panel("ledger_learned", B122, "not run", axes[4])
    return save(fig, "ledger_learned")


# ---- joint head ablation (51.2) -------------------------------------------------------------------------------------


def heads(plt) -> str:
    """Per model (9B, 27B, Muse, Lightning), the share of the address swap's switch cut by mean-ablating the top 1, 3,
    5, 10 heads and every head of the best layer at the last token; the mean of five random head sets of the same size
    beside (grey)."""
    by = {r["target"]: (r, path) for path in (HEADS, HEADS_L) for r in load(path)["results"]}
    sets = ("top1", "top3", "top5", "top10", "best_layer")
    names = ("top 1", "top 3", "top 5", "top 10", "best layer")
    fig, axes = plt.subplots(1, 5, figsize=(S.WIDTH, 3.5), sharey=True)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.72, bottom=0.2, wspace=0.12)
    S.title(fig, "No small set of heads carries the swapped address",
            "Share of the swap's switch cut by ablating heads at the last token; grey: random heads, same size")  # fmt: skip
    for ax, t in zip(axes[:4], SLOT_MODELS, strict=True):
        ax.set_title(SHORT[t], fontsize=12, weight="bold", loc="left")
        r, src = by[t]
        site = r["sites"]["last"]
        for i, s in enumerate(sets):
            c = site["cells"][s]["cut"]
            ax.plot([i, i], [c[1], c[2]], color=ADDRESS, lw=1.6)
            ax.plot([i], [c[0]], "o", color=ADDRESS, ms=6.5)
            rnd = site["random"][s]["cut_mean"]
            ax.plot([i + 0.25], [rnd], "o", color=NULL, ms=5)
            S.record("ledger_heads", t, f"last token, {names[i]}: share of the swap's switch cut", *c,
                     n=site["cells"][s]["n"], source=rel(src))  # fmt: skip
            S.record("ledger_heads", t, f"last token, {names[i]}: random sets' mean cut", round(rnd, 4),
                     source=rel(src))  # fmt: skip
        ax.axhline(0, color="#999999", lw=0.8)
        ax.axhline(0.5, color="#555555", lw=0.9, ls=":")
        ax.set_xticks(range(len(sets)), names, rotation=35, ha="right")
        ax.set_ylim(-0.45, 0.6)
    axes[0].set_ylabel("share of the switch cut")
    axes[0].text(4.4, 0.52, "rule's bar 0.5", fontsize=S.LABEL_PT, color=S.COL["muted"], ha="right")
    grey_panel("ledger_heads", B122, "not run", axes[4])
    return save(fig, "ledger_heads")


# ---- the full carrier (51.7) ----------------------------------------------------------------------------------------


def full_carrier(plt) -> str:
    """Per model (9B, 27B, Lightning), lookups and recalls lost without the lens part beyond a random part, fact first
    and fact after, the change at one layer (hollow) and at every layer up to L (filled)."""
    runs = [(m, CARRIER) for m in load(CARRIER)["models"]] + [(m, CARRIER_L) for m in load(CARRIER_L)["models"]]
    by = {m["target"]: (m, src) for m, src in runs}
    fig, axes = plt.subplots(1, 5, figsize=(S.WIDTH, 3.9), sharey=True)
    fig.subplots_adjust(left=0.18, right=0.98, top=0.72, bottom=0.15, wspace=0.1)
    S.title(fig, "Over every layer up to L, fact-after lookups follow the lens part",
            "Switches lost without the lens part, beyond a random part; hollow: one layer, filled: every layer to L")  # fmt: skip
    labels = ["fact first", "fact after"]
    for ax, t in zip(axes[:4], SLOT_MODELS, strict=True):
        if t not in by:
            rows_axis(ax, labels)
            ax.set_ylim(-1.6, 0.5)
            grey_panel("ledger_full_carrier", t, "not designed\n(9B / 27B only)", ax)
            continue
        m, src = by[t]
        ax.set_title(SHORT[t], fontsize=12, weight="bold", loc="left")
        for i, g in enumerate(("fact-first", "fact-after")):
            grp = m["groups"][g]
            for carrier, dy, hollow in (("one", 0.18, True), ("before", 0.0, False)):
                for reader, col, ddy in (("lookup", LOOKUP, 0.0), ("recall", INK, -0.32)):
                    e = grp[carrier][reader]["excess"]
                    if grp[carrier][reader]["valid"]:
                        whisker(ax, -i + dy + ddy, e, col, hollow=hollow)
                    else:  # under 30 switches under the whole change: left out (the README figures' convention)
                        ax.text(0.12, -i + dy + ddy, "under 30 switches", color=col, va="center",
                                fontsize=S.LABEL_PT - 1)  # fmt: skip
                    S.record("ledger_full_carrier", m["target"], f"{g}, {reader}, "
                             f"{'one layer' if carrier == 'one' else 'every layer to L'}: switches lost beyond random",
                             *e, n=grp[carrier][reader]["n"], source=rel(src))  # fmt: skip
        rows_axis(ax, labels)
        ax.set_ylim(-1.6, 0.5)
        zero_band(ax, -0.2, 1.0)
        ax.set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        ax.axvspan(-0.2, 0.10, color=S.COL["band"], lw=0, zorder=0)
    fig.text(0.58, 0.03, "switches lost beyond random", ha="center", fontsize=S.FONT)
    axes[1].text(0.55, 0.32, "lookup", color=LOOKUP, fontsize=S.LABEL_PT)
    axes[1].text(0.55, -0.18, "recall", color=INK, fontsize=S.LABEL_PT)
    grey_panel("ledger_full_carrier", B122, "not run", axes[4])
    return save(fig, "ledger_full_carrier")


# ---- the address at the last token (51.4) ---------------------------------------------------------------------------


def last_token_address(plt) -> str:
    """Per model (9B, 27B, Muse, Lightning), the slot probe's held-out accuracy at the last token by layer (the majority
    baseline dashed), L and L + 4 marked, and the bridge-fit swap's share sent to the target at L + 4 (dose 2) as
    text."""
    by = {m["target"]: (m, TRAVEL) for m in load(TRAVEL)["models"]}
    by.update({m["target"]: (m, TRAVEL_L) for m in load(TRAVEL_L)["models"]})
    models = [*MODEL3, ("nemotron-3.5-lightning", "Lightning")]
    fig, axes = plt.subplots(1, 5, figsize=(S.WIDTH, 3.6), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.72, bottom=0.17, wspace=0.12)
    S.title(fig, "The bridge word's code works at the last token only on Muse",
            "Slot probe's accuracy at the last token by layer; dashed: majority slot; text: the swap at L+4")  # fmt: skip
    for ax, (t, _name) in zip(axes[:4], models, strict=True):
        m, src = by[t]
        ax.set_title(SHORT[t], fontsize=12, weight="bold", loc="left")
        layers = sorted(int(k) for k in m["probe"])
        acc = [m["probe"][str(la)]["acc"] for la in layers]
        ax.fill_between(layers, [a[1] for a in acc], [a[2] for a in acc], color=ADDRESS, alpha=0.18, lw=0)
        ax.plot(layers, [a[0] for a in acc], "-", color=ADDRESS, lw=1.8)
        ax.plot(layers, [m["probe"][str(la)]["majority"][0] for la in layers], "--", color=NULL, lw=1.2)
        for la in m["layers"]:
            ax.axvline(la, color="#555555", lw=0.8, ls=":")
        swap = next(r for r in m["table"] if r["arm"] == "bridge_swap" and r["tag"] == "L+4" and r["s"] == 2.0
                    and r["scope"] == "all")  # fmt: skip
        ax.text(0.97, 0.06, f"swap at L+4: {swap['target'][0]:.2f}", transform=ax.transAxes, ha="right",
                fontsize=S.LABEL_PT, color="#222222")  # fmt: skip
        S.record("ledger_last_token_address", t, "bridge-fit swap at L+4, dose 2: lookups sent to the target",
                 *swap["target"], n=swap["n"], source=rel(src))  # fmt: skip
        for la, a in zip(layers, acc, strict=True):
            S.record("ledger_last_token_address", t, f"slot probe at the last token, layer {la}", *a,
                     n=m["probe"][str(la)]["n"], source=rel(src))  # fmt: skip
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("layer")
    axes[0].set_ylabel("probe accuracy")
    grey_panel("ledger_last_token_address", B122, "not run", axes[4])
    return save(fig, "ledger_last_token_address")


# ---- Zach's named passages (Z1) beside our main test ----------------------------------------------------------------


Z1_L = R / "x50_zach" / "x52_z1-20261029T013035Z" / "z1.json"  # Lightning's coverage run (L14 decides)
# Z1-P: Zach's named passages with made-up facts (Dan's morning brief, 29 Oct); Lightning's missed its gate
Z1P = {"qwen3.5-9b": R / "x50_zach" / "x52_z1p-20261029T081112Z" / "z1p.json",
       "qwen3.6-27b": R / "x50_zach" / "x52_z1p-20261029T081323Z" / "z1p.json",
       "nemotron-3.5-lightning": R / "x50_zach" / "x52_z1p-20261029T080731Z" / "z1p.json",
       "muse-glimmer-30b": R / "x50_zach" / "x52_z1p-20261029T094820Z" / "z1p.json"}  # fmt: skip


def _zach_cell(path: Path, target: str, reader: str) -> dict:
    (m,) = [m for m in load(path)["models"] if m["target"] == target]
    return m["layer_results"][str(m["layers"][0])][reader]


def _below_gate(path: Path, target: str) -> bool:
    (m,) = [m for m in load(path)["models"] if m["target"] == target]
    return str(m.get("status", "")).startswith("not tested")


def zach_named(plt) -> str:
    """Per model (9B, 27B, Muse, Lightning), each reader's switches lost without the lens part beyond a random part:
    our main test (X0's numbers; Lightning's conflict test at L14), Zach's named passages with true facts (Z1, at L)
    and with made-up facts (Z1-P; Muse not run). Lightning hollow (its gate set after the 60-scene pre-check; its
    made-up-fact run also below that run's gate, numbers descriptive only)."""
    numbers = S.numbers()
    lt = "nemotron-3.5-lightning"
    conflict = {c["reader"]: c for c in load(CONFLICT)["cells"]
                if c["dict"] == "jpp" and c["k"] == 25 and c["rendering"] == "chat" and c["layer"] == 14}  # fmt: skip
    models = [t for t, _ in MODEL3] + [lt]
    sets = (("our main test", "ours"), ("his, true facts", "true"), ("his, made-up facts", "made"))
    n_rows = len(models) * len(sets)
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 0.27 * n_rows + 1.9), sharey=True)
    h = fig.get_figheight()
    fig.subplots_adjust(left=0.325, right=0.98, top=1 - 1.2 / h, bottom=0.55 / h, wspace=0.08)
    S.title(fig, "Zach's lookups follow the lens part with true facts, less with made-up",
            "Lost beyond random, at L; grey: the lookup's 0.10 bar; whiskers 95%; ○ hollow: Lightning, below gate")  # fmt: skip
    labels = []
    for t in models:
        tag = SHORT[t] + (" ○" if t == lt else "")
        below = t in Z1P and _below_gate(Z1P[t], t)
        labels += [f"{tag}, {lab}" if not (below and k == "made") else f"{tag}, made-up, below gate" for lab, k in sets]
    for ax, (reader, col, key, pp) in zip(axes, (("lookup", LOOKUP, "lk", "PP"), ("recall", INK, "rc", "PM")),
                                          strict=True):  # fmt: skip
        ax.set_title(reader, fontsize=12, weight="bold", loc="left", color=col)
        for i, t in enumerate(models):
            hollow = t == lt
            y0 = -i * len(sets)
            ours = conflict[pp]["excess"] if t == lt else S.parse(numbers[f"{key}_excess_{MAIN[t]}"])
            whisker(ax, y0, ours, col, hollow=hollow)
            if t == lt:
                S.record("ledger_zach_named", t, f"our main test (L14), {reader}: switches lost beyond random", *ours,
                         source=rel(CONFLICT))  # fmt: skip
            for j, (_, k) in enumerate(sets[1:], start=1):
                path = (Z1_L if t == lt else Z1) if k == "true" else Z1P.get(t)
                if path is None:
                    ax.text(-0.2, y0 - j, "not run", color=S.COL["muted"], va="center", fontsize=S.LABEL_PT - 1)
                    continue
                cell = _zach_cell(path, t, reader)
                below = k == "made" and _below_gate(path, t)
                if cell["valid"]:
                    whisker(ax, y0 - j, cell["excess"], col, hollow=hollow or below)
                else:  # under 30 switches under the whole change: left out (the README figures' convention)
                    ax.text(-0.2, y0 - j, "under 30 switches", color=col, va="center", fontsize=S.LABEL_PT - 1)
                what = "true facts" if k == "true" else "made-up facts"
                S.record("ledger_zach_named", t, f"Zach's named passages, {what}, {reader}: switches lost beyond "
                         "random", *cell["excess"], source=rel(path))  # fmt: skip
            if i:
                ax.axhline(y0 + 0.5, color="#dddddd", lw=0.8)
        rows_axis(ax, labels)
        zero_band(ax, -0.25, 1.0)
        ax.axvspan(-0.25, 0.10, color=S.COL["band"], lw=0, zorder=0)
        ax.set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        ax.set_xlabel("switches lost beyond random")
    note_slot(fig, "ledger_zach_named")
    return save(fig, "ledger_zach_named")


# ---- routes on Zach's passages (Z3) ---------------------------------------------------------------------------------


def zach_routes(plt) -> str:
    """The lookup's answer under the whole change on Zach's scattered-fact passages: identity, position, value, the
    original answer, stacked, per model and layer (9B and Muse from the first run, the 27B and Lightning from their
    coverage runs)."""
    by = {m["target"]: (m, path) for path in (Z3, Z3_27B, Z3_L) for m in load(path)["models"] if m["layer_results"]}
    rows = []
    for t in (t for t in SLOT_MODELS if t in by):
        m, path = by[t]
        for la, lr in m["layer_results"].items():
            rows.append((f"{SHORT[t]} L{la}", lr["shares"]["C2"]["whole"], lr["n"], t, la, path))
    fig, ax = plt.subplots(figsize=(S.WIDTH, 0.55 * len(rows) + 1.7))
    fig.subplots_adjust(left=0.16, right=0.88, top=1 - 1.15 / fig.get_figheight(), bottom=0.65 / fig.get_figheight())
    S.title(fig, "On Zach's passages the lookup rarely takes the position route",
            "The lookup's answer under the whole change, share of passages")  # fmt: skip
    parts = (("identity", S.COL["identity"]), ("position", S.COL["position"]), ("value", S.COL["value"]),
             ("original", S.COL["original"]))  # fmt: skip
    for i, (_, sh, n, t, la, path) in enumerate(rows):
        left = 0.0
        for p, col in parts:
            w = sh[p][0]
            ax.barh(-i, w, left=left, color=col, height=0.6, edgecolor="white", lw=0.5)
            if w >= 0.08:
                ax.text(left + w / 2, -i, f"{p}\n{w:.2f}", ha="center", va="center", fontsize=S.LABEL_PT - 1,
                        color="white" if p in ("identity", "value") else "#222222")  # fmt: skip
            left += w
            S.record("ledger_zach_routes", t, f"L{la}, whole change: {p} share", *sh[p], n=n, source=rel(path))
        ax.text(1.01, -i, f"n = {n}", va="center", fontsize=S.LABEL_PT, color=S.COL["muted"])
    rows_axis(ax, [r[0] for r in rows])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("share of the lookup's answers")
    note_slot(fig, "ledger_zach_routes")
    return save(fig, "ledger_zach_routes")


# ---- clean reruns (49.5) --------------------------------------------------------------------------------------------


def clean_reruns(plt) -> str:
    """The 9B's headline cells from the run of record against the clean-checkout rerun, the identity line."""
    v = load(CLEAN)
    fig, ax = plt.subplots(figsize=(S.WIDTH, 4.9))
    fig.subplots_adjust(left=0.1, right=0.6, top=0.8, bottom=0.12)
    S.title(fig, "The 9B's headline cells reproduce from a clean checkout",
            "Each dot a headline cell; x: run of record, y: clean rerun")  # fmt: skip
    ax.plot([0, 1], [0, 1], color=NULL, lw=1.0, ls="--")
    for c in v["cells"]:
        col = INK if c["same"] else ADDRESS
        ax.plot([c["record"]], [c["clean"]], "o", color=col, ms=6, mfc=col if c["same"] else "white", mew=1.5)
        S.record("ledger_clean_reruns", "qwen3.5-9b", f"{c['cell']}: record / clean", round(c["record"], 4),
                 n=c["n_record"], source=rel(CLEAN))  # fmt: skip
        S.record("ledger_clean_reruns", "qwen3.5-9b", f"{c['cell']}: clean rerun", round(c["clean"], 4),
                 n=c["n_clean"], source=rel(CLEAN))  # fmt: skip
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("run of record")
    ax.set_ylabel("clean rerun")
    for t in SLOT_MODELS[1:]:
        grey("ledger_clean_reruns", t, "9B only by design (the caption)")
    ax.text(1.05, 0.5, "filled: the same\non every row\n\nhollow: the depth\nanatomy's cells,\n38 of 11,988 rows\ndiffer",
            transform=ax.transAxes, ha="left", va="center",
            fontsize=S.LABEL_PT, color=S.COL["muted"])  # fmt: skip
    note_slot(fig, "ledger_clean_reruns")
    return save(fig, "ledger_clean_reruns")


# ---- Lightning: the layer sweep and the conflict test at every layer ------------------------------------------------


def lightning_layers(plt) -> str:
    """Top: the whole change's switch rate per swept layer for both readers (60 dev scenes), the relative depth 0.25
    line, L14 marked. Bottom: the conflict test at every swept layer (200 scenes): each reader's switches lost without
    the lens part beyond a random part; cells under 30 switches greyed. Third panel: the 122B's conflict test at its
    swept layers (L24-L36; its L33), the fifth model (Dan 11:30)."""
    lay, ver = load(LAYER), load(CONFLICT)
    layers = sorted(int(k) for k in lay["rates"])
    fig, axes = plt.subplots(3, 1, figsize=(S.WIDTH, 8.2), gridspec_kw={"height_ratios": (1, 1, 0.85)})
    axes[0].sharex(axes[1])
    axes[0].tick_params(labelbottom=False)
    fig.subplots_adjust(left=0.1, right=0.86, top=0.89, bottom=0.1, hspace=0.42)
    S.title(fig, "On Lightning the recall follows the lens part; the lookup does not",
            "Top: switches per layer; middle: lost beyond a random part; bottom: the same on the 122B")  # fmt: skip
    ax = axes[0]
    for reader, col in (("lookup", LOOKUP), ("recall", INK)):
        ax.plot(layers, [lay["rates"][str(la)][reader] for la in layers], "-o", color=col, ms=4, lw=1.6)
        for la in layers:
            S.record("ledger_lightning_layers", "nemotron-3.5-lightning", f"layer sweep, L{la}: {reader} switch rate",
                     round(lay["rates"][str(la)][reader], 4), n=60, source=rel(LAYER))  # fmt: skip
    depth = 0.25 * lay["n_layers"]
    ax.axvline(depth, color="#555555", lw=0.9, ls=":")
    ax.text(depth - 0.5, 0.05, "depth 0.25", fontsize=S.LABEL_PT, color=S.COL["muted"], ha="right")
    ax.axhline(0.3, color="#555555", lw=0.8, ls="--")
    ax.set_ylim(-0.03, 1.05)
    ax.set_ylabel("switched")
    S.end_labels(ax, layers[-1], [(lay["rates"][str(layers[-1])]["lookup"], "lookup", LOOKUP),
                                  (lay["rates"][str(layers[-1])]["recall"] + 0.1, "recall", INK)], pad=1.0)  # fmt: skip
    ax = axes[1]
    cells = [c for c in ver["cells"] if c["dict"] == "jpp" and c["k"] == 25 and c["rendering"] == "chat"]
    for reader, col, dx in (("PP", LOOKUP, -0.5), ("PM", INK, 0.5)):
        for c in sorted((c for c in cells if c["reader"] == reader), key=lambda c: c["layer"]):
            ok = c["switched_whole"] >= 30 and c["excess"][0] == c["excess"][0]  # NaN when nothing switched
            if ok:
                ax.plot([c["layer"] + dx] * 2, [c["excess"][1], c["excess"][2]], color=col, lw=1.6)
                ax.plot([c["layer"] + dx], [c["excess"][0]], "o", color=col, ms=5.5)
            else:
                ax.axvspan(c["layer"] + dx - 0.9, c["layer"] + dx + 0.9, color="#e6e6e6", lw=0, zorder=0)
            S.record("ledger_lightning_layers", "nemotron-3.5-lightning", f"conflict test, L{c['layer']}, "
                     f"{'lookup' if reader == 'PP' else 'recall'}: switches lost beyond random",
                     *c["excess"], n=c["n"], source=rel(CONFLICT))  # fmt: skip
    ax.axhline(0, color="#999999", lw=0.8)
    ax.axhline(0.10, color=LOOKUP, lw=0.8, ls="--")
    ax.set_ylim(-0.2, 0.8)
    ax.set_ylabel("lost beyond random")
    ax.set_xlabel("layer (grey: under 30 switches, cannot tell)")
    for a in axes:
        a.axvline(lay["layer"], color="#222222", lw=1.0)
    axes[0].text(lay["layer"] + 0.6, 0.12, "L14 (the pick)", fontsize=S.LABEL_PT)
    axes[1].set_xlim(0, 52)
    axes[1].text(53, 0.10, "lookup bar 0.10", fontsize=S.LABEL_PT, color=LOOKUP, va="center")
    axes[1].set_xticks(layers)
    ax = axes[2]
    v122 = load(CONFLICT_122B)
    cells = [c for c in v122["cells"] if c["dict"] == "jpp" and c["k"] == 25 and c["omp"] == "signed"
             and c["rendering"] == "chat"]  # fmt: skip
    for reader, col, dx in (("PP", LOOKUP, -0.25), ("PM", INK, 0.25)):
        for c in sorted((c for c in cells if c["reader"] == reader), key=lambda c: c["layer"]):
            ax.plot([c["layer"] + dx] * 2, [c["excess"][1], c["excess"][2]], color=col, lw=1.6)
            ax.plot([c["layer"] + dx], [c["excess"][0]], "s", color=col, ms=5.5)
            S.record("ledger_lightning_layers", B122, f"conflict test, L{c['layer']}, "
                     f"{'lookup' if reader == 'PP' else 'recall'}: switches lost beyond random",
                     *c["excess"], n=c["n"], source=rel(CONFLICT_122B))  # fmt: skip
    ax.axhline(0, color="#999999", lw=0.8)
    ax.axhline(0.10, color=LOOKUP, lw=0.8, ls="--")
    ax.axvline(33, color="#222222", lw=1.0)
    ax.set_xlim(22.5, 37.5)
    ax.set_xticks(sorted({c["layer"] for c in cells}))
    ax.set_ylim(-0.2, 0.9)
    ax.set_ylabel("lost beyond random")
    ax.set_xlabel("the 122B's layer (of 48)")
    ax.text(33.3, 0.78, "L33 (its L)", fontsize=S.LABEL_PT)
    ax.set_title("122B (FP8; MoE, ~10B active): the conflict test per layer", fontsize=S.LABEL_PT, weight="bold",
                 loc="left")
    for t in SLOT_MODELS[:3]:
        grey("ledger_lightning_layers", t, "L fixed in advance; conflict test in the README")
    fig.text(0.1, 0.008, "9B, 27B, Muse: their layer was fixed in advance (L12 / L32 / L26); their conflict test is the "
             "README's", fontsize=S.LABEL_PT - 1, color=GREY)  # fmt: skip
    return save(fig, "ledger_lightning_layers")


# ---- where the answer is readable and usable (batch 52 B) -----------------------------------------------------------

ANSWER_MAP = R / "x52_answer_map" / "x52-20261029T004559Z" / "verdict.json"
ANSWER_MAP_L = R / "x52_answer_map" / "x52cov-20261029T005848Z" / "verdict.json"  # Lightning: our main test only


def answer_map(plt) -> str:
    """Per model, dataset (our main test, Zach's described passages) and reader: left, the best share of items with
    the answer word in the lens's top 5 before the answer layer (the rule's 0.5 dashed); right, the answers changed by
    writing the answer word's lens directions at that cell (the better of gains 1 and 2, whiskers 95%) with the random
    part of the same gain in grey (the rule's 0.3 dashed); the combination at the right."""
    v, vl = load(ANSWER_MAP), load(ANSWER_MAP_L)
    combos = {**v["combinations"], **vl["combinations"]}
    srcs = {m["target"]: ANSWER_MAP for m in v["models"]} | {m["target"]: ANSWER_MAP_L for m in vl["models"]}
    by = {m["target"]: m for m in v["models"] + vl["models"]}
    rows = []
    for t in SLOT_MODELS:
        for d, dname in (("main", "ours"), ("z2", "Zach's")):
            for rd in ("lookup", "recall"):
                rows.append((by[t], d, dname, rd))
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 0.36 * len(rows) + 1.9), sharey=True,
                             gridspec_kw={"width_ratios": [1, 1.25]})  # fmt: skip
    h = fig.get_figheight()
    fig.subplots_adjust(left=0.26, right=0.8, top=1 - 1.25 / h, bottom=0.75 / h, wspace=0.22)
    S.title(fig, "On Zach's passages the answer is readable and usable; on ours rarely",
            "Ours: our main test; Zach's: his described passages. Grey: a random part; ○ hollow: Lightning")  # fmt: skip
    labels = []
    for i, (m, d, dname, rd) in enumerate(rows):
        t, col, y = m["target"], (LOOKUP if rd == "lookup" else INK), -i
        labels.append(f"{SHORT[t]}{' ○' if t == LT else ''}, {dname}, {rd}")
        if d not in m["writes"]:  # Lightning on Zach's passages: the read has not landed
            if rd == "lookup":
                grey("ledger_answer_map", t, "Zach's passages: read pending", axes[0], 0.02, y - 0.5)
                _SLOTS["ledger_answer_map"].pop(SHORT[t])  # the model has data (ours); only these rows are grey
            continue
        r = m["maps"][d]["readers"][rd]
        best = r["readable"]["best_before"]
        hollow = t == LT
        axes[0].barh(y, best["top5"], color="white" if hollow else col, edgecolor=col, height=0.6, alpha=0.85)
        w = m["writes"][d][rd]["switch"]
        g = "ans1" if w["ans1"][0] >= w["ans2"][0] else "ans2"
        whisker(axes[1], y, w[g], col, hollow=hollow)
        axes[1].plot([w["rand" + g[-1]][0]], [y], "o", color=NULL, ms=5)
        combo = combos[f"{t}|{d}|{rd}"]["combination"]
        axes[1].text(1.05, y, combo, va="center", fontsize=S.LABEL_PT, color="#222222", clip_on=False)
        S.record("ledger_answer_map", t, f"{dname}, {rd}: best top-5 share before the answer layer "
                 f"({best['group']} L{best['layer']})", best["top5"], source=rel(srcs[t]))  # fmt: skip
        S.record("ledger_answer_map", t, f"{dname}, {rd}: answers changed by the write, gain {g[-1]}", *w[g],
                 n=m["writes"][d][rd]["n"], source=rel(srcs[t]))  # fmt: skip
    for ax, bar in ((axes[0], 0.5), (axes[1], 0.3)):
        ax.axvline(bar, color="#555555", lw=0.9, ls="--")
        ax.set_xlim(0, 1.0)
        ax.set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        ax.grid(axis="x", color="#eeeeee")
        for b in (3.5, 7.5, 11.5):
            ax.axhline(-b, color="#cccccc", lw=0.8)
    axes[0].set_yticks([-i for i in range(len(rows))], labels)
    axes[0].tick_params(axis="y", length=0)
    axes[0].set_ylim(-len(rows) + 0.4, 0.6)
    axes[0].set_xlabel("answer in the lens's top 5")
    axes[1].set_xlabel("answers changed by writing it")
    note_slot(fig, "ledger_answer_map")
    return save(fig, "ledger_answer_map")


# ---- the routes test on four models (Lightning's coverage run beside the others) ------------------------------------

ROUTES = {  # model -> (the main run's verdict, the run holding "the address alone")
    "qwen3.5-9b": (R / "x6_routes" / "qwen35_9b_x6_routes" / "verdict-20261025T104535Z" / "verdict.json",
                   R / "x6_routes" / "qwen35_9b_x6_routes_keeponly" / "verdict-20261025T152603Z" / "verdict.json"),
    "qwen3.6-27b": (R / "x6_routes" / "x6_routes_27b" / "verdict-20261025T105901Z" / "verdict.json",
                    R / "x6_routes" / "x6_routes_keeponly_27b" / "verdict-20261025T153505Z" / "verdict.json"),
    "muse-glimmer-30b": (R / "x6_routes" / "muse30b_x6_routes" / "verdict-20261026T004455Z" / "verdict.json",) * 2,
    "nemotron-3.5-lightning": (R / "x6_routes" / "nem35l_x52_routes" / "verdict-20261029T004324Z" / "verdict.json",) * 2,
    # the 122B: its 0.80 run failed the gate (recall 0.797); the g75 runs lowered it to 0.75 after the data: below gate
    B122: (R / "x6_routes" / "qwen35_122b_x6_routes_g75" / "verdict-20261025T134214Z" / "verdict.json",
           R / "x6_routes" / "qwen35_122b_x6_routes_keeponly_g75" / "verdict-20261025T202506Z" / "verdict.json"),
}  # fmt: skip


def routes(plt) -> str:
    """Per model (9B, 27B, Muse, Lightning, the 122B), the lookup's answer when another item's locker sentence moved
    and took a new number: under the whole change, without the address, and with the address added by itself; identity,
    position, value and the original answer, stacked; the 122B below its gate (○, faded)."""
    arms = (("whole", "whole change"), ("no_alf", "without the address"), ("keep_alf", "the address alone"))
    rows = []
    for t, (main, keep) in ROUTES.items():
        if t == B122:
            below_gate("ledger_routes", t)
        for arm, lab in arms:
            src = keep if arm == "keep_alf" else main
            r = next(x for x in load(src)["rows"] if x["condition"] == "C2" and x["arm"] == arm)
            rows.append((f"{SHORT[t]}{' ○' if t == B122 else ''}, {lab}", r, t, arm, src))
    fig, ax = plt.subplots(figsize=(S.WIDTH, 0.42 * len(rows) + 1.9))
    h = fig.get_figheight()
    fig.subplots_adjust(left=0.3, right=0.97, top=1 - 1.3 / h, bottom=0.65 / h)
    S.title(fig, "Every model's lookup takes identity or position, never the value",
            "The lookup's answer when another item's locker moved and took a new number; routes scenes, 300 each")  # fmt: skip
    parts = (("identity", S.COL["identity"]), ("position", S.COL["position"]), ("value", S.COL["value"]),
             ("original", S.COL["original"]))  # fmt: skip
    for i, (_, r, t, arm, src) in enumerate(rows):
        left = 0.0
        for p, col in parts:
            w = r["share"][p][0]
            ax.barh(-i, w, left=left, color=col, height=0.62, edgecolor="white", lw=0.5, alpha=0.45 if t == B122 else 1)
            if w >= 0.12:
                ax.text(left + w / 2, -i, f"{w:.2f}", ha="center", va="center", fontsize=S.LABEL_PT - 1,
                        color="white" if p == "identity" else "#222222")  # fmt: skip
            left += w
            S.record("ledger_routes", t, f"another item moved, {arm}: {p} share", *r["share"][p], n=r["n"],
                     source=rel(src))  # fmt: skip
    for b in range(1, len(ROUTES)):
        ax.axhline(-(3 * b - 0.5), color="#999999", lw=0.8)
    rows_axis(ax, [r[0] for r in rows])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("share of the lookup's answers")
    for k, (p, col) in enumerate(parts):
        ax.text(0.25 * k, 1.03, p, color=col if p != "original" else "#777777", fontsize=S.LABEL_PT, weight="bold",
                transform=ax.transAxes)  # fmt: skip
    return save(fig, "ledger_routes")


SIX = {"qwen3.5-9b": R / "x47_six" / "x47_2-20261028T113102Z" / "x47_2.json",
       "qwen3.6-27b": R / "x47_six" / "x52_six-20261029T004919Z" / "x47_2.json",
       "muse-glimmer-30b": R / "x47_six" / "x47_2-20261028T113102Z" / "x47_2.json",
       "nemotron-3.5-lightning": R / "x47_six" / "x52_six-20261029T011006Z" / "x47_2.json"}  # fmt: skip


def six_lockers(plt) -> str:
    """Per model (9B, 27B, Muse, Lightning), at dose 2: the share of start slots from which one fixed shift sends at
    least 0.25 of lookups one slot on, and the share of given-slot swaps that reach 0.25; the rule's 'most pairs' as a
    dashed 0.5."""
    fig, ax = plt.subplots(figsize=(S.WIDTH, 3.7))
    fig.subplots_adjust(left=0.1, right=0.78, top=0.74, bottom=0.14)
    S.title(fig, "One shift moves no lookup; pair swaps work on 9B, Muse and Lightning",
            "At dose 2: start slots where one shift works (of 5), and slot pairs a swap reaches (of 30)")  # fmt: skip
    for i, (t, path) in enumerate(SIX.items()):
        m = next(x for x in load(path)["models"] if x["target"] == t)
        r = m["rules"]["2"]
        shift, pairs = r["v_works_from"] / 5, r["pairs_reaching"] / r["pairs"]
        ax.bar(i - 0.18, shift, width=0.34, color=ADDRESS, alpha=0.45, edgecolor=ADDRESS)
        ax.bar(i + 0.18, pairs, width=0.34, color=ADDRESS, edgecolor=ADDRESS)
        ax.text(i + 0.18, pairs + 0.03, f"{r['pairs_reaching']} of {r['pairs']}", ha="center", fontsize=S.LABEL_PT)
        ax.text(i - 0.18, shift + 0.03, f"{r['v_works_from']} of 5", ha="center", fontsize=S.LABEL_PT)
        S.record("ledger_six_lockers", t, "dose 2: start slots where one shift sends >= 0.25 one slot on (of 5)",
                 r["v_works_from"], source=rel(path))  # fmt: skip
        S.record("ledger_six_lockers", t, "dose 2: given-slot swaps reaching 0.25 (of 30)", r["pairs_reaching"],
                 source=rel(path))  # fmt: skip
        S.record("ledger_six_lockers", t, "the rule's label at dose 2", m["label"], source=rel(path))
    ax.axhline(0.5, color="#555555", lw=0.9, ls="--")
    ax.text(-0.48, 0.52, "most pairs", fontsize=S.LABEL_PT, color=S.COL["muted"], va="bottom")
    labels = [next(x for x in load(p)["models"] if x["target"] == t)["label"] for t, p in SIX.items()]
    ax.set_xticks(range(len(SIX) + 1), [f"{SHORT[t]}\n{lab}" for t, lab in zip(SIX, labels, strict=True)] + ["122B"])
    grey("ledger_six_lockers", B122, "not run", ax, len(SIX), 0.05, ha="center")
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("share")
    ax.text(1.03, 0.75, "light: one shift\n(start slots)\n\ndark: swaps per pair\n(slot pairs)", transform=ax.transAxes,
            fontsize=S.LABEL_PT, color=S.COL["muted"], va="center")  # fmt: skip
    return save(fig, "ledger_six_lockers")


# ---- restyled from verdict folders: the lens part's atoms (52 A), the read window (51.5), the described bridge (Z2) --

ATOMS = R / "x52_atoms" / "report-20261029T000125Z" / "tables.json"
ATOMS_L = R / "x52_atoms" / "report-20261029T010648Z" / "tables.json"  # Lightning's run (our scenes only)
DEPTH = R / "x51_depth" / "x51_5-20261028T181100Z" / "x51_5.json"
DEPTH_L = R / "x51_depth" / "x52_depth51-20261029T083500Z" / "x51_5.json"  # Lightning, the 9B / 27B design
Z2 = R / "x50_zach" / "z2-20261028T162710Z" / "z2.json"
Z2_L = R / "x50_zach" / "x52_z2-20261029T025625Z" / "z2.json"  # Lightning's coverage run (L14 decides)
LIGHTNING_HOLLOW = "○ Lightning: gate set after its 60-scene pre-check (hollow)"


def atoms(plt) -> str:
    """Per model and view, the share of the lens part's rebuilt energy in each word class: our main test (the recall's
    view) and Zach's described passages (each reader's own change); stacked. Lightning: our scenes only (its row
    label carries ○, its gate set after the 60-scene pre-check)."""
    v = load(ATOMS)
    groups = (("bridge", "the original bridge word", S.COL["identity"]),
              ("new_bridge", "the new bridge word", ADDRESS),
              ("answer", "an answer word", S.COL["value"]),
              ("named", "other words of the prompt", "#9a9a9a"),
              ("other", "other words", S.COL["original"]))  # fmt: skip
    merge = {"answer": ("answer_own", "answer_other"), "named": ("scene_item", "person", "same_class", "function")}
    rows = []
    for t, _ in MODEL3:
        s = v["summary"][t]
        for key, view, lab in (("e1", "PM", "our scenes, recall"), ("z2", "K", "Zach's described, lookup"),
                               ("z2", "M", "Zach's described, recall")):  # fmt: skip
            rows.append((f"{SHORT[t]}, {lab}", s[key][view]["energy"], s[key][view]["n"], t, f"{key} {view}"))
    sl = load(ATOMS_L)["summary"]["nemotron-3.5-lightning"]["e1"]["PM"]
    rows.append(("Lightning ○, our scenes, recall", sl["energy"], sl["n"], "nemotron-3.5-lightning", "e1 PM"))
    fig, ax = plt.subplots(figsize=(S.WIDTH, 0.42 * len(rows) + 2.0))
    h = fig.get_figheight()
    fig.subplots_adjust(left=0.3, right=0.97, top=1 - 1.45 / h, bottom=0.65 / h)
    S.title(fig, "The lens part holds the two bridge words, almost never the answer",
            "Share of the lens part's rebuilt energy by what each of its 25 directions decodes to; 50 items each")  # fmt: skip
    for i, (_, energy, n, t, tag) in enumerate(rows):
        left = 0.0
        for key, _, col in groups:
            w = sum(energy[k][0] for k in merge.get(key, (key,)))
            ax.barh(-i, w, left=left, color=col, height=0.62, edgecolor="white", lw=0.5)
            if w >= 0.08:
                ax.text(left + w / 2, -i, f"{w:.2f}", ha="center", va="center", fontsize=S.LABEL_PT - 1,
                        color="white" if key in ("bridge",) else "#222222")  # fmt: skip
            left += w
        src = ATOMS_L if t == "nemotron-3.5-lightning" else ATOMS
        for k, x in energy.items():
            S.record("ledger_atoms", t, f"{tag}: rebuilt energy in '{v['classes'][k]}'", *x, n=n, source=rel(src))
    for b in (2.5, 5.5, 8.5):
        ax.axhline(-b, color="#999999", lw=0.8)
    rows_axis(ax, [r[0] for r in rows])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("share of the rebuilt energy")
    for k, (_, lab, col) in enumerate(groups):
        ax.text(0.2 * k, 1.02 + 0.045 * (k % 2), lab, color=col if col != S.COL["original"] else "#777777",
                fontsize=S.LABEL_PT - 1, weight="bold", transform=ax.transAxes)  # fmt: skip
    note_slot(fig, "ledger_atoms")
    return save(fig, "ledger_atoms")


def read_window(plt) -> str:
    """Per model (9B, 27B), the share of each reader's answers switched by the whole change at one layer at a time, on
    Zach's named passages (solid, band 95%) and on our routes scenes (dashed); 0.3 dotted, the window's end."""
    by = {m["target"]: (m, path) for path in (DEPTH, DEPTH_L) for m in load(path)["models"]
          if m.get("status", "tested") == "tested"}  # fmt: skip
    fig, axes = plt.subplots(1, 5, figsize=(S.WIDTH, 4.0), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.74, bottom=0.3, wspace=0.12)
    S.title(fig, "The 9B and Lightning read his passages over our layers; the 27B not",
            "Answers switched by the whole change at one layer; solid: his passages, dashed: our scenes")  # fmt: skip
    for ax, t in zip(axes[:4], SLOT_MODELS, strict=True):
        if t not in by:
            grey_panel("ledger_read_window", t, "not designed\n(9B / 27B only)", ax)
            continue
        m, src = by[t]
        ax.set_title(SHORT[t] + (" ○" if t == LT else ""), fontsize=12, weight="bold", loc="left")
        layers = sorted(int(k) for k in m["cells"])
        for reader, col in (("lookup", LOOKUP), ("recall", INK)):
            sw = [m["cells"][str(la)][reader]["switch"] for la in layers]
            ax.fill_between(layers, [x[1] for x in sw], [x[2] for x in sw], color=col, alpha=0.15, lw=0)
            ax.plot(layers, [x[0] for x in sw], "-", color=col, lw=1.8)
            ref = m["reference"]["rates"][reader]
            rl = sorted(int(k) for k in ref)
            ax.plot(rl, [ref[str(la)] for la in rl], "--", color=col, lw=1.3)
            for la, x in zip(layers, sw, strict=True):
                S.record("ledger_read_window", m["target"], f"his named passages, layer {la}: {reader} switched", *x,
                         n=m["cells"][str(la)][reader]["n"], source=rel(src))  # fmt: skip
        ax.axhline(0.3, color="#555555", lw=0.8, ls=":")
        ax.set_ylim(-0.02, 1.02)
        ends = m["ends"]["pooled"]
        ax.set_xlabel(f"layer\nends, his / ours:\nlookup L{ends['lookup']} / L{m['reference']['lookup']}\n"
                      f"recall L{ends['recall']} / L{m['reference']['recall']}", fontsize=S.LABEL_PT - 1)  # fmt: skip
    axes[0].set_ylabel("switched")
    axes[0].text(0.03, 0.08, "lookup", color=LOOKUP, transform=axes[0].transAxes, fontsize=S.LABEL_PT)
    axes[0].text(0.03, 0.18, "recall", color=INK, transform=axes[0].transAxes, fontsize=S.LABEL_PT)
    grey_panel("ledger_read_window", B122, "not run", axes[4])
    return save(fig, "ledger_read_window")


def described(plt) -> str:
    """Per model, on Zach's described passages: our gap (the recall's switches lost beyond random minus the lookup's)
    where both readers switch enough to tell, and Zach's knock-out (the recall's loss minus the lookup's under his top-10
    lens directions) beside, with his rotated-direction control in grey. Lightning (its coverage run, L14) hollow: its
    gate was set after the 60-scene pre-check."""
    models = [(m, Z2) for m in load(Z2)["models"]] + [(m, Z2_L) for m in load(Z2_L)["models"]]
    fig, ax = plt.subplots(figsize=(S.WIDTH, 4.0))
    fig.subplots_adjust(left=0.22, right=0.97, top=0.74, bottom=0.15)
    S.title(fig, "Zach's knock-out hits the recall more; our gap is unclear (withdrawn)",
            "Recall's loss minus the lookup's, Zach's described passages; whiskers 95%; ○ hollow: Lightning")  # fmt: skip
    labels = []
    for i, (m, path) in enumerate(models):
        hollow = m["target"] == "nemotron-3.5-lightning"
        la = str(m["layers"][0])
        r = m["layer_results"][la]
        ok = r["lookup"]["valid"] and r["recall"]["valid"]
        if ok:
            whisker(ax, -i + 0.15, r["gap"], INK, hollow=hollow)
        else:
            ax.text(-0.45, -i + 0.15, "our gap: the lookup switches too rarely to tell", fontsize=S.LABEL_PT - 1,
                    color=S.COL["muted"], va="center")  # fmt: skip
        his, rot = m["beside"]["full"]["paper10"]["m_minus_k"], m["beside"]["full"]["paper10_rot"]["m_minus_k"]
        whisker(ax, -i - 0.15, his, JPP, hollow=hollow)
        ax.plot([rot[0]], [-i - 0.15], "o", color=NULL, ms=5)
        labels.append(f"{SHORT[m['target']]}{' ○' if hollow else ''} (L{la})")
        S.record("ledger_described", m["target"], f"L{la}: our gap (recall minus lookup extra loss)", *r["gap"],
                 source=rel(path))  # fmt: skip
        S.record("ledger_described", m["target"], "Zach's knock-out, recall minus lookup", *his, source=rel(path))
    rows_axis(ax, labels)
    zero_band(ax, -0.8, 1.0)
    ax.set_xlabel("recall's loss minus the lookup's")
    ax.text(-0.78, 0.0, "dark: our removal\nteal: his knock-out\ngrey: his rotated control", fontsize=S.LABEL_PT,
            color=S.COL["muted"], va="center")  # fmt: skip
    note_slot(fig, "ledger_described")
    return save(fig, "ledger_described")


# ---- the address swap by dose and the split by sentence order, four models (Lightning's coverage runs) ---------------

SWAP = {
    "qwen3.5-9b": R / "x8_write" / "qwen35_9b_x8_write" / "verdict-20261026T110254Z" / "verdict.json",
    "qwen3.6-27b": R / "x8_write" / "x8_write_27b" / "verdict-20261026T125548Z" / "verdict.json",
    "muse-glimmer-30b": R / "x8_write" / "muse30b_x8_write" / "verdict-20261026T141141Z" / "verdict.json",
    "nemotron-3.5-lightning": R / "x8_write" / "nem35l_x52_write" / "verdict-20261029T005021Z" / "verdict.json",
    B122: R / "x8_write" / "qwen35_122b_x8_write_g75" / "verdict-20261026T125705Z" / "verdict.json",  # g75: below gate
}
ORDER = {"three": R / "x0_composition" / "split-by-order-20261026T173323Z" / "split.json",
         "nemotron-3.5-lightning": R / "x0_composition" / "split-by-order-20261029T005451Z" / "split.json"}  # fmt: skip


def address_swap(plt) -> str:
    """Per model, the share of lookups sent to the swapped-in locker by the address swap at doses 1, 2 and 4 (whiskers
    95%), a random vector of the same size dashed, and the recalls changed by the same swap (the collateral) in grey;
    the 122B's g75 run below its gate (hollow ○)."""
    fig, axes = plt.subplots(1, len(SWAP), figsize=(S.WIDTH, 3.5), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.72, bottom=0.17, wspace=0.12)
    S.title(fig, "Swapping the address sends the lookup to the swapped-in locker",
            "Lookups sent to the target by dose (orange); dashed: a random vector; grey: recalls changed")  # fmt: skip
    for ax, (t, path) in zip(axes, SWAP.items(), strict=True):
        cells = {(c["kind"], c["s"]): c for c in load(path)["cells"] if c["pair"] is None}
        doses = sorted(s for k, s in cells if k == "write")
        tgt = [cells[("write", s)]["target"] for s in doses]
        below = t == B122
        if below:
            below_gate("ledger_address_swap", t)
        ax.plot(doses, [x[0] for x in tgt], "-^", color=ADDRESS, ms=6, lw=1.8, mfc="white" if below else ADDRESS)
        for s, x in zip(doses, tgt, strict=True):
            ax.plot([s, s], [x[1], x[2]], color=ADDRESS, lw=1.2)
            S.record("ledger_address_swap", t, f"dose {s:g}: lookups sent to the target", *x, n=cells[("write", s)]["n"],
                     source=rel(path))  # fmt: skip
            S.record("ledger_address_swap", t, f"dose {s:g}: recalls changed", cells[("write", s)]["recall_changed"],
                     source=rel(path))  # fmt: skip
        rd = sorted(s for k, s in cells if k == "random")
        ax.plot(rd, [cells[("random", s)]["target"][0] for s in rd], "--", color=NULL, lw=1.3)
        ax.plot(doses, [cells[("write", s)]["recall_changed"] for s in doses], "-o", color="#8c8c8c", ms=4, lw=1.2)
        ax.set_title(SHORT[t] + (" ○" if t in (LT, B122) else ""), fontsize=12, weight="bold", loc="left")
        ax.set_xscale("log", base=2)
        ax.set_xticks([1, 2, 4], ["1", "2", "4"])
        ax.set_ylim(-0.02, 1.0)
        ax.set_xlabel("dose")
    axes[0].set_ylabel("share")
    return save(fig, "ledger_address_swap")


def order_split(plt) -> str:
    """Per model, the share of lookups the whole change switches on the main test, split by whether the item's locker
    sentence came before the asked pick or after it."""
    cells = {}
    for t, _ in (*MODEL3, ("nemotron-3.5-lightning", ""), (B122, "")):
        path = ORDER["nemotron-3.5-lightning" if t == "nemotron-3.5-lightning" else "three"]
        cells[t] = (load(path)["cells"][f"{t}|swap"]["cells"], path)
    fig, ax = plt.subplots(figsize=(S.WIDTH, 3.4))
    fig.subplots_adjust(left=0.1, right=0.8, top=0.72, bottom=0.16)
    S.title(fig, "The bridge word switches the lookup when its locker came first",
            "Main test: lookups switched by the whole change, by where the item's locker sentence sits")  # fmt: skip
    for i, (t, (c, path)) in enumerate(cells.items()):
        for dx, grp, col in ((-0.18, "before", LOOKUP), (0.18, "after", "#c9bdf0")):
            v = c[grp]["lookup_switch"]
            ax.bar(i + dx, v, width=0.34, color=col, edgecolor=LOOKUP)
            ax.text(i + dx, v + 0.02, f"n {c[grp]['n']}", ha="center", fontsize=S.LABEL_PT - 1, color=S.COL["muted"])
            S.record("ledger_order_split", t, f"locker {grp} the pick: lookups switched", round(v, 4), n=c[grp]["n"],
                     source=rel(path))  # fmt: skip
    ax.set_xticks(range(len(cells)), [SHORT[t] for t in cells])
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("lookups switched")
    ax.text(1.02, 0.7, "dark: locker before\nthe pick\n\nlight: locker after\nthe pick", transform=ax.transAxes,
            fontsize=S.LABEL_PT, color=S.COL["muted"], va="center")  # fmt: skip
    return save(fig, "ledger_order_split")


# ---- attention under the swap (49.7) --------------------------------------------------------------------------------

ATTN = (R / "x49_attn" / "x49_7-20261028T154511Z" / "verdict.json",
        R / "x49_attn" / "x52_attn-20261029T013321Z" / "verdict.json")  # fmt: skip


def attention(plt) -> str:
    """Per model, the best head (chosen on the fit half) at the last token: the attention moved to the swapped-in
    locker on read pairs where the lookup switched, on pairs where it did not, and under a random vector of the swap's
    size on the switched pairs; the rule's bars (0.30 switched, 0.10 non-switched) as lines."""
    res = {r["target"]: (r, path) for path in ATTN for r in load(path)["results"]}
    models = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning")
    arms = (("swap_switched", "pairs that switched", LOOKUP, 1.0), ("swap_nonswitched", "pairs that did not", LOOKUP, 0.35),
            ("random_switched", "a random vector (switched pairs)", NULL, 1.0))  # fmt: skip
    fig, ax = plt.subplots(figsize=(S.WIDTH, 3.8))
    fig.subplots_adjust(left=0.1, right=0.74, top=0.74, bottom=0.17)
    S.title(fig, "Heads move with the swap even where the lookup did not switch",
            "Best head per model at the last token: attention moved to the swapped-in locker")  # fmt: skip
    ticks = []
    for i, t in enumerate(models):
        r, path = res[t]
        bh = r["best_head"]
        h = next(x for x in r["sites"]["last"]["heads"] if (x["layer"], x["head"]) == (bh["layer"], bh["head"]))
        name = f"L{bh['layer']}:h{bh['head']}"
        ticks.append(f"{SHORT[t]}\n{name}")
        for j, (key, lab, col, alpha) in enumerate(arms):
            v = h["stats"][key]
            x = i + (j - 1) * 0.27
            ax.bar(x, v[0], width=0.25, color=col, alpha=alpha, edgecolor=col)
            ax.plot([x, x], [v[1], v[2]], color="#222222", lw=1.2)
            S.record("ledger_attention", t, f"best head {name}, last token: attention moved, {lab}", *v,
                     source=rel(path))  # fmt: skip
    ax.axhline(0.30, color="#555555", lw=0.9, ls="--")
    ax.axhline(0.10, color="#555555", lw=0.9, ls=":")
    ax.set_xticks(range(len(models) + 1), [*ticks, "122B"])
    grey("ledger_attention", B122, "not run", ax, len(models), 0.1, ha="center")
    ax.set_ylim(-0.05, 2.0)
    ax.set_ylabel("attention moved")
    ax.text(1.03, 0.62, "dark: pairs that switched\nlight: pairs that did not\ngrey: a random vector\n\n"
            "dashed: 0.30, the bar on\nswitched pairs\ndotted: 0.10, the bar on\npairs that did not",
            transform=ax.transAxes, fontsize=S.LABEL_PT, color=S.COL["muted"], va="center")  # fmt: skip
    return save(fig, "ledger_attention")


# ---- the swap after neutral sentences (47.16) and the gain map (49.1) -----------------------------------------------

DISTANCE = (R / "x47_distance" / "x47_16-20261028T131501Z" / "x47_16.json",
            R / "x47_distance" / "x52_distance-20261029T023426Z" / "x47_16.json",
            R / "x47_distance" / "x52_distance-20261029T090323Z" / "x47_16.json")  # fmt: skip  # Muse's r2
GAIN = (R / "x49_gain" / "x49_1-20261028T154510Z" / "x49_1.json",
        R / "x49_gain" / "x52_gain-20261029T021814Z" / "x49_1.json")  # fmt: skip


def distance(plt) -> str:
    """Per tested model, by the number of neutral sentences k before the picks: the position and identity shares of the
    lookup under the whole change, and the address swap's share sent to the target (dose 2)."""
    runs = [(m, path) for path in DISTANCE for m in load(path)["models"] if m["status"] == "tested"]
    by = {m["target"]: (m, path) for m, path in runs}
    ks = ("0", "5", "20", "50")
    fig, axes = plt.subplots(1, 5, figsize=(S.WIDTH, 3.6), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.72, bottom=0.17, wspace=0.12)
    S.title(fig, "The address survives fifty neutral sentences",
            "Lookups under the whole change by route, and the swap's lookups sent to the target, by sentences added")  # fmt: skip
    ident = S.MARK_COL["identity"]
    for ax, t in zip(axes[:4], SLOT_MODELS, strict=True):
        if t not in by:
            grey_panel("ledger_distance", t, "no outcomes\n(rerun running)", ax)
            continue
        m, path = by[t]
        ax.set_title(SHORT[t], fontsize=12, weight="bold", loc="left")
        series = (("position under the whole change", ADDRESS, "o", "-",
                   [m["cells"][k]["routes"]["whole"]["position"] for k in ks]),
                  ("identity under the whole change", ident, "o", "-",
                   [m["cells"][k]["routes"]["whole"]["identity"] for k in ks]),
                  ("the swap: lookups sent to the target", ADDRESS, "^", "--",
                   [m["cells"][k]["swap"]["write"] for k in ks]))  # fmt: skip
        for lab, col, mk, ls, vals in series:
            xs = range(len(ks))
            ax.plot(xs, [v[0] for v in vals], ls, marker=mk, color=col, lw=1.6, ms=6)
            for x, v in zip(xs, vals, strict=True):
                ax.plot([x, x], [v[1], v[2]], color=col, lw=1.2)
            for k, v in zip(ks, vals, strict=True):
                S.record("ledger_distance", t, f"{k} neutral sentences: {lab}", *v, n=m["cells"][k]["n"],
                         source=rel(path))  # fmt: skip
        ax.set_xticks(range(len(ks)), ks)
        ax.set_xlabel("sentences added")
        ax.set_ylim(0, 1.0)
    axes[0].set_ylabel("share of lookups")
    axes[3].text(0.98, 0.97, "blue: identity\norange: position\ndashed: the swap", transform=axes[-1].transAxes,
                  ha="right", va="top", fontsize=S.LABEL_PT, color=S.COL["muted"])  # fmt: skip
    grey_panel("ledger_distance", B122, "not run", axes[4])
    return save(fig, "ledger_distance")


def gain(plt) -> str:
    """Per model, the five cells the gain map's rule reads (recall at (2,0) and at (0,2) without the address, the
    recall's random corner R(2,0), the lookup at (2,0) and at (0,1)), each with the rule's bar as a tick."""
    runs = [(m, path) for path in GAIN for m in load(path)["models"]]
    cells = (("recall", "J(2,0)", "recall,\nlens part x2", INK, 0.5),
             ("recall", "J(0,2)-U", "recall, rest x2\nno address", INK, 0.5),
             ("recall", "R(2,0)", "recall,\nrandom x2", NULL, 0.15),
             ("lookup", "J(2,0)", "lookup,\nlens part x2", LOOKUP, 0.10),
             ("lookup", "J(0,1)", "lookup,\nrest x1", LOOKUP, 0.6))  # fmt: skip
    fig, ax = plt.subplots(figsize=(S.WIDTH, 3.9))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.7, bottom=0.25)
    S.title(fig, "The gain map fits neither reading on any model",
            "The five cells the rule reads, per model; ticks: the rule's bars")  # fmt: skip
    w = 0.16
    for i, (m, path) in enumerate(runs):
        t = m["target"]
        for j, (reader, arm, _lab, col, bar) in enumerate(cells):
            v = m["readers"][reader]["rate"][arm]
            x = i + (j - 2) * w
            ax.bar(x, v[0], width=w * 0.9, color=col, alpha=0.85 if col != NULL else 1.0)
            ax.plot([x, x], [v[1], v[2]], color="#222222", lw=1.0)
            ax.plot([x - w * 0.45, x + w * 0.45], [bar, bar], color="#c0392b", lw=1.6)
            S.record("ledger_gain", t, f"{reader} {arm}: switch rate", *v, n=m["n"], source=rel(path))
        S.record("ledger_gain", t, "the rule's label", m["label"], source=rel(path))
    ax.set_xticks(range(len(runs) + 1), [f"{SHORT[m['target']]}\n{m['label']}" for m, _ in runs] + ["122B"])
    grey("ledger_gain", B122, "not run", ax, len(runs), 0.05, ha="center")
    ax.set_xlim(-0.6, len(runs) + 0.5)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("switch rate")
    ax.text(0.0, -0.32, "per model, left to right: " + "; ".join(c[2].replace("\n", " ") for c in cells),
            transform=ax.transAxes, fontsize=S.LABEL_PT - 1, color=S.COL["muted"])  # fmt: skip
    return save(fig, "ledger_gain")


# ---- other kinds of item (47.11) ------------------------------------------------------------------------------------

AGNOSTIC = (R / "x47_agnostic" / "x47_11-20261028T143952Z" / "x47_11.json",
            R / "x47_agnostic" / "x52_agnostic-20261029T023820Z" / "x47_11.json",
            R / "x47_agnostic" / "x52_agnostic-20261029T031638Z" / "x47_11.json")  # fmt: skip


def agnostic(plt) -> str:
    """Per model, position answers lost without the address beyond a random part of its share, by kind of item: the
    address fit on animal scenes (filled) and refit per kind on a fit half (hollow); the rule's 0.3 dashed."""
    # the last folder re-reads the 27B with the same rows and adds Lightning; the first folder per model wins, so the
    # 27B keeps its first source (as the card cites it)
    runs: dict = {}
    for path in AGNOSTIC:
        for m in load(path)["models"]:
            if m["status"] == "tested":
                runs.setdefault(m["target"], (m, path))
    models = [t for t in SLOT_MODELS if t in runs]
    kinds = ("animals", "fruits", "names")
    fig, axes = plt.subplots(1, len(models) + 1, figsize=(S.WIDTH, 3.5), sharey=True)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.72, bottom=0.16, wspace=0.12)
    S.title(fig, "The animal-fit address does not carry over to other items as ruled",
            "Position answers lost without the address, beyond random; filled: fit on animals, hollow: refit per kind")  # fmt: skip
    for ax, t in zip(axes[: len(models)], models, strict=True):
        m, path = runs[t]
        ax.set_title(SHORT[t], fontsize=12, weight="bold", loc="left")
        for i, kind in enumerate(kinds):
            lab = m["labels"].get(kind)
            v = m["labels"]["fruits"]["fall_animals"] if kind == "animals" else lab["fall"]
            ax.plot([i - 0.1, i - 0.1], [v[1], v[2]], color=ADDRESS, lw=1.6)
            ax.plot([i - 0.1], [v[0]], "o", color=ADDRESS, ms=7)
            S.record("ledger_agnostic", t, f"{kind}: position lost without the animal-fit address, beyond random", *v,
                     source=rel(path))  # fmt: skip
            if kind != "animals":
                r = lab["refit"]["fall"]
                ax.plot([i + 0.1, i + 0.1], [r[1], r[2]], color=ADDRESS, lw=1.2)
                ax.plot([i + 0.1], [r[0]], "o", mfc="white", mec=ADDRESS, mew=1.5, ms=7)
                S.record("ledger_agnostic", t, f"{kind}: position lost without the refit address, beyond random", *r,
                         n=lab["refit"]["n"], source=rel(path))  # fmt: skip
        ax.axhline(0.3, color="#555555", lw=0.9, ls="--")
        ax.set_xticks(range(len(kinds)), kinds)
        ax.set_xlim(-0.5, len(kinds) - 0.5)
        ax.set_ylim(0, 0.75)
    axes[0].set_ylabel("position answers lost")
    axes[0].text(-0.45, 0.31, "rule's 0.3", fontsize=S.LABEL_PT, color=S.COL["muted"], va="bottom")
    grey_panel("ledger_agnostic", B122, "not run", axes[-1])
    return save(fig, "ledger_agnostic")


# ---- never the value, by text format (47.7 (c)) ---------------------------------------------------------------------

VALUEC = (R / "x47_value" / "x47_7c-20261028T123632Z" / "x47_7c.json",
          R / "x47_value" / "x52_valuec-20261029T040037Z" / "x47_7c.json")  # fmt: skip


def value_formats(plt) -> str:
    """Per model and text format, the lookup's answer under the whole change (identity, position, value, original,
    other), stacked; formats whose gate failed marked 'not tested'."""
    runs = {m["target"]: (m, path) for path in VALUEC for m in load(path)["models"]}
    models = [t for t in SLOT_MODELS if t in runs]
    fmts = ("prose", "json", "table")
    parts = (("identity", S.COL["identity"]), ("position", S.COL["position"]), ("value", S.COL["value"]),
             ("original", S.COL["original"]), ("other", "#e6e6e6"))  # fmt: skip
    fig, axes = plt.subplots(1, len(models) + 1, figsize=(S.WIDTH, 3.6), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.72, bottom=0.14, wspace=0.1)
    S.title(fig, "In prose, JSON and tables the lookup never takes the value",
            "The lookup's answer under the whole change, by text format; blue identity, orange position, grey original")  # fmt: skip
    for ax, t in zip(axes[: len(models)], models, strict=True):
        m, path = runs[t]
        ax.set_title(SHORT[t], fontsize=12, weight="bold", loc="left")
        for i, f in enumerate(fmts):
            c = m["cells"][f]
            if c is None or "arms" not in c:
                ax.text(i, 0.5, "not\ntested\n(gate)", ha="center", va="center", fontsize=S.LABEL_PT - 2,
                        color=S.COL["muted"])  # fmt: skip
                continue
            whole, bottom = c["arms"]["whole"], 0.0
            for p, col in parts:
                w = whole[p][0]
                ax.bar(i, w, bottom=bottom, color=col, width=0.6, edgecolor="white", lw=0.5)
                bottom += w
                if p in ("position", "value"):
                    S.record("ledger_value_formats", t, f"{f}, whole change: {p} share", *whole[p], n=c["n"],
                             source=rel(path))  # fmt: skip
        ax.set_xticks(range(len(fmts)), ["prose", "JSON", "table"])
        ax.set_xlim(-0.5, len(fmts) - 0.5)
        ax.set_ylim(0, 1.0)
    axes[0].set_ylabel("share of the lookup's answers")
    grey_panel("ledger_value_formats", B122, "not run", axes[-1])
    return save(fig, "ledger_value_formats")


# ---- the pooled person probe (49.3) ---------------------------------------------------------------------------------

POOLED = (R / "x49_probe" / "x49_3-20261028T154604Z" / "x49_3.json",
          R / "x49_probe" / "x52_probe49-20261029T044135Z" / "x49_3.json",
          R / "x49_probe" / "x52_probe49_below-20261029T085547Z" / "x49_3.json")  # fmt: skip  # Lightning below gate


def pooled_probe(plt) -> str:
    """Per model and layer, locker-after scenes: the probe for who picked the item, pooled over the locker sentence
    (whisker 95%) and its best single token (hollow); chance dotted, the rule's 0.85 dashed."""
    runs = {m["target"]: (m, path) for path in POOLED for m in load(path)["models"] if m["status"] == "tested"}
    rows = [(t, la) for t in SLOT_MODELS if t in runs for la in runs[t][0]["layers"]]
    below_gate("ledger_pooled_probe", LT)
    fig, ax = plt.subplots(figsize=(S.WIDTH, 0.5 * len(rows) + 1.9))
    fig.subplots_adjust(left=0.27, right=0.97, top=1 - 1.2 / fig.get_figheight(), bottom=0.75 / fig.get_figheight())
    S.title(fig, "No probe reads who picked an item at its locker sentence",
            "Locker-after scenes: who of three picked the item; filled: whole sentence, hollow: best token")  # fmt: skip
    for i, (t, la) in enumerate(rows):
        m, path = runs[t]
        pooled = m["results"][str(la)]["probes"]["picker"]["mean"]["after"]["accuracy"]
        best = m["rules"][str(la)]["i_token_max"]
        whisker(ax, -i, pooled, INK, hollow=t == LT)
        ax.plot([best], [-i - 0.25], "o", mfc="white", mec=INK, mew=1.5, ms=6)
        S.record("ledger_pooled_probe", t, f"L{la}: who picked it, pooled over the locker sentence", *pooled,
                 source=rel(path))  # fmt: skip
        S.record("ledger_pooled_probe", t, f"L{la}: who picked it, best single token", round(best, 4), source=rel(path))
    rows_axis(ax, [f"{SHORT[t]} L{la}" + (" ○ below gate" if t == LT else "") for t, la in rows])
    ax.set_ylim(-len(rows) + 0.3, 0.6)
    ax.axvline(1 / 3, color="#999999", lw=0.9, ls=":")
    ax.axvline(0.85, color="#555555", lw=0.9, ls="--")
    ax.text(1 / 3 + 0.01, 0.45, "chance", fontsize=S.LABEL_PT, color=S.COL["muted"])
    ax.text(0.86, 0.45, "rule's 0.85", fontsize=S.LABEL_PT, color=S.COL["muted"])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("probe accuracy")
    note_slot(fig, "ledger_pooled_probe")
    return save(fig, "ledger_pooled_probe")


# ---- the overview: coverage as a heatmap (Dan's restructure brief, 29 Oct 08:55) ------------------------------------

# fills by verdict; light tints so the cell words (dark ink) stay readable; the words carry the verdict too
VERDICT_FILL = {"H": "#a9d9b2", "B": "#f4d48c", "F": "#eda59d", "D": "#c9d6e7", "N": "#efefef", "X": "#efefef",
                "G": "#ffffff"}  # fmt: skip
PART_NAME = {"I": "I. Two readers", "II": "II. Identity", "III": "III. The address", "IV": "IV. Where, when",
             "V": "V. Other data", "VI": "VI. Did not hold"}  # fmt: skip


def coverage_map(plt) -> str:
    """One row per test card in the README's order (scripts/ledger_coverage.py's HEATMAP), one column per model (27B,
    Lightning, 9B, Muse, and the 122B where it has a verdict), each cell coloured by the card's verdict and labelled with
    its words; Parts I-VI in the left gutter. No number is drawn (every cell is a verdict word)."""
    from scripts import ledger_coverage as LC

    rows = LC.heatmap_cells()
    cols = [name for _, name in LC.COLUMNS] + ["122B"]
    gap = 0.45  # rows of white space between Parts
    ys, y, last = [], 0.0, None
    for part, *_ in rows:
        if last is not None and part != last:
            y += gap
        ys.append(y)
        y += 1
        last = part
    n_rows = y
    row_in = 0.235
    top_in, bottom_in = 1.55, 0.1
    fig = plt.figure(figsize=(S.WIDTH, n_rows * row_in + top_in + bottom_in))
    h = fig.get_figheight()
    ax = fig.add_axes((0.415, bottom_in / h, 0.575, (n_rows * row_in) / h))
    S.title(fig, "Which test ran on which model, and what its rule said",
            "One row per card, in the README's order; each cell names the card's verdict")  # fmt: skip
    ax.set_xlim(0, len(cols))
    ax.set_ylim(n_rows, 0)
    ax.axis("off")
    for (part, anchor, label, cells), yy in zip(rows, ys, strict=True):
        ax.text(-0.06, yy + 0.5, label, ha="right", va="center", fontsize=S.FONT - 1, color="#222222")
        for j, (code, words) in enumerate([*cells, LC.heatmap_122b(anchor, label)]):
            hatch = "////" if code == "G" else None
            ax.add_patch(plt.Rectangle((j + 0.03, yy + 0.06), 0.94, 0.88, facecolor=VERDICT_FILL[code],
                                       edgecolor="#c8c8c8" if code in "GNX" else "none", lw=0.6, hatch=hatch))  # fmt: skip
            muted = code in "GNX"
            ax.text(j + 0.5, yy + 0.5, words, ha="center", va="center", fontsize=S.FONT - (2.5 if len(words) > 13 else 1.5),
                    color=S.COL["muted"] if muted else "#1a1a1a",
                    bbox={"boxstyle": "square,pad=0.05", "fc": "white", "ec": "none"} if code == "G" else None)  # fmt: skip
    # Parts in the left gutter: a bracket and the Part's name, rotated
    for part in PART_NAME:
        idx = [i for i, r in enumerate(rows) if r[0] == part]
        y0, y1 = ys[idx[0]] + 0.1, ys[idx[-1]] + 0.9
        x = -2.62
        ax.plot([x + 0.06, x, x, x + 0.06], [y0, y0, y1, y1], color="#9a9a9a", lw=0.8, clip_on=False)
        ax.text(x - 0.06, (y0 + y1) / 2, PART_NAME[part], rotation=90, ha="right", va="center",
                fontsize=S.FONT - 1.5, color=S.COL["muted"], clip_on=False)  # fmt: skip
    for j, name in enumerate(cols):
        ax.text(j + 0.5, -0.35, name + (" ○" if name == "Lightning" else ""), ha="center", va="bottom",
                fontsize=S.FONT, weight="bold", color="#222222")  # fmt: skip
    # the key: one swatch per verdict colour, two lines
    key = [("H", "holds"), ("B", "in between or in part"), ("F", "fails"), ("D", "descriptive, no rule"),
           ("N", "not tested or not designed"), ("G", "below the gate")]  # fmt: skip
    kx, ky = 0.01, 1 - 0.78 / h
    for i, (code, text) in enumerate(key):
        cx = kx + (i % 3) * 0.25
        cy = ky - (i // 3) * (0.26 / h)
        fig.patches.append(plt.Rectangle((cx, cy - 0.06 / h), 0.022, 0.15 / h, transform=fig.transFigure,
                                         facecolor=VERDICT_FILL[code], edgecolor="#c8c8c8" if code in "GNX" else "none",
                                         lw=0.6, hatch="////" if code == "G" else None))  # fmt: skip
        fig.text(cx + 0.03, cy + 0.015 / h, text, ha="left", va="center", fontsize=S.FONT - 1, color="#333333")
    fig.text(kx + 0.75, ky + 0.015 / h, "○ Lightning: gate set after\n   its 60-scene pre-check", ha="left",
             va="center", fontsize=S.FONT - 1.5, color=S.COL["muted"])  # fmt: skip
    fig.text(kx + 0.75, ky - 0.26 / h + 0.015 / h, "° gate lowered after the data", ha="left", va="center",
             fontsize=S.FONT - 1.5, color=S.COL["muted"])  # fmt: skip
    return save(fig, "ledger_coverage_map")


# ---- batch 53 (exploration day, Dan 29 Oct 09:30) -------------------------------------------------------------------

LASTCONFLICT = R / "x53_lastconflict" / "x53_lastconflict-20261029T090326Z" / "verdict.json"  # 53.3, four models
# Dan 11:25 (critic_1125): at the answer layer minus 1 / 2 the lens is close to the output and the letter-token dictionary
# decides "through" vs "outside": those cells are "uninformative near the output (dictionary)"; read-peak cells keep labels
UNINFORMATIVE_BELOW_ANSWER = (1, 2)
# Dan 11:55 (decisions_1155): 53.3's digit lookup cells on Muse (L33 of 52) and Lightning (L43 of 52) keep their own
# labels ("the last layers" does not hold there)
LABEL_KEPT_53_3 = {("muse-glimmer-30b", "lookup", 33), ("nemotron-3.5-lightning", "lookup", 43)}


def last_conflict(plt) -> str:
    """53.3, per model (four slots), reader and layer (51.10's read peak, the answer layer minus 2): the switches lost
    without the lens part of the last token's change beyond a random part (bars 0.10 and 0.30), and the rest alone's
    switches as a share of the whole change's (bar 0.7); the rule's label at the right; Lightning hollow. A cell one or
    two layers below the answer layer (and not the read peak) is grey and labelled uninformative near the output
    (dictionary) (Dan, 11:25), its numbers descriptive, except Muse's and Lightning's digit lookups (Dan, 11:55)."""
    v = load(LASTCONFLICT)
    by = {m["target"]: m for m in v["models"]}
    rows = []
    for t in SLOT_MODELS:
        for c in sorted(by[t]["cells"], key=lambda c: (c["reader"] != "lookup", c["layer"])):
            rows.append((t, c))
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 0.3 * len(rows) + 1.9), sharey=True)
    h = fig.get_figheight()
    fig.subplots_adjust(left=0.25, right=0.8, top=1 - 1.25 / h, bottom=1.0 / h, wspace=0.12)
    S.title(fig, "At the read peak no lookup goes through the lens part",
            "The change at the last token; grey: uninformative near the output; ○ hollow: Lightning")  # fmt: skip
    labels = [f"{SHORT[t]}{' ○' if t == LT else ''} {c['reader']}, L{c['layer']}" for t, c in rows]
    for i, (t, c) in enumerate(rows):
        lay = by[t]["layers"]["readers"][c["reader"]]
        uninformative = (c["layer"] != lay["peak"] and lay["answer"] - c["layer"] in UNINFORMATIVE_BELOW_ANSWER
                         and (t, c["reader"], c["layer"]) not in LABEL_KEPT_53_3)
        col = NULL if uninformative else LOOKUP if c["reader"] == "lookup" else INK
        whisker(axes[0], -i, c["excess"], col, hollow=t == LT)
        whisker(axes[1], -i, c["rest_share"], col, hollow=t == LT)
        if i and t != rows[i - 1][0]:
            for ax in axes:
                ax.axhline(-i + 0.5, color="#dddddd", lw=0.8)
        short = {"computes outside the lens at the last token": "outside the lens"}.get(c["text"], c["text"])
        if uninformative:
            short = "uninformative"
        axes[1].text(1.08, -i, short, va="center", fontsize=S.LABEL_PT - 1, color=GREY if uninformative else col,
                     clip_on=False)
        S.record("ledger_last_conflict", t, f"{c['reader']} L{c['layer']}: switches lost without the lens part beyond "
                 "random (last token)", *c["excess"], n=c["n"], source=rel(LASTCONFLICT))  # fmt: skip
        S.record("ledger_last_conflict", t, f"{c['reader']} L{c['layer']}: the rest alone, share of the whole change",
                 *c["rest_share"], n=c["n"], source=rel(LASTCONFLICT))  # fmt: skip
    rows_axis(axes[0], labels)
    zero_band(axes[0], -0.2, 1.0)
    axes[0].axvline(0.10, color="#555555", lw=0.8, ls="--")
    axes[0].axvline(0.30, color="#555555", lw=0.8, ls=":")
    axes[0].set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
    axes[0].set_xlabel("lost without the lens part\nbeyond a random part")
    zero_band(axes[1], 0.0, 1.05)
    axes[1].axvline(0.7, color="#555555", lw=0.8, ls="--")
    axes[1].set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
    axes[1].set_xlabel("the rest alone,\nshare of the whole change")
    note_slot(fig, "ledger_last_conflict")
    return save(fig, "ledger_last_conflict")


# ---- four-slot figures that replace borrowed ones (Dan's figures brief, 29 Oct 10:00) ------------------------------


def four_panels(plt, name: str, title: str, sub: str, rows: dict, absent: dict, xlabel: str, xlim=(-0.05, 1.05),
                bars: tuple = (), height: float | None = None, left: float = 0.37,
                models: tuple = FIVE) -> str:
    """One panel per model slot (9B, 27B, Muse, Lightning, the 122B; Dan 12:50); a model with neither rows nor a label
    in absent gets the grey "not run" slot. rows: model -> [(row label, (v, lo, hi), colour, hollow)];
    absent: model -> its grey label. Row labels (the union, in first-seen order) on the left panel; each (x, style)
    in bars is drawn on every data panel. Every plotted value is recorded for figures/story/data.csv."""
    absent = {**{t: "not run" for t in models if t not in rows}, **absent}
    labels: list[str] = []
    for t in models:
        for lab, *_ in rows.get(t, []):
            if lab not in labels:
                labels.append(lab)
    fig, axes = plt.subplots(1, len(models), figsize=(S.WIDTH, height or 0.42 * len(labels) + 2.1), sharey=True)
    h = fig.get_figheight()
    fig.subplots_adjust(left=left, right=0.985, top=1 - 1.3 / h, bottom=0.75 / h, wspace=0.12)
    S.title(fig, title, sub)
    for ax, t in zip(axes, models, strict=True):
        if t in absent:
            rows_axis(ax, labels)
            grey_panel(name, t, absent[t], ax)
            continue
        # the hollow mark on every hollow panel: Lightning (its gate set after the pre-check) and any model registered
        # below gate for this figure (Dan's figures brief, 10:00: below-gate panels hollow and labelled alike)
        hollow_panel = t == LT or _SLOTS.get(name, {}).get(SHORT[t]) == "below gate"
        ax.set_title(SHORT[t] + (" ○" if hollow_panel else ""), fontsize=title_size(ax), weight="bold", loc="left")
        for lab, v, col, hollow in rows[t]:
            if isinstance(v, str):  # a cell this model does not have (not tested, pending): a grey note in its row
                ax.text(xlim[0] + 0.03, -labels.index(lab), v, color=GREY, va="center", fontsize=S.LABEL_PT - 1)
                continue
            whisker(ax, -labels.index(lab), v, col, hollow=hollow)
            S.record(name, t, lab, *v)
        rows_axis(ax, labels)
        ax.set_xlim(*xlim)
        ax.axvline(0, color="#999999", lw=0.8, zorder=1)
        ax.grid(axis="x", color="#eeeeee")
        ax.set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        for x, ls in bars:
            ax.axvline(x, color="#555555", lw=0.8, ls=ls)
    fig.text(0.68, 0.012, xlabel, ha="center", va="bottom", fontsize=S.LABEL_PT)  # one x label for the row of panels
    # the row labels on the left panel, also when that panel is a grey slot
    axes[0].tick_params(axis="y", labelleft=True)
    axes[0].set_yticks([-i for i in range(len(labels))], labels, fontsize=S.LABEL_PT)
    return save(fig, name)


PROBE = {"qwen3.5-9b": R / "x0_probe" / "qwen35_9b_x0_probe_v4" / "probe-20261024T172340Z" / "probe.json",
         "qwen3.6-27b": R / "x0_probe" / "x0_probe_v4_27b" / "probe-20261024T172424Z" / "probe.json",
         "muse-glimmer-30b": R / "x0_probe" / "muse30b_x0_probe_v4" / "probe-20261026T000115Z" / "probe.json",
         LT: R / "x0_probe" / "nem35l_x52_probe" / "probe-20261029T002432Z" / "probe.json",
         B122: R / "x0_probe" / "qwen35_122b_x0_probe_v4" / "probe-20261024T230718Z" / "probe.json"}  # fmt: skip


def address_probe(plt) -> str:
    """The address probe (x0_probe v4) at each model's L: which locker sentence (locker first; locker after, the
    control), with the layout-only baseline beside, and the answer digit; five models (the 122B, Dan 11:30),
    Lightning hollow."""
    rows = {}
    for t, path in PROBE.items():
        by = {(r["stratum"], r["target"]): r for r in load(path)["rows"] if r["subset"] == "all"}
        hollow = t == LT
        rows[t] = [("locker sentence, locker first", by[("before", "locker sentence")]["probe"], ADDRESS, hollow),
                   ("the same, layout alone", by[("before", "locker sentence")]["layout"], NULL, False),
                   ("locker sentence, locker after", by[("after", "locker sentence")]["probe"], ADDRESS, True),
                   ("answer digit, locker first", by[("before", "answer digit")]["probe"], INK, hollow)]  # fmt: skip
    return four_panels(plt, "ledger_address_probe", "A probe reads the address at the bridge word on all five models",
                       "Held-out probe accuracy at each model's L; grey: the layout alone; chance 0.20 (dotted)",
                       rows, {}, "probe accuracy", xlim=(0, 1.05), bars=((0.2, ":"),), models=FIVE)


CUMUL = {"qwen3.5-9b": R / "x47_cumulative" / "x47_4-20261028T113105Z" / "x47_4.json",
         "muse-glimmer-30b": R / "x47_cumulative" / "x47_4-20261028T113105Z" / "x47_4.json",
         "qwen3.6-27b": R / "x47_cumulative" / "x52_cumulative-20261029T023427Z" / "x47_4.json",
         LT: R / "x47_cumulative" / "x52_cumulative-20261029T044453Z" / "x47_4.json"}  # fmt: skip
CUMUL_BELOW = R / "x47_cumulative" / "x52_cumulative_below-20261029T085952Z" / "x47_4.json"  # Lightning, clean, below gate


def _cumul(path: Path, target: str, design: str) -> dict:
    (m,) = [m for m in load(path)["models"] if m["target"] == target and m["status"] == "tested"]
    return m["cells"][design]["lookup"]


def cumulative(plt) -> str:
    """47.4 on four slots: the lookups the change at L leaves unswitched (locker first) and the lookups the bridge word
    before L carries (locker after), main design; Lightning's clean design below gate beside (hollow)."""
    rows = {}
    for t, path in CUMUL.items():
        c = _cumul(path, t, "main")
        hollow = t == LT
        rows[t] = [("locker first: missed at L", c["locker-first"]["non_switch"], LOOKUP, hollow),
                   ("locker after: carried before L", c["locker-after"]["terms"]["before_L"], LOOKUP, hollow)]
    cb = _cumul(CUMUL_BELOW, LT, "clean")
    rows[LT].append(("the same, clean design", cb["locker-after"]["terms"]["before_L"], LOOKUP, True))
    below_gate("ledger_cumulative", LT)
    return four_panels(plt, "ledger_cumulative", "Lookups the change misses are read at the bridge word before L",
                       "Share of lookups; main design on all four; ○ Lightning's clean design below gate (exploratory)",
                       rows, {}, "share of lookups")


DAS48 = {"qwen3.5-9b": R / "x48_das" / "verdict-20261028T134153Z" / "verdict.json",
         "muse-glimmer-30b": R / "x48_das" / "verdict-20261028T134153Z" / "verdict.json",
         "qwen3.6-27b": R / "x48_das" / "x52_das-20261029T040955Z" / "verdict.json"}  # fmt: skip


def das48(plt) -> str:
    """48.1 on four slots: each reader's learned subspace at the chosen size k, its held-out own interchange accuracy
    (whiskers 95%), the rule's 0.7 dashed; Lightning grey (dropped: DAS port)."""
    rows = {}
    for t, path in DAS48.items():
        (m,) = [m for m in load(path)["models"] if m["target"] == t]
        rows[t] = []
        for key, word, col in (("PP", "lookup", LOOKUP), ("PM", "recall", INK)):
            r = m["readers"][key]
            rows[t].append((f"{word}'s subspace", r["test"]["own_iia"][str(r["k"])], col, False))
    return four_panels(plt, "ledger_das48", "Neither reader has a learned subspace of its own",
                       "Held-out switches carried by each reader's learned subspace at its chosen size; dashed: 0.7",
                       rows, {LT: "dropped:\nDAS port"}, "switches carried", bars=((0.7, "--"),))


REPORT = R / "x47_report" / "x47_10-20261028T113109Z" / "x47_10.json"


def report47(plt) -> str:
    """47.10 on four slots: the 27B, question last: the lens top five holding the right ordinal under the report
    prompt (rule's 0.4), the report's switches lost without the lens part and without the address, beyond random; the
    other three grey with the gate that stopped them."""
    (m,) = [m for m in load(REPORT)["models"] if m["target"] == "qwen3.6-27b"]
    o = m["orders"]["last"]
    rows = {"qwen3.6-27b": [("lens top 5: the right ordinal", o["lens"]["report"]["top5_ordinal"], ADDRESS, False),
                            ("lost without the lens part", o["readers"]["report"]["jpp"]["excess"], INK, False),
                            ("lost without the address", o["readers"]["report"]["alf"]["excess"], ADDRESS, False)]}
    absent = {"qwen3.5-9b": "not tested:\ngate (report\n0.568 < 0.80)", "muse-glimmer-30b": "not tested:\ngate (report\n0.498 < 0.80)",
              LT: "not tested:\ngate (report\n0.488 < 0.80)"}  # fmt: skip
    return four_panels(plt, "ledger_report47", "Asked for the position, the 27B's lens still does not show it",
                       "Question last; whiskers 95%; dashed: the rule's 0.4; the other three missed the report gate",
                       rows, absent, "share", bars=((0.4, "--"),))


SUBSET = R / "x53_subset27b" / "x53_subset27b-20261029T085435Z" / "x53_subset27b.json"


def subset27b(plt) -> str:
    """53.5 on four slots: on each model's position-route scenes, position answers without the address, without a
    random part of its share, with the address alone, with a random part alone, and the swap at dose 2 (C2 scenes);
    the rule's bars 0.10 and 0.25 dotted / dashed; Muse and Lightning grey (not designed)."""
    v = load(SUBSET)
    rows = {}
    for t in ("qwen3.5-9b", "qwen3.6-27b"):
        m = v["models"][t]
        sh = m["subset"]["pooled"]["share"]
        rows[t] = [("without the address", sh["no_alf"], ADDRESS, False),
                   ("without a random part", sh["no_alf_rand"], NULL, False),
                   ("the address alone", sh["keep_alf"], ADDRESS, False),
                   ("a random part alone", sh["keep_alf_rand"], NULL, False),
                   ("the swap at dose 2: to the target", m["swap"]["subset"]["swap"]["target"], ADDRESS, False)]
    absent = {"muse-glimmer-30b": "not designed\n(9B / 27B only)", LT: "not designed\n(9B / 27B only)"}
    return four_panels(plt, "ledger_subset27b", "On its position scenes the 27B's address brings fewer answers back",
                       "Position answers on each model's position-route scenes; dotted / dashed: the rule's 0.10 / 0.25",
                       rows, absent, "share of lookups", bars=((0.10, ":"), (0.25, "--")))


IDADDR53 = R / "x53_identity_address" / "x53_identity_address-20261029T105132Z" / "verdict.json"  # joint, four models
IDADDR = {t: IDADDR53 for t in SLOT_MODELS}


def identity_address(plt) -> str:
    """53.6 on four slots: the recall under the lens part toward item B plus the address swap toward item C's slot:
    the shares answering B's, C's and the original answer, with each part alone beside; Lightning hollow."""
    rows = {}
    for t, path in IDADDR.items():
        if not path.exists():
            continue
        (m,) = [m for m in load(path)["models"] if m["target"] == t]
        c = m["cells"]["PM"]
        hollow = t == LT
        rows[t] = [("both: B's answer", c["both"]["B"], JPP, hollow),
                   ("both: C's answer", c["both"]["C"], ADDRESS, hollow),
                   ("both: the original", c["both"]["original"], NULL, hollow),
                   ("lens part alone: B's", c["lens"]["B"], JPP, hollow),
                   ("address alone: C's", c["addr"]["C"], ADDRESS, hollow)]
    absent = {}
    for t in IDADDR:
        if t not in rows:
            absent[t] = "running"
    return four_panels(plt, "ledger_identity_address", "Every recall follows both; on the 27B and Muse it mostly stays put",
                       "The recall's answers; teal: item B (the lens part), orange: item C (the address); whiskers 95%",
                       rows, absent, "share of recalls")


ATTNBLOCK = R / "x53_attnblock" / "x53_attnblock-20261029T091303Z" / "verdict.json"
# the follow-up with Dan's 11:25 control (one placement; the first run, x53_attnspan-20261029T102727Z, superseded)
ATTNSPAN = R / "x53_attnblock" / "x53_attnspan_c-20261029T121412Z" / "verdict.json"  # + survivors (Dan 13:15)


def attnblock(plt) -> str:
    """53.4 on four slots: Lightning, the share of the whole change's lookup switches cut by blocking the bridge word in
    attention block 19, 26, both, every attention block after L, and the control (both blocks, another token); the
    recall beside; the rule's 0.6, 0.3 and 0.15 bars; the other three grey (a Lightning test). The follow-up beside:
    the span from the bridge word to the scene's end, and Dan's 11:25 control span (83 scenes where it fits)."""
    v, sp = load(ATTNBLOCK), load(ATTNSPAN)
    arms = (("b19", "(i) block 19"), ("b26", "(ii) block 26"), ("both", "(iii) blocks 19, 26"),
            ("after", "(iv) all after L"), ("control", "(v) control"))
    rows = {LT: []}
    for reader, col in (("lookup", LOOKUP), ("recall", INK)):
        r = v["readers"][reader]
        for k, lab in arms:
            rows[LT].append((f"{reader}: {lab}", [r["cut"][k], *r["cut_ci"][k]], col, True))
        q = sp["readers"][reader]
        for k, lab in (("span", "follow-up: span"), ("span_ctrl", "follow-up: control span")):
            rows[LT].append((f"{reader}: {lab}", [q["cut"][k], *q["cut_ci"][k]], col, True))
    absent = {t: "not applicable\n(Lightning test)" for t in (*SLOT_MODELS[:3], B122)}
    return four_panels(plt, "ledger_attnblock", "Two attention blocks carry a third of Lightning's lookup switch",
                       "Share of the whole change's switches cut by blocking the bridge word; dashed: 0.6, dotted: 0.3",
                       rows, absent, "switches cut", xlim=(-0.1, 1.05), bars=((0.6, "--"), (0.3, ":")))


JSUITE = R / "x51_answer" / "x53_jsuite-20261029T095443Z" / "verdict.json"  # 53.1b, both models (combined)
JSUITE_NOTES = {("z2p", "qwen3.5-9b"): "not tested\n(gate 0.757\n< 0.80)", ("z2p", "qwen3.6-27b"): "pending\n(rerun)"}


def jsuite(plt) -> str:
    """53.1b on four slots: per model and cell of Zach's made-up-fact passages (PP the lookup and PM the recall on the
    passages that name the bridge; MP the lookup and MM the recall on the passages that describe it), 51.12's arms:
    switches lost without the lens part beyond random, and without the answer directions only beyond random; a cell not
    tested or pending as a grey note; Muse and Lightning grey."""
    v = load(JSUITE)
    by = {(m["set"], m["target"]): m for m in v["models"] if m["status"] == "tested"}
    cells = (("z1p", "lookup", "PP lookup", LOOKUP), ("z1p", "recall", "PM recall", INK),
             ("z2p", "lookup", "MP lookup", LOOKUP), ("z2p", "recall", "MM recall", INK))
    rows = {}
    for t in ("qwen3.5-9b", "qwen3.6-27b"):
        rows[t] = []
        for st, rd, word, col in cells:
            m = by.get((st, t))
            for arm, what in (("1", "without the lens part"), ("3", "answer directions only")):
                lab = f"{word}: {what}"
                if m is None:
                    rows[t].append((lab, JSUITE_NOTES[(st, t)] if arm == "1" else "", col, False))
                else:
                    rows[t].append((lab, m["readers"][rd]["extra"][arm], col, False))
    absent = {"muse-glimmer-30b": "not designed\n(9B / 27B only)", LT: "not designed\n(9B / 27B only)"}
    return four_panels(plt, "ledger_jsuite", "Named: both recalls mixed; described: the 27B's reads as the answer",
                       "Lost beyond random; P- named bridge, M- described; -P lookup, -M recall; whiskers 95%",
                       rows, absent, "lost beyond random", xlim=(-0.3, 1.0))


WORDS53 = R / "x53_lastconflict" / "x53_lastconflict_words-20261029T100850Z" / "verdict.json"  # 53.3b, joint verdict


def _words53_kinds(layer: int, answer: int, peak: int) -> list[str]:
    """The rows a cell belongs to: its distance below the answer layer (1-3) and/or 51.10's read peak (the 27B's
    lookup read peak L60 is also its answer layer minus 3); a read-peak cell keeps its label (Dan, 11:25), so it never
    sits in an uninformative row (the 27B's locker-scene L60 is its read peak and its answer - 1)."""
    kinds = [f"answer - {answer - layer}"] if 1 <= answer - layer <= 3 else []
    if layer == peak:
        kinds = [k for k in kinds if answer - layer not in UNINFORMATIVE_BELOW_ANSWER] + ["read peak"]
    return kinds


def _words53_row(prefix: str, kind: str) -> tuple[str, bool]:
    """A row label and whether the row is uninformative near the output (answer - 1 / - 2; Dan, 11:25)."""
    un = kind in [f"answer - {k}" for k in UNINFORMATIVE_BELOW_ANSWER]
    return f"{prefix}, {kind}" + (": uninformative" if un else ""), un


def last_conflict_words(plt) -> str:
    """53.3b on four slots (the joint verdict): the last-token conflict test on Zach's word answers, per reader at its
    answer layer minus 1, 2, 3 and 51.10's read peak, switches lost without the lens part beyond a random part; the
    check on our locker scenes at the lookup's answer layer minus 1 and 3; a cell under 53.3's validity bar as a grey
    note; a model below its gate hollow and labelled; the answer - 1 / - 2 rows grey and labelled uninformative near
    the output (Dan, 11:25), their numbers descriptive."""
    v = load(WORDS53)
    rows = {}
    for t in SLOT_MODELS:
        (m,) = [m for m in v["models"] if m["target"] == t]
        below = bool(m.get("below_gate"))
        if below:
            below_gate("ledger_last_conflict_words", t)
        rows[t] = []
        for rd in ("lookup", "recall"):
            lay = m["layers"]["readers"][rd]
            cells = {c["layer"]: c for c in m["cells"] if c["reader"] == rd}
            for k in ("answer - 1", "answer - 2", "answer - 3", "read peak"):
                for c in (c for c in cells.values() if k in _words53_kinds(c["layer"], lay["answer"], lay["peak"])):
                    lab, un = _words53_row(f"words, {rd}", k)
                    col = NULL if un else LOOKUP if rd == "lookup" else INK
                    rows[t].append((lab, c["excess"] if c["x0_valid"] else f"L{c['layer']}: invalid", col, below))
        (chk,) = [c for c in v["checks"] if c["target"] == t]
        lay = chk["layers"]["readers"]["lookup"]
        for k in ("answer - 1", "answer - 3", "read peak"):
            for c in (c for c in chk["cells"] if k in _words53_kinds(c["layer"], lay["answer"], lay["peak"])):
                lab, un = _words53_row("locker, lookup", k)
                rows[t].append((lab, c["excess"] if c["x0_valid"] else f"L{c['layer']}: invalid",
                                NULL if un else LOOKUP, below))
    return four_panels(plt, "ledger_last_conflict_words", "Near the output the test is uninformative; read peaks differ",
                       "Lost without the lens part beyond random, last token; grey: uninformative; ○ below gate",
                       rows, {}, "lost beyond random", xlim=(-0.2, 1.05), bars=((0.10, "--"), (0.30, ":")), left=0.41)


BINDID = R / "x53_bindid" / "x53_bindid-20261029T122650Z" / "verdict.json"  # 53.8: the 9B, the 27B and Muse


def bindid(plt) -> str:
    """53.8 on five slots: lookups sent to X's locker at 2x under X's vector, Y's version and a random vector of the
    same norm, the pre-specified (uncentered) arm and the centered arm beside (Dan 12:10); the 27B and Muse grey
    (running), Lightning grey (not designed), the 122B grey (not run)."""
    rows = {}
    for m in load(BINDID)["models"]:
        rows[m["target"]] = []
        for var, lab in (("uncentered", "pre-specified"), ("centered", "centered")):
            cell = m["variants"][var]["cells"]["2"]
            for k, arm, col in (("X", "X's vector", ADDRESS), ("Y", "Y's version", JPP), ("R", "random", NULL)):
                rows[m["target"]].append((f"{lab}: {arm}", cell[k], col, False))
    absent = {LT: "not designed"}
    return four_panels(plt, "ledger_bindid", "Centered, the code moves lookups beyond random; raw, little or none",
                       "Lookups sent to X's locker at 2x; orange: X's vector, teal: Y's version, grey: random",
                       rows, absent, "share of lookups")


CODE_PROBE = R / "x0_probe" / "x53_7_probe-20261029T115640Z" / "verdict.json"  # 53.7 probe (the 9B; the 27B to come)
CODE_ROUTES = R / "x6_routes" / "x53_7_routes-20261029T122509Z" / "verdict.json"  # 53.7 routes, code + tool, 9B + 27B


def code_tool(plt) -> str:
    """53.7 (adapted design: lookup-only gate) on five slots: the routes test in code, condition C2, position answers
    under the whole change, without the address, without a random part of its share and with the address alone; the
    probe (which locker sentence, locker first) in code and tool output, a cell not tested or to come as a grey note;
    Muse and Lightning grey (not designed), the 122B grey (not run)."""
    rows: dict[str, list] = {}
    arms = (("C2|whole", "position, whole change", ADDRESS), ("C2|no_alf", "position without the address", ADDRESS),
            ("C2|no_alf_rand", "the same, random part out", NULL),
            ("C2|keep_alf", "position, the address alone", ADDRESS))  # fmt: skip
    runs = {(run["model"], run["format"]): run for run in load(CODE_ROUTES)["runs"]}
    for (model, fmt), run in sorted(runs.items(), key=lambda kv: (kv[0][0], kv[0][1] != "code")):
        rows.setdefault(model, [])
        for key, lab, col in arms:
            rows[model].append((f"{fmt}, routes: {lab}", run["cells"][key]["share"]["position"], col, False))
    probes = {(run["model"], run["format"]): run for run in load(CODE_PROBE)["runs"]}
    for t in ("qwen3.5-9b", "qwen3.6-27b"):
        for fmt in ("code", "tool"):
            lab = f"{fmt}, probe: locker sentence, locker first"
            run = probes.get((t, fmt))
            if run is None:
                rows.setdefault(t, []).append((lab, "to come", ADDRESS, False))
            elif run["status"] != "tested":
                gate = re.search(r"gate ([0-9.]+)", run["status"]).group(1)
                rows.setdefault(t, []).append((lab, f"○ not tested\n(gate {gate})", ADDRESS, True))
            else:
                r = next(x for x in run["rows"] if x["subset"] == "all" and x["stratum"] == "before"
                         and x["target"] == "locker sentence")  # fmt: skip
                rows.setdefault(t, []).append((lab, r["probe"], ADDRESS, bool(run.get("hollow"))))
    absent = {"muse-glimmer-30b": "not designed", LT: "not designed"}
    return four_panels(plt, "ledger_code_tool", "In code and tool output the address carries the position route",
                       "Another item moved: position answers by arm and format; probe: which locker sentence, first",
                       rows, absent, "share", left=0.4)


TWO_SOURCES = R / "x47_source" / "x47_15-20261028T142722Z" / "x47_15.json"  # 47.15, one question, two sources


def two_sources(plt) -> str:
    """47.15 on five slots: per instruction (from the text, from memory), the fact placed after, the switches lost beyond
    a random part without the lens part and without the address and identity parts (U + I); the rule's 0.10 / 0.30
    bars; the models whose gate failed grey."""
    rows = {}
    for m in load(TWO_SOURCES)["models"]:
        if m["status"] != "tested":
            continue
        conds = m["placements"]["after"]["conditions"]
        rows[m["target"]] = [(f"{lab}: without {part}", conds[k]["extra"][key], col, False)
                             for k, lab in (("text", "from the text"), ("memory", "from memory"))
                             for key, part, col in (("jpp", "the lens part", JPP), ("ui", "U + I", ADDRESS))]  # fmt: skip
    absent = {"qwen3.5-9b": "not tested\n(gate)", "muse-glimmer-30b": "not tested\n(gate)", LT: "not tested\n(gate)"}
    return four_panels(plt, "ledger_two_sources", "On the 27B neither instruction makes the part follow the source",
                       "Fact after: switches lost beyond a random part; dotted / dashed: the rule's 0.10 / 0.30",
                       rows, absent, "lost beyond random", xlim=(-0.2, 1.05), bars=((0.10, ":"), (0.30, "--")))


SLOT1 = {"qwen3.5-9b": R / "x49_report" / "x49_6-20261028T154511Z" / "x49_6.json",
         "qwen3.6-27b": R / "x49_report" / "x49_6-20261028T154511Z" / "x49_6.json",
         LT: R / "x49_report" / "x52_report49-20261029T082508Z" / "x49_6.json"}  # fmt: skip


def report_slot1(plt) -> str:
    """49.6 on four slots: question last, the share of scenes whose asked item sits in slot 1 that the report reads
    right, under 47.10's report wording and the two new wordings (position, sentence); the rule's 0.2 dashed; Muse grey
    (not designed); Lightning hollow (a coverage run with the 9B / 27B design)."""
    rows = {}
    for t, path in SLOT1.items():
        (m,) = [m for m in load(path)["models"] if m["target"] == t and m["status"] == "tested"]
        cells = m["orders"]["last"]["cells"]
        hollow = t == LT
        rows[t] = [("the earlier report wording", m["reference"]["report"]["1"]["read"], NULL, hollow),
                   ("position wording (a digit)", cells["position"]["1"]["read"], ADDRESS, hollow),
                   ("sentence wording (a word)", cells["sentence"]["1"]["read"], INK, hollow)]
    return four_panels(plt, "ledger_report_slot1", "Reworded, the report reads slot 1 on every model tested",
                       "Question last: scenes whose asked item is in slot 1, reported right; dashed: the rule's 0.2",
                       rows, {"muse-glimmer-30b": "not designed\n(9B / 27B only)"}, "share reported right",
                       bars=((0.2, "--"),))


TWOBYTWO = R / "x53_2x2" / "x53_2x2-20261029T113335Z" / "verdict.json"  # 53.1, the five-model verdict
# box verdicts read where the combined verdict lacks a model (none since the five-model verdict)
TWOBYTWO_INTERIM: tuple[Path, ...] = ()
TWOBYTWO_CELLS = (("qa_num", "Q after, number"), ("qb_num", "Q before, number"), ("qa_word", "Q after, word"),
                  ("qb_word", "Q before, word"))


def twobytwo(plt) -> str:
    """53.1 on four slots: per cell of the 2x2 (question after / before the scene x number / word answer), the
    recall's switches lost without the lens part beyond random (arm 1) and its share kept with the answer directions
    kept (arm 2 over arm 1), and the conflict test's lookup beside (dashed: the cross-check's 0.10); the lookup's
    paired difference, question before minus after (Dan 11:25); a cell not tested as a grey note with its own gate;
    Lightning hollow (its gate set after the pre-check); a model still running grey; the 122B as a fifth slot."""
    v = {m["target"]: m for m in _twobytwo_models(TWOBYTWO)}
    for m in (m for p in TWOBYTWO_INTERIM for m in _twobytwo_models(p)):
        if m.get("cells") and not v.get(m["target"], {}).get("cells"):
            v[m["target"]] = m
    rows, absent = {}, {}
    for t in FIVE:
        if v.get(t, {}).get("cells"):
            rows[t] = _twobytwo_rows(v[t], hollow=t == LT)
        else:
            absent[t] = "running" if v.get(t, {}).get("status") == "pending" else "not run"
    return four_panels(plt, "ledger_twobytwo", "With a number answer the recall follows the entity",
                       "Lost: without the lens part, beyond random; kept: share kept with the answer directions kept",
                       rows, absent, "share", xlim=(-0.2, 1.05), bars=((0.10, "--"),))


def _twobytwo_models(path: Path) -> list[dict]:
    """A 53.1 verdict's per-model entries: a list until 11:18 UTC, then {"models": [...], "across_models": ...}."""
    data = load(path)
    return data["models"] if isinstance(data, dict) else data


def _twobytwo_note(c: dict) -> str:
    """A cell without numbers: stopped (Dan 11:10), the word relation's 9B accuracy, or its own gate."""
    status = c.get("status") or ""
    if status.startswith("stopped"):
        return "not run\n(stopped,\nDan 11:10)"
    if "relation" in status:
        return "not tested\n(relation\n0.382 < 0.80)"
    return f"not tested\n(gate {c['gate']['org_read_accuracy']['PM']:.3f}\n< 0.80)"


def _twobytwo_rows(m: dict, hollow: bool = False) -> list:
    out = []
    for key, word in TWOBYTWO_CELLS:
        c = m["cells"].get(key, {})
        labs = (f"{word}: recall lost", f"{word}: recall kept", f"{word}: lookup lost")
        if c.get("status") == "tested":
            r = c["readers"]["recall"]
            out += [(labs[0], r["extra"]["1"], INK, hollow), (labs[1], r["share2"], INK, hollow),
                    (labs[2], c["lookup_extra"], LOOKUP, hollow)]
        else:
            out += [(labs[0], _twobytwo_note(c), INK, hollow), (labs[1], "", INK, hollow),
                    (labs[2], "", LOOKUP, hollow)]
    p = m.get("paired") or {}
    out.append(("lookup, Q before minus after", p["diff"] if p.get("diff") else "can't tell\n(a cell\nnot tested)",
                LOOKUP, hollow))
    return out


FIGURES = (coverage_map, answer_control, address_shape, learned, heads, full_carrier, last_token_address, zach_named,
           zach_routes, clean_reruns, lightning_layers, answer_map, routes, six_lockers, atoms, read_window, described,
           address_swap, order_split, attention, distance, gain, agnostic, value_formats, pooled_probe,
           last_conflict, address_probe, cumulative, das48, report47, subset27b, identity_address, attnblock,
           jsuite, last_conflict_words, report_slot1, twobytwo, bindid, code_tool, two_sources)  # fmt: skip


def build_all(plt) -> list[str]:
    return [f(plt) for f in FIGURES]


if __name__ == "__main__":
    import sys

    plt = S.setup()
    names = sys.argv[1:]
    print([f(plt) for f in FIGURES if not names or f.__name__ in names])
