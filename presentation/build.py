"""Every figure of the final deck (presentation brief, Fri 30 Oct ~00:40) into presentation/ (PNG + SVG), each linted
before it is saved, then presentation/CAPTIONS.md and presentation/contact_sheet.png. CPU only; every number is read
from figures/story/data.csv, docs/x0_numbers.json or docs/breadth/data.csv, never typed.

uv run python presentation/build.py            # everything
uv run python presentation/build.py p1 p5 p6   # some figures
"""

from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from presentation import lint
from presentation import style as ST

ST.setup()
S, B, X = ST.story(), ST.breadth(), ST.x0()
C = ST.COL
CAPTIONS: dict[str, str] = {}


def save(fig, name: str, caption: str) -> None:
    bad = lint.problems(fig, name)
    if bad:
        raise SystemExit("lint:\n" + "\n".join(bad))
    ST.OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(ST.OUT / f"{name}.png", dpi=ST.DPI, facecolor="white")
    fig.savefig(ST.OUT / f"{name}.svg", facecolor="white")
    plt.close(fig)
    CAPTIONS[name] = caption
    print("wrote", ST.OUT / f"{name}.png")


def band(ax, lo: float, hi: float, label: str | None = None, x: float | None = None) -> None:
    ax.axhspan(lo, hi, color=C["band"], alpha=ST.BAND_ALPHA, lw=0, zorder=0)
    if label:
        ax.text(ax.get_xlim()[1] if x is None else x, hi, f" {label}", fontsize=ST.SMALL, color=C["random"],
                va="bottom", ha="right")  # fmt: skip


def mark(ax, x, cell, color, hollow=False, marker="o", size=9, value=True, fmt="{:.2f}", dx=0.12, whisker=True):
    v, lo, hi = cell[0], cell[1], cell[2]
    if whisker and lo is not None and hi is not None:
        ax.vlines(x, lo, hi, color=color, lw=1.6, zorder=2)
    ax.plot(x, v, marker, ms=size, mfc="white" if hollow else color, mec=color, mew=2, zorder=3)
    if value:
        ax.text(x + dx, v, fmt.format(v), fontsize=ST.VALUE, va="center", ha="left", color=color)


# ---- P1: C1, the split, two tools, five models ----------------------------------------------------------------------
def p1() -> None:
    fig, (a, b) = ST.figure(ncols=2)
    zm = (("q27", "Qwen 27B", False), ("q9", "Qwen 9B", False), ("nl", "Lightning", False),
          ("mu", "Muse 30B ○", True), ("q122", "Qwen 122B ○", True))  # fmt: skip
    for i, (m, _name, hol) in enumerate(zm):
        rec, look = B[f"ko.{m}.lostM"], B[f"ko.{m}.lostK"]
        ctrl = max(v for v in (_ctrl(m)) if v is not None)
        a.vlines(i, look[0], rec[0], color=C["light"], lw=4, zorder=1)
        mark(a, i, rec, C["recall"], hol, fmt="{:.1f}", whisker=False)
        mark(a, i, look, C["lookup"], hol, fmt="{:.1f}", whisker=False)
        a.plot([i - 0.15, i + 0.15], [ctrl, ctrl], color=C["random"], lw=2.5)
        if i == 0:
            a.text(i - 0.15, rec[0], "recall ", ha="right", va="center", fontsize=ST.SERIES, color=C["recall"])
            a.text(i - 0.15, look[0], "lookup ", ha="right", va="center", fontsize=ST.SERIES, color=C["lookup"])
            a.text(i + 0.18, ctrl, "largest control", ha="left", va="center", fontsize=ST.SMALL, color=C["random"])
    a.set_xticks(range(len(zm)), [n for _, n, _ in zm], rotation=20, ha="right")
    a.set_xlim(-0.9, len(zm) - 0.4)
    a.set_ylim(-3, 70)
    a.set_ylabel("answers that turn wrong (pp)")
    for i, (m, _name) in enumerate(ST.DAN):
        rc = X.get(f"rc_excess_{_x(m)}") or ST.find(S, m, "conflict: recall, switches lost beyond a random part")
        lk = X.get(f"lk_excess_{_x(m)}") or ST.find(S, m, "conflict: lookup, switches lost beyond a random part")
        hol = ST.hollow(m)
        mark(b, i, rc, C["recall"], hol)
        mark(b, i, lk, C["lookup"], hol)
        gap = X.get(f"contrast_{_x(m)}")
        b.text(
            i, 1.0, f"{gap[0] if gap else rc[0] - lk[0]:.2f}", ha="center", va="top", fontsize=ST.VALUE, weight="bold"
        )
        if i == 0:
            b.text(i - 0.15, rc[0], "recall ", ha="right", va="center", fontsize=ST.SERIES, color=C["recall"])
            b.text(i - 0.15, lk[0], "lookup ", ha="right", va="center", fontsize=ST.SERIES, color=C["lookup"])
    b.set_xticks(range(len(ST.DAN)), [n for _, n in ST.DAN], rotation=20, ha="right")
    b.set_xlim(-0.9, len(ST.DAN) - 0.4)
    b.set_ylim(-0.2, 1.05)
    band(b, -0.10, 0.10, "not needed")
    b.axhline(0, color="black", lw=0.6)
    b.set_ylabel("switches lost beyond a random part")
    save(
        fig,
        "p1_c1_split",
        "**C1. Recall needs the lens part; lookup does not.** Left (Zach): the lens part's top-10 "
        "J++ directions removed at every token over his band; points lost on recalled (M) and stated (K) finals "
        "(docs/breadth/data.csv ko.*.lostM / lostK; n 892 / 563 / 563 / Muse / 122B per ko.*.mk); the grey tick is "
        "the largest same-size control in M − K (max of ko.*.rot, ko.*.u, PCA ko.*.pc or pcr × mk). Muse 30B and "
        "Qwen 122B hollow (Zach: shared with the logit lens; by probability). Right (Dan): the conflict test at L, "
        "switches lost beyond a random part (docs/x0_numbers.json rc_excess_* / lk_excess_*; Lightning from "
        "figures/story/data.csv 'conflict: …'), 200 scenes per model, 95% cluster-bootstrap whiskers; the bold number "
        "is recall minus lookup (computed here). Lightning hollow (gate chosen after its pre-check); Lightning "
        "pending hand-check (29 Oct).",
    )


