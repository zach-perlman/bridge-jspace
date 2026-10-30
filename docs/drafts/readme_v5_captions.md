# README v5: figure alt texts, captions and table headers (draft for Tuesday's merge)

Labels only (Dan, 26 Oct ~21:50): no number or claim changes. Per figure the current alt text and caption (README.md at bddf8b66), then the canonical one in the vocabulary of [docs/glossary.md](../glossary.md); the figures themselves are in figures/archive/drafts/v5/ and replace figures/depth/ at the merge. `tests/test_readme_build.py` checks every "canonical" line here until its switch `CHECK_README` is set at the merge; then it checks README.md's alt texts, "*Fig. N.*" lines and table headers.

The one-pick caveat (Dan ~22:10) goes into two captions only, Fig. 1b's (its one-pick panel) and Fig. 8's (panel (a), the first-sentence regroup, which runs on the one-pick items); not into any figure image. Its numbers: results/x0_necessity/duplicate-20261026T204558Z/duplicate.md, row qwen3.5-9b / x0_necessity/qwen35_9b_x0_single_r2 / gap (0.15 [0.07, 0.24] vs 0.64 [0.52, 0.74]). Dan's line says "needs J++"; here it says "needs the J++ part" (the glossary's part name).

## Fig. 0

- current alt text: One prompt, two questions about the same bridge word
- current caption: *Fig. 0.*
- canonical alt text: One prompt, two questions about the same bridge word
- canonical caption: *Fig. 0.*

## Fig. 1

- current alt text: Recall needs the J++ part of the bridge; the lookup mostly does not
- current caption: *Fig. 1.*
- canonical alt text: Recall needs the J++ part of the bridge; the lookup mostly does not
- canonical caption: *Fig. 1.*

## Fig. 1b

- current alt text: In every setting, recall needs J++ more than the lookup does
- current caption: *Fig. 1b.*
- canonical alt text: In every setting, recall needs the J++ part more than the lookup does
- canonical caption: *Fig. 1b.* One-pick scenes (only the asked pick changes): in this design the new bridge is an item another person already picks; when that pick comes first, the recall needs the J++ part much less (9B gap 0.15 vs 0.64).

## Fig. 2

The fourth panel is "random atoms" (Dan ~22:40): a dictionary of random atoms picked by the same OMP at its own (smaller) share, not the matched control; the figure's subtitle says so.

- current alt text: No other part of the same size costs the recall as much as J++
- current caption: *Fig. 2.*
- canonical alt text: No other part of the same size costs the recall as much as the J++ part
- canonical caption: *Fig. 2.*

## Fig. 3

- current alt text: Lookups follow the change mostly when the locker sentence comes first
- current caption: *Fig. 3.*
- canonical alt text: Lookups follow the change mostly when the locker sentence comes first
- canonical caption: *Fig. 3.*

## Fig. 4

- current alt text: Each route predicts a different locker
- current caption: *Fig. 4.*
- canonical alt text: Each route predicts a different locker
- canonical caption: *Fig. 4.*

## Fig. 5

- current alt text: The lookup follows identity or position, never the value
- current caption: *Fig. 5.*
- canonical alt text: The lookup follows identity or position, never the value
- canonical caption: *Fig. 5.*

## Fig. 6

- current alt text: Position answers appear with depth, once the lookup stops needing J++
- current caption: *Fig. 6.*
- canonical alt text: Position answers appear with depth, once the lookup stops needing the J++ part
- canonical caption: *Fig. 6.*

## Fig. 7

- current alt text: One fixed vector written at the bridge sends the lookup to its locker
- current caption: *Fig. 7.*
- canonical alt text: One fixed vector written at the bridge sends the lookup to its locker
- canonical caption: *Fig. 7.*

## Fig. 8

- current alt text: Our pointer directions separate the first-mentioned item from the rest
- current caption: *Fig. 8.*
- canonical alt text: (Fig. 8's title waits for Tuesday's "first" wording; the alt text is the new title)
- canonical caption: *Fig. 8.* (a), by what the prompt names first: in this design the new bridge is an item another person already picks; when that pick comes first, the recall needs the J++ part much less (9B gap 0.15 vs 0.64).

## Fig. 8b (new; after Fig. 8 at the merge)

- current alt text: (not in README.md yet)
- current caption: (not in README.md yet)
- canonical alt text: Naming an item before the lockers switches the lookup from position to identity
- canonical caption: *Fig. 8b.*

## Fig. 9

- current alt text: The split carries over to other texts; our pointer does not
- current caption: *Fig. 9.*
- canonical alt text: The split carries over to other texts; the pointer does not
- canonical caption: *Fig. 9.*

## Fig. 10

Dan's title (~22:40): 84 characters, 11.0 pt.

- current alt text: J++, the pointer and identity outside J++ stop most 9B and 27B lookups, not Muse's
- current caption: *Fig. 10.*
- canonical alt text: J++ part, pointer and identity outside J++ stop most 9B and 27B lookups, not Muse's
- canonical caption: *Fig. 10.*

## Fig. 11

- current alt text: What held where
- current caption: *Fig. 11.*
- canonical alt text: What held where
- canonical caption: *Fig. 11.*

## Tables

The test's README scope is table headers; the rows and the footnote below follow the glossary too. The tables' shares stay fractions here: writing them in % changes the README's number markers, not a label, so it is left for the merge.

- current header: Another item moved, the whole change
- canonical header: Another item moved, whole change
- current footnote: *°: after the data, the gate lowered to 0.75.*
- canonical footnote: *° gate lowered to 0.75 after the data.*
- current header: Sanity swap, J++ + pointer + identity outside J++ removed
- canonical header: Sanity swap, without the J++ part + pointer + identity outside J++
- current row: Lookups still switching: the part removed / a random part of its share
- canonical row: Lookups still switching: without the part / without a random part (same size)
- current row: Recall's extra loss without identity alone
- canonical row: Recall's extra loss without identity (nothing else removed)
- current cell: not in this test (the 122B)
- canonical cell: not run (the 122B)

## Supplementary figures (README Appendix A)

Their link texts already use the vocabulary ("every scene set", "every part", "every routes arm", "the parts removed together, with the bars fixed in advance"); the figures are in figures/archive/drafts/v5/supp/ and replace figures/depth/supp/ at the merge.

## docs/x0_details.md (from docs/x0_details.template.md)

The figures are in figures/archive/drafts/v5/x0_necessity/ and figures/archive/drafts/v5/status_2026-10-24/ and replace figures/archive/x0_necessity/ and figures/archive/status_2026-10-24/f6_digits.png at the merge. The page's prose still says "excess", "J-dependence", "edit" and "flips"; it is outside this pass (labels only), so the figures and the prose differ until it is reworded.

- current alt text: Overview: excess by layer, two models, three prompt formats
- canonical alt text: Overview: extra loss by layer, two models, three prompt formats
- current alt text: 27B detail
- canonical alt text: 27B detail
- current alt text: 9B detail
- canonical alt text: 9B detail
- current alt text: Equal removed share
- canonical alt text: Equal share of the change
- current alt text: Excess against the number of atoms
- canonical alt text: Extra loss against the number of atoms
- current alt text: Share against J-dependence
- canonical alt text: Share of the change against switches lost
- current alt text: Upstream change
- canonical alt text: Upstream change
- current alt text: The digit check
- canonical alt text: The digit check
