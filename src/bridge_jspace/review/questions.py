"""Guided checklists for the review tool (Dan 30 Oct, review-tool brief): the questions a view asks of every item, what
the machine says about each from the item's stored fields, the view-level header block, and the answers read back from
review/marks.jsonl.

Questions live in docs/review/review_views.yaml (`common_questions` at the top, `common:` and `questions:` per view, see the
comment there). Two kinds: `check` (a "No" means the item is wrong) and `observe` (a "No" is data, not an error). A
question's `machine` is an expression over the item, evaluated with the helpers of `Env` below and nothing else; its value
is shown on the card as "the machine says: ...". A machine that cannot compute says why instead of guessing.

marks.jsonl rows of this module: {"schema": 2, "view", "item_key", "q_id", "answer": yes | no | unclear, "note", "ts"} (plus
"seed" and "commit"). The item's own mark (consistent / wrong / unclear) is the row it always was; rows without a verdict
are skipped by handcheck.load_marks, so old files load as before.
"""

from __future__ import annotations

import collections
import json
from pathlib import Path
from typing import Any

from bridge_jspace.review import checks as C
from bridge_jspace.review import items as I

ANSWERS = ("yes", "no", "unclear")
KINDS = ("check", "observe")
REQUIRED = ("id", "text", "look_at", "yes_if", "protects_against", "kind")
SCHEMA = 2
FRAGILE = 0.5  # |logit gap| below this: a deciding switch hangs by a hair (A7)
SAME_SHARE = 0.02  # two stored shares within this are "the same" (A6; review_jspace.check_share's tolerance)


# ------------------------------------------------------------------------------------------------ the question set
def questions_of(view_id: str) -> list[dict]:
    """The view's checklist in order: its `common:` questions (from `common_questions`), then its own `questions:`.
    Each is validated (every required key, kind check | observe) and returned with `yes_if` resolved for this view."""
    spec, v = I.spec(), I.view(view_id)
    common = {q["id"]: q for q in spec.get("common_questions") or []}
    out = []
    for qid in v.get("common") or []:
        if qid not in common:
            raise ValueError(f"{view_id}: common question {qid} is not defined")
        out.append(dict(common[qid]))
    out += [dict(q) for q in v.get("questions") or []]
    seen: set[str] = set()
    for q in out:
        missing = [k for k in REQUIRED if not q.get(k)]
        if missing:
            raise ValueError(f"{view_id} {q.get('id')}: missing {missing}")
        if q["kind"] not in KINDS:
            raise ValueError(f"{view_id} {q['id']}: kind {q['kind']!r} is neither check nor observe")
        if q["id"] in seen:
            raise ValueError(f"{view_id}: question {q['id']} twice")
        seen.add(q["id"])
        y = q["yes_if"]
        q["yes_if"] = (y.get(view_id) or y.get("default") or "") if isinstance(y, dict) else y
        q.setdefault("anchor", "")
        q.setdefault("tally", q["text"])
    return out


def split(view_id: str) -> tuple[list[dict], list[dict]]:
    """(the human questions, the machine-only questions) of a view: H1, H2 (check) and H3 (observe, views a and b) are put to
    the human; every other question is answered by the machine and collapsed on the card (Dan 30 Oct, 45-minute read)."""
    qs = questions_of(view_id)
    return [q for q in qs if q.get("human")], [q for q in qs if not q.get("human")]


def five_ids(view_id: str) -> list[str]:
    """The view's five items (yaml `five`, drawn from the seed-29 fixed sample by the rule at the top of the file)."""
    return list(I.view(view_id).get("five") or [])


def has_questions(view_id: str) -> bool:
    v = I.view(view_id)
    return bool(v.get("common") or v.get("questions"))


def panel_ids(qs: list[dict]) -> list[str]:
    """The sub-answers a question collects on the J-space panel (A8's three ticks) instead of on the card."""
    return [x for q in qs for x in q.get("panel") or []]


