"""HTML for the review dashboard: the index, a view page (claim, automatic-check counts, samples) and item cards.
Self-contained pages (inline CSS / JS) so an export opens from disk."""

from __future__ import annotations

import html
import json
import re
from typing import Any
from urllib.parse import urlencode

from bridge_jspace.review import checks as C
from bridge_jspace.review import items as I

E = html.escape
CLASS_COLOR = {"b": "ok", "switch": "ok", "target": "ok", "follows S": "ok", "changed": "ok", "A": "org",
               "original": "org", "stays": "org", "unchanged": "org", "identity": "id", "position": "pos",
               "value": "val", "third": "third", "other": "oth"}  # fmt: skip
PARAMS = ("view", "seed", "n", "mode", "model", "reader", "condition", "s", "kind", "out", "superseded")

CSS = """
:root{--bg:#fbfbfa;--fg:#1d1d1f;--mut:#6b6b70;--card:#fff;--line:#e3e3e6;--hl:#fff1a8;--pos:#ffd0d0;
--ok:#2f7d4f;--org:#5b6b7f;--oth:#c98a12;--id:#2c6db5;--posc:#d4691b;--val:#7b4bb7;--third:#b8437a;--bad:#b8433a}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--fg:#e8e8ea;--mut:#9a9aa2;--card:#202024;--line:#36363c;
--hl:#5a4b10;--pos:#5c2626}}
body{background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,system-ui,sans-serif;margin:0;padding:16px}
main{max-width:1180px;margin:auto}a{color:var(--id)}h1{font-size:20px}h2{font-size:17px;margin-top:28px}
.mut{color:var(--mut)}.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;margin:10px 0}
form.ctl{display:flex;flex-wrap:wrap;gap:8px;align-items:end}form.ctl label{display:flex;flex-direction:column;font-size:12px}
input,select,textarea,button{font:inherit}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid var(--line);
padding:3px 6px;text-align:left;vertical-align:top;font-size:13px}th{color:var(--mut);font-weight:500}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;margin:12px 0}
.card.outside{border-style:dashed;opacity:.92}.hdr{font-weight:600}.tag{display:inline-block;border-radius:4px;padding:0 6px;
font-size:12px;color:#fff}.st{background:var(--mut)}.ok{background:var(--ok)}.org{background:var(--org)}.oth{background:var(--oth)}
.id{background:var(--id)}.pos{background:var(--posc)}.val{background:var(--val)}.third{background:var(--third)}
.fail{background:var(--bad)}.na{background:#999}.pass{background:var(--ok)}mark{background:var(--hl);color:inherit}
.prompt{white-space:pre-wrap;font-family:ui-monospace,Menlo,monospace;font-size:12.5px}.toks span{border:1px solid var(--line);
border-radius:3px;margin:1px;padding:0 2px;display:inline-block;font-family:ui-monospace,Menlo,monospace;font-size:12px}
.toks span.at{background:var(--pos);font-weight:700}.toks span.df{background:var(--hl)}.me{font-weight:600}
.marks{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:8px}.marks input[type=text]{flex:1;min-width:200px}
"""

JS = """
const MARKS=[];function key(){return 'review-marks'}
try{const s=localStorage.getItem(key());if(s)MARKS.push(...JSON.parse(s))}catch(e){}
async function mark(f){const d=Object.fromEntries(new FormData(f));if(!d.verdict){alert('pick consistent / wrong / unclear');return false}
d.utc=new Date().toISOString();d.commit=COMMIT;let ok=false;
if(SERVER){try{const r=await fetch('/mark',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});ok=r.ok}catch(e){}}
MARKS.push(d);try{localStorage.setItem(key(),JSON.stringify(MARKS))}catch(e){}
f.querySelector('.saved').textContent=(SERVER?(ok?'saved to review/marks.jsonl':'server failed, kept locally'):'kept locally')+' · '+d.verdict;return false}
function download(){const b=new Blob([MARKS.map(m=>JSON.stringify(m)).join('\\n')+'\\n'],{type:'application/json'});
const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='marks.jsonl';a.click()}
"""


def page(title: str, body: str, server: bool, commit: str) -> str:
    return (f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'>"
            f"<title>{E(title)}</title><style>{CSS}</style><script>const SERVER={'true' if server else 'false'};"
            f"const COMMIT={json.dumps(commit)};{JS}</script></head><body><main>{body}</main></body></html>")  # fmt: skip


