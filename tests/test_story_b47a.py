"""Batch 47's README figures (scripts/story_b47a.py) on planted verdict folders: each made by its test's own verdict
stage from the planted runs of tests/test_x47_*.py (no real result is read). Each figure builds, records every plotted
number with its verdict file as the source, saves to tmp_path, and has no overlapping text, banned variant or retired
term. The planted_* builders also make the preview PNGs (scratch, by hand)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import test_x47_atoms as TA
import test_x47_cue as TC
import test_x47_errors as TE
import test_x47_six as TS
import test_x47_zero as TZ
from test_readme_phase2_figures import check, saved  # noqa: F401 (saved: a fixture)

from scripts import story_b47a as B
from scripts import story_style as S
from scripts import x0_necessity as X
from scripts import x47_atoms as A
from scripts import x47_cue as C
from scripts import x47_errors as E
from scripts import x47_six as Q
from scripts import x47_zero as Z

N_BOOT = 100


def planted_atoms(tmp_path: Path, mp) -> Path:
    """27B and Muse: identity falls 0.40 / 0.35 beyond random, the recall loses 0.05: (a); the 9B: no fall, (c)."""
    TA._planted(tmp_path, mp, {"qwen3.6-27b": 0.4, "qwen3.5-9b": 0.0, "muse-glimmer-30b": 0.35})
    mp.setattr(A, "dan_answer", lambda q=A.QUESTION: "planted")
    return A.stage_verdict(N_BOOT, decode_for=lambda t: lambda ids: "".join(f"<{int(i)}>" for i in ids))


def planted_zero(tmp_path: Path, mp) -> Path:
    """9B and Muse: the recall loses 0.35 / 0.40 beyond random (needed); the 27B keeps 0.90 against 0.95 (followed)."""
    kept = {"qwen3.5-9b": {"zero_L": 60, "rand_L": 95}, "qwen3.6-27b": {"zero_L": 90, "rand_L": 95},
            "muse-glimmer-30b": {"zero_L": 50, "rand_L": 90}}  # fmt: skip
    TZ._planted(tmp_path, mp, kept)
    mp.setattr(A, "dan_answer", lambda q=A.QUESTION: "planted")
    return Z.stage_verdict(n_boot=N_BOOT, decode_for=lambda t: lambda ids: "".join(f"<{int(i)}>" for i in ids))


def planted_cue(tmp_path: Path, mp) -> Path:
    """The 27B: the split holds, never the value, a pointer at the word; the 9B: handed through the lens, some value;
    Muse: its gate fails (not tested)."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    runs = []
    for target, kw in (("qwen3.6-27b", {}), ("qwen3.5-9b", {"lookup_loss": 0.25, "value": 0.1, "pcf_cut": False}),
                       ("muse-glimmer-30b", {"gate_pass": False})):  # fmt: skip
        TC.planted(tmp_path, mp, **kw)
        run = C.RUNS[target]
        (tmp_path / "run").rename(tmp_path / run)
        man = tmp_path / run / "manifest.json"
        man.write_text(json.dumps({**json.loads(man.read_text()), "model": {"target": target}}))
        runs.append(run)
    mp.setattr(C, "dan_answer", lambda rev="HEAD": "planted")
    mp.setattr(C, "view", lambda *a, **k: [])  # the verify-pack view needs cases; the figure reads the json only
    return C.stage_verdict(runs, n_boot=N_BOOT)


def _six_run(root: Path, target: str, answer, mu: np.ndarray) -> str:
    """A finished 47.2 run: six slots, the test half's lookup rows planted by `answer`, the slot means mu."""
    run = Q.RUNS[target]
    src = root / run
    src.mkdir(parents=True)
    rows = TS.planted_rows(6, answer)
    man = {"model": {"target": target}, "layer": X.PREDICTED[target], "slots": 6, "tested": True,
           "fallback": {"note": "six slots passed the gate"}, "unit": {"value": 1.0, "fit_half_median": 1.0},
           "fit": {"states": 300, "W_rank": 5}, "items": {"fit": 60, "test": 60, "c0": 0}}  # fmt: skip
    (src / "manifest.json").write_text(json.dumps(man))
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "norms.jsonl", [{"scene": f"s{i}", "share_slot": 0.1, "share_U": 0.05} for i in range(10)])
    np.savez(src / "fit.npz", mu=mu)
    return run


