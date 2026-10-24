"""x0_parts: the word's surface variants, and the verdict reads planted part effects."""

import json

from scripts import x0_parts as W


def test_variants():
    v = W.variants("frog")
    assert {"frog", " frog", "Frog", " Frog", "FROG", " FROG", "frogs", " frogs", "Frogs", " Frogs"} == set(v)


def test_verdict_reads_planted_effects(tmp_path, monkeypatch):
    monkeypatch.setattr(W, "RESULTS", tmp_path)
    src = tmp_path / "fake"
    src.mkdir()
    m = {"model": {"target": "fake"}, "layer": 32, "single": "s", "items": 120,
         "pca": {"n": 2000, "prompts": 200, "set": "x", "tokens": 1, "variance_share": 0.9}}  # fmt: skip
    (src / "manifest.json").write_text(json.dumps(m))
    rows, shares = [], []
    for i in range(120):
        base = {"scene": f"s{i}", "entity": f"e{i % 30}", "rendering": "chat", "layer": 32, "upstream": False}
        for w in ("PP", "PM"):
            rows.append({**base, "reader": w, "dict": "-", "k": 0, "omp": "-", "arm": "whole", "switched": 1})
            for d, k, fit in (("w", 0, "lsq"), ("jw", 25, "signed"), ("pca", 25, "signed"), ("jpp", 25, "signed")):
                lost = w == "PM" and d in ("jw", "jpp")  # planted: recall loses its flips to J++ beyond the word only
                rows.append(
                    {**base, "reader": w, "dict": d, "k": k, "omp": fit, "arm": "no_part", "switched": int(not lost)}
                )
                rows.append({**base, "reader": w, "dict": d, "k": k, "omp": fit, "arm": "no_rand", "switched": 1})
        for d in W.PARTS:
            shares.append({"scene": f"s{i}", "dict": d, "share": 0.1, **({"variants": 6} if d == "w" else {})})
    (src / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (src / "shares.jsonl").write_text("".join(json.dumps(r) + "\n" for r in shares))
    blob = json.loads((W.stage_verdict("fake", 200) / "verdict.json").read_text())
    ex = {(r["part"], r["reader"]): r["excess"][0] for r in blob["rows"]}
    assert ex[("jw", "PM")] == 1.0 and ex[("jpp", "PM")] == 1.0
    assert ex[("w", "PM")] == 0.0 and ex[("pca", "PM")] == 0.0 and ex[("jw", "PP")] == 0.0
