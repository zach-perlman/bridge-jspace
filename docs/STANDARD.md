# Research repo docs standard, v1 (8 Nov 2026)

One structure for every research repo Dan publishes, so a newcomer finds the same things in the same places.
Applies to `danorel/mats.secret-elicitation-audit` (single track) and `zach-perlman/bridge-jspace` (two tracks), and to
later projects.

The model is bridge-jspace's root README after the readability pass (`42698e30`): it meets every target below. The
rules come from that pass, from the MATS rubric, and from how a skeptical LessWrong reader checks a claim
(a LessWrong-critic review of this repo and the ELK repo (8 Nov 2026)).

## 1. Three readers

Every document serves one of three readers. Write for that reader only.

| Reader | Arrives from | Wants, in order | Reads |
|---|---|---|---|
| **The 3-minute reader** | the post, a link, a tweet | what is claimed, how strong it is, one picture | README top: title, status, TL;DR, hero figure |
| **The skeptic** | a claim they doubt | the test, the controls, what was chosen after the data, raw examples, what failed | README findings and their folds, the ledger, the hypotheses, the examples |
| **The re-runner** | wants to build on it | how to rebuild figures, numbers and runs; cost; licence | README "Reproduce", DEVELOPER.md |

Agents are a fourth reader. Their file (`AGENTS.md`) is never on a reader's path.

## 2. The document set

Each role has one file. Same names in every repo.

