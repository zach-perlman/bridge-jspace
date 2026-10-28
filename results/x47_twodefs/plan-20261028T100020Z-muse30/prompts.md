# 47.12 plan on muse-glimmer-30b (L26): 5 of the main test's 200 items (seed 0), the lookup's O prompt as the model reads it; ⟦bridge:…⟧ the bridge token, ⟦other:…⟧ the other changed pick token (S changes it too; no arm patches it). Counts in plan.json.

## P2-L0-0019 (locker-first): bridge nitrogen -> oxygen, token 66

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>James picked ⟦other:oxygen⟧. The locker of oxygen is four. The locker of nitrogen is six. Adam picked lithium. ⟦pick:Kyle picked⟧ ⟦bridge:nitrogen⟧⟦pick:.⟧ The locker of lithium is eight.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

## P2-L0-0091 (locker-first): bridge oxygen -> hydrogen, token 73

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>Frank picked ⟦other:hydrogen⟧. The locker of oxygen is seven. Will picked carbon. The locker of carbon is one. The locker of hydrogen is eight. ⟦pick:Clara picked⟧ ⟦bridge:oxygen⟧⟦pick:.
⟧Which locker belongs to Clara's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

## P2-L0-0141 (mixed): bridge bee -> elephant, token 63

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>The locker of the bee is four. Hugo picked the ⟦other:elephant⟧. Will picked the wolf. ⟦pick:Dan picked the⟧ ⟦bridge:bee⟧⟦pick:.⟧ The locker of the elephant is one. The locker of the wolf is seven.
Which locker belongs to Dan's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

## P2-L0-0155 (locker-after): bridge beta -> epsilon, token 44

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦pick:Maria picked⟧ ⟦bridge:beta⟧⟦pick:.⟧ The locker of beta is five. The locker of epsilon is one. The locker of alpha is seven. Luke picked alpha. Rose picked ⟦other:epsilon⟧.
Which locker belongs to Maria's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

## P2-L0-0284 (locker-after): bridge delta -> epsilon, token 44

```
<|begin_of_text|><|start|>system<|message|>You are a helpful AI assistant.
Knowledge cutoff: 2026-01-04.

Reasoning strength: low.

# Valid recipients: "self", "user".<|eot|><|start|>user<|message|>⟦pick:Kyle picked⟧ ⟦bridge:delta⟧⟦pick:.⟧ Julia picked beta. Hugo picked ⟦other:epsilon⟧. The locker of epsilon is three. The locker of delta is seven. The locker of beta is four.
Which locker belongs to Kyle's pick? Answer with a single digit and nothing else.<|eot|><|start|>assistant to=user<|message|>Answer: 
```

