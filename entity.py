import dataclasses
import enum
import grid

@dataclasses.dataclass
class Passenger:
    pick_up: grid.Position
    drop_off: grid.Position
    in_trip : bool = False
    
    # Passenger metrics
    pick_up_time: int = 0
    travel_time: int = 0



class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __repr__(self) -> str:
        return f"Direction({self.name})"

@dataclasses.dataclass
class Taxi:
    loc: grid.Position
    direction: Direction 
    has_passenger: bool = False

    def rot_r(self):
        if self.direction == Direction.UP:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP
        else:
            raise ValueError(f"Unknown direction in taxi rotate right {self.direction}.")

    def rot_l(self):
        if self.direction == Direction.UP:
            self.direction = Direction.LEFT
        elif self.direction == Direction.DOWN:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.UP
        elif self.direction == Direction.LEFT:
            self.direction = Direction.DOWN
        else:
            raise ValueError(f"Unknown direction in taxi rotate left {self.direction}.")
        
    def pickup_up(self, passengers: list, env_grid: grid.Map):
        """Picks-Up Passenger from a location if near him"""
        passenger = env_grid.choose_adj_passenger(self.loc, passengers)
        if passenger != None and self.has_passenger == False:
            print("Picks passenger")
            passenger.in_trip = True
            self.has_passenger = True
            return passenger
            
        return None