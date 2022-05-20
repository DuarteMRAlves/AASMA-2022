import abc
import default
import entity
import env
import grid
import numpy as np
import pygame

from typing import Optional

class EnvironmentPrinter(env.Printer):

    def __init__(
        self, 
        width: Optional[int] = default.WIDTH, 
        height: Optional[int] = default.HEIGHT,
    ):
        self.__width = width
        self.__height = height

    def print(self, env: env.Environment):
        env_grid = env.map.grid
        n_cols, n_rows = env_grid.shape
        
        assert self.__height % n_cols == 0, "display height is not divisible by number of columns in grid"
        assert self.__width % n_rows == 0, "display width is not divisible by number of rows in grid"
        
        cell_height = self.__height // n_cols
        cell_width = self.__width // n_rows

        # Print roads and sidewalks
        road_printer = RoadPrinter(
            screen=self.__screen, cell_width=cell_width, cell_height=cell_height,
        )
        sidewalk_printer = SidewalkPrinter(
            screen=self.__screen, cell_width=cell_width, cell_height=cell_height,
        )

        with np.nditer(env_grid, flags=["multi_index", "refs_ok"]) as it:
            for i in it:
                height, width = it.multi_index
                cell = env_grid[height, width]
                pos = grid.Position(width=width, height=height)
                if cell == grid.Cell.ROAD:
                    road_printer.print(pos)
                elif cell == grid.Cell.SIDEWALK:
                    sidewalk_printer.print(pos)

        # Print passengers
        pass_printer = PassengerPrinter(
            screen=self.__screen, cell_width=cell_width, cell_height=cell_height,
        )
        for p in env.passengers:
            pass_printer.print(p)

        pygame.display.flip()

    def __enter__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        return self

    def __exit__(self, ex_type, ex_val, ex_traceback) -> bool:
        pygame.quit()
        return False


class BasePrinter:
    def __init__(self, screen: pygame.Surface, cell_width: int, cell_height: int):
        self._screen = screen
        self._cell_width = cell_width
        self._cell_height = cell_height

    def get_cell_center(self, pos: grid.Position):
        left = pos.width * self._cell_width
        top = pos.height * self._cell_height
        return (left + self._cell_width // 2, top + self._cell_height // 2)

class CellPrinter(abc.ABC, BasePrinter):
    @abc.abstractmethod
    def colour(self):
        pass

    def print(self, pos: grid.Position):
        left = pos.width * self._cell_width
        top = pos.height * self._cell_height
        rect = pygame.Rect(left, top, self._cell_width, self._cell_height)
        pygame.draw.rect(self._screen, self.colour(), rect)


class RoadPrinter(CellPrinter):
    def colour(self):
        return (50, 50, 50)

class SidewalkPrinter(CellPrinter):
    def colour(self):
        return (30, 70, 30)

class PassengerPrinter(BasePrinter):
    def print(self, passenger: entity.Passenger):
        draw_radius = 0.9 * (min(self._cell_height, self._cell_height) // 2)
        
        pick_up_center = self.get_cell_center(passenger.pick_up)
        pygame.draw.circle(self._screen, (128, 0, 0), center=pick_up_center, radius=draw_radius)
        drop_off_center = self.get_cell_center(passenger.drop_off)
        pygame.draw.circle(self._screen, (0, 0, 128), center=drop_off_center, radius=draw_radius)