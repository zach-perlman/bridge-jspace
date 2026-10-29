"""Automatic checks on an item, recomputed from its per-item files and the pinned tokenizer, independently of the run
code. A disagreement is a finding: it is listed (view page, STATUS), never fixed, and the check is not changed to pass.

  bridge at the change's token: the token at pos decodes to the bridge (org) and to the cf bridge (alt)
  only the scene's words differ: org and alt ids have the same length and differ only at tokens of words the scene changes;
                      pos differs iff the bridge does
  answers decode right: tok_A / tok_b decode to the original / swapped answer
  label from the top token: the class re-derived from the decoded top token and the expected digits equals the stored label
                      (routes C0: the stored route is "other" for a switch, a known quirk: original <-> original,
                      switch or other <-> other; the switched flag is checked on its own); x0 runs before batch 45
                      store no top token: n/a; x0 runs since (45m), x0_parts, the 45b sweep and 45d: the role the stored
                      top token gives against tok_A / tok_b equals the stored role, and switched = role b; 45g stores none:
                      n/a
  probabilities agree with the label: switched = (role b); role b: p_alt >= p_org, ld >= 0; role A: the reverse; p > 0.5 decides the role
  second run has the same prompts: routes: a second run whose rows are used has the same prompts; x8: the stored entity is the joined
                      case's bridge and j its locker slot; 45g: the stored entity is the single run's case's bridge, and the
                      stored org_order / alt_order (the rule's groups) are the case's sentence order, re-derived here
45a (one base scene in five variants): every check runs on each variant's case and rows; a failure in any variant fails
the item (named by variant).
"""

from __future__ import annotations

import collections
import difflib
import re
from functools import lru_cache
from typing import Any

from bridge_jspace import pins

PASS, FAIL, NA = "pass", "fail", "n/a"
CHECKS = (
    "bridge at the change's token",
    "only the scene's words differ",
    "answers decode right",
    "label from the top token",
    "probabilities agree with the label",
    "second run has the same prompts",
)
WORD = re.compile(r"[A-Za-z0-9]+")
LOCKER = re.compile(r"The locker of the (\w+) is (\d)\.")
EPS = 1e-6


@lru_cache(maxsize=8)
def tokenizer(model: str):
    """tokenizer.json at the revision pinned in pins.TARGETS (one small file; the three Qwens share it)."""
    from huggingface_hub import hf_hub_download
    from tokenizers import Tokenizer

    t = pins.TARGETS[model]
    return Tokenizer.from_file(hf_hub_download(t["repo"], "tokenizer.json", revision=t["revision"]))


@lru_cache(maxsize=200_000)
def piece(model: str, token: int) -> str:
    return tokenizer(model).decode([int(token)], skip_special_tokens=False)


def top_text(model: str, top: int | str) -> str:
    """A stored top: a token id (routes, x8), or already the answer word (natural passages)."""
    return top if isinstance(top, str) else piece(model, top)


def _strip(s: str) -> str:
    return s.strip().strip(".,'\"")


def changed_words(a: str, b: str) -> tuple[set[str], set[str]]:
    """The words the scene changes: position by position when both texts have as many words (sentences swapped or a
    pick replaced keep the count), else by a sequence diff."""
    wa, wb = WORD.findall(a), WORD.findall(b)
    if len(wa) == len(wb):
        pairs = [(x, y) for x, y in zip(wa, wb, strict=True) if x != y]
        return {x for x, _ in pairs}, {y for _, y in pairs}
    ca, cb = set(), set()
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=wa, b=wb, autojunk=False).get_opcodes():
        if tag != "equal":
            ca |= set(wa[i1:i2])
            cb |= set(wb[j1:j2])
    return ca, cb


def diff_positions(item: dict) -> list[int]:
    rd = item["case"]["readers"][item["reader"]]
    return [i for i, (x, y) in enumerate(zip(rd["ids"]["org"], rd["ids"]["alt"], strict=False)) if x != y]


