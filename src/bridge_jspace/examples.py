"""Worked examples: lens readout tables for selected items, written to examples.md for reading by hand.

Each experiment has a selector (`scripts/<exp>/examples.py: select(source_run, params)`) that picks items from one of
its runs by outcome group (seen / missed / model wrong / ...), at random with a fixed seed, and an `examples.yaml`
that runs `LensExamples` against that source run. The tables need the top tokens per layer, which the runs do not
store, so this re-runs the model on the selected items only.

Per example: the last-token table (layers x readers: top-5 words, ranks of the bridge and the answer) and, for the
J-lens, a position x layer table of the last tokens (top word, bridge rank).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import torch

from bridge_jspace.experiment import Experiment
from bridge_jspace.readout import Reader, formatting_mask, readout_logits, residuals, word_ranks
from bridge_jspace.utils import progress

MARK = {"bridge": "**{}**", "answer": "*{}*", "distractor": "[{}]", "swap_answer": "[{}]"}
READER_TITLE = {"logit": "logit lens", "jlens": "J-lens", "jpp": "J++"}


@dataclass
class Example:
    name: str
    group: str  # selection group key
    prompt: str  # exactly as the source run fed it
    words: dict[str, str]  # role -> word: bridge, answer and, if any, distractor / swap_answer
    word_ids: dict[str, list[int]]  # role -> token ids used for its word rank
    why: str  # the numbers that put it in its group
    info: dict[str, Any] = field(default_factory=dict)  # status, label, model's top word, ...


@dataclass
class Group:
    key: str
    title: str
    definition: str
    n_total: int  # items in the group before sampling


class LensExamples(Experiment):
    def run(self) -> dict[str, Any]:
        from bridge_jspace.run import import_object

        p = self.params
        lm, tok = self.model.lm, self.model.tokenizer
        readers: dict[str, Reader] = {"logit": None, **self.lenses}
        layers = {n: list(range(lm.n_layers - 1)) if r is None else r.source_layers for n, r in readers.items()}
        sanity = self.sanity_gate()
        groups, examples = import_object(p["selector"])(Path(p["source_run"]), p, tok)
        unembed = getattr(lm, "_lm_head")  # noqa: B009 - vocab size of the head
        mask = formatting_mask(tok, unembed.weight.shape[0]).to(self.model.device)
        show = sorted({*range(0, lm.n_layers - 1, p["layer_step"]), lm.n_layers - 2})
        pos_layers = p["position_layers"]

        records = []
        for ex in progress(examples, "examples"):
            ids = lm.encode(ex.prompt)
            tokens = [tok.decode([t]) for t in ids[0].tolist()]
            final = lm.n_layers - 1
            resid = residuals(lm, ids, sorted(set(show) | set(pos_layers) | {final}))
            out = lm.unembed(resid[final][[-1]]).float().masked_fill(mask, float("-inf"))
            rec: dict[str, Any] = {**asdict(ex), "tokens": tokens, "last_token": {}, "positions": {}}
            rec["info"]["model's top word"] = tok.decode([int(out.argmax())]).strip()
            for rname, reader in readers.items():
                rec["last_token"][rname] = {
                    str(layer): _cell(lm, reader, resid[layer][[-1]], layer, ex, mask, tok, p["top_k"])[0]
                    for layer in show
                    if layer in layers[rname]
                }
            n_pos = min(p["n_positions"], len(tokens))
            for rname in p["position_readers"]:
                reader = readers[rname]
                rec["positions"][rname] = {
                    str(layer): _cell(lm, reader, resid[layer][-n_pos:], layer, ex, mask, tok, 1)
                    for layer in pos_layers
                    if layer in layers[rname]
                }
            rec["slices"] = self._slice_pages(ex) if p.get("slice_pages") else {}
            records.append(rec)

        self.save_json("examples.json", {"groups": [asdict(g) for g in groups], "examples": records})
        out = export(self.run_dir)
        export_index()
        self.log.info(f"examples view refreshed: {out}/index.html (open with `make examples-serve`)")
        return {
            "sanity": sanity,
            "source_run": p["source_run"],
            "groups": {g.key: g.n_total for g in groups},
            "n_examples": len(records),
        }

    def _slice_pages(self, ex: Example) -> dict[str, str]:
        """jlens's own interactive layer x position page per lens reader, the example's words pinned. Written to
        slices/ (self-contained HTML with d3 inlined; large, so not committed: see .gitignore)."""
        from jlens.vis import build_page, compute_slice

        p, out = self.params, {}
        pinned = {i for ids in ex.word_ids.values() for i in ids}
        (self.run_dir / "slices").mkdir(exist_ok=True)
        for rname in p["slice_readers"]:
            lens = self.lenses.get(rname)
            if lens is None:
                continue
            sd = compute_slice(
                self.model.lm, lens, ex.prompt, top_n=p["slice_top_n"], max_tracked=p["slice_max_tracked"],
                pinned_token_ids=pinned, mask_display=True,
            )  # fmt: skip
            page, _, _ = build_page(
                sd, ex.prompt, title=f"{ex.name}: {_title(rname)}", description=ex.why, mode="embed"
            )
            rel = f"slices/{ex.name}__{rname}.html"
            (self.run_dir / rel).write_text(page)
            out[rname] = rel
        return out


@torch.no_grad()
def _cell(lm, reader: Reader, h, layer: int, ex: Example, mask, tok, k: int) -> list[dict[str, Any]]:
    """Per position: the top-k word tokens (formatting removed) and the word rank of each of the example's words."""
    logits = readout_logits(lm, reader, h, layer)  # [n, vocab]
    roles = [r for r, ids in ex.word_ids.items() if ids]
    ranks = word_ranks(logits, [ex.word_ids[r] for r in roles], mask)  # [n, roles]
    top = logits.masked_fill(mask.to(logits.device), float("-inf")).topk(k, dim=-1).indices.cpu()
    out = []
    for i in range(logits.shape[0]):
        out.append(
            {
                "top": [tok.decode([int(t)]) for t in top[i]],
                "top_ids": [int(t) for t in top[i]],
                "ranks": {r: int(ranks[i, j]) for j, r in enumerate(roles)},
            }
        )
    return out


