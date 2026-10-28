"""Batch 47's README figures, set C (scripts/story_b47c.py). The sealed tests (47.11, 47.12, 47.15, 47.16) on planted
verdict folders, each made by its test's own verdict stage from runs planted with tests/test_x47_*.py's helpers (no
real result is read); 47.14 and D4 (opened) on their committed verdict files and on planted variants of them. Each
figure builds, records every plotted number with its verdict file as the source, saves to tmp_path, and has no
overlapping text, banned variant or retired term. The planted_* builders also make the preview PNGs (scratch, by hand).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import test_x47_agnostic as TG
import test_x47_distance as TDist
import test_x47_twodefs as TW
import torch
from test_readme_phase2_figures import check, saved  # noqa: F401 (saved: a fixture)

from bridge_jspace import pins
from scripts import story_b47c as B
from scripts import story_style as S
from scripts import x0_necessity as X
from scripts import x47_agnostic as G
from scripts import x47_atoms as A
from scripts import x47_distance as D
from scripts import x47_source as Q
from scripts import x47_twodefs as W

N_BOOT = 100
CHAIN = pins.REPO_ROOT / "results" / "x47_chain" / "x47_14-20261028T115841Z"  # opened (Dan answered Q47.14)
DEPTH = pins.REPO_ROOT / "results" / "x47_depth_cpu" / "persistence-20261028T115530Z"  # opened (Q-depth)


def _sealed_open(mp) -> None:
    mp.setattr(A, "dan_answer", lambda question="", rev="HEAD": "planted")


# ---- 47.14 and D4: the committed verdicts, and planted variants of them -----------------------------------------------


def planted_chain(tmp_path: Path, mp) -> Path:
    """47.14's committed verdict with Muse made pending (the figure's status cell); the 9B as run."""
    out = tmp_path / "x47_14-planted"
    out.mkdir(parents=True)
    v = json.loads((CHAIN / "x47_14.json").read_text())
    v["models"] = [m if m["target"] == "qwen3.5-9b" else {"run": m["run"], "target": m["target"], "status": "pending",
                                                          "holds": False, "why": "planted"} for m in v["models"]]  # fmt: skip
    (out / "x47_14.json").write_text(json.dumps(v))
    return out


def planted_depth(tmp_path: Path, mp) -> Path:
    """D4's committed persistence verdict with the 9B's address made persistent (every overlap 0.7)."""
    out = tmp_path / "persistence-planted"
    out.mkdir(parents=True)
    v = json.loads((DEPTH / "persistence.json").read_text())
    u = v["models"]["qwen3.5-9b"]["U"]
    u["matrix"] = [[1.0 if i == j else 0.7 for j in range(len(u["matrix"]))] for i in range(len(u["matrix"]))]
    u.update({"label": "persistent", "mean_cos2": 0.7, "drops": [], "adjacent": dict.fromkeys(u["adjacent"], 0.7)})
    (out / "persistence.json").write_text(json.dumps(v))
    return out


# ---- 47.11: the item-agnostic pointer ----------------------------------------------------------------------------------


def _agnostic_run(root: Path, target: str, planted: dict[str, tuple]) -> str:
    """A finished 47.11 run: per type (pos_no_alf, pos_rand, pos_keep[, refit]) as test_x47_agnostic.planted_rows."""
    run = G.RUNS[target]
    src = root / run
    src.mkdir(parents=True)
    rows = [r for t, p in planted.items() for r in TG.planted_rows(t, *p[:3], refit=p[3] if len(p) > 3 else None)]
    reader = {"org_read_accuracy": 0.95, "org_said_accuracy": 0.95, "pass": True, "eligible": 100}
    gate = {t: {"readers": {"lookup": reader}, "chosen": 100, "recall_read_on": 0} for t in planted}
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": X.PREDICTED[target],
                                                   "types": list(planted)}))  # fmt: skip
    (src / "gate.json").write_text(json.dumps({"gate": gate}))
    X.write_jsonl(src / "outcomes.jsonl", rows)
    return run


def planted_agnostic(tmp_path: Path, mp) -> Path:
    """The 9B: fruits and names both fall 0.40 beyond random with only-U 0.20 (yes); Muse: names fall 0.10 and only-U
    0.05, the refit passes (per item type)."""
    mp.setattr(G, "RESULTS", tmp_path)
    mp.setattr(G, "stored_animals", lambda target, n_boot=0: None)
    _sealed_open(mp)
    runs = [_agnostic_run(tmp_path, "qwen3.5-9b", {"animals": (0.10, 0.55, 0.30), "fruits": (0.15, 0.55, 0.20),
                                                     "names": (0.15, 0.55, 0.20)}),
            _agnostic_run(tmp_path, "muse-glimmer-30b", {"animals": (0.10, 0.55, 0.30), "fruits": (0.15, 0.55, 0.20),
                                                           "names": (0.45, 0.55, 0.05, (0.4, 0.3))})]  # fmt: skip
    return G.stage_verdict(runs, n_boot=N_BOOT)


# ---- 47.12: two definitions of the lens part --------------------------------------------------------------------------


def _twodefs_run(root: Path, target: str, recall_lost: dict, lookup_lost: dict) -> str:
    run = W.RUNS[target]
    src = root / run
    src.mkdir(parents=True)
    rows = [{**r, "layer": X.PREDICTED[target]} for r in TW.planted(recall_lost, lookup_lost)]
    stored = {r["scene"]: {} for r in rows}
    for r in rows:
        if r["arm"] == "whole":
            stored[r["scene"]][r["reader"]] = r["switched"]
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": X.PREDICTED[target],
                                                   "source": "planted_main"}))  # fmt: skip
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "cases.jsonl", [{"scene": s, "stored": {"whole": w}} for s, w in stored.items()])
    X.write_jsonl(src / "shares.jsonl", [{"share_omp25": 0.2, "share_top10": 0.1, "share_top10_state": 0.1,
                                          "overlap_top10_in_omp25": 4, "overlap_top10_state_in_omp25": 3,
                                          "overlap_top10_state_in_top10": 5, "top10_displaced_by_protection": 0}])  # fmt: skip
    (src / "plan.json").write_text(json.dumps({"items": 100, "items_at_L": 100}))
    return run


def planted_twodefs(tmp_path: Path, mp) -> Path:
    """The 9B: gap 0.50 under (i), 0.40 under (ii) (agree); Muse: 0.50 against 0.20 (differ)."""
    mp.setattr(W, "RESULTS", tmp_path)
    _sealed_open(mp)
    zero = {"omp25": 0.0, "top10": 0.0, "top10_state": 0.0}
    runs = [_twodefs_run(tmp_path, "qwen3.5-9b", {"omp25": 0.5, "top10": 0.4, "top10_state": 0.1}, zero),
            _twodefs_run(tmp_path, "muse-glimmer-30b", {"omp25": 0.5, "top10": 0.3, "top10_state": 0.1},
                         {**zero, "top10": 0.1})]  # fmt: skip
    return W.stage_verdict(runs, n_boot=N_BOOT)


# ---- 47.15: one question, two sources ---------------------------------------------------------------------------------


def _source_run(root: Path, target: str, lost: dict[str, tuple[float, float]], n: int = 80) -> str:
    """A finished 47.15 run, both placements: the whole change switches 80% of items under every condition; without
    J++ / without U + I each condition keeps (1 - lost) of them, the random parts keep all (no instruction as memory)."""
    run = Q.RUNS[target]
    src = root / run
    src.mkdir(parents=True)
    rows, cases, norms = [], [], []
    for p in Q.PLACEMENTS:
        for i in range(n):
            scene, ent = f"{p}-C2-{i:04d}", f"e{i % 20}"
            cases.append({"scene": scene, "placement": p, "chosen": True,
                          "unedited_class": {"none": {"org": "memory", "alt": "memory"}}})  # fmt: skip
            norms.append({"placement": p, "share_jpp": 0.2, "share_ui": 0.1})
            for cond in Q.CONDS:
                lj, lu = lost["memory" if cond == "none" else cond]
                whole = i < round(0.8 * n)
                sw = {"none": 0, "source": 1, "whole": whole, "no_jpp": i < round(0.8 * n * (1 - lj)),
                      "no_ui": i < round(0.8 * n * (1 - lu)), "no_jpp_rand": whole, "no_ui_rand": whole,
                      "keep_jpp": 0, "keep_jpp_rand": 0, "keep_ui": 0, "keep_ui_rand": 0}  # fmt: skip
                for a in Q.ARMS:
                    rows.append({"scene": scene, "placement": p, "reader": cond, "arm": a, "entity": ent,
                                 "switched_text": int(sw[a]), "switched_memory": int(sw[a])})  # fmt: skip
    acc = {"org_read_accuracy": {"text": 0.9, "memory": 0.9}, "pass": True, "eligible": n, "cases": n,
           "follows": {c: {"org": {"instructed": 0.9, "other_source": 0.05, "no_digit": 0.0}} for c in Q.INSTRUCTED}}  # fmt: skip
    gate = {"gate": dict.fromkeys(Q.PLACEMENTS, acc), "items": n, "entities": 20, "identity_dropped": 0, "dropped": {}}
    (src / "manifest.json").write_text(json.dumps({"model": {"target": target}, "layer": X.PREDICTED[target],
                                                   "placements": list(Q.PLACEMENTS)}))  # fmt: skip
    (src / "gate.json").write_text(json.dumps(gate))
    X.write_jsonl(src / "outcomes.jsonl", rows)
    X.write_jsonl(src / "cases.jsonl", cases)
    X.write_jsonl(src / "norms.jsonl", norms)
    return run


def planted_source(tmp_path: Path, mp) -> Path:
    """The 27B and the 9B: from the text like a lookup (J++ 0.05, U + I 0.50), from memory like a recall (0.50, 0.05):
    the part follows the source; Muse: both like a recall (follows the question)."""
    mp.setattr(Q, "RESULTS", tmp_path)
    mp.setattr(Q, "dan_answer", lambda rev="HEAD": "planted")
    mp.setattr(Q, "example_lines", lambda run, decode, **k: [])  # the verify pack needs prompts; the figure reads json
    source = {"text": (0.05, 0.5), "memory": (0.5, 0.05)}
    runs = [_source_run(tmp_path, "qwen3.6-27b", source), _source_run(tmp_path, "qwen3.5-9b", source),
            _source_run(tmp_path, "muse-glimmer-30b", {"text": (0.45, 0.0), "memory": (0.5, 0.05)})]  # fmt: skip
    return Q.stage_verdict(runs, n_boot=N_BOOT, decode_for=lambda target: None)


# ---- 47.16: distance ---------------------------------------------------------------------------------------------------


def _distance_run(root: Path, mp, target: str, fail_k: int | None, tag: str) -> str:
    """test_x47_distance's fake end-to-end run (its tokenizer, model and pointer basis), the gate failing at fail_k;
    renamed to the target's run with the target in its manifest."""
    from bridge_jspace import model as M
    from scripts import x0_massmean as MM

    mp.setattr(X, "render", TDist.wrap)
    mp.setattr(TDist.R, "pools", lambda tok: (TDist.LEGS, TDist.ANIMALS, TDist.PEOPLE))
    tok = TDist.WordTok()
    for d in range(10):
        tok(str(d))
    base = TDist.fake_base(12)
    for k in D.KS:
        D.cases_at(tok, base, k)
    fake = TDist.FakeModel(tok, vocab=len(tok.vocab) + 8)

    def competence(model, cs, digits, ws):
        return [{"scene": c["scene"], "rendering": "chat", "reader": w, "variant": v, "greedy": "", "said": "",
                 "right": not bad, "read_right": not bad, "ws_skipped": 0, "cand_right": not bad}
                for i, c in enumerate(cs) for w in X.READERS for v in ("org", "alt")
                for bad in [c["k"] == fail_k and w == X.RECALL and v == "org" and bool(i % 3)]]  # fmt: skip

    g = torch.Generator().manual_seed(5)
    alf, _ = torch.linalg.qr(torch.randn(32, 2, generator=g))
    mu = {s: (alf @ torch.tensor([float(s), float(s % 2)])).numpy().astype(np.float64) for s in TDist.W.SLOTS}
    mp.setattr(M, "load_model", lambda: fake)
    mp.setattr(X, "competence", competence)
    mp.setattr(D, "base_cases", lambda tok_, n=D.N_CAND: base)
    mp.setattr(MM, "pointer_means", lambda run: mu)
    mp.setattr(MM, "subspaces", lambda run: ({"Alf": alf.numpy().astype(np.float64)}, {}))
    out = D.stage_run(f"{pins.RUN_PREFIX}fake_x47_16_{tag}", "planted")
    run = D.RUNS[target]
    out.rename(root / run)
    man = root / run / "manifest.json"
    man.write_text(json.dumps({**json.loads(man.read_text()), "model": {"target": target}}))
    return run


