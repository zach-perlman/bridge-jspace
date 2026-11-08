"""Measure the README's Reproduce tiers in fresh clones and write the values to data/figures/reproduce.csv by key.

Each tier is timed in its own fresh sparse clone of the public repo (a temporary directory outside this checkout,
removed at the end): wall time of each step, disk of the checkout (`du -sk`, the uv env counted apart) and the
machine. The sparse sets are TIERS below (`paths <tier>` prints one, for `git sparse-checkout set`).

  read   git clone --filter=blob:none --sparse, then sparse-checkout set docs figures data/figures; every local link of
         README.md checked for existence.
  tier1  the tier1 set, uv sync, make readme; then which tracked files differ from the commit, and how many changed
         words are not a commit hash (a rebuild stamps its own commit, "Built at <hash>"). The .git of this clone is
         large: provenance_counts.py's `git archive <rev> scripts src ...` makes a blob:none clone fetch nearly every
         blob of that commit, results/ included (seen with GIT_TRACE, 8 Nov).
  tier2  the tier2 set, uv sync, scripts/verify_headlines.py as is (exit code); then each of its checks on its own
         (`each` below), so a missing run file fails one check instead of the whole script.
  tier3  `make run` on a GPU box: not re-run; the memory needs are quoted from DEVELOPER.md.

  uv run python scripts/measure_reproduce.py                 # all tiers, uv's package cache as it is
  uv run python scripts/measure_reproduce.py --cold-uv-cache  # uv sync into an empty package cache (downloads)
  uv run --project <clone> python scripts/measure_reproduce.py each <clone>   # verify_headlines check by check
  python3 scripts/measure_reproduce.py paths tier1                # a tier's sparse set (stdlib only)
"""

from __future__ import annotations

import argparse
import ast
import csv
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "data/figures/reproduce.csv"
LINK = re.compile(r"\]\(([^)\s]+)\)|src=\"([^\"]+)\"")
HASH = re.compile(r"[0-9a-f]{7,40}")
SELF = "scripts/measure_reproduce.py"


