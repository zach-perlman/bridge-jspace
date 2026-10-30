"""atoms_multilingual: the 25 atoms of the J++ part, classified again with number words in other languages (Dan's
hand-check, 30 Oct: the 27B's atom 4 "，三" is Chinese "three", the recall's original answer, classed "other"; atom 10 " oito"
is Portuguese "eight"). CPU only, from the stored atoms (results/x52_atoms/report-*/labelled.jsonl: every atom of the 50 main-test
items per model, in both readers' views, with its old class, coefficient and energy share); no GPU, no run is changed.

New classes, laid over the old ones:
  answer (any language)    the token is a number word, ordinal, Roman numeral or digit (1-10) whose value is the view's
                           reader's original or changed answer, in English, Chinese, Japanese, Korean, Russian, Ukrainian,
                           German, French, Spanish, Portuguese or Italian
  number, not the answer   the same kinds of token with any other value
Every other atom keeps its old class (the old "answer_own" / "answer_other" are English number words, digits and ordinals; the
new classes contain them). Before matching a token, leading and trailing punctuation and spaces are stripped, the text is
NFKC-normalised and case-folded (Roman numerals are matched in capitals, two letters or more: a lone I, V or X is a letter of the dictionary's letter tokens).

Per model, over the f5 set (the 50 main-test items of the atoms report) and over the answer-control items (the 51.12 E1 scenes
among them), in each reader's view: the mean share of the J++ part's energy in each class (items averaged, as x52_atoms'
per_item), the share of items with an answer atom, and the answer energy split by the coefficient's sign (negative: toward the
original prompt, positive: toward the changed one). The old "answer" share (x52_atoms' answer_own) beside the new one, and the
largest examples.

uv run python scripts/atoms_multilingual.py        # writes results/atoms_multilingual/<UTC>/ (manifest first)
"""

from __future__ import annotations

import collections
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import x0_necessity as X  # noqa: E402

EXP = "atoms_multilingual"
X52 = REPO / "results" / "x52_atoms"
REPORTS = ("report-20261029T000125Z", "report-20261029T010648Z", "report-20261030T094628Z")  # 9B 27B Muse / Lightning / 122B
MODELS = ("muse-glimmer-30b", "qwen3.5-9b", "qwen3.6-27b", "nemotron-3.5-lightning", "qwen3.5-122b-a10b")  # Muse first (Dan's case)
RUNS = {"qwen3.5-9b": "qwen35_9b_x52_atoms_fwd", "qwen3.6-27b": "x52_atoms_fwd_27b", "muse-glimmer-30b": "muse30_x52_atoms_fwd",
        "nemotron-3.5-lightning": "nem35l_x52_atoms_fwd", "qwen3.5-122b-a10b": "qwen35_122b_x52_atoms_fwd"}  # fmt: skip
VIEWS = ("PM", "PP")  # f5 draws the recall's view (PM)
EDGE = re.compile(r"^[\W_]+|[\W_]+$")
CLASSES = ("bridge", "new_bridge", "answer_any", "number_other", "scene_item", "person", "same_class", "function", "other")
CLASS_TEXT = {"bridge": "old bridge word", "new_bridge": "new bridge word", "answer_any": "answer (any language)",
              "number_other": "number, not the answer", "scene_item": "another scene item", "person": "a person",
              "same_class": "a same-class word", "function": "function word / punctuation", "other": "other"}  # fmt: skip
OLD_TO_NEW = {"answer_own": "number_other", "answer_other": "number_other"}  # overridden below where the value is the answer

