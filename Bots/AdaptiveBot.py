#!/usr/bin/env python
"""
This bot is a bit overly complicated, it was still here from the original authors of the code.
The TL;DR of the code beneath (and the code in AdaptivityMap) is this:
- We assume some bots are better for some maps and some better for others.
- We calculate some characteristics of the current map (nr of neutral planets and average growth rate)
- In AdaptivityMap there is a large table, linking growth-rate and amount of neutral planets to the ideal bot
- We execute the code of that bot
The original intention was also change the table in Adaptivity Map for the best performance
(note that editing a 6x26 matrix is not that ideal, also the heuristics are rather bad)

/*
 * You're not expected
 * to understand this
 */

AdaptiveBot - A bot which adapts its behaviour according to the environment characteristics.
It changes its strategy, based on the current environment (e.g. number of neutral planets in the map,
number of ships, etc.). Knowing which strategy to use has to be collected beforehand.
This requires running a number of games of your bots, and evaluate which bot performs best for a certain environment.
You should then add this to the data structure (in AdaptivityMap.java).
The DoTurn method can then query this data structure to know what strategy should be used for this turn.
This example provides two environment variables: the number of neutral planets on the map, and the average growth
ratio of these neutral planets.

We provide a possible implementation using the hash adaptivityMap, which maps lists of integers (representing
the environment) with names of bots. See AdaptivityMap.py

Interesting questions (you can probably come up with other questions yourself as well):
 * 1. Can you modify or extend the environment variables we use? Maybe other things are interesting other than the number of neutral planets, and the average planet growth rate of these neutral planets.
 * 2. The table in AdaptivityMap.java is filled by us (randomly) with only two simple bots. But how should the table really look like?
 * This means you should collect data on how all your previous bots (BullyBot, RandomBot, HillclimbingBot, LookaheadBot and/or others) perform in different environments
 * 3. Can you implement your other bot implementations in AdaptiveBot.java? Currently the only strategies are BullyBot ('DoBullyBotTurn') and RandomBot ('DoRandomBotTurn').
 * Implement the bot strategies you used to fill AdaptivityMap.java here as well.
"""
# Import the PlanetWars class from the PlanetWars module.
import BullyBot
import LookaheadBot
import RandomBot
from AdaptivityMap import AdaptivityMap
from PlanetWarsAPI import PlanetWars

def do_turn(pw):
    """ Function that gets called every turn.
    This is where to implement the strategies.

    :type pw : PlanetWars
    """

    # Retrieve environment characteristics - features you can use to decide which bot to use for that specific map.
    # Are there characteristics you want to use instead, or are there more you'd like to use? Try it out!
    # In this example we will use the number of neutral planets and the average planet growth rate of neutral planets.
    neutral_planets = pw.neutral_planets()
    average_growth_rate = 0

    if len(neutral_planets) > 0:
        average_growth_rate = sum(p.growth_rate() for p in neutral_planets) / len(neutral_planets)

    adaptivity_map = AdaptivityMap()

    # Use AdaptivityMap to get the bot which matches the current environment characteristics
    this_turn_bot = adaptivity_map.get_best_bot(len(neutral_planets), average_growth_rate)

    if this_turn_bot is None:
        # There is no entry for the specified num_neutral_planets and average_growth_rate.
        RandomBot.do_turn(pw)
    elif this_turn_bot is 'BullyBot':
        BullyBot.do_turn(pw)
    elif this_turn_bot is 'RandomBot':
        RandomBot.do_turn(pw)
    elif this_turn_bot is 'LookaheadBot':
        LookaheadBot.do_turn(pw)
    else:
        # The bot in the entry is not supported yet.
        RandomBot.do_turn(pw)


# The main module that get's called everytime
def main():
    while True:
        pw = PlanetWars()
        do_turn(pw)
        pw.finish_turn()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'ctrl-c, leaving ...'
