"""writeup_data: the numbers of the LessWrong write-up's figures that no existing data file holds, recomputed from the
run files into data/figures/writeup/data.csv (the schema of docs/breadth/data.csv: key, figure, model, quantity, value,
lo, hi, n, unit, source). CPU only; it reads results/ and never writes there.

The `source` column names every file a row is computed from (repo-relative), with the condition or field inside it, and
the code that computes it. A reader script that only prints has its output saved under data/figures/writeup/raw/.

uv run python scripts/writeup_data.py            # recompute and write data/figures/writeup/data.csv
uv run python scripts/writeup_data.py --check    # recompute and compare with the stored file, write nothing
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from bridge_jspace import figdata as S  # noqa: E402
from scripts import f2_differences as F2  # noqa: E402

OUT = REPO / "data" / "figures" / "writeup" / "data.csv"
FIELDS = ("key", "figure", "model", "quantity", "value", "lo", "hi", "n", "unit", "source")
DIGITS = 4  # stored precision; the figures print fewer
ZK_MODEL = {"q9": "qwen3.5-9b", "q27": "qwen3.6-27b", "mu": "muse-glimmer-30b", "nl": "nemotron-3.5-lightning",
            "q122": "qwen3.5-122b-a10b"}  # fmt: skip
SHORT = {m: k for k, m in ZK_MODEL.items()}  # the kit's short model ids (figkit/exemplars.ZK) in every key


def _row(key, figure, model, quantity, value, lo=None, hi=None, n=None, unit="", source="") -> dict:
    r = lambda x: "" if x is None else round(float(x), DIGITS)  # noqa: E731
    return {"key": key, "figure": figure, "model": model, "quantity": quantity, "value": r(value), "lo": r(lo),
            "hi": r(hi), "n": "" if n is None else int(n), "unit": unit, "source": source}  # fmt: skip


# ---- fig05: the band difference at one decimal (docs/breadth/data.csv stores its interval rounded to whole points) ----
def fig05_rows() -> list[dict]:
    """Per model, the lens part minus its largest same-size control (specs.largest: rotated, logit lens or PCA), M - K
    in points, paired on the same items: f2_differences.band_difference (clusters relation:bridge, 1000 draws,
    random.Random(0)), the same computation as the f2.band.* rows, kept unrounded."""
    out = []
    for k, (run, pca_run) in F2.BAND_RUNS.items():
        top = S.largest(k)
        if top is None:
            continue
        cond = F2.CONTROLS[top[0]][0]
        other = pca_run if top[0] == "pc" else run
        if other is None:
            continue
        iv = F2.band_difference(run, "paper10", other, cond)
        if iv is None:
            continue
        src = (f"results/ablate_v2/{run}/rows.jsonl (paper10) minus results/ablate_v2/{other}/rows.jsonl ({cond}); "
               f"items data/tasks_v2/{F2.SET}/items.jsonl; scripts/f2_differences.py band_difference")  # fmt: skip
        out.append(_row(f"fig05.band_diff.{k}", "fig05_controls", ZK_MODEL[k],
                        f"M - K, lens part minus {F2.CONTROLS[top[0]][1]} (paired; the largest same-size control)",
                        *iv, unit="points", source=src))  # fmt: skip
    return out


# ---- fig04: the twin set (note 41, v4 draw 4001), the registered population: every gated item ---------------------------
ABLATE = REPO / "results" / "ablate_v2"
TWIN_PREFIX = {"qwen3.5-9b": "qwen35_9b_", "qwen3.6-27b": "", "nemotron-3.5-lightning": "nem35l_"}
READER = {"MM": "recall", "MP": "lookup"}


def fig04_rows() -> list[dict]:
    """Per model and twin (recall = MM, lookup = MP), accuracy (%) unedited, under the knock-out (paper10), rotated
    (paper10_rot) and the knock-out keeping the answer span (paper10_keepA); the recall - lookup gap of paper10 and of
    paper10_rot, points, with the registered interval (nn_ko37_read.boot: bridges resampled, 2000 draws, Random(0)).
    Accuracies: the ko41 run's summary.json over all gated items. keepA: note 37's run (same items and unedited reads,
    asserted by note41.json's stored check), whose rows are not in the repo: unedited minus its stored loss (to 0.1)."""
    out = []
    for model, p in TWIN_PREFIX.items():
        run = f"results/ablate_v2/{p}jsuite_v4_test_chat_ko41_cand2_v1/summary.json"
        note = f"results/ablate_v2/nn_ko_read/{p}note41.json"
        s, n41 = json.loads((REPO / run).read_text()), json.loads((REPO / note).read_text())
        band = next(iter(s["cells"]))
        cell, keep = s["cells"][band], n41["n37"]["conditions"]["paper10_keepA"]
        assert n41["n37"]["n"] == n41["A"]["n"], model  # keepA on the same population as the registered gap
        for fam, reader in READER.items():
            n = n41["A"]["n"][fam]
            un = 100 * s["unedited_accuracy"][f"{fam}/clean"]
            accs = {"unedited": (un, f'{run} unedited_accuracy["{fam}/clean"]'),
                    **{c: (100 * cell[f"{fam}/clean"][c]["accuracy"], f'{run} cells["{band}"]["{fam}/clean"]["{c}"].accuracy')
                       for c in ("paper10", "paper10_rot")},
                    "paper10_keepA": (un - keep[f"loss_{fam}"],
                                      f'{run} unedited_accuracy minus {note} n37.conditions.paper10_keepA.loss_{fam}')}  # fmt: skip
            for cond, (v, src) in accs.items():
                out.append(_row(f"fig04.{reader}.{cond}.{SHORT[model]}", "fig04_twin_set", model,
                                f"{reader} twins ({fam}), accuracy, {cond}, band {band}", v, n=n, unit="%",
                                source=src))  # fmt: skip
        for cond in ("paper10", "paper10_rot"):
            c = n41["A"]["conditions"][cond]
            out.append(_row(f"fig04.gap.{cond}.{SHORT[model]}", "fig04_twin_set", model,
                            f"recall - lookup accuracy drop, {cond} (registered: all gated items, draw 4001)",
                            c["gap"], *c["gap_ci"], n=n41["A"]["n"]["MM"] + n41["A"]["n"]["MP"], unit="points",
                            source=f"{note} A.conditions.{cond}.gap, gap_ci (scripts/nn_ko41_read.py)"))  # fmt: skip
    return out


# ---- fig11: removals orthogonal to the answers (notes 62 and 67; the stored reader outputs, rows not in the repo) -------
SD_READ = "results/sd_necessity/nn_sd_read"
SD_BAND = {"qwen3.5-9b": "L12-16", "qwen3.6-27b": "L32-40", "nemotron-3.5-lightning": "L27-33"}  # note 67's mid band


def fig11_rows() -> list[dict]:
    """Panel 1 (note 62, the one-hop question "{city} is in the country of", gated items, descriptive): accuracy loss in
    points of the city's J++ directions, of the same directions made orthogonal to the answers (no interval stored), and
    of the answers' own J++ directions. Panel 2 (note 67's registered R1, mid band): the cleaned data-built city subspace
    minus energy-matched random directions, points, bridge-clustered interval (ci_bridges, the one Amendment 85
    addendum 2 registers; the item interval is stored beside it)."""
    out = []
    for model, p in TWIN_PREFIX.items():
        k = SHORT[model]
        src62 = f"{SD_READ}/{p}sd62_ko_test_v1_note62.json"
        g = json.loads((REPO / src62).read_text())["strata"]["gated"]
        for key, field in (("city", "O:bridgeJ loss"), ("answers", "O:ansJ loss")):
            c = g["beside"][field]
            out.append(_row(f"fig11.onehop.{key}.{k}", "fig11_orthogonal", model,
                            f"one-hop question, accuracy loss, {field}", c["value"], *c["ci"], n=c["n"],
                            unit="points", source=f'{src62} strata.gated.beside["{field}"] (scripts/nn_sd62_read.py)'))  # fmt: skip
        o = g["R1_cells"]["O"]
        out.append(_row(f"fig11.onehop.city_perp.{k}", "fig11_orthogonal", model,
                        "one-hop question, accuracy loss, the city's J++ directions orthogonal to the answers (no interval)",
                        o["loss_perp"], n=o["n"], unit="points",
                        source=f"{src62} strata.gated.R1_cells.O.loss_perp (scripts/nn_sd62_read.py)"))  # fmt: skip
        src67 = f"{SD_READ}/{p}sd67_ko_test_v1_note67.json"
        r = json.loads((REPO / src67).read_text())["readings"]["R1_bands"][SD_BAND[model]]
        out.append(_row(f"fig11.clean_subspace.{k}", "fig11_orthogonal", model,
                        f"cleaned city subspace minus energy-matched random, band {SD_BAND[model]} (registered R1, bar 15); "
                        f"bridge-clustered interval; item interval {r['ci']}", r["value"], *r["ci_bridges"], n=r["n"],
                        unit="points", source=f'{src67} readings.R1_bands["{SD_BAND[model]}"].value, ci_bridges '
                        "(scripts/nn_sd67_read.py)"))  # fmt: skip
    return out


# ---- fig10: what recall loses is its answer's own directions (notes 41, 50, 57, 68; the stored reader outputs) ----------
KO_READ = "results/ablate_v2/nn_ko_read"


def fig10_rows() -> list[dict]:
    """(a) keepA's rescue of the recall (note 41 keep table, row A: 1 - net keep / net paper10; interval 1 - ratio_ci)
    and its grey control, note 50's P1: a random keep orthogonal to the answers, the one whose energy is closest to and
    not below keepA's (its rescue, or the reading's label where neither holds enough energy). (b) note 57's S1 on v4
    draw 4001 and (c) on the codename set (jsuite_v5al): [net onlyA - net onlyRperp] / net paper10, with onlyRperp's
    energy matching (matching.paper10.reached_share: the share of items whose random part reached its target energy)."""
    out = []
    for model, p in TWIN_PREFIX.items():
        k = SHORT[model]
        src41 = f"{KO_READ}/{p}note41.json"
        a = json.loads((REPO / src41).read_text())["keep"]["table"]["A"]
        out.append(_row(f"fig10.keep_span.{k}", "fig10_answer_span", model,
                        "share of the recall's damage undone by keeping only the answer span (keepA rescue)",
                        a["rescue"], 1 - a["ratio_ci"][1], 1 - a["ratio_ci"][0], n=a["n_MM"], unit="share",
                        source=f"{src41} keep.table.A.rescue; interval 1 - ratio_ci (scripts/nn_ko41_read.py)"))  # fmt: skip
        src50 = f"{KO_READ}/{p}note49_50.json"
        p1 = json.loads((REPO / src50).read_text())["readings"]["50_P1"]
        e = f"keepA energy {p1['E_A']}"
        if "rescue" in p1:
            out.append(_row(f"fig10.keep_ctrl.{k}", "fig10_answer_span", model,
                            f"rescue of a random keep orthogonal to the answers ({p1['perp']}, energy "
                            f"{p1['E_perps'][p1['perp']]}; {e})", p1["rescue"], *p1["rescue_ci"], n=p1["n_MM"],
                            unit="share", source=f'{src50} readings["50_P1"].rescue, rescue_ci (scripts/nn_ko49_read.py)'))  # fmt: skip
        else:
            out.append(_row(f"fig10.keep_ctrl.{k}", "fig10_answer_span", model,
                            f"no control: {p1['label']} (energies {p1['E_perps']}; {e})", None, unit="share",
                            source=f'{src50} readings["50_P1"].label (scripts/nn_ko49_read.py)'))  # fmt: skip
        for panel, name in (("v4", f"{p}note57.json"), ("codename", f"{p}jsuite_v5al_test_chat_note57.json")):
            src = f"{KO_READ}/{name}"
            d = json.loads((REPO / src).read_text())
            s1, mt = d["readings"]["S1"], d["matching"]["paper10"]
            out.append(_row(f"fig10.span_only.{panel}.{k}", "fig10_answer_span", model,
                            "removing only the answer span, net of energy-matched random, as a multiple of the full "
                            f"damage (S1, {d['run'].split('/')[-1]})", s1["value"], *s1["ci"], n=s1["n_MM"],
                            unit="multiple", source=f"{src} readings.S1.value, ci (scripts/nn_ko57_read.py)"))  # fmt: skip
            out.append(_row(f"fig10.span_only_matched.{panel}.{k}", "fig10_answer_span", model,
                            "share of items whose random part reached its target energy (onlyRperp)",
                            mt["reached_share"], n=mt["n"], unit="share",
                            source=f"{src} matching.paper10.reached_share (scripts/nn_ko57_read.py)"))  # fmt: skip
    return out


# ---- figA1: the knock-out inside agent transcripts (notes 56c, 59, 65; the stored reader outputs) ---------------------
ROLE = re.compile(r"^(\w+) \[[^,\]]+, (primary|confirmatory|descriptive)")


def _roles(readings: list[str]) -> dict[str, str]:
    """reading id -> its registered role, from the reader's lines ("G1 [qwen3.6-27b, descriptive (27B); ...]")."""
    return {m.group(1): m.group(2) for r in readings if (m := ROLE.match(r))}


def figA1_rows() -> list[dict]:
    """Specific loss in points: the knock-out's loss minus a control's, paired by item, bridge-clustered 95% intervals.
    copy (K instr_vis, printed beside K1: no registered reading of its own, so descriptive), pick (A1) and produce (G1)
    against the rotated control (note 59); verify (note 65 V1, L_V) against the largest of the three controls'
    losses, its bridge-clustered interval (ci_bridges; its item interval is stored beside); derive (hyp_vis, C1)
    against rotated from note 56c, run on the 9B only: no row for the others (the figure says "source missing")."""
    out = []
    for model, p in TWIN_PREFIX.items():
        k = SHORT[model]
        src59 = f"{SD_READ}/{p}sd59_ko_test_v1_note59.json"
        d59 = json.loads((REPO / src59).read_text())
        roles = _roles(d59["readings"])
        for col, key, role in (("copy", "K instr_vis", "descriptive"), ("pick", "A1", roles.get("A1", "")),
                               ("produce", "G1", roles.get("G1", ""))):  # fmt: skip
            e = d59["effects"][key]["paper10_rot"]
            out.append(_row(f"figA1.{col}.{k}", "figA1_agents", model,
                            f"{col}: specific loss vs rotated (paper10_rot); registered role: {role or 'none'}",
                            e["value"], *e["ci"], n=e["n"], unit="points",
                            source=f'{src59} effects["{key}"]["paper10_rot"] (scripts/nn_sd_ma1_read.py)'))  # fmt: skip
        src65 = f"{SD_READ}/{p}sd65_ko_test_v1_note65.json"
        d65 = json.loads((REPO / src65).read_text())
        v = d65["V1"]
        out.append(_row(f"figA1.verify.{k}", "figA1_agents", model,
                        f"verify: specific loss vs the harshest control (largest control loss); registered role: "
                        f"{d65['role']}; item interval {v['ci']}", v["L_V"], *v["ci_bridges"], n=v["n"], unit="points",
                        source=f"{src65} V1.L_V, V1.ci_bridges (scripts/nn_sd65_read.py)"))  # fmt: skip
        src56c = f"{SD_READ}/{p}sd56c_ko_test_v1_note56.json"
        if (REPO / src56c).exists():
            e = json.loads((REPO / src56c).read_text())["effects"]["hyp_vis spec loss paper10-vs-paper10_rot"]
            out.append(_row(f"figA1.derive.{k}", "figA1_agents", model,
                            "derive: specific loss vs rotated (paper10_rot); registered role: registered before the "
                            "run (note 56c, amendments 80 + 81)",
                            e["value"], *e["ci"], n=e["n"], unit="points",
                            source=f'{src56c} effects["hyp_vis spec loss paper10-vs-paper10_rot"] (scripts/nn_sd_ma1_read.py)'))  # fmt: skip
    return out


PROBE_RUN = {"qwen3.5-9b": "qwen35_9b_probe_ceiling_L12-16_v1", "qwen3.6-27b": "probe_ceiling_L32-40_v1",
             "nemotron-3.5-lightning": "nem35l_probe_ceiling_L27-33_v1"}  # fmt: skip


def fig12_rows() -> list[dict]:
    """Not drawn (Fig. 12 shows the pointer runs only): the post's text compares the lens part's swap with a probe's
    subspace on the same run and items (the probe-valid relations of the probe-ceiling run), transfer in points."""
    out = []
    for model, run in PROBE_RUN.items():
        k = SHORT[model]
        src = f"results/probe_ceiling/{run}/summary.json"
        s = json.loads((REPO / src).read_text())
        for key, cond, what in (("lens", "swap", "the lens part (J++) swapped in"),
                                ("probe", "swap_probe", "a probe's subspace swapped in")):  # fmt: skip
            v = s[f"memory_valid/{cond}"]
            out.append(_row(f"fig12.same_run.{key}.{k}", "fig12_pointer (text)", model,
                            f"{what}, transfer on the probe-valid relations (one run, one item set)", v["transfer"],
                            *(v.get("ci") or (None, None)), n=v.get("n"), unit="points",
                            source=f'{src} ["memory_valid/{cond}"].transfer'))  # fmt: skip
    return out


# ---- patch_split, panel 3: one layer against every token over four layers (no patch: the prompt's own state) ----------
# the files the ledger cards cite: zeroing at one layer (t47-5) and the removal ladder (49.2), each model's run
ZERO = {"q9": ("results/x47_zero/x47_5-20261028T113106Z/x47_5.json", "qwen35_9b_x47_5"),
        "q27": ("results/x47_zero/x47_5-20261028T113106Z/x47_5.json", "x47_5_27b"),
        "mu": ("results/x47_zero/x47_5-20261028T113106Z/x47_5.json", "muse30_x47_5"),
        "nl": ("results/x47_zero/x52_zero-20261029T032056Z/x47_5.json", "nem35l_x52_zero"),
        "q122": ("results/x47_zero/x52_zero-20261029T183120Z/x47_5.json", "qwen35_122b_x47_5")}  # fmt: skip
LADDER = {"q9": ("results/x49_ladder/x49_2-20261028T161612Z/x49_2.json", "qwen35_9b_x49_2"),
          "q27": ("results/x49_ladder/x52_ladder-20261029T012701Z/x49_2.json", "x52_ladder_27b_a"),
          "mu": ("results/x49_ladder/x49_2-20261028T161612Z/x49_2.json", "muse30_x49_2_r5"),
          "nl": ("results/x49_ladder/x52_ladder_below-20261029T091146Z/x49_2.json", "nem35l_x52_ladder_below"),
          "q122": ("results/x49_ladder/x52_ladder-20261029T192919Z/x49_2.json", "qwen35_122b_x49_2")}  # fmt: skip


def _run(path: str, run: str) -> dict:
    return next(m for m in json.loads((REPO / path).read_text())["models"] if m["run"] == run)


def patch_rows() -> list[dict]:
    out = []
    for k, (path, run) in ZERO.items():
        m = _run(path, run)
        for reader in ("recall", "lookup"):
            c = m["readers"][reader]
            v, lo, hi = c["kept"]["zero_L"]
            out.append(_row(f"patch.zero.{reader}.{k}", "patch_split", ZK_MODEL[k],
                            f"{reader}: answers kept, the lens part removed at the bridge word at L (no patch)", v, lo, hi,
                            c["n"], "share", f"{path} | {run} :: readers.{reader}.kept.zero_L (scripts/x47_zero.py)"))
    for k, (path, run) in LADDER.items():
        m = _run(path, run)
        for reader in ("recall", "lookup"):
            c = m["cells"][reader]["all"]
            for arm, what in (("zero5", "the lens part"), ("rand5", "a random part of the same share")):
                v, lo, hi = c["kept"][arm]
                out.append(_row(f"patch.every4.{arm[:4]}.{reader}.{k}", "patch_split", ZK_MODEL[k],
                                f"{reader}: answers kept, {what} removed at every token over L..L+3 (ladder rung 5, "
                                f"no patch)", v, lo, hi, c["n"], "share",
                                f"{path} | {run} :: cells.{reader}.all.kept.{arm} (scripts/x49_ladder.py)"))
    return out


BUILDERS = (fig04_rows, fig05_rows, fig10_rows, fig11_rows, figA1_rows, fig12_rows, patch_rows)


def rows() -> list[dict]:
    return [r for b in BUILDERS for r in b()]


def stored() -> list[dict]:
    with OUT.open() as f:
        return list(csv.DictReader(f))


def main(argv: list[str]) -> int:
    new = rows()
    for r in new:
        print(f"{r['key']:34s} {r['value']:>10} [{r['lo']}, {r['hi']}]  n={r['n']}")
    if "--check" in argv:
        old = {r["key"]: r for r in stored()}
        bad = [r["key"] for r in new if {k: str(v) for k, v in r.items()} != old.get(r["key"])]
        print(f"writeup_data --check: {len(bad)} row(s) differ from {OUT.relative_to(REPO)}: {bad}")
        return 1 if bad or len(old) != len(new) else 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(new)
    print(f"wrote {len(new)} rows to {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
