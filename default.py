import grid
import numpy as np

WIDTH = 800
HEIGHT = 800

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