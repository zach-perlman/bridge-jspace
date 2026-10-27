"""d1_precheck's topic condition (pure) and d1_verdict's decisive cell on a lens with maps at some layers only."""

from scripts import d1_precheck as PC
from scripts import d1_verdict as V


def test_topics_ok():
    assert PC.topics_ok({"animals": 40, "elements": 30, "greek": 10}, 2, 30)
    assert not PC.topics_ok({"animals": 40, "elements": 29, "greek": 10}, 2, 30)


def test_decisive_cell_uses_the_lens_layers(monkeypatch):
    rates = [{"family": "PP", "set": s, "transit": True, "layer": la, "cf": {"flips": [f, 0, 1]}}
             for s, la, f in (("context", 16, 0.9), ("context", 18, 0.6), ("bind_bridge", 21, 0.7))]  # fmt: skip
    monkeypatch.setattr(V.pins, "LENS_LAYERS", None)
    cell = V.decisive_cell(rates, "PP", 16, 22)
    assert cell is not None and cell["layer"] == 16  # every 4th layer: 16 only
    monkeypatch.setattr(V.pins, "LENS_LAYERS", list(range(0, 31, 3)))
    assert V.decisive_cell(rates, "PP", 16, 22) == {"set": "bind_bridge", "layer": 21, "map_flips": [0.7, 0, 1]}
