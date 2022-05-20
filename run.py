import env
import grid
import graphical
import numpy as np
import time

def main():
    map = grid.Map(np.array([
        [grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.ROAD,],
        [grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.ROAD,],
        [grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.SIDEWALK, grid.Cell.ROAD,],
        [grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.ROAD,],
        [grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.SIDEWALK, grid.Cell.ROAD,],
        [grid.Cell.SIDEWALK, grid.Cell.ROAD,     grid.Cell.ROAD,     grid.Cell.ROAD,],
    ]))
    with graphical.EnvironmentPrinter() as printer:
        environment = env.Environment(map=map, init_passengers=1, printer=printer)
        for _ in range(10):
            environment.render()
            time.sleep(1)


if __name__ == "__main__":
    main()