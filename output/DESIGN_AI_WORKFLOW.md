# Hollow Crown - DESIGN AI WORKFLOW

## AI TOOL USED

Claude, specifically the Sonnet 5 model, used conversationally, with direct shell and file access to this repo, making it able to run `sim/simulate.py` itself, extend it, and read back real output rather than reasoning about it in the abstract. The reason this mattered specifically for a balance pass: every proposal could be tested immediately in the same conversation, rather than "here's what I think the numbers should be" followed by a separate manual verification step later. That loop (propose, run, read the real output, react) is what made it possible to catch bad proposals before they went into the final CSV instead of after.

---

## CONCRETE PROMPTS & RESULTS

### Prompt #1 ###

*Run the simulate.py with the default trials=2000, seed=42 and try at least 10 more random seeds, so we can see the win rates between units.*

*Make a table with every unit-per-seed with each win%*

*Give me a detailed table with win%, win%/cost, averages, and include a column for crit% to see how the multiplayer works if they hit a critical hit, plus a deviation*

### Results: ###

Produced the baseline stability check: every unit's win% moved by under 1 percentage point across 11 seeds, plus an empirical crit-rate column (not the theoretical formula value — the actual measured rate). This became the template for confidence-checking every later iteration, and revealed that Rookwood lands crits ~3x the roster average (~11%) without that being enough to win his worst matchup — an early signal that "damage output" and "win rate" don't move together in simple ways in this system.

11 runs total: the default (trials=2000, seed=42) plus 10 more seeds (1, 13, 27, 55, 88, 123, 256, 500, 777, 999), same trials=2000 each. That's 22,000 trials per unit pairing in total across all seeds combined. CRIT% is empirical — the actual measured rate of that unit's own attacks landing as critical hits (not the theoretical crit_chance() formula value, the real observed frequency across every strike it threw as attacker).

**Per-seed win% (raw)**

| Seed         | Ser Halden | Rookwood | Brennan | Sable | Wisp  | Pyraxis |
|--------------|-----------:|---------:|--------:|------:|------:|--------:|
| 42 (default) | 78.5%      | 65.7%    | 46.8%   | 34.6% | 50.6% | 23.8%   |
| 1            | 78.4%      | 65.1%    | 46.4%   | 35.7% | 51.2% | 23.1%   |
| 13           | 78.7%      | 65.1%    | 46.9%   | 35.0% | 51.4% | 22.9%   |
| 27           | 79.0%      | 65.5%    | 46.8%   | 35.0% | 51.3% | 22.4%   |
| 55           | 78.8%      | 64.9%    | 46.5%   | 34.6% | 52.2% | 23.1%   |
| 88           | 78.6%      | 64.8%    | 46.4%   | 34.5% | 52.1% | 23.6%   |
| 123          | 79.0%      | 65.4%    | 46.9%   | 34.5% | 50.9% | 23.2%   |
| 256          | 78.8%      | 65.5%    | 46.2%   | 35.1% | 51.1% | 23.3%   |
| 500          | 78.2%      | 64.9%    | 46.2%   | 34.8% | 51.8% | 24.1%   |
| 777          | 78.2%      | 65.4%    | 45.9%   | 35.2% | 51.9% | 23.4%   |
| 999          | 78.4%      | 64.4%    | 47.7%   | 34.7% | 51.6% | 23.2%   |

**Aggregate table (sorted by avg win%)**

| Unit       | Class      | Cost | Avg Win% | Std Dev | Min   | Max   | Avg Win%/Cost | Avg Crit% |
|------------|------------|-----:|---------:|--------:|------:|------:|--------------:|----------:|
| Ser Halden | Knight     | 6    | 78.6%    | 0.27%   | 78.2% | 79.0% | 13.10         | 3.6%      |
| Rookwood   | Myrmidon   | 7    | 65.2%    | 0.41%   | 64.4% | 65.7% | 9.31          | 11.0%     |
| Wisp       | Cleric     | 4    | 51.5%    | 0.49%   | 50.6% | 52.2% | 12.87         | 6.3%      |
| Brennan    | Soldier    | 5    | 46.6%    | 0.49%   | 45.9% | 47.7% | 9.32          | 4.7%      |
| Sable      | Archer     | 5    | 34.9%    | 0.35%   | 34.5% | 35.7% | 6.98          | 6.8%      |
| Pyraxis    | Battlemage | 9    | 23.3%    | 0.44%   | 22.4% | 24.1% | 2.59          | 3.2%      |



### Prompt #2 ###

*Okay, before I throw my own list of stat tweaks at you, I want to test something different: I want you to look at the current units.csv file, the sim output from our previous analysis and the win% table we just built, and come up with your OWN rebalance proposal from scratch. Don't wait for me to tell you "buff this stat" or anything, analise through which units are underperforming relative to their cost (Sable and Pyraxis look weak, but Rookwood and Halden look strong) and propose specific stat or cost changes you think would make everything closer.*