def link(params: dict, server: bool) -> str:
    if server:
        return "/view?" + urlencode({k: v for k, v in params.items() if v not in (None, "")})
    return f"{params['view']}.html"


def tag(text: str, cls: str | None = None) -> str:
    return f"<span class='tag {cls or CLASS_COLOR.get(text, 'st')}'>{E(str(text))}</span>"


def tokens_html(model: str, ids: list[int], pos: int, diff: set[int]) -> str:
    out = []
    for i, t in enumerate(ids):
        s = C.piece(model, t).replace(" ", "␣").replace("\n", "↵")
        cls = "at" if i == pos else "df" if i in diff else ""
        out.append(f"<span class='{cls}' title='{i}: {t}'>{E(s)}</span>")
    return "<div class='toks'>" + "".join(out) + "</div>"


def marked(text: str, other: str) -> str:
    """The text with the words that differ from the other prompt highlighted (position by position)."""
    a, b = re.split(r"(\s+)", text), re.split(r"(\s+)", other)
    if len(a) != len(b):
        return E(text)
    return "".join(f"<mark>{E(x)}</mark>" if x != y and x.strip() else E(x) for x, y in zip(a, b, strict=True))


def expected_html(it: dict) -> str:
    c = it["case"]
    if it["kind"] == "routes":
        exp = ", ".join(f"{k} → {v}" for k, v in c["expect"].items())
        return f"<b>Routes predict</b> (lookup): {E(exp)}. " + "; ".join(
            f"{I.READER_NAME[w]}: O {E(str(c['readers'][w]['answer']))}, S {E(str(c['readers'][w]['cf_answer']))}"
            for w in I.READERS
        )
    if it["kind"] == "x8":
        digits = [d for _, d in C.LOCKER.findall(c["context"])]
        j, k = it["x8"]["j"], it["x8"]["k"]
        third = ({0, 1, 2} - {j, k}).pop()
        return (f"<b>Slots</b> {E(' · '.join(f'{n}: {d}' for n, d in enumerate(digits)))}; write j = {j} → k = {k}: "
                f"target {E(digits[k])}, original {E(digits[j])}, third {E(digits[third])}; recall answer "
                f"{E(str(c['readers']['PM']['answer']))}")  # fmt: skip
    return "; ".join(f"{I.READER_NAME[w]}: org {E(str(c['readers'][w]['answer']))}, cf (swapped) "
                     f"{E(str(c['readers'][w]['cf_answer']))}" for w in I.READERS)  # fmt: skip


def stored_label(it: dict, w: str, r: dict) -> str:
    if it["kind"] == "routes":
        return I.route_class(r, it["condition"]) if w == "PP" else ("follows S" if r["switched"] else "stays")
    if it["kind"] == "x8":
        return r.get("class") or ("changed" if r.get("changed") else "unchanged")
    return r["role"]


