"""Batch 49, test 49.5 (scripts/x49_clean.py): the row-for-row comparison and the headline cells on planted record /
clean runs (identical -> all zero; one changed row -> listed), the 47.8 scope, pending runs and the write-once json."""

import copy
import json
from pathlib import Path

import pytest

from scripts import x49_clean as C

SCENES = ("s1", "s2", "s3", "s4")


def _read(**kw) -> dict:
    return {"switched": 0, "cand_switched": 0, "cand_org_first": 1, "role": "A", "p_org": 0.9, "p_alt": 0.05,
            "ld": -3.0, **kw}  # fmt: skip


def _main_rows() -> list[dict]:
    rows = []
    for i, s in enumerate(SCENES):
        for w in ("PP", "PM"):
            base = {"scene": s, "entity": f"e{i % 2}", "rendering": "chat", "layer": 12, "reader": w, "upstream": False,
                    "ws_skipped": 0}  # fmt: skip
            rows.append({**base, "dict": "-", "k": 0, "omp": "-", "arm": "whole", **_read(switched=1)})
            # lookup: no_part keeps every switch, no_rand loses one; recall: no_part loses three, no_rand none
            part = int(w == "PP" or i == 0)
            rand = int(w == "PM" or i != 0)
            for arm, sw in (("no_part", part), ("no_rand", rand)):
                rows.append({**base, "dict": "jpp", "k": 25, "omp": "signed", "arm": arm, **_read(switched=sw)})
    return rows


def _route_rows(arms: dict[str, tuple[str, ...]]) -> list[dict]:
    """arms: arm -> the lookup's route per scene (the recall's rows get route 'original')."""
    return [{"scene": s, "condition": "C2", "entity": "e", "reader": w, "arm": arm, "top": 17 + j,
             "route": routes[j] if w == "PP" else "original", **_read()}
            for arm, routes in arms.items() for j, s in enumerate(SCENES) for w in ("PP", "PM")]  # fmt: skip


def _zero_rows() -> list[dict]:
    kept = {"none": (1, 1, 1, 1), "zero_L": (1, 1, 1, 0), "rand_L": (1, 1, 1, 1)}
    return [{"scene": s, "entity": "e", "reader": w, "arm": arm, "kept": ks[j], "to_org": 1 - ks[j], "cand_kept": ks[j],
             "top": 20, "role": "b", **{k: v for k, v in _read().items() if k in C.NUMERIC}}
            for arm, ks in kept.items() for j, s in enumerate(SCENES) for w in ("PP", "PM")]  # fmt: skip


def _anatomy_rows(layers=(10, 12, 14)) -> list[dict]:
    route = {10: ("identity",) * 4, 12: ("position", "position", "identity", "identity"), 14: ("position",) * 4}
    rows = []
    for j, s in enumerate(SCENES):
        for w in ("PP", "PM"):
            rows.append({"scene": s, "condition": "C2", "reader": w, "layer": None, "arm": "none", "route": "original",
                         "top": 17, "top_text": "2", **_read()})  # fmt: skip
            for la in layers:
                for arm in ("whole", "no_J"):
                    rows.append({"scene": s, "condition": "C2", "reader": w, "layer": la, "arm": arm,
                                 "route": route[la][j] if w == "PP" else "changed", "top": 18, "top_text": "3",
                                 **_read(switched=1)})  # fmt: skip
    return rows


RECORD_ROWS = {
    "main test": _main_rows,
    "routes": lambda: _route_rows(
        {
            "whole": ("identity", "position", "position", "value"),
            "no_alf": ("identity", "original", "original", "original"),
            "no_alf_rand": ("identity", "position", "position", "original"),
        }
    ),
    "only-U": lambda: _route_rows(
        {"keep_alf": ("position", "original", "original", "original"), "keep_alf_rand": ("original",) * 4}
    ),
    "47.5 zeroing": _zero_rows,
    "47.8 anatomy": _anatomy_rows,
}


