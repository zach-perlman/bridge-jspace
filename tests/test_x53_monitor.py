"""x53_monitor (53.2): labels, the J++ part's OMP, the forward's position mapping, the lens parts (CPU fakes)."""

import sys
from pathlib import Path

import numpy as np
import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x53_monitor as M

VARIANTS = M.VARIANTS
PROSE = "Amy picked lithium. The locker of lithium is eight. The locker of the frog is six. Owen picked frog."
PROSE_S = "Amy picked frog. The locker of lithium is eight. The locker of the frog is six. Owen picked lithium."
JSON = '[{"item": "owl", "locker": 4}, {"item": "cat", "locker": 7}, {"item": "fly", "locker": 5}]'


def test_slots_prose_and_json():
    assert M.locker_order(PROSE, "prose") == ["lithium", "frog"]
    assert M.slot_of(PROSE, "prose", "frog") == (1, 2)
    assert M.slot_of(JSON, "json", "fly") == (2, 3)
    with pytest.raises(AssertionError):
        M.slot_of(JSON, "json", "dog")


def test_labels_per_variant():
    lab = M.labels(PROSE, PROSE_S, "prose", "lithium", "frog", ("8", "6"), ("3", "0"))
    assert lab["org"] == {"bridge": "lithium", "slot": 0, "n_slots": 2, "lookup": "8", "recall": "3"}
    assert lab["alt"] == {"bridge": "frog", "slot": 1, "n_slots": 2, "lookup": "6", "recall": "0"}
    moved = "Amy picked frog. The locker of the frog is six. The locker of lithium is eight. Owen picked lithium."
    with pytest.raises(AssertionError):
        M.labels(PROSE, moved, "prose", "lithium", "frog", ("8", "6"), ("3", "0"))


def test_omp_parts_match_x0_signed_omp():
    from scripts.exp04_brew_parts import signed_omp

    g = torch.Generator().manual_seed(0)
    dic = torch.nn.functional.normalize(torch.randn(300, 40, generator=g), dim=-1)
    x = torch.randn(7, 40, generator=g)
    parts, chosen = M.omp_parts(dic, x, (5, 12))
    assert chosen.shape == (7, 12)
    for k in (5, 12):
        assert torch.allclose(parts[k], signed_omp(dic, x, k), atol=1e-5)
    # the part is a projection: the residual is orthogonal to the chosen atoms
    res = (x - parts[12]).double()
    assert torch.allclose(torch.einsum("md,msd->ms", res, dic[chosen].double()), torch.zeros(7, 12, dtype=torch.double),
                          atol=1e-6)  # fmt: skip


class FakeModel:
    """model.run: block output at layer la, position q = la * 1000 + q (+ 0.5 for the recall's prompt past B)."""

    device = "cpu"

    def __init__(self, d: int = 3, b: int = 1):
        self.d, self.b = d, b

    def run(self, ids, record=()):
        n = ids.shape[1]
        is_recall = int(ids[0, -2]) == 99
        rec = {}
        for la in record:
            h = torch.zeros(n, self.d)
            for q in range(n):
                h[q] = la * 1000 + q + (0.5 if is_recall and q > self.b else 0.0)
            rec[la] = h
        logits = torch.zeros(10)
        logits[3 if not is_recall else 4] = 1.0
        return logits, rec

    def letter_token_ids(self):
        return torch.arange(100, 130)


def fake_items():
    pp = {"ids": {"org": [1, 2, 3, 7], "alt": [1, 5, 3, 7]}, "suffix": [0], "tok_A": 3, "tok_b": 3,
          "pos": {"org": {"B": 1, "T": 4}, "alt": {"B": 1, "T": 4}}}  # fmt: skip
    pm = {"ids": {"org": [1, 2, 3, 8, 99], "alt": [1, 5, 3, 8, 99]}, "suffix": [0], "tok_A": 4, "tok_b": 5,
          "pos": {"org": {"B": 1, "T": 5}, "alt": {"B": 1, "T": 5}}}  # fmt: skip
    return [{"scene": "s0", "readers": {"PP": pp, "PM": pm}}]