# ---- the lexicon: value 1-10 -> {language: [forms]} ---------------------------------------------------------------------
CARDINAL: dict[str, list[list[str]]] = {  # per language: forms of 1, 2, ..., 10 (variants inside a list)
    "English": [["one"], ["two"], ["three"], ["four"], ["five"], ["six"], ["seven"], ["eight"], ["nine"], ["ten"]],
    "Chinese": [["一", "壹"], ["二", "两", "貳", "贰"], ["三", "叁", "參"], ["四", "肆"], ["五", "伍"], ["六", "陆", "陸"], ["七", "柒"],
                ["八", "捌"], ["九", "玖"], ["十", "拾"]],  # Japanese kanji are the same characters: tagged "Chinese / Japanese"
    "Japanese": [["いち", "イチ", "ひとつ"], ["に", "ニ", "ふたつ"], ["さん", "サン", "みっつ"], ["よん", "し", "ヨン", "よっつ"], ["ご", "ゴ", "いつつ"],
                 ["ろく", "ロク", "むっつ"], ["なな", "しち", "ナナ", "ななつ"], ["はち", "ハチ", "やっつ"], ["きゅう", "く", "キュウ", "ここのつ"],
                 ["じゅう", "ジュウ", "とお"]],
    "Korean": [["하나", "일", "한"], ["둘", "이", "두"], ["셋", "삼", "세"], ["넷", "사", "네"], ["다섯", "오"], ["여섯", "육"], ["일곱", "칠"],
               ["여덟", "팔"], ["아홉", "구"], ["열", "십"]],
    "Russian": [["один", "одна", "одно"], ["два", "две"], ["три"], ["четыре"], ["пять"], ["шесть"], ["семь"], ["восемь"], ["девять"],
                ["десять"]],
    "Ukrainian": [["один", "одна", "одне"], ["два", "дві"], ["три"], ["чотири"], ["п'ять", "пʼять", "пять"], ["шість"], ["сім"], ["вісім"],
                  ["дев'ять", "девʼять", "девять"], ["десять"]],
    "German": [["eins", "ein", "eine"], ["zwei"], ["drei"], ["vier"], ["fünf", "funf"], ["sechs"], ["sieben"], ["acht"], ["neun"], ["zehn"]],
    "French": [["un", "une"], ["deux"], ["trois"], ["quatre"], ["cinq"], ["six"], ["sept"], ["huit"], ["neuf"], ["dix"]],
    "Spanish": [["uno", "un", "una"], ["dos"], ["tres"], ["cuatro"], ["cinco"], ["seis"], ["siete"], ["ocho"], ["nueve"], ["diez"]],
    "Portuguese": [["um", "uma"], ["dois", "duas"], ["três", "tres"], ["quatro"], ["cinco"], ["seis"], ["sete"], ["oito"], ["nove"], ["dez"]],
    "Italian": [["uno", "un", "una"], ["due"], ["tre"], ["quattro"], ["cinque"], ["sei"], ["sette"], ["otto"], ["nove"], ["dieci"]],
}
ORDINAL: dict[str, list[list[str]]] = {
    "English": [["first", "1st"], ["second", "2nd"], ["third", "3rd"], ["fourth", "4th"], ["fifth", "5th"], ["sixth", "6th"], ["seventh", "7th"],
                ["eighth", "8th"], ["ninth", "9th"], ["tenth", "10th"]],
    "Chinese": [["第一"], ["第二"], ["第三"], ["第四"], ["第五"], ["第六"], ["第七"], ["第八"], ["第九"], ["第十"]],
    "Korean": [["첫째", "첫번째"], ["둘째", "두번째"], ["셋째", "세번째"], ["넷째", "네번째"], ["다섯째"], ["여섯째"], ["일곱째"], ["여덟째"], ["아홉째"],
               ["열째"]],
    "Russian": [["первый", "первая", "первое"], ["второй", "вторая"], ["третий", "третья"], ["четвёртый", "четвертый"], ["пятый"], ["шестой"],
                ["седьмой"], ["восьмой"], ["девятый"], ["десятый"]],
    "Ukrainian": [["перший"], ["другий"], ["третій"], ["четвертий"], ["п'ятий", "пʼятий"], ["шостий"], ["сьомий"], ["восьмий"], ["дев'ятий", "девʼятий"],
                  ["десятий"]],
    "German": [["erste", "erster", "erstes"], ["zweite", "zweiter"], ["dritte", "dritter"], ["vierte", "vierter"], ["fünfte", "fünfter"],
               ["sechste", "sechster"], ["siebte", "siebter"], ["achte", "achter"], ["neunte", "neunter"], ["zehnte", "zehnter"]],
    "French": [["premier", "première"], ["deuxième", "second", "seconde"], ["troisième"], ["quatrième"], ["cinquième"], ["sixième"], ["septième"],
               ["huitième"], ["neuvième"], ["dixième"]],
    "Spanish": [["primero", "primer", "primera"], ["segundo", "segunda"], ["tercero", "tercer", "tercera"], ["cuarto", "cuarta"], ["quinto", "quinta"],
                ["sexto", "sexta"], ["séptimo", "séptima"], ["octavo", "octava"], ["noveno", "novena"], ["décimo", "décima"]],
    "Portuguese": [["primeiro", "primeira"], ["segundo", "segunda"], ["terceiro", "terceira"], ["quarto", "quarta"], ["quinto", "quinta"],
                   ["sexto", "sexta"], ["sétimo", "sétima"], ["oitavo", "oitava"], ["nono", "nona"], ["décimo", "décima"]],
    "Italian": [["primo", "prima"], ["secondo", "seconda"], ["terzo", "terza"], ["quarto", "quarta"], ["quinto", "quinta"], ["sesto", "sesta"],
                ["settimo", "settima"], ["ottavo", "ottava"], ["nono", "nona"], ["decimo", "decima"]],
}
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
WEAK = {"I", "V", "X", "un", "um", "a", "ein", "and", "이", "일", "사", "오", "구", "십", "に", "し", "く", "ご", "한", "두", "세", "네", "열", "dos", "sei"}
# tokens that are common words in their own language as well: reported, never hidden (the examples show them)


