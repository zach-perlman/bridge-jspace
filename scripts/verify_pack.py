"""Verification pack for Dan (25 Oct plan, step 4): for each README finding, one raw-count table recounted directly from
the per-item files (outcomes.jsonl, cases.jsonl, eligible.jsonl; no verdict or aggregate file is read), with the file
paths and the one-line command that prints it; 10 random route cases (seed 0) with both prompts and the lookup's answer
per arm; the outputs recomputed locally after the jobq copy bug, with their commands. Extra loss from counts:
(switches without the random part - switches without the part) / switches with the whole change.

uv run python scripts/verify_pack.py                 # writes docs/verify_pack.md
uv run python scripts/verify_pack.py --only 3        # prints finding 3's table
"""

from __future__ import annotations

import argparse
import collections
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_first_mention as FM
from scripts import x0_necessity as X
from scripts import x0_strata as ST

R = pins.RESULTS_DIR
OUT = pins.REPO_ROOT / "docs" / "verify_pack.md"
LAYER = {"9B": 12, "27B": 32, "122B": 33}
CMD = "uv run python scripts/verify_pack.py --only {}"
READER = {X.LOOKUP: "lookup", X.RECALL: "recall"}


def rows_of(path: Path) -> list[dict]:
    return X.read_jsonl(path)


def tally(rows: list[dict], scenes: set[str] | None = None) -> dict[tuple, int]:
    """Switch counts per (reader, arm, dict, k, omp), on the given scenes."""
    t: dict[tuple, int] = collections.Counter()
    n: dict[str, set] = collections.defaultdict(set)
    for r in rows:
        if scenes is not None and r["scene"] not in scenes:
            continue
        key = (r["reader"], r["arm"], r.get("dict", "-"), r.get("k", 0), r.get("omp", "-"))
        t[key] += int(r["switched"])
        if r["arm"] == "whole":
            n[r["reader"]].add(r["scene"])
    return {**t, **{("n", w): len(s) for w, s in n.items()}}


def extra(whole: int, no: int, rand: int) -> str:
    return f"{(rand - no) / whole:.2f}" if whole else "–"


def at(rows: list[dict], layer: int) -> list[dict]:
    return [r for r in rows if r.get("rendering", "chat") == "chat" and r.get("layer", layer) == layer]


def part_rows(label: str, rows: list[dict], parts, scenes=None) -> list[str]:
    """One table row per reader and part: n, switches whole / without the part / without its random part, extra loss."""
    t = tally(rows, scenes)
    out = []
    for w in X.READERS:
        whole = t.get((w, "whole", "-", 0, "-"), 0)
        for name, d, k, omp in parts:
            no, rand = t.get((w, "no_part", d, k, omp), 0), t.get((w, "no_rand", d, k, omp), 0)
            out.append(f"| {label} | {READER[w]} | {name} | {t.get(('n', w), 0)} | {whole} | {no} | {rand} | "
                       f"{extra(whole, no, rand)} |")  # fmt: skip
    return out


HEAD = ["| run | reader | part | n | switches, whole change | without the part | without its random part | extra loss |",
        "|---|---|---|---|---|---|---|---|"]  # fmt: skip
JPP = [("J++ (25)", "jpp", X.K_MAIN, "signed")]


def f1() -> tuple[str, list[str], list[str]]:
    runs = [("9B, two people swap", "x0_necessity/qwen35_9b_x0_necessity", 12),
            ("27B, two people swap", "x0_necessity/x0_necessity_27b_chat", 32),
            ("122B, two people swap", "x0_necessity/qwen35_122b_x0_necessity_r2", 33),
            ("122B, only the asked pick", "x0_necessity/qwen35_122b_x0_single", 33)]  # fmt: skip
    lines = list(HEAD)
    for label, d, layer in runs:
        lines += part_rows(label, at(rows_of(R / d / "outcomes.jsonl"), layer), JPP)
    return (
        "1. Recall needs the J++ part far more than lookup does",
        [f"results/{d}/outcomes.jsonl" for _, d, _ in runs],
        lines,
    )