# ------------------------------------------------------------------------------------------------ the machine
def _num(x: Any) -> str:
    return f"{x:.3g}" if isinstance(x, float) else str(x)


def _says(r: dict | None) -> tuple[bool | None, str]:
    """(switched?, a phrase) of a stored row: the probabilities decide where stored, the label otherwise."""
    if r is None:
        return None, "not in the run"
    label = bool(r.get("switched"))
    if "p_alt" in r and "p_org" in r:
        pa, po = r["p_alt"], r["p_org"]
        by_p = pa > po
        note = "" if by_p == label else f" (the stored label says {'switched' if label else 'not switched'})"
        return by_p, f"P(changed) {_num(pa)} {'>' if by_p else '<='} P(original) {_num(po)}{note}"
    return label, f"no probabilities stored; the stored label says {'switched' if label else 'not switched'}"


class Env:
    """The helpers a `machine` expression may call, bound to one item. Arms are the view's labels ('whole', 'without
    J++', ...); readers 'PP' (lookup) and 'PM' (recall)."""

    def __init__(self, it: dict):
        self.it = it
        self.view = I.view(it["view"])
        self.whole = (self.view.get("header") or {}).get("whole", "whole")

    # -- stored rows
    def row(self, w: str, arm: str) -> dict | None:
        return (self.it["rows"].get(w) or {}).get(arm)

    def says(self, w: str, arm: str) -> str:
        sw, phrase = _says(self.row(w, arm))
        return phrase if sw is None else f"{'yes' if sw else 'no'}: {phrase}"

    def switched(self, w: str, arm: str) -> bool | None:
        return _says(self.row(w, arm))[0]

    def _base(self, w: str, base: str | None) -> tuple[bool, str]:
        base = base or self.whole
        sw = self.switched(w, base)
        return bool(sw), f"n/a: under '{base}' the {I.READER_NAME[w]} did not switch, so there is nothing to block"

    def blocked(self, w: str, arm: str, base: str | None = None) -> str:
        ok, why = self._base(w, base)
        if not ok:
            return why
        sw, phrase = _says(self.row(w, arm))
        if sw is None:
            return phrase
        return f"{'no: it still switched' if sw else 'yes: blocked'} ({phrase})"

    def still(self, w: str, arm: str, base: str | None = None) -> str:
        ok, why = self._base(w, base)
        return self.says(w, arm) if ok else why

    # -- the item
    def locker_order(self) -> str:
        o = self.it.get("order") or {}
        return f"original prompt {o.get('original', '?')} it, changed prompt {o.get('changed', '?')} it" if o else "not stored"

    def check(self, name: str) -> str:
        status, detail = C.run_checks(self.it)[name]
        return f"{status}: {detail}"

    def pre_change(self) -> str:
        parts, ok = [], True
        for w in I.READERS:
            rows = self.it["rows"].get(w) or {}
            first = next((lb for lb in rows if lb in ("unedited", "unwritten")), None)
            r = rows.get(first) if first else None
            if r is None or "p_org" not in r:
                parts.append(f"{I.READER_NAME[w]}: not stored")
                continue
            ok &= r["p_org"] >= 0.5
            parts.append(f"{I.READER_NAME[w]} P(original) {_num(r['p_org'])}")
        return f"{'yes' if ok else 'no'}: " + ", ".join(parts)

    def label_agrees(self) -> str:
        bad, n = [], 0
        for w in I.READERS:
            for label, r in (self.it["rows"].get(w) or {}).items():
                if r is None or "role" not in r:
                    continue
                n += 1
                if not _agree(r):
                    bad.append(f"{I.READER_NAME[w]} {label}: role {r['role']}, P(original) {_num(r['p_org'])}, "
                               f"P(changed) {_num(r['p_alt'])}")  # fmt: skip
        if not n:
            return "n/a: no probabilities stored"
        return f"yes: {n} rows agree" if not bad else "no: " + "; ".join(bad[:3])

    def shares_same(self) -> str:
        s = self.it.get("shares") or {}
        a, b = s.get("jpp"), s.get("random part")
        if a is None or b is None:
            return "not stored"
        return f"{'yes' if abs(a - b) <= SAME_SHARE else 'no'}: J++ part {a:.3f}, its random part {b:.3f}"

    def fragile(self, thr: float = FRAGILE) -> str:
        labels = self.view.get("decisive") or []
        hits, smallest = [], None
        for w in I.READERS:
            for label in labels:
                r = self.row(w, label)
                if r is None or r.get("ld") is None:
                    continue
                g = abs(r["ld"])
                if smallest is None or g < smallest[0]:
                    smallest = (g, w, label)
                if g < thr:
                    hits.append(f"{I.READER_NAME[w]}, {label} (logit gap {r['ld']:+.2f})")
        if hits:
            return "yes: " + "; ".join(hits)
        return "no" + (f" (smallest |gap| {smallest[0]:.2f}: {I.READER_NAME[smallest[1]]}, {smallest[2]})" if smallest else "")

    # -- the one-line story (H2)
    def _pairs(self) -> list[list[str]]:
        v = self.view
        if v.get("story"):
            return v["story"]
        h = v.get("header") or {}
        return [[h["part"], h["random"], "J++"]] if h.get("part") else []

    def _outcome(self, w: str, row: dict | None) -> str:
        if row is None:
            return "not in the run"
        if w == "PP" and "route" in row:
            return f"route {row['route']}"
        if w == "PP" and "class" in row:
            return f"digit {row['class']}"
        if "changed" in row and "role" not in row:
            return "changed" if row["changed"] else "unchanged"
        return "switched" if row.get("switched") else "kept"

    def story(self) -> str:
        """The item's story in one sentence per reader, from the stored rows: switched / blocked / kept under each arm."""
        pairs, parts = self._pairs(), []
        for w in ("PM", "PP"):
            name, rows = I.READER_NAME[w], self.it["rows"].get(w) or {}
            if pairs:
                rd = self.it["case"]["readers"][w]
                a, b = rd["answer"], rd["cf_answer"]
                head = f"{name} (original answer {a}, changed answer {b}):"
                sw = self.switched(w, self.whole)
                if sw is None:
                    parts.append(f"{head} no row under '{self.whole}'")
                elif not sw:
                    after = (self.it.get("order") or {}).get("original") == "after"
                    parts.append(f"{head} the whole change did not switch it, it stayed {a}"
                                 + (" (the locker sentence comes after the pick, so there is nothing for the lookup to follow)" if w == "PP" and after else ""))  # fmt: skip
                else:
                    bits = [f"the whole change switched it to {b}"]
                    for arm, rnd, phrase in pairs:
                        bits.append(f"without {phrase} it still switched to {b} (not blocked)" if self.switched(w, arm)
                                    else f"without {phrase} it stayed {a} (blocked)")  # fmt: skip
                        bits.append(f"without its random part it still switched to {b} (not blocked)" if self.switched(w, rnd)
                                    else f"without its random part it stayed {a} (blocked)")  # fmt: skip
                    parts.append(f"{head} " + "; ".join(bits))
            else:
                labels = [lb for lb in (self.view.get("decisive") or list(rows)) if lb in rows and lb not in ("unedited", "unwritten")]
                parts.append(f"{name}: " + "; ".join(f"{lb}: {self._outcome(w, rows.get(lb))}" for lb in labels))
        return " | ".join(parts)

    def names(self) -> dict[str, Any]:
        return {n: getattr(self, n) for n in ("says", "blocked", "still", "locker_order", "check", "pre_change", "label_agrees",
                                              "shares_same", "fragile", "switched", "row", "story")
                } | self.extra() | {"abs": abs, "min": min, "max": max, "len": len, "all": all, "any": any, "round": round}

    def extra(self) -> dict[str, Any]:
        """Helpers of the other views (routes, x8, last token, answer control): see review/questions_views.py."""
        from bridge_jspace.review import questions_views as QV

        return QV.helpers(self)


