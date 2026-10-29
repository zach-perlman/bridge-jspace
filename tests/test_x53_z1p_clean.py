"""Dan 12:50 item 0 (scripts/x53_z1p_clean.py): the excluded passages are the verify check's (the bridge's true value as
a whole word in the lookup's passage), both readers' rows of an excluded passage are dropped, and the full set
recomputed matches the stored Z1-P verdict. CPU, the stored run; no model."""

import json

import pytest

from scripts import x50_zach as Z
from scripts import x53_z1p_clean as C


def _case(true: str, k_context: str) -> dict:
    return {"readers": {"K": {"context": k_context, "answer": "made-up"}, "M": {"context": "-", "answer": true}}}


def test_true_in_lookup_passage_is_a_whole_word_case_insensitive():
    assert C.true_in_lookup_passage(_case("Russia", "The partner city for Mumbai is in russia."))
    assert not C.true_in_lookup_passage(_case("Russia", "The partner city for Mumbai is in Belarussia."))
    assert not C.true_in_lookup_passage(_case("Peru", "Moscow is in Chile."))


def test_on_the_stored_run(tmp_path):
    if not (Z.RESULTS / C.RUN / "outcomes.jsonl").exists() or not C.VERIFY.exists():
        pytest.skip("the stored Z1-P run or the verify checks are not in this checkout")
    out = C.stage(run=C.RUN, out_root=tmp_path)
    blob = json.loads((out / "verdict.json").read_text())
    assert len(blob["excluded"]) == 60 and blob["chosen"] == 200
    assert blob["excluded"][0] == "jsuite_v2_test_chat/j2:cities:P-L0-Moscow-0"
    rec = blob["layers"]["12"]
    assert rec["full_matches_stored"] is True
    assert rec["full"]["n"] == 200 and rec["clean"]["n"] == 140  # passages: K and M rows dropped together
    assert (out / "excluded.json").exists() and "Status: UNVERIFIED" in (out / "verdict.md").read_text()
