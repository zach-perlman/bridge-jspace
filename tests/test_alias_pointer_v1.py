"""alias_pointer_v1's generator: predictions, collision policy, conditions paired by scene (only the statements'
language differs), determinism, spans, token alignment (with the cached Qwen3.6-27B tokenizer), the competence judge."""

import collections
import copy

import pytest

from scripts import alias_pointer_v1 as A
from scripts import suite_v1 as S

LEVELS = ((3, 0), (5, 0), (5, 4))
CELLS = [(d, n_ent, n_fill) for d in A.DOMAINS for n_ent, n_fill in LEVELS]


def cell(domain: str, n_ent: int, n_fill: int, n: int = 40, seed: int = 123) -> dict[str, dict[str, list[dict]]]:
    return A.generate_cell(seed, domain, f"e{n_ent}f{n_fill}", n_ent, n_fill, n, tag="t")


def items_of(cells: dict[str, dict[str, list[dict]]]) -> list[dict]:
    return [it for fams in cells.values() for its in fams.values() for it in its]


@pytest.fixture(scope="module")
def tok():
    try:
        return A.tokenizer()
    except Exception:
        pytest.skip("Qwen3.6-27B tokenizer not cached")


@pytest.mark.parametrize(("domain", "n_ent", "n_fill"), CELLS)
def test_predictions_distinct_and_correct(domain, n_ent, n_fill):
    for it in items_of(cell(domain, n_ent, n_fill)):
        sl, d = it["slots"], it["sources"]["dissoc"]
        look = dict(zip(it["entities"], it["digits"], strict=True))
        q_s, p = d["query"], it["entities"][sl["position"]]
        assert it["entities"][sl["query"]] == it["query"]
        assert it["entities"][sl["identity"]] == q_s
        assert d["entities"][sl["position"]] == q_s  # the source queries slot k, where the base has p
        assert len({sl["query"], sl["identity"], sl["position"]}) == 3
        pd = d["predictions"]
        if it["family"] == "RR":
            assert pd["none"] != pd["identity"]
            assert pd["value"] == pd["identity"]
            assert pd["position"] == str(A.rec(domain, p))
        else:
            assert len(set(pd.values())) == 4
            assert pd == {"none": str(look[it["query"]]), "identity": str(look[q_s]), "position": str(look[p]),
                          "value": d["answer"]}  # fmt: skip
            assert int(pd["value"]) not in it["digits"]  # the value is absent from the base context
        assert set(it["sources"]["same"]["predictions"].values()) == {it["answer"]}


@pytest.mark.parametrize(("domain", "n_ent", "n_fill"), CELLS)
def test_collision_policy(domain, n_ent, n_fill):
    for it in items_of(cell(domain, n_ent, n_fill)):
        d = it["sources"]["dissoc"]
        critical = {A.rec(domain, e) for e in (it["query"], d["query"], it["entities"][it["slots"]["position"]])}
        assert not set(it["digits"]) & critical  # hard: always
        assert not set(d["digits"]) & critical
        if it["digit_policy"] == "soft":
            assert not set(it["digits"]) & set(it["recalled"].values())


@pytest.mark.parametrize(("domain", "n_ent"), [(d, n) for d in A.DOMAINS for n in (3, 5)])
def test_slots_balanced(domain, n_ent):
    n_pairs = n_ent * (n_ent - 1)
    cells = cell(domain, n_ent, 0, n=3 * n_pairs)
    for c in A.DOMAINS[domain]["conditions"]:
        for key in ("query", "position"):
            counts = collections.Counter(it["slots"][key] for it in cells[c]["RL"])
            assert set(counts.values()) == {3 * (n_ent - 1)}, (c, key, counts)


@pytest.mark.parametrize(("domain", "n_ent", "n_fill"), CELLS)
def test_conditions_differ_only_in_the_statements(domain, n_ent, n_fill):
    cells = cell(domain, n_ent, n_fill, n=20)
    conds = A.DOMAINS[domain]["conditions"]
    assert tuple(cells) == conds
    for fam in A.FAMILIES:
        for its in zip(*(cells[c][fam] for c in conds), strict=True):
            ref = A.without_surface(its[0])
            for it, c in zip(its, conds, strict=True):
                assert it["condition"] == c
                assert A.without_surface(it) == ref  # entities, digits, order, questions, answers, predictions
                assert it["level"] == f"e{n_ent}f{n_fill}" + A.SUFFIX[c]
                for x in (it, *it["sources"].values()):  # every statement is the condition's, with the same digit
                    want = [A.statement(domain, c, e, dg) for e, dg in zip(x["entities"], x["digits"], strict=True)]
                    assert x["statements"] == want
            eng, alt = its
            assert eng["context"] != alt["context"]
            fill = [s for s in eng["context"].split(". ") if s.rstrip(".") + "." in S.FILLER]
            for f in fill:  # filler stays English and in place
                assert f in alt["context"]
            for e in eng["entities"]:
                assert alt["surface"][e] != e
                assert eng["surface"][e] == e
    paired = A.paired_conditions(items_of(cells))
    assert paired["groups"] == paired["complete"] == paired["identical_but_statements"] == paired["statements_differ"]