| Role | Single-track repo | Multi-track repo | Required |
|---|---|---|---|
| Front door, the source of truth | `README.md` | `README.md` | yes |
| Track report (same skeleton as the README) | none | `docs/<track>/README.md` | multi-track |
| Ledger: one card per test | `EXPERIMENTS.md` | `docs/<track>/EXPERIMENTS.md` | yes (a track report may double as its ledger if it says so) |
| Hypotheses: every committed prediction and its verdict | a README section | `docs/plans/hypotheses.md` | the section always; the file when there are more than 5 predictions |
| Examples: real items, picked by a fixed rule | `docs/examples.md` | `docs/writeup/examples.md` | yes |
| Figure index, one per figure set | `figures/<set>/README.md` | `figures/<track>/<set>/README.md` | yes |
| Map of `docs/` | none (the README's Repository guide is enough) | `docs/README.md` | when `docs/` has more than 5 files |
| How to run, rebuild and publish | `DEVELOPER.md` | `DEVELOPER.md` | yes |
| Rules for coding agents | `AGENTS.md`, plus `CLAUDE.md` containing only `@AGENTS.md` | same | yes |
| This standard, for maintainers | `docs/STANDARD.md` (identical copy in every repo) | same | yes |
| What a human recomputed | `VERIFIED.md` | `VERIFIED.md` | only if a human recomputed something |
| Changes to claims and numbers after release | `CHANGELOG.md` | `CHANGELOG.md` | yes, from the first release tag |
| Licence | `LICENSE` (code); third-party terms in the README | same | yes |
| How to cite | `CITATION.cff` | `CITATION.cff` | yes |
| Records kept for the audit trail | `log/` or `docs/archive/` | `docs/archive/`, `docs/review/` | optional; never linked from the README's main text |

**The root holds only:** README, EXPERIMENTS (single track), DEVELOPER, AGENTS, CLAUDE, CHANGELOG, VERIFIED (if any),
LICENSE, CITATION.cff, and build files. A comparison table that the write-up links (ELK's `METRICS.md`) may stay.
Sprint logs, status notes and run tables go to `docs/archive/`.

## 3. The README skeleton

Fixed section names, fixed order. Every section is required in the root README.

| # | Section | Content | Budget |
|---|---|---|---|
| 0 | Title | The main claim as a sentence. It must survive the findings below it. | one line |
| 0 | Subtitle | Italic: what was tested, on what. | one sentence |
| 0 | Byline | Authors in the agreed order · context (program, sprint or application) · dates. | one line |
| 0 | **Status.** | (a) the kind of work and effort; (b) the verification level, in the vocabulary of §8; (c) the one caveat that most limits the headline. | ≤ 3 sentences |
| 0 | Links row | Write-up · Ledger (in a multi-track repo: one link per track report) · Hypotheses · Examples · Figures · Data · Reproduce · Code licence · Data licence. Same labels, same order. Drop an entry that does not exist; never a dead link. | one line |
| 1 | `## TL;DR` | One context paragraph that defines the 3–4 terms the bullets use. Then 3–4 claim bullets. Then one bullet "**For anyone …**": what a practitioner should do differently. Then the hero figure with its caption. | paragraph ≤ 80 words; bullets ≤ 40 words, one number or range each |
| 2 | `## Setup` | One illustrative example in prose. Real items, each picked by a fixed rule (the rule and item ids in a data file). `### Key terms` (≤ 10 bullets). One method picture: a diagram or a figure, not both. `### Reading the figures`: colour roles and marks, the key image folded. | |
| 3 | `## Findings` | `### Finding N. <claim sentence>` blocks (§4). Ends with an optional fold "Other results (ledger only)": one line and a link each. | ≤ 4 findings |
| 4 | `## What we predicted, and what happened` | One line per committed prediction: the guess in words → **verdict** → link to its ledger row. Predictions that failed stay. If no rule was fixed in advance for most tests, say so in one line. | one line each |
| 5 | `## Where it does not hold` | Bullets: settings, models or measures where the claim fails or weakens. Detail in one fold. | ≤ 1 number per bullet |
| 6 | `## How we checked` | Rules fixed in advance; reruns; recounts and who wrote them; what is not checked. Provenance in a fold. | |
| 7 | `## Related work and what is new` | **Not new.** · **New here.** · **Methods we build on.** Say when a result was expected from prior work. | |
| 8 | `## Open questions` | Each question with "Next:" and what it would take. A fold is fine. | |
| 9 | `## Reproduce` | Three tiers, each with commands, hardware, time and download size: figures from tracked numbers (CPU, no download); numbers from raw runs (CPU); the runs (GPU). | |
| 10 | `## Repository guide` | Where reports, ledger, figures, code, data and archives are. Licences and third-party terms. How to cite. | |

**Budgets for the root README:** ≤ 2,000 words outside `<details>`; ≤ 5,000 in total. A track report: ≤ 2,500 outside.

**Not sections:** "Summary" (it is the TL;DR), "Background" (it is Setup), "What we did" (Setup plus the findings'
Test lines), "More results" (the findings' last fold), "Why this matters" (the TL;DR's "For anyone" bullet).

**Track reports** use the same skeleton. Findings may be grouped into `## Part I. …` headings. Their TL;DR may be a
claims table (claim, grade, one column per model) under the bullets. Keep old anchors with `<a id="…"></a>` when a
heading is renamed, because posts and ledgers link to them.

## 4. The finding block

````markdown
### Finding N. <the claim, one sentence, no stronger than the fold supports>

<3–5 plain sentences. One number or range per sentence. The last sentence is the takeaway.
If a mundane explanation exists, name it here and say whether a control rules it out.>

![<alt: what the image shows, ≤ 25 words>](figures/<set>/<id>.png)

*<caption: takeaway first, then how the figure encodes it; ≤ 60 words>*

<details><summary>Test, results, controls and limits</summary>

- **Test.** What was run, on what, at which layer or position.
- **Result.** A table: rows are measures, columns are models or conditions. Numbers keep their source.
- **Controls.** Each control and its value, next to the effect.
- **Scope.** Where it was tested; where it was not.
- **Confidence.** Credence in % for the claim as stated, and what would change it. Set by the authors, never by an agent.
- **Limits.** What was chosen after the data (○), what is untested, known confounds.

<more figures, each with a caption>

</details>
````

No "In plain terms:" or "Takeaway." labels. No per-model slash lists ("0.50 / 0.74 / …") outside a fold.

## 5. The ledger

**Top of the ledger:** `## In one minute` (what it holds, in 3–6 bullets); one index table (test, data, result,
rule fixed in advance?, hand-checked?, where the README uses it); `## How to read`; then Parts in the README's order;
`## Scoped, not run`; `## Notes`.

**Each card:**

````markdown
### <the question>? <a id="<anchor>"></a>

`in README` | `ledger only` · *Used in: README <section>.*
Status: rule fixed in advance | post hoc | descriptive · hand-checked: yes / no · files: `<run ids or paths>` · recompute: `<command>`

- **Question.** - **Why we asked.** - **Data.** - **Method.**
![...](...)
*<caption>*
- **Rule, fixed in advance.** Quoted, or "Not recorded".
- **Result.** A table.
- **Read.** What the result says, nothing more.
- **Caveats.**
````

Dates and session names may stay in the card; clock times, people's initials and agent operations do not (they go to
`docs/review/` or `log/`).

## 6. Other files

- **Hypotheses.** Grouped by hypothesis, not by date. Each: the prediction verbatim, its source, the test that decided
  it, the verdict, the numbers. Verdict words from §8.
- **Examples page.** Generated by a script from a fixed seed or rule, with no filter on outcome, unless the page says
  which example was picked to show a typical case and how often that case occurs. Each example names its source file.
  What the model reads and what it answers, word for word. Items kept out of the public repo are described, not quoted.
- **Figure index.** One table per figure set: number, thumbnail, the caption's first sentence, status (post hoc cells,
  claimed or not). Generated, never hand-edited.