def _build() -> dict[str, list[tuple[int, str, str]]]:
    """form -> [(value, language, kind)]. Lower-cased forms; Roman numerals are kept in capitals."""
    table: dict[str, list[tuple[int, str, str]]] = collections.defaultdict(list)
    for kind, src in (("number word", CARDINAL), ("ordinal", ORDINAL)):
        for lang, per in src.items():
            for v, forms in enumerate(per, 1):
                for f in forms:
                    table[unicodedata.normalize("NFKC", f).casefold()].append((v, lang, kind))
    for v, r in enumerate(ROMAN, 1):
        table[r].append((v, "Roman numeral", "roman"))
    return dict(table)


LEXICON = _build()


def normalise(token: str) -> str:
    return EDGE.sub("", unicodedata.normalize("NFKC", token)).strip()


def numbers_of(token: str) -> list[tuple[int, str, str]]:
    """[(value 1-10, language, kind)] a token stands for, [] if it is no number. Kanji are tagged Chinese / Japanese."""
    s = normalise(token)
    if not s:
        return []
    out: list[tuple[int, str, str]] = []
    if s in ROMAN and len(s) >= 2:  # capitals, two letters or more: the dictionary's atoms are letter tokens, and a lone "I", "V",
        out.append((ROMAN.index(s) + 1, "Roman numeral", "roman"))  # "X" is a letter (or the pronoun), not a numeral
    low = s.casefold()
    for v, lang, kind in LEXICON.get(low, []):
        if kind == "roman":
            continue
        out.append((v, "Chinese / Japanese" if lang in ("Chinese", "Japanese") and low[0] in "一二三四五六七八九十壹贰貳两叁參肆伍陆陸柒捌玖拾第" else lang, kind))
    digits = "".join(str(unicodedata.digit(c, "x")) for c in s)
    if s and digits.isdigit() and 1 <= int(digits) <= 10:  # 3, ３, ٣, ३ (a digit run with leading space or punctuation)
        out.append((int(digits), "digit", "digit"))
    return out


