"""scripts/handcheck_pack.py on the repo's runs: the six recounts reproduce figures/story/data.csv (value and CI at 2
decimals), the comparison fails on a wrong value, and the shown prompt is the stored ids' exact decode with the bridge
marked; the batch-45 additions' loaders find their item sets, their recounts match the runs' verdict / table files and
stop matching when an item changes, and their prompts decode exactly with each model's tokenizer. Uses the pinned
tokenizers (hf_hub_download, cached), as tests/test_review.py. The 45m / 45q / 45p parts: every run of the three
models found, the recounts match the verdict files and flag a changed item, the 10 items per part are the seed-0
draw, every item's marked positions agree with the stored ones (and a moved one is caught), and the cards show the
exact prompts marked and every arm's stored answer for both readers."""

import copy
import random
import re

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


# ---- 45m, 45q, 45p (Dan 27 Oct ~14:40): each test on the 9B, the 27B and Muse, 10 items each

QPM_SIZES = {"45m · 9B": 417, "45m · 27B": 574, "45m · Muse": 409, "45q · 9B": 201, "45q · 27B": 288,
             "45q · Muse": 205, "45p · 9B": 186, "45p · 27B": 254, "45p · Muse": 178}  # fmt: skip
QPM_HEADLINES = {  # as predictions/2026-10-26_dan.md (Q45.10, Q45.12, Q45.13) and the verdict files state them
    ("45m · 9B", "locker-before: gap"): "0.23 [0.14, 0.31]",
    ("45m · 27B", "locker-before: gap"): "0.53 [0.42, 0.62]",
    ("45m · Muse", "locker-before: gap"): "0.38 [0.23, 0.54]",
    ("45q · 9B", "a: lookup switched"): "34 of 201, 0.17 [0.12, 0.22]",
    ("45q · 27B", "a: lookup switched"): "4 of 288, 0.01 [0.00, 0.03]",
    ("45q · Muse", "a: lookup switched"): "2 of 205, 0.01 [0.00, 0.03]",
    ("45q · 9B", "c among S's switches: lookup"): "140 of 201, 0.70 [0.65, 0.74]",
    ("45q · 27B", "c among S's switches: lookup"): "214 of 288, 0.74 [0.68, 0.80]",
    ("45q · Muse", "c among S's switches: lookup"): "155 of 205, 0.76 [0.70, 0.81]",
    ("45p · 9B", "recall: loss_2 − loss_3"): "0.25 [0.16, 0.34]",
    ("45p · 27B", "recall: loss_2 − loss_3"): "0.41 [0.32, 0.53]",
    ("45p · Muse", "recall: loss_2 − loss_3"): "0.42 [0.26, 0.63]",
    ("45p · 9B", "recall: loss_2 − loss_4"): "0.26 [0.18, 0.35]",
    ("45p · 27B", "recall: loss_2 − loss_4"): "0.49 [0.38, 0.64]",
    ("45p · Muse", "recall: loss_2 − loss_4"): "0.49 [0.31, 0.69]",
}
QPM_DRAWN_9B = {  # random.Random(0).sample(items, 10) over each 9B run's items sorted by scene
    "45m · 9B": ["P2-L0-0293", "P2-L0-0559", "P2-L0-0317", "P2-L0-0031", "P2-L0-0196", "P2-L0-0379", "P2-L0-0358",
                 "P2-L0-0309", "P2-L0-0579", "P2-L0-0234"],
    "45q · 9B": ["P2-L0-0306", "P2-L0-0584", "P2-L0-0321", "P2-L0-0045", "P2-L0-0210", "P2-L0-0387", "P2-L0-0376",
                 "P2-L0-0315", "P2-L0-0599", "P2-L0-0240"],
    "45p · 9B": ["P2-L0-0330", "P2-L0-0353", "P2-L0-0031", "P2-L0-0217", "P2-L0-0414", "P2-L0-0399", "P2-L0-0340",
                 "P2-L0-0246", "P2-L0-0392", "P2-L0-0301"],
}  # fmt: skip
QPM_ARMS = {"45m": 4, "45q": 9, "45p": 7}  # arms shown per reader on each card


@pytest.fixture(scope="module")
def qpm() -> dict[str, H.Addition]:
    got = {a.tag: a for a in H.additions_qpm()}
    for a in got.values():
        a.sample = H.draw(a.pool)
    return got


def test_qpm_loaders_find_every_run_and_item_set(qpm):
    assert {t: len(a.pool) for t, a in qpm.items()} == QPM_SIZES
    assert {(t.split(" · ")[0], a.model) for t, a in qpm.items()} == {
        (test, m) for test in ("45m", "45q", "45p") for m in H.QPM_MODELS
    }


def test_qpm_recounts_match_their_verdict_files(qpm):
    assert [(t, c["what"]) for t, a in qpm.items() for c in a.checks if not c["match"]] == []
    head = {(t, c["what"]): c["recount"] for t, a in qpm.items() for c in a.checks if c["head"]}
    assert {k: v for k, v in head.items() if k in QPM_HEADLINES} == QPM_HEADLINES


