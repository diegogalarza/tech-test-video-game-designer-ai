# Hollow Crown — Balance Report

## DIAGNOSIS

Baseline roster (`data/units.csv`), measured with `sim/simulate.py`, default settings and confirmed stable across 11 seeds (`42, 1, 13, 27, 55, 88, 123, 256, 500, 777, 999`, `trials=2000` each — every unit's win% moved by under 1 point across all 11 runs):

| Unit | Class | Cost | Avg Win% | Avg Win%/Cost |
|---|---|---|---|---|
| Ser Halden | Knight | 6 | 78.6% | 13.10 (best) |
| Rookwood | Myrmidon | 7 | 65.2% | 9.31 |
| Wisp | Cleric | 4 | 51.5% | 12.87 |
| Brennan | Soldier | 5 | 46.6% | 9.32 |
| Sable | Archer | 5 | 34.9% | 6.98 |
| Pyraxis | Battlemage | 9 | 23.3% | 2.59 (worst) |

**Ser Halden is the auto-include:** Cheapest-but-one unit, best win rate, and best cost-efficiency by a wide margin. Root cause: `hp 32 / def 12` pushes most of the roster's `atk` values (`combat-rules.md`'s damage formula is `max(1, power - defense)`) down near the 1-damage floor — e.g. Brennan's 13 `atk` vs. his 12 `def` deals 1 damage per hit. He has exactly one hard counter: Wisp, whose `mag 12` vs. his `res 4` does real damage, and whose `spd 12` vs. his `spd 6` (diff 6, over the `>=5` doubling threshold) lets her double him. Matchup matrix: he wins only ~13-15% against Wisp specifically, ~78-99% against everyone else.

**Pyraxis is the trap pick:** Most expensive unit in the roster (9) and the worst performer (23.3%). Lowest HP (20) and lowest total stats (68, vs. 79-87 for the rest of the roster) despite the highest price tag. Low `spd` (5) means almost the whole roster doubles him.

**Rookwood has the best raw stats in the game and still loses to Halden 99% of the time:** Best `spd` (16) and `skl` (15) by a wide margin, doubles almost everyone, decent aggregate win rate (65.2%). But his `atk` (12) is too low to clear Halden's `def` (12) even doubled — a rules interaction (the damage floor), not a simple "he's weak" problem.

**Wisp's ~51% aggregate win rate hides a lopsided matchup spread:** That number is propped up almost entirely by her ~85% win rate against Halden specifically; against the rest of the roster she sits closer to 25-40%. A single dominant matchup can make an otherwise middling unit look "balanced" on paper.

**Sable underperforms relative to her cost:** Same cost as Brennan (5), but a much lower win rate (34.9% vs. 46.6%) — losing badly to both Rookwood (9.7%) and Brennan (20.7%).

**Brennan is the closest thing to already-balanced:** (46.6%, near the 50% target) — used as an informal reference point for what "correctly costed" looks like going in.

---

## CHANGES (baseline to final)