def _x(m: str) -> str:
    return {"qwen3.5-9b": "9b", "qwen3.6-27b": "27b", "muse-glimmer-30b": "muse", "qwen3.5-122b-a10b": "122b"}.get(
        m, "-"
    )


def _ctrl(m: str) -> list[float | None]:
    pc = B.get(f"ko.{m}.pc")
    pcr, mk = B.get(f"ko.{m}.pcr"), B.get(f"ko.{m}.mk")
    pcv = pc[0] if pc else (pcr[0] * mk[0] if pcr and mk else None)
    return [B[k][0] if k in B else None for k in (f"ko.{m}.rot", f"ko.{m}.u")] + [pcv]


# ---- P5: C3, the address --------------------------------------------------------------------------------------------
def p5() -> None:
    fig, (a, b, c) = ST.figure(ncols=3)
    probe, lay = (
        "the locker probe at the bridge word, locker-first scenes",
        "the locker probe's layout baseline, locker-first scenes",
    )
    xs, names = [], []
    for i, (m, name) in enumerate(ST.DAN):
        cell = ST.find(S, m, probe)
        hol = ST.hollow(m)
        a.bar(i, cell[0], 0.7, color="white" if hol else C["address"], edgecolor=C["address"], lw=2)
        a.text(i, cell[0] + 0.01, f"{cell[0]:.2f}", ha="center", va="bottom", fontsize=ST.VALUE)
        xs.append(i)
        names.append(name)
    base = ST.find(S, "qwen3.5-9b", lay)[0]
    a.axhline(base, color=C["random"], ls="--", lw=1.5)
    a.text(-0.4, base + 0.01, f"layout baseline {base:.2f}", fontsize=ST.SMALL, color=C["random"], va="bottom")
    for k, (fmt, lab) in enumerate((("tool", "27B · tool"), ("code", "27B · code"))):
        cell = ST.find(
            S, "qwen3.6-27b", f"code and tool output, {fmt}: the locker probe at the bridge word, locker-first scenes"
        )
        x = len(ST.DAN) + 0.6 + k * 0.8
        a.bar(x, cell[0], 0.45, color=C["address"], alpha=0.55)
        a.text(x, cell[0] + 0.01, f"{cell[0]:.2f}", ha="center", va="bottom", fontsize=ST.VALUE)
        xs.append(x)
        names.append(lab)
    a.set_xticks(xs, names, rotation=35, ha="right")
    a.set_ylim(0.4, 1.06)
    a.set_ylabel("probe accuracy (share of scenes)")
    ends = []
    for m, name in ST.DAN:
        pts = []
        for s in (1, 2, 4):
            d = ST.find(S, m, f"dose (s / mean s*), s = {s}", "fig07")
            v = ST.find(S, m, f"lookup target share, mean over locker pairs, s = {s}", "fig07")
            if d and v:
                pts.append((d[0], v[0], s))
        if not pts:
            continue
        hol = ST.hollow(m, lowered_test=True)
        b.plot([p[0] for p in pts], [p[1] for p in pts], "-o", color=C["lookup"], mfc="white" if hol else C["lookup"],
               ms=7, lw=1.8)  # fmt: skip
        two = next(p for p in pts if p[2] == 2)
        b.plot(two[0], two[1], "o", ms=16, mfc="none", mec=C["lookup"], mew=1.2)
        ends.append([pts[-1][0], pts[-1][1], f"{name.split(' ○')[0].replace('Qwen ', '')} ({two[1]:.2f} at s = 2)"])
    ends.sort(key=lambda e: e[1])
    for k in range(1, len(ends)):  # stagger the end labels
        ends[k][1] = max(ends[k][1], ends[k - 1][1] + 0.055)
    for x, y, lab in ends:
        b.text(x + 0.06, y, lab, fontsize=ST.SMALL, va="center", color=C["lookup"])
    rnd = [v[0] for k, v in S.items() if k[0] == "fig07" and k[2] == "lookup target share, random direction, s = 4"]
    b.axhspan(-0.01, max(rnd) + 0.02, color=C["band"], alpha=ST.BAND_ALPHA, lw=0)
    b.text(0.05, max(rnd) + 0.03, "random part", fontsize=ST.SMALL, color=C["random"])
    b.axvline(1, color="black", ls="--", lw=1)
    b.text(1.03, 0.92, "a real change", fontsize=ST.SMALL, transform=b.get_xaxis_transform())
    b.set_xlim(0, 4.6)
    b.set_ylim(-0.02, 0.85)
    b.set_xlabel("dose (units of a real change)")
    b.set_ylabel("lookups answering the swapped-in locker")
    zq = "47.0 (b) share rebuilt by 25 lens directions: "
    models = [(m, n) for m, n in ST.DAN if any(k[1] == m and k[2].startswith(zq + "pointer: z") for k in S)]
    for i, (m, name) in enumerate(models):
        pz = next(v for k, v in S.items() if k[1] == m and k[2].startswith(zq + "pointer: z"))
        iz = next(v for k, v in S.items() if k[1] == m and k[2].startswith(zq + "identity_mean: z"))
        hol = ST.hollow(m)
        c.plot(i, pz[0], ">", ms=12, color=C["address"], mfc="white" if hol else C["address"])
        c.text(i + 0.15, pz[0], f"{pz[0]:.1f}", fontsize=ST.VALUE, va="center", color=C["address"])
        c.plot(i, iz[0], "o", ms=11, color=C["identity"], mfc="white" if hol else C["identity"])
        c.text(i + 0.15, iz[0], f"{iz[0]:.1f}", fontsize=ST.VALUE, va="center", color=C["identity"])
        if i == 0:
            c.text(
                i,
                iz[0] - 1.6,
                "item change\n(positive control)",
                fontsize=ST.SMALL,
                color=C["identity"],
                ha="center",
                va="top",
            )
            c.text(i, pz[0] + 1.6, "address swap", fontsize=ST.SMALL, color=C["address"], ha="center", va="bottom")
    c.axhspan(-1, 1, color=C["band"], alpha=ST.BAND_ALPHA, lw=0)
    c.text(-0.45, -1.9, "random vectors", fontsize=ST.SMALL, color=C["random"], ha="left", va="bottom")
    c.set_xticks(range(len(models)), [n for _, n in models], rotation=25, ha="right")
    c.set_xlim(-0.5, len(models) - 0.3)
    c.set_ylim(-2, 25)
    c.set_ylabel("lens rebuild above random vectors (z)")
    save(
        fig,
        "p5_c3_address",
        "**C3. The address: a probe finds it, a swap moves it, the lens cannot see it.** (A) a "
        "probe at the bridge word reads which locker sentence holds the item's locker (locker-first scenes; 657-758 "
        "scenes per model), against the layout baseline (dashed); the 27B's tool output (1,500 scenes) and code (682) "
        "beside. Lightning hollow; the 122B's probe ran at its gate (filled, as in the depth README). (B) the "
        "address swap by dose (dose = s / the mean real change, figures/story/data.csv fig07), 600 swaps per dose and "
        "model; ring = s = 2; Lightning and the 122B hollow (the 122B's gate lowered to 0.75 after the data); grey: "
        "a random vector at s = 4. The swap's rule fixed in advance was read at s = 1 and said no (a design error). "
        "(C) how far above 200 random vectors of the same size the lens's 25 directions rebuild the address swap "
        "(orange) and an item change (blue), in z (grey: the random vectors' 95% range, −1 to 1); 200 cases per "
        "model; the 122B has no 47.0 run in the depth README (not on the axis). Code and tool output, the 122B's "
        "rows, Lightning: pending hand-check (29 Oct).",
    )


