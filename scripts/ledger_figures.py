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
from pathlib import Path

from scripts import story_style as S

OUT = S.REPO / "figures" / "ledger"
R = S.REPO / "results"
INK, LOOKUP, JPP, ADDRESS, NULL = (S.MARK_COL[k] for k in ("recall", "lookup", "jpp", "address", "null"))
MODEL3 = (("qwen3.5-9b", "Qwen3.5-9B"), ("qwen3.6-27b", "Qwen3.6-27B"), ("muse-glimmer-30b", "Muse Glimmer 30B"))
SHORT = {"qwen3.5-9b": "9B", "qwen3.6-27b": "27B", "muse-glimmer-30b": "Muse", "nemotron-3.5-lightning": "Lightning"}

ANSWER = R / "x51_answer" / "x51_12-20261028T201842Z" / "verdict.json"
ANSWER_LIGHTNING = R / "x51_answer" / "x52_answer-20261029T002056Z" / "verdict.json"
ADDR = R / "x51_addr" / "verdict-20261028T215138Z" / "verdict.json"
DAS = R / "x51_das" / "verdict-20261028T194630Z" / "verdict.json"
HEADS = R / "x51_heads" / "x51_2-20261028T190358Z" / "verdict.json"
CARRIER = R / "x51_carrier" / "x51_7-20261028T171646Z" / "verdict.json"
TRAVEL = R / "x51_travel" / "x51_4-20261028T173333Z" / "verdict.json"
Z1 = R / "x50_zach" / "z1-20261028T161649Z" / "z1.json"
Z3 = R / "x50_zach" / "z3-20261028T163053Z" / "z3.json"
CLEAN = R / "checks" / "clean49_9b.json"
LAYER = R / "x51_lightning" / "nem35l_x52_layer_r2" / "layer.json"
CONFLICT = R / "x0_necessity" / "nem35l_x52_conflict" / "verdict-20261029T001612Z" / "verdict.json"
MAIN = {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse"}  # docs/x0_numbers.json's suffixes


def rel(p: Path) -> str:
    return str(p.relative_to(S.REPO))


def load(p: Path) -> dict:
    return json.loads(p.read_text())


def save(fig, name: str) -> str:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", facecolor="white")
    fig.savefig(OUT / f"{name}.png", dpi=200, facecolor="white")
    S.plt.close(fig)
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
    order = ("qwen3.5-9b", "qwen3.6-27b", "muse-glimmer-30b", "nemotron-3.5-lightning")
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
    models = [m for m in v["models"] if m.get("part1") and m["part1"].get("S")]
    fig, axes = plt.subplots(2, len(models), figsize=(S.WIDTH, 6.6))
    fig.subplots_adjust(left=0.09, right=0.97, top=0.84, bottom=0.08, hspace=0.55, wspace=0.18)
    S.title(fig, "Muse's code grows with the lockers, the 9B's does not; midpoints fail",
            "Top: learned code's accuracy by size k, per number of lockers; bottom: swaps to the midpoint slot")  # fmt: skip
    shades = {"3": "#f5c48a", "4": "#eaa04f", "6": "#c9731a", "8": "#8a4a0b"}
    for j, m in enumerate(models):
        ax = axes[0, j]
        name = dict(MODEL3)[m["target"]]
        ax.set_title(name, fontsize=12, weight="bold", loc="left")
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
        ax.set_xticks([0, 1], [b[0] for b in bars])
        ax.set_ylim(0, 1.0)
        if j == 0:
            ax.set_ylabel("share of lookups")
            ax.text(-0.36, 0.86, "dark: the midpoint swap, on the midpoint\nlight: the full swap, on its target",
                    fontsize=S.LABEL_PT, color=S.COL["muted"])  # fmt: skip
    return save(fig, "ledger_address_shape")


# ---- learned subspaces (51.3) ---------------------------------------------------------------------------------------


def learned(plt) -> str:
    """Per model, the learned subspace's own interchange accuracy on test pairs against its size k, for the recall and
    the lookup; a random subspace of the same size dashed."""
    v = load(DAS)
    by = {m["target"]: m for m in v["models"]}
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, 3.6), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.93, top=0.72, bottom=0.17, wspace=0.22)
    S.title(fig, "Learned subspaces carry each reader's item switch; random ones none",
            "Switches carried by a learned subspace of size k on held-out entities; dashed: random subspace")  # fmt: skip
    for ax, (t, name) in zip(axes, MODEL3, strict=True):
        ax.set_title(name, fontsize=12, weight="bold", loc="left")
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
        ax.set_xticks([4, 16, 64, 128], ["4", "16", "64", "128"])
        ax.set_xlim(3, 220)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel("subspace size k")
        S.end_labels(ax, 128, items, pad=8)
    axes[0].set_ylabel("switches carried")
    return save(fig, "ledger_learned")


