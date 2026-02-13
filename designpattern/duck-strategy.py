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
    
class MallardDuck(Duck):
    
    def fly(self):
        print('Fly in the cloud')
        
    def quack(self):
        print('Quack loud')
        
    def display(self):
        print('I"m MallardDuck')


class RedHeadDuck(Duck):

    def fly(self):
        print('Fly in the cloud')
        
    def quack(self):
        print('Quiet loud')
        
    def display(self):
        print('I"m read head')