def f2() -> tuple[str, list[str], list[str]]:
    lines = list(HEAD)
    files = []
    for label, d in (("varied scenes, 9B", "x0b_generalize/qwen35_9b_x0b_v2"), ("varied scenes, 27B", "x0b_generalize/x0b_v2_27b"),
                     ("varied scenes, 122B", "x0b_generalize/qwen35_122b_x0b_v2"),
                     ("natural passages, 27B", "x5_natural/x5_natural_27b"),
                     ("natural passages, 122B", "x5_natural/qwen35_122b_x5_natural")):  # fmt: skip
        layer = LAYER[label.split(", ")[1]]
        lines += part_rows(label, at(rows_of(R / d / "outcomes.jsonl"), layer), JPP)
        files.append(f"results/{d}/outcomes.jsonl")
    lines += ["", "The locker key in another language (lookup, each form on its own eligible items):", "",
              "| run | key | n | switches, whole change | without J++ | without its random part | extra loss |",
              "|---|---|---|---|---|---|---|"]  # fmt: skip
    for m, d in (
        ("9B", "x4_alias/qwen35_9b_x4_patch"),
        ("27B", "x4_alias/x4_patch_27b"),
        ("122B", "x4_alias/qwen35_122b_x4_patch"),
    ):
        rows = at(rows_of(R / d / "outcomes.jsonl"), LAYER[m])
        elig = {r["key"]: set(r["scenes"]) for r in rows_of(R / d / "eligible.jsonl")}
        files += [f"results/{d}/outcomes.jsonl", f"results/{d}/eligible.jsonl"]
        for key in sorted(k for k in elig if k.startswith("animals/") and k.endswith(f"/{X.LOOKUP}")):
            t = tally([r for r in rows if r["domain"] == "animals" and r["reader"] == X.LOOKUP], elig[key])
            whole, no, rand = (t.get((X.LOOKUP, a, *p), 0) for a, p in (("whole", ("-", 0, "-")),
                               ("no_part", ("jpp", X.K_MAIN, "signed")), ("no_rand", ("jpp", X.K_MAIN, "signed"))))  # fmt: skip
            form = {"same": "verbatim", "xlang": "translated"}.get(key.split("/")[1], key.split("/")[1])
            lines.append(f"| {m} | {form} | {len(elig[key])} | {whole} | {no} | {rand} | {extra(whole, no, rand)} |")
    return "2. It holds beyond the simple scenes on most models, not on all", files, lines


def f3() -> tuple[str, list[str], list[str]]:
    parts = [("J++ (25)", "jpp", X.K_MAIN, "signed"), ("main directions at J++'s share", "pca_eq", 0, "eq"),
             ("J++ without the word's directions", "jwo", X.K_MAIN, "signed"), ("the word only", "w", 0, "lsq")]  # fmt: skip
    lines, files = list(HEAD), []
    for label, d in (("9B", "x0_parts/qwen35_9b_x0_pcaeq"), ("27B", "x0_parts/x0_pcaeq_27b"), ("122B", "x0_parts/qwen35_122b_x0_parts"),
                     ("9B (word part run)", "x0_parts/qwen35_9b_x0_parts"), ("27B (word part run)", "x0_parts/x0_parts_27b")):  # fmt: skip
        rows = at(rows_of(R / d / "outcomes.jsonl"), LAYER[label.split(" ")[0]])
        have = {(r.get("dict"), r.get("k"), r.get("omp")) for r in rows}
        lines += part_rows(label, rows, [p for p in parts if p[1:] in have])
        files.append(f"results/{d}/outcomes.jsonl")
    return "3. The J++ part against the layer's main directions and the word", files, lines


