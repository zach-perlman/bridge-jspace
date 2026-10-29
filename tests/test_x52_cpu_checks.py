from scripts import x52_cpu_checks as C


def test_lens_class_orders_answers_before_names_and_words():
    names = ("lithium", "helium")
    assert C.lens_class({"role": "A"}, "4", names) == "original"
    assert C.lens_class({"role": "b"}, "2", names) == "new"
    assert C.lens_class({"role": "other"}, " 7", names) == "digit"
    assert C.lens_class({"role": "other"}, " lith", names) == "entity"
    assert C.lens_class({"role": "other"}, "He", names) == "entity"
    assert C.lens_class({"role": "other"}, " Four", names) == "number_word"
    assert C.lens_class({"role": "other"}, "<|im_end|>", names) == "other"
    assert C.lens_class({"role": "other"}, "h", names) == "other"  # one letter is not a name


def test_swap_class_reads_the_swapped_in_and_third_items_legs():
    tok_id = lambda d: 100 + d  # noqa: E731
    legs = [4, 2, 6]  # slots 0, 1, 2; j = 0 is the original item, k = 1 the swapped-in one
    row = {"j": 0, "k": 1, "changed": 1}
    assert C.swap_class({**row, "changed": 0, "top": 104}, tok_id, legs) == "unchanged"
    assert C.swap_class({**row, "top": 102}, tok_id, legs) == "swapped_in"
    assert C.swap_class({**row, "top": 106}, tok_id, legs) == "third"
    assert C.swap_class({**row, "top": 109}, tok_id, legs) == "digit"
    assert C.swap_class({**row, "top": 5}, tok_id, legs) == "non_answer"


def test_shares_handle_an_empty_group():
    assert C.shares([], C.SWAP_CLASSES[1:])["swapped_in"] is None
    assert C.shares(["swapped_in", "third"], C.SWAP_CLASSES[1:])["third"] == 0.5
