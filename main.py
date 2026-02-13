# main.py

from moldu_sorcier import Moldu, Sorcier
from strategy.duck import Duck
from strategy.fly_behavior import FlyWithWings
from strategy.quack_behavior import Quack
from simulator import DuckSimulator

if __name__ == "__main__":

    # Test Moldu / Sorcier
    harry = Sorcier("Harry", "Gryffondor")
    harry.lancer_un_sort()

    jean = Moldu("Jean")

    # Test Duck Simulator
    duck = Duck(FlyWithWings(), Quack())
    simulator = DuckSimulator()
    simulator.simulate(duck)
