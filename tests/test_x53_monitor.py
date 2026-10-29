"""x53_monitor (53.2): labels, the J++ part's OMP, the forward's position mapping, the lens parts (CPU fakes)."""

import sys
from pathlib import Path

import numpy as np
import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import x53_monitor as M

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
