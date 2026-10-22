"""attn_knockout's tasks_v2 adapter (D2 on Zach's generator): facts and statement spans from the context (no model),
and cases on freshly generated prose and table scenes, with C and O (scene_facts stored) and without (Greek letters
from a cue: facts read back from the context); the target's tokenizer, skipped when it is not cached."""

import random

import pytest

from scripts import attn_knockout as AK
from scripts import tasks_v2 as T

FACTS = {"pick": {"Clara": "eagle", "Ivy": "cat"}, "locker": {"eagle": 3, "cat": 6}}


def _item(fmt: str, numbers: str, context: str, facts: dict | None = None) -> dict:
    out = {"id": "PP-L0-0000", "word": "PP", "domain": "animals", "format": fmt, "numbers": numbers, "context": context}
    return out | ({"scene_facts": {**facts, "pairs": []}} if facts else {})


PROSE = "The locker of the eagle is three. Ivy picked the cat. Clara picked the eagle. The locker of the cat is six."
TABLE = ("Table picks:\n| name | pick |\n|---|---|\n| Ivy | cat |\n| Clara | eagle |\n\n"
         "Table lockers:\n| item | locker |\n|---|---|\n| eagle | 3 |\n| cat | 6 |")  # fmt: skip
JSON = ('Tool output from get_lockers:\n[{"item": "eagle", "locker": "three"}, {"item": "cat", "locker": "six"}]\n'
        'Tool output from get_picks:\n[{"name": "Ivy", "pick": "cat"}, {"name": "Clara", "pick": "eagle"}]')  # fmt: skip
JSON_DIGITS = JSON.replace('"three"', "3").replace('"six"', "6")
PICK = {"prose": "Clara picked the eagle.", "table": "| Clara | eagle |", "json": '{"name": "Clara", "pick": "eagle"}'}


@pytest.mark.parametrize(("fmt", "numbers", "ctx", "eagle", "value"), [
    ("prose", "words", PROSE, "The locker of the eagle is three.", "three"),
    ("table", "digits", TABLE, "| eagle | 3 |", "3"),
    ("json", "words", JSON, '{"item": "eagle", "locker": "three"}', "three"),
    ("json", "digits", JSON_DIGITS, '{"item": "eagle", "locker": 3}', "3"),
])  # fmt: skip
@pytest.mark.parametrize("stored", [True, False])
def test_tasks_spans_locate_statements_and_parts(fmt, numbers, ctx, eagle, value, stored):
    item = _item(fmt, numbers, ctx, FACTS if stored else None)
    assert AK.tasks_facts(item) == FACTS
    sp = AK.tasks_spans(item)
    got = sp["locker"]["eagle"]
    assert ctx[slice(*got["span"])] == eagle
    assert ctx[slice(*got["name"])] == "eagle"
    assert ctx[slice(*got["value"])] == value
    assert ctx[slice(*sp["pick"]["Clara"]["span"])] == PICK[fmt]


def test_tasks_spans_refuse_what_they_cannot_locate():
    with pytest.raises(AssertionError):  # the facts say 3, the context writes three
        AK.tasks_spans(_item("prose", "digits", PROSE, FACTS))
    with pytest.raises(AssertionError):  # the facts say 3, the tool output writes "three"
        AK.tasks_spans(_item("json", "digits", JSON, FACTS))
    with pytest.raises(AssertionError):
        AK.tasks_spans(_item("code", "digits", TABLE, FACTS))
    with pytest.raises(AssertionError):  # a thing outside the topic
        AK.tasks_facts(_item("prose", "words", PROSE.replace("eagle", "Mars")))


@pytest.fixture(scope="module")
def tok():
    from bridge_jspace.tokens import load_tokenizer

    try:
        return load_tokenizer()
    except Exception:
        pytest.skip("target tokenizer not cached")


def _scenes(tok, groups, domains, counterfactuals: bool) -> tuple[list[list[dict]], set]:
    out, cells = [], set()
    for group, words in groups:
        for domain in domains:
            for fmt in AK.TASKS_FORMATS:
                rng, got = random.Random(f"{group}{domain}{fmt}{counterfactuals}"), 0
                for _ in range(300):
                    its = T.make_scene(rng, group, words, domain, fmt, T.LEVELS[0], list(T.DOMAINS),
                                       tok if counterfactuals else None)  # fmt: skip
                    if its is None:
                        continue
                    for it in its:
                        it.update({"id": f"{it['word']}-{domain}-{fmt}-{got}", "scene": f"{group}-{domain}-{fmt}-{got}",
                                   "level": 0})  # fmt: skip
                    out.append(its)
                    cells.add((group, fmt))
                    got += 1
                    if got == 2:
                        break
    return out, cells