def card(it: dict, seed: int, server: bool, mark: dict | None) -> str:
    c, m, w0 = it["case"], it["model"], it["reader"]
    x8 = it["x8"]
    head = (f"{E(I.spec()['models'][m]['label'])} · L{it['layer']} · {E(it['run'].split('/')[-1])} · {E(it['scene'])} · "
            f"{I.READER_NAME[w0]}" + (f" · {it['condition']}" if it["condition"] else "")
            + (f" · {x8['kind']} j = {x8['j']} → k = {x8['k']}, s = {x8['s']:g}" if x8 else ""))  # fmt: skip
    status = "" if it["in_set"] else " " + tag(it["status"], "st")
    parts = [f"<div class='card{'' if it['in_set'] else ' outside'}'><div class='hdr'>{head}{status}</div>"
             f"<div class='mut' style='font-size:11px'>{E(it['id'])}</div>"]  # fmt: skip
    if c is None:
        parts.append("<p>No case for this scene in the run's cases.jsonl.</p></div>")
        return "".join(parts)
    alt_note = " (the routes case's S: not read by x8)" if x8 else ""
    parts.append("<table><tr><th style='width:50%'>original (org / O)</th><th>alt (cf / S)" + alt_note + "</th></tr>"
                 f"<tr><td class='prompt'>{marked(c['context'], c['cf_context'])}</td>"
                 f"<td class='prompt'>{marked(c['cf_context'], c['context'])}</td></tr></table>")  # fmt: skip
    qs = " &nbsp; ".join(f"<span class='{'me' if w == w0 else 'mut'}'>{I.READER_NAME[w]}: {E(c['readers'][w]['question'])}</span>"
                         for w in I.READERS)  # fmt: skip
    parts.append(f"<p>{qs}<br>bridge <b>{E(c['bridge'])}</b> → <b>{E(c['cf_bridge'])}</b> at token {c['pos']}. "
                 f"{expected_html(it)}</p>")  # fmt: skip
    rd = c["readers"][w0]
    diff = set(C.diff_positions(it))
    parts.append(f"<details><summary>tokens as the model saw them ({I.READER_NAME[w0]}; the change is added at "
                 f"<span class='toks'><span class='at'>{c['pos']}</span></span>, differing tokens marked)</summary>"
                 f"<p class='mut'>org</p>{tokens_html(m, rd['ids']['org'], c['pos'], diff)}"
                 f"<p class='mut'>alt</p>{tokens_html(m, rd['ids']['alt'], c['pos'], diff)}</details>")  # fmt: skip
    rows = ["<table><tr><th>reader</th><th>arm</th><th>top token</th><th>stored label</th><th>p_org</th><th>p_alt</th>"
            "<th>ld</th></tr>"]  # fmt: skip
    for w in sorted(I.READERS, key=lambda x: x != w0):
        for label, r in it["rows"][w].items():
            if r is None:
                rows.append(
                    f"<tr class='mut'><td>{I.READER_NAME[w]}</td><td>{E(label)}</td><td colspan=5>not in the run</td></tr>"
                )
                continue
            top = E(repr(C.piece(m, r["top"]))) if "top" in r else "<span class='mut'>not stored</span>"
            run = f" <span class='mut'>({E(r['_run'])})</span>" if "_run" in r else ""
            lab = stored_label(it, w, r)
            rows.append(f"<tr class='{'me' if w == w0 else ''}'><td>{I.READER_NAME[w]}</td><td>{E(label)}{run}</td><td>{top}</td>"
                        f"<td>{tag(lab)}</td><td>{r.get('p_org', '–')}</td><td>{r.get('p_alt', '–')}</td><td>{r.get('ld', '–')}</td></tr>")  # fmt: skip
    rows.append("</table>")
    parts.append("".join(rows))
    if it["shares"]:
        parts.append("<p class='mut'>shares: " + ", ".join(f"{E(k)} {v:.3f}" if isinstance(v, float) else f"{E(k)} {v}"
                                                          for k, v in it["shares"].items()) + "</p>")  # fmt: skip
    badges = " ".join(f"<span class='tag {st.replace('/', '')}' title='{E(d)}'>{E(n)}: {st}</span>"
                      for n, (st, d) in C.run_checks(it).items())  # fmt: skip
    parts.append(f"<p>{badges}</p>")
    prev = (
        f"<span class='mut'>last mark: {E(mark['verdict'])} ({E(mark.get('utc', ''))[:16]}) {E(mark.get('note', ''))}</span>"
        if mark
        else ""
    )
    parts.append(f"<form class='marks' onsubmit='return mark(this)'><input type='hidden' name='view' value='{E(it['view'])}'>"
                 f"<input type='hidden' name='item' value='{E(it['id'])}'><input type='hidden' name='seed' value='{seed}'>"
                 + "".join(f"<label><input type='radio' name='verdict' value='{v}'>{v}</label>" for v in ("consistent", "wrong", "unclear"))
                 + "<input type='text' name='note' placeholder='note'><button>save</button><span class='saved mut'></span>"
                 f"{prev}</form></div>")  # fmt: skip
    return "".join(parts)


