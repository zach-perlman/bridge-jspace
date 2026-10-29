"""The joint deck's figures (deck skeleton brief, 29 Oct ~23:45, Section 5) into figures/deck/ (PNG + SVG each, 16:9,
2400 x 1350 px). CPU only; every value is read from figures/story/data.csv, docs/x0_numbers.json, docs/breadth/data.csv
or docs/shared/grid.csv, never typed. Cells a source does not hold are left out of the frame and listed in
figures/deck/CAPTIONS.md with the n per bar.

  c0_setup_a / c0_setup_b  figures/shared/j0_setup.png cut in two (the datasets; the tools), no content change
  c1_controls              same-size parts do not do it: Zach's band removal (pp) | Dan's one-layer patch (share)
  c2_pointer               a pointer to the entity: Zach's transfer rows | Dan's lens-part atoms
  c3_address               the address: probe vs layout | the swap by dose | the lens's share rebuilt
  c4_readable              the last token: read / lens swap / whole patch | nine models: carried, needed
  c9_breaks                the 27B with more lens directions | Zach's named passages, true vs made-up facts

uv run python scripts/deck_figures.py
"""

from __future__ import annotations

import csv
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "figures" / "deck"
STORY = REPO / "figures/story/data.csv"
BREADTH = REPO / "docs/breadth/data.csv"
GRID = REPO / "docs/shared/grid.csv"
W, H, DPI = 16, 9, 150  # 2400 x 1350 px
COL = {"recall": "#3a3a3a", "lookup": "#6a4bd6", "lens": "#14a08a", "address": "#e08a1e", "identity": "#2b7bba",
       "random": "#9a9a9a", "band": "#efefef", "muted": "#666666", "answer": "#b8433a"}  # fmt: skip
DAN = (("qwen3.5-9b", "9B"), ("qwen3.6-27b", "27B"), ("muse-glimmer-30b", "Muse"),
       ("nemotron-3.5-lightning", "Lightning ○"), ("qwen3.5-122b-a10b", "122B"))  # fmt: skip
ZACH = (("q27", "27B"), ("q9", "9B"), ("nl", "Lightning"))
plt.rcParams.update({"font.size": 14, "axes.titlesize": 16, "axes.labelsize": 14, "xtick.labelsize": 13,
                     "ytick.labelsize": 14, "legend.fontsize": 13})  # fmt: skip
CAPTIONS: list[str] = []


def story() -> dict[tuple[str, str, str], tuple[float, float | None, float | None, str]]:
    out = {}
    with STORY.open() as f:
        for r in csv.DictReader(f):
            try:
                v = float(r["value"])
            except ValueError:
                continue
            lo = float(r["lo"]) if r["lo"] else None
            hi = float(r["hi"]) if r["hi"] else None
            out[(r["figure"], r["model"], r["quantity"])] = (v, lo, hi, r["n"])
    return out


def breadth() -> dict[str, dict]:
    with BREADTH.open() as f:
        return {r["key"]: r for r in csv.DictReader(f)}


def num(r: dict, k: str = "value") -> float | None:
    return float(r[k]) if r.get(k) not in (None, "") else None


S, B = story(), breadth()


def head(fig, title: str, sub: str) -> None:
    fig.text(0.015, 0.975, title, ha="left", va="top", fontsize=21, weight="bold")
    fig.text(0.015, 0.915, "\n".join(textwrap.wrap(sub, 150)), ha="left", va="top", fontsize=15, color=COL["muted"])


