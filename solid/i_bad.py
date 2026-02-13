from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def go(self):
        pass
    
    @abstractmethod
    def fly(self):
        pass
    
class Aircraft(Vehicle):
    def go(self):
        print("Taxiing")
    def fly(self):
        print("Flying")

class Car(Vehicle):
    def go(self):
        print("Going")
    def fly(self):
        raise Exception('The car cannot fly')
    
if __name__ == '__main__':
    airbus = Aircraft()
    airbus.go()
    airbus.fly()
    
    try:
        f1 = Car()
        f1.go()
        f1.fly()
    except Exception as e:
        print(e)