# ---- rendering (pure; unit-tested) -------------------------------------------------------------


def _title(reader: str) -> str:
    return READER_TITLE.get(reader, reader)


def _show(token: str) -> str:
    t = token.strip() or "␣"
    return t.replace("|", "\\|").replace("`", "'")


def _marked(token_id: int, token: str, ex_ids: dict[str, list[int]]) -> str:
    for role, ids in ex_ids.items():
        if token_id in ids:
            return MARK[role].format(_show(token))
    return _show(token)


def render(groups: list[Group], records: list[dict[str, Any]], p: dict[str, Any], model: str) -> str:
    lines = [
        f"# Examples: {p['title']}",
        "",
        f"Source run `{p['source_run']}`, model {model}. Examples are drawn at random with seed {p['seed_examples']}, "
        f"up to {p['per_group']} per group; groups can overlap. Marks in the tables: **bridge**, *answer*, "
        "[distractor]. Ranks are word ranks (1 = top; spaces and punctuation removed) of the bridge (B) and the "
        "answer (A). Readers: logit lens (baseline), J-lens, J++.",
        "",
        "| Group | Definition | Items in group | Shown |",
        "|---|---|---|---|",
    ]
    by_group: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        by_group.setdefault(r["group"], []).append(r)
    for g in groups:
        lines.append(f"| [{g.title}](#{g.key}) | {g.definition} | {g.n_total} | {len(by_group.get(g.key, []))} |")
    for g in groups:
        lines += ["", f'<a id="{g.key}"></a>', f"## {g.title}", "", g.definition, ""]
        for r in by_group.get(g.key, []):
            lines += _render_example(r, p)
    return "\n".join(lines) + "\n"


