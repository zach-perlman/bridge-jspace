"""exp10_lens_sanity: do the lenses read two-hop intermediates on this model at all?

1. Sanity gate: known fact, HF parity, our readout == jlens's `apply`. Any failure stops the run.
2. lens-eval-multihop pass@k: readout at the last prompt token (the token right before `target`), min rank over the
   reader's layers; pass@k = share of items with any of their `intermediates` at rank < k (an item's several
   intermediates are forms of one bridge, '5' / 'five'). The paper's rule (mean over items of the fraction of
   `intermediates` with rank < k) is kept as `pass_at_k_fraction`. Baseline: the logit lens on the same layers.
3. Positive control (probe-swap items, e.g. Hungary next to "Hungarian"): bridge vs same-category
   distractor (`swap_to`) ranks over every layer x position.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from bridge_jspace.experiment import Experiment
from bridge_jspace.pins import lens_eval_multihop_items, probe_swap_items
from bridge_jspace.readout import (
    Reader,
    continuation_first_token,
    rank_grid,
    ranks_of,
    residuals,
    word_tokens,
)
from bridge_jspace.stats import bootstrap_mean
from bridge_jspace.utils import progress

from .plot import plot_run


class LensSanity(Experiment):
    def run(self) -> dict[str, Any]:
        p = self.params
        lm = self.model.lm
        if "logit" in self.lenses:
            raise ValueError("'logit' is reserved for the logit-lens baseline; rename that lens")
        readers: dict[str, Reader] = {"logit": None, **self.lenses}
        layers = {name: list(range(lm.n_layers - 1)) if r is None else r.source_layers for name, r in readers.items()}

        sanity = self.sanity_gate()

        items = lens_eval_multihop_items()[: p.get("limit")]
        rows, item_meta = self._multihop(items, readers, layers)
        item_meta = label_items(item_meta, items)
        self.save_jsonl("multihop_ranks.jsonl", rows)
        self.save_jsonl("multihop_items.jsonl", item_meta)

        controls = self._controls(readers, layers)
        self.save_jsonl("control_ranks.jsonl", controls)

        summary = {
            "model": self.cfg.model.name,
            "readers": {name: [layers[name][0], layers[name][-1]] for name in readers},
            "sanity": sanity,
            **self._aggregate(rows, item_meta, list(readers)),
            "controls": _control_summary(controls),
        }
        plot_run(self.run_dir)
        return summary

    def _prompt(self, item: dict[str, Any]) -> str:
        # Most upstream prompts end in a space, which Qwen's BPE leaves as a lone " " token: the
        # readout then sits on an out-of-distribution token. Whether to strip it is a design choice.
        return item["prompt"].rstrip() if self.params["strip_trailing_space"] else item["prompt"]

    # ---- 2. lens-eval-multihop ------------------------------------------------------------

    def _multihop(
        self, items: list[dict[str, Any]], readers: dict[str, Reader], layers: dict[str, list[int]]
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        lm, tok = self.model.lm, self.model.tokenizer
        final = lm.n_layers - 1
        record_at = sorted({final}.union(*layers.values()))
        rows, meta = [], []
        for item in progress(items, "multihop items"):
            prompt = self._prompt(item)
            ids = lm.encode(prompt)
            resid = residuals(lm, ids, record_at)
            # Model's own greedy next token at the readout position, to split items it gets right.
            out_logits = lm.unembed(resid[final][[-1]]).float()
            target_id = continuation_first_token(tok, prompt, item["target"])
            target_rank = int(ranks_of(out_logits, [target_id])[0, 0])
            words = [word_tokens(tok, w) for w in item["intermediates"]]
            meta.append(
                {
                    "name": item["name"],
                    "readout_token": tok.decode(ids[0, -1:]),
                    "model_top1": tok.decode(out_logits.argmax(-1)),
                    "target": item["target"],
                    "target_first_token": tok.decode([target_id]),
                    "target_rank": target_rank,
                    "model_correct": target_rank == 0,
                    "all_single_token": all(w.single_token for w in words),
                }
            )
            all_ids = [t for w in words for t in w.ids]
            for name, reader in readers.items():
                grid = rank_grid(lm, reader, resid, layers[name], all_ids, positions=[-1])[:, 0]  # [L, ids]
                start = 0
                for w in words:
                    per_layer = grid[:, start : start + len(w.ids)].min(-1).values  # min over variants
                    start += len(w.ids)
                    best = int(per_layer.argmin())
                    rows.append(
                        {
                            "name": item["name"],
                            "reader": name,
                            "intermediate": w.word,
                            "pieces": w.pieces,
                            "single_token": w.single_token,
                            "min_rank": int(per_layer[best]),
                            "argmin_layer": layers[name][best],
                            "layers": layers[name],
                            "ranks": per_layer.tolist(),
                        }
                    )
        return rows, meta

    def _aggregate(self, rows: list[dict[str, Any]], meta: list[dict[str, Any]], readers: list[str]) -> dict[str, Any]:
        return aggregate(rows, meta, readers, self.params["ks"], self.params["n_boot"], self.cfg.seed)

    # ---- 3. positive control --------------------------------------------------------------

    def _controls(self, readers: dict[str, Reader], layers: dict[str, list[int]]) -> list[dict[str, Any]]:
        lm, tok = self.model.lm, self.model.tokenizer
        by_name = {it["name"]: it for it in probe_swap_items()}
        record_at = sorted(set().union(*layers.values()))
        rows = []
        for name in progress(self.params["control_items"], "control items"):
            item = by_name[name]
            ids = lm.encode(self._prompt(item))
            prompt_tokens = [tok.decode([t]) for t in ids[0].tolist()]
            resid = residuals(lm, ids, record_at)
            for role, word in (("bridge", item["intermediate"]), ("distractor", item["swap_to"])):
                w = word_tokens(tok, word)
                for rname, reader in readers.items():
                    grid = rank_grid(lm, reader, resid, layers[rname], w.ids).min(-1).values  # [L, seq]
                    best = int(grid.argmin())
                    li, pos = divmod(best, grid.shape[1])
                    rows.append(
                        {
                            "name": name,
                            "role": role,
                            "word": word,
                            "pieces": w.pieces,
                            "reader": rname,
                            "min_rank": int(grid.min()),
                            "argmin_layer": layers[rname][li],
                            "argmin_position": pos,
                            "argmin_token": prompt_tokens[pos],
                            "last_position_min_rank": int(grid[:, -1].min()),
                            "prompt_tokens": prompt_tokens,
                            "layers": layers[rname],
                            "ranks": grid.tolist(),  # [layer][position]
                        }
                    )
        return rows


NUMBER_WORDS = frozenset(
    [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
        "hundred",
        "first",
        "second",
        "third",
        "fourth",
        "fifth",
        "sixth",
        "seventh",
        "eighth",
        "ninth",
        "tenth",
        "eleventh",
        "twelfth",
    ]
)


def bridge_kind(intermediates: list[str]) -> str:
    """'number' if any form is a numeral or a number word ('6', 'six', 'third'), 'letter' if every form is one
    letter ('H', a chemical symbol), else 'word'."""
    forms = [w.strip() for w in intermediates]
    if any(f.isdigit() or f.lower() in NUMBER_WORDS for f in forms):
        return "number"
    if all(len(f) == 1 and f.isalpha() for f in forms):
        return "letter"
    return "word"


def bridge_in_prompt(prompt: str, intermediates: list[str]) -> bool:
    """Whether a form of the bridge is written in the prompt as a word of its own (not inside another word: 'H' in
    'The' does not count)."""
    return any(
        re.search(rf"(?<![A-Za-z0-9]){re.escape(w.strip())}(?![A-Za-z0-9])", prompt, re.IGNORECASE)
        for w in intermediates
    )


def label_items(meta: list[dict[str, Any]], items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """meta rows with each item's bridge kind and whether its bridge is named in the prompt."""
    by_name = {it["name"]: it for it in items}
    return [
        m | {"bridge_kind": bridge_kind(by_name[m["name"]]["intermediates"]),
             "bridge_in_prompt": bridge_in_prompt(by_name[m["name"]]["prompt"], by_name[m["name"]]["intermediates"])}
        for m in meta
    ]  # fmt: skip