# ---- P6: C4, readable is not used -----------------------------------------------------------------------------------
def p6() -> None:
    fig, ax = ST.figure(ST.HALF)
    rows = []
    for m, name in ST.DAN:
        read = next(((k[2], v) for k, v in S.items() if k[0] == "fig17_jspace_last_token" and k[1] == m
                     and re.match(r"51\.10: recall, last token, read peak layer \d+: the probe's accuracy", k[2])), None)  # fmt: skip
        swap = next(((k[2], v) for k, v in S.items() if k[0] == "fig17_jspace_last_token" and k[1] == m
                     and re.match(r"51\.10: recall, last token, read peak layer \d+: the lens swap's switches over", k[2])), None)  # fmt: skip
        if read and swap:
            rows.append((m, name, int(re.search(r"layer (\d+)", read[0]).group(1)), read[1], swap[1]))
    for i, (m, name, layer, read, swap) in enumerate(rows):
        hatch = "//" if ST.hollow(m) else None
        ax.bar(i - 0.27, read[0], 0.26, color=C["recall"], hatch=hatch, edgecolor="white")
        ax.bar(i, max(swap[0], 0.004), 0.26, color=C["lens"], hatch=hatch, edgecolor="white")
        ax.bar(i + 0.27, 1.0, 0.26, color="none", edgecolor=C["random"], lw=1.5)
        ax.text(i - 0.27, read[0] + 0.02, f"{read[0]:.2f}", ha="center", fontsize=ST.SMALL)
        ax.text(i, swap[0] + 0.02, f"{swap[0]:.2f}", ha="center", fontsize=ST.SMALL, color=C["lens"])
        if i == 0:
            ax.text(
                i - 0.27, read[0] / 2, "read", rotation=90, ha="center", va="center", color="white", fontsize=ST.SMALL
            )
            ax.text(i + 0.27, 0.5, "whole state = 1", rotation=90, ha="center", va="center", color=C["random"],
                    fontsize=ST.SMALL)  # fmt: skip
            ax.text(i, 0.12, "lens swap", rotation=90, ha="center", va="bottom", color=C["lens"], fontsize=ST.SMALL)
    chance = max(ST.find(S, m, "51.10: the read probe's chance (locker-first rows)")[0] for m, *_ in rows)
    ax.axhline(chance, color=C["random"], ls="--", lw=1.2)
    ax.text(len(rows) - 0.5, chance + 0.01, "chance", ha="right", fontsize=ST.SMALL, color=C["random"])
    ax.set_xticks(range(len(rows)), [n for _, n, *_ in rows])
    for i, (_, _, layer, _, _) in enumerate(rows):
        ax.text(i, -0.1, f"L{layer}", ha="center", va="top", fontsize=ST.SMALL, color=C["random"],
                transform=ax.get_xaxis_transform())  # fmt: skip
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("share")
    save(
        fig,
        "p6_c4_readable",
        "**C4. Readable is not used.** At the last token, at the layer where the read peaks "
        "(under each model): read = a probe for the recall's bridge entity on the lens part of the state (dark); lens "
        "swap = the changed prompt's lens part swapped in, its switches as a share of the whole-state patch's (teal); "
        "the whole-state patch = 1 by construction (grey outline). Locker-first items; chance = the probe's chance "
        "(dashed, the highest of the four). figures/story/data.csv fig17_jspace_last_token rows. Lightning hatched "
        "(its gate chosen after its pre-check; pending hand-check, 29 Oct); the 122B has no 51.10 run in the depth "
        "README (not on the axis). Rule: '(b) readable, not used' on all four.",
    )


