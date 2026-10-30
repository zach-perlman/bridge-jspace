"""Inventory of scripts/ and results/ (Dan 26 Oct ~13:40): every file under scripts/ and every run dir under results/
classified as current / superseded / legacy / unknown. Generated, rerunnable, read-only; nothing is moved.

current     results: a run of a view in docs/review_views.yaml (any status), a run a README number is sourced from
            (docs/x0_numbers.json) or that the README links, or a run named in a current run's manifest.json (its
            inputs), closed transitively. scripts: the script that wrote a current run (its EXP / RESULTS name, or named
            in the command of the job spec that ran it), the README chain (README_CHAIN), the review tools, and every
            script these import, directly or not (a static ast import graph).
superseded  a view's `superseded` run, or an older version of a current run in the same experiment (the current run's
            name is this one's plus _r2 / _r3 / _g75 / _v2), with superseded_by.
legacy      neither of the above, not cited by the README, and pre-pivot: the name matches a pre-pivot pattern
            (exp01-exp23, pointer_*, d1-d5, suite_*, ...) or the last commit is on or before 23 Oct (Dan: pre-pivot = 19-23 Oct).
unknown     anything else: listed for Dan, not guessed.

uv run python scripts/inventory.py        # writes docs/inventory.md
"""

from __future__ import annotations

import ast
import collections
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "inventory.md"
README_PAGE = REPO / "docs" / "depth" / "README.md"  # the built README (the root README.md is an index since the merge)
# scripts that write what the README shows: the page, docs/x0_numbers.json + docs/x0_details.md, figures/depth/
README_CHAIN = ("scripts/readme_build.py", "scripts/x0_details.py", "scripts/readme_story_figures.py")
REVIEW_TOOLS = ("scripts/review.py", "scripts/inventory.py")
LEGACY_NAME = re.compile(
    r"^(exp\d\d|pointer_|alias_pointer|code_pointer|d[1-5][a-z]?_|suite_|quick_|phase\d|recovery_)"
)
PIVOT_LAST_DAY = "2026-10-23"
SUPERSEDING_SUFFIXES = ("_r2", "_r3", "_g75", "_v2")