def item_scores(rows: list[dict[str, Any]], reader: str, k: int, rule: str) -> dict[str, float]:
    """Per item, from its intermediates' min ranks: `any` = 1 if any of them is ranked below k, `fraction` = the share
    that is (the paper's rule)."""
    hits: dict[str, list[bool]] = {}
    for row in rows:
        if row["reader"] == reader:
            hits.setdefault(row["name"], []).append(row["min_rank"] < k)
    return {n: float(any(v)) if rule == "any" else sum(v) / len(v) for n, v in hits.items()}


def aggregate(
    rows: list[dict[str, Any]], meta: list[dict[str, Any]], readers: list[str], ks: list[int], n_boot: int, seed: int
) -> dict[str, Any]:
    """pass@k per subset and reader, with bootstrap CIs over items. Primary rule `any`: an item counts as found if any
    of its `intermediates` is in the top k; in this set an item's several intermediates are forms of one bridge
    ('5' / 'five'), so finding one form finds the bridge. `*_fraction` keeps the paper's rule (the fraction of an
    item's intermediates found) for comparison with published numbers."""
    names = [m["name"] for m in meta]
    single = [m for m in meta if m["all_single_token"]]
    subsets = {
        "all": names,
        "model_correct": [m["name"] for m in meta if m["model_correct"]],
        "all_single_token": [m["name"] for m in single],
        # by bridge kind and naming (label_items); absent from rows saved before the labels
        **{f"{kind}_bridges": [m["name"] for m in single if m.get("bridge_kind") == kind]
           for kind in ("word", "number", "letter")},
        "bridge_named_in_prompt": [m["name"] for m in single if m.get("bridge_in_prompt")],
        "bridge_not_in_prompt": [m["name"] for m in single if m.get("bridge_in_prompt") is False],
    }  # fmt: skip
    out: dict[str, Any] = {
        "n_items": len(meta),
        "n_model_correct": len(subsets["model_correct"]),
        "n_all_single_token": len(subsets["all_single_token"]),
    }
    for rule, suffix in (("any", ""), ("fraction", "_fraction")):
        score = {r: {k: item_scores(rows, r, k, rule) for k in ks} for r in readers}
        pass_at_k: dict[str, Any] = {}
        diff_vs_logit: dict[str, Any] = {}
        for subset, members in subsets.items():
            if not members:
                continue
            pass_at_k[subset] = {"n": len(members)}
            for r in readers:
                pass_at_k[subset][r] = {
                    k: _ci(bootstrap_mean([score[r][k][n] for n in members], n_boot, seed)) for k in ks
                }
            diff_vs_logit[subset] = {
                r: {
                    k: _ci(bootstrap_mean([score[r][k][n] - score["logit"][k][n] for n in members], n_boot, seed))
                    for k in ks
                }
                for r in readers
                if r != "logit"
            }
        out[f"pass_at_k{suffix}"], out[f"diff_vs_logit{suffix}"] = pass_at_k, diff_vs_logit
    out["ci"] = f"95% percentile bootstrap over items, n_boot={n_boot}, seed={seed}"
    return out


