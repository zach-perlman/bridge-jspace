# D1 (where does a lookup in the prompt read the bridge?): interpretation, 2026-10-21

Written by hand from the saved files of the four D1 runs; every number below is from the file and field named.
Terms: org prompt / alt prompt (only the bridge differs), bridge org / bridge alt, answer org / answer alt, "paste" =
patch from the alt prompt (its hidden states at one layer pasted into the org prompt at some positions only).
Status: UNVERIFIED (nothing here is in VERIFIED.md).

## Gates (all pass)
| gate | first map (32 per family, layers 0-60) | confirmatory map (80 per family, layers 32-52) | file, field |
|---|---|---|---|
| identity paste changes nothing | top token kept 512/512; equal to an unedited read in the same batch (difference 0.0) | 1280/1280; 0.0 | map summary.json `sanity.identity` |
| alt prompt pasted everywhere at the first layer gives the alt prompt's answer | 256/256 (layer 0; margin difference up to 0.31) | 640/640 (layer 32; up to 2.0, bf16 batch rounding) | `sanity.all0` |
| memory-bridge families: pastes at the statements are exactly zero | 0 causality violations; 1,120 read anyway, difference from identity 0.0 | 0; 640 read, 0.0 | `n_causality_violations`, `sanity.noop_statements` |
| read vs greedy | 99.95% of 22,510 | 99.93% of 13,000 | `validation.agree` |
| recomputed from raw outputs == saved summary | yes (transit, handoff, sanity, validation) | yes | analysis summary.json `recomputed_equals_saved` |

## The pre-registered rule, applied (module docstring of scripts/statement_positions.py, quoted)
"H-loc (location artefact) is supported for a lookup-used bound family (BL, BLR) if at a statement set in transit at
the primary layers its J-space verdict is inside and the lens writes it there. H-around is supported if at every
statement set in transit at the primary layers its J-space verdict is around and the lens does not write it, while the
positive control at the same set and layers (countries B, else BR) is inside."

- Location: for prompt → prompt the only statement set in transit at 32-40 is the whole context (88-94% at 32-40, map
  `transit.BL.context`); the sentence stating bridge org and the bridge org word stop at layer 24 (0% from 28). The
  premise of H-loc holds only through "the whole context".
- Split (parts summary.json `cells["BL/context/primary"]`): concentration 0.14 [0.10, 0.19] at layers 32/36/40
  (random-dictionary null 0.07 [0.04, 0.10]); the rest beats the lens-readable part -> "around". Positive control at the
  same set (countries: prompt → memory) 2.66 [2.51, 2.83] -> "inside". Same for prompt → prompt → memory: 0.08
  [-0.06, 0.21], "around".
- Lens push (readwrite summary.json `cells["BL/context/primary"].by_scale`): 0/32 flips at 0.5x-8x (random 0/32);
  at 16x 3/32 vs random 1/32, difference +6 points [-6, +19]. The rule's "not written" needs every scale's upper bound
  below 10 points, so the verdict is "inconclusive" (n=32 cannot bound 3/32 vs 1/32 below 10 points).
- Verdict, as written: **neither H-loc nor H-around** for prompt → prompt and prompt → prompt → memory
  (`claims.BL.verdict` = "neither (mixed)"). H-loc is clearly not supported (lens-readable part around, lens push 0% at
  <= 4x). H-around misses only on the 16x cell of the lens-push half.
- Paired readers (the same pasted context, two questions): concentration of prompt → memory minus prompt → prompt
  = +4.84 [+4.46, +5.27] at layers 32/36; the two pastes are identical (largest share difference 0.0). The
  lens-readable part of the identical paste moves prompt → memory 59% of the way (61% flips) and prompt → prompt 2%
  (0% flips) (parts analysis summary.json `paired_means`).

## Does the confirmatory map confirm the first map's transit cells?
Yes for every cell the decision uses. Of the 416 family x set x layer cells both maps ran (layers 32-52), 54 are in
transit in both, 353 in neither, 9 differ, all near 50%: countries prompt → memory, sentence / word at 40 and 44
(56%/53% -> 45%/40%); prompt → memory, sentence / word at 36 and 38 (34-38% -> 50%); prompt → prompt → memory, whole
context at 38 (44% -> 50%). Prompt → prompt's whole context (32-44), its question (52) and its missing transit at the
sentence stating bridge org are identical in both (`d1_map_n80_v1` analysis summary.json `agreement`,
`disagreements`).

