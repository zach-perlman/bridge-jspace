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

### E3. The lookup's identity route runs outside the lens <a id="e3-identity"></a>

- **Hypothesis.** The lookup's answers by the identity route fall at least 0.30 beyond random without lens directions 26-100, or under 0.10 (outside the lens). Fixed in advance.
- **Mechanics.** Lens directions 1-25, 26-100 or both taken out of the change, against a random part.
- **Data.** Routes scenes, 300 items per model.
- **Result.** Identity route without 1-25 / 26-100 / both: {{dp|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 1-25}} / {{dp|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|9b|47.1: identity route: answers lost beyond random without lens directions 1-100}} (9B), {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 1-25}} / {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|27b|47.1: identity route: answers lost beyond random without lens directions 1-100}} (27B), {{dp|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 1-25}} / {{dp|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 26-100}} / {{dp|fig05d|muse|47.1: identity route: answers lost beyond random without lens directions 1-100}} (Muse), {{dp|e3_identity|nemotron-3.5-lightning|47.1: identity answers lost beyond random without lens directions 1-25}} / {{dp|e3_identity|nemotron-3.5-lightning|47.1: identity answers lost beyond random without lens directions 26-100}} / {{dp|e3_identity|nemotron-3.5-lightning|47.1: identity answers lost beyond random without lens directions 1-100}} (Lightning ○); position route at most {{dp|fig05d||47.1: position route: the most answers lost beyond random, over the models and slices}}; the 122B not run.
- **Figure.**

