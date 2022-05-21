import dataclasses
import enum
import grid

@dataclasses.dataclass(frozen=True)
class Passenger:
    pick_up: grid.Position
    drop_off: grid.Position

    # Passenger metrics
    pick_up_time: int
    travel_time: int

class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

@dataclasses.dataclass
class Taxi:
    loc: grid.Position
    direction: Direction 
    has_passenger: bool = False