def _render_example(r: dict[str, Any], p: dict[str, Any]) -> list[str]:
    w = r["words"]
    info = ", ".join(f"{k}: {v}" for k, v in r["info"].items())
    ctrl = f"; controls [{w['distractor']}] / [{w['swap_answer']}]" if "distractor" in w else ""
    out = [
        f"### `{r['name']}`",
        "",
        "> " + (r["prompt"][:-1] + "␣" if r["prompt"].endswith(" ") else r["prompt"]),
        "",
        f"Bridge **{w['bridge']}** -> answer *{w['answer']}*{ctrl}. {info}.",
        f"Why this group: {r['why']}",
        *(
            [
                "Interactive layer x position view (jlens, pinned words; open locally): "
                + " · ".join(f"[{_title(k)}]({v})" for k, v in r.get("slices", {}).items())
            ]
            if r.get("slices")
            else []
        ),
        "",
        f"**Last token** `{_show(r['tokens'][-1])}`: top-{p['top_k']} words per layer",
        "",
        "| layer | "
        + " | ".join(_title(x) for x in r["last_token"])
        + " | B / A rank: "
        + " · ".join(_title(x) for x in r["last_token"])
        + " |",
        "|---|" + "---|" * (len(r["last_token"]) + 1),
    ]
    layers = sorted({int(layer) for rd in r["last_token"].values() for layer in rd})
    for layer in layers:
        cells, ranks = [], []
        for rd in r["last_token"].values():
            c = rd.get(str(layer))
            if c is None:
                cells.append("")
                ranks.append("-")
                continue
            cells.append(", ".join(_marked(i, t, r["word_ids"]) for i, t in zip(c["top_ids"], c["top"], strict=True)))
            ranks.append(f"{c['ranks'].get('bridge', '-')} / {c['ranks'].get('answer', '-')}")
        out.append(f"| {layer} | " + " | ".join(cells) + " | " + " · ".join(ranks) + " |")
    for rname, by_layer in r["positions"].items():
        n = len(next(iter(by_layer.values())))
        toks = r["tokens"][-n:]
        out += [
            "",
            f"**{_title(rname)}, last {n} tokens x layers**: top word (bridge rank)",
            "",
            "| token | " + " | ".join(f"L{layer}" for layer in by_layer) + " |",
            "|---|" + "---|" * len(by_layer),
        ]
        for i, t in enumerate(toks):
            row = []
            for c in by_layer.values():
                cell = c[i]
                row.append(
                    f"{_marked(cell['top_ids'][0], cell['top'][0], r['word_ids'])} ({cell['ranks'].get('bridge', '-')})"
                )
            out.append(f"| `{_show(t)}` | " + " | ".join(row) + " |")
    out.append("")
    return out


# ---- shared selection helpers ------------------------------------------------------------------


def sample(names: list[str], k: int, seed: int) -> list[str]:
    """Up to k names at random with a fixed seed (order of `names` must be deterministic)."""
    rng = np.random.default_rng(seed)
    return [names[i] for i in sorted(rng.choice(len(names), size=min(k, len(names)), replace=False))] if names else []


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


# ---- HTML view (pure; unit-tested) ----------------------------------------------------------------

