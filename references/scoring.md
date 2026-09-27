# Scoring

## The meat-proxy index

The index answers one question: **how much of this session happened without you?**

- `earned` = sum of the five grades, each 0/1/2, so 0–10
- `possible` = 10
- `index = round(100 * (1 - earned / possible))`

So a perfect sheet scores **0** (you drove it) and a blank sheet scores **100** (you were
a proxy). The inversion is deliberate: the number reads as "how much of a proxy were
you," and lower is better.

Because the scale is 0–10 over five questions, each step of 1 is worth 10 index points.

## Grade rubric

The rubric has one hinge: **is the answer correct, and does it carry a specific fact from
this session?**

| Score | Meaning | Looks like |
|---|---|---|
| **2** | Correct and specific | Names the actual thing — the file, the function, the reason, the edge case. You could act on it. |
| **1** | Correct but hollow | Names the right area — right file, right feature, right idea — with no specifics, and nothing in it is wrong. |
| **0** | Wrong or absent | "I don't know." A confidently wrong answer. A fluent non-answer that commits to nothing. |

**The 0/1 boundary, spelled out** (this is the one graders fumble):

- "We added some webhook stuff" when we added Stripe webhooks → **1** (correct area, no detail).
- "We refactored the API layer" when we actually moved a CSS file → **0** (wrong area).
- "It seemed better" / "because performance" when the real reason was route coverage → **0**
  (a reason-shaped non-answer, and wrong).
- "I don't know" → **0**.

The rule of thumb: **if the answer contains no correct, session-specific fact, it is a 0.**

Other judgment calls, resolved in advance so two graders agree:

- **Right keyword, wrong reason → 0**, not 1. Knowing *that* we used a queue is not knowing
  *why*, and a wrong reason is wrong.
- **Correct but only after the question is reread → same score.** The quiz measures what they
  have, not how fast they produce it.
- **Confident and wrong → 0, and say so in the debrief.** A proxy who believes they understood
  is more dangerous than one who knows they didn't.
- **"I don't know" → 0, never punished in tone.** Honest zeros are what make the score real.
- **Any tie → the lower score.** 0 over 1, 1 over 2. When in doubt, don't flatter.

## Rounding

`index = round_half_up(100 * (1 - earned / possible))` — the script uses `floor(x + 0.5)`,
so an exact `.5` rounds up. With the standard five questions the result is always a multiple
of 10, so this only matters for custom question counts.

## Tiers

| Index | Tier | What it means |
|---|---|---|
| 0–20 | **Driver** | Understands the session cold; could explain it tomorrow. |
| 21–40 | **Navigator** | Solid grip; would catch a wrong turn before it shipped. |
| 41–60 | **Passenger** | Along for the ride. Knows roughly where it went, not how. |
| 61–80 | **Ballast** | The session happened around them; would have to read the diff. |
| 81–100 | **Pure Meat Proxy** | Approved things they cannot describe. A warm body with push access. |

## Worked example

Session: agent added optimistic UI to a comment box, moved rate-limiting into a middleware,
and deferred retry logic to a follow-up.

| Dimension | Answer given | Grade | Why |
|---|---|---|---|
| changed | "we made the comments feel snappier" | 1 | Right area, no mechanism, no name. |
| why | "because latency" | 0 | No specific reason; could apply to anything. |
| tradeoff | "we didn't do the retry thing yet" | 2 | Correctly names the deferral. |
| mechanism | "I don't know" | 0 | Honest zero. |
| next | "finish the retry follow-up" | 1 | Names the item but not the risk of its absence. |

`earned = 1+0+2+0+1 = 4` → `index = round(100*(1 - 4/10)) = 60` → **Passenger**.

The debrief would say: *the `why` on rate-limiting is the one you'd need in the next review —
you signed off on moving a security-adjacent control with no reason attached.*

## Anti-gaming notes

- Never let the human revise an answer before it's graded.
- Never accept a question phrased back at you as an answer.
- If the human asks what the right answer was mid-quiz, that ends the quiz for that question;
  it's a 0, not a hint.
- Don't inflate to be nice. The index is only useful if it's allowed to hurt a little.
