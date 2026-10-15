"""exp16_nla: does a second, independent verbalizer, the NLA, name the bridge where the J-lens and J++ both miss it?

exp15 with another reader: the NLA (bridge_jspace.nla: a separate 27B verbalizer trained on layer-42 activations of
Qwen3.6-27B; greedy, its published read contract) instead of the oracle lens, at layer 42 only. Same questions, read
positions, conditions (clean, after exp14's J++ bridge swap on the cue phrase, the mean activation), scoring and
analysis as exp15 (scripts.exp15_oracle_lens: `capture`, `build_reads`, `summarize`, `analyze`).

Two phases, since both 27B models do not fit one 80 GB card: Qwen3.6-27B captures every vector (saved to
cache/exp16_nla/<run>/vectors.pt) and is unloaded; then the NLA is loaded, passes its gate and reads them.
"""

from __future__ import annotations

import gc
from typing import Any

import torch

from bridge_jspace.experiment import Experiment
from bridge_jspace.items import entity_and_answer_pools, load_labelled_items
from bridge_jspace.pins import CACHE_DIR, REPO_ROOT
from bridge_jspace.utils import progress
from scripts.exp15_oracle_lens.experiment import batches, build_reads, capture, exp14_agreement, summarize


class NLAReads(Experiment):
    def run(self) -> dict[str, Any]:
        from bridge_jspace.model import load_model
        from bridge_jspace.nla import LAYER, NLA, nla_sanity_gate
        from bridge_jspace.tokens import concept_token

        p = self.params
        assert p["read_layers"] == [LAYER], f"the NLA reads layer {LAYER} only"

        # Phase 1: Qwen3.6-27B captures every vector, then leaves the GPU.
        model = load_model()  # part B's loader, as exp14 / exp15
        tokenizer = model.tokenizer
        all_items = load_labelled_items(REPO_ROOT / p["labels_file"], p["labels_sha256"])
        entity_pool, _ = entity_and_answer_pools(tokenizer, all_items)
        items = [it for it in all_items if it["status"] == "eligible"][: p.get("limit")]
        item_rows, vectors = capture(model, items, p)
        facts = []
        for f in p["sanity"]["facts"]:
            _, h = model.run(model.encode(f["prompt"]), record=(LAYER,))
            facts.append(h[LAYER][-1].cpu())
        fact_vectors = torch.stack(facts)
        cache = CACHE_DIR / "exp16_nla" / self.run_dir.name
        cache.mkdir(parents=True, exist_ok=True)
        torch.save({"vectors": vectors, "facts": fact_vectors, "item_rows": item_rows}, cache / "vectors.pt")
        del model
        gc.collect()
        torch.cuda.empty_cache()
        left = torch.cuda.memory_allocated() / 2**30
        assert left < 4, f"{left:.1f} GiB still allocated after unloading Qwen3.6-27B"

        # Phase 2: the NLA, its gate, then every reading.
        nla = NLA()
        checks = nla_sanity_gate(nla, fact_vectors, p["sanity"], p["max_new_tokens"], self.cfg.seed)
        self.save_json("sanity.json", checks)
        if not checks["passed"]:
            raise RuntimeError(f"NLA sanity gate failed: {checks['failed']} (see sanity.json)")
        texts: list[str] = [""] * len(vectors)
        for batch in progress(batches(vectors, p["read_layers"], p["batch_size"]), "read"):
            stack = torch.stack([vectors[i][4] for i in batch])
            for i, text in zip(batch, nla.read(stack, p["max_new_tokens"]), strict=True):
                texts[i] = text
        firsts: list[torch.Tensor | None] = [None] * len(vectors)  # the NLA writes prose, not bullets

        reads = build_reads(
            vectors, texts, firsts, items, entity_pool, lambda w: concept_token(tokenizer, w), item_rows, p
        )
        self.save_jsonl("items.jsonl", item_rows)
        self.save_jsonl("reads.jsonl", reads)
        return {
            "model": "Qwen3.6-27B (part B's loader) captures; the NLA (pins.NLA_*) reads",
            "n_questions": len(items),
            "entity_pool": len(entity_pool),
            "checks": {**checks, "exp14_top_word_agree": exp14_agreement(item_rows)},
            **summarize(reads, item_rows, p),
            "decision_rule": p["decision"],
        }