_CSS = """
/* Layout: a side index of groups and examples next to a reading column of example cards; stacks on phones. */
:root{--bg:#fbfbf9;--panel:#f3f3ef;--ink:#16171a;--muted:#4f5157;--faint:#7c7e85;--line:#e2e2dc;
--bridge:#1f63b8;--bridge-bg:rgba(42,120,214,.14);--answer:#b4410f;--answer-bg:rgba(235,104,52,.16);
--ctrl-bg:rgba(124,126,133,.16);--heat:42,120,214;--chip-on-bg:#16171a;--chip-on-fg:#fbfbf9;
--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
--mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17181b;--panel:#1f2024;--ink:#ecebe6;
--muted:#c2c1b9;--faint:#8d8f96;--line:#2e2f34;--bridge:#6aa6ef;--bridge-bg:rgba(85,152,231,.2);--answer:#f39a6e;
--answer-bg:rgba(240,138,93,.2);--ctrl-bg:rgba(141,143,150,.2);--heat:85,152,231;--chip-on-bg:#ecebe6;
--chip-on-fg:#17181b;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#17181b;--panel:#1f2024;--ink:#ecebe6;--muted:#c2c1b9;--faint:#8d8f96;
--line:#2e2f34;--bridge:#6aa6ef;--bridge-bg:rgba(85,152,231,.2);--answer:#f39a6e;--answer-bg:rgba(240,138,93,.2);
--ctrl-bg:rgba(141,143,150,.2);--heat:85,152,231;--chip-on-bg:#ecebe6;--chip-on-fg:#17181b;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 var(--sans)}
code{font-family:var(--mono)}
header{padding-block:18px 14px;padding-inline:20px;border-bottom:1px solid var(--line)}
h1{font-size:20px;margin:0 0 8px;text-wrap:balance}
.lead{color:var(--muted);max-width:78ch;margin:0}.lead p{margin:0 0 6px}
.layout{display:flex}
nav{position:sticky;top:env(safe-area-inset-top,0px);align-self:flex-start;width:270px;flex:none;
max-height:100vh;overflow:auto;padding-block:12px;padding-inline:16px;border-right:1px solid var(--line);background:var(--panel)}
nav h4{margin:12px 0 4px;font-size:13px}
nav a{display:block;color:var(--muted);text-decoration:none;font:12px var(--mono);padding:1px 0;overflow-wrap:anywhere}
nav a:hover,nav a:focus-visible{color:var(--ink);text-decoration:underline}
main{flex:1;min-width:0;padding-block:12px 40px;padding-inline:20px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 12px}
.chips button{border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:14px;padding:3px 10px;
cursor:pointer;font:12px var(--sans)}
.chips button.on{background:var(--chip-on-bg);color:var(--chip-on-fg);border-color:var(--chip-on-bg)}
.chips button:focus-visible{outline:2px solid var(--bridge);outline-offset:2px}
section.group>h2{font-size:16px;margin:24px 0 2px;text-wrap:balance}.def{color:var(--muted);margin:0 0 10px;max-width:78ch}
.card{border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin:12px 0;background:var(--bg);min-width:0}
.card h3{font:600 14px var(--mono);margin:0 0 6px;overflow-wrap:anywhere}
.badge{display:inline-block;font:11px var(--sans);padding:1px 7px;border-radius:9px;background:var(--ctrl-bg);
color:var(--muted);margin:2px 0 2px 6px}
.prompt{font:13px var(--mono);background:var(--panel);padding:6px 8px;border-radius:4px;margin:6px 0;overflow-wrap:anywhere}
.meta{color:var(--muted);margin:2px 0;max-width:90ch}.meta a{color:var(--bridge)}
.b{color:var(--bridge);font-weight:600}.a{color:var(--answer);font-weight:600}
.scroll{overflow-x:auto;max-width:100%}
table{border-collapse:collapse;margin:8px 0;font-size:12px}
th,td{border-bottom:1px solid var(--line);padding:3px 6px;text-align:left;vertical-align:top;white-space:nowrap}
th{color:var(--faint);font-weight:500}td.l{color:var(--faint);font-variant-numeric:tabular-nums}
.w{display:inline-block;padding:0 4px;margin:1px 2px 1px 0;border-radius:3px;font-family:var(--mono)}
.w.bridge{background:var(--bridge-bg);color:var(--bridge);font-weight:600}
.w.answer{background:var(--answer-bg);color:var(--answer);font-weight:600}.w.ctrl{background:var(--ctrl-bg)}
.r{display:block;color:var(--faint);font-size:11px;font-variant-numeric:tabular-nums}.r .hit{color:var(--ink);font-weight:600}
td.heat{font-family:var(--mono);text-align:center;min-width:70px}
td.heat small{color:var(--ink);opacity:.75;font-variant-numeric:tabular-nums}
td.heat .w.bridge{background:none;color:var(--ink);text-decoration:underline 2px}
h4.t{margin:12px 0 0;font-size:13px}
@media (max-width:760px){.layout{flex-direction:column}nav{position:static;width:auto;max-height:none;
border-right:0;border-bottom:1px solid var(--line)}header,main{padding-inline:16px}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
"""

_JS = """
const chips=[...document.querySelectorAll('.chips button')];
chips.forEach(b=>b.onclick=()=>{chips.forEach(x=>x.classList.toggle('on',x===b));
const g=b.dataset.g;document.querySelectorAll('section.group').forEach(s=>s.hidden=g!=='all'&&s.dataset.g!==g);});
"""


def _esc(s: str) -> str:
    import html

    return html.escape(s, quote=True)


def _word_html(token_id: int, token: str, word_ids: dict[str, list[int]]) -> str:
    cls = ""
    for role, ids in word_ids.items():
        if token_id in ids:
            cls = {"bridge": "bridge", "answer": "answer"}.get(role, "ctrl")
            break
    return f'<span class="w {cls}">{_esc(_show(token))}</span>'


def _rank_html(rank: Any, label: str) -> str:
    if rank in (None, "-"):
        return f"{label} -"
    return f'{label} <span class="hit">{rank}</span>' if int(rank) <= 10 else f"{label} {rank}"