def test_xlang_templates_and_symbols():
    it = cell("animals", 5, 0, n=5)["xlang"]["RL"][0]
    for e, s in zip(it["entities"], it["statements"], strict=True):
        lang, art, w = A.XLANG[e]
        assert it["language"][e] == lang
        assert s.startswith(f"{art} {w} ")
        assert " locker " not in s  # the whole statement is translated
    el = cell("elements", 5, 0, n=5)["syn"]["DL"][0]
    for e, s in zip(el["entities"], el["statements"], strict=True):
        assert s == f"The {A.SYMBOLS[e]} card is in locker {el['digits'][el['entities'].index(e)]}."
    assert el["question"] == f"Which locker holds the {el['query']} card?"  # the question names it in English
    sym = A.SYMBOLS[el["query"]]
    assert el["alias"] == {"question": f"What is the name of the element with the chemical symbol {sym}?",
                           "answer": el["query"], "kind": "elements"}  # fmt: skip
    lang, _, w = A.XLANG[it["query"]]
    assert it["alias"]["question"] == f"Which animal is called « {w} » in {A.LANG_NAME[lang]}? Answer in English."


def test_deterministic():
    assert cell("animals", 5, 4) == cell("animals", 5, 4)
    assert cell("elements", 5, 0, n=10, seed=1) != cell("elements", 5, 0, n=10, seed=2)


@pytest.mark.parametrize(("domain", "n_ent", "n_fill"), CELLS)
def test_spans_in_the_user_turn(domain, n_ent, n_fill):
    for it in items_of(cell(domain, n_ent, n_fill, n=10)):
        for x in (it, *it["sources"].values()):
            turn = A.user_turn(x["context"], x["question"])
            sp = x["spans"]
            assert [turn[s:e] for s, e in sp["statements"]] == x["statements"]
            assert all(turn[s:e] in S.FILLER for s, e in sp["filler"])
            assert len(sp["filler"]) == n_fill
            assert turn[slice(*sp["question"])] == x["question"]
            assert turn[sp["tail"][0] :] == " " + A.INSTRUCTION
            assert sp["tail"][1] == len(turn)


def test_token_alignment_and_spans_decode(tok):
    A.check_pools(tok)
    for domain in A.DOMAINS:
        for n_ent, n_fill in LEVELS:
            for it in items_of(cell(domain, n_ent, n_fill, n=6)):
                got = A.check_item(tok, it)
                bad = [k for k, v in got.items() if not v and k not in ("soft_collision_free", "soft_promised")]
                assert not bad, (it["id"], bad)


def test_checks_catch_breakage(tok):
    """Negative controls: a source statement of another length breaks alignment; a shifted span stops decoding."""
    it = cell("animals", 5, 0, n=3)["xlang"]["RL"][0]
    broken = copy.deepcopy(it)
    d = broken["sources"]["dissoc"]
    longer = d["statements"][0].replace(" a le casier", " a le grand casier").replace(" tiene la", " tiene la gran")
    longer = longer.replace(" hat den", " hat den großen")
    d["context"] = d["context"].replace(d["statements"][0], longer, 1)
    d["statements"][0] = longer
    assert longer != it["sources"]["dissoc"]["statements"][0]
    got = A.check_item(tok, broken)
    assert not got["dissoc_aligned"]
    assert not got["statements_text"]
    shifted = copy.deepcopy(it)
    shifted["spans"]["statements"][2] = [s + 1 for s in shifted["spans"]["statements"][2]]
    assert not A.check_item(tok, shifted)["spans_decode"]


def test_rendered_spans(tok):
    it = cell("animals", 5, 4, n=3)["xlang"]["DL"][1]
    text, rs = A.rendered_spans(tok, it["context"], it["question"], it["spans"])
    assert text == S.render(tok, it["context"], it["question"])
    assert [text[s:e] for s, e in rs["statements"]] == it["statements"]
    assert text[slice(*rs["question"])] == it["question"]
    assert rs["tail"][1] == len(text)
    assert text[rs["tail"][0] :].startswith(" " + A.INSTRUCTION)


def test_judge():
    aliases = {"Kuh": "cow", "perro": "dog", "O": "oxygen"}
    assert A.said(" cow", "animals", aliases) == "cow"
    assert A.said(" Kuh", "animals", aliases) is None  # the alias step wants the English name
    assert A.said(" Kuh", "animals+alias", aliases) == "cow"
    assert A.said("\n\nOxygen.", "elements", aliases) == "oxygen"
    assert A.said(" O", "elements+alias", aliases) == "oxygen"
    assert A.said(" o", "elements+alias", aliases) is None  # symbols match case-sensitively
    assert A.said(" 7", "digit", aliases) == "7"
    assert A.said(" seven", "digit", aliases) == "7"


def test_item_prompts():
    cells = cell("animals", 5, 0, n=2)
    rl, dl, rr = (cells["xlang"][f][0] for f in A.FAMILIES)
    assert set(A.item_prompts(rl)) == {"clean", "src_dissoc", "src_same", "src_redigit", "hop1", "hop2", "alias"}
    assert set(A.item_prompts(dl)) == {"clean", "src_dissoc", "src_same", "src_redigit", "alias"}
    assert "alias" not in A.item_prompts(rr)
    assert A.item_prompts(rl)["hop1"][3] == "animals+alias"
    assert A.item_prompts(rl)["alias"][3] == "animals"
    assert "alias" not in A.item_prompts(cells["same"]["RL"][0])


def test_level_names():
    assert A.level_name("e5f0") == "5 statements in English"
    assert A.level_name("e5f0-xlang") == "5 statements in French/Spanish/German"
    assert A.level_name("e3f0-syn") == "3 statements with the chemical symbol"
