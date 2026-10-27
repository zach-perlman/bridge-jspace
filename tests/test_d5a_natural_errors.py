"""d5a_natural_errors: the pre-registered verdict from saved rows (no model)."""

import json

from scripts import d5a_natural_errors as N


def row(right: bool, asked: int, answered, top: int, i: int) -> dict:
    return {"id": f"x{i}", "set": "main", "label": "main/elements_RL_e5f0-syn", "family": "RL", "domain": "elements",
            "level": "e5f0-syn", "entity": f"e{i % 6}", "top": "3", "right": right, "asked": asked,
            "answered": answered, "heads": {"51:22": {"top": top, "masses": []}}}  # fmt: skip


def run(tmp_path, monkeypatch, rows):
    monkeypatch.setattr(N, "RESULTS", tmp_path)
    d = tmp_path / "r"
    d.mkdir(parents=True)
    (d / "manifest.json").write_text(json.dumps({"heads": ["51:22"]}))
    (d / "rows.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    N.stage_summarise("r")
    out = next(d.glob("analysis-*/summary.json"))
    return json.loads(out.read_text())


def test_fetch_bridge_and_too_few(tmp_path, monkeypatch):
    wrong_fetch = [row(False, 0, 2, 2, i) for i in range(40)]
    right = [row(True, 1, 1, 1, 100 + i) for i in range(20)]
    s = run(tmp_path / "a", monkeypatch, wrong_fetch + right)
    assert s["heads"]["51:22"]["verdict"] == "H-fetch" and s["n_wrong_in_context"] == 40
    assert s["heads"]["51:22"]["right_on_asked"]["rate"][0] == 1.0
    wrong_bridge = [row(False, 0, 2, 0, i) for i in range(40)]
    s = run(tmp_path / "b", monkeypatch, wrong_bridge)
    assert s["heads"]["51:22"]["verdict"] == "H-bridge"
    few = [row(False, 0, 2, 2, i) for i in range(10)] + [row(False, 0, None, 1, 50)]
    s = run(tmp_path / "c", monkeypatch, few)
    assert s["heads"]["51:22"]["verdict"] == "too few errors" and s["n_wrong_off_prompt"] == 1
