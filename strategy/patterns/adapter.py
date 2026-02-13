# patterns/adapter.py

from strategy.duck import Duck


class Goose:
    def honk(self):
        print("Honk")


class GooseAdapter(Duck):
    def __init__(self, goose):
        self.goose = goose

    def perform_fly(self):
        print("Je vole comme une oie")

    def perform_quack(self):
        self.goose.honk()
