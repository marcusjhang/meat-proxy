---
name: meat-proxy
description: End-of-session interrogation that quizzes the human on what actually happened and scores how much of a meat proxy they were. Use at the end of any session where an agent did real work, and whenever the user says "meat proxy", "quiz me", "test me on this session", "did I understand this", "am I a meat proxy", "grade my understanding", or invokes /meat-proxy. Run it even when the user only hints they want a check on whether they followed what happened, and proactively offer it when a long agent-driven session is wrapping up.
license: MIT
metadata:
  version: 1.0.0
  category: productivity
---

# Meat Proxy

An agent that does the work alone turns its human into a **meat proxy**: a warm body
that approves output it cannot describe. The work ships; the understanding does not.

This skill runs at the end of a session and fixes that in the cheapest possible way.
The agent that just did the work — the only party that knows exactly what the human
*should* understand — turns around and interrogates them about it, then scores how
much of a proxy they were.

**The score is inverted on purpose.** 0 means you drove the session and could explain
it cold. 100 means you rubber-stamped things you cannot describe. Lower is better.

The quiz is not a formality. A soft quiz is a second rubber stamp. Your job is to
find out what the human actually absorbed, not to make them feel good about it.

## The one rule

**Do not reveal, hint, confirm, or correct anything until the verdict.**

No "close!", no "right direction", no "think about the diff", no letting them peek at
the answer and revise. Ask, wait for the reply, ask the next. If you signal correctness
mid-quiz you have handed the proxy a cheat sheet and the whole exercise is theater.

If the human tries to fish for the answer, decline and move on: "No hints until the
end. Next question."

## Workflow

### 1. Reflect on the session (before you write a single question)

Re-read what actually happened. You are looking for the load-bearing specifics you can
quiz against — not a vibe summary:

- The concrete change and where it landed (files, functions, endpoints, commands)
- The one or two decisions that had alternatives, and why this one won
- What was rejected or deferred, and the risk knowingly accepted
- The non-obvious mechanism: the part that works for a reason that isn't obvious
- What is unfinished, unverified, or one bad input away from breaking

If you cannot state the answer to a question you're about to ask, it's a bad question.
Delete it.

### 2. Write 5 questions, one per dimension

Use exactly these five dimensions, one question each. They are chosen so that a proxy
cannot survive on vibes: recall, reasoning, judgment, mechanism, and ownership.

| Dimension | What it probes | The question should make them... |
|---|---|---|
| `changed` | Concrete outcome | name what actually changed and where |
| `why` | Reasoning | explain why a specific choice beat its alternative |
| `tradeoff` | Judgment | name what was given up or what could now break |
| `mechanism` | Understanding | explain how a key piece works |
| `next` | Ownership | say what's unfinished and what would break it |

Rules for the questions:

- **Open-ended free recall only.** Never yes/no, never multiple choice — a proxy guesses
  multiple choice right at chance and learns nothing. Force them to produce the thing.
- **Specific to this session.** Name the real file, command, decision, or edge case.
  "What did we do today?" is not a question; "why did the retry live in the worker and
  not the client?" is.
- **Askable by someone who didn't do the work but did watch it.** Don't quiz on anything
  that was never surfaced in the session — that's trivia, not comprehension.
- **One at a time, in this order.** Send one question, stop, wait for the answer. Do not
  dump all five. Do not preview what's coming.
- Keep them short. The value is in the answer, not the prompt.

Read `references/question-bank.md` for stems and worked examples, and
`references/scoring.md` for the rubric in detail.

### 3. Interrogate

Ask question 1. Wait. Ask question 2. Wait. And so on.

Grade as you go, in your head, but stay silent about it. Accept "I don't know" gracefully
— it's a 0, and honesty is worth more than a bluff. If an answer is a bluff, don't call
it out yet; note it and let the verdict land.

### 4. Grade

Score each answer 0, 1, or 2:

- **0** — no idea, wrong, or a confident non-answer. "It was refactoring something."
- **1** — partial, directionally right but hollow, or a bluff that happened to be near the
  truth. A vague answer that names the right *area* but nothing specific lands here.
- **2** — precise and correct: the right name, the right reason, the right edge case.

Grade the understanding, not the effort. A polite "good answer" you can't quite pin down
is a 1. When torn between two scores, take the lower one — the cost of flattering a proxy
is that they stay one.

### 5. Compute the score with the script — don't do the math yourself

    python3 scripts/score.py 2 1 0 2 1

Pass the five grades in dimension order (`changed why tradeoff mechanism next`). The
script returns the 0–100 meat-proxy index and the tier, deterministically, so two runs
of the same answers never disagree. Use `--labels` to rename dimensions and `--json`
for machine output.

### 6. Deliver the verdict

ALWAYS use this exact structure. Fill it, don't invent a new one:

```
## Meat Proxy: <index>/100 — <Tier>

<one line, in the tier's voice, on what the score means for them>

| # | Dimension | Score | What an operator would have said |
|---|-----------|-------|----------------------------------|
| 1 | changed | 0/2 | <the precise answer they didn't give> |
| 2 | why | 1/2 | <...> |
| ... |

<For every question scored below 2, one blunt sentence on what that gap costs them.>

**Trend:** <from scripts/history.py, or "first recorded session">
```

The third column is the payoff — the actual answer, in full, so the session teaches them
something on the way out. Never leave it as "see above" or a restatement of the question.
For a 2/2, write "—" and move on.

### 7. Log it

    python3 scripts/history.py append --index <index> --tier "<Tier>" --session "<short label>"

Then show the trend with `python3 scripts/history.py trend`. History lives at
`~/.meat-proxy/history.jsonl`. The point of the log is the direction of travel: a single
score is a mood, a trend is a habit. Call out when they're improving or slipping.

## Non-interactive mode

Sometimes you can't ask — an eval, a batch run, or a retro on a saved transcript. When
asked to run non-interactively, or when handed a session summary plus a set of answers:

1. Build the same five questions from the summary.
2. Grade the supplied answers against the summary, same rubric, same honesty.
3. Emit the question list, the grades, and the full verdict in one pass.

Never invent answers on the human's behalf. If an answer is missing, it's a 0.

## Wiring it to run by itself

Skills don't self-trigger, so the quiz runs when the user or a hook calls it. For
auto-run at session end, see the hook snippets in `README.md`. Do not install a hook
without asking — silently interrupting every session is a surprise, not a feature.

## Reference files

- `references/scoring.md` — the rubric, the index math, and the tier table in full
- `references/question-bank.md` — question stems per dimension and worked examples
- `scripts/score.py` — deterministic grades → index + tier (`--selftest` to verify)
- `scripts/history.py` — append results and print the trend
