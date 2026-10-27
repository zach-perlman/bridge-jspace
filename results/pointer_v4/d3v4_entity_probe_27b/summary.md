used: ['countries', 'animals', 'body']

| domain | candidates | pass | usable | failed (step) |
|---|---|---|---|---|
| countries | 36 | 36 | True | {} |
| sports | 23 | 14 | False | {"polo": ["chain"], "softball": ["chain"], "pool": ["chain", "cue"], "tennis": ["chain"], "skiing": ["chain"], "fencing": ["chain"], "squash": ["chain", "cue"], "skating": ["fact"], "marathon": ["cue"]} |
| animals | 40 | 34 | True | {"dolphin": ["chain"], "tick": ["chain", "cue"], "shark": ["cue"], "beetle": ["chain", "cue"], "fox": ["cue"], "bat": ["chain", "fact"]} |
| body | 21 | 16 | True | {"nose": ["chain"], "kidney": ["cue"], "cheek": ["cue"], "lung": ["cue"], "thumb": ["chain"]} |
