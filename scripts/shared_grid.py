"""shared_grid (agent, 27 Oct; Dan ~14:40): the joint grid of both studies, claims x the nine models, every cell with its
source.

  docs/shared/grid.csv        one row per (claim, model, study): cell (ok / ~ / x / - / pending), flag (a: after the
                              data; *: not counted), source file, source row, the model's name in that source, its key(s)
                              and the value(s) behind the cell
  figures/shared/grid.png     (+ .svg) the grid, in Fig. 11's symbols and colours (readme_story_figures.CELL_SYMBOL) and
                              story_style's type

The two sources, never merged:
  depth (Dan's half)    figures/story/scorecard.csv: cell and flag copied; its 'data.csv key' resolves in
                        docs/x0_numbers.json ('numbers:') or figures/story/data.csv ('figNN:'), whose value is shown.
  breadth (Zach's half) docs/breadth/data.csv: one verdict per model by the rules on Zach's scorecard (scripts/fig_neel.py
                        f12, its note), one rule per row of BREADTH_RULES; a model whose data.csv lacks a rule's key is
                        '-'. Fixed in advance as in his prereg (docs/prereg_replication_1022.md); 'a' where it says not.
Where both halves grade the same claim (SHARED), the cell is split: depth's mark on the left, breadth's on the right.
Columns: depth's four models first (story_style.MODELS), then the breadth's other five in its table's order.

uv run python scripts/shared_grid.py      (CPU only; reads the three files, writes the grid and the figure)
"""

from __future__ import annotations

import csv
import json
import re
import sys
import textwrap
from collections.abc import Callable
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts import readme_story_figures as F  # noqa: E402
from scripts import story_style as S  # noqa: E402

SCORECARD = REPO / "figures" / "story" / "scorecard.csv"
DEPTH_DATA = REPO / "figures" / "story" / "data.csv"
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
    """The value a scorecard key names: an x0_numbers text, or a figures/story/data.csv row of that model."""
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
                   "source": "figures/story/scorecard.csv", "source row": card_claim, "model key": name or "", "key": "", "value": ""}  # fmt: skip
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


def label(claim: str, width: int) -> str:
    """The claim wrapped, never between "J++" and the "part" / "lens" the glossary requires after it."""
    held = re.sub(r"J\+\+ (part|lens)", "J++\N{NO-BREAK SPACE}\\1", claim)  # textwrap breaks at ASCII whitespace only
    return textwrap.fill(held, width).replace("\N{NO-BREAK SPACE}", " ")


