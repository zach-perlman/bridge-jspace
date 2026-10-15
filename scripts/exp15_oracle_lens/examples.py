"""Worked examples for exp15: per question, what the J-lens and J++ rank first and what the oracle lens says, at each
read position and layer, before and after the J++ bridge swap. No GPU: rendered from a run's readings.

    uv run python -m scripts.exp15_oracle_lens.examples results/exp15_oracle_lens/<run> [<run> ...]
writes examples/exp15_oracle_lens/ (index.html, source.json) and refreshes examples/index.html.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from bridge_jspace.examples import (
    _CSS,
    _esc,
    _examples_root,
    _repo_rel,
    export_index,
    oracle_words_html,
)
from bridge_jspace.pins import REPO_ROOT

from .experiment import load_runs

POSITION = {"last": "last word", "prev": "-1", "cue_last": "cue phrase, last token"}
FIELD_ROLE = {"intermediate": "bridge", "answer": "answer", "swap_to": "distractor", "swap_answer": "swap_answer"}
GROUPS = [  # key, short title (filter buttons), definition (under the group's heading)
    ("blind-named", "Lenses miss · oracle sees",
     "The lenses miss the bridge in some rows (highlighted: neither the J-lens nor J++ ranks it 1st among the 97 "
     "entities), and in at least one of those rows the oracle names it. The other rows are shown for comparison and "
     "do not decide the group."),
    ("blind-missed", "Lenses miss · oracle misses",
     "The lenses miss the bridge in some rows (highlighted), and the oracle names it in none of them (it may in the "
     "other rows, where the lenses see it too)."),
    ("seen", "Lenses always see",
     "In every row at least one lens ranks the bridge 1st, so no row tests the oracle where the lenses miss it."),
    ("flipped", "Swap changes the answer",
     "exp14's J++ bridge swap on the cue phrase (layers 24-40) changes the model's answer to the swap target's "
     "(Brazil -> Mexico gives Spanish). Compare the oracle's words before and after the swap (last two columns): "
     "after it, the oracle should name the swap target."),
]  # fmt: skip


def group_of(rows: list[dict]) -> str:
    """The question's main group from its clean readings."""
    blind = [r for r in rows if r["lens_class"] == "neither"]
    if any(r["named_bridge"] for r in blind):
        return "blind-named"
    return "blind-missed" if blind else "seen"


def highlight(text: str, item: dict[str, Any], numeric_answer: bool) -> str:
    """The oracle's text with the question's words marked (numeric answers are not: list numbering)."""
    words = {role: item[field] for field, role in FIELD_ROLE.items()}
    return oracle_words_html(text, words, mark_answers=not numeric_answer)


def _rank(rank: int | None) -> str:
    if rank is None:
        return "<td class='l'>-</td>"
    return "<td class='l'><span class='hit'>1</span></td>" if rank == 1 else f"<td class='l'>{rank}</td>"


