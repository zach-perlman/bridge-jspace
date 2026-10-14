"""Tokenizer-only helpers shared by the data checks and the model wrapper."""

from huggingface_hub import snapshot_download

from . import pins


def load_tokenizer():
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(
        snapshot_download(pins.QWEN_REPO, revision=pins.QWEN_REVISION, local_files_only=True)
    )


def _single_token(tokenizer, surface: str) -> int | None:
    ids = tokenizer(surface, add_special_tokens=False).input_ids
    return ids[0] if len(ids) == 1 else None


def surface_ids(tokenizer, word: str) -> list[int]:
    """Single-token ids among the word's surfaces (with/without a leading space; as given, capitalised, lowercase),
    as the reference runner scores answers. Multi-token surfaces are skipped, so the list can be empty."""
    ids = {
        _single_token(tokenizer, prefix + form)
        for form in {word, word.capitalize(), word.lower()}
        for prefix in ("", " ")
    }
    return sorted(i for i in ids if i is not None)


def concept_token(tokenizer, concept: str) -> int:
    """The one id whose J-lens vector stands for a concept, as in the reference runner: the first single-token
    surface among ' X', 'X', ' x', 'x' and the capitalised forms (X = the concept as written)."""
    c = concept.strip()
    for surface in (" " + c, c, " " + c.lower(), c.lower(), " " + c.capitalize(), c.capitalize()):
        token = _single_token(tokenizer, surface)
        if token is not None:
            return token
    raise ValueError(f"no single-token surface for {concept!r}")
