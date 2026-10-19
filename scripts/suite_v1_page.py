"""Render suite_v1 as one mobile-friendly HTML page: an overview grid (counts, competence, balance), then per family
two examples with the cue, the bridge and the answer marked and what C and O change, the answer distribution, the
retired sets and the sample-size table.   python3 scripts/suite_v1_page.py OUT_DIR  (reads data/ and results/)"""

import collections
import html
import json
import math
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA, RES = ROOT / "data" / "suite_v1", ROOT / "results" / "suite_v1" / "competence_v1"
FAMS = {  # family: (title, source -> use -> answer from, answer type)
    "BL": (
        "BL · bound → lookup",
        "bound in the prompt → a lookup in the prompt → answer in the prompt",
        "locker (odd digit)",
    ),
    "BR": ("BR · bound → recall", "bound in the prompt → a recalled fact → answer from memory", "legs (2/4/6/8)"),
    "RL": (
        "RL · recalled → lookup",
        "recalled from a cue → a lookup in the prompt → answer in the prompt",
        "locker (odd digit)",
    ),
    "RR": ("RR · recalled → recall", "recalled from a cue → a recalled fact → answer from memory", "legs (2/4/6/8)"),
    "NAMES": ("NAMES · pointer chase", "bound in the prompt → a lookup in the prompt → answer in the prompt", "a name"),
    "CODE": ("CODE · two-dict lookup", "bound in code → a lookup in code → answer in the code", "digit 1-9"),
}
CSS = """
body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#fcfcfb;color:#0b0b0b;margin:0;padding:14px;max-width:980px}
h1{font-size:20px;margin:4px 0 2px} h2{font-size:16px;margin:22px 0 6px} .muted{color:#6b6a65;font-size:13px}
table{border-collapse:collapse;width:100%;font-size:13px;margin:8px 0} th,td{border-bottom:1px solid #e1e0d9;padding:5px 6px;text-align:left;vertical-align:top}
th{color:#6b6a65;font-weight:600} .card{background:#fff;border:1px solid #e1e0d9;border-radius:10px;padding:12px;margin:12px 0}
.card h3{font-size:15px;margin:0 0 2px} .ex{background:#f6f5f1;border-radius:8px;padding:9px;margin:8px 0;font-size:13.5px;line-height:1.55;white-space:pre-wrap}
.q{font-weight:600} .tag{display:inline-block;font-size:11px;color:#6b6a65;margin-right:8px}
.cue{background:#fde7a7;border-radius:3px;padding:0 2px} .br{background:#cfe0f7;border-radius:3px;padding:0 2px}
.ans{background:#cdebd8;border-radius:3px;padding:0 2px;font-weight:600} .chg{background:#f6d0cc;border-radius:3px;padding:0 2px}
.bars{display:flex;gap:3px;align-items:flex-end;height:46px;margin:6px 0 2px} .bar{background:#3b6fb6;width:20px;border-radius:3px 3px 0 0}
.barlab{display:flex;gap:3px;font-size:10px;color:#6b6a65} .barlab span{width:20px;text-align:center}
.legend span{margin-right:10px;font-size:12px} .ok{color:#2f7d4f;font-weight:600} .warn{color:#b0472f;font-weight:600}
"""


def esc(s: str) -> str:
    return html.escape(s)


def mark(text: str, spans: list[tuple[str, str]]) -> str:
    """Escape text and wrap each (substring, class) once, longest first, without overlapping earlier marks."""
    out = esc(text)
    for sub, cls in sorted(spans, key=lambda x: -len(x[0])):
        if not sub:
            continue
        pat = re.escape(esc(sub))
        out, _ = re.subn(rf"(?<![\w>])({pat})(?![\w<])", rf'<span class="{cls}">\1</span>', out, count=0)
    return out


def bars(counter: collections.Counter, order=None) -> str:
    keys = order or sorted(counter, key=lambda k: (len(str(k)), str(k)))
    m = max(counter.values())
    b = "".join(
        f'<div class="bar" title="{esc(str(k))}: {counter[k]}" style="height:{max(3, 44 * counter[k] / m):.0f}px"></div>'
        for k in keys
    )
    lab = "".join(f"<span>{esc(str(k))[:4]}</span>" for k in keys)
    return f'<div class="bars">{b}</div><div class="barlab">{lab}</div>'


def diff_words(a: str, b: str) -> list[str]:
    wa, wb = re.findall(r"\w+", a), re.findall(r"\w+", b)
    return [y for x, y in zip(wa, wb, strict=True) if x != y] if len(wa) == len(wb) else []


