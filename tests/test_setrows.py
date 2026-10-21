import torch

from scripts.exp04_brew_parts import AddRows, SetRows


def test_setrows_pastes_and_does_not_stack():
    h = torch.zeros(5, 3)
    target = torch.ones(2, 3)
    once = SetRows(target, [1, 3])(h)
    assert torch.equal(once[[1, 3]], target) and torch.equal(once[[0, 2, 4]], h[[0, 2, 4]])
    assert torch.equal(SetRows(target, [1, 3])(once), once)  # a second paste changes nothing
    assert torch.equal(AddRows(target, [1, 3])(once)[[1, 3]], 2 * target)  # a second add stacks
