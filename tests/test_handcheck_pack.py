"""scripts/handcheck_pack.py on the repo's runs: the six recounts reproduce figures/story/data.csv (value and CI at 2
decimals), the comparison fails on a wrong value, and the shown prompt is the stored ids' exact decode with the bridge
marked. Uses the pinned tokenizer (hf_hub_download, cached), as tests/test_review.py."""

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
