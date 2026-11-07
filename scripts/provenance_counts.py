"""Provenance of the runs the root README cites (Dan, 8 Nov, follow-up 7): every src comment in README.md is traced to
the run folders (manifest.json) its number comes from, directly (results/…, runs/…) or through a data file's
source column (docs/breadth/data.csv, data/figures/depth/data.csv, data/figures/writeup/data.csv); each manifest is read
for a git commit (40 hex digits under a commit/git/code key) and a lens sha256 (64 hex digits under a lens key). Also the
two counts of the 8 Nov fix to the manifest writers (G1, commit bd43870f): writers that now record their switches and
writers left out of the check (no model loaded). Written as keys to data/figures/provenance.csv for the README.

uv run python scripts/provenance_counts.py
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
README = REPO / "README.md"
OUT = REPO / "data/figures/provenance.csv"
DATA = {
    "docs/breadth/data.csv": "key",
    "data/figures/writeup/data.csv": "key",
    "data/figures/depth/data.csv": "quantity",
}
SRC = re.compile(r"<!-- src: ([^|]+?) \| (.+?) -->")
RUNPATH = re.compile(r"((?:results|runs)/[\w./-]+)")
HEX40, HEX64 = re.compile(r"\b[0-9a-f]{40}\b"), re.compile(r"\b[0-9a-f]{64}\b")
G1 = "bd43870f"


def data_sources() -> dict[str, dict[str, list[str]]]:
    out: dict[str, dict[str, list[str]]] = {}
    for path, keycol in DATA.items():
        with (REPO / path).open() as f:
            for r in csv.DictReader(f):
                out.setdefault(path, {}).setdefault(r[keycol].strip(), []).append(r.get("source", ""))
    return out


def run_dir(path: str) -> Path | None:
    """The run folder of a cited file: the nearest ancestor with manifest.json, or a sibling folder named after the
    file (a score file such as results/ablate_v2/jsuite2_score/<run>.json, or a read file <run>_noteNN.json)."""
    p = REPO / path
    for q in [p, *p.parents]:
        if q == REPO:
            break
        if (q / "manifest.json").exists():
            return q
    stem = p.stem
    for parent in p.parents[:3]:
        if not parent.exists():
            continue
        for d in parent.iterdir():
            if d.is_dir() and (d / "manifest.json").exists() and (stem == d.name or stem.startswith(d.name + "_")):
                return d
    return None


def read_file_runs(path: str) -> list[Path]:
    """A read file that names its runs ({"prefix": …, "runs": {arm: run name}}, as results/ablate_v2/nn_ko_read/*.json do):
    the run folders it read, next to its own folder."""
    p = REPO / path
    if p.suffix != ".json" or not p.exists():
        return []
    try:
        d = json.loads(p.read_text())
    except ValueError:
        return []
    if not isinstance(d, dict):
        return []
    names = (
        list(d["runs"].values())
        if isinstance(d.get("runs"), dict)
        else [d["run"]]
        if isinstance(d.get("run"), str)
        else []
    )
    prefix = d.get("prefix") or ""
    out = []
    for name in names:
        for base in (p.parent.parent, p.parent):
            q = base / f"{prefix}{name}"
            if (q / "manifest.json").exists():
                out.append(q)
                break
    return out


def has(manifest: dict, keyword: tuple[str, ...], pattern: re.Pattern) -> bool:
    def walk(d, keyhit: bool) -> bool:
        if isinstance(d, dict):
            return any(walk(v, keyhit or any(w in k.lower() for w in keyword)) for k, v in d.items())
        if isinstance(d, list):
            return any(walk(v, keyhit) for v in d)
        return keyhit and isinstance(d, str) and bool(pattern.search(d))

    return walk(manifest, False)


def g1_counts() -> tuple[int, int, int]:
    """At {G1}'s parent, the test's own scan (tests/test_run_switches.py manifest_writers, with that commit's LEFT_OUT
    and DELEGATES): the manifest writers that recorded no switches; and of those, how many {G1} made record them and
    how many it left out (no model loaded)."""
    import importlib.util
    import io
    import sys
    import tarfile
    import tempfile

    def missing_at(rev: str, root: Path) -> tuple[set[str], set[str]]:
        tar = subprocess.run(["git", "archive", rev, "scripts", "src", "tests/test_run_switches.py"], capture_output=True,
                             cwd=REPO, check=True).stdout  # fmt: skip
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            t.extractall(root, filter="data")
        spec = importlib.util.spec_from_file_location(f"t_{rev}", root / "tests/test_run_switches.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        mod.REPO = root
        writers = mod.manifest_writers()
        return (
            {w for w, ok in writers.items() if not ok and w not in mod.LEFT_OUT and w not in mod.DELEGATES},
            set(mod.LEFT_OUT),
        )

    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        before, _ = missing_at(f"{G1}^", Path(a))
        after, left_after = missing_at(G1, Path(b))
    left = len(before & left_after)
    return len(before), len(before - after) - left, left


def main() -> None:
    srcs = data_sources()
    cited: set[str] = set()
    for path, keys in SRC.findall(README.read_text()):
        path = path.strip()
        if path.startswith(("results/", "runs/")):
            cited.add(path)
        elif path in srcs:
            for key in (k.strip() for k in keys.split(";")):
                for source in srcs[path].get(key, []):
                    cited.update(RUNPATH.findall(source))
    runs, untraced = set(), set()
    for c in cited:
        found = [d for d in [run_dir(c), *read_file_runs(c)] if d]
        runs.update(found) if found else untraced.add(c)
    no_commit = no_lens = 0
    for d in runs:
        m = json.loads((d / "manifest.json").read_text())
        no_commit += not has(m, ("commit", "git", "code"), HEX40)
        no_lens += not has(m, ("lens",), HEX64)
    unrecorded, switches, left_out = g1_counts()
    rows = {"prov.runs": (len(runs), "run folders (manifest.json) behind README.md's numbers"),
            "prov.untraced": (len(untraced), "cited result files with no manifest found beside or above them"),
            "prov.no_commit": (no_commit, "of the runs, manifests without a git commit"),
            "prov.no_lens_sha": (no_lens, "of the runs, manifests without a lens sha256"),
            "g1.writers_unrecorded": (unrecorded, f"manifest writers that recorded no switches before {G1} (the test's scan)"),
            "g1.writers_switches": (switches, f"of those, writers that record their switches since {G1}"),
            "g1.writers_left_out": (left_out, f"of those, writers {G1} left out of the check (no model loaded)")}  # fmt: skip
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["key", "value", "source"])
        for k, (v, what) in rows.items():
            w.writerow([k, v, f"scripts/provenance_counts.py: {what}"])
    print(f"wrote {OUT.relative_to(REPO)}: " + ", ".join(f"{k} {v}" for k, (v, _) in rows.items()))
    if untraced:
        print("untraced:", sorted(untraced)[:10])


if __name__ == "__main__":
    main()
