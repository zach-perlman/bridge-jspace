"""Qwen3.6-27B: loading, raw-text forwards with per-layer residual edits, word ranks, greedy continuations.

Conventions
- "Layer l" is the output of decoder block l (the J-lens's source convention), for l in 0..62.
- Prompts are raw text, no chat template, as in the jlens reference code.
- Word rank: the rank of the best candidate id after formatting tokens (no letter or digit, special and added tokens)
  are removed from the distribution, as in the reference swap runner.
"""

import contextlib
import re
from collections.abc import Callable
from dataclasses import dataclass

import torch
from huggingface_hub import snapshot_download

from . import pins, tokens

# An edit gets the block output at one layer, [seq, d] fp32, and returns the edited residual.
Edit = Callable[[torch.Tensor], torch.Tensor]

_HAS_LETTER_OR_DIGIT = re.compile(r"[^\W_]")
_HAS_LETTER = re.compile(r"[^\W\d_]")


@dataclass
class Model:
    hf: torch.nn.Module
    tokenizer: object
    decoded: list[str]             # decode of every id in the lm_head's vocabulary
    special_ids: frozenset[int]    # special and added tokens
    formatting_mask: torch.Tensor  # [vocab] bool, cuda: True for formatting tokens

    @property
    def layers(self):
        return self.hf.model.layers

    def encode(self, text: str) -> torch.Tensor:
        return torch.tensor([self.tokenizer(text, add_special_tokens=False).input_ids], device="cuda")

    def unembed(self, h: torch.Tensor) -> torch.Tensor:
        """Final norm then lm_head, fp32 logits."""
        return self.hf.lm_head(self.hf.model.norm(h.to(torch.bfloat16))).float()

    def norm_gain(self) -> torch.Tensor:
        """The final RMSNorm's per-dimension gain (Qwen3.5-family norms scale by 1 + weight), fp32."""
        return 1.0 + self.hf.model.norm.weight.float()

    @torch.no_grad()
    def run(self, ids: torch.Tensor, edits: dict[int, Edit] | None = None,
            record: tuple[int, ...] = ()) -> tuple[torch.Tensor, dict[int, torch.Tensor]]:
        """One forward of a single prompt [1, seq]. Returns the final-position logits [vocab] (fp32) and the block
        outputs [seq, d] (fp32, after any edit at that layer) at the `record` layers."""
        edits = edits or {}
        recorded: dict[int, torch.Tensor] = {}

        def hook_for(layer: int):
            def hook(_module, _args, out):
                h = out[0] if isinstance(out, tuple) else out
                if layer in edits:
                    h = edits[layer](h[0].float()).to(h.dtype)[None]
                if layer in record:
                    recorded[layer] = h[0].float().clone()
                if layer not in edits:
                    return None
                return (h,) + tuple(out[1:]) if isinstance(out, tuple) else h
            return hook

        with _forward_hooks([(self.layers[l], hook_for(l)) for l in sorted(set(edits) | set(record))]):
            logits = self.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[0, -1].float()
        return logits, recorded

    @torch.no_grad()
    def greedy_text(self, ids: torch.Tensor, max_new_tokens: int = 8) -> str:
        """Greedy continuation of a short prompt, decoded. Full forwards without a cache: slower, but the same
        forward path as `run`."""
        for _ in range(max_new_tokens):
            next_id = self.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[0, -1].argmax()
            ids = torch.cat([ids, next_id.view(1, 1)], dim=1)
        return self.tokenizer.decode(ids[0, -max_new_tokens:])

    def surface_ids(self, word: str) -> list[int]:
        return tokens.surface_ids(self.tokenizer, word)

    def concept_token(self, concept: str) -> int:
        return tokens.concept_token(self.tokenizer, concept)

    def answer_ids(self, answers: list[str]) -> list[int]:
        """Single-token surface ids of any of several accepted answers."""
        return sorted({i for a in answers for i in self.surface_ids(a)})

    def word_rank(self, logits: torch.Tensor, candidate_ids: list[int]) -> int:
        """1 + the number of other word tokens scoring at least as high as the best candidate (formatting tokens
        removed). Strict, so an exact tie with another word (common in bf16) ranks the candidate 2nd, not 1st."""
        word_logits = logits.masked_fill(self.formatting_mask, float("-inf"))
        best = word_logits[candidate_ids].max()
        word_logits[candidate_ids] = float("-inf")
        return int((word_logits >= best).sum()) + 1

    def top_word(self, logits: torch.Tensor) -> str:
        return self.decoded[int(logits.masked_fill(self.formatting_mask, float("-inf")).argmax())]

    def letter_token_ids(self) -> torch.Tensor:
        """Ids of non-special tokens whose decode contains a letter: the J-lens dictionary for the decomposition."""
        keep = [i for i, s in enumerate(self.decoded) if i not in self.special_ids and _HAS_LETTER.search(s)]
        return torch.tensor(keep, device="cuda")


def load_model() -> Model:
    from transformers import AutoModelForCausalLM
    path = snapshot_download(pins.QWEN_REPO, revision=pins.QWEN_REVISION, local_files_only=True)
    tokenizer = tokens.load_tokenizer()
    hf = AutoModelForCausalLM.from_pretrained(path, dtype=torch.bfloat16, device_map="cuda",
                                              attn_implementation="sdpa").eval()
    vocab = hf.lm_head.weight.shape[0]
    decoded = tokenizer.batch_decode([[i] for i in range(vocab)])
    special = frozenset(tokenizer.all_special_ids) | frozenset(int(i) for i in tokenizer.added_tokens_decoder)
    formatting = [i for i, s in enumerate(decoded) if i in special or not _HAS_LETTER_OR_DIGIT.search(s)]
    mask = torch.zeros(vocab, dtype=torch.bool, device="cuda")
    mask[formatting] = True
    return Model(hf, tokenizer, decoded, special, mask)


@contextlib.contextmanager
def _forward_hooks(pairs):
    handles = [module.register_forward_hook(hook) for module, hook in pairs]
    try:
        yield
    finally:
        for handle in handles:
            handle.remove()
