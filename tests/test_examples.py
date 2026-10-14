"""Example selection on the committed runs (fake tokenizer, no model) and markdown rendering."""

from pathlib import Path

import pytest

from bridge_jspace.examples import Group, render, sample
from bridge_jspace.pins import RESULTS_DIR

P = {"per_group": 3, "seed_examples": 0, "band": [32, 48], "top_k": 2, "title": "t", "source_run": "r"}


class _Ids:
    def __init__(self, ids):
        self.input_ids = ids


class _Tok:
    """Every surface is one token (id from a stable hash): enough for selection, which only needs some ids."""

    def _id(self, text: str) -> int:
        return sum(map(ord, text)) % 10_000

    def __call__(self, text, add_special_tokens=False):
        return _Ids([self._id(text)])

    def encode(self, text, add_special_tokens=False):
        return [self._id(text)]

    def decode(self, ids):
        return str(ids[0])


def _run(exp: str, stamp: str) -> Path:
    run = RESULTS_DIR / exp / stamp
    if not run.exists():
        pytest.skip(f"{run} not in this checkout")
    return run


def test_exp11_and_exp12_agree_on_last_token_misses():
    from scripts.exp11_bridge_vs_answer_by_layer.examples import select as s11
    from scripts.exp12_position_map.examples import select as s12

    g11, ex11 = s11(_run("exp11_bridge_vs_answer_by_layer", "20261014-092835"), P, _Tok())
    g12, ex12 = s12(_run("exp12_position_map", "20261014-095358"), P, _Tok())
    n11 = {g.key: g.n_total for g in g11}
    n12 = {g.key: g.n_total for g in g12}
    # same prompts, same lens, same last token: both runs must count the same misses (exp12 summary: 26 of 67)
    assert n11["missed_last"] == n12["seen_earlier"] + n12["unseen"] == 26
    assert n11["seen_last"] == n12["seen_last"] == 67 - 26
    assert n11["model_wrong"] == n12["model_wrong"] == 16
    for groups, examples in ((g11, ex11), (g12, ex12)):
        shown = {g.key: sum(e.group == g.key for e in examples) for g in groups}
        assert all(shown[g.key] == min(3, g.n_total) for g in groups)
    assert [e.name for e in ex12] == [e.name for e in s12(_run("exp12_position_map", "20261014-095358"), P, _Tok())[1]]


def test_exp10_groups():
    from scripts.exp10_lens_sanity.examples import select as s10

    groups, examples = s10(_run("exp10_lens_sanity", "20261013-205936"), P, _Tok())
    n = {g.key: g.n_total for g in groups}
    assert n["all_see"] + n["none_see"] <= 84  # single-token items only
    assert all(e.words["bridge"] and e.words["answer"] for e in examples)


def test_sample_is_deterministic_and_bounded():
    names = [f"n{i}" for i in range(10)]
    assert sample(names, 3, 0) == sample(names, 3, 0)
    assert len(sample(names, 30, 0)) == 10 and sample([], 3, 0) == []


def test_render_marks_words():
    rec = {
        "name": "amazon-language",
        "group": "seen_last",
        "prompt": "Fact: ... ends is ",
        "words": {"bridge": "Brazil", "answer": "Portuguese", "distractor": "Mexico", "swap_answer": "Spanish"},
        "word_ids": {"bridge": [1], "answer": [2], "distractor": [3], "swap_answer": [4]},
        "why": "because",
        "info": {"label (B)": "J-mediated"},
        "tokens": ["Fact", " is", " "],
        "last_token": {
            "jlens": {"32": {"top": [" Brazil", " Mexico"], "top_ids": [1, 3], "ranks": {"bridge": 1, "answer": 9}}}
        },
        "positions": {"jlens": {"32": [{"top": [" Portuguese"], "top_ids": [2], "ranks": {"bridge": 4}}] * 2}},
    }
    md = render([Group("seen_last", "Seen", "def", 41)], [rec], P, "m")
    assert "| [Seen](#seen_last) | def | 41 | 1 |" in md
    assert "**Brazil**, [Mexico]" in md and "1 / 9" in md
    assert "*Portuguese* (4)" in md
    assert "> Fact: ... ends is␣" in md