# ---- P2: same-size parts do not do it -------------------------------------------------------------------------------
def p2() -> None:
    fig, (a, b) = ST.figure(ncols=2)
    kinds = (("lens part (J++ top 10)", C["recall"], "o", False), ("rotated", C["random"], "o", True),
             ("logit lens", C["random"], "s", False), ("PCA, same norm", C["random"], "^", False))  # fmt: skip
    for i, (m, name) in enumerate(ST.ZACH[:3]):
        rot, u, pc = _ctrl(m)
        vals = [B[f"ko.{m}.mk"], (rot, None, None, ""), (u, None, None, ""), (pc, None, None, "")]
        for j, ((lab, col, mk, hol), cell) in enumerate(zip(kinds, vals, strict=True)):
            x = i + (j - 1.5) * 0.17
            mark(a, x, cell, col, hol, mk, value=(j == 0), fmt="{:.1f}")
            if i == 0:
                a.text(x, cell[0] + (4 if j else -6), lab, rotation=90, fontsize=ST.SMALL, color=col, ha="center",
                       va="bottom" if j else "top")  # fmt: skip
    a.set_xticks(range(3), [n for _, n in ST.ZACH[:3]])
    a.axhspan(-5, 5, color=C["band"], alpha=ST.BAND_ALPHA, lw=0)
    a.set_ylim(-8, 62)
    a.set_ylabel("recalled minus stated answers lost (pp)")
    qs = (("J++ part: recall extra loss", "lens part (25)", C["lens"], "o", False),
          ("PCA directions (same size): recall extra loss", "PCA, same size", C["random"], "^", False),
          ("logit-lens directions: recall extra loss", "logit lens", C["random"], "s", False),
          ("random lens directions: recall extra loss", "random lens dirs", C["random"], "o", True))  # fmt: skip
    models = [(m, n) for m, n in ST.DAN if ("fig02", m, qs[0][0]) in S]
    for i, (m, name) in enumerate(models):
        for j, (q, lab, col, mk, hol) in enumerate(qs):
            cell = S[("fig02", m, q)]
            x = i + (j - 1.5) * 0.17
            mark(b, x, cell, col, hol, mk, value=(j == 0), whisker=(j == 0))
            if i == 0 and j:
                b.text(x, cell[0] + 0.05, lab, rotation=90, fontsize=ST.SMALL, color=col, ha="center", va="bottom")
    b.set_xticks(range(len(models)), [n for _, n in models])
    band(b, -0.10, 0.10, "not needed")
    b.set_ylim(-0.12, 0.85)
    b.set_ylabel("recall: switches lost beyond a random part")
    save(
        fig,
        "p2_controls",
        "**Same-size parts do not do it.** Left (Zach, pp): recalled minus stated answers lost "
        "without the lens part's top-10 J++ directions over his band (dark, 95% whiskers) against rotated directions, "
        "the logit lens's top 10 and same-norm PCA directions (grey), on the three clean models (docs/breadth/data.csv "
        "ko.*.mk / rot / u / pc); band ±5 pp. Right (Dan, share): the recall's switches lost beyond a random part "
        "without the lens part's 25 directions (teal, whiskers) against same-size PCA, the logit lens's directions and "
        "random lens directions (figures/story/data.csv fig02 rows; main test at L, 200 scenes); band ±0.10. On the "
        "122B the PCA control is close (0.21 vs 0.26). Lightning has no fig02 row (not on the axis).",
    )


