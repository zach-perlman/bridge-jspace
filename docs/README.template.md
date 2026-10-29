<!-- grid: results/cross_model/20261023T210238Z -->
# One word, two readers: what a model keeps at the bridge and what the lens sees

*A two-step question passes through one word, the bridge. The recall asks what the model knows about the item, the lookup where the prompt put it. What does each read from that word, and what can a lens see?*

## In one minute

- **Four models, two families and a hybrid architecture:** Qwen3.5-9B and Qwen3.6-27B, Muse Glimmer 30B, and Nemotron 3.5 Lightning, a Mamba-attention hybrid (its marks hollow ○: its gate was chosen after a pre-check was seen). Qwen3.5-122B-A10B (FP8; MoE, ~10B active) ran the first tests and joins where it ran.
- **On all four, the two readers split the bridge word:** the recall follows the part the lens reads, the lookup the rest [A]; the recall does not need that part at one layer, it has other copies [B]. Of that part's directions the readable ones are the two bridge words, almost never the answer; most of its energy matches no word of the scene.
- **On all four, the lookup goes by which item it is or where its locker sits, never by the number** [A]; its "which item" runs outside the lens [B]. Where the locker sits is an address: readable before it is used, removable, swappable, invisible to the lens [A/B]. A swap sends the lookup to the swapped-in locker, and some recalls to the swapped-in item.
- **At the last token** the recall's item is readable through the lens on all four models, but not used there at a real change's size.
- **Weaker on the 27B:** its lookup follows the lens part in part; adding the address alone brings no position answers back; swaps between given lockers miss on most pairs; on its full layer grid the lookup still needs the lens part after it takes up the address.
- **Limits, withdrawn, failed:** on Zach's true-fact passages, and when every token before L changes, the lookup follows the lens part too; with made-up facts the split returns on the 9B. Withdrawn: the described bridge on Zach's passages; "one code per locker" is now "swaps between given lockers work; the code's size is open". Did not hold: four mechanism tests, a person mark at the locker sentence, blocking the pick sentence, on every model that ran them [✗].

**Status.** Five models: Qwen3.5-9B, Qwen3.6-27B, Muse Glimmer 30B (another family), Nemotron 3.5 Lightning 30B-A3B (a third family, a Mamba-attention hybrid), and Qwen3.5-122B-A10B (FP8; MoE, ~10B active) as the fifth where it ran (the first tests only; grey "not run" elsewhere); 29 Oct 2026. Unverified until hand-checked. Built at {{head}} from the run files. Lightning ran on the rules already fixed for the other models, with no prediction of its own; its numbers are marked ○ (hollow) everywhere: its gate was chosen after the 60-scene pre-check was seen. Nemotron 3.5 Bolt is out of scope: no J++ lens exists for it. The largest model's lookup loses nothing beyond random ({{pt|lk_excess_k25_122b}} with 25 lens directions; {{pt|lk_excess_k100_122b}} with 100, where the 27B loses {{pt|lk_excess_k100_27b}}), so the 27B's weakness is not a total-size trend; active parameters are not separated; its recall effect is the smallest of the five ({{pt|rc_excess_122b}}) and mixed on varied scenes ({{pt|x0b_c_122b}}); we cannot separate that from its later layer (L{{num|layer_122b}}, relative depth {{dp|cards|122b|L as a relative depth (L / the number of layers)}}) or FP8. Restructure in progress (Dan, 28 Oct 22:20): Parts II-VI keep their previous format until they move to the card template.

## The question and the setup

![One prompt, two questions about the same bridge word](figures/story/fig00_setup.png)
*The running example: one prompt, its two questions and the changed prompt.*

- **The prompt** (a main-test scene): "The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked carbon. Eva picked helium."
- **The lookup** asks "Which locker belongs to Eric's pick?" (3, found in the prompt). **The recall** asks "What is the atomic number of Eric's pick?" (6, from memory).
- **The bridge** is the word both questions pass through: "carbon", Eric's pick.
- **The changed prompt** swaps the two picks, so Eric picks oxygen and the answers become 7 and 8.
- **The question:** what does each reader take from the bridge word, and how much of it can the J++ lens read?
- **Lightning's layer**, L{{dp|cards|nemotron-3.5-lightning|L: the layer fixed in advance}}, was picked by a rule fixed before its layer sweep was read (Dan, 29 Oct ~00:50 Paris): the earliest layer passing the gate at relative depth ≥ 0.25, ties broken by the highest lens readability of the bridge word. [The conflict test at every swept layer](results/x0_necessity/nem35l_x52_conflict/verdict-20261029T001612Z/verdict.md).

## How to read this page

**Methods**, named the same way in every card:

- **The change**: at the bridge word and one layer, the changed prompt's state minus the original's, added to the original prompt's run (Eric's "carbon" moves towards "oxygen"). A reader **switches** if it then gives the changed prompt's answer.
- **The lens part** (on the figures, "the J++ part"): the 25 directions of the J++ lens that best rebuild the change. **A random part**: random directions with the same share of the change. **The rest**: the change without the lens part.
- **Conflict test**: the change with one part taken out; both readers read the same changed word, so each shows which part it follows.
- **Part alone**: one part added by itself, at a **dose** (a multiple of its size in the change).
- **Zeroing**: a part taken out of the changed prompt's own state, nothing added; a reader **keeps** or loses the changed prompt's answer.
- **Swap and state copy**: a swap replaces one code at the bridge word by another's; a state copy moves the changed prompt's states at chosen tokens and layers into the original.
- **Probe, lens readout, layer sweep**: a linear read-out trained on states; the lens's top words at a token; one test repeated over layers.

Every removal and every addition is matched by the same operation on a random part of the same size; only the difference between them is about the named part.

**Measures**, defined once:

- **Switches lost beyond a random part** (the figures' "extra loss"): switches lost without a part minus those lost without its random part, as a share of the whole change's switches. **The gap**: the recall's minus the lookup's.
- **Answers lost beyond random** (zeroing): answers kept with the random part taken out minus those kept with the lens part taken out.
- **L**: the layer fixed in advance, {{num|layer_9b}} / {{num|layer_27b}} / {{num|layer_muse}} / {{dp|cards|nemotron-3.5-lightning|L: the layer fixed in advance}} / {{num|layer_122b}} on the 9B / 27B / Muse / Lightning / 122B; **L to L+3**: L and the three layers after it.
- **Identity route**: the lookup names the item's own locker; **position route**: the locker now at the item's old place; **value**: the new number.
- **The address**: four directions at the bridge word that code where the item's locker sentence sits (Part III).
- **Rules** are quoted as committed, internal metric names replaced by these terms; "after the data" marks a rule or gate set after results were seen.

**Reading the figures**:

![How to read the figures: colour is who, the mark is what was done](figures/story/fig00b_marks.png)
*Colour says which reader or part; the mark says what was done to it.*

- **Whiskers and bands**: {{q|95%}} intervals, cluster bootstrap over bridge items. **● / ○** beside n: rule fixed in advance / read after the data; a hollow mark: a gate lowered after the data, or Lightning's gate (chosen after the 60-scene pre-check was seen). A model that misses a gate is "not tested (gate)"; where its numbers are shown they are descriptive only, hollow, and never relabelled.
- **Beyond random**: the grey band, strip or tick at zero (for Zach's stored rows, his rotated directions). **Dashed or dotted line**: a rule's bar. Cells not run, failing a gate or under 30 switches are left out.
- **Dose (×)**: a part's size relative to its size in the change; a **ring** marks the dose a rule reads. **z** (the lens-blindness figure): distance from 200 random vectors in units of half their {{q|95%}} range; the grey strip spans −1 to 1.

## Data: the prompt sets

Every prompt is read in the model's chat template, thinking off, the reply begun with "Answer:"; in the digit sets each question ends "Answer with a single digit and nothing else."

| Set | What it is | The changed prompt differs in | n (9B / 27B / Muse / Lightning ○ / 122B) | Gate; one-token answers | Used by |
|---|---|---|---|---|---|
| Main test | six sentences: three lockers and three picks, in shuffled order | two people swap picks (two pick sentences) | {{num|n_9b}} / {{num|n_27b}} / {{num|n_muse}} / {{dp|catalogue|nemotron-3.5-lightning|main test: scenes used}} / {{num|n_122b}} | both readers right on the original prompts at least 0.80 of the time; digits, one token | the conflict test, zeroing, the dose curves |
| Clean one-pick | the main test plus a locker for an item nobody picks | the asked pick becomes that item (one token) | {{dp|catalogue|9b|clean one-pick scenes: scenes used}} / {{dp|catalogue|27b|clean one-pick scenes: scenes used}} / {{dp|catalogue|muse|clean one-pick scenes: scenes used}} / not tested (gate) / not run | as above; digits | the ladder, the earlier mention, the order tests, the token map |
| Routes scenes | three lockers, then three picks | another item's locker sentence trades places with a third and gets a new number; the asked pick becomes that item | {{dp|catalogue|9b|routes scenes: scenes used}} / {{dp|catalogue|27b|routes scenes: scenes used}} / {{dp|catalogue|muse|routes scenes: scenes used}} / {{dp|catalogue|nemotron-3.5-lightning|routes scenes: scenes used}} / {{dp|catalogue|122b|routes scenes: scenes used}}° | as above; digits | the routes test; removing, adding and swapping the address |
| Six-locker scenes | six lockers, then three picks | the item's own locker sentence moves to another place and gets a new number; the pick stays | {{dp|catalogue|9b|six-locker scenes: scenes used}} / – / {{dp|catalogue|muse|six-locker scenes: scenes used}} / {{dp|catalogue|nemotron-3.5-lightning|six-locker scenes: scenes used}} / not run | as above; digits | swaps between given lockers |
| Varied scenes | prose, JSON or markdown tables; up to nine items, look-alike names, filler, paraphrased questions | the asked pick | {{dp|catalogue|9b|varied scenes: scenes used (prose, JSON and table)}} / {{dp|catalogue|27b|varied scenes: scenes used (prose, JSON and table)}} / {{dp|catalogue|muse|varied scenes: scenes used (prose, JSON and table)}} / {{dp|catalogue|nemotron-3.5-lightning|varied scenes: scenes used (prose, JSON and table)}} / {{num|x0b_n_122b}} | per format and level; failing cells left out; digits | the split in other texts, the refit address |
| Natural passages | notes, news, forum posts and emails with distractor sentences | the one sentence binding a person to the bridge | {{dp|catalogue|9b|natural passages: scenes eligible}} / {{dp|catalogue|27b|natural passages: scenes eligible}} / {{dp|catalogue|muse|natural passages: scenes eligible}} / {{dp|catalogue|nemotron-3.5-lightning|natural passages: scenes eligible (below gate)}} below gate / {{dp|catalogue|122b|natural passages: scenes eligible}} | as above, the 9B's lowered after the data; words, read by their first token | the split in natural text |
| Zach's passages | his passages: a named or a described bridge; the final fact stated in the lookup's passage, left out of the recall's | the sentence naming the bridge, or the description | named {{dp|catalogue|9b|Zach's passages, named bridge: passages used}} / {{dp|catalogue|27b|Zach's passages, named bridge: passages used}} / {{dp|catalogue|muse|Zach's passages, named bridge: passages used}} / {{dp|catalogue|nemotron-3.5-lightning|Zach's passages, named bridge: passages used}} / not run; described {{dp|catalogue|9b|Zach's passages, described bridge: passages used}} / {{dp|catalogue|27b|Zach's passages, described bridge: passages used}} / {{dp|catalogue|muse|Zach's passages, described bridge: passages used}} / – / not run | per reader; words, read by their first token; about a third of the bridge names are several tokens | Part V |

