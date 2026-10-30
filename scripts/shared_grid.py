"""shared_grid (agent, 27 Oct; Dan ~14:40): the joint grid of both studies, claims x the nine models, every cell with its
source.

  docs/shared/grid.csv        one row per (claim, model, study): cell (ok / ~ / x / - / pending), flag (a: after the
                              data; *: not counted), source file, source row, the model's name in that source, its key(s)
                              and the value(s) behind the cell
  figures/shared/grid.png     the claims graded on all nine models (both tracks' shared claims, Zach's tests)
  figures/shared/grid_dan.png Dan's own tests on his four models; both in coloured cells with Fig. 11's symbols
                              (readme_story_figures.CELL_SYMBOL) inside, short claims in the joint vocabulary (FIGURES)

The two sources, never merged:
  depth (Dan's half)    data/figures/depth/scorecard.csv: cell and flag copied; its 'data.csv key' resolves in
                        docs/depth/x0_numbers.json ('numbers:') or data/figures/depth/data.csv ('figNN:'), whose value is shown.
  breadth (Zach's half) docs/breadth/data.csv: one verdict per model by the rules on Zach's scorecard (scripts/fig_neel.py
                        f12, its note), one rule per row of BREADTH_RULES; a model whose data.csv lacks a rule's key is
                        '-'. Fixed in advance as in his prereg (docs/breadth/prereg_replication_1022.md); 'a' where it says not.
Where both halves grade the same claim (SHARED), the figure gives it two strips, Dan's above Zach's.
Columns: depth's four models first (story_style.MODELS), then the breadth's other five in its table's order.

uv run python scripts/shared_grid.py      (CPU only; reads the three files, writes the grid and the figure)
"""

from __future__ import annotations

import csv
import json
import sys
import textwrap
from collections.abc import Callable
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts import readme_story_figures as F  # noqa: E402
from scripts import story_style as S  # noqa: E402

SCORECARD = REPO / "data" / "figures" / "depth" / "scorecard.csv"
DEPTH_DATA = REPO / "data" / "figures" / "depth" / "data.csv"
BREADTH_DATA = REPO / "docs" / "breadth" / "data.csv"
GRID = REPO / "docs" / "shared" / "grid.csv"
FIG_DIR = REPO / "figures" / "shared"
FIELDS = ("group", "claim", "model", "study", "cell", "flag", "source", "source row", "model key", "key", "value")

# (header name, scorecard.csv model, breadth data.csv model); names as each README writes them
MODELS = (
    ("Qwen3.5-9B", "Qwen3.5-9B", "q9"),
    ("Qwen3.6-27B", "Qwen3.6-27B", "q27"),
    ("Qwen3.5-122B-A10B (FP8)", "Qwen3.5-122B", "q122"),
    ("Muse Glimmer 30B", "Muse Glimmer 30B", "mu"),
    ("Nemotron 3.5 Lightning", None, "nl"),
    ("DeepSeek-V4-Flash", None, "ds"),
    ("Ministral-3-14B", None, "mi"),
    ("Nemotron 3.5 Bolt", None, "nb"),
    ("OLMo-3-32B base", None, "ol"),
)
GROUPS = ("Both studies (a split cell: depth | breadth)", "Depth (Dan): the bridge word in locker scenes",
          "Breadth (Zach): the bridge's fact in passages")  # fmt: skip
RECALL = "recall needs the J++ part; reading the prompt does not"
MARGIN = "not a margin effect (depth: logit difference; breadth: probability)"
# the same claim in both halves: grid claim -> depth's scorecard claim (breadth's is the BREADTH_RULES row of that claim)
SHARED = {RECALL: "main test", MARGIN: "logit difference"}


def band(v: float, hold: float, partial: float) -> str:
    return "ok" if v >= hold else "~" if v >= partial else "x"


