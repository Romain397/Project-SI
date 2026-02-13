# strategy/wooden_duck.py

from strategy.duck import Duck
from strategy.fly_behavior import FlyNoWay
from strategy.quack_behavior import MuteQuack


class WoodenDuck(Duck):
    def __init__(self):
        super().__init__(FlyNoWay(), MuteQuack())