def example(it: dict) -> str:
    fam = it["family"]
    spans = [(it["cue"], "cue")] if fam in ("BL", "BR", "NAMES", "RL", "RR") else []
    spans += [(it["bridge"], "br")]
    if fam in ("BL", "RL", "CODE", "NAMES"):  # the answer stands in the prompt
        spans += [(it["answer"], "ans")] if fam != "CODE" else []
    ctx = mark(it["context"], spans)
    q = mark(it["question"], [(it["cue"], "cue")] if fam != "CODE" else [])
    if fam in ("RL", "RR"):  # C changes the cue in the question (cues are one or two words)
        cf_words = [re.search(r"known for (.+?)(?: have)?\?$", it["cf_question"]).group(1)]  # type: ignore[union-attr]
    else:
        cf_words = diff_words(it["context"] + " " + it["question"], it["cf_context"] + " " + it["cf_question"])
    off_words = diff_words(it["context"], it["off_context"])
    return (f'<div class="ex">{ctx}\n<span class="q">{q}</span>\n'
            f'<span class="tag">bridge</span><span class="br">{esc(it["bridge"])}</span> → '
            f'<span class="tag">answer</span><span class="ans">{esc(it["answer"])}</span>\n'
            f'<span class="tag">C</span>changes to <span class="chg">{esc(", ".join(cf_words))}</span>: bridge '
            f'<span class="br">{esc(it["cf_bridge"])}</span>, answer <span class="ans">{esc(it["cf_answer"])}</span>   '
            f'<span class="tag">O</span>changes <span class="chg">{esc(", ".join(off_words))}</span>, answer stays</div>')  # fmt: skip


def main(out_dir: Path) -> None:
    rows = [json.loads(line) for line in (RES / "items.jsonl").read_text().splitlines()]
    per = collections.defaultdict(lambda: collections.defaultdict(dict))
    for r in rows:
        per[r["family"]][r["id"]][r["kind"]] = r["correct"]
    rng = random.Random(1)
    grid, cards = [], []
    for fam, (title, design, atype) in FAMS.items():
        items = json.loads((DATA / f"{fam}.json").read_text())["items"]
        p = per[fam]
        clean = sum(v["clean"] for v in p.values())
        all5 = sum(all(v.values()) for v in p.values())
        answers = collections.Counter(it["answer"] for it in items)
        bridges = collections.Counter(it["bridge"] for it in items)
        grid.append(f"<tr><td><b>{esc(fam)}</b></td><td>{esc(design)}</td><td>{esc(atype)}</td><td>{len(items)}</td>"
                    f"<td>{clean}/{len(items)}</td><td><b>{all5}</b></td><td>{len(bridges)} ({min(bridges.values())}-{max(bridges.values())} each)</td></tr>")  # fmt: skip
        exs = "".join(example(it) for it in rng.sample(items, 2))
        cards.append(f'<div class="card"><h3>{esc(title)}</h3><div class="muted">{esc(design)} · answer: {esc(atype)} · '
                     f"{len(items)} items, {all5} eligible (clean, C, O and both steps right)</div>{exs}"
                     f'<div class="muted">answers</div>{bars(answers)}<div class="muted">bridges ({len(bridges)})</div>'
                     f"{bars(bridges, [b for b, _ in bridges.most_common()])}</div>")  # fmt: skip
    # brew (its own files) and B1 (the paper's reference set, annotated)
    brew = json.loads((ROOT / "data" / "brew_test.json").read_text())["items"]
    bx = rng.sample(brew, 1)[0]
    brew_text = bx["prompt"].split("Problem: ", 1)[-1]
    brew_card = (f'<div class="card"><h3>BREW · colour table, two lookups (kept as is)</h3><div class="muted">in the prompt → '
                 "a lookup → a lookup → answer in the prompt · answer: one of 12 colours · brew_test 600 + brew_fresh 200 "
                 "(ungated; the model 87-88% right, each step alone 100%) · its own pipeline (exp04, exp07)</div>"
                 f'<div class="ex">{mark(brew_text, [(bx["start"], "cue"), (bx["intermediates"][0], "br"), (bx["answer"], "ans")])}\n'
                 f'<span class="tag">start</span><span class="cue">{esc(bx["start"])}</span> → <span class="tag">bridge</span>'
                 f'<span class="br">{esc(bx["intermediates"][0])}</span> → <span class="tag">answer</span><span class="ans">{esc(bx["answer"])}</span></div></div>')  # fmt: skip
    ann = json.loads((DATA / "B1_annotations.json").read_text())["items"]
    cnt = collections.Counter((a["bridge_kind"], a["relation"]) for a in ann)
    clean_ex = [a for a in ann if a["clean"]][:4]
    flag_ex = [a for a in ann if not a["clean"]][:4]
    b1_card = ('<div class="card"><h3>B1 · the paper\'s 90 two-hop facts (reference, unchanged, annotated)</h3>'
               f'<div class="muted">recalled → recalled → memory · {cnt[("place","one_to_one")]} places, '
               f'{cnt[("person","one_to_one")]} people, {cnt[("other","one_to_one")]} other one-to-one (the France → Paris '
               f'risk), <b>{cnt[("other","many_to_one")]} clean</b> (non-place, answer shared by many bridges; 25 eligible)</div>'
               '<div class="ex">clean: ' + "; ".join(f'<span class="br">{esc(a["bridge"])}</span> → <span class="ans">{esc(a["answer"])}</span>' for a in clean_ex)
               + '\nflagged: ' + "; ".join(f'<span class="br">{esc(a["bridge"])}</span> → <span class="chg">{esc(a["answer"])}</span>' for a in flag_ex)
               + "</div></div>")  # fmt: skip

    # sample sizes
    def half(n, p):
        z = 1.96
        d = 1 + z * z / n
        return 100 * z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d

    nrows = "".join(
        f"<tr><td>{n}</td>" + "".join(f"<td>±{half(n, p):.1f}</td>" for p in (0.05, 0.15, 0.3, 0.5)) + "</tr>"
        for n in (40, 80, 100, 150, 200, 400)
    )
    retired = ("<ul class='muted'><li>exp09 R, B (city/person → country → <b>capital</b>): the France → Paris relation; "
               "R also failed in raw text</li><li>exp09 L, RL (countries as table keys, cities recalled to countries): place "
               "relations, 13 countries; replaced by RL/BL on animals</li><li>Phase 3 LM, RM, BT, RT (capitals and landmark "
               "cities; RM 74% competent): place relations</li><li>arithmetic: the copy carries too little (10%)</li>"
               "<li>B1's 61 one-to-one items: kept as the paper's reference, analysed apart</li></ul>")  # fmt: skip
    page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Part B prompt suite v1</title><style>{CSS}</style></head><body>
