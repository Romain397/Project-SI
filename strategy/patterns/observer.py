# patterns/observer.py

from abc import ABC, abstractmethod
from strategy.duck import Duck


class Observer(ABC):
    @abstractmethod
    def update(self):
        pass


class Quackologist(Observer):
    def update(self):
        print("Un canard a cancané !")


class ObservableDuck(Duck):
    def __init__(self, fly_behavior, quack_behavior):
        super().__init__(fly_behavior, quack_behavior)
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for obs in self.observers:
            obs.update()

    def perform_quack(self):
        super().perform_quack()
        self.notify_observers()
