# Hollow Crown — Combat Rules (v0.3, "needs balancing")

> These are the live resolution rules for the tactical combat in **Hollow Crown**
> (Twin Hearth Studios' dark-fantasy tactical RPG). The reference simulator in
> `/sim/simulate.py` implements exactly these formulas. If you change a rule,
> change both — or document the divergence.

## Unit stats

Each unit (see `data/units.csv`) has:

| Stat | Meaning |
|---|---|
| `hp` | Health. At 0, the unit is defeated. |
| `atk` | Physical power. |
| `mag` | Magical power. |
| `def` | Physical defense. |
| `res` | Magical defense (resistance). |
| `spd` | Speed — drives follow-up attacks and evasion. |
| `skl` | Skill — drives accuracy and crit. |
| `lck` | Luck — improves crit, reduces incoming crit, aids evasion. |
| `mov` | Tiles moved per turn. *(positioning stat — not used by the duel sim)* |
| `range` | Attack range in tiles. *(positioning stat — not used by the duel sim)* |
| `cost` | Deployment cost. You field a squad under a fixed cost budget. |
| `attack_type` | `physical` (uses `atk` vs target `def`) or `magic` (uses `mag` vs target `res`). |

## Resolution (single strike)

1. **Accuracy.** `hit% = clamp(75 + attacker.skl*2 − (target.spd*2 + target.lck), 30, 100)`
   Roll. On a miss, no damage.
2. **Damage.** `dmg = max(1, attacker.power − target.defense)`
   where `power`/`defense` are `atk`/`def` for physical attackers, `mag`/`res` for magic.
3. **Critical.** `crit% = clamp(attacker.skl//2 + attacker.lck − target.lck//2, 0, 50)`
   On a crit, `dmg ×= 3`.

## Follow-up (doubling)

If `attacker.spd − defender.spd ≥ 5`, the attacker performs **two** strikes in its
attack turn instead of one.

## Duel flow (what the reference sim measures)

- Two units alternate **attack turns**; the initiator strikes first.
- After the initiator's turn, the defender **counterattacks** (same rules), then
  they keep alternating until one unit reaches 0 HP.
- To remove first-mover bias, every pairing is run with each side initiating half
  the trials.
- Hard cap of 100 rounds; on timeout the unit with the higher remaining HP
  fraction is scored the winner (this should almost never trigger).

## Known limitations of the duel model

The duel is a **raw-stat-power** lens. It deliberately ignores `mov`, `range`,
terrain, positioning, healing-as-support, and squad composition. A unit can be
weak in a 1v1 duel and valuable in real play (e.g. a healer or a ranged poke
unit), or vice-versa. Knowing what your measurement *can't* see is part of the
job.

## Deployment & economy

In a real battle you field a squad under a **cost budget** (e.g. 20 points). Each
unit's `cost` is meant to price its battlefield value, so that no single unit is
an auto-include and no unit is a trap pick. Right now those costs were set by
gut, not data.
