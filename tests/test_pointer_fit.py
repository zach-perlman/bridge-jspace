"""pointer_fit's pure helpers (no model): entity split, class means, subspaces, projections, decodability, norms."""

import math

import pytest
import torch

import scripts.pointer_fit as PF


def test_entity_split_is_seeded_disjoint_and_covers_the_pool():
    pool = ["dog", "cat", "cow", "pig", "bee"]
    a, b = PF.entity_split(pool)
    assert sorted(a + b) == sorted(pool) and not set(a) & set(b)
    assert (a, b) == PF.entity_split(list(reversed(pool)))  # order-free and deterministic
    assert len(a) == 3 and len(b) == 2


def test_class_means_and_between_basis():
    torch.manual_seed(0)
    d, p = 16, 3
    slot_dirs = torch.randn(PF.N_SLOTS, d)
    y = torch.arange(50) % PF.N_SLOTS
    x = torch.randn(50, p, d) * 0.01 + slot_dirs[y][:, None, :]
    mu, m = PF.class_means(x, y)
    assert mu.shape == (PF.N_SLOTS, p, d) and m.shape == (p, d)
    assert torch.allclose(mu[2, 1], slot_dirs[2], atol=0.02)
    basis = PF.between_basis(mu, m, 4)
    assert torch.allclose(basis @ basis.T, torch.eye(4), atol=1e-4)
    # the slot deviations lie (almost) inside the rank-4 between-class subspace (5 classes -> rank 4 per token)
    dev = (mu - m).reshape(-1, d)
    assert float((PF.project(dev, basis) - dev).norm() / dev.norm()) < 0.05


def test_empty_class_falls_back_to_the_grand_mean():
    x = torch.randn(6, 2, 4)
    y = torch.tensor([0, 0, 1, 1, 2, 2])
    mu, m = PF.class_means(x, y)
    assert torch.allclose(mu[4], m)


def test_projection_and_matched_norms():
    basis = torch.eye(5)[:2]
    v = torch.tensor([[1.0, 2.0, 3.0, 0.0, 0.0]])
    inside = PF.project(v, basis)
    assert torch.allclose(inside, torch.tensor([[1.0, 2.0, 0.0, 0.0, 0.0]]))
    assert torch.allclose(inside + (v - inside), v)  # the two parts add back to the full vector
    norms = torch.tensor([0.0, 2.0, 5.0])
    out = PF.matched(torch.randn(3, 5), norms)
    assert torch.allclose(out.norm(dim=-1), norms, atol=1e-5)
    shared = PF.matched(torch.tensor([3.0, 4.0, 0, 0, 0]), norms)  # one direction for every token
    assert torch.allclose(shared[2], torch.tensor([3.0, 4.0, 0, 0, 0]))


def test_nearest_mean_decodes_a_planted_slot_and_not_shuffled_labels():
    torch.manual_seed(1)
    slot_dirs = torch.randn(PF.N_SLOTS, 32) * 3
    y = torch.arange(100) % PF.N_SLOTS
    x = torch.randn(100, 2, 32) + slot_dirs[y][:, None, :]
    assert PF.nearest_mean_cv(x, y) > 0.95
    shuffled = y[torch.randperm(100, generator=torch.Generator().manual_seed(0))]
    assert PF.nearest_mean_cv(x, shuffled) < 0.45


def test_principal_cosines():
    e = torch.eye(6)
    assert torch.allclose(PF.principal_cosines(e[:2], e[:3]), torch.ones(2), atol=1e-5)
    assert float(PF.principal_cosines(e[:2], e[3:5]).max()) < 1e-5
    tilted = torch.stack([e[0] + e[3]]) / math.sqrt(2)
    assert float(PF.principal_cosines(tilted, e[:1])[0]) == pytest.approx(1 / math.sqrt(2), abs=1e-5)


def test_boot_diff_and_statement_spans():
    pt, lo, hi = PF.boot_diff([1, 1, 1, 0], [0, 0, 0, 0], n_boot=200)
    assert pt == pytest.approx(0.75) and lo <= pt <= hi
    ctx = "The cow's locker is 5. The dog's locker is 3. The pig's locker is 7."
    text = "<|im_start|>user\n" + ctx + "\nWhich locker belongs to the cow?"
    spans = PF.statement_spans(text, ctx)
    assert [text[s:e] for s, e in spans] == [
        "The cow's locker is 5.",
        "The dog's locker is 3.",
        "The pig's locker is 7.",
    ]


def test_conditions_follow_the_configured_ranks():
    cfg = {"ks": [1, 4]}
    assert PF.conds_for(cfg, "RL") == ("slot", "sub1", "sub4", "shuffled", "random", "lens", "span", "rest")
    assert PF.conds_for(cfg, "RR") == PF.CONDS_RR