def test_forward_states_positions():
    items = fake_items()
    M.check_items(items)
    h, reads = M.forward_states(FakeModel(), items, (2, 4))
    assert h.shape == (2, 1, 2, 3, 3)
    assert h[0, 0, 0, 0, 0] == 2 * 1000 + 1  # B on the lookup's prompt
    assert h[1, 0, 1, 1, 0] == 4 * 1000 + 4  # T lookup, S
    assert h[0, 0, 0, 2, 0] == 2 * 1000 + 5 + 0.5  # T recall
    assert reads[0]["PP_org"] == {"top": 3, "right": True}
    assert reads[0]["PM_alt"] == {"top": 4, "right": False}
    assert reads[0]["b_gap_org"] == 0.0


def test_random_frame_is_x0s_basis():
    from scripts import statement_positions as SP

    for la, seed in ((4, 0), (6, 2)):
        want = SP.random_basis(64, torch.Generator().manual_seed(888 + la + 1000 * seed))[:, :10].double().numpy()
        assert np.allclose(M.random_frame(64, la, seed, 10), want, atol=1e-4)
    assert not np.allclose(M.random_frame(64, 4, 0, 10), M.random_frame(64, 4, 1, 10))


def test_fold_ids_keep_groups_together():
    groups = np.array([f"e{i % 13}" for i in range(80)])
    f0 = M.fold_ids(groups, 0)
    assert set(f0) == set(range(M.N_FOLDS))
    for g in set(groups):
        assert len(set(f0[groups == g])) == 1
    assert (M.fold_ids(groups, 0) == f0).all()
    assert not (M.fold_ids(groups, 1) == f0).all()


def test_span_coords_give_the_full_space_fit():
    rng = np.random.default_rng(0)
    xtr, xte = rng.normal(size=(30, 200)), rng.normal(size=(12, 200))
    ytr = np.array(["p", "q", "r"])[rng.integers(0, 3, 30)]
    ztr, zte = M.standardize(xtr, xte)
    ctr, cte = M.span_coords(ztr, zte)
    assert ctr.shape[1] <= 30
    assert np.allclose(ctr @ ctr.T, ztr @ ztr.T, atol=1e-8)  # the training geometry is kept
    assert np.allclose(cte @ ctr.T, zte @ ztr.T, atol=1e-8)
    assert (M.logistic(ctr, ytr, cte) == M.logistic(ztr, ytr, zte)).all()


def test_logistic_separates_and_gradient():
    from scipy.optimize import check_grad

    rng = np.random.default_rng(1)
    x = rng.normal(size=(60, 5))
    y = np.where(x[:, 0] > 0, "pos", "neg")
    assert (M.logistic(x, y, x) == y).mean() > 0.95
    assert (M.logistic(x, np.full(60, "only"), x[:3]) == "only").all()
    # the gradient of the objective as written (re-derived here on a 3-class problem)
    from scipy.special import logsumexp

    y3 = rng.integers(0, 3, 60)
    onehot = np.eye(3)[y3]

    def f(theta):
        w, b = theta[:15].reshape(5, 3), theta[15:]
        z = x @ w + b
        return 1.0 * float((logsumexp(z, axis=1) - z[np.arange(60), y3]).sum()) + 0.5 * float((w * w).sum())

    def g(theta):
        w, b = theta[:15].reshape(5, 3), theta[15:]
        z = x @ w + b
        p = np.exp(z - logsumexp(z, axis=1)[:, None]) - onehot
        return np.concatenate([(x.T @ p + w).ravel(), p.sum(0)])

    assert check_grad(f, g, rng.normal(size=18)) < 1e-4


def test_rule_labels():
    full_hi, full_lo = np.array([0.5, 0.9, 0.85]), np.array([0.5, 0.6, 0.7])
    assert M.rule_label(full_hi, np.array([0.3, 0.4, 0.5]), np.array([0.25, 0.35, 0.41]))["label"] == M.LABELS[0]
    assert M.rule_label(full_lo, np.array([0.3, 0.4, 0.5]), np.array([0.25, 0.35, 0.41]))["label"] == M.LABELS[2]
    r = M.rule_label(full_hi, np.array([0.3, 0.85, 0.5]), np.array([0.25, 0.5, 0.41]))
    assert r["label"] == M.LABELS[1]
    assert r["carry_layers_idx"] == [1]
    # J++ >= 0.8 but only 0.25 above random: in between; a gap of 0.11 at one layer breaks "blind"
    assert M.rule_label(full_hi, np.array([0.3, 0.85, 0.5]), np.array([0.25, 0.6, 0.41]))["label"] == M.LABELS[2]
    assert M.rule_label(full_hi, np.array([0.3, 0.4, 0.62]), np.array([0.25, 0.35, 0.51]))["label"] == M.LABELS[2]
    # at the bars exactly (EPS): within 0.10 is blind; 0.8 and 0.3 carry
    assert M.rule_label(full_hi, np.array([0.5, 0.6]), np.array([0.4, 0.5]))["label"] == M.LABELS[0]
    assert M.rule_label(full_hi, np.array([0.8]), np.array([0.5]))["label"] == M.LABELS[1]