def classify(atom: dict, answers: tuple[int, int]) -> tuple[str, list[tuple[int, str, str]]]:
    """(new class, the number readings) of one atom; answers: the view's reader's original and changed answer."""
    nums = numbers_of(atom["token"])
    if nums:
        if any(v in answers for v, _, _ in nums):
            return "answer_any", [n for n in nums if n[0] in answers]
        return "number_other", nums
    old = atom["class"]
    if old in OLD_TO_NEW:  # an English-number class that matched no value by the new rule (a plural, an alias): number, not the answer
        return "number_other", []
    return old, []


# ---- items and shares -------------------------------------------------------------------------------------------------
def labelled() -> dict[tuple[str, str, str], list[dict]]:
    """(model, view, scene) -> the old-classified atoms, from the three x52 reports."""
    out = {}
    for rep in REPORTS:
        for line in (X52 / rep / "labelled.jsonl").read_text().splitlines():
            r = json.loads(line)
            if r["set"] == "e1":
                out[(r["target"], r["view"], r["key"])] = r
    return out


def answers_of(model: str) -> dict[str, dict[str, tuple[int, int]]]:
    """scene -> reader view -> (original answer, changed answer), from the run's items.jsonl."""
    out = {}
    for line in (X52 / RUNS[model] / "items.jsonl").read_text().splitlines():
        it = json.loads(line)
        if it["set"] == "e1":
            out[it["key"]] = {w: tuple(int(a) for a in v) for w, v in it["views"]["PP"]["answers"].items()}
    return out


def answer_control_scenes(model: str) -> set[str]:
    from bridge_jspace.review import items as I

    return {it["scene"] for it in I.items("answer_control", model)}


def item_record(rec: dict, answers: tuple[int, int]) -> dict:
    atoms, total = [], sum(a["share"] for a in rec["atoms"])
    for a in rec["atoms"]:
        cls, nums = classify(a, answers)
        atoms.append({**a, "new_class": cls, "numbers": nums})
    energy = {c: sum(a["share"] for a in atoms if a["new_class"] == c) / total for c in CLASSES}
    old = sum(a["share"] for a in rec["atoms"] if a["class"] == "answer_own") / total
    sign = {"toward original": sum(a["share"] for a in atoms if a["new_class"] == "answer_any" and a["coef"] < 0) / total,
            "toward changed": sum(a["share"] for a in atoms if a["new_class"] == "answer_any" and a["coef"] > 0) / total}  # fmt: skip
    return {"scene": rec["key"], "entity": rec["entity"], "atoms": atoms, "energy": energy, "old_answer": old, "sign": sign,
            "has_answer": any(a["new_class"] == "answer_any" for a in atoms),
            "has_other_language": any(a["new_class"] == "answer_any" and any(n[1] != "English" and n[2] != "digit" for n in a["numbers"]) for a in atoms)}  # fmt: skip


def interval(series: list[float], entities: list[str]) -> list[float]:
    boot = X.resampled_rates({"x": series}, entities, X.N_BOOT, X.BOOT_SEED)["x"]
    return [round(float(np.mean(series)), 4), *(round(b, 4) for b in X.interval(boot))]


def summarise(recs: list[dict]) -> dict:
    ents = [r["entity"] for r in recs]
    out = {"n": len(recs), "energy": {c: interval([r["energy"][c] for r in recs], ents) for c in ("answer_any", "number_other")},
           "energy_other_classes": {c: round(float(np.mean([r["energy"][c] for r in recs])), 4) for c in CLASSES},
           "old_answer": interval([r["old_answer"] for r in recs], ents),
           "items_with_answer": sum(r["has_answer"] for r in recs), "items_with_other_language_answer": sum(r["has_other_language"] for r in recs),
           "sign": {k: round(float(np.mean([r["sign"][k] for r in recs])), 4) for k in ("toward original", "toward changed")}}  # fmt: skip
    return out