def save(fig, name: str, caption: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.svg", facecolor="white")
    fig.savefig(OUT / f"{name}.png", dpi=DPI, facecolor="white")
    plt.close(fig)
    CAPTIONS.append(f"- **{name}**: {caption}")
    print("wrote", OUT / f"{name}.png")


def dot(ax, y: float, cell, color: str, marker: str = "o", hollow: bool = False, label: str | None = None) -> None:
    v, lo, hi = cell[0], cell[1], cell[2]
    if lo is not None and hi is not None:
        ax.hlines(y, lo, hi, color=color, lw=2)
    ax.plot(v, y, marker, ms=11, mfc="white" if hollow else color, mec=color, mew=2, label=label, zorder=3)


def c0_setup() -> None:
    img = mpimg.imread(REPO / "figures/shared/j0_setup.png")
    half = img.shape[0] // 2
    for name, part, what in (("c0_setup_a", img[:half], "the two datasets"), ("c0_setup_b", img[half:], "the tools")):
        fig = plt.figure(figsize=(W, H))
        ax = fig.add_axes((0, 0, 1, 1))
        ax.imshow(part)
        ax.set_axis_off()
        save(fig, name, f"figures/shared/j0_setup.png, {what} (cut at half height; no content change).")


def c1_controls() -> None:
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, H))
    fig.subplots_adjust(top=0.74, bottom=0.14, left=0.08, right=0.98, wspace=0.35)
    head(fig, "No part of the same size costs recall as much as the lens part",
         "Left: Zach, the lens part removed over a band (recalled minus stated answers lost, points). Right: Dan, "
         "removed from a one-layer patch (recall's switches lost beyond random).")  # fmt: skip
    rows = (("mk", "lens part (J++ top 10)", COL["lens"], "o", False), ("pc", "PCA, same norm", COL["random"], "s", False),
            ("u", "logit-lens directions", COL["random"], "o", True), ("rot", "rotated", COL["random"], "D", False))  # fmt: skip
    ns = []
    for i, (m, name) in enumerate(ZACH):
        for j, (k, lab, c, mk, hol) in enumerate(rows):
            r = B.get(f"ko.{m}.{k}")
            if r is None:
                continue
            dot(a, i + 0.18 * j - 0.27, (num(r), num(r, "lo"), num(r, "hi")), c, mk, hol, lab if i == 0 else None)
        ns.append(f"{name} n = {B[f'ko.{m}.mk']['n']}")
    a.set_yticks(range(len(ZACH)), [n for _, n in ZACH])
    a.invert_yaxis()
    a.axvspan(-5, 5, color=COL["band"], zorder=0)
    a.axvline(0, color="black", lw=0.8)
    a.set_xlabel("recalled minus stated answers lost (points)")
    a.legend(frameon=False, loc="lower right")
    a.set_title("Zach: remove everywhere (band)", loc="left")
    qs = (("J++ part: recall extra loss", "lens part (25)", COL["lens"], "o", False),
          ("PCA directions (same size): recall extra loss", "PCA, same size", COL["random"], "s", False),
          ("logit-lens directions: recall extra loss", "logit-lens directions", COL["random"], "o", True),
          ("random lens directions: recall extra loss", "random lens directions", COL["random"], "D", False))  # fmt: skip
    models = [(m, n) for m, n in DAN if ("fig02", m, qs[0][0]) in S]
    for i, (m, _) in enumerate(models):
        for j, (q, lab, c, mk, hol) in enumerate(qs):
            if ("fig02", m, q) in S:
                dot(b, i + 0.18 * j - 0.27, S[("fig02", m, q)], c, mk, hol, lab if i == 0 else None)
    b.set_yticks(range(len(models)), [n for _, n in models])
    b.invert_yaxis()
    b.axvspan(-0.10, 0.10, color=COL["band"], zorder=0)
    b.axvline(0, color="black", lw=0.8)
    b.set_xlabel("recall: switches lost beyond a random part")
    b.legend(frameon=False, loc="lower right")
    b.set_title("Dan: remove from the patch (one layer)", loc="left")
    save(
        fig,
        "c1_controls",
        "docs/breadth/data.csv ko.{q27,q9,nl}.{mk,pc,u,rot} (" + "; ".join(ns) + "); "
        "figures/story/data.csv fig02 rows (main test at L; Lightning has no fig02 row: left out). Whiskers 95%.",
    )


