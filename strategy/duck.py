# strategy/duck.py


class Duck:
    def __init__(self, fly_behavior, quack_behavior):
        self.fly_behavior = fly_behavior
        self.quack_behavior = quack_behavior

    def perform_fly(self):
        self.fly_behavior.fly()

    def perform_quack(self):
        self.quack_behavior.quack()

    def set_fly_behavior(self, new_behavior):
        self.fly_behavior = new_behavior