def _agree(r: dict) -> bool:
    """check_probs' per-row test: the role follows the probabilities and the label."""
    eps = C.EPS
    role, po, pa, ld = r["role"], r["p_org"], r["p_alt"], r["ld"]
    ok = bool(r["switched"]) == (role == "b")
    ok &= not (role == "b" and (pa < po - eps or ld < -eps)) and not (role == "A" and (po < pa - eps or ld > eps))
    ok &= not (pa > 0.5 and role != "b") and not (po > 0.5 and role != "A")
    return bool(ok)


def show(value: Any) -> str:
    if value is None:
        return "not stored"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:.3f}"
    if isinstance(value, (list, tuple)):
        return ", ".join(show(x) for x in value)
    if isinstance(value, dict):
        return ", ".join(f"{k}: {show(x)}" for k, x in value.items())
    return str(value)


def machine(it: dict, q: dict) -> dict[str, str | None]:
    """{"text": the machine's answer or None, "error": why it could not compute or None} for one question on one item."""
    expr = q.get("machine")
    if not expr:
        return {"text": None, "error": None}
    try:
        value = eval(compile(expr, f"<machine {q['id']}>", "eval"), {"__builtins__": {}}, Env(it).names())
    except Exception as e:  # a machine that cannot compute says why: never a silent blank
        return {"text": None, "error": f"{type(e).__name__}: {e}"}
    return {"text": show(value), "error": None}


# ------------------------------------------------------------------------------------------------ the item's mark
def machine_status(it: dict) -> dict:
    """What the machine settles on one item: every machine-only question's answer and state (pass / fail / na / info), and
    which of them need the human: a failed check, or an observe question that is n/a where it matters (matters_if_na)."""
    _, mach = split(it["view"])
    rows = []
    for q in mach:
        if not q.get("machine"):
            continue
        m = machine(it, q)
        text, err = m["text"] or "", m["error"]
        if err:
            state = "fail"
        elif text.startswith(("n/a", "not stored")):
            state = "na"
        elif q["kind"] == "check":
            state = "pass" if text.startswith(("pass", "yes")) and "fail:" not in text else "fail"
        else:
            state = "info"
        need = state == "fail" or (state == "na" and bool(q.get("matters_if_na")))
        rows.append({"q": q, "text": text or (err or ""), "state": state, "need": need})
    return {"rows": rows, "need": [r for r in rows if r["need"]], "all_pass": not any(r["need"] for r in rows)}


def h3(it: dict) -> dict:
    """H3's pre-fill: the three ticks from the atom classes and the answer word's state rank (the J-space panel's machine);
    {"error": why} where the states or the readout are not there."""
    try:
        I.scripts_on_path()
        from scripts import review_jspace as J

        st = J.states(it["model"], it["view"], it["id"])
        return {"error": "no states for this item (cache/review_states)"} if st is None else J.a8_machine(st, it, it["model"])
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def five_items(view_id: str) -> list[dict]:
    """The view's five items as loaded items, in the yaml's order."""
    out = []
    for item_id in five_ids(view_id):
        model = model_of(item_id)
        got = next((it for it in I.items(view_id, model) if it["id"] == item_id), None)
        if got is not None:
            out.append(got)
    return out


