# Figure style: one palette, one grammar (Dan, 30 Oct)

Every figure in the root README, `docs/depth/README.md` and `docs/breadth/README.md` follows the rules below. The palette
and the model order live in one place, [`src/bridge_jspace/palette.py`](../../src/bridge_jspace/palette.py); the figure
kit ([`figkit/`](../../src/bridge_jspace/figkit/)), the depth story figures (`scripts/story_style.py`) and the audit
(`scripts/check_style.py`, `make readme`) all read it. Change a colour there, nowhere else.

## The logic

A colour names **what is drawn**, never a model, a panel or a figure. A reader learns five roles and reads every figure
with them; grey is everything secondary.

| role | colour | means |
|---|---|---|
| recall | black `#2B2B2B` | the recall reader and what it needs |
| lookup | purple `#6B5BD2` | the lookup reader (light `#B8B0EA`: made-up facts; dark `#3F3489`: question after the scene) |
| lens part | teal `#1A9E8A` | the lens part: the J++ part, the lens's directions |
| address | orange `#E08A1E` | the address, and the position route |
| identity | blue `#3A7DC9` | the identity route, and an item change |
| control | grey `#A8A8A8` | a control or baseline: a random part, a rotated part, a layout-only probe, a random vector. Grey only; never a role |
| other | light grey `#D9D9D9` | the rest of a stack |
| neutral | slate `#4A5F6A` | a method or quantity that is none of the roles (a supervised probe's subspace, the value) |
| positions | brown `#8C6D46`, pink `#B8689A` | the bridge's mention and the question, as places in the prompt |
| answer word | brick `#B8433A` | the answer word in the lens-readout figures |

Rules that go with the colours:

1. **One mark: the dot** (bars only for 100% stacks). A thin whisker in the same colour is the 95% interval; a grey
   connector joins two dots of one row. The only other mark is a hollow dot, **○ = post hoc** (a gate or rule set after the
   results were seen) and nothing else. Every figure that has one says so in its key.
2. **No red and green together** carry information. Rules and bars are grey, dashed; never red.
3. **A figure is a table**: models are rows (bold, left), measurements are columns; one model order everywhere: Qwen 9B,
   Qwen 27B, Muse 30B, Lightning, Qwen 122B, then the breadth-only models (DeepSeek, Ministral, Bolt, OLMo).
4. **Three text levels**: bold ink (titles, row labels, headline numbers), ink (values), grey (units, controls, notes). All
   text horizontal. A panel header names the quantity, never the claim; the claim is the sentence above the figure.
5. **Every panel has an x-axis title with the unit** ("points", "share", "accuracy"); every mark and colour is named by a
   coloured word above the first row or by the key row under the axes (no legend box).
6. **A missing cell says why, in the cell**, in grey ("no run", "below gate", "too few switches"), never a bare dash
   (Dan 30 Oct). No title or footnote inside a README image; one figure-wide subtitle line is allowed when a row or dot
   needs defining (r4, f8), and each axis has a grey direction cue under its title (which way is "more").
7. **Controls are grey and smaller** and named in the key ("the largest same-size control", "a random part",
   "a random vector").

## What checks it

- `figkit/lint.py` (every table figure, at build): rotated or overlapping text, text off the figure, a legend box, a marker
  other than "o", hatch, a mark colour outside the palette, a hollow mark without "post hoc", a bar segment that nothing
  names, a panel without an x-axis title.
- `scripts/check_style.py` (every PNG a README shows): the saturated pixels must lie on a palette colour or its tint.
  `make readme` prints the report; `tests/test_check_style.py` fails the root and depth READMEs on a figure off the palette.

## Where it stands (30 Oct)

- Root and depth READMEs: every figure is on the palette except `figures/breadth/fig10_beyond.png` (linked from the root
  README) and the supplementary `fig10b_enrichment`, `fig10d_heads` (brick red was a mark of its own; now the answer shade).
- Breadth README: the eleven figures (`figures/breadth/fig00` to `fig11`) are Zach's own style (blue `#184898`, green,
  vermilion, shape-coded models). They are pre-rendered images, not built here; redrawing them in the table style from
  `docs/breadth/data.csv` is the open step (`python scripts/check_style.py --report` lists them).
