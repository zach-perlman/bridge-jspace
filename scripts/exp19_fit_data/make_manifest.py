"""exp19_fit_data: write a run's manifest before it runs (write-once). Standard library only.

python3 scripts/exp19_fit_data/make_manifest.py RUN_NAME   (from the repo root, on the GPU box)
"""

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

POOLS = Path("data/exp19_fit_pools")
CONDITIONS = ("wiki_a", "wiki_b", "math", "chat", "mix")
JPP_LENS = "/workspace/lensfit/jpp_lens"
NEURONPEDIA = "/workspace/lensfit/neuronpedia"


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
        "question": "Does the text a J++ lens is fitted on change what it reads? Lenses on Qwen3.6-27B read places and "
        "people better than numbers, and every published open lens is fitted on raw WikiText while our instruction "
        "model is read inside its chat template: are those the fitting data?",
        "why": "Chosen by the human (Zach, 2026-10-16, after a meeting with Danyil): J++ only, 25 fitting prompts per "
        "lens, domains math (OpenWebMath), chat-formatted (UltraChat) and a mix; the router refit on each domain. "
        "The second WikiText draw (wiki_b) as the noise floor was the agent's proposal in the design the human "
        "answered; the human did not remove it.",
        "model": {"repo": "Qwen/Qwen3.6-27B", "revision": "6a9e13bd6fc8f0983b9b99948120bc37f49c13e9"},
        "tools": {
            "jpp_lens": {"repo": "safety-research/jpp_lens", "commit": head(JPP_LENS)},
            "neuronpedia": {
                "repo": "hijohnnylin/neuronpedia (utils/neuronpedia-utils/neuronpedia_utils/jlens)",
                "commit": head(NEURONPEDIA),
                "used": "jpp/grade.py",
            },
            "wrapper": "scripts/exp19_fit_data/jpp_pool_cli.py: jpp_cli.py with the router on the GPU (as "
            "neuronpedia's jpp_cli_gpu.py) and jlens.examples.load_wikitext_prompts replaced by the pool in "
            "$FIT_POOL_JSON, so the router (first 1000) and the shards (first 25) read the condition's pool",
        },
        "conditions": {c: {"pool": str(POOLS / f"{c}.json"), "sha256": sha(POOLS / f"{c}.json")} for c in CONDITIONS},
        "pools": "scripts/exp19_fit_data/make_pools.py: 1000 texts each, the first qualifying records of each stream "
        "(>= 600 characters, cut at 2000). wiki_a is exactly the J++ recipe's WikiText pool (checked); wiki_b the next "
        "1000 WikiText records; math open-web-math/open-web-math; chat HuggingFaceH4/ultrachat_200k train_sft "
        "rendered with Qwen3.6-27B's chat template (enable_thinking=False; earlier assistant turns carry no think "
        "block); mix = wiki_a, math, chat interleaved (first 25: 9 WikiText, 8 math, 8 chat).",
        "fit": {
            "recipe": "J++ (neuronpedia fit-jpp-lens.sh steps): grade -> fit-router (1000 pool texts, K=8, PCA 64, "
            "skip first 16 positions, 128 tokens) -> fit-shard (first 25 pool texts, rlens LRP, 16 Jacobian rows per "
            "pass) -> merge-experts (also writes the pooled lens: the experts' rlens-LRP Jacobians averaged, i.e. an "
            "R-lens on the same data) -> fit-weights (expert weights on the eval items' fitting split fit:0, the same for every "
            "condition)",
            "layers": "0-62 (every block but the last, 63, the transport target)",
            "n_prompts": 25,
            "differs_from_recipe": "25 shard prompts instead of 64 (the human's choice); the router pool is the "
            "condition's, not always WikiText",
            "supersedes": "fit_v1, whose manifest said 32 Jacobian rows per pass: 32 ran out of GPU memory in a smoke "
            "test before any fit, so fit_v1 never ran; 16 is the recipe default and changes batching, not the estimate",
        },
        "evals": {
            "primary": "J++'s readout evals (multihop, multilingual, typo, association, poetry) by jpp_cli.py evaluate "
            "on the held-out split held-out:0 (the expert weights never saw these items): pass@1 and pass@10 per "
            "family, item-weighted, for each condition's J++ lens and pooled (R-lens) lens",
            "references": "the published Qwen3.6-27B J++ (WikiText, 64 prompts) and J-lens (WikiText, 1000 prompts) "
            "from neuronpedia/jacobian-lens at the revision in pins.py, and the logit lens, in the same evaluate call",
            "planned_after": "a chat-formatted read (exp08's brew protocol inside the chat template) and Anthropic's "
            "arithmetic set; not part of this run",
        },
        "decision": {
            "noise_floor": "per family, |wiki_b - wiki_a| in pass@10",
            "domain_changes_family": "a condition changes a family if its pass@10 minus wiki_a's has a paired "
            "bootstrap 95% CI over held-out items (10,000 resamples, seed 0) excluding 0 and is larger in size than "
            "the noise floor",
            "H1_math_numbers": "math above wiki_a on multihop items whose intermediate is a number (digits or a number "
            "word), not on the other multihop items",
            "H2_chat": "no prediction on these raw-text evals (they are not chat formatted); reported, tested later "
            "on chat-formatted reads",
            "H3_mix": "mix no worse than wiki_a on any family (no family below by the rule above)",
            "n_25_cost": "wiki_a against the published J++ (64 prompts) shows what fitting on 25 prompts costs",
        },
        "seeds": {"router": 0, "items_split": "held-out:0 / fit:0", "bootstrap": 0},
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1])
