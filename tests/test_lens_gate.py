"""lens_gate: the pre-registered gate on synthetic ranks, the window summary, and the PP cases' position sets on
d1_topics_v2 with the target's tokenizer (skipped when it is not cached)."""

import pytest

from scripts import lens_gate as G


def _best(ranks: list[int]) -> dict[str, dict[str, int]]:
    return {"bind_bridge": {f"i{k}": r for k, r in enumerate(ranks)}}


@pytest.mark.parametrize(("bridge", "x", "ok"), [
    ([1] * 6 + [50] * 4, [50] * 10, True),  # 60% in the top 10, X 0%
    ([1] * 4 + [50] * 6, [50] * 10, False),  # 40%: the lens does not name the bridge often enough
    ([1] * 9 + [50], [1] * 5 + [50] * 5, False),  # X as often: the lens reads any mentioned word, not the bridge
])  # fmt: skip
def test_gate(bridge, x, ok):
    g = G.gate(_best(bridge), _best(x))
    assert g["pass"] is ok and g["n"] == 10


def test_summarise_takes_the_best_layer_per_item():
    rows = [{"id": "a", "set": s, "layer": la, "rank_bridge": rb, "rank_x": 99}
            for s in G.SETS for la, rb in ((24, 30), (28, 2))]  # fmt: skip
    out = G.summarise(rows, [24, 28])
    assert out["window_best"]["bind_bridge"]["top10"][0] == 1.0
    assert out["per_layer"]["bind_bridge/24"]["top10"][0] == 0.0
    assert out["gate"]["pass"]


def test_cases_have_the_bridge_sentence_and_word():
    from bridge_jspace.tokens import load_tokenizer

    try:
        tok = load_tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")
    cases = G.build(tok, "d1_topics_v2", 6)
    assert len(cases) == 6
    for c in cases:
        word = tok.decode([c["ids"]["clean"][i] for i in c["sets"]["bridge_word"]]).strip()
        sent = tok.decode([c["ids"]["clean"][i] for i in c["sets"]["bind_bridge"]]).strip()
        assert word == c["bridge"] and sent.endswith(f"{c['bridge']}.")
        assert set(c["sets"]["bind_bridge"]) <= set(c["sets"]["context"])
