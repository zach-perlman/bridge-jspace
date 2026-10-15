from typing import Any

import pytest
import torch

from bridge_jspace.oracle import LoraHooks, lora_delta, module_pairs
from scripts.exp15_oracle_lens.experiment import compare, first_bullet_ranks, lens_class, named, score_text


def test_named_whole_word_case_and_plural():
    text = "- Brazilian culture\n- the Amazon rainforest\n- Turtles"
    assert not named("Brazil", text)  # part of another word
    assert named("amazon", text)
    assert named("turtle", text)  # plural, other case
    assert named("Brazil", "- Brazil\n- Rio")
    assert not named("Rio", "- Riot")
    assert named("New York", "- new york city")
    assert not named("4", "- 14 legs") and named("4", "- 4 legs")  # digits count as part of a word


def test_score_text_other_bridges_exclude_own_pair():
    items = [
        {"intermediate": "Brazil", "swap_to": "Mexico", "answer": "Portuguese", "swap_answer": "Spanish"},
        {"intermediate": "Mexico", "swap_to": "Brazil", "answer": "Spanish", "swap_answer": "Portuguese"},
        {"intermediate": "France", "swap_to": "Spain", "answer": "French", "swap_answer": "Spanish"},
        {"intermediate": "Japan", "swap_to": "China", "answer": "Japanese", "swap_answer": "Chinese"},
    ]
    s = score_text("- Brazil\n- Mexico\n- France", items[0], items)
    assert s["named_bridge"] and s["named_distractor"] and not s["named_answer"]
    assert s["named_other_bridges"] == 0.5  # France and Japan are the others; Mexico is the distractor


def test_first_bullet_ranks():
    pool = [10, 20, 30]
    r = first_bullet_ranks(torch.tensor([0.1, 2.0, 1.0]), pool, bridge=20, distractor=10)
    assert r == {"first_rank_bridge": 1, "first_rank_distractor": 3}
    assert first_bullet_ranks(None, pool, 20, 10)["first_rank_bridge"] is None


def test_lens_class():
    assert lens_class(1, 1) == "both"
    assert lens_class(1, 4) == "one"
    assert lens_class(2, 9) == "neither"
    assert lens_class(None, 1) is None


def test_compare_clusters_by_question():
    # q1 has three reads, q2 one: question means, not read means, are compared.
    reads = [{"name": "q1", "a": 1, "b": 0}] * 3 + [{"name": "q2", "a": 0, "b": 0}]
    out = compare(reads, "a", "b", n_boot=200, seed=0)
    assert out is not None
    assert out["n_questions"] == 2 and out["n_reads"] == 4
    assert out["a"] == pytest.approx(0.5) and out["diff"][0] == pytest.approx(0.5)
    assert compare([], "a", "b", 10, 0) is None


def test_module_pairs_rejects_unpaired_keys():
    a, b = torch.zeros(2, 4), torch.zeros(3, 2)
    good = {"base_model.model.lin.lora_A.weight": a, "base_model.model.lin.lora_B.weight": b}
    assert set(module_pairs(good)) == {"lin"}
    with pytest.raises(ValueError):
        module_pairs({"base_model.model.lin.lora_A.weight": a})


def test_lora_hooks_match_merged_weights_and_switch_off():
    torch.manual_seed(0)
    net = torch.nn.Sequential(torch.nn.Linear(4, 3), torch.nn.ReLU(), torch.nn.Linear(3, 2))
    a, b = torch.randn(2, 4), torch.randn(3, 2)
    first: Any = net[0]
    hooks = LoraHooks(net, {"0": (a, b)}, scale=2.0)
    x = torch.randn(5, 4)
    base = net(x)
    with hooks.on():
        hooked = net(x)
    merged = torch.nn.Linear(4, 3)
    merged.weight.data = first.weight.data + 2.0 * b @ a
    merged.bias.data = first.bias.data
    assert torch.allclose(hooked, net[2](net[1](merged(x))), atol=1e-5)
    assert torch.allclose(net(x), base)  # off again after the block
    assert torch.allclose(lora_delta(x, a, b, 2.0), 2.0 * x @ a.T @ b.T, atol=1e-5)
    with pytest.raises(ValueError):
        LoraHooks(net, {"1": (a, b)}, 2.0)  # a ReLU, not a Linear


def test_lens_lookup_reads_the_cell_and_handles_missing_answers():
    import numpy as np

    from scripts.exp15_oracle_lens.experiment import lens_lookup

    pool = np.full((63, 4), 9, dtype=np.uint8)
    pool[36, 2] = 1  # layer 36, offset -1
    grids = {"jlens": {"q": {"bridge_pool": pool}}, "jpp": {"q": {"bridge_pool": pool}}}
    meta = {"q": {"offsets": [-3, -2, -1, 0]}}
    rows = [{"name": "q", "seq_len": 4, "read_at": {"last": 3, "prev": 2}}]
    out = lens_lookup(grids, meta, rows, [36, 44])
    assert out[("q", "prev", 36)]["lens_class"] == "both"
    assert out[("q", "last", 36)]["lens_class"] == "neither"
    answer = lens_lookup(grids, meta, rows, [36], role="answer", prefix="answer_")
    assert answer[("q", "prev", 36)] == {"answer_jlens_rank": None, "answer_jpp_rank": None, "answer_lens_class": None}


def test_oracle_words_html_marks_once_and_escapes():
    from bridge_jspace.examples import oracle_words_html

    words = {"bridge": "Brazil", "answer": "Portuguese", "distractor": "Mexico", "swap_answer": "Spanish"}
    html = oracle_words_html("- brazil <b>\n- Mexicos, Brazilian", words)
    assert "<span class='w bridge'>brazil</span>" in html and "<span class='w ctrl'>Mexicos</span>" in html
    assert "&lt;b&gt;" in html and "<br>" in html and "Brazilian" in html and html.count("<span") == 2
    # a word that is also part of the markup is not re-marked inside it
    assert oracle_words_html("w class span", {"bridge": "class"}).count("<span") == 1
    assert "span class='w answer'" not in oracle_words_html("- 4 legs", {"answer": "4"}, mark_answers=False)