def check_pos(it: dict) -> tuple[str, str]:
    """The token at pos is the bridge in O and the cf bridge in S. Zach's passages: about a third of his bridge names
    are several tokens; the stored span's tokens decode to the bridge and pos is the span's last token (where x50_zach
    adds the change). 51.10 (jread): the edit is at the last token (jpos P3), so P3 must be the prompt's last index,
    and P1 the bridge word (pos)."""
    c, m = it["case"], it["model"]
    rd = c["readers"][it["reader"]]
    p = c["pos"]
    o, a = _strip(piece(m, rd["ids"]["org"][p])), _strip(piece(m, rd["ids"]["alt"][p]))
    if it["kind"] == "zach" and c.get("span"):
        s0, s1 = c["span"]
        tk = tokenizer(m)
        o = _strip(tk.decode(rd["ids"]["org"][s0 : s1 + 1], skip_special_tokens=False))
        a = _strip(tk.decode(rd["ids"]["alt"][s0 : s1 + 1], skip_special_tokens=False))
        ok = p == s1 and o == c["bridge"] and a == c["cf_bridge"]
        return (PASS if ok else FAIL), (f"org[{s0}:{s1 + 1}] {o!r} / bridge {c['bridge']!r}; alt {a!r} / cf "
                                        f"{c['cf_bridge']!r}; pos {p} = the span's last token")  # fmt: skip
    else:
        ok = o == c["bridge"] and a == c["cf_bridge"]
    detail = f"org[{p}] {o!r} / bridge {c['bridge']!r}; alt[{p}] {a!r} / cf {c['cf_bridge']!r}"
    if it["kind"] == "jread":  # the read appends the space token (case "space"): the last token is that suffix
        jp = c.get("jpos", {}).get(it["reader"], {})
        last = {v: len(rd["ids"][v]) + len(read_suffix(it)) - 1 for v in ("org", "alt")}
        p3 = jp.get("P3", {})
        ok &= jp.get("P1", {}).get("org") == p and all(p3.get(v) == last[v] for v in ("org", "alt"))
        detail += f"; the edit at the last token (the appended space): P3 {p3} / last index {last}"
    return (PASS if ok else FAIL), detail


def read_suffix(it: dict) -> list[int]:
    """The tokens the run appended to the stored ids at the read (x0_necessity.read_logits, chat: a digit's space
    token): the case's own "space" / the reader's "suffix" where stored, else the tokenizer's " "; Zach's passages are
    read at the end of the template with nothing appended (x50_zach: space [])."""
    if it["kind"] == "zach":
        return []
    c = it["case"] or {}
    got = c.get("space") or c.get("readers", {}).get(it["reader"], {}).get("suffix")
    if got is None:
        for jc in (c.get("_joined") or {}).values():  # 51.12: its own case stores the suffix per reader
            got = got or (jc or {}).get("readers", {}).get(it["reader"], {}).get("suffix")
    return list(got) if got else tokenizer(it["model"]).encode(" ", add_special_tokens=False).ids


def check_diff(it: dict) -> tuple[str, str]:
    c, m = it["case"], it["model"]
    rd = c["readers"][it["reader"]]
    org, alt = rd["ids"]["org"], rd["ids"]["alt"]
    if len(org) != len(alt):
        return FAIL, f"lengths {len(org)} / {len(alt)}"
    diff = diff_positions(it)
    ca, cb = changed_words(c["context"], c["cf_context"])

    def inside(token: int, words: set[str]) -> bool:
        s = _strip(piece(m, token))
        return bool(s) and any(s in w for w in words)

    bad = [i for i in diff if not (inside(org[i], ca) and inside(alt[i], cb))]
    pos_ok = (c["pos"] in diff) == (c["bridge"] != c["cf_bridge"])
    ok = bool(diff) and not bad and pos_ok
    detail = f"{len(diff)} tokens differ" + (f"; outside the changed words: {bad[:5]}" if bad else "")
    return (PASS if ok else FAIL), detail + (
        "" if pos_ok else "; pos differs where the bridge does not, or the reverse"
    )


