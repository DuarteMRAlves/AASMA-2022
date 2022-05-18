import abc
import default
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

        road_printer = RoadPrinter(
            screen=self.__screen, width=cell_width, height=cell_height,
        )
        sidewalk_printer = SidewalkPrinter(
            screen=self.__screen, width=cell_width, height=cell_height,
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

        pygame.display.flip()

    def __enter__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        return self

    def __exit__(self, ex_type, ex_val, ex_traceback) -> bool:
        pygame.quit()
        return False


class CellPrinter(abc.ABC):
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        self.__screen = screen
        self.__width = width
        self.__height = height

    @abc.abstractmethod
    def colour(self):
        pass

    def print(self, pos: grid.Position):
        left = pos.width * self.__width
        top = pos.height * self.__height
        rect = pygame.Rect(left, top, self.__width, self.__height)
        pygame.draw.rect(self.__screen, self.colour(), rect)


class RoadPrinter(CellPrinter):
    def colour(self):
        return (50, 50, 50)

class SidewalkPrinter(CellPrinter):
    def colour(self):
        return (30, 70, 30)