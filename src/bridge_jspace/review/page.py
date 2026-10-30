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
PARAMS = ("view", "seed", "n", "mode", "model", "reader", "condition", "s", "kind", "group", "out", "superseded")
# beyond these, a view's own facets (filters.facets: 45a's move, 45d's format, 45e's control, 45g's scenes)

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
.marks{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:8px}.ans{background:var(--bg);border-left:3px solid var(--id);padding:6px 10px;margin:8px 0}.ans .tag{font-family:ui-monospace,Menlo,monospace}.marks input[type=text]{flex:1;min-width:200px}
.ins{outline:2px dashed var(--val);outline-offset:1px}.toks span.rl{background:var(--line)}.toks span.ri{background:var(--id);color:#fff}
.toks span.rv{background:var(--val);color:#fff}.toks span.rf{background:var(--third);color:#fff}.grid td,.grid th{text-align:center}
.grid td:first-child,.grid th:first-child{text-align:left}.wrap{overflow-x:auto}
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


def tokens_html(model: str, ids: list[int], pos: int, diff: set[int], classes: dict[int, str] | None = None) -> str:
    """classes: a colour class per position, in place of the change's position / the differing tokens (the sweep)."""
    out = []
    for i, t in enumerate(ids):
        s = C.piece(model, t).replace(" ", "␣").replace("\n", "↵")
        cls = classes.get(i, "") if classes is not None else "at" if i == pos else "df" if i in diff else ""
        out.append(f"<span class='{cls}' title='{i}: {t}'>{E(s)}</span>")
    return "<div class='toks'>" + "".join(out) + "</div>"


def marked(text: str, other: str) -> str:
    """The text with the words that differ from the other prompt highlighted (position by position)."""
    a, b = re.split(r"(\s+)", text), re.split(r"(\s+)", other)
    if len(a) != len(b):
        return E(text)
    return "".join(f"<mark>{E(x)}</mark>" if x != y and x.strip() else E(x) for x, y in zip(a, b, strict=True))


PLAIN = {"b": "changed answer", "A": "original answer", "other": "another token", "switch": "changed answer",
         "follows S": "follows the change", "stays": "original answer", "changed": "changed", "unchanged": "unchanged"}  # fmt: skip
ARM_NAME = {"unedited": "no change", "whole": "the whole change", "unwritten": "no write"}
SWEEP_END = {"none": "O unedited", "S": "S read on S (unedited)"}  # the 45b sweep's two arms without a layer
SHARE_NAME = {"jpp": "J++ part", "alf": "pointer directions", "random part": "its random part", "A": "probe subspace",
              "Alf": "pointer directions", "V": "value subspace", "pca": "main directions", "id": "identity",
              "idout": "identity outside J++", "both": "J++ and the pointer", "jpp50": "J++ part (k = 50)",
              "jpp100": "J++ part (k = 100)", "jppother100": "another scene's 100 atoms, refit here",
              "jpp_other": "another scene's atoms, refit here",
              # 45d: each part's random part (x0b_generalize's shares.jsonl) and the refit basis
              "jpp_rand": "J++'s random part", "alf_rand": "the pointer's random part", "pcf": "the refit basis",
              "pcf_rand": "the refit basis's random part",
              # 45e (x6_routes --identity --identity-controls) and 45g (x0_massmean two_routes)
              "wrong": "the wrong-pair control", "alf+idout": "the pointer and identity outside J++",
              "jpp+alf+idout": "J++, the pointer and identity outside J++",
              "jpp+alf+wrong": "J++, the pointer and the wrong-pair control",
              "jpp+alf+pca": "J++, the pointer and the main directions", "idsub": "the identity subspace",
              "jppAlf": "J++ and the pointer (their union)"}  # fmt: skip
GEOMETRY_NAME = {"cos2_U": "mean cos² with the pointer directions", "cos2_id": "cos² with the identity direction"}

LEGEND = """<details class='box'><summary><b>How to read a card</b></summary><ul>
<li><b>Original prompt</b>: what the model reads. <b>Changed prompt</b>: the same scene with the bridge (the asked
person's pick) changed; the change is taken from it. Words that differ are highlighted.</li>
<li><b>The change</b>: the difference of the model's hidden state at the bridge word (changed minus original), at the
layer shown, added to the original prompt there. <b>The whole change</b>: all of it. <b>Without X</b>: the change minus
its X part. <b>Without its random part</b>: minus a random part of the same size (the control). <b>Only X</b>: only the
X part added.</li>
<li><b>Original answer</b>: the answer to the original prompt; <b>changed answer</b>: the answer to the changed prompt.
The model <b>switches</b> when it gives the changed answer. Lookup: the locker written in the prompt; recall: a fact
from memory.</li>
<li><b>P(original answer)</b>, <b>P(changed answer)</b>: the probability the model gives each answer's first token.
<b>Logit gap</b>: logit of the changed answer minus logit of the original; above 0 the changed answer is preferred.</li>
<li><b>What it is</b>: the run's own label for the top token (its code in brackets: A = original answer, b = changed
answer). The main test stores no top token, only this label, so "another token" cannot be shown.</li>
<li><b>Extra loss</b>: (switches kept without the random part − switches kept without the part) / switches with the
whole change. An item counts only if the whole change switched it.</li></ul></details>"""


def expected_html(it: dict) -> str:
    c = it["case"]
    rd = c["readers"]
    if it["kind"] == "x5":
        return (f"Relation: {E(str(c.get('relation', '')))} ({E(str(c.get('genre', '')))}). " + " ".join(
            f"{I.READER_NAME[w].capitalize()}: original answer {E(str(rd[w]['answer']))}, changed answer "
            f"{E(str(rd[w]['cf_answer']))}." for w in I.READERS)
            + f" The passage's own value for the bridge (what a recall that reads the passage would say): "
              f"{E(str(rd['PM'].get('lure', '–')))} → {E(str(rd['PM'].get('cf_lure', '–')))}.")  # fmt: skip
    if it["kind"] == "routes":
        exp = ", ".join(f"{k} {v}" for k, v in c["expect"].items())
        return (f"Lookup, the answer each route predicts: {E(exp)}. Recall: original answer {E(str(rd['PM']['answer']))} "
                f"({E(c['bridge'])}), changed answer {E(str(rd['PM']['cf_answer']))} ({E(c['cf_bridge'])}).")  # fmt: skip
    if it["kind"] == "x8":
        digits = [d for _, d in C.LOCKER.findall(c["context"])]
        j, k = it["x8"]["j"], it["x8"]["k"]
        third = ({0, 1, 2} - {j, k}).pop()
        items = [x for x, _ in C.LOCKER.findall(c["context"])]
        lg = I.legs()
        return (f"Locker sentences in order: {E(', '.join(f'slot {n}: {x} → locker {d}, {lg[x]} legs' for n, (x, d) in enumerate(zip(items, digits, strict=True))))}. "
                f"The write moves the pointer from slot {j} (the bridge's) to slot {k}. Lookup: target {E(digits[k])}, "
                f"original {E(digits[j])}, third {E(digits[third])}. Recall: target item {lg[items[k]]} legs, original "
                f"{lg[items[j]]} ({E(str(rd['PM']['answer']))} is O's answer), third {lg[items[third]]}.")  # fmt: skip
    return " ".join(f"{I.READER_NAME[w].capitalize()}: original answer {E(str(rd[w]['answer']))}, changed answer "
                    f"{E(str(rd[w]['cf_answer']))}." for w in I.READERS)  # fmt: skip


def bridge_html(it: dict) -> str:
    c = it["case"]
    if c["bridge"] == c["cf_bridge"]:
        return (f"The bridge, the asked person's pick, is <b>{E(c['bridge'])}</b> in both prompts (token {c['pos']}); the "
                "prompts differ in the highlighted words.")  # fmt: skip
    text = (f"The bridge, the asked person's pick, is <b>{E(c['bridge'])}</b> in the original prompt and "
            f"<b>{E(c['cf_bridge'])}</b> in the changed one; the change is added at its token ({c['pos']}).")  # fmt: skip
    o = it.get("order") or {}
    if it["kind"] == "x5":
        text = (f"The bridge, the entity the questions are about, is <b>{E(c['bridge'])}</b> in the original passage and "
                f"<b>{E(c['cf_bridge'])}</b> in the changed one (its binding sentence only); the change is added at its token "
                f"({c['pos']}).")  # fmt: skip
    if o and it["kind"] == "x5":
        word = {"before": "<b>before</b>", "after": "<b>after</b>", "not found": "(not found)"}
        return text + (f"<br>Sentence order: the sentence with {E(c['bridge'])}'s fact comes {word[o['original']]} the "
                       f"bridge's mention; {E(c['cf_bridge'])}'s fact comes {word[o['changed']]} it (the lookup switches "
                       "mostly where the fact comes first).")  # fmt: skip
    if o:
        word = {"before": "<b>before</b>", "after": "<b>after</b>", "not found": "(not found)"}
        first = " (locker-first: the items the lookup claims are about)" if o["original"] == "before" else ""
        noun = "locker statement" if it["kind"] == "x45d" else "locker sentence"  # 45d: a JSON object or a table row
        text += (f"<br>Sentence order: in the original prompt, {E(c['bridge'])}'s {noun} comes "
                 f"{word[o['original']]} the asked pick{first}; in the changed prompt, {E(c['cf_bridge'])}'s {noun} "
                 f"comes {word[o['changed']]} it.")  # fmt: skip
    return text


def shares_html(shares: dict) -> str:
    parts = []
    for k, v in shares.items():
        if k in ("norm", "write norm"):
            parts.append(f"{'size of the change' if k == 'norm' else 'size of the write'} {v:.1f}")
        else:
            base, _, kk = k.partition("_k")
            name = str(SHARE_NAME.get(base, base)) + (f" (k = {kk})" if kk else "")
            parts.append(f"{E(str(name))} {100 * v:.0f}%")
    return "<p class='mut'>Share of the change's size (squared) in: " + ", ".join(parts) + "</p>"


def stored_label(it: dict, w: str, r: dict) -> str:
    if it["kind"] in ("routes", "x45a_prepend"):
        return I.route_class(r, it["condition"]) if w == "PP" else ("follows S" if r["switched"] else "stays")
    if it["kind"] == "x8":
        return r.get("class") or ("changed" if r.get("changed") else "unchanged")
    if it["kind"] == "identity_address":  # 53.6: whose answer the top token is (original / B / C / other)
        return r["class"]
    return I.whole_class(r, it["case"], w)


def answer_of(it: dict, w: str, r: dict) -> tuple[str, str]:
    """The answer an arm's top token gives, and what it is. The main test stores no top token, but its role names it:
    A = the original answer's token, b = the swapped answer's; other = a token the run did not store."""
    c, rd = it["case"], it["case"]["readers"][w]
    if "top" not in r:
        if r["role"] == "b":
            return str(rd["cf_answer"]), f"changed answer ({c['cf_bridge']}'s)"
        if r["role"] == "A":
            return str(rd["answer"]), f"original answer ({c['bridge']}'s)"
        return "?", "another token (not stored)"
    d = C.top_text(it["model"], r["top"]).strip()
    if it["kind"] == "routes" and w == "PP":
        route = I.route_class(r, it["condition"])
        return d, {"switch": "changed answer", "original": "original answer"}.get(route, f"{route} route")
    if it["kind"] == "x8" and w == "PP":
        cls = r["class"]
        return d, f"slot {cls[4:]}'s digit" if cls.startswith("slot") else cls
    if it["kind"] == "x8":  # the recall: whose legs (target, third, original slot's item; first match), as stage_recall
        if d == str(rd["answer"]):
            return d, f"original answer ({c['bridge']}'s legs)"
        items, x8 = [x for x, _ in C.LOCKER.findall(c["context"])], it["x8"]
        third = ({0, 1, 2} - {x8["j"], x8["k"]}).pop()
        lg = I.legs()
        for name, s in (("target", x8["k"]), ("third", third), ("original", x8["j"])):
            if d == str(lg[items[s]]):
                return d, f"{name} slot's item ({items[s]}'s legs)"
        return d, "another answer"
    who = (f"changed answer ({c['cf_bridge']}'s)" if d == str(rd["cf_answer"]) else
           f"original answer ({c['bridge']}'s)" if d == str(rd["answer"]) else "another answer")  # fmt: skip
    return d, who


def answer_class(what: str) -> str:
    """The colour of an answer by what it is."""
    for prefix, cls in (("changed", "ok"), ("original", "org"), ("identity", "id"), ("position", "pos"), ("value", "val"),
                        ("target", "ok"), ("third", "third"), ("slot", "org")):  # fmt: skip
        if what.startswith(prefix):
            return cls
    return "oth"


def contribution(it: dict, w: str) -> list[str]:
    """How this item counts in the view's extra loss: only items the whole change switched are counted; +1 when the
    switch is lost without the part and kept without its random part, -1 the reverse, 0 otherwise."""
    v = I.view(it["view"])
    h = v.get("headline")
    entries = [h] if isinstance(h, dict) else h or []
    pairs = []
    for e in entries:
        usable = (
            "part" in e
            and e.get("random")
            and e.get("stat", "extra_loss") in ("extra_loss", "ld_extra", "gap", "extra_loss_minus")
        )
        mine = e.get("reader", w) == w and e.get("condition", it["condition"]) == it["condition"]
        if usable and mine and (e["part"], e["random"]) not in pairs:
            pairs.append((e["part"], e["random"]))
    rows = it["rows"][w]
    whole = rows.get("whole")
    if not pairs or whole is None:
        return []
    if not whole["switched"]:
        return ["the whole change did not switch it, so it is not among the switches the extra loss counts"]
    out = []
    for part, rand in pairs:
        rp, rr = rows.get(part), rows.get(rand)
        if rp is None or rr is None:
            continue
        lost_p, lost_r = not rp["switched"], not rr["switched"]
        n = int(lost_p) - int(lost_r)
        out.append(f"the whole change switched it; {part}: the switch is {'lost' if lost_p else 'kept'}; {rand}: "
                   f"{'lost' if lost_r else 'kept'} → this item adds {n:+d} to the extra loss's numerator")  # fmt: skip
    return out


def answers_html(it: dict) -> str:
    """What the model answered, per reader: before the change, then under each arm, with what each answer is."""
    c, w0 = it["case"], it["reader"]
    out = ["<div class='ans'><b>What the model answered</b>"]
    for w in sorted(I.READERS, key=lambda x: x != w0):
        rows = [(label, r) for label, r in it["rows"][w].items() if r is not None]
        if not rows:
            continue
        rd = c["readers"][w]
        key = (f"original answer {E(str(rd['answer']))} = {E(c['bridge'])}'s; changed answer {E(str(rd['cf_answer']))} = "
               f"{E(c['cf_bridge'])}'s" if it["kind"] != "x8" else f"original answer {E(str(rd['answer']))}")  # fmt: skip
        steps = []
        for i, (label, r) in enumerate(rows):
            ans, what = answer_of(it, w, r)
            name = (
                "before the change"
                if i == 0 and label in ("unedited", "unwritten")
                else E(str(ARM_NAME.get(label, label)))
            )
            steps.append(
                f"{name} <span class='tag {answer_class(what)}'>{E(ans)}</span> <span class='mut'>{E(what)}</span>"
            )
        first, rest = steps[0], steps[1:]
        line = first + (" &nbsp;→&nbsp; " + " · ".join(rest) if rest else "")
        notes = "".join(f"<br><span class='mut'>{E(n)}</span>" for n in contribution(it, w))
        out.append(f"<p class='{'me' if w == w0 else ''}' style='margin:6px 0'><b>{I.READER_NAME[w]}</b>: "
                   f"{E(rd['question'])} <span class='mut'>({key})</span><br>{line}{notes}</p>")  # fmt: skip
    out.append("</div>")
    return "".join(out)


def arm_name(it: dict, label: str) -> str:
    """An arm's name on a card: the view's label, or for the sweep its stored name read out (bw16 -> bridge word at L16)."""
    if it["kind"] == "x45b_sweep":
        sw = I.sweep_arm(label)
        return f"{label}: {I.SWEEP_KINDS[sw[0]]} at L{sw[1]}" if sw else SWEEP_END.get(label, label)
    if it["kind"] == "x45a_prepend":  # "<variant> · <arm label>"
        x, _, arm = label.partition(I.SEP)
        return f"{x}: {ARM_NAME.get(arm, arm)}"
    return str(ARM_NAME.get(label, label))


def numbers_html(it: dict) -> str:
    """The stored numbers per arm and reader (the sampled reader first)."""
    m, w0 = it["model"], it["reader"]
    rows = ["<details><summary>the stored numbers per change</summary><table><tr><th>reader</th><th>change applied</th>"
            "<th>top token</th><th>what it is (run's label)</th><th>P(original answer)</th><th>P(changed answer)</th>"
            "<th>logit gap (changed − original)</th></tr>"]  # fmt: skip
    for w in sorted(I.READERS, key=lambda x: x != w0):
        for label, r in it["rows"][w].items():
            name = E(arm_name(it, label))
            if r is None:
                rows.append(
                    f"<tr class='mut'><td>{I.READER_NAME[w]}</td><td>{name}</td><td colspan=5>not in the run</td></tr>"
                )
                continue
            top = E(repr(C.top_text(m, r["top"]))) if "top" in r else "<span class='mut'>not stored</span>"
            run = f" <span class='mut'>(run {E(r['_run'])})</span>" if "_run" in r else ""
            lab = stored_label(it, w, r)
            plain = PLAIN.get(lab, lab) + (f" ({lab})" if lab in ("A", "b") else "")
            rows.append(f"<tr class='{'me' if w == w0 else ''}'><td>{I.READER_NAME[w]}</td><td>{name}{run}</td><td>{top}</td>"
                        f"<td>{tag(plain, CLASS_COLOR.get(lab, 'st'))}</td><td>{r.get('p_org', '–')}</td><td>{r.get('p_alt', '–')}</td>"
                        f"<td>{r.get('ld', '–')}</td></tr>")  # fmt: skip
    rows.append("</table></details>")
    return "".join(rows)


def checks_and_form(it: dict, seed: int, mark: dict | None) -> str:
    """The automatic checks' badges and the hand-mark form; closes the card."""
    badges = " ".join(f"<span class='tag {st.replace('/', '')}' title='{E(d)}'>{E(n)}: {st}</span>"
                      for n, (st, d) in C.run_checks(it).items())  # fmt: skip
    prev = (
        f"<span class='mut'>last mark: {E(mark['verdict'])} ({E(mark.get('utc', ''))[:16]}) {E(mark.get('note', ''))}</span>"
        if mark
        else ""
    )
    return (f"<p>{badges}</p><form class='marks' onsubmit='return mark(this)'><input type='hidden' name='view' value='{E(it['view'])}'>"
            f"<input type='hidden' name='item' value='{E(it['id'])}'><input type='hidden' name='seed' value='{seed}'>"
            + "".join(f"<label><input type='radio' name='verdict' value='{v}'>{v}</label>" for v in ("consistent", "wrong", "unclear"))
            + "<input type='text' name='note' placeholder='note'><button>save</button><span class='saved mut'></span>"
            f"{prev}</form></div>")  # fmt: skip


def outlined(html_text: str, sentence: str) -> str:
    """An escaped prompt with one sentence outlined (45m's inserted sentence; it is the same in both prompts, so marked()
    leaves its escaped text whole)."""
    s = E(sentence)
    return html_text.replace(s, f"<span class='ins'>{s}</span>", 1)


def fresh_html(it: dict) -> str:
    """45m: the sentence inserted in both prompts (x0_necessity.fresh_pair's draws) and the scene's group."""
    c = it["case"]
    f = c.get("fresh")
    if not f:
        return ""
    where = (f"before locker sentence {f['slot'] + 1} of {f['slots'] - 1}" if f["slot"] < f["slots"] - 1
             else "after the last locker sentence")  # fmt: skip
    group = f" Group (as x45m scores it): <b>{E(it['group'])}</b>." if it.get("group") else ""
    return (f"<p>Inserted in both prompts (outlined): “{E(f['sentence'])}”: {E(str(f['item']))}, locker {E(str(f['digit']))}, "
            f"{where} (sentence {f['sentence_index'] + 1} of the context); the asked pick changes from "
            f"<b>{E(c['bridge'])}</b> to it.{group}</p>")  # fmt: skip


def geometry_html(it: dict) -> str:
    """45k: per item, norms.jsonl's geometry of each k's atoms (routes) and jpp_other's partner scene (routes, and the
    main-test control from its manifest)."""
    geo = {k: v for k, v in (it.get("more") or {}).items() if k != "controls"}  # 45e's controls: controls_html
    if it["kind"] not in ("routes", "x0_parts") or not geo:
        return ""
    parts = []
    for k, v in geo.items():
        if k == "jpp_other_partner":
            parts.append(f"jpp_other's partner scene {E(str(v))}")
        else:
            base, _, kk = k.rpartition("_jpp")
            parts.append(f"{E(GEOMETRY_NAME.get(base) or base)} (k = {E(kk)}) {'none' if v is None else f'{v:.3f}'}")
    where = "Geometry (norms.jsonl)" if it["kind"] == "routes" else "From the run's manifest"
    return f"<p class='mut'>{where}: " + "; ".join(parts) + "</p>"


def controls_html(it: dict) -> str:
    """45e: the controls' achieved share beside identity outside J++'s (their target) in this scene, alone and in the
    union with J++ and the pointer directions; the directions each control took (k_wrong, k_pca) and the same-domain
    pairs the wrong-pair control drew from (n_wrong_pool). A control below 0.9 of the target is tagged short."""
    sh, ctl = it["shares"], (it.get("more") or {}).get("controls") or {}
    if "wrong" not in sh or "idout" not in sh:
        return ""

    def vs(key: str, target: float, how: str, k: int | None = None) -> str:
        got = sh.get(key)
        if got is None:
            return f"{E(SHARE_NAME.get(key, key))} not stored"
        ratio = f"{got / target:.2f} of the target" if target > 0 else "no target"
        flag = (" " + tag("0 directions: removes nothing", "fail") if k == 0 else
                " " + tag("short of the target", "fail") if target > 0 and got < I.WRONG_SHORT * target else "")  # fmt: skip
        return f"{E(SHARE_NAME.get(key, key))} <b>{100 * got:.1f}%</b> ({ratio}{how}){flag}"

    t, u = sh["idout"], sh.get("jpp+alf+idout", 0.0)
    pool = f"; {ctl['k_wrong']} directions from {ctl['n_wrong_pool']} same-domain pairs" if "k_wrong" in ctl else ""
    pca = f"; {ctl['k_pca']} directions" if "k_pca" in ctl else ""
    return (f"<p>Controls at identity outside J++'s share (norms.jsonl): identity outside J++ <b>{100 * t:.1f}%</b> (the "
            f"target) · {vs('wrong', t, pool, ctl.get('k_wrong'))} · {vs('pca', t, pca, ctl.get('k_pca'))} (the PCA "
            f"control).<br>With J++ and the pointer directions: J++, the pointer and identity outside J++ "
            f"<b>{100 * u:.1f}%</b> · {vs('jpp+alf+wrong', u, '')} · {vs('jpp+alf+pca', u, '')}.</p>")  # fmt: skip


FORMAT_NAME = {"prose": "prose", "json": "JSON", "table": "table"}


def x45d_html(it: dict) -> str:
    """45d: the scene's format and cell, and the bridges' halves of the fit run's split (the refit basis is fit on the
    other half; the bridge must be in the held-out half)."""
    c, sp = it["case"], (it.get("more") or {}).get("split")
    if it["kind"] != "x45d" or not sp:
        return ""
    held = tag("held out", "pass") if sp["bridge"] == "test" else tag(f"bridge in the {sp['bridge']} half", "fail")
    return (f"<p>Format <b>{E(str(FORMAT_NAME.get(c['format'], c['format'])))}</b> · level {c['level']} · {E(c['domain'])} · "
            f"numbers as {E(c['numbers'])}. {held} The bridge <b>{E(c['bridge'])}</b> is in the <b>{sp['bridge']}</b> half "
            f"of {E(sp['fit_run'])}/split.json for {E(c['format'])} (its refit basis was fit on the {sp['n_fit']} bridge items "
            f"of the fit half); the changed bridge {E(c['cf_bridge'])} is in the {sp['cf_bridge']} half.</p>")  # fmt: skip


def x45g_html(it: dict) -> str:
    """45g: the scene set and the sentence order the run stored (the rule's groups), beside the case's."""
    more = it.get("more") or {}
    if it["kind"] != "x45g" or not more:
        return ""
    st = more["stored_order"]
    return (f"<p>Scene set: <b>{E(more['scene_set'])}</b> (prompts: {E(more['cases_from'])}, the run named in the "
            f"manifest's single). Stored by the run (the 45g rule's groups): org_order <b>{E(str(st['org_order']))}</b> "
            f"(the original bridge's locker sentence vs the asked pick), alt_order {E(str(st['alt_order']))} (the changed "
            "bridge's).</p>")  # fmt: skip


# ------------------------------------------------- the verification read (Dan 29 Oct 11:45): what the model saw, the arms
def seen_html(it: dict) -> str:
    """The sampled reader's prompts decoded from the stored ids exactly as the model read them (chat template, thinking
    off, "Answer:"), with the tokens the run appended at the read (a digit's space) and the change's token marked."""
    c, m, w = it["case"], it["model"], it["reader"]
    rd = c["readers"][w]
    sfx = C.read_suffix(it)
    at = c["pos"]
    edit = (it.get("more") or {}).get("edit_at")  # 51.10: the edit is at the last token

    def text(v: str) -> str:
        ids = rd["ids"][v]
        tk = C.tokenizer(m)
        before, here, after = (tk.decode(ids[:at], skip_special_tokens=False), tk.decode([ids[at]], skip_special_tokens=False),
                               tk.decode(ids[at + 1 :], skip_special_tokens=False))  # fmt: skip
        tail = tk.decode(sfx, skip_special_tokens=False) if sfx else ""
        return (f"{E(before)}<span class='tag pos' title='token {at}'>{E(here)}</span>{E(after)}"
                + (f"<span class='tag st' title='appended at the read: {sfx}'>{E(tail.replace(' ', '␣'))}</span>" if sfx else ""))  # fmt: skip

    where = (f"the change is added at the last token (the appended space, index {edit.get('org')})" if edit else
             f"the change is added at the marked token ({at})")  # fmt: skip
    sfx_note = (f"; grey: the token the run appended at the read ({E(repr(C.tokenizer(m).decode(sfx)))})" if sfx else
                "; nothing appended: the read is the next token after the template")  # fmt: skip
    return (f"<details open class='box'><summary><b>As the model saw it</b> ({I.READER_NAME[w]}; decoded from the stored ids "
            f"with the pinned tokenizer; {where}{sfx_note})</summary><table><tr><th style='width:50%'>original prompt</th>"
            f"<th>changed prompt</th></tr><tr><td class='prompt'>{text('org')}</td><td class='prompt'>{text('alt')}</td></tr>"
            "</table></details>")  # fmt: skip


def decisive_html(it: dict) -> str:
    """The view's decisive arms side by side, per reader: each arm's top token (decoded; "not stored" where the run kept
    only its label) and the pipeline's own label for it."""
    v = I.view(it["view"])
    labels = v.get("decisive") or list(next(iter(it["rows"].values())).keys())
    m, w0 = it["model"], it["reader"]
    head = "".join(f"<th>{E(arm_name(it, lb))}</th>" for lb in labels)
    body = []
    for w in sorted(I.READERS, key=lambda x: x != w0):
        cells = []
        for lb in labels:
            r = it["rows"][w].get(lb)
            if r is None:
                cells.append("<td class='mut'>not in the run</td>")
                continue
            top = (
                E(repr(C.top_text(m, r["top"]))) if r.get("top") is not None else "<span class='mut'>not stored</span>"
            )
            lab = stored_label(it, w, r)
            plain = PLAIN.get(lab, lab) + (f" ({lab})" if lab in ("A", "b") else "")
            sw = f" · switched {r['switched']}" if "switched" in r else ""
            cells.append(
                f"<td><code>{top}</code><br>{tag(plain, CLASS_COLOR.get(lab, 'st'))}<span class='mut'>{sw}</span></td>"
            )
        rd = it["case"]["readers"][w]
        who = f"{I.READER_NAME[w]}<br><span class='mut'>{E(str(rd['answer']))} → {E(str(rd['cf_answer']))}</span>"
        body.append(f"<tr class='{'me' if w == w0 else ''}'><td>{who}</td>{''.join(cells)}</tr>")
    return (f"<div class='box wrap'><b>The decisive arms</b> <span class='mut'>(top token · the run's label; the answers are "
            f"original → changed)</span><table class='grid'><tr><th>reader</th>{head}</tr>{''.join(body)}</table></div>")  # fmt: skip


def flags_html(it: dict) -> str:
    """The model's flags (the 122B's L33 rule, Lightning's ○) and the view's per-model flags (the 122B's g75)."""
    v = I.view(it["view"])
    got = [*I.spec()["models"][it["model"]].get("flags", []), *(v.get("model_flags") or {}).get(it["model"], [])]
    return "<p>" + " ".join(tag(f, "oth") for f in got) + "</p>" if got else ""


def facts_html(it: dict) -> str:
    """Per view, what a reader needs to judge the item: E1 the answer word's lens rank at the bridge word; Z1-P the made-up
    fact beside the true one; x8 the slot written to, its item and digit; 51.10 the read peak and the logit lens."""
    c, more = it["case"], it.get("more") or {}
    if it["kind"] == "x51_answer":
        rk = more.get("answer_rank") or {}
        parts = [f"{I.READER_NAME[w]}: O {E(str((rk.get('org') or {}).get(w, '–')))}, S {E(str((rk.get('alt') or {}).get(w, '–')))}"
                 for w in I.READERS]  # fmt: skip
        words = ", ".join(more.get("answer_words") or [])
        return (f"<p>The answer word's rank in the lens readout at the bridge word (readout.jsonl; above 50 = outside the "
                f"top 50): {'; '.join(parts)}. Number words used for the answer directions: {E(words)}.</p>")  # fmt: skip
    if it["kind"] == "zach" and more.get("facts"):
        f = more["facts"]
        flag = (
            tag("the true value appears in the lookup's passage", "fail")
            if f["true_in_lookup_passage"]
            else tag("the true value is absent from the lookup's passage", "pass")
        )
        same = tag("made-up = true", "fail") if str(f["made_up"]).lower() == str(f["true"]).lower() else ""
        return (f"<p>Relation <b>{E(str(f['relation']))}</b> ({E(str(f['stratum']))}). Made-up fact in the lookup's passage: "
                f"<b>{E(c['bridge'])} → {E(str(f['made_up']))}</b>; the true fact (the recall's answer, from memory): "
                f"<b>{E(c['bridge'])} → {E(str(f['true']))}</b>. Changed: {E(c['cf_bridge'])} → {E(str(f['cf_made_up']))} "
                f"(made up) / {E(str(f['cf_true']))} (true). {flag} {same}</p>")  # fmt: skip
    if it["kind"] == "x8":
        x8 = it["x8"]
        items = [x for x, _ in C.LOCKER.findall(c["context"])]
        digits = [d for _, d in C.LOCKER.findall(c["context"])]
        if len(items) == 3:
            return (f"<p>The swap writes slot <b>{x8['k']}</b> (swapped in: <b>{E(items[x8['k']])}</b>, locker "
                    f"<b>{E(digits[x8['k']])}</b>) over the bridge's slot {x8['j']} ({E(items[x8['j']])}, locker "
                    f"{E(digits[x8['j']])}) at s = {x8['s']:g}; a lookup that follows the swap answers "
                    f"<b>{E(digits[x8['k']])}</b>.</p>")  # fmt: skip
    if it["kind"] == "jread":
        ll = more.get("logit_lens_top") or {}
        dec = {v: (repr(C.top_text(it["model"], t)) if t is not None else "–") for v, t in ll.items()}
        return (f"<p>Read peak (this reader): layer <b>{more.get('peak')}</b>; the arms act at the last token there. The plain "
                f"logit lens's top token at the last token at that layer: O {E(dec.get('org', '–'))}, S "
                f"{E(dec.get('alt', '–'))}. The J++ lens readout's top words per item are not stored by the run (see the "
                f"inspector panel).</p>")  # fmt: skip
    return ""


def card(it: dict, seed: int, server: bool, mark: dict | None) -> str:
    if it["kind"] == "x45b_sweep":
        return sweep_card(it, seed, mark)
    if it["kind"] == "x45a_prepend":
        return prepend_card(it, seed, mark)
    c, m, w0 = it["case"], it["model"], it["reader"]
    x8 = it["x8"]
    cond_name = {"C0": "sanity swap", "C1": "the same item moved", "C2": "another item moved"}
    head = (f"{E(I.spec()['models'][m]['label'])} · layer {it['layer']} · run {E(it['run'].split('/')[-1])} · scene "
            f"{E(it['scene'])} · {I.READER_NAME[w0]}" + (f" · {it['condition']} ({cond_name[it['condition']]})" if it["condition"] else "")
            + (f" · {'write' if x8['kind'] == 'write' else 'random direction'} from slot {x8['j']} to slot {x8['k']}, "
               f"dose s = {x8['s']:g}" if x8 else ""))  # fmt: skip
    status = "" if it["in_set"] else " " + tag(it["status"], "st")
    parts = [f"<div class='card{'' if it['in_set'] else ' outside'}'><div class='hdr'>{head}{status}</div>"
             f"<div class='mut' style='font-size:11px'>{E(it['id'])}</div>"]  # fmt: skip
    if c is None:
        parts.append("<p>No case for this scene in the run's cases.jsonl.</p></div>")
        return "".join(parts)
    if I.view(it["view"]).get("tier") == 1:  # the verification read: what the model saw and the decisive arms first
        parts.append(flags_html(it) + seen_html(it) + facts_html(it) + decisive_html(it))
    right = ("Second prompt of the routes case (not used by the write)" if x8 else
             "Changed prompt (the change is taken from here)")  # fmt: skip
    org, alt = marked(c["context"], c["cf_context"]), marked(c["cf_context"], c["context"])
    if c.get("fresh"):
        org, alt = outlined(org, c["fresh"]["sentence"]), outlined(alt, c["fresh"]["sentence"])
    parts.append("<table><tr><th style='width:50%'>Original prompt (the model reads this)</th><th>" + right + "</th></tr>"
                 f"<tr><td class='prompt'>{org}</td><td class='prompt'>{alt}</td></tr></table>")  # fmt: skip
    qs = " &nbsp; ".join(f"<span class='{'me' if w == w0 else 'mut'}'>{I.READER_NAME[w]}: {E(c['readers'][w]['question'])}</span>"
                         for w in I.READERS)  # fmt: skip
    parts.append(f"{fresh_html(it)}{x45d_html(it)}<p>{qs}<br>{bridge_html(it) if not x8 else ''} {expected_html(it)}</p>"
                 f"{x45g_html(it)}{controls_html(it)}")  # fmt: skip
    parts.append(answers_html(it))
    rd = c["readers"][w0]
    diff = set(C.diff_positions(it))
    parts.append(f"<details><summary>tokens as the model saw them ({I.READER_NAME[w0]}; the change is added at "
                 f"<span class='toks'><span class='at'>{c['pos']}</span></span>, differing tokens marked)</summary>"
                 f"<p class='mut'>original prompt</p>{tokens_html(m, rd['ids']['org'], c['pos'], diff)}"
                 f"<p class='mut'>changed prompt</p>{tokens_html(m, rd['ids']['alt'], c['pos'], diff)}</details>")  # fmt: skip
    parts.append(numbers_html(it))
    if it["shares"]:
        parts.append(shares_html(it["shares"]))
    parts.append(geometry_html(it))
    parts.append(checks_and_form(it, seed, mark))
    return "".join(parts)


# ------------------------------------------------------------------------------------------------ the 45b sweep card
SWEEP_TOKEN = (
    ("bw", "at", "the bridge word"),
    ("li", "ri", "an item"),
    ("lv", "rv", "a value"),
    ("lf", "rf", "a sentence-final token"),
    ("ls", "rl", "another locker-sentence token"),
)  # first match wins
ROLE_CLASS = {"b": "ok", "A": "org"}


def sweep_answer(it: dict, w: str, r: dict) -> tuple[str, str]:
    """An arm's top token and what it is: S's answer (role b), O's answer (role A), or another token."""
    rd = it["case"]["readers"][w]
    d = C.top_text(it["model"], r["top"]).strip() if "top" in r else "?"
    return d, {"b": f"S's answer ({rd['cf_answer']})", "A": f"O's answer ({rd['answer']})"}.get(
        r["role"], "another token"
    )


def sweep_grid(it: dict, w: str) -> str:
    """One reader's answers: O unedited and S read on S, then a row per sweep kind and a column per layer."""
    rows, more, rd = it["rows"][w], it["more"], it["case"]["readers"][w]
    ends = []
    for a in ("none", "S"):
        if rows.get(a):
            d, what = sweep_answer(it, w, rows[a])
            ends.append(
                f"{E(arm_name(it, a))} {tag(d, ROLE_CLASS.get(rows[a]['role'], 'oth'))} <span class='mut'>{E(what)}</span>"
            )
    head = "<tr><th>patched in O</th>" + "".join(f"<th>L{la}</th>" for la in more["layers"]) + "</tr>"
    body = []
    for k in more["kinds"]:
        cells = []
        for la in more["layers"]:
            r = rows.get(f"{k}{la}")
            if r is None:
                cells.append("<td class='mut'>–</td>")
                continue
            d, what = sweep_answer(it, w, r)
            cells.append(f"<td title='{E(what)}; P(O) {r.get('p_org', '–')}, P(S) {r.get('p_alt', '–')}'>"
                         f"{tag(d, ROLE_CLASS.get(r['role'], 'oth'))}</td>")  # fmt: skip
        body.append(f"<tr><td>{k}: {E(I.SWEEP_KINDS[k])}</td>{''.join(cells)}</tr>")
    return (f"<p class='{'me' if w == it['reader'] else ''}' style='margin:6px 0'><b>{I.READER_NAME[w]}</b>: "
            f"{E(rd['question'])} <span class='mut'>(O's answer {E(str(rd['answer']))}, S's answer {E(str(rd['cf_answer']))})"
            f"</span><br>{' &nbsp;·&nbsp; '.join(ends)}</p><div class='wrap'><table class='grid'>{head}{''.join(body)}</table></div>")  # fmt: skip


def sweep_card(it: dict, seed: int, mark: dict | None) -> str:
    """The 45b sweep: O's tokens with every patch position coloured by what patches it, the positions per kind (the same
    at every layer), and each arm's answer per layer for both readers (green S's answer, grey O's, amber another)."""
    c, m, w0, more = it["case"], it["model"], it["reader"], it["more"]
    lo, hi = (more["layers"][0], more["layers"][-1]) if more["layers"] else ("?", "?")
    head = (f"{E(I.spec()['models'][m]['label'])} · L {it['layer']} (sweep L{lo}–L{hi}) · run {E(it['run'].split('/')[-1])} "
            f"· scene {E(it['scene'])} · {I.READER_NAME[w0]}")  # fmt: skip
    parts = [
        f"<div class='card'><div class='hdr'>{head}</div><div class='mut' style='font-size:11px'>{E(it['id'])}</div>"
    ]
    if c is None:
        return "".join(parts) + "<p>No case for this scene in the run's cases.jsonl.</p></div>"
    parts.append("<table><tr><th style='width:50%'>O, the original prompt (the model reads this)</th><th>S, the swapped "
                 "prompt (the patches are taken from here)</th></tr>"
                 f"<tr><td class='prompt'>{marked(c['context'], c['cf_context'])}</td>"
                 f"<td class='prompt'>{marked(c['cf_context'], c['context'])}</td></tr></table>")  # fmt: skip
    rd = c["readers"][w0]
    ids = rd["ids"]["org"]
    where = I.sweep_positions(c)
    classes: dict[int, str] = {}
    for k, cls, _ in SWEEP_TOKEN:
        for p in where.get(k, []):
            classes.setdefault(p, cls)
    legend = " ".join(f"<span class='toks'><span class='{cls}'>{E(name)}</span></span>" for k, cls, name in SWEEP_TOKEN
                      if k in where)  # fmt: skip
    pos_lines = []
    for k in more["kinds"]:
        ps = where.get(k, [])
        listed = (f"{len(ps)} tokens between positions {ps[0]} and {ps[-1]} (each marked above)" if k == "ls" and ps else
                  ", ".join(f"{p} {E(repr(C.piece(m, ids[p])))}" for p in ps) or "none stored")  # fmt: skip
        pos_lines.append(f"<li>{k} ({E(I.SWEEP_KINDS[k])}): {listed}</li>")
    parts.append(f"<p>The bridge, the asked person's pick, is <b>{E(c['bridge'])}</b> in O and <b>{E(c['cf_bridge'])}</b> in "
                 f"S (token {c['pos']}). Locker sentences aligned by {E(c['lockers']['align'])}; each patch makes O's state "
                 f"at its positions S's (h_S − h_O added), at one layer.</p>"
                 f"<p class='mut'>O's tokens as the model reads them ({I.READER_NAME[w0]}; the other reader's prompt is the "
                 f"same through the last locker token). Patched: {legend}</p>{tokens_html(m, ids, c['pos'], set(), classes)}"
                 f"<ul class='mut'>{''.join(pos_lines)}</ul>")  # fmt: skip
    parts.append(
        "<div class='ans'><b>What the model answered</b>"
        + "".join(sweep_grid(it, w) for w in sorted(I.READERS, key=lambda x: x != w0))
        + "</div>"
    )
    parts.append(numbers_html(it))
    parts.append(checks_and_form(it, seed, mark))
    return "".join(parts)


# ------------------------------------------------------------------------------------------------- the 45a card
def prepend_grid(it: dict, w: str, per_change: bool) -> str:
    """One reader's answers in 45a: a row per arm, a column per variant (the top token, coloured by the stored route or
    by follows S / stays); per_change: then each variant's shares and the code's shift vs V0 (one change for both
    readers, so shown once)."""
    more = it["more"]
    xs = list(more["variants"])
    rd = it["case"]["readers"][w]
    head = "<tr><th>change applied</th>" + "".join(f"<th>{E(x)}</th>" for x in xs) + "</tr>"
    body = []
    for label in I.view(it["view"])["filters"]["arms"]:
        cells = []
        for x in xs:
            r = it["rows"][w].get(f"{x}{I.SEP}{label}")
            if r is None:
                cells.append("<td class='mut'>–</td>")
                continue
            sub = I.variant_item(it, x)
            d, what = answer_of(sub, w, r)
            lab = stored_label(sub, w, r)
            cells.append(f"<td title='{E(what)}; P(original answer) {r.get('p_org', '–')}, P(changed answer) "
                         f"{r.get('p_alt', '–')}'>{tag(d, CLASS_COLOR.get(lab, 'oth'))} <span class='mut' "
                         f"style='font-size:11px'>{E(lab)}</span></td>")  # fmt: skip
        mark = " <span class='mut'>(the class)</span>" if label == more["class_arm"] else ""
        body.append(f"<tr><td>{E(str(ARM_NAME.get(label, label)))}{mark}</td>{''.join(cells)}</tr>")

    def per(fn) -> str:
        return "".join(f"<td class='mut'>{fn(x)}</td>" for x in xs)

    def share(x: str, k: str) -> str:
        n = more["norms"].get(x) or {}
        return f"{100 * n[k]:.0f}%" if k in n else "–"

    def beta(x: str) -> str:
        b = more["beta"].get(x)
        return f"{b['beta']:+.2f}" if b else "–"

    def size(x: str) -> str:
        n = more["norms"].get(x) or {}
        return f"{n['norm']:.1f}" if "norm" in n else "–"

    if per_change:
        body += [f"<tr><td class='mut'>share of the pointer part</td>{per(lambda x: share(x, 'share_alf'))}</tr>",
                 f"<tr><td class='mut'>share of the J++ part</td>{per(lambda x: share(x, 'share_jpp'))}</tr>",
                 f"<tr><td class='mut'>size of the change</td>{per(size)}</tr>",
                 f"<tr><td class='mut'>code shift β vs V0 (beta.jsonl)</td>{per(beta)}</tr>"]  # fmt: skip
    key = (f"original answer {E(str(rd['answer']))}, changed answer {E(str(rd['cf_answer']))}" if w == "PM" else
           ", ".join(f"{k} {v}" for k, v in it["case"]["expect"].items()))  # fmt: skip
    return (f"<p class='{'me' if w == it['reader'] else ''}' style='margin:6px 0'><b>{I.READER_NAME[w]}</b>: "
            f"{E(rd['question'])} <span class='mut'>({key})</span></p><div class='wrap'><table class='grid'>{head}"
            f"{''.join(body)}</table></div>")  # fmt: skip


def prepend_card(it: dict, seed: int, mark: dict | None) -> str:
    """45a: one base scene in every variant, side by side (O and S, the prepended sentence outlined), the pointer's
    move, and each arm's answer per variant for both readers."""
    c, m, w0, more = it["case"], it["model"], it["reader"], it["more"]
    move = more["move"]
    head = (f"{E(I.spec()['models'][m]['label'])} · layer {it['layer']} · run {E(it['run'].split('/')[-1])} · base scene "
            f"{E(it['scene'])} · {I.READER_NAME[w0]} · C2 (another item moved)")  # fmt: skip
    status = "" if it["in_set"] else " " + tag(it["status"], "st")
    parts = [f"<div class='card{'' if it['in_set'] else ' outside'}'><div class='hdr'>{head}{status}</div>"
             f"<div class='mut' style='font-size:11px'>{E(it['id'])}</div>"]  # fmt: skip
    if c is None:
        return "".join(parts) + "<p>No case for this base scene in the run's cases.jsonl.</p></div>"
    rows = [
        "<table><tr><th style='width:16%'>variant: the sentence put before the scene (outlined)</th><th>O, the "
        "original prompt (the model reads this)</th><th>S, the source prompt (the change is taken from here)</th></tr>"
    ]
    for x, vc in more["variants"].items():
        o, s = marked(vc["context"], vc["cf_context"]), marked(vc["cf_context"], vc["context"])
        if vc.get("prepended"):
            o, s = outlined(o, vc["prepended"]), outlined(s, vc["prepended"])
        rows.append(f"<tr><td><b>{E(x)}</b><br><span class='mut'>{E(I.PREPEND_WHAT.get(x, ''))}</span></td>"
                    f"<td class='prompt'>{o}</td><td class='prompt'>{s}</td></tr>")  # fmt: skip
    parts.append("".join(rows) + "</table>")
    first = I.first_locker(move)
    where = ("a move to or from the first locker: the 45a rule's items" if first else
             "not to or from the first locker: outside the rule's moves (descriptive)")  # fmt: skip
    pos = ", ".join(f"{x} {vc['pos']}" for x, vc in more["variants"].items())
    asked = re.search(r"([A-Z][a-z]+)'s pick", c["readers"]["PP"]["question"])
    parts.append(f"<p>The bridge, {E(asked.group(1) if asked else 'the asked person')}'s pick, is <b>{E(c['bridge'])}</b> "
                 f"in O and <b>{E(c['cf_bridge'])}</b> in S; the change is added at its token ({pos}). The pointer moves "
                 f"from locker slot {move[0] if move else '?'} to slot {move[1] if move else '?'} (the O bridge's → the S "
                 f"bridge's): {where}. {expected_html(I.variant_item(it, next(iter(more['variants']))))}</p>")  # fmt: skip
    parts.append("<div class='ans'><b>What the model answered</b> <span class='mut'>(a column per variant; hover a cell for "
                 "P(original) and P(changed))</span>"
                 + "".join(prepend_grid(it, w, w == w0) for w in sorted(I.READERS, key=lambda x: x != w0)) + "</div>")  # fmt: skip
    strips = []
    for x, vc in more["variants"].items():
        rd = vc["readers"][w0]
        diff = {i for i, (a, b) in enumerate(zip(rd["ids"]["org"], rd["ids"]["alt"], strict=False)) if a != b}
        strips.append(f"<p class='mut'>{E(x)}: O</p>{tokens_html(m, rd['ids']['org'], vc['pos'], diff)}")
    parts.append(f"<details><summary>O's tokens as the model saw them, per variant ({I.READER_NAME[w0]}; the change is "
                 f"added at <span class='toks'><span class='at'>pos</span></span>, tokens that differ in S marked)</summary>"
                 f"{''.join(strips)}</details>")  # fmt: skip
    parts.append(numbers_html(it))
    parts.append(checks_and_form(it, seed, mark))
    return "".join(parts)


def fixed_note(v: dict, p: dict) -> str:
    """The page's line for the fixed sample (views file fixed_sample, at its seed), or "" for a random sample."""
    fs = I.spec().get("fixed_sample") or {}
    if fs.get("seed") != p["seed"] or v["id"] not in (fs.get("views") or {}) or p["mode"] != "uniform":
        return ""
    return (f"<p class='mut'><b>The fixed sample</b> (seed {p['seed']}, {len(fs['views'][v['id']])} items across the "
            "models: 6 random by model x reader + 4 targeted, each with its reason; docs/review_views.yaml fixed_sample, "
            "never re-drawn).")  # fmt: skip


def controls(v: dict, p: dict, server: bool) -> str:
    facet_names = list(v.get("filters", {}).get("facets", {}))
    fixed = fixed_note(v, p)
    if fixed and not server:
        return fixed + " Marks are kept in this browser; use “download marks”.</p>"
    if not server:
        return (f"<p class='mut'>Static export: seed {p['seed']}, N = {p['n']} per model, {p['mode']}"
                + "".join(f", {k} {p[k]}" for k in ("reader", "condition", "s", "kind", "order", "group", *facet_names)
                          if p.get(k) not in (None, "", "all"))
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
    if v["kind"] in ("x0", "massmean", "x45d", "x45g"):
        extra += sel("order", ["all", "locker first", "locker after"])
    if v["kind"] == "x5":
        extra += sel("order", ["all", "fact first", "fact after"])
    if v.get("filters", {}).get("groups"):  # 45m: x45m's groups
        extra += sel("group", ["all", *v["filters"]["groups"]])
    for name, values in v.get("filters", {}).get("facets", {}).items():  # 45a's move, 45d's format, ...
        extra += sel(name, ["all", *values])
    sup = (f"<label><span><input type='checkbox' name='superseded' value='1' {'checked' if p.get('superseded') else ''}>"
           "superseded runs</span></label>") if v.get("superseded") else ""  # fmt: skip
    head = fixed + " The filters below do not apply to it; another seed gives a random sample.</p>" if fixed else ""
    return head + (f"<form class='ctl box' method='get' action='/view'><input type='hidden' name='view' value='{E(v['id'])}'>"
            f"<label>seed<input name='seed' type='number' value='{p['seed']}' style='width:6em'></label>"
            f"<label>N<input name='n' type='number' value='{p['n']}' style='width:5em'></label>"
            + sel("mode", ["uniform", "stratified"]) + sel("model", models) + sel("reader", ["all", *I.READERS]) + extra
            + f"<label><span><input type='checkbox' name='out' value='1' {'checked' if p.get('out') else ''}>outside the claim's set"
            f"</span></label>{sup}<button>show</button></form>")  # fmt: skip


def filters_plain(v: dict) -> str:
    """The view's filters in words."""
    f = v.get("filters", {})
    cond = {"C0": "C0 sanity swap", "C1": "C1 the same item moved", "C2": "C2 another item moved"}
    bits = []
    if f.get("rendering"):
        bits.append("prompts in the chat template" if f["rendering"] == "chat" else f"{f['rendering']} prompts")
    bits.append({"fixed": "each model's layer fixed in advance", "run": "each run's own layer"}.get(f.get("layer"), ""))
    bits.append(" and ".join(I.READER_NAME[w] for w in f.get("readers", I.READERS)))
    if f.get("conditions"):
        bits.append(", ".join(cond[c] for c in f["conditions"]))
    if f.get("arms"):
        bits.append("changes: " + ", ".join(str(ARM_NAME.get(a, a)) for a in f["arms"]))
    if f.get("kinds"):
        bits.append("writes and random directions at dose s = " + ", ".join(map(str, f.get("s", []))))
    if f.get("groups"):
        bits.append("groups (filter): " + ", ".join(f["groups"]))
    for name, values in f.get("facets", {}).items():
        bits.append(f"{name} (filter): " + ", ".join(map(str, values)))
    if f.get("class_arm"):
        bits.append(f"class: the answer under “{f['class_arm']}” in the first variant")
    items = f.get("items") or "the items the run used (both readers read the original and changed prompts right)"
    return "; ".join(b for b in bits if b) + f"; {items}."


def runs_html(v: dict) -> str:
    """The view's runs per model (and the runs joined to them), each one not landed yet tagged with its state, and a
    landed one with what voids its items (a failed C0 check, or a failed gate of the view's rendering or conditions)."""
    f = v.get("filters", {})
    keys = {f["rendering"]} if f.get("rendering") else set(f.get("conditions", [])) or None

    def one(r: str) -> str:
        s = I.run_state(r)
        if s != "landed":
            return f"{E(r)} {tag(s, 'na')}"
        return E(r) + "".join(" " + tag(flag, "fail") for flag in I.run_flags(r, keys))

    out = []
    for m, rs in v.get("runs", {}).items():
        joined = v.get("join_runs", {}).get(m, [])
        out.append(f"<li>{E(I.spec()['models'][m]['label'])}: {', '.join(one(r) for r in rs)}"
                   + (f"; joined by scene: {', '.join(one(r) for r in joined)}" if joined else "") + "</li>")  # fmt: skip
    return "".join(out)


def claim_box(v: dict) -> str:
    runs = runs_html(v)
    classes = I.spec()["kinds"][v["kind"]]["classes"]
    cls = "; ".join(f"{tag(k)} {E(str(d))}" for k, d in classes.items())
    return (
        f"<div class='box'><p><b>Claim.</b> {E(v['claim'])}</p><p class='mut'>README: {E(v.get('readme', ''))}</p>"
        f"<p class='mut'>Sources (docs/x0_numbers.json): {E(', '.join(v.get('sources', [])) or 'none yet')}</p>"
        f"<p class='mut'>Item set: {E(filters_plain(v))}</p><ul class='mut'>{runs}</ul>"
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
            "(data/figures/depth/data.csv, 2 decimals)")  # fmt: skip
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
            claim_box(v), LEGEND, recount_box(recount), checks_box(stats), "<p><button onclick='download()'>download marks</button> "
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
                pending = I.not_landed(v, m) if section == "set" else []
                why = ("no run of this model in the view" if section == "set" and m not in v.get("runs", {}) else
                       "; ".join(f"{E(r)}: {E(s)}" for r, s in pending) or "no per-item file lists them")  # fmt: skip
                body.append(f"<p class='mut'>No items ({why}).</p>")
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
        pending = {m: I.not_landed(v, m) for m in stats}
        counts = ", ".join(f"{I.spec()['models'][m]['key']} {s['n'] or (pending[m][0][1].split(' (')[0] if pending[m] else 0)}"
                           for m, s in stats.items())  # fmt: skip
        fails = sum(sum(s["fail"].values()) for s in stats.values())
        mism = sum(r["status"] == "mismatch" for r in rec)
        match = sum(r["status"] == "match" for r in rec)
        body.append(f"<tr><td><a href='{link(params, server)}'>{E(v['title'])}</a></td><td>{counts}</td>"
                    f"<td>{tag(str(fails), 'fail' if fails else 'pass')}</td><td>{match} match, "
                    f"{tag(str(mism), 'fail' if mism else 'pass')} mismatch</td></tr>")  # fmt: skip
    body.append("</table>")
    return page("Review", "".join(body), server, commit)