def c2_pointer() -> None:
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, H), gridspec_kw={"width_ratios": [1.15, 1]})
    fig.subplots_adjust(top=0.74, bottom=0.14, left=0.27, right=0.97, wspace=0.45)
    head(fig, "The lens part says which entity it is: a pointer, from any context, not its fact",
         "Left: Zach, another entity's lens part written in (recall moved, points). Right: Dan, what the lens "
         "part's 25 directions are (share of the rebuilt energy).")  # fmt: skip
    labels = ["from D's own passage", "from one neutral sentence", "  without D's own-word directions",
              "  neutral donor, rotated", "the probe's subspace (reads the fact)", "  the lens part, same relations"]  # fmt: skip
    for j, (m, name) in enumerate(ZACH):
        own = B[f"ptr.{m}.swap"]
        base = num(own)
        cells = [(base, num(own, "lo"), num(own, "hi")), (base * num(B[f"ptr.{m}.neutral"]), None, None),
                 (base * num(B[f"ptr.{m}.noown"]), None, None), (num(B[f"ptr.{m}.rot"]), None, None),
                 (num(B[f"probe.{m}.probe"]), None, None), (num(B[f"probe.{m}.swap"]), None, None)]  # fmt: skip
        for i, cell in enumerate(cells):
            c = COL["lookup"] if i == 4 else COL["lens"] if i < 3 or i == 5 else COL["random"]
            dot(a, i + 0.22 * (j - 1), cell, c, ("o", "s", "^")[j], hollow=(m == "nl"), label=name if i == 0 else None)
    a.set_yticks(range(len(labels)), labels)
    a.invert_yaxis()
    a.axvline(0, color="black", lw=0.8)
    a.set_xlabel("recall moved toward the other entity (points)")
    a.legend(frameon=False, loc="lower right", title="model")
    parts = (("52 A: share of the rebuilt energy in the original bridge word", "old bridge word", COL["recall"]),
             ("52 A: share of the rebuilt energy in the new bridge word", "new bridge word", COL["lens"]),
             ("52 A: share of the rebuilt energy in the reader's answer word", "answer word", COL["answer"]),
             ("52 A: share of the rebuilt energy in no scene word", "no scene word", "#d9d9d9"))  # fmt: skip
    models = [
        (m, n)
        for m, n in DAN
        if ("fig18_atoms", m, parts[0][0]) in S or any(k[1] == m and k[2] == parts[0][0] for k in S)
    ]
    for i, (m, _) in enumerate(models):
        left = 0.0
        for q, lab, c in parts:
            v = next(val[0] for k, val in S.items() if k[1] == m and k[2] == q)
            b.barh(i, v, left=left, color=c, edgecolor="white", hatch="//" if m.startswith("nem") else None,
                   label=lab if i == 0 else None)  # fmt: skip
            if lab == "answer word":
                b.text(1.02, i, f"answer {v:.2f}", va="center", fontsize=12, color=COL["answer"])
            left += v
    b.set_yticks(range(len(models)), [n for _, n in models])
    b.invert_yaxis()
    b.set_xlim(0, 1.25)
    b.set_xticks((0, 0.5, 1))
    b.set_xlabel("share of the rebuilt energy")
    b.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.12), ncol=2, fontsize=12)
    b.set_title("The bridge words, never the answer", loc="left")
    save(
        fig,
        "c2_pointer",
        "docs/breadth/data.csv ptr.{q27,q9,nl}.{swap,neutral,noown,rot} and probe.*.{probe,swap}; "
        "the neutral-sentence and own-word rows are the same-passage swap times their stored ratios (computed "
        "here, no CI); the probe rows are on probe-valid relations. figures/story/data.csv 52 A rows (50 main-test "
        "scenes per model; the 122B: no 52 A row, left out; Lightning hatched).",
    )


