#!/usr/bin/env python
"""
EmptyBot - a skeleton of a bot that you can modify.
Over-commented for educational purposes.
"""

# Import the PlanetWars class from the PlanetWars module. (The planet class here is not necessary
# You can use the planet class to get specific information about a particular planet
from PlanetWarsAPI import PlanetWars


def do_turn(pw):
    """
    Function that gets called every turn.
    This is where to implement the strategies.

    Notice that a PlanetWars object called pw is passed as a parameter which you could use
    if you want to know what this object does, then read the API.

    The next line is to tell PyCharm what kind of object pw is (A PlanetWars object here)
    :type pw: PlanetWars
    """

    # The source variable will contain the planet from which we send the ships.
    # Create a source planet, if you want to know what this object does, then read the API
    source = None

    # The dest variable will contain the destination, the planet to which we send the ships.
    destination = None

    # (1) Implement an algorithm to determine the source planet to send your ships from
    # ... actual code here
    source = pw.my_planets()[0]

    # (2) Implement an algorithm to determine the destination planet to send your ships to
    # ... actual code here
    destination = pw.not_my_planets()[0]

    # (3) Attack/Defend
    # If the source and destination variables contain actual planets, then
    # send half of the ships from source to destination.
    if source is not None and destination is not None:
        pw.issue_order(source, destination)


def main():
    while True:
        # get the new state of the game
        pw = PlanetWars()

        # make a turn (your code)
        do_turn(pw)

        # finish the turn
        pw.finish_turn()


# If this is the main program -> execute main, catch Ctrl-C if pressed
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'ctrl-c, leaving ...'