![The lookup's identity route runs outside the lens; the position route never touches it](figures/story/fig05d_routes_lens.png)

- **Conclusion.** The identity route survives the loss of lens directions 26-100 on all four models and of 1-25 on the 9B, Muse and Lightning; on the 27B the two slices are redundant copies. Not shown: the identity code itself.

### E5. Identity, position, never the value <a id="e5-routes"></a>

- **Hypothesis.** The lookup follows the item's identity, its locker's position, or the number. Fixed in advance.
- **Mechanics.** The change comes from a prompt where another item's locker sentence moved and took a new number; each route predicts a different locker. Whole change; without the address, against a random part.
- **Data.** Routes scenes, 300 items per model.
- **Result.** Identity / position {{pt|rt_C2_whole_identity_9b}} / {{pt|rt_C2_whole_position_9b}} (9B), {{pt|rt_C2_whole_identity_27b}} / {{pt|rt_C2_whole_position_27b}} (27B), {{pt|rt_C2_whole_identity_muse}} / {{pt|rt_C2_whole_position_muse}} (Muse), {{dp|fig05|nemotron-3.5-lightning|another item moved, whole: identity share}} / {{dp|fig05|nemotron-3.5-lightning|another item moved, whole: position share}} (Lightning ○), {{pt|rtg_C2_whole_identity_122b}} / {{pt|rtg_C2_whole_position_122b}} (122B°); the value never, in any format.
- **Figure.**

![The lookup takes the identity route or the position route, never the value](figures/story/fig05_routes.png)
*The design is drawn on the setup figure's items; the routes test's own scenes are animals. The 122B° fifth: its gate lowered to 0.75 after the data.*

The same routes by depth:

![The address forms early; identity route first, position route later](figures/story/fig06b_anatomy.png)

- **Conclusion.** The lookup reads what the item is and where it sits. Not shown: who reads the position (the dereference test is running).

## Part III. The address: where the item's locker sits

*The lookup's second input is a code for where the locker sentence sits.*

### E6. The address: probe, remove, add, swap <a id="e6-address"></a>

- **Hypothesis.** Removing the address stops position answers; adding it alone creates them; swapping it moves the lookup. Fixed in advance; probe post hoc.
- **Mechanics.** Removed or kept alone, against a random part; swapped (two slot means' difference) against a random vector of its size.
- **Data.** Routes scenes, 300 items per model.
- **Result.** A probe reads it in {{num|v4_b_before_122b}}-{{num|v4_b_before_27b}} of scenes ({{dp|fig07|nemotron-3.5-lightning|the locker probe at the bridge word, locker-first scenes}} on Lightning ○). Without it position answers drop to {{pt|rt_C2_no_alf_position_9b}} / {{pt|rt_C2_no_alf_position_27b}} / {{pt|rt_C2_no_alf_position_muse}} / {{dp|fig05|nemotron-3.5-lightning|another item moved, no_alf: position share}} ○ / {{pt|rtg_C2_no_alf_position_122b}}° (random {{pt|rt_C2_no_alf_rand_position_9b}} / {{pt|rt_C2_no_alf_rand_position_27b}} / {{pt|rt_C2_no_alf_rand_position_muse}} / {{dp|fig05|nemotron-3.5-lightning|another item moved, no_alf_rand: position share}} ○ / {{pt|rtg_C2_no_alf_rand_position_122b}}°); alone it gives {{pt|rtk_C2_keep_alf_position_9b}} / {{pt|rtk_C2_keep_alf_position_27b}} / {{pt|rtk_C2_keep_alf_position_muse}} / {{dp|fig07|nemotron-3.5-lightning|another item moved, keep_alf: position share}} ○ / {{pt|rtk_C2_keep_alf_position_122b}}°; a swap at a real change's size (s = 2) moves {{dp|fig07|9b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|27b|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|muse|lookup target share, mean over locker pairs, s = 2}} / {{dp|fig07|nemotron-3.5-lightning|lookup target share, mean over locker pairs, s = 2}} ○ / {{pt|x8_t2_122b}}° (122B, pooled over locker pairs) of lookups, {{dp|e6_distance|9b|47.16: the swap (fit with none) sends lookups to the target, 50 sentences}} after 50 neutral sentences (9B). The 122B's routes and swap runs had their gate lowered to 0.75 after the data (°): its 0.80 routes run missed it on the recall.
- **The recall under the swap** (descriptive). At s = 2 the swap changes {{dp|cards|9b|the address swap at s = 2: recalls that change}} / {{dp|cards|27b|the address swap at s = 2: recalls that change}} / {{dp|cards|muse|the address swap at s = 2: recalls that change}} / {{dp|cards|nemotron-3.5-lightning|the address swap at s = 2: recalls that change}} ○ / {{dp|cards|122b|the address swap at s = 2: recalls that change}}° of recalls; of those, {{dp|cards|9b|the address swap at s = 2: changed recalls naming the swapped-in item's answer}} (9B) and {{dp|cards|nemotron-3.5-lightning|the address swap at s = 2: changed recalls naming the swapped-in item's answer}} ○ (Lightning) name the swapped-in item's answer. The address points to the item; the lookup always follows it, the recall sometimes.
- **Note.** The swap's rule fixed in advance was read at s = 1 (one times the slot difference) and said no on every model. That was a design error: s = 1 is below a real change's size. The swap numbers above are at s = 2.
- **Figure.**

![The address carries the position route; swapping it moves the lookup](figures/story/fig07_writes.png)

- **Conclusion.** The address is causal and survives distance. Not shown: who reads it.

### E7. Six lockers: swaps between given lockers <a id="e7-code"></a>

- **Hypothesis.** The address is a line over slots (one shift steps the lookup one slot), first-vs-rest, or one code per slot. Fixed in advance.
- **Mechanics.** Six-locker scenes: one shift per start slot and swaps between given slots, against a random direction.
- **Data.** 300 items each, 9B and Muse; the 27B and Lightning since; the 122B not run. On the 9B the code was then fit three ways on held-out items.
- **Result.** No single shift reaches the bar on any model; swaps between given lockers reach it on {{dp|fig09b|9b|47.2: pairwise writes reaching 25% (dose 2)}} / {{dp|cards|27b|47.2: pairwise writes reaching 25% (dose 2)}} / {{dp|fig09b|muse|47.2: pairwise writes reaching 25% (dose 2)}} / {{dp|fig09b|nemotron-3.5-lightning|47.2: pairwise writes reaching 25% (dose 2)}} ○ of 30 pairs (9B / 27B / Muse / Lightning). The code's size on the 9B: {{dp|cards|9b|51.11 part 1: the code's size}}; swaps to a midpoint slot reach it in {{dp|cards|9b|51.11 part 3: midpoint swaps reaching the slot between, from the first slot (dose 2)}} of cases against {{dp|cards|9b|51.11 part 3: full swaps reaching their target (dose 2)}} for full swaps, so the slots are not a metric order.
- **Figure.**