def controls(v: dict, p: dict, server: bool) -> str:
    if not server:
        return (f"<p class='mut'>Static export: seed {p['seed']}, N = {p['n']} per model, {p['mode']}"
                + "".join(f", {k} {p[k]}" for k in ("reader", "condition", "s", "kind") if p.get(k) not in (None, "", "all"))
                + ". Marks are kept in this browser; use “download marks”.</p>")  # fmt: skip

    def sel(name, opts):
        return (
            f"<label>{name}<select name='{name}'>"
            + "".join(
                f"<option {'selected' if str(p.get(name, '')) == str(o) else ''}>{E(str(o))}</option>" for o in opts
            )
            + "</select></label>"
        )

    models = ["all", *I.spec()["models"]]
    extra = ""
    if v["kind"] == "routes":
        extra += sel("condition", ["all", *v["filters"].get("conditions", [])])
    if v["kind"] == "x8":
        extra += sel("s", ["all", *v["filters"].get("s", [])]) + sel("kind", ["all", *v["filters"].get("kinds", [])])
    sup = (f"<label><span><input type='checkbox' name='superseded' value='1' {'checked' if p.get('superseded') else ''}>"
           "superseded runs</span></label>") if v.get("superseded") else ""  # fmt: skip
    return (f"<form class='ctl box' method='get' action='/view'><input type='hidden' name='view' value='{E(v['id'])}'>"
            f"<label>seed<input name='seed' type='number' value='{p['seed']}' style='width:6em'></label>"
            f"<label>N<input name='n' type='number' value='{p['n']}' style='width:5em'></label>"
            + sel("mode", ["uniform", "stratified"]) + sel("model", models) + sel("reader", ["all", *I.READERS]) + extra
            + f"<label><span><input type='checkbox' name='out' value='1' {'checked' if p.get('out') else ''}>outside the claim's set"
            f"</span></label>{sup}<button>show</button></form>")  # fmt: skip


def claim_box(v: dict) -> str:
    runs = "".join(
        f"<li>{E(I.spec()['models'][m]['label'])}: {', '.join(E(r) for r in rs)}</li>"
        for m, rs in v.get("runs", {}).items()
    )
    classes = I.spec()["kinds"][v["kind"]]["classes"]
    cls = "; ".join(f"{tag(k)} {E(str(d))}" for k, d in classes.items())
    return (
        f"<div class='box'><p><b>Claim.</b> {E(v['claim'])}</p><p class='mut'>README: {E(v.get('readme', ''))}</p>"
        f"<p class='mut'>Sources (docs/x0_numbers.json): {E(', '.join(v.get('sources', [])) or 'none yet')}</p>"
        f"<p class='mut'>Filters: {E(json.dumps(v.get('filters', {})))}</p><ul class='mut'>{runs}</ul>"
        f"<p style='font-size:12.5px'>Classes: {cls}</p>"
        + (f"<p class='mut'>{E(v['notes'])}</p>" if v.get("notes") else "")
        + "</div>"
    )


def checks_box(stats: dict[str, dict]) -> str:
    rows = [
        "<table><tr><th>model</th><th>items (lookup / recall)</th>"
        + "".join(f"<th>{E(c)}</th>" for c in C.CHECKS)
        + "</tr>"
    ]
    findings = []
    for m, s in stats.items():
        cells = "".join(
            f"<td>{tag(str(s['fail'][c]), 'fail') if s['fail'].get(c) else tag('0', 'pass')}"
            + (f" <span class='mut'>n/a {s['na'][c]}</span>" if s["na"].get(c) else "") + "</td>" for c in C.CHECKS)  # fmt: skip
        rows.append(
            f"<tr><td>{E(I.spec()['models'][m]['label'])}</td><td>{s['n_reader'].get('PP', 0)} / {s['n_reader'].get('PM', 0)}</td>{cells}</tr>"
        )
        for c, ex in s["examples"].items():
            findings += [f"<li>{E(c)}: {E(e)}</li>" for e in ex[:20]]
    rows.append("</table>")
    found = f"<p><b>Findings</b> (automatic checks that disagree with the stored data):</p><ul>{''.join(findings)}</ul>" if findings else (
        "<p class='mut'>No automatic check disagrees with the stored data over the whole item set.</p>")  # fmt: skip
    return (
        "<div class='box'><b>Automatic checks over the whole item set</b> (counted over every item, not the sample)"
        + "".join(rows)
        + found
        + "</div>"
    )