def model_said(exp14_run: Path) -> dict[str, dict[str, Any]]:
    """The model's own greedy answer per question (the first line of its continuation), before and after exp14's J++
    bridge swap on the cue phrase (layers 24-40), and whether the swap changed it to the swap target's answer."""
    out: dict[str, dict[str, Any]] = {}
    for line in (exp14_run / "items.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r.get("clean_continuation") is not None:
            out.setdefault(r["name"], {})["clean"] = r["clean_continuation"].strip().split("\n")[0]
    for line in (exp14_run / "outcomes.jsonl").read_text().splitlines():
        o = json.loads(line)
        if (o["lens"], o["positions"], o["band"], o["kind"], o["null"]) == ("jpp", "cue", "24-40", "bridge", False):
            out.setdefault(o["name"], {}).update(
                swapped=o["continuation"].strip().split("\n")[0], flip=o["flip"], kept=o["kept_clean"]
            )
    return out


def _said_html(item: dict[str, Any], said: dict[str, Any] | None, numeric: bool) -> str:
    said = said or {}
    if "clean" not in said:
        return ""
    verdict = (
        "changed to the swap target's answer"
        if said.get("flip")
        else "unchanged"
        if said.get("kept")
        else "changed, but to neither answer"
    )
    swap = (
        f" · <b>With the bridge swapped</b> ({_esc(item['intermediate'])} → {_esc(item['swap_to'])}, on the cue "
        f"phrase): {highlight(said['swapped'], item, numeric)} <i>({verdict})</i>"
        if "swapped" in said
        else ""
    )
    return f"<p class='meta'><b>Model's answer:</b> {highlight(said['clean'], item, numeric)}{swap}</p>"


def card(
    item: dict[str, Any],
    rows: list[dict],
    swapped: dict[tuple, dict],
    flip: bool | None,
    numeric: bool,
    said: dict[str, Any] | None = None,
) -> str:
    badges = f"<span class='badge'>{_esc(item['category'])}</span>"
    if flip is not None:
        badges += f"<span class='badge'>bridge swap {'flips' if flip else 'keeps'} the answer</span>"
    head = (
        f"<h3 id='{_esc(item['name'])}'>{_esc(item['name'])}{badges}</h3>"
        f"<div class='prompt'>{_esc(item['prompt'].rstrip())}</div>"
        f"<p class='meta'>bridge <span class='w bridge'>{_esc(item['intermediate'])}</span> (distractor "
        f"<span class='w ctrl'>{_esc(item['swap_to'])}</span>) · answer <span class='w answer'>{_esc(item['answer'])}"
        f"</span> (distractor <span class='w ctrl'>{_esc(item['swap_answer'])}</span>)</p>"
        + _said_html(item, said, numeric)
    )
    body = []
    for r in sorted(rows, key=lambda r: (list(POSITION).index(r["position"]), r["layer"])):
        after = swapped.get((r["position"], r["layer"]))
        blind = r["lens_class"] == "neither"
        seen = r["lens_class"]
        named = "<span class='hit'>yes</span>" if r["named_bridge"] else "no"
        body.append(
            f"<tr data-layer='{r['layer']}'{' class=blind' if blind else ''}><td class='l'>{POSITION[r['position']]}</td>"
            f"<td class='l'>{r['layer']}</td>{_rank(r['jlens_rank'])}{_rank(r['jpp_rank'])}"
            f"<td class='l'>{seen}</td><td class='l'>{named}</td>{_rank(r['answer_jlens_rank'])}"
            f"{_rank(r['answer_jpp_rank'])}<td class='o'>{highlight(r['text'], item, numeric)}</td>"
            f"<td class='o'>{highlight(after['text'], item, numeric) if after else ''}</td></tr>"
        )
    table = (
        "<div class='scroll'><table><tr><th>position</th><th>layer</th><th>bridge rank<br>J-lens</th>"
        "<th>bridge rank<br>J++</th><th>lenses with<br>the bridge 1st</th><th>oracle names<br>the bridge?</th>"
        "<th>answer rank<br>J-lens</th><th>answer rank<br>J++</th><th>oracle lens</th>"
        "<th>oracle lens, after the bridge swap</th></tr>" + "".join(body) + "</table></div>"
    )
    return f"<section class='card'>{head}{table}</section>"


LAYER_JS = """
const groupChips=[...document.querySelectorAll('.chips.groups button')];
groupChips.forEach(b=>b.onclick=()=>{groupChips.forEach(x=>x.classList.toggle('on',x===b));
const g=b.dataset.g;document.querySelectorAll('section.group').forEach(s=>s.hidden=g!=='all'&&s.dataset.g!==g);});
const layerChips=[...document.querySelectorAll('.chips.layers button')];
layerChips.forEach(b=>b.onclick=()=>{layerChips.forEach(x=>x.classList.toggle('on',x===b));
const l=b.dataset.l;document.querySelectorAll('tr[data-layer]').forEach(r=>r.hidden=l!=='all'&&r.dataset.layer!==l);});
"""


def render(run_dirs: Sequence[str | Path]) -> str:
    reads, item_rows, params, items = load_runs(run_dirs)
    clean = {}
    swapped: dict[str, dict[tuple, dict]] = {}
    for r in reads:
        if r["condition"] == "clean":
            clean.setdefault(r["name"], []).append(r)
        elif r["condition"] == "swapped":
            swapped.setdefault(r["name"], {})[(r["position"], r["layer"])] = r
    flips = {r["name"]: r["exp14_flip"] for r in item_rows}
    said = model_said(REPO_ROOT / params["exp14_run"])
    numeric = {n for n, it in items.items() if any(ch.isdigit() for ch in it["answer"] + it["swap_answer"])}
    members = {g: [n for n in clean if group_of(clean[n]) == g] for g, _, _ in GROUPS[:3]}
    members["flipped"] = [n for n in clean if flips.get(n)]

    chips = "<button class='on' data-g='all'>All</button>" + "".join(
        f"<button data-g='{g}'>{_esc(title)} ({len(members[g])})</button>" for g, title, _ in GROUPS
    )
    layer_chips = "<button class='on' data-l='all'>all layers</button>" + "".join(
        f"<button data-l='{layer}'>{layer}</button>" for layer in params["read_layers"]
    )
    nav, sections = [], []
    for g, title, definition in GROUPS:
        names = sorted(members[g])
        nav.append(f"<h4>{_esc(title)}</h4>" + "".join(f"<a href='#{_esc(n)}'>{_esc(n)}</a>" for n in names))
        cards = "".join(
            card(items[n], clean[n], swapped.get(n, {}), flips.get(n), n in numeric, said.get(n)) for n in names
        )
        sections.append(
            f"<section class='group' data-g='{g}'><h2>{_esc(title)} <span class='badge'>{len(names)}</span></h2>"
            f"<p class='def'>{_esc(definition)}</p>{cards}</section>"
        )
    runs = ", ".join(f"<code>{_esc(_repo_rel(Path(d)))}</code>" for d in run_dirs)
    lead = (
        "<ul>"
        f"<li><b>Cards:</b> the {len(clean)} two-hop questions Qwen3.6-27B answers correctly.</li>"
        "<li><b>Model's answer:</b> the first line of the model's own greedy continuation of the prompt (exp14), "
        "and the same with the bridge swapped to its distractor on the cue phrase (exp14's J++ swap); "
        '"unchanged" = still the right answer; "changed to the swap target\'s answer" = e.g. Spanish after Brazil -> '
        'Mexico; "changed, but to neither answer" = something else (e.g. 11 instead of 5 or 9).</li>'
        "<li><b>Rows:</b> where the oracle lens reads (the last word, -1, the cue phrase's last token) and at which "
        "layer. Filter the layers with the second row of buttons.</li>"
        "<li><b>Rank columns:</b> where the J-lens and J++ rank the bridge among the 97 entities, and the answer "
        "among the 112 answers, at that position and layer (exp12); <span class='hit'>1</span> = first. The two "
        "lists are separate, so the bridge and the answer can both be 1st in one row.</li>"
        "<li><b>Highlighted rows:</b> neither lens ranks the bridge 1st there; those rows put a question in its "
        "group.</li>"
        "<li><b>Oracle columns:</b> the oracle lens's bullets for the same activation (greedy, 64 tokens), before "
        "and after exp14's J++ bridge swap on the cue phrase. Marked: <span class='w bridge'>bridge</span>, "
        "<span class='w answer'>answer</span>, <span class='w ctrl'>their distractors</span> (numeric answers are not "
        "marked: list numbering).</li>"
        f"<li><b>Data:</b> runs {runs}; regenerate with "
        "<code>uv run python -m scripts.exp15_oracle_lens.examples &lt;run&gt; [&lt;run&gt; ...]</code>.</li></ul>"
    )
    css = (
        _CSS + "tr.blind td{background:var(--panel)}tr.blind td:first-child{box-shadow:inset 3px 0 0 var(--bridge)}"
        ".lead{max-width:none}.lead ul{margin:4px 0;padding-left:18px}.lead li{margin:2px 0}"
        ".chips .lbl{font:12px var(--sans);color:var(--faint);align-self:center;margin-right:2px}"
    )
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1,viewport-fit=cover'>"
        "<title>Oracle Lens Examples</title>"
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600'
        '&family=IBM+Plex+Sans:wght@400;600&display=swap">'
        f"<style>{css}</style></head><body><header><h1>Oracle lens vs J-lens / J++ (exp15)</h1>"
        f"<div class='lead'>{lead}</div></header><div class='layout'><nav>{''.join(nav)}</nav>"
        f"<main><div class='chips groups'><span class='lbl'>questions:</span>{chips}</div>"
        f"<div class='chips layers'><span class='lbl'>layers:</span>{layer_chips}</div>"
        f"{''.join(sections)}</main></div><script>{LAYER_JS}</script></body></html>"
    )


def export(run_dirs: Sequence[str | Path], root: Path | None = None) -> Path:
    """examples/exp15_oracle_lens/index.html and its index entry (source.json), then examples/index.html."""
    root = root or _examples_root()
    out = root / "exp15_oracle_lens"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(render(run_dirs))
    reads, item_rows, _, _ = load_runs(run_dirs)
    clean = {}
    for r in reads:
        if r["condition"] == "clean":
            clean.setdefault(r["name"], []).append(r)
    groups = [{"title": title, "n_total": sum(group_of(rows) == g for rows in clean.values())}
              for g, title, _ in GROUPS[:3]]  # fmt: skip
    groups.append({"title": GROUPS[3][1], "n_total": sum(bool(r["exp14_flip"]) for r in item_rows)})
    entry = {"title": "Oracle lens vs J-lens / J++ (exp15)", "n_examples": len(clean), "model": "Qwen/Qwen3.6-27B",
             "groups": groups}  # fmt: skip
    source = {"examples_runs": [_repo_rel(Path(d)) for d in run_dirs], "entry": entry}
    (out / "source.json").write_text(json.dumps(source, indent=2))
    export_index(root)
    return out


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    print(export(sys.argv[1:]))
