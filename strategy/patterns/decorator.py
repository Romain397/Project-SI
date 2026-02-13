# patterns/decorator.py

from strategy.duck import Duck


class QuackCounter(Duck):
    number_of_quacks = 0

    def __init__(self, duck):
        self.duck = duck

    def perform_fly(self):
        self.duck.perform_fly()

    def perform_quack(self):
        QuackCounter.number_of_quacks += 1
        self.duck.perform_quack()

    @classmethod
    def get_quacks(cls):
        return cls.number_of_quacks