def check_answers(it: dict) -> tuple[str, str]:
    rd, m = it["case"]["readers"][it["reader"]], it["model"]
    if "tok_A" not in rd:  # natural passages: answers are words, read among the relation's answer words
        return NA, "answer words (no answer token stored)"
    a, b = _strip(piece(m, rd["tok_A"])), _strip(piece(m, rd["tok_b"]))
    if it["kind"] == "zach":  # answer words, read by their first token
        ok = bool(a) and bool(b) and str(rd["answer"]).startswith(a) and str(rd["cf_answer"]).startswith(b) and a != b
        return (
            PASS if ok else FAIL
        ), f"first tokens: tok_A {a!r} / {rd['answer']!r}; tok_b {b!r} / {rd['cf_answer']!r}"
    ok = a == str(rd["answer"]) and b == str(rd["cf_answer"])
    return (PASS if ok else FAIL), f"tok_A {a!r} / {rd['answer']!r}; tok_b {b!r} / {rd['cf_answer']!r}"


def route_of(digit: str, expect: dict, condition: str) -> str:
    if condition == "C0":
        return (
            "switch" if digit == str(expect["switch"]) else "original" if digit == str(expect["original"]) else "other"
        )
    return next((r for r in ("identity", "position", "value", "original") if digit == str(expect.get(r))), "other")


def check_class(it: dict) -> tuple[str, str]:
    m, c, w = it["model"], it["case"], it["reader"]
    rows = {label: r for label, r in it["rows"][w].items() if r is not None}
    if it["kind"] == "x5":  # the top is stored as the answer word: switched = it is the changed answer
        rd = c["readers"][w]
        bad = [f"{label}: top {r['top']!r}, switched {r['switched']}" for label, r in rows.items()
               if bool(r["switched"]) != (r["top"] == rd["cf_answer"])]  # fmt: skip
        return (FAIL if bad else PASS), "; ".join(bad[:4]) or f"{len(rows)} rows agree"
    if it["kind"] in ("x0", "massmean", "x0_parts", "x45b_sweep", "x45d", "x45g", "x51_answer", "zach", "jread"):
        # runs since batch 45 store the top token (x0_necessity.read_row): the role it gives against the case's answer
        # tokens (b = tok_b, A = tok_A, else other) must be the stored role, and switched must be role b
        rd = c["readers"][w]
        topped = {label: r for label, r in rows.items() if isinstance(r.get("top"), int)}
        if not topped:
            return NA, "no top token stored (role is the stored class)"
        wrong = []
        for label, r in topped.items():
            derived = "b" if r["top"] == rd["tok_b"] else "A" if r["top"] == rd["tok_A"] else "other"
            if derived != r["role"] or bool(r["switched"]) != (derived == "b"):
                wrong.append(f"{label}: top {_strip(piece(m, r['top']))!r} -> {derived}, stored {r['role']} "
                             f"(switched {r['switched']})")  # fmt: skip
        return (FAIL if wrong else PASS), "; ".join(wrong[:4]) or f"{len(topped)} rows agree"
    if it["kind"] == "identity_address":  # 53.6: the role whose answer token the top token is (digit / legs per reader)
        tok = "tok_digit" if w == "PP" else "tok_legs"
        roles = c.get("roles") or {}
        bad = []
        for label, r in rows.items():
            derived = next((k for k, x in roles.items() if x.get(tok) == r["top"]), "other")
            if derived != r["class"]:
                bad.append(f"{label}: top {_strip(piece(m, r['top']))!r} -> {derived}, stored {r['class']}")
        return (FAIL if bad else PASS), "; ".join(bad[:4]) or f"{len(rows)} rows agree"
    bad = []
    if it["kind"] == "routes":
        rd = c["readers"][w]
        for label, r in rows.items():
            d = _strip(piece(m, r["top"]))
            if (d == str(rd["cf_answer"])) != bool(r["switched"]):
                bad.append(f"{label}: top {d!r}, switched {r['switched']}")
            if w == "PP":
                derived = route_of(d, c["expect"], it["condition"])
                stored = r["route"]
                same = (derived == stored) if it["condition"] != "C0" else (
                    stored == "original" if derived == "original" else stored == "other")  # fmt: skip
                if not same:
                    bad.append(f"{label}: top {d!r} -> {derived}, stored {stored}")
    else:  # x8
        digits = [d for _, d in LOCKER.findall(c["context"])]
        x8 = it["x8"]
        for label, r in rows.items():
            d = _strip(piece(m, r["top"]))
            if w == "PP":
                if label == "unwritten":
                    derived = f"slot{digits.index(d)}" if d in digits else "other"
                else:
                    j, k = x8["j"], x8["k"]
                    third = ({0, 1, 2} - {j, k}).pop()
                    derived = next(
                        (n for n, s in (("target", k), ("original", j), ("third", third)) if d == digits[s]), "other"
                    )
                if derived != r["class"]:
                    bad.append(f"{label}: top {d!r} -> {derived}, stored {r['class']}")
            elif "changed" in r and bool(r["changed"]) != (d != str(c["readers"][w]["answer"])):
                bad.append(f"{label}: changed {r['changed']}, top {d!r} vs O's answer {c['readers'][w]['answer']!r}")
    return (FAIL if bad else PASS), "; ".join(bad[:4]) or f"{len(rows)} rows agree"