# ---- joint head ablation (51.2) -------------------------------------------------------------------------------------


def heads(plt) -> str:
    """Per model, the share of the address swap's switch cut by mean-ablating the top 1, 3, 5, 10 heads and every head
    of the best layer at the last token; the mean of five random head sets of the same size beside (grey)."""
    v = load(HEADS)
    by = {r["target"]: r for r in v["results"]}
    sets = ("top1", "top3", "top5", "top10", "best_layer")
    names = ("top 1", "top 3", "top 5", "top 10", "best layer")
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, 3.5), sharey=True)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.72, bottom=0.2, wspace=0.12)
    S.title(fig, "No small set of heads carries the swapped address",
            "Share of the swap's switch cut by ablating heads at the last token; grey: random heads, same size")  # fmt: skip
    for ax, (t, name) in zip(axes, MODEL3, strict=True):
        ax.set_title(name, fontsize=12, weight="bold", loc="left")
        site = by[t]["sites"]["last"]
        for i, s in enumerate(sets):
            c = site["cells"][s]["cut"]
            ax.plot([i, i], [c[1], c[2]], color=ADDRESS, lw=1.6)
            ax.plot([i], [c[0]], "o", color=ADDRESS, ms=6.5)
            rnd = site["random"][s]["cut_mean"]
            ax.plot([i + 0.25], [rnd], "o", color=NULL, ms=5)
            S.record("ledger_heads", t, f"last token, {names[i]}: share of the swap's switch cut", *c,
                     n=site["cells"][s]["n"], source=rel(HEADS))  # fmt: skip
            S.record("ledger_heads", t, f"last token, {names[i]}: random sets' mean cut", round(rnd, 4),
                     source=rel(HEADS))  # fmt: skip
        ax.axhline(0, color="#999999", lw=0.8)
        ax.axhline(0.5, color="#555555", lw=0.9, ls=":")
        ax.set_xticks(range(len(sets)), names, rotation=35, ha="right")
        ax.set_ylim(-0.45, 0.6)
    axes[0].set_ylabel("share of the switch cut")
    axes[0].text(4.4, 0.52, "rule's bar 0.5", fontsize=S.LABEL_PT, color=S.COL["muted"], ha="right")
    return save(fig, "ledger_heads")


# ---- the full carrier (51.7) ----------------------------------------------------------------------------------------