One item per set, copied from the run files (the original prompt; → the changed prompt's answer):

**Main test** (all four models; the page's running example):

```
The locker of carbon is 3. The locker of helium is 5. The locker of oxygen is 7. Hugo picked oxygen. Eric picked carbon. Eva picked helium.
Changed: Hugo picked carbon. Eric picked oxygen.
Lookup: Which locker belongs to Eric's pick?        3 → 7
Recall: What is the atomic number of Eric's pick?   6 → 8
```

**Clean one-pick** (9B, 27B, Muse):

```
The locker of the cow is 3. The locker of the eagle is 5. The locker of the owl is 4. The locker of the fox is 1. Jack picked the cow. Tara picked the fox. Diana picked the owl.
Changed: Jack picked the eagle.
Lookup: Which locker belongs to Jack's pick?   3 → 5
Recall: How many legs does Jack's pick have?   4 → 2
```

**Routes scenes** (9B and 27B):

```
The locker of the pig is 3. The locker of the butterfly is 4. The locker of the horse is 7. Finn picked the butterfly. Mia picked the horse. Luke picked the pig.
Changed: The locker of the horse is 1. The locker of the butterfly is 4. The locker of the pig is 3. Finn picked the horse.
Lookup: Which locker belongs to Finn's pick?   4 → 1; identity route 7, position route 3, value 1
Recall: How many legs does Finn's pick have?   6 → 4
```

**Six-locker scenes** (9B):

```
The locker of the camel is 7. The locker of the rabbit is 4. The locker of the dog is 6. The locker of the beetle is 3. The locker of the mouse is 2. The locker of the fox is 9. Vera picked the fox. Oscar picked the rabbit. Lily picked the camel.
Changed: The locker of the beetle is 3. ... The locker of the camel is 5. ...
Lookup: Which locker belongs to Lily's pick?   7 → 5; identity route 7, position route 3, value 5
```

**Varied scenes** (JSON, all four models):

```
Tool output from get_lockers:
[{"item": "fly", "locker": 2}, {"item": "elephant", "locker": 9}, {"item": "camel", "locker": 6}, {"item": "ant", "locker": 4}, {"item": "duck", "locker": 3}, {"item": "rabbit", "locker": 7}]
Tool output from get_picks:
[{"name": "Nina", "pick": "elephant"}, ..., {"name": "Eve", "pick": "duck"}, {"name": "Carl", "pick": "ant"}, {"name": "Paul", "pick": "fly"}]
Changed: {"name": "Eve", "pick": "ant"}
Lookup: Which locker belongs to Eve's pick?   3 → 4
Recall: How many legs does Eve's pick have?   2 → 6
```

**Natural passages** (all four models; Lightning below gate):

```
Meeting notes, 14 March.
- The delegation from Kenya announced that its next meeting will take place in Asia.
- Hannah Kerr was raised in Finland.
- The delegation from Bolivia announced that its next meeting will take place in North America.
- Tess Garland was raised in Bolivia.
- Paul Whitaker was raised in Kenya.
(and four distractor lines)
Changed: Tess Garland was raised in Kenya.
Lookup: Which continent will host the next meeting of the delegation from the country where Tess Garland was raised?   North America → Asia
Recall: Which continent is the country where Tess Garland was raised in?   South America → Africa
```

**Zach's passages** (named bridge, 9B; excerpt of the lookup's passage):

```
Posted by travel_notes_88: Uzbekistan is a country in Asia. ... Laura Bennett spent a whole childhood in Vietnam. ... Poland is a country in Europe. ... Eli Thornton spent a whole childhood in Poland. ... Vietnam is a country in Asia.
Changed: Eli Thornton spent a whole childhood in Vietnam.
Both readers: The country of Eli Thornton's childhood is on which continent?   Europe → Asia
(the recall's passage drops the "is a country in" sentences)
```

## Claims

| # | Claim | Models | Grade | Key numbers | Hand-checked |
|---|---|---|---|---|---|
| 1 | The recall follows the lens part of the bridge word; the lookup follows the rest | 9B, 27B, Muse, Lightning, 122B (the 122B's varied scenes: mixed) | **A** (27B partial) | recall {{pt|rc_excess_9b}} / {{pt|rc_excess_27b}} / {{pt|rc_excess_muse}} / {{dp|cards|nemotron-3.5-lightning|conflict: recall, switches lost beyond a random part}} ○ / {{pt|rc_excess_122b}}; lookup {{pt|lk_excess_9b}} / {{pt|lk_excess_27b}} / {{pt|lk_excess_muse}} / {{dp|cards|nemotron-3.5-lightning|conflict: lookup, switches lost beyond a random part}} ○ / {{pt|lk_excess_122b}}. Limits: on the full carrier, fact-after lookups follow the lens ({{dp|cards|nemotron-3.5-lightning|51.7: fact-after lookups, full carrier: switches lost beyond a random part}}-{{dp|cards|9b|51.7: fact-after lookups, full carrier: switches lost beyond a random part}}); on Zach's true-fact passages the 9B's and 27B's lookups follow it ({{dp|cards|9b|Z1: lookup, switches lost beyond a random part}} / {{dp|cards|27b|Z1: lookup, switches lost beyond a random part}}); on his made-up-fact passages the split holds on the 9B, the 27B is in between (Part V) | no |
| 2 | The recall does not need the lens part at one layer; it has other copies | 9B, 27B, Muse, Lightning | **B** | kept {{dp|fig01c|9b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{dp|fig01c|27b|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{dp|fig01c|muse|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} / {{dp|cards|nemotron-3.5-lightning|47.5: recall's answers kept at L, the J++ part's 25 directions taken out}} ○ | no |
| 3 | The recall also reads the item's earlier mention | 9B, 27B, Muse | **B** | {{pt|x45p_d23_9b}}-{{pt|x45p_d23_muse}} | no |
| 4 | The lookup goes by which item it is or where its locker sits, never by the number | 9B, 27B, Muse, Lightning, 122B° | **A** | 9B identity / position {{pt|rt_C2_whole_identity_9b}} / {{pt|rt_C2_whole_position_9b}}; Lightning {{dp|fig05|nemotron-3.5-lightning|another item moved, whole: identity share}} / {{dp|fig05|nemotron-3.5-lightning|another item moved, whole: position share}} ○; 122B° {{pt|rtg_C2_whole_identity_122b}} / {{pt|rtg_C2_whole_position_122b}}; value none anywhere | no |
| 5 | The lookup's “which item” lives outside the lens | 9B, 27B, Muse, Lightning | **B** | identity route without 26–100: {{dp|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|e3_identity|nemotron-3.5-lightning|47.1: identity answers lost beyond random without lens directions 26-100}} ○; position route at most {{dp|fig05d||47.1: position route: the most answers lost beyond random, over the models and slices}} | no |
| 6 | The address can be removed, and a swap redirects the lookup | 9B, 27B, Muse, Lightning, 122B° | **A** | position answers without it {{pt|rt_C2_no_alf_position_9b}} / {{pt|rt_C2_no_alf_position_27b}} / {{pt|rt_C2_no_alf_position_muse}} / {{dp|fig05|nemotron-3.5-lightning|another item moved, no_alf: position share}} ○ / {{pt|rtg_C2_no_alf_position_122b}}° vs random {{pt|rt_C2_no_alf_rand_position_9b}} / {{pt|rt_C2_no_alf_rand_position_27b}} / {{pt|rt_C2_no_alf_rand_position_muse}} / {{dp|fig05|nemotron-3.5-lightning|another item moved, no_alf_rand: position share}} ○ / {{pt|rtg_C2_no_alf_rand_position_122b}}°; the swap at s = 2 moves {{dp|fig07|9b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|27b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|muse|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|nemotron-3.5-lightning|lookup target share, mean over locker pairs, s = 2}} ○ / {{pt|x8_t2_122b}}° (pooled over locker pairs) of lookups | no |
| 7 | Adding the address alone brings position answers back | 9B, Muse, Lightning, 122B° (27B fails) | **B** | {{pt|rtk_C2_keep_alf_position_9b}} / {{pt|rtk_C2_keep_alf_position_27b}} / {{pt|rtk_C2_keep_alf_position_muse}} / {{dp|fig07|nemotron-3.5-lightning|another item moved, keep_alf: position share}} ○ / {{pt|rtk_C2_keep_alf_position_122b}}° | no |
| 8 | With six lockers, swaps between given lockers work on most pairs; the code's size is not settled | 9B, Muse, Lightning (not the 27B) | **B** | pairs reaching the bar {{dp|fig09b|9b|47.2: pairwise writes reaching 25% (dose 2)}} / {{dp|cards|27b|47.2: pairwise writes reaching 25% (dose 2)}} / {{dp|fig09b|muse|47.2: pairwise writes reaching 25% (dose 2)}} / {{dp|fig09b|nemotron-3.5-lightning|47.2: pairwise writes reaching 25% (dose 2)}} ○ of 30; the code's size on the 9B: {{dp|cards|9b|51.11 part 1: the code's size}}; midpoint swaps fail ({{dp|cards|9b|51.11 part 3: midpoint swaps reaching the slot between, from the first slot (dose 2)}}), so not a metric order | no |
| 9 | The lens cannot read the address | 9B, 27B, Muse, Lightning | **B** | share rebuilt {{dp|fig07b_verbal|9b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|27b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|muse|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|cards|nemotron-3.5-lightning|47.0 (b) share rebuilt by 25 lens directions: pointer}} ○ | no |
| 10 | The bridge word redirects the lookup only when its locker sentence came first | 9B, 27B, Muse, Lightning | **A** | locker first {{num|lk_order_before_muse}}-{{num|lk_order_before_122b}}, after {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}}; Lightning {{dp|fig03|nemotron-3.5-lightning|lookups switched by the whole change, locker sentence before the pick}} / {{dp|fig03|nemotron-3.5-lightning|lookups switched by the whole change, locker sentence after the pick}} ○; copy {{pt|x45q_c_9b}} / {{pt|x45q_c_27b}} / {{pt|x45q_c_muse}} / {{dp|fig03|nemotron-3.5-lightning|45q, the rule's arm c: copy at L, every locker-sentence token (lookups switched)}} ○ below gate | no |
| 11 | Lookups the change at L misses were read from the bridge word before L | 9B, 27B, Muse, Lightning | **B** | carried before L {{dp|e11_before_l|9b|47.4: main, locker after the pick: lookups carried by the bridge word before L}} / {{dp|e11_before_l|27b|47.4: main, locker after the pick: lookups carried by the bridge word before L}} / {{dp|e11_before_l|muse|47.4: main, locker after the pick: lookups carried by the bridge word before L}} / {{dp|e11_before_l|nemotron-3.5-lightning|47.4: main, locker after the pick: lookups carried by the bridge word before L}} ○ | no |
| 12 | The address is readable before the lookup uses it, and the lookup never reads the value | 9B, 27B, Muse, Lightning | **B** | address readable from / used from layer {{dp|cards|9b|47.8: the address readable from}} / {{dp|cards|9b|47.8: the first layer of the position route}} (9B), {{dp|cards|27b|47.8 (full grid): the address readable from}} / {{dp|cards|27b|47.8 (full grid): the first layer of the position route}} (27B), {{dp|cards|muse|47.8: the address readable from}} / {{dp|cards|muse|47.8: the first layer of the position route}} (Muse), {{dp|cards|nemotron-3.5-lightning|47.8: the address readable from}} / {{dp|cards|nemotron-3.5-lightning|47.8: the first layer of the position route}} ○ (Lightning); the handoff from the lens part depends on the layer grid ([E12](#e12-anatomy)); whether the address travels to the last token: {{dp|cards|9b|51.4: the rule's reading}} (9B), {{dp|cards|27b|51.4: the rule's reading}} (27B), {{dp|cards|muse|51.4: the rule's reading}} (Muse), {{dp|cards|nemotron-3.5-lightning|51.4: the rule's reading}} ○ (Lightning) | no |

*Grades: **A**, a rule fixed in advance held on at least three models with a specificity control and a variant design; **B**, on two models, or three with one operation, or descriptive on three with a random null.* Weaker and failed results are in Part VI; pending tests under Status. Lightning ran on the rules already fixed for the other models, with no prediction of its own; its key numbers carry ○. Claim 8 said "every locker has its own code" until a test on held-out items left the code's size open; claim 12 said "identity route early, position route late" until the 27B's full grid failed the handoff; both stay B (claim 12: four models, one operation). The 122B is added only to the claims whose rule it meets at its own gate (1, 4, 6, 7); ° marks its runs with the gate lowered after the data (routes, address, swap); its varied scenes are mixed; the tests behind the other claims did not run on it.

## Part I. The two readers: lookup and recall

*The two readers weight different parts of one word, and the recall has copies elsewhere.*

### In a conflict, which part of the bridge word does each reader follow?

- **Question.** In a conflict, which part of the bridge word does each reader follow?
- **Why we asked.** Both readers pass through the same word; if they took the same thing from it, the lens part would matter to both alike.
- **Data.** Main test, {{num|n_9b}} / {{num|n_27b}} / {{num|n_muse}} / {{dp|catalogue|nemotron-3.5-lightning|main test: scenes used}} / {{num|n_122b}} scenes per model, the first in which both readers answer both prompts right; the gate passed on all five (Lightning's chosen after its pre-check, ○). The 122B (FP8; MoE, ~10B active) runs at L{{num|layer_122b}}: its L33 is the 27B's relative depth carried over (33/48), not the other models' rule; its J++ lens was fit on the bf16 weights.
- **Method.** The change at the bridge word at L, on the original prompt (Eric's "carbon" moves towards "oxygen"):
  - the whole change, which sets the switches each arm can lose;
  - without the lens part; control: without a random part;
  - specificity: without the lens part but keeping its directions for both readers' answer words ("six", "eight"), and without those answer directions only, each against a random part of their share; and the lens's rank of the answer word at the bridge word.
- **Rule, fixed in advance.** "Confirmed if the lookup loses at most 0.10 beyond random and the recall loses at least 0.30 of its switches without the lens part; killed if the lookup loses at least 0.20 or the recall under 0.20." Specificity: "the lens effect is the item if the recall keeps at least 0.7 of its loss with the answer directions kept and loses at most 0.10 beyond random without them only". Before that result was opened, the answer directions became number words (digits are not in the lens) and a check of the answer word's rank was put first. Lightning: the same rules, copied, no prediction.
- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | recall: switches lost beyond a random part | {{num|rc_excess_9b}} | {{num|rc_excess_27b}} | {{num|rc_excess_muse}} | {{d|cards|nemotron-3.5-lightning|conflict: recall, switches lost beyond a random part}} | {{num|rc_excess_122b}} |
  | recall: switches lost, not net of random | {{num|rc_jdep_9b}} | {{num|rc_jdep_27b}} | {{num|rc_jdep_muse}} | {{dp|cards|nemotron-3.5-lightning|conflict: recall, switches lost, not net of random}} | {{num|rc_jdep_122b}} |
  | lookup: switches lost beyond a random part | {{num|lk_excess_9b}} | {{num|lk_excess_27b}} | {{num|lk_excess_muse}} | {{d|cards|nemotron-3.5-lightning|conflict: lookup, switches lost beyond a random part}} | {{num|lk_excess_122b}} |
  | the rule | {{num|verdict_9b}} | {{num|verdict_27b}} | {{num|verdict_muse}} | {{dp|cards|nemotron-3.5-lightning|conflict: the rule}} | {{num|verdict_122b}} |
  | recall: share of its loss kept with the answer directions kept | {{d|conflict_answer|9b|main test, recall: share of its loss kept when the lens part keeps the answer words' directions}} | {{d|conflict_answer|27b|main test, recall: share of its loss kept when the lens part keeps the answer words' directions}} | {{d|conflict_answer|muse|main test, recall: share of its loss kept when the lens part keeps the answer words' directions}} | {{d|conflict_answer|nemotron-3.5-lightning|main test, recall: share of its loss kept when the lens part keeps the answer words' directions}} | {{d|conflict_answer|122b|main test, recall: share of its loss kept when the lens part keeps the answer words' directions}} |
  | recall: switches lost beyond random without the answer directions only | {{d|conflict_answer|9b|main test, recall: switches lost beyond random without the answer words' directions only}} | {{d|conflict_answer|27b|main test, recall: switches lost beyond random without the answer words' directions only}} | {{d|conflict_answer|muse|main test, recall: switches lost beyond random without the answer words' directions only}} | {{d|conflict_answer|nemotron-3.5-lightning|main test, recall: switches lost beyond random without the answer words' directions only}} | {{d|conflict_answer|122b|main test, recall: switches lost beyond random without the answer words' directions only}} |
  | recall: answer word outside the lens's top 50 at the bridge word | {{d|conflict_answer|9b|main test, recall: items whose answer word ranks below the lens's top 50 at the bridge word}} | {{d|conflict_answer|27b|main test, recall: items whose answer word ranks below the lens's top 50 at the bridge word}} | {{d|conflict_answer|muse|main test, recall: items whose answer word ranks below the lens's top 50 at the bridge word}} | {{d|conflict_answer|nemotron-3.5-lightning|main test, recall: items whose answer word ranks below the lens's top 50 at the bridge word}} | {{d|conflict_answer|122b|main test, recall: items whose answer word ranks below the lens's top 50 at the bridge word}} |
  | the specificity rule | {{dp|conflict_answer|9b|main test, recall: the rule's label (page words)}} | {{dp|conflict_answer|27b|main test, recall: the rule's label (page words)}} | {{dp|conflict_answer|muse|main test, recall: the rule's label (page words)}} | {{dp|conflict_answer|nemotron-3.5-lightning|main test, recall: the rule's label (page words)}} | {{dp|conflict_answer|122b|main test, recall: the rule's label (page words)}} |

- **Read.**
  - The recall follows the part of the bridge word the lens reads; the lookup follows the rest, fully on the 9B, Muse, Lightning and the 122B, mostly on the 27B.
  - What the recall follows is the item, not its answer: keeping the answer's lens directions keeps almost all of the recall's loss.
- **Caveats.**
  - Following is not needing: a part is taken out of an added change at one layer (see "Does the recall need the lens part, or only follow it?").
  - The 27B's lookup misses its bar, and loses {{pt|lk_excess_k100_27b}} beyond random when 100 lens directions go (an open question).
  - On Muse, Lightning and the 122B the answer word is almost never near the top of the lens readout, so the rule's first case decides there.
  - Two limits, on Zach's passages (Part V): on the full carrier (every token before L), fact-after lookups follow the lens part ({{dp|cards|nemotron-3.5-lightning|51.7: fact-after lookups, full carrier: switches lost beyond a random part}} ○ to {{dp|cards|27b|51.7: fact-after lookups, full carrier: switches lost beyond a random part}} lost beyond random); on his true-fact passages the 9B's and 27B's lookups follow it at L ({{dp|cards|9b|Z1: lookup, switches lost beyond a random part}} / {{dp|cards|27b|Z1: lookup, switches lost beyond a random part}}). On his made-up-fact passages the split holds on the 9B and is in between on the 27B; Lightning is not tested there (gate).

![The recall follows the lens part of the bridge word; the lookup mostly does not](figures/story/fig01_split.png)
*Switches lost without the lens part beyond a random part, per reader and model, main test at L (the 122B's L33: the 27B's relative depth carried over); whiskers: {{q|95%}} intervals; grey band: the lookup's 0.10 bar.*

### What do the lens part's 25 directions stand for?

- **Question.** What do the lens part's 25 directions stand for?
- **Why we asked.** The conflict test treats the lens part as one block; if its directions were mostly the answer words, "the recall follows the item" would be a reading of the answer.
- **Data.** Main test, {{dp|cards|9b|52 A: main-test scenes}} scenes per model (the same change for both readers).
- **Method.** Each of the 25 directions is a word of the lens's vocabulary; each is classed automatically as the original bridge word (or its spelling: first token, initial, prefix), the new bridge word, another scene item, a person, either reader's answer word, a word of the same class, a function word, or none of these. Its share is the energy it adds when it enters the rebuild. The classifier was hand-checked on {{dp|cards|9b|52 A: hand-checked items (the lookup's view)}} items per model on the 9B, 27B and Muse (agreement {{dp|cards|muse|52 A: hand labels agreeing with the classifier}}-{{dp|cards|9b|52 A: hand labels agreeing with the classifier}}; only Muse's labels are blind: on the 9B and 27B the labeller had seen some of the classifier's labels while writing its spelling rules); Lightning's labels are not hand-checked.
- **Rule, fixed in advance.** None: descriptive.
- **Result.**

  | share of the rebuilt energy | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | the old bridge word | {{d|cards|9b|52 A: share of the rebuilt energy in the original bridge word}} | {{d|cards|27b|52 A: share of the rebuilt energy in the original bridge word}} | {{d|cards|muse|52 A: share of the rebuilt energy in the original bridge word}} | {{d|cards|nemotron-3.5-lightning|52 A: share of the rebuilt energy in the original bridge word}} | not run |
  | the new bridge word | {{d|cards|9b|52 A: share of the rebuilt energy in the new bridge word}} | {{d|cards|27b|52 A: share of the rebuilt energy in the new bridge word}} | {{d|cards|muse|52 A: share of the rebuilt energy in the new bridge word}} | {{d|cards|nemotron-3.5-lightning|52 A: share of the rebuilt energy in the new bridge word}} | not run |
  | the recall's answer word | {{dp|cards|9b|52 A: share of the rebuilt energy in the reader's answer word}} | {{dp|cards|27b|52 A: share of the rebuilt energy in the reader's answer word}} | {{dp|cards|muse|52 A: share of the rebuilt energy in the reader's answer word}} | {{dp|cards|nemotron-3.5-lightning|52 A: share of the rebuilt energy in the reader's answer word}} | not run |
  | no scene word | {{d|cards|9b|52 A: share of the rebuilt energy in no scene word}} | {{d|cards|27b|52 A: share of the rebuilt energy in no scene word}} | {{d|cards|muse|52 A: share of the rebuilt energy in no scene word}} | {{d|cards|nemotron-3.5-lightning|52 A: share of the rebuilt energy in no scene word}} | not run |
  | bridge-word directions with the expected sign (old −, new +) | {{dp|cards|9b|52 A: the bridge words' directions whose sign points the expected way (old -, new +)}} | {{dp|cards|27b|52 A: the bridge words' directions whose sign points the expected way (old -, new +)}} | {{dp|cards|muse|52 A: the bridge words' directions whose sign points the expected way (old -, new +)}} | {{dp|cards|nemotron-3.5-lightning|52 A: the bridge words' directions whose sign points the expected way (old -, new +)}} | not run |

- **Read.**
  - The two bridge words carry about a tenth to a fifth of the rebuilt energy each, with the expected signs: the old word taken away, the new one added.
  - The answer words carry almost nothing.
  - Most of the energy matches no word of the scene; some of it is the bridge's spellings the classifier missed.
- **Caveats.**
  - This is what is readable through the lens's vocabulary, not all that is there.
  - Descriptive: no rule was fixed in advance; one set (the main test) per model.

![The lens part's directions: the bridge words, almost never the answer](figures/story/fig18_atoms.png)
*The lens part's rebuilt energy at the bridge word, split by the kind of lens word each of its 25 directions is; main test at L; Lightning hatched (○); 122B not run.*

### Does the split hold in other texts?

- **Question.** Does the split hold in other texts?
- **Why we asked.** The main test is one template; the split could belong to that layout rather than to the two readers.
- **Data.** Varied scenes, {{dp|catalogue|9b|varied scenes: scenes used (prose, JSON and table)}} / {{dp|catalogue|27b|varied scenes: scenes used (prose, JSON and table)}} / {{dp|catalogue|muse|varied scenes: scenes used (prose, JSON and table)}} / {{dp|catalogue|nemotron-3.5-lightning|varied scenes: scenes used (prose, JSON and table)}} / {{num|x0b_n_122b}}; natural passages, {{dp|catalogue|9b|natural passages: scenes eligible}} / {{dp|catalogue|27b|natural passages: scenes eligible}} / {{dp|catalogue|muse|natural passages: scenes eligible}} / {{dp|catalogue|nemotron-3.5-lightning|natural passages: scenes eligible (below gate)}} / {{dp|catalogue|122b|natural passages: scenes eligible}} (the figure shows the {{dp|catalogue|9b|natural passages: scenes used (fact first)}} / {{dp|catalogue|27b|natural passages: scenes used (fact first)}} / {{dp|catalogue|muse|natural passages: scenes used (fact first)}} whose fact comes first); the 9B's natural gate was lowered after the data; Lightning's natural passages miss the gate.
- **Method.** The conflict test unchanged, at L: without the lens part; control: without a random part.
- **Rule, fixed in advance.** Varied scenes, pooled: "holds if the lookup loses at most 0.10 beyond random (upper bound at most 0.20) and the gap is at least 0.20 (lower bound at least 0.10); fails if the lookup loses at least 0.20." Natural passages: "holds if the gap is at least 0.30 with its lower bound at least 0.15; fails at 0.10 or below; otherwise mixed."
- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | varied: lookup, switches lost beyond a random part | {{num|x0b_lk_excess_9b}} | {{num|x0b_lk_excess_27b}} | {{num|x0b_lk_excess_muse}} | {{d|cards|nemotron-3.5-lightning|varied: lookup, switches lost beyond a random part}} | {{num|x0b_lk_excess_122b}} |
  | varied: the gap | {{num|x0b_c_9b}} | {{num|x0b_c_27b}} | {{num|x0b_c_muse}} | {{d|cards|nemotron-3.5-lightning|varied: the gap}} | {{num|x0b_c_122b}} |
  | varied: the rule | {{num|x0b_verdict_9b}} | {{num|x0b_verdict_27b}} | {{num|x0b_verdict_muse}} | {{dp|cards|nemotron-3.5-lightning|varied: the rule}} | {{num|x0b_verdict_122b}} |
  | natural: recall, switches lost beyond a random part | {{num|natg75_rc_excess_9b}} | {{num|nat_rc_excess_27b}} | {{num|nat_rc_excess_muse}} | {{d|cards|nemotron-3.5-lightning|natural (below gate): recall, switches lost beyond a random part}} (below gate) | {{num|nat_rc_excess_122b}} |
  | natural: lookup, switches lost beyond a random part | {{num|natg75_lk_excess_9b}} | {{num|nat_lk_excess_27b}} | {{num|nat_lk_excess_muse}} | {{d|cards|nemotron-3.5-lightning|natural (below gate): lookup, switches lost beyond a random part}} (below gate) | {{num|nat_lk_excess_122b}} |
  | natural: the rule | after the data | {{num|nat_label_27b}} | {{num|nat_label_muse}} | not tested (gate); descriptive gap {{d|cards|nemotron-3.5-lightning|natural (below gate): the gap}} | {{num|nat_label_122b}} |

- **Read.**
  - In prose, JSON and tables the recall follows the lens part and the lookup does not, on the 9B, 27B, Muse and Lightning; on the 122B the lookup does not either, but the recall's lead is below the rule's bar, so the split is mixed there.
  - In natural passages the recall follows it on all five; the 27B's lookup follows it too, so there the split is mixed.
- **Caveats.**
  - In natural passages few lookups switch on Muse ({{num|nat_lk_whole_sw_muse}} under the whole change), and the figure leaves the 9B's and Muse's lookup cells out.
  - The 9B's natural run had its gate lowered after the data; Lightning's misses its gate, so its natural numbers are descriptive only.

![The split carries over to other texts](figures/story/fig09a_transfer.png)
*Switches lost without the lens part beyond a random part, by text format, for the recall and the lookup; "simple scenes" are the scenes the address was fit on; natural passages with the fact first; the 122B fifth; hollow: the 9B's lowered gate; grey band: the lookup's 0.10 bar.*

### Does each part, added by itself, move its reader?

- **Question.** Does each part, added by itself, move its reader?
- **Why we asked.** The conflict test takes a part away; a reader that follows a part should also move when only that part is added.
- **Data.** Main test, the scenes whose locker sentences come before the picks: {{dp|dose_rules|9b|dose curves: main-test scenes, locker sentences first}} / {{dp|dose_rules|27b|dose curves: main-test scenes, locker sentences first}} / {{dp|dose_rules|muse|dose curves: main-test scenes, locker sentences first}} / {{dp|dose_rules|nemotron-3.5-lightning|dose curves: main-test scenes, locker sentences first}} ○.
- **Method.** At the bridge word at L, on the original prompt:
  - the lens part alone at doses from 0.5 to 3; control: a random part of the same share at the same dose;
  - the rest alone at doses from 0.25 to 1.5; control: the change without a random part of the lens part's share;
  - the rest without the address; control: the rest without a random part of the address's share;
  - each dose's plain-text loss at the bridge word is checked against twice the whole change's; no dose passed it.
- **Rule, fixed in advance.** "(i) The lookup is blind to the lens part: switches minus random at most 0.10 at every dose whose plain-text loss stays under twice the whole change's, on all three. (ii) The recall reads the lens part above its share: at the first dose where the lens part alone switches at least 0.3, minus random at least 0.2, per model. (iii) Together only (Muse): the whole change at least 0.8 while the best single part stays at most 0.3."
- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | recall: lens part alone minus random, at dose 1.5 | {{d|fig16_dose|9b|51.1 A: recall switches with the J++ part by itself at dose 1.5, minus a random part (same size) at the same dose}} | {{d|fig16_dose|27b|51.1 A: recall switches with the J++ part by itself at dose 1.5, minus a random part (same size) at the same dose}} | {{d|fig16_dose|muse|51.1 A: recall switches with the J++ part by itself at dose 1.5, minus a random part (same size) at the same dose}} | {{d|fig16_dose|nemotron-3.5-lightning|51.1 A: recall switches with the J++ part by itself at dose 1.5, minus a random part (same size) at the same dose}} | not run |
  | recall: the same at dose 3 | {{d|fig16_dose|9b|51.1 A: recall switches with the J++ part by itself at dose 3, minus a random part (same size) at the same dose}} | {{d|fig16_dose|27b|51.1 A: recall switches with the J++ part by itself at dose 3, minus a random part (same size) at the same dose}} | {{d|fig16_dose|muse|51.1 A: recall switches with the J++ part by itself at dose 3, minus a random part (same size) at the same dose}} | {{d|fig16_dose|nemotron-3.5-lightning|51.1 A: recall switches with the J++ part by itself at dose 3, minus a random part (same size) at the same dose}} | not run |
  | lookup: lens part alone minus random, at dose 3 | {{d|fig16_dose|9b|51.1 A: lookup switches with the J++ part by itself at dose 3, minus a random part (same size) at the same dose}} | {{d|fig16_dose|27b|51.1 A: lookup switches with the J++ part by itself at dose 3, minus a random part (same size) at the same dose}} | {{d|fig16_dose|muse|51.1 A: lookup switches with the J++ part by itself at dose 3, minus a random part (same size) at the same dose}} | {{d|fig16_dose|nemotron-3.5-lightning|51.1 A: lookup switches with the J++ part by itself at dose 3, minus a random part (same size) at the same dose}} | not run |
  | (i) the lookup is blind to the lens part | {{dp|dose_rules|9b|(i) the lookup is blind to the J++ part}} | {{dp|dose_rules|27b|(i) the lookup is blind to the J++ part}} | {{dp|dose_rules|muse|(i) the lookup is blind to the J++ part}} | {{dp|dose_rules|nemotron-3.5-lightning|(i) the lookup is blind to the J++ part}} | not run |
  | (ii) the recall reads it above its share | {{dp|dose_rules|9b|(ii) the recall reads the J++ part above its share}} | {{dp|dose_rules|27b|(ii) the recall reads the J++ part above its share}} | {{dp|dose_rules|muse|(ii) the recall reads the J++ part above its share}} | {{dp|dose_rules|nemotron-3.5-lightning|(ii) the recall reads the J++ part above its share}} | not run |
  | lookups switched by the rest alone, dose 1 | {{d|fig16_dose|9b|51.1 B: lookups switched, the rest by itself, dose 1}} | {{d|fig16_dose|27b|51.1 B: lookups switched, the rest by itself, dose 1}} | {{d|fig16_dose|muse|51.1 B: lookups switched, the rest by itself, dose 1}} | {{d|fig16_dose|nemotron-3.5-lightning|51.1 B: lookups switched, the rest by itself, dose 1}} | not run |
  | the same without the address | {{d|fig16_dose|9b|51.1 B: lookups switched, the rest by itself without the address, dose 1}} | {{d|fig16_dose|27b|51.1 B: lookups switched, the rest by itself without the address, dose 1}} | {{d|fig16_dose|muse|51.1 B: lookups switched, the rest by itself without the address, dose 1}} | {{d|fig16_dose|nemotron-3.5-lightning|51.1 B: lookups switched, the rest by itself without the address, dose 1}} | not run |
  | the same without a random part of the address's share | {{d|fig16_dose|9b|51.1 B: lookups switched, the rest by itself without a random part of the address's share, dose 1}} | {{d|fig16_dose|27b|51.1 B: lookups switched, the rest by itself without a random part of the address's share, dose 1}} | {{d|fig16_dose|muse|51.1 B: lookups switched, the rest by itself without a random part of the address's share, dose 1}} | {{d|fig16_dose|nemotron-3.5-lightning|51.1 B: lookups switched, the rest by itself without a random part of the address's share, dose 1}} | not run |

  Rule (iii) on Muse: {{dp|dose_rules|muse|(iii) together only}}.
- **Read.**
  - Added by itself, the lens part moves the recall more than a random part of its size does, on the 9B, 27B and Muse; on Lightning only at middle doses, and its rule (ii) says no.
  - It moves the 9B's, Muse's and Lightning's lookups no more than random; the 27B's lookup moves a little at the highest dose.
  - The rest by itself moves the lookup; on the 9B, Muse and Lightning most of that goes when the address is removed from it, far more than with a random part.
- **Caveats.**
  - At high doses random parts switch readers too, so a negative lookup value means the random part moved it more, not that the lens part pushes back.
  - On the 27B, removing the address from the rest costs no more than removing a random part of its share.
  - One layer, and only scenes whose lockers come first.

![By itself the lens part moves the recall; the rest moves the lookup](figures/story/fig16_dose.png)
*Left: switches with the lens part alone minus a random part of the same size, by dose; rings mark the dose rule (ii) reads. Right: lookups switched by the rest alone, without the address, and without a random part. Rows: 9B, 27B, Muse, Lightning (hollow); 122B not run.*

### Does the recall need the lens part, or only follow it?

- **Question.** Does the recall need the lens part, or only follow it?
- **Why we asked.** The conflict test says the recall follows the lens part; following is not the same as needing it.
- **Data.** Zeroing: main test, {{num|n_9b}} / {{num|n_27b}} / {{num|n_muse}} / {{dp|catalogue|nemotron-3.5-lightning|main test: scenes used}} scenes. The ladder: clean one-pick scenes, {{dp|catalogue|9b|clean one-pick scenes: scenes used}} / {{dp|catalogue|27b|clean one-pick scenes: scenes used}} / {{dp|catalogue|muse|clean one-pick scenes: scenes used}}, every step from the full reruns (the 27B's first run had the first two steps; Muse's sixth step ran again inside Zach's layer band); Lightning's ladder ran below gate (its clean one-pick recall misses the gate): descriptive only, no rule label.
- **Method.** In the changed prompt's own run, nothing added, the lens part's directions are taken out, each step against a random part with the same share of the state:
  - zeroing, the ladder's first step: at the bridge word at L;
  - second step: at the bridge word over L to L+3;
  - third: also at the item's earlier mention, in its locker sentence;
  - fourth: also at the question's tokens;
  - fifth: at every token over L to L+3;
  - sixth, Zach's definition: at every token, each token's own top-10 lens directions over his layers.
- **Rule, fixed in advance.** Zeroing: "followed, not needed at one layer if the recall keeps at least 0.80 of its answers, within 0.10 of the random arm; needed if it loses at least 0.30 beyond random." The ladder: "(a) the second copy is the earlier mention: the third step costs the recall at least 0.3 more than the second where the locker comes first, and the second already costs at least 0.3 where it comes after; (b) needed only when everything goes: steps one to four each at most 0.2, and the fifth or sixth at least 0.5; (c) the lookup never needs it: at most 0.1 beyond random at every step."
- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | zeroing: recall answers lost beyond random | {{d|fig01c|9b|47.5: recall's answers kept, random part minus J++ part taken out (L)}} | {{d|fig01c|27b|47.5: recall's answers kept, random part minus J++ part taken out (L)}} | {{d|fig01c|muse|47.5: recall's answers kept, random part minus J++ part taken out (L)}} | {{d|cards|nemotron-3.5-lightning|47.5: recall's answers lost beyond random (L)}} | not run |
  | zeroing: the rule | {{dp|fig01c|9b|47.5: the rule's reading (recall at L)}} | {{dp|fig01c|27b|47.5: the rule's reading (recall at L)}} | {{dp|fig01c|muse|47.5: the rule's reading (recall at L)}} | {{dp|cards|nemotron-3.5-lightning|47.5: the rule's reading (recall at L)}} | not run |
  | recall, locker first, second step | {{d|fig01d|9b|rung 2: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|27b|rung 2: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|muse|rung 2: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|nemotron-3.5-lightning|rung 2: recall, locker before the pick: answers lost beyond random}} below gate | not run |
  | recall, locker first, third step | {{d|fig01d|9b|rung 3: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|27b|rung 3: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|muse|rung 3: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|nemotron-3.5-lightning|rung 3: recall, locker before the pick: answers lost beyond random}} below gate | not run |
  | recall, locker after, second step | {{d|fig01d|9b|rung 2: recall, locker after the pick: answers lost beyond random}} | {{d|fig01d|27b|rung 2: recall, locker after the pick: answers lost beyond random}} | {{d|fig01d|muse|rung 2: recall, locker after the pick: answers lost beyond random}} | {{d|fig01d|nemotron-3.5-lightning|rung 2: recall, locker after the pick: answers lost beyond random}} below gate | not run |
  | recall, locker first, fifth step | {{d|fig01d|9b|rung 5: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|27b|rung 5: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|muse|rung 5: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|nemotron-3.5-lightning|rung 5: recall, locker before the pick: answers lost beyond random}} below gate | not run |
  | recall, locker first, sixth step (Zach's definition) | {{d|fig01d|9b|rung 6: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|27b|rung 6: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|muse|rung 6: recall, locker before the pick: answers lost beyond random}} | {{d|fig01d|nemotron-3.5-lightning|rung 6: recall, locker before the pick: answers lost beyond random}} below gate | not run |
  | (a) the second copy is the earlier mention | {{dp|ladder_rules|9b|the second copy is the earlier mention}} | {{dp|ladder_rules|27b|the second copy is the earlier mention}} | {{dp|ladder_rules|muse|the second copy is the earlier mention}} | not tested (gate) | not run |
  | (b) needed only when everything goes | {{dp|ladder_rules|9b|needed only when everything goes}} | {{dp|ladder_rules|27b|needed only when everything goes}} | {{dp|ladder_rules|muse|needed only when everything goes}} | not tested (gate) | not run |
  | (c) the lookup never needs it | {{dp|ladder_rules|9b|the lookup never needs it}} | {{dp|ladder_rules|27b|the lookup never needs it}} | {{dp|ladder_rules|muse|the lookup never needs it}} | not tested (gate) | not run |

- **Read.**
  - At one layer the recall keeps nearly all its answers: it follows the lens part without needing it there.
  - Over four layers and at the earlier mention the 9B's recall loses many answers; where the locker comes first, the earlier mention holds the second copy. The 27B's recall loses answers step by step too, but its earlier mention stays below the rule's bar.
  - On Muse every step costs less, and Zach's definition, inside his band, costs little.
  - The lookup never needs the lens part.
- **Caveats.**
  - Rule (b) fails on every model: the recall's loss grows step by step rather than appearing only when everything goes.
  - Lightning's ladder is below gate: its steps are shown, its rules are not tested.

![Recall needs the lens part once its other copies go; the lookup never](figures/story/fig01d_ladder.png)
*Answers lost beyond a random part as the lens part's directions are taken out of the changed prompt, step by step; the recall split by sentence order, the lookup over every scene; ticks: what the random part itself costs; Lightning below gate, hollow; 122B not run.*

### Does the recall also read the item's earlier mention?

- **Question.** Does the recall also read the item's earlier mention?
- **Why we asked.** The ladder's third step points to a second copy where the locker sentence comes first; the earlier mention is the item's own word there.
- **Data.** Clean one-pick scenes whose new item's locker sentence comes before the asked pick: {{num|x45p_n_9b}} / {{num|x45p_n_27b}} / {{num|x45p_n_muse}}; Lightning below gate (its clean one-pick recall misses the gate), descriptive only.
- **Method.** At L, on the original prompt:
  - (1) the change without its lens part at the bridge word, as in the conflict test;
  - (2) (1), and the new item's tokens in its locker sentence without their own lens part;
  - (3) (1), and the same tokens without a random part of the same share: the control for (2);
  - (4) (1), and another item's tokens without their lens part: the control for the item.
- **Rule, fixed in advance.** "The recall reads the earlier mention if its switch loss in (2) exceeds (3) by at least 0.2 and (4) by at least 0.15, on at least two of three models; a model whose (1) switches fewer than 30 recalls is not tested." A loss is one minus the switches under the arm over those under (1).
- **Result.**

  | | 9B | 27B | Muse | Lightning ○ below gate | 122B |
  |---|---|---|---|---|---|
  | recalls switched under (1) | {{dp|fig03c|9b|45p, (1): recalls switched}} | {{dp|fig03c|27b|45p, (1): recalls switched}} | {{dp|fig03c|muse|45p, (1): recalls switched}} | {{dp|fig03c|nemotron-3.5-lightning|45p, (1): recalls switched}} | not run |
  | recall: loss in (2) minus (3) | {{num|x45p_d23_9b}} | {{num|x45p_d23_27b}} | {{num|x45p_d23_muse}} | {{d|cards|nemotron-3.5-lightning|45p (below gate): recall, loss in (2) minus (3)}} | not run |
  | recall: loss in (2) minus (4) | {{num|x45p_d24_9b}} | {{num|x45p_d24_27b}} | {{num|x45p_d24_muse}} | {{d|cards|nemotron-3.5-lightning|45p (below gate): recall, loss in (2) minus (4)}} | not run |
  | lookup: loss in (2) | {{d|fig03c|9b|45p, a2: lookup switches lost against (1)}} | {{d|fig03c|27b|45p, a2: lookup switches lost against (1)}} | {{d|fig03c|muse|45p, a2: lookup switches lost against (1)}} | {{d|fig03c|nemotron-3.5-lightning|45p, a2: lookup switches lost against (1)}} | not run |

  The rule holds on {{num|x45p_held}} models; Lightning is not tested (gate), its numbers descriptive only.
- **Read.**
  - The recall reads the item's lens part at its earlier mention as well as at the bridge word, on all three models; Lightning's numbers, below gate, point the same way.
  - The same removal at another item's mention costs nothing, so the effect belongs to the item.
  - The lookup does not read the earlier mention this way.
- **Caveats.**
  - Only scenes with the locker first; after the pick there is no earlier mention.
  - Few recalls switch under (1) on the 27B and Muse, so their intervals are wide.
  - Zeroing finds a weaker second copy on Muse (previous card): the two operations disagree in size there.

![The recall reads the item's earlier mention when its locker came first](figures/story/fig03c_earlier_mention.png)
*Recall and lookup switches lost against arm (1), per arm; clean one-pick scenes with the locker first; whiskers: {{q|95%}} intervals; 9B, 27B, Muse; Lightning below gate, hollow; 122B not run.*

## Part II. Identity: which item the lookup reads

*"Which item" is lens-readable for the recall, and the lookup's copy of it sits outside the lens.*

### Does the lookup's identity route run outside the lens?

- **Question.** Does the lookup's identity route run outside the lens?
- **Why we asked.** The lookup barely needs the lens part's 25 directions; its identity route could still sit in the lens's next 75 directions rather than outside the lens.
- **Data.** Routes scenes (another item moved), {{dp|catalogue|9b|routes scenes: scenes used}} / {{dp|catalogue|27b|routes scenes: scenes used}} / {{dp|catalogue|muse|routes scenes: scenes used}} / {{dp|catalogue|nemotron-3.5-lightning|routes scenes: scenes used}} per model, for the lookup's answers; the main test for the recall's switches. The 122B not run.
- **Method.** The change's 100 best lens directions in order; directions 1-25 (the lens part), 26-100 or all 100 taken out of the change at the bridge word at L, each against a random part of the same share. Read: the identity-route and position-route answers lost beyond random, and the recall's switches lost without directions 26-100.
- **Rule, fixed in advance.** "(a) 'the lookup's identity route sits in lens directions beyond the recall's 25': without 26-100, identity answers fall at least 0.30 beyond the random part (paired interval excluding 0) and the recall loses at most 0.10 of its switches beyond random without 26-100, on at least 2 of 3 models; (b) 'continuum': both readers lose at least 0.20 beyond random without 26-100; (c) 'outside the lens': without 26-100, identity answers fall under 0.10 beyond random." Lightning: the same rule, copied, no prediction.

![The lookup's identity route runs outside the lens; the position route never touches it](figures/story/fig05d_routes_lens.png)
*Identity-route and position-route answers lost without lens directions 1-25, 26-100 and all 100, beyond a random part of the same size, per model; routes scenes at L; Lightning hollow; 122B not run.*

- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | identity answers lost beyond random without lens directions 1-25 | {{d|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 1-25}} | {{d|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 1-25}} | {{d|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 1-25}} | {{d|fig05d|nemotron-3.5-lightning|47.1: identity route: answers lost beyond random without lens directions 1-25}} | not run |
  | the same without directions 26-100 | {{d|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 26-100}} | {{d|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 26-100}} | {{d|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 26-100}} | {{d|fig05d|nemotron-3.5-lightning|47.1: identity route: answers lost beyond random without lens directions 26-100}} | |
  | the same without all 100 | {{d|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 1-100}} | {{d|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 1-100}} | {{d|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 1-100}} | {{d|fig05d|nemotron-3.5-lightning|47.1: identity route: answers lost beyond random without lens directions 1-100}} | |
  | recall: switches lost beyond random without directions 26-100 (main test) | {{d|cards|9b|47.1: recall, switches lost beyond random without lens directions 26-100 (main test)}} | {{d|cards|27b|47.1: recall, switches lost beyond random without lens directions 26-100 (main test)}} | {{d|cards|muse|47.1: recall, switches lost beyond random without lens directions 26-100 (main test)}} | {{d|cards|nemotron-3.5-lightning|47.1: recall, switches lost beyond random without lens directions 26-100 (main test)}} | |
  | the rule | {{dp|cards|9b|47.1: the rule's label}} | {{dp|cards|27b|47.1: the rule's label}} | {{dp|cards|muse|47.1: the rule's label}} | {{dp|cards|nemotron-3.5-lightning|47.1: the rule's label}} | |

  The position route loses at most {{dp|fig05d||47.1: position route: the most answers lost beyond random, over the models and slices}} beyond random, over every model and slice.

- **Read.**
  - On all four models the identity route survives the loss of the lens's next directions: it runs outside the lens, not in lens directions beyond the recall's.
  - Only the 27B loses identity answers to the lens part itself or to all the directions together: there the slices are redundant copies.
  - The position route does not depend on any slice of the lens.
- **Caveats.**
  - Identity is read on routes scenes, the recall's switches on the main test: two scene sets.
  - Lightning's gate was chosen after its pre-check (○).
  - Not shown: the identity code itself.

### Which route does the lookup take: the item's identity, its locker's position, or the number?

- **Question.** Which route does the lookup take: the item's identity, its locker's position, or the number?
- **Why we asked.** The conflict test says the lookup follows the rest of the bridge word; the routes test says what in it the lookup reads.
- **Data.** Routes scenes, {{dp|catalogue|9b|routes scenes: scenes used}} / {{dp|catalogue|27b|routes scenes: scenes used}} / {{dp|catalogue|muse|routes scenes: scenes used}} / {{dp|catalogue|nemotron-3.5-lightning|routes scenes: scenes used}} / {{dp|catalogue|122b|routes scenes: scenes used}} per model. The 122B's routes run had its gate lowered to 0.75 after the data (hollow ○): its run at 0.80 missed the gate on the recall.
- **Method.** The change comes from a prompt where another item's locker sentence moved and took a new number, so each route predicts a different locker: the identity route the item's own locker, the position route the locker now at the item's old place, the value the new number. Arms at the bridge word at L: the whole change; without the address (Part III), against without a random part of its share. A sanity swap (two picks trade places, nothing moves) comes first.
- **Rule, fixed in advance.** "A route counts as used if its share is ≥ 0.20 with lower bound ≥ 0.10." The sanity swap must reproduce the one-pick lookup switch rate within 0.10; Lightning has no one-pick reference and takes Muse's rule (a switch rate of at least 0.50). Lightning and the 122B: the same rule, copied, no prediction.

![The lookup takes the identity route or the position route, never the value](figures/story/fig05_routes.png)
*Left: where each route sends the lookup, drawn on the setup figure's items (the routes test's own scenes are animals). Right: the lookup's answers under the whole change and without the address, per model; grey: without a random part of the same share. Lightning hollow; 122B hollow (gate lowered to 0.75 after the data; FP8).*

- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B ○ |
  |---|---|---|---|---|---|
  | whole change: identity route | {{d|fig05|9b|another item moved, whole: identity share}} | {{d|fig05|27b|another item moved, whole: identity share}} | {{d|fig05|muse|another item moved, whole: identity share}} | {{d|fig05|nemotron-3.5-lightning|another item moved, whole: identity share}} | {{d|fig05|122b|another item moved, whole: identity share}} |
  | whole change: position route | {{d|fig05|9b|another item moved, whole: position share}} | {{d|fig05|27b|another item moved, whole: position share}} | {{d|fig05|muse|another item moved, whole: position share}} | {{d|fig05|nemotron-3.5-lightning|another item moved, whole: position share}} | {{d|fig05|122b|another item moved, whole: position share}} |
  | whole change: the value | {{dp|fig05|9b|another item moved, whole: value share}} | {{dp|fig05|27b|another item moved, whole: value share}} | {{dp|fig05|muse|another item moved, whole: value share}} | {{dp|fig05|nemotron-3.5-lightning|another item moved, whole: value share}} | {{dp|fig05|122b|another item moved, whole: value share}} |
  | without the address: identity route | {{d|fig05|9b|another item moved, no_alf: identity share}} | {{d|fig05|27b|another item moved, no_alf: identity share}} | {{d|fig05|muse|another item moved, no_alf: identity share}} | {{d|fig05|nemotron-3.5-lightning|another item moved, no_alf: identity share}} | {{d|fig05|122b|another item moved, no_alf: identity share}} |
  | without the address: position route | {{d|fig05|9b|another item moved, no_alf: position share}} | {{d|fig05|27b|another item moved, no_alf: position share}} | {{d|fig05|muse|another item moved, no_alf: position share}} | {{d|fig05|nemotron-3.5-lightning|another item moved, no_alf: position share}} | {{d|fig05|122b|another item moved, no_alf: position share}} |
  | without a random part: position route | {{d|fig05|9b|another item moved, no_alf_rand: position share}} | {{d|fig05|27b|another item moved, no_alf_rand: position share}} | {{d|fig05|muse|another item moved, no_alf_rand: position share}} | {{d|fig05|nemotron-3.5-lightning|another item moved, no_alf_rand: position share}} | {{d|fig05|122b|another item moved, no_alf_rand: position share}} |

- **Read.**
  - On all five models the lookup answers by the item's identity or by its locker's position, never by the new number.
  - The 27B and the 122B lean on identity; the 9B, Muse and Lightning split about evenly.
  - Without the address the position route falls beyond a random part of its share; the identity route stays.
- **Caveats.**
  - The 122B (FP8; MoE, ~10B active): gate lowered to 0.75 after the data; its numbers are hollow and descriptive.
  - Lightning's gate was chosen after its pre-check (○); its sanity swap uses Muse's rule.
  - Not shown: what reads the position.

## Part III. The address: where the item's locker sits

*The lookup's second input is a code for where the locker sentence sits.*

### Can the address be read, removed, added and swapped?

- **Question.** Can the address be read, removed, added and swapped?
- **Why we asked.** If the bridge word stores where the item's locker sits, a probe should read it, removing it should cost position answers, adding it by itself should bring them back, and swapping it should send the lookup elsewhere.
- **Data.** The probe: every topic scene, split by whether the item's locker sentence comes before or after the pick. Removing and adding: the routes scenes ({{dp|catalogue|9b|routes scenes: scenes used}} per model). The swap: routes scenes without a move, each swapped to both other lockers.
- **Method.** At the bridge word at L:
  - the probe, held out by bridge entity: which locker sentence holds the item's locker, against the layout baseline; scenes with the locker after the pick are the control; the answer digit beside;
  - removing: the routes test without the address, against without a random part of its share; adding: only the address, against only a random part;
  - the swap: the difference between two lockers' mean address codes, at one, two and four times its size (s = 1, 2, 4), against a random vector of the same size; read: lookups sent to the swapped-in locker, and recalls that change.
- **Rule, fixed in advance.** Removing and adding: the routes test's, "a route counts as used if its share is ≥ 0.20 with lower bound ≥ 0.10". The swap: "at s = 1 the target share minus the random direction's ≥ 0.15 with lower bound > 0" (read at s = 1; see the caveats). The probe: none, descriptive, after the data. Lightning and the 122B: the same rules, copied, no prediction.

![The address carries the position route; swapping it moves the lookup](figures/story/fig07_writes.png)
*A: the probe at the bridge word, locker before the pick, against the layout baseline. B: position answers without the address and with only the address, against a random part of the same size (grey). C: lookups sent to the swapped-in locker by dose, against a random vector. Lightning hollow; 122B hollow in the removal, addition and swap panels (gate lowered to 0.75 after the data; FP8), filled in the probe panel.*

- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | probe, locker before the pick: which locker sentence | {{d|fig07|9b|the locker probe at the bridge word, locker-first scenes}} | {{d|fig07|27b|the locker probe at the bridge word, locker-first scenes}} | {{d|fig07|muse|the locker probe at the bridge word, locker-first scenes}} | {{d|fig07|nemotron-3.5-lightning|the locker probe at the bridge word, locker-first scenes}} | {{d|fig07|122b|the locker probe at the bridge word, locker-first scenes}} |
  | the layout baseline | {{dp|fig07|9b|the locker probe's layout baseline, locker-first scenes}} | {{dp|fig07|27b|the locker probe's layout baseline, locker-first scenes}} | {{dp|fig07|muse|the locker probe's layout baseline, locker-first scenes}} | {{dp|fig07|nemotron-3.5-lightning|the locker probe's layout baseline, locker-first scenes}} | {{dp|fig07|122b|the locker probe's layout baseline, locker-first scenes}} |
  | probe, locker after the pick (the control) | {{num|v4_b_after_9b}} | {{num|v4_b_after_27b}} | {{num|v4_b_after_muse}} | {{dp|cards|nemotron-3.5-lightning|address probe: the locker probe at the bridge word, locker-after scenes (the control)}} | {{num|v4_b_after_122b}} |
  | probe, locker before the pick: the answer digit | {{num|v4_a_before_9b}} | {{num|v4_a_before_27b}} | {{num|v4_a_before_muse}} | {{dp|cards|nemotron-3.5-lightning|address probe: the answer digit probe at the bridge word, locker-first scenes}} | {{num|v4_a_before_122b}} |
  | position answers without the address / without a random part | {{dp|fig05|9b|another item moved, no_alf: position share}} / {{dp|fig05|9b|another item moved, no_alf_rand: position share}} | {{dp|fig05|27b|another item moved, no_alf: position share}} / {{dp|fig05|27b|another item moved, no_alf_rand: position share}} | {{dp|fig05|muse|another item moved, no_alf: position share}} / {{dp|fig05|muse|another item moved, no_alf_rand: position share}} | {{dp|fig05|nemotron-3.5-lightning|another item moved, no_alf: position share}} / {{dp|fig05|nemotron-3.5-lightning|another item moved, no_alf_rand: position share}} | {{dp|fig05|122b|another item moved, no_alf: position share}} / {{dp|fig05|122b|another item moved, no_alf_rand: position share}} ○ |
  | position answers with only the address / with only a random part | {{dp|fig07|9b|another item moved, keep_alf: position share}} / {{dp|fig07|9b|another item moved, keep_alf_rand: position share}} | {{dp|fig07|27b|another item moved, keep_alf: position share}} / {{dp|fig07|27b|another item moved, keep_alf_rand: position share}} | {{dp|fig07|muse|another item moved, keep_alf: position share}} / {{dp|fig07|muse|another item moved, keep_alf_rand: position share}} | {{dp|fig07|nemotron-3.5-lightning|another item moved, keep_alf: position share}} / {{dp|fig07|nemotron-3.5-lightning|another item moved, keep_alf_rand: position share}} | {{dp|fig07|122b|another item moved, keep_alf: position share}} / {{dp|fig07|122b|another item moved, keep_alf_rand: position share}} ○ |
  | the swap at s = 1: lookups sent to the swapped-in locker (mean over locker pairs) | {{dp|fig07|9b|lookup target share, mean over locker pairs, s = 1}} | {{dp|fig07|27b|lookup target share, mean over locker pairs, s = 1}} | {{dp|fig07|muse|lookup target share, mean over locker pairs, s = 1}} | {{dp|fig07|nemotron-3.5-lightning|lookup target share, mean over locker pairs, s = 1}} | {{dp|fig07|122b|lookup target share, mean over locker pairs, s = 1}} ○ |
  | the swap at s = 2, about a real change's size (the same) | {{dp|fig07|9b|lookup target share, mean over locker pairs, s = 2}} | {{dp|fig07|27b|lookup target share, mean over locker pairs, s = 2}} | {{dp|fig07|muse|lookup target share, mean over locker pairs, s = 2}} | {{dp|fig07|nemotron-3.5-lightning|lookup target share, mean over locker pairs, s = 2}} | {{dp|fig07|122b|lookup target share, mean over locker pairs, s = 2}} ○ |
  | a random vector at s = 4 | {{dp|fig07|9b|lookup target share, random direction, s = 4}} | {{dp|fig07|27b|lookup target share, random direction, s = 4}} | {{dp|fig07|muse|lookup target share, random direction, s = 4}} | {{dp|fig07|nemotron-3.5-lightning|lookup target share, random direction, s = 4}} | {{dp|fig07|122b|lookup target share, random direction, s = 4}} ○ |
  | the swap at s = 2: recalls that change | {{dp|cards|9b|the address swap at s = 2: recalls that change}} | {{dp|cards|27b|the address swap at s = 2: recalls that change}} | {{dp|cards|muse|the address swap at s = 2: recalls that change}} | {{dp|cards|nemotron-3.5-lightning|the address swap at s = 2: recalls that change}} | {{dp|cards|122b|the address swap at s = 2: recalls that change}} ○ |
  | of those, naming the swapped-in item's answer | {{dp|cards|9b|the address swap at s = 2: changed recalls naming the swapped-in item's answer}} | not checked | not checked | {{dp|cards|nemotron-3.5-lightning|the address swap at s = 2: changed recalls naming the swapped-in item's answer}} | not checked |

  With 50 neutral sentences between the lockers and the picks, the 9B's swap at s = 2 still sends {{dp|e6_distance|9b|47.16: the swap (fit with none) sends lookups to the target, 50 sentences}} of lookups to the target.

- **Read.**
  - With its locker sentence before the pick, the bridge word holds which locker sentence the item's locker sits in, on all five models, far above the layout baseline; with the locker after the pick it does not.
  - Removing the address takes the position route away beyond a random part on every model; added by itself it brings position answers back on the 9B, Muse, Lightning and the 122B, not on the 27B.
  - At about a real change's size a swap sends a quarter to a half of lookups to the swapped-in locker on every model; a random vector sends none.
  - The address points to the item: the lookup always follows the swap, the recall sometimes, most on the 9B and Lightning.
- **Caveats.**
  - The swap's rule fixed in advance was read at s = 1 and said no on every model. That was a design error: s = 1 is below a real change's size; the swap numbers above are read at s = 2, after the data.
  - The probe is descriptive, chosen after the data; the answer digit is read only weakly.
  - The 122B (FP8; MoE, ~10B active): its routes and swap runs had their gate lowered to 0.75 after the data (hollow ○, descriptive); its probe ran at its gate.
  - Lightning's gate was chosen after its pre-check (○); its probe reads the locker sentence less well than the others'.
  - Not shown: what reads the address.

### With six lockers, does each locker have its own code?

- **Question.** With six lockers, does each locker have its own code?
- **Why we asked.** With three lockers a line over the lockers and a first-versus-rest marker look the same.
- **Data.** Six-locker scenes: a test half of {{dp|catalogue|9b|six-locker scenes: scenes used}} / {{dp|cards|27b|47.2: test scenes}} / {{dp|catalogue|muse|six-locker scenes: scenes used}} / {{dp|catalogue|nemotron-3.5-lightning|six-locker scenes: scenes used}} scenes per model; the other half fits the lockers' mean codes. The 122B not run. On the 9B, follow-ups with 3, 4, 6 and 8 lockers on held-out entities.
- **Method.** At the bridge word at L:
  - one fixed shift (the mean step between neighbouring lockers' mean codes) from each start locker, and swaps between given lockers, each at doses 1 and 2, against a random vector of the same size; the first principal component of the lockers' mean codes beside;
  - on the 9B: the smallest learned code that carries the position switch, per number of lockers, against random codes of the same size; swaps to the midpoint between two lockers, against full swaps.
- **Rule, fixed in advance.** "Ordinal: the first principal component is monotone in the locker (|Spearman| ≥ 0.9) and the shift sends ≥ 0.25 of lookups one locker on from ≥ 4 of 5 start lockers, the random vector ≤ 0.05; categorical, first vs rest: the shift works only from the first locker (others < 0.10) and removing the address on the other moves is within 0.10 of random; slot-specific: swaps between given lockers reach ≥ 0.25 on most pairs but no single shift does." Dose 2 decides. On the 9B: "one dimension per locker" if the learned code's size is at least the number of lockers minus 2 for every count and at least 5 at 8 lockers; "an ordinal code" if it is at most 2 up to 8 lockers; "categories" if midpoint swaps send < 0.1 to the midpoint locker while the full swaps reach ≥ 0.4 of the target; "a metric order" if midpoint swaps send ≥ 0.3 to the midpoint locker, from both ends. The 27B and Lightning: the same rule, copied, no prediction.

![Six lockers: swaps between given lockers work on most pairs, no single shift does](figures/story/fig09b_six_lockers.png)
*At dose 2, per model: start lockers from which one shift sends at least a quarter of lookups one locker on, and locker pairs that a swap between given lockers reaches; Lightning hollow; 122B not run.*

- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | swaps between given lockers reaching 0.25 of lookups at dose 2, of 30 pairs | {{dp|fig09b|9b|47.2: pairwise writes reaching 25% (dose 2)}} | {{dp|cards|27b|47.2: pairwise writes reaching 25% (dose 2)}} | {{dp|fig09b|muse|47.2: pairwise writes reaching 25% (dose 2)}} | {{dp|fig09b|nemotron-3.5-lightning|47.2: pairwise writes reaching 25% (dose 2)}} | not run |
  | the rule at dose 2 | {{dp|fig09b|9b|47.2: the rule's reading (dose 2)}} | {{dp|cards|27b|47.2: the rule's reading (dose 2)}} | {{dp|fig09b|muse|47.2: the rule's reading (dose 2)}} | {{dp|fig09b|nemotron-3.5-lightning|47.2: the rule's reading (dose 2)}} | |
  | the code's size, follow-up | {{dp|cards|9b|51.11 part 1: the code's size}} | | | | |
  | midpoint swaps reaching the locker between, from the first locker (dose 2) / full swaps reaching their target | {{dp|cards|9b|51.11 part 3: midpoint swaps reaching the slot between, from the first slot (dose 2)}} / {{dp|cards|9b|51.11 part 3: full swaps reaching their target (dose 2)}} | | | | |

- **Read.**
  - No single shift moves the lookup one locker on, on any model: the address is not a line over the lockers.
  - Swaps between given lockers work on most pairs on the 9B, Muse and Lightning, so each locker is its own target there; on the 27B on fewer than half, and no reading holds.
  - On the 9B the code's size is not settled, and midpoint swaps do not land between lockers: the lockers are not a metric order.
- **Caveats.**
  - The 27B's shifts move nothing from any start locker, though its lockers' mean codes lie in order.
  - The follow-ups are read here on the 9B only; Muse's and the 27B's runs of them are in the ledger.
  - Lightning's gate was chosen after its pre-check (○).
  - Not shown: whether the same code serves other kinds of item.

### Can the lens read the address?

- **Question.** Can the lens read the address?
- **Why we asked.** A lens monitor would have to see the address to see where the model will look.
- **Data.** Routes scenes, each swapped at the bridge word to both other lockers at about a real change's size; for each case 200 random vectors of the same size. The report prompt: the 27B's routes scenes, question last. The 122B not run.
- **Method.**
  - Through the lens after the swap: (a) the best rank of a position word (first, second, third, 1, 2, 3, ...) in the lens readout; (b) the share the lens's 25 best directions rebuild; (c) how far the readout moves; each against the random vectors; positive control: an item change of the same size.
  - The report prompt (27B): asked which locker sentence holds the item, the lens's top five at the bridge word, and the report's switches lost without the lens part and without the address, beyond random.
- **Rule, fixed in advance.** Descriptive, with the reading fixed in advance: "'not verbalizable': the share rebuilt with 25 lens directions within 2x the random vectors' share, no position word in the top 20 beyond the random vectors' 5th-percentile rank, and the readout's change under the swap within the random vectors' 95th percentile, on all three models." The report prompt: "'surfaced on demand': under the report prompt the lens ranks the right position word in its top five in ≥ 0.4 of items (under the lookup prompt ≤ 0.1), and the report loses ≥ 0.3 of its switches without the lens part beyond random"; else "reported late, not surfaced" or neither. Lightning: the reading copied, no prediction.

![The lens reads which item is at the bridge, not where its locker sits](figures/story/fig07b_verbal.png)
*How far above 200 random vectors of the same size the lens ranks a position word (left) and rebuilds the change with 25 directions (right), per model: the address swap and an item change of the same size; grey strip: the random vectors' range. Lightning hollow; 122B not run.*

- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | share rebuilt by 25 lens directions: the address swap | {{dp|fig07b_verbal|9b|47.0 (b) share rebuilt by 25 lens directions: pointer}} | {{dp|fig07b_verbal|27b|47.0 (b) share rebuilt by 25 lens directions: pointer}} | {{dp|fig07b_verbal|muse|47.0 (b) share rebuilt by 25 lens directions: pointer}} | {{dp|fig07b_verbal|nemotron-3.5-lightning|47.0 (b) share rebuilt by 25 lens directions: pointer}} | not run |
  | the same for random vectors (mean) | {{dp|fig07b_verbal|9b|47.0 (b) share rebuilt by 25 lens directions: random draws (mean; mean, 95th pct)}} | {{dp|fig07b_verbal|27b|47.0 (b) share rebuilt by 25 lens directions: random draws (mean; mean, 95th pct)}} | {{dp|fig07b_verbal|muse|47.0 (b) share rebuilt by 25 lens directions: random draws (mean; mean, 95th pct)}} | {{dp|fig07b_verbal|nemotron-3.5-lightning|47.0 (b) share rebuilt by 25 lens directions: random draws (mean; mean, 95th pct)}} | |
  | the same for an item change of the same size | {{dp|fig07b_verbal|9b|47.0 (b) share rebuilt by 25 lens directions: identity_mean}} | {{dp|fig07b_verbal|27b|47.0 (b) share rebuilt by 25 lens directions: identity_mean}} | {{dp|fig07b_verbal|muse|47.0 (b) share rebuilt by 25 lens directions: identity_mean}} | {{dp|fig07b_verbal|nemotron-3.5-lightning|47.0 (b) share rebuilt by 25 lens directions: identity_mean}} | |
  | a position word's rank after the swap, z (the random vectors: −1 to 1) | {{dp|fig07b_verbal|9b|47.0 (a) best ordinal word's rank, h + pointer write: z = (ln random median - ln median) / w (lo, hi: the random draws' 95% range in z)}} | {{dp|fig07b_verbal|27b|47.0 (a) best ordinal word's rank, h + pointer write: z = (ln random median - ln median) / w (lo, hi: the random draws' 95% range in z)}} | {{dp|fig07b_verbal|muse|47.0 (a) best ordinal word's rank, h + pointer write: z = (ln random median - ln median) / w (lo, hi: the random draws' 95% range in z)}} | {{dp|fig07b_verbal|nemotron-3.5-lightning|47.0 (a) best ordinal word's rank, h + pointer write: z = (ln random median - ln median) / w (lo, hi: the random draws' 95% range in z)}} | |
  | the new item's name rank after an item change, z | {{dp|fig07b_verbal|9b|47.0 (a) new item's name rank, h + identity change: z = (ln random median - ln median) / w (lo, hi: the random draws' 95% range in z)}} | {{dp|fig07b_verbal|27b|47.0 (a) new item's name rank, h + identity change: z = (ln random median - ln median) / w (lo, hi: the random draws' 95% range in z)}} | {{dp|fig07b_verbal|muse|47.0 (a) new item's name rank, h + identity change: z = (ln random median - ln median) / w (lo, hi: the random draws' 95% range in z)}} | {{dp|fig07b_verbal|nemotron-3.5-lightning|47.0 (a) new item's name rank, h + identity change: z = (ln random median - ln median) / w (lo, hi: the random draws' 95% range in z)}} | |
  | report prompt, question last: the lens's top five hold the right position word | not tested (gate) | {{dp|e8_report|27b|47.10: lens top-5 holds the right ordinal (report prompt)}} | not tested (gate) | not tested (gate) | |
  | the report's switches lost beyond random without the lens part / without the address | | {{dp|e8_report|27b|47.10: the report's extra loss without the J++ part}} / {{dp|e8_report|27b|47.10: the report's extra loss without the address}} | | | |

- **Read.**
  - On all four models the address swap reads through the lens like a random vector of its size: no position word, no more rebuilt, little change in the readout.
  - An item change of the same size stands far outside the random range: the lens reads which item is at the bridge, not where its locker sits.
  - Asked for the position, the 27B's lens still does not show it, and its report needs the address more than the lens part.
- **Caveats.**
  - Descriptive: the reading is the plan's, not a claim fixed in advance; it uses medians, and per case some readouts move beyond their own random range on the 9B and Muse.
  - Lightning rebuilds a little more of the swap than its random vectors ({{dp|cards|nemotron-3.5-lightning|47.0 (b) share rebuilt by 25 lens directions: pointer}} against {{dp|cards|nemotron-3.5-lightning|47.0 (b) share rebuilt by 25 lens directions: random draws (mean)}}), still a small share; its gate was chosen after its pre-check (○).
  - The report prompt: one cell tested (the 27B, question last); every other cell missed its gate. Its loss without the address is just under the rule's bar, so neither reading holds.

### Must the address be refit for each text format?

- **Question.** Must the address be refit for each text format?
- **Why we asked.** The address was fit on one template; in prose, JSON and tables the code may sit elsewhere.
- **Data.** The varied scenes (prose, JSON and tables), split in halves by bridge item: one half fits the address per format, the other half is tested. The 122B not run.
- **Method.** The address refit per format on one half (four directions) and taken out of the change at the bridge word at L on the other half, against a random part of its share; the address fit on the simple scenes beside.
- **Rule, fixed in advance.** "'Pointer elsewhere' if the refit address costs the lookup at least 0.2 of its switches beyond random, with lower bound above 0.1, in 2 of 3 formats; 'no linear pointer found' if all three formats are below 0.1 (point estimate); otherwise neither." After the data (Dan, 26 Oct): a format whose lookup has fewer than 30 switches under the whole change does not count. Lightning: the same rule, copied, no prediction.

![The address must be refit for each text format](figures/story/fig09b_refit.png)
*The lookup's switches lost without the address beyond a random part, by format: refit on the format (filled) and fit on the simple scenes (hollow); grey: the 0.10 bar. Lightning hollow; Muse's JSON left out (too few switches); 122B not run.*

- **Result.**

  | lookup's switches lost beyond random: refit / fit on the simple scenes | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | prose | {{dp|fig09b_refit|9b|(b) prose: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|9b|(b) prose: lookup extra loss without the pointer fit on simple scenes}} | {{dp|fig09b_refit|27b|(b) prose: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|27b|(b) prose: lookup extra loss without the pointer fit on simple scenes}} | {{dp|fig09b_refit|muse|(b) prose: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|muse|(b) prose: lookup extra loss without the pointer fit on simple scenes}} | {{dp|fig09b_refit|nemotron-3.5-lightning|(b) prose: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|nemotron-3.5-lightning|(b) prose: lookup extra loss without the pointer fit on simple scenes}} | not run |
  | JSON | {{dp|fig09b_refit|9b|(b) json: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|9b|(b) json: lookup extra loss without the pointer fit on simple scenes}} | {{dp|fig09b_refit|27b|(b) json: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|27b|(b) json: lookup extra loss without the pointer fit on simple scenes}} | too few switches ({{dp|fig09b_refit|muse|(b) json: lookup switches with the whole change}}) | {{dp|fig09b_refit|nemotron-3.5-lightning|(b) json: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|nemotron-3.5-lightning|(b) json: lookup extra loss without the pointer fit on simple scenes}} | |
  | tables | {{dp|fig09b_refit|9b|(b) table: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|9b|(b) table: lookup extra loss without the pointer fit on simple scenes}} | {{dp|fig09b_refit|27b|(b) table: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|27b|(b) table: lookup extra loss without the pointer fit on simple scenes}} | {{dp|fig09b_refit|muse|(b) table: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|muse|(b) table: lookup extra loss without the pointer fit on simple scenes}} | {{dp|fig09b_refit|nemotron-3.5-lightning|(b) table: lookup extra loss without the refit pointer}} / {{dp|fig09b_refit|nemotron-3.5-lightning|(b) table: lookup extra loss without the pointer fit on simple scenes}} | |
  | the outcome | {{num|x45d_outcome_9b}} | {{num|x45d_outcome_27b}} | {{num|x45d_outcome_muse}} | {{dp|cards|nemotron-3.5-lightning|45d: the outcome}} | |

- **Read.**
  - Refit on each format, the address carries the lookup again on the 9B, Muse and Lightning; on the 27B it stays weak in every format.
  - Fit on the simple scenes it costs the lookup little in JSON and tables: in other formats the code sits elsewhere.
- **Caveats.**
  - The bar of 30 switches was set after the first results; it drops Muse's JSON.
  - Lightning's JSON rests on few scenes; its gate was chosen after its pre-check (○).

### Is the address readable, and used, in Python code and tool output?

- **Question.** Is the address readable, and used, in Python code and tool output?
- **Why we asked.** Every other test reads the scene as prose; a model in an agent reads code and tool replies. If the address were a habit of prose, it would not show there.
- **Data.** The probe's scenes from the address card, rendered two ways: as Python in the user turn (`picks["Eva"] = "oxygen"`, `lockers["oxygen"] = 5`, one assignment per statement in the scene's order, then the question), and as the reply of a declared notes tool in the chat template, the question in a new user turn. Code keeps the scenes whose bridge is one token at one position in both prompts: {{dp|cards|27b|53.7, code: the probe's scenes (one token at one position in both prompts)}} scenes, {{dp|cards|27b|53.7, code: the probe's scenes, locker before the pick}} with the locker before the pick (27B); tool output keeps all {{dp|cards|27b|53.7, tool: the probe's scenes (one token at one position in both prompts)}} ({{dp|cards|27b|53.7, tool: the probe's scenes, locker before the pick}} with the locker before the pick). The routes test in code: {{dp|cards|9b|53.7, code: the routes test's items, another item moved}} / {{dp|cards|27b|53.7, code: the routes test's items, another item moved}} items, another item moved (9B / 27B). The 9B and the 27B; Muse, Lightning and the 122B not run.
- **Method.** Two of the address card's tests, unchanged, in each format, at L:
  - the probe at the bridge word: which locker sentence holds the bridge's locker, against the layout baseline; scenes with the locker after the pick are the control (the locker sentence comes later, so nothing can be read there);
  - the routes test, another item moved: the whole change; position answers without the address against without a random part of the same size, and with only the address against only a random part. The address is the one fit on the model's prose scenes, carried over to code, not refit<!-- src: results/x6_routes/qwen35_9b_x53_7_routes_code_l/manifest.json | alf_from :: qwen35_9b_x0_probe_v4 (scripts/x6_routes.py stage_run: x0_massmean on that run's states at L) --><!-- src: results/x6_routes/x53_7_routes_code_27b_l/manifest.json | alf_from :: x0_probe_v4_27b -->;
  - the lens monitor in both formats: running;
  - adapted design: lookup-only gate; the recall is not part of this test. A format is tested if the lookup answers and reads both prompts right on at least 0.80 of its scenes; the recall's rates are reported, not gated.
- **Rule, fixed in advance.** Pending hand-check. The routes test's, verbatim: "A route counts as used if its share is >= 0.2 with lower CI >= 0.1." The probe has no rule of its own (descriptive, after the data). The lookup-only gate was set before any result in these formats was opened, except the 9B's code probe: gate changed after the data (hollow ○). The 27B's probes ran under the earlier gate on both readers and passed it, so they pass either gate: adapted design. No prediction.

![Code and tool output: the address is readable; in code it carries less](figures/story/fig21_code_tool.png)
*A: the probe for the locker sentence at the bridge word, with the locker before the pick, against its layout baseline (hatched); the black tick: the same probe in prose. B: the routes test in code, another item moved, at L: position answers without the address and with only the address, each against a random part of the same size (grey). The 9B's code probe not tested (○); the 27B's probes under the earlier gate on both readers; cells still running and models not run keep their rows.*

- **Result.**

  | | 9B | 27B | Muse | Lightning | 122B |
  |---|---|---|---|---|---|
  | probe, locker before the pick: code | {{dp|fig21_code_tool|9b|code and tool output, code: the probe's status}} ○ | {{d|fig21_code_tool|27b|code and tool output, code: the locker probe at the bridge word, locker-first scenes}} (layout {{dp|fig21_code_tool|27b|code and tool output, code: the locker probe's layout baseline, locker-first scenes}}) | not run | not run | not run |
  | probe, locker before the pick: tool output | {{d|fig21_code_tool|9b|code and tool output, tool: the locker probe at the bridge word, locker-first scenes}} (layout {{dp|fig21_code_tool|9b|code and tool output, tool: the locker probe's layout baseline, locker-first scenes}}) | {{d|fig21_code_tool|27b|code and tool output, tool: the locker probe at the bridge word, locker-first scenes}} (layout {{dp|fig21_code_tool|27b|code and tool output, tool: the locker probe's layout baseline, locker-first scenes}}) | | | |
  | the same probe in prose | {{dp|fig21_code_tool|9b|code and tool output, tool: the locker probe in prose, locker-first scenes (stored)}} | {{dp|fig21_code_tool|27b|code and tool output, tool: the locker probe in prose, locker-first scenes (stored)}} | | | |
  | control, locker after the pick: probe / best baseline, tool output | {{dp|cards|9b|53.7, tool: the probe, locker sentence, locker-after scenes (the control)}} / {{dp|cards|9b|53.7, tool: the probe's best baseline (structure), locker sentence, locker-after scenes (the control)}} | {{dp|cards|27b|53.7, tool: the probe, locker sentence, locker-after scenes (the control)}} / {{dp|cards|27b|53.7, tool: the probe's best baseline (structure), locker sentence, locker-after scenes (the control)}} | | | |
  | control, locker after the pick: probe / best baseline, code | | {{dp|cards|27b|53.7, code: the probe, locker sentence, locker-after scenes (the control)}} / {{dp|cards|27b|53.7, code: the probe's best baseline (majority), locker sentence, locker-after scenes (the control)}} | | | |
  | the answer digit at the bridge word, locker before the pick: probe / chance, tool output | {{dp|cards|9b|53.7, tool: the probe, answer digit, locker-first scenes}} / {{dp|cards|9b|53.7, tool: chance, answer digit, locker-first scenes}} | {{dp|cards|27b|53.7, tool: the probe, answer digit, locker-first scenes}} / {{dp|cards|27b|53.7, tool: chance, answer digit, locker-first scenes}} | | | |
  | the probe's gate | lookup only: code {{dp|cards|9b|53.7, code: the probe's gate, the lookup says and reads both prompts right}}, tool output {{dp|cards|9b|53.7, tool: the probe's gate, the lookup says and reads both prompts right}} | earlier design, both readers (lookup / recall): code {{dp|cards|27b|53.7, code: the probe's gate (earlier design), lookup / recall read right}}, tool output {{dp|cards|27b|53.7, tool: the probe's gate (earlier design), lookup / recall read right}} | | | |
  | routes, code, the whole change: identity / position / value | {{dp|cards|9b|53.7, code: another item moved, the whole change: identity share}} / {{dp|cards|9b|53.7, code: another item moved, the whole change: position share}} / {{dp|cards|9b|53.7, code: another item moved, the whole change: value share}} | {{dp|cards|27b|53.7, code: another item moved, the whole change: identity share}} / {{d|cards|27b|53.7, code: another item moved, the whole change: position share}} / {{dp|cards|27b|53.7, code: another item moved, the whole change: value share}} | | | |
  | routes, code: the routes the rule counts as used | {{dp|cards|9b|53.7, code: another item moved, the whole change: the routes the rule counts as used}} | {{dp|cards|27b|53.7, code: another item moved, the whole change: the routes the rule counts as used}} | | | |
  | routes, code: position answers without the address / without a random part | {{d|fig21_code_tool|9b|code and tool output, code: another item moved, no_alf: position share}} / {{d|fig21_code_tool|9b|code and tool output, code: another item moved, no_alf_rand: position share}} | {{d|fig21_code_tool|27b|code and tool output, code: another item moved, no_alf: position share}} / {{d|fig21_code_tool|27b|code and tool output, code: another item moved, no_alf_rand: position share}} | | | |
  | routes, code: position answers with only the address / with only a random part | {{d|fig21_code_tool|9b|code and tool output, code: another item moved, keep_alf: position share}} / {{dp|fig21_code_tool|9b|code and tool output, code: another item moved, keep_alf_rand: position share}} | {{d|fig21_code_tool|27b|code and tool output, code: another item moved, keep_alf: position share}} / {{dp|fig21_code_tool|27b|code and tool output, code: another item moved, keep_alf_rand: position share}} | | | |
  | routes, code: the gate (lookup only) / the recall read right, not gated | {{dp|cards|9b|53.7, code: the routes test's gate, another item moved (lookup-only)}} / {{dp|cards|9b|53.7, code: the routes test, the recall's read right (descriptive)}} | {{dp|cards|27b|53.7, code: the routes test's gate, another item moved (lookup-only)}} / {{dp|cards|27b|53.7, code: the routes test, the recall's read right (descriptive)}} | | | |
  | routes, tool output | {{dp|fig21_code_tool|9b|code and tool output, tool: the routes test's status (another item moved)}} | {{dp|fig21_code_tool|27b|code and tool output, tool: the routes test's status (another item moved)}} | | | |
  | in prose (the address card): position answers without the address / without a random part / with only the address | {{pt|rt_C2_no_alf_position_9b}} / {{pt|rt_C2_no_alf_rand_position_9b}} / {{pt|rtk_C2_keep_alf_position_9b}} | {{pt|rt_C2_no_alf_position_27b}} / {{pt|rt_C2_no_alf_rand_position_27b}} / {{pt|rtk_C2_keep_alf_position_27b}} | | | |
  | the lens monitor, code and tool output | running | running | | | |

- **Read.**
  - In tool output on the 9B and the 27B, and in code on the 27B, the probe at the bridge word reads which locker sentence holds the bridge's locker as well as in prose, far above the layout baseline; with the locker after the pick it reads nothing beyond its baselines.
  - In code both models' lookups take the identity route or the position route, never the value; without the address they lose position answers beyond a random part of the same size, though less than in prose, and the address by itself brings almost none back.
  - The address is readable in both formats and used in code; whether the lookup uses it in tool output waits for the routes runs still going.
- **Caveats.**
  - Pending hand-check: today's runs, unverified until hand-checked.
  - Adapted design: lookup-only gate; the recall is not part of this test. The 9B's code probe: gate changed after the data (hollow ○); it fails that gate too. The 27B's probes passed the earlier gate on both readers.
  - The address removed and added in code is the one fit on prose, carried over, not refit.
  - Tool output is prose inside a tool reply; JSON is covered by the varied scenes ("Does the split hold in other texts?", Part I).
  - In the tool format the bridge word sits about 250 tokens later than in prose<!-- src: results/x0_probe/x53_7_probe-20261029T115640Z/verdict.md | the bridge ~250 tokens later in the tool format --> (the template's tools block and two turns come first), not separated from the format; on the 9B the address stays readable after 50 neutral sentences (probe {{dp|e6_distance|9b|47.16: slot probe with 50 neutral sentences}}).
  - The probe only shows the address is readable; the routes test decides whether the lookup uses it.
  - The code scenes keep only the domains whose names stay one token at one position, so their mix differs from prose.

## Part IV. Where and when the link is made

*The bridge word can only point back, so the order decides where the link is made, and the address is written early and used late.*

### Does the bridge word redirect the lookup only when its locker sentence came first?

- **Question.** Does the bridge word redirect the lookup only when its locker sentence came first?
- **Why we asked.** The bridge word can only point back: if the item's locker sentence comes after the pick, the link must be made somewhere else.
- **Data.** Main test, {{num|n_9b}} / {{num|n_27b}} / {{num|n_muse}} / {{dp|catalogue|nemotron-3.5-lightning|main test: scenes used}} / {{num|n_122b}} scenes per model, split by where the asked item's locker sentence sits. The copy: clean one-pick scenes ({{dp|catalogue|9b|clean one-pick scenes: scenes used}} / {{dp|catalogue|27b|clean one-pick scenes: scenes used}} / {{dp|catalogue|muse|clean one-pick scenes: scenes used}} on the 9B / 27B / Muse), those with the locker after the pick. Lightning: the clean design is not tested (gate: its clean one-pick recall is below 0.80); its copy numbers are descriptive only. The 122B: the split only.
- **Method.**
  - the split: the change at the bridge word at L; the lookups it switches, by sentence order;
  - the copy, clean scenes with the locker after the pick: (a) the change at the bridge word at L; (c) the changed prompt's states copied into every locker-sentence token at L; (d) the same at L/2; each as a share of the lookups the changed prompt itself switches.
- **Rule, fixed in advance.** The copy: "'the link is made in the locker sentences' if (c) or (d) switches at least half of the lookups the changed prompt switches while (a) stays at or below 0.25, on at least 2 of 3 models." The split by sentence order was read after the data (descriptive). Lightning: the same rule, copied, no prediction.

![Locker after the pick: the link is made in the locker sentences](figures/story/fig03_order.png)
*(A) Lookups switched by the change at the bridge word, locker sentence before or after the pick, per model (the recall beside); (B) the same split on Zach's passages, by fact order (Part V); (C) locker after the pick, by layer: the change at the bridge word (dashed) and the change copied into the locker sentences (solid), the rule's arms ringed. Lightning hollow, its copy below gate; the 122B (FP8, its L33 the 27B's relative depth) in panel A only.*

- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | lookups switched, locker sentence before the pick | {{d|fig03|9b|lookups switched by the whole change, locker sentence before the pick}} | {{d|fig03|27b|lookups switched by the whole change, locker sentence before the pick}} | {{d|fig03|muse|lookups switched by the whole change, locker sentence before the pick}} | {{d|fig03|nemotron-3.5-lightning|lookups switched by the whole change, locker sentence before the pick}} | {{d|fig03|122b|lookups switched by the whole change, locker sentence before the pick}} |
  | lookups switched, locker sentence after the pick | {{d|fig03|9b|lookups switched by the whole change, locker sentence after the pick}} | {{d|fig03|27b|lookups switched by the whole change, locker sentence after the pick}} | {{d|fig03|muse|lookups switched by the whole change, locker sentence after the pick}} | {{d|fig03|nemotron-3.5-lightning|lookups switched by the whole change, locker sentence after the pick}} | {{d|fig03|122b|lookups switched by the whole change, locker sentence after the pick}} |
  | the copy: (c) copied into the locker sentences at L | {{d|fig03|9b|45q, the rule's arm c: copy at L, every locker-sentence token (lookups switched)}} | {{d|fig03|27b|45q, the rule's arm c: copy at L, every locker-sentence token (lookups switched)}} | {{d|fig03|muse|45q, the rule's arm c: copy at L, every locker-sentence token (lookups switched)}} | below gate: {{d|fig03|nemotron-3.5-lightning|45q, the rule's arm c: copy at L, every locker-sentence token (lookups switched)}} | not run |
  | the copy: (d) the same at L/2 | {{d|fig03|9b|45q, the rule's arm d: copy at L/2, every locker-sentence token (lookups switched)}} | {{d|fig03|27b|45q, the rule's arm d: copy at L/2, every locker-sentence token (lookups switched)}} | {{d|fig03|muse|45q, the rule's arm d: copy at L/2, every locker-sentence token (lookups switched)}} | below gate: {{d|fig03|nemotron-3.5-lightning|45q, the rule's arm d: copy at L/2, every locker-sentence token (lookups switched)}} | not run |
  | the copy: (a) the change at the bridge word at L | {{d|fig03|9b|45q, the rule's arm a: the bridge-word change at L (lookups switched)}} | {{d|fig03|27b|45q, the rule's arm a: the bridge-word change at L (lookups switched)}} | {{d|fig03|muse|45q, the rule's arm a: the bridge-word change at L (lookups switched)}} | below gate: {{d|fig03|nemotron-3.5-lightning|45q, the rule's arm a: the bridge-word change at L (lookups switched)}} | not run |
  | the copy: the rule | **{{dp|cards|9b|45q: the rule's reading}}** | **{{dp|cards|27b|45q: the rule's reading}}** | **{{dp|cards|muse|45q: the rule's reading}}** | not tested (gate) | not run |

- **Read.**
  - With the locker sentence first, the change at the bridge word switches most lookups on all five models; with it after, few.
  - With the locker after the pick, copying the changed states into the locker sentences carries most of the lookup's switches and the bridge-word change almost none: the link is made in the locker sentences.
  - Lightning's copy, below its gate, reads the same way.
- **Caveats.**
  - The split by sentence order was chosen after the data; with the locker after the pick too few lookups switch to read either reader's loss there.
  - At L/2 the copy carries little on the 9B and 27B and about half on Muse.
  - Lightning's copy is below its gate: descriptive only, never in the claims or grades.

### Which token and layer carry the lookup when the locker sentence comes after the pick?

- **Question.** Which token and layer carry the lookup when the locker sentence comes after the pick?
- **Why we asked.** With the locker after the pick the bridge word cannot point back; a map of tokens and layers says where the link sits instead.
- **Data.** Clean one-pick scenes on the 9B, 27B and Muse (the main test beside them); Lightning the main test only, its clean design below gate; the 122B not run.
- **Method.**
  - the map: the changed prompt's state placed into one token group (the bridge word, the rest of the pick sentence, the asked person, each locker sentence's item and number, the question, the last token) at one layer, every second (9B) or fourth layer (27B, Muse, Lightning), by sentence order;
  - the lookups the change at L misses: the bridge word replaced at every layer up to L, against the change at L alone.
- **Rule, fixed in advance.** "(a) In locker-after scenes the lookup's mass sits at the locker sentences, not at the bridge word, at every layer (bridge-word cells ≤ 0.25 everywhere; some locker-sentence cell ≥ 0.5). (b) In locker-first scenes the lookup's bridge-word mass ends before the recall's does (the last layer with bridge-word switch ≥ 0.3 is earlier for the lookup, by ≥ 2 layers on the 9B, ≥ 4 on Muse)." The 27B and Lightning: the same rule, copied, no prediction. The lookups the change at L misses: descriptive.

![Locker after the pick: the lookup leaves the bridge word early](figures/story/fig03d_depth_map.png)
*Lookups and recalls switched when the changed state is placed in one token group at one layer, locker sentence before and after the pick, the locker sentences collapsed to their best cell; bottom rows: the bridge word replaced at every layer up to L, and from L on. The 9B, 27B and Muse on clean one-pick scenes; Lightning (hollow) on its main test.*

- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | (a) locker after the pick: a locker-sentence cell carries the lookup | {{dp|cards|9b|D1 (clean): (a) locker after: a locker-sentence cell carries the lookup}} | {{dp|cards|27b|D1 (clean): (a) locker after: a locker-sentence cell carries the lookup}} | {{dp|cards|muse|D1 (clean): (a) locker after: a locker-sentence cell carries the lookup}} | {{dp|cards|nemotron-3.5-lightning|D1 (main): (a) locker after: a locker-sentence cell carries the lookup}} (main test) | not run |
  | (b) locker before the pick: the lookup leaves the bridge word before the recall | {{dp|cards|9b|D1 (clean): (b) locker first: the lookup leaves the bridge word before the recall}} | {{dp|cards|27b|D1 (clean): (b) locker first: the lookup leaves the bridge word before the recall}} | {{dp|cards|muse|D1 (clean): (b) locker first: the lookup leaves the bridge word before the recall}} | {{dp|cards|nemotron-3.5-lightning|D1 (main): (b) locker first: the lookup leaves the bridge word before the recall}} (main test) | |
  | locker after the pick: of the lookups the change at L misses, carried by the bridge word before L (main test) | {{d|e11_before_l|9b|47.4: main, locker after the pick: lookups carried by the bridge word before L}} | {{d|e11_before_l|27b|47.4: main, locker after the pick: lookups carried by the bridge word before L}} | {{d|e11_before_l|muse|47.4: main, locker after the pick: lookups carried by the bridge word before L}} | {{d|e11_before_l|nemotron-3.5-lightning|47.4: main, locker after the pick: lookups carried by the bridge word before L}} | |
  | the same, clean one-pick scenes | {{d|e11_before_l|9b|47.4: clean, locker after the pick: lookups carried by the bridge word before L}} | {{d|e11_before_l|27b|47.4: clean, locker after the pick: lookups carried by the bridge word before L}} | {{d|e11_before_l|muse|47.4: clean, locker after the pick: lookups carried by the bridge word before L}} | not tested (gate) | |

- **Read.**
  - No single cell carries the locker-after lookup on any model: the link is spread over tokens and layers.
  - The lookup does not leave the bridge word before the recall by the margin fixed in advance; both read it to about the same depth, then the question and the last token carry the answer.
  - The lookups the change at L misses are read from the bridge word at earlier layers.
- **Caveats.**
  - The 27B, Muse and Lightning were sampled every fourth layer, so their layers are known to four.
  - Lightning: the main test only; its clean design is below its gate.
  - The lookups the change misses are descriptive: no rule was fixed for them.

### On Lightning, does the lookup read the bridge word through its attention blocks?

- **Question.** On Lightning, does the lookup read the bridge word through its attention blocks?
- **Why we asked.** Lightning's attention heads move with the address swap in blocks 19 and 26 (the appendix's attention figure); its other blocks carry a running state (Mamba-2), so the bridge word could reach the lookup through those two attention blocks, or through the state.
- **Data.** Main test at L: {{dp|cards|nemotron-3.5-lightning|53.4: scenes, bridge entities}}; the whole change switches the lookup on {{dp|cards|nemotron-3.5-lightning|53.4: lookups switched by the whole change}} of them. The follow-up uses the same scenes; its rule reads those where a control span fits ({{dp|cards|nemotron-3.5-lightning|53.4 span: scenes where the control fits, bridge entities}}); the other {{dp|cards|nemotron-3.5-lightning|53.4 span: scenes dropped (no control fits)}} are read on their own. The 9B, 27B and Muse: not applicable (a test of Lightning's blocks); the 122B: not run.
- **Method.** The whole change at the bridge word at L, while every later token cannot attend to the bridge word in:
  - (i) block 19, (ii) block 26, (iii) both, (iv) every attention block after L;
  - (v) control: both blocks, with attention to another token of the same sentence blocked instead;
  - read: the share of the whole change's lookup switches each block cuts; the recall alongside.
  - Follow-up: in blocks 19 and 26, every token after the scene's last token cannot attend to the whole span from the bridge word to the scene's end (median {{dp|cards|nemotron-3.5-lightning|53.4 span: median span length in tokens, the rule's scenes}} tokens on the rule's scenes); control: a span of the same length ending at the last token before the bridge's sentence, one placement, fixed before the run.
- **Rule, fixed in advance.** "'Read through two blocks' if (iii) cuts the lookup's switches by ≥ 0.6 of the whole change's and (v) by ≤ 0.15; 'one block' if (i) or (ii) alone cuts ≥ 0.6; 'not through attention at the bridge' if (iv) cuts < 0.3 (the Mamba state carries it); else in between." Follow-up: "'The pointer is read by attention after the Mamba state spreads it' if the span cuts the lookup's switches by ≥ 0.6 and the control by ≤ 0.15; else as [the rule above]." No prediction. The cut on the scenes where the lookup's clean answer survives the span block was added after the data (descriptive).

![Two attention blocks carry part of Lightning's lookup, not all of it](figures/story/fig22_attention_blocks.png)
*The share of the whole change's switches cut when later tokens cannot attend to the bridge word (top) or to the span from the bridge word to the scene's end (bottom), lookup (purple) and recall (dark), whiskers {{q|95%}}; dashed: the rule's 0.6, dotted: 0.3. Lightning hollow (○); the 9B, 27B and Muse not applicable (a test of Lightning's blocks); the 122B not run.*

- **Result.** Pending hand-check.

  | the lookup's switches cut | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | block 19 / block 26 | not applicable | not applicable | not applicable | {{d|fig22_attention_blocks|nemotron-3.5-lightning|attention blocks, the bridge word blocked, lookup: switches cut, block 19}} / {{d|fig22_attention_blocks|nemotron-3.5-lightning|attention blocks, the bridge word blocked, lookup: switches cut, block 26}} | not run |
  | both blocks | | | | {{d|fig22_attention_blocks|nemotron-3.5-lightning|attention blocks, the bridge word blocked, lookup: switches cut, blocks 19 and 26}} | |
  | every attention block after L | | | | {{d|fig22_attention_blocks|nemotron-3.5-lightning|attention blocks, the bridge word blocked, lookup: switches cut, every attention block after L}} | |
  | control: another token, both blocks | | | | {{d|fig22_attention_blocks|nemotron-3.5-lightning|attention blocks, the bridge word blocked, lookup: switches cut, control: another token, both blocks}} | |
  | the lookup keeps its clean answer: both blocks / every attention block after L | | | | {{dp|cards|nemotron-3.5-lightning|53.4: the lookup keeps its clean answer, blocks 19 and 26}} / {{dp|cards|nemotron-3.5-lightning|53.4: the lookup keeps its clean answer, every attention block after L}} | |
  | the recall's switches cut: every attention block after L | | | | {{d|fig22_attention_blocks|nemotron-3.5-lightning|attention blocks, the bridge word blocked, recall: switches cut, every attention block after L}} | |
  | the rule | | | | **{{dp|cards|nemotron-3.5-lightning|53.4: the rule (lookup)}}** | |
  | follow-up, the rule's scenes: the span / the control span | | | | {{d|fig22_attention_blocks|nemotron-3.5-lightning|attention blocks, the span follow-up, lookup: switches cut, the span, blocks 19 and 26}} / {{d|fig22_attention_blocks|nemotron-3.5-lightning|attention blocks, the span follow-up, lookup: switches cut, control span, same length}} | |
  | follow-up: both blocks at the bridge word, the same scenes | | | | {{d|fig22_attention_blocks|nemotron-3.5-lightning|attention blocks, the span follow-up, lookup: switches cut, the bridge word, both blocks (rerun)}} | |
  | follow-up: the lookup keeps its clean answer, the span / the control span | | | | {{dp|cards|nemotron-3.5-lightning|53.4 span: the lookup keeps its clean answer, the span, blocks 19 and 26}} / {{dp|cards|nemotron-3.5-lightning|53.4 span: the lookup keeps its clean answer, control span, same length}} | |
  | follow-up, the rule's scenes where the lookup's clean answer survives the span block ({{dp|cards|nemotron-3.5-lightning|53.4 span: the rule's scenes where the lookup's clean answer survives the span block}}; descriptive): the span / the control span | | | | {{d|cards|nemotron-3.5-lightning|53.4 span, the scenes where the clean answer survives: lookup switches cut by the span}} / {{d|cards|nemotron-3.5-lightning|53.4 span, the scenes where the clean answer survives: lookup switches cut by the control span}} | |
  | follow-up: the span on every scene / on the scenes without a control | | | | {{d|cards|nemotron-3.5-lightning|53.4 span: lookup switches cut by the span, all scenes}} / {{d|cards|nemotron-3.5-lightning|53.4 span: lookup switches cut by the span, scenes without a control}} | |
  | follow-up: the rule | | | | **{{dp|cards|nemotron-3.5-lightning|53.4 span: the rule (lookup)}}** | |

- **Read.**
  - Blocking the bridge word in both attention blocks cuts about a third of Lightning's lookup switches, as much as blocking every attention block after L; either block on its own cuts little, the control nothing. By the rule: in between.
  - Blocking the whole span from the bridge word to the scene's end in the same two blocks cuts about half, the control span nothing; still under the rule's bar, so in between: the lookup reads part of the bridge word through these two blocks and the rest some other way.
  - On the scenes where the lookup keeps its clean answer under the span block, the span cuts about as much: the cut is not only general damage.
- **Caveats.**
  - Pending hand-check: today's runs, unverified until hand-checked.
  - Lightning only, by design; its gate was chosen after its pre-check (○).
  - Collateral: blocking both blocks costs the lookup its clean answer on about a quarter of scenes; the span costs it on more than half of the rule's scenes, the control span on none. The survivors' cut is descriptive; the label is computed on all the rule's scenes.
  - The follow-up's rule reads only the scenes where a control span fits, whose spans are short (median {{dp|cards|nemotron-3.5-lightning|53.4 span: median span length in tokens, the rule's scenes}} tokens against {{dp|cards|nemotron-3.5-lightning|53.4 span: median span length in tokens, the dropped scenes}} on the others); on the others the lookup mostly does not switch under the whole change ({{dp|cards|nemotron-3.5-lightning|53.4 span: share of the scenes without a control whose lookup switches}}), so the span's cut there says little.
  - The control span is one placement and ends further from the question than the span (median {{dp|cards|nemotron-3.5-lightning|53.4 span: median distance from the end of the control span to the question}} tokens against {{dp|cards|nemotron-3.5-lightning|53.4 span: median distance from the end of the span to the question}}).

### Does the lookup drop the lens part before it takes up the address?

- **Question.** Does the lookup drop the lens part before it takes up the address?
- **Why we asked.** At L the lookup takes an identity route and a position route; depth says which comes first and whether the address is written before it is read.
- **Data.** Routes scenes with the locker sentence first, split in halves: refit on one, read on the other. The 9B, Muse and Lightning; the 27B on two grids (first a reduced one, then every fourth layer); the 122B not run.
- **Method.** At each sampled layer: the whole change and its parts (the lens part; the address refit at that layer; the identity outside the lens), each taken out or added by itself, against random parts of the same share; a probe for the locker at the bridge word. A layer counts only where the whole change switches 0.30 or more. Across depth: the overlap of the address refit at every pair of layers in the probe's window.
- **Rule, fixed in advance.** "Define l_J = the first layer from which the lookup's switches lost without the lens part beyond random stay ≤ 0.10; l_P = the first layer where the position route's share under the whole change is ≥ 0.20; l_probe = the first layer where the probe is ≥ 0.80. (a) 'Handoff': l_P ≥ l_J [...] (b) 'The address forms before it is used': l_probe ≤ l_P on every model [...] (d) 'Never the value, at any depth': value ≤ 0.05 at every interpretable layer." Across depth: "persistent if the mean cos² of the principal angles ≥ 0.5 across the window where the probe is ≥ 0.8; re-encoded if it drops below 0.2 between adjacent sampled layers." The 27B's full grid and Lightning: the same rule, copied, no prediction.

![The address forms early; identity route first, position route later](figures/story/fig06b_anatomy.png)
*Per sampled layer, the lookup's answers under the whole change at that layer (identity route blue, position route orange, the original answer grey) and the recall's switches (line); dashed: the address readable (probe ≥ 0.8); solid: position answers begin; hatched: too few switches to read. The 27B panel is its reduced grid; Lightning hollow; the 122B not run.*

- **Result.**

  | | 9B | 27B (full grid) | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | the address readable from layer | {{dp|cards|9b|47.8: the address readable from}} | {{dp|cards|27b|47.8 (full grid): the address readable from}} | {{dp|cards|muse|47.8: the address readable from}} | {{dp|cards|nemotron-3.5-lightning|47.8: the address readable from}} | not run |
  | the position route from layer | {{dp|cards|9b|47.8: the first layer of the position route}} | {{dp|cards|27b|47.8 (full grid): the first layer of the position route}} | {{dp|cards|muse|47.8: the first layer of the position route}} | {{dp|cards|nemotron-3.5-lightning|47.8: the first layer of the position route}} | |
  | the lookup needs the lens part up to layer | {{dp|cards|9b|47.8: the last layer the lookup needs the J++ part}} | {{dp|cards|27b|47.8 (full grid): the last layer the lookup needs the J++ part}} | {{dp|cards|muse|47.8: the last layer the lookup needs the J++ part}} | {{dp|cards|nemotron-3.5-lightning|47.8: the last layer the lookup needs the J++ part}} | |
  | (a) the handoff | {{dp|cards|9b|47.8: (a) the handoff}} | {{dp|cards|27b|47.8 (full grid): (a) the handoff}} (reduced grid: {{dp|cards|27b|47.8 (reduced grid): (a) the handoff}}) | {{dp|cards|muse|47.8: (a) the handoff}} | {{dp|cards|nemotron-3.5-lightning|47.8: (a) the handoff}} | |
  | (b) the address readable before it is used | {{dp|cards|9b|47.8: (b) readable before it is used}} | {{dp|cards|27b|47.8 (full grid): (b) readable before it is used}} | {{dp|cards|muse|47.8: (b) readable before it is used}} | {{dp|cards|nemotron-3.5-lightning|47.8: (b) readable before it is used}} | |
  | (d) never the value | {{dp|cards|9b|47.8: (d) never the value}} | {{dp|cards|27b|47.8 (full grid): (d) never the value}} | {{dp|cards|muse|47.8: (d) never the value}} | {{dp|cards|nemotron-3.5-lightning|47.8: (d) never the value}} | |
  | the address across depth: mean overlap (reading) | {{dp|fig06c|9b|D4: the address's mean overlap over every pair of window layers}} ({{dp|fig06c|9b|D4: the rule's reading (the address)}}) | {{dp|cards|27b|D4: the address's mean overlap over every pair of window layers}} ({{dp|cards|27b|D4: the rule's reading (the address)}}) | {{dp|fig06c|muse|D4: the address's mean overlap over every pair of window layers}} ({{dp|fig06c|muse|D4: the rule's reading (the address)}}) | {{dp|cards|nemotron-3.5-lightning|D4: the address's mean overlap over every pair of window layers}} ({{dp|cards|nemotron-3.5-lightning|D4: the rule's reading (the address)}}) | |

- **Read.**
  - On all four models the address is readable before the lookup starts using it, and the lookup never takes the value.
  - On the 9B, Muse and Lightning the lookup stops needing the lens part by the layer its position route starts; on the 27B's full grid it still needs it after, so the handoff depends on which layers are sampled.
  - The address's code changes across depth on every model.
- **Caveats.**
  - The 27B: the reduced grid gave a handoff (the lens part needed up to layer {{dp|cards|27b|47.8 (reduced grid): the last layer the lookup needs the J++ part}}, the position route from layer {{dp|cards|27b|47.8 (reduced grid): the first layer of the position route}}); the full grid samples a layer the reduced grid skipped. The figure shows the reduced grid.
  - Each layer's address and probe are refit on the fit half; early layers read less well.
  - Position grows with depth on the main test too (a candidate, not tested by a rule).

### At the last token, is the bridge entity in the lens part of the state, and does the model use it there?

- **Question.** At the last token, is the bridge entity in the lens part of the state, and does the model use it there?
- **Why we asked.** The cards above work at the bridge word; a lens monitor reads the last token, where the answer is written.
- **Data.** Main test, scenes with the locker sentence first: {{dp|cards|9b|51.10: main-test scenes, locker first}} / {{dp|cards|27b|51.10: main-test scenes, locker first}} / {{dp|cards|muse|51.10: main-test scenes, locker first}} / {{dp|cards|nemotron-3.5-lightning|51.10: main-test scenes, locker first}} ○.
- **Method.** At the last token, every fourth layer before the answer appears:
  - read: a probe for the bridge entity on the lens part of the state (and the lens's top five), against the probe on the whole state;
  - write, at the layer the read peaks: the lens part of the changed prompt's state swapped in, against the whole state patched in; control: a random part of the same size;
  - what the model then outputs (descriptive): its clean answer, the changed prompt's answer, another digit, the entity's name or a number word.
- **Rule, fixed in advance.** "Read: through-the-lens probe ≥ 0.8 and lens top-5 ≥ 0.5 at some layer before the answer digit's layer, while the full-residual probe ≥ 0.9 there. Write: at the layer of the read peak, his swap or the J++ part of the change (gain ≤ 2) switches ≥ 0.5 of what the whole-state patch switches at that layer, with the random part ≤ 0.10. (b) readable, not used: read holds, write fails." Lightning: the same rule, copied.

![The recall's entity at the last token: readable through the lens, not used](figures/story/fig17_jspace_last_token.png)
*At the last token, per reader and model: the probe's accuracy on the lens part of the state (read) and the lens swap's switches as a share of the whole-state patch's (swap), both at the layer where the read peaks; Lightning hollow; 122B not run.*

- **Result.**

  | the recall, last token | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | read: the probe on the lens part | {{d|fig17_jspace_last_token|9b|51.10: recall, last token, read peak: the probe's accuracy on the lens part}} | {{d|fig17_jspace_last_token|27b|51.10: recall, last token, read peak: the probe's accuracy on the lens part}} | {{d|fig17_jspace_last_token|muse|51.10: recall, last token, read peak: the probe's accuracy on the lens part}} | {{d|fig17_jspace_last_token|nemotron-3.5-lightning|51.10: recall, last token, read peak: the probe's accuracy on the lens part}} | not run |
  | write: the lens swap's switches | {{dp|fig17_jspace_last_token|9b|51.10: recall, last token, read peak: the lens swap's switches}} | {{dp|fig17_jspace_last_token|27b|51.10: recall, last token, read peak: the lens swap's switches}} | {{dp|fig17_jspace_last_token|muse|51.10: recall, last token, read peak: the lens swap's switches}} | {{dp|fig17_jspace_last_token|nemotron-3.5-lightning|51.10: recall, last token, read peak: the lens swap's switches}} | not run |
  | the whole-state patch's switches | {{dp|fig17_jspace_last_token|9b|51.10: recall, last token, read peak: the whole-state patch's switches}} | {{dp|fig17_jspace_last_token|27b|51.10: recall, last token, read peak: the whole-state patch's switches}} | {{dp|fig17_jspace_last_token|muse|51.10: recall, last token, read peak: the whole-state patch's switches}} | {{dp|fig17_jspace_last_token|nemotron-3.5-lightning|51.10: recall, last token, read peak: the whole-state patch's switches}} | not run |
  | the rule | {{dp|cards|9b|51.10: recall at the last token: the rule's reading}} | {{dp|cards|27b|51.10: recall at the last token: the rule's reading}} | {{dp|cards|muse|51.10: recall at the last token: the rule's reading}} | {{dp|cards|nemotron-3.5-lightning|51.10: recall at the last token: the rule's reading}} | not run |
  | the lookup at the last token: the rule | {{dp|cards|9b|51.10: lookup at the last token: the rule's reading}} | {{dp|cards|27b|51.10: lookup at the last token: the rule's reading}} | {{dp|cards|muse|51.10: lookup at the last token: the rule's reading}} | {{dp|cards|nemotron-3.5-lightning|51.10: lookup at the last token: the rule's reading}} | not run |
  | under the lens swap, the clean answer stays | {{dp|cards|9b|lenswrite: the recall keeps its clean answer under the lens swap}} | {{dp|cards|27b|lenswrite: the recall keeps its clean answer under the lens swap}} | {{dp|cards|muse|lenswrite: the recall keeps its clean answer under the lens swap}} | {{dp|cards|nemotron-3.5-lightning|lenswrite: the recall keeps its clean answer under the lens swap}} | not run |
  | outputs naming the entity or a number word, any arm | {{dp|cards|9b|lenswrite: the most outputs naming the entity or a number word, over every arm}} | {{dp|cards|27b|lenswrite: the most outputs naming the entity or a number word, over every arm}} | {{dp|cards|muse|lenswrite: the most outputs naming the entity or a number word, over every arm}} | {{dp|cards|nemotron-3.5-lightning|lenswrite: the most outputs naming the entity or a number word, over every arm}} | not run |
  | the J++ part at gain 2: the changed prompt's answer | {{dp|cards|9b|lenswrite: the J++ part at gain 2 gives the changed prompt's recall answer}} | {{dp|cards|27b|lenswrite: the J++ part at gain 2 gives the changed prompt's recall answer}} | {{dp|cards|muse|lenswrite: the J++ part at gain 2 gives the changed prompt's recall answer}} | {{dp|cards|nemotron-3.5-lightning|lenswrite: the J++ part at gain 2 gives the changed prompt's recall answer}} | not run |
  | a random part at gain 2: the same | {{dp|cards|9b|lenswrite: a random part at gain 2 gives the changed prompt's recall answer}} | {{dp|cards|27b|lenswrite: a random part at gain 2 gives the changed prompt's recall answer}} | {{dp|cards|muse|lenswrite: a random part at gain 2 gives the changed prompt's recall answer}} | {{dp|cards|nemotron-3.5-lightning|lenswrite: a random part at gain 2 gives the changed prompt's recall answer}} | not run |

- **Read.**
  - At the last token the recall's bridge entity is readable through the lens on all four models, but writing it through the lens does not move the answer at a real change's size: the whole-state patch switches nearly every recall, the lens swap almost none.
  - The lens swap never makes the model say the entity's name or a number word; the recall keeps its clean answer.
  - At twice the size, the J++ part moves part of Muse's and Lightning's recalls, beyond a random part of that size.
  - The lookup's entity is not readable there by the rule on any model.
- **Caveats.**
  - "Not used" means not at a real change's size: at gain 2 the J++ part has an effect on Muse and Lightning.
  - Lightning's swap moves more than the others' ({{dp|fig17_jspace_last_token|nemotron-3.5-lightning|51.10: recall, last token, read peak: the lens swap's switches}}), and its random part at gain 2 moves {{dp|cards|nemotron-3.5-lightning|lenswrite: a random part at gain 2 gives the changed prompt's recall answer}}.
  - The output classes are descriptive (CPU check of the stored runs).

## Part V. Other datasets and operations

*Our removal on Zach's passages and his operation on our scenes. The 122B: not run.*

### Does the split hold on Zach's passages, and do his operation and ours agree?

- **Question.** Does the split hold on Zach's passages, and do his operation and ours agree?
- **Why we asked.** Our scenes are short lists; his passages scatter the facts in prose, and his operation (a change in his own lens directions) is not our removal.
- **Data.** His passages with a named bridge, {{dp|catalogue|9b|Zach's passages, named bridge: passages used}} per model, at each model's L:
  - true facts (the lookup's passage states the bridge's final fact): the 9B, 27B, Muse and Lightning;
  - made-up facts: the same four models; Muse's and Lightning's miss the gate;
  - the recheck on the 9B (pending hand-check): the made-up-fact passages without the {{dp|cards|9b|Z1-P recheck: passages left out (the bridge's true value in the lookup's passage)}} whose bridge's true value stands in the lookup's passage as another entity's value, {{dp|cards|9b|Z1-P recheck, without the passages holding the true value: passages}} passages ({{dp|cards|9b|Z1-P recheck, without the passages holding the true value: bridge entities}} bridge entities) against all {{dp|cards|9b|Z1-P recheck, all passages: passages}} ({{dp|cards|9b|Z1-P recheck, all passages: bridge entities}});
  - the 122B not run.
- **Method.**
  - our removal: the conflict test at the bridge name's last token at L, without the lens part against without a random part, each reader with its own change;
  - the full carrier: the change at every layer up to L, the same removal;
  - the routes test on his passages: another item's fact sentence moved and took a new value;
  - his operation: his stored rows on his passages against his rotated directions, and on our clean scenes the ladder's last step (Part I).
- **Rule, fixed in advance.** "Per model: gap ≥ 0.3 and lookup extra loss ≤ 0.10 → the split holds on his passages; lookup ≥ 0.20 → the lookup follows the lens here; else in between. The order pattern replicates if the lookup's switch under the whole change is ≥ 2x higher fact-first than fact-after (both CIs)." The full carrier: "recall extra loss − lookup extra loss ≥ 0.3 and lookup ≤ 0.10 → the split holds on the full carrier; lookup ≥ 0.20 → the lookup follows the lens on the full carrier; else in between." The routes test: "Value ≤ 0.05; if position ≥ 0.2: the address exists in scattered-fact passages; if position ≤ 0.05: no position route in his layout." The recheck: the same rule, verbatim, on the remaining passages (set after the data). The two operations side by side: descriptive. Lightning: the same rules, copied, no prediction.

![Both operations, both datasets, one direction](figures/story/fig12_two_by_two.png)
*Recall minus lookup in four cells: our removal or Zach's operation, on our scenes or his passages; grey tick: the same operation with a random part of the same size (his: his rotated directions). The units differ by row, so only the sign and the order compare. Lightning hollow; the 122B in our main test only.*

- **Result.**

  | | 9B | 27B | Muse | Lightning ○ | 122B |
  |---|---|---|---|---|---|
  | true facts: lookup, switches lost beyond a random part | {{d|cards|9b|Z1: lookup, switches lost beyond a random part}} | {{d|cards|27b|Z1: lookup, switches lost beyond a random part}} | {{d|cards|muse|Z1: lookup, switches lost beyond a random part}} (too few switches: {{dp|fig12|muse|our removal, his passages: lookup switches under the whole change}} of {{dp|catalogue|muse|Zach's passages, named bridge: passages used}}) | {{d|cards|nemotron-3.5-lightning|Z1: lookup, switches lost beyond a random part}} | not run |
  | true facts: recall, the same | {{d|cards|9b|Z1: recall, switches lost beyond a random part}} | {{d|cards|27b|Z1: recall, switches lost beyond a random part}} | {{d|cards|muse|Z1: recall, switches lost beyond a random part}} | {{d|cards|nemotron-3.5-lightning|Z1: recall, switches lost beyond a random part}} | |
  | true facts: the rule | **{{dp|cards|9b|Z1: the rule's reading}}** | **{{dp|cards|27b|Z1: the rule's reading}}** | **{{dp|cards|muse|Z1: the rule's reading}}** (too few switches to read) | **{{dp|cards|nemotron-3.5-lightning|Z1: the rule's reading}}** | |
  | true facts: lookups switched, fact first / fact after | {{dp|fig03|9b|Zach's passages, L12: lookups switched by the whole change, fact-first}} / {{dp|fig03|9b|Zach's passages, L12: lookups switched by the whole change, fact-after}} | {{dp|fig03|27b|Zach's passages, L32: lookups switched by the whole change, fact-first}} / {{dp|fig03|27b|Zach's passages, L32: lookups switched by the whole change, fact-after}} | {{dp|fig03|muse|Zach's passages, L26: lookups switched by the whole change, fact-first}} / {{dp|fig03|muse|Zach's passages, L26: lookups switched by the whole change, fact-after}} | {{dp|fig03|nemotron-3.5-lightning|Zach's passages, L14: lookups switched by the whole change, fact-first}} / {{dp|fig03|nemotron-3.5-lightning|Zach's passages, L14: lookups switched by the whole change, fact-after}} | |
  | made-up facts: lookup, switches lost beyond a random part | {{d|cards|9b|Z1-P: lookup, switches lost beyond a random part}} | {{d|cards|27b|Z1-P: lookup, switches lost beyond a random part}} | ○ {{d|cards|muse|Z1-P: lookup, switches lost beyond a random part}} | {{d|cards|nemotron-3.5-lightning|Z1-P: lookup, switches lost beyond a random part}} | |
  | made-up facts: recall, the same | {{d|cards|9b|Z1-P: recall, switches lost beyond a random part}} | {{d|cards|27b|Z1-P: recall, switches lost beyond a random part}} | ○ {{d|cards|muse|Z1-P: recall, switches lost beyond a random part}} | {{d|cards|nemotron-3.5-lightning|Z1-P: recall, switches lost beyond a random part}} | |
  | made-up facts: the gap | {{d|cards|9b|Z1-P: the gap}} | {{d|cards|27b|Z1-P: the gap}} | ○ {{d|cards|muse|Z1-P: the gap}} | {{d|cards|nemotron-3.5-lightning|Z1-P: the gap}} | |
  | made-up facts: the rule | **{{dp|cards|9b|Z1-P: the rule's reading}}** | **{{dp|cards|27b|Z1-P: the rule's reading}}** | not tested (gate {{dp|cards|muse|Z1-P: the gate (the lookup's read accuracy on the original passages)}} < 0.80); descriptive only | not tested (gate {{dp|cards|nemotron-3.5-lightning|Z1-P: the gate (the lookup's read accuracy on the original passages)}} < 0.80); descriptive only | |
  | made-up facts, recheck (pending hand-check): lookup / recall / gap, all passages | {{d|cards|9b|Z1-P recheck, all passages: lookup, switches lost beyond a random part}} / {{d|cards|9b|Z1-P recheck, all passages: recall, switches lost beyond a random part}} / {{d|cards|9b|Z1-P recheck, all passages: the gap}} | not run | not run | not run | |
  | the same, without the passages holding the true value | {{d|cards|9b|Z1-P recheck, without the passages holding the true value: lookup, switches lost beyond a random part}} / {{d|cards|9b|Z1-P recheck, without the passages holding the true value: recall, switches lost beyond a random part}} / {{d|cards|9b|Z1-P recheck, without the passages holding the true value: the gap}} | | | | |
  | the recheck: the rule, all passages / without | **{{dp|cards|9b|Z1-P recheck, all passages: the rule's reading}}** / **{{dp|cards|9b|Z1-P recheck, without the passages holding the true value: the rule's reading}}** | | | | |
  | the recheck: lookups switched, fact first / fact after, all passages; without | {{dp|cards|9b|Z1-P recheck, all passages: lookups switched by the whole change, fact-first}} / {{dp|cards|9b|Z1-P recheck, all passages: lookups switched by the whole change, fact-after}}; {{dp|cards|9b|Z1-P recheck, without the passages holding the true value: lookups switched by the whole change, fact-first}} / {{dp|cards|9b|Z1-P recheck, without the passages holding the true value: lookups switched by the whole change, fact-after}} | | | | |
  | full carrier: fact-after lookups, switches lost beyond a random part | {{d|cards|9b|51.7: fact-after lookups, full carrier: switches lost beyond a random part}} | {{d|cards|27b|51.7: fact-after lookups, full carrier: switches lost beyond a random part}} | not run | {{d|cards|nemotron-3.5-lightning|51.7: fact-after lookups, full carrier: switches lost beyond a random part}} | |
  | routes test on his passages: position share under the whole change | {{d|cards|9b|Z3: position share under the whole change}} | {{d|cards|27b|Z3: position share under the whole change}} | {{d|cards|muse|Z3: position share under the whole change}} | {{d|cards|nemotron-3.5-lightning|Z3: position share under the whole change}} | |
  | routes test: the rule | **{{dp|cards|9b|Z3: the rule's reading}}** | **{{dp|cards|27b|Z3: the rule's reading}}** | **{{dp|cards|muse|Z3: the rule's reading}}** | **{{dp|cards|nemotron-3.5-lightning|Z3: the rule's reading}}** | |
  | his operation, his passages: his stored recall minus lookup (rotated) | {{d|fig12|9b|Zach's operation, his passages: his stored recall minus lookup}} ({{dp|fig12|9b|Zach's operation, his passages: his rotated-direction control, recall minus lookup}}) | {{d|fig12|27b|Zach's operation, his passages: his stored recall minus lookup}} ({{dp|fig12|27b|Zach's operation, his passages: his rotated-direction control, recall minus lookup}}) | {{d|fig12|muse|Zach's operation, his passages: his stored recall minus lookup}} ({{dp|fig12|muse|Zach's operation, his passages: his rotated-direction control, recall minus lookup}}) | {{d|fig12|nemotron-3.5-lightning|Zach's operation, his passages: his stored recall minus lookup}} ({{dp|fig12|nemotron-3.5-lightning|Zach's operation, his passages: his rotated-direction control, recall minus lookup}}) | |
  | his operation, our clean scenes: the recall's cost minus the lookup's (random) | {{dp|fig12|9b|Zach's operation, our scenes (rung 6): recall's cost minus the lookup's, every scene}} ({{dp|fig12|9b|Zach's operation, our scenes (rung 6): the control (a random part of the same size instead), recall minus lookup, every scene (kept with none minus kept with the random part)}}) | {{dp|fig12|27b|Zach's operation, our scenes (rung 6): recall's cost minus the lookup's, every scene}} ({{dp|fig12|27b|Zach's operation, our scenes (rung 6): the control (a random part of the same size instead), recall minus lookup, every scene (kept with none minus kept with the random part)}}) | {{dp|fig12|muse|Zach's operation, our scenes (rung 6): recall's cost minus the lookup's, every scene}} ({{dp|fig12|muse|Zach's operation, our scenes (rung 6): the control (a random part of the same size instead), recall minus lookup, every scene (kept with none minus kept with the random part)}}) | not tested (gate) | |

- **Read.**
  - On his true-fact passages the lookup follows the lens part too on the 9B and 27B: there the lookup can answer from memory, as the recall does.
  - With made-up facts the split returns on the 9B, and it stays when the passages that hold the bridge's true value are left out; the 27B is in between.
  - Carried over every layer up to L, the fact-after lookups follow the lens part on his passages; his layout gives the lookup little or no position route.
  - Both operations point the same way on both datasets: the recall depends on the lens directions more than the lookup does.
- **Caveats.**
  - The recheck is today's, run on CPU on the stored run, the rule unchanged: pending hand-check.
  - Muse's lookup switches under the whole change on too few of his passages to read its loss, with true facts and with made-up facts ({{dp|fig12|muse|our removal, his passages: lookup switches under the whole change}} and {{dp|cards|muse|Z1-P: lookups switched by the whole change}} of {{dp|catalogue|muse|Zach's passages, named bridge: passages used}}); Muse's and Lightning's made-up-fact gates are just under 0.80, so their numbers there are descriptive only (hollow).
  - The two operations differ in scope and units: only their sign and their order compare.
  - The routes test on his passages has few passages; the 27B is read at its L only.

## Part VI. What did not hold

*Harder prompts keep the split in part, and every mechanism we proposed for why failed.*

**Weaker results.**

- **A described bridge** ("the one known for honey"; rule fixed in advance): the split holds on the 9B and Muse (gap {{dp|fig05c|9b|47.3: gap (recall's extra loss minus the lookup's)}} / {{dp|fig05c|muse|47.3: gap (recall's extra loss minus the lookup's)}}); on the 27B the lookup follows the lens too ({{dp|fig05c|27b|47.3: lookup's extra loss without the J++ part}}). Lightning is not tested (gate {{dp|fig05c|nemotron-3.5-lightning|47.3: the gate (the lookup's read accuracy on the original prompts)}} < 0.80); descriptive only ○: gap {{d|fig05c|nemotron-3.5-lightning|47.3: gap (recall's extra loss minus the lookup's)}}, lookup {{dp|fig05c|nemotron-3.5-lightning|47.3: lookup's extra loss without the J++ part}}, and the answer word is not read at the changed token on {{dp|fig05c|nemotron-3.5-lightning|47.3 below gate, recall: items whose answer word ranks below the lens's top 50 at the changed token}} of items. Few bridge items ([figure](figures/story/fig05c_described_bridge.png); its example is another scene from the same set). Answer control: the answer word is not read at the bridge word on {{dp|cue_answer|9b|the described bridge in locker scenes, recall: items whose answer word ranks below the lens's top 50 at the changed token}} / {{dp|cue_answer|27b|the described bridge in locker scenes, recall: items whose answer word ranks below the lens's top 50 at the changed token}} of items (9B / 27B, 300 each); the arms beside say the item.

- **One question under two instructions** ("from the passage" / "from what you know"; 27B only, the others miss the gate): both instructions lose most switches without the J++ part and many without the address and the outside identity. With no instruction the 27B answers from the passage.
- **The address must be refit per text format:** fit on simple scenes it costs the lookup {{num|tptr_varied_range}} in varied scenes; refit it reaches {{pt|x45d_table_9b}}-{{pt|x45d_prose_9b}} (9B) and {{pt|x45d_prose_muse}}-{{pt|x45d_table_muse}} (Muse), {{dp|cards|nemotron-3.5-lightning|45d: the refit address, lookup switches lost beyond random: prose}}-{{dp|cards|nemotron-3.5-lightning|45d: the refit address, lookup switches lost beyond random: json}} on Lightning ○, at most {{pt|x45d_table_27b}} on the 27B ([figure](figures/story/fig09b_refit.png)).

- **The lookup's errors are not address errors** (9B, Lightning ○): the probe matches the wrong answer's slot in {{dp|fig07c|9b|47.13: wrong answers whose locker the address probe predicts}} / {{dp|cards|nemotron-3.5-lightning|47.13: wrong answers whose locker the address probe predicts}} of them.

**Withdrawn.**

- **The described bridge on Zach's passages.** At the token the change is made at, the lens ranks the answer word above the bridge entity on the 9B (median {{dp|withdrawn_z2|9b|Zach's described passages, lookup: the answer word's median lens rank at the changed token (original prompt), rounded}} against {{dp|withdrawn_z2|9b|Zach's described passages, lookup: the bridge entity's median lens rank at the changed token (original prompt), rounded}}) and level with it on the 27B ({{dp|withdrawn_z2|27b|Zach's described passages, lookup: the answer word's median lens rank at the changed token (original prompt), rounded}} against {{dp|withdrawn_z2|27b|Zach's described passages, lookup: the bridge entity's median lens rank at the changed token (original prompt), rounded}}). Taking out the answer directions alone costs {{dp|withdrawn_z2|9b|Zach's described passages, lookup: switches lost beyond a random part without the answer directions only}} / {{dp|withdrawn_z2|9b|Zach's described passages, recall: switches lost beyond a random part without the answer directions only}} (9B, lookup / recall) and {{dp|withdrawn_z2|27b|Zach's described passages, lookup: switches lost beyond a random part without the answer directions only}} / {{dp|withdrawn_z2|27b|Zach's described passages, recall: switches lost beyond a random part without the answer directions only}} (27B) of the switches beyond a random part, and about as much beyond a frequency-matched part; the verdict is "answer" or "mixed" in all four cells. Any reading of these passages as "the recall follows the item" is withdrawn.

**What did not hold** (each rule fixed in advance; [the five mechanism tests on one page](figures/story/fig15_mechanisms.png), now with the 27B and Lightning wherever they ran; none holds on any model):

- The J++ part keys the item's attribute at the bridge word; late MLPs there carry the recall → without the J++ part the attribute still moves part way; the MLPs are not needed.
- A person mark at the locker sentence → a probe reads chance there; a person direction moves nothing; pooled over the whole locker sentence, the probe stays at chance on the 9B and Muse and in between on the 27B, neither reading holding.
- The copying heads pass the rest at twice the J++ part → about equal.
- The address is the recall's second route → few recalls name the swapped slot's item. Removing the address does not hurt the recall, but swapping it at s = 2 redirects part of it (Part III, E6).
- Blocking the pick sentence from the lockers removes position answers only → identity answers and recall switches fall too.
- The second hop's key token (the locker number) carries the hall question's address → removing it costs no more than a random part of its large share.
- The address is the same for any kind of item (within 0.10 of the animal result) → on the 9B it moves fruits and names more than animals; on Muse names fall short.
- Token by layer: one locker-sentence cell carries the locker-after lookup; the lookup leaves the bridge word before the recall → neither.
- Also failed: the positive control, a second-vs-third address, the 9B in the clean design and its replication, the 27B's strict bar.

## How we checked

- **Hand-checked numbers:** none yet; [the verify pack](docs/verify_pack.md) recounts each claim from the per-item files.
- **The 122B:** the largest model's lookup loses nothing beyond random ({{pt|lk_excess_k25_122b}} with 25 lens directions; {{pt|lk_excess_k100_122b}} with 100, where the 27B loses {{pt|lk_excess_k100_27b}}), so the 27B's weakness is not a total-size trend; active parameters are not separated; its recall effect is the smallest of the five ({{pt|rc_excess_122b}}) and mixed on varied scenes ({{pt|x0b_c_122b}}); we cannot separate that from its later layer (L{{num|layer_122b}}, relative depth {{dp|cards|122b|L as a relative depth (L / the number of layers)}}) or FP8.
- **The ladder's reruns:** every step on this page comes from the full reruns (the 27B's full ladder; Muse's third run). Over every scene they agree with the first runs within {{dp|cards||the ladder: largest difference between the first runs and the full reruns, every scene, on the steps both ran at the same layers}} on each step both ran at the same layers ({{dp|cards||the ladder: the same within one sentence order}} at most within one sentence order); Muse's sixth step moved into Zach's layer band and differs by {{dp|cards|muse|the ladder: step 6's difference, every scene (moved into Zach's band)}}.
- **Independent reimplementation:** code written from scratch reproduces the 9B's main test on {{num|indep_agree_9b}} random items, every arm.
- **Predictions:** committed before results are opened, then scored ([predictions](predictions/README.md)): mean Brier {{num|pred_brier}} over {{num|pred_n}} answers, worse than always answering {{q|50%}}.
- **Limits:** one-token answers and bridges; reader and answer source confounded; the 122B in FP8 (MoE, ~10B active), with a J++ lens fit on its bf16 weights and its L carried over from the 27B's relative depth.

## Related work and what is new

Models bind entities to attributes in context (Feng & Steinhardt 2023) and track them through lookback pointers (Prakash et al. 2025) in a low-dimensional order subspace (Dai et al. 2024). The routes test follows Gur-Arieh et al. (2025); the address uses mass-mean directions (Marks & Tegmark 2023); random parts answer Makelov et al. (2023). The lens is the workspace paper's J++ (Gurnee et al. 2026). New here: two readers of one word follow different parts of it; the address is the part the lens misses, and swapping it redirects the lookup.

## Open questions

- **Why does the 27B's lookup need J++ only when all 100 directions go together?**
- **Why does the recall follow J++ without needing it at one layer?** Removing it over four layers costs the 9B's recall about a quarter.
- **Does the address exist in natural text?** Refit per format, it is found on the 9B, Muse and Lightning, not the 27B.
- **Does a write at the last token steer the output?** Not on this page: the write at the last token is close to steering the output, and its 1x and 2x doses disagree.

## Appendix A. Links

Every number on this page carries a source comment into figures/story/data.csv or docs/x0_numbers.json; where things live: run files under results/, job specs under jobs/c3/, scripts under scripts/. All figures on one page: [the contact sheet](docs/figures_contact_sheet.png). Supplementary figures: [every scene set](figures/supp/s01_split_all_scene_sets.png), [the settings](figures/story/fig01b_settings.png), [every part](figures/supp/s02_parts_all.png), [parts of the same size](figures/story/fig02_specificity.png), [the 27B with more directions](figures/story/fig02b_k_curve.png), [the J++ part taken out at one layer](figures/story/fig01c_zeroing.png), [the main test's parts](figures/story/fig05b_identity_outside.png), [a described bridge](figures/story/fig05c_described_bridge.png), [the order split with every model](figures/supp/s03_order_split.png), [the layer sweep](figures/story/fig03b_layers.png), [the link copy variants](figures/supp/s03d_link_copy_variants.png), [the lookups the change misses](figures/supp/s03e_cumulative.png), [the depth candidate on the main test](figures/story/fig06_depth.png), [the address across depth](figures/story/fig06c_address_depth.png), [the recall follows the swap](figures/supp/s07_recall_follows_swap.png), [the lens readout of the swap](figures/supp/s07b_lens_readout.png), [the lookup's errors](figures/story/fig07c_probe_errors.png), [the first locker](figures/story/fig08_first_locker.png), [the first sentence and the moves](figures/supp/s08b_pointer_moves_and_neutral_sentence.png), [the routes test drawn large](figures/supp/s04_routes_design.png), [every routes arm](figures/supp/s05_routes_all_arms.png), [the blocked pick sentence](figures/story/fig09c_formation.png), [chained addresses](figures/story/fig09d_chain.png), [what is left of the route](figures/story/fig10_what_is_left.png), [attribute probe and MLPs](figures/story/fig10b_enrichment.png), [binding](figures/story/fig10c_binding.png), [heads](figures/story/fig10d_heads.png), [second route](figures/story/fig10e_second_route.png), [the mechanism tests](figures/story/fig15_mechanisms.png), [attention follows the swapped address](figures/story/fig13_attention.png), [learned subspaces](figures/story/fig14_learned.png), [Muse's learned subspaces](figures/supp/s12_das_muse.png), [the transfer on every model](figures/story/fig09_transfer.png). Earlier figures: [figures/status_2026-10-25/](figures/status_2026-10-25/).