def examples(recs_by: dict[str, list[dict]], k: int = 5) -> list[dict]:
    allx = []
    for model, recs in recs_by.items():
        for r in recs:
            for a in r["atoms"]:
                if a["new_class"] == "answer_any":
                    for v, lang, kind in a["numbers"][:1]:
                        allx.append({"model": model, "scene": r["scene"], "token": a["token"], "language": lang, "kind": kind, "value": v,
                                     "sign": "toward changed" if a["coef"] > 0 else "toward original", "coef": a["coef"],
                                     "energy_share": a["share"], "old_class": a["class"],
                                     "weak": normalise(a["token"]) in WEAK})  # fmt: skip
    allx.sort(key=lambda e: -e["energy_share"])
    return allx[:k]


def translation_forms(value: int) -> list[str]:
    """Every cardinal number word for a value 1-10 in the eleven languages (the answer word and its translations)."""
    return sorted({f for per in CARDINAL.values() for f in per[value - 1]})


NOT_READ_RANK = 50  # x51_answer: the answer word is "not read" at the bridge word when its lens rank is > 50 on both prompts


def whole_token_ids(tok, forms: list[str]) -> list[int]:
    """The token ids of each form that the tokenizer keeps whole, in its spellings (form, ' form', capitalised, ' Capitalised'). A word the
    tokenizer splits is left out: its first piece (' o' of 'oito', ' F' of 'fünf') is a letter, not the number word."""
    ids = set()
    for f in forms:
        for v in (f, f" {f}", f.capitalize(), f" {f.capitalize()}"):
            got = tok(v, add_special_tokens=False).input_ids
            if len(got) == 1:
                ids.add(int(got[0]))
    return sorted(ids)


def translation_ranks() -> dict:
    """51.12's "the answer word is not read" rests on the English number word's lens rank at the bridge word. Here, for the
    answer_control items whose states are on this machine (the review's fixed sample: cache/review_states, a few per model; the
    other items' states are on the box), the same rank taken as the best over the answer's translations: the recall's original
    answer in O, the changed one in S, rank 1 = top, the J++ lens at L and the bridge word. English first (checked against
    the run's stored rank), then the best over the answer's whole-token number words in all eleven languages (a word the tokenizer splits is left out); an item whose best rank is > 50 is 'not read', one at <= 50
    'read'; the items whose label would change."""
    from bridge_jspace.review import items as I
    from scripts import review_jspace as J

    out: dict = {}
    fs = I.spec()["fixed_sample"]["views"]["answer_control"]
    for model in MODELS:
        ro, rows = None, []
        rd, cs = J.x51_rows(model)
        la = J.model_layer(model)
        for e in fs:
            if e["model"] != model:
                continue
            it = next(i for i in I.items("answer_control", model) if i["id"] == e["item"])
            st = J.states(model, "answer_control", it["id"])
            if st is None:
                continue
            ro = ro or J.readout(model)
            import torch

            case = it["case"]["readers"]["PM"]
            res = {}
            for prompt, v, word in (("O", "org", case["answer"]), ("S", "alt", case["cf_answer"])):
                h, _why = J.vector(st, model, prompt, int(st["meta"]["pos"]), la, "state")
                x = torch.as_tensor(h)[None]
                lg = ro.lens(x, la)[0] if (not ro.no_lens and la in ro.lens_layers) else ro.unembed(x)[0]
                english = J.rank_of(lg, cs[it["scene"]]["tokens"]["own_word"][v]["PM"])[0]
                ids = whole_token_ids(ro.tok, translation_forms(int(word)))
                best, tid = J.rank_of(lg, ids)
                row = rd.get((it["scene"], v))
                res[prompt] = {"english_rank": english, "stored_rank": (row or {}).get("answer_word_rank", {}).get("PM"),
                               "best_rank_any_language": best, "best_token": ro.decode(tid), "lens": "J++" if (not ro.no_lens and la in ro.lens_layers) else "logit lens"}  # fmt: skip
            old, new = min(r["english_rank"] for r in res.values()), min(r["best_rank_any_language"] for r in res.values())
            rows.append({"scene": it["scene"], "reader_card": it["reader"], "O": res["O"], "S": res["S"], "english_best": old, "translation_best": new,
                         "label_english": "not read" if old > NOT_READ_RANK else "read", "label_translations": "not read" if new > NOT_READ_RANK else "read",
                         "changes": (old > NOT_READ_RANK) != (new > NOT_READ_RANK)})  # fmt: skip
        out[model] = {"n": len(rows), "changed": sum(r["changes"] for r in rows), "items": rows}
    return out