def swap_key(m: str) -> str:
    """Zach's scorecard: Bolt's swap with 100 directions, DeepSeek's and Ministral's at mid depth (the only swaps run)."""
    return {"nb": "swap.nb.k100.swap", "ds": "swap.ds.mid.swap", "mi": "swap.mi.mid.swap"}.get(m, f"swap.{m}.swap")


# (grid claim, Zach's column (README section 7), keys of a model, verdict from the keys' values, flag)
BREADTH_RULES: tuple[tuple[str, str, Callable[[str], list[str]], Callable[..., str], str], ...] = (
    ("testable: the removal adds < 2 nats on plain text", "plain-text cost",
     lambda m: [f"text.{m}"], lambda t: "ok" if t < 2 else "x", ""),
    (RECALL, "M − K (top 10)", lambda m: [f"ko.{m}.mk"], lambda d: band(d, 30, 15), ""),
    ("specific: rotated and logit-lens removals cost < 10", "rotated / logit lens",
     lambda m: [f"ko.{m}.rot", f"ko.{m}.u"], lambda r, u: "ok" if max(r, u) < 10 else "x", ""),
    ("not variance: PCA directions (same size) cost ≤ 1/3 as much", "size-matched (share)",
     lambda m: [f"ko.{m}.pcr"], lambda s: "ok" if s <= 1 / 3 else "x" if s >= 2 / 3 else "~", ""),
    # amendment 48 A: probability scoring post hoc, all numbers seen; the 60% bar is the scorecard's
    (MARGIN, "by probability", lambda m: [f"ko.{m}.soft", f"ko.{m}.mk"], lambda p, d: "ok" if p >= 0.6 * d else "x", "a"),
    ("two more renderings: each within 10 of the first", "renderings",
     lambda m: [f"ko.{m}.mk", f"ko.{m}.r2", f"ko.{m}.r3"], lambda d, a, b: "ok" if max(abs(a - d), abs(b - d)) <= 10 else "x", ""),
    ("not the bridge's own word: keeping those directions restores < 0.75", "keep-own restores",
     lambda m: [f"keepown.{m}"], lambda k: "ok" if k < 0.75 else "x", ""),
    ("another entity's J++ part moves the answer (≥ 20 points)", "J-part swap / paste",
     lambda m: [swap_key(m)], lambda s: band(s, 20, 10), ""),
    ("context-free: a neutral sentence's J++ part moves ≥ 2/3 as much", "neutral donor",
     lambda m: [f"ptr.{m}.neutral"], lambda r: "ok" if r >= 2 / 3 else "x", ""),
    ("readable is not carried: a probe's subspace moves ≤ 1/3 as much", "probe swap (J++ / probe)",
     lambda m: [f"probe.{m}.swap", f"probe.{m}.probe"], lambda a, b: "ok" if b <= a / 3 and a >= 20 else "~", ""),
)  # fmt: skip


# EXPERIMENTS.md l.167 / l.169: the v2 knock-outs on the 122B and Muse were not pre-registered
AFTER_V2_KNOCKOUT = ("q122", "mu")


def breadth_flag(flag: str, m: str, keys: list[str]) -> str:
    """The rule's flag, or 'a' where the cell reads a v2 knock-out that was run after the data."""
    return "a" if flag == "a" or (m in AFTER_V2_KNOCKOUT and any(k.startswith("ko.") for k in keys)) else flag