![Six lockers: swaps between given lockers work on most pairs, no single shift does](figures/story/fig09b_six_lockers.png)

- **Conclusion.** A given locker can be targeted on most pairs on the 9B, Muse and Lightning, not on the 27B; the code's size is not settled. Not shown: whether the code is shared across item kinds (Part VI).

### E8. The lens is blind to the address <a id="e8-blind"></a>

- **Hypothesis.** Through the J++ lens an address swap looks like a random draw. Descriptive.
- **Mechanics.** The swap against 200 random draws: any position word's best rank and the share rebuilt; an identity change as control.
- **Data.** 200 cases per model; the 122B not run.
- **Result.** The lens rebuilds {{dp|fig07b_verbal|9b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|27b|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|fig07b_verbal|muse|47.0 (b) share rebuilt by 25 lens directions: pointer}} / {{dp|cards|nemotron-3.5-lightning|47.0 (b) share rebuilt by 25 lens directions: pointer}} ○ of the swap: as for random draws on the 9B, 27B and Muse; on Lightning a little more than its random draws ({{dp|cards|nemotron-3.5-lightning|47.0 (b) share rebuilt by 25 lens directions: random draws (mean)}}), still a small share. Asked for the position, the 27B's lens top five hold the right ordinal in {{dp|e8_report|27b|47.10: lens top-5 holds the right ordinal (report prompt)}} of reports, yet it loses {{dp|e8_report|27b|47.10: the report's extra loss without the address}} without the address.
- **Figure.**

![The lens reads which item is at the bridge, not where its locker sits](figures/story/fig07b_verbal.png)

- **Conclusion.** A lens monitor sees which item is at the bridge, not where the model will look. Not shown: a probe-based monitor.

## Part IV. Where and when the link is made

*The bridge word can only point back, so the order decides where the link is made, and the address is written early and used late.*

### E10. Sentence order: where the link is made <a id="e10-order"></a>

- **Hypothesis.** Locker after the pick: copying the changed prompt's locker-sentence states at L carries at least half the switches. Link rule fixed in advance, order split post hoc.
- **Mechanics.** Main test split by order; clean scenes; copies into the locker sentences per layer.
- **Data.** 200 items per model.
- **Result.** Lookups switch in {{num|lk_order_before_muse}}-{{num|lk_order_before_122b}} of locker-first scenes, {{num|lk_order_after_27b}}-{{num|lk_order_after_9b}} otherwise; Lightning {{dp|fig03|nemotron-3.5-lightning|lookups switched by the whole change, locker sentence before the pick}} / {{dp|fig03|nemotron-3.5-lightning|lookups switched by the whole change, locker sentence after the pick}} ○. The copy carries {{pt|x45q_c_9b}} / {{pt|x45q_c_27b}} / {{pt|x45q_c_muse}}; on Lightning the copy test is not tested (gate: its clean one-pick recall is below 0.80); below gate, descriptive only, the copy carries {{d|fig03|nemotron-3.5-lightning|45q, the rule's arm c: copy at L, every locker-sentence token (lookups switched)}} and the bridge-word change {{d|fig03|nemotron-3.5-lightning|45q, the rule's arm a: the bridge-word change at L (lookups switched)}}, as on the other models.
- **Figure.**

![Locker after the pick: the link is made in the locker sentences](figures/story/fig03_order.png)

- **Conclusion.** The bridge word links only when the locker came first. Not shown: what the locker sentence holds.

### E11. Token by token, layer by layer <a id="e11-map"></a>

