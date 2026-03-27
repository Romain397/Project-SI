from abc import ABC, abstractmethod

class SuperClass(ABC):
    def __init__(self, super_parameter):
        self.__super_parameter = super_parameter
        
    @abstractmethod
    def this_is_abstract(self):
        ...

class ThisIsConcrete(SuperClass):
    
    def __init__(self):
        super().__init__('')
    
    def this_is_abstract(self):
        ...
    
if __name__ == '__main__':
    
    this_is_concrete = ThisIsConcrete()
    