def read_csv(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def breadth_rows() -> dict[tuple[str, str], dict]:
    """(model, key) -> docs/breadth/data.csv row."""
    return {(r["model"], r["key"]): r for r in read_csv(BREADTH_DATA)}


def breadth_value(r: dict) -> str:
    v, u = float(r["value"]), r["unit"]
    s = f"{v:.2f}" if u in ("ratio", "nats") else f"{v:+.1f}"
    return f"{r['key']} {s}" + (f" [{r['lo']}, {r['hi']}]" if r["lo"] != "" else "")


def depth_value(key: str, target: str, numbers: dict, recorded: dict) -> str:
    """The value a scorecard key names: an x0_numbers text, or a data/figures/depth/data.csv row of that model."""
    fig_id, quantity = key.split(":", 1)
    if fig_id == "numbers":
        return numbers[quantity]["text"]
    r = recorded[(fig_id, target, quantity)]
    return r["value"] + (f" [{r['lo']}, {r['hi']}]" if r["lo"] != "" else "")


def build() -> list[dict]:
    """The grid's rows, in drawing order: the shared claims, depth's other claims (scorecard order), breadth's."""
    card = read_csv(SCORECARD)
    targets = {name: target for target, _, name in S.MODELS}
    assert {r["model"] for r in card} <= set(targets), "scorecard.csv has a model this grid has no column for"
    cells = {(r["claim"], r["model"]): r for r in card}
    numbers = json.loads(S.NUMBERS.read_text())
    recorded = {(r["figure"], r["model"], r["quantity"]): r for r in read_csv(DEPTH_DATA)}
    zach = breadth_rows()
    rules = {rule[0]: rule for rule in BREADTH_RULES}

    def depth(group: str, claim: str, card_claim: str) -> list[dict]:
        out = []
        for header, name, _ in MODELS:
            r = cells.get((card_claim, name)) if name else None
            row = {"group": group, "claim": claim, "model": header, "study": "depth", "cell": "-", "flag": "",
                   "source": "data/figures/depth/scorecard.csv", "source row": card_claim, "model key": name or "", "key": "", "value": ""}  # fmt: skip
            if name is not None and r is not None:
                row.update(cell=r["cell"], flag=r["flag"], key=r["data.csv key"])
                if r["data.csv key"]:
                    row["value"] = depth_value(r["data.csv key"], targets[name], numbers, recorded)
            out.append(row)
        return out

    def breadth(group: str, claim: str) -> list[dict]:
        _, column, keys_of, verdict, flag = rules[claim]
        out = []
        for header, _, m in MODELS:
            keys = keys_of(m)
            got = [zach[(m, k)] for k in keys if (m, k) in zach]
            row = {"group": group, "claim": claim, "model": header, "study": "breadth", "cell": "-", "flag": "",
                   "source": "docs/breadth/data.csv", "source row": column, "model key": m, "key": "", "value": ""}  # fmt: skip
            if len(got) == len(keys):  # a rule is graded only where data.csv holds every key it reads
                row.update(cell=verdict(*[float(r["value"]) for r in got]), flag=breadth_flag(flag, m, keys), key="; ".join(keys),
                           value="; ".join(breadth_value(r) for r in got))  # fmt: skip
            out.append(row)
        return out

    rows = []
    for claim, card_claim in SHARED.items():
        rows += depth(GROUPS[0], claim, card_claim) + breadth(GROUPS[0], claim)
    for card_claim in dict.fromkeys(r["claim"] for r in card):
        if card_claim not in SHARED.values():
            rows += depth(GROUPS[1], card_claim, card_claim)
    for claim, *_ in BREADTH_RULES:
        if claim not in SHARED:
            rows += breadth(GROUPS[2], claim)
    return rows


def write(rows: list[dict]) -> None:
    GRID.parent.mkdir(parents=True, exist_ok=True)
    with GRID.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(FIELDS))
        w.writeheader()
        w.writerows(rows)


# ------------------------------------------------------------------------------------------------- the two figures
# Redesigned for readers (Dan ~16:05): coloured cells with the symbol inside, a corner mark for "after the data", short
# claims in the joint vocabulary (the full wording and every source stay in grid.csv), row groups in the README's order,
# split rows (both tracks on one claim) as two labelled strips. Thirty claims x nine models did not read at 880 px, so the
# grid is two figures: grid.png, the claims graded on all nine models (both tracks' shared claims and Zach's tests), and
# grid_dan.png, Dan's own tests on his four models.
SHORT = {"q9": "Qwen 9B", "q27": "Qwen 27B", "q122": "Qwen 122B", "mu": "Muse 30B", "nl": "Nemotron Lightning",
         "ds": "DeepSeek V4 Flash", "mi": "Ministral 14B", "nb": "Nemotron Bolt", "ol": "OLMo 32B base"}  # fmt: skip