- **Hypothesis.** Locker after the pick: one locker-sentence cell carries the lookup, which stops reading the bridge word before the recall. Fixed in advance.
- **Mechanics.** The changed prompt's state placed into one token group at one layer, every other layer.
- **Data.** Clean scenes, 9B and Muse; since then the 27B (clean scenes and the main test) and Lightning (the main test only); the 122B not run.
- **Result.** Both fail: no single cell carries the locker-after lookup, which reads the bridge word early; both readers read it to about the same depth, then the question and last token carry the answer. Of the locker-after lookups the change at L misses, the bridge word before L carries {{dp|e11_before_l|9b|47.4: main, locker after the pick: lookups carried by the bridge word before L}} / {{dp|e11_before_l|27b|47.4: main, locker after the pick: lookups carried by the bridge word before L}} / {{dp|e11_before_l|muse|47.4: main, locker after the pick: lookups carried by the bridge word before L}} / {{dp|e11_before_l|nemotron-3.5-lightning|47.4: main, locker after the pick: lookups carried by the bridge word before L}} ○ (main test).
- **Figure.**

![Locker after the pick: the lookup leaves the bridge word early](figures/story/fig03d_depth_map.png)

- **Conclusion.** The link is spread over tokens and layers. The 27B and Lightning, run since, fail the same readings; the 27B's recall reads the bridge word up to the start of Zach's late band, as the 9B's.

### E12. The anatomy by depth <a id="e12-anatomy"></a>

- **Hypothesis.** The lookup drops the J++ part by the time it takes up the address, which is readable earlier; never the value. Fixed in advance.
- **Mechanics.** The change's parts per sampled layer against random parts, and a slot probe.
- **Data.** Routes scenes split in halves; 9B and Muse; the 27B on two grids (first a reduced one, then every fourth layer); Lightning; the 122B not run.
- **Result.**
  - (b) The address is readable before the lookup uses it, on all four: readable from / position route from layer {{dp|cards|9b|47.8: the address readable from}} / {{dp|cards|9b|47.8: the first layer of the position route}} (9B), {{dp|cards|27b|47.8 (full grid): the address readable from}} / {{dp|cards|27b|47.8 (full grid): the first layer of the position route}} (27B, full grid), {{dp|cards|muse|47.8: the address readable from}} / {{dp|cards|muse|47.8: the first layer of the position route}} (Muse), {{dp|cards|nemotron-3.5-lightning|47.8: the address readable from}} / {{dp|cards|nemotron-3.5-lightning|47.8: the first layer of the position route}} ○ (Lightning).
  - (d) Never the value, on all four.
  - (a) The handoff (the lookup stops needing the J++ part by the layer its position route starts) holds on the 9B, Muse and Lightning, and on the 27B's reduced grid ({{dp|cards|27b|47.8 (reduced grid): the last layer the lookup needs the J++ part}} / {{dp|cards|27b|47.8 (reduced grid): the first layer of the position route}}). On the 27B's full grid it fails: the lookup still needs the J++ part at layer {{dp|cards|27b|47.8 (full grid): the last layer the lookup needs the J++ part}}, after its position route starts at layer {{dp|cards|27b|47.8 (full grid): the first layer of the position route}}. The handoff depends on the layer grid.
  - The address settles late: mean overlap across depth {{dp|fig06c|9b|D4: the address's mean overlap over every pair of window layers}} / {{dp|cards|27b|D4: the address's mean overlap over every pair of window layers}} / {{dp|fig06c|muse|D4: the address's mean overlap over every pair of window layers}} / {{dp|cards|nemotron-3.5-lightning|D4: the address's mean overlap over every pair of window layers}} ○.
- **Figure.**

![The address forms early; identity route first, position route later](figures/story/fig06b_anatomy.png)

- **Conclusion.** The address is written before it is read, and the lookup never reads the value, on all four models; whether the lookup lets go of the J++ part before it takes up the address depends on which layers are sampled. Position grows with depth on the main test too (candidate).

### The recall's bridge entity at the last token: readable through the lens, not used