def planted_distance(tmp_path: Path, mp) -> Path:
    """The 9B: every k passes its gate; Muse: the gate fails at k = 50 (breaks at k = 50)."""
    mp.setattr(D, "RESULTS", tmp_path)
    mp.setattr(D, "dan_answer", lambda rev="HEAD": "planted")
    mp.setattr(D, "routes_reference", lambda target: None)
    mp.setattr(D, "examples_lines", lambda runs, **k: [])  # the verify pack needs a tokenizer; the figure reads json
    runs = [_distance_run(tmp_path, mp, "qwen3.5-9b", None, "a"),
            _distance_run(tmp_path, mp, "muse-glimmer-30b", 50, "b")]  # fmt: skip
    return D.stage_verdict(runs, n_boot=N_BOOT)


PLANTED = {"47.14": planted_chain, "47.11": planted_agnostic, "47.12": planted_twodefs, "47.15": planted_source,
           "47.16": planted_distance, "D4": planted_depth}  # fmt: skip
VERDICT_FILE = {"47.14": "x47_14.json", "47.11": "x47_11.json", "47.12": "x47_12.json", "47.15": "x47_15.json",
                "47.16": "x47_16.json", "D4": "persistence.json"}  # fmt: skip
REAL = {"47.14": CHAIN, "D4": DEPTH}