def analyze(run_dir: str | Path) -> Path:
    """Re-aggregate a finished run's saved ranks with the current rules into a new `<run_dir>/analysis-<timestamp>/`
    (the run's own files are not touched); ks, n_boot and seed from its manifest."""
    run_dir = Path(run_dir)
    cfg = json.loads((run_dir / "manifest.json").read_text())["config"]

    def load(name: str) -> list[dict[str, Any]]:
        return [json.loads(x) for x in (run_dir / name).read_text().splitlines() if x.strip()]

    rows = load("multihop_ranks.jsonl")
    meta = label_items(load("multihop_items.jsonl"), lens_eval_multihop_items())
    readers = list(dict.fromkeys(r["reader"] for r in rows))
    out = run_dir / f"analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out.mkdir()
    p = cfg["params"]
    summary = {"source_run": str(run_dir), **aggregate(rows, meta, readers, p["ks"], p["n_boot"], cfg["seed"])}
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    return out


def _ci(t: tuple[float, float, float]) -> dict[str, float]:
    return {"mean": round(t[0], 4), "lo": round(t[1], 4), "hi": round(t[2], 4)}


def _control_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for r in rows:
        out.setdefault(r["name"], {}).setdefault(r["reader"], {})[r["role"]] = {
            "word": r["word"],
            "min_rank": r["min_rank"],
            "at": f"L{r['argmin_layer']} {r['argmin_token']!r}",
            "last_position_min_rank": r["last_position_min_rank"],
        }
    return out


if __name__ == "__main__":
    # uv run python -m scripts.exp10_lens_sanity.experiment analyze <run_dir>   (re-aggregate with the current rules)
    import sys

    if sys.argv[1:2] != ["analyze"] or len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(analyze(sys.argv[2]))
