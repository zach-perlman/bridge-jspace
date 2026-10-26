# Draft: the pointer's "first" after 45a (Dan, 26 Oct ~21:40-21:45; merge on Tue after the 122B and the hand check)

Not merged. Each block names the place in docs/README.template.md (line numbers as of 7415c6f0) and the text that replaces it; every choice below is Dan's (~21:40) unless marked. Numbers: Q45.3's verdicts (results/x6_routes/*_x45a*/verdict-*) and the 45a descriptive table (results/x6_routes/x45a-descriptive-20261026T202952Z), after the data where marked. Drafts beside this file: docs/drafts/x0_details_45a.md (the table, for docs/x0_details.template.md) and figures/drafts/fig08b_layout.png with its data.csv rows in figures/drafts/fig08b_layout.csv (scripts/readme_story_figures.py f08b_layout; on Tue: add it to README_FIGS with draft=False). UNVERIFIED.

## 1. In one minute

Bullet 2 (line 9): "where it was first mentioned" becomes "where its locker sentence sits":

- **The lookup uses which item it is and where its locker sentence sits:** the "where" is a pointer the lens cannot see. Removing it stops position-based lookups, and writing it sends the lookup to the place it points at.

Bullet 3 (line 10), replaced:

- **The pointer we found is tied to the layout:** our directions mark the first locker only when no item is named before it. Refit per format, a pointer is found again in two of three formats on the 9B (prose, JSON) and Muse (prose, tables), not on the 27B. About half of the lookup's route around the lens is still open.

## 2. Section 3's title (line 64)

"## 3. The lookup uses which item it is and where its locker sentence sits"

## 3. Section 5, first bullet (line 112), then Fig. 8b right after it

- **It marks the first locker, in the clean layout:** a sentence placed before the lockers tests what "first" means (Q45.3, fixed in advance). By the rule it is mixed: the 9B and the 27B are mixed, Muse says "first locker stated before any item". After the data: our pointer marks the first locker only in the clean layout. Its code moves with every sentence that names an item before the lockers (beta: neutral 0.15-0.18; pick 0.30-0.60; an item with no locker 0.61-0.83). Once a pick sentence comes first, the Qwens' lookup stops following position and follows identity (whole change: identity 0.85-0.97 vs 0.54 / 0.65 in V0).

![Naming an item before the lockers switches the lookup from position to identity](figures/story/fig08b_layout.png)
*Fig. 8b. On Muse part of the lost position answers go back to the original answer.*

Fig. 8 keeps its panels (a)-(d) unchanged; only its title changes (block 4).

## 4. Fig. 8 title (line 115 and scripts/readme_story_figures.py, f08_first)

"Our pointer directions separate the first-mentioned item from the rest" becomes "Our pointer directions mark the first locker, in the clean layout" (alt text the same).

## 5. Section 6, Limits (line 149)

"The pointer comes from five position labels in simple scenes and mostly carries the first locker versus the rest, in the clean layout."

## 6. Fig. 11 row (scripts/readme_story_figures.py, SCORECARD_V4)

"First-mentioned item, not position in the text" becomes "Pointer tied to the layout (45a)": 9B ~, 27B ~, Muse ✓ (fixed in advance, no "a"), 122B – until its run lands. Footnote on Muse: "on a tie: the pointer part alone gives 36 position answers in V1 against 72 in V0".

## 7. docs/x0_details.md

Add the 45a table (docs/drafts/x0_details_45a.md) as its own section, after the data.

## Kept

docs/x0_details.template.md line 117, "whether the asked pick is the bridge's first mention", is a scene feature (the strata split), not the pointer's meaning.
