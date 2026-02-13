from abc import ABC, abstractmethod

class Duck(ABC):
    
    @abstractmethod
    def fly(self):
        pass
    
    @abstractmethod
    def quack(self):
        pass
    
    @abstractmethod
    def display(self):
        pass

class FlyBehavior(ABC):
    
    @abstractmethod
    def fly(self):
        pass

class FlyNone:
    
    def fly(self):
        print('I believe I can fly')

class FlyCloud:
    
    def fly(self):
        print('Fly in the cloud')

class FlyDry:
    
    def fly(self):
        print('Fly dry')


class MallardDuck(Duck):
    
    def __init__(self, fly_behavior: FlyBehavior):
        self.__fly_behavior = fly_behavior
    
    def fly(self):
        self.__fly_behavior.fly()
    
    def quack(self):
        print('Quack loud')
        
    def display(self):
        print('I"m MallardDuck')


class RedHeadDuck(Duck):
    
    def __init__(self, fly_behavior: FlyBehavior):
        self.__fly_behavior = fly_behavior    

    def fly(self):
        self.__fly_behavior.fly()
        
    def quack(self):
        print('Quiet loud')
        
    def display(self):
        print('I"m read head')