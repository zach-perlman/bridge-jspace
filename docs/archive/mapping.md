legacy: maps the 23 Oct README, see docs/review/review_views.yaml

# Names, internal codes, scripts and specs

The only place internal codes appear. The README's claims and the grid's findings map as below; the README numbers its claims 1-7, the grid its findings 1-8.

| README claim | Grid finding(s) |
|---|---|
| 1. The last tokens read the answer late, through attention | 4 |
| 2. They take the answer's digit, not the entity's name | 3 |
| 3. An order label picks the 1st and 2nd sentence, the bridge's identity the rest | 5 (and 6, how the label counts) |
| 4. The lens reads a stated bridge only at its own word | the lens gate (v1, v2) |
| 5. A lens push at the bridge's word writes recall, never the lookup | 7 |
| 6. The lookup ignores the lens-readable part of a stated bridge | 2 (and 8, the lens write at the same cell) |
| 7. Lookups don't need the J-space; recall does, to a varying degree | 1 |

## Findings, codes, scripts and specs

Rule ids: grid.md's mapping table states each rule.

| # | Finding | Internal codes | Scripts | Specs | Rule ids |
|---|---|---|---|---|---|
| 1 | Removing the J-space breaks recall, not the lookup | C1 (Zach's J-space knock-out; the J-space removal) | Zach's scripts/c1_v2.py (his branch); scripts/ablate_pilot.py | jobs/d5/ | removal, zach-c1 |
| 2 | A lookup ignores the lens-readable part of a stated bridge | D1 (topics, formats; parts) | scripts/statement_positions.py parts, scripts/d1_verdict.py | jobs/d1/ | stated-bridge |
| 3 | The last tokens read the answer's digit, not the entity's name | D2 parts (name vs digit) | scripts/attn_knockout.py, scripts/d2_parts.py, scripts/d2_formats.py | jobs/d2/ | formats, name-digit |
| 4 | A lookup ends in a late attention read of the answer's sentence | D2 late read (C1b) | scripts/attn_knockout.py, scripts/d2_formats.py | jobs/d2/ | formats, late-read |
| 5 | Order label for the 1st and 2nd sentence, the bridge's identity after | D3 v4 / v5 (pointer_swap) | scripts/pointer_swap.py, scripts/finding5_confirm.py | jobs/d3/ | order-identity |
| 6 | The order label counts order in the list, not place in the text | D3 v4x (pointer_v4x) | scripts/pointer_swap.py (v4x tests) | jobs/d3/ | counting |
| - | The lens names a stated bridge where it is stated (lens gate) | lens gate v1 / v2 | scripts/lens_gate.py | jobs/d1/ | lens-gate-v1, lens-gate-v2 |
| 7 | A lens push writes a stated bridge for recall; the lookup does not follow | D4 v2 / v2.1 (early_push_where) | scripts/early_push_where.py | jobs/d4/ | push-amended, push-main |
| 8 | Where the lens writes the bridge, the lookup still does not follow it | D1 readwrite; D3b lens arm | scripts/statement_positions.py readwrite, scripts/pointer_fit.py | jobs/d1/, jobs/d3/ | fitted-code, lens-write |

Internal words: D1 = the stated-bridge test (finding 2); D2 = blocking (findings 3-4); D3 = patching the last tokens (findings 5-6); D3b = the fitted position code (finding 8, last tokens); C1 = the J-space knock-out (finding 1); C2 = the lens positive control at the last tokens; D4 v2 / v2.1 = where the lens push writes, main / amended rule (finding 7). Families: PP = prompt → prompt (lookup of a stated bridge), PM = prompt → memory (recall of a stated bridge), RL / BL = lookups of a recalled / named bridge. A "draw" is a scene set; "off-path" questions are those whose bridge is not on the patched or blocked sentence; a "transit cell" is a layer and token set where patching the stated bridge still moves the answer; the "precheck" stops a stated-bridge run with too few usable scenes.

## How sure: the rule

**strong**: holds on three or more models, of both architectures (hybrid and attention-only), on two separate runs (draws, formats, long context) on at least two of them, and no cell of the finding fails, fails a control or is inconclusive · **open**: holds on no model, or fails (or is mixed) on as many models as it holds on · **medium**: everything in between. The reason given is the condition that decided it.

A model's state for a finding, from the verdicts of its cells (every draw and setting, main lens): holds = some cell holds and none fails; fails = some fails and none holds; mixed = both; unclear = only failed controls or the rule's own 'inconclusive'; values only = only cells without a committed rule; not testable = no lens, the gate or competence failed; missing = did not run or no saved verdict.

Rows used: the main lens's (grid.csv's lens column without 'listed beside'), each finding's grid settings; per-topic and per-family breakdown rows are not judged here. Separate runs: separate result folders. Numbers: grid.csv's, rounded half to even.
