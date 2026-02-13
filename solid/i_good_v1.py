from abc import ABC, abstractmethod

class Movable(ABC):
    @abstractmethod
    def go(self):
        pass

class Flyable(Movable):    
    @abstractmethod
    def fly(self):
        pass
    
class Aircraft(Flyable):
    def go(self):
        print("Taxiing")
    def fly(self):
        print("Flying")

class Car(Movable):
    def go(self):
        print("Going")
    
if __name__ == '__main__':
    airbus = Aircraft()
    airbus.go()
    airbus.fly()
    
    f1 = Car()
    f1.go()
