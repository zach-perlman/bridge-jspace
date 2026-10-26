# Batch 45 predictions (Dan; questions written 26 Oct ~19:00, before any run)

Answer as in batch 25: one option and a confidence from 50 / 60 / 70 / 80 / 90%, an optional one-line why. No result of a test is opened or reported until this file holds Dan's commit for that test. The designs and rules are in [jobs/c3/batch45.yaml](../jobs/c3/batch45.yaml), fixed in advance. 45.0 is a check (pass / fail), not a question.

**Q45.1** (45g a) Two routes for the recall: on at least 3 of 4 models, in locker-before scenes, the recall's extra loss with J++ and the pointer both removed is at least 0.3 and at least 0.2 above the larger single removal (paired CI excluding 0): (a) yes; (b) no.

Dan:

**Q45.2** (45g b) J++ is the recall's only route when the pick is the first mention: in locker-after scenes, J++ alone gives at least 0.3 and adding the pointer adds less than 0.1: (a) yes; (b) no.

Dan:

**Q45.3** (45a) First mention or first locker: (a) "first locker stated before any item"; (b) "order of lockers, picks ignored"; (c) mixed.

Dan:

**Q45.4** (45d) A pointer outside templates: (a) "pointer elsewhere"; (b) "no linear pointer found"; (c) neither.

Dan:

**Q45.5** (45b) The reading-order explanation holds (the locker-sentence patch at L or L/2 switches at least half of S's lookup switches while the bridge-word change stays at or below 0.25): (a) yes; (b) no.

Dan:

**Q45.6** (45c) A second-vs-third pointer is found (removal halves position on those moves, CI excluding 0, and keep-only gives at least 0.15): (a) on all three models; (b) on one or two; (c) on none.

Dan:

**Q45.7** (45e) Identity outside J++ is specific (both conditions on at least 2 of 3 models): (a) yes; (b) no.

Dan:

**Q45.8** (45i) Without the chat template the split and "never the value" hold (gap at least 0.2, value share 0) on: (a) both models; (b) one; (c) none; (d) not tested (gate).

Dan:
