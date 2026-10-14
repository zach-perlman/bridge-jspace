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
        md = render(groups, records, p, self.cfg.model.name)
        self.path("examples.md").write_text(md)
        self.log.info(f"wrote {self.path('examples.md')}")
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
