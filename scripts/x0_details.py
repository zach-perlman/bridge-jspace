"""x0_details: every X0 number the README quotes, recomputed from the run files, and the details page.

Writes docs/x0_numbers.json (key -> {"text", "source"}; the README's {{num|key}} markers read it through
scripts/readme_build.py) and docs/x0_details.md, rendered from docs/x0_details.template.md: {{num|key}} becomes the
number, {{tbl|name}} a table generated from the runs. UNVERIFIED like the runs.

uv run python scripts/x0_details.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from bridge_jspace import pins
from scripts import x0_descriptive as D
from scripts import x0_figures as XF
from scripts import x0_necessity as X
from scripts import x0_strata as ST

DOCS = pins.REPO_ROOT / "docs"
NUMBERS = DOCS / "x0_numbers.json"
TEMPLATE = DOCS / "x0_details.template.md"
MODELS = {"9b": ("qwen3.5-9b", "qwen35_9b_x0_necessity", "qwen35_9b_x0_kmatch"),
          "27b": ("qwen3.6-27b", "x0_necessity_27b_chat", "x0_kmatch_27b"),
          "122b": ("qwen3.5-122b-a10b", "qwen35_122b_x0_necessity_r2", "qwen35_122b_x0_necessity_r2")}  # fmt: skip
CTX = "results/d1_verdict/x0_ctx_parts_27b_20261024-144050/verdict.json"
NOCHAT = {"9b": "qwen35_9b_x0_necessity_nothink", "27b": "x0_necessity_27b_nothink"}
DIGIT = {"9b": "qwen35_9b_x0_digit_r2", "27b": "x0_digit_27b_r2", "122b": "qwen35_122b_x0_necessity_r2"}
SINGLE = {"9b": "qwen35_9b_x0_single_r2", "27b": "x0_single_27b_r2"}
PROBES = {"9b": "qwen35_9b_x0_probe", "27b": "x0_probe_27b"}
ATOMS = {"letters": "x0_atoms_27b_letters", "all": "x0_atoms_27b_all"}
ORDER = "org locker vs asked pick"


def f2(x: float) -> str:
    return f"{x:.2f}".replace("-", "−")


def ci(v: list[float]) -> str:
    return f"{f2(v[0])} [{f2(v[1])}, {f2(v[2])}]"


def pct(x: float) -> str:
    return f"{100 * x:.0f}%"


class Numbers:
    def __init__(self) -> None:
        self.d: dict[str, dict[str, str]] = {}

    def add(self, key: str, text: str, source: str) -> None:
        assert key not in self.d, key
        self.d[key] = {"text": text, "source": source}


def compute() -> tuple[Numbers, dict[str, list[str]]]:
    num, tables = Numbers(), {}
    for m, (target, run, kmatch) in MODELS.items():
        r = XF.Run(run)
        src = f"results/x0_necessity/{run}/outcomes.jsonl"
        la = X.PREDICTED[target]
        rows = [x for x in r.rows if x["rendering"] == "chat"]
        cells = D.all_cells(rows, X.N_BOOT)
        lk, rc = cells[("chat", la, X.LOOKUP, *X.MAIN)], cells[("chat", la, X.RECALL, *X.MAIN)]
        num.add(f"layer_{m}", str(la), src)
        num.add(f"n_{m}", str(lk["n"]), src)
        num.add(f"ents_{m}", str(lk["entities"]), src)
        num.add(f"verdict_{m}", X.verdict(lk, rc), src)
        for w, c in (("lk", lk), ("rc", rc)):
            num.add(f"{w}_excess_{m}", ci(c["excess"]), src)
            num.add(f"{w}_jdep_{m}", f2(c["Jdep"][0]), src)
            num.add(f"{w}_rdep_{m}", f2(c["Rdep"][0]), src)
            n = c["n"]
            num.add(f"{w}_whole_{m}", str(round(c["S_whole"][0] * n)), src)
            num.add(f"{w}_noj_{m}", str(round(c["S_no_part"][0] * n)), src)
            num.add(f"{w}_norand_{m}", str(round(c["S_no_rand"][0] * n)), src)
            num.add(f"{w}_dropj_{m}", f"{100 * c['drop_noD'][0]:.1f}", src)
            num.add(f"{w}_droprand_{m}", f"{100 * c['drop_noRand'][0]:.1f}", src)
        num.add(f"contrast_{m}", ci(XF.contrast(r, "chat", la)), src)
        # k-match: J++ at 25-200 atoms
        km = XF.Run(kmatch)
        kcells = km.cells("chat")
        for (_, l2, w, d, k, omp), c in kcells.items():
            if l2 == la and d == "jpp" and omp == "signed":
                num.add(f"{'lk' if w == X.LOOKUP else 'rc'}_excess_k{k}_{m}", f2(c["excess"][0]),
                        f"results/x0_necessity/{kmatch}/outcomes.jsonl")  # fmt: skip
        # sentence order (whole edit, lookups)
        cases = {c["scene"]: c for c in X.read_jsonl(r.dir / "cases.jsonl") if c["rendering"] == "chat"}
        whole = [x for x in rows if x["layer"] == la and x["reader"] == X.LOOKUP and x["arm"] == "whole"]
        for order in ("before", "after"):
            mine = [x for x in whole if ST.features(cases[x["scene"]])["org locker vs asked pick"] == order]
            num.add(f"lk_order_{order}_{m}", pct(sum(x["switched"] for x in mine) / len(mine)), src)
        # upstream change
        for name, keep in (("up", lambda x: x["upstream"]), ("af", lambda x: not x["upstream"])):
            sub = X.cells_of([x for x in rows if x["layer"] == la and keep(x)])
            c = sub[("chat", la, X.LOOKUP, *X.MAIN)]
            num.add(f"lk_excess_{name}_{m}", f2(c["excess"][0]), src)
            num.add(f"lk_swhole_{name}_{m}", pct(c["S_whole"][0]), src)
            num.add(f"lk_n_{name}_{m}", str(c["n"]), src)
        # no chat template, thinking off: the gate under the first-token read (the 9B and the 27B)
        if m not in NOCHAT:
            tables[f"layers_{m}"] = table_layers(cells, r)
            tables[f"dicts_{m}"] = table_dicts(cells, r, la)
            tables[f"strata_{m}"] = table_strata(rows, cases, la)
            continue
        g = json.loads((X.RESULTS / NOCHAT[m] / "gate.json").read_text())["gate"]["nothink"]["org_accuracy"]
        num.add(f"nochat_gate_{m}", f"{100 * g['PP']:.1f}% / {100 * g['PM']:.1f}%".replace(".0%", "%"),
                f"results/x0_necessity/{NOCHAT[m]}/gate.json")  # fmt: skip
        tables[f"layers_{m}"] = table_layers(cells, r)
        tables[f"dicts_{m}"] = table_dicts(
            D.all_cells([x for x in km.rows if x["rendering"] == "chat"], X.N_BOOT), km, la
        )
        tables[f"strata_{m}"] = table_strata(rows, cases, la)
    for m, run in DIGIT.items():
        digit_numbers(num, tables, m, run)
    atoms_numbers(num)
    single_numbers(num)
    probe_numbers(num)
    corr = json.loads(sorted((X.RESULTS / MODELS["27b"][1]).glob("descriptive-*/cells.json"))[-1].read_text())
    num.add("share_rho_27b", f2(corr["renderings"]["chat"]["correlations"][f"{X.LOOKUP} Jdep"]["spearman"]),
            f"results/x0_necessity/{MODELS['27b'][1]}/descriptive-*/cells.json")  # fmt: skip
    ctx = json.loads((pins.REPO_ROOT / CTX).read_text())["cells"]["context:32"]
    for w in ("lookup", "recall"):
        num.add(f"ctx_{w}_full", pct(ctx[w]["full"][0]), CTX)
        num.add(f"ctx_{w}_noj", pct(ctx[w]["not_jspace"][0]), CTX)
    nec = ctx["necessity"]
    num.add("ctx_recall_drop", f"{100 * nec['recall_drop_J']:.0f}", CTX)
    num.add("ctx_recall_droprand", f"{100 * nec['recall_drop_rand']:.0f}".replace("-", "−"), CTX)
    num.add("ctx_recall_diff", ci(nec["recall_dropJ_minus_droprand"]), CTX)
    num.add("ctx_n", str(nec["n_lookup"]), CTX)
    return num, tables


def digit_numbers(num: Numbers, tables: dict[str, list[str]], m: str, run: str) -> None:
    """The digit check: lookups and recalls by locker order, J++ over letters (jpp) vs every token (jppall) at
    25 / 50 / 100 atoms, and the 10 digit directions alone (jppdig); the answer-digit readout."""
    path = sorted((X.RESULTS / run).glob("strata-*/strata.json"))[-1]
    src = str(path.relative_to(pins.REPO_ROOT))
    rows = [s for s in json.loads(path.read_text())["strata"] if s["feature"] == ORDER and s["omp"] == "signed"]
    out = ["| locker vs pick | reader | dictionary | atoms | n | flipped by the whole edit | excess | label |",
           "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    name = {"jpp": "J++ (letters)", "jppall": "J++ (every token)", "jppdig": "the 10 digit directions"}
    for s in sorted(rows, key=lambda s: (s["value"] != "before", s["reader"] != X.LOOKUP, s["dict"], s["k"])):
        if s["dict"] not in name:
            continue
        w = "lk" if s["reader"] == X.LOOKUP else "rc"
        num.add(f"dig_{w}_{s['dict']}_k{s['k']}_{s['value']}_{m}", f2(s["excess"][0]), src)
        out.append(f"| {s['value']} | {'lookup' if w == 'lk' else 'recall'} | {name[s['dict']]} | {s['k']} | {s['n']} | "
                   f"{s['switched_whole']} | {ci(s['excess'])} | {s['label']} |")  # fmt: skip
    tables[f"digit_{m}"] = out
    la = X.PREDICTED[MODELS[m][0]]  # the 122B's X0 run reads out at every layer; the digit runs at one
    readout = [r for r in X.read_jsonl(X.RESULTS / run / "readout.jsonl") if r["layer"] == la]
    cases = {c["scene"]: c for c in X.read_jsonl(X.RESULTS / run / "cases.jsonl") if c["rendering"] == "chat"}
    for order in ("before", "after"):
        mine = [r for r in readout if r["reader"] == X.LOOKUP and r["run"] == "org"
                and ST.features(cases[r["scene"]])[ORDER] == order]  # fmt: skip
        num.add(f"dig_readout_first_{order}_{m}", pct(sum(r["rank_org_answer"] == 1 for r in mine) / len(mine)),
                f"results/x0_necessity/{run}/readout.jsonl")  # fmt: skip


def atoms_numbers(num: Numbers) -> None:
    """The J++ atoms of the bridge edit (27B L32, 20 random items): how often the first atom is the bridge's own
    token, and whether a digit or number word enters the top 25 when every token is allowed."""
    for v, run in ATOMS.items():
        rows = [r for r in X.read_jsonl(pins.RESULTS_DIR / "x0_atoms" / run / "atoms.jsonl") if r["subset"] == "all"]
        src = f"results/x0_atoms/{run}/atoms.jsonl"
        first = sum(r["atoms"][0]["mark"] in ("bridge_org", "bridge_alt") for r in rows)
        num.add(f"atoms_first_bridge_{v}", f"{first} of {len(rows)}", src)
        for mark in ("digit", "number_word"):
            k = sum(a["mark"] == mark for r in rows for a in r["atoms"][:25])
            num.add(f"atoms_{mark}_top25_{v}", f"{k} of {25 * len(rows)}", src)
        every = X.read_jsonl(pins.RESULTS_DIR / "x0_atoms" / run / "atoms.jsonl")  # random and asked-first items
        bridge = ("bridge_org", "bridge_alt")
        has = sum(any(a["mark"] in bridge for a in r["atoms"][:25]) for r in every)
        num.add(f"atoms_bridge_top25_{v}", f"{has} of {len(every)}", src)
        share = [sum(a["coef_k25"] ** 2 for a in r["atoms"][:25] if a["mark"] in bridge)
                 / sum(a["coef_k25"] ** 2 for a in r["atoms"][:25]) for r in every]  # fmt: skip
        num.add(f"atoms_bridge_coef2_{v}", pct(sorted(share)[len(share) // 2] if len(share) % 2
                                                else sum(sorted(share)[len(share) // 2 - 1 : len(share) // 2 + 1]) / 2), src)  # fmt: skip


def single_numbers(num: Numbers) -> None:
    """The single-change edit (only the asked pick changes; after data) at the pre-registered layer: the lookup's and
    the recall's excess at k = 25, and the lookup's at k = 100."""
    for m, run in SINGLE.items():
        r = XF.Run(run)
        la = X.PREDICTED[MODELS[m][0]]
        cells = r.cells("chat")
        src = f"results/x0_necessity/{run}/outcomes.jsonl"
        num.add(f"single_lk_excess_{m}", ci(cells[("chat", la, X.LOOKUP, *X.MAIN)]["excess"]), src)
        num.add(f"single_lk_excess_pt_{m}", f2(cells[("chat", la, X.LOOKUP, *X.MAIN)]["excess"][0]), src)
        num.add(f"single_rc_excess_{m}", ci(cells[("chat", la, X.RECALL, *X.MAIN)]["excess"]), src)
        num.add(f"single_lk_excess_k100_{m}", f2(cells[("chat", la, X.LOOKUP, "jpp", 100, "signed")]["excess"][0]), src)
        paired = sorted((X.RESULTS / run).glob("paired-*/paired.json"))[-1]  # single minus two-change, shared items
        for w, d in json.loads(paired.read_text())["readers"].items():
            num.add(f"paired_{'lk' if w == X.LOOKUP else 'rc'}_excess_{m}", ci(d["paired_difference"]["excess"]),
                    str(paired.relative_to(pins.REPO_ROOT)))  # fmt: skip


def probe_numbers(num: Numbers) -> None:
    """The probes at the bridge's word (X0 items, locker-before; descriptive): (a) the answer digit, (b) the locker
    sentence's index with its visible-layout baseline, (c) the bridge's identity."""
    for m, run in PROBES.items():
        path = sorted((pins.RESULTS_DIR / "x0_probe" / run).glob("probe-*/probe.json"))[-1]
        src = str(path.relative_to(pins.REPO_ROOT))
        rows = {
            r["target"]: r
            for r in json.loads(path.read_text())["rows"]
            if r["subset"] == "x0" and r["stratum"] == "before"
        }
        num.add(f"probe_a_before_{m}", f2(rows["answer digit"]["probe"][0]), src)
        num.add(f"probe_a_chance_{m}", f2(rows["answer digit"]["chance"]), src)
        num.add(f"probe_b_before_{m}", f2(rows["locker sentence"]["probe"][0]), src)
        num.add(f"probe_b_layout_before_{m}", f2(rows["locker sentence"]["layout"][0]), src)
        num.add(f"probe_c_before_{m}", f2(rows["bridge identity"]["probe"][0]), src)


def table_layers(cells: dict, run: Any) -> list[str]:
    out = ["| layer | reader | n | S whole | S without J++ | S without random | excess | J++ share | label |",
           "|---|---|---|---|---|---|---|---|---|"]  # fmt: skip
    for (rr, la, w, *d), c in sorted(cells.items()):
        if tuple(d) == X.MAIN:
            share = run.share[(rr, la, *X.MAIN)]
            out.append(f"| {la} | {'lookup' if w == X.LOOKUP else 'recall'} | {c['n']} | {f2(c['S_whole'][0])} | "
                       f"{f2(c['S_no_part'][0])} | {f2(c['S_no_rand'][0])} | {ci(c['excess'])} | {share:.3f} | {c['label']} |")  # fmt: skip
    return out


def table_dicts(cells: dict, run: Any, la: int) -> list[str]:
    out = ["| dictionary | atoms | reader | share removed | dependence | random dependence | excess | label |",
           "|---|---|---|---|---|---|---|---|"]  # fmt: skip
    name = {"jpp": "J++", "wu": "W_U", "we": "W_E", "rand": "random atoms", "jppall": "J++ (every token)",
            "jppdig": "the 10 digit directions"}  # fmt: skip
    order = lambda kv: (kv[0][3] != "jpp", kv[0][3], kv[0][4], kv[0][2] != X.LOOKUP)  # noqa: E731
    for (_rr, l2, w, d, k, omp), c in sorted(cells.items(), key=order):
        if l2 == la and omp == "signed":
            out.append(f"| {name[d]} | {k} | {'lookup' if w == X.LOOKUP else 'recall'} | "
                       f"{run.share[('chat', la, d, k, omp)]:.3f} | {ci(c['Jdep'])} | {ci(c['Rdep'])} | {ci(c['excess'])} | "
                       f"{c['label']} |")  # fmt: skip
    return out


def table_strata(rows: list[dict], cases: dict, la: int) -> list[str]:
    out = [
        "| split | value | reader | n | flipped by the whole edit | excess | label |",
        "|---|---|---|---|---|---|---|",
    ]
    feat = {s: ST.features(cases[s]) for s in {x["scene"] for x in rows}}
    for key in ST.FEATURES:
        for value in sorted({f[key] for f in feat.values()}):
            cells = X.cells_of([x for x in rows if x["layer"] == la and feat[x["scene"]][key] == value])
            for w in X.READERS:
                c = cells[("chat", la, w, *X.MAIN)]
                flag = " (too few)" if c["switched_whole"] < X.VALID_N else ""
                out.append(f"| {key} | {value} | {'lookup' if w == X.LOOKUP else 'recall'} | {c['n']} | "
                           f"{c['switched_whole']}{flag} | {ci(c['excess'])} | {c['label']} |")  # fmt: skip
    return out


def render(text: str, num: Numbers, tables: dict[str, list[str]]) -> str:
    import re

    out = []
    for line in text.splitlines():
        m = re.fullmatch(r"\{\{tbl\|([\w]+)\}\}", line.strip())
        if m:
            out += tables[m.group(1)]
            continue
        out.append(re.sub(r"\{\{num\|([\w]+)\}\}", lambda x: num.d[x.group(1)]["text"], line))
    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    num, tables = compute()
    NUMBERS.write_text(json.dumps(num.d, indent=1, ensure_ascii=False) + "\n")
    page = render(TEMPLATE.read_text(), num, tables)
    (DOCS / "x0_details.md").write_text(
        "<!-- Generated by scripts/x0_details.py from docs/x0_details.template.md and the X0 runs; edit the template. -->\n"
        + page
    )
    print(NUMBERS, len(num.d), "numbers;", DOCS / "x0_details.md")


if __name__ == "__main__":
    main()