@pytest.fixture(scope="module")
def scenes(tok):
    """Up to two scenes per (group, topic, format) at level 0 with C and O, as tasks_v2.make makes them (Greek letters
    from a cue have none: too few single-token letters with a cue of the same length for C); and Greek memory-started
    scenes without C and O (Dan, 2026-10-22: option (a), D2 only)."""
    groups = (("P", ["PP", "PM"]), ("M", ["MP", "MM"]))
    cf, cells = _scenes(tok, groups, ("animals", "planets", "elements", "greek"), True)
    assert cells == {(g, f) for g in "PM" for f in AK.TASKS_FORMATS}, cells
    greek, cells = _scenes(tok, groups[1:], ("greek",), False)
    assert cells == {("M", f) for f in AK.TASKS_FORMATS}, cells
    assert all("scene_facts" not in it for its in greek for it in its)
    return cf + greek


def test_tasks_facts_read_back_equal_the_stored_ones(scenes):
    for its in scenes:
        for it in its:
            if "scene_facts" in it:
                bare = {k: v for k, v in it.items() if k != "scene_facts"}
                assert AK.tasks_facts(bare) == AK.tasks_facts(it), it["id"]


def test_tasks_cases_decode_to_their_statements(tok, scenes):
    for its in scenes:
        for it in its:
            c = AK.tasks_case(it, tok)
            src, x, facts = c["sources"], it["steps"][0]["answer"], AK.tasks_facts(it)

            def dec(key: str, src=src, c=c) -> str:
                return tok.decode([c["ids"][i] for i in src[key]]).strip()

            n = facts["locker"][x]
            value = str(n) if it["numbers"] == "digits" else T.NUMBER_WORDS[n]
            assert c["bridge"] == x
            # a statement's last token may carry the separator after it (json: '"},'), never more
            assert dec("lookup").rstrip(",]\n|") == c["source_text"]["lookup"].rstrip("|"), it["id"]
            assert x in dec("lookup") and dec("lookup").replace(x, "").count(value) == 1
            assert dec("lookup_name") == x
            assert dec("lookup_digit") == value
            for key in ("lookup", "lookup_off"):
                assert sorted(src[f"{key}_nodigit"] + src[f"{key}_digit"]) == src[key]
                assert sorted(src[f"{key}_noname"] + src[f"{key}_name"]) == src[key]
            assert c["source_text"]["lookup_off_name"] != x  # whole names: eta is inside beta
            if c["source_flags"]["lookup_off"] == "same_length":
                assert len(src["lookup_off"]) == len(src["lookup"])
            if it["word"][0] == "P":
                person = it["start_desc"].removesuffix("'s pick")
                assert person in dec("binding").split(x)[0]
                assert x in dec("binding") and person not in c["source_text"]["binding_off"]
            else:
                assert "binding" not in src
            question = set(c["dests"]["question"])
            assert all(max(v) < min(question) for v in src.values())
            assert set(c["dests"]["cue"]) <= question
            others = [t for t in facts["locker"] if t != x]
            if it["word"][1] == "P":  # another thing's locker
                expected = {str(facts["locker"][t]) for t in others}
            else:  # another thing's number
                expected = {str(T.DOMAINS[it["domain"]].values[t]) for t in others}
            assert set(c["conf_answers"]) == expected - {it["answer"]}


def test_tasks_scene_words_hide_the_same_statements(tok, scenes):
    """A scene's two words (PP and PM, or MP and MM) read one context: the same statements are hidden in both."""
    for its in scenes:
        a, b = (AK.tasks_case(it, tok) for it in its)
        for key in ("lookup", "lookup_off", "lookup_name", "lookup_digit", "binding", "binding_off"):
            assert a["sources"].get(key) == b["sources"].get(key), (a["id"], key)
            if key in a["sources"]:
                assert [a["ids"][i] for i in a["sources"][key]] == [b["ids"][i] for i in b["sources"][key]]


def test_tasks_families_sit_in_the_suite_places():
    for word, suite in zip(AK.TASKS_FAMILIES, ("RL", "RR", "BL", "BR"), strict=True):
        assert AK.PATH[word] == AK.PATH[suite]
        assert AK.SWEEP[word] == AK.SWEEP[suite]