def full_carrier(plt) -> str:
    """Per model (9B, 27B), lookups and recalls lost without the lens part beyond a random part, fact first and fact
    after, the change at one layer (hollow) and at every layer up to L (filled)."""
    v = load(CARRIER)
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 3.9), sharey=True)
    fig.subplots_adjust(left=0.25, right=0.98, top=0.72, bottom=0.15, wspace=0.1)
    S.title(fig, "Over every layer up to L, fact-after lookups follow the lens part",
            "Switches lost without the lens part, beyond a random part; hollow: one layer, filled: every layer to L")  # fmt: skip
    labels = ["fact first", "fact after"]
    for ax, m in zip(axes, v["models"], strict=True):
        ax.set_title(dict(MODEL3)[m["target"]], fontsize=12, weight="bold", loc="left")
        for i, g in enumerate(("fact-first", "fact-after")):
            grp = m["groups"][g]
            for carrier, dy, hollow in (("one", 0.18, True), ("before", 0.0, False)):
                for reader, col, ddy in (("lookup", LOOKUP, 0.0), ("recall", INK, -0.32)):
                    e = grp[carrier][reader]["excess"]
                    if grp[carrier][reader]["valid"]:
                        whisker(ax, -i + dy + ddy, e, col, hollow=hollow)
                    else:  # under 30 switches under the whole change: left out (the README figures' convention)
                        ax.text(0.12, -i + dy + ddy, "one layer: under 30 switches", color=col, va="center",
                                fontsize=S.LABEL_PT - 1)  # fmt: skip
                    S.record("ledger_full_carrier", m["target"], f"{g}, {reader}, "
                             f"{'one layer' if carrier == 'one' else 'every layer to L'}: switches lost beyond random",
                             *e, n=grp[carrier][reader]["n"], source=rel(CARRIER))  # fmt: skip
        rows_axis(ax, labels)
        ax.set_ylim(-1.6, 0.5)
        zero_band(ax, -0.2, 1.0)
        ax.set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        ax.axvspan(-0.2, 0.10, color=S.COL["band"], lw=0, zorder=0)
        ax.set_xlabel("switches lost beyond random")
    axes[1].text(0.62, 0.32, "lookup", color=LOOKUP, fontsize=S.LABEL_PT)
    axes[1].text(0.62, -0.18, "recall", color=INK, fontsize=S.LABEL_PT)
    return save(fig, "ledger_full_carrier")


# ---- the address at the last token (51.4) ---------------------------------------------------------------------------


def last_token_address(plt) -> str:
    """Per model, the slot probe's held-out accuracy at the last token by layer (the majority baseline dashed), L and
    L + 4 marked, and the bridge-fit swap's share sent to the target at L + 4 (dose 2) as text."""
    v = load(TRAVEL)
    by = {m["target"]: m for m in v["models"]}
    fig, axes = plt.subplots(1, 3, figsize=(S.WIDTH, 3.6), sharey=True)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.72, bottom=0.17, wspace=0.12)
    S.title(fig, "The slot is readable at the last token; the code works there on Muse",
            "Slot probe's accuracy at the last token by layer; dashed: majority slot; text: the swap at L+4")  # fmt: skip
    for ax, (t, name) in zip(axes, MODEL3, strict=True):
        m = by[t]
        ax.set_title(name, fontsize=12, weight="bold", loc="left")
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
                 *swap["target"], n=swap["n"], source=rel(TRAVEL))  # fmt: skip
        for la, a in zip(layers, acc, strict=True):
            S.record("ledger_last_token_address", t, f"slot probe at the last token, layer {la}", *a,
                     n=m["probe"][str(la)]["n"], source=rel(TRAVEL))  # fmt: skip
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("layer")
    axes[0].set_ylabel("probe accuracy")
    return save(fig, "ledger_last_token_address")


# ---- Zach's named passages (Z1) beside our main test ----------------------------------------------------------------


def zach_named(plt) -> str:
    """Per model, each reader's switches lost without the lens part beyond a random part: our main test (X0's numbers)
    and Zach's named-bridge passages (Z1, at L)."""
    numbers = S.numbers()
    v = load(Z1)
    by = {m["target"]: m for m in v["models"]}
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 3.6), sharey=True)
    fig.subplots_adjust(left=0.2, right=0.98, top=0.72, bottom=0.16, wspace=0.1)
    S.title(fig, "On Zach's named passages the lookup follows the lens part too",
            "Lost beyond a random part; hollow: our main test, filled: his passages; grey: 0.10 bar")  # fmt: skip
    for ax, (reader, col, key) in zip(axes, (("lookup", LOOKUP, "lk"), ("recall", INK, "rc")), strict=True):
        ax.set_title(reader, fontsize=12, weight="bold", loc="left", color=col)
        for i, (t, _) in enumerate(MODEL3):
            ours = S.parse(numbers[f"{key}_excess_{MAIN[t]}"])
            lr = by[t]["layer_results"]
            cell = lr[str(by[t]["layers"][0]) if "layers" in by[t] else next(iter(lr))][reader]
            his = cell["excess"]
            whisker(ax, -i + 0.15, ours, col, hollow=True)
            if cell["valid"]:
                whisker(ax, -i - 0.15, his, col)
            else:  # under 30 switches under the whole change: left out (the README figures' convention)
                ax.text(0.2, -i - 0.15, "his passages: under 30 switches", color=col, va="center",
                        fontsize=S.LABEL_PT - 1)  # fmt: skip
            S.record("ledger_zach_named", t, f"Zach's named passages, {reader}: switches lost beyond random", *his,
                     source=rel(Z1))  # fmt: skip
        rows_axis(ax, [SHORT[t] for t, _ in MODEL3])
        zero_band(ax, -0.25, 1.0)
        ax.axvspan(-0.25, 0.10, color=S.COL["band"], lw=0, zorder=0)
        ax.set_xlabel("switches lost beyond random")
    return save(fig, "ledger_zach_named")