def deck_line(view_id: str, marks: list[dict], rows: list[dict]) -> str:
    """One line per view, ready for the deck: the five items' marks, the machine's observe tallies over them, the H3 tallies
    ("5 items: 3 consistent, 1 wrong, 1 unclear · machine: recall switch blocked without J++ 3/4 · H3: old bridge (-) 3/4")."""
    five = five_ids(view_id)
    last = {r["item"]: r for r in marks if r.get("view") == view_id and r.get("item") in five}
    c = collections.Counter(r["verdict"] for r in last.values())
    extra = len({r["item"] for r in marks if r.get("view") == view_id and r.get("item") not in five})
    head = (f"{view_id}: {len(five)} items: {c['consistent']} consistent, {c['wrong']} wrong, {c['unclear']} unclear"
            + (f" ({len(five) - len(last)} not read yet)" if len(last) < len(five) else "") + (f"; {extra} extra" if extra else ""))
    _, mach = split(view_id)
    items = five_items(view_id)
    bits = []
    for q in mach:
        if q["kind"] != "observe" or not q.get("machine"):
            continue
        res = [machine(it, q)["text"] or "" for it in items]
        yes, no = sum(x.startswith("yes") for x in res), sum(x.startswith("no") for x in res)
        na = len(res) - yes - no
        bits.append(f"{q.get('tally', q['text'])} {yes}/{yes + no}" + (f" ({na} n/a)" if na else ""))
    h3rows = [r for r in rows if r["item_key"] in set(five) and r["q_id"] in ("H3a", "H3b", "H3c")]
    lastq = latest(h3rows)
    names = {"H3a": "old bridge (-)", "H3b": "new bridge (+)", "H3c": "answer word"}
    h3bits = []
    for qid, nm in names.items():
        got = [qa[qid]["answer"] for qa in lastq.values() if qid in qa]
        if got:
            h3bits.append(f"{nm} {got.count('yes')}/{len(got)}")
    return head + (" · machine: " + "; ".join(bits) if bits else "") + (" · H3: " + ", ".join(h3bits) if h3bits else "")


def overall(answers: dict[str, str], qs: list[dict]) -> str | None:
    """The item's derived mark: wrong if any human check (H1, H2) is No, unclear if any is Unclear, consistent once both are
    Yes; None until they are answered. Observe questions and the machine's checks never change it."""
    checks = [q["id"] for q in qs if q["kind"] == "check" and q.get("human")] or [q["id"] for q in qs if q["kind"] == "check"]
    got = [answers.get(c) for c in checks]
    if "no" in got:
        return "wrong"
    if "unclear" in got:
        return "unclear"
    return "consistent" if checks and all(g == "yes" for g in got) else None


# ------------------------------------------------------------------------------------------------ marks
def load_rows(path: Path) -> list[dict]:
    """The schema-2 question rows of a marks file, in file order."""
    if not path.exists():
        return []
    rows = [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
    return [r for r in rows if r.get("schema") == SCHEMA and r.get("answer") in ANSWERS and r.get("q_id") and r.get("item_key")]


def latest(rows: list[dict]) -> dict[str, dict[str, dict]]:
    """item_key -> q_id -> the last row."""
    out: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for r in rows:
        out[r["item_key"]][r["q_id"]] = r
    return out


def model_of(item_key: str) -> str:
    return item_key.split("|", 1)[0]


def tallies(rows: list[dict]) -> dict[str, dict[str, dict[str, collections.Counter]]]:
    """view -> model -> q_id -> Counter(yes / no / unclear), the last answer per item and question."""
    out: dict = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(collections.Counter)))
    for item, qa in latest(rows).items():
        for qid, r in qa.items():
            out[r["view"]][model_of(item)][qid][r["answer"]] += 1
    return out


def tally_lines(rows: list[dict], view_id: str) -> list[str]:
    """Per model: a check question's yes / no / unclear counts, an observe question as a tally ("recall switch blocked
    without J++: 7/10"), for the summary and VERIFIED.md."""
    t = tallies(rows).get(view_id) or {}
    if not t or not has_questions(view_id):
        return []
    qs = {q["id"]: q for q in questions_of(view_id)}
    sub = {s: q for q in qs.values() for s in q.get("panel") or []}
    out = []
    for m, per in sorted(t.items()):
        label = I.spec()["models"].get(m, {}).get("label", m)
        for qid in [*qs, *sub]:
            c = per.get(qid)
            if not c:
                continue
            q = qs.get(qid) or sub[qid]
            n = sum(c.values())
            if q["kind"] == "check":
                out.append(f"- {label}: {qid} {q['text']} yes {c['yes']}, no {c['no']}, unclear {c['unclear']}")
            else:
                phrase = q.get("tally", q["text"]) + (f" ({qid})" if qid in sub else "")
                out.append(f"- {label}: {phrase}: {c['yes']}/{n}" + (f" ({c['unclear']} unclear)" if c["unclear"] else ""))
    return out


