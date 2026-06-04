# Video Game Designer (AI) — Technical Assessment

**Time limit:** 2–3 hours max.

---

## Challenge

You've joined **Twin Hearth Studios** as a systems designer on **Hollow Crown**,
a dark-fantasy tactical RPG (think Fire Emblem / Triangle Strategy). The combat
prototype works, but the **roster is unbalanced and the costs were set by gut**.
Right now one unit is an auto-include, another is a trap pick, and the deployment
costs don't reflect real battlefield value.

Your job is to **turn that into a balanced, defensible system** — and to do it the
way an AI-first designer would: measure, diagnose, iterate, and document.

You are given the live system in `/data/`:

- `units.csv` — the starting roster (6 units) with full stats and deployment costs. **It is intentionally unbalanced.**
- `combat-rules.md` — the exact combat resolution rules.
- `encounters.md` — two reference encounters for sanity-checking your changes in context.

And a tool in `/sim/`:

- `simulate.py` — a **reference combat simulator** (pure Python, no dependencies) that runs the duel rules and reports win rates and cost efficiency. **This is given to you so you don't have to build a combat engine.** Run it, extend it, or drive it from an AI workflow — your call.

```bash
python3 sim/simulate.py                 # baseline, see the imbalance
python3 sim/simulate.py --trials 5000 --seed 7
```

> This is a **design** assessment, not an engineering one. You will *not* be graded
> on building a simulator. You'll be graded on your balancing judgment, your method,
> and how you use AI to get there.

---

## What to deliver

Put everything in `/output/`.

### 1. `GDD.md` — design one core system
Take **one** of the system's core loops and write a short, living design doc for it.
Pick exactly one and own it end-to-end:
- the **deployment economy** (how `cost` should map to value, the budget, what makes a pick a real trade-off), **or**
- a **progression / difficulty curve** for how this roster scales across a campaign, **or**
- a **counter/triangle system** (e.g. a rock-paper-scissors layer over the classes) that makes weak units situationally strong.

Keep the GDD scoped to the *same* combat system you're balancing — not a bolted-on new feature. Include: the design intent, the rules, the key numbers, and the player-experience goal.

### 2. `units.balanced.csv` — the rebalanced roster
Your fixed stats and/or costs. Same columns as the input. No unit should be an
auto-include or a trap pick.

### 3. `BALANCE_REPORT.md` — the evidence
This is the heart of the assessment:
- **Diagnosis:** which units are broken and *why*, with numbers from the simulator (not vibes).
- **Changes:** what you changed and the reasoning per change.
- **Before/after:** simulator output showing the roster moved toward your target (e.g. tighter win-rate spread, flatter cost-efficiency). Show **at least two iterations** — your first fix will not be your last.
- **Limitations:** what the duel model can't see (positioning, range, healing-as-support) and how you'd validate those.

### 4. `DESIGN_AI_WORKFLOW.md` — mandatory
How you used AI as a design partner (see below).

---

## Mandatory: `DESIGN_AI_WORKFLOW.md`

Document how you used AI to do the design work — not just to write prose:

1. Which AI tool(s) and why.
2. 3–5 concrete prompts you used and what they produced (diagnosis, stat proposals, sim extensions, edge-case hunting, GDD drafting).
3. One moment where the AI was wrong or misleading and how you caught it. *(A model will happily propose "balanced" numbers that fail in the sim — show that you verify against evidence, not the model's confidence.)*
4. How you'd scale this: balancing **50+ units across multiple games per quarter** with an AI-assisted pipeline.

---

## Tooling

Use whatever you want, and combine freely:

- **Design partner:** Claude Code, Cursor, ChatGPT, etc. — for diagnosis, proposals, GDD drafting, edge cases.
- **The sim:** run `simulate.py` as-is, or extend it (squad battles, the encounters, new metrics like time-to-kill or matchup matrices). Spreadsheets / notebooks are fine too.
- **Docs:** Markdown is perfect. Charts/tables welcome but not required.

You may change the combat *rules* if you justify it — but if you do, keep the sim and `combat-rules.md` in sync.

## Out of scope

Building a production combat engine, art/animation, netcode, a full campaign, or a
shipping UI. We want the **system and the reasoning**, not a finished game.

---

## Evaluation

We grade **methodology over a single "correct" roster** — there is no one true set of
numbers. A well-measured, well-argued, iterated balance beats a lucky guess.

| Area | Weight |
|---|---|
| Balance method — measure → diagnose → iterate → verify against the sim | 30% |
| Systems design — the `GDD.md`: coherent intent, numbers, player experience | 25% |
| Use of AI as a design partner (`DESIGN_AI_WORKFLOW.md`) | 20% |
| Design judgment — sane trade-offs, caught the subtle issues, knows the model's limits | 15% |
| Clarity of documentation | 10% |

---

## How to submit

1. **Fork** this repo.
2. Create branch `submission/<your-name>`.
3. Commit your deliverables in `/output/`.
4. Open a **Pull Request** to `main` of this repo.
5. In the PR include: time spent, how you used AI, and trade-offs made.
