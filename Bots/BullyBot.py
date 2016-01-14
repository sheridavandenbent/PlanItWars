#!/usr/bin/env python

"""
BullyBot - A bit smarter kind of bot, who searches for its strongest planet and then attacks the weakest planet.
The score is computed based on the number of ships.
"""
# Import the PlanetWars class from the PlanetWars module.
from PlanetWarsAPI import PlanetWars


def do_turn(pw):
    """:type pw: PlanetWars"""

    # The source variable will contain the planet from which we send the ships.
    source = None

    # The dest variable will contain the destination, the planet to which we send the ships.
    destination = None

    # (1) Find my strongest planet
    # (1.1) Create a list of my planets with their number of ships as score, in the following form
    # [(score, planet), ... , (score, planet)]
    planet_scores = [(p.number_ships(), p) for p in pw.my_planets()]
    # (1.2) Get the item with maximum first argument (the score) and catch the result
    score, source = max(planet_scores)

    # (2) Find the weakest enemy or neutral planet (lowest score).
    # (2.1) Create a list of planets that are not mine with their number of ships as score, in the following form
    # [(score, planet), ... , (score, planet)]
    planet_scores = [(p.number_ships(), p) for p in pw.not_my_planets()]
    # (2.2) Get the item with maximum first argument (the score) and catch the result
    score, destination = min(planet_scores)

    # (3) Attack.
    # If the source and dest variables contain actual planets, then
    # send half of the ships from source to dest.
    if source is not None and destination is not None:
        pw.issue_order(source, destination)


# Don't change from this point on. Also not necessary to understand all the details.
# Machinery that reads the status of the game and puts it into PlanetWars.
# It calls do_turn.
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
