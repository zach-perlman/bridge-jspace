# 48.3 examples (verify pack): prompts exactly as the model reads them; ⟦bridge:…⟧ the bridge word, ⟦write:…⟧ the written sentence's item and number tokens. UNVERIFIED.

## qwen35_9b_x48_bind: 10 random written scenes of 97 (seed 0)

### P2-L0-0040 (main, elements): bridge lithium picked by Ryan; written: carbon (picked by Emma; locker 5, attribute 6)

**lookup** (PP-L0-0040): O's answer 2, the written item's 5

```
<|im_start|>user
The locker of helium is four. Ryan picked ⟦bridge:lithium⟧. The locker of lithium is two. Emma picked carbon. Vera picked helium. The locker of ⟦write:carbon⟧ is ⟦write:five⟧.
Which locker belongs to Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | ' 2\n' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | ' 2\n' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | ' 2\n' |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | ' 2\n' |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | ' 2\n' |

**recall** (PM-L0-0040): O's answer 3, the written item's 6

```
<|im_start|>user
The locker of helium is four. Ryan picked ⟦bridge:lithium⟧. The locker of lithium is two. Emma picked carbon. Vera picked helium. The locker of ⟦write:carbon⟧ is ⟦write:five⟧.
What is the atomic number of Ryan's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | ' 3\n' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | ' 3\n' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | ' 3\n' |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | ' 3\n' |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | ' 3\n' |

### P2-L0-0010 (45m, elements): bridge oxygen picked by Grace; written: hydrogen (picked by Adam; locker 4, attribute 1)

**lookup** (PP-L0-0010): O's answer 3, the written item's 4

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked ⟦bridge:oxygen⟧. The locker of oxygen is 3. The locker of helium is 8. The locker of ⟦write:hydrogen⟧ is ⟦write:4⟧. Oscar picked carbon.
Which locker belongs to Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | ' 3\n' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | ' 3\n' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | ' 3\n' |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | ' 3\n' |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | ' 3\n' |

**recall** (PM-L0-0010): O's answer 8, the written item's 1

```
<|im_start|>user
The locker of carbon is 7. Adam picked hydrogen. Grace picked ⟦bridge:oxygen⟧. The locker of oxygen is 3. The locker of helium is 8. The locker of ⟦write:hydrogen⟧ is ⟦write:4⟧. Oscar picked carbon.
What is the atomic number of Grace's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | original | ' 8\n' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '8' | original | ' 8\n' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '8' | original | ' 8\n' |
| r1 | a random vector of the s = 1 write's norm, per token | '8' | original | ' 8\n' |
| r2 | a random vector of the s = 2 write's norm, per token | '8' | original | ' 8\n' |

### P2-L0-0085 (45m, elements): bridge helium picked by Will; written: nitrogen (picked by Max; locker 4, attribute 7)

**lookup** (PP-L0-0085): O's answer 5, the written item's 4

```
<|im_start|>user
Julia picked lithium. Max picked nitrogen. Will picked ⟦bridge:helium⟧. The locker of helium is 5. The locker of ⟦write:nitrogen⟧ is ⟦write:4⟧. The locker of lithium is 1. The locker of hydrogen is 7.
Which locker belongs to Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '5' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '5' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '5' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '5' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '5' | original | None |

**recall** (PM-L0-0085): O's answer 2, the written item's 7

```
<|im_start|>user
Julia picked lithium. Max picked nitrogen. Will picked ⟦bridge:helium⟧. The locker of helium is 5. The locker of ⟦write:nitrogen⟧ is ⟦write:4⟧. The locker of lithium is 1. The locker of hydrogen is 7.
What is the atomic number of Will's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | None |

### P2-L0-0157 (45m, elements): bridge oxygen picked by Julia; written: carbon (picked by Amy; locker 1, attribute 6)

**lookup** (PP-L0-0157): O's answer 9, the written item's 1

```
<|im_start|>user
Julia picked ⟦bridge:oxygen⟧. Amy picked carbon. The locker of hydrogen is 5. The locker of nitrogen is 6. The locker of ⟦write:carbon⟧ is ⟦write:1⟧. Tom picked nitrogen. The locker of oxygen is 9.
Which locker belongs to Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '9' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '9' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '9' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '9' | original | None |

**recall** (PM-L0-0157): O's answer 8, the written item's 6