def _write(path: Path, rows: list[dict], sha: str) -> None:
    path.mkdir(parents=True)
    (path / "outcomes.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (path / "manifest.json").write_text(json.dumps({"code": {"sha": sha, "dirty": sha == "rec"}}) + "\n")


@pytest.fixture
def plant(tmp_path, monkeypatch):
    """Planted record runs and clean runs (the clean ones from `clean`: label -> rows, or None to leave one out)."""
    monkeypatch.setattr(C, "RESULTS", tmp_path / "results")
    monkeypatch.setattr(C, "OUT", tmp_path / "results" / "checks" / "clean49_9b.json")
    monkeypatch.setattr(C, "DOC", tmp_path / "handcheck_clean49.md")
    record = {label: make() for label, make in RECORD_ROWS.items()}

    def go(edit=None, skip=()):
        for p in C.PAIRS:
            _write(C.RESULTS / p.exp / p.record, record[p.label], "rec")
            if p.label in skip:
                continue
            clean = copy.deepcopy(record[p.label])
            if p.label == "47.8 anatomy":  # the clean run has L10 and L12 only
                clean = [r for r in clean if r["layer"] != 14]
            if edit:
                clean = edit(p.label, clean)
            _write(C.RESULTS / p.exp / p.clean, clean, "abc123")
        return record

    return go


def test_identical_runs_are_all_zero_and_the_cells_are_the_record_values(plant):
    plant()
    rep = C.build()
    assert rep["all_identical"] is True
    for c in rep["comparisons"]:
        assert c["identical"] and c["only_record"] == c["only_clean"] == 0
        assert c["rows_record"] == c["rows_clean"] == c["shared"]
        assert not any(c["differing"].values()) and not any(c["max_abs_diff"].values())
        assert c["examples"] == [] and c["clean_code"] == {"sha": "abc123", "dirty": False}
    cells = {c["cell"]: c for c in rep["cells"]}
    assert all(c["same"] for c in rep["cells"])
    # the planted counts: lookup (no_rand 3 - no_part 4) / 4, recall (4 - 1) / 4 -> gap 0.75 + 0.25 = 1.0
    gap = cells["Main test gap (recall extra loss minus lookup extra loss), L12, chat"]
    assert gap["record"] == pytest.approx(1.0) and gap["n_record"] == 4
    assert cells["Routes, another item moved, whole change: position share"]["record"] == 0.5
    assert cells["Routes, another item moved, whole change: value share"]["record"] == 0.25
    assert cells["Pointer directions removed: position share"]["record"] == 0.0
    assert cells["Only the pointer directions added (only-U): position share"]["record"] == 0.25
    assert cells["47.5: recall answers kept, J++ atoms zeroed at L12"]["record"] == 0.75
    assert cells["47.8: position share under the whole change at L12"]["record"] == 0.5
    assert cells["47.8: position share under the whole change at L10"]["record"] == 0.0


def test_the_anatomy_record_is_compared_at_l10_l12_and_the_unedited_row_only(plant):
    plant()
    c = next(c for c in C.build()["comparisons"] if c["test"] == "47.8 anatomy")
    assert c["rows_record"] == len([r for r in _anatomy_rows() if r["layer"] != 14])  # L14 out of scope
    assert c["identical"]


def test_one_changed_row_is_listed(plant):
    def edit(label, rows):
        if label == "47.8 anatomy":
            r = next(r for r in rows if r["reader"] == "PP" and r["layer"] == 12 and r["arm"] == "whole")
            r["route"], r["ld"] = "identity", r["ld"] + 0.5
        return rows

    plant(edit)
    rep = C.build()
    assert rep["all_identical"] is False
    by = {c["test"]: c for c in rep["comparisons"]}
    c = by["47.8 anatomy"]
    assert not c["identical"]
    assert c["differing"]["route"] == 1 and sum(c["differing"].values()) == 1
    assert c["max_abs_diff"]["ld"] == pytest.approx(0.5) and c["max_abs_diff"]["p_org"] == 0.0
    assert c["examples"] == [{"key": {"scene": "s1", "condition": "C2", "reader": "PP", "layer": 12, "arm": "whole"},
                              "differs": {"route": ["position", "identity"]}}]  # fmt: skip
    assert all(by[t]["identical"] for t in by if t != "47.8 anatomy")
    cell = next(x for x in rep["cells"] if x["cell"].endswith("at L12") and x["test"] == "47.8 anatomy")
    assert cell["same"] is False and cell["record"] == 0.5 and cell["clean"] == 0.25
    doc = C.render(rep)
    assert "**no**" in doc and '"route": ["position", "identity"]' in doc


def test_rows_only_in_one_run_are_counted(plant):
    def edit(label, rows):
        if label == "47.5 zeroing":
            rows = [*rows[1:], {**rows[0], "scene": "s9"}]
        return rows

    plant(edit)
    c = next(c for c in C.build()["comparisons"] if c["test"] == "47.5 zeroing")
    assert (c["only_record"], c["only_clean"], c["shared"]) == (1, 1, c["rows_record"] - 1)
    assert c["only_record_first"] == [{"scene": "s1", "reader": "PP", "arm": "none"}]
    assert not c["identical"]


def test_pending_writes_the_doc_alone_and_a_full_run_writes_the_json_once(plant):
    plant(skip=("routes",))
    with pytest.raises(AssertionError, match="pull the clean runs"):
        C.build()
    C.main(["--pending"])
    assert not C.OUT.exists()
    doc = C.DOC.read_text()
    assert "| 0.50 | pending |" in doc and "All identical: pending." in doc
    p = next(p for p in C.PAIRS if p.label == "routes")
    _write(C.RESULTS / p.exp / p.clean, RECORD_ROWS["routes"](), "abc123")
    C.main([])
    rep = json.loads(C.OUT.read_text())
    assert rep["all_identical"] is True and len(rep["comparisons"]) == len(C.PAIRS)
    assert "All identical: yes." in C.DOC.read_text()
    with pytest.raises(AssertionError, match="written once"):
        C.main([])
