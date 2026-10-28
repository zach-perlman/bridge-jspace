"""scripts/story_b49c.py: 49.3's figure drawn from a verdict folder x49_probe.py wrote on its fake run (the fixtures of
tests/test_x49_probe.py; the verdict json marked planted), with the builder's own title and with a passed one; every
plotted number recorded against the verdict file; the figure's words pass the README's banned-term matcher and nothing
overlaps. Nothing is written under figures/ (story_style.OUT goes to a temporary folder). No real run is read."""

from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest
from test_readme_phase2_figures import check, saved  # noqa: F401 (saved: a fixture)

from scripts import story_b49c as C
from scripts import story_style as S
from tests import test_x49_probe as TP


def pooled_verdict(tmp_path: Path, mp: pytest.MonkeyPatch) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    mp.setattr(TP.P.W.X, "render", lambda tok, item, rendering, context: TP.TB.wrap(context, item["question"]))
    run = inspect.unwrap(TP.fake_run)(tmp_path, mp, None).out
    mp.setattr(TP.P, "dan_answer", lambda: "planted")
    out = TP.P.stage_verdict([run.name], n_boot=50)
    path = out / "x49_3.json"
    path.write_text(json.dumps({**json.loads(path.read_text()), "planted": True}, indent=1))
    return out


def test_pooled_figure_from_its_verdict(tmp_path, monkeypatch, saved):  # noqa: F811
    out = pooled_verdict(tmp_path / "runs", monkeypatch)
    assert C.build_pooled(out, "fig27_pooled") == "fig27_pooled"
    assert (S.OUT / "fig27_pooled.png").exists() and (S.OUT / "fig27_pooled.svg").exists()
    fig = saved["fig27_pooled"]
    check(fig)
    assert any(t.startswith("PLANTED") for t in fig["texts"])
    rows = [r for r in S.ROWS if r["figure"] == "fig27"]
    sources = {r["source"] for r in rows}  # the verdict's json, one file
    assert rows and len(sources) == 1 and sources.pop().endswith(f"{out.name}/x49_3.json")
    # the 9B's two layers drawn (Muse pending): readings, and the three marks per probe and layer
    assert sum(r["quantity"].startswith("49.3: the rule's reading") for r in rows) == 3
    assert sum("sentence mean, locker after the pick" in r["quantity"] for r in rows) == 4
    assert any("best single token" in r["quantity"] for r in rows)
    assert "Muse Glimmer 30B" in fig["texts"] and any("pending" in t for t in fig["texts"])
    # a passed title replaces the builder's claim; the rest is the same figure
    n = len(S.ROWS)
    assert C.build_pooled(out, "fig27_pooled", title="A claim passed in") == "fig27_pooled"
    assert saved["fig27_pooled"]["title"] == "A claim passed in" and len(S.ROWS) == 2 * n


def test_pooled_title_follows_the_labels():
    def m(label: str, status: str = "tested") -> dict:
        return {"label": label, "status": status}

    assert C.pooled_title([m("distributed"), m("distributed")]).startswith("Who picked the item is spread")
    assert "picked-flag" in C.pooled_title([m("flag"), m("flag")])
    assert C.pooled_title([m("neither"), m("neither")]).startswith("No person mark")
    assert C.pooled_title([m("neither"), m("flag")]).endswith("the models differ")
    assert C.pooled_title([m("pending", "pending")]).endswith("no model tested yet")
    for labels in (["distributed"], ["flag"], ["neither"], ["between"], []):
        assert len(C.pooled_title([m(x) for x in labels])) <= 86
