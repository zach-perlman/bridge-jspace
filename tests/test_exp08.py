"""exp08_brew_read: colour ranks and the code as a reader (no model)."""

import torch

from scripts.exp07_step_code import COLOURS
from scripts.exp08_brew_read import code_scores, colour_ranks


def test_colour_ranks_count_the_colours_above():
    scores = torch.zeros(2, len(COLOURS))
    roles = {"I": "teal", "X": "red", "S": "blue", "A": "gold"}
    scores[0, COLOURS.index("teal")] = 3.0
    scores[0, COLOURS.index("red")] = 2.0
    scores[1, COLOURS.index("red")] = 5.0
    ranks = colour_ranks(scores, roles)
    assert ranks["I"] == [0, 1]
    assert ranks["X"] == [1, 0]
    assert ranks["S"] == [2, 1]  # ties with the other zeros count as not above


def test_code_scores_pick_the_planted_intermediate():
    g = torch.Generator().manual_seed(0)
    k, p, d = len(COLOURS), 3, 32
    w = torch.randn(1 + 3 * k, p, d, generator=g)
    h = w[0] + w[1 + k + COLOURS.index("pink")]
    assert int(code_scores(w, h).argmax(dim=1)[0]) == COLOURS.index("pink")
    assert (code_scores(w, h).argmax(dim=1) == COLOURS.index("pink")).all()
