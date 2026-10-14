#!/usr/bin/env bash
# Run an experiment in its own detached tmux session; output is tee'd to log/<session>.log.
#   bash scripts/run.sh scripts/exp10_lens_sanity/config.yaml [overrides...]
#   tmux attach -t <session>     (Ctrl-b d to detach; the run keeps going)
#   tail -f log/<session>.log    (same output, survives the session)
set -euo pipefail

[ $# -ge 1 ] || { echo "usage: $0 <config.yaml> [key=value ...]" >&2; exit 2; }
command -v tmux >/dev/null || { echo "tmux not installed" >&2; exit 1; }

config=$1
exp=$(basename "$(dirname "$config")")
session="${exp}-$(date +%Y%m%d-%H%M%S)"
mkdir -p log
log="log/${session}.log"

# .env carries HF_HOME etc.: it must be exported before Python starts (huggingface_hub reads it on
# import), and the tmux shell is non-interactive, so ~/.bashrc does not provide it.
cmd='export PATH="$HOME/.local/bin:$PATH"; set -a; [ -f .env ] && . ./.env; set +a; '
# printf %q keeps overrides with spaces/brackets intact through the inner shell.
cmd+="uv run bj-run $(printf '%q ' "$@") 2>&1 | tee -a $(printf '%q' "$log")"
cmd+="; echo \"[exit \${PIPESTATUS[0]}] \$(date '+%F %T')\" | tee -a $(printf '%q' "$log")"
# Keep the pane open after the run so its final output can still be read on attach.
tmux new-session -d -s "$session" -c "$PWD" bash -c "$cmd; exec bash"

echo "session: $session"
echo "  attach: tmux attach -t $session"
echo "  log:    tail -f $log"
