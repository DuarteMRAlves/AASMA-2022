import dataclasses
import enum
import numpy as np

from typing import List, Optional

@dataclasses.dataclass(frozen=True)
class Position:
    """Represents the coordinates of a grid position.
    
    This position is not guarantied to be inside the map
    or be of any specific type (such as Road or Sidewalk).
    """
    x: int
    y: int

    @property
    def up(self) -> "Position":
        """Position above this position."""
        # Y-axis is inverted as arrays are indexed as follows:
        # 0      -> [[...],
        # 1      ->  [...],
        # ...         ...
        # len(a) ->  [...]]
        # and so y=y-1 increases the position.
        return Position(x=self.x, y=self.y-1)

    @property
    def down(self) -> "Position":
        """Position below of this position."""
        # Y-axis is inverted as arrays are indexed as follows:
        # 0      -> [[...],
        # 1      ->  [...],
        # ...         ...
        # len(a) ->  [...]]
        # and so y=y+1 decreases the position.
        return Position(x=self.x, y=self.y+1)

    @property
    def left(self) -> "Position":
        """Position to the left of this position."""
        return Position(x=self.x-1, y=self.y)

    @property
    def right(self) -> "Position":
        """Position to the right of this position."""
        return Position(x=self.x+1, y=self.y)

    @property
    def adj(self) -> "List[Position]":
        """Positions that are adjacent to this position.
        
        Returns a list with the position above, below, to the
        right and to the left."""
        return [self.up, self.down, self.left, self.right]

class Cell(enum.Enum):
    ROAD = 0
    SIDEWALK = 1

    def __repr__(self) -> str:
        return f"Cell({self.name})"

class Map:

    def __init__(self, grid: np.ndarray):
        self.grid = grid

    @property
    def height(self):
        return self.grid.shape[0]

    @property
    def width(self):
        return self.grid.shape[1]

    @property
    def all_positions(self) -> List[Position]:
        positions = []
        with np.nditer(self.grid, flags=["multi_index", "refs_ok"]) as it:
            for _ in it:
                y, x = it.multi_index
                positions.append(Position(x=x, y=y))
        return positions

    @property
    def possible_taxi_positions(self) -> List[Position]:
        return [p for p in self.all_positions if self.is_road(p)]

    @property
    def possible_passenger_positions(self) -> List[Position]:
        return [
            p 
            for p in self.all_positions 
            if self.is_sidewalk(p) and self.has_adj_of_type(p, Cell.ROAD)
        ]

    def is_inside_map(self, p: Position) -> bool:
        return 0 <= p.y < self.height and 0 <= p.x < self.width

    def is_road(self, p: Position) -> bool:
        return self.grid[p.y, p.x] == Cell.ROAD

    def is_sidewalk(self, p: Position) -> bool:
        return self.grid[p.y, p.x] == Cell.SIDEWALK

    def adj_positions(self, p: Position, cell_type: Optional[Cell]) -> List[Position]:
        positions = [adj for adj in p.adj if self.is_inside_map(adj)]
        if cell_type == Cell.ROAD:
            positions = [adj for adj in positions if self.is_road(adj)]
        elif cell_type == Cell.SIDEWALK:
            positions = [adj for adj in positions if self.is_sidewalk(adj)]
        return positions

    def has_adj_of_type(self, p: Position, cell_type: Optional[Cell]) -> bool:
        positions = self.adj_positions(p, cell_type)
        if cell_type == Cell.ROAD:
            return any(self.is_road(adj) for adj in positions)
        elif cell_type == Cell.SIDEWALK:
            return any(self.is_sidewalk(adj) for adj in positions)
        else:
            raise ValueError(f"Unknown cell type: {cell_type}")