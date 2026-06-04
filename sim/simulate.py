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
import argparse
import csv
import random
from dataclasses import dataclass


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", default="data/units.csv")
    ap.add_argument("--trials", type=int, default=2000,
                    help="duels per unit pairing (split evenly on who strikes first)")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    units = load_units(args.units)
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
