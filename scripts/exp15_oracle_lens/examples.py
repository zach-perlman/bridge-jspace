"""Worked examples for exp15: per question, what the J-lens and J++ rank first and what the oracle lens says, at each
read position and layer, before and after the J++ bridge swap. No GPU: rendered from a run's readings.

    uv run python -m scripts.exp15_oracle_lens.examples results/exp15_oracle_lens/<run>
writes examples/exp15_oracle_lens/ (index.html, source.json) and refreshes examples/index.html.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from bridge_jspace.examples import _CSS, _JS, _esc, _examples_root, _repo_rel, export_index

from .experiment import load_scored

POSITION = {"last": "last word", "prev": "-1", "cue_last": "cue phrase, last token"}
WORD_CLASS = {"intermediate": "bridge", "answer": "answer", "swap_to": "ctrl", "swap_answer": "ctrl"}
GROUPS = [
    ("blind-named", "Neither lens has the bridge first, the oracle names it",
     "Questions with at least one reading where neither the J-lens nor J++ ranks the bridge first among the 97 "
     "entities and the oracle's bullets name it."),
    ("blind-missed", "Neither lens has the bridge first, the oracle does not name it either",
     "Questions with readings where neither lens has the bridge first, none of which the oracle names it in."),
    ("seen", "The lenses have the bridge first wherever we read",
     "Every reading has the bridge first in at least one lens."),
    ("flipped", "The bridge swap flips the answer: does the oracle follow?",
     "exp14's J++ bridge swap on the cue phrase (layers 24-40) changes the model's answer to the swap target's. "
     "Compare the oracle's readings before and after the swap (right-hand column)."),
]  # fmt: skip


def group_of(rows: list[dict]) -> str:
    """The question's main group from its clean readings."""
    blind = [r for r in rows if r["lens_class"] == "neither"]
    if any(r["named_bridge"] for r in blind):
        return "blind-named"
    return "blind-missed" if blind else "seen"


def highlight(text: str, item: dict[str, Any], numeric_answer: bool) -> str:
    """The oracle's text, escaped, with the question's words marked (numeric answers are not: list numbering)."""
    out = _esc(text)
    for field, cls in WORD_CLASS.items():
        if numeric_answer and field in ("answer", "swap_answer"):
            continue
        pattern = rf"(?<![^\W_])({re.escape(_esc(item[field]))}(?:e?s)?)(?![^\W_])"
        out = re.sub(pattern, rf"<span class='w {cls}'>\1</span>", out, flags=re.IGNORECASE)
    return out.replace("\n", "<br>")


def _rank(rank: int | None) -> str:
    if rank is None:
        return "<td class='l'>-</td>"
    return "<td class='l'><span class='hit'>1</span></td>" if rank == 1 else f"<td class='l'>{rank}</td>"


def card(item: dict[str, Any], rows: list[dict], swapped: dict[tuple, dict], flip: bool | None, numeric: bool) -> str:
    badges = f"<span class='badge'>{_esc(item['category'])}</span>"
    if flip is not None:
        badges += f"<span class='badge'>bridge swap {'flips' if flip else 'keeps'} the answer</span>"
    head = (
        f"<h3 id='{_esc(item['name'])}'>{_esc(item['name'])}{badges}</h3>"
        f"<div class='prompt'>{_esc(item['prompt'].rstrip())}</div>"
        f"<p class='meta'>bridge <span class='w bridge'>{_esc(item['intermediate'])}</span> (distractor "
        f"<span class='w ctrl'>{_esc(item['swap_to'])}</span>) · answer <span class='w answer'>{_esc(item['answer'])}"
        f"</span> (distractor <span class='w ctrl'>{_esc(item['swap_answer'])}</span>)</p>"
    )
    body = []
    for r in sorted(rows, key=lambda r: (list(POSITION).index(r["position"]), r["layer"])):
        after = swapped.get((r["position"], r["layer"]))
        body.append(
            f"<tr><td class='l'>{POSITION[r['position']]}</td><td class='l'>{r['layer']}</td>"
            f"{_rank(r['jlens_rank'])}{_rank(r['jpp_rank'])}{_rank(r['answer_jlens_rank'])}"
            f"{_rank(r['answer_jpp_rank'])}<td class='o'>{highlight(r['text'], item, numeric)}</td>"
            f"<td class='o'>{highlight(after['text'], item, numeric) if after else ''}</td></tr>"
        )
    table = (
        "<div class='scroll'><table><tr><th>position</th><th>layer</th><th>bridge rank<br>J-lens</th>"
        "<th>bridge rank<br>J++</th><th>answer rank<br>J-lens</th><th>answer rank<br>J++</th>"
        "<th>oracle lens</th><th>oracle lens, after the bridge swap</th></tr>" + "".join(body) + "</table></div>"
    )
    return f"<section class='card'>{head}{table}</section>"


