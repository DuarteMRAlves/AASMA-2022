import grid
import numpy as np
 

MAP = np.array([
    [grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK],
    [grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK],
    [grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.SIDEWALK],
    [grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK],
    [grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK],
    [grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.SIDEWALK],
    [grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK],
    [grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK],
    [grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK],
    [grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.SIDEWALK],
])