def muse_case() -> dict:
    """Dan's case: Muse, the 51.12 run muse30_x51_12_e1_r2, item P2-L0-0095: the change's 25 atoms at the bridge word (review states, the
    panel's atoms) under the new classes, with the atom '，三' (OMP 4)."""
    from bridge_jspace.review import items as I
    from scripts import review_jspace as J

    model = "muse-glimmer-30b"
    it = next(i for i in I.items("answer_control", model) if i["scene"] == "P2-L0-0095" and i["reader"] == "PP")
    st = J.states(model, "answer_control", it["id"])
    atoms = J.atoms_at(st, it, model, int(st["meta"]["pos"]), J.model_layer(model))
    case = it["case"]["readers"]["PM"]
    ans = (int(case["answer"]), int(case["cf_answer"]))
    total = sum(a["share"] for a in atoms)
    rows = []
    for a in atoms:
        cls, nums = classify({"token": a["token"], "class": a["x52_class"], "coef": a["coef"], "share": a["share"]}, ans)
        rows.append({"omp": a["rank"], "token": a["token"], "coef": a["coef"], "energy_share": a["share"], "old_class": a["class"], "new_class": cls,
                     "numbers": nums})  # fmt: skip
    return {"item": it["id"], "run": "muse30_x51_12_e1_r2", "recall_answers": {"original": ans[0], "changed": ans[1]}, "atoms": rows,
            "answer_energy_any_language": round(sum(r["energy_share"] for r in rows if r["new_class"] == "answer_any") / total, 4)}


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / EXP / stamp
    out.mkdir(parents=True, exist_ok=False)
    manifest = {"exp": EXP, "written_utc": stamp, "script": "scripts/atoms_multilingual.py", "inputs": [f"results/x52_atoms/{r}/labelled.jsonl" for r in REPORTS],
                "runs": RUNS, "views": VIEWS, "classes": CLASS_TEXT, "languages": sorted({*CARDINAL, "Roman numeral", "digit"}),
                "note": "CPU only; descriptive; the 51.12 verdicts are not rerun", "git": __import__("subprocess").run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))  # before the numbers (AGENTS.md)
    lab = labelled()
    tables: dict = {"sets": {}}
    recs_all: dict[tuple[str, str, str], list[dict]] = {}
    for model in MODELS:
        ans = answers_of(model)
        ac = answer_control_scenes(model)
        for view in VIEWS:
            scenes = sorted(s for (m, v, s) in lab if m == model and v == view)
            recs = [item_record(lab[(model, view, s)], ans[s][view]) for s in scenes]
            recs_all[(model, view, "f5")] = recs
            recs_all[(model, view, "answer_control")] = [r for r in recs if r["scene"] in ac]
    for (model, view, which), recs in recs_all.items():
        if recs:
            tables["sets"].setdefault(which, {}).setdefault(model, {})[view] = summarise(recs)
    tables["examples"] = examples({m: recs_all[(m, "PM", "f5")] + recs_all[(m, "PP", "f5")] for m in MODELS})
    tables["examples_by_model"] = {m: examples({m: recs_all[(m, "PM", "f5")] + recs_all[(m, "PP", "f5")]}, 3) for m in MODELS}
    tables["muse_case"] = muse_case()
    tables["translation_ranks"] = translation_ranks()
    (out / "tables.json").write_text(json.dumps(tables, indent=1, default=float))
    (out / "tables.md").write_text(render(tables))
    (out / "items.json").write_text(json.dumps({f"{m}|{v}|{w}": [{k: x for k, x in r.items() if k != "atoms"} for r in rs]
                                                for (m, v, w), rs in recs_all.items()}, default=float))
    print(f"wrote {out.relative_to(REPO)}")
    return out