def _heat(rank: Any) -> str:
    """Background for a bridge rank: rank 1 full colour, >= 1000 none (log scale)."""
    if rank in (None, "-"):
        return ""
    alpha = max(0.0, 1 - np.log10(max(int(rank), 1)) / 3) * 0.75
    return f' style="background:rgba(var(--heat),{alpha:.2f})"'


def render_html(
    groups: list[Group],
    records: list[dict[str, Any]],
    p: dict[str, Any],
    model: str,
    standalone: bool = True,
    slice_prefix: str = "",
) -> str:
    by_group: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        by_group.setdefault(r["group"], []).append(r)
    nav, chips, body = [], ['<button class="on" data-g="all">all</button>'], []
    for g in groups:
        recs = by_group.get(g.key, [])
        chips.append(f'<button data-g="{g.key}">{_esc(g.title)} ({g.n_total})</button>')
        nav.append(f"<h4>{_esc(g.title)} <span class='badge'>{g.n_total}</span></h4>")
        nav += [f'<a href="#{g.key}-{_esc(r["name"])}">{_esc(r["name"])}</a>' for r in recs]
        body.append(f'<section class="group" data-g="{g.key}"><h2>{_esc(g.title)}</h2>')
        body.append(f'<p class="def">{_esc(g.definition)} {g.n_total} items; {len(recs)} shown.</p>')
        body += [_card_html(r, g.key, p, slice_prefix) for r in recs]
        body.append("</section>")
    title = p.get("page_title") or f"Examples: {p['title']}"
    lead = (
        f"<p><b>How to read this page.</b> Each card is one two-hop question and what three readers (logit lens, "
        f"J-lens, J++) show inside the model at each layer. Model: {_esc(model)}. Questions are sorted into groups by "
        f"what the J-lens showed in run <code>{_esc(p['source_run'])}</code>; within a group the cards are a random "
        f"pick (seed {p['seed_examples']}, at most {p['per_group']}), not the best or worst cases, and one question "
        "can sit in two groups."
        + (f" Tables from run <code>{_esc(p['examples_run'])}</code>." if p.get("examples_run") else "")
        + "</p>"
        '<p>Colours: <span class="w bridge">bridge</span> <span class="w answer">answer</span> '
        '<span class="w ctrl">distractor</span>. Under each cell, <b>B 3 · A 120</b> means: at that layer the bridge '
        "is the reader's 3rd most likely word and the answer its 120th (spaces and punctuation not counted); bold "
        "marks the top 10. The colour of the J-lens position table shows the bridge rank: darker is higher.</p>"
    )
    head = (
        f"<title>{_esc(title)}</title>"
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600'
        '&family=IBM+Plex+Sans:wght@400;600&display=swap">'
        f"<style>{_CSS}</style>"
    )
    page = (
        f"<header><h1>{_esc(title)}</h1><div class='lead'>{lead}</div></header><div class='layout'>"
        f"<nav aria-label='Examples'>{''.join(nav)}</nav><main><div class='chips' role='toolbar'>{''.join(chips)}</div>"
        f"{''.join(body)}</main></div><script>{_JS}</script>"
    )
    if not standalone:  # Artifact pages: the host adds doctype/head/body; title and style go first
        return head + page
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1,viewport-fit=cover'>"
        f"{head}</head><body>{page}</body></html>"
    )