<h1>Part B prompt suite v1</h1>
<div class="muted">Qwen3.6-27B, chat template, thinking off, "Answer:" prefilled. Every family: a counterfactual C that changes
only the bridge, an off-path control O, both lined up token for token with the clean prompt (2,400/2,400). Eligible = the
model answers the clean prompt, C, O and each step alone (results/suite_v1/competence_v1).</div>
<div class="legend" style="margin-top:8px"><span><span class="cue">cue</span></span><span><span class="br">bridge</span></span>
<span><span class="ans">answer</span></span><span><span class="chg">what C / O change</span></span></div>
<h2>Overview</h2>
<table><tr><th>family</th><th>source → used by → answer from</th><th>answer</th><th>items</th><th>clean right</th><th>eligible</th><th>bridges</th></tr>
{"".join(grid)}
<tr><td><b>BREW</b></td><td>prompt → lookup → lookup → prompt</td><td>12 colours</td><td>800</td><td>87-88%</td><td>exp04's rule</td><td>12</td></tr>
<tr><td><b>B1</b></td><td>recalled → recalled → memory (reference)</td><td>mixed</td><td>90</td><td>77 (86%)</td><td>25 clean</td><td>77</td></tr></table>
<div class="muted">The 2x2 core (BL, BR, RL, RR) shares one context per scene; only the question differs, so its families
are paired item by item. Lockers are odd digits and legs even, so the answers never collide; legs is many-to-one (ten of the
sixteen animals have 4), so an answer cannot stand in for its bridge.</div>
<h2>How many items</h2><div class="muted">Half-width (points) of a 95% Wilson interval by n and true rate. Patching runs
sample ≥150 eligible items per family (±8 at worst; paired part-vs-rest differences ±4); competence uses every item.</div>
<table><tr><th>n</th><th>5%</th><th>15%</th><th>30%</th><th>50%</th></tr>{nrows}</table>
<h2>Families</h2>{"".join(cards)}{brew_card}{b1_card}
<h2>Retired from headline runs</h2>{retired}
</body></html>"""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(page)
    print("wrote", out_dir / "index.html")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