# ---- routes on Zach's passages (Z3) ---------------------------------------------------------------------------------


def zach_routes(plt) -> str:
    """The lookup's answer under the whole change on Zach's scattered-fact passages: identity, position, value, the
    original answer, stacked, per model and layer."""
    v = load(Z3)
    rows = []
    for m in v["models"]:
        for la, lr in m["layer_results"].items():
            rows.append((f"{SHORT[m['target']]} L{la}", lr["shares"]["C2"]["whole"], lr["n"], m["target"], la))
    fig, ax = plt.subplots(figsize=(S.WIDTH, 0.55 * len(rows) + 1.7))
    fig.subplots_adjust(left=0.16, right=0.88, top=1 - 1.15 / fig.get_figheight(), bottom=0.65 / fig.get_figheight())
    S.title(fig, "On Zach's passages the lookup rarely takes the position route",
            "The lookup's answer under the whole change, share of passages")  # fmt: skip
    parts = (("identity", S.COL["identity"]), ("position", S.COL["position"]), ("value", S.COL["value"]),
             ("original", S.COL["original"]))  # fmt: skip
    for i, (_, sh, n, t, la) in enumerate(rows):
        left = 0.0
        for p, col in parts:
            w = sh[p][0]
            ax.barh(-i, w, left=left, color=col, height=0.6, edgecolor="white", lw=0.5)
            if w >= 0.08:
                ax.text(left + w / 2, -i, f"{p}\n{w:.2f}", ha="center", va="center", fontsize=S.LABEL_PT - 1,
                        color="white" if p in ("identity", "value") else "#222222")  # fmt: skip
            left += w
            S.record("ledger_zach_routes", t, f"L{la}, whole change: {p} share", *sh[p], n=n, source=rel(Z3))
        ax.text(1.01, -i, f"n = {n}", va="center", fontsize=S.LABEL_PT, color=S.COL["muted"])
    rows_axis(ax, [r[0] for r in rows])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("share of the lookup's answers")
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
    ax.text(1.05, 0.5, "filled: the same\non every row\n\nhollow: the depth\nanatomy's cells,\n38 of 11,988 rows\ndiffer",
            transform=ax.transAxes, ha="left", va="center",
            fontsize=S.LABEL_PT, color=S.COL["muted"])  # fmt: skip
    return save(fig, "ledger_clean_reruns")


# ---- Lightning: the layer sweep and the conflict test at every layer ------------------------------------------------


def lightning_layers(plt) -> str:
    """Top: the whole change's switch rate per swept layer for both readers (60 dev scenes), the relative depth 0.25
    line, L14 marked. Bottom: the conflict test at every swept layer (200 scenes): each reader's switches lost without
    the lens part beyond a random part; cells under 30 switches greyed."""
    lay, ver = load(LAYER), load(CONFLICT)
    layers = sorted(int(k) for k in lay["rates"])
    fig, axes = plt.subplots(2, 1, figsize=(S.WIDTH, 5.8), sharex=True)
    fig.subplots_adjust(left=0.1, right=0.86, top=0.85, bottom=0.09, hspace=0.25)
    S.title(fig, "On Lightning the recall follows the lens part; the lookup does not",
            "Top: switches by the whole change per layer; bottom: switches lost beyond a random part")  # fmt: skip
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
    return save(fig, "ledger_lightning_layers")