- **Question.** At the last token, is the bridge entity in the lens part of the state, and does the model use it there?
- **Why we asked.** The cards above work at the bridge word; a lens monitor reads the last token, where the answer is written.
- **Data.** Main test, scenes with the locker sentence first: {{dp|cards|9b|51.10: main-test scenes, locker first}} / {{dp|cards|27b|51.10: main-test scenes, locker first}} / {{dp|cards|muse|51.10: main-test scenes, locker first}} / {{dp|cards|nemotron-3.5-lightning|51.10: main-test scenes, locker first}} ○.
- **Method.** At the last token, every fourth layer before the answer appears:
  - read: a probe for the bridge entity on the lens part of the state (and the lens's top five), against the probe on the whole state;
  - write, at the layer the read peaks: the lens part of the changed prompt's state swapped in, against the whole state patched in; control: a random part of the same size;
  - what the model then outputs (descriptive): its clean answer, the changed prompt's answer, another digit, the entity's name or a number word.
- **Rule, fixed in advance.** "Read: through-the-lens probe ≥ 0.8 and lens top-5 ≥ 0.5 at some layer before the answer digit's layer, while the full-residual probe ≥ 0.9 there. Write: at the layer of the read peak, his swap or the J++ part of the change (gain ≤ 2) switches ≥ 0.5 of what the whole-state patch switches at that layer, with the random part ≤ 0.10. (b) readable, not used: read holds, write fails." Lightning: the same rule, copied.
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

![The recall's entity at the last token: readable through the lens, not used](figures/story/fig17_jspace_last_token.png)
*At the last token, per reader and model: the probe's accuracy on the lens part of the state (read) and the lens swap's switches as a share of the whole-state patch's (swap), both at the layer where the read peaks; Lightning hollow; 122B not run.*

## Part V. Other datasets and operations

*Our removal on Zach's passages and his operation on our scenes. The 122B: not run.*

- **His true-fact passages** (the final fact stated in the lookup's passage): the lookup follows the lens part too on the 9B and 27B ({{d|cards|9b|Z1: lookup, switches lost beyond a random part}} / {{d|cards|27b|Z1: lookup, switches lost beyond a random part}} lost beyond random); Muse's lookup switches rarely there; Lightning is {{dp|cards|nemotron-3.5-lightning|Z1: the rule's reading}} ○ ({{dp|cards|nemotron-3.5-lightning|Z1: lookup, switches lost beyond a random part}}).
- **His made-up-fact passages** (same rule): on the 9B {{dp|cards|9b|Z1-P: the rule's reading}} (lookup {{d|cards|9b|Z1-P: lookup, switches lost beyond a random part}}, recall {{dp|cards|9b|Z1-P: recall, switches lost beyond a random part}}, gap {{dp|cards|9b|Z1-P: the gap}}); on the 27B {{dp|cards|27b|Z1-P: the rule's reading}} (lookup {{d|cards|27b|Z1-P: lookup, switches lost beyond a random part}}, recall {{dp|cards|27b|Z1-P: recall, switches lost beyond a random part}}, gap {{dp|cards|27b|Z1-P: the gap}}); Lightning not tested (gate {{dp|cards|nemotron-3.5-lightning|Z1-P: the gate (the lookup's read accuracy on the original passages)}} < 0.80), descriptive only ○: lookup {{d|cards|nemotron-3.5-lightning|Z1-P: lookup, switches lost beyond a random part}}, recall {{dp|cards|nemotron-3.5-lightning|Z1-P: recall, switches lost beyond a random part}}, gap {{dp|cards|nemotron-3.5-lightning|Z1-P: the gap}}.
- **The full carrier** (every token before L changed): fact-after lookups follow the lens part ({{dp|cards|9b|51.7: fact-after lookups, full carrier: switches lost beyond a random part}} / {{dp|cards|27b|51.7: fact-after lookups, full carrier: switches lost beyond a random part}} / {{dp|cards|nemotron-3.5-lightning|51.7: fact-after lookups, full carrier: switches lost beyond a random part}} ○ lost beyond random; 9B / 27B / Lightning).
- **The routes test on his passages:** position answers under the whole change {{dp|cards|9b|Z3: position share under the whole change}} / {{dp|cards|27b|Z3: position share under the whole change}} / {{dp|cards|muse|Z3: position share under the whole change}} / {{dp|cards|nemotron-3.5-lightning|Z3: position share under the whole change}} ○: no position route on the 27B; the others in between.
- The two operations differ in scope, so only their sign and their order are comparable.

![Both operations, both datasets, one direction](figures/story/fig12_two_by_two.png)

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
