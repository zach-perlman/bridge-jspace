"""docs/review/verify_pack.md for Dan's hand check (Dan 29 Oct 11:45, jobs/c3/batch53.yaml verify_prep_1145 item 4): first page
"How to review in 2 hours", then the automatic checks over every item (review/verify_checks.json) and the independent
recount (review/verify_independent.json), the inspector's J-space rank checks (kept as they are on regeneration), and one
section per tier-1 view: its claim in the README's words (quoted from docs/depth/README.md at generation, src comments
stripped), its numbers recounted beside their source, its runs and flags, its checks and the 10 items of the fixed
sample. CPU only; reads files, writes docs/review/verify_pack.md.

make verify-pack        # verify-checks + verify-independent, then this
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bridge_jspace.review import items as I

PACK = I.REPO / "docs" / "review" / "verify_pack.md"
CHECKS = I.REPO / "review" / "verify_checks.json"
INDEP = I.REPO / "review" / "verify_independent.json"
README = I.REPO / "docs" / "depth" / "README.md"
LEDGER = I.REPO / "docs" / "depth" / "EXPERIMENTS.md"
INSPECTOR = "## J-space rank checks (inspector)"
JSPACE = I.REPO / "docs" / "review" / "verify_pack_jspace.md"  # the inspector agent's section, included verbatim
INSPECTOR_TODO = ("_Reserved for the inspector agent (inspector_1145 item 3): the rank of S's bridge token and of the answer "
                  "words in the readout of the J++ part, the rest and a random part of the same share, at L and the bridge "
                  "word, over every item of the conflict test and the routes test. Not written yet. Everything between this "
                  "heading and the next view section is kept when the pack is regenerated._")  # fmt: skip
EXTRA = {"answer_control": ["the 122B's answer control landed after the sample was fixed; not in the hand-check (Dan 12:10, "
                            "jobs/c3/batch53.yaml decisions_1210b)"]}  # fmt: skip
MINUTES = 15  # per view: 7 views x 15 min ~ 1 h 45 min, ~1.5 min per item


def strip(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text).replace("\\|", "|").strip()


def readme_rows(nums: list[int]) -> list[str]:
    out = []
    for line in README.read_text().splitlines():
        m = re.match(r"\| (\d+) \| (.+)", line)
        if m and int(m.group(1)) in nums:
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            n, claim, models, grade, key = (strip(c) for c in cells[:5])
            out.append(f"Claims row {n} ({grade}; {models}): **{claim}** Key numbers: {key}")
    return out


def readme_quotes(subs: list[str], source: Path = README) -> list[str]:
    lines = source.read_text().splitlines()
    out = []
    for s in subs:
        hit = next((ln for ln in lines if s in ln), None)
        out.append(strip(hit).lstrip("- ").strip() if hit else f"(not found in the README: {s!r})")
    return out


def label(m: str) -> str:
    return I.spec()["models"][m]["label"]


def fmt(x: float, quantity: str = "") -> str:
    """Counts (k, n) as integers, everything else with 2 decimals."""
    return f"{x:.0f}" if quantity.endswith((": k", ": n")) else f"{x:.2f}".replace("-", "−")


def numbers_table(vid: str, rc: list[dict]) -> list[str]:
    """quantity x model: the recount over the whole item set; ✓ = equals its source (x0_numbers.json, 2 decimals, or
    data.csv), ✗ = differs (its source's value beside), – = no source for that model."""
    keep = [r for r in rc if r["status"] != "no source" or vid in ("answer_control", "x8_writes")]
    if vid == "routes":
        keep = [
            r for r in keep if r["quantity"].startswith("C2 ") and re.search(r": (identity|position)$", r["quantity"])
        ]
    models = [m for m in I.spec()["models"] if any(r["model"] == m for r in keep)]
    qs = list(dict.fromkeys(r["quantity"] for r in keep))
    cell = {(r["quantity"], r["model"]): r for r in keep}
    out = [
        "| recounted quantity (n per model) | " + " | ".join(label(m) for m in models) + " |",
        "|---" * (len(models) + 1) + "|",
    ]
    for q in qs:
        cs = []
        for m in models:
            r = cell.get((q, m))
            if r is None:
                cs.append("")
                continue
            mark = {"match": " ✓", "mismatch": f" ✗ (source {r['data']})", "no source": " (no source)"}[r["status"]]
            cs.append(f"{fmt(r['value'], q)}{mark} <sub>n {r['n']}</sub>")
        out.append(f"| {q} | " + " | ".join(cs) + " |")
    return out


def check_lines(vc: dict) -> list[str]:
    out = []
    for m, x in vc["models"].items():
        if not x.get("n"):
            nl = "; ".join(f"`{r}` ({s})" for r, s in x.get("not_landed", []))
            out.append(f"- {label(m)}: no items" + (f" ({nl})" if nl else ""))
            continue
        fails = ", ".join(f"{k}: {n}" for k, n in x["item_fail"].items()) or "none"
        na = ", ".join(f"{k}: {n}" for k, n in x["item_na"].items())
        bad = [c for c in x["run_checks"] if c["status"] not in ("pass",)]
        out.append(f"- {label(m)}: {x['n']} items; per-item failures: {fails}" + (f" (n/a: {na})" if na else "")
                   + (f"; run checks: {sum(c['status'] == 'pass' for c in x['run_checks'])} pass" if x["run_checks"] else ""))  # fmt: skip
        for c in bad:
            out.append(f"  - **{c['status']}**: {c['check']}: {c['detail']}")
        for f in x["item_fail_examples"][:4]:
            out.append(f"  - **fail** `{f['item']}` ({f['check']}): {f['detail']} ({f['where']})")
    return out


def sample_lines(vid: str) -> list[str]:
    fs = (I.spec().get("fixed_sample") or {}).get("views", {}).get(vid) or []
    out = ["| # | model | reader | scene | why it is in the sample |", "|---|---|---|---|---|"]
    for n, e in enumerate(fs, 1):
        extra = f" · {e['condition']}" if e.get("condition") else ""
        if e.get("x8"):
            extra += f" · slot {e['x8']['j']} → {e['x8']['k']}, s = {e['x8']['s']:g}"
        why = e["stratum"].replace("|", "\\|")  # "|p_alt - p_org|" inside a table cell
        out.append(f"| {n} | {label(e['model'])} | {I.READER_NAME[e['reader']]} | `{e['scene']}`{extra} | {why} |")
    return out


TOP_NOT_STORED = ("The conflict-test runs of the 9B, 27B, 122B and Muse store no top token (only the label): on their "
                  "cards the top token reads \"not stored\", and the check \"label = top token == S's answer\" is n/a "
                  "there. Their labels were compared with the 51.12 E1 rerun of the same prompts, which stores the top "
                  "token: the 27B agrees on every arm; the 9B, Muse and Lightning differ on 1 to 7 of 400 per arm "
                  "(near ties: two runs of identical prompts are not bit-reproducible).")  # fmt: skip
READ_FIRST = {
    "main_swap": [TOP_NOT_STORED],
    "sentence_order": [TOP_NOT_STORED],
    "z1p": ["Dan's check \"the true value is absent from the lookup's passage\" fails on 60 of 200 lookup passages: the "
            "bridge's true value appears there as another entity's made-up value (the made-up values are drawn from the "
            "relation's own answer words). Example jsuite_v2_test_chat/j2:cities:P-L0-Moscow-0: Moscow's true country is "
            "Russia; the passage says \"This year's partner city for Mumbai is in Russia\", while the lookup's answer is "
            "the made-up France. The 60 passages: review/verify_checks.json, view z1p, check \"Z1-P: the true value is "
            "absent from the lookup's passage\".",
            "The token-diff check fails on 2 passages (4 items) with hyphenated multi-word bridges (\"Mont Saint-Michel\" "
            "→ \"Christ the Redeemer\"): every differing token is inside the bridge name, but the check splits words at "
            "\"-\" (a limit of the check, not changed): results/x50_zach/qwen35_9b_x52_z1p/outcomes.jsonl lines 665, "
            "669, 1553, 1557.",
            "Zach's prompts end at the chat template (no \"Answer:\", nothing appended at the read); his answers are "
            "words read by their first token."],
    "x8_writes": ["The swap runs store no probabilities: \"nearest the decision\" cannot be computed, so the 4 targeted "
                  "items are all \"surprising\" (2: the lookup goes to the target, the recall does not change; 2: the "
                  "recall changes, the lookup does not go to the target). The probability check is n/a."],
    "last_token": ["Per item the run stores the write outcomes and the plain logit lens's top token at the last token; "
                   "the J++ lens readout's top words per item are not stored (the inspector panel computes them)."],
}  # fmt: skip


def read_first(vid: str, vc: dict) -> list[str]:
    """Automatic-check findings to read before the view's items: its failures, what is not computable, and the
    sample's items that sit on an exact logit tie."""
    out = []
    for m, x in vc["models"].items():
        for c in x.get("run_checks", []):
            if c["status"] == "fail":
                out.append(f"{label(m)}: **{c['check']}** failed: {c['detail']}")
        for f in x.get("item_fail_examples", [])[:4]:
            out.append(f"{label(m)}: **{f['check']}** failed on `{f['item']}`: {f['detail']} ({f['where']})")
        for r in [r for r in vc["recount"]["mismatch"] if r["model"] == m]:
            out.append(f"{label(m)}: recount mismatch, {r['quantity']}: {r['value']:.4f} against {r['data']}")
    out += READ_FIRST.get(vid, [])
    fs = (I.spec().get("fixed_sample") or {}).get("views", {}).get(vid) or []
    ties = [str(n) for n, e in enumerate(fs, 1) if "= 0.0000" in e["stratum"]]
    if ties:
        out.append(f"Items {', '.join(ties)} sit on a tie as stored under a decisive arm (P(original) = P(changed) to 4 "
                   "decimals, logit gap 0.000): the label there is decided by the argmax's tie-break, not by a margin.")  # fmt: skip
    return [f"- {x}" for x in out]


def flags(v: dict) -> list[str]:
    out = []
    for m in v.get("runs", {}):
        fl = [*I.spec()["models"][m].get("flags", []), *(v.get("model_flags") or {}).get(m, [])]
        if fl:
            out.append(f"- {label(m)}: " + "; ".join(fl))
    return out


def inspector_section(old: str) -> list[str]:
    """The inspector agent's section: docs/review/verify_pack_jspace.md verbatim where it exists (their file, the source); else
    the section as it stands in the current pack (up to the first view section); else a stub."""
    if JSPACE.exists():
        body = JSPACE.read_text().strip("\n")
        return [
            INSPECTOR,
            "",
            "_Included verbatim from docs/review/verify_pack_jspace.md (the inspector agent's file)._",
            "",
            body,
            "",
        ]
    if INSPECTOR in old:
        body = old.split(INSPECTOR, 1)[1]
        body = re.split(r"\n## a\. ", body, maxsplit=1)[0].strip("\n")
        return [INSPECTOR, "", body, ""] if body.strip() else [INSPECTOR, "", INSPECTOR_TODO, ""]
    return [INSPECTOR, "", INSPECTOR_TODO, ""]


def commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=I.REPO, capture_output=True, text=True
    ).stdout.strip()