def git_dates() -> dict[str, str]:
    """Path -> the date of the last commit that touched it (one git log pass)."""
    log = subprocess.run(["git", "log", "--format=@%cs", "--name-only", "--", "scripts", "results"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout  # fmt: skip
    dates, day = {}, ""
    for line in log.splitlines():
        if line.startswith("@"):
            day = line[1:]
        elif line and line not in dates:
            dates[line] = day
    return dates


def last_date(path: str, dates: dict[str, str]) -> str:
    if path in dates:
        return dates[path]
    hits = [d for p, d in dates.items() if p.startswith(path + "/")]
    return max(hits) if hits else "uncommitted"


def run_dirs() -> list[str]:
    """results/<exp>/<run> dirs, and results/<exp> dirs that hold no run dirs."""
    out = []
    for exp in sorted(p for p in (REPO / "results").iterdir() if p.is_dir()):
        subs = sorted(p for p in exp.iterdir() if p.is_dir())
        out += [str(p.relative_to(REPO)) for p in subs] if subs else [str(exp.relative_to(REPO))]
    return out


def run_of(path: str) -> str | None:
    m = re.match(r"(results/[^/]+/[^/]+)", path)
    return m.group(1) if m else None


def readme_citations(nums: dict) -> dict[str, set[str]]:
    """Run dir -> README sections citing it (through {{num|key}} markers and direct links)."""
    cites: dict[str, set[str]] = collections.defaultdict(set)
    section = "top"
    for line in (REPO / "docs" / "README.template.md").read_text().splitlines():
        if line.startswith("## "):
            section = line[3:].split(".")[0] if line[3].isdigit() else line[3:]
        for key in re.findall(r"\{\{num\|([^}]+)\}\}", line):
            run = run_of(nums.get(key, {}).get("source", ""))
            if run:
                cites[run].add(f"README {section}")
        for path in re.findall(r"\((results/[^)\s]+|scripts/[^)\s]+)\)", line):
            cites[run_of(path) or path].add(f"README {section}")
    return cites


def manifest_inputs(run: str, names: dict[str, str]) -> set[str]:
    """Other runs named in a run's manifest.json (by run name or path)."""
    f = REPO / run / "manifest.json"
    if not f.exists():
        return set()
    found = set()
    for s in re.findall(r'"([^"]+)"', f.read_text()):
        s = s.removeprefix("results/").rstrip("/")
        if "/" in s and f"results/{s}" in names.values():
            found.add(f"results/{s}")
        elif "_" in s and s in names and names[s] != run:  # a bare run name: unique and not a generic word like "gate"
            found.add(names[s])
    return found


def module_map() -> dict[str, str]:
    """Dotted module name (scripts.x, scripts.figs.common) -> path, for every .py under scripts/."""
    out = {}
    for p in (REPO / "scripts").rglob("*.py"):
        rel = p.relative_to(REPO).with_suffix("")
        parts = list(rel.parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
        out[".".join(parts)] = str(p.relative_to(REPO))
    return out


def imports_of(path: str, modules: dict[str, str]) -> set[str]:
    """The scripts/ files a .py file imports (any depth of the tree, lazy imports included)."""
    try:
        tree = ast.parse((REPO / path).read_text())
    except (SyntaxError, UnicodeDecodeError):
        return set()
    pkg = ".".join(Path(path).with_suffix("").parts[:-1])
    found = set()
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                up = pkg.split(".")[: len(pkg.split(".")) - node.level + 1]
                base = ".".join([*up, base] if base else up)
            names = [base] + [f"{base}.{a.name}" for a in node.names]
        for n in names:
            if n in modules and modules[n] != path:
                found.add(modules[n])
    return found


def producers(current_runs: set[str], modules: dict[str, str]) -> dict[str, set[str]]:
    """Script -> the current runs it wrote: runs of its own results dir (a module-level EXP = "..." or RESULTS =
    pins.RESULTS_DIR / "...", else its file name), or a run named by --name in the same command segment of a job spec
    as the script (a wrapper like muse_step.sh: the run's name in its segment)."""
    exp_of_script = {}
    for path in modules.values():
        text = (REPO / path).read_text(errors="ignore")
        m = re.search(r'^EXP\s*=\s*"([^"]+)"', text, re.M) or re.search(
            r'^RESULTS\s*=\s*pins\.RESULTS_DIR\s*/\s*"([^"]+)"', text, re.M
        )
        exp_of_script[path] = m.group(1) if m else Path(path).stem
    out: dict[str, set[str]] = collections.defaultdict(set)
    for path, exp in exp_of_script.items():
        out[path] |= {r for r in current_runs if r.split("/")[1] == exp}
    for spec in (REPO / "jobs").rglob("*.yaml"):
        for seg in re.split(r"&&|;|\|\||\n\s*\n", spec.read_text(errors="ignore")):
            scripts = [s for s in re.findall(r"scripts/[\w./-]+\.(?:py|sh)", seg) if (REPO / s).exists()]
            named = set(re.findall(r"--name\s+([\w.-]+)", seg)) | set(re.findall(r"\.sh\s+[\w-]+\s+([\w.-]+)", seg))
            for s in scripts:
                exp = exp_of_script.get(s)
                out[s] |= {
                    r
                    for r in current_runs
                    if r.split("/")[-1] in named and (s.endswith(".sh") or r.split("/")[1] == exp)
                }
    return out


def readme_links(page: Path = README_PAGE) -> set[str]:
    """The README's local link targets under docs/ and figures/, as paths from the repo root (the built page sits in
    docs/depth/ since the merge into main, so its links are relative to that folder)."""
    base = page.parent.relative_to(REPO)
    links = re.findall(r"\]\(([^)\s]+\.\w+)\)", page.read_text())
    rel = {os.path.normpath(base / t) for t in links if not re.match(r"[a-z][a-z0-9+.-]*:", t) and t[0] not in "#/"}
    return {Path(r).as_posix() for r in rel if r.startswith(("docs/", "figures/"))}


def readme_writers(files: list[str]) -> dict[str, set[str]]:
    """Script -> the README link targets (docs/, figures/) it names: by full path, else by the file's name."""
    targets = readme_links()
    texts = {f: (REPO / f).read_text(errors="ignore") for f in files if f.endswith(".py") and f not in REVIEW_TOOLS}
    out: dict[str, set[str]] = collections.defaultdict(set)
    for t in targets:
        hits = [f for f, s in texts.items() if t in s] or [f for f, s in texts.items() if Path(t).name in s]
        for f in hits:
            out[f].add(t)
    return out


def makefile_scripts() -> set[str]:
    text = (REPO / "Makefile").read_text()
    found = set(re.findall(r"scripts/[\w./-]+\.(?:py|sh)", text))
    found |= {f"scripts/{m}.py" for m in re.findall(r"-m scripts\.(\w+)", text)}
    return {f for f in found if (REPO / f).exists()}


def classify() -> tuple[list[dict], dict]:
    views = yaml.safe_load((REPO / "docs" / "review_views.yaml").read_text())["views"]
    nums = json.loads((REPO / "docs" / "x0_numbers.json").read_text())
    dates = git_dates()
    runs = run_dirs()
    grid = re.match(r"<!-- grid: (results/[^ ]+) -->", (REPO / "docs" / "README.template.md").read_text())
    base = collections.Counter(r.split("/")[-1] for r in runs if r.count("/") == 2)
    names = {r.split("/", 2)[2]: r for r in runs if r.count("/") == 2 and base[r.split("/")[-1]] == 1}
    names.update({r.split("/", 1)[1]: r for r in runs})  # exp/run as named in manifests
    cited = readme_citations(nums)
    if grid:
        cited[grid.group(1)].add("README build (the grid pinned in the template)")
    by_view: dict[str, set[str]] = collections.defaultdict(set)
    superseded: dict[str, str] = {}
    for v in views:
        for model, dirs in v.get("runs", {}).items():
            for d in dirs:
                by_view[d].add(v["id"])
            for d in v.get("superseded", {}).get(model, []):
                superseded[d] = dirs[0]
                by_view[d].add(f"{v['id']} (superseded)")
        for d in v.get("cases_from", {}).values():
            by_view[d].add(f"{v['id']} (prompts)")
        for d in v.get("analyses", []):  # analysis outputs over the view's runs: every run dir under the path
            for r in runs:
                if fnmatch.fnmatch(r, d) or r.startswith(d.rstrip("/") + "/"):
                    by_view[r].add(f"{v['id']} (analysis)")
    current = {r for r in runs if (r in by_view and r not in superseded) or r in cited}
    sourced = {r for e in nums.values() if (r := run_of(e.get("source", ""))) and r in runs}
    current |= sourced
    todo = list(current)
    while todo:
        for dep in manifest_inputs(todo.pop(), names):
            if dep not in current and dep not in superseded:
                current.add(dep)
                todo.append(dep)
    for r in runs:
        if r in current or r in superseded:
            continue
        exp, name = r.split("/")[1], r.split("/")[-1]
        newer = [
            c
            for c in current
            if c.split("/")[1] == exp and c.split("/")[-1] in {name + s for s in SUPERSEDING_SUFFIXES}
        ]
        if newer:
            superseded[r] = sorted(newer)[0]

    modules = module_map()
    wrote = producers(current, modules)
    files = sorted(str(p.relative_to(REPO)) for p in (REPO / "scripts").rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts)  # fmt: skip
    links = readme_writers(files)
    tooling = makefile_scripts()
    seeds = {s for s, rs in wrote.items() if rs} | {s for s in (*README_CHAIN, *REVIEW_TOOLS) if (REPO / s).exists()}
    seeds |= set(links)
    current_scripts, todo = set(seeds), list(seeds)
    graph = {f: imports_of(f, modules) for f in files if f.endswith(".py")}
    while todo:
        for dep in graph.get(todo.pop(), ()):
            if dep not in current_scripts:
                current_scripts.add(dep)
                todo.append(dep)
    importers = collections.defaultdict(set)
    for f, deps in graph.items():
        for d in deps:
            importers[d].add(f)

    rows = []
    for path in runs + files:
        is_script = path.startswith("scripts/")
        stem = Path(path).name if not is_script else Path(path).parts[1].removesuffix(".py").removesuffix(".sh")
        exp = path.split("/")[1] if not is_script else stem
        date = last_date(path, dates)
        cites = sorted(by_view.get(path, set()) | cited.get(path, set())) if not is_script else []
        if is_script:
            if path in current_scripts:
                why = ("wrote " + ", ".join(sorted(r.split("/")[-1] for r in wrote[path]))[:120]) if wrote.get(path) else (
                    "README chain" if path in README_CHAIN else "review tools" if path in REVIEW_TOOLS else
                    "writes " + ", ".join(sorted(links[path]))[:120] + " (linked by the README)" if path in links else
                    "imported by " + ", ".join(sorted(Path(i).name for i in importers[path] if i in current_scripts))[:120])  # fmt: skip
                cls, by = "current", ""
            elif path in tooling:
                cls, by, why = "unknown", "", "tooling: named in the Makefile"
            elif LEGACY_NAME.match(stem) or date <= PIVOT_LAST_DAY:
                cls, by, why = "legacy", "", "pre-pivot name" if LEGACY_NAME.match(stem) else f"last commit {date}"
            else:
                cls, by, why = "unknown", "", ""
        elif path in superseded:
            cls, by, why = "superseded", superseded[path], ""
        elif path in current:
            cls, by = "current", ""
            why = (
                ""
                if cites
                else "a docs/x0_numbers.json source"
                if path in sourced
                else "input of a current run (its manifest)"
            )
        elif not any(c.startswith("README") for c in cites) and (LEGACY_NAME.match(exp) or date <= PIVOT_LAST_DAY):
            cls, by, why = "legacy", "", "pre-pivot name" if LEGACY_NAME.match(exp) else f"last commit {date}"
        else:
            cls, by, why = "unknown", "", ""
        rows.append(
            {"path": path, "class": cls, "superseded_by": by, "cited_by": cites, "last_commit": date, "why": why}
        )
    counts = collections.Counter((r["path"].split("/")[0], r["class"]) for r in rows)
    return rows, counts


def main() -> None:
    rows, counts = classify()
    lines = ["# Inventory of scripts/ and results/", "",
             "Generated by `uv run python scripts/inventory.py` from docs/review_views.yaml, docs/x0_numbers.json, the README "
             "template, run manifests, job specs and a static import graph; rerun it after any change. Nothing is moved: "
             "pre-pivot experiments are kept and labelled legacy. Rules: the docstring of scripts/inventory.py.", "",
             "| | current | superseded | legacy | unknown |", "|---|---|---|---|---|"]  # fmt: skip
    for top in ("scripts", "results"):
        lines.append(
            f"| {top} | "
            + " | ".join(str(counts[(top, c)]) for c in ("current", "superseded", "legacy", "unknown"))
            + " |"
        )
    for cls in ("unknown", "current", "superseded", "legacy"):
        mine = [r for r in rows if r["class"] == cls]
        lines += [
            "",
            f"## {cls} ({len(mine)})",
            "",
            "| path | superseded by | cited by | last commit | note |",
            "|---|---|---|---|---|",
        ]
        for r in mine:
            lines.append(
                f"| {r['path']} | {r['superseded_by']} | {'; '.join(r['cited_by'])} | {r['last_commit']} | {r['why']} |"
            )
    OUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT.relative_to(REPO)}:", dict(counts))


if __name__ == "__main__":
    sys.exit(main())
