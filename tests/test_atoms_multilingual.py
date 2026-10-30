"""scripts/atoms_multilingual.py: number words in eleven languages, Roman numerals, ordinals and digits match as the reader's answer or
as another number, leading punctuation and spaces stripped (Dan's hand-check, 30 Oct: '，三', ' oito')."""

from __future__ import annotations

import pytest

from scripts import atoms_multilingual as M


def langs(token: str) -> set[tuple[int, str]]:
    return {(v, lang) for v, lang, _ in M.numbers_of(token)}


@pytest.mark.parametrize(("token", "want"), [
    ("，三", (3, "Chinese / Japanese")), (" oito", (8, "Portuguese")), ("三", (3, "Chinese / Japanese")), (" Third", (3, "English")),
    ("3rd", (3, "English")), ("третій", (3, "Ukrainian")), (" cinq", (5, "French")), ("(sechs", (6, "German")), ("さん", (3, "Japanese")),
    ("셋", (3, "Korean")), (" dieci", (10, "Italian")), (" diez", (10, "Spanish")), ("пять", (5, "Russian")), ("-IV", (4, "Roman numeral")),
    ("第三", (3, "Chinese / Japanese")), (" 7", (7, "digit")), ("，８", (8, "digit")),
])  # fmt: skip
def test_tokens_read_as_numbers(token, want):
    assert want in langs(token), (token, langs(token))


@pytest.mark.parametrize("token", ["I", " V", "X", "Gamma", "，", " the", "三十三个", "11", "0"])
def test_non_numbers_and_lone_roman_letters_are_not_numbers(token):
    assert not M.numbers_of(token), token


def test_the_answer_class_is_the_readers_original_or_changed_answer():
    atom = {"token": "，三", "class": "other", "coef": -18.5, "share": 0.013}
    assert M.classify(atom, (3, 7))[0] == "answer_any" and M.classify(atom, (7, 3))[0] == "answer_any"
    assert M.classify(atom, (1, 2))[0] == "number_other"
    assert M.classify({"token": " oito", "class": "other", "coef": 1, "share": 0.007}, (3, 7))[0] == "number_other"
    assert M.classify({"token": " Gamma", "class": "bridge", "coef": 1, "share": 0.02}, (3, 7))[0] == "bridge"  # old classes stay
