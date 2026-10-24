#!/bin/bash
# Zach (2026-10-24, amendment 27 note 2): keep the pooled RelP lens (the R-Lens: the kind every published neuronpedia
# "jpp" lens is, 0 clusters) of each 9B fit in h200_q9fit_1024.sh, which deletes it after the weighted J++ is exported.
# A hard link once merge-experts has written it and exited; the stamp is copied. CPU only.
set -u
K=/workspace/ext/pooled_keep; mkdir -p $K
for key in qwen3.5-9b-base qwen3.5-9b-ourjpp; do
  out=/workspace/ext/${key}_fit
  until [ -f "$out/pooled_lens.pt" ] && ! pgrep -f "merge-experts.*${key}_fit" > /dev/null; do
    grep -qs "=== $key \(fit\|merge\|router\) FAILED" /workspace/runs/bridge-cse_01EetL8PM7B9hLWZTfSi7urd-h200q9b-1024-0305.log && { echo "=== KEEP $key: its fit failed"; continue 2; }
    sleep 10
  done
  sleep 5
  ln "$out/pooled_lens.pt" "$K/${key}_pooled_lens.pt" && cp "$out"/pooled_lens*stamp*.json "$K/" 2>/dev/null
  echo "=== KEEP $key $(ls -la $K/${key}_pooled_lens.pt) sha256 $(sha256sum $K/${key}_pooled_lens.pt | cut -d' ' -f1) $(date -u +%T)"
done