def c3_address() -> None:
    fig, axs = plt.subplots(1, 3, figsize=(W, H), gridspec_kw={"width_ratios": [1, 1.1, 1]})
    fig.subplots_adjust(top=0.74, bottom=0.14, left=0.12, right=0.98, wspace=0.42)
    head(fig, "The lookup reads an address: a probe finds it, a swap moves it, the lens cannot see it",
         "(A) a probe at the bridge word; (B) the address swap by dose; (C) the lens's share rebuilt by 25 "
         "directions.")  # fmt: skip
    a = axs[0]
    rows = [(m, n, ("fig07", m)) for m, n in DAN]
    probe = "the locker probe at the bridge word, locker-first scenes"
    lay = "the locker probe's layout baseline, locker-first scenes"
    ys, labs = [], []
    for i, (m, n, _) in enumerate(rows):
        cell = next((v for k, v in S.items() if k[1] == m and k[2] == probe), None)
        base = next((v for k, v in S.items() if k[1] == m and k[2] == lay), None)
        if cell is None:
            continue
        a.barh(i, cell[0], color=COL["address"], fill=not m.startswith("nem"), edgecolor=COL["address"], lw=2)
        a.text(cell[0] + 0.01, i, f"{cell[0]:.2f}", va="center", fontsize=12)
        if base:
            a.plot([base[0]] * 2, [i - 0.4, i + 0.4], color="black", lw=2, ls=":")
        ys.append(i)
        labs.append(n)
    for k, (fmt, lab) in enumerate((("tool", "27B · tool output"), ("code", "27B · code"))):
        q = f"code and tool output, {fmt}: the locker probe at the bridge word, locker-first scenes"
        cell = S.get(("fig21_code_tool", "qwen3.6-27b", q)) or next(
            (v for kk, v in S.items() if kk[1] == "qwen3.6-27b" and kk[2] == q), None
        )
        if cell:
            y = len(rows) + k + 0.3
            a.barh(y, cell[0], color=COL["address"], alpha=0.6)
            a.text(cell[0] + 0.01, y, f"{cell[0]:.2f}", va="center", fontsize=12)
            ys.append(y)
            labs.append(lab)
    a.set_yticks(ys, labs)
    a.invert_yaxis()
    a.set_xlim(0.4, 1.08)
    a.set_xlabel("probe accuracy (dotted: layout baseline)")
    a.set_title("(A) a probe reads it", loc="left")
    b = axs[1]
    ring: list[str] = []
    for m, n in DAN:
        pts = [(s, S[("fig07", m, f"lookup target share, mean over locker pairs, s = {s}")])
               for s in (1, 2, 4) if ("fig07", m, f"lookup target share, mean over locker pairs, s = {s}") in S]  # fmt: skip
        if not pts:
            continue
        hol = m.startswith("nem") or m.startswith("qwen3.5-122b")
        b.plot([s for s, _ in pts], [c[0] for _, c in pts], "-o", color=COL["lookup"], mfc="white" if hol else COL["lookup"],
               ms=8, alpha=0.9)  # fmt: skip
        two = dict(pts).get(2)
        if two:
            b.plot(2, two[0], "o", ms=18, mfc="none", mec=COL["lookup"], mew=1.5)
            ring.append(f"{n} {two[0]:.2f}")
    b.text(0.03, 0.97, "s = 2:\n" + "\n".join(ring), transform=b.transAxes, ha="left", va="top", fontsize=12)
    rnd = [c[0] for k, c in S.items() if k[0] == "fig07" and k[2] == "lookup target share, random direction, s = 4"]
    if rnd:
        b.axhspan(min(rnd), max(rnd) + 0.01, color=COL["band"])
    b.axvline(1, color="black", ls=":", lw=1)
    b.set_xticks((1, 2, 4))
    b.set_xlabel("dose (2 = about a real change)")
    b.set_ylabel("lookups sent to the swapped-in locker")
    b.set_title("(B) a swap moves it (ring: s = 2)", loc="left")
    c = axs[2]
    q = "47.0 (b) share rebuilt by 25 lens directions: "
    models = [(m, n) for m, n in DAN if ("fig07b_verbal", m, q + "pointer") in S]
    for i, (m, _) in enumerate(models):
        rng = S.get(("fig07b_verbal", m, q + "the random draws' 95% range"))
        if rng and rng[1] is not None:
            c.barh(i, rng[2] - rng[1], left=rng[1], color=COL["band"], height=0.6)
        c.plot(S[("fig07b_verbal", m, q + "pointer")][0], i, ">", ms=14, color=COL["address"],
               mfc="white" if m.startswith("nem") else COL["address"], label="address swap" if i == 0 else None)  # fmt: skip
        c.plot(S[("fig07b_verbal", m, q + "identity_mean")][0], i, "o", ms=12, color=COL["identity"],
               mfc="white" if m.startswith("nem") else COL["identity"], label="item change (control)" if i == 0 else None)  # fmt: skip
    c.set_yticks(range(len(models)), [n for _, n in models])
    c.invert_yaxis()
    c.set_xlabel("share rebuilt (grey: random vectors)")
    c.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=12)
    c.set_title("(C) the lens does not see it", loc="left")
    save(
        fig,
        "c3_address",
        "figures/story/data.csv: fig07 (probe 657-758 scenes, swap 600 per dose and model; Lightning "
        "hollow; the 122B hollow in (B): its gate lowered after the data), fig21_code_tool (the 27B's code 682 and "
        "tool 1,500 scenes), fig07b_verbal (200 cases; the 122B has no 47.0 row in the depth README: left out). "
        "Random vector at s = 4: the grey band in (B).",
    )


