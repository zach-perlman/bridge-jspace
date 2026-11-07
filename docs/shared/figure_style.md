# Figure style v2: one visual grammar for every figure (Dan, 7 Nov)

Every figure of both tracks (the write-up's `figures/writeup/`, the root README's `figures/readme/`, the depth README's
`figures/depth/`, `figures/shared/` and the breadth README's `figures/breadth/`) follows these rules. They replace v1
(30 Oct). The single sources are:

- [`src/bridge_jspace/palette.py`](../../src/bridge_jspace/palette.py): the role colours, the model order.
- [`src/bridge_jspace/figkit/terms.py`](../../src/bridge_jspace/figkit/terms.py): every word a figure may print (labels,
  units, cues, key phrases, missing-cell words).
- [`data/figures/status.csv`](../../data/figures/status.csv): the status of every drawn cell (fixed in advance, post hoc,
  descriptive, not claimed).

Change a colour, a word or a status there, nowhere else. The checks below test meaning (a colour means one role, a
hollow mark means post hoc), not only membership. Frozen, never regenerated: `figures/slides/` (the deck of 30 Oct is a
record), `figures/archive/`, `figures/pre-sprint/`.

## A. Colour = role. One hue per role; a shade never encodes a variable

| role | colour | used for |
|---|---|---|
| recall | black `#2B2B2B` | the recall reader, and what it loses |
| lookup | purple `#6B5BD2` | the lookup reader, only |
| lens part | teal `#1A9E8A` | the lens part (any J++ directions read at a word, the city's included) |
| address | orange `#E08A1E` | the address and the position route; anything measured under an address swap |
| identity | blue `#3A7DC9` | the identity route; a change of item |
| answer | brick `#B8433A` | the answer span, the answers' own directions, the answer word |
| neutral | slate `#4A5F6A` | a method that is none of the roles (a supervised probe's subspace, a data-built subspace) |
| mention / question | brown `#8C6D46` / pink `#B8689A` | only where rows or columns are places in the prompt |
| control | grey `#A8A8A8` | a control or baseline, and nothing else |
| other | light grey `#D9D9D9` | the remainder of a 100% stack; chrome |

- No lighter or darker shade of a role. A second condition of the same reader gets its own column or sub-row, named in
  words, in the same role colour (sentence order: "locker sentence first" / "locker sentence after", both purple).
- A mark that is not a reader takes the colour of the intervention whose effect is drawn (pairs reached, attention
  under an address swap: orange).

## B. Status is never a colour

- **○ hollow = post hoc**, and nothing else.
- **descriptive**: the role colour, plus the grey tag "descriptive" in the cell.
- **not claimed**: the role colour, plus the grey tag "not claimed: <reason>".
- **missing cell**: grey words from a fixed list only: "no run", "no comparable run", "below gate", "too few switches",
  "no interval".

Every drawn cell's status is a row of `data/figures/status.csv` (figure, cell, status, reason, source). Figures read it;
a test fails when a hollow mark is not `post_hoc` there, or the reverse.

## C. Marks

- **The dot** is an estimate; a same-colour whisker is its 95% interval; a grey connector joins dots of one row.
- **Bars** only for 100% stacks. Counts are dots, printed "18 of 30".
- **Lines** only when x is depth; cells fixed in advance are filled dots on the line.
- **The largest same-size control** is a grey tick on the estimate's own axis, never a number in parentheses.
- **Reference lines** are dashed grey with canonical labels ("bar fixed in advance: 15", "chance"). The light-grey band
  at zero is always "within 0.10 of a random part".

## D. Layout

- **Models are rows**, in `palette.MODELS` order (then DeepSeek, Ministral, Bolt, OLMo). **Conditions are columns.**
- Two tests on two datasets stay in two panels with their own x-axis titles and units, never a shared axis.
- Small multiples (only where one table cannot hold the dots) stack in model order with shared x-axes.
- A panel header names the quantity, never the claim.

## E. Keys: every encoding named in the figure

1. Every role colour in a panel is named by a coloured word above the first row.
2. One key line under the axes, in this order, with these phrases, listing only what the figure uses: "grey: <which
   control>", "grey tick: the largest same-size control", "○ post hoc", "whiskers: 95% interval", "grey band: within
   0.10 of a random part".
3. Nothing drawn is unnamed; nothing named is undrawn. No legend boxes.

## F. Words

A figure prints only a term from `terms.py`, a number, a canonical model name, or prompt text in a schematic.

- **Units**: each x-axis title names the unit and the denominator: "accuracy (%)", "accuracy drop (points)", "gap:
  recall − lookup (points)", "share of switches", "share of lookups", "share of the rebuilt energy", "× the full damage",
  "z against 200 random vectors".
- **Direction cues**: under every x-axis exactly "→ more <the axis quantity>", always pointing right. Cues describe the
  axis; claims stay in the post.
- **Canonical terms**: lens part (not J++ part, J-part); knock-out (band) / removed from the patch (one layer) (not taken
  out, KO, ablated); swapped in, the whole change, a change of item (not item change, donor, patch alone); another
  entity (not D, donor); switches blocked beyond random; gap: recall − lookup (not M − K); address, identity, position,
  the number (not slot, ALF, value route); answer span, answer span kept, answer span removed; rotated, logit lens, PCA,
  a random part, energy-matched random, a random vector, layout-only probe, 10 random heads; fixed in advance (not
  registered); post hoc, descriptive, not claimed; points (not pts); Qwen 9B, Qwen 27B, Muse 30B, Lightning, Qwen 122B,
  DeepSeek, Ministral, Bolt, OLMo.
- No people's names, note numbers, run ids or set codes in any figure.

## G. Numbers: one precision per unit, everywhere

| unit | format |
|---|---|
| accuracy | % integer |
| points (drops, gaps, differences) | one decimal |
| shares | two decimals |
| × damage | two decimals |
| z | integer |
| counts | "18 of 30" |

Intervals at the value's precision, as "[lo, hi]". The same data key prints the same string in every figure.

## H. Type and size

1600 px at 200 dpi, width to height 1.0 to 2.6, three text levels (bold ink, ink, grey), nothing under 11 pt at 720 px,
white background, no title inside an image. Font sizes per text level come from `figkit/theme.py` only.

## I. The key figure

`figures/writeup/key.png` shows the whole grammar on one image (each role colour with its meaning, grey = control, ○ =
post hoc, the whisker, the grey band, the grey tick, the missing-cell words, one example row read aloud), for the post's
"How to read the numbers".

## What checks it

1. Role tags: every mark is drawn through a figkit call with a role tag; its colour equals `ROLE[tag]`.
2. One meaning per colour: a role colour appears only on marks tagged with that role.
3. Status registry ↔ marks: hollow ↔ `post_hoc`; "descriptive" and "not claimed" tags ↔ the registry.
4. Key completeness: every encoding drawn is named, nothing named is undrawn.
5. Terms: every text is a canonical term, a number, a model name or schematic prompt text.
6. Cues: every cue matches `^→ more `.
7. Number format by unit, and the same key prints the same string across figures.
8. Colour vision: under simulated deuteranopia, protanopia and tritanopia, CIEDE2000 ≥ 12 between two role colours in
   one figure and ≥ 8 between a role colour and control grey.
9. Grayscale: `contact_sheet_gray.png` beside the colour sheet; every figure reads through words and marks.
10. The v1 checks still run: text crossings (`figkit/lint.py`), `scripts/check_style.py`, `scripts/check_figure_terms.py`.

`docs/shared/figure_audit.md` lists every figure in scope against these rules.
