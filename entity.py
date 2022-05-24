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

    def move(self):
        if self.direction == Direction.UP:
            self.loc = self.loc.up
        elif self.direction == Direction.DOWN:
            self.loc = self.loc.down
        elif self.direction == Direction.RIGHT:
            self.loc = self.loc.right
        elif self.direction == Direction.LEFT:
            self.loc = self.loc.left
        else:
            raise ValueError(f"Unknown direction in taxi movement {self.direction}")

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
            raise ValueError(f"Unknown direction in taxi rotate right {self.direction}")

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
            raise ValueError(f"Unknown direction in taxi rotate left {self.direction}")