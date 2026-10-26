"""T's analysis (scripts/t_pointer.py) on planted runs: the pointer cells, the bars and who counts as tested."""

import json

from scripts import t_pointer as T


def _x0b(root, run, lookup_lost: bool):
    src = root / run
    src.mkdir(parents=True)
    (src / "manifest.json").write_text(json.dumps({"predicted": 12}))
    cases, rows = [], []
    for i in range(80):
        s = f"s{i}"
        cases.append({"scene": s, "format": ("prose", "json", "table")[i % 3]})
        for w in ("PP", "PM"):
            base = {"scene": s, "entity": f"e{i % 16}", "rendering": "chat", "layer": 12, "reader": w}
            rows.append({**base, "dict": "-", "k": 0, "omp": "-", "arm": "whole", "switched": 1})
            lost = lookup_lost and w == "PP"
            rows.append({**base, "dict": "alf", "k": 4, "omp": "signed", "arm": "no_part", "switched": int(not lost)})
            rows.append({**base, "dict": "alf", "k": 4, "omp": "signed", "arm": "no_rand", "switched": 1})
    (src / "cases.jsonl").write_text("".join(json.dumps(c) + "\n" for c in cases))
    (src / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))


def test_bars_count_only_landed_models(tmp_path, monkeypatch):
    monkeypatch.setattr(T, "X0B", tmp_path / "x0b")
    monkeypatch.setattr(T, "NAT", tmp_path / "nat")
    monkeypatch.setattr(T, "RUNS", {"a": ("xa", "na"), "b": ("xb", "nb"), "c": ("xc", "nc")})
    _x0b(tmp_path / "x0b", "xa", lookup_lost=True)
    _x0b(tmp_path / "x0b", "xb", lookup_lost=False)
    (tmp_path / "nat" / "na").mkdir(parents=True)  # stopped at its gate: no outcomes
    per = {m: {"varied": T.varied(x, 200), "natural": T.natural(n, 200)} for m, (x, n) in T.RUNS.items()}
    assert abs(per["a"]["varied"]["pooled"]["PP"]["excess"][0] - 1.0) < 1e-9
    assert per["a"]["varied"]["json + table"]["n"] == 53
    assert per["a"]["natural"] == {"gate": False} and per["c"]["natural"] is None and per["c"]["varied"] is None
    q1 = T.count(per, "q42_1")
    assert q1["passed"] == ["a"] and q1["tested"] == ["a", "b"] and q1["option"] == "(c) one or two" and not q1["final"]
    assert T.count(per, "q42_3")["tested"] == []
