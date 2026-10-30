# Natural-text task sets (Zach, 2026-10-23)

> **Status (2026-10-24):** for new work use the combined suite `jsuite_v2_1_*` (docs/archive/jsuite_v2.md, amendment 35). The
> combined suite v1 (`jsuite_v1_*`) is retired and the sets below are kept frozen for the results that cite them.

Two- and three-hop questions over passages, built from real facts, in the tasks_v2 item format. A word names the
source of each hop in order: **P** read from the passage, **M** recalled from memory. Example (natplus, countries):
the passage binds "Paul Whitaker was raised in Argentina"; **PM** asks "Which continent is the country where Paul
Whitaker was raised on?" (Argentina from the passage, South America from memory); **PP** asks where Argentina's
delegation meets next, a made-up fact stated in the same passage (Asia). Each set directory holds `items.jsonl` and
`manifest.json` (seed, generator commit). Pre-registration: docs/prereg_replication_1022.md, amendments 10B-20.
Results: EXPERIMENTS.md.

## The sets

| Set | Generator (seed) | Words | Items | What it adds |
|---|---|---|---|---|
| natural_v1_chat, natural_v2_chat, natural_v3_chat | scripts/natural_v1.py (801, 802, 803) | PP PM MP MM | 1,296 each | Real facts (country -> continent, person -> nationality, city -> country; 81 bridges), fictional-person passages, chat framing, the bridge absent from MM passages |
| natural_v1_qa | natural_v1.py derive-qa | PP PM MP MM | 1,296 | natural_v1 in raw text, two-shot "Question: / Answer:" |
| natural_v*_cloze | natural_v1.py | | | Plain cloze; models answer " the" / ":", dropped |
| natplus_v1_chat | scripts/natplus.py (901) | PP PM MP MM | 2,336 | Adds 47 rare bridges (popularity field), animal -> class, three wordings per fact and question, facts spliced into runs of consecutive WikiText sentences |
| natplus_v2_chat, natplus_v3_chat | natplus.py (903, 904) | PP PM MP MM | 2,336 each | Rendering seeds: the same facts, new passages and wordings |
| natplus_dev_chat | natplus.py (902) | PP PM MP MM | 1,168 | Band sweeps only (shares facts with v1-v3, see caveats) |
| natctl_v1_chat | scripts/natctl.py (1201) | PP PK PM PA MP MK MM MA | 2,048 | Final-hop controls on one shared scene: P new fact, K the true fact stated in the passage, M recall with the answer word absent, A recall with the answer word present once as another entity's value |
| nat3_v1_chat | scripts/natural3.py (1101) | all 8 three-hop words | 1,792 | Cities and people -> country -> continent |

Item fields used downstream: `word`, `context`, `question`, `answer`, `kind` ("open"), `framing`, `steps` (per hop:
`question`, `answer`, `source`, hop 1's `alts` = every name for the bridge, per-step `cand_vocab` in nat3),
`bridge`, `answer_vocab` (the relation's answers), `domain`, `popularity`, `scene`, `level`, `guess_question`,
`answer_in_passage`.

## Running them

Rendering is scripts/tasks_v2.py `render()` (chat: one user turn, thinking off, "Answer with just the answer,
nothing else."; qa: the two-shot preamble). Always use the **cand2** read (amendment 20): an answer is right if its
first token tops the relation's candidate answers (either case; at hop 1 any of the bridge's names).

```
BJ_TARGET=qwen3.6-27b python scripts/natural_v1.py competence --set natplus_v1_chat --name natplus_v1_chat_competence_cand2_v1 --read cand2 --why "..."
BJ_TARGET=qwen3.6-27b python scripts/ablate_v2.py --name natplus_v1_chat_ko_cand2_v1 --why "..." --plan bands --bands 32-40 \
  --conditions paper10 paper10_rot unembed10 unembed10_rot --tasks natplus_v1_chat --tasks-competence natplus_v1_chat_competence_cand2_v1 \
  --tasks-words PP PM MP MM --tasks-level all --n 1000 --kinds clean --batch 32 --read cand2
python scripts/c1_v2.py RUN --middle L32-40 --set natplus_v1_chat     # the C1 rule
python scripts/natplus_split.py RUN --set natplus_v1_chat            # by popularity and relation, bootstrap over bridges
python scripts/natctl_score.py RUN                                   # natctl: K-M, A-M, P-K, P-M
python scripts/nat3_score.py RUN --drop "South Africa"               # nat3 (add --tasks-per-word to ablate_v2)
python scripts/gen_spot.py ...                                       # what the model actually says under an edit
```

scripts/queues/h200_fix_1023.sh chains these per model (competence, knock-out, scoring).

## Caveats (from the 2026-10-23 review, amendment 20)

- **Use cand2, not cand.** cand missed natplus's rare people's first names at hop 1 (most rare-person scenes starting
  from memory were never eligible) and compared only capitalised answers (animals' prompt-final answers are lowercase).
  Runs named `*_cand_v1` on natplus, natctl and nat3 have that problem; `*_cand2_v1` do not.
- **natplus_dev is not held out:** dev and v1-v3 render the same chains (bridges, facts, hop-1 descriptions). A
  band chosen on dev is chosen on the test facts. v1-v3 are rendering seeds of one fact set; the intervals over
  bridges carry the fact sampling.
- **PM has a lure:** PM shares PP's passage, which gives the bridge a made-up value from the same answer list (a
  different relation). MM passages never name the bridge. MM - MP is the lure-free gap.
- **The answer word is often present:** about 30% of memory-final passages in natplus (38-42% in natural_v1) contain
  the answer as another entity's value, which understates memory-final losses. natctl's M words have none.
- **First-token reads:** answers outside the candidate list map onto a candidate ("North Africa" scores as North
  America, "Swiss" as Swedish). Hop-1 bridge candidates share first tokens (Mozart / Mendeleev / Miguel: "M"), so the
  hop-1 eligibility check is lenient. gen_spot shows the full replies.
- **nat3:** chains through South Africa leak the answer Africa (drop them with `--drop`); only the 27B composes
  three-hop chains (the 9B and Muse are at chance).
- **Wording oddities:** "Which continent is the country where ... was raised on?" (memory-final words only); "a owl".
