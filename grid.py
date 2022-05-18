import dataclasses
import enum
import numpy as np

from typing import List, Optional

@dataclasses.dataclass(frozen=True)
class Position:
    width: int
    height: int

    @property
    def adj(self):
        return [
            Position(width=self.width+1, height=self.height),
            Position(width=self.width-1, height=self.height),
            Position(width=self.width, height=self.height+1),
            Position(width=self.width, height=self.height-1),
        ]

class Cell(enum.Enum):
    ROAD = 0
    SIDEWALK = 1

class Map:

    def __init__(self, grid: np.ndarray):
        self.grid = grid

    def is_road(self, p: Position) -> bool:
        return self.grid[p.height, p.width] == Cell.ROAD

    def is_sidewalk(self, p: Position) -> bool:
        return self.grid[p.height, p.width] == Cell.SIDEWALK

    def adj(self, p: Position, cell_type: Optional[Cell]) -> List[Position]:
        adj_positions = p.adj
        if cell_type == Cell.ROAD:
            adj_positions = [adj for adj in adj_positions if self.is_road(adj)]
        elif cell_type == Cell.SIDEWALK:
            adj_positions = [adj for adj in adj_positions if self.is_sidewalk(adj)]
        return adj_positions
