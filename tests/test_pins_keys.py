"""pins.TARGETS keys, run prefixes and lens paths (the danorel -> main merge, 27 Oct 2026; main kept every key).

A dict literal with a repeated key keeps the last value without a word, so two branches that each pin a target under
the same name merge into one silent entry (the merge found four: qwen3-32b, muse-glimmer-30b, qwen3.6-27b-jlens and
gemma-4-31b-it-full). These tests read pins.py's source for repeated keys, then check that every run prefix names one
target, that the one documented overlap of a legacy and a live prefix resolves by lens sha256, that no local lens path
holds two lenses, and that every existing run under the legacy prefix resolves to the key of the lens it recorded.
"""

import ast
from collections import Counter

from bridge_jspace import pins

SOURCE = (pins.REPO_ROOT / "src" / "bridge_jspace" / "pins.py").read_text()
# Prefixes shared on purpose: gpt-oss-20b-prefit is gpt-oss-20b's checkpoint before its lens was pinned (Zach,
# amendment 8; "the fit registers gpt-oss-20b with the same run prefix"); its runs are lens-free.
SHARED_ON_PURPOSE = {"gptoss20_": {"gpt-oss-20b", "gpt-oss-20b-prefit"}}
# The one legacy prefix that is also live: Dan's Qwen3-32B J-lens runs (his old "qwen3-32b") and Zach's J++ runs (main's
# "qwen3-32b") are both named qwen3_32b_; the manifest's lens sha256 tells them apart (pins.LEGACY_PREFIXES).
LEGACY_LIVE = {"qwen3_32b_": "qwen3-32b"}


def _module_dict(name: str) -> ast.Dict:
    for node in ast.parse(SOURCE).body:
        if isinstance(node, ast.AnnAssign | ast.Assign):
            targets = [node.target] if isinstance(node, ast.AnnAssign) else node.targets
            if any(isinstance(t, ast.Name) and t.id == name for t in targets):
                assert isinstance(node.value, ast.Dict), name
                return node.value
    raise AssertionError(f"no module-level {name} = {{...}} in pins.py")


def _literal_keys(d: ast.Dict) -> list[str]:
    keys = [k.value for k in d.keys if isinstance(k, ast.Constant)]
    assert len(keys) == len(d.keys) and all(isinstance(k, str) for k in keys), "a non-string or computed key"
    return [str(k) for k in keys]


def _subscript_assigned(name: str) -> list[str]:
    """Keys set as NAME["key"] = ... at module level (TARGETS["deepseek-v4-flash"] = {...})."""
    out = []
    for node in ast.parse(SOURCE).body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == name:
                    assert isinstance(t.slice, ast.Constant), ast.dump(t)
                    out.append(str(t.slice.value))
    return out


def test_targets_literal_has_no_repeated_key():
    keys = _literal_keys(_module_dict("TARGETS")) + _subscript_assigned("TARGETS")
    repeated = sorted(k for k, n in Counter(keys).items() if n > 1)
    assert not repeated, f"TARGETS keys set twice (the last silently wins): {repeated}"
    assert set(keys) == set(pins.TARGETS)


def test_legacy_prefixes_literal_has_no_repeated_key():
    keys = _literal_keys(_module_dict("LEGACY_PREFIXES"))
    assert len(keys) == len(set(keys)) == len(pins.LEGACY_PREFIXES)


def test_the_qwen3_32b_keys_name_one_lens_each():
    shas = {k: pins.TARGETS[k]["frozen_lens_sha256"][:8] for k in ("qwen3-32b", "qwen3-32b-jlens", "qwen3-32b-jpp")}
    assert shas == {"qwen3-32b": "6fbc0386", "qwen3-32b-jlens": "0af5ccf2", "qwen3-32b-jpp": "7d6856b6"}