def f4() -> tuple[str, list[str], list[str]]:
    lines = ["| run | the original's locker sentence | n | lookup switches, whole change |", "|---|---|---|---|"]
    files = []
    for m, d in (("9B", "x0_necessity/qwen35_9b_x0_necessity"), ("27B", "x0_necessity/x0_necessity_27b_chat"),
                 ("122B", "x0_necessity/qwen35_122b_x0_necessity_r2")):  # fmt: skip
        cases = {c["scene"]: c for c in rows_of(R / d / "cases.jsonl") if c["rendering"] == "chat"}
        sw: dict[str, list[int]] = collections.defaultdict(list)
        for r in at(rows_of(R / d / "outcomes.jsonl"), LAYER[m]):
            if r["reader"] == X.LOOKUP and r["arm"] == "whole":
                sw[ST.features(cases[r["scene"]])["org locker vs asked pick"]].append(int(r["switched"]))
        lines += [f"| {m} | {o} | {len(v)} | {sum(v)} |" for o, v in sorted(sw.items())]
        files += [f"results/{d}/outcomes.jsonl", f"results/{d}/cases.jsonl"]
    return "4. Lookups move mostly when the locker sentence comes first", files, lines


def f5() -> tuple[str, list[str], list[str]]:
    lines = ["| run | the new item's first earlier mention | n | lookup switches, whole change | without J++ | "
             "recall switches, whole change | without J++ |", "|---|---|---|---|---|---|---|"]  # fmt: skip
    files = []
    for m, d in (("9B", "x0_necessity/qwen35_9b_x0_single_r2"), ("27B", "x0_necessity/x0_single_27b_r2"),
                 ("122B", "x0_necessity/qwen35_122b_x0_single")):  # fmt: skip
        cases = {c["scene"]: c for c in rows_of(R / d / "cases.jsonl") if c["rendering"] == "chat"}
        rows = at(rows_of(R / d / "outcomes.jsonl"), LAYER[m])
        both = {s for s in {r["scene"] for r in rows} if (f := ST.features(cases[s]))["org locker vs asked pick"] == "before"
                and f["alt locker vs asked pick"] == "before"}  # fmt: skip
        groups = collections.defaultdict(set)
        for s in both:
            groups[FM.first_mention(cases[s])].add(s)
        for g, scenes in sorted(groups.items()):
            t = tally(rows, scenes)
            c = [
                t.get((w, a, *p), 0)
                for w in X.READERS
                for a, p in (("whole", ("-", 0, "-")), ("no_part", ("jpp", X.K_MAIN, "signed")))
            ]
            lines.append(f"| {m} | {g} | {len(scenes)} | {c[0]} | {c[1]} | {c[2]} | {c[3]} |")
        files += [f"results/{d}/outcomes.jsonl", f"results/{d}/cases.jsonl"]
    lines += ["", "The probe's own accuracy (0.97 / 0.99 / 0.92) is not recountable from saved per-item files: the "
              "probe's per-scene predictions are not written. It refits from the saved states on CPU: "
              "`uv run python scripts/x0_probe.py fit --name x0_probe_v4_27b` (9B / 122B: `BJ_TARGET=qwen3.5-9b` / "
              "`BJ_TARGET=qwen3.5-122b-a10b`, `--name qwen35_9b_x0_probe_v4` / `qwen35_122b_x0_probe_v4`), into a new "
              "probe-<UTC>/ folder."]  # fmt: skip
    return "5. The bridge word holds a pointer to the item's first mention (the duplicate-pick split)", files, lines


