from duck_strategy import Duck, FlyBehavior, QuackBehavior
from duck_strategy import MallardDuck, RedHeadDuck, RubberDuck, DisplayBold
from weatherstation_observer import Observer

class QuackoLogist(Observer):
    
    def __init__(self, pseudo):
        self.__pseudo = pseudo
        self.__ducks_quack = {}
        
    def notify(self, subject):
        duck = subject
        if duck in self.__ducks_quack:
            self.__ducks_quack[duck] += 1
        else:
            self.__ducks_quack[duck] = 1

class DuckSimulator:
    
    nb_quacks = {}

    
    def number_of_quacks(func):
        def inner(self, duck:Duck):
            old_quack = duck.quack
            def new_quack():
                old_quack()
                if duck in DuckSimulator.nb_quacks:
                    DuckSimulator.nb_quacks[duck] += 1
                else:
                    DuckSimulator.nb_quacks[duck] = 1
                print(DuckSimulator.nb_quacks[duck])
            duck.quack = new_quack
            func(self, duck)
        return inner
    
    def simulate(self, duck:Duck):
        #duck = DuckQuackCounter(duck)
        self.__fly_n_times(duck, 2)
        self.__quack_n_times(duck, 4)
        self.__fly_n_times(duck, 3)

    def __quack_n_times(self, duck, n_times):
        for _ in range(n_times):
            duck.quack()

    
    def __fly_n_times(self, duck, n_times):
        for _ in range(n_times):
            duck.fly()

class DuckAugmented(Duck):
    
    def __init__(self, duck:Duck):
        super().__init__(duck._Duck__fly_behavior, duck._Duck__quack_behavior, duck._Duck__display_behavior)
        self.__duck = duck
        
    @property
    def duck(self):
        return self.__duck

class DuckQuackCounter(DuckAugmented):
    
    def __init__(self, duck:Duck):
        self.__quack_counter = 0
        super().__init__(duck)
    
    def quack(self):
        self.__quack_counter += 1
        self.duck.quack()
        print(f'Quack has been called {self.__quack_counter} times')

class DuckQuackStar(DuckAugmented):
    
    def __init__(self, duck:Duck):
        super().__init__(duck)
        
    def quack(self):
        self.duck.quack()
        print('*****')

class Goose:
    
    def honk(self):
        print('honk')
        
    def fly(self):
        print('Goosing')


# goose as a duck ?
class GooseAsDuck(Duck):
    
    def __init__(self, goose: Goose):
        super().__init__(self, None, None)
        self.__goose = goose
    
    def quack(self):
        self.__goose.honk()
        
    def fly(self):
        self.__goose.fly()

class GooseFly(FlyBehavior):
    def fly(self):
        print('goosing like a duck')
        
class GooseQuack(QuackBehavior):
    def quack(self):
        print('honking like a duck')

class MonsterGoose(Duck, Goose):
    
    # missing constructor for Duck
    def __init__(self):
        super().__init__(GooseFly(), GooseQuack(), DisplayBold())
    
    def quack(self):
        super().honk()
        
    def fly(self):
        self.fly_like_a_goose()



if __name__ == '__main__':
    quackologist = QuackoLogist('Jean-Bernard-Rao')
    ducks = []
    ducks.append(MallardDuck())
    ducks.append(RedHeadDuck())
    ducks.append(RubberDuck())
    for duck in ducks:
        duck.add_observer(quackologist)
    sim_duck = DuckSimulator()
    for duck in ducks:
         sim_duck.simulate(duck)
    sim_duck.simulate(GooseAsDuck(Goose()))
    #sim_duck.simulate(MonsterGoose())
    print(quackologist._QuackoLogist__ducks_quack)
    