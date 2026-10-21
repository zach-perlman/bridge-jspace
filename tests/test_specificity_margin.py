"""Toy tests (CPU, no model) for the 2026-10-21 additions: the unembedding knock-out dictionary (ablate_v2 unembed10)
and C1's margin-matched gap (c1_v2.margin_matched)."""

import math
import random
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace.ablate import LensDictionary, top_span_removal
from scripts.ablate_v2 import top_k
from scripts.c1_v2 import margin_matched


def test_unembed_conditions_are_top10():
    assert top_k("unembed10") == 10 and top_k("unembed10_rot") == 10 and top_k("paper10_keepown_rot") == 10


def test_unembed_dictionary_is_the_logit_lens():
    g = torch.Generator().manual_seed(0)
    wg, x = torch.randn(50, 8, generator=g), torch.randn(3, 8, generator=g)
    dic = LensDictionary(wg, torch.eye(8))
    assert torch.allclose(dic.logits(x), x @ wg.T, atol=1e-5)
    assert torch.allclose(dic.atoms(torch.tensor([4])), wg[4:5] / wg[4].norm(), atol=1e-6)
    proj, top = top_span_removal(dic, x, 2, return_chosen=True)
    assert torch.equal(top[0].sort().values, (x[:1] @ wg.T).topk(2).indices[0].sort().values)
    resid = x - proj  # what is left is orthogonal to the removed atoms
    assert torch.allclose((resid[0] @ dic.atoms(top[0]).T), torch.zeros(2), atol=1e-4)


def test_margin_matching_removes_a_pure_confidence_gap():
    # loss depends only on the margin (smoothly); memory-final items have lower margins: a raw gap, no matched gap
    rng = random.Random(1)
    items = []
    for w, mu in (("PP", 5.5), ("MP", 5.0), ("PM", 4.0), ("MM", 3.8)):
        for _ in range(400):
            m = round(rng.gauss(mu, 1.0) * 8) / 8  # rounded, so ties are common
            items.append((w, m, int(rng.random() < 1 / (1 + math.exp(3 * (m - 4.5))))))
    out = margin_matched(items)
    assert out["raw_gap"] > 0.2
    assert abs(out["matched_gap"]) < 0.05 and out["matched_gap_ci"][0] < 0 < out["matched_gap_ci"][1]
    assert abs(out["gap_at_prompt_margins"]) < 0.15 and abs(out["gap_at_memory_margins"]) < 0.15


def test_margin_matching_keeps_a_real_gap():
    # one margin for all: memory-final items all lose, half the prompt-final ones do
    items = [(w, 4.0, 1) for w in ("PM", "MM") for _ in range(25)]
    items += [(w, 4.0, i % 2) for w in ("PP", "MP") for i in range(50)]
    out = margin_matched(items)
    assert out["raw_gap"] == 0.5 and out["matched_gap"] == 0.5 and out["matched_n"] == 50