FILL = {"ok": "#d5ebdb", "~": "#f6e5c0", "x": "#f3d2cd", "-": "#eeeeee", "pending": "#eeeeee"}
AFTER_MARK = "#4a4a4a"
SWAP_CLAIM = "another entity's J++ part moves the answer (≥ 20 points)"
# figure -> (title, subtitle, model codes, groups of (group title, ((short label, grid.csv claim), ...)), footnote)
FIGURES: dict[str, tuple[str, str, tuple[str, ...], tuple[tuple[str, tuple[tuple[str, str], ...]], ...], str]] = {
    "grid": (
        "Only Qwen 9B, Qwen 27B and Nemotron Lightning pass every Zach check",
        "Dan's tool: remove from the patch. Zach's: remove everywhere and swap.",
        ("q9", "q27", "nl", "mu", "q122", "ds", "mi", "nb", "ol"),
        (("1. Recalled vs lookup answers", (
            ("recalled answers need the\nlens part, lookup ones not", RECALL),
            ("not a margin effect", MARGIN),
            ("beats rotated and logit lens", "specific: rotated and logit-lens removals cost < 10"),
            ("beats a same-size PCA removal", "not variance: PCA directions (same size) cost ≤ 1/3 as much"))),
         ("2. What the swap moves", (
            ("swap moves the recalled answer", SWAP_CLAIM),
            ("works from a neutral sentence", "context-free: a neutral sentence's J++ part moves ≥ 2/3 as much"),
            ("a probe's subspace moves little", "readable is not carried: a probe's subspace moves ≤ 1/3 as much"))),
         ("Checks of remove everywhere", (
            ("costs plain text under 2 nats", "testable: the removal adds < 2 nats on plain text"),
            ("holds on two more renderings", "two more renderings: each within 10 of the first"),
            ("not the bridge's own word", "not the bridge's own word: keeping those directions restores < 0.75")))),
        "Nemotron Bolt's swap: with 100 directions (with 10: +3). DeepSeek's and Ministral's swaps: at mid depth.",
    ),
    "grid_dan": (
        "An order signal steers lookup answers on three of four models",
        "Dan's own tests on his four models: remove from the patch, the order signal, writes.",
        ("q9", "q27", "mu", "q122"),
        (("1. Recalled vs lookup answers: more scenes", (
            ("clean one-pick scenes", "clean one-pick scenes"),
            ("the locker sentence before the pick", "locker before the pick"))),
         ("3. What lookup answers use", (
            ("never the bridge's value", "never the value"),
            ("removing the order signal stops position answers", "the lookup needs it"),
            ("only the order signal gives position answers", "only it gives position answers"),
            ("writing the order signal moves the answer", "a write moves the lookup"),
            ("the recalled answer follows the write", "the recall follows the write"),
            ("it counts mentions, not text position", "counts mentions, not text position"),
            ("a pick sentence first switches to identity", "a pick sentence first moves the lookup to identity"),
            ("a refit order signal found per format", "refit per format"),
            ("the fit on simple scenes transfers", "the pointer fit on simple scenes transfers"),
            ("identity outside the lens is specific", "identity outside J++ is specific"))),
         ("Robustness", (
            ("varied scenes: prose, JSON, table", "varied scenes"),
            ("natural passages", "natural passages"),
            ("without the chat template", "without the chat template"),
            ("never the value, without the chat template", "never the value without the chat template"))),
         ("Internals of remove from the patch", (
            ("a cause for Qwen 27B's loss at 100 directions", "a tested cause for the 27B's loss with 100 directions"),
            ("the recalled answer needs only the lens part", "the recall needs only the J++ part, locker after the pick"),
            ("the recalled answer reads the earlier mention", "the recall reads the earlier mention, locker before the pick"),
            ("the link sits in the locker sentences", "the link sits in the locker sentences, clean one-pick scenes")))),
        "*Muse 30B, natural passages: too few switches to count ({n_sw} of {n}).",
    ),
}  # fmt: skip
STRIP, GROUP_GAP = 0.34, 1.25  # inches per strip; a group title's height in strips


