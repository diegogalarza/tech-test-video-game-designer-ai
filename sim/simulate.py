#!/usr/bin/env python3
"""
Hollow Crown — reference combat simulator.

This is a TOOL, not the assessment. It models the duel resolution rules in
`data/combat-rules.md` and reports raw balance signal (win rates, time-to-kill,
cost efficiency) for the roster in `data/units.csv`.

You are free to run it as-is, extend it (add squad battles, encounters, new
metrics), or drive it from an AI workflow. No third-party dependencies — just:

    python3 sim/simulate.py
    python3 sim/simulate.py --units data/units.csv --trials 2000 --seed 7

The model is intentionally a 1v1 duel: it measures *raw stat power*, and
deliberately ignores positioning, movement, range and terrain. Treat that as a
known limitation, not a bug — part of good balance work is knowing what your
tool does and does not measure.
"""

"""
NEW SEGMENT: Squad-battle extension
Added a squad-battle extension re-using the same functions from the duel 
simulator, but sending multiple units per side instead of a 1v1 duel, 
with a simple alternating-turn

    python3 sim/simulate.py --squads
"""
import argparse
import csv
import random
from dataclasses import dataclass, replace


@dataclass
class Unit:
    id: str
    name: str
    cls: str
    attack_type: str  # "physical" -> atk vs def, "magic" -> mag vs res
    hp: int
    atk: int
    mag: int
    def_: int
    res: int
    spd: int
    skl: int
    lck: int
    cost: int


def load_units(path):
    units = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            units.append(Unit(
                id=row["id"], name=row["name"], cls=row["class"],
                attack_type=row["attack_type"],
                hp=int(row["hp"]), atk=int(row["atk"]), mag=int(row["mag"]),
                def_=int(row["def"]), res=int(row["res"]), spd=int(row["spd"]),
                skl=int(row["skl"]), lck=int(row["lck"]), cost=int(row["cost"]),
            ))
    return units


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def power(u):
    return u.mag if u.attack_type == "magic" else u.atk


def defense_vs(attacker, target):
    return target.res if attacker.attack_type == "magic" else target.def_


def hit_chance(attacker, target):
    return clamp(75 + attacker.skl * 2 - (target.spd * 2 + target.lck), 30, 100)


