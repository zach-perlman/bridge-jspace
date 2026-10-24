"""Part B's target model (pins.TARGET: Qwen3.6-27B by default, or Gemma 4 31B-it): loading, raw-text forwards with
per-layer residual edits, word ranks, greedy continuations.

Conventions
- "Layer l" is the output of decoder block l (the J-lens's source convention), for l in 0..n_layers - 2.
- Prompts are raw text, no chat template, as in the jlens reference code; a target that needs a BOS gets it first
  (tokens.raw_encoding).
- Word rank: the rank of the best candidate id after formatting tokens (no letter or digit, special and added tokens)
  are removed from the distribution, as in the reference swap runner.
- Devices: with BJ_DEVICE_MAP unset the whole model sits on one GPU, as always. With it set (`placement`), accelerate
  splits the decoder blocks over the visible GPUs. Either way the input embedding is on the home device cuda:0
  (`Model.device`; asserted for a split), and every tensor a Model takes or hands out lives there: input ids, logits
  (`run`, `unembed`, the lens's readouts), recorded block outputs, the tensors an edit holds, the lens's vectors. A
  block on another GPU sends its output home for an edit and takes the result back (`OnDevice`); on one device nothing
  moves or is copied. Scripts that hook blocks themselves (not through Model) must do the same.
"""

import contextlib
import os
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import torch
from huggingface_hub import snapshot_download

from . import pins, tokens

# An edit gets the block output at one layer, [seq, d] fp32, and returns the edited residual.
Edit = Callable[[torch.Tensor], torch.Tensor]

DEVICE_MAP_ENV = "BJ_DEVICE_MAP"

_HAS_LETTER_OR_DIGIT = re.compile(r"[^\W_]")
_HAS_LETTER = re.compile(r"[^\W\d_]")


def to_device(x: torch.Tensor, device: torch.device) -> torch.Tensor:
    """x on `device`: x itself, not a copy, when it is there already."""
    return x if x.device == device else x.to(device)


class OnDevice:
    """An edit run on `device`, where its own tensors live, for a block output on any device: the output goes to
    `device`, the edit runs, and its result goes back to the output's device. When the output is already on `device`,
    the edit gets that very tensor and its result is returned as is (no copies)."""

    def __init__(self, edit: Edit, device: torch.device):
        self.edit, self.device = edit, device

    def __call__(self, h: torch.Tensor) -> torch.Tensor:
        return to_device(self.edit(to_device(h, self.device)), h.device)


def placement(spec: str | None) -> dict[str, Any]:
    """from_pretrained's placement arguments for a BJ_DEVICE_MAP value.
    unset or ""         device_map="cuda": the whole model on the current GPU (the default; unchanged)
    "auto"              accelerate's balanced split of the blocks over every visible GPU (load_model caps each GPU at
                        its memory, so nothing is offloaded to the CPU)
    "0:30GiB,1:75GiB"   the same split over the listed GPUs (numbered as CUDA_VISIBLE_DEVICES shows them), each
                        capped at its size; GPU 0 must be listed, as it holds the embedding (the home device)"""
    spec = (spec or "").strip()
    if not spec:
        return {"device_map": "cuda"}
    if spec == "auto":
        return {"device_map": "auto"}
    usage = f"{DEVICE_MAP_ENV}={spec!r}: expected 'auto' or '<gpu>:<size>,...' such as '0:30GiB,1:75GiB'"
    max_memory: dict[int, str] = {}
    for part in spec.split(","):
        gpu, sep, size = (s.strip() for s in part.partition(":"))
        if not (sep and gpu.isdigit() and size):
            raise ValueError(usage)
        if int(gpu) in max_memory:
            raise ValueError(f"{usage}; GPU {gpu} is listed twice")
        max_memory[int(gpu)] = size
    if 0 not in max_memory:
        raise ValueError(f"{usage}; GPU 0 must be listed (the embedding and every tensor a Model hands out live there)")
    return {"device_map": "auto", "max_memory": max_memory}


