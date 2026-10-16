# Is the first hop outside the J-space?

Dan Orel & Zach Perlman · Qwen3.6-27B · 2026-10-16 · every number below is human-verified ([VERIFIED.md](VERIFIED.md))
unless marked *unverified*

## Question
In Claude, the bridge of a two-hop question ("the language spoken in the country where the Amazon River ends" →
*Brazil* → *Portuguese*) acts on the answer through the J-space (Gurnee et al. 2026). On open models the J-lens often
fails to show the bridge. Is the bridge acting outside the J-space there, or is the miss about how we read?

## What we found
1. **The miss is mostly where we read.** At the last word the lenses rank the bridge first far above a distractor
   (57% vs 5% of layers 32-48); most of the remaining misses are found at an earlier word (22/30). [A2-A3]
2. **A bridge recalled from memory acts through the J-space, as in Claude.** Swapping only its J-space part flips
   52% of answers (Claude 61%); the rest, with the J-space held fixed, 1% (Claude 6%). [B1]
3. **A variable looked up in the prompt does not.** In brew, a two-step lookup in a colour table, the step is carried
   outside the J-space: the lens can read it but not write it (1%), while a direction nearly orthogonal to the lens
   writes it (34%). [B2-B3]
4. **Readers report what is written into the vector, not what the model uses.** The verbalizers (oracle lens, NLA)
   name a direction the model ignores on 99% of items. [B4]

![B1: J-space part vs remainder](figures/exp02_swaps/v4b/jpart_vs_remainder.png)

*B1: swapping only the J-space part flips the answer, the remainder barely does; Claude's numbers are the black
dashed line.*

## Where the line falls (unverified lead, exp09)
| | used by a recalled fact | used by a lookup in the prompt |
|---|---|---|
| **recalled bridge** | inside the J-space | outside |
| **bound in the prompt** | inside | outside (as brew) |

What uses the variable decides, not where it comes from. Caveat: "used by a lookup" also means "answer read from the
prompt".

![exp09: which part of the lens-free copy acts, by family](figures/exp09_bind_recall/v2/source_use.png)

*Unverified (exp09): which part of the lens-free copy acts in each family. Used by a lookup (right column): the
J-space part 0%, the rest acts. Used by a recalled fact (left): B's J-space part acts (12% vs 0%); R's split is small
both ways (4% vs 7%), so R's "inside" above rests on exp02's swap (82% vs 3%), not on this panel.*

## Limits
- One model, one run; single-token bridges.
- The reference set is 90 prompts (Claude's and ours), mostly places and people; the effects sit there.
- Effects are partial: the J-part swap flips about half of the answers, the bridge swap on the cue phrase 18%, the
  lens-free brew copy about a third.

## Sprint: pick one core direction
- **(a) Use vs answer source.** Families where a lookup uses the variable but the answer comes from memory.
- **(b) What the outside part is.** Does brew's code follow the table row (a pointer, like binding IDs) or the colour?
- **(c) A stronger reference.** Re-decompose against a stronger lens-free bridge direction (contrastive pairs or DAS).

Then generality: Gemma 4 31B (started), a balanced prompt set beyond places and people.

## Questions for Neel
1. Which story is worth sharpening: (2) recalled bridges act through the J-space as in Claude, (3-4) lookup variables
   live outside it and readers cannot tell used from written, or the exp09 line?
2. Does "lookup variables live outside the J-space" sound new, or like binding IDs (Feng & Steinhardt 2023) seen
   through a lens?