def crit_chance(attacker, target):
    return clamp(attacker.skl // 2 + attacker.lck - target.lck // 2, 0, 50)


def doubles(attacker, target):
    return (attacker.spd - target.spd) >= 5


def strike(attacker, target, hp, rng):
    """Resolve a single strike. Returns updated target hp."""
    if rng.uniform(0, 100) > hit_chance(attacker, target):
        return hp  # miss
    dmg = max(1, power(attacker) - defense_vs(attacker, target))
    if rng.uniform(0, 100) <= crit_chance(attacker, target):
        dmg *= 3
    return hp - dmg


def attack_turn(attacker, target, target_hp, rng):
    n = 2 if doubles(attacker, target) else 1
    for _ in range(n):
        if target_hp <= 0:
            break
        target_hp = strike(attacker, target, target_hp, rng)
    return target_hp


def duel(a, b, rng, max_rounds=100):
    """a strikes first. Returns id of winner, and number of rounds taken."""
    hp_a, hp_b = a.hp, b.hp
    for r in range(1, max_rounds + 1):
        hp_b = attack_turn(a, b, hp_b, rng)
        if hp_b <= 0:
            return a.id, r
        hp_a = attack_turn(b, a, hp_a, rng)
        if hp_a <= 0:
            return b.id, r
    # timeout -> whoever has more remaining HP fraction wins
    return (a.id if hp_a / a.hp >= hp_b / b.hp else b.id), max_rounds


def run(units, trials, seed):
    rng = random.Random(seed)
    wins = {u.id: 0 for u in units}
    fights = {u.id: 0 for u in units}
    rounds_sum = 0
    rounds_n = 0
    for i in range(len(units)):
        for j in range(i + 1, len(units)):
            a, b = units[i], units[j]
            for t in range(trials):
                first, second = (a, b) if t % 2 == 0 else (b, a)
                w, rounds = duel(first, second, rng)
                wins[w] += 1
                fights[a.id] += 1
                fights[b.id] += 1
                rounds_sum += rounds
                rounds_n += 1
    return wins, fights, rounds_sum / rounds_n


# ---------------------------------------------------------------------------
# Squad-battle extension (from squad_sim.py) — degeneracy hunting only.
#
# Not a replacement for combat-rules.md or the duel model above -- reuses the
# exact same strike/hit/crit/damage/doubling functions already defined above.
# Just orchestrates multiple units per side instead of a 1v1 duel, with a
# simple alternating-turn, focus-fire (lowest current HP%) targeting rule,
# since the duel model has no positioning and this is only meant to
# sanity-check the degeneracy question, not model real tactics.
# ---------------------------------------------------------------------------

@dataclass
class Combatant:
    unit: Unit
    hp: int


def act(attacker_c, side_targets, rng):
    living = [c for c in side_targets if c.hp > 0]
    if not living:
        return
    target_c = min(living, key=lambda c: c.hp / c.unit.hp)  # focus lowest hp%
    n = 2 if doubles(attacker_c.unit, target_c.unit) else 1
    for _ in range(n):
        if target_c.hp <= 0:
            break
        target_c.hp = strike(attacker_c.unit, target_c.unit, target_c.hp, rng)


def battle(squad_units, enemy_units, rng, max_rounds=60):
    squad = [Combatant(u, u.hp) for u in squad_units]
    enemies = [Combatant(u, u.hp) for u in enemy_units]
    first_squad = rng.random() < 0.5
    for r in range(max_rounds):
        order = [squad, enemies] if first_squad else [enemies, squad]
        for i, acting_side in enumerate(order):
            other_side = order[1 - i]
            for c in acting_side:
                if c.hp > 0:
                    act(c, other_side, rng)
            if all(c.hp <= 0 for c in other_side):
                return acting_side is squad
        if all(c.hp <= 0 for c in squad) or all(c.hp <= 0 for c in enemies):
            break
    return sum(c.hp for c in squad if c.hp > 0) > sum(c.hp for c in enemies if c.hp > 0)


def make_enemy(id_, name, cls, atype, hp, atk, mag, def_, res, spd, skl, lck):
    return Unit(id=id_, name=name, cls=cls, attack_type=atype, hp=hp, atk=atk, mag=mag,
                def_=def_, res=res, spd=spd, skl=skl, lck=lck, cost=0)


ENCOUNTERS = {
    "A - Sunken Gate": [make_enemy(f"wretch{i}", "Gate Wretch", "Brigand", "physical", 22,11,0,5,2,7,6,3) for i in range(3)]
                        + [make_enemy("acolyte", "Bog Acolyte", "Acolyte", "magic", 18,0,12,3,7,8,8,5)],
    "B - Hollow Throne": [make_enemy(f"guard{i}", "Throne Guard", "Knight", "physical", 30,15,0,12,5,6,8,4) for i in range(2)]
                          + [make_enemy("magus", "Crown Magus", "Battlemage", "magic", 22,0,17,4,9,7,10,6)],
    "C - Carrion Run": [make_enemy(f"shrike{i}", "Shrike Runner", "Skirmisher", "physical", 16,18,0,4,4,15,10,6) for i in range(3)],
}


def run_squad_vs_encounter(squad_units, enemy_units, trials=2000, seed=42):
    rng = random.Random(seed)
    wins = 0
    for _ in range(trials):
        w = battle(squad_units, [replace(e) for e in enemy_units], rng)
        wins += w
    return 100 * wins / trials


def run_squad_demo(units, trials=2000, seed=42):
    """Run the fixed set of degeneracy-check squads against all reference
    encounters, using whatever roster was loaded via --units."""
    roster = {u.id: u for u in units}

    SQUADS = {
        "4x Brennan (5+5+5+5=20)": [roster['brennan']]*4,
        "2x Sable + 1x Wisp (6+6+8=20)": [roster['sable']]*2 + [roster['wisp']],
        "2x Halden (9+9=18)": [roster['halden']]*2,
        "2x Rookwood (9+9=18)": [roster['rookwood']]*2,
        "Brennan+Sable+Halden (5+6+9=20)": [roster['brennan'], roster['sable'], roster['halden']],
        "3x Sable (6+6+6=18)": [roster['sable']]*3,
        "Brennan+Sable+Rookwood (5+6+9=20)": [roster['brennan'], roster['sable'], roster['rookwood']],
        "Wisp+Pyraxis+Brennan (8+8+5=21->trim: Wisp+Pyraxis=16+Brennan doesn't fit, use Wisp+Pyraxis only)": [roster['wisp'], roster['pyraxis']],
        "One of each cheap-to-mid (Brennan+Sable+Wisp=5+6+8=19)": [roster['brennan'], roster['sable'], roster['wisp']],
        "All six, one each (5+6+8+8+9+9=45, OVER BUDGET, illegal - included as upper-bound reference)": list(roster.values()),
    }

    for enc_name, enemies in ENCOUNTERS.items():
        print(f"\n=== Encounter {enc_name} (enemy total 'cost'-equivalent bodies: {len(enemies)}) ===")
        for squad_name, squad in SQUADS.items():
            cost = sum(u.cost for u in squad)
            wr = run_squad_vs_encounter(squad, enemies, trials=trials, seed=seed)
            flag = "  <-- OVER BUDGET (reference only)" if cost > 20 else ""
            print(f"  {squad_name:<70} cost={cost:<4} win%={wr:>6.1f}%{flag}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", default="data/units.csv")
    ap.add_argument("--trials", type=int, default=2000,
                    help="duels per unit pairing (split evenly on who strikes first)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--squads", action="store_true",
                     help="run the squad-battle degeneracy demo against the reference "
                          "encounters instead of the 1v1 duel balance report")
    args = ap.parse_args()

    units = load_units(args.units)

    if args.squads:
        run_squad_demo(units, trials=args.trials, seed=args.seed)
        return

    wins, fights, avg_rounds = run(units, args.trials, args.seed)

    rows = []
    for u in units:
        wr = 100 * wins[u.id] / fights[u.id]
        rows.append((u.name, u.cls, u.cost, wr, wr / u.cost))
    rows.sort(key=lambda r: r[3], reverse=True)

    print(f"\nHollow Crown — duel balance  (trials/pair={args.trials}, seed={args.seed})")
    print(f"Avg duel length: {avg_rounds:.1f} rounds\n")
    print(f"{'UNIT':<14}{'CLASS':<12}{'COST':>5}{'WIN%':>8}{'WIN%/COST':>11}")
    print("-" * 50)
    for name, cls, cost, wr, eff in rows:
        print(f"{name:<14}{cls:<12}{cost:>5}{wr:>7.1f}%{eff:>10.2f}")
    print("\nA balanced roster trends toward ~50% win rate and a flat WIN%/COST "
          "column.\nWide spreads in either are the imbalances to diagnose and fix.\n")


if __name__ == "__main__":
    main()