def _rows_ok(test_id: str, name: str) -> None:
    rows = [r for r in S.ROWS if r["figure"] == B.fig_id(name)]
    assert rows and all(r["source"].endswith(VERDICT_FILE[test_id]) for r in rows)
    assert any(isinstance(r["value"], float) and r["lo"] is not None for r in rows) or test_id == "D4"
    assert any(isinstance(r["value"], float) for r in rows)


@pytest.mark.parametrize("test_id", list(B.TESTS))
def test_figure_on_its_planted_verdict(test_id, tmp_path, monkeypatch, saved):  # noqa: F811
    verdict = PLANTED[test_id](tmp_path / "results", monkeypatch)
    _, build, name = B.TESTS[test_id]
    assert build(verdict, name) == name
    assert (S.OUT / f"{name}.png").exists() and (S.OUT / f"{name}.svg").exists()
    check(saved[name])
    _rows_ok(test_id, name)


@pytest.mark.parametrize("test_id", list(REAL))
def test_figure_on_the_committed_verdict(test_id, monkeypatch, saved):  # noqa: F811
    _, build, name = B.TESTS[test_id]
    assert build(REAL[test_id], name) == name
    check(saved[name])
    _rows_ok(test_id, name)


def test_titles_read_the_outcomes(tmp_path, monkeypatch):
    v = {k: json.loads((PLANTED[k](tmp_path / k, monkeypatch) / VERDICT_FILE[k]).read_text()) for k in PLANTED}
    real = {k: json.loads((REAL[k] / VERDICT_FILE[k]).read_text()) for k in REAL}
    assert (
        B.chain_title(real["47.14"])
        == "The hall is readable at the locker digit, yet a random part cuts nearly as much"
    )
    assert B.chain_title(v["47.14"]) == B.chain_title(real["47.14"])  # one model tested reads the same
    assert B.agnostic_title(v["47.11"]) == "The pointer fit on animals transfers to fruits and names on 1 of 2 models"
    assert (
        B.twodefs_title(v["47.12"]) == "Two definitions of the J++ part agree on the recall–lookup gap on 1 of 2 models"
    )
    assert B.source_title(v["47.15"]) == "The part the answer needs follows its source, not the question"
    assert B.distance_title(v["47.16"]).startswith("Filler sentences before the picks: 9B ")
    assert B.distance_title(v["47.16"]).endswith("Muse breaks at 50 fillers")
    assert B.depth_title(real["D4"]) == "The address is re-encoded across depth on the 9B and Muse, not one code"
    assert B.depth_title(v["D4"]) == "The address across depth: one code on the 9B, re-encoded on Muse"


def test_a_given_title_wins(saved):  # noqa: F811
    B.build_chain(CHAIN, "fig21_chained_addresses", title="A claim Dan wrote")
    assert saved["fig21_chained_addresses"]["title"] == "A claim Dan wrote"


def test_a_long_subtitle_is_refused():
    with pytest.raises(AssertionError, match="subtitle on 3 lines"):
        B.frame("A title", "word " * 50, (1.0,), 1.0)
