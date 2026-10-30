"""scripts/story_b48.py: each batch-48 figure drawn from a verdict folder its own script wrote on that script's fake
run (the fixtures of tests/test_x48_*.py; the verdict json marked planted), with the builder's own title and with a
passed one; every plotted number recorded against the verdict file; the figure's words pass docs/glossary.md's matcher.
Nothing is written under figures/ (story_style.OUT goes to a temporary folder). No real run is read."""

from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest
from matplotlib.text import Text

from scripts import story_b48 as F
from scripts import story_style as S
from tests import test_x48_bind as TB
from tests import test_x48_das as TD
from tests import test_x48_enrich as TE
from tests import test_x48_heads as TH
from tests import test_x48_route2 as TR
from tests.test_readme_build import banned


def planted(out: Path, name: str) -> Path:
    """Marks a fake verdict's json as planted (the figures' subtitles then say so); returns the verdict folder."""
    path = out / name
    blob = json.loads(path.read_text())
    path.write_text(json.dumps({**blob, "planted": True}, indent=1))
    return out


# ---- the fake verdicts (each script's own verdict stage on its tests' fake runs) ------------------------------------


def das_verdict(tmp_path: Path, mp: pytest.MonkeyPatch) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    env = inspect.unwrap(TD.fake_env)(tmp_path, mp)
    run = TD.D.stage_run(f"{env.prefix}fake_48f", "test", steps=1, ks=(1, 2))
    mp.setattr(TD.D, "KS", (1, 2))
    mp.setattr(TD.D, "dan_answer", lambda *_: "planted")
    return planted(TD.D.stage_verdict([run.name], n_boot=50), "verdict.json")


def enrich_verdict(tmp_path: Path, mp: pytest.MonkeyPatch) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    mp.setattr(F.pins, "TARGET", "qwen3.5-9b")  # 48.2 runs on the 9B and Muse (the default target is the 27B)
    mp.setattr(F.pins, "RUN_PREFIX", "qwen35_9b_")
    env = inspect.unwrap(TE.fake_env)(tmp_path, mp)
    a = TE.E.stage_run_a(f"{env.pins.RUN_PREFIX}fake_a", "test")
    b = TE.E.stage_run_b(f"{env.pins.RUN_PREFIX}fake_b", "test")
    mp.setattr(TE.E, "dan_answer", lambda: "planted")
    return planted(TE.E.stage_verdict([a.name], [b.name], n_boot=50), "x48_2.json")


def bind_verdict(tmp_path: Path, mp: pytest.MonkeyPatch) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    inspect.unwrap(TB.render_fake)(mp)
    run = inspect.unwrap(TB.fake_run)(tmp_path, mp, None).out
    mp.setattr(TB.W, "dan_answer", lambda: "planted")
    return planted(TB.W.stage_verdict([run.name], n_boot=50), "x48_bind.json")


def heads_verdict(tmp_path: Path, mp: pytest.MonkeyPatch) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    mp.setattr(TH.H, "dan_answer", lambda rev="HEAD": "planted")
    reads = {"jpp": 0.1, "rest": 0.3, "address": 0.35, "random": 0.2}
    flat = {"jpp": 0.3, "rest": 0.3, "address": 0.1, "random": 0.2}
    TH.planted_run(tmp_path, mp, "qwen35_9b_x48_heads", "qwen3.5-9b", [reads] * 3 + [flat] * 2)
    TH.planted_run(tmp_path, mp, "muse30_x48_heads", "muse-glimmer-30b", [reads] * 2 + [flat] * 3)
    return planted(TH.H.stage_verdict(["qwen35_9b_x48_heads", "muse30_x48_heads"], n_boot=50), "x48_heads.json")


def route2_verdict(tmp_path: Path, mp: pytest.MonkeyPatch) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    run = inspect.unwrap(TR.fake_run)(tmp_path, mp).out
    mp.setattr(TR.Q, "dan_answer", lambda: "planted")
    return planted(TR.Q.stage_verdict([run.name], n_boot=50), "x48_route2.json")


VERDICTS = {"48.1": das_verdict, "48.2": enrich_verdict, "48.3": bind_verdict, "48.4": heads_verdict,
            "48.5": route2_verdict}  # fmt: skip


# ---- the figures ------------------------------------------------------------------------------------------------------


@pytest.fixture
def drawn(tmp_path, monkeypatch):
    """story_style into a temporary folder; each saved figure's texts kept by name."""
    texts: dict[str, list[str]] = {}
    save = S.save

    def grab(fig, name: str, supp: bool = False) -> None:
        texts[name] = [t.get_text() for t in fig.findobj(Text) if t.get_text().strip()]
        save(fig, name, supp)

    monkeypatch.setattr(S, "OUT", tmp_path / "story")
    monkeypatch.setattr(S, "ROWS", [])
    monkeypatch.setattr(S, "save", grab)
    return texts


def test_every_test_has_a_builder_and_a_figure_name():
    assert set(F.TESTS) == set(VERDICTS)
    assert [F.TESTS[t][2] for t in sorted(F.TESTS)] == [f"fig{n}_{w}" for n, w in
                                                         zip(range(21, 26), ("das", "enrichment", "binding", "heads",
                                                                             "second_route"), strict=True)]  # fmt: skip
    for script, fn, _ in F.TESTS.values():
        assert (Path(F.pins.REPO_ROOT) / script).exists() and callable(fn)


@pytest.mark.parametrize("test", sorted(VERDICTS))
def test_figure_from_its_verdict(test, tmp_path, monkeypatch, drawn):
    out = VERDICTS[test](tmp_path / "runs", monkeypatch)
    _, build, name = F.TESTS[test]
    assert build(out, name) == name
    assert (S.OUT / f"{name}.png").exists()  # PNG only (Dan, 30 Oct)
    texts = drawn[name]
    assert any(t.startswith("PLANTED") for t in texts)  # the subtitle says the data are planted
    rows = [r for r in S.ROWS if r["figure"] == name.split("_")[0]]
    sources = {r["source"] for r in rows}  # the verdict's json, one file
    assert rows and len(sources) == 1 and sources.pop().endswith(f"{out.name}/{next(out.glob('*.json')).name}")
    assert all(r["value"] is not None for r in rows)
    assert not banned([(name, t) for t in texts]), banned([(name, t) for t in texts])
    # a passed title replaces the builder's claim; the rest is the same figure
    assert build(out, name, title="A claim passed in") == name
    assert "A claim passed in" in drawn[name] and len(S.ROWS) == 2 * len(rows)


def test_das_title_follows_the_rules():
    def model(target: str, **rules: bool) -> dict:
        r = {k: rules.get(k, False) for k in "abcd"}
        return {"target": target, "rules": {**r, "fallback_no_low_dimensional_mediator": rules.get("fb", False)}}

    nine, muse = "qwen3.5-9b", "muse-glimmer-30b"
    assert F.das_title([model(nine, a=True, b=True), model(muse, a=True, b=True)]).endswith("lies in the J++ part")
    assert F.das_title([model(nine, a=True), model(muse, a=True)]) == "Two readers, two subspaces at the bridge word"
    assert F.das_title([model(nine, a=True), model(muse)]) == "Two readers, two subspaces on the 9B only"
    assert F.das_title([model(nine), model(muse)]).startswith("The two readers do not")
    assert F.das_title([model(nine, fb=True), model(muse, fb=True)]).startswith("No small subspace")