```
<|im_start|>user
Julia picked ⟦bridge:oxygen⟧. Amy picked carbon. The locker of hydrogen is 5. The locker of nitrogen is 6. The locker of ⟦write:carbon⟧ is ⟦write:1⟧. Tom picked nitrogen. The locker of oxygen is 9.
What is the atomic number of Julia's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '8' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '8' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '8' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '8' | original | None |

### P2-L0-0178 (45m, elements): bridge carbon picked by Lily; written: oxygen (picked by Ryan; locker 3, attribute 8)

**lookup** (PP-L0-0178): O's answer 7, the written item's 3

```
<|im_start|>user
The locker of helium is four. Lily picked ⟦bridge:carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of ⟦write:oxygen⟧ is ⟦write:three⟧. The locker of lithium is five. Olivia picked helium.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | None |

**recall** (PM-L0-0178): O's answer 6, the written item's 8

```
<|im_start|>user
The locker of helium is four. Lily picked ⟦bridge:carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of ⟦write:oxygen⟧ is ⟦write:three⟧. The locker of lithium is five. Olivia picked helium.
What is the atomic number of Lily's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '6' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '6' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '6' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '6' | original | None |

### P2-L0-0205 (45m, elements): bridge oxygen picked by Ella; written: lithium (picked by Beth; locker 8, attribute 3)

**lookup** (PP-L0-0205): O's answer 1, the written item's 8

```
<|im_start|>user
The locker of carbon is three. Ella picked ⟦bridge:oxygen⟧. Max picked carbon. The locker of oxygen is one. Beth picked lithium. The locker of hydrogen is six. The locker of ⟦write:lithium⟧ is ⟦write:eight⟧.
Which locker belongs to Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '1' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '1' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '1' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '1' | original | None |

**recall** (PM-L0-0205): O's answer 8, the written item's 3

```
<|im_start|>user
The locker of carbon is three. Ella picked ⟦bridge:oxygen⟧. Max picked carbon. The locker of oxygen is one. Beth picked lithium. The locker of hydrogen is six. The locker of ⟦write:lithium⟧ is ⟦write:eight⟧.
What is the atomic number of Ella's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '8' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '8' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '8' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '8' | original | None |

### P2-L0-0224 (45m, greek): bridge delta picked by Tara; written: beta (picked by Vera; locker 4, attribute 2)

**lookup** (PP-L0-0224): O's answer 6, the written item's 4

```
<|im_start|>user
Tara picked ⟦bridge:delta⟧. The locker of delta is six. The locker of epsilon is seven. Vera picked beta. Max picked epsilon. The locker of ⟦write:beta⟧ is ⟦write:four⟧. The locker of alpha is five.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '6' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '6' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '6' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '6' | original | None |

**recall** (PM-L0-0224): O's answer 4, the written item's 2

```
<|im_start|>user
Tara picked ⟦bridge:delta⟧. The locker of delta is six. The locker of epsilon is seven. Vera picked beta. Max picked epsilon. The locker of ⟦write:beta⟧ is ⟦write:four⟧. The locker of alpha is five.
Which position in the Greek alphabet does Tara's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | original | None |

### P2-L0-0277 (45m, elements): bridge carbon picked by Lucy; written: helium (picked by Sean; locker 8, attribute 2)

**lookup** (PP-L0-0277): O's answer 5, the written item's 8

```
<|im_start|>user
Lucy picked ⟦bridge:carbon⟧. The locker of oxygen is seven. The locker of lithium is six. The locker of carbon is five. Sean picked helium. The locker of ⟦write:helium⟧ is ⟦write:eight⟧. Jack picked oxygen.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '5' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '5' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '5' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '5' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '5' | original | None |

**recall** (PM-L0-0277): O's answer 6, the written item's 2

```
<|im_start|>user
Lucy picked ⟦bridge:carbon⟧. The locker of oxygen is seven. The locker of lithium is six. The locker of carbon is five. Sean picked helium. The locker of ⟦write:helium⟧ is ⟦write:eight⟧. Jack picked oxygen.
What is the atomic number of Lucy's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '6' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '6' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '6' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '6' | original | None |

### P2-L0-0284 (45m, greek): bridge delta picked by Kyle; written: epsilon (picked by Hugo; locker 3, attribute 5)

**lookup** (PP-L0-0284): O's answer 7, the written item's 3

```
<|im_start|>user
Kyle picked ⟦bridge:delta⟧. Julia picked beta. Hugo picked epsilon. The locker of ⟦write:epsilon⟧ is ⟦write:three⟧. The locker of delta is seven. The locker of beta is four. The locker of gamma is five.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | None |