*Pick whichever unit you think needs it most first, don't ask me to confirm before running it, just make the change directly in the CSV, run the simulate.py the same way we did for the baseline (same trials, same seed unless you have a reason to change it), and show me the before/after numbers side by side so I can see exactly what moved and by how much. I specifically don't want you trying blindfolded if you believe a change is correct, run it and let the simulation tell us if you're right. If the numbers come back worse, or reveal something weird, tell me straight. Treat this like "fix whatever looks broken" with no other guidance, I want to see what you'd actually do with that authority, and I want the sim to be the judge, not either of our gut feelings about which stat "should" matter more.*
 
### Results: ###

This was the deliberate "let the AI propose independently and test it" prompt. It produced the first genuine failure (see below) rather than an unverified assumption, because the very next step was running it through the sim rather than trusting the reasoning.



### Prompt #3 ###

*Before you touch anything else, let me tell you how I actually read each of these six units, because I think my mental model of their archetypes might not match what the sim is telling us, and I want you to check my read against the actual matchup data instead of just taking my word for it.*

    *- Halden is built as the classic front-line tank. like  the Knights and Paladins from D&D or the heavy Iop-style bruisers in Dofus, someone who plants himself in the front line and just doesn't die, high def and res, wins by attrition rather than burst.*

    *- Rookwood I pictured as more of a nimble skirmisher/duelist type, closer to a Sram or a rogue archetype. I assumed his weakness was his attack being too low for his cost, he hits nothing for his cost.*

    *- Brennan I see him as a line-holder, is the more "mid" of them all, the 50/50 guy, moves at a reasonable speed, does some "normal" atk which i think it should be very similar to his def stats plus his res should kind be also in the middle. Veyr middle-ly unit cost, player might use brennan as the first line of defense.*

    *- Sable (is a she?) is supposed to be an archer, like the fragile high-damage ranged units in Mewgenics or a Baldur's Gate ranger. As an archer she needs to be fast, deal not much damage but as she's faster he might get a chance to attack more times, which makes her a difficult ranged unit to get to, some players might target her first because she's "annoying" in that sense, some players might target larger units first. As an archer she should be easier to kill in terms of hp, has to have lower hp, but because of her speed it's easier for her to move and dodge attacks. Sable needs to have a small unit cost (I think for balance purposes)*

    *- Wisp is my support/cleric archetype, but I think, given his stats, is like a mage-tank that counters Halden in almost everything; has to be slow, high-cost, almost mirrored.*

    *- Pyraxis is my intended burst mage / win-condition unit. Given his current stats I'll put him almost like a direct Rookwood counter, same style of attack and speed but in magic terms.*

*Can you go through each of these one at a time against the actual stat sheet and the win%/crit% data from Prompt #1's table and tell me flat out where my read holds up and where it's wrong? I'd rather you correct me with specific numbers than agree just to be agreeable.*

### Results: ###

Produced a mixed verdict, not a rubber stamp: confirmed my read on Halden, Brennan, and Pyraxis's intended archetype, but corrected two specific claims with matchup data — that Rookwood's bottleneck was *atk* (he already had the best *spd/skl* in the game), and that Sable wasn't actually "glass" in the baseline (her *hp* was tied for second-highest in the roster; she was underpowered for her cost, not fragile).



### Prompt #4 ###

*Alright, we've been doing one-off changes and checking them individually, but I want to switch into more of a rapid-iteration mode now. Let's just keep running it and seeing how everything behaves as we go, instead of treating each stat tweak as its own isolated event.*
*I'm going to mix two kinds of changes together in this pass: actual design decisions on my end: I want you to run the CSV forward through as many versions as it takes until the roster actually feels right, not just stop after one pass. On the design side: I want Wisp to function as Halden's counter-pick, basically a mirror-match answer, if a player builds around Halden as their tank anchor, picking Wisp should meaningfully swing that specific matchup back in the other player's favor, even if Wisp is weaker across the rest of the roster. Same idea with Pyraxis as the counter to Rookwood specifically, I want that one matchup to feel like Pyraxis was built to punish him, without turning Pyraxis into a general unit against everyone else. On top of those relationships, please show me in detail each iteration so I can keep adjusting individual stats wherever the win% numbers still look off from Prompt #1's baseline table. Just version the CSV as you go (v2, v3... and so on) and rerun the sim after every single version, so we always know what changed and what it did. Call out anything weird you notice along the way, even if it's not what we were specifically looking for, I'd rather find surprises now during this iteration phase. We'll compare iteration results and check any strage behaviors as we go, please proceed.*

### Results: ###

Produced two more caught failures (Iteration 5's accidental auto-include, Iteration 7's oversized swing from a 1-point stat change) and two real mechanical discoveries about the combat rules themselves — the doubling threshold is a hard cliff, and damage-floor matchups are hypersensitive to small changes. Neither of those was something either of us went looking for; they came out of just running the numbers and reading what actually happened.



