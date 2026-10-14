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
            records.append(rec)

        self.save_json("examples.json", {"groups": [asdict(g) for g in groups], "examples": records})
        self.path("examples.md").write_text(render(groups, records, p, self.cfg.model.name))
        self.path("examples.html").write_text(render_html(groups, records, p, self.cfg.model.name))
        self.log.info(f"wrote {self.path('examples.md')} and examples.html")
        return {
            "sanity": sanity,
            "source_run": p["source_run"],
            "groups": {g.key: g.n_total for g in groups},
            "n_examples": len(records),
        }


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
:root{--bg:#fcfcfb;--panel:#f9f9f7;--ink:#0b0b0b;--muted:#52514e;--faint:#898781;--line:#e1e0d9;
--bridge:#2a78d6;--bridge-bg:rgba(42,120,214,.14);--answer:#c2410c;--answer-bg:rgba(235,104,52,.16);
--ctrl-bg:rgba(137,135,129,.18);--heat:42,120,214}
@media (prefers-color-scheme:dark){:root{--bg:#1a1a19;--panel:#0d0d0d;--ink:#f0efec;--muted:#c3c2b7;
--faint:#898781;--line:#2c2c2a;--bridge:#5598e7;--answer:#f08a5d;--heat:85,152,231}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,sans-serif}
header{padding:16px 20px;border-bottom:1px solid var(--line)}h1{font-size:18px;margin:0 0 6px}
.lead{color:var(--muted);max-width:110ch;margin:0}.layout{display:flex}
nav{position:sticky;top:0;align-self:flex-start;width:280px;flex:none;height:100vh;overflow:auto;padding:12px 16px;
border-right:1px solid var(--line);background:var(--panel)}nav h4{margin:12px 0 4px;font-size:13px}
nav a{display:block;color:var(--muted);text-decoration:none;font:12px ui-monospace,monospace;padding:1px 0}
nav a:hover{color:var(--ink)}main{flex:1;min-width:0;padding:12px 20px 40px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 12px}
.chips button{border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:14px;padding:3px 10px;
cursor:pointer;font-size:12px}.chips button.on{background:var(--ink);color:var(--bg)}
section.group>h2{font-size:16px;margin:24px 0 2px}.def{color:var(--muted);margin:0 0 10px}
.card{border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:12px 0;background:var(--bg)}
.card h3{font:600 14px ui-monospace,monospace;margin:0 0 6px}.badge{display:inline-block;font:11px system-ui;
padding:1px 7px;border-radius:9px;background:var(--ctrl-bg);color:var(--muted);margin-left:6px}
.prompt{font:13px ui-monospace,monospace;background:var(--panel);padding:6px 8px;border-radius:6px;margin:6px 0}
.meta{color:var(--muted);margin:2px 0}.b{color:var(--bridge);font-weight:600}.a{color:var(--answer);font-weight:600}
.scroll{overflow-x:auto}table{border-collapse:collapse;margin:8px 0;font-size:12px}
th,td{border-bottom:1px solid var(--line);padding:3px 6px;text-align:left;vertical-align:top;white-space:nowrap}
th{color:var(--faint);font-weight:500}td.l{color:var(--faint);font-variant-numeric:tabular-nums}
.w{display:inline-block;padding:0 4px;margin:1px 2px 1px 0;border-radius:4px;font-family:ui-monospace,monospace}
.w.bridge{background:var(--bridge-bg);color:var(--bridge);font-weight:600}
.w.answer{background:var(--answer-bg);color:var(--answer);font-weight:600}.w.ctrl{background:var(--ctrl-bg)}
.r{display:block;color:var(--faint);font-size:11px}.r .hit{color:var(--ink);font-weight:600}
td.heat{font-family:ui-monospace,monospace;text-align:center;min-width:70px}td.heat small{color:var(--ink);opacity:.75}td.heat .w.bridge{background:none;color:var(--ink);text-decoration:underline 2px}
h4.t{margin:12px 0 0;font-size:13px}
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


def render_html(groups: list[Group], records: list[dict[str, Any]], p: dict[str, Any], model: str) -> str:
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
        body += [_card_html(r, g.key, p) for r in recs]
        body.append("</section>")
    title = f"Examples: {p['title']}"
    lead = (
        f"Source run <code>{_esc(p['source_run'])}</code>, model {_esc(model)}. Examples drawn at random with seed "
        f"{p['seed_examples']}, up to {p['per_group']} per group; groups can overlap. "
        '<span class="w bridge">bridge</span> <span class="w answer">answer</span> <span class="w ctrl">distractor</span>. '
        "B / A: word rank of the bridge / answer (1 = top; spaces and punctuation removed; bold if in the top 10)."
    )
    return (
        f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' "
        f"content='width=device-width,initial-scale=1'><title>{_esc(title)}</title><style>{_CSS}</style></head><body>"
        f"<header><h1>{_esc(title)}</h1><p class='lead'>{lead}</p></header><div class='layout'>"
        f"<nav>{''.join(nav)}</nav><main><div class='chips'>{''.join(chips)}</div>{''.join(body)}</main></div>"
        f"<script>{_JS}</script></body></html>"
    )


def _card_html(r: dict[str, Any], group: str, p: dict[str, Any]) -> str:
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


def rerender(run_dir: str | Path) -> Path:
    """Write examples.md and examples.html for a finished examples run into a new `<run_dir>/render-<timestamp>/`."""
    from datetime import datetime

    run_dir = Path(run_dir)
    data = json.loads((run_dir / "examples.json").read_text())
    manifest = json.loads((run_dir / "manifest.json").read_text())
    groups = [Group(**g) for g in data["groups"]]
    p, model = manifest["config"]["params"], manifest["config"]["model"]["name"]
    out = run_dir / f"render-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    (out / "examples.md").write_text(render(groups, data["examples"], p, model))
    (out / "examples.html").write_text(render_html(groups, data["examples"], p, model))
    return out


if __name__ == "__main__":
    # uv run python -m bridge_jspace.examples <examples run dir>   (re-render md + html, no model needed)
    import sys

    print(rerender(sys.argv[1]))
