"""x0_amnesic: the probe subspace spans the planted class directions; the verdict reads planted arm effects."""

import json

import numpy as np

from scripts import x0_amnesic as A
from scripts import x0_probe as P


def test_subspace_spans_the_planted_directions():
    rng = np.random.default_rng(0)
    d, n, k = 40, 300, 4
    dirs = np.linalg.qr(rng.normal(size=(d, k)))[0]  # [d, k] orthonormal
    y = [int(v) for v in rng.integers(0, k, n)]
    x = rng.normal(size=(n, d)) * 0.3 + 3.0 * dirs[:, y].T
    q = P.subspace(x, y, 1e-2)
    assert q.shape == (d, k - 1)
    centered = dirs - dirs.mean(1, keepdims=True)  # the class-mean differences live in this span (rank k - 1)
    cos = np.linalg.svd(q.T @ np.linalg.qr(centered)[0][:, : k - 1], compute_uv=False)
    assert cos.min() > 0.8  # a discriminative probe's weights also carry some noise directions
    assert np.allclose(q.T @ q, np.eye(k - 1), atol=1e-8)


def test_verdict_reads_planted_arm_effects(tmp_path, monkeypatch):
    monkeypatch.setattr(A, "RESULTS", tmp_path)
    src = tmp_path / "fake"
    src.mkdir()
    m = {"model": {"target": "fake"}, "layer": 32, "single": "s", "probe": {"rank": 4, "probe_run": "p", "n": 300,
                                                                            "cv_accuracy": 0.9}}  # fmt: skip
    (src / "manifest.json").write_text(json.dumps(m))
    rows = []
    for i in range(120):
        for w in ("PP", "PM"):
            base = {"scene": f"s{i}", "entity": f"e{i % 30}", "reader": w, "order": "before", "share": 0.01}
            lookup = w == "PP"
            out = {"none": 0, "whole": 1, "no_probe": 0 if lookup else 1, "no_rand": 1,
                   "probe_only": 1 if lookup else 0, "rand_only": 0}  # fmt: skip
            rows += [{**base, "arm": a, "switched": s} for a, s in out.items()]
    (src / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    blob = json.loads((A.stage_verdict("fake", 200) / "verdict.json").read_text())
    lk = next(r for r in blob["rows"] if r["reader"] == "PP")
    rc = next(r for r in blob["rows"] if r["reader"] == "PM")
    assert lk["excess"][0] == 1.0 and lk["sufficiency_diff"][0] == 1.0
    assert rc["excess"][0] == 0.0 and rc["sufficiency_diff"][0] == 0.0
