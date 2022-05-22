import dataclasses
import enum
import grid

@dataclasses.dataclass
class Passenger:
    pick_up: grid.Position
    drop_off: grid.Position

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