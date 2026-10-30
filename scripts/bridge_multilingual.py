"""bridge_multilingual: the bridge classes of the 25 atoms, in any language (Dan's hand-check, 30 Oct; CPU, saved atoms only; descriptive).

Extends scripts/atoms_multilingual.py (9a34b0b5, same inputs, same text normalisation, same single-token rule: an atom is a token, matched
whole after stripping edge punctuation and spaces, NFKC, case-folded) from the answer class to the bridge class. An atom is a bridge atom if
the saved English rules class it "bridge" / "new_bridge" (old = English), or its text is a form of the scene's old / new bridge word in one of
eleven languages or a symbol (Greek letters, lower and upper case; the two-letter chemical symbols He / Li, matched case-sensitively and
flagged weak). The bridge words are the 43 old and new entities of the f5 items (29 animals, 6 elements, 8 Greek letters).

Pre-set (Dan 30 Oct, before the run):
- an atom that is both a bridge atom and an answer atom (answer value in any language, atoms_multilingual.numbers_of) goes to the separate
  class "both", never to either;
- f5 is redrawn only if the bridge share (energy share of the old + new bridge classes) changes by more than 0.05 on any model.

Per model (f5 items, both views PM / PP; 50 items each): bridge share old (English) vs new (any language) with 95% cluster-bootstrap
intervals over the bridge entity, the "both" share, the sign split (old bridge -, new bridge +), the 5 largest newly classed atoms.

uv run python scripts/bridge_multilingual.py        # writes results/bridge_multilingual/<UTC>/ (manifest first)
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
from scripts import atoms_multilingual as M  # noqa: E402

EXP = "bridge_multilingual"
THRESHOLD = 0.05
LANGS = (
    "Chinese",
    "Japanese",
    "Korean",
    "Russian",
    "Ukrainian",
    "German",
    "French",
    "Spanish",
    "Portuguese",
    "Italian",
)
# entity -> forms per language, in LANGS order (variants split by "/"); the Greek letters also carry Greek names and symbols below
_ROWS = {
    "ant": "蚂蚁/蚁|アリ/蟻|개미|муравей|мураха/мурашка|Ameise|fourmi|hormiga|formiga|formica",
    "bee": "蜜蜂/蜂|ミツバチ/ハチ/蜂|꿀벌/벌|пчела|бджола|Biene|abeille|abeja|abelha|ape",
    "beetle": "甲虫/甲壳虫|カブトムシ/甲虫|딱정벌레|жук|жук|Käfer|scarabée/coléoptère|escarabajo/coleóptero|besouro/escaravelho|scarabeo/coleottero",
    "butterfly": "蝴蝶|チョウ/蝶/蝶々|나비|бабочка|метелик|Schmetterling|papillon|mariposa|borboleta|farfalla",
    "camel": "骆驼|ラクダ/駱駝|낙타|верблюд|верблюд|Kamel|chameau|camello/camel|camelo|cammello",
    "cat": "猫|ネコ/猫|고양이|кошка/кот|кішка/кіт|Katze|chat|gato|gato|gatto",
    "chicken": "鸡/小鸡|ニワトリ/鶏|닭/치킨|курица/цыплёнок|курка/курча|Huhn/Hühnchen|poulet/poule|pollo/gallina|frango/galinha|pollo/gallina",
    "cow": "奶牛/母牛|ウシ/牛|젖소/소|корова|корова|Kuh|vache|vaca|vaca|mucca",
    "crow": "乌鸦|カラス/烏|까마귀|ворона|ворона|Krähe/Rabe|corbeau/corneille|cuervo|corvo|corvo/cornacchia",
    "dog": "狗/犬|イヌ/犬|개/강아지|собака/пёс|собака/пес|Hund|chien|perro|cachorro/cão|cane",
    "duck": "鸭/鸭子|アヒル/鴨|오리|утка|качка|Ente|canard|pato|pato|anatra",
    "eagle": "鹰/老鹰|ワシ/鷲|독수리|орёл/орел|орел|Adler|aigle|águila|águia|aquila",
    "elephant": "大象/象|ゾウ/象|코끼리|слон|слон|Elefant|éléphant|elefante|elefante|elefante",
    "fly": "苍蝇|ハエ/蝿|파리|муха|муха|Fliege|mouche|mosca|mosca|mosca",
    "fox": "狐狸/狐|キツネ/狐|여우|лиса/лис|лисиця/лис|Fuchs|renard|zorro|raposa|volpe",
    "frog": "青蛙/蛙|カエル/蛙|개구리|лягушка|жаба/жаба|Frosch|grenouille|rana|sapo/rã|rana",
    "goose": "鹅|ガチョウ/鵞鳥|거위|гусь|гуска|Gans|oie|ganso|ganso|oca",
    "horse": "马|ウマ/馬|말|лошадь/конь|кінь/кобила|Pferd|cheval|caballo|cavalo|cavallo",
    "lion": "狮子/狮|ライオン/獅子|사자|лев|лев|Löwe|lion|león|leão|leone",
    "mouse": "老鼠/鼠|ネズミ/鼠|쥐|мышь|миша|Maus|souris|ratón|rato|topo",
    "owl": "猫头鹰|フクロウ/梟|올빼미/부엉이|сова|сова|Eule|hibou/chouette|búho/lechuza|coruja|gufo/civetta",
    "pig": "猪|ブタ/豚|돼지|свинья|свиня|Schwein|cochon/porc|cerdo|porco|maiale/porco",
    "rabbit": "兔子/兔|ウサギ/兎|토끼|кролик|кролик|Kaninchen|lapin|conejo|coelho|coniglio",
    "sheep": "绵羊/羊|ヒツジ/羊|양|овца|вівця|Schaf|mouton|oveja|ovelha|pecora",
    "spider": "蜘蛛|クモ/蜘蛛|거미|паук|павук|Spinne|araignée|araña|aranha|ragno",
    "tick": "蜱/扁虱|ダニ|진드기|клещ|кліщ|Zecke|tique|garrapata|carrapato|zecca",
    "tiger": "老虎/虎|トラ/虎|호랑이|тигр|тигр|Tiger|tigre|tigre|tigre|tigre",
    "turkey": "火鸡|シチメンチョウ/七面鳥|칠면조|индейка|індик|Truthahn/Pute|dinde|pavo|peru|tacchino",
    "wolf": "狼|オオカミ/狼|늑대|волк|вовк|Wolf|loup|lobo|lobo|lupo",
    "carbon": "碳|炭素|탄소|углерод|вуглець|Kohlenstoff|carbone|carbono|carbono|carbonio",
    "helium": "氦|ヘリウム|헬륨|гелий|гелій|Helium|hélium|helio|hélio|elio",
    "hydrogen": "氢|水素|수소|водород|водень|Wasserstoff|hydrogène|hidrógeno|hidrogênio|idrogeno",
    "lithium": "锂|リチウム|리튬|литий|літій|Lithium|lithium|litio|lítio|litio",
    "nitrogen": "氮|窒素|질소|азот|азот|Stickstoff|azote|nitrógeno|nitrogênio|azoto",
    "oxygen": "氧|酸素|산소|кислород|кисень|Sauerstoff|oxygène|oxígeno|oxigênio|ossigeno",
    "alpha": "阿尔法|アルファ|알파|альфа|альфа|Alpha|alpha|alfa|alfa|alfa",
    "beta": "贝塔|ベータ|베타|бета|бета|Beta|bêta/beta|beta|beta|beta",
    "gamma": "伽马/伽玛|ガンマ|감마|гамма|гамма|Gamma|gamma|gamma|gama|gamma",
    "delta": "德尔塔|デルタ|델타|дельта|дельта|Delta|delta|delta|delta|delta",
    "epsilon": "艾普西龙|イプシロン|엡실론|эпсилон|епсилон|Epsilon|epsilon|épsilon|épsilon|epsilon",
    "eta": "艾塔|イータ|에타|эта|ета|Eta|êta/eta|eta|eta|eta",
    "iota": "约塔|イオタ|요타|йота|йота|Iota|iota|iota|iota|iota",
    "theta": "西塔|シータ|세타|тета|тета|Theta|thêta/theta|theta/zeta|teta|theta/teta",
}
GREEK = {"alpha": ("άλφα", "α", "Α"), "beta": ("βήτα", "β", "Β"), "gamma": ("γάμμα", "γ", "Γ"), "delta": ("δέλτα", "δ", "Δ"),
         "epsilon": ("έψιλον", "ε", "Ε"), "eta": ("ήτα", "η", "Η"), "iota": ("γιώτα", "ι", "Ι"), "theta": ("θήτα", "θ", "Θ")}  # fmt: skip
SYMBOLS = {"helium": ("He",), "lithium": ("Li",)}  # case-sensitive; weak (an English pronoun, a surname)
WEAK_FORMS = {
    "chat",
    "ape",
    "cane",
    "pute",
    "rana",
    "tiger",
    "wolf",
    "lion",
    "fly",
}  # words that are also English / the same in English


def build() -> tuple[dict[str, dict[str, set[str]]], dict[str, set[str]]]:
    """entity -> {language: folded forms}; entity -> case-sensitive symbols."""
    forms: dict[str, dict[str, set[str]]] = {}
    for ent, row in _ROWS.items():
        cells = row.split("|")
        assert len(cells) == len(LANGS), ent
        forms[ent] = {
            lang: {M.normalise(f).casefold() for f in cell.split("/") if f}
            for lang, cell in zip(LANGS, cells, strict=True)
        }
    for ent, (name, lower, upper) in GREEK.items():
        forms[ent]["Greek"] = {M.normalise(x).casefold() for x in (name, lower, upper)}
    return forms, {e: set(s) for e, s in SYMBOLS.items()}


FORMS, SYMS = build()


def bridge_match(token: str, entity: str) -> tuple[str, bool] | None:
    """(language or 'symbol', weak) if the token is a translation / symbol form of the entity, else None."""
    s = M.normalise(token)
    low = s.casefold()
    for lang, fs in FORMS[entity].items():
        if low in fs:
            return (lang, low in WEAK_FORMS)
    if s in SYMS.get(entity, ()):
        return ("symbol (chemical)", True)
    return None


def record(rec: dict, answers: tuple[int, int]) -> dict:
    atoms, total = [], sum(a["share"] for a in rec["atoms"])
    ent, cf = rec["entity"], rec["cf_entity"]
    for a in rec["atoms"]:
        old = a["class"] if a["class"] in ("bridge", "new_bridge") else None
        new, lang, weak = old, ("English rules" if old else None), False
        if old is None:
            for cls, e in (("bridge", ent), ("new_bridge", cf)):
                if (m := bridge_match(a["token"], e)) is not None:
                    new, (lang, weak) = cls, m
                    break
        nums = M.numbers_of(a["token"])
        answer = any(v in answers for v, _, _ in nums)
        cls = "both" if new and answer else new or ("answer_any" if answer else "number_other" if nums else a["class"])
        atoms.append(
            {
                **a,
                "old_bridge_class": old,
                "bridge_class": new,
                "final_class": cls,
                "form_language": lang,
                "weak": weak,
                "numbers": nums,
            }
        )

    def e(pred) -> float:
        return sum(a["share"] for a in atoms if pred(a)) / total

    out = {
        "scene": rec["key"], "entity": ent, "atoms": atoms,
        "old": e(lambda a: a["old_bridge_class"] is not None), "new": e(lambda a: a["bridge_class"] is not None and a["final_class"] != "both"),
        "both": e(lambda a: a["final_class"] == "both"),
        "old_bridge": e(lambda a: a["old_bridge_class"] == "bridge"), "old_new_bridge": e(lambda a: a["old_bridge_class"] == "new_bridge"),
        "new_bridge_word": e(lambda a: a["final_class"] == "bridge"), "new_new_bridge": e(lambda a: a["final_class"] == "new_bridge"),
        # the expected signs: the old bridge word enters with -, the new one with + (the change adds the new word and removes the old)
        "old_sign_ok": e(lambda a: a["old_bridge_class"] == "bridge" and a["coef"] < 0) + e(lambda a: a["old_bridge_class"] == "new_bridge" and a["coef"] > 0),
        "new_sign_ok": e(lambda a: a["final_class"] == "bridge" and a["coef"] < 0) + e(lambda a: a["final_class"] == "new_bridge" and a["coef"] > 0),
    }  # fmt: skip
    return out


def summarise(recs: list[dict]) -> dict:
    ents = [r["entity"] for r in recs]
    s = {k: M.interval([r[k] for r in recs], ents) for k in ("old", "new", "both", "old_bridge", "old_new_bridge", "new_bridge_word", "new_new_bridge", "old_sign_ok", "new_sign_ok")}  # fmt: skip
    s["n"] = len(recs)
    s["change"] = M.interval([r["new"] - r["old"] for r in recs], ents)
    return s


def newly_classed(recs: list[dict], view: str, k: int = 5) -> list[dict]:
    rows = []
    for r in recs:
        for a in r["atoms"]:
            if (a["old_bridge_class"] is None and a["bridge_class"] is not None) or (
                a["final_class"] == "both" and a["old_bridge_class"] is None
            ):
                rows.append({"scene": r["scene"], "view": view, "token": a["token"], "class": a["final_class"], "bridge_class": a["bridge_class"], "form_language": a["form_language"],
                             "weak": a["weak"], "sign": "+" if a["coef"] > 0 else "-", "coef": a["coef"], "energy_share": a["share"], "old_class": a["class"], "numbers": a["numbers"]})  # fmt: skip
    return sorted(rows, key=lambda x: -x["energy_share"])[:k]


def main() -> Path:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = REPO / "results" / EXP / stamp
    out.mkdir(parents=True, exist_ok=False)
    manifest = {"exp": EXP, "written_utc": stamp, "script": "scripts/bridge_multilingual.py", "post_hoc": True, "cpu": True,
                "inputs": [f"results/x52_atoms/{r}/labelled.jsonl" for r in M.REPORTS], "languages": [*LANGS, "Greek", "symbols"],
                "pre_set": {"both": "an atom that matches the bridge class (old or new, any language) and the answer class (any language) goes to 'both', never to either",
                            "redraw_f5": f"only if the bridge share (old + new bridge energy share) changes by more than {THRESHOLD} on any model"},
                "bridge_share": "energy share (sum of atom shares / the item's total) of the old + new bridge classes; old = the saved English rules, new = those plus the translation / symbol forms",
                "entities": sorted(FORMS), "weak_forms": sorted(WEAK_FORMS), "git": __import__("subprocess").run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()}  # fmt: skip
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))  # before the numbers
    lab = M.labelled()
    tables: dict = {"models": {}}
    for model in M.MODELS:
        ans = M.answers_of(model)
        per_view, allrecs, newly = {}, [], []
        for view in M.VIEWS:
            scenes = sorted(s for (m, v, s) in lab if m == model and v == view)
            recs = [record(lab[(model, view, s)], ans[s][view]) for s in scenes]
            per_view[view] = summarise(recs)
            allrecs += recs
            newly += newly_classed(recs, view, 50)
        pooled = summarise(
            allrecs
        )  # both views: the same 50 scenes twice; the cluster bootstrap is over the bridge entity
        newly.sort(key=lambda x: -x["energy_share"])
        tables["models"][model] = {"pooled": pooled, "views": per_view, "largest_newly_classed": newly[:5],
                                   "n_newly_classed_atoms": len(newly), "languages_of_new_atoms": {lang: sum(1 for x in newly if x["form_language"] == lang) for lang in sorted({x["form_language"] for x in newly})}}  # fmt: skip
    changes = {
        f"{m}|{v}": abs(d[v]["new"][0] - d[v]["old"][0])
        for m, d0 in tables["models"].items()
        for d in [d0["views"]]
        for v in d
    }
    tables["max_abs_change"] = round(max(changes.values()), 4)
    tables["redraw_f5"] = bool(tables["max_abs_change"] > THRESHOLD)
    tables["changes_by_model_view"] = {k: round(v, 4) for k, v in changes.items()}
    (out / "tables.json").write_text(json.dumps(tables, indent=1, ensure_ascii=False, default=float))
    lines = [
        "# Bridge classes in any language (30 Oct; post hoc; CPU, saved atoms)\n",
        f"Max |change| of the bridge share (old + new bridge): {tables['max_abs_change']} (bar {THRESHOLD}): redraw f5 = {tables['redraw_f5']}\n",
    ]
    for model, t in tables["models"].items():
        p = t["pooled"]
        lines.append(f"## {model}: {t['n_newly_classed_atoms']} newly classed atoms {t['languages_of_new_atoms']}\n")
        lines.append(
            "| view | bridge share old (English) | new (any language) | both | change | sign-correct share old | new |\n|---|---|---|---|---|---|---|"
        )
        for name, s in (("PM", t["views"]["PM"]), ("PP", t["views"]["PP"]), ("pooled", p)):

            def iv(k, s=s):
                return f"{s[k][0]:.4f} [{s[k][1]:.4f}, {s[k][2]:.4f}]"

            lines.append(
                f"| {name} | {iv('old')} | {iv('new')} | {iv('both')} | {iv('change')} | {iv('old_sign_ok')} | {iv('new_sign_ok')} |"
            )
        lines.append("\nLargest newly classed atoms: " + "; ".join(f"{x['token']!r} {x['class']} ({x['form_language']}{', weak' if x['weak'] else ''}) {x['sign']} {x['energy_share']:.4f} {x['scene']}/{x['view']}" for x in t["largest_newly_classed"]) + "\n")  # fmt: skip
    (out / "tables.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out.relative_to(REPO)}")
    return out


if __name__ == "__main__":
    main()