| Unit | Stat changes | Cost | Reasoning |
|---|---|---|---|
| Ser Halden | `def` 12→10 | 6→9 | Cost increase is the single most directly-supported change in the roster (best win% *and* best efficiency); the `def` trim lets more of the roster clear the damage floor, not just Wisp |
| Rookwood | `atk` 12→13, `skl` 15→13 | 7→9 | A larger `atk` buff (tested at +3) turned him into a worse auto-include than the original Halden (see Iteration 1 below) — settled on a minimal `atk` nudge plus trimming the accuracy/crit engine (`skl`) that was making every matchup unreliable-proof for his opponents |
| Brennan | `atk` 13→15, `def` 9→10, `res` 5→6 | 5 (unchanged) | Deliberately kept `res` well below `def` — stacking both high (tested in Iteration 5) recreated an auto-include with *no* exploitable weakness, which is a worse failure mode than the one we started fixing |
| Sable | `hp` 24→22, `spd` 11→14, `skl` 11→13 | 5→6 | Leaned into "fast, evasive, dies if caught" rather than just being a cheaper Brennan — `hp` wasn't contributing to her wins in the baseline, so cutting it doesn't touch her identity, just her punishability |
| Wisp | `hp` 24→30, `mag` 12→16, `def` 5→6, `res` 9→13, `spd` 12→8 | 4→8 | Rebuilt as the deliberate heavy magic-tank counterpart to Halden (the archetype originally proposed for Pyraxis); losing her speed advantage over Halden softened that matchup from an 85% blowout to a real ~60/40 fight rather than removing it |
| Pyraxis | `hp` 20→26, `def` 4→7, `res` 8→9, `skl` 9→12, `lck` 4→6 | 9→8 | First attempt fixed his durability only and left him still losing to Rookwood 68/32 — the sim showed the real bottleneck was accuracy (~52% hit chance vs. Rookwood's ~91%), not survivability; `skl`/`lck` closed that gap |

---

## BEFORE/AFTER (Selected iterations from the full 8 versions)

**Baseline:** 
Reference to Diagnosis table above: win% spread 23.3%-78.6% (55.3 points), win%/cost spread 2.59-13.10.

**Iteration 1: First attempt, a clean failure.** 
Raised Rookwood's `atk` 12→15 on the reasoning "best spd/skl in the game, just needs the damage to count." Result: **83.7% win rate**, beating every other unit in the roster 79% + head to head, this made him a WORSE aunto-include than the one we started with. The reasoning was directionally right but didn't account for how much his existing `crit` rate was already doing; adding raw damage on top turned every matchup into a blowout, not just the intended one against Halden.

**Iteration 5: Recreated the original problem from a different direction.** 
Trying to give Brennan a complete fix, raised both `def` (9→11) AND `res` (5→7) together. The result was: **71.8% win rate**, best win%/cost in the whole session (11.97), but a more dangerous failure than Halden's original 'broken' status, because this version had no exploitable elemental weakness at all (put a decent `def` and `res` simultaneously). Corrected in Iteration 6 by keeping `res` deliberately in the middle of the roster rather than matched to `def`.

**Final (Iteration 8):**

| Unit | Cost | Avg Win% | 95% CI | Avg Win%/Cost |
|---|---|---|---|---|
| Rookwood | 9 | 57.72% | [57.42%, 58.01%] | 6.41 |
| Ser Halden | 9 | 52.68% | [52.39%, 52.98%] | 5.85 |
| Wisp | 8 | 51.20% | [50.90%, 51.49%] | 6.40 |
| Pyraxis | 8 | 49.19% | [48.89%, 49.48%] | 6.15 |
| Sable | 6 | 46.12% | [45.83%, 46.42%] | 7.69 |
| Brennan | 5 | 43.09% | [42.80%, 43.39%] | 8.62 |

- Win% spread: 43.1%-57.7% (14.6 points, down from 55.3). 
- Win%/cost spread: 5.85-8.62, down from 2.59-13.10. 
- No unit is a clear auto-include or trap pick.

Two additional mechanical findings surfaced that were worth carrying forward as system-level notes rather than just stat fixes: the doubling rule (`spd` diff `>=5`) is a hard threshold, but not a gradient, a single point of `spd` crossing that line can swing a specific matchup by 60+ percentage points (found while tuning Brennan in Iteration 4); and damage-floor matchups (where `power` is only barely above `defense`) are disproportionately sensitive to small `atk`/`mag` changes, because in a 1-point stat change there can be a 30%+ change in actual per-hit output (found when tuning Rookwood in Iteration 7).

---

## CONFIDENCE

Before trusting this final roster, I ran it through two checks to make sure the numbers are real and not just noise.

First, I ran again the whole thing across the same 11 seeds we used from the start (2000 trials each) and looked at how much each unit's win rate bounced around. The biggest sway on any unit was under 0.6 points, so this isn't luck, the numbers hold steady no matter which random seed you throw at it.

Second, I pooled every duel across all 11 seeds together, that is 110,000 fights per unit, and checked how tight confidence interval was on each one's win rate. Every unit came back within about ±0.3 points, and none of the six overlap with each other. That means the ranking above isn't a coin flip that happened to land a certain way, it's a real repeatable difference between units.

One thing worth mentioning is that with a sample size this big, even tiny differences start looking "statistically significant" on paper — Wisp and Pyraxis both technically come back as almost-50%. That's just what happens with big numbers, not proof that either of them is actually unbalanced. What actually matters for balance purposes is the big picture: the whole roster's win rates now sit between 43.1% and 57.7%, not whether one unit's interval happens to brush up against the exact 50% line.

Even with n=110,000 tiny real differences register as "statistically significant" — Wisp's and Pyraxis's CIs both technically exclude exactly 50%. That's a property of large-sample statistics, not evidence either is meaningfully unbalanced. The number that actually matters for design purposes is the roster's overall spread (43.1%-57.7%), not if any single unit's interval happens to touch 50.00% exactly.

---

## DEGENERACY

Built a minimal squad-battle extension on top of `simulate.py` (same underlying strike/hit/crit/damage functions, just sending multiple units per side with simple alternating turns and lowest-HP%-first focus-fire targeting) and tested 9 budget-legal squads (20-point budget) against all three reference encounters, 2000 trials each.

- **Encounter A** ("the easy one" as its own design note): Nearly every squad clears it except the two lowest-body-count tank squads (2x Halden 77.2%, 2x Rookwood 87.3%), it is consistent with the encounter's stated intent, so not a red flag.
- **Encounter B**: Every all-physical squad tested got wiped (0.0%-1.4% win rate) against the armored Knights + magic Battlemage mix. Only squads including Wisp did reasonably good (34-58%). No budget-legal squad came close to a trivial win, the best was 58% (Brennan + Sable + Wisp). This roster actively punishes ignoring the physical/magic split.
- **Encounter C**: The one real finding worth naming plainly, where I mass-spam 4x Brennan (the cheapest unit) scored 73.2%, clearly the best of anything tested. Not a guaranteed win and not an exploit exactly (more units genuinely dissipates a doubling-heavy enemy's threat, since each Shrike Runner can only double one target per round), but it is a measurable "mass beats speed" incentive that budget mlimited by cost doesn't fully police. Flagged as an open design question: is that an acceptable tactic?, or does it argue for a slot cap alongside the cost budget?

An illegal overpowered 45-cost "one of everything" squad wins ~100% everywhere, confirming the budget is really constraining work in encounters B and C.

---

## LIMITATIONS

Everything above comes from a 1v1 duel model. It deliberately doesn't see:

- **Positioning, movement (`mov`), range (`range`), or terrain** — the CSV carries these columns but the duel sim ignores them entirely. A unit that's weak in a straight duel (e.g. a low-range poke unit) could be much stronger in real play if it can avoid being engaged at all.
- **Healing-as-support** — there is no heal action anywhere in `combat-rules.md` or `simulate.py`. Wisp's "Cleric" class is flavor-only under the current rules; if healing were added as an actual mechanic, her value (and the whole roster's math around her) would need to be re-evaluated from scratch.
- **Squad-level tactics beyond focus-fire** — the degeneracy check's squad extension uses a simple lowest-HP% targeting rule. Real players would make smarter targeting and positioning decisions that could change which squads are actually strong, in either direction.
- **Turn order isn't speed-driven** — a real limitation of the given rules, not something we changed: `spd` only controls whether a unit doubles within its own turn, not who acts first each round (that's fixed as "initiator, then defender, alternating"). This is a simplification relative to how speed typically works in Fire Emblem-likes, and is worth validating against actual player expectations before shipping.

To validate what the duel model can't see, the next step would be a lightweight positional prototype (even a paper/spreadsheet mockup of a few tiles) run through actual playtests, specifically checking whether `mov`/`range` differences meaningfully change any of the conclusions here — particularly for Sable (a ranged unit whose duel performance may understate her real value) and Wisp/Pyraxis (both `range 2`, which the duel model can't credit at all).