def c4_readable() -> None:
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, H), gridspec_kw={"width_ratios": [1, 1.3]})
    fig.subplots_adjust(top=0.74, bottom=0.24, left=0.08, right=0.98, wspace=0.3)
    head(fig, "Readable is not used: the lens reads the entity; the answer does not go through it",
         "Left: Dan, at the last token: a probe on the lens part, the lens swap, the whole-state patch. "
         "Right: Zach, nine models: carried by a swap, needed.")  # fmt: skip
    qs = (("51.10: recall, last token, read peak: the probe's accuracy on the lens part", "read (probe on the lens part)", COL["recall"]),
          ("51.10: recall, last token, read peak: the lens swap's switches", "lens swap: recalls switched", COL["lens"]),
          ("51.10: recall, last token, read peak: the whole-state patch's switches", "whole-state patch", COL["random"]))  # fmt: skip
    models = [(m, n) for m, n in DAN if ("fig17_jspace_last_token", m, qs[0][0]) in S]
    for i, (m, _) in enumerate(models):
        for j, (q, lab, c) in enumerate(qs):
            v = S[("fig17_jspace_last_token", m, q)][0]
            a.bar(i + 0.27 * (j - 1), v, 0.25, color=c, hatch="//" if m.startswith("nem") else None,
                  label=lab if i == 0 else None)  # fmt: skip
            a.text(i + 0.27 * (j - 1), v + 0.02, f"{v:.2f}", ha="center", fontsize=11)
    a.set_xticks(range(len(models)), [n for _, n in models])
    a.set_ylim(0, 1.15)
    a.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=1, fontsize=12)
    a.set_title("Dan: the recall at the last token", loc="left")
    with GRID.open() as f:
        grid = list(csv.DictReader(f))
    claims = (("another entity's J++ part moves the answer (≥ 20 points)", "breadth", "carried by a swap"),
              ("recall needs the J++ part; reading the prompt does not", "breadth", "needed"))  # fmt: skip
    models9 = list(dict.fromkeys(r["model"] for r in grid))
    mark = {"ok": ("✓", "#2f7d4f"), "~": ("~", "#b07a0a"), "x": ("✗", "#b8433a"), "-": ("–", "#9a9a9a")}
    for i, (claim, study, _lab) in enumerate(claims):
        for j, m in enumerate(models9):
            cell = next(
                (r["cell"] for r in grid if r["claim"] == claim and r["study"] == study and r["model"] == m), "-"
            )
            s, c = mark.get(cell, ("–", "#9a9a9a"))
            b.text(j, i, s, ha="center", va="center", fontsize=24, color=c, weight="bold")
    b.set_xlim(-0.6, len(models9) - 0.4)
    b.set_ylim(len(claims) - 0.5, -0.6)
    b.set_yticks(range(len(claims)), [lab for _, _, lab in claims])
    b.set_xticks(range(len(models9)), [m.replace(" (FP8)", "").replace("Nemotron 3.5 ", "") for m in models9],
                 rotation=30, ha="right")  # fmt: skip
    b.tick_params(length=0)
    for s in b.spines.values():
        s.set_visible(False)
    b.set_title("Zach: nine models (✓ holds, ~ in part, ✗ no, – not run)", loc="left")
    save(
        fig,
        "c4_readable",
        "figures/story/data.csv fig17_jspace_last_token rows (locker-first items; the 122B not run "
        "in the depth README: left out; Lightning hatched); docs/shared/grid.csv, breadth study cells of the two "
        "claims. 'Readable at the mention' (all nine) has no row in the CSVs: not drawn.",
    )


