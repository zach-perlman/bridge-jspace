"""exp19_fit_data, 64-prompt fits: write the run's manifest before it runs (write-once). Standard library only.

python3 scripts/exp19_fit_data/make_manifest64.py RUN_NAME   (from the repo root, on the GPU box, after fit_v2)
"""

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

POOLS = Path("data/exp19_fit_pools")
V2 = Path("cache/exp19/fit_v2")
CONDITIONS = {"chat64": "chat", "wiki64": "wiki_a"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def head(repo: str) -> str:
    return subprocess.run(
        ["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()


def main(run: str) -> None:
    path = Path("results/exp19_fit_data") / run / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), f"{path} exists; manifests are written once"
    manifest = {
        "exp": "exp19_fit_data",
        "run": run,
        "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "follows": "fit_v2 (25 prompts per lens; UNVERIFIED): J++ macro pass@10 chat .706 vs wiki_a .638 "
        "(+.068 [+.03, +.11], led by poetry +.25), while the pooled lens was lower on chat (-.062 [-.09, -.03])",
        "question": "Does the chat pool's J++ advantage over WikiText hold at the recipe's 64 fitting prompts, and does "
        "our pipeline reproduce the published 64-prompt J++?",
        "why": "The human (Zach, 2026-10-17) asked for a chat fit on 64 prompts. The agent proposed adding wiki64: the "
        "published Qwen J++ was fitted by the J++ authors' own code (its config.yaml: source koayon/jpp-lenses, fitted "
        "2026-09-07), so it is not a same-pipeline baseline. The human chose chat64 + wiki64 over chat64 alone.",
        "model": {"repo": "Qwen/Qwen3.6-27B", "revision": "6a9e13bd6fc8f0983b9b99948120bc37f49c13e9"},
        "tools": {
            "jpp_lens": {"repo": "safety-research/jpp_lens", "commit": head("/workspace/lensfit/jpp_lens")},
            "wrapper": "scripts/exp19_fit_data/jpp_pool_cli.py (as fit_v2); run by scripts/exp19_fit_data/run_fits64.sh",
        },
        "conditions": {
            c: {
                "pool": str(POOLS / f"{pool}.json"),
                "pool_sha256": sha(POOLS / f"{pool}.json"),
                "fit_prompts": "the pool's first 64 texts (fit_v2's 25-prompt lens used the first 25 of them)",
                "router": f"{V2 / pool / 'router.pt'} copied (fit on the same pool's first 1000 texts, seed 0)",
                "router_sha256": sha(V2 / pool / "router.pt"),
            }
            for c, pool in CONDITIONS.items()
        },
        "shared_inputs": {
            "correctness.csv": {"from": str(V2 / "correctness.csv"), "sha256": sha(V2 / "correctness.csv")},
            "readout_cache.pt": {"from": str(V2 / "readout_cache.pt"), "sha256": sha(V2 / "readout_cache.pt")},
        },
        "fit": "fit_v2's recipe (rlens LRP, 16 Jacobian rows per pass, layers 0-62, expert weights on fit:0) with 64 "
        "shard prompts instead of 25; the router and the item grades are fit_v2's, so a 25-vs-64 comparison differs "
        "only in the number of shard prompts",
        "evals": {
            "primary": "jpp_cli.py evaluate (J++ readout evals, held-out:0), one call per condition right after its "
            "lenses are saved (J++ and pooled), in results/exp19_fit_data/RUN/eval_<condition>/",
            "combined_with": "results/exp19_fit_data/fit_v2/eval_ranks.csv (the 25-prompt lenses, the published J++ "
            "and J-lens, logit). Pooling the files is valid because evaluate is deterministic: fit_v2's early and "
            "final evals gave identical ranks on all 231,525 shared rows",
            "analysis": "scripts/exp19_fit_data/analyze.py (paired bootstrap over items, 10,000 resamples, seed 0)",
        },
        "decision": {
            "main": "jpp_chat64 - jpp_wiki64, macro pass@10: the chat advantage holds at 64 prompts if the 95% CI "
            "excludes 0 on the positive side",
            "prediction": "positive for J++ (led by poetry, as fit_v2); negative for the pooled lenses",
            "pipeline_check": "jpp_wiki64 - published J++, macro pass@10: our pipeline reproduces the published fit if "
            "the CI includes 0; if not, the published lens is not a fair reference and fit_v2's 25-prompt cost "
            "(-.076, wiki_a vs published) mixes prompt count with pipeline",
            "scaling": "chat64 - chat and wiki64 - wiki_a (64 vs 25 prompts within our pipeline), reported",
        },
        "limits": "one fit per condition and no noise floor between fits (fit_v2's wiki_b was cancelled); each 64-prompt "
        "lens shares its first 25 prompts and its router with the fit_v2 lens of the same pool, so 25-vs-64 "
        "comparisons are not independent",
        "seeds": {"router": 0, "items_split": "held-out:0 / fit:0", "bootstrap": 0},
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1])