def check_probs(it: dict) -> tuple[str, str]:
    rows = {label: r for label, r in it["rows"][it["reader"]].items() if r is not None and "role" in r}
    if not rows:
        return NA, "no p / ld stored"
    rd = it["case"]["readers"][it["reader"]]
    if rd["tok_A"] == rd["tok_b"]:  # routes C1's recall: the same item, one answer; role b by the run's order of tests
        return NA, "the original and the swapped answer are one token (p_org = p_alt); nothing to switch to"
    bad = []
    for label, r in rows.items():
        role, po, pa, ld = r["role"], r["p_org"], r["p_alt"], r["ld"]
        ok = bool(r["switched"]) == (role == "b")
        ok &= not (role == "b" and (pa < po - EPS or ld < -EPS)) and not (role == "A" and (po < pa - EPS or ld > EPS))
        ok &= not (pa > 0.5 and role != "b") and not (po > 0.5 and role != "A")
        if not ok:
            bad.append(f"{label}: role {role}, switched {r['switched']}, p_org {po}, p_alt {pa}, ld {ld}")
    return (FAIL if bad else PASS), "; ".join(bad[:4]) or f"{len(rows)} rows agree"


def check_joined(it: dict) -> tuple[str, str]:
    c = it["case"]
    if it["kind"] == "x8":
        slots = [x for x, _ in LOCKER.findall(c["context"])]
        entity = next(r for r in it["rows"][it["reader"]].values() if r)["entity"]
        ok = entity == c["bridge"] and slots.index(c["bridge"]) == it["x8"]["j"]
        return (
            (PASS if ok else FAIL),
            f"entity {entity!r} / case bridge {c['bridge']!r}; j {it['x8']['j']} / slot {slots.index(c['bridge']) if c['bridge'] in slots else '?'}",
        )
    if it["kind"] == "x45g":
        from bridge_jspace.review import items as I

        more, got = it["more"], I.sentence_order(c)
        derived = {"org_order": got.get("original"), "alt_order": got.get("changed")}
        bad = [f"{k} {more['stored_order'][k]!r} / case {derived[k]!r}" for k in derived
               if more["stored_order"][k] != derived[k]]  # fmt: skip
        if more["entity"] != c["bridge"]:
            bad.insert(0, f"entity {more['entity']!r} / case bridge {c['bridge']!r}")
        return (FAIL if bad else PASS), "; ".join(bad) or (
            f"entity {c['bridge']!r}; org_order {derived['org_order']}, alt_order {derived['alt_order']} as the case"
        )
    if it["kind"] == "x51_answer":  # 51.12's own reader ids and bridge position against the source X0 case's
        w = it["reader"]
        bad = []
        for run, own in (c.get("_joined") or {}).items():
            if own is None:
                bad.append(f"{run}: no case for this scene")
                continue
            o, s = own["readers"][w], c["readers"][w]
            if (
                o["ids"] != s["ids"]
                or o.get("pos", c["pos"]) != c["pos"]
                or (o["tok_A"], o["tok_b"]) != (s["tok_A"], s["tok_b"])
            ):
                bad.append(f"{run}: ids / pos / answer tokens differ from the source case")
            if own.get("entity") != c["bridge"] or own.get("cf_entity") != c["cf_bridge"]:
                bad.append(
                    f"{run}: entity {own.get('entity')!r} / {own.get('cf_entity')!r} vs {c['bridge']!r} / {c['cf_bridge']!r}"
                )
        return (FAIL if bad else PASS), "; ".join(
            bad
        ) or f"same ids, pos and answer tokens in {list(c.get('_joined') or {})}"
    used = {r["_run"] for r in it["rows"][it["reader"]].values() if r and "_run" in r}
    joined = {run: jc for run, jc in (c.get("_joined") or {}).items() if run in used}
    if not joined:
        return NA, "every row from one run"
    bad = [run for run, jc in joined.items()
           if jc is None or any(jc[k] != c[k] for k in ("context", "cf_context", "pos"))
           or jc["readers"][it["reader"]]["ids"] != c["readers"][it["reader"]]["ids"]]  # fmt: skip
    return (FAIL if bad else PASS), (f"prompts differ in {bad}" if bad else f"same prompts in {list(joined)}")


