"""finding5_confirm generalised to N statements: the 5-statement verdicts stay byte-identical (the committed ones are
recomputed), and on longer lists B pools the 3rd to the last statement."""

import json
import re

import pytest

from scripts import finding5_confirm as F

COMMITTED = sorted(F.OUT.glob("*/verdict.json"))


def _run_of(folder: str) -> str:
    return re.sub(r"_\d{8}-\d{6}$", "", folder)


@pytest.mark.parametrize("verdict", COMMITTED, ids=[p.parent.name for p in COMMITTED])
def test_committed_five_statement_verdicts_are_reproduced(verdict, tmp_path, capsys):
    """The default options (5 statements, every level) give the committed verdict.json and verdict.md byte for byte."""
    old = json.loads(verdict.read_text())
    if "sentences" in old:
        pytest.skip("a verdict made with the generalised options")
    run = _run_of(verdict.parent.name)
    if not (F.PS_RESULTS / run / "outcomes.jsonl").exists():
        pytest.skip(f"pointer_swap run {run} not present")
    by_layer = old["value_by_layer"]
    args = ["--layers", *by_layer] if by_layer else ["--layer", str(old["layer"])]
    assert F.main(["--run", run, *args, "--out", str(tmp_path)]) == 0
    capsys.readouterr()
    (new,) = tmp_path.iterdir()
    assert (new / "verdict.json").read_bytes() == verdict.read_bytes()
    assert (new / "verdict.md").read_bytes() == (verdict.parent / "verdict.md").read_bytes()


def _fake(n: int, level: str = "e8-digit", layer: int = 50) -> tuple[list[dict], dict[str, dict]]:
    """Every place k twice per topic and entity: position for k <= 2, identity from the 3rd on (finding 5's shape)."""
    rows, items = [], {}
    for dom in ("animals", "body", "countries"):
        for e in ("x", "y", "z", "w"):
            for k in range(1, n + 1):
                for rep in range(2):
                    name = f"{dom}-RL-{level}-{e}{k}{rep}"
                    items[name] = {"entities": ["e"] * n, "slots": {"position": k - 1}, "domain": dom, "query": e}
                    role = "position" if k <= 2 else "identity"
                    rows.append({"name": name, "family": "RL", "domain": dom, "level": level, "layer": layer,
                                 "source": "dissoc", "group": "last", "role": role})  # fmt: skip
    return rows, items


def test_b_pools_the_third_to_the_last_statement():
    for n in (5, 8, 12):
        rows, items = _fake(n)
        fam = F.confirm(F.select(rows, items, None, n), 50, n)["RL"]
        assert list(fam["by_k"]) == list(range(1, n + 1))
        assert fam["first2"]["n"] == 3 * 4 * 2 * 2 and fam["rest"]["n"] == 3 * 4 * 2 * (n - 2)
        assert fam["first2"]["position_minus_identity"][0] == 1.0 and fam["rest"]["identity_minus_position"][0] == 1.0
        assert fam["verdict"] == "confirms"


def test_the_list_length_must_match_the_items():
    rows, items = _fake(8)
    with pytest.raises(AssertionError, match="8 statements"):
        F.select(rows, items, None, 5)


def test_level_keeps_one_level_and_the_layer_rule_reads_it():
    digit, it_d = _fake(8, "e8-digit", 46)
    word, it_w = _fake(8, "e8-word", 46)
    for r in word:  # the word level's donor answer arrives at 46; the digit level's never does
        r["role"] = "value"
    late_w, it_lw = _fake(8, "e8-word", 44)
    late_d, it_ld = _fake(8, "e8-digit", 44)
    items = {**it_d, **it_w, **it_lw, **it_ld}
    rows = digit + word + late_w + late_d
    sel = F.select(rows, items, "e8-digit", 8)
    assert {r["level"] for r in sel} == {"e8-digit"}
    assert F.pick_layer(sel, [44, 46], "RL")[0] == 46
    assert F.pick_layer(F.select(rows, items, "e8-word", 8), [44, 46], "RL")[0] == 44


def test_report_names_the_last_statement():
    rows, items = _fake(12, "e12-word")
    sel = F.select(rows, items, "e12-word", 12)
    out = {"run": "r", "level": "e12-word", "sentences": 12, "layer": 50, "value_by_layer": {},
           "families": F.confirm(sel, 50, 12)}  # fmt: skip
    text = F.report(out, "RL", 12)
    assert "3rd-12th" in text and "(e12-word, 12 statements)" in text
    ks = (1, 2, 3, 5, 8, 11, 12, 21)
    assert [F.ordinal(k) for k in ks] == ["1st", "2nd", "3rd", "5th", "8th", "11th", "12th", "21st"]