def legend_strip(fig, y_in: float, h: float) -> None:
    """The legend at the top: a sample cell per state, then the corner mark."""
    lax = fig.add_axes((0.0, 1 - (y_in + 0.32) / h, 1.0, 0.32 / h))
    lax.set_xlim(0, 100)
    lax.set_ylim(0, 1)
    lax.axis("off")
    lax.set_xticks([])
    lax.set_yticks([])
    items = (("ok", "held"), ("~", "partial"), ("x", "no"), ("-", "not tested"), ("ok", "after the data"))
    for k, (cell, text) in enumerate(items):
        x = 1 + 19 * k
        lax.add_patch(plt_rect((x, 0.08), 4.4, 0.84, FILL[cell]))
        sym, col = F.CELL_SYMBOL[cell]
        lax.text(x + 2.2, 0.5, sym, ha="center", va="center", fontsize=S.FONT + 1, color=col, weight="bold")
        if text == "after the data":
            corner(lax, x + 4.4, 0.92, 1.3, 0.38)
        lax.text(x + 5.6, 0.5, text, va="center", fontsize=S.FONT)


def plt_rect(xy: tuple[float, float], w: float, h: float, fc: str):
    from matplotlib.patches import Rectangle

    return Rectangle(xy, w, h, fc=fc, ec="none", lw=0, zorder=1)


def corner(ax, x1: float, ytop: float, w: float, h: float) -> None:
    """The after-the-data mark: a dark triangle in a cell's top-right corner (h is signed along the axis' y)."""
    from matplotlib.patches import Polygon

    ax.add_patch(Polygon([(x1, ytop), (x1 - w, ytop), (x1, ytop - h)], closed=True, fc=AFTER_MARK, ec="none", zorder=3))


