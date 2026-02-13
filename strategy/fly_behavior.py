# strategy/fly_behavior.py

from abc import ABC, abstractmethod


class FlyBehavior(ABC):
    @abstractmethod
    def fly(self):
        pass


class FlyWithWings(FlyBehavior):
    def fly(self):
        print("Je vole avec des ailes")


class FlyNoWay(FlyBehavior):
    def fly(self):
        print("Je ne vole pas")