def per_variant(it: dict) -> dict[str, tuple[str, str]]:
    """45a: each check on every variant (its case and rows as a routes item); fail if any variant fails, n/a if every
    variant is n/a, else pass."""
    from bridge_jspace.review import items as I

    got = [(x, run_checks(I.variant_item(it, x))) for x in it["more"]["variants"]]
    out = {}
    for name in CHECKS:
        fails = [f"{x}: {r[name][1]}" for x, r in got if r[name][0] == FAIL]
        if fails:
            out[name] = (FAIL, "; ".join(fails))
        elif all(r[name][0] == NA for _, r in got):
            out[name] = (NA, got[0][1][name][1])
        else:
            out[name] = (PASS, f"every variant ({', '.join(x for x, _ in got)}); {got[0][0]}: {got[0][1][name][1]}")
    return out


def run_checks(it: dict) -> dict[str, tuple[str, str]]:
    if it["kind"] == "x45a_prepend" and it["case"] is not None:
        return per_variant(it)
    if it["case"] is None:
        return {
            name: (FAIL if name == "second run has the same prompts" else NA, "no case for this scene")
            for name in CHECKS
        }
    out = {"bridge at the change's token": check_pos(it), "only the scene's words differ": check_diff(it), "answers decode right": check_answers(it),
           "label from the top token": check_class(it), "probabilities agree with the label": check_probs(it), "second run has the same prompts": check_joined(it)}  # fmt: skip
    return out


def summary(items: list[dict]) -> dict[str, Any]:
    """Failure counts per check over a whole item set, with the failing item ids."""
    fails: dict[str, list[str]] = collections.defaultdict(list)
    na: collections.Counter = collections.Counter()
    for it in items:
        for name, (status, detail) in run_checks(it).items():
            if status == FAIL:
                fails[name].append(f"{it['id']}: {detail}")
            elif status == NA:
                na[name] += 1
    return {"n": len(items), "fail": {k: len(v) for k, v in fails.items()}, "na": dict(na), "examples": dict(fails)}