def test_no_local_lens_path_holds_two_lenses():
    """Two keys may read one local file only if they pin the same sha256 (Zach's and Dan's Qwen3-32B J++ were both
    cache/qwen3-32b/lenses/jpp/Qwen3-32B_jpp_lens.pt)."""
    shas: dict[str, set[str]] = {}
    for t in pins.TARGETS.values():
        for source in t["lenses"].values():
            if source[0] == "local":
                shas.setdefault(source[1], set()).add(source[2])
    assert not {p: s for p, s in shas.items() if len(s) > 1}


def test_every_run_prefix_names_one_target():
    keys_of: dict[str, set[str]] = {}
    for key, t in pins.TARGETS.items():
        keys_of.setdefault(t["run_prefix"], set()).add(key)
    shared = {p: ks for p, ks in keys_of.items() if len(ks) > 1}
    assert shared == SHARED_ON_PURPOSE, f"run prefixes shared by several targets: {shared}"
    for keys in shared.values():  # the same checkpoint, and at most one of them with a lens
        a, b = (pins.TARGETS[k] for k in sorted(keys))
        assert (a["repo"], a["revision"]) == (b["repo"], b["revision"])
        assert sum(bool(pins.TARGETS[k]["lenses"]) for k in keys) <= 1


def test_legacy_prefixes_overlap_live_ones_only_as_documented():
    live = {t["run_prefix"]: k for k, t in pins.TARGETS.items() if t["run_prefix"]}
    overlap = {p: live[p] for p in pins.LEGACY_PREFIXES if p in live}
    assert overlap == LEGACY_LIVE, overlap
    for prefix, by_sha in pins.LEGACY_PREFIXES.items():
        assert None in by_sha, f"{prefix}: no key for runs that record no lens"
        for sha, key in by_sha.items():
            assert key in pins.TARGETS, (prefix, key)
            if sha is not None:  # the lens that sha256 names is that key's frozen lens
                assert pins.TARGETS[key]["frozen_lens_sha256"] == sha, (prefix, key)
            assert pins.run_target(prefix + "x_v1", sha) == key
        if prefix in live:  # the live key's own lens resolves to it
            assert by_sha[pins.TARGETS[live[prefix]]["frozen_lens_sha256"]] == live[prefix]


def test_longer_live_prefixes_keep_their_runs():
    """A live prefix that extends a legacy one (qwen3_32b_jpp_ and qwen3_32b_) keeps its own runs."""
    for key, t in pins.TARGETS.items():
        p = t["run_prefix"]
        if p and p not in pins.LEGACY_PREFIXES and key not in SHARED_ON_PURPOSE.get(p, set()):
            assert pins.run_target(p + "x_v1") == key
    assert pins.run_target("full2_ko_v1") == "qwen3.6-27b"


def test_existing_legacy_runs_resolve_to_the_lens_they_recorded():
    """Every results/<exp>/<run> under a legacy prefix (and no longer live one) resolves to a key; where its manifest
    records one of the prefix's lens sha256s, to the key whose frozen lens that is."""
    seen = Counter()
    for prefix, by_sha in pins.LEGACY_PREFIXES.items():
        known = [s for s in by_sha if s]
        for run in sorted(p for p in pins.RESULTS_DIR.glob(f"*/{prefix}*") if p.is_dir()):
            longest = max(
                (t["run_prefix"] for t in pins.TARGETS.values() if run.name.startswith(t["run_prefix"])), key=len
            )
            if len(longest) > len(prefix):
                continue  # a longer live prefix's run (qwen3_32b_jpp_)
            manifest = run / "manifest.json"
            text = manifest.read_text() if manifest.exists() else ""
            shas = [s for s in known if s in text]
            assert len(shas) <= 1, (run, shas)
            key = pins.run_target(run.name, shas[0] if shas else None)
            if shas:
                assert pins.TARGETS[key]["frozen_lens_sha256"] == shas[0]
            seen[(prefix, key)] += 1
    assert seen[("qwen3_32b_", "qwen3-32b-jlens")] and seen[("qwen3_32b_", "qwen3-32b")], seen
