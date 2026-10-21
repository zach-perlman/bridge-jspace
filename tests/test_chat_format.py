"""chat.py's prompt-format switch (BJ_FORMAT: chat or raw), its manifest record and run-name rule, and that the
position code (pointer_swap's groups, attn_knockout's question/final split) finds the same parts in raw text."""

import importlib

import pytest

from bridge_jspace import chat, pins

CONTENT = "The cat's locker is 4. The dog's locker is 7.\nWhich locker belongs to the dog? " + chat.QUESTION_INSTRUCTION


class FakeTok:
    def apply_chat_template(self, messages, tokenize, add_generation_prompt, enable_thinking):
        return f"<|im_start|>user\n{messages[0]['content']}<|im_end|>\n<|im_start|>assistant\n"


def test_raw_is_the_content_a_newline_and_answer():
    assert chat.chat_text(FakeTok(), CONTENT, fmt="raw") == CONTENT + "\nAnswer:"
    assert chat.raw_text(CONTENT).endswith("\nAnswer:")
    assert "<|im_start|>" not in chat.chat_text(FakeTok(), CONTENT, fmt="raw")


def test_chat_is_the_template_prefilled():
    out = chat.chat_text(FakeTok(), CONTENT, fmt="chat")
    assert out == FakeTok().apply_chat_template([{"content": CONTENT}], False, True, False) + "Answer:"
    with pytest.raises(AssertionError):
        chat.chat_text(FakeTok(), CONTENT, fmt="chat_prefill")  # exp09's item format is not a prompt format


def test_env_variable_switches_the_default(monkeypatch):
    try:
        monkeypatch.setenv("BJ_FORMAT", "raw")
        importlib.reload(chat)
        assert chat.FORMAT == "raw"
        assert chat.chat_text(FakeTok(), CONTENT) == CONTENT + "\nAnswer:"
        assert "raw text" in chat.format_note()
        monkeypatch.setenv("BJ_FORMAT", "plain")
        with pytest.raises(AssertionError):
            importlib.reload(chat)
    finally:
        monkeypatch.delenv("BJ_FORMAT", raising=False)
        importlib.reload(chat)
    assert chat.FORMAT == "chat"


def test_manifest_records_the_format_and_run_names_say_raw(monkeypatch):
    assert pins.model_pin()["prompt_format"] == "chat"
    pins.check_run_name("d3v4_swap_main")
    with pytest.raises(AssertionError):
        pins.check_run_name("d3v4_swap_raw_main")  # a chat run must not look like a raw one
    monkeypatch.setattr(chat, "FORMAT", "raw")
    assert pins.model_pin()["prompt_format"] == "raw"
    pins.check_run_name("d3v4_swap_raw_main")
    with pytest.raises(AssertionError):
        pins.check_run_name("d3v4_swap_main")


def test_a_stage_runs_in_its_manifests_format(monkeypatch):
    chat.check_format({"model": {"prompt_format": "chat"}})
    chat.check_format({"model": {"target": "qwen3.6-27b"}})  # older manifests: chat
    with pytest.raises(AssertionError):
        chat.check_format({"model": {"prompt_format": "raw"}})
    monkeypatch.setattr(chat, "FORMAT", "raw")
    chat.check_format({"model": pins.model_pin()})


def test_content_end_in_both_formats():
    for fmt in chat.PROMPT_FORMATS:
        text = chat.chat_text(FakeTok(), CONTENT, fmt=fmt)
        end = chat.content_end(text, text.index("Which"))
        assert text[:end].endswith(chat.QUESTION_INSTRUCTION)
        assert text[end:] == ("\nAnswer:" if fmt == "raw" else "<|im_end|>\n<|im_start|>assistant\nAnswer:")


@pytest.fixture(scope="module")
def tok():
    from scripts import pointer_v1 as PV

    try:
        return PV.tokenizer()
    except Exception:
        pytest.skip("no tokenizer snapshot")


def first_item(path: str) -> dict:
    from scripts import pointer_v1 as PV

    return PV.load_file(pins.REPO_ROOT / path)[0]