### Prompt #5 ###
*One more thing before we call this balance pass done. I'm still worried about cheap-unit spam, like there might be some degenerate squad comp made entirely of the lowest-cost units that just steamrolls everything because the cost curve doesn't actually punish stacking bodies the way it's supposed to. I don't want you to just reason about this and tell me "I don't think that's a problem",  that's not good enough, because that's exactly we've already caught being wrong twice in this session just by trusting logic. I want you to actually test it:*

*Please extend the simulator so it can:*

    *- Run squad-vs-squad battles instead of just 1v1 duels, reusing the same combat math from sim/simulate.py so we're not introducing new assumptions, just adding the  layer for multiple units fighting at once.*

    *- After that run a bunch of squad comps against each other, cheap-unit-filledsquad vs expensive-but-few, then mixed comps, and then rnadom combinations seem reasonable*

    *- Specifically stress-test against at least one fast-enemy encounter setup, since speed and turn order are exactly the kind of thing a cheap-unit-spam strategy might overuse. If there's genuinely nothing there, just show me the data that proves it. But if there IS a squad comp that's very obviously outperforming everything else, I want to know about it even if it's not a full broken exploit, sometimes a "soft"  pattern that performs suspiciously well is still worth flagging and me knowing about it before it goes anywhere near actual players.*

### Results:###

Produced an actual squad-battle extension of the simulator (reusing the duel model's exact combat math, just adding multi-unit orchestration) rather than a hand-waved answer — and it found a real, worth-reporting soft-degenerate pattern (mass-cheap-bodies scoring notably highest against the fast-enemy encounter) that a purely "I don't think there is one" answer would have missed entirely.

---

## AI WRONG OR MISLEADING MOMENT

**Iteration 5.** Trying to give Brennan a complete, holistic fix (rather than another single-stat poke), It raised both his `def` and `res` together, reasoning that a "durable front-liner" needed both. The sim showed a 71.8% win rate — a worse problem than the one we'd started with, because unlike the original broken Halden (who had an exploitable weak side in low `res`), this version of Brennan had *no* exploitable weakness at all. The reasoning sounded complete and defensible going in ("give the tank real durability"). It was wrong, and the only reason it didn't ship is that the very next step was running it, not trusting the justification. Caught it, understood *why* (stacking both defense stats removes the floor-damage mechanic's ability to punish anyone), and the fix in the next iteration was specifically informed by that failure rather than a guess.

A second, smaller instance of the same pattern happened in Iteration 1 (a 3-point `atk` buff to Rookwood based on sound-sounding logic turned him into an 83.7%-win-rate auto-include) and again in Iteration 7 (a 1-point `atk` *cut* to the same unit swung his win rate by 15 points because the matchup sat right at the damage floor). Three separate instances of the same underlying lesson — reasoning about this system's numbers in the abstract is unreliable, because the combat formulas contain nonlinear thresholds (doubling) and hypersensitive regions (the damage floor) that aren't visible from the stat sheet alone. That's the actual takeaway for how AI should be used here: not as a source of correct numbers, but as a fast hypothesis generator whose output is only trustworthy after it's been run.

---

## SCALING TO 50+ UNITS ACROSS MULTIPLE GAMES PER QUARTER

The workflow that worked at 6 units doesn't scale by just doing more of the same conversation, it needs to be a pipeline with a verification step built in structurally, not just habitually:

1. **Every proposed stat/cost change runs through the sim automatically before a human sees it**, not after — a change that isn't paired with its own before/after numbers shouldn't be reviewable at all.

2. **Isolate variables by default.** Iterations 1 and 5 both failed by changing two stats at once and being unable to tell which one caused the result. At 50+ units, a pipeline should default to single-variable changes with multi-variable changes flagged for extra scrutiny (more trials, an explicit isolation test), not the reverse.

3. **A standing regression suite, not a one-off check.** The multi-seed stability check and the degeneracy squad search should run on every proposed roster change automatically, the same way a test suite runs on every code change — flagging any unit whose win%/cost falls outside a tolerance band, or any squad that spikes above a threshold against a reference encounter, before a human reviews anything.

4. **Known-dangerous patterns get an explicit lint rule.** We now know two specific patterns are high-risk in this rule system: stacking both defense stats on one unit, and changing `spd` near a doubling threshold. At 50+ units, those become automated checks a proposal has to clear, not tribal knowledge one designer has to remember.

5. **AI proposes, sim verifies, human decides.** The role split that worked here holds at scale: AI is fast at generating plausible-sounding candidate changes and reading structured output; the simulation is the actual arbiter of whether a change works; a human designer makes the final call on trade-offs the sim can't see (theme, player experience, what a "fun" weakness looks like) — which is exactly the kind of judgment this whole session kept needing (deciding Wisp should still beat Halden even after softening the matchup, deciding mass-cheap-bodies is an acceptable emergent strategy rather than a bug). None of those were the sim's call to make; all of them needed the sim's numbers to make responsibly.

---