#!/bin/bash
# Zach (2026-10-21): Qwen3-32B competence on the full v8 set right after its J++ fit (qwen3_32b_after_gemma_1021.sh).
# Registers target qwen3-32b (Qwen/Qwen3-32B@9216db5, 64 layers, standard RMSNorm gain, no BOS, prefix qwen3_32b_) with
# the exported lens's sha256 and the fit's held-out readout (its gate: macro recall@10 >= 0.45, recorded, not enforced
# for competence, which needs no lens), commits, then runs competence --guess and its report.
set -u
cd /workspace/bridge-jspace
set -a; . ./.env; set +a
PY="uv run --no-sync python"
Q=/workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-q32-1021-0432.log
until grep -q "^EXIT" $Q; do sleep 120; done
LENS=cache/qwen3-32b/lenses/jpp/Qwen3-32B_jpp_lens.pt
[ -f "$LENS" ] || { echo "no exported Qwen3-32B lens (the fit failed): stop"; exit 1; }
SHA=$(sha256sum "$LENS" | cut -d" " -f1)
GATE=$(grep -o "macro recall@10: .*" $Q | tail -1)
.venv/bin/python - "$SHA" "$GATE" <<'PY' || exit 1
import sys
from pathlib import Path
sha, gate = sys.argv[1], sys.argv[2]
p = Path("src/bridge_jspace/pins.py")
s = p.read_text()
anchor = "    # Qwen3.5-122B-A10B (MoE, 10B active)"
assert anchor in s and '"qwen3-32b"' not in s
block = f'''    # Qwen3-32B (dense, full attention in every layer: separates architecture from family; Zach, 2026-10-20/21): a J++ we
    # fit on it at every source layer 0-62 (32 wikitext prompts, the safety-research/jpp_lens@93f02cd recipe,
    # scripts/queues/qwen3_32b_fit_1020.sh); held-out readout {gate or "(not found in the fit log)"}.
    "qwen3-32b": {{
        "repo": "Qwen/Qwen3-32B",
        "revision": "9216db5781bf21249d130ec9da846c4624c16137",
        "n_layers": 64,
        "norm_gain": "weight",
        "bos": False,
        "run_prefix": "qwen3_32b_",
        "lenses": {{
            "jpp": ("local", "cache/qwen3-32b/lenses/jpp/Qwen3-32B_jpp_lens.pt", "{sha}"),
        }},
        "frozen_lens_sha256": "{sha}",
    }},
'''
p.write_text(s.replace(anchor, block + anchor))
print("target qwen3-32b registered")
PY
git add src/bridge_jspace/pins.py && git -c user.name="Zach Perlman" -c user.email=zachperlman20@gmail.com commit -q -m "pins: qwen3-32b (J++ at every layer 0-62); $GATE

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || exit 1
BJ_TARGET=qwen3-32b $PY scripts/tasks_v2.py competence --set full_v8 --name qwen3_32b_full_v8_competence_v1 --guess \
  --why "Zach (2026-10-21): Qwen3-32B competence on the full v8 set, right after its fit" \
  && $PY scripts/competence_full_report.py qwen3_32b_full_v8_competence_v1