def draw(plt, rows: list[dict], name: str = "grid"):
    """One of the two grid figures: groups of claims (rows) x models (columns); a coloured cell per grade with Fig. 11's
    symbol inside, a corner mark for after the data; a claim graded by both tracks gets two strips, Dan's and Zach's."""
    title, sub, codes, groups, foot = FIGURES[name]
    cells = {(r["claim"], code_of(r), r["study"]): r for r in rows}
    by_claim: dict[str, list[str]] = {}
    for r in rows:
        if r["study"] not in by_claim.setdefault(r["claim"], []):
            by_claim[r["claim"]].append(r["study"])
    staggered = len(codes) > 4  # nine names do not fit side by side: alternate columns' names stand one tier higher
    # vertical layout in strips: a group title, then per claim one strip per track that graded it
    y, heads, places = 0.0, [], []
    for gtitle, items in groups:
        heads.append((gtitle, y + GROUP_GAP * 0.55))
        y += GROUP_GAP
        for short, claim in items:
            tracks = [s for s in ("depth", "breadth") if s in by_claim[claim]]
            places.append((short, claim, tracks, y))
            y += len(tracks)
    sub_lines = sub.count("\n") + 1
    names_in = 1.2 if staggered else 0.45
    top_in = 0.5 + 0.2 * sub_lines + 0.5 + names_in
    n_sw, n = S.numbers().get("nat_lk_whole_sw_muse"), S.numbers().get("nat_n_muse")
    foot = foot.format(n_sw=n_sw, n=n)
    bottom_in = 0.25 + 0.2 * (foot.count("\n") + 1)
    h = top_in + STRIP * y + bottom_in
    left, right = (0.31, 0.975) if staggered else (0.47, 0.98)
    fig = plt.figure(figsize=(S.WIDTH, h))
    ax = fig.add_axes((left, bottom_in / h, right - left, STRIP * y / h))
    S.title(fig, title, sub)
    legend_strip(fig, 0.5 + 0.2 * sub_lines + 0.05, h)
    fig.text(0.01, 0.12 / h, foot, fontsize=S.FONT, color=S.COL["muted"], va="bottom")
    ax.set_xlim(-0.5, len(codes) - 0.5)
    ax.set_ylim(y, 0)
    ax.axis("off")
    ax.set_xticks([])
    ax.set_yticks([])
    for j, code in enumerate(codes):
        upper = staggered and j % 2 == 1
        name = textwrap.fill(SHORT[code], 10) if staggered else SHORT[code]
        yb = -1.65 if upper else -0.15
        ax.text(j, yb, name, ha="center", va="bottom", fontsize=S.FONT, weight="bold", linespacing=1.0)
        if upper:  # a leader down to its column, between the lower tier's names
            ax.plot([j, j], [yb + 0.05, -0.08], color="#b5b5b5", lw=0.8, clip_on=False)
    tr = F.blend(fig, ax)
    for gtitle, gy in heads:
        ax.text(0.01, gy, gtitle, transform=tr, fontsize=S.FONT + 1, weight="bold", va="center")
    for k, (short, claim, tracks, y0) in enumerate(places):
        if k % 2 == 0:
            ax.add_patch(plt.Rectangle((-0.5 - 20, y0), len(codes) + 20, len(tracks), fc="#f7f7f7", ec="none", zorder=0,
                                       clip_on=False))  # fmt: skip
        ax.text(0.01, y0 + len(tracks) / 2, short, transform=tr, fontsize=S.FONT, va="center", linespacing=1.1)
        for t, study in enumerate(tracks):
            yc = y0 + t + 0.5
            if len(tracks) == 2:
                ax.text(-0.56, yc, "Dan" if study == "depth" else "Zach", ha="right", va="center", fontsize=S.FONT,
                        color=S.COL["muted"])  # fmt: skip
            for j, code in enumerate(codes):
                r = cells.get((claim, code, study))
                cell, flag = (r["cell"], r["flag"]) if r else ("-", "")
                ax.add_patch(plt_rect((j - 0.45, yc - 0.42), 0.9, 0.84, FILL[cell]))
                sym, col = F.CELL_SYMBOL[cell]
                ax.text(j, yc, sym + ("*" if "*" in flag else ""), ha="center", va="center", fontsize=S.FONT + 1,
                        color=col, weight="bold")  # fmt: skip
                if "a" in flag:
                    corner(ax, j + 0.45, yc - 0.42, 0.24, -0.36)
    return fig


def code_of(r: dict) -> str:
    """The breadth data.csv model code of a grid row's column."""
    return {h: code for h, _, code in MODELS}[r["model"]]


def save(fig, name: str) -> None:
    """As story_style.save, into figures/shared."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{name}.png", dpi=200, facecolor="white")


def main() -> None:
    rows = build()
    write(rows)
    plt = S.setup()
    for name in FIGURES:
        fig = draw(plt, rows, name)
        save(fig, name)
        plt.close(fig)
    split = sum(1 for c in SHARED for _, name, _ in MODELS if name)
    print(f"{GRID.relative_to(REPO)}: {len(rows)} rows, {len(dict.fromkeys(r['claim'] for r in rows))} claims x "
          f"{len(MODELS)} models ({split} cells graded by both tracks); "
          f"{', '.join(f'figures/shared/{n}.png' for n in FIGURES)}")  # fmt: skip


if __name__ == "__main__":
    main()
