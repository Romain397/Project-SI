from abc import ABC, abstractmethod

class Beverage(ABC):
    
    def __init__(self, description, beverage = None):
        self.__description = description
        self.__beverage = beverage
        
    @abstractmethod
    def cost(self):
        pass
    
    @property
    def description(self):
        return self.__description
    
    @property
    def beverage(self):
        return self.__beverage
    
class Coffee(Beverage):
    
    def __init__(self):
        super().__init__('coffee')
        
    def cost(self):
        return 1
        
class Latte(Beverage):
    
    def __init__(self):
        super().__init__('latte')
        
    def cost(self):
        return 2
        
class Chocolate(Beverage):
    
    def __init__(self):
        super().__init__('chocolate')
        
    def cost(self):
        return 1.5

class Ingredient(Beverage):
    
    def __init__(self, price, quantity, description, beverage:Beverage):
        self.__price = price
        self.__quantity = quantity
        super().__init__(description=description, beverage=beverage)
        
    def cost(self):
        return self.__price * self.__quantity + self.beverage.cost()

class Soja(Ingredient):
    
    def __init__(self, quantity, beverage):
        super().__init__(1, quantity, 'soja', beverage)
        
class CoffeeBean(Ingredient):
    
    def __init__(self, quantity, beverage):
        super().__init__(2, quantity, 'coffeebean', beverage)
        
class Sugar(Ingredient):
    
    def __init__(self, quantity, beverage):
        super().__init__(1.5, quantity, 'sugar', beverage)
        
class Milk(Ingredient):
    
    def __init__(self, quantity, beverage):
        super().__init__(0.6, quantity, 'milk', beverage)

if __name__ == '__main__':
    beverage = Sugar(1, Sugar(1, Milk(2, Coffee())))
    print(beverage.cost())