**recall** (PM-L0-0284): O's answer 4, the written item's 5

```
<|im_start|>user
Kyle picked ⟦bridge:delta⟧. Julia picked beta. Hugo picked epsilon. The locker of ⟦write:epsilon⟧ is ⟦write:three⟧. The locker of delta is seven. The locker of beta is four. The locker of gamma is five.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | original | None |

### P2-L0-0310 (45m, elements): bridge helium picked by Victor; written: lithium (picked by David; locker 4, attribute 3)

**lookup** (PP-L0-0310): O's answer 5, the written item's 4

```
<|im_start|>user
The locker of carbon is 1. David picked lithium. Victor picked ⟦bridge:helium⟧. Eric picked carbon. The locker of ⟦write:lithium⟧ is ⟦write:4⟧. The locker of helium is 5. The locker of oxygen is 2.
Which locker belongs to Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '5' | original | ' 5\n' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '5' | original | ' 5\n' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '5' | original | ' 5\n' |
| r1 | a random vector of the s = 1 write's norm, per token | '5' | original | ' 5\n' |
| r2 | a random vector of the s = 2 write's norm, per token | '5' | original | ' 5\n' |

**recall** (PM-L0-0310): O's answer 2, the written item's 3

```
<|im_start|>user
The locker of carbon is 1. David picked lithium. Victor picked ⟦bridge:helium⟧. Eric picked carbon. The locker of ⟦write:lithium⟧ is ⟦write:4⟧. The locker of helium is 5. The locker of oxygen is 2.
What is the atomic number of Victor's pick? Answer with a single digit and nothing else.<|im_end|>
<|im_start|>assistant
<think>

</think>

Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '2' | original | ' 2\n' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '2' | original | ' 2\n' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '2' | original | ' 2\n' |
| r1 | a random vector of the s = 1 write's norm, per token | '2' | original | ' 2\n' |
| r2 | a random vector of the s = 2 write's norm, per token | '2' | original | ' 2\n' |

## muse30_x48_bind: 10 random written scenes of 89 (seed 0)

### P2-L0-0052 (main, elements): bridge carbon picked by Zoe; written: nitrogen (picked by James; locker 1, attribute 7)

**lookup** (PP-L0-0052): O's answer 8, the written item's 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of oxygen is 2. Zoe picked ⟦bridge:carbon⟧. James picked nitrogen. The locker of carbon is 8. Adam picked oxygen. The locker of ⟦write:nitrogen⟧ is ⟦write:1⟧.
Which locker belongs to Zoe's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '8' | original | ' 8' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '8' | original | ' 8' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '8' | original | ' 8' |
| r1 | a random vector of the s = 1 write's norm, per token | '8' | original | ' 8' |
| r2 | a random vector of the s = 2 write's norm, per token | '8' | original | ' 8' |

**recall** (PM-L0-0052): O's answer 6, the written item's 7

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of oxygen is 2. Zoe picked ⟦bridge:carbon⟧. James picked nitrogen. The locker of carbon is 8. Adam picked oxygen. The locker of ⟦write:nitrogen⟧ is ⟦write:1⟧.
What is the atomic number of Zoe's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | original | ' 6' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '6' | original | ' 6' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '6' | original | ' 6' |
| r1 | a random vector of the s = 1 write's norm, per token | '6' | original | ' 6' |
| r2 | a random vector of the s = 2 write's norm, per token | '6' | original | ' 6' |

### P2-L0-0058 (45m, elements): bridge hydrogen picked by Carl; written: helium (picked by Peter; locker 4, attribute 2)

**lookup** (PP-L0-0058): O's answer 9, the written item's 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Peter picked helium. David picked oxygen. The locker of oxygen is 5. Carl picked ⟦bridge:hydrogen⟧. The locker of fluorine is 8. The locker of ⟦write:helium⟧ is ⟦write:4⟧. The locker of hydrogen is 9.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '9' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '9' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '9' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '9' | original | None |

**recall** (PM-L0-0058): O's answer 1, the written item's 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Peter picked helium. David picked oxygen. The locker of oxygen is 5. Carl picked ⟦bridge:hydrogen⟧. The locker of fluorine is 8. The locker of ⟦write:helium⟧ is ⟦write:4⟧. The locker of hydrogen is 9.
What is the atomic number of Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '1' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '1' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '1' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '1' | original | None |

### P2-L0-0093 (45m, animals): bridge goat picked by Owen; written: wolf (picked by Anna; locker 5, attribute 4)

**lookup** (PP-L0-0093): O's answer 6, the written item's 5

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the crow is seven. Anna picked the wolf. Eve picked the crow. Owen picked the ⟦bridge:goat⟧. The locker of the goat is six. The locker of the owl is four. The locker of the ⟦write:wolf⟧ is ⟦write:five⟧.
Which locker belongs to Owen's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '6' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '6' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '6' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '6' | original | None |

**recall** (PM-L0-0093): O's answer 4, the written item's 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the crow is seven. Anna picked the wolf. Eve picked the crow. Owen picked the ⟦bridge:goat⟧. The locker of the goat is six. The locker of the owl is four. The locker of the ⟦write:wolf⟧ is ⟦write:five⟧.
How many legs does Owen's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | same | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | same | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | same | None |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | same | None |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | same | None |

### P2-L0-0178 (45m, elements): bridge carbon picked by Lily; written: oxygen (picked by Ryan; locker 3, attribute 8)

**lookup** (PP-L0-0178): O's answer 7, the written item's 3

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. Lily picked ⟦bridge:carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of ⟦write:oxygen⟧ is ⟦write:three⟧. The locker of boron is six. Olivia picked helium.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | None |

**recall** (PM-L0-0178): O's answer 6, the written item's 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. Lily picked ⟦bridge:carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of ⟦write:oxygen⟧ is ⟦write:three⟧. The locker of boron is six. Olivia picked helium.
What is the atomic number of Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '6' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '6' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '6' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '6' | original | None |

### P2-L0-0224 (45m, greek): bridge delta picked by Tara; written: beta (picked by Vera; locker 4, attribute 2)

**lookup** (PP-L0-0224): O's answer 6, the written item's 4

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Tara picked ⟦bridge:delta⟧. The locker of delta is six. The locker of epsilon is seven. Vera picked beta. Max picked epsilon. The locker of ⟦write:beta⟧ is ⟦write:four⟧. The locker of alpha is five.
Which locker belongs to Tara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '6' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | target | None |
| r1 | a random vector of the s = 1 write's norm, per token | '6' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '6' | original | None |

**recall** (PM-L0-0224): O's answer 4, the written item's 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Tara picked ⟦bridge:delta⟧. The locker of delta is six. The locker of epsilon is seven. Vera picked beta. Max picked epsilon. The locker of ⟦write:beta⟧ is ⟦write:four⟧. The locker of alpha is five.
Which position in the Greek alphabet does Tara's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | original | None |

### P2-L0-0269 (45m, greek): bridge delta picked by Amy; written: alpha (picked by Mark; locker 2, attribute 1)

**lookup** (PP-L0-0269): O's answer 9, the written item's 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mark picked alpha. Amy picked ⟦bridge:delta⟧. The locker of epsilon is 4. Beth picked epsilon. The locker of eta is 6. The locker of ⟦write:alpha⟧ is ⟦write:2⟧. The locker of delta is 9.
Which locker belongs to Amy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '9' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '9' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '9' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '9' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '9' | original | None |

**recall** (PM-L0-0269): O's answer 4, the written item's 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Mark picked alpha. Amy picked ⟦bridge:delta⟧. The locker of epsilon is 4. Beth picked epsilon. The locker of eta is 6. The locker of ⟦write:alpha⟧ is ⟦write:2⟧. The locker of delta is 9.
Which position in the Greek alphabet does Amy's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '4' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '4' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '4' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '4' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '4' | original | None |

### P2-L0-0277 (45m, elements): bridge carbon picked by Lucy; written: helium (picked by Sean; locker 8, attribute 2)

**lookup** (PP-L0-0277): O's answer 5, the written item's 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Lucy picked ⟦bridge:carbon⟧. The locker of oxygen is seven. The locker of boron is four. The locker of carbon is five. Sean picked helium. The locker of ⟦write:helium⟧ is ⟦write:eight⟧. Jack picked oxygen.
Which locker belongs to Lucy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '5' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '5' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '5' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '5' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '5' | original | None |

**recall** (PM-L0-0277): O's answer 6, the written item's 2

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Lucy picked ⟦bridge:carbon⟧. The locker of oxygen is seven. The locker of boron is four. The locker of carbon is five. Sean picked helium. The locker of ⟦write:helium⟧ is ⟦write:eight⟧. Jack picked oxygen.
What is the atomic number of Lucy's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '6' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '6' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '6' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '6' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '6' | original | None |

### P2-L0-0322 (45m, elements): bridge hydrogen picked by Ruby; written: oxygen (picked by Max; locker 9, attribute 8)

**lookup** (PP-L0-0322): O's answer 7, the written item's 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Ruby picked ⟦bridge:hydrogen⟧. Max picked oxygen. The locker of boron is eight. The locker of lithium is four. The locker of ⟦write:oxygen⟧ is ⟦write:nine⟧. The locker of hydrogen is seven. Eva picked lithium.
Which locker belongs to Ruby's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | None |

**recall** (PM-L0-0322): O's answer 1, the written item's 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Ruby picked ⟦bridge:hydrogen⟧. Max picked oxygen. The locker of boron is eight. The locker of lithium is four. The locker of ⟦write:oxygen⟧ is ⟦write:nine⟧. The locker of hydrogen is seven. Eva picked lithium.
What is the atomic number of Ruby's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '1' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '1' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '1' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '1' | original | None |

### P2-L0-0323 (45m, greek): bridge eta picked by Lily; written: theta (picked by Mia; locker 9, attribute 8)

**lookup** (PP-L0-0323): O's answer 1, the written item's 9

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Lily picked ⟦bridge:eta⟧. Mia picked theta. The locker of ⟦write:theta⟧ is ⟦write:9⟧. Julia picked alpha. The locker of beta is 6. The locker of eta is 1. The locker of alpha is 8.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | original | ' 1' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '1' | original | ' 1' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '1' | original | ' 1' |
| r1 | a random vector of the s = 1 write's norm, per token | '1' | original | ' 1' |
| r2 | a random vector of the s = 2 write's norm, per token | '1' | original | ' 1' |

**recall** (PM-L0-0323): O's answer 7, the written item's 8

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Lily picked ⟦bridge:eta⟧. Mia picked theta. The locker of ⟦write:theta⟧ is ⟦write:9⟧. Julia picked alpha. The locker of beta is 6. The locker of eta is 1. The locker of alpha is 8.
Which position in the Greek alphabet does Lily's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '7' | original | ' 7' |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '7' | original | ' 7' |
| w2 | s = 2 (mu_Iris - mu_Jack) | '7' | original | ' 7' |
| r1 | a random vector of the s = 1 write's norm, per token | '7' | original | ' 7' |
| r2 | a random vector of the s = 2 write's norm, per token | '7' | original | ' 7' |

### P2-L0-0379 (45m, elements): bridge hydrogen picked by Finn; written: carbon (picked by Sara; locker 1, attribute 6)

**lookup** (PP-L0-0379): O's answer 3, the written item's 1

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Anna picked helium. Sara picked carbon. Finn picked ⟦bridge:hydrogen⟧. The locker of hydrogen is three. The locker of ⟦write:carbon⟧ is ⟦write:one⟧. The locker of fluorine is four. The locker of helium is five.
Which locker belongs to Finn's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '3' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '3' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '3' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '3' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '3' | original | None |

**recall** (PM-L0-0379): O's answer 1, the written item's 6

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Anna picked helium. Sara picked carbon. Finn picked ⟦bridge:hydrogen⟧. The locker of hydrogen is three. The locker of ⟦write:carbon⟧ is ⟦write:one⟧. The locker of fluorine is four. The locker of helium is five.
What is the atomic number of Finn's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

| arm | what | top token | class | greedy |
|---|---|---|---|---|
| none | O unedited | '1' | original | None |
| w1 | s = 1 (mu_Iris - mu_Jack) at the written sentence's item and number tokens | '1' | original | None |
| w2 | s = 2 (mu_Iris - mu_Jack) | '1' | original | None |
| r1 | a random vector of the s = 1 write's norm, per token | '1' | original | None |
| r2 | a random vector of the s = 2 write's norm, per token | '1' | original | None |

