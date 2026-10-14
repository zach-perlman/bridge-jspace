"""exp13's answer judging on hand-written continuations."""

from scripts.exp13_greedy_answers.experiment import answer_forms, first_clause, judge


def test_first_clause_cuts_at_sentence_end_not_decimal():
    assert first_clause(" gastric acid. It is strong") == " gastric acid"
    assert first_clause(" 3.5 billion years") == " 3.5 billion years"
    assert first_clause(" Paris\nQuestion:") == "Paris"
    assert first_clause("\n\nEarth.\nFact") == "Earth"  # leading line breaks are skipped, not a cut


def test_criteria_on_known_cases():
    v = judge(" drumsticks.\nQuestion", "sticks", "mallets")
    assert (v["A"], v["B"], v["C"], v["match"]) == (False, False, True, "compound")
    v = judge(" gastric acid, which", "acid", "bile")
    assert (v["A"], v["B"], v["C"], v["match"]) == (False, False, True, "word")
    v = judge(" a gas at room temperature.", "gas", "liquid")
    assert (v["A"], v["B"], v["C"]) == (False, True, True)
    v = judge(" Portuguese.", "Portuguese", "Spanish")
    assert (v["A"], v["B"], v["C"], v["ambiguous"]) == (True, True, True, False)


def test_no_false_compounds_or_short_answers():
    assert judge(" a hundred years", "red", "blue")["C"] is False  # 3-letter answer: no compound rule
    assert judge(" someone else", "one", "two")["C"] is False
    assert judge(" Las Vegas", "gas", "solid")["C"] is False


def test_numbers_and_ambiguity():
    assert judge(" twenty-six letters", "26", "20")["C"] is True
    assert judge(" 4 legs", "four", "eight")["C"] is True
    v = judge(" Spanish or Portuguese", "Portuguese", "Spanish")
    assert v["C"] and v["swap_also"] and v["ambiguous"]
    assert answer_forms("8") == [["8"], ["eight"]]
