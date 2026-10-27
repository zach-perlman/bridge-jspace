"""scripts/handcheck_pack.py on the repo's runs: the six recounts reproduce figures/story/data.csv (value and CI at 2
decimals), the comparison fails on a wrong value, and the shown prompt is the stored ids' exact decode with the bridge
marked; the batch-45 additions' loaders find their item sets, their recounts match the runs' verdict / table files and
stop matching when an item changes, and their prompts decode exactly with each model's tokenizer. Uses the pinned
tokenizers (hf_hub_download, cached), as tests/test_review.py."""

import copy

import pytest

from bridge_jspace.review import checks as C
from scripts import handcheck_pack as H

HEADLINES = {  # the numbers as the README / data.csv state them
    "contrast_9b": "0.53 [0.42, 0.61]",
    "lk_order_before_9b_k": "86",
    "lk_order_after_9b_k": "19",
    "rt_C2_whole_identity_9b": "0.48 [0.43, 0.53]",
    "rt_C2_whole_position_9b": "0.51 [0.46, 0.56]",
    "rt_C2_whole_value_9b": "0.00 [0.00, 0.00]",
    "rt_C2_no_alf_position_9b": "0.08 [0.05, 0.12]",
    "rt_C2_no_alf_rand_position_9b": "0.54 [0.49, 0.59]",
    "x8_t2_9b": "0.46 [0.42, 0.50]",
    "sbo_swap_before_gap_9b": "0.34 [0.23, 0.43]",
}


@pytest.fixture(scope="module")
def nums() -> list[H.Number]:
    return H.numbers()


def test_every_recount_matches_data_csv(nums):
    assert [n.no for n in nums] == [1, 2, 3, 4, 5, 6]
    assert [(n.no, c) for n in nums for c in n.checks if not c["match"]] == []


def test_headlines_recount_to_the_stated_values(nums):
    assert {c["key"]: c["recount"] for n in nums for c in n.headline()} == HEADLINES


def test_the_comparison_fails_on_a_wrong_value_or_a_missing_key():
    assert H.check("contrast_9b", "0.53 [0.42, 0.61]")["match"]
    assert not H.check("contrast_9b", "0.52 [0.42, 0.61]")["match"]
    assert not H.check("contrast_9b", "0.53 [0.41, 0.61]")["match"]  # the CI counts too
    assert not H.check("no_such_key_9b", "0.53")["match"]


def test_item_sets_have_the_stated_sizes(nums):
    assert [len(n.pool) for n in nums] == [200, 200, 300, 300, 600, 100]


def test_samples_are_fixed_and_the_prompt_is_the_exact_decode(nums):
    n = nums[0]
    first, again = H.draw(n.pool), H.draw(n.pool)
    assert len(first) == H.N_SHOW
    assert [it["scene"] for it in first] == [it["scene"] for it in again]
    c = first[0]["case"]
    ids = c["readers"]["PP"]["ids"]["org"]
    fence, text, end, _ = H.prompt(ids, c["pos"])
    assert (fence, end) == ("```text", "```")
    assert text.count("⟦") == 1 and f"⟦{c['bridge']}⟧" in text
    shown = text.replace("⟦", "").replace("⟧", "").removesuffix(H.SPACE)
    assert shown == C.tokenizer(H.MODEL).decode(ids, skip_special_tokens=False)


# ---- batch 45 additions: each part's own loader, recounted against its run's verdict / table file

BATCH45_HEADLINES = {  # as Dan's brief (26 Oct ~21:45) and the files state them
    ("A", "V0 whole: identity"): "103 of 191, 0.54",
    ("A", "V2 whole: identity"): "183 of 191, 0.96",
    ("B · 9B", "a: switched"): "20 of 100, 0.20",
    ("B · 9B", "b_half: switched"): "68 of 100, 0.68",
    ("B · 9B", "c: switched"): "66 of 100, 0.66",
    ("B · 9B", "d: switched"): "12 of 100, 0.12",
    ("B · 27B", "a: switched"): "8 of 99, 0.08",
    ("B · 27B", "b_half: switched"): "78 of 99, 0.79",
    ("B · 27B", "c: switched"): "59 of 99, 0.60",
    ("B · 27B", "d: switched"): "3 of 99, 0.03",
    ("C", "extra loss (the rule's number)"): "(83 − 46) / 79 = 0.47 [0.34, 0.60]",
}


@pytest.fixture(scope="module")
def adds() -> dict[str, H.Addition]:
    return {a.tag: a for a in H.additions()}


def test_batch45_loaders_find_the_item_sets(adds):
    assert {t: len(a.pool) for t, a in adds.items()} == {"A": 191, "B · 9B": 100, "B · 27B": 99, "C": 238}
    assert all(0 in it["move"] for it in adds["A"].pool)  # first-locker moves only
    assert all(it["cases"]["V2"]["prepended"] and not it["cases"]["V0"]["prepended"] for it in adds["A"].pool)
    assert all(it["case"]["format"] == "table" and it["layer"] == 26 for it in adds["C"].pool)


def test_batch45_recounts_match_their_files(adds):
    assert [(t, c) for t, a in adds.items() for c in a.checks if not c["match"]] == []
    head = {(t, c["what"]): c["recount"] for t, a in adds.items() for c in a.checks if c["head"]}
    assert head == BATCH45_HEADLINES


def test_batch45_recounts_flag_a_changed_item(adds):
    """One item's stored outcome changed: the recount no longer matches its file."""
    a = copy.deepcopy(adds["A"].pool)
    a[0]["rows"][("V0", "whole")]["route"] = "value"
    assert not all(c["match"] for c in H.x45a_number(a).checks)
    b = copy.deepcopy(adds["B · 27B"].pool)
    b[0]["rows"]["c"]["switched"] = 1 - b[0]["rows"]["c"]["switched"]
    assert "c: switched" in [c["what"] for c in H.x45b_number("qwen3.6-27b", b).checks if not c["match"]]
    d = copy.deepcopy(adds["C"].pool)
    d[0]["rows"]["no_part"]["switched"] = 1 - d[0]["rows"]["no_part"]["switched"]
    assert not next(c for c in H.x45d_number(d).checks if c["head"])["match"]


@pytest.mark.parametrize("tag", ["A", "B · 27B", "C"])
def test_batch45_cards_show_the_exact_prompt_in_each_models_tokens(adds, tag):
    a = adds[tag]
    it = H.draw(a.pool, H.N_SHOW_45)[0]
    lines = a.card(it)
    blocks = [lines[i + 1] for i, x in enumerate(lines) if x == "```text"]
    c = it["cases"]["V2"] if tag == "A" else it["case"]
    want = C.tokenizer(a.model).decode(c["readers"]["PP"]["ids"]["org"], skip_special_tokens=False)
    shown = [b.translate({ord(ch): None for ch in "⟦⟧«»"}).removesuffix(H.SPACE) for b in blocks]
    assert want in shown
    assert all(b.count("⟦") == 1 for b in blocks)
    if tag == "A":  # V0, then V2 with its prepended pick sentence first
        assert blocks[1].split("\n")[1].startswith(c["prepended"])
    if tag.startswith("B"):  # the patched locker-sentence tokens marked apart from the bridge
        assert "«The locker of" in blocks[0]


def test_runs_of_merges_consecutive_positions():
    assert H.runs_of([9, 3, 4, 5, 10]) == [(3, 6), (9, 11)]
    assert H.runs_of([]) == []