def test_raw_judge_reads_digits_and_words(tok, monkeypatch):
    from scripts import pointer_v1 as PV
    from scripts import pointer_v4 as P4

    digit = {"expected": "3", "answer_kind": "digit", "read_top": "3", "continuation": "\n\n<think>\nHere's"}
    assert PV.raw_right(tok, digit)  # the read decides, not the 8 greedy tokens that never reach the answer
    assert not PV.raw_right(tok, digit | {"read_top": "7"})
    word = {
        "expected": "Japan",
        "answer_kind": "word",
        "judge": "countries",
        "read_top": "",
        "continuation_think": "Japan",
    }
    monkeypatch.setattr(PV, "said", P4.said)  # what pointer_v4's competence does
    assert PV.raw_right(tok, word)
    assert not PV.raw_right(tok, word | {"continuation_think": "Greece"})
    assert not PV.raw_right(tok, word | {"continuation_think": "G"})  # a first token alone is not the entity
    assert "raw format" in PV.judge_rule("raw")
    assert "greedy" in PV.judge_rule("chat")
    monkeypatch.setattr(chat, "FORMAT", "raw")
    assert PV.judge_rule() == PV.JUDGE_READ
    monkeypatch.setattr(chat, "FORMAT", "chat")
    monkeypatch.setenv("BJ_JUDGE", "read")  # a target whose greedy reply names the bridge (OLMo-3-7B-Instruct)
    assert PV.judge_mode() == "read" and PV.judge_rule() == PV.JUDGE_READ_CHAT
    monkeypatch.setenv("BJ_JUDGE", "loose")
    with pytest.raises(AssertionError):
        PV.judge_mode()


def test_pointer_swap_groups_in_raw_text(tok, monkeypatch):
    from scripts import pointer_swap as PS

    item = first_item("data/pointer_v4/main/animals_RL_e5f0.json")
    chat_prep = PS.prepare(item, tok)
    monkeypatch.setattr(chat, "FORMAT", "raw")
    prep = PS.prepare(item, tok)  # asserts: sources token-aligned, the same tokens after the question everywhere
    assert prep["text"].endswith(item["question"] + " " + chat.QUESTION_INSTRUCTION + "\nAnswer:")
    assert "<|im_start|>" not in prep["text"]
    ids = prep["read_ids"]["base"]
    assert tok.decode([ids[i] for i in prep["groups"]["question"]]).strip() == item["question"]
    assert tok.decode([ids[i] for i in prep["groups"]["final"]]) == f" {chat.QUESTION_INSTRUCTION}\nAnswer:"
    assert prep["groups"]["last"] == [len(ids) - 2, len(ids) - 1]  # ':' and the read's space, as in chat
    assert tok.decode(ids[-2:]) == ": "
    assert len(chat_prep["groups"]["final"]) > len(prep["groups"]["final"])  # chat adds the template's tokens


def test_attn_knockout_question_and_final_in_raw_text(tok, monkeypatch):
    AK = pytest.importorskip("scripts.attn_knockout")
    item = first_item("data/pointer_v1/main/animals_RL_e5f0.json")
    chat_case = AK.pointer_case(item, tok, "pointer_v1")
    text = chat_case["prompt"]
    assert chat.content_end(text, chat_case["q_start"]) == text.index("<|im_end|>", chat_case["q_start"])  # unchanged
    monkeypatch.setattr(chat, "FORMAT", "raw")
    case = AK.pointer_case(item, tok, "pointer_v1")
    ids, d = case["ids"], case["dests"]
    assert tok.decode([ids[i] for i in d["question"]]).strip() == f"{item['question']} {chat.QUESTION_INSTRUCTION}"
    assert tok.decode([ids[i] for i in d["final"]]) == "\nAnswer: "
    for name in ("lookup", "random"):  # the same statement and same-length span in both formats
        got = tok.decode([ids[i] for i in case["sources"][name]])
        assert got == tok.decode([chat_case["ids"][i] for i in chat_case["sources"][name]]), name