@dataclass
class Model:
    hf: Any  # transformers' Qwen3_5ForCausalLM or Gemma4ForConditionalGeneration: untyped submodule access
    tokenizer: Any
    decoded: list[str]  # decode of every id in the lm_head's vocabulary
    special_ids: frozenset[int]  # special and added tokens
    formatting_mask: torch.Tensor  # [vocab] bool, home device (cuda:0): True for formatting tokens

    @property
    def text(self):
        """The text decoder (its layers and final norm): hf.model, or a multimodal model's hf.model.language_model."""
        return getattr(self.hf.model, "language_model", self.hf.model)

    @property
    def layers(self):
        return self.text.layers

    @property
    def device(self) -> torch.device:
        """The home device (cuda:0 on the GPU box): the input embedding's (module docstring, Devices)."""
        return self.hf.get_input_embeddings().weight.device

    def homed(self, edits: dict[int, Edit]) -> dict[int, Edit]:
        """Edits whose tensors live on the home device, made safe for blocks on any device (OnDevice)."""
        return {layer: OnDevice(edit, self.device) for layer, edit in edits.items()}

    def encode(self, text: str) -> torch.Tensor:
        return torch.tensor([tokens.raw_encoding(self.tokenizer, text)["input_ids"]], device="cuda")

    def unembed(self, h: torch.Tensor) -> torch.Tensor:
        """Final norm then lm_head, fp32 logits on the home device, softcapped as the model's own (Gemma:
        30 tanh(x / 30); ranks unchanged)."""
        logits = self.hf.lm_head(self.text.norm(h.to(torch.bfloat16))).float()
        cap = getattr(self.hf.config.get_text_config(), "final_logit_softcapping", None)
        return to_device(cap * torch.tanh(logits / cap) if cap else logits, self.device)

    def norm_gain(self) -> torch.Tensor:
        """The final RMSNorm's per-dimension gain, fp32 on the home device: 1 + weight for Qwen3.5-family norms, weight
        for Gemma 4's."""
        weight = to_device(self.text.norm.weight.float(), self.device)
        return 1.0 + weight if pins.TARGETS[pins.TARGET]["norm_gain"] == "one_plus_weight" else weight

    @torch.no_grad()
    def run(
        self, ids: torch.Tensor, edits: dict[int, Edit] | None = None, record: tuple[int, ...] = ()
    ) -> tuple[torch.Tensor, dict[int, torch.Tensor]]:
        """One forward of a single prompt [1, seq]. Returns the final-position logits [vocab] (fp32) and the block
        outputs [seq, d] (fp32, after any edit at that layer) at the `record` layers, all on the home device."""
        home = self.device
        edits = self.homed(edits or {})
        recorded: dict[int, torch.Tensor] = {}

        def hook_for(layer: int):
            def hook(_module, _args, out):
                h = out[0] if isinstance(out, tuple) else out
                if layer in edits:
                    h = edits[layer](h[0].float()).to(h.dtype)[None]
                if layer in record:
                    recorded[layer] = to_device(h[0].float().clone(), home)
                if layer not in edits:
                    return None
                return (h, *out[1:]) if isinstance(out, tuple) else h

            return hook

        with _forward_hooks([(self.layers[layer], hook_for(layer)) for layer in sorted(set(edits) | set(record))]):
            logits = self.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[0, -1].float()
        return to_device(logits, home), recorded

    @torch.no_grad()
    def greedy_text(self, ids: torch.Tensor, max_new_tokens: int = 8) -> str:
        """Greedy continuation of a short prompt, decoded. Full forwards without a cache: slower, but the same
        forward path as `run`."""
        for _ in range(max_new_tokens):
            next_id = self.hf(input_ids=ids, use_cache=False, logits_to_keep=1).logits[0, -1].argmax()
            ids = torch.cat([ids, next_id.view(1, 1)], dim=1)
        return self.tokenizer.decode(ids[0, -max_new_tokens:])

    @torch.no_grad()
    def generate(
        self, ids: torch.Tensor, max_new_tokens: int, edits: dict[int, Edit] | None = None
    ) -> tuple[torch.Tensor, str, int]:
        """Greedy continuation through HF `generate` (as exp13 does), with `edits` applied only to the prompt's own
        forward; generated tokens are not edited. Returns the first step's raw logits [vocab] (fp32), the decoded
        continuation and the number of new tokens."""
        edits = self.homed(edits or {})
        prompt_len = ids.shape[1]

        def hook_for(layer: int):
            def hook(_module, _args, out):
                h = out[0] if isinstance(out, tuple) else out
                if h.shape[1] != prompt_len:  # a decoding step
                    return None
                h = edits[layer](h[0].float()).to(h.dtype)[None]
                return (h, *out[1:]) if isinstance(out, tuple) else h

            return hook

        with _forward_hooks([(self.layers[layer], hook_for(layer)) for layer in sorted(edits)]):
            out = self.hf.generate(
                input_ids=ids,
                attention_mask=torch.ones_like(ids),
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
                output_logits=True,
                return_dict_in_generate=True,
            )
        new = out.sequences[0, prompt_len:]
        return out.logits[0][0].float(), self.tokenizer.decode(new, skip_special_tokens=True), int(new.shape[0])

    @torch.no_grad()
    def generate_batch(
        self,
        ids: torch.Tensor,
        max_new_tokens: int,
        edits: list[dict[int, Edit]],
        first_logits: bool = False,
        steps: bool = False,
    ) -> Any:
        """Greedy continuations under several edit sets at once, one batch row per set (a row without an edit at a layer
        passes through): of one prompt [1, seq], or of as many prompts of one length [len(edits), seq]. Each row is
        `generate(ids[row], max_new_tokens, edits[row])` up to batched-kernel rounding; one batched call pays the
        per-kernel launch cost once instead of once per row, which is what bounds generation speed on this model
        (thousands of small kernels per token). Returns the decoded continuations, and with first_logits also the
        first step's raw logits [len(edits), vocab] (fp32), as `generate` returns them. With steps: (texts, every
        step's raw logits [len(edits), steps, vocab] fp32, the new token ids [len(edits), steps])."""
        edits = [self.homed(row_edits) for row_edits in edits]
        prompt_len = ids.shape[1]

        def hook_for(layer: int):
            def hook(_module, _args, out):
                h = out[0] if isinstance(out, tuple) else out
                if h.shape[1] != prompt_len:  # a decoding step
                    return None
                h = h.clone()
                for row, row_edits in enumerate(edits):
                    if layer in row_edits:
                        h[row] = row_edits[layer](h[row].float()).to(h.dtype)
                return (h, *out[1:]) if isinstance(out, tuple) else h

            return hook

        layers = sorted({layer for row_edits in edits for layer in row_edits})
        batch = ids if ids.shape[0] == len(edits) else ids.expand(len(edits), -1).contiguous()
        with _forward_hooks([(self.layers[layer], hook_for(layer)) for layer in layers]):
            out = self.hf.generate(
                input_ids=batch,
                attention_mask=torch.ones_like(batch),
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id,
                output_logits=first_logits or steps,
                return_dict_in_generate=True,
            )
        texts = [self.tokenizer.decode(seq[prompt_len:], skip_special_tokens=True) for seq in out.sequences]
        if steps:
            return texts, torch.stack(out.logits, dim=1).float(), out.sequences[:, prompt_len:]
        return (texts, out.logits[0].float()) if first_logits else texts

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


