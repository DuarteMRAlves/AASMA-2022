import abc
import colour
import default
import entity
import env
import grid
import numpy as np
import pygame

from typing import Optional, Tuple

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
        colour_picker = colour.Picker()
        pass_printer = PassengerPrinter(
            screen=self.__screen, 
            cell_width=cell_width, 
            cell_height=cell_height,
            colour_picker=colour_picker,
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
        return colour.ROAD

class SidewalkPrinter(CellPrinter):
    def colour(self):
        return colour.SIDEWALK

class PassengerPrinter(BasePrinter):
    def __init__(
        self, 
        screen: pygame.Surface, 
        cell_width: int, 
        cell_height: int, 
        colour_picker: colour.Picker,
    ):
        super().__init__(screen=screen, cell_width=cell_width, cell_height=cell_height)
        self._picker = colour_picker

    def print(self, passenger: entity.Passenger):
        draw_radius = 0.9 * (min(self._cell_height, self._cell_height) // 2)
        draw_colour = self._picker.random(not_close=[colour.ROAD, colour.SIDEWALK])

        pick_up_center = self.get_cell_center(passenger.pick_up)
        pygame.draw.circle(self._screen, draw_colour, center=pick_up_center, radius=draw_radius)

        draw_text(self._screen, "Pick-Up", pick_up_center, (0, 0, 0), 18)

        drop_off_center = self.get_cell_center(passenger.drop_off)
        pygame.draw.circle(self._screen, draw_colour, center=drop_off_center, radius=draw_radius)

        draw_text(self._screen, "Drop-Off", drop_off_center, (0, 0, 0), 18)


def draw_text(
    screen: pygame.Surface,
    text: str, 
    center: Tuple[int, int], 
    color: Tuple[int, int, int], 
    size: int, 
    font: str = "arial", 
    bold: bool = False,
):
    font = pygame.font.SysFont(font, size, bold)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    rect.center = center

    screen.blit(surf, rect)