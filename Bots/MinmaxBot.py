#!/usr/bin/env python


# Import the PlanetWars class from the PlanetWars module.
from PlanetWarsAPI import PlanetWars, Planet


def do_turn(pw):
    """
    This is the main function, here we make the decision what to do.
    :type pw: PlanetWars
    """

    try:
        best_option = simulate_actions(pw, 3, 0)
        source = best_option[1]
        dest = best_option[2]


        # Attack.
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
    ship_max = -1.0
    source = None
    dest = None
    strongest_num_ships = -1

    for my_planet in old_pw_state.my_planets():
        if my_planet.number_ships() > strongest_num_ships:
            strongest_planet = my_planet
            strongest_num_ships = my_planet.number_ships()
    for not_my_planet in old_pw_state.not_my_planets():
        new_pw_state = SimulatedPlanetWars(old_pw_state)
        new_pw_state.simulate_attack(strongest_planet, not_my_planet)
        new_pw_state.simulate_growth()
        new_pw_state.simulate_bullybot()
        new_pw_state.simulate_growth()

        if i > 0:
            new_score = simulate_actions(new_pw_state, (i-1), (count+1))
        else:
            new_score = new_pw_state.evaluate_state()
        if new_score == score_max and strongest_planet.number_ships() > ship_max:
            score_max = new_score
            source = strongest_planet
            dest = not_my_planet
            ship_max = strongest_planet.number_ships()
        elif new_score > score_max:
            score_max = new_score
            source = strongest_planet
            dest = not_my_planet
            ship_max = strongest_planet.number_ships()
    if count == 0:
        return [score_max, source, dest]
    return score_max

class SimulatedPlanetWars(PlanetWars):

    def __init__(self, original_pw):

        self._planets = []
        """:type : list[Planet]"""

        PlanetWars.__init__(self, clone=original_pw)

    def simulate_growth(self):

        for p in self._planets:
            # Neutral planets don't grow.
            if p.is_neutral():
                continue
            p.set_number_ships(p.number_ships() + p.growth_rate())

    def simulate_attack(self, source, dest):

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

        source = self._planets[source_id]
        dest = self._planets[dest_id]

        self.simulate_attack(source, dest)

    def simulate_bullybot(self):
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

        my_ships = (1.0 + sum(p.number_ships() for p in self.my_planets()))
        enemy_ships = (1.0 + sum(p.number_ships() for p in self.enemy_planets()))
        ship_score = my_ships / enemy_ships

        my_growth_rate = (1.0 + sum(p.growth_rate() for p in self.my_planets()))
        enemy_growth_rate = (1.0 + sum(p.growth_rate() for p in self.enemy_planets()))
        growth_score = my_growth_rate / enemy_growth_rate

        my_planets = (1.0 + sum(1.0 for p in self.my_planets()))
        enemy_planets = (1.0 + sum(1.0 for p in self.enemy_planets()))
        planet_score = my_planets / enemy_planets

        total_score = planet_score + (0.5 * growth_score) + (0.25 * ship_score)

        return total_score


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