def test_cluster_ci_brackets_the_mean():
    rng = np.random.default_rng(2)
    den = rng.integers(0, 3, (90, 3)).astype(float)
    num = np.minimum(den, rng.integers(0, 3, (90, 3)))
    clusters = np.array([f"e{i % 9}" for i in range(90)])
    ci = M.cluster_ci(num, den, clusters, n_boot=2000)
    acc = num.sum(0) / den.sum(0)
    assert ci.shape == (3, 2)
    assert (ci[:, 0] <= acc).all()
    assert (acc <= ci[:, 1]).all()


def test_probe_matrix_groupings():
    """A label unique to each entity is unreadable on held-out entities (b) but readable on held-out scenes (a); a
    planted shared label is read by the full residual."""
    rng = np.random.default_rng(3)
    n_items, d = 60, 40
    ents = [f"e{i % 12}" for i in range(n_items)]
    items = []
    for i in range(n_items):
        lab = {
            v: {"bridge": ents[i], "slot": i % 3, "n_slots": 3, "lookup": str(i % 4), "recall": "0"} for v in VARIANTS
        }
        items.append({"scene": f"s{i}", "labels": lab})
    rows = M.row_table(items)
    ent_vec = {e: rng.normal(size=d) * 3 for e in sorted(set(ents))}
    slot_vec = rng.normal(size=(3, d)) * 6
    h = np.stack([ent_vec[e] + slot_vec[int(s)] + rng.normal(size=d) * 0.3
                  for e, s in zip(rows["entity"], rows["y_b"], strict=True)])  # fmt: skip
    rows["y_b"] = rows["y_a"].copy()  # (b) := the entity's name: unseen classes on held-out entities
    rows["y_c"] = np.array([str(int(s)) for s in M.row_table(items)["y_b"]])  # (c) := the slot, planted
    mats = {"h": h, **{f"jpp{k}": h for k in M.KS}}
    frames = {s: M.random_frame(d, 0, s, M.K_MAX) for s in range(M.N_SEEDS)}
    out = M.probe_matrix(mats, frames, rows, [("B", "a"), ("B", "b"), ("B", "c")])
    acc = {k: v[0].sum() / v[1].sum() for k, v in out.items()}
    assert acc["B|a|full"] > 0.9  # held-out scenes: every entity seen in training
    assert acc["B|b|full"] == 0.0  # held-out entities: never seen
    assert acc["B|c|full"] > 0.9
    assert (out["B|b|full"][1] == M.N_SEEDS).all()  # 5-fold per seed: every row held out once per seed
    assert (out["B|b|full"][0] <= out["B|b|full"][1]).all()


def test_lens_parts_cpu(monkeypatch):
    g = torch.Generator().manual_seed(1)
    dic = torch.nn.functional.normalize(torch.randn(30, 6, generator=g), dim=-1)
    monkeypatch.setattr(M.X, "dictionary", lambda name, la, model, lens, letters: dic)
    monkeypatch.setattr(M, "KS", (2, 4))
    monkeypatch.setattr(M, "K_MAX", 4)

    class Lens:
        def __init__(self):
            self._J_gpu: dict = {}

    h = np.random.default_rng(0).normal(size=(2, 3, 2, 3, 6)).astype(np.float16)
    parts, atoms = M.lens_parts(FakeModel(d=6), Lens(), h, (0, 2))
    assert parts[4].shape == h.shape and atoms.shape == (2, 3, 2, 3, 4)
    assert atoms.min() >= 100 and atoms.max() < 130  # token ids, not dictionary rows
    x = torch.from_numpy(h[1, 2, 1, 0].astype(np.float32))[None]
    want, _ = M.omp_parts(dic, x, (2, 4))
    assert np.allclose(parts[2][1, 2, 1, 0], want[2][0].numpy(), atol=2e-3)
