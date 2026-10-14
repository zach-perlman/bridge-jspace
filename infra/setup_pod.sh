#!/usr/bin/env bash
# Bootstrap a fresh GPU box (Vast / Runpod / Sesterce). Idempotent; re-run after restarts.
#   git clone <repo> && cd bridge-jspace && bash infra/setup_pod.sh
# Env knobs: PERSIST (cache root; auto-detected), MODEL_CONFIG (model + lenses to prefetch).
set -euo pipefail

MIN_DRIVER_CUDA="12.6"   # torch is pinned to the cu126 wheels, see pyproject

die() { echo "!! $*" >&2; exit 1; }

# Big disk for caches: a mounted volume if present, else the provider's scratch disk, else $HOME.
pick_persist() {
  for d in /workspace /ephemeral; do
    [ -d "$d" ] && [ -w "$d" ] && { echo "$d"; return; }
  done
  echo "$HOME"
}
PERSIST="${PERSIST:-$(pick_persist)}"
export HF_HOME="${HF_HOME:-$PERSIST/hf}"
export UV_CACHE_DIR="${UV_CACHE_DIR:-$PERSIST/uv-cache}"
MODEL_CONFIG="${MODEL_CONFIG:-configs/models/qwen3.5-4b.yaml}"
mkdir -p "$HF_HOME" "$UV_CACHE_DIR"
echo ">> caches under $PERSIST ($(df -h "$PERSIST" | awk 'NR==2 {print $4}') free)"

# Fail early on an old driver: CUDA wheels newer than the driver import fine but die on first use.
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
driver_cuda=$(nvidia-smi | grep -oP 'CUDA Version: \K[0-9.]+')
[ "$(printf '%s\n' "$MIN_DRIVER_CUDA" "$driver_cuda" | sort -V | head -1)" = "$MIN_DRIVER_CUDA" ] \
  || die "driver supports CUDA $driver_cuda < $MIN_DRIVER_CUDA: pick an image with a newer driver"

if ! command -v uv >/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

# Persist env vars for new shells; the marked block is rewritten so PERSIST changes stick.
sed -i '/# >>> setup_pod >>>/,/# <<< setup_pod <<</d' ~/.bashrc 2>/dev/null || true
cat >> ~/.bashrc <<RC
# >>> setup_pod >>>
export HF_HOME=$HF_HOME
export UV_CACHE_DIR=$UV_CACHE_DIR
export PATH="\$HOME/.local/bin:\$PATH"
# <<< setup_pod <<<
RC

uv sync --locked
[ -f .env ] || { cp .env.example .env; echo ">> fill in .env (HF_TOKEN)"; }
# scripts/run.sh sources .env: keep the cache locations there too, because non-interactive shells
# (ssh commands, tmux `bash -c`) return early from Ubuntu's ~/.bashrc and would miss HF_HOME.
for kv in "HF_HOME=$HF_HOME" "UV_CACHE_DIR=$UV_CACHE_DIR"; do
  key=${kv%%=*}
  if grep -q "^$key=" .env; then sed -i "s|^$key=.*|$kv|" .env; else echo "$kv" >> .env; fi
done
set -a; source .env; set +a

# Run a real kernel: torch.cuda.is_available() can be True while kernels still fail.
echo ">> CUDA check"
uv run python - <<'PY' || die "CUDA kernels fail (driver vs torch CUDA mismatch?)"
import torch
x = torch.ones(2, device="cuda")
assert (x * 2).sum().item() == 4.0
print(f"   torch {torch.__version__} (CUDA {torch.version.cuda}) on {torch.cuda.get_device_name(0)}: ok")
import fla  # noqa: F401  fast gated-delta kernels for the qwen3_5 linear-attention layers
print("   flash-linear-attention: ok")
PY

# Prefetch the pinned model snapshot and its lens files (retries on HF 429s).
uv run python scripts/prefetch.py "$MODEL_CONFIG"

command -v tmux >/dev/null || die "tmux missing: install it (apt-get install -y tmux); runs go through scripts/run.sh"
# Mouse-wheel scrolling through run output, and a longer history to scroll back in.
touch ~/.tmux.conf
grep -q '^set -g mouse on' ~/.tmux.conf || printf '%s\n' \
  '# mouse: wheel scrolls the pane history (enters copy mode); select text with Shift held' \
  'set -g mouse on' 'set -g history-limit 50000' >> ~/.tmux.conf
tmux source-file ~/.tmux.conf 2>/dev/null || true  # applies to an already running tmux server
echo ">> next: make check && make test-model   (open a new shell or 'source ~/.bashrc' first)"
