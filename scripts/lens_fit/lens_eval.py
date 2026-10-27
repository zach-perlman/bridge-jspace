"""lens_eval: score published or fitted lenses with the J++ recipe's own held-out evaluation (Dan, 2026-10-22), so every
lens we use has the number Zach's cards report: pass@10 per eval and the macro, item-weighted, on the held-out:0
readout items the model answers right.

The recipe's `evaluate` reads neuronpedia's / Zach's exported layout ({"J": {layer: [d, d]}, "source_layers",
"d_model", "n_prompts"[, "provenance"]}) as it is (workspace_lens.utils.load_lens_file -> load_legacy_format_lens;
checked on every lens below on 2026-10-22), so no conversion: such a file is labelled with --hf-model-name, so the
model check is on d_model only, and a base-model lens can be scored on the chat model.

Steps: manifest.json (before anything runs) -> grade the model once (scripts/lens_fit/jpp_grade.py; or reuse
--correctness-csv, e.g. the CSV another lens of this model was scored with, so the item sets are equal) -> one
`jpp_cli.py evaluate --items held-out:0` per distinct layer set (each lens at every layer it has; the logit lens, the
floor every model gets, at the union). pass@10 at any layer subset is then computed from the per-layer ranks
(scripts/lens_table.py): the recipe's pass@k is the best rank over the layers given, per item.

Run in the recipe's environment from its root (its data paths are relative), output to
results/lens_eval/<name>/ of this repo (never overwritten):

cd /ephemeral/ext/jpp_lens && uv run --no-sync python <repo>/scripts/lens_fit/lens_eval.py --name NAME --model HF_NAME \
  --lens hf:REPO@REVISION:PATH[#SHA256] [--lens /local/lens.pt ...] [--correctness-csv CSV]
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LOGIT = "logit"  # jpp_cli.py's spec for the logit lens


@dataclass(frozen=True)
class LensSpec:
    """A lens file: on the Hub (repo, revision, path) or local (path only); sha256 checked when given."""

    path: str
    repo: str | None = None
    revision: str | None = None
    sha256: str | None = None


def parse_spec(text: str) -> LensSpec:
    """'hf:REPO@REVISION:PATH[#SHA256]' or 'LOCAL_PATH[#SHA256]'. The revision must be a full commit hash (a pin)."""
    body, _, sha = text.partition("#")
    if sha and (len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha)):
        raise ValueError(f"{text!r}: sha256 must be 64 lowercase hex characters")
    if not body.startswith("hf:"):
        return LensSpec(path=body, sha256=sha or None)
    repo_rev, sep, path = body[3:].partition(":")
    repo, at, rev = repo_rev.partition("@")
    if not (sep and at and repo and path) or len(rev) != 40:
        raise ValueError(f"{text!r}: expected hf:REPO@<40-char commit>:PATH")
    return LensSpec(path=path, repo=repo, revision=rev, sha256=sha or None)


def plan_groups(lens_layers: dict[str, list[int]]) -> list[tuple[list[int], list[str]]]:
    """One evaluate call per distinct layer set: [(layers, lens names)], the widest set first. The logit lens joins the
    group at the union of all layers (its own group if no lens has exactly that set), so it covers every layer any
    lens is scored at."""
    by_layers: dict[tuple[int, ...], list[str]] = {}
    for name, layers in lens_layers.items():
        by_layers.setdefault(tuple(sorted(set(layers))), []).append(name)
    union = tuple(sorted(set().union(*by_layers))) if by_layers else ()
    if not union:
        raise ValueError("no lens layers given")
    by_layers.setdefault(union, []).append(LOGIT)
    return [(list(k), v) for k, v in sorted(by_layers.items(), key=lambda kv: (-len(kv[0]), kv[0]))]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 24), b""):
            h.update(block)
    return h.hexdigest()


def resolve(spec: LensSpec) -> Path:
    if spec.repo is None:
        return Path(spec.path).resolve()
    from huggingface_hub import hf_hub_download

    return Path(hf_hub_download(spec.repo, spec.path, revision=spec.revision))


def lens_meta(path: Path) -> dict:
    """source_layers, d_model, n_prompts of an exported lens (J layout, no config: the recipe's legacy loader) or one
    the recipe wrote (with "config": BaseLens.load), read memory-mapped. The layers are the ones evaluate may use."""
    import torch

    ck = torch.load(path, map_location="cpu", weights_only=True, mmap=True)
    cfg = ck.get("config") or {}
    layers = ck.get("source_layers") or list(ck["J"])
    return {"format": "J" if not cfg else "recipe", "source_layers": sorted(int(x) for x in layers),
            "d_model": ck.get("d_model", cfg.get("d_model")),
            "n_prompts": ck.get("n_prompts", cfg.get("num_prompts_trained_on"))}  # fmt: skip


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, check=False).stdout.strip()


def run(cmd: list[str], cwd: Path) -> float:
    print(f"\n=== {' '.join(cmd[:4])} ... ({dt.datetime.now().strftime('%H:%M:%S')})", flush=True)
    t = time.time()
    subprocess.run(cmd, cwd=cwd, check=True)
    return round(time.time() - t, 1)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="run name = the job id; output results/lens_eval/<name>/")
    ap.add_argument("--model", required=True, help="HF model name, as the recipe loads it (its main revision)")
    ap.add_argument("--lens", action="append", required=True, help="hf:REPO@REVISION:PATH[#SHA256] or a local path")
    ap.add_argument("--correctness-csv", help="reuse this graded CSV (path relative to this repo) instead of grading")
    ap.add_argument("--recipe-dir", default=".", help="the jpp_lens checkout (default: the working directory)")
    ap.add_argument("--device-map", help="passed to evaluate (e.g. 'cpu' for a smoke run, 'auto' to shard a big model)")
    args = ap.parse_args(argv)

    recipe = Path(args.recipe_dir).resolve()
    assert (recipe / "scripts" / "jpp_cli.py").exists(), f"{recipe} is not a jpp_lens checkout"
    out = REPO / "results" / "lens_eval" / args.name
    assert not out.exists(), f"{out} exists; runs are written once"

    lenses: dict[str, dict] = {}
    for text in args.lens:
        spec = parse_spec(text)
        path = resolve(spec)
        sha = sha256_of(path)
        if spec.sha256 and sha != spec.sha256:
            raise SystemExit(f"{text}: sha256 {sha} != pinned {spec.sha256}")
        name = path.stem  # jpp_cli.py names each lens by its file stem
        if name in lenses or name == LOGIT:
            raise SystemExit(f"two lenses named {name!r}: the ranks could not tell them apart")
        lenses[name] = {"spec": text, "path": str(path), "sha256": sha, **lens_meta(path)}
    groups = plan_groups({k: v["source_layers"] for k, v in lenses.items()})
    union = groups[0][0]  # the widest set comes first: the union, where the logit lens is

    out.mkdir(parents=True)
    csv_src = None if args.correctness_csv is None else (REPO / args.correctness_csv).resolve()
    manifest = {
        "exp": "lens_eval",
        "run": args.name,
        "written_utc": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": socket.gethostname(),
        "argv": sys.argv,
        "repo_commit": git(REPO, "rev-parse", "HEAD"),
        "model": {"hf_model_name": args.model, "revision": "the Hub's main at run time (the recipe takes no revision)"},
        "recipe": {
            "dir": str(recipe),
            "commit": git(recipe, "rev-parse", "HEAD"),
            "dirty": bool(git(recipe, "status", "--porcelain", "--untracked-files=no")),
        },
        "items": "held-out:0 (the recipe's split, fit fraction 0.2), the items the model answers right",
        "correctness": {
            "source": "graded by scripts/lens_fit/jpp_grade.py" if csv_src is None else str(csv_src),
            "sha256": None if csv_src is None else sha256_of(csv_src),
        },
        "lenses": lenses,
        "groups": [
            {"layers": g, "lenses": names, "out": f"eval_ranks_g{i}.csv"} for i, (g, names) in enumerate(groups)
        ],
        "metric": "pass@10 per eval and macro (mean of the five), item-weighted, best rank over the layers scored",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")

    timing: dict[str, float] = {}
    csv = out / "model_correctness.csv"
    if csv_src is None:
        timing["grade"] = run([sys.executable, str(REPO / "scripts/lens_fit/jpp_grade.py"), args.model,
                               ",".join(map(str, union)), str(csv)], recipe)  # fmt: skip
    else:
        shutil.copy(csv_src, csv)
    device = [] if args.device_map is None else ["--device-map", args.device_map]
    for i, (layers, names) in enumerate(groups):
        paths = [LOGIT if n == LOGIT else lenses[n]["path"] for n in names]
        timing[f"evaluate_g{i}"] = run([sys.executable, "scripts/jpp_cli.py", "evaluate", "--hf-model-name", args.model,
                                        *device, "--layers", ",".join(map(str, layers)), "--lens", *paths, "--items",
                                        "held-out:0", "--correctness-csv", str(csv), "--out",
                                        str(out / f"eval_ranks_g{i}.csv")], recipe)  # fmt: skip
    (out / "timing.json").write_text(json.dumps(timing, indent=1) + "\n")
    print(f"LENS_EVAL_DONE {out}")


if __name__ == "__main__":
    main()
