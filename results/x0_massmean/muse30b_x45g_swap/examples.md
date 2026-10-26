# Examples: muse30b_x45g_swap (mode two_routes)

10 random items (seed 0) of 200; the prompt as the model reads it (the chat read appends a space), ⟦the bridge word⟧ where the change is added at layer 26; each arm's answer = the top token at the read step. UNVERIFIED.

## P2-L0-0019 (bridge nitrogen -> oxygen; its locker sentence before the pick)

**lookup** (original 6, changed 4)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ nitrogen⟧. The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 7, changed 8)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked oxygen. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. Kyle picked⟦ nitrogen⟧. The locker of lithium is eight.
What is the atomic number of Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0091 (bridge oxygen -> hydrogen; its locker sentence before the pick)

**lookup** (original 7, changed 8)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ oxygen⟧.
Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), changed answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 8, changed 1)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked hydrogen. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. Clara picked⟦ oxygen⟧.
What is the atomic number of Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

## P2-L0-0106 (bridge lithium -> helium; its locker sentence after the pick)

**lookup** (original 6, changed 9)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Will picked carbon. The locker of helium is 9. Paul picked⟦ lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
Which locker belongs to Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 3, changed 2)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Will picked carbon. The locker of helium is 9. Paul picked⟦ lithium⟧. Amy picked helium. The locker of carbon is 3. The locker of lithium is 6.
What is the atomic number of Paul's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

## P2-L0-0141 (bridge bee -> elephant; its locker sentence before the pick)

**lookup** (original 4, changed 1)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦ bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 6, changed 4)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the elephant. Will picked the wolf. Dan picked the⟦ bee⟧. The locker of the elephant is one. The locker of the wolf is seven.
How many legs does Dan's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0148 (bridge nitrogen -> carbon; its locker sentence after the pick)

**lookup** (original 3, changed 2)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked carbon. Carl picked⟦ nitrogen⟧. Ella picked oxygen. The locker of oxygen is 4. The locker of nitrogen is 3. The locker of carbon is 2.
Which locker belongs to Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 7, changed 6)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Max picked carbon. Carl picked⟦ nitrogen⟧. Ella picked oxygen. The locker of oxygen is 4. The locker of nitrogen is 3. The locker of carbon is 2.
What is the atomic number of Carl's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), changed answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0155 (bridge beta -> epsilon; its locker sentence after the pick)

**lookup** (original 5, changed 1)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 2, changed 5)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Maria picked⟦ beta⟧. The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked epsilon.
Which position in the Greek alphabet does Maria's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

## P2-L0-0175 (bridge lithium -> carbon; its locker sentence before the pick)

**lookup** (original 9, changed 1)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is five. The locker of lithium is nine. Mia picked⟦ lithium⟧. Liam picked carbon. Adam picked hydrogen. The locker of carbon is one.
Which locker belongs to Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 3, changed 6)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of hydrogen is five. The locker of lithium is nine. Mia picked⟦ lithium⟧. Liam picked carbon. Adam picked hydrogen. The locker of carbon is one.
What is the atomic number of Mia's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), changed answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0178 (bridge carbon -> oxygen; its locker sentence after the pick)

**lookup** (original 7, changed 3)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. Lily picked⟦ carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of oxygen is three. Olivia picked helium.
Which locker belongs to Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 6, changed 8)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is four. Lily picked⟦ carbon⟧. Ryan picked oxygen. The locker of carbon is seven. The locker of oxygen is three. Olivia picked helium.
What is the atomic number of Lily's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), changed answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), changed answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), changed answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0187 (bridge hydrogen -> helium; its locker sentence after the pick)

**lookup** (original 6, changed 1)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. Nina picked⟦ hydrogen⟧. Maria picked helium. The locker of hydrogen is 6. The locker of lithium is 2.
Which locker belongs to Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 1, changed 2)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of helium is 1. Grace picked lithium. Nina picked⟦ hydrogen⟧. Maria picked helium. The locker of hydrogen is 6. The locker of lithium is 2.
What is the atomic number of Nina's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), changed answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), changed answer |

## P2-L0-0284 (bridge delta -> epsilon; its locker sentence after the pick)

**lookup** (original 7, changed 3)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

**recall** (original 4, changed 5)

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.
Current date: 2026-10-26.

Reasoning strength: high.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Kyle picked⟦ delta⟧. Julia picked beta. Hugo picked epsilon. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which position in the Greek alphabet does Kyle's pick have? Answer with a single digit and nothing else.<|eot|><|start|>assistantAnswer: 
```

| arm | answer |
|---|---|
| unedited | (not stored), original answer |
| the whole change | (not stored), original answer |
| without J++ | (not stored), original answer |
| without the pointer U | (not stored), original answer |
| without J++ and U | (not stored), original answer |
| without a random part (J++'s share) | (not stored), original answer |
| without a random part (U's share) | (not stored), original answer |
| without a random part (J++ and U's share) | (not stored), original answer |

