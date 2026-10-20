"""Example selection on the committed runs (fake tokenizer, no model) and markdown rendering."""

from pathlib import Path

import pytest

from bridge_jspace.examples import (
    Group,
    _with_cue,
    cue_token_indices,
    export,
    export_index,
    latest_examples_run,
    prompt_html,
    render,
    render_html,
    sample,
)
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

    html = render_html([Group("seen_last", "Seen", "def", 41)], [rec], P, "m")
    assert html.startswith("<!doctype html>") and 'class="w bridge">Brazil<' in html
    assert 'id="seen_last-amazon-language"' in html and "<script>" in html


def test_cue_phrase_is_marked_in_prompt_and_position_table():
    tokens = ["Fact", ":", " where", " the", " Amazon", " River", " ends", " is"]
    rec = {
        "name": "amazon-language",
        "group": "g",
        "prompt": "".join(tokens),
        "words": {"bridge": "Brazil", "answer": "Portuguese"},
        "word_ids": {"bridge": [1], "answer": [2]},
        "why": "w",
        "info": {},
        "tokens": tokens,
        "last_token": {},
        "positions": {"jlens": {"32": [{"top": [" x"], "top_ids": [9], "ranks": {"bridge": 4}}] * 5}},
    }
    assert cue_token_indices(tokens, "Amazon River ends") == {4, 5, 6}
    assert cue_token_indices(tokens, "zon Riv") == {4, 5}  # a span that cuts tokens marks every token it touches
    assert cue_token_indices(tokens, "Nile") == set() == cue_token_indices(tokens, None)
    assert prompt_html("a <b> c ", "<b>") == "a <span class='cue'>&lt;b&gt;</span> c␣"
    assert prompt_html("a b", "zz") == "a b"

    cued = _with_cue(rec, {"amazon-language": "Amazon River ends"})
    assert _with_cue(rec, {"amazon-language": "not in this prompt"}) is rec  # another set reusing the name
    html = render_html([Group("g", "G", "d", 1)], [cued], P, "m")
    assert "<span class='cue'>Amazon River ends</span>" in html and "Dotted underline" in html
    assert html.count("class='cuetok'") == 3  # the last 5 tokens are shown; three are in the cue
    md = render([Group("g", "G", "d", 1)], [cued], P, "m")
    assert 'Cue phrase: "Amazon River ends"' in md and md.count("(cue)") == 3
    assert "Dotted underline" not in render_html([Group("g", "G", "d", 1)], [rec], P, "m")


def _fake_run(root, exp, stamp, target="bridge_jspace.examples:LensExamples"):
    import json

    run = root / exp / stamp
    (run / "slices").mkdir(parents=True)
    (run / "slices" / "x__jlens.html").write_text("<!doctype html><title>x</title>")
    params = {
        "title": "t",
        "page_title": "Fake Examples",
        "source_run": "r",
        "seed_examples": 0,
        "per_group": 1,
        "top_k": 1,
    }
    (run / "manifest.json").write_text(
        json.dumps({"config": {"name": exp, "target": target, "params": params, "model": {"name": "org/m"}}})
    )
    (run / "examples.json").write_text(
        json.dumps({"groups": [{"key": "g", "title": "G", "definition": "d", "n_total": 2}], "examples": []})
    )
    return run


def test_export_builds_the_view_and_index(tmp_path):
    results, root = tmp_path / "results", tmp_path / "examples"
    _fake_run(results, "exp99_x", "20260101-000000")
    newest = _fake_run(results, "exp99_x", "20260102-000000")
    _fake_run(results, "exp99_x", "20260103-000000", target="scripts.other:Main")  # not an examples run
    assert latest_examples_run("exp99_x", results) == newest
    out = export(newest, root)
    assert {p.name for p in out.iterdir()} == {"index.html", "examples.md", "artifact.html", "slices", "source.json"}
    assert (out / "slices" / "x__jlens.html").exists()
    assert not (out / "artifact.html").read_text().startswith("<!doctype")  # publishable variant
    index = export_index(root).read_text()
    assert "exp99_x/index.html" in index and "Fake Examples" in index
