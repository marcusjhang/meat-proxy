# meat-proxy

An end-of-session interrogation for people who use coding agents.

Your agent did the work. Did *you*? `meat-proxy` is a skill that, at the end of a
session, quizzes you on what actually happened — then scores how much of a **meat proxy**
you were: a warm body that approved output it can't describe.

```
## Meat Proxy: 60/100 — Passenger

You were along for the ride. You know roughly where you went, not how.

| # | Dimension | Score | What an operator would have said |
|---|-----------|-------|----------------------------------|
| 1 | changed   | 1/2   | Optimistic UI in `CommentBox`, reconciled on the server id. |
| 2 | why       | 0/2   | Rate-limiting moved to middleware so every route gets it, not just comments. |
| 3 | tradeoff  | 2/2   | — |
| 4 | mechanism | 0/2   | The optimistic entry is keyed by a temp id and swapped on response. |
| 5 | next      | 1/2   | Retry is deferred, so a dropped comment is lost silently today. |

The `why` is the one you'd need in review: you signed off on moving a
security-adjacent control with no reason attached.
```

## How it works

1. The agent re-reads the session and picks its **five load-bearing moments**.
2. It asks **five questions, one at a time, free recall** — no hints, no multiple choice,
   no reveal until the end. Multiple choice lets a proxy guess.
3. Each answer is graded **0 / 1 / 2** — absent / hollow / precise.
4. `scripts/score.py` turns the grades into a **0–100 meat-proxy index**, deterministically.
5. You get a verdict card with every answer you *should* have given, and a rolling trend.

**The score is inverted on purpose: 0 = you drove it, 100 = you were a proxy. Lower is better.**

| Index | Tier | Meaning |
|---|---|---|
| 0–20 | **Driver** | Understands the session cold. |
| 21–40 | **Navigator** | Would catch a wrong turn before it shipped. |
| 41–60 | **Passenger** | Knows roughly where it went, not how. |
| 61–80 | **Ballast** | The session happened around you. |
| 81–100 | **Pure Meat Proxy** | A warm body with push access. |

## Install

```bash
git clone https://github.com/marcusjhang/meat-proxy.git
cd meat-proxy
./install.sh              # symlinks into ~/.agents/skills/meat-proxy
./install.sh --claude     # also symlink into ~/.claude/skills/meat-proxy
```

Manual install is the same thing by hand:

```bash
ln -sfn "$(pwd)" ~/.agents/skills/meat-proxy
```

Restart your agent so it picks up the new skill.

## Use

Any of these should trigger it:

```
/meat-proxy
meat proxy me
quiz me on what just happened
did I actually understand this session?
```

For best results, run it **at the end of a session while the context is still live** —
the agent quizzes on the real specifics (files, decisions, tradeoffs) only if it can
still see them.

### Retro and batch runs

The skill has a non-interactive mode. Hand it a session summary plus a set of answers and
it emits the questions, grades, and full verdict in one pass — useful for testing, or for
grading a transcript after the fact.

### Scores over time

Every run is appended to `~/.meat-proxy/history.jsonl`:

```bash
python3 scripts/history.py trend
# 12 sessions · avg 47.3 · best 10 · worst 90 · last 5 avg 38.0 (improving)
```

## Auto-running at session end

Skills don't trigger themselves. The honest options are:

- **Habit** — type `/meat-proxy` when you wrap up.
- **A reminder hook.** A Stop hook can *nudge* you at the end of a turn. It runs
  non-interactively, so it can't give you a live quiz, but it can prompt you to start one.
  Example for Claude Code (`~/.claude/settings.json`):

  ```json
  {
    "hooks": {
      "Stop": [
        {
          "hooks": [
            { "type": "command", "command": "echo 'Session ending. Consider: /meat-proxy'" }
          ]
        }
      ]
    }
  }
  ```

Don't wire this in silently — a quiz that interrupts every session is a surprise, not a
feature. Turn it on when you want it.

## Layout

```
meat-proxy/
├── SKILL.md                     # the skill: workflow, rules, verdict format
├── references/
│   ├── scoring.md               # rubric, index math, tiers, worked example
│   └── question-bank.md         # question stems per dimension
├── scripts/
│   ├── score.py                 # grades -> index + tier (--selftest)
│   └── history.py               # append results, print trend
├── evals/evals.json             # test cases for non-interactive mode
└── install.sh
```

## License

MIT © Marcus Jhang
