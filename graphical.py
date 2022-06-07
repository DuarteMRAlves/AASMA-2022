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
        grid: np.array
    ):
        # Mapping between the passenger Drop-Off location
        # and its colour.
        self._passenger_colours = {}
        self.grid = grid
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

        for pos in env.map.all_positions:
            if env.map.is_road(pos):
                road_printer.print(pos)
            elif env.map.is_sidewalk(pos):
                sidewalk_printer.print(pos)
            else:
                raise ValueError(f"Position not road or sidewalk: {pos}")

        # Print taxis
        taxi_printer = TaxiPrinter(
            screen=self.__screen,
            cell_width=cell_width,
            cell_height=cell_height,
            pick_colour_fn=self._pick_passenger_colour
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
            *colour.ROADS, *colour.SIDEWALKS, *colour.TAXI, *self._passenger_colours.values(),
        )
        self._passenger_colours[drop_off_loc] = new_colour
        return new_colour

    def __enter__(self):
        pygame.init()
        n_cells = self.grid.shape[0] * self.grid.shape[1]
        self.__width = self.__height = ((min(pygame.display.Info().current_w, pygame.display.Info().current_h) * 0.8) // n_cells) * n_cells
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

    def get_upper_left(self, pos: grid.Position) -> Tuple[int, int]:
        """Computes the upper left corner for a given position."""
        return pos.x * self._cell_width, pos.y * self._cell_height

    def get_cell_center(self, pos: grid.Position) -> Tuple[int, int]:
        """Computes the center pixels for a given position."""
        left, top = self.get_upper_left(pos)
        return left + self._cell_width // 2, top + self._cell_height // 2

    def get_px_side(self):
        """Computes the pixelart pixel size."""
        return int(self._cell_width // 16)


class CellPrinter(abc.ABC, BasePrinter):
    @abc.abstractmethod
    def colour(self):
        pass

    def print(self, pos: grid.Position) -> None:
        """Draws a rectangle of a given colour for the given position."""
        left = pos.x * self._cell_width
        top = pos.y * self._cell_height
        #Change function colour name
        self._screen.blit(self.colour(), (left,top))
        

class RoadPrinter(CellPrinter):
    def colour(self):
        #return colour.ROAD
        return pygame.transform.scale(pygame.image.load("Images/estrada.png"), (self._cell_width, self._cell_height))

class SidewalkPrinter(CellPrinter):
    def colour(self):
        #return colour.SIDEWALK
        return pygame.transform.scale(pygame.image.load("Images/passeio.png"), (self._cell_width, self._cell_height))

class TaxiPrinter(BasePrinter):
    def __init__(
        self,
        screen: pygame.Surface,
        cell_width: int,
        cell_height: int,
        pick_colour_fn: Callable[[entity.Passenger], colour.Colour],
    ):
        super().__init__(screen=screen, cell_width=cell_width, cell_height=cell_height)
        self._pick_fn = pick_colour_fn


    def print(self, taxi: entity.Taxi):

        car = pygame.transform.scale(pygame.image.load("Images/taxi.png"), (0.8*self._cell_width, 0.8*self._cell_height))

        left = taxi.loc.x * self._cell_width + 0.1 * self._cell_width
        top = taxi.loc.y * self._cell_height + 0.1 * self._cell_height

        if taxi.direction == entity.Direction.UP:
            taxi_sprite = pygame.transform.rotate(car, 0)
            
        elif taxi.direction == entity.Direction.DOWN:
            taxi_sprite = pygame.transform.rotate(car, -180)
            
        elif taxi.direction == entity.Direction.LEFT:
            taxi_sprite = pygame.transform.rotate(car, 90)
            
        elif taxi.direction == entity.Direction.RIGHT:
            taxi_sprite = pygame.transform.rotate(car, -90)

        if taxi.has_passenger is not None:
            draw_colour = self._pick_fn(taxi.has_passenger)
            # taxi_center = self.get_cell_center(taxi.loc)
            # px_side = self.get_px_side()
            x, y = self.get_upper_left(taxi.loc)

            taxi_rect = pygame.Rect(x, y, self._cell_width, self._cell_height)
            pygame.draw.rect(self._screen, draw_colour, taxi_rect)

            # taxi_rect1 = pygame.Rect(taxi_center[0] - (2 * px_side), taxi_center[1] + px_side, 4 * px_side, 4 * px_side)
            # taxi_rect2 = taxi_rect1.copy().inflate(2 * px_side, -2 * px_side)
            # taxi_rect3 = taxi_rect1.copy().inflate(-2 * px_side, 2 * px_side)
            # pygame.draw.rect(self._screen, draw_colour, taxi_rect1)
            # pygame.draw.rect(self._screen, draw_colour, taxi_rect2)
            # pygame.draw.rect(self._screen, draw_colour, taxi_rect3)

        self._screen.blit(taxi_sprite, (left, top))

        taxi_center = self.get_cell_center(taxi.loc)
        draw_text(self._screen, f"{taxi.id}", taxi_center, (0, 0, 0), 18, bold=True)

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
        # draw_radius = 0.9 * (min(self._cell_height, self._cell_width) // 2)
        draw_colour = self._pick_fn(passenger)
        pick_up_center = self.get_cell_center(passenger.pick_up)
        px_side = self.get_px_side()

        if passenger.in_trip in [entity.TripState.WAITING, entity.TripState.FINISHED]:
            pick_up_rect1 = pygame.Rect(pick_up_center[0] - (3 * px_side), pick_up_center[1] - (3 * px_side),
                                        6 * px_side, 6 * px_side)
            pick_up_rect2 = pick_up_rect1.copy().inflate(2 * px_side, -2 * px_side)
            pick_up_rect3 = pick_up_rect1.copy().inflate(-2 * px_side, 2 * px_side)
            pygame.draw.rect(self._screen, draw_colour, pick_up_rect1)
            pygame.draw.rect(self._screen, draw_colour, pick_up_rect2)
            pygame.draw.rect(self._screen, draw_colour, pick_up_rect3)

            passenger_center = self.get_cell_center(passenger.pick_up)
            draw_text(self._screen, f"{passenger.id}", passenger_center, (0, 0, 0), 18, bold=True)


        drop_off_upper_left = self.get_upper_left(passenger.drop_off)
        drop_off_rect = pygame.Rect(drop_off_upper_left[0], drop_off_upper_left[1],
                                    self._cell_width, self._cell_height)
        pygame.draw.rect(self._screen, draw_colour, drop_off_rect, 2 * px_side)


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