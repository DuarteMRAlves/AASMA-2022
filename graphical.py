import abc
import colour
import default
import entity
import env
import grid
import numpy as np
import pygame

from typing import Callable, List, Optional, Tuple

class EnvironmentPrinter(env.Printer):

    def __init__(
        self, 
        width: Optional[int] = default.WIDTH, 
        height: Optional[int] = default.HEIGHT,
    ):
        self.__width = width
        self.__height = height

        # Mapping between the passenger Drop-Off location
        # and its colour.
        self._passenger_colours = {}

        self._colour_picker = colour.Picker()

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

        # Print taxis
        taxi_printer = TaxiPrinter(
            screen=self.__screen, cell_width=cell_width, cell_height=cell_height,
        )
        for t in env.taxis:
            taxi_printer.print(t)

        # Print passengers
        self._remove_colours_for_disapeared_passengers(env.passengers)

        pass_printer = PassengerPrinter(
            screen=self.__screen, 
            cell_width=cell_width, 
            cell_height=cell_height,
            pick_colour_fn=self._pick_passenger_colour,
        )
        for p in env.passengers:
            pass_printer.print(p)

        pygame.display.flip()

    def _remove_colours_for_disapeared_passengers(self, passengers: List[entity.Passenger]):
        drop_off_locations = {p.drop_off for p in passengers}
        mark_for_delete = []
        for loc in self._passenger_colours:
            if loc not in drop_off_locations:
                mark_for_delete.append(loc)
        for loc in mark_for_delete:
            del self._passenger_colours[loc]

    def _pick_passenger_colour(self, p: entity.Passenger) -> colour.Colour:
        drop_off_loc = p.drop_off
        if drop_off_loc in self._passenger_colours:
            return self._passenger_colours[drop_off_loc]
        
        new_colour = self._colour_picker.random_not_close(
            colour.ROAD, colour.SIDEWALK, colour.TAXI, *self._passenger_colours.values(),
        )
        self._passenger_colours[drop_off_loc] = new_colour
        return new_colour

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

class TaxiPrinter(BasePrinter):
    def print(self, taxi: entity.Taxi):
        center_width, center_height = self.get_cell_center(taxi.loc)
        car_length = 0.9 * min(self._cell_height, self._cell_width)
        car_width = car_length // 2

        if taxi.direction in (entity.Direction.UP, entity.Direction.DOWN):
            left = center_width - car_width // 2
            top = center_height - car_length // 2
            rect = pygame.Rect(left, top, car_width, car_length)
        elif taxi.direction in (entity.Direction.LEFT, entity.Direction.RIGHT):
            left = center_width - car_length // 2
            top = center_height - car_width // 2
            rect = pygame.Rect(left, top, car_length, car_width)
        pygame.draw.rect(self._screen, colour.TAXI, rect)

        if taxi.direction == entity.Direction.UP:
            front_loc = (center_width, center_height - car_length // 2)
        elif taxi.direction == entity.Direction.DOWN:
            front_loc = (center_width, center_height + car_length // 2)
        elif taxi.direction == entity.Direction.LEFT:
            front_loc = (center_width - car_length // 2, center_height)
        elif taxi.direction == entity.Direction.RIGHT:
            front_loc = (center_width + car_length // 2, center_height)
        pygame.draw.line(self._screen, (0, 0, 0), (center_width, center_height), front_loc, width=2)


class PassengerPrinter(BasePrinter):
    def __init__(
        self, 
        screen: pygame.Surface, 
        cell_width: int, 
        cell_height: int, 
        pick_colour_fn: Callable[[entity.Passenger], colour.Colour],
    ):
        super().__init__(screen=screen, cell_width=cell_width, cell_height=cell_height)
        self._pick_fn = pick_colour_fn

    def print(self, passenger: entity.Passenger):
        draw_radius = 0.9 * (min(self._cell_height, self._cell_width) // 2)
        draw_colour = self._pick_fn(passenger)

        pick_up_center = self.get_cell_center(passenger.pick_up)
        pygame.draw.circle(self._screen, draw_colour, center=pick_up_center, radius=draw_radius)

        draw_text(self._screen, "Pick-Up", pick_up_center, (0, 0, 0), 16)

        drop_off_center = self.get_cell_center(passenger.drop_off)
        pygame.draw.circle(self._screen, draw_colour, center=drop_off_center, radius=draw_radius)

        draw_text(self._screen, "Drop-Off", drop_off_center, (0, 0, 0), 16)


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