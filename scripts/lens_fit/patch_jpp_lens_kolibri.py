"""Adds Kolibri-1 (transformers 5.20 kolibri1) to a copy of jpp_lens at /workspace/ext/jpp_lens_kol (Zach, 2026-10-24,
prereg amendment 28 note 2): cp -r of /workspace/ext/jpp_lens (LICENSE NOTICE README.md pyproject.toml scripts src), then
python3 scripts/lens_fit/patch_jpp_lens_kolibri.py. Each replacement must match exactly once. Run Kolibri J++ with
PYTHONPATH=/workspace/ext/jpp_lens_kol/src and /workspace/ext/kolibri_env/bin/python (its jlens shadows Anthropic's)."""
from pathlib import Path

p = Path("/workspace/ext/jpp_lens_kol/src/workspace_lens/lrp/lrp.py")
s = p.read_text()


def rep(old: str, new: str) -> None:
    global s
    assert s.count(old) == 1, (s.count(old), old[:80])
    s = s.replace(old, new)


rep('''    "Gemma4TextMLP",  # GELU-tanh; same down(act(gate(x)) * up(x)) forward
''', '''    "Gemma4TextMLP",  # GELU-tanh; same down(act(gate(x)) * up(x)) forward
    "Kolibri1MLP",  # Kolibri-1's shared expert: SiLU, down(act(gate(x)) * up(x)) (bridge-jspace, 2026-10-24; transformers 5.20.2)
''')
rep('''_KNOWN_FUSED_EXPERTS = ("Qwen3_5MoeExperts", "Qwen3MoeExperts", "DeepseekV4Experts")
_KNOWN_MOE_BLOCKS = ("Qwen3_5MoeSparseMoeBlock",)
''', '''_KNOWN_FUSED_EXPERTS = ("Qwen3_5MoeExperts", "Qwen3MoeExperts", "DeepseekV4Experts", "Kolibri1Experts")
_KNOWN_MOE_BLOCKS = ("Qwen3_5MoeSparseMoeBlock",)
# MoE blocks whose shared expert has NO gate: experts(x) + shared_experts(x) (Kolibri-1; bridge-jspace, 2026-10-24,
# transformers 5.20.2). Only ``shared_expert_scale`` acts on them; ``shared_gate_detach`` has nothing to detach.
_KNOWN_UNGATED_MOE_BLOCKS = ("Kolibri1SparseMoeBlock",)
# Fused-experts classes whose stock loop one-hots over num_experts + 1 (a sentinel "no expert" slot it skips).
_SENTINEL_SLOT_EXPERTS = ("Kolibri1Experts",)
''')
rep('''    "Qwen3MoeRMSNorm": _qwen2_rmsnorm_lrp_forward,  # byte-identical to Qwen2's
''', '''    "Qwen3MoeRMSNorm": _qwen2_rmsnorm_lrp_forward,  # byte-identical to Qwen2's
    "Kolibri1RMSNorm": _qwen2_rmsnorm_lrp_forward,  # byte-identical to Qwen2's (bridge-jspace, 2026-10-24; transformers 5.20.2)
''')
rep('''        with t.no_grad():
            expert_mask = nn.functional.one_hot(top_k_index, num_classes=self.num_experts)
''', '''        num_classes = self.num_experts + (1 if type(self).__name__ in _SENTINEL_SLOT_EXPERTS else 0)
        with t.no_grad():
            expert_mask = nn.functional.one_hot(top_k_index, num_classes=num_classes)
''')
rep('''def _deepseek_hyperconnection_lrp_forward(''', '''def _make_ungated_moe_block_lrp_forward(shared_expert_scale: float) -> Any:
    """Value-exact replica of Kolibri1SparseMoeBlock.forward (transformers 5.20.2): the routed experts plus an ungated
    shared expert on the block input, with ``shared_expert_scale`` multiplying the GRADIENT through the shared
    contribution by c via ``s + (c-1)*(s - s.detach())`` (exactly zero in the forward, so values are bit-identical)."""

    def forward(self: Any, hidden_states: Tensor) -> Tensor:
        residuals = hidden_states
        orig_shape = hidden_states.shape
        _, topk_weights, topk_indices = self.gate(hidden_states)
        hidden_states = hidden_states.view(-1, hidden_states.shape[-1])
        hidden_states = self.experts(hidden_states, topk_indices, topk_weights).view(*orig_shape)
        shared = self.shared_experts(residuals)
        if shared_expert_scale != 1.0:
            shared = shared + (shared_expert_scale - 1.0) * (shared - shared.detach())
        result: Tensor = hidden_states + shared
        return result

    return forward


def _deepseek_hyperconnection_lrp_forward(''')
rep('''                report.moe_gates.append(name)
            elif _is_gated_mlp(module):''', '''                report.moe_gates.append(name)
            elif cls in _KNOWN_UNGATED_MOE_BLOCKS:
                if lrp_config.shared_expert_scale == 1.0:
                    continue  # no gate to detach; the shared branch keeps stock grads
                required_attributes = ("shared_experts", "experts", "gate")
                if not all(hasattr(module, attr) for attr in required_attributes) or hasattr(module, "shared_expert_gate"):
                    raise RuntimeError(
                        f"MoE block class {cls!r} at {name!r} does not match the ungated Kolibri-1 block "
                        f"({required_attributes}, no shared_expert_gate) — verify its forward before registering."
                    )
                _patch(module, _make_ungated_moe_block_lrp_forward(lrp_config.shared_expert_scale))
                report.moe_gates.append(name)
            elif _is_gated_mlp(module):''')
p.write_text(s)
print("patched", p)
