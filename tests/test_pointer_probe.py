"""pointer_probe's pure helpers (no model): nearest class mean, out-of-fold predictions, entity-cluster bootstrap."""

import pytest
import torch

import scripts.pointer_probe as PP


def test_nearest_mean_masks_absent_classes():
    mu = torch.stack([torch.zeros(2, 3), torch.ones(2, 3), 5 * torch.ones(2, 3)])
    x = torch.stack([0.1 * torch.ones(2, 3), 0.9 * torch.ones(2, 3), 4 * torch.ones(2, 3)])
    assert PP.nearest_mean(x, mu).tolist() == [0, 1, 2]
    assert PP.nearest_mean(x, mu, torch.tensor([True, True, False])).tolist() == [0, 1, 1]
    big = torch.randn(70, 2, 3)  # more items than one chunk
    assert PP.nearest_mean(big, mu).shape == (70,)


def test_cv_predictions_are_out_of_fold_and_find_a_planted_code():
    torch.manual_seed(0)
    dirs = torch.randn(5, 16) * 3
    y = torch.arange(60) % 5
    x = torch.randn(60, 2, 16) + dirs[y][:, None, :]
    pred = PP.cv_predictions(x, y)
    assert (pred >= 0).all() and float((pred == y).float().mean()) > 0.9
    shuffled = y[torch.randperm(60, generator=torch.Generator().manual_seed(1))]
    assert float((PP.cv_predictions(x, shuffled) == shuffled).float().mean()) < 0.5


def test_entity_boot_resamples_entities_within_domain():
    hits = [1, 1, 0, 0, 1, 1]
    doms = ["a", "a", "a", "b", "b", "b"]
    ents = ["x", "x", "y", "z", "z", "w"]
    m, lo, hi = PP.entity_boot(hits, doms, ents, n_boot=400)
    assert m == pytest.approx(4 / 6) and lo <= m <= hi
    m1, lo1, hi1 = PP.entity_boot([1, 1, 1], ["a", "a", "a"], ["x", "y", "z"], n_boot=50)
    assert (m1, lo1, hi1) == (1.0, 1.0, 1.0)
