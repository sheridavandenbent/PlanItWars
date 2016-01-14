#!/usr/bin/env python

"""
RandomBot - an example bot that picks up one of his planets and send half of the ships
from that planet to a random target planet.

Not a very clever bot, but showcases the functions that can be used.
Over-commented for educational purposes.
"""

# Import the module that implements the random number generator.
import random
# Import the PlanetWars class from the PlanetWars module.
from PlanetWarsAPI import PlanetWars


def do_turn(pw):
    """
    This is the function that get's called every turn. Strategies implemented here.
    :type pw: PlanetWars
    """

    # The source variable will contain the planet from which we send the ships.
    source = None

    # The destination variable will contain the destination planet, we send the ships here.
    destination = None

    # Get a list of all my planets and store it in the variable my_planets.
    my_planets = pw.my_planets()

    # The number of planets I own is the length of this list.
    number_of_my_planets = len(my_planets)

    # An example debug statement. These statements are useful when you don't understand the behaviour of your bot.
    pw.log("I have %d planets. (example debug statement, you can remove or change me!)" % number_of_my_planets)

    # If I own at least a planet, i.e. there is at least one planet in the list.
    if number_of_my_planets > 0:
        # Use random.choice to obtain a random planet from which we send our fleet
        source = random.choice(my_planets)

    # Get a list of all planets which are either enemy or neutral (not mine).
    not_my_planets = pw.not_my_planets()

    # The number of planets I don't own is the length of this list.
    number_of_not_my_planets = len(not_my_planets)

    # If there is at least a planet I don't own, i.e. there is at least one planet in the list.
    if number_of_not_my_planets > 0:
        # Select a planet that is not ours, and set it as target for our fleet
        destination = random.choice(not_my_planets)

    # If the source and destination variables contain actual planets, then
    # send half of the ships from source to destination.
    if source is not None and destination is not None:
        pw.issue_order(source, destination)


def main():
    # This is the main routine, it ...
    while True:
        # Creates a PlanetWars game state object
        pw = PlanetWars()

        # makes a turn
        do_turn(pw)

        # and finishes it
        pw.finish_turn()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'ctrl-c, leaving ...'