# ---- where the answer is readable and usable (batch 52 B) -----------------------------------------------------------

ANSWER_MAP = R / "x52_answer_map" / "x52-20261029T004559Z" / "verdict.json"


def answer_map(plt) -> str:
    """Per model, dataset (our main test, Zach's described passages) and reader: left, the best share of items with
    the answer word in the lens's top 5 before the answer layer (the rule's 0.5 dashed); right, the answers changed by
    writing the answer word's lens directions at that cell (the better of gains 1 and 2, whiskers 95%) with the random
    part of the same gain in grey (the rule's 0.3 dashed); the combination at the right."""
    v = load(ANSWER_MAP)
    rows = []
    for m in sorted(v["models"], key=lambda m: [t for t, _ in MODEL3].index(m["target"])):
        for d, dname in (("main", "ours"), ("z2", "Zach's")):
            for rd in ("lookup", "recall"):
                rows.append((m, d, dname, rd))
    fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH, 0.36 * len(rows) + 1.9), sharey=True,
                             gridspec_kw={"width_ratios": [1, 1.25]})  # fmt: skip
    h = fig.get_figheight()
    fig.subplots_adjust(left=0.215, right=0.8, top=1 - 1.25 / h, bottom=0.75 / h, wspace=0.22)
    S.title(fig, "On Zach's passages the answer is readable and usable; on ours rarely",
            "Ours: our main test; Zach's: his described passages. Grey: a random part, same gain")  # fmt: skip
    labels = []
    for i, (m, d, dname, rd) in enumerate(rows):
        t, col, y = m["target"], (LOOKUP if rd == "lookup" else INK), -i
        r = m["maps"][d]["readers"][rd]
        best = r["readable"]["best_before"]
        axes[0].barh(y, best["top5"], color=col, height=0.6, alpha=0.85)
        w = m["writes"][d][rd]["switch"]
        g = "ans1" if w["ans1"][0] >= w["ans2"][0] else "ans2"
        whisker(axes[1], y, w[g], col)
        axes[1].plot([w["rand" + g[-1]][0]], [y], "o", color=NULL, ms=5)
        combo = v["combinations"][f"{t}|{d}|{rd}"]["combination"]
        axes[1].text(1.05, y, combo, va="center", fontsize=S.LABEL_PT, color="#222222", clip_on=False)
        labels.append(f"{SHORT[t]}, {dname}, {rd}")
        S.record("ledger_answer_map", t, f"{dname}, {rd}: best top-5 share before the answer layer "
                 f"({best['group']} L{best['layer']})", best["top5"], source=rel(ANSWER_MAP))  # fmt: skip
        S.record("ledger_answer_map", t, f"{dname}, {rd}: answers changed by the write, gain {g[-1]}", *w[g],
                 n=m["writes"][d][rd]["n"], source=rel(ANSWER_MAP))  # fmt: skip
    for ax, bar in ((axes[0], 0.5), (axes[1], 0.3)):
        ax.axvline(bar, color="#555555", lw=0.9, ls="--")
        ax.set_xlim(0, 1.0)
        ax.set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
        ax.grid(axis="x", color="#eeeeee")
        for b in (3.5, 7.5):
            ax.axhline(-b, color="#cccccc", lw=0.8)
    axes[0].set_yticks([-i for i in range(len(rows))], labels)
    axes[0].tick_params(axis="y", length=0)
    axes[0].set_ylim(-len(rows) + 0.4, 0.6)
    axes[0].set_xlabel("answer in the lens's top 5")
    axes[1].set_xlabel("answers changed by writing it")
    return save(fig, "ledger_answer_map")


FIGURES = (answer_control, address_shape, learned, heads, full_carrier, last_token_address, zach_named, zach_routes,
           clean_reruns, lightning_layers, answer_map)  # fmt: skip


def build_all(plt) -> list[str]:
    return [f(plt) for f in FIGURES]


if __name__ == "__main__":
    print(build_all(S.setup()))