def recount_box(rows: list[dict]) -> str:
    """The view's headline numbers recounted over the whole item set, beside data.csv (mismatches first)."""
    if not rows:
        return ""
    count = {s: sum(r["status"] == s for r in rows) for s in ("match", "mismatch", "no source")}
    head = (f"<b>Recount from the per-item files</b> (whole item set): {tag(str(count['match']), 'pass')} match, "
            f"{tag(str(count['mismatch']), 'fail' if count['mismatch'] else 'pass')} mismatch, {count['no source']} no source "
            "(figures/story/data.csv, 2 decimals)")  # fmt: skip
    order = sorted(rows, key=lambda r: (r["status"] != "mismatch", r["status"] == "no source"))
    table = [
        "<table><tr><th>model</th><th>quantity</th><th>n</th><th>recount</th><th>data.csv</th><th>key</th><th></th></tr>"
    ]
    for r in order:
        cls = {"match": "pass", "mismatch": "fail"}.get(r["status"], "na")
        table.append(f"<tr><td>{E(I.spec()['models'][r['model']]['key'])}</td><td>{E(r['quantity'])}</td><td>{r['n']}</td>"
                     f"<td>{r['value']:.4f}</td><td>{E(r['data'])}</td><td class='mut'>{E(r['key'])}</td><td>{tag(r['status'], cls)}</td></tr>")  # fmt: skip
    table.append("</table>")
    return f"<div class='box'>{head}<details{' open' if count['mismatch'] else ''}><summary>all rows</summary>{''.join(table)}</details></div>"


def view_page(
    v: dict, p: dict, samples: dict[str, Any], stats: dict, server: bool, commit: str, marks: dict, recount: list[dict]
) -> str:
    seed = int(p["seed"])
    body = [f"<p><a href='{'/' if server else 'index.html'}'>← all views</a></p><h1>{E(v['title'])}</h1>", controls(v, p, server),
            claim_box(v), recount_box(recount), checks_box(stats), "<p><button onclick='download()'>download marks</button> "
            "<span class='mut'>(also kept in this browser)</span></p>"]  # fmt: skip
    for section, label in (("set", "Sample from the claim's item set"), ("out", "Outside the claim's set (ineligible or beyond the first N)"),
                           ("superseded", "Superseded runs")):  # fmt: skip
        per_model = samples.get(section)
        if not per_model:
            continue
        body.append(f"<h2>{label}</h2>")
        for m, strata in per_model.items():
            body.append(f"<h3>{E(I.spec()['models'][m]['label'])}</h3>")
            if not any(s["population"] for s in strata):
                body.append("<p class='mut'>No items (run not landed, or no per-item file lists them).</p>")
            for s in strata:
                if s["stratum"] != "all" or section != "set":
                    body.append(
                        f"<p class='mut'>stratum <b>{E(s['stratum'])}</b>: {len(s['items'])} of {s['population']}</p>"
                    )
                else:
                    body.append(
                        f"<p class='mut'>{len(s['items'])} of {s['population']} items, uniform, seed {seed}</p>"
                    )
                body += [card(it, seed, server, marks.get(it["id"])) for it in s["items"]]
    return page(v["title"], "".join(body), server, commit)


def index_page(rows: list[tuple[dict, dict, list[dict]]], server: bool, commit: str, seed: int, n: int) -> str:
    body = ["<h1>Review: read the claims' items by hand</h1><p class='mut'>Each view is one README claim (docs/review_views.yaml); "
            f"items come from the runs' per-item files, decoded with the pinned tokenizers. Commit {E(commit)}.</p><table>"
            "<tr><th>view</th><th>items per model (lookup + recall)</th><th>automatic-check failures</th>"
            "<th>recount vs data.csv</th></tr>"]  # fmt: skip
    for v, stats, rec in rows:
        params = {"view": v["id"], "seed": seed, "n": n, **v.get("export", {})}
        counts = ", ".join(f"{I.spec()['models'][m]['key']} {s['n']}" for m, s in stats.items())
        fails = sum(sum(s["fail"].values()) for s in stats.values())
        mism = sum(r["status"] == "mismatch" for r in rec)
        match = sum(r["status"] == "match" for r in rec)
        body.append(f"<tr><td><a href='{link(params, server)}'>{E(v['title'])}</a></td><td>{counts}</td>"
                    f"<td>{tag(str(fails), 'fail' if fails else 'pass')}</td><td>{match} match, "
                    f"{tag(str(mism), 'fail' if mism else 'pass')} mismatch</td></tr>")  # fmt: skip
    body.append("</table>")
    return page("Review", "".join(body), server, commit)