def build(old: str = "") -> str:
    vc = json.loads(CHECKS.read_text())
    ind = json.loads(INDEP.read_text()) if INDEP.exists() else None
    views = [v for v in I.spec()["views"] if v.get("tier") == 1]
    tier2 = sorted(
        (v for v in I.spec()["views"] if v.get("tier") == 2 and v["id"] in vc["views"]), key=lambda v: v["order"]
    )
    fs = I.spec().get("fixed_sample") or {}
    L = ["# Verification pack: the seven headline claims, for Dan's hand check (30 Oct)", "",
         f"Generated by `make verify-pack` (scripts/verify_pack_tier1.py) at {commit()}, {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}, "
         f"from docs/review/review_views.yaml, review/verify_checks.json ({vc['generated_utc']}), review/verify_independent.json and "
         "docs/depth/README.md (quoted as it stands). Do not edit by hand; regenerate. Every claim below is UNVERIFIED "
         "until it is in VERIFIED.md. The pack of 26 Oct is in git history (docs/review/verify_pack.md before this commit); the "
         "one of 25 Oct is docs/archive/verify_pack_25oct.md.", "",
         "## How to review in 2 hours", "",
         "**Open it.** `make review-serve SEED=29`, then http://localhost:8001 (marks go to review/marks.jsonl). Without "
         "a server: `make review-export SEED=29 N=10`, then open review/seed-29/index.html (marks stay in the browser; "
         "the page's download button saves them as marks.jsonl, to put in review/).", "",
         f"**The order.** Seven views, {fs.get('n_per_view', 10)} items each (seed {fs.get('seed', 29)}, fixed in "
         "docs/review/review_views.yaml, never re-rolled): about 15 minutes per view, 1.5 minutes per item.", "",
         "| | view | the claim in short | models | your items |", "|---|---|---|---|---|"]  # fmt: skip
    for v in views:
        ms = ", ".join(label(m) for m in v["runs"] if vc["views"][v["id"]]["models"].get(m, {}).get("n"))
        L.append(f"| {v['order']} | [{v['id']}](#{v['order']}-{v['id'].replace('_', '-')}) | {v['title'].split('. ', 1)[1]} | {ms} | "
                 f"{len((fs.get('views') or {}).get(v['id']) or [])} |")  # fmt: skip
    if tier2:
        L += ["", "Tier 2, only once tier 1 is done (no fixed sample): " + "; ".join(
            f"[{v['order']}. {v['id']}](#{v['order']}-{v['id'].replace('_', '-')})" for v in tier2) + "."]  # fmt: skip
    L += ["",
          "**Each item: three questions**, answered from the card's first boxes:",
          "1. *Is the prompt what the claim says?* \"As the model saw it\" decodes the stored token ids with the pinned "
          "tokenizer: the chat template, thinking off, the reply begun with \"Answer:\" (Zach's passages end at the "
          "template, no \"Answer:\"), the token the run appended at the read in grey, the changed token in red. Is the "
          "changed prompt the claim's change (two picks swapped; another item moved; the bridge's sentence only)?",
          "2. *Is each arm's top token what is shown?* \"The decisive arms\" gives, per reader and arm, the top token "
          "decoded from its stored id and the run's label. The conflict-test runs of the 9B, 27B, 122B and Muse stored no "
          "top token (\"not stored\"): read the label against P(original) and P(changed) under \"the stored numbers\" "
          "(their labels were also compared with the 51.12 rerun, which stored the token: see the automatic checks).",
          "3. *Does the label follow?* The original answer is \"original answer (A)\", the changed answer \"changed "
          "answer (b)\" and a switch; routes: the digit each route predicts is listed above the arms; the swap: the "
          "swapped-in slot's digit is named on the card.", "",
          "**Mark** each item consistent / wrong / unclear, with a note for wrong or unclear (what you saw, e.g. \"label "
          "b, but the top token is '7' and S's answer is '4'\"). The last mark per item counts.", "",
          "**Stop rule.** Two items marked wrong in one view: stop that view, flag it in the note of the second, go on "
          "to the next view. A flagged view is not hand-checked.", "",
          "**What a machine already checked** (do not redo it): the section below, over every item of every view (not "
          "only your 70), with each failure's file and line; each card also shows its own check badges (red: fail). "
          "Read a failure there before the view it belongs to.", "",
          "**After.** `make review-summary` (docs/review/review_summary.md: per view, items read, consistent / wrong / unclear, "
          "flagged items) and `make review-verified` (VERIFIED.md's generated section: per claim, the hand marks, the "
          "automatic checks and the independent recount).", "",
          "## Automatic checks", "",
          "scripts/verify_checks.py over every item of the seven views (not the sample), and scripts/verify_independent.py, "
          "written from scratch (standard library only, no pipeline or review import). Per item: the changed token "
          "decodes to the bridge in O and S; the answers decode to the stated answers; the label equals \"top token == "
          "S's answer\" recomputed from the stored ids; the prompts differ only in the scene's words; the probabilities "
          "agree with the label; a second run's prompts are the same. Per run: gate and eligibility recomputed from "
          "competence.jsonl; duplicates; Z1-P's facts; the random part's share against the lens part's; the headline "
          "numbers recounted from the per-item files against x0_numbers.json / data/figures/depth/data.csv.", "",
          "| view | items | per-item failures | run checks failed | headline recount | n/a (not computable) |",
          "|---|---|---|---|---|---|"]  # fmt: skip
    findings = []
    for v in views + tier2:
        if v["id"] not in vc["views"]:  # checks not run for it yet (make verify-checks)
            continue
        r = vc["views"][v["id"]]
        n = sum(x.get("n", 0) for x in r["models"].values())
        nf = sum(sum(x.get("item_fail", {}).values()) for x in r["models"].values())
        bad = [(m, c) for m, x in r["models"].items() for c in x.get("run_checks", []) if c["status"] == "fail"]
        na = {}
        for x in r["models"].values():
            for k, c in x.get("item_na", {}).items():
                na[k] = na.get(k, 0) + c
        rc = r["recount"]
        L.append(f"| {v['order']}. {v['id']} | {n} | {nf} | {len(bad)} | {rc['match']} match, {len(rc['mismatch'])} mismatch | "
                 + ("; ".join(f"{k}: {c}" for k, c in na.items() if k != "second run has the same prompts") or "–") + " |")  # fmt: skip
        for m, x in r["models"].items():
            for f in x.get("item_fail_examples", []):
                findings.append(
                    f"- {v['order']}. {v['id']}, {label(m)}: `{f['item']}`: {f['check']}: {f['detail']} ({f['where']})"
                )
        findings += [f"- {v['order']}. {v['id']}, {label(m)}: {c['check']}: {c['detail']}" for m, c in bad]
        findings += [f"- {v['order']}. {v['id']}, {label(m)}: {r_['quantity']}: recount {r_['value']:.4f}, source {r_['data']}"
                     for m in r["models"] for r_ in rc["mismatch"] if r_["model"] == m]  # fmt: skip
    L += [
        "",
        "**Failures** (findings: listed, not fixed; no check was changed to pass):",
        "",
        *(findings or ["None."]),
        "",
    ]
    L += ["**Read beside them.**",
          "- The label check is n/a on the conflict-test runs of the 9B, 27B, 122B and Muse (views a and g): they store "
          "no top token. Their labels against the 51.12 E1 rerun of the same prompts (which stores it) are the run check "
          "\"labels against the 51.12 E1 rerun\" in view a; two runs of identical prompts disagree on a few near-tie "
          "items, so that check fails on the 9B, Muse and Lightning by 1 to 7 items of 400 per arm.",
          "- Z1-P, the true value in the lookup's passage (Dan's check, failed on 60 of 200): the made-up values are "
          "drawn from the relation's own answer words, so the bridge's true value often stands in the passage as "
          "another entity's made-up value (Moscow, true country Russia: \"This year's partner city for Mumbai is in "
          "Russia\", while the lookup's answer is the made-up \"France\"). Whether that matters for the claim is for "
          "you to judge; the list of passages is in review/verify_checks.json (z1p).",
          "- The Z1-P token-diff failures are hyphenated multi-word bridges (\"Mont Saint-Michel\" → \"Christ the "
          "Redeemer\"): every differing token is inside the bridge name, but the check splits words at \"-\".",
          "- The x8 probability check is n/a: the swap runs store no probabilities. Several targeted items are exact "
          "logit ties (P(original) = P(changed), logit gap 0.0; the argmax keeps the lower token id).", ""]  # fmt: skip
    if ind:
        s = ind["summary"]
        L += [f"**Independent recount** (review/verify_independent.json): {s['match']} of {s['rows']} numbers equal the "
              f"README's and their source, {s['mismatch']} differ; the item sets recomputed from competence.jsonl equal "
              "the runs' on every model (conflict test, routes); each routes label recomputed from the raw top-token id "
              "equals the stored one. The 9B (the brief's model):", "",
              "| quantity | recomputed | README shows | source |", "|---|---|---|---|"]  # fmt: skip
        L += [f"| {r['quantity']} | {r['value']:+.4f} | {', '.join(r['readme']) or '–'} | {r['source']} ({r['status']}) |"
              for r in ind["rows"] if r["model"] == "9b"]  # fmt: skip
        L.append("")
    L += inspector_section(old)
    for v in views + tier2:
        r = vc["views"][v["id"]]
        if v is (tier2 or [None])[0]:
            L += ["## Tier 2: only once tier 1 is done", "",
                  "Dan 11:45: \"Tier 2, only if tier 1 is done\". In the dashboard, checked and recounted like tier 1, but "
                  "with no fixed sample (their items are not in the inspector's states job): open a view at any seed for a "
                  "random sample.", ""]  # fmt: skip
        title = v["title"] if v["title"].endswith(("?", ".")) else v["title"] + "."
        L += [f"## {v['order']}. {v['id']}", "", f"**{title}** README: {v.get('readme', '')}.", ""]
        first = read_first(v["id"], r)
        L += ["**Read first: automatic-check findings for this view.**", "", *(first or ["- None."]), ""]
        quotes = readme_rows(v.get("readme_rows") or []) + readme_quotes(v.get("readme_quotes") or [])
        where = "README's"
        if v.get("ledger_quotes"):  # not in the README yet: the ledger's words
            quotes += readme_quotes(v["ledger_quotes"], LEDGER)
            where = "ledger's (docs/depth/EXPERIMENTS.md)" if not v.get("readme_quotes") else where
        L += [f"**The claim in the {where} words** (quoted at generation):", "", *[f"> {q}" for q in quotes], ""]
        L += [f"**What the cards test.** {v['claim'].strip()}", ""]
        L += [
            "**Numbers**, recounted over the whole item set (✓ equals its source):",
            "",
            *numbers_table(v["id"], r["recount"]["rows"]),
            "",
        ]
        L += [
            "**Runs.** " + "; ".join(f"{label(m)}: " + ", ".join(f"`{x}`" for x in rs) for m, rs in v["runs"].items()),
            "",
        ]
        fl = flags(v)
        if fl:
            L += ["**Flags.**", *fl, ""]
        L += ["**Automatic checks.**", *check_lines(r), ""]
        if v.get("tier") == 1:
            L += [f"**Your {len((fs.get('views') or {}).get(v['id']) or [])} items** (open the view in the dashboard; "
                  "the same items, in this order by model):", "", *sample_lines(v["id"]), ""]  # fmt: skip
        else:
            L += ["**Items.** No fixed sample (tier 2): the dashboard draws a random one at any seed.", ""]
        notes = [*EXTRA.get(v["id"], []), *([v["notes"].strip()] if v.get("notes") else [])]
        if notes:
            L += ["**Notes.**", *[f"- {x}" for x in notes], ""]
    return "\n".join(L) + "\n"


def main() -> Path:
    old = PACK.read_text() if PACK.exists() else ""
    PACK.write_text(build(old))
    print(f"wrote {PACK.relative_to(I.REPO)}")
    return PACK


if __name__ == "__main__":
    main()
