# Figure readability: the 5-second test

Each MAIN figure is shown to a fresh agent with no context (the image only, nothing else read). It states the claim, the main exception, what is covered, and what confused it. A figure it misreads is fixed and tested again. Dan's figure guide, 23 Oct, section 7.

| Figure | Version tested | Claim as read | Exception as read | Read right? | Confusing | Fix |
|---|---|---|---|---|---|---|
| order_identity_main | 1428990 | Position wins for the 1st-2nd sentence, the donor's entity from the 3rd on | Qwen3-32B, scene set 1, 3rd on, "fails" near 0 | yes | Jargon undefined (bridge, donor, swapped in, scene set, memory → prompt); the difference axis is hard to compare; the inset has no model labels; scene sets 1-3 unlabeled; "fails" not clearly attached to its dot | sent to the figure agent |
| counting_main | 1428990 | With a filler moved, answers follow the list order far more than the place in the text | Qwen3-32B (fails) | yes | Patched / label / donor undefined; Gemma's dot looks as low as the 32B's but only the 32B is flagged (it fails per topic, not pooled); column labels not tied to the dots | sent to the figure agent |