def test_qpm_recounts_flag_a_changed_item(qpm):
    m = copy.deepcopy(qpm["45m · 27B"].pool)
    it = next(x for x in m if x["group"] == "locker-before" and x["rows"]["PM"]["without J++"]["switched"])
    it["rows"]["PM"]["without J++"]["switched"] = 0
    assert not next(c for c in H.x45m_number("qwen3.6-27b", m).checks if c["what"] == "locker-before: gap")["match"]
    q = copy.deepcopy(qpm["45q · Muse"].pool)
    q[0]["rows"]["PP"]["c"]["switched"] = 1 - q[0]["rows"]["PP"]["c"]["switched"]
    assert "c: lookup switched" in [c["what"] for c in H.x45q_number("muse-glimmer-30b", q).checks if not c["match"]]
    p = copy.deepcopy(qpm["45p · 9B"].pool)
    p[0]["rows"]["PM"]["a2"]["switched"] = 1 - p[0]["rows"]["PM"]["a2"]["switched"]
    got = H.x45p_number("qwen3.5-9b", p).checks
    assert not next(c for c in got if c["what"] == "recall: loss_2 − loss_3")["match"]


def test_qpm_samples_are_seed_0_draws_and_reproducible(qpm):
    for a in qpm.values():
        scenes = [it["scene"] for it in a.pool]
        assert scenes == sorted(scenes)
        assert [it["scene"] for it in a.sample] == random.Random(0).sample(scenes, 10)
        assert [it["scene"] for it in H.draw(a.pool)] == [it["scene"] for it in a.sample]
    assert {t: [it["scene"] for it in qpm[t].sample] for t in QPM_DRAWN_9B} == QPM_DRAWN_9B


def test_qpm_marked_positions_agree_with_the_stored_ones_for_every_item(qpm):
    assert [(t, it["scene"], it["bad"]) for t, a in qpm.items() for it in a.pool if it["bad"]] == []
    # 45p: the same marked prompts as the run's own verify pack (examples.md), both readers
    assert all(next(c for c in qpm[f"45p · {m}"].checks if c["what"].startswith("marked prompts"))["match"]
               for m in ("9B", "27B", "Muse"))  # fmt: skip


@pytest.mark.parametrize("tag", ["45m · Muse", "45q · 27B", "45q · Muse", "45p · 9B", "45p · Muse"])
def test_qpm_position_checks_catch_a_moved_position(qpm, tag):
    a = qpm[tag]
    case = a.sample[0]["case"]

    def moved(edit) -> dict:
        c = copy.deepcopy(case)
        edit(c)
        return c

    if tag.startswith("45m"):
        c = moved(lambda c: c.update(pos=c["pos"] + 1))
        assert H.bridge_bad(c, a.model, c["bridge"], c["cf_bridge"], c["pos"])
    elif tag.startswith("45q"):
        assert not H.lockers_found(case, a.model)[1]
        for edit in (lambda c: c.update(pos=c["pos"] - 1),
                     lambda c: c["lockers"]["org"].__setitem__(0, [p + 1 for p in c["lockers"]["org"][0]]),
                     lambda c: c.update(patched=c["patched"][1:]),
                     lambda c: c["marks"]["lockers"][0].__setitem__(0, c["marks"]["lockers"][0][0] + 1)):  # fmt: skip
            assert H.lockers_found(moved(edit), a.model)[1]
    else:
        assert not H.items_found(case, a.model)[1]
        for edit in (lambda c: c.update(pos=c["pos"] + 1),
                     lambda c: c["new"].update(positions=[p - 1 for p in c["new"]["positions"]]),
                     lambda c: c["control"].update(positions=[p + 1 for p in c["control"]["positions"]]),
                     lambda c: c["control"].update(item=c["new"]["item"])):  # fmt: skip
            assert H.items_found(moved(edit), a.model)[1]


def test_qpm_sections_are_generated_with_the_exact_prompts_marked_and_every_answer(qpm):
    text = H.render([], "test", (), list(qpm.values()))
    lines = text.split("\n")
    assert "## 45m, 45q and 45p (UNVERIFIED)" in lines
    for t, a in qpm.items():
        assert f"### {t}. {a.title}" in lines
        assert sum(x.startswith(f"##### {t} ") for x in lines) == H.N_SHOW == 10
        test = t.split(" · ")[0]
        for it in a.sample:
            card = a.card(it)
            o = next(card[i + 1] for i, x in enumerate(card) if x == "```text")
            c = it["case"]
            plain = re.sub(r"⟦(bridge|locker|new|control):", "", o).replace("⟧", "").removesuffix(H.SPACE)
            assert plain == C.tokenizer(a.model).decode(c["readers"]["PP"]["ids"]["org"], skip_special_tokens=False)
            assert re.findall(r"⟦bridge:([^⟧]*)⟧", o) == [it["bridge"]]
            assert len(re.findall("⟦", o)) == 1 + (len(c["lockers"]["sentences"]) if test == "45q" else 0) + (
                2 if test == "45p" else 0)  # fmt: skip
            if test == "45q":
                # a sentence's last token can carry the newline too (Muse's ".\n"): the mark closes after it
                assert [x.strip() for x in re.findall(r"⟦locker:([^⟧]*)⟧", o)] == c["lockers"]["sentences"]
            if test == "45p":
                assert re.findall(r"⟦new:([^⟧]*)⟧", o) == [c["new"]["item"]]
                assert re.findall(r"⟦control:([^⟧]*)⟧", o) == [c["control"]["item"]]
            assert any(x.startswith("S (both readers' prompts): O with these tokens changed") for x in card)
            assert any(x.startswith("Positions, stored vs re-derived") and x.endswith("**agree**.") for x in card)
            answers = [x for x in card if x.startswith(("| lookup |", "| recall |"))]
            assert len(answers) == 2 * QPM_ARMS[test] and not any("not stored" in x for x in answers)