# ------------------------------------------------------------------------------------------------ the view header
def _count(items: list[dict], w: str, arm: str) -> tuple[int, int]:
    """(items whose row for reader w under `arm` exists, those that switched), over the items sampled as reader w."""
    n = sw = 0
    for it in items:
        if it["reader"] != w:
            continue
        s = _says((it["rows"].get(w) or {}).get(arm))[0]
        if s is None:
            continue
        n += 1
        sw += bool(s)
    return n, sw


def header(view_id: str, stats: dict[str, dict], recount: list[dict]) -> dict[str, list[dict]]:
    """Per model, the view-level checks over every item of the view: H1 the denominators (switched items per reader under
    the whole change), H2 control sanity (the random part blocks something, and less than the lens part), H3 the headline
    recount against data.csv, H4 label and probabilities agree on every item. Each: id, status (pass / fail / na), the
    numbers, and a sentence on what it means."""
    h = I.view(view_id).get("header")
    if not h:
        return {}
    whole, part, rnd = h["whole"], h["part"], h["random"]
    bar = int(h.get("min_switched", 30))
    out: dict[str, list[dict]] = {}
    for m in stats:
        its = I.items(view_id, m)
        rows: list[dict] = []
        if not its:
            out[m] = [{"id": "-", "status": "na", "value": "no items", "means": "no per-item file for this model in the view"}]
            continue
        sw = {w: _count(its, w, whole) for w in I.READERS}
        short = [I.READER_NAME[w] for w in I.READERS if sw[w][1] < bar]
        rows.append({"id": "H1", "status": "fail" if short else "pass",
                     "value": ", ".join(f"{I.READER_NAME[w]} {sw[w][1]} of {sw[w][0]}" for w in I.READERS),
                     "means": f"items the whole change switched, per reader: the denominator of every share below; the bar is {bar}"
                              + (f" ({' and '.join(short)} below it: its numbers are not readable)" if short else "")})  # fmt: skip
        parts = []
        status = "pass"
        for w in I.READERS:
            _n0, s0 = sw[w]
            _, sp = _count(its, w, part)
            _, sr = _count(its, w, rnd)
            if not s0:
                parts.append(f"{I.READER_NAME[w]}: nothing switched")
                continue
            jdep, rdep = 1 - sp / s0, 1 - sr / s0
            parts.append(f"{I.READER_NAME[w]} lens part {jdep:.2f}, random part {rdep:.2f}")
            if w == "PM" and not (0 < rdep < jdep):
                status = "fail"
        rows.append({"id": "H2", "status": status, "value": "; ".join(parts) + " (share of the whole change's switches blocked)",
                     "means": "a control that blocks nothing (or everything) is broken: the recall's random part should block "
                              "something, and less than the lens part"})  # fmt: skip
        rec = [r for r in recount if r["model"] == m]
        mism = [r for r in rec if r["status"] == "mismatch"]
        match = sum(r["status"] == "match" for r in rec)
        rows.append({"id": "H3", "status": "fail" if mism else ("pass" if match else "na"),
                     "value": f"{match} match, {len(mism)} mismatch",
                     "means": "the headline numbers recounted from the per-item files against data/figures/depth/data.csv"})
        fails = {k: v for k, v in (stats[m].get("fail") or {}).items() if k in ("label from the top token", "probabilities agree with the label")}
        rows.append({"id": "H4", "status": "fail" if fails else "pass",
                     "value": f"{sum(fails.values())} items disagree" if fails else f"all {stats[m]['n']} items agree",
                     "means": "each arm's stored label agrees with its top token and its probabilities (automatic, every item)"})
        out[m] = rows
    return out