def render(run_dir: str | Path) -> str:
    reads, item_rows, _, items = load_scored(run_dir)
    clean = {}
    swapped: dict[str, dict[tuple, dict]] = {}
    for r in reads:
        if r["condition"] == "clean":
            clean.setdefault(r["name"], []).append(r)
        elif r["condition"] == "swapped":
            swapped.setdefault(r["name"], {})[(r["position"], r["layer"])] = r
    flips = {r["name"]: r["exp14_flip"] for r in item_rows}
    numeric = {n for n, it in items.items() if any(ch.isdigit() for ch in it["answer"] + it["swap_answer"])}
    members = {g: [n for n in clean if group_of(clean[n]) == g] for g, _, _ in GROUPS[:3]}
    members["flipped"] = [n for n in clean if flips.get(n)]

    chips = "<button class='on' data-g='all'>All</button>" + "".join(
        f"<button data-g='{g}'>{_esc(title)} ({len(members[g])})</button>" for g, title, _ in GROUPS
    )
    nav, sections = [], []
    for g, title, definition in GROUPS:
        names = sorted(members[g])
        nav.append(f"<h4>{_esc(title)}</h4>" + "".join(f"<a href='#{_esc(n)}'>{_esc(n)}</a>" for n in names))
        cards = "".join(card(items[n], clean[n], swapped.get(n, {}), flips.get(n), n in numeric) for n in names)
        sections.append(
            f"<section class='group' data-g='{g}'><h2>{_esc(title)} <span class='badge'>{len(names)}</span></h2>"
            f"<p class='def'>{_esc(definition)}</p>{cards}</section>"
        )
    lead = (
        "<p>Each card is one of the 77 two-hop questions Qwen3.6-27B answers correctly. Rows: where the oracle lens "
        "reads (the last word, -1, the cue phrase's last token) and at which layer. Rank columns: where the J-lens "
        "and J++ rank the bridge among the 97 entities, and the answer among the 112 answers, at that position and "
        "layer (exp12); <span class='hit'>1</span> = first. Oracle columns: the oracle lens's bullets for the same "
        "activation (greedy, 64 tokens), before and after exp14's J++ bridge swap on the cue phrase. Marked words: "
        "<span class='w bridge'>bridge</span>, <span class='w answer'>answer</span>, "
        "<span class='w ctrl'>their distractors</span> (numeric answers are not marked: list numbering).</p>"
        f"<p>Run <code>{_esc(_repo_rel(Path(run_dir)))}</code>; regenerate with "
        "<code>uv run python -m scripts.exp15_oracle_lens.examples &lt;run&gt;</code>.</p>"
    )
    css = _CSS + "td.o{white-space:normal;min-width:260px;max-width:420px;font:12px/1.45 var(--mono)}"
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1,viewport-fit=cover'>"
        "<title>Oracle Lens Examples</title>"
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600'
        '&family=IBM+Plex+Sans:wght@400;600&display=swap">'
        f"<style>{css}</style></head><body><header><h1>Oracle lens vs J-lens / J++ (exp15)</h1>"
        f"<div class='lead'>{lead}</div></header><div class='layout'><nav>{''.join(nav)}</nav>"
        f"<main><div class='chips'>{chips}</div>{''.join(sections)}</main></div><script>{_JS}</script></body></html>"
    )


def export(run_dir: str | Path, root: Path | None = None) -> Path:
    """examples/exp15_oracle_lens/index.html and its index entry (source.json), then examples/index.html."""
    root = root or _examples_root()
    out = root / "exp15_oracle_lens"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(render(run_dir))
    reads, item_rows, _, _ = load_scored(run_dir)
    clean = {}
    for r in reads:
        if r["condition"] == "clean":
            clean.setdefault(r["name"], []).append(r)
    groups = [{"title": title, "n_total": sum(group_of(rows) == g for rows in clean.values())}
              for g, title, _ in GROUPS[:3]]  # fmt: skip
    groups.append({"title": GROUPS[3][1], "n_total": sum(bool(r["exp14_flip"]) for r in item_rows)})
    entry = {"title": "Oracle lens vs J-lens / J++ (exp15)", "n_examples": len(clean), "model": "Qwen/Qwen3.6-27B",
             "groups": groups}  # fmt: skip
    (out / "source.json").write_text(json.dumps({"examples_run": _repo_rel(Path(run_dir)), "entry": entry}, indent=2))
    export_index(root)
    return out


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(export(sys.argv[1]))
