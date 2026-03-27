class Spaceship:
    
    __instance = None

    
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance



class SingletonMeta(type):
    
    __instance = None
    
    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance
    
class SpaceshipSingleton(metaclass=SingletonMeta):
    
    def __init__(self, max_speed):
        self.__max_speed = max_speed
    
    @property
    def max_speed(self):
        return self.__max_speed

class Pilot(metaclass=SingletonMeta):
    
    def pilot_high(self):
        print('houra')

if __name__ == '__main__':
    a = Spaceship.get_instance()
    b = Spaceship.get_instance()
    print(f'Type: {type(a)}, Name: {a}')
    print(f'Type: {type(b)}, Name: {b}')
    assert a == b
    
    u1 = SpaceshipSingleton(10)
    u2 = SpaceshipSingleton(20)
    
    assert u1 == u2
    print(u1.max_speed)
    print(u2.max_speed)
    assert u1.max_speed == u2.max_speed
    assert u1.max_speed == 10
    
    p1 = Pilot()
    print(type(p1))