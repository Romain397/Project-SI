from dataclasses import dataclass, field

class Ship:
    # speed: m/s
    # time_to_speed: seconds
    def __init__(self, name:str, color, speed, time_to_speed):
        self.__name = name
        self.__color = color
        self.__speed = speed
        self.__time_to_speed = time_to_speed

    @property
    def name(self):
        return self.__name

    @property
    def speed(self):
        return self.__speed
    
    @property
    def time_to_speed(self):
        return self.__time_to_speed

    def __repr__(self):
        return self.__name
    
    def __hash__(self):
        return hash(self.__name)
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.name == self.name
        return False
    

@dataclass
class DataShip:
    name: str
    color: str = field(repr=False)
    speed: float
    time_to_speed: int


class Track:
    
    def __init__(self, name, distance):
        self.__name = name
        self.__distance = distance
        
    @property
    def distance(self):
        return self.__distance

# link between Ship and nb_ticks through Competitor
class CompetitorInheritance(Ship):

    def __init__(self, name:str, color, speed, time_to_speed):
        super().__init__(name, color, speed, time_to_speed)
        self.__nb_ticks = 0

    def move(self, track, nb_laps):
        total_distance_to_run = track.distance * nb_laps
        self.__nb_ticks = total_distance_to_run / self.speed + self.time_to_speed
        
    @property
    def nb_ticks(self):
        return self.__nb_ticks
    
    def __repr__(self):
        return f'{self.name} finished in {self.__nb_ticks} ticks.'

# link by composition between Ship and nb_ticks through Competitor
class CompetitorComposition:

        def __init__(self, ship):
            self.__ship = ship
            self.__nb_ticks = 0

        def move(self, track, nb_laps):
            total_distance_to_run = track.distance * nb_laps
            self.__nb_ticks = total_distance_to_run / self.__ship.speed + self.__ship.time_to_speed

        @property
        def nb_ticks(self):
            return self.__nb_ticks

        def __repr__(self):
            return f'{self.__ship.name} finished in {self.__nb_ticks} ticks.'

class Simulation:
    
    def __init__(self, track, nb_laps):
        self.__track = track
        self.__nb_laps = nb_laps
        self.__ships = set()
    
    
    @property
    def track(self):
        return self.__track
    
    @property
    def nb_laps(self):
        return self.__nb_laps
    
    def add_competitor(self, ship):
        self.__ships.add(ship)
        
    def display_competitors(self):
        print(self.__ships)
        
    def start(self):
        for ship in self.__ships:
            ship.move(self.track, self.nb_laps)
            
        
if __name__ == '__main__':
    ship1 = CompetitorInheritance('ship1', 'red', 10, 3)    
    ship1_copy = CompetitorInheritance('ship1', 'red', 10, 3)
    ship2 = CompetitorComposition(Ship('ship2', 'yellow', 20, 100))
    ship3 = CompetitorComposition(Ship('ship3', 'green', 20, 10))
    track = Track('track', 1000)
    simu = Simulation(track, 62)
    for s in [ship1, ship1_copy, ship2, ship3]:
        simu.add_competitor(s)
    simu.display_competitors()
    simu.start()
    simu.display_competitors()
    