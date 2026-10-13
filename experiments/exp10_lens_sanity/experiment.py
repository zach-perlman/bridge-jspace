"""exp10_lens_sanity: do the lenses read two-hop intermediates on this model at all?

1. Sanity gate: known fact, HF parity, our readout == jlens's `apply`. Any failure stops the run.
2. lens-eval-multihop pass@k (paper protocol): readout at the last prompt token (the token right
   before `target`), min rank over the reader's layers; pass@k = mean over items of the fraction
   of `intermediates` with rank < k. Baseline: the logit lens on the same layers.
3. Positive control (probe-swap items, e.g. Hungary next to "Hungarian"): bridge vs same-category
   distractor (`swap_to`) ranks over every layer x position.
"""

from __future__ import annotations

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
from bridge_jspace.sanity import check_hf_parity, check_known_fact, check_reference_readout
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

        sanity = self._sanity()
        if not all(c["passed"] for c in sanity.values()):
            raise RuntimeError(f"sanity failed, see {self.path('sanity.json')}")

        items = lens_eval_multihop_items()[: p.get("limit")]
        rows, item_meta = self._multihop(items, readers, layers)
        self.save_jsonl("multihop_ranks.jsonl", rows)
        self.save_jsonl("multihop_items.jsonl", item_meta)

        controls = self._controls(readers, layers)
        self.save_jsonl("control_ranks.jsonl", controls)

        summary = {
            "model": self.cfg.model.name,
            "readers": {name: [layers[name][0], layers[name][-1]] for name in readers},
            "sanity": {name: c["passed"] for name, c in sanity.items()},
            **self._aggregate(rows, item_meta, list(readers)),
            "controls": _control_summary(controls),
        }
        plot_run(self.run_dir)
        return summary

    # ---- 1. sanity gate -------------------------------------------------------------------

    def _sanity(self) -> dict[str, dict[str, Any]]:
        p = self.params
        checks = {
            "known_fact": check_known_fact(self.model, p["fact_prompt"], p["fact_expected"]),
            "hf_parity": check_hf_parity(self.model, p["parity_prompts"], p["parity_atol"]),
        }
        for name, lens in self.lenses.items():
            checks[f"reference_readout_{name}"] = check_reference_readout(self.model, lens, p["parity_prompts"][0])
        self.save_json("sanity.json", checks)
        for name, c in checks.items():
            self.log.info(f"[{'PASS' if c['passed'] else 'FAIL'}] {name} {c}")
        return checks

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
        p = self.params
        ks, n_boot, seed = p["ks"], p["n_boot"], self.cfg.seed
        names = [m["name"] for m in meta]
        subsets = {
            "all": names,
            "model_correct": [m["name"] for m in meta if m["model_correct"]],
            "all_single_token": [m["name"] for m in meta if m["all_single_token"]],
        }
        # score[reader][k][item] = fraction of the item's intermediates with rank < k
        score: dict[str, dict[int, dict[str, float]]] = {}
        for r in readers:
            score[r] = {}
            for k in ks:
                by_item: dict[str, list[bool]] = {}
                for row in rows:
                    if row["reader"] == r:
                        by_item.setdefault(row["name"], []).append(row["min_rank"] < k)
                score[r][k] = {n: sum(v) / len(v) for n, v in by_item.items()}

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
        return {
            "n_items": len(meta),
            "n_model_correct": len(subsets["model_correct"]),
            "n_all_single_token": len(subsets["all_single_token"]),
            "pass_at_k": pass_at_k,
            "diff_vs_logit": diff_vs_logit,
            "ci": f"95% percentile bootstrap over items, n_boot={n_boot}, seed={seed}",
        }

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