# ---- P3: graded across nine models ----------------------------------------------------------------------------------
GRADE = ("clean", "clean", "clean", "weak", "weak", "not specific", "carried, not needed", "shared with logit lens",
         "by probability")  # fmt: skip


def p3() -> None:
    fig, ax = ST.figure()
    for i, ((m, name), word) in enumerate(zip(ST.ZACH, GRADE, strict=True)):
        mk = B[f"ko.{m}.mk"]
        ctrl = max(v for v in _ctrl(m) if v is not None)
        ax.vlines(i, ctrl, mk[0], color=C["light"], lw=4, zorder=1)
        mark(ax, i, mk, C["recall"], fmt="{:.1f}")
        ax.plot(i, ctrl, "o", ms=9, mfc="white", mec=C["random"], mew=2)
        ax.text(i, -0.1, "\n".join(textwrap.wrap(word, 11)), ha="center", va="top", fontsize=ST.SMALL, color=C["random"],
                transform=ax.get_xaxis_transform())  # fmt: skip
        if m == "q122":
            soft = B["ko.q122.soft"]
            ax.plot(i + 0.2, soft[0], "o", ms=8, mfc="white", mec=C["recall"], mew=1.5)
            ax.text(i + 0.3, soft[0], f"{soft[0]:.1f} by probability", fontsize=ST.SMALL, va="center")
        if i == 0:
            ax.text(i + 0.15, ctrl, "largest control", fontsize=ST.SMALL, color=C["random"], va="center")
    ax.axhline(30, color="black", ls="--", lw=1)
    ax.text(len(ST.ZACH) - 0.5, 31, "the plan's bar", ha="right", fontsize=ST.SMALL)
    ax.set_xticks(range(len(ST.ZACH)), [n for _, n in ST.ZACH])
    ax.set_ylim(-5, 70)
    ax.set_ylabel("recalled minus stated answers lost (pp)")
    save(
        fig,
        "p3_graded_nine",
        "**Across nine models it is graded.** Zach's removal of the lens part's top-10 J++ "
        "directions over his band: recalled minus stated answers lost (dark, 95% whiskers; docs/breadth/data.csv "
        "ko.*.mk) against the largest same-size control (open grey: max of rotated, logit lens, PCA / size-matched); "
        "the grade under each model in Zach's words; the 122B's effect scored by probability beside (ko.q122.soft). "
        "Gemma 4, gpt-oss and Kolibri cannot be tested (the removal breaks plain text) and are not on the axis.",
    )