def draw(plt, rows: list[dict]):
    """The grid: rows = claims under their group, columns = MODELS; one Fig. 11 mark per cell, two (depth | breadth) in
    a shared claim's cell; 'a' (after the data) or '*' beside a mark."""
    claims = list(dict.fromkeys(r["claim"] for r in rows))
    group = {r["claim"]: r["group"] for r in rows}
    marks: dict[tuple[str, str], list[dict]] = {}
    for r in rows:
        marks.setdefault((r["claim"], r["model"]), []).append(r)
    wrap = 34
    ys, y, last, heads, half = {}, 0.0, None, [], {}
    for claim in claims:  # a heading row before each group; a two-line label gets a taller row
        if group[claim] != last:
            heads.append((group[claim], y))
            y -= 1.0
            last = group[claim]
        half[claim] = 0.5 + 0.15 * label(claim, wrap).count("\n")
        y -= half[claim] - 0.5
        ys[claim] = y
        y -= half[claim] + 0.5
    top_in, row_in = 3.1, 0.36  # the title block, then the model names standing over their columns
    h = top_in + row_in * (-y) + 0.75
    fig, ax = plt.subplots(figsize=(S.WIDTH, h))
    fig.subplots_adjust(left=0.375, right=0.99, top=1 - top_in / h, bottom=0.75 / h)
    S.title(fig, "What held where, both studies",
            "Depth (Dan): figures/story/scorecard.csv. Breadth (Zach): docs/breadth/data.csv,\n"
            "graded by his scorecard's rules. The first four models are in both studies.\n"
            "✓ held   ~ partial   ✗ no   – not tested*   a: after the data")  # fmt: skip
    n_sw, n = S.numbers().get("nat_lk_whole_sw_muse"), S.numbers().get("nat_n_muse")
    fig.text(0.01, 0.12 / h, f"*Not run or not counted. Depth, Muse, natural passages: the lookup has too few switches ({n_sw} of {n}).\n"
             "Breadth: Bolt's swap with 100 directions (with 10: +3); DeepSeek's and Ministral's swaps at mid depth.",
             color=S.COL["muted"], va="bottom")  # fmt: skip
    for j, (header, _, _) in enumerate(MODELS):
        ax.text(j, 0.65, textwrap.fill(header, 17), ha="center", va="bottom", rotation=90, fontsize=S.FONT, weight="bold",
                linespacing=1.0)  # fmt: skip
        for claim in claims:
            got = marks[(claim, header)]
            # the split cell: a box, depth's mark left of a rule and breadth's right of it, both shifted left so that
            # breadth's flag stays inside the box (a flag beside depth's mark would need a wider column)
            split = len(got) == 2
            xs = (j - 0.27, j + 0.13) if split else (j,)
            size = S.FONT + 1 if split else S.FONT + 5
            if split:
                top, bot = ys[claim] - half[claim] + 0.1, ys[claim] + half[claim] - 0.1
                box = plt.Rectangle((j - 0.47, top), 0.94, bot - top, fc="white", ec="#c8c8c8", lw=0.8, zorder=1)
                ax.add_patch(box)
                ax.plot([j - 0.07, j - 0.07], [top, bot], color="#c8c8c8", lw=0.8, zorder=1)
            for x, r in zip(xs, got, strict=True):
                sym, col = F.CELL_SYMBOL[r["cell"]]
                ax.text(x, ys[claim], sym, ha="center", va="center", fontsize=size, color=col, weight="bold")
                if r["flag"]:  # just clear of the mark (its half width plus overlaps()' two 2-px pads)
                    ax.annotate(r["flag"], (x, ys[claim]), xytext=(size * 0.42 + 3, 3), textcoords="offset points",
                                ha="left", va="center", fontsize=S.FONT, color=S.COL["muted"])  # fmt: skip
    for k, claim in enumerate(claims):
        if k % 2 == 0:
            ax.axhspan(ys[claim] - half[claim], ys[claim] + half[claim], color="#f6f6f6", lw=0, zorder=0)
    ax.axvline(3.5, color="#d0d0d0", lw=1.0, zorder=0)
    tr = F.blend(fig, ax)
    for name, gy in heads:
        ax.text(0.01, gy - 0.1, name, transform=tr, fontsize=S.FONT + 1, weight="bold", va="center")
    ax.set_xlim(-0.5, len(MODELS) - 0.5)
    ax.set_ylim(y + 0.5, 0.5)
    ax.set_yticks([ys[c] for c in claims], [label(c, wrap) for c in claims])
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0)
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)
    return fig


def save(fig) -> None:
    """As story_style.save, into figures/shared."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / "grid.svg", facecolor="white")
    fig.savefig(FIG_DIR / "grid.png", dpi=200, facecolor="white")


def main() -> None:
    rows = build()
    write(rows)
    plt = S.setup()
    fig = draw(plt, rows)
    save(fig)
    plt.close(fig)
    split = sum(1 for c in SHARED for _, name, _ in MODELS if name)
    print(f"{GRID.relative_to(REPO)}: {len(rows)} rows, {len(dict.fromkeys(r['claim'] for r in rows))} claims x "
          f"{len(MODELS)} models ({split} split cells); {FIG_DIR.relative_to(REPO)}/grid.png")  # fmt: skip


if __name__ == "__main__":
    main()
