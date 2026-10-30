Glossary for the joint README, 27 Oct (Dan ~15:50; ~19:15: "lookup answer" replaces "stated answer" (stated = lookup), "remove from the patch" replaces "remove from the change", and every joint figure counts in percentage points, pp). The root [README.md](../../README.md) uses only the right-hand terms.

# Joint glossary: the reports' terms and the front page's

The two reports keep their own words: [docs/depth/README.md](../depth/README.md) (Dan) and [docs/breadth/README.md](../breadth/README.md) (Zach). The joint drafts ([joint_story_draft.md](joint_story_draft.md), [gaps.md](gaps.md)) use both. This table maps each term to the word on the front page.

## Answers and questions

| Term in a report or draft | Where | Meaning | Front page |
|---|---|---|---|
| M final, M | breadth | the attribute is never stated, so it must be recalled | recalled answer |
| K final, K | breadth | the attribute is stated in the passage | lookup answer |
| P, A, N finals | breadth | controls: a new made-up fact stated; the answer word once, on another entity; nothing stated | not on the front page (the lookup-answer controls) |
| PP, PK, PM, TK, TM, MK, MM, … | breadth | start × final: the bridge read (P), tracked (T) or recalled (M), then the final | "lookup answer" / "recalled answer" |
| P→P→M, M→M→P, … | breadth | three-hop chains, one letter per hop's source | three-step chain ending on a recalled / lookup answer |
| RM − MM | breadth | the bridge never named minus named once in passing | earlier mention |
| M − K | breadth | recall points lost minus stated-fact points lost | points more on recalled than on lookup answers |
| recall | depth | "How many legs does Iris's pick have?" | recalled answer |
| lookup | depth | "Which locker belongs to Iris's pick?" | lookup answer |
| stated answer | front page until 27 Oct ~19:15 | an answer written in the text (stated = lookup) | lookup answer |
| in-context read | joint drafts | an answer read from the prompt (lookup or K) | lookup answer |
| final | breadth | the last question of a chain | answer |

## The lens part and the tools

| Term in a report or draft | Where | Meaning | Front page |
|---|---|---|---|
| J-part | breadth | span of the top-10 J++ directions at the token | the lens part |
| J++ part | depth | the 25 signed-OMP J++ atoms that best rebuild the change | the lens part |
| entity code | joint drafts | the J-part read as "which entity" | the lens part (it says which entity it is) |
| knock-out, paper10 | breadth | the top-10 J++ directions projected out at every token of a band | remove everywhere |
| change-removal, "without the J++ part" | depth | the bridge word's change added at one layer, minus its J++ part | remove from the patch |
| remove from the change, whole change | front page until 27 Oct ~19:15 | Dan's tool; the patch with nothing removed | remove from the patch, whole patch |
| J-part swap, swap | breadth | another entity's J-part written in | swap |
| swap_comp, complement | breadth | everything but the J-part swapped | swap of everything but the lens part |
| paste | breadth | the whole residual written in | not on the front page |
| order pointer, pointer, pointer directions, alf | depth | 4 mass-mean directions outside J++ coding which locker sentence is the item's | order signal |
| identity outside J++, idout | depth | a rank-1 class-mean direction for the item, orthogonal to J++ | identity outside the lens |
| keep-only, "only the J++ part" | depth | the change with only that part added | adding only the lens part |
| write, s = 1 / 2 / 4 | depth | a fixed vector added at the bridge; s is its strength in units of the write fixed in advance | writing the order signal in (strength in words, no s) |

## Measures and controls

| Term in a report or draft | Where | Meaning | Front page |
|---|---|---|---|
| extra loss, gap | depth | share of switches lost without a part minus without a random part; recall's minus lookup's | the gap … of the change's effect |
| switch | depth | the reader gives the changed prompt's answer | moves the answer |
| transfer | breadth | share answering the donor's fact minus a third entity's | moves the answer (points) |
| random part | depth | a random subspace with the same share of the change | a random part of the same size |
| rotated, paper10_rot | breadth | the removal turned to a random direction | a random rotation |
| logit-lens control, unembed10 | breadth | the logit lens's own top-10 directions | the logit lens's own directions |
| size-matched, pcasize, PCA directions (same size) | both | the same size of removal along the residual's top principal directions | a same-size removal of the largest directions |
| by probability, soft | breadth | the score on the answer's probability | scored by probability |
| logit difference, ld | depth | the score on the answer's logit difference | scored on the answer's logit |
| band | breadth | the layers a removal spans | band of layers |
| layer L, L/2 | depth | the one layer fixed in advance | one layer (a middle layer) |

## Tests, markers and models

| Term in a report or draft | Where | Meaning | Front page |
|---|---|---|---|
| X0 | depth | Dan's main test and its strict rule | Dan's strict bar |
| main test, "two people swap picks" | depth | the change from a prompt with another bridge | Dan's scenes |
| clean design, one-pick (45m) | depth | an added item nobody picks becomes the asked pick | Dan's cleaner design |
| replication, fresh scenes | depth | the rerun on new scenes | replication |
| routes test | depth | which locker the lookup answers: by identity, position or value | Dan's scenes: "never takes the moved number" |
| 45r, Q46.1 | predictions | Zach's knock-out on Muse at L23-29 against Dan's L26 gap | pending test: Muse 30B at the same depth |
| 45s, Q46.2-Q46.3 | predictions | Dan's tests on Lightning at L30 | pending test: Lightning with remove from the patch |
| GAP -> … | joint drafts | a cell with no number yet | Pending tests |
| ° | joint drafts | judged after the data | (post hoc: a gate or rule set after the results were seen) |
| Qwen3.5-9B | both | | Qwen 9B |
| Qwen3.6-27B | both | | Qwen 27B |
| Qwen3.5-122B-A10B (FP8) | both | | Qwen 122B |
| Muse Glimmer 30B | both | | Muse 30B |
| Nemotron 3.5 Lightning | breadth | | Nemotron Lightning |
| Bolt, DeepSeek, Ministral, OLMo | breadth | the other models | grid only (and the methods section) |