def c9_breaks() -> None:
    fig, (a, b) = plt.subplots(1, 2, figsize=(W, H), gridspec_kw={"width_ratios": [1, 1.4]})
    fig.subplots_adjust(top=0.74, bottom=0.14, left=0.08, right=0.98, wspace=0.3)
    head(fig, "Where it breaks: the 27B with more directions; passages whose fact the model already knows",
         "Left: the lookup without 25 / 50 / 100 lens directions, beyond random. Right: Zach's named passages, "
         "true facts (filled) vs made-up facts (open).")  # fmt: skip
    for m, n, c in (("qwen3.6-27b", "27B", COL["lookup"]), ("qwen3.5-122b-a10b", "122B", "#b07a0a")):
        cells = [S[("fig02b", m, f"(a) main test, {k} directions: lookup extra loss")] for k in (25, 50, 100)]
        a.plot((25, 50, 100), [c_[0] for c_ in cells], "-o", color=c, ms=10, label=n)
        for k, cell in zip((25, 50, 100), cells, strict=True):
            if cell[1] is not None and cell[2] is not None:
                a.vlines(k, cell[1], cell[2], color=c)
            a.text(k + 2, cell[0], f"{cell[0]:.2f}", color=c, fontsize=12, va="center")
    a.axhspan(-0.10, 0.10, color=COL["band"], zorder=0)
    a.axhline(0, color="black", lw=0.8)
    a.set_xticks((25, 50, 100))
    a.set_xlabel("lens directions taken out")
    a.set_ylabel("lookup: switches lost beyond a random part")
    a.legend(frameon=False)
    for i, (m, _n) in enumerate(DAN[:4]):
        for j, facts in enumerate(("true facts", "made-up facts")):
            k = ("ledger_zach_named", m, f"Zach's named passages, {facts}, lookup: switches lost beyond random")
            if k in S:
                v = S[k][0]
                b.bar(
                    i + (j - 0.5) * 0.38, v, 0.36, color="white" if j else COL["lookup"], edgecolor=COL["lookup"], lw=2
                )
                b.text(i + (j - 0.5) * 0.38, max(v, 0) + 0.02, f"{v:.2f}", ha="center", fontsize=11)
    b.set_xticks(range(4), [n for _, n in DAN[:4]])
    b.axhspan(-0.10, 0.10, color=COL["band"], zorder=0)
    b.axhline(0, color="black", lw=0.8)
    b.set_ylabel("lookup: switches lost beyond random")
    save(
        fig,
        "c9_breaks",
        "figures/story/data.csv fig02b (main test, 200 scenes) and ledger_zach_named (his named "
        "passages; Lightning's gate chosen after its pre-check; Muse and Lightning missed the made-up-fact gate: "
        "descriptive). The question-order panel moved to the appendix (A18).",
    )


def main() -> None:
    c0_setup()
    c1_controls()
    c2_pointer()
    c3_address()
    c4_readable()
    c9_breaks()
    (OUT / "CAPTIONS.md").write_text("# figures/deck: captions and n\n\nBuilt by scripts/deck_figures.py.\n\n"
                                     + "\n".join(CAPTIONS) + "\n")  # fmt: skip
    print("wrote", OUT / "CAPTIONS.md")


if __name__ == "__main__":
    main()