def load_model(device_map: str | None = None) -> Model:
    """The pinned target in bf16. `device_map` is a BJ_DEVICE_MAP value (`placement`); None reads BJ_DEVICE_MAP."""
    from transformers import AutoConfig, AutoModelForCausalLM, AutoModelForImageTextToText

    path = snapshot_download(pins.MODEL_REPO, revision=pins.MODEL_REVISION, local_files_only=True)
    tokenizer = tokens.load_tokenizer()
    architectures = AutoConfig.from_pretrained(path).architectures or []
    multimodal = any(a.endswith("ForConditionalGeneration") for a in architectures)
    auto = AutoModelForImageTextToText if multimodal else AutoModelForCausalLM  # Gemma 4: the checkpoint's own class
    where = placement(os.environ.get(DEVICE_MAP_ENV) if device_map is None else device_map)
    if where["device_map"] == "auto" and "max_memory" not in where:  # uncapped, accelerate may offload to the CPU
        gpus = range(torch.cuda.device_count())
        where["max_memory"] = {i: torch.cuda.get_device_properties(i).total_memory for i in gpus}
    hf = auto.from_pretrained(path, dtype=torch.bfloat16, attn_implementation="sdpa", **where).eval()
    split = sorted({str(d) for d in getattr(hf, "hf_device_map", {}).values()})
    if len(split) > 1:
        assert not {"cpu", "disk"} & set(split), f"{DEVICE_MAP_ENV}: part of the model was offloaded ({split})"
        home = hf.get_input_embeddings().weight.device
        assert home == torch.device("cuda", 0), f"the embedding is on {home}: tensors made on 'cuda' would not be home"
        print(f"{DEVICE_MAP_ENV}: the model is split over GPUs {split}", flush=True)
    n = hf.config.get_text_config().num_hidden_layers
    assert n == pins.N_LAYERS, f"{pins.MODEL_REPO} has {n} blocks; pins.TARGETS says {pins.N_LAYERS}"
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
