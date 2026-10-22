"""The Qwen3-32B J++ fit on a 2x H200 box (Dan, 22-23 Oct night). Standard library only; run on the box:

  nohup python3 ~/work/bridge-jspace/scripts/lens_fit/h200_fit.py > ~/work/fit32b/launcher.log 2>&1 &

Recipe: safety-research/jpp_lens@93f02cd, 64 WikiText prompts x 128 tokens, skip 16, router seed 0 (fit once on the 64
prompts), target = the last block, rlens LRP, 8 experts (the recipe's), source layers 16-51 (25-80% depth: Zach's band;
a full-depth fit does not fit next to a 32B model). Two shards x 32 prompts, one per GPU, the same router; merged into
one lens; graded, readout weights fit, held-out evaluation, exported to fp16, sha256.
Rules (Dan): Jacobian rows per pass 10, on OOM 8, then 6; abort on > 300 s per prompt at the chosen rows or OOM at 6;
a 4 h wall-time limit. On any stop: logs and artifacts are kept, status.json says why, and TERMINATE_CMD (if set:
the provider's API call) runs last.
"""

import json
import os
import subprocess
import time
from pathlib import Path

W = Path.home() / "work"
OUT = W / "fit32b"
JPP = W / "jpp_lens"
MODEL = "Qwen/Qwen3-32B"
LAYERS = ",".join(str(x) for x in range(16, 52))
N, SHARDS, ROWS = 64, 2, (10, 8, 6)
LIMIT_S, SLOW_S, CKPT, LOAD_S = 4 * 3600, 300, 4, 1200  # wall limit; s / prompt; prompts per checkpoint; model load
ENV = {**os.environ, "UV_CACHE_DIR": str(W / "uv-cache"), "HF_HOME": str(W / "hf"),
       "PATH": f"{Path.home()}/.local/bin:{os.environ['PATH']}"}  # fmt: skip
C = ["uv", "run", "--no-sync", "python", "scripts/jpp_cli.py"]
T0 = time.time()
status: dict = {"model": MODEL, "layers": LAYERS, "prompts": N, "shards": SHARDS, "started": time.strftime("%FT%TZ", time.gmtime()), "steps": []}  # fmt: skip


def save(state: str, **kw) -> None:
    status.update(state=state, elapsed_s=round(time.time() - T0), **kw)
    (OUT / "status.json").write_text(json.dumps(status, indent=1) + "\n")


def stop(state: str, **kw) -> None:
    save(state, **kw)
    if os.environ.get("TERMINATE_CMD"):
        subprocess.run(os.environ["TERMINATE_CMD"], shell=True, check=False)
    raise SystemExit(0 if state == "DONE" else 1)


def run(name: str, args: list[str], gpu: int = 0) -> None:
    """A blocking step; its log in OUT/<name>.log; the wall limit applies."""
    t = time.time()
    with open(OUT / f"{name}.log", "w") as log:
        p = subprocess.Popen(
            args, cwd=JPP, env={**ENV, "CUDA_VISIBLE_DEVICES": str(gpu)}, stdout=log, stderr=subprocess.STDOUT
        )
        while p.poll() is None:
            if time.time() - T0 > LIMIT_S:
                p.kill()
                stop("ABORT_TIME", at=name)
            time.sleep(15)
    status["steps"].append({"step": name, "seconds": round(time.time() - t), "exit": p.returncode})
    save("RUNNING", at=name)
    if p.returncode:
        stop("FAIL", at=name)


def newest(d: Path) -> float:
    return max((f.stat().st_mtime for f in d.rglob("*") if f.is_file()), default=0.0)