# ---- P4: a pointer to the entity, not its fact ----------------------------------------------------------------------
def p4() -> None:
    fig = plt.figure(figsize=ST.FULL, dpi=ST.DPI, constrained_layout=True)
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 1.5])
    conds = ("own passage", "neutral sentence", "no own-word dirs", "rotated", "probe subspace")
    ax0 = None
    for k, (m, name) in enumerate(ST.ZACH[:3]):
        ax = fig.add_subplot(gs[0, k], sharey=ax0)
        ax0 = ax0 or ax
        own = B[f"ptr.{m}.swap"]
        vals = [own, (own[0] * B[f"ptr.{m}.neutral"][0], None, None, ""), (own[0] * B[f"ptr.{m}.noown"][0], None, None, ""),
                B[f"ptr.{m}.rot"], B[f"probe.{m}.probe"]]  # fmt: skip
        for j, cell in enumerate(vals):
            col = C["lookup"] if j == 4 else C["random"] if j == 3 else C["lens"]
            mark(ax, j, cell, col, fmt="{:.0f}", dx=0.15)
        ax.set_xticks(range(5), conds, rotation=45, ha="right")
        ax.set_ylim(-5, 100)
        ax.text(0.5, 0.97, name, transform=ax.transAxes, ha="center", va="top", fontsize=ST.SERIES)
        if k == 0:
            ax.set_ylabel("answers moved to D's fact (points)")
        else:
            ax.tick_params(labelleft=False)
    b = fig.add_subplot(gs[0, 3])
    parts = (("52 A: share of the rebuilt energy, the old bridge word", "old bridge word", C["recall"]),
             ("52 A: share of the rebuilt energy, the new bridge word", "new bridge word", C["lens"]),
             ("52 A: share of the rebuilt energy, an answer word", "answer word", C["address"]),
             ("52 A: share of the rebuilt energy, another scene word or its class", "another scene word", C["random"]),
             ("52 A: share of the rebuilt energy, no scene word", "no scene word", C["light"]))  # fmt: skip
    models = [(m, n) for m, n in ST.DAN if ST.find(S, m, parts[0][0])]
    ends = []
    for i, (m, name) in enumerate(models):
        bottom = 0.0
        for q, lab, col in parts:
            v = ST.find(S, m, q)[0]
            b.bar(i, v, 0.6, bottom=bottom, color=col, hatch="//" if ST.hollow(m) else None, edgecolor="white")
            if lab == "answer word":
                b.text(i, 1.02, f"{v:.2f}", ha="center", fontsize=ST.SMALL, color=C["address"])
            if i == len(models) - 1:
                ends.append([bottom + v / 2, lab])
            bottom += v
    for k in range(1, len(ends)):  # stagger the labels
        ends[k][0] = max(ends[k][0], ends[k - 1][0] + 0.075)
    for y, lab in ends:
        b.text(len(models) - 0.6, y, lab, fontsize=ST.SMALL, va="center")
    b.text(-0.3, 1.08, "answer word:", fontsize=ST.SMALL, color=C["address"], va="bottom")
    b.set_xticks(range(len(models)), [n for _, n in models], rotation=25, ha="right")
    b.set_xlim(-0.5, len(models) + 1.3)
    b.set_ylim(0, 1.15)
    b.set_ylabel("share of the lens part's rebuilt energy")
    save(
        fig,
        "p4_c2_pointer",
        "**C2. The lens part says which entity it is: a pointer, from any context, not its "
        "fact.** Left (Zach, points): another entity D's lens part written in; answers moved to D's fact when the part "
        "comes from D's own passage (with 95% whiskers), from one neutral sentence about D, without D's own-word "
        "directions, the neutral donor rotated (grey), and a probe's subspace that reads the fact (purple; on "
        "probe-valid relations). docs/breadth/data.csv ptr.*.swap / rot, probe.*.probe; the neutral and own-word "
        "points are ptr.*.swap times the stored ratios ptr.*.neutral / noown (computed here, no interval). The "
        "cross-relation and paste rows are dropped. Right (Dan, share): what the lens part's 25 directions are, main "
        "test at L, 50 scenes per model (figures/story/data.csv 52 A rows); Lightning hatched (gate chosen after its "
        "pre-check; pending hand-check, 29 Oct); the 122B has no 52 A row in the depth README (not on the axis).",
    )


