# strategy/quack_behavior.py

from abc import ABC, abstractmethod


class QuackBehavior(ABC):
    @abstractmethod
    def quack(self):
        pass


class Quack(QuackBehavior):
    def quack(self):
        print("Coin coin")


class MuteQuack(QuackBehavior):
    def quack(self):
        print("... silence ...")