def shards() -> None:
    rows = {i: 0 for i in range(SHARDS)}  # index into ROWS
    procs: dict[int, tuple] = {}

    def launch(i: int) -> None:
        r = ROWS[rows[i]]
        art = OUT / f"artifacts_s{i}_r{r}"
        args = C + ["fit-shard", "--hf-model-name", MODEL, "--layers", LAYERS, "--router-path", str(OUT / "router.pt"),
                    "--shard-idx", str(i), "--num-shards", str(SHARDS), "--num-prompts", str(N), "--target-offset", "-1",
                    "--lrp-mode", "rlens", "--jacobian-rows-per-pass", str(r), "--max-seq-len", "128",
                    "--skip-first-n-positions", "16", "--checkpoint-every-n-prompts", str(CKPT),
                    "--artifacts-base-dir", str(art), "--checkpoint-name", f"fit{N}"]  # fmt: skip
        log = open(OUT / f"shard{i}_r{r}.log", "w")  # noqa: SIM115 (closed when the process ends)
        p = subprocess.Popen(
            args, cwd=JPP, env={**ENV, "CUDA_VISIBLE_DEVICES": str(i)}, stdout=log, stderr=subprocess.STDOUT
        )
        procs[i] = (p, art, time.time(), log, r)
        status["steps"].append({"step": f"shard{i}", "rows": r, "launched_s": round(time.time() - T0)})
        save("RUNNING", at="shards")

    for i in range(SHARDS):
        launch(i)
    done: set[int] = set()
    while len(done) < SHARDS:
        time.sleep(30)
        if time.time() - T0 > LIMIT_S:
            for p, *_ in procs.values():
                p.kill()
            stop("ABORT_TIME", at="shards")
        for i, (p, art, t_start, log, r) in list(procs.items()):
            if i in done:
                continue
            rc = p.poll()
            if rc is None:  # the slow rule: no new checkpoint within CKPT x SLOW_S (plus the model load at first)
                last = newest(art) if art.exists() else 0.0
                quiet = time.time() - max(last, t_start + LOAD_S)
                if quiet > CKPT * SLOW_S:
                    for q, *_ in procs.values():
                        q.kill()
                    stop("ABORT_SLOW", at=f"shard{i}", rows=r, quiet_s=round(quiet))
                continue
            log.close()
            text = (OUT / f"shard{i}_r{r}.log").read_text(errors="replace")
            if rc == 0:
                done.add(i)
                status["steps"].append(
                    {"step": f"shard{i}", "rows": r, "seconds": round(time.time() - t_start), "exit": 0}
                )
                save("RUNNING", at="shards")
            elif "OutOfMemoryError" in text or "CUDA out of memory" in text:
                if rows[i] + 1 >= len(ROWS):
                    for q, *_ in procs.values():
                        q.kill()
                    stop("ABORT_OOM", at=f"shard{i}", rows=r)
                rows[i] += 1
                launch(i)
            else:
                for q, *_ in procs.values():
                    q.kill()
                stop("FAIL", at=f"shard{i}", rows=r, exit=rc)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    save("RUNNING", at="router")
    run("router", [*C, "fit-router", "--hf-model-name", MODEL, "--layers", LAYERS, "--num-prompts", str(N), "--skip-first-n-positions", "16", "--max-seq-len", "128", "--seed", "0", "--out", str(OUT / "router.pt")])  # fmt: skip
    shards()
    dirs = [str(sorted(OUT.glob(f"artifacts_s{i}_r*/*/fit{N}/shard{i}of{SHARDS}"))[-1]) for i in range(SHARDS)]
    run("merge", [*C, "merge-experts", "--checkpoint-dirs", *dirs, "--out", str(OUT / "experts.pt"), "--pooled-lens-out", str(OUT / "pooled_lens.pt")])  # fmt: skip
    grade = str(W / "bridge-jspace" / "scripts" / "lens_fit" / "jpp_grade.py")
    run("grade", ["uv", "run", "--no-sync", "python", grade, MODEL, LAYERS, str(OUT / "model_correctness.csv")])
    lens = OUT / "Qwen3-32B_jpp_lens.pt"
    run("fit_weights", [*C, "fit-weights", "--hf-model-name", MODEL, "--layers", LAYERS, "--experts", str(OUT / "experts.pt"), "--items", "fit:0", "--correctness-csv", str(OUT / "model_correctness.csv"), "--cache-path", str(OUT / "readout_cache.pt"), "--out", str(lens)])  # fmt: skip
    run("evaluate", [*C, "evaluate", "--hf-model-name", MODEL, "--layers", LAYERS, "--lens", str(lens), str(OUT / "pooled_lens.pt"), "--items", "held-out:0", "--correctness-csv", str(OUT / "model_correctness.csv"), "--out", str(OUT / "eval_ranks.csv")])  # fmt: skip
    export = OUT / "export" / "Qwen3-32B_jpp_lens.pt"
    export.parent.mkdir(exist_ok=True)
    note = (f"J++ for {MODEL}: safety-research/jpp_lens@93f02cd, {N} WikiText prompts x 128 tokens ({SHARDS} shards x "
            f"{N // SHARDS}, one router, seed 0), skip 16, target = the last block, rlens LRP, 8 experts, source layers "
            f"16-51; fit {time.strftime('%Y-%m-%d')} on 2x H200")  # fmt: skip
    run("export", ["uv", "run", "--no-sync", "python", str(W / "bridge-jspace" / "scripts" / "lens_fit" / "export_jpp_lens.py"),
                   str(lens), str(export), note])  # fmt: skip
    sha = subprocess.run(["sha256sum", str(export)], capture_output=True, text=True, check=True).stdout.split()[0]
    stop("DONE", lens=str(export), sha256=sha, note=note)


if __name__ == "__main__":
    main()