# ---- P7: where it breaks --------------------------------------------------------------------------------------------
def p7() -> None:
    fig, (a, b) = ST.figure(ncols=2)
    for m, name, col in (("27b", "Qwen 27B", C["lookup"]), ("122b", "Qwen 122B", C["random"])):
        ks = (25, 50, 100)
        vs = [X[f"lk_excess_k{k}_{m}"][0] for k in ks]
        a.plot(ks, vs, "-o", color=col, ms=8, lw=2)
        for k, v in zip(ks, vs, strict=True):
            a.text(k, v + 0.03, f"{v:.2f}", ha="center", fontsize=ST.VALUE, color=col)
        a.text(103, vs[-1], name, va="center", fontsize=ST.SERIES, color=col)
    band(a, -0.10, 0.10)
    a.axhline(0, color="black", lw=0.6)
    a.set_xticks((25, 50, 100))
    a.set_xlim(20, 125)
    a.set_xlabel("lens directions taken out")
    a.set_ylabel("lookup: switches lost beyond a random part")
    models = ST.DAN[:4]
    for i, (m, name) in enumerate(models):
        for j, facts in enumerate(("true facts", "made-up facts")):
            cell = S.get(
                ("ledger_zach_named", m, f"Zach's named passages, {facts}, lookup: switches lost beyond random")
            )
            if not cell:
                continue
            x = i + (j - 0.5) * 0.36
            b.bar(x, cell[0], 0.34, color="white" if j else C["lookup"], edgecolor=C["lookup"], lw=2,
                  hatch="//" if ST.hollow(m) and not j else None)  # fmt: skip
            b.text(x, max(cell[0], 0) + 0.015, f"{cell[0]:.2f}", ha="center", fontsize=ST.SMALL)
            if i == 0:
                b.text(x + (-0.08 if not j else 0.08), -0.14, "true" if not j else "made-up", ha="right" if not j else "left",
                       fontsize=ST.SMALL, color=C["lookup"])  # fmt: skip
    band(b, -0.10, 0.10, "not needed")
    b.axhline(0, color="black", lw=0.6)
    b.set_xticks(range(len(models)), [n for _, n in models])
    b.set_ylim(-0.16, 0.7)
    b.set_ylabel("lookup: switches lost beyond a random part")
    save(
        fig,
        "p7_breaks",
        "**Where it breaks.** Left: the lookup's switches lost beyond a random part without 25 / 50 "
        "/ 100 lens directions, main test at L (docs/x0_numbers.json lk_excess_k*_27b / _122b; 200 scenes); the 27B "
        "loses 0.60 at 100, the 122B nothing. Right: Zach's named passages run through Dan's conflict test, the "
        "lookup's loss with true facts (filled) vs made-up facts (open) (figures/story/data.csv ledger_zach_named); on "
        "true facts the lookup can answer from memory. Muse and Lightning missed the made-up-fact gate: descriptive; "
        "Lightning hatched (pending hand-check, 29 Oct).",
    )


# ---- P0a, P0b: the setup --------------------------------------------------------------------------------------------
def p0() -> None:
    img = mpimg.imread(ST.REPO / "figures/shared/j0_setup.png")
    half = img.shape[0] // 2
    for name, part, what in (
        ("p0a_datasets", img[:half], "the two datasets"),
        ("p0b_tools", img[half:], "the three tools"),
    ):
        fig = plt.figure(figsize=ST.FULL, dpi=ST.DPI)
        ax = fig.add_axes((0, 0, 1, 1))
        ax.imshow(part)
        ax.set_axis_off()
        save(
            fig,
            name,
            f"**Setup: {what}.** figures/shared/j0_setup.png, its {'top' if 'a_' in name else 'bottom'} half "
            "placed on the slide canvas (not re-drawn: its text size is the shared figure's).",
        )