def _card_html(r: dict[str, Any], group: str, p: dict[str, Any], slice_prefix: str = "") -> str:
    w = r["words"]
    prompt = r["prompt"][:-1] + "␣" if r["prompt"].endswith(" ") else r["prompt"]
    ctrl = f" · controls {_esc(w['distractor'])} / {_esc(w['swap_answer'])}" if "distractor" in w else ""
    badges = "".join(f"<span class='badge'>{_esc(k)}: {_esc(str(v))}</span>" for k, v in r["info"].items())
    parts = [
        f'<div class="card" id="{group}-{_esc(r["name"])}"><h3>{_esc(r["name"])}{badges}</h3>',
        f'<div class="prompt">{_esc(prompt)}</div>',
        f'<p class="meta">bridge <span class="b">{_esc(w["bridge"])}</span> → answer '
        f'<span class="a">{_esc(w["answer"])}</span>{ctrl}</p>',
        f'<p class="meta">{_esc(r["why"])}</p>',
        (
            '<p class="meta">Interactive layer × position view (jlens; click a cell to pin a token): '
            + " · ".join(
                f'<a href="{_esc(slice_prefix + v)}" target="_blank">{_esc(_title(k))}</a>'
                for k, v in r["slices"].items()
            )
            + "</p>"
            if r.get("slices")
            else ""
        ),
        f'<h4 class="t">Last token <code>{_esc(_show(r["tokens"][-1]))}</code>: top-{p["top_k"]} words per layer</h4>',
        '<div class="scroll"><table><tr><th>layer</th>'
        + "".join(f"<th>{_esc(_title(x))}</th>" for x in r["last_token"])
        + "</tr>",
    ]
    layers = sorted({int(layer) for rd in r["last_token"].values() for layer in rd})
    for layer in layers:
        row = [f'<td class="l">{layer}</td>']
        for rd in r["last_token"].values():
            c = rd.get(str(layer))
            if c is None:
                row.append("<td></td>")
                continue
            words = "".join(_word_html(i, t, r["word_ids"]) for i, t in zip(c["top_ids"], c["top"], strict=True))
            rk = c["ranks"]
            row.append(
                f"<td>{words}<span class='r'>{_rank_html(rk.get('bridge'), 'B')} · {_rank_html(rk.get('answer'), 'A')}</span></td>"
            )
        parts.append("<tr>" + "".join(row) + "</tr>")
    parts.append("</table></div>")
    for rname, by_layer in r["positions"].items():
        n = len(next(iter(by_layer.values())))
        toks = r["tokens"][-n:]
        parts.append(
            f'<h4 class="t">{_esc(_title(rname))}: last {n} tokens × layers (top word; colour and number: bridge rank)</h4>'
            '<div class="scroll"><table><tr><th>token</th>'
            + "".join(f"<th>L{layer}</th>" for layer in by_layer)
            + "</tr>"
        )
        for i, t in enumerate(toks):
            cells = []
            for c in by_layer.values():
                cell = c[i]
                rank = cell["ranks"].get("bridge", "-")
                cells.append(
                    f"<td class='heat'{_heat(rank)}>{_word_html(cell['top_ids'][0], cell['top'][0], r['word_ids'])}"
                    f"<br><small>{rank}</small></td>"
                )
            parts.append(f"<tr><td><code>{_esc(_show(t))}</code></td>{''.join(cells)}</tr>")
        parts.append("</table></div>")
    parts.append("</div>")
    return "".join(parts)


EXAMPLES_DIR_NAME = "examples"


def _examples_root() -> Path:
    from bridge_jspace.pins import REPO_ROOT

    return REPO_ROOT / EXAMPLES_DIR_NAME


def _repo_rel(path: Path) -> str:
    """`path` relative to the repo root when inside it (so committed views work on any machine)."""
    from bridge_jspace.pins import REPO_ROOT

    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def _from_repo(path: str) -> Path:
    from bridge_jspace.pins import REPO_ROOT

    return Path(path) if Path(path).is_absolute() else REPO_ROOT / path


def _params_with_title(manifest: dict[str, Any]) -> dict[str, Any]:
    p = dict(manifest["config"]["params"])
    if "page_title" not in p:  # runs from before page titles: take the experiment's current one
        from bridge_jspace.config import load_config
        from bridge_jspace.pins import REPO_ROOT

        cfg = REPO_ROOT / "scripts" / manifest["config"]["name"] / "examples.yaml"
        if cfg.exists():
            p["page_title"] = load_config(cfg).params.get("page_title")
    return p


def latest_examples_run(exp: str, results: Path | None = None) -> Path | None:
    """The newest run of `exp` made by LensExamples (run dirs are named by timestamp)."""
    from bridge_jspace.pins import RESULTS_DIR

    runs = []
    for m in sorted((results or RESULTS_DIR).glob(f"{exp}/*/manifest.json")):
        if (
            json.loads(m.read_text())["config"]["target"].endswith(":LensExamples")
            and (m.parent / "examples.json").exists()
        ):
            runs.append(m.parent)
    return runs[-1] if runs else None