## Dan's predictions (jobs/predictions/2026-10-21_dan.md, D1) vs results
| Q | Dan | Result | Verdict |
|---|---|---|---|
| Q1.1 where does the paste flip prompt → prompt, at which layers | (a) sentence / (b) word at 20-36, (c) question / (d) last tokens at 36-56 | (a)/(b) 100% at 0-16, 81%/59% at 24, 0% from 28; (c)/(d) only from 52 (88% / 81%); in 28-44 only the whole context (88-100%), no single sentence or table row (<= 12%) | partly: order right, the handoff from (a)/(b) is earlier (24-28) and (c)/(d) take over later (52); in between the bridge is spread over the context |
| Q1.2 does the lens-readable part alone flip it there | 0% at (a)/(b); 40-50% at (c)/(d) | (a)/(b) not in transit at 32-40 (nothing to split); whole context 0/32 flips (1.8% of the way); (c)/(d) in transit only at 52, above the split layers; memory → prompt question 0% | 0% confirmed where testable; 40-50% at (c)/(d) not tested |
| Q1.3 can the lens push write prompt → prompt there | yes at 20-36 on early words, no at 36-56 | 32-40, whole context: 0/32 at 0.5-8x, 3/32 at 16x (random 1/32); 20-28 not run | "no" confirmed at 32-40; 20-28 untested |
| Q1.4 memory-bridge statement pastes do nothing | confirm | exactly zero at every statement position, layer and item (0 violations; 1,760 reads equal the identity) | confirmed |

Agent priors in the job specs: map H-loc 0.55 vs H-early-handoff 0.45. Both conditions are met as written (they were
not exclusive): the sentence stating bridge org hands off by 28, but the whole context stays in transit at 32-44 while
the question copy is 6-19%. Split H-around (prior 0.5) is what the split shows; lens H-loc (">= 30% at <= 4x") did not
happen.

## Three dumbest ways this could be wrong
1. The whole-context paste might act just like retyping the swapped words. Checked: the identical paste is 5.0x its
   share in the lens-readable part for prompt → memory and 0.14x for prompt → prompt, so the split sees "inside" on
   this very patch; what differs is the question that reads it.
2. bf16 batch noise near the threshold. Checked: the prompt → prompt cells are 81-94% (far from 50%) and replicate at
   n=80; the 9 cells that changed verdict sit at 34-56%.
3. The split and the lens push ran on n=32 at three layers only, from the first map's cells. Not fixed: the lens-push
   half is inconclusive only because n=32 cannot bound 3/32 vs 1/32 at 16x; the manifests also record a dirty tree
   (code 96c9ec2 / 3b8db6e), so the exact code state is not pinned.

Not interpretable: the lens read at the whole context (both bridge org and bridge alt are written there, 100% top-10
each), and the three-step pair's "same patch" comparison (the tables differ; largest share difference 0.13).

## Worked example (examples.json of the split run, item BL-0111, layer 36)
Org prompt: "Leo's pet is a duck. Rose's pet is a cat. Eve's pet is a turkey. The duck's locker is 3. The cat's
locker is 1. The turkey's locker is 9. Which locker belongs to Leo's pet?" -> answer org 3 (bridge org duck). Alt prompt:
"Leo's pet is a cat. ... Rose's pet is a duck." -> answer alt 1 (bridge alt cat). At layer 36: pasting the alt prompt's
states into "Leo's pet is a duck." alone -> still 3; into the question -> still 3; into the whole context -> 1. Of that
whole-context paste, the lens-readable part alone -> 3 (0.3% of the way); the rest alone -> 1 (88%). A lens push
cat − duck at the paste's size (1x) or 4x -> 3; a random push -> 3.

## For the human to verify
- results/statement_positions/d1_parts_v1/outcomes.jsonl: rows family=BL, set=context, layer in {32,36,40}, part=jspace,
  null=false -> per-item mean of `frac`; fve.jsonl rows what=jspace -> per-item share; concentration = sum(effect) /
  sum(share x full effect) = 0.14.
- results/statement_positions/d1_map_n80_v1/outcomes.jsonl: family=BL, set=context, layer=36, source=cf -> share with
  role "b" = 86% (69/80); set=bind_bridge -> 0/80.
- results/statement_positions/d1_rw_v1/outcomes.jsonl: family=BL, set=context, part=lens_x16 -> 3/32 role "b";
  random_x16 -> 1/32.
