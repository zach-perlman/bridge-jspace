# Draft: the pointer's "first" after 45a (Dan, 26 Oct ~21:45; merge on Tue after the 122B and the hand check)

Not merged. Each block names the place in docs/README.template.md (line numbers as of 7415c6f0) and the text that replaces it. Numbers: Q45.3's verdicts (results/x6_routes/*_x45a*/verdict-*) and the 45a descriptive table (results/x6_routes/x45a-descriptive-20261026T202952Z, the same numbers as 202236Z plus the identity share's CI), after the data where marked. Drafts beside this file: docs/drafts/x0_details_45a.md (the table, for docs/x0_details.template.md) and figures/drafts/fig08d_45a_identity.png (Fig. 8's new panel), both from `scripts/x45a_descriptive.py --draft`. UNVERIFIED.

## 1. In one minute, bullet 3 (line 10)

Now: "**The pointer we found is narrow:** it mostly separates the first-mentioned item from the rest and explains little outside simple scenes. About half of the lookup's route around the lens is still open."

Dan's draft: "The pointer we found is tied to the layout: our directions mark the first locker only when no item is named before it. Refit per format, a pointer is found again in prose and tables on the 9B and Muse, not on the 27B."

Agent's note: the 45d formats differ by model. On the 9B the refit pointer passes in prose and JSON; tables give 0.18 [0.13, 0.24], under the 0.2 bar. On Muse it passes in prose and tables; JSON has too few switches to count. Proposed:

- **The pointer we found is tied to the layout:** our directions mark the first locker only when no item is named before it. Refit per format, a pointer is found again in two of three formats on the 9B (prose, JSON) and Muse (prose, tables), not on the 27B. About half of the lookup's route around the lens is still open.

## 2. Section 5, first bullet (line 112)

Now: "**It mostly separates the first-mentioned item from the rest:** removing it costs the lookup most when ... so it tracks the order of mentions, not the position in the text; items in the first slot shift a little (...)."

Replace with (the rule's verdict first, then after the data):

- **It marks the first locker, in the clean layout:** a sentence placed before the lockers tests what "first" means (Q45.3, fixed in advance). By the rule it is mixed: the 9B and the 27B are mixed, Muse says "first locker stated before any item". After the data: our pointer marks the first locker only in the clean layout. Its code moves with every sentence that names an item before the lockers (beta: neutral 0.15-0.18; pick 0.30-0.60; an item with no locker 0.61-0.83). Once a pick sentence comes first, the Qwens' lookup stops following position and follows identity (whole change: identity 0.85-0.97 vs 0.54 / 0.65 in V0).

## 3. Fig. 8 title (line 115 and scripts/readme_story_figures.py line 996)

Now: "Our pointer directions separate the first-mentioned item from the rest". Replace with: "Our pointer directions mark the first locker, in the clean layout" (alt text the same). New panel (d): identity share by variant, whole change, three models (draft render: figures/drafts/fig08d_45a_identity.png).

## 4. Section 6, Limits (line 149)

Now: "The pointer comes from five position labels in simple scenes and mostly carries the first-mentioned item versus the rest." Replace with: "The pointer comes from five position labels in simple scenes and mostly carries the first locker versus the rest, in the clean layout."

## 5. Fig. 11 row (scripts/readme_story_figures.py line 1186)

Now: "First-mentioned item, not position in the text" (9B ✓, 27B ✓a, 122B ✓a, Muse ✓a). Replace with "Pointer tied to the layout (45a)", one cell per model with the rule's verdict: 9B mixed, 27B mixed, Muse "first locker" (V1 exactly on the half bar, 36 of 199 against 72), 122B: the 45a run is queued last, "if time". Symbols to confirm: mixed = ~, "first locker" = ✓ (fixed in advance, so no "a"), not run = –.

## 6. Not in Dan's list, but saying "first mentioned" (to decide)

- In one minute, bullet 2 (line 9) and the Section 3 title (line 64): "The lookup uses which item it is and where it was first mentioned". 45b says that when the locker comes after the pick, the binding happens at the locker sentence, not at the bridge word. Candidate: "The lookup uses which item it is and where its locker sentence sits".
- docs/x0_details.template.md line 117: "whether the asked pick is the bridge's first mention" is a scene feature (the strata split), not the pointer's meaning. Keep it.