def render_muse(t: dict) -> list[str]:
    c = t.get("muse_case")
    if not c:
        return []
    L = [f"## Muse first: Dan's case, `{c['item']}` ({c['run']})", "",
         f"The recall's answers: original {c['recall_answers']['original']}, changed {c['recall_answers']['changed']}. Share of the J++ part's energy in an answer "
         f"atom, any language: {c['answer_energy_any_language']}.", "", "| OMP | token | coefficient | energy share | old class | new class | reads as |", "|---|---|---|---|---|---|---|"]
    L += [f"| {r['omp']} | `{r['token']}` | {r['coef']:+.2f} | {r['energy_share']:.4f} | {r['old_class']} | {r['new_class']} | "
          f"{'; '.join(f'{v} {lang} {kind}' for v, lang, kind in r['numbers'][:2])} |" for r in c["atoms"][:12]]
    return [*L, ""]


def render_ranks(t: dict) -> list[str]:
    r = t.get("translation_ranks")
    if not r:
        return []
    L = ["## 51.12's 'the answer word is not read': English rank against the best over the translations", "",
         "The answer_control items whose states are on this machine (the review's fixed sample; the run's other items need the box). Rank 1 = top, "
         "the recall's answer in O and its changed answer in S, the J++ lens at L and the bridge word; not read = best rank over both prompts > 50.", "",
         "| model | items | label changes if translations count | per item: English best rank -> best over translations (token) |", "|---|---|---|---|"]
    for m in MODELS:
        x = r.get(m, {"n": 0, "changed": 0, "items": []})
        per = "; ".join(f"{i['scene']}: {i['english_best']} -> {i['translation_best']} ({i['O']['best_token'] if i['O']['best_rank_any_language'] <= i['S']['best_rank_any_language'] else i['S']['best_token']!r})"
                        f"{' CHANGES' if i['changes'] else ''}" for i in x["items"]) or "no states on this machine"
        L.append(f"| {m} | {x['n']} | {x['changed']} | {per} |")
    return [*L, ""]


def render(t: dict) -> str:
    L = ["# Multilingual answer classes for the 25 atoms (30 Oct)", "", *render_muse(t), *render_ranks(t),
         "Share of the J++ part's energy (mean over items). old: x52_atoms' answer_own (English number words, digits, ordinals of "
         "the reader's two answers); new: the reader's original or changed answer in any of eleven languages, Roman numerals and "
         "digits, leading punctuation and spaces stripped.", ""]
    for which, per in t["sets"].items():
        L += [f"## {which}", "", "| model | view | n | old answer share | new answer (any language) [95%] | number, not the answer | items with an answer atom | "
              "of those in another language | answer energy toward original / changed |", "|---|---|---|---|---|---|---|---|---|"]
        for m, views in per.items():
            for v, s in views.items():
                e = s["energy"]["answer_any"]
                L.append(f"| {m} | {v} | {s['n']} | {s['old_answer'][0]:.4f} | {e[0]:.4f} [{e[1]:.4f}, {e[2]:.4f}] | {s['energy']['number_other'][0]:.4f} | "
                         f"{s['items_with_answer']} of {s['n']} | {s['items_with_other_language_answer']} | {s['sign']['toward original']:.4f} / {s['sign']['toward changed']:.4f} |")
        L.append("")
    L += ["## The largest answer atoms (any model, both views, the f5 items)", "", "| model | scene | token | language | kind | value | sign | energy share | old class | weak |", "|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {e['model']} | {e['scene']} | `{e['token']}` | {e['language']} | {e['kind']} | {e['value']} | {e['sign']} | {e['energy_share']:.4f} | {e['old_class']} | {'weak' if e['weak'] else ''} |" for e in t["examples"]]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
