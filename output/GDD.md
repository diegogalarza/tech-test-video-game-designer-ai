# Hollow Crown - GDD: THE DEPLOYMENT ECONOMY

## DESIGN INTENT

One, if not the most interesting decision a player can make before a battle/match starts is "Which units do I bring?". But that only works if '*cost*' actually prices battelfield value, and if no single answer is the corect for every encounter.

The deployment economy's job is to turn a fixed 'cost' budget into a real trade-off system: Every point the player spends on a unit, is a point they cannot spend somewhere else, and different encounters should reward different spending patterns.

Two failure states we're explicitly designing against:
1. **The auto-include** - a unit so efficient relative to its cost that leaving it home is a mistake in every matchup.
2. **The trap pick** - a unit priced above its actual value, chosen only by mistake or misunderstanding.

There was a subtle third failure state that was discovered was the **the unexplotable unit**, basically a unit strong that **also** has no weakness. A unit with a real weak side is mopre interesting to deploy against than one that's simply *good* because it rewards the player for noticing and punishing it.

---

## THE RULES

**Budget:** Player has 20 points available as a fixed cost budget for the current 3 reference encounters. Costs are derived from a measured battlefield performance (1v1 duel win rate) and validated against multi-unit reference encounters.

**Cost must track win rate:** Two different units but with similar total stats budget can have differente cost if their stats interact differently with the roster and the combar formulas, therefore *cost* reflects a measured value, not total from a spreadsheet.

**Every unit should have  an exploitable weak side:** No unit should be strong against everything without something that punishes it. 

In the current roster: A physical unit (built around *def*) should not be also built around *res*; therefore stacking both removes that unit's counterplay, which is far more dangerous than a unity simply being strong, it removes the "use magic against armor" strat for the player.

**Specialists price differently than generalists:** Units excellent against one archetype but awful elsewhere shouldn't be priced as if that kind of performance is the avergae value, it should be priced closer to it's typical value across encounters like that, with a counter matchup treated as bonus upside and not baseline. Pricing a specialist should be at its average bringin it to a tactical bet instead of princing it at its peak where its a trap outside that matchup.

---

## KEY NUMBERS (Current roster)

| Unit | Cost | Measured win% | Role in the economy |
|---|---|---|---|
| Ser Halden | 9 | 52.7% | Physical wall, premium price, exploitable magic weakness |
| Rookwood | 9 | 57.7% | Speed/accuracy specialist, premium price |
| Wisp | 8 | 51.2% | Heavy magic-tank, deliberate hard counter to Halden, exploitable physical weakness |
| Pyraxis | 8 | 49.2% | Durable magic striker, deliberate counter to Rookwood via accuracy, not raw power |
| Sable | 6 | 46.1% | Fast, fragile, cheap — punishable if caught, hard to catch |
| Brennan | 5 | 43.1% | Budget generalist, no specialization, cheapest full-price option |

Budget: 20 points. Target tolerance band: roughly 43-58% duel win rate per unit is treated as "inside acceptable spread" for this pass — tight enough that no unit reads as broken, loose enough to preserve distinct identities rather than flattening everyone to a robotic 50.0%.

---

## Player-Experience Goal

A player looking at their roster should *feel* it like a bet and not filling a checklist.

- If they bring Halden, should mean they commit toa budget wall that magic-heavy enemies can punish.
- If the bring Wisp, should mean that they are specifically giving answer to that wall, and being weaker somewhere else.
- Bringing 4 Brennans instead of 2 'premium' units means trading an individual unit's power for numbers. This was  a legitimate trade-off I've found in the degeneracy testing where more cheap units is legitimate, but not always optimal, against faster enemy squads.
- No player should feel obliged to 'bring' a certain unit into battle regardless the mission, but also, they should not feel that a unit they brought was a waste of budget. The economy succeeds when the player has that post-battle question of "Did I analised the encounter right?" and *NOT* the question of "Did I pick the correct unit as everyone else always said to pick?"