# ---- P8: where (Zach's Finding 5) -----------------------------------------------------------------------------------
def p8() -> None:
    fig, (a, b) = ST.figure(ncols=2, sharey=True)
    cols = (("all tokens", C["recall"]), ("the mention only", C["lens"]), ("the question only", C["lookup"]))
    mid = [
        (m, n, [B.get(f"pos.{m}.all.all"), B.get(f"pos.{m}.all.bridge"), B.get(f"pos.{m}.all.question")])
        for m, n in ST.ZACH[:3]
    ]
    late = [
        (m, n, [B.get(f"late.{m}.all"), B.get(f"late.{m}.bridge"), B.get(f"late.{m}.question")]) for m, n in ST.ZACH[:3]
    ]
    late.append(("mu", "Muse 30B", [B.get("ko.mu.mk"), B.get("pos.mu.bridge"), B.get("pos.mu.question")]))
    for ax, rows in ((a, mid), (b, late)):
        for i, (m, n, cells) in enumerate(rows):
            for j, ((lab, col), cell) in enumerate(zip(cols, cells, strict=True)):
                if cell is None:
                    continue
                x = i + (j - 1) * 0.27
                ax.bar(x, cell[0], 0.25, color=col)
                ax.text(x, cell[0] + 1, f"{cell[0]:.1f}", ha="center", fontsize=ST.SMALL)
                if i == 0:
                    ax.text(
                        x, cell[0] / 2, lab, rotation=90, ha="center", va="center", color="white", fontsize=ST.SMALL
                    )
        ax.set_xticks(range(len(rows)), [n for _, n, _ in rows])
        ax.text(
            0.02,
            0.97,
            "middle layers" if ax is a else "deeper layers",
            transform=ax.transAxes,
            va="top",
            fontsize=ST.SERIES,
        )
    a.set_ylim(0, 70)
    a.set_ylabel("recalled minus stated answers lost (pp)")
    save(
        fig,
        "p8_where",
        "**Backup B1. At middle layers the bridge's mention carries it; deeper, the question does** "
        "(Zach's Finding 5). The lens part removed at all tokens, at the bridge's mention only, or in the question "
        "only, over a middle and a deeper band (docs/breadth/data.csv pos.*.all.*, late.*); Muse 30B tested only at "
        "layers 36-42 (deeper panel: ko.mu.mk, pos.mu.bridge, pos.mu.question). Fixed in advance; rotated controls "
        "cost at most 2.5 points.",
    )


# ---- P9: routes (j8) ------------------------------------------------------------------------------------------------
def p9() -> None:
    fig, ax = ST.figure(ST.HALF)
    parts = (("identity", C["identity"]), ("position", C["address"]), ("value", C["recall"]))
    models = [(m, n) for m, n in ST.DAN if ST.find(S, m, "another item moved, whole: identity share")]
    for i, (m, name) in enumerate(models):
        bottom = 0.0
        for lab, col in parts:
            v = ST.find(S, m, f"another item moved, whole: {lab} share")[0]
            ax.bar(i, v, 0.6, bottom=bottom, color=col, hatch="//" if ST.hollow(m, lowered_test=True) else None,
                   edgecolor="white")  # fmt: skip
            if v > 0.06:
                ax.text(i, bottom + v / 2, f"{v:.2f}", ha="center", va="center", color="white", fontsize=ST.SMALL)
            if i == len(models) - 1:
                ax.text(i + 0.35, bottom + max(v, 0.02) / 2, lab, fontsize=ST.SMALL, va="center")
            bottom += v
    ax.set_xticks(range(len(models)), [n for _, n in models], rotation=25, ha="right")
    ax.set_xlim(-0.5, len(models) + 0.4)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("lookups switched by the whole change (share)")
    save(
        fig,
        "p9_routes",
        "**Backup B2. The lookup goes by identity or position, never the value.** Routes test "
        "(another item moved), the whole change at L: shares of switched lookups naming the item's own locker "
        "(identity), the locker now at its old place (position) or the new number (value); 300 scenes per model "
        "(figures/story/data.csv fig05 rows). Lightning hollow; the 122B hollow (gate lowered to 0.75 after the "
        "data).",
    )


FIGS = {"p0": p0, "p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5, "p6": p6, "p7": p7, "p8": p8, "p9": p9}


def contact_sheet() -> None:
    pngs = sorted(p for p in ST.OUT.glob("p*.png"))
    if not pngs:
        return
    n = len(pngs)
    cols = 2
    rows = (n + 1) // cols
    fig, axs = plt.subplots(rows, cols, figsize=(16, 3.6 * rows), squeeze=False)
    for ax in axs.flat:
        ax.set_axis_off()
    for ax, p in zip(axs.flat, pngs, strict=False):
        ax.imshow(mpimg.imread(p))
        ax.text(0, -0.02, p.name, transform=ax.transAxes, fontsize=12, va="top")
    fig.savefig(ST.OUT / "contact_sheet.png", dpi=80, facecolor="white")
    plt.close(fig)
    print("wrote", ST.OUT / "contact_sheet.png")


def write_captions() -> None:
    path = ST.OUT / "CAPTIONS.md"
    old = {}
    if path.exists():
        for block in path.read_text().split("\n## ")[1:]:
            k, _, body = block.partition("\n")
            old[k.strip()] = body.strip()
    old.update(CAPTIONS)
    text = "# presentation/: captions (the speaker notes)\n\nBuilt by `uv run python presentation/build.py`; every number on a figure is read from its source row. One block per figure.\n"
    text += "".join(f"\n## {k}\n\n{v}\n" for k, v in sorted(old.items()))
    path.write_text(text)


def main(names: list[str]) -> None:
    for n in names or list(FIGS):
        FIGS[n]()
    write_captions()
    contact_sheet()


if __name__ == "__main__":
    main(sys.argv[1:])
