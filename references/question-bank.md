# Question Bank

Five dimensions, one question each. The stems below are starting points — the value comes
from anchoring every question in the **specifics of the session** (real names, real
decisions), not from the wording.

## Choosing what to quiz

Before writing questions, pick the session's load-bearing moments:

1. **The change** — the one diff that mattered most.
2. **The fork** — a decision that had a real alternative.
3. **The sacrifice** — something knowingly deferred, or a risk accepted.
4. **The trick** — the part that works for a non-obvious reason.
5. **The loose end** — what's unverified, unfinished, or fragile.

Each maps to a dimension below.

## The five dimensions

### `changed` — concrete outcome
Probes recall of what actually landed.

- "What changed in `<file>` and what does it do now that it didn't before?"
- "Name the two functions we touched and what each one does differently."
- "What's the one-line summary of the diff we just shipped?"

Avoid: "What did we do this session?" — too broad to grade.

### `why` — reasoning behind a decision
Probes whether they followed the *thinking*, not just the output.

- "Why did we put `<X>` in `<place A>` instead of `<place B>`?"
- "We chose `<approach>` over `<alternative>`. What tipped it?"
- "What was the reason for `<non-obvious choice>`?"

### `tradeoff` — judgment and risk
Probes whether they know what was given up.

- "What did we decide not to do, and what's the risk of leaving it?"
- "What could break in production from this change?"
- "What did `<approach>` cost us that `<alternative>` wouldn't have?"

### `mechanism` — how it works
Probes the part that isn't obvious from the surface.

- "Walk me through what happens when `<input/event>` hits this."
- "Why does `<thing>` work — what's it actually doing under the hood?"
- "What's the failure mode when `<edge case>` occurs?"

### `next` — ownership
Probes whether they own the work, not just watched it.

- "What's unfinished, and how would we know if it's wrong?"
- "What's the very next thing that needs doing, and why that first?"
- "If we shipped this today, what would you be nervous about?"

## Worked example — weak vs. strong

Session: agent added an in-memory LRU cache in front of a costly DB query, invalidated on
write, and left a TODO to bound memory.

| Dimension | Weak (gameable) | Strong (session-specific) |
|---|---|---|
| changed | "We added caching." | "We added an LRU in `getUserStats`, keyed by user id." |
| why | "For performance." | "Why LRU and not a plain dict — what was the concern?" |
| tradeoff | "Memory might grow." | "We didn't bound the cache size. What made that acceptable now?" |
| mechanism | "It caches the query." | "What happens to the cache when a user row is updated?" |
| next | "Check the cache later." | "The invalidation is per-write — what write path could we have missed?" |

The weak column can be answered from the question alone. The strong column can only be
answered by someone who was paying attention to *this* session.

## Keeping the five dimensions distinct

The dimensions overlap in two predictable places. Resolve them by construction, not by
grading:

- **`why` vs `mechanism`** collide when one decision is also the key mechanism — why Vite is
  fast *is* how Vite is fast. Put the *alternative* under `why` ("why not keep react-scripts?")
  and the *behavior* under `mechanism` ("what does esbuild actually do in dev?"), or pick a
  different mechanism entirely.
- **`tradeoff` vs `next`** collide when a deferral is both the thing given up and the thing
  left to do. Keep the deferral in `tradeoff` ("what did we give up / what's the risk?") and
  make `next` about verification — "how would we know if this is wrong?" — so the two can't be
  answered by the same sentence.

If two questions would accept the same answer, one is redundant. Replace it with a different
moment from the session.

## Self-check before you send

- Could someone who has never seen the session answer any of these from the wording alone?
  If yes, it's not testing comprehension — rewrite it.
- Can *you*, the agent, produce a precise model answer to each? If not, drop it.
- Are all five about a different moment? If two overlap, replace one.
- Fix the five questions *before* grading — an answer is graded against the question you chose,
  not one it happens to fit.
