#!/usr/bin/env bash
# Bootstrap a fresh GPU box (Vast / Runpod / Sesterce). Idempotent; re-run after restarts.
#   git clone <repo> && cd bridge-jspace && bash infra/setup_pod.sh
# Env knobs: PERSIST (cache root; auto-detected), MODELS (targets to prefetch, default our three: the 9B, the 27B,
# Muse; a target with configs/models/<t>.yaml or one pinned in bridge_jspace.pins), MODEL_CONFIG (one YAML instead).
# An old driver (CUDA < 12.8, e.g. 535 / 12.2 on the 28 Oct helper) gets NVIDIA's forward-compatibility package
# (cuda-compat-12-8, no reboot) when sudo works; its library path goes into ~/.bashrc and .env for the jobs.
set -euo pipefail

MIN_DRIVER_CUDA="12.8"   # torch is pinned to the cu128 wheels, see pyproject

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
MODELS="${MODELS:-qwen3.5-9b qwen3.6-27b muse-glimmer-30b}"
MODEL_CONFIG="${MODEL_CONFIG:-}"
COMPAT=/usr/local/cuda-12.8/compat
mkdir -p "$HF_HOME" "$UV_CACHE_DIR"
echo ">> caches under $PERSIST ($(df -h "$PERSIST" | awk 'NR==2 {print $4}') free)"

# Fail early on an old driver: CUDA wheels newer than the driver import fine but die on first use.
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
driver_cuda=$(nvidia-smi | grep -oP 'CUDA (UMD )?Version: \K[0-9.]+')  # newer drivers print 'CUDA UMD Version'
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:-}"
if [ "$(printf '%s\n' "$MIN_DRIVER_CUDA" "$driver_cuda" | sort -V | head -1)" != "$MIN_DRIVER_CUDA" ]; then
  # Datacenter GPUs on an LTS driver run newer CUDA through the forward-compatibility user-mode driver.
  sudo -n true 2>/dev/null || die "driver supports CUDA $driver_cuda < $MIN_DRIVER_CUDA and no sudo for cuda-compat: pick a newer image"
  [ -d "$COMPAT" ] || sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -q cuda-compat-12-8 >/dev/null \
    || die "driver supports CUDA $driver_cuda < $MIN_DRIVER_CUDA and cuda-compat-12-8 did not install"
  export LD_LIBRARY_PATH="$COMPAT${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  echo ">> driver CUDA $driver_cuda: using the forward-compatibility driver in $COMPAT"
fi

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
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
# <<< setup_pod <<<
RC

uv sync --locked
[ -f .env ] || { cp .env.example .env; echo ">> fill in .env (HF_TOKEN)"; }
# scripts/run.sh sources .env: keep the cache locations there too, because non-interactive shells
# (ssh commands, tmux `bash -c`) return early from Ubuntu's ~/.bashrc and would miss HF_HOME.
for kv in "HF_HOME=$HF_HOME" "UV_CACHE_DIR=$UV_CACHE_DIR" ${LD_LIBRARY_PATH:+"LD_LIBRARY_PATH=$LD_LIBRARY_PATH"}; do
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

# Prefetch the pinned model snapshots and their lens files (retries on HF 429s; local lenses placed and sha-checked).
if [ -n "$MODEL_CONFIG" ]; then
  uv run python scripts/prefetch.py "$MODEL_CONFIG"
else
  for m in $MODELS; do
    echo ">> prefetch $m"
    if [ -f "configs/models/$m.yaml" ] && ! grep -q "\"$m\": {" src/bridge_jspace/pins.py; then
      uv run python scripts/prefetch.py "configs/models/$m.yaml"
    else
      uv run python scripts/prefetch.py "$m"
    fi
  done
fi

command -v tmux >/dev/null || die "tmux missing: install it (apt-get install -y tmux); runs go through scripts/run.sh"
# Mouse-wheel scrolling through run output, and a longer history to scroll back in.
touch ~/.tmux.conf
grep -q '^set -g mouse on' ~/.tmux.conf || printf '%s\n' \
  '# mouse: wheel scrolls the pane history (enters copy mode); select text with Shift held' \
  'set -g mouse on' 'set -g history-limit 50000' >> ~/.tmux.conf
tmux source-file ~/.tmux.conf 2>/dev/null || true  # applies to an already running tmux server
echo ">> next: make check && make test-model   (open a new shell or 'source ~/.bashrc' first)"