# The sparse-checkout set of each tier. read: the README with its figures and docs. tier1: what `make readme` reads,
# found by tracing every file the recipe's Python processes open (an audit hook), widening the set until the recipe ran,
# then adding the run folders scripts/provenance_counts.py resolves (it checks manifests with exists(), which a trace
# misses) until its counts and every output equalled the committed ones. tier2: what scripts/verify_headlines.py reads,
# traced the same way; 13 run folders it also reads are in no commit and are left out. In tier2, data/figures brings
# data/'s top-level files (a cone's parent level), which verify_headlines.py reads.
TIERS: dict[str, list[str]] = {
    "read": [
        "docs",
        "figures",
        "data/figures",
    ],
    "tier1": [
        "data/figures",
        "data/tasks_v2/jsuite_v2_test_chat",
        "docs",
        "examples",
        "figures",
        "jobs",
        "predictions",
        "runs",
        "scripts",
        "src",
        "tests",
        "verification",
        "results/ablate_v2/c1_v2",
        "results/ablate_v2/dsv4f_jsuite_v2_test_chat_ko_cand2_L18-23_dose54_s150_v1",
        "results/ablate_v2/dsv4f_jsuite_v2_test_chat_ko_cand2_L18-23_v1",
        "results/ablate_v2/fresh2_ko_v1",
        "results/ablate_v2/fresh3_ko_v1",
        "results/ablate_v2/full2_ko_v1",
        "results/ablate_v2/jsuite_score",
        "results/ablate_v2/jsuite_v2_test_chat_ko_cand2_v1",
        "results/ablate_v2/jsuite_v2_test_chat_threehop_ko_cand2_v1",
        "results/ablate_v2/jsuite_v2nb_test_chat_threehop_ko_cand2_v1",
        "results/ablate_v2/jsuite_v4_test_chat_ko41_cand2_v1",
        "results/ablate_v2/jsuite_v4_test_chat_ko41_posfinal_cand2_v1",
        "results/ablate_v2/jsuite2_score",
        "results/ablate_v2/min14_jsuite_v2_test_chat_ko_cand2_v1",
        "results/ablate_v2/muse30_jsuite_v2_test_chat_ko_cand2_v1",
        "results/ablate_v2/natplus_split",
        "results/ablate_v2/natplus_v1_chat_ko_cand2_v1",
        "results/ablate_v2/natural_v1_chat_ko_v1",
        "results/ablate_v2/natural_v2_chat_ko_v1",
        "results/ablate_v2/natural_v3_chat_ko_v1",
        "results/ablate_v2/nem35b_jsuite_v2_test_chat_ko_cand2_L42-53_dose54_s150_v1",
        "results/ablate_v2/nem35l_jsuite_v2_test_chat_ko_cand2_v1",
        "results/ablate_v2/nem35l_natplus_v1_chat_ko_cand2_v1",
        "results/ablate_v2/nn_ko_read",
        "results/ablate_v2/olmo32_jsuite_v2_test_qa_ko_cand2_L12-20_v1",
        "results/ablate_v2/qwen35_122b_jsuite_v2_test_chat_ko_cand2_v1",
        "results/ablate_v2/qwen35_9b_fresh2_ko_v1",
        "results/ablate_v2/qwen35_9b_fresh3_ko_v1",
        "results/ablate_v2/qwen35_9b_full2_ko_v1",
        "results/ablate_v2/qwen35_9b_jsuite_v2_test_chat_ko_cand2_v1",
        "results/ablate_v2/qwen35_9b_jsuite_v2_test_chat_threehop_ko_cand2_v1",
        "results/ablate_v2/qwen35_9b_natplus_v1_chat_ko_cand2_v1",
        "results/ablate_v2/qwen35_9b_natural_v1_chat_ko_v1",
        "results/ablate_v2/qwen35_9b_natural_v2_chat_ko_v1",
        "results/ablate_v2/qwen35_9b_natural_v3_chat_ko_v1",
        "results/ablate_v2/qwen35_9bb_jsuite_v1_facts_test_qa_ko_cand2_v1",
        "results/ablate_v2/qwen35_9boj_jsuite_v1_facts_test_qa_ko_cand2_v1",
        "results/ablate_v2/soft_score",
        "results/cross_model/20261023T210238Z",
        "results/jswap/olmo32_jswap_v2_v1",
        "results/removal_textloss/gemma4itf_sink_textloss_v1",
        "results/removal_textloss/gptoss20_textloss_top_v1",
        "results/removal_textloss/kol1_textloss_top_l15_35_v1",
        "results/sd_necessity/nem35l_sd59_ko_test_v1",
        "results/sd_necessity/nem35l_sd65_ko_test_v1",
        "results/sd_necessity/nn_sd_read",
        "results/sd_necessity/qwen35_9b_sd59_ko_test_v1",
        "results/sd_necessity/qwen35_9b_sd65_ko_test_v1",
        "results/sd_necessity/sd59_ko_test_v1",
        "results/sd_necessity/sd65_ko_test_v1",
        "results/sd_necessity/sd67_ko_test_v1",
        "results/x0_necessity/x0_necessity_27b_chat",
        "results/x0_probe/muse30b_x0_probe_v4",
        "results/x0_probe/nem35l_x52_probe",
        "results/x0_probe/qwen35_122b_x0_probe_v4",
        "results/x0_probe/qwen35_9b_x0_probe_v4",
        "results/x0_probe/x0_probe_v4_27b",
        "results/x47_six/x52_six-20261029T004919Z",
        "results/x47_six/x52_six-20261029T231821Z",
        "results/x47_verbal/summary-20261028T033646Z",
        "results/x47_verbal/summary-20261029T005548Z",
        "results/x47_verbal/summary-20261029T180530Z",
        "results/x47_zero/x47_5-20261028T113106Z",
        "results/x47_zero/x52_zero-20261029T032056Z",
        "results/x47_zero/x52_zero-20261029T183120Z",
        "results/x49_das_pos/verdict-20261028T154510Z",
        "results/x50_zach/x52_z1-20261029T013035Z",
        "results/x50_zach/x52_z1-20261029T215701Z",
        "results/x50_zach/z1-20261028T161649Z",
        "results/x51_jread/muse30_x51_10",
        "results/x51_jread/nem35l_x52_jread",
        "results/x51_jread/qwen35_122b_x51_10",
        "results/x51_jread/qwen35_9b_x51_10",
        "results/x51_jread/read-muse30_x51_10-20261028T185636Z",
        "results/x51_jread/read-nem35l_x52_jread-20261029T005704Z",
        "results/x51_jread/read-qwen35_122b_x51_10-20261029T140039Z",
        "results/x51_jread/read-qwen35_9b_x51_10-20261028T185634Z",
        "results/x51_jread/read-x51_10_27b-20261028T185638Z",
        "results/x51_jread/x51_10_27b",
        "results/x53_2x2/x53_2x2-20261029T113335Z",
        "results/x6_routes/muse30b_x6_routes",
        "results/x6_routes/nem35l_x52_routes",
        "results/x6_routes/qwen35_122b_x6_routes_g75",
        "results/x6_routes/qwen35_9b_x6_routes",
        "results/x6_routes/x6_routes_27b",
        "results/x8_write/muse30b_x8_write",
        "results/x8_write/nem35l_x52_write",
        "results/x8_write/qwen35_122b_x8_write_g75",
        "results/x8_write/qwen35_9b_x8_write",
        "results/x8_write/x8_write_27b",
        "results/z1p_checks/20261030T222158Z",
    ],
    "tier2": [
        "data/figures",
        "scripts",
        "src",
        "results/exp02_swaps/main_v4_jlens",
        "results/exp02_swaps/main_v4_jlens_pos-cue",
        "results/exp02_swaps/main_v4_jpp",
        "results/exp02_swaps/main_v4_jpp_pos-cue",
        "results/exp02_swaps/main_v4_jpp_pos-prev",
        "results/exp02_swaps/matched_v4_jlens",
        "results/exp02_swaps/matched_v4_jpp",
        "results/exp03_brew_swaps/fresh_steer",
        "results/exp03_brew_swaps/swap_amp",
        "results/exp04_brew_patch/parts_window",
        "results/exp04_brew_patch/parts_window_fresh",
        "results/exp04_brew_patch/patch_map",
        "results/exp04_brew_patch/patch_map_fresh",
        "results/exp04_brew_patch/positions_window",
        "results/exp06_sigma_writes/sigma_v1",
        "results/exp07_step_code/code_v1",
        "results/exp08_brew_read/read_v1",
        "results/exp09_bind_recall/map_lookup_v2",
        "results/exp09_bind_recall/map_v1",
        "results/exp09_bind_recall/parts_lookup_v2",
        "results/exp09_bind_recall/parts_rl_v1",
        "results/exp09_bind_recall/parts_v1",
        "results/exp09_bind_recall/swaps_v1",
        "results/exp10_lens_sanity/20261013-205936",
        "results/exp11_bridge_vs_answer_by_layer/20261014-092835",
        "results/exp11_bridge_vs_answer_by_layer/20261015-100110",
        "results/exp11_bridge_vs_answer_by_layer/20261015-100426",
        "results/exp12_position_map/20261015-100735",
        "results/exp14_cue_answer_swaps/20261015-111137",
        "results/exp14_cue_answer_swaps/20261015-114825",
        "results/exp15_oracle_lens/20261015-123226",
        "results/exp15_oracle_lens/20261015-134316",
        "results/exp15_oracle_lens/20261015-140424",
        "results/exp16_nla/20261015-144540",
        "results/exp18_brew_verbalizers/20261015-205549",
        "results/exp18_brew_verbalizers/20261015-230148",
        "results/exp20_competence/v1",
    ],
}