def export(run_dir: str | Path, root: Path | None = None) -> Path:
    """Render one examples run into `examples/<exp>/` (replacing the previous view): index.html, examples.md,
    artifact.html (for publishing) and a copy of slices/. The run in results/ stays the source of record."""
    import shutil

    run_dir = Path(run_dir)
    data = json.loads((run_dir / "examples.json").read_text())
    manifest = json.loads((run_dir / "manifest.json").read_text())
    groups = [Group(**g) for g in data["groups"]]
    p, model = _params_with_title(manifest), manifest["config"]["model"]["name"]
    p["examples_run"] = _repo_rel(run_dir)
    out = (root or _examples_root()) / manifest["config"]["name"]
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "index.html").write_text(render_html(groups, data["examples"], p, model))
    (out / "examples.md").write_text(render(groups, data["examples"], p, model))
    (out / "artifact.html").write_text(render_html(groups, data["examples"], p, model, standalone=False))
    if (run_dir / "slices").exists():
        shutil.copytree(run_dir / "slices", out / "slices")
    (out / "source.json").write_text(
        json.dumps({"examples_run": p["examples_run"], "groups_from": p["source_run"]}, indent=2)
    )
    return out


def export_all(exps: list[str] | None = None, root: Path | None = None) -> list[Path]:
    """Export the latest examples run of every experiment that has one."""
    from bridge_jspace.pins import REPO_ROOT

    exps = exps or sorted(d.parent.name for d in (REPO_ROOT / "scripts").glob("*/examples.yaml"))
    outs = [export(run, root) for e in exps if (run := latest_examples_run(e)) is not None]
    export_index(root)
    return outs


def export_index(root: Path | None = None) -> Path:
    """examples/index.html: one entry per exported experiment, with its groups and sizes."""
    root = root or _examples_root()
    entries = []
    for src in sorted(root.glob("*/source.json")):
        exp_dir = src.parent
        run = _from_repo(json.loads(src.read_text())["examples_run"])
        data = json.loads((run / "examples.json").read_text())
        manifest = json.loads((run / "manifest.json").read_text())
        p = _params_with_title(manifest)
        groups = "".join(
            f"<li>{_esc(g['title'])} <span class='badge'>{g['n_total']}</span></li>" for g in data["groups"]
        )
        entries.append(
            f"<section class='card'><h3><a href='{_esc(exp_dir.name)}/index.html'>{_esc(p.get('page_title') or exp_dir.name)}</a></h3>"
            f"<p class='meta'><code>{_esc(exp_dir.name)}</code> · {len(data['examples'])} examples · model "
            f"{_esc(manifest['config']['model']['name'])}</p><ul class='meta'>{groups}</ul></section>"
        )
    page = (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1,viewport-fit=cover'>"
        "<title>Bridge Lens Examples</title>"
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600'
        '&family=IBM+Plex+Sans:wght@400;600&display=swap">'
        f"<style>{_CSS}</style></head><body><header><h1>Bridge Lens Examples</h1><div class='lead'><p>Worked "
        "examples per experiment: two-hop questions grouped by what the lenses read, with layer-by-layer tables and "
        "interactive jlens views. Regenerate with <code>make examples-render</code>.</p></div></header>"
        f"<main>{''.join(entries) or '<p>No examples exported yet.</p>'}</main></body></html>"
    )
    root.mkdir(parents=True, exist_ok=True)
    (root / "index.html").write_text(page)
    return root / "index.html"


def serve(port: int = 8000, open_browser: bool = True) -> None:
    """Export all examples, then serve examples/ on http://localhost:<port>/ until interrupted."""
    import contextlib
    import functools
    import http.server
    import webbrowser

    export_all()
    root = _examples_root()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://localhost:{port}/index.html"
        print(f"serving {root} at {url}  (Ctrl-C to stop; on a pod: ssh -L {port}:localhost:{port} <host>)")
        if open_browser:
            webbrowser.open(url)
        with contextlib.suppress(KeyboardInterrupt):
            httpd.serve_forever()


if __name__ == "__main__":
    # uv run python -m bridge_jspace.examples export [exp ...]   render the latest examples runs into examples/
    # uv run python -m bridge_jspace.examples serve [port]       export, then serve examples/ and open the browser
    import sys

    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else "export"), sys.argv[2:]
    if cmd == "export":
        for out in export_all(args or None):
            print(out)
        print(_examples_root() / "index.html")
    elif cmd == "serve":
        serve(int(args[0]) if args else 8000, open_browser="--no-browser" not in args)
    else:
        raise SystemExit("usage: python -m bridge_jspace.examples [export [exp ...] | serve [port] [--no-browser]]")
