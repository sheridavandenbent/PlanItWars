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
        source = best_option[1]
        dest = best_option[2]


        # (3) Attack.
        # If the source and dest variables contain actual planets, then
        # send half of the ships from source to dest.
        if source is not None and dest is not None:
            pw.issue_order(source, dest)
        else:
            source_score = -100000
            dest_score = 100000

            for p in pw.planets():
                if p.owner() == 1:
                    score_max = p.number_ships()
                    if score_max > source_score:
                        source_score = score_max
                        source = p
                else:
                    score_min = p.number_ships()
                    if score_min < dest_score:
                        dest_score = score_min
                        dest = p
            pw.issue_order(source, dest)
    except Exception, e:
        pw.log(e.message, e.__doc__)

def simulate_actions(old_pw_state, i, count):
    score_max = -1.0
    source = None
    dest = None

    for my_planet in old_pw_state.my_planets():
        # Skip planets with only one ship
        if my_planet.number_ships() <= 1:
            continue
        for not_my_planet in old_pw_state.not_my_planets():
            new_pw_state = SimulatedPlanetWars(old_pw_state)
            new_pw_state.simulate_attack(my_planet, not_my_planet)
            new_pw_state.simulate_growth()
            new_pw_state.simulate_bullybot()
            new_pw_state.simulate_growth()

            if i > 0:
                new_score = simulate_actions(new_pw_state, (i-1), (count+1))
            else:
                new_score = new_pw_state.evaluate_state()
            if new_score > score_max:
                score_max = new_score
                source = my_planet
                dest = not_my_planet
    if count == 0:
        print source
        return [score_max, source, dest]
    return score_max

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
        source = None
        dest = None

        source_score = -100000
        dest_score = 100000

        for p in self.planets():
            # self.log("Planet(ships:%d, owner:%d)" % (p.number_ships(), p.owner()))
            if p.is_enemy():
                if p.number_ships() <= 1:
                    continue

                score_max = p.number_ships()
                if score_max > source_score:
                    source_score = score_max
                    source = p
            else:
                score_min = p.number_ships()
                if score_min < dest_score:
                    dest_score = score_min
                    dest = p

        if source is not None and dest is not None:
            self.simulate_attack(source, dest)

    def evaluate_state(self):

        try:
            my_ships = (1.0 + sum(p.number_ships() for p in self.my_planets()))
            enemy_ships = (1.0 + sum(p.number_ships() for p in self.enemy_planets()))
            ship_score = my_ships / enemy_ships

            my_growth_rate = (1.0 + sum(p.growth_rate() for p in self.my_planets()))
            enemy_growth_rate = (1.0 + sum(p.growth_rate() for p in self.enemy_planets()))
            growth_score = my_growth_rate / enemy_growth_rate

            my_planets = (1.0 + sum(1.0 for p in self.my_planets()))
            enemy_planets = (1.0 + sum(1.0 for p in self.enemy_planets()))
            planet_score = my_planets / enemy_planets

            total_score = ship_score + (5 * growth_score) + (2 * planet_score)
            return total_score

        except Exception, e:
            print (e.message, e.__doc__)


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
