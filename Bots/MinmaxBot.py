#!/usr/bin/env python

"""
MinmaxBot - Another smarter kind of bot, which implements a minimax algorithm with look-ahead of two turns.
It simulates the opponent using the minimax algorithm and simulates the possible outcomes for any
choice of source and destination planets in the attack. The simulated outcome states are ranked by
the evaluation function, which returns the most promising one.

Try to improve this bot. For example, you can try to answer some of this questions.
 - Can you come up with smarter heuristics/scores for the evaluation function?
 - What happens if you run this bot against your bot from week1?
 - How can you change this bot to beat your week1 bot?
 - Can you extend the bot to look ahead more than two turns? How many turns do you want to look ahead?
 - Is there a smart way to make this more efficient?
"""
# Import the PlanetWars class from the PlanetWars module.
from PlanetWarsAPI import PlanetWars, Planet


def do_turn(pw):
    """
    This is the main function, here we make the decision what to do.
    :type pw: PlanetWars
    """

    try:

        # We try to simulate each possible action and its outcome after two turns
        # considering each of my planets as a possible source
        # and each enemy planet as a possible destination.
        score = -1

        best_option = simulate_actions(pw, 3, 0)

        print best_option

        source = best_option[1]
        dest = best_option[2]

        # (3) Attack.
        # If the source and dest variables contain actual planets, then
        # send half of the ships from source to dest.
        if source is not None and dest is not None:
            pw.issue_order(source, dest)
    except Exception, e:
        pw.log(e.message, e.__doc__)

def simulate_actions(pw_state, old_i, old_count):
    i = old_i
    count = old_count
    new_pw_state = SimulatedPlanetWars(pw_state)
    try:
        total_scores = []
        if count%2 == 0:
            for my_planet in new_pw_state.my_planets():
                # Skip planets with only one ship
                if my_planet.number_ships() <= 1:
                    continue

                for not_my_planet in new_pw_state.not_my_planets():
                    new_pw_state.simulate_attack(my_planet, not_my_planet)
                    new_pw_state.simulate_growth()
                    if i > 0:
                        total_scores.append([simulate_actions(new_pw_state, (i-1), (count+1)), my_planet, not_my_planet])
                    else:
                        total_scores.append(new_pw_state.evaluate_state())
            if i > 0:
                score, source_planet, destination = max(total_scores)
            else:
                score = max(total_scores)
            print "max"
            print total_scores
            print max(total_scores)
        else:
            not_enemy_planets = new_pw_state.my_planets()
            not_enemy_planets.extend(new_pw_state.neutral_planets())
            for enemy_planet in new_pw_state.enemy_planets():
                # Skip planets with only one ship
                if enemy_planet.number_ships() <= 1:
                    continue
                for my_planet in not_enemy_planets:
                    new_pw_state.simulate_attack(enemy_planet, my_planet)
                    new_pw_state.simulate_growth()
                    if i > 0:
                        total_scores.append([simulate_actions(new_pw_state, (i-1), (count+1)), enemy_planet, my_planet])
                    else:
                        total_scores.append(new_pw_state.evaluate_state())
            if i > 0:
                score, source_planet, destination = min(total_scores)
            else:
                score = min(total_scores)
            print "min"
            print total_scores
            print min(total_scores)
        if i == 3:
            return [score, source_planet, destination]
        else:
            return score


    except Exception, e:
        new_pw_state.log(e.message, e.__doc__)


class SimulatedPlanetWars(PlanetWars):
    """
    SimulatedPlanetWars, like the name suggests, simulates a PlanetWars object.
    It inherits all its features (including my_planets() and everything)

    It allows to simulate the actions before executing them and evaluate the
    consequences, including the growth in the planets.
    """

    def __init__(self, original_pw):
        """
        Constructs a SimulatedPlanetWars object instance, given a PlanetWars object
        :type original_pw: PlanetWars
        """

        self._planets = []
        """:type : list[Planet]"""

        PlanetWars.__init__(self, clone=original_pw)

    def simulate_growth(self):
        """
        Simulates the growth of all the non neutral planets.
        Note: Neutral planets don't have growth
        """

        for p in self._planets:
            # Neutral planets don't grow.
            if p.is_neutral():
                continue
            p.set_number_ships(p.number_ships() + p.growth_rate())

    def simulate_attack(self, source, dest):
        """
        Simulates an attack from source to destination
        :type source : Planet
        :type dest : Planet
        :rtype None
        """
        if source is not None and dest is not None:
            sent_ships = source.number_ships() // 2
            source.set_number_ships(source.number_ships() - sent_ships)

            if dest.number_ships() < sent_ships:
                dest.set_owner(source.owner())

            # if we're defending
            if dest.owner() is source.owner():
                dest.set_number_ships(dest.number_ships() + sent_ships)
            # if we're attacking
            else:
                dest.set_number_ships(abs(dest.number_ships() - sent_ships))

    def simulate_attack_by_id(self, source_id, dest_id):
        """
        Simulates the attack by player_id from planet source to planet dest.
        :type source_id: int
        :type dest_id: int
        :rtype None
        """
        source = self._planets[source_id]
        dest = self._planets[dest_id]

        self.simulate_attack(source, dest)

    def simulate_bullybot(self):
        """
        This is basically the code in Bullybot.py, except for one key difference:
        it only acts on the simulated game state.
        """
        # (1) Find my strongest planet
        # (1.1) Create a list of my planets with their number of ships as score, in the following form
        # [(score, planet), ... , (score, planet)]
        planet_scores = [(p.number_ships(), p) for p in self.my_planets()]
        # (1.2) Get the item with maximum first argument (the score) and catch the result
        score, source = max(planet_scores)

        # (2) Find the weakest enemy or neutral planet (lowest score).
        # (2.1) Create a list of planets that are not mine with their number of ships as score, in the following form
        # [(score, planet), ... , (score, planet)]
        planet_scores = [(p.number_ships(), p) for p in self.not_my_planets()]
        # (2.2) Get the item with maximum first argument (the score) and catch the result
        score, destination = min(planet_scores)

        # (3) Attack.
        # If the source and dest variables contain actual planets, then
        # send half of the ships from source to dest.
        if source is not None and destination is not None:
            self.simulate_attack(source, destination)

    def evaluate_state(self):
        """
        Evaluates how promising a simulated state is.

        CHANGE HERE:
        Currently it computes the total number of my ships/total number of enemy ships.
        This means that the biggest the proportion of my ships,
        the highest the score of the evaluated state.
        You can change it to anything that makes sense, using combinations
        of number of planets, ships or growth rate.
        Returns score of the final state of the simulation
        """

        my_ships = (1.0 + sum(p.number_ships() for p in self.my_planets()))
        enemy_ships = (1.0 + sum(p.number_ships() for p in self.enemy_planets()))

        return my_ships / enemy_ships


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
