# Draft: Q46.2 and Q46.3 (45s on Nemotron-3.5-Lightning), for predictions/2026-10-27_dan.md

To paste into predictions/2026-10-27_dan.md in place of the line "**Q46.2, Q46.3** (45s on Nemotron-3.5-Lightning: ...) are added here, unanswered, ...". The sealed verdict (scripts/x45s.py verdict) reads each question's own block (the line that starts with its bold id, up to the next question) and that block's single "Dan:" line; it refuses until both are filled and committed.

---

**Q46.2** (45s-a, added 27 Oct ~15:00; DRAFT, not queued until this is answered and Zach's lens file is on our box; rule fixed before any run, jobs/c3/x45s_a_lightning.yaml) On Nemotron-3.5-Lightning, at L30, in our main test (two people swap picks), does the recall need the J++ part of the bridge word's change while the lookup does not?

Our main test has run on four models, each at a layer fixed in advance, and the split held on all four. Lightning is Zach's second family: a hybrid of Mamba-2, attention and mixture-of-experts blocks (52 blocks), read with his J++ lens. His knock-out on Lightning, the top 10 J++ directions taken out at every token over L27-33, costs recall answers 52 points more than stated-fact answers on his dev items, and the logit lens's own top 10 cost 2 (EXPERIMENTS.md, 26 Oct). Our side has never run on Lightning. 45s-a runs our main test at L30, the middle of his band (Dan, 27 Oct): the bridge word's change at L30, whole, without its J++ part (25 directions), and without a random part of the same size, read by the lookup and by the recall. On Lightning's tokenizer, 516 of the 600 scenes keep the bridge as one token; the first 200 that pass the read gate are used. One thing is known before the run: on Muse, also 52 blocks, the bridge word's change at L30 switched only 4% of lookups (recall 41%), below the 30% the rule needs, so (d) is a real outcome here.
- (a) confirmed: the lookup's extra loss (the share of switches lost without the J++ part, minus that lost without a random part of the same size) is at most 0.10, and the recall loses at least 0.30 of its switches without the J++ part;
- (b) not confirmed: neither (a) nor (c);
- (c) killed: the lookup's extra loss is at least 0.20, or the recall loses less than 0.20 of its switches without the J++ part;
- (d) can't tell: the whole change switches less than 30% (or fewer than 30) of either reader's items, or the read gate fails (below 0.80, or fewer than 150 scenes both readers read right).

Rule: jobs/c3/x45s_a_lightning.yaml (the main test's rule, jobs/c3/X0.md, at L30). Point estimates decide; the gap, its logit-difference and probability versions and the split by sentence order are reported beside it.

Dan:

**Q46.3** (45s-b, added 27 Oct ~15:00; DRAFT, not queued until this is answered and Zach's lens file is on our box; rule fixed before any run, jobs/c3/x45s_b_lightning.yaml) On Nemotron-3.5-Lightning, at L30, in the clean one-pick design, does the split hold where the locker sentences come before the pick?

The clean design (45m) adds one locker item that nobody picks and makes it the asked person's pick, so only the bridge token changes. It held on the 27B (gap 0.53) and Muse (0.38) and missed on the 9B (0.23); the bar is a gap of at least 0.3 with the lookup's extra loss at most 0.10, in scenes where both items' locker sentences come before the asked pick. The gap is the recall's extra loss minus the lookup's. 45s-b runs the same design on Lightning at L30, with the same three arms as 45s-a, on every scene that passes the read gate. On Lightning's tokenizer, 559 of the 600 scenes are made; 198 of them have both lockers before the pick (before the gate). On Lightning alone, 45m's rule is read per model: Lightning is not added to 45m's count of 2 of 3 models.
- (a) holds: in locker-before scenes, gap at least 0.3 and the lookup's extra loss at most 0.10;
- (b) does not hold: tested, and one of the two bars is missed;
- (c) not tested: the read gate fails (below 0.80, or fewer than 150 scenes), or no locker-before item switches under the whole change.

Rule: jobs/c3/x45s_b_lightning.yaml (45m's rule, jobs/c3/batch45.yaml, its per-model clause on Lightning). Point estimates decide; locker-after, all scenes, and the gap's logit-difference and probability versions are reported beside it.

Dan:
