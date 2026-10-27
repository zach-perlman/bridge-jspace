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

Prompt format of a run (BJ_FORMAT, 2026-10-21; G1: is a result about the chat template's tokens?): every prompt
builder renders its user content through chat_text, which follows the environment variable BJ_FORMAT:
  chat (default)  the content in the target's chat template, thinking off, the assistant turn prefilled "Answer:"
  raw             the same content as plain text, a newline and "Answer:": no template tokens at all; the target's BOS,
                  if it needs one, comes from tokens.raw_encoding as for any raw text
The format is recorded in every manifest (pins.model_pin()['prompt_format']) and raw runs carry "_raw" in their names
(pins.check_run_name). Not to be confused with FORMATS below: exp09's item formats, where "raw" is a statement to
complete ("The capital of ... is"), not a question.
"""

import os
import re

PREFILL = "Answer:"
QUESTION_INSTRUCTION = "Answer with a single word and nothing else."
BLANK_INSTRUCTION = "Fill in the blank. Answer with only the missing word or words and nothing else."
FORMATS = ("raw", "chat_prefill")  # exp09's item formats (see the docstring)
PROMPT_FORMATS = ("chat", "raw")
FORMAT = os.environ.get("BJ_FORMAT", "chat")
assert FORMAT in PROMPT_FORMATS, f"BJ_FORMAT={FORMAT!r}: one of {PROMPT_FORMATS}"


def template_text(tokenizer, content: str) -> str:
    """One user turn in the target's chat template, thinking off, the assistant turn prefilled with PREFILL."""
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": content}], tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    return text + PREFILL


def raw_text(content: str) -> str:
    """The same user content as plain text, a newline and PREFILL (no template)."""
    return f"{content}\n{PREFILL}"


def chat_text(tokenizer, content: str, fmt: str | None = None) -> str:
    """One user turn as the run's prompt format renders it (`fmt`, default BJ_FORMAT): the chat template prefilled
    with PREFILL (chat) or the plain content, a newline and PREFILL (raw)."""
    fmt = fmt or FORMAT
    assert fmt in PROMPT_FORMATS, f"prompt format {fmt!r}: one of {PROMPT_FORMATS}"
    return template_text(tokenizer, content) if fmt == "chat" else raw_text(content)


def format_note(fmt: str | None = None) -> str:
    """The prompt format in words, for manifests."""
    if (fmt or FORMAT) == "chat":
        return f"chat template, thinking off, '{PREFILL}' prefilled (BJ_FORMAT=chat)"
    return f"raw text: the user content, a newline and '{PREFILL}', no template (BJ_FORMAT=raw)"


def manifest_format(manifest: dict) -> str:
    """The prompt format a manifest was written in (older manifests: chat)."""
    return manifest.get("model", {}).get("prompt_format", "chat")


def check_format(manifest: dict) -> None:
    """A stage that renders prompts for an existing manifest (run, competence) runs in the manifest's format."""
    want = manifest_format(manifest)
    assert want == FORMAT, f"this run's manifest is in {want} format; set BJ_FORMAT={want} (now {FORMAT})"


def content_end(rendered: str, start: int = 0) -> int:
    """Where the user content ends in a rendered question prompt (its last words are QUESTION_INSTRUCTION in both
    formats): the template's turn end (chat) or the newline before PREFILL (raw) begins there."""
    i = rendered.index(QUESTION_INSTRUCTION, start)
    return i + len(QUESTION_INSTRUCTION)


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