- **DEVELOPER.md.** Sections in this order: Layout · Setup · Reproduce (the README's three tiers, in detail) · Figures ·
  Running experiments · Checks · Writing results (a pointer to `docs/STANDARD.md` plus this repo's exceptions, if
  any) · Known issues in the numbers · Upstream (forks only).
- **AGENTS.md.** The project's state in two lines with links (README, hypotheses, VERIFIED). Roles. Environment.
  Rules for runs and for writing. No plans and no hypotheses that are not public.
- **CHANGELOG.md.** One file with versions (Keep a Changelog): `[Unreleased]`, one section per release tag, and the
  sprint as a pre-release version at the bottom. The version lives in the build file (`pyproject.toml`); the tag
  `vX.Y.Z` and `CITATION.cff` follow it. From the first release tag on, one entry per change to a claim, a number or
  a rule, newest first, with the tag or commit.
- **CITATION.cff.** Authors in the agreed order, title, repo URL, release tag, and the paper it builds on.
- **Licence section** in the README's Repository guide: what MIT covers; each third-party source with its terms; data
  derived from model weights keeps the model's licence.

## 7. Writing rules (each one checkable)

1. One idea per sentence, at most 30 words. Split at colons and semicolons.
2. Define a term before or at its first use, in plain words. One word per concept; aliases only in the glossary.
3. No notation the reader was not given: no hypothesis ids, batch ids, claim numbers or job names in prose. A label may
   appear only as link text to its ledger row.
4. Round in prose: two or three significant digits. Exact values belong in tables and data files.
5. Captions put the takeaway first, at most 60 words in a README. Every figure has a caption.
6. Say a thing once and link to it elsewhere.
7. Use "we" for joint work and "I" for single-author work; never mix. Section names follow ("How I checked").
8. US spelling.

## 8. Shared vocabulary

- **Marks.** ○ (hollow) = a gate, rule or choice set after the data were seen. † = not in the hand-checked sample.
  Nothing else.
- **Verdicts.** held · held in part · failed · withdrawn · not tested in the final design · not separable ·
  favored, not proven.
- **Verification levels** (the Status line names every level reached and the first level not reached):
  1. computed by code from tracked run files;
  2. checked by automated tests (sources resolve, numbers match);
  3. raw items read by hand (n, rule);
  4. recounted from the raw files by code written independently of the analysis (say whether a human or an agent
     wrote it);
  5. recomputed by a human (VERIFIED.md).
- **Confidence.** A credence in %, set by the authors.

## 9. What a skeptical reader must find (and the agent must never remove)

Each item must be visible without opening the code:

1. **What was chosen after the data**, marked ○ in text, tables and figures, and named in the sentence that states the
   headline if the headline depends on it.
2. **How the reported models, layers or items were selected.** "The three clearest of nine" is a selection by outcome;
   say so, or give the rule fixed in advance.
3. **The strongest mundane explanation** of each finding, in the finding's visible paragraph, with the control that
   rules it out or the admission that none does.
4. **Controls next to effects**: same size, same norm, random, base model, blank input. Say what each control is
   matched on (norm, energy, damage).
5. **The independent unit and the interval** (prompts, not items, when the evidence is fixed by the prompt).
6. **Raw examples** by a fixed rule, linked from the Setup.
7. **What failed**: the predictions that failed and the tests that dropped a reading.
8. **Who checked what** (§8 levels), including which checks were written by agents.
9. **What was expected from prior work**, so a confirmation is not sold as a discovery.

## 10. What stays out of reader paths

Ops logs and status notes; job queues and autonomy windows; batch, job and session ids in prose; clock times and
initials of decisions (keep "decided after seeing X"); agent instructions; private plans; application-process detail
beyond one effort line; duplicated text across README, track reports and ledger.

## 11. Checks

- `scripts/readme_lint.py` (one file, identical in every repo): words outside folds and in total; slash lists; sentences
  over 30 and 40 words; colons; caption mean and maximum; ledger labels. It reads paragraphs, so hard-wrapped and
  one-line paragraphs measure the same. A test holds the README to §3's budgets.
- Links and anchors resolve (README, track reports, ledger, docs map).
- Every number in a README or ledger traces to a tracked data file: rendered from a key (bridge) or carrying
  `<!-- src: <path> | <key> -->` with a test that the value matches (ELK).
- Render check: the README as GitHub renders it (`gh api /markdown -f mode=gfm -F text=@README.md`), looked at once
  per release.