def https(url: str) -> str:
    m = re.match(r"git@([^:]+):(.+)", url)
    url = f"https://{m.group(1)}/{m.group(2)}" if m else url
    return url if url.endswith(".git") else url + ".git"


def run(cmd: list[str] | str, cwd: Path, env: dict[str, str]) -> tuple[float, subprocess.CompletedProcess]:
    t = time.monotonic()
    p = subprocess.run(cmd, cwd=cwd, env=env, shell=isinstance(cmd, str), capture_output=True, text=True)
    return time.monotonic() - t, p


def du_mb(path: Path, *exclude: str) -> float:
    def kb(p: Path) -> int:
        return int(subprocess.run(["du", "-sk", p], capture_output=True, text=True, check=True).stdout.split()[0])

    return (kb(path) - sum(kb(path / x) for x in exclude if (path / x).exists())) / 1024


def clone(url: str, branch: str, dest: Path, paths: list[str], env: dict[str, str]) -> float:
    t1, p = run(
        ["git", "clone", "-q", "--filter=blob:none", "--sparse", "-b", branch, url, str(dest)], dest.parent, env
    )
    assert p.returncode == 0, p.stderr
    t2, p = run(["git", "sparse-checkout", "set", *paths], dest, env)
    assert p.returncode == 0, p.stderr
    return t1 + t2