def planted_six(tmp_path: Path, mp) -> Path:
    """The 9B: a line (every shift works, the means in slot order); Muse: first vs rest."""
    mp.setattr(Q, "RESULTS", tmp_path)
    g = np.random.default_rng(1)
    a, b = g.normal(size=30), g.normal(size=30)

    def first(arm, i, j):
        if arm["arm"] == "v":
            return arm["target"] if i == 1 else i
        if arm["arm"] == "write":
            return arm["target"] if 1 in (i, arm["target"]) else i
        return j if arm["arm"] in ("whole", "no_U", "no_U_rand", "no_slot_rand") else i

    runs = [_six_run(tmp_path, "qwen3.5-9b", TS.ordinal_answer, np.stack([b + k * a for k in range(1, 7)])),
            _six_run(tmp_path, "muse-glimmer-30b", first, np.stack([a] + [1e-3 * g.normal(size=30) for _ in range(5)]))]  # fmt: skip
    mp.setattr(Q, "dan_answer", lambda rev="HEAD": "planted")
    mp.setattr(Q, "examples_lines", lambda runs, **k: [])  # the verify pack needs cases; the figure reads the json only
    return Q.stage_verdict(runs, n_boot=N_BOOT)


def planted_errors(tmp_path: Path, mp) -> Path:
    """The 9B: the probe matches 24 of 40 wrong answers, the lens right on 22 of them (holds); the 27B: 5 wrong answers
    (not tested); Muse: 18 of 36 matched, the lens right on 8 (does not hold)."""
    mp.setattr(E, "RESULTS", tmp_path)
    mp.setattr(E, "dan_answer", lambda rev="HEAD": "planted")
    TE.write_planted(tmp_path, "r9", "qwen3.5-9b", 40, 24, 22)
    TE.write_planted(tmp_path, "r27", "qwen3.6-27b", 5, 5, None)
    TE.write_planted(tmp_path, "rmuse", "muse-glimmer-30b", 36, 18, 8)
    return E.stage_verdict(["r9", "r27", "rmuse"], n_boot=N_BOOT)


PLANTED = {"47.1": planted_atoms, "47.5": planted_zero, "47.3": planted_cue, "47.2": planted_six,
           "47.13": planted_errors}  # fmt: skip
VERDICT_FILE = {"47.1": "x47_1.json", "47.5": "x47_5.json", "47.3": "x47_3.json", "47.2": "x47_2.json",
                "47.13": "x47_errors.json"}  # fmt: skip


@pytest.mark.parametrize("test_id", list(B.TESTS))
def test_figure_on_its_planted_verdict(test_id, tmp_path, monkeypatch, saved):  # noqa: F811
    verdict = PLANTED[test_id](tmp_path / "results", monkeypatch)
    _, build, name = B.TESTS[test_id]
    assert build(verdict, name) == name
    assert (S.OUT / f"{name}.png").exists() and (S.OUT / f"{name}.svg").exists()
    check(saved[name])
    rows = [r for r in S.ROWS if r["figure"] == B.fig_id(name)]
    assert rows and all(r["source"].endswith(VERDICT_FILE[test_id]) for r in rows)
    assert any(isinstance(r["value"], float) and r["lo"] is not None for r in rows)  # a number with its interval


def test_titles_read_the_planted_outcomes(tmp_path, monkeypatch):
    v = {k: json.loads((PLANTED[k](tmp_path / k, monkeypatch) / VERDICT_FILE[k]).read_text()) for k in PLANTED}
    assert B.atoms_title(v["47.1"]).startswith("The lookup's identity route sits in lens directions 26–100")
    assert B.zero_title(v["47.5"]).endswith("the recall needs it on 2 of 3 models")
    assert B.cue_title(v["47.3"]) == "A described bridge gives no clean split; the lookup sometimes takes the value"
    assert B.six_title(v["47.2"]) == "Six lockers: the order code differs by model"
    assert B.errors_title(v["47.13"]) == "The address probe predicts the lookup's errors on 1 of 2 models"


def test_a_given_title_wins(tmp_path, monkeypatch, saved):  # noqa: F811
    verdict = planted_errors(tmp_path / "results", monkeypatch)
    B.build_errors(verdict, "fig15_probe_errors", title="A claim Dan wrote")
    assert saved["fig15_probe_errors"]["title"] == "A claim Dan wrote"
