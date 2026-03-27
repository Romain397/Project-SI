from abc import ABC, abstractmethod
from weatherstation_observer import Subject

class FlyBehavior(ABC):
    
    @abstractmethod
    def fly(self):
        pass

class QuackBehavior(ABC):
    
    @abstractmethod
    def quack(self):
        pass

class DisplayBehavior(ABC):
    
    @abstractmethod
    def display(self):
        pass

class Duck(Subject, ABC):
    
    def __init__(self, fly_behavior:FlyBehavior, quack_behavior:QuackBehavior, display_behavior:DisplayBehavior):
        super().__init__()
        self.__fly_behavior = fly_behavior
        self.__quack_behavior = quack_behavior
        self.__display_behavior = display_behavior
    
    def fly(self):
        self.__fly_behavior.fly()

    def quack(self):
        self.__quack_behavior.quack()
        self.notify()
        
    def display(self):
        self.__display_behavior.display()

    def change_fly_behavior(self, fly_behavior):
        self.__fly_behavior = fly_behavior

    def notify(self):
        for observer in super().observers:
            observer.notify(self)
            
    def __repr__(self) -> str:
        return self.__class__.__name__

class FlyNone(FlyBehavior):
    
    def fly(self):
        print('I believe I can fly')

class FlyCloud(FlyBehavior):
    
    def fly(self):
        print('Fly in the cloud')

class FlyDry(FlyBehavior):
    
    def fly(self):
        print('Fly dry')


class MallardDuck(Duck):
    
    def __init__(self):
        super().__init__(
            fly_behavior=FlyDry(),
            quack_behavior=QuackLoud(),
            display_behavior=DisplayBold())
    

class RedHeadDuck(Duck):
    
    def __init__(self):
        super().__init__(
            fly_behavior=FlyDry(),
            quack_behavior=QuackLoud(),
            display_behavior=DisplayBold())   
        

class RubberDuck(Duck):
    
    def __init__(self):
        super().__init__(fly_behavior=FlyNone(),
                    quack_behavior=QuackLoud(),
                    display_behavior=DisplayBold())
        

class QuackLoud(QuackBehavior):
    
    def quack(self):
        print('Quack loud')
        
class BeQuiet(QuackBehavior):
    
    def quack(self):
        print('....')

class DisplayBold(DisplayBehavior):
    
    def display(self):
        print('Bold duck')

if __name__ == '__main__':
    donald = MallardDuck()
    picsou = RedHeadDuck()
    rubber = RubberDuck()
    donald.fly()
    picsou.fly()
    rubber.fly()
    picsou.change_fly_behavior(FlyNone())
    picsou.fly() # I believe I can fly expected ???