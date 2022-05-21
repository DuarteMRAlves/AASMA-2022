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
                height, width = it.multi_index
                positions.append(Position(width=width, height=height))
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
        return 0 <= p.height < self.height and 0 <= p.width < self.width

    def is_road(self, p: Position) -> bool:
        return self.grid[p.height, p.width] == Cell.ROAD

    def is_sidewalk(self, p: Position) -> bool:
        return self.grid[p.height, p.width] == Cell.SIDEWALK

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