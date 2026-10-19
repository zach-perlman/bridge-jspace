"""Part B's prompts in the target's chat template, the format its runs use from 2026-10-19 (README, Decisions): one user
turn, thinking off, the assistant turn prefilled "Answer:" (brew's format since exp03). exp20 measured the model's
competence in it: every exp09 item answered, B1's questions 86%.

A raw-text prompt is a statement to complete. In the chat template it becomes, after the same context:
  question  "... The capital of the country where Lyon is located is" -> "... What is the capital of the country where
            Lyon is located? Answer with a single word and nothing else." (exp09's families)
  blank     "Fact: The language spoken in the country where the Amazon River ends is" -> "Fill in the blank. Answer
            with only the missing word or words and nothing else.\\n\\nThe language spoken in the country where the
            Amazon River ends is ___" (B1's questions and exp01's entity prompts, whose endings are too varied for a
            question: "is called a", "border with", "the rider's")
These are exp20's chat_prefill renderings, character for character.
"""

import re

PREFILL = "Answer:"
QUESTION_INSTRUCTION = "Answer with a single word and nothing else."
BLANK_INSTRUCTION = "Fill in the blank. Answer with only the missing word or words and nothing else."
FORMATS = ("raw", "chat_prefill")


def chat_text(tokenizer, content: str) -> str:
    """One user turn in the target's chat template, thinking off, the assistant turn prefilled with PREFILL."""
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": content}], tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    return text + PREFILL


def lower_the(s: str) -> str:
    return "the" + s[3:] if s.startswith("The ") else s


def as_question(statement: str) -> str:
    """A statement to complete as a question: 'The capital of X is' -> 'What is the capital of X?'."""
    s = statement.strip().removeprefix("Fact: ")
    if m := re.fullmatch(r"(.*) is located in", s):
        return f"In which country is {m[1]} located?"
    if m := re.fullmatch(r"(.*) lives in", s):
        return f"In which country does {m[1]} live?"
    if m := re.fullmatch(r"The city where (.*) stands is", s):
        return f"In which city does {lower_the(m[1])} stand?"
    if m := re.fullmatch(r"(.*) has the colour", s):
        return f"What colour does {lower_the(m[1])} have?"
    m = re.fullmatch(r"(.*) (is|was)(?: the)?", s)
    assert m, f"no question form for {statement!r}"
    return f"What {m[2]} {lower_the(m[1])}?"


def split_context(text: str) -> tuple[str, str]:
    """(context, the statement to complete): the statement is the text after the last sentence end."""
    cut = text.rfind(". ")
    return ("", text) if cut < 0 else (text[: cut + 1], text[cut + 2 :])


def question_content(text: str) -> str:
    """The user turn for a context plus a statement to complete (exp09's families)."""
    context, statement = split_context(text)
    return f"{context} {as_question(statement)}".strip() + " " + QUESTION_INSTRUCTION


def blank_content(statement: str) -> str:
    """The user turn for a statement to complete with no context (B1's questions, exp01's entity prompts)."""
    return f"{BLANK_INSTRUCTION}\n\n{statement.strip().removeprefix('Fact: ')} ___"


def question_span(rendered: str, cue: str, clause: str) -> tuple[int, int, int]:
    """In a rendered exp09 prompt: (start of the question, start of the cue word, end of the cue phrase). The cue
    phrase is the cue word and its clause (" is located", " lives": "Lyon is located", "Emma lives"), as the raw
    prompts' ran to the final " is"; the question starts after the last sentence end before it."""
    cue_start = rendered.rindex(cue + clause)
    return rendered.rindex(". ", 0, cue_start) + 2, cue_start, cue_start + len(cue) + len(clause)
