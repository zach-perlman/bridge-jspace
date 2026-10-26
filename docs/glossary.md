# Figure vocabulary

One vocabulary across Figs. 0-11, 1b and 8b (Dan, 26 Oct ~21:50). Scope: every figure label, legend, subtitle and README caption (figure alt texts, "*Fig. N.*" lines, table headers) uses only the canonical strings; prose keeps the exceptions named in the table. `tests/test_readme_build.py` fails on a banned variant in the README figures' drawn text and in the captions (`docs/drafts/readme_v5_captions.md` until Tuesday's merge, then README.md).

| Concept | Canonical label | Banned variants |
|---|---|---|
| the 25 lens directions | "J++ part" | "J++" alone as a part name, "lens's part", "lens-readable part" (prose may keep "the part the lens can read" once, in In one minute) |
| our 4 position directions | "pointer"; refit ones "refit pointer"; label-free ones "label-free pointer" | "our pointer", "pointer directions", "pointer part", Alf, U |
| identity outside J++ | "identity outside J++" | "idout", "identity direction" (except in its definition) |
| the matched control | "random part (same size)"; for writes "random direction (same size)" | "random part, same size", "random directions", "random part of its size", "J++ size" |
| PCA control | "PCA directions (same size)" | "main directions", "the layer's main directions" |
| removing / keeping | "without the X", "only the X", "whole change" | "part removed", "no J++", "keep-only", "X alone", "edit" |
| answer classes | "identity", "position", "value", "original answer", "other" | "unchanged", "original" (alone) |
| prompts | "original prompt", "changed prompt" | "swapped", "Changed" as a row title without "prompt", O / S in figures |
| lockers | "first / second / third locker" | slot numbers, "slot" |
| sentence order | "locker before the pick", "locker after the pick" | "locker first/after" (prose may use "locker-first scenes" after defining it once) |
| scene sets | "main test (two people swap picks)", "one-pick scenes (only the asked pick changes)", "routes test", "sanity swap", "same item moved", "another item moved", "varied scenes: prose / JSON / table", "natural passages" | C0 / C1 / C2, "json", "simple" alone, "Same test", "one-change scenes" |
| neutral-sentence test | "a sentence before the first locker", "a sentence between the lockers and the picks" | B1 / B2 |
| metrics | "extra loss" (0-1, defined in the subtitle wherever it appears); "gap"; "code shift (positions)", written β only after "code shift"; "dose (× a real change)" | "J++ extra loss", "Jdep", "s", "s*", "beta" alone |
| shares | answer and switch shares in %, 0-100: "lookups switched (%)", "lookup answers (%)", "lookups still switching (%)" | the same quantities on 0-1 axes, "position share" |
| cell states | "not tested (gate)"; "not run"; "too few switches (k of n)" | "not in this test", "queued", "queued (if time)", "not measurable" |
| status | filled "fixed in advance"; open "after the data"; "° gate lowered to 0.75 after the data". Legend only if a figure has both statuses; otherwise one phrase in the subtitle | "fixed in advance (main test)", "° gate lowered after the data" |

Typography: arrows are drawn as "→" and "↔" (Dan's "->" and "<->"), the dose as "×". A canonical string may wrap over lines on a figure; it is still the same string.