def readme_links(root: Path) -> tuple[int, list[str]]:
    targets = set()
    for a, b in LINK.findall((root / "README.md").read_text()):
        t = (a or b).split("#")[0]
        if t and "://" not in t and not t.startswith("mailto:"):
            targets.add(os.path.normpath(t))
    return len(targets), sorted(t for t in targets if not (root / t).exists())


def hardware() -> dict[str, str]:
    if sys.platform == "darwin":
        cpu = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout
        mem = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout)
        osname = f"macOS {platform.mac_ver()[0]}"
    else:
        cpu = next(
            (ln.split(":", 1)[1] for ln in Path("/proc/cpuinfo").read_text().splitlines() if "model name" in ln), ""
        )
        mem = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        osname = f"{platform.system()} {platform.release()}"
    return {"cpu": cpu.strip(), "ram_gb": f"{mem / 2**30:.0f}", "cores": str(os.cpu_count()), "os": osname}


def each(root: Path) -> None:
    """scripts/verify_headlines.py's checks, each evaluated on its own: prints OK / DIFF / MISSING per check and a
    SUMMARY line. The script's check list is rewritten so that each value is computed lazily (a lambda)."""
    path = root / "scripts/verify_headlines.py"
    tree = ast.parse(path.read_text())
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    checks = main.body[0]
    assert isinstance(checks, ast.Assign)
    assert isinstance(checks.value, ast.List)
    for t in checks.value.elts:
        names: list[str] = []
        if isinstance(t, ast.Starred):  # a generator of checks: its loop names become the lambda's defaults
            assert isinstance(t.value, ast.GeneratorExp)
            loop = {n.id for g in t.value.generators for n in ast.walk(g.target) if isinstance(n, ast.Name)}
            t = t.value.elt
            names = sorted(loop & {n.id for n in ast.walk(t) if isinstance(n, ast.Name)})
        assert isinstance(t, ast.Tuple)
        args = ast.arguments(
            [], [ast.arg(n) for n in names], None, [], [], None, [ast.Name(n, ast.Load()) for n in names]
        )
        t.elts[2] = ast.Lambda(args=args, body=t.elts[2])
    main.body = [checks, ast.Return(ast.Name("checks", ast.Load()))]
    mod = types.ModuleType("verify_headlines")
    mod.__file__ = str(path)
    exec(compile(ast.fix_missing_locations(tree), str(path), "exec"), mod.__dict__)
    ok = diff = err = 0
    missing: set[str] = set()
    for exp, what, value, claimed in mod.main():
        try:
            got = value()
        except FileNotFoundError as e:
            err += 1
            missing.add(os.path.relpath(str(e.filename), root))
            print(f"MISSING {exp}  {what}: {os.path.relpath(str(e.filename), root)}")
            continue
        good = round(got, 2) == round(claimed, 2) if isinstance(claimed, float) else got == claimed
        ok, diff = ok + good, diff + (not good)
        print(f"{'OK  ' if good else 'DIFF'} {exp}  {what}  recomputed {got}  README {claimed}")
    print(f"SUMMARY checks={ok + diff + err} ok={ok} diff={diff} missing={err} missing_files={len(missing)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", default="measure", choices=["measure", "each", "paths"])
    ap.add_argument("root", nargs="?", help="each: the checkout whose verify_headlines.py to run; paths: the tier")
    ap.add_argument("--url", default=None, help="default: origin, as https")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--workdir", default=None, help="parent of the fresh clones (default: a new temporary directory)")
    ap.add_argument("--cold-uv-cache", action="store_true", help="uv sync into an empty package cache")
    ap.add_argument("--keep", action="store_true", help="keep the clones")
    a = ap.parse_args()
    if a.cmd == "each":
        return each(Path(a.root).resolve())
    if a.cmd == "paths":
        return print(" ".join(TIERS[a.root]))

    url = a.url or https(subprocess.run(["git", "remote", "get-url", "origin"], cwd=REPO, capture_output=True,
                                        text=True, check=True).stdout.strip())  # fmt: skip
    work = Path(a.workdir or tempfile.mkdtemp(prefix="bj-reproduce-")).resolve()
    work.mkdir(parents=True, exist_ok=True)
    assert REPO not in work.parents, "the clones go outside this checkout"
    env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "PYTHONPATH")}
    if a.cold_uv_cache:
        env["UV_CACHE_DIR"] = str(work / "uv-cache")
    sets, hw, rows = TIERS, hardware(), []
    when = time.strftime("%Y-%m-%d", time.gmtime())
    sync_how = "an empty uv package cache" if a.cold_uv_cache else "uv's package cache as it was (warm)"

    def row(key: str, value, unit: str, what: str) -> None:
        rows.append([key, value, unit, f"{SELF} ({when}): {what}"])
        print(f"{key:28} {value} {unit}", flush=True)

    def disk(tier: str, d: Path) -> None:
        row(f"repro.{tier}.files_mb", round(du_mb(d, ".git", ".venv")), "MB", f"du -sk of the {tier} checkout's files (no .git, no .venv)")  # fmt: skip
        row(f"repro.{tier}.git_mb", round(du_mb(d / ".git")), "MB", f"du -sk of the {tier} checkout's .git (partial clone: the blobs fetched)")  # fmt: skip
        if (d / ".venv").exists():
            row(f"repro.{tier}.venv_mb", round(du_mb(d / ".venv")), "MB", f"du -sk of the {tier} checkout's uv env (.venv)")  # fmt: skip

    for k, v in hw.items():
        row(f"repro.hw.{k}", v, "GB" if k == "ram_gb" else "text" if k in ("cpu", "os") else "count", "this machine")

    # read: the docs and figures only
    d = work / "read"
    t = clone(url, a.branch, d, sets["read"], env)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=d, capture_output=True, text=True).stdout.strip()
    row("repro.commit", commit[:8], "text", f"the commit measured ({a.branch} of {url})")
    n, dead = readme_links(d)
    row("repro.read.time_s", round(t), "s", "git clone --filter=blob:none --sparse + sparse-checkout set (read set)")
    disk("read", d)
    row("repro.read.links", n, "count", "README.md's local link targets")
    row(
        "repro.read.links_dead",
        len(dead),
        "count",
        "of those, missing from the read checkout: " + (" ".join(dead) or "none"),
    )

    # tier1: make readme from tracked numbers
    d = work / "tier1"
    t = clone(url, a.branch, d, sets["tier1"], env)
    ts, p = run(["uv", "sync", "-q"], d, env)
    assert p.returncode == 0, p.stderr
    tr, p = run(["make", "readme"], d, env)
    changed = run(["git", "status", "--porcelain", "--untracked-files=no"], d, env)[1].stdout.splitlines()
    words = run(["git", "diff", "--word-diff=porcelain"], d, env)[1].stdout.splitlines()
    words = [w[1:] for w in words if w[:1] in "+-" and w[:3] not in ("+++", "---")]
    other = [w for w in words if not HASH.fullmatch(w.strip())]  # a rebuild stamps its own commit ("Built at <hash>")
    nres = sum(1 for x in sets["tier1"] if x.startswith("results/"))
    row("repro.t1.clone_s", round(t), "s", "git clone + sparse-checkout set (tier1 set)")
    row("repro.t1.sync_s", round(ts), "s", f"uv sync, {sync_how}")
    row("repro.t1.readme_s", round(tr), "s", f"make readme (exit {p.returncode})")
    row("repro.t1.exit", p.returncode, "count", "make readme's exit code")
    row("repro.t1.changed", len(changed), "count", "tracked files differing from the commit after make readme: " + (" ".join(c[3:] for c in changed) or "none"))  # fmt: skip
    row("repro.t1.changed_other", len(other), "count", "changed words in them other than a commit hash (the build stamp)")  # fmt: skip
    disk("t1", d)
    row(
        "repro.t1.results_folders",
        nres,
        "count",
        "results/ folders in the tier1 set (TIERS in scripts/measure_reproduce.py)",
    )
    row("repro.t1.results_mb", round(du_mb(d / "results")), "MB", "du -sk of results/ in the tier1 checkout")
    if not a.keep:
        shutil.rmtree(d)  # tier1's checkout is the largest; free it before tier2

    # tier2: verify_headlines.py
    d = work / "tier2"
    t = clone(url, a.branch, d, sets["tier2"], env)
    ts, p = run(["uv", "sync", "-q"], d, env)
    assert p.returncode == 0, p.stderr
    tv, p = run(["uv", "run", "python", "scripts/verify_headlines.py"], d, env)
    err = (p.stderr.strip().splitlines() or [""])[-1].replace(f"{d}/", "")
    _, q = run(["uv", "run", "python", str(REPO / SELF), "each", str(d)], d, env)
    summ = dict(
        kv.split("=") for kv in next(ln for ln in q.stdout.splitlines() if ln.startswith("SUMMARY")).split()[1:]
    )
    nres = sum(1 for x in sets["tier2"] if x.startswith("results/"))
    row("repro.t2.clone_s", round(t), "s", "git clone + sparse-checkout set (tier2 set)")
    row("repro.t2.sync_s", round(ts), "s", f"uv sync, {sync_how}")
    row("repro.t2.verify_s", round(tv, 1), "s", "uv run python scripts/verify_headlines.py")
    row("repro.t2.exit", p.returncode, "count", "verify_headlines.py's exit code; last stderr line: " + err[:200])
    for k in ("checks", "ok", "diff", "missing", "missing_files"):
        row(f"repro.t2.{k}", summ[k], "count", f"{SELF} each: verify_headlines.py's checks one by one ({k})")
    disk("t2", d)
    row(
        "repro.t2.results_folders",
        nres,
        "count",
        "results/ folders in the tier2 set (TIERS in scripts/measure_reproduce.py)",
    )
    row("repro.t2.results_mb", round(du_mb(d / "results")), "MB", "du -sk of results/ in the tier2 checkout")

    # the whole results/ tree at that commit, for scale (sizes from this checkout's objects: no download)
    sizes = subprocess.run(["git", "ls-tree", "-r", "-l", commit, "results"], cwd=REPO, capture_output=True, text=True,
                           check=True).stdout.splitlines()  # fmt: skip
    row("repro.results_all_gb", round(sum(int(s.split()[3]) for s in sizes) / 1e9, 1), "GB", f"git ls-tree -r -l {commit[:8]} results: tracked bytes, uncompressed")  # fmt: skip
    row("repro.results_all_files", len(sizes), "count", f"git ls-tree -r {commit[:8]} results: tracked files")

    # tier3: quoted, not re-run
    row(
        "repro.t3.gpu_gb_27b",
        80,
        "GB",
        "DEVELOPER.md, GPU box: Qwen3.6-27B needs one 80 GB card; quoted, not re-run for this page",
    )
    row(
        "repro.t3.gpu_gb_4b",
        24,
        "GB",
        "DEVELOPER.md, GPU box: Qwen3.5-4B fits a 24 GB card; quoted, not re-run for this page",
    )

    if not a.keep:
        shutil.rmtree(work, ignore_errors=True)
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["key", "value", "unit", "source"])
        w.writerows(rows)
    print(f"wrote {OUT.relative_to(REPO)} ({len(rows)} keys)" + (f"; clones kept in {work}" if a.keep else ""))


if __name__ == "__main__":
    main()