def f6() -> tuple[str, list[str], list[str]]:
    lines = ["| run | reader | part | n | switches, whole change | without the part | without its random part | extra loss |",
             "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    files = []
    for m, d in (("9B", "x0_massmean/qwen35_9b_x0_massmean_lf"), ("27B", "x0_massmean/x0_massmean_lf_27b"),
                 ("122B", "x0_massmean/qwen35_122b_x0_massmean_grid")):  # fmt: skip
        rows = rows_of(R / d / "outcomes.jsonl")
        for w in X.READERS:
            c = collections.Counter(r["arm"] for r in rows if r["reader"] == w and r["switched"])
            n = sum(1 for r in rows if r["reader"] == w and r["arm"] == "whole")
            lines.append(f"| {m} | {READER[w]} | pointer directions | {n} | {c['whole']} | {c['no_Alf']} | {c['no_Alf_rand']} | "
                         f"{extra(c['whole'], c['no_Alf'], c['no_Alf_rand'])} |")  # fmt: skip
        files.append(f"results/{d}/outcomes.jsonl")
    for m, d in (
        ("9B, replication", "x0_replicate/qwen35_9b_x0_replicate"),
        ("27B, replication", "x0_replicate/x0_replicate_27b"),
    ):
        rows = at(rows_of(R / d / "outcomes.jsonl"), LAYER[m.split(",")[0]])
        lines += part_rows(m, rows, [("pointer directions", "alf", 0, "proj"), ("J++ (25)", "jpp", X.K_MAIN, "signed")])
        files.append(f"results/{d}/outcomes.jsonl")
    return "6. Pointer directions outside the lens matter to the lookup on the 9B and 122B", files, lines


def f7() -> tuple[str, list[str], list[str]]:
    routes = ("identity", "position", "value", "original", "other")
    lines = ["| run | swap | arm | n | " + " | ".join(routes) + " |", "|---|---|---|---|" + "---|" * len(routes)]
    files = []
    for m, d in (("9B", "x6_routes/qwen35_9b_x6_routes"), ("27B", "x6_routes/x6_routes_27b")):
        c = collections.Counter((r["condition"], r["arm"], r["route"]) for r in rows_of(R / d / "outcomes.jsonl")
                                if r["reader"] == X.LOOKUP and r["condition"] != "C0")  # fmt: skip
        for cond in ("C1", "C2"):
            for arm in ("whole", "no_jpp", "no_jpp_rand", "no_alf", "no_alf_rand"):
                counts = [c[(cond, arm, rt)] for rt in routes]
                lines.append(f"| {m} | {'same item moved' if cond == 'C1' else 'another item moved'} | {arm} | {sum(counts)} | "
                             + " | ".join(map(str, counts)) + " |")  # fmt: skip
        files.append(f"results/{d}/outcomes.jsonl")
    lines += ["", "Same item moved: 'identity' is the unchanged answer."]
    return "7. The lookup follows the bridge's identity or its locker sentence's position", files, lines


FINDINGS = {1: f1, 2: f2, 3: f3, 4: f4, 5: f5, 6: f6, 7: f7}


def route_cases(n: int = 10) -> list[str]:
    pool = []
    for m, d in (("9B", "x6_routes/qwen35_9b_x6_routes"), ("27B", "x6_routes/x6_routes_27b")):
        cases = {c["scene"]: c for c in rows_of(R / d / "cases.jsonl")}
        by = collections.defaultdict(dict)
        for r in rows_of(R / d / "outcomes.jsonl"):
            if r["reader"] == X.LOOKUP and r["condition"] in ("C1", "C2"):
                by[r["scene"]][r["arm"]] = r
        pool += [(m, d, cases[s], by[s]) for s in sorted(by)]
    out = [f"Drawn with `random.Random(0).sample` from the {len(pool)} same-item-moved and another-item-moved scenes of the 9B and 27B "
           "runs (layer fixed in advance). Each arm's answer is the route its top token matched (the digit in brackets).", ""]  # fmt: skip
    for k, (m, d, c, arms) in enumerate(random.Random(0).sample(pool, n), 1):
        exp = c["expect"]
        out += [f"### {k}. {m}, {'same item moved' if c['condition'] == 'C1' else 'another item moved'}, {c['scene']} (results/{d})", "",
                f"- Original prompt: {c['context']}", f"- Swapped prompt: {c['cf_context']}",
                f"- Question: {c['readers'][X.LOOKUP]['question']}",
                "- Routes: " + ", ".join(f"{rt} → {v}" for rt, v in exp.items()), "",
                "| arm | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms),
                "| lookup's answer | " + " | ".join(f"{r['route']} ({exp.get(r['route'], '?')})" for r in arms.values()) + " |", ""]  # fmt: skip
    return out


RECOMPUTED = [
    (
        "The 122B's first-mention cross-tab (lost by the box copy; b3)",
        "BJ_TARGET=qwen3.5-122b-a10b uv run python scripts/x0_first_mention.py --single qwen35_122b_x0_single",
        "results/x0_necessity/qwen35_122b_x0_single/first-mention-20261024T232524Z/",
    ),
    (
        "X4 on the 122B, the probe fit and the verdict (b5)",
        "BJ_TARGET=qwen3.5-122b-a10b uv run python scripts/x4_alias.py probe_fit --name qwen35_122b_x4_patch && "
        "BJ_TARGET=qwen3.5-122b-a10b uv run python scripts/x4_alias.py verdict --name qwen35_122b_x4_patch",
        "results/x4_alias/qwen35_122b_x4_patch/{probe,verdict}-20261025T003459Z/",
    ),
    (
        "X4 on the 9B and 27B, the probe fit and the verdict (24 Oct)",
        "uv run python scripts/x4_alias.py probe_fit --name x4_patch_27b && uv run python scripts/x4_alias.py verdict "
        "--name x4_patch_27b (9B: BJ_TARGET=qwen3.5-9b, --name qwen35_9b_x4_patch)",
        "results/x4_alias/{x4_patch_27b,qwen35_9b_x4_patch}/{probe,verdict}-*/",
    ),
    (
        "The 122B's varied-scene cross-tab (b6)",
        "BJ_TARGET=qwen3.5-122b-a10b uv run python scripts/x0b_generalize.py cross --name qwen35_122b_x0b_v2",
        "results/x0b_generalize/qwen35_122b_x0b_v2/cross-20261025T112138Z/",
    ),
    (
        "The 122B's probe a-given-b (b3)",
        "BJ_TARGET=qwen3.5-122b-a10b uv run python scripts/x0_probe.py a_given_b --name qwen35_122b_x0_probe_v4",
        "results/x0_probe/qwen35_122b_x0_probe_v4/a-given-b-20261025T112514Z/",
    ),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int, default=None)
    a = ap.parse_args()
    if a.only:
        title, files, lines = FINDINGS[a.only]()
        print(f"## {title}\n\n" + "\n".join(lines))
        return
    out = ["# Verification pack (25 Oct)", "",
           "For Dan's own checks. Every table below is recounted from per-item files only (outcomes.jsonl, cases.jsonl, "
           "eligible.jsonl), not from verdict or aggregate files; each has the command that prints it again. Extra loss "
           "from counts = (switches without the random part - switches without the part) / switches with the whole "
           "change; its point value should equal the README's. Layers fixed in advance: 9B 12, 27B 32, 122B 33; chat "
           "prompts; 25 J++ directions. Generated by scripts/verify_pack.py. Unverified until Dan's check.", ""]  # fmt: skip
    for i, fn in FINDINGS.items():
        title, files, lines = fn()
        out += [f"## {title}", "", f"Files: {', '.join(f'`{f}`' for f in dict.fromkeys(files))}", "",
                f"Command: `{CMD.format(i)}`", "", *lines, ""]  # fmt: skip
    out += ["## 10 random route cases (seed 0)", "", *route_cases(), "## Outputs recomputed locally after the jobq copy bug", "",
            "The box copies only run folders new to it, so CPU output a later job wrote into an earlier job's folder was "
            "lost; these were recomputed locally from the same input files (checksums matched the box's).", "",
            "| output | command | folder |", "|---|---|---|",
            *[f"| {t} | `{c}` | `{f}` |" for t, c, f in RECOMPUTED], ""]  # fmt: skip
    OUT.write_text("\n".join(out) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
